---
tipo: overview
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [precificação, pricing, overview, simulador]
---

# 00 — Visão Geral Precificação

## Propósito do domínio

Documenta a **lógica completa de precificação** da Sacchelli: fórmulas, componentes, normas técnicas, modos de venda, alçadas, ferramentas. É o domínio mais denso do sub-vault porque pricing é o **coração da inteligência comercial**.

---

## Princípio central

**Preço certo é aquele que:**
1. Cobre o custo real (aço + processo + despesas)
2. Recupera a margem alvo sobre o aço
3. Cobra explicitamente os serviços adicionais (ou preserva margem oculta deles)
4. Considera o custo de servir do cliente específico
5. Respeita alçada (Verde/Amarela/Vermelha)
6. Tem contrapartida para qualquer desconto (Give/Get)

Preço **errado** é qualquer um que falha em pelo menos um desses pontos.

---

## Mapa conceitual

```
                    CUSTO                    MARGEM
                      │                        │
                      ▼                        ▼
           ┌──────────────────┐      ┌────────────────┐
           │ Aço              │      │ MC sobre aço   │
           │ Processo (corte) │      │ (alvo)         │
           │ Serviços externos│      └────────┬───────┘
           │ Impostos         │               │
           │ Comissão         │               │
           │ Frete            │               │
           │ Despesas fixas   │               │
           └──────────┬───────┘               │
                      │                        │
                      └──────────┬─────────────┘
                                 │
                                 ▼
                        ┌────────────────┐
                        │ PREÇO DE VENDA │
                        │   (R$/kg,      │
                        │   R$/pç,       │
                        │   R$/m)        │
                        └────────┬───────┘
                                 │
                                 ▼
                  ┌──────────────────────────┐
                  │ Comparar com tabelas:    │
                  │  A (verde) B (amarela)   │
                  │  C (vermelha)            │
                  └──────────┬───────────────┘
                             │
                             ▼
                  ┌──────────────────────────┐
                  │ Dentro → vendedor ok     │
                  │ Fora (abaixo C) → diretor│
                  └──────────────────────────┘
```

---

## Notas neste domínio

| # | Nota | Descrição |
|---|---|---|
| 00 | [[00 - Visão Geral Precificação]] | Este mapa |
| 01 | [[01 - Fórmula do Lucro]] | Lucro = Receita − Descontos − Custo − Custo de Servir |
| 02 | [[02 - Fórmula de Preço Sacchelli]] | Equação completa de formação de preço |
| 03 | [[03 - Componentes de Custo]] | Detalhamento de cada item (aço, corte, etc.) |
| 04 | [[04 - MC1 MC2 e DRE]] | Estrutura da margem de contribuição e DRE |
| 05 | [[05 - Modos de Venda]] | R$/Kg, R$/Pç, R$/m — regras por modo |
| 06 | [[06 - VPP Tolerância e Lâmina]] | Variação de peso, tolerância de medida |
| 07 | [[07 - Tabelas e Alçadas]] | Verde, Amarela, Vermelha + sistema de aprovação |
| 08 | [[08 - Simulador HTML - Arquitetura]] | Referência canônica |
| 09 | [[09 - Simulador Web App (futuro)]] | PRD concluído, pausado |
| 10 | [[10 - Custo de Servir Aplicado]] | Como entra no pricing |
| 11 | [[11 - Normas Técnicas]] | EN 10060, Metals, referências |
| 12 | [[12 - Modo Pacote Multi-Item]] | DRE blended, compartilhamento de campos |

---

## Conexões estratégicas

Este domínio alimenta (e é alimentado por) notas do vault estratégico:

- **Conceito estratégico:** [[Pricing - Precificação]] (vault raiz)
- **Conceito estratégico:** [[Custo de Servir]] (vault raiz)
- **Conceito estratégico:** [[Proposta de Valor]] (vault raiz)

Aqui é **mecânica**. Lá é **estratégia**. Quando decisão de preço sobe ao nível estratégico (ex: revisar tabela por mudança de posicionamento), criar entrada em [[Decisões C-Level]].

---

## Ordem de leitura recomendada

**Para entender pricing do zero:**
01 → 02 → 03 → 04 → 05 → 06 → 07 → 10

**Para usar o simulador:**
08 → 05 → 06 → 07

**Para desenvolver ferramenta nova de pricing:**
[[05 - Padrões de Desenvolvimento]] + 08 + 02

---

## Números de referência (abr/2026)

| Parâmetro | Valor | Fonte |
|---|---|---|
| VPP laminado | 1% | [[06 - VPP Tolerância e Lâmina]] |
| VPP forjado | 5-6% | [[06 - VPP Tolerância e Lâmina]] |
| Despesas comerciais (fixo) | 3,70% | [[03 - Componentes de Custo]] |
| Despesas logísticas GRU | 1,54% | [[03 - Componentes de Custo]] |
| Despesas logísticas PIR | 1,64% | [[03 - Componentes de Custo]] |
| Despesas logísticas SCA | 3,24% | [[03 - Componentes de Custo]] |
| Despesas logísticas RIP | 2,76% | [[03 - Componentes de Custo]] |
| Despesas logísticas CXS | 5,65% | [[03 - Componentes de Custo]] |
| Comissão vendedor (s/IPI) | 2% | [[07 - Tabelas e Alçadas]] |
| MC contábil realizada | 29,30% | RAF jan-abr/2026 |
| MC econômica realizada | 35,44% (+6,15 pp) | RAF jan-abr/2026 |
| Frete China→SFS (break bulk) | USD 110/mt | `project_freight_parameters` |

---

## Riscos e atenções

### Remuneração desalinhada com pricing
Vendedor ganha sobre **fat s/IPI**, não sobre MC. Incentivo é para volume, não para margem. Ver [[07 - Tabelas e Alçadas]] e discussão estratégica em [[Pricing - Precificação]].

### Zona cega Verde → Vermelha
Vendedor age sozinho nessa faixa. Diretor não vê. Oportunidade de vazamento de margem. Relatório de frequência por vendedor resolveria parcialmente (alavanca sem mexer em remuneração).

### Custo de servir não entra no pricing operacional
O simulador hoje não calcula custo de servir por cliente. Isso significa que pricing é feito "em tese" sem considerar o esforço específico de atender aquele cliente. Oportunidade crítica de melhoria.

### Tabela vencida
Se custos de aço sobem (ex: CFR China +35% em 5 semanas) mas tabelas não são atualizadas, piso Vermelho vira prejuízo silencioso. Revisão de tabela deve ser **no mínimo mensal**.
