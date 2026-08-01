---
data: 2026-04-22
tipo: log
status: vigente
obs: "fechado"
projeto: Simulador Precificação
fase: W3 Wrapper Fino — W3d-4 + sweep pt-BR
---

# W3d-4 — Render MC Cards + Sweep pt-BR validados em produção

## Resultado

Bloco "MC do Pedido" — 5 cards Verde / Amarela / Vermelha / Preta / Repasse (#sim-pv-*) — extraído do `simCalc()` monolítico para módulo puro `render_mc.js`. Segue o padrão W3d consolidado (piloto `render_corte.js`, W3d-2 `render_dre.js`, W3d-3 `render_comparativo.js`).

Na mesma leva, sweep pt-BR aplicado em `render_dre.js` e `render_corte.js` fechando a dívida aberta no W3d-2 (`.toFixed(N)` preservado 1:1 do inline original por estar "fora do escopo"). Agora os 4 módulos de render seguem formatação pt-BR consistente.

Validado em produção por Gustavo abrindo orçamentos já realizados: "esta ok".

## Entregue

### W3d-4 Render MC Cards

- **`03_Ferramentas/js/render_mc.js`** (~145 linhas) — IIFE + `window.SimRender.mcV4 = render` + `module.exports` (dual Node/browser). Guards triviais (ctx null/undefined ou sem primaryUnit → null). Decisão arquitetural: retorna objeto estruturado com fragments por card `{verde, amarela, vermelha, preta, repasse}` × `{hero, det, marg, units, visible}` — wrapper aplica os 4 sub-IDs DOM por card × 5 cards. Preserva estrutura DOM atual (necessário porque `propostaFromDOM` e impressão leem os 4 sub-IDs individualmente).

- **`03_Ferramentas/js/render_mc.smoke.js`** (~214 linhas) — 48 asserts em 10 seções: guards, render mínimo, Preta visível, Repasse com MP sugerida, primaryUnit kg/pc/m, font-size adaptável no hero (>10→16, >7→18, else 22), units filtra valores zero (Engenheirado), formatação pt-BR, repasseMgMp arredondado (25.7→26). **48/48 PASS**.

- **HTML wrapper** — `<script src="js/render_mc.js"></script>` adicionado na L.238 (após `render_comparativo.js`). Bloco inline ~110 linhas substituído por 32 linhas: cálculo de Repasse aritmética (motor igual V/A/R com swap de margem MP) + ctx de ~20 campos + chamada com guard `(window.SimRender && window.SimRender.mcV4)` + helper `_applyCard(prefix, frag)` que faz 4 DOM writes por card.

### Sweep pt-BR

- **`render_dre.js`** — helpers `pct1` e `pct2` adicionados (replicando padrão do W3d-3). 15 pontos de `.toFixed(N)` substituídos: ICMS, PIS/COFINS, Selic, DDV/Com real, Logística real, Spread Financeiro/DDV/Logística/Comissão (4 labels × 2 valores cada), Lâmina/Tolerância (1 decimal em mm), MC do Min1kg, sucata R$/kg da Ponta, PIS na Ponta. Bar widths da Composição separados em `barMatW` (CSS, com ponto — CSS não entende vírgula) / `barMatWDisp` (display, com vírgula).

- **`render_corte.js`** — helper `_pct2` adicionado. 2 pontos corrigidos: `mcBaseEff * 100` em "Camada 2 MC aplicada" (L.114) e em "Spread Corte + Mín 1kg" (L.119). `toFixed(0)` do Ratio IC mantido — `.toFixed(0)` produz string inteira sem ponto decimal, seguro.

- **`render_dre.smoke.js`** — expandido de 27/27 → 48/48 com 19 asserts novos em seção "Formatação pt-BR nos percentuais e labels" cobrindo os pontos corrigidos (ICMS/PIS/COFINS/Selic/DDV/Com/Log/Financeiro/DDV Spread/Comissão Spread/Lâmina/Tolerância/Composição/dreN pct/Ponta PIS/Min1kg MC). Asserts negativos verificam ausência do formato US antigo (`18.00`, `1.50/kg`, etc).

- `render_corte.js` sem smoke próprio (piloto foi antes da convenção de smoke por módulo — débito leve, fica pra quando houver motivo de tocar o módulo de novo).

## Validações

- Smoke tests Node: **48/48 PASS** render_mc + **48/48 PASS** render_dre + **58/58 PASS** render_comparativo. Total render suite: **154/154**.
- `node --check` no JS embutido do HTML (~689k chars após refactor): SYNTAX OK.
- Shadow bloqueante (W2.5) continua ativo, 0 divergências aritméticas. Shadow não cobre render (é aritmética-only), então validação de render é visual + smoke.
- Validação visual em produção: Gustavo abriu orçamentos já realizados, conferiu o bloco renderizado (os 5 cards em modo normal + Repasse quando aplicável, DRE com formatação pt-BR consistente, detalhamento do corte). Resposta: "esta ok".
- `propostaFromDOM` e função de impressão: continuam lendo os 4 sub-IDs individualmente — arquitetura do módulo preserva a estrutura DOM, nenhuma mudança necessária downstream. `_repUpRef` preservado pro card Negociado. W3b-2 instrumentation (`_htmlCardValRep`/`_htmlMsvlRep`/`_htmlUpRep`) preservada pro shadow.

## Decisões arquiteturais

- **Alternativa A (fragments object) vs Alternativa B (adapter callback)** — Gustavo escolheu A explicitamente. Razão: 4 sub-elementos por card × 5 cards = 20 atribuições DOM. Callback seria overhead desnecessário; struct object mantém o módulo 100% puro e o wrapper lida com a aplicação DOM. Mesma arquitetura do W3d-3 funcionou, mesma aqui.
- **Aritmética do Repasse fica no HTML** — ~40 linhas do cálculo de Repasse (motor igual V/A/R com swap de margem MP) permanecem no simCalc antes do ctx. Migração para motor é camada futura (W3e ou Camada 10). Neste W3d-4 o objetivo é extrair render puro.
- **pt-BR nativo** — `render_mc.js` já nasceu com helpers `f2`/`pct2`/`pct0` (toLocaleString + toFixed+replace). Aproveitei a janela aberta pra fazer sweep nos outros 2 módulos (`render_dre.js` + `render_corte.js`) que ainda tinham o bug herdado 1:1 de quando foram extraídos. `render_comparativo.js` já foi corrigido no W3d-3 quando Gustavo flagou durante a validação.
- **Bar widths CSS vs display** — caso sutil em `render_dre.js`: `barMatW` é usado em `style="width:X.X%"` (CSS) E em display text. CSS precisa de ponto, display precisa de vírgula. Solução: manter `barMatW` com ponto pro CSS, criar `barMatWDisp` com vírgula pro display. Explicito e auditável.

## Estatísticas

- Linhas adicionadas em `js/`: render_mc.js (~145) + render_mc.smoke.js (~214) = ~359 linhas.
- Linhas removidas do simCalc: ~110 (renderCard inline + 4 invocações + Repasse render + Preta visibility).
- Linhas adicionadas no simCalc: ~32 (ctx + chamada com guard + _applyCard helper).
- Redução líquida no simCalc: ~78 linhas.
- Tamanho do HTML: 690k → 689k chars (sweep pt-BR também enxugou fracamente).
- Suite total: **154/154 PASS** (render_dre 48 + render_mc 48 + render_comparativo 58). Motor principal intacto: 764/764 (rodado não neste log, mas nenhuma mudança na lógica de cálculo).
- Tempo de execução: ~45min do W3d-4 (render + smoke + substituição + node --check) + ~25min do sweep pt-BR (3 arquivos + expansão da smoke) + validação visual.

## Próximos passos

1. **W3d-5** — `render_estoque.js`. Bloco "Estoque & Custo MP" (#sim-estoque). Estimativa: ~60 linhas inline. Último render a extrair antes do W3e.
2. **W3e** — `simCalc` adapter fino. Só depois de W3d-5 fechar. Consolida os cards do motor (`cards.repasse` já bate bit-idêntico em 60/60 campos no shadow) como fonte única e apaga inline que sobrou. Este é o passo que materializa o ganho estrutural do sprint W3.
3. **Fase pós-motor de config** — migração dos hardcodes AFS (CF escalonado, certificações, fases industriais) do motor para `parametros_afs.json`. Independente do W3, mas pré-requisito pra MetalM compartilhar o motor.
4. **Débito leve** — criar smoke test pro `render_corte.js` (piloto). Baixa prioridade; só se houver motivo de tocar o módulo de novo.

## Lições reforçadas

- **Sweep oportunístico vale.** Dívida herdada do W3d-2 (`.toFixed(N)` preservado 1:1) custou trivial pra fechar junto com o W3d-4. Se tivesse deixado aberto, teria me incomodado de novo na próxima vez que tocasse DRE. Lição do W3d-3 confirmada: bug herdado trivial + arquivo aberto = conserta junto.
- **Alternativa A venceu por previsibilidade.** Callback seria mais flexível mas acopla módulo e wrapper de um jeito que dificulta o teste unitário. Fragments object é feio como API ("toma um objeto com 5 sub-objetos") mas cristalino pra testar. Pagamos custo de legibilidade do lado de quem chama (_applyCard helper) em troca de pureza do lado de quem é chamado.
- **Smoke test continua pegando o que shadow não pega.** Shadow roda aritmética; smoke verifica estrutura e formato. O bug do pt-BR no W3d-3 seria invisível pro shadow pra sempre — só a smoke (e o olho do Gustavo) pega.
- **Validação visual do Gustavo é rápida quando o padrão está consolidado.** W3d piloto foi mais demorado; W3d-2, W3d-3 e agora W3d-4 foram "esta ok" direto em produção. Efeito composto do padrão + shadow aritmético bloqueante + smoke por módulo.
