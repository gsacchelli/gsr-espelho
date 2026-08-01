---
data: 2026-04-22
tipo: log
status: vigente
obs: "fechado"
projeto: Simulador Precificação
fase: Fase 4a — Config AFS externalizada (CF tabela + certificações)
---

# Fase 4a — CF tabela + certificações externalizadas para parametros_afs.json

## Resultado

Grupos A e B da fase pós-motor de config concluídos. Motor deixou de depender de hardcodes para CF cobrado e certificações quando rodando no browser — lê de `window.AFS_CONFIG` via `domToConfig()`. Testes Node continuam usando `DEFAULT_AFS_CERT_PHASES` como fallback (retrocompat).

## O que foi feito

### Arquivos criados/modificados

| Arquivo | Mudança |
|---|---|
| `config/parametros_afs.json` | Versão 1.0-draft → 1.1-fase4a. Adicionada seção `cf_cobrado_tabela`. Seção `certificacoes` populada com os 19 itens reais (era PLACEHOLDER). |
| `config/parametros_afs.js` | **Novo.** Loader browser+Node: define `window.AFS_CONFIG` + `module.exports`. IIFE, `'use strict'`. |
| `Analise_Precificacao_Sacchelli.html` | `<script src="config/parametros_afs.js">` adicionado antes do motor (L.228). |
| `js/dom_to_entrada.js` | `domToConfig()` lê `window.AFS_CONFIG` e passa `cf_cobrado_tabela` + `cert_phases` ao motor. |
| `js/motor_precificacao.js` | Comentário do bloco W3b-2/W3e atualizado (sem mudança de lógica). |

### Grupo A — CF cobrado tabela

```json
"cf_cobrado_tabela": [
  { "prazo_max_dias": 45,   "taxa_pct": 2.0  },
  { "prazo_max_dias": 60,   "taxa_pct": 2.5  },
  { "prazo_max_dias": 9999, "taxa_pct": 3.75 }
]
```

Motor já tinha hook `config.cf_cobrado_tabela` — agora o browser sempre passa o valor do JSON. Fallback hardcoded do motor permanece para testes Node.

### Grupo B — Certificações

19 certificações migradas de dois lugares simultâneos (`SIM_CERT_PHASES` no HTML + `DEFAULT_AFS_CERT_PHASES` no motor) para fonte única no JSON. `domToConfig()` passa como `cert_phases`. Motor usa `certPhases || DEFAULT_AFS_CERT_PHASES` — se config vier (browser), usa JSON; se não vier (Node/testes), usa DEFAULT.

Deduplicação completa (remover DEFAULT do motor) fica para Fase 4b junto com fases industriais.

## Validações

- **SYNTAX OK** — HTML (689k chars JS embutido) + parametros_afs.js
- **555/555 motor tests PASS** — sem mudança aritmética
- **202/202 render tests PASS**
- **Bit-idêntico confirmado via Node:**
  - `calcular(entrada, {})` vs `calcular(entrada, { cert_phases: AFS_CONFIG.certificacoes })` → diferença: 0 ✓
  - `calcCFCobrado(50, {})` vs `calcCFCobrado(50, { cf_cobrado_tabela: ... })` → idêntico ✓
  - Breakpoints CF: 45d → 3.0000 ✓, 61d → 7.6250 ✓
- **Validação em produção:** pendente (abrir simulador, confirmar cotação normal + shadow 0 divergências)

## Arquitetura do fluxo pós-Fase 4a

```
parametros_afs.js (carrega antes do motor)
    → window.AFS_CONFIG

simCalc → domToConfig()
    → { cf_cobrado_tabela: AFS_CONFIG.cf_cobrado_tabela,
        cert_phases: AFS_CONFIG.certificacoes, ... }
    → calcular(entrada, config)
        → calcCFCobrado usa config.cf_cobrado_tabela (não hardcode)
        → aplicarCertificacoes usa config.cert_phases (não DEFAULT)
```

## Próximos passos

1. **Validação em produção** — abrir simulador, cotação normal, shadow 0 divergências
2. **Fase 4b (Grupo C) — Fases industriais:** extrair `SIM_TT/TD/USX/EMB_PHASES` do HTML para `parametros_afs.json/js`, gerar UI dinamicamente do config. Mais complexo — refatoração de UI.
3. **Deduplicação completa (junto com 4b):** remover `DEFAULT_AFS_CERT_PHASES` do motor e `SIM_CERT_PHASES` do HTML. Atualizar testes para importar de `parametros_afs.js`.
