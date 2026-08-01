---
tipo: conceito-fundacional
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [lucro, margem, custo-servir, fórmula, conceito]
---

# 01 — Fórmula do Lucro

## Enunciado

**Lucro = Receita − Descontos/Abatimentos − Custo de Produzir/Comprar − Custo de Servir**

Este é o princípio **mais importante** de toda a inteligência comercial. Quem não entende isso negocia no escuro.

---

## Decomposição dos 4 termos

### Receita
O que o cliente paga, antes de qualquer ajuste. Inclui:
- Preço base por unidade (R$/kg, R$/pç, R$/m)
- Serviços faturados explicitamente (quando aplicável)
- Juros financeiros quando venda a prazo

### Descontos / Abatimentos
Reduções **visíveis** aplicadas ao preço:
- Desconto comercial (negociado por vendedor)
- Abatimento por qualidade (quando item não conforme ainda vendido)
- Bonificação em espécie (entrega além do faturado)
- Ajustes de campanha promocional

**Característica:** aparecem em sistema. Diretor vê se desce abaixo da tabela Vermelha.

### Custo de Produzir / Comprar
O que **entra no produto** para ele existir:
- **Aço** (custo de aquisição, campo `ABCPRE_KG` no RAF)
- **Corte** (processamento que transforma barra → peça cortada)
- **Serviços externos** (tratamento térmico, ensaios, certificação)
- **Impostos não-recuperáveis**
- **Perda de processo** (rendimento: material que vira refugo)

**Característica:** documentado no pedido, rastreável por OS.

### Custo de Servir
O que **varia por cliente** e **não está no produto**:
- Urgências (produção/separação fora do padrão)
- Setup adicional (troca de lote, mudança de programa)
- Fracionamento (pedidos pequenos, múltiplas entregas)
- Retrabalhos e reorçamentos
- Devoluções e recoletas
- Armazenagem específica
- Fretes especiais (horário, veículo, região)
- Entregas múltiplas pelo mesmo valor faturado
- Horas de engenharia e aplicação técnica
- Cotação repetida sem fechamento
- Crédito prolongado e renegociação de prazo
- Custo de cobrança, inadimplência
- Customização de documentação, laudo, NF
- Visitas comerciais fora do padrão
- Atendimento pós-venda intensivo
- Gerenciamento de conflito operacional

**Característica:** geralmente **invisível** no sistema. É aqui que mora a destruição silenciosa de margem.

---

## As 3 verdades fundamentais

### Verdade 1 — Volume sem rentabilidade é armadilha
Todo cliente que cresce sem reduzir custo de servir **corrói margem**, mesmo com receita alta.

Exemplo: cliente A cresce 30% mas exige 4 urgências/mês e entregas em 3 horários. Receita sobe, margem real pode cair.

### Verdade 2 — Desconto é visível; custo oculto é silencioso
Quem não calcula custo de servir **negocia no escuro e perde duas vezes** — dá desconto E absorve custo.

Exemplo: vendedor dá 3% de desconto para fechar pedido. Cliente pede urgência e fracionamento. Custo de servir adicional: 5%. Resultado: MC real é 8 pp abaixo da cotação original.

### Verdade 3 — Give/Get não é recusa — é respeito
Exigir contrapartida é profissional. Ceder sem condição destrói valor para todos.

Exemplo: cliente pede desconto. Vendedor aceita se cliente comprometer volume mínimo trimestral. Sem volume, sem desconto. Isso é negociação de adulto.

---

## Diagnóstico em 3 camadas (para aplicar em cliente)

### Camada 1 — Sintoma visível
- O que o cliente reclama ou pede?
- O que você observa na superfície?

Exemplo: "cliente pede mais desconto"

### Camada 2 — Causa operacional
- Qual **comportamento ou processo do cliente** gera o custo oculto?
- Ele fraciona demais? Muda programa sempre? Devolve muito?

Exemplo: "cliente fraciona pedido em 8 entregas/mês, todas urgência"

### Camada 3 — Alavanca de valor
- Que **mudança de comportamento** ou proposta resolve a causa?
- Que contrapartida (Give/Get) converte custo de servir em margem?

Exemplo: "se cliente consolidar em 2 entregas/mês, podemos oferecer 2% de desconto — custo absorvido + economia logística paga o abatimento"

**Regra crítica:** nunca pular direto para Camada 3. Sem mapear causa, qualquer solução é chute.

---

## Decisão sobre a carteira

Após calcular custo de servir real, cada cliente cai em uma categoria:

| Categoria | Perfil | Ação |
|---|---|---|
| Estratégico e rentável | MC alta + custo de servir controlado | **Manter e expandir** |
| Volume sem margem real | Receita alta, mas MC real baixa devido custo de servir | **Requalificar com Give/Get** |
| Margem real negativa | Perde dinheiro atender | **Renegociar ou descontinuar** |

### Tese de valor (modelo de proposta)
> "Se o Cliente X adotar [mudança de comportamento Y], o custo de servir reduz em Z%, e a margem líquida real passa de A para B."

Isso é conversa comercial **profissional**. "Vamos dar desconto pra aumentar volume" é amadorismo.

---

## Métricas que operacionalizam a fórmula

| Métrica | Como calcular | Fonte |
|---|---|---|
| **Receita líquida** | Fat s/IPI, s/devolução | RAF `ABCTOT_LIQ` |
| **MC contábil** | Receita − custo aço (explícito) | RAF `ABCPER_MAR` |
| **MC econômica** | MC contábil + margem oculta | Calculada (ver [[Sistema Operacional Comercial/04 RAF/03 - MC Contábil vs Econômica]]) |
| **Custo de servir** | Soma real dos componentes | RAF `ABCCUS_X_COB` (cuidado com convenção invertida) |
| **Margem líquida real** | MC contábil − custo de servir real | Calculada |
| **MC por cliente** | MC econômica agregada por cliente | Motor Analítico |
| **Ratio receita / esforço** | Receita / nº de urgências+retrabalhos | Motor Analítico |

---

## Aplicação — AFS atual (abr/2026)

### O que funciona
- RAF tem estrutura para calcular margem econômica
- Motor Analítico consome RAF e separa margem oculta por componente
- Gustavo tem visibilidade dos números (29,30% contábil + 6,15 pp oculto = 35,44% econômico)

### O que não funciona
- **Simulador não usa custo de servir** — cotação não considera
- **Vendedor não vê** margem real por cliente no sistema
- **Remuneração não reflete** MC real
- **Conversa com cliente** sobre Give/Get não é sistemática

### Oportunidades imediatas
1. Adicionar **custo de servir por cliente** no Motor Analítico (v2)
2. Relatório mensal **Top 20 clientes por margem líquida real**
3. Conversa cirúrgica com 2-3 clientes identificados como "volume sem margem"
4. Inserir **campo Give/Get** no simulador (Entrega 2 pacote)

---

## Pitch de 3 minutos (estrutura)

Quando precisar convencer cliente da Tese de Valor:

1. **Contexto** — segmento e perfil do cliente (30s)
2. **Diagnóstico** — principal causa de custo oculto (60s)
3. **Proposta** — Give/Get prioritário com número (45s)
4. **Impacto** — resultado financeiro estimado (15s)
5. **Próximo passo** — ação concreta e prazo (15s)

**Checklist de qualidade:**
- [ ] Usou números do custo de servir?
- [ ] Apresentou Give **E** Get?
- [ ] Conectou custo de servir à margem?
- [ ] Proposta é específica, não genérica?

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[10 - Custo de Servir Aplicado]]
- [[Sistema Operacional Comercial/04 RAF/03 - MC Contábil vs Econômica]]
- [[Sistema Operacional Comercial/04 RAF/04 - Margem Oculta (7 componentes)]]
- Vault estratégico: [[Pricing - Precificação]], [[Custo de Servir]]
