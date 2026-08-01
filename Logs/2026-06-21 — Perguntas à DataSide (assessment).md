---
data: 2026-06-21
tipo: questionário / due diligence
projeto: Data Lake + IA dedicada (Aços Sacchelli)
destinatário: DataSide
relacionado: Logs/2026-06-21 — Avaliação Assessment DataSide (Data Lake + IA Sacchelli).md
---

# Perguntas e questionamentos à DataSide

Lista consolidada (24 perguntas) a partir do parecer dos 3 especialistas que avaliaram o assessment. Ordenada por bloco; os itens marcados **[GATE]** são bloqueadores — sem resposta satisfatória, não há decisão de contratação. Pronta para enviar.

## A. Acesso aos dados e prova de viabilidade  *(o caminho crítico de tudo)*

1. **[GATE]** Já existe **prova de acesso** ao SQL Server do Softcomp? Vocês já extraíram um único registro real do banco? Se não, qual é o caminho e o prazo até essa prova — e ela é pré-condição contratual antes de qualquer fase paga?
2. **[GATE]** O acesso será sobre **réplica de leitura** ou **produção direta**? Qual a garantia de que a leitura não degrada a performance do ERP em operação?
3. **[GATE]** Qual é o **contrato de dados** com o Softcomp para a leitura direta do banco? Há compromisso formal do fornecedor de estabilidade de schema, versionamento e suporte? O que acontece com os pipelines quando o Softcomp aplicar um update que renomeie tabelas/colunas internas?
4. Para CDC via DMS: o banco do Softcomp aceita habilitar CDC / full transaction logging? Quem administra esse banco — Sacchelli ou Softcomp? Como vocês mitigam crescimento/estouro do transaction log e a carga adicional no transacional?
5. O que acontece com cronograma e valores se a prova de acesso **falhar ou atrasar**? Qual o plano B e quem assume esse risco?

## B. Arquitetura e custo  *(adequação ao porte e realismo do número)*

6. Qual a **volumetria real** do dado transacional do Softcomp por domínio (nº de linhas e GB em vendas, estoque, movimentação, financeiro) e a taxa de crescimento mensal? Sem isso, como se justifica tecnicamente Databricks/EMR (Spark) em vez de um data warehouse SQL convencional?
7. O custo de infra citado (~R$ 566/mês Azure, ~R$ 666/mês AWS) inclui o quê exatamente? Detalhem: DBUs por tipo de cluster e horas/dia ligado, VMs/compute, storage, egress, ambientes dev **e** prod, Unity Catalog, observabilidade, e custo de inferência de Bedrock/Genie e training/endpoint de SageMaker. Esse número sobrevive a um cluster rodando algumas horas/dia?
8. Apresentem o **TCO a 36 meses** (infra + run + sustentação), não só o componente de infra mensal.
9. Por que **duas clouds em paralelo** sem recomendação nem critério objetivo de escolha (custo, skill interno, lock-in)? E por que EMR (Spark) aparece como ferramenta de **ingestão de APIs** em vez de um orquestrador/serverless adequado?
10. Avaliaram alternativas mais enxutas (**Microsoft Fabric, BigQuery, Snowflake, ou Postgres + dbt + Power BI** direto, aproveitando o SQL Server e o Power BI que já temos)? Apresentem um **cenário "frugal" comparável** e digam a partir de qual volumetria/complexidade o Databricks passa a se justificar — e se a Sacchelli a atinge.
11. Qual o **modelo dimensional alvo** para o domínio aço? Qual o grão dos fatos (venda, movimentação de estoque por lote) e como a `Dim_Cliente` será conformada entre matriz e as 6 filiais hoje fragmentadas no CRM?
12. Qual a estratégia de **migração das regras de negócio** embutidas nas planilhas (ex.: 67.782 fórmulas na aba Baixas da Programação de Corte)? Quem valida que a lógica reimplementada bate com o Excel, e com qual estratégia de testes/reconciliação?
13. Quais SLAs de **frescor por domínio** vocês recomendam (financeiro D-1 vs. produção near-real-time), e como isso muda arquitetura e custo entre batch e streaming? Para os painéis "near-real-time", qual a latência real garantida, dado que SKA→Softcomp já tem 15–30 min de defasagem?

## C. Inteligência Artificial  *(risco de overselling)*

14. Genie/Bedrock "vendedor virtual": sobre qual camada semântica isso responderá? Existe modelo gold definido? Qual a taxa de acerto esperada de text-to-SQL sobre o domínio aço (liga/perfil/bitola) e como vocês evitam respostas confiantes e erradas em reunião de decisão?
15. Para o modelo de "probabilidade de fechamento de cotação": qual o dataset de treino, o grão e a definição de label, considerando que o próprio doc registra que vendedores encerram cotações antes de confirmar o pedido (métrica de conversão inconsistente)?
16. Os itens de IA preditiva dependem de base histórica integrada que o próprio diagnóstico classifica como **"Inicial"**. Em que fase realista vocês colocam esses itens e qual o volume/qualidade de histórico necessário?

## D. Comercial e contratação

17. Qual a faixa de **investimento (R$) e prazo (meses)** para o **MVP** (os 3–5 casos de uso de maior valor) e para o escopo completo?
18. Apresentem, lado a lado, (a) custo mensal do **squad dedicado** com composição e senioridade exatas e (b) preço **fechado por release** com a lista de change requests previsíveis — para o mesmo MVP.
19. Qual exatamente é o **incentivo financeiro** que a DataSide recebe de AWS, Microsoft e Databricks por esta conta, e como ele varia entre as duas arquiteturas? Pedimos transparência por escrito do conflito de interesse.
20. **Propriedade e saída:** ao final do contrato, de quem é o código, os pipelines, os modelos e a documentação? Qual o plano de transferência de conhecimento para nossa equipe operar sem vocês, e em quanto tempo?
21. Dos ~20 casos de uso, quais **5 entregam maior retorno com menor esforço**, com estimativa de payback de cada? Queremos um roadmap MoSCoW, não uma lista plana.
22. Indiquem **2–3 referências** de porte/segmento comparáveis (distribuição/indústria de médio porte, sem time de dados maduro) onde implementaram esta mesma stack, com resultado e custo real realizado.

## E. Operação, governança e adoção

23. Quem **opera e sustenta** a plataforma (data lake, pipelines, Databricks/EMR) depois da entrega? Qual o modelo e o custo mensal de run + sustentação, e existe plano de **capacitação/handover** para a equipe interna? A Sacchelli já tem fluência interna em IA/analytics (SAC360, automações de DIFAL/DRE/conciliação feitas pela própria família) — a solução de vocês **substitui, integra ou coexiste** com isso, e como evitam retrabalho e baixa adoção?
24. Como fica a **governança LGPD** dos dados de RH (folha, ponto, atestados — sensíveis): DPA, base legal, política de retenção, controlador vs. operador? E como vocês definem **fonte oficial** quando Softcomp e os controles em Excel divergem (ex.: Carteira Semanal) — quem arbitra a regra de negócio em produção?

---

*24 perguntas consolidadas de um painel de avaliação de 3 especialistas (Comercial, Arquitetura Técnica, Operações). Bloqueadores [GATE] em A1–A3 e A5.*
