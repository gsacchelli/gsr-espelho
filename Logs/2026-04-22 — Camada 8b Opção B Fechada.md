---
data: 2026-04-22
tipo: log
status: vigente
---
# 2026-04-22 — Camada 8b Opção B Fechada (DRE Camada 2 no motor)

Fechamento formal da decomposição gerencial do spread total (DRE Camada 2) no motor. Paridade bit-idêntica com HTML validada via fixture real capturada em produção.

## Escopo entregue

Todos os spreads gerenciais de `simCalc L.4988-5030` agora vivem no motor como função pura `calcDRECamada2()`:

**A — Derivados dos items[]:**
- `mc2_servicos_rs` — margem cobrada em fases ext (TT/TD/USX/EMB) + cert externa
- `mc2_certs_int_rs` — receita INTEIRA de cert interna (custo + margem junto)
- `mc2_mtlcomp_rs` — margem cobrada em material comprado
- `mc2_servPedido_rs` — margem cobrada em CAP (fase_pedido)

**B — Cobrado vs real × valorBase:**
- `mc2_fin_rs` = (cfCob − cfReal)/100 × valorBase
- `mc2_dv_rs`  = (dvaCob − dvaReal)/100 × valorBase
- `mc2_log_rs` = (logCob − logReal)/100 × valorBase
- `mc2_com_rs` = (comCob − comReal)/100 × valorBase

**C — Inflados pela MC ativa do card selecionado:**
- `spread_corte_dre_rs` = mc2_corte × inflator − custoRealCorte
- `spread_min1kg_infl_rs` = spreadMin1kgVal × inflator
- `corte_cobrado_preco_rs` = mc2_corte × inflator
- `inflator` = 1/(1−mcBaseEff); `mc_base_eff_pct`

**D — Spread Peça (Softcomp vs Real):**
- `spread_lamina_rs` = coef × (lamSoft − lamReal) × qtyPcs × custoTon/1000
- `spread_tol_rs` = coef × (tolSoft − tolReal) × qtyPcs × custoTon/1000
- `spread_peca_total_rs` = lamina + tol

**E — Cross-term:**
- `cross_term_rs` = valorBase × icms × pis (se !abaterERP)

Total: `spread_total_rs` soma de todos.

## Arquivos modificados

- `03_Ferramentas/js/motor_precificacao.js`
  - Nova função `calcDRECamada2(args)` pura
  - Nova função `aplicarCAP(items, entrada)` — injeta CAP pré-rateado como `fase_pedido`
  - `dre.camada2`, `dre.custo_serv_pedido_rs` expostos no retorno
  - `dreCustoTotal` agora soma `dre_custoServPedido` (bug de paridade corrigido)
  - Bump `motor_versao: '1.1-camada8b-mtlcomp'`
- `03_Ferramentas/js/debug_to_entrada.js`
  - `_extrairMtlComp(dom)` — lê `sim-mtlc-*` e converte NF → custo líq
  - `_extrairCAP(fixture)` — lê localStorage `sacchelli-simulador-proposta-meta`
  - Adapter agora popula `entrada.material_comprado` e `entrada.custos_adicionais_pedido`
- `03_Ferramentas/Analise_Precificacao_Sacchelli.html`
  - Instrumentação `window.SIM_LAST_CALC.camada2` com 22 campos dos spreads
  - Bump `versao_instrumentacao: '1.1-camada2-spreads'`
- `03_Ferramentas/js/motor_precificacao.test.js`
  - Suite DRE Camada 2 — spreads isolados A/B/C/E + combinado (14 testes sintéticos)
  - Suite Fixture 11 regressão bit-idêntica (18 testes)
- `03_Ferramentas/js/fixtures/fixture_11_camada2_combinado.json`
  - Cenário "Teste 8b" em produção: TT TR1 10% + cert int + cert ext + MtlComp Caixa Especial 15% + CAP Frete 10%, abaterERP=OFF

## Resultado

**531/531 testes verdes** (499 → 531, +32 testes novos).

Paridade bit-idêntica em 14/14 campos do card Vermelha na fixture real:

```
Campo                     | motor         | HTML          | diff
-------------------------------------------------------------------
mc2_servicos_rs           |    161.849722 |    161.849722 | ✓
mc2_certs_int_rs          |     30.162288 |     30.162288 | ✓
mc2_mtlcomp_rs            |     32.029412 |     32.029412 | ✓
mc2_servPedido_rs         |     50.416667 |     50.416667 | ✓
mc2_fin_rs                |     91.389613 |     91.389613 | ✓
spread_corte_dre_rs       |    154.598171 |    154.598171 | ✓
cross_term_rs             |     87.828979 |     87.828979 | ✓
spread_total_rs           |    608.274851 |    608.274851 | ✓
valorBase                 |   7912.520589 |   7912.520589 | ✓
```

## Lacunas retroativas assumidas (débito sem bloqueio)

1. **Rateio CAP multi-item** — adapter hoje assume single-item (100% pro ativo). Multi-item requer rateio externo pronto antes do motor. Quando houver pacote multi-item com CAP real, estender adapter pra replicar `propostaCalcRateioItemAtivo()` (por peso/valor/uniforme).

2. **Ramos `mc2_dv/log/com > 0`** — só cobertos por testes sintéticos. Capturar fixture real quando `setup-dva-real`/`setup-log-real`/`setup-com-real` forem preenchidos em cotação natural.

3. **Ramo `spread_peca > 0`** — só coberto sintético. Capturar quando vendedor preencher `sim-lamina-real`/`sim-tol-real`.

4. **Min1kg ativo + crossTerm** — só sintético. Capturar com cotação de peça leve em kg.

## Decisão arquitetural registrada

**Adapter é responsável pelo rateio.** Motor recebe CAP como lista `[{descricao, real_rs, margem_pct}]` já rateada. Rateio externo (`propostaCalcRateioItemAtivo()` no HTML) continua fora do motor porque depende do estado do PACOTE, que é concern do wrapper, não da precificação pura.

## Técnica de diagnóstico validada

Primeiro cálculo com adapter incompleto retornou `spread_total_rs` divergente (503 motor vs 608 HTML). Diff por campo revelou instantaneamente os 2 ramos faltantes (mtlcomp + CAP). Confirmou valor da regra: **diagnosticar campo-a-campo antes de procurar bug complexo.**

## Próxima frente

**Wrapper fino HTML → motor.** Objetivo: reduzir simCalc a um adapter fino que delega tudo pro motor, sem lógica de cálculo duplicada entre os dois. Requer análise prévia de escopo antes de codar (tamanho + interdependências do simCalc justificam decisão estruturada, não execução direta).
