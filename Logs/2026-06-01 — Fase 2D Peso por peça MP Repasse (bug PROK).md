# 2026-06-01 — Fase 2D Peso por peça MP Repasse (bug PROK forjado)

## Contexto

Caso real PROK/MG: orçamento Sacchelli p/ 3 peças de eixo forjado 4340 redondo, comprimento 2150mm, R$ 12.800/Pç (ICMS 18% + PIS/COFINS 9,25%). Vendedor não preencheu bitola da peça final porque é peça forjada — geometria irregular, não cilíndrica.

Painel mostrou:
- Custo Líq. Unit: R$ 9.525,12/Pç ✓ (calculado corretamente)
- **Matéria Prima na Memória de Cálculo: R$ 0,00** ✗ (zerada silenciosamente)
- Preço sugerido R$ 621,99/Pç (MC 14,31%) — calculado SÓ sobre serviços externos (EMT R$ 246,84 + EUT R$ 122,55)
- **Custo real ignorado: R$ 28.575,36** (3 × R$ 9.525,12)

Se a proposta fechasse: prejuízo de ~R$ 27 mil no pedido.

## Causa raiz

`motor_precificacao.js` linha 1950 — `calcCustoRepasseNacional`:

```js
let peso_total_kg = 0;
if      (unidade === 'ton')   peso_total_kg = qty * 1000;
else if (unidade === 'kg')    peso_total_kg = qty;
else if (unidade === 'pc' && coef_lin > 0 && comp_mm > 0) peso_total_kg = coef_lin * comp_mm * qty;
```

Para `unidade='pc'`, peso vem de `coef_lin × comp_mm × qty`. `coef_lin` é função de perfil + bitola (Ø):
- Redondo: `π × (Ø/2)² × 7,85e-6`

Sem bitola, `coef_lin = 0` → `peso_total_kg = 0` → `custo_liq_ton = 0` → motor principal lê zero do dataset → MP não entra na cascata de margens. Silenciosamente.

Pra forjados, isso NUNCA funcionaria mesmo com bitola — porque cálculo geométrico `π × Ø²` pressupõe seção cilíndrica constante. Forjado tem ressaltos, flanges, escalonamentos — peso real ≠ peso geométrico.

## Implementação

### 1. Campo novo no HTML
`sim-rep-peso-pc` (opcional, kg/peça) — aparece quando MP Repasse Pç está ativo. Tooltip explica: "Use quando o motor não consegue calcular peso geométrico — peça forjada, usinada, geometria irregular. Quando preenchido, sobrescreve o cálculo geométrico (π × Ø² × comp). Deixe vazio se for tarugo cilíndrico padrão."

### 2. Motor — `calcCustoRepasseNacional`
Novo parâmetro `peso_pc_kg`. Quando informado E `unidade='pc'`, sobrescreve cálculo geométrico:
```js
else if (unidade === 'pc' && peso_pc_kg != null && peso_pc_kg > 0 && qty > 0) {
    peso_total_kg = peso_pc_kg * qty;
}
```
Mantém os outros caminhos (ton, kg, pc geométrico, m geométrico) intactos — retrocompatibilidade total.

### 3. `simCalcRepasse` — leitura do novo campo
Passa `peso_pc_kg` (null se vazio) pro motor. Persistido no `SIM_SAVE_FIELDS` ao lado de `sim-rep-comp`.

### 4. Alerta visual — quando peso=0 + qty>0 + nf>0 + unit=pc
Banner vermelho no `sim-rep-peso-info`:
> ⚠ SEM PESO POR PEÇA: preencha a bitola (Ø) da peça final OU o campo "Peso por peça (kg)" acima. Sem isso, o custo da Matéria Prima NÃO entra na margem e o preço final fica subdimensionado.

Banner é dismissable só ao corrigir o input. Vendedor não tem como gerar proposta com custo zero sem ver o alerta.

### 5. Persistência
`sim-rep-peso-pc` adicionado ao `SIM_SAVE_FIELDS`. Save/restore do PACOTE pega como qualquer outro campo per-item.

## Validação com caso PROK

| Configuração | peso_total_kg | custo_liq_ton | custoTotal MP |
|---|---|---|---|
| Antes do fix (sem bitola, sem peso) | 0,0000 | R$ 0,00 | **R$ 0,00 (bug)** |
| Pós-fix (peso 65kg/pç) | 195,0000 | R$ 146.540,31 | **R$ 28.575,36 ✓** |
| Pós-fix (legado: bitola Ø100, sem peso explícito) | 397,6667 | R$ 71.857,56 | R$ 28.575,36 ✓ |
| Pós-fix (sem bitola, sem peso → bug original) | 0,0000 | R$ 0,00 | R$ 0,00 + ALERTA VERMELHO |

Note que o último cenário ainda zera o cálculo — mas agora o vendedor VÊ o alerta antes de fechar a proposta. Não vaza silenciosamente.

## Suite

1.126/1.126 testes verdes (zero regressão). Validação adicional via 4 casos manuais do motor.

## Mensagem pro time comercial

Quando o material de partida for **peça forjada, usinada ou de geometria irregular**:
1. Marque MP Repasse, escolha unidade "R$/Pç"
2. Digite o **Preço Unit. (c/ ICMS e PIS)** como antes
3. **Preencha "Peso por peça (kg)"** — pegue da NF do fornecedor (linha de peso bruto/peça) ou da ficha técnica do forjado
4. O custo total da MP aparece corretamente na Memória de Cálculo

Pra tarugo cilíndrico padrão (laminado redondo, sem usinagem), continue preenchendo só a bitola (Ø) da peça final — o motor calcula peso geométrico como antes.

## Pendências derivadas

1. **Auditar propostas geradas no simulador desde 22/04/2026** (quando MP Repasse foi refatorado) — qualquer item MP Repasse Pç sem bitola da peça é candidato a margem furada. Filtrar por `_pacote_state` no localStorage / propostas salvas.
2. **Estender fix pra Importação Pç**: motor de importação tem cascata análoga em `calcCustoImportacao` — pode ter o mesmo bug pra importações de peças prontas. Avaliar.
3. **Refactor arquitetural (parqueado)**: motor aceitar custo unitário em qualquer unidade sem forçar conversão pra Ton. Não vale pra esse caso (peso_pc_kg resolve), mas vale acompanhar se outros cenários aparecerem.

---

## Update 01/06/2026 — Fase 2D-bis: regra de negócio simplifica tudo

Gustavo apontou regra de negócio AFS: **MP Repasse Pç → Venda obrigatoriamente Pç**. Peça pronta comprada de terceiro não vira tarugo nem é refaturada por Kg/Ton.

Isso muda o desenho:

### Decisões revisadas

1. **Peso da peça não é obrigatório** quando compra=Pç e venda=Pç. Matemática fecha unitariamente: `custoTotal = custo_liq_unit × qty`.
2. **Motor agora suporta "modo unitário fictício"**: quando `unidade='pc'` E sem peso (geométrico ou explícito), assume peso=1kg/Pç fictício. `custo_liq_ton` fica "inflado" internamente, mas a cascata matemática (R$/ton × kg/1000) reconstrói o custo total correto. Flag `_peso_modo_unitario` retornada pra UI saber.
3. **Toggle "Venda por:" travado em Pç quando MP Repasse Pç ativo**: botões Kg/m ficam desabilitados (opacity 35%, cursor not-allowed, tooltip explicativo). Setor de venda força `setSellUnit('pc')` ao ativar.
4. **Banner azul informativo** substitui o alerta vermelho: "Cálculo unitário ativo · Custo Líq/Pç: R$ X · Custo Total MP: R$ Y". Não é problema, é o caminho válido.
5. **Campo "Peso por peça (kg)"** continua disponível mas é OPCIONAL — serve só pra info no PDF (logística, frete por peso, declaração de NF). Não afeta cálculo de margem.

### Validação caso PROK

- Compra 3 Pç a R$ 12.800/Pç (ICMS 18% PIS 9,25%) → Custo Líq R$ 9.525,12/Pç
- Sem bitola, sem peso → modo unitário fictício
- Custo Total MP = R$ 28.575,36 ✓
- Banner azul: "Cálculo unitário ativo · Custo Líq/Pç: R$ 9.525,12 · Custo Total MP: R$ 28.575,36"
- Botões Kg e m desabilitados no "Venda por:" — vendedor não consegue trocar
- Suite 1.126 testes verdes

### Próximo passo
Próxima sessão pode revisar: a regra "MP Repasse Pç → Venda Pç" se aplica também a **MP Repasse Kg** vs **Venda Pç**? Caso típico: cliente compra barra (Kg) e revende como peça cortada (Pç). Provavelmente sim — mas precisa peso pra converter. Esse cenário fica fora do escopo da Fase 2D — motor já tratava corretamente nesse caminho.

---

## Update 01/06/2026 noite — Fase 2D-quattro: auditor de serviços agregados

Gustavo apontou: alguns serviços agregados têm custos calculados por peso (R$/ton, R$/kg) ou comprimento (R$/m). No modo MP Repasse Pç, esses dependem da peça final ter peso (quando custo é por peso) ou comprimento (quando custo é por metro) — senão zeram silenciosamente, igual ao bug original.

### Mapeamento das dependências

| Tipo | Default unit | Depende de | Exemplos AFS |
|---|---|---|---|
| Certificação `pct_custo` | % sobre custo MP | Custo MP correto (✓ Fase 2D) | AQ1, GTT, DUR, EME, TTU, TGA, EJO, EPM |
| Certificação `unitario` | R$/un | Nada | EMT, EMI, ET2, EUS, MAC, MET, CBP, JBS |
| Certificação `metro` | R$/m | **Comprimento da peça** | EUQ, EUT, EUP |
| Fase TT | R$/ton | **Peso da peça** | BJ1, BJ2, NO2, TR1, AT1, RZ1, etc |
| Fase TD | R$/ton | **Peso da peça** | TA1, TA2, DL1, TD1, DSX |
| Fase USX `unit:'peca'` | R$/Pç | Nada | USX, USS, FUX |
| Fase USX `unit:'ton'` | R$/ton | **Peso da peça** | U01, U02, U11, U21, U31, DL1 (USX) |
| Fase EMB default | R$/un | Nada | BX2, BX4, BX5, BX6, BXX |
| Fase EMB `unit:'ton'` | R$/ton | **Peso da peça** | BX3 (Plástico Bolha) |

### Implementação

Função `simAuditarServicosRepasse()` (~70 linhas) que:
1. Só roda quando MP Repasse Pç ativo (early return)
2. Inspeciona estado: peso explícito (sim-rep-peso-pc) + peso geométrico (dataset.pesoTotalKg/qty) + comprimento da peça (sim-peca-l)
3. Considera "peso real" quando ≥1,5 kg/Pç (filtra fictício de 1kg do fallback Fase 2D)
4. Coleta certificações ativas (`_certs`) e fases industriais (`simPhases`)
5. Cruza com catálogo (`SIM_CERT_PHASES`, `SIM_TT/TD/USX/EMB_PHASES`) pra inferir base de cálculo
6. Detecta combinações onde campo requerido está vazio
7. Renderiza banner amarelo agregado (`#sim-rep-audit-info`) listando código + descrição + base de cada serviço pendente

### Hooks engatados

- Fim de `simCalcRepasse` — recálculo padrão do bloco MP Repasse
- Toggle de Certificações (`sim-cert-on` onchange)
- `simRenderPhases` — quando adiciona/remove fase TT/TD/USX/EMB
- `simCertChange` — quando marca/desmarca certificação individual
- `oninput` do `sim-peca-l` — quando vendedor preenche comprimento da peça

### UX do banner

Cores: fundo amarelo escuro (#78350f), texto amarelo claro (#fef3c7), borda âmbar (#f59e0b). Ícone ⚠ + cabeçalho "Campos obrigatórios pra serviços agregados". Lista agrupada por campo faltante (Peso vs Comprimento), com requisitos detalhados. Disclaimer no rodapé: "Sem isso, esses serviços calculam R$ 0,00 e o preço final fica subdimensionado."

### Suite

1.126 testes verdes — auditor é puramente UI (DOM-side), não toca motor.

### Pendência derivada

Auditor não cobre Importação Pç (`calcCustoImportacao`) — esse motor tem cascata análoga mas a auditoria precisa de adaptação. Próxima sessão.
