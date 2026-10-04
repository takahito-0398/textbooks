# AI教科書ポータル

Quarto + GitHub Actions + GitHub Pagesで公開する個人教科書ポータルです。

- 公開URL: https://takahito-0398.github.io/textbooks/
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

## Deploy

`main` branchへのpushでGitHub ActionsがQuartoサイトをビルドし、GitHub Pagesへ公開します。
