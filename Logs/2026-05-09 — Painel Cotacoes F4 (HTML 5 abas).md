---
data: 2026-05-09
tipo: log
status: supersedida
substituida_por: "[[Logs/2026-07-14 — Regras de negócio oficializadas (DRE, comissão agente) + Estágio 5]]"
obs: "F4 fechada — painel HTML em produção"
contexto: Painel Comercial de Cotações
tags: [painel, cotações, html, frontend, sessão]
---

# 2026-05-09 — Painel Cotações F4 (HTML 5 abas)

## TL;DR

F4 entregue na mesma sessão da F3. `03_Ferramentas/Painel_Cotacoes.html` (~1.250 LOC, 68 KB, **template versionável** sem dado embutido). Carrega `cotacoes_data.js` via `<script src=>`. Schema check no boot, wrapper `_safeRender` por bloco, glossário ❓, vocabulário consistente com Painel RAF. Smoke test (Node + DOM mock) confirmou que **todas as 5 abas renderizam sem throw** com o `cotacoes_data.js` real (62k cotações + 1,8k pendentes).

Painel pronto para Gustavo abrir e usar. Ainda não validado em browser real, mas estrutura e lógica passaram em todos os smoke tests possíveis em sandbox.

## O que foi entregue

### Estrutura do arquivo

```
03_Ferramentas/Painel_Cotacoes.html
├── <head> CSS (mesmo design system do Painel RAF — variáveis :root, dark theme)
├── <body>
│   ├── Header (título + botão ❓ Glossário + meta info)
│   ├── Modal Glossário (4 seções: Métricas, Faixas, Auto-flag, Cubos)
│   ├── Nav .tabs (5 abas)
│   ├── .controls — filtros globais (Ano/Unidade/Gerência/Vendedor/Família/UF + Reset)
│   ├── #kpis — KPI bar geral (8 cards densos)
│   ├── 5 .tab-content
│   └── <script src="./cotacoes_data.js">
└── <script> IIFE com toda a lógica (~770 LOC JS)
```

### Helpers core (espelhados do Painel RAF)

- **`_safeRender(tabId, fn)`** — captura erro JS de qualquer aba, mostra inline em vez de quebrar painel inteiro. Banner vermelho com `e.message`.
- **`_avisoFiltrosIgnorados(alvoSelector, suportes)`** — banner amarelo no topo do bloco quando filtros globais ativos não atingem o cubo. Aplicado em Pipeline (cubo_pendentes não suporta ano/uf) e Perdas (cubo_motivos não suporta unidade/uf).
- **Schema check no boot** — aborta render se `CD.schema_version !== 'v1-2026-05-08'`. Banner vermelho com instrução de regerar.
- **Formatadores** — `fmtR$` (resumido: R$ 4,8 MM), `fmtR$Full` (BRL completo), `fmtN`, `fmtPct`, `faixaBadge`, `statusBadge`.
- **Filtros por cubo** — `filtraCuboMain`, `filtraCuboCliente`, etc. Cada um aplica só os filtros que o cubo suporta. UI mostra aviso amarelo no resto.

### As 5 abas

#### Aba 1 — Pipeline (default)
Cubo: `cubo_pendentes`.
- **Aging por bucket** — tabela com 0-7d / 8-15d / 16-30d / 31-60d / 60+ + R$ + % do total. Cores: pos (0-7d) / neg (>30d).
- **Pipeline por vendedor** — top 10 ordenado por R$ aberto.
- **Foco da semana** — itens críticos pendentes (idade > 30d ou flag_projeto_suspeito), max 80 linhas.
- **Top 30 cotações abertas** — agregação por chave de cotação (sem item), com R$ total da cotação + idade max + faixas que aparecem.

#### Aba 2 — Win Rate
Cubo: `cubo_main` + `cubo_geo`.
- **Global** — R$ ganho / R$ total cotado. Cores por threshold (≥25% verde, ≥15% amarelo, <15% vermelho).
- **Ajustado** — exclui Orç.prévio do denominador. Cor por ≥40% / ≥25% / <25%.
- **Por motivo** — Ganhou + Orç.prévio + Preço + Prazo + Outros + Cancelado, com R$ e %.
- **Por vendedor** (≥R$ 100k cotado) — ranking por R$ cotado, mostra WR ajustado.
- **Por gerência** — todas, ordenadas por R$.
- **Por família** — top 15.
- **Por região** — top 15 (cubo_geo).

#### Aba 3 — Análise de Perdas
Cubo: `cubo_motivos`.
- **Top concorrentes** (apenas motivo Preço, exclui "Sem nomeado" e "requer comprovação") — top 15 por número de itens. Trefita/Torres deve aparecer no topo (~2.551 itens).
- **Distribuição por motivo** (apenas perdas — exclui Ganhou e Pendente).
- **Por região** — top 15.
- **Por família** — top 15.
- **Heatmap concorrente × família** — 8 concorrentes × 10 famílias, intensidade vermelha por log(n+1). Apenas motivo Preço.

#### Aba 4 — Item × Estoque × Vermelha ⭐
Lista granular `itens_criticos_top` (5.000 itens).

**Filtros locais:**
- Faixa (todas/Verde/Amarela/Vermelha/Preta)
- Status (todos/Ganhou/Perdeu/Pendente)
- Estoque match (exato/tolerancia/familia/sem_match/engenheirado)
- Flag (Ganhou em Preta / Projeto suspeito / Bloqueio operacional)
- Cliente contém (free text)
- Vendedor

**Componentes:**
- Stoplight bar (distribuição por valor, ignorando filtros locais — cores Verde/Amarela/Vermelha/Preta/N/D, pcts).
- 4 KPI cards: Itens / R$ filtrado / Perda estimada (R$ vermelho) / % com estoque.
- Tabela mestre paginada (100 linhas/página) com 15 colunas: Cot, Cliente, UF, Vend., Família, PU, F3, Gap%, Faixa (badge), Status (badge), Qtd, R$ total, Perda est., Estoque, Flags (G+P / PRJ / 🔒).
- Pager (Anterior / Próxima / Página X de Y) + botão CSV.

**Achado-âncora preservado:** Filtrar `Status=Ganhou` + `Faixa=Preta` mostra os 7 itens da BINOTTO/MATRIZ_537267 com PU=7,50 vs F3=8,07 (Fabiola/RS).

#### Aba 5 — Tabelistas & Projetos
Lê `cliente_classificacao`.

- **Perfil A — Tabelista (68 clientes)** — tabela ordenada por R$ cotado. Mostra n_cotacoes, %Orç.prévio (vermelho — high é ruim), %Conv (vermelho — low é ruim). Top 80.
- **Perfil B — Projeto Suspeito (359 clientes)** — tabela com idade_max colorida por threshold (>60d vermelho, >30d amarelo).
- **Ganhou em Preta** — agregação por (vendedor × cliente) dos itens críticos com `flag_ganhou_preta`. Mostra perda estimada total — foco do Plano Pricing Discipline.

## Decisões de design

| Decisão | O que ficou |
|---|---|
| Visual | Dark theme idêntico ao Painel RAF — mesmas variáveis CSS, sem charts pesados (Chart.js só se necessário em iteração futura) |
| Boot check | Aborta render se schema_version mismatch (não tenta degradar — risco de NaN silencioso) |
| Filtros globais | 6 dimensões (Ano/Unidade/Gerência/Vendedor/Família/UF). Cascata Gerência→Vendedor. Cada cubo aplica só o subset que suporta + banner amarelo no resto. |
| Sem Chart.js | Tabelas + stoplight bar inline. Suficiente pra MVP. Chart.js futuro se Gustavo pedir evolução temporal. |
| Paginação Aba 4 | 100 linhas por página, max 5.000 itens (top crítico). Suficiente pra ver Top X em qualquer recorte. |
| Export CSV | Aba 4 inclui botão CSV — exporta os filtrados (não só a página atual). Headers fixos: 31 colunas |
| Vocabulário | Consistente com Painel RAF: Verde/Amarela/Vermelha/Preta canônico, Pipeline aberto, Win Rate ajustado, Item engenheirado, Cliente-tabelista, Projeto suspeito, Ganhou em Preta, Foco da semana. |
| Smoke test | Node + DOM mock — confirmou IIFE OK, DOMContentLoaded OK, KPI bar populated, todas as 5 abas renderizam sem throw com dado real (62k+1,8k cotações). |

## Smoke test executado

```
Boot OK — Pipeline default rendered
  ✓ KPI bar (1138 chars)
  ✓ Pipeline aging (514 chars)
  ✓ Pipeline vendedor (962 chars)
  ✓ Meta info (76 chars)
  ✓ aba winrate (wr-global chars=31)
  ✓ aba perdas (perd-concorrentes chars=1027)
  ✓ aba item (i-stoplight chars=518)
  ✓ aba tabelistas (tab-tabelistas chars=16080)
SMOKE FULL PASS
```

Validou: ausência de erros de runtime, schemas batem, helpers funcionam, filtros aplicam, tabelas renderizam.

**Não validou (precisa browser real):** layout visual, cores, contraste, responsividade, performance com 5.000 linhas em DOM, hover/click interações.

## Pendentes (após Gustavo abrir e dar feedback)

### Validações com Gustavo
- Visual em browser real (Chrome/Firefox)
- 68 tabelistas: cruzar mentalmente — THERMON / ANDRITZ / USIMATRIX / IBRATEC / CHICO TORNEARIA / etc fazem sentido?
- 359 projetos suspeitos é demais — refinar threshold (R$ 500k? exigir cliente industrial?)
- Win rate 24,23% (corrigido) bate com sensação?
- Caso BINOTTO aparece como esperado em Aba 4 (filtro Ganhou + Preta)?

### Ajustes técnicos previsíveis
- Chart.js para Evolução temporal (mensal Win Rate / Pipeline / Preta) — 1 nova subaba
- Suite de testes Python pro `aggregator.py` — paralelo aos 55 testes do enriquecer
- Cross-check RAF rodar localmente (sandbox limitado a 45s)
- Otimizar Aba 4 se >5k linhas tornarem render lento (virtualização do scroll)
- PDF export como o Painel RAF tem

## Arquivos relevantes

### Novos
```
03_Ferramentas/Painel_Cotacoes.html         (1.248 LOC, 68 KB, template versionável)
```

### Já existiam
```
03_Ferramentas/cotacoes_data.js             (gitignored, 9 MB, schema v1-2026-05-08)
MotorAnalitico/cotacoes/aggregator.py       (entregue F3)
MotorAnalitico/main.py                      (--painel-cotacoes wirado F3)
```

### Atualizados
```
CLAUDE.md                                   (F4 fechada — bumpa)
```

## Conexões

- [[2026-05-09 — Painel Cotacoes F3 (aggregator + cubos OLAP)]]
- [[2026-05-08 — Painel Cotacoes F1+F2 (esqueleto motor + match estoque)]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/03 - Ferramentas Analíticas - Inventário]] — bumpar Painel de Cotações pra **EM PRODUÇÃO**
- [[Sistema Operacional Comercial/05 Cotações/00 - Visão Geral Cotações]] — agora tem painel ativo
- [[2026-04-30 — Plano Pricing Discipline Tabela Preta (Sacchelli)]] — Aba 5 / "Ganhou em Preta" implementa cockpit prometido
