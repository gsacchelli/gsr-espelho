---
data: 2026-07-20
tipo: log
status: vigente
---
# 2026-07-20 — Integração SQL Softcomp (Gate 0): desenho da operação

Retomada do acesso ao banco Softcomp pra eliminar o export manual e alimentar o
SAC360 online. Base do e-mail de nov/2024 do Nelson (Softcomp).

## Estado do acesso
- Servidor **10.0.0.215:1433** (SQL Server) responde; banco **SGRA_SACCH**.
- Credencial de 2024 (`SACCHELLI_BI` / senha do PDF) **não loga mais** — erro
  18456 (senha rotacionada em ~20 meses). Driver `pymssql` instalado no venv.
- Próximo passo: Nelson reativa/gera credencial nova (pedir senha nova — a antiga
  circulou por e-mail) → conectar e inventariar tabelas/colunas reais.

## Insight que define a arquitetura
Os exports Excel que importamos são **relatórios formatados** (joins + pivots:
"Nome cliente", "Razão social", "Meses de estoque", "Compras até <mês>"). As
tabelas cruas do banco (ABCxxx) NÃO têm isso. → Pedir à Softcomp **VIEWS SQL que
reproduzam os relatórios** (as mesmas queries dos botões de export), não acesso
às tabelas cruas. Aceitar também o dicionário de dados se ele preferir (dá
autonomia). Modelo é **polling nosso sobre views vivas** — sem export agendado
(tira trabalho do Nelson). Cada view idealmente expõe um **marcador de
atualização** (data/ID) pra puxarmos só o delta.

## Split SQL × Manual (decidido com Gustavo)
**SQL — automatizado:**
| Fonte | Frescor |
|---|---|
| Cotações Pendentes | 30 min |
| RAF · Pedidos · Cotações Encerradas · Estoque · Movimentação · Lista de Clientes | 1×/dia |
| Vendedores/Equipes/Gerentes · Tipos NF · Motivos de Perda | 10 dias |

**Manual — de propósito:**
- **Fases · Famílias** — governança de preço: reajuste de fornecedor / política de
  MC mudam o CUSTO da cotação; revisar antes de propagar (casos Embraço, AQ1).
- **Despesas** (mensal, pós-fechamento) · **DUO · Balanço · PGA** (não são Softcomp).

Anexo-spec: `06_Docs/Solicitacao_Softcomp_Views_SQL_2026-07-20.xlsx` (aba "SQL
(automatizado)" com frescor + marcador; aba "Importação manual"; 1 aba de colunas
por view — 10 views, 352 colunas).

## Cockpit "quase ao vivo" (pendentes a 30 min) — medido
- Gerar o Cockpit isolado: **1,5 s** (é a última milha).
- Cadeia atual `atualizar-cotacoes-pendentes`: **5m39s** — inviável a 30 min
  porque re-enriquece as **285k encerradas** + rebuild total do gold a cada vez.
- Arquitetura-alvo: **refresh pesado 1×/dia** (encerradas/RAF/estoque = ingredientes
  lentos do score) + **caminho enxuto a cada 30 min** (puxa só pendentes novas,
  enriquece só elas, re-pontua contra as tabelas quentes, regenera Cockpit ~<1 min).
  Construir o alvo `--pendentes-only` (pula encerradas + gold leve) quando o SQL entrar.

## Sequência quando a credencial voltar
1. Conectar (pymssql) e inventariar SGRA_SACCH (read-only).
2. Cruzar com as 10 views do anexo → de-para "já tem × falta".
3. Definir com Nelson: views prontas vs dicionário; marcador por view.
4. Construir pulls incrementais + caminho enxuto de pendentes (30 min).
5. Segurança: rotacionar senha; usuário com escopo só nas views.

E-mail ao Nelson: rascunho no Gmail (thread "Re: Banco de Dados - Softcomp"),
anexo em `~/Downloads/`.

---

## Adendo 22/07 — Cockpit AO VIVO ligado (1ª fonte migrada)

- Nelson expôs schema **BI** (10 views) na réplica; credencial reativada.
  Inventário: `06_Docs/Softcomp_SQL_BI_Schema.md`.
- **Pendentes migradas pro SQL**: `sql/pull_pendentes.py` (joins de cadastro,
  UF via CEP, guard de volume <50% aborta) → formato do export manual →
  `enriquecer_pendentes()` isolado → gold → Cockpit. `make cockpit-sql` = **11s**.
- **LaunchAgent `com.sacchelli.cockpit-sql`**: a cada 30 min, seg-sex 6h-20h,
  lock + sai quieto fora da rede. Log: `lake/meta/cockpit_sql_30min.log`.
  Desativar: `launchctl bootout gui/$UID/com.sacchelli.cockpit-sql`.
- Confirmação de dado vivo: itens variando entre rodadas (3.625→3.614→3.615).

### Agenda técnica pra call com o Nelson (o que falta pra migrar o resto)
1. **BI.Cotacao (encerradas)** — faltam **Data de encerramento** (win rate por
   período, ciclo), **Descrição do motivo** e **Concorrente**; sem elas as
   Encerradas seguem no export manual. Tb faltam Prazo de entrega e nome do
   emitente (afeta pendentes: 2 campos vazios hoje).
2. **BI.Clientes** — 14 colunas vs 39 do relatório; faltam p.ex. **Grupo
   Cliente** (overlay do grupo econômico), UF, Ramo de Atividade, situação.
3. **BI.RAF** — de-para 116↔133 colunas a validar campo a campo; **histórico
   2023-25** (Gustavo propôs BD fixo separado pros anos fechados — ideal).
4. **Produto Padrão (estoque) + Movimentação** — views a criar (Nelson pediu ok
   dos parâmetros; Gustavo autorizou usar o usuário dele). Pedir período FIXO
   (ano corrente) em vez de parâmetro de tela.
5. **TiposNF** — view pequena que falta.
6. Rotação da senha `SACCHELLI_BI` + escopo só no schema BI.

**Auditoria de paridade 22/07 (manual 17/07 × SQL, 2.328 cotações em comum):**
núcleo idêntico (cliente/valor/kg/qtd; ~30 divergências = cotações editadas entre
os snapshots, 6 reabertas). Corrigido no pull: faixas da view vêm SEMPRE em R$/kg
→ conversão pra unidade do item (faixa_kg × kg÷qtd, 99,6% de bate); 'PC'→'PÇ'.
**+ Item 7 pra call Nelson:** `FamiliaProduto` da BI.Cotacao devolve `99RV`
("FAMILIA GENERICA") em ~220 itens onde o relatório resolve a família real
(0026/0631/0641...) — degrada score de família e custo de reposição; qual campo
a view usa e dá pra trazer a família resolvida?

---

## Adendo 25/07 — Pedidos migrados (2ª fonte) + histórico de encerradas

**Pedidos Emitidos → SQL** (`sql/pull_pedidos.py`). Gustavo perguntou se devia
enviar planilha semanal; a resposta foi NÃO — a `BI.Pedido` já existia, viva,
atualizada até o dia. Auditoria de paridade (jan-jun/26): SQL é **superconjunto
perfeito** (zero item do lake ausente lá); única diferença sistemática =
**transferência entre filiais** (cliente SACCHELLI-*, 4.390 itens/R$ 64,5M), que
o relatório do Softcomp filtra e o pull passa a filtrar. Resíduo 0,9%.
**Julho estava invisível no portal** (lake parava em 30/06) — agora até 24/07.

**FIX importante (afetava pendentes também):** quantidade nem sempre está na
unidade do PU — item por METRO com qtd em MILÍMETROS fazia a faixa sair 1000×
menor (325 itens). `faixa_na_unidade` agora converte (mm→m, peças×compr→m,
BR≈PÇ) e devolve R$/kg sem converter em combinação desconhecida.

**Cadência decidida:** pendentes seguem a 30 min (11s); pedidos NÃO cabem
(5min: 71s enriquecer + ~4min cross-check) → diário de madrugada + botão sob
demanda. **Otimização à vista:** `BI.Pedido` traz `NumeroCotacao` — o elo
OFICIAL do ERP torna o cross-check por matching dispensável (5min → ~1min, e
mais preciso que nossos 98%).

**Corrida entre sessões:** um `make atualizar-cotacoes` rodando em OUTRA sessão
(carga do histórico 2023-2024) reescrevia o silver enquanto meu build_gold lia →
segmentação zerou temporariamente. Sem corrupção; gold reconstruído depois.
**Ganho:** encerradas passaram de 285k (2025-26) para **671k linhas (2023-26)**
— mais lastro pro score, pro ML e pra segmentação. Pendente: avaliar lock global
no lake pra impedir escrita concorrente.

**25/07 (parte 2) — ENCERRADAS migradas (3ª fonte).** Dois achados do Gustavo
destravaram: (a) concorrente vem do MOTIVO (cadastro mapeia código→descrição
com o nome: '1'=Trefita/Torres, '2'=Açotubo…) — resolve local; (b) data de
encerramento não existe na view, mas merge preserva 90% e anos fechados ficam
intactos. Paridade 2026: Status 100%, cód. motivo 100%, valor 1 divergência.
Julho entrou: cotações até 25/07, WR ajustado calculável no mês corrente.
**RAF NÃO migrado (decisão fundamentada):** BI.RAF está CONGELADA em 30/06
(view montada com "parâmetros do usuário", não dinâmica) → migrar hoje = mesmo
dado, zero ganho; e o de-para exige mapear 133 colunas técnicas (ABCxxx) ↔ 116
amigáveis, na fonte de MARGEM. Desbloqueio = 1 pedido ao Nelson (período
dinâmico). **Pauta final da call: só 3 itens** — RAF dinâmico, DataEncerramento,
views de Estoque/Movimentação.
