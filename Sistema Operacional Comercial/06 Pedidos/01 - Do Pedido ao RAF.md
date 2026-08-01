---
tipo: processo
domínio: pedidos
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [ciclo, pedido, faturamento, raf]
---

# 01 — Do Pedido ao RAF

## O pipeline completo

Pedido emitido → RAF em 5 etapas:

### Etapa 1 — Pedido registrado
Cotação ganha vira pedido. Sistema cria:
- Número de OS (Ordem de Serviço)
- Itens do pedido (cada item = OS + ITE)
- Reserva de estoque ou ordem de produção

**Campos-chave criados:**
- `ABCOII_NUM` (OS)
- `ABCOII_ITE` (item)
- Valores planejados (preço, quantidade, cliente)

### Etapa 2 — Fases de processo
Se pedido envolve processos além de separação pura:
- **Corte:** dimensionamento
- **Tratamento térmico (TT):** têmpera, revenido, etc.
- **Ensaios:** dureza, dimensional, metalografia
- **Certificações:** emissão de documentos
- **Rastreabilidade:** controle de lote/corrida

Cada fase pode ter **fornecedor interno ou externo**:
- Interno: operação AFS
- Externo: terceirizado (TT geralmente)

### Etapa 3 — Separação e conferência
Material é separado fisicamente:
- Pesagem
- Conferência dimensional
- Conferência visual
- Certificação do lote

### Etapa 4 — Faturamento
Nota fiscal emitida:
- Valor faturado
- Impostos (IPI, ICMS, PIS, COFINS)
- Prazo de pagamento (se aplicável)
- Frete e condições

**Neste momento**, o item "entra" no RAF. Colunas `ABCCUS_*` e `ABCTOT_*` são populadas.

### Etapa 5 — Entrega e ciclo fechado
Material enviado ao cliente. Entrega registrada no sistema.

Se houver **liberação parcial**: múltiplas entregas da mesma OS → múltiplas linhas no RAF → **precisa consolidação** (ver [[04 RAF/08 - Consolidação por OS]]).

---

## Pontos de atenção

### 1. Pedido ≠ RAF em tempo real
Pedido emitido hoje pode aparecer no RAF daqui a semanas (fases demoram). Análise de pipeline precisa considerar esse delay.

### 2. Liberação parcial é comum
Grandes OS têm múltiplas liberações. Cada uma vira linha no RAF. Sem consolidação, distorce análise.

### 3. Campos COB populados apenas após faturamento
Custo real (`ABCCUS_X_COB`) só é conhecido após **processo finalizado**. Durante o pedido, só há custo **planejado**.

### 4. Cancelamento/renegociação afeta dados
Se pedido é cancelado após iniciar processo, pode gerar linhas negativas no RAF ou registros fantasma.

---

## Métricas do ciclo

### Lead time
```
Lead time = Data_entrega - Data_pedido (em dias)
```

Componentes:
- Pedido → início produção: minutos a dias
- Início → TT: dias a semanas
- TT → ensaios: dias
- Separação: horas a dia
- Faturamento: horas
- Entrega: dias (logística)

### On-time delivery
```
On-time = Entregue_no_prazo_contratado / Total_entregas
```

### Cycle time para faturamento
```
Cycle = Data_faturamento - Data_pedido
```

Métrica importante para **fluxo de caixa** — quanto tempo dinheiro fica preso.

---

## Desafios de análise

### Pipeline em andamento
Pedidos **emitidos mas não faturados** não aparecem no RAF. Para ter visão completa, precisa juntar:
- **Pedidos abertos** (Softcomp → módulo pedidos)
- **RAF** (pedidos faturados)

Cruzamento permite visão de pipeline completo em valor e ciclo.

### Reconciliação cotação → pedido → RAF
Cotação tem um número. Pedido gera OS. RAF tem linhas por OS+ITE.
Se o cruzamento não for feito por chaves consistentes, perde-se rastreabilidade.

**Chave universal proposta:** cotação_id → OS → OS+ITE no RAF.

### Material de partida vs faturado
Como já discutido:
- Material de partida (`ABCMAT_*`): insumo bruto
- Material faturado (`ABC*`): produto entregue após processo

Se quer analisar **uso de estoque**, usar `ABCMAT_FAA`. Se quer analisar **venda**, usar `ABCFAACOD`.

---

## Ferramentas (existente e planejado)

### Hoje
- Consulta de pedidos em aberto via Softcomp (individual)
- RAF para pedidos faturados

### Planejado — Análise de Pedidos Emitidos
Dashboard que consolida:
- Pedidos abertos por valor, idade, cliente
- Liberações parciais em andamento
- Pedidos em risco (prazo estourando)
- Mix do pipeline (qual família, qual unidade)

Vai consumir dados cruzados (cotação + pedido + RAF).

---

## Conexões

- [[00 - Visão Geral Pedidos]]
- [[02 - Ciclo e Status]]
- [[03 - Métricas de Pedido]]
- [[05 Cotações/00 - Visão Geral Cotações]]
- [[04 RAF/00 - Visão Geral RAF]]
- [[04 RAF/08 - Consolidação por OS]]
- [[07 Cruzamentos e Previsões/01 - Cotação x Pedido x RAF]]
