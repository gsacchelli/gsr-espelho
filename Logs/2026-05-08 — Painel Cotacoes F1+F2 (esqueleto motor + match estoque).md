---
data: 2026-05-08
contexto: Painel Comercial de Cotações
status: F1+F2 fechadas, F3+F4 pendentes
tags: [painel, cotações, motor-analítico, sessão]
---

# 2026-05-08 — Painel Cotações F1+F2 (esqueleto motor + match estoque)

## TL;DR

Construído o motor de enriquecimento de Cotações (Encerradas + Pendentes) seguindo padrão idêntico ao motor RAF. F1 (esqueleto) + F2 (match estoque) entregues e validadas com 55/55 testes verde. Falta F3 (aggregator + cubos OLAP) e F4 (HTML 5 abas).

## O que foi entregue

### F1 — Esqueleto motor

`MotorAnalitico/cotacoes/`:
- `lookup_familia.py` (316 LOC) — carrega `01_Brutos/FamiliasProdutos/FamiliasProdutos.xlsx` em estruturas tipadas. 98 famílias indexadas O(1) pelo código (ex: '0016' → "Laminado Importado, Redondo, Laminado, range 1045 até 1050M, range bitola 101.61 até 230.00, F1=9399.87 / F2=9033.64 / F3=8694.88")
- `enriquecer.py` (487 LOC) — 7 funções puras: `derivar_chave`, `derivar_datas`, `derivar_familia`, `derivar_tipo_item`, `derivar_gap_e_faixa`, `derivar_motivo_e_concorrente`, `derivar_pedido_id`, `enriquecer_linha` (orquestrador)
- `pipeline.py` (~330 LOC) — I/O streaming via xlsxwriter (3-5x mais rápido que openpyxl para 60k+ linhas). Throughput observado: 1.585 linhas/s
- `test_enriquecer.py` (~600 LOC) — 55 testes verde

Wirado em `main.py` via `--cotacoes-enriquecer`.

### F2 — Match × Estoque + Pedido ID

`MotorAnalitico/cotacoes/match_estoque.py` (377 LOC):
- Carrega `EstoquePadrao.xlsx` (524 SKUs, 18 MM kg)
- Indexa por `(aço, perfil, acab, bitola)` — chave canônica usando `_norm_aco`/`_norm_perfil`/`_norm_acab`
- 5 status de match: `exato` / `tolerancia` (±5%) / `familia` (mesmo aço/perfil/acab, bitola distante) / `sem_match` / `engenheirado` / `sem_estoque`

Adiciona 5 colunas no enriquecido: `estoque_match_status`, `estoque_qtd_kg`, `estoque_familia_kg`, `estoque_meses_giro`, `estoque_bitola_match_mm`.

Plus: `pedido_id` extraído do `Descrição motivo` (regex `ped:NNNNN.X` em "Ganhou > ped:334349.1") — chave para cross-check com RAF na F3.

## Decisões tomadas com Gustavo

| Decisão | Resposta |
|---|---|
| Faixas | F1=Verde, F2=Amarela, F3=Vermelha (piso). PU < F3 = Preta. |
| Família | Cruzar com `FamiliasProdutos.xlsx` (cadastro Softcomp) |
| Match estoque | Match exato + tolerância. Engenheirado = skip |
| Escopo MVP | 5 abas (Pipeline / Win Rate / Perdas / Item×Estoque×Vermelha / Tabelistas) |
| Reuso lookup RAF | Sim, em F3 (BitolaPadrao + AcoPadrao + CidadeRegiao) |
| Cross-check RAF | Sim, já em F2/F3 via `pedido_id` |
| F4 (HTML) | 5 abas todas de uma vez |
| Datas 2028/2029 | Bug de digitação confirmado pelo Gustavo (14 ocorrências, 0,02%) |
| Dedupe acumulativo | `(Unidade, Número, Item)` + manter mais recente por `data_encerramento` |

PRD completo em `Planejamento Estratégico - Comercial/06_Docs/PRD_Painel_Cotacoes.md`.

## Achados sobre dados reais (62.313 itens encerrados + 1.786 pendentes)

### Cotações Encerradas
- **Win rate por valor**: 12,1% (R$ 104 MM ganhos / R$ 861 MM cotados). Win rate ajustado (excluindo orç. prévio do denominador) sai melhor — vai aparecer no painel.
- **Faixa orçada**: Verde 13.456 (22%), Amarela 24.466 (39%), Vermelha 19.234 (31%), Preta 4.850 (8%)
- **4.850 cotações orçadas em Preta** — orçamentos abaixo da Vermelha. 1.898 dessas viraram pedido (Ganhou em Preta — visibilidade nova que o painel vai expor).
- **Engenheirados**: 338 itens (sucata, cavaco, descrições livres) — corretamente classificados.
- **Match estoque**: 96% (51.686 exato + 7.789 tolerância de 62.311).
- **Pedido ID** extraído: 23.048 / 23.048 (100% das Ganhou — cross-check RAF garantido).

### Cotações Pendentes
- 1.786 itens / 601 cotações / 421 clientes / R$ 31 MM em pipeline aberto
- Match estoque: 1.708 / 1.778 catalogados (96%)
- Pipeline em aberto suficiente para começar a aba "Foco da semana"

### Top concorrentes nomeados (regex parser do `Descrição motivo`)
1. Trefita/Torres — 2.551 (consistente com vault: principal concorrente)
2. Açovisa — 1.060
3. GGD — 710
4. Açofera — 438
5. Diferro — 403
6. Açotubo — 333

(Existe ruído tipo "requer comprovação" — 204 entradas — que é status, não concorrente; filtrar no aggregator F3.)

### Datas anômalas
14 linhas com data de emissão > today + 60d. Cotação `MATRIZ_252673` tem várias linhas com data 2028-08-29 — bug de digitação. Painel terá aba diagnóstico para Gustavo revisar caso a caso.

## Caso Binotto (Fabiola/RS) — exemplo concreto

Cotação `MATRIZ_537267` (cliente BINOTTO IND DE COMPONENTES HIDRAULICOS, FLORES DA CUNHA-RS, vendedor Fabiola):
- 6 itens, todos orçados PU=7,50 vs Vermelha=8,07 (gap −7,06%)
- Status final: **GANHOU** (todos os 6 itens viraram pedido na Tabela Preta)
- Família: 0016 (Laminado Importado 1045/1050M, range bitola 101–230mm)

Padrão a investigar: cliente-âncora que sistematicamente negocia tudo abaixo do piso, ou processo comercial precisa ser reapertado? O painel novo expõe esse padrão por cliente × vendedor.

## Pontos de retomada para a próxima sessão

### Como retomar
1. Ler este log + `Planejamento Estratégico - Comercial/06_Docs/PRD_Painel_Cotacoes.md`
2. Confirmar arquivos enriquecidos existem em `02_Derivados/Cotacoes/`
3. Rodar `python3 MotorAnalitico/main.py --cotacoes-enriquecer` se brutos foram atualizados

### F3 — Aggregator (próximo passo, ~1 dia)
Criar `MotorAnalitico/cotacoes/aggregator.py` espelhando `raf/painel_aggregator.py`. Precisa:
- 6 cubos OLAP: `cubo_main`, `cubo_cliente`, `cubo_pendentes`, `cubo_motivos`, `cubo_pricing_item`, `cubo_geo`
- Lista `itens_criticos_top` (≤ 5.000 itens em Preta + Ganhou-em-Preta + projetos suspeitos)
- Cross-check com RAF: indexar `pedido_id` → linha do RAF enriquecido, computar delta orçado vs efetivo
- Auto-flag tabelista (>70% orç.prévio + <10% conv) e projeto suspeito (>R$100k + idade >30d)
- Saída: `03_Ferramentas/cotacoes_data.js` (window.CD)
- Schema versionado: `SCHEMA_VERSION = 'v1-2026-05-08'`

### F4 — Painel HTML (~2-3 dias)
Criar `03_Ferramentas/Painel_Cotacoes.html` com 5 abas:
1. Pipeline (Pendentes + aging + foco da semana + suspeita projeto)
2. Win Rate (global + ajustado + ranking + evolução)
3. Análise de Perdas (concorrentes + gap ganhas vs perdidas + PIR/CXS diagnóstico)
4. **Item × Estoque × Vermelha** ⭐ (filtros + tabela mestre + stoplight + Ganhou em Preta)
5. Tabelistas & Projetos (auto-flag dos 2 perfis do vault)

Padrões obrigatórios: glossário ❓ (igual RAF), wrapper `_safeRender` por bloco, schema check no boot, vocabulário consistente (Verde/Amarela/Vermelha/Preta, Pipeline aberto, Win Rate ajustado, Item engenheirado).

### F3 extra — Cross-check RAF (decisão validada)
Cada linha de cotação com `pedido_id` recebe colunas:
- `raf_pu_efetivo` (PU realmente faturado)
- `raf_faixa_efetiva` (faixa em que fechou no faturamento)
- `delta_cotacao_pedido` (mudou de faixa entre cotação e pedido?)

Cuidado: precisa indexar 200k+ linhas do RAF (todos os anos) por (`OS`, `item`) ou por `pedido_id` se aparecer no RAF. Verificar como `pedido_id` da cotação se mapeia em `ABCNFENF` ou `ABCOSFNF` do RAF antes.

## Arquivos relevantes

### Brutos
- `01_Brutos/CotacoesEncerradas/CotacoesEncerradas.xlsx` (12,6 MB, 62.313 itens)
- `01_Brutos/CotacoesPendentes/CotacoesPendentes.xlsx` (357 KB, 1.786 itens)
- `01_Brutos/FamiliasProdutos/FamiliasProdutos.xlsx` (22 KB, 98 famílias) — aguardando atualização do Gustavo

### Derivados
- `02_Derivados/Cotacoes/CotacoesEncerradas_enriquecido.xlsx` (~10 MB, 67 colunas × 62.311 linhas)
- `02_Derivados/Cotacoes/CotacoesPendentes_enriquecido.xlsx` (~510 KB)

### Código
```
MotorAnalitico/cotacoes/
├── __init__.py
├── lookup_familia.py
├── enriquecer.py
├── match_estoque.py
├── pipeline.py
├── test_enriquecer.py    (55 testes)
└── README.md
```

### Documentação
- `06_Docs/PRD_Painel_Cotacoes.md` (PRD completo)

## Decisões de arquitetura preservadas

1. **xlsxwriter no lugar de openpyxl write_only** para os 62k linhas — economiza minutos. Padrão a copiar para qualquer pipeline grande no futuro.
2. **Família via Cód. left-padded para 4 chars** (`'16'` → `'0016'`) — Excel pode trazer como int, sempre normalizar.
3. **`tipo_item` precisa ser computado antes do match estoque** — engenheirado vai como skip.
4. **Status secundários nos Pendentes** (5 Ganhou + 5 Perdeu de 1.784) — overlap por momento do export. Aba 1 do painel filtra `Status = Pendente` e sinaliza os outros como ruído.
5. **Concorrente nomeado** vem em parênteses no `Descrição motivo`. "Sem informação" e "requer comprovação" não são concorrentes — filtrar.
6. **Pedido ID** vem em `desc_motivo` no formato `ped:NNNNN.X` — extrai com regex.
7. **Datas anômalas** sinalizadas via flag `data_anomalia` (>60d futuro). 14 linhas no dataset atual.

## Conexões

- [[Sistema Operacional Comercial/05 Cotações/00 - Visão Geral Cotações]]
- [[Sistema Operacional Comercial/05 Cotações/02 - Motivos de Encerramento]]
- [[Sistema Operacional Comercial/05 Cotações/03 - Orçamento Prévio vs Projeto Real]]
- [[Sistema Operacional Comercial/05 Cotações/04 - Cliente-Tabelista (flag proposta)]]
- [[Sistema Operacional Comercial/05 Cotações/05 - Win Rate e Métricas]]
- [[Sistema Operacional Comercial/07 Cruzamentos e Previsões/00 - Visão Geral Cruzamentos]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/03 - Ferramentas Analíticas - Inventário]] (atualizar status: Dashboard de Cotações Pendentes → Em desenvolvimento F2)
