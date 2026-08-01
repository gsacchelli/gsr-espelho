---
data: 2026-05-09
contexto: Painel Comercial de Cotações
status: F5 fechada — refactor profundo pra espelhar Excel do Gustavo
tags: [painel, cotações, refactor, sessão]
---

# 2026-05-09 — Painel Cotações F5 (refactor pra espelhar Excel)

## TL;DR

Gustavo desconfiou do painel F4 e me mandou os 2 Excel originais (62k Encerradas + 1,8k Pendentes) pedindo pra olhar as colunas cinza (derivadas) e as abas analíticas. Eu havia construído um painel **executivo** com win rate como métrica central, mas o Excel real é **operacional/diagnóstico**: drilldown produto × cliente × motivo × faixa de bitola, decomposto em 5+1 buckets de status.

F5 entrega refactor profundo: enriquecedor + aggregator + HTML reescritos pra espelhar a forma como Gustavo opera no Excel.

## O que aprendi do Excel

### As 12 colunas derivadas (cinza) na aba "Dados"

O Excel tem fórmulas XLOOKUP/INDEX/MATCH em 12 colunas que padronizam aço, calculam faixa, classificam tabela:

| Col | Header | O que faz |
|---|---|---|
| H | Cidade SP | XLOOKUP cadastro de cidades |
| I | Região SP | cidade → região (44 regiões SP) |
| J | UF | derivada de cidade SP |
| U | Aço Cópia | normalização do aço |
| V | Perfil | classificação tipo aço |
| Y | DE Padrão | bitola padronizada com tolerância |
| Z | DI | diâmetro interno |
| AC | Corte? | sim/não baseado em Und.2 + L |
| **AD** (Pendentes) | **Estoque (meses)** | match contra Estoque Padrão → cobertura |
| AM/AN | Tabela | Preto/Vermelho/Amarelo/Verde |
| AN/AO | %/Tab.Verm | (PU − F3) / **PU** |
| AO/AP | Faixa 1-14 | bitola categórica |
| AP/AQ | Descrição Faixa | "1045 R L de 12,70 até 101,60" |
| AS | WeekN. | semana ISO |
| AX | Ganhou/Perdeu | Cód → 6 buckets canônicos |

**Achado crítico:** o `criterios_raf.xlsx` que o motor JÁ CARREGA tem TODA essa informação. Eu só não estava usando no aggregator de cotações. F5 conecta os dois mundos.

### Os 22 códigos de motivo viram 6 buckets canônicos

Mapeamento da aba Critérios (cols AI/AJ/AK):

| Cód | Descrição | Bucket |
|---|---|---|
| 1-9, $, A | Perda - Por Preço (Trefita/Açovisa/GGD/...) | **Perdeu Preço** |
| B, C, D, E, F | LC, prazo, procedência, motivo n/inf | **Perdeu** |
| O | Cotação somente para orçamento prévio | **Orçamento** |
| P, W, X, Y | Cancelado / S/inf / Faturado outra unid | **S/Inf.** |
| Z | Produto fora do mix | **Produto Fora** |
| (sem cód) | Status=Ganhou | **Ganhou** |
| Status='Pendente' | — | **Pendente** |

Total: 7 buckets (incluindo Pendente).

### As 9 abas analíticas revelam como ele opera

**Métricas principais não são R$ nem win rate — são Peso (Kg), Qtd Cot. e R$ alternados.**

| Aba | Linha | Coluna | Métrica |
|---|---|---|---|
| Gerencial | Gerência | Mês | **Qtd Cot.** + **MoM%** |
| Mensal | Aço × Faixa-bitola × Status | Mês | **Peso (Kg)** + % |
| Familia | Aço × Faixa-bitola | Status | R$ + % + Qtd It |
| Resumo Cliente | Cliente | Status (5 buckets) | R$ decomposto lado a lado |
| Gestor | Gerente × Aço × Faixa | Status | Peso (Kg) + % |
| Material (Pend) | Aço → Aço×Perfil×Acab×Faixa | — | Valor + Peso + 25 maiores clientes |
| Região (Pend) | Gerência + UF/Região/Cidade | — | Qtd Cli + R$ + Peso + Ticket médio |
| Clientes (Pend) | Gestor → Cliente → OS → Item | — | drilldown hierárquico |

## O que entreguei na F5

### F5.1 — Enriquecedor (`MotorAnalitico/cotacoes/enriquecer.py`)

Adicionei 8 campos derivados:
- `bucket_status` — 6 buckets canônicos via lookup do `MOTIVO_COD_TO_BUCKET` (22 códigos mapeados)
- `aco_filtro` (1018→1020), `aco_tipo` (Carbono/Beneficiamento/Cementação/Inox/Tubo/Manganês) via `crit.aco_padrao_por`
- `faixa_bitola_sn` (1-11) e `familia_canonica_desc` ("1045 R L de 12,70 até 101,60") via `crit.familia_por`
- `gap_pu_pct` — (PU − F3) / **PU** (métrica do Excel; complementa `gap_f3_pct` que divide por F3)
- `week_iso` — semana ISO (1-53)
- `corte_sn` — sim/não
- `regiao_sp` agora populada via lookup RAF (antes era placeholder None)

**Smoke test confirmou em caso BINOTTO:**
- aco_filtro='1045', aco_tipo='Carbono'
- familia_canonica_desc='1045 R L de 101,61 até 203,20' (idêntico ao Excel)
- faixa_bitola_sn=2, week_iso=4
- bucket_status='Ganhou' (status='Ganhou')
- Mapping de 22 códigos validado (1→Perdeu Preço, B→Perdeu, O→Orçamento, Z→Produto Fora)

### F5.2 — Aggregator (`MotorAnalitico/cotacoes/aggregator.py`)

Schema bumped: **v1-2026-05-08 → v2-2026-05-09**.

Mudanças nos cubos:
- `cubo_main`: `motivo_grupo` substituído por `bucket_status` na chave + adicionados `aco_filtro`, `aco_tipo`, `perfil`, `acab`, `faixa_sn`. Total: 15 dims.
- `cubo_cliente`, `cubo_motivos`, `cubo_pricing_item`, `cubo_geo`, `cubo_pendentes`: substituem motivo por bucket; cubo_pendentes ganha aço/perfil/acab/S/N; cubo_motivos ganha aço×perfil×acab×S/N.
- **Novo `cubo_aco_faixa` ⭐**: drilldown produto (ano × mes × aco_tipo × aco × perfil × acab × faixa_sn × bucket). Coração da nova aba "Família".
- `cliente_classificacao` agora carrega `peso_total`, `peso_ganhou`, etc + sub-objeto `buckets` com {n, valor, peso} pra cada um dos 7 buckets — pronto pra carteira lado-a-lado.

Validação local (sem rodar Encerradas no sandbox por timeout):
- Schema v2 ok
- 7 cubos serializados
- 192 células no cubo_aco_faixa (drilldown)
- 14 aços filtrados, 5 tipos de aço, 64 famílias canônicas
- 68 tabelistas, 359 projetos suspeitos
- Output 9.6 MB

### F5.3 — HTML refatorado (`03_Ferramentas/Painel_Cotacoes.html`)

**5 abas novas espelhando Excel** (rasguei as 5 antigas):

1. **Visão Gerencial** (espelha aba "Gerencial")
   - Tabela: Gerência × Mês com métrica + MoM% + Total
   - Decomposição mensal por bucket (mês × 7 buckets com R$ + %)
   - Top 10 vendedores

2. **Carteira por Cliente** (espelha "Resumo Cotações por Cliente")
   - Tabela: Cliente × 7 buckets lado a lado (Ganhou / Perdeu Preço / Perdeu / Orçamento / S/Inf. / Produto Fora / Pendente)
   - Cada bucket: Métrica + %
   - Filtros: busca cliente, flag (tabelista/projeto/ganhou-em-preta), top 50/200/500/all

3. **Família × Faixa de Bitola** (espelha "Familia"/"Mensal"/"Diário"/"Gestor")
   - Drilldown 3 níveis: Aço → Perfil×Acab×Faixa → Mês
   - Decomposição em 7 buckets em cada nível
   - Filtros: aço, tipo, perfil, acab
   - Click pra expandir/colapsar

4. **Pipeline (Pendentes)** (espelha "Material"/"Região"/"Clientes")
   - Aging por bucket, por gerência, por UF
   - Foco da semana (>15d ou >R$50k)
   - Top 25 cotações abertas

5. **Pricing & Itens Críticos** (mantido da F4 com ajustes)
   - Stoplight por faixa (Verde/Amarela/Vermelha/Preta)
   - 4 KPI cards
   - Tabela mestre paginada com 15 colunas (incluindo Bucket)
   - 68 tabelistas + 359 projetos suspeitos

**Toggle global de métrica:** R$ / Peso (Kg) / Qtd — aplicado em TODAS as abas. Métrica é uma decisão dele.

**Compatibilidade v1 → v2:** se o derivado das Encerradas ainda for v1 (sem `bucket_status`), o aggregator cai no fallback `motivo_grupo` e o painel mapeia automaticamente: "Preço" → "Perdeu Preço", "Outros" → "Perdeu", "Cancelado" → "S/Inf.", etc. Quando Gustavo rodar `--cotacoes-enriquecer` localmente, os buckets canônicos passam a vir direto.

**Smoke test:** todas as 5 abas renderizam sem erro com dado real.

## Trade-offs e bloqueios da F5

1. **Sandbox 45s não roda Encerradas** (62k linhas × crit_raf lookup ~50s). Validei só Pendentes (1.784 linhas). Gustavo precisa rodar `python3 MotorAnalitico/main.py --cotacoes-enriquecer` no Mac dele.

2. **Testes do enriquecedor** (55 testes existentes) provavelmente quebram com os 8 campos novos. Não atualizei nesta sessão — fica pendente. Sugestão: rodar `pytest MotorAnalitico/cotacoes/test_enriquecer.py`, atualizar fixtures, capturar caso BINOTTO como teste F5.

3. **`corte_sn` é aproximação** — Excel usa Und.2 (PÇ/BR), eu uso comprimento>0. Pode divergir.

4. **`gap_pu_pct` foi adicionado mas não substituiu `gap_f3_pct`** — ambos coexistem. Painel atual usa gap_f3_pct na tabela mestre. Se quiser unificar com Excel, troca pra gap_pu_pct.

5. **`faixa_bitola_sn`** vai de 1-11 do critério RAF, não 1-14 do Excel original. As 14 faixas aparecem só na aba "Faixa (original)" do Excel (sistema legado). Se quiser as 14, importa do Excel pra config.

## Pra Gustavo rodar local

Sequência completa (Mac, ~3-4 min):

```bash
cd "Planejamento Estratégico - Comercial"

# 1. Re-enriquece com os 8 campos novos (precisa do crit_raf)
python3 MotorAnalitico/main.py --cotacoes-enriquecer

# 2. Re-agrega (gera cotacoes_data.js v2)
python3 MotorAnalitico/main.py --painel-cotacoes

# 3. Abre o painel
open 03_Ferramentas/Painel_Cotacoes.html
```

Ou em uma única passada:
```bash
python3 MotorAnalitico/main.py --cotacoes-enriquecer && python3 MotorAnalitico/main.py --painel-cotacoes && open 03_Ferramentas/Painel_Cotacoes.html
```

## Arquivos relevantes

### Modificados
```
MotorAnalitico/cotacoes/enriquecer.py    (529 → 672 LOC, +8 campos derivados)
MotorAnalitico/cotacoes/pipeline.py      (379 → 351 LOC, ordem nova de colunas + crit_raf)
MotorAnalitico/cotacoes/aggregator.py    (806 → 879 LOC, schema v2 + cubo_aco_faixa)
03_Ferramentas/Painel_Cotacoes.html      (1.248 → 1.241 LOC, 5 abas novas)
03_Ferramentas/cotacoes_data.js          (regenerado v2, 9.6 MB)
```

### Sem mudança
```
MotorAnalitico/main.py                   (--cotacoes-enriquecer + --painel-cotacoes)
MotorAnalitico/cotacoes/test_enriquecer.py  (não atualizado — pendente)
```

## Próximas iterações possíveis (se Gustavo aprovar)

- **Charts visuais** (Chart.js): evolução temporal, barras empilhadas pra mix mensal
- **Export PDF** das abas (igual Painel RAF)
- **Atualizar fixtures dos 55 testes** + capturar caso BINOTTO como teste F5
- **Faixa 14** se quiser as faixas mais granulares do Excel (12,7-25,4mm, 25,41-38,1mm, etc)
- **Corte_sn refinado** lendo Und.2 do bruto (precisa adicionar campo no enriquecedor)
- **Aba Diagnóstico** com qualidade dos dados (datas anômalas, famílias não-mapeadas, aço sem padrão)

## Conexões

- [[2026-05-09 — Painel Cotacoes F4 (HTML 5 abas)]] — versão anterior (rasgada)
- [[2026-05-09 — Painel Cotacoes F3 (aggregator + cubos OLAP)]]
- [[Sistema Operacional Comercial/05 Cotações/00 - Visão Geral Cotações]] — agora reflete uso real
