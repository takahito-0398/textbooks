# 95ページ正本の復元記録

作業名は「95ページ正本への復元・増補改訂」とする。48ページ版は正本として採用しない。

## 復元元

- 編集可能原稿: `gauge-theory-smooth-topology/production/legacy-95p-sources`
- 復元先: `gauge-theory-smooth-topology/index.qmd`, `gauge-theory-smooth-topology/chapters`, `gauge-theory-smooth-topology/contracts`, `gauge-theory-smooth-topology/production/manifest.json`
- 参照PDF: `C:/Users/takah/Downloads/gauge-theory-smooth-topology.pdf`
- 参照PDFのSHA-256: `e8f3885897d5a74201b477275b7693b6b2025ab114d788ffbe691237dbf9cc49`
- 参照PDFのページ数: 95

## 退避

48ページ版の現行原稿、契約、生成PDF、関連スクリプト、制作記録は `gauge-theory-smooth-topology/production/rejected-48p-2026-10-12` に退避した。退避ファイルは正本として読まれないよう、本文ソースは `.bak` 形式で保存した。

## 復元確認

旧95ページ版に対応する18章構成と付録2本を復元した。復元後の章一覧は `01-smooth-structures.qmd` から `18-kahler-symplectic.qmd`、および `appendix-analysis.qmd`、`appendix-notation-exercises.qmd` である。

## 版識別条件

結び目手術の貼り合わせでは、トーラスの法線円周 `μ_T` を結び目の標準ロンジチュード `λ_K` に対応させる版を正とする。この条件は復元後の本文とPDF抽出結果で確認する。

