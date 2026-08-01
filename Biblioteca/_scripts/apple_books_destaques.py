#!/usr/bin/env python3
"""Extrai destaques do Apple Books para a Biblioteca do vault.

O Apple Books guarda as anotações num SQLite local, fora do arquivo do livro —
ler daqui não toca no DRM nem no conteúdo protegido, só nas SUAS marcações.

Uso:
    python3 apple_books_destaques.py            # todos os livros com destaque
    python3 apple_books_destaques.py --listar    # só lista o que existe
    python3 apple_books_destaques.py "Fifer"     # filtra por título/autor
"""

from __future__ import annotations

import re
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

DESTAQUES = Path(__file__).resolve().parent.parent / "Destaques"
CONTAINER = Path.home() / "Library/Containers/com.apple.iBooksX/Data/Documents"
ANOTACOES = CONTAINER / "AEAnnotation"
BIBLIOTECA = CONTAINER / "BKLibrary"

# Core Data conta segundos a partir de 2001-01-01.
EPOCA_APPLE = datetime(2001, 1, 1)

# Convenção de cores (ver "00 - Método de Leitura e Síntese").
# O código do estilo é do Apple Books; o significado é nosso.
CORES = {
    0: ("sublinhado", "Sublinhado"),
    1: ("aplicavel", "Aplicável à AFS"),
    2: ("dado", "Dado / número"),
    3: ("central", "Ideia central"),
    4: ("discordo", "Discordo"),
    5: ("metodo", "Método / framework"),
}


def copiar_para_temp(pasta: Path, padrao: str, destino: Path) -> Path:
    """Copia o .sqlite junto com -wal/-shm: o Books deixa escrita pendente no WAL."""
    bancos = sorted(pasta.glob(padrao))
    if not bancos:
        raise SystemExit(f"Banco não encontrado em {pasta}")
    principal = bancos[0]
    for arquivo in pasta.glob(principal.name + "*"):
        shutil.copy2(arquivo, destino / arquivo.name)
    return destino / principal.name


def carregar(temp: Path) -> list[dict]:
    anot = copiar_para_temp(ANOTACOES, "AEAnnotation*.sqlite", temp)
    libr = copiar_para_temp(BIBLIOTECA, "BKLibrary*.sqlite", temp)

    con = sqlite3.connect(f"file:{anot}?mode=ro", uri=True)
    con.execute(f"ATTACH DATABASE 'file:{libr}?mode=ro' AS lib")
    con.row_factory = sqlite3.Row

    linhas = con.execute(
        """
        SELECT  l.ZTITLE                     AS titulo,
                l.ZAUTHOR                    AS autor,
                a.ZANNOTATIONSELECTEDTEXT    AS texto,
                a.ZANNOTATIONNOTE            AS nota,
                a.ZFUTUREPROOFING5           AS capitulo,
                a.ZANNOTATIONSTYLE           AS estilo,
                a.ZANNOTATIONCREATIONDATE    AS criado
        FROM    ZAEANNOTATION a
        JOIN    lib.ZBKLIBRARYASSET l ON l.ZASSETID = a.ZANNOTATIONASSETID
        WHERE   a.ZANNOTATIONSELECTEDTEXT IS NOT NULL
          AND   IFNULL(a.ZANNOTATIONDELETED, 0) = 0
        ORDER BY l.ZTITLE, a.ZPLABSOLUTEPHYSICALLOCATION, a.ZANNOTATIONCREATIONDATE
        """
    ).fetchall()
    con.close()
    return [dict(r) for r in linhas]


def nome_arquivo(titulo: str, autor: str) -> str:
    base = f"{titulo} — {autor}" if autor and autor != "UnknownAuthor" else titulo
    return re.sub(r'[/:\\|#^\[\]]', "-", base).strip()[:110] + " (destaques).md"


def render(titulo: str, autor: str, trechos: list[dict]) -> str:
    hoje = datetime.now().strftime("%Y-%m-%d")
    linhas = [
        "---",
        "tipo: destaques-apple-books",
        f'titulo: "{titulo}"',
        f'autor: "{autor}"',
        f"sincronizado_em: {hoje}",
        f"total: {len(trechos)}",
        "---",
        "",
        f"# {titulo}" + (f" — {autor}" if autor else ""),
        "",
        "> Trechos literais do livro (obra do autor). Fonte para a síntese em "
        "`Biblioteca/`; não publicar, não sair do GSR.",
        "",
    ]
    capitulo_atual = None
    for t in trechos:
        if t.get("capitulo") and t["capitulo"] != capitulo_atual:
            capitulo_atual = t["capitulo"]
            linhas += [f"## {capitulo_atual}", ""]
        _, rotulo = CORES.get(t.get("estilo"), ("", ""))
        selo = f"`{rotulo}`" if rotulo else ""
        if t.get("criado"):
            quando = (EPOCA_APPLE + timedelta(seconds=t["criado"])).strftime("%Y-%m-%d")
            selo = f"{selo} · *{quando}*" if selo else f"*{quando}*"
        if selo:
            linhas.append(selo)
        linhas += [f"> {ln}" for ln in (t["texto"] or "").strip().splitlines()]
        if t.get("nota"):
            linhas += ["", f"**Nota sua:** {t['nota'].strip()}"]
        linhas.append("")
    return "\n".join(linhas)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    filtro = args[0].lower() if args else None

    with tempfile.TemporaryDirectory() as tmp:
        registros = carregar(Path(tmp))

    livros: dict[tuple[str, str], list[dict]] = {}
    for r in registros:
        chave = (r["titulo"] or "Sem título", r["autor"] or "")
        if filtro and filtro not in " ".join(chave).lower():
            continue
        livros.setdefault(chave, []).append(r)

    if not livros:
        raise SystemExit("Nenhum destaque encontrado" + (f" para '{filtro}'" if filtro else "."))

    if "--listar" in sys.argv:
        for (titulo, autor), trechos in sorted(livros.items(), key=lambda x: -len(x[1])):
            print(f"  {len(trechos):4d}  {titulo} — {autor}")
        return

    DESTAQUES.mkdir(parents=True, exist_ok=True)
    for (titulo, autor), trechos in sorted(livros.items()):
        destino = DESTAQUES / nome_arquivo(titulo, autor)
        destino.write_text(render(titulo, autor, trechos), encoding="utf-8")
        print(f"  * {destino.name} ({len(trechos)} trechos)")

    print(f"\n{len(livros)} livro(s) em {DESTAQUES}")


if __name__ == "__main__":
    main()
