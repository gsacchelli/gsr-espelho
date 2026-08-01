# Bot Telegram do lake — sucessor do Stalo local

**Data:** 28/07/2026
**Contexto:** Em 27/07 o OpenClaw foi removido do Mac (migrado pro VPS Hostinger com ChatGPT 5.5, assistente "Stalo"). A remoção matou os dois serviços do Stalo local (log 2026-07-25): a consulta de bolso ao lake e o briefing de pedidos 8h (cron do gateway). Este bot substitui os dois — sem OpenClaw e sem LLM no caminho.

## Arquitetura (aprovada pelo Gustavo em 28/07)

- **Long-polling de saída** na API do Telegram (`getUpdates`): o Mac pergunta, nada entra. Zero porta aberta, Mac invisível na internet. Mesmo padrão dos LaunchAgents que puxam do SQL Softcomp.
- **Allowlist dura de chat_id** (8090040277, owner) ANTES de qualquer consulta; mensagem de terceiro é descartada e logada.
- **Comandos determinísticos, sem LLM** → injeção por mensagem não vira SQL. Argumentos entram parametrizados. A guarda `stalo_query.py` (endurecida em 27/07 contra `read_text`/`glob`) fica reservada pra uma futura v2 com linguagem natural.
- **Gold em read_only**, conexão por chamada; lock de escrita do build vira mensagem "lake em atualização".
- **Token no Keychain** (serviço `afs-lake`, conta `TELEGRAM_BOT_TOKEN`) via `segredos.py` — nunca em arquivo.
- **Dado nominal liberado** (diferente do digest cogitado pro Stalo/Hostinger): o caminho é Mac → Telegram → Gustavo, sem OpenAI e sem VPS. Ressalva consciente: chats normais do Telegram não são E2E.

## Componentes

| Peça | Caminho |
|---|---|
| Loop + allowlist | `MotorAnalitico/telegram_bot/bot.py` |
| Comandos | `MotorAnalitico/telegram_bot/consultas.py` |
| Briefing 8h (envia) | `MotorAnalitico/telegram_bot/enviar_briefing.py` (reusa `agente/briefing_pedidos.py` intacto) |
| Testes (16, no `make ci`) | `MotorAnalitico/telegram_bot/test_bot.py` |
| Serviço do bot | LaunchAgent `com.sacchelli.telegram-lake` (KeepAlive on-failure; log `lake/meta/telegram_lake.log`) |
| Serviço do briefing | LaunchAgent `com.sacchelli.briefing-8h` (seg-sex 8h00; dispara no despertar se o Mac dormia; log `lake/meta/briefing_8h.log`) |

## Comandos v1

`/kpi [ano]` (fat/MC ajustada/Preta por mês + YTD) · `/pendentes` (gerência + aging + bloqueios) · `/cliente <nome>` (ficha compacta + pendente hoje; busca contains p/ holdings) · `/top [n]` · `/funil [ano]` · `/estoque` (CRITICO) · `/pedidos` (mesmo texto das 8h) · `/status` (frescor do gold).

Validado em 28/07 contra o gold real: KPI YTD R$ 105,8 MM · 3.335 pendentes R$ 39,5 MM · briefing de seg 27/07 R$ 1.095.471.

## Divisão de mundos (reafirmada)

- **Stalo (Hostinger/ChatGPT)**: assistente genérico, ZERO dado AFS. Digest agregado segue em avaliação — decisão adiada.
- **Bot do lake (este)**: só comandos, só leitura, só Gustavo. Depende do Mac acordado (limite aceito).

## Pendências

- [ ] Gustavo: criar bot no @BotFather + gravar token no Keychain + bootstrap dos 2 LaunchAgents (comandos na sessão de 28/07).
- [ ] Herdada de 25/07, segue aberta: **rotacionar senha SQL Softcomp** (Nelson/Francisco) e migrar segredos restantes do `.env` pro Keychain.
- [x] v2 (se sentir falta): pergunta livre roteada por Claude local usando o runner `stalo_query.py` como única porta de SQL. **FEITO 30/07/2026** — ver log `2026-07-30 — Agente LLM no bot Telegram (v2, pergunta livre).md` (motor: `claude -p --model sonnet` pela assinatura; memória curada no vault via /aprender).

## Adendo 30/07/2026 — briefing parcial + pedido fantasma (incidente e correções)

**Sintoma:** briefing das 8h reportou 29/07 = R$ 105k; Softcomp SP4140 = R$ 492.585,09; portal = R$ 575.685.

**Duas causas independentes:**
1. **Base parcial**: o pull das 7h nunca alcança o SQL (Mac fora da rede AFS de manhã) e só rodava ~11h40 — o briefing das 8h lia o dia anterior INCOMPLETO sem avisar (MAX(data) não denuncia dia parcial). **Correções:** pull movido p/ 7h45; briefing p/ 8h15 e **só envia se o pull rodou HOJE** (decisão Gustavo: parcial não tem valor); senão fica pendente e o próprio `atualizar_pedidos_diario.sh` dispara o envio após a 1ª atualização (trava de 1 envio/dia). Validado em produção no mesmo dia.
2. **Pedido fantasma**: 343024 (SUPERIOR, R$ 83.100) cancelado no ERP e reemitido como 343047 — mas a `BI.Pedido` não expõe situação (cancelar só zera o Saldo). Lake contava os dois; 4 gerências batiam ao centavo e a diferença era exatamente esse pedido. **Correções:** `config/pedidos_cancelados.yaml` (expurgo só com confirmação manual no ERP) + detector de redigitações no pull (mesmo dia+cliente+valor, um saldo zerado → AVISA). O detector pegou METSO 338690→338691 na 1ª rodada — **falso positivo corretamente resolvido** (era faturamento integral, NF 316983 de 13/05/2026): prova de que expurgo automático por saldo teria apagado venda real.

**Pendente (call Nelson):** `BI.Pedido` expor a situação do pedido — correção de raiz.
