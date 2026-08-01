---
tipo: projeto-futuro
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [simulador, web-app, prd, nodejs, react, futuro]
---

# 09 — Simulador Web App (futuro)

## Status

**Projeto em pausa.** PRD concluído, implementação ainda não iniciada.

**Documento fonte:** `PRD_Simulador_Precificacao_Web.docx` (15 capítulos, 22 tabelas)
**Arquivo:** disponível na pasta raiz do projeto
**Orientação Claude Code:** CLAUDE.md, estrutura de pastas e sequência de prompts por fase já preparados

---

## Propósito

Migrar o **Simulador HTML atual** para aplicação web **multi-usuário**, protegendo inteligência comercial e permitindo acesso controlado.

---

## Motivação

### Limitações do HTML atual
1. **Inteligência comercial exposta** — fórmulas e custos estão legíveis no source do HTML
2. **Uso individual** — cada usuário com seu próprio arquivo desincronizado
3. **Sem sincronização com Softcomp** — dados manuais, desatualizados
4. **Sem auditoria** — quem simulou o quê, quando
5. **Sem histórico centralizado** — orçamentos ficam em localStorage local

### Ganhos esperados do Web App
1. **Motor de cálculo no servidor** (JS minificado + não exposto ao cliente)
2. **Multi-usuário (5 users)** com autenticação
3. **Sync automático** de dados do Softcomp (cron 6h)
4. **Histórico centralizado** em banco
5. **Auditoria** (quem simulou, quando, resultado)
6. **Controle de versão** de tabelas e parâmetros

---

## Arquitetura definida no PRD

### Stack técnico
| Camada | Tecnologia |
|---|---|
| Backend | Node.js 20 + Express |
| Frontend | React 18 + Vite + Tailwind |
| Banco | SQLite (better-sqlite3) |
| Auth | JWT + bcrypt |
| Deploy | VM Sacchelli + Nginx + HTTPS |
| Sync | SQL espelho Softcomp → SQLite (cron 6h) |

### Motor de cálculo (9 módulos JS)
1. **pricing-engine** — orquestrador principal
2. **cost** — custo aço e subcomponentes
3. **cut** — cálculos de corte e lâmina
4. **process** — TT, ensaios, certificações
5. **vpp** — aplicação de VPP por modo
6. **spread** — spread financeiro
7. **tax** — ICMS, PIS/COFINS
8. **dre-builder** — montagem da DRE
9. **kpi-builder** — indicadores e corredor de MC

### Usuários (5)
Pré-definidos:
- Gustavo (admin)
- 2-3 gerentes (leitura + simulação)
- 1-2 vendedores sênior (simulação, sem setup)

### Auth
- Login com email + senha (bcrypt)
- JWT com expiração 8h
- Refresh token para sessão longa

---

## Estrutura de dados (banco SQLite)

```
tables:
  users
    id, email, nome, password_hash, role, created_at

  sessions
    id, user_id, token, expires_at, created_at

  simulacoes
    id, user_id, cliente, item_nome, input_json, output_json,
    modo_venda, mc1, mc2, preco_final, created_at

  pacotes
    id, user_id, cliente, nome, itens_json, created_at

  parametros_setup
    chave, valor, atualizado_em, atualizado_por
    (ex: vpp_laminado, vpp_forjado, desp_logistica_gru, ...)

  tabelas_preco  (espelho do Softcomp)
    produto, tabela_a, tabela_b, tabela_c, data_vigencia

  custos_aco  (espelho do Softcomp)
    aco, acabamento, bitola, custo_ton, data_atualizacao

  auditoria
    id, user_id, acao, entidade, entidade_id, diff_json, created_at
```

---

## Roadmap 4 fases

### Fase 1 — Extração do motor de cálculo
**Objetivo:** tirar o JS do HTML e transformar em módulos isolados.

**Tarefas:**
- Extrair funções de cálculo do HTML atual
- Quebrar em 9 módulos JS (pricing-engine + 8 auxiliares)
- Criar suite de testes comparativos (HTML atual × módulos)
- Validar que 50 cotações geram mesma DRE nos dois

**Entregável:** `/motor/*.js` + testes

### Fase 2 — Backend mínimo + sync
**Objetivo:** servidor rodando, dados do Softcomp sincronizados.

**Tarefas:**
- Estrutura Express + rotas básicas
- Auth JWT
- SQLite com tabelas
- Script de sync Softcomp → SQLite (cron 6h)
- Endpoints: `/login`, `/tabelas`, `/custos`, `/simular`

**Entregável:** API funcional + sync automático

### Fase 3 — Frontend React
**Objetivo:** UI equivalente ao HTML atual, consumindo API.

**Tarefas:**
- Setup React + Vite + Tailwind
- Componentes: form de input, DRE, comparativos
- Estado com Zustand ou similar
- Auth flow
- Modo multi-item (pacote)

**Entregável:** app rodando em browser, login, simulação funcionando

### Fase 4 — Testes, deploy, onboarding
**Objetivo:** sistema em produção, usuários usando.

**Tarefas:**
- Testes E2E (Playwright)
- Deploy em VM AFS com Nginx + HTTPS (Let's Encrypt)
- Documentação de uso
- Treinamento dos 5 usuários
- Monitoramento (logs, erros)

**Entregável:** sistema em produção

---

## Razão da pausa (abr/2026)

### Prioridade estratégica maior
- **Processo Duferco-Brasil** em andamento (ver vault estratégico)
- Tempo e atenção do Gustavo direcionados para decisão de carreira
- Implementação do Web App demanda 200-300 horas técnicas — investimento grande

### Custo/benefício
- HTML atual **atende a necessidade atual** (uso individual Gustavo)
- Web App é para **time + proteção**, não para Gustavo sozinho
- Se Cenário F se materializar (transição para MetalM), Web App pode virar **projeto MetalM** em vez de AFS

### Cenários possíveis de retomada
1. **Retomar em AFS** se Wagner aprovar e houver necessidade de time usando simulador
2. **Retomar em MetalM** como ferramenta nova (decisão Cenário F avança)
3. **Descartar** e manter HTML se uso individual continua suficiente

---

## Segurança

### Proteção da inteligência comercial
- Motor de cálculo **no servidor** (não baixa pro cliente)
- Custos e fórmulas nunca chegam ao navegador
- Cliente só vê **input e output**

### Dados sensíveis
- Banco SQLite **criptografado em repouso**
- Conexão HTTPS obrigatória
- Backup diário automatizado (cifrado)
- Auditoria de tudo (quem acessou o quê)

### Conformidade
- LGPD: dados de cliente são identificáveis — políticas claras de acesso
- Termo de confidencialidade para usuários (gerentes, vendedores)

---

## Conexões

- [[08 - Simulador HTML - Arquitetura]] (versão atual)
- [[Sistema Operacional Comercial/01 Sistema de Dados/03 - Ferramentas Analíticas - Inventário]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/05 - Padrões de Desenvolvimento]]
- Vault estratégico: [[2026-04-17 — Estrutura Duferco-Brasil]] (decisões que afetam este projeto)

## Arquivo fonte
- `PRD_Simulador_Precificacao_Web.docx` (pasta raiz do projeto)
