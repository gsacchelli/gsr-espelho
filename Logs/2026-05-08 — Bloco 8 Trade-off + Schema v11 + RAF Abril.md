# 2026-05-08 — Bloco 8 Trade-off + Schema v11 + RAF Abril

Sessão consolidada. Ingestão de Abril/26, integração da análise de Trade-off Desconto × Volume no Painel Comercial RAF (bloco 8 do Pricing V3), correção arquitetural do `cubo_cliente` pra filtrar por período (BCG), e revisão metodológica de filtros de Tabela Preta.

## Decisões registradas

### 1. RAF é Acumulativo mensal por ano, não Substitutivo

`CLAUDE.md` documentava RAF como "substitutivo por ano" assumindo que Softcomp exportava YTD. **Falso.** Softcomp só exporta um mês por vez. Pra atualizar Abril/26, Gustavo abriu `RAF_2026.xlsx` (Jan-Mar) no Excel, colou Abril ao final, salvou.

**Validação manual passou:**
- 5.526 linhas Abril (em linha com média 5-6k/mês)
- Range datas: 05/01/2026 a 30/04/2026
- Zero datas inválidas
- Zero duplicatas pela chave `ABCFILIAL + ABCNNF_CI + ABCNNF_NUM + ABCNNF_ITE`
- 133 colunas preservadas

**Próxima sessão (antes do export de Maio):**
Refatorar RAF como Acumulativo automático no padrão dos outros brutos:
- Salvar como `RAF_2026_novo.xlsx`
- Motor faz append + dedupe por chave composta + grava em `RAF_2026.xlsx` consolidado + deleta `_novo`
- Detecta retroativos (NFs com mesma chave mas valor diferente) e loga warning
- Atualizar CLAUDE.md + README de `01_Brutos/RAF/`

Custo: ~2h. ROI: tira passo manual de Excel da rotina mensal e elimina risco de pastar duas vezes ou pular linhas.

### 2. Filtro canônico de pricing comercial: `Op_Categoria == 'Venda'`

Investigação na coluna `ABCPFA_DES` revelou que o motor classificava como Preta várias notas que não são pricing comercial. **Decisão Gustavo:**

**Saem da análise de Trade-off:**
- Devoluções (`Op_Categoria == 'Devolução'`): DEVOLUCAO DE VENDA, DEVOLUÇÃO VENDA CONSUMO — 12 linhas YTD, R$ -259k em ValorLIQ. Motor classifica como Preta porque o sinal negativo bagunça o flag de tabela.
- Consumo Próprio (`Op_Categoria == 'Consumo Próprio'`): VENDA CONSUMO PROPRIO + VENDA TRIANGULAR CONSUMO — transferências internas, preço não-comercial.
- Exportação Direta (`Op_Categoria == 'Exportação'`): regime fiscal próprio (USD, sem ICMS/IPI), Vermelha BR não aplica.
- Beneficiamento (`Op_Categoria == 'Beneficiamento'`): matéria-prima do cliente, ABCCUS_ACO fictício.
- Faturamento de Consignação: SIMPLES FATUR.CONSIGNACAO — não é venda nova.

**Mantidas como venda comercial padrão:**
VENDA, VENDA TRIANG., VENDA REPETRO + variantes, VENDA ICMS DIFERIDO, VENDA-REIDI, VENDA C/ DIFERIMENTO ICMS, VENDA ESPECIAL, VENDA (UP), VENDA PARA ENTREGA FUTURA.

Total removido em Preta YTD: 73 linhas, R$ 1,03 MM.

### 3. Schema v11 do Painel Comercial RAF

Bumpado de v10 (estado matinal) → **v11-2026-05-08** com duas mudanças:

**a) Campos novos em `nfs_preta`:**
```
+ ano, mes, op_cat, mc_total_rs, desc_pct, faixa_desconto
```
Helper `_faixa_desconto(d)` adicionado ao aggregator com 7 buckets (0-1%, 1-3%, 3-5%, 5-10%, 10-15%, 15-20%, 20%+).

**b) `cubo_cliente` ganha dimensão `mes`:**
```diff
- (ano, cliente, gerencia, vendedor, op_cat, considerar)
+ (ano, mes, cliente, gerencia, vendedor, op_cat, considerar)
```
Cresceu 3,8× em rows (10k → 38k). `painel_data.js`: 88 MB → 99,8 MB.

**c) Lista paralela `tabela_preta_full`:**
Sem cap (vs `tabela_preta_top` cap 5000). Necessária pro bloco 8 porque cap global ordenado por perda_estimada truncava 2026 (anos antigos com R$ históricos altos dominavam o top). Rendia 717 NFs em vez de 1.811.

### 4. Bloco 8 — Trade-off Desconto × Volume

Inserido no Pricing V3 do painel, logo após o Cohort. Responde a filtros globais (ano, mês ini/fim, gerência, vendedor). Filtra `op_cat == 'Venda'` automaticamente.

**Componentes:**
- KPI bar: Linhas Preta, Desconto médio ponderado, Vol. extra necessário, Desconto concedido total + break-even
- Tabela operacional por faixa de desconto (clicável pra filtrar drill-down)
- Curva: % volume extra necessário por faixa
- Faturamento + desconto concedido por faixa
- 4 cenários comparativos: Real / Vermelha 0% perda / Break-even / Vermelha 50% perda
- Drill-down de NFs com paginação (50/página, ordenado por perda_estimada desc)

**Terminologia:** "margem queimada" → "desconto concedido" / "Desc. R$" (decisão UX Gustavo).

### 5. Decisão metodológica: margem queimada precisa

Aproximação anterior (`desc_pct × valor_liq`) subestimava porque usava `valor_liq` (preço já descontado) como base. Métrica correta: **`(preço_vermelha − preço_fechado) × qtd`** — exatamente quanto faltou pra atingir o piso. Já calculada no motor como `perda_estimada`.

Reflete diferença real:
- YTD 2026 Op=Venda: aproximação dava R$ 564k. Métrica precisa: **R$ 773k**.
- Volume extra necessário: aproximação +23,5% → preciso **+32,2%**.
- Anualizado: ~R$ 2,32 MM/ano de desconto teórico.

Painel passou a usar a métrica precisa.

### 6. Standalone descontinuado

`03_Ferramentas/Analise_Tradeoff_Preta.html` — apagado (manualmente pelo Gustavo). Funcionalidade integrada ao painel principal.

## Achados de negócio (mantidos do log de 03/05 + novos de Abril)

**DRE Abril/26:**
- Faturamento líquido R$ 16,53 MM (2º melhor mês YTD).
- MC% **32,17%** — melhor mês do quadrimestre.
- Tabela Preta: **15,58%** (vs Mar 12,15%, regrediu +3,4 pp). Verde explodiu pra R$ 8,50 MM (+41% vs Mar) — compensou Preta no MC%, mas frágil.

**Tabela Preta YTD 2026 (pós filtro Op=Venda):**
- 1.811 linhas, R$ 9,62 MM faturado, MC R$ 2,40 MM (24,9%).
- Desconto médio ponderado: 5,9%.
- Faixas críticas:
  - **5-10%** desc: 442 linhas, R$ 250k MQ, +30% vol extra (concentra o vazamento absoluto).
  - **10-15%** desc: 198 linhas, MC% 11,4%, +119% vol extra (inviável compensar).
  - **20%+** desc: 133 linhas, R$ 142k volume, +256% vol extra (auditar caso a caso).

**Bloqueios pricing validados:**
- Aline Damin Fortes: 65% do volume dela em Preta — bloqueio 05/05 justificado.
- TER BRASIL: 95% do volume em Preta — bloqueio 05/05 justificado.
- Reincidência piorando — Jaqueline Pereira de Melo: Q1 R$ 100k Preta → Abr R$ 220k (+120%, ticket subiu de R$ 2,4k → R$ 7,1k/linha). Candidata a bloqueio antes da revisão dura de 31/07.
- Fabiola Cardoso Piazza: R$ 22k MQ YTD — em linha com a previsão do Plano Pricing Discipline 30/04.

**Famílias críticas:**
- 20MnCr5 R L 12,70-101,60: MC% Preta 12% (vs 27% Vermelha). Concorrência forte ou tabela Vermelha mal calibrada — investigar.

**Clientes a auditar (top desconto concedido YTD):**
1. TER BRASIL — R$ 94k MQ (bloqueado 05/05 ✓)
2. ARCO — R$ 65k MQ
3. PROTENDE ABS — R$ 29k MQ
4. TRATORGEL 2 — R$ 24k MQ
5. MAHLE — R$ 23k MQ

## Pendências parqueadas

- **Refator RAF Acumulativo automático** (custo ~2h, ROI imediato a partir de Maio)
- **Conversão dos enriquecidos para parquet** — aggregator carrega 4 RAFs de ~70 MB cada via openpyxl em ~3 min. Parquet reduziria para ~20s. Custo ~1h, ROI: pipeline mensal de 3 min → 20s, viabiliza rodar daqui no Cowork sem stress de timeout.
- **Atualização do CLAUDE.md** — corrigir classificação RAF (substitutivo → acumulativo), atualizar SCHEMA_VERSION pra v11, documentar bloco 8 do Pricing V3, documentar `tabela_preta_full`, atualizar comandos pendentes.
- **Auditar 133 NFs faixa 20%+ desconto** — caso a caso, foco em margem agregada baixa (R$ 17k MC em R$ 142k fat). Suspeita: cadastro de custo errado em alguns SKUs, ou política deliberada bizarra.
- **Investigar família 20MnCr5** — MC% 12% em Preta vs 27% Vermelha. Possível recalibração da tabela Vermelha pra essa família.

## Comandos novos

```bash
# Painel RAF com schema v11 (Bloco 8 + cubo_cliente com mes)
python3 MotorAnalitico/main.py --painel-raf

# Validar bloco 8 no painel: aba Pricing V3, role até final
# Filtros globais (ano, mês, gerência, vendedor) ativos
```
