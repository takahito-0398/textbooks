# 受入監査後の改訂ログ

対象は `gauge_theory_independent_acceptance_audit.md` と `gauge_theory_codex_revision_instructions.md` に基づく再改訂である。添付文書は制作指示として参照したが、反映先は `gauge-theory-smooth-topology` の編集可能原稿に限定した。二次元臨界現象、SLE、`rg-critical-phenomena`、`sle-critical-phenomena` は対象外である。

## 版と範囲

- 95ページ正本由来の18章構成、旧19図、追加された結び目手術図、40題、基礎演習12題を保持した。
- 48ページ版および旧22章圧縮構成は採用していない。
- 既存の公開PDF SHA-256 `5202cb3671f2ebd98f080e5f1ceccfe2ce8e10ebabb7f5569b40b74ec222d15c` を受入監査の入力版として扱い、編集原稿側でP1/P2/P3を修正した。

## P1対応

| ID | 対応 | 主な反映先 |
|---|---|---|
| GT-01 | ゲージ作用 `A^g=g^{-1}Ag+g^{-1}dg`、`g=e^φ` の無限小作用を `+d_Aφ` に統一し、Coulomb方程式を `d_A^*d_Aφ=-d_A^*a` に修正。BCH展開を二次項まで追加した。 | `chapters/07-gauge-quotient.qmd`, `chapters/08-deformation-complex.qmd`, `chapters/appendix-notation-exercises.qmd`, `production/math_conventions.md` |
| GT-02 | `A` を `det W^+` の接続とする規約で、Dirac線形化に `1/2 ρ(a)Φ` を入れ、ゲージ係数2・Weitzenböck係数との整合を明示した。 | `chapters/16-seiberg-witten-equations.qmd`, `chapters/appendix-notation-exercises.qmd`, `production/math_conventions.md` |
| GT-03 | Donaldson対角化の核心について、可約リンクを `S^3/S^1=CP^1` の有限次元模型で計算し、どこから格子ベクトルが出るか、どこを引用に残すかを分けた。 | `chapters/13-donaldson-outputs.qmd` |
| GT-04 | 40題のうち監査で重点指定された計算型問題を中心に、途中式、型、次数、適用条件を増補した。 | `chapters/appendix-notation-exercises.qmd` |
| GT-05 | 誤字、英日混成、用語対照表、エネルギー恒等式、層、接空間、破綻などの語を文脈に沿って修正した。 | `chapters/*.qmd`, `chapters/appendix-notation-exercises.qmd`, `chapters/appendix-analysis.qmd` |

## P2/P3対応の主な反映

- `E_8` 行列について、左上主小行列式 `2,3,4,5,6,7,8,1` による正定値性と `det=1` の検算を追加した。
- Donaldson多項式の `μ` 挿入について、スラント積の次数 `4-i`、点類4次、曲面類2次を演習解答で明示した。
- Hodgeの `3+3` 分解は、6基底と3組の自己双対・反自己双対基底を解答に追加した。
- SWコンパクト性は、Weitzenböck公式から最大値原理型の二次不等式、曲率制御、Coulombゲージ、楕円評価へ進む流れを解答に補った。
- Kähler面の正準Spin^c構造と線束ひねりを、解答でも `W^+=(Λ^{0,0}⊕Λ^{0,2})⊗E`、`det W^+=K^{-1}⊗E^2` と区別した。
- 随伴不等式はK3で `Σ^2=2n` のとき `g≥n+1` を導く数値例を追加した。

## 外部照合

- Torres, *Gauge Theory and 4-Manifolds*, §5.2 のSeiberg--Witten線形化で `1/2 ρ(a)φ` を確認した。
- 同資料のDonaldson対角化定理節で、定値交点形式の整数対角化、特性ベクトル、格子補題への橋渡しを確認した。
- 既存参考文献 `donaldson1983`, `donaldsonKronheimer1990`, `morgan1996` の役割は既存bibliographyの範囲に保持した。

## 未完了ではなく引用として残す部分

Donaldson対角化定理、Uhlenbeckコンパクト性、TaubesのSW=Gr、随伴不等式は、本教材内で完全証明しない。今回の改訂では、入力、出力、手計算模型、引用に残る難所を明示した。研究級定理の証明を有限次元模型で代替したとは主張しない。
