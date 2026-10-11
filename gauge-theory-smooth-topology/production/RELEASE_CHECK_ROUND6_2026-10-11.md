# Release check — Round 6

## Scope

Round 6 incorporated the self-contained reader audit into the editable source. The release check covers source validation, Web render, integrated PDF regeneration, text extraction, visual spot checks, and publication readiness.

## Local checks

| Check | Result |
|---|---|
| `python scripts\validate_gauge_authoring.py` | PASS |
| `python -m unittest tests.test_gauge_authoring` | PASS, 7 tests |
| `python scripts\validate_site.py` | PASS |
| `quarto render gauge-theory-smooth-topology` | PASS |
| `python scripts\build_gauge_theory_pdf.py` | PASS |
| PDF metadata | PASS, 95 pages, 3,004,051 bytes, A4 |
| PDF text scan for Round 6 and earlier corruption strings | PASS |
| Representative PDF page rendering | PASS, rendered pages 1, 13--18, 38--43, 56--61, 66--73, and 95; inspected pages 13, 39, 40, 58, and 67. |

## Known tooling limitation

The PDF operation marker command could not run because `container_tools/mark_artifact_operation_started.mjs` is not present in this checkout. This is a tooling-marker limitation only; the PDF was regenerated and verified from the editable source.

## Release decision

Round 6 is ready to commit, push, and deploy through the existing GitHub Pages workflow.
