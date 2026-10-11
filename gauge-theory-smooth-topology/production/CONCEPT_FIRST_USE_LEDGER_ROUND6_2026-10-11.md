# Concept first-use ledger — Round 6

## Scope

This ledger records the high-impact first-use and dependency checks performed for the Round 6 self-contained rewrite. It focuses on concepts that the audit identified as likely to appear before a non-specialist science student can use them.

## Ledger

| Concept / notation | First meaningful use after revision | Required prior support | Round 6 action | Status |
|---|---|---|---|---|
| Tangent vector / cotangent vector | Chapter 2, before differential forms | Multivariable calculus velocity vectors and linear functionals | Added a local-coordinate construction of $T_pX$, $T_p^*X$, and $dx^i(\partial/\partial x^j)=\delta^i_j$ before 1-forms are used. | PASS |
| Differential form and wedge product | Chapter 2, differential-forms section | Tangent/cotangent paragraph immediately before it | Kept the $dx\wedge dy$ calculation and made the type of a 1-form explicit before use. | PASS |
| Cochain / coboundary | Chapter 2 | Chain groups and boundary matrices | Existing Round 5 material retained; dependency from boundary matrix to dual coboundary checked. | PASS |
| Cup product / de Rham exterior product bridge | Chapter 2 | Cochains, normalized forms, fundamental class | Retained torus calculation and the warning separating integer cup product from real de Rham representatives. | PASS |
| Self-intersection / normal bundle / section | Chapter 2 | Tangent planes and transverse intersections | Expanded self-intersection as push-off by a section of the rank-2 normal bundle, with a local Jacobian-sign formula for zeros. | PASS |
| Connection / covariant derivative | Chapter 4 | Vector bundle, local trivialization, moving frame | Existing moving-frame derivation retained; Round 6 fixed corruption strings in the Chern--Weil/Yang--Mills transition. | PASS |
| Principal symbol | Chapter 8 | Fourier/high-frequency calculation | Moved the high-frequency motivation before the ASD symbol sequence is used; Chapter 9 now treats it as prior work. | PASS |
| Fredholm finite-dimensionality | Chapter 9 | Principal-symbol exactness, Sobolev estimate, Rellich compactness | Existing derivation retained; order now follows symbol motivation. | PASS |
| Universal bundle / slant product / $\mu$ map | Chapter 12 | Cut-down model and degree matching | Added explicit type check: $p_1(\mathbb P)/\alpha\in H^{4-i}(\mathcal B^*)$. | PASS |
| Donaldson concrete output | Chapter 13 | Freedman existence, Donaldson diagonalization, $E_8$ parity | Clarified that the book's concrete Donaldson-side output is $E_8$ non-smoothability, while Donaldson polynomial computation is presented as a construction model. | PASS |
| Knot surgery inputs | Chapter 14 | Basic knot, tubular neighborhood, meridian, longitude, Alexander polynomial | Added a short local vocabulary section before the Fintushel--Stern construction. | PASS |
| Half-spinors | Chapter 15 | $SU(2)\to SO(3)$, Pauli matrices | Added the reason $\mathrm{Spin}(4)\cong SU(2)_+\times SU(2)_-$ produces $W^\pm$ before Clifford matrices are used. | PASS |
| Complex/symplectic bridge | Chapter 18 | Almost-complex structure, type decomposition, Kähler form | Existing CP examples retained; English drift in hyperplane/canonical terms corrected. | PASS |

## Remaining limits

Research-level theorems such as Freedman classification, Donaldson diagonalization, Uhlenbeck compactness, Atiyah--Singer, Taubes, and Fintushel--Stern knot surgery remain cited results. Round 6 requires their assumptions and outputs to be explicit, not their full proofs.
