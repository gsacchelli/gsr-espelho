---
data: 2026-06-02
tipo: log
status: vigente
tags: [motor-cotacoes, motor-pedidos, politica-dados, refactor, bug, analise-big4, win-rate, cross-check]
relacionado: 
---

# Refactor Cotações pra política anual + descoberta bug gap_cot_ped_pct + análise big4

## TL;DR

Sessão de 3 frentes consecutivas:

1. **Fix do bug `valor_orc_previo`** (continuação 01/06): Cotações schema v2.4, Win Rate ajustado YTD 2026 passa de "24% reportado, 40% real" para 40,2% lido direto do cubo. Documentado em log próprio.
2. **Descoberta de problema estrutural na cadeia de export**: `CotacoesEncerradas.xlsx` foi configurada no Softcomp como **janela rolante ~3 meses**, não como acumulativo. Cada export sobrescrevia o anterior e perdia histórico. Refatoração: política passa a ser **"substitutivo por ano"** espelhando RAF e Pedidos. Arquivo canônico: `CotacoesEncerradas_YYYY.xlsx`. Anos fechados imutáveis.
3. **Novo bug descoberto**: `gap_cot_ped_pct` no cross-check pedido↔cotação está contaminado por **mismatch de unidade PU** (R$/peça vs R$/kg). Métrica agregada inflada para R$ 9,7 bi ponderado (faturamento total YTD = R$ 373 MM — magnitude impossível). Fix ainda não aplicado, decisão pendente.

Bonus: com **2025 inteiro + 2026 jan-jun** agora disponíveis, cobertura cross-check pedido↔cotação saltou de **15,2% → 87,2%**. Universo de cotações triplicou (44k → 242k → ~250k+).

## Frente 1: refactor pra política anual

### Causa-raiz do problema operacional

`01_Brutos/CotacoesEncerradas/CotacoesEncerradas.xlsx` era **substitutivo único** (1 arquivo só, sobrescrito a cada export). README dizia "acumulativo" mas o Softcomp exportava janela rolante. Resultado: a cada export, perdia-se cobertura dos meses mais antigos.

Histórico verificado:
- **Export 09/05/2026** (15 MB): cobria **02/01/2026 → 08/05/2026**
- **Export 01/06/2026** (9 MB, MENOR): cobria **02/03/2026 → 01/06/2026** — perdeu jan-fev/26
- **Cross-check pedido↔cotação caiu de 22,2% → 15,2%** como artefato

Diferenças de tamanho deveriam ter sido red flag em revisão semanal, mas não havia validação automática de "arquivo NOVO ≥ arquivo ANTIGO em tamanho/itens" no pipeline. Política era confiar no export do Softcomp ser bem-feito.

### Fix aplicado

**`MotorAnalitico/cotacoes/pipeline.py`** — refatorado:

1. Novo `src_encerradas_arquivos() -> list[Path]`: faz `glob('CotacoesEncerradas*.xlsx')` na pasta de brutos, retorna lista ordenada. Filtra duplicatas (sufixo `(1)`, `- cópia`, `~$`).
2. `src_encerradas()` mantida como compat (retorna 1º arquivo) — sem quebrar callers.
3. Nova função `enriquecer_consolidado(srcs, dst, ...)`: processa N inputs num único output. Espelha exatamente o padrão de `MotorAnalitico/pedidos/pipeline.py`.
4. `enriquecer_encerradas()` agora chama `enriquecer_consolidado(src_encerradas_arquivos(), dst_encerradas())`.
5. Aggregator (`cotacoes/aggregator.py`) sem mudança: continua consumindo 1 arquivo enriquecido consolidado.

**Renomeação:** `01_Brutos/CotacoesEncerradas/CotacoesEncerradas.xlsx` → `CotacoesEncerradas_2026.xlsx`.

**README atualizado** (`01_Brutos/CotacoesEncerradas/README.md`): política substitutiva por ano, motivação histórica, contrato consumer/producer.

**CLAUDE.md atualizado** em 3 pontos: árvore, tabela de nomes canônicos, descrição do pipeline de cotações.

### Validação

Smoke test: `--cotacoes-enriquecer` rodou 44.207 linhas em 28,8s (1535 l/s, mesma performance da versão single-file). Bucket distribution intacta. Bug #1 (`valor_orc_previo`) já corrigido aparece com R$ 138,4 MM populados corretamente.

## Frente 2: 2025 + 2026 inteiros entram

Gustavo exportou 2 arquivos novos:
- `CotacoesEncerradas_2025.xlsx` — 48 MB, cobre **02/01/2025 → 31/12/2025** (198.072 itens)
- `CotacoesEncerradas_2026.xlsx` (3ª versão de hoje) — 18 MB, cobre **02/01/2026 → 02/06/2026** com jan-fev incluídos

Total consolidado: **~250.000 cotações**, R$ 1,92 bi cotado.

### Impacto na cobertura cross-check pedido↔cotação

| Versão | Universo cotações Ganhou | Cobertura pedidos |
|---|---:|---:|
| Export 09/05 + Pedidos hoje | 23.046 | 22,2% |
| Export 01/06 + Pedidos hoje | 16.118 | 15,2% (piorou — janela rolante perdeu jan-fev/26) |
| Política anual + 2025 inteiro | 91.032 | 87,2% |
| **Política anual + 2025 + 2026 completo** | **102.136** | **97,9%** ✓ |

Distribuição final por mês: todos os 17 meses entre jan/25 e mai/26 entre **93,8% e 99,5%** de cobertura. Apenas 2.074 pedidos cold reais (2,1%) — sem cotação prévia identificável (clientes que ligam e fecham direto, sem orçamento formal).

Cobertura cross-check é o que destrava o cálculo de margem oculta real por pedido — capítulo 4º estágio "NF Faturada" do funil consolidado fica viável quando combinado com RAF.

## Frente 3: novo bug descoberto — `gap_cot_ped_pct` contaminado

### Sintoma agregado

Log do `--pedidos-crosscheck` reportava:
- Gap médio: **+55,61%**
- Gap R$ ponderado (kg × delta_pu): **R$ +9.726.202.044** (9,7 bilhões)

Magnitude impossível: faturamento total YTD da AFS é R$ 373 MM. Métrica agregada está inflada por outliers.

### Causa-raiz

Cross-check em `MotorAnalitico/pedidos/cross_check_cotacao.py` calcula `gap = (pu_ped - pu_cot) / pu_cot` **sem normalizar unidades**.

Distribuição de `unid_pu` nos pedidos:
- KG: 59.308 (62%) — PU em R$/kg
- **PÇ: 27.342 (27%)** — PU em **R$/peça**
- M: 908 (1%)
- (resto sem unid_pu)

Cotações têm PU sempre em R$/kg. Quando pedido com `unid_pu='PÇ'` é cruzado, compara-se `R$/peça vs R$/kg` — sem sentido matemático.

### Distribuição real do gap

| Bucket | Count | % |
|---|---:|---:|
| ±1% mantido | 85.658 | **97,8%** |
| -10 a -1% | 615 | 0,7% |
| +1 a +10% | 430 | 0,5% |
| -50 a -10% | 271 | 0,3% |
| +10 a +50% | 204 | 0,2% |
| **>+1000% (outliers)** | **148** | **0,2%** |
| +200 a +1000% | 109 | 0,1% |
| <-50% | 65 | 0,1% |
| +50 a +200% | 58 | 0,1% |

A maioria (97,8%) bate em ±1% — gap real é negligenciável. Mas os 0,5% de outliers (~470 itens) com gap entre +200% e **+918.000%** inflam a média ponderada por R$ várias ordens de magnitude.

### Top 5 outliers (todos `unid_pu='PÇ'`)

| Gap | PU pedido | PU cotação | Unid PU | R$ Total |
|---:|---:|---:|---|---:|
| +918.102% | 133.231,13 | 14,51 | PÇ | R$ 532.924,52 |
| +652.348% | 94.670,22 | 14,51 | PÇ | R$ 568.021,32 |
| +402.115% | 57.918,94 | 14,40 | PÇ | R$ 57.918,94 |
| +358.157% | 50.908,34 | 14,21 | M | R$ 17.817,91 |
| +247.900% | 36.852,80 | 14,86 | PÇ | R$ 36.852,80 |

Confirma o diagnóstico: PU em R$/peça (na casa dos R$ 50k-130k por peça) sendo comparado com PU em R$/kg (~R$ 14/kg).

### Fix aplicado e validado (02/06/2026 noite)

Schema Pedidos `v3-2026-05-11` → **`v4-2026-06-02`**.

**Lógica aplicada em duas camadas:**

1. **Indexação de cotações** (`indexar_cotacoes_ganhou`): calcula `pu_kg_cotacao = valor_total/kg` apenas quando `tipo_item='catalogado'`. Engenheiradas ficam com `None` porque `kg` nelas é nº de peças (caveat já documentado).
2. **Cruzamento por linha** (`cruzar_pedido`): calcula `ped_pu_kg = valor_total/kg` apenas quando `unid_pu='KG'`. Pedidos em `unid_pu='PÇ'` ficam com `None` honesto.
3. **Comparação**: só gera `gap_cot_ped_pct` quando ambos os lados têm valor (catalogado × KG).

**Novas colunas no enriquecido** (debug explícito): `cot_pu_kg`, `ped_pu_kg`.

### Resultado da validação

| Métrica | v3 (bug) | v4 (fix) | Sanidade |
|---|---:|---:|---|
| Gap médio | **+55,61%** | **+0,27%** | ✓ realista |
| Gap R$ ponderado | R$ +9.726 MM | **R$ +0,585 MM** | ✓ dentro do faturamento (R$ 374 MM) |
| Pedidos com gap calculado | 98.328 (forçado) | **66.547** | honesto — só onde comparável |
| Pedidos sem comparação | 0 | 31.781 | PÇ ou cotação engenheirada |
| Recuperou / Cedeu / Mantido | 1.086 / 1.050 / 96.192 | 544 / 562 / 65.441 | equilíbrio próximo |
| Direção do ajuste agregado | viesada | **+0,27% recuperou** | leve recuperação líquida |

### Achado de negócio do gap corrigido

Vendedores **recuperaram +R$ 585 mil** líquidos vs PU cotado nos pedidos fechados (gap R$ ponderado positivo). Distribuição:
- 544 pedidos com PU **superior** ao cotado (recuperação ativa)
- 562 pedidos com PU **inferior** ao cotado (concessões)
- Saldo líquido R$ +585k em ~66k pedidos = R$ 9 por pedido em média — disciplina de pricing aplicada com mão leve.

Sinal de que o motor de Pricing Discipline (bloqueios + alertas) está funcionando: ajustes pós-fechamento são pontuais, não sistêmicos. Os 1,7% dos pedidos com ajuste relevante (>1%) carregam quase todo o sinal — útil pra auditoria caso a caso.

## Frente 4: análise big4 do painel pós-fix

### KPIs por ano (universo completo 2025 + 2026 YTD completo após inclusão jan-fev)

| Ano | R$ Cotado | R$ Ganhou | WR ajustado | %Orç | %Preta |
|---|---:|---:|---:|---:|---:|
| **2025** | R$ 1.593,6 MM | R$ 298,6 MM | **40,5%** | 53,7% | 8,8% |
| **2026 YTD (jan-mai)** | R$ 519,1 MM | R$ 107,0 MM | **40,3%** | 45,3% | **11,3%** ⚠ |

**Leituras críticas:**

1. **WR ajustado estável**: 40,5% (2025) → 40,3% (2026 YTD). Política de pricing mantém performance ano vs ano.

2. **%Orçamento Prévio caiu 8,4 pp** (53,7% → 45,3%). Possíveis causas:
   - Redução de prospecção em projetos engenheirados (ANDRITZ, VALLOUREC, JUMBO mantêm orçamento ativo mas em menor volume)
   - Curadoria de carteira: vendedores parando de aceitar "qualquer pedido de orçamento" sem qualificação
   - Mercado em retração reduz demanda especulativa
   - Sinal **positivo** se for curadoria; **neutro** se for retração geral

3. **%Preta subiu 2,5 pp** (8,8% → 11,3%) ⚠ **SINAL DE ALERTA**: maior fatia das cotações fechando abaixo do piso operacional. Combinado com queda do %Orç, sugere que vendedores estão concedendo mais piso em disputas reais (não em orçamentos). Pode ser ponta visível de:
   - Pressão competitiva crescente (concorrentes precificando mais agressivo)
   - Mix de clientes mais sensível a preço
   - Disciplina de bloqueios precisa reforço

Para próxima sessão técnica/estratégica: validar via análise temporal mensal — %Preta foi piorando ao longo do 1S/26?

### Comparativo YoY 1S25 vs 1S26 (período completo com jan-fev/26)

| Mês | 2025 Cotou | 2025 Ganhou | 2026 Cotou | 2026 Ganhou | Δ Cot | Δ Ganh | WR 2025 | WR 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Jan | R$ 124,9 MM | R$ 29,5 MM | R$ 88,8 MM | R$ 20,6 MM | **-29%** | -30% | 35,2% | **46,6%** |
| Fev | R$ 146,2 MM | R$ 31,2 MM | R$ 103,1 MM | R$ 23,0 MM | **-30%** | -26% | 44,5% | 45,1% |
| Mar | R$ 148,9 MM | R$ 21,8 MM | R$ 114,7 MM | R$ 22,2 MM | **-23%** | +1,8% | 34,3% | 38,9% |
| Abr | R$ 138,3 MM | R$ 21,5 MM | R$ 104,0 MM | R$ 20,8 MM | **-25%** | -3,1% | 26,2% | 30,6% |
| Mai | R$ 137,2 MM | R$ 25,3 MM | R$ 90,1 MM | R$ 20,4 MM | **-34%** | -19,3% | 41,8% | 45,1% |
| **1S** | **R$ 784,9 MM** | **R$ 151,0 MM** | **R$ 519,1 MM** | **R$ 107,0 MM** | **-33,9%** | **-29,1%** | **36,9%** | **40,3%** |

**Leituras estratégicas:**

1. **Mercado encolheu ~30% em volume cotado YoY**. Não é fenômeno isolado da AFS — provavelmente reflete contração da indústria de aços especiais. Validar com benchmark setorial (INDA, ABREMA) antes de concluir.

2. **WR ajustado SUBIU 3,4 pp** (36,9% → 40,3%) mesmo com volume caindo. Significa que Sacchelli mantém **share na disputa real**: do que ainda se cota, fecha mais. Resultado coerente com queda do %Orç (curadoria melhor) e queda do volume absoluto.

3. **Janeiro/26 é o destaque positivo**: WR 46,6% vs 35,2% em jan/25 (+11,4 pp!). Performance excepcional num mês historicamente fraco em conversão. Vale entender o que funcionou (mix de carteira? campanha? operação?).

4. **Abril 2026 WR 30,6%** continua o pior do semestre — mas era pior em 2025 (26,2%). Padrão sazonal de pior mês de pricing — investigar por quê (Tirad encia? Concorrência específica?).

5. **Mai/26 caiu 19% em R$ ganho** vs mai/25. Combina com -34% em volume cotado. Sinal de aceleração da queda no fim de Q2 — observar jun-jul com atenção.

### Performance por gerência (YTD 2025+2026, fonte v2.4 fixed)

Atualizado em [[#KPIs por ano]] — repetir tabela aqui seria duplicação. Pontos:
- **Felipe/Fuscão** continua dominando (72% do que se cota em rua). Carteira de tabelistas (Reynaldo, Carlinhos, Estratégicos, Denilson) responde por 50%+ dos R$ 856 MM de orçamento prévio em 2025.
- **Fabiola (CAXIAS)** com WR ajustado 29,1% (pior gerência operacional) + cota pessoalmente 334 itens em Preta em 3 meses. Material reforçado pra PIP de 31/07.
- **Odair-SCA** continua a unidade mais "saudável" (%Orç baixo, WR competitivo).

Análise detalhada na seção 4 da resposta de hoje (no chat — não migrei aqui pra evitar duplicar).

### Concorrência consolidada

Top concorrentes nomeados em "Perdeu Preço" (2025+2026):
- **Sem nomeado**: 39,6% do R$ perdido — gap de market intelligence persiste
- **Trefita/Torres**: #1 nomeado em volume de itens (1.570 + ?)
- **Usinas**: #1 nomeado em R$ por item (R$ 60k médio — disputa de projetos)

## Recomendações operacionais (re-priorizadas pós-2025)

| # | Ação | Owner | Status |
|---|---|---|---|
| 1 | Refactor política anual em Cotações | Claude | ✅ feito 01/06 |
| 2 | Exportar `CotacoesEncerradas_2025.xlsx` | Gustavo | ✅ feito 02/06 |
| 3 | Exportar `CotacoesEncerradas_2026.xlsx` completo (jan-fev incluídos) | Gustavo | ✅ feito 02/06 |
| 4 | **Fix gap_cot_ped_pct (mismatch unid_pu)** | Claude | ⏳ pendente — decisão |
| 5 | Reunião pricing Wagner/Felipe sobre Fabiola/CAXIAS | Gustavo | ⏳ pendente |
| 6 | UX Softcomp: motivo=Preço obriga Concorrente; Status=Encerrado obriga Motivo | Gustavo | ⏳ pendente |
| 7 | Validar com Softcomp/Felipe se relatório de Cotações Encerradas tem janela aberta ou rolante (evitar repetir problema no fim de 2026) | Gustavo | ⏳ pendente |
| 8 | **Fase 1 do Painel Executivo Consolidado** (6 blocos, schema v1) | Claude | ⏳ próxima sessão |

## Lições reforçadas

1. **Política "acumulativo" é frágil sem validação automática.** Política RAF (1 arquivo por ano-calendário, anos fechados imutáveis) é arquiteturalmente superior — controle local, sem dependência do ERP. Aplicada agora também a Cotações Encerradas; vale revisar se outros brutos marcados como "acumulativo" (PedidosEmitidos já é anual ✓) têm a mesma fragilidade.

2. **Caveat parqueado vira incidente.** Bug `valor_orc_previo` documentado no caveat há 17 dias custou 17 dias de Win Rate errado em reuniões. Bug `gap_cot_ped_pct` documentado em CLAUDE.md como "PU misturado" caveat há mais tempo — só agora, ao olhar com olhos de consultor big4, virou diagnóstico operacional.

3. **Cobertura cross-check é proxy de saúde do dado.** 15% → 87% revelado por simples mudança de política. Se KPI agregado de cobertura tivesse painel próprio com threshold mínimo (~85%), problema teria sido detectado em 09/05/2026 quando exporte rolou.

4. **Magnitude impossível é sinal mais óbvio que se ignora.** Gap +R$ 9,7 bilhões num faturamento de R$ 373 MM ficou na saída do crosscheck sem ninguém olhar. Big4 cria controles de razoabilidade no pipeline (sanity checks que abortam ou alertam quando totais cruzam threshold). Vale adicionar ao motor.

## Princípio que está se consolidando

> Cada bug descoberto na fonte é precondição para o próximo upgrade arquitetural. Bug `valor_orc_previo` precedia o Painel Executivo (sem ele, executivo herdaria 22% errado). Bug `gap_cot_ped_pct` precede o funil consolidado (sem ele, pricing leakage end-to-end seria fake). Resolver na fonte é caminho crítico — não atalho.

## Diagnóstico %Preta — onde o piso está sendo perdido

### Achado-chave: o salto não foi 2026 — foi 2H/25

| Semestre | R$ Cotado | R$ Preta | %Preta |
|---|---:|---:|---:|
| 2025 1S | R$ 784,9 MM | R$ 55,0 MM | **7,0%** |
| **2025 2S** | **R$ 808,7 MM** | **R$ 84,4 MM** | **10,4%** ⚠ |
| 2026 1S YTD | R$ 519,1 MM | R$ 58,7 MM | 11,3% |

A piora começou em **julho/2025**. Pico foi setembro/25 (16% no mês). 1S/26 é continuação de tendência iniciada em jul/25, não fenômeno novo. **Investigar o que aconteceu em jul/25** — pressão competitiva específica, mudança de tabela interna, ou perda de cliente estratégico que distorceu mix?

### Concentração por gerência (1S/26 vs 2025)

| Gerência | %Preta 2025 | %Preta 2026 | Δ pp | Severidade |
|---|---:|---:|---:|---|
| **Fabiola** | 23,0% | **37,0%** | **+14,1** | 🔴 grave |
| **Fernando** | 20,3% | **32,4%** | **+12,1** | 🔴 grave |
| **Odair - SCA** | 10,5% | 14,7% | +4,3 | 🟡 alerta |
| Felipe/Fuscão | 7,1% | 8,8% | +1,7 | OK |
| Odair - PIR | 11,3% | 9,8% | -1,5 | melhorou |
| Marketing | 0,8% | 0,4% | -0,4 | OK |

**70% da deterioração consolidada vem de 2 gerências** (Fabiola + Fernando). Não é fenômeno generalizado da força de vendas.

### Fabiola — perfil temporal alarmante (a gerente cota pessoalmente)

| Mês | %Preta dela |
|---|---:|
| 2025 jan-mai | 5-12% |
| 2025 jun-jul | 16% → **36%** |
| 2025 ago-set | **51% → 56%** |
| 2025 out-dez | 37% → 49% → 63% |
| **2026 jan** | **86%** ⚠⚠ |
| 2026 fev | 25% |
| 2026 mai | 65% |

**11 meses de deterioração consistente.** A gerente da unidade pior em pricing cota PESSOALMENTE com 60-80% em Preta. PIP que estava marcado pra 31/07/2026 — material reforçado para conversa **imediata** com Wagner+Felipe.

### Carlinhos — caso isolado (fev/26)

Vendedor disciplinado em 2025 (média 3-5%, mínimo 0% em mar/25). **Fevereiro/26 foi outlier**: 43,7% em Preta com R$ 2,47 MM. Voltou pra 3-17% em mar-mai/26.

Causa provável: cliente **HKM** concentrou R$ 1,99 MM de cotações dele em Preta (Carlinhos = vendedor). Investigar se foi negociação tática consciente ou furo isolado. Não é caso de PIP — é caso de conversa pontual.

### Concentração por cliente — candidatos a bloqueio

Clientes com >50% das cotações em Preta YTD 2026:

| Cliente | Vendedor | R$ Preta | %Preta |
|---|---|---:|---:|
| **TER BRASIL** | Aline | R$ 2,10 MM | **98%** | ✅ já bloqueada |
| **PANORAMA** | Açotec-SCA | R$ 0,85 MM | **100%** | candidato |
| **ELLO** | Fabiana-SCA | R$ 0,90 MM | **99%** | candidato |
| **TRATORGEL 2** | Açotec-SJRP | R$ 0,92 MM | 82% | candidato |
| **ARCO** | Estratégicos | R$ 0,92 MM | 65% | avaliar |
| **SEW-INDAIATUBA** | Estratégicos | R$ 2,57 MM | 62% | avaliar |
| **FIMAC** | Fabiola | R$ 1,20 MM | 60% | candidato |
| J & C | Thais | R$ 0,87 MM | 50% | avaliar |

**Padrão claro:** clientes que economicamente só fecham fora do piso → adicionar ao `MotorAnalitico/config/bloqueios_pricing.yaml` (linha por cliente). Estimativa de impacto se bloqueasse os 4 candidatos diretos: ~R$ 4,9 MM de proteção de margem.

### Liga 20MnCr5 — problema sistêmico de tabela, não comportamental

- **40,5% das cotações em Preta** (vs 6-15% das outras ligas)
- **Aline (94,1%) + Fabiola pessoalmente (83,2%) + Açotec-SJRP (92,6%)** dominam o problema
- Volume relativamente pequeno (R$ 12,1 MM cotado) mas categoria SISTEMICAMENTE subprecificada

Hipótese: piso F1/F2/F3 de 20MnCr5 no Softcomp está acima do que o mercado paga atualmente (tabela desatualizada). Auditar `criterios_raf.xlsx` e tabela de preços do Softcomp pra 20MnCr5 — pode resolver categoria inteira sem PIP de vendedor.

## Decisões táticas urgentes que saem deste diagnóstico

1. **Fabiola → PIP antecipado** (não esperar 31/07). Material quantitativo amplamente suficiente. Reunião Wagner+Felipe **esta semana**.
2. **Adicionar 4 clientes ao `bloqueios_pricing.yaml`**: PANORAMA, ELLO, TRATORGEL 2, FIMAC. Editar 1 YAML + rodar `--painel-raf` + `--painel-cotacoes`. Esperado: -R$ 5 MM de Preta a futuro.
3. **Auditoria tabela 20MnCr5**: piso pode estar desatualizado, resolvendo categoria inteira.
4. **Investigar HKM × Carlinhos × fev/26**: caso isolado mas R$ 2,47 MM justifica conversa.
5. **Retrospectiva 2H/2025**: o que aconteceu em jul/25 que iniciou a tendência? Vale análise dedicada antes de assumir que mudou a média histórica.

## Próxima sessão técnica

1. Aplicar fix `gap_cot_ped_pct` em `cross_check_cotacao.py`, bumpar schema Pedidos v4, re-rodar painel.
2. Iniciar Fase 1 do **Painel Executivo Consolidado** sobre fonte agora **tripla-limpa** (orc_previo + cobertura histórica + gap normalizado).
3. Considerar adicionar **sanity checks** no motor: gap R$ ponderado > 10% do faturamento total = ABORT.

## Fase 1 do Painel Executivo — entregue hoje (02/06/2026 tarde/noite)

### Decisões de arquitetura tomadas

1. **Win Rate Real (pedido emitido) vs Declarativo (cot Ganhou) lado a lado**, com gap em destaque. Insight: vendedores declaram cotações "Ganhou" mas nem todas viram pedido — gap mede leakage de marcação no Softcomp.
2. **Engenheirados via `familia_canonica_desc`** quando disponível, fallback `familia_descricao`.
3. **Filtros globais limitados a 3**: Ano · Unidade · Gerência (drilldown granular vai pros painéis profundos).
4. **Tela operacional de Pendentes × Estoque** (bloco 7) — não estava no escopo inicial; surgiu como demanda direta de Gustavo. Cruza pendentes do CD com cubo_estoque do RAF + curva ABC dos clientes + bloqueios YAML.

### Schema executivo v1-2026-06-02

```js
window.ED = {
  schema_version, generated_at, ano_alvo, meta,
  filtros_disponiveis: {anos, unidades, gerencias},
  kpis_global: {faturamento, win_rate_real, win_rate_decl, gap_declarativo, aov, pct_preta, pipeline, mc_total_pct},
  pendentes_estoque: [...lista enriquecida com status_sugerido...],
  // stubs próxima iteração:
  funil, saude_semanal, alertas, cross_funil, performance_dim
}
```

Tamanho: **0,67 MB** (alvo era 1-2 MB). Carrega instantâneo.

### Comando

```bash
python3 MotorAnalitico/main.py --painel-executivo
```

Depende dos 3 painéis individuais terem sido gerados. Aggregator de 2º nível — não toca enriquecidos, apenas lê os 3 *_data.js já produzidos. Tempo total: ~1 segundo.

### Arquivos novos

- `MotorAnalitico/executivo/__init__.py`
- `MotorAnalitico/executivo/README.md` (PRD compacto)
- `MotorAnalitico/executivo/aggregator.py` (~600 LOC — toda a lógica de KPIs + pendentes×estoque)
- `03_Ferramentas/Painel_Executivo.html` (template versionável, ~700 LOC — header sticky + 7 seções)
- `03_Ferramentas/executivo_data.js` (gerado, gitignored)

### Bloco 1 — KPI Bar Sticky (7 cards renderizados)

KPIs YTD 2026 lidos do aggregator:

| KPI | Valor |
|---|---:|
| Faturamento YTD | R$ 65,9 MM (YoY -44,4%) |
| **Win Rate Real** | **37,75%** (R$ 100,3 MM pedidos / R$ 265,7 MM cot encerradas) |
| **Win Rate Declarativo** | **40,28%** (R$ 107 MM cot Ganhou / R$ 265,7 MM) |
| **Gap declarativo** | **+2,5 pp** — vendedores marcam Ganhou ~2,5 pp acima do que vira pedido |
| AOV | R$ 3.741 (YoY +0,6%) |
| %Preta no faturado (RAF) | **15,41%** ⚠ |
| Pipeline aberto | R$ 18,4 MM (cobertura 1,1 meses) |
| MC Total / Receita | 31,1% |

**Achado bônus do KPI bar:** %Preta no FATURADO (15,41%) > %Preta nas COTAÇÕES (11,3%). Significa que disciplina deteriora entre cotar e faturar — cotou Vermelha, fechou em Preta com desconto no fechamento. Outro vetor de leakage além do declarativo.

### Bloco 7 — Pendentes × Estoque (operacional)

1.521 cotações pendentes enriquecidas com:
- `estoque_kg` da família (cubo_estoque RAF)
- `cobertura_meses` (consumo médio dos últimos 12 meses)
- `cliente_abc` (curva ABC sobre receita RAF)
- `status_sugerido` por fórmula multifator

**Distribuição inicial:**
- 🟢 **PRIORIZAR: 261** (estoque parado >24m, ou Preta com estoque, ou ABC-A aguardando >15d)
- 🔵 ESPERAR: 1.255
- 🔴 NEGAR: 5 (bloqueios ativos + Preta sem estoque)

**Match família com estoque:** `_familia_prefix()` extrai "8640 R L" de "8640 R L de 101,61 até 203,20" pra match com cubo_estoque RAF (formato curto). 1.366 pendentes (89,8%) acharam match.

### Achados de negócio que saltam do bloco 7

| Cliente | Vendedor | Cotação R$ | Estoque | Cobertura | Insight |
|---|---|---:|---:|---:|---|
| **LINDNER TECHNO** | Jaqueline | R$ 57k | 710 t | **292 meses (24 anos!)** | Liquidação urgentíssima |
| **INPEL** | Fabiola | R$ 95k | 2.000 t | 106 meses | Queimar estoque |
| **CASA DO AÇO** | Prospecção-CXJ | R$ 81k+70k | 154 t | 27 meses | 2 cotações abertas |
| **IMEPEL** | Thais | R$ 63k | 632 t | 16 meses | Priorizar |

### Filtros locais bloco 7

- Cliente / Vendedor / Família (texto contém)
- Status (Priorizar/Esperar/Negar)
- Faixa (V/A/V/P)
- Estoque (com / sem / excedente >24m)
- **Botão "Exportar CSV"** — exporta lista filtrada com BOM UTF-8 pra Excel não quebrar acento

### Stubs (próxima iteração — blocos 2-6)

| Bloco | Conteúdo | Estimativa |
|---|---|---|
| 2 — Funil Consolidado | Sankey 4 estágios com NF Faturada tracejada (cross-check RAF↔Pedidos parqueado) | 2-3h |
| 3 — Saúde Semanal | 3 séries (Fat/Pedidos/Cotações) + bullet vs run-rate + sparkline 12 sem | 2h |
| 4 — Top 10 Alertas (paginação até 50) | Bloqueios, pendentes >30d, vendedores PIP, churn ABC-A, ligas %Preta sistêmica | 3-4h |
| 5 — Cross-funil (4 sub-blocos) | Leakage waterfall, Heatmap migração faixa, Ajustes vendedor, Cotação × Estoque | 3-4h |
| 6 — Performance por Dimensão | Drilldown Unid → Ger → Vend → Família, sempre com % | 2h |

Total restante estimado: **12-15h** (1-2 sessões dedicadas).

### Lições da Fase 1

1. **Schemas dos 3 painéis não estavam alinhados** — PD usa `cubo` (não `cubo_main`), colunas lowercase (`mc_aco` vs `MC_Aco`). Aggregator do executivo precisou de helpers tolerantes. Vale pensar em padronizar quando refatorar (não bloqueia).

2. **Famílias têm formatos diferentes entre fontes** — pendentes têm "8640 R L de 101,61 até 203,20" (com faixa), estoque tem "8640 R L" (sem). Função `_familia_prefix()` ponte. Padrão big4: ter um lookup canônico de família publicado num lugar único (próxima iteração).

3. **NaN propaga silenciosamente em JSON** — pandas DataFrames com NaN viram "NaN" literal em JSON sem `default=str`, quebrando parsing. Helper `_none_se_nan()` adicionado pra sanitização.

4. **0,67 MB de cubo executivo** vs ~95 MB do PD — aggregator de 2º nível é o caminho certo. KPIs cross-funil cabem em memória JS sem problema, abre em <1s no browser.

5. **Achados surgem da própria construção** — bloco 7 mostrou %Preta deteriorando entre cotação→fatura (15,4% > 11,3%), insight que não estava na pauta. Cruzamentos viram análise.
