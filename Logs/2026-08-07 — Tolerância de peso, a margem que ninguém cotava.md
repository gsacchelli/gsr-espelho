---
data: 2026-08-07
tipo: log
status: vigente
---
# Tolerância de peso — a margem que ninguém cotava

**Origem:** revisão dos bloqueios de pricing. Ao revogar o bloqueio da TER
BRASIL ("preços autorizados, baixos mas estratégicos"), o Gustavo apontou:
*"entre o peso atualizado e o peso faturado deve existir uma diferença — um
'chute no peso' que faturamos a mais do que o peso real"* — e pediu para
verificar se isso reflete na margem do RAF. Refletia. E era maior do que
parecia.

## O mecanismo (confirmado por print do ERP)

O campo **`Tolerância`** do cadastro do cliente (tela CP51010, aba Dados de
Controle) é um percentual que o Softcomp SOMA ao peso na hora de faturar:

```
peso faturado (ABCQTD) ≈ peso baixado (ABCPES_ACO) × (1 + Tolerância%)
```

O custo do aço, porém, é apurado pelo peso **BAIXADO** (`ABCPFAPESFAT = 2` em
99,9% das linhas; confirmado por dispersão — custo÷baixado tem CV 0,38 contra
1,10 do custo÷faturado). **O kg extra entra na receita e não entra no custo:
é margem inteira, embutida no `ValorMC` sem ninguém ver.**

## Validação (RAF 2026)

- **Só atua na venda POR PESO** (hipótese do Gustavo, confirmada): vendas KG
  têm 38,8% das linhas com gap; por PEÇA são 12 linhas em 12.486; por METRO,
  1 em 439.
- **É parâmetro, não acaso**: o gap mediano por cliente agrupa em degraus
  redondos — **97 clientes em 1,0% · 57 em 3,0% · 15 em 2,0%**. TER BRASIL
  (cadastro 03%) mede +3,0% em 116 de 125 linhas.
- **Tamanho na casa (2026)**: +77.921 kg faturados além do baixado →
  **R$ 651 mil ≈ 2,2% da MC do aço** (R$ 29,2 MM). Guardas de análise
  passaram (sem concentração, sem linha dominante).
- **TER BRASIL**: R$ 33,6 mil de ganho de peso sobre MC total de R$ 70,4 mil
  — **48% da margem do cliente vem do peso, não do preço**. Se o cliente
  exigir faturamento por peso pesado, a margem cai pela metade.
- Lado negativo (faturar MENOS que o baixado): −61 mil kg nas vendas KG,
  metade com corte — fenômeno separado (quebra/ponta), não é tolerância.

## A aritmética que importa (para não errar depois)

**NÃO é um 8º spread.** `MC_Total = MC_Aco + MC_Spread` e o ganho de peso já
está DENTRO do `MC_Aco` (a identidade `ValorMC = LiquidoAco − ABCCUS_ACO`
fecha ao centavo em 39.777/39.777 linhas). Somar a tolerância ao MC_Total
contaria em dobro. O correto é **decomposição do MC do Aço**:
`MC_Aco = margem de preço + margem de tolerância`.

Conceitualmente o Gustavo tem razão em chamá-la de spread — é margem que a
cotação NÃO considera ao fechar (a definição da casa para "Margem Agregada").
Mas na conta ela mora dentro do MC_Aco.

## O que foi implementado

- **Motor RAF** (`raf/enriquecer.py::derivar_tolerancia_peso`): 3 colunas
  novas no enriquecido — `Peso_Gap_Kg` (assinado), `Tolerancia_pct`,
  `MC_Tolerancia_RS` (só gap positivo, venda por peso, fora de
  Beneficiamento — material do cliente). 9 testes novos (suite 149/149).
- **Gold**: `vw_faturamento.peso_gap_kg` + `mc_tolerancia`, com o aviso de
  dupla contagem no próprio SQL.
- **Portal / Visão Geral**: card "dentro do MC Aço: tolerância de peso"
  junto à Composição da Margem, antes do Breakdown do MC Spread — rotulado
  como decomposição, nunca como 8ª barra.
- **Dicionário de Fontes** (`raf_custos.yaml`): verbetes de `ABCQTD` (o
  rótulo oficial "Peso" esconde a tolerância), `ABCPFAPESFAT` (a flag que
  faz a tolerância virar margem — se migrar para '1', o ganho deixa de
  existir) e `ABCOIIUNP` (análise sem filtrar KG/TN dilui o sinal).

## Respostas do Gustavo (mesma sessão, 07/08/2026)

- **Por que os degraus 1/2/3%? Não há padrão — é NEGOCIAÇÃO, limitada pela
  balança do cliente.** Textual: *"onde dá para aumentar, tentamos... a
  maioria dos clientes tem balança no recebimento, 1% passa na maioria."* Ou
  seja: alavanca comercial deliberada e informal, calibrada pelo que o
  recebimento do cliente tolera — não é compensação estrutural de laminação.
  Os 97 clientes em 1% são o teto do que passa com balança; os degraus
  maiores são onde deu para subir.
- **O parâmetro NÃO entra em export nenhum, por decisão.** O assunto fica
  *"escondido de todos"* — pedir a coluna ao Nelson espalharia numa view o
  que hoje só existe tela a tela no CP51010. A tolerância do lake segue
  INFERIDA do gap (validada nos degraus: TER BRASIL 03% → +3,0% medido), o
  que é suficiente E mais discreto. Pendência Nelson: **cancelada**.
  ⚠ Pelo mesmo motivo, o número não vai a artefato de gerência: o cartão
  vive só na Visão Geral (portal single-user); Montar Relatório e relatórios
  de gerência NÃO o recebem.
- **TER BRASIL, correção de leitura**: o mix é **20MnCr5 em barra a R$ 8,90/kg
  bruto (ICMS 12%)** — 94% do peso (190 t), líquido medido R$ 7,35/kg (a
  conta 8,90 × 0,88 × 0,9075 dá 7,11). O "R$ 6,00/kg" citado antes era só
  das 6 linhas de maior gap, outro item. E **a estratégia é o VOLUME na
  região de Caxias do Sul**, não a margem do peso — a tolerância de 3% é
  consequência da negociação, não o motivo da conta.

## Prova de não-contaminação (pergunta do Gustavo, mesma sessão)

Gustavo: *"no engenheirado o baixado costuma ser MAIOR que o faturado, assim
como trefilados, descascados, desbastados, usinados — como está separando?"*
Medido no RAF 2026:

- **Engenheirado**: 24 linhas no ano — 7 por peça (fora pelo filtro de
  unidade) e **17 por KG com gap exatamente ZERO** (faturado = baixado ao kg
  em todas: AEROACO, SÃO JOÃO, NEWFER, RFR). O ERP não aplica tolerância no
  engenheirado. Nenhum entra.
- **Remoção de material em processo** (desbaste/usinagem): aparece como gap
  NEGATIVO — Laminado −43 mil kg, Forjado −17,7 mil kg — e gap negativo
  nunca vira `MC_Tolerancia_RS` (só `Peso_Gap_Kg` assinado).
- **Trefilado/Descascado/Usinado DE ESTOQUE entram, e devem**: a barra em
  estoque já está no acabamento, a baixa é do produto pronto — gap positivo
  nos mesmos degraus (medianas +1,8% / +1,0% / +2,0%) e **zero linhas
  negativas** nesses acabamentos.
- **Corte não contamina**: linhas com corte medem mediana +1,72% com p25–p75
  em 1,00–3,00% — os mesmos degraus das sem corte. Se a baixa somasse a
  ponta, os degraus borravam; não borram → `ABCPES_ACO` já é líquido do
  corte.

Conclusão: os R$ 625 mil de 2026 são tolerância pura — sem mistura com perda
de processo, engenheirado ou beneficiamento.

## Pendência restante

- **Cotação**: ao precificar, a tolerância é margem invisível a favor —
  simulador e cockpit não a consideram. Avaliar se entra como informação no
  Simulador de Precificação (não no preço, na leitura de margem esperada).

## Relacionado

- `04 RAF/02 - Convenção Softcomp (Invertida)` — semântica de custos
- Memória `raf-convencao-custos-auditada`
- `Logs/2026-08-07 — Auditoria do time Stalo...` (mesma sessão)
