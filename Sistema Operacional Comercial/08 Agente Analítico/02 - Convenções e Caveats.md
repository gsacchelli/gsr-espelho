---
tags: [agente, sacchelli, caveats, qualidade-dados]
status: vivo — adicionar caveats à medida que aparecerem
ultima_atualizacao: 2026-06-02
---

# 02 — Convenções e Caveats

Pegadinhas dos dados que afetam o agente. Documentar aqui evita re-descobrir.

## 1. Engenheirados vs Catalogados

Cotações de produto engenheirado (ex: "Eixo usinado conforme desenho 1234 Rev.1") aparecem nos enriquecidos com `liga`, `perfil`, `acabamento`, `medida_1` em **branco/NaN**. A info está só na descrição livre do `material`.

O cubo de cotações tem `tipo_item` ∈ {`catalogado`, `engenheirado`} pra distinguir.

**Impacto:**
- Filtros `aco='4140'` nos enriquecidos casam só com catalogados — engenheirados ficam invisíveis.
- Engenheirados costumam ter **alto valor unitário** (R$ 90k-450k) — não é resíduo, é peça crítica.
- Coluna `kg` em engenheirados frequentemente é **número de peças** (1, 3...), não peso real. Logo **não dá pra calcular R$/kg**.

**Como tratar:**
- Em análise de pricing por R$/kg: filtrar engenheirados out e reportar quantos ficaram de fora.
- Em análise de valor (vendas, win rate, motivos): incluir engenheirados — eles entram.
- Pra encontrar engenheirados de uma liga: buscar em `material.str.contains('4140')` (não em `liga`).

**Medido em 2026-05-14:** no recorte "4140 entre 102-230mm encerradas", 39 cotações engenheiradas (R$ 2,78MM, ~19% do recorte) ficavam invisíveis com filtro `liga='4140'` puro.

## 2. PU no enriquecido mistura R$/peça e R$/kg

Coluna `pu` em `CotacoesEncerradas_enriquecido.xlsx` é `valor_total / qtd`. Quando `qtd` é em kg, vira R$/kg. Quando `qtd=1` (peça única), vira R$/peça. Resultado: distribuição absurda com outliers de R$ 25.000/"kg".

**Regra canônica:** sempre calcular `pu_kg = valor_total / kg` no agente. Nunca confiar na coluna `pu` direto.

Filtro de sanidade pra liga base: R$/kg ∈ [1, 100]. Fora disso, é serviço/processo embutido ou erro de unidade.

**Bug correlato — RESOLVIDO 02/06/2026 (Pedidos schema v4-2026-06-02):** o cross-check pedido↔cotação em `MotorAnalitico/pedidos/cross_check_cotacao.py` calculava `gap = (pu_ped - pu_cot) / pu_cot` sem normalizar unidades — pedidos com `unid_pu='PÇ'` (27%) eram comparados R$/peça vs R$/kg. Fix: ambos os lados normalizados pra R$/kg via `valor_total/kg`, com guards:
- Cotação: só calcula `pu_kg_cotacao` se `tipo_item='catalogado'` (engenheirados têm `kg=nº peças`)
- Pedido: só calcula `ped_pu_kg` se `unid_pu='KG'` (PÇ fica None — sem comparação artificial)

Resultado: gap médio **+0,27%** (era +55,6%), gap R$ ponderado **R$ +585 mil** (era +R$ 9,7 bi). ~66k pedidos com gap confiável; 33k ficam sem comparação (honesto — magnitudes incompatíveis). Schema v4 expõe `cot_pu_kg` e `ped_pu_kg` como colunas explícitas no enriquecido pra debug.

Nova regra canônica: **nunca comparar PU entre pedido e cotação sem antes verificar ambos os lados em R$/kg via `valor_total/kg`**. Se um dos lados é PÇ ou engenheirado, comparação inválida — retornar None.

## 3. ~~Bug do `valor_orc_previo`~~ — RESOLVIDO (01/06/2026, schema v2.4)

**Status:** corrigido na fonte. A métrica `valor_orc_previo` agora é populada corretamente nos 7 cubos OLAP de Cotações a partir do schema **v2.4-2026-06-01**. Fix: callsite do `_acumular` passava `bucket` mas a comparação interna era contra a string antiga `'Orç. prévio'` — agora compara contra `'Orçamento'` (string canônica do `bucket_status`).

Log completo: `GSR/Logs/2026-06-01 — Fix valor_orc_previo (Win Rate dobra de 22%→40%).md`.

**Win Rate de leitura direta do cubo_main** (sem workaround):
- Bruto YTD 2026: **21,7%** (denom = ganhou + perdeu_bruto, inclui orçamento)
- Líquido YTD 2026: **40,2%** (denom = ganhou + perdeu_real, exclui orçamento)

Workaround documentado abaixo continua válido como defesa em profundidade e pra contagem direta no enriquecido.

**Pra extrair Orçamento Prévio em qualquer cubo:** somar `valor_orc_previo` direto (a partir de v2.4) **OU** filtrar `bucket_status == 'Orçamento'` e somar `valor_total` (compatível com v2.3 também).

**Caso emblemático:** Denilson aparecia como 5,7% de conversão (pior depois de Priscila/Evandro). Real é **37,1%**. 67% do volume dele é orçamento prévio (R$ 37MM de R$ 44MM cotados em 2026) — perfil de clientes engenharia (ANDRITZ, JUMBO, MUNIZ, VALLOUREC) que pedem cotação só pra estimar custo. Bug expunha vendedor injustamente em ranking.

## 4. Bitolas em polegada convertidas

O catálogo AFS usa bitolas convertidas de polegadas (304,8mm = 12"). Quando o usuário pergunta "1045 R F 304,20mm", o catálogo tem **304,80mm**.

**Como tratar:** funções de estoque (`cobertura`, `excedente`) usam `bitola_tolerancia=1.0` por default. Margem suficiente pra capturar diferenças de digitação sem capturar bitola adjacente errada.

## 5. Cliente como holding/grupo econômico

"WEG" no cadastro são 6 razões sociais distintas: WEG - SC, WEG CESTARI, WEG HISA, WEG LINHARES, WEG MAQ. SBC, WEG TGM. Análise por cliente exato perde a visão do grupo.

**Como tratar:** `vendas.vendas_cliente('WEG')` usa match `contains` case-insensitive, retorna total consolidado + breakdown por razão.

Idem pra: ANDRITZ (ANDRITZ + ANDRITZ SCHULER), TER BRASIL (variantes), THERMON, etc.

## 6. Bucket aging "60+" sem o "d"

Em `cubo_pendentes` (window.CD), os buckets de aging são `'0-7d'`, `'8-15d'`, `'16-30d'`, `'31-60d'` e **`'60+'`** (note: sem o `d` final). Filtros que mapeiam buckets por dia mínimo precisam considerar essa exceção.

## 7. Win rate "bruto" vs "líquido" — duas leituras válidas

| Tipo | Inclui Orçamento Prévio? | Numerador | Denominador |
|---|---|---|---|
| **Bruto** | Sim | `valor_ganhou` | `valor_ganhou + valor_perdeu_bruto` |
| **Líquido** | Não | `valor_ganhou` | `valor_ganhou + (valor_perdeu_bruto − valor_orc_previo)` |

CLAUDE.md cita win rate bruto (24% em 2026 YTD). Painéis HTML usam o mesmo. Pra **decisão comercial real** (onde dá pra atuar), líquido (40%) é mais útil.

## 8. RAF é substitutivo por ano

`RAF_2026.xlsx` contém só 2026. Pra histórico, ler RAF de cada ano separado ou usar os enriquecidos `RAF_enriquecido_YYYY.xlsx` (em `02_Derivados/RAF/`).

O `window.PD` já agrega os 4 anos disponíveis (2023-2026) — função de vendas pode pedir período histórico sem se preocupar com o split por ano.
