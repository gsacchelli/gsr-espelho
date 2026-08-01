---
data: 2026-04-22
tipo: log
projeto: Simulador Precificação
fase: Fase 4c — Deduplicação completa das certificações
status: fechado
---

# Fase 4c — DEFAULT_AFS_CERT_PHASES removido do motor

## Resultado

Deduplicação completa das certificações. As 19 certs agora têm fonte única em `parametros_afs.js`. Motor, HTML e testes leem do mesmo objeto (Node module cache garante referência idêntica).

## O que foi feito

### Arquivo modificado

| Arquivo | Mudança |
|---|---|
| `js/motor_precificacao.js` | `DEFAULT_AFS_CERT_PHASES` de 19 linhas hardcoded → `require('../config/parametros_afs.js').certificacoes` (1 linha). Exportação e uso interno inalterados. |

### Antes / Depois

```javascript
// ANTES (19 linhas de dados duplicados):
const DEFAULT_AFS_CERT_PHASES = [
    { cod:'AQ1', desc:'Análise Química (S+Usina)', tipo:'pct_custo', ... },
    // ... 18 itens mais
];

// DEPOIS (1 linha — fonte única):
const DEFAULT_AFS_CERT_PHASES = require('../config/parametros_afs.js').certificacoes;
```

### Por que esta abordagem

- Testes importam `DEFAULT_AFS_CERT_PHASES` do motor (L.28) — interface pública inalterada
- Motor usa `certPhases || DEFAULT_AFS_CERT_PHASES` internamente — fallback Node continua funcionando
- Browser passa `cert_phases` via `domToConfig()` (de `window.AFS_CONFIG.certificacoes`) — caminho browser não toca o require
- `DEFAULT_AFS_CERT_PHASES === AFS_CONFIG.certificacoes` → `true` (Node module cache, mesma referência)

## Validações

- **555/555 motor tests PASS** — sem mudança aritmética, require resolve corretamente
- **19 itens** — [0] AQ1, [18] JBS (corretos)
- **Mesma referência** confirmada: `DEFAULT_AFS_CERT_PHASES === require('../config/parametros_afs.js').certificacoes → true`
- **Validação em produção:** não necessária — mudança zero impacto no browser (caminho browser usa `config.cert_phases` do domToConfig, não o fallback Node)

## Estado final da deduplicação de certs

| Local | Antes | Depois |
|---|---|---|
| `motor_precificacao.js` | 19 linhas hardcoded | `require('../config/parametros_afs.js').certificacoes` |
| `Analise_Precificacao_Sacchelli.html` | 21 linhas hardcoded (`SIM_CERT_PHASES`) | `(window.AFS_CONFIG&&window.AFS_CONFIG.certificacoes)\|\|[]` (Fase 4b) |
| `config/parametros_afs.js` | — | Fonte canônica (19 itens) |
| `config/parametros_afs.json` | — | Fonte canônica espelhada |

## Fase pós-motor de config — CONCLUÍDA

Grupos A, B e C fechados. Todos os hardcodes de catálogo AFS migrados para `parametros_afs.json/js`.

Hardcodes residuais restantes (fora do escopo desta fase):
- Tolerâncias dimensionais
- Extra-corte por acabamento  
- ICMS por UF/procedência
