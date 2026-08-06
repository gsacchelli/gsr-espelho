# Memória do Agente Telegram

Fatos ensinados via /aprender (injetados em todo prompt do agente). Editável à vontade.

- [30/07/2026] WEG é holding com 5-6 razões sociais — sempre buscar cliente com 'contém WEG'.
- [30/07/2026] Gustavo prefere valores em R$ MM e respostas curtas: número primeiro, recorte depois.
- [30/07/2026] "Pendente" sem qualificador = cotações pendentes (vw_cotacoes_pendentes), não pedidos em carteira.
- [31/07/2026] O report diário de pedidos JÁ EXISTE fora do meu alcance: LaunchAgent do macOS `com.sacchelli.briefing-8h` roda `MotorAnalitico/agente/briefing_pedidos.py` seg-sex 8h15 e envia pro Telegram (pedidos do dia anterior por gerência com valor/peso/qtd + acumulado do mês + média/dia útil + ritmo). Só sai depois do 1º pull de pedidos do dia — se o Mac estiver fora da rede AFS às 7h45, atrasa até a janela das 11h/15h. NUNCA criar rotina nova pra isso (nem via /schedule): se perguntarem "cadê o report?", explicar o atraso e conferir `lake/meta/.briefing_8h_ultimo` (data do último envio) e `lake/meta/.pedidos_diario_ultima` (data do último pull).

- [06/08/2026] Vendas = pedidos emitidos, NÃO faturamento (RAF/NF). Todo pedido nasce de uma cotação.
- [06/08/2026] Pedido nasce SEMPRE de uma cotação encerrada como Ganha — não existe pedido sem cotação. Quando o valor de pedidos do dia não bate com o das cotações encerradas do dia, a causa provável é pedido represado em análise crítica ou análise de crédito, liberado em dia posterior (não é erro de dado).
- [06/08/2026] Quando o Gustavo pede a CONVERSÃO do dia, ele quer pedidos emitidos × cotações encerradas — não o win rate só das cotações encerradas naquele dia. Apresentar as duas métricas e explicar o descasamento temporal (o pedido pode vir de cotação fechada em dia anterior).
- [06/08/2026] Se o Gustavo disser que um número está errado, conferir primeiro se a MÉTRICA é a que ele espera (cotação × pedido × faturamento) antes de suspeitar de conexão ou base — em 04/08/2026 fui checar o SQL e o problema era eu ter respondido win rate de encerradas quando ele queria pedidos emitidos.
- [06/08/2026] VOCABULÁRIO da casa (decisão 06/08/2026): 'vendas' = PEDIDO EMITIDO (entrada de pedidos), nunca faturamento. 'Faturamento' = NF faturada (RAF). O rótulo 'Faturamento (vendas)' foi removido do portal e do doc canônico justamente para a palavra não ter dois sentidos.
- [06/08/2026] A liberação do pedido (Pedidos Liberar → Análise Crítica → Aprovação de Crédito) é processo RÁPIDO e não é gargalo — decisão do Gustavo em 06/08/2026 de NÃO medir tempo por etapa. Essas etapas servem só para explicar o descasamento de um dia entre cotação encerrada e pedido emitido; não sugerir instrumentá-las.
- [06/08/2026] O fluxo do pedido é orçamento do cliente → cotação implantada e proposta enviada → negociação opcional → cliente formaliza pedido → cotação encerrada item a item como Ganha → fase Pedidos Liberar (OC, item, prazo, reserva de material) → Análise Crítica (feita pelo vendedor) → se houver pendência financeira, Aprovação de Crédito (financeiro) → impressão na produção.
