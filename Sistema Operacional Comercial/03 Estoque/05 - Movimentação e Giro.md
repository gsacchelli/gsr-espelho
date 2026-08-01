---
tipo: análise-operacional
domínio: estoque
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [movimentação, giro, fluxo, kpi]
---

# 05 — Movimentação e Giro

## Conceitos

### Movimentação
Entradas e saídas de estoque em período. Revela **ritmo de rotação** do estoque.

### Giro
Mede quantas vezes o estoque "gira" (é consumido e reposto) no período.

```
Giro (vezes/ano) = Saídas no período × 12 / estoque médio no período

Giro (dias) = Estoque atual / Venda diária média
```

### Cobertura
Duração esperada do estoque ao ritmo de consumo atual.

```
Cobertura (dias) = Estoque atual / Venda diária média
```

---

## Por que importa

### Giro alto
- Capital de giro eficiente (pouco dinheiro preso)
- Menor risco de obsolescência
- **Porém:** risco de ruptura se ritmo da demanda varia

### Giro baixo
- Capital preso
- Custo de armazenagem
- Risco de obsolescência
- **Porém:** segurança (sempre tem em estoque)

### Ponto ótimo
Varia por família:
- **Alto giro (alta rotatividade):** 4140 redondo laminado faixa 1-2 — 30-60 dias
- **Giro médio:** aços beneficiamento — 60-90 dias
- **Baixo giro aceitável:** aços ferramenta, bitolas grandes — 90-180 dias

---

## KPIs de movimentação

### 1. Saídas por família (kg ou R$)
Volume de venda por família no período.

**Uso:** entender onde a receita vem. Famílias A (80% do volume) vs B (15%) vs C (5%).

### 2. Giro (em vezes)
```
Giro = 12 × (saídas mensais) / estoque médio
```

**Interpretação:**
- Giro > 12: estoque roda mais de 1×/mês — muito alto
- Giro 6-12: saudável para maioria
- Giro 3-6: atenção
- Giro < 3: investigar (obsolescência?)

### 3. Dias de estoque
```
Dias = 30 × estoque / saída mensal
```

**Alvo por família:**
- A (alta rotatividade): 30-60 dias
- B (média): 60-120 dias
- C (baixa): 120-180 dias

### 4. Itens sem movimento (dormentes)
Itens com **zero saída** em 90, 180, 365 dias.

**Ação:**
- 90 dias: flag amarela
- 180 dias: revisar (reduzir preço? descontinuar?)
- 365+ dias: obsolescência quase certa — decisão estratégica

### 5. Fluxo de caixa do estoque
Valor do estoque como % do faturamento anual. Ideal < 20%.

### 6. Ruptura (stockout)
Itens que zeraram durante o período.
- Pontual: normal (item acabou antes do reabastecimento)
- Recorrente: problema de planejamento

---

## Fluxo típico de saída

### Caminho normal
1. Cliente cota → pedido → pré-separação → faturamento → expedição → cliente
2. Saída no ERP no momento do faturamento (não expedição)
3. Estoque decrementa

### Exceções
- **Consignado:** estoque fica na AFS mas "comprometido" com cliente
- **Devolução:** entrada negativa (estoque incrementa)
- **Transferência entre unidades:** decrementa numa, incrementa em outra

---

## Aba Movimentação no Painel v2 (v1 em construção)

### Blocos propostos

#### Bloco 1 — Concentração (hero)
Top 20 famílias por saídas do mês (ou período selecionado).

#### Bloco 2 — Fluxo
Entradas vs Saídas por família, em gráfico de barras lado a lado.

Interpretação:
- Entradas >> Saídas: estoque crescendo (planejamento ou compra demais)
- Entradas ≈ Saídas: operação estável
- Entradas << Saídas: estoque diminuindo (consumindo estoque antigo ou quebra de planejamento)

#### Bloco 3 — Tendência agregada
Evolução temporal (últimos 12 meses) das saídas totais.
Identifica sazonalidade, tendência de crescimento/queda.

#### Bloco 4 — Saúde do estoque
Métricas:
- % do estoque em itens sem movimento > 180 dias
- Média de dias de estoque global
- # de SKUs "dormentes"
- # de rupturas no período

---

## Cruzamento com RAF

### Integração futura
Painel de Estoque hoje usa Excel de estoque (posição). Giro **real** calcula-se cruzando com RAF (saídas efetivas).

### Roadmap (Motor Analítico v2)
Gerar visão unificada:
```
Por família canônica:
- Estoque atual (Excel Estoque)
- Saídas últimos 12m (RAF)
- Giro (cálculo)
- Dias de cobertura (cálculo)
- Margem média (RAF)
- MC econômica (RAF)
```

Isso cria visão 360° por família — **estoque + venda + margem** em um lugar.

---

## Análises operacionais clássicas

### 1. Pareto 80/20
Top 20 famílias → 80% das vendas? (Normalmente sim). O que acontece nas outras 80%?

### 2. Bitolas dormentes
Bitolas fora do padrão típico (faixa 3-6) frequentemente giram devagar. Normal, mas monitorar para não virar obsolescência.

### 3. Sazonalidade
Alguns clientes/segmentos têm padrão (ex: construção civil aquece em X trimestre). Estoque deve acompanhar.

### 4. Correlação estoque × cotação
Item com cotação recorrente mas estoque zero = vendedor perde deals. Analisar cotações perdidas por "sem estoque" / "prazo de entrega".

### 5. Correlação estoque × margem
Item com estoque alto e margem baixa: possível indicação de que foi comprado caro demais ou que preço de venda caiu.

---

## Decisões estratégicas derivadas

### Descontinuar item
Critérios combinados:
- Giro < 3 vezes/ano
- Sem movimento > 180 dias
- Baixa concentração (< 0,5% do estoque por valor)
- Nenhum cliente estratégico dependente

Se todos verdadeiros: candidato forte a descontinuar.

### Reforçar estoque
Critérios:
- Giro > 12 vezes/ano
- Rupturas recentes
- Cotação perdida por "sem estoque"
- Família saudável em margem

### Mudar mix de compra
Se uma família cresce em saída e outra cai, realocar capital de giro:
- Reduzir compra do que cai
- Aumentar do que cresce

### Expandir em nova faixa
Se "Fora de Padrão" tem itens recorrentes, vale formalizar faixa nova (ver [[02 - Faixas de Bitola]]).

---

## Limitações de análise hoje

### 1. Sem série temporal automática
Cada snapshot é isolado. Precisa abrir múltiplos para ver tendência.

### 2. Giro real requer cruzamento
Só posição de estoque não dá giro — precisa das saídas do RAF.

### 3. Cobertura específica por SKU vs família
Média por família oculta que SKU específico pode estar zerando.

---

## Ações recomendadas (roadmap)

### Imediato (usar painel v2)
1. Revisão semanal da concentração
2. Lista de itens dormentes (> 180 dias) com decisão (manter, descontar, descontinuar)

### Curto prazo (Motor Analítico v2)
1. Cruzar estoque × RAF automaticamente
2. Giro por família calculado
3. Alertas de ruptura e obsolescência
4. Comparativo com trimestre anterior

### Médio prazo
1. Integração com sistema de compras
2. Forecast de demanda (previsão)
3. Sugestão automática de reposição (com aprovação manual)

---

## Conexões

- [[00 - Visão Geral Estoque]]
- [[01 - Família Canônica]]
- [[03 - ABC XYZ (futuro)]]
- [[04 - Painel de Estoque v2]]
- [[06 - Fora de Padrão]]
- [[04 RAF/00 - Visão Geral RAF]]
- [[01 Sistema de Dados/06 - Motor Analítico v1]]
- [[07 Cruzamentos e Previsões/02 - Estoque x RAF (giro real)]]
