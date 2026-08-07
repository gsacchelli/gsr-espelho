# Flori Vigia — alertas proativos do lake

**Data:** 02/08/2026
**Contexto:** Na avaliação "precisamos de um agente novo tipo Hermes?", a resposta foi não — a lacuna real do time era o Flori ser só reativo. Gustavo aprovou o investimento: o Flori agora avisa sozinho quando algo cruza limiar no lake.

## Desenho (mesmo princípio do briefing das 8h)

**Detecção 100% determinística** — SQL sobre o gold read-only + limiares em `MotorAnalitico/config/vigia.yaml` (editável sem rebuild). Zero LLM no caminho: número de alerta não pode nascer de modelo. O Flori empresta a voz e o canal (Telegram, allowlist).

## Os 3 vigias v1

| Vigia | Regra | Limiar default |
|---|---|---|
| 🚫 Pedido cancelado | flag `cancelado` (StatusPedido da BI.Pedido, entrega Nelson 01/08) | ≥ R$ 30k |
| ⏳ Cotação parada | valor da cotação (soma dos itens) cruzando marcos de aging | ≥ R$ 100k · marcos 7/14/30d |
| 👻 Cliente sumindo | top 20 por pedidos 12m; gap > 2× cadência mediana do PRÓPRIO cliente | e gap ≥ 21d |

**Anti-ruído:** estado em `lake/meta/vigia_estado.json` — cada chave dispara 1×; marco novo = chave nova; cliente que voltou a comprar = episódio novo re-alertável. **1ª execução é baseline**: as 33 situações já abertas em 02/08 NÃO inundaram o Telegram — só valem cruzamentos novos daqui pra frente.

## Operação

- LaunchAgent `com.sacchelli.flori-vigia`: de hora em hora, :20 (8h20-17h20 + 18h00), todos os dias — o código silencia fim de semana e fora de 8-18h. Log `lake/meta/flori_vigia.log`.
- Manual: `.venv/bin/python -m MotorAnalitico.telegram_bot.vigia [--dry-run] [--agora]`.
- Testes (9) em `telegram_bot/test_vigia.py`, no `make ci`.

## O que a baseline de 02/08 já mostrou (dry-run)

Sinal real, não ruído: **TUP R$ 2,16 MM parada há 31d**, **PROK R$ 1,55 MM há 31d** (PROK aparece em 12 das 32 cotações paradas ≥ R$ 100k — padrão a investigar), **TER BRASIL sumido há 26d** (cadência ~8d, R$ 3,3 MM/12m). Nenhum cancelado ≥ R$ 30k no momento.

## Parte 2 (mesmo dia) — Vigia × Segmentação: o caso PROK vira regra

**Contexto:** Gustavo pediu "arquétipos de cliente" pra qualificar os alertas (PROK cota pra orçamento, não pra compra). Reconhecimento com 3 agentes paralelos (código/semântica/dados) revelou: **o sistema de arquétipos JÁ EXISTIA** — segmentação v1, congelada 23/07 (`vw_segmentacao_clientes`: Perfil Projeto/Revenda/Negociador/Orçamentista/Programado/Fiel/Esporádico + Tier + Trajetória + Regime). Ela já classificava PROK = Projeto/regime Orçamentação (91,7% orç., conv 18,3%) e TER BRASIL = Negociador A Crescendo. **Quem não a consultava era o Vigia.** Nada de sistema paralelo: conectamos.

**Mudança:** `detectar_paradas` agora recebe segmento/regime da segmentação (join por `cod_cliente`, nunca por nome — 157 nomes colidem) e cliente com **regime 'Orçamentação' ou segmento 'Orçamentista' só alerta no marco 30d**, rotulado "perfil orçamentista" (`vigia.yaml::marco_minimo_orcamentista`). Fallback sem a view = comportamento antigo. Segmentação segue CONGELADA — o Vigia consome, não re-calibra.

**Efeito medido:** 33 → 20 situações ativas; PROK 12 → 4 alertas (todos ≥30d, rotulados); TER BRASIL intocada. 12 testes.

**Calibração com o Gustavo:** entregue `02_Derivados/Segmentacao/Calibracao_Arquetipos_2026-08-02.xlsx` — 951 clientes (Tier A/B ou ≥R$ 1MM cotado) com os eixos da segmentação + WR em R$ na disputa real 2024+, cadência de pedidos e %Preta RAF 2025+. Resumo por perfil: Programado 270 cli/R$ 23,7MM de MC 12m · Negociador 98/14,9 · Orçamentista 203/8,9 · Esporádico 234/5,3 · Fiel 65/2,2 · Projeto 27/1,9 · Revenda 54/1,1.

**Correção de passagem:** nota-espelho SAC360 tinha a linha do WR Ajustado defasada (excluía só Orç. prévio; o código exclui também Enc. administrativo desde 17/07) — corrigida.

**v2 candidata anotada (insight do Gustavo, não escopada):** *trajetória de intenção* — PROK migrou de compradora (2023: 13,6% orç., WR 52,9%) pra orçamentista (2026: 65,6%, WR 6,7%); a segmentação fotografa 18m, não captura a migração. Se virar eixo, é evolução da régua v2 COM o Gustavo, não retune unilateral (v1 congelada).

## Parte 3 (mesmo dia) — PROK: leitura de mercado do Gustavo + checagem Trefita

**Contexto do Gustavo (02/08):** PROK compra direto de usina (Villares Metals, Arcelor) e forjaria (Açoforja); distribuição é pulmão — "como usinas/forjarias têm atendido no prazo, pouco sobra para distribuição". Trefita teria política agressiva (possivelmente sem custear direito — tipicamente eixos desbastados).

**Checagem nos dados Trefita/Torres (janela mai-jun/26, R$ 48,1 MM em pedidos, 1.683 clientes compradores):** **PROK BRASIL comprou R$ 0 da Trefita** — zero por nome, zero por CNPJ (26950902/0001-82) e por raiz. ⚠ Janela de só 2 meses; cadastro bruto deles não está mais no disco (só a análise consolidada em `~/Documents/Concorrencia/`); reavaliar quando vier export novo.

**Nosso lado (entrada de pedidos PROK):** 2023 R$ 3,56 MM (163 t) → 2024 R$ 2,65 MM → 2025 R$ 1,69 MM → **2026 R$ 176 mil (8,9 t)**. Na mesma janela mai-jun/26: R$ 82 mil.

**Leitura consolidada:** o colapso do WR da PROK (53%→6,7%) NÃO é a Trefita nos comendo — na janela observada ela também levou zero. É a usina atendendo no prazo e secando o pulmão da distribuição INTEIRA; as 812 cotações da PROK conosco são cotação-de-referência pra compra que vai pra usina. Implicação comercial: a proposta de valor da distribuição pra PROK é DISPONIBILIDADE quando a usina falha (urgência, lote pequeno, corte) — prêmio de urgência, não disputa de preço; esforço de venda mínimo no resto (o Vigia já a silenciou pra marcos curtos). Pauta pro Felipe atualizada com esse ângulo.

## v2 possível (não escopado)

Bloqueio de pricing novo em cotação grande; queda de MC de referência (agora que `CustoMP` chegou); resumo semanal "o que o Vigia pegou"; alerta de RAF defasado; trajetória de intenção (acima).


## Adendo 07/08/2026 — recalibração pelo Gustavo (6 regras) e uma regra desligada

Limiares novos, todos MEDIDOS no gold antes de abrir: cancelado qualquer
valor · parada ≥50k · sumido top-20/21d/2× (já era) · **EMITIDA >100k**
(resumida: 5 detalhadas + rodapé com chave POR DIA) · **oportunidade**
(item >15k, cliente A/B, `status_sugerido=PRIORIZAR`). Nasceu o
`--rebaseline` (mexeu no yaml → rodar, senão o passivo que o limiar antigo
escondia vira enxurrada). 🪤 `materiais_monitorados` DESLIGADA: o "nós zero"
do 17CrNiMo6 era o bug de família já corrigido — vendemos R$ 4,9 MM em 2026.
**Alvo de vigia derivado de análise precisa ser re-verificado quando a
análise é corrigida.** Detalhes: CLAUDE.md + `config/vigia.yaml` (cada limiar
com o porquê e o volume medido ao lado).
