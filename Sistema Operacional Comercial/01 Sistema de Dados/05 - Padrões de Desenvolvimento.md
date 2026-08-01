---
tipo: padrão-desenvolvimento
domínio: sistema-de-dados
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [padrão, desenvolvimento, style-guide, html, python]
---

# 05 — Padrões de Desenvolvimento

## Propósito

Este documento é o **style guide canônico** para desenvolvimento de novos programas, painéis, análises e ferramentas no ecossistema analítico comercial AFS/MetalM.

**Referências base:**
- **Painel de Estoque v2** (`Painel_Estoque_Sacchelli_v2.html`) — padrão canônico atual
- **Simulador de Precificação** (`Analise_Precificacao_Sacchelli.html`) — referência atualizada

Quando houver divergência entre programas, **esses dois são os padrões**. Outros devem se alinhar a eles com o tempo.

---

## Princípios fundamentais

### 1. Self-contained quando possível
Saída preferencial: **HTML único**, sem dependências externas (CDN, fontes remotas). Razão: funciona offline, não quebra com mudanças de CDN, distribuição simples (copiar arquivo).

### 2. Dados não saem da máquina
**Sem SaaS, sem cloud, sem APIs externas** que transmitam dados comerciais. Tudo roda local (navegador, Python na máquina).

### 3. Fonte de verdade é o Softcomp
Nenhuma ferramenta mantém sua própria cópia de verdade. Todas consomem exports atualizados. Se há divergência, reprocessar.

### 4. Taxonomia unificada
Todas usam a mesma **Família Canônica** (ver [[03 Estoque/01 - Família Canônica]]). Nenhuma inventa a sua.

### 5. Graceful degradation
Dados faltando não quebram a ferramenta. Linha sem cidade? Agrupa em "Não informado". SKU sem família? Vai pra "Fora de Padrão" com flag.

---

## Stack tecnológica preferencial

### Para ferramentas interativas leves (pricing, painel)
- **HTML + JS puro** (sem framework pesado)
- **Tailwind CSS** — somente **utility classes inline**, sem processo de build
- **localStorage** para persistência de estado de usuário
- **Plotly.js ou Chart.js** se precisar gráfico (via CDN aceitável só em dev; em produção, incluir no HTML)

### Para processamento pesado (análise RAF, cruzamentos, motor)
- **Python 3.10+** local
- **pandas + numpy** para data
- **openpyxl** para Excel read/write
- **PyYAML** para config
- **Jinja2** para gerar HTML a partir de Python
- **Sem banco** (SQLite aceitável se estritamente necessário)

### Para versão multi-usuário futura (Simulador Web App)
- **Node.js 20 + Express** (backend)
- **React 18 + Vite + Tailwind** (frontend)
- **SQLite (better-sqlite3)** (persistência)
- **JWT + bcrypt** (auth)
- Deploy: VM AFS interna + Nginx + HTTPS

---

## Convenções de código

### HTML
```html
<!-- Cabeçalho padrão -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nome Ferramenta — AFS</title>
  <style>
    /* CSS embutido */
  </style>
</head>
<body>
  <!-- Conteúdo -->
  <script>
    // JS embutido
  </script>
</body>
</html>
```

### Nomenclatura de arquivos
Ver [[02 - Arquivos Brutos e Convenções]]:
- Ferramentas: `NomeFerramenta.html` (sem data)
- Versões majoritárias: sufixo `_v2`, `_v3` (quando muda arquitetura)
- Backups: `NomeFerramenta.bak-<razão>-YYYYMMDD-HHMMSS.html`
- Saídas datadas: `Relatorio_YYYY-MM-DD.html`

### Nomenclatura de variáveis (JavaScript)
- Constantes em SNAKE_CASE_MAIÚSCULAS: `FAIXAS_BITOLA`, `TABELA_CORES`
- Variáveis camelCase: `pesoMPTon`, `custoTonKg`
- Funções camelCase: `getFamilia()`, `calcularMC()`
- Prefixos de DOM id: `sim-` para simulador, `estq-` para estoque, `raf-` para RAF

### Nomenclatura Python
- PEP 8 padrão
- Módulos snake_case: `ingestao_raf.py`, `analitica_raf.py`
- Funções descritivas: `load_raf()`, `consolidar_por_os()`, `calc_margem_oculta()`
- Config centralizada em `config/` (YAML ou Python)

---

## Padrão de arquitetura HTML self-contained

### Estrutura do arquivo (baseado em Estoque v2 + Simulador)

```
1. Header HTML + meta tags
2. Bloco <style> com CSS
3. Bloco de dados (JSON ou JS const) com critérios embutidos
4. Layout HTML (divs, tabelas, placeholders)
5. Bloco <script> dividido em:
   a. Constantes e config
   b. Funções utilitárias
   c. Funções de cálculo (motor)
   d. Funções de renderização
   e. Event listeners
   f. Inicialização
```

### Princípios específicos
- **Config embutida:** não depender de arquivo externo para faixas de bitola, famílias, etc. Edita no HTML mesmo quando precisar mudar (ver [[03 Estoque/01 - Família Canônica]]).
- **Data/hora no título:** quando HTML é derivado de dados datados, incluir data no cabeçalho visível.
- **Impressão otimizada:** CSS `@media print` com layout A4 landscape, 1-2 páginas.
- **Auto-save debounced:** se ferramenta tem estado de usuário, salvar em localStorage com debounce 1,5s em input/change, save imediato em ações críticas.

---

## 🎨 Padrão visual canônico (identidade AFS)

**Todo painel, dashboard ou ferramenta HTML criado para AFS DEVE seguir esta identidade.**

### Referência canônica
**Arquivo-modelo:** `03_Ferramentas/Analise_Precificacao_Sacchelli.html` (Simulador de Precificação)

Cores, tipografia, hierarquia visual, layout de cards, cores semáforo — tudo replicar a partir deste arquivo.

### Logo obrigatório
**Arquivo:** `07_Marca/SACCHELLI-HORIZONTAL.png` (ou variante conforme fundo):
- `SACCHELLI-HORIZONTAL.png` — principal (horizontal, padrão)
- `SACCHELLI-HORIZONTAL-RESUMIDA.png` — versão resumida
- `SACCHELLI-HORIZONTAL-RESUMIDA-RGB.png` — colorida
- `SACCHELLI-HORIZONTAL-NEGATIVA.png` — fundo escuro

**Posicionamento:** cabeçalho superior esquerdo do painel.

**Inserção no HTML:** logo como base64 inline ou referência relativa a `07_Marca/`. Nunca depender de logo externo (CDN, URL).

### Paleta (extrair do Simulador)
- Verde (positivo/saudável) — usado em indicadores "ok"
- Amarelo (atenção) — usado em alertas médios
- Vermelho (crítico/abaixo do piso) — usado em alertas fortes
- Azul (informativo) — usado em destaques neutros
- Cinza (secundário) — usado em labels e metadados

Valores exatos de hex/RGB: extrair do CSS do simulador e documentar em `templates/_tokens.css` quando criar (v2 da arquitetura).

### Estrutura de cabeçalho padrão
```html
<header>
  <img src="logo_sacchelli.png" alt="Sacchelli">
  <h1>[Nome da Ferramenta] — AFS</h1>
  <p class="meta">Atualizado em: [data] | Versão: [vX]</p>
</header>
```

### Layout geral
- Grid CSS de 2-3 colunas no desktop (responsivo)
- Hero metric bem visível no topo
- Cards com borda leve, sombra sutil, padding generoso
- Separação visual por seções com divisores
- Impressão otimizada (A4 landscape)

### Checklist visual para nova ferramenta
```
[ ] Logo Sacchelli no cabeçalho
[ ] Cores seguem paleta do Simulador
[ ] Hierarquia visual clara (H1 > H2 > H3)
[ ] Hero metric destacado
[ ] Cores semáforo aplicadas corretamente
[ ] Layout A4 landscape no print
[ ] Data de atualização visível
[ ] Título segue padrão: "[Nome] — AFS"
```

**Divergir do padrão visual é aceitável apenas em ferramentas experimentais (protótipos).** Ferramentas que vão pra produção seguem o padrão.

---

## Padrão de arquitetura Python

### Estrutura de projeto
```
MotorAnalitico/
├── motor/
│   ├── __init__.py
│   ├── ingestao_raf.py        ← load e transformação de RAF
│   ├── ingestao_cotacoes.py
│   ├── ingestao_estoque.py
│   ├── analitica_raf.py       ← análises derivadas
│   ├── consolidacao.py
│   ├── familia.py             ← lógica de família canônica
│   └── render.py              ← geração de HTML output
├── config/
│   ├── cidades_overrides.yaml
│   ├── familias.yaml (se não embutido no HTML)
│   └── grupos_concorrentes.yaml
├── input/                     ← arquivos brutos do Softcomp
├── output/                    ← HTMLs/Excel gerados
├── templates/                 ← Jinja2
└── main.py                    ← entrada
```

### Princípios
- **Separação clara:** ingestão ≠ análise ≠ renderização
- **Funções puras:** receber dataframe, retornar dataframe (sem efeito colateral)
- **Config externa:** regras mutáveis (cidades, famílias, grupos) em YAML, não hardcoded
- **Log de qual bruto foi usado:** todo output inclui metadado do arquivo de origem

---

## Padrão de taxonomia e dados compartilhados

### Família canônica
**Obrigatório** em qualquer ferramenta que agregue por produto.

Estrutura:
```javascript
const FAIXAS_BITOLA = [
  {sn: 1, min: 12.7, max: 101.6, label: '12.7-101.6mm'},
  {sn: 2, min: 101.61, max: 203.2, label: '101.6-203.2mm'},
  // ...
];

const FAMILIAS_PADRAO = [
  {aco: '1045', tipo: 'Carbono', perfil: 'Redondo', acabamento: 'Trefilado', sn: 1, descricao: '...'},
  // ...
];

function getFamilia(aco, acabamento, bitola) {
  // retorna {sn, descricao, tipo, label} ou "Fora de Padrão"
}
```

Fonte canônica: `Critérios_descrição_familia.xlsx` fornecido pelo Gustavo. Config **embutido direto no HTML** (não externo).

### Cidades SP
Usar sempre override (consolidação de truncamentos e apelidos).
Arquivo canônico: `config/cidades_sp.xlsx` + `cidades_overrides.yaml`.

### Grupos de concorrentes
Consolidação conhecida:
- Trefita + Torres = mesmo grupo (Torres = forjado)
- GGD = Gerdau usina (bucket separado)

---

## Padrão de UX para painéis e dashboards

### Layout geral
- **Hero metric no topo** — número mais importante visível de cara
- **Filtros no topo** — período, unidade, vendedor
- **Blocos em grid** — concentração, fluxo, tendência
- **Drill-down disponível** — clicar em família abre SKUs

### Cores padrão (baseado em Estoque v2)
- Verde: positivo, saudável, verde
- Amarelo: atenção, intermediário
- Vermelho: crítico, negativo
- Azul: informativo neutro
- Cinza: secundário / disabled

### Interação
- Hover mostra detalhe
- Click abre drill-down (modal ou painel lateral)
- Atalhos de teclado: ESC fecha modal
- Print sempre possível (Ctrl+P)

### Performance
- Renderização inicial < 2s
- Interação (filtro, click) < 500ms
- Se processamento mais longo, mostrar spinner + tempo estimado

---

## Padrão de segurança e confidencialidade

### Dados comerciais AFS
- **Nunca** em serviços externos (Google Sheets public, Claude web, etc.)
- **Nunca** em repos Git públicos
- Compartilhar agregados e rankings; dados individuais de cliente requerem cuidado

### Arquivos com dados
- Pasta local apenas
- iCloud aceitável para backup (criptografia no disco recomendada — FileVault)
- Não versionar dados brutos em Git (só código)

### API keys / credenciais
- Nunca em código-fonte
- Arquivo `.env` local (gitignored)
- Se precisar commit (ex: config do simulador web), variável de ambiente

---

## Padrão de teste e validação

### Ao criar ferramenta nova
1. **Validar contra Softcomp** em 5-10 casos conhecidos — número bate?
2. **Validar contra ferramenta existente** em overlap (se há) — consistente?
3. **Casos extremos:** SKU sem família, cliente sem cidade, OS com 10 linhas
4. **Print:** sai em A4 landscape legível?
5. **Diferentes períodos:** 1 mês, 1 ano, sem dados — todos funcionam?

### Ao alterar ferramenta existente
1. **Backup antes** (`Nome.bak-motivo-YYYYMMDD-HHMMSS.html`)
2. **Teste de regressão:** funcionalidade antiga continua funcionando?
3. **Changelog em comentário** no topo do arquivo ou em `CHANGELOG.md`

---

## Padrão de documentação

### Código
- Comentários em partes não-óbvias (lógica comercial, fórmulas de pricing)
- Docstrings em funções Python
- README.md por projeto com: propósito, como rodar, input/output

### Vault (este sub-vault)
- Toda ferramenta nova ganha nota neste sub-vault
- Na nota: arquivo, status, capacidades, dependências, pendências
- Mudança de arquitetura: atualizar nota + data de revisão

---

## Checklist para nova ferramenta

```
[ ] Propósito claro (uma frase)
[ ] Stack alinhado com padrão (HTML self-contained ou Python local)
[ ] Taxonomia Família Canônica incluída
[ ] Cidades override aplicado (se análise regional)
[ ] Convenção Softcomp ABCCUS tratada (se usa RAF)
[ ] Consolidação por OS (se usa RAF)
[ ] Input aceita arquivo bruto nomeado YYYYMMDD
[ ] Output inclui metadados (data do bruto, versão)
[ ] CSS @media print funcional
[ ] Nota criada neste vault referenciando a ferramenta
[ ] Backup da versão antes de mudanças majoritárias
```

---

## Divergências conhecidas entre programas atuais

> Levantamento para ação futura — trazer programas antigos ao padrão.

| Programa | Divergência | Ação |
|---|---|---|
| Painel Comercial AFS v1-v4 | Múltiplas versões, taxonomia inconsistente entre versões | Consolidar em v5 usando Estoque v2 como base |
| Diagnostico_Precificacao_Sacchelli | Foi análise pontual; formato ad-hoc | Reescrever se análise for recorrente; caso contrário, manter como histórico |
| Campanha_60anos_Dashboard | Histórico, padrão antigo | Arquivar em `05_Arquivo/` |
| Analise_Financeira_Acovisa | PPTX, fora do padrão HTML | Manter como PPTX (é apresentação, não ferramenta) |

---

## Conexões

- [[00 - Arquitetura de Dados]]
- [[02 - Arquivos Brutos e Convenções]]
- [[04 - Qualidade de Dados]]
- [[03 Estoque/01 - Família Canônica]]
- [[03 Estoque/04 - Painel de Estoque v2]] — referência canônica
- [[02 Precificação/08 - Simulador HTML - Arquitetura]] — referência canônica
