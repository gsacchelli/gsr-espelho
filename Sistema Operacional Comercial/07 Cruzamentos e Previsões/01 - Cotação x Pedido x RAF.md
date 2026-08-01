---
tipo: cruzamento
domínio: cruzamentos
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [cruzamento, cotação, pedido, raf]
---

# 01 — Cotação × Pedido × RAF

## Propósito

Cruzar as 3 fontes do ciclo comercial para gerar **rastreabilidade completa**:

```
Cotação → Pedido → Faturamento (RAF) → Resultado real
```

---

## Perguntas que o cruzamento responde

### Conversão e funil
- Qual % das cotações vira pedido?
- Qual % dos pedidos é faturado (e não cancelado)?
- Qual o tempo médio de cada etapa?

### Financeiro
- Qual a diferença entre cotação (planejado) e RAF (realizado)?
- Há vendedores que **desviam sistematicamente** da cotação (ex: dão desconto extra no momento do pedido)?
- MC cotada vs MC realizada — gap?

### Operacional
- Qual % de pedidos tem liberação parcial?
- Lead time médio (cotação → entrega)?
- On-time delivery vs prazo cotado?

### Estratégico
- Quais clientes fecham sempre com gap (cotado alto, faturado baixo)?
- Qual é o padrão de cada vendedor?
- Há sazonalidade?

---

## Chaves de cruzamento

### Chave primária: **cotação_id**
No Softcomp, cada cotação tem ID único. Quando vira pedido, esse ID é mantido ou referenciado.

### Chave secundária: **OS + ITE**
No RAF, cada linha tem `ABCOII_NUM + ABCOII_ITE`. Esse ID deve ser rastreável até a cotação original.

### Desafio
Se a rastreabilidade **se perde** (cotação sem link ao pedido, pedido sem link ao RAF), cruzamento fica incompleto.

**Implementação:** validar no motor se 100% das chaves têm match. Se < 95%, investigar.

---

## Estrutura do cruzamento (dataframe unificado)

```
por_cotacao = {
  cotacao_id,
  data_cotacao,
  cliente,
  valor_cotado,
  mc_cotada,
  status_final,  # Ganhou / Perdeu / Orçamento prévio

  # Se virou pedido:
  pedido_os,
  data_pedido,
  valor_pedido,

  # Se foi faturado:
  valor_faturado,  # RAF
  mc_realizada,   # RAF
  margem_oculta,  # RAF
  data_faturamento,

  # Métricas derivadas:
  gap_cotacao_pedido,   # valor_pedido - valor_cotado
  gap_pedido_raf,       # valor_faturado - valor_pedido
  gap_mc_cotada_real,   # mc_realizada - mc_cotada
  ciclo_dias,           # data_faturamento - data_cotacao
}
```

---

## Análises típicas

### 1. Funil de conversão

```
Cotações: 100%
     ↓ (ganhou)
Pedidos: 67%
     ↓ (faturado)
RAF: 62%
     ↓ (não cancelado)
Receita real: 60%
```

Perdas em cada etapa:
- Cotação → Pedido: 33% (dos acionáveis)
- Pedido → Fatura: 5%
- Cancelamentos: 2%

### 2. Gap de pricing

**Cotação → Pedido:** diferença no momento de fechar.
- Gap = 0: vendedor manteve preço
- Gap negativo: vendedor deu desconto adicional
- Padrão por vendedor ilumina comportamento

**Pedido → RAF:** diferença no faturamento (ajustes técnicos, fiscais).
- Pequeno gap é normal
- Gap grande = investigar

### 3. MC cotada vs realizada

Simulador prevê MC X%. RAF reporta Y%.
- Y ≈ X: simulador bem calibrado
- Y < X sistematicamente: parâmetros desatualizados (custo aço subiu, vendedor desconta mais que simulador aceita, etc.)
- Y > X: custo real veio menor (ajuste de fornecedor, lote bom)

### 4. Ciclo por família/cliente

- Quais famílias têm ciclo longo?
- Quais clientes são rápidos / lentos?
- Identificar outliers

---

## Aplicação — Dashboard proposto

### Tela 1 — Funil de conversão
- Números em cada etapa
- Evolução temporal
- Drill-down por vendedor / região / família

### Tela 2 — Gap de pricing
- Gap médio por vendedor
- Outliers (ganhas com gap negativo grande)
- Tendência mensal

### Tela 3 — MC cotada vs realizada
- Scatter plot: previsto × realizado por pedido
- Regressão ideal (linha y=x)
- Desvio sistemático

### Tela 4 — Rastreabilidade quebrada
- Cotações sem pedido identificado (ganhas mas sem match)
- Pedidos sem RAF (ainda não faturados? cancelados sem registro?)
- Linhas RAF sem pedido origem (correções/ajustes?)

---

## Desafios de implementação

### 1. Rastreabilidade no Softcomp
Precisa investigar como Softcomp linka cotação → pedido → RAF. Pode requerer:
- SQL direto (via VPN, v2 do Motor)
- Ou exports específicos que tragam a relação

### 2. Timing dos exports
Cotação fechada hoje pode virar pedido amanhã, faturamento em 2 semanas. Se export é mensal, recortes podem estar desalinhados.

**Solução:** cruzamento com **janela móvel** (ex: pedidos últimos 90 dias + RAF últimos 90 dias), não mês fechado.

### 3. Consolidação
RAF precisa ser **consolidado por OS** (ver [[04 RAF/08 - Consolidação por OS]]) antes de cruzar com pedido, senão múltiplas linhas distorcem.

### 4. Campos com nomes diferentes
Campo "cliente" pode ter nome diferente em cada tabela (`ABCCLI_*` no RAF, outro no módulo de cotação). Padronizar.

---

## Roadmap

### Motor Analítico v1
- Ingestão separada de RAF + Cot_Encerradas
- Cruzamento simples (por cliente, não por cotação_id)

### Motor Analítico v2
- Cruzamento por cotação_id
- Dashboard completo
- Rastreabilidade quebrada como alerta

### Motor Analítico v3 (futuro)
- Conexão SQL direta (via VPN)
- Cruzamento em tempo real
- Alertas automáticos de desvio

---

## Conexões

- [[00 - Visão Geral Cruzamentos]]
- [[03 - Pricing Planejado x Realizado]]
- [[05 Cotações/00 - Visão Geral Cotações]]
- [[06 Pedidos/01 - Do Pedido ao RAF]]
- [[04 RAF/00 - Visão Geral RAF]]
- [[04 RAF/08 - Consolidação por OS]]
- [[01 Sistema de Dados/06 - Motor Analítico v1]]
