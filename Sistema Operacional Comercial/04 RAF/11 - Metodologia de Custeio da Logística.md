---
tipo: referência-técnica
domínio: logística / custeio
criado: 2026-06-11
última-revisão: 2026-06-11
tags: [logística, custeio, frete, custo-de-servir, pricing, CPK, make-vs-buy, política-frete]
aliases: [Metodologia de Custeio da Logística]
---

# 11 — Metodologia de Custeio da Logística

> Origem: rascunho do Gustavo (`Metodologia de Custeio da Logistica.md`), revisado e confrontado com as **despesas não orçamentárias (Jan–Mai/2026)** e o RAF em 2026-06-11. Supersede a tabela de % da [[06 - Despesas Logísticas por Unidade]] (que estava defasada).

## Propósito

Padronizar **como a Sacchelli mede o custo logístico real**, recupera esse custo no preço e decide entre frota própria e terceiro. Serve de base para a política de frete, o dimensionamento de frota e a conversa de [[Sistema Operacional Comercial/02 Precificação/10 - Custo de Servir Aplicado|Custo de Servir]] por cliente.

A tese central: o custo logístico médio (% sobre faturamento) **esconde** que uns pedidos pagam demais e outros de menos. Custear corretamente é separar o que é **fixo**, **variável** e **marginal**, e alocar cada um pelo direcionador certo.

---

## 1. Princípio: fixo + variável (CPK)

O custo de rodar um veículo se separa em duas naturezas:

- **Custo fixo** (independe de rodar): depreciação/reposição, salário do motorista + encargos, IPVA, seguro, licenciamento, rastreador. É diluído pelos km/viagens do mês.
- **Custo variável** (escala com o km): diesel, ARLA, pneus, manutenção, lubrificantes.

**Custo por km (CPK) = Custo fixo do mês ÷ km rodados + Custo variável por km.**

Consequência prática: o mesmo veículo tem CPK muito diferente se roda pouco (caminhão ocioso = CPK alto) ou muito. **Ociosidade é o maior destruidor de eficiência — maior que o preço do diesel.**

Comparação entre veículos deve usar **R$ por tonelada transportada (R$/ton·km)**, não só R$/km: o veículo maior carrega mais e tende a ter menor custo por tonelada — *desde que vá carregado*.

---

## 2. Componentes do custo logístico (não orçamentárias Guarulhos)

| Componente | % do custo | Natureza |
|---|---|---|
| Combustível + lubrificantes | ~41% | variável |
| Manutenção de caminhões | ~23% | variável |
| Pessoal (motoristas + equipe) | ~20% | fixo |
| Fretes terceiros | ~6% | — (buy) |
| IPVA | ~5% | fixo (pago à vista em jan → ratear pro-rata) |
| Pedágio (Sem Parar) | ~4,5% | repasse (pass-through) |
| Seguros / multas | ~1% | fixo |

Notas de método:
- O orçamento é **caixa** — não inclui depreciação (frota própria quitada). Para custo econômico real, somar reserva de reposição.
- **IPVA** é lançado de uma vez em janeiro; nas análises unitárias deve ser **rateado pro-rata** (×meses/12).
- **Pedágio** é repasse idêntico no próprio e no terceiro (Lorry reembolsa via Tag) → sai da comparação make-vs-buy.
- A janela de análise unitária deve usar meses com **romaneios completos** (em 2026, Jan–Mar; Abr–Jun vieram subcontados).
- Fonte dos valores absolutos: planilha **Despesas não Orçamentárias** (contas 71–78), confrontada na seção 4b.

---

## 3. Rateio do CD de Jacareí

O CD de Jacareí (conta **77.12**) é um **pool de custo logístico separado**, rateado entre as unidades de venda:

| Unidade | % do rateio |
|---|---|
| Guarulhos (Matriz) | 66,473% + 3,324% (Vila Prudente) = **69,797%** |
| Piracicaba | 10,024% |
| São Carlos | 8,554% |
| Caxias do Sul | 8,388% |
| Rio Preto | 3,237% |

Os cinco percentuais **somam exatamente 100%** (verificado). Pool Jan–Mai/2026 ≈ **R$ 137 mil** (≈ R$ 96 mil só para Guarulhos no rateio).

**Custo logístico de uma unidade = logística própria (X.12) + (% rateio × CD Jacareí 77.12).**

> **Anchieta (conta 78.12):** consolida em Guarulhos (Matriz), junto com a Vila Prudente — decisão de 2026-06-11, **confirmada** pela investigação do RAF. A Anchieta é uma **filial física nova** (só emite NF a partir de 2026: 4 itens, 3 clientes, R$ 351 mil) cujo custo logístico (R$ 94 mil Jan–Mai) é centro de custo próprio que apoia a operação de SP. As vendas são **reais, não transferência interna** — o cliente ADDN (92% do faturamento da filial) é cliente externo recorrente que compra milhões/ano em Matriz/SC/PIR desde 2023. O **26% logística/faturamento** é efeito de **ramp-up** (custo já instalado, emissão de NF ainda não escalou). É o que empurra Guarulhos de break-even para pequeno déficit no nível de grupo (ver 4b) — leitura correta enquanto a filial não escala. ⚠️ Revisar a razão quando a emissão da Anchieta crescer (a revisão trimestral cobre).

---

## 4. Recuperação no preço (quanto se cobra vs quanto custa)

O preço de venda embute **CML = Comercial + Logística** (campo RAF `ABCCUS_CML`), aplicado sobre o **faturamento bruto** (`ValorTotal`):

**% logística da unidade = (CML ÷ ValorTotal) − 3,70% (comercial fixo).**

% embutido por unidade (RAF, **validado Jan–Mai/2026**):

| Unidade | CML / ValorTotal | Logística cobrada |
|---|---|---|
| Guarulhos (Matriz) | 5,53% | **1,83%** |
| Piracicaba | 5,88% | 2,18% |
| Rio Preto | 6,74% | 3,04% |
| São Carlos | 7,29% | 3,59% |
| Caxias do Sul | 9,18% | 5,48% |

> Correção: a versão anterior trazia GRU 1,85% / CX 5,5% etc. (arredondados, janela diferente). Os valores acima são os do RAF Jan–Mai/2026. A [[06 - Despesas Logísticas por Unidade]] trazia números **muito mais defasados** (GRU 1,54%, PIR 1,64%) — desconsiderar.

⚠️ **Erro a evitar:** dividir o custo logístico pelo *valor entregue nos romaneios* (subconjunto do faturamento) infla o % artificialmente. O denominador correto é o **faturamento bruto da unidade (RAF)**, porque o % é cobrado de todos os pedidos faturados — **inclusive os retirados (rateio)**.

---

## 4b. Confrontação cobrado × real (não orçamentárias, Jan–Mai/2026)

Confronto do que se **cobra** (3,70% comercial + % logística por unidade) com o **custo real** das despesas não orçamentárias. Período Jan–Mai (junho parcial). Consolidação: Vila Prudente **e Anchieta** em Guarulhos; CD Jacareí rateado.

### Comercial — cobrado 3,70% × faturamento bruto vs custo real (R$ mil)

| Unidade | Fat. bruto | Cobrado 3,70% | Custo real | % real | Δ (cobr−real) |
|---|--:|--:|--:|--:|--:|
| Guarulhos | 71.536 | 2.647 | 2.234 | 3,12% | **+413** ✅ |
| Piracicaba | 8.189 | 303 | 201 | 2,45% | **+102** ✅ |
| São Carlos | 9.012 | 333 | 578 | 6,42% | **−245** ❌ |
| Caxias do Sul | 5.945 | 220 | 278 | 4,67% | **−58** ❌ |
| Rio Preto | 2.080 | 77 | 114 | 5,50% | **−37** ❌ |
| **Consolidado** | **96.763** | **3.580** | **3.405** | **3,52%** | **+175** ✅ |

**Leitura:** o 3,70% flat **cobre no agregado** (custo real consolidado 3,52%), mas **não cabe por unidade**. Guarulhos (3,12%) e Piracicaba (2,45%) **subsidiam** o interior — São Carlos custa **6,42%**, Rio Preto **5,50%**, Caxias **4,67%**. São Carlos sozinho consome R$ 245 mil a mais do que arrecada de comercial em 5 meses. Uma taxa comercial **diferenciada por unidade** (ou por porte de cliente) corrigiria o cross-subsídio.

### Logística — cobrado (CML − 3,70%) vs custo real, já com rateio do CD (R$ mil)

| Unidade | Própria | +CD rat. | Total real | % real | % cobrado | Δ |
|---|--:|--:|--:|--:|--:|--:|
| Guarulhos | 1.287 | 96 | 1.382 | 1,93% | 1,83% | **−71** ❌ |
| São Carlos | 331 | 12 | 343 | 3,80% | 3,59% | **−19** ❌ |
| Rio Preto | 56 | 4 | 60 | 2,90% | 3,04% | **+3** ✅ |
| Caxias do Sul | 289 | 11 | 301 | 5,06% | 5,48% | **+25** ✅ |
| Piracicaba | 126 | 14 | 140 | 1,70% | 2,18% | **+39** ✅ |
| **Consolidado** | | | **2.226** | **2,30%** | **2,28%** | **−23** ≈ break-even |

**Leitura:** logística praticamente **no break-even consolidado** (2,30% real vs 2,28% cobrado, déficit fino de R$ 23 mil em 5 meses). Caxias e Piracicaba **sobre-recuperam**; Guarulhos e São Carlos ficam levemente no vermelho. O déficit de Guarulhos (−R$ 71 mil) vem **da consolidação da Anchieta** — sem ela, Guarulhos fica em **1,81% real vs 1,83% cobrado (folga fina de +R$ 17 mil)**, como na tese original.

---

## 5. As três naturezas de custo por pedido (a distinção que decide tudo)

Para qualquer pedido, há **três** custos diferentes — usar o errado leva a decisão errada:

1. **Custo marginal** — o que muda ao adicionar 1 entrega numa rota que já vai sair: tempo do motorista na parada + km de desvio (~R$ 40–80 Grande SP, ~R$ 60–120 interior). *É o número certo para decidir se aceita um pedido pequeno.*
2. **Custo alocado** — o custo da viagem ÷ nº de entregas (~R$ 590 Grande SP, ~R$ 840 interior). *Serve para enxergar rentabilidade, não para precificar o pedido marginal.*
3. **Custo de viagem dedicada** — o custo cheio se o veículo sair só por aquele pedido (R$ 3.000–5.300 no interior). *É o que se evita com consolidação.*

**Cross-subsídio:** como o 1,83% é % sobre o valor, a NF grande e a retirada pagam mais que custam; a **NF pequena entregue paga muito menos** que o custo da sua parada. O médio fecha, mas os pedidos não são justos entre si. A política de frete corrige isso **por pedido**, sem mexer no % médio. (O mesmo vale para o 3,70% comercial — ver 4b.)

---

## 6. Métricas-chave

- **CPK** (R$/km) e **R$/ton·km** por veículo e perfil de rota (urbano vs rodoviário).
- **R$/kg de frete por região** — na ocupação atual e na ocupação-alvo (a tarifa-alvo usa carga consolidada).
- **Custo por viagem** e **custo por entrega/parada** por região.
- **Ocupação** (peso médio ÷ capacidade) — direcionador nº 1 do custo unitário.
- **Recuperação por unidade** (% cobrado vs custo real com CD) — comercial **e** logística.
- **Custo de servir por cliente** (alocar custo real às NFs do cliente).

---

## 7. Make vs Buy (frota própria vs terceiro)

- Comparar no **agregado** (dinheiro real gasto na frota no período vs o que o terceiro cobraria pelas mesmas viagens) e **por rota**.
- Excluir pedágio (repasse igual) dos dois lados.
- Mapear cada romaneio à rota do terceiro pela **cidade de destino mais distante** (manda na diária).
- Resultado 2026 (Jan–Mar): próprio ~R$ 3.560/viagem vs Lorry ~R$ 2.539 → terceiro **~30% mais barato**, vantagem **maior nos eixos longos** (Piracicaba/Limeira/Sorocaba 1,5×) e menor no urbano denso (1,3×). Causa: **subutilização** (≈39 viagens/mês, carga média 42% da capacidade).
- Pré-condição para a economia: cortar os **custos evitáveis** (motorista, manutenção, IPVA, seguro) ao reduzir frota; senão é custo duplo.

---

## 8. Política de frete derivada

- **Valor/peso mínimo de NF** para frete embutido (grátis): Grande SP **R$ 3.000 / 300 kg**; Interior **R$ 6.000 / 600 kg**.
- **Taxa de entrega** para NF abaixo do mínimo: **R$ 200** (Grande SP) / **R$ 400** (interior) — cobre o custo marginal e corrige o cross-subsídio, sem inviabilizar o pedido.
- **Grade de consolidação** por região (dias fixos de saída): pedido pequeno espera a janela da região. **Não despachar viagem dedicada do interior abaixo de ~8.000 kg (60% da capacidade).**
- **Urgência fora da janela:** cobrar frete especial (custo da viagem dedicada). Nunca absorver.
- **Retirada (Cliente Retira)** como opção "econômica" para baixo tíquete.

Não recusar pedido pequeno que pega carona — o custo extra é marginal (R$ 40–120), não o alocado. Recusar perde a margem da venda **e** deixa o caminhão mais vazio.

---

## 9. Dimensionamento de frota

A ocupação real revela sobredimensionamento: na Grande SP o caminhão sai com **29%** da carga (peso médio ~3,9 t) e **83% das viagens cabem em 7 t**. Implicação:
- **Urbano (Grande SP):** redimensionar para **toco 7t** (mais barato de comprar, abastecer e de IPVA). Economia ~R$ 1,0/km variável + ~R$ 2,0 mil/mês fixo por veículo.
- **Interior:** manter **truck 13,5t** (49% das viagens passam de 7 t).
- É decisão de **renovação** (frota quitada): ao trocar um caminhão urbano, comprar toco.

---

## 10. Caveats e qualidade de dados

- Romaneios de Abr–Jun/2026 vieram **incompletos** (viagens caem de 73 para 6/mês sem queda de custo). Usar Jan–Mar para economia unitária.
- A confrontação 4b usa **Jan–Mai** (junho parcial na planilha de despesas — pessoal zerado, totais despencam).
- Orçamento é **caixa** (sem depreciação). Para custo econômico, somar reserva de reposição.
- A tabela CML do vault antiga ([[06 - Despesas Logísticas por Unidade]], GRU 1,54%) está **desatualizada** — o RAF Jan–Mai mostra **1,83%**. Sempre validar % no RAF.
- O resultado de Guarulhos é **sensível ao tratamento da Anchieta** (78.12): com ela, déficit; sem ela, folga fina. Decisão atual = consolidar (ver seção 3).
- Para qualquer número que entra em decisão estratégica: anotar **fonte + data + margem de erro**.

---

## Conexões
- [[05 - Custo Real vs Cobrado]]
- [[06 - Despesas Logísticas por Unidade]]
- [[03 - MC Contábil vs Econômica]]
- [[Sistema Operacional Comercial/02 Precificação/03 - Componentes de Custo]]
- [[Custo de Servir]]
- [[Pricing - Precificação]]
- [[Playbook - Diagnóstico Comercial]]
