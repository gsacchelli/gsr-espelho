---
tipo: armadilha-analítica
domínio: cotações
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [inbound, outbound, erp, armadilha]
---

# 01 — Inbound vs Outbound (ficção do ERP)

## O problema

**Softcomp não distingue** cotação de demanda inbound (cliente mandou e-mail/WhatsApp/ligou) de cotação outbound (prospecção ativa do vendedor).

**100% das cotações são lançadas manualmente pelo vendedor** no ERP.

---

## Consequência analítica

### Interpretação errada
"Vendedor aceita muita cotação ruim — precisa melhorar filtragem de leads."

### Interpretação correta
Não existe "filtragem" porque não existe inbound com lead ranked. Toda cotação é **iniciada pelo vendedor** com **esforço normal de cotação**.

Quando motor mostra "Cotação somente para orçamento prévio" como principal motivo de perda:
- ❌ "Vendedor não filtra lead"
- ❌ "Pipeline sombra de cotação fantasma entrando no funil"
- ✅ **"Vendedor SABIA que aquele cliente ia cotar só para comparar, e ainda assim cotou com esforço normal"**
- ✅ **É um problema de DISCIPLINA DE PRIORIZAÇÃO e custo de servir, não de filtragem**

---

## Alavanca proposta — Flag de cliente-tabelista

Criar critério automatizado:

**Cliente-tabelista** = cliente com:
- **>70% das cotações encerradas como "orçamento prévio"**
- **E <10% de conversão nos últimos 12 meses**

Esses clientes recebem **atendimento industrializado**:
- Tabela automática
- Zero análise de engenharia
- Zero customização
- Cotação em 5 minutos, não 30

**Libera tempo do vendedor para oportunidades reais.** Alavanca de ROI mais barata identificada.

Ver [[04 - Cliente-Tabelista (flag proposta)]].

---

## Implicação para ferramentas

### Relatórios de funil
Não reportar "conversão inbound vs outbound". Reportar:
- **Conversão global** (Ganhou / Total acionável)
- **Por vendedor**
- **Por região**
- **Por perfil de cliente**

### Dashboard de cotações
Destacar **tipo de cliente** (tabelista vs regular vs projeto), não origem da cotação (que não é confiável).

---

## Implicação para remuneração futura

Se remuneração virar atrelada a "qualidade de venda" (proposta — ver [[02 Precificação/07 - Tabelas e Alçadas]]), não usar "cotação inbound" como proxy de qualidade. Usar:
- Aderência à tabela
- Cobrança de juro
- Custo de servir baixo

---

## Conexões

- [[00 - Visão Geral Cotações]]
- [[02 - Motivos de Encerramento]]
- [[03 - Orçamento Prévio vs Projeto Real]]
- [[04 - Cliente-Tabelista (flag proposta)]]
- [[01 Sistema de Dados/04 - Qualidade de Dados]]
