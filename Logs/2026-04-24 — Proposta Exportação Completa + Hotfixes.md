---
data: 2026-04-24
tipo: log
projeto: Simulador Precificação
fase: Fase 4f + Camada 10a + UI Export + PDF i18n + 2 hotfixes
status: fechado
---

# Sessão consolidada — Proposta Exportação USD/EN ativada de ponta a ponta

Sessão longa cobrindo tudo da feature Exportação (saída do parking de 21/04) + 2 bugs encontrados em produção. Estado: feature 100% funcional em produção; débito leve apenas no shadow bloqueante (#5 não estendido pra modo export — vale só se aparecer drift).

## Decisões principais reafirmadas / novas

| Tópico | Decisão |
|---|---|
| Hedge cambial | 100% sintético (via preço). AFS não contrata ACC/NDF; pagamento antecipado → exposição só durante produção/negociação |
| Câmbio no PDF | **SPOT puro** (sem hedge). Hedge fica só nos cards USD do simulador como visão interna do vendedor. Cliente vê câmbio "limpo" |
| Economic Level | **REMOVIDO** do card Export. Validade 2d torna redundante com data de emissão |
| Pacote híbrido (BR+EXP no mesmo orçamento) | Não existe — toggle único na proposta |
| Certificado Mercosul | Injeção automática em Custos Adicionais com flag `_mercosul_auto`; remoção automática ao desligar Export |
| Linhas Freight × Incoterm no PDF | Manter só **INCOTERM** (padrão internacional ICC); Freight é redundante quando EXW |
| Slogan rodapé | Manter em PT mesmo no PDF EN ("SACCHELLI · QUALIDADE DE AÇO") — slogan é identidade de marca, não documento |
| Info Gerais EN | **2 textareas** (PT + EN) com swap pelo toggle. Cada uma preserva edições independentemente |
| MP Repasse + venda Pç | Sim, deveria ter VPP/tolerância — fica como Camada 11 (auto-tolerância). Pendente |

## Entregas

### Fase 4f — bloco `exportacao` no config AFS
`config/parametros_afs.json` v1.5-fase4f + `parametros_afs.js`. Bloco unificado:
```js
exportacao: {
  hedge_default_pct: 3.0,
  certificado_origem: { nome: 'Certificado de Origem Mercosul', valor_default_rs: 2000, ... },
  condicoes_comerciais_padrao: { pagamento_label: 'CAD', frete: 'EXW...', validade_dias: 2, ... },
  info_gerais_texto_en: '...',  // template AFS EN
  incoterm_padrao: 'EXW Sacchelli-Guarulhos',
  moeda_pdf: 'USD',
  idioma_pdf: 'en'
}
```

### Camada 10a — modo export no motor
`entrada.modo_exportacao = true` zera ICMS e PIS no topo de `calcular()` (normalização única, propaga pra DESP / Receita Líquida / DRE Camada 2 sem cada função precisar conhecer a flag). Motor permanece agnóstico de moeda — conversão BRL→USD vive no gerador de proposta.

Adapter `dom_to_entrada.js` lê `prop-exportacao-on` → flag top-level. `debug_to_entrada.js` espelhado.

9 testes sintéticos cobrindo: zeragem ICMS+PIS, preservação CF/DVA/LOG/COM, despFactor, DRE Pedido, Camada 2 cross_term, imutabilidade da entrada original, retrocompat default false, contrato `calcDESP standalone`.

### HTML — UI card Export
- Layout reorganizado: `Exchange Rate` + `Hedge %` lado a lado, **Economic Level removido**, label "Câmbio efetivo: R$ X,XX" dinâmico
- Input Exchange Rate: `type=text inputmode=decimal` com `onblur` formatando pra "0,00" pt-BR. Helper `_simParseBR` aceita "5", "5,8", "5.8", "1.234,56"
- Helper canônico `simGetCambioEfetivo()` retorna `{spot, hedge_pct, efetivo}` — usado no overlay USD dos cards (Verde/Amarela/Vermelha/Preta + **Preço Negociado**, que tinha sido esquecido na primeira passada)

### HTML — injeção Mercosul + Condições + Info Gerais
- `simToggleExportacao(opts)`: orquestra swap UF↔Country, injeção/remoção Mercosul, pré-preenchimento Condições com defaults config, swap textareas Info Gerais PT/EN
- Helpers IIFE expostos: `window._exportacaoAplicarMercosul` (idempotente), `window._exportacaoRemoverMercosul` (filtra por flag `_mercosul_auto`)
- Defaults BR `_COND_DEFAULTS_BR` ↔ defaults EN do config
- 2 textareas `prop-info-texto` + `prop-info-texto-en` com wrappers swappable. Cada uma preserva edições; template EN só popula na primeira vez (se vazio)
- `propostaResetInfoTexto` detecta modo ativo e reseta o textarea correto
- `propostaFromDOM` / `propostaToDOM` persistem ambos `texto` e `texto_en` no meta

### PDF i18n — gerador_proposta + dicionário
- `js/i18n_proposta.js` carregado no HTML (era o bug silencioso — script não estava no HTML, fallback PT-only era usado em runtime)
- `_ctxFromMeta(meta)` cria contexto único `{t, lang, cambio, exportActive, formatMoney, formatData, i18n}` propagado pra todos os builders. Retrocompat: builders sem ctx caem em comportamento PT
- Dicionário cobre header/cliente/intro/itens/inclusos/totais/condições/footer
- `TERMS_PT_EN` traduz perfis (Redondo→Round, etc), acabamentos (Laminado→Hot Rolled, Forjado→Forged, Usinado→Machined…), prazos ("A combinar"→"To be confirmed") e custos_pedido ("Certificado de Origem Mercosul"→"Mercosur Certificate of Origin")
- Conversão BRL→USD via câmbio SPOT. Format en-US `$ 1,234.56`; format date `DD/MMM/YYYY` (ex: `24/Apr/2026`)
- Em export: bloco Créditos fiscais escondido, colunas NCM/ICMS/IPI da tabela ocultas, IPI total fundido em uma linha só, Freight removido (Incoterm cobre), Uso/Impostos das Condições removidos, slogan PT preservado
- Layout `.totais-export`: barra azul ocupa largura total (`grid-template-columns:1fr`); divisória abaixo do título via `border-bottom` do título (atravessa o box inteiro); padding-right 180px nas rows alinha valor com coluna Amount; labels `text-align:right` agrupam consistentemente; `flex-end + gap:20px` aproxima label e valor (sem vão grande no meio)
- Incoterm com país: `EXW - Sacchelli (Guarulhos/SP, Brazil)`
- Header EN: `unidadeBadge` mostra só "GUARULHOS" (sem "UNIT" redundante)
- Pagamento "CAD" force-overridden em export independente do select BR
- Validação City: `propostaFromDOM` lê `prop-cliente-city` em export e `prop-cliente-cidade` em BR — antes lia sempre BR, gerando "City obrigatória" mesmo com City preenchido em export

24 testes novos cobrindo PDF export. Suite gerador 110→136.

## Bugs encontrados em produção (lições)

### Bug 1 — `require()` no motor explodia no browser silenciosamente
**Sintoma:** Card MP Repasse mostrava `R$ 0,00`, console com `[Repasse] motor não carregado` e `[W3e] cards.repasse indisponível`.

**Causa raiz:** linha 1068 do `motor_precificacao.js`:
```js
const DEFAULT_AFS_CERT_PHASES = require('../config/parametros_afs.js').certificacoes;
```

`require` não existe no browser → `ReferenceError` aborta todo o módulo → `window.MotorPrecificacao` nunca é setado.

**Quando entrou:** Fase 4c, 22/04. Log da fase tinha a frase **"validação em produção: não necessária — caminho browser usa config.cert_phases do domToConfig"** — ERRADO. O `require` é executado no LOAD do módulo, antes de qualquer função rodar.

**Por que ficou escondido 2 dias:**
- Cards Verde/Amarela/Vermelha/Preta usavam o cálculo HTML inline legado, não o motor (W3e-A migrou só `cards.repasse`)
- Shadow bloqueante usava `window.MotorPrecificacao` mas falhava silenciosamente
- MP Repasse / W3e-A só dispara código motor quando o checkbox está ON — e ninguém testou Repasse desde 22/04

**Fix (24/04):** detecção de ambiente:
```js
const DEFAULT_AFS_CERT_PHASES = (function(){
    if (typeof require !== 'undefined') {
        try { return require('../config/parametros_afs.js').certificacoes; } catch(e) {}
    }
    if (typeof window !== 'undefined' && window.AFS_CONFIG && window.AFS_CONFIG.certificacoes) {
        return window.AFS_CONFIG.certificacoes;
    }
    return [];
})();
```

**Lição estrutural:** validação em produção NÃO é opcional após mudanças de arquitetura no motor — mesmo que pareça "óbvio" que o caminho browser não usa o código alterado. Bugs silenciosos podem ficar latentes por dias até alguém ativar a feature certa.

### Bug 2 — CP não entrava no denominador do rateio MP Repasse
**Sintoma:** "Sobra de material" exibida 20 kg quando o real era ~10 kg (havia CP de 10 kg consumindo material da mesma barra). Custo rateado superestimava → spread fictício de margem oculta no DRE Camada 2.

**Causa raiz:** `calcCustoLiqRateado` calculava `custo × pesoComprado / pesoPecasKg`. CP era ignorado no denominador (CP era calculado depois no fluxo).

**Decisão Gustavo:**
- CP entra no denominador (CP consome material da mesma barra)
- Lâmina e tolerância **NÃO entram** (são absorvidas no custo unitário, não rateadas)

**Fix:** `calcCustoLiqRateado(entrada, pesoPecasKg, config, cpPesoKg)` — 4º parâmetro opcional. CP calculado early no `calcular()` (`cpInfoEarly`) e reusado no resto do fluxo (zero overhead). HTML `simCalc` espelha mesma lógica.

3 testes novos: retrocompat sem-CP, custo MENOR com-CP (dilui), rateio-OFF ignora CP.

## Arquivos tocados nesta sessão

| Arquivo | Mudança |
|---|---|
| `config/parametros_afs.json` | v1.2-fase4b → **v1.5-fase4f**, bloco `exportacao` |
| `config/parametros_afs.js` | Espelhado |
| `js/motor_precificacao.js` | Camada 10a (modo_exportacao), Hotfix require browser, Hotfix CP rateio |
| `js/motor_precificacao.test.js` | +9 Camada 10a + 3 Hotfix CP |
| `js/dom_to_entrada.js` | Lê `prop-exportacao-on` → `entrada.modo_exportacao` |
| `js/debug_to_entrada.js` | Espelhado |
| `js/i18n_proposta.js` | Dicionário EN expandido + `TERMS_PT_EN` (perfis/acabamentos/prazos/custos_pedido) |
| `js/gerador_proposta.js` | `_ctxFromMeta`, todos os builders aceitam ctx, layout `.totais-export`, conversão USD spot |
| `js/gerador_proposta.test.js` | +24 PDF export + ajustes (City, slogan PT, USD spot) |
| `js/schema_proposta.js` | Validação City já usa `cliente.cidade` (genérico), HTML alimenta corretamente |
| `Analise_Precificacao_Sacchelli.html` | Card Export reformulado, swap textareas Info Gerais, validação `prop-cliente-city` em export, hotfix CP no rateio |

## Status de testes ao fim da sessão

| Suíte | Verde | Antes | Δ |
|---|---|---|---|
| motor_precificacao.test.js | **567** | 555 | +12 (9 export + 3 CP rateio) |
| gerador_proposta.test.js | **136** | 110 | +26 (PDF i18n) |
| schema_proposta.test.js | 85 | 85 | 0 |
| comparativo_identity.test.js | 14 | 14 | 0 |
| render_*.smoke.js (5 suites) | 249 | 249 | 0 |
| **Total** | **1051** | 1013 | +38 |

## Pendências reconhecidas

- **#5 Shadow bloqueante estender pra modo export** — débito leve. Como motor e HTML batem por construção (mesmo guard `isExportacao()` em `simCalcDESP`/`simCalc` espelhando `entrada.modo_exportacao` no motor), não há expectativa de drift. Ativar só se aparecer divergência em uso real.
- **Camada 11 — auto-tolerância em MP Repasse a granel + venda Pç** — discutido com Gustavo. Vendedor esquece de preencher VPP/tolerância nesse cenário, comendo 5-8% de margem em silêncio. Plano:
  - Detecção: `mp_repasse.unidade ∈ {kg, ton}` + `sell_unit = pc`
  - Auto-popular `sim-tol` do `parametros_afs.json` (Fase 4d já tem tabela laminado/forjado por bitola)
  - Auto-popular `sim-lamina` com default 2mm (config novo `cortes.lamina_default_mm` ou hardcoded)
  - Badge visual "🔁 Auto-tolerância: 2,5mm" no campo, editável
  - Flag `_auto:true` que vira `false` ao editar (mesma mecânica do Mercosul)
- **Fixture real Camada 10a** — capturar quando rodar uma cotação export real em produção (Bolívia ou outro destino). Hoje só temos testes sintéticos.
- **Smoke test pro `render_corte.js` piloto** — débito leve já registrado em log anterior.

## Pra retomar

- `arrancar Camada 11` → auto-tolerância MP Repasse Pç
- `validar shadow export` → estender W2.5 pra modo export (#5)
- `capturar fixture export` → próxima cotação Bolívia ou similar

Próxima sessão deveria começar lendo este log + o `CLAUDE.md` atualizado.
