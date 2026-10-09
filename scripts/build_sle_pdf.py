"""Build the complete SLE textbook PDF from the same QMD used by the Web site."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "sle-critical-phenomena"
OUTPUT = BOOK / "assets" / "sle-critical-phenomena.pdf"
SOURCES = (
    BOOK / "index.qmd",
    *(BOOK / "chapters" / f"{number:02d}-{slug}.qmd" for number, slug in (
        (1, "lattice-to-interface"),
        (2, "curve-space"),
        (3, "conformal-erasure"),
        (4, "loewner-equation"),
        (5, "schramm-principle"),
        (6, "brownian-loewner"),
        (7, "bessel-threshold"),
        (8, "geometric-phases"),
        (9, "martingales"),
        (10, "left-passage"),
        (11, "fractal-dimension"),
        (12, "convergence-blueprint"),
        (13, "percolation-sle6"),
        (14, "lerw-sle2"),
        (15, "universality"),
        (16, "gff"),
        (17, "gff-sle4"),
        (18, "outlook"),
    )),
    BOOK / "appendices" / "a-probability.qmd",
    BOOK / "appendices" / "b-convergence.qmd",
    BOOK / "appendices" / "c-bessel-dimension.qmd",
    BOOK / "appendices" / "d-numerics.qmd",
)


def find_quarto() -> str:
    configured = os.environ.get("QUARTO")
    if configured and Path(configured).is_file():
        return configured
    executable = shutil.which("quarto")
    if executable:
        return executable
    raise RuntimeError("Quarto CLI was not found. Install Quarto or set QUARTO to its executable.")


def body_from_qmd(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        match = re.match(r"\A---\n.*?\n---\n(.*)\Z", text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"Invalid front matter: {path}")
        text = match.group(1)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = text.replace("../assets/", "assets/")
    text = re.sub(r"\[([^\]]+)\]\((?:\.\./)?authoring/[^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\((?:\.\./)?index\.qmd\)", r"\1", text)
    return text.strip()


def verify_inputs() -> None:
    required = [
        *SOURCES,
        BOOK / "references.bib",
        BOOK / "assets" / "figures" / "vertical-slit-map.svg",
        BOOK / "assets" / "figures" / "driving-trace-print.svg",
        BOOK / "assets" / "figures" / "percolation-interface.svg",
        BOOK / "assets" / "figures" / "kappa-phases.svg",
        BOOK / "assets" / "figures" / "left-passage.svg",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Missing PDF inputs: " + ", ".join(missing))
    find_quarto()


def build(check_only: bool = False) -> None:
    verify_inputs()
    if check_only:
        print("SLE PDF inputs, Quarto executable, and output path are valid.")
        return

    build_root = Path(tempfile.mkdtemp(prefix="sle-pdf-"))
    try:
        shutil.copytree(BOOK / "assets" / "figures", build_root / "assets" / "figures")
        shutil.copy2(BOOK / "references.bib", build_root / "references.bib")
        page_break = "```{=typst}\n#pagebreak(weak: true)\n```\n\n"
        combined = build_root / "sle-critical-phenomena.qmd"
        front_matter = '''---
title: "二次元臨界現象とSLE"
subtitle: "格子模型から等角不変なランダム曲線へ"
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
    fontsize: 10pt
    linestretch: 1.1
    page-numbering: "1"
---

'''
        combined.write_text(
            front_matter + ("\n\n" + page_break).join(body_from_qmd(path) for path in SOURCES),
            encoding="utf-8",
            newline="\n",
        )
        subprocess.run(
            [find_quarto(), "render", combined.name, "--to", "typst", "--output", OUTPUT.name],
            cwd=build_root,
            check=True,
        )
        temporary_pdf = build_root / OUTPUT.name
        if not temporary_pdf.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError("Quarto did not create a valid PDF signature")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(temporary_pdf, OUTPUT)
        print(f"Built {OUTPUT}")
    finally:
        shutil.rmtree(build_root, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    build(check_only=args.check)


if __name__ == "__main__":
    main()
