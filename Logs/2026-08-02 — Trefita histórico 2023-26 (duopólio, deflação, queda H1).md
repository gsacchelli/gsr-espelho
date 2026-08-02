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

**Página no portal (mesmo dia):** `🔒 Restrito → Concorrência (Trefita)` — duopólio anual, acabamento H1×H1, unidades, busca de cliente com wallet share e itens deles. Gate: só aparece na máquina com o parquet; lê o dado DIRETO (nunca via gold — o gold alimenta relatórios de gerência). ⚠ Lição TCC de novo: launchd não lê `~/Documents` → dado movido pra **`~/dev/concorrencia/`** (fora do TCC, fora do git, fora do iCloud).

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
