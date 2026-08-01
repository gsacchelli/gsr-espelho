---
tipo: padrão
domínio: sistema-de-dados
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [arquivos, convenções, padrão, dados]
---

# 02 — Arquivos Brutos e Convenções

## Princípio

Arquivos brutos são **snapshots temporais do Softcomp**. Cada export representa a verdade do ERP no momento da extração. Para rastreabilidade:
- Nome do arquivo carrega **tipo + data**
- Original **nunca é sobrescrito**
- Derivados (limpo, consolidado) ficam em pasta separada

---

## Nomenclatura canônica

### Padrão geral
`<TIPO>_<YYYYMMDD>.<ext>`

Exemplos:
- `DetalhesRAF_20260415.xlsx`
- `Cot_Encerradas_20260228.xlsx`
- `Estoque_20260412.xlsx`
- `tabela_preco_20260210.xlsx`

### Data no nome: qual data?
**Data do snapshot no Softcomp**, não a data de criação do arquivo.
- Se export é feito hoje mas com filtro "faturamento até 31/mar", data = 20260331
- Dúvida em casos ambíguos: data de criação do arquivo (com comentário na pasta)

### Versões com sufixo
Para revisões dentro do mesmo dia ou snapshots especiais:
- `DetalhesRAF_20260415_v2.xlsx` (segunda extração)
- `DetalhesRAF_20260415_abril.xlsx` (filtro específico)

---

## Estrutura de pastas

### Hoje (abr/2026)
```
~/Documents/Personal/00. Projetos - Claude/Planejamento Estratégico - Comercial/
├── DetalhesRAF*.xlsx              ← brutos RAF na raiz (mover)
├── Estoque_Sacchelli*.html        ← painéis gerados
├── Analise_Precificacao*.html     ← simuladores
├── MotorAnalitico/                ← projeto motor Python
├── MetalM/                        ← projeto MetalM separado
├── Arquivo/                       ← histórico
└── (outros)
```

### Estrutura recomendada (padrão proposto)
```
~/Documents/Personal/00. Projetos - Claude/Planejamento Estratégico - Comercial/
├── 01_Brutos/
│   ├── RAF/
│   │   ├── DetalhesRAF_20260115.xlsx
│   │   ├── DetalhesRAF_20260215.xlsx
│   │   └── DetalhesRAF_20260315.xlsx
│   ├── Cotacoes/
│   │   └── Cot_Encerradas_YYYYMMDD.xlsx
│   ├── Estoque/
│   │   └── Estoque_YYYYMMDD.xlsx
│   ├── Tabelas/
│   │   └── tabela_preco_YYYYMMDD.xlsx
│   └── Criterios/
│       ├── Critérios_planilhas_YYYYMMDD.xlsx
│       └── cidades_sp.xlsx
│
├── 02_Derivados/
│   ├── RAF_limpo_YYYYMMDD.xlsx    ← pós-consolidação por OS
│   └── cruzamentos_YYYYMMDD.xlsx
│
├── 03_Ferramentas/
│   ├── Analise_Precificacao_Sacchelli.html
│   ├── Estoque_Sacchelli.html
│   └── Motor/ (python)
│
├── 04_Saidas/
│   ├── Dashboards_YYYYMMDD.html
│   └── Relatórios_YYYYMMDD.pdf
│
├── 05_Arquivo/                    ← legados, backups, antigos
│
└── Vault_GSR/                     ← documentação (este sub-vault)
```

**Nota:** reorganizar para esse padrão pode ser trabalho de 30-60 min. Vale priorizar quando houver tempo ocioso.

---

## Convenções de export do Softcomp

### RAF (DetalhesRAF.xlsx)
**Filtros recomendados no export:**
- Período: mês fechado ou acumulado do ano
- Unidade: todas (análises consolidadas)
- Status: faturado (exclui cancelado)
- Incluir colunas de custo COB e real (133 colunas — ver [[04 RAF/01 - Estrutura das 133 Colunas]])

### Cotações (Cot_Encerradas.xlsx)
**Filtros recomendados:**
- Período: últimos 12 meses rolantes (para análises de tendência)
- Apenas encerradas (não abertas) — abertas viram outro export
- Incluir motivo de encerramento + concorrente nomeado

### Estoque
**Filtros recomendados:**
- Snapshot de todas as unidades
- Incluir SKU, família, peso, custo, valor, dias parado

---

## Versionamento e retenção

### Regra 1 — Nunca sobrescrever bruto
O arquivo original extraído do Softcomp é **imutável**. Se precisar re-exportar, novo nome com data atualizada.

### Regra 2 — Retenção mínima
| Tipo | Retenção mínima |
|---|---|
| RAF | Todos os meses do ano corrente + 24 meses anteriores |
| Cotações encerradas | 24 meses rolantes |
| Tabelas de preço | Todas as versões que serviram de base para análises |
| Estoque | Fim de mês dos últimos 12 meses |
| Critérios | Todas as versões (são pequenas) |

### Regra 3 — Backup
Pasta `Planejamento Estratégico - Comercial` está em iCloud Drive — **sincronização automática**. Aceitável como backup para uso pessoal. **Não aceitável** como backup único para material crítico (ex: logs de decisão vault GSR). Ver política de backup em cada contexto.

---

## Nomenclatura interna dos dados

### Convenção Softcomp (colunas)
**Padrão:** `ABCXXX_YYY[_SUFIXO]`

- Prefixo `ABC` = módulo de faturamento/DRE
- Sufixo `_COB` **significa CUSTO REAL** (invertido! — ver [[04 RAF/02 - Convenção Softcomp (Invertida)]])
- Sufixo `_MIN_X` = piso de tabela (A/B/C)
- `_KG`, `_PC`, `_M` = unidade de medida

**Atenção máxima à inversão do `_COB`.** Custou uma análise inteira de pricing errada em jan/2026 por essa armadilha.

### Convenção de família
Padrão proposto (ver [[03 Estoque/01 - Família Canônica]]):
`<Aço>_<Tipo>_<Perfil>_<Acabamento>_<S/N da faixa de bitola>`

Exemplo: `1045_Carbono_Redondo_Trefilado_1` (1020 1045 carbono, redondo, trefilado, faixa 12.7-101.6mm)

---

## Atualização do dado

### Frequência ideal por dado
| Dado | Frequência | Razão |
|---|---|---|
| RAF | Semanal | Base de margem real — ciclo de decisão curto |
| Cotações | Semanal | Funil dinâmico |
| Estoque | Semanal | Giro + disponibilidade para venda |
| Tabelas de preço | Mensal | Não muda diário |
| Critérios (taxonomia) | Sob demanda | Só quando surgir nova família/faixa |

### Frequência atual (abr/2026)
Mensal na maioria dos casos. **Gap:** semanal seria melhor mas depende de ter o processo automatizado (Motor Analítico em construção).

---

## Qualidade do dado no momento do export

### Antes de usar um export
Checagens rápidas:
1. **Número de linhas** bate com expectativa? (ex: RAF tem ~5.000 linhas/mês)
2. **Período filtrado** está correto?
3. **Sem células vazias em colunas-chave** (cliente, produto, valor)?
4. **Cidades já saem truncadas** — aplicar override antes de agrupar
5. **Consolidação por OS** necessária? (múltiplas linhas mesmo item — ver [[04 RAF/08 - Consolidação por OS]])

Se falhar em qualquer item, **não avançar a análise sem resolver**.

---

## Conexões

- [[00 - Arquitetura de Dados]]
- [[01 - ERP Softcomp - Detalhes]]
- [[04 - Qualidade de Dados]]
- [[05 - Padrões de Desenvolvimento]]

## Padrão recomendado para novos programas

Ao criar ferramenta nova (dashboard, análise), **sempre** aceitar input em:
1. Arquivo bruto com nome `<TIPO>_<YYYYMMDD>.xlsx` na pasta esperada
2. Checar se data do arquivo bate com período de análise solicitado
3. Em caso de múltiplos brutos, usar o mais recente por default (com opção de override)
4. Log de qual bruto foi carregado deve aparecer no output (UI ou console)

Isso vale para: Motor Analítico, futuros painéis, scripts Python pessoais.
