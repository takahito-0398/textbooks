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

復元直後に `python scripts\build_gauge_theory_pdf.py` でPDFを再生成した。生成PDFは95ページで、`pdftotext -layout` による抽出テキストのSHA-256は参照PDFと同一だった。

- 参照PDF抽出テキストSHA-256: `c45c89d366641f2d4dd082a7b8ccb42b842e5e6a221cbaa322647a7b8930254a`
- 復元PDF抽出テキストSHA-256: `c45c89d366641f2d4dd082a7b8ccb42b842e5e6a221cbaa322647a7b8930254a`
- 抽出行数: 4996行で一致

## 版識別条件

結び目手術の貼り合わせでは、トーラスの法線円周 `μ_T` を結び目の標準ロンジチュード `λ_K` に対応させる版を正とする。この条件は復元後の本文とPDF抽出結果で確認する。

復元後の `chapters/14-topological-vs-smooth.qmd` とPDF抽出テキストで、`μ_T` が `λ_K` に対応し、`μ_K` との取り違えが標準的なFintushel-Stern結び目手術ではないと明記されていることを確認した。

## 増補後の生成物

増補後のPDFは `gauge-theory-smooth-topology/assets/gauge-theory-smooth-topology.pdf` に生成した。

- ページ数: 98
- PDF SHA-256: `5202cb3671f2ebd98f080e5f1ceccfe2ce8e10ebabb7f5569b40b74ec222d15c`
- 生成時刻: 2026-10-12 00:31頃

