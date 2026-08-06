# Villares Metals — catálogo de construção mecânica e apostila de tratamento térmico

**Depositados em 06/08/2026.** Dois documentos do mesmo fabricante, com valor e confiabilidade **muito diferentes**. Leia a ressalva de cada um antes de usar.

## 1. Apostila *Tratamentos Térmicos dos Aços* — Rômulo Fernandes Moreno (Eng. de Produto, Laminados)

28 páginas, camada de texto (não precisou de OCR). `Técnico/Apostilas/`.

**Veredito: confere com o que já temos, e é a melhor porta de entrada rápida do assunto.**

Conferido ponto a ponto contra o `[[05 - Aços e Ligas Especiais (Costa e Silva & Mei) — mapa do livro]]`: **nenhum conflito**. Diagrama Fe-C com 2,11% C a 1148 °C e eutetóide a 727 °C, dureza da martensita função só do %C com máximo em 0,8%, austenita retida transformando no primeiro revenimento e exigindo o segundo, endurecimento secundário por precipitação de carbonetos de liga — tudo igual ao livro, em versão condensada.

O que ela **acrescenta** é forma, não conteúdo: 28 páginas em português de usina, com as reações químicas da cementação em caixa escritas, e uma seção nomeada de **sub-zero** que no livro está diluída dentro de "austenita retida". Serve para explicação rápida e para redigir resposta a cliente.

| Onde está | Pág. |
|---|---|
| Definições (fases, constituintes) | 6 |
| Curvas TTT e TRC | 14 |
| Recozimento · Normalização | 17 |
| **Têmpera e revenimento** | 19 |
| Martêmpera · Austêmpera | 22 |
| Endurecimento por precipitação · **Sub-zero** | 23 |
| **Termoquímicos** (cementação, nitretação, carbonitretação, boretação) | 24 |

**O que NÃO cobre:** temperabilidade quantitativa (Jominy, Grossmann, DI), seleção de aço, ensaios, critério de aceitação. Para isso: livro (cap. 3.6) e norma (A255 para Jominy).

**Precedência:** é apostila de fabricante. Abaixo do livro em conceito; abaixo da norma em requisito. Em divergência, o livro manda.

## 2. Catálogo *Aços para Construção Mecânica — Aços para Beneficiamento*

65 páginas, **scan puro → OCR**. `Técnico/Catalogos de Fabricante/`. **4ª edição, 1992** — 34 anos.

**⚠️ Veredito: entra com ressalva dura — os números dele NÃO são confiáveis.**

O catálogo é feito de **tabelas de composição, curvas Jominy e curvas de revenimento**. É exatamente o tipo de conteúdo que o OCR destrói: `0,60` saiu `O60`, e os eixos dos gráficos viraram sequências como `2 4 6 B 10 12 14 16 18 20 22 24 26 28 3032`. **Curva de gráfico não é extraível por OCR — ponto.**

Ou seja: o documento cujo valor inteiro está nos números entrou no corpus com os números corrompidos, e legíveis o bastante para enganar. Por isso ele carrega uma **`⚠ RESSALVA` no cabeçalho do próprio texto** (`config/conhecimento_ressalvas.yaml`), instruindo a nunca citar composição, dureza ou curva sem conferir a página original.

**Para que ele ainda serve:** saber **que aços existem** na linha e **que tratamentos o fabricante recomenda**. O mapa comercial↔ABNT é o achado aproveitável:

- **VB-30/40/50/60** e **VR-35/40/50/60** — as duas famílias principais de beneficiamento
- **VN-50 · VS-60 · VC-52 · VL-30/40 · VM-40**
- ABNT cobertos: **4130, 4140, 4340, 5135, 5140, 5150, 5160, 5210, 6150, 8630, 8640, 8650, 8660**

Traz também curvas de **limite de fadiga** (superfície polida × retificada) e **severidade de têmpera H** por diâmetro de barra — conceitualmente úteis, numericamente não confiáveis aqui.

**Duas ressalvas além do OCR:**
1. É **catálogo de fabricante**: valor típico e indicativo, **não requisito**. Requisito é norma.
2. É de **1992** (4ª edição) — logo "VILLARES", não "Villares Metals". As designações VB-xx/VR-xx são daquela época e podem não existir na linha atual; o cliente que citar uma delas pode estar lendo um documento tão velho quanto este. O mapa marca↔ABNT é a parte que envelhece menos.

> A data foi achada pelo **Flori, na etapa 6**: eu tinha escrito "sem data" nesta nota e no nome do arquivo, e ele leu `4º EDIÇÃO 1992` na pág. 3. Conferido no texto e corrigido — inclusive o nome do arquivo no acervo. É o segundo erro meu que a etapa da prova pega (o primeiro foi a régua do MBA).

**Se esse catálogo importa de verdade**, o caminho não é OCR melhor: é **transcrever à mão as tabelas dos aços que a gente realmente vende** para um `.md`. Meia dúzia de linhas de composição resolve mais que 65 páginas de ruído.

## O que isso mudou no sistema

Nasceu daqui o mecanismo de **ressalva por documento** (`config/conhecimento_ressalvas.yaml`): aviso que entra no cabeçalho do `.txt` e viaja junto com o texto. Sem ele, extrair texto passaria por extrair conhecimento — e o agente citaria `O60` como composição química com toda a confiança do mundo. O Mini Anuário do Aço Brasil já precisava do mesmo tratamento, e recebeu.

Ver `[[04 - Corpus Técnico Local (normas ASTM, livros) — mapa e regras]]`.
