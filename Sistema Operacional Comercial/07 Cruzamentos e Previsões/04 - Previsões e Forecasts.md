---
tipo: esqueleto
domínio: cruzamentos
criado: 2026-04-17
última-revisão: 2026-04-17
status: esqueleto-a-desenvolver
tags: [forecast, previsão, pipeline]
---

# 04 — Previsões e Forecasts

## Status

**Esqueleto — a desenvolver** quando Motor Analítico v2/v3 estiver maduro.

---

## Objetivo

Projetar:
- **Receita** nos próximos 30/60/90 dias
- **Margem** esperada
- **Pipeline de projeto** (ANDRITZ, PROK, etc.)
- **Necessidade de estoque** por família

---

## Metodologia proposta

### Forecast de receita
Soma ponderada:
- Pedidos em carteira (alto peso — já fechado)
- Cotações em andamento (peso médio — probabilidade de fechamento)
- Projetos identificados (peso baixo — ciclo longo, incerteza)
- Mais: média móvel 90 dias de clientes recorrentes

### Forecast de margem
Aplicar MC histórica por família × volume projetado.

### Forecast de demanda por família
Série temporal mensal + sazonalidade + tendência.

### Forecast de pipeline de projeto
Listar projetos conhecidos com:
- Probabilidade de fechamento (subjetiva inicial, objetiva depois)
- Valor estimado
- Mês esperado

---

## Fontes de dados

- Cotações abertas (pipeline atual)
- Pedidos abertos (confirmado, não faturado)
- RAF histórico (base para média móvel)
- Estoque (restrições de capacidade)

---

## KPIs de acurácia

- **MAPE (Mean Absolute Percentage Error):** |previsto − realizado| / realizado
- Meta: MAPE < 15% para horizonte 30 dias

---

## Desenvolvimento futuro

Implementar somente após:
1. Motor Analítico v1 maduro
2. Cruzamentos 01, 02, 03 funcionando
3. Série temporal de 12+ meses acumulada no sistema

Prematuro implementar sem essas bases.

---

## Conexões

- [[00 - Visão Geral Cruzamentos]]
- [[01 - Cotação x Pedido x RAF]]
- [[02 - Estoque x RAF (giro real)]]
- [[03 - Pricing Planejado x Realizado]]
- [[Sistema Operacional Comercial/05 Cotações/03 - Orçamento Prévio vs Projeto Real]] (projetos)
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]
