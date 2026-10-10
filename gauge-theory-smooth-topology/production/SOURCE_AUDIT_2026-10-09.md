# Source Audit - 2026-10-09

## 判定

FAIL。公開可能な完成教材ではない。

ただし、古い独立監査時点の29ページ版とは状態が変わっている。全18章は一通り存在し、Chapter 1--12、15--18、Appendix Aは増補済みである。今回の監査はPDFを再生成せず、現在の`.qmd`ソースを対象にした。

## 監査範囲

- `gauge-theory-smooth-topology/chapters/*.qmd`
- `gauge-theory-smooth-topology/production/NEXT_STEPS.md`
- 既存の独立監査レポート
- authoring validator / site validator の対象ファイル

今回はユーザー方針により、単位作業ごとのPDF生成は行わない。統合PDFは、ソースが一通り揃った最終段階でまとめて生成・QAする。

## 前回監査から改善された点

- Chapter 1--6に、smooth構造比較、intersection formの具体計算、$E_8$ の偶奇、gauge変換則、Chern--Weil導出、Hodge分解、ASD energy identityの説明が追加された。
- Chapter 7--12に、Sobolev設定、slice、ASD変形複体、Fredholm index、Kuranishi模型、transversality、bubbling、Uhlenbeck compactification、Donaldson不変量への橋渡しが追加された。
- Chapter 15--18に、Spin-c構造、Seiberg--Witten方程式、Weitzenböck評価、reducible回避、Donaldson/SW比較、Kähler還元、Taubesの証明アーキテクチャ、adjunction inequalityの読み方が追加された。
- Appendix Aは、Sobolev埋め込み、乗法評価、Coulomb gaugeの楕円評価、Fredholm判定、implicit function theorem、Sard--Smaleの役割まで拡張された。
- `references.bib` と manifest に Atiyah--Singer index theorem、Sard--Smale regular value theorem のsource coverageが追加された。

## 残る重大問題

### P0-1: 全体の厚みがまだ完成教材に達していない

現在の本文は、章構成としては揃っているが、完成教科書というより、詳細アウトラインを増補した段階に近い。読者が自力で再構成できる計算・例・反例・演習がまだ不足している。

特に、後半で「定義・結果・説明」の密度が上がる一方、読者が手を動かして確認する区間が少ない。

### P0-2: Chapter 13--14 が現在の最弱リンクである

Chapter 13「Donaldson理論の出力」とChapter 14「位相同相だが微分同相でない」は、全体の知的到達点に直結するにもかかわらず、他章より短く、橋渡しが不足している。

不足している説明:

- Donaldson diagonalization theoremで、なぜmoduli spaceの境界・compactificationがintersection formの制約に変わるのか。
- Donaldson polynomial invariantで、$\mu$-map、orientation、dimension matchingがどのように数え上げに入るのか。
- 「homeomorphicだがdiffeomorphicでない」候補を、Freedman側とDonaldson側の不一致としてどう作るのか。
- 具体的なintersection formを使った判別例。

### P0-3: 演習・解答がまだ薄い

Appendix Bは12問まで増えたが、18章構成に対して不足している。章ごとのReader Stop-Pointを実際に検査するには、各章に最低限の確認問題、計算問題、概念比較問題が必要である。

不足している種類:

- intersection formの計算
- Hodge starの符号確認
- ASD energy identityの導出
- deformation complexのcohomology解釈
- index公式の代入計算
- Kuranishi模型の有限次元例
- bubblingのscale計算
- Spin-c構造と$c_1$の具体例
- Seiberg--Witten expected dimension

## P1問題

### P1-1: source coverageがまだ不足している

次の主張は、本文中で扱う前にsource registry / bibliographyへ明示的に補強する必要がある。

- Donaldson diagonalization theorem
- Donaldson polynomial invariant
- Freedman classification の使用範囲
- Uhlenbeck compactification の詳細
- Seiberg--Witten invariantの構成
- adjunction inequality
- Kähler surface上のSW方程式の還元
- Taubes SW=Gr theorem

### P1-2: Visual assetsがDonaldson側に偏っている

現在の可視化は、bundle / connection / ASD / bubbling / moduli / wall-crossing まではある。一方で、Spin-c、Seiberg--Witten、Kähler還元、Taubes、adjunction inequalityを支える図が不足している。

追加候補:

- Spin-c構造を $H^2(X;\mathbb Z)$ torsor として見る図
- SW方程式の二つの式が spinor と curvature を結ぶ構造図
- reducible / irreducible の比較図
- Kähler還元で方程式が複素幾何のデータへ分解される図
- adjunction inequalityで曲面のgenus・self-intersection・basic classを比較する図

### P1-3: Appendixの独立参照性が不足している

Appendix Aは解析寄りに改善されたが、次の付録がまだ独立していない。

- 格子とintersection form
- characteristic classes
- Spin-c構造
- determinant line / orientation
- gluingの概念図と解析的入力
- Donaldson / SW invariantの定義に必要な代数位相

## Reader Stop-Point監査

現時点で重大な未解消疑問:

1. なぜDonaldsonのmoduli空間の端が、intersection formの対角化制約を生むのか。
2. Donaldson polynomialの$\mu$-mapは、何を幾何的に測っているのか。
3. Freedmanで同相を作り、Donaldsonで微分同相を否定する流れを、具体例でどう確認するのか。
4. Spin-c構造はなぜSW理論の自然な入力なのか。
5. SW方程式の二次写像$q(\Phi)$は、どの意味で曲率の自己双対成分と同じ型を持つのか。
6. Kähler曲面でSW方程式がなぜ複素幾何の方程式へ分解されるのか。
7. TaubesのSW=Grを、どこまでBlack Boxとして使い、どこまで証明アーキテクチャを説明するのか。

## 今回の即時修正

- 数式レンダリング互換性のため、本文中に裸の`qquad`として残っていた箇所を`\quad`へ修正した。
- Chapter 13に、Donaldson対角化定理の証明アーキテクチャ、低次元moduliの端が格子制約へ戻る論理、$\mu$-classとdimension matchingの説明を追加した。
- Chapter 14に、非平滑化可能性とexotic pairの証明形式の違い、照合表、$E_8$ 型例とexotic pairの読み分けを追加した。
- Appendix Bを12問から40問へ拡張し、章別の確認問題・計算問題・概念比較問題と略解を追加した。
- Donaldson polynomial、Kirby calculus、Seiberg--Witten標準文献、adjunction inequalityのsource coverageを追加し、chapter contractsとmanifestへ反映した。
- SW方程式とadjunction inequalityのSVG図を追加し、Chapter 16・18へ配置した。
- Chapter 15--16に、$\mathbb{CP}^2$ 上のSpin-c特性類とSW expected dimensionの代入例を追加した。
- Chapter 1--6に、exotic証明の比較順序、自己交点のnormal bundle解釈、整数格子と実形式の違い、$E_8$ 推論、接続の必要性、Hodge符号、ASD最小化、BPST scaleの危険性を追加した。
- Chapter 17に、Donaldson/SW理論を「難易度」ではなく「失敗の形」で比較する表、connected sum消滅の読み方、basic class配置の比較方法を追加した。
- Appendix Aにdeterminant line / orientation、gluing、characteristic classes、Spin-c構造の実用チェックを追加した。
- Chapter 9・10・12に、determinant line、orientation、compactificationとgluingの関係を本文側の橋として追加した。
- これはソース修正のみであり、今回PDFは再生成していない。

## 次の修正順序

1. Kähler還元・Taubes・gluing・orientationの図または付録説明をさらに追加する。
2. Chapter 7--12を再監査し、解析partの証明密度とReader Stop-Pointをさらに増やす。
3. Chapter 18を再増補し、Kähler還元・Taubes・adjunctionの具体例を増やす。
4. 全体を再監査し、残るReader Stop-Pointを新しい監査レポートとして整理する。
5. ソースが安定してから、Web render、mobile/dark spot check、統合PDF生成、PDF QAをまとめて実施する。
