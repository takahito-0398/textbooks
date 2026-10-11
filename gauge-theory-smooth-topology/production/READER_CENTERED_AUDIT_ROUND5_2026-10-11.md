# Reader-centered audit — Round 5

## Reader model

The simulated reader knows linear algebra, calculus, and elementary differential equations, but not topology, cohomology, bundles, gauge theory, Sobolev spaces, spinors, or complex/symplectic geometry.

## Findings and repairs

| Area | First likely stop point | Repair |
|---|---|---|
| Chapter 2: cohomology | The text moved from homology and forms to cup products without a concrete cochain construction. | Added `C^k=Hom(C_k,Z)`, coboundary `delta`, cohomology as `ker/im`, and an `S^1` cochain example. |
| Chapter 2: cup product | The formula with `PD(x) cup PD(y)` could look like a symbolic shortcut. | Added `T^2=R^2/Z^2`, normalized `dx,dy`, and `int_T2 dx wedge dy = 1`, tied to the intersection of the two basic loops. |
| Chapter 9: principal symbol | A reader might not understand why the "highest-order part" controls finite-dimensionality. | Added the exponential test `D(e^{i xi x})=i xi e^{i xi x}` and the second-order example before returning to ASD symbols. |
| Chapter 10: Kuranishi model | Corrupted prose made the finite-dimensional obstruction model unreadable. | Repaired the cusp explanation and "all directions look first-order" sentence. |
| Chapter 18: current | Taubes architecture used "current" without a definition. | Added the functional-on-forms explanation and how smooth curves define currents by integration. |
| Japanese / terminology | Several Round 5 seed strings remained visible in source. | Repaired source strings and added validator patterns for the new class of corruption. |

## Residual improvement candidates

The current revision is publishable within the repository's existing book scale. If a later expansion is desired, the most useful additions would be a full torus cellular cohomology computation, a longer Spin(4) representation derivation, and a worked example of a Donaldson invariant value from a standard reference.
