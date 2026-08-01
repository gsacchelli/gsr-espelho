---
data: 2026-05-11
tipo: log
status: vigente
---
# 2026-05-11 — F12+F13 — Dashboard reset + sistema de overrides

> Sessão de tarde. Continuação da F10+F11 (manhã). Foco: simplificação radical pós-feedback ("painel muito confuso, falta o básico").

## Contexto da sessão

Após entregar 6 abas MECE big4 de manhã (F11), o Gustavo deu feedback honesto: **"acho muita informação e nao temos o basico, uma analise e kpis basicos"**.

Decidi recuar e refazer o Dashboard do zero, focando no que ele realmente usa toda semana. As outras 5 abas ficaram intocadas como reservatório de análises sofisticadas pra quando precisar.

## Estado final do painel (10 fases nessa tarde)

| Fase | Entrega |
|---|---|
| **F12** | Dashboard novo (3 cards iguais + evolução + tabela por corte) |
| **F12.1** | Fixes pós-feedback (Faturamento→Pedidos, bug Encerradas zero, MoM tooltips, %Preta semáforo) |
| **F12.1b** | "Emitidas"→"Encerradas" + linha Conversão no modo Dia |
| **F12.1c** | Bloco Motivos das Cotações (donut + toggle por motivo) + Taxa Fechamento correta (Pedidos÷Encerradas, não ÷Ganhou) |
| **F12.2** | Engenharia de dados: helper unificado `_passaFiltroGlobal` em 6 agregadores |
| **F12.3** | Suavizar Taxa Fechamento + schema cotações bumpado pra **v2.3** (cubo_pendentes com gerencia+uf) |
| **F12.4** | Bloco crítico: KPI bar sticky escondido na Dashboard + fix Δ MoM em mês parcial + remover Métrica global redundante |
| **F12.5** | Saneamento: 1.086 linhas dead code removidas + UF global (4 abas refatoradas) + threshold conversão 50k→10k |
| **F12.6** | Gráfico Dia: detecção automática quando filtro gerência/vendedor/UF ativo → usa pedidos_top (cobertura 100% pro universo AFS) |
| **F12.7** | Header compactado em 1 linha (−50px acima da dobra) |
| **F13** | Sistema de overrides manuais (`cotacoes_overrides.yaml`) + correção TUP MATRIZ_547979_1 + cotações pendentes na tabela |

## Dashboard final — 4 blocos

### Filtros (1 linha compacta)
`Período abr/26 → abr/26 | [Mês][3M][YTD][Tudo] | Corte: Unidade/Gerente/Vendedor | Medida: R$/Peso | info`

### 3 cards principais (mesmo tamanho)
- **Cotações Pendentes** (azul): R$ aberto + n cotações + idade média + críticas (>30d) + ticket médio
- **Cotações Encerradas** (roxo): R$ período + WR% + Δ MoM/YoY/YTD
- **Pedidos Emitidos** (verde): R$ + n itens + peso + %Preta + Δ MoM/YoY/YTD

Mês parcial detectado automaticamente: badge "PARCIAL" + Δ MoM com mesma janela de dias úteis.

### Gráfico evolução (toggle Dia / Mês)
- 4 séries: Cotações Encerradas · Cotações Ganhou · Pedidos Emitidos · Taxa de Fechamento %
- Modo Dia: usa `pedidos_top` quando filtros gerência/vendedor/UF ativos (cobertura 100% pra AFS)
- Threshold dia 10k R$ (ou 100kg) pra evitar ruído

### Bloco Motivos das Cotações Encerradas
- Donut + toggle por motivo (Ganhou · Perdeu Preço · Perdeu · Orçamento · S/Inf · Produto Fora)
- Click no chip ativa/desativa
- Tabela ao lado com R$ · % · itens · total

### Tabela por corte (Unidade / Gerente / Vendedor)
Headers em 4 grupos:
- **Cot. Pendentes** (snapshot) — R$ · Peso · n
- **Cot. Encerradas** (período) — R$ · WR% · Δ MoM
- **Pedidos** (período) — R$ · Δ MoM · Δ YoY · %Preta R$
- **Taxa Fechamento** — Pedidos ÷ Encerradas (verde ≥30%, vermelho <15%)

Totais no rodapé + export CSV.

## Sistema de overrides (F13)

`MotorAnalitico/config/cotacoes_overrides.yaml` — trilha de auditoria pra correções manuais que sobrevivem a re-export do Softcomp.

### Estrutura
```yaml
overrides:
  - chave_cotacao: MATRIZ_547979_1
    data_aplicacao: 2026-05-11
    responsavel: Gustavo
    motivo: |
      Vendedor TUP digitou qtd em "T" quando era "KG".
      Erro inflou valor_total de R$ 13.881 para R$ 13.881.460 (1000x).
    overrides:
      unid_qtd: KG
      kg: 1697
      valor_total: 13881.46
```

### Aplicação
- `cotacoes/enriquecer.py` chama `aplicar_overrides(linha, chave)` antes das derivações
- Faixa atingida, gap %F3 etc são recalculados sobre valor corrigido
- Sobrevive a `--cotacoes-enriquecer` indefinidamente
- Pra adicionar: editar YAML + rodar `--cotacoes-enriquecer`

### Cotações corrigidas
- **MATRIZ_547979_1** (TUP, Estratégicos, 13/abr/26): kg/qtd em T → KG (fator 1000x)

## Bugs encontrados e resolvidos nessa sessão

| Bug | Causa | Fix |
|---|---|---|
| "Faturamento" no card KPI bar | label errado pra Pedidos | renomeado pra "Pedidos Emitidos YTD" |
| Card Encerradas zerado | `sx.mes_emissao` não existe no cubo (correto é `sx.mes`) | trocado nos agregadores |
| KPI bar sticky não filtrava | helper antigo só filtrava `ano`, não `gerencia`/`vendedor` | unificado helper |
| Δ MoM ↓85% artificial | comparava mai/26 (8d) com abr/26 (30d) | detecção mês parcial + comparativo mesma janela |
| Filtro Métrica global vs Medida local | duplicação confusa | Métrica global removida |
| Taxa Fechamento sumiu no dia 16/04 | threshold 50k escondia | reduzido pra 10k |
| Conversão saltando 0%–150% | divisor errado (Cot. Ganhou intraday) | trocado pra Cot. Encerradas (estável) + renomeado "Taxa de Fechamento" |
| Gráfico Dia com Pedidos > Cards Total | `cubo_dia` não tem `gerencia` no schema | detecção automática + uso de `pedidos_top` |
| Filtro Gerência: Odair-PIR zerando cards | era cache do navegador | hard reload + diagnóstico no boot |
| Card Pendentes não filtrava por gerência | `cubo_pendentes` sem `gerencia` | aggregator Python bumpado v2.3 com `gerencia + uf` |
| UF quebrado em 4 das 6 abas | 5 helpers de filtro inline | refatorado pra 1 helper único `_passaFiltroGlobal` |
| TUP MATRIZ_547979_1 com R$ 13,88M errado | erro digitação T vs KG | sistema de overrides + entrada manual |
| 26 funções órfãs (~1.086 linhas) | stubs F11.5 + helpers do antigo Dashboard | deletadas |

## Decisões arquiteturais relevantes

### Helper unificado `_passaFiltroGlobal(r, sx)`
```js
function _passaFiltroGlobal(r, sx) {
  if (ESTADO.ano && sx.ano !== undefined && String(r[sx.ano]) !== String(ESTADO.ano)) return false;
  if (ESTADO.unidade && sx.unidade !== undefined && r[sx.unidade] !== ESTADO.unidade) return false;
  if (ESTADO.gerencia && sx.gerencia !== undefined && r[sx.gerencia] !== ESTADO.gerencia) return false;
  if (ESTADO.vendedor && sx.vendedor !== undefined && r[sx.vendedor] !== ESTADO.vendedor) return false;
  if (ESTADO.uf && sx.uf !== undefined && r[sx.uf] !== ESTADO.uf) return false;
  return true;
}
```

**Princípio:** filtro só aplica se a dimensão existe no schema. Cubos sem `uf` (ex.: `cubo_pendentes`) passam transparente quando filtrar UF — evita zerar silenciosamente.

### Dashboard vs Outras abas
- **Dashboard** = entrada operacional, KPIs básicos, uso diário
- **Executive Summary, Funil, Performance, Carteira, Mix & Pricing, Análise Livre** = análises sofisticadas (intocadas, mas disponíveis)
- KPI bar sticky **escondido na Dashboard** (redundante com 3 cards grandes); aparece nas outras abas

### Threshold conversão diária
- R$ 10k pra valor (ou 100kg pra peso) — abaixo, linha Taxa de Fechamento omite ponto pra evitar ruído
- Cap automático em 150% (quando pedidos vêm de cotações de dias anteriores)

### Detecção de mês parcial
- `_dashMesParcial(ym)` retorna `{is_parcial, dia_atual, dias_total}`
- Se parcial e range = 1 mês: Δ MoM compara **mesma janela de dias**
- Card mostra badge "PARCIAL" e dia atual/dia total

## Métricas-chave finais

### Pedidos
- 2025: **R$ 273,6 MM** · 73.594 itens · 20.897 t
- 2026 YTD (jan-mai parcial): **R$ 85,2 MM** · 22.877 itens · 6.434 t

### Cotações (YTD 2026)
- Encerradas: R$ 430,5 MM cotado · WR 24,2%
- Pendentes (snapshot): R$ 15,4 MM · 1.763 cotações · idade média 8d

### Performance por gerência (abr/26)
- Felipe/Fuscão: cotação R$ 93,8M ↑13% · pedido R$ 13,6M ↑12% · Taxa 14,5%
- Odair-PIR: cotação R$ 9,1M ↓24% · pedido R$ 2,9M ↑38% · Taxa 31,9%
- Odair-SCA: cotação R$ 8,5M ↓9% · pedido R$ 2,7M ↑4% · Taxa 32%
- Fernando: cotação R$ 1,5M ↑1% · pedido R$ 906k ↑35% · Taxa 58,9%
- Fabiola: cotação R$ 3,9M ↓52% · pedido R$ 691k ↓41% · Taxa 17,9% (alerta duplo)
- Marketing: SDR, baixo volume

Interpretação: **mais cotação ≠ mais venda**. Fernando cota seletivamente e fecha 58,9% — vendedor de classe A. Fabiola perdeu volume E taxa — sinal de revisão.

## Comandos operacionais

```bash
# Rotina semanal (segunda 9h)
cd ~/Documents/Personal/00.\ Projetos\ -\ Claude/Planejamento\ Estratégico\ -\ Comercial
python3 MotorAnalitico/main.py --cotacoes-enriquecer    # diário (cotações pendentes substitui)
python3 MotorAnalitico/main.py --painel-cotacoes
python3 MotorAnalitico/main.py --pedidos-all            # semanal (~80s, 2025+2026)
```

## Backlog parqueado (opcional, sem urgência)

- Dividir gráfico evolução em 2 painéis (volume + taxa)
- Quebrar `bootControls` em 6 `_bootXxx` (manutenibilidade)
- Sistema de detecção de anomalia ±5σ (vendedor × cliente)
- Adicionar gerência + vendedor no `cubo_dia` do aggregator (cobertura 100% sem `pedidos_top`)
- Variance Bridge YoY na aba Executive (depende de comparar 2025 vs 2024 — não temos 2024)
- Cross-check RAF × Pedidos (4º estágio do funil "NF Faturada")

## Estado técnico final

- **Painel HTML**: 5.303 linhas (era 6.401 antes do saneamento — economia 17%)
- **Aggregator cotações**: schema v2.3-2026-05-09
- **Aggregator pedidos**: schema v3-2026-05-11 (multi-ano 2025+2026)
- **Smoke test**: passa
- **6 abas operacionais** (Dashboard core + 5 análises sofisticadas)

## Lições da sessão

1. **Over-engineer antes do básico funcionar = ruído**. F11 entregou 6 abas com Variance Bridge / Pocket Price Waterfall / HHI / Cohort, mas o Gustavo precisava de KPI básico por gerência primeiro. Tive que recuar.

2. **Schema do cubo é contrato implícito**. `cubo_dia` sem `gerencia` → filtro silenciosamente não atua → gráfico mostra valor 5x maior que cards. Solução: helper que verifica `sx[dim] !== undefined` antes de filtrar (transparente em vez de bug silencioso).

3. **Cache do navegador é primeira hipótese em qualquer bug visual**. Engenheiro de dados rodou aggregator em Node e retornou correto — sintoma era cache.

4. **Mês parcial sempre distorce MoM**. Em qualquer painel temporal com mês corrente, comparativo mensal precisa de janela equivalente OU badge "PARCIAL" visível.

5. **Taxa de Fechamento (Pedidos ÷ Cot. Encerradas) > Taxa de Conversão (Pedidos ÷ Cot. Ganhou)**. A primeira é estável e absorve duas eficiências (WR declarada + evaporação cot→ped) numa só. Padrão "Hit Rate × Win Rate" em B2B distribuição.

6. **Sistema de overrides em YAML salva fim de quartil**. Erro de vendedor (T vs KG, fator 1000x) contamina toda a base. YAML com auditoria sobrevive ao re-export semanal.
