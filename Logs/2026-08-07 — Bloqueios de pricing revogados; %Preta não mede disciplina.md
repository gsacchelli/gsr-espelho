---
data: 2026-08-07
tipo: log
status: vigente
---
# Bloqueios de pricing revogados — e o que %Preta realmente mede

**Contexto:** varredura "o fato que originou a regra ainda é verdade?" nas
regras vivas (`bloqueios_pricing.yaml`, `alarmes_flori.yaml`,
`cotacoes_overrides.yaml`), pedida pelo Gustavo após o caso da vigia de
material monitorado (alvo baseado em bug já corrigido).

## As decisões (Gustavo, textualmente)

1. **Bloqueio de vendedor (Aline) — REVOGADO.** *"Não existe bloqueio de
   vendedor; os preços realizados na tabela preta foram PRÉ-AUTORIZADOS por
   mim. O vendedor ou gerente não tem autonomia para liberar o pedido —
   portanto não tem por que bloquear tabela preta."*
2. **Bloqueio de cliente (TER BRASIL) — REVOGADO.** *"Os preços foram
   autorizados, são baixos, mas são estratégicos"* (volume na região de
   Caxias do Sul; mix 20MnCr5 em barra a R$ 8,90/kg bruto, ICMS 12%).

O mecanismo (`vw_pricing_bloqueios`, `flag_bloqueio`, `NEGAR`) continua no
código e testado, com as listas VAZIAS — pronto para bloqueio com razão
operacional real (crédito, litígio, ruptura). Preço autorizado não é razão.

## A consequência conceitual — maior que a regra

**%Preta por vendedor NÃO mede disciplina do vendedor.** Mede o que a
diretoria autorizou, fatiado por quem vendeu. Toda leitura que trate Preta
alta como indisciplina atribui ao vendedor uma decisão do Gustavo. Afeta:
Stoplight do Pricing (semáforo por vendedor) e
`agente/analises/pricing.py::pct_preta_vendedor`. A métrica continua útil —
mostra qual carteira PRECISA de Preta para vender (mix/concorrência) — mas o
rótulo de culpa está errado. Reenquadramento das telas: pendente, a decidir.

## Por que a regra sobreviveu 3 meses sem ninguém notar

O bloqueio de vendedor NUNCA funcionou: `vendedor IN ('Aline Damin Fortes')`
contra cotações que gravam `Aline - CXJ` — match exato falhando desde 05/05.
Regra que não morde não gera atrito; sem atrito ninguém questiona a premissa.
(Mesma família do vendedor_canon: RAF grava nome completo, cotações gravam
fantasia.)

## Varredura completa (3 arquivos, 8 regras)

- `cotacoes_overrides.yaml`: ✅ limpo — 3 overrides aplicados ao centavo no
  silver, 2 conferidas íntegras, "não afeta win rate" do WEG confirmado
  (`disputa_real=False`).
- `alarmes_flori.yaml` (forjado>50k): fato segue verdadeiro, mas sobrepõe a
  regra nova "emitida >100k" da vigia — alinhamento pendente.
- `bloqueios_pricing.yaml`: revogado (acima). Detalhe: `proxima_revisao:
  2026-07-31` tinha vencido sem ninguém voltar — regra com data de revisão
  precisa de guarda que cobre a revisão.

## Relacionado
- `Logs/2026-08-07 — Tolerância de peso...` (a pergunta da TER BRASIL que
  nasceu desta revogação)
