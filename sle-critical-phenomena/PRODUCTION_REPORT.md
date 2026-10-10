# Production Report

判定日: 2026-10-10

## 結論

旧 bootstrap の PASS は、Infrastructure check であって教材完成判定ではない。今回の修整では、自己監査基準を更新し、本文を長編教材の初稿として増補した。

## 変更内容

- `INDEPENDENT_AUDIT.md` を作成し、旧 PASS 判定を無効化した。
- `authoring/production.json` に新しい合格条件、用語、日本語化、証明状態、図版 registry を追加した。
- `authoring/README.md` に完成判定と執筆ルールを明記した。
- `index.qmd` を本文正本として作成し、第1〜18章を Major Revision 方針で再構成した。
- 第1〜5章を、percolation 探索経路から Brown 駆動までの導入部として重点増補した。
- 第7〜11章に Bessel 閾値、マルチンゲール生成作用素、左側通過確率公式、Hausdorff 次元の証明設計図を追加した。
- 第12〜14章に収束証明の点検項目、percolation -> SLE6、LERW -> SLE2 の骨格を追加した。
- 第15章に Ising、FK-Ising、UST、SAW、一般普遍性の証明状態を分離する表を追加した。
- 第16〜18章で GFF は本編に残し、CLE / CFT / LQG は出口章として抑制した。
- 図版・数値実験仕様を追加し、静的 HTML と PDF の生成スクリプトを作成した。
- 継続作業として第1〜5章を二次改稿し、Dobrushin 探索経路の逐次性、曲線 / trace / hull の具体例、半平面容量の手計算、Loewner 方程式の合成則、離散の領域マルコフ性と連続の領域マルコフ性の差、連続なレヴィ過程から Brown 運動へ至る説明を追加した。
- さらに第6〜18章を増補し、Brown 駆動の粗さ、Bessel 境界値問題、SLE 幾何相、マルチンゲール生成作用素、左側通過確率公式、Hausdorff 次元の Green estimate、収束証明の流れ、percolation / LERW の観測量、普遍性の境界、GFF 結合、CLE / CFT / LQG の出口整理を追加した。
- 付録A〜Eを追加し、Brown 運動と連続なレヴィ過程、伊藤計算と停止時刻、等角写像と Carathéodory 収束、数値実験仕様、Reader Stop-Point チェックリストを整理した。
- 独立再監査を取り込み、PDF未検証の限定表現、正式レンダリング未確認の分離、drift 排除の補強、収束位相の橋、文献注、図版 status の実体一致、日本語用語の追加修正を行った。
- 追加の自己監査ループとして、第1〜18章へ章末の到達点を追加し、左側通過確率公式の停止時刻、図版ラベルの日本語化、英単語混在の削減を行った。
- 独立再監査 UPDATE2 を取り込み、古いPDF通過表現を削除し、`production.json` の `required_statement` を現行判定へ更新した。
- 第12章に Kemppainen-Smirnov 型枠組みの引用を追加し、第13章・第14章の見出しを日本語化し、Bessel 計算の中間式と local set の用語方針を補った。
- 旧PDFを `tmp/previous-build-publish-stale/sle-critical-phenomena.previous-build.pdf` へ退避し、公開対象の `dist/` から外した。

## 検証と公開

実行した検証は `dist/verification.txt` に記録する。現行の公開物は Quarto により生成した `dist/index.html` と、Quarto Typst により生成した `dist/sle-critical-phenomena.pdf` である。Quarto は日本語を含むワークスペースパスで Lua 読み込みに失敗したため、ASCII 一時パスでレンダリングして `dist/` へ反映した。

現行の自己監査は `scripts/self_audit.py` により `SELF_AUDIT=PASS checks=10/10`。正式PDFは50ページで、代表ページの目視確認でも数式、図版、目次、改ページの崩れは確認されなかった。

## 未完了事項

- 第三者による Gate 7 独立監査。
- 全章を 120〜180 ページ相当までさらに拡張する追加改稿。
- 独立監査者による最終確認。
- PDFの全ページ目視確認と、図版・数式・目次・リンク・改ページの追加確認。

## 現在の判定

- Infrastructure check: Quarto HTML render PASS / Quarto Typst PDF render PASS
- Textbook content completeness: MAJOR REVISION ADDRESSED IN DRAFT; CHAPTER ACCEPTED CANDIDATE
- Long-form pedagogical acceptance: CONTENT ACCEPTED CANDIDATE / INDEPENDENT FINAL AUDIT PENDING
