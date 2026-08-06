---
data: 2026-08-06
tipo: processo
fonte: Gustavo (ensinado ao Flori via Telegram, 06/08/2026)
---

# Fluxo do Pedido — do orçamento do cliente à produção

Processo real da AFS, contado pelo Gustavo. Complementa a regra canônica **"pedido nasce sempre de uma cotação encerrada como Ganha"** e explica ONDE o pedido pode ficar represado.

## As etapas

1. **Orçamento do cliente** chega por e-mail, WhatsApp ou telefone.
2. **Vendedor implanta a cotação** no Softcomp e envia a proposta padronizada.
3. **Negociação** (opcional).
4. **Cliente formaliza o pedido** — formal (OC), verbal ou aceite na própria proposta.
5. **Vendedor encerra a cotação item a item como "Ganhou"** — é o que faz o pedido existir.
6. **Fase "Pedidos Liberar"** — preenchimento de nº da OC, item, código, prazo e reserva de material.
7. **Análise Crítica** — liberação feita pelo VENDEDOR.
8. **Aprovação de Crédito** — só quando há pendência financeira; o financeiro reavalia limite e pendências.
9. **Impressão na produção** — se crédito ok e sem bloqueio, vai direto da Análise Crítica para cá.

## Por que isso importa para a análise

- **O represamento tem DUAS portas, não uma**: pode travar na Análise Crítica (vendedor) ou na Aprovação de Crédito (financeiro). Ao explicar divergência entre cotações encerradas e pedidos emitidos no mesmo dia, dizer qual.
- **Explica o descasamento temporal**: pedido emitido hoje pode vir de cotação ganha em dia anterior, liberada só agora — foi o que se mediu em 06/08 (25% do valor dos pedidos de 05/08 vinha de cotação fechada no dia anterior).

## O que o SAC360 enxerga (e por que basta)

O lake **não** enxerga as etapas 6-8: `vw_pedidos.status` só tem `Normal / Abortado / Encerrado`, e `fases_producao` é o cadastro de fases INDUSTRIAIS (TT, certificação, embalagem). O pedido só aparece nos dados depois de emitido.

**Decisão do Gustavo (06/08/2026): não medir.** A liberação é processo RÁPIDO — não é gargalo, e instrumentar etapa que não trava é medição sem decisão do outro lado. Nada a pedir ao Nelson aqui.

O que **fica** dessas etapas para a análise: elas explicam o descasamento de UM DIA entre cotação encerrada e pedido emitido (o pedido de hoje pode vir de cotação ganha ontem, liberada hoje de manhã) — medido em 06/08: 25% do valor dos pedidos de 05/08 vinha de cotação fechada em 04/08. É explicação de timing, não sintoma de problema.
