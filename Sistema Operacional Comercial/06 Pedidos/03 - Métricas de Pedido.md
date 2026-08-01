---
tipo: esqueleto
domínio: pedidos
criado: 2026-04-17
última-revisão: 2026-04-17
status: esqueleto-a-desenvolver
tags: [métricas, kpi, pedidos]
---

# 03 — Métricas de Pedido

## Status

**Esqueleto — a desenvolver** ao implementar Análise de Pedidos Emitidos.

---

## Métricas propostas

### Volume e valor
- # de pedidos abertos
- Valor total em pedidos abertos (pipeline)
- Valor médio por pedido (ticket médio)
- Mix por unidade / família / cliente

### Ciclo
- Lead time médio (pedido → entrega)
- Cycle time médio (pedido → faturamento)
- On-time delivery %

### Liberações parciais
- % de pedidos com >1 liberação
- # médio de liberações por OS
- Valor em "comprometido mas não faturado"

### Atraso
- # pedidos em atraso
- Valor em atraso
- Causa raiz (TT, fornecedor, material, cliente)

### Cancelamento
- % pedidos cancelados
- Valor cancelado
- Motivo principal

### Qualidade
- # de retrabalhos por pedido
- # de devoluções
- Relação com cliente (concentração em clientes específicos?)

---

## KPI-alvo (propostos, ajustar com dados reais)

| KPI | Meta propuesta |
|---|---|
| On-time delivery | > 92% |
| Cycle time médio | < 21 dias |
| % retrabalho | < 2% |
| Pipeline em atraso | < 5% do total aberto |

---

## Conexões

- [[00 - Visão Geral Pedidos]]
- [[01 - Do Pedido ao RAF]]
- [[02 - Ciclo e Status]]
- [[Sistema Operacional Comercial/04 RAF/00 - Visão Geral RAF]]
