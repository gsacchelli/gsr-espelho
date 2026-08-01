---
tipo: overview
domínio: cotações
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [cotações, pipeline, overview]
---

# 00 — Visão Geral Cotações

## Propósito do domínio

Documenta o **funil de cotações** da AFS: como são emitidas, classificadas, encerradas, e o que os dados revelam sobre pipeline real.

Cotação é o **input do funil comercial** — sem cotação não há pedido.

---

## Fatos críticos (abr/2026)

### 1. Toda cotação é lançada pelo vendedor
**Não existe inbound distinguível** no ERP. ERP não diferencia demanda que chegou (inbound) de prospecção ativa (outbound). 100% das cotações são lançadas **manualmente pelo vendedor**.

Ver [[01 - Inbound vs Outbound (ficção do ERP)]].

### 2. "Orçamento prévio" é caixa-preta
O motivo de encerramento mais comum esconde **dois perfis totalmente diferentes** (tabelista vs projeto real).

Ver [[03 - Orçamento Prévio vs Projeto Real]].

### 3. Análise-base (mar/2026)
Diagnóstico de **29.748 cotações** (Jan-Fev/2026):
- **Win rate:** 67,6% (cotações acionáveis, excluídas orçamentos prévios)
- **Perdidas por preço:** 21%, sendo que **53% sem concorrente nomeado** (muito ruído)
- **Diferença entre ganhas (+3.0% vs red table) e perdidas por preço (+1.1%)** é só ~2pp — muitas "perdas por preço" provavelmente não são preço
- **Piracicaba é região problema:** 3 vendedores com >40% taxa de perda por preço
- **Trefita/Torres é #1 concorrente nomeado** (R$9,35M perdidos para eles)

Ver [[05 - Win Rate e Métricas]].

---

## Notas neste domínio

| # | Nota | Status |
|---|---|---|
| 00 | [[00 - Visão Geral Cotações]] | Completa |
| 01 | [[01 - Inbound vs Outbound (ficção do ERP)]] | Completa |
| 02 | [[02 - Motivos de Encerramento]] | Completa |
| 03 | [[03 - Orçamento Prévio vs Projeto Real]] | Completa |
| 04 | [[04 - Cliente-Tabelista (flag proposta)]] | Esqueleto |
| 05 | [[05 - Win Rate e Métricas]] | Completa |

---

## Conexões principais

- [[04 RAF/00 - Visão Geral RAF]] (cotações viram pedidos, pedidos viram RAF)
- [[02 Precificação/07 - Tabelas e Alçadas]] (pricing na cotação)
- [[07 Cruzamentos e Previsões/01 - Cotação x Pedido x RAF]]
- Vault estratégico: [[Cliente Ideal]], [[Custo de Servir]]
