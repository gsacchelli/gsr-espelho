---
titulo: Critérios de Classificação no Motor de Enriquecimento RAF
tipo: documentação técnica
projeto: Motor RAF de Enriquecimento + Painel Comercial
ultima_revisao: 2026-04-28
relacionados:
  - "[[04 RAF/00 - Visão Geral RAF]]"
  - "[[04 RAF/02 - Convenção Softcomp (Invertida)]]"
  - "[[04 RAF/03 - MC Contábil vs Econômica]]"
  - "[[04 RAF/04 - Margem Oculta (7 componentes)]]"
  - "[[04 RAF/05 - Custo Real vs Cobrado]]"
---

# Critérios de Classificação no Motor RAF

Esta nota é a **fonte da verdade** das decisões metodológicas que regem como o motor de enriquecimento (`MotorAnalitico/raf/enriquecer.py`) e o painel agregador (`MotorAnalitico/raf/painel_aggregator.py`) classificam linhas do RAF.

Toda mudança aqui deve ser refletida no código + log datado. Toda mudança no código que não passe por aqui é débito metodológico.

---

## 1. Corte SN — qual linha é "Cortada"

**Critério atual (28/04/2026)**: `ABCCUS_CTE > 0` (custo de corte cobrado > 0).

**Histórico**:
- Até 27/04/2026: `ABCPES_CTE > 0` (peso de corte > 0).
- A partir de 28/04/2026: trocado para `ABCCUS_CTE > 0`.

**Motivo da mudança**: Alguns serviços de corte não geram peso registrado (corte de chapa fina, corte sob medida sem subproduto remanescente identificado no estoque), mas geram custo cobrado na linha. Usar `ABCCUS_CTE` captura todas as operações que **financeiramente** são cortadas, independente de haver peso de subproduto.

**Implementação**: `MotorAnalitico/raf/enriquecer.py::derivar_corte`.

---

## 2. Considerar para Análise — Tipo_Linha + Considerar_Analise

Linhas que entram nas análises por default (toggle "Apenas linhas analisáveis"):
- Tipo_Linha = `Produto` ou `Beneficiamento` ou `Devolução`
- Tipo_Linha = `Acessório` ou `Sucata` → Considerar = False (filtradas)

**Decisão**: Devolução fica True porque faz parte do faturamento líquido (não pode ser ignorada na MC). Acessório e Sucata são operações distintas, sem mix com produto principal.

---

## 3. Família Canônica — produto vendido

Família vendida é codificada no formato:
```
<Aço> <Perfil> <Acab> de <Bitola_min> até <Bitola_max>
Ex: "1045 R T de 12,70 até 101,60"
```

Onde:
- **Aço**: padronizado por dicionário (ex: 1018→1018, 1022→1020, 4140→4140 etc.)
- **Perfil**: 1 letra (R=Redondo, Q=Quadrado, S=Sextavado, etc.)
- **Acab.**: 1 letra (T=Trefilado, L=Laminado, F=Forjado, etc.)
- **Faixa Bitola**: range fechado (ex: 12,70 até 101,60)

207 combinações possíveis no `criterios_raf.xlsx`.

**No painel** (a partir de 28/04/2026): perfil e acabamento mostram nome completo via `ABCPER_DES` e `ABCACA_DES` (Redondo, Trefilado etc.) — código de 1 letra fica só na string da família.

---

## 4. Especiais — produtos com descrição em texto livre

**Critério**: `ABCTIP_PRO = 2` no RAF.

São linhas onde o produto vendido NÃO está cadastrado na taxonomia padrão — descrição entrou como texto livre (geralmente itens sob encomenda / sob medida / fora de portfólio).

**Tratamento no painel** (decisão 28/04/2026, Opção C):
- Todas as linhas com `ABCTIP_PRO=2` viram bucket único: família = `ESPECIAIS`.
- Aço, Perfil, Acabamento aparecem como `Especiais` (não decompostos).
- Bitola fica como `—`.

**Por que não decompor?** A descrição de texto livre não segue padrão; tentar parsear gera ruído ("Combinação não mapeada: 4130MOD Redondo Forjado 508mm" não é um Aço chamado "Combinação"). Agregar tudo num bucket único é mais honesto.

**Distinção importante** — três coisas diferentes que parecem iguais:
- `ABCTIP_PRO=2` → **Especiais** (texto livre cadastrado intencionalmente)
- Família = `Não mapeada` → falha do enriquecimento (criterios_raf.xlsx não cobriu o caso, é dívida técnica)
- Família = `Produto Fora Padrão` → produto fora dos critérios padrão (ex: bitola fora dos ranges, mas aço conhecido)

Especiais ficam agregadas; Não Mapeada e Fora Padrão ficam expandidas pra você corrigir o lookup.

---

## 5. Material Vendido vs Material Partida

**Vendido**: o produto que sai pro cliente. Família via `Familia_Desc` (criterios_raf).

**Partida**: o material consumido do estoque pra produzir o vendido. Família construída como `<ABCMAT_TIP> <P> <A>` (sem bitola — agrega muitas bitolas em uma linha de estoque).
- Ex: `4130MOD R F` (4130MOD Redondo Forjado em todas as bitolas)
- ~40-50 famílias possíveis (vs 200+ no vendido)

**Quando `ABCMAT_TIP_PRO != 1`**: material partida não é padrão de estoque (ex: Beneficiamento puro, onde matéria-prima é do cliente). Tratado como `Material Partida n/d`.

**Implementação**: cubos paralelos `cubo_produto` e `cubo_produto_partida` no aggregator. Toggle "Material" do painel escolhe um ou outro.

---

## 6. Tabela Fechada (V/A/V/Preta)

Determinada por linha-a-linha comparando `ABCOIIPVO` (preço fechado) com `ABCPRE_MIN_A`, `ABCPRE_MIN_B`, `ABCPRE_MIN_C` (mínimos das tabelas Verde/Amarela/Vermelha):
- Preço >= Verde → `Verde`
- Preço >= Amarela e < Verde → `Amarela`
- Preço >= Vermelha e < Amarela → `Vermelha`
- Preço < Vermelha → `Preta`

**Tabela predominante por OS** (KPIs de Pricing): a OS é classificada pela tabela com maior `ValorLIQ` somado entre suas linhas. ~95% das OSs fecham em uma única tabela; minoria que mistura é tratada por valor predominante.

**Tabela Preta** = oportunidade perdida. Vale rastrear: quem é o vendedor / cliente / família que mais fecha abaixo da Vermelha?

---

## 7. MC Aço, Margem Agregada, MC Total

Conceitos críticos. Detalhe completo em `[[04 RAF/03 - MC Contábil vs Econômica]]` e `[[04 RAF/04 - Margem Oculta (7 componentes)]]`.

Resumo:
- **MC Aço (R$)** = `ValorMC` do RAF cru = `ValorLIQ − Aço − Σ reais − Descontos s/ Vendas`. É a MC parcial calculada pelo Softcomp.
- **Margem Agregada (R$)** = `Σ (cobrado − real) por linha`, somando os 7 componentes (Externo, Financeiro, Comissão, Interno, Certificação, DDV+LOG, Corte). É a margem oculta reconhecida pelo motor.
- **MC Total Econômica** = MC Aço + Margem Agregada.

**Margem de Contribuição "clássica" (DRE Gerencial)** = `ValorLIQ − Aço − Custos Diretos de Operação − Custos de Servir`. Diferente do MC Total Econômica em ~R$ 5 MM/ano (na ordem de 2-3% pp).

A diferença vem de duas coisas: descontos s/ vendas (que ValorMC desconta mas a DRE simples não) e diferentes pcts cobrado/real.

---

## 8. Regra Temporária DDV+LOG (até OrcamentoAnual)

**Vigente desde 27/04/2026**: motor força `real DDV+LOG = cobrado` (spread = 0) porque os pcts reais granulares por unidade × ano não estão no `criterios_raf.xlsx`.

**Fim da regra**: quando `01_Brutos/OrcamentoAnual/OrcamentoAnual.xlsx` for preenchido com despesas reais por (ano, unidade) → motor passa a calcular pct real e gerar spread DDV+LOG real.

**Status atual**: orçamentos de 2023-2026 já parseados e preenchidos no template (sessão 28/04). Caminho de implementação parqueado por enquanto — o Report do Sacchelli foi simplificado pra usar `ABCCUS_CML_COB` (cobrado bruto), eliminando a divergência principal.

Detalhes: `[[Logs/2026-04-27 — Bloco 1+2 RAF + Painel Estoque + Aggregator Painel Comercial]]` seção "Reconciliação contra Report v2".

---

## 9. Distinct Counts (OS, NF, Cliente)

KPIs de Operações usam o cubo OS (1 linha por `ABCOII_NUM`):
- **OS** = `ABCOII_NUM` distintas
- **NF** = `ABCNNF_NUM` distintas (uma OS pode ter múltiplas NFs por entrega parcelada)
- **Clientes** = `ABCCLIRED` distintos

**Ticket Médio** = Receita Líquida ÷ nº OS (NÃO por linha — uma OS pode ter 5-50 itens).

**R$/kg** (preço médio) = ValorLIQ ÷ Qtd. Métrica de elasticidade — quando cai mantendo MC%, é pricing power perdido; quando sobe junto com MC%, é mix-shift positivo.

---

## Integração com painéis

| Coluna derivada | Onde aparece | Filtro? |
|---|---|---|
| `Familia_Desc` | Heatmap Família×Gerência, Produtos | Sim |
| `Familia_partida` (calc no aggregator) | Aba Produtos, toggle Material=Partida | Sim |
| `Corte_SN` | Filtro secundário Produtos, Mix Atributos | Sim |
| `Tabela_Fechada` | KPIs Pricing (V/A/V/Preta), Tab Tabela Preta | — |
| `Tipo_Linha` / `Considerar_Analise` | Toggle global "Apenas linhas analisáveis" | Sim |
| `Op_Categoria` | Filtro global Op. Categoria | Sim |
| `MC_Aco_RS` / `MC_Spread_RS` / `MC_Total_RS` | DRE Gerencial, Tabelas, KPIs Margens | — (calculadas) |

---

## Histórico de revisões

- **2026-04-28** — Corte SN: `ABCPES_CTE > 0` → `ABCCUS_CTE > 0`. Especiais (`ABCTIP_PRO=2`) viraram bucket "ESPECIAIS" agregado. Material Partida implementado como cubo paralelo. Métricas de OS/NF/Cliente distintas + R$/kg adicionadas aos KPIs. Esta nota criada como fonte da verdade.
- **2026-04-27** — Regra temporária DDV+LOG (real=cobrado, spread=0) ativada no Bloco 2. MC Econômica vs Contábil definida.
