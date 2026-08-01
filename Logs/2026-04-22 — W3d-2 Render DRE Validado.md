# 2026-04-22 — W3d-2 Render DRE Validado em Produção

Fechamento formal do W3d-2 (segundo módulo de render extraído do simCalc). Padrão do piloto W3d (render_corte.js) confirmado com bloco bem mais complexo.

## Resultado

Bloco "DRE do Pedido" (#sim-mc2) renderizado por módulo separado. Gustavo validou visualmente em produção: "esta funcionando".

## Entregue

- **`03_Ferramentas/js/render_dre.js`** (~330 linhas) — função pura `SimRender.dreV4(ctx)` → HTML string.
  - Replica fiel de simCalc L.5065-5157 (grid principal + separadores + Composição do Resultado + bloco Ponta).
  - Export dual: `module.exports` (Node) + `window.SimRender.dreV4` (browser).
  - Guard clauses: `!ctx`, `valorBase === undefined`, `dreRecLiq === undefined` → retorna `''`.
  - ctx enxuto (~60 campos) em seções: Receita, Custos Diretos, Despesas, Spreads, Spreads de Peça, Ponta.

- **`03_Ferramentas/js/render_dre.smoke.js`** (~130 linhas) — 27 testes em Node cobrindo:
  - Guards (null/undefined/{} → '')
  - Render mínimo (ctx completo sem Ponta, sem flags)
  - Ponta ativa (bloco laranja visível, ganho vs sucata)
  - Resultado negativo (Composição some, Total Spreads permanece)
  - Flags OFF (sem spread DDV/Log/Com)
  - Spreads parâmetros de peça (Lâmina/Tolerância)
  - Custos condicionais (Corte oculto quando 0, Serv Ext visível quando > 0)

- **`Analise_Precificacao_Sacchelli.html`** editado em 2 pontos:
  - L.237: `<script src="js/render_dre.js"></script>` após `render_corte.js`.
  - L.5038-5071: substituição do bloco inline (~120 linhas) por 32 linhas de ctx + chamada `window.SimRender.dreV4(ctx)` com guard `(window.SimRender && window.SimRender.dreV4)`. Removidos 5 helpers locais (`pctRL`, `_lbl`, `dreH`, `dreN`, `dreL`) e as 2 IIFEs (Composição, Ponta).

## Validações

- **Smoke test Node**: 27/27 PASS.
- **`node --check` no JS embutido do HTML** (697.045 chars): SYNTAX OK.
- **Grep de variáveis do ctx no escopo de simCalc**: todas declaradas antes do ponto de uso (`_pontaAtivo`, `cutGrupo`, `_cutV4`, `custoTon`, `_mcBaseEff`, `_spreadCorteKg`, `baseColor`, `mc2_totalSpreads`, etc.).
- **Validação visual em produção**: confirmada por Gustavo.

## Decisões arquiteturais

### 1. ctx único com ~60 campos vs sub-módulos

Considerei quebrar em 3 módulos (grid principal + Composição + Ponta). Escolhi ctx único pela mesma razão do piloto W3d: simplicidade de coordenação no simCalc + espelha a estrutura linear do código original. Sub-módulos só ganham quando houver cenário com reuso (ex: Composição usada em outro card), o que não existe hoje.

### 2. Helpers locais replicados dentro do módulo

`dreH/dreN/dreL` moveram do simCalc pro módulo (privados à IIFE interna). `f2` também — redeclarado, não importado. Trade-off consciente: manter o módulo self-contained (roda em Node sem injeção), aceitando duplicação mínima de formatters.

### 3. Shadow não cobre renders

W2.5 monitora 50 campos aritméticos. Render é HTML puro — não há "divergência numérica" possível. Validação de W3d-2 é obrigatoriamente visual, por isso: smoke test sintético em Node (guards + variações condicionais) + teste ocular em produção.

### 4. Comportamentos estéticos preservados 1:1

- `1.50/kg` com ponto (do `.toFixed(2)`) em vez de `1,50` com vírgula (do `toLocaleString`): mantido conforme original. É inconsistência estética, mas fora do escopo de W3d-2 (refactor não deve mudar output).
- `fR` interna do bloco Composição usa `toLocaleString` (vírgula) enquanto o `f2` do módulo usa o mesmo → output idêntico ao antigo.

## Estatísticas

- **Linhas removidas do simCalc**: ~120
- **Linhas adicionadas no simCalc**: 32 (construção de ctx + chamada)
- **Redução líquida no HTML**: ~90 linhas.
- **Módulo novo**: ~330 linhas (com JSDoc e helpers internos).
- **Tempo do refactor**: ~1h30 (mapear + module + smoke test + substituição + validação).

## Próximos passos — W3d-3/4/5 (demais renders)

Fila:
1. **W3d-3 — `render_comparativo.js`** — Comparativo Softcomp × DRE (bloco logo abaixo do DRE, ~50 linhas inline).
2. **W3d-4 — `render_mc.js`** — Cards MC Verde/Amarela/Vermelha/Preta (~80 linhas inline).
3. **W3d-5 — `render_estoque.js`** — Bloco "Material em Estoque" (~60 linhas inline).
4. **W3e — simCalc adapter fino** — motor roda ANTES dos renders, HTML fica só `const r = motor.calcular(); render.all(r);`. Elimina o inline do Card Repasse (W3b-2 pendente) e os inlines que os renders W3d-2/3/4/5 ainda consomem de variáveis locais de simCalc.

Cada W3d pode rodar isoladamente. W3e depende de todos os W3d fecharem.

## Lições reforçadas

1. **Padrão do piloto funciona mesmo em bloco 2× maior.** W3d (corte) tinha 65 linhas inline; W3d-2 (DRE) tinha 120. Mesmo processo, mesma estrutura de módulo. Sinal de que o padrão escala.

2. **Guard no chamador, não só no módulo.** `(window.SimRender && window.SimRender.dreV4) ? ... : ''` protege contra ordem de carga de scripts. Barato, defensivo.

3. **Variáveis do IIFE interno sobem pro escopo do chamador.** As 4 MCs da Ponta (`_mcPV/A/R/P`) estavam encapsuladas na IIFE antiga. Ao extrair, viraram leituras `document.getElementById()` no simCalc e são passadas no ctx. Não há "mágica" — cada variável tem dono explícito.

4. **`node --check` no JS embutido é um sanity check barato.** Extrair inline scripts com Python regex e rodar `node --check` pega erro de sintaxe em < 1s. Vale a pena executar após qualquer edição estrutural no HTML.
