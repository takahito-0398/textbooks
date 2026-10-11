# Environment inventory

作成日: 2026-10-11

## Scope

対象は `textbooks/gauge-theory-smooth-topology` のみである。二次元臨界現象、SLE、`rg-critical-phenomena`、`sle-critical-phenomena` は調査・編集対象外とした。

## Repository and build system

- ルート: `C:/Users/takah/Desktop/main/programming/04_learning/math/textbooks`
- 対象教材: `gauge-theory-smooth-topology`
- サイト生成: Quarto website
- 対象教材入口: `gauge-theory-smooth-topology/index.qmd`
- 章本文: `gauge-theory-smooth-topology/chapters/*.qmd`
- 図版: `gauge-theory-smooth-topology/assets/figures/*.svg`
- 統合PDF: `gauge-theory-smooth-topology/assets/gauge-theory-smooth-topology.pdf`
- 章契約: `gauge-theory-smooth-topology/contracts/*.json`
- 制作規約: `gauge-theory-smooth-topology/authoring/README.md`
- 全体manifest: `gauge-theory-smooth-topology/production/manifest.json`

## Inherited production bootstrap

旧 `production-bootstrap` から継承する拘束条件は、章契約、Reader Stop-Point、proof depth A--D、black box契約、図版registry、検証スクリプト、Round 4/95ページレビューのP0/P1回帰防止である。旧bootstrapの本文fixtureや3ページPDFは正式本文ではなく、現在の反映先は `textbooks/gauge-theory-smooth-topology` 側の18章本文と95ページPDFである。

## Current editable sources

本文正本は抽出テキストではなく、次のQMD群である。

- 第1章から第18章: `gauge-theory-smooth-topology/chapters/01-*.qmd` から `18-*.qmd`
- 付録A: `chapters/appendix-analysis.qmd`
- 付録B: `chapters/appendix-notation-exercises.qmd`

## Recovery point

作業開始時点の `git status --short` は空であり、作業ツリーに未追跡・未コミット差分はなかった。旧資材ディレクトリは削除・移動していない。

## Reused commands

- `python scripts/validate_gauge_authoring.py`
- `python -m unittest tests.test_gauge_authoring`
- `python scripts/build_gauge_theory_pdf.py`
- `python scripts/validate_site.py`
- `quarto render gauge-theory-smooth-topology`

