# リリース検証

## 生成経路

編集正本は `gauge-theory-smooth-topology/index.qmd`、`gauge-theory-smooth-topology/chapters`、`gauge-theory-smooth-topology/contracts`、`gauge-theory-smooth-topology/production/manifest.json` である。配布PDFは `gauge-theory-smooth-topology/assets/gauge-theory-smooth-topology.pdf` とする。

## 復元段階

参照PDFは95ページで、SHA-256は `e8f3885897d5a74201b477275b7693b6b2025ab114d788ffbe691237dbf9cc49` だった。復元後のビルド、PDF比較、Web確認、全ページ視覚確認はこの記録へ追記する。

復元直後のPDFは95ページで、参照PDFと `pdftotext -layout` の抽出テキストが完全一致した。

## 増補後検証

- `python scripts\validate_gauge_authoring.py --audit-bundle gauge-theory-smooth-topology\production\post-augmentation-validation-bundle`: PASS
- `python scripts\build_gauge_theory_pdf.py`: PASS
- `pdfinfo gauge-theory-smooth-topology\assets\gauge-theory-smooth-topology.pdf`: 98ページ
- `quarto render gauge-theory-smooth-topology`: PASS
- `python -m unittest tests.test_gauge_authoring`: 8 tests PASS
- `python scripts\validate_site.py`: PASS
- `pdftoppm -png -r 90`: 98ページをレンダリング生成
- 独立監査: 初回P1。`_site` に残っていた旧22章HTMLを削除し、Webを再生成。旧章HTML残存0件、旧章参照0件を確認。

PDFの最終SHA-256は `5202cb3671f2ebd98f080e5f1ceccfe2ce8e10ebabb7f5569b40b74ec222d15c`。

## 公開状態

この作業では、外部へのpushやデプロイは実行結果で確認できた場合だけ公開済みと記録する。

ローカルのQuarto出力 `_site/gauge-theory-smooth-topology/index.html` はクリーン再生成済み。外部へのpushまたはGitHub Pagesデプロイは、まだ実行結果を確認していないため未公開。

