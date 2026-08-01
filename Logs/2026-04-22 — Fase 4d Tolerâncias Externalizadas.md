---
data: 2026-04-22
tipo: log
status: vigente
obs: "fechado"
projeto: Simulador Precificação
fase: Fase 4d — Tolerâncias dimensionais externalizadas
---

# Fase 4d — SIM_TOL_LAMINADO/FORJADO externalizados

## Resultado

`SIM_TOL_LAMINADO` (11 faixas, EN 10060:2003) e `SIM_TOL_FORJADO` (11 faixas, Villares Metals) migrados de hardcode no HTML para `window.AFS_CONFIG.tolerancias`. Padrão idêntico à Fase 4b.

## O que foi feito

| Arquivo | Mudança |
|---|---|
| `config/parametros_afs.json` | v1.2-fase4b → v1.3-fase4d. Seção `tolerancias` populada (laminado: 11 itens, forjado: 11 itens). |
| `config/parametros_afs.js` | Mesma versão. Seção `tolerancias` adicionada após `fases_industriais`. |
| `Analise_Precificacao_Sacchelli.html` | 2 `const` com 28 linhas de dados → 2 linhas com leitura de `window.AFS_CONFIG.tolerancias.*`. |

## Validações

- **SYNTAX OK** — `parametros_afs.js`
- **Counts OK** — laminado:11, forjado:11
- **Spot checks** — lam Ø50mm → 0.8mm ✓, for Ø250mm → 7.2mm ✓
- **555/555 motor tests PASS**
- **Validação produção:** não necessária (simAutoVPP é UI-only, zero aritmética de motor)

## Status hardcodes AFS (pós-Fase 4d)

| Hardcode | Status |
|---|---|
| CF cobrado tabela | ✅ 4a |
| Certificações (19) | ✅ 4a/4c |
| Fases industriais TT/TD/USX/EMB | ✅ 4b |
| Tolerâncias laminado/forjado | ✅ 4d |
| ICMS por UF/procedência/acabamento | Pendente (Fase 4e) |
| Extra-corte | N/A — já configurável via XLSX |
