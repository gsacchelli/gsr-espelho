---
data: 2026-04-20
tipo: log
status: vigente
obs: "concluída — aguarda validação visual no navegador"
projeto: Simulador Precificação → Proposta Comercial
fase: 4 (Gerador HTML — greedy)
relacionados: 
---

# Fase 4 — Gerador de HTML da Proposta (greedy)

## Decisão estratégica

**Não esperar Camada 6 fechar.** Puxado o Caminho 1: Fase 4 roda com o que o motor expõe hoje. NCM/prazo/certif ricos viram upgrade aditivo quando Fase 2 chegar (pós-Camada 6). Justificativa: tirar produto da gaveta > zero retrabalho. Custo do retrabalho da Fase 2 é marginal (adapter do coletor consome mais campos quando existirem — HTML gerado não muda estrutura).

## Entregas

### 1. `03_Ferramentas/js/gerador_proposta.js` — módulo puro autocontido

- **Logo Sacchelli embutida como data URI base64** (~30KB PNG → ~41KB base64 no arquivo). Proposta gerada é portável, compartilhável, imprimível sem depender do folder da Sacchelli.
- **CSS inline** copiado do `07_Marca/Proposta_Sacchelli_Layout.html` (20/04/2026). Um único arquivo HTML é output — abre no browser, imprime em PDF via Ctrl+P.
- **Funções puras**: `formatBRL`, `formatDataBR`, `formatUnit`, `escHTML`, `unidadeCurta`, + 7 builders de seção.
- **Orquestrador `buildHTML({meta, linhas, totais, creditos})`** — retorna string HTML completa com 7 seções: header (logo + dados + meta + número) → cliente → intro → tabela itens → totais (créditos + grande destaque) → info-grid (informações gerais + condições comerciais) → footer.
- **Segurança**: todo texto externo passa por `escHTML` — injection HTML em razão social ou descrição é neutralizada.
- **Dual export**: roda em browser (`window.GeradorProposta`) e Node (`require`).

### 2. `03_Ferramentas/js/gerador_proposta.test.js` — 84 testes verdes

Cobertura:
- **formatBRL** (14 casos): inteiros, decimais, zero, negativos, 8 dígitos, precisão 0/4, NaN/null/undefined, string parseável, sub-mil, primeiro ponto de milhar
- **formatDataBR** (7 casos): ISO→BR, BR passthrough, vazio/null/undefined, string arbitrária
- **formatUnit** (7 casos): pc/Pç/kg/Kg/m/M + vazio default
- **escHTML** (7 casos): `<>`, `&`, `"`, `'`, null/undefined, texto normal
- **unidadeCurta** (5 casos): todas as 6 unidades AFS + sem UF + vazio
- **buildHTML documento completo** (38 checks): estrutura (DOCTYPE, html lang, title, CSS, logo), header (unidade curta, nº, revisão), cliente (razão, cidade+UF, att, email), tabela (2 itens com unidades diferentes, vunit BR, subtotal BR, NCM, ICMS, IPI, prazo custom + default, badges), totais (s/IPI, c/IPI, créditos), condições (pagamento parcelado BR, frete, validade, uso, observação, bullets info gerais), footer
- **Edge cases** (6 casos): sem certificados/extras → sem badges, pacote vazio, pagamento À vista sem "ddl", ISO→BR, "1 dia" singular, injection XSS neutralizado

### 3. Integração no HTML do simulador

Substituí o placeholder Fase 3 do `propostaGerar()`:

1. **Coletor `propostaColetarLinhas()`** — varre `PACOTE.itens`, força snapshot fresco do ativo via `pacoteCaptureFullState()`, reutiliza `_pacoteItemMetrics` (linha 9145 do HTML) pra derivar qty/preço/receita/peça/ICMS por item. Fallbacks greedy: IPI 3,25%, NCM 7228.5000, prazo "A combinar".
2. **Totais `propostaCalcularTotais(linhas)`** — reduz subtotal s/IPI, calcula IPI R$, soma com subtotal pra c/IPI, créditos ICMS (12%), PIS+COFINS (9,25% do SIM_LAST_CALC se disponível), IPI. Alinhado com o que o painel do pacote já mostra.
3. **Gerar → nova aba via Blob URL**. Fallback pra download de arquivo se o popup for bloqueado.
4. **Modal de revisão preservado** (Fase 3). Sim → incrementa rev + atualiza data + gera; Não → sobrescreve versão atual + gera.
5. **Consumo de numeração** — só consome do contador se o campo "Orçamento nº" estiver vazio ou abaixo do seed (500000). Override manual do usuário preserva a sequência interna.

Novo script tag carregado:
```html
<script src="js/gerador_proposta.js"></script>
```

## Arquivos alterados

- **Novo**: `03_Ferramentas/js/gerador_proposta.js` (472 linhas — 30 linhas de lógica + 1 linha de 41KB base64 + CSS inline)
- **Novo**: `03_Ferramentas/js/gerador_proposta.test.js` (84 testes)
- **Editado**: `03_Ferramentas/Analise_Precificacao_Sacchelli.html` — script tag + reescrita de `propostaGerar` + novas helpers `propostaColetarLinhas` e `propostaCalcularTotais`

## Validações executadas

- ✓ 56/56 testes schema_proposta.test.js
- ✓ 84/84 testes gerador_proposta.test.js
- ✓ 458/458 testes motor_precificacao.test.js (regressão — layer desacoplada não tocou motor)
- ✓ Runtime check com DOM mock + PACOTE mock de 2 itens (1 estruturado pc com cert, 1 livre kg sem cert):
  - buildHTML invocado
  - HTML gerado contém cliente, 2 itens, unidades corretas (Pç/Kg), peça livre no item 2, badge Certificados no item 1
  - Revisão incrementada corretamente (00 → 01)
  - Override manual de numeração NÃO consumiu contador (storage preserved)
- ⏳ **Smoke visual no navegador — pendente validação do Gustavo**

## Limitações conhecidas (greedy — Fase 2 upgrade aditivo)

1. **NCM fixo 7228.5000** — cobre ~90% do catálogo AFS (aços especiais ligados). Aços-carbono lisos (7228.30+1045 por exemplo) têm NCM diferente. Upgrade: Fase 2 expõe NCM do motor via família canônica.
2. **IPI fixo 3,25%** — default AFS. Alguns produtos têm alíquota diferente. Upgrade: campo editável por item ou leitura do cadastro do produto.
3. **Prazo "A combinar"** — não existe campo de prazo por item no simulador hoje. Upgrade: adicionar campo no DOM do item OU no Setup da proposta.
4. **Certificados/Extras simples** — "Sacchelli + Usina · Conforme orçamento" como rótulo genérico. Upgrade: expor do motor a lista legível de fases ativas (TT/TD/USX/EMB/Cert por código).
5. **Descrição técnica** — monta de `pecaLabel` (estruturado) ou `sim-peca-texto` (livre). Sem override dedicado pra proposta. Upgrade: campo "descrição pra proposta" por item na Fase 2.
6. **Desconto do pacote** — hoje reduz subtotal na UI do pacote consolidado, mas o gerador atual usa receita bruta por item. Se o usuário usar desconto de pacote, a proposta mostrará valores sem o desconto — tem que ser aplicado manualmente ou virar upgrade.

## Fluxo real pro usuário

1. No simulador, abre a seção "📄 Proposta Comercial" (topo) e preenche razão social, cidade, UF, att, email, ref.
2. Preenche/ajusta condições (pagamento, frete, validade, uso).
3. No rail do Pacote, adiciona/edita itens — cada item com preço negociado + VTs.
4. Clica "📄 Gerar Proposta" (toolbar top).
5. Modal: "Nova revisão?" Sim/Não.
6. Nova aba abre com a proposta formatada.
7. Ctrl+P → Salvar como PDF → envia pro cliente.

## Próxima sessão

### Validação visual (imediato)
1. Abrir simulador no Chrome
2. Preencher 1 item + dados da proposta
3. Gerar — confirmar que nova aba abre com layout correto
4. Conferir: logo Sacchelli renderizada, nº/rev no canto direito azul, cidade/UF com badge, pagamento com "ddl" se parcelado, tabela de itens com valores BR (vírgula decimal, ponto de milhar), totais destacando IPI incluso em amarelo, condições legíveis, footer com data
5. Imprimir em PDF (Ctrl+P) — verificar que cabe em A4, sem cortar

### Se tudo ok, próximos passos possíveis:
- **Fase 2** (expor NCM/prazo/certif/descrição do motor) — destrava upgrade aditivo sem mexer no HTML gerado
- **Fase 5 futura** (integração Softcomp CNPJ → autopreenche cliente)
- **Fase 6** (numeração sincronizada com ERP)
- **Refatoração Setup em 5 abas (#56)**

### Se algo quebrar visualmente:
- Ajuste de CSS ou template é localizado em `gerador_proposta.js` (seção `CSS_PROPOSTA` + builders de seção)
- Estrutura dos 84 testes unitários dá cobertura rápida pra regressão após correção

## Decisões arquiteturais registradas nesta sessão

1. **Greedy > esperar Fase 2**. Tiramos produto da gaveta com fallbacks explícitos. Retrabalho Fase 2 é aditivo, não-breaking.
2. **Logo embutida em base64** (~41KB). Autocontenção é mais valiosa que o custo do arquivo maior.
3. **CSS inline** (cópia do layout 07_Marca). Autocontido. Evolução do CSS exige atualizar o módulo — trade-off aceitável porque mudanças de brand são raras.
4. **Output em nova aba + Blob URL**. Abre instantaneamente, usuário imprime via browser. Alternativa iframe-embed foi descartada (complicação de layout) e download direto tem UX pior (precisa clicar no arquivo).
5. **Fallback de download se popup bloqueado**. UX degrada com graça.
6. **Coletor reutiliza `_pacoteItemMetrics`**. Zero duplicação da lógica de parse — aproveita o que o pacote consolidado já faz.
7. **Contador NÃO avança se usuário editou nº manualmente**. Reproduz comportamento do Softcomp velho sem poluir a sequência interna.

## Status geral do projeto Proposta

| Fase | Descrição | Status |
|---|---|---|
| 1 | Camada 6 (motor — MP Repasse + Importação) | Em andamento (fixtures 09/10 + regressão pendente) |
| **3** | **Schema Proposta + UI no simulador** | **Concluída 20/04/2026 manhã** |
| **4 greedy** | **Gerador HTML da Proposta** | **Concluída 20/04/2026 tarde — esta sessão** |
| 2 | Expor descrição/certif/NCM/prazo no output do motor | Aguardando Camada 6 |
| 5 (futura) | Integração Softcomp (cliente + numeração) | Backlog |
| Setup | Refatorar Setup atual em 5 abas | Após validação Fase 4 |

**Produto já usável**: desde agora, Gustavo pode gerar propostas reais para clientes. Upgrades Fase 2 são incrementais e não bloqueiam o uso.
