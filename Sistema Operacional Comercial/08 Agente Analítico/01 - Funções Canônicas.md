---
tags: [agente, sacchelli, referencia]
status: 12 funções entregues
ultima_atualizacao: 2026-05-14
---

# 01 — Funções Canônicas

Inventário das funções do agente. Cada função tem propósito, assinatura, fonte, exemplo de uso e caveats.

Importação padrão:

```python
from MotorAnalitico.agente.analises import vendas, cotacoes, estoque, pedidos, pricing
```

## Vendas — `agente/analises/vendas.py`

### `top_materiais(periodo, n, metrica)`

Top N famílias canônicas por receita ou volume.

- **Fonte:** `cubo` (window.PD)
- **Args:** `periodo` ('mes_corrente' | 'ytd' | etc.), `n=10`, `metrica='valor'|'kg'`
- **Retorna:** DataFrame `[familia, valor_liq, qtd_kg, mc_total, mc_pct, n_linhas]`
- **Exemplo:** `vendas.top_materiais('mes_anterior', metrica='kg')` → família mais vendida em peso no mês anterior

### `vendas_cliente(termo, periodo, detalhar=True)`

Vendas para cliente(s) cujo nome contém `termo` (case-insensitive).

- **Fonte:** `cubo_cliente` (window.PD)
- **Args:** `termo` (substring, ex: 'WEG' pega 5 razões sociais), `periodo`, `detalhar`
- **Retorna:** dict com `total` (DataFrame 1 linha) + `por_cliente` (DataFrame agrupado)
- **Exemplo:** `vendas.vendas_cliente('WEG', 'ano_corrente')` → R$ 3,42MM em 5 razões WEG

## Cotações — `agente/analises/cotacoes.py`

### `listar(status, vendedor, cliente, valor_min, ...)` — drilldown genérico

Lista cotações linha-a-linha com filtros opcionais. Cobre família enorme de perguntas ("perdidas do Denilson", "pendentes >R$ 100k", "ganhou em Preta nos últimos 30d", etc).

- **Fonte:** `CotacoesPendentes_enriquecido.xlsx` se `status='Pendente'`, senão `CotacoesEncerradas_enriquecido.xlsx`
- **Args:** `status` (obrigatório), `vendedor`, `cliente`, `valor_min`, `valor_max`, `faixa`, `aco`, `aging_min`, `motivo`, `concorrente`, `periodo`, `n=50`, `ordenar='valor_total'`
- **Retorna:** DataFrame com colunas executivas
- **Caveats:**
    - Filtro `aco` casa em `liga` (catalogados) — engenheirados ficam de fora silenciosamente. Ver `02 - Convenções e Caveats.md`.

### `conversao(periodo, dim, valor_min, excluir_orc_previo, n)`

Win rate por valor — global ou por dimensão.

- **Fonte:** `cubo_main` (window.CD)
- **Args:** `dim=None|'vendedor'|'unidade'|'gerencia'|'aco'|'faixa_bitola'`, `excluir_orc_previo=True`
- **Retorna:** dict (global) ou DataFrame (por dim, ordenado por pct asc = piores primeiro)
- **⚠ Bug corrigido (2026-05-14):** `valor_orc_previo` do cubo está SEMPRE zerado — orçamento prévio fica embutido em `valor_perdeu`. A função deriva via `bucket_status='Orçamento'`. Win rate "correto" YTD = 40,2% (vs 24% bruto do CLAUDE.md que inclui orçamento).

### `perdas_por_preco(periodo, n)`

Top combinações Aço × Faixa de Bitola com mais valor perdido por preço.

- **Fonte:** `cubo_main` (window.CD), filtra `bucket_status='Perdeu Preço'`
- **Retorna:** DataFrame `[aco, faixa_bitola, n_cotacoes_perdidas, valor_perdido, kg_perdido, gap_f3_pct_medio]`

### `cotacoes_aging(dias_min, n)`

Cotações pendentes com aging >= dias_min, por cliente×vendedor.

- **Fonte:** `cubo_pendentes` (window.CD)
- **Caveat:** bucket aging final é `'60+'` (sem `d`) — diferente dos outros (`'31-60d'` etc).

### `aging_resumo()`

Distribuição do pipeline pendente por bucket — sanity check rápido.

## Estoque — `agente/analises/estoque.py`

### `cobertura(aco, perfil, acabamento, bitola, bitola_tolerancia, cobertura_max, n)`

SKUs em estoque com saldo + cobertura, filtros opcionais.

- **Fonte:** `cubo_estoque` (window.PD)
- **Caveats:**
    - `bitola_tolerancia=1.0` por default (em mm) — catálogo AFS usa bitolas convertidas de polegada (304,8mm = 12"), tolerância acomoda diferenças de digitação.
    - Filtra automaticamente SKUs com saldo > 0.

### `excedente(aco, perfil, acabamento, bitola, meses_saudaveis, n)`

Estoque acima da cobertura saudável.

- **Cálculo:** `excedente_kg = qtd_estoque_kg - (media_mensal_kg * meses_saudaveis)`. Default `meses_saudaveis = max(lead_time + 1, 3)`.
- **Útil pra:** identificar candidatos a liquidação. Ex: 1045 R F 304,80mm = 122 meses de cobertura excedente (R$ centenas de milhares parados).

### `materiais_parados(meses_min, n)`

SKUs com cobertura alta (proxy de capital parado). Mais simples que `excedente` — filtra direto pela cobertura.

## Pedidos — `agente/analises/pedidos.py`

### `pedidos_semana(dias, hoje)`

Pedidos dos últimos N dias por unidade.

- **Fonte:** `cubo_dia` (window.PED) — única fonte com granularidade diária
- **Métricas:** valor, kg, pu_medio, **pct_cold** (sem cotação prévia), **pct_preta**, ajustes pós-fechamento
- **Default dias=7.** Inclui linha 'TOTAL'.

### `ajustes_pos_fechamento(top_n)`

Cross-check cotação×pedido por vendedor — quem recupera vs cede margem entre cotar e fechar.

- **Fonte:** `cubo_ajustes` (window.PED)
- **Retorna:** vendedor + valor_recuperou + valor_cedeu + valor_mantido + **saldo_rs** + **pct_disciplina**.

## Pricing — `agente/analises/pricing.py`

### `pct_preta_vendedor(periodo, valor_minimo, n)`

Ranking de vendedores por % de receita em Tabela Preta.

- **Fonte:** `cubo` (window.PD), filtra `considerar=True` + `op_cat='Venda'`
- **Recomendado:** `valor_minimo=100_000` ou maior pra excluir ruído.

### `preco_para_win_rate(liga, bitola_min, bitola_max, target_pct, ...)`

Curva PU × Win Rate empírica — qual R$/kg pra fechar X% das cotações.

- **Fonte:** `CotacoesEncerradas_enriquecido.xlsx`
- **PU canônico:** `valor_total / kg` (NÃO usar a coluna `pu` direta — mistura R$/peça e R$/kg conforme `qtd` é unitário ou em kg)
- **Filtro de sanidade:** R$/kg ∈ [1, 100] (acima é serviço/processo embutido)
- **Método:** ordena por PU asc, calcula win rate cumulativo, acha PU onde curva cruza o target. Considera só pontos com N≥50 pra evitar ruído inicial.
- **Achado importante:** pra liga base + faixas amplas, win rate satura em ~57% — não é viável fechar 75% só com preço (precisa atacar perdas não-preço).
- **Caveat:** engenheirados ficam de fora (não têm kg real). Análise reporta separadamente quantos R$ ficaram invisíveis no recorte.
