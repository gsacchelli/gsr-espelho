---
tipo: regra-canônica
domínio: estoque
criado: 2026-08-03
última-revisão: 2026-08-03
tags: [estoque, origem, nacional, importado, fornecedor, lead-time, arcelor, daye]
---

# 07 — Origem do Material (Nacional × Importado)

## Propósito

Classifica a origem do **material de partida** (matéria-prima estocada) → **Nacional** ou **Importado**, com fornecedor e lead time. É o que decide a régua de saúde do estoque: importado com 8 meses de cobertura é estoque **estratégico**; nacional com 8 meses é **problema**.

**Fonte única no código:** `MotorAnalitico/raf/origem.py::classificar_origem`. Consumida por `raf/enriquecer.py` (linha do RAF) e `raf/painel_aggregator.py` (linha do EstoquePadrao).

**O painel não tem cópia da regra.** O Painel de Estoque roda em `file://` e exporta HTML autocontido, então não pode carregar a regra de um arquivo externo. Em vez de manter uma segunda implementação em JS — que foi o que divergiu e causou o erro de 03/08 — o bloco JS é **projetado do Python** por `MotorAnalitico/geradores/gerar_origem_js.py` e injetado no template entre marcadores `AUTO-GERADO`. Editar esse bloco à mão é erro; o `make ci` reprova se o painel sair de sincronia (`--conferir` + `geradores/test_origem_js.py`, que executa Python e JS lado a lado sobre a mesma grade e sobre os SKUs reais). Ver [[04 - Painel de Estoque v2]].

Mudou a regra? Muda o Python e roda:

```bash
python3 MotorAnalitico/geradores/gerar_origem_js.py
```

> **Por que esta nota existe.** Até 03/08/2026 a regra vivia só no log datado `Logs/2026-04-30 — Reestruturação Painel Comercial RAF`. Quando a política de compra mudou em jun/2026, não havia documento vivo para atualizar — e o erro sobreviveu dois meses em tela. Regra de negócio que o código lê mora aqui, não num log.

---

## Tabela oficial (vigente desde jun/2026, corrigida 03/08/2026)

| Perfil + Acabamento | Aço | Faixa de bitola | Origem | Fornecedor | Regulador |
|---|---|---|---|---|---|
| Redondo Forjado | qualquer | qualquer | **Nacional** | Villares/Metals | 5 meses |
| Redondo Laminado | 10XX (carbono) | ≤ 101,60 mm | **Nacional** | Simec/Arcelor | 3 meses |
| Redondo Laminado | **4140** | **≤ 88,90 mm** | **Nacional** | **Arcelor** (dupla fonte) | **5 meses** |
| Redondo Laminado | **20MnCr5** | **≤ 101,60 mm** | **Nacional** | **Arcelor** (dupla fonte) | **5 meses** |
| Redondo Laminado | 4320 / 4340 / 8620 / 8640 / **17CrNiMo6** | qualquer | **Importado** | Daye/HBIS | 8 meses |
| Redondo Laminado | 10XX / 4140 / 20MnCr5 | acima do teto acima | **Importado** | Daye/HBIS | 8 meses |
| Redondo Trefilado | qualquer | qualquer | **Nacional** | **Arcelor** | 4 meses |
| Catch-all (perfil não-redondo, inox, 6150, ST52.3, 8630…) | — | — | Não mapeado | — | — |

---

## As duas linhas que mudaram (03/08/2026)

**4140 e 20MnCr5 laminados na faixa fina têm DUPLA FONTE** — Arcelor (nacional) **ou** Daye/HBIS — e na prática a compra recente é **Arcelor**. O **custo carregado na família de produto é o da Arcelor**. Por isso a origem canônica destes dois, nessa faixa, passou a ser Nacional.

Até então a regra classificava **toda** liga laminada como importada Daye/HBIS. Efeito medido no RAF 2026: **5.297 linhas / R$ 13,19 MM de líquido** classificadas como importadas quando são nacionais — 13,3% das linhas do ano.

Isso não é rótulo cosmético: material nacional lido como importado ganha uma régua de saúde que **tolera 12 meses de cobertura** em vez de 5. Estoque que deveria acender alerta aparecia como posição estratégica.

**O teto por aço vem do estoque regulador do ERP**, que foi ajustado de 8 → 5 meses exatamente nessas faixas em jun/2026 (junto com o lote de compra, 10.000 → 5.000 kg). Conferido no `EstoquePadrao` de 03/08/2026:

- **4140 laminado:** regulador 5 de 19,05 a 88,90 mm · regulador 8 de 95,25 mm para cima
- **20MnCr5 laminado:** regulador 5 de 15,88 a 101,60 mm · regulador 8 de 107,95 mm para cima

⚠ **Os tetos são diferentes entre os dois aços** (88,90 vs 101,60). Não unificar sem conferir o regulador no ERP.

**Sem consequência de preço.** O custo é mantido igual entre a família nacional e a importada do mesmo produto, **líquido de impostos** (havendo dupla fonte, vale o custo mais alto para as duas). A origem muda o **bruto** ofertado — porque muda a carga de ICMS — mas **não o líquido**. Trocar de fonte não desloca margem nem exige repasse. Ver [[02 - Fórmula de Preço Sacchelli]].

---

## Armadilha: o estoque regulador NÃO identifica a origem sozinho

**Regulador 5 cobre duas origens diferentes** — Villares/Metals (forjado nacional) e Arcelor (4140/20MnCr5 laminado nacional). Foi exatamente essa ambiguidade que quebrou o Plano 30d do Painel de Estoque: o painel inferia a origem só do regulador, com um mapa `{5: 'Villares (forjado)'}`, e rotulava **todo 4140 e 20MnCr5 laminado fino como forjado**.

Para identificar origem são necessários **acabamento + aço + bitola**. O regulador é consequência da origem, não substituto dela.

---

## A origem lê o aço PADRONIZADO, não a grafia do ERP (03/08/2026)

O Softcomp escreve o mesmo aço de várias formas. Até 03/08 a regra de origem mantinha uma **lista própria de grafias** e comparava por igualdade exata — então toda variante caía em "Não mapeado", em silêncio, porque "Não mapeado" não levanta erro.

O caso que revelou: o ERP grafa **sempre** `D17-18CrNiMo7-6`, nunca `18CrNiMo7-6` puro — que era o que a lista tinha. **255 das 403 linhas "Não mapeado" do RAF 2026 (63%, R$ 1,14 MM de líquido)** eram esse único aço, todas laminadas. As forjadas vinham corretas porque a regra do forjado casa por perfil + acabamento sem olhar o aço — **foi isso que mascarou a lacuna**. Confirmado pelo Gustavo: é o mesmo aço, só grafia diferente.

**A correção não foi acrescentar a grafia à lista — foi passar a usar a régua canônica.** A padronização de aço do `criterios_raf.xlsx` (`CriteriosRAF.aco_padrao_por`), a mesma que indexa a família canônica, já resolvia tudo isso:

| Grafias do ERP | Aço padronizado |
|---|---|
| `D17-18CrNiMo7-6` · `18CrNiMo7-6` · `18CrNiMo6-7` · `18CrNiMo7` · `18CrNiMo6` | **17CrNiMo6** |
| `42CrMo4` · `42CrMoS4` · `41CrS4` · `4140H` · `4140 H` · `414` | **4140** |
| `20MnCr4` · `20MnCrS5` · `25MoCr4` · `25MoCrS4` · `25CrMoS4` | **20MnCr5** |
| `4320H` · `4340H` · `8620H` · `8640H` | 4320 / 4340 / 8620 / 8640 |

A lista de aços de liga da regra de origem passou a guardar **7 aços padronizados** — `4140, 4320, 4340, 8620, 8640, 20MnCr5, 17CrNiMo6` — em vez de grafias soltas. Aço novo se cadastra no `criterios_raf`, não na regra de origem. Duas entradas mortas saíram junto (`17CrNiMo7`, que nem existe no cadastro, e `18CrNiMo7-6` sem prefixo).

`D17-` é **nomenclatura interna da casa: D = DIN, 17 = 17CrNiMo6** (confirmado pelo Gustavo, 03/08/2026) — não é aço distinto.

---

## Régua de saúde por origem

Cobertura relativa ao lead time da origem — não tempo absoluto em estoque. Em distribuidor com lead time longo, **estoque é parte do produto ofertado**.

| Categoria | Saudável | Atenção | Risco |
|---|---|---|---|
| Nacional laminado carbono (regulador 3m) | até 3 meses | 3–6 meses | > 6 meses |
| Nacional trefilado Arcelor (regulador 4m) | até 4 meses | 4–8 meses | > 8 meses |
| Nacional forjado / liga Arcelor (regulador 5m) | até 5 meses | 5–10 meses | > 10 meses |
| **Importado (regulador 8m)** | **até 12 meses** | **12–18 meses** | **> 18 meses** |

---

## Três SKUs onde o cadastro do ERP se contradiz

O par **(estoque regulador, lote de compra)** anda junto: a mudança de jun/2026 baixou os dois ao mesmo tempo (regulador 8→5, lote 10.000→5.000 kg). Nos blocos consistentes, os dois campos concordam. **Três SKUs quebram o par** — cada um com um campo de cada lado:

| SKU | Regulador | Lote | Bloco a que pertence | Cobertura |
|---|---|---|---|---|
| `4140 laminado 15,88 mm` | **8** (importado) | 5.000 (nacional) | os outros 22 da faixa fina são reg 5 | 8,6 meses |
| `20MnCr5 laminado 12,70 mm` | **8** (importado) | 5.000 (nacional) | os outros 23 da faixa fina são reg 5 | **71,5 meses** |
| `4140 laminado 165,10 mm` | **5** (nacional) | 10.000 (importado) | os outros 25 acima do teto são reg 8 | 8,7 meses |

**Hipóteses distintas para os dois grupos:**

- **15,88 e 12,70 mm** são as bitolas **mais finas** de cada aço, e ambas ficaram com lote de nacional e regulador de importado. Parece cadastro que não acompanhou a virada de jun/2026. Mas há uma alternativa que muda a regra: **se a Arcelor não lamina essas bitolas finas**, elas são importadas de fato — e aí a faixa nacional tem **piso**, não só teto. ⚠ Confirmar com a Arcelor.
- **165,10 mm** é o lote alocado à **Uniforja** (300 t, registrado em `ALOCADO` no painel). Regulador 5 num material importado pode ser **deliberado**: contrato firme justifica carregar menos estoque. Provavelmente intencional.

Efeito prático hoje: a regra classifica pela **bitola**, então 15,88 e 12,70 saem como Arcelor nacional (régua apertada) e 165,10 sai como importado — mas o painel usa o **regulador do ERP** para a cobertura-alvo, que discorda nos três. O 20MnCr5 de 12,70 mm merece atenção por si só: **4.379 kg parados contra 735 kg/ano de saída**.

---

## Pendências abertas (03/08/2026)

1. **Confirmar com a Arcelor** se ela lamina 4140 15,88 mm e 20MnCr5 12,70 mm — decide se a faixa nacional ganha piso de bitola ou se são dois cadastros a corrigir no ERP.
2. **Reprocessar o RAF** para propagar ao lake (`Origem_Partida` → silver → gold → portal).

---

## Relacionadas

- [[00 - Visão Geral Estoque]] — princípios do domínio
- [[04 - Painel de Estoque v2]] — onde a regra aparece em tela
- [[01 - Família Canônica]] — taxonomia que a origem acompanha
- [[02 - Fórmula de Preço Sacchelli]] — por que a origem não desloca o líquido
