---
tipo: esqueleto
domínio: pedidos
criado: 2026-04-17
última-revisão: 2026-04-17
status: esqueleto-a-desenvolver
tags: [ciclo, status, pedidos]
---

# 02 — Ciclo e Status

## Status

**Esqueleto — a desenvolver.** Aguarda implementação da Análise de Pedidos Emitidos.

---

## Rascunho de conteúdo

### Status possíveis de pedido (a confirmar com Softcomp)
- Aberto / Em análise
- Aprovado / Em produção
- Em separação
- Em TT / Processamento externo
- Pronto para faturamento
- Faturado
- Entregue
- Encerrado
- Cancelado

### Fluxo de status
Mapear transições válidas entre status.

### Status-alvo por idade
- Em produção > 30 dias: atenção
- Em TT > 45 dias: investigar
- Faturado > 60 dias sem entrega: problema logístico

### KPIs
- Tempo médio por status
- % de pedidos em cada status
- Pedidos em risco (prazo)

---

## Próxima ação

Ao implementar Análise de Pedidos Emitidos, extrair status do Softcomp e preencher esta nota com dados reais.

## Conexões

- [[00 - Visão Geral Pedidos]]
- [[01 - Do Pedido ao RAF]]
- [[03 - Métricas de Pedido]]
