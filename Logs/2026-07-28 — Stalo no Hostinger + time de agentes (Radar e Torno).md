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

**Receita de correção (vai repetir):** CLI da instância → `openclaw models auth login --provider openai-codex` → abrir URL, autorizar com a conta OpenAI, colar a callback URL no prompt → `openclaw models set openai/gpt-5.5` → `openclaw gateway restart`. Verificar com `openclaw models status` (Runtime auth: usable).

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
