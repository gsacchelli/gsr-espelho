---
tipo: referência-técnica
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [normas, en-10060, metals, especificações, dimensional]
---

# 11 — Normas Técnicas

## Propósito

Referências normativas que governam **tolerâncias dimensionais**, **especificações de material** e **condições de fornecimento** que afetam pricing e aceitação pelo cliente.

Conhecimento das normas é crítico para:
- Precificar corretamente (tolerâncias cobertas no custo)
- Atender especificação do cliente
- Defender pricing frente a cliente que questiona (ex: "por que tão caro?")

---

## Normas dimensionais principais

### EN 10060 — Aço redondo laminado a quente
Norma europeia para **barras redondas laminadas** para uso geral.

**Tolerâncias por diâmetro:**
- Até 25 mm: ±0,3 a ±0,6 mm
- 26-50 mm: ±0,6 a ±1,0 mm
- 51-100 mm: ±1,0 a ±1,5 mm
- 101-200 mm: ±1,5 a ±2,5 mm
- \> 200 mm: negociação específica

**Comprimento:**
- Comprimento comercial (5 a 12 m): ±100 mm normalmente
- Comprimento fixo: ±30 mm

**Retidão:** 0,2% a 0,4% do comprimento.

**Peso:** variação permissível (VPP) de **±1%** em laminado.

### EN 10277 — Aços para usinagem
**Aços descascados, trefilados, retificados.**

**Tolerâncias mais apertadas:**
- h9: usinagem geral
- h11: usinagem média
- h7: usinagem fina

### DIN/ISO específicos por aço ferramenta
Aços como D2, D3, M2, H13 têm especificações próprias de fornecimento (forjado, laminado, retificado) conforme padrão do fabricante.

### ABNT NBR (brasileiras equivalentes)
Em muitos casos, NBR segue EN com adaptações. Mercado brasileiro aceita ambas.

---

## Variação de peso (VPP)

### Norma de origem
Faixa permitida pela norma para que uma barra "nominal X" tenha peso real dentro do aceitável.

### Valores operacionais Sacchelli

| Acabamento | VPP default Sacchelli | Justificativa |
|---|---|---|
| Laminado | 1% | Processo de laminação moderno tem precisão boa |
| Forjado | 5-6% | Processo de forja tem variação dimensional maior |

Configurável por família de produto no Setup do simulador.

### Quando usar VPP diferente do default
- Cliente com especificação mais rigorosa (reduzir VPP, aumentar preço)
- Norma específica do setor (aero, militar) que exige tolerância apertada
- Fornecedor com histórico de variação acima/abaixo (ajustar na fonte)

---

## Tolerância dimensional aplicada

### Quando tolerância entra no preço
Ver [[05 - Modos de Venda]] e [[06 - VPP Tolerância e Lâmina]]:

- **R$/Kg:** não entra (peso real é faturado)
- **R$/Pç:** entra (AFS absorve material extra)
- **R$/m:** não entra (comprimento real é faturado)

### Cálculo prático
Se tolerância é +3/−0 mm em peça de 1000 mm, AFS pode cortar qualquer comprimento entre 1000 e 1003 mm.

Em R$/Pç, precificar assumindo **pior caso** (cliente recebe 1003 mm, pesa 0,3% mais). Incluir no custo.

---

## Especificações comuns de aço

### Carbonos
- 1020, 1045 (SAE)
- ABNT equivalente: 1020, 1045
- Aplicação: peças simples, uso geral

### Beneficiáveis
- 4140, 4340, 8620, 8640 (SAE)
- Aplicação: peças mecânicas, eixos, engrenagens
- Tratamento: têmpera + revenido típico

### Cementáveis
- 8620, 4320, 18CrNiMo7-6
- Aplicação: peças com superfície dura (engrenagens, eixos)
- Tratamento: cementação + têmpera + revenido

### Aços ferramenta
- D2, D3 (para frio)
- H13 (para quente)
- M2 (para corte)
- Aplicação: ferramentaria, matrizes, estampos

---

## Certificações comuns

### Por exigência setorial
- **Automotivo (IATF 16949):** rastreabilidade de lote, certificação por corrida
- **Petroleum (API):** composição química garantida
- **Aeroespacial (AS9100):** testes destrutivos por lote
- **Ferroviário:** certificações dimensionais e metalúrgicas

### Por tipo de teste
- **Composição química:** espectrometria
- **Propriedades mecânicas:** tração, impacto, dureza
- **Dimensional:** calibre, paquímetro, 3D scan
- **Metalografia:** microscopia óptica/eletrônica
- **Ultrassom:** defeitos internos
- **Partículas magnéticas / líquido penetrante:** defeitos superficiais

### Precificação
Certificação cobrada como **serviço separado** quando solicitada. Custo real **quase zero** quando emitida internamente (só laudo); margem oculta próxima de 100%. Ver [[03 - Componentes de Custo]].

---

## Tratamentos térmicos comuns

### Recozimento
- Amolece o material, alivia tensões
- Cliente: facilita usinagem
- Custo: médio

### Normalização
- Refina grão, homogeneíza
- Cliente: uniforme para tratamento posterior
- Custo: baixo-médio

### Têmpera + Revenido
- Endurece superfície e miolo
- Cliente: resistência a desgaste, impacto
- Custo: médio-alto
- Fornecedores: TT externos (CTT, Brasimet, etc.)

### Cementação
- Endurece só a superfície
- Cliente: engrenagens, eixos
- Custo: alto
- Processo especializado

### Solubilização
- Para inox, remove precipitados
- Cliente: inox austenítico

### Processamentos AFS
Alguns TTs internos, mas a maioria é terceirizada. Pricing: terceiro × (1 + margem AFS).

---

## Rastreabilidade

### Padrão Sacchelli
Cada lote de aço tem **certificado de origem** da usina. AFS mantém rastreabilidade barra → OS → cliente.

### Campos-chave no Softcomp
- `ABCMAT_*` = dados do material de partida
- `ABCCOR_*` = corrida / lote de origem
- `ABCCER_*` = certificação emitida

### Para clientes que exigem
- **Certificado do fornecedor** (usina)
- **Rastreamento da corrida**
- **Histórico dimensional e térmico**

Custa tempo para emitir, mas é cobrado.

---

## Fiscal e Impostos

### ICMS
- ST (Substituição Tributária) aplicável em alguns estados
- Cobrança antecipada
- Recuperável para cliente contribuinte

### IPI
- Aplicável a aço (tabela TIPI)
- Alíquota varia por produto
- Recuperável

### PIS/COFINS
- **Atenção à base de cálculo:** PIS/COFINS **NÃO** incide sobre ICMS
- Erro comum: calcular sobre base cheia (inflando o custo)
- Implicação: simulador deve subtrair ICMS antes de calcular PIS/COFINS

### Diferencial de alíquota (DIFAL)
- Venda interestadual para não-contribuinte
- Recolhimento parcial no estado de origem, parcial no de destino

### Arbitragem fiscal (nota crítica)
Trefita/Torres tem unidade em **Contagem-MG**. Para clientes MG/ES, isso permite arbitragem fiscal resultando em gap de **4-8%** vs AFS (sediada em SP).

Ver `project_trefita_torres_intel` (memória).

---

## Fontes e atualização

### Onde consultar as normas atualizadas
- EN 10060, EN 10277, etc.: CEN (comitê europeu)
- ABNT NBR: site ABNT (acesso pago)
- AMS (aeroespacial): SAE International
- API (petróleo): American Petroleum Institute

### Revisão de normas
Normas têm revisões periódicas (5-10 anos). Verificar se versão usada pela AFS está vigente.

### Atualização desta nota
Quando norma específica mudar de forma relevante para pricing, atualizar aqui.

---

## Aplicação no simulador

O simulador tem:
- Hint EN 10060 / Metals no campo VPP
- Opções de acabamento (laminado, trefilado, descascado, forjado) que carregam VPP default
- Tolerância configurável quando aplicável

**Lacuna:** simulador não tem catálogo completo de certificações/TT com preços. Entrada manual hoje.

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[03 - Componentes de Custo]]
- [[05 - Modos de Venda]]
- [[06 - VPP Tolerância e Lâmina]]
- [[08 - Simulador HTML - Arquitetura]]
- [[03 Estoque/01 - Família Canônica]]
- `project_trefita_torres_intel` (memória)
