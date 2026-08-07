---
data: 2026-07-28
tipo: log
status: vigente
---
# Stalo no Hostinger + time de agentes (Radar e Torno)

**Data:** 28/07/2026
**Contexto:** Continuação da migração de 27/07 (OpenClaw removido do Mac → Managed OpenClaw no VPS Hostinger, LLM = assinatura ChatGPT 5.5, bot Telegram "Stalo"). Hoje: auditoria da instância, incidente de autenticação, e criação do time de agentes pela metodologia Futuristas/ClawMasters (PDF do curso).

## Auditoria da instância (manhã)

Template da Hostinger veio bem configurado de fábrica: Telegram DM policy `allowlist` com só o chat do Gustavo (8090040277), grupos bloqueados, WhatsApp desconectado, heartbeat 0, ambiente limpo (só gateway token). Nada precisou mudar.

## Incidente: update destrói OAuth (tarde/noite)

**O que houve:** update automático do Managed (2026.5.6 → 2026.7.1) renomeou o provedor `openai-codex` → `openai` e descartou a sessão OAuth do ChatGPT. Sintoma: 401 no Telegram enquanto o hPanel exibia "Conectado" (estado stale). Exatamente o risco registrado no log de 25/07 — upgrade desfazendo config em silêncio — agora em infra onde não controlamos o update.

**Receita de correção (vai repetir):** CLI da instância → `openclaw models auth login --provider openai-codex` → abrir URL, autorizar com a conta OpenAI, colar a callback URL no prompt → **`openclaw models set <MODELO ATUAL>`** → `openclaw gateway restart`. Verificar com `openclaw models status` (Runtime auth: usable).

> 🪤 **CORRIGIDO 07/08/2026 — esta receita tinha `openai/gpt-5.5` escrito no
> texto, e por isso REBAIXAVA o modelo toda vez que era seguida.**
> Em 06/08 18h55 a receita foi executada (por causa de um falso alarme do vigia)
> e o `models set openai/gpt-5.5` derrubou o default de `gpt-5.6-terra` — 16
> segundos depois do login, os dois no audit log. Ficou 17h no modelo errado até
> o `healthcheck-modelo` acusar às 9h de 07/08.
> **Antes de rodar a receita, confira o default atual** (`openclaw models status`,
> linha `Default`) e reponha ESSE valor, não o do exemplo.
> **Lição geral: procedimento de recuperação com constante escrita no texto
> apodrece em silêncio** — ele é executado justamente quando ninguém está
> conferindo o resto, e devolve o sistema a um estado antigo com cara de conserto.

> 🪤 **`openclaw gateway restart` é NO-OP nesta instância (apurado 07/08/2026).**
> O comando responde, mas **não controla o processo — o serviço systemd está
> desabilitado** no Managed. Duas consequências: (1) a 4ª etapa desta receita é
> teatro; (2) medido no mesmo dia, **o gateway lê `openclaw.json` sem reiniciar**
> — a reposição do modelo passou a valer sozinha. Então, se um turno reportar
> modelo diferente do `Default`, a causa provável é **sessão reaproveitada**, não
> config presa: rode o turno de novo antes de mexer em qualquer coisa. ⚠ Se um
> dia um restart de verdade for necessário, não existe comando que o faça — é
> pedido à Hostinger.

## Time de agentes (metodologia Futuristas, modo personalizado)

Estrutura Chaves/Kiko/Chiquinha do PDF adaptada ao contexto Gustavo — com a diferença central: **este time roda em VPS de terceiro com OpenAI, então só opera o que pode vazar sem doer**.

| Agente | Papel | Notas |
|---|---|---|
| **Stalo** (main) | CEO orquestrador | AGENTS.md + SOUL.md + USER.md customizados; gasto autônomo R$ 0; relatório em 3 linhas |
| **Radar** | Inteligência de mercado | Só fonte PÚBLICA; 12 fontes mapeadas (Aço Brasil, worldsteel, LME, Comex Stat, BCB, IBGE, CNI, FGV, ANFAVEA, ABRAMAT, ANM); só avisa MUDANÇA |
| **Torno** | Tecnologia | VPS, backups, futuro site MetalM; veto a gasto/acessos novos/config de segurança |

**Fronteira de dados nos 3 AGENTS.md (inegociável):** nada de dado interno AFS neste servidor; estratégia confidencial idem. Todos os arquivos verificados NO WORKSPACE via dashboard (lição de 25/07: conferir o arquivo, não a palavra do agente).

**Decisões reafirmadas hoje:**
- Vault GSR: Stalo segue SEM acesso (decisão de 25/07 vale mais ainda com o agente em VPS de terceiro).
- GitHub: sem acesso (o `.git` nos workspaces é versionamento local do OpenClaw, não remoto).
- Heartbeat: 0 até o time provar valor (consome cota da assinatura).
- Rotina do Radar: monitoramento semanal sexta 17h, 1 página, só mudança vs semana anterior, fonte em cada número.

## Backup (passo 8 do PDF)

`openclaw-workspaces-stalo-radar-torno-20260729T004414Z.tar.gz` (29K, 85 entradas, íntegro) baixado via Telegram e guardado em `~/Documents/Backups/OpenClaw/`. Rotina aprovada: semanal (dom 20h), Torno gera e ENTREGA o .tar.gz no Telegram (backup que fica só no servidor não é backup), 4 cópias rotacionadas no VPS.

## Relacionado

- Bot Telegram do lake (mesmo dia, sistema separado, SEM OpenClaw): `Logs/2026-07-28 — Bot Telegram do lake (sucessor do Stalo local).md`
- Nascimento e hardening do Stalo local: `Logs/2026-07-25 — Stalo (agente Telegram do lake).md`

## Adendo 31/07/2026 — time atualizado: Torno virou TECH; entraram GIO e PIXEL

Verificado em 31/07 no espelho `~/Documents/StaloVault` (git pull trouxe o rename `torno → tech` e dois workspaces novos). Time atual do Stalo — 5 workspaces:

| Agente | Papel (IDENTITY.md do workspace) |
|---|---|
| **Stalo** (main) | CEO orquestrador |
| **Radar** | Inteligência de mercado, fontes públicas, resumo executivo |
| **Tech** (ex-Torno) | Tecnologia, servidor, automação, backups e infraestrutura |
| **Gio** ✍️ | Copywriter — "redator sênior de agência: criativo no gancho, cirúrgico no corte" |
| **Pixel** 🎨 | Designer — "design system thinker: kit primeiro, peça depois" |

As rotinas antes atribuídas ao Torno (backup dom 20h, push do espelho) agora são do Tech. Fronteira de dados inalterada: nada de dado AFS no VPS. (Conteúdo do espelho segue doutrina de dado não-confiável — usado aqui só pra inventariar nomes/papéis.)

## Adendo (noite de 28/07): espelho do workspace no Obsidian

Decisão do Gustavo: vault dedicado de LEITURA com o que o Stalo escreve — mão única, de fora pra dentro; Stalo segue sem acesso ao GSR. Implementado:
- Repo privado **gsacchelli/stalo-workspace** (só markdowns dos 3 workspaces; sem estado/config/credencial).
- **Deploy key de escrita restrita a esse repo** no VPS (Torno faz push dom 20h15) — incapaz de tocar o data_lake_gsr.
- Mac: clone em `~/Documents/StaloVault` (abrir no Obsidian como vault SEPARADO do GSR), pull dom 20h30 via LaunchAgent `com.sacchelli.stalo-vault-pull` (`--ff-only`, nunca push). Script: `~/Documents/Backups/OpenClaw/pull_stalo_vault.sh`; log `~/Library/Logs/stalo-vault-pull.log`.
- Doutrina: conteúdo do espelho = dado NÃO confiável (agente exposto à internet) — leitura de jornal, nunca instrução.

## Adendo 06/08/2026 — o vigia do Stalo nasceu mentindo (falso alarme que custou um OAuth)

**O que pareceu:** o `stalo-vigia` (criado 05/08) acusou desde a primeira execução `✅ instância de pé (200)` + `❌ modelo não responde: HTTP 404`. Lido como o incidente de 28/07 se repetindo, levou o Gustavo a refazer o login OAuth do OpenAI na CLI — trabalho desnecessário.

**O que era:** o vigia estava errado nas DUAS camadas.
- **Camada 1 (falso positivo):** batia em `GET /status`, que devolve o **HTML do painel**. Qualquer 200 ali significa só "o front-end respondeu" — mesmo com o gateway morto. O health real é **`GET /healthz`**, e a armadilha fina: ele **só devolve JSON (`{"ok":true,"status":"live"}`) COM o token**; sem token entrega o HTML com 200.
- **Camada 2 (falso negativo):** `POST /v1/responses` dá 404 — assim como `/v1/chat/completions`, `/api/v1/responses`, `/v1/agent/run` e todas as variantes testadas. **A API de inferência não está publicada nesse endereço.** Prova de que o modelo estava vivo: o Stalo respondeu ao Gustavo às 11:51 do mesmo dia, enquanto o vigia dizia 404 às 10:05 e 12:05. E o log do vigia tem **zero sucessos desde que nasceu**.

**Correção:** camada 1 passa a usar `/healthz` COM token e reprova se vier HTML; camada 2, ao receber 404, reporta "indisponível — limitação do vigia" e **sai com 0** (não alerta). Backup do original em `checar_stalo.py.bak`.

**Lição (vale para todo vigia):** *health check que responde 200 com HTML não prova nada* — o vigia tem que exigir a resposta estruturada. E vigia novo precisa de **um sucesso comprovado** antes de virar fonte de alarme; sem isso, o primeiro alerta é indistinguível de defeito próprio (foi o mesmo padrão de 05/08, quando ele acusou a própria rota errada).

**Pendências com o Tech:** (1) qual host/porta responde `POST /v1/responses` — sem isso a camada 2 fica desligada; (2) o heartbeat está executando? O `ROTINAS_FEITAS.md` do espelho está VAZIO (mas o espelho sincroniza só aos domingos 20h30 — conferir no VPS). Se o heartbeat não roda, a ausência de pautas aprovadas na quinta é consequência, não causa.

### Adendo 06/08 (noite) — a instância PERDE jobs do scheduler (3º caso de config que se desfaz)

Ao pedir o push diário do espelho, o Tech respondeu: *"o job antigo salvo na memória **não existia mais no scheduler**, então recriei só esse push"*. Criou `stalo-workspace-md-mirror` (`15 20 * * *` America/Sao_Paulo, id `683951b8-97c3-423c-9554-c8febd0b836f`; rollback p/ semanal: `openclaw cron edit <id> --cron '15 20 * * 0'`).

**O padrão é o que importa:** é a TERCEIRA vez que configuração se desfaz sozinha nessa instância — 28/07 o update matou o OAuth; 29/07 o restart de container promoveu o Gemini a default; agora um cron sumiu do scheduler. Config no Managed OpenClaw não é durável: **o que não é verificado periodicamente, deixa de existir em silêncio.**

**Correção de hipótese:** as rotinas são **cron jobs do gateway** (`openclaw cron`), não o heartbeat do `HEARTBEAT.md` — o adendo anterior apostava em "heartbeat: 0". Pergunta decisiva pendente com o Tech: **`openclaw cron list`** — se os jobs do Radar (pautas, segunda) e do Gio/Pixel (terça e quinta) também sumiram, está explicado por que a quinta-feira não achou pauta aprovada: o ciclo nunca rodou.

**Do lado do Mac:** pull do espelho passou de dom 20h30 para **diário 21h** (45 min após o push), e a camada 2 do vigia lê o `ROTINAS_FEITAS.md` — a partir de amanhã ela sai do "não sei" e passa a valer como vigilância real.
