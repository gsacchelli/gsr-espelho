---
data: 2026-06-21
versao: v2 (revisado pelo Time de Inovação em 2026-06-21)
tipo: projeto
codinome: Forja
framework: Inovação H1·H2·H3 (FDC / Três Horizontes)
escopo: Aços Sacchelli — plataforma de dados, inteligência e IA
fora_de_escopo: MetalM, Duferco (iniciativa tratada isoladamente)
relacionado: "[[Inovação H1, H2 e H3]] · Logs/2026-06-21 — Avaliação Assessment DataSide (Data Lake + IA Sacchelli).md · Logs/2026-06-21 — Revisão Projeto Forja (Time de Inovação).md"
---

# Projeto Forja — Plataforma de Dados e IA da Aços Sacchelli

> **v2 — Ajustes pós-revisão do Time de Inovação (2026-06-21).** Um painel de 5 papéis (Head, Ecossistema, Benchmark, PM-UX, Execução) revisou este projeto com base em conceitos, casos e tendências. Decisões incorporadas, resumidas no bloco abaixo e detalhadas em `Logs/2026-06-21 — Revisão Projeto Forja (Time de Inovação).md`:
> 1. **Bus-factor é o risco nº 1** (todo o ativo numa pessoa/laptop) → criar **Gate 0-B de sucessão técnica** paralelo ao Gate 0; sem isso, não escalar.
> 2. **Horizonte por prontidão de dado, não por calendário** (crítica de Steve Blank) → os prazos abaixo são referência de maturidade, não cronograma; experimento-semente de H3 pode começar já.
> 3. **70/20/10 vira orçamento de duas camadas**: *run-rate* para sustentar/industrializar o core (não é "inovação") + *fundo de inovação* liberado por discovery-driven planning contra hipóteses testadas, com kill-criteria.
> 4. **Innovation sourcing (make/buy/partner) antes de todo build** + ecossistema (Softcomp como parceiro com plano B, créditos de cloud, startups metaltech, INDA, cliente-âncora) + funil contínuo de ideias.
> 5. **Adoção vira gate** (não bullet): paridade <1% *E* abandono medido da planilha antiga. Cooptar a **família como super-user/co-autora**; coexistência/parallel-run; trust como UX frontstage; **agente NLQ como interface primária do H1**.
> 6. **Preencher números**: teto de R$ do Gate 0, proxy de ROI em R$ (horas + p.p. de margem/%Preta com meta), stack ancorada na volumetria real (**Postgres+dbt+CDC** como default; lakehouse só se justificar). NLQ permanece em **funções canônicas** (text-to-SQL livre entrega ~11% em schema real).
> 7. **Sistema de entrega**: dual-track, sprint de 2 semanas, **WIP limit (2 experimentos + 1 entrega)**, retrô blameless; cada iniciativa de H2/H3 reescrita como Riskiest Assumption Test; **Gate 0 rodado como sprint cronometrado de 2 semanas**.

> **Forja**: o nome vem do chão de fábrica — é onde a matéria bruta vira valor sob calor e pressão. Aqui, o dado bruto e estático do Softcomp vira inteligência, previsibilidade e, no limite, um novo modelo de operar. (Codinome de trabalho — renomeável.)

Projeto estruturado nos **Três Horizontes de Inovação** ([[Inovação H1, H2 e H3]]) vistos no curso da FDC. Trata exclusivamente da jornada de dados/IA da Aços Sacchelli; não envolve MetalM nem Duferco.

## Problema central

O Softcomp concentra o dado de negócio, mas é **estático**: para virar informação gerencial, depende de extração manual, Excel e interpretação de pessoas-chave. Isso torna a decisão lenta, pouco escalável e sujeita a divergência de versão. A Sacchelli **não parte do zero** — já há dado rico e granular no ERP e uma camada analítica artesanal funcionando (afs-lake / MotorAnalitico / Portal SAC360 / painéis / agente analítico). O projeto Forja transforma esse ativo artesanal numa **plataforma**, e usa os três horizontes para equilibrar o retorno de curto prazo com a construção de futuro.

## Princípio de leitura (importante)

1. **Os três horizontes correm em paralelo, com pesos diferentes** — não em fila. Como cobra a sua própria nota da FDC, uma empresa saudável investe nos três ao mesmo tempo. A alocação-alvo de esforço/investimento: **~70% H1 · ~20% H2 · ~10% H3**.
2. **Mas há uma dependência técnica de mão única:** a *confiabilidade* de H2 e H3 depende da fundação de dado de H1. Dashboard tolera dado 90% limpo; agente que **age** (cota, decide, responde cliente) exige ~99%. Por isso H1 é a fundação que **destrava o direito** de H2 e H3 existirem com segurança — não porque venham depois no calendário, mas porque sem dado governado o resto é aposta.
3. **Cada horizonte precisa cruzar um gate de valor** antes de liberar peso para o próximo. Sem prova de valor em H1, não se escala H2.

---

## H1 — Inovação no Core · "Tirar o Softcomp do estático"

**Objetivo (sua nota):** otimizar o negócio atual — eficiência, produtividade, margem. Baixo risco, retorno previsível, incremental.

**A tradução para a Sacchelli:** industrializar a camada analítica que já existe e estendê-la a todas as áreas, eliminando a extração manual. Sair de "report mensal feito à mão" para "inteligência viva e governada".

**Iniciativas:**
- **Fundação:** automatizar a ingestão do Softcomp (acesso SQL Server / réplica de leitura) — o **Gate 0** de todo o projeto. Sem isso, tudo continua dependendo de Excel.
- Tirar o afs-lake/SAC360 do laptop → ambiente governado, com selo de frescor, linhagem e fonte oficial por domínio.
- Estender reports e previsibilidade do Comercial (já maduro) para Financeiro, Produção, Estoque, Qualidade e RH.
- Governança de dados de verdade: dono de dado por domínio, regras de qualidade, catálogo.

**O que REUSAR (não reconstruir):** motor analítico, cubos OLAP, painéis (RAF, Cotações, Pedidos, Estoque, Executivo), agente analítico NLQ, convenções de negócio AFS já codificadas (%Preta, faixas, metas, DRE gerencial). Isto é capital já investido — qualquer fornecedor entra para *industrializar*, não para refazer.

**Prontidão de dado exigida:** média — tolera imperfeição; o valor está em centralizar e automatizar.

**Riscos:** gargalo de acesso ao Softcomp não destravado; over-engineering (comprar plataforma pesada para um problema de porte médio); virar refém de squad externo para operar.

**KPIs (alinhados à sua nota: EBITDA, margem, produtividade):** horas manuais/mês eliminadas · tempo de decisão (de mensal → semanal/diário) · margem recuperada via disciplina de pricing (%Preta) · MAPE do forecast < 15% (30d) · adoção real (o time abandona a planilha antiga?).

**Gate de avanço → H2:** pipeline automático batendo número com o controle manual (paridade < 1%) + ao menos 1 área além do Comercial no ar.

**Horizonte:** 0–12 meses · **Peso: ~70%.**

---

## H2 — Inovação de Expansão · "Automatizar processo e ampliar capacidade"

**Objetivo (sua nota):** criar novas capacidades / expandir o core. Risco moderado, crescimento, exige capacidades novas.

**A tradução para a Sacchelli:** atacar as tarefas repetitivas e a gestão — transformar a plataforma de "ver o passado" em "operar o presente com menos esforço e menos erro". Capacidades que a empresa **não tem hoje**.

**Iniciativas:**
- Automação de processos hoje 100% manuais: conciliação bancária (razão × extrato Itaú), análise de crédito (Softcomp + Serasa via API), controle de importação, pipeline de indicadores de RH (Madis + Sólides), follow-up de fornecedores, ingestão de leads (RD Station via webhook).
- **Copilotos de gestão:** previsão de fluxo de caixa, previsão de fechamento de cotação, alertas com dono e cifra (a "fila de trabalho", não o "mural").
- Digitalização de pontos de risco já materializados: pagamentos sem OC (3 já perdidos), histórico de RH sem backup.

**Nuance honesta:** parte disto, no modelo canônico, é eficiência de core (H1). Classifico como H2 porque são **capacidades operacionais novas que escalam** e exigem qualidade de dado superior — meio-caminho entre core e transformação.

**Prontidão de dado exigida:** alta — toca Financeiro/Fiscal; erro vira dinheiro e autuação. Depende do H1 governado.

**Riscos:** regra de negócio presa em planilha (ex.: 67k fórmulas do corte) sem plano de decodificação; credenciais de terceiros (Serasa, SISPAG, Madis, Catho) fora do controle; LGPD em dados de RH/cliente.

**KPIs (sua nota: receita de novos produtos/capacidades, crescimento):** nº de processos automatizados · FTE-hora liberado e **realocado** para tarefa de maior valor · redução de erro/retrabalho · ciclo de fechamento financeiro · MAPE do fluxo de caixa.

**Gate de avanço → H3:** 3+ processos críticos automatizados em produção com confiança + base histórica integrada e limpa o suficiente para treinar/avaliar modelos.

**Horizonte:** 12–24 meses · **Peso: ~20%.**

---

## H3 — Inovação Transformadora · "Operação AI-native"

**Objetivo (sua nota):** criar o futuro — alto risco/incerto, potencial de disrupção, pode canibalizar o modelo atual. Mede-se por **aprendizado validado e experimentos**, não por entrega certa.

**A tradução para a Sacchelli — e aqui eu contesto o enquadramento inicial:** a sua ideia foi "treinar agentes em várias áreas para reduzir custo com pessoas, inclusive vendedor de atendimento passivo". Isso é real, mas **não trate redução de headcount como o objetivo de design** — três razões:

1. Atendimento passivo em aço **não é só tirar pedido**: tem julgamento (estoque, substituição de material, preço dentro da faixa, spec técnica). Meia-automação gera o pior dos mundos.
2. A decisão de cortar/realocar o vendedor puramente passivo é de **design organizacional e comissionamento — você pode tomar hoje, sem IA** (o painel já identifica quem é). A IA acelera, não cria a decisão.
3. O enquadramento que gera valor e sobrevive à execução é **aumento de capacidade**: o agente absorve a camada transacional passiva e libera o humano para relacionamento e contas de maior valor. Se sobrar redução de custo, que seja **consequência, não a tese**.

**O H3 como portfólio de opções (não roadmap fechado):**
- **Modelo comercial AI-native:** agente de atendimento/cotação para o fluxo passivo + vendedores requalificados para relacionamento. Experimento controlado, com humano no loop.
- **Agentes funcionais por área** (financeiro, compras, PCP) treinados sobre o dado governado de H1/H2.
- **Opção mais ousada — inteligência como diferencial:** a capacidade analítica vira ativo competitivo (nível de serviço informacional ao cliente, previsibilidade de entrega, recomendação técnica). Conecta com [[Servitização]] e [[Transformação de Mercado]].

**Prontidão de dado exigida:** muito alta + processos digitalizados + guardrails. Só é responsável depois de H1/H2 sólidos.

**Riscos:** overselling (vender "vendedor virtual" sobre dado fragmentado — prontidão IA hoje é "Inicial"); aceitação do cliente B2B; risco reputacional de agente que erra em cotação; sinalização organizacional de "projeto para demitir".

**KPIs (sua nota: aprendizado validado, experimentos):** nº de experimentos rodados · taxa de acerto do agente em ambiente controlado · % do fluxo passivo absorvido com segurança · NPS/retenção nas contas tocadas por agente · capacidade humana redirecionada para relacionamento.

**Horizonte:** 24–36+ meses · **Peso: ~10% (sementes e experimentos desde já, compromisso só após gates).**

---

## Comparação dos horizontes (espelho da sua nota, aplicado à Forja)

| Horizonte | Foco na Sacchelli | Risco | Retorno | Tempo | Peso |
|---|---|---|---|---|---|
| **H1** | Tirar o Softcomp do estático: fundação + inteligência | Baixo | Previsível | 0–12m | ~70% |
| **H2** | Automatizar processo + copilotos de gestão | Médio | Crescente | 12–24m | ~20% |
| **H3** | Operação AI-native: agentes + novo modelo comercial | Alto | Incerto | 24–36m+ | ~10% |

## Governança do portfólio

- **Regra de alocação:** ~70/20/10. Revisar trimestralmente. Se H1 escorregar, H2/H3 perdem direito a recurso — a fundação manda.
- **Gates de valor** entre horizontes (acima) são inegociáveis: não se escala o seguinte sem prova do anterior.
- **Propriedade do ativo:** código, pipelines, modelos e documentação devem ser **da Sacchelli**, com plano de capacitação interna — para não virar dependência permanente de fornecedor. (Vínculo direto com a decisão de contratação — ver avaliação DataSide.)
- **Fonte oficial por domínio** definida antes de qualquer painel entrar em produção (quem ganha quando Softcomp e Excel divergem).

## Riscos transversais ao projeto

- **Bus-factor = risco nº 1:** todo o ativo (motor, cubos, painéis, agente NLQ) foi construído por uma pessoa e vive num laptop. Ponto único de falha humano — mais perigoso que o gargalo do Softcomp. **Mitigação: Gate 0-B de sucessão técnica** (documentação independente, 2º operador, propriedade do código pela empresa) rodando em paralelo ao Gate 0.
- **Gargalo único:** acesso automatizado ao Softcomp. É pré-condição de H1 e, por herança, de tudo. **Gate 0.**
- **Conhecimento tácito** preso em planilhas e pessoas-chave, sem plano de extração.
- **Governança de dados/LGPD** ainda "Baixa" — precisa sair da ferramenta para o processo (dono, regra, retenção).
- **Adoção:** a casa já tem ferramentas próprias em que confia (SAC360, automações caseiras). A plataforma nova **compete com elas** — se for pior, é ignorada. São benchmark a superar, não "fragilidade a substituir".

## Primeiras decisões / próximos passos

1. **Disparar o Gate 0** — prova de acesso ao Softcomp (réplica de leitura), reproduzindo um indicador que já existe no SAC360 com paridade de número. É o experimento que valida ou mata o projeto inteiro, barato.
2. **Definir orçamento e alocação** pelos três horizontes (referência 70/20/10) e o teto de investimento.
3. **Escolher o piloto de H1** — recomendação: Comercial (mais maduro, dono claro, benchmark existente).
4. **Nomear donos de dado** por domínio (embrião da governança).
5. **Selar a propriedade do ativo** em qualquer contrato (código/pipeline/modelos = Sacchelli).
6. Rodar **1 experimento-semente de H3** em paralelo, pequeno e cercado (ex.: agente de cotação assistida com humano no loop), só para gerar aprendizado — sem compromisso de escala.

## Reflexão estratégica (as perguntas da sua nota, respondidas para a Forja)

- **Quanto do investimento está em cada horizonte?** Meta 70/20/10 — hoje quase tudo é H1 artesanal não industrializado.
- **Seu H2 está forte o suficiente para virar o próximo H1?** Ainda não — H2 depende de credenciais de terceiros e de qualidade de dado que o H1 precisa entregar primeiro.
- **Existe um H3 que pode transformar seu setor?** A aposta defensável não é "demitir vendedor", é **redesenhar a operação comercial em torno de relacionamento humano + camada transacional autônoma** — e, no limite, transformar inteligência em diferencial competitivo.

## Conexões

- [[Inovação H1, H2 e H3]]
- [[Servitização]]
- [[Transformação de Mercado]]
- [[Posicionamento Estratégico]]
- [[Modelo de Negócio]]
- `Logs/2026-06-21 — Avaliação Assessment DataSide (Data Lake + IA Sacchelli).md`
- `Logs/2026-06-21 — Perguntas à DataSide (assessment).md`
