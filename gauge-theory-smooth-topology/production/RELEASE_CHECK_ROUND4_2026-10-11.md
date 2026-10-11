# Round 4 release check — 2026-10-11

## Build and validation

| Check | Result |
|---|---|
| `python scripts/validate_gauge_authoring.py` | PASS |
| `python -m unittest tests.test_gauge_authoring` | PASS, 7 tests |
| `python scripts/validate_site.py` | PASS |
| Quarto render for `gauge-theory-smooth-topology` | PASS |
| `python scripts/build_gauge_theory_pdf.py` | PASS |

## PDF

- Path: `gauge-theory-smooth-topology/assets/gauge-theory-smooth-topology.pdf`
- Pages: 91
- Page size: A4
- File size after final Round 4 build: 2,918,947 bytes
- Engine: Typst through the existing PDF builder.

## Text extraction regression

`pdftotext` extraction was searched for known Round 4 corruption terms, including `cokee`, `Kueanishi`, `て射`, `ららかな`, `in 定値`, `in定値`, `滑らかなである`, `定確`, `図 図`, and web-only PDF button labels. The final search returned no matches.

## Rendered page spot checks

Representative pages were rendered to PNG:

- page 1: table of contents;
- page 16: Chapter 2 intersection-form calculation and exercise;
- page 38: ASD deformation complex / `coker` area;
- page 60: Freedman classification and smooth/topological distinction;
- page 72: Donaldson/SW comparison table;
- page 91: bibliography / final page.

No clipping, overlap, or visible corruption was found in the inspected pages. Page 72 initially exposed remaining English fragments, which were corrected before the final build.

## Deployment status

Round 4 source and PDF have been prepared locally. Commit, push, and external GitHub Pages deployment verification are performed after this release check when publishing is requested/available.
