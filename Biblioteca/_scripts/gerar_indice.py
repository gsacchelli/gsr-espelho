#!/usr/bin/env python3
"""Regenera o índice da Biblioteca a partir do frontmatter das sínteses.

O índice existe para governança: mostra de relance qual nota é confiável e qual
está apoiada em fonte fraca. Nota sem proveniência declarada aparece marcada.

Uso:
    python3 gerar_indice.py
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

BIBLIOTECA = Path(__file__).resolve().parent.parent
INDICE = BIBLIOTECA / "00 - Índice da Biblioteca.md"

ROTULO_FONTE = {
    "livro-completo": "📖 livro completo",
    "destaques+publico": "📑 destaques + público",
    "destaques": "📑 destaques",
    "material-publico": "🌐 material público",
}


def frontmatter(texto: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", texto, re.DOTALL)
    if not m:
        return {}
    dados = {}
    for linha in m.group(1).splitlines():
        if ":" in linha and not linha.startswith(" "):
            chave, _, valor = linha.partition(":")
            dados[chave.strip()] = valor.strip().strip('"')
    return dados


def main() -> None:
    linhas = [
        "# Índice da Biblioteca",
        "",
        f"*Regenerado em {datetime.now().strftime('%Y-%m-%d')} por `_scripts/gerar_indice.py`.*",
        "",
        "A coluna **Fonte** é o que decide o quanto confiar na nota: síntese de material",
        "público descreve o framework do autor, não a leitura do Gustavo.",
        "",
        "| Livro | Autor | Fonte | Cobertura |",
        "|---|---|---|---|",
    ]

    encontrados = 0
    for arquivo in sorted(BIBLIOTECA.glob("*.md")):
        if arquivo.name.startswith(("00 - ", "TEMPLATE")):
            continue
        fm = frontmatter(arquivo.read_text(encoding="utf-8"))
        if fm.get("tipo") != "livro":
            continue
        encontrados += 1
        fonte = ROTULO_FONTE.get(fm.get("fonte", ""), "⚠️ não declarada")
        cobertura = fm.get("cobertura_da_fonte", "—")
        if len(cobertura) > 90:
            cobertura = cobertura[:87] + "…"
        linhas.append(
            f"| [[{arquivo.stem}]] | {fm.get('autor', '—')} | {fonte} | {cobertura} |"
        )

    if not encontrados:
        linhas.append("| *nenhuma síntese ainda* | | | |")

    linhas += [
        "",
        "---",
        "",
        "## Como ler a coluna Fonte",
        "",
        "- **📖 livro completo** — leitura do texto inteiro (EPUB/PDF sem DRM). Confiança máxima.",
        "- **📑 destaques** — só o que Gustavo marcou lendo. Traz a hierarquia dele; não cobre o livro todo.",
        "- **🌐 material público** — framework reconstruído de fontes públicas do autor. **Não é a leitura do livro.**",
        "- **⚠️ não declarada** — frontmatter incompleto; tratar como não auditável até corrigir.",
        "",
        "## Conexões",
        "- [[00 - Método de Leitura e Síntese]]",
        "- [[00 - Leia-me (Biblioteca)]]",
    ]

    INDICE.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"  * {INDICE.name} ({encontrados} livro(s))")


if __name__ == "__main__":
    main()
