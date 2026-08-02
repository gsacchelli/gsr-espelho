---
tipo: log
domínio: sistema-de-dados
criado: 2026-08-02
tags: [continuidade, custo, margem, cockpit, raf, calibracao]
---

# 2026-08-02 — Onde parei (custo, margem e calibração)

Ponto de retomada da sessão de 01-02/08. Tudo commitado, testes verdes.

## O que ficou pronto

**Custo do ERP no lake** (entrega do Nelson em 31/07, consumida em 01/08).
`CustoMP`/`CustoTotal` de `BI.Cotacao` e `BI.Pedido` fluem até o gold:
cobertura 98,7% (pendentes), 99,5% (encerradas 2026), 99,8% (pedidos).
Mais `PrazoEntrega` (100%), `StatusPedido`, `PedidoCliente`, `Origem`.

**Cockpit na régua `ck-2`.** Margem agora usa custo do ITEM (ERP) sobre preço
LÍQUIDO, não custo médio de família sobre bruto. Cobertura da margem
51,6% → **87,9% do R$**; cobertura da carga de ICMS 51,5% → **99,8%**.
Alerta de tabela furada (82 itens / R$ 1,41 MM, 96% em PROK BRASIL).

**Convenção de custos do RAF auditada e travada.** Três rotas independentes
confirmaram: `ABCCUS_X` = COBRADO, `ABCCUS_X_COB` = REAL, **exceto no AÇO**
(onde o sem-sufixo é custo — o vault generalizava errado). O código estava
certo; a documentação dos dois lados estava errada em pontos diferentes.
Agora há teste sobre dado real (`test_convencao_custo_softcomp_ancorada_no_dado`).

**Semáforo calibrado** no drawer: traduz a MC da cotação para a MC que ela
vira no RAF, com base de 15 mil itens pareados, recalculada a cada rodada.

## ⚠️ O que exige atenção na retomada

**A calibração foi corrigida duas vezes hoje, ambas por questionamento do
Gustavo.** Errei a base (usei `LiquidoAco`, que já tem serviços descontados,
em vez de `ValorLIQ`) e a estatística (mediana simples em vez de ponderada
por R$). Lição: **todo número novo tem de ser confrontado com a régua que o
Gustavo já conhece (MC_Total ÷ ValorLIQ ≈ 31,8%) antes de ir para a tela.**
Se não bate com a percepção dele, provavelmente está errado.

**Tabela de calibração vigente** (base ValorLIQ, ponderada, itens de nota
única, líquido ≥ R$ 500, `LiquidoAco` > 0):

| MC na cotação | n | MC real (ponderada) | abaixo de 15% |
|---|---|---|---|
| ≥ 0% | 63 | 6,5% | 79% |
| ≥ 10% | 5.044 | 26,1% | 16% |
| ≥ 15% | 4.974 | **33,6%** | 3,7% |
| ≥ 20% | 2.851 | 39,4% | 1,4% |
| ≥ 30% | 774 | 51,9% | 0,5% |

## Pendências, em ordem

1. **C4 — reordenar o Foco pela MC calibrada: RECOMENDEI NÃO FAZER agora.**
   Muda 18 das 20 posições, mas é estimativa sobre estimativa e seria a 2ª
   mudança de semântica do `me` no mesmo dia (o snapshot ficaria com 3 réguas
   na mesma semana). Sugestão: deixar `ck-2` rodar 2-3 semanas, medir com
   `make cockpit-desfechos` se melhorou, e só então decidir.
2. **P1 — painel de drift no portal** (separa margem comercial de ganho de
   estocagem). Depende de o Gustavo achar que muda como avalia a MATRIZ.
3. **`DataEncerramento`** — pedida ao Nelson em 02/08. Quando chegar, rodar
   `python3 MotorAnalitico/sql/conferir_colunas.py` (já mapeada com sinônimos)
   e ligar no `pull_encerradas.py`, que hoje preserva a data do export manual.
4. **Inventário das 44 colunas não usadas do RAF** — três com 99%+ de
   preenchimento: `ABCSETPDES` (setor de produção, 100% — **resolve pendência
   pedida ao Nelson**), `ABCOII_PRA` (prazo da OI), `ABCOIIQUA` (qualidade).
5. **ANDRITZ SCHULER 22/05** — único caso substantivo de MC alta na cotação
   virando negativa no RAF sem ser artefato (R$ 94k, serviços em só 15%).
   Merece um olhar do Gustavo.
6. **Março/2026** — CPV contábil de R$ 15,88 MM contra receita de R$ 14,71 MM
   (lucro bruto negativo). **Explicado**: entrada pesada de material importado
   impactando estoque. Não é erro; é competência da compra × da venda.

## Decisões desta sessão (não re-litigar)

- **Corte entra 100% como margem** — o `ABCCUS_CTE_COB` foi criado zerado POR
  DESIGN, sobre a premissa da AFS de que corte é conta orçamentária e não custo
  direto. Gustavo discorda pessoalmente (para ele é custo de produção), mas a
  convenção fica. R$ 1,86 MM/ano.
- **A diferença DUO × RAF é estrutural** — "são visões diferentes do negócio".
  Nunca ler margem contábil mensal isolada como desempenho comercial.
- **MC contábil negativa quase sempre é artefato**, não venda ruim: 3 linhas em
  37.606, onde o serviço externo cobrado supera a venda inteira.

## Conexões

- [[2026-08-01 — Custo na cotação e no pedido (entrega Nelson)]]
- [[2026-08-02 — Dicionário do RAF e a semântica dos campos do pedido]]
- [[Sistema Operacional Comercial/04 RAF/02 - Convenção Softcomp (Invertida)]] — auditada
- [[Sistema Operacional Comercial/05 Cotações/06 - Margem × Win Rate (curva empírica)]]
- Repo: `06_Docs/Custo_Referencia_vs_Real_2026-08-01.md`, `06_Docs/LEIA-ME_Dicionario_RAF.md`
