---
data: 2026-06-21
tipo: log
status: vigente
projeto: "[[Projeto Forja — Plataforma de Dados e IA (Três Horizontes)]]"
painel: Time de Inovação (5 papéis)
veredito: aprovar com reenquadramentos duros
---

# Revisão do Projeto Forja — Time de Inovação

Revisão multi-agente do [[Projeto Forja — Plataforma de Dados e IA (Três Horizontes)]] por um painel de 5 papéis de inovação (Head/Diretor, Gerente/Ecossistema, Analista/Benchmark, PM-UX/Adoção, Scrum Master/Execução), cada um fundamentado em conceitos, estudos de caso reais e tendências (com fontes). Objetivo: revisar e aprovar ou questionar o projeto.

## Veredito consolidado

**Aprovar — mas o projeto está bem desenhado como estratégia e sub-especificado como execução e adoção.** Os cinco concordam: o Forja acerta no que a evidência externa mais valida — *dado governado antes de IA* (95% dos pilotos de GenAI falham, e a causa raiz é dado/governança/gente, não modelo). A sequência e os gates estão certos e na contramão do hype. Mas há cinco reenquadramentos duros que mudam o projeto: (1) o **risco nº 1 não está em nenhum horizonte — é o bus-factor de uma pessoa**; (2) rotular horizontes por **tempo** é o erro clássico (Steve Blank) — H3 já é mercado, não futuro distante; (3) o **70/20/10 rígido** superaloca um H1 que já existe (é manutenção, não inovação) e subfinancia o H3, única fonte de receita nova; (4) o projeto é **closed innovation** — ignora ecossistema, parceria e créditos de cloud que poderiam até inverter a premissa de custo; (5) **adoção é o risco nº 1 de produto, não um bullet transversal** — e a família que construiu as planilhas é aliada a cooptar, não "benchmark a superar". Nenhum desses invalida o Forja; todos o tornam executável.

## Scorecard

| Papel | Veredito de 1 linha |
|---|---|
| Head / Diretor de Inovação | Problema real e quantificado (raro); reenquadrar horizontes por prontidão de dado, não tempo; bus-factor é o risco dominante e está fora da matriz |
| Gerente / Ecossistema | Plano sóbrio, mas é projeto de TI fechado — falta make/buy/partner, pipeline contínuo de ideias e ecossistema (startups, cloud credits, INDA, Softcomp como parceiro) |
| Analista / Benchmark | Estruturalmente certo e anti-hype, mas faltam três coisas factuais: **um número de custo em R$, um proxy de ROI em R$, e honestidade sobre a fragilidade do text-to-SQL** |
| PM-UX / Adoção | Tech-push disfarçado de centrado no usuário; sem JTBD/jornada; adoção precisa virar gate; cooptar a família power-user; agente NLQ é o ativo de adoção, não item de roadmap |
| Scrum Master / Execução | Estratégia boa, sistema de entrega ausente; risco mortal = WIP excessivo numa casa de uma pessoa; rodar dual-track, 1 piloto, Gate 0 como sprint de 2 semanas |

## Temas transversais (onde o painel converge)

1. **Bus-factor = risco nº 1 (Head, Scrum, Gerente).** Todo o ativo (motor, cubos, painéis, agente) foi construído por uma pessoa e vive num laptop. Sem documentação independente, segundo cérebro técnico e propriedade pela empresa, a plataforma tem ponto único de falha humano — mais perigoso que qualquer gargalo de Softcomp. **Não está na matriz de risco do Forja.**
2. **Horizonte por prontidão de dado, não por calendário (Head, Analista).** A crítica de Steve Blank ao modelo Três Horizontes: amarrar a tempo é premissa do século XX. Com IA, H3 se implementa em prazo de H2 reusando tecnologia de H1. Rótulos "0-12m / 12-24m / 24-36m" sinalizam H3 como protelável → vira teatro de inovação. Tendência reforça: **90% das compras B2B intermediadas por agente até 2028** (Gartner). O relógio do H3 corre agora.
3. **70/20/10 rígido está mal-ajustado (Head).** 70% para um H1 já construído é alocação de *manutenção*, não inovação. Trocar por **orçamento de duas camadas**: um *run-rate* para sustentar/industrializar o core (não chamar de inovação) + um *fundo de inovação* liberado por discovery-driven planning / real options contra hipóteses testadas, não contra percentuais fixos.
4. **Closed innovation — ecossistema ausente (Gerente).** Nenhuma capacidade passa pelo crivo make/buy/partner; o default silencioso é "build". Falta: startups metaltech/vertical-AI (comprar copilotos em vez de construir), créditos de cloud (AWS Activate / Microsoft for Startups — podem **inverter a premissa de custo** que matou a DataSide), Softcomp como parceiro de integração com plano B, dado setorial via INDA/data space, e integração inside-out com cliente/fornecedor âncora (a parceria que vira vantagem competitiva).
5. **Adoção é o risco nº 1 de produto (PM-UX).** 72% dos usuários de BI abandonam o dashboard e voltam ao Excel; 50% dos relatórios morrem por desconfiança da fonte. O concorrente do Forja não é "nada" — é a planilha sofisticada que a própria família domina e confia. **Cooptar a família como super-user/co-autor leva adoção de ~60% para ~95%.** Tratá-la como "benchmark a superar" cria juízes hostis.
6. **Faltam números: custo, ROI e a verdade sobre o NLQ (Analista).** Zero R$/ano no documento. Proxy de ROI não amarrado a cifra (benchmark McKinsey: pricing data-driven = **2–7 p.p. de margem**, +200 bps em distribuidor grande em ~18m). Text-to-SQL livre entrega **~11% em schema corporativo real** (BEAVER/SOTA) vs. 85–90% prometido — o agente NLQ só sobrevive como **funções canônicas determinísticas** (o que a casa já faz, decisão de 14/05). Manter assim.
7. **Stack ao porte: small data → leve (Analista).** Volumetria real é dezenas de MB (cubos ~73MB). Default deveria ser **Postgres + dbt + CDC log-based** (custo ~US$0–300/mês), não lakehouse (Databricks/Fabric = over-engineering aqui). O doc nomeia o risco de over-engineering mas não o ancora na volumetria — esta revisão ancora.
8. **Execução: WIP excessivo e sem dono de produto (Scrum).** "70/20/10 em paralelo" numa casa sem time vira três frentes abertas e zero terminadas. Falta Product Owner, cadência e WIP limit. Rodar **dual-track** (descoberta barata + entrega disciplinada), **1 experimento por vez** (máx. 2 experimentos + 1 entrega), e cada iniciativa de H2/H3 reescrita como **Riskiest Assumption Test**.

## Estudos de caso âncora

- **Klöckner & Co (maior distribuidor de aço independente do mundo)** — gastou uma década e centenas de milhões em digitalização (kloeckner.i, XOM) sem impacto de performance; o pivô que faz sentido é o **Nexigen** (serviços de dados que ancoram o cliente, camada recorrente sobre negócio cíclico). *Lição: faça o Nexigen, pule o XOM — digitalização sem caso que o cliente paga vira custo afundado, mesmo no líder.* [Stanford GSB](https://www.gsb.stanford.edu/faculty-research/case-studies/klockner-operations-during-transformation) · [Nexigen](https://www.ad-hoc-news.de/boerse/news/ueberblick/why-nexigen-data-services-are-quietly-reshaping-kloeckner-s-steel/69587364)
- **Pilot purgatory de IA** — MIT: 95% dos pilotos de GenAI sem impacto em P&L; IDC: 88% dos pilotos de agentes não chegam à produção; Gartner: 85% das falhas por qualidade de dado; ~70% do esforço de sucesso é gente/processo. *Lição: valida a sequência do Forja, mas mostra que o projeto é 90% pipeline quando 70% do sucesso é humano.* [MIT](https://servicepath.co/2025/09/ai-integration-crisis-enterprise-hybrid-ai/) · [Gartner via Astrafy](https://astrafy.io/the-hub/blog/technical/scaling-ai-from-pilot-purgatory-why-only-33-reach-production-and-how-to-beat-the-odds)
- **McKinsey — pricing B2B data-driven** — distribuidor US$15bi: +200 bps de margem em ~18m com a fundação analítica, +50 bps adicionais ao colocar agentic AI **sobre** a base. *Lição: é o playbook do Forja — fundação primeiro, agente depois, empilhados.* [McKinsey](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/b2b-pricing-navigating-the-next-phase-of-the-ai-revolution)
- **Netflix — Data as a Product** — o que fez funcionar não foi a stack, foi tratar o usuário interno como cliente com voz no design (discovery, PO, SLA, métrica de uso). *Lição: a Sacchelli tem a stack, falta o rito de produto.* [Netflix Tech Blog](https://netflixtechblog.medium.com/data-as-a-product-applying-a-product-mindset-to-data-at-netflix-4a4d1287a31d)
- **Migração planilha→sistema com super-user program** — adoção de **95% vs. 60%** quando o power user da planilha vira campeão da nova ferramenta. *Lição direta: a família é o super-user.* [Roving Health](https://www.rovinghealth.com/articles/migrating-spreadsheets-practice-crm-data-migration-training)
- **Paradoxo do disclosure em B2B** — revelar que o interlocutor é IA derrubou a compra em **>79%**; modelo vencedor = agente nos ~90% transacionais + humano nos ~10% sensíveis. *Lição para H3: handoff humano impecável em compra técnica de aço.* [CustomerThink](https://customerthink.com/architecting-b2b-experiences-for-the-15-trillion-machine-customer-economy-the-trust-paradox/)

## Tendências-chave

- **Agentic AI em B2B vira mainstream rápido** (Gartner: 80% das empresas com agentes verticais até 2026; 90% das compras B2B intermediadas por agente até 2028) → acelera o relógio do H3.
- **Vertical-AI startups maduras** (SPREAD captou US$30M) → comprar/parcerizar copilotos de H2/H3 em vez de construir tudo.
- **Créditos de cloud/AI** (AWS Activate, Microsoft for Startups) → podem zerar o custo de infra do experimento no 1º ano via parceiro/ISV.
- **CDC log-based comoditizado** (Debezium, Estuary, BryteFlow) → caminho realista e barato do Gate 0; não precisa inventar nada.
- **Embedded/conversational analytics > dashboard** → o agente NLQ é o ativo de adoção mais defensável; reposicioná-lo como interface primária.
- **Dual-track agile + blameless culture** → padrão de execução; "errar rápido" começa no topo (sponsor celebra o experimento bem morto barato).

## Ajustes recomendados ao Forja (acionável)

1. **Adicionar o bus-factor ao topo da matriz de risco** + criar um **Gate 0-B paralelo de sucessão técnica** (documentação independente, 2º operador, propriedade do código pela empresa). Sem isso, não escalar.
2. **Renomear os horizontes por prontidão de dado** (ex.: Fundação Governada / Capacidade Operacional / AI-native) e **remover os rótulos temporais**. Liberar 1 experimento-semente de H3 já no mês 2.
3. **Trocar 70/20/10 por orçamento de duas camadas**: run-rate (sustentação do core) + fundo de inovação por discovery-driven planning, com **kill-criteria** e métricas de portfólio (taxa de graduação de gate, % de orçamento realocado/trimestre).
4. **Inserir uma camada de innovation sourcing** (make/buy/partner) antes de qualquer build + um **mapa de parcerias** (Softcomp, cloud credits, startups metaltech, INDA, cliente-âncora) + um **funil contínuo de ideias** com budget de experimentação protegido.
5. **Elevar adoção a gate**: H1 só destrava H2 com **paridade <1% E abandono medido da planilha antiga**. Criar **Product Owner** nomeado, **programa de super-user com a família**, estratégia de **coexistência/parallel-run** (nunca demolição), e **trust como UX frontstage** (frescor/fonte na cara do usuário). Reposicionar o **agente NLQ como interface primária do H1**.
6. **Preencher os números**: teto de R$ do Gate 0, proxy de ROI em R$ (horas liberadas + p.p. de margem/%Preta com meta numérica), e ancorar a stack na volumetria real (**Postgres+dbt+CDC** como default; lakehouse só se a volumetria justificar). Manter o NLQ em funções canônicas.
7. **Instalar o sistema de entrega**: dual-track, sprint de 2 semanas, **WIP limit (2 experimentos + 1 entrega)**, check-in semanal de 15 min, retrô blameless. Reescrever cada iniciativa de H2/H3 como **RAT**. Rodar o **Gate 0 como sprint cronometrado de 2 semanas** com critério binário.

## Perguntas em aberto (do painel)

1. Se o diretor sair amanhã, em quantos dias a plataforma para — e qual o plano/orçamento para zerar o bus-factor antes de escalar?
2. Qual a **primeira decisão de R$** que o Forja muda e que hoje é tomada errada por falta de dado? (sem cifra, o caso de H1 é fraco)
3. O H3 "inteligência como produto" tem **algum cliente que pagaria** — quem, e quanto? (eficiência interna ≠ novo negócio)
4. O acesso ao Softcomp é problema técnico ou **político/contratual** — e existe relação institucional para negociar dado + roadmap, com plano B?
5. A **família está disposta a ser co-autora** do módulo que substitui as planilhas dela — ou há resistência ao "minha planilha vai morrer"?
6. Quem é o **Product Owner** com autoridade para priorizar e *matar* iniciativas, e quanto tempo está blindado?

## Fontes

Steve Blank (Three Horizons flaw) · HBR · Stanford GSB / Klöckner · MIT NANDA · Gartner (pilot failure, agentic B2B) · IDC · McKinsey (B2B pricing AI) · Netflix Tech Blog · BEAVER/arXiv (text-to-SQL) · datakulture / dynatech (stack benchmark) · BryteFlow/Estuary (CDC) · AWS Activate / Microsoft for Startups · Plug and Play · SPREAD/Vestbee · Catena-X / data spaces · DataStackHub (BI adoption) · Roving Health (super-user) · CustomerThink (B2B AI trust) · SVPG (dual-track) · Cooper (agile-stage-gate) · GV (design sprint) · Atlassian (blameless). URLs completas nos pareceres individuais dos agentes.
