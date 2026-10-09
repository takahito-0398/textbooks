# AI教科書ポータル

Quarto + GitHub Actions + GitHub Pagesで公開する個人教科書ポータルです。

- 公開URL: https://textbooks.yohakostudio.com/
- Repository: https://github.com/takahito-0398/textbooks

## ローカル環境

Quarto CLIをインストールします。GitHub Actionsでは`quarto-dev/quarto-actions/setup`を使います。

## Preview

```powershell
quarto preview
```

## Build

```powershell
quarto render
```

## Validation

```powershell
python scripts/validate_site.py
```

## 楕円曲線・BSD教材のPDF

Web版と同じQMD正本から、手元保存用PDFを生成します。

```powershell
python scripts/build_bsd_pdf.py
```

出力先は `dist/elliptic-curves-bsd.pdf` です。Quarto CLI 1.10以降と、日本語を含むシステムフォントが必要です。

## 逆スペクトル幾何教材のPDF

Web版と同じQMD正本から生成します。

```powershell
python scripts/build_inverse_spectral_geometry_pdf.py
```

公開・ダウンロード用PDFは `inverse-spectral-geometry/assets/inverse-spectral-geometry.pdf` に出力されます。

## 4次元ゲージ理論教材

本文執筆前の章契約・依存関係・記法・定理・ブラックボックス・図版・出典を検証します。

```powershell
python scripts/validate_gauge_authoring.py
python -m unittest tests.test_gauge_authoring
python scripts/generate_gauge_figures.py
python scripts/build_gauge_theory_pdf.py
```

監査提出物は `python scripts/validate_gauge_authoring.py --audit-bundle dist/gauge-theory-audit` で生成します。

## 二次元臨界現象とSLE教材の制作基盤

全18章の疑問鎖、数学的・教育的依存、記法、定理status、black box、図版、出典、Reader Stop-Pointを検証します。

```powershell
python scripts/generate_sle_figures.py
python scripts/sle_authoring.py validate
python -m unittest tests.test_sle_authoring
python scripts/build_sle_pdf.py
```

執筆contextは `python scripts/sle_authoring.py context fixture-00 --output tmp/sle-context.md`、独立監査bundleは `python scripts/sle_authoring.py audit --output dist/sle-audit` で生成します。

## 新しい教科書の追加

1. `<slug>/index.qmd` と `<slug>/chapters/*.qmd` を追加する。
2. 画像は `<slug>/assets/` に置き、相対パスで参照する。
3. `_quarto.yml` のnavbarとsidebarへ追加する。
4. `quarto render` と `python scripts/validate_site.py` を実行する。

## 掲載教材

- Navier-Stokes方程式を読む
- Buffer Overflow / ROP 入門
- 作用素環論から非可換幾何へ
- 複素多様体・複素幾何
- 繰り込み群・臨界現象――ミクロを忘れて普遍性を得る
- 楕円曲線の有理点と Birch–Swinnerton-Dyer 予想
- 逆スペクトル幾何
- 4次元ゲージ理論と滑らかな位相
- 二次元臨界現象とSLE（制作基盤検証中）

## Deploy

`main` branchへのpushでGitHub ActionsがQuartoサイトをビルドし、GitHub Pagesへ公開します。
