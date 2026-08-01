# Memória do Agente Telegram

Fatos ensinados via /aprender (injetados em todo prompt do agente). Editável à vontade.

- [30/07/2026] WEG é holding com 5-6 razões sociais — sempre buscar cliente com 'contém WEG'.
- [30/07/2026] Gustavo prefere valores em R$ MM e respostas curtas: número primeiro, recorte depois.
- [30/07/2026] "Pendente" sem qualificador = cotações pendentes (vw_cotacoes_pendentes), não pedidos em carteira.
- [31/07/2026] O report diário de pedidos JÁ EXISTE fora do meu alcance: LaunchAgent do macOS `com.sacchelli.briefing-8h` roda `MotorAnalitico/agente/briefing_pedidos.py` seg-sex 8h15 e envia pro Telegram (pedidos do dia anterior por gerência com valor/peso/qtd + acumulado do mês + média/dia útil + ritmo). Só sai depois do 1º pull de pedidos do dia — se o Mac estiver fora da rede AFS às 7h45, atrasa até a janela das 11h/15h. NUNCA criar rotina nova pra isso (nem via /schedule): se perguntarem "cadê o report?", explicar o atraso e conferir `lake/meta/.briefing_8h_ultimo` (data do último envio) e `lake/meta/.pedidos_diario_ultima` (data do último pull).
