---
tipo: processo-crítico
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [consolidação, os, agregação, dados]
---

# 08 — Consolidação por OS

## O problema

No RAF, um **mesmo item** (OS + ITE) pode ter **múltiplas linhas** devido a:
- **Liberações parciais** (entrega fracionada)
- **Revisões de faturamento**
- **Corrections fiscais**
- **Transferências entre unidades**

E **custos** (`ABCCUS_X`) podem estar **concentrados em uma única linha**, deixando as outras com valores zero ou parciais.

---

## Consequência se não consolidar

Análise linha-por-linha sem agregação gera **distorções graves**:

### Exemplo real
OS 332660, Item 02, com 3 linhas:
- Linha 1: Receita R$10.000, Custo aço R$7.000, Custo CTE R$300
- Linha 2: Receita R$15.000, Custo aço R$10.500, Custo CTE R$0
- Linha 3: Receita R$5.000, Custo aço R$0, Custo CTE R$0 (cancelamento parcial?)

Se eu calcular MC linha-por-linha:
- Linha 1: MC% = (10000 - 7000) / 10000 = 30%
- Linha 2: MC% = (15000 - 10500) / 15000 = 30%
- Linha 3: MC% = (5000 - 0) / 5000 = **100%** ← completamente irreal

**Consolidado:**
- Receita total: R$30.000
- Custo aço total: R$17.500
- MC real: (30000 - 17500) / 30000 = **41,7%**

Ou seja: média não ponderada de linhas → **53%** (errado). Consolidação → **41,7%** (certo).

---

## Regra

**Sempre agregar por `ABCOII_NUM + ABCOII_ITE` antes de calcular métricas unitárias.**

### Implementação Python

```python
def consolidar_por_os(df):
    # Agrupar por OS + Item
    grp = df.groupby(['ABCOII_NUM', 'ABCOII_ITE'])

    # Somar valores
    valores = grp.agg({
        'ABCTOT_LIQ': 'sum',
        'ABCCUS_ACO': 'sum',
        'ABCCUS_FIN': 'sum',
        'ABCCUS_FIN_COB': 'sum',
        'ABCCUS_CTE': 'sum',
        'ABCCUS_CTE_COB': 'sum',
        # ... demais custos cobrados e reais
        'ABCPES': 'sum',  # peso total
    }).reset_index()

    # Capturar dados descritivos da primeira linha (não somam)
    descritivos = grp.first()[
        ['ABCCLI_COD', 'ABCCLI_NOM', 'ABCCLI_CID', 'ABCFAACOD', 'ABCDT_FAT']
    ].reset_index()

    # Merge
    consolidado = valores.merge(descritivos, on=['ABCOII_NUM', 'ABCOII_ITE'])

    return consolidado
```

### Em Excel
Use `SUMIFS` e `AVERAGEIFS` agrupando por OS+Item.

---

## Regras específicas

### Somar
- Valores em R$ (receita, custos)
- Quantidades (peso, quantidade)
- Qualquer campo **aditivo**

### Não somar
- Datas (usar a mais recente ou primeira)
- Identificadores (OS, cliente)
- Campos descritivos (nome, família)

### Média ponderada
- Preço unitário: `Σ (preço × quantidade) / Σ quantidade`
- MC%: calcular **sobre o total consolidado**, não média de MC% por linha

### Casos especiais
- **Cancelamento parcial:** linha pode ter valor negativo. Somar mantém consistência.
- **Transferência entre unidades:** múltiplas linhas, somar mantém total correto.

---

## Quando NÃO consolidar

### Análise de eventos
Se analisa **número de faturamentos parciais** (ex: "quantas liberações parciais em média por OS?"), não consolidar — cada linha é um evento.

### Análise de datas
Se analisa **intervalo entre faturamentos de uma mesma OS**, precisa das datas individuais de cada linha.

### Análise de fluxo de caixa
Se analisa **quando cada faturamento aconteceu**, linha individual é o dado correto.

**Regra:** para métricas **financeiras por item** (MC, spread, valor), consolidar. Para métricas **de processo** (eventos, tempo), linha individual.

---

## Implementação no Motor Analítico

`motor/consolidacao.py::consolidar_os(df_raf)` já implementado com:
- Agregação correta
- Somas de valores numéricos
- Preserva identificação e datas
- Retorna dataframe consolidado

Todas as análises downstream consomem o **dataframe consolidado**, nunca o bruto.

---

## Validação

### Check 1 — Totais devem bater
Soma da receita antes e depois da consolidação deve ser idêntica:
```
total_antes = df['ABCTOT_LIQ'].sum()
total_depois = df_consolidado['ABCTOT_LIQ'].sum()
assert total_antes == total_depois
```

### Check 2 — Número de OS × Itens
```
n_linhas_antes = len(df)
n_os_item = df_consolidado[['ABCOII_NUM', 'ABCOII_ITE']].drop_duplicates().shape[0]

# n_linhas_antes deve ser >= n_os_item (cada OS+Item vira 1 linha consolidada)
assert n_os_item <= n_linhas_antes
```

### Check 3 — MC média ponderada
```
# MC ponderada antes da consolidação (pelas linhas)
mc_antes = (df['ABCPER_MAR'] × df['ABCTOT_LIQ']).sum() / df['ABCTOT_LIQ'].sum()

# MC recalculada após consolidação
mc_depois = df_consolidado['valor_mc'].sum() / df_consolidado['liquido_aco'].sum() × 100

# Devem ser próximos (pequena diferença aceitável por arredondamento)
```

---

## Armadilhas comuns

### 1. Não consolidar antes de calcular MC
Mais comum dos erros. Gera MC irrealista em outliers.

### 2. Consolidar mas esquecer de agregar custos também
Se agrega receita mas não custo, MC fica distorcida.

### 3. Usar média simples de MC% por linha
Matematicamente errado. Sempre use média ponderada ou recalcule sobre totais.

### 4. Consolidar campos não-aditivos
Somar dados descritivos (códigos, nomes) não faz sentido. Usar `first()` ou similar.

---

## Checklist de uso

Antes de usar qualquer número do RAF:

- [ ] Dataframe foi consolidado por `ABCOII_NUM + ABCOII_ITE`?
- [ ] Valores (receita, custos) somados?
- [ ] Dados descritivos preservados (não somados)?
- [ ] MC recalculada sobre totais, não média de MC%?
- [ ] Totais consolidados batem com totais brutos?

Se qualquer item falhar, **análise pode estar errada**.

---

## Conexões

- [[00 - Visão Geral RAF]]
- [[01 - Estrutura das 133 Colunas]]
- [[02 - Convenção Softcomp (Invertida)]]
- [[05 - Custo Real vs Cobrado]]
- [[01 Sistema de Dados/04 - Qualidade de Dados]]
- [[01 Sistema de Dados/06 - Motor Analítico v1]]
