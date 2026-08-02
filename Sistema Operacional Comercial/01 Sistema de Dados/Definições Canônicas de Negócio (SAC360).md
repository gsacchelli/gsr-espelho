---
data: 2026-08-01
tipo: referência viva
projeto: Portal SAC360 (afs-lake)
fonte de verdade: MotorAnalitico/definicoes.py
---

# Definições Canônicas de Negócio — SAC360

> **Fonte única no código:** `~/dev/afs-lake/MotorAnalitico/definicoes.py` — consumida por build_gold (views), portal, MCP server e agente analítico desde a Fase 2 da auditoria (11/07/2026). **Este documento é o espelho humano**; em divergência, o código vence e este arquivo deve ser atualizado. Auditoria completa: `06_Docs/Auditoria_Ecossistema_SAC360_2026-07-11.md` (repo).

## Faixas de preço (política comercial — intocável)
Verde · Amarela · Vermelha · **Preta** (PU abaixo do piso Vermelho). Todo Preto é pré-autorizado pela diretoria.

## Win Rate — três definições, sempre nomeadas
| Nome | Fórmula | Uso |
|---|---|---|
| Declarativo | R$ Ganhou ÷ R$ Encerradas | como marcado no Softcomp |
| Ajustado | R$ Ganhou ÷ (Encerradas − "Orç. prévio" − "Enc. administrativo") | disputa real (conjunto {X,W,P,Y} fora desde 17/07/2026; linha corrigida 02/08 — estava defasada vs `SQL_DISPUTA_REAL` do código) |
| Real | R$ Pedidos Emitidos ÷ R$ Encerradas | independe de marcação — KPI principal |

Grafia única do motivo: `Orç. prévio` (constante `MOTIVO_ORC_PREVIO`).

## %Preta — duas bases, nunca misturar
- **%Preta (faturamento)** — base RAF/NF faturada (~16% YTD 2026)
- **%Preta (cotação)** — base cotações encerradas (~11%)
São números diferentes por construção; todo rótulo no portal indica a base.

## Estoque — cobertura em meses (cobertura = (estoque − |reservado|) ÷ CMM)
| Situação | Regra |
|---|---|
| CRITICO | < 1 mês E abaixo do regulador |
| REPOSICAO | < 3 meses |
| EXCESSO | > 24 meses (liquidação) |
Lead times: nacional 45d · importado 180d · forjado 75d. View única: `vw_estoque` (gold).

## Triagem de Cotações Pendentes (PRIORIZAR / ESPERAR / NEGAR)
Cascata (view `vw_cotacoes_pendentes`): bloqueio YAML → NEGAR · Preta sem estoque → NEGAR · estoque parado >24m → PRIORIZAR · Preta com estoque e cobertura >12m → PRIORIZAR (queimar estoque) · cliente ABC-A aguardando >15d → PRIORIZAR · resto ESPERAR. ABC de clientes: A até 80% acumulado, B até 95%.

## Comissão de agentes (formação de preço) — 14/07/2026
- O % acertado com o **agente** (facilitador/indicação; ≠ representante com carteira) entra **DOBRADO** no preço; a metade extra é **margem oculta** (REP_Spread = ABCCUS_COM cobrado − ABCCUS_COM_COB pago).
- **Exceções que não dobram:** vendedores **Açotec São Carlos / Rio Preto** (negociação específica) e **exportações** (`Op_Categoria='Exportação'` — casos ELIN/MATEC).
- No **DRE**, deduz-se só a comissão PAGA (RAF, competência); a conta "COMISSÕES REPRESENTANTES" do razão é o MESMO dinheiro em caixa e fica FORA do DRE (natureza própria) — corrigida dupla contagem de ~R$ 213k em 14/07.
- **Monitor permanente** na aba Pricing do portal (conformidade do dobro; 100% em 14/07).

## Mês fechado (DRE e Despesas) — 14/07/2026
Um mês só entra quando **Faturamento (RAF) E despesas estão fechados** — despesas fecham no mês seguinte; o parcial do mês corrente é **ignorado** (não exibido), com aviso "fechamento contábil pendente". Implementação: piso de 50% da média dos meses cheios (`dre_meses_fechados`).

## DRE Gerencial — metodologia (auditada 13-14/07/2026)
- Custo REAL em tudo: aço/serviços via `ABCCUS_*_COB` (RAF, competência); comercial/logística/estrutura/corporativo via razão de Despesas (caixa).
- **Regime misto** (proxy gerencial, não DRE societário): receita por competência, despesa por caixa; comissão paga refere-se ao mês anterior (~R$ 68k de descasamento no acumulado).
- Bases dos %: "% Líq." sobre faturamento líquido; "% Bruto s/IPI" é *common-size* sobre venda — **não comparar com o benchmark 3,70%**, que usa o faturamento TOTAL de operações s/IPI (expander "Conferência de bases" no portal mostra as duas).
- Rateios: CD Jacareí → Logística; Corporativo → overhead; por **% do PGA** — EDITÁVEIS em `MotorAnalitico/config/rateio_cd.yaml` (vigência 14/07/2026: 69,8/10,0/8,6/8,4/3,2); compensações manuais permitidas, com trava: soma=100% ou o build do gold falha. Guarulhos = Matriz+VP+Anchieta.
- Leitura de tendência: mensal com **média móvel 3M** (mês isolado mistura sinal e ruído de caixa — Corporativo oscila 7-10,5%/mês).

## Spread DDV/LOG (Margem Agregada) — 14/07/2026
A regra temporária "spread=0" (27/04) morreu: o spread real vem do **razão de Despesas** (DDV = estrutura comercial sem comissão de agentes; LOG = logística com rateio CD), aplicado por **unidade×mês fechado**; mês aberto usa o cobrado como proxy. `OrcamentoAnual.xlsx` deixou de ser necessário.

## Frescor de dados (selo do portal)
🟢 ≤7 dias · 🟡 ≤15 · 🔴 acima. Cadências oficiais por base: RAF/Pedidos/CotEncerradas/Despesas mensais · CotPendentes semanal · Estoque+Movimentação 2-3 dias · ListaClientes bimestral · demais sob demanda. Semáforo por base: portal → 🔄 Central de Atualizações.

## ⭐ BASE ÚNICA DE FATURAMENTO (re-base 16/07/2026 — substitui a régua dupla)
**Faturamento (vendas) = TODAS as modalidades ex-Sucata/Devolução = base contábil, conciliada ao centavo (teste de ouro no CI).** Modalidades (Op_Categoria com nomes de negócio): Venda de produto · **Consumo do cliente** (venda p/ quem consome — MAHLE, Suzano...) · **Consignação** (ex-"Outros") · Exportação · **Beneficiamento (serviço)**. YTD 2026: R$ 117,66M. **Margem confiável**: beneficiamento fora das análises de margem/%Preta (MC Softcomp fictícia — custo do material do cliente; custo real do serviço está no razão de Produção); receita dentro. %Preta re-baseado 16,27% · MC 31,66% (denominador = líquido margem-confiável). **Metas PGA comparam contra a base única** (PGA aprovado sobre faturamento total). Valores pré-re-base p/ rastreabilidade: venda de produto 112,11M · %Preta 16,0%.

## Conciliação contábil do faturamento (validada 14/07/2026 — junho AO CENTAVO)
**Contabilidade (Receita Bruta − IPI − Devoluções) = RAF todas as operações s/IPI, EXCLUINDO Sucata e Devolução.** View: `vw_conciliacao_contabil` (ano×mês×unidade, com devoluções e sucata em colunas separadas p/ investigar deltas). Junho/26: R$ 17.840.975,34 = exato. Desde 14/07/2026 o headline do portal é o **Faturamento (todas as operações)** = base contábil (R$ 117,66M YTD), com o recorte **"Venda de produto"** (R$ 112,1M — base dos KPIs comerciais: %Preta, ticket, metas) ao lado e o split por tipo de operação em expander. Nota: a contabilidade abate devoluções em timing próprio — 1º suspeito em qualquer delta futuro. Validador mensal contábil↔portal: a construir quando os relatórios mensais da contabilidade chegarem.

## Aluguel dos imóveis — holding (15/07/2026)
Imóveis transferidos da Sacchelli para a **holding do Wagner em jan/26**; aluguel (~R$ 531k/mês, conta DUO 31206.1, com retroativo em mar/26) pago à holding. **ENTRA na análise de resultado da empresa** (linha própria no DRE, após o Resultado Operacional Gerencial: "Resultado após aluguel"); **FORA da base de metas PGA** — o PGA foi aprovado quando os imóveis ainda eram da Sacchelli.

## Comissões — timing (15/07/2026)
Vendedores **CLT/PJ**: comissão sobre o faturamento do mês. **Representantes**: comissão após a liquidação da duplicata. Por isso o DUO (competência/provisão) roda ~R$ 126k/mês acima do razão gerencial (caixa) na conta 32302.2 — divergência com causa conhecida, documentada no validador.

## Canais de venda — INT / PJ / REP / EST (17/07/2026 — decisão Gustavo)
Cadastro oficial: **Lista de Vendedores** (Softcomp). Coluna `Equipe` = "Unidade - TIPO":
- **INT** — funcionário CLT Sacchelli. Ganho: salário fixo (por faixa) + comissão sobre o faturamento líquido (sem impostos) individual + bonificação.
- **PJ** — vendedor com empresa aberta, trabalha SÓ para a Sacchelli (emite NF). Comissão **2% sobre faturamento s/ IPI**, paga no mês seguinte ao faturamento.
- **REP** — representante comercial. Comissão **2% s/ IPI**, paga **após a liquidação da duplicata** (por isso o timing difere no razão — ver "Comissões — timing").
- **EST** — contas estratégicas (Luiz Carlos Cruz - Fuscão, Priscila Toledo, Clientes em Desenvolvimento; "Estrategico - Piracicaba" está classificado INT no cadastro).
- **Exceção Açotec (São Carlos / Rio Preto)**: NÃO são vendedores — são **clientes atendidos diretamente pelos gerentes das unidades**, com comissão a terceiro por indicação/lobby; o custo **não dobra** (refina a exceção registrada em 14/07).
- Ponte de dados: RAF (`ABCVEN_NOM`) casa pelo **Nome**; Cotações casam pelo **Nome Fantasia**. Prefixo `***` no cadastro = registro inativo/histórico.

## Análises contábil × gerencial (15/07/2026)
O SAC360 mantém as DUAS visões: **gerencial** (DRE proxy, razão caixa, base das decisões comerciais) e **contábil** (página "Resultado Contábil (DUO)" — balancete por unidade/consolidado, com receitas financeiras, aluguel, depreciação). Regra de ouro: **o faturamento bate em todas as análises** — só existem duas bases nomeadas (todas as operações = contábil; venda de produto = comercial), conciliadas ao centavo e travadas por teste.

## Nomenclatura contábil (diretriz obrigatória, 14/07/2026)
Todo demonstrativo/gráfico/tabela usa terminologia contábil profissional + unidades explícitas. Modelo **híbrido**: termo contábil principal + termo AFS entre parênteses onde enraizado. DRE: lentes "Por unidade de negócio (filial)" / "Por gerência — margem de contribuição" / "Por gerência — após custo de servir"; cascata: "(−) Deduções da receita" · "= Lucro Bruto (MC Operacional)" · "= Margem de Contribuição" · "= **Resultado Operacional Gerencial**" (exclui depreciação, resultado financeiro e IR/CSLL — regime misto competência/caixa).

## Indicadores econômicos — Painel Executivo (15/07/2026, Fase A)
View `vw_indicadores_executivos` (gold, base DUO meses fechados): Receita líquida (grupo 411) · Margem bruta · **EBITDA** = LAIR + depreciação + resultado financeiro líquido (**JCP fora** — remuneração de sócio, coluna própria) · EBIT · **LAIR** (= resultado contábil; DUO não traz provisão IR/CSLL) · Cobertura de juros (EBIT ÷ desp. financeiras) · DSO **contratual** (prazo médio ponderado ABCCPGMED — não é o efetivo) · CAPEX realizado (razão grupo 13) · Aluguel holding · Forecast rolling 12m (sazonalidade 2023-25 × ritmo 3m — projeção estatística, não guidance). **Fase B** (capital de giro, ciclo de caixa, dívida líquida/EBITDA, ROIC×WACC) aguarda o **balancete patrimonial mensal** (grupos 1-2) da contabilidade. Fórmulas completas: glossário do portal.

## Despesas "Investimento" e área 10 (17/07/2026 — decisão Gustavo)
As áreas 21/22/26 do razão são **despesas reais** (valuation Swiss Steel, feiras, marketing) chamadas "investimento" pelo **trâmite de aprovação do Diretor Superintendente (Wagner)** — entram no resultado com **linha própria no DRE** ("Despesas c/ aprovação Diretoria", rateadas pelas % do PGA; jan–jun: −R$ 1,42M). **Capex real = grupo contábil 1** (flag `eh_capex`), fora do resultado. **Área 10 = RH corporativo** (VR, salários, FOPAG, Unimed — antes caía em "Outras"). **Cadastro TiposNF** (`01_Brutos/TiposNF/`) é a fonte oficial do significado das operações — CFOP 5102 confirma "Consumo Próprio" como venda a cliente; alerta operacional: tipo 47 "VENDA ESPECIAL" está marcado NÃO USAR no cadastro e faturou R$ 282k em 2026.

## WACC (16/07/2026 — decisão Gustavo)
Build-up simplificado (praxe p/ empresa fechada): **Ke = SELIC 14,25% + spread 5,0% = 19,25% a.a.**; Kd = juros observados no DUO ×(1−34%); pesos do balanço mais recente → **WACC ≈ 18,7%**. ROIC anualizado 30,4% ⇒ spread **+11,7pp**. ⚠ Para valuation externo é **PISO de range** (sem prêmio de tamanho/iliquidez). Componentes em `definicoes.py`; balanços patrimoniais MENSAIS em `01_Brutos/BalancoPatrimonial/`.

## Perfil e acabamento SEMPRE por extenso (27/07/2026 — regra FECHADA)
O Softcomp manda a MESMA dimensão em duas grafias conforme a rota: export manual → nome ('Redondo'); views `BI.*` do SQL → código de 1 letra ('R'). Mapa canônico único em `definicoes.py::PERFIL_LABEL/ACABAMENTO_LABEL` + `perfil_por_extenso()`/`acabamento_por_extenso()`, consumido por pedidos e cotações:
- **Perfil**: R=Redondo · A=Anel (NÃO 'Achatado') · T=Tubo · C=Chato (NÃO 'Chapa') · Q=Quadrado · S=Sextavado · D=Disco de Aço · L=Cantoneira (NÃO 'Lâmina') · P=Chapa
- **Acabamento**: L=Laminado · F=Forjado · T=Trefilado · U=Usinado · D=Descascado · R=Retificado
- Colunas do enriquecido: `perfil_legivel`/`acabamento_legivel`; as cruas `perfil`/`acabamento` guardam o que o Softcomp mandou — **nunca filtrar por elas**. Contrato no `make ci` reprova código de 1 letra nas 4 views.
- ⚠ Pendente: em cotações o perfil ainda vem do cadastro de família (só Redondo) — ~8,9k linhas de Anel/Tubo/Chato aparecem 'Redondo'.

## Pricing — thresholds
Stoplight %Preta por vendedor: atenção >12% · crítico >25% (R$ mínimo 50k). Piso Operacional de MC: 24%.
