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
MANIFEST_PATH = BOOK / "production" / "manifest.json"
OUTPUT = BOOK / "assets" / "gauge-theory-smooth-topology.pdf"
PART_TITLES = {
    "I": "Part I　分類問題の衝突",
    "II": "Part II　4次元の方程式",
    "III": "Part III　モジュライ空間の局所構造",
    "IV": "Part IV　コンパクト化とDonaldson理論",
    "V": "Part V　Seiberg-Witten理論",
    "VI": "Part VI　幾何への帰還",
}


def split_qmd(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, str] = {}
    if text.startswith("---\n"):
        match = re.match(r"\A---\n.*?\n---\n(.*)\Z", text, flags=re.DOTALL)
        if not match:
            raise ValueError(f"invalid front matter: {path}")
        header = text[4 : text.find("\n---\n", 4)]
        for line in header.splitlines():
            key, separator, value = line.partition(":")
            if separator:
                metadata[key.strip()] = value.strip().strip('"')
        text = match.group(1)
    return metadata, text


def shift_headings(text: str, levels: int) -> str:
    shifted: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("#"):
            match = re.match(r"^(#{1,6})(\s+.*)$", line)
            if match:
                hashes, rest = match.groups()
                line = f"{'#' * min(6, len(hashes) + levels)}{rest}"
        shifted.append(line)
    return "\n".join(shifted)


def body_from_qmd(path: Path, *, heading_shift: int = 0) -> str:
    _, text = split_qmd(path)
    text = text.replace("../assets/", "assets/")
    text = re.sub(r"\[PDF検証版をダウンロード\]\(assets/gauge-theory-smooth-topology\.pdf\)\{[^}]+\}", "", text)
    text = re.sub(r"\[([^\]]+)\]\((?:\.\./)?authoring/README\.md\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\((?:\.\./)?(?:index|chapters/[^)]+)\.qmd\)(\{[^}]+\})?", r"\1", text)
    if heading_shift:
        text = shift_headings(text, heading_shift)
    return text.strip()


def find_quarto() -> str:
    configured = os.environ.get("QUARTO")
    if configured and Path(configured).is_file():
        return configured
    quarto = shutil.which("quarto")
    if quarto:
        return quarto
    raise RuntimeError("Quarto CLI was not found. Install Quarto or set QUARTO to its executable.")


def contract_sources() -> list[tuple[dict, Path]]:
    contracts = []
    for path in sorted((BOOK / "contracts").glob("*.json")):
        contracts.append(json.loads(path.read_text(encoding="utf-8")))
    return [(contract, BOOK / contract["source"]) for contract in contracts]


def combined_pdf_body() -> str:
    sections = [body_from_qmd(BOOK / "index.qmd")]
    current_part: str | None = None
    for contract, source in contract_sources():
        part = next(
            item["part"]
            for item in json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["curriculum"]
            if item["id"] == contract["chapter_id"]
        )
        if part != current_part:
            sections.append(f"# {PART_TITLES[part]}")
            current_part = part
        metadata, _ = split_qmd(source)
        title = metadata.get("title", source.stem)
        sections.append(f"## {title}\n\n{body_from_qmd(source, heading_shift=2)}")
    for appendix in [
        BOOK / "chapters" / "appendix-analysis.qmd",
        BOOK / "chapters" / "appendix-notation-exercises.qmd",
    ]:
        metadata, _ = split_qmd(appendix)
        title = metadata.get("title", appendix.stem)
        sections.append(f"# {title}\n\n{body_from_qmd(appendix, heading_shift=1)}")
    return "\n\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Render into a temporary directory without publishing the PDF")
    args = parser.parse_args()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_gauge_authoring.py")], check=True)

    with tempfile.TemporaryDirectory(prefix="gauge-theory-pdf-") as temporary:
        build_root = Path(temporary)
        shutil.copytree(BOOK / "assets" / "figures", build_root / "assets" / "figures")
        shutil.copy2(BOOK / "references.bib", build_root / "references.bib")
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
            + combined_pdf_body().replace("\n\n# ", "\n\n" + page_break + "# "),
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
