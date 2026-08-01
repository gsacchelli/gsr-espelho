---
data: 2026-05-03
tipo: implementação + ferramenta de gestão
projeto: Painel Comercial RAF — Cockpit Pricing Review semanal (instrumentação Decisão 1+3 Wagner)
status: código aplicado, pendente Gustavo rodar `--painel-raf` (~8 min) e validar
relacionados:
  - "[[Logs/2026-04-30 — One-Pager Decisões Wagner (esta semana)]]"
  - "[[Logs/2026-04-30 — Plano Pricing Discipline Tabela Preta (Sacchelli)]]"
  - "[[Logs/2026-04-30 — Reestruturação Painel Comercial RAF (UX executivo + Estoque + PDF)]]"
---

# 03/05/2026 — Cockpit Pricing Review semanal no Painel Comercial RAF

Sessão curta de instrumentação. Briefing pricing review semanal começa segunda 05/05 8h-9h (Plano Pricing Discipline). Sem cockpit, vira reunião de PDF estático com dado semana atrasada. Com cockpit, vira gestão ativa de R$ 200-400k/mês de margem que para de vazar (Decisão 1+3 do One-Pager Wagner).

Trabalho executado em janela única, escopo contido.

## O que foi feito

### Backend — `MotorAnalitico/raf/painel_aggregator.py`

Mudança cirúrgica no bloco que serializa `nfs_preta` (linha-a-linha das NFs Tabela Preta). Adicionados 3 campos por NF:

- **`semana_iso`** — string ISO 8601 `YYYY-Www` derivada de `ABCDAT` (ex: `2026-W18`). Permite agrupamento semanal sem precisar de cubo novo.
- **`mc_pct`** — MC% por linha (`mc_total / valor_liq * 100`). Pra ranquear pior margem dentro da Preta.
- **`flag_bloqueio`** — booleano. `True` quando vendedor é exatamente `Aline Damin Fortes` OU cliente contém `TER BRASIL`. Reflete Decisão 1 do One-Pager Wagner: bloqueio operacional vigente desde 05/05/2026.

Limite da lista subiu **200 → 1000** NFs (Q1/26 tem 485 Preta com perda > 0; 200 não cobria a cauda longa de Aline 155 NFs e Thais 104 NFs). Ainda enxuto JSON (~150 KB extras).

Backward-compat: chave de saída duplicada como `tabela_preta_top200` (legado, agora com 1000) **e** `tabela_preta_top` (alias canônico). Render existente da aba "preta" continua funcionando.

### Frontend — `03_Ferramentas/Painel_Comercial_RAF.html`

Nova **aba principal "💰 Pricing"** após Evolução. Decisão consciente: não virou sub-tab da Carteira porque cockpit é executivo (briefing semanal) e merece nível top na navegação. Não compete com layout 60/40 da Carteira.

Conteúdo da aba (do topo pro fim):

1. **Header com seletor de semana** (dropdown auto-preenchido com semanas ISO presentes em `tabela_preta_top`, mais recente primeiro) + botão **📋 Copiar pro briefing**.

2. **4 KPI cards** da semana selecionada:
   - R$ Preta semana (com #NFs e #vendedores)
   - Δ vs média 4 semanas anteriores (cor: verde se ↓>5%, vermelho se ↑>5%, amarelo neutro)
   - Perda estimada (vs preço Vermelha) com dif% médio
   - 🚫 Bloqueios na semana (Aline + TER BRASIL) — card fica vermelho se >0

3. **Trend semanal R$ Preta últimas 12 semanas** — barras + média móvel 4-sem (linha pontilhada azul tracejada).

4. **Trend mensal %Preta últimos 12 meses** — linha vermelha + bandas verde (8% meta 90d Plano Pricing) e amarela (12% atenção). Usa `cubo_main` mensal — não precisa de agregação semanal.

5. **Top 30 NFs Preta da semana selecionada** — ordenadas por perda. Linhas com `flag_bloqueio=true` aparecem com fundo vermelho-pálido + ícone 🚫.

6. **Vendedor × últimas 4 semanas** — tabela cruzada com R$ Preta + #NFs por célula, coluna final "Δ WoW" comparando semana corrente vs anterior. Aline Damin Fortes destacada em vermelho.

7. **🚫 Bloqueios operacionais ativos** — card com borda vermelha listando todas as NFs Preta de Aline ou TER BRASIL na semana selecionada. Inclui banner de total (NFs + R$ + perda). Se zero, exibe ✓ verde "nenhuma violação".

### Botão "📋 Copiar pro briefing"

Gera markdown formatado e copia pro clipboard (pronto pra colar em e-mail/WhatsApp do briefing 8h):

```
*Pricing Review — semana DD/MM-DD/MM (YYYY-Wnn)*

R$ Preta: R$ X.XXX (N NFs)
Δ vs média 4-sem: ↑ X,X%
Perda estimada: R$ X.XXX (dif% médio X,X%)

🚫 N NF(s) bloqueio violado (Aline/TER BRASIL) — perda R$ X,Xk

*Top 5 ofensores da semana:*
1. Vendedor → Cliente · -X,X% · perda R$ Xk
...
```

## Decisões metodológicas

### Por que **valores absolutos** (não %) na semana

%Preta exige R$Total como denominador. `cubo_main` agrega por mês, não semana. Tentar dividir Preta-semanal por receita-mensal escalada produz métrica frágil. Em vez disso:

- **Métrica semanal**: R$ absoluto + Δ vs média 4-sem. Direto, defendível, capta atividade e tendência.
- **Métrica mensal/trimestral**: %Preta no chart de 12 meses (essa sim divisão correta de cubo_main). Termômetro de longo prazo da meta 8%.

Ambas convivem no mesmo painel sem ambiguidade.

### Por que aba principal (não sub-tab da Carteira)

Briefing semanal é compromisso recorrente top-of-mind. Esconder dentro da Carteira viraria fricção mental (clica → muda sub-tab → procura). Aba principal: 1 clique, sempre lá.

A Carteira segue dona da visão "estado da carteira" (BCG + tabela top 200 + detalhe cliente). Pricing é **fluxo operacional**, não retrato de carteira.

### Por que `flag_bloqueio` no aggregator (não no JS)

Padronização. Bloqueios mudam com decisão executiva (Wagner aprovou Aline/TER em 30/04; pode incluir Fabiola Cardoso Piazza em 30 dias se PIP não dar resultado). Centralizar no Python:

- 1 lugar pra ajustar quando bloqueio mudar
- Lista vai pra logs/auditoria já marcada
- JS é dumb (só lê flag)

Quando 3ª pessoa entrar no bloqueio, edita-se 1 linha no aggregator e roda `--painel-raf`. Não exige mexer em HTML.

## Como Gustavo valida

```bash
# 1. Re-rodar motor pra reinjetar PD com novos campos (semana_iso + mc_pct + flag_bloqueio)
cd "/Users/gustavosacchelli/Documents/Personal/00. Projetos - Claude/Planejamento Estratégico - Comercial"
python3 MotorAnalitico/main.py --painel-raf
# Espera ~8 min (4 RAFs × ~2min cada)

# 2. Abrir o painel atualizado
open 03_Ferramentas/Painel_Comercial_RAF.html

# 3. Clicar na aba "💰 Pricing" (nova, à direita de Evolução)
# 4. Selecionar a semana mais recente no dropdown
# 5. Conferir KPIs, charts, top NFs, tabela vendedor x semana
# 6. Clicar "📋 Copiar pro briefing" e colar em algum lugar pra ver o markdown gerado
```

**Checklist de validação:**

- [ ] Aba "💰 Pricing" aparece na nav
- [ ] Dropdown "Semana" lista semanas ISO (mais recente primeiro)
- [ ] 4 KPI cards renderizam (mesmo se zero em alguma semana)
- [ ] Chart "R$ Preta últimas 12 semanas" mostra barras + linha tracejada média móvel
- [ ] Chart "% Preta últimos 12 meses" mostra linha vermelha + bandas 8% verde / 12% amarela
- [ ] Tabela top NFs da semana lista até 30 linhas, NFs Aline/TER com fundo rosado + 🚫
- [ ] Tabela "Vendedor × 4 semanas" lista top 20 vendedores ordenados por R$ semana atual
- [ ] Card "🚫 Bloqueios operacionais ativos" no rodapé funciona (vermelho se >0, verde ✓ se zero)
- [ ] Botão "📋 Copiar pro briefing" copia markdown formatado pro clipboard

**Possíveis bugs a procurar:**

- Semana ISO conta semana errada se ABCDAT vier em formato `DD/MM/YYYY` em vez de `YYYY-MM-DD`. O parse usa `datetime.strptime('%Y-%m-%d')`. Se quebrar, semana_iso fica `''` e a NF não entra no cockpit. Vai aparecer no console.
- Chart.js consome canvas só quando aba ativa. O `requestAnimationFrame(aplicar)` no handler de tab já cobre isso (mesmo padrão das outras abas).
- `navigator.clipboard.writeText` exige HTTPS ou localhost ou origem `file://`. Se browser bloquear, fallback abre `alert()` com o conteúdo.

## Próximas iterações (parqueadas)

1. **Filtro de gerência no cockpit** — hoje cockpit mostra empresa toda. Pra Felipe Sória ver só Matriz, Fabiola só Fabiola, etc. Aproveitaria filtros globais (`f-ger`).
2. **Comparativo YoY na semana** — "esta semana este ano vs mesma semana ano passado". Útil pra calibrar sazonalidade.
3. **Email automático segunda 7h** — agendar `--painel-raf` + envio do markdown gerado direto pro grupo Pricing Review (Gustavo + 5 gerentes). Cron + script de envio.
4. **Quando workflow Softcomp de aprovação entrar** (Decisão 3, vigência 11/05): adicionar coluna "Aprovador" / "Status aprovação" no top NFs — mostra quem deixou passar a Preta. Hoje a info não existe no RAF.
5. **Adicionar Fabiola Cardoso Piazza ao bloqueio** — se PIP de 30 dias não der resultado (avaliação 04/06). 1 linha no aggregator.
6. **Painel exporta CSV/PDF do briefing** — hoje só copia markdown. Pra ata semanal arquivada no vault precisaria PDF dedicado.

## Arquivos alterados

- `MotorAnalitico/raf/painel_aggregator.py` — bloco `nfs_preta.append({...})` (L278-298 → L278-318) com 3 campos novos. Limite top 200 → 1000. Alias `tabela_preta_top` no return.
- `MotorAnalitico/main.py` — print de status atualizado.
- `03_Ferramentas/Painel_Comercial_RAF.html` — +22.4 KB. Nav (+1 tab), tab-content "pricing" (~3 KB HTML), bloco JS (~18 KB) com 6 funções novas (`renderPricing`, `_isoSemanaJS`, `_semanaParaSegunda`, `_semanaLabel`, `_ultimasSemanas`, `_semanasDisponiveisPreta`, `_agregarSemana`, `_pctPretaMensal`, `_prCopiarBriefing`).
- `03_Ferramentas/Painel_Comercial_RAF.html.bak.20260502-cockpit` — backup pré-mudança (76 MB).

## Sanity checks rodados

- Marcador `const PD = {…};` ainda único no HTML — motor reinjeta sem problema
- 5 tabs nav × 5 tab-contents matching exato
- 4 funções novas presentes no fonte
- 1 branch `ESTADO.tab === 'pricing'` em `aplicar()`
- Aggregator importa limpo (`from raf.painel_aggregator import construir_painel_data`)
- Bloco JS novo (18 KB / 352 linhas) passa em `node --check` (parse OK)
- Balanceamento de chaves/parens OK (script Python custom)

## Para retomar

Se Wagner aprovar Decisão 1 (bloqueio Aline+TER) e Decisão 3 (workflow alçada Softcomp) na conversa de segunda 05/05:

- **Cockpit já está pronto pra usar no briefing 8h**.
- Acompanhar 4 semanas (até 02/06) pra validar se métrica "Δ WoW por vendedor" pega comportamento certo.
- Em 04/06: avaliar PIP Aline/Fabiola Piazza. Se piorar, adicionar Fabiola Cardoso Piazza ao bloqueio (1 linha no aggregator + reinject).

Se Wagner não aprovar e mantiver alçada atual:

- Cockpit ainda serve internamente pra Gustavo monitorar tendência.
- Mas perde o sentido executivo do briefing semanal — vira só dashboard pessoal.
- Reorientação possível: usar pra apresentação Vanessa/Sérgio (Cenário F Duferco) como evidência de "operação tem instrumentação madura, não é só intuição".

---

## ADENDO 03/05 (mesma sessão) — pivot semanal → mensal

Após primeira validação do cockpit, Gustavo apontou:

1. **Cores do gráfico %Preta confundem.** Linha real em vermelho + linhas de referência tracejadas em verde/amarelo/vermelho disputam atenção visual. Pattern certo: **bandas semafóricas preenchidas no fundo** (verde 0-8%, amarela 8-12%, vermelha 12%+) e linha real em **cinza neutro** com pontos coloridos por zona.
2. **RAF é mensal, não semanal** (atualização D+5 após fechamento do mês). RAF poderia ser diário mas não vale o esforço hoje — futuro só com acesso direto ao BD do Softcomp.
3. **Briefing pricing review semanal** vai ser **discussão de processo** (NFs em aprovação Softcomp, casos abertos por gerente) — não consulta de painel.

### Implicação estrutural

Cockpit semanal estava furado na premissa. "R$ Preta da semana", "Δ vs média 4-sem", "Vendedor × 4 semanas" não fazem sentido se o dado tem defasagem de até 4 semanas dentro do ciclo mensal. Erro meu por não levantar a cadência antes de codar.

### O que mudou nesta segunda rodada

**Cockpit virou mensal.** Insumo da revisão mensal quando RAF do mês fechado entra (D+5), não ferramenta semanal.

- Seletor: Mês (não Semana). Dropdown lista meses presentes na base, mais recente primeiro.
- KPIs:
  - **% Preta do mês** com border colorido pela zona (verde/amarela/vermelha) e fonte 32px destacando o número
  - Δ vs mês anterior (em pp)
  - Δ vs mesmo mês ano anterior (YoY, em pp)
  - 🚫 Bloqueios no mês (Aline + TER BRASIL) com perda agregada
- Chart "R$ Preta últimos 12 meses": barras com cor da zona (verde/amarela/vermelha) por mês — visualmente fica óbvio quando empresa cruzou pra zona ruim.
- Chart "% Preta últimos 12 meses": **bandas preenchidas no fundo** (verde 0-8%, amarela 8-12%, vermelha 12%+) + linha cinza com pontos coloridos. Tooltip mostra zona ao passar o mouse.
- Top 50 NFs do mês selecionado.
- Vendedor × últimos 4 meses (cruzada R$ Preta + #NFs com Δ MoM).
- Bloqueios ativos no mês com lista detalhada.
- Botão "📋 Copiar pro briefing" gera markdown mensal:

```
*Pricing Review — Mar/2026*

% Preta: 15.4% (Destrói margem) · +2.1 pp vs Fev/2026
R$ Preta: R$ 7,58 MM de R$ 49,30 MM total
485 NFs · 38 vendedores · 142 clientes
Perda estimada: R$ XXX (dif% médio -16.3%)

🚫 N NF(s) bloqueio violado (Aline/TER BRASIL) — perda R$ Xk

*Top 5 ofensores do mês:*
1. Vendedor → Cliente · -X% · perda R$ Xk
...
```

### Decisão metodológica

A regra é: **a cadência da ferramenta tem que casar com a cadência do dado.** Quando o dado é mensal, a ferramenta é mensal. Cockpit semanal só faz sentido quando tivermos acesso direto ao BD Softcomp (dado intra-dia) — fica parqueado pra esse momento futuro.

### Briefing semanal segunda 8h

Continua acontecendo, mas é **discussão de processo**:
- NFs em aprovação Softcomp (workflow Decisão 3 quando ativar 11/05)
- Casos abertos por gerente (Felipe/Fabiola/Odair Pira/Odair SC/Roveda)
- Decisões pendentes de alçada
- Status de bloqueios Aline/TER BRASIL

O **painel** entra **uma vez por mês**, no início do mês seguinte ao fechado, como insumo da revisão mensal estruturada (não da reunião semanal).

### Pra Gustavo validar

```bash
# Não precisa rodar motor. Só recarregar:
# Cmd+R no painel aberto
```

Checklist:
- [ ] Aba "💰 Pricing" mostra título "Pricing Review Mensal"
- [ ] Dropdown lista meses (Mar/2026, Fev/2026, ...)
- [ ] KPI %Preta tem fonte grande, border colorido pela zona
- [ ] Chart de R$ Preta tem barras coloridas por zona (cada mês com sua cor)
- [ ] Chart de %Preta tem **fundo verde até 8%, amarelo 8-12%, vermelho 12%+** e linha cinza com pontos
- [ ] Tabela top 50 NFs do mês com Aline/TER em vermelho
- [ ] Tabela "Vendedor × últimos 4 meses" com Δ MoM
- [ ] Botão copiar gera markdown mensal

### Arquivos alterados nesta segunda rodada

- `MotorAnalitico/raf/painel_aggregator.py` — patch anterior (parse multi-formato de data) já estava aplicado, mantém pra próxima rodada do motor.
- `03_Ferramentas/Painel_Comercial_RAF.html` — substituição completa do bloco JS do cockpit (~370 linhas). HTML do tab-content ajustado: header, titles, copy.


---

## ADENDO 03/05 (3ª rodada) — sequência QA + redução B + refatoração

Após revisão técnica completa solicitada, executada sequência de hardening + redução de escopo + uma melhoria estrutural.

### Decisão de escopo da aba Pricing — caminho B (reduzir)

Aba Pricing reduzida a **termômetro minimalista**. Manter só:
1. **Chart de tendência %Preta últimos 12 meses** com bandas semafóricas no fundo (verde 0–8%, amarela 8–12%, vermelha 12%+) e linha cinza com pontos coloridos pela zona.
2. **Lista de bloqueios operacionais** do mês selecionado (Aline + TER BRASIL com perda agregada).

Removidos: 4 KPI cards, chart R$ Preta, top 50 NFs do mês, vendedor × 4 meses, botão "copiar pro briefing".

**Razão**: análise detalhada de NFs/vendedores/clientes já existe em DRE Gerencial / Carteira (top 200 NFs Preta) / Evolução. Aba Pricing duplicava conteúdo. Reduzida vira **termômetro** focado: "estamos saindo da zona ruim?" + "alguém violou os bloqueios?". Nada mais.

JS: 18 KB → 6.7 KB. HTML: -13 KB. Mais simples de manter, mais óbvio de interpretar.

### Wrapper genérico de erro pra todas as abas

Adicionada função `_safeRender(tabId, fn)` que envolve render de cada aba em try/catch. Se erro ocorrer, banner vermelho aparece no topo da aba com a mensagem e o stack vai pro console — o resto do painel continua funcional. Aplicada em todas as 5 abas via `aplicar()`.

Antes: erro JS em qualquer aba quebrava o painel inteiro silenciosamente.
Depois: erro fica isolado e visível.

### `requirements.txt` + `README.md`

- `MotorAnalitico/requirements.txt` agora declara: openpyxl, PyYAML, pandas, numpy
- `README.md` na raiz do projeto (não havia) com setup, fluxo operacional, painéis disponíveis, política de dados, confidencialidade, caveats conhecidos
- `.gitignore` criado: exclui `painel_data.js`, backups `*.bak.*`, `output/`, `__pycache__/`, `.venv/`

### Bloqueios pricing em config YAML

Antes: vendedores e clientes bloqueados hardcoded em string literal no `painel_aggregator.py`.

Depois: `MotorAnalitico/config/bloqueios_pricing.yaml`:

```yaml
vigente_desde: 2026-05-05
proxima_revisao: 2026-06-04
vendedores_bloqueados:
  - "Aline Damin Fortes"
clientes_substring:
  - "TER BRASIL"
```

Aggregator carrega via `_carregar_bloqueios()` no início de `_agregar_arquivo`. Match exato em vendedor + match por substring upper em cliente. Quando Wagner adicionar Fabiola Cardoso Piazza ao bloqueio em 04/06: edita 1 linha no YAML, roda `--painel-raf`, painel atualiza. Sem código tocado.

### Schema versionado

`SCHEMA_VERSION = 'v3-2026-05-03'` constante no aggregator. Incluído no return de `construir_painel_data()` como `schema_version` no top-level do JSON. JS no boot valida `PD.schema_version === SCHEMA_ESPERADO` e dispara `console.warn` se desbater.

Bumpear quando adicionar/remover/renomear chave de cubo. Evita classe inteira de bugs como `tab_fech` vs `tabela_fechada` que custou ~30 min nesta sessão.

### Separação JSON ↔ HTML (refatoração estrutural)

**Antes**: Painel_Comercial_RAF.html = 76 MB (template + 75 MB de JSON injetado inline via `const PD = {…};`).

**Depois**: 2 arquivos separados:
- `03_Ferramentas/Painel_Comercial_RAF.html` = **312 KB** (só template + JS de render)
- `03_Ferramentas/painel_data.js` = **73 MB** (`window.PD = {…};`)

HTML faz `<script src="./painel_data.js"></script>` antes do bundle principal. Funciona em `file://` sem precisar servir HTTP (estratégia `<script>` em vez de `fetch()` evita CORS).

**Ganhos**:
1. **Confidencialidade**: compartilhar HTML não vaza dados. Só vaza se mandar também o `painel_data.js` (que está no `.gitignore`).
2. **Performance**: Cmd+R passa a ser instantâneo no template; JS é cacheado pelo navegador depois da 1ª carga.
3. **Manutenibilidade**: editar layout/JS não força regenerar 73 MB.

`main.py` `run_painel_raf` atualizado pra escrever `painel_data.js` separado (não toca mais o HTML do template). HTML fica versionável; `painel_data.js` é gitignored.

### Estado final dos arquivos

```
03_Ferramentas/
├── Painel_Comercial_RAF.html       312 KB  (template — versionável)
├── painel_data.js                  73 MB   (dados — gitignored)
├── Painel_Comercial_RAF.html.bak.20260502-cockpit
├── Painel_Comercial_RAF.html.bak.20260503-restore
└── Painel_Comercial_RAF.html.bak.20260503-pre-split

MotorAnalitico/
├── config/
│   └── bloqueios_pricing.yaml      NOVO — bloqueios em config
├── raf/
│   └── painel_aggregator.py        +SCHEMA_VERSION, +_carregar_bloqueios
├── main.py                         run_painel_raf escreve .js separado
├── requirements.txt                +pandas, +numpy
└── README.md                       (já existia)

README.md                           NOVO — setup, fluxo, painéis, caveats
.gitignore                          NOVO — exclui painel_data.js + backups
```

### Pra Gustavo testar agora

1. Cmd+R no painel já aberto — deve carregar com layout novo, aba Pricing minimalista.
2. Próxima vez que rodar `python3 MotorAnalitico/main.py --painel-raf`, vai gerar `painel_data.js` em vez de re-injetar inline. HTML do template fica intacto.
3. Pra adicionar Fabiola Piazza ao bloqueio em junho: editar `MotorAnalitico/config/bloqueios_pricing.yaml`, rodar `--painel-raf`, pronto.

### Itens parqueados (não vale a pena hoje)

- Extrair CSS inline pra `painel.css` separado (~2h, cosmético)
- Quebrar `painel_aggregator.py` em módulos (~3h, sem teste E2E o risco é alto)

Só atacar quando dor real aparecer (manutenção visual frequente / motor crescendo pra mais responsabilidades).


---

## ADENDO 03/05 (4ª rodada) — Pricing V2 com 4 análises ricas

Após reduzir aba Pricing ao termômetro, Gustavo apontou que ficou pobre demais: "que análises podemos fazer com receita × tabelas × família × região × vendedores?"

Pensei como diretor comercial, listei 7 cruzamentos possíveis, escolhi **bundle de 4** que respondem perguntas executivas distintas que não estão em outras abas:

### Estrutura final da aba Pricing

```
[1. Termômetro — % Preta últimos 12 meses com bandas semafóricas]
[2. Mix de tabelas por mês — stacked bar 100% (Verde/Amarela/Vermelha/Preta)]
[3. Heatmap família × tabela — top 15 famílias com cor por intensidade]
[4. Stoplight vendedor — top 20 com mini-barras de mix]
[5. Pareto da Preta — 3 mini-charts side-by-side (vendedor/cliente/família)]
[6. Bloqueios operacionais — lista do mês selecionado]
```

### Por que essas 4 e não outras

| Análise | Pergunta executiva | Por que aqui (não em outra aba) |
|---|---|---|
| Mix mensal | Como portfolio está deteriorando ao longo do tempo? | DRE Gerencial mostra %Preta única; mix mensal mostra **para onde** a margem está fugindo. |
| Heatmap família × tabela | Em quais famílias a Preta é desastre vs aceitável? | Carteira/Produtos mostra famílias por receita; isso mostra famílias por **disciplina**. |
| Stoplight vendedor | Quem fecha o quê — comportamento sistemático ou pontual? | Lista plana de vendedores não mostra padrão; mini-barras visualizam mix individual em 1 segundo. |
| Pareto da Preta | Concentração compensa ataque cirúrgico? | Plano Pricing Discipline (30/04) tinha esse Pareto em PDF; agora atualiza sozinho. |

### Análises descartadas pra V3 (parqueadas)

- **Família × Região (heatmap geográfico)**: poderoso pra detectar concorrência local (ex: 4140 em Piracicaba vs MATRIZ), mas mais complexo de ler e a região como dimensão é menos prioritária que vendedor/família.
- **Migração de cliente entre tabelas (cohort)**: mostra clientes que "rebaixaram" (Verde → Preta como TER BRASIL); poderoso, mas exige cubo cliente×tabela×ano que não existe direto no aggregator atual.
- **Bubble Vendedor (R$ × MC% × volume)**: redundante com Stoplight (mesma informação, formato diferente).

### Decisões técnicas

1. **Tudo respeita filtros globais**. Helper `_filtrarCuboGlobal(callback)` aplica ESTADO.{ano, mes_ini, mes_fim, gerencia, vendedor, op_cat, considerar} antes de cada agregação. Pareto por cliente usa `tabela_preta_top` (NFs Preta granulares) e replica os mesmos filtros.

2. **Cores padronizadas em `_PR_CORES_TAB`** (Verde, Amarela, Vermelha, Preta). Constante única. Mudar cor = 1 lugar.

3. **Heatmap em HTML + table** (não Chart.js): mais legível com 15 famílias × 4 tabelas (60 células), texto dentro da célula é importante. Chart.js heatmap exigiria plugin extra.

4. **Stoplight em divs flexbox** (não Chart.js): mini-barras são essencialmente uma só barra com 4 segmentos coloridos. CSS resolve mais elegante que Chart.

5. **Pareto em 3 mini-charts side-by-side**: top 5 vendedores, top 10 clientes, top 5 famílias. Linha azul = % acumulado (eixo Y direito); barras vermelhas = R$ Preta absoluto. Padrão clássico de Pareto.

### Tamanhos finais

- HTML: 313 KB → 327 KB (+13 KB)
- JS bloco da aba Pricing: 6.7 KB → 17.8 KB (~600 linhas)

### Pra Gustavo testar

Cmd+R no painel. Aba Pricing agora tem 6 seções verticalmente. Filtros globais (ano, mês, gerência, vendedor) afetam TUDO menos os bloqueios (que tem seu próprio dropdown de mês).

**Cenários de validação:**
- Filtrar Gerência = "Felipe Sória / Fuscão" → ver se Stoplight só mostra vendedores da MATRIZ; Pareto recalcula
- Filtrar Ano = 2025 → comparar mix de tabelas com 2026 (deterioração visível?)
- Conferir se Aline aparece destacada com 🚫 no Stoplight
- Conferir se Heatmap mostra 4140 e 8620 com células de Preta intensa (esperado: alta concentração de Preta nesses aços especiais)
- Conferir Pareto: top 5 vendedores deve concentrar ~43% da Preta (conforme Plano Pricing 30/04)


---

## ADENDO 03/05 (sessão consolidada — fechamento) — Pricing V3 + Due Diligence + Padronização

Sessão excepcionalmente longa fecha em **schema v9** com painel maduro. Resumo do que entrou após os adendos anteriores:

### Pricing V3 — 7 blocos finais

| # | Bloco | Fonte | O que responde |
|---|---|---|---|
| 1 | Termômetro %Preta 12m | cubo_main | Tendência estrutural + filtro família |
| 2 | Mix de tabelas mensal | cubo_main | Como portfolio está deteriorando |
| 3 | Heatmap família × tabela | cubo_main + cubo_transacoes + tabela_preta_top | Em que famílias a Preta dói (com MC% + Itens Tot/Pr + Clientes Tot/Pr + Peso Tot/Pr) |
| 4 | Heatmap cliente × tabela | cubo_cliente_mes_tab | Top 20 clientes por R$ Tab. Preta absoluto (com decomposição) |
| 5 | Stoplight vendedor | cubo_main + cubo_vendedor_cliente_tab | Mix individual + #clientes em Preta + R$ Preta + Itens |
| 6 | Pareto da Preta | cubo_main + tabela_preta_top | 4 charts: gerência / vendedor / cliente / família |
| 7 | Cohort de migração | cubo_cliente_mes_tab | Cliente Preta no mês N → tabela em N+3 (ROI do investimento via desconto) |

### Decisão metodológica fundamental — visão linha em todo lugar

KPI bar do DRE Gerencial usava `cubo_os` (visão "OS predominante" — soma 100% do valor da OS pela tabela com maior parcela). Stoplight Vendedor usava `cubo_main` (visão "linha" — agrega cada linha individualmente). Para Elaine isso dava 31% (KPI) vs 28% (Stoplight) — **incoerência matemática** que apareceu durante uso.

**Decisão**: TODOS os blocos do painel usam visão linha. Pricing é decidido linha-a-linha (cada item da NF é precificado individualmente), painel reflete isso. Visão OS predominante removida do KPI bar. Contagens distintas (n_os, n_nfs, n_cli) seguem vindo do cubo_os.

### Decisão de paradigma — alocação de alçada vs auditoria de vazamento

Gustavo confirmou que TODA venda Preta passa pela mesa dele com critério estratégico (estoque, cliente, concorrência). Isso muda diagnóstico do painel:

- **Antes**: framing "auditoria de desconto não autorizado" — implicava vazamento.
- **Depois**: framing "alocação de alçada Preta + retorno do investimento via desconto" — Preta é capital comercial alocado deliberadamente.

Reformulações aplicadas:
- Header da aba Pricing: "Toda venda Preta passa pela diretoria... mapa de alocação de alçada e retorno do investimento via desconto."
- "Pareto da Preta" → "Alocação da alçada Preta — onde sua aprovação está concentrando".
- Cohort de migração responde "esse meu investimento Preta tá funcionando?": migração pra Verde/Amarela = fidelizou; repetição em Preta = subsídio perpétuo.

### Due diligence completa de cálculos e nomenclatura

Auditoria sistemática identificou e corrigiu:

**Cálculo**:
- KPI bar tab_* via cubo_os (OS predominante) vs Stoplight via cubo_main (linha) — alinhado pra visão linha.
- Clientes únicos Preta por vendedor: era top 1000 NFs com perda > 0 → cubo dedicado `cubo_vendedor_cliente_tab` (dado completo). Elaine subnotificada de 1 → 12 clientes.
- Heatmap família "Itens" e "Clientes": eram totais da família, davam impressão de "só Preta" → formato Tot/Pr.
- ESPECIAIS com -21,2% Preta: causa = devolução de NF previamente em Preta. Heatmap família agora exclui Devolucao.
- Heatmap família "Receita" era ValorLIQ → renomeado pra "Receita Líq." pra clareza.
- Cálculo de R$/kg no KPI bar: usava receita líquida → trocado pra receita s/IPI ("R$ s/ IPI / Kg") com sub mostrando R$ Líq./Kg complementar.

**Nomenclatura padronizada** (vocabulário comercial > jargão técnico):
- M. Agregada → Margem Agregada
- MC % → MC%
- % Tabela Preta → % Preta
- Linhas → Itens (exceto coluna do DRE)
- Vaca Saudável → Vaca Leiteira (alinha com BCG canônico)
- Threshold Operacional → Piso Operacional
- "do recorte" → "do mix" (aba Produtos) ou "no filtro" (outras abas)
- OS / NFs / Clientes (KPI bar) → Qtd. Pedidos / Qtd. NF's / Qtd. Clientes
- Margem do aço: MC Aço (canônico)

### Bugs estruturais corrigidos hoje

1. **`_mesLabel` redefinida em 2 lugares** (Pricing sobrescrevia versão original). Sub-tabs Produtos quebravam silenciosamente, Qualidade do Crescimento sumia. Renomeado pra `_prMesLabel` no bloco Pricing.
2. **`ESTADO.produtos_view` undefined** no boot — ifs `=== 'tabela'` retornavam todos false → sub-tabs Produtos não renderizavam conteúdo. Default explícito.
3. **`renderQualidadeCrescimento` sem dado YoY** — `m` filtrava só ano corrente, função buscava ano-1 e não achava → fallback texto silencioso. Cubo `m_qc` separado inclui ano + ano-1.
4. **Termômetro com filtros globais** — não fazia sentido ano restringir 12 meses históricos. Função `_statsMensaisPorTabelaSemAno` ignora ano.
5. **Heatmap cabeçalho Preta invisível** — cor `#1f2937` sobre fundo escuro. Trocado pra `#9ca3af`.
6. **Heatmap Família × Tabela: cabeçalho Receita desalinhado** + colunas faltavam contexto Tot/Pr. Reformatado.
7. **Stateful early return em renderProdutosAtributos** — `parentElement.innerHTML = "Sem dados"` destruía canvas. Subsequente render com dado de volta não conseguia plotar (canvas inexistente). Trocado por overlay sobre canvas (não destrutivo).
8. **R$ negativo no Heatmap** (Especiais -21,2% Preta) — devoluções com valor_liq < 0. Filtro Op_Categoria != 'Devolucao' adicionado ao heatmap família.
9. **Banner filtros ignorados** — blocos como Geografia, Produtos>Atributos, Cohort, Estoque ignoravam filtros silenciosamente. Helper `_avisoFiltrosIgnorados` mostra aviso amarelo explícito.
10. **Filtros físicos no Estoque** — cubo_estoque é snapshot mas tem aço/perfil/acab/bitola_mm. Helper `_filtrarSkusFisicos` aplica esses filtros mantendo o aviso de que ano/mês/gerência/vendedor/op_cat ignorados.

### Análises de PMP, Heatmap Cliente, Cohort

**PMP (Prazo Médio Ponderado)** — campo `ABCCPGMED` ponderado por ABCTOT — adicionado em cubo_main e cubo_cliente. KPI bar global + card individual do cliente em Carteira mostram PMP com Δ vs média da gerência.

**Heatmap Cliente × Tabela de Preço** — top 20 clientes por R$ Tab. Preta absoluto. Colunas: Receita Líq | R$ Tab. Preta | Peso Tot/Pr | Itens Tot/Pr | MC% | Verde | Amarela | Vermelha | Preta. Filtros físicos + globais aplicam.

**Cohort de migração Preta** — pra cada mês N nos últimos 6 meses, identifica clientes que tiveram Preta como predominante e cruza com tabela predominante 3 meses depois (N+3). Matriz cohort responde "o investimento Preta valeu?" — verde/amarela = fidelizou, Preta repetida = refém.

### Glossário central

Botão **❓ Glossário** no header (ao lado do PDF). Modal completo com 6 seções:
- Métricas financeiras (Receita s/IPI vs Líq, MC Aço, Margem Agregada, MC Total, MC%, PMP, Dif% Vermelha)
- Tabelas de preço (Verde/Amarela/Vermelha/Preta + significados)
- Contagens (Itens, OS, NFs, Clientes, Famílias, Peso)
- Visões e granularidades (linha vs OS, vendido vs partida, considerar análise, devoluções)
- Zonas de cor (semáforos MC% e %Preta + BCG)
- Cubos de dados (12 cubos do PD com explicação)
- Caveats conhecidos

Schema versionado é exibido dinamicamente.

### Bloco "KPIs Secundários DRE" enxuto

Era 10 cards. 6 duplicavam KPI bar (Margem Agregada, %Preta, OS, Clientes, Ticket Médio, R$/kg). Reduzido a **4 cards**: Custo Aço, Custos Diretos Op., Custos de Servir, Conc. Top 10. Vira "decomposição de custos + concentração da carteira" — visão complementar à margem do KPI bar.

### Schema evolution v3 → v9

- v3 (27/04): inicial com cubo_main e demais cubos básicos
- v4 (03/05): +PMP em cubo_main e cubo_cliente
- v5 (03/05): +cubo_cliente_mes_tab (cohort)
- v6 (03/05): +familia em tabela_preta_top (heatmap)
- v7 (03/05): +qtd em cubo_cliente_mes_tab (peso por cliente)
- v8 (03/05): +cubo_vendedor_cliente_tab (Stoplight clientes corretos)
- v9 (03/05): +op_cat em cubos *_tab + valor_sem_ipi/qtd em cubo_cliente + top 5000 NFs Preta

### Estado dos arquivos finais

```
03_Ferramentas/
├── Painel_Comercial_RAF.html       365 KB  (template)
├── painel_data.js                  73 MB   (dados — gitignored, schema v9)
└── *.bak.20260503-pre-split        backup do estado anterior

MotorAnalitico/
├── config/
│   ├── bloqueios_pricing.yaml      Aline + TER BRASIL (vigente 05/05)
│   └── criterios_raf_overrides.yaml
├── raf/
│   ├── painel_aggregator.py        v9, 12 cubos, ~870 linhas
│   ├── exportar_negativos.py       Script standalone pra MC negativa por mês
│   └── (demais inalterados)
└── README.md, requirements.txt

CLAUDE.md                           Atualizado v9 + vocabulário + 12 cubos + banners
```

### Pra retomar

Painel está em **patamar de ferramenta de gestão**, não mais de protótipo. Próximos disparos naturais:

- Rodar `--painel-raf` (~8 min) pra schema v9 popular dado real (PMP completo + cohort + heatmap cliente + clientes Preta corretos)
- QA visual após rodar — abrir cada aba com filtros típicos
- **Pausa de 1-2 semanas** pra usar o painel e descobrir o que falta de verdade
- Recomeçar com lista de fricções concretas, não hipóteses

Análises parqueadas pra V4 ou demanda real:
- Família × Região (heatmap geográfico) — concorrência local
- Material partida no heatmap família — exige expandir cubo
- Auditoria forense top 50 NFs Preta Q1/26 (Plano Pricing item F)

