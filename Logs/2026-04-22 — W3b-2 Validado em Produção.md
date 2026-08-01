# 2026-04-22 — W3b-2 Validado em Produção

Fechamento formal do W3b-2 (Card Repasse no motor). Instrumentado em 22/04 na sessão consolidada, validado em produção hoje em cenário real.

## Resultado

Cotação real com MP Repasse ativo + NF. F5 pra restaurar shadow ON. Clicar Calcular.

**Saída de `window._simMotorDiff()`:**
- `total`: 60 campos monitorados
- `divergencias`: 0
- `linhas`: 60 entradas, todas bit-idênticas

Motor bateu HTML em todos os 50 campos originais da Camada 2 + 2 do Card Repasse (`cards.repasse.preco_total_rs`, `cards.repasse.mc_svl_pct`) + 8 campos auxiliares.

## Status pós-validação

- W3b-1 (Repasse nacional) ✅ validado 22/04
- W3c (Importação) ✅ validado 22/04
- W3b-2 (Card Repasse) ✅ validado 22/04 (este fechamento)
- W3d piloto (render_corte.js) ✅ instrumentado + smoke test Node, sem shadow necessário (render puro, sem aritmética comparável)

## Observação arquitetural

Shadow pegou 0 divergências num cenário real com MP Repasse na primeira tentativa. Isso confirma que:
1. A função `_recalcTotalVRepasse` no motor replica fielmente o `recalcTotalV` inline do HTML (mesma matemática, só swap da margem da linha MP).
2. O adapter `dom_to_entrada.js` está coletando os inputs de Repasse corretamente (já tinha sido validado em W3b-1).
3. O cálculo do `mg_mp_rep_pct` relativo (motor) bate com o valor absoluto exibido no HTML.

O inline do Card Repasse no HTML continua rodando (duplicação proposital — shadow roda depois). Eliminação acontece no W3e (simCalc adapter fino), quando motor roda ANTES do render e os renders passam a consumir direto o retorno do motor.

## Próximo passo

W3d-2: extrair DRE do Pedido (~90 linhas) do simCalc pro módulo `render_dre.js`. Padrão validado no piloto W3d (render_corte.js).

## Variações não cobertas em produção (aceitas via testes sintéticos)

- Unidade de venda Kg / Pç / m separadamente (7 testes sintéticos cobrem)
- Toggle Repasse ON → OFF → ON (idempotência)
- MC MP sugerida ≠ 25%

Se aparecer divergência em qualquer variação futura, shadow bloqueante pega automaticamente (é pra isso que ele existe).
