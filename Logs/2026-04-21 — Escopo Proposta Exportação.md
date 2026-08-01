---
data: 2026-04-21
tipo: log
status: vigente
---
# 2026-04-21 — Escopo Proposta de Exportação (USD, EN)

Feature planejada. Escopo fechado com Gustavo. **Implementação parada aguardando sinal verde** (prioridade definida depois, sem conflito com processo Duferco-Brasil em curso).

## Modelo de negócio (decisões)

1. **Cálculo de custo idêntico ao atual.** Mesmo motor das tabelas V/A/R. Nada muda no custo (MP, fases, certs, CP, CAP, mtl comp) — AFS não tem drawback nem regime especial de exportação.
2. **Impostos zerados na saída.** DESP% perde ICMS, PIS/COFINS e IPI. Sobra só CF, comissão, DDV, outros/logística.
3. **Preço de venda em USD.** Cálculo fica em BRL, no final divide pelo câmbio do Economic Level e mostra o preço final em dólar. Custo no simulador mantém-se em BRL — nenhum campo "equivalente em USD" no DRE.
4. **Cliente exportação não tem CNPJ.** Schema substitui UF por `country` (e mantém `cidade` → "City").
5. **Frete fixo: EXW Sacchelli-Guarulhos.** Incoterm não editável no modo exportação.
6. **DRE com impostos zerados.** Linhas de ICMS/PIS/COFINS/IPI aparecem mas com valor zero (transparência fiscal de imunidade).

## PDF em inglês

- Todas as strings do template (`gerador_proposta.js`) traduzidas para EN via dicionário `i18n.pt/i18n.en`.
- Formatação US pra valores em USD: `$ 1,234.56` (vírgula milhar, ponto decimal).
- Campos novos no bloco de Condições:
  - **Exchange Rate:** `USD 1 = BRL X,XX` (câmbio usado)
  - **Economic Level:** `DD/MM/YYYY` (data da cotação de custos + câmbio)
  - **Incoterm:** `EXW Sacchelli-Guarulhos` (fixo)
- Blocos "ICMS / PIS / COFINS / IPI" do rodapé zerados ou suprimidos (decidir visual: manter com "0%" ou esconder).

## Alterações técnicas previstas

### Schema da proposta
```js
PropostaMeta.exportacao = {
  ativa: boolean,
  cambio_usd_brl: number,
  economic_level_date: string (ISO YYYY-MM-DD),
  incoterm: 'EXW Sacchelli-Guarulhos'  // fixo quando ativa=true
}

PropostaMeta.cliente = {
  // campos existentes + country em vez de uf quando exportação
  razao_social, att, email, cidade,
  uf | country   // mutualmente exclusivos por modo
}
```

### UI — card "Orçamento & Cliente"
- Toggle `☐ Proposta de Exportação (USD)` no topo.
- Quando ATIVA: esconde UF, mostra `Country`; adiciona campos Câmbio USD/BRL e Economic Level (default = data de hoje); Incoterm trava em EXW Guarulhos.
- Quando INATIVA: UI normal atual.

### Motor de cálculo (simCalcDESP + simCalc)
- Ler flag `window.PROPOSTA_EXPORTACAO?.ativa` (ou via getter no IIFE).
- Se ativa: ICMS=0, PIS/COFINS=0, IPI=0 (desconsidera valores de tela). Resto do cálculo inalterado.
- Preço de venda em USD = preço BRL / câmbio.

### Validações
- Exportação ativa + câmbio vazio/zero → bloqueia `Gerar Proposta` com mensagem clara.
- Economic Level obrigatório (default = hoje).

### PDF (gerador_proposta.js)
- Novo arquivo `i18n_proposta.js` com dicionário PT/EN.
- `buildHTML` recebe `meta.exportacao`, escolhe idioma.
- Formatação: função `formatMoney(valor, moeda, idioma)` → BRL/BR ou USD/US.
- Bloco Condições Comerciais adaptado em EN quando modo exportação.

## Estimativa

- Schema + toggle UI + motor: 1-2h.
- PDF i18n (EN + US format + campos exportação): 2-3h.
- Validações + testes: 1h.
- Total: **meio dia de trabalho concentrado**.

## Decisões complementares (21/04/2026 noite)

1. **Linhas fiscais do DRE em modo exportação: ESCONDIDAS.** Layout limpo. Sem ICMS/PIS/COFINS/IPI no bloco.
2. **Campo Country: input livre.** Sem lista — vendedor digita o país do cliente.
3. **Data Economic Level no PDF EN: `DD/MMM/YYYY`** (ex: `21/Apr/2026`). Formato inequívoco, legível internacionalmente.
4. **Moeda: só USD por ora.** Não projetar EUR — se precisar no futuro, fica pra outro momento.

## Arquivos impactados

- `03_Ferramentas/Analise_Precificacao_Sacchelli.html` — UI do card Orçamento & Cliente + novos campos + getter flag + validação pré-gerar.
- `03_Ferramentas/js/schema_proposta.js` — bloco `exportacao`, defaults, validação.
- `03_Ferramentas/js/gerador_proposta.js` — consumir flag, renderizar campos exportação no PDF.
- **Novo:** `03_Ferramentas/js/i18n_proposta.js` — dicionário PT/EN.
- Motor analítico: NENHUM impacto (motor é Softcomp puro, não conhece impostos de venda).

## Risco / cuidados

- **Reset de ICMS/PIS/IPI no modo exportação** não pode vazar para modo BR se o vendedor trocar o toggle mid-proposta. Teste: alternar toggle ON → OFF → ON sem refresh e garantir que impostos voltam aos valores originais do item.
- **Modo exportação + Repasse importado simultâneo:** faz sentido? Se sim, custo nacionalizado da MP + impostos de saída zerados. Validar matematicamente que o landed factor da importação ainda funciona.
- **Clientes sem CNPJ**: o `propostaFromDOM` captura UF hoje como string. Precisa não quebrar se UF virar `country` (tratar fallback).
