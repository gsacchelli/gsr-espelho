---
data: 2026-06-21
tipo: avaliação
projeto: Data Lake + IA dedicada (Aços Sacchelli)
fornecedor: DataSide
documento avaliado: DocumentacaoFinal_Assessment_AcosSacchelli.pdf (EFT v1.1, 12/06/2026)
veredito: aprovar como diagnóstico · recusar como base de contratação
---

# Avaliação do Assessment DataSide — Data Lake + IA dedicada

Avaliação multi-agente da **Especificação Funcional e Técnica (EFT) / Assessment** entregue pela DataSide para a Aços Sacchelli (41 páginas, v1.1 de 12/06/2026), mais a transcrição da reunião de apresentação (números de custo e modelos de contratação só aparecem na fala, não no PDF). Painel de 3 especialistas — **Comercial/Estratégia, Arquitetura Técnica de Dados, Operações/Implementação** — lendo o documento integral. Objetivo: assessment preliminar para **futura contratação da infra + projeto de IA**, podendo ser a DataSide **ou concorrente**. O documento foi avaliado por mérito próprio.

## Veredito consolidado

**Bom diagnóstico, mapa reaproveitável — mas não é base de decisão de contratação, e a parte de arquitetura/custo não deve ser comprada como está.** O assessment é um retrato AS-IS honesto, granular e portável: mapeia 5 áreas, o ERP Softcomp, planilhas críticas e ~20 casos de uso candidatos, sem fingir que partimos do zero. Esse é seu valor real. Os três especialistas convergem, porém, em três problemas que pesam mais que as qualidades: (1) o número de custo apresentado verbalmente (**R$ 566–666/mês**) é **irreal por uma ordem de grandeza** e cobre só infra — o custo que decide a contratação (squad/implementação) ficou omitido; (2) a arquitetura proposta (Databricks/EMR + duas clouds, Genie/Bedrock/SageMaker) é **superdimensionada** para nossa volumetria; (3) toda a solução repousa sobre um acesso ao banco do Softcomp que **nunca foi testado** ("não houve contato com os dados do banco"). Aprovar como insumo de diagnóstico. Recusar como contrato. Forçar a conversa para números reais e prova de acesso antes de comprar qualquer plataforma.

## Scorecard por dimensão

| Dimensão | Veredito |
|---|---|
| Comercial / Estratégia | Aprovar com ressalvas como diagnóstico — **não** como base de RFP ainda (faltam preço, prazo, esforço) |
| Arquitetura Técnica | Diagnóstico sólido, **arquitetura superdimensionada e imatura** (custo irreal, acesso não comprovado) |
| Operações / Implementação | Viável, mas com **pré-requisitos pesados**; "quick wins quase imediatos" é otimista demais |

## O que o documento faz bem (forças)

- **Ativo portável e reaproveitável.** O diagnóstico não amarra a DataSide. Serve de base para uma concorrência (RFP) com outros fornecedores — já pagamos pelo trabalho de descoberta em tempo de entrevistas.
- **Honestidade no diagnóstico.** Afirma explicitamente que a Sacchelli **não parte do zero** — temos dados ricos e granulares no Softcomp e controles sofisticados (Carteira Semanal, Programação de Corte com ~67k fórmulas na aba Baixas). Um vendedor predatório teria pintado terra arrasada.
- **Pega o eixo de modelagem certo do domínio aço.** Identifica o **lote como identidade do material**, ligando NF-entrada → OC → composição química → certificado da usina → estoque → qualidade. Raro acertar isso na primeira passada.
- **Isola corretamente o gargalo-mãe.** Aponta o acesso ao Softcomp (via SQL Server) como pré-requisito **absoluto** e risco **crítico**. Está certo: sem isso, tudo volta a ser exportação manual de Excel.
- **Rastreabilidade dos achados.** Cada caso de uso e requisito candidato cita a fonte (reunião X, discovery Softcomp, arquivo Y) com nome e data. Auditável.
- **Riscos materializados documentados sem maquiagem.** 3 pagamentos perdidos em pasta física; histórico de RH perdido por estar só na máquina do Marcos (perda já ocorreu em 2026); conciliação automática desativada desde a abertura das filiais.

## Red flags e lacunas transversais (onde os 3 convergem)

1. **Ancoragem de preço enganosa — a red flag mais grave.** R$ 566–666/mês é só infra, sem dizer no mesmo fôlego que a implementação (squad) custa muito mais. Pior: o próprio número de infra não sobrevive a um teste de realidade. Referência de mercado para uma stack Databricks/EMR rodando ETL diário: **US$ 1.500–4.000/mês (~R$ 8k–22k/mês)** all-in. Squad de dados dedicado no Brasil: **R$ 50k–120k/mês** → projeto de 6–12 meses = **R$ 300k a R$ 1,4 MM**. A decisão está sendo ancorada num número irrelevante.
2. **Over-engineering para o porte.** Databricks/EMR são plataformas Spark para escala de TB–PB de dado analítico. Nossa fonte é um único SQL Server de ERP de distribuidora (provavelmente dezenas de GB de dado de negócio) + 1,2 TB de File Server que são **1,15 milhão de documentos** (PDF/XML/planilha), não tabelas a processar. Não há volume, velocidade nem variedade que justifique Spark. Alternativas mais enxutas e baratas de operar: **Microsoft Fabric** (integra nativo com o Power BI que já temos), **BigQuery/Snowflake** (serverless, sem cluster para administrar), ou até **Postgres + dbt + Power BI**.
3. **Acesso ao Softcomp via leitura direta do banco — sem prova e sem contrato de dados.** A API REST foi descartada pelo fornecedor ("cara e delicada"). Ler o schema interno do Softcomp significa: acoplamento a um schema não documentado de terceiro (um update do Softcomp quebra os pipelines em silêncio), ausência de SLA/versionamento, e ficar fora de suporte. CDC via DMS sobre banco de produção de ERP de terceiro adiciona risco de carga no transacional e de estouro de transaction log — e exige aval de quem administra o banco (Softcomp), que não foi consultado sobre isso.
4. **Conflito de interesse declarado contamina a "neutralidade".** A DataSide se diz agnóstica entre AWS e Azure, mas admite receber incentivo financeiro dos parceiros cloud por trazer cliente novo ("calculadora de incentivo"), e é parceira Databricks/Microsoft. As duas arquiteturas convenientemente convergem para os dois ecossistemas onde ela tem incentivo. Um agnóstico de verdade teria posto na mesa também a opção frugal (ficar no SQL Server + Power BI que já temos).
5. **Camada de IA vendida cedo demais.** O próprio diagnóstico classifica prontidão para IA como **"Inicial"**, governança e integração como **"Baixa"**. Prometer "vendedor virtual" (Bedrock/Genie) e "previsão de fechamento de cotação / fluxo de caixa" (SageMaker) sobre dados ainda fragmentados é vender o telhado antes da fundação. Genie/text-to-SQL só funciona sobre uma camada gold semântica que ainda não existe; modelo de probabilidade de fechamento precisa de histórico rotulado limpo — exatamente o que hoje é inconsistente (vendedores encerram cotação antes de confirmar o pedido, registrado no próprio doc).
6. **"Quick wins quase imediatos" contradizem o próprio documento.** Quase todos (painel de vendas near-real-time, contas a receber, pedidos) dependem do acesso ao Softcomp que **ainda não existe**. O quick win mais rápido seria reproduzir o que o Gustavo já faz à mão no SAC360. "Tempo real" colide com a janela SKA→Softcomp de 15–30 min.
7. **Sustentação (run) e handover não endereçados.** Quem opera o data lake e os pipelines depois da entrega? Não temos time de dados interno. Ou viramos refém de squad externo (custo recorrente indefinido), ou precisamos de plano de capacitação — que não existe no documento.
8. **Lacunas técnicas de um assessment que vai justificar Databricks:** sem volumetria por fonte/tabela, sem dicionário de dados, sem modelo dimensional alvo (grão dos fatos, Dim_Cliente conformada entre matriz e 6 filiais), sem estratégia de migração das regras das planilhas (as 67k fórmulas), sem SLAs de frescor por domínio. Coerente com o escopo declarado da EFT, mas é exatamente o que falta para comparar propostas por TCO.
9. **LGPD superficial.** Dados de RH (folha, ponto, atestados) são sensíveis. Faltam base legal, DPA com o fornecedor, política de retenção e a decisão de ler **réplica** em vez de produção.
10. **~20 casos de uso sem priorização valor×esforço** = scope creep embutido (change request a cada item no escopo fechado; horas infinitas no squad).

## Recomendação (consenso dos 3 especialistas)

**Nem squad aberto, nem big-bang de escopo fechado. Comprar primeiro um piloto pago, curto e de escopo fechado — começando pela prova de acesso.**

- **Gate 0 — Prova de acesso ao Softcomp (1–3 semanas, baixo custo, pré-condição contratual):** extrair automaticamente os mesmos relatórios que o Gustavo puxa à mão (RAF, pedidos, cotações encerradas/pendentes), idealmente sobre **réplica de leitura**, e reproduzir **um** indicador que já existe no SAC360. Critério binário: **o pipeline automatizado bate número com o controle manual.** Passou → o projeto é real. Não passou (acesso negado/insuficiente/latência inviável) → descobrimos isso gastando semanas, não meses nem seis dígitos.
- **Piloto Fase 1 — Comercial (4–6 semanas após Gate 0):** painel de Carteira Semanal automatizado (D-1 ou intradiário, **sem** prometer tempo real), stack **mínimo**, não a plataforma completa. Área mais madura (já temos o SAC360), dono claro e engajado, benchmark existente, risco regulatório baixo. Sucesso medido por **paridade de número (<1%), horas economizadas e adoção real** (o time abandona a planilha antiga em 30 dias?).
- **Em paralelo:** levar este assessment a **1–2 concorrentes** (idealmente um que não seja parceiro Databricks/Microsoft) para cotar o mesmo MVP, e **exigir da DataSide o cenário "frugal"** aproveitando SQL Server + Power BI já existentes, para precificar o custo real da decisão hyperscaler.
- **Capturar quick wins independentes da stack desde já:** webhook RD Station, API Serasa para crédito, repositório centralizado do histórico de RH (risco já materializado), digitalização do fluxo de pagamentos sem OC.
- **Pôr na mesa como leverage** a capacidade interna já existente (motor analítico, painéis, IA própria — João automatizou DIFAL/DRE/conciliação; Gabriel usa IA para fluxo de caixa). Não somos compradores desesperados; já fazemos boa parte disso sozinhos. Isso reduz escopo e preço.

## Próximos passos

1. **Não assinar a arquitetura.** Enviar a lista de perguntas à DataSide (doc anexo) e exigir as respostas por escrito antes de qualquer decisão de plataforma.
2. Pedir TCO 36 meses, preço e prazo do MVP, e o detalhamento honesto do custo de infra (DBUs + VMs + storage + egress + dev/prod + inferência de IA).
3. Exigir transparência do incentivo de parceria cloud/Databricks por escrito.
4. Disparar Gate 0 (prova de acesso ao Softcomp) — depende de Francisco + Nelson (Softcomp); é o caminho crítico de tudo.
5. Levar o assessment a concorrentes e pedir o cenário frugal.

## Anexo

Lista de perguntas/questionamentos à DataSide (24 perguntas, agrupadas por Acesso & Dados, Arquitetura & Custo, IA, Comercial & Contratação, Operação & Governança): `Logs/2026-06-21 — Perguntas à DataSide (assessment).md`.

---

*Avaliação conduzida por painel de 3 agentes especialistas (Comercial, Arquitetura, Operações) + síntese. Documento-fonte e transcrição da reunião arquivados nos uploads da sessão.*
