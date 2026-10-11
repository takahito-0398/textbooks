# Render QA

作成日: 2026-10-11

## Required render targets

- Web: `quarto render gauge-theory-smooth-topology`
- PDF: `python scripts/build_gauge_theory_pdf.py`
- Site validation: `python scripts/validate_site.py`
- Contract validation: `python scripts/validate_gauge_authoring.py`
- Unit tests: `python -m unittest tests.test_gauge_authoring`

## Current evidence

Round 7の95ページPDFは `production/legacy-95p-sources/` に退避した旧版に対応する。現在の正本は22章新稿であり、以下の再実行結果を現在の根拠とする。

## Re-run on 2026-10-11

| Check | Result |
|---|---|
| `python scripts\validate_gauge_authoring.py --audit-bundle gauge-theory-smooth-topology\production\fresh-rebuild-validation-bundle` | PASS |
| `python -m unittest tests.test_gauge_authoring` | PASS, 8 tests |
| `python scripts\validate_site.py` | PASS |
| `python scripts\build_gauge_theory_pdf.py` with `QUARTO=C:\Users\takah\.cache\quarto\1.10.18\bin\quarto.exe` | PASS |
| `quarto render gauge-theory-smooth-topology` with the same cached Quarto executable | PASS, 25 QMD rendered |
| `pdfinfo gauge-theory-smooth-topology/assets/gauge-theory-smooth-topology.pdf` | PASS, 48 pages, A4, 1,345,553 bytes |
| `pdftotext` scan for Round 7 P0/P1 regression phrases | PASS, no matches |
| Visual page-by-page PDF review | NOT RUN in this pass |
| Mobile browser screenshot review | NOT RUN in this pass |

## QA policy

PDF抽出テキストだけで数式の上付き・下付き誤りを断定しない。重大な数式・図版変更後は、PDFの可視レンダリングとWeb狭幅表示を再確認する。

