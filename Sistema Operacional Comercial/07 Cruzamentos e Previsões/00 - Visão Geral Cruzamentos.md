---
tipo: overview
domínio: cruzamentos
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [cruzamentos, previsões, overview, integração]
---

# 00 — Visão Geral Cruzamentos e Previsões

## Propósito do domínio

Este domínio é **onde os dados se encontram**. Não trata de um sistema isolado, mas de **como os dados de estoque, cotação, pedido, pricing e RAF se cruzam** para gerar:
- Análises integradas
- Previsões (forecasts)
- Decisões de maior alavancagem

Este é o coração da **inteligência comercial** — perguntas que nenhum sistema isolado responde.

---

## Por que cruzar dados importa

### Exemplo 1 — Pricing planejado vs realizado
- Simulador cria DRE planejada
- RAF reporta realizado
- **Cruzamento** revela onde vendedor "contorna" o simulador ou parâmetros estão desatualizados

### Exemplo 2 — Estoque × venda
- Painel mostra posição estática
- RAF mostra saídas reais
- **Cruzamento** dá giro real por família

### Exemplo 3 — Cotação × pedido × RAF
- Cotação tem preço alvo
- Pedido confirma (ou ajusta)
- RAF finaliza com custo real
- **Cruzamento** revela desvios em cada etapa

### Exemplo 4 — Forecast
- Pipeline atual (cotações + pedidos abertos)
- Histórico de conversão (RAF × Cotações encerradas)
- **Cruzamento** projeta receita futura

---

## Notas deste domínio

| # | Nota | Status |
|---|---|---|
| 00 | [[00 - Visão Geral Cruzamentos]] | Este mapa |
| 01 | [[01 - Cotação x Pedido x RAF]] | Completa |
| 02 | [[02 - Estoque x RAF (giro real)]] | Completa |
| 03 | [[03 - Pricing Planejado x Realizado]] | Completa |
| 04 | [[04 - Previsões e Forecasts]] | Esqueleto |

---

## Ferramentas

### Motor Analítico v1 — parcialmente
Motor Analítico já tem ambição de fazer alguns cruzamentos (RAF + Cotações, RAF + Critérios). **Integração completa fica para v2**.

### Cruzamentos futuros
- Motor Cruzamento dedicado (módulo do Motor Analítico v2)
- API unificada que consome dos 6 domínios

---

## Princípios para cruzamentos

### 1. Chave consistente
Qualquer cruzamento precisa de **chave comum**:
- Entre cotação/pedido/RAF: **cotação_id → OS**
- Entre domínios de produto: **Família Canônica**
- Entre cliente: **código de cliente**
- Entre tempo: **período datado**

### 2. Qualidade antes de cruzar
Se um domínio tem dado ruim, cruzamento propaga o problema. **Validar cada fonte** antes de unir.

### 3. Granularidade adequada
Cruzar **granularidades diferentes** (ex: cotação individual vs estoque diário) exige agregação explícita.

### 4. Tempo é dimensão
Dados estáticos podem enganar. Tempo mostra tendências.

---

## Ordem de prioridade dos cruzamentos (implementação)

### Alta prioridade
1. **Pricing planejado × realizado** — calibra simulador
2. **Cotação × pedido × RAF** — rastreabilidade comercial
3. **Estoque × venda** — giro real por família

### Média prioridade
4. **Vendedor × margem econômica** (não só volume)
5. **Cliente × margem líquida real** (MC econômica − CS)

### Baixa prioridade (sofisticado)
6. **Forecast de demanda** por família
7. **Probabilidade de projeto fechar** (pipeline de ANDRITZ, PROK, etc.)
8. **Simulação de cenários** (e se cliente X aceita Give/Get Y?)

---

## Conexões

- [[01 - Cotação x Pedido x RAF]]
- [[02 - Estoque x RAF (giro real)]]
- [[03 - Pricing Planejado x Realizado]]
- [[04 - Previsões e Forecasts]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]
- Todos os outros domínios (convergem aqui)
