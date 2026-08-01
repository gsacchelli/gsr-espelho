---
data: 2026-04-20
tipo: log
status: vigente
categoria: simulador / pricing / fiscal
domínio: bloco-importação
tags: [simulador, importação, fiscal, hedge, siscomex, incoterm, breakdown, impressão]
---

# 2026-04-20 — Bloco Importação Consolidado

Sessão longa de aprofundamento e correção do bloco Importação do simulador de precificação. Começou com auditoria fiscal (erro que eu introduzi na base PIS/Cofins e o Gustavo cobrou verificação), e evoluiu pra redesenho completo da cascata, UX, persistência e impressão.

## O que ficou pronto hoje

### Correções fiscais (auditoria completa)

1. **Base PIS/Cofins-Importação = APENAS VA** (Lei 12.865/2013, STF RE 559.937). Reverti erro meu anterior que tinha acrescentado II+IPI baseado em código Python do ChatGPT sem verificar fonte primária.
2. **Cofins-Imp 9,65% mantida pra aços** — confirmei via pesquisa na gov.br/pgfn que adicional da Lei 14.973/2024 (escalonado 0,8pp→0,6pp→0,4pp até 2028) incide apenas sobre 17 setores desonerados (CPRB). Aços (NCM 7218-7228) NÃO estão na lista.
3. **Semântica do campo SELIC corrigida**: campo `sim-selic` é mensal (label "% a.m."), mas motor tratava como anual convertendo pra mensal composto → subestimava CF em ~12x. Corrigido: motor agora usa SELIC mensal direto.
4. **VA sem duplicação de frete** — CFR já inclui frete por INCOTERM, não soma de novo.
5. **Auditoria completa** de todos os tributos registrada em `Logs/2026-04-20 — Auditoria Fiscal Importação.md`.

### Seletor INCOTERM (CFR / CIF)

Dropdown inline no próprio campo de preço. CFR (padrão) soma seguro no VA. CIF esconde e zera seguro automaticamente (evita dupla contagem). Motor tem proteção dupla: mesmo se usuário forçar seguro > 0 em CIF, é ignorado.

### Câmbio — arquitetura final (Opção A+)

**Dois câmbios distintos, cada um com propósito:**
- **Câmbio fiscal (cascata):** nominal puro. Aplicado em VA, II, IPI, PIS, Cofins, ICMS, AFRMM. Correto pelo Dec. 6.759/09 art. 97 (PTAX do dia do registro da DI, independente de hedge).
- **Câmbio operacional (landed):** nominal × (1 + hedge%). Usado como denominador do landed factor — é o câmbio que o Gustavo aplica mentalmente na fórmula rápida de precificação.

**Hedge aparece duas vezes com propósitos diferentes:**
- Como linha explícita **"Custo de Hedge"** no bruto (prêmio real pago ao banco sobre parcela Final): `final% × CFR_BRL × hedge%`. NÃO é recuperável.
- Embutido no denominador do landed factor (pra fórmula rápida fechar matematicamente).

**Nomenclatura dos campos:**
- "Câmbio de referência" (antes "Câmbio → BRL"): tooltip explica que aqui embute "gordura" de estimativa pro dia do desembaraço.
- "Hedge final (%)" (antes "Hedge câmbio"): tooltip distingue entre hedge real contratado (vai aqui) e gordura de estimativa (vai no câmbio de referência).

### Taxa Siscomex

Campo próprio separado (R$ absoluto). Default R$ 214,50 (Port. ME 4131/2021). Integra base do ICMS-Importação (tributo federal aduaneiro). Tooltip documenta a estrutura (R$ 214,50 base + R$ 38,56 por adição até a 2ª).

### Outras correções/renomeações

- "Portuárias (R$ total)" → **"Despesas portuárias (R$)"** (padronização com "Despesas diversas").
- Frete Marítimo ganhou label "(já incluso no preço)" + tooltip explicando que em CFR/CIF serve apenas como base do AFRMM.
- Tooltips enciclopédicos em I.IMP, IPI, PIS, Cofins, AFRMM citando base legal (leis, STF, STJ).

### Breakdown detalhado

**5 colunas agora**: Item | Unit R$/T | % Bruto | % Líq | Total R$.

- **% Bruto**: composição do custo bruto antes de recuperar. Ex: VA = 58,4% do bruto.
- **% Líq**: contribuição real ao custo líquido após recuperar ICMS/PIS/Cofins. Recuperáveis mostram 0% (neutros no caixa). Ex: VA = 71,6% do líquido (sobe porque recuperáveis saíram).

**Sequência fiscal explícita**:
VA → (+) II → (+) IPI → (+) PIS → (+) Cofins → (+) AFRMM → (+) Despesas portuárias → (+) Siscomex → (+) Diversos → **Base ICMS** → (+) ICMS gross-up → **Subtotal nacionalizado** → (+) Comissão → (+) Frete Interno → (+) Custo de Hedge → (+) CF Sinal → (+) CF Final → **Custo Bruto** → (−) Créditos recuperáveis → **Custo Líquido**.

**Landed Factor com fórmula inline** no display: "1,34× (4.452,98 = 635,00 × 5,2500 × 1,3357)".

### Defaults Importação migrados pro Setup

Nova seção no menu Setup com 17 campos editáveis (INCOTERM, frete marítimo, seguro, hedge, alíquotas fiscais, AFRMM, portuárias, Siscomex, diversos, frete interno, comissão, parcelas CF). Persistência via `SETUP_LS_FIELDS`. Botões:
- **"↺ Restaurar defaults AFS"** — reverte aos valores originais
- **"Aplicar ao simulador"** — força aplicação imediata

`simLoadImpDefaults()` copia Setup → sim-imp-*. Chamado em `simLoadSetupDefaults()` (boot) e `simClear()` (limpeza).

`simClear()` agora limpa corretamente MP Repasse + Importação (antes persistiam ao limpar orçamento).

### Persistência

Todos os 30+ campos `sim-imp-*` e `sim-rep-*` adicionados ao `SIM_SAVE_FIELDS`. Estado sobrevive ao refresh. Após restore, `simToggleRepasse`/`simToggleImportacao`/`_simImpIncotermChange` são disparados na ordem correta pra reaplicar visibilidade.

Bug crítico do "Venda por" resetando pra Pç no refresh — corrigido com tripla proteção (chamada imediata + setTimeout 150ms + setTimeout 500ms).

### Impressão

Breakdown Importação aparece na Página 2 (Análise da Margem) quando ativo. Layout em grid 2 colunas:
- Esquerda: Breakdown Importação (cascata completa)
- Direita: DRE (em cima) + Comparativo Softcomp × DRE (abaixo) — leitura coerente

Fontes comprimidas (6px no breakdown, 7,5px nos outros) + padding reduzido → tudo cabe em uma página A4 paisagem.

Header do breakdown na impressão mostra contexto: INCOTERM, descrição do material, preço, qty, câmbio + hedge, custo líq unit, custo total, landed factor.

### Motor de precificação — estado atual

- **458 testes verdes** (zero regressão)
- `calcCustoImportacao(importacao, ctx, config)` — cascata canônica em 7 passos (VA → tributos fed → despesas locais → base ICMS → ICMS gross-up → custo de hedge → CF → bruto → líquido)
- `calcCustoLiq` integrado: importação ativa → motor calcula cascata; nacional → fallback dataset
- `calcCustoLiqRateado` trata rateio venda < lote
- Breakdown exposto em `window.SIM_LAST_CALC_IMP` com 30+ campos

## Impacto numérico vs estado inicial

Cenário típico (CFR 635 USD/ton, 10t, câmbio 5,00 + hedge 5%, ICMS 12%, SELIC 1,25% a.m.):

| Versão | Custo líq R$/ton | Observação |
|---|---|---|
| Original (vários bugs) | 4.393,64 | frete duplicado + base PIS errada + SELIC a.a. |
| Após correções fiscais + SELIC mensal | 4.163,74 | base PIS só VA (correção STF) |
| Com Siscomex + Diversos 3% + Comissão 3% (cenário real) | 4.452,98 | cenário completo Opção A+ |

**A matemática está hoje fiscalmente correta e validada contra fontes primárias** (Receita Federal, PGFN, STF, STJ, Planalto).

## Gate pendente pra fechar Camada 6 definitivamente

Pela regra de cobertura (documentada no CLAUDE.md), a Camada 6 só fecha com **fixture real capturada exercitando todos os ramos + regressão bit-idêntica contra `SIM_LAST_CALC.imp`**. Até lá, a Camada 6 permanece em estado "parcial" mesmo com 458 testes sintéticos verdes.

Próxima sessão do simulador: capturar `fixture_09_repasse_nacional.json` + `fixture_10_repasse_importacao.json` via botão Debug e rodar regressão formal.

## Projeto futuro — Tabela Comparativa Importação vs Gerdau vs Sacchelli

Gustavo registrou que quer usar a mesma lógica da cascata de importação do motor pra construir uma **tabela comparativa de custos e preços** entre:
- **Importação** (motor atual — custo nacionalizado calculado)
- **Gerdau** (preço de aquisição no mercado interno — usina direto)
- **Sacchelli** (preço que a AFS pratica atualmente, com margem)

Útil pra:
- Decisão make-or-buy (importar vs comprar nacional)
- Benchmark de posicionamento comercial
- Identificar onde importação compensa vs Gerdau
- Estratégia competitiva da MetalM

**Escopo implícito:** tabela com dimensão NCM/liga/bitola × 3 colunas de custo/preço. Motor de importação já entrega uma das colunas. As outras dependem de integração com tabelas Gerdau (possivelmente manual por enquanto) e carteira Sacchelli (vem do ERP).

Registrado como memória separada pra retomar.

## Conexões

- [[Logs/2026-04-20 — Auditoria Fiscal Importação]] — base legal de cada tributo
- [[Logs/2026-04-20 — Camada 6c Pre-work]] — contexto técnico motor
- [[Logs/2026-04-20 — Camada 6a Repasse UX]] — 1ª sessão do dia
- [[Logs/2026-04-20 — Camada 6b Importação]] — 2ª sessão do dia
- [[Logs/2026-04-17 — Plano Fases 1+3 Simulador Precificação]] — plano geral do refactor
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]] — arquitetura do simulador
