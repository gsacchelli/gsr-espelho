---
data: 2026-04-22
tipo: log
status: vigente
obs: "fechado"
projeto: Simulador Precificação
fase: W3 Wrapper Fino — W3d-3
---

# W3d-3 — Render Comparativo Softcomp × DRE validado em produção

## Resultado

Bloco "Comparativo Softcomp × DRE" (#sim-comparativo) extraído do `simCalc()` monolítico para módulo puro `render_comparativo.js`. Segue o padrão W3d do piloto (`render_corte.js`) e do W3d-2 (`render_dre.js`). Validado em produção por Gustavo: "perfeito".

Camada aritmética (spreads fiscais, financeiros e deltas de custo) permanece em `simCalc` — migração para o motor é camada futura, fora do escopo deste wrapper fino.

## Entregue

- **`03_Ferramentas/js/render_comparativo.js`** (159 linhas) — IIFE + `window.SimRender.comparativoV4 = render` + `module.exports` (dual Node/browser). Guards triviais (`ctx` null/undefined ou sem os 3 campos obrigatórios → retorna string vazia). Helpers internos: `pctVL`, `pctVLfmt`, `cmpH`, `cmpSub`. Formatadores pt-BR (`f2` via `toLocaleString`, `pct2`/`pct1` via `toFixed().replace('.', ',')`).
- **`03_Ferramentas/js/render_comparativo.smoke.js`** (214 linhas) — 58 asserts em 7 seções: guards, render mínimo, spreads fiscais/financeiros, margem oculta, margens no VT, deltas negativos, flags OFF, valorBase = 0. **58/58 PASS**.
- **HTML wrapper** — `<script src="js/render_comparativo.js"></script>` adicionado na L.238 (após `render_dre.js`). Bloco inline do `simCalc` (~86 linhas: 5 helpers + `innerHTML` template) substituído por 22 linhas: cálculo de spreads (`cfSpread`, `adjDVA`, `adjLog`, `adjCom`, `_spreadCorteAcrescimo`, `_spreadCorteMargemMC`) + ctx de ~24 campos + chamada com guard `(window.SimRender && window.SimRender.comparativoV4)`.

## Validações

- Smoke test Node: **58/58 PASS** (rodado em 2 iterações — primeira com formato US, segunda com formato pt-BR após fix).
- `node --check` no JS embutido do HTML (690k chars após refactor): SYNTAX OK.
- Shadow bloqueante (W2.5) continua ativo, 0 divergências aritméticas. Shadow não cobre render (é aritmética-only), então validação de render é visual + smoke.
- Validação visual em produção: Gustavo abriu cotação real, rodou simCalc, conferiu o bloco renderizado. Flagou bug herdado (valores sem localização pt-BR). Após fix: "perfeito".
- `propostaPatchComparativo` permanece funcional — é DOM-based (busca por textContent "Base comparativa", "Resultado Softcomp (atual)", "Resultado DRE" e injeta spans no gridEl). Módulo refatorado entrega o mesmo DOM, patch continua transparente.

## Decisões arquiteturais

- **ctx único com ~24 campos** — alinhado ao piloto e ao W3d-2. Sem sub-módulos, sem splits (Comparativo é relativamente plano comparado ao DRE).
- **Aritmética fica no HTML** — spreads fiscais (`cfSpread`, `adjDVA`, `adjLog`, `adjCom`) e deltas de custo (`_spreadCorteAcrescimo`, `_spreadCorteMargemMC`) continuam calculados em `simCalc` antes do ctx. Migração para o motor é camada futura (possível Camada 10 ou integração W3e). Neste W3d-3 o objetivo é extrair render puro — não mover cálculo.
- **Dead code removido** — `cmpRow` (helper não usado), `_totalSpreadsCmp`, `margemMaterial`, `compDif`, `compDifPct` (variáveis derivadas que ficavam na função mas não eram referenciadas no HTML final). Motor a refatorar é oportunidade de limpeza, desde que o diff visual feche.
- **Fix pt-BR aproveitado** — Gustavo flagou durante a validação que os valores saíam em formato US (1000.00 / 2.50%). Bug herdado do bloco original, preservado 1:1 por padrão (mesma decisão que tomei em W3d-2 com o `1.50/kg`). Como a correção é trivial e a regressão já estava aberta no meu teclado, apliquei no mesmo checkpoint em vez de reabrir depois. Smoke test atualizado pra validar pt-BR (58/58 PASS novamente). Sweep pros outros módulos (`render_dre.js` e `render_corte.js`) fica registrado como dívida.

## Estatísticas

- Linhas removidas do `simCalc`: ~86 (5 helpers inline + innerHTML multi-linha + variáveis derivadas mortas).
- Linhas adicionadas no `simCalc`: 22 (cálculo de 6 spreads + ctx + chamada com guard).
- Redução líquida: ~64 linhas.
- Tamanho do HTML: 697k → 690k chars.
- Tempo de execução: ~35min do refactor + smoke + validação visual + ~15min do fix pt-BR e regressão da smoke.
- Teste total da suite: 764/764 PASS (motor + schema + gerador + comparativo + recontagem — inalterado, smoke do render é teste standalone fora da suite principal).

## Próximos passos

1. **W3d-4** — `render_mc.js`. Bloco "MC do Pedido" (#sim-mc) com cards Verde/Amarela/Vermelha/Preta. Estimativa: ~80 linhas inline, 4 variantes do mesmo layout. Oportunidade natural pra fix pt-BR em `render_dre.js` e `render_corte.js` no mesmo sprint.
2. **W3d-5** — `render_estoque.js`. Bloco "Estoque & Custo MP" (#sim-estoque). Estimativa: ~60 linhas inline.
3. **W3e** — `simCalc` adapter fino. Só depois de W3d-4 e W3d-5 fecharem. Consolida os cards do motor (`cards.repasse` já bate bit-idêntico em 60/60 campos) como fonte única e apaga inline que sobrou.
4. **Sweep pt-BR** — aplicar `toLocaleString('pt-BR', …)` em `render_dre.js` e `render_corte.js`. Pode ser incluído no commit do W3d-4 pra não ocupar um sprint isolado.

## Lições reforçadas

- **Bug herdado ≠ bug pra ignorar.** No W3d-2 deixei o `1.50/kg` escapar ("fora do escopo"). Funcional, mas reincidente em W3d-3 com formato US. Custou menos consertar junto com o refactor do que abrir uma dívida pendurada. Daqui pra frente: se o bug herdado é trivial e já tô com o código aberto, corrige.
- **Validação visual do Gustavo pega o que smoke não pega.** Smoke valida estrutura (labels, classes, condicionais). Formato de número é qualidade perceptível que só aparece aos olhos. Manter o ciclo: smoke verde → ship → validação visual do Gustavo → correções de UX no mesmo sprint.
- **ctx enxuto vence sub-módulos.** Repetição do padrão W3d-2. 24 campos num objeto é legível, testável e não paga overhead de orchestration.
- **Shadow aritmético não cobre render.** Recorrente. Smoke standalone por módulo é o complemento necessário. Manter o padrão pra W3d-4 e W3d-5.
