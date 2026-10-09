# Authoring Guide

このディレクトリは教材本文ではなく、本文を制作・監査するための契約である。正本は `production/manifest.json` と各章の `contracts/*.json` に置く。本文の見出しをmetadataから自動生成してはならない。

## 章を着手可能にする手順

1. `manifest.json` の該当章で数学的依存と教育的依存を分けて確認する。
2. `chapter-contract.schema.json` に沿って章契約を作る。
3. 中心問題、開始時点、前章からのbridge、次の疑問、証明深度、black box、図、sourceを埋める。
4. Reader Stop-Pointを予測し、`body`、`appendix`、`black_box` のいずれかへ解消先を割り当てる。`unresolved` はGate 3を失敗させる。
5. `python scripts/validate_gauge_authoring.py` を実行する。制作停止条件が一つでも残る章は本文を書かない。

## 本文生成ハーネス

執筆エージェントには、教材全体ではなく次の束だけを渡す。

```text
global specification
+ current chapter contract
+ referenced notation/conventions/assumptions
+ theorem and black-box dependencies
+ previous chapter exit state
+ unresolved bridges
+ relevant sources and figure briefs
+ review policy
```

本文は「既知事項 → 自然な疑問 → 既存方法の不足 → 新概念の必要性 → 定義と導出 → 意味 → 限界 → 次の疑問」の因果を持たせる。ただし、この列を見出しとして露出させない。

## レビューハーネス

レビューは次の順で行う。

1. **Missing Explanation First**: motivation、bridge、derivation、assumption、definition、distinction、interpretation、example、proof idea、前章接続、次章理由の欠落を先に列挙する。
2. **Reader Advocate**: 読者が外部へ質問したくなる地点を列挙し、本文・付録・意図的black box・説明不足に分類する。
3. **Mathematics**: 記号、型、次数、符号、仮定、定理status、expected/actual dimensionを照合する。
4. **Continuity**: 前章の出口と当章の入口、当章の未解決疑問と次章の入口を照合する。
5. **Rendering**: Web、狭幅、dark mode、PDFで数式・図・引用・リンクを確認する。

「standard」「well known」「generic」「one can show」を説明の代用にしてはならない。用いる場合は、何が標準か、何を動かすか、入力と出力は何かを同じ段落で示す。

## 独立監査

`python scripts/validate_gauge_authoring.py --audit-bundle dist/gauge-theory-audit` は、執筆者が編集する本文とは別に、manifest、章契約、検証結果、source hashをまとめる。監査者はbundleだけでGate 1〜6の機械検査結果を再確認し、Gate 7を人手で判定する。

## 図版

図の正本は `manifest.json` のfigure registryと再生成スクリプトである。4次元空間を無理に描かず、bundle、orbit、slice、分解、moduli、bubbling、compactification、理論間の論理を描く。alt text、mobile、dark-mode、生成方法、出典・ライセンスを欠く図は完成扱いにしない。

## PDF

WebとPDFは同じQMD正本から作る。`python scripts/build_gauge_theory_pdf.py` は章契約の順序でQMDを結合し、Typst PDFを生成する。`--check` は生成物を残さず、PDF経路だけを検証する。

