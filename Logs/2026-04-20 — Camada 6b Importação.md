---
tipo: log-execução
categoria: simulador / pricing
domínio: camada-6b
data: 2026-04-20
tags: [simulador, motor, camada-6b, importação, repasse, sprint-3]
---

# 2026-04-20 — Camada 6b Importação

Continuação direta da 6a (Repasse UX). Bloco Importação completo dentro do Repasse: 22 inputs em 5 seções, cascata de cálculo para custo nacionalizado bruto e líquido em R$/ton, pipe para o motor downstream sem tocar no núcleo.

## Decisões tomadas

### Ativação e layout

**Toggle explícito "Origem Importada"** dentro de `#sim-mp-repasse-fields`, no topo do painel. Sem auto-open via ICMS=0 (discutido, descartado — importação nem sempre tem ICMS suspenso; acoplar dois triggers confunde).

**Swap completo — campos nacionais somem quando Importação ON.** Alternativas (aditivo, accordion) descartadas: poluição visual, ambiguidade sobre qual preço vale. Um modo por vez.

**Quantidade do lote vive no próprio bloco Importação** (`sim-imp-qty` + unidade do CFR), não reusa `sim-rep-qty`. Motivo: unidade de compra na importação é `mt`/`pc` (CFR), diferente do nacional (`kg`/`ton`/`pc`/`m`). Duplicar é menos ruído que forçar conversão bidirecional.

### Fórmula e arquitetura

**Cálculo cascata fiel.** Escolha confirmada contra simplificada. Regras:
- IPI incide sobre VA + I.IMP (não só sobre VA)
- Diversos incide sobre VA + tributos federais (não só sobre VA)
- ICMS gross-up por dentro: `ICMS = Base × i/(1−i)` — integra a própria base, padrão para DI

**Seis passos do cálculo, em ordem:**
1. Base em R$: `VA = CFR_BRL + Frete_BRL + Seguro`
2. Tributos federais cascata: `I.IMP`, `IPI s/VA+II`, `PIS-Imp`, `Cofins-Imp`
3. Despesas locais (compõem base do ICMS): `AFRMM s/frete`, `Portuárias R$`, `Diversos s/VA+trib`, `Comissão trading s/CFR`, `Frete interno R$/ton`
4. ICMS gross-up por dentro sobre `VA + trib federais + AFRMM + Portuárias + Diversos`
5. Custo financeiro isolado: `CF_sinal = %sinal × CFR_BRL × SELIC_mensal × meses_sinal`, idem final. SELIC do Setup, convertida para mensal equivalente composto
6. Custo bruto = soma tudo. Custo líquido = bruto − recuperáveis (ICMS + PIS + Cofins)

**Recuperáveis = ICMS + PIS-Imp + Cofins-Imp.** Premissa RPA/lucro real com saídas tributadas (conforme decisão 6a). IPI fora dos recuperáveis por default — aço não costuma creditar.

**CFR com unit select `mt`/`pc` + moeda USD/EUR.** Cobre forjados grandes cotados por peça (caso 4340 Ø508 da Duferco) além de commodity por tonelada. Frete marítimo sempre USD/ton.

**Final% readonly = 100 − Sinal%.** Sinal e Final sempre somam 100%. Evita incoerência.

### Defaults AFS confirmados

| Parâmetro | Default |
|---|---|
| Seguro sobre CFR | 0,30% |
| AFRMM sobre frete marítimo | 25,00% |
| PIS-Imp | 2,10% |
| Cofins-Imp | 9,65% |
| I.IMP | 0,00% (usuário preenche caso a caso) |
| IPI | 0,00% |
| Diversos | 0,00% |
| Comissão trading | 0,00% |
| CF Sinal | 20% × 8 meses |
| CF Final | 80% × 3 meses |
| ICMS preset | 0 / 4 / 7 / 12 / 18% com input editável |

## Execução

Patches aplicados em `03_Ferramentas/Analise_Precificacao_Sacchelli.html`. Backup: `_backups/Analise_Precificacao_Sacchelli_pre-camada6b_2026-04-20.html`.

### UI (linhas ~478-580)
- Toggle `sim-imp-on` "Origem Importada" com hint "custo nacionalizado"
- Wrapper `sim-rep-nacional-inputs` envolvendo os campos nacionais
- Bloco `sim-mp-import-fields` em 5 seções: MATERIAL (7 inputs: descrição, CFR + moeda + unit, Qty, Peso/Pç condicional, Frete mar, Seguro, Câmbio) / TRIBUTOS FEDERAIS (4) / ICMS (preset + manual, idêntico padrão do Repasse nacional) / DESPESAS LOCAIS (5) / CUSTO FINANCEIRO (Sinal%×meses + Final%×meses, SELIC do Setup)
- Saídas específicas: Custo BRUTO R$/ton + Landed Factor

### JS (linhas ~2678-2745 e ~2940-3050)
- 5 helpers novos: `simToggleImportacao`, `_simImpUnitChange`, `_simImpIcmsPresetChange`, `_simImpIcmsAlertCheck`, `_simImpCfSync`
- `simCalcImportacao()` com cascata em 6 passos
- `simCalcRepasse()` delega quando `sim-imp-on` ON
- `simToggleRepasse()` reseta `sim-imp-on.checked=false` quando Repasse desliga (evita estado inconsistente)
- `simUpdateRepasseVisibility()` respeita `sim-imp-cfr-unit` no modo importação (comprouPeca se cfrUnit='pc')

### Pipe pro motor
Saída alimenta `sim-rep-nf.dataset.custoLiqTon` e `.pesoTotalKg` — mesmo canal que o Repasse nacional usa hoje. **Zero mudança no motor principal.** `simCalc()` continua lendo os dataset attributes e roda normalmente.

Sintaxe validada via `node --check` no bloco script inline (único agora, ~568k chars).

## Smoke tests (aritmética isolada em Node)

Replicamos a função em Node puro e rodamos 3 cenários:

| Cenário | Qty | VA (R$) | ICMS | Bruto/ton | Líq/ton | Landed |
|---|---|---|---|---|---|---|
| **A** — 4340 Ø508 forj, CFR 1800 USD/ton, 20t, ICMS 18%, SELIC 13% | 20t | 191.540 | 50.050 | 14.571 | **10.944** | 1,216× |
| **B** — idem A, ICMS 0% (suspensão) | 20t | 191.540 | 0 | 12.069 | **10.944** | 1,216× |
| **C** — 5 pç × 1200kg, CFR 2800 USD/pç, I.IMP 12%, comissão 3% | 6t | 73.510 | 15.881 | 20.962 | **15.948** | 1,367× |

Valores batem com cálculo manual em planilha.

## Observação estratégica — ICMS invisível no líquido

**A = B no custo líquido (R$ 10.944/ton em ambos), apesar do ICMS ser 18% vs 0%.** Matematicamente correto pela premissa "ICMS = crédito integral em RPA" — entra no bruto, sai no líquido.

**Implicação prática:** o modelo atual não captura o custo financeiro do **capital imobilizado em ICMS pago na DI**. No Cenário A, a AFS desembolsa ~R$ 50k de ICMS que só recupera contra vendas futuras. Esse R$ 50k fica parado por X meses até ser compensado — custo de capital real.

Hoje o CF-Sinal/CF-Final corre sobre o CFR_BRL apenas. Para capturar o ICMS, precisaria de um CF extra: `CF_ICMS = ICMS × SELIC_mensal × meses_compensação`. Seria Camada 6b.1 se/quando virar prioridade. Por ora, aceito na premissa — Gustavo conhece o buraco e decidiu não tapar agora.

## Validações pendentes

1. **Teste em produção com cenário real.** Abrir HTML, ativar MP Repasse → Origem Importada, preencher caso concreto (ex: última importação AFS ou proposta Duferco ativa) e conferir se o card Repasse atualiza conforme esperado. Preferencialmente bater linha a linha contra planilha de importação antiga.
2. **Fixture retroativa 6b** (Camada 6c): capturar via botão Debug um snapshot real com importação preenchida + SIM_LAST_CALC correspondente. Só então implementar Camada 6 no `motor_precificacao.js` com regressão bit-idêntica.

## Iteração dentro da sessão

Propostas corrigidas por Gustavo:
- Inicialmente chamei o cálculo de "CPIT". Corrigido: CPIT é nome de usina (não de metodologia). Renomeado para "custo nacionalizado" / "Importação" em todos os comentários e no hint do toggle.
- Ícone "ℹ ICMS = crédito integral em RPA" proposto para explicar a observação A=B. Descartado — usuário prefere UI limpa, seletor ICMS já comunica o padrão operacional.

## Próximos passos (Sprint 3 em curso)

### Camada 6c — próxima sessão
1. Abrir HTML, rodar cenário real de importação até convergir com cálculo manual (ou planilha antiga).
2. Capturar 2 fixtures via botão Debug: 1 Repasse nacional + 1 Repasse importação.
3. Implementar Camada 6 no `motor_precificacao.js` com adapter atualizado em `dom_to_entrada.js` lendo os novos campos `sim-imp-*`.
4. Regressão bit-idêntica contra `SIM_LAST_CALC`.

### Depois de fechar Camada 6
- Camada 8b ponta completa (card "ponta", spread venda × sucata, ajuste corte real quando ponta ativa)
- Camada 8b material comprado (componentes avulsos)
- Wrapper fino — `simCalc()` reduz pra ~30 linhas delegando ao motor

## Conexões

- [[Logs/2026-04-20 — Camada 6a Repasse UX]] — sessão imediatamente anterior, decisões sobre Repasse nacional
- [[Logs/2026-04-17 — Plano Fases 1+3 Simulador Precificação]] — plano geral
- [[Logs/2026-04-19 — Plano Técnico Refatoração 3 Bases Paralelas]] — Sprint 1-3
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]] — arquitetura atual
- [[Logs/2026-04-17 — Estrutura Duferco-Brasil]] — processo estratégico que pode alimentar fixture real de importação
