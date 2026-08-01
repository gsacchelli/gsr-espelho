# 2026-04-21 — Bugs 3, 4 e 5 da Proposta Comercial (FIX)

## Bug 5 — pacoteAfterCalc corrompe state durante restore (FIXADO 21/04/2026 noite)

**Sintoma:** após refresh (F5), tela "trava com os dados do Item 2" mesmo com PACOTE.ativo=0. Investigação mostrou que, no localStorage, Items 1 e 2 ficavam **idênticos** — Item 1 era sobrescrito com dados do Item 2.

**Investigação:** instrumentei `Storage.prototype.setItem` + `Object.defineProperty` no `PACOTE.itens[0].state` pra capturar cada write com stack trace. Log revelou o culpado: **`pacoteAfterCalc` chamado de dentro de `simCalc` durante `pacoteRestoreFullState`**.

**Sequência do bug:**
1. User clica pill Item 1 no rail (estava no Item 2).
2. `pacoteSwitchItem(0)`:
   - Captura Item 2.state (DOM atual = Item 2) ✓
   - `PACOTE.ativo = 0` (novo ativo)
   - `pacoteRestoreFullState(Item 1.state)` — **assíncrono**: seta `sim-table.value`, chama `filterSimFamilies()` síncrono, agenda `finalize` via `setTimeout(80)`
3. Dentro da parte síncrona: `filterSimFamilies` → `loadFamilyToSim` → `simCalc` → **`pacoteAfterCalc`**
4. `pacoteAfterCalc` executa `PACOTE.itens[PACOTE.ativo].state = pacoteCaptureFullState()` — mas ativo já é 0 E DOM ainda tem dados do Item 2 → Item 1.state é sobrescrito com DOM do Item 2.
5. Meu LS write posterior (já corrigido no Bug 5 inicial) serializa PACOTE.itens com Item 1 corrompido.

**Fix:** flag `_pacoteRestaurando` protege `pacoteAfterCalc` durante a janela de restore:

```js
let _pacoteRestaurando = false;

function pacoteRestoreFullState(f){
  _pacoteRestaurando = true;          // início do restore
  const finalize = () => {
    // ... todo o trabalho de restore ...
    _pacoteRestaurando = false;       // libera captura
  };
  // ... seta sim-table e agenda finalize via setTimeout(80) ...
}

function pacoteAfterCalc(){
  try {
    if (!_pacoteRestaurando) {        // só captura fora de restore
      if(PACOTE.itens[PACOTE.ativo])
        PACOTE.itens[PACOTE.ativo].state = pacoteCaptureFullState();
    }
    // renders continuam normalmente
  } catch(_){}
}
```

**Validação em produção (21/04 noite):**
- Antes do fix: Item 1.state corrompido logo após switch, ambos items ficam idênticos no LS.
- Depois do fix: log mostra Item 1=120 preservado, Item 2=651 preservado. Switch e F5 funcionam. Ponta mantida. Dados corretos em ambos os items.

**Fix complementar (Bug 5 inicial):** `pacoteSwitchItem` não chama mais `pacotePersist()` no final — grava LS direto com PACOTE já sincronizado. `pacotePersist()` recaptura DOM via `pacoteCaptureFullState`, e durante o restore o DOM ainda tem dados do item anterior.

**Auditoria pendente:** outras funções que chamam `pacoteRestoreFullState` seguido de `pacotePersist()` têm mesmo potencial de corrupção. Linha 9075 (restaura proposta) e `pacoteHidratarTodos` (linha 9599+) são candidatos — usam `sleep(160)` que tecnicamente respeita o async, mas vale auditar quando a janela de refactor abrir.

---



Sessão curta de fechamento dos dois bugs pendentes do teste guiado da manhã/tarde (ver `Logs/2026-04-21 — Teste Guiado Proposta.md`). Ordem executada: Bug 4 primeiro (mais simples, mesma classe do Bug 1 já validado), Bug 3 em seguida.

## Bug 4 — Ponta não persiste no refresh (FIXADO)

**Sintoma recapitulado:** Item gravado com ponta ON retornava ponta OFF após refresh. MCs Verde/Amarela/Vermelha/Preta voltavam aos originais da MP, divergindo do PDF imortalizado.

**Raiz confirmada (H1 do log da manhã):** `pacoteRestoreFullState` (linha 9249-9252) setava `sim-ponta-on.checked=true`, mas nunca disparava `simPontaToggle()` no restore. Side effects (override MC 12/9/6/3 + zerar simPhases/certs) não eram reaplicados.

**Fix aplicado (`Analise_Precificacao_Sacchelli.html`, pós-linha 9275):**

```js
// Reset defensivo — variáveis globais _pontaOrig* podem vazar entre itens
if(typeof _pontaOrigMC!=='undefined') _pontaOrigMC=null;
if(typeof _pontaOrigServicos!=='undefined') _pontaOrigServicos=null;
// Chama simPontaToggle APENAS quando snapshot tem ponta ON.
// Não é idempotente em relação a _pontaOrig* — chamar com OFF e _pontaOrigMC
// vazado de outro item restauraria MCs erradas.
if(f['_chk_sim-ponta-on']&&typeof simPontaToggle==='function'){
  try{simPontaToggle();}catch(_){}
}
```

**Escolha de design — por que `if(f._chk_)` e não "chamar sempre" (como Bug 1):**

No Bug 1 (`simToggleRepasse`/`simToggleImportacao`), chamar sempre é seguro porque as funções leem o checkbox internamente e aplicam display correto em ambos os casos (on/off). Em `simPontaToggle`, porém, o caminho OFF restaura `_pontaOrigMC` — variável global em memória que vaza entre itens. Cenário-quebra:

1. Item A: ponta ON → `_pontaOrigMC = {v:15, a:10, r:5, p:1}` (originais).
2. Troca pra Item B (ponta OFF, MCs diferentes) → restore seta MCs corretas do snapshot B.
3. Se chamasse `simPontaToggle()` sempre, ele entraria no branch OFF e restauraria MCs de A em cima das de B. ❌

**Solução:** reset defensivo + chamada condicional. Quando snapshot tem OFF, nada é feito (MCs restauradas do snapshot ficam válidas).

**Limitação conhecida (aceitável):** ao reabrir proposta com ponta ON e depois o usuário desmarcar ponta manualmente, MCs não voltam aos originais pré-ponta (porque `_pontaOrigMC` foi populado com as MCs do snapshot, que já são 12/9/6/3). Não é crítico — o caso de uso primário é visualizar proposta como foi enviada, não editar.

## Bug 3 — Card REPASSE ignora fases ativas (FIXADO)

**Sintoma recapitulado:** Item 04 (15B24 10.000 Kg, MP Repasse Importada + TT + 5 certs + CAP) mostrava MC card Repasse negativo. Custo total R$ 60.375, preço de referência calculado só sobre MP (~R$ 8,73/Kg) — indicador enganoso de -1,47% vs Repasse.

**Raiz confirmada:** no bloco `if(mpRepasseOn)` de `simCalc` (`Analise_Precificacao_Sacchelli.html` linha 4549), `repTotalVLiq` aplicava margem apenas sobre a MP repassada:

```js
// ANTES — bug
const repVendaLiqTon=mgMpRep>0&&mgMpRep<100?custoLiq/(1-mgMpRep/100):custoLiq;
const repTotalVLiq=repVendaLiqTon*pesoMPTon;  // só MP, ignora fases
```

`repTotalCusto` já era calculado incluindo fases (via `totalCusto-mpCusto+custoLiq*pesoMPTon`), mas a venda líquida saía desconectada — daí o MC card negativo quando fases > preço MP puro.

**Fix aplicado:**

```js
// DEPOIS — venda líquida aplicada sobre custo TOTAL (inclui fases/certs/CAP)
const repTotalCusto=totalCusto-mpCusto+(custoLiq*pesoMPTon);
const repTotalVLiq=mgMpRep>0&&mgMpRep<100?repTotalCusto/(1-mgMpRep/100):repTotalCusto;
const repVTBruto=despFactor>0?repTotalVLiq/despFactor:repTotalVLiq;
```

**Retrocompat preservada:** sem fases/certs/CAP, `totalCusto==mpCusto`, então `repTotalCusto==custoLiq*pesoMPTon`. Matematicamente idêntico ao cálculo anterior (`custoLiq × pesoMPTon / (1-mgMpRep/100)`). Algebra:

- Sem fases: `repTotalVLiq_novo = custoLiq × pesoMPTon / (1-mc) == repVendaLiqTon × pesoMPTon = repTotalVLiq_antigo` ✓
- Com fases: `repTotalVLiq_novo = (MP + fases + certs + CAP) / (1-mc)` → preço de repasse "honesto" sobe pra cobrir valor agregado, MC card vira positivo e realista.

**Caso numérico (Item 04 do teste, mgMpRep=5% hipotético):**

- Antes: preço ref ~R$ 8,73/Kg → com preço negociado R$ 8,60/Kg → diff -1,47% / MC negativo
- Depois: preço ref ~R$ 9,75/Kg (inclui fases) → com preço negociado R$ 8,60/Kg → diff ~-11,8% / MC card reflete realidade do custo total

Validação numérica exata em produção fica pro próximo teste guiado (passos 5-7 originais).

## Bug 3 v2 — Margens individuais por linha (FIXADO 21/04/2026 tarde 2)

**Sintoma novo descoberto na validação em produção:** depois do fix v1, a MC do card Repasse mostrava `25%` fixo e não reagia à margem configurada no mtl comp (testado com Ensaio Especial 20% → 0%). Preço Repasse também não mudava (ficava R$ 13,11/Kg nos dois cenários). Tabelas Verde/Amarela/Vermelha reagiam normalmente (R$ 104.713 → R$ 101.233).

**Raiz:** v1 aplicava `mgMpRep` sobre o **custo total bruto** (`repTotalCusto / (1-mgMpRep/100)`) — ou seja, ignorava as margens individuais das linhas de fase/cert/CP/mtl comp/CAP. O card Repasse virou "margem única sobre tudo", divergindo da lógica das tabelas V/A/R que agregam margens por linha.

**Alinhamento de produto (Gustavo, 21/04 tarde):** no Repasse, `mgMpRep` deve ser usada APENAS na linha MP, substituindo as margens V/A/R padrão da MP. Demais linhas (fases/certs/CP/CAP/mtl comp) mantêm as margens individuais já configuradas. Isto é: Repasse = tabela Verde com swap só da MP.

**Fix v2 aplicado:**

```js
if(mpRepasseOn){
  const mgMpRep=+(document.getElementById('sim-mg-mp-rep')?.value)||0;
  const mpCustoRep=custoLiq*pesoMPTon;
  // Σ vendas líquidas: MP com mgMpRep + demais linhas com margV individual
  let repTotalVLiq=0;
  items.forEach(it=>{
    if(it.tipo==='mp') repTotalVLiq+=safeDiv(mpCustoRep,mgMpRep);
    else                repTotalVLiq+=safeDiv(it.custo,it.margV);
  });
  const repTotalCusto=totalCusto-mpCusto+mpCustoRep;
  const repVTBruto=despFactor>0?repTotalVLiq/despFactor:repTotalVLiq;
  // ... resto igual
}
```

**MC do card deixa de ser `mgMpRep`** — passa a ser a MC efetiva da operação considerando mgMpRep na MP + margens individuais nas demais linhas. Isto é o comportamento semanticamente correto: mgMpRep é margem desejada sobre a MP, não MC-alvo da operação inteira.

**Validação aritmética (Item 04 do teste, mgMpRep 25%, despFactor 0,652):**

| Cenário | Preço/Kg v1 | MC card v1 | Preço/Kg v2 | MC card v2 |
|---|---|---|---|---|
| Mtl comp margem 20% | R$ 13,11 | 25,00% (fixo) | **R$ 12,68** | **22,48%** |
| Mtl comp margem 0% | R$ 13,11 | 25,00% (fixo) | **R$ 12,34** | **20,29%** |

Preço repasse agora reage à margem do mtl comp (diff R$ 0,34/Kg ao mudar de 20→0). MC card reflete o resultado ponderado real da operação.

**Retrocompat preservada:** item só com MP (sem fases/certs/CAP/mtl comp): `repTotalVLiq = safeDiv(mpCustoRep, mgMpRep)` = custoLiq × pesoMPTon / (1-mgMpRep/100) → preço R$ 8,85/Kg e MC 25% — idêntico ao comportamento pré-Bug 3. Smoke test confirmou.

**MC do Preço Negociado permanece como está.** O MC 16,66% do PN é a MC econômica ponderada sobre custo total (modelo Softcomp). É a margem real da operação. As margens "ocultas" (spreads, margens individuais por linha, etc.) ficam por conta do DRE do pedido — esse é o papel dele. Confirmado por Gustavo: "quero ver a margem ponderada sobre o custo total (modelo Softcomp) e o DRE fazendo o papel dele e identificando as margens ocultas".

**Terminologia precisa de mgMpRep:** é "margem **sugerida**" (ou desejada) sobre a MP — não margem mínima. O vendedor usa o card Repasse como referência de NEGOCIAÇÃO; pode subir ou descer dali. Não é piso.

## Validação técnica (v2)

- **Syntax check HTML:** 1 script inline, 0 erros.
- **Testes motor:** 499/499 verdes (motor não espelha card Repasse).
- **Smoke test aritmético:** `outputs/smoke_test_bug3_v2.js` reproduz Item 04 e confirma valores acima.
- **Validação em produção:** pendente. Reabrir proposta gravada com Item 04 e conferir visualmente: (a) preço Repasse agora muda ao mudar margem do mtl comp/fases; (b) MC card Repasse mostra valor ponderado real (próximo de 22% com margem mtl 20%, e cai pra ~20% quando zera mtl).

## Bug 3 v3 — Repasse alinha cálculo Softcomp (FIXADO 21/04/2026 tarde 3)

**Pedido (Gustavo):** "preço de repasse deve considerar o cálculo do softcomp".

**Diagnóstico:** v2 usava `mpCustoRep = custoLiq × pesoMPTon` (custo cru da MP repasse). Isso bypassava os acréscimos do Softcomp (VPP, acréscimo corte, extra corte, tolerância) que as tabelas V/A/R aplicam via `custoTon_full` / `mpCusto_pc/_m/_kg`. Em modo kg (caso do Item 04), v2 acertou por coincidência — `custoTon_kg = custoLiq` em modo peso. Em modo pc com material não-cortado, v2 subestimaria o preço.

**Insight:** o `custoLiq` global JÁ é substituído pelo da MP repassada lá em cima na cascata (linha 3713: `if(repCustoLiqTon>0) custoLiq = repCustoLiqTon`). Logo todos os intermediários Softcomp (`custoTon`, `custoTon_full`, `custoTon_kg`, `mpCusto_pc/_m/_kg`, `totalCusto_pc/_m/_kg`) já refletem o custo importado nacionalizado COM os acréscimos do modo. O Repasse só precisa usar essas variáveis, em vez de recalcular cru.

**Fix v3:**

```js
if(mpRepasseOn){
  const mgMpRep=+(document.getElementById('sim-mg-mp-rep')?.value)||0;
  // Variantes do modo ativo — mesmas usadas em recalcTotalV pras tabelas V/A/R
  const _mpCusto_modo = sellUnit==='m'?mpCusto_m
                      : sellUnit==='pc'?mpCusto_pc
                      : mpCusto_kg;
  const _cpCusto_modo = sellUnit==='m'?cpMatCusto_m
                      : sellUnit==='pc'?cpMatCusto_pc
                      : cpMatCusto_kg;
  const _custoTon_modo = sellUnit==='kg'?custoTon_kg : custoTon_full;
  // Σ vendas líquidas: paridade com recalcTotalV, mas margem MP = mgMpRep
  let repTotalVLiq=0;
  items.forEach(it=>{
    let c=it.custo;
    let mg=it.margV;
    if(it.tipo==='mp'){c=_mpCusto_modo; mg=mgMpRep;}
    else if(it.tipo==='cp') c=_cpCusto_modo;
    else if(it.tipo==='cert' && typeof it._certPctFactor==='number') c=it._certPctFactor*_custoTon_modo;
    repTotalVLiq += safeDiv(c, mg);
  });
  const repTotalCusto = sellUnit==='m'?totalCusto_m
                      : sellUnit==='pc'?totalCusto_pc
                      : totalCusto_kg;
  // ... resto igual
}
```

**Impacto por modo (smoke test):**

| Cenário | mpCustoRep v2 | mpCustoRep v3 | Δ preço/Kg |
|---|---|---|---|
| Modo Kg (Item 04 do usuário) | R$ 43.297,90 | R$ 43.297,90 | R$ 0,00 (idêntico) |
| Modo Pç + VPP 3% + corte 5% + extra 2% (repasse por ton) | R$ 43.297,90 | R$ 48.860,12 | +R$ 1,14 |
| Modo Pç + Repasse POR PEÇA (vpp=0, acorte=0 forçado) | R$ 43.297,90 | R$ 43.297,90 | R$ 0,00 |

Item 04 do Gustavo (modo Kg) **não muda** em v3 vs v2. v3 é correção de modo Pç com material não-cortado, onde v2 subestimaria. Bonus: certs `pct_custo` agora usam `custoTon_modo` correto (paridade total com `recalcTotalV`).

## UX — clareza do MC do card Repasse (21/04/2026 tarde 3)

`mgMpRep` é margem **sugerida** sobre a MP — não margem mínima. Vendedor usa o card como referência de NEGOCIAÇÃO, pode subir ou descer dali.

Adicionado sufixo discreto no MC do card pra deixar claro:

```
MC: 18,33% · MP sugerida 25%
```

A primeira é a MC efetiva ponderada (resultado real da operação com mgMpRep na MP + demais linhas como custo). A segunda é o input do vendedor — a sugestão.

## Bug 3 v4 — DESCARTADA (interpretação errada)

v4 tratou linhas não-MP como custo puro, invariante às margens. Gustavo reafirmou que o motor deve ser **EXATAMENTE igual das V/A/R**, com swap só da margem da MP por mgMpRep — as outras linhas mantêm margens individuais. Preço reage às margens de componentes (igual Verde/Amarela/Vermelha quando se muda margem de linha). v3 restabelecida como final.

Lição: quando Gustavo disse "margem oculta → DRE", eu interpretei como "tirar a margem da soma do preço"; o que ele quis dizer é que o **MC displayed subindo** é sintoma legítimo da matemática, não causa pra alterar o motor. DRE é quem identifica a composição dessa margem. Motor = V/A/R sem desvio.

## Bug 3 v3 — Repasse: motor idêntico V/A/R (FIXADO 21/04/2026 tarde 4)

**Alinhamento final (Gustavo, 21/04 tarde 4):** "quero o repasse calculando igual as tabelas V/A/R, partindo do custo líquido do aço nacionalizado e margem da matéria-prima de 25%, o restante tem que funcionar igual."

**Motor:** mesmo `recalcTotalV` das V/A/R. Única diferença: a linha MP usa `mgMpRep` em vez de `mcV/A/R`. Demais linhas (fases/certs/CP/CAP/mtl comp) mantêm margens individuais exatamente como nas V/A/R. Como `custoLiq` global já é substituído pela MP repasse (linha 3713), todos os intermediários Softcomp (custoTon_full/kg, mpCusto_pc/m/kg, totalCusto_pc/m/kg) já refletem a MP importada com VPP/acorte/extra corte/tolerância aplicados.

**Código final:**

```js
if(mpRepasseOn){
  const mgMpRep=+(document.getElementById('sim-mg-mp-rep')?.value)||0;
  const _mpCusto_modo = sellUnit==='m'?mpCusto_m
                      : sellUnit==='pc'?mpCusto_pc
                      : mpCusto_kg;
  const _cpCusto_modo = sellUnit==='m'?cpMatCusto_m
                      : sellUnit==='pc'?cpMatCusto_pc
                      : cpMatCusto_kg;
  const _custoTon_modo = sellUnit==='kg'?custoTon_kg : custoTon_full;
  // Mesmo motor do recalcTotalV, swap só da margem MP por mgMpRep
  let repTotalVLiq=0;
  items.forEach(it=>{
    let c=it.custo;
    let mg=it.margV;
    if(it.tipo==='mp'){c=_mpCusto_modo; mg=mgMpRep;}
    else if(it.tipo==='cp') c=_cpCusto_modo;
    else if(it.tipo==='cert' && typeof it._certPctFactor==='number') c=it._certPctFactor*_custoTon_modo;
    repTotalVLiq += safeDiv(c, mg);
  });
  const repTotalCusto = sellUnit==='m'?totalCusto_m
                      : sellUnit==='pc'?totalCusto_pc
                      : totalCusto_kg;
  const repVTBruto = despFactor>0?repTotalVLiq/despFactor:repTotalVLiq;
  // ... resto igual
}
```

**Validação aritmética (smoke test reproduz prints do Gustavo):**

| Cenário | Preço Repasse | MC card |
|---|---|---|
| Item 04, mtl 10%, fases 10%, CAP 10% | **R$ 12,45/Kg** ✓ (bate com print) | **20,75%** ✓ |
| Item 04, mtl 50%, fases 10%, CAP 10% | **R$ 13,69/Kg** ✓ (bate com print) | **27,91%** ✓ |

Preço Repasse reage às margens das linhas — igual Verde/Amarela/Vermelha reage. DRE é quem identifica a composição de margens ocultas (quanto da receita veio de margem da MP vs margens dos componentes).

**O que reage no Repasse (igual V/A/R):**
- custoLiq da MP, peso da MP, mgMpRep
- Margens individuais das linhas (fases/certs/CP/CAP/mtl comp)
- VPP/acorte/extra corte/tolerância via cálculo Softcomp

## Validação técnica (v3 final)

- Syntax check HTML: 0 erros.
- Motor: 499/499 testes verdes.
- Smoke test aritmético: `outputs/smoke_test_bug3_v4.js` confirma valores bit-idênticos aos prints do Gustavo.
- **Validação em produção:** pendente. Reabrir Item 04 e conferir: (a) preço Repasse R$ 12,45 com mtl 10%, R$ 13,69 com mtl 50% — igualzinho antes; (b) mudar qualquer margem de linha move o preço Repasse (por design, igual V/A/R).

## MC do Negociado no modelo Softcomp (FIXADO 21/04/2026 tarde 4)

**Observação do Gustavo:** "o preço negociado não impacta na margem quando altero uma margem de uma fase".

**Racional (Gustavo):** "se o preço negociado calcula com a mesma lógica de precificação do Softcomp, se eu aumentar a margem de um serviço, para o Softcomp estou aumentando o custo de produção, que deveria sim impactar a margem já que tenho um preço de venda fixo. As margens ocultas serão capturadas no DRE."

**Modelo conceitual:**
- **Custo Softcomp** de cada linha = `safeDiv(it.custo, it.margV)` — custo cobrado do cliente no modelo Softcomp (inclui margem alvo do componente).
- **Custo real** de cada linha = `it.custo`.
- **Margem oculta** = custo Softcomp − custo real = margem alvo de cada linha, capturada no DRE como spread.
- **MC do Negociado no card** = `(PN_líq − totalVV_modo) / PN_líq` — ganho efetivo sobre a venda mínima Softcomp (que representa o custo cobrado com todas as margens alvo).

**Antes:** `msvlS = margSVL(valorSug, cardCusto)` = MC econômica sobre custo bruto real. Não reagia às margens de linha (PN fixo + custo real fixo → MC fixa).

**Agora:** `msvlS = margSVL(valorSug, _totalVV_modo)` = MC sobre venda mínima Softcomp. Reage a margens de linha (PN fixo + totalVV cresce com margem → MC cai).

**Validação aritmética (Item 04, PN R$ 13,50/Kg, PN_líq R$ 88.020):**

| Margem Ensaio | MC Negociado antes | MC Negociado agora | Margem oculta (DRE) |
|---|---|---|---|
| 10% | 26,92% (constante) | **24,18%** | R$ 2.409 |
| 50% | 26,92% (constante) | **15,02%** | R$ 10.476 |

A MC econômica (26,92%) continua existindo — é a margem real da operação. No card, a leitura passa a ser "quanto o PN ganha acima do piso Softcomp" (24,18% vs 15,02%). O spread (26,92% − 24,18% = 2,74pp vs 26,92% − 15,02% = 11,90pp) é a margem oculta identificada pelo DRE.

**Trade-off / nuance:**
- Se o vendedor precificar PN abaixo da venda mínima Softcomp, MC do card vira negativa — **alerta visual** de que PN não cobre o custo Softcomp (inclui margens alvo).
- MC contábil (receita_líq − custo_real) continua existindo no DRE — não se perde.
- Coerência: cards V/A/R mostram MC estrutural das margens; card Negociado agora também mostra MC no mesmo modelo.

### REVERTIDO (21/04/2026 tarde 4, pós-produção 3)

**Motivo:** caso real (Item 2 do print Gustavo — 4340 Usinado, PN R$ 75.000/Pç) mostrou resultado absurdo:
- PN bruto R$ 150.000 > Vermelha R$ 149.593 → PN acima do piso
- MC Vermelha: 18,72% · MC Amarela: 21,01% · MC Verde: 23,36%
- Com fórmula `totalVV` como base: MC Negociado = −5,76% (negativo, contradiz PN > Vermelha)

**Motivo do absurdo:** totalVV (Verde) é sempre o mais alto. Se PN está entre Vermelha e Verde, PN_líq < totalVV → MC negativa. Mas semanticamente PN está acima do piso (Vermelha) — MC deveria ser positiva.

**Decisão:** MC do Negociado volta a usar `cardCusto` (fórmula contábil original) — mesma base das tabelas V/A/R. Coerência perfeita:
- PN > Verde → MC Negociado > MC Verde
- PN entre Verde e Amarela → MC entre MC Verde e MC Amarela
- PN entre Amarela e Vermelha → MC entre MC Amarela e MC Vermelha  
- PN < Vermelha → MC < MC Vermelha (eventualmente negativa)

**Item 2 do print, fórmula original:**
`MC = (PN_líq − cardCusto) / PN_líq = (97.800 − 79.277,49) / 97.800 = 18,94%`
Entre MC Vermelha (18,72%) e MC Amarela (21,01%). Coerente.

**Sobre "MC não reage à margem de fase":** é correto matematicamente. PN fixo + cardCusto fixo (margem de linha só muda margV, não it.custo) = MC fixa. A **sensibilidade** às margens de linha aparece naturalmente em dois lugares:
1. **Preços V/A/R reagem** — se margem sobe, Verde/Amarela/Vermelha sobem → PN que estava acima pode passar pra abaixo.
2. **Campo "diff vs VM R$/X"** reflete — se Vermelha passa o PN, diff vira negativo (alerta visual automático).

Se quiser sensibilidade explícita no MC do card, é outra discussão (opções: base dinâmica V/A/VM dependendo da faixa, ou mostrar duas MCs). Por ora, fica a fórmula original + alertas via diff vs VM.

## Validação técnica

- **Syntax check HTML:** 1 script inline, 0 erros (`node syntax_check.js`).
- **Testes motor:** 499/499 verdes. Bug 3 é puramente wrapper-side (card visual), motor não tem espelho do card Repasse — intocado.
- **Validação em produção:** pendente. Rodar passos 5-7 do teste guiado original (Reabrir / Revisar / Mesmo cliente) pra confirmar que Bug 4 eliminou a divergência PDF vs tela reaberta, e conferir visualmente preço/MC no card Repasse com fases ativas.

## Auditoria aberta (mesma classe de bug)

No log da manhã ficou anotada a sugestão de auditar os outros `_chk_*` capturados na linha 9249 — `sim-cert-on`, `sim-min1kg-override`, `sim-mtl-comp-on`, `sim-rep-ratear`. Inspeção rápida:

- `sim-cert-on` — restaurado via linha 9253-9256 (mostra/esconde `sim-cert-fields` direto). Sem handler externo dependente do click. OK.
- `sim-min1kg-override` — afeta só cálculo interno em simCalc, sem side effect visual. OK.
- `sim-mtl-comp-on` — display do `sim-mtl-comp-fields` aplicado linha 9305. OK.
- `sim-rep-ratear` — lido em simCalcImportacao/simCalc via `.checked`. Sem handler de click separado. OK.

Nenhum desses tem um equivalente de `simTogglePonta` (função de toggle com side effects fora da leitura direta do checkbox). Conclusão: auditoria completa — só `sim-ponta-on` estava quebrado.

## Próximos passos

1. **Validar Bug 4 em produção** — reabrir a proposta gravada com ponta ON no teste da tarde, conferir que os valores na tela batem com o PDF. Gustavo.
2. **Validar Bug 3 em produção** — reabrir Item 04 do mesmo pacote, olhar card PREÇO REPASSE: (a) MC não-negativo; (b) % diff vs Repasse agora reflete diferença real. Gustavo.
3. **Passos 5-7 do teste guiado original** — Reabrir / Revisar / Mesmo cliente — retomar agora que os dois bloqueadores estão fixados.
4. **Refinos UX** (task #8 do roadmap Proposta): botão "🔄 Mesmo cliente" oculto até cliente preenchido, campo Reajuste editável nas Condições Comerciais, badge "ignorado — repasse importado" na aba MP quando Importação ativa, label /Kg no PDF mostrar conversão quando unidade venda ≠ unidade compra.

## Aprendizado meta (atualização)

Bug 1 + Bug 4 foram **duas manifestações da mesma classe** (restore sem re-dispatch de handler). Fix do Bug 4 valida a teoria arquitetural: sempre que snapshot restaura um checkbox com side effect externo, o handler precisa ser chamado explicitamente.

Bug 3 foi classe diferente — **bug de fórmula matemática** no bloco do card Repasse, pré-existente desde que o card foi criado. Só ficou visível quando a Proposta Comercial trouxe cenários com fases+repasse pra primeira linha de cenários testados. Lição: card de preço que aplica margem sempre precisa aplicar sobre CUSTO TOTAL, nunca sobre componente isolado — mesmo que intuitivamente pareça "é um card de MP Repasse, margem vai sobre MP". A semântica "MC mínimo sobre MP" só é consistente sem valor agregado; com fases, o certo é "MC mínimo sobre produção".
