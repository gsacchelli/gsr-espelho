# 2026-04-21 — Teste Guiado Proposta Comercial

Sessão com Claude pra validar o fluxo Proposta Comercial em cenário real após o refactor de Etapas 1-4 fechado hoje de manhã. Resultado: **2 fixes críticos aplicados + 2 bugs estruturais descobertos + 3 refinos de UX mapeados**.

## Contexto

Refactor da Proposta (Etapas 1+2+3+4) fechou 21/04 de manhã. Primeira validação em cenário real (não sintético): cotação com 4 itens, cliente "Teste Usinagem/SP", MP Repasse Importada no Item 4, fases de produção em alguns itens, desconto 2% no pacote.

Fluxo planejado: Nova → preencher → Gerar → Reabrir → Revisar → Mesmo cliente. Executado até o Gerar + validação dos fixes. Passos finais (Reabrir / Revisar / Mesmo cliente) ficaram pendentes.

## Fixes aplicados

### Bug 1 — Cards de preço travados ao trocar item

**Sintoma:** os cards PREÇO REPASSE e PREÇO NEGOCIADO ficavam travados com os valores do último item ativado, mesmo ao trocar pra outro item do pacote.

**Evidência:** Item 2 (4340 Redondo, 2 Pç, Venda por Pç, **sem MP Repasse**) mostrava PREÇO REPASSE R$ 8,90/Kg · Total R$ 44.491,21 — exatamente o valor do Item 4 (15B24 5.000 Kg, MP Repasse Importada). R$ 8,90/Kg × 5.000 Kg = R$ 44.500 confirmou a origem do valor.

**Causa:** `pacoteRestoreFullState` (linhas 9262-9269) só chamava `simToggleRepasse` / `simToggleImportacao` quando o item restaurado tinha o checkbox ON. Quando trocava pra item sem repasse, nenhuma função era chamada → card persistia visível com o estado visual do item anterior.

**Fix:** chamar as 2 funções sempre. Elas leem `document.getElementById('sim-mp-repasse-on').checked` internamente e aplicam display correto pra ambos os casos (on/off).

```js
// ANTES
if(f['_chk_sim-mp-repasse-on']&&typeof simToggleRepasse==='function'){
  try{simToggleRepasse();}catch(_){}
}

// DEPOIS
if(typeof simToggleRepasse==='function'){
  try{simToggleRepasse();}catch(_){}
}
```

Mesma mudança pro `simToggleImportacao`.

### Bug 2 — Desconto de pacote sempre 0 no PDF

**Sintoma:** aplicando 2% de desconto no pacote, o PDF gerado não mostrava linha de desconto e o total permanecia bruto.

**Evidência:** PDF sem desconto mostrava Subtotal = IPI não incluso = R$ 262.925,99. Com 2% aplicado na tela, PDF continuava mostrando o mesmo valor (sem a linha "Desconto").

**Causa:** Mesma classe de bug do `simPhases` (que quebrou 3x em 21/04 manhã). `let PACOTE_DESCONTO_PCT = 0` em top-level (linha 9443) **não** expõe em `window`. Mas `propostaCalcularTotais` (linha 11422) fazia `+(window.PACOTE_DESCONTO_PCT || 0)` — sempre undefined. Resultado: desconto no cálculo = 0 independente do input do usuário.

**Fix:** ler direto do DOM. Elimina a classe de bug pela raiz — não depende mais de sincronia entre variável local e window.

```js
// ANTES
const descPct = Math.max(0, Math.min(100, +(window.PACOTE_DESCONTO_PCT || 0)));

// DEPOIS
const _descInput = document.getElementById('pacote-desconto');
const descPct = Math.max(0, Math.min(100, +(_descInput?.value || 0)));
```

**Validação matemática** (2 PDFs lado a lado):

| Campo | Sem desconto | Com 2% | Check |
|---|---|---|---|
| Subtotal | R$ 262.925,99 | R$ 262.925,99 | ✓ igual (antes do desconto) |
| Desconto | — | −R$ 5.258,52 | ✓ 262.925,99 × 2% = 5.258,52 |
| IPI não incluso | R$ 262.925,99 | R$ 257.667,47 | ✓ subtotal − desconto |
| ICMS | R$ 46.101,73 | R$ 45.179,70 | ✓ × 0,98 |
| PIS/COFINS | R$ 24.320,65 | R$ 23.834,24 | ✓ × 0,98 |
| IPI | R$ 8.545,09 | R$ 8.374,19 | ✓ × 0,98 |

Lógica econômica confirmada: desconto aplica no subtotal E escala os créditos fiscais proporcionalmente (base tributável menor → créditos menores).

## Bugs pendentes

### Bug 3 — Card PREÇO REPASSE ignora fases ativas

**Sintoma:** Item com MP Repasse + fases de produção (TT, certificações, usinagem) mostra MC negativo no card de referência.

**Exemplo (Item 04 — 15B24 10.000 Kg, MP Repasse Importada + fase TT + 5 certificações):**

| Linha | Valor |
|---|---|
| Custo MP nacionalizado | R$ 42.683,20 |
| Custo TT (TR1) | R$ 14.072,30 |
| Custo certificações | R$ 1.026,54 |
| CAP Frete CIF | R$ 2.135,15 |
| **Custo total produção** | **R$ 60.375,37** |
| Preço Negociado | R$ 8,60/Kg × 10.000 = R$ 86.000,00 |
| Venda Líquida (após desp 34,80%) | R$ 56.072,00 |
| **Resultado** | **R$ −4.303,37 · MC −7,67%** |

Card PREÇO REPASSE mostrava "-1,47% vs Repasse R$/Kg" — mas o preço de referência (~R$ 8,73/Kg) é calculado só sobre MP, ignorando R$ 17.233,99 de fases + certs + CAP. Indicador vira enganoso.

**Raiz:** semântica. "Repasse" com fases ativas não é mais repasse puro. O card precisa redefinir a referência quando há valor agregado.

**Decisão:** card REPASSE passa a incluir custo das fases. Fórmula proposta: `preco_min = (MP_nacionalizada + fases + certs + CAP) × markup_repasse / (1 - desp%)`. Implementação em `simCalcRepasse`.

**Alternativas consideradas:**
- (A) Esconder card REPASSE quando fases ativas (fall-back pros cards Verde/Amarela/Vermelha padrão que já consideram custo total) — mais limpo mas perde referência de markup mínimo
- (C) Warning visual mantendo cálculo atual — menor intervenção, menor risco

Escolhida a Opção B ("repasse honesto") — mantém o card, recalcula com custo real incluindo valor agregado.

### Bug 4 — Ponta desativa no refresh, PDF imortaliza inconsistência

**Sintoma:** Item 3 estava com ponta ativa quando gerou a proposta. Após refresh do navegador, ponta foi desativada automaticamente. Reabrindo a proposta, os valores na tela não batem com o PDF gerado anteriormente.

**Evidência:** PDF comercial enviado: "50 Pç × R$ 301,45/Kg = R$ 15.072,27". Tela pós-refresh: R$ 10,20/Kg × 1.438,01 kg = R$ 14.667,65. Números divergentes (R$ 404,62 de diferença, ~2,7%).

**Raiz:** decisão anterior (abr/2026) de não persistir `sim-ponta-on` no localStorage. A ideia era "ponta é decisão por-item, não global — faz sentido resetar no refresh". Fazia sentido quando ponta era decisão volátil. Com Proposta Comercial serializando valores calculados **com ponta**, a decisão cria inconsistência permanente entre PDF × storage × tela.

**Hipóteses do mecanismo exato:**
- **H1:** `_chk_sim-ponta-on` é capturado (linhas 9177, 9249) e o `.checked` é restaurado — mas `simTogglePonta()` não é chamado no restore. Side effects (override das margens Verde/Amarela/Vermelha/Preta pra 12/9/6/3) não são reaplicados. Mesma classe do Bug 1.
- **H2:** persistência falha num ponto anterior (ex: `pacotePersist` não serializa o flag, ou algum `simCalc` sobrescreve o checkbox antes do restore concluir).

**Fix provável (se H1):** adicionar `if(typeof simTogglePonta === 'function') simTogglePonta();` dentro de `pacoteRestoreFullState`, junto das chamadas de `simToggleRepasse`/`simToggleImportacao` que foram corrigidas no Bug 1.

**Fix mais defensivo (se H2 ou se quisermos robustez):** persistir flag dentro do snapshot v2 do pacote (no campo `pacote.itens[i].state._chk_sim-ponta-on`) em adição ao state em memória.

**Criticidade:** alta — quebra reprodutibilidade da proposta. Vendedor abre proposta antiga, vê valores diferentes do que mandou. Se cliente questionar depois, não tem como defender/explicar.

## Refinos de UX registrados

1. **Botão "🔄 Mesmo cliente" sempre visível.** Função tem proteção embutida (toast "Nenhum cliente preenchido — use 🆕 Nova" se razão social vazia). Sugestão: esconder até cliente preenchido. Interface inicial mais limpa.

2. **Campo "Reajuste" hardcoded no template PDF.** PDF mostra "REAJUSTE: Preço fixo" mas não há campo editável na tela. Causa conflito com a Observação "Reajuste cfe. usinas produtoras". Decisão: virar campo editável nas Condições Comerciais (ao lado de Pagamento/Frete/Validade/Uso).

3. **Aba MATERIAL DE PARTIDA com MP Repasse Importado mostra aço/acabamento irrelevantes.** Quando importação ativa, a MP nacional selecionada não influencia cálculo. Mostrar como display-only ou adicionar badge "ignorado — repasse importado".

4. **Label "/Kg" no PDF do Item 03 era legítimo** — peso correto (1.438 kg) × preço/kg (R$ 10,20) = R$ 14.667,65. Cliente pode confundir vendo "50 Pç × R$ 301,45/Kg". Revisitar UX do template — se unidade de venda difere da unidade de compra, talvez mostrar conversão no PDF ("50 Pç = 1.438 kg × R$ 10,20/Kg = R$ 14.667,65").

## Retificações do CLAUDE.md

1. **`window.SP` não existe.** Minha leitura anterior do CLAUDE.md dizia "IIFE precisa expor `window.SP = window.SchemaProposta`". Código real (linha 8584 + linha 9967) faz `const SP = window.SchemaProposta` como alias local em cada escopo fora do IIFE. Apenas `window.SchemaProposta` é global. Linha obsoleta do CLAUDE.md corrigida.

2. **Numeração não queima números no Nova.** `consumirProximoNumero` roda só no Gerar (linha 8932). Nova faz `peekProximoNumero` (mostra próximo sem incrementar). Os "3 números queimados" anteriormente mencionados foram consequência de Gustavo apagar manualmente propostas do storage, não do sistema. Documentação corrigida.

3. **Persistência de `sim-ponta-on` foi revisitada.** Decisão anterior passou a ser o Bug 4.

## Status da sessão

- 2 fixes críticos aplicados e validados aritmeticamente
- 2 bugs pendentes mapeados com hipóteses e fix proposto
- 3 refinos de UX registrados
- Passos 5-7 do teste original (Reabrir / Revisar / Mesmo cliente) **não executados** — com Bug 4 em aberto, Passo 5 pegaria inevitavelmente inconsistência de ponta e poluiria o diagnóstico. Pausado até Bug 4 fechado.
- CLAUDE.md atualizado com retificações + lições novas

## Próxima sessão

Dizer: `fechar bug 4 e 3 da proposta` ou `retomar teste guiado proposta após fix 4`.

Ordem sugerida:

1. **Bug 4 primeiro** (fix simples se H1 — reativar `simTogglePonta` no restore, mesma classe do Bug 1 já validado hoje). Testar se H1 é suficiente antes de ir pra H2.
2. **Validar com teste de reabertura** — confirma que ponta persiste através de refresh + reabertura da proposta. Se falhar, aplicar fix H2 (persistir no snapshot v2).
3. **Bug 3** (mais trabalho — mexer em `simCalcRepasse` pra incluir fases no cálculo de preço mínimo). Considerar gate de cobertura real — capturar fixture com Repasse + fases antes de codar.
4. **Retomar Passos 5-7 do teste guiado original** (Reabertura + Revisar + Mesmo cliente).
5. **Refinos de UX** da task #8 em batch (esconder "Mesmo cliente" sem cliente, campo Reajuste editável, badge na aba Material de Partida com Repasse Importado, label /Kg no PDF).

## Aprendizado meta

**2 fixes, 2 bugs — mesma classe raiz.** Bug 1 (cards travados) e Bug 4 (ponta no refresh) são literalmente idênticos: `pacoteRestoreFullState` seta checkbox mas não dispara handler que aplica side effects. Já foi fixado pra `simToggleRepasse`/`simToggleImportacao`; precisa estender pra `simTogglePonta` (e auditar os outros `_chk_*` da linha 9249 — `sim-cert-on`, `sim-min1kg-override`, `sim-mtl-comp-on`, `sim-rep-ratear` — todos podem ter o mesmo padrão).

Bug 2 (desconto) + Bug anterior `simPhases` também são mesma classe: `let X = 0` em top-level não cria `window.X`. Regra pra frente: **qualquer variável de estado global que precise ser lida por outro escopo fora do IIFE nasce como `window.X = ...` ou é lida direto do DOM**. Nunca confiar em `let X` esperando que funcione como global.

Vale auditar o arquivo HTML inteiro atrás de outros `let FOO = ` em top-level que tenham pares `window.FOO` em leitura — é ambiente de bug estrutural escondido.
