---
tipo: referência-técnica
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [vpp, tolerância, lâmina, peso, norma-técnica]
---

# 06 — VPP, Tolerância e Lâmina

## Os 3 elementos que distinguem peso nominal de peso real

Em venda de aço, existem 3 fatores que fazem o **peso real entregue** divergir do **peso nominal calculado**:

1. **VPP** — Variação Permissível de Peso (peso extra por densidade)
2. **Tolerância** — variação permissível de medida (dimensional)
3. **Lâmina** — material perdido no corte

Cada um tem tratamento específico no pricing (ver [[05 - Modos de Venda]] para tabela por modo).

---

## VPP — Variação Permissível de Peso

### O que é
Norma técnica permite que uma barra "de 100mm" tenha peso real diferente do peso teórico (calculado pela geometria × densidade teórica). Essa **variação** é a VPP.

### Por que acontece
- Densidade real do aço varia por elemento de liga
- Processo de laminação/forja deixa variação dimensional
- Normas (EN 10060, etc.) permitem faixa

### Percentuais operacionais Sacchelli

| Acabamento | VPP típica |
|---|---|
| **Laminado** | **1%** |
| **Forjado** | **5-6%** |

Configurável no Setup do simulador por família.

### Exemplo prático
Cliente pede 1.000 kg de aço 4140 redondo laminado.

- Peso teórico: 1.000 kg
- Com VPP 1%: peso real pode chegar a 1.010 kg
- Peso real entregue: 1.010 kg
- Em R$/kg: cliente paga 1.010 × R$/kg (recupera o excesso)
- Em R$/pç ou R$/m: cliente paga 1.000 × R$/kg equivalente (AFS absorve 10 kg se não precificar)

### Implicação para pricing

**R$/Kg:** VPP não entra no custo. Cliente paga peso real.

**R$/Pç e R$/m:** VPP **entra** no custo. Calcular o custo do material considerando o peso máximo que pode vir (custo ponderado).

### Campo no simulador
Input: "VPP (%)" no Setup. Padrão conforme acabamento.

---

## Tolerância Dimensional

### O que é
Norma técnica permite que uma peça "de 1000mm de comprimento" tenha comprimento real levemente diferente. Ex: 1000mm +3/−0 mm.

### Por que acontece
- Processo de corte tem precisão limitada
- Normas definem tolerâncias aceitáveis
- Expectativa do cliente é peça dentro da tolerância

### Referências normativas
- **EN 10060** (redondos laminados a quente)
- **EN 10277** (aços para usinagem)
- **DIN/ISO** específicos por aço ferramenta
- **ABNT NBR** equivalentes brasileiras

Ver [[11 - Normas Técnicas]] para detalhes por aço.

### Tipos de tolerância aplicáveis
- **Dimensional:** variação de diâmetro, comprimento, retidão
- **Superficial:** rugosidade, acabamento
- **Geométrica:** circularidade, cilindricidade

No pricing, geralmente o foco é **tolerância de comprimento** (cortes) e diâmetro.

### Exemplo
Cliente pede peça de 1000mm, tolerância +3/−0 mm.

- Peça real pode vir: 1000 a 1003 mm
- Em R$/kg: cliente paga peso real — se peça é 1003mm (mais pesada), paga mais
- Em R$/pç: preço fixo por peça — AFS absorve 3mm de material extra
- Em R$/m: cliente paga 1,003 m (comprimento medido)

### Implicação para pricing

**R$/Kg:** tolerância não entra no custo — peso real é faturado.

**R$/Pç:** tolerância **entra** no custo. AFS precisa cobrir material extra.

**R$/m:** tolerância não entra no custo — comprimento real é faturado.

### Campo no simulador
Input: "Tolerância (%)" ou valor absoluto, ativado conforme modo de venda.

---

## Lâmina

### O que é
Espessura de corte da serra (ou outra ferramenta). Material que vira **refugo** durante o processo de cortar a barra em peças.

### Por que importa para pricing
AFS compra barra inteira. Só entrega as peças cortadas. O material da lâmina (kerf) **foi pago pela AFS** mas **não vai para o cliente**.

Em todo pricing, material comprado > material entregue. A lâmina deve estar coberta.

### Valores típicos
Depende da ferramenta:
- **Serra fita fina:** 1,5-2,5 mm
- **Serra fita normal:** 2,5-4,0 mm
- **Tesoura:** 0,5-1,0 mm (deformação)

No simulador, lâmina é input de Setup por processo/equipamento.

### Exemplo
Barra de 3 metros cortada em 3 peças de 1 metro.

- Material nominal para peças: 3 × 1000 mm = 3000 mm
- Com lâmina de 3mm × 2 cortes: 3000 + 6 mm = 3006 mm de barra necessária
- Diferença: 0,2% de material extra

Em barra de 10mm de diâmetro, isso é pouco. Em barra de 400mm de diâmetro, cada milímetro de lâmina pesa muito.

### Implicação para pricing
**Todos os modos:** lâmina **entra** no custo. Material comprado é maior que entregue.

### Cálculo
```
peso_barra = peso_peças_entregues × (comprimento_total / comprimento_peças)
           = peso_peças × (1 + lâmina_total / comprimento_peças)
```

### Campo no simulador
Configurado por tipo de corte e diâmetro. Geralmente automático baseado no setup da peça.

---

## Tabela consolidada (visão do pricing)

| Elemento | R$/Kg | R$/Pç | R$/m | Comportamento |
|---|:---:|:---:|:---:|---|
| VPP | — | ✅ | ✅ | Peso extra por densidade |
| Tolerância | — | ✅ | — | Variação dimensional |
| Lâmina | ✅ | ✅ | ✅ | Material perdido no corte |

**Regra mnemônica:** em R$/Kg, o cliente paga o peso real — apenas lâmina cai no custo AFS. Em R$/Pç, AFS absorve tudo menos o que está previsto — calcular todos. Em R$/m, comprimento real é faturado — tolerância é recuperada, mas VPP e lâmina entram no custo.

---

## Dúvidas frequentes

### "VPP e tolerância são a mesma coisa?"
Não. **VPP é de peso** (densidade × variação dimensional), **tolerância é dimensional** (comprimento, diâmetro). Relacionadas mas distintas.

### "Por que VPP em forjado é maior?"
Porque processo de forja tem variação dimensional maior que laminação. Peça forjada vem mais "grosseira" — precisa de mais material bruto.

### "Como calcular VPP se aço não tem especificação?"
Default conforme acabamento. Se cliente tem especificação específica, usar a dele.

### "Lâmina grande corrói margem?"
Sim, em barras de grande diâmetro. Por isso a escolha de serra importa — serra fita fina é mais cara operacionalmente mas economiza material.

### "O que é 'peso de partida' vs 'peso de orçamento'?"
- **Peso de partida:** peso total do material bruto comprado para gerar o pedido (inclui lâmina, perda de processo)
- **Peso de orçamento:** peso final que cliente recebe (material acabado)
- Em R$/Kg com acabado: divisor é o peso de orçamento, não peso de partida

---

## Relação com o RAF

No RAF, spread relacionado a VPP e tolerância aparece indiretamente:
- Se planejado e realizado divergem em margem aço (`ABCPER_MAR`), possível causa é VPP/tolerância mal calculada no simulador
- Ajuste: revisar parâmetros do simulador periodicamente comparando com realidade RAF

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[03 - Componentes de Custo]]
- [[05 - Modos de Venda]]
- [[08 - Simulador HTML - Arquitetura]]
- [[11 - Normas Técnicas]]
