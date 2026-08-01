---
tipo: armadilha-crítica
domínio: cotações
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [orçamento-prévio, projeto, tabelista, armadilha]
---

# 03 — Orçamento Prévio vs Projeto Real

## A armadilha mais cara do pipeline

O motivo de encerramento "Cotação somente para orçamento prévio" **engloba dois perfis completamente diferentes** de cliente. Tratamento confundido = ação oposta à que deveria ser.

---

## Os dois perfis

### Perfil A — Tabelista real
**Cliente que compra de outro fornecedor e usa AFS como referência de preço.**

Características:
- Cotação recorrente com AFS
- Nunca (ou quase nunca) vira pedido
- AFS é "cotação de base" (price check)
- Volume cotado considerável, conversão próxima de zero

**Tratamento correto:** industrializar atendimento
- Tabela automática (sem análise)
- Zero customização
- Zero engenharia
- Cotação em 5 minutos
- Ver [[04 - Cliente-Tabelista (flag proposta)]]

### Perfil B — Projeto real (CAPEX industrial)
**Cliente em fase de budget para planta nova, retrofit ou expansão.**

Exemplos confirmados por Gustavo (abr/2026):
- **ANDRITZ** — equipamentos industriais
- **PROK BRASIL** — equipamentos pesados
- **SUPERIOR** — grandes projetos

Características:
- Orçamentos **reais** de projeto industrial
- **Ciclo cotação → decisão de compra: 6-18 meses**
- Cliente precisa de precificação detalhada para seu budget
- Decisão final muito depois da cotação

**Problema atual:**
- **Vendedor encerra a cotação em 2-5 dias como "orçamento prévio"** porque o ERP não tem status adequado
- AFS **perde controle do funil** de projeto durante o período crítico de influência
- Concorrente que aparece toda semana (amostra, revisão técnica, reunião) **ganha** o projeto
- O que encerrou e sumiu vira memória

---

## Volume do problema

### Pipeline escondido (análise mar/2026)
- ~53% do pipeline de cotações vira "orçamento prévio"
- Dos 42 clientes com >80% do valor cotado encerrado como orçamento prévio:
  - Alguns são **tabelistas reais** (perfil A)
  - Outros são **projetos reais** (perfil B)
- **Não sabemos exatamente** quanto é A e quanto é B sem análise caso a caso

### Estimativa de impacto
**R$174M de pipeline encerrado** em Q1+abr/26 provavelmente contém **dezenas de projetos** que vão fechar com concorrente por falta de follow-up da AFS.

**Não é disciplina** — é **infraestrutura de processo inexistente**.

---

## Tratamento oposto

| Dimensão | Perfil A (Tabelista) | Perfil B (Projeto) |
|---|---|---|
| Frequência de contato | Baixa (industrializado) | **Alta (semanal/quinzenal)** |
| Personalização | Zero | **Máxima** |
| Engenharia | Zero | **Recursos dedicados** |
| Prazo esperado | Dias | **Meses** |
| Investimento de tempo AFS | Mínimo | **Máximo** |
| Métrica-chave | % de cotações aceitas | **Taxa de ganho no fechamento** |

**Industrializar tratamento do Perfil B seria entregar o projeto ao concorrente.**

---

## Alavanca estrutural (proposta — não implementada)

### Status novo no Softcomp: "Em Projeto"

**Características:**
- **Não-encerramento automático** (cotação não fecha sozinha)
- **Follow-up forçado** em 30/60/90 dias (sistema cobra retorno)
- **Só pode ser encerrada como:**
  - Ganhou
  - Perdeu
  - Projeto Cancelado
  - **NUNCA** como "orçamento prévio"
- **Métricas novas:**
  - Valor em carteira de projeto
  - Idade média dos projetos
  - Projetos tocados (com interação recente) vs esquecidos (>90d sem contato)
  - Taxa de conversão de projeto (quanto de projeto vira pedido?)

### Impacto esperado
- Visibilidade do pipeline de projeto (hoje invisível)
- Disciplina de follow-up forçada
- Recuperação de projetos que iam cair por inércia

### Barreira para implementação
- Customização no Softcomp (requer fornecedor do ERP ou dev)
- Treinamento do time para usar novo status corretamente
- Cultura comercial de "vender = fechar rápido" precisa mudar

---

## Ações imediatas (enquanto estrutural não vem)

### 1. Identificação manual de projetos
Revisar cotações encerradas como "orçamento prévio" com:
- Valor alto (>R$X threshold)
- Cliente conhecido como indústria pesada (ANDRITZ, PROK, SUPERIOR, equivalentes)
- Reabrir ou criar follow-up manual

### 2. Flag em ferramenta paralela
Motor Analítico v2 pode gerar **lista de cotações suspeitas de serem projetos**:
- Critérios: valor > R$100k + cliente industrial + encerrada como orçamento prévio < 15 dias
- Output: lista para revisão semanal

### 3. Processo comercial
Regra interna: **cotações acima de X valor** não podem ser encerradas como orçamento prévio sem aprovação do gerente.

### 4. Lista de clientes-projeto conhecidos
Manter planilha com clientes que são **sempre** projeto (ANDRITZ, PROK, SUPERIOR, etc.) e seus padrões de comportamento. Tratamento automático diferenciado.

---

## Comparação com concorrentes

Tradings (Duferco, DITH) e distribuidores grandes **sabem disso e operam diferente:**
- Dedicam KAM (Key Account Manager) para projetos industriais
- Follow-up estruturado
- Investimento em relacionamento de longo prazo

AFS está em **desvantagem estrutural** em pipeline de projeto. Corrigir é alavanca grande.

---

## Métricas ideais (quando estrutural existir)

### Dashboard "Pipeline de Projeto"
- # de projetos ativos
- Valor em carteira
- Idade média (dias desde última interação)
- Projetos por fase (budget, spec, orçamento, decisão)
- Taxa de conversão por ciclo
- Top 10 projetos por valor
- Top 10 clientes de projeto

### KPIs
- **Taxa de atividade:** % de projetos com interação nos últimos 30d
- **Taxa de conversão:** projetos fechados / projetos iniciados
- **Ticket médio de projeto:** R$ médio por projeto fechado
- **Ciclo médio:** tempo médio de conversão

---

## Conexões

- [[00 - Visão Geral Cotações]]
- [[01 - Inbound vs Outbound (ficção do ERP)]]
- [[02 - Motivos de Encerramento]]
- [[04 - Cliente-Tabelista (flag proposta)]]
- [[05 - Win Rate e Métricas]]
- [[01 Sistema de Dados/01 - ERP Softcomp - Detalhes]]
- Vault estratégico: [[Cliente Ideal]]

## Memórias relacionadas
- `project_afs_pipeline_projeto`
- `project_afs_cotacao_orcamento_previo`
