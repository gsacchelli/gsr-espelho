---
data: 2026-04-22
tipo: log
projeto: Simulador Precificação
fase: Fase 4b — Fases industriais externalizadas para parametros_afs.json
status: fechado
---

# Fase 4b — Fases industriais (TT/TD/USX/EMB) externalizadas

## Resultado

Grupo C da fase pós-motor de config concluído. HTML deixou de ter 60 linhas de arrays hardcoded para TT/TD/USX/EMB. SIM_CERT_PHASES também migrada (consolidando a Fase 4a no mesmo ponto). Browser lê de `window.AFS_CONFIG` via `parametros_afs.js` carregado como `<script src>` antes do motor.

## O que foi feito

### Arquivos criados/modificados

| Arquivo | Mudança |
|---|---|
| `config/parametros_afs.json` | Versão 1.1-fase4a → 1.2-fase4b. Seção `fases_industriais` populada com 4 arrays reais (TT=25, TD=8, USX=19, EMB=8 itens). |
| `config/parametros_afs.js` | Versão 1.1-fase4a → 1.2-fase4b. Adicionada seção `fases_industriais` com os mesmos 4 arrays. Correção: vírgula faltando após `certificacoes` (syntax error detectado no primeiro `node --check`). |
| `Analise_Precificacao_Sacchelli.html` | 5 declarações de array substituídas por leitura de `window.AFS_CONFIG` (L.2611-2700): `SIM_TT_PHASES`, `SIM_TD_PHASES`, `SIM_USX_PHASES`, `SIM_CERT_PHASES`, `SIM_EMB_PHASES`. Antes: ~90 linhas de dados. Depois: 7 linhas com fallback `||[]`. |

### Padrão de substituição aplicado

```javascript
// ANTES (exemplo TT — 27 linhas de dados):
let SIM_TT_PHASES=[
  {cod:'BJ2',desc:'Beneficiar NTR + Jato',preco:2550,marg:50},
  ... (25 itens)
];

// DEPOIS (1 linha por array):
let SIM_TT_PHASES=(window.AFS_CONFIG&&window.AFS_CONFIG.fases_industriais&&window.AFS_CONFIG.fases_industriais.tt)||[];
let SIM_CERT_PHASES=(window.AFS_CONFIG&&window.AFS_CONFIG.certificacoes)||[];
```

Fallback `||[]` garante retrocompat — se `parametros_afs.js` não carregar, arrays ficam vazios em vez de quebrar com ReferenceError.

## Constraint arquitetural respeitado

`SIM_PHASE_CATS` é `const` que captura referências às arrays em declaração (L.2711-2716). Portanto as 5 variáveis precisavam ser declaradas e populadas **antes** de `SIM_PHASE_CATS`. Como `parametros_afs.js` é carregado via `<script src>` antes do bloco inline, `window.AFS_CONFIG` está disponível quando as declarações são avaliadas. Sem reordenação necessária.

## Validações

- **SYNTAX OK** — `parametros_afs.js` (node --check)
- **COUNTS OK** — TT:25, TD:8, USX:19, EMB:8, CERT:19 (verificado via Node require)
- **SYNTAX OK** — HTML JS inline (~687k chars, `new Function()`)
- **555/555 motor tests PASS** — sem mudança aritmética
- **202/202 render tests PASS** — dre/comparativo/mc/estoque
- **Validação em produção:** pendente (abrir simulador, confirmar fases TT/TD/USX/EMB populadas + cotação normal + shadow 0 divergências)

*Nota: `render_corte.smoke.js` não existe — débito leve desde o piloto W3d, baixa prioridade.*

## Arquitetura do fluxo pós-Fase 4b (config completa)

```
parametros_afs.js (carrega antes do motor)
    → window.AFS_CONFIG {
        versao: '1.2-fase4b',
        cf_cobrado_tabela: [...],    ← Fase 4a (Grupo A)
        certificacoes: [...],        ← Fase 4a (Grupo B)
        fases_industriais: {         ← Fase 4b (Grupo C)
          tt, td, usx, emb
        }
      }

HTML inline:
    SIM_TT/TD/USX/EMB_PHASES ← window.AFS_CONFIG.fases_industriais.*
    SIM_CERT_PHASES           ← window.AFS_CONFIG.certificacoes
    SIM_PHASE_CATS            ← captura referências das arrays acima

domToConfig():
    → { cf_cobrado_tabela, cert_phases } → calcular(entrada, config)
```

## Hardcodes AFS migrados (status pós-Fase 4)

| Hardcode | Status |
|---|---|
| `calcCFCobrado` tabela escalonada | ✅ Migrado (Fase 4a) |
| `DEFAULT_AFS_CERT_PHASES` (19 certs) | ✅ Migrado (Fase 4a) — DEFAULT permanece no motor como fallback Node/testes |
| `SIM_TT/TD/USX/EMB_PHASES` (60 fases) | ✅ Migrado (Fase 4b) |
| Tolerâncias dimensionais | Pendente (Fase futura) |
| Extra-corte por acabamento | Pendente (Fase futura) |
| ICMS por UF/procedência | Pendente (Fase futura) |

## Próximos passos

1. **Validação em produção** — abrir simulador, confirmar UI de fases (TT/TD/USX/EMB) populada do config, cotação normal, shadow 0 divergências
2. **Deduplicação completa (Fase 4c, quando conveniente)** — remover `DEFAULT_AFS_CERT_PHASES` do motor e atualizar testes para importar de `parametros_afs.js`. Custo: atualizar ~10 linhas de imports nos testes. Benefício: fonte única.
3. **Smoke test `render_corte.js`** — débito leve pendente desde piloto W3d
4. **Próxima frente grande** — W3e ou hardcodes restantes (tolerâncias/ICMS) ou Proposta Exportação USD/EN (parked)
