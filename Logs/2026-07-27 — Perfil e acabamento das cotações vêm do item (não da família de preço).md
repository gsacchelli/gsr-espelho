---
data: 2026-07-27
tipo: log
status: vigente
---
# Perfil e acabamento das cotações vêm do item (não da família de preço)

**Data:** 27/07/2026
**Contexto:** continuação do commit `14e5675` (pedidos), que já tinha deixado esta pendência registrada. Fecha o vocabulário físico nas 4 views de fato do gold.
**Commit:** `0fc9f02` (branch `claude/nifty-euclid-746c9f`) — merge no principal ainda pendente, ver "Pendências".

## O erro

`cotacoes/enriquecer.py::derivar_familia` resolvia `perfil`/`acabamento` pelo cadastro `FamiliasProdutos.xlsx` e só caía pro código do próprio item quando a família não existia. Precedência invertida: **no cadastro, perfil é atributo da família de PREÇO, não do item** — as 133 entradas são TODAS 'Redondo'.

Não era erro de código, era erro de premissa sobre o que aquele campo significa.

## Medido (encerradas 2023-2026, 671k linhas)

**Perfil — 8.901 linhas com código diferente de 'R' saíam 'Redondo':**

| perfil | antes | depois |
|---|---|---|
| Anel | não existia como recorte | 5.317 linhas · R$ 320 MM · WR 49,4% |
| Tubo | 41 linhas · R$ 0,6 MM | 3.487 · R$ 237 MM · WR 65,7% |
| Chato | 61 (rotulado 'Chapa') | 247 · R$ 8,3 MM · WR 23,3% |
| Redondo | 681.124 · R$ 5.697 MM | 672.223 · R$ 5.143 MM · WR 63,0% |

**Acabamento estava pior — 18.630 linhas erradas.** Passou despercebido porque o cadastro VARIA nesse campo (83 Laminado / 44 Forjado / 4 Descascado / 2 Trefilado), então parecia dado do item. O caso grave: **'Usinado' tinha 185 linhas / R$ 11 MM onde o item diz 12.546 / R$ 885 MM** — o resto contado como Forjado ou Laminado.

O WR do Redondo mal se move (62,9% → 63,0%): a diluição é pequena em 672k linhas. O ganho não é corrigir o Redondo, é os recortes não-Redondo **deixarem de ser ficção**. Anel a 49,4% contra 63,0% do Redondo é diferença de negócio que estava invisível.

## Por que o código do item é confiável

Conferido contra a descrição do próprio material (`'1045 Redondo Laminado 110.00'` — o campo é auto-explicativo): bate em **~100% das linhas, em todo código de perfil e de acabamento**. Não é convenção suposta.

De passagem, isso provou que o mapa que vivia em `cotacoes/enriquecer.py` tinha **3 rótulos errados desde sempre**: `A` era 'Achatado' (é **Anel** — 5.301 de 5.317 linhas dizem "anel", zero dizem "achatado"), `C` era 'Chapa' (é **Chato**), `L` era 'Lâmina' (é **Cantoneira**); `D` e `P` faltavam. Inverter a precedência usando aquele mapa teria trocado um erro por outro.

Mapa canônico único: `definicoes.py::PERFIL_LABEL`/`ACABAMENTO_LABEL`, compartilhado com pedidos e faturamento.

## Decisões

1. **Item manda, cadastro é fallback.** Mesma regra do RAF, que passa `ABCPER_DES`/`ABCACA_DES` direto pro lookup.
2. **Linhas sem código continuam herdando 'Redondo' do cadastro** — 3.581 linhas / **R$ 572 MM**. Decisão consciente do Gustavo (27/07): manter. Fica registrado como **a maior imprecisão restante** do campo: é palpite, não dado. A alternativa (deixar vazio, tornando a lacuna visível) está desenhada e custa uma linha + reenriquecimento.
3. **Código desconhecido volta cru, sem inventar rótulo.** Sobraram 2 anomalias de origem em 671k: perfil `'U'` de uma viga U de verdade (ROMI, R$ 15,5 mil) e acabamento `'8'` vazado da classe de tolerância h8 (R$ 23,90). `'U'` não virou 'Viga U' no vocabulário compartilhado porque 1 linha não sustenta rótulo novo — se aparecer volume, revisar.

## Propagação (feita)

`make atualizar-cotacoes` completo: reenriquecer 671k → cross-check pedidos → bronze → silver → gold → cockpits. Portal já reflete (reconecta pelo mtime do `.duckdb`).

Verificação: 58/58 testes de contrato do gold · 75/75 cotações · `vw_pedidos` íntegra (145 nulos em 2026, família nula 3,3% — igual ao esperado pós-`14e5675`) · zero avisos de sanidade do pipeline. A tolerância `{"P","D"}` do teste de contrato foi zerada (viraram 'Chapa' e 'Disco de Aço') e substituída pelas 2 anomalias nomeadas.

## Fase 2 — o degrau que faltava, e o remendo a jusante (`f071d44`)

Investigando o que mais lia perfil, apareceram duas consequências da idade do bug.

**1. Faltava um degrau na hierarquia.** `0fc9f02` deixou `código do item → cadastro`, e o cadastro é palpite. Item engenheirado não traz campo físico nenhum (`DISCO SAE 4140 - Ø 812,8 X 130mm`), então caía direto no palpite — **46 discos forjados marcados 'Redondo'**. A descrição do item ainda é DADO. Hierarquia final: **código do item → marca no texto → cadastro**. Recupera 120 linhas / R$ 18,4 MM (46 Disco de Aço, 35 Anel, 24 Tubo, 7 Chapa, 5 Quadrado, 3 Sextavado).

Isso revisitou a decisão de "deixar como está" das linhas em branco: a escolha oferecida era binária (cadastro *ou* vazio) e existia uma terceira melhor que as duas. Os R$ 556 MM que sobram sem marca no texto seguem no fallback, como decidido.

**2. O Cockpit tinha um remendo com a mesma premissa errada.** `perfil_efetivo()` lia o TEXTO antes do campo — criado em 18/07 porque *"o export de PENDENTES marca perfil R em praticamente tudo"*. Alguém já tinha visto o sintoma e compensado no consumidor, sem chegar na causa. Dois achados ao desmontar:

- `("ACHAT", "Chato")` era **código morto**: nenhuma linha em 671k tem 'ACHAT' no texto. Herdou a premissa de que A era 'Achatado' — A é Anel.
- a supressão de matéria-prima de partida comparava com `'Disco'`. Trocar a fonte sem ajustar **desligaria a supressão em silêncio**, porque o canônico é `'Disco de Aço'`. Hoje tem teste travando o vocabulário.

Agora o campo manda; o texto só decide se dá pra confiar no engenheirado (sem marca, exibe `(engenheirado)` em vez de afirmar perfil não verificado — 43 itens no cockpit atual).

## Fase 3 — retreino do score (27/07, 21:09)

O modelo de 22/07 tinha sido treinado com o vocabulário errado: `cat_levels['perfil']` era `['Achatado', 'Chapa', 'Lâmina', ...]`. Consequência medida: 53 pendentes (R$ 1,80 MM) de Anel e Chato caíam em **NaN** — o XGBoost tratava como missing e o item perdia o sinal de perfil, silenciosamente. Pior no conceito: o modelo aprendeu 'Achatado'/'Chapa'/'Lâmina' que eram Anel/Chato/Cantoneira, e 'Usinado' com 185 linhas quando a verdade eram 12.546.

Retreino (7,5 s): AUC **0,859** e erro por banda **1,5pp**, contra a régua do log-odds atual (0,723 / 4,7pp) — venceu nos 2 critérios e assumiu. Níveis agora canônicos.

⚠️ **Duas ressalvas honestas:**
- Esse 0,859 × 0,723 é XGBoost × heurística log-odds, que é a regra de promoção do script. **Não** é prova de que o retreino de hoje superou o modelo de 22/07 — não dá pra saber, porque o `treinar_score_ml.py` promete `relatorio.md` no docstring e **nunca escreve o arquivo**, então não há métrica histórica guardada. Vale corrigir.
- No SHAP, perfil e acabamento **não aparecem no top 10** (domina `prior_cliente`, 1,011). O ganho do fix no score é modesto; o ganho grande é na leitura por recorte, não na priorização.

O cockpit precisou ser regerado DEPOIS do retreino — a cadeia o gerou às 21:09 com o modelo velho.

## Pendências

- ✅ Merge em `corrige-automacoes-e-segredos` — feito (`1008153`, por sessão paralela). Tudo commitado; working tree limpo.
- `treinar_score_ml.py` não escreve o `relatorio.md` que documenta — sem isso, cada retreino apaga a memória de métrica do anterior.
- Reavaliar as 3.435 linhas sem código nem marca no texto (R$ 556 MM) se o recorte por perfil virar decisão de peso.
- **Anel como negócio**: R$ 326 MM de cotação histórica convertendo a 49,4% contra 63,0% do Redondo. Recorte que nunca foi analisado porque não existia. É o único desdobramento comercial, não técnico.

## Aprendizado transferível

Duas fontes descreviam a mesma dimensão e uma delas era de outro nível de granularidade (família de preço × item). O sintoma — "pendentes 100% preenchidas com Redondo" — parecia dado completo, não dado errado. **Campo preenchido não é campo correto**; a checagem barata foi cruzar o campo com a descrição textual do próprio registro, que aqui era auto-explicativa.

Relacionado: [[2026-07-14 — Regras de negócio oficializadas (DRE, comissão agente) + Estágio 5]]
