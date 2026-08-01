---
data: 2026-06-01
tags: [incidente, motor-cotacoes, win-rate, fix-fonte]
relacionado:
  - "[[2026-05-09 — Painel Cotacoes F3 (aggregator + cubos OLAP)]]"
  - "[[2026-05-14 — Agente Analítico Sacchelli (fundação)]]"
  - "[[Sistema Operacional Comercial/08 Agente Analítico/02 - Convenções e Caveats]]"
---

# Fix `valor_orc_previo` — Win Rate dobra de 22% → 40%

## TL;DR

Bug estrutural no `aggregator.py` de Cotações desde a F3 (09/05/2026) zerava silenciosamente a métrica `valor_orc_previo` em **7 cubos OLAP**. Resultado: todo cálculo de Win Rate em painel HTML, Agente Analítico e qualquer consumidor do `cotacoes_data.js` que usasse a métrica do cubo retornava **21,7% (bruto)** em vez do real **40,2% (líquido)** — quase metade.

Fix: 3 linhas. Impacto: dobra a métrica que mais aparece em reunião de carteira. Vendedores que pareciam fracos (Alam 32%, Reynaldo 28%, Carlinhos 22%) na verdade estavam em 80%, 59%, 44%. **3 semanas operando com leitura errada.**

## Causa-raiz

`MotorAnalitico/cotacoes/aggregator.py` linha 99:

```python
def _acumular(d, valor_total, qtd, kg, pu, gap_f3_pct, status, motivo, ciclo_dias=None):
    ...
    if motivo == 'Orç. prévio':          # ← string do schema antigo (motivo_grupo)
        d['n_orc_previo'] += 1
        d['valor_orc_previo'] += valor_total
```

Mas todos os 7 callsites passam `bucket` (string canônica do `bucket_status` F5):

```python
_acumular(cubo_main[chave], valor_total, qtd, kg, pu, gap_f3, status, bucket, ciclo_dias)
```

`bucket` chega como **'Orçamento'**, nunca como **'Orç. prévio'**. Condição jamais satisfeita → métrica zerada nos cubos:
- cubo_main
- cubo_aco_faixa
- cubo_cliente
- cubo_pendentes
- cubo_motivos
- cubo_pricing_item
- cubo_geo

**Não afetados** (usam variável `motivo` do escopo do loop, que é `motivo_grupo` original):
- `cliente_stats` (linha 538)
- `cubo_dia` (linha 423)
- itens críticos / projeto suspeito (linha 582)

## Origem temporal

F3 (09/05) introduziu `bucket_status` como dimensão canônica e mudou os callsites de `motivo` → `bucket`, mas esqueceu de atualizar a comparação dentro de `_acumular`. Variável local `motivo` (do escopo do loop, ainda em `motivo_grupo`) continuou existindo na linha 423/538, mascarando o bug parcialmente: alguns blocos do painel HTML mostravam Orç. Prévio corretamente (vinham de `cliente_stats`/`cubo_dia`), outros zero (vinham de `cubo_main`). Inconsistência interna no painel que confundiu auditoria.

## Como foi descoberto

Sessão Agente Analítico (14/05) documentou o sintoma em `02 - Convenções e Caveats.md`:

> Bug `valor_orc_previo`: métrica do cubo_main de cotações está SEMPRE ZERADA. Orçamento prévio fica embutido em `valor_perdeu`. Recuperar via `bucket_status='Orçamento'`. Impacto: win rate global YTD 2026 sobe de 24% (bruto, CLAUDE.md, painéis) → 40,2% (líquido, real disputa).

Mas o caveat ficou parqueado como "auditoria pendente" durante 17 dias. Hoje (01/06) entrou na pauta como precondição pro Painel Executivo Consolidado.

## Fix aplicado

`MotorAnalitico/cotacoes/aggregator.py`:

1. Renomeado param `motivo` → `bucket` na assinatura de `_acumular` (linha 99) — limpeza semântica para refletir o que realmente chega.
2. Comparação ajustada (linha 123): `bucket == 'Orçamento'` em vez de `motivo == 'Orç. prévio'`.
3. Schema bumpado: `v2.3-2026-05-09` → **`v2.4-2026-06-01`**.

`03_Ferramentas/Painel_Cotacoes.html`:

4. `SCHEMA_ESPERADO` bumpado para a nova versão.

`MotorAnalitico/agente/analises/cotacoes.py`:

5. Atualizada a nota "está sempre zerado" (já não é mais verdade). Mantido o cálculo via `bucket_status` como defesa em profundidade.

## Validação numérica (cotacoes_data.js v2.4)

Antes do fix (cubo_main agregado YTD 2026):
- valor_ganhou: R$ 90,4 MM
- valor_perdeu: R$ 326,0 MM (incluía orçamento embutido)
- valor_orc_previo: R$ 0 (bug)
- Win Rate bruto: 21,7%
- Win Rate "ajustado" pelo Agente Analítico via workaround: 40,2%

Depois do fix:
- valor_ganhou: R$ 90,4 MM
- valor_perdeu: R$ 326,0 MM (continua bruto por construção — status Softcomp)
- **valor_orc_previo: R$ 191,3 MM (21.279 cotações)** ✓
- Win Rate bruto: 21,7% (igual — denominador "encerradas" não muda)
- **Win Rate ajustado direto do cubo: 40,2%** ✓ (sem precisar do workaround)

Diferença operacional: agora qualquer consumidor (painel, Agente, executivo futuro) lê **a métrica certa direto do cubo**. Sem reconstrução manual via bucket_status.

## Impacto por vendedor (top 10 por R$ ganhou YTD 2026)

| Vendedor | WR bruto | WR ajustado | Δ | R$ orç prévio camuflado |
|---|---:|---:|---:|---:|
| Alam | 32,3% | **80,2%** | +47,8 pp | R$ 7,4 MM |
| Reynaldo | 27,6% | 58,9% | +31,2 pp | R$ 14,5 MM |
| Carlinhos | 21,5% | 44,0% | +22,5 pp | R$ 14,9 MM |
| Jaqueline | 41,6% | 57,0% | +15,4 pp | R$ 2,4 MM |
| Elaine | 31,1% | 45,4% | +14,3 pp | R$ 4,1 MM |
| Rep - Marcelo | 30,5% | 41,6% | +11,0 pp | R$ 3,9 MM |
| Barbosa | 32,8% | 43,5% | +10,8 pp | R$ 4,7 MM |
| Estratégicos | 10,2% | 19,4% | +9,2 pp | R$ 23,8 MM |
| Fabiana - SCA | 38,0% | 42,8% | +4,8 pp | R$ 1,1 MM |
| Açotec - SCA | 35,9% | 39,2% | +3,3 pp | R$ 1,6 MM |

Reynaldo e Carlinhos são os mais subestimados em volume absoluto (R$ 14-15 MM em orçamento prévio cada). Alam aparece como caso extremo de carteira tabelista (orçamento > ganhou em valor — perfil B2B repetitivo).

## Não afetado

- **Painel RAF**: não usa essa métrica. Faturamento real (linha NF) tem outra lógica de tabela.
- **Painel Pedidos**: cross-check é item-a-item via `pedido_id`, não consome agregados de cotações. Pedidos `cubo_main` não tem `orc_previo`.
- **Painéis HTML em blocos que reconstroem por `bucket_status`**: já mostravam corretamente. Eram os blocos que pareciam não bater com KPIs do topo (que vinham do cubo zerado).

## Próximos passos

1. ✅ Fonte limpa para construir o **Painel Executivo Consolidado** (Fase 1 do plano de 01/06).
2. Auditoria visual no Painel de Cotações HTML em sessão presencial — confirmar que tudo bate agora (a inconsistência entre blocos some).
3. **Atualizar CLAUDE.md**: remover linha de caveat sobre bug zerado, marcar `valor_orc_previo` como confiável a partir da v2.4.
4. **Atualizar `02 - Convenções e Caveats.md`**: marcar bug como resolvido com a versão do schema.

## Lições

- **Schema versionado salvou tempo de debugging**: bastou bumpar v2.3 → v2.4 e o painel HTML alertou via banner. Sem isso, leitura silenciosa do JS desatualizado teria deixado a confusão.
- **Refatorações de dimensão (motivo_grupo → bucket_status) precisam de busca cruzada por TODOS os usos do nome antigo**. F3 mudou os callsites mas deixou a comparação dentro da função privada. `grep -n "Orç\. prévio"` teria pegado.
- **Caveat parqueado é dívida que sangra**. 17 dias com Win Rate errado significa decisões de carteira erradas em todas as reuniões de pricing semanais nesse período. Resolver caveats com impacto financeiro alto deve furar fila.
- **Workaround na camada de consumo (Agente Analítico) mascarou o problema**: a função canônica retornava o número certo via reconstrução, então quem usava o Agente nunca via o bug. Quem abria o painel HTML, sim. Esse tipo de divergência é tóxica — vira "o Agente diz X, o painel diz Y, em qual eu confio?"

## Princípio reforçado

> Quando uma métrica importante diverge entre dois consumidores do mesmo dado, o bug está na fonte — não na camada de consumo. Fix na fonte primeiro, sempre.
