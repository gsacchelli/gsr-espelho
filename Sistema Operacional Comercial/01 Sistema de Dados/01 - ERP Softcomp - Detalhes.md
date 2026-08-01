---
tipo: referência-técnica
domínio: sistema-de-dados
criado: 2026-04-17
última-revisão: 2026-08-01
tags: [erp, softcomp, dados, fonte-verdade]
---

# 01 — ERP Softcomp — Detalhes

## O que é o Softcomp

ERP proprietário brasileiro utilizado pela AFS para operação completa: cadastros de cliente/fornecedor, cotações, pedidos, faturamento, estoque, fiscal, financeiro, contábil.

É a **fonte de verdade única** para dados operacionais comerciais. Qualquer divergência entre ferramenta externa e Softcomp: Softcomp ganha.

---

## Infraestrutura

| Item | Detalhe |
|---|---|
| Banco | SQL Server |
| IP | 10.0.0.215 |
| Base | SGRA_SACCH |
| Rede | Interna AFS (não exposta) |
| Acesso externo | Via VPN interna ou export manual |

**Implicação operacional:** análises externas dependem de **export Excel/CSV** (camada 2 do sistema). Conexão direta SQL fica para v2 do Motor Analítico, sob VPN.

---

## Fluxos principais do Softcomp

```
CADASTRO ─┬─► CLIENTE (código, razão, endereço, cidade*, tipo tabela)
          │
          ├─► FORNECEDOR (usinas, tradings, prestadores)
          │
          └─► PRODUTO (material, família, preços A/B/C)

COTAÇÃO ──► emitida por vendedor
          │
          ├─► aberta (em negociação)
          │
          ├─► encerrada ganha → vira PEDIDO
          │
          └─► encerrada perdida (motivo) → análise post-mortem

PEDIDO ───► libera produção / separação
          │
          ├─► FATURAMENTO → gera RAF
          │
          └─► ENTREGA → fecha ciclo

ESTOQUE ──► atualização por entrada/saída
          │
          ├─► consultas por SKU, família, unidade
          │
          └─► snapshot posição (exportável)
```

*Cidade: campo truncado em 20 chars — ver [[04 - Qualidade de Dados]]

---

## Cadastros — campos críticos

### Cliente
- Código (identificador único)
- Razão social
- **Cidade** (⚠ truncado em 20 caracteres)
- Tipo de tabela (A=Verde, B=Amarela, C=Vermelha) — determina preço-base
- Vendedor responsável
- Canal (INT/PJ/REP) — **atenção: canal é fiscal, não comercial** ([[05 - Padrões de Desenvolvimento]])
- Status (ativo, inativo, em desenvolvimento*)

*Carteira "Clientes em Desenvolvimento" ≠ prospects; são contas fechadas entre diretorias, vendedor não entra. ~R$3,3M/ano, ~8 clientes. Não incluir em ranking de vendedor.

### Produto
- Código interno
- Família: Aço + Tipo + Perfil + Acabamento + Faixa de Bitola — ver [[03 Estoque/01 - Família Canônica]]
- Tabela de preço mínimo por faixa (A/B/C)
- Fornecedor-origem
- Unidade de medida (kg, peça, metro)

### Produção / Cotação
- OS (número) + ITE (item)
- Material de partida × Material faturado (podem divergir — permite rastrear transformação)
- Fases de processo (corte, tratamento, ensaio)
- Vendedor que emitiu
- Motivo de encerramento (se perdida)

---

## Tabelas de preço (A/B/C)

**3 níveis oficiais:**

| Tabela | Cor | Alçada | Significado |
|---|---|---|---|
| A | Verde | Vendedor livre | Preço cheio, cliente premium |
| B | Amarela | Vendedor livre | Preço intermediário |
| C | Vermelha | Vendedor livre até este piso | Piso normal de venda |
| (abaixo de C) | — | **Apenas Diretor** | Exceção, requer justificativa |

**Zona cega:** entre Verde e Vermelha, vendedor age sozinho. Diretor só vê o que desce abaixo da Vermelha. Essa lacuna é **onde mora vazamento de margem** — objeto de atenção em [[02 Precificação/07 - Tabelas e Alçadas]].

**Campos RAF correspondentes:**
- `ABCPRE_MIN_A` = piso Tab Verde (R$/kg)
- `ABCPRE_MIN_B` = piso Tab Amarela (R$/kg)
- `ABCPRE_MIN_C` = piso Tab Vermelha (R$/kg)

---

## Motivos de encerramento de cotação

Lista oficial do Softcomp (classificação pelo vendedor no pós-fechamento):

- **Cotação somente para orçamento prévio** — comum, **ambíguo** (ver seção Armadilhas)
- **Preço** (perdida por preço) — com ou sem concorrente nomeado
- **Prazo** (perdida por prazo)
- **Qualidade / técnico**
- **Ganhou** (vira pedido)
- **Projeto cancelado**
- **Outros**

### Armadilha crítica — "Orçamento prévio"

Essa classificação **é heterogênea** e esconde 2 perfis diferentes:

| Perfil | Descrição | Tratamento correto |
|---|---|---|
| Tabelista real | Cliente que compra de outro fornecedor e usa AFS como referência de preço | Atendimento industrializado, zero customização |
| Projeto real (ANDRITZ, PROK, SUPERIOR) | CAPEX industrial, ciclo 6-18 meses | Follow-up intensivo, oposto do industrializado |

O Softcomp **não distingue** os dois. O vendedor encerra em 2-5 dias como "orçamento prévio" porque **o ERP não tem status adequado** para projeto em longo prazo.

**Alavanca estrutural proposta (não implementada):** status novo "Em Projeto" no Softcomp — ver [[05 Cotações/03 - Orçamento Prévio vs Projeto Real]].

---

## Limitações estruturais

### 1. Truncamento de cidade (20 chars)
Bug conhecido. Gera duplicidade e falsos "municípios" nos dados. **Mitigação:** `config/cidades_overrides.yaml` no Motor Analítico.

### 2. Sem status "Em Projeto"
Pipeline de projeto longo desaparece como "orçamento prévio". Impacto estimado: dezenas de milhões em pipeline não-acompanhado por trimestre.

### 3. Canal INT/PJ/REP é fiscal, não comercial
Quase todos vendedores são PJ por natureza fiscal/tributária. **Não comparar performance por canal** — erro analítico comum.

### 4. Remuneração sobre fat s/IPI, não sobre MC
Sistema não ajuda a alinhar incentivo com margem. Ver discussão em `project_afs_remuneracao_alcada` (memória).

### 5. Inbound vs Outbound indistinguíveis
Toda cotação é lançada pelo vendedor. Não há como diferenciar demanda que chegou (inbound) de prospecção ativa (outbound).

### 6. Sem histórico versionado de preço da tabela
Quando tabela muda, antigo é sobrescrito. Análises retroativas de preço perdem acurácia.

---

## Exports mais usados

### DetalhesRAF.xlsx
- **O que é:** RAF — Relatório de Acompanhamento de Faturamento
- **Colunas:** 133 (cobradas e reais)
- **Volume:** ~5.000 linhas/mês (~19.500 Jan-Abr/2026)
- **Faturamento coberto:** ~R$66M Jan-Abr/2026
- **Frequência recomendada:** mensal (ideal semanal)
- **Uso principal:** análise de margem real, custo de servir, calibração do simulador
- **Nota completa:** [[04 RAF/00 - Visão Geral RAF]]

### Cot_Encerradas.xlsx
- **O que é:** cotações fechadas (ganhas + perdidas) com motivo
- **Uso principal:** win rate, análise de perdas, intel competitiva
- **Análise referência (mar/2026):** 29.748 cotações Jan-Fev/2026 → win rate 67,6%, 21% perdidas por preço
- **Nota completa:** [[05 Cotações/00 - Visão Geral Cotações]]

### tabela_preco.xlsx
- **O que é:** tabelas A/B/C vigentes
- **Uso:** input do simulador, referência de piso
- **Frequência:** mensal ou ao mudar

### Estoque.xlsx
- **O que é:** posição de estoque por SKU e unidade
- **Uso:** painel de estoque, análise de giro
- **Nota completa:** [[03 Estoque/00 - Visão Geral Estoque]]

### Critérios_planilhas.xlsx
- **O que é:** regras de negócio editáveis — famílias, bitolas, cidades, grupos de concorrentes
- **Uso:** input de configuração do Motor Analítico
- **Convenção:** Gustavo edita o Excel, motor rebuilda
- **Completude:** parcial para cidades (207 de 645 SP). Lista completa em `config/cidades_sp.xlsx` agora é fonte canônica.

---

## Segurança e confidencialidade

Dados do Softcomp são **internos AFS**. Contêm:
- Preços de custo de aço (informação material)
- Margens por cliente (sensível comercial)
- Lista de clientes e relacionamentos (propriedade AFS)

**Regras de manipulação externa:**
- Arquivos brutos nunca devem ser enviados para serviços externos (cloud, IA online não-local)
- Análises externas rodam **localmente** (Python, HTML, Python sandbox pessoal)
- Dados derivados (agregados, rankings) podem ser compartilhados, dados individuais não

---

---

## Integração SQL — schema `BI` (réplica read-only)

Acesso liberado pelo Nelson (Softcomp) em 07/2026: `10.0.0.215` · `SGRA_SACCH` ·
schema `BI` · usuário `SACCHELLI_BI` (somente leitura). **10 objetos**: `Cotacao`,
`Pedido`, `RAF`, `Clientes`, `Vendedores`, `Gerentes`, `Equipes`, `Empresas`,
`Familias`, `Motivos`. Inventário técnico completo (coluna a coluna) fica no repo:
`06_Docs/Softcomp_SQL_BI_Schema.md`.

⚠ **O servidor é interno.** Fora da rede AFS / VPN nada disso responde — os
LaunchAgents registram "fora da rede — pulando" e seguem.

### Entrega de 31/07/2026 — custo na cotação e no pedido

O Nelson adicionou colunas (validadas em 01/08 contra a réplica; cobertura de 2026
entre parênteses):

| View | Coluna | Cobertura | O que destrava |
|---|---|---|---|
| `BI.Cotacao` | `CustoMP`, `CustoTotal` | 99,4% | MC estimada **por item, na cotação** — antes só existia proxy por custo de reposição da família (~49% do R$) |
| `BI.Cotacao` | `Origem` | 100% | origem fiscal por item (CST-A) — melhora o ajuste de ICMS |
| `BI.Pedido` | `CustoMP`, `CustoTotal` | 99% | margem no **pedido**, sem esperar o RAF do mês |
| `BI.Pedido` | `PrazoEntrega` | 100% | aposenta a semente manual do SP8001A na Carteira de Pedidos |
| `BI.Pedido` | `StatusPedido` | 1,2%* | **cancelado ≠ faturado** — resolve o caso SUPERIOR |
| `BI.Pedido` | `PedidoCliente` | 53% | OC do cliente (depende de o cliente informar) |
| `BI.Pedido` | `Procedencia` | 97% | procedência do material |

\* `StatusPedido` é **sinal de exceção**, não campo mal preenchido: vazio = pedido
normal; `Abortado`/`Encerrado` = cancelado. Em 2026 são 519 itens / R$ 4,6 MM que
até então entravam como faturamento (o cancelamento só zerava o `Saldo`).
Validado no caso SUPERIOR: pedido 343024 `Encerrado` × 343047 (reemitido) vazio.

> **Custo do ERP é REFERÊNCIA, não custo realizado.** É o custo que o vendedor
> tinha na mão ao precificar, carimbado na emissão. O custo REAL é apurado no
> **RAF**, depois de faturar. Confrontar os dois é justamente a análise que a
> entrega destrava — ver [[04 RAF/00 - Visão Geral RAF]].

### Nomes: o que pedimos ≠ o que veio

Pedimos `Situacao` e `OrdemCompra`; vieram `StatusPedido` e `PedidoCliente`. Por
isso a conferência é automatizada e tolera sinônimos:
`python3 MotorAnalitico/sql/conferir_colunas.py` — compara **o que pedimos × o que
existe × o que os loaders consomem**, e separa o que é pendência do Nelson do que
é trabalho nosso. Rodar depois de toda mexida dele, antes de cobrar qualquer coisa.

⚠ **Coluna nova na view não chega sozinha no lake**: os loaders fazem `SELECT` com
lista explícita. Enquanto ninguém edita o SELECT + enricher + silver + gold, o
dado existe na origem e é ignorado em silêncio.

### Pendências abertas com o Nelson (01/08/2026)

1. **Histórico** — nova planilha, já combinado (é a pendência que o Gustavo rastreia).
2. `BI.Cotacao.DataEncerramento` — **descoberta em 28/07, provavelmente não está na
   lista dele**: a view não expõe data de encerramento, então 11,7% das encerradas
   de 2026 ficam sem data e o ciclo emissão→fechamento não fecha.
3. `BI.Cotacao.PrazoEntrega` e `RazaoSocial`; `BI.Pedido.SetorProducao`.
4. Detalhamento de custo: pedimos 9 componentes × real/cobrado (como em `BI.RAF`);
   vieram 2 agregados (MP + Total). **Decidir se o detalhe ainda é necessário**
   antes de cobrar — o agregado já resolve a maior parte das análises.
5. `BI.CondPagamentos` — cadastro de condições (hoje só vem o código).
6. `BI.RAF` segue espelhando o **acúmulo do relatório do usuário**, não as tabelas
   de faturamento (ver seção do RAF) — por isso o RAF continua manual.

---

## Conexões com outras notas

- [[00 - Arquitetura de Dados]] (visão do sistema)
- [[02 - Arquivos Brutos e Convenções]] (o que sair do Softcomp vira)
- [[04 - Qualidade de Dados]] (problemas conhecidos no dado bruto)
- [[04 RAF/00 - Visão Geral RAF]]
- [[05 Cotações/00 - Visão Geral Cotações]]

## Referência externa
- SQL Server: 10.0.0.215 (SGRA_SACCH) — rede interna AFS
- Documentação oficial Softcomp: solicitar ao provedor
