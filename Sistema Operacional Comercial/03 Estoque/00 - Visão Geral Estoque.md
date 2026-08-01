---
tipo: overview
domínio: estoque
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [estoque, overview, família, giro, portfolio]
---

# 00 — Visão Geral Estoque

## Propósito do domínio

Documenta a **lógica e ferramentas de gestão de estoque** — taxonomia de produto (família canônica), análise de giro, saúde de portfolio, painel operacional.

Estoque é o **ativo mais caro** da AFS no balanço. Gestão de estoque eficiente = margem preservada + capital liberado.

---

## Princípios centrais

### 1. Família canônica é a chave de análise
Qualquer agregação de estoque, cotação, pedido ou faturamento usa a mesma taxonomia: **Aço + Tipo + Perfil + Acabamento + Faixa de Bitola**.

Ver [[01 - Família Canônica]].

### 2. Estoque parado destrói valor
Item com baixo giro consome:
- Capital de giro
- Espaço físico (custo de armazenagem)
- Atenção operacional
- Risco de obsolescência

### 3. Mix de estoque reflete estratégia
O que está em estoque é decisão estratégica (comprar ou não comprar). Gap entre estoque e demanda = problema de carteira ou problema de compra.

### 4. Fora de Padrão é higiene, não exceção
Itens fora das famílias canônicas existem (engenheirados, customizados, compras pontuais). Rastreá-los é crítico para saúde de portfolio.

---

## Notas neste domínio

| # | Nota | Descrição |
|---|---|---|
| 00 | [[00 - Visão Geral Estoque]] | Este mapa |
| 01 | [[01 - Família Canônica]] | Taxonomia oficial de 207 combinações |
| 02 | [[02 - Faixas de Bitola]] | Tabela de faixas S/N e gestão |
| 03 | [[03 - ABC XYZ (futuro)]] | Framework proposto para v2 |
| 04 | [[04 - Painel de Estoque v2]] | Ferramenta canônica |
| 05 | [[05 - Movimentação e Giro]] | Análise de fluxo |
| 06 | [[06 - Fora de Padrão]] | Higiene de portfolio |

---

## Como o estoque alimenta outros domínios

```
     ┌───────────────────────┐
     │ Estoque (03)          │
     │ Família Canônica      │
     │ Posição + movimento   │
     └─────────┬─────────────┘
               │
        ┌──────┴──────┐
        ▼              ▼
 ┌────────────┐  ┌────────────────┐
 │ Cotações   │  │ Precificação   │
 │ (disponib.)│  │ (custo ponder.)│
 └─────┬──────┘  └───────┬────────┘
       │                 │
       └────┬────────────┘
            ▼
     ┌─────────────┐
     │ Pedidos (06)│
     │ (confirmar  │
     │  estoque)   │
     └─────┬───────┘
           │
           ▼
     ┌───────────┐
     │ RAF (04)  │
     │ Consumo   │
     └───────────┘
```

---

## Ferramentas principais

### Painel de Estoque HTML (v2) — padrão canônico
- **Arquivo:** `Painel_Estoque_Sacchelli_v2.html`
- **Status:** em uso
- Ver [[04 - Painel de Estoque v2]]

### Motor Analítico
- Consome mesma taxonomia de família
- Cruza com RAF para giro real
- Ver [[01 Sistema de Dados/06 - Motor Analítico v1]]

### Excel alternativo
- Gustavo tem arquivo alternativo com toda movimentação + preço de venda (mais simples que puxar do RAF)
- Util para v2 futura do painel (métrica R$ ao invés de só kg)

---

## Métricas-chave

| Métrica | Definição | Uso |
|---|---|---|
| Giro (dias) | Estoque / venda diária média | Saúde item individual |
| Pareto de concentração | % do estoque em top 20 famílias | Visão macro |
| Cobertura | Estoque / venda média × 30 | Planejamento de compra |
| Obsolescência | Itens sem movimento > 180d | Limpeza de portfolio |
| Giro por família | Giro agregado por taxonomia | Decisão estratégica família |
| % fora de padrão | Valor/peso não enquadrado | Higiene portfolio |

---

## Unidades AFS e estoque

| Unidade | % do estoque total (approx) | Característica |
|---|---|---|
| CD São Paulo + Guarulhos (GRU) | ~90% | Core — receber importação SFS → SP |
| São Carlos (SCA) | ~5% | Reabastecido de SP |
| Piracicaba (PIR) | ~3% | Reabastecido de SP |
| Rio Preto (RIP) | <1% | Reabastecido de SP |
| Caxias do Sul (CXS) | ~2% | Cadeia de 3 pernas (SFS→SP→CXS) |

Ver `project_afs_estrutura_logistica` (memória).

---

## Parâmetros operacionais

### Fora de Padrão
- Bitolas que não entram nas 6 faixas canônicas
- Ligas não mapeadas (aço fora da lista)
- Engenheirados (material com especificação específica de cliente)

### Giro-alvo
- Aços de alta rotatividade (4140 redondo laminado): 60-90 dias
- Aços especiais (cementáveis): 90-120 dias
- Aços ferramenta: 180+ dias aceitável se valor agregado alto

### Níveis de estoque
- **Mínimo:** cobertura para não quebrar (evitar rupture)
- **Ideal:** cobertura que otimiza margem e capital
- **Máximo:** trigger para não comprar mais

---

## Riscos conhecidos

### Handicap CXS
Importação chega em SFS → transferida para SP → transferida para CXS → clientes.
- 3 pernas logísticas
- 5,65% de despesa logística (vs 1,54% em GRU)
- Concorrentes têm 1-2 pernas

Afeta decisão de quanto estoque manter em CXS vs. reabastecer rápido de SP.

### Fora de Padrão invisível
Material engenheirado acumula se cliente original cancela compra. Se não visível no painel, vira obsolescência silenciosa.

### Taxonomia desatualizada
Se surge novo aço/acabamento que não entra nas 207 combinações, vira "Fora de Padrão" até família ser atualizada. Revisão periódica importante.

---

## Conexões estratégicas

- Vault estratégico: [[Cadeia de Valor]] (estoque é elo crítico)
- Vault estratégico: [[Vantagem Competitiva]] (estoque bem gerido = diferencial)
- Simulador: usa preço médio do estoque como input

---

## Conexões

- [[01 - Família Canônica]]
- [[02 - Faixas de Bitola]]
- [[04 - Painel de Estoque v2]]
- [[05 - Movimentação e Giro]]
- [[06 - Fora de Padrão]]
- [[01 Sistema de Dados/06 - Motor Analítico v1]]
- [[04 RAF/00 - Visão Geral RAF]]
