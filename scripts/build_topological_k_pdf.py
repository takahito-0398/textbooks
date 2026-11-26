"""Render the chapter QMDs as one two-column Typst book."""
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
    papersize: iso-b6
    margin:
      top: 13mm
      bottom: 15mm
      left: 8mm
      right: 8mm
    mainfont: "Yu Mincho"
    fontsize: 11.5pt
    page-numbering: "1"
---

"""

def raw_typst(code):
    return f"\x60\x60\x60{{=typst}}\n{code}\n\x60\x60\x60\n\n"


def read_chapter(path):
    _, metadata, content = path.read_text(encoding="utf-8").split("---\n", 2)
    title = next(line.removeprefix("title: ").strip('"')
                 for line in metadata.splitlines() if line.startswith("title: "))
    content = re.sub(
        r"\]\((?:\./)?([\w-]+)\.qmd(?:#([\w-]+))?\)",
        lambda link: f"](#{link[2] or link[1]})", content,
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
    paths = sorted((BOOK / "chapters").glob("[0-7][0-9]-*.qmd"))
    if options.sample:
        paths = [path for path in paths if path.name.startswith(("00-", "01-", "06-"))]
    if len(paths) != (3 if options.sample else 8):
        raise ValueError("Expected three sample chapters or all eight release chapters")
    chapters = [(path.stem, *read_chapter(path)) for path in paths]
    styles = raw_typst('''
#set text(lang: "ja", cjk-latin-spacing: auto)
#set par(justify: true, leading: 0.83em)
#set heading(numbering: none)
#set document(title: "位相的K理論を読む ― 貼り合わせ・特性類・指数")
#show math.equation.where(block: true): it => context {
  let max-width = 49mm
  let width = measure(it).width
  if width > max-width {
    scale(x: max-width / width * 100%, y: max-width / width * 100%, reflow: true, it)
  } else { it }
}
#show heading.where(level: 1): set text(font: "Yu Gothic", size: 17pt, fill: rgb("#173c37"))
#show heading.where(level: 2): set text(font: "Yu Gothic", size: 13pt, fill: rgb("#173c37"))
#show heading.where(level: 3): set text(font: "Yu Gothic", size: 10pt)
#v(1fr)
#align(center)[
  #text(font: "Yu Gothic", size: 26pt, weight: "bold", fill: rgb("#173c37"))[位相的K理論を読む]
  #v(8mm)
  #text(size: 13pt)[貼り合わせ・特性類・指数]
]
#v(1fr)
#pagebreak()
'''.strip())
    body = raw_typst('#heading(level: 1, outlined: false)[目次]\n#outline(title: none, depth: 1, indent: 0pt)')
    for key, title, content in chapters:
        body += raw_typst("#pagebreak(weak: true)")
        body += f"# {title} {{#{key}}}\n\n"
        body += raw_typst("#columns(2, gutter: 6mm)[")
        body += f"{content}\n\n"
        body += raw_typst("]")
    output = options.sample.resolve() if options.sample else OUTPUT
    with TemporaryDirectory(prefix="ku-pdf-") as directory:
        stage = Path(directory)
        (stage / "book.qmd").write_text(HEADER + styles + body, encoding="utf-8")
        render(options.quarto, stage, output)
    evidence = {"chapters": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest()}
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
