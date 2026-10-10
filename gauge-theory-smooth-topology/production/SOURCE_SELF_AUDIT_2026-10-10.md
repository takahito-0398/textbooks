# Source Self-Audit - 2026-10-10

## 判定

SOURCE PASS。

この判定は、本文ソース、chapter contract、manifest、citation、figure registry、HTML renderを対象とする。統合PDF生成、PDF目視QA、公開・publish QAはまだ含めない。ユーザー方針により、PDFは元ソースが揃った後にまとめて生成する。

## 監査対象

- `gauge-theory-smooth-topology/chapters/*.qmd`
- `gauge-theory-smooth-topology/contracts/*.json`
- `gauge-theory-smooth-topology/production/manifest.json`
- `gauge-theory-smooth-topology/references.bib`
- `gauge-theory-smooth-topology/assets/figures/*.svg`
- `scripts/generate_gauge_figures.py`
- Quarto HTML render output

## 監査結果

### 1. Curriculum / continuity

PASS。

全18章と付録A/Bが存在し、章間の論理は以下の流れで接続されている。

1. smooth structureの比較問題
2. intersection form
3. Freedman / Donaldsonの衝突
4. 接続・曲率・Chern--Weil
5. 4次元Hodge分解
6. ASD方程式
7. gauge quotient
8. deformation complex
9. Fredholm index
10. Kuranishi / regularity
11. bubbling
12. invariant machine
13. Donaldson出力
14. topological分類とsmooth分類の照合
15. Spin-c / spinor
16. Seiberg--Witten方程式
17. Donaldson/SW比較
18. Kähler / symplectic / Taubes / adjunction

章境界のtopic jumpは残っていない。各章末は次章の必要性へ接続している。

### 2. Missing Explanation / Reader Stop-Point

PASS。

過去監査で重大だったStop-Pointは本文に反映済み。

- 非平滑化可能性とexotic pairの違い: Chapter 1, 3, 14で反復して整理。
- 自己交点の意味: Chapter 2でnormal bundleの押し出しとして説明。
- 整数格子と実形式の違い: Chapter 2で $H$ と $I_{1,1}$ を比較。
- $E_8$ 衝突の論理: Chapter 3で推論形式を明記。
- 接続が必要な理由: Chapter 4で普通の微分の破綻から導入。
- Hodge符号と交差項: Chapter 5で計算を展開。
- ASD方程式の必然性: Chapter 6で和と差の最小化として導出。
- gauge quotient / reducible: Chapter 7で有限次元模型と自明接続例を追加。
- deformation complex / ellipticity: Chapter 8でsymbol計算を展開。
- indexとactual dimensionの違い: Chapter 9--10で明示。
- orientation / determinant line: Chapter 9, 10, 12, Appendix Aで接続。
- compactification / gluing: Chapter 12, Appendix Aで接続。
- Donaldson diagonalizationとpolynomialの違い: Chapter 13で分離。
- Freedman照合とsmooth invariant照合: Chapter 14で証明パターン化。
- Spin-c構造の必要性: Chapter 15でtorsorと $\mathbb{CP}^2$ 例を追加。
- SW expected dimension: Chapter 16で $\mathbb{CP}^2$ 代入例を追加。
- Donaldson/SW比較: Chapter 17で失敗モード別に整理。
- Kähler還元 / Taubes / adjunction: Chapter 18で図と具体計算例を追加。

### 3. Mathematical correctness / proof depth

PASS for source level。

定理・証明深度はmanifestと本文で一致している。

- 完全導出: intersection form、Hodge分解、energy identity、ASD implies Yang--Mills。
- 本質的証明: ASD deformation complex、symbol exactness、Fredholm有限次元性。
- Proof architecture: slice、Kuranishi、Uhlenbeck、Donaldson diagonalization、SW compactness。
- Black Box: Freedman classification、Taubes SW=Gr、adjunction inequalityの深部。

Black Boxは、入力・出力・難所・下流での用途を本文または付録に明示している。

### 4. Rigorous / heuristic status

PASS。

definition、theorem、proof architecture、black-box theorem、heuristic、physical prediction / Witten予想の区別は本文上で混同していない。Chapter 17ではDonaldson/SW対応を無条件定理として扱わず、Wittenの物理的予想と厳密に使う範囲を分けた。

### 5. Sources

PASS。

`references.bib` と manifest に、本文で必要な主要source coverageを登録済み。

- Donaldson--Kronheimer
- Freed--Uhlenbeck
- Freedman
- Donaldson diagonalization
- Donaldson polynomial
- Witten SW
- Morgan SW
- Taubes SW=Gr
- Kronheimer--Mrowka adjunction
- Atiyah--Singer
- Sard--Smale
- Gompf--Stipsicz

authoring validatorでcitation / contract整合性は通過している。

### 6. Visual assets

PASS。

再生成可能なSVGを `scripts/generate_gauge_figures.py` で生成する。

主要図:

- category-layers
- hodge-split
- gauge-slice
- bubbling
- donaldson-sw
- sw-equations
- adjunction
- kahler-reduction
- taubes-limit
- gluing
- orientation-line

manifestにalt text、mobile、dark mode、generator、licenseを登録済み。

### 7. Exercises / appendix

PASS for source level。

Appendix Bは40問に拡張済みで、Part I--Vを横断する確認問題・計算問題・概念比較問題・略解を含む。Appendix AはSobolev/Fredholmだけでなく、orientation、gluing、characteristic classes、Spin-c構造の参照にも使える。

### 8. Rendering / validation

PASS for HTML source stage。

直近検証:

- `python scripts/validate_gauge_authoring.py --audit-bundle dist/gauge-theory-audit`: PASS
- `python -m unittest tests.test_gauge_authoring`: PASS
- `python scripts/validate_site.py`: PASS
- `quarto render gauge-theory-smooth-topology`: PASS

また本文中の `qquad` は `\quad` へ統一し、既知のTypst/PDF互換リスクを減らした。

## 残作業

SOURCE PASS後の残作業は、本文改善ではなく最終成果物化フェーズである。

1. 統合PDFを生成する。
2. PDFを目視QAする。
3. Web / mobile / dark modeをspot checkする。
4. portal integrationとpublish pathを確認する。
5. 必要ならGitHub Pages publishまで進める。

## 結論

教材ソースは、Production Bootstrapと監査レポートで要求された主要な本文・章契約・出典・図版・演習・解析付録・Reader Stop-Pointを反映している。現時点で、ソース制作フェーズはPASSとする。次工程はPDF生成と公開QAである。

