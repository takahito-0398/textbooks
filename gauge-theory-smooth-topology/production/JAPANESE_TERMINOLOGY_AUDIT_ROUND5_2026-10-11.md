# Japanese terminology audit — Round 5

## New seed issues checked

The Round 5 prompt identified new visible defects. The source was searched for and repaired where present:

- `りり合わされる` -> `貼り合わされる`;
- `orthonormal frame/coframe` -> `正規直交枠/正規直交余標構`;
- `指数 theorem` -> `指数定理`;
- `てての方向`, `平面て体` -> repaired as meaningful Japanese;
- `障害 space` -> `障害空間`;
- `nonlinear coupling` -> `非線形な連成`;
- `current` -> `カレント` with a definition;
- `elliptic コンパクト性` -> `楕円型コンパクト性`;
- `Sard theorem`, `Sard--Smale theorem`, `critical value` -> Japanese theorem prose.

## Regression guard

`scripts/validate_gauge_authoring.py` now includes the Round 5 corruption patterns in addition to earlier Round 3/4 patterns. The final source check returned no matches for the known corruption set.

## Deliberate exceptions

Names and standard symbols remain where appropriate: Donaldson, Seiberg--Witten, Taubes, Dirac, Hodge, Uhlenbeck, Sard--Smale, Weitzenböck, `Spin^c`, `SU(2)`, `SO(3)`, `U(1)`, `ker`, `im`, `coker`, `PD`.
