---
data: 2026-06-06
tipo: log
status: vigente
tags: [data-lake, backup, backblaze-b2, rclone, infra, git, ssh, migracao, fase-4]
relacionado: 
---

# Data Lake — Fase 4 (Backup Backblaze B2) + migração do projeto pra ~/dev/afs-lake

## TL;DR

Sessão de infra, três frentes:

1. **Fase 4 do data lake entregue**: backup off-site de baixo custo via `rclone` → Backblaze B2. Scripts `backup_b2.sh` + `restore_b2.sh`, `.env.example`, doc `lake/metadata/backup.md`, targets `make backup`/`make restore`. Commitado e no GitHub.
2. **Validação completa pós-migração**: rodadas todas as suites — **1.049 testes verdes, 0 falhas** (877 JS do simulador + 172 Python do motor). A migração de pasta não quebrou nada.
3. **Setup de credencial Git**: a máquina não tinha chave SSH nenhuma. Gerada `ed25519`, registrada no GitHub, repo `data_lake_gsr` (estava vazio) recebeu o primeiro push com o histórico inteiro.

Descoberta de contexto: **o projeto migrou** de `…/00. Projetos - Claude/Planejamento Estratégico - Comercial/MotorAnalitico` para **`~/dev/afs-lake`** (repo git versionado, medallion bronze/silver/gold). O caminho antigo não existe mais.

## Contexto: a migração

O projeto agora é um repo git em `/Users/gustavosacchelli/dev/afs-lake`, remote `git@github.com:gsacchelli/data_lake_gsr.git` (privado). Estrutura: `MotorAnalitico/` (engine Python), `lake/` (Parquet+DuckDB), `01_Brutos/`, `02_Derivados/`, `03_Ferramentas/` (painéis HTML), `Makefile`, `CLAUDE.md`.

Roadmap do lake em fases (no histórico git):
- **Fase 0** — estrutura `lake/` + Makefile + deps ✅
- **Fase 1** — Parquet + DuckDB layer ✅
- **Fase 2** — Portal Streamlit (`MotorAnalitico/portal/`) ✅ **(esta sessão — ver Frente 4)**
- **Fase 3** — MCP Server pro Claude Desktop ✅ (+ 4 tools de vault GSR)
- **Fase 4** — Backup Backblaze B2 ✅ **(esta sessão)**

> Com a Fase 2 entregue, **o roadmap original do lake (Fases 0-4) está completo.**

> ⚠️ Impacto no dia-a-dia: o bookmark antigo do **Simulador de Precificação** está morto.
> Novo caminho: `file:///Users/gustavosacchelli/dev/afs-lake/03_Ferramentas/Analise_Precificacao_Sacchelli.html`
> A ferramenta migrou completa (HTML + `js/` + `config/`, tudo por caminho relativo) e está intacta.

## Frente 1: Fase 4 — Backup B2

### Decisões arquiteturais

- **Ferramenta: `rclone`** (não rsync puro). O README dizia "rsync lake/ → B2", mas rsync não fala com B2. rclone é o padrão de fato, nativo de B2, com sync incremental e suporte a versionamento.
- **Escopo de backup: `01_Brutos` + `lake`** (configurável via `BACKUP_PATHS` no `.env`). `01_Brutos` é a **fonte insubstituível** do Softcomp (única cópia). `lake` é regenerável via `make lake` mas caro de reconstruir. `views/metadata/exemplos` já estão no git, então protegidos independente do B2.
- **`rclone sync` SEM `--b2-hard-delete`** — de propósito: arquivos removidos na origem viram delete-markers e versões antigas ficam retidas pela lifecycle do B2. Proteção contra apagão acidental / ransomware.
- **Restore não sobrescreve in-place**: `restore_b2.sh` baixa pra `./restore_b2/` por padrão; confere e move manualmente.
- **Segredos via `.env`** (gitignorado). Scripts montam o remote rclone via env vars (`RCLONE_CONFIG_AFSB2_*`), sem config interativo nem segredo em disco fora do `.env`.

### Arquivos

| Arquivo | Papel |
|---|---|
| `scripts/backup_b2.sh` | Sync `01_Brutos` + `lake` → B2. `--dry-run`, saída colorida, exclui `__pycache__`/`.DS_Store`/`*.wal`/`*.tmp`. Guard-rails: pede `.env` se faltam credenciais, instrui `brew install rclone` se ausente. |
| `scripts/restore_b2.sh` | Restaura do B2 em `./restore_b2/` (ou pasta/destino custom). |
| `.env.example` | `B2_KEY_ID` / `B2_APP_KEY` / `B2_BUCKET` + `BACKUP_PATHS`. |
| `lake/metadata/backup.md` | Setup/uso/retenção/restore de emergência (versionado). |
| `Makefile` | `make backup` roda o script; novo `make restore`. |

Commit: `7564b59 feat: Fase 4 — Backup Backblaze B2 (rclone)`.

## Frente 2: validação de testes

Rodadas todas as suites pra confirmar que a migração de pasta não quebrou nada:

| Suite | Resultado |
|---|---|
| `motor_precificacao` (JS) | 570 ✓ |
| `gerador_proposta` (JS) | 149 ✓ |
| `schema_proposta` (JS) | 105 ✓ |
| `tipi_lookup` (JS) | 39 ✓ |
| `comparativo_identity` (JS) | 14 ✓ |
| `raf/test_enriquecer` (Py) | 117 ✓ |
| `cotacoes/test_enriquecer` (Py) | 55 ✓ |
| **Total** | **1.049 ✓ / 0 falhas** |

Limpeza: removidos 3 temporários versionados por engano (`config/_probe.tmp`, `config/_test_write.tmp`, `js/_teste.txt`). Commit `ac7bf85`.

## Frente 3: setup de credencial Git

- Máquina não tinha chave SSH nenhuma (`~/.ssh` só com `known_hosts`, agente vazio, sem `gh`).
- Gerada `ed25519` sem passphrase (`~/.ssh/id_ed25519`), carregada no agente, registrada em github.com/settings/ssh/new.
- Repo `data_lake_gsr` estava **vazio** no GitHub. Primeiro push criou a `main` remota com o histórico inteiro. `main` local agora rastreia `origin/main` — daqui pra frente é só `git push`.

## Frente 4: Fase 2 — Portal Streamlit

Construído `MotorAnalitico/portal/app.py` — camada visual SQL **read-only** sobre o gold DuckDB, espelhando vocabulário e cores canônicas dos painéis HTML. `make portal` já apontava pra cá; streamlit/plotly já estavam no `requirements.txt`.

**5 páginas:**
1. **Visão Geral** — KPIs do ano (Faturamento, MC Total %, %Preta, Itens) + evolução mensal (Faturamento × MC% com linha do Piso Operacional 24%) + donut mix por faixa.
2. **Vendas (RAF)** — DRE Gerencial, %Preta por gerência, scatter BCG (Faturamento × MC%, eixo log), top 30 clientes.
3. **Cotações** — Win Rate por ano (`vw_cotacoes_funil`) e por gerência, análise de perdas por motivo, top concorrentes.
4. **Pedidos** — Faturamento/Volume/Cold Orders, faturamento mensal, mix por faixa, Gap Cotação→Pedido por gerência.
5. **SQL Livre** — editor read-only (SELECT/WITH/DESCRIBE), schema das views, export CSV.

**Decisões:** conexão DuckDB read-only cacheada (`@st.cache_resource`) + cursor por query; queries cacheadas (TTL 10min); wrapper de erro por página (não derruba o portal); caminho do DB resolvido por `__file__` (independe do cwd). Faixas Verde/Amarela/Vermelha/Preta com cores fixas + Piso Operacional 24% como referência.

**Dados reais no gold (confirmados):** RAF 263.588 linhas, Pedidos 100.402, Cotações encerradas 271.697, `vw_kpi_mensal` 216 linhas, `vw_carteira_cliente` 4.032 clientes. Win Rate declarativo 2025=18,7% / 2026=21,4% (`vw_cotacoes_funil`).

**Validação:** 14/14 queries SQL rodam contra o gold; `AppTest` percorre as 5 páginas sem exceção e sem `st.error`. Corrigida API depreciada (`use_container_width` → `width="stretch"` em dataframe; `plotly_chart` mantém `use_container_width`).

Commit: `c947d4f feat: Fase 2 — Portal Streamlit sobre o gold DuckDB`.

## Frente 5: evolução do portal pós-uso (mesma sessão)

Após Gustavo abrir e navegar o portal, ajustes:

- **Dimensão Unidade no gold:** `vw_kpi_mensal` e `vw_carteira_cliente` ganharam coluna `unidade` (`TRIM(ABCEMPRED)`). 7 filiais: MATRIZ, PIRACICABA, SAO CARLOS, RIO PRETO, CAXIAS DO SUL, ANCHIETA, VILA PRUDENTE. **Filtro de Unidade** na sidebar, combinável com Gerência. (vw_kpi_mensal foi de 216 → 628 linhas.)
- **Vendedor:** RAF tem `ABCVEN_NOM` (gerência é `ABCGER_NOM`). Drill por vendedor é **por página** (grafia nativa da fonte), não filtro global — grafias divergem entre fontes e são ~48 vendedores. Leaderboard em Vendas + Win Rate por vendedor em Cotações.
- **Pesquisa de Estoque:** página com busca por material/medidas + filtros (Linha, cobertura ruptura<3m/normal/excesso>24m) + tabela + CSV.

**Decisões de arquitetura (portal vs HTML) — tomadas com Gustavo:**
- **Pesquisa de estoque → portal + HTML segue.** O portal vira a consulta interativa; o `--estoque` continua gerando `Estoque_Sacchelli.html` como **entregável** pros gestores (abrem offline, sem servidor).
- **Orçar itens (Softcomp vs DRE) = Simulador de Precificação → continua HTML.** Motor JS de ~2.800 linhas, 1.074 testes, shadow-mode fiscal, proposta A4 PDF, localStorage. Reescrever em Python arriscaria **paridade fiscal** (erro fiscal = cotação errada + autuação). Portal apenas linka/atalha; integração de dados lake→simulador fica para o futuro.

Commits: `c947d4f` (portal base), `d4caefe` (gerência+estoque), `c998d41` (vendedor+evolução+glossário), `64b8d75` (unidade+pesquisa estoque). Portal com **7 páginas**: Visão Geral · Vendas · Cotações · Pedidos · Pesquisa de Estoque · SQL Livre · Glossário.

## Próximos passos

### Pra ativar o backup de fato (quando quiser)
1. `brew install rclone`
2. Criar bucket privado no B2 (ex.: `afs-lake-backup`) com versionamento "Keep all versions" + Application Key dedicado (não o master key).
3. `cp .env.example .env` e preencher credenciais.
4. `make backup -n` (dry-run, confere o que sobe) → `make backup`.
5. **Considerar agendar** (cron/launchd) o `make backup` semanal — alinhado ao ciclo de atualização dos brutos.

### Roadmap do lake
- **Fases 0-4 completas.** Roadmap original fechado.
- Evoluções possíveis do portal (não-roadmap): mais views agregadas no `build_gold.py` (hoje só 3: `vw_kpi_mensal`, `vw_carteira_cliente`, `vw_cotacoes_funil`); filtros de gerência/vendedor; aba de Estoque (cobertura/giro); deploy do portal além do localhost.
- Proteger a chave SSH com passphrase (opcional): `ssh-keygen -p -f ~/.ssh/id_ed25519`.

### Higiene
- Recriar o bookmark do Simulador com o caminho novo.
- Validar que o `make lake` completo roda do início ao fim no caminho novo (motors + silver + gold).
