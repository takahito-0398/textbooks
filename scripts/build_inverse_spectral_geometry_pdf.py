"""Build the inverse-spectral-geometry PDF from the Web QMD sources."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = ROOT / "inverse-spectral-geometry"
BUILD_ROOT = Path(tempfile.gettempdir()) / "tmp" / "pdfs" / "inverse-spectral-geometry"
OUTPUT = BOOK_ROOT / "assets" / "inverse-spectral-geometry.pdf"

SOURCES = (
    BOOK_ROOT / "index.qmd",
    *(BOOK_ROOT / "chapters" / name for name in (
        "01-string.qmd",
        "02-membrane.qmd",
        "03-spectrum.qmd",
        "04-solvable-shapes.qmd",
        "05-inverse-problem.qmd",
        "06-weyl-law.qmd",
        "07-heat-trace.qmd",
        "08-variational-rigidity.qmd",
        "09-isospectral-drums.qmd",
        "10-transplantation.qmd",
        "11-sunada.qmd",
        "12-data-and-stability.qmd",
        "13-beyond.qmd",
        "a-analytic-foundations.qmd",
        "b-numerical-lab.qmd",
    )),
)


def body_from_qmd(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        match = re.match(r"\A---\n.*?\n---\n(.*)\Z", text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"invalid front matter: {path}")
        text = match.group(1)
    text = text.replace("../assets/", "assets/")
    # Typst does not implement TeX's equation-tag command; keep the printed label.
    text = re.sub(r"\\tag\{([^}]+)\}", r"\\qquad\\text{(\1)}", text)
    text = re.sub(r"\[([^\]]+)\]\(chapters/[^)]+\.qmd\)", r"\1", text)
    return text.strip()


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
    shutil.copytree(BOOK_ROOT / "assets" / "figures", BUILD_ROOT / "assets" / "figures")
    shutil.copy2(BOOK_ROOT / "references.bib", BUILD_ROOT / "references.bib")

    page_break = "```{=typst}\n#pagebreak(weak: true)\n```\n\n"
    sections = [body_from_qmd(source) for source in SOURCES]
    combined = BUILD_ROOT / "inverse-spectral-geometry.qmd"
    combined.write_text(
        r'''---
title: "逆スペクトル幾何"
subtitle: "音から形はどこまで聞こえるか"
lang: ja
bibliography: references.bib
reference-section-title: "参考文献"
number-sections: true
execute:
  enabled: false
format:
  typst:
    toc: true
    toc-title: "目次"
    toc-depth: 3
    papersize: a4
    margin:
      top: 22mm
      bottom: 24mm
      left: 22mm
      right: 22mm
    mainfont: "Yu Mincho"
    fontsize: 10pt
    linestretch: 1.1
    page-numbering: "1"
---

'''
        + ("\n\n" + page_break).join(sections),
        encoding="utf-8",
        newline="\n",
    )

    temporary_pdf = BUILD_ROOT / OUTPUT.name
    subprocess.run(
        [find_quarto(), "render", combined.name, "--to", "typst", "--output", OUTPUT.name],
        cwd=BUILD_ROOT,
        check=True,
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(temporary_pdf, OUTPUT)
    shutil.rmtree(BUILD_ROOT)
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
