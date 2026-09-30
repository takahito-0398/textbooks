# Migration Report

作成日: 2026-10-01

## 調査対象

- 移行元: `takahito-0398/zenn-articles`
- 調査範囲: `articles/`, `books/`, `images/`, `content/`, README、frontmatter、本文、画像参照、関連QA資料
- 移行先: `takahito-0398/textbooks`

## 1. Navier-Stokes方程式

- 教材名: Navier-Stokes方程式を読む
- 移行元ファイル: `articles/navier-stokes-mathematical-notes.md`
- 関連ディレクトリ: `images/navier-stokes-mathematical-notes/`, `content/navier-stokes-mathematical-notes/`（QA・補助コード）
- 関連画像: fig-01.png, fig-02.png, fig-03.png, fig-04.png, fig-05.png, fig-06.png, fig-07.png, fig-08.png, fig-09.png, fig-10.png, fig-11.png, fig-12.png, fig-13.png, fig-14.png, fig-15.png, fig-16.png, fig-17.png, fig-18.png, fig-19.png, fig-20.png, fig-21.png, fig-22.png, fig-23.png, fig-24.png, fig-25.png
- 関連GIF: kh-rollup.gif
- 現在のMarkdown構造: Zenn記事の単一Markdown。第I部から第X部、付録までを`##`、各章を`###`中心で構成。
- 数式記法: `$...$`および`$$...$$`のLaTeX記法。
- Zenn固有記法の有無: frontmatterの`emoji`, `type`, `topics`, `published`、ルート相対`/images/...`参照、deploy triggerコメント。
- 画像パス: `/images/navier-stokes-mathematical-notes/...`
- 移行時の変換: Zenn frontmatter除去、Quarto frontmatter追加、`##`単位で章ファイル分割、画像参照を`assets/`または`../assets/`へ変換。
- 欠損・参照切れの可能性: 自動検査対象。調査時点で参照画像26件は移行対象に含めた。
- 移行後配置先: `navier-stokes/index.qmd`, `navier-stokes/chapters/*.qmd`, `navier-stokes/assets/`

## 2. Buffer Overflow / ROP

- 教材名: Buffer Overflow / ROP 入門
- 移行元ファイル: `articles/technical-buffer-overflow-to-rop.md`
- 関連ディレクトリ: `images/technical-buffer-overflow-to-rop/`, `content/technical-buffer-overflow-to-rop/`
- 関連画像: 01-execution-pipeline.png, 02-array-address-length.png, 03-process-memory-map.png, 04-instruction-cycle.png, 05-call-ret-four-states.png, 06-assembly-normal-state.png, 07-normal-abnormal-comparison.png, 08-assembly-abnormal-state.png, 09-capability-ladder.png, 10-code-placement.png, 11-defense-layers.png
- 関連GIF: なし
- 現在のMarkdown構造: Zenn記事の単一Markdown。導入、0-10章、補遺A-Dを`#`、節を`##`で構成。
- 数式記法: 主にコードブロック・表。数式は限定的。
- Zenn固有記法の有無: frontmatterの`emoji`, `type`, `topics`, `published`、ルート相対`/images/...`参照。
- 画像パス: `/images/technical-buffer-overflow-to-rop/...`
- 移行時の変換: Zenn frontmatter除去、Quarto frontmatter追加、`#`単位で章ファイル分割、画像参照を`assets/`または`../assets/`へ変換。
- 欠損・参照切れの可能性: 自動検査対象。調査時点でPNG 11件は移行対象に含めた。
- 移行後配置先: `buffer-overflow/index.qmd`, `buffer-overflow/chapters/*.qmd`, `buffer-overflow/assets/`

## 3. 非可換幾何

- 教材名: 作用素環論から非可換幾何へ
- 移行元ファイル: `books/operator-algebras/*.md`, `books/operator-algebras/config.yaml`
- 関連画像: なし
- 関連GIF: なし
- 関連ディレクトリ: `books/operator-algebras/`
- 現在のMarkdown構造: `config.yaml`に章順を持つZenn book形式。第0章から第14章、付録A-Eまで20ファイル。
- 数式記法: `$...$`および`$$...$$`のLaTeX記法。
- Zenn固有記法の有無: book用`config.yaml`、各章frontmatterの`title`。
- 画像パス: ローカル画像参照なし（推定: 本文は数式・表・外部参考リンク中心）。
- 移行時の変換: 各章frontmatterをQuarto frontmatterへ変換、`.md`から`.qmd`へ変換、章順をQuarto sidebarへ反映。
- 欠損・参照切れの可能性: 外部参考リンクはCIのローカルリンク検査対象外。ローカル画像欠損はなし。
- 移行後配置先: `noncommutative-geometry/index.qmd`, `noncommutative-geometry/chapters/*.qmd`

## 共通変換

- Quarto websiteとして `_quarto.yml` を作成。
- Light / Dark対応テーマを設定。
- 全文検索をQuarto標準検索で有効化。
- 数式はMathJaxでレンダリング。
- 長い数式・表・コードがモバイルで横にはみ出しにくいCSSを追加。
- GitHub Actionsで`main` push時にPagesへデプロイする構成を追加。
