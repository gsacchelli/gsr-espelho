---
tags: [log, decisao, simulador, motor-pricing, camada-8b, ponta]
date: 2026-04-21
---

# Camada 8b Ponta fechada

## Contexto

Após fechamento da Camada 6 (Importação) na mesma sessão, Gustavo optou por seguir pra Camada 8b Ponta — listada como pendente no CLAUDE.md.

## Descoberta inicial

Ao investigar o escopo do trabalho, descobri que o fix principal **já estava implementado**:

- HTML `simCalc` L4139: `const hrCorte=_pontaAtivo?hrEfetivo:hrTotal` ✓
- HTML setup: `const setupMin=_pontaAtivo?0:eSetupSec/60` ✓
- Motor `calcCorteV4` L1991: mesma lógica ✓
- Motor setup em ponta L1986: mesma lógica ✓
- Card Ponta no simulador (L4945-4958): já renderiza "Ganho vs Sucata" com indicador laranja ✓

O CLAUDE.md estava desatualizado — o fix e o card foram feitos em alguma sessão anterior sem atualizar a nota.

## Gap real identificado

Embora a **lógica** estivesse correta, a **cobertura de testes** não existia:

- Todas as 8 fixtures 01-08 têm `ponta: { aproveitamento_ativo: false }`
- Nenhum teste sintético exercitava `pontaAtiva=true`
- Risco: regressão silenciosa se alguém mexer no cálculo de ponta

## Decisão

Em vez de re-implementar o já feito, **fechar Camada 8b-ponta formalmente** com:
1. Testes sintéticos cobrindo a lógica de ponta no motor
2. Guia de captura de fixture ponta (dívida retroativa) pra quando houver cotação real

## Execução

### 15 testes sintéticos adicionados ao motor

**Bloco `calcPontaAtiva` (4 testes):** ativação condicional
- Ponta ativa: isPc + comp ≤ comp_max_mm + flag on
- Ponta inativa: comp > comp_max_mm
- Ponta inativa: unidade ≠ pc
- Ponta inativa: flag off

**Bloco `calcCorteV4` (7 testes):** fórmula do custo
- Com ponta: `hr_corte === hr_efetivo`
- Sem ponta: `hr_corte === hr_total`
- Com ponta: `setup_min === 0`
- Sem ponta: `setup_min > 0`
- Ponta reduz custo real vs sem ponta (redução > 5%)
- Fórmula: `custo_maquina = hrEfetivo × (n × tempoPorCorte) / 60` sem setup
- Não aplicável quando `isPc=false`

**Bloco `calcPonta` (4 testes):** receita sucata + ganho vs venda
- Retorna receita bruta e líquida (PIS dedutível)
- `ganho_vs_sucata = dreResultado + dreCustoMP − sucataLiquida`
- Retorna `aplicavel=false` quando ponta inativa
- Default `sucata_rs_kg = 1.5 R$/kg`

### Guia de captura de fixture ponta

Criado `03_Ferramentas/js/fixtures/CAPTURA_FIXTURE_PONTA.md` com:
- Cenário típico de ponta (barra curta <30cm, aço nobre)
- Snippet de console pra capturar `SIM_LAST_CALC` com ponta ativa
- Lista dos campos a validar na regressão bit-idêntica
- Reconhecimento explícito de que testes sintéticos são camada 1; fixture real é camada 2 (opcional mas recomendada)

## Status final da suite

**704/704 testes verdes:**
- 499 motor precificação (+15 novos de ponta)
- 85 schema proposta
- 106 gerador proposta
- 14 comparativo identidade

## Dívidas retroativas abertas

- **Fixture 09 (Repasse nacional)**: capturar na próxima cotação nacional real
- **Fixture 10 contra DI arquivada**: validação fiscal externa (opcional)
- **Fixture ponta ativa**: capturar na próxima cotação com ponta (guia pronto)
- **Fixtures 04-08 com `sell_unit=kg/m` e `margin_base=vermelha`**: recaptura com instrumentação estendida Camada 7

## Reflexão sobre processo

Padrão que emergiu nesta sessão:
1. Código muda rápido
2. Documentação de status (CLAUDE.md) atrasa
3. Re-investigação do escopo real sempre vale antes de implementar

Recomendação pra próximas sessões: abrir cada camada com **grep do motor + HTML** pra confirmar estado real ANTES de assumir que está pendente.

## Próximas frentes disponíveis

- 8b material comprado (sair do placeholder)
- Wrapper fino: migração HTML → motor.js via adapter mais limpo
- Gerador de Proposta Fase 3+: polir impressão, reabrir orçamentos salvos
- Fase pós-motor de config: migrar hardcodes AFS (tabela CF, certificações, fases) pra `parametros_afs.json`
