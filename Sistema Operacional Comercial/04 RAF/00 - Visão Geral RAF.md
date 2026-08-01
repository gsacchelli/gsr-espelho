---
tipo: overview
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [raf, overview, faturamento, margem]
---

# 00 — Visão Geral RAF

## O que é

**RAF = Relatório de Acompanhamento de Faturamento** do Softcomp.

Arquivo: `DetalhesRAF.xlsx`
Estrutura: **133 colunas**
Volume: ~5.000 linhas/mês (~19.500 linhas Jan-Abr/2026)
Faturamento coberto (Jan-Abr/2026): ~R$66M

É a **fonte de verdade para análise de margem real** — pós-faturamento, com custos realizados (não estimados).

---

## Por que é o domínio mais crítico

O RAF permite responder perguntas como:
- **Qual MC real por cliente/produto/vendedor?**
- **Qual margem oculta está sendo capturada?**
- **Onde há destruição silenciosa de valor?**
- **O que o simulador previa vs o que aconteceu?**

Ou seja: é o **feedback loop** do pricing. Sem ele, negocia-se no escuro.

---

## Descoberta crítica (abr/2026)

### Convenção invertida
O Softcomp usa **nomenclatura invertida** nos campos de custo:
- `ABCCUS_X` = **VALOR COBRADO** do cliente
- `ABCCUS_X_COB` = **CUSTO REAL** pago pela AFS

Ver [[02 - Convenção Softcomp (Invertida)]].

### MC econômica revelada
Com interpretação correta, descoberta:
- **MC contábil:** R$12,59M → **29,30%** sobre líquido do aço
- **Margem escondida total:** +R$2,64M (7 componentes)
- **MC econômica:** R$15,23M → **35,44%** sobre líquido do aço
- **Uplift:** +6,15 p.p.

Em jan-fev/2026, interpretação errada gerou narrativa falsa de "margem oculta = −R$2,57M". Corrigido em abr/2026.

---

## Notas deste domínio

| # | Nota | Descrição |
|---|---|---|
| 00 | [[00 - Visão Geral RAF]] | Este mapa |
| 01 | [[01 - Estrutura das 133 Colunas]] | Descrição das colunas |
| 02 | [[02 - Convenção Softcomp (Invertida)]] | O quê é cobrado vs real |
| 03 | [[03 - MC Contábil vs Econômica]] | Diferença e interpretação |
| 04 | [[04 - Margem Oculta (7 componentes)]] | Breakdown detalhado |
| 05 | [[05 - Custo Real vs Cobrado]] | Como identificar e calcular |
| 06 | [[06 - Despesas Logísticas por Unidade]] | CXS, GRU, PIR, SCA, RIP |
| 07 | [[07 - Tab A B C e Preços Mínimos]] | Pisos por produto |
| 08 | [[08 - Consolidação por OS]] | Agregação de múltiplas linhas |
| 09 | [[09 - Critérios de Classificação]] | Tab Verde/Amarela/Vermelha/Preta + regras |
| 10 | [[10 - Margem MC PGA (Metas Anuais)]] | **Fórmula oficial das metas anuais** (MC = Aço + FIN + COR + EXT + INT + CER, sobre ValorLIQ sem IPI) |

---

## Fórmulas-chave (referência rápida)

### MC básica
```
LiquidoAco = ABCTOT_LIQ - ABCCUS           (receita líquida menos despesas embutidas)
ValorMC    = LiquidoAco - ABCCUS_ACO       (sobra após custo do aço)
MC%        = ValorMC / LiquidoAco × 100    (campo ABCPER_MAR)
```

### Margem oculta por componente
```
margem_oculta_X = ABCCUS_X - ABCCUS_X_COB
                = cobrado    - real
```

**Positivo:** margem positiva capturada
**Negativo:** AFS está absorvendo (prejuízo invisível)

### Componentes de custo
Componentes: **ACO, FIN, IMP, COM, CML, INT, CER, EXT, CTE**

| Código | Nome | Spread típico |
|---|---|---|
| ACO | Aço | Zero (estrutural) |
| FIN | Financeiro | Positivo (CF% > Selic) |
| IMP | Impostos | Zero (se bem calculado) |
| COM | Comissão | Variável |
| CML | Comercial+Logística | Zero (só custo) |
| INT | Interno | ~100% (margem oculta cheia) |
| CER | Certificação | ~100% |
| EXT | Externo (TT) | 20-40% |
| CTE | Corte | 100% (AFS absorve) |

---

## Números validados (RAF abr/2026)

### DRE consolidada
```
Receita líquida (total): ~R$66M
Receita líquida do aço:   R$42,96M (base para MC%)

MC contábil:              R$12,59M → 29,30%
Margem oculta positiva:   +R$2,64M

  Corte:        +R$1,01M
  Financeiro:   +R$1,01M
  Externo (TT): +R$466k
  Comissão:     +R$111k
  Certif:       +R$23k
  Interno:      +R$19k
  Impostos:     R$0 (bem calculado)

MC econômica:             R$15,23M → 35,44%

UPLIFT:                   +6,15 p.p.
```

### Implicação
Vendedor **vê MC contábil** na negociação. Se dá desconto, desconto come MC contábil direto. Margem oculta fica no pedido **se** cliente não corta serviços.

---

## Integração com outras ferramentas

### Motor Analítico
`motor/ingestao_raf.py::load_raf()` carrega o RAF e já calcula:
- margem_oculta_X corretamente
- mc_pct_economica
- consolidação por OS

`motor/analitica_raf.py::dre_consolidado()` gera DRE com seção "MARGEM ECONÔMICA ESCONDIDA".

### Painel de Estoque
Bloco "Famílias com margem econômica escondida" + coluna "+pp escondido" no Pareto.

### Simulador
Hoje **não usa dados do RAF** diretamente. Oportunidade futura: calibrar parâmetros do simulador com realizado do RAF (Motor Analítico v2).

---

## Atenções críticas

### 1. Convenção invertida é **armadilha**
Sem o tratamento correto, toda análise fica errada. Sempre usar funções do motor (não ler campos brutos).

### 2. Consolidação por OS é **obrigatória**
Custos podem estar em uma linha só. Analisar linha-por-linha distorce margem.

### 3. Material de partida ≠ material faturado
Campos `ABCMAT_*` (partida) vs `ABC*` (faturado) podem divergir por processo de transformação.

### 4. Campos de preço mínimo
`ABCPRE_MIN_A/B/C` — pisos das tabelas. Útil para spread: preço praticado vs piso.

### 5. ABCPRE_KG é CUSTO, não preço de venda
`ABCPRE_KG` = custo do aço em R$/tonelada. Não confundir com preço de venda.

---

## Ciclo de uso recomendado

### Semanal
1. Export do DetalhesRAF atualizado
2. Motor Analítico processa
3. Revisão de DRE consolidada
4. Notas em [[Aprendizados]] sobre pontos de atenção

### Mensal
1. Comparativo mês a mês (MC, uplift econômico, por cliente)
2. Ranking de clientes por margem líquida real
3. Decisões de carteira (requalificar, expandir, descontinuar)

### Trimestral
1. Revisão de tendência (3 meses rolantes)
2. Ajuste de parâmetros simulador
3. Conversas com vendedores sobre outliers

---

## Conexões

- [[01 - Estrutura das 133 Colunas]]
- [[02 - Convenção Softcomp (Invertida)]]
- [[03 - MC Contábil vs Econômica]]
- [[04 - Margem Oculta (7 componentes)]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]
- [[Sistema Operacional Comercial/02 Precificação/01 - Fórmula do Lucro]]
- [[Sistema Operacional Comercial/02 Precificação/04 - MC1 MC2 e DRE]]
