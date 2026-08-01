---
data: 2026-07-14
tipo: log
status: vigente
projeto: Portal SAC360 (afs-lake)
---

# Regras de negócio oficializadas + Estágio 5 da migração

Sequência da auditoria de 11/07 (`06_Docs/Auditoria_Ecossistema_SAC360_2026-07-11.md`). Decisões do Gustavo em 13-14/07, todas codificadas em `MotorAnalitico/definicoes.py` e espelhadas em `Sistema Operacional Comercial/01 Sistema de Dados/Definições Canônicas de Negócio (SAC360).md`.

## Decisões (Gustavo)

1. **Comissão de agentes dobra no preço** (agente ≠ representante com carteira); exceções: Açotec SC/RP e exportações. A conta "COMISSÕES REPRESENTANTES" do razão = pagamento da mesma comissão do RAF → estava contada 2× no DRE (**Resultado YTD corrigido: +R$ 213k → R$ 15,85M / 17,59% líq**). Monitor permanente na aba Pricing (conformidade 100% na estreia).
2. **Mês fechado**: DRE/Despesas só consideram mês com RAF **e** despesas fechados (despesas fecham no mês seguinte; parcial ignorado com aviso). Unificou as duas páginas; "Consumo do orçado" honesto = **98,5%** (era 50,1% com a régua torta).
3. **Spread DDV/LOG real vem do razão** (não do OrcamentoAnual, que fica aposentável): DDV = estrutura comercial s/ comissão de agentes, LOG = logística c/ rateio CD; correção por unidade×mês fechado; mês aberto usa cobrado como proxy. Mata a regra temporária de 27/04 (viés ~R$ 189k/sem. na MC).
4. **Rateio do CD Jacareí** é pelo % do PGA e deve virar **editável** (compensações manuais) com trava de soma = 100% — implementação em curso (config YAML validada no build).
5. **Estágio 5 antecipado**: os painéis HTML congelados já não eram usados → aposentados HOJE.

## Auditoria do DRE (resumo)

Print de junho do Gustavo reproduzido ao centavo; cascata/lentes/rateios reconciliam com diff zero; achados: dupla contagem de comissão (corrigida), duas bases de % na mesma página (3,88% venda × 3,77% total — expander de conferência criado; no YTD o comercial real está em ~3,3%, ABAIXO do 3,70% cobrado), piso de mês parcial. DRE aprovado para o Montar Relatório com 4 notas de rodapé embutidas + visão mensal com média móvel 3M.

## Estágio 5 — aposentadoria (migração 100%)

`Painel_Comercial_RAF.html` e `Painel_Cotacoes.html` → `Arquivo/paineis-aposentados-2026-07/`; 174 MB de `*_data.js` deletados; flags `--painel-*` e 4 steps do manifesto removidos do motor; Makefile enxuto. O plano de 02/07 (portal hub único) está **concluído**: um modelo, uma cadeia (bruto → motor → silver → gold → portal), um hub. Ficam como apoio: Simulador de Precificação e Painel de Estoque (HTML).

## Aberto

- Rateio CD editável (YAML + validação) — em implementação.
- Spread DDV/LOG no gold — em implementação (vw_spread_ddvlog + MC ajustada).
- Gate 0 Softcomp (Francisco/Nelson) — parado desde junho; destrava a automação da extração.
