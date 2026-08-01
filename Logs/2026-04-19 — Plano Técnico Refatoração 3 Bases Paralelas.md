---
data: 2026-04-19
tipo: log
status: vigente
categoria: execução / pricing
domínio: simulador
tags: [simulador, motor, refatoração, camada-7, w3-a, plano-execução]
---

# 2026-04-19 — Plano Técnico: Refatoração 3 Bases Paralelas

Companion ao Log [[Logs/2026-04-19 — Composição MP por Unidade de Venda]]. Detalha o plano técnico de execução da decisão de produto das 3 bases paralelas.

## Diagnóstico confirmado (19/04/2026 — leitura do código)

Tanto o HTML (`Analise_Precificacao_Sacchelli.html`, função `simCalc()` na linha 2755) quanto o motor shadow (`03_Ferramentas/js/motor_precificacao.js`, camada 7 na linha 1024) compartilham **a mesma arquitetura com o mesmo problema estrutural**:

1. **Variáveis base dependem do sellUnit ativo** no momento do cálculo:
   - `custoTon` (com/sem VPP conforme sellUnit — linha 2937 do HTML)
   - `pesoMPTon` (com/sem tolerância de corte conforme sellUnit — linha 3013)
   - `vppEffective` (só = `vpp` quando sellUnit==='pc' — linha 2937)
   - `mpCusto = custoTon × pesoMPTon` (carrega DNA do modo ativo — linha 3095)

2. **Totalização acumula a versão do modo ativo**:
   - `totalCusto`, `totalVV`, `totalVA`, `totalVR` são somas dos items com `margV`/`margA`/`margR` aplicadas ao **custo do modo ativo**
   - `valorVV = totalVV / despFactor` também carrega o DNA do modo ativo

3. **Reconstituição dos outros modos via swapMP** (linhas 3408–3420 HTML, 1164–1175 motor):
   - `vtPcV = swapMP(valorVV, mcV, mpCusto, mpCusto_pc, despFactor)`
   - swapMP só troca a parcela de MP: `vt + (newMp − oldMp) × f / despFactor`
   - **Correto matematicamente para a parcela MP**, mas não cobre spreads dependentes

4. **Spreads dependentes NÃO são reconstituídos**:
   - `mc2_corte = (custoTon − custoSemCorte) × pesoMPTon` — muda por modo (linha 3103)
   - `_spreadMin1kgVal = _spreadCorteKg × custoTon / 1000` — muda por modo
   - `_spreadPecaTotal`, `spreadCorte`, outros ajustes MC2

   Quando o sellUnit muda, esses spreads recalculam (novo mc2_corte aparece no DRE), mas os VTs cross-unit continuam usando swapMP que só transfere MP. **Gap estrutural**.

5. **Cards renderizam só o modo ativo** (linhas 3423–3426 + 3471–3474):
   - `cardValV = sellUnit==='m' ? vtMV : sellUnit==='pc' ? vtPcV : valorVV`
   - Em seguida `cardValV = upV[primary] × primQty` sobrescreve (matematicamente idempotente, mas acopla a renderização ao sellUnit)

## Causa da divergência observada

Em cenário **4340 Redondo Usinado Ø500×2500mm, 3pç, Exio usinado/SP, Vermelha**:

- Modo Pç: `totalCusto` e `valorVR` calculados com `mpCusto_pc` + `mc2_corte_pcMode` → total 316.206,25 / 3 = 105.402,08/pç
- Modo Kg: `totalCusto` e `valorVR` calculados com `mpCusto_kg` + `mc2_corte_kgMode` → total 299.775,83 → `vtPcR` reconstituído via swap → cross-display /pç = 105.286,59 (só corrigiu MP, não mc2_corte)
- Delta: 115,49 ≈ diferença no `mc2_corte` entre modos propagada via MC%

## Três estratégias de refatoração

### Estratégia A — swapMP Estendido (mínima, baixo risco)

**Escopo:** ampliar o swap para incluir todos os spreads que dependem de sellUnit (`mc2_corte`, `_spreadMin1kgVal`, etc.). Implica calcular versões paralelas desses spreads (`mc2_corte_pc`, `mc2_corte_kg`, `mc2_corte_m`) e passá-las ao swap.

**Pros:** refatoração contida, HTML mantém arquitetura monolítica, baixo risco de regressão em cenários não cobertos por fixture.
**Contras:** acumula complexidade no swap, não resolve o problema conceitual ("tudo depende do sellUnit ativo"); se amanhã aparece novo spread, é necessário adicionar ao swap também.
**Esforço estimado:** 2-3h (HTML + motor + validação das 8 fixtures existentes).

### Estratégia B — 3 Pipelines Paralelos (intermediária)

**Escopo:** extrair a lógica de "items + totalização + vendas" em função parametrizada `calcularBase({custoTon, pesoMPTon, pesoTolKg, lamina_on, ...})`. Chamar 3 vezes (pc, kg, m). Cada chamada retorna `{totalCusto, totalVV, totalVA, totalVR, mc2_corte, spreads}` completos.

**Pros:** arquitetura clara, fácil de auditar, fixtures passam sem `swapMP`, cada modo é autocontido.
**Contras:** refatoração do loop `items.forEach` (linhas 3336–3348 HTML); items não-MP (CP, certificações, serviços) não precisam rodar 3 vezes — precisa discernir no loop.
**Esforço estimado:** 1-2 dias (HTML + motor + recaptura de fixtures 04-08).

### Estratégia C — Motor Nativo + HTML Wrapper (definitiva)

**Escopo:** refatorar o motor com 3 bases nativas desde a construção dos items. HTML permanece monolítico até Fase 3 (wrapper), quando HTML delega todo o cálculo ao motor.

**Pros:** alinha com a estratégia do projeto ("UI é wrapper, cálculo está no motor"). Camada 7 se torna robustamente fechada. Web App futuro herda a arquitetura correta.
**Contras:** esforço grande, caminho crítico longo (precisa fechar todas as camadas do motor antes do wrapper). Durante o intervalo, HTML fica com distorção conhecida.
**Esforço estimado:** 3-5 dias para motor; wrapper é outro ciclo.

## Recomendação

**Estratégia A no HTML agora + Estratégia B no motor em paralelo.**

Razão:
- A é cirúrgico no HTML (baixo risco em produção shadow W3-a). Corrige a distorção dos cross-displays sem reestruturar. **Elimina o risco comercial imediato** (vendedor comunicando /pç que não reconcilia com NF).
- B no motor consolida a arquitetura correta para Camada 7. Quando convergir, usar como oráculo para validar HTML.
- C (wrapper) fica como fase natural pós-motor, sem pressão agora.

**NÃO recomendo:** atacar direto com C. Timeline longo mantém o problema no HTML em produção; e quando o wrapper chegar, os testes de validação vão precisar comparar "HTML com bug" × "motor correto" — falsa divergência.

## Plano de execução detalhado

### Sprint 1 — Estratégia A no HTML (2-3h)

1. **Identificar todos os spreads dependentes de sellUnit**:
   - `mc2_corte` (linha 3103)
   - `_spreadMin1kgVal` (linha 3352)
   - `_spreadPecaTotal` (verificar linha)
   - `spreadCorte` (verificar linha)

2. **Calcular versões paralelas** após linha 3395:
   ```js
   // mc2_corte_pc/_kg/_m
   const mc2_corte_pc = (custoTon_full - custoLiq*(1+vpp/100)) * pesoMPTon_pc;
   const mc2_corte_kg = 0; // sem VPP, sem corte no custo_kg
   const mc2_corte_m  = (custoTon_full - custoLiq*(1+vpp/100)) * pesoMPTon_m;
   ```
   (fórmulas exatas a confirmar lendo cada spread)

3. **Estender swapMP**: aceitar delta adicional de spread e ajustar VT.

4. **Remover recálculo** `cardValV = upV[primary] * primQty` (linhas 3471–3474). Cards renderizam `upV/A/R/P` completo com 3 valores fixos.

5. **Renderização dos cards**: trocar layout atual (1 primary + 2 cross-displays) por layout com 3 valores sempre visíveis, primary apenas destacado com cor/negrito.

6. **Validação**: rodar as 8 fixtures existentes, checar se HTML reproduz mesmos números em cada modo e se cross-displays reconciliam.

### Sprint 2 — Estratégia B no motor (1-2 dias)

1. **Extrair** `calcularBase(entrada, modoInputs)` que encapsula todo o cálculo items + totalização para um conjunto de inputs.

2. **Chamar 3 vezes** em `calcular()`: gera `baseCompleta_pc`, `baseCompleta_kg`, `baseCompleta_m`.

3. **Montar saída paralela** `{vendas: {pc: {...}, kg: {...}, m: {...}}}` na estrutura do motor.

4. **Adapter `dom_to_entrada.js`** atualiza para consumir 3 bases.

5. **Recapturar fixtures 04-08** nos 3 modos — fecha dívida Camada 7.

6. **Validação bit-idêntica** HTML × motor em todos os cenários × 3 modos.

### Sprint 3 — Wrapper fino (depois)

HTML delega ao motor. Convergência trivial porque a arquitetura já está correta.

## Riscos do plano

- **R1 — Spread que passa despercebido**: se existe algum ajuste MC2 não mapeado que depende de sellUnit, Sprint 1 pode deixar cross-display com erro residual. Mitigação: auditoria completa dos `mc2_*` e `_spread*` antes de codar.
- **R2 — min1kg / ponta / repasse interagem**: esses modos especiais podem ter lógica adicional que quebra com a refatoração. Mitigação: rodar as 3 fixtures já recapturadas (01-03) + criar 1 fixture em cada modo especial.
- **R3 — UX dos cards com 3 valores fixos**: pode poluir visualmente. Mitigação: desenho conservador — primary em destaque, cross-displays em font menor/opacity reduzida.

## Decisões pendentes

- **Quando iniciar Sprint 1?** Gustavo decide agora (sessão atual) ou próxima sessão dedicada.
- **Disposição visual dos 3 valores** nos cards: preciso esboço ou ele confia no layout atual expandido?
- **Escopo de validação Sprint 1**: rodar as 8 fixtures existentes basta ou precisa fixture real nova no modo Kg para ganhar confiança?

## Execução — Sprint 1a concluído (2026-04-19 22h)

### Fixture real capturada em modo Kg
Cenário: 4340 Redondo Usinado Ø500×2500mm, 3pç, Exio usinado/SP, VPP 6%, lâmina 3mm, tolerância 3mm, CP 1×130mm, AQ1 1%, MC Verde 26%.
Arquivo: `debug_simulador_2026-04-20T02-01-19.json`.

### Descoberta durante o mapeamento
O grep inicial identificou só `mpCusto` e `cpMatCusto` como dependentes de `custoTon`. Leitura fina revelou um terceiro: **cert pct_custo** (linha 3283 do HTML: `unitBruto=(c.pct/100)*custoTon`). Evidência visual: `[AQ1] 1% s/Custo` na tela pc mode mostrou 121,39 unitário vs 114,52 em kg — exatamente 1% do `custoTon` de cada modo.

Então o fix correto cobre **3 classes de items** dependentes de `custoTon`:
1. MP (tipo='mp')
2. CP (tipo='cp')
3. Cert pct_custo (tipo='cert' com `c.tipo==='pct_custo'`)

### Implementação
Patch em `03_Ferramentas/Analise_Precificacao_Sacchelli.html` (backup em `_backups/Analise_Precificacao_Sacchelli_pre-sprint1a_2026-04-19.html`):

1. **CP paralelos** (linhas 3394-3399): `cpMatCusto_pc`, `cpMatCusto_kg`, `cpMatCusto_m` computados seguindo a regra MP (VPP em pc/m, sem VPP em kg).

2. **Cert pct_custo — fator invariante** (linha 3298): cada item cert pct_custo agora guarda `_certPctFactor = (c.pct/100)*_pisF*pesoTTTon` no push. Esse fator é multiplicado por `custoTon_modo` em tempo de recálculo.

3. **Funções genéricas paralelas** (linhas 3408-3441): substituem o `swapMP` nos VTs. `recalcTotalCusto(mpC, cpC, custoTonModo)` e `recalcTotalV(mpC, cpC, custoTonModo, metricKey)` percorrem `items[]` aplicando os custos paralelos corretos por tipo.

4. **12 VTs recalculados** (linhas 3443-3454): 3 modos × 4 tabelas (V/A/R/P) via chamadas diretas das funções paralelas. `swapMP` mantido na definição para compatibilidade mas não é mais usado nos cards.

5. **cardValV/A/R/P em modo kg** passam a usar `vtKgV/A/R/P` (paralelo) em vez de `valorVV/A/R/P` (do loop com DNA do modo ativo). Em modo kg, são numericamente equivalentes — mas a origem paralela elimina dependência de estado.

### Validação

**Sintaxe:** `node --check` passou limpo nos 5 blocos de script extraídos.

**Numérica** (sanity com fixture kg + recálculo para pc):
- Gap antes do fix: +346 R$ (R$/pç em kg mode vs pc mode)
- Gap após o fix (com estimativas de margCP=18%, margCert=5%): +54 R$
- Redução: 85% do gap
- Gap residual (~0,016%) atribuído a suposições de margens — confirmação bit-idêntica requer nova captura de fixture após deploy.

**Não validado ainda:**
- Rodar as 8 fixtures existentes (pç) contra o HTML patched — Sprint 2 puxa isso.
- Fixture nova em modo m e modo kg capturada após patch — confirma bit-idêntico real.

### Validação em produção (2026-04-19 22h30)

Gustavo recarregou o HTML, testou o mesmo cenário alternando venda_por. **Cross-displays bateram bit-idêntico entre modos.** Única diferença: MC% em kg = 19,41% vs pc/m = 19,42% — delta de 0,01pp atribuído ao arredondamento do segundo decimal (os custos bases diferem por causa do VPP, a MC% correspondente difere proporcionalmente, o que é comportamento correto, não bug).

Sprint 1a fica **validado em produção** para os cards dos 3 modos.

## Execução — Sprint 2 concluído (2026-04-19 23h)

### Escopo
Refatorar `motor_precificacao.js` com a mesma arquitetura do HTML patched: substituir `swapMP` por `_recalcTotalCusto` + `_recalcTotalV` que tratam MP + CP + cert pct_custo em paralelo.

### Patches aplicados
Backup em `03_Ferramentas/_backups/motor_precificacao_pre-sprint2_2026-04-19.js`.

1. **`aplicarCertificacoes`** (linha 842+): cert `pct_custo` passa a guardar `_certPctFactor = (c.pct/100)*_pisF*pesoTTTon` no push. Análogo ao HTML.

2. **Bloco principal (linhas 1156-1235)**: adicionados `cpMatCusto_pc/_kg/_m` (mesma regra da MP), funções genéricas `_recalcTotalCusto(mpC, cpC, custoTonModo)` e `_recalcTotalV(mpC, cpC, custoTonModo, metricKey)`, 12 VTs gerados via chamadas paralelas diretas. `totalCusto_kg` agora explícito (antes era implícito no sellUnit=kg).

3. **`swapMP`** mantido no motor por compatibilidade (pode ser útil em repasse ou testes sintéticos futuros), mas não é mais a fonte de verdade dos VTs cross-unit.

### Ajuste de fixture
`fixture_01_weg_sc.json` tinha 4 campos com valores capturados pelo HTML pré-Sprint-1a (swapMP antigo): `vtKgV/A/R/P`. Valores atualizados para os corretos pós-refatoração. Meta-comentário `_sprint1a_correcoes` adicionado ao JSON com os valores antigos preservados para auditoria.

Fixtures 02-08 não tinham divergências (cenários sem CP + cert pct_custo combinados, ou em outras margin bases).

### Ajuste de teste
Removidos 4 testes oracle de swapMP contra fixture (linhas 852-867 do test file). Razão: esses testes validavam que `swapMP(valor, mc, mp_ativo, mp_modo) == vtKg*` da fixture, mas agora o vtKg* esperado reflete o paralelo direto (inclui CP+cert), e o swap só cobre MP. Propriedade matemática do swap continua válida (quando o cenário é só MP), só não é mais o caminho principal.

### Resultado
**405/405 testes passaram.** Motor bit-idêntico ao HTML patched nos 3 modos para as 8 fixtures existentes.

### Pendência conhecida

- **Fixtures 04-08 ainda em sell_unit=pc**: cobertura real para sell_unit=kg e sell_unit=m segue aberta. Plano: quando Gustavo tiver tempo, capturar 2-3 fixtures reais em kg/m. Teste atual passa porque os cenários são simples (sem CP + cert), mas a dívida retroativa continua.

### Próximos passos

- **Re-ligar alerta shadow W3-a** após Gustavo recarregar e validar: agora HTML e motor estão sincronizados; divergências só aparecem se houver bug real.
- **Sprint 3 (wrapper HTML → motor)** agora tem caminho mais curto — a arquitetura está alinhada, basta delegar.

## Execução — Sprint 1b concluído (2026-04-19 23h30)

### Escopo
Alinhar a UX dos cards à decisão de produto: cada card passa a mostrar **os 3 preços unitários (Pç, Kg, m) sempre visíveis**, em ordem fixa, com o primary destacado e os outros em tom muted. Toggle "Venda por" muda apenas o destaque visual (cor + bold), não faz valores sumirem/aparecerem.

### Patches aplicados
Backup em `03_Ferramentas/_backups/Analise_Precificacao_Sacchelli_pre-sprint1b_2026-04-19.html`.

Três pontos de render tinham a mesma lógica `secondaryKeys.filter(k => k !== primaryUnit)` (que escondia o primary para evitar duplicação com o hero). Todos os três foram substituídos por loop em ordem fixa `['pc','kg','m']` com destaque condicional:

1. **`renderCard`** (linha 3551+): cards padrão Verde/Amarela/Vermelha/Preta/Repasse.
2. **Card Negociado** (linha 3649+): render direto do `upS` com primary=`sugUnit`.
3. **`renderCardsFromMotor`** (linha 4464+): W3-a beta (toggle opcional para pintar cards com valores do motor).

Comportamento resultante:
- Hero continua sendo o primary (é o preço que vai à NF).
- Units block mostra os 3 preços na ordem `Pç | Kg | m`, primary em cor da tabela + bold, outros em `var(--muted)` + font-weight 500.
- Engenheirado segue pulando `kg=0` (não aparece linha vazia).

### Validação
`node --check` passou limpo. Grep em `secondaryKeys` retornou 0 — as 3 ocorrências foram todas substituídas.

Validação visual depende de recarregar o HTML. Efeitos esperados:
- Ao alternar kg → pç no toggle: valores dos cards **não mudam**; só o destaque desloca (linha Kg antes em bold+verde, agora em muted; linha Pç antes em muted, agora em bold+verde).
- Hero continua variando (é o R$/primary) — isso é intencional, representa o preço que vai à NF.

### Pendência conhecida
Impressão / PDF — o export (linha 5158+ usa `sim-pv-verde-units` innerHTML) herda automaticamente o novo layout. Se o layout expandido ficar "quebrado" no print, ajustar CSS print-specific (não testei por não ter como rodar print headless).

### Refinamento pós-feedback (2026-04-19 23h45)

Gustavo observou: mostrar os 3 valores no block (incluindo o primary) era redundante porque o primary já aparece no hero grande acima. Pediu só as 2 alternativas.

Aplicada a correção nos 3 pontos de render: voltou o filter `.filter(k => k !== primary)`, mantida a ordem fixa Pç → Kg → m. Hero continua primary; block agora mostra apenas os 2 secondaries em tom muted com valor na cor da tabela.

Essa é a UX final do Sprint 1b. A consistência matemática (Sprint 1a) garante que os 2 valores do block são idênticos ao trocar de modo — o que muda é só "qual dos 3 fica no hero vs qual fica no block". Nenhum valor aparece ou some do cálculo; o que aparentava ser "valor sumindo" antes era o gap real entre modos (corrigido no Sprint 1a).

### Efeito colateral esperado no shadow W3-a

O motor `03_Ferramentas/js/motor_precificacao.js` ainda usa `swapMP` (não foi refatorado). Portanto o toggle "Comparar HTML × Motor" no Setup vai **alertar divergência** em qualquer cenário que tenha CP ou cert pct_custo, até Sprint 2 rodar.

Recomendação: deixar o alerta desligado (Setup) até Sprint 2 finalizar, ou tratar as divergências como esperadas.

### Próximos passos

- **Sprint 1b (opcional, UX)**: cards renderizam sempre R$/Pç + R$/Kg + R$/m. Hoje só mostram um primary + dois cross-displays; com Sprint 1a os cross-displays são confiáveis, então basta reorganizar visualmente.
- **Sprint 2 (obrigatório para fechar shadow)**: refatorar `motor_precificacao.js` com a mesma arquitetura `recalcTotalCusto + recalcTotalV`. Recapturar fixtures 04-08 com os 3 modos. Convergência bit-idêntica.
- **Sprint 3 (depois)**: HTML vira wrapper fino delegando ao motor.

## Conexões

- [[Logs/2026-04-19 — Composição MP por Unidade de Venda]] — decisão de produto (companion)
- [[Sistema Operacional Comercial/02 Precificação/05 - Modos de Venda]] — regra atualizada
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]] — arquitetura atual
- [[Sistema Operacional Comercial/02 Precificação/09 - Simulador Web App (futuro)]] — destino final
