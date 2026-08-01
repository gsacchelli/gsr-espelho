# 2026-04-22 — Sessão Consolidada (8b fechada + W2.5 + W3b-1 + W3c + W3b-2 + W3d piloto)

Sessão longa (~6h) consolidando 6 frentes significativas do motor + wrapper fino do simulador. Todas protegidas pelo shadow bloqueante desde o meio da sessão — 2 bugs reais pegos no primeiro uso.

## 1. Camada 8b Opção B — DRE Camada 2 completa no motor (FECHADA)

Decomposição gerencial do spread total saindo do HTML para função pura do motor.

**Entregue:**
- `calcDRECamada2(args)` — decompõe spread total em 14 campos (mc2_servicos, mc2_certs_int, mc2_mtlcomp, mc2_servPedido, mc2_fin/dv/log/com, spread_corte_dre, spread_min1kg_infl, spread_peca_total, cross_term).
- `aplicarCAP(items, entrada)` — injeta CAP pré-rateado como `fase_pedido` no items[].
- `dre.camada2` + `dre.custo_serv_pedido_rs` expostos no retorno do motor.
- Bug de paridade corrigido: motor não somava `dre_custoServPedido` em `dreCustoTotal`.

**Validação:** fixture 11 "Teste 8b produção" (TT TR1 10% + cert int + cert ext + MtlComp Caixa Especial 15% + CAP Frete 10%, abaterERP=OFF) — **14/14 campos bit-idêntica** contra HTML. `spread_total_rs = 608.27`.

**Testes:** 14 sintéticos + 18 bit-idênticos fixture 11. `motor_versao: 1.1-camada8b-mtlcomp`.

## 2. W2.5 Shadow Bloqueante (instalado)

Promoção do shadow mode de diagnóstico (opt-in) a proteção contra regressão silenciosa.

**Entregue:**
- `_simMotorDiff()` estendido de 29 → 50 campos (Camada 2 completa + valorBase).
- Toggle `setup-motor-alert-on` default ON (não persistido — F5 sempre restaura proteção).
- Toast persistente sem auto-dismiss (fecha manualmente).
- Audit log rolling em `localStorage.afs_motor_divergencias` (50 entradas).
- Limpa toast fantasma quando divergência zera.

**Design defensivo:** toggle não persiste em LS → qualquer reload volta pra proteção ON.

## 3. W3b-1 — simCalcRepasse → motor (VALIDADO EM PRODUÇÃO)

Primeiro módulo de wrapper fino. Conversão de Repasse Nacional pro motor.

**Entregue:**
- `calcCustoRepasseNacional({nf, icms, pis, unidade, qty, comp_mm, perfil, de_mm, di_mm})` — função pura.
- HTML `simCalcRepasse` reduzido de ~65 linhas mistas para ~40 linhas de I/O puro.

**Testes:** 15 sintéticos (ton/kg/pc/m × 5 perfis × casos borda fiscais).

**Validação em produção:** Gustavo validou MP Repasse + unidade Kg com NF real, nenhuma divergência no shadow.

## 4. W3c — simCalcImportacao → motor (VALIDADO EM PRODUÇÃO)

Refactor mais cirúrgico da noite. Motor já tinha `calcCustoImportacao` desde Camada 6c — HTML passou a delegar.

**Entregue:**
- HTML `simCalcImportacao`: ~100 linhas de cascata fiscal removidas. Delega pra `window.MotorPrecificacao.calcCustoImportacao(...)`.
- Mantém só: coleta de inputs, render de breakdown (40+ campos), dataset, SIM_LAST_CALC_IMP.
- Impossível motor divergir do HTML em importação — mesma função.

**Validação:** 546 testes verdes. Fixture 10 já cobria paridade bit-idêntica. Produção sem divergência.

## 5. W3b-2 — Card Repasse no motor (instrumentado, aguardando validação)

Bloco que causou Bug 3 v1→v4 em cascata (21/04). Motor agora calcula `cards.repasse`.

**Entregue:**
- Nova função interna `_recalcTotalVRepasse(mp, cp, ct, mgMpRep)` no motor.
- `cards.repasse = { ativo, preco_total_rs, mc_svl_pct, mg_mp_rep_pct, unit_prices: {pc, kg, m} }`.
- HTML expõe `cardValRep` + `msvlRep` em SIM_LAST_CALC.
- Shadow diff compara motor × HTML (2 campos adicionais).

**Estado:** cálculo inline ainda existe no HTML (shadow motor roda DEPOIS do render). No W3e (simCalc adapter), motor roda antes e o inline morre.

**Testes:** 7 sintéticos (ausência/ativação/mg_mp_rep_pct relativo/unit_prices).

## 6. W3d piloto — render_corte.js (Detalhamento do Corte v4)

Primeiro módulo de render extraído. Padrão validado.

**Entregue:**
- `03_Ferramentas/js/render_corte.js` — função pura `SimRender.corteV4(ctx)` → HTML string.
- HTML `simCalc` substituiu 65 linhas de innerHTML inline por 18 linhas de chamada ao módulo.

**Validação:** smoke test em Node (null → '', sem cutV4 → '', contexto completo → 5.5KB de HTML com equipName/grupo/spread corretos, pontaAtivo=false sem bloco ponta).

## Bugs pegos pelo shadow em 1 dia de uso

### Bug #47 — CAP faltando em dom_to_entrada
Primeira cotação real após W2.5: toast "Motor diverge em 28/57 campos" com `totalCusto: Δ R$ 453,75`.

**Causa:** estendi `debug_to_entrada.js` (fixtures) com `_extrairMtlComp` + `_extrairCAP` mas não estendi `dom_to_entrada.js` (produção). Shadow bloqueante pegou na primeira tentativa.

**Fix:** adicionado `_cap()` em `dom_to_entrada.js` chamando `window.propostaCalcRateioItemAtivo()` — mesma fonte do HTML. Caiu 28→4.

### Bug #49 — Toast fantasma
Após fix CAP, toast continuava mostrando "4/57 campos divergentes" mesmo com motor bit-idêntico em console.

**Causa:** toast persistente (W2.5 design) nunca era removido quando divergência zerava. Ficava órfão de sessão anterior.

**Fix:** `simCalc` agora remove toast fantasma automaticamente quando `_diff.divergencias === 0`.

**Lição arquitetural:** `debug_to_entrada.js` e `dom_to_entrada.js` precisam andar em paralelo. Qualquer campo novo em um exige espelho no outro. Shadow bloqueante garante que drift é pego no primeiro teste em produção.

## Estatísticas agregadas

- **Testes motor:** 499 → 553 (+54 novos na sessão).
- **Arquivos criados:** `render_corte.js`, `fixture_11_camada2_combinado.json`, `fixture_12_pos_cap_fix.json`.
- **Arquivos modificados:** `motor_precificacao.js`, `motor_precificacao.test.js`, `dom_to_entrada.js`, `debug_to_entrada.js`, `Analise_Precificacao_Sacchelli.html`.
- **Frentes fechadas:** 5 (Camada 8b, W2.5, W3b-1, W3c, W3d piloto).
- **Frente instrumentada:** 1 (W3b-2, aguarda validação em produção).

## Decisões arquiteturais registradas

1. **CAP multi-item fica como débito.** Adapter hoje assume single-item (100% pro ativo). Quando houver multi-item com CAP real, rateio precisa vir pronto do chamador — motor não conhece PACOTE.

2. **Shadow bloqueante é proteção, não validação.** Motor e HTML podem ter o mesmo bug — shadow só detecta quando UM deles muda sem o outro acompanhar. Autoridade continua sendo a bateria de testes do motor + fixtures reais.

3. **Toggle `setup-motor-alert-on` não persistido.** Design defensivo: F5 sempre restaura proteção ON.

4. **Render inline do Card Repasse mantido temporariamente.** Motor roda no fim do simCalc (shadow) — se eu delegar o render agora, motor ainda não calculou. W3e (simCalc adapter) é o momento certo pra matar o inline.

## Backlog W3 (próximas sessões)

- **W3b-2 — validação em produção:** F5 + MP Repasse ativo, observar se shadow mostra divergência em `cards.repasse.preco_total_rs` ou `cards.repasse.mc_svl_pct`.
- **W3d-2 — render_dre.js:** DRE do Pedido (~90 linhas).
- **W3d-3 — render_comparativo.js:** Comparativo Softcomp × DRE.
- **W3d-4/5 — render_mc.js + render_estoque.js.**
- **W3e — simCalc adapter fino:** motor roda antes do render, HTML fica só `const r = motor.calcular(); render.all(r);`.

## Lições da sessão

1. **Alinhar semântica antes de codar em área sensível** (registrado como feedback em 21/04) — hoje evitado: perguntei bloco A/B/C antes de extrair W3a, fiz piloto W3b-1 antes de W3b-2.

2. **Shadow bloqueante paga o investimento imediatamente.** W2.5 instalado de manhã, pegou 2 bugs reais à noite. Regras:
   - Default ON (confiar na proteção > conveniência).
   - Toast persistente (não pode sumir sem ação do usuário).
   - Audit log sempre grava (mesmo com alerta OFF — forense).

3. **Diagnóstico campo-a-campo antes de adivinhar.** Quando shadow mostrou 4 divergências residuais pós-fix CAP, fui pedir `console.log` de cada campo do motor × HTML antes de teorizar. Resultado: descobri que tudo batia bit-idêntico e o toast era fantasma. Teria perdido 1h adivinhando.

4. **Refactor incremental > big bang.** Dividir W3 em W3a/b-1/b-2/c/d/e permitiu parar em qualquer ponto sem deixar código pendente. Cada commit é shippable isoladamente.
