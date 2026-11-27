# 『位相的K理論を読む』改訂版の制作・検証記録

改稿の基点は初版の公開コミット `69950f9994807bef75aa4e6ca17d239761061fd4`。同じ章原稿からHTMLとPDFを生成する。入口は `index.qmd`、本文は `chapters/00-*.qmd` から `21-*.qmd`。序章を含む22章に361個の別行数式を置いた。うち312式に番号があり、本文の式・図・表参照は章内326件、章をまたぐ式参照は3件。図は23点を作図して24か所に置き、表は14点を組んだ。

## 再生成

PDFはA5判二段組。本文9.3 pt、段間5 mm、天・地13 mm、左右11 mm。表紙と一頁の目次を含む104頁で、本文は3〜104頁の102頁。式が段幅を超える場合はTypstで縮尺を調整する。PDFの式番号は全巻通し、HTMLの式番号は章内通し。章をまたぐ参照の行先は両方で同じ式にそろえた。

Windowsの Python 3.13.14、Quarto 1.11.9、同梱のTypst 0.15.1、Pillow 13を使用。日本語本文と見出しは Yu Mincho と Yu Gothic。Pillowは図を再作図するときに使う。PDF生成時は段組の設定で指定したフォントも利用できる状態にする。

```powershell
python topological-k-theory/production/verify_examples.py
python topological-k-theory/production/verify_edition.py
python topological-k-theory/production/draw_figures.py
python scripts/build_topological_k_pdf.py
quarto render
python scripts/validate_site.py
```

Quartoの実行ファイルを明示する場合はPDF生成コマンドに `--quarto` を加える。図の書体ファイルは `draw_figures.py --font` で指定できる。PDF生成時に各章と成果物のSHA-256を出力する。再生成でPDFのメタデータが変わり得るため、その場合は配布するファイルからハッシュを取り直す。

配布PDFのSHA-256は `23159f4a51ff338b23cce82c38f88ece098f8ef39ca679961eeee31d0b32263a`。

## 数学の確認

| 対象 | 確認した計算 |
|---|---|
| 貼り合わせ・Thom・指数の導入 | 北・南での巻き数の符号、Koszulの境界同型、射影直線のLaurent係数とTodd積分を照合した。 |
| セル濾過とレンズ空間 | 関係行列の全小行列式を使って五つの例のSmith不変因子を再計算した。実射影5次元空間の縮約群は位数4。 |
| 射影空間のRiemann–Rochと対角線 | 次元1〜8でTodd級数と指数関数の有理積を一般化二項係数と照合した。同じ範囲で指数対合行列と対角線の係数行列の積を検査した。 |
| 族の指数 | 射影直線束上で負次数の余核束から得る一次成分を、ファイバー積分の多項式と比較した。 |
| トーラスの指数 | 両符号の次数について、Gaussianの係数比が境界条件の漸化式を満たすことを確認した。 |

原稿は各章の参考欄と該当する証明箇所に使用した結果を記す。主要な借用は、Bott積定理の証明の構成、セル濾過のスペクトル系列、指数定理と族への拡張、Clifford加群による実Thom類。数値・多項式の検算は、これらの一般定理の証明の独立した査読を含まない。 [Hatcher, Vector Bundles and K-Theory](https://pi.math.cornell.edu/~hatcher/VBKT/VB.pdf) [Atiyah–Hirzebruch, Vector Bundles and Homogeneous Spaces](https://ncatlab.org/nlab/files/AtiyahHirzebruch61.pdf) [Atiyah–Singer III](https://annals.math.princeton.edu/1968/87-3/p07) [Atiyah–Singer IV](https://annals.math.princeton.edu/1971/93-1/p03) [Atiyah–Bott–Shapiro, Clifford modules](https://doi.org/10.1016/0040-9383(64)90003-5)

## 組版と配信の検査

- PDFは全ページの縮小一覧に加え、序章、実射影空間の濾過、レンズ空間の表、四次元曲面の指数比較などを拡大確認した。図の記号欠落、表の見出しの重なり、参照記号がそのまま印字される箇所を修正した。
- 抽出したPDFテキストに未解決の式・図・表参照記号がないことを確認した。組版ログにTeX変換警告は0件。数式フォントを含む行の段間と紙面外へのはみ出しを検査した。目次の22リンクを各章の開始頁と照合し、文書内リンクの行先を検査した。Popplerで日本語・数式のフォント埋め込みを確認した。
- HTMLは入口と全章を対象に、幅320・390・1366 pxのEdgeで数式表示、図の読み込み、参照先、ページ全体の横幅を検査した。式・図・表の329リンクについて行先が存在することをHTMLでも確認した。全サイト236ページのレンダリング、サイトのリンク検査、既存のゲージ理論・SLEの検証はすべて成功した。
- 独立試読、紙への印刷、Edge以外のブラウザーの表示は未検証。
