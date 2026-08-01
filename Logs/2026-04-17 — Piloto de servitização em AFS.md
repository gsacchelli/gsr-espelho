---
status: em-teste
tipo: hipótese
categoria: modelo-de-negócio
data-formulação: 2026-04-17
prazo-validação: 2026-10-17
tags: [hipótese, afs, metalm, servitização, piloto]
---

# 2026-04-17 — Hipótese: Piloto de servitização em AFS antes de MetalM greenfield

> **Rascunho estruturado — precisa de validação do Gustavo** antes de virar plano executivo.

---

## Hipótese

**Acreditamos que** pilotar um catálogo de 3 serviços cobrados explicitamente dentro da AFS (operação existente) **vai gerar aprendizados sobre adesão, pricing e mudança cultural**, suficientes para **reduzir o risco executional da MetalM greenfield em ≥50%**, antes de comprometer capital com parceria Duferco ou planta nova.

**Saberemos que é verdade se**, em 6 meses:

- Pelo menos **2 dos 3 serviços piloto** apresentarem adesão por mais de **5 clientes-tipo** (contratos recorrentes ≥ 3 meses)
- **Margem incremental** dos serviços vendidos for ≥ **15 p.p. acima** da margem de aço puro desses clientes
- **Aprendizado documentado** sobre precificação, operação e venda (estilo [[Aprendizados]]) cobrindo 5+ insights não-óbvios por serviço
- **Resistência do time comercial** mapeada e mitigada (ou bloqueio identificado — que é aprendizado também)

---

## Razão (por que achamos isso)

1. **Custo de testar em AFS é baixo:** estrutura já existe (corte, armazenagem, relacionamento comercial). Testar em MetalM greenfield exige CapEx + contratação + marca nova — custo 10-20x maior.

2. **Servitização exige mudança cultural mais do que capacidade técnica.** Cultura só se testa na prática — não em plano de negócios. Ver [[Servitização]].

3. **Risco maior da tese MetalM** não é se o cliente quer serviço (ele diz que quer). É se o cliente **paga explicitamente** pelo serviço quando pode ter "de graça" do concorrente tradicional. Só o piloto responde isso.

4. **Remuneração atual AFS (fixo + 2% s/IPI)** não incentiva venda de serviço. O piloto força o confronto com a alavanca comportamental — ver [[Pricing - Precificação]] e conexão com remuneração (tratar como decisão separada).

---

## Os 3 serviços candidatos a piloto

### Serviço 1 — Corte sob demanda com dimensionamento garantido
- **Cobrança:** R$/corte fixo + R$/tolerância estreita (se aplicável)
- **Proibição:** "corte cortesia" desaparece do vocabulário
- **Métrica de adesão:** % de pedidos que contratam corte vs puro
- **Resistência esperada:** vendedor vai dizer "cliente não vai aceitar pagar pelo que era cortesia"

### Serviço 2 — Estoque do cliente consignado na base AFS
- **Cobrança:** mensalidade fixa de armazenagem + mínimo de giro mensal
- **Valor para cliente:** reduz capital empatado, acesso em ≤24h
- **Métrica de adesão:** clientes ativos × tonelagem média consignada
- **Resistência esperada:** exige redesenho de processo de faturamento e inventário

### Serviço 3 — Dashboard de carteira do cliente (inteligência de consumo)
- **Cobrança:** opcional no início (valor via dados + upsell), cobrado depois
- **Entregável:** relatório mensal com consumo, tendência, sugestões de otimização
- **Métrica de adesão:** clientes que **solicitam** relatório vs. que ignoram
- **Resistência esperada:** exige capacidade analítica — ver Motor Analítico Sacchelli (já em construção)

---

## Experimento (desenho)

### Recorte
- **Clientes-alvo:** 8-12 clientes médios da AFS, com perfil industrial recorrente
- **Unidade:** começar em **Guarulhos** (infra logística mais saudável, ver memória AFS)
- **Time:** designar 2 vendedores "piloto" com perfil mais receptivo + engenheiro de aplicação
- **Duração:** 6 meses, revisão mensal

### Medição
- Dashboard semanal de adesão, margem, resistência do time
- Entrevistas com cliente em D+30 e D+90
- Retrospectiva mensal com time piloto

### Controle
- Grupo de controle: clientes-irmão sem oferta dos serviços
- Comparar evolução de ticket, margem, churn

---

## Resultado esperado

**Cenário positivo (validação):**
- Adesão ≥ 5 clientes em 2 serviços
- Margem incremental ≥ 15 p.p.
- → **Luz verde para MetalM com servitização como posição central**
- → Próximo passo: parceria Duferco com contrato blindado

**Cenário negativo (refutação):**
- Adesão < 3 clientes ou margem incremental < 5 p.p.
- → **Revisar posicionamento MetalM** para "parceiro técnico" (Opção A da decisão linkada)
- → Ou reformular portfólio de serviços

**Cenário inconclusivo:**
- Adesão parcial, resistência cultural forte
- → Estender piloto + atacar alavancas (remuneração, comunicação)
- → Decisão adiada em 6 meses com condições explicitadas

---

## Resultado observado
*(preencher após piloto)*

---

## Conclusão
*(preencher após piloto: validada / refutada / inconclusiva)*

---

## Próximo passo
*(preencher após piloto: escalar / pivotar / descartar)*

---

## Riscos da hipótese

- **Piloto enviesado:** vendedores piloto são "os melhores" → resultado infla
  - **Mitigação:** escolher perfil receptivo + médio, não apenas o top
- **Clientes-piloto não representativos:** escolha por conveniência
  - **Mitigação:** definir critério objetivo de seleção (setor, volume, histórico)
- **Falta de monitoria:** sem dashboard, aprendizado se perde
  - **Mitigação:** RAF já tem estrutura analítica; adaptar para capturar piloto
- **Conflito com carteira atual:** cliente-tabelista pode estranhar mudança
  - **Mitigação:** piloto isolado, não anunciar como "novo modelo AFS"

---

## Frameworks aplicados
- [[Hipóteses de Negócio]] — estrutura e ordenação por risco × custo
- [[Servitização]] — espectro e exigências culturais
- [[Pricing - Precificação]] — precificação explícita como condição
- [[Custo de Servir]] — entrada obrigatória no desenho de cada serviço
- [[Cliente Ideal]] — refinamento do ICP real via piloto
- [[Sistema de Decisão - C-Level]] — Tipo 1 bem escolhido reduzido para Tipo 2 via piloto

## Conexões
- [[Hipóteses de Negócio]] (hub)
- [[2026-04-17 — Posicionamento MetalM - Servitizador]] (decisão dependente)
- [[Ideias em Desenvolvimento]] (origem da ideia)
