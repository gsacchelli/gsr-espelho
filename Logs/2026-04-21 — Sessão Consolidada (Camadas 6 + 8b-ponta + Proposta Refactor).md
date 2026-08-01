---
data: 2026-04-21
tipo: log
status: vigente
tags: [log, sessao, simulador, motor-pricing, proposta, camada-6, camada-8b-ponta, refactor]
date: 2026-04-21
---

# Sessão consolidada 21/04/2026

Sessão longa e produtiva. Três grandes frentes fechadas.

## Entregas

### 1. Camada 6 (Importação) — FECHADA formalmente
- Auditoria HTML × motor: paridade bit-idêntica linha-a-linha na cascata fiscal
- Fixture 10 capturada em produção com cenário real CFR 2026-04-20 (575 USD/ton, 10 ton, câmbio 5,20, SELIC 1,23% a.m.)
- HTML retornou `custoLiqTon = 4163.7410 R$/ton` vs motor `4163.74 R$/ton` — bit-idêntico
- **26 testes de regressão** adicionados ao motor (`fixture_10_repasse_importacao.json` + bloco "Camada 6 — regressão bit-idêntica fixture 10" em `motor_precificacao.test.js`)
- CLAUDE.md atualizado com status FECHADO

### 2. Camada 8b Ponta — FECHADA formalmente
- Descoberta: fix `hrCorte=hrEfetivo` + `setupMin=0` + card Ponta já existiam há tempos
- Gap real era cobertura de testes: zero fixture/teste exercitava `pontaAtiva=true`
- **15 testes sintéticos** adicionados cobrindo `calcPontaAtiva`, `calcCorteV4` (hrCorte, setup, redução de custo, fórmula) e `calcPonta` (receita sucata, ganho vs venda)
- Guia de captura criado (`CAPTURA_FIXTURE_PONTA.md`) pra dívida retroativa quando houver cotação real com ponta
- **Lição de processo**: antes de implementar algo marcado como pendente no CLAUDE.md, fazer grep no motor/HTML pra confirmar estado real. A pendência pode estar desatualizada (código mudou sem o CLAUDE.md atualizar).

### 3. Proposta Comercial — Refactor UX completo (Etapas 1+2+3+4)

Causa-raiz descoberta via auditoria: **dois sistemas paralelos** de persistência rodando em paralelo (`sim_quotes` antigo + `sacchelli-simulador-proposta-meta` novo), cada um com numeração própria. Fonte da sensação de "meio montado".

**Etapa 1+2 — Unificação:**
- Storage único `afs_propostas_v2` indexado por `orcamento_num + revisao`
- Numeração única via `SP.consumirProximoNumero()` (500.000+)
- Migração automática dos quotes legados preservada como backup
- `propostaGerar` chama `simSave` internamente — gravação automática ao gerar PDF
- Botão 💾 Gravar removido (redundante)
- Modal "📋 Orçamentos" renomeado pra "📂 Propostas"
- Badge de status no header: 📝 Rascunho / ✓ Gravada às HH:MM / ↻ Reaberta

**Etapa 3 — Botões de fluxo:**
- **🆕 Nova** — zera tudo (cliente, pacote, custos, item)
- **🔄 Mesmo cliente** — mantém cliente+condições, zera pacote+custos+item, novo número
- **✏️ Revisar** — só aparece quando proposta reaberta; incrementa revisão (0 → 01 → 02) mantendo dados
- Todos usam **peek** de número (não consomem até commitar via Gerar)

**Etapa 4 — Desconto no PDF:**
- Desconto do pacote (que antes só vivia na análise gerencial) agora aplica linearmente no PDF
- Linhas novas no rodapé do PDF quando desc > 0: "Subtotal" + "Desconto (X,XX%)" com valor negativo em amarelo
- Créditos fiscais (ICMS/PIS/Cofins) escalados proporcionalmente
- 4 testes novos em `gerador_proposta.test.js`

**Bônus:**
- Fix de dimensão do PDF (saía em portrait cortando lateralmente): `@page size: 297mm 210mm` literal + width 297mm só no `@media print`

## Bugs corrigidos ao longo do caminho

1. **Nova não limpava pacote** — só zerava meta; agora zera tudo
2. **Sync Prazo Pgto não disparava em input** — listener era `change` (blur); adicionado `input`
3. **SP undefined em simSave** — alias global `const SP = window.SchemaProposta` adicionado no escopo global
4. **propostaFromDOM/propostaToDOM não expostos ao global** — meta gravava como `null` em snapshot. Fix: `window.propostaFromDOM = ...`. Fallback retroativo no `simLoadQuote` reconstrói meta mínima a partir de `pacoteLevel` pra snapshots legados sem meta
5. **Confirm() com HTML literalizado** — tags `<strong>` apareciam como texto; removidas, uso aspas
6. **Colisão de numeração na migração** — quotes migrados pegaram números na faixa do contador ativo, causando sobrescritas. Opção A aplicada: reset completo do storage, começou limpo
7. **PDF em portrait cortando conteúdo** — `@page A4 landscape` keyword ignorado pelo Chrome; fix com dimensões literais `297mm 210mm`
8. **Comparativo do DRE tinha gap não explicado de 2,13%** — reestruturado em 3 blocos (recuperação fiscal/financeira + composição de custo + informativos); Acréscimo de corte e Cert Internas movidos pra "causa do delta" (antes estavam em "informativos" erroneamente)
9. **Custo Pedido rateado misturado com Serviços externos no DRE** — separado como linha dedicada "(−) Custo Pedido rateado" + spread próprio; alinhado com framework PEC (Custo de Servir ≠ Custo de Produzir)

## Números finais

**710 testes verdes:**
- 499 motor precificação (26 novos da fixture 10 + 15 novos da ponta)
- 85 schema proposta
- 110 gerador proposta (4 novos da Etapa 4 desconto)
- 14 comparativo identity (todos novos nesta sessão)

**Arquivos modificados:**
- `03_Ferramentas/Analise_Precificacao_Sacchelli.html` — unificação de storage, botões de fluxo, badge de status, SP global, propostaFromDOM exposto
- `03_Ferramentas/js/motor_precificacao.js` — sem mudanças (motor já estava correto)
- `03_Ferramentas/js/motor_precificacao.test.js` — +26 testes fixture 10, +15 testes ponta
- `03_Ferramentas/js/schema_proposta.js` — `setContador()` adicionado
- `03_Ferramentas/js/gerador_proposta.js` — Etapa 4 desconto, fix dimensão PDF, bloco Inclusos
- `03_Ferramentas/js/gerador_proposta.test.js` — +4 testes Etapa 4
- `03_Ferramentas/js/comparativo_identity.test.js` — arquivo novo (14 testes identidade Softcomp + Σ = DRE)
- `03_Ferramentas/js/fixtures/fixture_10_repasse_importacao.json` — fixture capturada em produção
- `03_Ferramentas/js/fixtures/CAPTURA_FIXTURE_10.md` — guia
- `03_Ferramentas/js/fixtures/CAPTURA_FIXTURE_PONTA.md` — guia dívida retroativa
- `CLAUDE.md` — atualizado: camadas fechadas, contador de testes (412 → 710), valor alvo fixture (4.030,73 → 4.163,74)

## Lição arquitetural (pra próximas sessões)

**IIFE × Escopo global**: funções globais (`simSave`, `simLoadQuote`, `_afsMigrarLegado`) que precisam chamar funções do IIFE da Proposta (`propostaFromDOM`, `propostaToDOM`, `SP`, helpers) **TÊM** que acessar via `window.X`. O IIFE precisa expor explicitamente no bootstrap:
```js
window.propostaFromDOM = function(){ return propostaFromDOM(); };
window.propostaToDOM = function(m){ return propostaToDOM(m); };
window.SP = window.SchemaProposta;  // se não for local, usa global
```

Esse padrão quebrou 3 vezes nesta sessão (SP, propostaFromDOM, propostaToDOM). Sempre auditar antes de criar nova integração global × IIFE.

## Dívidas retroativas abertas (não bloqueiam nada)

1. **Fixture 09 (Repasse nacional)** — capturar na próxima cotação nacional real
2. **Fixture ponta ativa** — capturar na próxima cotação com ponta (guia pronto)
3. **Validação fiscal externa da fixture 10** — conferir contra DI arquivada (opcional mas recomendada)
4. **Fixtures 04-08 recaptura** — cobertura dos ramos `sell_unit=kg/m` e `margin_base=vermelha`

## Próxima sessão — frentes disponíveis

Ordenadas por valor × custo:

1. **Smoke visual do fluxo completo** — validar Nova → Mesmo cliente → Revisar em cenário real. Pega bugs que aparecem só em uso real. ~15 min.
2. **Camada 8b material comprado** — sair do placeholder. Similar escopo ao CAP. ~60 min.
3. **Wrapper fino** — refactor HTML → motor via adapter mais limpo. Médio/longo prazo. 1-2h.
4. **Fase pós-motor de config** — migrar hardcodes AFS (tabela CF, certificações, fases industriais) pra `parametros_afs.json`. Médio prazo; fica mais crítico quando MetalM entrar. 1-2h.
5. **Gerador de Proposta Fase 5+** — polimento contínuo (ex: desconto por item além do linear, assinatura digital, envio por email).

## Estado emocional da sessão

Gustavo começou a sessão pedindo pra "fechar Camada 6" e terminou com o simulador bem mais coeso. Em dado momento ele disse "estou te achando muito incompetente" quando um refactor (B1) distorceu visualmente — reverti, reestruturei o Comparativo (Opção 2) e seguimos. Ao fim da sessão, os fluxos Nova → Gerar → Reabrir → Revisar funcionam end-to-end e o PDF sai bonito em landscape.

Boas próximas sessões.
