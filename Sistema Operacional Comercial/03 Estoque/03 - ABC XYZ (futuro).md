---
tipo: framework-proposto
domínio: estoque
criado: 2026-04-17
última-revisão: 2026-04-17
status: proposto-não-implementado
tags: [abc-xyz, framework, futuro, giro, classificação]
---

# 03 — ABC / XYZ (Framework proposto — não implementado)

## Status

**Framework proposto, ainda não implementado.** Gustavo já indicou que "classificação ABC não existe hoje, fica para o futuro".

Esta nota documenta o framework para **quando for a hora de implementar** (provavelmente v2 do Motor Analítico ou Painel de Estoque).

---

## Conceitos

### Classificação ABC — Valor
**Foco:** quanto cada item representa em **valor do estoque** (ou venda).

| Classe | Critério típico | Característica |
|---|---|---|
| A | Top 20% dos itens → 80% do valor | Altíssima atenção |
| B | Próximos 30% → 15% do valor | Atenção média |
| C | Últimos 50% → 5% do valor | Atenção baixa (mas existem) |

### Classificação XYZ — Demanda / Previsibilidade
**Foco:** quão previsível é a demanda do item.

| Classe | Característica |
|---|---|
| X | Demanda estável, previsível (baixo desvio-padrão) |
| Y | Demanda variável, com padrão sazonal ou cíclico |
| Z | Demanda irregular, esporádica, imprevisível |

### Matriz ABC × XYZ
Combinação forma 9 quadrantes, cada um com **estratégia de estoque** diferente:

| | X (previsível) | Y (variável) | Z (esporádico) |
|---|---|---|---|
| **A (valor alto)** | AX — automatizar reposição | AY — gestão ativa, buffer | AZ — análise caso a caso |
| **B (valor médio)** | BX — reposição padrão | BY — acompanhar | BZ — JIT ou sob demanda |
| **C (valor baixo)** | CX — lote econômico | CY — revisão periódica | CZ — descontinuar? |

---

## Adaptação para Sacchelli

### Por SKU ou por família?
**Proposta:** começar por **família canônica** (não SKU). Razões:
- Famílias são mais estáveis que SKUs específicos
- Análise por família informa decisão estratégica (expandir/reduzir família)
- Por SKU vira ruído em portfolio de centenas

### Horizonte de análise
- **Valor (ABC):** rolling 12 meses
- **Previsibilidade (XYZ):** rolling 24 meses (para capturar sazonalidade)

### Fonte de dados
- **Estoque:** Excel de estoque
- **Venda:** RAF (faturamento real)
- **Consumo interno:** motor calcula giro

---

## Aplicação esperada (por quadrante)

### AX — Itens estratégicos, previsíveis
- Reposição automatizada (pedido recorrente de usina)
- Estoque mínimo garantido
- Exemplo provável: 4140 redondo laminado faixa 1-2

### AY — Itens estratégicos com variação
- Gestão ativa — S&OP mensal
- Buffer de segurança maior
- Exemplo provável: 8620 cementação redondo

### AZ — Itens estratégicos imprevisíveis
- Análise caso a caso
- Possivelmente sob encomenda (não estoque)
- Exemplo provável: aços ferramenta premium

### BX/BY — Gestão média
- Revisão trimestral
- Automatização parcial

### BZ/CZ — Candidatos a descontinuação
- Itens de baixo valor e imprevisíveis
- Questionar: mantemos ou deixamos sob encomenda?

### CX — Lote econômico
- Reposição em lote grande, baixa frequência
- Itens de prateleira

---

## Implementação proposta (Motor Analítico v2)

### Fase 1 — Cálculo ABC (valor)
```python
# Pseudo-código
def classificar_abc(df_vendas):
    df_valor = df_vendas.groupby('familia')['valor'].sum().sort_values(ascending=False)
    df_cumsum = df_valor.cumsum() / df_valor.sum()
    df_abc = df_cumsum.apply(lambda x: 'A' if x <= 0.80 else ('B' if x <= 0.95 else 'C'))
    return df_abc
```

### Fase 2 — Cálculo XYZ (coefic. de variação)
```python
def classificar_xyz(df_vendas, periodos=24):
    # Agrupar por mês para cada família
    mensal = df_vendas.groupby(['familia', 'mes'])['quantidade'].sum()
    cv = mensal.groupby('familia').std() / mensal.groupby('familia').mean()
    df_xyz = cv.apply(lambda x: 'X' if x <= 0.25 else ('Y' if x <= 0.75 else 'Z'))
    return df_xyz
```

### Fase 3 — Matriz 9 quadrantes
Cruzar ABC × XYZ, exibir heatmap com # de famílias em cada quadrante.

### Fase 4 — Recomendações automáticas
Para cada família, sugerir estratégia baseada no quadrante (mais regra que inteligência no início).

---

## Critérios de implementação

### Quando faz sentido implementar
- Motor Analítico v1 estável
- Série temporal de 24+ meses disponível
- Gustavo ou time com tempo para revisar categorização inicial

### Quando NÃO vale a pena
- Se portfolio tem < 50 famílias (pouca diferenciação entre A/B/C)
- Se demanda muda muito (mercado em transformação — classificação fica obsoleta rápido)
- Se não há capacidade de agir sobre a categorização (framework sem ação é decorativo)

---

## Riscos conhecidos

### Falso positivo — item AZ subestimado
Item classificado como "estratégico mas imprevisível" pode estar recebendo demanda **sazonal** que parece aleatória. Análise de 24 meses mitiga.

### Falso negativo — item CZ descontinuado equivocadamente
Item pouco girado pode ser **estratégico para cliente específico**. Descontinuar sem considerar relação com cliente = perder cliente.

### Mudança de classificação frequente
Se item pula entre A/B ou X/Y a cada trimestre, classificação é instável. Ações baseadas nela ficam inconsistentes.

**Mitigação:** classificar **trimestralmente**, não mensalmente. Transição suave.

---

## Benchmark vs concorrência

**Trefita/Torres:** não temos inteligência sobre o ABC/XYZ deles, mas grupos grandes geralmente usam esse framework. Se AFS não usar, pode estar em desvantagem analítica.

**Gerdau / Usinas:** produzem, não distribuem — framework ABC/XYZ de forma diferente (foco em produção, não estoque final).

---

## Conexões

- [[00 - Visão Geral Estoque]]
- [[01 - Família Canônica]]
- [[04 - Painel de Estoque v2]]
- [[05 - Movimentação e Giro]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]
