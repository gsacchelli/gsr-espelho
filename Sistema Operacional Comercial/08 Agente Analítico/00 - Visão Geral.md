---
tags: [agente, sistema-operacional, sacchelli]
status: fundação entregue — 12 funções canônicas
ultima_atualizacao: 2026-05-14
---

# 00 — Agente Analítico Sacchelli (Visão Geral)

Camada de consulta em linguagem natural sobre os dados comerciais da AFS. Lê os cubos OLAP já gerados pelo Motor Analítico (RAF, Cotações, Pedidos, Estoque) + drilldown nos enriquecidos quando precisa de detalhe linha-a-linha. Responde perguntas como "qual o material mais vendido na semana?", "qual o excedente do 1045 R F 304,80mm?", "vendas pra WEG em 2026?".

## Propósito

Substituir a operação de abrir planilha + filtro + tabela dinâmica + gráfico por uma consulta de 5 segundos. Foco no diretor comercial usando no dia-a-dia — sem precisar de TI, BI ou analista intermediário.

**Não substitui** o Motor Analítico nem os painéis HTML. É **camada de leitura** sobre os mesmos dados que o motor já produz.

## Arquitetura

```
Pergunta NL
    ↓
[Claude (eu, no chat ou app cloud)] roteia → função canônica + parâmetros
    ↓
[MotorAnalitico/agente/] executa função
    ├── carregador.py — parser dos *_data.js + cache RAM
    └── analises/ — funções determinísticas
    ↓
DataFrame pandas com resultado
    ↓
[Claude] formata em prosa pt-BR
```

**Determinismo:** funções canônicas em Python puro sobre os cubos. Mesmo input → mesmo output. Sem LLM gerando código pandas a cada pergunta (caro, inconsistente, difícil de testar).

**Portabilidade:** funções não dependem do Claude Code. Mesma biblioteca vai rodar no app cloud (fase 2) sem mudança — só substitui a camada de roteamento por uma chamada HTTP.

## Fontes consumidas

| Fonte | Arquivo | Conteúdo | Granularidade |
|---|---|---|---|
| `window.PD` | `03_Ferramentas/painel_data.js` | RAF (vendas + estoque) | ano×mês (cubos) + SKU (estoque) |
| `window.CD` | `03_Ferramentas/cotacoes_data.js` | Cotações | ano×mês + clientes + aging |
| `window.PED` | `03_Ferramentas/pedidos_data.js` | Pedidos emitidos | ano×mês + dia + cross-check com cotação |
| Enriquecido pendentes | `02_Derivados/Cotacoes/CotacoesPendentes_enriquecido.xlsx` | Drilldown linha-a-linha | item de cotação |
| Enriquecido encerradas | `02_Derivados/Cotacoes/CotacoesEncerradas_enriquecido.xlsx` | Drilldown linha-a-linha | item de cotação |

**Princípio:** cubos pra agregação (95% das perguntas). Enriquecidos só pra drilldown (listas detalhadas, pricing curve).

## Estado atual — Fase 1 (esta semana)

**12 funções canônicas entregues** cobrindo Vendas, Cotações, Estoque, Pedidos, Pricing. Ver `01 - Funções Canônicas.md`.

Modo de uso atual: Gustavo pergunta no chat com Claude Code, Claude roteia para a função certa.

## Roadmap

**Fase 2 (futuro — não escopado ainda):** app cloud com Claude API roteando + endpoint HTTP. Funções canônicas viajam intactas.

**Fase 3 (futuro):** integração com base SQL espelho do Softcomp (tempo real, sem dependência de export Excel).

## Princípios de design

1. **Resposta determinística** — sem LLM gerando query a cada pergunta. Função canônica testável e reusável.
2. **DataFrame como contrato** — toda função retorna `pd.DataFrame` ou `dict`. Camada de formatação é separada.
3. **Cubo primeiro, enriquecido só quando necessário** — performance + consistência com painéis.
4. **Cache RAM module-level** — primeira consulta carrega (~3s PD), próximas são instantâneas.
5. **Tolerância semântica** — bitola 304,20 ≈ 304,80 (catálogo polegada), "WEG" pega 5 razões sociais. Inputs do usuário não precisam ser exatos.
6. **Caveats documentados** — engenheirados, PU em R$/peça vs R$/kg, orçamento prévio. Ver `02 - Convenções e Caveats.md`.

## Onde vive o código

```
MotorAnalitico/
└── agente/
    ├── __init__.py
    ├── carregador.py          — leitura dos *_data.js + enriquecidos com cache
    ├── periodos.py            — resolver textual: 'ytd', 'mes_anterior', 'ultimos_12m' etc.
    └── analises/
        ├── vendas.py          — top_materiais, vendas_cliente
        ├── cotacoes.py        — listar (drill), conversao, perdas_por_preco, cotacoes_aging
        ├── estoque.py         — cobertura, excedente, materiais_parados
        ├── pedidos.py         — pedidos_semana, ajustes_pos_fechamento
        └── pricing.py         — pct_preta_vendedor, preco_para_win_rate
```

## Notas de cabeceira pro Claude futuro

- **CLAUDE.md no repo** é fonte da verdade pra schema do RAF/Cotações/Pedidos/Estoque. Não tentar reinventar.
- **Logs em `GSR/Logs/`** narram a sessão de construção e contêm achados que não estão no código.
- **Sempre validar bugs com auditoria do cubo** quando o número não bater com benchmark (ex: bug do `valor_orc_previo` zerado descoberto auditando Denilson — ver log 2026-05-14).
