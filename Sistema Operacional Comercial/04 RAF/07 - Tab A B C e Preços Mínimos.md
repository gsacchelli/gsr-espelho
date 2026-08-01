---
tipo: referência-técnica
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [tabelas, preço-mínimo, verde-amarela-vermelha]
---

# 07 — Tab A B C e Preços Mínimos

## Referência cruzada

Esta nota detalha os **campos RAF** relacionados a tabelas de preço. Para o processo operacional e alçada (Verde/Amarela/Vermelha), ver [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]].

---

## Campos RAF

| Campo | Significado | Interpretação |
|---|---|---|
| `ABCPRE_MIN_A` | Piso Tabela Verde (R$/kg) | Preço cheio — cliente premium |
| `ABCPRE_MIN_B` | Piso Tabela Amarela (R$/kg) | Preço intermediário |
| `ABCPRE_MIN_C` | Piso Tabela Vermelha (R$/kg) | Piso mínimo padrão |

### Campo `ABCPRE_VDA`
Preço **efetivamente praticado** na venda. Permite comparação:

```
Spread_Tab_A = (PRE_VDA − PRE_MIN_A) / PRE_MIN_A × 100
Spread_Tab_C = (PRE_VDA − PRE_MIN_C) / PRE_MIN_C × 100
```

**Interpretação:**
- Spread Tab A > 0: venda **acima** do piso verde (ótimo)
- Spread Tab A ≈ 0: venda **no piso verde**
- Spread Tab A < 0 mas Spread Tab C > 0: venda **entre verde e vermelho** (zona cega)
- Spread Tab C < 0: venda **abaixo** do vermelho — requereu aprovação de diretor

---

## Análise típica

### Classificação da venda
```python
def classificar_venda(pre_vda, pre_a, pre_b, pre_c):
    if pre_vda >= pre_a:
        return 'Acima Verde (ótimo)'
    elif pre_vda >= pre_b:
        return 'Verde-Amarela'
    elif pre_vda >= pre_c:
        return 'Amarela-Vermelha'
    else:
        return 'Abaixo Vermelha (exceção)'
```

### Distribuição esperada
Em operação saudável:
- **Acima Verde:** 5-10% (cliente premium, AFS manda preço)
- **Verde-Amarela:** 30-50% (negociação normal)
- **Amarela-Vermelha:** 30-50% (negociação agressiva)
- **Abaixo Vermelha:** <10% (exceção justificada)

**Sinais de alerta:**
- **Abaixo Vermelha > 15%:** exceção virou regra — problema de pricing ou cadastro
- **Acima Verde < 2%:** vendedor não captura prêmio de cliente premium
- **Concentração em Amarela-Vermelha:** vendedor opera na zona cega (onde o diretor não vê)

---

## Problemas típicos

### Tabela vencida
Se **custo de aço sobe** (CFR China +35% recente) mas tabelas **não são atualizadas**, piso Vermelho vira prejuízo silencioso.

**Mitigação:** revisão de tabela **no mínimo mensal**. Quando custo mexe > 5%, revisar imediatamente.

### Zona cega verde-vermelha
Vendedor age sozinho entre Verde e Vermelha. Diretor só vê o que desce abaixo da Vermelha.

**Consequência:** se 80% das vendas estão em Amarela-Vermelha, diretor não vê — mas a margem está corroída.

**Mitigação operacional (sem mexer em remuneração):**
- Relatório mensal de **frequência de uso das 3 tabelas por vendedor**
- Identificar vendedores concentrados em Amarela-Vermelha sem justificativa
- Conversa cirúrgica com 2-3 piores casos

### Falta de tabela para fora de padrão
Itens "Fora de Padrão" não têm tabela A/B/C definida. Vendedor precisa precificar manualmente.

**Mitigação:** formalizar tabela quando item Fora de Padrão vira recorrente (ver [[Sistema Operacional Comercial/03 Estoque/06 - Fora de Padrão]]).

---

## Análises úteis

### Por vendedor
- % de vendas em cada faixa
- Spread médio vs tabela
- Ranking de vendedores por **preservação de preço**

### Por família
- Família com alto % Acima Verde: cliente valoriza muito — mercado aceita prêmio
- Família com alto % Abaixo Vermelha: pressão competitiva — revisar tabela?

### Por cliente
- Cliente que compra sempre Acima Verde: **cliente premium real**
- Cliente que compra sempre Abaixo Vermelha: **tabelista ou problemático**

### Temporal
- Evolução do % em cada faixa ao longo do tempo
- Queda de Verde → Amarela sinaliza erosão de pricing

---

## Correlação com MC

Venda em Verde: MC típica alta (25-35%)
Venda em Amarela-Vermelha: MC típica média (15-25%)
Venda Abaixo Vermelha: MC típica baixa (< 15%)

**Não é regra perfeita** — MC depende de outros fatores (custo aço, serviços embutidos, cliente específico). Mas é correlação forte.

---

## Integração com ferramentas

### Simulador
Simulador mostra as 3 tabelas + preço praticado no cálculo. Vendedor vê **visualmente** onde está.

### Motor Analítico
Motor pode gerar dashboard "Corredor de Tabela":
- % em cada faixa por vendedor/família/cliente
- Outliers
- Tendência temporal

### Painel Comercial (versões antigas)
Painéis existentes (v1-v4) podem ter visão parcial disso. Trazer ao padrão v2 se implementado consistentemente.

---

## Conexões

- [[00 - Visão Geral RAF]]
- [[01 - Estrutura das 133 Colunas]]
- [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]]
- [[Sistema Operacional Comercial/02 Precificação/02 - Fórmula de Preço Sacchelli]]
- [[Sistema Operacional Comercial/03 Estoque/06 - Fora de Padrão]]
