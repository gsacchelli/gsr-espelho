---
tipo: overview
domínio: pedidos
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [pedidos, overview, ciclo]
---

# 00 — Visão Geral Pedidos

## Status

**Domínio em construção** — documentação inicial. Ferramenta de análise de pedidos em desenvolvimento.

---

## O que é um pedido

No Softcomp, pedido é a **confirmação da venda** — transformação de cotação ganha em compromisso executado:
- Material comprometido
- Estoque alocado ou ordem de produção aberta
- Fiscal/financeiro iniciado
- Processo de entrega disparado

---

## Ciclo do pedido

```
Cotação ganha
    ↓
Pedido emitido
    ↓
Estoque alocado / Produção iniciada
    ↓
Fases de processo (corte, TT, ensaio)
    ↓
Separação
    ↓
Faturamento (nota emitida)
    ↓
RAF captura
    ↓
Entrega
    ↓
Recebimento cliente
```

---

## Notas deste domínio

| # | Nota | Status |
|---|---|---|
| 00 | [[00 - Visão Geral Pedidos]] | Esqueleto |
| 01 | [[01 - Do Pedido ao RAF]] | Completa |
| 02 | [[02 - Ciclo e Status]] | Esqueleto |
| 03 | [[03 - Métricas de Pedido]] | Esqueleto |

---

## Ferramentas

**Em desenvolvimento:** análise de Pedidos Emitidos. Parte do plano de cruzamentos entre cotação-pedido-RAF.

---

## Conexões

- [[01 - Do Pedido ao RAF]]
- [[05 Cotações/00 - Visão Geral Cotações]]
- [[04 RAF/00 - Visão Geral RAF]]
- [[07 Cruzamentos e Previsões/01 - Cotação x Pedido x RAF]]
