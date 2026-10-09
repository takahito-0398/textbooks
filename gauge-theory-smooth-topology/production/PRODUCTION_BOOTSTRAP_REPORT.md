# Production Bootstrap Final Report

作成日: 2026-10-08

## A. Environment

- 既存の `takahito-0398/textbooks` はQuarto websiteで、教材ごとのQMD、sidebar、共通CSS、reader UIを一つの `_quarto.yml` で統合する。
- `main` push時にGitHub Actionsがsource validation、Quarto render、GitHub Pages artifact upload、deployを行う。
- `CNAME` と既存の `https://textbooks.yohakostudio.com/` を維持し、新framework・本番依存・別repositoryは導入していない。
- Web数式はMathJax、PDFは既存方針に合わせQuarto + Typstを使う。

## B. Audit Ingestion

- 確定監査の中心問題、scope、18章curriculum、前提、二種類の依存、proof depth、black box、P0/P1説明欠落、図版、制作停止条件をmanifestへ変換した。
- Stage 2.5の150頁案は確定監査と不整合のため採用せず、Core 300〜380頁とAppendix 100〜150頁を自然な目安とした。
- Donaldson対角化、Donaldson多項式、smoothability obstruction、exotic pairを別の論理として管理する。
- SWは「簡単なDonaldson理論」ではなく、共通機械を持つ別の非線形moduli問題として扱う。

## C. Production Architecture

正本は `production/manifest.json` と `contracts/*.json` である。manifestが全体scope、curriculum graph、notation、convention、assumption、theorem、proof depth、black box、source、figure、Reader Question、moduli lifecycle、quality gateを保持する。章契約は章ごとの中心問題、開始状態、導出、結果、厳密性、Stop-Point、bridge、図、source、前後接続を固定する。

執筆時は全リポジトリではなく、global specification、当該章契約、必要registry、前章の出口、未解決bridge、sourceとfigure briefだけをcontextとして渡す。metadataを本文の見出しへ機械変換しない。

## D. Created Assets

- `gauge-theory-smooth-topology/`: portal入口、合成検証章、参考文献、authoring guide、schema、manifest、章契約、図版、PDF。
- `scripts/validate_gauge_authoring.py`: 依存順序、循環、registry参照、proof depth、black box契約、Stop-Point、引用、図版、停止条件を検査し、audit bundleを生成。
- `scripts/generate_gauge_figures.py`: dark mode対応SVGを決定的に再生成。
- `scripts/build_gauge_theory_pdf.py`: 同じQMD正本を章契約順に結合してTypst PDFを生成・検査。
- `tests/test_gauge_authoring.py`: 前方依存、未解消Stop-Point、未契約black boxを負例として検査。
- `_quarto.yml`、portal index、README、Pages workflowへ既存方式で統合。

## E. Quality System

Gate 1〜7を architecture、mathematics、explanation、continuity、sources、rendering、independent audit として固定した。Missing Explanation Firstをレビュー順序の先頭に置き、Reader Stop-Pointの `unresolved` を完成阻止条件にした。定理はA〜Dのproof depth、主張はdefinition/theorem/heuristic等のstatusを持つ。章間依存は数学的依存と教育的依存を別graphにし、未来参照と循環をvalidatorで拒否する。

## F. Visual System

figure registryはteaching objective、concept、asset type、generator、source/license、caption相当のalt、mobile、dark mode、再生成状態を保持する。4次元空間の外観ではなく、Hodge分解、gauge orbit、slice、moduli、bubbling、compactification、Donaldson/SWの論理構造を描く。合成章のHodge分解SVGで再生成とWeb/PDFの両経路を検証した。

## G. Validation

- `python scripts/validate_site.py`: PASS。
- `python scripts/validate_gauge_authoring.py --audit-bundle ...`: PASS。
- `python -m unittest tests.test_gauge_authoring`: 4 tests PASS。
- Python構文検査: PASS。
- 図版再生成前後のSHA-256一致: PASS。
- Quarto 1.10.18によるrepository全137 QMD render: PASS。
- Typst PDF check: PASS、A4 3頁、241,365 bytes。
- PDF全3頁をPNG化して目視確認: 日本語、数式、行列、cases、SVG、callout、引用、改ページ、ページ番号に欠け・重なりなし。
- ブラウザ実測: desktop 1280×720とmobile 390×844、dark mode、TOC、progress、previous/next、PDF link、SVG loadを確認。mobileではbody overflowなし。長いdisplay mathだけが意図どおり横スクロール可能。

## H. Red Team

検査実装後、Quarto cross-referenceの `@fig-*` と `@eq-*` を文献引用と誤認する欠陥を発見した。引用keyからcross-reference prefixを除外し、再テストした。前方依存、未解消Stop-Point、未登録black boxをそれぞれ破壊した負例がvalidatorを確実に失敗させることも確認した。

metadataを埋めるだけの品質偽装は自動検査だけでは防げないため、独立Reader Advocateが本文の実際の因果と説明密度を読む工程を残した。Part IV〜VIを前半と同一rubricで監査することを運用条件とする。

## I. Remaining Risks

- 数学的正しさ、定理statementの版と仮定、historical attributionは章ごとの一次資料照合が必要。
- 自然な説明、天下りの有無、後半の品質低下は完全自動化できない。
- mobile/dark modeの視覚監査は重要図版追加ごとに繰り返す必要がある。
- 合成章はpipeline検証用であり、正式本文の品質を保証するものではない。

## J. Production Readiness

**READY WITH CONDITIONS**

制作ラインはpilot chapterの執筆を開始できる。条件は、各章が章契約を先に確定し、重要主張を一次資料または標準文献へ照合し、Gate 7を執筆者と独立したReader Advocateが判定することである。教材本文の本制作は本bootstrapには含めていない。

