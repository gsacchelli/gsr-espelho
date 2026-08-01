---
tipo: referência-técnica
domínio: sistema-de-dados
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [qualidade-dados, erp, softcomp, mitigações]
---

# 04 — Qualidade de Dados

## Princípio

Dado bruto do Softcomp **tem problemas conhecidos**. Ignorá-los leva a análises erradas. Esta nota cataloga os problemas e as **mitigações já implementadas** ou **a implementar**.

**Regra:** antes de confiar em qualquer análise, validar que os dados passaram pelos filtros/overrides correspondentes.

---

## Problema 1 — Truncamento de cidade (20 chars)

### O que é
Softcomp trunca o campo CIDADE do cadastro de cliente em **20 caracteres**.

### Exemplos reais
| Cidade real | Como aparece no Softcomp |
|---|---|
| São José do Rio Preto | `SAO JOSE DO RIO PRET` |
| São José do Rio Pardo | `SAO JOSE DO RIO PARD` |
| Santa Bárbara d'Oeste | `SANTA BARBARA D'OEST` |
| Santa Cruz da Conceição | `SANTA CRUZ DA CONCEI` |
| Vargem Grande Paulista | `VARGEM GRANDE PAULIS` |
| Bom Jesus dos Perdões | `BOM JESUS DOS PERDOE` |
| Ferraz de Vasconcelos | `FERRAZ DE VASCONCELO` |
| São João da Boa Vista | `SAO JOAO DA BOA VIST` |
| São Bernardo do Campo | `SAO BERNARDO DO CAMP` |

### Consequências
- **Duplicidade de município:** São Bernardo do Campo aparece como `S.B. CAMPO` em alguns cadastros e `SAO BERNARDO DO CAMP` em outros
- **Análises regionais erradas:** mesmo município vira duas linhas em Pareto
- **Agrupamento por cidade/Região Administrativa** quebra sem override

### Adicionais conhecidos
- `CAPITAL` como apelido informal para São Paulo
- Distritos cadastrados como município (`SANTA EUDOXIA` é distrito de São Carlos; `TUPI` é distrito de Piracicaba)

### Mitigação implementada
Arquivo `config/cidades_overrides.yaml` no Motor Analítico consolida nomes canônicos.

### Mitigação estrutural (ideal)
Corrigir cadastros no Softcomp + aumentar limite do campo. Envolve ação do time administrativo AFS.

### Padrão recomendado
**Toda análise por cidade/região SP** deve aplicar o override **antes** de agrupar. Se ferramenta nova não faz isso, está errada.

---

## Problema 2 — "Orçamento prévio" como caixa-preta

### O que é
O motivo de encerramento "Cotação somente para orçamento prévio" **engloba dois perfis completamente diferentes**:

| Perfil A — Tabelista | Perfil B — Projeto real |
|---|---|
| Cliente usa AFS como referência de preço | Cliente em fase de CAPEX (planta nova, retrofit) |
| Compra de outro fornecedor | Vai decidir em 6-18 meses |
| Nunca vira pedido | Pode virar pedido grande |
| Atendimento industrializado faz sentido | Atendimento intensivo é crítico |

### Consequência
Tratamentos opostos confundidos no mesmo balde. ~53% do pipeline encerrado vira "orçamento prévio" — grande parte é pipeline de projeto que a AFS perdeu visibilidade.

### Mitigação estrutural proposta
Novo status "Em Projeto" no Softcomp com:
- Não-encerramento automático
- Follow-up forçado 30/60/90 dias
- Só encerrável como Ganhou / Perdeu / Projeto Cancelado (nunca como orçamento prévio)
- Métricas: valor em carteira, idade média, projetos tocados vs esquecidos

### Padrão recomendado (enquanto estrutural não existe)
Análise nunca deve tratar "orçamento prévio" como bloco uniforme. Sempre segmentar:
1. Por valor cotado (grande = provável projeto)
2. Por setor do cliente (industrial pesado = provável projeto)
3. Por nome conhecido (ANDRITZ, PROK, SUPERIOR = projeto)

Ver detalhes em [[05 Cotações/03 - Orçamento Prévio vs Projeto Real]].

---

## Problema 3 — Canal INT/PJ/REP é fiscal, não comercial

### O que é
O campo "canal" (INT = interno CLT, PJ = pessoa jurídica, REP = representante) é **classificação fiscal/tributária**, não operacional.

Hoje AFS tem:
- Quase todos vendedores são **PJ** (por razão tributária, não comportamental)
- **Apenas 2 juniors INT** em Guarulhos
- Alguns REP legítimos (representantes externos), minoritários

### Consequência
**Comparar conversão ou performance por canal INT vs PJ gera conclusão errada.** Quase todos são PJ — comparar PJ vs INT = comparar quase toda empresa vs 2 juniors.

### Mitigação
Análises de vendedor **nunca** segmentam por canal. Usar:
- Região (CXS, SP, PIR, SCA, RIP)
- Gerente
- Perfil (sênior vs júnior vs especialista)
- Tempo de casa

### Padrão recomendado
Ferramentas não devem ter visualização "por canal" sem contexto explicativo. Se aparecer, rotular como "fiscal/tributário" para evitar erro interpretativo.

---

## Problema 4 — Convenção de custo invertida no RAF (ABCCUS_X vs ABCCUS_X_COB)

### O que é
No export RAF do Softcomp:
- `ABCCUS_X` (sem sufixo) = **VALOR COBRADO do cliente**
- `ABCCUS_X_COB` = **CUSTO REAL pago pela empresa**

Nomenclatura é **invertida** em relação à intuição natural.

### Consequência
Se interpretar como intuitivo: spread parece "custo de servir negativo". Se interpretar corretamente: spread é **margem oculta positiva**.

**Impacto real:** em jan/fev/2026, interpretação errada gerou narrativa falsa de "margem oculta = −R$2,57M". Gustavo corrigiu em abr/2026 → números reais:
- MC contábil: 29,30%
- MC econômica: **35,44%** (+6,15 pp)

### Mitigação implementada
- Motor Analítico: `ingestao_raf.py::load_raf()` calcula `margem_oculta_X = ABCCUS_X − ABCCUS_X_COB` com sinal correto
- Dashboard RAF: seção "Margem Econômica Escondida" separada
- Memória `project_raf_convencao_softcomp.md` atualizada

### Padrão recomendado
Em qualquer análise RAF, **primeiro** passar pelas funções de carga do motor (que aplicam a inversão correta), **nunca** ler direto dos campos brutos sem tradução. Ver [[04 RAF/02 - Convenção Softcomp (Invertida)]].

---

## Problema 5 — Múltiplas linhas do mesmo item (consolidação por OS)

### O que é
No RAF, um mesmo item (OS + ITE) pode ter **múltiplas linhas** por causa de:
- Liberações parciais
- Revisões de faturamento
- Corrections fiscais

Custos (ABCCUS_X) podem estar **concentrados em uma linha só**, deixando outras com zero.

### Consequência
Análise de margem por item sem consolidação → resultado distorcido. Margem de 80% "aparente" numa linha + margem 5% na outra linha do mesmo item.

### Mitigação
Sempre consolidar linhas **por OS + ITE** antes de calcular métricas unitárias:
- Somar valores (receita, custo, MC)
- Médias ponderadas por peso/quantidade

### Padrão recomendado
Funções de análise do RAF operam **sempre** sobre dataframe consolidado, não sobre linhas brutas. Implementado no Motor Analítico. Ver [[04 RAF/08 - Consolidação por OS]].

---

## Problema 6 — Família do produto: 3 campos, interpretação cuidadosa

### O que é
Existem 3 campos relacionados a família no RAF:
- `ABCFAACOD` — família do produto **faturado**
- `ABCOII_FAA` — família da **OS**
- `ABCMAT_FAA` — família do **material de partida**

Podem divergir porque material de partida (bruto) passa por transformação (corte, usinagem, tratamento).

### Consequência
Agregar por campo errado gera análise distorcida:
- `ABCMAT_FAA` = visão do fornecedor de insumo
- `ABCFAACOD` = visão de o que o cliente recebeu
- `ABCOII_FAA` = visão da OS como registro

### Padrão recomendado
- Analise **margem por produto vendido**: use `ABCFAACOD`
- Analise **utilização de estoque**: use `ABCMAT_FAA`
- Rastreamento de processo: compare os três para detectar transformações

---

## Problema 7 — Tabela de preço sem versionamento histórico

### O que é
Quando tabelas A/B/C são alteradas no Softcomp, versão antiga **não fica preservada**. Análise retroativa usa a tabela vigente, não a que estava em vigor na data da cotação/pedido.

### Consequência
Análise de aderência à tabela ou spread real perde acurácia com o tempo.

### Mitigação manual
Salvar snapshot do `tabela_preco.xlsx` a cada mudança (convenção `tabela_preco_YYYYMMDD.xlsx`).

### Mitigação estrutural (ideal)
Tabela de preço em banco próprio com versionamento (simulador web app futuro).

---

## Problema 8 — "Clientes em Desenvolvimento" ≠ prospects

### O que é
No Softcomp existe uma flag/categoria "Clientes em Desenvolvimento". **Não são prospects ativos de vendedor.** São:
- Contas **fechadas entre diretorias** (Gustavo × stakeholders do cliente)
- Vendedor de campo não entra
- ~R$3,3M/ano
- ~8 clientes

### Consequência
Se incluir "Clientes em Desenvolvimento" em ranking de vendedor, vendedor que não contribuiu aparece como top performer. Erro comum em análise de equipe.

### Padrão recomendado
Análises de vendedor **excluem explicitamente** essa carteira. Se ferramenta nova agrupa por vendedor, checar filtro.

---

## Problema 9 — "Cotação somente por orçamento prévio" como filtro entrada

### Interpretação errada (original, abr/2026)
"Motor mostra que vendedor está aceitando lead ruim e desperdiçando tempo."

### Interpretação correta (confirmada com Gustavo)
Toda cotação é gerada pelo vendedor. Classificação "orçamento prévio" é **post-mortem**, não flag de entrada.

Significado real:
- Vendedor **sabia** que cliente ia cotar só para comparar
- E ainda assim cotou com **esforço normal**
- É problema de **disciplina de priorização**, não de filtragem

### Mitigação proposta
Flag "cliente-tabelista" automática:
- >70% das cotações encerradas como orçamento prévio
- <10% de conversão nos últimos 12 meses

Esses clientes recebem **atendimento industrializado**: tabela automática, zero análise de engenharia, zero customização.

---

## Como validar qualidade antes de análise

Checklist rápido (5 min antes de usar dado novo):

```
[ ] Arquivo bruto tem data no nome?
[ ] Data do arquivo bate com período solicitado?
[ ] Número de linhas faz sentido (RAF ~5k/mês)?
[ ] Cidades já passaram pelo override?
[ ] Consolidação por OS feita (se RAF)?
[ ] Campo ABCCUS_X interpretado como cobrado (invertido)?
[ ] Canal INT/PJ/REP não sendo usado como dimensão comercial?
[ ] Clientes em Desenvolvimento excluídos (se análise de vendedor)?
[ ] Versão da tabela de preço bate com data da análise?
[ ] Família sendo agregada pelo campo correto (FAACOD vs MAT_FAA)?
```

Se qualquer item responder "não", **pare e corrija antes de concluir algo**.

---

## Conexões

- [[00 - Arquitetura de Dados]]
- [[01 - ERP Softcomp - Detalhes]]
- [[05 - Padrões de Desenvolvimento]]
- [[04 RAF/02 - Convenção Softcomp (Invertida)]]
- [[04 RAF/08 - Consolidação por OS]]
- [[05 Cotações/03 - Orçamento Prévio vs Projeto Real]]
