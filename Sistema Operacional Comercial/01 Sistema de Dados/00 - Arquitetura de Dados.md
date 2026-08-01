---
tipo: overview
domínio: sistema-de-dados
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [sistema-de-dados, arquitetura, overview, erp, softcomp]
---

# 00 — Arquitetura de Dados

## Princípio central

**O ERP Softcomp é a fonte de verdade.** Tudo o que é analisado deriva de exports dele. Ferramentas analíticas (simulador, painel, motor) são **camadas de interpretação** — nunca fontes independentes.

Se uma ferramenta reporta número que não bate com o Softcomp: **o Softcomp está certo**, a ferramenta precisa ser calibrada.

---

## Camadas do sistema

```
┌────────────────────────────────────────────────────────────┐
│  CAMADA 1 — FONTE (Softcomp ERP)                            │
│  IP interno: 10.0.0.215 (SGRA_SACCH)                        │
│  Banco: SQL Server                                          │
│  Tabelas: cadastros, cotações, pedidos, faturamento, etc.   │
└─────────────────────────┬──────────────────────────────────┘
                          │ Export manual / agendado
                          ▼
┌────────────────────────────────────────────────────────────┐
│  CAMADA 2 — ARQUIVOS BRUTOS (Excel / CSV)                   │
│  DetalhesRAF.xlsx, Cot_Encerradas.xlsx, Estoque.xlsx,       │
│  tabela_preco.xlsx, Critérios_planilhas.xlsx                │
└─────────────────────────┬──────────────────────────────────┘
                          │ Processamento / leitura
                          ▼
┌────────────────────────────────────────────────────────────┐
│  CAMADA 3 — FERRAMENTAS ANALÍTICAS                          │
│  Simulador HTML • Painel Estoque HTML • Motor Analítico     │
│  Dashboards ad-hoc                                          │
└─────────────────────────┬──────────────────────────────────┘
                          │ Visões estruturadas
                          ▼
┌────────────────────────────────────────────────────────────┐
│  CAMADA 4 — DECISÃO COMERCIAL                               │
│  Pricing • Gestão de carteira • Alocação • Forecast         │
└────────────────────────────────────────────────────────────┘
```

---

## Camada 1 — ERP Softcomp

### O que é
ERP proprietário usado pela AFS para operação completa: cadastros, cotação, pedido, faturamento, estoque, fiscal, financeiro.

### Restrições conhecidas
- **Banco SQL Server interno** (IP 10.0.0.215) — fora da rede externa
- **Conexão direta não disponível** em ambiente externo (casa, cloud, sandbox)
- **Na v1 do Motor Analítico, dados chegam via export Excel** — conexão direta fica para v2
- **Truncamento em campo CIDADE (20 chars)** — ver [[04 - Qualidade de Dados]]

### Exports principais usados
| Export | Conteúdo | Frequência | Ferramenta que consome |
|---|---|---|---|
| `DetalhesRAF.xlsx` | 133 colunas, faturamento detalhado | Mensal (idealmente semanal) | [[Sistema Operacional Comercial/04 RAF/00 - Visão Geral RAF]], Motor Analítico |
| `Cot_Encerradas.xlsx` | Cotações finalizadas com motivo | Conforme análise | [[Sistema Operacional Comercial/05 Cotações/00 - Visão Geral Cotações]], Motor Analítico |
| `tabela_preco.xlsx` | Tabelas A/B/C por produto | Mensal ou ao mudar | [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]] |
| `Estoque.xlsx` | Posição de estoque, giro | Semanal | [[Sistema Operacional Comercial/03 Estoque/00 - Visão Geral Estoque]] |
| `Critérios_planilhas.xlsx` | Regras: famílias, bitolas, cidades | Sob demanda | Motor Analítico, Painel Estoque |

---

## Camada 2 — Arquivos brutos

### Princípio
Arquivos brutos são **snapshots temporais**. Cada export tem data e deve ser nomeado consistentemente:
- `DetalhesRAF_YYYYMMDD.xlsx` (data do export)
- `Cot_Encerradas_YYYYMMDD.xlsx`
- `Estoque_YYYYMMDD.xlsx`

### Convenção de versionamento
- Arquivos de **dados operacionais** (RAF, Estoque): datados por export
- Arquivos de **configuração** (critérios, taxonomia): versionados por data de mudança significativa
- Arquivos-fonte editáveis (Critérios_planilhas): Gustavo edita → motor rebuilda → nova versão do HTML derivado

### Pasta e organização
Localização atual: `~/Documents/Personal/00. Projetos - Claude/Planejamento Estratégico - Comercial/`
Subpastas: `MotorAnalitico/`, `Arquivo/`, `MetalM/`

---

## Camada 3 — Ferramentas analíticas

### Ferramentas em produção
1. **Simulador de Precificação HTML** (`Analise_Precificacao_Sacchelli.html`)
   - 5.300+ linhas, self-contained, Entrega 1 multi-item validada
   - Ver [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]]

2. **Painel de Estoque HTML** (`Estoque_Sacchelli_YYYY-MM-DD.html`)
   - Gerado a partir do Excel de estoque + Critérios_planilhas
   - Versão atual: Estoque v2 — **padrão canônico para novos dashboards**

3. **Motor Analítico v1** (Python local, em codificação)
   - Backbone: ingestão RAF + cotações + critérios
   - Output: HTML dashboard semanal

### Ferramentas em desenvolvimento / PRD
4. **Simulador Web App** (Node.js/React/SQLite) — PRD concluído, implementação pausada
5. **Dashboard de Cotações Pendentes** — em construção
6. **Análise de Pedidos** — em construção

### Princípio arquitetural (ver [[05 - Padrões de Desenvolvimento]])
- **HTML self-contained** para distribuição simples + offline
- **Python local** para processamento pesado (RAF, cruzamentos)
- **Sem SaaS, sem cloud** — dados não saem da máquina (decisão de segurança + confidencialidade)

---

## Camada 4 — Decisão comercial

Ferramentas servem decisões em 4 eixos:
1. **Pricing** — que preço praticar? qual MC está adequada?
2. **Carteira** — quais clientes investir, renegociar, descontinuar?
3. **Alocação** — onde alocar estoque, tempo comercial, capacidade?
4. **Forecast** — o que esperar de faturamento, margem, pipeline?

Cada eixo tem ferramentas-chave:

| Decisão | Ferramenta primária | Apoio |
|---|---|---|
| Pricing de item/pedido | Simulador | RAF (calibração) |
| Pricing de carteira | Motor Analítico | RAF |
| Gestão de carteira | Motor Analítico | RAF, Cot_Encerradas |
| Saúde de estoque | Painel Estoque | Estoque.xlsx + Critérios |
| Forecast | Em construção (cruzamento) | Cotação + Pedido + RAF |

---

## Fluxo semanal (processo recorrente ideal)

> Esta é a rotina-alvo, ainda não totalmente implementada — motor Python em construção automatizará parte.

**Segunda-feira manhã:**
1. Export Softcomp: RAF, Cotações Encerradas, Estoque
2. Drop arquivos em pasta do motor (`MotorAnalitico/input/`)
3. Rodar motor Python → gera HTML dashboard
4. Revisar dashboard → anotar 3-5 insights

**Durante a semana:**
5. Usar Simulador para novas cotações
6. Consultar Painel Estoque ao planejar pedidos
7. Escalar insights para decisões via [[Decisões C-Level]]

**Sexta-feira:**
8. Registrar aprendizados da semana em [[Aprendizados]]
9. Atualizar hipóteses em [[Hipóteses de Negócio]] se houver sinal

---

## Dependências e interconexões entre domínios

```
    Precificação (02)
         │
         │ usa taxonomia de
         ▼
       Família Canônica ←─── Estoque (03)
         │                      │
         │                      │ movimento alimenta
         ▼                      ▼
       Cotações (05) ──────→ Pedidos (06)
                                │
                                │ vira
                                ▼
                              RAF (04)
                                │
                                │ realimenta
                                ▼
                        Cruzamentos (07)
                                │
                                │ gera
                                ▼
                          Insight de decisão
```

Ou seja: **família canônica é a chave comum** que permite cruzar pricing, estoque, cotação, pedido e RAF.

---

## Notas correlatas neste domínio

- [[01 - ERP Softcomp - Detalhes]] — estrutura, limitações, acessos
- [[02 - Arquivos Brutos e Convenções]] — nomenclatura, pastas, versionamento
- [[03 - Ferramentas Analíticas - Inventário]] — todas as ferramentas e seus estados
- [[04 - Qualidade de Dados]] — problemas conhecidos e mitigações
- [[05 - Padrões de Desenvolvimento]] — style guide para novos programas
- [[06 - Motor Analítico v1]] — arquitetura e implementação

## Referência externa
- Pasta de arquivos brutos: `~/Documents/Personal/00. Projetos - Claude/Planejamento Estratégico - Comercial/`
- SQL Server AFS: 10.0.0.215 (SGRA_SACCH) — rede interna AFS apenas
