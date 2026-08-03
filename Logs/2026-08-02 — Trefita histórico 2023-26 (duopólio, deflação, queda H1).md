# Trefita/Torres — série histórica 2023-jun/2026

**Data:** 02/08/2026
**Fonte:** Gustavo entregou os Pedidos Emitidos da TREFITA/TORRES jan/23-jun/26 (305.899 linhas, layout Softcomp com faixas F1/F2/F3, kg, prazo, setor). **Atualização mensal combinada**: tabela completa do ano corrente substitui `PedidosEmitidos_T_2026.xlsx` em `~/Documents/Concorrencia/Trefita/01_Brutos/` → rodar `processar_trefita.py`. Dado segue FORA do lake (política 27/07).

## O quadro (pedidos emitidos, ex-intercompany)

| Período | ELES R$ MM / mil t / R$kg | NÓS R$ MM / mil t / R$kg | Share nosso (R$) |
|---|---|---|---|
| 2023 | 313,9 / 19,6 / 16,05 | 282,1 / 18,1 / 15,54 | 47,3% |
| 2024 | 321,4 / 23,9 / 13,46 | 276,2 / 21,3 / 12,97 | 46,2% |
| 2025 | 298,9 / 21,6 / 13,82 | 273,6 / 20,9 / 13,09 | 47,8% |
| **2026 H1** | 148,3 / 11,2 / 13,20 | 114,7 / 8,5 / 13,53 | **43,6%** |

## As 4 leituras

1. **Duopólio equilibrado até 2025** — share nosso estável em 46-48% do combinado por 3 anos.
2. **2026 H1: o alarme é a NOSSA queda, não o ataque deles.** H1×H1: eles −5,1% (156,3→148,3); nós **−19%** (141,6→114,7). O mercado de distribuição encolheu pros dois — consistente com usinas atendendo no prazo (fenômeno PROK em escala) — mas caímos 4× mais rápido. Investigar ONDE (UF × liga × cliente) é a próxima análise.
3. **Deflação paralela de preço**: eles 16,05→13,20 (−18%), nós 15,54→13,53 (−13%). Movimento de price-follower mútuo; em 2026 H1, pela 1ª vez, nosso PU de mix fica ACIMA do deles. ⚠ PU compara mix (TORRES forjado puxa o deles); comparação justa é liga×perfil×acabamento.
4. **Único vetor de crescimento deles: TREFITA SC** (H1: 4,3→3,5→7,1→**8,4 MM**, +18% a/a) — o buraco SC/PR que a foto de mai-jun já mostrava está COMPONDO ano a ano.

## PROK: caso encerrado com a série completa

PROK BRASIL comprou **R$ 2.351 da Trefita em 3,5 anos** (1 pedido em 2023; o resto do "PROK" é PROKORTE, caldeiraria SP, R$ 36k na TORRES). Não existe concorrente de distribuição na PROK — a queda dela conosco (R$ 3,6 MM→176k) é usina/forjaria servindo direto. Estratégia registrada no log do Vigia (Parte 3): disponibilidade premium quando a usina falha, esforço mínimo no resto.

## Adendo (mesmo dia, tarde) — T3 incluída, tese Wagner testada, página no portal

**T3 (TREFITA-3, filial MG) faltava na 1ª leva** — Gustavo reenviou com ela: R$ 53-64 MM/ano. Números revisados (H1): share nosso 42,0% (2023) → 43,1% → 43,2% → **39,9% (2026)**; o grupo deles é ~30% maior que nós. Cadastros deles não são unificados (T1/T2/SC × T3 × Torres) — cadastro unificado com coluna de unidade a caminho.

**Tese do Gustavo ("política comercial do Wagner: subiu laminados e principalmente forjados") — TESTADA:**
- Cotações 2026: Ganhou R$ 142,0 MM × Perdido-por-Preço R$ 132,6 MM — no TOTAL ainda ganhamos mais, mas a razão caiu de 1,23 (2025) pra 1,07. **No FORJADO inverteu: perdido 44,8 > ganho 32,2.**
- Like-for-like H1×H1 forjado: nosso PU **+7,7%** (17,33→18,66) × deles **−2,5%** (17,78→17,34) — nosso preço CRUZOU o deles; receita nossa −23,4% × deles −5,9%.
- Laminado: nós PU −4,0% / receita −19,5%; eles PU −6,2% / receita −3,2% — eles cortaram mais fundo e seguraram o volume.
- **Migrações nomeadas** (caiu conosco E cresceu lá): RENK-ZANINI (−1,6 MM ↔ +2,4 MM lá; wallet nosso 12%→26%→**45% em 2025**→**16%** em 2026 — a conta que tínhamos conquistado; compra forjado redondo grande 18CrNiMo7-6/4140/4340 na T2) e WEG CESTARI (−1,0 ↔ +0,85). SEW/NETZSCH: eles já dominavam (posição nossa marginal). HOWDEN/MARCHESAN/SUPERIOR: mercado caiu pros dois.

**Página no portal (mesmo dia):** `🔒 Concorrência (Trefita/Torres)` — duopólio anual, acabamento H1×H1, famílias (gap), UF, prospects CNPJ, wallet share por cliente. **Acesso (decisão Gustavo, tarde): botão no rodapé de Entrada de Pedidos (fora do menu lateral) + senha** (SHA-256 no código; gate de privacidade — a segurança real é o dado só existir nesta máquina). Lê o dado DIRETO (nunca via gold — o gold alimenta relatórios de gerência). ⚠ Lição TCC de novo: launchd não lê `~/Documents` → dado movido pra **`~/dev/concorrencia/`** (fora do TCC, fora do git, fora do iCloud).

## Adendo 2 (mesmo dia) — cadastro unificado, famílias canônicas, UF e prospects

**Cadastro unificado recebido** (32.336 clientes; mapa: T1/T2/SC→cadastro T2, TREFITA-3→T3, TORRES→TO) → pedidos deles com **CNPJ em 99,8% das linhas** (match determinístico com nossa base). **Famílias**: as linhas deles passaram pela NOSSA régua (motor RAF via `processar_trefita.py`) — cobertura 74,3% do R$ (o resto é fora da nossa linha). Página do portal ganhou: **Famílias (gap nós×eles), UF e Prospects** com seletor de ano + H1.

**Achados H1 2026:**
1. **TREFILADO é o maior buraco de produto** — famílias R T 12,70-101,60: 1045 gap R$ 8,1 MM (share nosso 6%!), 4140 gap 3,9 (15%), 1020 gap 3,4 (7%), 8620 gap 2,1 (18%). ~R$ 17,5 MM/semestre no conjunto — é a T1 deles inteira. **Valida o lançamento comercial de trefilados de 19/06** (log próprio): o mercado existe e está mapeado cliente a cliente.
2. **Forjado grande** (4140/4340/1045 R F ≥230mm): gaps de 1,4-4,0 MM cada com share nosso 20-38% — o mesmo território do erro de preço (adendo 1).
3. **Onde ganhamos**: laminado fino — 4140/1045/8620 R L 12,70-101,60 com share 56-65%. ⚠ **CORREÇÃO (desconfiança do Gustavo, procedente)**: o "20MnCr5 100% nosso" era ARTEFATO — eles grafam `20MNCR5` (caixa alta) e o lookup do RAF é match exato; com fallback case-insensitive no processador, **eles vendem R$ 2,98 MM de 20MnCr5 no H1/26** (nós R$ 5,8 MM — share nosso ~66%, liderança real mas não exclusividade). Cobertura de família subiu 74,3%→76,4%.

**Auditoria completa do "sem família" (23,6% do R$ da série = R$ 302 MM) — NÃO é erro de match, é linha que a nossa régua não descreve:** 18CrNiMo7-6 R$ 65 MM (forjado grande 198-1570mm + anel usinado + laminado — a liga NEM EXISTE nas nossas 207 famílias, e é o aço da RENK/redutores); trefilado sextavado/quadrado ~R$ 48 MM (a T1 faz barra trefilada não-redonda); 1045 redondo RETIFICADO fino R$ 31 MM; forjados >800mm; engenheirado da TORRES R$ 88 MM (hollow bar/anel sob desenho, liga vazia). Expander "Fora da nossa régua" na página lista tudo por ano. **Pergunta estratégica que isso abre: quais dessas linhas são decisão de não-ter e quais são buraco de catálogo?** (18CrNiMo7-6 e trefilado não-redondo merecem resposta explícita.)
4. **UF**: **MG é o buraco absoluto** (eles R$ 29,8 MM × nós 3,2 — share 10%; é a T3 jogando em casa); SC 35%, PR 19%, RJ 35%. RS seguimos líderes (55%); SP 46%.
5. **Prospects**: **1.566 CNPJs compraram deles no H1 e NÃO EXISTEM na nossa ListaClientes** — R$ 23,4 MM que nunca nos cotou. Top: C.A.W. Projetos (PR, 748k), CSM Engenharia (SC, 419k), Multi Supri (SP, 395k), PRW (MG, 247k). Lista completa na página (aba Prospects).

## Adendo 3 (mesmo dia) — grafias validadas, famílias do 17CrNiMo6 destravadas, monitor armado

**Grafias**: Gustavo validou as 14 pendentes → consolidadas em `criterios_raf_overrides.yaml` (25CrMoS4→20MnCr5 caso SEW; 8630M→8630 Oil&Gas; 414 e "4140 PET"→4140; 1016=canônico próprio "baixa liga", NÃO vira 1020; ST52→ST52.3 do catálogo; A-504/ASTM 668 classes→A504/A668 Carbono "vendemos sim"; GGG*=ferro fundido FORA; SUC-CAVACO/55006/"10" ignorados de propósito). ⚠ anotado: catálogo tem 'ASTM A668'→filtro 'A688' — possível typo antigo, conferir.

**BUG HISTÓRICO CORRIGIDO — famílias do 17CrNiMo6 eram inalcançáveis desde sempre**: existiam 23 famílias no xlsx sob o aço 'D17-18CrNiMo7-6', mas a padronização converte tudo pra '17CrNiMo6' e o match era exato → nenhum pipeline as alcançava. `raf/lookup.py` agora indexa famílias pelo aço PADRONIZADO (identidade pros demais; 5 checks novos na suite, 140/140). Efeito Trefita: cobertura 76,4%→**80,9%**; **R$ 37,6 MM deles em famílias 17CrNiMo6** (+R$ 19,5 MM CrNiMo em Fora Padrão: >800mm/anel) — a liga agora APARECE na tabela de gap, com share nosso 0%.

**Monitor estratégico (pedido do Gustavo "precisamos monitorar")**: `vigia.yaml::materiais_monitorados` — cotação pendente de 17CrNiMo6 (aço padronizado OU 'CRNIMO' no texto) alerta na hora, qualquer valor. **Baseline revelou: a demanda JÁ ESTÁ no nosso funil — 42 itens / R$ 1,25 MM pendentes HOJE** (SEW-Indaiatuba R$ 967k com item parado há 31d, CESTARI, ADDN, RENK-ZANINI...). Cotamos sem ter a linha — provável preço de referência ou compra-se-vier. Semeados na baseline; daqui em diante só cotação NOVA alerta. Testes: 15 no test_vigia.

## Próximas análises (backlog)

- [ ] Preço like-for-like POR FAMÍLIA (agora possível: mesma régua dos dois lados) — a medida final da "política agressiva"
- [ ] % abaixo da própria F3 deles ao longo do tempo (o "39% fura tabela" de mai-jun em série)
- [ ] TREFITA SC e T3/MG: clientes e ligas que sustentam as praças — mapa de entrada
- [ ] Sazonalidade mensal + procedência (importado×nacional) deles
- [ ] Wallet share por CNPJ no histórico (upgrade da busca por nome)
- [ ] Campanha trefilado: cruzar os gaps R T com os 1.566 prospects (lista de ataque pronta)

## Adendo 4 (mesmo dia, noite) — instrumentação das decisões + Radar série completa

Aprovação do Gustavo aos 3 instrumentos + filtro de ano: (1) **Prêmio mês a mês** na página do portal (like-for-like por família × mês, ponderados Forjado/Laminado — o velocímetro da recalibração que será proposta ao Wagner em 03/08); (2) **alerta de movimento de preço deles** no processar_trefita (último mês vs média 3m, |Δ|>5%); (3) **placar de campanha** — `Trefita/campanhas.json` com os 50 alvos trefilado-Arcelor (baseline 02/08) × funil nosso por CNPJ, na página. **Radar regenerado com a série completa** (2023-26, R$ 1,28 BI deles; grupos: A 337MM · B perda silenciosa 380MM/857 cli · C 11MM · D dormente 420MM · E 131MM) + filtro ANO na barra + UX: nome preferindo cadastro Sacchelli (laranja = sem cadastro nosso), "Nossa fatia"→"Wallet nosso %", linhas compactas. Encadeado: processar → radar em 1 comando. Botão de acesso: Entrada de Pedidos → 🔒 Concorrência (senha) → página + botão do Radar.

## Adendo 5 (02/08, noite) — ERRO GRAVE no elo do Radar, achado pelo Gustavo (caso SEW)

**Sintoma:** SEW aparecia com "nada" em R$ conosco; o print do SP8001A mostrava **R$ 1.377.395 no H1/26** (cod 8156). O número da PÁGINA do portal estava certo (bate ao centavo) — o furo era só do **Radar**.

**Três bugs empilhados, todos no elo cliente-nosso ↔ cliente-dele:**
1. **Elo por NOME via faturamento** — o Radar ligava nossos pedidos ao cliente dele pelo nome (vw_pedidos não tinha `cod_cliente`). Deixava **21,7% do nosso R$ sem dono**. Corrigido: passou a ler `pedidos_enriquecidos` (tem cod) → elo **cod → raiz CNPJ → nome**.
2. **Cliente rachado por filial** — SEW deles usa 2 CNPJs do mesmo grupo (…002052 e …000432): o R$ deles ficava num registro e o nosso elo em outro, com wallet zerado nos dois. Corrigido: cliente do Radar passou a ser o **GRUPO ECONÔMICO** (raiz de CNPJ) — mesma doutrina da segmentação ("SEW/WEG = 1 mesa, não 7").
3. **Fuzzy de nome ROUBAVA código** (o mais perigoso): 'MULT USI' (R$ 2,9 mil na Trefita) casava por semelhança com o nosso 'MULT ENGRENAG.' e **levava os R$ 3,84 MM** de pedidos da MULT ENGRENAGENS — porque `cod2ci` é dict e o último a escrever vencia (ordem instável entre execuções!). O mesmo padrão inventava venda em AGT (deles) → 'AGT ESTRELA' (nosso, outra empresa), MM SANTOS, SIGMA, VIA PORTO, RDB.

**Regra fechada (02/08):** **documento manda; nome só quando não há documento.** Se o cliente dele tem CNPJ e esse CNPJ/raiz não existe na nossa base, a resposta honesta é "não é nosso cliente" (grupo E) — nunca casar por semelhança. Precedência no elo: CNPJ > grupo > nome, e um código **nunca troca de dono**.

**AUDITORIA AUTOMÁTICA embutida no gerar_radar** (regra da casa: número exibido tem que ser o que o dado sustenta): a cada geração, compara o R$ nosso de cada cliente casado contra a soma dos pedidos dos códigos do mesmo grupo econômico e **lista as divergências >2%**. Hoje: `✓ todo cliente casado bate`. Conferência externa contra o gold na mesma janela: **20/20 dos maiores clientes conferem (<2%)**.

**Efeito nos números:** SEW passa de R$ 0 → **R$ 9,08 MM (wallet 22%)**; MULT ENGRENAGENS de 0 → 3,84 MM; grupo E sobe (4.098) porque quem não tem match por documento deixou de ser inventado. Ligação total do nosso R$: 80,3% (o resto é cliente que não compra da Trefita — correto).

**Lição registrada:** match por similaridade de nome em análise estratégica é dívida escondida — só sobrevive com documento como âncora e auditoria automática que quebre quando o número não fecha.

## Adendo 6 (02/08, noite) — plano quantificado para o Wagner: o problema tem DUAS naturezas

Cruzando **prêmio de preço × margem REAL da família** (RAF H1/26), as famílias caras se separam em dois blocos com decisões opostas — e isso muda a tese da reunião de "baixar preço do forjado" para algo bem mais preciso:

**O que a política fez (forjado, RAF H1):** 2025 R$ 25,9 MM / 1,92 mil t / MC 25,9% = **R$ 6,7 MM de MC** → 2026 R$ 22,0 MM / 1,53 mil t / MC 29,3% = **R$ 6,4 MM**. Subimos a margem 3,4 pp, perdemos 20% do volume, e a **MC em reais caiu 4%**. Preço médio +6,6% (13,49 → 14,38 R$/kg líq). O trade não pagou.

**BLOCO 1 — corrigir preço** (R$ 13,1 MM nossos; MC média 41,9%; prêmio 13-34%): 1045 R F 230-355, 4140/1045/1020/4340/8620 R L 230-355, 4140 R F 230-355, 8640 R L 101-203. Corte médio **11,7%** com piso de margem de 30% por família → MC média cai para 34%. **Custo: R$ 1,54 MM de MC/semestre**; mercado deles nessas famílias: R$ 16,9 MM (1,3× o nosso).

**BLOCO 2 — não é preço, é CUSTO** (R$ 10,7 MM nossos; eles R$ 25,3 MM): forjado ≥355mm, trefilado fino, 20MnCr5 R L. Estamos 12-36% acima **com margem de só 23-30%** — cortar preço aqui destrói margem sem recuperar volume. ⚠ **CORREÇÃO do Gustavo (03/08): a TORRES NÃO é forjaria** — é distribuição de aço focada em forjados, com parque de serras e tornos para desbaste. Minha explicação de 'verticalização' estava errada e foi removida do dossiê. O dado revisado é mais duro: a TORRES vende peça desbastada/pré-shape a **18,10 R$/kg** (o produto mais caro do grupo) e por isso *inflava* a média deles; comparando só contra a **barra pura** (T1/T2/T3/SC), nosso prêmio agregado sobe de +4,7% para **+8,7%** e nas famílias do Bloco 2 vai a 14-36%. Conclusão sustentada: vendemos barra mais cara que um concorrente que compra no MESMO mercado e ainda ganhamos menos margem nela → **custo de aquisição do forjado pesado está alto**. Pauta de SUPRIMENTO com pergunta aberta (sem dado nosso p/ responder): escala (eles giram R$ 50 MM/sem em forjado × nossos 22 MM), formato de compra (bitola padrão + ajuste na serra/torno × sob medida), lote e prazo.

Entregues: `Dossie_Preco_Forjado_Wagner_2026-08-03.md` (v3) e `Plano_Recalibracao_Familias.xlsx` (família a família: corte, MC antes/depois, volume p/ empatar). Reconquista dirigida: RENK-ZANINI, CALDEX, SUPERIOR, MARTIN, MULT ENGRENAGENS somam R$ 12,9 MM comprando deles com wallet nosso caído de 28-53% → 6-23%.

## Adendo 7 (03/08) — contexto Villares Metals do Gustavo + medição da redução de preço

**Contexto que o Gustavo trouxe (não estava em dado nenhum):** o Wagner apostou na **Villares Metals** desde o fim de 2025 — garantiu **500 t/mês** e, em troca, a Metals cobraria **10% a mais de qualquer concorrente**, inclusive Trefita/Torres (que também é distribuidor tradicional dela). A Trefita contornou por duas vias: (1) **>508 mm — importou direto**, recebeu em **abril/26**, e por isso não programou com a Metals; (2) **<508 mm — compra da Steel** (forjaria com aciaria), mais barata, qualidade inferior à Metals, mas **atende ~80% do mercado — poucos clientes exigem procedência Metals, preço decide**. Agora a Trefita parece estar voltando a programar com a Metals **com preços reajustados, mas ainda não repassou**.

**O dado confirma a história:** PU deles em forjado >508 mm caiu de ~21 R$/kg (2025) para **18,7-18,8 em abr-jun/26** (−12%) — exatamente a chegada do importado; e o volume dessa faixa **despencou em junho (95,8 t contra 145-190 t nos meses anteriores)** = estoque importado se esgotando. Do nosso lado, a MC mais baixa do forjado está justamente em **355-508 (26,2%) e 508-800 (26,5%)** contra 34,2% em 230-355 — o prêmio Metals num mercado que não paga por ele.

**Medição da redução de preços da semana de 27/07 (Gustavo: "não senti impacto"):** no FUNIL o impacto foi imediato — cotações de forjado (encerradas+pendentes, sem viés) passaram de 424 itens/R$ 7,5 MM/PU 19,03 (semana 20/07) para **545 itens (+29%) / R$ 9,7 MM (+30%) / PU 15,66 (−17,7%)**; pedidos da semana: **61,2 t**, a maior das 9 anteriores (média ~38 t), 5 dias completos, sem pedido atípico — e a **MARTIN voltou (12,1 t)**. A percepção estava certa quanto ao FATURAMENTO (pedido vira NF depois do prazo), errada quanto ao mercado.

⚠ **Mas a redução foi DESIGUAL** (PU cotado antes 29/06-20/07 × depois 27/07+, contra a barra deles abr-jun sem TORRES): no alvo em 4140 R F 558-800 (−3,6% → prêmio 3%), 4140 R F 355-558 (−3,1% → 5%), 8620 R F 355-558 (−6,6% → 4%), 4140 R F 230-355 (−6,0% → 7%), 8620 R F 230-355 (−8,2% → 8%); **passou do ponto** em 1020 R F 230-355 (−16,3% → **−6%**) e 1045 R F 558-800 (−12,5% → **−2%**) — abaixo do concorrente, margem cedida sem ganho; e **SUBIU** em 5 famílias que seguem caras: 1045 R F 355-558 (+0,8% → 15%), 1045 R F 230-355 (+8,5% → 11%), 4340 R F 355-558 (+4,1% → 20%) e **4340 R F 230-355 (+13,4% → 41%)**. Ressalva: PU médio também varia por mix — a lista diz onde conferir a tabela, não prova que a tabela subiu.

**Conclusão estratégica p/ a reunião:** a alavanca de preço FUNCIONA (funil +30% na 1ª semana) mas precisa de pontaria; e a janela é agora — o importado deles acabou, eles vão repassar o reajuste da Metals e ainda não mexeram no preço. Quem se posicionar antes do repasse recupera volume com margem.

## Adendo 8 (03/08) — ERRO DE MÉTODO na medição do corte, pego pelo Gustavo ("41% não parece correto")

**Ele estava certo de novo.** Duas falhas na tabela do adendo 7:
1. **Peça-com-serviço contamina PU/kg.** O caso: `HYDAC · 4340 Redondo Forjado 355,60 x 35mm · 27 kg · R$ 91.570 · PU R$ 3.354/kg` — disco cortado de barra Ø355, preço de peça usinada e não de aço. Nove linhas desse tipo (entre 1.739) somam R$ 318 mil em 401 kg e dominaram a média. **Guard-rail aplicado: excluir PU > 3× a mediana da família** (mesma lógica do PANEGOSSI).
2. **Comparei COTAÇÃO nossa × PEDIDO deles** — cotação é preço de tabela, pedido é preço fechado: infla nosso lado sistematicamente. O correto é pedido × pedido.

**Números corrigidos (pedido nosso abr-jul × pedido de barra deles abr-jun):** 4340 R F 230-355 = **+26%** (não 41%, e teve corte de 4,7% — não aumento de 13,4%); 1045 R F 230-355 **+28%**; 4140 R F 355-558 **+25%**; 1020 R F 355-558 **+23%**; 8620 R F 230-355 +20%; 4140 R F 230-355 +18%; **1020 R F 230-355 +16% (NÃO ficamos abaixo deles — alarme falso meu)**; 4340 R F 355-558 +14%; 4140 R F 558-800 +12%; 1045 R F 355-558 +10%; 8620 R F 355-558 +8%; **1045 R F 558-800 +2%** (único a vigiar: corte de 10,1% já cotado pode levar a negativo); 4340 R F 558-800 +1%.

**Lição p/ toda análise de preço:** (a) PU/kg só compara BARRA com BARRA — peça cortada/usinada tem que sair da conta; (b) comparar sempre o mesmo estágio do funil dos dois lados (pedido×pedido, cotação×cotação). As duas viraram regra no método de comparação com concorrente.

## Adendo 9 (03/08) — "não posso correr esse risco": guardas de ANÁLISE

Gustavo, depois do 4º erro que ELE pegou (SEW zerada, TORRES-forjaria, 20MnCr5, 41% do 4340): *"não posso correr esse tipo de risco de análise errada! o que precisamos desenvolver para criar um sistema confiável?"*

**Diagnóstico:** o `make auditar` (02/08) protege o dado NO GOLD. Os quatro erros aconteceram todos na camada seguinte — **análise ad-hoc**: script de sessão, join novo, base externa (Trefita fora do lake por decisão), agregação inédita. Essa camada não tinha teste, auditoria nem reconciliação. O padrão dos erros não era descuido pontual; era **ausência de rede numa camada inteira**.

**Construído:** `MotorAnalitico/analise/guardas.py` — seis guardas, cada uma amarrada ao caso real que a originou (o campo `porque` é obrigatório, mesma regra do `test_auditoria`):
| Guarda | Pergunta que faz | Caso-âncora |
|---|---|---|
| `sensibilidade_razao` | o número sobrevive sem a linha mais influente? | HYDAC (disco 27 kg, R$ 3.354/kg, movia o PU em 16%) |
| `concentracao` | 1 linha domina o total? | PANEGOSSI |
| `cobertura` | quanto do universo entrou na conta? | 20MnCr5 em caixa alta (R$ 26,7 MM invisíveis) |
| `reconciliar` | fecha com uma fonte independente? | SEW (R$ 0 no Radar × R$ 1,38 MM no gold) |
| `comparavel` | mesmo estágio/base/natureza/janela dos 2 lados? | cotação nossa × pedido deles |
| `pu_de_barra` | PU/kg comparando barra com barra? | peça-com-serviço contamina R$/kg |

`relatar()` **ergue `AnaliseSuspeita` quando há CRÍTICO — o número não circula.** 18 testes ancorados nos números reais dos erros (memória viva), no `make ci`.

**Prova de eficácia:** re-rodando a análise errada de ontem com as guardas ligadas, ela é **BLOQUEADA com 3 críticos** — inclusive um que nem eu tinha percebido (janelas diferentes: nossa cotação de jul contra pedido deles de abr-jun).

**Regra de trabalho que fica:** todo número que vai para reunião, e-mail ou tela passa pelas guardas e **declara o método** (fonte, janela, filtros, estágio do funil). Número sem método declarado não sai.
