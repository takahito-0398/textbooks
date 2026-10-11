# Independent math audit

作成日: 2026-10-11

## Scope

対象は `gauge-theory-smooth-topology` のQMD本文、章契約、manifest、参考文献、図版registryである。対象外教材は確認していない。

## Findings

| Priority | Finding | Status | Evidence |
|---|---|---|---|
| P0 | Fintushel-Stern結び目手術でトーラス法線円周を結び目メリディアンへ送る記述は残してはならない。 | Fixed / guarded | 第14章で優先ロンジチュード対応を明示し、validatorに回帰パターンを登録済み。 |
| P0 | Freedman分類、Donaldson対角化、異種滑らかな構造の論理を混同してはならない。 | Pass for structure | 第3章、第13章、第14章が役割を分け、manifestのtheorem/black boxで出典を分離している。 |
| P1 | 楕円核の有限次元性はL2正規直交列、楕円評価、Rellichで説明する必要がある。 | Pass for intended route | 第9章と付録Aで扱う設計。 |
| P1 | Spin^c構造の行列式接続とゲージ変換の係数2を章またぎでそろえる必要がある。 | Pass for convention | manifest `conv-sw-q` に規約を固定。 |
| P1 | SW随伴不等式、Taubes定理、Kähler還元は仮定と適用範囲を示す必要がある。 | Pass for source contract | 第18章契約、`thm-taubes`, `thm-adjunction`, `bb-taubes`, `bb-adjunction` に記録。 |

## Residual risk

研究級定理の完全証明は本書の前提を越えるため、本文ではproof depth C/Dとして扱う。数学的完成判定は、引用定理の仮定・結論・用途が明示され、本文内で初等的に検算できる部分が別に示されていることに依存する。

