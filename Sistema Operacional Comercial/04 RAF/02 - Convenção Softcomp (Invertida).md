---
tipo: armadilha-crítica
domínio: raf
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [convenção, softcomp, invertida, armadilha, crítico]
---

# 02 — Convenção Softcomp (Invertida)

## A armadilha mais cara do sistema operacional

O Softcomp usa **nomenclatura invertida** nos campos de custo do RAF. Interpretar errado leva a análises completamente erradas — como aconteceu em jan/fev/2026 antes de descobrir.

---

## A convenção

### Regra (contraintuitiva)

| Campo | Significado real |
|---|---|
| `ABCCUS_X` **sem sufixo** | **VALOR COBRADO do cliente** (embutido no preço) |
| `ABCCUS_X_COB` **com sufixo** | **CUSTO REAL pago pela empresa** |

**A intuição natural é ler "_COB" como "cobrado"**. Mas é o oposto. O sufixo `_COB` no Softcomp marca o **custo real** (provavelmente "Contábil" ou "de Origem" — origem da nomenclatura incerta).

---

## Fórmula correta para margem oculta

```
margem_oculta_X = ABCCUS_X - ABCCUS_X_COB
                = cobrado   - real
```

**Resultado positivo:** margem positiva capturada pela AFS (o que cobrou é maior do que gastou)

**Resultado negativo:** AFS está absorvendo (cobrou menos do que gastou — prejuízo invisível)

---

## Componentes com convenção aplicada

Todos os 9 componentes seguem a convenção invertida:

| Código | Campo cobrado | Campo real | Spread típico AFS |
|---|---|---|---|
| ACO | `ABCCUS_ACO` | `ABCCUS_ACO_COB` | **Zero (estrutural)** |
| FIN | `ABCCUS_FIN` | `ABCCUS_FIN_COB` | Positivo (CF% > Selic) |
| IMP | `ABCCUS_IMP` | `ABCCUS_IMP_COB` | Zero (se bem calculado) |
| COM | `ABCCUS_COM` | `ABCCUS_COM_COB` | Variável |
| CML | `ABCCUS_CML` | `ABCCUS_CML_COB` | Zero (só custo) |
| INT | `ABCCUS_INT` | `ABCCUS_INT_COB` | Positivo (~100%) |
| CER | `ABCCUS_CER` | `ABCCUS_CER_COB` | Positivo (~100%) |
| EXT | `ABCCUS_EXT` | `ABCCUS_EXT_COB` | Positivo (20-40%) |
| CTE | `ABCCUS_CTE` | `ABCCUS_CTE_COB` | Positivo (100%, AFS absorve) |

---

## Histórico da descoberta

### Jan/2026 — interpretação errada
Inicialmente interpretei **spread como custo de servir / subsídio negativo**, gerando narrativa falsa: "margem oculta = −R$2,57M — AFS está absorvendo dezenas de componentes de custo".

### Abr/2026 — correção por Gustavo
Gustavo explicou que a convenção é invertida. Números reais:

- Antes (errado): **MC econômica = 22% (subsídio de 7 p.p.)**
- Depois (correto): **MC econômica = 35,44% (uplift de 6,15 p.p.)**

**Diferença:** 13 p.p. Completamente oposto.

### Impacto se não tivesse sido descoberto
- Narrativa interna falsa de "AFS está perdendo margem"
- Decisões comerciais baseadas em premissa errada
- Possível mudança de política de pricing desnecessária

**Memória** `project_raf_servit_negativa.md` está **INVALIDADA** — remover/ignorar.

---

## Como aplicar corretamente

### Em análise pontual (Excel, planilha)
Sempre lembrar: `_COB` = real, sem sufixo = cobrado.

```excel
// Margem oculta do corte
= ABCCUS_CTE - ABCCUS_CTE_COB

// Se positivo, cobramos do cliente além do que pagamos → margem
// Se negativo, pagamos mais do que cobramos → absorção
```

### Em Motor Analítico Python
`motor/ingestao_raf.py::load_raf()` aplica a convenção correta:

```python
def load_raf(path_xlsx):
    df = pd.read_excel(path_xlsx)

    # Renomear para nomes claros
    componentes = ['ACO', 'FIN', 'IMP', 'COM', 'CML', 'INT', 'CER', 'EXT', 'CTE']

    for comp in componentes:
        # Cobrado (sem sufixo no Softcomp)
        df[f'valor_cobrado_{comp}'] = df[f'ABCCUS_{comp}']

        # Real (com sufixo _COB no Softcomp)
        df[f'custo_real_{comp}'] = df[f'ABCCUS_{comp}_COB']

        # Margem oculta
        df[f'margem_oculta_{comp}'] = df[f'valor_cobrado_{comp}'] - df[f'custo_real_{comp}']

    return df
```

### Em novos programas
**Nunca** acessar colunas `ABCCUS_*` diretamente sem traduzir. Sempre usar função de carga do motor (ou replicar a lógica).

---

## Regras operacionais

### Regra 1 — Em relatórios internos, chamar de "cobrado" e "real"
Usar nomenclatura clara em qualquer dashboard:
- "Custo cobrado (embutido no preço)"
- "Custo real (pago pela empresa)"

**Evitar** "COB" no output — é ambíguo.

### Regra 2 — Spread como margem positiva
Sempre interpretar `cobrado − real` como margem (positiva ou negativa, mas padrão positivo em AFS).

### Regra 3 — ACO é exceção
`ABCCUS_ACO_COB = ABCCUS_ACO` sempre (ou quase). Spread do aço é zero estrutural.

### Regra 4 — Desconto come margem aço primeiro
Se vendedor dá desconto bruto, ele vem **direto da MC sobre aço** (contábil), não da margem oculta.

Margem oculta fica intacta **desde que o cliente não corte serviços** (ex: "aço puro, sem TT" removeria spread EXT).

---

## Aplicação: Narrativa correta

### Narrativa falsa (pré-correção)
"Vendedor está dando desconto e a empresa está absorvendo mais que deveria em custo de servir."

### Narrativa correta (pós-correção abr/2026)
"Vendedor vê MC contábil (29,30%) ao negociar. Mas há +6,15 p.p. de margem econômica escondida em serviços/spread. Se incentivarmos por MC econômica, alinhamos comportamento com captura real de valor."

---

## Implicação para remuneração

Gustavo **não mexe na remuneração agora** (abr/2026 — fase de transição). Mas quando mexer, o design correto é:

- **Não** pagar sobre MC contábil (vendedor não controla spreads de serviço)
- **Não** pagar sobre MC econômica direta (mudaria contrato psicológico)
- **Sim** pagar sobre aderência à tabela + cobrança de serviços (proxies que movem MC econômica)

Ver [[02 Precificação/07 - Tabelas e Alçadas]] para detalhes.

---

## Implicação para simulador

Simulador precifica **a partir** do pricing com spreads incluídos (CF%, margem TT, etc.). Nesse sentido, simulador **já** reflete MC econômica nas projeções.

**Gap:** vendedor pode não perceber quanto da MC é "oculta". Dashboard do simulador poderia destacar explicitamente: "Sua MC é X%, sendo Y p.p. de margem explícita no aço e Z p.p. escondida em spreads".

---

## Conexões

- [[00 - Visão Geral RAF]]
- [[01 - Estrutura das 133 Colunas]]
- [[03 - MC Contábil vs Econômica]]
- [[04 - Margem Oculta (7 componentes)]]
- [[05 - Custo Real vs Cobrado]]
- [[01 Sistema de Dados/04 - Qualidade de Dados]]
- [[01 Sistema de Dados/06 - Motor Analítico v1]]
