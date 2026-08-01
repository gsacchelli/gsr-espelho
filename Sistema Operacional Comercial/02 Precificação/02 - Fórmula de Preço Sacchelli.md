---
tipo: fórmula-técnica
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [fórmula, preço, pricing, matemática]
---

# 02 — Fórmula de Preço Sacchelli

## Enunciado geral

**Preço = Custo Aço + Corte + MC sobre aço + Serviços com margem + Despesas variáveis (inclui spread financeiro)**

Essa fórmula reflete a **lógica real de pricing** da AFS, considerando:
1. O custo-base do material (aço)
2. Os serviços de processamento (corte e outros)
3. A margem alvo sobre o aço
4. Os serviços adicionais (tratamento, ensaio, certificação — com margem embutida)
5. As despesas variáveis (comissão, impostos, logística, spread financeiro)

---

## Fórmula expandida

```
Preço_unitário = Σ componentes

Onde:

Custo Aço        = peso × custo_aço_ton × (1 + VPP)     [quando aplicável]
Corte            = custo_corte_fixo + variável_por_kg
MC aço           = Custo Aço × MC%_alvo_sobre_aço
Serviços margem  = custo_TT × (1 + margem_TT)          [mesmo padrão para ensaio, certif]
Despesas var     = (Preço_bruto) × %_despesas_variáveis
Spread fin       = diferença entre CF% cobrado e Selic real (margem oculta)
```

**Preço_final** é calibrado para que, após aplicar impostos sobre a base, o líquido alvo seja atingido.

---

## Detalhamento dos componentes

### 1. Custo do aço
**Variável base**. Pode vir de:
- Preço FOB China + frete + AFRMM + impostos (importação)
- Preço negociado com usina nacional (Gerdau, Villares, etc.)
- Custo ponderado do estoque (mistura de lotes)

**Campo RAF:** `ABCPRE_KG` (custo do aço em R$/tonelada — **não é preço de venda**).

**VPP aplicado ou não?** Depende do modo de venda (ver [[05 - Modos de Venda]]):
- R$/kg: **sem** VPP no custo (cliente paga peso real)
- R$/pç: **com** VPP (AFS absorveria a diferença se não incluir)
- R$/m: **com** VPP (peso extra por VPP não é recuperado)

### 2. Corte
Processo de transformação barra → peça dimensionada.

**Custo real:** computado por operação (tempo-máquina + energia + desgaste)
**Custo cobrado (no pricing):** pode ser zero ou embutido — depende da política.

**Atenção:** no RAF, ABCCUS_CTE **registrado é o cobrado**, mas `ABCCUS_CTE_COB = 0` frequentemente. Significa: corte é **custo absorvido** pela AFS (não cobrado separadamente), mas aparece como "cobrado" no sistema devido à convenção invertida.

**Implicação:** corte hoje é **despesa absorvida**, não serviço cobrado. Isso **contradiz** a lógica de servitização. Se MetalM (ou AFS evolutiva) for servitizar, corte precisa virar linha explícita de preço.

### 3. MC sobre aço
Margem alvo aplicada sobre o custo do aço.

**MC% alvo** varia por:
- Família de produto (aços especiais têm MC maior)
- Tipo de cliente (tabela A/B/C)
- Política comercial da unidade

**Campo RAF:** `ABCPER_MAR` (MC% realizada pós-faturamento).

### 4. Serviços com margem (TT, ensaio, certificação)
Serviços externos ou internos com margem **embutida no preço**.

**Padrão de cobrança:**
- Tratamento térmico (TT): custo terceiro × (1 + margem AFS)
- Ensaios (dureza, metalografia): custo terceiro × margem
- Certificações: valor cheio cobrado, custo interno baixo ou zero

**Campos RAF:**
- `ABCCUS_EXT` (cobrado) e `ABCCUS_EXT_COB` (real) → TT
- `ABCCUS_CER` (cobrado) e `ABCCUS_CER_COB` (real) → certificação
- `ABCCUS_INT` (cobrado) e `ABCCUS_INT_COB` (real) → interno

**Spreads típicos (abr/2026):**
- CER: cobrado R$23k, real ~0 → margem oculta quase 100%
- INT: cobrado R$19k, real ~0 → margem oculta quase 100%
- EXT: cobrado R$466k, real menor → margem oculta relevante

### 5. Despesas variáveis

**Despesas comerciais (fixo):** 3,70%

**Despesas logísticas (variável por unidade):**

| Unidade | % |
|---|---|
| Guarulhos (GRU) | 1,54% |
| Piracicaba (PIR) | 1,64% |
| São Carlos (SCA) | 3,24% |
| Rio Preto (RIP) | 2,76% |
| **Caxias do Sul (CXS)** | **5,65%** — gargalo |

CXS é gargalo estrutural: 3 pernas logísticas (SFS → SP → CXS → cliente) vs 1-2 dos concorrentes. Ver `project_afs_estrutura_logistica`.

**Comissão vendedor:** 2% sobre faturamento s/IPI (não atrelado a MC).

**Impostos:** PIS/COFINS/ICMS conforme regime (ver [[11 - Normas Técnicas]] para detalhes fiscais).

### 6. Spread financeiro
Diferença entre **CF% cobrado** do cliente (custo financeiro embutido em vendas a prazo) e **Selic real** que AFS paga.

**Campos RAF:**
- `ABCCUS_FIN` (CF% cobrado) — o que cliente paga
- `ABCCUS_FIN_COB` (Selic real) — o que AFS gasta

**Spread típico:** positivo quando CF% > Selic real. Margem oculta relevante — em abr/2026, spread FIN total foi ~R$1,0M.

---

## Fluxo de cálculo no simulador

```
INPUT:
- Peça: aço, acabamento, bitola, comprimento, quantidade
- Material comprado: custo aço R$/ton, VPP, fornecedor
- Processo: corte (sim/não), TT (sim/não), ensaios, certificações
- Prazo de pagamento (dias)
- Cliente: nome, cidade, tipo tabela (A/B/C)
- Modo de venda: R$/kg, R$/pç ou R$/m

MOTOR:
1. Calcula peso de partida (baseado em bitola + comprimento + quantidade)
2. Calcula peso do orçamento do cliente (descontando perda de processo, se acabado)
3. Aplica VPP conforme modo de venda
4. Calcula custo aço total
5. Adiciona processo (corte, TT, ensaio, certif)
6. Aplica MC% sobre aço
7. Adiciona despesas variáveis (comissão, logística, comercial, frete)
8. Aplica spread financeiro
9. Calcula impostos (sobre a base correta — ICMS, PIS/COFINS)
10. Gera preço final por unidade (R$/kg, R$/pç ou R$/m)

OUTPUT:
- Preço sugerido
- DRE (MC1, MC2, composição)
- Comparativo com tabelas A/B/C
- Alerta se abaixo da tabela Vermelha
- Simulação de desconto com impacto na MC
```

---

## Relação com RAF (validação pós-venda)

Após o faturamento, o RAF permite validar:
- **MC realizada** bate com MC planejada?
- **Spreads** foram capturados conforme esperado?
- **Custo de servir** (se rastreado) bate com o previsto?

Divergências sistemáticas entre planejado (simulador) e realizado (RAF) indicam:
- Simulador com parâmetros desatualizados (ex: custo aço)
- Vendedor "emula" no simulador mas negocia diferente
- Custo real subestimado (ex: CF% cobrado não reflete Selic real)

**Calibração:** rodar dashboard corredor de MC (Motor Analítico v2) para detectar drift.

---

## Atenções críticas

### 1. Custo do aço **não** inclui VPP em R$/kg
Em venda R$/kg, cliente paga peso real na balança. Se barra vem mais pesada, cliente paga a mais — AFS não absorve. Então VPP não entra no pricing R$/kg.

### 2. Modo de venda muda componentes inclusos
Ver tabela detalhada em [[05 - Modos de Venda]]. Cada modo tem regra própria para VPP, tolerância, lâmina.

### 3. Peso de venda ≠ peso de partida (acabados)
Material acabado (trefilado, descascado, usinado) tem perda de processo. Peso de **partida** (insumo) é maior que peso do **orçamento do cliente** (acabado).

Em R$/kg com peça acabada:
- Divisor correto = peso do orçamento do cliente
- Implementado no simulador via `pesoVendaKg` (2026-04-09)

### 4. Engenheirado é exclusivamente R$/pç
Material engenheirado (ex: fora de padrão complexo) não tem peso de venda definido. Custeio usa peso de partida, venda por peça.

### 5. Desconto come MC aço primeiro
Quando vendedor dá desconto bruto, ele vem **direto da MC sobre aço**. A margem escondida (spreads) fica intacta **desde que o cliente não corte serviços**.

Implicação: descontos em pedidos **sem serviço adicional** (aço puro) derrubam MC rapidamente. Em pedidos **com serviços**, o cliente pode estar pagando mais do que percebe.

---

## Diferenças com concorrentes

### Gerdau direto ao cliente grande
- Entrega sem intermediação de distribuidor
- Custo menor (sem markup de distribuição)
- Porém: mix limitado a aço que Gerdau produz, serviços mínimos
- AFS vantagem: mix amplo, serviços, relacionamento

### Trefita/Torres
- Grupo único (Torres = forjado)
- Unidade em Contagem-MG permite arbitragem fiscal para clientes MG/ES (gap ~4-8%)
- AFS vantagem: tecnicamente mais sofisticado, melhor serviço

### GGD (Gerdau usina)
- Fornecedor de aço (bucket separado em análises)
- Não é concorrente direto — é fornecedor

### Tradings (Duferco, DITH, Stemcor)
- Musculatura financeira
- Aço global (europeu premium, etc.)
- Não operam distribuição direta (por enquanto)

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[01 - Fórmula do Lucro]]
- [[03 - Componentes de Custo]]
- [[04 - MC1 MC2 e DRE]]
- [[05 - Modos de Venda]]
- [[06 - VPP Tolerância e Lâmina]]
- [[08 - Simulador HTML - Arquitetura]]
- [[04 RAF/02 - Convenção Softcomp (Invertida)]]
- [[04 RAF/04 - Margem Oculta (7 componentes)]]
