---
tipo: referência-operacional
domínio: cotações
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [motivos, encerramento, perdas, pipeline]
---

# 02 — Motivos de Encerramento

## Lista oficial (Softcomp)

Classificação feita pelo vendedor no **pós-fechamento** da cotação:

| Motivo | Descrição | Ação analítica |
|---|---|---|
| **Ganhou** | Cotação virou pedido | Medir: ciclo, margem, cliente |
| **Cotação somente para orçamento prévio** | Cliente não tinha intenção real | **Caixa-preta** — desagregar |
| **Perdeu por Preço** | Cliente fechou com concorrente por preço | Analisar: concorrente nomeado? |
| **Perdeu por Prazo** | Perdeu por prazo de entrega | Revisar estoque/produção |
| **Perdeu por Qualidade / Técnico** | Especificação ou qualidade insuficiente | Investigar caso a caso |
| **Projeto Cancelado** | Cliente desistiu do projeto | Info, não ação |
| **Outros** | Diversos | Caixa preta — detalhar se recorrente |

---

## Distribuição típica (mar/2026)

Baseado em 29.748 cotações Jan-Fev/2026:

| Motivo | ~% do total |
|---|---|
| Ganhou | ~30-40% |
| Orçamento prévio | ~50-55% |
| Perdeu por preço | ~10-15% |
| Perdeu por prazo | 2-3% |
| Perdeu por qualidade | <1% |
| Projeto cancelado | 2-5% |
| Outros | <1% |

**Win rate ajustado** (excluindo orçamento prévio do denominador): **67,6%**.

Ou seja: quando excluímos cotações que nunca foram para fechar, conversão é alta. O problema analítico é **distinguir quais orçamentos prévios eram reais** (ver [[03 - Orçamento Prévio vs Projeto Real]]).

---

## Perda por preço — decomposição

### Análise 29.748 cotações
- **21% perdidas "por preço"**
- **53% sem concorrente nomeado** — vendedor marcou "preço" sem saber o concorrente

### Decomposição
| Subgrupo | % da perda por preço |
|---|---|
| Concorrente nomeado (ex: Trefita/Torres, Gerdau) | ~47% |
| Sem concorrente nomeado | ~53% |

### Significado
- **Com concorrente nomeado:** perda real por preço vs X. Analisar gap.
- **Sem concorrente nomeado:** provavelmente **não é preço**. Vendedor marcou "preço" porque é o motivo mais fácil de explicar internamente. Pode ser:
  - Cliente não respondeu (desistência disfarçada)
  - Outro critério (prazo, relacionamento, qualidade)
  - Cliente escolheu Gerdau direto (não vê como "concorrente" tradicional)

### Ação
Criar **obrigatoriedade** de nome do concorrente quando motivo = "preço". Se vendedor não sabe, marcar outro motivo.

---

## Concorrentes principais (quando nomeados)

### Trefita/Torres (grupo único)
- **#1 concorrente** — R$9,35M perdidos em Jan-Fev/2026
- Torres = forjado (parte do mesmo grupo)
- **Arbitragem fiscal MG/ES** via unidade Contagem-MG (gap ~4-8% vs AFS)
- Ver `project_trefita_torres_intel`

### Gerdau / GGD
- Gerdau usina — bucket separado (é **fornecedor**, não só concorrente)
- Alguns clientes grandes foram perdidos para Gerdau indo direto

### Outros
- Outros distribuidores regionais
- Importadores diretos (cliente importa ele mesmo)

---

## Diagnóstico regional (mar/2026)

### Piracicaba — região problema
3 vendedores com >40% de taxa de perda por preço:
- Fabiola: 50%
- Juliana-PIR: 47,6%
- Marcos Lemes: 41,3%

### Top performers (mesma tabela, mesmos produtos)
- Alam: 94,1%
- Aline-CXJ: 92,5%
- Açotec-SCA: 91,4%

### Leitura
"Problema de preço" em PIR é **problema de processo comercial**, não de tabela (tabela é igual em SP inteiro). Três vendedores específicos concentram perdas.

**Alavanca:** treinamento comercial + ajuste de abordagem, não desconto.

---

## Perdidas por preço — análise de gap

### Observação (mar/2026)
- Ganhas: média **+3,0%** sobre Tab Vermelha
- Perdidas por preço: média **+1,1%** sobre Tab Vermelha
- Diferença: **~2 p.p.**

### Interpretação
**Não é um abismo de preço.** Muitas "perdas por preço" provavelmente seriam fechadas com ajuste mínimo — ou não são preço mesmo.

**Implicação:** dar 3-5% de desconto "para ganhar" perdidas por preço **não é a solução**. É processo comercial.

---

## Custo estrutural vs Gerdau-supplied

Análise 29.748 cotações identificou:
- **Sacchelli tem vantagem estrutural de custo** vs concorrentes supridos por Gerdau
- **28% menor** em aços carbono

Significa: onde AFS perde para Gerdau-supplied, geralmente não é por preço de custo — é execução comercial ou logística.

---

## Ações recomendadas (baseadas em análise)

### Curto prazo
1. **Obrigatoriedade de concorrente nomeado** em perdas por preço
2. **Conversa cirúrgica** com 3 vendedores de PIR (Fabiola, Juliana, Marcos)
3. **Revisão mensal** dos motivos (evitar drift)

### Médio prazo
1. **Defesa Trefita/Torres** focada — 14 clientes perdidos em CXS (pode ser logística, não preço)
2. **Análise por vendedor** do mix de motivos
3. **Flag de cliente-tabelista** automatizada

### Longo prazo
1. **Mudança do processo de encerramento** no Softcomp (status "Em Projeto" — ver [[03 - Orçamento Prévio vs Projeto Real]])
2. **Dashboard de motivos** no Motor Analítico v2

---

## Conexões

- [[00 - Visão Geral Cotações]]
- [[01 - Inbound vs Outbound (ficção do ERP)]]
- [[03 - Orçamento Prévio vs Projeto Real]]
- [[05 - Win Rate e Métricas]]
- [[02 Precificação/07 - Tabelas e Alçadas]]
- [[04 RAF/06 - Despesas Logísticas por Unidade]] (CXS + Trefita)
- `project_trefita_torres_intel` (memória)
