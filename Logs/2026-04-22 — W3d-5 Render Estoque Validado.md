---
data: 2026-04-22
tipo: log
projeto: Simulador Precificação
fase: W3 Wrapper Fino — W3d-5 (última extração antes do W3e)
status: fechado
---

# W3d-5 — Render Estoque validado em produção

## Resultado

Bloco "Estoque & Custo MP" (#sim-estoque) extraído do `simUpdateEstoque` monolítico para módulo puro `render_estoque.js`. Último render a sair do simCalc antes do W3e. Série W3d agora completa: 5/5 renders extraídos (corte piloto + dre + comparativo + mc + estoque).

Validado em produção por Gustavo: "testado, ok".

## Entregue

### Módulo render

- **`03_Ferramentas/js/render_estoque.js`** (~108 linhas) — IIFE + `window.SimRender.estoqueV4 = render` + `module.exports` (dual Node/browser). Helpers pt-BR nativos (`fmt0`/`fmt1` com toLocaleString) já no nascimento. Assinatura: `render(ctx) → { visible, html, borderLeftColor }`. Guards: se !ctx ou sem liga → `{ visible: false, html: '', borderLeftColor: '' }`. Módulo não acessa DOM — wrapper aplica `innerHTML`, `borderLeftColor` e `display`.

- **`03_Ferramentas/js/render_estoque.smoke.js`** (~140 linhas) — 48 asserts em 10 seções: guards, render mínimo, semáforo (Verde/Amarelo/Vermelho, incluindo variante lowercase), cobertura (3 ramos cobColor), atrasado destacado, data ref (7 dias → muted, 20 dias → laranja, sem dataRef → '—'), formatação pt-BR (com asserts negativos), estKg=0, sem acabamento. **48/48 PASS.**

- **HTML wrapper** — `<script src="js/render_estoque.js"></script>` adicionado na L.240 (após `render_mc.js`). Bloco inline de ~24 linhas na `simUpdateEstoque` (L.8799-8822: semáforo + helpers + date/cobColor + line1/line2 + innerHTML + borderLeftColor + display) substituído por 24 linhas de ctx estruturado (~18 campos) + chamada com guard + aplicação DOM. Mesmo número de linhas, arquitetura separada: wrapper = busca no `DATA.estoque` + cálculo de OCs (atrasado/mesAtual/proximo); módulo = string HTML + efeitos visuais declarativos.

## Decisão arquitetural

- **Single-ctx com retorno estruturado** (não fragments object como W3d-4). Justificativa: bloco tem DOM único (`#sim-estoque-content`), não 5 sub-cards. Retorno `{ visible, html, borderLeftColor }` cobre os 3 efeitos colaterais da função original (innerHTML + borderLeftColor + display). Padrão mais simples que W3d-4 (fragments object) e coerente com W3d-2/W3d-3.

- **Busca e cálculo ficam no wrapper.** A `simUpdateEstoque` original fazia 3 coisas: (1) guards de visibilidade + busca no `DATA.estoque`, (2) cálculo de OCs por mês (atrasado/mesAtual/proximo), (3) render. Só (3) foi pro módulo. Justificativa: busca depende de `DATA.estoque` (estado global) e cálculo depende de `DATA.estoque.ocMonths` + `item.oc[]` — mover pra módulo puro exigiria passar o DATA inteiro. Separação clara: wrapper lida com dados/estado, módulo lida com apresentação.

- **Sweep pt-BR grátis.** Única herança US no original era `item.de.toFixed(1)` (gera `Ø25.4mm`). Já nasceu corrigido no módulo com `fmt1(de)` → `Ø25,4mm`. Os outros helpers do bloco original (`fmt0`/`fmt1`) já usavam `toLocaleString('pt-BR')` — nada mais a varrer.

## Validações

- Smoke tests Node: **202/202 PASS** na suite render completa (48 mc + 48 dre + 58 comparativo + **48 estoque**). Antes do W3d-5 era 154/154.
- `node --check` no JS embutido do HTML (687k chars após refactor): **SYNTAX OK**.
- Shadow bloqueante (W2.5) continua ativo, 0 divergências aritméticas. Shadow não cobre render (é aritmética-only).
- Validação visual em produção: Gustavo abriu cotações com material em estoque, ativou MP Repasse (card somem), conferiu semáforo/cobertura/data ref. Resposta: "testado, ok".

## Estatísticas

- Linhas adicionadas em `js/`: render_estoque.js (~108) + render_estoque.smoke.js (~140) = ~248 linhas.
- Linhas no wrapper: mesmas ~24 (ctx + chamada + guard + aplicação DOM). Mesmo volume, arquitetura diferente.
- Tamanho do HTML: 689k → 687k chars (leve redução por remoção dos helpers `fmt0`/`fmt1`/`semaLabel` etc inline).
- Suite total render: **202/202 PASS**. Motor principal intacto: 764/764.
- Tempo de execução: ~25min (módulo + smoke + substituição + validação).

## Série W3d — fechada

| # | Módulo | Linhas | Smoke | Validado |
|---|---|---|---|---|
| W3d piloto | `render_corte.js` | ~125 | — (débito leve) | ✓ 22/04 |
| W3d-2 | `render_dre.js` | ~380 | 48/48 | ✓ 22/04 |
| W3d-3 | `render_comparativo.js` | ~160 | 58/58 | ✓ 22/04 |
| W3d-4 | `render_mc.js` | ~145 | 48/48 | ✓ 22/04 |
| W3d-5 | `render_estoque.js` | ~108 | 48/48 | ✓ 22/04 |

5/5 renders extraídos. Sweep pt-BR fechado em todos. Total suite: **202/202**.

## Próximos passos

1. **W3e — simCalc adapter fino.** Este é o passo que materializa o ganho estrutural do sprint W3. Consolida os cards do motor (`cards.repasse` já bate bit-idêntico em 60/60 campos no shadow) como fonte única e apaga inline que sobrou. Série W3d completa é o pré-requisito — agora cumprido.
2. **Fase pós-motor de config** — migração dos hardcodes AFS (CF escalonado, certificações, fases industriais) do motor para `parametros_afs.json`. Independente do W3, mas pré-requisito pra MetalM compartilhar o motor.
3. **Débito leve** — criar smoke test pro `render_corte.js` piloto. Baixa prioridade; só se houver motivo de tocar o módulo de novo.
4. **Proposta de Exportação USD/EN** — parked desde 21/04. Meio dia de trabalho quando sinal verde.

## Lições reforçadas

- **Extração incremental paga-se em previsibilidade.** W3d-5 foi o mais rápido da série (~25min) porque o padrão já estava consolidado em 4 módulos anteriores. Mesma arquitetura, mesma estrutura de smoke test, mesmo fluxo de substituição. A primeira extração (piloto) foi a cara; as seguintes ficam quase automáticas.
- **Retorno estruturado > callback pra renders single-element.** Módulo puro retornando `{ visible, html, borderLeftColor }` em vez de receber callback pra aplicar DOM. Justificativa: teste unitário fica trivial (valida a struct, não mocka DOM). Wrapper paga custo mínimo de legibilidade (3 linhas de `if (frag.visible) { ... } else { ... }`).
- **Herança US em formatação é silenciosa mas pega fácil.** `item.de.toFixed(1)` passou por todos os reviews anteriores porque ninguém notou — até a lição do W3d-3 (Gustavo flagou "formato dólar"). Agora todo módulo novo nasce com helpers pt-BR nativos e smoke test com asserts negativos pra formato US.
- **Separação render vs. busca simplifica testes.** Tentativa alternativa seria passar `DATA.estoque` inteiro + `liga/perfil/bitola` pro módulo e ele fazer busca. Deixaria o módulo acoplado ao schema de `DATA.estoque`. Manter busca no wrapper e passar ctx plano pro módulo = módulo testável sem mock de estado global.
