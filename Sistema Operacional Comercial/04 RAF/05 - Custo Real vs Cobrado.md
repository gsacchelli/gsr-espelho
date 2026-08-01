---
tipo: referência-técnica
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [custo, real, cobrado, análise]
---

# 05 — Custo Real vs Cobrado

## Nota de consolidação

Esta nota sintetiza como **calcular e interpretar** a diferença cobrado vs real para análises operacionais. Para a nomenclatura e armadilha, ver [[02 - Convenção Softcomp (Invertida)]]. Para detalhes componente a componente, ver [[04 - Margem Oculta (7 componentes)]].

---

## Fórmulas por componente (referência)

```
Para cada componente X em {ACO, FIN, IMP, COM, CML, INT, CER, EXT, CTE}:

  valor_cobrado_X = ABCCUS_X         # sem sufixo = cobrado
  custo_real_X    = ABCCUS_X_COB     # com sufixo _COB = real
  margem_oculta_X = valor_cobrado_X - custo_real_X
```

**Positivo:** AFS capturou margem (cobrou > real)
**Negativo:** AFS absorveu (cobrou < real)
**Zero:** sem spread (estrutural, como ACO)

---

## Aplicação prática — análise por cliente

### Processo
1. Carregar RAF (com tradução correta)
2. Agregar por cliente:
   - Soma de valor_cobrado por componente
   - Soma de custo_real por componente
   - Soma de margem_oculta por componente
3. Calcular total margem oculta por cliente
4. Rankear por valor econômico total (MC contábil + margem oculta)

### Exemplo
```
Cliente ACME:
  Receita líquida:        R$1.000.000
  Custo aço:              R$ 700.000
  MC contábil:            R$ 300.000  (30%)

  Margem oculta:
    Corte:                +R$ 25.000
    TT (EXT):             +R$ 10.000
    Financeiro:           +R$ 20.000
    Outros:               +R$  5.000
  Total margem oculta:    +R$ 60.000  (6,0 p.p.)

  MC econômica:           R$ 360.000  (36,0%)
```

---

## Aplicação por família

Agregar por família canônica (ver [[03 Estoque/01 - Família Canônica]]):

**Perguntas respondidas:**
- Qual família tem maior margem oculta?
- Famílias de aço puro vs famílias com serviço — comparar
- Aço ferramenta premium tem margem oculta maior?

---

## Aplicação por vendedor

Agregar por `ABCCLI_VND`:

**Perguntas respondidas:**
- Qual vendedor captura mais margem econômica (não apenas volume)?
- Vendedor com MC contábil baixa mas alta margem oculta = vende serviço embutido muito bem
- Vendedor com MC contábil alta mas baixa margem oculta = vende aço puro

Isso muda o ranking tradicional de vendedor (só por volume ou MC contábil).

---

## Aplicação por unidade

Agregar por unidade (GRU, SCA, PIR, RIP, CXS):

**Pergunta-chave:** CXS tem handicap logístico. MC contábil dela é menor. Mas a margem econômica compensa?

Ver [[06 - Despesas Logísticas por Unidade]].

---

## Cuidados ao calcular

### 1. Consolidação por OS
Obrigatório. Sem isso, uma linha pode ter custo total e outra zero, distorcendo análise.

Ver [[08 - Consolidação por OS]].

### 2. Missing values
Se campo `ABCCUS_X_COB` estiver vazio (não zero), não é o mesmo. Verificar como interpretar:
- Se NaN: usar 0 ou excluir linha?
- Default recomendado: usar 0 (componente não aplicável)

### 3. Valores negativos anormais
Componente com margem oculta negativa grande pode ser:
- Absorção legítima (caso a caso)
- Erro de cadastro
- Inversão de coluna (bug no export)

**Investigar** antes de concluir que AFS está perdendo.

### 4. Outliers
Pedidos atípicos (cliente único, material engenheirado) podem distorcer. Filtrar ou separar em análise.

---

## Análise temporal

### Evolução mensal
Gráfico de margem oculta total por mês. Tendência:
- **Estável:** saudável
- **Crescente:** AFS capturando mais valor (por quê?)
- **Decrescente:** erosão — investigar causa

### Por componente ao longo do tempo
- Corte: estável se política não mudou
- Financeiro: depende de mix de prazo
- EXT: depende de mix de serviços

### Alertas
Margem oculta cai > 20% mês-a-mês: alerta vermelho. Causa:
- Cliente grande negociou serviço barato
- Mix de pedidos mudou (mais aço puro)
- Erro de cálculo / cadastro

---

## Comparação planejado vs realizado

### Simulador vs RAF
Simulador gera DRE **planejada** para cotação. RAF mostra **realizado** pós-fechamento.

Drift sistemático indica:
- Simulador com parâmetros desatualizados
- Vendedor "contorna" no simulador
- Cliente consegue descontos não previstos

**Motor Analítico v2 pode gerar dashboard "Corredor de MC"**:
- Distribuição de MC realizada por família
- Corredor normal (P25-P75)
- Outliers
- Desvio do previsto

---

## Recomendações de ação

### Curto prazo
1. **Ranking mensal** de clientes por valor econômico (não só volume)
2. **Top 10** clientes com maior margem oculta — entender por quê (replicar?)
3. **Top 10** clientes com margem oculta negativa — renegociar?

### Médio prazo
1. **Calibração do simulador** com parâmetros realizados
2. **Dashboard por unidade** com breakdown cobrado vs real
3. **Alertas** quando uplift cai abaixo de 5 p.p.

### Longo prazo
1. **Servitização** (trazer margem oculta para explícito) — discussão estratégica
2. **Mudança de remuneração** (incentivar aderência à tabela e cobrança de serviço)

---

## Conexões

- [[00 - Visão Geral RAF]]
- [[02 - Convenção Softcomp (Invertida)]]
- [[03 - MC Contábil vs Econômica]]
- [[04 - Margem Oculta (7 componentes)]]
- [[06 - Despesas Logísticas por Unidade]]
- [[08 - Consolidação por OS]]
- [[02 Precificação/10 - Custo de Servir Aplicado]]
- [[01 Sistema de Dados/06 - Motor Analítico v1]]
