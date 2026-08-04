---
data: 2026-08-04
tipo: log
status: vigente
---
# Stalo apagado no Hostinger + kit de restore

**Data:** 04/08/2026
**Contexto:** a instância OpenClaw do VPS Hostinger foi apagada. Sessão de recuperação: inventariar o que sobreviveu, medir o que se perdeu, e montar a receita de remontagem dos 5 agentes.

## O que sobreviveu — e por quê

**Nenhum prompt se perdeu.** Três cópias independentes, todas conferidas nesta sessão:

| Cópia | Onde | Data |
|---|---|---|
| Espelho git local | `~/dev/stalo-vault` | commit `84643cf`, 02/08 20h15 |
| Espelho GitHub | `gsacchelli/stalo-workspace` | mesmo commit — confirmado no ar |
| Tarball | `~/Documents/Backups/OpenClaw/…20260729T004414Z.tar.gz` | 29/07, 85 entradas |

A decisão de 28/07 — *"backup que fica só no servidor não é backup"* — é o que salvou a operação. O espelho de markdown pro GitHub e o tarball baixado pelo Telegram eram exatamente a redundância que faltava no desenho original.

## O que se perdeu (e a lição de cada perda)

- **Os scripts do VPS** (`mirror-stalo-workspace-md.sh`, `pull-conhecimentos-gerais.sh`). O espelho só carregava `.md` — protegeu os PROMPTS e não a INFRA. Reconstruídos nesta sessão, e agora versionados **no Mac**, não no servidor.
- **As 2 deploy keys.** Regerar; as antigas seguem autorizadas nos repos do GitHub até alguém removê-las.
- **Definição dos 4 crons.** Salva por acaso: o Stalo tinha registrado ids e horários no próprio `MEMORY.md`. Sorte, não desenho.
- **02/08 → 04/08 de trabalho dos agentes.** O espelho era **semanal** (domingo 20h15) e a instância caiu numa terça.
- **`SOUL.md` do Radar e do Tech nunca foram customizados** — ficaram no template genérico do OpenClaw desde 28/07. Não é perda: é dívida descoberta pelo inventário.

## Decisões tomadas

**1. Remontar com os 5 agentes.** Levantei que uma semana de operação rendeu 1 rascunho do Gio, 1 kit do Pixel e uma newsletter do Radar que precisou de correção de cron — e propus remontar só com Stalo/Radar/Gio. **Gustavo optou pelos 5.**

**2. Espelho passa de semanal para DIÁRIO** (20h15 no VPS, 20h30 no Mac). Reduz a perda máxima de 7 dias para 24h. Custo: zero.

**3. Plataforma — rota A recomendada, decisão pendente do Gustavo.** Dos 3 incidentes em 8 dias de operação, **2 têm a mesma causa raiz: o template Managed da Hostinger** (update de 28/07 apagou o OAuth; script de boot de 29/07 remove o modelo a cada restart de container). Rota A = VPS limpo com OpenClaw pinado por nós, +1h de setup, resolve na raiz. Rota B = manter o Managed e adicionar healthcheck horário do modelo, +20 min, detecta mas não previne. Se ficar no B, o healthcheck é obrigatório.

**4. Plano KVM 2** (2 vCPU / 8 GB). O KVM 1 aperta quando o Pixel renderiza PNG com headless browser. Decidir pelo preço de **renovação** (US$ 14,99), não pelo promocional. A alavanca real não é cupom — é a garantia de 30 dias: se o time não se pagar, sai sem custo.

**5. Infra passa a ser versionada como os prompts.** Kit em `~/dev/stalo-restore` (git local, sem remoto): runbook `RESTORE.md`, os 2 scripts reconstruídos, `infra/crons.md` (com os ids antigos como rastro e coluna pros novos), `infra/env.md` (nomes de segredo, **nunca valores**), e os `SOUL.md` novos do Radar e do Tech. Regra escrita no topo do runbook: **mexeu no VPS, reflete aqui.**

## Melhorias embutidas na remontagem

- **Guarda anti-vazamento no script de espelho** (padrão do `push_conhecimentos_gerais.sh`): aborta antes do commit se aparecer arquivo não-markdown ou padrão de credencial no conteúdo novo.
- **`referencias/` sai do espelho** — é o clone do `conhecimentos-gerais`, que já tem repo próprio. O espelho guarda o que os agentes **escrevem**, não o que **leem**.
- **Trava de mão única** no clone do `conhecimentos-gerais` no VPS: push apontado pra lugar nenhum, e o script reverte se alguém reconfigurar.
- **`SOUL.md` do Radar e do Tech** escritos com as cicatrizes registradas — o Tech carrega no prompt "depois de todo restart, conferir o estado do modelo antes de dizer que está tudo bem", que é a lição de 28-29/07 virando comportamento.

## Fronteira de dados — reafirmada

Inalterada e inegociável: nada de dado interno AFS no VPS (cliente, preço, margem, cotação, faturamento), nada de estratégia confidencial, Stalo segue **sem acesso ao vault GSR**. O espelho `~/dev/stalo-vault` continua sendo **dado não-confiável** na direção contrária — origem é VPS exposto à internet; nenhum agente do lake o lê, nunca entra em `--add-dir`.

## Relacionado

- `Logs/2026-07-28 — Stalo no Hostinger + time de agentes (Radar e Torno)` — nascimento do time, incidente do OAuth, decisão do espelho
- `Logs/2026-07-25 — Stalo (agente Telegram do lake)` — auditoria de segurança e hardening que definiu a barra
- `Logs/2026-07-31 — Vault ConhecimentosGerais (base pública Flori + Stalo)` — o canal de mão única Mac→VPS
- Kit de restore: `~/dev/stalo-restore/RESTORE.md`
