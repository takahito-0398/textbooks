# Round 4 concept dependency audit

## Reader contract

The Round 4 prompt sets a strict reader contract: linear algebra, calculus, and elementary ODE/PDE may be assumed; topology, manifolds, forms, bundles, connections, Sobolev spaces, spinors, and gauge theory may not.

## Changes made

| Dependency gap | Source action |
|---|---|
| `ker/im/coker` appeared later in deformation theory without a fully elementary computation. | Chapter 2 now computes homology of `S^1` and `[0,1]` using boundary matrices, then explicitly links this to later kernel/image/quotient reasoning. |
| Gauge quotient language mixed English terms and could look like jargon rather than structure. | Chapters 7, 8, 10, 12, 17 and Appendix B now use 安定化群, 障害, 正則性, 軌道, スライス, 主記号, 評価 where these are explanatory prose. |
| Chapter 8 corruption obscured the actual deformation complex. | Chapter 8 now uses correct `coker`, Kuranishi, 主記号, 正規直交基底, 自己双対部分, and Japanese role explanations. |
| PDF-visible comparison table in Chapter 17 retained avoidable English. | Chapter 17 table and prose now say 非可換接続, `U(1)` 接続, Weitzenböck評価, 先験的評価. |

## Follow-up watchpoints

If future revisions expand the book further, the next high-value additions are:

1. a longer worked cellular homology computation for a torus;
2. a fully expanded first example of a cup product;
3. a low-dimensional toy Kuranishi map with both zero and nonzero obstruction cases.

These are improvements, not newly observed P0 regressions in the current output.
