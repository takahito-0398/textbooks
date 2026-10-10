# Independent Audit

判定日: 2026-10-10

## 現在の判定

- Infrastructure check: Quarto HTML render PASS / Quarto Typst PDF render PASS
- Textbook content completeness: Content Accepted Candidate
- Publication acceptance: Publication Ready Candidate / Independent Final Audit Pending

Quarto による HTML と Quarto Typst による PDF は生成済みである。独立監査者による最終確認は未完了であるため、Complete 判定とは分離する。

## 履歴メモ

旧判定語 `Infrastructure PASS / Textbook Content Major Revision` は履歴としてのみ残す。現在判定として使ってはならない。特に「PDF が通っている」と読める表現は現状と一致しない。

## 修整後の暫定判定

- Infrastructure check: Quarto HTML render PASS / Quarto Typst PDF render PASS
- Textbook content completeness: MAJOR REVISION ADDRESSED IN DRAFT; SELF-AUDIT LOOP ACTIVE
- Long-form pedagogical acceptance: CONTENT ACCEPTED CANDIDATE / INDEPENDENT FINAL AUDIT PENDING

今回の修整では、第1〜5章を Loewner 方程式と Brown 駆動の必然性を説明する導入部として増補し、第7〜15章の証明状態、停止時刻、収束証明の構造、模型対応表を補った。続く二次改稿で、第1〜5章に探索経路の逐次生成、同じ trace で異なる curve の例、飲み込みと通過の違い、標準化の自由度、半平面容量の手計算、短時間増分の合成則、離散の領域マルコフ性と連続の領域マルコフ性の違い、連続なレヴィ過程から Brown 運動へ至る説明を追加した。さらに第6〜18章へ、Brown 駆動の粗さ、Bessel 境界値問題、幾何相、伊藤補正、左側通過確率公式、Green estimate、収束証明の流れ、percolation / LERW の観測量、Ising / FK-Ising / SAW の証明状態、GFF 結合、CLE / CFT / LQG の出口整理を追加した。付録では Brown 運動、伊藤計算、Carathéodory 収束、数値実験仕様、Reader Stop-Point チェックリストを補った。独立再監査の指摘は取り込み済みだが、PDF・正式Web・ポータル統合の確認前なので最終合格ではない。

## 独立再監査の取り込み

`INDEPENDENT_REAUDIT_2026-10-10.md` と `INDEPENDENT_REAUDIT_2026-10-10_UPDATE2.md` の判定は Conditional Go / Content Accepted Candidate であり、Complete ではない。取り込み対象は、PDF未検証の明示、正式レンダリング未確認の分離、drift 排除の補強、レヴィ過程表記の統一、収束位相の橋、主要主張の文献注、図版 status の実体一致、日本語化、未検証PDFの隔離である。

## 新しい自己監査合格条件

次をすべて満たさない限り、教材を COMPLETE / PASS としてはならない。

1. 最初の30〜45ページで、読者が Loewner 方程式と Brown 駆動の必然性を説明できる。
2. Loewner equation が定義として突然出ていない。
3. Brown 運動が「有名だから」ではなく、領域マルコフ性、等角不変性、スケーリング不変性、連続性から強制されている。
4. curve / trace / hull / Loewner chain / 駆動関数を混同していない。
5. SLE 分類問題と、格子模型のスケーリング極限証明を混同していない。
6. percolation と LERW について、SLE 収束証明の骨格が読者に追える。
7. Ising / FK-Ising / UST / SAW の証明状態が、定理、予想、発展項目として明確に分離されている。
8. CFT / CLE / LQG が本編を薄めていない。
9. 発見的説明、定理、外部定理、予想、数値的証拠の区別が本文で読める。
10. 日本語として不自然な英単語混在が減っている。
11. 主要概念に必要な図、模式図、数値実験仕様がある。
12. PDF ページ数ではなく、Reader Stop-Point が実際に解消されていることを根拠に acceptance している。

## Reader Stop-Point 監査

| Stop-Point | 修整 |
|---|---|
| Loewner 方程式が突然出る | 縦スリット写像、無限遠展開、微分、合成則から導入した。 |
| 「等角不変だから Brown 運動」という飛躍 | 領域マルコフ性、容量時間、平行移動、独立増分、定常増分、連続なレヴィ過程、スケーリングの順に分解した。 |
| curve と hull の混同 | 第2章で curve / trace / hull / 駆動関数を例と表で分離した。 |
| trace が通ることと hull が飲み込むことの混同 | 第2章に、弧の内側の点が trace 上になくても hull に入る例を追加した。 |
| 半平面容量が長さに見える | 第3章に縦スリットの容量 \(\operatorname{hcap}([0,ih])=h^2/2\) を追加した。 |
| 一般 Loewner 方程式への飛躍 | 第4章に短時間増分写像 \(\phi_{t,\Delta t}\) と合成則を追加した。 |
| 領域マルコフ性だけで Brown 運動になるように見える | 第5章に、標準化、容量時間、先端平行移動、等角不変性が必要であることを追加した。 |
| SLE 定義と格子模型収束の混同 | 第5章と第12章で分類と収束証明を分離した。 |
| martingale / 伊藤計算の目的化 | 第9章で「条件付き確率を保存する道具」として導入した。 |
| percolation の \(\kappa=6\) が見た目由来に見える | 第13章で Smirnov 観測量、Cardy 公式、locality の位置づけを追加した。 |
| LERW と UST の関係が表だけに見える | 第14章で loop-erasure の領域マルコフ性、Green 関数、Wilson のアルゴリズム、UST Peano との関係を追加した。 |
| CFT / LQG の権威語化 | 第18章を発見的対応表と出口章に抑えた。 |
| 普遍性の証明済み部分と予想部分の混同 | 第15章に証明状態表を置いた。 |

## 自己監査ループ記録

2026-10-10 の追加ループでは、独立再監査の R-01、R-03〜R-16 を本文・監査文書・制作メタデータへ取り込んだ。具体的には、旧検証ファイルの無限定な合格表示を、限定された `html-fallback-check: PASS` へ置き換え、PDF未生成と正式レンダリング未確認を明示した。第5章では drift 排除を容量時間スケーリングの式で補強し、第10章では停止時刻と境界条件を追加した。第1〜18章には章末の「本章の到達点」を置き、章間の論理接続を監査可能にした。図版生成スクリプトとSVGラベルも日本語寄りに更新した。

このループ後の内容判定は Content Accepted Candidate である。Quarto HTML と Quarto Typst PDF は生成済みだが、第三者による最終確認が未実施であるため、Complete とはしない。

### 現行版の自己監査結果（2026-10-10）

`scripts/self_audit.py` を現行の `index.qmd`、`dist/index.html`、`dist/sle-critical-phenomena.pdf` に対して実行し、10項目すべてに合格した。

- 本文文字数: 51,595字
- Reader Stop-Point: 欠落なし
- 数式区切り: Quarto対応形式のみ
- 登録概念・図版・証明状態: 整合
- 正式HTML: PASS
- 正式PDF: Quarto Typst、50ページ、PASS
- 総合: `SELF_AUDIT=PASS checks=10/10`

これは自己監査の合格であり、第三者による独立最終監査の sign-off とは分けて記録する。

2026-10-10 UPDATE2 の取り込みでは、PDF検証済みと誤読される古い監査文言を現在判定へ置換し、`production.json` の `required_statement` を更新した。また、第12章に Kemppainen-Smirnov 型枠組みの引用を追加し、第13章・第14章の見出しを日本語化し、Bessel 次元比較の中間式と local set の用語方針を補った。旧PDFは `tmp/previous-build-publish-stale/` に退避し、現行配布物ではないことを明示した。

## 残る制約

- この監査は自己監査であり、独立監査者の最終 sign-off ではない。
- Quarto Typst により現行PDFを生成した。Quarto は日本語を含むワークスペースパスで Lua 読み込みに失敗したため、ASCII 一時パスでレンダリングして `dist/` へ反映した。
- `tmp/previous-build-publish-stale/sle-critical-phenomena.previous-build.pdf` は旧ビルドの退避物であり、公開対象の `dist/` には含めない。
