---
tipo: taxonomia
domínio: estoque
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [família, taxonomia, padrão, cross-ferramentas]
---

# 01 — Família Canônica (Taxonomia de Produto)

## Estrutura oficial

**Família = Aço + Tipo + Perfil + Acabamento + Faixa de Bitola**

Baseado em `Critérios_descrição_familia.xlsx` (fornecido pelo Gustavo em abr/2026).

**207 combinações canônicas** mapeadas. Qualquer SKU que não se encaixa → **"Fora de Padrão"**.

---

## Aplicação cross-ferramentas

Essa taxonomia é **compartilhada** por:
- Painel de Estoque
- Análise de Cotações
- RAF / Faturamento
- Motor Analítico
- Análise de Pedidos
- Simulador de Precificação

**Regra:** ao implementar nova análise que envolva produto, **usar esta família como chave de agregação padrão**. Nunca inventar uma nova taxonomia.

---

## Componentes da família

### 1. Aço (liga)
Lista atual (extensível):
- **Carbonos:** 1020, 1045
- **Beneficiamento:** 4140, 4320, 4340, 8620, 8640, 20MnCr5
- **Aços ferramenta / cementação:** D17-18CrNiMo7-6

Ao surgir novo aço, adicionar à lista. Por enquanto ele cai em "Fora de Padrão" até ser mapeado.

### 2. Tipo
- **Carbono** — 1020, 1045
- **Beneficiamento** — 4140, 4340, 8640
- **Cementação** — 8620, 4320, 20MnCr5, 18CrNiMo7-6

**Regra:** tipo é derivado do aço. Lookup interno do sistema.

### 3. Perfil
- **Redondo** (atual único)

Futuro pode incluir Quadrado, Sextavado, Chato. Por enquanto único.

### 4. Acabamento
- **Trefilado**
- **Descascado**
- **Laminado**
- **Forjado**

Cada acabamento afeta:
- VPP (ver [[Sistema Operacional Comercial/02 Precificação/06 - VPP Tolerância e Lâmina]])
- Custo (forjado > descascado > trefilado > laminado)
- Aplicação do cliente

### 5. Faixa de Bitola
Numerada por S/N sequencial (Serial Number).

| S/N | Min (mm) | Max (mm) |
|-----|----------|----------|
| 1 | 12.7 | 101.6 |
| 2 | 101.61 | 203.2 |
| 3 | 203.21 | 230 |
| 4 | 230.01 | 355.6 |
| 5 | 355.61 | 558 |
| 6 | 558.01 | 800 |

**Fora dessas faixas:** família "Fora de Padrão" (dificilmente aparece no Estoque Padrão).

**Decisão abr/2026:** numeração S/N sequencial — abandona gaps históricos 4-8 do Excel original.

Ver [[02 - Faixas de Bitola]] para detalhes.

---

## Exemplos concretos

| Aço | Tipo | Perfil | Acabamento | Bitola | S/N | Família canônica |
|---|---|---|---|---|---|---|
| 4140 | Beneficiamento | Redondo | Laminado | 80 mm | 1 | `4140_Beneficiamento_Redondo_Laminado_1` |
| 8620 | Cementação | Redondo | Trefilado | 150 mm | 2 | `8620_Cementação_Redondo_Trefilado_2` |
| 1045 | Carbono | Redondo | Descascado | 250 mm | 3 | `1045_Carbono_Redondo_Descascado_3` |
| 4340 | Beneficiamento | Redondo | Forjado | 900 mm | — | `Fora de Padrão` |
| (inox, não mapeado) | — | — | — | 50 mm | — | `Fora de Padrão` |

---

## Implementação

### Fonte de verdade
Config **embutido direto no HTML** — não arquivo externo.

Gustavo prefere editar no HTML diretamente quando precisar mudar. Razão: simplicidade, ferramentas self-contained, facilidade de deploy (copiar arquivo).

### Estrutura no HTML

```javascript
const FAIXAS_BITOLA = [
  {sn: 1, min: 12.7,  max: 101.6, label: '12.7-101.6mm'},
  {sn: 2, min: 101.61, max: 203.2, label: '101.6-203.2mm'},
  {sn: 3, min: 203.21, max: 230,   label: '203.2-230mm'},
  {sn: 4, min: 230.01, max: 355.6, label: '230-355.6mm'},
  {sn: 5, min: 355.61, max: 558,   label: '355.6-558mm'},
  {sn: 6, min: 558.01, max: 800,   label: '558-800mm'}
];

const FAMILIAS_PADRAO = [
  // 207 combinações Aço × Tipo × Acabamento × SN
  {aco: '1020', tipo: 'Carbono', perfil: 'Redondo', acabamento: 'Laminado', sn: 1, descricao: '1020 Carbono Redondo Laminado 12.7-101.6'},
  {aco: '1020', tipo: 'Carbono', perfil: 'Redondo', acabamento: 'Laminado', sn: 2, descricao: '1020 Carbono Redondo Laminado 101.6-203.2'},
  // ... até as 207
];
```

### Função de lookup

```javascript
function getFamilia(aco, acabamento, bitola) {
  // 1. Encontrar faixa de bitola
  const faixa = FAIXAS_BITOLA.find(f => bitola >= f.min && bitola <= f.max);
  if (!faixa) {
    return {sn: 999, descricao: 'Fora de Padrão', tipo: null, label: null};
  }

  // 2. Procurar família padronizada
  const fam = FAMILIAS_PADRAO.find(f =>
    f.aco === aco &&
    f.acabamento === acabamento &&
    f.sn === faixa.sn
  );

  // 3. Se aço/acabamento não mapeado → Fora de Padrão
  if (!fam) {
    return {sn: 999, descricao: 'Fora de Padrão', tipo: null, label: faixa.label};
  }

  return {sn: fam.sn, descricao: fam.descricao, tipo: fam.tipo, label: faixa.label};
}
```

---

## Adicionando nova família

Quando surgir:
1. Novo aço importante (ex: liga específica que virou volumoso)
2. Nova faixa de bitola (ex: barras muito grandes viram item recorrente)
3. Novo acabamento (improvável mas possível)

**Processo:**
1. Atualizar `FAMILIAS_PADRAO` no HTML do Painel de Estoque
2. Atualizar `FAMILIAS_PADRAO` no HTML do Simulador
3. Atualizar `FAMILIAS_PADRAO` no Motor Analítico (Python ou config)
4. Documentar mudança nesta nota (data + aço/acabamento adicionado)
5. Comentar mudança no HTML para rastreabilidade

---

## Riscos conhecidos

### 1. Edição de faixa muda relatórios históricos retroativamente
Sem versionamento de taxonomia, análises antigas podem mudar se classifcação for alterada.

**Mitigação:** datar mudanças em comentário no HTML. Em análises históricas importantes, snapshot da taxonomia vigente na época.

### 2. Grade atual tem gap histórico (S/N 4-8 vazio antigo)
Numeração legada tinha lacunas. Decisão abr/2026 de usar S/N sequencial corrigiu. Mas análises antigas podem ter S/N 4 apontando para outra faixa.

**Mitigação:** análise histórica pré-abr/2026 deve validar taxonomia.

### 3. Material engenheirado
Customizado por cliente — não entra em FAMILIAS_PADRAO. Cai em "Fora de Padrão" com flag para revisão.

### 4. Aço fora da lista
Se cliente pede um aço (ex: inox) que não está em FAMILIAS_PADRAO, vira "Fora de Padrão". Não bloqueia a venda, mas pode distorcer análise.

**Mitigação:** monitorar frequência de "Fora de Padrão" — se um aço está aparecendo muito, vale formalizar na taxonomia.

---

## Validação da família em análises

### Checklist ao fazer análise por família
- [ ] Família usada é a canônica (207 combinações + "Fora de Padrão")?
- [ ] Ligas/acabamentos fora da lista foram corretamente enviados para "Fora de Padrão"?
- [ ] Faixa de bitola aplicada é a sequencial atual (não legada 4-8)?
- [ ] Se análise histórica: taxonomia vigente na época foi considerada?

---

## Conexões

- [[00 - Visão Geral Estoque]]
- [[02 - Faixas de Bitola]]
- [[04 - Painel de Estoque v2]]
- [[06 - Fora de Padrão]]
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/05 - Padrões de Desenvolvimento]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/06 - Motor Analítico v1]]

## Arquivo fonte
- `Critérios_descrição_familia.xlsx` (na pasta raiz do projeto)
