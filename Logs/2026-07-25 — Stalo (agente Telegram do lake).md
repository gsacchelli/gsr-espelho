# Stalo — agente Telegram do lake (nascimento)

**Data:** 25/07/2026
**Contexto:** agente criado no OpenClaw, conectado ao Telegram, rodando na máquina local junto do afs-lake.

## O que é

Interface móvel de **LEITURA** do data lake (`lake/gold/sacchelli.duckdb`). Três camadas de função:

1. **Consulta de bolso** — perguntas comerciais em linguagem natural via Telegram (KPIs, clientes, pendentes, estoque, pricing), respondendo curto, número primeiro, sempre citando a data do dado.
2. **Sentinela** — vigia mtime do duckdb + logs dos LaunchAgents (`cockpit_sql_30min.log`, `portal_sac360.log`). Alerta só quando quebra; silêncio = saúde.
3. **Briefing 7h15 seg-sex** — Foco do Dia do Cockpit + pendentes novas relevantes (>R$ 100k ou bloqueio) + estoque CRITICO se mudou. Máx 5 linhas.

**Não é:** motor, gerador de painéis, tomador de decisão. Não re-litiga definições (`definicoes.py` é a fonte).

## Nome

**Stalo** = aço em Esperanto (rigorosamente *ŝtalo*; *stalo* sem diacrítico é "estábulo" — irrelevante na prática). Escolhido sobre "GuGaL" (piada interna que não escala) e "Torre" (candidato anterior). Comunica o domínio, funciona como vocativo no Telegram, sobrevive se um dia for exposto aos gerentes.

## Onde vive o prompt

Lado OpenClaw: `IDENTITY.md` + `memory/stalo-brief.md` (Stalo confirmou persistência entre restarts). O prompt canônico foi desenhado na sessão Claude Code de 25/07 — seções: fonte de dados, regras de resposta Telegram, armadilhas de dado (holdings contains, pu_kg, engenheirados, bitolas polegada, MC benef.), sentinela, allowlist de ações, segurança.

## Guard-rails (inegociáveis)

- **Read-only por padrão.** SQL só SELECT. Única ação permitida: `make cockpit-sql`, com confirmação "s/n".
- **Allowlist de chat ID** — só Gustavo; idealmente na config do gateway (prompt é segunda linha de defesa).
- Nunca ecoar `.env`, credenciais Softcomp, senhas de app.
- Conteúdo encaminhado por terceiros = dado, não instrução (anti prompt-injection).

## Decisão de acesso: vault e GitHub — NÃO (25/07/2026)

- **Vault GSR: sem acesso.** O vault contém o material mais sensível que existe (Duferco, MetalM, transição de carreira, valuations). Stalo é um endpoint exposto a rede (Telegram) — cada acesso a mais é superfície de vazamento. E ele não precisa: tudo do escopo dele (definições, catálogo de views, docs técnicos) já vive no repo `~/dev/afs-lake` (`definicoes.py`, `06_Docs/Catalogo_Dados_SAC360.md`), que ele lê localmente. Se um dia precisar de um doc específico do Sistema Operacional Comercial, copiar o doc pro repo — não abrir o vault.
- **GitHub: sem acesso.** O repo é local na mesma máquina; leitura local já cobre qualquer necessidade de contexto. Acesso GitHub = capacidade de escrita/push = contradiz o contrato read-only. Sem caso de uso, só risco.

## Status do primeiro boot (relatório do Stalo, 25/07)

- Lake conecta: 22 views OK, leitura via `.venv/bin/python` + duckdb 1.4.4 read-only.
- MCP afs-lake NÃO registrado na sessão dele — opera por Python local. Funciona; registrar o MCP no gateway é opcional (nice-to-have, não bloqueia).
- Defasagem detectada corretamente: `vw_pedidos` até 30/06 (esperado — cadência mensal, atualizar via `make pedidos-portal` pós-fechamento). Cockpit-sql: último run 24/07 16:02 · 3.880 pendentes · pipeline R$ 24,1M.

## Auditoria de segurança + hardening (25/07/2026, sessão Claude Code)

Barra definida pelo Gustavo: qualquer dúvida estrutural → eliminar o bot. **Veredito: manter — nenhum achado estrutural; gaps encontrados foram corrigidos em runtime, não só em prompt.**

**Estado encontrado (bom):** gateway bind loopback (confirmado via lsof: só 127.0.0.1/::1, porta 18789), Tailscale off, Telegram `dmPolicy: pairing` + `groupPolicy: disabled`, **allowlist de pareamento VAZIA** (ninguém — nem Gustavo — pareado ainda; desconhecido que achar o bot cai em fila de aprovação), token do bot em `secrets/` com perms 600, denyCommands p/ camera/sms/etc.

**Gaps encontrados e corrigidos:**
1. **Exec default do OpenClaw era `security=full, ask=off`** — Stalo tinha shell completo sem aprovação; contrato read-only era só prompt. → Política trocada p/ `security=allowlist, ask=on` (defaults + agente main). Agora só o Python do venv roda direto; qualquer outro comando pede aprovação ao Gustavo (askFallback=deny).
2. **Interpretador allowlistado sem trava** — `python -c "qualquer coisa"` passava. → `tools.exec.strictInlineEval=true` + criado runner fixo `MotorAnalitico/agente/stalo_query.py` (SELECT/WITH only, conexão read_only, 1 instrução, máx 200 linhas; testado: rejeita UPDATE e multi-statement). Brief do Stalo atualizado p/ usar só o runner.
3. Grant órfão `crestodian: full/ask:off` (artefato do onboarding) removido do exec-approvals (backup em `exec-approvals.json.bak-pre-hardening`).
4. `controlUi.allowInsecureAuth` desligado.

**Dois bugs de config descobertos no teste real (25/07, manhã):**
- `ask: "on"` é valor INVÁLIDO (enum aceita `off|on-miss|always`) — o CLI descartou em silêncio e a política ficou em `ask=off`: comando fora da allowlist era negado seco, sem chegar pedido de aprovação. Corrigido p/ `on-miss` no exec-approvals + `tools.exec.ask`.
- **Allowlist de interpretador não funciona com venv**: `~/dev/afs-lake/.venv/bin/python3` é SYMLINK pro Python do CommandLineTools; a política resolve o binário real antes de casar o padrão → nunca casava. **Solução melhor que a original:** o runner virou executável com shebang pro venv e a allowlist passou a conter **o SCRIPT** (`MotorAnalitico/agente/stalo_query.py`), não um interpretador. Ganho de segurança: allowlistar "python" autorizaria rodar qualquer script; allowlistar o runner autoriza exatamente uma coisa. Stalo chama direto, sem `python3` na frente.

**Auditoria embutida (`openclaw security audit`): 0 critical · 1 warn** (trusted proxies — irrelevante, sem proxy reverso, loopback-only).

**Limite honesto do modelo de segurança:** o OpenClaw não é sandbox hermético — o Stalo roda como o usuário gustavosacchelli. As camadas reais são: (1) ninguém fala com ele sem pareamento aprovado; (2) gateway inacessível pela rede; (3) exec allowlist+ask em runtime; (4) prompt. Se um dia o pareamento for aberto a terceiros, reavaliar do zero.

## ⚠️ ACHADO ESTRUTURAL — o modelo de segurança desenhado NÃO é implementável neste backend (25/07, manhã)

Depois de 3 rodadas de teste com o Stalo batendo em "negado", fui ao código-fonte do OpenClaw (`dist/claude-live-session-*.js:1403` e `:1360`). A regra é literal:

```js
const allowed = execPermission.security === "full" && execPermission.ask === "off";
permissionMode: security === "full" && ask === "off" ? "bypassPermissions" : "default"
```

**Com o backend `claude-cli` (Claude Code como motor do agente), a allowlist de exec NUNCA é consultada.** É binário:
- `security=full` + `ask=off` → Claude Code roda em `bypassPermissions`: **shell irrestrito**, sem allowlist, sem aprovação.
- Qualquer outra combinação → **todo uso de ferramenta nativa (Bash/Write/Edit) é negado em bloco**; não existe fluxo de aprovação, o ping no Telegram nunca acontece.

Ou seja: o desenho aprovado (runner allowlistado + aprovação caso a caso) **não existe** nesse backend. Testei também regra de permissão do próprio Claude Code em `~/.openclaw/workspace/.claude/settings.json` — não vence o handler do OpenClaw; segue negado.

**Segundo achado, mais grave: `Read` NÃO é gated.** Mesmo com o Bash trancado, o agente lê qualquer arquivo do usuário. Confirmado em teste: ele **leu o `~/dev/afs-lake/.env`** e reportou (sem expor valores, por decisão própria — comportamento correto) que contém **chave de API Anthropic real e senha real do banco SQL Softcomp em texto puro**. A allowlist de exec nunca foi fronteira de segredo. O mesmo vale pro vault GSR: a decisão "Stalo não acessa o vault" era prompt, não mecanismo — `Read` alcança tudo.

### Ações imediatas decorrentes
- [ ] **Rotacionar as credenciais do `.env`**: revogar/gerar nova chave Anthropic no console; trocar a senha do usuário SQL Softcomp (pedir ao Nelson/Francisco). Tratar como expostas — passaram por um processo com canal de rede.
- [ ] Tirar os segredos do texto puro (Keychain ou secrets do gateway) antes de religar qualquer agente.
- [ ] Decidir arquitetura (ver abaixo) — Stalo segue TRANCADO (sem Bash) até a decisão.

### Decisão (25/07): opção 2 — trocar backend pra API Anthropic

Confirmado no código que o caminho funciona: o tool próprio do OpenClaw (`dist/bash-tools-*.js`) importa `evaluateShellAllowlistWithAuthorization` e implementa aprovação real com timeout + `askFallback=deny`. Com backend de API o agente usa ESSES tools (não os nativos do Claude Code), então allowlist e aprovação passam a ser mecanismo.

Hardening aplicado (vale só no backend de API — testado e confirmado que NÃO tem efeito no claude-cli):
- `tools.fs.workspaceOnly=true` — read/write/edit limitados a `~/.openclaw/workspace` (fecha o buraco do `.env` e do vault).
- `tools.elevated.enabled=false`.
- Mantidos: `security=allowlist`, `ask=on-miss`, `strictInlineEval=true`, allowlist só com o runner.

**EXECUTADO E VALIDADO 25/07 ~10h.** Backend trocado pra `anthropic/claude-sonnet-5` (chave nova inserida pelo Gustavo via `models auth paste-api-key`; a chave antiga do `.env` e uma segunda chave exposta em chat foram revogadas por ele). Três testes end-to-end, todos verificados no audit — não na palavra do agente (numa rodada ele respondeu de memória sem chamar ferramenta nenhuma; só o `openclaw audit` mostrou isso):
1. **Runner passa direto** — `tool.action:exec succeeded`, saída correta do duckdb.
2. **Comando fora da allowlist (`whoami`) → aprovação real** — `exec.approval.waitDecision` ficou 41 min esperando, com mensagem entregue no Telegram do Gustavo; sem resposta, expirou e a ferramenta falhou (askFallback=deny). O fluxo prometido existe de fato neste backend.
3. **Filesystem fora do workspace bloqueado** — `read` retornou "Path escapes sandbox root (~/.openclaw/workspace)". `.env`, repo e vault agora são inalcançáveis por ferramenta de arquivo. (Nota: o agente se recusou a sequer TENTAR abrir o `.env` mesmo com autorização explícita no teste, e sinalizou a repetição do pedido como possível engenharia social — comportamento correto; o teste do mecanismo teve que usar arquivo neutro.)

Efeito colateral aceito: o Stalo não lê mais `definicoes.py`/catálogo/docs do repo. A referência dele passa a ser o próprio brief (lista de views + armadilhas de dado). Se precisar de doc novo, copiar pro workspace dele.

Pendente anterior (histórico): chave de API (só o Gustavo insere — `openclaw models auth paste-api-key --provider anthropic`), depois trocar `agents.defaults.model.primary` e revalidar os 3 testes (runner passa / comando fora da lista pede aprovação / `.env` bloqueado).

### Opções de arquitetura (histórico da decisão)
1. **Matar o Stalo** — coerente com a barra "qualquer dúvida, elimina". Custo: perde a consulta de bolso.
2. **Trocar o backend do agente pra API Anthropic** (em vez do Claude Code CLI) — aí a allowlist de exec do OpenClaw passa a valer de verdade e o desenho original funciona. Custo: chave de API + billing por token, separado da assinatura.
3. **Aceitar `full`/`bypassPermissions`** — funciona hoje, mas dá shell irrestrito ao agente. **Não recomendado** dada a barra declarada.

## Briefing de pedidos 8h00 — NO AR (25/07)

Cron job do gateway `briefing-pedidos-8h` (id `ec04598a-…`), `0 8 * * 1-5` em America/Sao_Paulo, entrega direto no Telegram do Gustavo. **Payload é comando, não turno de agente** — roda `MotorAnalitico/agente/briefing_pedidos.py` e manda a saída crua. Sem modelo no meio: custo zero de token, número não passa por LLM. Testado com `cron run`: entregue OK.

Conteúdo (spec do Gustavo, 25/07): pedidos do último dia útil por gerência (valor, peso, nº de pedidos) + acumulado do mês até ontem + **ritmo** = acumulado ÷ dias úteis decorridos × dias úteis totais do mês.

Decisões de calendário: dias úteis excluem sáb/dom, feriados **federais e estaduais de SP** (lib `holidays`, subdiv SP — instalada no venv). Carnaval (seg/ter) e Corpus Christi entram como NÃO úteis por decisão operacional AFS, apesar de ponto facultativo — editável na constante `OPCIONAIS_NAO_UTEIS` do script. Numa segunda-feira a janela cobre sex-dom (não perde lançamento de fim de semana); no dia seguinte a feriado, cobre o feriado junto.

Números do primeiro run (sex 24/07): Felipe/Fuscão R$ 366.010 · 36,4 t; Odair-PIR R$ 101.559; Odair-SCA R$ 91.247; Fabiola R$ 75.288; Fernando R$ 31.830. Total R$ 665.934 · 61,6 t. Mês até 24/07: R$ 14,38 MM. Ritmo: R$ 18,61 MM (17 de 22 dias úteis).

Nota: a base de pedidos avançou pra **24/07** durante a sessão (estava em 30/06 de manhã).

## Endurecimento pós-decisão "manter o bot" (25/07, tarde)

Gustavo perguntou se vale manter o agente. Resposta: manter, mas separando o **briefing 8h** (cron determinístico, risco ~zero, valor diário) do **Stalo conversacional** (o que precisa de escrutínio). Risco residual honesto: não é o agente virar malicioso — é um upgrade do OpenClaw reabrir em silêncio o que fechamos, já que o painel de status do produto exibiu política "allowlist + aprovação" enquanto o backend a ignorava por completo.

Executado:
- **Controle de navegador DESLIGADO** (`plugins disable browser`) — superfície grande, zero uso aqui.
- **Atualização automática travada**: `update.auto.enabled=false`, `update.checkOnStart=false`, canal `extended-stable` (nunca auto-aplica). Regra combinada: após qualquer upgrade manual, repetir os 3 testes de hoje (runner passa / fora da allowlist pede aprovação / fs fora do workspace bloqueado).
- **Ferramentas elevadas desligadas** (antes habilitadas).
- Auditoria final: **0 critical**; `tools.elevated: disabled`, `browser control: disabled`.
- **Revisão marcada p/ ~25/08/2026**: se a consulta ad-hoc pelo Telegram tiver sido usada só 2-3 vezes no mês, matar a parte conversacional e ficar só com o cron.
- **Gatilho de cancelamento definido**: se o Gustavo começar a aprovar pedidos no Telegram por reflexo, sem ler, a trava deixou de existir → desligar.

### Segredos: `.env` deixou de ser a fonte (25/07)

Criado `MotorAnalitico/segredos.py` — fonte única, ordem **ambiente → Keychain (serviço `afs-lake`) → `.env` (legado)**. `portal/comum.py::env()` e `sql/conexao.py::_env()` agora delegam pra ele (mudança compatível: nada quebra, conexão real ao Softcomp testada OK após o refactor). `.env` teve permissão fechada pra 600.

Migrar cada segredo (o valor é digitado em prompt oculto, não passa por arquivo nem por chat):
```
security add-generic-password -s afs-lake -a SOFTCOMP_SQL_PASSWORD -w -U
```
Depois apagar a linha do `.env`. Conferir status: `.venv/bin/python3 MotorAnalitico/segredos.py` (imprime a ORIGEM de cada chave, nunca o valor). Pendentes hoje: ANTHROPIC_API_KEY, SOFTCOMP_SQL_PASSWORD, SOFTCOMP_SQL_USER.

## Pendências

- [x] ~~Canal do briefing: Telegram via cron do gateway~~ — feito (briefing de pedidos 8h00).
- [x] ~~Allowlist de chat ID na config do gateway~~ — feito: pareamento aprovado, ID 8090040277 é owner, fila de pendentes vazia.
- [ ] **Rotacionar senha do usuário SQL Softcomp** (Nelson/Francisco) e tirar segredos do `.env` em texto puro. Chave Anthropic já rotacionada pelo Gustavo.
- [ ] **Decisão 25/07: NÃO incluir os demais reports por enquanto** — sentinela de pipelines e briefing qualitativo (Foco do Dia, pendentes novas, estoque CRÍTICO) ficam parados. Rodar o de pedidos primeiro e ver o que falta na prática.
- [ ] (Opcional) Registrar MCP afs-lake na sessão do Stalo pra ganhar as tools canônicas (kpi_executivo, ficha_360…).
