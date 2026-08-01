---
data: 2026-06-14
tipo: log
status: vigente
obs: "entregue — documento em 3 fases pronto para discussão"
domínio: logística / custeio / política comercial
criado: 2026-06-14
tags: [logística, frete, guarulhos, conselho, cowork, fase1]
---

# Política Logística Guarulhos — documento em fases + cortes derivados da base NF a NF

Retomada do projeto (o cowork "Projeto Politica Logistica Guarulhos - Handoff" travou; contexto recuperado via vault + pasta `04_Logistica/` + sessão idle "Sacchelli Guarulhos logistics proposal"). Nada foi perdido — a v2 de 12/06 estava intacta.

## Decisão de reestruturação (Gustavo)
Quebrar em fases:
- **Fase 1 (aplicar já)**: política de mínimo por entrega para Guarulhos — valor **ou** peso mínimo, para Grande SP e Interior.
- **Fase 2 (estudo)**: redefinir regiões, R$/kg por região, governança de revisão de custos, revisão da frota (toco vs terceirização).
- Entregável: **documento simples** com Diagnóstico + Fase 1 + Fase 2 (tópicos para discussão).

Definições do Gustavo: usar **as duas variáveis com lógica OU** (valor OU peso). Os números R$3k/300kg etc. eram sugestão dele — pediu **derivar de análise**, não chutar.

## Análise nova — base de romaneios NF a NF jan–mai/2026
Gustavo subiu os brutos que faltavam: `logistica janeiro..maio.xlsx` + `Logistica - regioes.xlsx`. Migrados para `04_Logistica/brutos_romaneios/`. (Resolve a pendência #6 do log de 12/06.)

- Schema: Romaneio · Data · Veículo · Motorista · **Região ID** (de-para no arquivo de regiões) · **Tipo** (Cliente/Fornecedor/Transporte) · ID Dest+Nome (cliente) · **Transportadora** (N/Caminhão = frota própria · Cliente Retira · terceiros) · Nº Documento (NF) · Peças · **Peso** · **Valor**.
- Universo da política = **Tipo=Cliente & Transportadora=N/Caminhão** (frota própria) = 3.275 NFs → **2.370 entregas** (agrupadas por romaneio × cliente ≈ CNPJ×dia). 2.889 NFs distintas.
- Classificação: **Grande SP** = regiões 5,6,7,8,9,11 (zonas SP + Guarulhos + ABCD) · **Interior** = 1,2,3,4,10,13,14 (Campinas, Bragança, Piracicaba, Sorocaba, Vale, Limeira, BH).

### Distribuição por entrega
| | Grande SP (n=1767) | Interior (n=603) |
|---|---|---|
| Valor mediano | R$ 4.292 | R$ 14.630 |
| Peso mediano | 388 kg | 1.034 kg |
| Custo real alocado/entrega | R$ 696 | R$ 1.225 |
| Frete embutido médio (1,85%) | R$ 235 | R$ 628 |
| % entregas que não cobrem custo cheio | **92%** | **86%** |

Custo/entrega = custo do romaneio (fixo R$965 + R$8,71/km × km da região, do estudo de rotas) rateado pelas paradas.

### Break-even e cortes (lógica OU — paga taxa só se valor<Vmin **E** peso<Wmin)
Break-even = onde 1,85% embutido cobre o custo marginal da parada (GSP R$40–80; Int R$60–120):
- Grande SP: R$ 2.200–4.300 → **corte R$ 3.000 / 300 kg / taxa R$ 200** (atinge 36% das entregas, **4,1% do valor**, ~128/mês)
- Interior: R$ 3.200–6.500 → **corte R$ 5.000 / 500 kg / taxa R$ 400** (atinge 17%, **1,4% do valor**, ~21/mês)

Ajuste vs sugestão do Gustavo: Interior baixou de R$6.000 (pegava 20%) para **R$5.000**, centrado no break-even.

**Achado-âncora**: as entregas abaixo do corte na GSP têm frete embutido médio de **R$ 27** vs custo de parada R$ 40–80 — são deficitárias de fato. A regra corrige o subsídio em 1/3 das entregas urbanas tocando só ~4% do valor entregue. O agregado fecha porque retirada + pedido grande pagam 1,85% e subsidiam a entrega pequena.

## Entregáveis (em `~/dev/afs-lake/04_Logistica/`)
- `Politica_Logistica_Guarulhos_Fases.docx` / `.pdf` — 3 pgs (builder `build_fase1.py`, python-docx)
- `brutos_romaneios/` — 5 meses + regiões + `entregas_calibracao_jan-mai.csv` (2.370 entregas, base do cálculo)

## Revisão v2 (mesma sessão) — 3 perguntas do Gustavo
1. **Agrupamento NF→entrega confirmado**: das 2.370 entregas, 434 (18%) têm 2+ NFs do mesmo cliente no mesmo romaneio (máx 7, média 1,25 NF/entrega). Sem agrupar, o % abaixo do mínimo seria inflado.
2. **Entregas/mês por região** (frota própria): ABCD 107 · Zona Oeste 79 · Guarulhos 70 · Zona Leste 56 · Zona Norte 28 · Zona Sul 14 (GSP=353) · Campinas 45 · Piracicaba 37 · Sorocaba 22 · Vale 15 · Bragança 1,0 · Limeira 0,8 (INT=121). Total 474/mês. Bragança/Limeira ~1 entrega/mês cheia → terceirizar.
3. **Modelo tarifa fixa + variável** (despesas reais 2026): fixo (pessoal+IPVA+seguros+CD) R$ 79,5 mil/mês = 31%; variável (comb+manut+pedágio+terceiros+multas) R$ 178,1 mil/mês = 69%. **Achado grande: só ~58% do faturamento é entregue; ~42% é retira** (todos pagam 1,85% hoje → retira subsidia entrega). Percentuais: **% fixo 0,53% (todos) + % variável 2,05% (só entrega) → entrega paga 2,58%, retira paga 0,53%**. Neutro no agregado. Alternativa: motorista na entrega → fixo 0,21% / entrega 2,80%. Split 58/42 a confirmar contra CIF/FOB do ERP.

Documento revisado para v2 (4 pgs) incorporando os 3 itens. `Politica_Logistica_Guarulhos_Fases.docx/.pdf` regravados.

## Revisão v3 — tarifa em 2 cenários + calculadora de governança
Gustavo perguntou: cobrar 1,00% de todos (em vez de 0,53%) + variável vale a pena? Tem metodologia/governança?

**Pegadinha da sobre-recuperação**: base 1,00% mantendo variável 2,05% recupera R$ 329k/mês vs custo R$ 257,7k → **sobra R$ 71k/mês (R$ 857k/ano, +28%)**. Não é política de custo, é aumento disfarçado. Base só sobe se variável descer junto (neutro).

**Cenários neutros** (recuperam os mesmos R$ 257,7k/mês; muda só a distribuição):
| Base (todos) | Variável (entrega) | Entrega paga | Retira paga | Gap incentivo |
|---|---|---|---|---|
| 0,53% (só fixo) | 2,04% | 2,57% | 0,53% | 2,04 pp |
| 0,75% (colchão) | 1,66% | 2,41% | 0,75% | 1,66 pp |
| 1,00% (base alta) | 1,23% | 2,23% | 1,00% | 1,23 pp |

Trade-off: base maior alivia a entrega e onera a retira, **reduzindo o incentivo à retirada** (o ganho estratégico). Recomendação minha: não ir a 1,00%; 0,53% (máx. incentivo) ou ~0,75% (colchão). Mantidos os dois cenários no doc por pedido do Gustavo.

**Metodologia + governança** (Fase 2c): classificar contas fixo/var; trimestral % fixo = base alvo, % variável = (custo total − base×fat total)/fat entrega; banda ±0,15pp; gatilhos diesel ±10%/dissídio/troca frota/share retira ±5pp; dono controladoria+comercial; KPIs custo/recuperado/folga/% retira/ocupação/R$kg.

**Entregáveis novos**:
- Doc revisado para 4 pgs com Fase 2(a) em 2 cenários + aviso sobre-recuperação + Fase 2(c) ciclo de governança.
- `Calculadora_Tarifa_Logistica_Guarulhos.xlsx` (3 abas: Custos classificação fixo/var · Calculadora com base alvo editável + cenários · Acompanhamento trimestral). Fórmulas vivas, recalc 0 erros. Lever: trocar Pessoal FIXO→VARIÁVEL testa "motorista na entrega".

## Revisão v4 — toco, base recomendada, variável por região (Google Docs)
Gustavo migrou o doc para Google Docs (título virou "Política Comercial | Logística | Unidade Guarulhos"). 3 pedidos:
1. **Estudo do toco na Fase 2(e)** — puxados números do `cpk_frota_sacchelli.xlsx`: CPK cheio urbano toco R$ 5,25/km vs truck R$ 7,17/km; custo mensal R$ 18,4k vs R$ 25,1k; R$/ton·km decisivo, **truck só vence acima de ~68% ocupação** (GSP roda a 29%); economia ~R$ 135k/ano trocando 2 urbanos por toco na renovação. Mantida terceirização dos eixos longos (~R$ 59k/mês). É decisão de RENOVAÇÃO (frota quitada).
2. **Base recomendada = 0,75%** (com 0,53% como piso de custo). Mantidos os dois cenários no doc; B marcada como recomendada.
3. **Variável diferenciada por região** — minha posição: sim, mas a forma certa é a parcela variável virar **R$/kg por faixa de região** (não % diferente por região), porque o custo é dirigido por peso × distância. Agrupar em 3–4 faixas (GSP densa/GSP/interior próximo/distante). Sequência: lançar com variável única e migrar para R$/kg quando o estudo de R$/kg + de-para CEP→região estiverem prontos. Registrado na Fase 2(b).

Doc segue 4 pgs. Artefatos da conversão p/ Google Docs a corrigir: box "Achado central" virou linha da tabela de indicadores com typo "Observaçãoi"; rótulo "Em uma frase." sumiu.

## Revisão v5 — peso mínimo de despacho, R$/kg por região, separação de transferências
Gustavo: incluir na Fase 1 o peso mínimo p/ truck sair; R$/kg por região (2026); e separar transferências (Jacareí/Anchieta).

**Transferências mal classificadas (ACHADO)**: estão lançadas como Tipo='Cliente', não 'Transporte' (esse tipo = transportadora terceira). Razão social Sacchelli = transferência interna:
- "AÇOS F. SACCHELLI - JACAREÍ" (região Vale): 285 t — transferência padrão.
- "AÇOS F SACCHELLI LTDA" (sem cidade, região ABCD): 1,5 t (mar) → 35 t (abr) → **100 t (mai)** = o envio de forjados Guarulhos→**Anchieta** (palavra Anchieta não aparece; sistema usa razão social; ABCD = região do ABC/Via Anchieta). **A confirmar com Gustavo.**
- Total transferências 436 t / R$ 3,5 mi em 5m, **pico 177 t em maio**. Inflam custo logístico de abr–mai → tarifa deve usar custo normalizado.
- "ARCO FORJADO" mantido como CLIENTE real (entregas regulares Zona Sul/Oeste, mix com outros no romaneio).

Universo limpo: 2.370 → **2.344 entregas**. Entrega/retira recalculado: **~55%/45%** (era 58/42; a retira interna inflava).

**R$/kg REAL por região (2026, limpo) — dirigido por OCUPAÇÃO, não distância**:
| Região | ocup | R$/kg | | Região | ocup | R$/kg |
|---|---|---|---|---|---|---|
| Vale | 14% | **1,64** | | Zona Oeste | 49% | 0,48 |
| Zona Norte | 16% | 1,29 | | Piracicaba | 68% | 0,52 |
| Guarulhos | 20% | 1,01 | | Bragança | 76% | 0,41 |
| Zona Leste | 22% | 0,79 | | Campinas/Sorocaba | 51-56% | 0,63 |
| ABCD | 27% | 0,76 | | Limeira | 53% | 0,68 |
| Zona Sul | 30% | 0,69 | | Média GSP/INT | 29/50% | 0,71/0,64 |
Vale (235km, 14%) custa 3× Piracicaba (432km, 68%). Encher > encurtar.

**Peso mínimo de despacho (Fase 1)**: truck 14t → GSP ~5.000 kg (hoje 3.954/29%) · Interior ~8.000 kg (~60%). Abaixo: consolidar/terceirizar. Interior baixa freq (Vale/Bragança/Limeira) sempre acumular. Com toco 7t cai p/ ~4.000–4.500 kg.

Doc → 5 pgs. Tarifa %s mantidas (2,04/1,66) com caveat de normalizar transferências; não recalculei pra não introduzir inconsistência (custo também tem transfer).

## Revisão v6 — validação RAF das transferências + bloco no diagnóstico
Gustavo confirmou: "AÇOS F SACCHELLI" (ABCD) = Anchieta. Jacareí→GRU é abastecimento (processo); GRU→Anchieta é >90% transferência de estoque de forjados.

**Cross-check RAF (decisivo)**: via `mcp__afs-lake__query_sql` no `raf_enriquecido` (263k linhas). Match por ABCNNF_NUM:
- 45 NFs de transferência (destino Sacchelli) → **0 no RAF** (não geram faturamento).
- 50 NFs de entrega a cliente → **48 no RAF** (96%).
Confirma fiscalmente que transferência ≠ venda. Não há cliente 'SACCHELLI' no RAF (ABCCLIRAZ).

**Volumes de transferência (jan–mai)**:
| Movimento | Volume | Natureza |
|---|---|---|
| Jacareí → GRU | 285 t · R$ 1,63 mi | recorrente (abastece estoque GRU) |
| GRU → Anchieta (forjados) | 136 t · R$ 1,71 mi | pontual: 0→2→35→100 t (mar→mai) |
| Outras unidades | 14 t · R$ 0,19 mi | esporádico |
| **Total** | **436 t · R$ 3,53 mi** | movimentação, não venda |
Pico de maio (177 t total) é o Anchieta. Bloco "Transferências entre unidades" adicionado ao diagnóstico do doc (agora 5 pgs).

**RAF acessível via SQL** (DuckDB read-only): raf_enriquecido/raf_bruto, vw_faturamento, pedidos, cotações, estoque etc. Útil para validações futuras. Colunas-chave RAF: ABCNNF_NUM (NF), ABCCLIRAZ (cliente), ABCFILIAL, Op_Categoria/Op_Original, ValorTotal, ABCPFAPESFAT (peso fat), ABCDAT (varchar).

## Estudo de fundo — frete real × margem (cruzamento romaneio × RAF), v7
Join por **código de cliente** (romaneio `ID Dest` = RAF `ABCCLI` — validado: 6884=QUALIFERR etc.). RAF via SQL (filial 1 Guarulhos, 2026 jan–mai). MC = `MC_Total_RS`.

**Achados (69 clientes de frete relevante):**
- Frete real médio = **4,66% do valor entregue** vs 1,85% cobrado (2,5×). Frete total dos romaneios (sem transfer) = R$ 1,92 mi em 5m sobre R$ 41,2 mi entregues.
- Frete consome **14% da MC entregue** no agregado, mas concentrado na cauda:
  - >100% (entrega destrói margem): **5 clientes** (R$ 0,18 mi) — EIKIL (frete 41,7%, pocket −R$ 7,2 mil), AP Equip, General Roller, PKM, Grazzimetal.
  - 50–100%: 21 clientes (R$ 1,08 mi) · 25–50%: 24 (R$ 2,88 mi) · <25% saudável: 19 (R$ 18,96 mi).
- Confirma o subsídio cruzado em R$ e dá lista acionável. pocket = MC_entregue − frete_real + 1,85%×valor.

**Entregável**: `04_Logistica/Custo_de_Servir_Cliente.xlsx` (69 clientes, status DEFICITÁRIO/ATENÇÃO/MONITORAR/SAUDÁVEL) + `brutos_romaneios/custo_servir_cliente.csv`. Bloco "Validação — frete real × margem" adicionado ao doc (5 pgs).

**Próximo nível possível**: rodar os 468 clientes (não só 69); split MC entrega vs retira; usar para fechar os % definitivos da tarifa (custo normalizado ex-Anchieta).

## Correção v8 — método de rateio do frete (Gustavo pegou furo na EIKIL)
Gustavo questionou EIKIL R$ 14.180 e apontou: "o caminhão não foi só na EIKIL, deve ter outras NFs no romaneio". CORRETO — furo no rateio.

**Erro v1**: rateava custo do romaneio igualmente só entre as entregas de CLIENTE da frota própria. Excluía coletas de fornecedor, retira e terceiros do denominador → concentrava a viagem inteira em poucos clientes. Ex: romaneio 13017 era coleta na ANTHIS (Campinas, 11,6 t) com EIKIL (224 kg) de carona — joguei R$ 4.344 na EIKIL.

**Método v3 (correto)**: rateio do custo do romaneio **por peso entre as linhas que andaram no nosso caminhão (N/Caminhão)** — inclui coletas de fornecedor (caminhão foi lá), exclui transportadora terceira e retira. km = maior região visitada pelo N/Caminhão.

**Impacto da correção**:
- EIKIL: R$ 14.181 → **R$ 3.682** (10,8% do valor); pocket +R$ 3.304, vira ATENÇÃO (não deficitário).
- Frete médio agregado: 4,66% → **4,30%** do valor (ainda 2,3× o 1,85% cobrado — tese mantida).
- Custo do nosso caminhão por finalidade: Cliente 87% · Fornecedor 9% · Transferência 4%.
- Custo-de-servir (95 clientes c/ MC): **1 deficitário** (ATRAMETAL, revenda interior, frete 159% da MC) · 13 atenção · 37 monitorar · 44 saudável (antes: 5 deficit/21 atenção — inflado).
- R$/kg região (v3): GSP Zona Oeste 0,48 → Zona Norte 1,20; INT Bragança 0,41 → Vale 1,13. Indicadores/entrega: GSP R$ 632, INT R$ 1.134; 95%/88% não cobrem custo cheio.

`Custo_de_Servir_Cliente.xlsx` regravado (95 clientes, v3). Doc atualizado em todos os números (validação, região R$/kg, indicadores, nota de método). 5 pgs.

**Lição preservada**: rateio de frete por romaneio tem que usar TODAS as linhas que andaram no caminhão (coletas + entregas), não só as entregas de cliente — senão pequenos clientes em viagens de coleta absorvem custo que não é deles.

## v9 — custo-de-servir nos 468 clientes + curva custo/entrega por carga
**Todos os clientes**: 468 entrega → 414 com MC no RAF (54 faturam por outra filial). Join via string_agg do RAF (1 query). Distribuição: **26 deficitário** (R$ 0,22 mi) · 53 atenção (R$ 1,17 mi) · 126 monitorar (R$ 5,58 mi) · 209 saudável (R$ 31,15 mi). Frete agregado 4,26%. 2 clientes com MC negativa (vendeu abaixo do custo — problema de preço, não frete: ERNAINE, RDN). Doc validação atualizada p/ 414. `Custo_de_Servir_Cliente.xlsx` regravado com todos.

**Curva custo/entrega por carga (GSP, viagem típica, custo ~fixo)** — pergunta do Gustavo:
| Carga | Ocup | Custo/entrega | Custo/kg |
|---|---|---|---|
| ~4t (hoje) | 29% | R$ 632 | 0,64 |
| 5t | 37% | R$ 500 | 0,51 |
| 6t | 44% | R$ 417 | 0,42 |
| 7t | 52% | R$ 357 | 0,36 |
| 8t | 59% | R$ 312 | 0,32 |
Mecânica: custo da viagem ~fixo (R$ ~2.547 GSP); mais entregas/viagem diluem. Encher 4t→8t corta custo/entrega pela metade. Até 7t toco resolve; acima, truck. Adicionado à Fase 2(d) grade. INT: drop maior (1.880 kg), custo/viagem R$ 4.449; mesma lógica.

## v10 — entregas/romaneio por região + blindagem dos "três custos"
**Entregas/romaneio por região**: GSP média 3,9 (ABCD 4,6 · ZLeste 4,1 · Guarulhos 3,9 · ZOeste 3,8 · ZNorte 3,6 · ZSul 3,3) · INT média 2,8 (Piracicaba 4,9 · Campinas 4,1 · Sorocaba 3,2 · Limeira 2,0 · Vale 1,8 · **Bragança 1,0**). Densidade da rota é o que dirige o custo/entrega.

**Pergunta-chave do Gustavo**: "se a entrega custa R$ 632 e cobro só R$ 200, não cubro nem metade do custo real?" Resposta = armadilha de raciocínio (3 custos distintos):
- **Marginal** (parada extra em rota que já sai): R$ 40–120 — o que o pedido pequeno causa de fato.
- **Mercado** (transportadora Lorry, mesma viagem): ~R$ 460/entrega (73–76% do nosso custo).
- **Cheio** (nosso, a 29% ocup): R$ 632 — ineficiência, não custo do pedido.
A taxa R$ 200 fica acima do marginal e abaixo de mercado/cheio. **Não deve cobrir o R$ 632** — cobrar a ociosidade ao cliente o empurraria para retira/concorrente. O R$ 632 se ataca por consolidação + frota (operacional), não pela taxa (comercial). O gatilho de despacho impede o pedido pequeno disparar viagem dedicada.

Benchmark Lorry/entrega por região (próprio vs terceiro): GSP R$ 632→460 (−27%) · Interior denso ~R$ 1.000→675 (−33%) · esparso R$ 1.700–4.200→1.200–2.840 (−30%).

Adicionados ao doc: bloco "Os três custos — por que a taxa não cobre o custo cheio" (Fase 1) + tabela benchmark transportadora por eixo (Fase 2e). Doc 6 pgs.

## v11 — Deck do conselho (minimalista)
`Logistica_Guarulhos_Deck.pptx` (10 slides, python-pptx + 4 gráficos matplotlib, paleta navy+laranja Georgia/Calibri 16:9). Build: `build_deck.py`. Estrutura: capa · a questão (3 KPIs) · cross-subsídio (cobrado×real) · ociosidade (R$/kg região) · Fase 1 mínimo (tabela) · três custos (R$200 vs R$632) · Fase 2 tarifa (2 cenários) · consolidação (curva 632→312) · governança (4 cards) · decisão. QA visual nos 10 slides; corrigido espaçamento tabela×texto no slide 7.

## v12 — Tabela frete por região com valor do RAF (confronto romaneio)
Gustavo pediu tabela por região (frete, R$/kg, R$/entrega, qtd, valor, peso) usando valor do RAF confrontado com romaneio. Cruzei as 2.860 NFs de entrega com o RAF (filial 1, via 3 blocos string_agg) — 2.539 casaram (89%).

**ACHADO: o valor do romaneio infla ~16% no agregado** (R$ 41,2 mi romaneio vs **R$ 35,6 mi RAF**) porque repete o valor da NF em linhas múltiplas. Concentrado em **Campinas (+49%)** e **Zona Oeste (+23%)**; ABCD/Zona Leste batem (1-3%); Vale/Bragança/Limeira batem. RAF é a base oficial.

**Consequência**: o frete real sobre o valor entregue **não é 4,30% — é 4,97%** (R$ 1,77 mi ÷ R$ 35,6 mi RAF), **2,7× o 1,85% cobrado** (antes eu usava o valor inflado do romaneio no denominador). Validação no doc atualizada.

Tabela por região (jan–mai, RAF): Zona Oeste 394 ent/691t/R$7,31mi/frete R$331mil/0,48/R$841 · ABCD 532/428/4,86/286/0,67/537 · Campinas 224/369/6,00/231/0,62/1.029 · Bragança 5/51/0,55/21/0,41/4.170 ... TOTAL 2.344/2.820t/R$35,6mi/R$1,77mi/0,63/R$756. CSV: `brutos_romaneios/frete_por_regiao.csv`.

Doc atualizado: tabela região detalhada (RAF), frete% 4,97%, nota de método (valor RAF). **Pendência**: o custo-de-servir por cliente ainda usa valor romaneio no mc_entregue — recalcular com valor RAF deslocaria a distribuição para mais deficitários (frete% maior). Parqueado.

## Pendências / próximos passos
1. Definir **data de vigência** da Fase 1 + comunicado a vendedores/balcão; campo de classificação GSP×Interior no pedido.
2. Calibrar o **custo marginal de parada** real (hoje estimado R$40–120) — afina os cortes.
3. Fase 2: redefinir regiões + tarifa R$/kg + governança trimestral + make-vs-buy de frota por eixo + simulador de frete no orçamento + de-para CEP→região no ERP.
4. Confirmar tratamento de **fretes de terceiros** e **transferências** (Tipo=Transporte, 318 linhas) na política — hoje fora do universo.

## Notas técnicas
- npm bloqueado no sandbox (403) → documento feito com **python-docx 1.2.0** (não docx-js).
- Região 12 (FORA DA ÁREA) e 55/56 (processos internos) excluídas do universo.

## Conexões
- [[2026-06-12 — Política Logística Guarulhos — doc e deck v2 em 3 partes]]
- [[Sistema Operacional Comercial/04 RAF/11 - Metodologia de Custeio da Logística]]
- [[2026-06-19 — Lançamento Comercial Material Trefilado (e-mail aos gestores)]]

---

## Atualização 19/06/2026 — itens fechados para o e-mail da política de frete

Definidos dois textos-padrão durante a redação do e-mail da Política de Frete (a ser enviado à equipe de vendas). Vigência da política: pedidos a partir de **22/06/2026**. Mínimos confirmados: **Grande SP** 500 kg ou R$ 4.000; **Interior** 800 kg ou R$ 7.000. Taxa abaixo de ambos: **R$ 200 (Grande SP) / R$ 350 (Interior)**. Critério vale para **qualquer produto** da unidade (não nasceu só do trefilado, mas a revisão foi disparada pela entrada da linha). Contexto: antes **não havia mínimo na Grande SP** e o **Interior exigia 600 kg** — a mudança principal é passar a um piso de **VALOR ou PESO**.

### 1. Cláusula-padrão de frete na Proposta Comercial (texto voltado ao cliente)

> **FRETE INCLUSO** para pedidos que atingirem o valor ou o peso mínimo nas regiões atendidas. Abaixo disso, os pedidos podem ser retirados na unidade ou entregues mediante taxa de entrega. Valores conforme a Política de Frete vigente **na data do pedido** (sob consulta).

Decisões de redação:
- "FRETE INCLUSO" escolhido em vez de "frete grátis" (não é grátis — custo embutido no preço; "grátis" soa promocional e abre flanco para pedir desconto na retirada) e em vez de só "CIF" (técnico demais para cliente leigo). Opção de casar: "FRETE INCLUSO (CIF)".
- **Sem valores na cláusula** — limiares e taxa ficam na "Política vigente" (fonte única; revisar política não obriga reescrever proposta).
- "**na data do pedido**" trava qual versão da política governa (proteção jurídica quando a política mudar entre proposta e pedido — CC arts. 427–429).
- Condição de validade da cobrança: a taxa precisa ser **fornecida quando o cliente consultar** e **constar na O.S./confirmação antes do faturamento** — é isso que transforma "sob consulta" em consentimento. (Validar com jurídico/contador AFS.)

### 2. Regra para a equipe de vendas — como informar a taxa (texto interno, com valores)

> **Como informar ao cliente sobre a taxa de entrega**
> - A taxa cobrada não pode ser surpresa: o cliente precisa saber e aceitar **antes do fechamento**, sempre por escrito (proposta, e-mail ou WhatsApp). Combinado verbal pode gerar ruído na comunicação.
> - Quando o pedido ficar abaixo do valor **e** do peso mínimo:
>   - Tente completar a carga com outros pedidos do cliente (elimina a taxa); ou
>   - Ofereça as duas opções: retirar na unidade (com prioridade) ou pagar a taxa de R$ 200,00 (Grande SP) / R$ 350,00 (Interior).
>   - Com o aceite do cliente, emita a O.S. já com a taxa.

Notas:
- **WhatsApp escrito tem valor de prova** (mensagem com valor + "ok" do cliente serve como aceite). Ligação sem registro, não.
- Ponto em aberto / escolha do Gustavo: o texto final suavizou "combinado verbal não vale" para "pode gerar ruído na comunicação". Para **sustentar a cobrança** em contestação, o registro por escrito é o que protege — se o objetivo for blindar a cobrança (não só orientar clareza), considerar firmar para "sem registro por escrito, não emita com taxa".
- Consolidação de carga ficou como **primeira tentativa** (reduz taxa cobrada, melhora relação) — não imposta rigidamente; vendedor avalia.
