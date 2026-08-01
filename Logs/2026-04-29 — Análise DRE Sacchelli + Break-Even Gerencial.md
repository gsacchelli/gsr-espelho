---
data: 2026-04-29
tipo: análise financeira + decisão metodológica
projeto: Painel Comercial RAF — Pacote 1 (Matriz BCG) + threshold MC% break-even
fonte: Balanço Patrimonial 2023, 2024, 2025 + Balancete fev/2026 (uploads Gustavo)
relacionados:
  - "[[Logs/2026-04-28 — Sessão Painel Comercial RAF + Decisões Metodológicas]]"
  - "[[Logs/2026-04-27 — Bloco 1+2 RAF + Painel Estoque + Aggregator Painel Comercial]]"
  - "[[Logs/2026-04-17 — Estrutura Duferco-Brasil]]"
---

# 29/04/2026 — Análise DRE Sacchelli + Break-Even Gerencial

Análise dos 4 balanços (BP 2023-25 + Balancete YTD 2026 fev) extraídos pra calibrar threshold "Vaca Leiteira em zona crítica" da matriz BCG do Pacote 1 (rodada 2).

## DRE consolidada — recorrente

| Linha | 2023 | 2024 | 2025 | 2026 YTD jan-fev |
|---|---:|---:|---:|---:|
| Receita Bruta | 412,3 MM | 286,7 MM | 293,3 MM | 43,9 MM |
| (−) Deduções (impostos s/ vendas) | (75,6) | (62,7) | (63,7) | (9,7) |
| **Receita Líquida** | **336,7** | **224,0** | **229,6** | **34,2** |
| (−) CMV (Aço + serviços) | (256,2) | (134,8) | (157,7) | (22,5) |
| **Lucro Bruto** | **80,4** | **89,2** | **71,9** | **11,7** |
| Margem Bruta % | 23,9% | 39,8% | 31,3% | 34,2% |
| (−) Despesas Operacionais | (30,9) | (34,0) | (38,5) | (3,6) |
| Resultado Não-Op + Financeiro | +10,2 | +17,3 | +11,5 | (0,04) |
| **LAIR** | **59,7** | **72,6** | **44,9** | **8,1** |
| (−) IR + CSLL | (19,0) | (23,9) | (14,3) | (2,7) |
| **Lucro Líquido** | **40,7** | **48,6** | **30,5** | **5,3** |
| Margem Líquida (declarada) | 12,1% | 21,7% | 13,3% | 15,5% |

**Ajuste 2024**: R$ 10,6 MM de receita não recorrente (venda de imóveis + equivalência patrimonial). LL ajustado ≈ R$ 38 MM, margem ajustada ≈ 17%.

**Margem líquida recorrente média (4 anos): ~13%.**

## Decomposição dos custos fixos não-comerciais (base 2025)

| Categoria | R$ MM | % Receita Líq |
|---|---:|---:|
| Despesas Administrativas (pessoal, trib, assess, conservação) | 7,0 | 3,1% |
| Despesas Gerais (viagem, fornec público, etc) | 2,6 | 1,1% |
| **Despesas Financeiras (juros bancários + custos bancários)** | **16,6** | **7,2%** |
| Outras (depreciação imob comercial, Rouanet, baixa ativo) | 0,5 | 0,2% |
| **Total fixos estruturais (não-comerciais)** | **26,7** | **11,6%** |

**Importante**: Despesas Comerciais (R$ 11,8 MM em 2025 = 5,1% receita) NÃO entram nessa conta — já estão capturadas no MC do RAF via componentes DDV+LOG+Comissão+Financ. Evita dupla contagem.

## Cálculo do break-even gerencial MC%

Pro cliente "ainda gerar caixa positivo pra Sacchelli", MC% precisa cobrir 3 camadas:

| Camada | % Receita | Cumulativo |
|---|---:|---:|
| Custos fixos não-comerciais | 11,6% | 11,6% |
| IR + CSLL (~6% sobre receita líquida) | 6,2% | 17,8% |
| Lucro líquido alvo (5%) | 5,0% | **22,8%** |

**Decisão: zona crítica em 23%** (com lucro alvo 5%, patamar conservador).

Alternativas:
- **Mínimo absoluto** (zero lucro, só cobrir fixos + impostos): 18%
- **Saudável-alto** (lucro alvo 8%): 26%
- **Mediana histórica observada**: 32%

## Defaults aprovados pra Pacote 1 (Matriz BCG)

| Linha | Valor | Significado |
|---|---|---|
| Linha verde (Estrela cutoff) | **32%** | Mediana histórica — cliente acima entrega margem acima da média |
| Linha vermelha (zona crítica Vaca) | **23%** | Break-even gerencial com lucro alvo 5% |

Cliente entre 23-32% MC = Vaca Leiteira saudável. Abaixo de 23% = Vaca Leiteira em risco (cor vermelha). Inputs configuráveis no header da matriz pra Gustavo testar 25%/26%.

## 3 achados estratégicos críticos (relevantes pra Duferco-Brasil)

### 1. Despesa financeira pesa 7,2% da receita em 2025 — maior depois do CMV

| Ano | Despesa Financeira R$ MM | % Receita Líquida |
|---|---:|---:|
| 2023 | 13,7 | 4,1% |
| 2024 | 14,0 | 6,3% |
| 2025 | 16,6 | 7,2% |
| 2026 YTD | 0,8 | 2,2% |

**Tendência piora ano a ano.** Sacchelli carrega R$ 16,6 MM em juros bancários por ano. Se a alavancagem reduzir pela metade (capitalização externa, redução CDI, alongamento), break-even MC% cai pra ~19%.

**Implicação Duferco**: capital novo desalavanca a empresa → muda toda a leitura de "saúde da carteira" no painel. **Variável crítica pra modelar o cenário pós-deal.**

### 2. Receita 2024 caiu 33% vs 2023 (337 → 224 MM)

CMV caiu proporcionalmente mais (-47%, 256 → 135 MM) — clássico de **destocagem agressiva**. Margem bruta saltou pra 39,8% em 2024 (vs 23,9% em 2023) por giro de estoque velho com preço melhor. Em 2025 volta a 31,3% — fim do efeito destocagem.

**2024 não é caso normal — distorce médias históricas.** Documentar pro vault que 2024 vale como referência de "ano de ajuste de estoque", não de operação recorrente.

### 3. Margem bruta caiu 850 bps de 2024 → 2025

39,8% → 31,3%. Bate com o diagnóstico do painel: Tabela Preta = 15,4% da receita 2026. **Causa estrutural: mix de pricing pior + maior Preta.** Combinado com juros subindo, é o que explica LL caindo de 48,6 → 30,5 MM em 2025 (-37%).

**2025 foi um ano financeiramente apertado pra Sacchelli.** Dado relevante pra modelagem de valuation Duferco.

## Pendências pra fechar Pacote 1

- [ ] Confirmar se despesa financeira é estrutural recorrente ou tem componente temporário (refinanciamento em curso? CDI em queda?)
- [ ] Validar lucro alvo: 5% conservador ou 7% saudável?

Após confirmação, implementar matriz BCG com defaults 32% / 23% (ou 32% / 26% se lucro alvo 7%).

## Conexão com outros logs

- Diagnóstico de pricing fraco: [[Logs/2026-04-27 — Bloco 1+2 RAF + Painel Estoque + Aggregator Painel Comercial#Bit-paridade]] (Tabela Preta 15,4%)
- Decisões Duferco: [[Logs/2026-04-17 — Estrutura Duferco-Brasil]] (Cenário F preferido)
- Metodologia matriz: [[Sistema Operacional Comercial/04 RAF/09 - Critérios de Classificação]] — atualizar com defaults 32%/23%
