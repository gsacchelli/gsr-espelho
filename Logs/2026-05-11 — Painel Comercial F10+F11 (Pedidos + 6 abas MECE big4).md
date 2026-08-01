---
data: 2026-05-11
tipo: log
status: vigente
---
# 2026-05-11 — Painel Comercial F10+F11

## TL;DR

Sessão grande. Em ~1 dia entreguei:

1. **Motor de Pedidos Emitidos** (espelha estrutura RAF/Cotações): enriquecedor, cross-check com cotação Ganhou, aggregator com 8+ cubos OLAP, comando único `--pedidos-all`.
2. **Histórico 2025** importado (73.594 itens / R$ 547,2 MM). Pipeline multi-ano: glob `PedidosEmitidos*.xlsx` consolida tudo num único derivado.
3. **Redesign completo do Painel Comercial** em **6 abas MECE big4**: Executive Summary · Funil Comercial · Performance · Carteira de Clientes · Mix & Pricing · Análise Livre. 4 abas legacy (Dashboard, Cotações Encerradas, Pendentes, Pedidos) aposentadas.
4. **KPI bar global sticky** + breadcrumb de filtros + drill-by-click padronizado.
5. **Glossário PT/EN big4** com 28 termos canônicos.

Painel hoje: **5.485 linhas HTML**, smoke OK, schema PED v3 com 8 cubos.

---

## Arquitetura final do painel (6 abas MECE)

| Aba | Pergunta que responde | Audiência |
|---|---|---|
| **Executive Summary** | Como estamos vs plano e período anterior? | Board / Wagner |
| **Funil Comercial** | Onde estamos perdendo conversão? | Gerência |
| **Performance** | Quem está performando? | Gerência |
| **Carteira de Clientes** | Quem compra, quem deixou, quem cresceu? | KAM / semanal |
| **Mix & Pricing** | Que material vendemos e a que preço? | Comercial + Compras |
| **Análise Livre** | Quero cruzar X com Y filtrando Z (pivot ad-hoc) | Diretor |

Princípio MECE: cada aba tem **sujeito gramatical único** (resultado, funil, pessoa, cliente, produto, ad-hoc). Conversão Real / Pedidos Cold / Tabelistas / Stoplight viraram **lentes dentro do Funil** e da **Performance**, não abas próprias.

### Componentes únicos de cada aba

**Executive Summary** (board-ready):
- 4 Big KPI cards com Δ YoY destacado
- **Variance Bridge YoY** (waterfall McKinsey: Volume Effect + Price Effect + Mix/Outros)
- Heatmap Unidade × Mês
- Top 10 alertas automáticos (regras: %Preta ≥30% crítico, vendedor com >R$500k em ≥35% Preta, cliente premium 60-90d sem comprar, %cold ≥15%)
- Bullet chart real vs run-rate anualizado (benchmark = ano cheio anterior)
- Tendência semanal (últimas 26 semanas ISO)
- Síntese executiva em 5 linhas (texto pronto pra ata)

**Funil Comercial:**
- Funil visual 4 estágios: Cotação Emitida → Ganhou (declarada) → Pedido Emitido → NF Faturada* (roadmap)
- Leakage rate em cada transição
- 3 cards de resumo dos estágios (Pendentes · Encerradas · Pedidos)
- Motivos de perda + Top concorrentes
- **Velocidade de conversão** (Sales Cycle médio por unidade)
- **Pipeline Coverage Ratio** (pipeline aberto ÷ run-rate mensal, ideal ≥3×)

**Performance Comercial:**
- Leaderboard com 3 toggles (vendedor/gerência/unidade) e 6 critérios de sort
- **Heatmap Vendedor × Família** (cor = R$/kg)
- **Heatmap Vendedor × Faixa** (cores das faixas, intensidade = % R$ por faixa)
- Status emoji semáforo por vendedor

**Carteira de Clientes:**
- **Curva ABC** (Pareto: A=80%, B=15%, C=5%) com chart bar + linha cumulativa
- **Customer Concentration** (top 10/20/50/100 + HHI)
- **Cohort de retenção** (heatmap mensal: safra × M0..Mn)
- **Em risco** (60-90d) · **Churn** (>90d, era ativo)
- **Cross-sell** (histograma + top clientes baixo cross-sell)
- Tabela mestre 1.664 clientes paginados

**Mix & Pricing:**
- **Treemap squarified** (Aço → Perfil → Acab → Família, tamanho R$ + cor R$/kg)
- **Heatmap Aço × Faixa de Bitola** (cor = R$/kg médio)
- **Pocket Price Waterfall padrão McKinsey** (6 níveis: F1 → F2 → F3 → PU cotação → PU pedido → Pocket Price)
- Stacked bar 100% mix de faixa por unidade
- Mix com vs sem corte (premium de serviço)
- Tabela mestre por família canônica (top 60)

**Análise Livre (Pivot Builder):**
- 8 dimensões (Ano, Mês, Unidade, Gerência, Vendedor, Família, Faixa, Origem cold/com cotação)
- 7 métricas (R$, Volume, Itens, R$ Preta, % Preta, R$/kg, AOV)
- Toggle Tabela / Heatmap
- **Salvar até 10 visões nomeadas** (localStorage, persistente entre sessões)
- Drill-by-click (linhas drillable adicionam ao filtro global)
- Export CSV

---

## Vocabulário canônico (PT/EN big4)

28 termos padronizados no glossário central:

**Métricas financeiras:** Faturamento · Volume (t/kg) · Preço médio realizado · AOV (Average Order Value) · R$/kg médio.

**Conversão:** Win Rate (R$ declarado) · Hit Rate (itens) · Conversão Real (R$ pedido ÷ R$ cotação Ganhou) · Leakage · Pipeline Coverage · Sales Cycle Length.

**Temporal:** YoY · MoM · YTD · MTD · Run-rate (YTD × 12 / mes_atual).

**Segmentação:** Curva ABC · Customer Concentration · HHI (Herfindahl-Hirschman) · Share-of-Wallet · Cross-sell Ratio · Churn · Reativação · Aging.

**Pricing:** Pocket Price · Cold Order · Ajuste pós-fechamento · Variance Bridge.

**Faixas internas AFS (mantidas):** Verde (PU ≥ F1) · Amarela (entre F1 e F2) · Vermelha (entre F2 e F3, piso) · **Preta** (abaixo de F3, piso furado).

---

## Decisões importantes da sessão

### 1. Painel é template + dados separados
HTML versionável (~270 KB sem dado), `pedidos_data.js` carrega `window.PED` (~6 MB com schema v3), `cotacoes_data.js` carrega `window.CD` (~21 MB). Ambos gitignored. Estratégia `<script src=>` (não `fetch()`) evita CORS em `file://`.

### 2. Aggregator é multi-ano
Glob `PedidosEmitidos*.xlsx` processa todos os arquivos numa passada. **Anos fechados imutáveis**, ano corrente substituído semanalmente. Mesma estratégia do RAF.

### 3. Pedido cold = pedido sem cotação prévia Ganhou
Detecção via cross-check de `pedido_id` (formato `NNNNN.X`) entre derivado de pedidos e derivado de cotações onde `bucket_status='Ganhou'`. 97,3% de cobertura em 2026 (2,7% cold). Caso BINOTTO `MATRIZ_537267 item 1` validou 1:1 (cotação PU 7,50 → pedido PU 7,50 → mantido em Preta).

### 4. Cliente ativo = compra nos últimos 90 dias
Definição confirmada com Gustavo (alguns clientes têm ciclos mais longos, mas é exceção). Em risco = 60-90d sem compra (era ativo, ≥2 meses históricos). Churn = >90d sem compra (era ativo).

### 5. Cohort baseado na primeira compra do período visível
Não na primeira compra histórica (que exigiria RAF antigo carregado). Trade-off: cohort fica limitado ao horizonte do `pedidos_data.js`, mas é honesto sobre o que sabemos.

### 6. Pocket Price Waterfall padrão McKinsey simplificado
6 níveis (sem cost-to-serve, sem margem oculta — não temos pré-faturamento). Filtrado SÓ pra itens cobrados em R$/kg (PÇ e M distorcem média ponderada).

### 7. Variance Bridge YoY com 3 componentes
- Volume Effect: (kg_atual − kg_anterior) × P_anterior
- Price Effect: (P_atual − P_anterior) × kg_atual
- Mix/Outros: resíduo
- Clientes novos/perdidos: métrica complementar (não soma no bridge pra evitar dupla contagem)

### 8. Histórico de chaves pra detectar cancelamentos
Aggregator mantém `02_Derivados/Pedidos/historico_chaves.json` com `{semana_iso: [chaves]}`. Compara exports consecutivos pra detectar: novos pedidos, cancelados (chave sumiu), reajustes (mesma chave PU diferente). Espelha o que o Softcomp **omite** do export (cancelados não vêm).

### 9. Treemap squarified, não d3-treemap
Implementação JS puro (algoritmo Bruls et al. 2000 simplificado). Não adicionei dependência d3 — Chart.js + CSS resolvem 100%. Hierarquia Aço → Perfil → Acab → Família com toggle de profundidade.

### 10. Visualização heatmap usa gradiente verde→amarelo→vermelho
Convenção: alto R$/kg = verde (margem boa), baixo = vermelho. NUNCA usar verde/amarelo/vermelho/preto pra outras dimensões — esses 4 são exclusivos da política de faixa de preço AFS.

### 11. Drill-by-click padronizado
Helper `adicionarFiltroGlobal(dim, valor)` ativa filtros globais a partir de qualquer click em barra/célula/linha. Breadcrumb mostra chips removíveis com `×`. Só drillable nas dimensões globais (ano/unidade/gerência/vendedor/UF) — outras dim viram filtro só local da tabela.

### 12. Bug `unid_pu`/`unid_qtd` (Softcomp exporta header None nas col AC/AE)
Pipeline de pedidos tinha que mapear posições fixas (AC=Column2, AE=Column3) pra capturar essas colunas. Igual problema das cotações resolvido em F9.2. Mantido helper `_POS_FALLBACK` em `pedidos/pipeline.py`.

---

## Métricas-chave validadas (YTD 2026 jan-mai)

**Globais:**
- 22.877 itens · R$ 85,2 MM · 6.434 t · 1.664 clientes · 87 dias úteis com atividade
- R$ 979 mil/dia útil médio
- Ticket médio R$ 3.724/item

**Tabela Preta por unidade:**
- **CAXIAS DO SUL: 53,8% R$ em Preta** (Fabiola, única gerente da unidade — 18,9% dos itens) ⚠️
- RIO PRETO: 25,1%
- MATRIZ: 19,3%
- PIRACICABA: 12,2%
- SAO CARLOS: 6,9%
- VILA PRUDENTE: 0%

**Pocket Price Waterfall:**
- MATRIZ: PU R$ 12,25 vs F3 R$ 11,65 → +5,21% ✓
- CAXIAS DO SUL: PU R$ 10,29 vs F3 R$ 11,01 → **−6,57%** (abaixo do piso)

**Curva ABC (clássica 80/15/5):**
- A: 232 clientes (14%) → R$ 68,1M (80%)
- B: 427 clientes (26%) → R$ 12,8M (15%)
- C: 1.005 clientes (60%) → R$ 4,3M (5%)

**Customer Concentration (BAIXA):**
- Top 10 = 25,9%
- Top 20 = 38,1%
- Top 50 = 52,1%
- HHI = 107 (categoria "baixa")
- Argumento defensivo pro board: diversificação de receita é moat.

**Cross-check pedido × cotação:**
- 97,3% match (22.251 itens)
- 2,7% cold (626 itens)

**Histórico 2025 (ano fechado):**
- 73.594 itens
- R$ 547,2 MM
- ~17,7 mil t (estim.)

**Top concorrentes (cotações):**
- Trefita/Torres · Açovisa · GGD · Açofera · Diferro · Açotubo
- TER BRASIL: 97,2% R$ em Preta (bloqueio vigente validado)
- ARCO: 66,2% · CESTARI: 34,8% · WEG SC: 22,3%

**Lixo cadastral identificado:**
- "Lamiando Importado" (R$ 0,97M, 63 itens)
- "Laminiado Importado" (R$ 0,70M, 85 itens)
- 148 itens / R$ 1,67M em famílias-fantasma por typo no `FamiliasProdutos.xlsx`. Vale rodada de limpeza.

---

## Comandos operacionais

### Rotina semanal (segunda-feira de manhã)
```bash
cd ~/Documents/Personal/00.\ Projetos\ -\ Claude/Planejamento\ Estratégico\ -\ Comercial
python3 MotorAnalitico/main.py --pedidos-all
```
Tempo estimado: ~70-80s (96k linhas, 2025 + 2026 + lookup RAF + cross-check + aggregator).

### Comandos atômicos (debug)
```bash
python3 MotorAnalitico/main.py --pedidos-enriquecer     # só enriquecedor
python3 MotorAnalitico/main.py --pedidos-crosscheck     # só cross-check
python3 MotorAnalitico/main.py --painel-pedidos         # só aggregator
```

### Cadência de exports do Softcomp
| Bruto | Cadência | Comportamento |
|---|---|---|
| CotacoesPendentes | Diário | Substitutivo |
| CotacoesEncerradas | Semanal (segunda 9h, YTD) | Substitutivo full |
| PedidosEmitidos_YYYY | Semanal (segunda 9h, YTD) | Substitutivo por ano |
| RAF_YYYY | Mensal (fechamento contábil) | Substitutivo por ano |

---

## Backlog / próximas evoluções

### Curto prazo (pós-validação em uso real)
- Refinos baseados em uso (cards que vieram zerados, dimensões faltantes na Análise Livre, gaps no Funil)
- Limpeza do cadastro `FamiliasProdutos.xlsx` (typos "Lamiando/Laminiado/Forajdo")

### Médio prazo
- **Cross-check RAF × Pedidos** (4º estágio do funil "NF Faturada"): requer cruzar `pedido_id` × NF do RAF. Destrava margem oculta real por pedido (já que RAF tem spreads ABCDV_LOG/COR/FIN/INT/CERT/EXT/REP).
- **Bloqueios operacionais** em `config/bloqueios_pricing.yaml` aplicados ao painel de pedidos (hoje só RAF usa).
- **Quality check de typos** rotativo no aggregator (warning quando família contém "lamia"/"forajd"/etc).

### Longo prazo
- Forecast estatístico (parqueado — board prefere run-rate simples)
- Pipeline scoring por probabilidade (parqueado — sem modelo, evitar charlatanismo)
- NPS / satisfação (fora do escopo dos cubos)
- Cost-to-serve nível McKinsey (frete + bonificação + serviço técnico) — quando RAF tiver granularidade suficiente

---

## Stack técnica final

- **HTML**: `03_Ferramentas/Painel_Cotacoes.html` (5.485 linhas, template versionável)
- **Dados**: `cotacoes_data.js` (~21 MB, `window.CD`, schema v2.2) + `pedidos_data.js` (~6 MB, `window.PED`, schema v3-2026-05-11) — ambos gitignored
- **Charts**: Chart.js 4.4.0 + chartjs-plugin-datalabels 2.2.0 via CDN
- **Treemap**: implementação JS própria (squarified)
- **Tema**: dark mode (CSS variables `:root`)
- **Smoke test**: Node + DOM mock (`/tmp/smoke_pedidos.js`)

### Motor Analítico
- `MotorAnalitico/pedidos/`: enriquecer.py, pipeline.py (multi-ano), cross_check_cotacao.py, aggregator.py, lookup_familia.py (reuso cotações)
- 6 cubos OLAP novos no v3: `cubo_aco_bitola`, `cubo_aco_perfil_acab`, `pocket_price`, `cubo_corte`, `cubo_cliente_mes`, `clientes_dim`
- Histórico de chaves em `02_Derivados/Pedidos/historico_chaves.json` pra detecção de cancelamentos

---

## Notas pra retomar em sessão futura

- O painel agora roda **6 abas core puras**. As 4 legacy foram apagadas. Se algum drill-down granular fizer falta, refazer sob demanda.
- Variance Bridge YoY só ativa quando 2 anos carregados (2026 + 2025). Hoje destravado.
- Pocket Price Waterfall filtra `unid_pu='KG'` (R$/kg faz sentido). PÇ e M ficam de fora — adicionar waterfall próprio pra esses universos é roadmap futuro se necessário.
- Pivot Builder (Análise Livre) salva combinações em `localStorage['pv_saved_v1']` — persistente entre sessões, sem servidor.
- Drill-by-click hoje só funciona em dimensões globais (ano/unidade/gerência/vendedor/UF). Família/Faixa/Aço/Perfil/Acab são filtros locais por aba.

Caso atualizar `CLAUDE.md` da pasta principal: bumpar schema de cotações pra v2.2-2026-05-09 e pedidos pra v3-2026-05-11. Adicionar lista das 6 abas MECE.
