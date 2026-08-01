# Dicionário — Produto, Acabamento e Engenheirado (RAF / Faturamento)

**Definido com Gustavo em 02/07/2026. Decisões fechadas — não re-litigar.**
Fonte técnica: `vw_faturamento` (gold DuckDB) ← `raf_enriquecido` ← RAF. Base = NF faturada, `Op_Categoria='Venda'`, `Considerar_Analise=true`.

## A distinção que gera confusão: PRODUTO faturado vs MATERIAL de partida

O RAF tem **dois conjuntos** de campos, e misturá-los foi a origem da confusão:

| Conceito | Campos crus (Softcomp) | O que é |
|---|---|---|
| **Produto faturado** | `ABCPER_DES`, `ABCACA_DES`, `ABCPRO_DES` | O item vendido na NF |
| **Material de partida** | `ABCMAT_PER_DES`, `ABCMAT_ACA_DES`, `ABCMAT_DES` | A barra (matéria-prima) de onde a peça saiu |

Para **catalogados** os dois coincidem. Para **engenheirados** o produto é texto livre e **só o material de partida traz os detalhes** (aço, bitola, perfil, acabamento da barra).

## Definição de ENGENHEIRADO (fechada)

- **Engenheirado = `ABCTIP_PRO = 2`.** Item de texto livre sob desenho — ex.: *"SAE 4140H DESBASTADO CONFORME DES 100115"*, *"TIRANTE SAE 1045N"*, *"4130MOD DES. 10001209637 REV.00"*. **Sem** campos padrões (perfil/acabamento/bitola vazios); só o material de partida (`ABCMAT_DES`) traz o material.
- Confirma-se em três campos: `ABCTIP_PRO=2` = `ABCLIN_PRO='ESP'` = `ABCLIN_DES='Especial'`. ~29 itens / R$ 1,1 MM (2026 = 1,2% do faturamento).
- **Não existe código separado de "engenheirado" no RAF** além do tipo 2. O que foi chamado de "especial" **É** o engenheirado.
- **`Usinado` NÃO é engenheirado** — é um acabamento **normal** (item com campos padrões preenchidos, produzido a partir de uma barra). ~193 itens / R$ 2,9 MM (2026 = 3,1%).
- Engenheirado **não é separável no faturamento** por outro sinal. Na aba **Cotações** há `tipo_item` (catalogado/engenheirado) por regra de campos vazios — mas é conceito de **cotação** (antes da venda), não do faturamento.

## Acabamento (do produto faturado, `ABCACA_DES`)

Valores: Laminado, Forjado, **Usinado**, Trefilado, Descascado, Retificado. Vazio → engenheirado.

Referência 2026 (fat. c/ imp s/ IPI): Laminado 69,4% · Forjado 25,2% · Usinado 3,1% · **Engenheirado 1,2%** · Trefilado 0,9% · Descascado 0,2%.

## Colunas resultantes em `vw_faturamento`

`perfil`=ABCPER_DES · `acabamento`=ABCACA_DES · `produto`=ABCPRO_DES · `material_partida`=ABCMAT_DES · `tipo_os`=(ABCTIP_PRO=2→Engenheirado, senão Catalogado) · `bitola_mm`=Bitola_Padrao_mm · `dif_vermelha_pct`=gap vs Vermelho.

## Onde vive no portal

Aba **Produtos → Produto**: quebra por acabamento (Engenheirado como categoria), cortado × barra, resumo por família, explorador com filtro Catalogado × Engenheirado e drill mostrando produto faturado + material de partida.

Espelho técnico no repo: `~/dev/afs-lake/06_Docs/Dicionario_Dados_Produto_Faturamento.md`.
