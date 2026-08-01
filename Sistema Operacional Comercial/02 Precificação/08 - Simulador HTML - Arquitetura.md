---
tipo: ferramenta-arquitetura
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [simulador, html, arquitetura, padrão-canônico]
---

# 08 — Simulador HTML — Arquitetura

## Visão geral

**Arquivo:** `Analise_Precificacao_Sacchelli.html`
**Localização:** pasta raiz do projeto
**Tamanho:** ~5.300 linhas
**Tecnologia:** HTML self-contained (JS + CSS embutidos)
**Status:** Entrega 1 (multi-item rail) validada em 2026-04-15

Esta é uma das **referências canônicas** do padrão de desenvolvimento do sistema operacional. A outra é o Painel de Estoque v2.

---

## Propósito

Calcular **preço de venda sugerido** para um item (ou pacote de itens) com:
- Todos os componentes de custo
- Margem alvo
- Comparativo com tabelas A/B/C
- DRE com MC1/MC2
- Spreads de Lâmina e Tolerância (Real vs Softcomp)
- Comparativo por unidade (GRU, SCA, PIR, RIP, CXS)

---

## Capacidades (Entrega 1 validada)

### Motor de cálculo
- Suporte aos **3 modos de venda** (R$/Kg, R$/Pç, R$/m) com regras próprias de VPP, tolerância, lâmina
- Cálculo de peso de partida vs peso de orçamento (acabados)
- VPP diferenciado por acabamento (laminado 1%, forjado 5-6%)
- Processamentos (corte, TT, ensaios, certificações) com margem embutida
- Comissão customizável (vendedor 2% padrão, lobista/agente configurável)
- ICMS por item, PIS/COFINS pacote-level
- Spread financeiro (CF% vs Selic)
- Despesas por unidade (logística variável)

### DRE e KPIs
- **MC1 e MC2** em tempo real ao ajustar inputs
- Composição do resultado (barra empilhada)
- KPIs principais destacados
- Comparativo com tabelas A/B/C
- Cores semáforo (verde/amarelo/vermelho)
- Spreads de Lâmina e Tolerância (Real vs Softcomp)

### VPP e normas
- VPP informativo com hint de tolerância (EN 10060 / Metals)
- Labels "(Softcomp)" removidos dos campos, mantido apenas no título de seção

### Multi-item (Entrega 1)
- **Rail horizontal no topo** com pills de itens
- Botões: `+ Novo`, `⎘ Duplicar`, `✕ Excluir`, `↺ Resetar`
- Marker `⚠` amarelo em pills cujo item não tem Preço Negociado preenchido
- **Campos pacote-level** (compartilhados entre itens): cliente, prazo, DVA, outros, cidade, PIS, Selic, tipo cliente
- **Campos item-level:** todo o resto (peça, material, processo, ICMS, comissão, MCs, preço negociado, etc.)
- Edição de campo pacote-level propaga para todos os itens via listener

### Persistência
- **localStorage** chave `sacchelli-pacotes-v1`
- Auto-save debounced 1,5s em input/change do container
- Save imediato em switch de item, novo, duplicar, excluir
- Chave separada de `sacchelli-sim-v1` (orçamentos gravados pelo botão Gravar)

### Impressão
- Layout A4 landscape otimizado
- 2 páginas (1 para DRE, 1 para composição + KPIs)
- CSS `@media print` específico

---

## Pendências (Entregas 2 e 3)

### Entrega 2 — Modo Pacote
Ver [[12 - Modo Pacote Multi-Item]] para detalhes.

- Card consolidado com DRE do pacote (soma ponderada)
- Margem blended
- Custo de servir do pedido
- Give/Get visual (o que ganha × o que concede)
- Campo de desconto no pacote (aplica % igual a todos)
- Alerta obrigatório se faltar preço negociado

### Entrega 3 — Impressão e Versionamento
- Layout multi-item comprimido (ex: tabela compacta por item + resumo do pacote na última página)
- Versionamento v1/v2/v3 com histórico navegável

---

## Arquitetura do arquivo HTML

### Estrutura geral

```
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta/>
  <title>Análise de Precificação Sacchelli</title>
  <style>
    /* CSS embutido */
  </style>
</head>
<body>
  <header/>
  <main>
    <!-- Rail multi-item (Entrega 1) -->
    <div id="item-rail">...</div>

    <!-- Abas principais -->
    <div class="tabs">
      <button data-tab="simulador">Simulador</button>
      <button data-tab="setup">Setup</button>
      <button data-tab="salvos">Orçamentos Gravados</button>
    </div>

    <!-- Tab: Simulador -->
    <section id="tab-simulador">
      <!-- Cards de input: peça, material, processo, financeiro, cliente -->
      <!-- Card de output: DRE, KPIs, composição -->
      <!-- Card de comparativo: tabelas A/B/C -->
      <!-- Card de comparativo: por unidade -->
    </section>

    <!-- Tab: Setup -->
    <section id="tab-setup">
      <!-- Parâmetros editáveis: VPP, DVA, etc. -->
    </section>

    <!-- Tab: Orçamentos Gravados -->
    <section id="tab-salvos">
      <!-- Lista de orçamentos previamente salvos -->
    </section>
  </main>

  <script>
    /* JS embutido */
  </script>
</body>
</html>
```

### Organização do JS

```javascript
// 1. Constantes e config
const FAIXAS_BITOLA = [...];
const FAMILIAS_PADRAO = [...];
const PACOTE_LEVEL_IDS = [...]; // campos compartilhados
const SIM_SAVE_FIELDS = [...]; // campos serializáveis

// 2. Funções utilitárias
function getFamilia(aco, acabamento, bitola) { ... }
function formatarMoeda(valor) { ... }
function parseNumero(str) { ... }

// 3. Motor de cálculo
function calcularPesoPartida() { ... }
function calcularPesoOrcamento() { ... }
function calcularCustoAco() { ... }
function calcularMC1() { ... }
function calcularMC2() { ... }
function calcularPrecoFinal() { ... }

// 4. Renderização
function renderDRE() { ... }
function renderKPIs() { ... }
function renderComposicao() { ... }
function renderComparativo() { ... }
function renderRail() { ... }

// 5. Estado e persistência
const PACOTE = { itens: [...], ativo: 0, pacoteLevel: {} };
function salvarPacote() { ... }
function carregarPacote() { ... }
function snapshotItem() { ... }
function restoreItem() { ... }

// 6. Event listeners
document.addEventListener('input', debounce(salvarPacote, 1500));
// ... outros listeners

// 7. Inicialização
document.addEventListener('DOMContentLoaded', () => {
  carregarPacote();
  atualizarUI();
});
```

---

## Taxonomia embutida

O simulador carrega a **Família Canônica** direto no HTML (config embutido):

```javascript
const FAIXAS_BITOLA = [
  {sn: 1, min: 12.7, max: 101.6, label: '12.7-101.6mm'},
  {sn: 2, min: 101.61, max: 203.2, label: '101.6-203.2mm'},
  // ... até sn: 6
];

const FAMILIAS_PADRAO = [
  {aco: '1045', tipo: 'Carbono', perfil: 'Redondo', acabamento: 'Trefilado', sn: 1, descricao: '...'},
  // ... 207 combinações
];

function getFamilia(aco, acabamento, bitola) {
  const faixa = FAIXAS_BITOLA.find(f => bitola >= f.min && bitola <= f.max);
  if (!faixa) return {descricao: 'Fora de Padrão', sn: 999};
  return FAMILIAS_PADRAO.find(f => f.aco === aco && f.acabamento === acabamento && f.sn === faixa.sn) || {descricao: 'Fora de Padrão', sn: 999};
}
```

Fonte canônica: `Critérios_descrição_familia.xlsx` fornecido pelo Gustavo.

---

## Serialização (persistência)

### Campos serializáveis
`SIM_SAVE_FIELDS` — array de IDs de elementos cujo value é salvo em localStorage.

Mais extras:
- `_peca-mode` (modo R$/Kg, R$/Pç, R$/m)
- `_chk_*` (checkboxes)
- `_certs` (certificações selecionadas)
- `_phases` (fases de processo)
- `_tol_options` (opções de tolerância)
- `_tol_value` (valor de tolerância)
- `_mtlComps` (array de material comprado dinâmico)
- `_sell_unit` (Kg/Pç/m do card direito)

### Estado na memória
```javascript
PACOTE = {
  itens: [
    { nome: 'Item 1', state: {...} },
    { nome: 'Item 2', state: {...} },
    // ...
  ],
  ativo: 0,  // índice do item atualmente sendo editado
  pacoteLevel: {
    'sim-cliente-nome': 'ACME Indústria',
    'sim-prazo': 30,
    // ... outros campos compartilhados
  }
}
```

### Chaves localStorage
- `sacchelli-pacotes-v1` — pacote atual (auto-save)
- `sacchelli-sim-v1` — orçamentos gravados (save explícito)

---

## Decisões de produto (locked)

1. **Sem rateio de custo fixo do pedido.** Precificação é individual; pacote é view analítica.

2. **Desconto item-a-item.** Pode haver campo de desconto no pacote que aplica % igual a todos (Entrega 2).

3. **Sem gatilho de alerta de margem do pacote** — apenas exibir blended.

4. **Comissão variável por item** (lobista/agente podem ter % diferente). Vendedor interno sempre 2%.

5. **ICMS por item** (muda com produto). **PIS/COFINS pacote-level** (99% das vezes igual).

6. **Saída apenas interna.** Análise individual por item e consolidada do pacote.

7. **Preço Negociado obrigatório em pacote.** Sem preço ofertado por item, não existe margem real do pacote. Marker `⚠` já implementado no rail.

---

## Backup e versionamento

### Convenção de backup
Antes de qualquer mudança majoritária:
```
Analise_Precificacao_Sacchelli.bak-<razão>-YYYYMMDD-HHMMSS.html
```

Exemplo: `Analise_Precificacao_Sacchelli.bak-pre-pacote-20260415-025719.html` (backup antes da Entrega 1).

### Versionamento planejado (Entrega 3)
Histórico de cotações/pacotes versionado dentro do localStorage, com UI de navegação v1/v2/v3.

---

## Riscos residuais declarados (Entrega 1)

### Auto-save via bubbling
Listener usa event bubbling no container. Pode capturar edição em painéis vizinhos se o DOM for reorganizado. Se aparecer comportamento estranho, restringir listener ao painel específico.

### Duas abas abertas
Uma sobrescreve a outra (last-write-wins). Não crítico para uso individual (Gustavo único usuário).

---

## Quando retomar

- Verificar se **Entrega 2** ou 3 foi iniciada olhando o código HTML
- Se não houver `pacoteCalcularBlended` ou similar, **Entrega 2 ainda não começou**
- Os fixes dos 3 bugs reportados e validados já estão em produção:
  - Campos novos vindo limpos
  - Sell-unit persistindo
  - Pacote-level propagando
- Próximo passo natural: implementar DRE blended (Entrega 2)

---

## Padrão canônico replicável

Este arquivo serve como **referência** para novos desenvolvimentos. Para criar ferramenta similar:

1. Mesma estrutura HTML self-contained (style + script embutidos)
2. Mesma organização JS (const → util → motor → render → listeners → init)
3. Mesma taxonomia (Família Canônica embutida)
4. Mesma persistência (localStorage com auto-save debounced)
5. Mesma UX (cards, cores semáforo, impressão A4 landscape)

Ver [[Sistema Operacional Comercial/01 Sistema de Dados/05 - Padrões de Desenvolvimento]] para style guide completo.

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[03 - Componentes de Custo]]
- [[04 - MC1 MC2 e DRE]]
- [[05 - Modos de Venda]]
- [[06 - VPP Tolerância e Lâmina]]
- [[07 - Tabelas e Alçadas]]
- [[09 - Simulador Web App (futuro)]]
- [[12 - Modo Pacote Multi-Item]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/05 - Padrões de Desenvolvimento]]

## Arquivos
- `Analise_Precificacao_Sacchelli.html` (principal)
- `Analise_Precificacao_Sacchelli.bak-pre-pacote-20260415-025719.html` (backup pré-Entrega 1)
- `Analise_Precificacao_Sacchelli_backup_2026-04-14.html` (backup geral)
