---
tipo: referência-técnica
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [margem-oculta, spread, componentes, economia]
---

# 04 — Margem Oculta (7 componentes)

## Conceito

**Margem oculta** = diferença entre o que a AFS **cobrou** do cliente (embutido no preço) e o que **realmente pagou** — para cada componente de custo.

Total = **+R$2,64M / +6,15 p.p.** (RAF abr/2026, jan-abr).

Esta nota detalha **cada um dos 7 componentes** que geram margem oculta.

---

## Recapitulação da convenção

| | Campo cobrado | Campo real | Margem oculta |
|---|---|---|---|
| Padrão | `ABCCUS_X` | `ABCCUS_X_COB` | `cobrado − real` |

Ver [[02 - Convenção Softcomp (Invertida)]].

---

## Os 9 componentes (2 sem spread + 7 com spread)

### Sem spread (valor cobrado = custo real)

#### ACO — Aço
- **Campo:** `ABCCUS_ACO`
- **Status:** `ABCCUS_ACO_COB = ABCCUS_ACO` **(estrutural)**
- **Por que:** é o **insumo principal**, precificado como custo puro. Margem sobre aço é capturada via MC contábil, não via spread.
- **Margem oculta:** **R$0**

**Implicação:** qualquer mudança no preço do aço no Softcomp mexe direto na MC contábil.

#### CML — Comercial + Logística
- **Campo:** `ABCCUS_CML`
- **Status:** só custo, sem spread
- **Composição:** 3,70% comercial fixo + logística variável por unidade
- **Margem oculta:** **R$0** (é despesa, não componente de margem)

Ver [[06 - Despesas Logísticas por Unidade]].

---

### Com spread — onde mora a margem oculta

#### 1. CTE — Corte (margem oculta **+R$1,01M**)

- **Campo cobrado:** `ABCCUS_CTE` = valor de corte embutido no preço
- **Campo real:** `ABCCUS_CTE_COB` = **0 na maioria dos casos**

**Por que spread é ~100%:**
Corte é **despesa orçamentária absorvida** pela AFS. No pricing, entra como custo embutido. Custo operacional de corte está na despesa fixa, não variável. Então todo valor cobrado (embutido) vira margem.

**Valor em jan-abr/2026:** R$1,01M (2,35 p.p.)

**Risco:** se AFS **servitizar** (cobrar corte explicitamente), margem oculta desaparece desse item — vira margem de serviço explícita. Mas se cliente **negocia corte "de graça"**, AFS perde o valor embutido.

---

#### 2. FIN — Financeiro (margem oculta **+R$1,01M**)

- **Campo cobrado:** `ABCCUS_FIN` = CF% embutido em vendas a prazo
- **Campo real:** `ABCCUS_FIN_COB` = Selic equivalente no período

**Por que spread é positivo:**
Em vendas a prazo, AFS cobra **CF% baseado em Selic + spread** (risco, custo operacional financeiro). Quando a empresa paga Selic "pura" ao banco, captura o spread.

**Valor em jan-abr/2026:** R$1,01M (2,35 p.p.)

**Risco:**
- Vendedor que negocia "desconto para pagamento à vista" pode estar dando mais do que vale o spread. Calcular antes.
- Se cliente paga antes do prazo, AFS **perde** o spread — é vantagem só se pagamento ocorre no prazo contratado.

---

#### 3. EXT — Externo / TT (margem oculta **+R$466k**)

- **Campo cobrado:** `ABCCUS_EXT` = preço do TT cobrado do cliente
- **Campo real:** `ABCCUS_EXT_COB` = custo pago ao fornecedor (tratador térmico)

**Por que spread é positivo:**
Margem AFS sobre tratamento térmico. Cliente paga 20-40% acima do custo real.

**Valor em jan-abr/2026:** R$466k (1,08 p.p.)

**Risco:**
- Cliente que **conhece o custo** de TT (informação de mercado) pode negociar desconto em TT. Impacta spread.
- Fornecedor de TT que aumenta preço força AFS a repassar ou absorver.

---

#### 4. COM — Comissão (margem oculta **+R$111k**)

- **Campo cobrado:** `ABCCUS_COM` = comissão cobrada (tipicamente 2% padrão)
- **Campo real:** `ABCCUS_COM_COB` = comissão paga efetivamente

**Por que spread é positivo:**
Quando vendedor **interno** recebe 2% mas cliente vê cobrança "padrão" que reflete o cenário típico (lobista/agente 2×), há margem.

**Quando spread é negativo:**
Venda via **lobista/agente** cujo custo é 3-4%, mas preço cobrado tem só 2% de comissão embutida. AFS absorve a diferença.

**Valor líquido em jan-abr/2026:** R$111k (0,26 p.p.)

**Regra:** sempre precificar comissão real no simulador. Se tem lobista, cobrar a comissão real.

---

#### 5. CER — Certificação (margem oculta **+R$23k**)

- **Campo cobrado:** `ABCCUS_CER` = preço de certificação cobrado
- **Campo real:** `ABCCUS_CER_COB` = custo interno de emitir (quase zero)

**Por que spread é ~100%:**
Certificações são emitidas internamente ou via lab parceiro com custo baixo. Preço cobrado ao cliente é padrão por tipo de certificado.

**Valor em jan-abr/2026:** R$23k (0,05 p.p.)

**Observação:** valor pequeno em absoluto, mas margem percentual altíssima. Opção de crescer o serviço sem custo operacional proporcional.

---

#### 6. INT — Interno (margem oculta **+R$19k**)

- **Campo cobrado:** `ABCCUS_INT` = processos internos cobrados
- **Campo real:** `ABCCUS_INT_COB` = custo real quase zero

**Tipicamente:** preparações especiais, inspeção adicional, documentação internal.

**Valor em jan-abr/2026:** R$19k (0,04 p.p.)

---

#### 7. IMP — Impostos (margem oculta **R$0**)

- **Campo cobrado:** `ABCCUS_IMP` = impostos cobrados (base do preço)
- **Campo real:** `ABCCUS_IMP_COB` = impostos pagos efetivamente

**Por que zero:**
AFS já calcula PIS/COFINS sobre a **base correta** (excluindo ICMS). Não há "erro de base" que gere diferença.

**Valor em jan-abr/2026:** R$0

**Se fosse negativo:** indicaria que AFS está calculando imposto sobre base cheia e absorvendo diferença (problema real em outros distribuidores que não sabem).

---

## Consolidado

| Componente | Margem oculta | % sobre líquido aço | Risco principal |
|---|---|---|---|
| CTE (corte) | +R$1,01M | +2,35 p.p. | Servitização ou desconto |
| FIN (financeiro) | +R$1,01M | +2,35 p.p. | Pagamento antecipado |
| EXT (TT) | +R$466k | +1,08 p.p. | Cliente conhecer custo |
| COM (comissão) | +R$111k | +0,26 p.p. | Venda via lobista |
| CER (certificação) | +R$23k | +0,05 p.p. | (baixo — oportunidade de crescer) |
| INT (interno) | +R$19k | +0,04 p.p. | (baixo) |
| IMP (impostos) | R$0 | 0,00 p.p. | (neutro — bem calculado) |
| **TOTAL** | **+R$2,64M** | **+6,15 p.p.** | — |

---

## Análise por tipo de pedido

### Pedido 100% aço puro (sem serviço)
- **Margem oculta = ~0** (só spread FIN se a prazo)
- Desconto come MC contábil direto
- **Risco alto** — qualquer desconto aparece inteiro em margem

### Pedido com corte + serviço (TT/ensaio/certif)
- **Margem oculta significativa** (pode chegar 5-7 p.p.)
- Desconto come MC contábil, mas margem oculta fica
- **Mais resiliente** a desconto

### Implicação de carteira
Clientes que compram **pacote completo** (aço + serviços) geram **maior valor econômico** que clientes de aço puro, mesmo se volume parecido.

**Ação proposta:** ranking de clientes por **spread total capturado**, não só MC contábil.

---

## O que pode **diminuir** margem oculta no tempo

### Competitivo
- Concorrente agressivo começa a ofertar serviços mais barato
- Tradings (Duferco, DITH) entram com pricing de serviço premium mas mais transparente

### Cliente
- Cliente fica mais sofisticado e negocia serviços item a item
- Cliente passa a fazer serviços internamente (traz TT in-house)

### Tecnológico
- Plataformas digitais de distribuição trazem transparência
- Clientes comparam preços de corte, TT, certificação online

### Interno
- Mudança de política (cobrar corte explicitamente em vez de embutir)
- Mudança de composição de carteira (mais clientes tabelistas = menos serviços)

---

## Medidas de preservação

1. **Não negociar serviço isoladamente.** Se cliente pede desconto, é desconto no pacote, não no TT isolado.
2. **Precificar serviço explicitamente** no simulador — não omitir componente.
3. **Monitorar uplift** (Motor Analítico). Se cai abaixo de 4-5 p.p., investigar causa.
4. **Treinar vendedor** a entender que nem todo desconto come margem igual (depende do tipo de pedido).

---

## Conexões

- [[00 - Visão Geral RAF]]
- [[02 - Convenção Softcomp (Invertida)]]
- [[03 - MC Contábil vs Econômica]]
- [[05 - Custo Real vs Cobrado]]
- [[10 - Margem MC PGA (Metas Anuais)]] — **fórmula oficial das metas anuais 2026** (subset desta nota: MC_Aço + FIN + COR + EXT + INT + CER; exclui REP e CML)
- [[02 Precificação/01 - Fórmula do Lucro]]
- [[02 Precificação/03 - Componentes de Custo]]
- [[02 Precificação/10 - Custo de Servir Aplicado]]
