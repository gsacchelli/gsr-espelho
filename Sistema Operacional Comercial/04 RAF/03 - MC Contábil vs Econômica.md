---
tipo: conceito-crítico
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [mc, contábil, econômica, margem, uplift]
---

# 03 — MC Contábil vs MC Econômica

## Os dois números da margem

A Sacchelli tem **duas medidas de MC** que coexistem e dizem coisas diferentes:

### MC Contábil
MC tradicional, reportada no sistema. Calcula **apenas margem sobre aço explícito**.

**Campo RAF:** `ABCPER_MAR`

**O que mede:** receita líquida menos custo do aço, como % sobre líquido.

**O que o vendedor vê:** este número. Ao negociar desconto, vê essa MC.

### MC Econômica
MC contábil **mais** todas as margens ocultas capturadas em serviços e spreads.

**Não tem campo direto no RAF** — calculada a partir dos spreads.

**O que mede:** captura real de valor pela AFS, incluindo margem oculta.

**O que a gestão vê:** este número, via Motor Analítico.

---

## Fórmula

### MC Contábil
```
MC_contábil$  = LiquidoAco - ABCCUS_ACO
MC_contábil%  = MC_contábil$ / LiquidoAco × 100
                = campo ABCPER_MAR
```

### MC Econômica
```
MC_econômica$ = MC_contábil$ + Σ margem_oculta_X
              = MC_contábil$ + margem_oculta_corte
                           + margem_oculta_TT
                           + margem_oculta_ensaios
                           + margem_oculta_certif
                           + margem_oculta_interno
                           + margem_oculta_financeiro
                           + margem_oculta_comissão
                           + margem_oculta_impostos

MC_econômica% = MC_econômica$ / LiquidoAco × 100
```

### Uplift
```
Uplift (p.p.) = MC_econômica% - MC_contábil%
```

---

## Números validados (RAF abr/2026)

### Base
- **Volume analisado:** 19.535 vendas (Jan-Abr/2026)
- **Líquido do aço:** R$42,96M

### MC Contábil
- **Valor:** R$12,59M
- **Percentual:** **29,30%**

### Margem oculta detalhada
| Componente | Margem oculta | % sobre líquido aço |
|---|---|---|
| Corte (CTE) | +R$1,01M | +2,35 p.p. |
| Financeiro (FIN) | +R$1,01M | +2,35 p.p. |
| Externo/TT (EXT) | +R$466k | +1,08 p.p. |
| Comissão (COM) | +R$111k | +0,26 p.p. |
| Certificação (CER) | +R$23k | +0,05 p.p. |
| Interno (INT) | +R$19k | +0,04 p.p. |
| Impostos (IMP) | R$0 | 0,00 p.p. |
| **Total** | **+R$2,64M** | **+6,15 p.p.** |

### MC Econômica
- **Valor:** R$15,23M
- **Percentual:** **35,44%**

### Uplift total
**+6,15 p.p.**

Significa: a **margem real capturada** pela AFS é **1/5 maior** do que a MC contábil reportada.

---

## Implicação estratégica

### O que o vendedor vê × o que a empresa captura

| | Vendedor | Empresa |
|---|---|---|
| Vê | 29,30% | 35,44% |
| Decide desconto baseado em | MC contábil | (inconsciente) |
| Sensibilidade | alta (cada p.p. pesa) | menor (há cushion) |

### Risco de desconto bruto
Vendedor dá 5% de desconto pensando que MC continua em "saudável" ~25%. Na realidade, MC econômica cai de 35,44% para ~30,44% — dentro do aceitável.

**Mas:** se cliente **cortar serviços** (pedir aço puro), a margem oculta **some**. Aí o desconto come MC de verdade.

### Regra operacional
Ao analisar impacto de desconto:
1. Calcular desconto sobre MC **contábil** (pior cenário — cliente corta serviços)
2. Calcular desconto sobre MC **econômica** (melhor cenário — cliente mantém serviços)
3. Range entre os dois é o intervalo de confiança do impacto

---

## Por que não incentivar direto por MC econômica?

### Opção 1 — Pagar por MC econômica
**Problema:** Wagner pode mexer no custo do aço ou na alíquota de spread. Vendedor perde comissão por razões fora do controle dele. **Quebra contrato psicológico.**

### Opção 2 — Pagar por MC contábil
**Problema:** vendedor não captura valor oculto. Pode dar desconto reduzindo MC econômica sem perceber.

### Opção 3 (recomendada) — Pagar por **proxies controláveis**
Pagar por:
- Aderência à tabela (preço vs Verde/Amarela/Vermelha)
- Cobrança de juro em prazo (não "devolver" via desconto)
- Cobrança de serviços discricionários (não cortesia)

Essas métricas **movem** MC econômica, mas são 100% sob controle do vendedor.

Ver [[02 Precificação/07 - Tabelas e Alçadas]].

---

## Como calcular MC Econômica na prática

### Hoje (Motor Analítico v1)
`motor/analitica_raf.py::dre_consolidado()` já gera:

```
DRE CONSOLIDADO (abr/2026)
─────────────────────────────────────
Receita líquida do aço:    R$42,96M
Custo aço:                 R$30,37M
─────────────────────────────────────
MC CONTÁBIL:               R$12,59M  29,30%

MARGEM ECONÔMICA ESCONDIDA:
  Corte:                   +R$1,01M
  Financeiro:              +R$1,01M
  Externo:                 +R$466k
  Comissão:                +R$111k
  Certificação:            +R$23k
  Interno:                 +R$19k
  Impostos:                 R$0
─────────────────────────────────────
MC ECONÔMICA:              R$15,23M  35,44%
UPLIFT:                   +6,15 p.p.
```

### Por cliente
Desagregar por cliente permite saber quais clientes geram mais **valor econômico** (não apenas mais volume).

### Por família
Desagregar por família canônica mostra quais produtos carregam mais margem oculta.

### Por unidade
Comparação interessante: CXS (handicap logístico) tem MC contábil menor que GRU? A margem econômica compensa?

---

## O que pode distorcer o cálculo

### 1. Consolidação por OS não feita
Sem consolidar, uma linha pode ter custo zerado e outra inflado. Margem oculta calculada por linha vira bagunça. Ver [[08 - Consolidação por OS]].

### 2. Convenção invertida não aplicada
Interpretação errada (spread como subsídio negativo) gerou narrativa oposta. Ver [[02 - Convenção Softcomp (Invertida)]].

### 3. Componentes faltando
Se o export RAF não trouxer todos os campos `ABCCUS_X_COB`, alguns spreads vão zerar artificialmente. Validar completude.

### 4. Período atípico
Análise de período muito curto (1 semana) pode ter outliers. Recomendado rolling 3 meses mínimo.

---

## Próximos passos para uso sistemático

### Dashboard mensal (Motor Analítico v2)
- MC Contábil e Econômica por mês
- Uplift % ao longo do tempo
- Top 10 clientes por valor econômico captured
- Famílias com maior spread

### Calibração do simulador
Se simulador prevê MC 28% e RAF realiza 32% (MC contábil), ajustar parâmetros do simulador.

### Alertas
Alerta se uplift cai abaixo de 5 p.p. — indicador de que margem oculta está sendo comprometida.

---

## Conexões

- [[00 - Visão Geral RAF]]
- [[01 - Estrutura das 133 Colunas]]
- [[02 - Convenção Softcomp (Invertida)]]
- [[04 - Margem Oculta (7 componentes)]]
- [[05 - Custo Real vs Cobrado]]
- [[02 Precificação/01 - Fórmula do Lucro]]
- [[02 Precificação/04 - MC1 MC2 e DRE]]
- [[02 Precificação/07 - Tabelas e Alçadas]]
