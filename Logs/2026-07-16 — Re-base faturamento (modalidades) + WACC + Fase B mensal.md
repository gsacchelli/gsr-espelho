---
data: 2026-07-16
tipo: decisão + execução
projeto: Portal SAC360 (afs-lake)
---

# Re-base do faturamento + WACC + Fase B mensal

## Decisões do Gustavo (16/07)

1. **RE-BASE DO FATURAMENTO — a maior correção semântica do sistema.** As Op_Categoria do RAF são TODAS vendas: "Consumo Próprio" = venda p/ cliente que consome (MAHLE, Suzano — confirmado nos dados: 100% clientes reais); "Outros" = faturamento de consignação; "Exportação" = venda externa; "Beneficiamento" = serviço vendido (HKM, corte WEG TGM). → **Base única de faturamento = tudo ex-Sucata/Devolução = R$ 117,66M YTD = idêntica à contábil** (teste de ouro: igualdade ao centavo, mês a mês, no CI). O rótulo "operações não-venda" morreu; agora são **modalidades de venda**.
2. **Margem confiável**: beneficiamento tem receita real mas MC fictícia no Softcomp (custo do material DO CLIENTE no custo; preço só do serviço) → flag `margem_confiavel=FALSE`; análises de margem/%Preta excluem, receita inclui (custo real do serviço já está no razão de Produção). %Preta re-baseado: 16,27% YTD; MC 31,66%.
3. **Metas PGA** comparam contra o faturamento total (PGA aprovado sobre faturamento total).
4. **WACC** (build-up simplificado, praxe p/ empresa fechada): Ke = SELIC 14,25% + spread 5,0% = 19,25%; Kd observado do DUO ×(1−34%); pesos do balanço → **WACC ≈ 18,7%**. ROIC 30,4% ⇒ **spread +11,7pp de criação de valor**. ⚠ Para valuation externo é PISO (sem prêmio de tamanho/iliquidez).

## Execução

- **Balanços patrimoniais MENSAIS** (dez/25→jun/26) parseados de PDF → Fase B mensal: capital de giro, dívida líquida (caixa líquido de R$ 46,6MM), DSO/DIO/DPO, **ciclo de caixa subiu 227→352 dias jan→jun** (estoque), FCO/FCL mensais, ROIC×WACC com semáforo. Mistério da data resolvido: header "01/06/2026" era a posição de 30/06 (bate ao centavo).
- Painel Executivo (Diretoria): **19 dos 20 indicadores** pedidos, mensais (falta lucro líquido pós-IR — provisão mensal com a contabilidade).
- Conciliação DUO: receita 6/6 meses ao centavo; despesas por conta contábil (de-para grupo+subconta+unidade), causas conhecidas documentadas (créditos fiscais; aluguel holding; timing comissões).

## Lição de método (pergunta do Gustavo)

O caso Consumo Próprio expôs um risco de classe: **rótulos herdados do sistema podem significar outra coisa no negócio**. Disparada auditoria semântica de TODAS as definições essenciais (derivações do motor, mapeamentos, convenções de sinal) com lista de premissas implícitas para o Gustavo confirmar. Resultado → nota própria.


## Adendo 17/07 — decisões da auditoria semântica

- **Áreas 21/22/26 do razão** = despesas reais com trâmite de aprovação do Wagner → linha própria no DRE ("Despesas c/ aprovação Diretoria", −R$ 1,42M jan–jun); capex real = grupo contábil 1. **Área 10 = RH corporativo.**
- **Cadastro TiposNF** incorporado como fonte de referência (`01_Brutos/TiposNF/`). Alerta: tipo 47 "VENDA ESPECIAL" marcado NÃO USAR faturou R$ 282k em 2026 — checar com fiscal/GA.
- **Plano de saúde**: gap orçado×realizado da Unimed (385k×3k) é esperado — hoje só funcionários muito antigos têm benefício; novo acordo com a **Amil** previsto. Quando fechar, o realizado de assistência médica passa a rodar próximo do orçado.
