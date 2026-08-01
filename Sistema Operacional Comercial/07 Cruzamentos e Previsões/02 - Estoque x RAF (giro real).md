---
tipo: cruzamento
domínio: cruzamentos
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [cruzamento, estoque, raf, giro]
---

# 02 — Estoque × RAF (giro real)

## Propósito

Cruzar **posição de estoque** (Excel Estoque) com **saídas efetivas** (RAF) para calcular:
- Giro real por família canônica
- Dias de cobertura por SKU
- Alertas de ruptura
- Obsolescência por valor

---

## Perguntas respondidas

### Giro
- Qual o giro real de cada família? (não estimado)
- Quais famílias giram mais rápido que o histórico sugere?
- Quais giram mais devagar?

### Cobertura
- Para cada SKU, quantos dias de estoque temos ao ritmo atual de venda?
- Qual SKUs podem zerar em X dias?

### Obsolescência
- Quais itens estão sem movimento há mais de 180/365 dias?
- Qual o valor total de estoque "dormente"?

### Mix
- Onde o estoque está (família/unidade) vs onde a venda acontece?
- Mismatches indicam problemas de planejamento.

---

## Chave de cruzamento

### Família Canônica
`Aço + Tipo + Perfil + Acabamento + Faixa de Bitola` (ver [[Sistema Operacional Comercial/03 Estoque/01 - Família Canônica]]).

### Unidade
GRU, SCA, PIR, RIP, CXS.

### Período
- Estoque: snapshot em data D
- RAF: saídas nos últimos N dias (recomendado 90-180)

---

## Estrutura do cruzamento

```
por_familia_unidade = {
  familia_canonica,
  unidade,

  # Do Estoque:
  estoque_kg,
  estoque_valor,
  idade_media_dias,

  # Do RAF (últimos 90 dias):
  saida_kg_90d,
  saida_valor_90d,
  num_vendas,
  mc_media,

  # Métricas derivadas:
  giro_anualizado = saida_kg_90d × 4 / estoque_kg,
  dias_cobertura = estoque_kg / (saida_kg_90d / 90),
  taxa_ruptura = # dias zerado / 90,
  valor_dormente = estoque_valor if saida_kg_90d == 0 else 0,
}
```

---

## Análises típicas

### 1. Ranking de giro

Top famílias por giro (alto):
- AFS captura bem essas famílias, compra na quantidade certa
- Pode aumentar buffer se há rupturas

Top famílias por baixo giro:
- Capital preso
- Candidatos a descontinuar ou promover

### 2. Cobertura por SKU

Alerta vermelho: SKU com < 7 dias de cobertura e histórico de demanda consistente
→ **Risco de ruptura** — acionar compra

Alerta amarelo: SKU com > 180 dias de cobertura
→ **Estoque alto para a demanda** — reduzir compra, promover venda

### 3. Mismatch estoque × venda

- Família X: 30% do estoque, só 5% das vendas → concentração errada
- Família Y: 5% do estoque, 20% das vendas → rupturas frequentes?

Implicação: realocar compra.

### 4. Obsolescência

Itens com **saída zero em 180 dias**:
- Quantos SKUs?
- Valor total?
- Tendência (aumentando ou diminuindo)?

Com esse número, decidir:
- Liquidar com desconto
- Descontinuar família
- Investigar causa (demanda caiu? concorrente ficou mais barato?)

### 5. Por unidade

Análise de estoque por unidade:
- Onde está o estoque
- Onde acontece a venda
- Transferências entre unidades resolvem mismatch

CXS (handicap logístico) — estoque alto pode ser necessário para compensar 3 pernas logísticas. Mas precisa justificar.

---

## Alertas automáticos (propostos)

| Alerta | Condição | Ação |
|---|---|---|
| Ruptura iminente (vermelho) | Cobertura < 7 dias, demanda consistente | Compra urgente |
| Ruptura provável (amarelo) | Cobertura < 15 dias | Planejar reposição |
| Estoque alto (amarelo) | Cobertura > 180 dias | Reduzir compra, promover |
| Dormente (amarelo) | Sem saída > 180 dias | Avaliar descontinuar |
| Obsoleto (vermelho) | Sem saída > 365 dias | Liquidar ou baixa |
| Mismatch (informativo) | Família concentrada em estoque mas não em venda | Revisar planejamento |

---

## Aplicação estratégica

### Revisão trimestral
Com dashboard pronto, revisar:
- Top 20 famílias por rotatividade
- Top 20 SKUs dormentes
- % do capital empatado em estoque dormente

### Decisões derivadas
- **Expandir estoque** em famílias de alta rotatividade e margem boa
- **Reduzir** em famílias de baixa rotatividade
- **Descontinuar** famílias fora-de-padrão sem giro
- **Realocar** entre unidades se faz sentido

### Compras
Planejamento de compra alinhado com giro real, não intuição.

---

## Desafios de implementação

### 1. Não há arquivo único com estoque + RAF
Precisa juntar snapshot de estoque (Excel) com RAF.

### 2. Timing dos snapshots
Estoque em data D × RAF de D-90 a D. Precisa cuidado para não contar saídas após snapshot.

### 3. Família canônica em ambas fontes
Precisa aplicar a taxonomia **no momento de carregar cada fonte** para ter chave consistente.

### 4. Material de partida vs faturado
Estoque tem material "em estoque" (ABCMAT_*). RAF tem "faturado" (ABC*). Transformação precisa ser considerada.

---

## Roadmap

### Motor Analítico v1
- Painel de Estoque isolado (posição)
- RAF analisado separadamente

### Motor Analítico v2
- Cruzamento automatizado
- Dashboard "Giro Real por Família"
- Alertas de ruptura e obsolescência

---

## Conexões

- [[00 - Visão Geral Cruzamentos]]
- [[Sistema Operacional Comercial/03 Estoque/00 - Visão Geral Estoque]]
- [[Sistema Operacional Comercial/03 Estoque/01 - Família Canônica]]
- [[Sistema Operacional Comercial/03 Estoque/04 - Painel de Estoque v2]]
- [[Sistema Operacional Comercial/03 Estoque/05 - Movimentação e Giro]]
- [[Sistema Operacional Comercial/04 RAF/00 - Visão Geral RAF]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]
