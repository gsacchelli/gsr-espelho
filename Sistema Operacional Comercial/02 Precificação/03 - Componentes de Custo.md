---
tipo: referência-técnica
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [custo, componentes, pricing, detalhado]
---

# 03 — Componentes de Custo

## Propósito

Detalhamento de **cada componente** que entra no cálculo do preço, com: o que é, como calcular, em qual campo RAF está, e o que fazer se mudar.

---

## Componentes

### 1. Aço (custo do material)

**O que é:** custo de aquisição da matéria-prima.

**Subcomponentes (quando importação):**
- Preço FOB China
- Frete break bulk (USD 110/mt — ver `project_freight_parameters`)
- AFRMM (25% do frete)
- Seguro internacional
- Despesas aduaneiras
- ICMS importação
- IPI
- PIS/COFINS (importação)
- Frete interno (SFS → unidade AFS)

**Quando nacional:**
- Preço negociado com usina
- Frete usina → unidade AFS
- Impostos aplicáveis

**Custo ponderado no estoque:**
Quando estoque tem múltiplos lotes com custos diferentes, AFS usa **custo médio ponderado** (PEPS/PMP conforme política contábil).

**Campo RAF:** `ABCPRE_KG` (R$/ton)

**Atualização:** preço China sobe/cai com frequência. CFR China teve +35% em 43XX em 5 semanas (fev→mar/2026). Monitorar via relatório `steel-market-intel-weekly`.

**Impacto em pricing:** mudança de 1 ponto percentual no custo aço = ~1 p.p. na MC aço (se preço de venda for mantido).

### 2. Corte

**O que é:** serviço de dimensionamento da barra em peças.

**Custo real inclui:**
- Tempo-máquina (serra, tesoura)
- Desgaste de lâmina
- Energia
- Mão de obra direta

**Custo cobrado hoje:** **absorvido** (não cobrado separadamente). ABCCUS_CTE_COB = 0 na maioria dos casos.

**Implicação:** no pricing ferroso da AFS, corte é **despesa orçamentária absorvida**. Cliente não vê custo separado.

**Margem oculta:** todo ABCCUS_CTE registrado é **margem capturada** pela AFS (o cliente teria essa despesa se fosse em outro lugar). Ver [[Sistema Operacional Comercial/04 RAF/04 - Margem Oculta (7 componentes)]].

**Em abr/2026:** R$1,0M de margem oculta via corte.

**Mudança em servitização:** se MetalM ou evolução AFS servitizar, corte vira linha explícita de preço. Isso muda a conversa comercial inteira.

### 3. Tratamento térmico (TT)

**O que é:** têmpera, revenido, alívio de tensão, solubilização, etc.

**Fornecedores:** terceirizado (poucas operações internas).

**Custo real:** custo pago ao terceiro + logística entre AFS e terceiro.

**Custo cobrado:** terceiro × (1 + margem AFS). Margem típica 20-40%.

**Campos RAF:**
- `ABCCUS_EXT` = cobrado
- `ABCCUS_EXT_COB` = custo real

**Spread:** em abr/2026, ~R$466k de margem oculta.

**Atenção:** se cliente negociar desconto pedindo TT "de graça", AFS absorve o custo **e** perde a margem. Sempre precificar TT explicitamente.

### 4. Ensaios e certificações

**O que é:** dureza, metalografia, dimensional, certificação de qualidade.

**Custo real:** baixo a zero (alguns ensaios são internos, outros terceirizados baratos).

**Custo cobrado:** valor padrão por certificado, faturado à parte.

**Campos RAF:**
- `ABCCUS_CER` = cobrado (certificação)
- `ABCCUS_CER_COB` = real (tipicamente 0)
- `ABCCUS_INT` = cobrado (interno)
- `ABCCUS_INT_COB` = real (tipicamente 0)

**Em abr/2026:** R$23k certif + R$19k interno = R$42k margem oculta. Valores pequenos, mas margem percentual próxima de 100%.

### 5. Impostos

**Impostos não-recuperáveis que entram no custo:**
- ICMS substituição tributária (quando aplicável)
- IPI na entrada (quando aplicável)
- PIS/COFINS sobre a base correta

**Regra PIS/COFINS:** não incide sobre ICMS. Erro comum é calcular sobre base cheia, inflando o custo e perdendo competitividade.

**Campos RAF:**
- `ABCCUS_IMP` = cobrado (base completa)
- `ABCCUS_IMP_COB` = real (base correta)

**Spread típico:** margem oculta por arrumar a base. Em abr/2026, IMP = zero (AFS já calcula corretamente).

### 6. Comissão

**Tipos:**
- Vendedor interno (INT/PJ): 2% sobre faturamento s/IPI
- Lobista/agente: % variável (alguns 3%, alguns 4%)
- Representante externo (REP): conforme contrato

**Campos RAF:**
- `ABCCUS_COM` = cobrado (vendedor interno padrão 2%)
- `ABCCUS_COM_COB` = real (quando paga lobista/agente 2× o padrão)

**Spread:** quando vendedor interno 2% (cobrado) vs lobista/agente real 2% — spread zero. Quando cliente requer lobista 4% e AFS cobra 2% — spread negativo (AFS absorve).

**Em abr/2026:** spread COM positivo ~R$111k (casos onde comissão cobrada foi maior que a real).

### 7. Comercial + Logística (CML)

**Comercial (fixo):** 3,70% ao ano, rateado por operação. Cobre estrutura comercial (vendedores, gestão, processos).

**Logística (variável por unidade):**

| Unidade | % de despesa logística | Observações |
|---|---|---|
| Guarulhos (GRU) | 1,54% | Core operacional, menor handicap |
| Piracicaba (PIR) | 1,64% | Próximo SP |
| Rio Preto (RIP) | 2,76% | Distância média |
| São Carlos (SCA) | 3,24% | Distância maior |
| **Caxias do Sul (CXS)** | **5,65%** | Gargalo — 3 pernas logísticas |

**Reavaliação:** trimestral para logística, fixo anual para comercial.

**Campos RAF:** `ABCCUS_CML` = soma (sem spread estrutural — só custo).

**Em abr/2026:** CML sem spread (é despesa, não componente de margem).

### 8. Financeiro (CF%)

**O que é:** custo financeiro cobrado em vendas a prazo (juros embutido no preço).

**Cálculo cobrado:** CF% aplicado sobre prazo médio de recebimento, baseado em Selic + spread AFS.

**Custo real:** Selic vigente no momento.

**Campos RAF:**
- `ABCCUS_FIN` = cobrado (CF% no pricing)
- `ABCCUS_FIN_COB` = real (Selic equivalente)

**Spread:** CF% cobrado tipicamente > Selic real. Em abr/2026, margem oculta ~R$1,0M.

**Atenção:** vendedor que negocia "desconto para pagamento à vista" pode estar dando desconto maior do que o spread financeiro real. Calcular antes de aceitar.

---

## VPP (Variação Permissível de Peso)

Ver detalhes em [[06 - VPP Tolerância e Lâmina]].

**Referências:**
- Laminado: 1%
- Forjado: 5-6% (configurável por família)

**Impacto:** no pricing R$/pç e R$/m, VPP entra no custo (AFS absorve diferença). Em R$/kg, cliente paga peso real.

---

## Tolerância dimensional

**Quando aplica:** venda em R$/pç (preço fixo por unidade).

**Referências:**
- EN 10060 (normativa europeia para produtos laminados)
- ABNT NBR equivalentes
- Specs internas por família

**Impacto:** se peça cortada tem +3mm sobre o pedido (dentro da tolerância), cliente não paga a mais. Em R$/pç, tolerância deve ser coberta no pricing.

---

## Lâmina

**O que é:** espessura de corte (material perdido na serra). Inclui no custo porque é material que foi comprado mas não vai pro cliente.

**Referências:** ~2-5mm dependendo da serra e diâmetro.

**Quando entra:**
- Sempre no custo (material comprado vai além do pedido pelo corte)
- Exceto quando explicitamente descontado

---

## Perda de processo (acabamento)

**Quando aplica:** materiais acabados (trefilado, descascado, usinado).

**Rendimento típico:**
- Trefilado: ~95-97% (3-5% de perda)
- Descascado: ~93-95% (5-7% de perda)
- Usinado: variável, depende da forma final

**Impacto:** peso de partida > peso do orçamento do cliente. Em R$/kg com peça acabada, divisor é o peso acabado, não partida.

---

## Tabela consolidada de custos

| Componente | % típico sobre Receita | Variabilidade | Margem oculta típica |
|---|---|---|---|
| Aço | 60-80% | Alta (mercado global) | Zero |
| Corte | 1-3% | Baixa | 100% (absorvido) |
| TT (quando aplicável) | 2-5% | Média | 20-40% |
| Ensaios/Certif | <1% | Baixa | ~100% |
| Comissão | 2% | Fixa | Zero ou positiva |
| Logística | 1,5-5,7% | Alta (por unidade) | Zero (despesa pura) |
| Comercial | 3,70% | Fixa | Zero (despesa pura) |
| Financeiro (prazo) | 1-3% | Média (Selic) | Positiva (spread) |
| Impostos | Variável | Baixa | Zero (se bem calculado) |

---

## Atualização dos componentes

### Quando atualizar cada um

| Componente | Frequência |
|---|---|
| Aço | Contínua (mercado) — alerta se variação >5% |
| Corte | Anual (custo operacional) |
| TT | Sob demanda (quando fornecedor muda preço) |
| Ensaios/Certif | Anual |
| Comissão | Quando há mudança contratual |
| Logística | Trimestral |
| Comercial | Anual |
| Financeiro | Contínuo (Selic) — mensal na prática |
| Impostos | Quando legislação muda |

### Onde atualizar (simulador)
No Simulador HTML, aba "Setup" tem os parâmetros editáveis.

### Onde validar (RAF)
Pós-faturamento, spread de cada componente visível no RAF.

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[06 - VPP Tolerância e Lâmina]]
- [[10 - Custo de Servir Aplicado]]
- [[11 - Normas Técnicas]]
- [[Sistema Operacional Comercial/04 RAF/02 - Convenção Softcomp (Invertida)]]
- [[Sistema Operacional Comercial/04 RAF/04 - Margem Oculta (7 componentes)]]
- [[Sistema Operacional Comercial/04 RAF/06 - Despesas Logísticas por Unidade]]
