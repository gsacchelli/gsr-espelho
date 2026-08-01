---
tipo: ferramenta-arquitetura
domínio: estoque
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [painel, estoque, v2, html, padrão-canônico]
---

# 04 — Painel de Estoque v2

## Status

**Em uso — padrão canônico para novos dashboards.**

Versão atual: **v2**. Outras versões anteriores (v1, Painel_Comercial_AFS_v1-v4 relacionados) estão em divergência de padrão — trazer ao padrão v2 quando houver tempo.

---

## Arquivos

- `Painel_Estoque_Sacchelli_v2.html` — versão v2 (atual)
- `Estoque_Sacchelli_YYYY-MM-DD.html` — snapshots datados gerados
- Backups anteriores conforme convenção em [[Sistema Operacional Comercial/01 Sistema de Dados/02 - Arquivos Brutos e Convenções]]

---

## Propósito

Dashboard **self-contained** que transforma o export de estoque do Softcomp + Critérios_planilhas em visão estruturada para decisão operacional.

---

## Arquitetura

### Stack
- **HTML + JS + CSS** embutidos (self-contained)
- **Sem dependências externas** (nem Tailwind CDN — estilo inline)
- **Config embutido:** taxonomia de família + critérios de região

### Padrão canônico (replicar em novos dashboards)
- Estrutura HTML → style → data → layout → script
- Organização JS: const → util → motor → render → listeners → init
- Print A4 landscape
- localStorage para estado de usuário (filtros, etc.)

---

## Capacidades atuais (v2)

### Visão macro
- **Concentração de estoque** por família canônica
- Pareto: top 20 famílias + acumulado
- Métrica principal atual: **peso (kg)**. v2 futura: métrica R$.

### Drill-down
- Click na família → abre lista de SKUs
- SKUs ordenados por peso ou valor
- Info: bitola, comprimento, valor, dias parado

### Blocos v1 da aba Movimentação (em construção)
- **Concentração (hero)**
- **Fluxo** (entradas vs saídas)
- **Tendência agregada**
- **Saúde do estoque** (giro, obsolescência)

### Higiene
- "Fora de Padrão" aparece em seção própria
- Alertas de SKUs sem movimento > 180 dias

---

## Dados consumidos

### Input
1. **Excel de estoque** — snapshot do Softcomp (convenção `Estoque_YYYYMMDD.xlsx`)
2. **Critérios_planilhas.xlsx** — taxonomia, cidades, grupos (ver [[01 - Família Canônica]])

### Processamento
- Aplica família canônica a cada SKU
- Aplica override de cidade se aplicável
- Calcula métricas agregadas

### Output
- Dashboard HTML visualizável imediatamente

---

## Estrutura do HTML

### Seções principais
```
Painel_Estoque_Sacchelli_v2.html
├── <head>
│   ├── meta tags
│   └── <style> com CSS embutido
├── <body>
│   ├── Header (título + data do snapshot)
│   ├── Filtros (unidade, família, etc.)
│   ├── KPIs hero (peso total, valor total, giro médio)
│   ├── Pareto de concentração
│   ├── Aba Movimentação (v1 em construção)
│   │   ├── Concentração
│   │   ├── Fluxo
│   │   ├── Tendência
│   │   └── Saúde
│   ├── Fora de Padrão
│   └── Drill-down modal
└── <script> com JS embutido
```

### Organização JS (padrão canônico)
```javascript
// 1. Config
const FAIXAS_BITOLA = [...];
const FAMILIAS_PADRAO = [...];
const CIDADES_OVERRIDE = {...};

// 2. Utilitários
function formatarNumero(n) { ... }
function calcularDiasParado(dt) { ... }

// 3. Motor (processamento)
function processarEstoque(rawData) {
  // aplica família canônica
  // aplica override cidade
  // calcula métricas
}

// 4. Renderização
function renderKPIs(data) { ... }
function renderPareto(data) { ... }
function renderDrilldown(familia) { ... }

// 5. Listeners
document.querySelector('[data-family]').addEventListener('click', ...);

// 6. Inicialização
(function init() {
  const data = processarEstoque(DADOS_RAW);
  renderKPIs(data);
  renderPareto(data);
})();
```

---

## Padrão visual (referência canônica)

### Cores semáforo
- **Verde:** saudável (giro bom, concentração adequada)
- **Amarelo:** atenção (giro abaixo de padrão, concentração começa a preocupar)
- **Vermelho:** crítico (sem movimento 180+d, concentração excessiva)

### Layout
- Grid CSS de 2-3 colunas no desktop
- Responsivo (1 coluna em mobile)
- Hero metric bem visível
- Pareto com acumulada em linha

### Tipografia
- Sans-serif legível (padrão browser)
- Números grandes para métricas
- Contraste alto para acessibilidade

### Interação
- Hover mostra tooltip com detalhe
- Click abre drill-down
- ESC fecha modal
- Ctrl+P sempre funcional (@media print)

---

## Padrão replicável (do v2 para novos dashboards)

Ao criar novo painel (ex: Pedidos, Cotações), **seguir esta estrutura exata**:

1. Self-contained HTML
2. Config embutido (não arquivo externo)
3. Taxonomia canônica compartilhada
4. 3 cores semáforo
5. Hero + Pareto + Drill-down
6. Print otimizado
7. localStorage para filtros se aplicável

Ver [[Sistema Operacional Comercial/01 Sistema de Dados/05 - Padrões de Desenvolvimento]] para checklist completo.

---

## Roadmap

### v2 em curso
- [x] Aba Concentração
- [x] Família canônica aplicada
- [x] Fora de Padrão separado
- [x] Drill-down
- [ ] Aba Movimentação v1 (em construção)
- [ ] Export para Excel do drill-down

### v3 (planejada)
- [ ] Métrica R$ ao invés de só kg (usar arquivo alternativo com preço de venda — simpler que puxar do RAF)
- [ ] ABC/XYZ por família (ver [[03 - ABC XYZ (futuro)]])
- [ ] Integração com RAF para giro real (kg vendidos por família × estoque atual)
- [ ] Comparativo com trimestre anterior

### v4 (ideal, mais longe)
- [ ] Integração com Motor Analítico (feedback loop)
- [ ] Sugestão automática de ações (descontinuar X, reforçar Y)
- [ ] Alertas proativos (item vai zerar em 15 dias)

---

## Integração com Softcomp

### Hoje
- Export manual do Softcomp → Excel
- Dashboard gerado a partir do Excel
- Frequência: semanal (ideal) / mensal (atual)

### Futuro (Motor Analítico v2)
- Dashboard gerado automaticamente por script Python ao receber bruto
- Conexão SQL direto (via VPN) possível no futuro

---

## Limitações conhecidas

### 1. Valor R$ depende de arquivo alternativo
Métrica R$ não sai diretamente do Excel de estoque padrão. Precisa cruzar com arquivo alternativo (ou RAF — mais trabalhoso).

### 2. Sem série temporal
Cada snapshot é isolado. Comparar com mês anterior requer abrir 2 arquivos.

### 3. Sem alertas automáticos
Dashboard mostra estado atual. Mudanças críticas (item zerando, fora de padrão aumentando) precisam ser pegas pela revisão visual.

---

## Conexões

- [[00 - Visão Geral Estoque]]
- [[01 - Família Canônica]]
- [[02 - Faixas de Bitola]]
- [[03 - ABC XYZ (futuro)]]
- [[05 - Movimentação e Giro]]
- [[06 - Fora de Padrão]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/05 - Padrões de Desenvolvimento]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]
