# Independent Final Acceptance Audit / Adversarial Quality Review

対象教材: 『4次元ゲージ理論と滑らかな位相』  
監査日: 2026-10-10  
監査対象: `chapters/*.qmd`、`contracts/*.json`、`production/manifest.json`、`references.bib`、SVG 図版、既存の統合 PDF、Bootstrap の完成条件・執筆規約・構成監査。  
監査方法: 執筆者の自己監査を根拠にせず、本文、章契約、定理・Black Box 登録、PDF 実描画を直接照合した。本文は更新中の作業ツリーを対象とし、PDF は作成日時 2026-10-09 21:05:31 +09:00 の既存成果物を対象とした。

## 1. Executive Verdict

**REJECT（正式公開不可）**

最大の理由は、公開対象の統合 PDF が最新の本文・図・引用を反映しておらず、しかも完成基準が要求する説明密度と証明深度を、特に Donaldson の核心橋と Seiberg--Witten 側の主要 Black Box で満たしていないためである。

最も優れている点は、`Freedman による位相的存在`、`Donaldson による滑らかな制約`、`exotic pair の非微分同相性`を混同しない主線である。第1、3、13、14章は、この区別を繰り返し明示している。

最大の弱点は、中心問題である「PDE の解空間の端・交点数が、なぜ滑らかな位相不変量になるか」を支える厳密な仮定・構成・具体例が、見取り図の列挙に留まることである。加えて、最終 PDF は現本文と一致しない。

## 2. Completion Criteria Compliance

Bootstrap で固定された quality gate と完成条件を逐条照合した。`PASS` は正式公開の可否ではなく、当該項目だけの判定である。

| 完成条件 | 判定 | 根拠と不足 | 必要な修正 |
|---|---|---|---|
| 18章・付録・依存順序が存在する | PASS | manifest と章契約は前方依存・循環なしで揃う | 維持する |
| 中心問題が一貫する | PASS | 第1章の問いから第18章の総括まで主線は保たれる | 最終改稿後も同じ問いを維持する |
| Reader Stop-Point を解消する | PARTIAL | 契約上の未解消項目は0件だが、Ch.13、16、18に実質的未解決点が残る | 下記 M-1〜M-5 を本文で解消する |
| A〜D の証明深度を守る | FAIL | C指定の Donaldson 対角化・不変量構成が入力と出力の一般論に留まる。D指定の adjunction inequality も正確な仮定を欠く | 定理ごとの statement、仮定、難所、下流用途を改稿する |
| Black Box が契約を持つ | PARTIAL | Freedman、Uhlenbeck、Taubes は概ね役割を示すが、adjunction と connected-sum 消滅の適用条件が曖昧 | 各 Black Box の適用範囲を本文と registry に固定する |
| 数学的記法・型が整合する | FAIL | Ch.15 の `q(Φ)=(Φ⊗Φ*)_0` は Hermitian endomorphismであり、本文が同一視する skew-Hermitian / `iΛ^2_+` とは因子と同一視の指定なしには型が合わない | 係数・`i`・Clifford 同一視を一つの規約として固定する |
| PDEから smooth invariant への橋が再構成可能 | PARTIAL | Ch.7--12 の順序はよいが、実際の 1-parameter cut-down moduli を最後まで追う例がない | 1本の最小例を、次元・向き・境界・wall/bubbling除外まで通す |
| Freedman と Donaldson の役割を分離する | PASS | Ch.3、14で非平滑化可能性と exotic pair を明確に分ける | 実例へ接続する際も同じ区別を維持する |
| Donaldson から SW への必然性 | PARTIAL | 非可換 bubbling と SW の評価を比較できているが、Donaldson 不変量の具体的計算の重さと SW の具体的な利点を同一例で示さない | 一つの例または比較表を「定義・計算・出力」まで具体化する |
| 定理・出典の追跡可能性 | PARTIAL | ソースには標準文献・原論文を追加済み。ただし PDF は古い8件のみで、現ソースの引用と一致しない | 最終生成物で bibliography と引用を同期する |
| 図版が教育目的を満たす | PARTIAL | Hodge、slice、bubbling、比較、SW、Taubes の構造図はよい。束の局所自明化/parallel transport と、cut-down 交点数の可視化がない | 不足する二図を追加し、本文で参照する |
| 後半の説明密度を維持する | PARTIAL | Ch.15--18は単なる定理列挙ではないが、Kähler還元・adjunction・connected sum の仮定が圧縮されている | 後半にも前半と同じ仮定・例・反例密度を与える |
| 日本語として自然で一貫する | FAIL | 英語の専門語が日本語の文法内に過密に混在し、見出しにも残る | 用語方針を適用し、日本語の定着語を置換する |
| Web/PDFが同じ正本から生成される | FAIL | PDF は最新の QMD より約17時間以上古く、後から追加した図・文献・修正を含まない | 最新正本から PDF を再生成し、source hash を記録する |
| 数式・図・目次・文献の表示が正常 | FAIL | PDF p.36 に `qquad` が文字として残る。目次は Part/章階層を示さず、文献は旧版 | 再生成後に全ページの機械検査と代表頁の目視QAを行う |
| 独立監査を通過する | FAIL | 本レポートの判定が REJECT | BLOCKER と MAJOR を解消して再監査する |
| 完成量が設計の説明密度に見合う | FAIL | Bootstrap は Core 300--380頁、Appendix 100--150頁を自然な目安とした。現PDFは48頁で、主張の省略を吸収できていない | ページ数を機械目標にせず、必要な構成・例・証明アーキテクチャを追加した結果として到達させる |

## 3. Blocking Issues

### B-1: 統合PDFが現本文を反映していない

- **Location:** `assets/gauge-theory-smooth-topology.pdf`、全体
- **Problem:** PDF の更新時刻は 2026-10-09 21:05:31 +09:00。主要 QMD は 2026-10-10 13:43--13:51 に更新されている。PDF p.36 には `qquad` が本文文字として残り、p.48 の参考文献は8件で終了する。ソースに追加済みの図と引用を反映しない。
- **Why it matters:** 公開物が正本と異なり、数式レンダリングも壊れている。Web/PDF 同一正本という完成条件に直接反する。
- **Required change:** 全修正後に既存 builder でPDFを再生成し、生成時の source hash を audit bundle に保存する。
- **Acceptance condition:** PDF の更新時刻・章数・図数・文献キーが正本と一致し、`qquad` 等の生文字、欠落図、旧文献がない。

### B-2: 説明量と完成教材としての深さが設計目標に届かない

- **Location:** 全体、とくに Ch.7--13、15--18、付録A
- **Problem:** 48頁のPDFは、Bootstrap が「150頁圧縮でも不足」と判断した設計に対してなお短い。現本文は改善済みでも、契約が要求する C深度の主要結果、具体例、解析補講、実際の不変量構成を収容できていない。
- **Why it matters:** 短さの主要因は重複除去ではなく、仮定・証明アーキテクチャ・worked example の省略である。大学院レベル初学者が外部質問なしに主線を再構成できない。
- **Required change:** 頁数を埋めるのではなく、M-1〜M-5の必要内容、Donaldson/SW各1例、解析付録の利用箇所を追加する。
- **Acceptance condition:** 指定された proof-depth と Reader Stop-Point が本文だけで満たされ、独立監査で「詳細は文献へ」の連鎖が主要橋に残らない。

### B-3: SW方程式の二次写像の型と規約が不十分

- **Location:** Ch.15「曲率とspinorを同じ型で結ぶ」、Ch.16 冒頭
- **Problem:** `(Phi\otimes\Phi^*)_0` は自然には trace-free Hermitian endomorphismである。一方本文は自己双対2形式を trace-free skew-Hermitian endomorphism、曲率を `i\Lambda^2_+` と置く。`i` と規格化係数、および Clifford 同一視を明示しない等式は型が合わない。
- **Why it matters:** これはSW方程式の中心式であり、Weitzenböck公式の係数・符号・後続のコンパクト性議論に影響する。
- **Required change:** `q` を一つの規約で定義する。例えば「Clifford 作用による `i\Lambda^2_+\cong\mathfrak{su}(W^+)` の同一視の下、`q(\Phi)` は規格化済みの `i(\Phi\Phi^*)_0` に対応する」と書き、Ch.16 の係数・gauge作用と揃える。
- **Acceptance condition:** 各辺が同じ束の section であり、gauge不変性と Weitzenböck の四次項の符号が採用規約から追跡できる。

## 4. Mathematical Audit

| 箇所 | 判定 | 監査所見 |
|---|---|---|
| Ch.2--6: intersection form、Hodge分解、energy identity | PASS WITH MINOR | 和と差から ASD を導く説明、`ASD ⇒ YM` の導出、閉多様体の境界項は良い。規約も概ね一貫する。 |
| Ch.7: sliceとreducible | PARTIAL | 有限次元の `S^1` 模型は有効。ただし「irreducibleなら逆作用素」は中心/基点 gauge群の処理をさらに明示すべきである。 |
| Ch.8: ASD変形複体 | PARTIAL | symbol計算は適切。ただし Hodge型分解の `im d_A^*` は次数を明記すると不正確で、正しくは複体の随伴 `im d_A^{+,*}` を使う必要がある。 |
| Ch.9--10: Fredholm、index、横断性 | PARTIAL | index と actual dimension の区別は明確。一方、Sard--Smale を使う universal section の具体的 domain/codomain と、何を摂動するかの固定が不足する。 |
| Ch.11: Uhlenbeck compactness | PASS WITH MINOR | bubbling、energy量子化、ideal instanton、codimension 4 の因果はよく説明される。`\operatorname{Sym}^\ell X` が重複点で multiplicity を表すことを一文追加するとよい。 |
| Ch.12: 不変量構成 | MAJOR | 1-parameter moduli の一般図はあるが、Donaldson不変量の `w`、構造群、reducible回避、cut-down、compactified boundary を一つの定義として閉じない。universal bundle も full/based gauge quotient の選択と併記が必要である。 |
| Ch.13: Donaldson対角化・多項式 | MAJOR | 対角化定理のC深度に対して、選ぶ束、必要な低次元moduli、boundary/linkから characteristic vector/格子制約へ至る補題の役割が書かれていない。読者の最重要疑問を「端が格子に戻る」で止めている。 |
| Ch.14: Freedmanとの照合 | PASS WITH MINOR | 非平滑化可能性と exotic pair の論理分離は正確。実在の exotic pair を一例だけ最後まで扱わないため、照合手順が模型に留まる。 |
| Ch.15--16: Spin-c、SW | MAJOR | B-3の型問題に加え、`c_1` による Spin-c ラベルは2-torsionの注意がなく、gauge作用の符号規約も Ch.4 と表現規約の対応を説明しない。 |
| Ch.17: 比較・connected sum | MAJOR | `多くの標準状況` は定理の仮定にならない。closed/oriented、各因子の `b_2^+>0`、不変量の版・chamber等を明示する。 |
| Ch.18: Taubes・adjunction | MAJOR | adjunction inequality は `b_2^+>1`、`[\Sigma]` 非torsion、通常は genus 条件など、用いる定理版の仮定を「適切な仮定」で隠している。D深度の正確な statement に達しない。 |

## 5. Explanation Audit

### 機能している説明

- Ch.4 は普通の微分が局所フレーム変更と両立しないことから接続を導く。
- Ch.5--6 は4次元性、Hodge分解、Chern--Weil、energy最小化を因果で接続する。
- Ch.7--12 は gauge重複、線形化、Fredholm、orientation、compactificationを別問題として分離する。
- Ch.14 は「同相」と「非微分同相」を二本の証明に分ける。

### 未解消または不十分な Reader Stop-Point

| Location | 読者の問い | 欠落 | 必要な本文追加 |
|---|---|---|---|
| Ch.12 | 何を数えれば本当にDonaldson不変量なのか | general principleから具体的定義への橋 | bundle型、次元、`\mu`挿入、generic representative、boundary回避、cobordismを一例で通す |
| Ch.13 | moduliの端がなぜ対角化を強制するのか | bundle選択と格子論への翻訳 | 低次元moduliの選択、reducible link、格子の characteristic vector へ至る主要補題を役割付きで示す |
| Ch.15 | なぜ spinor二次式が曲率と同じ型か | 同一視と係数 | B-3の規約表と短い局所行列計算 |
| Ch.16 | なぜSWでは接続全体も制御できるのか | spinor上界から接続のgauge-fixed boundへの橋 | Hodge分解、固定されたde Rham class、Coulomb gauge、楕円評価の順で説明 |
| Ch.18 | adjunction inequalityをいつ使えるのか | theorem hypotheses | 定理の正確な版と、適用できないsphere/torsion等の注意 |

## 6. Narrative / Curriculum Audit

**PARTIAL。** 前半から Donaldson への導線は自然で、SWを「有名だから追加する」構成にはなっていない。一方、Ch.13の証明アーキテクチャが抽象度を上げたまま終わるため、最重要の「PDEからsmooth topologyへ」の橋で読者が足場を失う。

また、Ch.18は Kähler 還元、Taubes、adjunction を一章へ集める。到達点としては正しいが、Kählerの場合と symplecticの場合、公式と不等式、Black Boxと本文導出の境界を明示的に分けなければ、後半が概説調に見える。

## 7. Intuition Audit

**PARTIAL。** Hodge分解、gauge orbit、bubbling、理論比較、Taubes極限の図は、文章より構造理解を速めている。特に bubble の「scaleは失われ、位置とchargeだけが残る」という説明は適切である。

ただし、次の二箇所は図または有限次元図解が必要である。

1. Ch.4: 局所自明化を変えたときに `ds` の余分な項を接続が打ち消す図。現状は式だけなので、connectionを初めて学ぶ読者には急である。
2. Ch.12--13: cut-down moduli と oriented boundary count の図。これは「交点数が不変量になる」主張の中心であり、図の費用対効果が高い。

## 8. Japanese / Language Audit

### 判定表

| 項目 | 判定 | 主な問題 |
|---|---|---|
| 自然な日本語 | PARTIAL | 論理自体は読みやすいが、英語名詞の挿入が文の流れを切る |
| 平易さ | PARTIAL | 前半は良い。後半は仮定を省いた抽象名詞列が増える |
| 英単語過多 | FAIL | `smooth`, `moduli space`, `compactness`, `expected dimension`, `regularity` 等が見出しと本文に反復する |
| カタカナ語過多 | PARTIAL | gauge、spinor、instantons 等には分野慣行があるが、英語のまま残す語が多い |
| 直訳調 | PARTIAL | `Proof Architecture`、`Black Box`、`small-energy threshold` などが日本語の文章へ未消化で入る |
| 独自造語 | PASS | 明白な造語は検出しない |
| 一文の長さ | PARTIAL | 主要文は短いが、後半の「仮定のもと」「概略的には」が情報不足を覆う |
| 箇条書き依存 | PARTIAL | チェックリストとして有効な箇所と、証明骨格を箇条書きで済ませる箇所が混在する |
| 見出し過多 | FAIL | PDF目次では節が連番で平板化し、Part/章の論理階層が読めない |
| 用語統一 | FAIL | 登録済みの日本語訳がある語まで英語表記が優勢である |

### 英語表記の分類

- **A: 英語のままが自然** — gauge、instanton、spin^c、Seiberg--Witten、Donaldson、Taubes、moduli（ただし初出は「モジュライ空間（moduli space）」が望ましい）。
- **B: 初出のみ併記し、以降は日本語が自然** — smooth structure（滑らかな構造/微分構造）、connection（接続）、curvature（曲率）、bundle（束）、orientation（向き）、compactness（コンパクト性）、regularity（正則性）、transversality（横断性）。
- **C: 原則日本語に直すべき** — expected dimension（期待次元）、actual dimension（実際の次元）、worked example（計算例）、proof architecture（証明の骨格）、black box（引用定理/ブラックボックス定理。初出のみ併記）、source（出典）、input/output（仮定・結論）。

### 代表的な修正方針

- Ch.16 見出し `Weitzenböck formulaがcompactnessを作る` は「Weitzenböck公式からコンパクト性評価を得る」にする。公式が単独でコンパクト性を“作る”のではなく、評価、gauge固定、楕円正則性を組み合わせるためである。
- Ch.15 の `rank 2の複素vector bundle` は「階数2の複素ベクトル束」とする。
- Ch.17 の `connected sumとbasic class` は「連結和と基本類」とし、初出に英語を併記する。
- PDF目次の `worked example`、`unimodular`、`even/odd` 等は日本語見出しへ統一する。

## 9. Visual / Rendering Audit

### Source figures

SVGは再生成可能で、目的・alt text・dark mode/mobile登録もある。構造図としては有効である。ただしB-1により、最終PDFで全図を確認できない。

### PDF実査

既存 PDF（48頁）を p.1、12、24、36、48 でPNG化して確認した。

- p.12、p.24、p.48: 日本語、表示数式、callout、参考文献に明らかな切れや重なりはない。
- p.1: 目次の節階層が平坦で、Part・章の構造が読めない。完成教材のナビゲーションとして不十分である。
- p.36: 数式内に `qquad` がそのまま印字される。数式レンダリングFAIL。
- p.48: 文献は8件のみで終了し、現ソースに登録された後続資料を反映しない。

Webの現行HTMLを、独立した実ブラウザで desktop/mobile/dark mode 再検証してはいない。以前の作者側検証を、本監査の視覚的PASS根拠には採用しない。最終PDF再生成後に、Webも同じコミット/正本から再検証する必要がある。

## 10. Back-Half Quality Audit

**PARTIAL。** Ch.15--17 はDonaldson側と同じ moduli lifecycle を再利用し、単なる用語紹介にはなっていない。この点は合格水準である。

しかし、Ch.18のKähler還元、Taubes、adjunctionは一章に圧縮され、定理の正確な適用範囲を読者が復元できない。後半で用いる `適切な仮定のもと`、`多くの標準状況` は、前半で避けていた説明省略が再出現した箇所である。後半品質は前半と同等とは判定できない。

## 11. Reader Simulation

| 読者 | 停止地点 | 予想される質問 | 判定 |
|---|---|---|---|
| A: 微分幾何・特性類既習、gauge初学 | Ch.7--8 | `irreducible` と中心の除去後に、なぜsliceが一意なのか。`d_A^{+,*}` はどこから来るのか | MODERATE |
| A | Ch.12--13 | 実際のDonaldson不変量を一度も組み立てずに、なぜ格子制約まで言えるのか | MAJOR |
| B: PDE既習、4次元位相初学 | Ch.3、14 | Freedman分類で何を追加確認すれば同相といえるのか。実在のexotic pairはどれか | MODERATE |
| B | Ch.11--12 | codimension 4 がなぜ cobordism の余分な端を除くのか。cut-down 後にも同じか | MAJOR |
| C: Chern--Weil/Atiyah--Singer既習 | Ch.15--16 | 二次写像の型、規格化、Weitzenböck公式の係数は整合しているか | MAJOR |
| C | Ch.18 | adjunction inequality の厳密な仮定と Taubes 定理のどの版を使うか | MAJOR |

## 12. Findings Register

| ID | Severity | Location | Finding |
|---|---|---|---|
| B-1 | BLOCKER | PDF全体 | 最新ソースと不一致。p.36 に生文字 `qquad`、p.48 は旧参考文献。 |
| B-2 | BLOCKER | 全体 | 完成基準の説明密度に対して48頁は不足。主要橋の省略を伴う。 |
| B-3 | BLOCKER | Ch.15--16 | `q(\Phi)` の型・`i`・規格化が未固定。 |
| M-1 | MAJOR | Ch.12 | 実在するDonaldson不変量の定義/cobordismを一例として閉じない。 |
| M-2 | MAJOR | Ch.13 | 対角化定理のC深度の証明骨格が具体的束・link・格子補題を欠く。 |
| M-3 | MAJOR | Ch.17 | connected-sum消滅を曖昧な範囲で述べる。 |
| M-4 | MAJOR | Ch.18 | adjunction inequality の仮定が正確でない。 |
| M-5 | MAJOR | Ch.8 | Hodge型分解の随伴像の次数表記が不正確。 |
| M-6 | MAJOR | 全文/PDF | 英語優勢と平坦な見出し構造が日本語教材・読書導線を損なう。 |
| M-7 | MAJOR | PDF | Web/PDF同一正本、数式・目次・文献の完成条件に不合格。 |
| MD-1 | MODERATE | Ch.7 | irreducible、中心、based/full gauge group の関係を整理していない。 |
| MD-2 | MODERATE | Ch.12 | universal bundle と `\mu`-map の construction scope が曖昧。 |
| MD-3 | MODERATE | Ch.14 | exotic pair の実例が模型で終わる。 |
| MD-4 | MODERATE | Ch.18 | Kähler と symplectic の入力・出力の境界が圧縮される。 |
| MD-5 | MODERATE | Ch.4、12 | connection/parallel transport、cut-down count の高価値図がない。 |
| N-1 | MINOR | Ch.15 | Spin-c構造を `c_1(L)` でラベルする際の2-torsionへの注意がない。 |
| N-2 | MINOR | Ch.11 | `\operatorname{Sym}^\ell(X)` の重複点とmultiplicityの対応を補うとよい。 |

## 13. Required Revision Plan

1. **規約を先に修正する。** Ch.15--16 と notation registry に、Spin-c Dirac作用素、`q`、`F_A^+`、gauge action、Weitzenböck公式の一組の規約表を置く。B-3、M-5を修正し、関連する演習・図・本文を同期する。
2. **PDEから不変量への一本の完全な最小経路を追加する。** Ch.12に「固定した bundle と0次元 cut-down moduli」を選び、regularity、orientation、compactification、1-parameter cobordism、`b_2^+>1` の役割を順に示す。これは抽象表の追加ではなく、記号を最後まで追う例にする。
3. **Donaldson対角化の proof architecture をC深度まで上げる。** Ch.13に、選ぶSO(3)束、期待次元、reducible link、Uhlenbeck端、格子条件という主要補題を、各々の入力・出力・難所・依存関係付きで書く。完全証明にはしない。
4. **SW後半の定理statementを固定する。** Ch.17のconnected-sum消滅、Ch.18のTaubesとadjunctionについて、用いる版の仮定・結論・除外例・本書での用途をcalloutとして明記する。Kähler還元とsymplectic出力の間に短い橋を置く。
5. **日本語と見出しを全体改稿する。** 用語表をB/C分類に従って本文・図・PDF目次へ適用する。Part → Chapter → Section の階層をPDFとWebで明示する。
6. **図を二点追加する。** connectionの局所表示/parallel transport、cut-down/向き付きcobordismの図を再生成可能な正本として追加する。
7. **最終成果物を再生成してからQAする。** 最新ソースから一度だけ統合PDFを生成し、全ページの文字列検査、目次/文献/図数の照合、代表頁のdesktop/mobile/dark-mode確認を行う。作者側ではなく独立者が結果を確認する。

## 14. Final Acceptance Conditions

次のすべてを満たした場合にのみ **ACCEPT** を再判定できる。

1. B-1〜B-3 と M-1〜M-7 が修正され、各修正に対応する章契約・registry・演習が同期している。
2. Ch.12--13 の読み手が、具体的な cut-down moduli/cobordism と対角化定理の補題配置を本文だけから説明できる。
3. Ch.15--18 の式が型・係数・仮定まで一貫し、Black Boxの statement が「適切な仮定」で止まらない。
4. 日本語用語方針と見出し階層がWeb/PDFへ反映される。
5. 最新ソースと一致するPDFについて、数式、図、文献、目次、リンク、mobile、dark modeを再検証し、重大な描画不良がない。
6. 完成基準の各gateを、執筆者の自己判定ではなく独立監査で再度PASSと判定する。

この時点では、公開・publish・正式完成のいずれも承認しない。
