---
tipo: referência-técnica
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [raf, colunas, estrutura, campos]
---

# 01 — Estrutura das 133 Colunas

## Visão geral

O export `DetalhesRAF.xlsx` do Softcomp tem **133 colunas**. Esta nota cataloga as **mais usadas** para análise, agrupadas por categoria.

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
