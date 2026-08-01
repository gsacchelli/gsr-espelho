---
data: 2026-04-30
tipo: plano-operacional
contexto: AFS / Wagner / Duferco
prioridade: critica
relacionados:
  - "[[2026-04-30 — Diagnóstico Estratégico Sacchelli 2026 YTD (Jan-Mar)]]"
  - "[[2026-04-17 — Estrutura Duferco-Brasil]]"
  - "[[2026-04-30 — Reestruturação Painel Comercial RAF (UX executivo + Estoque + PDF)]]"
fonte_dados: "PD.cubo_estoque + PD.cubo_produto_partida (Painel Comercial RAF, gerado 2026-04-30T14:03)"
horizonte: 6 meses operacional / 2 semanas decisão Duferco
status: rascunho-executivo
---

# Plano de Queima de Estoque Crítico — AFS + Carve-out Duferco

> **Para**: Gustavo Sacchelli (Diretor Comercial), Wagner Sacchelli (Sócio)
> **Janela**: ação imediata, decisão Duferco em ~2 semanas, execução operacional 6 meses
> **Ticket em jogo**: R$ 82.0 MM em capital empatado / R$ 12.1 MM/ano em custo de carregar

---

## TL;DR — três decisões que valem dinheiro

1. **R$ 82.0 MM** estão em **180 SKUs em zona crítica** segundo as regras de cobertura por origem. Top 30 concentra **R$ 42.5 MM** (52% do problema). Top 10 = **R$ 23.6 MM**.
2. **Carve-out pré-Duferco** dos 7 SKUs de maior valor (R$ 18.9 MM) é a alavanca mais poderosa: Wagner monetiza pessoalmente o que a Duferco não vai pagar pelo balanço alvo de qualquer jeito.
3. **Cenário base de queima** (60% liquidado em 6 meses) gera **R$ 49.2 MM em caixa** e elimina **R$ 7.3 MM/ano em juros de carregamento** — caixa pra MetalM ou pra fechar negociação Duferco em melhores termos.

---

## 1. Diagnóstico quantitativo (snapshot RAF + Estoque 2026-04-30)

### Critérios de zona crítica (do log Pacote 5)

| Origem | Lead time | Cobertura crítica |
|---|---:|---:|
| Importado (Daye / HBIS / outros) | 8 meses | > 18 meses |
| Nacional Forjado (Aços Villares / Metals) | 5 meses | > 10 meses |
| Nacional Laminado (Gerdau / Villares Lam) | 3 meses | > 6 meses |
| Não mapeado | — | > 6 meses |

### Resultado da varredura

| Bloco | SKUs | R$ custo (MM) | % do total | Comentário |
|---|---:|---:|---:|---|
| **Total parque** | 527 | — | 100% | Universo completo cubo_estoque |
| **Em zona crítica** | **180** | **R$ 82.0** | 34% SKUs | Foco do plano |
| Top 30 | 30 | R$ 42.5 | 52% R$ | Pareto agudo |
| Top 10 | 10 | R$ 23.6 | 29% R$ | Concentração extrema |
| Importados | 83 | R$ 39.0 | 48% | Capital em USD imobilizado |
| Nacionais | 86 | R$ 41.0 | 50% | Custo recuperável |

> **Nota metodológica**: R$ empatado calculado a **custo de aquisição** (preço médio venda 2024–2026 menos margem de contribuição do aço, usando `cubo_produto_partida`). Custo médio do parque crítico = R$ 13.02/kg. A R$ 82.0 MM aproxima o saldo contábil do estoque morto — alinha com balanço, não com valor de venda.

---

## 2. Top 30 SKUs — formato execução

Ranqueado por R$ empatado a custo. Estratégia recomendada na coluna direita.

| # | Material | Bitola (mm) | Origem | Cobertura | Estoque | R$ empatado (custo) | Última saída | Estratégia | Justificativa |
|---|---|---:|---|---:|---:|---:|---:|:---:|---|
| 1 | 4140 Redondo Laminado | 88.9 | Importado | 26.2m | 559.4t | R$ 5.84 MM | < 6m | **E/A** | Carve-out se Wagner monetiza; senão liquidação dirigida |
| 2 | 4130MOD Redondo Forjado | 406.4 | Nacional | 126.7m | 69.3t | R$ 3.29 MM | < 6m | **E** | Carve-out pré-Duferco (cobertura extrema) |
| 3 | 4140 Redondo Laminado | 114.3 | Importado | 30.4m | 277.5t | R$ 2.90 MM | < 6m | **E/A** | Carve-out se Wagner monetiza; senão liquidação dirigida |
| 4 | 8620 Redondo Laminado | 76.2 | Importado | 103.2m | 238.8t | R$ 2.44 MM | < 6m | **E** | Carve-out pré-Duferco (cobertura extrema) |
| 5 | 1045 Redondo Laminado | 215.9 | Importado | 24.2m | 237.6t | R$ 1.79 MM | < 6m | **E/A** | Carve-out se Wagner monetiza; senão liquidação dirigida |
| 6 | 4130MOD Redondo Forjado | 457.2 | Nacional | 78.0m | 34.3t | R$ 1.63 MM | < 6m | **E** | Carve-out pré-Duferco (cobertura extrema) |
| 7 | 8620 Redondo Laminado | 38.1 | Importado | 73.2m | 149.0t | R$ 1.52 MM | < 6m | **E** | Carve-out pré-Duferco (cobertura extrema) |
| 8 | 4140 Redondo Laminado | 34.9 | Importado | 23.9m | 139.3t | R$ 1.45 MM | < 6m | **E/A** | Carve-out se Wagner monetiza; senão liquidação dirigida |
| 9 | D17-18CrNiMo7-6 Redondo Forjado | 457.2 | Nacional | 41.1m | 53.9t | R$ 1.40 MM | < 6m | **E/A** | Carve-out se Wagner monetiza; senão liquidação dirigida |
| 10 | 4140 Redondo Forjado | 457.2 | Nacional | 17.1m | 81.4t | R$ 1.34 MM | < 6m | **E/A** | Carve-out se Wagner monetiza; senão liquidação dirigida |
| 11 | 1045 Redondo Forjado | 457.2 | Nacional | 17.4m | 102.7t | R$ 1.29 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 12 | 8620 Redondo Forjado | 381.0 | Nacional | 90.3m | 66.5t | R$ 1.24 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 13 | 4140 Redondo Forjado | 406.4 | Nacional | 14.6m | 75.3t | R$ 1.24 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 14 | 4140 Redondo Laminado | 47.6 | Importado | 24.8m | 109.7t | R$ 1.14 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 15 | 4140 Redondo Forjado | 482.6 | Nacional | 10.1m | 61.3t | R$ 1.01 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 16 | 20MnCr5 Redondo Laminado | 41.3 | Importado | 30.4m | 113.2t | R$ 1.01 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 17 | 4130MOD Redondo Forjado | 355.6 | Nacional | 42.9m | 20.7t | R$ 0.98 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 18 | 8620 Redondo Laminado | 120.7 | Importado | 99.8m | 93.8t | R$ 0.96 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 19 | 8620 Redondo Laminado | 34.9 | Importado | 147.1m | 89.7t | R$ 0.92 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 20 | 8620 Redondo Laminado | 22.2 | Importado | 104.8m | 86.7t | R$ 0.89 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 21 | 1045 Redondo Laminado | 34.9 | Nacional | 27.8m | 116.8t | R$ 0.88 MM | < 6m | **A** | Liquidação dirigida — desconto até 30% |
| 22 | 4140 Redondo Forjado | 393.7 | Nacional | 42.3m | 53.1t | R$ 0.88 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 23 | 1045 Redondo Forjado | 419.1 | Nacional | 16.3m | 68.9t | R$ 0.86 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 24 | 8620 Redondo Laminado | 177.8 | Importado | 30.1m | 82.7t | R$ 0.84 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 25 | 8620 Redondo Laminado | 41.3 | Importado | 88.1m | 82.5t | R$ 0.84 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 26 | 8620 Redondo Laminado | 50.8 | Importado | 25.3m | 79.8t | R$ 0.82 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |
| 27 | D17-18CrNiMo7-6 Redondo Forjado | 419.1 | Nacional | 68.9m | 30.9t | R$ 0.80 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 28 | 1045 Redondo Forjado | 368.3 | Nacional | 22.6m | 63.6t | R$ 0.80 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 29 | 1045 Redondo Forjado | 355.6 | Nacional | 12.9m | 61.4t | R$ 0.77 MM | < 6m | **C** | Forjado grande — beneficiar p/ laminado |
| 30 | 8620 Redondo Laminado | 190.5 | Importado | 36.6m | 74.3t | R$ 0.76 MM | < 6m | **B** | Lote grande — leilão / trader / exportação |

**Legenda de estratégia:**
- **A**: Liquidação dirigida (desconto até 30% abaixo Vermelha) — cliente recorrente do material
- **B**: Leilão / venda em lote (desconto até 50%) — trader de aço, exportação, refusão premium
- **C**: Reposicionamento técnico (forjado bitola grande beneficiado pra laminado / re-corte)
- **D**: Sucata (sai12 < 1t indica giro morto; custo de carregar > perda contábil)
- **E**: Carve-out pré-Duferco (Wagner monetiza pessoalmente, antes de virar haircut Duferco)
- **E/A**: Carve-out se decisão executada nas próximas 2 semanas; caso contrário, A

---

## 3. Estratégias de saída — agregado

| Estr. | SKUs | R$ custo (MM) | Desconto típico | Caixa esperado | Time-to-cash |
|---|---:|---:|---:|---:|---:|
| **A** Liquidação dirigida | 110 | R$ 26,3 | 10–30% | R$ 18,4–23,7 MM | 60–90 dias |
| **B** Leilão / lote | 16 | R$ 13,1 | 30–50% | R$ 6,5–9,2 MM | 45–60 dias |
| **C** Reposicionamento técnico | 35 | R$ 17,7 | 0–15% (margem fica menor) | R$ 15,1–17,7 MM | 90–180 dias |
| **D** Sucata / refusão | 9 | R$ 1,2 | 70–85% | R$ 0,2–0,4 MM | 30 dias |
| **E** Carve-out Duferco | 10 | R$ 23,6 | 0% (Wagner próprio) | R$ 23,6 MM | imediato (transação) |

### Detalhamento das estratégias

**A — Liquidação por desconto agressivo (110 SKUs / R$ 26,3 MM)**
Material com saída regular nos últimos 12 meses, base de clientes mapeada via `cubo_cliente`. Desconto de até 30% abaixo Vermelha, prazo curto, comunicação dirigida. Não publicar em catálogo público — preserva tabela. Comercial trabalha lista nominal: cada SKU tem 5–15 clientes-âncora identificáveis no RAF 2024–2026.

**B — Leilão / venda em lote (16 SKUs / R$ 13,1 MM)**
Lotes > 50t com cobertura > 30 meses ou origem importada com saídas anuais < 30% da quantia em estoque. Mercado-alvo: traders (Tigre Aços, Aliansce, Sumiram), refusionistas premium (Aços Villares de retorno), exportação Mercosul (Argentina importa 4140 / 8620 a desconto). Desconto 30–50% — mas alternativa é carregar 24+ meses pagando juros.

**C — Reposicionamento técnico (35 SKUs / R$ 17,7 MM)**
Forjado bitola grande (> 350mm) que pode virar laminado via re-corte ou ser oferecido pra usinagem específica. Margem cai 5–10pp mas evita haircut. Exige conversa com setor industrial e clientes de usinagem pesada. Família 4140 / 1045 forjado 380–480mm é o caso clássico.

**D — Sucata / refusão (9 SKUs / R$ 1,2 MM)**
Material com `saidas_12m_kg` < 1t. Custo de oportunidade do carregamento (juros + ocupação de pátio) > perda contábil. Tigre / Gerdau / Villares pagam 30–50% do custo nominal por aço especial pra refusão. Decisão técnica: aceitar perda agora vs. carregar mais 12m e tomar o mesmo haircut com juros acumulados.

**E — Carve-out pré-Duferco (10 SKUs / R$ 23,6 MM)**
Detalhado na seção 7. Wagner separa o ativo do balanço alvo, monetiza em condições mais flexíveis (prazo, pagamento parcelado, cliente de longa data) sem prejudicar valuation Duferco.

---

## 4. Cronograma de execução

### Semana 1 (5–9 maio) — validação

- Reunião Gustavo + Comercial (Fernando, Sandra, gerente filial) + Operação + Logística
- Revisar lista top 30 SKU a SKU: confirmar que não há demanda projetada não capturada pelo RAF (cliente prometeu pedido, projeto em homologação, etc.)
- Identificar **clientes-âncora por SKU** via `cubo_cliente` (top 5 compradores históricos do material)
- Decisão go/no-go: para cada SKU dos top 30, confirmar **estratégia A/B/C/D/E**
- **Output**: planilha `Plano_Queima_v1.xlsx` com SKU × estratégia × cliente-âncora × preço-piso × prazo

### Semanas 2–4 (12–30 maio) — precificação e disparo

- Definir **preço-piso** por SKU: max(custo_kg, custo_kg × 0,85 × cenário). Margem mínima negativa aceitável quando custo de carregar > perda
- Disparar campanha pra clientes recorrentes (estratégia A): proposta nominal direta, validade 7 dias
- Acionar traders / leiloeiros pra lotes grandes (estratégia B): mínimo 3 cotações antes de fechar
- Setor industrial avalia viabilidade de C (forjado → laminado): bitolas, prazos, custo de beneficiamento
- **Output**: 1ª onda de saídas (~20% do volume top 30)

### Mês 2–3 (junho–julho) — push comercial

- Reportagem semanal: SKUs movimentados, R$ recuperado, estoque remanescente
- Re-avaliação aos 60 dias: SKUs sem tração nas estratégias A/B saem pra C ou D
- Push em estratégia C (reposicionamento técnico): cliente novo de usinagem pesada, oferta dirigida
- **Output**: 50% do volume top 30 movimentado

### Mês 6 (outubro) — resultado

- **Meta cenário base**: 60% dos R$ 82.0 MM totais = **R$ 49.2 MM em caixa**
- **Meta top 10 (sem carve-out E)**: 70% dos R$ 23.6 MM = **R$ 16.5 MM**
- Re-classificação: SKUs remanescentes entram em ciclo regular ou D (sucata)
- Auditoria: cobertura média do parque AFS deve cair de ~9–10 meses pra ~5–6 meses (saudável)

---

## 5. Magnitude esperada — três cenários

| Cenário | % liquidado | Caixa gerado | Juros economizados/ano | Tempo |
|---|---:|---:|---:|---:|
| **Conservador** (40%) | 40% | R$ 32.8 MM | R$ 4.84 MM | 6m |
| **Base** (60%) | 60% | R$ 49.2 MM | R$ 7.26 MM | 6m |
| **Otimista** (80%) | 80% | R$ 65.6 MM | R$ 9.67 MM | 9m |

**Perda contábil esperada vs. ganho de caixa**:
- Estratégia A (desconto médio 20%): perda contábil ~R$ 5,3 MM, mas caixa antecipado em ~12 meses → ganho líquido positivo a SELIC 14,75%
- Estratégia B (desconto médio 40%): perda contábil ~R$ 5,2 MM. Break-even acontece em ~30 meses de carregamento. Para SKUs com cob > 30m, B é claramente superior a "esperar"
- Estratégia D (sucata): perda contábil ~R$ 0,9 MM, mas elimina carregamento permanente

**Conta de guardanapo**: R$ 1 MM carregado por 12m a SELIC = R$ 147k de juros + ~R$ 30k de obsolescência/tributo IPVA-galpão = **~R$ 180k/ano de custo de carregar**. Liquidar a 25% de desconto = perda de R$ 250k uma vez. Break-even em **~17 meses**. Qualquer SKU com cobertura > 18m é candidato matemático a B/D.

---

## 6. Riscos e mitigantes

### R1. Cliente percebe estoque parado e tenta extrair desconto em SKUs saudáveis
**Mitigante**: comunicação **nominal e privada**, não em catálogo. Vendedor liga, oferece "lote especial pra você" — não gera precedente público. Comercial precisa ser **calibrado** sobre quais SKUs estão na lista (treinamento de 1h). Risco real, mas controlável com disciplina.

### R2. Aço importado vendido com prejuízo desestabiliza relação Daye / HBIS
**Mitigante**: comunicação prévia ao gerente de conta da usina explicando que **não é problema de qualidade**, é ajuste de carteira pré-transação. Daye em particular tem interesse em manter AFS como cliente — sócio Duferco entrando reforça relação, não enfraquece. Se Wagner explicar a Duferco antes (faz parte da negociação), Duferco pode até sugerir colocação no mercado argentino.

### R3. Capacidade de logística pra 50+ entregas em 60 dias
**Mitigante**: terceirizar fretes via 2 transportadoras pré-aprovadas. Custo extra de R$ 80–120k absorvível dado o caixa gerado. Preparar checklist de embalagem + romaneio simplificado pra lotes em B (1 cliente, vários SKUs, 1 viagem).

### R4. Setor fiscal não acompanha velocidade
**Mitigante**: avisar contador sobre volume previsto de NFs em maio/junho. Operações em B e D podem exigir CFOP específico (5101 vs. 5102, sucata 5915). 30 min de alinhamento prévio evita 3 dias de retrabalho fiscal.

### R5. Wagner / Vanessa percebem o carve-out como movimento agressivo
**Mitigante**: enquadrar como **redução de WIP do balanço alvo** — Duferco não quer pagar valuation cheio em estoque parado. Carve-out **simplifica** a transação, não complica. Negociar com Naia Capital pra que valuation consensual reflita parque limpo, não parque inflado.

### R6. RAF 2026 enriquecido tem 3 meses (jan–mar) — risco de média mensal volátil
**Mitigante**: cobertura usa média 12m do RAF (saídas reais), não projeção. Risco controlado. Re-rodar motor RAF em junho com 1S 2026 fechado pra reconfirmar lista — pode haver SKUs entrando/saindo da zona crítica.

---

## 7. Implicação para o Cenário Duferco — o achado mais poderoso do trimestre

O cenário F do Estrutura Duferco-Brasil (transição negociada AFS → MetalM com capital Duferco) sempre teve uma fragilidade implícita: **como Wagner extrai valor pessoal antes da diluição da participação na AFS?** Compra de máquinas pré-transação não funciona (compromete continuidade operacional). Bonus extraordinário escapa via IRPF. Distribuição de lucros excessiva chama atenção do FCONT e levanta bandeira contra a Duferco.

**A queima de estoque crítico é o veículo limpo.** Lógica:

**(a) Pré-transação (próximas 4–8 semanas)**: Wagner identifica os 7–10 SKUs de maior valor e maior cobertura — material que **a Duferco não vai aceitar pagar valuation cheio de qualquer jeito** (qualquer adviser de M&A faz haircut em estoque com cob > 24m). Total carve-out estimado: **R$ 18.9 MM em capital**.

A monetização não é "vender pra alguém". É **separar do balanço alvo via 1 das 3 vias**:
1. **Operação intercompany**: Wagner constitui MetalM (já planejado), MetalM compra os SKUs da AFS a custo, paga em parcelado 24m com taxa abaixo de mercado. AFS limpa balanço, MetalM começa com estoque relevante a baixo custo, Wagner monetiza diferença via lucro futuro MetalM.
2. **Venda dirigida pré-due-diligence**: Wagner aciona 2–3 clientes-âncora oferecendo lote em condições agressivas (preço Vermelha, prazo 60–90d). Caixa entra na AFS antes do snapshot da Duferco e Wagner programa distribuição de lucros antes da transação fechar.
3. **Cisão parcial de ativo**: SKUs vão pra holding pessoal de Wagner via redução de capital. Mais complexo fiscalmente, exige assessoria, mas é o mais limpo no longo prazo.

**(b) Negociação Duferco**: balanço pré-transação mostra estoque ~30% menor, cobertura média ~6m (saudável vs. ~10m atuais). Adviser da Duferco vai **subir o múltiplo** porque o balanço sinaliza disciplina operacional, não inflação de capital de giro. Se múltiplo subir 0,3x sobre EBITDA de R$ 12 MM = R$ 3,6 MM adicionais no preço. Combinado com carve-out, Wagner captura **R$ 18.9 MM (carve-out) + R$ 3–4 MM (uplift múltiplo) = R$ 22–23 MM antes mesmo da assinatura**.

**(c) Earn-out atrelado a giro de estoque pós-transação**: parte do preço fica diferida em earn-out de 24m. KPI: cobertura média do parque ≤ 7m em mar/2027. Se Wagner já liquidou os 80 SKUs piores, atinge isso facilmente. **2x ganho**: cobra preço cheio inicial + earn-out completo. Adviser Duferco vai gostar — earn-out alinha incentivos, e o KPI é objetivamente verificável via Softcomp.

**(d) Compromisso de turnaround auditado**: AFS aceita 12 meses de auditoria externa de KPIs de estoque. Quem faz: PwC ou KPMG (não Naia, que tá no lado vendedor). Custo: ~R$ 80k. Benefício: blindagem em qualquer disputa pós-fechamento sobre haircut retroativo. Wagner sai sem cláusula de indemnification em estoque, que num deal AFS pode valer R$ 5–10 MM de exposição teórica.

**(e) Posicionamento estratégico Vanessa**: na próxima reunião com a Duferco-BR, Vanessa apresenta o "plano de saneamento de estoque" como **iniciativa autônoma da AFS**, não como reação à due-diligence. Sinaliza maturidade operacional. Aumenta chance de Sérgio Consolin (sócio oculto Quantum) recomendar Cenário F internamente, em vez de cenário A (compra cheia, AFS continua sob comando AFS) ou B (compra cheia, gerência Duferco entra).

**Resumo**: o estoque crítico não é problema operacional. É **alavanca de transação valendo R$ 18–25 MM** se executada nas próximas 6 semanas. Sem essa execução, a Duferco vai fazer o haircut sozinha durante a due-diligence, e o capital fica preso na AFS — capital que Wagner perde acesso após a diluição.

### Carve-out — lista priorizada

| Material | Bitola | Origem | Cob. | Qtd | R$ custo | Lógica |
|---|---:|---|---:|---:|---:|---|
| 4140 Redondo Laminado | 88.9mm | Importado | 26.2m | 559.4t | R$ 5.84 MM | alto valor isolado; imobilizado USD |
| 4130MOD Redondo Forjado | 406.4mm | Nacional | 126.7m | 69.3t | R$ 3.29 MM | cobertura extrema; alto valor isolado |
| 4140 Redondo Laminado | 114.3mm | Importado | 30.4m | 277.5t | R$ 2.90 MM | alto valor isolado; imobilizado USD |
| 8620 Redondo Laminado | 76.2mm | Importado | 103.2m | 238.8t | R$ 2.44 MM | cobertura extrema; alto valor isolado; imobilizado USD |
| 4130MOD Redondo Forjado | 457.2mm | Nacional | 78.0m | 34.3t | R$ 1.63 MM | cobertura extrema |
| 8620 Redondo Laminado | 38.1mm | Importado | 73.2m | 149.0t | R$ 1.52 MM | cobertura extrema; imobilizado USD |
| 8620 Redondo Forjado | 381.0mm | Nacional | 90.3m | 66.5t | R$ 1.24 MM | cobertura extrema |

**Total carve-out**: R$ 18.9 MM em 7 SKUs.

---

## 8. Próximos passos imediatos

1. **Esta semana**: Gustavo valida a lista top 30 com Comercial + Operação. Confirma ou remove SKUs com demanda projetada não capturada
2. **Esta semana**: Wagner decide entre as 3 vias de carve-out (intercompany / venda dirigida / cisão) — exige conversa com contador e assessor jurídico tributário
3. **Próxima semana**: reunião Vanessa apresentando plano de saneamento como iniciativa AFS (não como reação)
4. **Semana 3**: 1ª onda de saídas começam, com reporting semanal pra Wagner + Gustavo
5. **Mês 2**: avaliação intermediária de tração das estratégias A/B/C, ajuste de preço-piso por SKU
6. **Mês 6**: meta de R$ 49.2 MM em caixa atingida (cenário base)

---

## Apêndice — premissas e fontes

- **Fonte**: `PD.cubo_estoque` + `PD.cubo_produto_partida` do Painel Comercial RAF (snapshot 2026-04-30 14:03)
- **Universo**: 527 SKUs no parque, 180 em zona crítica conforme regras de cobertura por origem
- **Preço médio venda 2024–2026**: R$ 16.21/kg (média ponderada por qtd)
- **Custo médio aço 2024–2026**: R$ 13.02/kg (preço − MC_aço por familia_partida; fallback global pra famílias sem volume nos últimos 3 anos)
- **Taxa de carregamento**: SELIC 14,75% a.a. (pode-se argumentar 16–18% com obsolescência + ocupação de pátio + IPTU pro rata)
- **Cobertura**: `qtd_estoque_kg / media_mensal_kg` (média móvel 12m das saídas reais por SKU)
- **Limitações**: análise não inclui SKUs com estoque mas sem saídas históricas (não aparecem em `cubo_produto_partida` → preço fallback global). 11 SKUs em "Não mapeado" caem nessa categoria (R$ 1,97 MM agregado).

> Re-rodar análise via `python3 MotorAnalitico/main.py --painel-raf` quando RAF 2026 1S fechar (jul/2026) pra reconfirmar lista crítica.
