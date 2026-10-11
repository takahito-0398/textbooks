# Source corruption regression — Round 4

## Cause class

Round 4 found replacement artifacts consistent with over-broad prose cleanup touching mathematical words, English identifiers, and parts of Japanese words. The exact mechanism was not assumed; the remedy was to protect visible mathematical identifiers and add regression checks.

## Implemented guard

`scripts/validate_gauge_authoring.py` now scans chapter sources, the index, and generated SVG assets for known corruption patterns:

- `cokee`, `Kueanishi`, `て射`, `ららかな`, `in 定値`, `in定値`;
- `滑らかなである`, `滑らかな化`, `定確`;
- `stabilizee`, `obsteuction`, `eegulae`, `theoeem`, `peincipal`;
- `則部分`, `則しくは`, `則規`, `foemula`, `図 図`.

The check intentionally allows correct mathematical `coker`, because replacing formula operators would be a mathematical regression.

## Output check

The generated PDF text is also extracted with `pdftotext` and searched for the same corruption list. Round 4 final extraction returned no matches.

## Known tool limitation

The PDF skill's requested operation marker command could not be run because `container_tools/mark_artifact_operation_started.mjs` is absent from this repository. This limitation is recorded here and in the release check; PDF generation and rendering QA were still performed.
