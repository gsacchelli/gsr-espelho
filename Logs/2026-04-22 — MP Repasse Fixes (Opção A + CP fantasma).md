---
data: 2026-04-22
tipo: log
projeto: Simulador Precificação
fase: Bug hunt pós-W3e-A
status: fechado
---

# MP Repasse — Fixes consolidados (Opção A estrita + CP fantasma)

## Resultado

Dois bugs descobertos em sequência no uso real do simulador com MP Repasse após a instalação do W3e-A (motor como fonte canônica do card Repasse). Ambos são a mesma classe de problema — **estado fantasma herdado do modo anterior** — em superfícies diferentes (custo líquido da MP no primeiro, CP na Memória de Cálculo no segundo).

Ambos validados em produção por Gustavo:
- Opção A: "funcionou" (Açokorte Proposta N° 500004 Item 2, R$ 12.514,71/Pç, MC 20,22%).
- CP fantasma: "funcionou".

## Bug 1 — Custo líquido fantasma em MP Repasse com NF vazia

### Sintoma

Item já existente, com custos digitados para MP padrão (custoLiq preenchido), ao marcar "MP Repasse" sem preencher a NF o simulador continuava usando os custos antigos. Card Repasse mostrava preço calculado usando o custo da MP padrão como se fosse o custo da nota fiscal do repasse — sem indicação nenhuma de erro.

Gustavo: *"peguei um item ja existente, preenchido com materia-prima de partida padrão, selecionei MP Repasse e o simulador continuou assumindo os custos digitados anteriormente da materia-prima de partida padrão, assim como, os serviços e comprados... essa logica estaria certa?"*

### Causa raiz

Surface triangular — todos concordavam no valor errado:

1. **HTML `simCalc`**: havia guard silencioso `if(repCustoLiqTon > 0){ custoLiq = repCustoLiqTon; }` — se a NF estava vazia, o swap não acontecia e o custoLiq do modo anterior (MP padrão) continuava vivo no cálculo.
2. **Motor `calcCustoLiq`**: fazia fallback pro `custo.liquido_rs_ton` quando MP Repasse estava ativa mas `custo_liq_ton=0`.
3. **Test suite**: tinha teste **documentando o bug como expected** — *"repasse ativo + custo_liq_ton=0 → fallback pro liquido_rs_ton"*.

**Por que o shadow bloqueante não pegou:** ambos os lados (HTML e motor) concordavam no valor errado. Shadow só detecta divergência, não detecta "ambos errados".

### Fix — Opção A estrita

Decisão alinhada com Gustavo: quando MP Repasse ativa e NF vazia, o card Repasse **bloqueia com placeholder**, sem fallback silencioso.

**Motor** (`motor_precificacao.js`):
- `calcCustoLiq` L.627-649: removido fallback silencioso. Se `mp.ativo && mp.custo_liq_ton=0 && !imp.ativo`, retorna `0` (explícito).
- `cards.repasse.ativo` L.1679-1684: `ativo = mpRepAtivo && mgMpRep > 0 && custoLiq > 0`. Card só "ativa" quando tem custo real.

**HTML** (`Analise_Precificacao_Sacchelli.html`):
- `simCalc` L.3845-3863: removido guard silencioso. Força swap sempre (inclusive pra 0) quando Repasse on.
- W3e-A block L.4691-4720: 3 cases (ativo / bloqueado / indisponível) com flag `_repaseBloqueado`.
- Placeholder L.4747-4762: injetado após `_applyCard` — "Preencha a NF do Repasse" + ícone muted.

**Tests**:
- Teste invertido: `calcCustoLiq` retorna 0 (sem fallback) quando repasse + NF vazia. L.1806-1818.
- 5 testes W3b-2 ganham `custo_liq_ton: 5000` explícito (pré-Opção A assumiam fallback).
- Novo bloco: "W3b-2 — Opção A estrita: Repasse ON + NF vazia bloqueia o card" — 2 testes validando `cards.repasse.ativo=false` com `custo_liq_ton=0`.

**Suite:** 555 motor + 202 render + 85 schema + 14 comparativo identity — **ALL PASS**.

### Validação em produção

Açokorte Proposta N° 500004 Item 2 — Pacote com Repasse ativo + NF preenchida retornou R$ 12.514,71/Pç (MC 20,22%). Teste do cenário original (item com MP padrão + trocar pra Repasse sem NF): placeholder aparece corretamente ("Preencha a NF do Repasse"), sem número fantasma.

Cobertura de cenários validada:
- Item criado do zero no modo Repasse → OK.
- Item duplicado via Pacote (mesma superfície do restore) → OK, porque `pacoteRestoreFullState` passa pelo mesmo `simCalc` → `calcCustoLiq`.

---

## Bug 2 — CP (Corpo de Prova) fantasma em MP Repasse/Pç

### Sintoma

Após o fix do Bug 1, Gustavo notou que ao trocar um item com CP ativo (EMT, EMI, MET) de MP padrão pra MP Repasse com unit=Pç:
- Menu "Serviços / Fases de Produção" escondia a opção CP (correto — material engenheirado não tem barra pra cortar CP).
- **Mas** a linha CP continuava aparecendo na Memória de Cálculo, precificando normalmente.
- Se trocasse unit pra Kg (barra bruta), CP reaparecia no menu.

Gustavo: *"nesse caso, deveria dar um alerta, deveria excluir o CP?"*

### Física do negócio

Alinhamento com Gustavo antes de codar:
1. **CP só faz sentido com barra bruta.** Usa-se um pedaço da barra pra produzir o corpo de prova dos ensaios destrutivos (EMT, EMI, MET, outros).
2. **CP com MP padrão + qualquer unit**: válido (barra bruta, vai cortar CP em casa).
3. **CP com MP Repasse/Kg (barra bruta comprada)**: válido (mesma lógica).
4. **CP com MP Repasse/Pç (peça engenheirada)**: **inválido** — não há barra pra cortar.
5. **CP com Importação/Pç**: mesmo caso (peça engenheirada vinda de fora).

Também confirmado: só **CP e corte** são incompatíveis com material engenheirado. TT/TD/USX/EMB continuam aplicáveis em peça engenheirada (podem tratar, dimensionar, usinar, embalar o material pronto).

### Fix — Opção B (remove + toast)

Decisão alinhada com Gustavo:
- **Remoção automática** (não alerta bloqueante) — reversão manual (usuário reativa se quiser, não auto-restaura).
- **Toast informativo** (não silencioso) — dar visibilidade do que o simulador fez.
- **Escopo narrow** — só CP, não expandir auditoria pra outras fases.

**HTML** (`simUpdateRepasseVisibility` L.3404-3419):
```js
const _cpTipoEl=document.getElementById('sim-cp-tipo');
if(_cpTipoEl && _cpTipoEl.value!=='nao'){
  _cpTipoEl.value='nao';
  const _cpFields=document.getElementById('sim-cp-fields');
  if(_cpFields) _cpFields.style.display='none';
  const _dentroRestore=(typeof _pacoteRestaurando!=='undefined' && _pacoteRestaurando);
  if(!_dentroRestore && typeof _toast==='function'){
    _toast('CP removido: material engenheirado não requer corpo de prova.');
  }
}
```

**Por que esse spot:** `simUpdateRepasseVisibility()` é o funil canônico que já calcula `comprouPeca` e é chamado pelos 4 caminhos que levam a material engenheirado:
1. `simToggleRepasse` (liga Repasse com unit=Pç).
2. `simRepUnitChange` (muda unit pra Pç com Repasse ativo).
3. `simToggleImportacao` (liga Importação com cfr-unit=Pç).
4. `_simImpUnitChange` (muda cfr-unit pra Pç com Importação on).

Silencia o toast durante `_pacoteRestaurando` pra não poluir a troca de item no pacote — cleanup silencioso funciona, só não avisa (usuário não disparou a ação).

**Reversão manual:** nada no código reativa CP quando Repasse sai ou unit volta pra Kg. Se Gustavo quiser CP de novo (cenário MP padrão pra corpo de prova), seleciona manualmente no dropdown.

### Validação

- `node --check` no JS embutido (690.671 chars): SYNTAX OK.
- Produção: Gustavo validou o fluxo (MP padrão + CP → MP Repasse/Pç → CP removido + toast aparece + Memória de Cálculo sem linha CP).

## Classe do problema (padrão que continua aparecendo)

Ambos os bugs do dia são a mesma classe vista em Bug 1 e Bug 4 da série Proposta (21/04):

> **Estado fantasma herdado do modo anterior.** Toggle muda o modo, mas dados do modo anterior ficam em campos ocultos e continuam sendo lidos pelo cálculo.

Superfícies no dia 22/04:
- Bug 1: `custoLiq` de MP padrão vivendo em cálculo de MP Repasse porque o guard silencioso do swap pulava quando NF=0.
- Bug 2: `sim-cp-tipo='ensaio'` vivendo em cálculo de material engenheirado porque o panel estava só escondido visualmente (não resetado).

**Padrão de correção:** no ponto em que o toggle decide "o cenário mudou", **resetar** os dados do modo anterior em vez de só esconder. Se o reset for relevante pro usuário, toast. Se for silencioso, só cleanup. Auto-reversão geralmente é má ideia — deixa o usuário controlar o modo novo.

**Auditoria futura (débito leve):** outros panels hidden no modo Repasse/Pç provavelmente têm mesma classe de bug (sim-corte-mm, sim-acorte, sim-extcorte, sim-lamina, sim-tol, sim-vpp parcialmente tratado em L.3917). Só capturar quando aparecer sintoma em produção — não vale auditoria proativa. Essa classe é notoriamente fácil de introduzir e notoriamente difícil de flagrar sem uso real.

## Arquivos mudados

- `03_Ferramentas/js/motor_precificacao.js` — Opção A estrita (calcCustoLiq + cards.repasse.ativo).
- `03_Ferramentas/js/motor_precificacao.test.js` — teste invertido + novo bloco Opção A.
- `03_Ferramentas/Analise_Precificacao_Sacchelli.html` — swap sempre + W3e-A block + placeholder + CP reset.

## Tempo

- Bug 1 (Opção A): ~1h30 (diagnóstico + motor + HTML + testes + validação produção).
- Bug 2 (CP fantasma): ~20min (diagnóstico alinhado + fix + syntax check + validação).
- Log + CLAUDE.md: ~15min.

## Tasks fechadas

- #32 — Aplicar fix Opção A (estrito).
- #33 — Validar fix Opção A em produção e fechar log.
- #34 — Fix CP fantasma em MP Repasse/Pç (Opção B).
- #24, #25, #23, #29, #30, #31 — W3e-A pre-work (motor canônico shadow antes do render + auditoria de contrato).

## Pendências relacionadas

- **W3e propriamente dito** (próxima frente disponível): apagar o cálculo inline de `cards.repasse` no HTML agora que o motor é a fonte canônica e bateu bit-idêntico no shadow por dias de uso real.
- **Fixture com MP Repasse/Pç + CP ativo (pré-fix)** — não capturei antes do fix. Se precisar reproduzir o bug no futuro, vai ter que forjar manualmente em item antigo.
- Shadow bloqueante continua ativo, 0 divergências aritméticas nas últimas horas de uso.
