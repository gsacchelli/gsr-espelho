---
tipo: higiene-portfolio
domínio: estoque
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [fora-de-padrão, higiene, portfolio, obsolescência]
---

# 06 — Fora de Padrão

## Conceito

**"Fora de Padrão"** é o bucket onde caem SKUs que **não se encaixam** nas 207 combinações canônicas da Família Canônica (ver [[01 - Família Canônica]]).

Pode ser por:
- **Aço não mapeado** na lista oficial (ex: inox, carbono especial)
- **Bitola fora das faixas** S/N 1-6
- **Acabamento especial** não catalogado
- **Material engenheirado** com especificação única de cliente

---

## Por que importa

### Visibilidade de portfolio
Sem esse bucket, SKUs "fora de padrão" ficariam espalhados ou invisíveis. O bucket força **reconhecimento** dessa fatia do estoque.

### Fonte de obsolescência silenciosa
Material engenheirado que cliente não retirou, compra pontual errada, liga que entrou sem análise — tudo pode virar estoque parado.

### Sinal de expansão de portfolio
Se "Fora de Padrão" cresce com um tipo específico (ex: muitos pedidos de inox), pode ser **hora de formalizar na taxonomia** — criar famílias para esse tipo.

---

## Características típicas

### Distribuição esperada
Em estoque saudável:
- **< 5% do valor total** em "Fora de Padrão" é normal
- **5-10%** é atenção
- **> 10%** é problema — ou portfolio mal mapeado ou compra errática

### Perfil dos itens
- Alto valor unitário (engenheirados, ligas especiais)
- Baixo giro
- Poucos clientes (às vezes único)
- Difícil de reaproveitar se cliente original cancela

---

## Gestão

### Processo recomendado (mensal)

#### Etapa 1 — Revisão da lista
Abrir painel de estoque → aba "Fora de Padrão" → listar SKUs.

#### Etapa 2 — Classificar cada item

**Material válido, em giro:** ok, deixar
- Cliente específico compra regularmente
- Margem boa
- Deixa no bucket mas monitorar

**Material válido, sem giro > 180d:** decisão
- Cliente original sumiu?
- Possível reaproveitar?
- Reduzir preço para mercado?
- Descontinuar?

**Erro de cadastro:** corrigir
- SKU que deveria estar em família padrão mas não classificou corretamente
- Atualizar cadastro

**Candidato a nova família:**
- Tipo recorrente aparecendo há meses
- Volume começa a justificar
- Formalizar na taxonomia (ver [[02 - Faixas de Bitola]])

#### Etapa 3 — Ações
Para cada item, decisão:
- Manter (código verde)
- Monitorar (amarelo)
- Descontar/promover (amarelo-alaranjado)
- Descontinuar/baixa (vermelho)

---

## Material engenheirado — tratamento especial

### O que é
Material com especificação única do cliente. Geralmente:
- Cliente enviou desenho específico
- Corte/usinagem customizada
- Impossível reaproveitar para outro cliente

### Pricing e venda
- **Exclusivamente em R$/Pç** (ver [[Sistema Operacional Comercial/02 Precificação/05 - Modos de Venda]])
- Custeio pelo peso de partida
- Simulador bloqueia Kg e m

### Risco de obsolescência
Se cliente cancela:
- Material vira quase obsoleto
- Pode ser **revendido** para outro cliente se especificação compatível
- Pode ser **retornado** para usina se acordado
- Pode ser **sucata** em último caso

### Mitigação
- **Sinal contratual:** pedido engenheirado requer sinal do cliente (comprometimento financeiro)
- **Prazo de retirada:** cliente tem X dias para retirar, depois custo de armazenagem passa
- **Cláusula de cancelamento:** se cancelar, cliente paga material + custo operacional

---

## Critérios para formalizar nova família

Se um tipo aparece frequentemente em "Fora de Padrão":

### Triggers
- **Volume:** > X kg ou > Y R$ de estoque recorrente por 3+ meses
- **Demanda:** > N cotações por trimestre para o tipo
- **Clientes:** múltiplos clientes, não concentrado em 1
- **Margem:** boa margem (justifica operacionalizar)

### Processo
1. Analisar o tipo (ex: inox AISI 304 redondo laminado)
2. Definir faixas de bitola relevantes
3. Mapear 1-2 acabamentos mais comuns
4. Adicionar à `FAMILIAS_PADRAO` em:
   - Painel de Estoque
   - Simulador de Precificação
   - Motor Analítico
5. Atualizar [[01 - Família Canônica]] com as novas combinações
6. Criar tabelas de preço Verde/Amarela/Vermelha para o tipo no Softcomp
7. Comunicar ao time comercial

---

## Indicadores a acompanhar

### No painel de estoque
- **% do valor/peso em Fora de Padrão**
- **Número de SKUs Fora de Padrão**
- **Idade média** dos itens Fora de Padrão (dias parado)
- **Top 10 SKUs Fora de Padrão por valor**

### Evolução temporal
- Comparar com trimestre anterior: aumentou ou diminuiu?
- Se aumentou: investigar tipo/causa

---

## Alertas recomendados (futuro)

No Motor Analítico v2 ou Painel de Estoque v3:

- Alerta **amarelo** se novo SKU Fora de Padrão é adicionado
- Alerta **vermelho** se % total Fora de Padrão > 10% do estoque
- Alerta **vermelho** se um item Fora de Padrão fica 365+ dias parado
- Alerta **verde (informativo)** se um tipo está crescendo — candidato a formalização

---

## Lacunas conhecidas na gestão atual

### 1. Sem revisão sistemática
Revisão de Fora de Padrão não acontece em cadência. Acumula.

### 2. Sem política clara de descontinuação
Item que deveria sair do portfolio fica por "possível cliente interessado um dia".

### 3. Sem cobrança de armazenagem para engenheirados parados
Cliente cancela, AFS absorve. Sem cláusula contratual robusta.

### 4. Sem base histórica
Não sabemos quanto % do estoque é "Fora de Padrão" ao longo dos últimos anos. Dificulta benchmark.

---

## Prioridade

**Prioridade baixa-média** na agenda atual. Não é fonte imediata de risco, mas:
- Se Cenário F (MetalM) materializar, limpar portfolio AFS ajuda transição
- Se AFS for vendida para Duferco, portfolio limpo = valuation mais claro

**Ação recomendada (30 min/mês):** revisão mensal dos Top 10 itens Fora de Padrão, decisão caso a caso.

---

## Conexões

- [[00 - Visão Geral Estoque]]
- [[01 - Família Canônica]]
- [[02 - Faixas de Bitola]]
- [[04 - Painel de Estoque v2]]
- [[05 - Movimentação e Giro]]
- [[Sistema Operacional Comercial/02 Precificação/05 - Modos de Venda]]
