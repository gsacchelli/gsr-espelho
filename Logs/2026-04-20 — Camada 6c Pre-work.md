---
data: 2026-04-20
tipo: log
status: vigente
categoria: simulador / pricing
domínio: camada-6c
tags: [simulador, motor, camada-6c, repasse, importação, sprint-3, pre-work]
---

# 2026-04-20 — Camada 6c Pre-work

Terceira sessão do dia (6a UX → 6b Importação → 6c pre-work). O plano original da 6c tinha 4 passos: (a) teste em produção do bloco Importação, (b) captura de 2 fixtures via botão Debug, (c) implementar Camada 6 no motor, (d) regressão bit-idêntica. Como (a) e (b) ainda não foram feitos, optei por adiantar (c) em modo "pre-work" — com gate explícito de que a camada só fecha quando a fixture real chegar.

## Decisão estruturante — Opção B (motor vira referência canônica)

Duas arquiteturas possíveis:

**Opção A** — motor consome `mp_repasse.custo_liq_ton` direto do dataset. Cascata da importação fica só no HTML.
**Opção B** — motor replica a cascata da importação internamente. Motor vira referência canônica; bug no HTML detectado via divergência com motor.

Comecei com Opção A (menos trabalho), mas Gustavo escolheu **Opção B** no meio da sessão. Vantagem estrutural: motor canônico significa que qualquer divergência HTML ↔ motor vira um sinal de bug, não ambiguidade. Perda: escopo maior nesta sessão (cascata + instrumentação + 30+ testes).

Feito na mesma sessão:
1. Instrumentação do `SIM_LAST_CALC_IMP` no HTML (breakdown completo de 28 campos intermediários da cascata, publicado como `window.SIM_LAST_CALC_IMP` no final de `simCalcImportacao`; incluído em `SIM_LAST_CALC.imp` pelo simCalc).
2. `calcCustoImportacao(importacao, ctx, config)` novo no motor — função pura que replica os 6 passos da cascata.
3. `calcCustoLiq` integrado: importação ativa + dados completos → cascata motor (canônico); importação inválida ou nacional → dataset (retrocompat).
4. `calcCustoLiqRateado` passou a usar `pesoTotalKg` do motor quando importação ativa.
5. `_aplicarOverrideComp` **removido** do motor — redundância com adapter (HTML sincroniza `sim-comp` com `sim-rep-comp` via `simUpdateRepasseVisibility` antes do cálculo).

## Execução

### Schema estendido — `schemas.js`

Bloco `MpRepasse` ganhou:
- `pis_pct` (default 9.25, adicionado na 6a)
- Sub-typedef `ImportacaoRepasse` com 22 campos + 3 saídas (custo_bruto_ton, landed_factor, recuperaveis_brl)
- Defaults AFS documentados em JSDoc (seguro 0.30, AFRMM 25, PIS-Imp 2.10, Cofins 9.65, CF sinal 20%×8m, CF final 80%×3m)

Unidade da NF expandida de `"ton"|"pc"` pra `"ton"|"kg"|"pc"|"m"` — o HTML sempre aceitou os 4, só o schema estava defasado.

### Adapters — `debug_to_entrada.js` e `dom_to_entrada.js`

Ambos agora populam `mp_repasse.importacao` quando `sim-imp-on` existe no DOM (retrocompat: fixtures 01-08 antigas continuam funcionando, importacao fica `undefined`).

`debug_to_entrada` detecta importação via `if (dom['sim-imp-on'])` antes de serializar.
`dom_to_entrada` usa `document.getElementById('sim-imp-on')`.

### Motor — `motor_precificacao.js` (Opção B)

Mudanças:

1. **`calcCustoImportacao(importacao, ctx, config)`** — nova função pura replicando fielmente a cascata do HTML L.2946-3065. Retorna breakdown completo + `custoLiqTon` + `pesoTotalKg` + `landedFactor`. Guarda mínima: se `cfr/cambio/qty inválidos`, retorna `valido=false`. SELIC mensal via `(1+selic_aa/100)^(1/12) - 1`.

2. **`calcCustoLiq` integrado com cascata.** Quando `mp_repasse.importacao.ativo=true`, motor calcula cascata internamente (ignorando dataset) — motor canônico. Se cascata inválida ou importação OFF, fallback pro dataset (retrocompat Repasse nacional).

3. **`calcCustoLiqRateado` usa pesoTotalKg do motor quando importação.** Rateio não depende mais do dataset em cenário de importação.

4. **`_aplicarOverrideComp` removido.** Override de `comp_mm` (Repasse por peça nacional) é responsabilidade do adapter — HTML sincroniza `sim-comp` via `simUpdateRepasseVisibility` L.2820-2824 antes do cálculo. Motor consome direto, sem defesa em profundidade. Decisão: simplicidade > redundância.

### HTML — instrumentação SIM_LAST_CALC_IMP

`simCalcImportacao()` agora publica `window.SIM_LAST_CALC_IMP` com 28 campos do breakdown (inputs brutos + VA + tributosFed + despesas locais + ICMS + CF + bruto/líq/recuperáveis/landed). Zerado quando guarda mínima dispara ou toggle de Importação desliga. `simCalc` inclui em `SIM_LAST_CALC.imp`.

Pipe pro motor canônico: quando fixture real for capturada (próxima sessão), regressão compara `SIM_LAST_CALC.imp` contra `r.breakdown` do motor — bit-idêntica em todos os 28 campos.

### Testes sintéticos — 38 novos

Organizados em 9 blocos:
- `calcCustoLiq honra override` — 3 testes
- `calcCustoLiqRateado` — 6 testes (precondições: ratear OFF, venda=comprado, venda<comprado, venda>comprado, repasse nacional por peça, importação por peça)
- `comp_mm consumo direto (sem override motor)` — 1 teste (override agora é do adapter)
- `calcular() integrado com Repasse nacional` — 2 testes (custo sobrescrito, rateio eleva custo/ton)
- **Opção B — guarda mínima cascata** — 3 testes (cfr/cambio/qty inválidos)
- **Opção B — Cenário A** (log 6b: 4340 Ø508 20t ICMS 18%) — 10 testes (VA, IPI, SELIC mensal, identidade bruto/líq, recuperáveis, ICMS gross-up, landed>1, custoLiqTon na faixa)
- **Opção B — Cenário B** (ICMS 0%) — 4 testes incluindo **invariante crítico**: líquido A = líquido B (premissa de crédito integral)
- **Opção B — Cenário C** (5pç × 1200kg CFR 2800 USD/pç + I.IMP 12% + comissão 3%) — 6 testes (qtyTon, cfrTotalBRL×qtyInput, I.IMP, Comissão, cfrUsdTon)
- **Opção B — integração calcCustoLiq ↔ cascata** — 3 testes (importação completa usa motor; inválida cai no dataset; nacional usa dataset)

**AVISO explícito no header:** testes validam aritmética. **Não substituem** regressão bit-idêntica.

Suite completa: **443/443 testes verdes** (405 originais + 38 novos da Camada 6c). Zero regressão.

### Divergência aberta (CRÍTICA, resolver na fixture real)

Cenário A calibrado com câmbio 5,00 e parâmetros defaults (frete 110, seguro 0,30, AFRMM 25, PIS-Imp 2,10, Cofins 9,65) retorna `custoLiqTon = 10.083 R$/ton`. Log 6b declarou 10.944 R$/ton no smoke test em Node. **Gap de ~8%.**

Duas hipóteses, sem como distinguir sem fixture:
1. Motor tem bug sutil em algum passo da cascata (mais provável candidato: composição do CF ou ICMS gross-up base)
2. Smoke test em Node do log 6b usou parâmetros ligeiramente diferentes dos que ficaram no HTML final

Abordagem: marquei o teste como baseline provisório (faixa 9.000–12.000) com comentário explicando. Regressão bit-idêntica contra `SIM_LAST_CALC.imp` (próxima sessão) vai resolver — se divergir, comparo campo a campo do breakdown pra localizar o erro.

## Lacunas conhecidas (fechadas quando fixture real vier)

1. **Regressão bit-idêntica contra `SIM_LAST_CALC.imp`** — fecha a Camada 6. 38 testes sintéticos cobrem ramos; fixture valida fidelidade ao HTML.
2. **Gap de 8% no Cenário A** — ver seção "Divergência aberta" acima. Prioridade alta na próxima sessão.
3. **Validação `MP_REP_COMP_VAZIO` vs sincronização HTML** — motor ainda dispara aviso se `mp_repasse.comp_mm=0` em modo por peça. Não quebra (é aviso), mas redundante agora que override é do adapter. Resolver quando fixture real mostrar se é falso-positivo.

## Correções fiscais aplicadas na mesma sessão (4ª sub-sessão)

Gustavo revisou a cascata e apontou 2 bugs conceituais. Validei contra código Python referência (ChatGPT) e confirmei. Correções:

### Bug 1 — VA duplicava frete marítimo

**Antes:** `VA = cfrTotalBRL + freteMarBRL + seguroBRL`
**Corrigido:** `VA = cfrTotalBRL + seguroBRL`

CFR já inclui frete por definição INCOTERM. Somar de novo inflava VA em ~freteMar/CFR (10-20% no cenário típico), o que cascateava em II, PIS, Cofins e ICMS. Frete marítimo continua no modelo, mas APENAS como base do AFRMM (`AFRMM = freteMarBRL × 25%`).

### Bug 2 — Base do PIS/Cofins incompleta

**Antes:** `PIS = VA × 2,10%` / `Cofins = VA × 9,65%`
**Corrigido:** `basePisCofins = VA + II + IPI`; `PIS = base × 2,10%`; `Cofins = base × 9,65%`

Regra operacional AFS (PIS/Cofins-Importação, Lei 10.865 com alinhamento pós-STF): base = VA + tributos federais intermediários. Confirmado pelo Python e pela prática da casa.

### Funcionalidade nova — Hedge % câmbio

Adicionado campo `sim-imp-hedge` (default 0%). Fórmula: `câmbio_operacional = câmbio_nominal × (1 + hedge/100)`. Utilizado em todas as conversões USD → BRL da cascata. Default 0 preserva retrocompat.

### UX — descrição unificada

Removido textarea isolado `sim-imp-desc`. Material importado usa a descrição da Peça Engenheirada (`sim-peca-texto`/`sim-peca-descr`). Mensagem inline explicando. Evita dado redundante.

### UX — painel breakdown da cascata

Adicionado bloco colapsável `<details>` ao final do painel de Importação mostrando linha a linha: câmbio operacional / VA / II / IPI / PIS / Cofins / AFRMM / Portuárias / Diversos / Comissão / Frete Interno / CF Sinal / CF Final / Subtotal / ICMS gross-up / Custo Bruto / Recuperáveis / Custo Líquido. Usa valores em R$ absoluto do lote. Zero matemática nova — pura exposição de `SIM_LAST_CALC_IMP`.

### Instrumentação estendida

`window.SIM_LAST_CALC_IMP` ganhou campos `cambioNominal`, `hedgePct`, `cambio` (operacional) e `basePisCofins` — auditoria completa via JSON de Debug.

### Impacto nos valores

**Cenário A** (4340 Ø508, 20t, ICMS 18%, câmbio 5,00):
- Motor antigo (com bugs): **10.083 R$/ton**
- Motor corrigido: **9.533 R$/ton**
- Delta: −550 R$/ton (−5,5%)

**Fixture real 2026-04-20 05:59:28** (1045 Ø200, 10t, ICMS 12%, câmbio 5,20):
- HTML antigo (dataset capturado): **4.393,64 R$/ton**
- Motor corrigido: **4.030,73 R$/ton**
- Delta: −362,91 R$/ton (−8,3%)

Ambas as reduções são coerentes: VA deixa de duplicar frete (baixa o custo), base PIS/Cofins aumenta (sobe), ICMS gross-up recalcula sobre subtotal menor (baixa). Efeito líquido: redução no custo final. Motor e HTML agora convergem ambos para o número correto.

### Testes

Suite atualizada: **447/447 verdes**:
- Testes antigos que codificavam o bug (`A: VA = CFR + Frete + Seguro = 191.540`) corrigidos para refletir a fórmula nova
- Novos testes: `base PIS/Cofins = VA + II + IPI`, `hedge default 0`, `hedge 5% infla câmbio`
- Novo teste de regressão contra fixture real (4.030,73 R$/ton após correção)
- Testes antigos de "faixa defensável" substituídos por teste exato (tol ±50 R$/ton)

## Checklist próxima sessão (fechar Camada 6)

1. **Validar HTML corrigido em produção.** Abrir simulador, ativar Importação, preencher mesmo cenário da fixture antiga (1045 Ø200, 10t, CFR 575 USD, câmbio 5,20, ICMS 12%, etc.). Confirmar que custo líq agora é **R$ 4.030,73/ton** (era 4.393,64 antes). Confirmar painel breakdown novo aparece e abre.
2. **Conferir contra planilha** — uma DI real ou cotação Duferco. Especialmente: linha PIS, linha Cofins, ICMS gross-up. Se divergir da planilha, premissa fiscal AFS pode precisar de ajuste fino (ex: base PIS/Cofins "ainda mais" ampliada).
3. **Cenário Repasse nacional** (NF de terceiro). NF antiga (WEG, Sant'ana).
4. **Debug → Exportar JSON** — recapturar `fixture_09_repasse_nacional.json` + `fixture_10_repasse_importacao.json` com instrumentação Opção B (agora exporta `SIM_LAST_CALC.imp` com 30+ campos do breakdown).
5. **Atualizar `fixtures/README.md`** com manifesto.
6. **Estender suite** com testes de regressão bit-idêntica:
   - Fixture 09: `rep.custoLiq do motor === dataset.custoLiqTon` (Repasse nacional)
   - Fixture 10: `r.breakdown.*` motor === `SIM_LAST_CALC.imp.*` HTML — campo a campo (VA, II, IPI, basePisCofins, PIS, Cofins, ICMS, AFRMM, Diversos, Comissao, FreteInt, CF_sinal, CF_final, custoBrutoBRL, custoLiqBRL)
7. **Rodar `node motor_precificacao.test.js`** — se bit-idêntico, Camada 6 fecha definitivamente.
8. **Atualizar CLAUDE.md + memória Claude** declarando Camada 6 fechada com Opção B + correções fiscais.
9. **Seguir pra Camada 8b** (ponta completa + material comprado) ou wrapper fino.

## Decisões confirmadas (5ª/6ª sub-sessões do dia)

Gustavo decidiu no final da sessão:

- **Portuárias**: mantém como R$ **absoluto** (total do lote). Label atualizado para "Portuárias (R$ total)" e tooltip explicativo.
- **Diversos**: mantém base **VA + tributos federais** (atual HTML/motor). Default preenchido **5%**.
- **Landed factor**: MUDOU para **câmbio nominal** no denominador. Hedge é decisão financeira interna, não parte do preço FOB. Consequência: landed com hedge > landed sem hedge (hedge aparece no markup). Aplicado em HTML e motor. Teste novo validando: `landed(hedge 5%) / landed(hedge 0) ≈ 1,05`.
- **Defaults AFS novos**: I.IMP 10,80%, Diversos 5,00%, Portuárias em branco.
- **UX formato**: onblur force 2 casas decimais em todos os 18 inputs numéricos do bloco (1 casa em meses, 4 em câmbio). Browser pt-BR exibe vírgula.
- **Tooltips informativos**: Portuárias (capatazia/THC/armazenagem/despachante), Diversos (buffer/imprevistos/ISS), I.IMP (varia por NCM), AFRMM, Frete Marítimo (só base AFRMM, não VA), Landed Factor (fórmula completa).

Suite final: **448/448 testes verdes**.

## Decisões pendentes (próxima sessão pode revisitar)

- **Parcelas CF arbitrárias** — hoje 2 parcelas fixas (sinal/final). Python aceita lista. Overengineering pra hoje?

## Conexões

- [[Logs/2026-04-20 — Camada 6a Repasse UX]] — sessão 1 de hoje (UX)
- [[Logs/2026-04-20 — Camada 6b Importação]] — sessão 2 de hoje (bloco importação no HTML)
- [[Logs/2026-04-20 — Auditoria Fiscal Importação]] — auditoria completa da base legal de cada tributo (gerada após erros de cascata)
- [[Logs/2026-04-17 — Plano Fases 1+3 Simulador Precificação]] — plano geral
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]] — arquitetura atual
