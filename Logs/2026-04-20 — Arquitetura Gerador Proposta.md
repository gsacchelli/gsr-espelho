---
data: 2026-04-20
tipo: decisão arquitetural
projeto: Simulador Precificação → Proposta Comercial
relacionados:
  - "[[Logs/2026-04-17 — Plano Fases 1+3 Simulador Precificação]]"
  - "[[Logs/2026-04-20 — Bloco Importação Consolidado]]"
  - "[[07_Marca/Filosofia_Design_Proposta]]"
status: aprovada — pronta para Fase 3
---

# Arquitetura — Gerador de Proposta Comercial

## Contexto

Template HTML da proposta comercial (`07_Marca/Proposta_Sacchelli_Layout.html`) finalizado em 20/04/2026 com a filosofia "Precisão Industrial" (logo + dados Sacchelli à esquerda, card meta + bloco azul do orçamento à direita, cliente strip com Cidade/UF, tabela de itens com unidade `/Pç`/`/Kg`/`/m`, badges Certificados/Extras em cor única azul Sacchelli — sem verde decorativo, paleta consolidada em azul + amarelo + cinza).

Próximo passo: conectar essa proposta ao motor de precificação para que o simulador deixe de gerar apenas a análise de margem e passe a gerar a peça comercial pronta.

## Diagnóstico — gap entre simulador e proposta

### Já no simulador (reaproveita direto)
Quantidade, unidade de venda (Pç/Kg/m), custo líquido, preço unitário, subtotal, impostos por item (ICMS/IPI/PIS/Cofins), DRE com créditos totais.

### Parcialmente no simulador (precisa expor no output)
- Descrição técnica do item (motor tem família canônica, mas a Softcomp usa descrição mais rica com desenho/MTL — precisa campo livre por item)
- Certificados / Serviços / Extras (motor tem fases ativas mas só saem como custo agregado no DRE — precisa virar lista legível)
- NCM (existe na família canônica, mas não exposto no return do motor)
- Prazo de entrega por item (não existe no output do motor)

### Gap total — não existe no simulador
- **Bloco A — Identificação:** orçamento nº, revisão, data de emissão, ref. do cliente, emitido por (vendedor)
- **Bloco B — Cliente:** razão social, cidade, **UF (crítico pro ICMS)**, Att., e-mail
- **Bloco C — Condições comerciais:** pagamento, frete, validade, uso, impostos, observação
- **Bloco D — Informações gerais de fornecimento:** texto livre default editável

## Decisão — Opção 1: layer de Proposta SOBRE o motor

Avaliadas duas opções:

**Opção 1 (escolhida) — Camada de Proposta separada do motor.**
Motor continua focado em cálculo. Nova layer "proposta" consome saída do motor + metadados (Blocos A/B/C/D) e gera HTML. Schema novo separado. Motor não incha.

**Opção 2 (descartada) — Expandir motor pra incluir dados de proposta.**
`EntradaPrecificacao` ganharia blocos `cabecalho`, `cliente`, `condicoes`. Motor viraria calculadora + empacotador.

### Razões pra Opção 1

1. **Separation of concerns.** Cálculo é matemática determinística com 458 testes verdes. Proposta é metadados + apresentação, muda com frequência, não tem regressão fiscal.
2. **Reusabilidade.** Mesma saída do motor serve hoje painel de simulação, amanhã proposta, depois pedido de venda, eventualmente API pro ERP.
3. **Ciclo de evolução diferente.** Motor muda em correção fiscal. Proposta muda em política comercial. Separar é mais limpo.

## Decisões finais — Schema da Proposta

### Bloco A — Identificação

| Campo | Tipo | Default | Editável |
|---|---|---|---|
| Orçamento nº | número | **autogerado sequencial a partir de 500.000** (persistido em localStorage) | manual — override permitido pra reproduzir número Softcomp antigo |
| Revisão | texto | "00" | manual |
| Data de emissão | data | hoje | manual (pode mudar com revisão) |
| Ref. Cliente | texto | — | manual |
| Vendedor (Por) | texto | "Gustavo S. Ramos" | manual |
| Unidade Sacchelli | seletor | vinculado ao campo "Unidade / Logística" do simulador | manual |

**Numeração — regra de incremento:**
- Contador interno em localStorage (`afs_proposta_seq`) começa em 500.000
- Cada nova proposta gerada incrementa +1
- **Override manual NÃO altera a sequência interna.** Se o usuário editar uma proposta para casar com número Softcomp antigo (ex: 547540), o contador continua na sua sequência (ex: 500.001 → 500.002), preservado independente da edição
- Botão "Resetar contador" no Setup (caso necessário em manutenção ou reinicialização)

**Revisão — incremento por confirmação:**
- A cada clique em "Salvar proposta", o simulador pergunta via modal: *"Esta alteração é uma nova revisão?"*
  - **Sim** → incrementa revisão (+1) e atualiza data de emissão pra hoje. Ex: Rev. 00 → Rev. 01
  - **Não** → mantém revisão atual, sobrescreve a versão existente (uso típico: correções menores antes de enviar)
- Histórico de revisões persistido por proposta (mesma numeração, múltiplas revisões no localStorage)
- Checkbox opcional "Não perguntar nesta sessão" no modal pra evitar fadiga em salvamentos consecutivos (decisão de UX na implementação)

### Bloco B — Cliente (digitação manual no MVP)

| Campo | Tipo | Default | Editável |
|---|---|---|---|
| Razão social | texto | — | manual |
| Cidade | texto | — | manual |
| UF | seletor (27) | — | manual — **crítico pro ICMS** |
| Att. Sr(a) | texto | — | manual |
| E-mail | texto | — | manual |

Integração Softcomp (Fase 5 futura) apenas troca a origem do dado, mantém os mesmos campos.

### Bloco C — Condições Comerciais

**Pagamento:**
- Seletor: `Antecipado` / `À vista` / `Parcelado`
- Mapeamento para o motor (alimenta CF):
  - Antecipado = **0 dias** (sem custo financeiro)
  - À vista = **1 dia** (CF mínimo)
  - Parcelado = campo texto formato "30/45/60" (N parcelas separadas por `/`)
- Cálculo da média: **aritmética simples** = (soma das parcelas) / (n de parcelas). Ex: "30/45/60" → 45 dias
- Display na proposta:
  - "Antecipado"
  - "À vista"
  - "30/45/60 ddl" (mantém formato original digitado)

**Frete:** seletor com 3 opções
- Por conta da Sacchelli
- Por conta do Cliente (retira)
- Por conta do Cliente (via transportadora)

**Validade:** default `2 dias`, editável (política AFS — proteção contra volatilidade do aço)

**Uso:** seletor `Industrialização` / `Consumo`
- **Apenas informativo na v1.** Não afeta o motor.
- Achado fiscal: para venda de aço pela Sacchelli, alíquota ICMS na NF não muda em função do uso do cliente. Eventual diferimento ICMS-SP (Art. 400-B do Decreto 45.490/00) para produtos siderúrgicos destinados a estabelecimento industrial é candidato pra v2 — exige validação com contador AFS antes de codar (ver `feedback_tributario_fonte_primaria.md`).

**Impostos:** texto fixo `"ICMS, PIS e COFINS inclusos nos preços"` na v1
- v2: adaptar para orçamento de exportação (sem esses impostos)

**Observação:** default `"Material sujeito a venda prévia"`, editável por proposta

### Bloco D — Informações Gerais de Fornecimento

Texto livre multilinha, salvo no Setup, aplicado a todas as propostas por padrão, ajustável na proposta individual.

## Estrutura dos cards na UI do simulador

3 blocos verticais antes do botão "Gerar Proposta":

1. **Card "Orçamento & Cliente"** — junta cabeçalho + cliente + unidade + vendedor
2. **Card "Condições Comerciais"** — pagamento / frete / validade / uso / impostos / observação
3. **Card "Informações Gerais de Fornecimento"** — texto livre

## Ordem de fases

| Fase | Descrição | Status | Depende de |
|---|---|---|---|
| 1 | Camada 6 (MP Repasse + Importação) | Em andamento — fechar antes | — |
| **3** | **Schema Proposta + UI no simulador** | **Pronta para arrancar — em paralelo com Fase 1** | — |
| 2 | Expor descrição/certif/NCM/prazo no output do motor | Aguardando Fase 1 | Fase 1 |
| 4 | Gerador HTML de Proposta | Aguardando Fases 2+3 | Fases 2, 3 |
| 5 (futura) | Integração Softcomp (cadastro cliente + numeração) | Backlog | Fase 4 |
| Setup | Refatorar Setup atual em 5 abas (Custos & Produção / Importação / Comercial / Certificações / Geral) | Após Fase 3 | Fase 3 |

**Por que Fase 3 antes da 2:** Fase 3 cria UI e schema independentes do motor — não conflita com Camada 6. Permite tirar produto da gaveta enquanto motor estabiliza.

**Por que refatoração Setup vem após Fase 3:** os campos novos da proposta vão entrar na aba Comercial. Refatorar de uma vez evita mexer na estrutura duas vezes.

## Tasks geradas

- #51 — Log vault (este documento) — **completed**
- #52 — Fase 3 (Schema Proposta + UI) — pendente, sem bloqueios após decisões fechadas
- #53 — Fase 2 (Expor metadados no output do motor) — bloqueada por Camada 6
- #54 — Fase 4 (Gerador HTML) — bloqueada por #52 + #53
- #55 — Coletar padrões AFS — **completed** (todas decisões fechadas neste log)
- #56 — Refatorar Setup em abas — pendente, executar após Fase 3

## Próxima sessão

**Arrancar Fase 3 — Schema Proposta + UI no simulador.**

Tudo destravado. Padrões coletados, decisões fiscais documentadas, estrutura de cards definida. Próxima sessão entra direto na implementação:

1. Criar `03_Ferramentas/js/schema_proposta.js` com tipos do Bloco A/B/C/D
2. Adicionar bloco "Proposta" no HTML do simulador com 3 cards
3. Persistência localStorage + integração com snapshot do pacote multi-item
4. Defaults AFS no Setup (validade 2 dias, vendedor "Gustavo S. Ramos", texto observação, texto informações gerais, etc.)
5. Validação de campos obrigatórios antes de habilitar botão "Gerar Proposta"
6. Testes do parser de pagamento parcelado (formato "30/45/60" → média 45)
