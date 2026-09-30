# AGENTS.md

このリポジトリは、既存教材をQuartoで公開する個人教科書ポータルである。教材本文を勝手に要約・改稿せず、忠実な移行と保守を優先する。

## 構造

- `index.qmd`: ポータルトップ。
- `<book-slug>/index.qmd`: 各教科書の入口。
- `<book-slug>/chapters/`: 各章の正本となる`.qmd`。
- `<book-slug>/assets/`: その教科書専用の画像・GIFなど。
- `shared/styles/`: サイト共通CSS/SCSS。
- `scripts/`: buildやvalidation補助。
- `.github/workflows/`: GitHub Pagesデプロイ。

## 教材追加方法

1. 英数字・ハイフンの安定した`<book-slug>`を決める。
2. `<book-slug>/index.qmd`、`<book-slug>/chapters/*.qmd`、必要なら`<book-slug>/assets/`を追加する。
3. `_quarto.yml`のnavbarとsidebarへ追加する。
4. 画像参照は原則として章ファイルから`../assets/file.ext`、indexから`assets/file.ext`にする。
5. `quarto render`と`python scripts/validate_site.py`を通す。

## 編集原則

- 元教材を勝手に削除しない。
- 教材本文を勝手に要約しない。
- 許可される変更は、Quarto frontmatter、画像パス、リンク修正、数式表示上必要な修正、軽微なタイポ修正に限る。
- Zenn由来の記法をQuartoで壊れる形のまま残さない。
- broken linkや存在しないローカル画像参照を残さない。

## 数式

- インライン数式は`$...$`、別行数式は`$$...$$`を使う。
- 長い数式はスマートフォンで横スクロールできるよう、CSSの`.math.display`設定を維持する。
- 定理・命題・証明ブロックを追加する場合は、元教材に該当構造が明確にあるときだけ行う。

## 画像

- 教科書固有画像は`<book-slug>/assets/`に置く。
- PNG/JPEG/WebP/GIF/SVGを対象に、存在・大文字小文字・相対パスを確認する。
- GIFは変換せず、アニメーションを維持する。

## Build / Preview / Validation

```powershell
quarto preview
quarto render
python scripts/validate_site.py
```

commit前に上記を実行し、必要なら`git status --short`で意図しない差分がないか確認する。

## Deploy

`main` branchへのpushで`.github/workflows/pages.yml`がQuartoをビルドし、GitHub Pagesへデプロイする。Actionsの権限はPages公開に必要な範囲に限定する。
