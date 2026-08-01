---
data: 2026-06-08
tipo: log
status: vigente
projeto: Portal SAC360 (afs-lake)
---

# Portal SAC360 — evolução pós-avaliação + IA v2 + decisão de arquitetura

Sessão dando sequência à [avaliação dos 6 especialistas (2026-06-07)](2026-06-07%20—%20Avaliação%20Portal%20SAC360%20(painel%206%20especialistas).md). Praticamente todo o roadmap foi entregue + uma repaginada da IA. Tudo commitado/pushado no repo `~/dev/afs-lake` (branch main).

## Decisão de arquitetura: lakehouse no DuckDB (manter)

Pergunta: data lake ou data warehouse para o portal? **Resposta: lakehouse — manter o que existe.**
- O uso (BI, KPIs definidos, IA texto→SQL, reconciliação) é caso de **warehouse**; mas o volume é pequeno (~260k linhas RAF, fonte única Softcomp).
- **Não migrar para DW cloud** (Snowflake/BigQuery) — custo/complexidade sem ganho no volume atual. DuckDB local entrega.
- **bronze/silver** = camada "lake" (ingestão flexível, histórico cru, enriquecimento — bom p/ novas fontes: orçamento de despesas, OC).
- **gold** deve evoluir como **warehouse**: modelo dimensional limpo, **definição única de cada métrica** (origem de muitos bugs corrigidos), governança (`test_gold.py` iniciou), camada semântica/dicionário (iniciada no prompt da IA).
- Migrar p/ DW cloud só se: multiusuário concorrente pesado, tempo real, ou volume 100×.

## Bloco "Agora" (confiabilidade) — feito
- Selo de **frescor** dos dados na sidebar (MAX ABCDAT + defasagem em dias) + Forecast marcado "YTD parcial".
- **Win rates reconciliados** na Cotações (cards por ano = ajustado, mesma fonte; declarativo no tooltip). Fim do 18,7% vs 40,3% sem explicação.
- Conexão DuckDB **chaveada por mtime** (não segura banco reconstruído) + botão "🔄 Recarregar dados".
- **Inteligência** virou fila de ação: cada alerta com ação + R$ em jogo + dono, ordenado por R$.
- **%Preta** rotulada "(sobre líquido)".

## Bloco "Próximo" — feito
- **Meta sazonalizada** (anual × fração sazonal dos meses, não ÷12) — Metas passou a bater com o Forecast (atingimento Venda 73,3% / MC 52,6%).
- **Ranking por vendedor** vs meta-proxy (rateio da meta do gerente pela participação em ano-1), com semáforo.
- **Variance Bridge YoY** (Volume(t) × Preço) na Visão Geral — queda 2026 = 89% volume, 11% preço.
- **IA**: RAG de exemplos (similaridade), insight/validação semântica (2ª chamada Haiku), atributos físicos do aço (Aco_Padrao, bitola, corte, perfil/acab).
- **Tabelas coloridas** (semáforo MC%/%Preta/atingimento) + **headline de síntese** dinâmico na Visão Geral.
- **test_gold.py** de contrato no `make ci` (views, colunas, GER_MAP vs grafias reais, aço+spread=MC, metas reconciliam).
- **Peso (t)** com YoY nos KPIs da Visão Geral.

## Bloco "Depois" — feito
- **Customer Revenue Bridge** (Clientes): novos/perdidos/expansão/contração YoY. Achado: queda 2026 é R$ 47,5M de **contração** vs 12,5M de churn → clientes compram menos, não somem.
- **Cohort de retenção por safra** (Clientes): base sticky ~90% em anos completos; 2026 abaixo do proporcional.
- **Funil end-to-end** (página nova): Cotado→Disputa→Ganho→Pedido→Faturado + **Win Rate Real** (Pedido/Cotado = 20%) + por gerência.
- **What-if no Forecast**: alavancas (contração/churn/disputa-preço) → projeção vs meta. **Gap por gerência reversível**: gap R$79M concentrado em Felipe/Guarulhos (R$77,5M); Odair já acima da meta; pools cobrem 200%+.

## Página Pedidos — entrada diária
- **Mapa calendário** (mês × dia) da entrada de pedidos, métrica selecionável (valor/peso/itens).
- Quadro **média diária por mês** (MoM/YoY/YTD) + **linha 2026 vs 2025 + gap** + **acumulado diário** + **por gerência** + **heatmap YoY gerência × mês**.
- **Bug corrigido**: o YoY comparava 2026 parcial vs 2025 ano cheio (−4,4% falso) → restrito ao mesmo período (−11,2% real). Entrada de pedidos cai menos que faturamento (gap legítimo: pedido por data de emissão ≠ NF + saldo).

## IA v2 — repaginada (Relatórios IA / SQL)
- **Multi-step**: planner (Haiku) decompõe perguntas multi-parte em sub-perguntas + síntese.
- **Memória conversacional robusta**: `_resolver_pergunta` reescreve o refinamento numa pergunta COMPLETA (incorpora o thread) ANTES de gerar — "no mês de maio" vira "itens 4140 R L barras SP em maio". Indicador "🔁 interpretado como". Botão "Nova conversa".
- **Apresentação enxuta**: resposta em prosa (💡) primeiro, gráfico+tabela, SQL recolhido em expander; datas dd/mm/aaaa; $ escapado (bug LaTeX).
- **Dicionário de valores** no prompt com os **gotchas entre tabelas**: CORTE em 3 convenções (RAF 'Sim'/'Não', pedidos BOOLEAN, cotações 'sim'/'não'); perfil/acab (pedidos perfil_canon/acab_canon agrupado, cotações *_legivel, RAF códigos em Familia_Desc); unidades com espaços (TRIM); UF; nomes EXATOS de gerência.
- **Bug grave corrigido**: a IA gerava `ILIKE '%Felipe%' OR '%Fuscão%'` (precedência quebrada) → R$ 64,3M errado vs R$ 7,8M real. Agora usa nome exato com `=`.
- **Distinção VENDA × FATURAMENTO**: "vendido/pedido" → pedidos_enriquecidos (preço de venda); "faturado/NF" → RAF. O lake já tinha a venda em pedidos com colunas limpas.

## Outros ajustes de UX
Renomes (Vendas→Faturamento (RAF); Consultas→Relatórios IA/SQL; Pedidos abaixo de Faturamento no menu); KPIs 3+3 (fim do truncamento, via agente de design); MC Total R$ + breakdown do spread (Corte/Financeiro/Externo/Comissão/Certificação/Interno; Comercial+Logístico = 0 até o orçamento); observação de que a MC usa **custo de ENTRADA do aço**; DRE sem %Preta/Itens (já em Indicadores); Indicadores mostra o período; explicação do HHI.

## Pendentes
- Ingerir **Orçamento de Despesas** → destrava spread Comercial+Logístico (hoje 0) e o controle de despesas nas Metas.
- IA: **guardrail ativo** (validar nome de cliente/gerência contra a lista real antes de rodar).
- Evolução do gold para modelo dimensional + camada de métricas canônica (disciplina de warehouse).
- Manter o **RAF atualizado** (em 08/06 estava ~10 dias defasado — o selo de frescor avisa).

Ver memórias: [[project_avaliacao_portal]], [[project_metas_pga]], [[project_metricas_faturamento]].
