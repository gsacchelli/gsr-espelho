---
data: 2026-07-17
tipo: log
status: vigente
projeto: Portal SAC360 (afs-lake)
---

# Cockpit de Cotações Pendentes

Pedido do Gustavo: ferramenta única e interativa pra trabalhar as pendentes o
dia inteiro e aumentar conversão baseado em dados — cruzamentos, histórico,
busca por material/região, margem de pacote, estoque, chance de fechamento e
campos qualitativos. Entregue como **HTML standalone** (padrão da casa:
template versionado + dados injetados gitignored), linkado na sidebar do
SAC360 ("🎯 Cockpit de Cotações").

## Arquitetura

- `MotorAnalitico/geradores/gerar_cockpit_cotacoes.py` → lê o GOLD
  (`vw_cotacoes_pendentes` + histórico `vw_cotacoes`/`vw_faturamento`) e gera
  `03_Ferramentas/cockpit_data.js` (~3,8 MB, gitignored).
- `03_Ferramentas/Cockpit_Cotacoes.html` — app vanilla JS, zero libs externas,
  funciona em `file://`.
- Integração: `make cockpit`; encadeado no `make atualizar-cotacoes-pendentes`;
  step "Cockpit Cotações" no build graph (`--cockpit`); testes no `make ci`.

## Score de chance de fechamento (o coração)

Blend em **log-odds** de win rates EMPÍRICOS (encerradas 2025+, disputa real —
já com a régua nova ex-Enc. administrativo), cada componente com **shrinkage**
bayesiano pro global (R$ 300k — cliente com 1 cotação não vira 100%):
cliente (peso 1,0) · posição de preço vs Vermelha por bucket de gap (0,9) ·
família canônica (0,7) · vendedor (0,5) · região/UF (0,3) · penalidade de
aging (>30/60/90d) · bloqueio de pricing → piso 3%. **Breakdown visível no
drawer** ("Por que esse score") — transparência > caixa-preta. Validação de
sanidade: TUP com score 95% = real (R$ 6,5M disputados, 98,4% ganho).

**Valor esperado (EV) = score × valor** é a régua de priorização do dia.

## O que a ferramenta tem

- **Triagem**: tabela com facetas (unidade, gerência, vendedor, faixa, score,
  estoque, ABC, aging, região, tipo, temperatura), busca sem acento, ordenação.
- **Pacotes**: cotação inteira — mix de faixas, R$ vs Vermelha do pacote,
  chance ponderada, EV.
- **Foco do dia**: top 20 por EV ainda SEM próxima ação registrada.
- **Radar**: vendedores/regiões/famílias/clientes (pendente × esperado),
  curva de preço empírica (WR por bucket de gap), distribuição por score.
- **Drawer por item**: ladder de preço F1/F2/F3 com PU posicionado, estoque
  (match/disponível/cobertura), breakdown do score, último GANHO e último
  FATURADO do cliente na família (R$/kg + data), histórico recente do cliente.
- **Qualitativos** (localStorage, backup/restore JSON): temperatura 🔥🌤🧊,
  target do cliente (R$/kg), concorrente (lista canônica), "faz sentido
  brigar?", "preço possível?", próxima ação (tira do Foco), notas. Export CSV.

## Números de estreia (export 17/07)

3.499 itens · 1.056 cotações · R$ 48,6M pendentes · **pipeline esperado
R$ 27,3M** · chance média ponderada 56% · 43% do R$ com estoque na bitola ·
438 PRIORIZAR.

## Caveats e próximos passos

- Engenheirado: R$/kg suprimido (kg = nº de peças — caveat conhecido).
- Notas ficam no NAVEGADOR (localStorage) — backup via 💾; se um dia precisar
  compartilhar entre máquinas, próximo passo natural é persistir no repo
  (JSON versionado) ou no gold.
- Pesos do score são heurísticos documentados; quando houver base suficiente,
  calibrar contra desfechos reais (backtest ganha/perde).
- Fix pré-existente pendente no portal: NAType na Visão Geral (chip aberto).

## Adendo v1.1 (17/07, tarde — feedback do Gustavo em uso)

- Facetas de material no rail: **Aço / Perfil / Acabamento + range de bitola
  (mm)** — o recorte "4140 100–230mm" sai em 2 cliques (336 itens, R$ 4,38M).
- Pacotes: itens ordenáveis por **nº do item / material / valor**.
- **PU na unidade nativa** da cotação (R$/pç, R$/kg, R$/m) ao lado do R$/kg
  convertido pelo peso. Destravado por fix estrutural no pipeline: o Softcomp
  omite o header das colunas de unidade e a leitura descartava — fallback
  posicional (mesmo padrão dos Pedidos); `vw_cotacoes_pendentes` expõe
  `unid_pu`/`unid_qtd` (KG 2.352 · PÇ 1.139 · M 8).

## Adendo v1.2 (17/07, fim do dia)

- **Export de recorte com validade**: botão 📤 gera HTML standalone do recorte
  filtrado (ex.: gerência Felipe → 2.419 itens) pra mandar pro gestor. Dados
  cifrados AES-GCM com chave derivada da validade+rótulo → editar a data no
  arquivo MATA o arquivo; expirado bloqueia; a mecânica do score (pesos, curva,
  WRs por dimensão) NÃO vai no arquivo. Limite honesto documentado: conteúdo
  client-side nunca é 100% protegível (relógio local pode ser voltado; dados
  visíveis valem só pelo prazo).
- **Score recalibrado por backtest** (agente; treino 2025 → teste 2026, 54k
  cotações em disputa real): AUC 0,735, erro de calibração 6,5pp com 10% do R$
  saturado no teto → `W_CLIENTE 1,0→0,7` corta o erro pra 4,7pp (−28%) por
  1,2pt de AUC. Próxima fronteira apontada: banda 20–35% segue ~8pp otimista
  em R$ (candidato: componente de tamanho do item).
- **Dashboard** (primeira aba): cards gerenciais + quebras por gerência/
  unidade/vendedor/região/aço/família/cliente (pendente × esperado), mix de
  faixas, aging, triagem×score — reage aos filtros.
- **Bug corrigido**: "Disponível (bitola)" no drawer mostrava o estoque da
  FAMÍLIA inteira (ex.: 3.048 t) — agora usa `estoque_qtd_kg` da bitola
  matchada (ARCO 63,50 → 56,4 t). Família continua exibida ao lado.
- Drawer: conversão **Cliente NESTA família** + **mediana regional das ganhas**
  (uf×família); ladder com marcadores "últ. ganho cli." e "med. região".
- Botão "✕ Limpar filtros" fixo no rail com contador de filtros ativos.

## Adendo v1.3 (17/07, noite)

- Radar aposentado (subconjunto do Dashboard); curva de preço migrou.
- Logo Sacchelli (negativa, base64) no header.
- Últ. ganho/faturado corrigido: PU PONDERADO por kg do último dia (caso
  AGRITECH: 4 ganhas em 11/06 de 15,27 a 20,37 conforme o lote → 15,76
  ponderado, com kg exibido). ARG_MAX empatado pegava linha arbitrária.
- **Matriz material** no Dashboard (aço × faixa de bitola, pendente × estoque
  físico): 🚨 cotando sem ter · 🔥 queima possível · 🧊 parado sem cotação;
  célula clica → filtra. Achados de estreia: R$ 4,8M cotado sem material;
  4320 118t paradas sem demanda; 4140 2-4" 531t paradas com R$ 862k pendente.

## Adendo v1.4 (17/07, noite) — cliente por CÓDIGO

Achado do Gustavo validado nos dados: AGRITECH pendente = cód 7318 (LAVRALE,
Caxias-RS, sem histórico) exibindo WR/histórico/últ. ganho do cód 5927
(Indaiatuba-SP). **157 nomes reduzidos colidem entre códigos distintos.**
Toda a cadeia de cliente (WR do score, cliente×família, últ. ganho/faturado,
histórico, badge ABC) passou a casar por `cod_cliente`; ABC do gold refeito
por código. AGRITECH-RS 93%→41%, ABC A→C; pipeline esperado 27,1→26,1M.
Caveat de grupo (WEG etc.): visão de HOLDING continua possível pela busca por
nome na UI; o score/histórico não mistura códigos.

## Adendo v2.0 (17/07, noite) — auditoria tripla por agentes + próximos passos

Gustavo pediu: recalibração periódica, notas fora do navegador, e auditoria
por agentes (dados, lógica, design). Resultado:

- **Recalibração agendada**: tarefa local 15/09/2026 9h — backtest com a massa
  da régua nova + teste do componente de tamanho do item; só aplica se
  melhorar calibração sem perder discriminação.
- **Notas com arquivo**: botão "Sincronizar notas" (File System Access) grava
  cockpit_notas.json (multi-máquina via repo/iCloud); merge por timestamp
  fecha o ciclo gerente exporta → Gustavo importa sem sobrescrever.
- **Auditoria de DADOS** (agente 1): núcleo estatístico bateu em recomputação
  independente; 2 bugs: gap dos pendentes DUPLA-convertido pra % (731 itens
  no bucket de preço errado, EV inflado R$ 1,57M → pipeline 26,1→24,6M) e
  faixa ≤1" da matriz nunca atribuída (MIN lexicográfico). Corrigidos d3e91b0.
- **Auditoria de LÓGICA** (agente 2): 7 bugs corrigidos (ladder com tabela
  zerada afirmando preço confortável, borda da matriz divergindo do clique,
  export podendo auto-conectar as notas do dono, busca fantasma no limpar,
  import sem validação, "sem dados" em aba oculta) + blindagens (apóstrofo
  no esc — 153 clientes com ', fallbacks de faceta, sanitização do rótulo).
- **DESIGN REVIEW** (agente 3): 8 aplicadas — drawer virou ESTEIRA (j/k +
  ‹i/N› + ações rápidas no topo), rail em 4 grupos colapsáveis com filtro
  selecionado sempre visível, Triagem sugerida na 3ª coluna, cards do
  Dashboard acionáveis (Sem próxima ação/Bloqueio/Sem estoque nem partida).
  Elogios do reviewer: facetas ponderadas por R$, EV como moeda única de
  ponta a ponta, export cifrado com validade. Commits d3e91b0 + 0cbfefc.

## Adendo v2.1 (18/07) — memória do pendente

Aprovada a recomendação: cada `make cockpit` grava a FOTO do dia em
`lake/history/cockpit_pendentes/snapshot_date=*/` (parquet, view
`cockpit_pendentes_hist` no gold). Destrava: painel "Evolução do pendente"
no Dashboard (≥2 fotos), e `make cockpit-desfechos` — cruza fotos ×
encerradas pela `chave_cotacao` (mesma derivação nas duas pontas, confirmado)
e mede: funil da memória (ganhou / perdeu disputa real / administrativo /
ainda pendente / sumiu-reemitida), CALIBRAÇÃO MEDIDA por banda de score
(alimenta a recalibração de 15/09 com desfecho real) e "o que o Foco rendeu"
(conversão com × sem próxima ação registrada, via cockpit_notas.json).
Primeira foto: 18/07, 3.499 itens / R$ 48,6M.

**Correção de régua (18/07, lembrete Gustavo):** o relatório de desfechos
passou a medir conversão pela régua CANÔNICA — R$ de PEDIDO EMITIDO ÷ R$
encerrado (bases total e disputa real), via `cot_chave` do cross-check de
Pedidos (~98%, item exato). 'Ganhou' declarativo vira reconciliação, não
régua. Funil mostra o R$ do pedido ao lado do cotado (pedido pode diferir
do cotado — é o nº que importa).

**Validação do ciclo de fechamento (18/07, questionado pelo Gustavo):** o
"0 dias" das Ganhou é real no REGISTRO (105k/106k com emissão=encerramento
no bruto do Softcomp) mas não mede negociação — a Ganhou é formalizada no
dia do pedido. A cadeia cotação-anterior→Ganhou (mesmo cliente+material,
≤45d) só cobre 19,5% (mediana 14d — proxy ruidoso). Retratação: rótulo
"quente" do bucket 0-3d removido; a penalidade de aging do score segue
aguardando o hazard medido. Medição LIMPA implementada no
`make cockpit-desfechos`: TEMPO DE DECISÃO = emissão da cotação fotografada
pendente → data do pedido (cot_chave), geral + por cliente (mín/mediana,
n≥3). Quando houver massa, vira campo do drawer ("prazo típico do cliente",
possivelmente por família).

## Adendo v2.2 (18-19/07) — refinamentos de uso real (lote Gustavo)

- Aging: buckets 0-3/4-7/8-15/16-30/>30 (pedido dele; "quente" retirado após
  validação — ver ciclo de fechamento acima). Facetas ordinais com ordem fixa.
- Perfil efetivo pelo TEXTO do material (3º campo não-confiável do export):
  Tubo R$10,2M / Anel R$748k saíram do "Redondo"; engenheirado vira bucket
  próprio em perfil e acabamento; partida suprimida p/ tubo/anel/chapa.
- "(sem tabela)" ≠ "(engenheirado)": 54 itens catalogados R$2,5M com F1-F3
  zerados (trefilados do lançamento sem faixa no Softcomp — ação de pricing).
- Vocabulário: "padrão" (Produto Padrão) no lugar de catalogado; "Tipo de
  produto" no lugar de Tipo de item.
- Rail: grupos sempre minimizados + ACCORDION (1 aberto por vez); Região de
  SP só aparece com Estado SP marcado (desmarcar limpa junto), Grande SP
  fixo no topo + interior por R$; nome quebra em 2 linhas, valor nunca.
- REGRA de apresentação: valor monetário nunca quebra linha (rail + gráficos).
- Dashboard: painel Vendedores virou tabela "Gestão da carteira" (pendente,
  EV, chance ponderada, aging médio, SEM AÇÃO em vermelho).
- Matriz: faixas 12-16"/16-22"/>22" (5.066t saíram do balaio >12"), depois
  1-4" unificada; colunas com largura uniforme (Aço 118px).
- **FILTRO INTELIGENTE**: facetas em cascata — cada uma conta sobre o recorte
  das outras (gerência Felipe ⇒ só vendedores/unidades dele); a própria
  ignora a própria seleção; selecionada nunca some.

## Adendo v2.3 (19/07) — teste de usuário veterano (agente "Ricardo")

Gustavo pediu um agente-persona: gerente comercial com 20 anos de Softcomp,
carregado com produtos/políticas da casa, operando o Cockpit ao vivo
(7 cenários, ~40 interações reais no browser). Veredito dele: "faz em 3
cliques o que me tomava meia manhã; números fecham centavo com centavo;
honesto nos casos-armadilha — mas negociando Preta ainda preciso do
Softcomp do lado" (falta custo/margem).

APLICADO na hora (commit 3cf6af7): R$/kg do histórico só quando a cotação
foi em KG (croquis "catalogados" tinham kg=peças — 42.569 "R$/kg" era
R$/pç); material do texto nas linhas vazias; scroll lock do drawer; j/k
navega a fila de ORIGEM (Foco navega o Foco); linha da Gestão da carteira
clicável → Triagem do vendedor; faceta "Próxima ação"; selo "score
(parcial) — sem fator preço"; aging KPI ponderado por R$; "Cuidados de
leitura" no Como funciona (curva em U = viés de seleção; ΣEV ≠ forecast).

PAUTA DE PRODUTO (aguarda decisão Gustavo):
1. Custo/margem na Preta — REQUER fonte de custo de estoque no lake (hoje
   só custo de venda no RAF); é o que falta pro drawer decidir alçada.
2. OC em trânsito ("chega dia X") — as colunas "Compras até <mês>" do
   EstoquePadrao JÁ têm o dado; candidato natural a próximo dev.
3. Idade do estoque parado (última saída, via MovimentacaoEstoque).
4. Validade da cotação / "vence hoje" — confirmar semântica do campo prazo.
5. Follow-up com dono+data e notas compartilhadas gestor↔vendedor.
6. Visão de grupo econômico (códigos irmãos lado a lado).
7. Concorrente: já é datalist canônico; avaliar torná-lo obrigatório-select.

## Adendo v2.4 (19/07) — decisões da pauta: custo, OC, validade, corte

Gustavo destravou a pauta do teste de usuário:
- **MC estimada s/ AÇO** no drawer: custo de reposição da FAMÍLIA
  (FamiliasProdutos 'Liquido' R$/ton→R$/kg, match 99,3%). Disclaimer:
  serviços agregados não vêm no relatório — margem é do aço. Verde ≥24%.
- **OC em trânsito** por SKU (colunas "Compras até" do EstoquePadrao) +
  situação do SKU; aviso fixo de não prometer sem confirmar (importações).
- **Validade padrão 5d** (campo não vem no excel): vence em/hoje/vencida.
- **Corte Sim/Não**: faceta (Material) + coluna Triagem + CSV.
- **Próxima ação com data** ("para quando").
Pendências da pauta que seguem: follow-up compartilhado gestor↔vendedor,
grupo econômico, tendência do estoque no drawer (fonte: painel/movim.).

## Adendo v2.5 (19/07) — tendência, grupo econômico e distribuição

- **Tendência do SKU** no drawer (MovimentacaoEstoque via parser do Painel):
  ▲/▼ média 3m÷12m + última saída, na linha Situação do SKU.
- **Grupo econômico AUTOMÁTICO por raiz de CNPJ** (descoberta: 'Grupo Cliente'
  do Softcomp existe mas só 58 preenchidos; a raiz do CNPJ agrupa 567 grupos /
  1.500 códigos sem manutenção — AGRITECH SP+RS confirmados como filiais,
  raiz 88658984). Drawer mostra irmãos (WR + últ. ganho na família); score
  segue por código. ListaClientes 24/05 canonizada no lake ('Grupo Cliente'
  como overlay quando preenchido).
- **Distribuição por gerência**: `make cockpit-gerencias` / duplo clique em
  `exportar_gerencias.command` → 5 HTMLs cifrados (config em
  cockpit_gerencias.yaml: Felipe/Fuscão, Odair PIR+SCA, Fabiola, Fernando,
  Francisco) + RASCUNHOS no Mail.app com anexo (1º uso: autorizar Automação
  do macOS). Criptografia Python espelha a do HTML (validade 3d).

**Distribuição por gerência — rota final Gmail/IMAP (19/07):** Gustavo usa só
Chrome; Mail.app descartado. Anexo via API/MCP inviável (arquivos até 3,4MB
estouram contexto) e file_upload do Chrome só aceita arquivo compartilhado à
mão. Solução: o script deposita o rascunho COMPLETO (com anexo) em
[Gmail]/Rascunhos via IMAP APPEND — aparece no Gmail web. Auth: senha de app
no Keychain (gravada pelo próprio Gustavo; setup único de 2 min impresso pelo
script). Duplo clique em exportar_gerencias.command faz tudo.

---

## Adendo v2.6 — 19/07/2026: página do portal vira dashboard gerencial

Decisão do Gustavo: com o Cockpit dono do detalhe item-a-item, a página "Cotações
Pendentes" do SAC360 sobe de altitude. Redesenho (commit `ba8b1fc`):

- **Removido** (duplicava o Cockpit): fila PRIORIZAR top-30, matriz aging×estoque,
  tabela mestre paginada + CSV, NEGAR item a item.
- **Novo dashboard** (fonte: foto mais recente de `cockpit_pendentes_hist`; fallback
  `vw_cotacoes_pendentes` sem memória): headline + cartões (R$ pendente, **valor
  esperado**, conversão 12m em disputa real por valor como régua — 48,8%, bate com
  os ~50% do valor esperado; priorizar); **evolução entre fotos distintas** (dedupe
  por assinatura de conteúdo — o snapshot diário repete sem export novo);
  **movimento** entrou×saiu×"saiu e virou pedido" (ANTI JOIN entre fotos +
  `cot_chave` do cross-check de Pedidos); **qualidade** por banda de score
  (alta ≥50% = R$ 23,0M · média R$ 19,9M · baixa R$ 5,8M); **onde está o dinheiro**
  por gerência com "% tende a fechar" (Felipe/Fuscão R$ 40,6M/51% · Marketing 25%)
  e vendedor no expander; **top-10 clientes** (51% do pipeline; VALLOUREC R$ 8,2M
  é ABC B). Botão "Abrir o Cockpit" no header.
- Blocos de memória degradam com honestidade: com 1 foto distinta mostram a
  promessa ("aparece na segunda foto com export novo"), nunca movimento falso.

---

## Adendo v2.7 — 19/07/2026: fluxo de dados fechado ponta a ponta + ponte Fases → Simulador

Sessão de operacionalização (commits `44e6ae4`…`108449d`):

1. **Fluxo 1-clique**: botão "Receber e atualizar" (Central de Atualizações) valida
   `00_Entrada/`, arquiva com nome canônico e roda o `make atualizar-*` certo por
   fonte. Sidebar enxuta: Cockpit + relatório gerencial no header da aba Cotações
   Pendentes; receber só na Central.
2. **ListaClientes e FasesProducao canonizadas** (contratos regenerados; rejeição
   agora orienta o conserto quando a fonte não tem contrato). `make
   atualizar-cadastros` cobre clientes/vendedores/tipos NF/motivos/fases.
3. **Cockpit sempre fresco**: gerar_cockpit encadeado em TODO alvo atualizar-* que
   alimenta o score (pedidos, cotações, RAF, estoque, famílias — 5 lacunas fechadas).
4. **Ponte Softcomp → Simulador** (`gerar_fases_simulador.py` → overlay
   `config/fases_softcomp.js`): preço/margem do cadastro de Fases fluem pro
   simulador por código, só com tipo de cálculo compatível; divergência incompatível
   vira aviso. 1ª rodada pegou o reajuste Embraço (TA1 860→950 + marg 20→15, TA2
   1030, TA3 1210, TD1 1950) e NO1 marg 15→20. Pendência: fase AQ1 (tipo misto
   '% s/ Total + Custo Unitário') — Gustavo confere.
5. Famílias → Simulador segue pelo snapshot `--comparativo` (já existia).

**Semântica de fases no Softcomp (Gustavo, 19/07 — memória 000557152-0001):**
preço de fase é fixo na cotação; TT negociado entra pela fase **TTX** "TT -
Especial" (Valor vazio = digitado na hora, marg 30 — simulador já espelha).
A memória exibe fase TERCEIRIZADA **líquida de PIS/COFINS** (BJ1 2.630 ×
0,9075 = 2.386,73 — não era desconto); interna/cert/embalagem sai cheia.
Cadastro e overlay são sempre preço cheio. AQ1 confirmado como 1% s/ custo
do aço (rótulo misto com Valor vazio = % puro) — zero avisos na ponte.

---

## Adendo v3.0 — 22/07/2026: Score ML (XGBoost) vence o backtest cego

Decisão Gustavo: evoluir o EV com "ML pesado" + arcabouço Big4. Construído
`MotorAnalitico/ml/treinar_score_ml.py`:

- **Treino 2025** (122.795 disputas reais) → **teste CEGO 2026** (54.241).
- **AUC 0,860** (log-odds atual: 0,723) · **erro de calibração 1,6pp/banda**
  (atual: 4,7pp) · Brier 0,150. Régua "só assume se vencer": **venceu nos 2**.
- Anti-vazamento: priors expansivos (cliente/vendedor/família/cli×fam só veem
  histórico ANTERIOR à emissão; `data` da view conferida = data_emissao);
  isotônica ajustada em nov-dez/25, nunca no teste.
- SHAP: prior_cliente (0,98) e prior_cli×fam (0,82) dominam — coerente com o
  log-odds; o ganho do ML vem das INTERAÇÕES. Explicabilidade preservada
  (SHAP por item no drawer quando integrar).
- Modelo em `lake/meta/score_ml/` (gitignored). Deps: sklearn/xgboost/shap
  (+ brew libomp).

**Plano de integração (proposto): modo SHADOW** — score ML ao lado do atual no
Cockpit por 2-4 semanas; memória diária grava ambos; `cockpit-desfechos` julga
com desfecho REAL (régua canônica: pedido emitido). Troca oficial só com
vitória confirmada em produção. Caveat honesto: backtest usa Ganhou declarada
(mesma régua do benchmark) — a prova final é contra pedido emitido.

**v3.1 (22/07, noite): SHADOW LIGADO.** Coluna "ML" na aba Itens (cinza, tooltip
"não decide triagem/EV") + linha no drawer; scml gravado na memória diária;
`make cockpit-desfechos` julga os dois scores na mesma régua (banda × virou
pedido + erro absoluto médio ponderado por R$ — menor vence). Corr sc×scml=0,66.
Julgamento começa quando as ENCERRADAS atualizarem (export está de 02/07 —
itens fechados aparecem como "Sumiu" até lá). Decisão de troca: ~2-4 semanas
de desfechos. Ciclo de 30 min roda o ML a cada rodada (custo ~4s).

---

## Adendo v3.2 — 23/07: Segmentação de clientes (time de agentes) — PROPOSTA PRONTA

Doc: `06_Docs/Segmentacao_Clientes_Sacchelli_Proposta.md` (crítico adversarial
validou 30/30 exemplos contra o gold). 3 eixos: **Perfil de Compra** (7 segmentos
por regra objetiva: Projeto, Revenda, Negociador, Orçamentista, Programado, Fiel,
Esporádico — precedência 1→7), **Tier por MARGEM MC** (não faturamento),
**Trajetória** (6m vs 6m). Achados: Programados = 35% da margem com 10% do funil;
Orçamentista+Projeto = 62% do funil e 26% da margem; Negociadores concentram 63%
da Preta (WEG-SC 49%). TUP=Programado (conv 93%) vs ADDN=Orçamentista (31%) —
mesma régua. Riscos abertos: sombra Orçamentista→Programado (87 clientes, ex.
VAMA — sub-flag compra_recorrente sugerida); Fiel talvez seja antessala do
Programado. PRÓXIMO: validação do Gustavo → recomputo mensal no gold → feature
do score (recalibração 15/09).

**v3.3 (23/07): segmentação OPERACIONALIZADA.** Régua v1.1 em `definicoes.py`
(guard do híbrido confiável — TUP na navalha do 60% de orç. prévio virou o caso
que provou o risco 'sombra #4→#5' da crítica); `vw_segmentacao_clientes` no gold
(recomputo por rebuild); Cockpit com badge de perfil, faceta no rail e linha no
drawer (TUP = "Programado · Tier A · Crescendo · compra recorrente"). Pendentes
por perfil: Orçamentista 1.311 itens, Programado 691, Negociador 406, Projeto 217.
Snapshot diário grava o segmento → desfechos medirão conversão POR SEGMENTO.
Pendente: validação top-100 com Gustavo/gerentes (Fase 1 do doc); feature no
score na recalibração 15/09.

**v3.4 (23/07): segmentação auditada por fatos EXTERNOS.** Camada 1: CNAE da
Receita (BrasilAPI) pros 120 maiores — 77 confirmam a régua, 9 divergem.
Camada 2: workflow de 10 agentes pesquisou as 9 na web/sites — 3 confirmadas,
2 reclassificações aplicadas via override novo (segmentacao_overrides.yaml:
SIDERTECNICA=forjaria não revenda; REITZ=engineered-to-order), 3+1 pendências
no Excel de validação (06_Docs/Validacao_Segmentacao_Top120_2026-07-23.xlsx,
cópia em ~/Downloads). Meta-achado p/ v1.2: régua lê job-shop intermitente
como Revenda/Projeto — falta sinal 'fabricante sob encomenda'. Destaque
comercial: SPECIAL (2 CNPJs) é provavelmente REVENDA cotando como consumidor
final — se confirmar, pricing de canal imediato.

**v3.5 (23/07): validação humana FECHOU o top 120.** Gustavo respondeu o Excel
('Sim' USIESP→Orçamentista; 'Sim' SPECIAL 2 CNPJs→Revenda de tubo e aço) e
colou os textos dos sites de USICAL e DANFER (ambos job shop 'conforme
especificação/sobre desenhos' → Orçamentista, cadência protegida pela flag
rec). 7 overrides ativos em segmentacao_overrides.yaml. Top 120 = 100%
validado por comportamento + Receita + site/humano. AÇÃO COMERCIAL ABERTA:
SPECIAL é revenda cotando como consumidor final → aplicar degrau de canal
(playbook Revenda §4) — decisão de pricing com a gerência.

**v3.6 (23/07): Segmentação v2 — REGIME COMERCIAL derivado dos dados.** Discussão
Gustavo sobre critérios rendeu o eixo que faltava: COMO o cliente transaciona
(≠ o que ele é). Insight-chave: todo pedido Softcomp exige cotação → cotação de
cliente-contrato é BUROCRACIA, não disputa (por isso TUP 'converte' 93%).
Assinatura estatística (par cliente×material ≥3 compras, preço estável ±2%,
ciclo ≤2d) achou sozinha os 4 que ele citou de memória (JACTO 87%, KSB 80/75%,
TER 72%, TUP 71%) e revelou contratos informais não-nomeados (MAHLE 97%,
AGRITECH 90%, STOLLE 100%, ARCO 68% — 'Negociador' que negociou UMA tabela e
programa). Regimes: Contrato-programação/parcial · Competitivo recorrente ·
Orçamentação · Spot. Consignação = flag (WEG TGM). No Cockpit: faceta + drawer.
Excel Validacao_Natureza_Top100 (99/100 pré-preenchidos por CNAE+pesquisa) pros
gerentes — distinção nova validada: componente p/ OEM ≠ produto próprio de
catálogo. Score 15/09 ganha: segmento + regime + flag item-fora-do-padrão.

**v3.7 (23/07): RÉGUA FINAL proposta (aguarda ok do Gustavo).** 4 agentes
destilaram as 100 naturezas dele: 6 rótulos no vocabulário DELE (Usinagem e
Caldeiraria sob encomenda · Fabricante de Equipamentos · Redutores e
Engrenagens · Peças Seriadas auto/agro · Forjaria e Fixadores · Revenda) +
2 flags (Contrato ⚙ dos dados; Marca própria de reposição 🏷). Árvore de
bolso de 3 perguntas; crítica reclassificou os 100 (80 limpos, 20 por regra
do verbo dominante). Doc: Segmentacao_Sacchelli_Regua_Final.md + anexo
Top100 xlsx. Perfis v1 viram insumo interno do score.

**v3.8 (23/07): régua final NA CARTEIRA TODA + primeiros padrões.** Natureza em
camadas (100 validados > CNAE > nome > ramo; confiança marcada; cobertura 75%+
por valor). Cockpit com badges USI/EQP/RED/SER/FOR/REV. PADRÕES (cotações 18m):
Usinagem&Caldeiraria = MAIOR funil (R$658M cotado) e só R$44M comprado (15:1 —
custo de cotar é o problema do segmento); Fabricante de Equipamentos = maior
comprador real (R$117M) e maior margem (R$23M MC); Peças Seriadas = conv mais
alta (49%) E mais Preta (31% — contratos agressivos TUP/MAHLE); Redutores =
assinatura de material perfeita (17CrNiMo6 cementação = R$13,5M, 1º aço do
segmento); Forjaria&Fixadores = 75% das compras na VERDE (paga preço cheio);
Revenda compra no meio da tabela (6% Preta, 5% Verde). Ciclo mediano 0 em tudo
= viés Ganhou-formalizada (conhecido); tempo real de decisão fica pros
desfechos. Próximo: página Segmentação no portal + features do score 15/09.

**v3.9 (24/07): página Segmentação no portal** (Equipe & Clientes): padrões por
segmento vivos, heatmap Natureza×Regime, alerta Esfriando A/B, drill, memória
de trocas (foto diária em lake/history/segmentacao_clientes). Janela do ciclo
de 30 min ajustada: seg-sex 07-18h (definição Gustavo).

**v4.0 (24/07): tripé do EV completo.** Margem esperada (chance × valor × MC
estimada s/ aço; KPI com cobertura 52% do R$, coluna em Itens, FOCO reordenado
por margem — sem estimativa entra por EV × MC mediana) + banda Monte Carlo no
Pipeline esperado (2.000 cenários, cotação fecha em bloco, determinístico:
"80% conf.: R$ 20,7M–26,4M"). Tudo no cliente = reage aos filtros. Pendências
do EV: calibração medida + hazard ficam pra recalibração 15/09 (dependem de
encerradas frescas — Gustavo atualiza).
