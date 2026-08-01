---
tipo: referência-técnica
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [mc1, mc2, dre, margem, demonstração]
---

# 04 — MC1, MC2 e DRE

## Conceitos

### MC1 — Margem de Contribuição 1
**Definição:** receita líquida menos custo do aço.

```
MC1 = Receita_Líquida − Custo_Aço
```

É a margem sobre o **material puro**. Reflete quanto sobra depois de pagar o insumo principal.

### MC2 — Margem de Contribuição 2
**Definição:** MC1 menos custos variáveis (processos, despesas variáveis).

```
MC2 = MC1 − Custos_Variáveis
    = Receita_Líquida − Custo_Aço − Corte − TT − Ensaios − Frete − Comissão
```

É a margem depois de **todas as variáveis do pedido**. Deve cobrir as despesas fixas da operação e gerar lucro.

### Spread de Valor
**Definição:** margem econômica total, incluindo os spreads de cada componente de serviço/financeiro.

```
Spread_Valor = MC2 + Σ margens_ocultas_por_componente
```

---

## Estrutura DRE (simplificada do simulador)

```
RECEITA BRUTA                               R$ X
(-) IPI                                   − R$ ipi
= RECEITA S/IPI                             R$ A
(-) Descontos/abatimentos                 − R$ d
(-) Impostos s/venda (ICMS, PIS, COFINS)  − R$ imp
= RECEITA LÍQUIDA                           R$ B

(-) Custo do Aço                          − R$ c_aço
= MC1                                       R$ mc1    [% sobre B]

(-) Corte                                 − R$ c_cte
(-) Tratamento Térmico (serviço)          − R$ c_ext
(-) Ensaios, Certificações                − R$ c_cer + c_int
(-) Frete (entrega)                       − R$ c_fre
(-) Comissão                              − R$ c_com
(-) Spread Financeiro                     − R$ c_fin
= MC2                                       R$ mc2    [% sobre B]

(-) Despesas Fixas (comercial, logística) − R$ c_fix
= RESULTADO OPERACIONAL                     R$ op    [% sobre B]
```

---

## MC contábil vs MC econômica

Este é um ponto **crítico** descoberto em abr/2026 (ver [[Sistema Operacional Comercial/04 RAF/03 - MC Contábil vs Econômica]]).

### MC contábil
É a MC "tradicional" reportada no sistema — calcula apenas margem sobre o aço explícito.

**No RAF:** `ABCPER_MAR` (pós-faturamento).

**Em abr/2026:** 29,30% sobre receita líquida do aço.

### MC econômica
MC contábil **mais** todas as margens ocultas capturadas em serviços/spreads.

```
MC_econômica = MC_contábil + margem_oculta_corte
                          + margem_oculta_TT
                          + margem_oculta_ensaios
                          + margem_oculta_certif
                          + margem_oculta_interno
                          + margem_oculta_financeiro
                          + margem_oculta_comissão
                          + margem_oculta_impostos
```

**Em abr/2026:**
- MC contábil: R$12,59M → 29,30%
- Margem escondida total: +R$2,64M (corte R$1,0M + FIN R$1,0M + EXT R$466k + COM R$111k + CER R$23k + INT R$19k + IMP 0)
- **MC econômica: R$15,23M → 35,44%**
- **Uplift: +6,15 p.p.**

### Implicação estratégica

**Vendedor vê MC contábil** ao negociar. Se der desconto, desconto come MC contábil direto.

**Margem oculta fica no pedido** a menos que o cliente corte serviços.

**Risco:** vendedor dá desconto acreditando que MC ainda é 29%, sem saber que há +6 p.p. escondido. Em pedido sem serviço, desconto raspa tudo.

**Oportunidade:** incentivar por MC **econômica**, não contábil. Isso alinha incentivo com captura real de valor.

---

## Corredor de MC

### Definição
Faixa de variação **aceitável** de MC% para um perfil de cliente/produto/vendedor.

**Exemplo:**
- Produto X, cliente Y, vendedor Z: corredor 25-35%
- Vendas dentro do corredor: normal
- Vendas abaixo: investigar (desconto agressivo? custo errado?)
- Vendas acima: investigar (oportunidade de ajuste de tabela? cliente mal precificado?)

### Uso operacional
Motor Analítico v1 tem visão "Corredor de MC" — mostra boxplot de MC por família, cliente, vendedor, unidade.

### Para gestão
Indicadores a monitorar semanalmente:
- MC média (mediana) por família
- Outliers (top 5 mais altos, top 5 mais baixos)
- Mudança de corredor mês a mês

---

## DRE no Simulador HTML

### Estrutura implementada
O simulador HTML gera DRE em tempo real ao ajustar inputs:

1. **Cabeçalho:** peça, cliente, data
2. **Bloco de custos:** aço, processos, despesas
3. **Bloco de receita:** preço de venda nos 3 modos (kg, pç, m)
4. **MC1 e MC2 destacados** em verde/amarelo/vermelho
5. **Composição do resultado:** barra empilhada mostrando onde foi parar cada real
6. **KPIs:** MC%, MC R$, comparativo com tabelas A/B/C
7. **Comparativo por unidade:** mesmo cálculo para cada unidade AFS

### Diferencial
- Cores semáforo intuitivas (verde/amarelo/vermelho) — vendedor vê sem precisar ler número
- Alertas visuais quando abaixo da tabela Vermelha
- Print otimizado A4 para entregar ao cliente (com sensibilidade — omite dados internos)

---

## DRE do pacote (multi-item — Entrega 2 pendente)

Conforme [[12 - Modo Pacote Multi-Item]]:

### Conceito
Quando pedido tem múltiplos itens (ex: 10 itens diferentes do mesmo cliente), cada item tem seu próprio pricing. **Pacote** é a **visão consolidada** do pedido.

### Cálculo consolidado (planejado — Entrega 2)
- Soma ponderada de receita por item
- Soma de custos por item
- MC blended (ponderada)
- Custo de servir do pedido (aplicado sobre pacote, não item a item)
- Give/Get visual (o que ganha × o que concede)

### Decisão de produto já tomada (locked):
- **Sem rateio de custo fixo** — precificação é individual; pacote é view analítica
- **Desconto item-a-item** (pode ter campo de desconto % no pacote, aplica igual em todos)
- **Sem gatilho de alerta de margem do pacote** — apenas exibir blended
- **Sem conflito se item tiver Preço Negociado faltando** — rail mostra ⚠ marker

---

## Relação com o RAF (validação)

Todo pricing feito no simulador (planejado) pode ser confrontado com o RAF (realizado). Drift sistemático entre planejado e realizado indica:
- Simulador com parâmetros desatualizados
- Vendedor "contorna" no simulador mas negocia diferente
- Custo real diferente do custo usado no simulador

**Solução estrutural:** Motor Analítico v2 deve gerar feedback loop: comparar DRE esperado × realizado por faixa de pedido, identificar padrões.

---

## Fórmulas-chave (referência rápida)

```
MC1 %              = MC1 / Receita_Líquida × 100
MC2 %              = MC2 / Receita_Líquida × 100
MC econômica %     = (MC contábil + Σ margens_ocultas) / Receita_Líquida × 100
Uplift econômico   = MC econômica − MC contábil (em p.p.)
Corredor MC        = [P25, P75] da distribuição de MC%
Desvio fora corredor = |MC_atual − Mediana_corredor| / Mediana_corredor
```

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[01 - Fórmula do Lucro]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[03 - Componentes de Custo]]
- [[08 - Simulador HTML - Arquitetura]]
- [[12 - Modo Pacote Multi-Item]]
- [[Sistema Operacional Comercial/04 RAF/03 - MC Contábil vs Econômica]]
- [[Sistema Operacional Comercial/04 RAF/04 - Margem Oculta (7 componentes)]]
