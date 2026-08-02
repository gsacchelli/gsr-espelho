---
tipo: referência-técnica
domínio: raf
criado: 2026-06-02
ultima-revisao: 2026-06-02
tags: [mc-pga, metas, pga, margem, raf, apuração-meta]
---

# 10 — Margem MC PGA (Metas Anuais)

## Contexto

Métrica oficial para apuração da **Margem de Contribuição Global** definida no PGA (Plano Geral de Atividades) 2026, aprovado por Wagner Sacchelli. Cada unidade tem meta anual de MC Global a entregar.

Diferente do `MC_Total_RS` do enriquecimento RAF — exclui componentes que **não são entregáveis ao cliente** (REP, CML).

Definida em reunião com gerentes em 02/06/2026.

### A cascata do PGA

Importante entender a hierarquia das linhas do PGA, porque três valores diferentes circulam pela empresa:

| Linha PGA | Valor consolidado | Definição |
|---|---:|---|
| **L** — Lucro Líquido Real Desejado | R$ 47.250.000,00 | Patrimônio Líquido × Taxa de Retorno (7,5% — metade da Selic) |
| **B** — Lucro Global | R$ 70.875.000,00 | L ajustado pela participação do governo (`L / (1−K)` onde K=33,33%) |
| **M** — Margem de Contribuição Global | **R$ 104.100.113,86** | B + Despesas Orçamentárias das Unidades + Despesas Corporativas + Investimentos |

**A meta de gestão de cada unidade é a linha M (Margem de Contribuição Global), não a linha B (Lucro Global).** A MC Global precisa cobrir todas as despesas operacionais + retornar o lucro desejado.

Existe ainda uma linha auxiliar **V — Venda Global Sem IPI** (R$ 297.428.896,74 consolidado) calculada como `M / 35%` (margem média relativa). É **valor indicativo**, não meta — usado para dimensionamento de carteira.

Fonte: `01_Brutos/PGA2026/PGA 2026 - Resumo.xlsx`, aba "PGA 2026", linhas 16, 22, 30 e 36.

---

## Convenções de cálculo (auditadas em 02/06/2026)

### Faturamento "Sem IPI" do PGA

```
Faturamento_PGA = valor_sem_ipi   (= ValorTotal − IPI)
```

Coluna no cubo OLAP RAF: `valor_sem_ipi`. No enriquecido linha-a-linha: `ValorTotal − ABCIPI`.

**Não confundir com `ValorLIQ`** — `ValorLIQ` é o líquido contábil (já desconta ICMS, PIS, COFINS), valor menor. Para o PGA, "sem IPI" significa apenas remover IPI; ICMS continua dentro.

| Métrica | YTD jan-mai/2026 (Sacchelli) |
|---|---:|
| ValorTotal | R$ 101,55 MM |
| ABCIPI | R$ 2,05 MM |
| **valor_sem_ipi (Faturamento PGA)** | **R$ 99,50 MM** |
| ValorLIQ (líquido contábil) | R$ 80,04 MM |

### Op_Categoria — recorte do faturamento

Incluído no Faturamento PGA (todas as operações comerciais):
- Venda
- Devolução (entra com sinal negativo — compensação correta)
- Consumo Próprio
- Beneficiamento
- Exportação
- Outros

**Excluído:** Sucata (não é venda comercial — receita marginal de descarte).

Filtro aplicado: `op_cat != 'Sucata'`.

### Clientes ativos — APENAS quem comprou

```
Clientes_Ativos = nunique(cliente) WHERE op_cat = 'Venda'
```

**Importante:** exclui clientes que só apareceram em Devolução, Consumo Próprio, Sucata, Beneficiamento ou outras operações não-Venda. Sem esse filtro, contamos ~3-4% a mais (cliente que recebeu devolução mas não comprou, por exemplo).

| Recorte | Clientes únicos YTD 2026 |
|---:|---:|
| Todos op_cat | 1.765 |
| **Apenas op_cat=Venda** | **1.704** |

### Margem PGA

```
MC_PGA = MC_Aço + FIN + COR + EXT + INT + CER
```

Calculada sobre as mesmas linhas filtradas do Faturamento (excl Sucata).

Soma de **6 componentes**:

| Componente | Coluna enriquecido | Fórmula interna |
|---|---|---|
| **MC_Aço** | `MC_Aco_RS` | `LiquidoAço − Custo Aço` (margem contábil direta) |
| **FIN** | `FIN_Spread` | `ABCCUS_FIN − ABCCUS_FIN_COB` (CF% cobrado − Selic equivalente) |
| **COR** | `COR_Spread` | `ABCCUS_CTE − ABCCUS_CTE_COB` (corte cobrado − custo real ~0) |
| **EXT** | `EXT_Spread` | `ABCCUS_EXT − ABCCUS_EXT_COB` (TT cobrado − pago ao tratador) |
| **INT** | `INT_Spread` | `ABCCUS_INT − ABCCUS_INT_COB` (processos internos − custo ~0) |
| **CER** | `CERT_Spread` | `ABCCUS_CER − ABCCUS_CER_COB` (certificação − custo emissão ~0) |

### % MC PGA

```
MC_PGA_pct = MC_PGA / ValorLIQ
```

---

## Excluídos da MC PGA

| Componente | Por que NÃO entra |
|---|---|
| **REP** (comissão) | Custo de venda paga a representante/vendedor. Não é serviço entregue ao cliente. |
| **DDV+LOG** (despesas logísticas embutidas em CML) | Despesa fixa absorvida — não é entregável. Sai pela conta de despesa. |
| **IPI** | Imposto. Faturamento PGA é sem IPI por convenção. |

---

## Diferença vs MC_Total_RS (RAF enriquecimento)

| Métrica | Componentes |
|---|---|
| **MC_Total_RS** (enriquecimento) | MC_Aço + FIN + COR + EXT + INT + CER + **REP** + CML |
| **MC_PGA** (meta) | MC_Aço + FIN + COR + EXT + INT + CER |

Diferença = `REP_Spread + CML embutido`.

Em alguns recortes a diferença é pequena (~1-2% do MC); em outros, mais relevante (depende de quanto da venda foi via representante e quanto de logística cobrada).

---

## Implementação no motor

Cálculo está em `MotorAnalitico/exports/gerar_apresentacao_gerentes.py` (função `_agregar_kpis`):

```python
out['mc_aco']    = _f(raf['mc_aco'].sum())
out['fin']       = _f(raf['fin'].sum())
out['cor']       = _f(raf['cor'].sum())
out['ext']       = _f(raf['ext'].sum())
out['int_']      = _f(raf['int_'].sum())
out['cer']       = _f(raf['cer'].sum())
out['mc_pga']    = out['mc_aco'] + out['fin'] + out['cor'] + out['ext'] + out['int_'] + out['cer']
out['mc_total']  = out['mc_pga']  # substitui mc_total antigo
out['mc_pct']    = out['mc_pga'] / out['faturamento'] * 100  # sobre ValorLIQ (sem IPI)
```

No cubo OLAP (`painel_data.js → window.PD → cubo`), os componentes individuais já estão agregados como `mc_aco`, `fin`, `cor`, `ext`, `int_`, `cer`.

---

## Metas de Margem de Contribuição PGA 2026

Aprovado por Wagner Sacchelli. Meta é a **Margem de Contribuição Global** por unidade (linha M do PGA).

| Unidade                | Gestor                | Meta MC Global Anual  |
| ---------------------- | --------------------- | --------------------: |
| Matriz + Vila Prudente | Felipe Sória / Fuscão |      R$ 73.402.067,99 |
| Piracicaba             | Odair Oliveira        |      R$ 10.140.473,37 |
| São Carlos             | Odair Oliveira        |       R$ 8.816.000,80 |
| Caxias do Sul          | Fabíola Cardoso       |       R$ 8.388.093,23 |
| Rio Preto              | Fernando Roveda       |       R$ 3.353.478,48 |
| **TOTAL SACCHELLI**    | —                     | **R$ 104.100.113,86** |

Fonte: `01_Brutos/PGA2026/PGA 2026 - Resumo.xlsx`, linha 30 ("M — Margem de Contribuicão Global"). Revisão 17/12/2025.

---

## Status atingimento da MC Global (jan-mai/2026 — 41,7% do ano transcorrido)

Recalculado contra a meta M (linha 30 do PGA) — não mais contra B (Lucro Global).

| Unidade | Meta MC Global | MC Realizada YTD | % Atingido | % Projetado | Status |
|---|---:|---:|---:|---:|---|
| São Carlos | R$ 8,82 MM | R$ 3,56 MM | **40,4%** | 97,0% | ⚠ ATENÇÃO |
| Piracicaba | R$ 10,14 MM | R$ 3,19 MM | 31,5% | 75,5% | 🔴 ATRASADO |
| Rio Preto | R$ 3,35 MM | R$ 0,95 MM | 28,4% | 68,2% | 🔴 ATRASADO |
| Matriz +VP | R$ 73,40 MM | R$ 17,10 MM | 23,3% | 55,9% | 🔴 ATRASADO |
| Caxias do Sul | R$ 8,39 MM | R$ 0,85 MM | **10,1%** | 24,3% | 🔴 ATRASADO |
| **TOTAL** | **R$ 104,10 MM** | **R$ 25,65 MM** | **24,6%** | **59,1%** | 🔴 ATRASADO |

MC Realizada calculada via fórmula MC PGA acima (= MC_Aço + FIN + COR + EXT + INT + CER).


**Diagnóstico:** com a meta correta (R$ 104 MM), Sacchelli está significativamente atrasada — projeção de 59% do ano. Mesmo São Carlos (que era a única "no ritmo" contra a meta B errada) agora cai pra 40,4% (vs ideal 41,7%). Diferença vem da expectativa do PGA de que a MC cubra TODAS as despesas operacionais (D_Unidades + D_Corporativa) + Investimentos + Lucro Global.

---

## Como auditar

Excel de auditoria detalhada por linha: `02_Derivados/Reuniao_Gerentes/Auditoria_MC_PGA_20linhas.xlsx`. Mostra cada um dos 6 componentes decompostos em (Cobrado · Real · Spread) numa amostra estratificada.

Script de geração: `MotorAnalitico/exports/gerar_auditoria_mc_pga.py`.

---

## Conexões

- [[04 - Margem Oculta (7 componentes)]] — origem conceitual dos spreads
- [[02 - Convenção Softcomp (Invertida)]] — campos cobrado/real
- [[03 - MC Contábil vs Econômica]]
- [[05 - Custo Real vs Cobrado]]
- [[06 - Despesas Logísticas por Unidade]] — CML / DDV+LOG

---



> ⚠️ **Correção 02/08/2026:** esta nota citava `ABCCUS_COR` e `ABCCUS_REP`, que **não existem** no RAF — os nomes reais são `ABCCUS_CTE` (corte) e `ABCCUS_COM` (representação). O mesmo erro estava em `MotorAnalitico/exports/gerar_auditoria_mc_pga.py`, que devolvia 0,0 em silêncio: o Excel `Auditoria_MC_PGA_20linhas.xlsx` que circulou entre os gerentes mostrava **Cobrado 0 / Real 0** nas linhas de Corte e Representação, com o Spread preenchido. Corrigido nos dois lugares, e a leitura agora levanta exceção em coluna inexistente.
