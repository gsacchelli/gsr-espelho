# Corpus Técnico Local — normas ASTM, livros e a regra de citação

**Criado em 06/08/2026.** Resolve o defeito que apareceu num teste do Gustavo com o Stalo: perguntado sobre a **ASTM A668 classe MH**, o agente respondeu de memória, com tom de quem sabia, e errou tudo.

| | Stalo respondeu | A norma exige (A668/A668M-04, Tabela 2, ≤ 4″) |
|---|---|---|
| Tração mín. | 550 MPa | **1000 MPa** |
| Escoamento mín. | 275 MPa | **825 MPa** |
| Alongamento | 22% | **15%** |
| Redução de área | 35% | **45%** |

E inventou o conceito junto: disse que "MH" era *Medium Hardness*. O §7.3 da norma diz outra coisa — o sufixo **H** identifica o forjado fornecido **com certificação por ensaio de dureza apenas** ("AH", "BH", "CH"…). MH é a classe M certificada por dureza. Classe M, aliás, é aço **liga** (§1.3: seis classes de carbono A–F, sete de liga G–N).

Num certificado ou numa proposta técnica, esse erro vira recusa de lote.

## A causa: não era prompt, era falta de fonte

O acervo `~/Documents/Sacchelli/13. Data Base/15. Conhecimentos Gerais (IA)/` tem **1.902 normas ASTM** — inclusive a A668, em três cópias. Só que:

1. a pasta **não era `--add-dir`** de nenhum agente; e
2. mesmo que fosse, **PDF é binário** — `Grep` não acha nada dentro.

Sem fonte alcançável, LLM preenche a lacuna com o que lembra. É o comportamento esperado, não um bug do modelo.

> ⚠️ Vale para esta pasta também: **PDF depositado aqui não é pesquisável.** O `00 - Leia-me` prometia que "basta salvar o arquivo aqui". Isso vale para `.md`; para PDF, ou você transcreve o trecho, ou deposita no acervo e roda o extrator (abaixo).

## O que existe agora

**Corpus:** `~/.afs_agente/conhecimento/` — texto puro extraído do acervo, com marcas `[[pág. N]]` para citação.

| Conteúdo | Números |
|---|---|
| Normas ASTM com texto | **1.818 arquivos · 928 designações distintas** |
| Livro *Aços e Ligas Especiais* (Costa e Silva & Mei) | 512 pgs, via OCR — ver `[[05 - Aços e Ligas Especiais (Costa e Silva & Mei) — mapa do livro]]` |
| Apostila *Tecnologia dos Materiais* (SENAI-SP/CPTM 2010) | 197 pgs — ver `[[06 - Tecnologia dos Materiais (SENAI-SP) — escopo e sobreposição]]` |

**Dois índices, que são a porta de entrada:** `_INDICE_NORMAS.md` (designação → edição → título → arquivo) e `_INDICE_ACERVO.md` (livros, apostilas e as lacunas conhecidas).

**Onde mora e por quê:** sob `~/.afs_agente/` (o cwd do Flori), **fora do repo git e fora do iCloud**. É material de terceiro protegido — não pode ser versionado, sincronizado nem republicado. O vault público `ConhecimentosGerais`, que espelha para o VPS do Stalo, continua recebendo **só síntese escrita por nós**.

**Ferramentas** (no repo, re-rodáveis a cada depósito novo no acervo):
- `MotorAnalitico/conhecimento/extrair_corpus.py` — PDF/docx/xlsx/htm → texto, com OCR (tesseract) para scan puro
- `MotorAnalitico/conhecimento/gerar_indice.py` — regera os dois índices
- Atalho: `make conhecimento`

## A regra de citação (está no prompt do Flori, e é testada)

Para **requisito de norma** — composição, tração, dureza, tolerância, critério de aceitação, classe:

1. Grep no `_INDICE_NORMAS.md` pela designação;
2. abrir o `.txt` e **ler** a tabela;
3. responder citando **designação + edição + página**;
4. **não acrescentar atributo que não leu** (tipo de aço, tratamento, aplicação, sentido de sufixo);
5. **não achou → dizer que não temos a norma.** Nunca preencher com valor lembrado.

Para **conceito**: base pública → livro Costa e Silva & Mei → apostila SENAI → norma, quando virar requisito. **Apostila não sobrepõe livro; livro não sobrepõe norma em matéria de requisito.**

`test_agente_llm.py` reprova se essa regra sumir do prompt ou se o corpus sair do `--add-dir` — regra que vive só em prompt é regra que evapora numa refatoração.

## Lacunas conhecidas (não inventar o que falta)

- **63 normas com arquivo de 0 byte** na origem (download que falhou): A123, A153, A653, A123/A153 e a família de galvanização/revestido em geral. Fora do nosso miolo (barra e forjado), mas é lacuna real — lista completa no `_INDICE_ACERVO.md`.
- **A série E (métodos de ensaio) está quase toda ausente** — só 10 arquivos. Faltam **E8/E8M** (tração), **E18** (Rockwell), **E10** (Brinell), **E112** (tamanho de grão), **E45** (inclusões), **E381** (macroataque), **E709/E1444** (partículas magnéticas), **E165/E1417** (líquido penetrante). O acervo é dos volumes 01.xx (produtos siderúrgicos), não do 03.01 (ensaios). Temos a **A370** (mecânicos, que referencia as E) e, em ultrassom, **A388** (forjados), **A578** (chapa) e **A745** (forjado austenítico) — o essencial de UT está coberto; o de laboratório, não.
- **Edições envelhecidas**: a cópia mais nova da A668 é de **2004**. Toda citação declara a edição e avisa que pode haver revisão.

## Ligações

`[[dicionario-de-fontes]]` · `[[auditoria-e-inegociavel]]` · `[[guardas-de-analise]]` — mesma família de problema: número que chega à tela com cara de fato sem ter fonte que o sustente.
