---
tipo: overview
domínio: sistema-operacional
criado: 2026-04-17
tags: [overview, sistema, operações, afs, metalm]
---

# 00 — Visão Geral do Sistema Operacional Comercial

## Propósito deste sub-vault

Documenta o **sistema nervoso analítico** da operação comercial — lógica, normas, dados, ferramentas e cruzamentos. Não é estratégia; é a **infraestrutura de conhecimento operacional** que sustenta decisão no dia a dia e cross-ferramenta.

Objetivos:
1. **Transferir conhecimento tácito** que hoje está espalhado entre o cérebro do Gustavo, planilhas, HTMLs e ERP para algo **externalizável**
2. **Ativo pessoal transferível** — esse conhecimento vai junto se Gustavo sair da AFS (via Cenário F — ver vault estratégico)
3. **Base de onboarding** — material de ensino se houver analista, gestor comercial ou time MetalM no futuro
4. **Repositório de decisões técnicas** — não confundir com o log de decisões estratégicas (vault raiz `Logs/`)

---

## Arquitetura dos 7 domínios

```
Sistema Operacional Comercial/
├── 01 Sistema de Dados         ← base: ERP, fluxos, qualidade, ferramentas
├── 02 Precificação             ← lógica de pricing, simulador, alçadas
├── 03 Estoque                  ← família canônica, giro, ABC/XYZ, painel
├── 04 RAF                      ← receita real, custo de servir, MC econômica
├── 05 Cotações                 ← funil, motivos, tabelista vs projeto
├── 06 Pedidos                  ← do pedido ao faturamento
└── 07 Cruzamentos e Previsões  ← onde os dados se encontram
```

Cada domínio tem uma **nota "00 - Visão Geral"** com o mapa do território e links para notas específicas.

---

## Fluxo de dados conceitual

```
┌─────────────────────────────────────────────────────────────┐
│                    ERP SOFTCOMP (fonte)                      │
│   Cadastros • Cotações • Pedidos • Faturamento • Estoque    │
└────────────────────────┬────────────────────────────────────┘
                         │ (export Excel / CSV)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              ARQUIVOS BRUTOS (DetalhesRAF.xlsx,              │
│            Cot_Encerradas.xlsx, Estoque.xlsx, etc.)          │
└──┬──────────────────┬───────────────────┬───────────────────┘
   │                  │                   │
   ▼                  ▼                   ▼
┌─────────┐   ┌──────────────┐   ┌──────────────────┐
│Simulador│   │ Painel       │   │ Motor Analítico  │
│ HTML    │   │ Estoque HTML │   │ (Python + HTML)  │
└────┬────┘   └──────┬───────┘   └────────┬─────────┘
     │               │                    │
     └───────────────┴────────────────────┘
                     │
                     ▼
         ┌─────────────────────────┐
         │  Decisão comercial      │
         │  (pricing, carteira,    │
         │   alocação, previsão)   │
         └─────────────────────────┘
```

**Princípio central:** os dados brutos do Softcomp são a verdade. Ferramentas (simulador, motor, painéis) são **visões derivadas** — se há divergência, retornar ao bruto.

---

## Ferramentas em operação ou construção

| Ferramenta | Status (abr/2026) | Domínio | Nota principal |
|---|---|---|---|
| Simulador Precificação HTML | **Em uso, Entrega 1 validada** | 02 | [[08 - Simulador HTML - Arquitetura]] |
| Simulador Web App | PRD concluído, implementação em pausa | 02 | [[09 - Simulador Web App (futuro)]] |
| Painel Estoque HTML | **Em uso** | 03 | [[04 - Painel de Estoque v2]] |
| Motor Analítico v1 | Arquitetura aprovada, em codificação | 01/07 | [[06 - Motor Analítico v1]] |
| RAF análises | **Em uso** (via Excel + Python) | 04 | [[00 - Visão Geral RAF]] |
| Análise de Cotações Encerradas | **Diagnóstico feito**, monitor em construção | 05 | [[00 - Visão Geral Cotações]] |
| Dashboard Cotações Pendentes | Em desenvolvimento | 05 | (em construção) |
| Análise de Pedidos | Em desenvolvimento | 06 | [[00 - Visão Geral Pedidos]] |
| Motor Cruzamento (futuro) | Conceito | 07 | [[00 - Visão Geral Cruzamentos]] |

---

## Princípios de escrita destas notas

1. **Conceito + Aplicação concreta** — cada nota explica o conceito genérico **e** como aplica na AFS/MetalM. Sem aplicação real, vira enciclopédia morta.

2. **Números validados vs estimados** — quando um número é da memória validada, vem sem marca. Quando é premissa não-confirmada, vem marcado `{{A VALIDAR: Gustavo}}`. Nunca inventar.

3. **Referência ao arquivo-fonte** — quando a nota cita dado/fórmula/regra que está materializada num arquivo (HTML, Python, Excel), linkar o arquivo.

4. **Data de revisão** — frontmatter tem `última-revisão`. Nota sem revisão há 6+ meses deve ser checada (tecnologia e operação mudam).

5. **Sem duplicação com vault estratégico** — se a nota vira sobre "decisão" (ex: remuneração deve mudar?), linka para `Logs/` ou notas de estratégia. Aqui é **mecânica**, não **estratégia**.

---

## Conexões com o vault estratégico

Este sub-vault é **base operacional** que alimenta as decisões registradas em:

- [[Decisões C-Level]] — decisões de alto impacto
- [[Aprendizados]] — insights operacionais relevantes viram aprendizado
- [[Hipóteses de Negócio]] — hipóteses técnicas que podem virar estratégicas
- [[Custo de Servir]] — conceito estratégico que tem implementação aqui
- [[Pricing - Precificação]] — mesma lógica

---

## Como navegar

- **Primeira vez:** começar pela [[01 Sistema de Dados/00 - Arquitetura de Dados]] para entender o fluxo
- **Dúvida específica sobre pricing:** [[02 Precificação/00 - Visão Geral Precificação]]
- **Dúvida sobre número do RAF:** [[04 RAF/00 - Visão Geral RAF]]
- **Ferramenta quebrou ou não bate:** [[01 Sistema de Dados/04 - Qualidade de Dados]]

---

## Metadados do sub-vault

- **Criado:** 2026-04-17 (sessão noturna de documentação)
- **Último ciclo de revisão:** 2026-04-17
- **Próxima revisão programada:** 2026-07-17 (trimestral)
- **Autor primário:** Gustavo Sacchelli
- **Suporte:** Claude (documentação estruturada a partir de memória de conversas anteriores)
