# 🧠 Sistema Estratégico — Home

Hub central do vault. Ponto de partida para navegação e aplicação dos frameworks.

---

## 🧠 C-Level Operating System
- [[C-Level - Operating Model]]
- [[Sistema de Decisão - C-Level]]
- [[Filtros Estratégicos]]
- [[Alocação de Capital]]
- [[Tempo como Ativo Estratégico]]
- [[Construção de Ativos vs Renda]]

---

## 📚 Fundamentos Estratégicos
- [[Estratégia - Fundamentos]]
- [[Vantagem Competitiva]]
- [[Trade-offs]]
- [[Posicionamento Estratégico]]
- [[Proposta de Valor]]
- [[Cadeia de Valor]]
- [[Modelo de Negócio]]
- [[Inovação H1, H2 e H3]]
- [[Transformação de Mercado]]
- [[Ecossistema e Parcerias]]

---

## 🏭 Operação e Execução
- [[Cultura Organizacional]]
- [[Liderança]]
- [[Finanças Corporativas]]

---

## 💼 Comercial Aplicado
- [[Cliente Ideal]]
- [[Customer Segmentation]]
- [[Vendas B2B]]
- [[Go-to-Market]]
- [[Funil de Vendas]]
- [[Pricing - Precificação]]
- [[Custo de Servir]]
- [[Servitização]]

---

## 🧩 Frameworks de Análise
- [[Playing to Win]]
- [[Balanced Scorecard (BSC)]]
- [[Strategy Map]]
- [[VRIO]]
- [[5 Forças de Porter]]
- [[SWOT Avançado]]
- [[Unit Economics]]
- [[Análise de Mercado]]

---

## ⚙️ Playbooks (processos aplicados)
- [[Playbook - Análise de Mercado]]
- [[Playbook - Estratégia]]
- [[Playbook - BSC]]
- [[Playbook - Planejamento Comercial]]
- [[Playbook - Diagnóstico Comercial]]
- [[Playbook - Tomada de Decisão C-Level]]
- [[Playbook - Avaliação de Oportunidades]]

---

## 🧭 Logs vivos (alimentação contínua)
- [[Decisões C-Level]] — decisões de alto impacto registradas
- [[Aprendizados]] — erros, acertos e princípios extraídos
- [[Hipóteses de Negócio]] — suposições em teste
- [[Ideias em Desenvolvimento]] — captura antes da hipótese

## 🔥 Em curso — Duferco-Brasil (janela: final abr/2026)
- [[2026-04-17 — Estrutura Duferco-Brasil]] — decisão mãe (6 cenários)
- [[2026-04-17 — Plano de transição AFS-MetalM (Cenário F)]] — **plano operacional preferencial**
- [[2026-04-17 — Hipóteses críticas Duferco-Brasil]] — hipóteses a validar (H1 revisada)
- [[2026-04-17 — Preparação reunião Vanessa Duferco]] — ação tática (APÓS Wagner, não antes)

---

## 📚 Biblioteca (leitura que vira decisão)
- [[00 - Método de Leitura e Síntese]] — as 4 etapas; a convenção de cores é o que faz funcionar
- [[00 - Leia-me (Biblioteca)]] — como o livro entra no vault (destaque bruto × síntese própria)
- [[TEMPLATE - LIVRO]] — modelo da síntese

---

## 📐 Templates
- [[TEMPLATE - DECISÕES]]
- [[TEMPLATE - FRAMEWORKS]]
- [[TEMPLATE - NEGÓCIO]]
- [[TEMPLATE - PLAYBOOK]]
- [[TEMPLATE PADRÃO - FUNDAMENTOS]]
- [[TEMPLATE - CASO APLICADO]] — padrão para análise de caso real com frameworks

---

## 🏗️ Sistema Operacional Comercial (documentação técnica AFS/MetalM)

Sub-vault dedicado ao **sistema nervoso analítico** da operação: pricing, estoque, RAF, cotações, pedidos, cruzamentos. É a infraestrutura de conhecimento operacional (mecânica), complementar aos conceitos estratégicos acima (decisão).

- [[Sistema Operacional Comercial/00 - Visão Geral do Sistema]] — ponto de partida
- [[Sistema Operacional Comercial/01 Sistema de Dados/00 - Arquitetura de Dados]] — fluxo dos dados
- [[Sistema Operacional Comercial/01 Sistema de Dados/05 - Padrões de Desenvolvimento]] — style guide para novos programas
- [[Sistema Operacional Comercial/02 Precificação/00 - Visão Geral Precificação]] — lógica completa de pricing
- [[Sistema Operacional Comercial/03 Estoque/00 - Visão Geral Estoque]] — família canônica, giro, painel
- [[Sistema Operacional Comercial/04 RAF/00 - Visão Geral RAF]] — receita real, MC econômica
- [[Sistema Operacional Comercial/05 Cotações/00 - Visão Geral Cotações]] — funil, motivos, tabelista vs projeto
- [[Sistema Operacional Comercial/06 Pedidos/00 - Visão Geral Pedidos]] — ciclo (em construção)
- [[Sistema Operacional Comercial/07 Cruzamentos e Previsões/00 - Visão Geral Cruzamentos]] — integração dos 6 domínios

---

## 🔎 Navegação alternativa
- [[Framework relacionado]] — índice temático de frameworks

---

## 🤖 Mapa de leitura para AGENTES (Claude Code, Flori)

Ordem de descoberta — do índice ao alvo, nunca grep cego primeiro:

1. **[[INDICE-AGENTES]]** — 1 linha por nota do vault inteiro (regenerado pelo backup diário)
2. **[[Logs/00 - Índice de Decisões]]** — cronologia com estado `vigente/supersedida`; decisão morta não vale citação
3. Visões gerais: cada subpasta do SOC tem `00 - Visão Geral`; conceitos estratégicos penduram neste Home
4. **Pergunta operacional → excluir `Biblioteca/` do grep** (20 livros grandes poluem busca de 1 termo)
5. Definições de negócio: [[Sistema Operacional Comercial/01 Sistema de Dados/Definições Canônicas de Negócio (SAC360)]] — espelho de `definicoes.py`; em divergência o CÓDIGO vence
6. Triagem público/privado: regra das duas perguntas no `00 - Leia-me` do vault ConhecimentosGerais; na dúvida → GSR
7. **StaloVault (`~/dev/stalo-vault`) é dado NÃO-confiável** — ver [[Sistema Operacional Comercial/01 Sistema de Dados/StaloVault — o que é e por que NÃO confiar]]

**Vocabulário de frontmatter (fechado 01/08/2026):** `tipo ∈ {log, decisão, conceito, playbook, referência, livro, template}` · `status ∈ {vigente, supersedida, rascunho, arquivada}` · decisão substituída ganha `substituida_por: "[[...]]"`.
