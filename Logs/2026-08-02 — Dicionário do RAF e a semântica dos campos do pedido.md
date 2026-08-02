---
tipo: log
domínio: sistema-de-dados
criado: 2026-08-02
tags: [raf, softcomp, custo, margem, drift, dicionario, kpi]
---

# 2026-08-02 — Dicionário do RAF e a semântica dos campos do pedido

## Origem

Gustavo perguntou duas coisas sobre o achado de 01/08 (o RAF carrega o custo do
pedido dentro dele):

1. o custo apurado é **igual**, ou o RAF **importa** do pedido e mantém registrado?
2. as demais colunas do RAF estão todas validadas, com entendimento do
   significado, conexões e cálculos?

E enviou o **dicionário oficial do RAF**, que a Softcomp mandou em **18/04/2026** —
documento que estava fora do repo e do vault. Arquivado em
`06_Docs/Dicionario_RAF_Softcomp_2026-04-18.xlsx`.

## Resposta 1 — o RAF IMPORTA e registra

Confirmado pela fonte, não por dedução. O dicionário nomeia:
`ABCOIICUS_ACO` = **"Custo do aço do pedido"**; `ABCCUS_ACO` = "Custo Aço"
(o apurado). São campos distintos que convivem na mesma linha — diferem em
**99,9%** das linhas de 2026, e o de referência bate com o `CustoMP` da
`BI.Pedido` em **100%** das 36.798 linhas casadas.

Detalhe do dicionário: `ABCPES_ACO` é **"Peso baixado"**, não "peso do aço" — é
o que saiu do estoque, e não necessariamente o peso faturado.

## O erro que o dicionário expôs (e a correção)

O arquivo traz **dois exemplos da mesma nota** (OI 332314/01) com uma linha
marcando onde diferem. Os campos `ABCOII*` são **idênticos** nos dois; os de
apuração mudam. Isso confirmou que **o custo de referência é do pedido INTEIRO,
repetido em cada nota parcial**:

```
NF 316604  ped 338273 │ REAL  72.024 │ REF 215.755
NF 317153  ped 338273 │ REAL 105.266 │ REF 215.755   ← repetido
```

Medido: dos 1.814 itens faturados em várias notas em 2026, **100%** repetem.

**Correção necessária:** a tabela mensal de drift enviada em 01/08 estava
inflada. O drift correto de 2026 é **−13,9%**, não −34%. O número consolidado
(R$ 22,5 MM em 2025-26) já estava certo — a query mensal foi reescrita do zero
e não replicou o tratamento. Vale para toda aquela tabela, inclusive a coluna
"MC aço REF" negativa, que era artefato do mesmo problema.

Risco verificado e descartado: no 1º exemplo o custo apurado é **zero** (nasce
zerado, é preenchido depois). Não nos afeta — **100%** das linhas de 2026 chegam
apuradas, porque o export é feito após a apuração.

## Resposta 2 — documentadas sim, usadas não

| | |
|---|---|
| colunas documentadas pela Softcomp | **133 de 133** |
| colunas que o motor consome | **89 (67%)** |
| **nunca tocadas** | **44 (33%)** |

Foi exatamente numa dessas 44 que estava o `ABCOIICUS_ACO`. O dicionário é
melhor do que se esperava — traz significado e legenda de código de todos os
campos. O problema nunca foi falta de documentação: foi ela estar fora do
sistema, num anexo de e-mail de abril.

Catálogo completo das 133, agrupado e marcado com uso, em
[[Sistema Operacional Comercial/04 RAF/01 - Estrutura das 133 Colunas]].

### Não usadas COM dado (vale investigar)

`ABCSETPDES` setor de produção **100%** · `ABCOII_PRA` prazo da OI **99,7%** ·
`ABCOIIQUA` nível da qualidade **99,3%** · `ABCTRA` transportadora **96,2%** ·
`ABCTRA_PROPRIO` cliente retira 58,2% · `ABCCPL_1` info complementar 56,1%.

**`ABCSETPDES` resolve uma pendência aberta com o Nelson** — foi pedido como
coluna nova na `BI.Pedido` e já existe no RAF com 100% de preenchimento.

### Não usadas SEM dado (lacuna de processo, não de sistema)

A família inteira da **OC** — `ABCOIINUM_OC`, `ABCOCCFOR` (fornecedor),
`ABCOCIENTREGA` (data de entrega) — está em **0,2%**. O agente analítico
registra "sem fonte de OC" como lacuna; a coluna existe, **o ERP é que não é
preenchido**. Se a análise de ruptura importa, o caminho é disciplina de
cadastro, não pedido à Softcomp.

## Achados de negócio que este trabalho consolidou

Medidos no lake, documentados em `06_Docs/Custo_Referencia_vs_Real_2026-08-01.md`:

1. **Drift de custo −13,9% (R$ 22,5 MM em 2025-26).** O custo que o vendedor usa
   para precificar é sistematicamente MAIOR que o apurado. **A causa é ganho de
   estocagem**, não erro: item sob encomenda tem drift de −1,5% contra −11,9% do
   que sai do estoque, e em 2023 (aço em queda) o sinal **inverteu**.
   → *Parte da margem que o RAF reporta é ganho de estoque, não margem
   comercial.* Praticamente todo o gap é MATRIZ.
2. **O win rate SOBE com a margem** — 24,1% (MC<0) → 77,0% (MC>30%). Margem baixa
   não é preço agressivo para ganhar: é sinal de que estamos **fora de posição**
   naquele item. Ganha menos *e* rende menos. Inverte a leitura do Foco do dia.
3. **A tabela Vermelha está abaixo do custo** em 82 itens pendentes / R$ 1,41 MM
   (96% concentrado em PROK BRASIL) e em 588 itens / R$ 8,8 MM nas encerradas de
   2026, com **WR de 91%** — ganhamos justamente onde a tabela está furada.
4. **Só 18% do que perdemos por preço tinha margem para dar** (R$ 15,7 MM de
   R$ 130,7 MM) — mata a narrativa "perdemos por preço".

## Lição de processo

Duas descobertas desta semana (`ABCOIICUS_ACO` e a repetição em notas parciais)
mostram o mesmo padrão: **o dado existia, a documentação existia, e nenhum dos
dois estava no sistema**. O dicionário ficou 3 meses num anexo de e-mail
enquanto se deduzia o significado das colunas por engenharia reversa.

Regra que fica: **documento de fornecedor sobre estrutura de dado entra no repo
e no vault no dia em que chega.** Vale para o dicionário do RAF, para o layout
das views BI e para o que o Nelson mandar daqui em diante.

## Conexões

- [[Sistema Operacional Comercial/04 RAF/01 - Estrutura das 133 Colunas]] — catálogo completo
- [[Sistema Operacional Comercial/04 RAF/05 - Custo Real vs Cobrado]]
- [[2026-08-01 — Custo na cotação e no pedido (entrega Nelson)]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/01 - ERP Softcomp - Detalhes]]
- Repo: `06_Docs/Dicionario_RAF_Softcomp_2026-04-18.xlsx`,
  `06_Docs/Custo_Referencia_vs_Real_2026-08-01.md`
