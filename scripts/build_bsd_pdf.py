"""Build the elliptic-curves textbook PDF from the Web chapter sources."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = ROOT / "elliptic-curves-bsd"
BUILD_ROOT = Path(tempfile.gettempdir()) / "tmp" / "pdfs" / "elliptic-curves-bsd"
OUTPUT = ROOT / "dist" / "elliptic-curves-bsd.pdf"

SOURCES = (
    BOOK_ROOT / "index.qmd",
    BOOK_ROOT / "chapters" / "01-rational-points.qmd",
    BOOK_ROOT / "chapters" / "02-group-law.qmd",
    BOOK_ROOT / "chapters" / "03-mordell-weil-rank-height.qmd",
    BOOK_ROOT / "chapters" / "04-reduction-and-hasse.qmd",
    BOOK_ROOT / "chapters" / "05-euler-product-and-l-function.qmd",
    BOOK_ROOT / "chapters" / "06-modularity-and-center.qmd",
    BOOK_ROOT / "chapters" / "07-bsd-conjecture.qmd",
    BOOK_ROOT / "chapters" / "08-synthesis.qmd",
    BOOK_ROOT / "chapters" / "references.qmd",
)


def split_qmd(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"front matter not found: {path}")
    front_matter, body = match.groups()
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front_matter, flags=re.MULTILINE)
    if not title_match:
        raise ValueError(f"title not found: {path}")
    return title_match.group(1), body.strip()


def pdf_body(path: Path, title: str, body: str) -> str:
    heading = "はじめに" if path.name == "index.qmd" else title
    body = body.replace("../assets/", "assets/")
    body = body.replace(r"\Sha", r"\operatorname{Sha}")
    body = body.replace(r"\varprojlim_{k,\,[\ell]}", r"\lim_{\leftarrow\,k,\,[\ell]}")
    body = re.sub(r"\[([^\]]+)\]\(chapters/[^)]+\.qmd\)", r"\1", body)
    body = re.sub(r"\[([^\]]+)\]\(references\.qmd\)", r"\1", body)
    page_break = "```{=typst}\n#pagebreak(weak: true)\n```\n\n"
    return f"{page_break}# {heading}\n\n{body}\n"


def find_quarto() -> str:
    configured = os.environ.get("QUARTO")
    if configured and Path(configured).is_file():
        return configured
    quarto = shutil.which("quarto")
    if quarto:
        return quarto
    raise RuntimeError("Quarto CLI was not found. Install Quarto or set QUARTO to its executable.")


def main() -> None:
    shutil.rmtree(BUILD_ROOT, ignore_errors=True)
    BUILD_ROOT.mkdir(parents=True)
    shutil.copytree(BOOK_ROOT / "assets", BUILD_ROOT / "assets")

    sections = []
    for source in SOURCES:
        title, body = split_qmd(source)
        sections.append(pdf_body(source, title, body))

    combined = BUILD_ROOT / "elliptic-curves-bsd.qmd"
    combined.write_text(
        r"""---
title: "楕円曲線の有理点と Birch-Swinnerton-Dyer 予想"
subtitle: "有理点・Mordell-Weil 群・L 関数から BSD 予想へ"
lang: ja
number-sections: false
format:
  typst:
    toc: true
    toc-title: "目次"
    toc-depth: 3
    papersize: a4
    margin:
      top: 22mm
      bottom: 24mm
      left: 23mm
      right: 23mm
    mainfont: "Yu Mincho"
    fontsize: 10.5pt
    linestretch: 1.12
    page-numbering: "1"
---

"""
        + "\n\n".join(sections),
        encoding="utf-8",
        newline="\n",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary_pdf = BUILD_ROOT / OUTPUT.name
    subprocess.run(
        [find_quarto(), "render", combined.name, "--to", "typst", "--output", OUTPUT.name],
        cwd=BUILD_ROOT,
        check=True,
    )
    shutil.copy2(temporary_pdf, OUTPUT)
    shutil.rmtree(BUILD_ROOT)
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
