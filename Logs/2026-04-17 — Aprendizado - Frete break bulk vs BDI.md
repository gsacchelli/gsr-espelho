---
tipo: aprendizado
categoria: parâmetros-de-mercado
classificação: acerto-processo / erro-evitado
data: 2026-04-17
tags: [aprendizado, metalm, frete, parâmetros, pricing]
---

# 2026-04-17 — Aprendizado: Frete break bulk China→SFS — fonte correta vs BDI

## Contexto

Durante estudo de viabilidade da MetalM (parceria Duferco/DITH), foi necessário estimar o **custo de frete internacional** para compor o custo do aço importado e avaliar competitividade.

A referência "padrão" usada inicialmente foi o **Baltic Dry Index (BDI)** — índice público, amplamente citado em mídia financeira, aparente proxy de mercado para frete a granel.

Resultado: número batido com a realidade do mercado estava **~50% abaixo** do praticado para o trade **break bulk China → Santos/SFS** com aços especiais.

---

## O que aconteceu

- Cotação inicial baseada em BDI: ~**USD 55/mt**
- Cotação real de armadores + validação com trading (Duferco/DITH): **USD 110/mt**
- Erro de ~50% para baixo no cálculo de custo CIF

Impacto se tivesse sido usado na decisão:
- Margem operacional estimada da MetalM **sobrestimada em ~7-10 p.p.**
- Preço de venda projetado **abaixo do competitivo real**
- Tese de viabilidade financeira passaria falso positivo

---

## Foi erro ou acerto?

**Acerto por processo de validação** (ou erro evitado).

O uso inicial do BDI era razoável em primeira aproximação — é fonte pública, disponível, tratada como referência em muitos contextos. **A validação cruzada com armador real e trading parceira** é o que evitou o erro tornar-se estrutural no modelo.

Sem a validação, a tese MetalM teria rodado meses com premissa errada.

---

## Por quê? (causa raiz)

**BDI não é proxy válido para break bulk de aços especiais rota China→BR** por 3 razões estruturais:

1. **BDI mede seco a granel** (minério, carvão, grãos) em navios grandes
   - Aços especiais vão em **break bulk** (carga unitizada, navio específico)
   - Estruturas de custo e oferta/demanda muito diferentes

2. **BDI reflete médias globais** de rotas principais (Cape size, Panamax)
   - Rotas específicas (China-Santos com porto intermediário) têm **prêmio de rota** não capturado

3. **Natureza da carga altera preço**
   - Aço especial exige cuidados de estiva e manuseio
   - Seguro e risco diferentes de commodities soltas

Lição estrutural: **índice público genérico ≠ preço aplicável**. Válido como referência direcional, nunca como input de modelo financeiro de decisão.

---

## Aprendizado

**Regra 1 — Sobre premissas de modelo:** toda premissa de custo com **impacto ≥ 5% na margem estimada** deve ser validada com **pelo menos 2 fontes independentes do mercado real** antes de virar input de decisão.

**Regra 2 — Sobre índices públicos:** índice público é bom para direção (subindo? caindo?), ruim para nível (qual o valor praticado hoje no meu trade?). Usar nível absoluto sem validação é armadilha.

**Regra 3 — Sobre validação cruzada em B2B industrial:** sempre que possível, **perguntar a quem opera**, não a quem publica. Armador, trader, despachante, operador portuário conhecem o preço real. Publicações conhecem médias.

**Regra 4 — Sobre MetalM especificamente:** premissas logísticas (frete internacional, frete interno, armazenagem, desembaraço) devem ser **revalidadas trimestralmente** no modelo — são voláteis e assimétricas.

---

## Aplicação futura

- No modelo financeiro MetalM: **USD 110/mt** como premissa base para break bulk China→SFS (atualizar trimestralmente via cotação direta com Duferco/armador)
- No simulador de precificação Sacchelli: revisar parâmetros de frete internacional se aplicável
- **Hábito geral:** para qualquer número que entra em modelo de decisão estratégica, anotar **fonte + data + margem de erro estimada**. Se a margem de erro > 20%, tratar como hipótese a validar, não como fato
- Aplicar o mesmo padrão de validação a outras premissas MetalM: frete interno, preço de aço FOB, custo de corte terceirizado, taxa de armazenagem, custo de capital

---

## Conexão com outras verdades

Este aprendizado reforça uma regra da minha [[Sistema de Decisão - C-Level]]: **não esperar informação perfeita, mas separar opinião de fato**. BDI parecia fato — era opinião médio-global sem aplicação ao caso específico.

Também conecta com [[Finanças Corporativas]]: premissas mal calibradas distorcem NPV e IRR. Uma única premissa com erro de 50% pode transformar projeto atrativo em dinheiro jogado fora.

---

## Frameworks aplicados
- [[Aprendizados]] — estrutura de registro
- [[Sistema de Decisão - C-Level]] — princípio "separar opinião de fato"
- [[Finanças Corporativas]] — sensibilidade de modelo a premissas
- [[Hipóteses de Negócio]] — tratar premissas como hipóteses se têm alto impacto

## Conexões
- [[Aprendizados]] (hub)
- [[Ecossistema e Parcerias]] — relação com Duferco como fonte de validação
