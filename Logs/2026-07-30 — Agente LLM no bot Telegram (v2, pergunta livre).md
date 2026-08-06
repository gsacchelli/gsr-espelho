---
data: 2026-07-30
tipo: log
status: vigente
---
# Agente LLM no bot Telegram — v2, pergunta livre

**Data:** 30/07/2026
**Contexto:** A v2 prevista no log de 28/07 ("pergunta livre roteada por Claude local usando o runner `stalo_query.py` como única porta de SQL") saiu do papel. Gatilho: Gustavo não gosta dos comandos fixos e quer perguntar em português. Decisão de motor tomada hoje após comparar as 4 alternativas sem cobrança por token.

## Decisão de motor (por que Claude, e por que Sonnet)

| Opção | Veredito |
|---|---|
| **A. Assinatura Claude via `claude -p`** | **ESCOLHIDA.** Zero custo por token (consome limite do plano). Argumento decisivo: o Claude JÁ vê 100% do dado AFS todo dia — nenhuma exposição nova. `--model sonnet` poupa o limite do Opus/Fable das sessões de trabalho; pra pergunta roteada a SQL, Sonnet sobra. |
| B. Gemini (assinatura Google AI Pro do Gustavo) | Descartada. Assinatura de app consumidor não vira API; termos de conta pessoal (mesmo paga) permitem uso do dado pra melhoria de produto — mandaria faturamento/margem/carteira pro Google. Incoerente com a divisão de mundos. |
| C. ChatGPT (assinatura) | Descartada. Sem rota de API pela assinatura (só Codex CLI, agente de código). E a divisão de mundos já crava: ChatGPT/Stalo com ZERO dado AFS. |
| D. Modelo local (Ollama) | Plano B se os limites da assinatura incomodarem. Qualidade pt-BR e roteamento abaixo do Claude. |

**Limitação aceita (de novo):** só funciona com o Mac acordado. Mensagem não se perde (Telegram segura ~24h; bot processa ao acordar). Se incomodar, `pmset` com despertar seg-sex em horário comercial; 24/7 de verdade = lake na nuvem (Fase 2, não agora).

## Arquitetura

```
Telegram (só chat_id do Gustavo)
  → bot.rotear(): "/..." → consultas.py (determinístico, como antes)
                  texto livre → agente_llm.responder_livre()
      → claude -p --model sonnet  (headless, ~15-60s)
          prompt = regras de negócio + esquema do gold (cache por mtime)
                 + MEMÓRIA do vault + últimas 6 Q&A (follow-up funciona)
          única ferramenta: stalo_query.py "SELECT ..." (read-only)
  → resposta em prosa pt-BR no Telegram
```

**Contenção (o coração da coisa)** — testada em `test_agente_llm.py::TestContencao`; regressão nas flags reabre execução arbitrária:
- `--setting-sources ""` — NÃO herda permissões do Claude Code. Achado da sessão: o settings de usuário do Gustavo libera `Bash(python3 -c '*)` = execução arbitrária se herdasse.
- `--allowedTools "Bash(<stalo_query.py>:*)"` — única porta de dados; o guard de 27/07 (SELECT-only, sem read_text/glob/literal de arquivo) vira a fronteira.
- cwd `~/.afs_agente` fora do repo — leitura automática de arquivo não alcança `.env` nem o lake.
- `--strict-mcp-config` com MCP vazio; WebFetch/WebSearch/Write/Edit desabilitados.
- Allowlist de chat_id continua na frente de tudo: só o Gustavo alcança o agente.

## "Aprendizado" (sem treinar modelo)

- **Memória curada no VAULT** (decisão do Gustavo em sessão: Obsidian, não repo): `Sistema Operacional Comercial/08 Agente Analítico/03 - Memória do Agente Telegram.md`. `/aprender <fato>` grava; `/memoria` mostra; editável à vontade no Obsidian (inclusive celular). Injetada em todo prompt. iCloud fora → agente segue sem memória (degrada, não quebra).
- **Histórico** `lake/meta/agente_livre.jsonl`: toda Q&A com duração e flag de erro. Últimas 6 entram no prompt como conversa recente. Serve de matéria-prima pra curadoria periódica (mesma lógica da recalibração do score do Cockpit).

## Validação (30/07)

- Headless contido, ponta a ponta: "data mais recente + pedidos distintos 2026" → correto em 16s.
- Pergunta composta com memória: "pendente da WEG hoje + faturamento no ano" → "Pendente R$ 119,4 mil (11 itens) · Faturamento 2026 R$ 7,3 MM, 565 t" em 14s, aplicando 'pendente = cotações' e WEG por contém.
- Suites: 14 novas (contenção/memória/roteamento) + 25 do bot, verdes; `make ci` ganhou o alvo.
- LaunchAgent `com.sacchelli.telegram-lake` reiniciado com o código novo — em produção.

## Adendo (mesmo dia) — o agente virou FLORI, com vault e base técnica

**Nome: Flori** (homenagem a Florivaldo Sacchelli, fundador) — escolhido pelo Gustavo entre 13 opções; argumento: nome de pessoa > nome de conceito pra um chat diário, e a homenagem carrega a história da casa. "Forja" foi vetado por colidir com o Projeto Forja do Time de Inovação.

**Escopo ampliado (pedido do Gustavo): agente analítico E técnico.** Duas fontes de conhecimento entraram em LEITURA via `--add-dir` (escrita segue bloqueada; quem escreve é o /aprender):
1. **Vault GSR inteiro** — decisões (Logs/), docs do sistema comercial, e a nova **`09 Base Técnica do Flori/`**: semeada com `01 - Peso Teórico e Conversões` (fórmulas por perfil, pol↔mm, dureza HRC↔HB) e `02 - Equivalência de Aços SAE×DIN×W.Nr` (mix AFS, com ressalva de aproximação). Normas e catálogos: é só depositar arquivo na pasta (md ou pdf) — o Flori enxerga sozinho. Regra fiscal continua exigindo fonte primária (o prompt carrega a política).
2. **`06_Docs/` do repo** — revisões/auditorias. Incluído depois que um teste real mostrou a lacuna: a decisão da FCF (R$ 1/kg placeholder) está documentada no repo, não no vault.
   ⚠ Lição de doutrina: decisão registrada SÓ no CLAUDE.md do repo é invisível pro Flori — decisões relevantes devem ter log no vault (que é a regra da casa de qualquer forma).

**Nota consciente de privacidade:** "vault inteiro" inclui notas estratégicas (Duferco, carreira). O caminho continua Mac → Telegram → Gustavo (allowlist), mas Telegram não é E2E — mesma ressalva aceita em 28/07 pro dado nominal. Se incomodar, é 1 linha restringir o add-dir ao sub-vault Sistema Operacional Comercial.

**Ajustes de prompt que os testes reais forçaram:** (1) ordem de busca — pergunta de decisão/definição greppa conhecimento ANTES de SQL (sem isso, foi direto pro gold e não achou a FCF); (2) anti-âncora — "conversa recente é contexto, não verdade; se o Gustavo insiste, refaça a busca" (sem isso, repetiu a conclusão errada do histórico); (3) allowlist do Bash tolera `python3 <stalo_query>` (o modelo às vezes prefixa o interpretador e caía em negação de permissão).

**Validação final:** peso de barra Ø8"×6m = 1.527 kg + equivalente DIN 42CrMo4 citando a Base Técnica (19s); decisão FCF encontrada com as 3 razões e fonte `Revisao_Cockpit_Cotacoes_2026-07-28.md` linha 425 (53s). 42 testes verdes; LaunchAgent reiniciado.

**Renomeio no @BotFather (exibição do bot no Telegram) é gesto manual do Gustavo.**

## Pendências

- [ ] Gustavo: renomear o bot no @BotFather pra Flori (parte visual; o código já é Flori).
- [ ] Depositar catálogo Sacchelli e normas usuais na `09 Base Técnica do Flori/`.
- [ ] Observar consumo do limite Sonnet na prática (se apertar: plano B = Ollama local pro roteamento).
- [ ] Curadoria periódica do `agente_livre.jsonl` → destilar fatos pra memória do vault.
- [ ] Herdada: rotacionar senha SQL Softcomp + migrar segredos restantes do `.env` pro Keychain.

## Adendo 06/08/2026 — /aprender à prova de TCC + 1ª curadoria do histórico

**Bug achado pelo Gustavo:** `/aprender` respondia *"Não consegui gravar no vault (PermissionError) — iCloud fora?"* e **o fato ensinado se perdia**. Causa: o bot roda por LaunchAgent e o **TCC do macOS nega escrita em `~/Library/Mobile Documents` ao Python do venv** (leitura passava — por isso ele LIA a memória mas não gravava). Mesma família da memória `tcc-launchd-icloud`.

**Correção (ordem invertida de propósito):** grava primeiro no **espelho local** `~/.afs_agente/memoria_flori.md` (sempre funciona, fora do iCloud), vault vira espelho best-effort, e `_memoria()` **une os dois sem duplicar** — o ensinamento vale no próximo prompt com ou sem iCloud. `sincronizar_memoria()` sobe o pendente de onde houver permissão (sessão do Claude Code/terminal; o serviço não tem). Princípio: *perder o que o Gustavo ensina é pior que perder a sincronia com o Obsidian.* +3 testes no `make ci`.

**1ª curadoria do `agente_livre.jsonl`** (124 interações, 30/07→06/08). Achado que justifica a memória existir: **"vendas = pedido emitido, não faturamento" foi ensinado TRÊS VEZES** (31/07, 04/08, 06/08) — a janela rolante de 6 Q&A esquecia e ele repetia. Regras destiladas e gravadas:
1. Vendas = pedidos emitidos, NÃO faturamento (RAF/NF).
2. **Pedido nasce sempre de cotação encerrada como Ganha**; divergência cotação×pedido no dia = pedido represado em análise crítica/crédito, não erro de dado.
3. **"Conversão do dia" = pedidos emitidos × cotações encerradas** (não o win rate das encerradas do dia); apresentar as duas e explicar o descasamento temporal.
4. Comportamento: se o Gustavo diz que o número está errado, conferir a MÉTRICA antes de suspeitar de conexão/base (em 04/08 fui checar o SQL e o problema era eu ter dado win rate quando ele queria pedidos).

Memória do Flori agora: **8 fatos**. Curadoria vira rotina — o log é a matéria-prima.
