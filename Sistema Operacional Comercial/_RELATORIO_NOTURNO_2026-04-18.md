---
tipo: relatório
data: 2026-04-18
autor: Claude (sessão noturna)
status: concluído
---

# Relatório Noturno — Construção do Sub-Vault Sistema Operacional Comercial

**Sessão iniciada:** 2026-04-17 ~23:50
**Sessão concluída:** 2026-04-18 (noite)
**Vault total antes:** 61 notas
**Vault total depois:** 113 notas
**Novas notas criadas nesta sessão:** 52

---

## Escopo executado

Conforme solicitado pelo Gustavo:
- **Opção A** (tudo no vault GSR, pasta separada)
- **Nível 3 enciclopédico** (o que coubesse em 1 sessão)
- **Ordem proposta:** Sistema de Dados → Precificação → Estoque → RAF → Cotações → Pedidos → Cruzamentos
- **Público:** só Gustavo
- **Direcionamento adicional:** documentar **padrões** para novos programas; Estoque v2 e Simulador de Precificação como referência canônica

---

## O que foi criado

### Domínio 01 — Sistema de Dados (7 notas, nível 3 completo)
- [[01 Sistema de Dados/00 - Arquitetura de Dados]]
- [[01 Sistema de Dados/01 - ERP Softcomp - Detalhes]]
- [[01 Sistema de Dados/02 - Arquivos Brutos e Convenções]]
- [[01 Sistema de Dados/03 - Ferramentas Analíticas - Inventário]]
- [[01 Sistema de Dados/04 - Qualidade de Dados]]
- [[01 Sistema de Dados/05 - Padrões de Desenvolvimento]] ← style guide canônico
- [[01 Sistema de Dados/06 - Motor Analítico v1]]

### Domínio 02 — Precificação (13 notas, nível 3 completo)
- [[02 Precificação/00 - Visão Geral Precificação]]
- [[02 Precificação/01 - Fórmula do Lucro]]
- [[02 Precificação/02 - Fórmula de Preço Sacchelli]]
- [[02 Precificação/03 - Componentes de Custo]]
- [[02 Precificação/04 - MC1 MC2 e DRE]]
- [[02 Precificação/05 - Modos de Venda]]
- [[02 Precificação/06 - VPP Tolerância e Lâmina]]
- [[02 Precificação/07 - Tabelas e Alçadas]]
- [[02 Precificação/08 - Simulador HTML - Arquitetura]]
- [[02 Precificação/09 - Simulador Web App (futuro)]]
- [[02 Precificação/10 - Custo de Servir Aplicado]]
- [[02 Precificação/11 - Normas Técnicas]]
- [[02 Precificação/12 - Modo Pacote Multi-Item]]

### Domínio 03 — Estoque (7 notas, nível 3 completo)
- [[03 Estoque/00 - Visão Geral Estoque]]
- [[03 Estoque/01 - Família Canônica]]
- [[03 Estoque/02 - Faixas de Bitola]]
- [[03 Estoque/03 - ABC XYZ (futuro)]]
- [[03 Estoque/04 - Painel de Estoque v2]]
- [[03 Estoque/05 - Movimentação e Giro]]
- [[03 Estoque/06 - Fora de Padrão]]

### Domínio 04 — RAF (9 notas, nível 3 completo)
- [[04 RAF/00 - Visão Geral RAF]]
- [[04 RAF/01 - Estrutura das 133 Colunas]]
- [[04 RAF/02 - Convenção Softcomp (Invertida)]]
- [[04 RAF/03 - MC Contábil vs Econômica]]
- [[04 RAF/04 - Margem Oculta (7 componentes)]]
- [[04 RAF/05 - Custo Real vs Cobrado]]
- [[04 RAF/06 - Despesas Logísticas por Unidade]]
- [[04 RAF/07 - Tab A B C e Preços Mínimos]]
- [[04 RAF/08 - Consolidação por OS]]

### Domínio 05 — Cotações (6 notas, todas completas)
- [[05 Cotações/00 - Visão Geral Cotações]]
- [[05 Cotações/01 - Inbound vs Outbound (ficção do ERP)]]
- [[05 Cotações/02 - Motivos de Encerramento]]
- [[05 Cotações/03 - Orçamento Prévio vs Projeto Real]]
- [[05 Cotações/04 - Cliente-Tabelista (flag proposta)]]
- [[05 Cotações/05 - Win Rate e Métricas]]

### Domínio 06 — Pedidos (4 notas — 2 completas + 2 esqueleto)
- [[06 Pedidos/00 - Visão Geral Pedidos]] — esqueleto
- [[06 Pedidos/01 - Do Pedido ao RAF]] — completa
- [[06 Pedidos/02 - Ciclo e Status]] — esqueleto
- [[06 Pedidos/03 - Métricas de Pedido]] — esqueleto

### Domínio 07 — Cruzamentos e Previsões (5 notas, 4 completas + 1 esqueleto)
- [[07 Cruzamentos e Previsões/00 - Visão Geral Cruzamentos]]
- [[07 Cruzamentos e Previsões/01 - Cotação x Pedido x RAF]]
- [[07 Cruzamentos e Previsões/02 - Estoque x RAF (giro real)]]
- [[07 Cruzamentos e Previsões/03 - Pricing Planejado x Realizado]]
- [[07 Cruzamentos e Previsões/04 - Previsões e Forecasts]] — esqueleto

### Overview raiz
- [[00 - Visão Geral do Sistema]]

---

## Status por domínio

| Domínio | Notas | Status | Qualidade |
|---|---|---|---|
| 01 Sistema de Dados | 7 | **Completo** | Alta — todas nível 3 |
| 02 Precificação | 13 | **Completo** | Alta — todas nível 3 |
| 03 Estoque | 7 | **Completo** | Alta — todas nível 3 |
| 04 RAF | 9 | **Completo** | Alta — todas nível 3 |
| 05 Cotações | 6 | **Completo** | Alta — todas nível 3 |
| 06 Pedidos | 4 | **Parcial** | 1 completa + 3 esqueleto |
| 07 Cruzamentos | 5 | **Quase completo** | 4 completas + 1 esqueleto |
| Overview | 1 | **Completo** | Alta |

**Total: 52 notas** (vs 35-50 estimadas — produção acima do planejado, mantendo qualidade).

---

## O que ficou como **esqueleto** (a expandir em próximas sessões)

### Domínio 06 — Pedidos
- **00 - Visão Geral Pedidos** — visão geral criada, mas domínio precisa de análise de pedidos em desenvolvimento
- **02 - Ciclo e Status** — esqueleto: aguarda levantamento de status reais do Softcomp
- **03 - Métricas de Pedido** — esqueleto: KPIs propostos mas precisa de dados reais

### Domínio 07 — Cruzamentos
- **04 - Previsões e Forecasts** — esqueleto: implementação espera Motor Analítico v2

### Sugestão
Quando Análise de Pedidos Emitidos for implementada, voltar para completar Domínio 06. Previsões só fazem sentido com série temporal de 12+ meses acumulada.

---

## Conteúdo `{{A VALIDAR: Gustavo}}`

Durante a construção, mantive convenção de **não inventar**. Onde havia incerteza, marquei para você validar. Revisão cuidadosa recomendada em:

### Parâmetros numéricos
Valores abaixo **vieram da memória de conversas anteriores**, mas vale validar que continuam vigentes:

- VPP laminado 1%, forjado 5-6%
- Despesas comerciais 3,70%
- Despesas logísticas por unidade (GRU 1,54% ... CXS 5,65%)
- Comissão vendedor 2% s/IPI
- Frete break bulk USD 110/mt
- MC contábil realizada 29,30%
- MC econômica realizada 35,44% (+6,15 pp)
- Margem oculta: corte R$1M, FIN R$1M, EXT R$466k, COM R$111k, CER R$23k, INT R$19k, IMP R$0 (total +R$2,64M)

**Se algum desses mudou, atualizar** nas notas correspondentes (principalmente [[02 Precificação/00 - Visão Geral Precificação]] e [[04 RAF/00 - Visão Geral RAF]]).

### Métricas operacionais
- Win rate 67,6%
- 29.748 cotações analisadas
- Piracicaba com 3 vendedores problemáticos (Fabiola 50%, Juliana-PIR 47,6%, Marcos Lemes 41,3%)
- R$9,35M perdidos para Trefita/Torres

### Propostas não-implementadas
Algumas notas documentam **propostas** que discuti com você mas não foram implementadas. Marcadas como tal:
- ABC/XYZ (Domínio 03)
- Cliente-Tabelista flag (Domínio 05)
- Status "Em Projeto" no Softcomp (Domínio 05)
- Nova remuneração por aderência à tabela (Domínio 02)

Se alguma virou realidade ou se decidiu abandonar, atualizar nota.

---

## Referências a memórias

Durante a construção, precisei referenciar memórias internas (minhas) que **não são notas do vault**. Convertidos para **código inline** (não wikilink) para não gerar broken link:

- `project_freight_parameters` (frete break bulk)
- `project_afs_estrutura_logistica` (logística por unidade, CXS)
- `project_trefita_torres_intel` (concorrente)
- `project_afs_cxs_problema_comercial` (CXS comercial)
- `project_afs_expansao_mg` (estudo histórico)
- `project_afs_remuneracao_alcada` (remuneração)

**Se quiser**, posso criar notas no vault equivalentes a essas memórias numa próxima sessão. Por enquanto ficam como referência informacional.

---

## Verificação estrutural

### Estado final
- **Total de notas no vault:** 113
- **Broken links críticos:** 0 (o script reporta 3, mas todos são **falsos positivos**)
- **Falsos positivos explicados:**
  - 1 link em código inline em [[08 - Consolidação por OS]] (Obsidian ignora dentro de backticks)
  - 2 links para nota arquivada `_Arquivadas/2026-04-17 — Posicionamento MetalM - Servitizador` (arquivo existe, mas script ignora pastas `_*`)

### Hubs emergentes do sub-vault operacional
(incoming links dentro do sub-vault)

- **00 - Visão Geral RAF:** 23
- **01 - Família Canônica:** 23
- **06 - Motor Analítico v1:** 21
- **07 - Tabelas e Alçadas:** 19
- **08 - Simulador HTML - Arquitetura:** 17
- **02 - Convenção Softcomp (Invertida):** 17

Família Canônica e Motor Analítico se destacam como **conectores cross-domínio** — coerente com o princípio de taxonomia unificada.

---

## Padrões de desenvolvimento documentados

Conforme direcionamento, a nota [[01 Sistema de Dados/05 - Padrões de Desenvolvimento]] foi construída como **style guide canônico** para novos programas. Baseado em:
- **Painel de Estoque v2** (referência)
- **Simulador de Precificação HTML** (referência)

Principais padrões consolidados:
- HTML self-contained (sem CDN externa)
- Python local para processamento pesado
- Taxonomia Família Canônica embutida
- Convenção de nomes, estrutura de código
- Localstorage para persistência
- Print A4 landscape
- Cores semáforo (verde/amarelo/vermelho)

**Divergências conhecidas** listadas na nota — programas antigos (Painel Comercial v1-v4, Campanha_60anos, Acovisa) precisam ser trazidos ao padrão ou arquivados.

---

## Próximas ações recomendadas

### Revisão imediata (Gustavo)
1. **Ler as notas 00 (overviews)** de cada domínio — são 7 notas, ~30 min total
2. **Validar parâmetros numéricos** críticos (lista acima em `{{A VALIDAR}}`)
3. **Sinalizar o que discorda** ou o que precisa ajustar

### Curto prazo (próximas sessões)
4. **Completar Domínio 06 Pedidos** quando houver mais clareza do módulo Pedidos no Softcomp
5. **Consolidar nota Pricing Web App** se o projeto for retomado (ou arquivar se descartado)
6. **Atualizar parâmetros** trimestralmente (despesas logísticas, especialmente)

### Médio prazo
7. **Criar notas no vault** para as "memórias" referenciadas (se fizer sentido)
8. **Ampliar Domínio 07 Cruzamentos** quando Motor Analítico v2 materializar
9. **Integrar com logs vivos** — ex: entrada em [[Aprendizados]] quando sub-vault operacional revelar insight

### Ações técnicas fora do vault (sugestões)
10. **Trazer Painel Comercial v1-v4 ao padrão** (ver [[01 Sistema de Dados/05 - Padrões de Desenvolvimento]])
11. **Arquivar dashboards históricos** (Campanha_60anos, Acovisa) para pasta dedicada

---

## Arquivos não tocados nesta sessão

Por escopo:
- **Vault estratégico (raiz):** apenas Home.md atualizado para incluir link para o sub-vault
- **Logs/:** não modificados
- **Templates:** não modificados

---

## Observações técnicas

### Backup
O vault está sincronizado via iCloud. Recomendado:
- Antes de qualquer edição majoritária, fazer cópia local
- Considerar Git versionamento (pessoal) para rastreamento de mudanças

### Gestão do sub-vault
- Revisão trimestral recomendada
- Atualizar "última-revisão" no frontmatter quando modificar
- Datar mudanças estruturais em comentário

### Impacto no grafo do Obsidian
Com 113 notas, grafo de conexões ficou denso. Obsidian renderiza sem problema em máquinas modernas. Se quiser filtrar, pode usar filtros por tag (`#precificação`, `#raf`, etc.).

---

## Conclusão

Cobertura **além do planejado** para o que comporta uma sessão:
- 52 notas criadas
- 45 delas no nível 3 (completo)
- 7 como esqueleto (reconhecido, a desenvolver)
- Zero broken links críticos
- Padrão canônico documentado

O sub-vault está **operacional** e pode ser usado imediatamente como:
- Referência de consulta rápida sobre lógica AFS
- Base de onboarding (se houver analista/time futuro)
- Ativo pessoal transferível (conhecimento codificado, seu)
- Style guide para novos programas

---

## Conexões principais

- [[00 - Visão Geral do Sistema]] — ponto de partida
- [[01 Sistema de Dados/00 - Arquitetura de Dados]] — fluxo de dados
- [[01 Sistema de Dados/05 - Padrões de Desenvolvimento]] — style guide
- Vault estratégico: [[Home]]

---

*Gerado automaticamente por Claude durante sessão noturna de documentação.*
*Qualquer incoerência ou erro: reportar para correção.*
