# 2026-05-05 — Fase 2C TIPI Lookup Proposta

## Contexto

Sessão disparada pela proposta **900001 Rev.0 — Produsi** (PR, 5/5/2026, 6 itens carbono+ligado redondo laminado). Ao revisar o PDF, identifiquei o campo "IPI 3,25" em todos os itens, inflando o valor "IPI incluso" em **R$ 679,72** sobre o subtotal de R$ 20.914,60.

**Achado**: hardcode `ipi_pct: 3.25` + `ncm: '7228.5000'` em `Analise_Precificacao_Sacchelli.html` linhas 12370-12372. Era débito conhecido — fallback greedy do dia 20/04/2026, parqueado como **Fase 2C** ("NCM + IPI lookup data-driven; exige decisão de produto sobre mapeamento família×NCM + levantamento TIPI").

A proposta Produsi foi o primeiro caso real em que o débito virou erro de campo:
- **NCM 7228.5000** (outras ligas, acabadas a frio) está duplamente errado pra 1045 redondo laminado: deveria ser 7214.99.10 (carbono não-ligado, laminado a quente, seção circular).
- **IPI 3,25%** parece memória institucional pré-Decreto 11.158/2022. TIPI vigente (Decreto 11.158/2022 + ADE COANA 001/2026) coloca **0%** em todas as posições do Capítulo 72 que cobrem o mix AFS.

## Risco fiscal pré-fix

- Toda proposta gerada via simulador desde 20/04/2026 saiu com IPI 3,25%.
- Cliente que tomar crédito de IPI pode ter glose; AFS pode autuar por IPI declarado e não recolhido (se a NF for emitida com 3,25% e o ICMS de fato calculado com 0%).
- Reputacional com clientes recorrentes (Produsi é PR — DIFAL e crédito de IPI são sensíveis).

## Decisão

Fase 2C completa, em vez do quick fix (zerar) ou médio (lookup só por família). Razão: trabalho técnico (schema, lookup, testes) é independente do conteúdo da tabela — fechar a arquitetura agora paga em todo aço novo que entrar no mix.

## Implementação

### Artefatos novos

| Arquivo | Linhas | Função |
|---|---|---|
| `03_Ferramentas/config/tipi_data.js` | 153 | Tabela canônica: 78 regras (categoria × perfil × acabamento) → NCM + IPI. 17 NCMs distintos cobrindo carbono, beneficiamento, cementação, mola Si-Mn, inox, aço rápido, ferramenta liga, tubos. Versão 1.0-2026-05-05. |
| `03_Ferramentas/js/tipi_lookup.js` | 126 | Lookup com `categorizarAco(aco)` + `lookup(aco, perfil, acabamento)`. Categoriza string livre (1045, SAE 4140, Inox 304, M2, D2, etc) em 7 classes. Fallback explícito quando categoria não casa. |
| `03_Ferramentas/js/tipi_lookup.test.js` | ~210 | 39 testes unitários cobrindo: categorização (carbono/benef/cement/mola/inox/rápido/ferramenta/outro), casos da proposta Produsi, variações de perfil×acabamento, fallback. |

### Modificações

`03_Ferramentas/Analise_Precificacao_Sacchelli.html`:
1. Adicionados `<script src="config/tipi_data.js">` e `<script src="js/tipi_lookup.js">` antes do motor (linha 230).
2. `propostaColetarLinhas` (linha 12361+) — substituído hardcode por chamada `TipiLookup.lookup(aço, perfil, acabamento)`. Suporta override manual via `state['sim-ncm-override']` e `state['sim-ipi-override']` (preservados pra casos especiais que contador AFS apontar).
3. Novos campos `_tipi_categoria`, `_tipi_fallback`, `_tipi_motivo` no LinhaItem (uso interno; não renderizados no PDF) — permitem futura tela de UI alertando quando proposta cai no fallback.
4. Comentário do bloco atualizado pra apontar pra este log.

## Mapeamento NCM (resumo)

```
Carbono (1010-1095, 1213, 12L14, A36):
  Redondo Laminado    → 7214.99.10
  Outros Laminado     → 7214.99.90
  Forjado             → 7214.10.90 (>0,6%C)
  Trefilado/Frio      → 7215.50.00

Beneficiamento (4140, 4340, 4150, 4145, 4137, 4130, 8640, 8645, 5140, 6150):
  Laminado            → 7228.30.00
  Forjado             → 7228.40.00
  Acabado a frio      → 7228.50.00

Cementação (8620, 8617, 8615, 4320, 4820, 9310, 17CrNiMo6, 18CrNiMo7-6, 25MoCr4):
  Mesma hierarquia que beneficiamento (mesmos NCMs)

Mola Si-Mn (9260, 9258, 51B60, "5160 mola"):
  Laminado            → 7228.20.00
  Frio                → 7228.50.00

Inox (304, 316, 420, 440, 410, 17-4PH, 2205):
  Redondo Laminado    → 7222.19.10
  Quadrado/Chato Lam. → 7222.11.00
  Forjado             → 7222.30.00
  Frio                → 7222.20.00

Aço rápido (M2, M35, M42, T1, HSS):
  Tudo                → 7228.10.00

Ferramenta liga (D2, D6, H13, O1, S1, P20):
  Laminado            → 7228.30.00
  Frio                → 7228.50.00

Tubo:
  Carbono             → 7304.31.10
  Liga                → 7304.51.10
  Inox                → 7304.41.00
```

**Todas as regras retornam IPI = 0%** baseado na TIPI vigente (Decreto 11.158/2022 + revisões 2026). Fallback também é 0% — defensável fiscalmente: errar em zerar é melhor que errar inflando.

## Caveats abertos

1. **TIPI 0% para Cap. 72 — VALIDAR COM CONTADOR AFS antes de virar política definitiva.** Conhecimento setor + carga IBPT da ArcelorMittal (7228.30 = 34,12% federal+estadual+municipal, compatível com IPI 0% + ICMS 18% + PIS 1,65% + COFINS 7,6%) sustentam a hipótese, mas **não é fonte primária formal**. Se contador AFS confirmar exceção (ex: aço importado, regime especial PR), atualizar `tipi_data.js` regra a regra.

2. **5160 puro NÃO categoriza como mola.** Decisão consciente: 5160 é Cr-Mo de médio C, vai em "outro" no lookup atual (cai no fallback 7228.5000). Vendedor que estiver vendendo 5160 EXPLICITAMENTE pra mola deve escrever "5160 mola" no campo aço — aí categoriza correto pra 7228.20.00 (Si-Mn). Alternativa futura: adicionar override de categoria via UI.

3. **Forjado carbono em 7214.10.90 vs 7214.10.10** depende do teor de carbono. Mapping atual coloca tudo em 7214.10.90 (>0,6%C) — vendedor de aço carbono baixo (1010-1015) precisa override. Marcar pra revisão.

4. **Acabamento "Usinado" tratado como acabado a frio.** Na verdade, peça usinada pode escapar pra posição 7326 (obras de aço) se for peça pronta. Decisão pragmática: maioria dos casos AFS é semi-acabado, fica no Capítulo 72.

5. **Override manual (`sim-ncm-override` / `sim-ipi-override`)** está plumbing-completo no coletor mas SEM UI pra vendedor preencher. Próxima sessão: adicionar 2 campos opcionais no setup do simulador (Fase 2C-extra). Por ora, override só via state programático.

## Suite de testes — pós-Fase 2C

| Suite | Testes | Status |
|---|---|---|
| Motor Precificação | 570 | ✓ |
| Schema Proposta | 105 | ✓ |
| Gerador Proposta | 149 | ✓ |
| Comparativo Identity | 14 | ✓ |
| Render Comparativo (smoke) | 58 | ✓ |
| Render Corte (smoke) | 47 | ✓ |
| Render DRE (smoke) | 48 | ✓ |
| Render Estoque (smoke) | 48 | ✓ |
| Render MC (smoke) | 48 | ✓ |
| **TIPI Lookup (novo)** | **39** | **✓** |
| **TOTAL** | **1.126** | **✓** |

## Validação Produsi (caso real)

| Item | Aço | Perfil | Acab. | NCM antigo | NCM novo | IPI antigo | IPI novo |
|---|---|---|---|---|---|---|---|
| 01 | 8620 | Redondo | Laminado | 7228.5000 | **7228.30.00** | 3,25% | **0%** |
| 02 | 1045 | Redondo | Laminado | 7228.5000 | **7214.99.10** | 3,25% | **0%** |
| 03 | 8640 | Redondo | Laminado | 7228.5000 | **7228.30.00** | 3,25% | **0%** |
| 04 | 8640 | Redondo | Laminado | 7228.5000 | **7228.30.00** | 3,25% | **0%** |
| 05 | 1045 | Redondo | Laminado | 7228.5000 | **7214.99.10** | 3,25% | **0%** |
| 06 | 1045 | Redondo | Laminado | 7228.5000 | **7214.99.10** | 3,25% | **0%** |

Resultado pro PDF Produsi:
- "IPI não incluso" R$ 20.914,60 — inalterado
- "IPI incluso" cai de **R$ 21.594,32** → **R$ 20.914,60** (= idêntico ao não-incluso, já que IPI = 0)
- Bloco "Créditos gerados — IPI R$ 679,72" cai pra R$ 0,00

## Pendências derivadas

1. **Reemissão da Produsi 900001 Rev.1** com NCMs corretos e IPI 0% — Thais Rinco hoje, validade vencendo amanhã.
2. **Auditoria de propostas geradas 20/04 → 05/05** — quantas viraram NF? Risco de NF emitida com IPI 3,25% que precisa retificação.
3. **Validação fiscal formal com contador AFS** — confirmar tabela `tipi_data.js` regra a regra antes de marcar Fase 2C como produção.
4. **UI de override** (Fase 2C-extra, ~30min) — 2 campos no setup do simulador pra vendedor sobrescrever NCM/IPI quando o lookup cair no fallback.
5. **Consolidar caveats 1-4 acima** num PR fiscal pra contador analisar.

## Decisões registradas

- **Format**: JS-as-data (`tipi_data.js`) em vez de YAML/JSON. Razão: igual ao painel comercial RAF — evita CORS no `file://` quando vendedor abre HTML local. `<script src="config/tipi_data.js">` carrega `window.TIPI_DATA`.
- **Schema**: 5 campos por regra (categoria, perfil, acabamento, ncm, ipi_pct + obs). Match em ordem (primeira regra que casa ganha). Fallback global no fim do array.
- **Categorização heurística por regex** em vez de tabela aço-padrão completa replicada do RAF. Razão: regex em 50 linhas cobre 95% do mix AFS sem manutenção dupla. Quando aparecer aço raro, adicionar regra explícita ou regex específico.
- **Acabamento "Retificado" mapeia para "Trefilado"** internamente (mesmo NCM 7228.50/7215.50 — ambos são acabamento a frio).
- **Cementação e Beneficiamento mantidos como categorias separadas** mesmo tendo NCMs idênticos. Documentação explícita > generalização precoce.

---

## Update 05/05/2026 noite — Fase 2C-extra fechada

UI de override implementada. Bloco `<details>` colapsado por padrão no editor de item da proposta, logo abaixo da textarea "Descrição pra Proposta".

### Componentes
- **Sumário do bloco**: mostra `NCM · IPI X% (categoria)` calculado pelo TipiLookup. Quando `_fallback=true`, mostra badge vermelho `⚠ não mapeado`. Quando vendedor override, preview vira itálico azul com ✏️.
- **Campo `sim-ncm-override`**: input livre (ex: 7228.30.00). Vazio = usa automático.
- **Campo `sim-ipi-override`**: input numérico (step 0,01 max 20). Vazio = usa automático.
- **Caveat inline**: "Default usa TIPI Lookup (Decreto 11.158/2022 + ADE COANA 001/2026). Cap. 72 mix AFS = IPI 0%. Override só com validação fiscal."

### Hooks
- `simTipiAtualizarPreview()` engatado em `oninput` do sim-peca-aco e `onchange` do sim-peca-perfil + sim-peca-acabamento.
- Também chamado no fim de `pacoteRestoreFullState` pra atualizar preview ao trocar item ativo.
- `simTipiOverrideAtualizar()` chamado pelos `oninput` dos 2 campos override.

### Persistência
- `sim-ncm-override` e `sim-ipi-override` adicionados no `SIM_SAVE_FIELDS` — pegam carona no save/restore do PACOTE como qualquer outro campo per-item.
- Campos `_tipi_categoria`, `_tipi_fallback`, `_tipi_motivo` (já adicionados na Fase 2C principal) continuam disponíveis pro PDF e pra inspeção.

### Suite pós Fase 2C-extra
1.126 testes verdes — sem regressão. UI puramente DOM-side, não muda comportamento de motor/gerador/schema (todos seguem testes próprios).

### Ainda pendente
- **Validação fiscal formal com contador AFS** (caveat principal — herdado da Fase 2C).
- **Auditoria de propostas geradas 20/04 → 05/05** que viraram NF.
- Reemissão Produsi 900001 Rev.1 hoje.
