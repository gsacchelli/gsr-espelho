---
tipo: taxonomia
domínio: estoque
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [bitola, faixa, sn, taxonomia]
---

# 02 — Faixas de Bitola

## Propósito

A **Faixa de Bitola** é um dos componentes da Família Canônica (ver [[01 - Família Canônica]]). Ela agrupa SKUs de diferentes diâmetros em **faixas de comportamento comercial similar** — mesma família de uso, mesma margem aproximada, mesma logística.

---

## Tabela oficial (abr/2026)

| S/N | Mín (mm) | Máx (mm) | Label |
|-----|---------:|---------:|-------|
| 1 | 12.7 | 101.6 | 12.7-101.6mm |
| 2 | 101.61 | 203.2 | 101.6-203.2mm |
| 3 | 203.21 | 230 | 203.2-230mm |
| 4 | 230.01 | 355.6 | 230-355.6mm |
| 5 | 355.61 | 558 | 355.6-558mm |
| 6 | 558.01 | 800 | 558-800mm |

**Bitolas fora dessas faixas:** família "Fora de Padrão" — visível para higiene de portfolio.

---

## Lógica das faixas

### Por que essas quebras?
As faixas foram desenhadas para refletir **comportamento comercial e operacional** similar dentro de cada faixa:
- **Faixa 1 (12.7-101.6mm):** barras finas/médias — maior volume, maior rotatividade, menor margem unitária
- **Faixa 2 (101.6-203.2mm):** média-grossa — mix comum, margem média
- **Faixa 3 (203-230mm):** transição — pouca quantidade, margem pode ser melhor
- **Faixa 4 (230-355mm):** grossa — clientes específicos (engrenagens, grandes peças)
- **Faixa 5 (356-558mm):** muito grossa — especialistas
- **Faixa 6 (558-800mm):** extra — raros, alto valor unitário

### Implicação estratégica
Cada faixa tem **cliente-alvo e margem-alvo diferentes**. Análise por faixa permite:
- Identificar onde AFS tem vantagem (margem boa)
- Identificar onde AFS é commodity (margem baixa)
- Decidir onde investir (expandir faixa X, reduzir faixa Y)

---

## Numeração S/N — decisão abr/2026

### Anterior
O Excel original tinha numeração com **gaps históricos** (S/N 4-8 vazios ou inconsistentes).

### Atual (sequencial)
Decisão abr/2026: **numeração sequencial limpa** (1, 2, 3, 4, 5, 6).

### Implicação retroativa
Análises históricas pré-abr/2026 podem ter usado S/N antigo. Cuidado ao comparar análises antes × depois da mudança — validar taxonomia vigente.

---

## Bitolas "Fora de Padrão"

### Faixas típicas
- **< 12.7 mm:** finos especiais (improvável no estoque AFS padrão)
- **> 800 mm:** super-grandes (caso a caso)
- **Entre faixas:** se aparece, provavelmente erro de cadastro

### O que fazer com Fora de Padrão
Ver [[06 - Fora de Padrão]]:
- **Visibilidade:** sempre aparecem no painel, mesmo que em categoria separada
- **Higiene:** flag para revisão periódica (algumas bitolas "Fora de Padrão" podem virar recorrentes e justificar inclusão na grade)
- **Não ignorar:** apenas separar

---

## Expansão da grade (processo)

### Quando expandir
- Bitolas específicas viram recorrentes em pedidos
- Cliente grande fecha demanda consistente em faixa não mapeada
- Estratégia comercial mira nicho (ex: barras gigantes para nicho nuclear)

### Como expandir
1. Identificar a faixa a adicionar (ex: 800.01-1000mm)
2. Atribuir próximo S/N (ex: 7)
3. Atualizar `FAIXAS_BITOLA` em:
   - Painel de Estoque HTML
   - Simulador de Precificação HTML
   - Motor Analítico Python
4. Atualizar mapeamento `FAMILIAS_PADRAO` para incluir combinações com a nova faixa
5. Comentar mudança no HTML (data + razão)
6. Atualizar [[01 - Família Canônica]] e esta nota

### Custo da mudança
Mudança na grade afeta **todas as análises** que agregam por família. Revisar:
- Dashboards
- Motor Analítico
- Simulador

---

## Mapeamento com tabela de preços

### Tabelas A/B/C no Softcomp
As tabelas Verde/Amarela/Vermelha (ver [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]]) geralmente são específicas por:
- Aço
- Acabamento
- Faixa de bitola

Ou seja: **cada combinação Aço × Acabamento × Faixa** tem sua própria tabela de 3 preços.

Campos RAF:
- `ABCPRE_MIN_A` = piso Tab Verde (R$/kg)
- `ABCPRE_MIN_B` = piso Tab Amarela (R$/kg)
- `ABCPRE_MIN_C` = piso Tab Vermelha (R$/kg)

### Implicação
**Ao criar nova família, definir tabelas de preço para ela.** Sem tabela, vendedor não tem piso.

---

## Análises por bitola

### Concentração do estoque
Pareto de peso/valor por faixa. Onde está concentrado o estoque?

### Giro por faixa
Algumas faixas giram rápido (1), outras devagar (5, 6). Normal.

### Margem por faixa
Faixas maiores (3, 4, 5, 6) tendem a ter margem unitária maior (menor concorrência). Análise RAF valida.

### Fora de Padrão por bitola
Quais bitolas aparecem em "Fora de Padrão"? Candidatos a formalização.

---

## Conexões

- [[00 - Visão Geral Estoque]]
- [[01 - Família Canônica]]
- [[04 - Painel de Estoque v2]]
- [[06 - Fora de Padrão]]
- [[Sistema Operacional Comercial/02 Precificação/06 - VPP Tolerância e Lâmina]]
- [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]]
- [[Sistema Operacional Comercial/02 Precificação/11 - Normas Técnicas]]
