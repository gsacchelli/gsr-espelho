---
tipo: conceito-aplicado
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [custo-servir, pricing, aplicação, carteira]
---

# 10 — Custo de Servir Aplicado

## Contexto

Esta nota é a **aplicação operacional** do conceito estratégico [[Custo de Servir]] (vault raiz) no contexto AFS.

Para o conceito teórico completo, ver nota estratégica. Aqui detalhamos **como aplicar** na prática do dia a dia.

---

## O problema no AFS atual

### O que está funcionando
- RAF captura estrutura de custo com campos COB e real
- Dashboard Motor Analítico separa margem econômica da contábil
- Spread por componente mensurável (corte, TT, financeiro, etc.)

### O que NÃO está funcionando
- **Simulador não calcula custo de servir** por cliente antes de propor preço
- **Vendedor não vê** margem líquida real por cliente ao negociar
- **Remuneração não reflete** custo de servir
- **Conversa com cliente** sobre Give/Get não é sistemática
- **Ranking de clientes** não distingue volume de rentabilidade real

---

## Componentes de custo de servir no AFS

### Operação
| Item | Indicador | Onde está no RAF |
|---|---|---|
| Urgência (produção ou separação) | % de pedidos com flag urgência | Não capturado hoje |
| Setup adicional | Horas extras de setup por pedido | Não capturado |
| Fracionamento | # de liberações parciais por OS | RAF (múltiplas linhas) |
| Retrabalho | # de retrabalhos por OS | Não capturado sistematicamente |
| Devolução | % de devoluções | Financeiro/fiscal |
| Armazenagem específica | Dias de custo de estoque dedicado | Não capturado |

### Logística
| Item | Indicador | Onde está |
|---|---|---|
| Frete especial | Desvio do frete padrão | Parcial — custo cobrado vs real |
| Entregas múltiplas | # de entregas por OS | Não capturado |
| Paletização customizada | Custo adicional embalagem | Não capturado |

### Comercial / Administrativo
| Item | Indicador | Onde está |
|---|---|---|
| Horas engenharia | Horas aplicadas por cliente | Não capturado formalmente |
| Cotação repetida sem fechamento | # de cotações não-convertidas | Cot_Encerradas |
| Crédito prolongado | Dias além do prazo padrão | Financeiro |
| Inadimplência | % e valor de atraso/provisão | Financeiro |
| Customização documental | # de docs específicas | Não capturado |

### Relacional
| Item | Indicador | Onde está |
|---|---|---|
| Visitas fora de padrão | # de visitas/mês | Não capturado |
| Atendimento pós-venda | Horas de suporte | Não capturado |
| Gerenciamento de conflito | Qualitativo | Não capturado |

**Conclusão:** hoje **a maior parte** do custo de servir não é capturada sistematicamente no Softcomp. É conhecimento tácito dos vendedores + análises ad-hoc.

---

## Framework de cálculo (proposta para Motor Analítico v2)

### Etapa 1 — Capturar o que é capturável hoje (RAF + Cot_Encerradas)

Para cada cliente, calcular:

```
CS_1_fracionamento = (# linhas RAF do cliente / # OS únicas) − 1
                      (quanto mais linhas por OS, mais fracionamento)

CS_2_cotacao_nao_convertida = valor_cotado_nao_fechado / valor_fechado
                               (esforço de cotação desperdiçado)

CS_3_desvio_frete = |frete_real − frete_padrão_região| / frete_padrão

CS_4_prazo_extendido = dias_real_pagamento − dias_contratado
```

### Etapa 2 — Adicionar capturas manuais sistemáticas

Para cada cliente, anotar (planilha/form):
- Nº de urgências/mês (conta vendedor)
- Nº de retrabalhos/ano
- Nº de visitas fora de padrão
- Horas de engenharia/mês (aproximado)

Esses valores vão para tabela mestre de custo de servir.

### Etapa 3 — Calcular índice composto

```
CS_total_cliente = (CS_1 × peso_1) + (CS_2 × peso_2) + ... + (CS_manual × peso_m)

Margem_líquida_real = MC_econômica_cliente − CS_total_cliente × volume_cliente
```

### Etapa 4 — Ranking de carteira por margem líquida real

Output: **Top 20 clientes por margem líquida real** (vs volume apenas).

Cliente com alto volume e baixa margem líquida → candidato a requalificar.

---

## Fluxo de aplicação na negociação

### Cenário 1 — Cliente pede desconto

**Sem custo de servir mapeado:** vendedor dá desconto por "sensibilidade".

**Com custo de servir mapeado:**
1. Vendedor consulta painel — margem líquida real do cliente é X%
2. Se X% está acima da média da carteira: desconto possível
3. Se X% está abaixo: negociação invertida — "atual margem líquida só permite esse preço se reduzirmos seu custo de servir (frequência de urgência, consolidação de entrega, etc.)"

### Cenário 2 — Prospect novo

**Sem CS:** precifica com tabela padrão.

**Com CS:** estima custo de servir **baseado em perfil** (indústria, localização, expectativa de prazo). Precifica incluindo CS estimado.

### Cenário 3 — Revisão anual de carteira

**Sem CS:** revisão por volume e tabela atual.

**Com CS:** ranking de margem líquida real. 3 categorias:

- **Top rentável:** manter e **expandir** (até +30% volume sem perder margem)
- **Meio:** requalificar com Give/Get estruturado
- **Cauda não-rentável:** renegociar termos ou descontinuar

---

## Propostas de Give/Get típicas

### Give/Get 1 — Consolidação de entrega
**Get (cliente dá):** consolidar pedidos em 2 entregas/mês (vs múltiplas)
**Give (AFS dá):** 2% de desconto

**Impacto AFS:**
- Custo de servir reduz 3-4% (frete + manuseio)
- Margem líquida real melhora 1-2 p.p.

### Give/Get 2 — Prazo de produção
**Get:** cliente aceita prazo padrão (não urgência a cada pedido)
**Give:** garantia de disponibilidade + preço estável por trimestre

**Impacto AFS:**
- Elimina urgências (maior custo de servir)
- Cliente ganha previsibilidade

### Give/Get 3 — Redução de retrabalho
**Get:** cliente envia especificação completa e definitiva antes do corte
**Give:** commitment de prazo de produção

**Impacto AFS:**
- Retrabalho cai
- Ciclo melhora

### Give/Get 4 — Pagamento em dia
**Get:** pagamento em data (sem extensão)
**Give:** preservar condição atual / evitar repasse de Selic

**Impacto AFS:**
- Spread financeiro mantido
- Capital de giro otimizado

---

## Regras fundamentais

### Regra 1 — Custo de servir entra **antes** do preço
Sequência correta:
1. Escopo definido (o que cliente quer)
2. Custo de servir estimado (como vai atender)
3. Margem alvo
4. Preço final

Invertendo: vendedor dá preço sem saber o custo operacional real. Fórmula para destruir margem silenciosamente.

### Regra 2 — Não aceitar "cortesia"
Urgência, retrabalho, customização **nunca** são cortesia. São **serviços**. Ou são cobrados ou são negociados com Give/Get.

"Refaz sem custo" = perdemos 2x (custo do refazer + precedente para repetir).

### Regra 3 — Não confundir urgência do cliente com obrigação contratual
Prazo contratado = obrigação. Prazo além da urgência do cliente = serviço que custa.

### Regra 4 — Desconto destrói MC contábil; margem oculta fica
Se cliente **corta serviço** (aço puro, sem TT, sem certif), margem oculta some. Vendedor precisa saber.

### Regra 5 — Pedir contrapartida é profissional
Ceder sem condição destrói valor para todos. Give/Get é padrão de conversa, não exceção.

---

## Dashboard proposto (Motor Analítico v2)

### Tela 1 — Ranking da carteira
- Top 20 clientes por margem líquida real (MC econômica − CS)
- Cliente com alto volume e baixa margem → destaque
- Comparar com ranking por volume (mostra a inversão)

### Tela 2 — Componentes de CS por cliente
- Breakdown: fracionamento, urgência, retrabalho, frete, etc.
- Evolução temporal
- Benchmark com média da carteira

### Tela 3 — Propostas de Give/Get
- Para cada cliente do "meio" ou "cauda", sugerir 2-3 Give/Gets
- Estimativa de impacto se cliente aceitar

### Tela 4 — Simulação de requalificação
- Se clientes X e Y aceitarem Give/Gets propostos, qual o impacto na margem da carteira?
- Quanto % da carteira precisa mudar para alinhar pricing com realidade?

---

## Histórico e próximos passos

### Já feito
- RAF estruturado (133 colunas, margem oculta mapeada)
- Diagnóstico 29.748 cotações (identificação de perdas)
- Motor Analítico v1 arquitetura definida

### Próximos (quando houver tempo)
1. **Ativar CS no Motor v2** — adicionar ranking de margem líquida real
2. **Simulador — campo CS estimado** — Entrega 2 já prevê
3. **Relatório mensal Top 20** — disparar conversas de requalificação
4. **Conversa cirúrgica com 2-3 clientes** identificados

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[01 - Fórmula do Lucro]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[04 - MC1 MC2 e DRE]]
- [[08 - Simulador HTML - Arquitetura]]
- [[12 - Modo Pacote Multi-Item]]
- [[Sistema Operacional Comercial/04 RAF/05 - Custo Real vs Cobrado]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]
- Vault estratégico: [[Custo de Servir]], [[Cliente Ideal]]
