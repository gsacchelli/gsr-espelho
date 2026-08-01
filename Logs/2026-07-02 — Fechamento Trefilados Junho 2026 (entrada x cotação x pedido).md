---
data: 2026-07-02
tipo: fechamento comercial / análise de lançamento
projeto: Material Trefilado (Família 892 — 1020/1045)
status: relatório entregue (v1) + análise de disponibilidade
---

# Fechamento Trefilados — Junho 2026 (1º mês da linha)

Recorte de dados: aço **1020/1045**, perfil **Redondo**, acabamento **Trefilado** (Família 892). Fontes: AFS-Lake (`vw_pedidos`, `vw_cotacoes`, `cotacoes_pendentes_enriquecido`) + planilha de entradas ArcelorMittal (`entrada trefilados.xlsx`).

## Números do mês

| Bloco | Valor |
|---|---|
| **Entrada (recebimento)** | **187,6 t** (1020: 92,4 t · 1045: 95,2 t) — a partir de 15/06. ≈38% das 500 t iniciais |
| **Vendas (pedidos)** | **R$ 67,2 mil · 7,7 t · 13 itens** |
| **Cotado no mês (encerradas)** | **R$ 573,8 mil · 148 itens · 65,3 t** |
| **Win rate (encerradas, valor)** | 5,4% (12 ganhou / 136 perdeu) |
| **Pipeline pendente** | **R$ 136,6 mil · 25 clientes · 51 itens · 14,9 t** (aging fresco 0–3 d) |

Entrada por dia (kg): 15/06 40.959 · 17/06 36.984 · 18/06 33.926 · 19/06 19.461 · 23/06 31.223 · 24/06 21.277 · 29/06 3.771.

## Contexto de meta (definido 02/07)
Meta de **150 t/mês** a ser atingida em **5–6 meses** (ramp), não no 1º mês. Junho (7,7 t) é base de partida — o relatório não deve tratar como "miss", e sim como início da curva.

## Achado central — DEMANDA veio antes do ESTOQUE

A campanha de marketing (2 semanas antes do lançamento) gerou cotações desde **1º de junho**, mas o material só entrou em **15/06**. Cruzando cada cotação encerrada com a data em que a bitola foi recebida:

| Situação na data da cotação | Itens | Valor cotado | % valor | Win rate (valor) |
|---|---|---|---|---|
| **A. Bitola não recebida em junho** | 81 | R$ 309,4 mil | **54%** | 1,1% |
| **B. Cotou antes da bitola chegar** | 24 | R$ 146,8 mil | 26% | 13,9% |
| **C. Bitola disponível na cotação** | 43 | R$ 117,6 mil | 20% | 6,2% |

**Leitura:** 80% do valor cotado (A+B) foi para bitolas que **não estavam fisicamente disponíveis** no momento da cotação. A baixa conversão do 1º mês é, em grande parte, **restrição de disponibilidade**, não falha de venda. Mas atenção: mesmo no bucket C (bitola disponível), win rate é só 6,2% — logo, pricing/conversão também pesa; não dá pra atribuir tudo ao estoque.

## Cobertura de bitolas — 17 de ~41

Curva padrão = 41 bitolas (25 no 1045 + 16 no 1020, Anexo B da política). Em junho recebemos **17 SKUs** (9 do 1020, 8 do 1045). Recebido skew para bitolas pequenas/médias (19,05 · 25,4 · 25,0 · 22,22 · 31,75 · 50,8) enquanto a demanda puxou as grandes.

**Top bitolas demandadas e NÃO recebidas em junho (lista de reposição prioritária):**
- 1045 38,10 mm — R$ 42,5 mil (3 itens)
- 1020 63,50 mm — R$ 27,3 mil
- 1045 35,00 mm — R$ 27,2 mil
- 1020 76,20 mm — R$ 22,3 mil
- 1045 50,80 mm — R$ 15,7 mil · 1020 38,10 mm — R$ 13,1 mil · 1045 44,45 / 57,15 / 63,50 / 60,32...

Quase todas são bitolas **padrão de alto giro** (38,10 é a #1 da curva Anexo B para ambas as ligas). Sinal claro para a próxima OC ArcelorMittal.

## Clientes que compraram (junho)
JACTO (R$ 43,9 mil — **65% do faturamento**, cliente-âncora Estratégicos), CASALE (R$ 8,2k), TECPARTS (R$ 6,3k), WM REDUTORES (R$ 5,7k), MEGASTEEL, DE NADAI, BRANIVA, INTERMETRIC, USINAGEM J.J. Vendas concentradas em **Verde/Amarela** (aderente à política; 2 pedidos em Vermelha, 0 em Preta).

## Maiores perdas (encerradas) — reabordar com estoque
FEEDER (6 t, Vermelha, R$ 51k) · AUROTEC (6 t, R$ 50k) · C.C.S. (R$ 66,6k somados) · AGROSTAHL e OLIVO (Preta). Muita perda por preço em Vermelha/Preta.

## Pipeline aberto — priorizar
PROK BRASIL R$ 64,8 mil (47% do pipeline, Vermelha, 6,5 t) · FUJII R$ 16k (Preta) · MASTERMAG R$ 15k (Amarela).

## Entregáveis
- `Fechamento_Trefilados_Junho_2026.html` (relatório v1, corpo de e-mail, gráfico entrada×vendas embutido).
- `grafico_tri_fluxos_junho.png` (entrada × cotação × pedido por dia).

## Próximos passos / a evoluir
- Enviar OC de reposição priorizando as bitolas do bucket A (38,10; 63,50; 76,20; 35,00; 50,80).
- v2 do relatório com: gráfico tri-fluxo, cobertura 17/41, tabela de disponibilidade (A/B/C), shopping list de bitolas.
- Acompanhar conversão do bucket C (disponível) isoladamente — é o termômetro puro de pricing/venda, sem ruído de estoque.
- Diluir dependência de JACTO ativando cross-sell.

---

## E-mail enviado — 02/07/2026, 10:05

**Para:** Fernando Roveda, Odair Oliveira, Fabíola Cardoso Piazza, Fuscão, Felipe Sória, **Francisco França (marketing)**. **Cc:** Wagner Sacchelli.
**Assunto:** Material Trefilado - Junho 26

Gustavo enviou uma versão enxuta do relatório v2 (manteve o achado central de disponibilidade + tabela A/B/C + cobertura 17/41; cortou tabelas de clientes/pipeline e o gráfico de reposição). Ajustes de conteúdo relevantes vs. draft:
- **Novo direcionamento estratégico:** "não somos a preferência deste produto, mesmo em clientes tradicionais da Sacchelli" → **foco em prospecção e contato ativo**.
- **Nova ação atribuída:** @Francisco França (marketing) apresentar **relatório da prospecção dos clientes com foco no trefilado, fora das carteiras dos vendedores** (base SDR/prospecção).
- Manteve a ressalva de pricing como ação: conversão de 6,2% nas bitolas em estoque "é % baixo, precisamos avaliar e entender os motivos".
- Meta 150 t/mês reafirmada como maturação 5–6 meses.

### Texto enviado (íntegra)

> **Material Trefilado** — Junho / 2026 · Família 0892 (1020 e 1045 · Redondo · Trefilado) · Unidade Guarulhos
>
> Fechamos o primeiro mês do início dos trefilados. Recebemos 187,6 ton a partir de 15/06 (≈38% das 500 ton iniciais). As vendas começaram em ritmo lento, mas esperado para um lançamento.
>
> Após a campanha de marketing em junho tivemos R$ 573,8 mil cotados contra R$ 67,2 mil faturados, sendo 80% dessa demanda em bitolas que ainda não estavam disponíveis no estoque.
>
> **KPIs:** Entrada 187,6 ton (recebidas em jun) · Vendas R$ 67,2 mil (7,7 ton · 13 itens) · Cotado no mês R$ 573,8 mil (148 itens · 65,3 ton) · Pipeline aberto R$ 136,6 mil (25 clientes · 14,9 ton).
>
> **1 · Demanda chegou antes do estoque.** Material começou a entrar no estoque a partir de 15/06. Cruzando cada cotação com a data em que a bitola foi recebida: 54% do valor cotado foi para bitolas que não chegaram em junho e outros 26% foram cotados antes de a bitola entrar. Só 20% da demanda encontrou a bitola disponível. Ou seja, a baixa conversão do mês, mesmo que esperada, em grande parte foi falta de disponibilidade. A conversão das bitolas em estoque ficou em 6,2%, % baixo e precisamos avaliar e entender os motivos.
>
> | Situação na data da cotação | Itens | Valor cotado | % valor | Win rate |
> |---|---|---|---|---|
> | Bitola não recebida em junho | 81 | R$ 309,4 mil | 54% | 1,1% |
> | Cotou antes de a bitola chegar | 24 | R$ 146,8 mil | 26% | 13,9% |
> | Bitola disponível na cotação | 43 | R$ 117,6 mil | 20% | 6,2% |
>
> **3 · Estoque Disponível.** Do estoque padrão de 41 bitolas (25 no 1045 + 16 no 1020), recebemos 17 bitolas em junho (≈41%) — com tendência para as bitolas menores, enquanto as cotações solicitam bitolas maiores.
>
> **Leitura e próximos passos:**
> • A demanda existe — o gargalo do 1º mês foi disponibilidade.
> • Meta de 150 t/mês é referência de maturação (5–6 meses); junho é a base de partida da curva.
> • Manter foco na prospecção e contato com os clientes — não somos a preferência deste produto, mesmo em clientes tradicionais da Sacchelli.
> • @Francisco França apresentar relatório da prospecção dos clientes com foco no trefilado, fora das carteiras dos vendedores.
