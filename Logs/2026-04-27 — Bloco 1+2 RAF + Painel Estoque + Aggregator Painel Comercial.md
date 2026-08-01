---
data: 2026-04-27
tipo: implementação
projeto: Motor RAF + Reorganização Brutos + Painel Comercial
status: Bloco RAF fechado, Painel Comercial em curso (P1 fechado, P2-P6 pendentes)
relacionados:
  - "[[Logs/2026-04-25 — Fase 2A.1 + 2A.2 Proposta Prazo + Descrição]]"
  - "[[Sistema Operacional Comercial/01 RAF/01 - Estrutura RAF]]"
---

# Sessão 27/04/2026 — Bloco 1+2 RAF + Painel Estoque + Início Painel Comercial

Sessão longa cobrindo 3 frentes grandes:
1. Reorganização completa de `01_Brutos/` + Motor RAF de Enriquecimento (Bloco 1+2)
2. Bug fix Painel Estoque (colunas ABC/Tendência/Ruptura ausentes)
3. Início do Painel Comercial RAF (aggregator pronto, frontend amanhã)

## Bloco 1 — Reorganização de Brutos

**Antes**: `01_Brutos/Estoque/QRY_PPB Tabela.xlsx` + `Movimentação de estoque.xlsx`. Outras pastas reservadas (Cotacoes/Tabelas/Criterios) vazias.

**Depois**: 9 fontes canônicas em `01_Brutos/<Fonte>/<Fonte>.xlsx`:

| Fonte | Comportamento |
|---|---|
| RAF | substitutivo por ano (RAF_YYYY.xlsx) |
| PedidosEmitidos | acumulativo |
| CotacoesEncerradas | acumulativo |
| CotacoesPendentes | substitutivo |
| EstoquePadrao | substitutivo |
| MovimentacaoEstoque | substitutivo |
| FamiliasProdutos | substitutivo |
| FasesProducao | substitutivo |
| ListaClientes | substitutivo (base crua) |
| OrcamentoAnual | substitutivo (aguardando upload) |

Cada pasta tem README.md próprio. Motor (`MotorAnalitico/main.py` + `geradores/gerar_painel_estoque.py`) atualizado com globs novos + retrocompat (1-2 sessões pra paths antigos).

**Critérios + Dicionário** movidos pra paths canônicos:
- `MotorAnalitico/config/criterios_raf.xlsx` (input do motor)
- `06_Docs/Dicionario_RAF.xlsx` (referência humana)

## Bloco 2 — Motor RAF de Enriquecimento

`MotorAnalitico/raf/`:
- **lookup.py** — 8 dataclasses + 9 lookups O(1) (família, aço, bitola, comprimento, região SP, despesas)
- **enriquecer.py** — 10 funções puras de derivação (família, aço padrão, bitola, comprimento, cidade/região, tabela fechada, op_categoria, tipo_linha, corte, spreads, margens)
- **pipeline.py** — streaming I/O via openpyxl write_only
- **test_enriquecer.py** — 117 testes verdes
- **agregar_por_gerencia.py** — utilitário de bit-paridade contra tabela Gustavo
- **painel_aggregator.py** — pré-computa cubos OLAP pra Painel Comercial

### Comando

```bash
python3 MotorAnalitico/main.py --raf-enriquecer 2026    # 1 ano
python3 MotorAnalitico/main.py --raf-enriquecer all     # todos
```

### Output

`02_Derivados/RAF/RAF_enriquecido_YYYY.xlsx` com 32 colunas derivadas:
- Família canônica (207 combinações)
- Aço padronizado + tipo (Carbono / Beneficiamento / Cementação / Inox / Tubo / Manganês / Mola)
- Bitola padronizada (138 entradas)
- Comprimento segmento (31 segmentos A-ZH)
- Cidade revisada + Região SP (645 cidades)
- Tabela em que pedido fechou (V/A/V/Preta) + Dif% vs Vermelha
- Op_Categoria (7 categorias) + Op_Original
- Tipo_Linha + Considerar_Analise (Acessório/Sucata=False)
- Corte SN
- 7 spreads (cobrado − real)
- MC Aço + MC Spread + MC Total

### Performance

- RAF_2026 (18k linhas, 11MB): **35s** (sandbox)
- RAFs cheios (~50MB cada): **~6 min cada**, ~25 min total pros 4 anos local
- Throughput: ~520 linhas/s

### Numeração após Gustavo rodar local (`--raf-enriquecer all`)

| Ano | Linhas | Tempo | Output |
|---|---|---|---|
| 2023 | 77.544 | 148s | RAF_enriquecido_2023.xlsx (70 MB) |
| 2024 | 77.916 | 156s | RAF_enriquecido_2024.xlsx (70 MB) |
| 2025 | 79.349 | 149s | RAF_enriquecido_2025.xlsx (72 MB) |
| 2026 | 18.299 | 33s  | RAF_enriquecido_2026.xlsx (16 MB) |
| **Total** | **253.108** | **~8 min** | — |

## Achados estruturais ao longo do dia

### 1. Bug D17-18CrNiMo7-6 com tipo vazio na planilha
Fix: loader infere tipo via filtro irmão (R125 vazio → herda "Cementação" do filtro 17CrNiMo6). 328 linhas que vinham `Aco_Tipo=None` foram corrigidas.

### 2. 70 aços não mapeados (RAF_2026)
Categorizados em 3 grupos:
- **Grupo A** (24 chaves / 30 linhas): descrição vazada no ABCTIP → fix com regex em 3 níveis (match direto / extração / sem letra de sufixo)
- **Grupo B** (5 aços novos): 42CrMo4→4140, 1045H→1045, C45→1045, C45E→1045, 25MoCr4→20MnCr5
- **Grupo C** (Sucata/Acessório/Beneficiamento): `Aco_Tipo='N/A'` quando Tipo_Linha != 'Produto'

Resultado: **0 não mapeados** em RAF_2026 (era 70).

### 3. openpyxl corrompe fórmulas Excel ao salvar
Tentei adicionar 5 aços direto no `criterios_raf.xlsx` via openpyxl. Save destruiu valores cacheados de fórmulas Excel no bloco Bitola Padrão (cols `DE mm`/`DE Min`/`DE Max` viraram None). Library Python sem engine de cálculo.

**Solução**: criar `criterios_raf_overrides.yaml` ao lado do xlsx. Loader carrega ambos e mescla. Quando consolidar manualmente no xlsx (no Mac), apaga o YAML.

### 4. Beneficiamento com MC fictícia
Investigação das 12 NFs de Beneficiamento que apareceram com 100% MC negativa em RAF_2026. Achado: HKM e WEG TGM são **serviço puro** (matéria-prima do cliente). ABCCUS_ACO_COB == ValorTotal por convenção fiscal de remessa pra industrialização — NÃO é custo real Sacchelli.

**Regra aplicada**: quando `Tipo_Linha == 'Beneficiamento'`, motor força `MC_Aco = None` e `MC_Total = MC_Spread` (só margem do serviço prestado). Antes: 12/12 com MC negativa (R$ −140K). Depois: 0/12 com MC negativa, MC_Total = +R$ 38K (27,4% sobre R$ 141K em 3 meses).

### 5. Bit-paridade vs tabela dinâmica do Gustavo (RAF 2025)

Comparação contra `RAF_2025_CustoLote_Valuation.xlsx > Report` (agregado por gerência × 14 métricas):

**Batem bit-idêntico**: ValorTotal, ValorLIQ, Custo Aço, Externo, Comissão, Interno, Certificação, Financ, MC Aço (raw via ValorMC).

**Divergem sistematicamente**: Logística (motor 33-45% menor), DDV (3-5% menor), MC Spread (16-41% maior), MC Total (3-6% maior).

**Causa raiz**: pcts DDV/LOG da tabela do Gustavo são MAIORES e MAIS GRANULARES (variam por dimensão extra além de unidade × ano — provavelmente UF cliente / gerência). O motor usa pcts flat do `criterios_raf.xlsx` (que tem só os pcts COBRADOS).

**Decisão pragmática Gustavo**: até `OrcamentoAnual.xlsx` chegar com pcts reais discriminados, **tratar real = cobrado**. Spread DDV+LOG = 0. Quando OrcamentoAnual entrar, motor recalcula com pcts reais variáveis.

Implementação: `derivar_spread_cml` simplificado pra retornar `DDV_LOG_R_Real = ABCCUS_CML, DDV_LOG_Spread = 0`. DDV_R_Real / LOG_R_Real ficam None (sem visibilidade da divisão).

## Bug fix Painel Estoque

Gustavo flagrou que colunas ABC, Tendência e Ruptura não apareciam no painel.

**Diagnóstico**: arquivo `MovimentacaoEstoque.xlsx` em `01_Brutos/` tinha apenas 28 bitolas (export filtrado/parcial). Pros 499 itens restantes (95% do estoque), código JS caía no fallback `r[9]='—'`.

**Fix**: Gustavo subiu versão completa (527 bitolas — match 1:1 com estoque). Painel regenerado mostra 100% das colunas. **Nota pro README de MovimentacaoEstoque**: documentar critério de export do Softcomp pra evitar repetição do problema.

Cache localStorage pode ter `_needsABC` desatualizado bloqueando recálculo — instrução: hard reload (Cmd+Shift+R) ou limpar localStorage no DevTools.

## Início do Painel Comercial RAF

Decisão estratégica: HTML standalone com 4 anos embutidos, modelo DRE do pedido, Chart.js, ano corrente como filtro padrão, Considerar_Analise=True default.

5 tabs propostas:
1. **DRE Comercial** (waterfall + decomposição MC Aço + Spread + Total)
2. **Heatmap MC Gerência × Família**
3. **Carteira de Cliente** (Pareto ABC, top 50, mapa Risco/Joia)
4. **Evolução 2023-2026** (linhas/áreas mensais)
5. **Tabela Preta drilldown** (top 200 NFs por perda estimada)

KPI bar fixa no topo: Receita Líq / Custo Aço% / MC Aço% / MC Spread% / MC Total% / Tabela Preta% / N NFs / Concentração top10 / Ticket médio.

### P1 fechado — Aggregator (`MotorAnalitico/raf/painel_aggregator.py`)

Pré-computa 2 cubos + 2 listas:
- **Cubo principal** (sem cliente): (ano, mes, ger, fam, op_cat, tipo, tab, considerar) — denso, ~500-2000 células por ano
- **Cubo cliente** (separado): (ano, cliente, considerar) — pra Tab Carteira
- **carteira_top200**: top 200 clientes por receita
- **tabela_preta_top200**: top 200 NFs por perda estimada (R$ acima da Vermelha × Quantidade)

Saída JSON-serializable pra injetar no template HTML.

### P2-P6 pendentes (próxima sessão)

- **P2** Template HTML (5 tabs + KPI bar + filtros globais)
- **P3** Render JS reativo (Chart.js + filtros)
- **P4** Comando `--painel-raf` no main.py
- **P5** Smoke + validação cruzada
- **P6** Validação produção

Estratégia escolhida: 3 etapas validáveis — A (KPI bar + DRE), B (Heatmap + Carteira), C (Evolução + Preta). Cada etapa entrega algo navegável.

### Etapa A FECHADA na sequência (27/04 fim do dia)

P2-P6 entregues no mesmo dia.

- **P2/P3** — `03_Ferramentas/Painel_Comercial_RAF.html` (~600 linhas, single file). Header + 5 tabs (DRE ativa, demais como esqueleto rotulado "Etapa B/C"). Filtros globais: ano (default = ano corrente), gerência, op_categoria, considerar=true. KPI bar com 9 KPIs (Receita, Custo Aço%, MC Aço%, MC Spread%, MC Total%, Tabela Preta%, Linhas, Ticket, Conc. Top 10). DRE Comercial: waterfall Receita → −Custo Aço → MC Aço → +Spread → MC Total + barras horizontais por componente do spread + tabela DRE detalhada com 7 sub-linhas de spread (COR/CER/INT/REP/FIN/EXT/CML). Estado em closure, render por callback nas mudanças de filtro. Marcador inline `const PD = {...};` pra injection.
- **P4** — `--painel-raf` no `MotorAnalitico/main.py`. Chama `painel_aggregator.construir_painel_data()`, serializa JSON, injeta in-place no template via regex `const PD = \{[\s\S]*?\};`. Output: 03_Ferramentas/Painel_Comercial_RAF.html (overwrite). Funciona com `--all` também. JSON do RAF_2026 = 456KB minified (~2k células no cubo).
- **P5** — Validação bit-paridade contra soma direta do RAF_2026 enriquecido. **0 divergência** em ValorLIQ, Custo Aço, MC Total, Tabela Preta R\$/n — total e considerar=true. **6/6 gerências** com MC% idêntica ao ground truth. Tabela Preta agregada = 15,36% (R\$ 7,58 MM em 1.412 NFs) — bate com achado do Bloco 2.
- **P6** — Self-check: regex injetou (1 substituição), JSON re-parseável, template abre direto sem servidor (file://), tabs disabled bloqueiam navegação até Etapa B/C, KPIs com cores condicionais (MC Total ≥30% verde, Tabela Preta ≥12% vermelho).

### Pra Gustavo rodar local

```bash
python3 MotorAnalitico/main.py --painel-raf
```

Vai processar os 4 anos (2023-2026) do `02_Derivados/RAF/`. Tempo esperado: ~8 min (cada ano cheio ~2 min de leitura). Output substitui o template in-place. Abrir `03_Ferramentas/Painel_Comercial_RAF.html` no navegador.

### Próximos passos

- **Etapa B**: Heatmap MC (Gerência × Família) + Carteira ABC (Pareto top200). Cubo cliente já agregado no aggregator. ~2h.
- **Etapa C**: Evolução mensal 2023-2026 (linha tempo) + Drilldown Tabela Preta (top 200 NFs já agregadas). ~2h.
- **Refino KPI Conc. Top 10**: hoje é proxy do top200 não filtrado por ano. Resolver com cubo cliente filtrável (parqueado pra Etapa B).

---

## Tentativa de fechar Camada 2 (DDV+LOG real) — PARQUEADA

Gustavo subiu os 4 orçamentos (2023-26). Plano era extrair real DDV (XX.16.*) e real LOG (XX.12.*) por (ano, unidade) das folhas do plano de contas, derivar pcts e injetar no motor RAF.

**Achados que travaram a tese**:

1. **Plano de contas mudou em 2024**: 2023 usa `01-06`, 2024 é transição (01-06 + 71-76 paralelos), 2025-26 usa `71-76`. Resolvido com mapeamento por ano.

2. **Outras unidades não-mapeadas**: `78` (Anchieta, R$ 174k LOG 2025), `30.*` (Corporativo Sacchelli — RH/Adm/Marketing/Jacareí/Itajaí com `30.18.13 DESPESAS COMERCIAL`). Não entram nas 6 unidades comerciais mas têm despesa.

3. **Comissão Representantes**: `XX.16.02.102` somou R$ 553k em 2025 vs R$ 927k no Report. Discrepância de **+67%** numa conta-folha simples. Sintoma definitivo: **o Report não é realizado contábil — é modelo paralelo do Gustavo com pcts granulares (UF cliente / gerência) e alguma alocação extra (overhead? rateio do Corporativo nos comerciais?) que não vive nos orçamentos brutos**.

4. **Gap total 2025**: orçamento 6 unidades = R$ 14,53 MM vs Report R$ 15,95 MM = **-8,9%**.

**Decisão**: Gustavo parou a tese ("acho que vai dar ruim essa análise"). Decisão correta — orçamento bruto não reconstrói o Report.

**Caminhos alternativos parqueados pra retomar**:

- **B (preferível)**: Gustavo exporta os pcts granulares dele direto da tabela dinâmica (não reconstruir, copiar). Bateria bit-idêntico com Report. Trabalho dele: 10-15 min.
- **C**: usar realizado contábil dos orçamentos como "MC econômica conservadora". MC do painel cairia ~3 MM em 2025 (de 32,77% pra ~31,2%, próximo dos 31,37% do Report). Não bate idêntico mas captura margem oculta DDV+LOG. Trabalho meu: 1h.

**Artefatos que ficam de pé**:

- `01_Brutos/OrcamentoAnual/OrcamentoAnual.xlsx` — preenchido com realizado contábil 2023-26 × 6 unidades × {DDV, LOG}. Útil pra análises de aderência ao plano mesmo sem virar input do motor.
- `01_Brutos/OrcamentoAnual/README.md` — documentação técnica completa.
- Aprendizado: orçamento bruto ≠ pcts granulares do Report. **Distinção importante**: os pcts do Gustavo aplicam algum rateio/overhead que não está nas folhas. Pra reconstruir, precisaria do modelo dele.

**Painel mantém-se na regra original**: `real_DDV+LOG = cobrado` (spread = 0) até decisão de retomar via caminho B ou C.

---

## Reconciliação contra Report v2 — fechada (Caminho A)

Gustavo enviou nova versão do Report (`RAF_2025_CustoLote_Valuation-b657b6c4.xlsx`) **simplificada**: fundiu DDV+LOG em coluna única "Comercial + Logística" trocando a fonte pra `Sum of ABCCUS_CML_COB` — exatamente a coluna que o painel já lia. Mudou o jogo.

### Bit-paridade contra Report v2 (2025, sem filtro Considerar)

| Métrica | Painel | Report v2 | Δ |
|---|---:|---:|---:|
| ValorLIQ | 230,42 MM | 230,21 MM | +0,09% ✓ |
| Custo Aço | 127,46 MM | 127,16 MM | +0,24% ✓ |
| Externo | 7,90 MM | 7,89 MM | +0,16% ✓ |
| **CML (DDV+LOG)** | **17,68 MM** | **17,67 MM** | **+0,05% ✓** |
| Comissão REP | 0,93 MM | 0,93 MM | **0,00% ✓** |
| Financeiro | 5,14 MM | 5,14 MM | +0,01% ✓ |
| Interno | 0,29 MM | 0,29 MM | 0,00% ✓ |
| Certificação | 0,64 MM | 0,64 MM | +0,01% ✓ |
| MC Aço | 58,38 MM | 58,13 MM | +0,43% ✓ |
| MC Total | 75,51 MM | 72,22 MM | **+4,56% (margem oculta)** |

Todas as bases batem bit-paridade. Ruídos de 0,01-0,43% são correções de Beneficiamento e remapeamento de aços do enriquecimento.

### Diferença residual em MC Total = +R$ 3,3 MM (+1,40 pp)

Não é mais erro de fonte — é diferença de **modelo de cálculo**:
- **Report v2** soma a coluna `MC Total R$` do RAF cru (pcts internos do Gustavo).
- **Painel** calcula `MC Total = MC Aço + Spread (cobrado − real)` usando pcts do `criterios_raf.xlsx`.
- Motor reconhece **R$ 3,3 MM de margem oculta** nos 6 componentes não-DDV/LOG (Externo, REP, Fin, Int, Cer, Corte) onde cobrado > real.

### Decisão Caminho A — aceitar e documentar

Diferença é a tese central do projeto (`project_raf_convencao_softcomp.md` — MC contábil vs MC econômica). Painel mostra **margem oculta capturada**, Report mostra **MC contábil pura**.

**Implementação 27/04 (fim do dia)**:
- Bloco visual `info-note` adicionado no painel (DRE — Vista Tabular) explicando a tese inline.
- Log fechado.
- Painel Etapa A 100% fechada, sem pendências.
- Tentativa de ajuste via orçamento (Caminhos B/C) parqueada — pode voltar se Gustavo quiser bater bit-idêntico.

### Pra Etapas B e C (próxima sessão)

Etapa A fechada com 11 indicadores + DRE + nota tese. Próximas:
- **Etapa B**: Heatmap MC + Carteira ABC já implementadas (achadas no template do Gustavo). Validar visual e refinar UX.
- **Etapa C**: Evolução mensal + Tabela Preta drilldown idem.

## Limpeza CLAUDE.md

Reescrito do zero: 55k → 16k chars (-70%). Mantidas seções operacionais vivas (Estrutura, Política de dados, Nomes canônicos, Motor, Regras técnicas, Pra retomar, Duferco). Descartado histórico detalhado de Camadas 1-11, Bugs 1-5 da Proposta, Sprints W3a-W3e (consolidado em "Wrapper W3 fechado") — tudo preservado em logs de abr/2026.

## Estado das pendências

| # | Frente | Status |
|---|---|---|
| #17 | Validação Fase 2B Proposta | Pending desde 25/04 (5 min Gustavo) |
| #41 | Rodar 2023/2024/2025 RAF | Concluído hoje (Gustavo rodou local) |
| OrcamentoAnual.xlsx | Aguardando upload | Destrava spread DDV+LOG real |
| Fase 2C Proposta (NCM+IPI) | Aguardando mapeamento família×NCM + TIPI | ~3-5h |
| Painel RAF Comercial | P1 fechado, P2-P6 pendentes | Etapa A (~1h) próxima sessão |
| Setup Proposta em 5 abas (#56) | Parqueada | UX, não bloqueia |

## Pra retomar amanhã

`arrancar etapa A painel raf` — KPI bar + DRE Comercial. Aggregator já gera dados. Foco: fazer as primeiras KPIs aparecerem na tela com filtros funcionais (período, gerência), validar números contra `agregar_por_gerencia.py`. ~1h. Sem decisões pendentes.

Outras frentes possíveis (em ordem de valor):
- `validar fase 2b proposta` (#17, 5 min)
- `Fase 2C Proposta` (Gustavo traz mapeamento NCM)
- Análise estratégica Duferco-Brasil (prazo final abril/2026)
