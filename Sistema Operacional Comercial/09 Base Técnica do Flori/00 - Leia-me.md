# Base Técnica do Flori

Pasta de conhecimento técnico que o Flori (agente Telegram) lê pra responder dúvidas de metalurgia, normas, conversões e catálogo. **Basta salvar o arquivo `.md` aqui** — o Flori enxerga automaticamente na próxima pergunta, sem precisar avisar ninguém.

> ⚠️ **PDF salvo aqui NÃO é pesquisável** (corrigido em 06/08/2026 — esta linha prometia que sim). PDF é binário: o `Grep` do agente não acha nada dentro, e o resultado prático é ele responder de memória achando que consultou. Para PDF há dois caminhos: **(a)** transcrever num `.md` o trecho que importa, ou **(b)** depositar em `~/Documents/Sacchelli/13. Data Base/15. Conhecimentos Gerais (IA)/` e rodar `make conhecimento`, que extrai o texto para o corpus do Flori. Ver `[[04 - Corpus Técnico Local (normas ASTM, livros) — mapa e regras]]`.

> **Divisão com o vault ConhecimentosGerais (desde 31/07/2026):** conhecimento **público e sem risco** (conversões, equivalências, resumos de norma) vive no vault `ConhecimentosGerais` — o Flori lê os dois, mas SÓ o público chega ao Stalo/VPS. Aqui na Base Técnica fica o que é interno ou protegido: PDFs integrais de normas (direito autoral), catálogos com custo/preço, fichas com informação comercial. Regra completa no `00 - Leia-me` do ConhecimentosGerais.

## O que colocar aqui

- **Normas** (ABNT/NBR, SAE, DIN, ASTM) — resumos em md ou o PDF direto
- **Catálogos Sacchelli** — linha de produtos, bitolas, comprimentos, tolerâncias
- **Tabelas de conversão** — já semeadas em `01` e `02`
- **Fichas técnicas de aços** — composição química, tratamento térmico, aplicações

## Convenções

- Nome de arquivo descritivo (o Flori acha por busca): `Norma NBR NM 87 - Aços Carbono.pdf`, `Catalogo Sacchelli 2026.pdf`
- Conteúdo em `.md` é mais confiável que PDF pra busca por texto — quando der, prefira transcrever o trecho que importa
- Correção de erro em tabela semeada: edita direto, o Flori lê a versão atual

## Aviso que o Flori carrega

Equivalências de aço e propriedades são **aproximadas/típicas** — aplicação crítica exige confirmar a norma específica com o cliente. Regra fiscal/tributária NUNCA sai daqui: só de fonte primária (Receita/Planalto), conforme política da casa.
