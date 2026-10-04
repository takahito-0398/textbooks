# AI教科書ポータル Mobile-First External UX Audit

## Executive Summary

Productionを390px幅で、ポータル、教材トップ、文章・数式・表・コードを含む章、長文の中間章、最終章まで操作した。Reader UIの方向性は妥当であり、本文、数式、表、コードをページ全体の横スクロールから守る実装も機能していた。一方、読書以外のページにもReader UIが出ること、初期表示の固定領域が大きいこと、下部ナビゲーションが読書中に縮小・再展開すること、1280–1440pxでNavbarが折り返すことが、教材への集中を妨げていた。

改修ではUIを追加せず、適用範囲の限定、固定領域の縮小、Navbar情報の集約、下部ナビゲーションの状態一本化を行った。390×844の教材ページでは、初期上部領域を約157pxから98pxへ縮小した。下部ナビゲーションは約60pxで固定し、スクロール、目次開閉、ページ末尾で形状やラベルを変えない。

## Audit Method

- Production: `https://takahito-0398.github.io/textbooks/`
- 主対象: 390×844、補助対象: 360 / 375 / 412 / 430 / 768 / 1280 / 1440px
- Journey: ポータル → 教材トップ → 最初の章 → 長文・数式・表・コード → 目次 → 前後移動 → 最終章
- 実測対象: 固定UIの矩形、ページ横幅、要素内overflow、前後リンク、目次のfocus、スクロール前後の状態
- Source: Quarto設定、共通CSS/JavaScript、教材Sidebar、GitHub Actions、validation script

## Critical

該当なし。Productionで本文消失、ページ全体の横スクロール、リンク全面不通など、読書を継続できない問題は確認しなかった。

## High

### 下部ナビゲーションが読書中に変形する

- 現象: 390pxで通常約349px幅のナビゲーションが、スクロール後に約249px幅へ縮小し、章名が消えて矢印だけになる。ページ末尾や目次表示時には再展開する。
- 発生場所: 全教材ページのMobile Reader UI。
- 再現Viewport: 360–991px。390×844で実測。
- 問題: スクロール方向・位置で操作対象の形と情報量が変わり、本文以外へ注意を向けさせる。
- Mobile影響: 高。長時間読書中に繰り返し視覚ノイズになる。
- 改善: 状態依存の幅・grid・padding・ラベル表示規則を削除し、常に同じ形状と高さへ固定した。

### 初期表示の固定領域が本文を圧迫する

- 現象: 390×844でNavbar約85px、現在地バー約72px、下部ナビ約65px。上下一体で約222px、Viewport高の約26%を占める。長い章名では現在地バーが約94pxまで増える。
- 発生場所: 教材トップ・本文ページ。改修前はポータルにも発生。
- 再現Viewport: 360–430px。
- 問題: 本文を読む前から章タイトルが複製され、可変高の固定情報が読書面積を奪う。
- Mobile影響: 高。
- 改善: Navbarを56px、現在小章と進捗だけの単一行を42pxに固定。章名は本文H1に残し、読書中はNavbarを退避する。

### Desktop Navbarが折り返し、約120pxになる

- 現象: 全教材へのNavbarリンクが横一列に収まらず、1280pxと1440pxでNavbarが約120px高になる。
- 発生場所: 全ページ。
- 再現Viewport: 1280 / 1440px。
- 問題: 教材一覧はポータルにあり、教材内にはSidebarもあるため、重複ナビゲーションが本文を押し下げている。
- Mobile影響: Mobileでは折り畳まれるが、グローバルナビ構造が冗長。
- 改善: Navbarの教材リンク群を削除し、サイト名、検索、GitHubに限定。教材選択はポータル、章選択はSidebarへ集約した。

## Medium

### ポータルにもReader UIが表示される

- 現象: Homeに「現在地」「前の章」「次の章」「目次」が表示され、前後リンクは`#`を指す。
- 発生場所: Portal Home。
- 再現Viewport: 991px以下。
- 問題: カタログ画面を読書画面として扱い、意味のない操作を提示する。
- 改善: 有効なSidebar current itemがある教材ページだけでReader UIを生成する。

### 教材トップと最終章の境界リンクが無効な`#`になる

- 現象: 教材トップの前リンク、最終章の次リンクが`href="#"`になる。
- 問題: 位置が先頭へ飛ぶだけで、前後関係を誤認させる。
- 改善: 教材トップの前リンクは「教材一覧」へ接続。最終章の次操作はリンクでないdisabled表示にする。

### 目次Dialogのモーダル挙動が不完全

- 現象: Closeへfocusは移るが、背景スクロールを抑止せず、Tab focusがDialog外へ出られる。
- 発生場所: Mobile目次。
- 改善: 開いている間の背景スクロール抑止、Tab循環、Escape、focus復帰、anchor移動後の見出しfocusを実装した。

### 進捗がページ外周を含む

- 現象: 改修前はDocument全体のscroll量で算出し、Reader本文外のpaddingやchromeも分母へ含む。
- 問題: 特に短いページで「読み終えた」感覚と100%がずれやすい。
- 改善: `main.content`の開始位置と読書可能距離を基準に計算する。

## Low

### Motion preferenceへの配慮が不足

- 現象: Header退避とsmooth scrollが常に動作する。
- 改善: `prefers-reduced-motion`でtransitionとsmooth scrollを無効化した。

### Tabletの下部ナビゲーションが広すぎる

- 現象: 768pxでほぼ全幅になる。
- 改善: 下部ナビを最大560pxで中央配置し、片手・両手のいずれでも操作距離が過大にならないようにした。

## Reader Journey Audit

UIへ意識を奪われた主な瞬間は、Homeで読書ナビが出た時、スクロール直後にHeaderと下部ナビが同時に形を変えた時、ページ末尾で下部ナビが再展開した時、1280pxでNavbarが2段になった時だった。数式・表・コードを読む場面では、横に長い要素が独立スクロールへ収まり、ページ全体の横位置は維持された。

改修後は、読書開始時の上部情報を小章名と進捗へ限定し、スクロール中に変化するのはNavbarの一度の退避と進捗値だけになった。章移動の操作形状は一定である。

## Mobile UX

- 360–430pxでページ全体の`scrollWidth`はViewport幅以内。
- 本文左右paddingは360pxで14px、375px以上で16px。
- 本文は17px（360px未満）または17.5px、line-height 1.82。
- 初期上部は56px + 42px。読書中は42px。
- 下部ナビは約60px、Safe Areaを`env(safe-area-inset-bottom)`で考慮。
- Tap targetは主要操作で46px以上。

## Desktop UX

- Navbarは58pxへ安定し、1280 / 1440pxで折り返さない。
- 左Sidebarは章間移動を維持する。
- 1440pxでは本文860px、Reader railは本文と重ならない。1280pxではrailを隠し、本文幅を優先する。
- Mobile変更によるDesktopのbottom navigation表示はない。

## Navigation

- Portal → 教材: Portal cardを維持。
- 教材 → 章: Sidebarと教材トップのリンクを維持。
- 章 → 前後章: Mobile固定ナビ、Desktop Sidebar / reader railを維持。
- 教材一覧へ戻る: 教材トップの前操作をPortalへ接続。
- 章内目次: Mobile bottom sheetを維持し、現在項目へ`aria-current="location"`を付与。

## Typography

現在の日本語本文向けfont stackと暗色配色は維持した。Mobileでは18pxから17.5pxへわずかに縮小し、360pxでは17pxとした。左右余白を増やさず、数式と日本語本文の1行幅を確保した。見出しはH1/H2/H3の差、H2の罫線とaccentを維持し、1画面を見出しだけで消費しない寸法とした。

## Math / Table / Code / Figure

- Math: display mathは要素内横スクロール。長い数式があるページでページ全体の横スクロールなし。
- Table: `display:block; overflow-x:auto`を維持。390pxで幅438–502pxの表を表内に収容。
- Code: `pre`内横スクロールとQuarto copy UIを維持。コードページでページ全体のoverflowなし。
- Figure: `max-width:100%; height:auto`とcaption stylingを維持。

## Dark Mode

既存サイトはDarklyと共通CSSによる暗色固定テーマであり、背景`#0b1118`、本文`#e7edf4`、accent blue/greenの方向性は長時間読書に妥当と判断して維持した。純黒・純白の組合せにはしていない。Code、Table、Blockquote、Math、Navigationも同じtokenを使用する。今回、Light/Dark切替UIは追加していない。

## Accessibility

- 基本文字`#e7edf4`、muted文字`#9daabc`、link accent`#4da3ff`は背景`#0b1118`に対し、それぞれ16.09:1、8.04:1、7.22:1。
- Focus ring、semantic heading、Quartoのlandmarkを維持。
- 前後リンクに内容を含む`aria-label`を付与。
- 存在しない遷移は偽リンクにせず、`aria-disabled`の非link要素にした。
- 目次Dialogにfocus循環、Escape、focus復帰、現在位置の`aria-current`を追加。
- Reduced motionを尊重。

## Performance

新しいframework、UI library、font、animation libraryは追加していない。Reader UIは既存の小さなvanilla JavaScriptを整理し、scroll処理は`requestAnimationFrame`で1 frameに集約する。状態変更用のIntersectionObserverを削除し、scroll経路を一本化した。固定UIの高さを固定して、章名の折返しによる初期layout差を除去した。

## 採用した改善

- Reader UIを教材ページだけへ限定
- Mobile statusを現在小章 + 進捗の42pxへ統合
- 下部ナビの縮小・再展開・ラベル非表示を廃止
- 無効`#`リンクを廃止
- 教材トップからPortalへ戻る導線を追加
- Navbarの重複教材リンクを削除
- 目次Dialogのkeyboard / focus / background scrollを改善
- Quartoの`section[id]` anchorにも固定バー分の`scroll-margin-top`を適用
- 本文基準の進捗計算
- Reduced motionと安定したscrollbar領域を追加

## 採用しなかった改善と理由

- 新しい読書履歴の永続化: 保存仕様とprivacy判断が必要で、今回の外側UI改善を超える。
- 固定UIの完全撤去: 長文で現在小章と章移動を失うため不採用。
- Headerをスクロール方向で再表示: 視覚変化を増やすため不採用。
- 数式の自動縮小: 可読性を損なうため、要素内横スクロールを維持。
- Light/Dark切替追加: 現行が暗色専用として一貫しており、新しい状態と検証範囲を増やすため不採用。
- Frontend framework導入: 性能・保守コストに見合わない。

## Residual Risks

- 実機のiOS Safari / Android Chromeにおけるbrowser chromeとSafe Areaは、Desktop ChromeのViewport emulationでは完全には再現できない。
- Core Web Vitalsのfield dataは今回取得していない。変更はCLSを減らす方向だが、Production反映後の実測監視が望ましい。
