#!/usr/bin/env python3
"""Manda o trecho da área de transferência para a nota de destaques de um livro.

Serve para o que o destaque nativo não alcança: livro em que a marcação é ruim,
página que você quer discutir, trecho lido no app do celular. O texto vem do
Live Text do macOS (selecione direto na captura de tela e copie).

Uso:
    python3 capturar_trecho.py "Coragem"                    # tipo central (padrão)
    python3 capturar_trecho.py "Coragem" --aplicavel        # verde: aplica à AFS
    python3 capturar_trecho.py "Coragem" --discordo -n "não vale p/ B2B industrial"

Tipos: --central --aplicavel --discordo --dado --metodo
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

DESTAQUES = Path(__file__).resolve().parent.parent / "Destaques"

TIPOS = {
    "--central": "Ideia central",
    "--aplicavel": "Aplicável à AFS",
    "--discordo": "Discordo",
    "--dado": "Dado / número",
    "--metodo": "Método / framework",
}

# Trecho longo demais deixa de ser citação e vira cópia. O limite é deliberado:
# para o livro inteiro, a rota é comprar o EPUB sem DRM.
LIMITE_CARACTERES = 1500


def clipboard() -> str:
    return subprocess.run(["pbpaste"], capture_output=True, text=True).stdout.strip()


def achar_nota(busca: str) -> Path:
    candidatos = [p for p in DESTAQUES.glob("*.md")
                  if busca.lower() in p.stem.lower() and not p.stem.startswith("00 -")]
    if not candidatos:
        raise SystemExit(
            f"Nenhuma nota em Destaques/ casa com '{busca}'.\n"
            f"Rode antes o apple_books_destaques.py, ou crie a nota do livro."
        )
    if len(candidatos) > 1:
        nomes = "\n  ".join(p.stem for p in candidatos)
        raise SystemExit(f"'{busca}' casa com mais de uma nota:\n  {nomes}")
    return candidatos[0]


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        raise SystemExit(__doc__)

    tipo = next((TIPOS[f] for f in sys.argv[1:] if f in TIPOS), "Ideia central")
    nota_manual = ""
    if "-n" in sys.argv:
        i = sys.argv.index("-n")
        if i + 1 < len(sys.argv):
            nota_manual = sys.argv[i + 1]

    texto = clipboard()
    if not texto:
        raise SystemExit("Área de transferência vazia. Copie o trecho antes.")
    if len(texto) > LIMITE_CARACTERES:
        raise SystemExit(
            f"Trecho com {len(texto)} caracteres — acima do limite de {LIMITE_CARACTERES}.\n"
            "Isso deixou de ser citação. Para o livro inteiro, compre o EPUB sem DRM."
        )

    destino = achar_nota(args[0])
    if texto in destino.read_text(encoding="utf-8"):
        raise SystemExit(f"Esse trecho já está em {destino.name}.")

    bloco = [
        "",
        f"`{tipo}` · *{datetime.now().strftime('%Y-%m-%d')}* · captura manual",
        *[f"> {ln}" for ln in texto.splitlines() if ln.strip()],
    ]
    if nota_manual:
        bloco += ["", f"**Nota sua:** {nota_manual}"]
    bloco.append("")

    with destino.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(bloco))
    print(f"  + {destino.name} ({tipo}, {len(texto)} caracteres)")


if __name__ == "__main__":
    main()
