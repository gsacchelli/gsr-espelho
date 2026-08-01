---
tipo: ferramenta-arquitetura
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [pacote, multi-item, simulador, dre-blended]
---

# 12 — Modo Pacote Multi-Item

## Contexto

Pedidos da AFS frequentemente têm **múltiplos itens** diferentes (peças diferentes, acabamentos diferentes, modos de venda diferentes). Pricing item-a-item é correto; a **análise consolidada** do pacote é crítica para decisões comerciais.

**Estado atual (abr/2026):**
- Entrega 1 (rail multi-item) validada — permite editar múltiplos itens simultaneamente
- Entrega 2 (DRE blended do pacote) — **pendente**
- Entrega 3 (impressão comprimida + versionamento) — pendente

---

## Decisões de produto (locked)

### 1. Sem rateio de custo fixo do pedido
**Precificação é individual; pacote é view analítica.**

Cada item é precificado pelos seus próprios custos (aço, processo, margem, etc.). Não há alocação de custo fixo do pedido aos itens.

**Consequência:** DRE do pacote é **soma** dos DREs individuais, não recalculado com rateio.

### 2. Desconto item-a-item (ou % pacote)
Desconto pode ser aplicado:
- **Item a item** (cada item tem seu desconto)
- **% do pacote** (aplicado igualmente a todos os itens — útil em desconto de pedido)

**Não há:** desconto em volume de apenas 1 item afetando o rateio dos demais.

### 3. Sem gatilho de alerta de margem do pacote
Apenas **exibir** margem blended. Nenhuma ação automática do sistema.

**Consequência:** vendedor vê blended e decide se precisa ajustar algum item individualmente.

### 4. Comissão variável por item
Lobista/agente pode ter % diferente por item. Vendedor interno sempre 2%.

**Uso:** alguns itens podem ter representante diferente (parceria específica).

### 5. ICMS por item, PIS/COFINS pacote-level
- **ICMS** varia com produto — por item
- **PIS/COFINS** é fixo por regime tributário — pacote-level (compartilhado entre itens)

Campos compartilhados (pacote-level): cliente, prazo, DVA, outros, cidade, PIS/COFINS, Selic, tipo cliente.
Campos item-level: todo o resto.

### 6. Saída apenas interna
Pacote é análise interna. Impressão ao cliente pode omitir detalhes sensíveis (breakdown de custo, margem).

### 7. Preço Negociado obrigatório em pacote
**Sem preço ofertado por item, não existe margem real do pacote.**

**UI atual:** marker `⚠` no rail para itens sem Preço Negociado.

**Entrega 2:** bloqueio duro (não permite calcular blended sem todos os preços preenchidos).

---

## Estrutura do Modo Pacote (Entrega 2 planejada)

### Card consolidado
```
╔══════════════════════════════════════════╗
║  PACOTE — Cliente X — OS 12345          ║
║  Itens: 5                                ║
║  Receita total: R$ 450.000              ║
║                                          ║
║  MC1 blended:  32,5%                    ║
║  MC2 blended:  24,8%                    ║
║  Custo de servir estimado: 3,2%         ║
║  ────────                                ║
║  Margem líquida real: 21,6%              ║
║                                          ║
║  DRE blended:                            ║
║    Receita líq:  R$ 380.000             ║
║    Custo aço:    R$ 258.000             ║
║    MC1:          R$ 122.000 (32,1%)     ║
║    Variáveis:    R$  28.000             ║
║    MC2:          R$  94.000 (24,7%)     ║
║    Fixos+CS:     R$  30.400             ║
║    Resultado:    R$  63.600 (16,7%)     ║
║                                          ║
║  [ Simular desconto % no pacote ]        ║
╚══════════════════════════════════════════╝
```

### Campos específicos da Entrega 2

- **Desconto % no pacote:** aplica % igual a todos itens, mostra impacto em blended
- **Custo de servir estimado:** input (ou cálculo baseado em perfil cliente)
- **Give/Get visual:** o que cliente entrega × o que AFS entrega, alinhado a [[10 - Custo de Servir Aplicado]]
- **Comparativo "com desconto X% vs sem":** diferença de margem

### Cores e alertas (Entrega 2)
- **MC blended < 20%:** vermelho
- **MC blended 20-28%:** amarelo
- **MC blended > 28%:** verde
- Se qualquer **item individual tem MC < 10%:** alerta específico (mesmo se blended está ok)

---

## Cálculo blended (matemática)

### Receita ponderada
```
Receita_pacote = Σ Receita_item
```

### MC ponderada
```
MC_blended = Σ MC_item / Σ Receita_líq_item
           = (Σ MC$_item) / (Σ Receita_líq_item)
```

**Ou seja:** soma de MC$ dividida pela soma de receita. Não é média simples de %.

### Desconto % no pacote
```
Para cada item:
  novo_preço = preço_atual × (1 − desconto%)
  nova_MC$ = novo_preço − custo_fixo_do_item

MC_blended_novo = Σ nova_MC$ / Σ Receita_líq_nova
```

### Custo de servir do pedido
- **Estimativa inicial:** valor padrão por perfil de cliente (1-5% da receita)
- **Futuro:** cálculo baseado em histórico do cliente específico

---

## Exemplos práticos

### Exemplo 1 — Pacote "equilibrado"
- Item 1: Receita R$100k, MC 35%
- Item 2: Receita R$80k, MC 28%
- Item 3: Receita R$50k, MC 40%

**Blended:**
- Receita: R$230k
- MC$: R$35k + R$22,4k + R$20k = R$77,4k
- MC blended: 33,6%

Todos os itens estão saudáveis. Pacote verde.

### Exemplo 2 — Pacote "puxado por loss leader"
- Item 1: Receita R$100k, MC 40% (premium)
- Item 2: Receita R$80k, MC 8% (sacrificado para fechar o deal)
- Item 3: Receita R$50k, MC 35% (normal)

**Blended:**
- Receita: R$230k
- MC$: R$40k + R$6,4k + R$17,5k = R$63,9k
- MC blended: 27,8%

Blended parece ok (amarelo), mas **item 2 está em 8%** — alerta individual dispara.

**Decisão:** vendedor precisa justificar item 2. Pode ser que ganho no item 1 compense, mas precisa ser **deliberado**, não acidente.

### Exemplo 3 — Pacote com desconto 5%
Pegando Exemplo 1 (MC blended 33,6%):
- Desconto 5% em todos os itens
- Nova receita: R$230k × 0,95 = R$218,5k
- MC$ reduzida (custo fixo mantido): aprox R$55,9k (supondo custos constantes)
- MC blended: 25,6%

**Impacto:** desconto 5% derrubou MC em 8 p.p. — mais do que o desconto. Porque a parte fixa do custo (aço) não muda, só a margem encolhe.

**Decisão:** desconto 5% é caro. Precisa contrapartida equivalente (Give/Get robusto).

---

## Integração com outros conceitos

### Com [[10 - Custo de Servir Aplicado]]
Custo de servir é aplicado **no nível do pedido**, não por item. Entrega 2 do simulador deve ter campo "Custo de Servir estimado %" que afeta blended.

### Com [[07 - Tabelas e Alçadas]]
Cada item tem sua comparação com tabelas A/B/C. Se **qualquer** item ficar abaixo da Vermelha, alçada do diretor aciona — mesmo que o blended esteja ok.

### Com [[01 - Fórmula do Lucro]]
Pacote permite calcular **Margem líquida real** do pedido completo:
```
Margem_líquida_real_pedido = MC_blended − Custo_Servir_%
```

---

## Persistência multi-item

### Estado em memória (já implementado — Entrega 1)
```javascript
PACOTE = {
  itens: [
    { nome: 'Item 1', state: {...campos individuais...} },
    { nome: 'Item 2', state: {...} },
    // ...
  ],
  ativo: 0,  // índice do item em edição
  pacoteLevel: {
    'sim-cliente-nome': 'ACME',
    'sim-prazo': 30,
    'sim-dva': ...,
    'setup-dva-real': ...,
    'sim-outros': ...,
    'setup-log-real': ...,
    'sim-cidade': ...,
    'sim-pis': ...,
    'sim-selic': ...,
    'sim-cliente': ...
  }
}
```

### LocalStorage
- Chave: `sacchelli-pacotes-v1`
- Auto-save debounced 1,5s em input/change
- Save imediato em switch de item, novo, duplicar, excluir

### Diferença de `sacchelli-sim-v1`
`sacchelli-sim-v1` é para **orçamentos gravados** pelo botão "Gravar" (histórico). `sacchelli-pacotes-v1` é **trabalho em andamento** (última versão do pacote editado).

---

## Rail multi-item (UX implementada — Entrega 1)

### Elementos
- **Pills horizontais** no topo da aba Simulador
- Cada pill = 1 item (nome customizável)
- Click muda o item em edição
- Drag & drop (futuro): reordenar itens

### Botões no rail
- `+ Novo` — adiciona item em branco
- `⎘ Duplicar` — duplica item atual (rápido para pacotes com similaridade)
- `✕ Excluir` — remove item (confirmação)
- `↺ Resetar` — volta item ao estado original (se restaurável)

### Marker ⚠
Pills com item sem Preço Negociado preenchido mostram `⚠` amarelo. **Visual claro** — sem preço, não há margem real.

---

## Riscos conhecidos (Entrega 1)

### Auto-save via event bubbling
Listener captura edição em painéis vizinhos se DOM for reorganizado. Se aparecer comportamento estranho, restringir listener.

### Duas abas abertas
Uma sobrescreve a outra (last-write-wins). Não crítico para uso individual.

---

## Roadmap

### Entrega 2 — Modo Pacote Analítico
Foco: DRE blended + desconto pacote + Give/Get + custo de servir.

### Entrega 3 — Impressão e Versionamento
- Layout comprimido: tabela compacta por item + resumo na última página
- Versionamento v1/v2/v3 do mesmo pacote com histórico navegável
- Comparativo de versões (o que mudou)

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[04 - MC1 MC2 e DRE]]
- [[05 - Modos de Venda]]
- [[07 - Tabelas e Alçadas]]
- [[08 - Simulador HTML - Arquitetura]]
- [[10 - Custo de Servir Aplicado]]
