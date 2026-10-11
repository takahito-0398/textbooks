# Audit Ingestion and Production Decisions

## 入力と優先順位

制作要件の正本は、2026-10-08の `Pre-Production Curriculum Audit / Architecture Review` とする。Stage 2.5候補比較は題材選定と初期30頁案の背景として使い、両者が異なる場合は後発の監査版を優先した。したがって、150頁上限は採用せず、Core 300〜380頁、Appendix 100〜150頁を自然な目安とし、説明密度を落とす短縮はしない。

## 取り込んだ制作要件

| 監査項目 | 制作上の実装 |
|---|---|
| 中心問題 | `manifest.json` の `book.central_problem` に固定 |
| scope | 閉・連結・向き付きsmooth 4-manifold、Donaldson主線の単連結性、`b_2^+`条件をledger化 |
| curriculum | 6 Part・18章を順序付きgraphとして保持 |
| prerequisites | 章契約の `prerequisites` とconcept registryで追跡 |
| mathematical / pedagogical dependency | curriculum内で別edgeとして管理し、循環と未来参照をvalidatorで拒否 |
| proof depth | A〜Dをmanifestに定義し、定理と章契約へ割当 |
| black boxes | 必要性、入力、出力、難所、後続依存を必須化 |
| Missing Explanation | review順序の最初に置き、欠落分類をAuthoring Guideへ固定 |
| rigorous / heuristic | 章契約の `rigor_statuses` と本文calloutで区別 |
| Reader Stop-Point | question、resolution、locationを必須化し、`unresolved` をGate失敗にする |
| visual requirements | figure registryに目的、概念、方式、alt、mobile、dark mode、再生成、licenseを保持 |
| production requirements | Quarto既存構成、同一QMD正本、Typst PDF、GitHub Pages workflowを再利用 |
| Red Team | 曖昧語、placeholder、前方依存、未契約black box、未解消Stop-Pointを負例testで攻撃 |

## 監査から修正した点

- Stage 2.5の30頁案では `S^4` を初期のintersection form例に含めていたが、確定監査に従い、初期計算は `CP^2` と `S^2×S^2` を主とする。`S^4` は `H^2=0` でも非自明なbundle chargeとBPST instantonを持つ後半の反転へ保存する。
- Donaldson対角化定理とDonaldson多項式不変量は、同じ出力として統合しない。Chapter 13で二つの論理を比較し、依存定理を分離する。
- 「Freedmanが許しDonaldsonが禁じる」から直ちにexotic pairが得られるとは書かない。非平滑化可能性とhomeomorphic but nondiffeomorphic pairをChapter 14で別々に扱う。
- SW理論は「可換だから簡単」としない。非線形spinor連成、reducibles、orientation、wall crossingを残る課題として管理する。

## 既存環境との整合

既存リポジトリはQuarto websiteで、`_quarto.yml` が教材ごとのsidebarとrender対象を管理し、共通CSSが長い数式の横スクロール、狭幅レイアウト、dark modeを提供する。`reader-ui.html` が目次、進捗、前後移動をsidebarから組み立てる。GitHub Actionsはmain push時にvalidation、Quarto render、Pages artifact upload、deployを行い、`CNAME` により既存custom domainを維持する。

新教材はこの構造へ `gauge-theory-smooth-topology/` として追加し、新frameworkや本番依存を導入しない。標準ライブラリだけのvalidatorとfigure generatorを追加し、PDFは既存教材と同様にQuarto Typst経路を使う。

## まだ人間の判断を要する事項

- 数学的正しさ、説明の自然さ、引用statementの版と仮定は自動検査だけでは保証できない。
- mobileとdark modeはCSSとSVGの構造を検査できても、最終的な可読性はスクリーンショット監査が必要である。
- 章後半の品質低下はmetadata充足だけでは防げない。Part IV〜VIを独立Reader Advocateが読み、前半と同じrubricで採点する。
- 一次資料の内容確認とhistorical attributionは執筆章ごとに再確認する。

