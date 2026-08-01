---
data: 2026-04-22
tipo: log
projeto: Simulador Precificação
fase: W3 Wrapper Fino — W3e (simCalc adapter fino)
status: fechado
---

# W3e — simCalc adapter fino

## Resultado

Adapter fino concluído. Motor é agora a fonte canônica de `cards.repasse` sem variáveis intermediárias de bridge. W3e-A havia movido o motor para rodar antes do render e deletado o inline de L.4661-4705. W3e colapsa o bridge residual.

## Mudanças

### `03_Ferramentas/Analise_Precificacao_Sacchelli.html`

| # | Linha | O que | Por quê |
|---|---|---|---|
| 1 | ~4195 | Removida `const mgMpRep = ...` | Dead variable — só existia para o inline deletado em W3e-A |
| 2 | ~4702-4737 | Colapsado bloco W3e-A: 7 vars intermediárias (`_htmlCardValRep`, `_htmlMsvlRep`, `_htmlUpRep`, `_mcCtxRepasseActive/Valor/Up/Msvl/MgMp`) → `_motorRep` direto | Motor fala direto com SimRender.mcV4, sem bridge de cópia |
| 3 | ~4749-4754 | `SimRender.mcV4()` usa `_motorRep` inline | Elimina indireção via `_mcCtxRepasse*` |
| 4 | ~5268-5270 | Removidos `cardValRep`/`msvlRep`/`upRep` de `SIM_LAST_CALC` | Motor-vs-motor = sempre 0 divergência, não agrega sinal |
| 5 | ~5399-5400 | Removidas 2 entradas `cards.repasse.*` de `_simMotorDiff` | Mesmo motivo — shadow 47 campos (era 49) |

### `03_Ferramentas/js/motor_precificacao.js`

| # | Linha | O que |
|---|---|---|
| 6 | ~1529-1532 | Atualizado cabeçalho do bloco W3b-2 → W3b-2/W3e; removido comentário stale "Replica simCalc L.4710-4751." |

## Estado do adapter pós-W3e

```javascript
// simCalc — novo adapter (W3e)
let _repUpRef=null;         // unit_prices do repasse (ref preço sugerido)
let _repaseBloqueado=false;
let _motorRep=null;          // motor.cards.repasse — fonte única
if(mpRepasseOn){
  _motorRep = (SIM_LAST_CALC_MOTOR?.cards?.repasse) || null;
  if(_motorRep && _motorRep.ativo)      { _repUpRef = _motorRep.unit_prices || {...}; }
  else if(_motorRep && !_motorRep.ativo){ _repaseBloqueado = true; }
  else                                  { _repaseBloqueado = true; console.error(...); }
}
// SimRender.mcV4 recebe direto:
repasseActive: !!(_motorRep && _motorRep.ativo),
repasseValor:  (_motorRep?.preco_total_rs) || 0,
repasseUp:     _repUpRef || {pc:0,kg:0,m:0},
repasseMsvl:   (_motorRep?.mc_svl_pct)    || 0,
repasseMgMp:   (_motorRep?.mg_mp_rep_pct) || 0,
```

## Validações

- **SYNTAX OK** — `vm.Script` nos 689.379 chars do JS embutido no HTML
- **555/555 motor tests PASS** — sem mudança aritmética
- **202/202 render tests PASS** — sem mudança em módulos de render
- Shadow bloqueante (W2.5) mantido ativo — 47 campos monitorados (removidas 2 entradas motor-vs-motor que sempre davam 0)
- **Validação em produção: OK** — card Repasse normal, shadow 0 divergências (22/04/2026)

## Estatísticas

- Linhas removidas do HTML: ~12 (vars + entradas shadow)
- Vars eliminadas: 7 (`_htmlCardValRep`, `_htmlMsvlRep`, `_htmlUpRep`, `_mcCtxRepasseActive`, `_mcCtxRepasseValor`, `_mcCtxRepasseUp`, `_mcCtxRepasseMsvl`, `_mcCtxRepasseMgMp`) + `mgMpRep` = 8 total
- Shadow: 49 → 47 campos (remoção das 2 entradas motor-vs-motor)
- Aritmética: zero mudança

## Próximos passos

1. **Validação em produção** — abrir simulador, acionar MP Repasse com NF preenchida, confirmar card Repasse renderiza normal + shadow 0 divergências. Se toast aparecer: investigar imediatamente.
2. **Fase pós-motor de config** — migração hardcodes AFS → `parametros_afs.json` (CF escalonado, certificações, fases industriais). Pré-requisito pra MetalM compartilhar o motor.
3. **Smoke test `render_corte.js`** — débito leve desde o piloto W3d.
4. **Proposta de Exportação USD/EN** — parked, meio dia de trabalho quando sinal verde.
