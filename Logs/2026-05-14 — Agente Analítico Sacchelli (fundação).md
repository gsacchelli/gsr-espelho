---
data: 2026-05-14
tipo: log
status: vigente
obs: "12 funções canônicas entregues, validadas em produção real"
contexto: Agente Analítico Sacchelli — Fase 1 (fundação)
tags: [agente, sacchelli, fase-1, fundação, python, pandas, sessão]
---

# 2026-05-14 — Agente Analítico Sacchelli (fundação)

## TL;DR

Construída a fundação do Agente Analítico Sacchelli — biblioteca Python que consulta os cubos OLAP do Motor Analítico e responde perguntas comerciais em linguagem natural. **12 funções canônicas entregues** cobrindo Vendas, Cotações, Estoque, Pedidos e Pricing. Validadas em produção contra 6 perguntas reais que o Gustavo fez na sessão.

Decisões arquiteturais importantes:
- **Funções canônicas determinísticas** em Python (NÃO "Claude gera pandas livre" — caro, inconsistente, difícil de testar)
- **Cubos OLAP como fonte primária** (95% das perguntas), enriquecidos só pra drilldown
- **Portabilidade pro futuro app cloud** — biblioteca não depende do Claude Code
- **Cache RAM module-level** — primeira consulta carrega ~3s, próximas instantâneas

Documentação técnica vivendo em `Sistema Operacional Comercial/08 Agente Analítico/` (Visão Geral, Funções, Caveats).

## Decisões arquiteturais — antes de qualquer código

**Brief original do Gustavo** propunha arquitetura "Claude API → pandas → Claude API" rodando como serviço externo acessando Google Drive. Três problemas:

1. **Drive desnecessário:** a working directory `/Users/gustavosacchelli/Documents/Personal/00. Projetos - Claude/Planejamento Estratégico - Comercial` **É** a raiz que o brief descreve. Capítulos 2.1, 5.1, 8 do brief sobre montar Drive: resolvidos antes de começar.

2. **"Claude gera pandas livre" é a arquitetura errada:** Gustavo tem ~20-30 perguntas recorrentes, vocabulário fechado (Verde/Vermelha/Preta/MC/família), e precisa de determinismo (números errados = decisão errada). LLM gerando query livre é caro, lento, inconsistente entre execuções e difícil de testar. Padrão melhor: biblioteca de funções canônicas + roteador.

3. **CLI separado é overhead injustificável:** o workflow real do Gustavo é Claude Code. Construir CLI standalone adiciona infra sem ganho na fase 1.

**Decidido em conjunto com Gustavo (3 perguntas via AskUserQuestion):**
- **Interface:** começar no Claude Code, evoluir pra app cloud
- **Roteamento:** funções canônicas + roteador (não Claude-gera-código)
- **Fonte:** cubos OLAP (não relê enriquecidos a cada query)

Tudo registrado em `Sistema Operacional Comercial/08 Agente Analítico/00 - Visão Geral.md`.

## Estrutura entregue

```
MotorAnalitico/agente/
├── __init__.py
├── carregador.py          — parser dos *_data.js + cache de enriquecidos
├── periodos.py            — 8 períodos textuais ('ytd', 'mes_anterior', etc.)
└── analises/
    ├── vendas.py          — top_materiais, vendas_cliente
    ├── cotacoes.py        — listar, conversao, perdas_por_preco, cotacoes_aging, aging_resumo
    ├── estoque.py         — cobertura, excedente, materiais_parados
    ├── pedidos.py         — pedidos_semana, ajustes_pos_fechamento
    └── pricing.py         — pct_preta_vendedor, preco_para_win_rate
```

12 funções canônicas. Lista completa com assinaturas em `Sistema Operacional Comercial/08 Agente Analítico/01 - Funções Canônicas.md`.

## Perguntas reais respondidas durante a sessão (validação)

### Rodada 1 — sanidade da fundação

| # | Pergunta | Função usada | Resultado |
|---|---|---|---|
| 1 | Estoque 1045 R L 57,15mm + tem OC? | `estoque.cobertura()` | 28.489 kg, 3,3 meses. **OC: lacuna (sem fonte)** |
| 2 | Família mais vendida em kg Abril/2026 | `vendas.top_materiais()` | 4140 R L 101-203mm = 246t |
| 3 | Vendas WEG em 2026 | `vendas.vendas_cliente('WEG')` | R$ 3,42MM em 5 razões (WEG-SC=71%) |

### Rodada 2 — drilldown

| # | Pergunta | Função usada | Resultado |
|---|---|---|---|
| 4 | Excedente 1045 R F 304,20mm | `estoque.excedente()` | **122 meses de cobertura excedente** — 28t parados |
| 5 | Aço + faixa que mais perde por preço em Abril/2026 | `cotacoes.perdas_por_preco()` | 4140 12-101mm = R$ 1,40MM em 302 cotações |
| 6 | Pior vendedor em conversão | `cotacoes.conversao(dim='vendedor')` | **Bug detectado e corrigido** (ver abaixo) |

### Rodada 3 — drilldown detalhado

| # | Pergunta | Função usada | Resultado |
|---|---|---|---|
| 7 | Cotações perdidas do Denilson | `cotacoes.listar(status='Perdeu', vendedor='Denilson')` | 24/25 das maiores = **Orçamento Prévio** |
| 8 | Pendentes >R$ 100k | `cotacoes.listar(status='Pendente', valor_min=100_000)` | 44 cotações / R$ 9,45MM, **4 em Preta** |

### Rodada 4 — pricing analytics

| # | Pergunta | Função usada | Resultado |
|---|---|---|---|
| 9 | PU pra fechar 75% das cotações 4140 102-230mm | `pricing.preco_para_win_rate()` | **Não viável só com preço** — teto observado 57% |

## Bugs e descobertas críticas durante a sessão

### Bug — `valor_orc_previo` do cubo_main está zerado

Descoberto auditando Denilson, que aparecia com 5,7% de conversão YTD (impossivelmente baixo). Cubo de Denilson:

| Campo | Valor |
|---|---|
| `valor_ganhou` | R$ 2,50MM |
| `valor_perdeu` | **R$ 41,53MM (inclui orçamento prévio!)** |
| `valor_orc_previo` (cubo) | **R$ 0,00 (zerado!)** |
| `valor_pendente` | R$ 3,49MM |

No enriquecido linha-a-linha:
- Orçamento Prévio: 2.517 cotações = R$ 37,29MM (67% do volume dele)
- Ganhou: 742 = R$ 2,50MM
- Perdeu Preço: 390 = R$ 1,87MM

A métrica `valor_orc_previo` no `cubo_main` nunca é populada — orçamento prévio fica embutido em `valor_perdeu`. **Pra extrair, filtrar `bucket_status == 'Orçamento'` e somar `valor_total`.**

**Função `cotacoes.conversao()` refatorada pra usar `bucket_status` em vez da métrica zerada.** Impacto:
- Conversão **global YTD 2026: 24% (bruto, CLAUDE.md) → 40,2% (líquido, correto)**
- Conversão **global Abril/2026: 20% → 30,6%**
- Denilson: 5,7% → **37,1%** (próximo da média AFS)

Documentado em `02 - Convenções e Caveats.md` como caveat persistente.

**Implicação:** o painel HTML de cotações pode estar mostrando o número bruto também. Vale auditar (próxima sessão).

### Descoberta — PU no enriquecido mistura unidades

Pergunta de pricing analytics revelou que a coluna `pu` em `CotacoesEncerradas_enriquecido.xlsx` é `valor_total / qtd`. Quando qtd é em kg, vira R$/kg. Quando qtd=1 (peça única), vira R$/peça. Resultado: PU médio R$ 323/"kg", máximo R$ 25.300/"kg" — absurdo pra liga base.

**Regra canônica adotada no agente:** sempre calcular `pu_kg = valor_total / kg`. Nunca confiar em `pu` direto.

Documentado no caveat 2.

### Descoberta — Engenheirados invisíveis em filtros físicos

Cotações de produto engenheirado ("Eixo usinado conf. desenho 1234") têm `liga`, `perfil`, `acabamento`, `medida_1` em **branco/NaN**. A info está só na descrição livre do `material`.

**Medido no recorte da pergunta 9 (4140 102-230mm):**
- Catalogados (incluídos): 2.948 cotações, R$ 14,77MM
- Engenheirados com "4140" na descrição (excluídos silenciosamente): **39 cotações, R$ 2,78MM (~19%)**

Engenheirados costumam ter alto valor unitário (R$ 90k-450k cada) — não é resíduo. E coluna `kg` neles vira número de peças (1, 3...) — não peso real. Logo **não dá pra calcular R$/kg em engenheirados** com os dados atuais.

**Próximo:** ajustar funções pra:
1. Parâmetro `tipo_item='catalogado'|'engenheirado'|'ambos'` em `cotacoes.listar()`
2. Reportar engenheirados separadamente em `pricing.preco_para_win_rate()`
3. Match em `material` (não só `liga`) quando incluir engenheirados

Documentado no caveat 1 + memória do Claude (`memory/engenheirados_vs_catalogados.md`).

## Achados de negócio surgidos durante a validação

### Win rate AFS — duas leituras

- **Bruto YTD 2026 (inclui orçamento prévio):** 24,2% (número do CLAUDE.md, painéis HTML)
- **Líquido YTD 2026 (exclui orçamento prévio):** **40,2%** ← útil pra decisão

Pra decisão comercial real ("onde dá pra atuar"), líquido é o número correto.

### Denilson — perfil de carteira, não problema de conversão

67% do volume dele é orçamento prévio (R$ 37MM de R$ 44MM cotados em 2026). Clientes dominantes: ANDRITZ, ANDRITZ SCHULER, JUMBO, MUNIZ, VALLOUREC, TRIENG — perfil engenharia/projetos grandes que pedem cotação só pra estimar custo.

**Conversão real corrigida: 37,1%** — próximo da média AFS. **Não é problema dele**, é perfil de carteira. Possível ação: revisar política de aceitação de "orçamento prévio" pra otimizar tempo do vendedor.

### Estoque parado emblemático — 1045 R F 304,80mm

28t em estoque com saída média de 220 kg/mês → **128,2 meses de cobertura**, **122 meses excedente**. Fornecedor Metals (nacional), lead time 5 meses. Candidato a liquidação imediata ou conversão pra bitola adjacente.

### Pricing curve 4140 102-230mm — teto estrutural

Win rate satura em ~57% nesse recorte. **PU médio das GANHAS (R$ 12,05/kg) é MAIOR que das PERDIDAS (R$ 10,93/kg)** — preço não é o driver dominante de conversão. Cotações em PU baixíssimo (R$ 9-10) têm win rate de só 28-35% (provável amostra problemática). Pra subir win rate de 57% pra 75% não basta baixar preço — precisa atacar perdas não-preço (prazo, estoque, certificado, relação).

### Pendentes >R$ 100k da semana — 4 em Preta

R$ 768k de pipeline em Tabela Preta:
- REX (Thais) 4140 R 45mm, gap -3,5%
- ADDN (Açotec-SCA) 4340 R 665mm + 590mm, gap -3,8% e -4,1%
- YTK (Thais) 4140 R 31,75mm, gap -6,7%
- **PREC-TECH (Denilson) 4340 R 30mm, gap -25,1%** ⚠ caso extremo

Cliente MILLENIUM (Denilson) concentra R$ 1,15MM em cotações fresquinhas (13/05) — conta ativa, follow.

## Lacunas reconhecidas pra próxima fase

1. **Sem fonte de OC** (Ordem de Compra) — não tem `01_Brutos/OrdensCompra/`. Limita análise de ruptura de estoque. Gustavo precisa decidir como resolver.
2. **Engenheirados sem peso unitário** — limita análise de R$/kg. Pedir ao Softcomp coluna `kg_unitario` nas exportações.
3. **Granularidade semanal limitada** — cubos vão até mês. Pra "última semana" usar `pedidos_data.cubo_dia` ou ler enriquecido (mais lento).
4. **Bug do `valor_orc_previo`** — afeta também painéis HTML que usam mesma métrica. Auditoria pendente nos painéis RAF e Cotações.
5. **Função `cotacoes.listar()` não suporta engenheirados** — ajuste pendente (parâmetro `tipo_item`).

## Próximos passos

- Pequenos ajustes do que ficou pendente (parâmetro `tipo_item` na `listar`, reporte de engenheirados na `preco_para_win_rate`)
- **Auditoria dos painéis HTML** pra ver se também usam `valor_orc_previo` zerado
- **Mais perguntas reais do Gustavo** pra expandir o conjunto de funções conforme utilidade comprovada (não pela lista teórica do brief)
- Eventualmente — Fase 2: app cloud + roteamento via Claude API.

## Documentação criada

- `Sistema Operacional Comercial/08 Agente Analítico/00 - Visão Geral.md`
- `Sistema Operacional Comercial/08 Agente Analítico/01 - Funções Canônicas.md`
- `Sistema Operacional Comercial/08 Agente Analítico/02 - Convenções e Caveats.md`
- `Logs/2026-05-14 — Agente Analítico Sacchelli (fundação).md` (este arquivo)
- Memória do Claude: `~/.claude/projects/.../memory/engenheirados_vs_catalogados.md`

## Arquivos modificados no repo (não-vault)

- `MotorAnalitico/agente/` — toda a pasta nova (12 funções + carregador + períodos)
