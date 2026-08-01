---
data: 2026-04-20
tipo: log
status: vigente
obs: "concluída — aguarda validação em produção"
projeto: Simulador Precificação → Proposta Comercial
fase: 3 (Schema + UI no simulador)
relacionados: 
---

# Fase 3 — Schema de Proposta + UI no Simulador

## O que entrou

Implementação da camada de **metadados da proposta** (Blocos A/B/C/D) sobre o motor de precificação. Opção 1 da arquitetura: layer separada do motor, sem expandir EntradaPrecificacao. Tudo isolado em JS puro testável + UI embutida no simulador atual.

## Entregas

### 1. `03_Ferramentas/js/schema_proposta.js` — módulo puro (dual export: browser + Node)

- **Constantes**: `SEQ_SEED=500000`, 27 UFs, opções de pagamento/frete/uso, `DEFAULTS_AFS` (6 bullets de Informações Gerais + vendedor Gustavo S. Ramos + validade 2d + textos fixos).
- **Parser `parsePagamento(tipo, parcelado)`**:
  - Antecipado → 0 dias
  - À vista → 1 dia
  - Parcelado "30/45/60" → média aritmética 45 dias (alimenta o CF do motor)
  - Malformado → fallback 1 dia + flag de erro (nunca 0 por acidente — design defensivo)
- **Helpers**: `displayPagamento`, `proximaRevisao` (zero-padded), `peekProximoNumero`/`consumirProximoNumero`/`resetarContador`.
- **Factory `novaProposta(overrides)`**: retorna Meta completa com defaults aplicados.
- **Validação `validarProposta(meta, {itens})`**: razão social + cidade + UF válida (27) + parcelado consistente + pacote não vazio. Retorna `{ok, erros:[{campo,msg}]}` pra highlight de UI.

### 2. `03_Ferramentas/js/schema_proposta.test.js` — 56 testes verdes

Cobertura: 14 casos do parser (inclui "30,5/45,5", "-30", "//"), 5 do display, 8 de revisão, 7 de numeração (com mock storage), 3 do factory, 12 de validação, 7 de constantes. **Regra de cobertura real aplicada**: todos os ramos de parsePagamento testados (Antecipado, À vista, Parcelado 1 parcela, Parcelado N parcelas, vazio, não-numérico, negativo, só separadores, tipo desconhecido). 458 testes do motor seguem verdes (regressão limpa — layer de proposta não toca motor).

### 3. UI — seção colapsável "📄 Proposta Comercial" no simulador

Ancoragem: **entre a toolbar top e o rail de pacote** (linha ~360 do HTML). Razão: dados da proposta são "envelope" per-pacote; rail é "itens"; detalhe é "item". Fluxo semântico: envelope → itens → detalhe.

3 cards em grid responsivo (`minmax(280px,1fr)`):
- **Card 1** — Orçamento & Cliente: nº/rev/data/ref/vendedor/unidade + razão social/cidade/UF/att/email.
- **Card 2** — Condições Comerciais: pagamento (com campo de parcelas condicional) / frete / validade / uso / impostos / observação. Hint dinâmico em "Parcelas" mostra média calculada em tempo real.
- **Card 3** — Informações Gerais: textarea 12 linhas + botão "↻ Default AFS" + bloco de status de validação (live).

Header mostra resumo: `📄 Proposta Comercial — <RAZÃO> · <Cidade/UF>   Nº 500000 · Rev. 00`.

### 4. Integração com painel original "Orçamento do Cliente"

**Decisão**: manter `sim-cliente-nome` e `sim-cliente-uf` como single source of truth pros cálculos (simAutoICMS, print, save/restore). Campos novos no card de Proposta espelham via event listener `input` bidirecional. Mudança em um reflete no outro imediatamente. Zero duplicação de dado.

Justificativa: 8+ referências ao `sim-cliente-nome`/`sim-cliente-uf` espalhadas no código (cálculo, print, save). Migrar seria cirurgia arriscada. Espelhar via listener resolve UX com custo marginal.

### 5. Setup — nova seção "Padrões de Proposta Comercial"

Colapsável, no final do tab-setup (antes da refatoração #56 em 5 abas). Contém:
- Vendedor default + Unidade default
- Pagamento/Frete/Validade/Uso default (com toggle condicional do campo de parcelas)
- Texto de Impostos + Observação default
- Textarea de Informações Gerais (6 bullets AFS pre-populados)
- **Bloco Numeração**: visualização do próximo número, botão "↺ Resetar contador" (com confirm), botão "↻ Restaurar defaults AFS"

Persistência: key `afs_proposta_defaults` (JSON). Merge com `DEFAULTS_AFS` do schema — override parcial funciona.

### 6. Persistência da proposta corrente

Key `sacchelli-simulador-proposta-meta` — JSON completo dos 4 blocos. Auto-save com debounce de 400ms em qualquer mudança. Restore ao carregar. Se não houver meta salva, usa `novaProposta(defaults do Setup)` + data de hoje + preview do próximo número.

**Numeração**:
- Preview exibido no campo "Orçamento nº" e no header da seção
- `consumirProximoNumero()` só é chamado no clique de "Gerar Proposta" (não em auto-save)
- Override manual do usuário no campo NÃO quebra a sequência interna — contador do storage é independente

### 7. Botão "📄 Gerar Proposta" (toolbar top)

Clique executa:
1. `validarProposta(meta, {itens: PACOTE.itens.length})`
2. Se inválido: destaca campos em vermelho (box-shadow pulsante 2.6s), toast de erro, abre a seção se estiver colapsada
3. Se válido: abre modal de revisão — *"Esta alteração é uma nova revisão?"*
   - Sim → incrementa revisão + atualiza data de emissão + salva
   - Não → sobrescreve versão atual + salva
   - Checkbox "Não perguntar nesta sessão" (responde "Não")
4. Consome número do contador (se ainda era preview)
5. Toast de sucesso com número + revisão
6. **Placeholder pra Fase 4**: gerador HTML A4 não implementado ainda ("aguarda Fase 4")

## Arquivos alterados

- **Novo**: `03_Ferramentas/js/schema_proposta.js` (módulo de schema)
- **Novo**: `03_Ferramentas/js/schema_proposta.test.js` (suite 56 testes)
- **Novo**: `Logs/2026-04-20 — Fase 3 Proposta Schema e UI.md` (este log)
- **Editado**: `03_Ferramentas/Analise_Precificacao_Sacchelli.html`
  - Linha ~223: `<script src="js/schema_proposta.js">`
  - Linha ~359: botão "📄 Gerar Proposta" na toolbar + bloco colapsável com 3 cards
  - Linha ~1707: seção "Padrões de Proposta Comercial" no Setup
  - Linha ~9532: IIFE com ~500 linhas — schema glue, persistência, mirror, validação, modal, toast

## Validações executadas

- ✓ 56/56 testes schema_proposta.test.js
- ✓ 458/458 testes motor_precificacao.test.js (regressão, layer separada não tocou motor)
- ✓ Parse syntax do IIFE (node new Function)
- ✓ Runtime check do IIFE com mocks DOM — init + 5 funções globais + propostaGerar sem throw
- ✓ 40/40 IDs HTML presentes via grep
- ✓ 9/9 funções globais `window.proposta*` declaradas
- ⏳ **Smoke visual real no navegador — pendente validação do Gustavo**

## Correções pós-implementação (mesma sessão, 20/04/2026 tarde)

Feedback do Gustavo durante review:

1. **Unidades corretas da Sacchelli** — substituídas nos selects (card Proposta + Setup):
   - Guarulhos/SP, São Paulo/SP, Piracicaba/SP, São Carlos/SP, São José do Rio Preto/SP, Caxias do Sul/RS
   - `DEFAULTS_AFS.unidade` e fallback → "Guarulhos/SP"
2. **Campos Emissão e E-mail padronizados como `type="text"`**:
   - Emissão: placeholder "dd/mm/aaaa", default do JS agora em `hojeBR()` (dd/mm/yyyy) em vez de `hojeISO()`
   - E-mail: `type="email"` → `type="text"` (alinha com estilo do campo Cliente)
   - Razão: o painel "Orçamento do Cliente" (que hoje hospeda o campo Cliente como `type="text"`) **será deletado em breve** — essa padronização antecipa a migração pros campos do card de Proposta.
3. **Teste ajustado** pra novo default "Guarulhos/SP" — 56/56 seguem verdes.

## Limitações conhecidas (por design, não bugs)

1. **Gerador HTML A4 é placeholder** — toast diz "aguarda Fase 4". Fase 4 bloqueada pela Fase 2 (Expor NCM/prazo/descrição rica/certificados legíveis no output do motor), que por sua vez aguarda fechamento formal da Camada 6 (MP Repasse + Importação).
2. **Per-item fields fora do escopo** — descrição técnica rica por item, NCM, prazo, lista legível de certificados. Esses ficam na Fase 2.
3. **Integração Softcomp (auto-preencher cliente por CNPJ)** — Fase 5 futura, fora de escopo.
4. **Refatoração do Setup em 5 abas (#56)** — seção "Padrões de Proposta" hoje vive no Setup monolítico. Quando a refatoração rodar, migra pra aba Comercial.

## Próxima sessão

**Validação em produção no navegador** (prioridade imediata):
1. Abrir `03_Ferramentas/Analise_Precificacao_Sacchelli.html` no Chrome
2. Clicar em "▸ 📄 Proposta Comercial" — deve expandir 3 cards
3. Preencher razão social, cidade, UF — confirmar mirror com painel "Orçamento do Cliente" (campo original deve atualizar sozinho)
4. Mudar pagamento pra "Parcelado", digitar "30/45/60" — hint deve mostrar "Média = 45 dias"
5. Clicar "📄 Gerar Proposta" com campos incompletos — deve destacar campos + toast de erro
6. Preencher tudo + clicar Gerar — modal de revisão aparece
7. Refresh da página — dados devem persistir (localStorage)
8. Ir no Setup → "Padrões de Proposta Comercial" — verificar defaults + testar "Resetar contador"

**Depois da validação**:
- Se algo quebrar → correção pontual, mantém cobertura de teste
- Se tudo ok → a Fase 3 fecha e desbloqueia Fase 4 assim que Camada 6 terminar
- Paralelo: Gustavo pode tocar **Camada 6 finish** (fixtures 09/10 + regressão bit-idêntica do HTML corrigido) enquanto Proposta sedimenta

## Decisões arquiteturais registradas nesta sessão

1. **Opção 1 (layer separada) mantida na implementação** — zero acoplamento com motor. Motor ficou com 458 testes verdes intocados.
2. **Mirror bidirecional > migração de IDs** — evita cirurgia nas 8+ referências a `sim-cliente-*`. Event listener `input` nos dois lados.
3. **Fallback defensivo em parsePagamento** — erro retorna 1 dia (À vista), nunca 0. Só Antecipado explícito zera o CF.
4. **Contador independente de edição manual** — override do usuário no campo de número não mexe no storage. Sequência preservada mesmo se ele reproduzir números Softcomp antigos.
5. **Auto-save debounce 400ms** — rápido o suficiente pra sensação de "gravado automaticamente", lento o suficiente pra não martelar o localStorage em digitação.
6. **Seção colapsável inicia fechada** — tela limpa no primeiro load. Header mostra resumo + número, então o usuário já vê o estado sem precisar abrir.

## Hardcodes a migrar na fase pós-motor (lista incremental)

Nenhum novo — essa camada não usa o config do motor. `DEFAULTS_AFS` do schema já é sobrescrito pelo Setup da própria proposta, o que é o comportamento correto.
