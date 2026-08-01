---
data: 2026-05-09
contexto: Painel Comercial de Cotações
status: F1+F2+F3 fechadas, F4 (HTML) pendente
tags: [painel, cotações, motor-analítico, aggregator, cubos-olap, sessão]
---

# 2026-05-09 — Painel Cotações F3 (aggregator + cubos OLAP)

## TL;DR

F3 entregue: `MotorAnalitico/cotacoes/aggregator.py` (~800 LOC) espelhando o padrão do `raf/painel_aggregator.py`. 6 cubos OLAP pré-computados, lista granular de itens críticos, auto-flag de tabelista/projeto, cross-check com RAF via `pedido_id` validado end-to-end. Comando `python3 MotorAnalitico/main.py --painel-cotacoes` gera `03_Ferramentas/cotacoes_data.js` (`window.CD`, ~9 MB sem cross-check). Schema versionado `v1-2026-05-08`.

Achado importante: **win rate por valor real é 24,23%, não 12,1% como o log do dia 8 dizia**. Re-agregação direta sobre Encerradas: R$ 104,3 MM ganhos / R$ 430,5 MM cotados. Os números do log eram inconsistentes — ficou esclarecido nesta sessão.

## Arquitetura entregue

### 6 cubos OLAP

| Cubo | Granularidade | Uso na UI (F4) |
|---|---|---|
| `cubo_main` | ano × mes × unidade × gerência × vendedor × família × status × motivo × tipo_item × faixa × considerar | KPI bar geral, Win Rate por dimensão |
| `cubo_cliente` | ano × cliente × gerência × vendedor × status × motivo × faixa | Top clientes, classificação tabelista |
| `cubo_pendentes` | aging_bucket × unidade × vendedor × cliente × família × faixa | Aba 1 Pipeline (apenas Pendentes) |
| `cubo_motivos` | ano × motivo × concorrente × família × região × vendedor | Aba 3 Análise de Perdas (apenas Encerradas) |
| `cubo_pricing_item` | ano × mes × faixa × família × status × tipo_item | Stoplight + heatmap pricing (apenas catalogados sem anomalia) |
| `cubo_geo` | ano × região × UF × motivo × concorrente | Aba 5 Geografia/concorrência regional |

### Métricas comuns (todos os cubos)

`n`, `valor_total`, `qtd`, `kg`, `pu_pond_num/den`, `gap_f3_pct_pond_num/den`, `n_ganhou`/`valor_ganhou`, `n_perdeu`/`valor_perdeu`, `n_pendente`/`valor_pendente`, `n_orc_previo`/`valor_orc_previo`.

JS divide num/den nos campos ponderados pra obter PU médio dimensional e gap médio % vs F3 — padrão herdado dos campos `prazo_pond_*` do RAF.

### Itens críticos (top 5.000)

Lista granular incluindo:
- **Preta** (faixa < Vermelha em catalogados sem anomalia)
- **Ganhou-em-Preta** (caso Binotto — venda fechou abaixo do piso)
- **Projetos suspeitos** (Pendentes >R$50k+>30d ou Encerradas Orç.prévio >R$100k+ciclo<15d)

Cada item carrega `flag_ganhou_preta`, `flag_projeto_suspeito`, `flag_bloqueio` (lê do mesmo `config/bloqueios_pricing.yaml` do RAF), `perda_estimada` (max(0, F3-PU)*qtd), e quando cross-check ativo: `raf_pu_efetivo`, `raf_faixa_efetiva`, `raf_valor_liq`. Ordenação por perda estimada DESC.

### Auto-flag de perfis

Critérios decididos com base no vault (Cliente-Tabelista) e PRD:

**Perfil A — Tabelista** (industrializar atendimento):
- >70% das cotações com motivo Orç. prévio
- <10% conversão por item
- ≥20 cotações distintas (chave_cotacao)

**68 clientes flagados.** Top 5 por valor cotado:

| Cliente | Cotações | %Orç.prévio | %Conv | R$ cotado |
|---|---|---|---|---|
| THERMON | 140 | 71% | 1% | R$ 4,8 MM |
| ANDRITZ | 32 | 88% | 0% | R$ 3,5 MM |
| USIMATRIX | 468 | 86% | 8% | R$ 1,9 MM |
| IBRATEC | 115 | 83% | 8% | R$ 1,7 MM |
| CHICO TORNEARIA | 129 | 76% | 7% | R$ 0,4 MM |

**Perfil B — Projeto** (cliente industrial com cotação grande e demorada):
- valor_total > R$ 200k
- idade_max > 30d

**359 clientes flagados.** Cobertura mais ampla — vai precisar refinar o threshold com Gustavo.

### Cross-check com RAF (opcional)

Ativa quando `02_Derivados/RAF/RAF_enriquecido_*.xlsx` existem. Indexa por `(ABCOII_NUM, ABCNNF_ITE)` e cruza com `pedido_id` da cotação (split em `os.item`). Output: tabela `cross_check_raf` com:
- `pu_orcado` vs `pu_efetivo`
- `faixa_orcada` vs `faixa_efetiva`
- `migracao` ∈ {subiu, desceu, manteve}
- `valor_orcado` vs `valor_efetivo`

**Validação manual ok**: cotação BINOTTO `MATRIZ_537267` itens 1-7 → RAF OS=334349 itens 1-7 com mesmo PU=7,50 e mesma faixa Preta. Estrutura de chaves está correta.

**Nota operacional:** sandbox aqui é ~10× mais lento que o Mac do Gustavo. Cross-check completo (4 RAFs, 230MB total) excede 45s em sandbox; rodar localmente sempre. Localmente, é esperado ~3 min total.

## Achados quantitativos

### Win rate corrigido

Recálculo direto em Encerradas:

```
n=62.311 (G=23.048 P=39.263)
R$ total cotado: 430.545.342
R$ ganho:        104.312.980  
R$ perdido:      326.232.363
Win rate valor:  24,23%
```

**Log do dia 8 dizia 12,1% / R$ 861 MM cotados — erro.** R$ 861 MM era ~2× o real (provavelmente ganho+perdido foi confundido com cotado). Os outros números do log batem (4.850 Preta, 23.048 Ganhou). 

→ Atualizar `Sistema Operacional Comercial/05 Cotações/05 - Win Rate e Métricas` se houver fórmula documentada lá.

### Tabela Preta

- **4.850 itens / R$ 50,4 MM** em Encerradas (bate com log do dia 8)
- Agregado total (incluindo Pendentes em Preta): 5.017 itens
- `cubo_main` tem chave 9 = `faixa`, então filtrar `Preta` é trivial

### Pipeline aberto (status='Pendente')

- 1.774 itens / R$ 15,5 MM (bate com log)
- 1.763 em 0-7d / 5 em 31-60d / 6 em 60+ — **só 11 cotações antigas pra revisar** (foco da semana)

### Top concorrentes (cubo_motivos)

| Concorrente | Itens cotados perdidos |
|---|---|
| Trefita/Torres | 2.551 |
| Açovisa | 1.060 |
| GGD | 710 |
| Açofera | 438 |
| Diferro | 403 |
| Açotubo | 333 |

**Bate 100% com log e vault.** Confirma o regex de extração de concorrente está consistente.

## Decisões da sessão

| Decisão | O que ficou |
|---|---|
| Schema versionado | `v1-2026-05-08` (igual à F1+F2). Não bumpei pq F3 só agrega — não muda enriquecidos. |
| Considerar=True regra | catalogado AND not data_anomalia. Engenheirados e datas furadas saem das análises de pricing (mas continuam em cubo_main e cubo_cliente, contam pra win rate). |
| Cross-check é opcional | Default True, pode ser desativado via `cross_check_raf=False`. Útil pra rodar rápido em iteração. |
| Threshold tabelista | >70% orç.prévio + <10% conv + ≥20 cotações. Pode ajustar quando Gustavo trouxer feedback dos 68 flagados. |
| Threshold projeto | >R$200k + >30d. Sai 359, é alto demais — refinar. |
| Itens críticos cap | 5.000 (igual RAF). Lista total fica em `meta.itens_criticos_total`. |
| Output | `03_Ferramentas/cotacoes_data.js` (window.CD) — padrão estabelecido pelo Painel RAF. |
| Faixa N/D | 305 itens em Encerradas têm faixa null (provavelmente F1/F2/F3 ausentes). Mantive como 'N/D' — não vira Preta nem Vermelha. |

## Arquitetura de chaves do cubo_main

Índice `k[9] = faixa` permite slice trivial `Preta` no JS:

```js
const PRETA_IDX = CD.cubo_main.schema.indexOf('faixa');  // = 9
const preta_rows = CD.cubo_main.rows.filter(r => r[PRETA_IDX] === 'Preta');
```

`k[10] = considerar` permite filtro pra excluir engenheirados das análises de pricing sem dobrar contagem.

## Performance

- Sem cross-check: **26,4s** (62k+1,8k linhas em 7 dimensões × 6 cubos)
- Com cross-check (4 RAFs ~230MB): estimativa ~3 min localmente
- JSON resultante: ~9 MB sem cross-check, ~12 MB com

## Pontos de retomada

### Como retomar (F4)
1. Ler este log + `06_Docs/PRD_Painel_Cotacoes.md` (seção 6 — abas)
2. Confirmar `cotacoes_data.js` foi gerado: `python3 MotorAnalitico/main.py --painel-cotacoes`
3. Criar `03_Ferramentas/Painel_Cotacoes.html` espelhando `Painel_Comercial_RAF.html`:
   - `<script src="./cotacoes_data.js">` no head
   - Schema check no boot via `console.warn` se `CD.schema_version !== 'v1-2026-05-08'`
   - Wrapper `_safeRender` por bloco (banner inline em erro)
   - Botão ❓ Glossário no header
   - 5 abas: Pipeline / Win Rate / Análise de Perdas / Item×Estoque×Vermelha ⭐ / Tabelistas & Projetos
   - Aba 4 é o coração do pedido — filtros cascateados + tabela mestre item-a-item paginada com 100 linhas + exportável CSV

### Coisas a validar com Gustavo
- Threshold do auto-flag projeto (359 saindo é demais — talvez subir pra >R$ 500k ou >R$ 1MM, ou exigir cliente industrial)
- 68 tabelistas flagados — listar pra ele cruzar mentalmente com o que vê no dia-a-dia
- Win rate corrigido — pedir confirmação que 24,23% bate com sensação dele (vs 12,1% que estava sendo usado)

### Pendentes técnicos
- Render Painel HTML (F4) — sem decisões pendentes, só execução
- Suite de testes do aggregator: criar `MotorAnalitico/cotacoes/test_aggregator.py` com fixtures sintéticas
- Documentação técnica no sub-vault: atualizar `Sistema Operacional Comercial/05 Cotações/00 - Visão Geral Cotações`

## Conexões

- [[2026-05-08 — Painel Cotacoes F1+F2 (esqueleto motor + match estoque)]]
- [[Sistema Operacional Comercial/05 Cotações/05 - Win Rate e Métricas]] — atualizar formula com 24,23% confirmado
- [[Sistema Operacional Comercial/05 Cotações/04 - Cliente-Tabelista (flag proposta)]] — incluir 68 clientes auto-flagados
- [[Sistema Operacional Comercial/01 Sistema de Dados/03 - Ferramentas Analíticas - Inventário]] — bumpar Painel de Cotações pra "F3 (motor) entregue, F4 (HTML) pendente"
- [[2026-04-30 — Plano Pricing Discipline Tabela Preta (Sacchelli)]] — caso Binotto valida processo de cobertura

## Arquivos relevantes

### Código
```
MotorAnalitico/cotacoes/aggregator.py    (~800 LOC, novo)
MotorAnalitico/main.py                   (run_painel_cotacoes adicionado)
```

### Outputs
```
03_Ferramentas/cotacoes_data.js          (gitignored, ~9 MB)
```

### Inputs (já existiam)
```
02_Derivados/Cotacoes/CotacoesEncerradas_enriquecido.xlsx   (62.311 itens)
02_Derivados/Cotacoes/CotacoesPendentes_enriquecido.xlsx    (1.784 itens)
02_Derivados/RAF/RAF_enriquecido_2023..2026.xlsx            (~230 MB total — cross-check)
MotorAnalitico/config/bloqueios_pricing.yaml                (reuso do RAF)
```
