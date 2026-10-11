# Japanese Terminology Audit

## Policy

Use established Japanese mathematical terminology when it is natural: 交点形式, 同相, 微分同相, 不変量, コンパクト性, 向き, 種数, 法束, オイラー数, 随伴不等式. Keep conventional symbols, theorem names, and unavoidable proper names in Roman letters where standard.

## Corrected Examples

| Before | After |
|---|---|
| 捩れ空間 | トーサー／主等質空間 |
| 位相的ly | 位相的に |
| positivity of 交差s | 擬正則曲線の交点正値性 |
| 滑らかななPDE | 滑らかなデータに依存する構成 |
| normal bundle | 法束 |
| Euler number | オイラー数 |
| adjunction inequality | 随伴不等式 |
| genus | 種数 |
| scalar curvature | スカラー曲率 |
| Donaldson polynomial | Donaldson多項式 |

## Exception List

- Gauge, Spin-c, Seiberg-Witten, Donaldson, Taubes, Kähler, Dirac, Hodge, Uhlenbeck, Sard--Smale remain where they are proper names, standard theory names, or search-critical terminology.
- Internal manifest keys such as `moduli_lifecycle`, `regularity`, `compactification`, and `count` are retained because validators depend on these machine-readable keys.

## Method

1. Scanned chapters, manifest, contracts, SVG assets, and PDF builder source for review-specified mixed-language failures.
2. Corrected paragraph-level language rather than only replacing isolated words.
3. Re-ran targeted scans for the concrete failures.
4. Re-ran the authoring validator and unit tests after fixing source and manifest side effects.

## Remaining Judgment

Some English remains in source code templates before translation, bibliography keys, theorem identifiers, and machine-readable registry fields. These are not visible prose defects or are required by build tooling.
