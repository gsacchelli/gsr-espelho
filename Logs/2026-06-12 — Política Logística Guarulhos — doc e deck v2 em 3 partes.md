---
data: 2026-06-12
tipo: log
status: vigente
obs: "entregue — v2 pronta para o conselho"
domínio: logística / custeio / política comercial
criado: 2026-06-12
tags: [logística, frete, guarulhos, conselho, cowork]
---

# Política Logística Guarulhos — doc e deck v2 (estrutura em 3 partes)

Sessão de retomada (Cowork). A pedido do Gustavo, documento e apresentação do conselho foram **reestruturados em 3 blocos**: Parte I Diagnóstico (metodologia de apuração + custos + indicadores) · Parte II As três opções (A/B/C desenvolvidas individualmente) · Parte III Recomendação (sequenciamento A→C com piloto B + roteiro + decisão).

## Entregáveis (em `~/dev/afs-lake/04_Logistica/`)
- `Politica_Logistica_Guarulhos_Conselho_v2.docx/.pdf` — 10 pgs (builder: `build_doc_conselho_v2.py`)
- `Logistica_Sacchelli_Conselho_v2.pptx/.pdf` — 13 slides (builder: `build_ppt_conselho_v2.py`)
- Versões v1 preservadas na mesma pasta.

## Auditoria de números (fact sheet por agente, 12/06)
Workbooks recalculados (openpyxl não cacheia fórmulas). Correções aplicadas na v2:
- Tabela de custo §2 agora usa o **realizado** (comb. 97,1 · manut. 55,8 · pessoal 47,5 · CD 19,1 · terceiros 13,7 · IPVA 11,3 · pedágio 10,7 · seguros 1,6 · multas 0,9 = 257,7 mil/mês). A v1 aplicava % sobre o total e omitia Fretes Terceiros.
- Padronizado: fixa **apurada 0,53% / adotada 0,55%** em todo o texto (v1 misturava).
- Toco: economia **~R$ 135 mil/ano com 2 tocos** (v1 dizia "por veículo" — errado).
- Make-vs-buy padronizado: **3.554 vs 2.501/viagem** (base _params Jan–Mar, ex-pedágio).
- Ocupação com base declarada (Jan–Mar romaneios completos): 29% urbano / 54% interior; 72% viagens ≤7 t no total (83% só GSP — sempre qualificado).
- R$/kg completo por região na tabela CEP: 0,23 GSP · 0,25 RMSP-Oeste · 0,35 Campinas/Jundiaí · 0,38 Vale/Bragança · 0,40 Piracicaba-Limeira/Sorocaba · 0,50 exceção.
- Removida coluna Viag/mês da tabela de regiões (somava ~190 vs operação ~133/mês — base não auditável; revalidar na calibração).
- 13 regiões atuais (10 só na capital/RMSP) — esclarecido.

## Refinos pós-revisão do Gustavo (12/06, tarde)
- **R$ 57 mil/mês da Opção A é TETO contado por NF**: os 45%/47% "abaixo do mínimo" da aba Politica_Frete contam NF a NF, sem agrupar notas do mesmo cliente no mesmo romaneio (~5 NFs/viagem na média). Unidade correta de cobrança = **entrega (CNPJ × dia)**: notas agrupadas somam valor/peso e, abaixo do mínimo, pagam 1 taxa. Doc e deck reescritos com o qualificador; recalcular por entrega quando os romaneios brutos chegarem. Regra explicitada também na Opção C (§8.3).
- **Curva ABC é sobre o valor ENTREGUE (R$ 43,2 mi, 472 clientes), não o faturamento total**: build_doc.py ordena por "faturamento entregue". Cabeçalho corrigido para "% do valor entregue" + nota de base declarada (quem só retira não aparece; tiers definitivos virão da margem de bolso do RAF total).
- **Novo §4.2.1 Raio-X por região** no doc (dados da aba Por_Regiao, Jan–Mar): viagens, NFs/viagem (proxy de clientes/rota), peso, ocupação, custo/viagem, custo/entrega, R$/kg por região. Destaques: capital/ABCD a R$ 0,95–0,97/kg por ociosidade (4× a tarifa-alvo); Bragança cheio a 0,38; Vale = 1 NF dedicada a R$ 3.012. Doc agora tem 11 pgs.

- **% logística vigentes corrigidos (reajuste fev/2026, informado pelo Gustavo)**: Guarulhos 1,85 · **Piracicaba 1,85** (não 2,24) · São Carlos 3,70 · Rio Preto 3,10 · Caxias 5,65. Folgas recalculadas: Piracicaba cai de +0,55 para **+0,16 pp** — também no fio da navalha. Os % "medidos no RAF" do workbook eram efetivos da janela (reajuste no meio do período + mix), não os nominais. Tabela §3 do doc atualizada com nota de fonte. ATENÇÃO: o CLAUDE.md do afs-lake também lista os % antigos (2,2/3,0/3,6/5,5) — atualizar quando mexer nele.

## Pendências abertas (sem mudança)
1. Calibrar R$/kg por eixo com custo variável real (hoje tarifa-alvo @80% ocupação).
2. Curva da baleia com margem de bolso (pós-frete) do RAF → tiers A/B/C.
3. Cenário híbrido quantificado + custo de servir por cliente.
4. De-para CEP→região no ERP + simulador no fluxo de orçamento.
5. ~~**IPVA contraditório**~~ — **RESOLVIDO 12/06** com o razão da conta 71.12.14.116 (Gustavo trouxe o detalhe): caminhões **pagam** IPVA em SP a **1,5% do venal** — a premissa "isento" do `cpk_frota_sacchelli.xlsx` é que estava errada. Composição do R$ 56,7 mil: IPVA R$ 53,2 mil/ano (4 caminhões ~R$ 450k venal · 4 ~R$ 187k · 1 ~R$ 155k · 1 Volvo ~R$ 833k) + licenciamento 12× R$ 174,08 + R$ 1,4 mil de despachante/2ª via/vistoria. Isentos só a carreta e o CXU1751 (+20 anos). Desembolso anual concentrado em jan: média da janela 5m = 11,3 mil/mês vs anualizado ~4,7 mil/mês (recalibração trimestral anualiza). **Ajuste pendente no CPK**: incluir IPVA real (~R$ 250–1.050/mês por veículo conforme venal) no fixo mensal — direção favorece o toco (venal menor → IPVA menor).
6. Brutos mensais (logistica janeiro–maio.xlsx) não foram migrados para `04_Logistica/` — necessários para a recalibração (item 1).

## Conexões
- [[Sistema Operacional Comercial/04 RAF/11 - Metodologia de Custeio da Logística]]
- [[Custo de Servir]]
