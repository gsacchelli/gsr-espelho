# Pricing — Precificação

## Definição
Decisão sobre **quanto capturar do valor criado** para o cliente, sob restrição de mercado, custo e posicionamento.

Pricing não é cálculo — é **estratégia expressa em números**. Mudar preço sem mudar posicionamento é tática; mudar preço **para expressar** posicionamento é estratégia.

---

## As 3 abordagens clássicas

### 1. Cost-plus (custo + markup)
- Parte do custo, adiciona margem-alvo
- **Vantagem:** simples, defende de venda abaixo do custo
- **Limitação:** ignora valor percebido e mercado — deixa dinheiro na mesa no cliente-A, perde deal no cliente-C
- **Uso:** piso absoluto, não decisão de venda

### 2. Market-based (referência de mercado)
- Preço relativo ao concorrente / tabela de mercado
- **Vantagem:** aderência a realidade competitiva
- **Limitação:** vira commodity rapidamente; "desconto sobre tabela" é corrida ao fundo
- **Uso:** validação de posicionamento (estou no range certo?)

### 3. Value-based (valor percebido)
- Preço reflete **valor econômico para o cliente específico**
- **Vantagem:** captura máximo do valor criado, reforça posicionamento
- **Limitação:** exige entender economia do cliente; difícil em commodity
- **Uso:** onde existe proposta de valor real (ver [[Proposta de Valor]])

**Na prática:** toda empresa industrial precisa das 3. Cost-plus define o piso, market-based define a faixa, value-based captura o prêmio.

---

## Arquitetura de pricing (componentes)

### Preço-base
- Por produto/SKU, refletindo custo + margem-alvo
- Deve ser **visível para time comercial** (não "segredo do diretor")

### Política de desconto
- Descontos **estruturados** (volume, prazo, combinação)
- **Alçadas por nível** (quem aprova o quê)
- **Sempre com contrapartida** (Give/Get)

### Pricing por segmento/cliente
- Diferentes tabelas para diferentes ICPs
- Diferencial justificado por [[Custo de Servir]] + valor percebido
- Não é "quem reclama mais ganha desconto"

### Precificação de serviços adicionais
- Cada serviço do portfólio tem **preço explícito**
- "Cortesia" é subsídio invisível — proibido por default
- Ver [[Servitização]]

---

## Princípio: pricing é conversa sobre escopo

**Erro clássico:** discutir preço sem fechar escopo.

Sequência correta:
1. Definir escopo (o que é entregue, em qual padrão, com qual prazo)
2. Calcular custo de servir real para esse escopo
3. Calcular valor percebido pelo cliente para esse escopo
4. **Depois** negociar preço

Inversão dessa sequência é a causa #1 de margem ruim.

---

## Estrutura de negociação: 3 propostas com escalada

Toda negociação relevante deve ter 3 opções:

1. **Conservadora** — escopo mínimo, preço menor, menor valor entregue
2. **Intermediária** — escopo balanceado (geralmente a escolha natural)
3. **Premium** — escopo ampliado, preço superior, valor máximo

Vantagens:
- Cliente escolhe **escopo**, não só preço
- Você ancora no intermediário (psicologia da comparação)
- Reduz resposta "caro demais" (há alternativa explícita)

---

## Give/Get: regra de ouro

**Nunca aceite concessão sem contrapartida concreta.**

Mesmo que a contrapartida seja simbólica (dados, preferência, prazo longo), deve ser explícita. Ceder sem contrapartida:
- Destrói percepção de valor (preço "inflado")
- Treina o cliente a pedir mais
- Desalinha incentivos internos
- Prejudica carteira inteira (precedente vira política)

Regras práticas:
- Não aceitar "refaz sem custo" como cortesia
- Não fechar preço antes do escopo aprovado
- Não confundir **urgência do cliente** com **sua obrigação contratual**

---

## Métricas-chave

- **Margem de contribuição (MC) %** — por item, cliente, família
- **Corredor de MC** (faixa de variação aceitável)
- **VPP — Variação de preço praticado** (aderência à tabela)
- **Win rate por faixa de desconto** (quanto mais desconto, mais ganha?)
- **MC líquida** (MC − custo de servir)

---

## Erros comuns

- Precificar **item por item** sem considerar cesta
- Dar desconto **antes de precisar** (antecipar queda é política disfarçada)
- Não revisar tabela com frequência (inflação corrói sem aviso)
- **Não diferenciar** pricing por ICP (cliente A paga o mesmo que cliente C — subsídio invisível)
- Confundir **preço** com **margem** (cliente com preço alto e MC ruim é pior que preço médio e MC ok)
- Remunerar vendedor por **receita** — incentiva desconto fácil (ver conexão com Custo de Servir)

---

## Aplicação — AFS / MetalM

**AFS hoje:**
- 3 tabelas de preço (verde, amarela, vermelha) — estrutura existe
- Abaixo da vermelha, só diretor aprova — alçada funciona
- Remuneração (fixo + 2% s/IPI) **não está atrelada a MC** — desalinhado com pricing saudável
- Simulador de Precificação HTML (projeto ativo) já calcula MC, DESP e custo de servir por item — ferramenta está pronta, adoção é o gargalo
- Diagnóstico de 29.748 cotações mostrou ruído em perdas por preço — maturidade de pricing ainda está na fase 2 (market-based) sem escalada para value-based

**Próximo nível para AFS:**
1. Ligar simulador de pricing ao RAF para fechar o loop (planejado → realizado)
2. Flag de cliente-tabelista vs cliente de projeto (atendimento diferenciado)
3. Remuneração futura atrelada a MC + aderência à tabela + custo de servir (não agora — é decisão mais tarde)

**MetalM (tese):**
- Pricing value-based desde o dia zero
- Cada serviço com preço explícito (não "pacote fechado")
- 3 propostas em toda negociação relevante
- Give/Get como padrão cultural comercial

**Ponte com outras notas:**
Pricing sem [[Custo de Servir]] é ilusão de margem.
Pricing sem [[Posicionamento Estratégico]] é reação ao mercado.
Pricing sem [[Proposta de Valor]] é commodity.

---

## Insight chave

**Preço é o único número que você pode mudar sem investir capital — e que muda o resultado imediatamente.**

Por isso é a alavanca mais sensível. E por isso a maioria das empresas a usa mal: **dá desconto** (destrói margem em minutos) em vez de **construir preço** (ganha margem em trimestres).

---

## O que a Biblioteca acrescenta

Duas sínteses de livro tocam diretamente esta nota, por ângulos opostos e complementares:

- [[Malcolm McDonald on Value Propositions — Malcolm McDonald]] — **como executar o value-based**: a proposta de valor é uma conta em dinheiro feita na economia do cliente (RP + NRG + NCR + EC), e a Tabela Vermelha é o *Reference Price* dessa fórmula. Sem a conta, a única linguagem que sobra na mesa é desconto.
- [[Rápido e devagar — Daniel Kahneman]] — **por que a tabela funciona antes de ser uma régua**: ela é uma âncora numérica, e âncora não se desarma com advertência, se desarma com ordem de apresentação. Traz também a leitura de que %Preta deve ser sempre ponderada por R$, nunca por contagem de linhas — as duas leituras diferem por ~2× e a Preta se concentra nas linhas grandes.

Juntas: McDonald explica *por que* a %Preta sobe (falta argumento em dinheiro); Kahneman explica *por que a subida não é percebida* a tempo.

---

## Conexões
- [[Custo de Servir]]
- [[Proposta de Valor]]
- [[Posicionamento Estratégico]]
- [[Cliente Ideal]]
- [[Vendas B2B]]
- [[Unit Economics]]
- [[Finanças Corporativas]]
- [[Playbook - Planejamento Comercial]]
- [[Malcolm McDonald on Value Propositions — Malcolm McDonald]] · [[Rápido e devagar — Daniel Kahneman]]

## Aplicado na AFS

Notas operacionais que usam este conceito (costura conceito↔aplicado, 01/08/2026):
- [[Sistema Operacional Comercial/00 - Visão Geral do Sistema]]
- [[Sistema Operacional Comercial/02 Precificação/00 - Visão Geral Precificação]]
- [[Sistema Operacional Comercial/02 Precificação/01 - Fórmula do Lucro]]
- [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]]
- [[Sistema Operacional Comercial/04 RAF/11 - Metodologia de Custeio da Logística]]
