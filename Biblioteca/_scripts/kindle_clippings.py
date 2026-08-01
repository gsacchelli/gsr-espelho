#!/usr/bin/env python3
"""Converte o My Clippings.txt do Kindle em uma nota por livro na Biblioteca.

O arquivo vive no próprio aparelho (documents/My Clippings.txt) e é texto puro —
sem DRM, sem login, sem depender da região da conta Amazon.

Uso:
    python3 kindle_clippings.py                      # procura o Kindle em /Volumes
    python3 kindle_clippings.py "/caminho/My Clippings.txt"

Roda quantas vezes quiser: destaque já existente na nota não é duplicado.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

DESTAQUES = Path(__file__).resolve().parent.parent / "Destaques"
SEPARADOR = "=========="

# O Kindle escreve o cabeçalho no idioma do aparelho. Cobrimos pt-BR e inglês.
TIPOS = {
    "destaque": "destaque",
    "highlight": "destaque",
    "nota": "nota",
    "note": "nota",
    "marcador": "marcador",
    "bookmark": "marcador",
}


def achar_clippings() -> Path | None:
    for volume in Path("/Volumes").glob("*"):
        candidato = volume / "documents" / "My Clippings.txt"
        if candidato.exists():
            return candidato
    return None


def ler(caminho: Path) -> str:
    # Kindle grava UTF-8 com BOM; alguns aparelhos antigos usam cp1252.
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return caminho.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"Não consegui decodificar {caminho}")


def separar_titulo_autor(linha: str) -> tuple[str, str]:
    """'Playing to Win (Lafley, A.G.)' -> ('Playing to Win', 'Lafley, A.G.')"""
    m = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", linha.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return linha.strip(), ""


def parse_meta(linha: str) -> dict:
    """Extrai tipo, página e localização do cabeçalho do trecho."""
    baixa = unicodedata.normalize("NFKD", linha.lower())
    baixa = "".join(c for c in baixa if not unicodedata.combining(c))

    tipo = "destaque"
    for chave, valor in TIPOS.items():
        if chave in baixa:
            tipo = valor
            break

    pagina = re.search(r"(?:pagina|page)\s+([\w-]+)", baixa)
    local = re.search(r"(?:localizacao|location)\s+([\d-]+)", baixa)
    return {
        "tipo": tipo,
        "pagina": pagina.group(1) if pagina else "",
        "local": local.group(1) if local else "",
    }


def parse(texto: str) -> dict[tuple[str, str], list[dict]]:
    livros: dict[tuple[str, str], list[dict]] = {}
    for bloco in texto.split(SEPARADOR):
        linhas = [ln.strip() for ln in bloco.strip().splitlines()]
        linhas = [ln for ln in linhas if ln]
        if len(linhas) < 2:
            continue

        titulo, autor = separar_titulo_autor(linhas[0])
        meta = parse_meta(linhas[1])
        conteudo = "\n".join(linhas[2:]).strip()

        if not conteudo or meta["tipo"] == "marcador":
            continue  # marcador não tem texto; não vira nota

        livros.setdefault((titulo, autor), []).append({**meta, "texto": conteudo})
    return livros


def nome_arquivo(titulo: str, autor: str) -> str:
    base = f"{titulo} — {autor}" if autor else titulo
    return re.sub(r'[/:\\|#^\[\]]', "-", base).strip()[:110] + " (destaques).md"


def render(titulo: str, autor: str, trechos: list[dict]) -> str:
    hoje = datetime.now().strftime("%Y-%m-%d")
    linhas = [
        "---",
        "tipo: destaques-kindle",
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
    for t in trechos:
        ref = " · ".join(
            p for p in (
                f"pág. {t['pagina']}" if t["pagina"] else "",
                f"loc. {t['local']}" if t["local"] else "",
            ) if p
        )
        rotulo = "Nota sua" if t["tipo"] == "nota" else "Destaque"
        linhas.append(f"### {rotulo}{' — ' + ref if ref else ''}")
        linhas.append("")
        if t["tipo"] == "nota":
            linhas.append(t["texto"])
        else:
            linhas.extend(f"> {ln}" for ln in t["texto"].splitlines())
        linhas.append("")
    return "\n".join(linhas)


def main() -> None:
    if len(sys.argv) > 1:
        origem = Path(sys.argv[1]).expanduser()
    else:
        achado = achar_clippings()
        if not achado:
            raise SystemExit(
                "Nenhum Kindle encontrado em /Volumes.\n"
                "Conecte o aparelho por USB (ele monta como disco) ou passe o "
                "caminho do My Clippings.txt como argumento."
            )
        origem = achado

    if not origem.exists():
        raise SystemExit(f"Arquivo não encontrado: {origem}")

    livros = parse(ler(origem))
    if not livros:
        raise SystemExit("Nenhum destaque reconhecido no arquivo.")

    DESTAQUES.mkdir(parents=True, exist_ok=True)
    for (titulo, autor), trechos in sorted(livros.items()):
        destino = DESTAQUES / nome_arquivo(titulo, autor)

        # Dedupe contra o que já está na nota: só conta o que é texto novo.
        anterior = destino.read_text(encoding="utf-8") if destino.exists() else ""
        novos = [t for t in trechos if t["texto"] not in anterior]
        if anterior and not novos:
            print(f"  = {destino.name} (nada novo)")
            continue

        destino.write_text(render(titulo, autor, trechos), encoding="utf-8")
        marca = "+" if anterior else "*"
        print(f"  {marca} {destino.name} ({len(trechos)} trechos, {len(novos)} novos)")

    print(f"\n{len(livros)} livro(s) em {DESTAQUES}")


if __name__ == "__main__":
    main()
