---
data: 2026-08-07
tipo: log
status: vigente
---
# Acesso ao servidor Softcomp (mapa + procedimento) e o piloto da idade do estoque

## A decisão

O Gustavo abriu o acesso de leitura ao share do Softcomp
(`smb://10.0.0.216/h`, montado por ele no Finder) para **pesquisa,
conferência e parâmetros que não existem no SQL** — nunca para pipeline.
Nasceram: **`06_Docs/Mapa_Programas_Softcomp.md`** (18 programas mapeados por
prints dele: SP8203 parâmetros de precificação POR UNIDADE, SP3010/A famílias
com margens, SP7120C fases com custo/fornecedor, CP95400C duplicatas,
CP55030* estoque por lote, SP7001C/P fases da produção com timeline, CP99S041
orçamento previsto×realizado, SP3008P/3009* movimentação de lotes) e a
**skill `consultar-softcomp`** (o ritual: mapa → montagem → cópia → extração
com âncora → validação com gabarito → sensível fora do repo).

Regras duras: READ-ONLY, .DAT nunca vira fonte de produção (decisão 26/07
mantida), extração sem validação não circula, print de programa novo deve
mostrar a barra de status (revela o .DAT).

## Primeiro fruto: tolerância do CP51010

`CD51CLI.DAT` extraído e validado contra o gap medido (22-23/25 exatos) →
`CD51CLI_Tolerancias.csv` com 14.656 clientes (fora do repo, assunto
reservado). 🪤 Descoberto no caminho: cliente tem múltiplas fichas por
filial e a legível pode ser a DORMIDA — caso HENFEL (ficha de 1995 diz 1%,
balança fatura 3% cravado). **Ficha legível ≠ ficha em uso; o comportamento
medido vence.**

## Piloto: idade do estoque por lote (a pergunta do turnaround)

**Lição nº 1 do piloto: a resposta estava em casa.** Comecei decifrando o
`CD23LOT` no share e parei no meio — o export mensal
`01_Brutos/EstoqueAnalitico/Posicao analitica*.xlsx` (que o Gustavo já baixa)
traz **data de entrada POR LOTE**, com fornecedor, NF e NCM. O silver é que
descartava a dimensão ao agregar por SKU. Regra nova no mapa: antes de
decifrar .DAT, conferir se um export existente já carrega o dado.

⚠️ **A TABELA ABAIXO ESTÁ SUPERADA — ver a correção mais adiante neste log.**
Ela veio dos exports de junho, que estavam TRUNCADOS em 5 das 6 unidades.
Fica registrada porque o erro é a lição: o parque "reconciliou ao centavo"
com a auditoria de 03/08 porque **as duas leram os mesmos arquivos cortados**.
Reconciliação contra fonte que compartilha o defeito não é validação.

**Resultado (posição jun/2026 — INVÁLIDO, exports truncados):**

| Época | Lotes | Peso | R$ líquido | % parque |
|---|---|---|---|---|
| até 2015 (10+ anos) | 6.159 | 628 t | 1,95 MM | 3,2% |
| 2016-2019 | 4.597 | 1.762 t | 6,64 MM | 10,9% |
| 2020-2022 | 2.179 | 399 t | 2,18 MM | 3,6% |
| 2023-2024 | 3.129 | 1.292 t | 5,70 MM | 9,4% |
| 2025-2026 | 7.046 | 11.067 t | 44,4 MM | 73,0% |

**★ Pré-2020: 10.756 lotes · 2.390 t · R$ 8,6 MM líquido (14,1% do parque).**

Leitura: 73% do valor é fresco — reposição saudável, problema não é geral.
Dois alvos DISTINTOS: os R$ 6,6 MM de 2016-2019 (lote médio 383 kg —
vendável, alvo de liquidação); os R$ 1,95 MM de 10+ anos (lote médio 102 kg —
pontas/sobras: leilão ou sucata, quase write-off). Concentração: os lotes
velhos mais caros estão em PIRACICABA e SÃO CARLOS — as unidades cuja posição
não traz descrição (só NCM): ninguém vê O QUE está parado sem ir ao ERP.
⚠ Idade e excedente-sobre-regulador (~R$ 30,3 MM) são réguas diferentes —
não somar; parte é interseção.

🪤 Armadilhas do export, pegas pelas guardas: linhas 'Totais'/'#' no MEIO dos
dados (somar cru dobra o parque — a 1ª rodada deu R$ 124,6 MM e a guarda de
reconciliação travou) e SAFRA (arquivos de 03/08 = posição de junho; julho a
Roberta gerou 07/08 9h56).

## ⚠ CORREÇÃO NA MESMA SESSÃO — os exports de junho estavam TRUNCADOS

Ao receber a posição de JULHO (Gustavo exportou as 6 unidades em 07/08), a
pirâmide não bateu: pré-2020 saltou de 10.756 lotes (junho) para 3.047
(julho). Impossível em um mês → investigação → **os arquivos de junho, no lake
desde 03/08, estavam cortados em 5 das 6 unidades.**

Assinaturas encontradas: **Anchieta** trouxe 19 de 980 lotes (códigos 13→31,
**100% consecutivos** = 1ª página); **Caxias** parou em **2018** (zero lotes
de 2019-2026); Rio Preto e Piracicaba idem. Só **Guarulhos** veio completo —
e como ele é 85% do peso, o total pareceu plausível e ninguém desconfiou.
O corte deixava passar justamente os LOTES ANTIGOS, o que inflou a pirâmide.

🪤 **Suspeita não é prova:** São Carlos disparou meu detector (só 16,4% de
lotes recentes) e estava ÍNTEGRO — a unidade tem mesmo 1.872 lotes pré-2020,
**583 deles com menos de 5 kg** (média 31,7 kg). É resíduo de cadastro, não
truncagem. Só o total da tela decide.

## Números corretos (posição julho/2026, 6 unidades, validado ao centavo)

| | 03/08 (truncado) | 07/08 (completo) |
|---|---|---|
| Parque, custo c/ impostos | R$ 82,79 MM | **R$ 132,51 MM** |
| Parque, custo líquido | — | **R$ 100,09 MM** |
| R$/kg | 5,35 | **6,65** (líq. 5,02) |
| Peso | 15.485 t | **19.940 t** |

**Anchieta é unidade da MESMA empresa** (Gustavo, 07/08) e responde sozinha
por **41% do valor**: R$ 54,2 MM em 980 lotes de forjado grande (4340,
D17-18CrNiMo7-6, Ø600-790mm) a **R$ 9,79/kg** contra R$ 5,44/kg no resto.

**PIRÂMIDE DE IDADE (a pergunta original):** pré-2020 é só **1,0% do parque**
(3.047 lotes · 371 t · R$ 1,02 MM líq). **88% do valor entrou em 2025-26.**
A tese de "estoque morto por idade" NÃO se sustenta — e essa é a notícia boa.
O velho real são R$ 657 mil em Guarulhos (material vendável) e R$ 221 mil em
São Carlos em micro-lotes (baixa de cadastro).

## O que isso derruba, e precisa ser refeito

- O **excedente de ~R$ 30,3 MM** e a **cascata do turnaround (R$ 78 MM →
  ~R$ 24 MM)** foram derivados do parque truncado. Recalcular.
- 🪤 Reabilita um descarte de 03/08: "quantidade do ERP × preço da
  contabilidade dá R$ 108,9 MM, **estoura o balanço**" foi rejeitado contra
  uma âncora truncada. O líquido real (R$ 100,09 MM) fica PERTO desse valor —
  a rejeição pode ter sido do número certo.
- A frase "posição só traz Descrição em Guarulhos e Anchieta (86% do peso)"
  foi medida no truncado; com dados completos são **92%**.

## Regra nova (vale para TODO export de tela)

**Export de tela pode vir truncado em silêncio** — abre, soma e parece
plausível. Todo export entra com a **contagem e os totais da TELA anotados**,
e o loader reprova se não bater. Assinaturas: códigos consecutivos em alta
proporção · faixa de anos que não alcança o mês corrente · contagem abaixo
do `#` do rodapé.

## Pendente (proposto, sem decisão)
Silver por lote + pirâmide de idade como bloco permanente da página Estoque —
agora com a validação contra os totais da tela embutida no loader.
