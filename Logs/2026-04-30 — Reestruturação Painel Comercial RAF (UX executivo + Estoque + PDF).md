---
data: 2026-04-30
tipo: log
status: supersedida
substituida_por: "[[Logs/2026-07-14 — Regras de negócio oficializadas (DRE, comissão agente) + Estágio 5]]"
obs: "Pacotes 6, 7, 8, 9, 9b aplicados — boot validado em todos"
projeto: Painel Comercial RAF — Reestruturação completa de UX (4 abas) + Análise de Estoque Estratégico + PDF Export
relacionados: 
---

# 30/04/2026 — Reestruturação Painel Comercial RAF + Pacote 5 (Estoque) + Pacote 6 (PDF)

Sessão grande de UX. Trazendo o painel pra padrão executivo "como estamos / o que mudou / o que aconteceu". Foram 8 pacotes consecutivos (rodadas R5b, R6, R7, R8, R9, R9b) com decisões metodológicas que precisam ficar registradas no vault.

## Pacote 5 — Análise de Estoque Estratégico (rodada anterior, contexto)

Fechado entre 29 e 30/04. Resumo decisional:

### Regra de classificação de origem do material PARTIDA

Aplicada no enriquecedor RAF (`raf/enriquecer.py::derivar_origem`) e também no aggregator quando processa `EstoquePadrao.xlsx`. Cobre ~99% do estoque/RAF Sacchelli:

| Perfil + Acabamento | Faixa Bitola | Aço | Origem | Fornecedor | Lead Time |
|---|---|---|---|---|---|
| Redondo Forjado (qualquer) | qualquer | qualquer | **Nacional** | Metals | 5 meses |
| Redondo Laminado | ≤ 101,60 mm | 10XX (carbono) | **Nacional** | Simec/Arcelor | 3 meses |
| Redondo Laminado | ≤ 101,60 mm | 4140/43XX/86XX/20MnCr5/17CrNiMo7 | **Importado** | Daye/HBIS | 8 meses |
| Redondo Laminado | 101,61-380 mm | 10XX/4140/43XX/86XX/20MnCr5/17CrNiMo7 | **Importado** | Daye/HBIS | 8 meses |
| **Catch-all** | — | — | **Não mapeado** | — | — |

Cobertura medida no RAF 2026 enriquecido: 98,5% (Importado 62,9% + Nacional 35,6%; Não mapeado 1,5%).

### Decisão metodológica fundamental — "encalhado" não existe em distribuidor de aço importado

Em distribuidor com lead time longo, **estoque é parte do produto ofertado**. Cliente vai à Sacchelli porque ela tem o aço PRONTO. Métrica errada: tempo absoluto no estoque. Métrica certa: **cobertura relativa ao lead time específico da origem.**

| Categoria | Saudável | Atenção | Risco |
|---|---|---|---|
| Nacional Laminado (lead 3m) | até 3 meses | 3-6 meses | > 6 meses |
| Nacional Forjado (lead 5m) | até 5 meses | 5-10 meses | > 10 meses |
| **Importado (lead 8m)** | **até 12 meses** | **12-18 meses** | **> 18 meses** |

**Aço importado com 8m de cobertura = estoque ESTRATÉGICO, não problema.** Aço nacional com 8m de cobertura = problema.

### Métrica visual da matriz de Estoque

Bubble chart Cobertura × MC% médio histórico da família partida (do RAF):
- Eixo X: cobertura em meses (limite visual 36m, com bandas verticais nos lead times de cada origem)
- Eixo Y: MC% médio histórico (cruzado via `cubo_produto_partida`)
- Cor: origem (verde Nacional / azul Importado / cinza Não mapeado)
- Tamanho: qtd em estoque (kg)

## Pacote 6 — Filtros refinados + DRE Gerencial reestruturada + PDF Export

### 6a. Filtros — período + cascateamento dinâmico + Configurações

- **Filtro de período** dentro do ano: selects de Mês Início e Mês Fim (Jan-Dez). Visíveis apenas quando ano específico selecionado.
- **Cascateamento dinâmico** de Gerência/Vendedor/Op_Categoria por ano + período + considerar. `_resolverDimensoesAtivas()` itera o cubo_main filtrado e expõe só dimensões com volume real. Vendedor que saiu em 2024 some quando filtra 2026.
- **"Apenas linhas analisáveis"** movido pra menu Configurações ⚙ no canto direito do filtro. Default ON. Renomeado pra "Excluir Acessórios e Sucata" (mais explícito).

### 6b. DRE Gerencial — reestruturação narrativa executiva

Princípio aplicado: **hierarquia "Como estamos / O que mudou / O que aconteceu"** — pintura de painel executivo clássico.

Nova estrutura em 6 blocos:

1. **KPI Hero (4 cards grandes com sparkline 12m):**
   - Receita Líquida (com Δ YoY %)
   - Margem de Contribuição (R$ + %)
   - MC Ampliada (gerencial — captura Margem Agregada)
   - **MC% vs Break-Even** (cor de zona: verde "paga prêmio" / amarelo "no fio" / vermelho "destrói valor")

2. **KPIs secundários** — 10 métricas em tabela compacta subordinada visualmente (Custo Aço, Custos Diretos, Custos de Servir, Margem Agregada, % Tabela Preta, nº OS, nº Clientes, Ticket Médio, R$/kg, Concentração Top 10).

3. **Tendência MC% últimos 24 meses** — line chart com bandas coloridas:
   - Verde: ≥ 35% (saudável)
   - Amarelo: 28-35% (cobre capital com pouco prêmio)
   - Vermelho: < 28% (destrói valor)

4. **Driver Tree YoY (único)** — Volume × Preço × Custo Aço × Mix. Removido o Waterfall (redundante com a tabela DRE). Adicionada **leitura textual automática** abaixo: "MC subiu/caiu R$ X. Driver dominante: ..."

5. **DRE Vista Tabular com toggle Resumida/Detalhada** (default Resumida = 6 linhas estruturais). Coluna **Δ consolidada** (R$ + pp) substitui as 2 colunas separadas anteriores: "−R$ 435k (+0,3pp)" — uma leitura única.

6. **Insights horizontais** — 4 cards lado a lado: Top 3 Famílias YoY · Top 5 Clientes · Variação por Componente · Alertas Auto.

### Decisão crítica — YTD-comparable em todo lugar

Quando ano corrente é parcial (ex: 2026 jan-fev), comparar com ano cheio anterior é apples-to-oranges. **Solução universal**: helper `_resolverAnoComparativo(anoAtual)` que detecta se ano corrente está incompleto e recorta o ano anterior pelo mesmo período. Aplicado em DRE Vista Tabular, Leitura Estratégica e Driver Tree YoY.

Header da tabela passa a mostrar "R$ Jan-Fev/2026" e "R$ Jan-Fev/2025" em vez de "R$ 2026" e "R$ 2025" — sem ambiguidade.

### 6c. PDF Export

Botão 📄 PDF no header do painel. Modal com seleção de abas e orientação. Print CSS nativo (sem libs externas) — texto pesquisável, charts vetoriais via canvas, page break entre abas. Defaults: landscape, header minimalista.

## Pacote 7 — Carteira (3 sub-pacotes 7a/7b/7c)

### 7a. KPI Hero + Concentração & Risco

KPI Hero com 4 cards no topo da aba Carteira:
- % Receita Estrela (zona pos: ≥ 50%; warn: 30-50%; neg: < 30%)
- % Receita Vaca Saudável
- % Receita em Risco (Vaca-Risco + Cachorro)
- Concentração Top 10

Bloco "Concentração & Risco" sempre visível com 3 cards:
- Concentração de receita (Top 5/10/20/50, nº de clientes pra 80%)
- Distribuição BCG por contagem
- **Top 5 Clientes em Zona Crítica** (com volume e MC%) — ação imediata

### 7b. Detalhe do cliente reformulado

Removido o **mini-DRE redundante** com a aba DRE Gerencial (era a mesma cascata em escala menor). Em vez disso, conteúdo específico do cliente:

- 4 mini-KPIs: Receita | **MC% vs média da gerência dele** (cor de zona) | NFs/mês | dias desde última compra
- **Histórico de receita 24 meses** em mini-bar chart inline
- **Mix de família com semáforo de MC%** — barras coloridas (verde ≥35% / amarelo 28-35% / vermelho <28%) — cliente com mix concentrado em famílias de baixa MC% fica visualmente vermelho
- Sinais YoY anual + YoY mensal + YTD (mantidos)

### 7c. Migração BCG — visão dinâmica em vez de foto

Tag de migração no header do detalhe do cliente: **"Estrela 2024 → Vaca em Risco 2026"** com cor up/down/stable. Hierarquia de saúde dos quadrantes:

```
Estrela (4) > Interrogação (3) > Vaca (2) > Vaca-Risco (1) > Cachorro (0)
```

Cliente que migrou pra cima ↑ verde, pra baixo ↓ vermelho, igual cinza. Resolve a crítica "matriz é foto, não filme".

## Pacote 8 — Produtos (KPI hero + filtros colapsáveis + Estoque hero)

- **KPI Hero do recorte filtrado** (4 cards): Receita do filtro · MC% · % do total empresa · Volume kg
- **Filtros secundários colapsáveis** em accordion `<details>` "Filtros avançados ▾" com chips de filtros ativos no summary. Removeu poluição visual dos 8 dropdowns.
- **Estoque Hero** (4 cards específicos da subtab Estoque): Total R$ estoque (estimado via preço médio do RAF) · % SKUs cobertura > 12m · % Não Mapeado · SKUs em Zona Crítica (com lógica contextual por origem)

## Pacote 9 + 9b — Evolução

### 9a (rodada inicial)
- Toggle Trimestral adicionado entre Mensal e Anual (V1 funcionava como variante mensal)

### 9b (refinamento)
- **Trimestral REAL**: agregação Q1/Q2/Q3/Q4 (3 meses em 1 ponto). Labels formato "2025-Q3", "2026-Q1".
- **Tendência projetada** com regressão linear simples 6 períodos à frente (2 anos pra modo anual): linha tracejada azul (Receita) + linha tracejada verde (MC%). Mostra "onde a empresa estará se mantiver trajetória".
- **Markers de eventos verticais** — array `EVENTOS_RELEVANTES` configurável no JS. Default já tem mudança plano de contas jan/2024. Posso adicionar futuros: distribuição dividendos out/2025, fechamento Duferco, etc.
- **Bloco "Qualidade do Crescimento"** com 2 mini-charts side-by-side (Δ Receita YoY × Δ MC% YoY) + diagnóstico textual automático classificando entre 4 padrões:
  - **Crescimento Saudável**: receita ↑ + margem ↑
  - **QUEIMA de Margem**: receita ↑ mas margem ↓ (vendendo mais barato)
  - **Qualificação**: receita ↓ mas margem ↑ (saindo de clientes ruins)
  - **Declínio**: receita ↓ + margem estável/↓
  - **Estável**: variação dentro de ±5%

## Decisões metodológicas a preservar

### 1. KPI Hero hierárquico vs lista densa

Painel executivo NÃO comporta 14 KPIs com peso visual igual. Solução: **4 hero (grandes, com sparkline e zona de cor)** + tabela secundária subordinada visualmente. Aplicada em DRE Gerencial, Carteira e Produtos. Criar matriz mental: "se vou ver o painel em 5 segundos, quais 4 números preciso ver?"

### 2. Comparação YTD-comparable como princípio universal

Sempre que houver comparativo YoY e o ano atual estiver incompleto, recortar ano anterior pelo mesmo período. Helper `_resolverAnoComparativo` aplicado em todos os pontos. Header das tabelas mostra período exato ("Jan-Fev/2026") pra evitar confusão.

### 3. Δ R$ ≠ Δ pp — separar leituras de volume vs eficiência

A coluna consolidada "Δ vs Ano-1" mostra "−R$ 435k (+0,3pp)" — força leitura combinada: receita encolheu (volume ruim) MAS margem subiu (eficiência boa). Cliente da diretoria precisa ver as 2 dimensões.

### 4. Migração BCG > Snapshot BCG

Matriz BCG estática é foto. Cliente que era Estrela ano passado e hoje é Vaca-Risco precisa aparecer com tag visual. Resolveu a crítica "matriz não conta a história, só mostra o estado".

### 5. Lead time é a métrica de saúde do estoque, não tempo absoluto

Distribuidor de aço importado sustenta 8-12 meses de estoque. Métrica certa: **cobertura ÷ lead_time da origem**. Bandas dinâmicas por origem (não fixas). Resolveu a confusão estratégica que estoque alto era sempre ruim.

### 6. Nomes BCG canônicos (não Joia/Diluído)

Quadrantes: ★ Estrela / 🐄 Vaca Leiteira (com sub-classificação Vaca em Risco abaixo de 28%) / ? Ponto de Interrogação / 🐕 Cachorro. Nomenclatura BCG clássica → comunicação executiva limpa. "Matriz BCG" (não "Diagrama") por preferência do Gustavo.

### 7. Threshold MC% via custo de capital, não chute

Ver [[Logs/2026-04-29 — Análise DRE Sacchelli + Break-Even Gerencial]] pra detalhamento. **Defaults: 28% (vermelha — break-even SELIC) / 35% (verde — saudável SELIC + 10pp) / 32% (mediana histórica, referência informativa).**

## Próximas pendências (parqueadas)

- **Tabela top famílias com colunas mais focadas** (Pacote 8 não cobriu): hoje mistura "Linhas" sem clareza. Reformular pra ranquear por MC$ e usar indicadores claros de saúde.
- **Atributos da aba Produtos** com 6 charts duplicados (Mix por Aço/Perfil/Acab/Bitola/Corte/Comprimento) → considerar substituir por treemap drillable.
- **Markers de eventos configuráveis via UI** (não só via array JS hardcoded).
- **`renderEvolucao` não filtra vendedor no eixo histórico** ainda — precisa atualizar (foi feito o filtro vendedor mas só nos KPIs comparativos da aba Evolução, não no chart principal). Refinamento futuro.

## Para retomar

Próxima sessão deve focar em **validação de produção** dos pacotes UX (deixar Gustavo testar tudo a fundo) antes de novo escopo. Possíveis próximos:
- Plugar `EstoquePadrao.xlsx` atualizado (último é de 27/04) — re-rodar `--painel-raf`
- Calibrar markers de eventos com datas reais que Gustavo achar relevantes (Duferco, dividendos, etc.)
- Implementar tabela top famílias refinada (Pacote 10?)

## Código alterado nesta sessão

- `MotorAnalitico/raf/enriquecer.py` — adicionada `derivar_origem` + 3 colunas
- `MotorAnalitico/raf/painel_aggregator.py` — `_processar_estoque_padrao` + `_classificar_origem_estoque` + cubo_estoque + vendedor em cubo_transacoes
- `03_Ferramentas/Painel_Comercial_RAF.html` — todos os pacotes 6/7/8/9/9b (UI completa)

Backups antigos em `.bak.20260429*` (várias versões intermediárias).
