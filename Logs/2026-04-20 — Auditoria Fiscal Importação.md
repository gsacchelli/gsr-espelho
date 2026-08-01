---
tipo: log-auditoria
categoria: simulador / pricing / fiscal
domínio: importação
data: 2026-04-20
tags: [simulador, importação, fiscal, auditoria, pis, cofins, icms, ii, ipi, afrmm, lei-10865, lei-14973]
---

# 2026-04-20 — Auditoria Fiscal Importação

Auditoria completa da base legal de cada tributo e despesa da importação, provocada por uma sequência de erros meus na cascata fiscal que só foram capturados quando o Gustavo cobrou verificação em fontes primárias.

## Contexto do erro que deu origem à auditoria

No contexto da Camada 6c (cascata da importação), apliquei uma "correção" da base do PIS/Cofins-Importação de `VA` para `VA + II + IPI` baseada num código Python trazido pelo ChatGPT. O Gustavo cobrou verificação. Pesquisa em fontes oficiais (Receita Federal, PGFN, STF, Planalto) confirmou que a base correta é **apenas o Valor Aduaneiro** — a correção que apliquei era na verdade um bug.

Reversão aplicada + auditoria completa de todos os tributos para garantir que o motor esteja alinhado à legislação vigente.

## Tabela consolidada — base legal por tributo (validada 20/04/2026)

| Tributo | Base de cálculo | Alíquota padrão | Fórmula do motor | Status |
|---|---|---|---|---|
| **II** (Imposto de Importação) | **Valor Aduaneiro apenas** (AVA-GATT) | TEC — varia por NCM (default AFS 10,80%) | `II = VA × i` | ✅ correto |
| **IPI-Imp** | **VA + II** (art. 47, II, CTN) | TIPI — varia por NCM (aço 0%) | `IPI = (VA + II) × i` | ✅ correto |
| **PIS-Imp** | **VA apenas** | 2,10% | `PIS = VA × i` | ✅ correto (pós reversão) |
| **Cofins-Imp** | **VA apenas** | **9,65% base** (+ adicional escalonado para 17 setores desonerados) | `Cofins = VA × i` | ✅ correto |
| **ICMS-Imp** | VA + II + IPI + PIS + Cofins + AFRMM + despesas aduaneiras + **próprio ICMS (gross-up por dentro)** | Varia por UF (SP 18% padrão; 4% p/ importados em muitos casos) | `ICMS = baseSemICMS × i / (1−i)` | ✅ correto |
| **AFRMM** | **Frete marítimo** (remuneração do transporte aquaviário) | **25% longo curso** / 10% cabotagem / 40% granéis líquidos N-NE | `AFRMM = freteMarBRL × 25%` | ✅ correto |
| **Taxa Siscomex** | Valor fixo por DI + R$ 38,56 por adição até a 2ª | R$ 214,50 primeira DI | — | ⚠️ sem campo próprio no HTML (vai em "Portuárias") |

## Adicional da Cofins-Importação — NÃO se aplica a aços

A Lei 14.973/2024 prorrogou o adicional da Cofins-Importação com redução escalonada:

| Ano | Adicional | Cofins total |
|---|---|---|
| 2025 | +0,8 pp | 10,45% |
| **2026** | **+0,6 pp** | **10,25%** |
| 2027 | +0,4 pp | 10,05% |
| 2028+ | — | 9,65% |

**O adicional NÃO é universal.** Incide apenas sobre NCMs dos **17 setores desonerados da folha** (Lei 12.546/2011 — CPRB): confecção/vestuário, calçados, construção civil, call center, comunicação, couro, veículos, máquinas, proteína animal, têxtil, TI/TIC, circuitos integrados, transportes (metroferroviário, rodoviário coletivo e de cargas).

**Aços planos/longos/especiais (NCMs 7218–7228) NÃO estão na lista.** Cofins permanece **9,65%** para as importações da AFS.

**Observação crítica:** quando aplicável, o adicional **NÃO é creditável** (STF). Vira custo real, não passa pelos recuperáveis. Para NCMs da lista, o adicional aumenta o custo líquido efetivo.

## Impacto dos recuperáveis no custo líquido

Ponto que ficou claro na auditoria:

- **Alíquota base da Cofins (9,65%)**: 100% recuperável em RPA/lucro real com saídas tributadas. Entra no BRUTO, sai no LÍQUIDO via créditos. **Custo líquido não muda.**
- **Adicional da Cofins (se aplicável)**: NÃO creditável. **Aumenta o custo líquido real.**

Consequência prática: pra aços na AFS, o Cofins-Importação é **custo de fluxo de caixa**, não de resultado. O dinheiro fica imobilizado desde o DARF da DI até a compensação contra saídas futuras. O motor NÃO modela esse custo de capital imobilizado nos tributos recuperáveis (ICMS + PIS + Cofins pagos na DI) — é a lacuna 6b.1 já documentada.

## Correções aplicadas ao motor nesta sessão (20/04/2026)

Sequência de correções da cascata:

1. **VA não duplica frete marítimo** — CFR já inclui frete por INCOTERM. `VA = CFR_BRL + Seguro_BRL`. Frete marítimo permanece no modelo apenas como base do AFRMM.
2. **Base PIS/Cofins volta a ser apenas VA** — correção de erro meu que tinha aplicado base = VA+II+IPI. Fontes oficiais confirmam apenas VA.
3. **SELIC tratada como mensal** — campo `sim-selic` é % a.m. (label explícito). Motor antigo convertia de a.a. (errado, subestimava CF em ~12×).
4. **Landed factor usa câmbio operacional** — para casar com fórmula de precificação `CFR × câmbio_op × landed = custo`.
5. **Hedge % câmbio** — novo campo, default 0. Câmbio operacional = nominal × (1 + hedge/100).
6. **Breakdown reestruturado** — linhas "Base do ICMS-Importação" / "ICMS-Importação (por dentro)" / "Subtotal nacionalizado (com ICMS)" refletem a sequência fiscal real e fecham aritmeticamente.
7. **Coluna unitária no breakdown** — valor R$/T ou R$/Pç conforme cfr_unit.
8. **Créditos tributários recuperáveis** — nomenclatura contábil precisa, em vez de "Recuperáveis".

## Tooltips enciclopédicos adicionados ao HTML

Para documentar a base legal inline no simulador:

- **I.IMP**: "base VA (AVA-GATT). Alíquota TEC. Capatazia nacional integra o VA (STJ Tema 1014)."
- **IPI**: "base VA + II (art. 47, II, CTN). TIPI varia por NCM. Aço costuma ser 0%."
- **PIS-Imp**: "base APENAS VA (Lei 12.865/2013, art. 7º I da Lei 10.865/04; STF RE 559.937). 100% recuperável em RPA/lucro real com saídas tributadas."
- **Cofins-Imp**: "base APENAS VA. Alíquota base 9,65%. ATENÇÃO: produtos dos 17 setores desonerados sofrem adicional escalonado (2026: 10,25%). O adicional NÃO É CREDITÁVEL (STF). Aços NÃO sofrem adicional."

## Aprendizado estrutural

**Tributário exige verificação em fonte primária**, não "ChatGPT disse" ou "Python do blog diz". Erro fiscal no motor vira:
- Cotações erradas → margem comprometida
- Pagamento indevido de tributos → dinheiro perdido
- Risco de autuação quando há subestimação

Regra que adoto daqui pra frente: **toda alíquota/base/regime novo que o motor implementar passa por busca em Receita Federal + PGFN + Planalto antes de codar.** Blogs e LLMs viram referência secundária só pra ordenar a pesquisa.

## Sutilezas operacionais que vale lembrar

**1. Capatazia nacional e base do ICMS-Imp.** STJ Tema 1014 diz que capatazia integra o VA (e portanto o II). Mas a capatazia **nacional pós-desembaraço** não deveria entrar na base do ICMS-Importação (SP, RS consolidaram esse entendimento). Hoje o motor soma "Portuárias" no `baseSemICMS` sem distinguir — se o valor digitado tem capatazia nacional relevante, há leve superestimação de ICMS. Em geral o erro é pequeno; vale documentar como lacuna aceita.

**2. Taxa Siscomex não tem campo próprio.** Hoje vai em "Portuárias" (R$ absoluto). É tributo federal, não despesa portuária — mas pro cálculo do custo nacionalizado, somar tudo em "Portuárias" dá o mesmo resultado.

**3. Reforma Tributária do Consumo em curso.** Lei Complementar 224/2025 e Lei 14.973/2024 já iniciam transição CBS/IBS substituindo PIS/Cofins/ICMS. Motor usa regime atual; quando a transição avançar (2027-2033), vai precisar atualizar.

## Fontes consultadas (lista canônica para referência futura)

- [Lei 10.865/2004 (compilada) — Planalto](https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l10.865compilado.htm)
- [Lei 12.546/2011 — Planalto (CPRB / 17 setores)](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12546.htm)
- [Lei 14.973/2024 — Planalto (reoneração + Cofins-Imp escalonada)](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/lei/l14973.htm)
- [Receita Federal — II](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/tributos/imposto-importacao)
- [Receita Federal — IPI](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/tributos/ipi)
- [Receita Federal — AFRMM](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/tributos/afrmm)
- [Receita Federal — Taxa Siscomex](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/tributos/taxa-de-utilizacao-do-siscomex)
- [PGFN — PIS/Cofins-Importação](https://www.gov.br/pgfn/pt-br/cidadania-tributaria/por-assunto/pis-cofins-2/pis-cofins-importacao)
- [PGFN — Alteração de alíquotas Cofins-Imp no tempo](https://www.gov.br/pgfn/pt-br/cidadania-tributaria/por-assunto/indice-assuntos-portal/pis-cofins-2/aliquotas-pis-cofins-1/alteracao-de-aliquotas-no-tempo)
- [STF RE 559.937 Tema 1 RG — Dizer o Direito](https://buscadordizerodireito.com.br/jurisprudencia/9751/e-inconstitucional-a-parte-do-art-7o-i-da-lei-108652004-que-acresce-a-base-de-calculo-da-denominada-piscofins-importacao-o-valor-do-icms-incidente-no-desembaraco-aduaneiro-e-o-valor-das-proprias-contribuicoes)
- [STJ Tema 1014 — Capatazia integra base do II](https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/Servicos-de-capatazia-integram-base-de-calculo-do-Imposto-de-Importacao.aspx)
- [STJ — PIS e Cofins compõem base do ICMS (jan/2025)](https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Noticias/2025/22012025-Repetitivo-define-que-PIS-e-Cofins-compoem-base-de-calculo-do-ICMS-quando-esta-e-o-valor-da-operacao.aspx)
- [SEFAZ-RS — Base de cálculo do ICMS na importação](https://atendimento.receita.rs.gov.br/da-base-de-calculo-do-icms-na-importacao)
- [Machado Meyer — STF mantém adicional 1% Cofins-Imp e proíbe compensação](https://www.machadomeyer.com.br/pt/imprensa-ij/stf-mantem-adicional-de-1-a-cofins-importacao-e-proibe-compensacao)

## Conexões

- [[Logs/2026-04-20 — Camada 6c Pre-work]] — log da sessão técnica onde os bugs foram introduzidos e corrigidos
- [[Logs/2026-04-20 — Camada 6b Importação]] — implementação original do bloco Importação no HTML
- [[Sistema Operacional Comercial/02 Precificação/08 - Simulador HTML - Arquitetura]] — arquitetura
