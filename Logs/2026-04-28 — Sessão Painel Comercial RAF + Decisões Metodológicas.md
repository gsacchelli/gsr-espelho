---
data: 2026-04-28
tipo: implementação + decisões metodológicas
projeto: Painel Comercial RAF — Etapa B/C/D + Refinamentos
status: Painel multi-aba pronto (DRE, Carteira, Produtos, Evolução); aggregator expandido com cubo OS/Produto/Partida
relacionados:
  - "[[Logs/2026-04-27 — Bloco 1+2 RAF + Painel Estoque + Aggregator Painel Comercial]]"
  - "[[Sistema Operacional Comercial/04 RAF/09 - Critérios de Classificação]]"
---

# Sessão 28/04/2026 — Painel Comercial RAF: Etapa B/C/D + Profissionalização + Decisões Metodológicas

Sessão grande. Fechou o painel comercial em formato apresentável a consultoria, com 4 abas (DRE Gerencial, Carteira, Produtos, Evolução) e tomada várias decisões de metodologia que precisaram ser documentadas no vault. **Pivô importante**: até hoje as decisões metodológicas viviam só em código + CLAUDE.md; agora têm casa permanente em `[[04 RAF/09 - Critérios de Classificação]]`.

## Bloco 1 — Reformulação do Painel Comercial (Etapas B/C/D)

### Etapa B refinada (Carteira)
- Cubo cliente expandido: ano × cliente × gerência × vendedor × op_cat × considerar.
- Layout 60/40: matriz Risco/Joia + tabela + Pareto à esquerda; card cliente com mini-DRE + mix família + sinais YoY à direita.
- Filtro vendedor cascateado da gerência (mudança em gerência → reseta vendedor + popula opções).
- Diagnóstico textual automático no card cliente: Joia / QUEIMA / Decadência / Estável.
- Linha Δ entre MC Total Contábil e MC Total Econômica (resolve confusão visual entre os dois).

### Etapa C completa (Família × Região + Evolução)
- Aba Geografia: heatmap Top 15 Regiões SP × Top 15 Famílias com 4 modos (MC%, Receita, Mix-shift YoY, Gap vs Média).
- Cidades SP via lookup das 44 RGs; UFs fora SP como "Fora SP — UF".
- Aba Evolução refinada: stacked bar por gerência + linha MC%, toggle Mensal/Anual.

### Etapa D iniciada (Profissionalização)
- DRE Comercial → **DRE Gerencial** (terminologia gerencial, não contábil).
- "MC Total" → **Margem de Contribuição** (clássica).
- "Margem Oculta" → **Margem Agregada** (alinha com terminologia interna do Sacchelli).
- "Especiais" / "Texto Livre" padronizados em todos os locais.
- KPIs reformulados: 14 cards em 2 linhas densas (era 5 grupos espaçados verticalmente).
- Ticket médio agora por **OS** (era por linha — gerencialmente errado em distribuidor).

### Aba Produtos — visão estratégica de mix
- Filtros secundários cascateados: Aço, Perfil, Acabamento, Bitola De/Até (numéricos!), Faixa Comprimento, Corte SN, Família.
- Família como select com 200+ famílias do criterios_raf.xlsx.
- Bitola De/Até: filtro por sobreposição de range (não contenção exata).
- Toggle Material **Vendido / Partida** funcional (dois cubos paralelos no aggregator).
- Sub-tab "Clientes" — drilldown: top 50 clientes que compraram o recorte filtrado.
- Botão Exportar CSV (BOM UTF-8 + separador `;` para Excel BR).
- Mix por Atributo (6 charts), Evolução Temporal Top 10 famílias, KPIs do recorte.

## Bloco 2 — Decisões Metodológicas (documentadas em `[[04 RAF/09 - Critérios de Classificação]]`)

### Mudança de critério: Corte SN
**Hoje 28/04**: `ABCPES_CTE > 0` → `ABCCUS_CTE > 0`.

Motivo: alguns serviços de corte (chapa fina, corte sob medida sem subproduto identificado) não geram peso registrado mas geram custo cobrado. Usar custo captura todas as operações financeiramente cortadas.

Implementação: `enriquecer.py::derivar_corte` + 117/117 testes verdes após ajuste.

### Tratamento de Especiais (Opção C)
**Decisão**: linhas com `ABCTIP_PRO=2` viram bucket único `ESPECIAIS`. Aço/Perfil/Acabamento todos = "Especiais". Bitola = "—".

Motivo: descrição de texto livre não codificada; tentar parsear gera ruído visual. Bucket honesto.

**Distinção mantida**: famílias `Não mapeada` e `Produto Fora Padrão` continuam expandidas (são dívida técnica do enriquecimento, não Especiais reais).

### Material Vendido vs Material Partida
**Definição**:
- Vendido: produto que sai. Família via `Familia_Desc`.
- Partida: material consumido do estoque. Família construída como `<TIP> <P> <A>` (sem bitola — agrega range no estoque).

Cubos paralelos no aggregator. Toggle no painel.

### Tabela predominante por OS
Pra KPIs de Pricing (Verde/Amarela/Vermelha/Preta), a OS é classificada pela tabela com maior ValorLIQ entre suas linhas. ~95% das OSs fecham em uma única tabela; aproximação aceitável.

### KPIs renomeados e redefinidos
- "MC Spread" → "Margem Agregada" (terminologia interna Sacchelli)
- "Ticket Médio" agora = Receita / nº OS (era por linha, errado conceitualmente)
- "R$/kg" adicionado = ValorLIQ / Qtd (preço médio do recorte)
- Distinct counts via cubo OS: nº OS, nº NF, nº Clientes

### Padronização "Especiais" em todos os lugares
Em vez de "Texto Livre" / "Especial" / "ESPECIAIS" / outros nomes → SEMPRE "Especiais" / "ESPECIAIS" (família).

## Bloco 3 — Discussão sobre Vault (lição aprendida)

**Contexto**: Gustavo perguntou se eu estava salvando as decisões metodológicas no vault. Resposta honesta: **não**. As mudanças estavam só no código + CLAUDE.md.

**Problema**: daqui a 6 meses, ninguém vai lembrar por que `ABCCUS_CTE` substituiu `ABCPES_CTE`, ou por que MC Agregada bate com Margem Oculta mas tem nome diferente. Os logs do dia capturam o "fato"; o vault em `Sistema Operacional Comercial/` deve capturar a "regra".

**Correção aplicada**: criada nota `[[04 RAF/09 - Critérios de Classificação]]` como fonte da verdade. Toda mudança metodológica futura deve passar por lá ANTES (ou junto com) a mudança no código.

## Para retomar amanhã

Triggers:
- `arrancar fase 2 partida` — Material Partida hoje só usa `<TIP> <P> <A>` sem bitola. Pra ter granularidade igual ao vendido, precisa rodar lookup de bitola padrão no enriquecedor (ou no aggregator).
- `arrancar polimento executivo painel` — header com logo Sacchelli, paleta calibrada, narrativa visual de abertura. Fica útil quando Gustavo precisar mostrar pra Wagner / Duferco / Banco.
- `validar painel completo` — Gustavo precisa rodar `--painel-raf` local com aggregator novo (~8 min) e testar todas as abas com dados de 4 anos.

Outros pendentes:
- DRE Gerencial: filtro vendedor não atinge componentes de custo (ext/fin/etc) — só margens consolidadas. Fix exigiria adicionar dimensões ao cubo_main (custo: tamanho).
- Produtos > Drilldown Clientes: limitado a top 500 × top 10 famílias do `cliente_familia_mix`. Pra cobertura total precisa expor cubo cliente×família completo.
- Material Partida com bitola real: hoje `<TIP> <P> <A>`, sem faixa de bitola. Adicionar requer mexer no enriquecimento.

## Comandos típicos

```bash
# Re-rodar com aggregator novo (cubos OS, Produto, Partida, familia_metadata)
python3 MotorAnalitico/main.py --painel-raf

# Re-enriquecer RAF se mudou critério no enriquecedor (ex: Corte_SN)
python3 MotorAnalitico/main.py --raf-enriquecer all

# Testes do enriquecedor
cd MotorAnalitico && python3 -m raf.test_enriquecer
```
