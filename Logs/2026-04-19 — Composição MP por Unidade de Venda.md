---
tipo: decisão
categoria: produto / pricing
domínio: simulador
data: 2026-04-19
tags: [decisão, simulador, pricing, modos-venda, composição-mp, camada-7, w3-a]
---

# 2026-04-19 — Composição de MP por Unidade de Venda (3 bases paralelas)

## Contexto

Durante testes da onda W3-a do simulador (motor shadow rodando em paralelo ao HTML), detectada **divergência entre o preço /pç exibido no modo Kg e o preço /pç exibido no modo Pç** para o mesmo cenário (4340 Redondo Usinado Ø500×2500mm, 3 peças, Exio usinado/SP):

| | Modo Kg | Modo Pç |
|---|---|---|
| Card Vermelha /pç | R$ 105.286,59 | R$ 105.402,08 |
| Card Vermelha /Kg | R$ 25,10 | R$ 25,13 |
| Total Vermelha | R$ 299.775,83 | R$ 316.206,25 |
| MC% Vermelha | 19,41% | 19,42% |

Spread entre modos: ~0,11% nos cross-displays, ~5,5% no total. O comportamento estava por design parcial (VPP aplicado só em /pç), mas com **dois problemas combinados**:

1. **Cards recalculam ao trocar o lead_unit** — trocar "Venda por" mudava os valores de TODOS os cards, não só o destacado. Contrato pouco claro para vendedor e cliente.
2. **Cross-display /pç no modo Kg não bate com total/qtd** — R$ 105.286,59/pç × 3 = R$ 315.859,77 ≠ total R$ 299.775,83. Usa massa de conversão diferente da massa de faturamento. Risco comercial: vendedor promete preço /pç que o ERP não cobra.

## Alternativas consideradas

**A. Manter arquitetura atual** (base única de MP derivada do lead_unit)
- Prós: zero refatoração, comportamento estável em produção.
- Contras: mantém os dois problemas acima. Cliente que troca unidade recebe composição inconsistente. Vendedor pode comunicar /pç que não reconcilia com total.

**B. Três bases paralelas, cards calculados independentes do lead_unit** (escolhida)
- Prós: cada unidade sempre significa a mesma coisa; cross-display reconcilia com total na sua própria unidade; contrato claro com cliente e vendedor. Abre caminho para fechar a dívida retroativa da Camada 7 do motor (cobertura real nos 3 modos).
- Contras: refatoração do HTML + motor; recaptura de 5 fixtures (04-08).

**C. Cards recalculam a cada toggle mas cross-display reconcilia com total**
- Prós: resolve o problema 2 sem mexer em arquitetura.
- Contras: mantém o problema 1 (cliente que troca unidade pega composição diferente). Resolve sintoma, não causa.

## Trade-offs

A decisão por (B) troca **esforço de refatoração** (contido: a composição já é bem definida na nota [[05 - Modos de Venda]]) por **clareza contratual** e **eliminação de risco comercial estrutural**.

A janela para essa mudança é favorável: o motor shadow W3-a está em produção mas com toggle de alerta, e as Camadas 1-5, 7, 8a, 8b-corte e 9 já convergiram bit-idêntico em cenário real. A Camada 7 tem dívida retroativa documentada (fixtures só em sell_unit=pc) — a refatoração atual fecha a dívida em vez de acumulá-la.

## Decisão tomada

**Os 3 cards (Verde/Amarela/Vermelha) passam a calcular R$/pç, R$/kg e R$/m em paralelo, cada um com sua própria base de MP. Toggle "Venda por" muda apenas o lead unit (total + DRE + preço negociado); os valores dos cards não mudam.**

### Matriz de composição

| Componente | /pç | /kg | /m |
|---|:---:|:---:|:---:|
| MP líquida | ✓ | ✓ | ✓ |
| VPP (tolerância Ø externo) | ✓ | ✗ | ✓ |
| Corte | ✓ | ✓ | ✓ |
| Extra de corte | ✓ | ✓ | ✓ |
| Lâmina (mm/corte) | ✓ | ✓ | ✓ |
| Tolerância corte (mm/peça) | ✓ | ✗ | ✗ |

### Princípio unificador

**Tolerâncias (VPP Ø e tolerância corte mm/peça) só entram na base quando afetam receita.**

- `/pç` — cliente paga valor fixo por peça → toda variação absorvida pela empresa → todas as tolerâncias aplicam.
- `/m` — cliente paga valor fixo por metro, mas metragem é medida real no corte → VPP aplica (Ø subdimensionado pelo mesmo preço/m), tolerância de corte não (cobra o que cortou).
- `/kg` — cliente paga peso real → qualquer variação já está no peso faturado → nenhuma tolerância aplica.

Custos operacionais reais (MP, corte, extra de corte, lâmina) entram nas 3 bases sempre.

### Regra do preço negociado

Vale a **unidade ativa em "Venda por"**. Não recalcula cross-unit. Se vendedor troca venda_por depois de negociar, precisa ajustar manualmente. Princípio de mínimo-surpresa.

### Caso crítico — extra de corte em /m

Cenário real: vender 100 peças de 30mm cada (total 3m) cobrando R$/metro. Sem o extra de corte embutido no preço/m, os 100 setups de corte somem do custo e a margem real despenca.

Fórmula correta para composição do R$/m:
```
R$/m_extra_corte = (extra_corte_por_peça × qtd_peças) ÷ comprimento_total_m
```

O dado `qtd_peças` já está upstream no escopo do cálculo — vem da seção "Orçamento do Cliente" e alimenta "Material de Partida". Propagação até a função de preço/m é trivial.

## Justificativa

**Verdade 1 — Volume sem rentabilidade é armadilha.** O problema 2 (cross-display /pç ≠ total/qtd no modo Kg) cria risco de vendedor comunicar preço /pç inflado que o ERP não cobra → margem real silenciosamente abaixo do planejado. É o clássico "desconto invisível".

**Verdade 2 — Desconto é visível, custo oculto é silencioso.** Essa divergência é custo oculto estrutural no processo de cotação. Fica no simulador, mas quem paga é a margem na NF.

**Contrato claro com o cliente.** A regra "R$/pç sempre significa a mesma coisa, independente de como o vendedor entrou na tela" elimina uma classe de disputa comercial ("mas no orçamento você me mandou X, por que a nota veio Y?").

**Fecha dívida técnica.** A Camada 7 do motor tem lacuna documentada: fixtures só cobrem sell_unit=pc. A refatoração força a captura real de sell_unit=kg e sell_unit=m, fechando a cobertura real de uma vez.

## Riscos

**R1 — Refatoração do HTML pode introduzir regressão** em cenários não cobertos por fixture. Mitigação: fixar motor no paralelo (shadow W3-a) antes de refatorar HTML; validar bit-idêntico entre HTML novo e HTML antigo nos 8 cenários de fixture atuais; só depois autorizar cutover.

**R2 — Propagação de `qtd_peças` até cálculo de /m pode exigir ajustes em funções downstream** que hoje não conhecem esse dado. Mitigação: auditar antes de codar o caminho do dado.

**R3 — Decisão do preço negociado ("não recalcula cross-unit") pode gerar queixa de vendedor experiente** que esperava regeneração automática. Mitigação: documentar na UI com tooltip curto.

**R4 — Totalização do modo /kg depende de resolver a ambiguidade de peso** (massa de cálculo de MP vs massa de cross-display). A refatoração precisa unificar em uma única massa sellable.

## Resultado esperado

- Cards paralelos nos 3 modos, com valores idênticos independente do lead_unit.
- Total = `lead_unit_price × qty_lead`, com badge "Base ativa" indicando qual composição gerou o DRE.
- Cross-displays reconciliam com total dentro da tolerância de arredondamento.
- Camada 7 do motor com fixtures 04-08 recapturadas nos 3 modos, dívida retroativa fechada.

## Plano de execução

1. **Agora** — mapear `simCalc()` e identificar exatamente onde plugar as 3 bases paralelas.
2. **Implementar no HTML primeiro** (sem mexer no motor) → validar visualmente no cenário Exio usinado.
3. **Refatorar motor** para calcular `{pç, kg, m}` em paralelo; adapter espelha.
4. **Recapturar fixtures 04-08** com os 3 modos exercitados.
5. **Validação shadow W3-a** — 3 cards × 3 tabelas × 9 campos = 81 convergências bit-idênticas.

## Aprendizados futuros

(preencher após execução — foco em: (a) se o `qtd_peças` propagou limpo; (b) se a unificação de massa sellable resolve o cross-display; (c) se a recaptura das fixtures 04-08 revelou mais ramos não cobertos.)

## Conexões

- [[05 - Modos de Venda]] — atualizada hoje com a matriz completa e princípio unificador
- [[06 - VPP Tolerância e Lâmina]] — detalha os 3 elementos de variação
- [[08 - Simulador HTML - Arquitetura]] — estrutura do `simCalc()` e cards
- [[09 - Simulador Web App (futuro)]] — a refatoração atual alinha a arquitetura do web app futuro
- [[10 - Custo de Servir Aplicado]] — o caso das peças curtas em /m é exatamente custo de servir
- [[Pricing - Precificação]] — fundamentos
- [[Custo de Servir]] — princípio
