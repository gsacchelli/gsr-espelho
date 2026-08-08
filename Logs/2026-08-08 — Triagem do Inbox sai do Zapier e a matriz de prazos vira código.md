---
data: 2026-08-08
tema: sistema operacional pessoal
status: em produção
---

# Triagem do Inbox sai do Zapier e a matriz de prazos vira código

O fluxo Gmail ⇄ ClickUp deixou de depender do Zapier (que quebra em **11/nov/2026**,
quando a conta cai para o Free e o limite de 2 steps mata os dois Zaps de 7 steps).
Tudo roda agora em Google Apps Script, nos servidores do Google — **com o MacBook
desligado e com o celular na mão**. Custo: R$ 0 de infraestrutura, mais ~US$ 0,02 por
rodada de triagem.

Projeto: `Espelho ClickUp-Gmail`, conta **gustavo@sacchelli.com.br**.
Código: `~/dev/automacoes/clickup-gmail/` (a pasta É o projeto; publica com `clasp push`).

---

## A decisão que importa: prioridade não é fato, é política

A **matriz (status × etiqueta → prazo e prioridade)** existia desde maio, mas **não
estava escrita em lugar nenhum** — vivia dentro do step 6 (Code JS) do Zap #1. Ia
morrer em novembro junto com ele. Hoje ela é uma tabela declarativa no código, com o
motivo escrito ao lado de cada linha.

| Status | Etiqueta | Prazo | Prioridade |
|---|---|---|---|
| Responder | WS · CD | 1 dia | Urgente |
| Responder | Comercial · Financeiro · Produção | 2 dias | Alta |
| Responder | outras | 3 dias | Alta |
| A fazer | WS · CD | 2 dias | Alta |
| A fazer | outras | 3 dias | Alta |
| Em progresso | qualquer | 5 dias | Normal |
| Acompanhar | qualquer | 7 dias | Baixa |

Regras que a tabela sozinha não diz e o código precisa saber:
- **A ordem é o desempate** — a primeira linha que casa vence. Tarefa com `_ws` *e*
  `comercial` cai na linha do WS.
- **Dias ÚTEIS.** "Responder + WS = 1 dia" numa sexta à tarde daria sábado.
- **`Completo` fica de fora de propósito**: a tarefa está sendo arquivada.
- **Data escrita no e-mail vence a matriz**, para mais perto ou para mais longe.

**Por que isso saiu do modelo.** Na primeira rodada, com o modelo decidindo prioridade,
ele discordou desta matriz em **4 das 5 tarefas — sempre para mais alarme**: dois
"urgente" que a régua chama de alta, dois "normal" que ela chama de baixa. Não é
incompetência do modelo: prioridade não é um fato sobre o e-mail, é uma política minha.
Pedir a um modelo que infira política é pedir que ele invente uma. Ele ficou só com o
que é julgamento de verdade — o título — e com a data literal do e-mail.

---

## O erro que ensinou a guarda de evidência

A triagem manda o lote inteiro numa chamada só (mais barato, e dá coerência entre
itens). O preço apareceu na primeira rodada real: a data da reunião do Wagner (10/08)
**vazou** e virou prazo de um e-mail sobre retrabalho RTR que **não tinha data nenhuma
no corpo**. Conferido na fonte.

E a simulação da mesma rodada **não tinha o defeito** — ali o item saiu sem prazo. É
erro que passa no teste e chega na tela.

Conserto: o modelo agora devolve, junto com a data, o **trecho literal do e-mail onde
ela aparece**; o código confere que esse trecho existe no texto *daquele* item. Não
bate → data recusada, motivo no log, cai no padrão da matriz.

> **Lição que vale além deste caso:** lote numa chamada só é barato e contamina.
> Quando o modelo extrai um dado pontual, exija a citação da fonte e confira a citação
> contra o texto de origem. O modelo propõe, o código verifica.

---

## O que os marcadores do Gmail realmente são (medido, não suposto)

Levantei os marcadores contra os e-mails reais antes de automatizar. Duas famílias:

**Por remetente/participante — 81% do volume, resolve sem modelo nenhum:**
- `_WS` = `from:wagner@sacchelli.com.br`. **1.877 threads, 63% de tudo.** Não é área da
  empresa, é pessoa — responde "quem", não "o quê".
- `Usinas` = domínio da contraparte (Villares, Gerdau, ArcelorMittal, Simec, Steel).
  ⚠ **É participante, não remetente**: metade é gente de dentro escrevendo *para* a
  usina. Filtro só em `from:` perderia essas.
- `Financeiro` = `from:cadastro@sacchelli.com.br` (Sérgio, análise de crédito).

**Por assunto — precisa ler:** `Arquivo/Tabelas de Preço` tem remetentes todos
diferentes; o que une é "tabela", "reajuste", "proposta em vigor".

⚠ **O marcador é por MENSAGEM, não por thread.** Na mesma conversa, a mensagem do
Wagner tem `_WS` e as respostas dos outros não.

**Defeito achado de raspão:** o mapa de etiquetas da captura tinha 10 entradas para
uma taxonomia de ~20. `TI` tinha **0 mensagens** e `Produção` **1** — letra morta —
enquanto `CD` (Conselho Diretor, 122 threads com o sub-marcador) estava **fora**, e é
linha de topo da matriz. Corrigido, mais herança de sub-marcador
(`CD/Budget FY26` → `cd`, `Comercial/Relatório Visitas` → `comercial`).

*Decisão: classificação automática de marcador de contexto fica de fora por ora — faço
na mão. O caminho, se um dia valer, é filtro nativo do Gmail para os 81% e modelo só
no resíduo.*

---

## Como isso vive

| Peça | Cadência |
|---|---|
| Captura Gmail → ClickUp (cria a tarefa **já com prazo e prioridade da matriz**) | 1 min |
| Sincronia de status nos dois sentidos | 5 min (trava de 2 min) |
| Reconciliação (rede para queda de webhook) | 1 h |
| Triagem — título + data literal, via Anthropic API | diária, 6h-7h |
| Cura de órfãs ativas | semanal, segunda 5h-6h |

**A matriz roda na CAPTURA, não na triagem.** Descoberto usando: uma tarefa nasceu
sem prazo e ficaria assim até as 6h do dia seguinte, esperando uma chamada de API de
que ela não depende. Prazo e prioridade só precisam de status + etiqueta, ambos
conhecidos no instante da captura. O modelo ficou com o que é julgamento.

### As duas redes de segurança

**Alarme de falha repetida.** A ordem do código já garante que criação falha não marca
a thread — o gatilho de 1 min tenta de novo para sempre. Mas *"tenta para sempre"* não
é *"funciona"*: se o token do ClickUp expirar, quebra a cada minuto e o único registro
é um log que ninguém lê. Agora, passadas 3 falhas seguidas, chega um e-mail — uma vez,
e outro quando voltar. O problema nunca foi a falha; era o silêncio.

**Cura de órfãs ativas.** Órfã = thread com o marcador `✓ ClickUp` e sem tarefa. A
captura a ignora para sempre (o marcador é a trava anti-duplicata) — é o único caso do
fluxo que não se recupera sozinho. 🪤 Curar órfã **cega** seria o incidente das
duplicatas por outra porta: as ~47 threads da baseline são órfãs de propósito. O filtro
que separa: **a thread ainda tem marcador de ação hoje?** Se tem, você espera uma tarefa
que não existe — cura. Se não, é inerte — não toca.

`5. Completo` / status `completo` **arquiva** o e-mail, venha de que lado vier.

**Nunca:** cria subtarefa · deleta · fecha tarefa · escreve e-mail. Teto de 15
renomeações por rodada. E o critério de entrada protege o trabalho manual: **só entra
tarefa cujo título ainda é o assunto cru do e-mail** — título reescrito por mim sai da
fila para sempre.

---

## Armadilhas registradas (todas custaram tempo hoje)

1. **Conta errada.** O Apps Script só enxerga o Gmail da conta dona do projeto.
   Criado por engano na conta pessoal, falhava com "e-mail não encontrado" **e sem erro
   nenhum** — caixa vazia é resposta legítima à pergunta feita no lugar errado.
2. **Colar código no editor trunca.** Três vezes num dia. Resolvido com `clasp push`.
   Numa tentativa por injeção o texto chegou **corrompido no meio**, com o mesmo
   tamanho e as mesmas pontas — só o CRC do gzip pegou.
3. **Nome de arquivo tem que bater exato.** Remoto `Código.gs` (com acento), local
   `Codigo.gs` (sem): o push criaria um *segundo* arquivo e as duas cópias declarariam
   as mesmas constantes, quebrando o projeto inteiro.
4. **Trocar o segredo do webhook não basta.** Ele viaja na query string da URL
   registrada no ClickUp. Trocar só a propriedade quebra o espelho **em silêncio**.
   Criada a função `atualizarWebhook()` para reapontar.
5. **`clasp push` sobrescreve o remoto inteiro.** Clonar e comparar antes.

---

## Aberto

- Rodar a matriz de ponta a ponta — hoje a fila estava vazia por construção.
- Compromissos das atas do Plaud virando tarefa (máx. 3 por reunião): desenhado,
  não implementado. Cria tarefas, então é decisão separada.
- Zaps desligados em 08/08. O Zapier morre sozinho em novembro.

Relacionado: [[2026-05-15 — Setup Sistema Operacional Pessoal (ClickUp + Briefings + Triage Zapier)]]
