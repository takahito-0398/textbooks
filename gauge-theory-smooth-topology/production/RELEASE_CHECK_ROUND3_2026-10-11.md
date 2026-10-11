# Release Check Round 3

## Completed Before Final Build

- Round 3 review ingested.
- P0/P1 mathematical blockers corrected in source.
- Japanese terminology and hybrid-expression scan performed.
- Figure generator rerun.
- PDF builder updated to suppress web-only button links.

## Commands

```powershell
python scripts\generate_gauge_figures.py
python scripts\validate_gauge_authoring.py
python -m unittest tests.test_gauge_authoring
quarto render gauge-theory-smooth-topology
python scripts\validate_site.py
python scripts\build_gauge_theory_pdf.py
pdftotext -enc UTF-8 gauge-theory-smooth-topology\assets\gauge-theory-smooth-topology.pdf tmp\round3-pdf.txt
pdftoppm -png -f 1 -l 1 -r 120 gauge-theory-smooth-topology\assets\gauge-theory-smooth-topology.pdf tmp\round3-pdf-render2\page-1
```

## Current Results

- Authoring validation: PASS
- Unit tests: PASS
- Web render: PASS
- Site validation: PASS
- PDF render: PASS, 90 pages, A4, 2,907,050 bytes
- Targeted source/PDF scan for listed broken phrases: PASS except allowed source-code translation templates.
- PDF representative page image checks: pages 1, 18, 38, 64, 78, 90 inspected; no clipping or major formula/figure collapse observed.
- `git diff --check`: PASS

## Note

The PDF skill's optional artifact marker script was not present in this repository, so the repository-native PDF builder was used directly.
