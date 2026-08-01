---
data: 2026-04-24
tipo: log
status: vigente
obs: "fechado"
projeto: Simulador Precificação
fase: Camada 11 — Auto-VPP + Lâmina em MP Repasse a granel + venda Pç
---

# Camada 11 — Proteção contra margem furada em MP Repasse a granel

Hotfix estrutural pra cenário comum (compra MP a granel, vende por peça) onde vendedor esquecia de preencher VPP/lâmina e perdia 5-8% de margem em silêncio. Auto-popula VPP via fórmula raio² da tabela AFS de tolerâncias dimensionais; lâmina default 2mm do config; tolerância de corte (mm/peça) permanece manual (UX do operador).

## Origem da conversa

Sintoma: Gustavo testando MP Repasse comprado em Kg + venda Pç percebeu que VPP/tolerância não eram populados — vendedor precisaria preencher manualmente, e tipicamente esquece. Resultado: spread fictício de margem oculta no DRE Camada 2 + custo subestimado.

Discussão técnica chegou em 3 conceitos distintos que estavam embaralhados:

| Campo | Semântica | Origem do valor |
|---|---|---|
| **Lâmina (mm/corte)** | Kerf — material que vira pó/cavaco a cada corte | Kerf do equipamento (não depende do material) — default 2mm |
| **Tolerância corte (mm/peça)** | Quanto a mais que a medida pedida o operador pode cortar (ex: pediu 1000mm, sai 1000-1003mm) | UX comercial / qualidade operador — manual (~+3mm típico) |
| **VPP (Venda por Peça %)** | Cobertura de **bitola maior** vinda da usina (tolerância dimensional do bruto) — afeta massa por raio² | Tabela AFS por acabamento+bitola convertida em % via fórmula geométrica |

A primeira tentativa de implementação (manhã) confundiu os 3 — auto-popular `sim-tol` com valor da tabela dim, o que misturou tolerância de comprimento com tolerância dimensional. Gustavo identificou imediatamente. Fix correto: popular VPP em vez de tol.

## Decisões fixadas

1. **Auto-popular SOMENTE VPP e Lâmina.** Tolerância corte (mm/peça) volta a ser manual.
2. **Fórmula VPP:** `((bitola + tol_tabela)² / bitola² − 1) × 100` — massa proporcional ao quadrado do raio em peças redondas.
3. **Cenário de ativação:** MP Repasse ON + repUnit ∈ {kg, ton} + venda Pç + perfil ∈ {redondo, tubo} + bitola > 0. Outros perfis (chato, sextavado, quadrado) ficam manuais — fórmula raio² inválida.
4. **Mostrar campo VPP** em MP Repasse a granel + Pç. Antes era escondido em qualquer Repasse com a justificativa "preço de compra é real, não precisa VPP" — só vale para Repasse Pç (já cortado).
5. **Detecção de edição manual:** `oninput` em sim-vpp e sim-lamina marca `dataset.auto='false'`. Setar `.value` via JS NÃO dispara `oninput` event, então auto não retroage por engano.
6. **Badge visual:** `🔁 Auto: 7,12% (Ø+6,3mm)` no label do VPP, `🔁 Auto: 2,0mm` no label da Lâmina. Edição manual remove o badge.
7. **Lâmina e tolerância NÃO entram no denominador do rateio** (decisão Hotfix CP rateio do mesmo dia, mantida).

## Entregas

### Config — bloco `cortes`

`parametros_afs.json/.js` v1.5-fase4f → **v1.6-camada11**:

```js
cortes: {
  lamina_default_mm: 2.0,
  auto_tolerancia_mp_repasse_pc: true  // flag liga/desliga
}
```

Tabela `tolerancias` da Fase 4d permanece a fonte do valor dimensional (mm radial) por bitola+acabamento.

### HTML — `simAutoTolerancia()` + helpers

Função pura adicionada antes de `simCalc()`. Lógica:

1. Lê flag `cortes.auto_tolerancia_mp_repasse_pc` — se false, sai.
2. Detecta cenário: MP Repasse ON + repUnit kg/ton + sellUnit pc + bitola>0 + acabamento conhecido.
3. Bitola: tenta `sim-peca-de` (peça estruturada), fallback pra `sim-bitola` (material principal).
4. Acabamento: tenta `sim-peca-acabamento`, fallback pra `sim-acab`. Mapeamento PT→tabela: forjado/laminado direto; trefilado/descascado→laminado; usinado→forjado se ø≥140 senão laminado.
5. Lookup `AFS_CONFIG.tolerancias[acab]` por bitola → tol em mm.
6. Calcula VPP via raio² (só para perfil redondo/tubo).
7. Se `sim-vpp.dataset.auto !== 'false'`, popula valor + marca auto + atualiza badge.
8. Idem `sim-lamina` com `cortes.lamina_default_mm`.

Helpers:
- `_simAtualizarBadgeAuto(id, msg)` — cria/atualiza/remove span `.sim-auto-badge` no label do input.
- `_simMarkUserEdit(id)` — chamado em oninput, marca `auto='false'` + remove badge.
- `_simAutoTolLimpar()` — chamado quando cenário deixa de aplicar (toggle off, troca pra venda Kg, etc).

Triggers wirados:
- `simToggleRepasse()` — liga/desliga MP Repasse
- `simRepUnitChange()` — muda unidade de compra
- `simUnitChange()` — muda unidade de venda
- `simPecaAcabChange()` — muda acabamento da peça
- `sim-acab` (onchange) — material principal
- `sim-bitola` (onchange) — bitola material principal
- `sim-peca-de` (onblur) — DE peça estruturada
- `simCalc()` — chama auto no início como safety-net

### HTML — visibilidade do campo VPP

`simUpdateRepasseVisibility()` antes ocultava o VPP em qualquer Repasse. Agora mostra quando `qtyUnit === 'pc'` (venda por peça) — cobertura do cenário Camada 11. `simToggleRepasse` (off) restaura visibilidade pro modo BR normal.

### HTML + Motor — VPP no cálculo

Antes: `vpp = mpRepasseOn ? 0 : input.value` (zerava VPP em qualquer Repasse).
Agora: `vpp = (mpRepasseOn && _repPeca) ? 0 : input.value` (zera só em Repasse Pç).

Mesma mudança espelhada no motor `calcVpp()`:

```js
function calcVpp(entrada) {
    const { isPc } = detectarFlagsUnidade((entrada.quantidade || {}).unidade);
    if (!isPc) return 0;
    const mp = entrada.mp_repasse || {};
    const repPeca = !!(mp.ativo && mp.unidade === 'pc');
    if (repPeca) return 0;
    return Number((entrada.vpp_corte || {}).vpp_pct) || 0;
}
```

### Testes — 2 novos

```
✓ Camada 11: MP Repasse a granel + venda Pç → VPP é APLICADO (não zerado)
✓ Camada 11: MP Repasse Pç (já cortado) → VPP é zerado mesmo se preenchido
```

569/569 motor verde.

## Bug detectado pelo shadow bloqueante (lição estrutural)

Após o fix do HTML mas ANTES do fix do motor, ao testar em produção o **shadow bloqueante (W2.5) disparou imediatamente**:

```
Motor diverge em 22/58 campos
• custoTon: Δ R$ 467,64
• totalCusto/cardCusto/mpCusto/mpCusto_pc: Δ R$ 3.285,18
```

A divergência era exatamente o efeito do VPP 7,12% que o HTML passou a aplicar mas o motor continuava zerando. Bug não chegou a sair de produção — shadow agarrou na hora.

**Crédito ao shadow bloqueante:** este é o segundo evento esta semana em que ele justificou a manutenção (primeiro foi o `require()` no browser, descoberto só porque o shadow estava silenciosamente desligado por causa do mesmo bug). Continuar deixando shadow ativo é critério, não overhead.

## Comparação de impacto (cenário ø180 forjado, 5 peças × 1000mm)

| | Sem Camada 11 | Com Camada 11 |
|---|---|---|
| Lâmina | manual (vendedor preencheu 0mm — esqueceu) | auto 2mm (badge) |
| VPP | escondido — vendedor não tem como aplicar | auto 7,12% (badge) |
| pesoMP | ~7.961 kg | ~8.091 kg (+130 kg) |
| custoTon | R$ 8.027/T | **R$ 8.494/T** |
| mpCusto | R$ 63.961 | **R$ 67.246** |
| **Diferença** | — | **+R$ 3.285** absorvido na margem |

Em peça menor com mais quantidade (ex: ø50 × 100mm × 200 peças), o efeito relativo escala — pode chegar a 2,2-3% sobre o VT total.

## Pendências

- **Validação em produção** — toast sumiu após fix do motor, números bateram. Confirmação verbal Gustavo: "aparentemente ok". Próxima cotação real do cenário valida ainda mais.
- **Outros perfis (chato, sextavado, quadrado)** — fórmula raio² inválida. Auto não popula. Vendedor preenche manual. Deixar como débito leve — se aparecer demanda real, refinar fórmula por perfil.
- **Tolerância corte (mm/peça)** — manual definido pela conversa. Se aparecer caso onde +3mm também deve ser auto-default por equipamento, abrir Camada 12.

## Arquivos tocados

| Arquivo | Mudança |
|---|---|
| `config/parametros_afs.json` | v1.5-fase4f → **v1.6-camada11**, bloco `cortes` |
| `config/parametros_afs.js` | Espelhado |
| `js/motor_precificacao.js` | `calcVpp` deixa de zerar em qualquer Repasse — só em Repasse Pç |
| `js/motor_precificacao.test.js` | +2 testes Camada 11 |
| `Analise_Precificacao_Sacchelli.html` | `simAutoTolerancia()` + helpers, triggers, swap visibilidade VPP, fix `vpp = ` em simCalc |

## Pra retomar

A feature está completa, mas se aparecer demanda específica:
- `refinar VPP perfil chato` — fórmula área/volume diferente
- `auto tolerância corte` — se valor padrão por equipamento aparecer
- `validar cenário kg-vendido-em-Pç` — testar caso real com peças pequenas (alta sensibilidade ao VPP)
