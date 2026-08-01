# 📚 Biblioteca — leitura que vira decisão

Pasta de livros lidos. A regra é uma só: **destaque bruto e síntese própria são coisas separadas e moram em arquivos diferentes.**

```
Biblioteca/
├── 00 - Leia-me (Biblioteca).md    ← esta nota
├── TEMPLATE - LIVRO.md             ← modelo da síntese
├── _scripts/kindle_clippings.py    ← importa os destaques do aparelho
├── Destaques/                      ← ESCRITO PELO SCRIPT, não editar à mão
│   └── Título — Autor (destaques).md ← trechos literais do Kindle + notas suas
└── Título — Autor.md               ← SUA síntese (é o que o Flori usa)
```

---

## Por que duas notas por livro

**`Destaques/Título — Autor.md`** é matéria-prima: trecho literal do livro, palavra do autor, sincronizado da Amazon. Não é seu texto. Fica aqui como fonte para consulta e citação — nunca é publicado, nunca sai do GSR.

**`Título — Autor.md`** (raiz da Biblioteca) é a síntese escrita por você: tese do autor com suas palavras, o que se aplica à AFS/MetalM, onde você discorda. Esse é o texto que tem valor de decisão e que o Flori deve encontrar quando você perguntar "o que aquele livro dizia sobre X".

Quem lê o vault (você daqui a um ano, o Flori) precisa saber, sem esforço, se está lendo o autor ou lendo você. A separação de arquivos garante isso melhor do que qualquer convenção de formatação.

---

## O que NUNCA vai para o `ConhecimentosGerais`

Trecho literal de livro é obra de terceiro. O `ConhecimentosGerais` sincroniza para o VPS por git e é público na prática — **publicado = visto pra sempre**. Então:

| Conteúdo | Onde vive |
|---|---|
| Destaque literal do Kindle | **só** `GSR/Biblioteca/Destaques/` |
| Sua síntese com conteúdo AFS (preço, cliente, margem, estratégia) | **só** `GSR/Biblioteca/` |
| Sua síntese puramente técnica e universal, sem citação literal | pode subir ao `ConhecimentosGerais` — passando pelas duas perguntas do Leia-me de lá |

Na dúvida, fica no GSR. Mover privado → público depois é grátis; o contrário é impossível.

---

## Como os destaques chegam aqui

O Kindle grava tudo que você destaca num arquivo de texto puro **dentro do próprio aparelho**: `documents/My Clippings.txt`. Sem DRM, sem login, sem depender da região da conta Amazon — é a rota mais confiável, e é a que usamos.

1. Conectar o Kindle no Mac por **USB** (ele monta como disco em `/Volumes`).
2. Rodar:

```bash
python3 "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/GSR/Biblioteca/_scripts/kindle_clippings.py"
```

O script acha o aparelho sozinho, escreve uma nota por livro em `Destaques/` e é incremental — rodar de novo não duplica trecho que já está lá. Se o Kindle não estiver montado, dá para passar o caminho do `My Clippings.txt` como argumento.

**Por que não o plugin do Obsidian** (testado e descartado em 01/08/2026): o `Kindle Highlights` só conversa com `read.amazon.com`, `.ca`, `.co.uk`, `.co.jp` e `.in` — não tem região Brasil. Com conta `amazon.com.br` o login não entrega a biblioteca.

**Rota alternativa, sem cabo:** `leia.amazon.com.br/notebook` no navegador → copiar → colar em `Destaques/`. Serve para livro lido no app do celular, cujos destaques não passam pelo aparelho.

---

## O ciclo

Ler → destacar no Kindle → sync → **escrever a síntese** (é aqui que o livro vira ativo; destaque parado não decide nada) → linkar aos conceitos do vault (`[[Pricing - Precificação]]`, `[[Playing to Win]]`…) → o que virou decisão real desce para `Logs/`.

---

## Conexões
- [[Home]]
- [[Aprendizados]] — o que o livro mudou na prática vira princípio aqui
- [[Decisões C-Level]] — se a leitura destravou uma decisão, ela é registrada lá
