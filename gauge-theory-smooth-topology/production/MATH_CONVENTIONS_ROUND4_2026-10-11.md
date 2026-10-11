# Round 4 mathematical conventions

## Protected mathematical identifiers

The following are mathematical identifiers or standard operators and must not be mechanically translated inside formulas:

- `\ker`, `\operatorname{im}`, `\operatorname{coker}`;
- `\operatorname{ind}`, `\det D_A`, `H_A^0,H_A^1,H_A^2`;
- `Spin^c`, `SU(2)`, `SO(3)`, `U(1)`;
- `F_A^+`, `F_A^-`, `d_A`, `d_A^+`, `D_A`.

Visible prose may explain these as 核, 像, 余核, 指数, 行列式線束, 安定化群, 障害空間, but the formula identifiers remain Roman/TeX.

## ASD deformation complex

For an ASD connection,

```tex
0 \to \Omega^0(\operatorname{ad}P)
  \xrightarrow{d_A}
  \Omega^1(\operatorname{ad}P)
  \xrightarrow{d_A^+}
  \Omega^2_+(\operatorname{ad}P)
  \to 0
```

is a complex because `d_A^+d_A\phi=[F_A^+,\phi]=0`. Its cohomology is read as:

- `H_A^0`: infinitesimal stabilizer / 無限小安定化群;
- `H_A^1`: true first-order deformation modulo gauge;
- `H_A^2`: obstruction / 障害.

The gauge-fixed operator is

```tex
D_A=d_A^*\oplus d_A^+
```

and, under the usual slice/Fredholm hypotheses, `\ker D_A` represents `H_A^1`, while `\operatorname{coker}D_A` corresponds to `H_A^0\oplus H_A^2`.

## Fredholm finite-dimensionality

The finite-dimensionality proof uses an `L^2`-orthonormal sequence in the kernel. The elliptic estimate gives uniform Sobolev boundedness; Rellich compactness gives a strongly convergent `L^2` subsequence; orthonormal separation gives a contradiction. This is explicitly preserved in Chapter 9.

## Freedman / Donaldson convention

Round 4 preserves the corrected Round 3 convention: in the simply connected closed oriented topological category, even and odd unimodular forms have different Kirby--Siebenmann behavior. The text must not regress to the false statement that every form gives a unique topological manifold without the parity and KS qualifications.
