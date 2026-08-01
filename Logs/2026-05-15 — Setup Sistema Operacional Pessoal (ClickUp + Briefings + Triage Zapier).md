---
data: 2026-05-15
tipo: log
status: vigente
---
# 2026-05-15 — Setup Sistema Operacional Pessoal (ClickUp + Briefings + Triage Zapier)

**Duração:** ~3h em sessão única
**Trigger:** "Quero criar uma automação entre Gmail (Sacchelli) e ClickUp, pensando em testar N8N por ser mais barato"
**Resultado:** Sistema operacional pessoal redesenhado, 51 tasks ruído removidas, 2 rituais automatizados agendados, decisão Zapier parqueada com base em dados.

---

## A virada da pergunta

A pergunta inicial era "Zapier vs N8N por economia". Análise da conta Zapier revelou três fatos que mudaram o frame:

1. **Plano Zapier Pro**: US$ 239,88/ano (~US$ 20/mês, ~R$ 100/mês)
2. **0 tasks billable em 30 dias** (filtros reprovam quase todos os triggers antes do step billable — Zapier não cobra task filtrada)
3. **Downgrade pra Free já agendado pra 11/nov/2026** — eu mesmo havia cancelado renovação

Conclusão imediata: pagando caro pra usar quase nada, com Free chegando que **limita Zaps a 2 steps** (meus 2 Zaps têm 7 steps cada — vão quebrar no D-day).

A pergunta certa: "**preciso migrar antes de nov/2026 OU cancelar o downgrade**", não "Zapier vs N8N".

Mas a virada maior veio depois: ao olhar o ClickUp, vi 69 tasks abertas, ID custom AFS-202 — o ClickUp **não está morto**, está acumulado. Não tinha problema de capture, tinha problema de **revisão**. Mais automação não ia resolver. **Ferramenta não cria hábito, trigger cria.**

Daí emergiu o trabalho real: redesenhar o sistema operacional pessoal, não trocar ferramenta.

---

## Auditoria Zapier (situação atual)

### Plano
- Pro, US$ 239,88/ano (cobrado anual)
- 750 tasks/mês de quota
- Downgrade agendado pra Free em 11/nov/2026 (já cancelei renovação)
- Próximo reset de quota: 11/jun/2026
- Outros produtos: Agents (Free), Chatbots beta (Free)

### Uso real (30 dias)
- **0 tasks billable** apesar de 2 Zaps rodarem
- Filtros (Filter by Zapier) reprovam quase todos triggers antes do step billable
- Quota de 750 sendo desperdiçada

### Zaps ativos
1. **"Criação e update de tarefa através do Gmail Extension → ClickUp"** (ID 339067882, v12 — já refeito 12 vezes)
   - 7 steps: ClickUp trigger → Filter → Code JS → Gmail Find Email → Filter → Code JS (processa labels) → ClickUp Update Task
   - Trigger: nova task criada no ClickUp (via extensão do ClickUp dentro do Gmail)
   - Função: enriquece a task com infos do email original (labels viram tags/prioridade)
   - Last successful run: 09/abr/2026 (não rodou há +1 mês, pode estar com problema)
2. **"Status update from ClickUp → Gmail"** (ID 339129203, v5)
   - 7 steps: ClickUp Task Changes → Filter → Gmail Find Email → Filter → Code JS → Gmail Remove Label → Gmail Add Label
   - Função: quando task muda no ClickUp (status), troca o label do email correspondente no Gmail
   - Last successful run: 12/mai/2026 (3 dias atrás — ativo)

### Trade-off Zapier × N8N × Make (pós-nov/2026)
| Critério | Zapier Free | N8N Cloud | N8N Self-Host | Make Free |
|---|---|---|---|---|
| Custo | US$ 0 | ~€20/mês | ~US$ 5-10/mês | US$ 0 (1k ops/mês) |
| Multi-step (7 steps) | ❌ máx 2 | ✅ | ✅ | ✅ |
| Code nodes | ❌ | ✅ | ✅ | ✅ |
| Manutenção | Zero | Quase zero | Você é o ops | Zero |
| Risco quebrar Zaps atuais | **ALTO** (em 11/nov) | Baixo | Baixo | Baixo |

### Decisão parqueada
Não tomei decisão de cancelar downgrade nem migrar. Razão: depende do USO real do sistema novo nos próximos 60 dias. Se ClickUp pegar tração, Zaps viram infraestrutura valiosa e vale cancelar o downgrade (US$ 240/ano = R$ 100/mês é barato pra capture funcionando). Se não pegar tração, Free serve OU vou pra Make.

Reavaliação: **30-60 dias** (entre meados de junho e meados de julho/2026).

---

## Triage massiva no ClickUp (achado crítico)

### Antes
- 1 Space (Sacchelli)
- 4 Lists planas (Central, Marketing, Comercial GRU, Comercial CXJ)
- **69 tasks abertas**
- Custom ID AFS-N até AFS-202

### Diagnóstico do ruído
Investigação revelou que dois e-mails de janeiro/2026 haviam gerado **explosão de subtasks fantasmas** via agente AI antigo (creator "Stalo" — id -27913788):

1. **Cluster Flytour** (28 tasks, AFS-115 a AFS-138): email da Cintia Gomes Silva (Flytour SP Boa Vista) em 6/jan/2026 pedindo retomada do Tech Travel virou 28 subtasks vazias do tipo "preparar resposta", "revisar histórico", "alinhar com áreas internas". AFS-117 ainda tinha 4 sub-subtasks. AFS-116 tinha 8 sub-subtasks. Padrão: pra responder UM email, foram criadas ~30 tasks.

2. **Cluster Cliente 3086** (28 tasks, AFS-139 a AFS-166): emails do Odair Oliveira em 7/jan/2026 (Fwd: COTAÇÃO + Fwd: Contrato de Consignação Industrial e Comercial WEG/Bruno Mussa) viraram 28 subtasks vazias do mesmo tipo.

Total ruído: ~56 tasks (4 meses sem revisão, virou ruína).

### Decisão
Ambos clusters: **resolvidos fora do ClickUp** (já tinham 4+ meses). Triage:
- 51 tasks deletadas (subtasks fantasmas + 3 pais que perderam validade)
- 17 tasks legítimas preservadas (incluindo AFS-10 Definir Bônus 2026 urgent, AFS-99 Sacchelli 60 anos high, AFS-185 Manual Boas Práticas, AFS-193-196 comerciais ativas)

### Lição
**O Zap #1 (Gmail Extension → ClickUp) provavelmente foi quem alimentou o agente Stalo que decompôs demais.** Versão v12 reflete 12 iterações de tentar refinar isso. Capture sem ritual de leitura = ruído acumulado.

Antes de mexer no ClickUp, **desliguei os 2 Zaps** temporariamente pra evitar cascata de webhooks DELETE causarem estragos no Gmail (labels). Religuei ao final.

---

## Arquitetura do novo sistema

### Filosofia
```
CAPTURE  →  TRIAGE  →  EXECUTION  →  REVIEW
```

Princípio: **ritual de leitura > automação de escrita.** Sem revisão, capture vira lixo. Mais automação não cria hábito — gatilho de leitura cria.

### Estrutura ClickUp final (2 Spaces, 9 Folders, 18 Lists úteis)

**🏢 Sacchelli** (operação AFS, já existia)
- 📥 Inbox (capture do Gmail Sacchelli)
- Central, Marketing, Comercial GRU, Comercial CXJ (Lists legacy — migrar gradualmente)
- 📁 Comercial (vazio — apagar no UI, duplica Central/GRU/CXJ)
- 📁 Marketing (vazio — apagar no UI, duplica Marketing legacy)
- 📁 Operacional/ RH · Financeiro · Sistemas
- 📁 Pricing & Análise/ Motor Analítico · Painéis · Simulador Pricing · Agente Analítico

**👤 Pessoal** (novo Space, criado durante a sessão)
- 📥 Inbox Pessoal
- 📁 MetalM/ Estratégia & Modelo · Operacional · Captação & Investidores · Network
- 📁 Estratégico/ Duferco · Carreira & Transição · Wagner & Sucessão AFS · Leituras
- 📁 Saúde/Geral · Família/Geral · Finanças pessoais/Geral

### Convenções

**Tags (contexto de execução, não área):**
- `@email`, `@call`, `@leitura`, `@decisão`, `@aguardando`, `@5min`, `@profundo`
- Filosofia: tag responde "como vou fazer?", Folder responde "sobre o que é?"

**Custom IDs por Space:**
- AFS-N (Sacchelli, preservar numeração existente em AFS-202)
- MTL-N (MetalM, criar)
- EST-N (Estratégico, criar)
- PER-N (Pessoal, criar)

**Status padronizados (pendente próxima sessão):**
- 📥 Capturado · 🎯 Próximo · 🔄 Em progresso · ⏸ Aguardando externo · ✅ Concluído
- Custom statuses atuais ("a fazer", "responder", "acompanhar", "em progresso") são confusos — "responder" é o que faço, não onde a task está

### Lessons learned na arquitetura

1. **Over-engineered no primeiro corte.** Propus 4 Spaces (Sacchelli, MetalM, Estratégico, Inbox, Pessoal). Gustavo questionou: "Por que tudo isso? Particulares podem ficar juntos." Recalibrei pra 2 Spaces. **Mais Spaces = mais cliques pra navegar, sem benefício real pra solo.**

2. **"Geral" é preguiçoso.** Primeira versão tinha 9 Lists "Geral" — placeholders ruins que viram cemitério. Refinei pra 18 Lists com nomes específicos. Princípio: **se eu não consigo nomear a List em 3 palavras úteis, ainda não entendi pra que ela serve.**

3. **API do MCP ClickUp tem buracos.** Não tem `create_space`, não tem `delete_folder`, não tem `delete_list`, não tem `move_list_between_folders`. Resultado: 2 Folders duplicados no Sacchelli (Comercial + Marketing vazios) precisam ser apagados manualmente no UI. Lists antigas (Central, GRU, CXJ, Marketing) não podem ser movidas pra dentro dos Folders novos via API — terão que ser migradas com create+copy+delete (trabalhoso) ou ficar onde estão.

---

## Automações ativas

### Capture (escrita)
1. **Gmail Sacchelli → ClickUp** (Zapier #1, ON novamente após pausa pra triage)
2. **ClickUp → Gmail labels** (Zapier #2, ON novamente)
3. **Apple Shortcut "Captura rápida"** (PENDENTE — próxima sessão)
4. **Cowork com Claude** (já ativo via MCP ClickUp, sem Zapier)

### Briefings & Review (leitura)
1. **Daily Briefing** — todo dia útil 7h via scheduled task no Cowork
   - Coleta: Gmail (não-lidos 24h, focar AFS/Wagner/Vanessa/Bruno Mussa/Cintia/Odair/Francisco) + ClickUp (tasks de hoje + atrasadas, space Sacchelli) + Calendar (eventos do dia) + Vault GSR (2 logs mais recentes)
   - Output: 4 blocos × máx 250 palavras: Foco do dia (3 prioridades) · Compromissos · Decisões esperando · Atrasados/risco
   - Próxima execução: segunda 18/05 7h
2. **Weekly Digest** — sexta 17h
   - Coleta: ClickUp fechadas/abertas/atrasadas da semana + Gmail (sem resposta) + Vault GSR (logs recentes) + status do steel-market-intel-weekly
   - Output: 5 blocos × máx 400 palavras: Fechamentos · Aberto/atrasado · Decisões registradas · Pendências externas · Prioridades próxima semana
   - **Primeira execução: HOJE 15/05 17h (~6h após esta sessão fechar)** — vai ser o teste real
3. **Steel Market Intel** — segunda 8h02 (já existia, mantida)

### Princípios dos prompts dos briefings
- Conselheiro C-Level, sem floreio
- Brutal honesty sobre prioridade (se 2 dos 3 podem ser delegados/cancelados, diga)
- Não inventar tasks (só apresentar o que veio das fontes)
- Se semana foi improdutiva ou produtiva-demais-overload: dizer

---

## Vault GSR ↔ ClickUp — convenção pra não duplicar

| Onde | Pra que serve |
|---|---|
| **Vault Obsidian (GSR/)** | Decisões estratégicas, contexto, análises, logs de sessão, documentação técnica. Permanente, busca por conteúdo, fácil refatoração. |
| **ClickUp** | Tasks acionáveis com dono+prazo. Status muda. Filtro por contexto/tag. |
| **Como ligar** | Tasks ClickUp críticas linkam pro log do vault no campo descrição (`URL: obsidian://...` ou caminho do arquivo). Decisão estratégica é registrada UMA VEZ no vault, e a task no ClickUp é "executar a decisão X registrada em [link]". |

---

## Pendências e próximas sessões

### Manual (Gustavo, ~2 min no UI ClickUp)
- [ ] Apagar Folder Sacchelli/Comercial vazio (clique direito → Delete)
- [ ] Apagar Folder Sacchelli/Marketing vazio (clique direito → Delete)

### Próxima sessão Cowork (~1h)
- [ ] Migrar Lists antigas (Central, Marketing, GRU, CXJ) — criar Lists espelhadas dentro dos Folders novos, copiar 17 tasks, apagar legacy
- [ ] Padronizar Status customizados across Spaces (📥 🎯 🔄 ⏸ ✅)
- [ ] Criar Tags padrão no workspace (@email, @call, @leitura, @decisão, @aguardando, @5min, @profundo)
- [ ] Apple Shortcut "Captura rápida" pro iPhone — gerar JSON + instruções
- [ ] Atualizar CLAUDE.md com seção "Sistema Operacional Pessoal" pra próximas sessões saberem o contexto

### Próximos 60 dias (Gustavo + revisão Cowork)
- [ ] Ler o weekly digest hoje 17h e dar feedback (calibrar prompt)
- [ ] Operar o sistema por 30 dias com daily/weekly funcionando
- [ ] Avaliar: hábito pegou? Inbox estável? Tasks atrasadas <5?
- [ ] Decisão Zapier: cancelar downgrade (manter Pro) OU migrar pra Make Free/N8N

---

## Reflexão estratégica

Em 3 horas resolvemos 3 coisas grandes:
1. **Revelei que o Zapier era cobrança fantasma** — US$ 240/ano pra 0 tasks billable, com downgrade já agendado quebrando os 2 Zaps
2. **Limpamos 75% do ClickUp** que era ruído puro de um agente AI descontrolado
3. **Montamos infra de ritual** (daily 7h + weekly sexta 17h) que substitui hábito por automação

**Mas a parte difícil ainda é o Gustavo.** Sem ler o briefing quando chegar segunda 7h e responder, repete o ciclo de capture sem revisão. **Sistema vive ou morre no primeiro toque.**

Sugestão final dada: separar 30 min sábado pra criar os Folders, validar o weekly digest que sairá hoje, e fazer o primeiro daily briefing acontecer segunda. Esse "primeiro toque" determina o futuro do sistema.

---

## Arquivos produzidos nesta sessão

1. `[Workspace ClickUp]/Manual do Sistema Operacional — Sacchelli + Pessoal` — manual de uso pra cada Folder, convenções, rituais
2. `[Workspace Cowork]/Auditoria_Zapier_Migracao_N8N.md` — análise da conta Zapier e opções de migração
3. **Este arquivo** — fluxo completo, decisões, lessons learned, sistema operacional

## Scheduled tasks criadas
- `daily-briefing-gustavo` — cron `0 7 * * 1-5`, prompt detalhado em /Users/gustavosacchelli/Documents/Claude/Scheduled/daily-briefing-gustavo/SKILL.md
- `weekly-digest-gustavo` — cron `0 17 * * 5`, prompt detalhado em /Users/gustavosacchelli/Documents/Claude/Scheduled/weekly-digest-gustavo/SKILL.md

## Status final (15/05/2026 EOD)
- ClickUp: 17 tasks legítimas, 2 Spaces, 9 Folders, 18 Lists, 2 Inboxes
- Zapier: Pro ativo, 2 Zaps ativos, downgrade pra Free em 11/nov/2026 ainda pendente de decisão
- Cowork: 3 scheduled tasks ativas (daily, weekly, steel-market)
- Vault GSR: este log + outros estratégicos
- Pendência crítica: primeiro weekly digest hoje 17h (teste real do sistema)
