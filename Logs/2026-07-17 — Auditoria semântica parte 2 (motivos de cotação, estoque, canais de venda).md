---
data: 2026-07-17
tipo: log
status: vigente
projeto: Portal SAC360 (afs-lake)
---

# Auditoria semântica — parte 2 (áreas não cobertas em 16/07)

Continuação da auditoria disparada pelo caso "Consumo Próprio". Três áreas:
motivos de cotação bucket a bucket, reservado/regulador do estoque, distinção
agente × representante × vendedor. Nenhuma mudança de código aplicada —
tudo abaixo aguarda confirmação.

## A) Motivos de cotação — 22 códigos enumerados, bucket a bucket

Mapeamento completo `cod_motivo → bucket` (2026, encerradas, R$ valor_total):

| Bucket hoje | Códigos | R$ 2026 | Observação semântica |
|---|---|---|---|
| Orç. prévio | O | 313,1M | ok — fora da disputa real |
| Preço | $ 1 2 3 4 5 6 7 8 9 A | 114,4M | ok — concorrente nomeado já extraído (Trefita/Torres, Açovisa, Açotubo, Usinas, GGD…). Nota: **$ "Sem informação" = R$ 48,9M, 43% do bucket Preço** — perda "por preço" sem saber pra quem |
| Outros | X B W D E F Y Z | 65,3M | **bucket-lixo: mistura 4 semânticas distintas** (ver abaixo) |
| Cancelado | P | 3,7M | conta como perda no win rate ajustado hoje |
| Prazo | C | 3,0M | ok |
| Qualidade | (nenhum) | 0 | bucket existe no código mas nenhum código cai nele |

### Premissas pra confirmar (A)

1. **"Outros" esconde R$ 53,3M de "sem informação"** (X "Sem informação do
   vendedor" 38,4M + B "Motivo não informado p/ cliente" 14,2M + W "Encerrada
   por WS" 0,7M) = **~29% de todo o R$ perdido ex-orç-prévio**. Proposta: bucket
   próprio **"Sem informação"** — é disciplina de registro do time, não motivo
   de perda. Continua no denominador do win rate (perdeu de fato), mas separado
   na análise de motivos.
2. **Y "Faturado por outra unidade" (R$ 1,85M, 269 itens) está como PERDA** —
   mas a empresa ganhou (outra unidade faturou). No win rate consolidado é
   contagem invertida. Proposta: excluir da disputa real (como Orç. prévio) ou
   reclassificar "Ganhou (outra unidade)".
3. **P "Cancelado" conta como perda na disputa real** (`disputa_real` só exclui
   Orç. prévio). Cancelada = não houve disputa. Proposta: excluir do denominador
   do win rate ajustado (R$ 3,7M; efeito ~0,5pp).
4. **D "Não tem LC aprovado" (R$ 6,0M)** = perda por CRÉDITO, não comercial.
   Vale bucket "Crédito" próprio? É alavanca da política de crédito, não do
   pricing.
5. **F "Procedência material não atende" (R$ 1,4M)** cai em "Outros" — é
   semanticamente "Qualidade" (bucket que existe e está vazio)?
6. E "Não tem o material" (R$ 3,25M) — perda por DISPONIBILIDADE (ruptura de
   estoque). Cruzável com a análise Pendentes×Estoque. Bucket próprio?

## B) Estoque — reservado e regulador

Fatos levantados (569 SKUs no EstoquePadrao):

- **Reservado é sempre ≤ 0** no export (convenção de sinal Softcomp); 151 SKUs,
  591,5 t reservadas (1,8% das 33.179 t). 4 SKUs com |reservado| > estoque
  (vendido além da posição, gap 1,4 t).
- **`Quantidade prevista` = estoque − |reservado| (+ OC em aberto quando há)** —
  posição líquida projetada.
- **⚠ ACHADO: `Estoque regulador` aparenta estar em MESES-alvo, não em kg.**
  Valores são só {3, 4, 5, 8} e correlacionam com a classe: Trefilado=4,
  Forjado=5, Laminado importado=8, Laminado nacional (1020/1045)=3 — bate com
  lead time (nacional 45d, forjado 75d, importado 180d) + margem. **Mas a
  `vw_estoque` compara `estoque_kg < regulador`** — condição que só dispara com
  estoque ≈ 0. Os 12 CRITICO de hoje são todos estoque zerado.
- **⚠ ACHADO 2: cobertura usada ("Meses de estoque" do Softcomp) NÃO desconta a
  reserva** — conferido ao centavo (527.103/17.234 = 30,59 ✓). A definição
  canônica em `definicoes.py` manda `(estoque − |reservado|)/CMM`. Portal E
  Painel de Estoque JS usam o número cru do Softcomp → definição diz uma coisa,
  implementações fazem outra.
- **Impacto simulado da correção dupla** (cobertura líquida + regulador em
  meses): CRITICO 12→17 (**15 SKUs em ruptura real hoje escondidos em
  REPOSICAO**; 10 falsos CRITICO saem — estoque 0 com demanda 0). 7 SKUs
  EXCESSO virariam OK por cobertura nula (CMM=0 — na verdade estoque morto,
  tratar como EXCESSO na implementação).

### Premissas pra confirmar (B)

1. `Estoque regulador` = cobertura-alvo em **meses** definida no Softcomp por
   classe de material (quem define? é política viva ou cadastro fóssil?).
2. Se sim: corrigir `vw_estoque` → CRITICO = `cobertura_liq < 1 E cobertura_liq
   < regulador`; e cobertura passa a ser líquida de reserva (alinha com
   `definicoes.py`). Espelhar no Painel de Estoque JS.
3. Reservado = material comprometido com pedido emitido ainda não faturado?
   (ou inclui bloqueios de qualidade/consignação?)

## C) Canais de venda — agente × representante × vendedor

**Fato central: NÃO existe campo sistêmico distinguindo as classes.** O campo
`ABCVEN_NOM` (→ `vendedor` no portal) mistura 4 semânticas:

1. **Vendedores internos** (pessoas): Reynaldo, Elaine, Fabiana… (~26 nomes)
2. **Agentes/representantes PJ**: Açotec ×2, Longhi, BRL, Nilson Franca,
   E.L. Manto, Sousa e Juca — juntos R$ 13,1M em 2026 (Açotec-SCA é o maior
   "vendedor" da empresa: R$ 8,9M)
3. **Buckets organizacionais**: "Unidade de São Carlos/Piracicaba/Rio Preto/
   Caxias", "Estrategico - Piracicaba", "Clientes em Desenvolvimento",
   "Prospecção MKT" — R$ 8,1M sem dono pessoa física
4. **None**: 15 clientes, R$ 0,05M

Marcadores indiretos que existem hoje:
- `ABCDIG_NOM` (digitador) é quase sempre apelido do próprio vendedor, MAS
  revela operação: "Açotec - São Carlos" digitado por "Fabiana - SCA"/"Odair -
  SCA" (interno operando conta de agente); prefixo "Rep - Marcelo" em Marcelo
  Evangelista sugere representante.
- Comissão paga (`ABCCUS_COM_COB > 0`) marca linhas COM agente — e a razão
  cobrado/pago confirma a regra do dobro: internos ≈ 2,0; Açotec = 1,0
  (exceção conhecida); "Clientes em Desenvolvimento" = 1,0 mas é 100%
  Exportação (coberto pela exceção de 14/07). **Zero desvios novos.**
- As exceções em `definicoes.py` funcionam por match de SUBSTRING no nome —
  frágil: renomeou no Softcomp, quebrou silenciosamente.

### Premissas pra confirmar (C)

1. Classificação oficial dos ~43 valores de `ABCVEN_NOM` em
   {interno, agente, representante, casa/bucket} — proposta: tabela de-para
   versionada (YAML em `MotorAnalitico/config/`, mesmo padrão dos bloqueios)
   → coluna `canal_venda` na `vw_faturamento`. Análises por vendedor passam a
   poder separar pessoa × PJ × bucket (hoje Açotec aparece como "vendedor" no
   Stoplight, ranking, %Preta…).
2. Agente ≠ representante na AFS? (comissão, vínculo, quem emite pedido?) Ou é
   distinção só de nomenclatura?
3. "Estrategico - Piracicaba" (R$ 3,1M, 3 clientes, comissão razão 2,0 ok) —
   o que é? Conta-casa de diretoria?

## Respostas do Gustavo (17/07 — tarde)

**A) Motivos — decidido em parte:**
- **Y "Faturado por outra unidade" → IGNORAR na conversão.** Todo pedido exige
  cotação antes; a outra unidade emitiu e ganhou a própria cotação — contar Y
  como perda é dupla contagem invertida. ✅ decidido.
- **X "Sem informação do vendedor"**: contexto operacional revelado — é o
  **encerramento em massa da virada do mês** (Gustavo encerra as pendentes do
  mês anterior no 2º-3º dia útil; vendedor deveria encerrar com motivo real ou
  rolar a data de emissão, mas nem todos fazem). Se o cliente retoma a
  negociação, emite-se NOVA cotação → **duplicata**: a ganha nova conta como
  vitória e a X antiga como derrota do MESMO negócio. Gustavo propõe ignorar
  na conversão; recomendação Claude: concordar, e generalizar como bucket
  **"Encerramento administrativo" = {X, W, P, Y}** fora da disputa real
  (mesma classe: encerramentos sem desfecho de mercado). Impacto: win rate
  ajustado 2026 **39,7% → 46,4%** (+6,7pp). X segue visível como métrica de
  DISCIPLINA por vendedor (% de cotações encerradas sem informação).
  ✅ conjunto {X,W,P,Y} APROVADO pelo Gustavo (17/07, tarde).

**C) Canais — CONFIRMADO com cadastro oficial** (`Lista de Vendedores.xlsx`,
coluna Equipe = Unidade + INT/PJ/REP/EST). Regras de remuneração e exceção
Açotec documentadas em [[Definições Canônicas de Negócio (SAC360)]] (seção
"Canais de venda"). Cobertura verificada: RAF casa 100% pelo **Nome**;
Cotações casam pelo **Nome Fantasia**. Açotec: são CLIENTES atendidos pelos
gerentes das unidades (comissão por indicação/lobby, não dobra) — refina a
exceção de 14/07. Os dois xlsx (Motivos de perda + Lista de Vendedores) devem
virar fontes de referência em `01_Brutos/` (mesmo padrão TiposNF) quando a
implementação rodar.

**B) Estoque — CONFIRMADO** (17/07, tarde): "tem que levar em consideração a
qtd reservada para definir o disponível ou a comprar" — cobertura líquida de
reserva + regulador lido como cobertura-alvo em meses.

## Implementação (17/07 — mesma sessão, A+B+C aprovados)

- `definicoes.py`: `MOTIVO_ENC_ADMIN` + `MOTIVOS_ADMIN_CODIGOS` (P/W/X/Y) +
  `SQL_DISPUTA_REAL` (fragmento canônico do denominador); semântica de estoque
  documentada (disponível líquido, regulador em meses).
- `cotacoes/enriquecer.py`: bucket `Enc. administrativo` por cod_motivo (com
  fallback textual); bucket `Cancelado` morreu (P entrou no administrativo).
- `build_gold.py`: 3 fontes bronze novas (tipos_nf, lista_vendedores,
  motivos_perda) + `vw_vendedores` (dim canal) + `canal_venda` em
  vw_faturamento (join por Nome) e vw_cotacoes (join por Nome Fantasia) +
  `cod_motivo` exposto + `disputa_real` novo + `vw_estoque` reescrita
  (disponivel_kg, cobertura_meses líquida, cobertura_meses_bruta, CRITICO por
  meses vs regulador, estoque morto CMM=0 → EXCESSO).
- Portal: funil/visão geral/relatório/cotações no denominador novo; bloco novo
  **"Disciplina de registro"** (% R$ encerrado cód. X por vendedor) na página
  Cotações; glossário e contexto da IA atualizados.
- `gerar_painel_estoque.py`: meses líquidos de reserva (alinha com o JS do
  template, que já fazia certo).
- Brutos: `01_Brutos/{TiposNF,ListaVendedores,MotivosPerda}/` com README,
  contratos regenerados (make receber já aceita), guarda anti-drift limpa.
- Testes: enricher 59/59; test_sync 21/21; test_gold com testes novos
  (disputa nova, cobertura líquida, regulador≤24, estoque morto, cobertura
  ≥99% do canal_venda).

Números pós-implementação: WR ajustado 2026 **46,4%** (era 39,7%); CRITICO
**17 SKUs** (era 12, todos zerados); canal_venda cobrindo ~100% do R$.
