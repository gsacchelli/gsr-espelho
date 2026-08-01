---
data: 2026-06-07
tipo: log
status: vigente
projeto: Portal SAC360 (afs-lake)
nota: 6.9/10
---

# Avaliação Portal SAC360 — Painel de 6 especialistas

Avaliação multi-agente do Portal SAC360 (Streamlit sobre o data lake `~/dev/afs-lake`), conduzida por 6 especialistas (Comercial, Estratégia/C-Level, UX/UI, Análise de Dados, Arquitetura de Dados, IA/NLQ) lendo o código e os dados reais + síntese executiva. 7 agentes, ~536k tokens.

## Scorecard

| Especialista | Nota |
|---|---|
| Analista Comercial | 7,5 |
| Análise de Dados / Métricas | 7,5 |
| Design UX/UI | 7,0 |
| Estratégia / C-Level | 6,5 |
| Arquitetura de Dados | 6,5 |
| IA / NLQ (texto→SQL) | 6,5 |
| **Média** | **6,9** |

## Veredito

Cockpit comercial acima da média do mercado de distribuição; convenções de negócio da AFS (faturamento_cimp vs ValorLIQ, faixas, %Preta, metas por gerente) internalizadas com rigor e números que reconciliam. Teto é de **altitude executiva**, não de engenharia: diz com precisão ONDE sangra, mas não diz POR QUE caímos (variance volume×preço fora da vista de conselho), QUEM age (sem meta/ranking por vendedor; alertas sem dono/cifra) nem se posso CONFIAR no número de hoje (zero indicador de frescor; RAF 9 dias defasado; 3 win rates na mesma tela). Falta a camada que transforma dado em tese.

## Temas transversais

1. **Diagnóstico forte, prescrição fraca** (4 de 6) — não fecha o ciclo alerta→dono→ação→R$ recuperável. Inteligência é mural, não fila de trabalho.
2. **Falta causa-raiz e narrativa de board** — queda de 24% como número único, sem variance bridge (volume×preço) nas páginas estratégicas; insight-âncora escondido em Pedidos (só kg).
3. **Confiança nos dados é a lacuna mais perigosa** — 3 win rates (18,7% / 24,2% / 40,3%) sem reconciliação; sem selo de frescor (RAF até 29/05, portal aberto em 07/06).
4. **Gestão de performance individual ausente** — PGA só por gerente; sem meta/atingimento/ranking por vendedor.
5. **Sazonalidade contraditória** — Forecast projeta sazonal (jan-mai ≈ 43-45%), Meta rateia ÷12 (41,7%); penaliza atingimento YTD ~3-7pp.

## Lacunas de severidade ALTA (com evidência)

- **Sem metas/ranking por vendedor** (Comercial) — PGA só por gerente; pagina_vendedores é 360 manual de 1 por vez.
- **Funil cotação→pedido→faturamento não conciliado** (Comercial) — 3 estágios em 3 páginas/fontes; sem Win Rate Real no portal (legado HTML tem).
- **Causa-raiz volume×preço ausente nas páginas estratégicas** (Estratégia) — único Variance Bridge está em Pedidos, só itens em kg.
- **Sem priorização risco×oportunidade dimensionada** (Estratégia) — nenhum quadrante gap×reversibilidade por cliente/segmento/região/família.
- **Tabelas sem cores de faixa** (UX) — FAIXA_CORES só em gráficos; 16 st.dataframe monocromáticas (fmt_df só formata string).
- **Sem headline de síntese na 1ª dobra** (UX) — páginas abrem em KPIs, sem one-liner de leitura.
- **Dois+ win rates sem reconciliação** (Dados) — vw_cotacoes_funil dá 18,7% (2025) vs ajustado 40,3% na mesma página.
- **Sem selo de frescor/defasagem** (Arquiteto) — MAX(ABCDAT)=2026-05-29; portal não avisa.
- **Conexão cacheada (@st.cache_resource) segura banco antigo após rebuild** (Arquiteto) — make gold faz unlink do .duckdb; handle fica órfão.
- **Catálogo declara views inexistentes** (Arquiteto) — lista_clientes, fases_producao sem Parquet; build só imprime ⊘.
- **Zero validação de contrato no gold** (Arquiteto) — testes só cobrem enriquecimento.
- **IA: exemplos por recência (sem RAG), sem memória conversacional, sem validação semântica** (IA).

## Quick wins (alto impacto / baixo esforço)

- Selo de frescor no topo (MAX ABCDAT + mtime + defasagem dias)
- Reconciliar 3 win rates numa cascata explicada
- Inteligência vira fila: alerta com ação + R$ recuperável + dono, ordenado por impacto, com Upside total
- Invalidar conexão DuckDB por mtime + botão Recarregar dados
- Ranking de fechamento por gerente vs meta no Forecast
- Colorir tabelas-chave com FAIXA_CORES + thresholds

## Apostas (alto impacto / esforço maior)

- Metas e ranking por vendedor (atingimento, gap R$, semáforo)
- Página Funil end-to-end Cotado→Pedido→Faturado + Win Rate Real
- Quadro "Gap até a meta — onde está e quanto é reversível" + Variance Bridge YoY (volume×preço×mix)
- Camada de IA que valida e explica (2ª chamada Haiku) + memória conversacional + RAG de exemplos
- Suite de testes de contrato do gold + governança schema/lineage

## Roadmap

**Agora:** selo de frescor · reconciliar win rates · invalidar cache + recarregar · Inteligência com dono/R$/ação · corrigir base/rótulo de %Preta.
**Próximo:** metas/ranking por vendedor · meta sazonalizada (não ÷12) · Variance Bridge YoY · test_gold.py no CI · headline de síntese + tabelas coloridas · IA com validação semântica + RAG.
**Depois:** Funil end-to-end · Gap-até-a-meta reversível · simulador what-if no Forecast · cohort/churn/RFM em Clientes · pipeline pendente + coverage · página Board (one-pager PDF).

## Decisão

Começar pelo bloco **Agora** (confiabilidade) — pequenos esforços que protegem a credibilidade de todos os números. Implementação iniciada em 2026-06-07.
