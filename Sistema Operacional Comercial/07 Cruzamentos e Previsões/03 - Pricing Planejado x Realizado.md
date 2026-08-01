---
tipo: cruzamento
domínio: cruzamentos
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [cruzamento, pricing, calibração, drift]
---

# 03 — Pricing Planejado × Realizado

## Propósito

Comparar **DRE planejada** (gerada pelo Simulador no momento da cotação) com **DRE realizada** (reportada no RAF pós-faturamento) para:
- **Calibrar** o simulador (parâmetros estão realistas?)
- **Detectar drift** (vendedor contorna simulador? cliente negocia além?)
- **Alertar** sobre mudanças de mercado (custo subiu e pricing não foi ajustado?)

---

## Perguntas que respondemos

### Calibração
- Simulador previu MC 28% — RAF realizou 25%. Por quê?
- Quais parâmetros do simulador estão desatualizados?

### Drift comportamental
- Há vendedores com gap sistemático (cotam alto, faturam baixo)?
- Há clientes específicos que sempre negociam além do cotado?

### Contexto de mercado
- Custo aço subiu mas tabela e simulador não acompanharam?
- MC geral caindo — por erosão ou mix?

### Validação da regra de negócio
- Spread financeiro cotado bate com Selic realizada?
- Custo de TT estimado bate com realizado?
- VPP e tolerância aplicados corretamente?

---

## Estrutura do cruzamento

```
por_cotacao_faturada = {
  cotacao_id,
  pedido_os,

  # Do simulador (cotação):
  simulador_preco,
  simulador_custo_aco,
  simulador_mc1,
  simulador_mc2,
  simulador_margem_oculta,
  simulador_mc_economica,

  # Do RAF (realizado):
  raf_receita_liq,
  raf_custo_aco,
  raf_mc_contabil,
  raf_margem_oculta,
  raf_mc_economica,

  # Gap:
  gap_preco = raf_preco - simulador_preco,
  gap_custo_aco = raf_custo_aco - simulador_custo_aco,
  gap_mc_contabil = raf_mc_contabil - simulador_mc1,
  gap_margem_oculta = raf_margem_oculta - simulador_margem_oculta,
  gap_mc_economica = raf_mc_economica - simulador_mc_economica,
}
```

---

## Análises típicas

### 1. Scatter plot MC planejada vs MC realizada

Eixo X: MC do simulador
Eixo Y: MC do RAF
Linha ideal: y = x

- **Pontos na linha:** simulador bem calibrado
- **Pontos abaixo da linha:** realizado é menor que planejado (desconto não previsto, custo maior)
- **Pontos acima:** realizado melhor que planejado (custo veio menor, MC real boa)

Padrão sistemático revela calibração necessária.

### 2. Evolução temporal do gap

Gap mês a mês:
- Estável: calibração ok
- Tendência de piora (gap crescente negativo): algo está mudando
- Salto brusco: evento específico (mudança de custo, política)

### 3. Gap por vendedor

- Vendedores com gap = 0 (ou positivo): seguem o simulador
- Vendedores com gap negativo sistemático: "contornam" — dão desconto extra
- Investigar causa: conversa necessária ou ajuste de processo

### 4. Gap por família

- Famílias com gap 0: calibração ok
- Famílias com gap negativo: parâmetros do simulador defasados?
- Exemplo: custo CFR China +35% em 5 semanas mas simulador não atualizou → gap negativo crescente

### 5. Drift de custo

Comparar `simulador_custo_aco` com `raf_custo_aco`:
- Se sistemático raf > simulador: custo subiu, simulador desatualizado
- Se raf < simulador: custo caiu, simulador pode ter ajuste positivo

---

## Dashboard proposto (Motor Analítico v2)

### Tela 1 — Gap agregado
- MC planejada vs realizada (total)
- Gap médio e P25/P75
- Tendência últimos 6 meses

### Tela 2 — Por vendedor
- Ranking de gap (positivo ou negativo)
- Outliers
- Alerta vermelho para gap grande e persistente

### Tela 3 — Por família
- Heatmap família × gap
- Famílias com calibração problemática

### Tela 4 — Drift de parâmetros
- Custo aço: evolução simulador vs realizado
- Spread financeiro: idem
- Despesas logísticas: idem

### Tela 5 — Ação sugerida
- "Revisar parâmetro X — drift de Y%"
- "Conversa com vendedor Z — gap persistente"
- "Atualizar tabela de preço para família W"

---

## Benefício esperado

### Calibração contínua do simulador
Simulador vira **ferramenta viva**: parâmetros ajustados com base em realizado, não congelados.

### Feedback loop pricing
Vendedor pode ver: "Você está sistematicamente fechando abaixo do simulador. Isso é intencional?"

### Alerta de mercado
Custo aço subiu? Dashboard detecta na primeira semana de gap — não 3 meses depois.

---

## Desafios de implementação

### 1. Cotações que não viraram pedidos
Precisam ser excluídas do cruzamento (não há RAF correspondente).

### 2. Consolidação
RAF precisa ser consolidado por OS (ver [[04 RAF/08 - Consolidação por OS]]).

### 3. Cotação vs Pedido
Se houve desconto adicional entre cotação e pedido, **o gap não é contra o simulador**, é contra a negociação. Rastreabilidade importante.

### 4. Timing
Cotação de fev, fatura em maio. Comparar exige janela móvel, não mês fechado.

---

## Roadmap

### Motor Analítico v2
- Ingestão cruzada cotação + RAF
- Dashboard de calibração

### v3 (futuro)
- Ajuste **automático** de parâmetros do simulador com base em drift persistente
- Alertas em tempo real

---

## Conexões

- [[00 - Visão Geral Cruzamentos]]
- [[01 - Cotação x Pedido x RAF]]
- [[02 Precificação/00 - Visão Geral Precificação]]
- [[02 Precificação/02 - Fórmula de Preço Sacchelli]]
- [[02 Precificação/08 - Simulador HTML - Arquitetura]]
- [[04 RAF/03 - MC Contábil vs Econômica]]
- [[04 RAF/05 - Custo Real vs Cobrado]]
