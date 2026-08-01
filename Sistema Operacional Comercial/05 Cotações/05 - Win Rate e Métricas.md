---
tipo: métricas
domínio: cotações
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [win-rate, métricas, conversão, kpi]
---

# 05 — Win Rate e Métricas

## Métricas principais

### Win Rate (taxa de conversão)

**Fórmula:**
```
Win Rate = Cotações Ganhas / (Ganhas + Perdidas reais)
```

**Atenção:** excluir do denominador as cotações encerradas como "orçamento prévio" — são cotações **que nunca iam fechar**. Incluir distorce para baixo.

**Valor observado (jan-fev/2026):** **67,6%** (cotações acionáveis)

### Ticket médio
```
Ticket médio = Σ valor de cotações ganhas / # cotações ganhas
```

### Ciclo médio
```
Ciclo = Data_pedido - Data_cotação (em dias)
```

Relevante para previsibilidade de fechamento.

### Taxa de ganho por preço
```
% perda por preço = Perdidas por preço / Total perdidas
```

### Concorrente nomeado em perdas por preço
```
% nomeado = Perdas por preço com concorrente nomeado / Total perdas por preço
```

Observado (jan-fev): apenas **47%** dos "perdidos por preço" têm concorrente nomeado.

---

## Análise segmentada (jan-fev/2026)

### Por vendedor

**Top performers:**
| Vendedor | Win Rate |
|---|---|
| Alam | 94,1% |
| Aline-CXJ | 92,5% |
| Açotec-SCA | 91,4% |

**Baixa performance em preço (Piracicaba):**
| Vendedor | Taxa perda por preço |
|---|---|
| Fabiola | 50% |
| Juliana-PIR | 47,6% |
| Marcos Lemes | 41,3% |

**Leitura:** todos operam com as mesmas tabelas, mesmos produtos. Diferença está em **processo comercial**, não preço estrutural.

### Por região
- PIR: região-problema (perda por preço elevada)
- CXS: handicap logístico (14 clientes perdidos para Trefita)
- Outras unidades SP: conversão saudável

### Por concorrente
- **Trefita/Torres:** R$9,35M perdidos (principal)
- Gerdau direto: significativo em clientes grandes
- Outros: distribuídos

---

## Diagnóstico crítico

### Diferença preço ganhas vs perdidas

- Cotações **ganhas:** preço médio **+3,0% sobre Tab Vermelha**
- Cotações **perdidas por preço:** preço médio **+1,1% sobre Tab Vermelha**
- **Diferença: ~2 p.p.**

### Interpretação
Não é um abismo. Se fosse preço mesmo, gap seria maior. Provável: **parte das "perdas por preço" não é realmente preço** — é outro motivo (relacionamento, prazo, serviço, processo comercial).

### Implicação
Descontar mais 3-5% "para ganhar" cotações perdidas por preço **não vai resolver**. Processo comercial resolve.

---

## Vantagem estrutural (descoberta)

Sacchelli tem **vantagem estrutural de custo vs concorrentes supridos por Gerdau**:
- **28% menor** em aços carbono
- Possível explicação: importação direta otimizada

**Implicação:** onde AFS perde para Gerdau-supplied, não é custo de aço. É:
- Processo comercial
- Relacionamento
- Logística local
- Serviço

Alavanca de ganho: atacar esses eixos, não cortar preço.

---

## Dashboard ideal (Motor Analítico v2)

### Tela 1 — Win Rate geral
- Taxa global
- Por vendedor (ranking)
- Por região
- Evolução temporal (últimos 12 meses)

### Tela 2 — Perdas detalhadas
- Motivo de perda (distribuição)
- Perdas por preço com/sem concorrente nomeado
- Top concorrentes

### Tela 3 — Projetos em andamento (ver [[03 - Orçamento Prévio vs Projeto Real]])
- Pipeline de projeto
- Idade (dias parados)
- Próxima ação sugerida

### Tela 4 — Cliente-tabelista
- Lista automatizada
- Tempo economizado pelo industrializado

### Tela 5 — Vendedores para conversa cirúrgica
- Combinação perigosa: volume alto × MC baixa × prazo longo
- Piracicaba em destaque (abr/2026)

---

## Metas vs realizado

Sem histórico formal de metas de win rate no sistema atual. Recomendação:

### Metas propostas (baseline)
- **Win Rate geral (acionável):** ≥65%
- **Win Rate em clientes-âncora:** ≥80%
- **% perda por preço sem concorrente nomeado:** <20%
- **% projetos com follow-up ativo (> 30 dias):** <20% (quanto menor, melhor)

### Revisão trimestral
Ajustar metas com base em evolução.

---

## Conexões

- [[00 - Visão Geral Cotações]]
- [[02 - Motivos de Encerramento]]
- [[03 - Orçamento Prévio vs Projeto Real]]
- [[04 - Cliente-Tabelista (flag proposta)]]
- [[01 Sistema de Dados/06 - Motor Analítico v1]]
- [[04 RAF/06 - Despesas Logísticas por Unidade]] (CXS, Trefita)
