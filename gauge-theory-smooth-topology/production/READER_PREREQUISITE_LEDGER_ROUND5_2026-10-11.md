# Reader prerequisite ledger — Round 5

## Scope

This ledger records the major concepts whose first use matters for a reader assumed to know only linear algebra, calculus, and elementary differential equations. It focuses on concepts changed or audited in Round 5.

| Concept / notation | First teaching location | First substantial use | Prerequisites | Round 5 status |
|---|---|---|---|---|
| Chain, boundary, cycle | Chapter 2, "チェイン、境界、サイクル" | Homology and intersection form | Linear algebra with integer matrices | Already present; kept. |
| Boundary matrix | Chapter 2, "境界写像を行列で計算する" | Later `ker/im/coker` and deformation complex | Kernel and image of a matrix | Strengthened in Round 4; retained. |
| Cochain and coboundary | Chapter 2, "コチェインと余境界" | Cup product / Poincare duality | Homomorphisms of free abelian groups | Added in Round 5. |
| Cup product | Chapter 2, "カップ積をトーラスで見る" | Intersection form via `PD(x) cup PD(y)` | Cochains, differential forms, integration | Added explicit torus calculation in Round 5. |
| Poincare duality / fundamental class | Chapter 2, theorem callout | Intersection form | Homology, cohomology, orientation | Still cited as a theorem, but now preceded by cochain/cup examples. |
| Normal bundle / Euler number | Chapter 2, self-intersection section | Adjunction inequality | Push-off of a surface | Existing explanation retained; future expansion candidate. |
| Principal bundle / adjoint bundle | Chapter 4 | Gauge transformations, `ad P` | Bundle examples, group action | Text repaired (`貼り合わされる`) and terminology audited. |
| Principal symbol | Chapters 8--9 | Ellipticity / Fredholm | Fourier mode calculation | Chapter 9 now derives principal symbol from high-frequency exponentials. |
| Kuranishi map / obstruction space | Chapter 10 | Smooth moduli | Kernel, cokernel, finite-dimensional model | Corrupted prose repaired; finite-dimensional cusp example retained. |
| Universal bundle / slant product / `mu` | Chapters 12--13 | Donaldson invariants | Cohomology, degree matching | Existing staged explanation retained; terminology check passed. |
| Spin^c, half spinors, Clifford action | Chapter 15 | SW equations | Matrices, rotations, bundles | Existing construction retained; no Round 5 regression found. |
| Current | Chapter 18, Taubes architecture | SW to pseudoholomorphic curves | Integration of forms over curves | Added short definition as generalized curve/functionals on forms. |

## Reader-first conclusion

Round 5 does not merely remove corrupted words. It adds missing bridges before use: cochains before cup products, torus integration before intersection via cup product, and Fourier high-frequency computation before principal symbols. These are the highest-impact prerequisite inversions detected in the current pass.
