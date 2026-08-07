---
data: 2026-08-07
tipo: log
status: vigente
---
# Auditoria do time Stalo — painel de 5 especialistas

**Pedido do Gustavo:** *"quero que o time funcione, atualmente está uma bagunça.
convoque o time de arquiteto, redator, engenheiro, design, arte, para avaliar a
estrutura atual, se necessário redefinir a arquitetura, comandos, processos,
estratégia, ferramentas de cada agente, objetivos, monitoramentos."*

**Método:** 5 especialistas independentes (arquiteto, engenheiro de
confiabilidade, diretor editorial, diretor de design, estrategista) leram o
espelho, o runbook `~/dev/stalo-restore`, o vigia e os logs. Cada diagnóstico
foi confrontado por um cético com mandato de derrubar o que não se sustenta.
Síntese arbitrada. 11 agentes, 241 verificações.

## O diagnóstico em uma frase

**Nada do que o time faz vira arquivo — então o passo seguinte não consegue ler,
e o Gustavo não consegue verificar.** Não é falta de agente, prompt ou
ferramenta. É ausência de estado e de prova.

## A causa raiz do espelho travado — erro do Claude, não da Hostinger

`origin/main` está em **`a6b117b`**, commit feito **por mim no Mac em 05/08
14h43**, cinco minutos depois do último push da instância (`ec88537`, 14h38).
O `mirror-stalo-workspace-md.sh` faz `git add → commit → push` **sem
`fetch`/`rebase`**. Desde então todo push do VPS é non-fast-forward → `exit 1` →
job `stalo-workspace-md-mirror` em `error`. Recriar o cron nunca resolveria.

Consequência dupla: **os SOUL customizados de Radar e Tech nunca chegaram aos
agentes** — foram escritos no espelho, que é a ponta de LEITURA. O Radar, único
produto consumido diariamente, segue com voz genérica. E o `rsync --delete` os
apagaria assim que o push voltasse.

Ficou registrado em `~/dev/stalo-vault/LEIA-ME.md` (deliberadamente não
commitado — commit a mais agrava a divergência).

## O que o placar de produção escondia

O Pixel **produziu**: commit `b5ba9d4` (29/07), 8 PNGs 1080×1350 com a paleta e
o grid do `KIT.md` aplicados. O `rsync --include='*.md' --exclude='*' --delete`
do espelho os apagou **20 horas depois** (`f537f63`). O log de 04/08 contou a
semana como "1 kit do Pixel". **Aposentar agente por defeito de encanamento é o
erro de reinstalar o OpenVPN 24 vezes** — a arte está recuperável em
`git show b5ba9d4:artes-preview/slide-01.png`.

Mesmo padrão no Gio: o rascunho de estreia (29/07) está pronto, bem escrito, e
**nunca foi publicado**. O gargalo não é produzir — é publicar e registrar.

## Decisão de fundo

**O time continua com 5, a agenda encolhe de 6 rotinas para 3 de produção, e
tem data de morte em 03/09.** Cortar para 3 já foi recomendado e vetado duas
vezes (04/08; `infra/crons.md`) — recomendação sem mecanismo não muda nada.

Quem tem relógio: **Radar** (boletim seg-sex 8h) · **Stalo** (pauta seg 10h,
retro sex 17h) · **Gio** (rascunho ter/qui 11h). Sem relógio, e certo assim:
**Pixel** (acionado pelo Gio) e **Tech** (sob demanda + 1 pergunta na sexta).
Infra é determinística: **infra não depende de modelo** — em 04/08 as duas
pernas de LLM caíram e o healthcheck caiu junto.

## Arbitragens (divergências entre especialistas)

| Divergência | Veredito |
|---|---|
| Matar o heartbeat, tudo em cron | **Ninguém sabe qual mecanismo existe** — o `RESTORE.md` testou e registrou que `openclaw cron` não existe neste produto, e o vigia cita `cron list` com saída real. Provar antes de mover. |
| "Heartbeat morto desde 05/08" | Refutado — foi ligado 09h15 de quarta; na janela observável nenhuma rotina era elegível. Arquivo vazio ≠ morte. |
| Congelar Tech, Gio e Pixel | Refutado — o Tech é o único posto que enxerga em qual perna de modelo o time rodou. |
| Baixar para 1 post/semana | Refutado — zero dado. |
| Checar kit por pixel do PNG | **Refutado por teste** — reprova 5 dos 8 slides, inclusive os corretos (antialiasing). Só é medível no SVG-fonte. |
| Pixel vira script | Adiado — dias de trabalho sobre capacidade nunca vista rodar duas vezes. |

## Onde mora o estado (3 arquivos, todos `.md` de propósito)

O rsync é `--include='*.md' --exclude='*'` — um `.json` nunca atravessaria o
canal e seria relatório invisível.

1. `main/CALENDARIO.md` — fila de pauta com a **frase literal de aprovação do
   Gustavo**. Estados: proposta → aprovada → rascunho → arte → publicada | morta.
2. `main/PULSO.md` — uma linha por despertar do heartbeat ("o relógio gira?").
3. `main/ROTINAS_FEITAS.md` — ledger, **depois** que o inventário declarar o dono
   de cada rotina (hoje o heartbeat o usa como dedupe: um cron escrevendo lá
   *silencia* a rotina em vez de registrá-la).

**Fonte da verdade: o arquivo que chegou ao Mac pelo espelho — nunca a mensagem
do agente.** A plataforma já mentiu nas duas direções: confirmou um cron com
nome, agenda, canal e UUID inexistentes, e relatou falha num push que estava no
GitHub. Confere-se o efeito, nunca o relato.

## Config que se desfaz sozinha — 4º caso

OAuth morto por update (28/07) · modelo default trocado por restart (29/07) ·
instância apagada (04/08) · cron sumido do scheduler (06/08). Mecanismo sempre
o mesmo: **o que não é verificado deixa de existir em silêncio.** Resposta:
`inventario.yaml` declara rotina/dono/id; um job determinístico publica
`_ESTADO/estado.md` antes do espelho; reconciliador no Mac cospe
FALTA/SOBRA/DIVERGE. E o `main/MEMORY.md` **para de afirmar infraestrutura** —
hoje declara 4 crons ativos, três comprovadamente inexistentes, e é lido em
todo turno.

## Critério de morte

**03/09/2026** — último dia da garantia de reembolso do plano (pago até
04/08/2028). Depois disso o custo vira afundado.

**Critério único: ≥ 4 posts PUBLICADOS até lá.** Publicados pelo Gustavo no
LinkedIn, não entregues pelo Gio. É a única métrica que não se falsifica: não
depende de registro auto-escrito pelo agente, não depende de gesto diário, e se
confere fora do servidor. **Sem número apurado até lá = falhou por definição.**

⚠️ Pendência de 5 minutos: `grep 'R$'` no `RESTORE.md` inteiro **não devolve o
preço do plano**. Não dá para pesar benefício contra número que ninguém anotou.

**Morte parcial (retro da sexta que vem):** Pixel com template commitado + 1
carrossel entregue + 1 linha de memória. Três sim = fica.

## Relacionado

- `Logs/2026-07-28 — Stalo no Hostinger + time de agentes (Radar e Torno).md`
- Runbook: `~/dev/stalo-restore/RESTORE.md`
- Documento completo do painel: `~/dev/stalo-restore/REDESENHO-2026-08-07.md`
