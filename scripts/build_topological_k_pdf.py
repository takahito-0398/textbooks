"""Render the chapter QMDs as one single-column Typst book."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

BOOK = Path(__file__).resolve().parents[1] / "topological-k-theory"
OUTPUT = BOOK / "assets" / "topological-k-theory.pdf"

HEADER = """---
lang: ja
execute:
  enabled: false
format:
  typst:
    crossref:
      chapters: true
      eq-prefix: 式
      fig-prefix: 図
      fig-title: 図
      tbl-title: 表
      tbl-prefix: 表
    papersize: iso-b5
    margin:
      top: 23mm
      bottom: 24mm
      left: 25mm
      right: 25mm
    mainfont: "Yu Mincho"
    fontsize: 10.7pt
    page-numbering: "1"
---

"""

def raw_typst(code):
    return f"\x60\x60\x60{{=typst}}\n{code}\n\x60\x60\x60\n\n"


def format_reading_block(match):
    kind, content = match.groups()
    opening = raw_typst(f'#reading("{kind}")[')
    label, separator, body = content.partition("\n\n")
    if separator and label.startswith("**") and label.endswith("**"):
        opening += raw_typst("#reading-label[") + label + "\n\n" + raw_typst("]")
        content = body
    return opening + content + "\n" + raw_typst("]")


def read_chapter(path):
    _, metadata, content = path.read_text(encoding="utf-8").split("---\n", 2)
    title = next(line.removeprefix("title: ").strip('"')
                 for line in metadata.splitlines() if line.startswith("title: "))
    content = re.sub(
        r"\]\((?:\./)?([\w-]+)\.qmd(?:#([\w-]+))?\)",
        lambda link: f"](#{link[2] or link[1]})", content,
    )
    content = content.replace("](../assets/figures/", "](figures/")
    content = re.sub(
        r"^::: \{\.ku-(chapter|summary|definition|theorem|column|worked|point)\}[ \t]*\n(.*?)^:::[ \t]*$",
        format_reading_block,
        content,
        flags=re.M | re.S,
    )
    return title, content.strip()


def render(quarto, stage, output):
    command = [quarto, "render", "book.qmd", "--to", "typst", "--output", "book.pdf"]
    completed = subprocess.run(command, cwd=stage, capture_output=True,
                               encoding="utf-8", errors="replace")
    log = completed.stdout + completed.stderr
    sys.stdout.reconfigure(errors="backslashreplace")
    print(log)
    completed.check_returncode()
    if re.search(r"Could not convert TeX math|undefined reference", log, re.I):
        raise RuntimeError("Unconverted math or unresolved reference")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(stage / "book.pdf", output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quarto", default=os.environ.get("QUARTO", "quarto"))
    parser.add_argument("--sample", type=Path, help="Render the opening and a dense formula sample.")
    options = parser.parse_args()
    paths = sorted((BOOK / "chapters").glob("[0-9][0-9]-*.qmd"))
    if options.sample:
        paths = [path for path in paths if path.name.startswith(("00-", "01-", "06-"))]
    if not paths:
        raise ValueError("No chapters were found")
    chapters = [(path.stem, *read_chapter(path)) for path in paths]
    styles = raw_typst('''
#set text(lang: "ja", cjk-latin-spacing: auto)
#set par(justify: true, leading: 0.68em, spacing: 0.95em)
#let reading-label(body) = block(sticky: true, below: 0.4em, body)
#let reading(kind, body) = {
  let accent = rgb("#294952")
  let background = if kind == "summary" { none } else { rgb("#f3f5f5") }
  block(
    width: 100%,
    breakable: true,
    inset: (left: 10pt, right: 10pt, top: 7pt, bottom: 7pt),
    fill: background,
    stroke: (left: if kind == "summary" { 0.75pt + luma(160) } else { 1.25pt + accent }),
    above: 0.9em, below: 0.95em,
    body,
  )
}
#set page(header: context {
  if counter(page).get().first() > 2 {
    align(right, text(font: "Yu Gothic", size: 8pt, fill: luma(100))[位相的K理論を読む])
  }
})
#set figure(gap: 6pt)
#show figure.caption: set text(size: 9pt)
#set table(stroke: 0.35pt + luma(180), inset: (x: 3pt, y: 2pt))
#set math.equation(number-align: right + bottom)
#set heading(numbering: none)
#set document(title: "位相的K理論を読む ― 貼り合わせ・特性類・指数")
#show math.equation.where(block: true): set block(above: 0.9em, below: 0.9em)
#show heading.where(level: 1): set text(font: "Yu Gothic", size: 18pt, fill: rgb("#20363d"))
#show heading.where(level: 2): it => block(above: 1.3em, below: 0.55em)[
  #text(fill: rgb("#294952"), size: 8pt)[■] #h(0.45em)
  #text(font: "Yu Gothic", size: 12.1pt, weight: "bold", fill: rgb("#20363d"))[#it.body]
]
#show heading.where(level: 3): set text(font: "Yu Gothic", size: 11pt)
#v(1fr)
#align(center)[
  #text(font: "Yu Gothic", size: 26pt, weight: "bold", fill: rgb("#173c37"))[位相的K理論を読む]
  #v(8mm)
  #text(size: 13pt)[貼り合わせ・特性類・指数]
]
#v(1fr)
#pagebreak()
'''.strip())
    body = raw_typst('#heading(level: 1, outlined: false)[目次]\n#text(size: 9pt)[#outline(title: none, depth: 1, indent: 0pt)]')
    for key, title, content in chapters:
        body += raw_typst("#pagebreak(weak: true)")
        body += f"# {title} {{#{key}}}\n\n"
        body += f"{content}\n\n"
    output = options.sample.resolve() if options.sample else OUTPUT
    with TemporaryDirectory(prefix="ku-pdf-") as directory:
        stage = Path(directory)
        source_figures = BOOK / "assets" / "figures"
        if source_figures.is_dir():
            shutil.copytree(source_figures, stage / "figures")
        (stage / "book.qmd").write_text(HEADER + styles + body, encoding="utf-8")
        render(options.quarto, stage, output)
    evidence = {"chapters": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest()}
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
