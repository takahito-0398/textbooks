"""Build or check the gauge-theory PDF from the Web QMD sources."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "gauge-theory-smooth-topology"
OUTPUT = BOOK / "assets" / "gauge-theory-smooth-topology.pdf"


def body_from_qmd(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        match = re.match(r"\A---\n.*?\n---\n(.*)\Z", text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"invalid front matter: {path}")
        text = match.group(1)
    text = text.replace("../assets/", "assets/")
    text = re.sub(r"\[PDF検証版をダウンロード\]\(assets/gauge-theory-smooth-topology\.pdf\)\{[^}]+\}", "", text)
    text = re.sub(r"\[([^\]]+)\]\((?:\.\./)?authoring/README\.md\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\((?:\.\./)?(?:index|chapters/[^)]+)\.qmd\)(\{[^}]+\})?", r"\1", text)
    return text.strip()


def find_quarto() -> str:
    configured = os.environ.get("QUARTO")
    if configured and Path(configured).is_file():
        return configured
    quarto = shutil.which("quarto")
    if quarto:
        return quarto
    raise RuntimeError("Quarto CLI was not found. Install Quarto or set QUARTO to its executable.")


def contract_sources() -> list[Path]:
    contracts = []
    for path in sorted((BOOK / "contracts").glob("*.json")):
        contracts.append(json.loads(path.read_text(encoding="utf-8")))
    chapter_sources = [BOOK / contract["source"] for contract in contracts]
    appendices = [
        BOOK / "chapters" / "appendix-analysis.qmd",
        BOOK / "chapters" / "appendix-notation-exercises.qmd",
    ]
    return [*chapter_sources, *appendices]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Render into a temporary directory without publishing the PDF")
    args = parser.parse_args()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_gauge_authoring.py")], check=True)

    with tempfile.TemporaryDirectory(prefix="gauge-theory-pdf-") as temporary:
        build_root = Path(temporary)
        shutil.copytree(BOOK / "assets" / "figures", build_root / "assets" / "figures")
        shutil.copy2(BOOK / "references.bib", build_root / "references.bib")
        sources = [BOOK / "index.qmd", *contract_sources()]
        page_break = "```{=typst}\n#pagebreak(weak: true)\n```\n\n"
        combined = build_root / "gauge-theory-smooth-topology.qmd"
        combined.write_text(
            '''---
title: "4次元ゲージ理論と滑らかな位相"
subtitle: "Donaldson理論からSeiberg-Witten理論へ"
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
            + ("\n\n" + page_break).join(body_from_qmd(source) for source in sources),
            encoding="utf-8",
            newline="\n",
        )
        temporary_pdf = build_root / OUTPUT.name
        subprocess.run(
            [find_quarto(), "render", combined.name, "--to", "typst", "--output", OUTPUT.name],
            cwd=build_root,
            check=True,
        )
        if not temporary_pdf.is_file() or temporary_pdf.stat().st_size < 1_000:
            raise RuntimeError("PDF render did not produce a non-empty document")
        if not args.check:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(temporary_pdf, OUTPUT)
            print(f"Built {OUTPUT.relative_to(ROOT)}")
        else:
            print(f"PDF check passed ({temporary_pdf.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
