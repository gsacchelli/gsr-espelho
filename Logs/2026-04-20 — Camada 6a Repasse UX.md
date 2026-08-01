---
data: 2026-04-20
tipo: log
status: vigente
categoria: simulador / pricing
domínio: camada-6a
tags: [simulador, motor, camada-6a, repasse, ux, sprint-3]
---

# 2026-04-20 — Camada 6a Repasse UX

Sessão de retomada do Sprint 3 (wrapper). Opção A escolhida — fechar motor antes de refatorar HTML pra wrapper. Camada 6 decomposta em 6a (UX do Repasse nacional) + 6b (bloco Importação detalhado) + 6c (implementação no motor).

## Decisões tomadas

### Sobre o Repasse (nacional)

**Material livre, sem vínculo com catálogo AFS.** Repasse é material sob encomenda (comprado no mercado ou importado específico pro pedido), não precisa casar com família/liga/perfil/acabamento do produto padrão. Consequência: `sim-mp-estoque-fields` inteiro fica oculto quando Repasse ON. `simCalcRepasse` já usa `sim-peca-perfil`/`sim-peca-de`/`sim-peca-di` (Peça Final) pra coefLin — ocultar não quebra cálculo.

**ICMS com preset, sem opção "Manual".** Dropdown cobre os 5 casos reais (0 / 4 / 7 / 12 / 18%). Quando NF preenchida sem ICMS selecionado, input ganha borda amarela de alerta. Input numérico ao lado aceita digitação livre — opção "Manual..." no dropdown é redundante.

**PIS/Cofins editável, default 9,25%.** Era span fixo. Importação com suspensão/isenção zera; caso padrão mantém default. Campo numérico com vírgula pt-BR.

**Unidade compra logo após preço.** Sequência mental: "compro X a R$ Y por [unidade]" — unidade é informação de primeira ordem, não de segunda. Impostos vêm depois.

**Comprimento oculto quando venda = Kg/Ton.** Granel não precisa de comprimento. Regra: `compRow` visível quando venda ∈ {pc, m, barra}, oculto em {kg, ton}.

### Sobre o fluxo 6b (próxima sessão)

**Opção I confirmada — detalhamento completo de importação.** Baseado na proposta ChatGPT (mais rigorosa que CPIT original) + ajustes AFS:

Campos planejados:
- **Material (4)**: descrição livre (textarea), CFR USD + unit (mt/pc) + moeda (USD/EUR), frete marítimo USD/ton (separado pro AFRMM), seguro % sobre CFR (default 0,30), exchange rate
- **Impostos (5)**: I.IMP %, IPI % (default 0), PIS-Imp % (default 2,10), Cofins-Imp % (default 9,65), ICMS % com preset
- **Despesas locais (3)**: AFRMM % sobre frete (default 25), despesas portuárias R$ absoluto, diversos % sobre subtotal, frete interno R$/ton, comissão trading % (default 0)
- **CF Importação (3)**: % sinal (default 20) + prazo meses (default 8), % final = 100-sinal + prazo (default 3), reusa `sim-selic` do setup

Saídas:
- Custo nacionalizado bruto R$/ton
- **Custo líquido R$/ton** (ICMS + PIS + Cofins recuperáveis descontados) — alimenta `custoLiqTon` do motor
- Landed factor efetivo (referência)

Regra fiscal confirmada com Gustavo: ICMS na importação vai como crédito integral (RPA/lucro real, saídas tributadas). Só impacta fluxo de caixa (capital imobilizado). Daí entra no "líquido" como recuperável.

Material livre também na Importação: descrição textual, sem vínculo com catálogo. Coerente com a regra do Repasse.

### Sobre custo financeiro na importação

CF-Sinal/CF-Final **entram** no CPIT (era minha proposta inicial tirar pra DRE — Gustavo corrigiu). Justificativa: importação tem 8-11 meses de capital imobilizado vs nacional 2-3 meses. Se misturar na DRE genérica, subestima custo da importação. Fica isolado no bloco Importação.

Fórmula linear (confirmada com valores da planilha CPIT):
```
CF_sinal = %sinal × CFR_BRL × Selic × meses_sinal
CF_final = %final × CFR_BRL × Selic × meses_final
```

Comissão da trading (ex: Duferco intermediando importação) também entra no CPIT como custo do material.

## Execução

Patches aplicados em `03_Ferramentas/Analise_Precificacao_Sacchelli.html`. Backup: `_backups/Analise_Precificacao_Sacchelli_pre-camada6a-ux_2026-04-20.html`.

1. Linha 478 (preço) + 493-497 (unidade) → reordenado: unidade logo após preço
2. Linhas 479-491: ICMS preset sem "Manual" + input manual ao lado + handler `_simRepIcmsPresetChange` + alerta `_simRepIcmsAlertCheck`
3. Linha 492: PIS/Cofins virou input editável (id `sim-rep-pis`, default 9,25)
4. Linha 550: ID `sim-familia-softcomp-block` adicionado (dead code após reversão — deixado pra flexibilidade futura)
5. `simToggleRepasse` (~2540): oculta `sim-mp-estoque-fields` inteiro no Repasse
6. `simUpdateRepasseVisibility` (~2605): else branch respeita `sim-qty-unit` — compRow oculto em kg/ton
7. `simCalcRepasse` (~2684): lê PIS dinâmico do input com fallback 9,25
8. Handlers de geometria (linhas 402, 409, 412): `_maybeRecalcRepasse()` injetado pra re-disparar `simCalcRepasse` quando perfil/DE/DI da peça mudam (corrige bug `custoLiqTon='0.00'`)
9. 3 funções helper novas: `_maybeRecalcRepasse`, `_simRepIcmsPresetChange`, `_simRepIcmsAlertCheck` (antes de `simToggleRepasse`)

Sintaxe validada via `node -e` em todos os 5 blocos `<script>`.

## Validação em produção

Gustavo testou 3 cenários:
- **Teste A** — Padrão+Repasse, venda por Kg/Ton: ok. Custo Líq 8.929,80/T com NF 12.000 + ICMS 18 + PIS 9,25 bateu com conta manual.
- **Teste B** — Padrão+Repasse, venda por Peça: ok. Comprimento reaparece.
- **Teste C** — Engenheirado+Repasse, venda por Peça: ok. `dataset.custoLiqTon` sai de 0 quando perfil/DE da peça final são preenchidos.

Ratear custo total (toggle dentro do repasse): comportamento preservado. Aparece quando peso vendido < peso comprado; cliente paga pelo lote integral quando ON.

## Iteração dentro da sessão

Primeira proposta minha errou dois pontos que Gustavo corrigiu:
- Propus manter filtros de material visíveis no Repasse (argumentei que alimentam coefLin) — errado, `simCalcRepasse` usa campos da Peça Final, não filtros. Revertido.
- Propus CF/comissão na DRE — errado, pertencem ao CPIT de importação. Revertido.

Registro: quando Gustavo corrige premissa técnica, quase sempre é porque conhece operação real. Priorizar pergunta específica antes de propor arquitetura.

## Próximos passos

### Camada 6b (próxima sessão)
Bloco Importação dentro do Repasse. Revelar via toggle adicional dentro dos campos MP Repasse (quando ICMS é 0% importação suspensa, ou toggle explícito "Origem Importada"). Desenho detalhado acima.

### Camada 6c (após 6b)
Captura de 2 fixtures reais (Repasse nacional e Repasse importação) + implementação da Camada 6 no `motor_precificacao.js` com regressão bit-idêntica. `dom_to_entrada.js` precisa adaptar schema pra ler os novos campos.

### Após Camada 6 (roadmap Sprint 3)
- Camada 8b ponta completa (card "ponta", spread venda×sucata)
- Camada 8b material comprado (componentes avulsos)
- Wrapper fino — `simCalc()` vira ~30 linhas delegando ao motor

## Conexões

- [[Logs/2026-04-17 — Plano Fases 1+3 Simulador Precificação]] — plano geral
- [[Logs/2026-04-19 — Plano Técnico Refatoração 3 Bases Paralelas]] — Sprint 1-3
- [[Logs/2026-04-19 — Composição MP por Unidade de Venda]] — decisão 3 bases
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]] — arquitetura atual
- [[Sistema Operacional Comercial/02 Precificação/09 - Simulador Web App (futuro)]] — destino final
