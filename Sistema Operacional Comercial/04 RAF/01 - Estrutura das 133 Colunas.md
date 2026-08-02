---
tipo: referência-técnica
domínio: raf
criado: 2026-04-17
última-revisão: 2026-08-02
tags: [raf, colunas, estrutura, campos]
---

# 01 — Estrutura das 133 Colunas

> **Fonte primária (02/08/2026):** dicionário OFICIAL enviado pela Softcomp em
> **18/04/2026**, arquivado em `06_Docs/Dicionario_RAF_Softcomp_2026-04-18.xlsx`.
> Ele documenta as **133 colunas**, com significado e legenda dos códigos, mais
> dois exemplos reais da mesma nota (OI 332314/01) — que é o que revelou a
> semântica dos campos `ABCOII*` (ver abaixo). Antes disso, o entendimento das
> colunas era por dedução; agora há fonte.

## Visão geral

O export `DetalhesRAF.xlsx` do Softcomp tem **133 colunas**, todas documentadas.
Desta nota em diante: catálogo completo no fim, e as mais usadas por categoria.

**Cobertura de uso (medido em 02/08/2026):** o motor consome **89 de 133 (67%)**.
As 44 restantes existem, estão documentadas e **nunca foram tocadas** — foi
assim que `ABCOIICUS_ACO` ficou anos invisível até ser encontrado em 01/08.

**Atenção:** convenção de nomes de custo é **invertida** — ver [[02 - Convenção Softcomp (Invertida)]].

---

## Colunas de identificação

| Coluna | Significado |
|---|---|
| `ABCOII_NUM` | Número da OS (Ordem de Serviço) |
| `ABCOII_ITE` | Número do item na OS |
| `ABCFAACOD` | Família do produto **faturado** |
| `ABCOII_FAA` | Família da OS |
| `ABCMAT_FAA` | Família do **material de partida** (insumo) |
| `ABCCOR_*` | Corrida / lote de origem |

**Consolidação por OS:** sempre agregar por `ABCOII_NUM + ABCOII_ITE` antes de calcular métricas unitárias. Ver [[08 - Consolidação por OS]].

---

## ⚠️ Os campos `ABCOII*` são DO PEDIDO, não do faturamento

Descoberto em 01/08/2026 e confirmado pelo dicionário oficial em 02/08. O RAF
**importa** o custo do pedido e o guarda como campo próprio, ao lado do custo
apurado. São valores diferentes na mesma linha:

| Coluna | Dicionário Softcomp | O que é |
|---|---|---|
| `ABCOIITOT_LIQ` | "Total liq. do pedido" | valor líquido **do pedido** |
| `ABCOIICUS` | "Custo total no pedido" | custo total **de referência** |
| `ABCOIICUS_ACO` | "Custo do aço do pedido" | custo do aço **de referência** |
| `ABCCUS_ACO` | "Custo Aço" | custo do aço **apurado** (real) |
| `ABCPES_ACO` | "Peso **baixado**" | peso que saiu do estoque (≠ peso faturado) |

Provas medidas: os dois campos diferem em **99,9%** das linhas de 2026 (se fossem
o mesmo, o drift seria zero), e `ABCOIICUS_ACO` bate com o `CustoMP` da
`BI.Pedido` em **100%** das 36.798 linhas casadas.

### 🪤 A armadilha: o custo de referência é do pedido INTEIRO

Quando o pedido é faturado em **várias notas**, o campo `ABCOII*` **repete o
valor cheio em cada nota**, enquanto o custo real é o da parcela:

```
NF 316604  ped 338273 │ REAL  72.024 │ REF 215.755
NF 317153  ped 338273 │ REAL 105.266 │ REF 215.755   ← repetido
```

Confirmado nos dois exemplos do próprio dicionário e medido no lake: dos 1.814
itens faturados em várias notas, **100%** repetem o custo de referência.

**Consequência:** somar as duas colunas sem tratar isso infla o drift de
**−13,9% para −36,9%**. Normalizar por peso, ou restringir a itens de nota
única (94% dos casos). Este erro já foi cometido — ver
[[2026-08-02 — Dicionário do RAF e a semântica dos campos do pedido]].

### Custo real nasce zerado

No 1º exemplo do dicionário o custo apurado é **0** e o peso baixado é **0**; no
2º, preenchidos. O custo real é apurado DEPOIS da emissão. **Não nos afeta**:
100% das linhas de 2026 chegam apuradas, porque o export é feito depois.
Campo relacionado: `ABCPFAPESFAT` — "Apura o custo da MP pelo peso faturado:
1-Sim / 2-Não" (na prática 99,95% = 2).

---

## Colunas de cliente

| Coluna | Significado |
|---|---|
| `ABCCLI_COD` | Código do cliente |
| `ABCCLI_NOM` | Nome/razão social |
| `ABCCLI_CID` | Cidade (⚠ truncada em 20 chars) |
| `ABCCLI_UF` | UF |
| `ABCCLI_TIP` | Tipo de tabela (A/B/C) |
| `ABCCLI_VND` | Vendedor responsável |

**Atenção cidade:** aplicar override (ver [[Sistema Operacional Comercial/01 Sistema de Dados/04 - Qualidade de Dados]]).

---

## Colunas de produto / material

| Coluna | Significado |
|---|---|
| `ABCMAT_*` | Material de partida (insumo) |
| `ABCFAACOD` | Família produto faturado |
| `ABCDIA` | Diâmetro (bitola) |
| `ABCCOMP` | Comprimento |
| `ABCPES` | Peso |
| `ABCQTD` | Quantidade |
| `ABCACB` | Acabamento |

---

## Colunas de preço / receita

| Coluna | Significado |
|---|---|
| `ABCTOT_LIQ` | Valor total líquido (receita líquida) |
| `ABCPRE_VDA` | Preço de venda unitário |
| `ABCPRE_KG` | **Custo do aço** em R$/tonelada (NÃO é preço de venda) |
| `ABCPRE_MIN_A` | Piso Tab Verde (R$/kg) |
| `ABCPRE_MIN_B` | Piso Tab Amarela (R$/kg) |
| `ABCPRE_MIN_C` | Piso Tab Vermelha (R$/kg) |

---

## Colunas de custo (convenção invertida! ⚠)

**Padrão:** `ABCCUS_<CODIGO>` = **COBRADO** do cliente; `ABCCUS_<CODIGO>_COB` = **REAL** pago pela AFS.

| Base | Cobrado | Real | Significa |
|---|---|---|---|
| ACO | `ABCCUS_ACO` | `ABCCUS_ACO_COB` | Aço (custo = cobrado, estrutural) |
| FIN | `ABCCUS_FIN` | `ABCCUS_FIN_COB` | Financeiro (CF% cobrado vs Selic real) |
| IMP | `ABCCUS_IMP` | `ABCCUS_IMP_COB` | Impostos (base cheia vs correta) |
| COM | `ABCCUS_COM` | `ABCCUS_COM_COB` | Comissão (cobrado vs pago) |
| CML | `ABCCUS_CML` | `ABCCUS_CML_COB` | Comercial+Logística (só custo) |
| INT | `ABCCUS_INT` | `ABCCUS_INT_COB` | Interno (cobrado vs real) |
| CER | `ABCCUS_CER` | `ABCCUS_CER_COB` | Certificação (cobrado vs real) |
| EXT | `ABCCUS_EXT` | `ABCCUS_EXT_COB` | Externo (TT) (cobrado vs real) |
| CTE | `ABCCUS_CTE` | `ABCCUS_CTE_COB` | Corte (absorvido pela AFS) |

**Ver [[04 - Margem Oculta (7 componentes)]]** para detalhes de cada spread.

### Campo consolidado ABCCUS
`ABCCUS` (sem sufixo de categoria) = **soma de despesas cobradas**.

---

## Colunas de MC

| Coluna | Significado |
|---|---|
| `ABCPER_MAR` | **MC% pós-faturamento** (contábil, não econômica) |
| `ABCVAL_MAR` | Valor de MC em R$ |

**Importante:** é MC **realizada**, não estimada do pedido.

---

## Colunas fiscais

| Coluna | Significado |
|---|---|
| `ABCTOT_BRU` | Valor bruto (com IPI) |
| `ABCVAL_IPI` | IPI |
| `ABCVAL_ICM` | ICMS |
| `ABCVAL_PIS` | PIS |
| `ABCVAL_COF` | COFINS |
| `ABCICM_ST` | ICMS ST |

---

## Colunas de data

| Coluna | Significado |
|---|---|
| `ABCDT_FAT` | Data de faturamento |
| `ABCDT_PED` | Data do pedido |
| `ABCDT_COT` | Data da cotação |
| `ABCDT_ENT` | Data de entrega |

---

## Colunas de processo

| Coluna | Significado |
|---|---|
| `ABCFASES` | Fases de processamento |
| `ABCCOR_*` | Certificação da corrida |

---

## Fórmulas derivadas (calculadas a partir das colunas)

### Líquido do aço
```
LiquidoAco = ABCTOT_LIQ - ABCCUS
           = receita líquida - despesas embutidas
```

### Valor de MC
```
ValorMC = LiquidoAco - ABCCUS_ACO
        = receita líquida - despesas - custo aço
```

### MC%
```
MC% = ValorMC / LiquidoAco × 100
    = campo ABCPER_MAR
```

### Margem oculta por componente
```
margem_oculta_X = ABCCUS_X - ABCCUS_X_COB
                = cobrado    - real
```

### MC econômica
```
MC_econômica$ = MC_contábil$ + Σ margens_ocultas_positivas
MC_econômica% = MC_econômica$ / LiquidoAco × 100
```

---

## Categorização por volume

### Colunas críticas (top 30 usadas)
As colunas listadas acima cobrem >90% das análises comerciais. Motor Analítico v1 usa esse subset.

### Colunas secundárias (próximas 50)
Detalhes fiscais, processos específicos, certificações. Usar quando necessário.

### Colunas raras (últimas 50)
Campos com uso pontual, às vezes vazios, às vezes específicos de módulos não críticos.

---

## Volume e tamanho esperado

| Período | Linhas esperadas | Faturamento |
|---|---|---|
| 1 mês | ~5.000 | ~R$16M |
| 1 trimestre | ~15.000 | ~R$50M |
| 1 ano | ~60.000 | ~R$200M |

Arquivo Excel resultante: ~10-30 MB dependendo do período.

---

## Atenção à qualidade do dado

### Checklist antes de usar
- [ ] Período filtrado está correto?
- [ ] Número de linhas faz sentido (5k/mês)?
- [ ] Coluna `ABCOII_NUM` preenchida em todas as linhas?
- [ ] Consolidação por OS aplicada?
- [ ] Cidades passadas por override?
- [ ] Custos interpretados com convenção correta (COB = real)?

Se falhar em qualquer item, **corrigir antes** de concluir análise.

---

## Conexões

- [[00 - Visão Geral RAF]]
- [[02 - Convenção Softcomp (Invertida)]]
- [[03 - MC Contábil vs Econômica]]
- [[04 - Margem Oculta (7 componentes)]]
- [[05 - Custo Real vs Cobrado]]
- [[08 - Consolidação por OS]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/04 - Qualidade de Dados]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]


---

## Catálogo completo — as 133 colunas

Gerado do dicionário oficial da Softcomp (18/04/2026) cruzado com o código do
motor em 02/08/2026. "Motor usa?" = a coluna aparece em algum `.py` do
MotorAnalitico.

### OS/OI, pedido e OC

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 56 | `ABCOII_NUM` | Nº da OI | ✅ |
| 57 | `ABCOII_ITE` | Item da OI | ✅ |
| 58 | `ABCOII_PRA` | Prazo da OI | — |
| 66 | `ABCOIIPVO` | Preço unitário | ✅ |
| 67 | `ABCOIIUNQ` | Unidade medida Qtd: 1-KG / 2-TN / 3-MM / 4-PC / 5-BR / 6-M / 7-CM / 8-UM | — |
| 68 | `ABCOIIUNP` | Unidade medida de preço: 1-KG / 2-TN / 3-PC / 4-M / 5-M2 / 6-UM | — |
| 103 | `ABCOIITOT_LIQ` | Total liq. do pedido | — |
| 104 | `ABCOIICUS` | Custo total no pedido | — |
| 105 | `ABCOIICUS_ACO` | Custo do aço do pedido | — |
| 106 | `ABCOIINUM_OC` | Nº da OC | — |
| 107 | `ABCOIIITE_OC` | Item da OC | — |
| 108 | `ABCOCIPRAZO` | Prazo da OC | — |
| 109 | `ABCOCIENTREGA` | Data da entrega OC | — |
| 112 | `ABCOCCFOR` | Cod. Fornecedor da OC | — |
| 113 | `ABCOIIQUA` | Nivel da qualidade | — |
| 127 | `ABCOII_FAA` | Familia do produto | ✅ |

### Custos

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 55 | `ABCPFAPESFAT` | Apura o custo da MP pelo peso faturado: 1-Sim / 2-Não | — |
| 75 | `ABCCUS` | Total Custo | ✅ |
| 76 | `ABCCUS_ACO` | Custo Aço | ✅ |
| 77 | `ABCCUS_FIN` | Custo financeiro | ✅ |
| 78 | `ABCCUS_IMP` | Custo Impostos | ✅ |
| 79 | `ABCCUS_COM` | Custo c/ representação | ✅ |
| 80 | `ABCCUS_CML` | Custo comercial | ✅ |
| 81 | `ABCCUS_INT` | Custo industrial | ✅ |
| 82 | `ABCCUS_CER` | Custos c/ Certificação | ✅ |
| 83 | `ABCCUS_EXT` | Custo Externo | ✅ |
| 84 | `ABCCUS_CTE` | Custo do corte | ✅ |
| 85 | `ABCCUS_COB` | Custo cobrado do cliente | — |
| 86 | `ABCCUS_ACO_COB` | Custo aço cobr. cliente | ✅ |
| 87 | `ABCCUS_FIN_COB` | Custo financeiro cobr. do cliente | ✅ |
| 88 | `ABCCUS_IMP_COB` | Custos impostos cobrado cliente | ✅ |
| 89 | `ABCCUS_COM_COB` | Custor representação cobr. Cliente | ✅ |
| 90 | `ABCCUS_CML_COB` | Custo comercial cobr. Cliente | ✅ |
| 91 | `ABCCUS_INT_COB` | Custo industrial cobr. Cliente | ✅ |
| 92 | `ABCCUS_CER_COB` | Custos certificação cobr. Cliente | ✅ |
| 93 | `ABCCUS_EXT_COB` | Custos externos cobr. Cliente | ✅ |
| 94 | `ABCCUS_CTE_COB` | Custo corte cobr. Cliente | ✅ |
| 131 | `ValorCusto` | Vlr Custo | ✅ |

### Preço, peso e margem

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 42 | `ABCTOT` | Valor total do item | ✅ |
| 43 | `ABCNOR` | Valor venda normal | ✅ |
| 44 | `ABCESP` | Valor venda especial | — |
| 49 | `ABCQTD` | Peso | ✅ |
| 50 | `ABCPCS` | Peças | ✅ |
| 71 | `ABCCPGMED` | Qtd media dias cond.pgto | ✅ |
| 72 | `ABCPES_CTE` | Peso corte | ✅ |
| 73 | `ABCPES_ACO` | Peso baixado | ✅ |
| 74 | `ABCTOT_LIQ` | Valor total liquido | ✅ |
| 95 | `ABCPER_MAR` | % margem contribuição | — |
| 96 | `ABCPRE_KG` | Preço por KG | ✅ |
| 97 | `ABCPRE_MIN_A` | Preço min. A | ✅ |
| 98 | `ABCPRE_MIN_B` | Preço min. B | ✅ |
| 99 | `ABCPRE_MIN_C` | Preço min. C | ✅ |
| 130 | `ValorLIQ` | Valor liq. Do item | ✅ |
| 133 | `ValorMC` | Vlr Margem contribuição | ✅ |

### Produto

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 25 | `ABCPRO_DES` | Descrição do produto | ✅ |
| 26 | `ABCTIP_PRO` | cod. Tipo de produto | ✅ |
| 27 | `ABCLIN_PRO` | Cod. Linha de produto | ✅ |
| 28 | `ABCLIN_DES` | Descrição linha de produto | ✅ |
| 29 | `ABCLIN_RED` | Nome reduzido linha de produto | — |
| 30 | `ABCTIP` | Tipo de material | ✅ |
| 31 | `ABCPER` | Perfil do material | ✅ |
| 32 | `ABCPER_DES` | Descrição do perfil do material | ✅ |
| 33 | `ABCPER_RED` | Nome reduzido perfil do material | ✅ |
| 34 | `ABCACA` | Cod. do acabamento | ✅ |
| 35 | `ABCACA_DES` | Descrição do acabamento | ✅ |
| 36 | `ABCACA_RED` | Nome reduzido do acabamento | ✅ |
| 37 | `ABCBIT` | Bitola do material | ✅ |
| 38 | `ABCLAR` | Largura | — |
| 39 | `ABCTER` | 3ª  medida | — |
| 40 | `ABCCOM` | Comprimento | ✅ |
| 62 | `ABCFAM` | Descrição da Famila | ✅ |
| 63 | `ABCFAACOD` | Cod. Familia | ✅ |

### Material de partida (MP)

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 114 | `ABCMAT_TIP` | Tipo MP | ✅ |
| 115 | `ABCMAT_DES` | Descrição MP | ✅ |
| 116 | `ABCMAT_LIN` | Linha da MP | — |
| 117 | `ABCMAT_LIN_DES` | Descrição da linha | — |
| 118 | `ABCMAT_TIP_PRO` | Tipo prod. MP | ✅ |
| 119 | `ABCMAT_PER` | Perfil da MP | ✅ |
| 120 | `ABCMAT_PER_DES` | Descrição do perfil MP | ✅ |
| 121 | `ABCMAT_ACA` | Acabamento MP | ✅ |
| 122 | `ABCMAT_ACA_DES` | Descr. Acabamento | ✅ |
| 123 | `ABCMAT_BIT` | Bitola MP | ✅ |
| 124 | `ABCMAT_LAR` | Largura MP | — |
| 125 | `ABCMAT_TER` | 3º medida MP | — |
| 126 | `ABCMAT_COM` | Comprimento MP | ✅ |
| 128 | `ABCMAT_FAA` | Fam. MP | ✅ |

### Fiscal e nota

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 2 | `ABCNNF_CI` | Nº do CI da NF | — |
| 3 | `ABCNNF_ITE` | Item da NF | ✅ |
| 4 | `ABCNNF_NUM` | Nº da NF | ✅ |
| 5 | `ABCDAT` | Emissão da NF | ✅ |
| 17 | `ABCCLA` | Cod.Classif. Fiscal | ✅ |
| 18 | `ABCNCM` | NCM do produto | — |
| 41 | `ABCCPL_1` | Inf. Complem. do item | — |
| 45 | `ABCICM` | Valor do Icms | ✅ |
| 46 | `ABCIPI` | Valor do Ipi | ✅ |
| 47 | `ABCPIS` | Valor do Pis | ✅ |
| 48 | `ABCCOFINS` | Valor do Cofins | ✅ |
| 51 | `ABCALI` | Aliq. Icms | ✅ |
| 53 | `ABCPFA` | cod. tipo de NF | ✅ |
| 54 | `ABCPFA_DES` | Descrição do tipo de NF | ✅ |

### Cliente e geografia

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 7 | `ABCCLI` | Cod. Cliente | ✅ |
| 8 | `ABCCLICGC` | CNPJ do cliente | — |
| 9 | `ABCCLIRAZ` | Razão Social do Cliente | ✅ |
| 10 | `ABCCLIRED` | Nome reduzido Cliente | ✅ |
| 11 | `ABCCLIREG` | Cod. Região | — |
| 12 | `ABCCLIREG_DES` | Nome da Região | — |
| 13 | `ABCCLICEP` | CEP cliente | — |
| 14 | `ABCCLICIT` | Cidade Cliente | ✅ |
| 15 | `ABCCLIEST` | UF cliente | ✅ |
| 16 | `ABCCLIEST_DES` | Nome do Estado Cliente | — |
| 52 | `ABCEST` | UF na NF | — |
| 59 | `ABCCLITIP` | Tipo de pessoa(Cliente) 0-Juridica 1-Fisica / 2-Isento / 3-Outros | — |

### Organização

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 1 | `ABCFILIAL` | cod. Empresa / Filial | ✅ |
| 6 | `ABCEMPRED` | Nome reduzido da Empresa/Filial | ✅ |
| 19 | `ABCGER` | Cod. do gerente | ✅ |
| 20 | `ABCGER_NOM` | Nome do gerente | ✅ |
| 21 | `ABCVEN` | Cod. do vendedor | ✅ |
| 22 | `ABCVEN_NOM` | Nome do vendedor | ✅ |
| 23 | `ABCDIG` | cod.Emitente pedido | — |
| 24 | `ABCDIG_NOM` | Nome do emitente pedido | — |
| 110 | `ABC_CD_EQV` | Cod. Da equipe | — |
| 111 | `ABC_EQV_RED` | Nome reduzido equipe | — |

### Outros

| # | Coluna | Significado (dicionário Softcomp) | Motor usa? |
|---|---|---|---|
| 60 | `ABCCLIDOC` | Não utlizado | — |
| 61 | `ABCATUALIZACAO` | Dta atualiz. Estoque | — |
| 64 | `ABCSETPCOD` | Cod. Setor produção | ✅ |
| 65 | `ABCSETPDES` | Descrição Setor produção | — |
| 69 | `ABCCPG` | Cod. Cond. Pgto | ✅ |
| 70 | `ABCCPGDES` | Descrição condição pagamento | — |
| 100 | `ABCDAT_EXP` | Data expedição | — |
| 101 | `ABCTRA` | Cod. Transportadora | — |
| 102 | `ABCTRA_PROPRIO` | Transp. Retira: 1-Sim / 0-Não | — |
| 129 | `ValorTotal` | Vlr total do Item | ✅ |
| 132 | `LiquidoAco` | Vlr total liq. Do aço | ✅ |

### Não usadas com dado — o que vale investigar

Preenchimento medido no RAF 2026 (38.471 linhas):

| Coluna | O que é | Preenchida |
|---|---|---|
| `ABCSETPDES` | Setor de produção | **100%** |
| `ABCOIIQUA` | Nível da qualidade | **99,3%** |
| `ABCOII_PRA` | Prazo da OI | **99,7%** |
| `ABCTRA` | Transportadora | **96,2%** |
| `ABCTRA_PROPRIO` | Cliente retira (1-Sim/0-Não) | 58,2% |
| `ABCCPL_1` | Informação complementar do item | 56,1% |

⚠️ **A família da OC está praticamente vazia** — `ABCOIINUM_OC`, `ABCOCCFOR`
(fornecedor), `ABCOCIENTREGA`: **0,2%**. O agente analítico registra "sem fonte
de OC" como lacuna; a coluna existe, mas o campo **não é preenchido no ERP**.
É lacuna de processo, não de dado. `ABCCUS_COB` (custo cobrado total) está 0%,
embora os componentes `_COB` sejam usados.

**`ABCSETPDES` (setor de produção) resolve uma pendência aberta com o Nelson** —
foi pedido como coluna nova na `BI.Pedido` e já existe no RAF, com 100%.
