# 2026-04-17 — Plano Fases 1+3 Simulador de Precificação

**Status:** proposta técnica (não executado)
**Decisão de escopo:** Fases 1 e 3. Fase 2 (UX de pré-preenchimento) cortada — uso pessoal, vendedor experiente.
**Arquivo-alvo:** `03_Ferramentas/Analise_Precificacao_Sacchelli.html`
**Contexto estratégico:** construir instrumento pessoal, portátil caso transição MetalM ([[2026-04-17 — Plano de transição AFS-MetalM (Cenário F)]]).

---

## Revisão da recomendação inicial

Propus extrair a lógica de cálculo pra Python. **Revisado após mapeamento do código.**

**Mapa real do simulador (7.782 linhas, 741 KB, 176 funções JS):**
- `simCalc()` é monolítica — ~1.300 linhas orquestrando leitura DOM, cálculo de 4 tabelas em paralelo (Verde/Amarela/Vermelha/Preta), validações visuais, escrita DOM.
- Funções de cálculo **não são puras** — leem `document.getElementById(...).value` ~80-100x, escrevem `innerHTML`, bordas amarelas de warning, sticky bar.
- Estado disperso em 7 chaves de localStorage, globals mutáveis (`simPhases`, `_pontaOrigMC`, `_manualBitolaPartida`).
- Tabelas hardcoded e customizáveis via Setup convivem (defaults embedded + overrides persistidos).
- Modo Pacote implementado parcialmente (~600 linhas, snapshot/restore funcional, DRE blended no consolidado).
- Família canônica **não formalizada** — usa "Tabela Família AFS" customizada via upload.

**Conclusão:** portar pra Python como Fase 1 é projeto de 8-12 sessões. Risco alto, orquestração browser↔Python não trivial. Rewrite em framework moderno (React + API) é 20+ sessões — fora de escopo agora.

**Fase 1 redefinida: refatoração JS interna** — isolar o núcleo de cálculo do DOM, sem trocar de linguagem. Base limpa pra Fase 3 sem reescrita massiva. Python fica como Fase 4 opcional se virar web app de fato.

---

## Fase 1 — Núcleo de cálculo isolado (JS puro)

### Objetivo

Transformar `simCalc()` monolítica em pipeline de funções puras `dados_entrada → resultado_calculado`, sem acesso direto ao DOM. O HTML continua sendo a UI, mas delega cálculo ao módulo.

### Escopo concreto

1. **Extrair schema de entrada.** Todos os inputs de DOM que `simCalc` lê viram um objeto JavaScript tipado:
   ```js
   const entrada = {
     material: { liga, perfil, bitola, comp_mm, di2, proc },
     quantidade: { qty, unidade },
     custo: { liquido_kg, frete },
     mp_repasse: { ativo, nf, peso, custo_liq_ton, unidade },
     servicos: { tt: [...], td: [...], usx: [...], cert: [...], emb: [...] },
     fiscal: { uf_cliente, uf_fat, icms_pct, icms_auto },
     tabelas_mc: { verde, amarela, vermelha, preta },
     vpp: { auto, manual_pct },
     acorte: { ativo, pct },
     corte: { comp_nominal, extra_tabela },
     ponta: {...}
   };
   ```

2. **Extrair núcleo de cálculo como módulo JS puro.** Novo arquivo `03_Ferramentas/js/motor_precificacao.js` (ou inline namespaced `window.MotorPrec = {...}`). Funções extraídas:
   - `calcular(entrada, config) → resultado` (função raiz)
   - `calcPesoLinear(perfil, bitola, di2)` (já isolada, L.2391)
   - `calcDESP(entrada, config)` (hoje em `simCalcDESP` L.2440)
   - `calcCorte(comp_mm, acab_mp, extras)` (hoje em `getExtraCorte` L.5992)
   - `calcICMS(uf_cliente, uf_fat, proc, acab)` (hoje em `simAutoICMS` L.2237)
   - `calcVPP(entrada, config)` (hoje em `simAutoVPP` L.2017)
   - `calcMP_Repasse(entrada)` (hoje em `simCalcRepasse` L.2568)
   - `calcMargSVL(valor_venda, custo_base)` (hoje aninhada dentro de simCalc L.3361)
   - `calcSwapMP(vt, mc, old_mp, new_mp)` (hoje aninhada L.3333)

3. **Schema de resultado estruturado.**
   ```js
   const resultado = {
     cards: {
       verde: { preco_kg, preco_pc, preco_m, preco_total_modo, mc_nominal, mc_svl, warnings:[] },
       amarela: {...}, vermelha: {...}, preta: {...}
     },
     diagnostico: {
       peso_teorico, peso_bruto, perda_corte_pct, desp_pct, icms_pct,
       mp_repasse_ativo, vpp_aplicado_pct, acorte_aplicado_pct
     },
     dre: { mp_aco, desp_operacional, margem_bruta_rs, margem_svl_rs, ... },
     validacoes: [ { campo, severidade, mensagem } ]
   };
   ```

4. **UI vira thin wrapper.** `simCalc()` HTML passa a ser:
   ```js
   function simCalc() {
     const entrada = lerDOM();
     const config = carregarConfig();  // tabelas AFS
     const resultado = MotorPrec.calcular(entrada, config);
     renderizarCards(resultado.cards);
     renderizarStickyBar(resultado);
     aplicarValidacoes(resultado.validacoes);
   }
   ```

5. **Configuração AFS em arquivo separado.** `config/parametros_afs.json`:
   ```json
   {
     "tabelas_mc_default": { "verde": 20, "amarela": 15, "vermelha": 10, "preta": 5 },
     "extras_corte_default": [...],
     "fases_industriais": { "tt": [...], "td": [...], ... },
     "regras_icms": [...],
     "tolerancias": { "laminado": [...], "forjado": [...] }
   }
   ```
   No dia MetalM: cria `parametros_metalm.json` e troca o import.

6. **Suite de testes.** Critério de sucesso da Fase 1 = bateria de ~30 casos conhecidos onde o output do motor refatorado bate exatamente com o simCalc original. Sem regressão = ok.

### Armadilhas mapeadas

1. **Funções aninhadas em simCalc** (`swapMP`, `margSVL`, `ceil2`, formatters) — precisam ser promovidas pra escopo do módulo antes de extrair.
2. **4 tabelas paralelas (V/A/R/P)** — hoje variáveis sufixadas `vtPcV/A/R/P`. Generalizar como array ou map, passar como parâmetro.
3. **VPP e acorte têm regras condicionais** — MP Repasse zera VPP; repasse por Pç zera acorte. Modelar como pre-condições no schema, não como if espalhado.
4. **Preço sugerido** (`simParseSug`, `simPrecoSugChanged`) — faz cálculo INVERSO (preço dado → MC derivada). Precisa ser função separada `calcularInverso(preco_desejado, entrada) → mc_derivada`.
5. **Recursão em simUnitChange** (chama simCalc em loop) — verificar que refatoração não quebra.
6. **Validações visuais (bordas amarelas)** — separar `validar(entrada) → [warnings]` de `renderizar_warnings(warnings)`.

### Custo estimado

**4-6 sessões de dev**, assumindo:
- Sessão 1: extração de schemas (entrada/saída/config) + suite de testes a partir de cases atuais
- Sessão 2: extração de peso, DESP, corte, ICMS (funções mais simples)
- Sessão 3: extração do núcleo de MC/VPP/acorte/MP_repasse
- Sessão 4: extração do cálculo inverso (preço sugerido)
- Sessão 5: regressão contra HTML original + fix de diffs
- Sessão 6: documentação + cleanup + persistência via config JSON

### Entregáveis

- `03_Ferramentas/js/motor_precificacao.js` — módulo puro
- `03_Ferramentas/config/parametros_afs.json` — configuração AFS
- `03_Ferramentas/js/motor_precificacao.test.js` — suite de regressão
- HTML refatorado — simCalc vira wrapper de 20-30 linhas
- README técnico com contrato de entrada/saída

### Valor entregue mesmo sem Fase 3

- **Base testável**: qualquer bug futuro reproduzível com caso isolado
- **Portabilidade preparada**: se virar MetalM, troca arquivo de config
- **Legibilidade**: novo dev (ou você daqui a 6 meses) entende o cálculo sem ler 1.300 linhas entrelaçadas com DOM
- **Modo Pacote simplificado**: blended do pacote consome o motor N vezes com entradas diferentes, consolida

---

## Fase 3 — Inteligência de preço com histórico

### Objetivo

No momento do orçamento, o simulador mostra automaticamente 4 sinais históricos pra cliente+família:
1. Preço médio praticado (RAF, últimos 6m)
2. MC% mediana realizada (RAF)
3. Preço médio de cotações **ganhas** (últimos 6m)
4. Preço médio de cotações **perdidas por preço** + concorrente ganhador (últimos 6m)

Isso transforma decisão de preço de "intuição" em "instrumento".

### Pré-requisitos

- **Fase 1 concluída** — o motor precisa aceitar contexto histórico como entrada adicional
- **Família canônica consolidada** — chave de matching `Aço|Acabamento|Faixa` já existe no Motor Analítico e nos painéis Estoque/Comercial. Simulador hoje usa "Tabela Família AFS" customizada — **precisa migrar pra família canônica** ou criar mapeamento bidirecional
- **RAF rodando regularmente** — com aba `R4_MC_MatPartida` + cruzamento cliente por família
- **Cotações processadas** com status limpo e motivos de perda categorizados (hoje no motor existe, aba de cotações com zumbi tratado)

### Escopo concreto

1. **Camada de dados histórica.** Novo módulo `js/historico_loader.js`:
   - Consome dois XLSX pré-injetados no HTML (mesma mecânica dos outros painéis):
     - `analitica_raf_*.xlsx` → tabelas `Cliente×Familia` e `Familia_Corredor`
     - `analitica_cotacoes_*.xlsx` → tabelas `Cotacoes_Ganhas` e `Cotacoes_Perdidas_Preco`
   - Builda 2 índices em memória:
     - `historicoRAF[chaveCanonica][cnpj] = { preco_medio, mc_mediana, volume_ton, ultima_nf }`
     - `historicoCotacoes[chaveCanonica][cnpj] = { ganhas: [...], perdidas_preco: [...] }`

2. **Classificação automática de família.** Quando usuário preenche liga+perfil+acabamento+bitola, simulador calcula a família canônica (reaproveitar função `familia_canonica()` do motor Python em JS, ou duplicar lógica).

3. **Lookup contextual no simulador.** Quando cliente+família ficam populados, `historico_loader.buscar(chave, cnpj) → contexto` retorna:
   ```js
   {
     raf: {
       preco_medio_kg, mc_realizada_pct, volume_6m_ton,
       ultima_compra: { data, preco_kg, mc_pct, peso_kg },
       n_transacoes: 12
     },
     cotacoes: {
       ganhas_recentes: [ {data, preco_kg, peso_ton}, ... ],
       perdidas_preco: [
         { data, preco_oferecido_kg, concorrente, preco_concorrente_kg, peso_ton },
         ...
       ]
     },
     corredor_familia: {
       mc_p10, mc_p25, mc_mediana, mc_p75, mc_p90,
       preco_kg_mediano, preco_kg_p90
     }
   }
   ```

4. **Painel lateral de inteligência.** Novo bloco UI ao lado dos 4 cards de preço:
   - **Cliente X Família (histórico):** preço médio praticado, MC realizada, volume 6m
   - **Última compra:** data + preço + MC (âncora de referência)
   - **Cotações ganhas recentes:** últimas 3 com preço e concorrência ausente
   - **Cotações perdidas por preço:** últimas 3 com preço do concorrente (CRÍTICO)
   - **Corredor de MC da família:** barra horizontal com P10-P25-P50-P75-P90, marca onde seu preço proposto cai
   - **Alerta visual:** borda vermelha se preço proposto < P25 ou > P90 do corredor

5. **Mitigação do risco "piso virar teto".** Três salvaguardas explícitas:
   - Label da "última compra" inclui MC realizada. Se foi MC=8%, sinalizar vermelho "compra anterior com margem ruim — não repetir"
   - Mostrar o custo de servir do cliente (do RAF) junto com preço médio. Cliente com custo alto e preço baixo = alerta de prejuízo
   - **Sinal primário é o teto (cotação perdida), não o histórico.** Layout prioriza "perdeu por X" acima de "vendeu por Y"

6. **Mitigação do risco "matching falho".** Fallback em cascata:
   - Chave ideal: `cliente_cnpj + familia_canonica`
   - Fallback 1: `grupo_economico + familia_canonica` (se cliente novo mas grupo conhecido)
   - Fallback 2: `familia_canonica` (mercado geral, não o cliente)
   - Sempre mostrar qual fallback foi usado ("Sem histórico desse cliente — mostrando mercado geral")

### Armadilhas específicas

1. **Volume de dados no HTML.** RAF tem ~84 famílias, mas cruzamento por cliente pode gerar índice de 50-100 mil entradas. Pré-computar no Motor Analítico (Python) e gerar XLSX/JSON enxutos específicos pro simulador.
2. **Privacidade de dados.** Simulador vai expor preços de concorrentes, nomes de clientes. Ok pra uso pessoal. Se um dia virar ferramenta compartilhada, precisa filtragem por usuário.
3. **Frescor dos dados.** Se RAF tem 30 dias, alguns clientes podem ter comprado e não aparecer. Sempre mostrar data do último ciclo processado.
4. **Categorização "perdida por preço".** Depende de qualidade do campo `motivo_perda` no Softcomp. Se vendedor marca errado, sinal é ruim. Vale um relatório de qualidade antes de confiar.

### Custo estimado

**6-8 sessões**, assumindo Fase 1 pronta:
- Sessão 1: definir schemas de índice RAF + Cotações, extrair do Motor
- Sessão 2: loader JS + índices em memória + fallback matching
- Sessão 3: classificação automática de família canônica (migrar do motor Python)
- Sessão 4-5: UI do painel lateral (cards, corredor MC, alertas)
- Sessão 6: integração com Fase 1 (motor aceita `contexto_historico` e pondera alertas)
- Sessão 7-8: QA + ajustes visuais + salvaguardas "piso virar teto"

### Entregáveis

- `js/historico_loader.js` — loader + índices
- `js/familia_classifier.js` — mapeamento liga+perfil+acab+bitola → chave canônica
- Painel lateral HTML + CSS
- Extensão do motor (Fase 1) aceitando `contexto` e gerando alertas
- Extensões no Motor Analítico (Python) gerando XLSX específico pro simulador: `analitica_simulador_contexto_*.xlsx`

---

## Considerações transversais

### Ownership / portabilidade MetalM

- **Motor** (Fase 1) fica limpo. Configurações AFS em arquivo separado. Portar = trocar config.
- **Inteligência histórica** (Fase 3) é específica AFS porque bases são do ERP Softcomp. Na MetalM, terão novo ERP ou trading data — lógica se preserva, conexão de dados muda.
- **Se construir em horário pessoal, em máquina pessoal, com dados sanitizados**: ownership pessoal inequívoco. Construir em horário AFS com dados AFS gera ambiguidade legal — verificar com [[Filtros Estratégicos]].

### Decisão de ritmo

**Fase 1 pode começar a qualquer momento** — não depende do processo Duferco-Brasil. Ganho de organização independente do cenário.

**Fase 3 é mais sensível ao timing.** Se Cenário F (transição MetalM) se confirmar, Fase 3 vira investimento na AFS que depois migra parcialmente. Se Cenário B (MetalM greenfield), Fase 3 na AFS é desperdício — melhor esperar e fazer já no ERP novo.

**Recomendação de ritmo:**
- Fase 1 agora (valor estrutural garantido em qualquer cenário)
- Fase 3 congelada até decisão Duferco-Brasil consolidar (final abril/2026)
- Após decisão, revisar: se Cenário F, executa Fase 3 na AFS com consciência de migração; se Cenário B, adia Fase 3 e faz direto no novo ambiente

### Alternativa a considerar

Se após Fase 1 você perceber que o uso real é raro (não orçamenta todo dia), Fase 3 pode ser overkill. **Alternativa enxuta**: 1 relatório semanal gerado pelo Motor Analítico com "top 20 famílias mais cotadas + top 20 clientes + alertas de preços perdidos" — você lê antes da semana, decora mentalmente, e orçamenta. Custo: 1 sessão. Valor: 70% do que a Fase 3 entregaria, com 10% do custo.

Vale revisar isso após rodar Fase 1.

---

## Próximos passos concretos

- [ ] Decidir: executa Fase 1 agora, ou congela até janela Duferco-Brasil fechar?
- [ ] Se sim: sessão 1 é "extrair schemas + suite de testes" — começar lendo `simCalc` linha a linha, rodando casos conhecidos e capturando input/output em JSON
- [ ] Confirmar construção em horário/máquina pessoal (proteger ownership)
- [ ] Definir critério de "sucesso Fase 1" objetivo — sugerido: 30 casos de regressão com output idêntico ao HTML original

---

## Perguntas que ainda precisam ser respondidas

1. **Qual o volume real de uso do simulador hoje?** Se orçamenta 2x/mês, investir 6 sessões é overkill. Se orçamenta 20x/semana, paga.
2. **O "preço sugerido" (cálculo inverso) é usado?** Se sim, Fase 1 precisa tratá-lo como caminho principal, não secundário.
3. **Quantas famílias canônicas diferentes são orçadas no dia a dia?** Se 90% do volume está em 10 famílias, Fase 3 pode focar nessas e ignorar o resto.
4. **Cotações perdidas por preço têm concorrente identificado em quantos % dos casos?** Se 20%, sinal ruidoso; se 80%, sinal forte.

---

## Conexões

- Decisão de arquitetura do Motor Analítico: [[Sistema Operacional Comercial/01 Sistema de Dados/07 - Gestão Centralizada de Dados]]
- Família canônica e classificação: [[Sistema Operacional Comercial/03 Estoque/01 - Família Canônica]]
- Inteligência comercial (custo de servir, 3 verdades): instruções do projeto "Estratégico - Comercial"
- Processo Duferco-Brasil (afeta timing): [[2026-04-17 — Estrutura Duferco-Brasil]]
- Plano transição AFS-MetalM (define ownership): [[2026-04-17 — Plano de transição AFS-MetalM (Cenário F)]]
