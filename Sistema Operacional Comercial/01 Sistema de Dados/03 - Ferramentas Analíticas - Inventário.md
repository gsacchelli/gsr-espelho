---
tipo: inventário
domínio: sistema-de-dados
criado: 2026-04-17
última-revisão: 2026-07-17
tags: [ferramentas, inventário, simulador, painel, motor]
---

# 03 — Ferramentas Analíticas — Inventário

## Ferramentas em produção (em uso ativo)

### 0. Cockpit de Cotações Pendentes (criado 17/07/2026)
- **Arquivo:** `03_Ferramentas/Cockpit_Cotacoes.html` (template versionado) + `cockpit_data.js` (gerado, gitignored)
- **Status:** v2.0 — auditado por 3 agentes (dados/lógica/design) no dia do lançamento
- **Tecnologia:** HTML self-contained (vanilla JS, sem dependências); dados via `make cockpit` (lê o gold DuckDB); encadeado no `make atualizar-cotacoes-pendentes`; botão na sidebar do Portal SAC360
- **Log canônico:** `GSR/Logs/2026-07-17 — Cockpit de Cotações Pendentes (score de fechamento + triagem diária).md`

**Capacidades:**
- Score de chance de fechamento por item (log-odds com shrinkage; histórico 2025+ em disputa real; cliente por CÓDIGO; peso do cliente calibrado por backtest) com breakdown "×N nas chances" visível
- EV (score × valor) como régua de priorização; Dashboard gerencial; Triagem com 4 grupos de facetas + busca; Pacotes; Foco do dia (top 20 EV sem ação)
- Matriz material aço × faixa de bitola (pendente × estoque físico, células clicáveis)
- Drawer-esteira (j/k): ladder de preço F1/F2/F3 com últ. ganho do cliente e mediana da região; estoque da bitola + partida INDICATIVA p/ acabamentos produzidos; conversões cliente/família/cliente×família; histórico do código
- Notas qualitativas (temperatura, target, concorrente, próxima ação) em localStorage + sync opcional com `cockpit_notas.json` (File System Access, merge por timestamp)
- Export de recorte com validade (AES-GCM amarrado à data; sem a mecânica do score) pra mandar a gerentes

**Pendências:**
- Recalibração do score AGENDADA (tarefa local 15/09/2026 — componente de tamanho do item, banda 20–35%)
- Decisão Gustavo: levar "partida" pra regra NEGAR da triagem canônica (vw_cotacoes_pendentes)

### 1. Simulador de Precificação HTML
- **Arquivo:** `Analise_Precificacao_Sacchelli.html`
- **Status:** Entrega 1 (multi-item rail) validada em 2026-04-15
- **Tamanho:** ~5.300 linhas
- **Tecnologia:** HTML self-contained (JS + CSS embutidos, sem dependências externas)
- **Backup:** `Analise_Precificacao_Sacchelli.bak-pre-pacote-20260415-025719.html`
- **Nota técnica:** [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]]

**Capacidades:**
- DRE com MC1/MC2, composição do resultado, KPIs
- Comparativo por unidade (GRU, SCA, PIR, RIP, CXJ)
- Modos R$/Kg, R$/Pç, R$/m (ver [[Sistema Operacional Comercial/02 Precificação/05 - Modos de Venda]])
- Spreads de Lâmina e Tolerância (Real vs Softcomp)
- VPP informativo com hint EN 10060 / Metals
- Print A4 landscape otimizado
- Multi-item (Entrega 1) com rail + snapshot/restore + localStorage

**Pendências:**
- Entrega 2 — Modo Pacote (DRE blended, custo de servir do pedido, Give/Get visual)
- Entrega 3 — Impressão comprimida multi-item + versionamento v1/v2/v3

### 2. Painel de Estoque HTML (v2)
- **Arquivo:** `Painel_Estoque_Sacchelli_v2.html` (versão atualizada)
- **Status:** em uso, **padrão canônico para novos dashboards**
- **Tecnologia:** HTML self-contained
- **Fonte de dados:** Excel de estoque + Critérios_planilhas
- **Nota técnica:** [[Sistema Operacional Comercial/03 Estoque/04 - Painel de Estoque v2]]

**Capacidades:**
- Concentração de estoque por família
- Movimentação (em construção — aba Movimentação v1)
- Saúde do estoque (fluxo + tendência)
- Drill-down por SKU
- Taxonomia família canônica embutida

### 3. Motor Analítico Sacchelli v1
- **Localização:** `MotorAnalitico/` (Python)
- **Status:** arquitetura aprovada (Motor_Analitico_v1_Arquitetura.md), em codificação
- **Tecnologia:** Python local + HTML dashboard gerado
- **Sem SaaS, dados não saem da máquina**
- **Nota técnica:** [[06 - Motor Analítico v1]]

**Capacidades (planejadas):**
- Ingestão automática RAF + cotações + critérios
- 14+ visões já implementadas incluindo MC% real, corredor de MC
- Dashboard HTML semanal
- Cruzamentos entre domínios

**Próximo passo:** codificação Fase 1, baseada em doc de arquitetura validado.

---

## Ferramentas em desenvolvimento / PRD

### 4. Simulador Web App
- **Status:** PRD concluído (`PRD_Simulador_Precificacao_Web.docx`), implementação em pausa
- **Objetivo:** multi-usuário (5 users), proteção de inteligência comercial
- **Stack definida:** Node.js 20 + Express + React 18 + Vite + Tailwind + SQLite (better-sqlite3)
- **Auth:** JWT + bcrypt
- **Deploy:** VM Sacchelli + Nginx + HTTPS
- **Sync:** SQL espelho Softcomp → SQLite (cron 6h)
- **Motor de cálculo:** 9 módulos JS (pricing-engine, cost, cut, process, vpp, spread, tax, dre-builder, kpi-builder)
- **Nota técnica:** [[Sistema Operacional Comercial/02 Precificação/09 - Simulador Web App (futuro)]]

**Razão da pausa:** prioridade estratégica (Duferco-Brasil) + custo/benefício do HTML atual vs. overhead do web app.

### 5. Painel Comercial de Cotações
- **Status:** F1+F2 fechadas (08/05/2026), F3+F4 pendentes
- **Escopo:** Cotações Encerradas + Pendentes em painel único
- **Motor:** `MotorAnalitico/cotacoes/` — 55/55 testes verde
- **Output atual (F2):** `02_Derivados/Cotacoes/Cotacoes{Encerradas,Pendentes}_enriquecido.xlsx` com 67 colunas (chave, datas, família, tipo_item, gap F1/F2/F3, faixa atingida, motivo agrupado, concorrente nomeado, pedido_id, match estoque)
- **Throughput:** 1.585 linhas/s via xlsxwriter — 62k linhas em 40s
- **Match estoque:** 96% dos itens catalogados (exato + tolerância)
- **Cross-check RAF:** pedido_id extraído em 100% das Ganhou (23.048 cotações), pronto para F3
- **Output final (F4):** painel HTML 5 abas (Pipeline / Win Rate / Perdas / Item×Estoque×Vermelha / Tabelistas & Projetos)
- **PRD:** `Planejamento Estratégico - Comercial/06_Docs/PRD_Painel_Cotacoes.md`
- **Log F1+F2:** [[Logs/2026-05-08 — Painel Cotacoes F1+F2 (esqueleto motor + match estoque)]]

### 6. Análise de Pedidos Emitidos
- **Status:** em construção
- **Objetivo:** do pedido ao faturamento, ciclo, status, anomalias
- **Nota técnica:** [[Sistema Operacional Comercial/06 Pedidos/00 - Visão Geral Pedidos]]

---

## Ferramentas históricas / ad-hoc

### 7. Campanha 60 anos — Dashboard
- **Arquivo:** `Campanha_60anos_Dashboard.html`, `Campanha_60anos_Analise_Precificacao.xlsx`
- **Status:** concluído, histórico

### 8. Análise Financeira Acovisa 2025
- **Arquivo:** `Analise_Financeira_Acovisa_2025.pptx`
- **Status:** concluído, histórico

### 9. Diagnóstico de Concentração (abr/2026)
- **Arquivo:** `Diagnostico_Concentracao_2026-04-13.xlsx`
- **Status:** análise pontual

### 10. Diagnóstico de Precificação Sacchelli (mar/2026)
- **Arquivo:** `Diagnostico_Precificacao_Sacchelli.html`
- **Status:** referência histórica
- **Contém:** análise 29.748 cotações Jan-Fev/2026, benchmark Gerdau

### 11. Painel Comercial AFS (v1-v4)
- **Arquivos:** `Painel_Comercial_AFS.html`, `_v2.html`, `_v3.html`, `_v4.html`
- **Status:** evolução histórica
- **Observação:** versões antigas podem estar desatualizadas — **priorizar última versão**

---

## Padrão para novas ferramentas

Quando criar ferramenta nova, seguir padrões documentados em [[05 - Padrões de Desenvolvimento]].

Síntese do padrão atual (baseado em Estoque v2 + Simulador Precificação):

| Aspecto | Padrão |
|---|---|
| Formato de saída | HTML self-contained (preferencial) ou Python + HTML |
| Dependências | Sem CDN externa (reduzir quebra), Tailwind só se inline |
| Taxonomia de produto | Família canônica embutida ([[Sistema Operacional Comercial/03 Estoque/01 - Família Canônica]]) |
| Fonte de dados | Arquivo bruto do Softcomp (nomeado conforme [[02 - Arquivos Brutos e Convenções]]) |
| Persistência de estado | localStorage quando aplicável |
| Print | A4 landscape, 1-2 páginas |
| Confidencialidade | Sem serviços externos que exportem dados |

---

## Dependências entre ferramentas

```
Simulador (preço de venda) ────┐
                                │
Painel Estoque (disponibilidade)┼─► Decisão comercial
                                │
Motor Analítico (RAF análise) ──┘
                                │
                                ▼
                          Log de Decisões
                          (vault estratégico)
```

**Cruzamentos existentes (implementados):**
- Simulador usa taxonomia de família do Painel Estoque
- Motor Analítico consome mesma família

**Cruzamentos futuros (ver domínio 07):**
- Simulador usa preço de custo atualizado do RAF
- Painel Estoque cruza com vendas RAF para giro
- Motor consolida todos em forecast

---

## Conexões

- [[00 - Arquitetura de Dados]]
- [[05 - Padrões de Desenvolvimento]]
- [[06 - Motor Analítico v1]]
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]]
- [[Sistema Operacional Comercial/03 Estoque/04 - Painel de Estoque v2]]
- [[Sistema Operacional Comercial/07 Cruzamentos e Previsões/00 - Visão Geral Cruzamentos]]
