# SLE教材 Production Bootstrap

ここは教材本文ではなく、本文を安定して制作・監査するための正本である。全体仕様は `production.json`、各章の着手契約は `contracts/*.json` に置く。metadataを本文見出しへ機械的に変換してはならない。

## 制作順序と実行単位

1. `production.json` でscope、数学的依存、教育的依存、記法、規約、定理status、source、図版を確認する。
2. `chapter-contract.schema.json` に沿って章契約を作る。
3. Reader Stop-Pointを `body`、`appendix`、`black_box` のいずれかへ割り当てる。`unresolved` が残る章は執筆しない。
4. 次のコマンドで執筆用contextを生成する。

```powershell
python scripts/sle_authoring.py context fixture-00 --output tmp/sle-fixture-context.md
```

5. 本文作成後、検証とレビュー票生成を行う。

```powershell
python scripts/sle_authoring.py validate
python scripts/sle_authoring.py review fixture-00 --output tmp/sle-fixture-review.md
```

本番では、原則としてユーザー確認を章ごとに挟まない。エージェントが、依存関係に従って複数章または指定された制作範囲を連続して、章契約作成、本文執筆、内部レビュー、修正、Web/PDF確認まで完了させる。ユーザーへ途中確認を求めるのは、scope変更、数学的に解消できない矛盾、外部資料・権限が必要なブロッカーがある場合だけとする。通常のReader Stop-Pointや数式修正はエージェントが自律的に処理し、最後にまとめて結果を報告する。

検査は章ごとに内部実行するが、それはユーザーとの停止点ではない。全範囲を作り切った後に、全章を横断してnotation、terminology、theorem status、bridge、後半の説明密度、Web/PDFを再監査する。

## 執筆ハーネス

執筆者へ渡すcontextは、全教材を無差別に含めず、次だけに限定する。

```text
global specification
+ current chapter contract
+ mathematical and pedagogical prerequisites
+ referenced notation / conventions / normalizations
+ theorem and black-box dependencies
+ previous chapter exit question
+ unresolved bridges
+ relevant sources and figure briefs
+ review policy
```

各節は、既知事項から自然な疑問を立て、既存の方法の不足を実際に見せてから新概念を導入する。これは内部設計であり、「現在わかっていること」「新概念」などの定型見出しを本文へ露出させない。

## レビューハーネス

レビュー順は固定する。

1. **Missing Explanation First**: motivation、bridge、derivation、assumption、definition、distinction、interpretation、example、proof idea、前章接続、次章理由の欠落を列挙する。
2. **Reader Advocate**: 外部へ質問したくなる地点を抽出し、本文・付録・意図的black box・説明不足へ分類する。
3. **Mathematics**: 記法、係数、符号、仮定、status、規約をregistryと照合する。
4. **Continuity**: 前章の出口と当章入口、当章の出口と次章入口を照合する。
5. **Sources**: 深い主張を一次資料または標準文献へ追跡する。
6. **Rendering**: Web、375px幅、dark mode、PDFで数式・図・引用・リンクを確認する。

「明らか」「容易」「よく知られている」「one can show」を説明の代用にしてはならない。使う場合は、直後に入力、許される操作、結論、参照先のいずれかを明示する。

## 独立監査

```powershell
python scripts/sle_authoring.py audit --output dist/sle-audit
```

このbundleには仕様、章契約、検証結果、source hash、生成図版hash、公開経路の確認結果を含める。Gate 7の判定者は本文執筆者と分ける。

## 図版とsimulation

図版は `production.json` のregistryを正本とし、生成可能な資材は `scripts/generate_sle_figures.py` で再生成する。乱数を使う場合はseed、格子幅、刻み、algorithm、検証法を必須とする。simulationは予想形成と式の検算にのみ使い、定理の証明として扱わない。

## Web / PDF

WebとPDFは同じQMDを正本とする。アニメーションには印刷用の静止fallbackを登録する。PDFは `python scripts/build_sle_pdf.py` で生成し、`--check` では入力、Quarto、出力経路だけを検査する。
