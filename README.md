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

## Deploy

`main` branchへのpushでGitHub ActionsがQuartoサイトをビルドし、GitHub Pagesへ公開します。
