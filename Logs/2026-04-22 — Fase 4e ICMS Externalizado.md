---
data: 2026-04-22
tipo: log
projeto: Simulador Precificação
fase: Fase 4e — Parâmetros ICMS externalizados
status: fechado
---

# Fase 4e — simAutoICMS lê de window.AFS_CONFIG.icms

## Resultado

Os valores hardcoded de `simAutoICMS()` (UF de faturamento por cidade, alíquotas interestaduais, regras internas forjado+carbono/usinado) migrados para `window.AFS_CONFIG.icms`. Lógica de detecção (acabamento/liga via string/regex) permanece no HTML.

## O que foi feito

| Arquivo | Mudança |
|---|---|
| `config/parametros_afs.json` | v1.3 → v1.4-fase4e. Seção `regras_icms` (placeholder) substituída por `icms` estruturado. |
| `config/parametros_afs.js` | Mesma versão. Seção `icms` adicionada antes de `tolerancias`. |
| `Analise_Precificacao_Sacchelli.html` | `simAutoICMS()` refatorado: 3 hardcodes → leitura de `icmsCfg`. |

## Estrutura config

```json
"icms": {
  "uf_faturamento": [{ "cidade_contem": "caxias", "uf": "RS" }],
  "uf_faturamento_default": "SP",
  "interestadual": { "nacional_pct": 12, "importado_pct": 4 },
  "regras_internas": [
    { "condicao": "usinado",             "aliquota_pct": 12 },
    { "condicao": "forjado+carbono10xx", "aliquota_pct": 12 },
    { "condicao": "forjado+st52",        "aliquota_pct": 12 }
  ]
}
```

## Lógica que permanece no JS (não parametrizável com custo/benefício)

- Detecção de acabamento via `indexOf('forjado')`, `indexOf('usinado')`
- Regex de liga: `/^10\d{2}[a-z]?$/i` (carbono 10xx) e `/^st[\s\-]?52$/i`
- Lookup no `<select id="sim-icms">` por valor numérico

## Comportamento preservado

| Cenário | Antes | Depois |
|---|---|---|
| Caxias do Sul → UF fat | `indexOf('caxias')>=0?'RS':'SP'` | `uf_faturamento` map, substring |
| Interestadual nacional | `12` hardcoded | `icms.interestadual.nacional_pct` |
| Interestadual importado | `4` hardcoded | `icms.interestadual.importado_pct` |
| Usinado → 12% | `isUsinado?12:erp` | `regras_internas[0]` |
| Forjado+carbono → 12% | `isForjado&&isCarb10xx?12:erp` | `regras_internas[1]` |
| Forjado+ST52 → 12% | `isForjado&&isCarbSt52?12:erp` | `regras_internas[2]` |
| Fallback interno | `erpIcms` (DOM) | `erpIcms` (DOM) — inalterado |

## Validações

- **SYNTAX OK** — `parametros_afs.js`
- **Lógica OK** — Caxias→RS, Guarulhos→SP, Usinado→12 (verificados via Node)
- **555/555 motor tests PASS**
- **Validação em produção:** necessária — testar cotação com cliente RS (Caxias) + cliente interestadual + usinado SP

## Status final hardcodes AFS (pós-Fase 4e)

| Hardcode | Status |
|---|---|
| CF cobrado tabela | ✅ 4a |
| Certificações (19) | ✅ 4a/4c |
| Fases industriais TT/TD/USX/EMB | ✅ 4b |
| Tolerâncias laminado/forjado | ✅ 4d |
| ICMS (UF/alíquotas/regras internas) | ✅ 4e |
| Extra-corte | N/A — configurável via XLSX |
| Tolerâncias h-grade (trefilado/descascado) | Pendente — menor prioridade |
