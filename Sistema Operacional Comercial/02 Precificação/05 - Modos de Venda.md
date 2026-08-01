---
tipo: regra-negócio
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-19
tags: [modos-venda, kg, peca, metro, pricing, regras, composição-mp]
---

# 05 — Modos de Venda (R$/Kg, R$/Pç, R$/m)

## Conceito central

Sacchelli vende aço em **3 modos** distintos, cada um com **regras próprias** de como VPP, Tolerância e Lâmina entram no cálculo.

Essa regra é fundamental porque determina **o que a AFS absorve** e **o que o cliente paga**.

---

## Tabela canônica (composição completa de MP por modo)

> **Atualizada em 2026-04-19** — ver decisão de produto no Log [[Logs/2026-04-19 — Composição MP por Unidade de Venda]].

| Componente | /Kg | /Pç | /m | Observação |
|---|:---:|:---:|:---:|---|
| **MP líquida** | ✓ | ✓ | ✓ | Sempre entra |
| **VPP** (tolerância Ø) | ✗ | ✓ | ✓ | Tolerância dimensional de diâmetro |
| **Corte** | ✓ | ✓ | ✓ | Custo operacional de serrar |
| **Extra de corte** | ✓ | ✓ | ✓ | Setup adicional por peça cortada |
| **Lâmina** (mm/corte) | ✓ | ✓ | ✓ | Material perdido no kerf |
| **Tolerância corte** (mm/peça) | ✗ | ✓ | ✗ | Variação dimensional no comprimento |

### Princípio unificador

**Tolerâncias só entram onde a tolerância afeta receita.** Custos operacionais reais (MP, corte, extra corte, lâmina) entram sempre.

- `/Kg` — cliente paga peso real. Toda variação (VPP ou tolerância de corte) já está embutida no peso faturado → nenhuma tolerância aplica.
- `/Pç` — cliente paga valor fixo por peça. Empresa absorve qualquer variação dimensional → todas as tolerâncias aplicam.
- `/m` — cliente paga pelo comprimento medido real. VPP afeta receita (Ø menor no mesmo preço/m = menos massa entregue); tolerância de corte não afeta (cobra o que cortou).

---

## Explicação de cada modo

### R$/Kg (por quilo)

**Como funciona:**
- Preço é R$/kg
- Cliente paga pelo **peso real na balança** no momento do faturamento
- Se barra vem mais pesada (VPP), cliente paga a mais — **automaticamente recuperado**
- Lâmina entra no custo (material comprado vai além do pedido pelo corte)

**VPP no pricing:** ❌ **não aplicar** — o peso real cobre isso.

**Tolerância no pricing:** ❌ **não aplicar** — se peça cortada pesa a mais, cliente paga.

**Lâmina no pricing:** ✅ **aplicar** — a AFS compra material além do pedido para absorver corte.

**Quando usar:** venda padrão de barras, chapas, peças que serão pesadas.

**Divisor para peça acabada:** peso do **orçamento do cliente** (material acabado), não peso de partida.
- Exemplo: cliente pede 1.000 kg de descascado → partida = 1.072 kg → R$/kg = Valor_Total / 1.000, não / 1.072
- Implementado via `pesoVendaKg` no simulador (2026-04-09)

### R$/Pç (por peça)

**Como funciona:**
- Preço é R$/peça
- Cliente paga **valor fixo por unidade**, independente de peso real da peça
- Se peça vier mais pesada (VPP ou tolerância), AFS absorve — cliente não paga a mais
- Se peça for menor, AFS ganha (mas em commodity normalmente não — material é aproveitado)

**VPP no pricing:** ✅ **aplicar** — AFS precisa cobrir o peso extra que vai entregar.

**Tolerância no pricing:** ✅ **aplicar** — se tolerância permite +3mm e cliente não paga por isso, AFS precisa cobrir.

**Lâmina no pricing:** ✅ **aplicar** — corte consome material adicional.

**Quando usar:**
- Peças fornecidas em quantidade exata (lote contratado)
- Engenheirado: **exclusivamente R$/Pç** (único modo permitido)

**Engenheirado:** material engenheirado não tem peso de venda definido; custeio usa peso de partida. Botões Kg e m **desabilitados** no simulador.

### R$/m (por metro)

**Como funciona:**
- Preço é R$/metro
- Cliente paga pelo **comprimento medido real** (ex: 1003 mm vira 1,003 m)
- Peso extra por VPP **não é recuperado** (fatura é por metro, não por peso)
- Tolerância de comprimento é recuperada (se peça tem 3 mm a mais, cobra)

**VPP no pricing:** ✅ **aplicar** — peso extra não aparece no faturamento.

**Tolerância no pricing:** ❌ **não aplicar** — comprimento real é faturado.

**Lâmina no pricing:** ✅ **aplicar** — corte consome material adicional.

**Quando usar:** vergalhões longos, perfis que são medidos em metros, aplicações onde comprimento é o referencial crítico.

---

## Cards paralelos e preço negociado (decisão 2026-04-19)

### Cards são calculados em paralelo

Os 3 cards (Verde/Amarela/Vermelha) mostram **sempre** R$/Pç, R$/Kg e R$/m calculados de acordo com a composição de cada modo. **Trocar "Venda por" não recalcula os cards** — apenas muda o lead_unit (qual é o primário, qual gera Total e DRE).

Consequência prática: o valor /pç mostrado no card **sempre significa a mesma coisa** independentemente de como o vendedor entrou na tela. Elimina risco de cliente receber composição inconsistente ao trocar unidade de referência.

### Preço negociado vale a unidade ativa

Quando vendedor insere preço negociado, vale a **unidade ativa em "Venda por"**. Não há regeneração automática cross-unit. Se o vendedor troca venda_por depois de negociar, o preço negociado precisa ser ajustado manualmente.

Princípio: mínimo-surpresa. O vendedor controla quando e em qual unidade o preço é fixado.

### Total e DRE usam o lead_unit

- Total = `lead_unit_price × qty_lead`
- DRE e memória de cálculo mostram badge "Base ativa: MP com VPP /pç" (ou /m, ou sem VPP /kg)
- Cross-displays nos cards são calculados a partir da **sua própria composição**, não derivados do total do lead

---

## Cenário crítico — extra de corte em /m

### O problema

Venda de peças curtas por R$/metro pode esconder custo operacional. Exemplo:

> Cliente pede **100 peças de 30mm cada** (total 3m), cobrando R$/metro.

Se o simulador calcula R$/m com extra de corte como custo único (1 setup), os **100 setups reais de corte somem do custo** e a margem real despenca ao executar o pedido.

### Fórmula correta de composição em /m

```javascript
// Extra de corte em /m precisa ratear pelo nº de cortes realizados
const extraCorteMperUnit = (extraCortePorPeca * qtdPecas) / comprimentoTotalMetros;
```

O dado `qtd_peças` já está upstream no escopo do cálculo — vem da seção "Orçamento do Cliente" e alimenta "Material de Partida". Propagação até a função de preço/m é trivial.

### Regra geral (todos os componentes operacionais em /m)

Qualquer componente que é **por peça** (corte, extra corte, setup de tratamento) e não **por metro** precisa ser convertido:

```javascript
componente_por_m = (componente_por_peca * qtd_pecas) / comprimento_total_m
```

Essa conversão também vale para /Kg quando o componente é intrinsicamente por-peça (ex: certificação por lote de peças, embalagem individual).

---

## Implementação no Simulador HTML

### Variáveis-chave (JavaScript)

```javascript
// Peso base Softcomp (peças × lâmina, sem tolerância)
const pesoMPTon = ...;

// Peso para R$/Pç (com tolerância)
const pesoMPTon_pc = pesoMPTon × (1 + tolerancia%);

// Custo aço R$/kg para R$/Pç e R$/m (com VPP — aplicado ao custo)
const custoTon_full = custoTon_base × (1 + VPP);

// Custo aço R$/kg para R$/Kg (sem VPP — cliente paga peso real)
const custoTon_kg = custoTon_base;
```

### Cálculo por modo

```javascript
// R$/Kg — sem VPP, sem tolerância no custo
mpCusto_kg = pesoMPTon × custoTon_kg;

// R$/Pç — com VPP e tolerância
mpCusto_pc = pesoMPTon_pc × custoTon_full;

// R$/m — com VPP, sem tolerância (comprimento é medido)
mpCusto_m = pesoMPTon × custoTon_full;
```

---

## Referências VPP (valores operacionais)

| Acabamento | VPP típico |
|---|---|
| Laminado | **1%** |
| Forjado | **5-6%** |

Configurável no Setup do simulador.

---

## Referências Tolerância

Depende da norma aplicável por produto:
- EN 10060 (redondos laminados)
- EN 10088 (inox)
- DIN/ISO específicos por aço ferramenta
- Especificação interna do cliente (às vezes mais rigorosa)

Ver [[11 - Normas Técnicas]] para detalhes.

---

## Atenções críticas

### 1. Nunca misturar modos sem calcular
Se cliente pede peça "1000 kg da peça X e 50 peças da peça Y", não calcular um modo só. Cada item tem seu modo, seu custo, sua margem.

### 2. Engenheirado é R$/Pç exclusivo
Não tentar fazer R$/kg em material engenheirado. Não há peso de venda definido. Simulador bloqueia os botões kg e m.

### 3. Conversão entre modos
- **Peso → peça:** peso do orçamento / peso unitário
- **Peso → metro:** peso / (peso_por_metro)
- **Peça → metro:** usa peso_por_peça × peso_por_metro

Essas conversões são úteis para negociação ("cliente quer pagar R$/pç, vamos ver se em R$/kg ficaria melhor").

### 4. Custo de produzir ≠ preço de venda
Os três modos são **modos de faturamento**, não modos de produção. Material é produzido do mesmo jeito independente do modo de venda. Só o preço muda.

### 5. R$/Kg com acabado — divisor correto
Repetindo porque é crítico: em R$/Kg com peça acabada (trefilado, descascado, usinado), divisor é o **peso do orçamento do cliente** (peso acabado), não o peso de partida.

---

## Decisão comercial — quando propor cada modo

### Cliente de alto volume consistente
**R$/Kg** tipicamente. Vantagem: cliente entende (pesagem), AFS não absorve surpresas.

### Cliente de baixo volume ou lote fechado
**R$/Pç** faz mais sentido. Cliente paga valor fixo, tem previsibilidade. AFS protege com VPP e tolerância.

### Produto que é medido/cortado com base em comprimento
**R$/m** é natural. Tipicamente vergalhões, barras longas especiais.

### Proposta comercial
Em negociações complexas, apresentar **2 modos** com valor equivalente para o cliente escolher. Modo de venda é parte da proposta, não só o preço.

---

## Relação com outras notas

- [[02 - Fórmula de Preço Sacchelli]]
- [[03 - Componentes de Custo]]
- [[06 - VPP Tolerância e Lâmina]]
- [[08 - Simulador HTML - Arquitetura]]
- [[10 - Custo de Servir Aplicado]] — cenário peças curtas em /m é custo de servir
- [[11 - Normas Técnicas]]

## Logs de decisão

- [[Logs/2026-04-19 — Composição MP por Unidade de Venda]] — decisão de produto das 3 bases paralelas, princípio unificador e regra do preço negociado
