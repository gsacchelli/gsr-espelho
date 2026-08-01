---
tipo: ferramenta-arquitetura
domínio: sistema-de-dados
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [motor-analitico, python, dashboard, rafia, analytics]
---

# 06 — Motor Analítico v1

## O que é

Motor Python local que **ingere exports do Softcomp** (RAF, cotações, estoque) e **gera dashboard HTML semanal** com análises comerciais recorrentes.

Substitui análises ad-hoc em Excel por **processo repetível** com saída padronizada.

**Status (abr/2026):** arquitetura aprovada (`Motor_Analitico_v1_Arquitetura.md` existe); implementação em codificação. 14+ visões já prototipadas incluindo MC% real, corredor de MC.

**Documento de arquitetura:** `Motor_Analitico_v1_Arquitetura.md` na pasta raiz do projeto.

---

## Por que existe

### Problema que resolve
- Análises ad-hoc em Excel consumiam horas, não repetíveis
- Números críticos (custo de servir, margem econômica, corredor) ficavam em planilhas esquecidas
- Falta de processo para **consumir dados novos todo ciclo**

### Proposta de valor
- Drop arquivos em pasta → rodar script → dashboard pronto
- Mesma análise, mesmo formato, toda semana
- Série temporal começa a se formar automaticamente

---

## Arquitetura

```
INPUT (pasta `input/`)
├── DetalhesRAF_YYYYMMDD.xlsx
├── Cot_Encerradas_YYYYMMDD.xlsx
├── Estoque_YYYYMMDD.xlsx (futuro)
└── Critérios_planilhas.xlsx
         │
         ▼
MOTOR (Python)
├── motor/ingestao_*.py      ← carrega e limpa
├── motor/analitica_*.py     ← processa e agrega
├── motor/consolidacao.py    ← consolidação por OS
├── motor/familia.py         ← taxonomia
└── motor/render.py          ← gera HTML com Jinja2
         │
         ▼
OUTPUT (pasta `output/`)
├── dashboard_YYYY-MM-DD.html
└── (opcional: exports Excel derivados)
```

### Stack
- **Python 3.10+**
- **pandas + numpy** — data
- **openpyxl** — Excel
- **PyYAML** — config
- **Jinja2** — templates HTML

### Filosofia
- **Local-only:** dados nunca saem da máquina
- **Idempotente:** rodar duas vezes gera o mesmo resultado
- **Extensível:** adicionar nova análise = nova função em `analitica_*.py` + novo bloco no template

---

## Regras de negócio já validadas no motor

### 1. Convenção invertida ABCCUS_X
Implementado corretamente em `motor/ingestao_raf.py::load_raf()`:
```
ABCCUS_X         → valor_cobrado_X
ABCCUS_X_COB     → custo_real_X
margem_oculta_X  = valor_cobrado_X - custo_real_X
```

### 2. Consolidação por OS
`motor/consolidacao.py::consolidar_os()` — agrega linhas com mesmo `ABCOII_NUM + ABCOII_ITE`, soma valores, calcula médias ponderadas.

### 3. Família canônica
`motor/familia.py::get_familia(aco, acab, bitola)` — aplica as 207 combinações canônicas. Fora do padrão vira "Fora de Padrão" com flag.

### 4. Cidades override
`motor/cidade.py::normalizar_cidade(raw)` — lê `config/cidades_overrides.yaml` + `cidades_sp.xlsx`. Consolida truncamentos.

### 5. Grupos de concorrentes
Trefita + Torres agregados. GGD (Gerdau usina) separado de outros.

### 6. Exclusão de "Clientes em Desenvolvimento"
Filtros default removem essa carteira quando análise é por vendedor.

---

## Visões implementadas / planejadas

### Dashboard DRE
- MC% contábil (tradicional)
- MC% econômica (com margem oculta)
- Uplift por componente (corte, financeiro, TT, certif, interno, comissão)

### Dashboard Carteira
- Top clientes por ValorMC
- Top clientes por margem oculta absorvida
- Clientes com margem líquida real negativa (renegociar ou descontinuar)
- Share of Wallet estimado

### Dashboard Pipeline
- Win rate por gerente, região, faixa de valor
- Perdas por motivo, com/sem concorrente
- Cotações tabelistas suspeitas (flag automática)
- Pipeline de projeto escondido em "orçamento prévio"

### Dashboard Unidade
- Margem por unidade (GRU, SCA, PIR, RIP, CXJ)
- Custo logístico real vs fixo do sistema
- Handicap CXS (3 pernas logísticas)

### Dashboard Produto
- Giro por família canônica
- Fora de Padrão (higiene de portfólio)
- Margem por aço, acabamento, bitola

### Dashboard Corredor de MC
- Faixa de MC praticada por cada vendedor/família/cliente
- Outliers (MC muito abaixo ou acima da média)
- Evolução temporal do corredor

---

## Integração com outras ferramentas

### Motor ↔ Simulador de Precificação
**Futuro:** motor pode **calibrar parâmetros** do simulador com dados reais (custo de servir efetivo, spread financeiro real, etc.).

**Hoje:** simulador HTML lê tabelas fixas e inputs manuais. Motor usa os mesmos inputs mas comparando com realizado.

### Motor ↔ Painel de Estoque
Motor pode consumir output do Painel (ou os mesmos brutos) para cruzar giro × receita.

### Motor ↔ Vault (este sub-vault)
Motor gera insights → entradas em [[Aprendizados]] ou [[Hipóteses de Negócio]] no vault estratégico.

---

## Processo semanal (rotina)

> Alvo quando motor estiver operacional. Hoje ainda manual.

**Segunda-feira manhã (15-30 min):**
1. Extrair DetalhesRAF.xlsx atualizado do Softcomp → pasta `input/`
2. Extrair Cot_Encerradas.xlsx → pasta `input/`
3. `cd MotorAnalitico && python main.py`
4. Abrir `output/dashboard_YYYY-MM-DD.html`

**Durante a semana:**
5. Revisar dashboard, anotar 3-5 insights
6. Insights relevantes viram entrada em [[Aprendizados]]
7. Anomalias viram hipóteses em [[Hipóteses de Negócio]]

**Sexta-feira:**
8. Quick review: KPIs semanais bateu?
9. Ajuste de rumo se necessário

---

## Roadmap / pendências

### v1 (em codificação)
- [x] Arquitetura aprovada (doc)
- [x] Ingestão RAF com convenção correta
- [x] Consolidação por OS
- [x] Família canônica
- [x] Cidades override
- [ ] Template HTML dashboard
- [ ] 14 visões principais
- [ ] Script `main.py` completo
- [ ] Testes de regressão
- [ ] Documentação de uso

### v2 (futuro)
- Conexão direta SQL Server (via VPN)
- Série temporal acumulada (histórico de dashboards)
- Alertas automáticos (ex: MC abaixo de threshold)
- Integração com simulador (calibração de parâmetros)
- Integração com pipeline de projeto (tracking ANDRITZ, PROK)

---

## Restrições conhecidas

### 1. Consumo solo
V1 é uso exclusivo do Gustavo. Não compartilhado com time. Motivo: simplicidade + confidencialidade.

### 2. Sem histórico legado no início
Série temporal começa quando motor entra em produção. Pode-se reprocessar RAFs antigos, mas análises cruzadas históricas não existem.

### 3. Não substitui Softcomp
Motor não emite pedido, não fatura, não altera dados operacionais. É **read-only** em relação à realidade — gera análise, não transação.

### 4. Dependência de exports manuais
V1 depende de Gustavo exportar do Softcomp. Sem VPN + script automatizado, processo semanal é manual (30 min/semana).

---

## Riscos e mitigações

### Risco — Motor cria narrativa que não reflete realidade
Se regras de negócio estão mal implementadas (ex: convenção ABCCUS invertida), dashboard fica bonito mas errado.
**Mitigação:** validação cruzada com Softcomp + revisão de 10 casos conhecidos a cada alteração de regra.

### Risco — Gustavo sai da AFS sem conseguir levar motor
Motor roda em máquina da AFS ou pessoal?
**Mitigação:** motor deve rodar em máquina pessoal do Gustavo (já é essa a arquitetura). Código versionado em Git local pessoal. Acompanha saída.

### Risco — Motor vira fantasia de "tudo automatizado" sem revisão
Dashboard automático que ninguém lê é pior que não ter dashboard.
**Mitigação:** revisão semanal obrigatória (15 min sexta-feira). Se 2 semanas sem revisão, pausar processo.

---

## Conexões

- [[00 - Arquitetura de Dados]]
- [[03 - Ferramentas Analíticas - Inventário]]
- [[05 - Padrões de Desenvolvimento]]
- [[Sistema Operacional Comercial/04 RAF/00 - Visão Geral RAF]]
- [[Sistema Operacional Comercial/05 Cotações/00 - Visão Geral Cotações]]
- [[Sistema Operacional Comercial/07 Cruzamentos e Previsões/00 - Visão Geral Cruzamentos]]

## Arquivo de arquitetura
- `Motor_Analitico_v1_Arquitetura.md` (pasta raiz do projeto)
