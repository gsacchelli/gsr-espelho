---
data: 2026-08-01
tipo: log
status: vigente
domínio: sistema-de-dados
criado: 2026-08-01
tags: [softcomp, sql, custo, margem, cotacoes, pedidos, raf]
---

# 2026-08-01 — Custo na cotação e no pedido (entrega do Nelson)

## O que aconteceu

O Nelson (Softcomp) entregou em 31/07 as colunas que pedimos nas solicitações de
20/07 (views) e 23/07 (custos). Conferimos contra a réplica em 01/08 e o resultado
foi **maior do que o esperado** — e diferente do que parecia à primeira vista.

## A descoberta que mudou a conversa

Gustavo tinha a leitura de que "só faltava o histórico". Duas coisas apareceram:

1. **Coluna nova na view não chega sozinha no lake.** Os loaders (`pull_pedidos.py`,
   `pull_pendentes.py`, `pull_encerradas.py`) fazem `SELECT` com lista explícita —
   as colunas estavam na origem desde 31/07 e o pipeline as ignorava em silêncio.
   Existem **duas pendências distintas**: a do Nelson (coluna existir) e a nossa
   (consumir). Confundir as duas leva a cobrar o fornecedor por trabalho nosso.

2. **O que pedimos ≠ o nome que veio.** Pedimos `Situacao` e `OrdemCompra`;
   vieram `StatusPedido` e `PedidoCliente`. A primeira conferência acusou
   "não chegou" para campos que estavam lá. Por isso a conferência virou script
   com sinônimos: `MotorAnalitico/sql/conferir_colunas.py`.

## O que chegou (validado com dado real, 2026)

| View | Coluna | Cobertura | Destrava |
|---|---|---|---|
| `BI.Cotacao` | `CustoMP` / `CustoTotal` | 99,4% | **MC por item na cotação** — antes era proxy por custo de reposição da família, cobrindo ~49% do R$ |
| `BI.Cotacao` | `Origem` | 100% | origem fiscal por item (CST-A) → ajuste de ICMS mais preciso |
| `BI.Pedido` | `CustoMP` / `CustoTotal` | 99% | margem no pedido, sem esperar o RAF |
| `BI.Pedido` | `PrazoEntrega` | 100% | aposenta a semente manual do SP8001A na Carteira |
| `BI.Pedido` | `StatusPedido` | exceção | **cancelado ≠ faturado** |
| `BI.Pedido` | `PedidoCliente` | 53% | OC do cliente |
| `BI.Pedido` | `Procedencia` | 97% | procedência do material |

### O caso SUPERIOR, resolvido na origem

Consulta direta na réplica:

```
343024/1  StatusPedido='Encerrado'  saldo=0  R$ 15.900
343024/2  StatusPedido='Encerrado'  saldo=0  R$ 67.200
343047/1  StatusPedido=''           saldo=1  R$ 15.900   ← o reemitido
```

Os R$ 83.100 que inflaram 29/07 estão marcados. Em 2026 são **519 itens /
R$ 4,6 MM** entre `Abortado` e `Encerrado`, todos com saldo zero — exatamente o
padrão que entrava como faturamento. Substitui o `pedidos_cancelados.yaml` manual
e a heurística de redigitação por um campo do ERP.

## A distinção que organiza tudo — custo REFERÊNCIA × custo REAL

Enquadramento do Gustavo, e é a chave da modelagem:

> "os custos tanto em cotações quanto pedidos são as referências na elaboração das
> cotações, o RAF deve apurar o custo real"

- **Cotação** carrega o custo que o vendedor tinha ao precificar (carimbado na emissão)
- **Pedido** carrega a mesma referência, no momento do fechamento
- **RAF** apura o custo realizado, depois de faturar

Por isso a coluna derivada chama-se **`mc_cheia_pct`**, nunca "MC". Dois motivos,
os dois medidos:
- **base**: o `CustoTotal` do ERP já embute os impostos da venda (resíduo estável
  em ~8,5% do bruto em todas as cargas), então a razão é bruto÷bruto — enquanto a
  MC do portal é sobre valor líquido;
- **custo**: o do ERP é de REPOSIÇÃO, o do RAF é do LOTE histórico.
Um campo chamado "MC de referência" seria comparado com os 31,8% do portal, daria
15% e seria lido como erro. São três réguas que não se comparam sem conversão.

## Implementado hoje

- Loaders consomem as 10 colunas; `Status` do pedido passa a vir do ERP
- `derivar_mc_cheia()` nos enrichers de cotações e pedidos (mesma fórmula nos
  dois, de propósito — é o que permite comparar os elos da cadeia)
- Guarda de custo zero: `_custo()` nos loaders (0 → None) + `NULLIF` nas views —
  custo zero produziria margem 100% e jogaria o item ao topo do Foco do dia
- Gold expõe `custo_mp`, `custo_total`, `mc_cheia_rs`, `mc_cheia_pct`, `origem_fiscal`
  em `vw_cotacoes`, `vw_cotacoes_pendentes` e `vw_pedidos`, mais a flag
  `cancelado` em `vw_pedidos`
- `06_Docs/Softcomp_SQL_BI_Schema.md` regravado a partir do banco

## Estado final (validado no gold)

| view | itens com custo | R$ coberto |
|---|---|---|
| pendentes | 98,7% | 87,8% |
| encerradas 2026 | 99,5% | 97,9% |
| pedidos 2026 | 99,8% | 99,7% |

**O drift referência × real, medido:** −13,6% em 2025-26 (102.274 linhas de NF
única), **gap de R$ 22,5 MM**. Pela normalização por peso do agente: −16,8% e
R$ 33,7 MM em 18 meses; R$ 56,7 MM em 4 anos. **A causa é ganho de estocagem** —
item sob encomenda tem drift de −1,5% contra −11,9% do que sai do estoque, e em
2023 (aço em queda) o sinal inverteu. Praticamente todo o gap é MATRIZ.

**Dois achados que mudam decisão comercial:**
1. **O win rate SOBE com a margem** — 24,1% (MC<0) → 77,0% (MC>30%). Margem baixa
   não é preço agressivo: é sinal de que estamos fora de posição naquele item.
2. **A Vermelha está abaixo do custo** em 588 itens / R$ 8,8 MM, com WR de 91%.

**O YAML de cancelados pode virar backup**: o `StatusPedido` cobre **100%** dos
440 itens que ele declara (teste item a item — por pedido dá falso negativo, por
causa de cancelamento parcial).

Detalhamento completo: `06_Docs/Custo_Referencia_vs_Real_2026-08-01.md`.

## Pendências com o Nelson (o que sobrou)

1. **Histórico** — nova planilha, já combinado (a que o Gustavo rastreava)
2. `BI.Cotacao.DataEncerramento` — ⚠ **descoberta em 28/07, provavelmente não está
   na lista dele**: sem ela 11,7% das encerradas de 2026 ficam sem data e o ciclo
   emissão→fechamento não fecha
3. `BI.Cotacao.PrazoEntrega`, `RazaoSocial`; `BI.Pedido.SetorProducao`
4. Detalhe de custo: pedimos 9 componentes × real/cobrado, vieram 2 agregados —
   **decidir se o detalhe ainda é necessário** antes de cobrar
5. `BI.CondPagamentos`
6. `BI.RAF` continua espelhando o acúmulo do relatório do usuário (por isso o RAF
   segue manual)
7. **`BI.RAF.ValorMC` e `BI.RAF.LiquidoAco`** — acrescentadas em 02/08, ver abaixo

### Adendo 02/08/2026 — a MC não sobrevive à migração do RAF como a view está hoje

Gustavo rodou o RAF de julho na tela e pediu uma leitura do mês. Conferindo a
`BI.RAF` contra o gold no trecho que se sobrepõe (01–24/07, o que o portal já
tinha do export de 25/07), **linhas, NFs e valor líquido batem ao centavo** —
4.473 linhas, 1.729 NFs, R$ 11.192.985,64. A view é fiel. Mas ela tem **116
colunas contra as 133 do export**, e duas das que faltam são justamente as que
sustentam a MC da casa:

| falta | o que é | por que trava |
|---|---|---|
| `ValorMC` | MC do aço em R$ (= `LiquidoAco − ABCCUS_ACO`) | é o **numerador**; o motor lê essa coluna já calculada (`raf/enriquecer.py::derivar_margens`) |
| `LiquidoAco` | parcela do líquido atribuída ao aço | é o **denominador** do MC% do aço |

A view expõe `PercentualMC`, que **não** substitui: aplicado ao líquido de julho
dá R$ 4,11 MM contra os R$ 3,17 MM reais de MC do aço. Reconstruí a régua por
rota indireta — `(liq − ValorCustoTotal − CustodaMP) + Σ(Custo_X − Custo_X_Cob)`
— e o agregado fecha com resíduo de R$ 48 em R$ 3,73 MM (0,001%). Serviu para
ler julho, **mas proxy não é contrato**: por linha ela já erra (a NF 321056 da
SEW aparece com MC −R$ 10 mil quando o desvio real é −R$ 1,8 mil), e a origem
pode mudar sem aviso. Enquanto essas duas colunas não existirem, a rota A (view
lendo as tabelas de faturamento) **entrega faturamento sem margem** — o que
mataria o indicador central do portal.

**Armadilha de nome, já medida** (não é pendência dele, é documentação nossa):
`BI.RAF.ValorTottal` **não é o bruto da NF — já vem sem IPI**. Equivale ao
`faturamento_cimp` do gold, não ao `valor_bruto`. A diferença de R$ 298.946,63
em julho é, ao centavo, `SUM(ValorIPI)`. Bruto da NF = `ValorTottal + ValorIPI`.

E o item 6 ganhou prova nova: em 02/08 a view tinha **um mês só** (01 a 31/07),
exatamente o período que o Gustavo rodou na tela. O `conferir_colunas.py` passou
a checar isso sozinho — se `BI.RAF` tiver um único mês, ele avisa que a view
está espelhando relatório, não faturamento.

## Conexões

- [[Sistema Operacional Comercial/01 Sistema de Dados/01 - ERP Softcomp - Detalhes]] — inventário e pendências
- [[2026-07-20 — Integração SQL Softcomp (Gate 0) — desenho da operação]]
- [[Sistema Operacional Comercial/04 RAF/00 - Visão Geral RAF]] — onde o custo real é apurado
- Repo: `06_Docs/Softcomp_SQL_BI_Schema.md`, `MotorAnalitico/sql/conferir_colunas.py`
