---
tipo: referência-comercial
domínio: cotações
criado: 2026-08-02
última-revisão: 2026-08-02
tags: [cotacoes, margem, win-rate, pricing, tabela-vermelha, kpi]
---

# 06 — Margem × Win Rate (curva empírica)

Achados medidos no lake em 01-02/08/2026, quando o ERP passou a expor custo na
cotação (`BI.Cotacao.CustoMP`/`CustoTotal`, 99,4% de cobertura). Pela primeira
vez dá para cruzar **margem prevista × desfecho** por item.

Base: encerradas de 2026, disputa real (exclui orç. prévio e enc. administrativo).

---

## 1. O win rate SOBE com a margem — e isso inverte a leitura padrão

| MC bruta na cotação | itens | **win rate** |
|---|---|---|
| < 0% | 174 | **24,1%** |
| 0–10% | 5.751 | 41,1% |
| 10–20% | 40.282 | 57,8% |
| 20–30% | 13.769 | 65,6% |
| > 30% | 3.029 | **77,0%** |

**A leitura intuitiva está errada.** Margem baixa não é "preço agressivo para
ganhar o negócio" — é sinal de que **estamos fora de posição naquele item**:
material que não temos, comprado caro, ou fora da nossa linha. **Ganha menos
E rende menos.**

Consequência operacional: o Foco do dia não deve tratar margem baixa como
oportunidade a perseguir. O oposto.

### Confirmação pelo outro lado

Das perdidas por preço em 2026 (21.030 itens / R$ 130,7 MM, MC mediana 14,8%),
**só 18% (R$ 15,7 MM) tinham MC ≥ 20%** — ou seja, espaço real para baixar preço
existe em R$ 15,7 MM, não nos R$ 130,7 MM.

> Isso mata a narrativa "perdemos por preço". Na maior parte do que perdemos,
> **não havia margem para dar**.

---

## 2. A tabela Vermelha está abaixo do custo em parte do mix

A Vermelha é o **piso operacional**: vender abaixo dela exige alçada. Mas quando
o próprio piso não cobre o custo, **o vendedor cumpre a regra e a operação perde
dinheiro** — e ninguém vê, porque a régua diz que está tudo certo.

| recorte | itens | R$ | win rate |
|---|---|---|---|
| pendentes (02/08) | 82 | R$ 1,41 MM | — |
| encerradas 2026 | 588 | R$ 8,8 MM | **91%** |

**Ganhamos justamente onde a tabela está furada.** Concentração nas pendentes:
**PROK BRASIL — 12 itens / R$ 1,36 MM** (96% do valor), forjado no perfil com
sobremetal, MC na Vermelha de −42% a −123%. Nas encerradas: 0511 Forjado
Importado (R$ 3,52 MM), **99RV "família genérica" (R$ 1,82 MM, WR 100%)**,
0016 Laminado Importado.

A razão mediana Vermelha ÷ custo é **1,15** (a tabela carrega ~15% de markup);
abaixo de 1,00 estamos comprando participação com dinheiro.

⚠️ **Régua correta:** custo **TOTAL** (que já embute impostos) contra preço
**BRUTO**. Comparar o custo do *aço* dá zero casos — o aço é ~63% do custo total,
então sobra margem sobre ele mesmo quando a operação não se paga.

**No Cockpit:** alerta no drawer, faceta "Tabela vs custo" no rail, e card no
Dashboard que só aparece quando há caso.

---

## 3. A margem está sendo decidida no feeling — e o feeling acerta

**11,3% do faturamento de 2026 (R$ 13,7 MM) saiu com MC de referência NEGATIVA**
— e em **92% dessas linhas o real virou positivo**. A empresa aceita negócio
"vermelho no papel" por intuição e acerta, porque a referência é pessimista
(ver §4).

Na outra ponta: **780 linhas / R$ 1,8 MM fecharam com MC real negativa**, e 37%
delas tinham referência ≥ 15% — o custo enganou para cima. Perda apurada
R$ 290 mil.

---

## 4. Por que a referência é pessimista: ganho de estocagem

O custo do ERP é de **REPOSIÇÃO** (repor o aço hoje); o do RAF é do **LOTE
histórico** (o que pagamos). Drift medido: **−13,9%** em 2025-26,
**R$ 22,5 MM**. Três provas de que é ganho de estoque, não erro:

1. item sob encomenda (não passa pelo estoque): drift **−1,5%**; item do
   estoque: **−11,9%**;
2. em **2023 o sinal inverteu** (o aço caiu, o estoque velho ficou mais caro);
3. importado **−18,4%** contra nacional **−5,9%** (ciclo de estoque mais longo).

> **Parte da margem que o RAF reporta é ganho de estoque, não margem comercial.**
> Enquanto o estoque comprado barato durar, o resultado parece melhor do que a
> operação corrente sustenta. Praticamente todo o gap é **MATRIZ** — as filiais
> giram rápido e ficam com referência ≈ real.

**Indicador a acompanhar:** se a margem de reposição cair e a do RAF não, o
ganho de estoque está secando — aviso de precificação com meses de antecedência.

---

## Três réguas de MC, nenhuma comparável sem conversão

| régua | fórmula | base | mediana |
|---|---|---|---|
| cotação (`mc_cheia_pct`) | 1 − CustoTotal/ValorTotal | **bruta** | 17,0% |
| RAF (`ABCPER_MAR`) | ValorMC / LiquidoAco | líquida do aço | 31,0% |
| Cockpit (`mcp`, régua ck-2) | (líquido − custo aço) / líquido | **líquida** | 30,8% |

Diferença de ~14 pp entre cotação e RAF vem de duas coisas medidas: o
`CustoTotal` do ERP **já embute impostos** (resíduo estável de ~8,5% do bruto), e
o overhead do custeio da cotação vale **29,5% do bruto** contra 11,4% do
`ABCCUS` real — o custeio da cotação é ~2,6× mais pesado.

Tabela de conversão MC-cotação → MC-real (112.929 linhas 2025-26) e P(prejuízo)
em `06_Docs/Custo_Referencia_vs_Real_2026-08-01.md`. **Ainda não validada contra
um mês fechado** — pendência com Gustavo antes de virar régua oficial.

---

## Conexões

- [[05 - Win Rate e Métricas]] — definição canônica de WR e disputa real
- [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]] — a Vermelha como piso
- [[Sistema Operacional Comercial/04 RAF/01 - Estrutura das 133 Colunas]] — de onde vem o custo real
- [[2026-08-02 — Dicionário do RAF e a semântica dos campos do pedido]]
- [[2026-08-01 — Custo na cotação e no pedido (entrega Nelson)]]
