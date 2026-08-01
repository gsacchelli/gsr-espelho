---
tipo: proposta-não-implementada
domínio: cotações
criado: 2026-04-17
última-revisão: 2026-04-17
status: proposta
tags: [tabelista, flag, automatização, eficiência]
---

# 04 — Cliente-Tabelista (flag proposta)

## Status

**Proposta — não implementada.**

Oportunidade de implementação no Motor Analítico v2 ou via relatório específico.

---

## Conceito

**Cliente-tabelista** = cliente que usa AFS como **referência de preço** para comprar de outro fornecedor, sem intenção real de fechar negócio.

Ver contexto em [[03 - Orçamento Prévio vs Projeto Real]] (Perfil A).

---

## Critérios de classificação automática

```
Cliente-tabelista = cliente que nos últimos 12 meses tem:
  - >70% das cotações encerradas como "orçamento prévio"
  - E <10% de conversão (cotação → pedido)
  - E valor cotado > R$X (significativo, não ruído de 1-2 cotações)
```

Ajustar thresholds conforme realidade observada.

---

## Tratamento proposto

### Cotação
- **Tabela automática** — sistema gera preço com base em tabelas vigentes
- **Zero análise de engenharia** — não personalizar
- **Zero customização** — padrão-padrão
- **Tempo: 5 minutos** vs 30+ minutos de cotação normal

### Relacionamento
- Vendedor mantém relação cordial
- Sem investimento de tempo adicional (visitas, customização)
- Se cliente quiser algo especial, **precifica premium**

### Operação
- Time comercial **não perde tempo** em cotação industrializada
- **Tempo liberado** vai para oportunidades reais

---

## Benefícios esperados

### Quantitativos
- Redução de tempo de vendedor em cotações industrializáveis: ~30-50%
- Tempo liberado: ~10-20 horas/semana por vendedor (estimativa)
- Impacto: mais atenção em Perfil B (projetos) e Perfil de cliente real

### Qualitativos
- Vendedor não se frustra com cliente-tabelista (sabe que é assim)
- Cliente-tabelista continua recebendo serviço (só sem o "tratamento premium")
- Cultura de priorização

---

## Riscos

### 1. Classificação errada
Cliente que era "tabelista" por circunstância (crise, período difícil) pode mudar. Industrializar pode perder oportunidade futura.

**Mitigação:** revisão trimestral da classificação. Se cliente volta a cotar com frequência aumentada, reclassificar.

### 2. Cliente percebe e reclama
"Por que antes vocês eram atenciosos e agora nem me retornam?"

**Mitigação:** industrializar **sem parecer desdém**. Cotação em 5min via sistema, comunicação cordial.

### 3. Classificação como desculpa
Vendedor pode marcar cliente como "tabelista" para não se esforçar.

**Mitigação:** classificação **automática** (não manual). Revisão pelo gerente antes de ativar.

---

## Implementação técnica (proposta)

### Opção A — Dashboard analítico
Motor Analítico v2 gera **lista mensal** de clientes candidatos a tabelista.
Gerente comercial revisa e aprova caso a caso.
Vendedor consulta antes de investir tempo em cotação.

### Opção B — Flag no Softcomp
Campo customizado no cadastro de cliente.
Sistema alerta vendedor quando abre cotação de cliente-tabelista.
Cotação sugerida automaticamente com tabela vigente.

### Opção C — Meio-termo
Flag visual em planilha auxiliar usada pelo time.
Cada vendedor consulta antes de cotar.
Atualizada mensalmente pelo gerente.

---

## Próximos passos

1. **Validar thresholds** com análise histórica
2. **Rodar lista experimental** — quais clientes seriam classificados hoje?
3. **Revisar caso a caso** com gerentes
4. **Piloto com 1-2 vendedores** por 30 dias
5. **Medir impacto** (tempo liberado, qualidade de cotação residual)
6. **Escalar ou ajustar**

---

## Conexões

- [[00 - Visão Geral Cotações]]
- [[01 - Inbound vs Outbound (ficção do ERP)]]
- [[03 - Orçamento Prévio vs Projeto Real]]
- [[Sistema Operacional Comercial/02 Precificação/10 - Custo de Servir Aplicado]]
- Vault estratégico: [[Cliente Ideal]]
