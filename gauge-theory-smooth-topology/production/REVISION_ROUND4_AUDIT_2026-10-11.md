# Round 4 revision audit — 2026-10-11

## Verdict

Round 4 was treated as a source-level and output-level blocking review. The revision did not rely on the older 63-page or 89-page states; the starting point was the 90-page published PDF/source from commit `381d64c`.

## Blocking issues handled

| ID | Severity | Location | Action | Verification |
|---|---:|---|---|---|
| R4-P0-01 | P0 | Chapters 3, 8, 10, 17, Appendix B | Repaired corrupted prose and identifiers such as `定確`, `滑らかなである`, `cokee`, `Kueanishi`, `て射`, `ららかな`, `in定値`, and related replacement artifacts. | Added validator checks in `scripts/validate_gauge_authoring.py`; PDF text extraction search returns no matches. |
| R4-P0-02 | P0 | Chapter 8 | Rechecked `ker/im/coker` roles in the ASD deformation complex. Mathematical `\operatorname{coker}` was preserved; broken `cokee` was corrected only where it was a corruption. | Authoring validator and PDF text search. |
| R4-P1-01 | P1 | Chapter 2 | Added an explicit boundary-matrix computation for `S^1` and `[0,1]` so that later `ker/im/coker` language has a concrete prerequisite. | Web/PDF render and manual page check. |
| R4-P1-02 | P1 | Chapters 7--13, 16--17, Appendix A/B | Replaced avoidable English fragments in visible prose: `stabilizer`, `obstruction`, `regular`, `dimension`, `symbol`, `estimate`, `connection`, `bound`, `a priori`, etc., with context-appropriate Japanese. | Grep audit and PDF spot checks. |
| R4-P1-03 | P1 | Chapter 7 | Repaired an over-broad terminology replacement that temporarily changed the figure filename/id for the gauge-slice figure. | `python scripts/validate_site.py` catches the regression; now passes. |

## Regression prevention

The validator now scans chapter sources, the index, and generated SVGs for known corruption patterns. This is not a substitute for mathematical review, but it prevents the exact class of replacement bugs that triggered Round 4.

## Remaining scope note

The round improves the published textbook and removes the observed P0 output corruptions. It does not claim to turn the book into a 300-page foundational monograph; the current acceptance claim is limited to the repository's current production format and the Round 4 defects addressed here.
