---
data: 2026-04-21
tipo: log
status: vigente
tags: [log, decisao, simulador, importacao, motor-pricing, camada-6]
date: 2026-04-21
---

# Camada 6 fechada + CAP com linha dedicada no DRE

## Contexto

Sessão de 21/04/2026. Dois trabalhos principais:

1. **Fechamento formal da Camada 6** (Importação) — validação em produção + fixture bit-idêntica
2. **Reclassificação do Custo Pedido rateado** como linha dedicada no DRE (framework PEC — Custo de Servir vs Custo de Produzir)

Também aconteceu em paralelo:
- **Comparativo Modelos reestruturado** em 3 blocos (recuperação fiscal + composição de custo + informativos)
- **Botão "Nova Proposta"** no card de Proposta Comercial (substitui limpeza manual)

## Camada 6 — fechamento

### Auditoria HTML × motor (manhã)

Revisão linha-a-linha de `simCalcImportacao` (HTML) contra `calcCustoImportacao` (motor). Paridade **bit-idêntica** em todos os 7 passos da cascata fiscal:

- VA = CFR + seguro (sem duplicação de frete marítimo)
- basePisCofins = VA apenas (Lei 12.865/2013, STF RE 559.937 Tema 1 RG)
- SELIC mensal (não anual)
- Custo de hedge isolado (não afeta tributos)
- CIF elimina seguro (já embutido no preço)
- ICMS gross-up por dentro

### Captura em produção

Cenário da fixture real 2026-04-20 05:59 rodado no simulador:
- CFR 575 USD/ton × 10 ton × 5,20 câmbio
- SELIC 1,23% a.m.
- Todas as alíquotas e despesas conforme `fixture_10_repasse_importacao.json`

**Resultado HTML:** custoLiqTon = 4163.7410 R$/ton
**Resultado motor:** custoLiqTon = 4163.74 R$/ton
**Paridade bit-idêntica confirmada** em 5 pontos críticos + 20 campos do breakdown.

### Regressão de 26 testes adicionada ao motor

Bloco "Camada 6 — regressão bit-idêntica fixture 10" em `motor_precificacao.test.js`. Valida cada campo do breakdown com tolerância R$ 0,01:
- VA, IImp, IPI, basePisCofins, PISImp, CofinsImp, tributosFed
- AFRMM, Diversos, Comissão, FreteInt
- baseSemICMS, ICMS, CustoHedge
- CF_sinal, CF_final, CF
- custoBrutoBRL, custoBrutoTon, recuperaveis, custoLiqBRL, custoLiqTon
- landedFactor

Suite total: **689/689 testes verdes** (484 motor + 85 schema + 106 gerador + 14 comparativo).

### Pendências retroativas

- Fixture 09 (Repasse nacional) — capturar na próxima cotação nacional real
- Conferência contra DI arquivada — validação fiscal externa (opcional mas recomendada)

## Reclassificação do Custo Pedido rateado

### Gatilho

O CAP (Custos Adicionais do Pedido — frete CIF, book docs, pallet especial) estava caindo em `dre_custoServExt` junto com TT/TD/USX/EMB. Questão levantada: isso é correto?

### Framework PEC aplicado

No modelo de "fórmula do lucro" (Receita − Descontos − Custo de Produzir − **Custo de Servir**), o CAP é literalmente Custo de Servir — urgências, fretes, retrabalhos, reorçamentos, devoluções, cobrança. Framework separa explicitamente essa categoria de Custo de Produzir (transformação do material).

### Decisão

Linha dedicada no DRE: **"(−) Custo Pedido rateado"** abaixo de Material Comprado. Spread dedicado: **"Spread Custo Pedido rateado"** nos Spreads capturados. No Comparativo Modelos (bloco 3 informativos): **"Margem sobre custo pedido rateado"**.

### Implementação

- Novo bucket `dre_custoServPedido` (separado de `dre_custoServExt`)
- Novo spread `mc2_servPedido` (separado de `mc2_servicos`)
- Classificador do DRE atualizado: `tipo='fase_pedido'` cai em bucket dedicado
- `dreCustoTotal`, `mc2_totalSpreads`, `_totalSpreadsCmp`, `totalSpreadsComp` atualizados
- 3 testes novos em `comparativo_identity.test.js` validando:
  - CAP sem margem: identidade Softcomp + Σ spreads = DRE preservada
  - CAP com margem 20%: spread é informativo, não altera delta
  - CAP R$ 1.000 reduz ambos resultados em R$ 1.000 simetricamente

### Leitura comercial

Vendedor agora enxerga 3 fontes distintas de margem pós-pedido:
- **Spread Serviços (TT/USX/Emb)** — ganho sobre expertise produtiva
- **Spread Material Comprado** — ganho sobre aquisição
- **Spread Custo Pedido rateado** — ganho sobre logística/docs/embalagem especial

Cada um responde a decisão comercial diferente.

## Comparativo Modelos — reestruturação em 3 blocos

### Gatilho

Print do Comparativo mostrou Softcomp 12,99% + só 2,24% em spreads capturados ≠ DRE 17,35%. Gap não explicado de 2,13% (R$ 1.472,71).

### Diagnóstico

O gap se decompõe em duas partes que estavam escondidas em "informativos":

1. **Acréscimo de corte (Camada 1)** — R$ 987,63: Softcomp embute `mc2_corte` no custo MP; DRE remove e contabiliza custo real da máquina.
2. **Certificações internas** — R$ 485,08: Softcomp conta como custo; DRE trata como overhead AFS (orçamento fixo).

### Decisão

Comparativo reestruturado em 3 blocos:

```
(+) Spreads de recuperação fiscal/financeira:
    PIS sobre ICMS (Tema 69)
    Financeiro (Selic × CF)
    Comercial / Comissão / Logística (se ativos)

(+) Margem oculta em custo de produção (Softcomp cobra como custo, DRE reclassifica):
    Acréscimo de corte (embutido no MP Softcomp − custo real máquina)
    Certificações internas (overhead AFS)

Margens cobradas no VT (informativas — presentes em ambos modelos):
    Margem MC sobre corte (Camada 2)
    Margem sobre serviços
    Margem sobre material comprado
    Margem sobre custo pedido rateado
```

### Testes de identidade algébrica

Criado `03_Ferramentas/js/comparativo_identity.test.js` com 14 testes validando Softcomp + Σ spreads = DRE em 6 cenários (base, sem corte, sem cert internas, limpo, stress, prejuízo, com CAP, CAP com margem).

### Nomenclaturas adotadas

- "Acréscimo de corte: embutido no MP Softcomp (R$ X) − custo real da máquina (R$ Y)"
- "Certificações internas: Softcomp conta como custo; DRE trata como overhead AFS (orçamento fixo)"
- "Margem MC sobre corte: MC X% aplicada sobre acréscimo"
- "Margem sobre custo pedido rateado (logística/docs/embalagem especial)"

## Decisões adicionais

### Botão "Nova Proposta"

Gustavo observou que o botão "Limpar" não zerava campos da Proposta Comercial. Solução: botão dedicado "🆕 Nova" no header do card Proposta que:
- Confirma antes de limpar
- Zera cliente/condições/info gerais/custos CAP
- Consome próximo número do contador (sequencial 500.000+)
- Reseta revisão pra "0" (não "00")
- Atualiza data de emissão

Descartado: botão "Duplicar" (não precisa por enquanto).

### Revisão inicial "0" em vez de "00"

Mudança de UX em "Nova" — revisão começa sem padding. `proximaRevisao()` do schema mantém padding "01", "02"... pra retrabalhos.

## Artefatos gerados

- `03_Ferramentas/js/fixtures/fixture_10_repasse_importacao.json` — fixture capturada com input, ctx, expected_motor (20+ campos) e breakdown_html.
- `03_Ferramentas/js/fixtures/CAPTURA_FIXTURE_10.md` — guia de captura reutilizável.
- `03_Ferramentas/js/comparativo_identity.test.js` — 14 testes de identidade algébrica do Comparativo.
- Atualizações em `03_Ferramentas/js/motor_precificacao.test.js` (+26 testes), `03_Ferramentas/Analise_Precificacao_Sacchelli.html` (CAP dedicado + revisões de Comparativo e DRE + botão Nova + paridade fiscal).

## Próximas frentes disponíveis

- **Camada 8b ponta**: card ponta + ajuste custo real de corte (`hrCorte=hrEfetivo` em vez de `hrTotal`)
- **Camada 8b material comprado**: passar do placeholder
- **Wrapper fino**: migração HTML → motor.js via adapter mais limpo (refactor)
- **Gerador de Proposta (Fase 3+)**: schema + UI já existem, falta polir impressão, templates, reabrir orçamentos
- **Fase pós-motor de config**: migrar hardcodes AFS (tabela CF, certificações, fases industriais) pra `parametros_afs.json`
