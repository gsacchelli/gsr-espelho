# Destaques — pasta de sincronização

Esta pasta é **escrita pelo script `_scripts/kindle_clippings.py`**, que lê o `My Clippings.txt` do Kindle. Uma nota por livro, com os trechos que você destacou e suas notas de margem.

## Regras

**Não editar à mão.** O import é incremental e reescreve a nota do livro — edição manual se perde. Reflexão sua vai na síntese, em `Biblioteca/Título — Autor.md`.

**Conteúdo aqui é obra do autor.** Trecho literal de livro comprado: uso pessoal, referência para a sua síntese. Não vai para o `ConhecimentosGerais`, não vai para o repo `conhecimentos-gerais`, não sai do GSR.

**É fonte, não é resposta.** Quando o Flori for perguntado sobre um livro, a resposta boa vem da síntese; daqui vem só a citação exata quando você pedir "qual foi a frase".

## Formato que o script escreve

Frontmatter com título, autor, data do import e total de trechos; depois cada destaque em citação (`>`) com página e localização, e as suas notas de margem em texto normal — para separar à vista o que é do autor e o que é seu.

Colar aqui manualmente o export de `leia.amazon.com.br/notebook` funciona igual — mesmo lugar, mesma regra.
