---
tipo: processo-operacional
domínio: precificação
criado: 2026-04-17
última-revisão: 2026-04-17
tags: [tabelas, alçada, verde-amarela-vermelha, aprovação, remuneração]
---

# 07 — Tabelas e Alçadas

## Sistema de 3 tabelas (Verde / Amarela / Vermelha)

A AFS opera com **3 níveis de preço** por produto, materializados em tabelas:

| Tabela | Cor | Significado | Alçada |
|---|---|---|---|
| **A** | Verde | Preço cheio (cliente premium) | Vendedor livre |
| **B** | Amarela | Preço intermediário | Vendedor livre |
| **C** | Vermelha | Piso padrão de venda | Vendedor livre até este piso |
| (abaixo de C) | — | Exceção | **Apenas Diretor Comercial** |

### Vigência
Tabelas são atualizadas **periodicamente** (mensal ou quando custo sobe/cai significativamente). Tabela vigente no momento da cotação é a que vale.

### Campos RAF
- `ABCPRE_MIN_A` = piso Tab Verde (R$/kg)
- `ABCPRE_MIN_B` = piso Tab Amarela (R$/kg)
- `ABCPRE_MIN_C` = piso Tab Vermelha (R$/kg)

---

## Alçada de preço

### Funcionamento prático
1. Vendedor recebe cliente, gera cotação no Softcomp
2. Softcomp mostra as 3 tabelas para aquele produto
3. Vendedor negocia entre Verde e Vermelha **livremente**
4. Se negociar abaixo da Vermelha → tem que solicitar aprovação do Diretor (Gustavo)

### Zona cega (crítica)
**Entre Verde e Vermelha, vendedor age sozinho.** O Diretor só vê o que **desce abaixo** da Vermelha.

**Consequência:** diretor tem visibilidade **binária** — vê só o "abaixo do vermelho". Não vê a **frequência de uso** das faixas intermediárias.

**É aqui que provavelmente mora o maior vazamento de margem.** Vendedor pode estar vendendo constantemente perto da Vermelha sem o diretor perceber.

### Aprovação abaixo da Vermelha
Hoje: conversa direta, sem justificativa formalizada.

**Alavanca sem mexer em remuneração (proposta não implementada):**
- Campo obrigatório de justificativa para desconto abaixo da Vermelha
- Relatório de frequência de uso das 3 tabelas por vendedor (ilumina a zona cega)
- Conversa cirúrgica com 2-3 vendedores de pior combinação volume alto × MC real baixa × prazo longo

---

## Remuneração dos vendedores (abr/2026)

### Modelo atual
| Tipo | Remuneração |
|---|---|
| Vendedores CLT (INT) | **Fixo + 2% sobre faturamento s/IPI** |
| Vendedores PJ | **2% sobre faturamento s/IPI** (sem fixo) |

**Pontos-chave:**
- Não atrelado a MC, prazo, custo de servir ou qualquer métrica de qualidade
- **Atende volume, não margem**
- Incentivo atual: dar desconto para fechar mais rápido, porque comissão é sobre receita, não margem

### Decisão atual (abr/2026)
Gustavo **decidiu não alterar agora**. Razão: em fase de transição de carreira, mexer em remuneração queima capital político e pode disparar saídas de vendedores — sem ganho imediato proporcional.

### Design correto (quando for hora de mexer)

**NÃO pagar sobre MC diretamente.** Pagar sobre o que o vendedor **100% controla** e que move a MC:

#### 1. Preservação de preço vs tabela
% de pedidos em **verde/amarela/vermelha** (não abaixo).
- Bom vendedor: alto % verde/amarela
- Mal vendedor: alto % vermelha ou abaixo
- **Incentiva manter pricing na faixa saudável**

#### 2. Aderência ao juro Softcomp
Em vendas a prazo, sistema calcula juro. Se vendedor "devolver" o juro via desconto extra, perde.
- **Incentiva não queimar o spread financeiro**

#### 3. Custo de servir discricionário
Urgência, retrabalho, corte fora de padrão: cobrar ou absorver?
- Métrica: % de "cortesias" por vendedor
- **Incentiva cobrar serviços extras**

#### Propriedades dessas 3 métricas
- Todas **insensíveis** a mexidas no custo do aço ou logística (Wagner pode mudar, não afeta vendedor)
- Sempre sob controle do vendedor
- Quebram o contrato psicológico de "dar volume → ganhar comissão"

### Estrutura recomendada (quando for a hora)
- **Manter 2% atual** (contrato psicológico preservado)
- **Adicionar bônus trimestral/semestral** escalonado sobre as 3 métricas
- Bônus representa 20-30% do variável total
- **Só positivo, nunca negativo** (zero perda percebida)

---

## Canal INT / PJ / REP (clarificação)

**Atenção:** canal é **fiscal / tributário**, não comercial. Ver [[Sistema Operacional Comercial/01 Sistema de Dados/04 - Qualidade de Dados]].

### Hoje (abr/2026)
- Quase todos os vendedores são **PJ** (por razão tributária)
- **Apenas 2 juniors** são INT em Guarulhos
- Poucos REP legítimos (representantes externos)

### Consequência
**Comparar conversão ou performance por canal INT vs PJ é erro analítico comum.** A distinção não é comportamental — é fiscal.

Em análises, segmentar por:
- Região (CXS, SP, PIR, SCA, RIP)
- Gerente
- Perfil (sênior, júnior, especialista)
- Tempo de casa

---

## Clientes em Desenvolvimento (carteira especial)

### O que é
Categoria do Softcomp para **contas fechadas entre diretorias** — Gustavo + stakeholders do cliente.

### Características
- Vendedor de campo **não entra**
- ~R$3,3M/ano
- ~8 clientes

### Não confundir com "prospects"
Não são leads em qualificação. São contas operantes fora da carteira de vendedor comum.

### Implicação para análise
- Ranking de vendedor **sempre exclui** essa carteira
- Ferramenta que agrupa por vendedor deve filtrar esses ~8 clientes
- Se não filtrar, vendedor responsável formal "aparece como top" sem ter operado

---

## CXS — handicap logístico

A unidade de Caxias do Sul tem handicap estrutural:

- **3 pernas logísticas** (SFS → SP CD → CXS → cliente)
- **5,65% de despesa logística** (vs 1,54% em GRU)
- Concorrentes têm 1-2 pernas

**Implicação para pricing:** preço final em CXS precisa **absorver** o handicap. Ou:
- Cliente aceita preço maior (valorizando serviço)
- Cliente não aceita e AFS perde
- Descontar agressivamente (duplo handicap: sacrifica margem + carrega custo estrutural)

**Implicação para análise de performance:**
- Sempre **descontar handicap** antes de avaliar gestão CXS
- Fabíola (gerente CXS) não deve ser comparada com gerentes SP sem esse ajuste
- Em perdas "por preço" em CXS, verificar estrutura do concorrente antes de atribuir a preço

Ver `project_afs_estrutura_logistica` (memória).

---

## Problema comercial em CXS (a retomar)

Além do handicap logístico, CXS tem **problema comercial identificado**:
- Vendedores "sem técnica"
- Combinação perigosa: gargalo estrutural + falta de sofisticação comercial

Se combinado com análise da defesa Trefita (14 clientes perdidos em CXS), parte dessa perda **pode ser técnica, não preço**. Vendedor sem técnica negocia só em preço.

Ação futura (quando houver tempo): treinar ou substituir time comercial CXS. Não resolvido enquanto Gustavo está em transição de carreira.

---

## Operação ideal de alçada (proposta)

### Fluxo futuro
```
Vendedor cota → Sistema mostra 3 tabelas
            → Vendedor escolhe preço
            → Sistema classifica em Verde/Amarela/Vermelha/Abaixo
            → Se Verde/Amarela/Vermelha: cotação segue
            → Se Abaixo: obrigatório justificar
            → Diretor aprova/rejeita com visibilidade
```

### Dashboard de uso de tabela (proposta Motor Analítico v2)
- % em cada tabela por vendedor
- Evolução temporal (tendência)
- Correlação com taxa de conversão
- Identificação de outliers (ex: vendedor X sempre amarela, conversão alta — amarela está barata demais? ou ele é muito bom?)

---

## Conexões

- [[00 - Visão Geral Precificação]]
- [[01 - Fórmula do Lucro]]
- [[02 - Fórmula de Preço Sacchelli]]
- [[08 - Simulador HTML - Arquitetura]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/04 - Qualidade de Dados]]
- Vault estratégico: [[Pricing - Precificação]], [[Custo de Servir]]
