# UI Rework Plan

## 現状UI

- Quarto website標準のnavbar、左sidebar、右TOC、page navigationを使用している。
- 教材は章単位ページで、節は章内に連続して配置されている。
- Light/Dark切替はあるが、初期印象はBootstrap寄りで明るく、長時間読書向けの暗色設計ではない。

## 現状スマホUI

- Quarto標準の折り畳みsidebarはあるが、現在章・現在節・進捗が読みながら分かりにくい。
- 下部の前後移動がなく、章移動の操作が読書の流れから離れる。
- 本文幅、見出し、画像、長い数式の扱いは最低限で、学術書的な読書体験には弱い。

## 問題

- 現在位置の常時把握が弱い。
- スマホで目次を開く導線がQuarto標準UIに依存している。
- Dark academic readerとしての統一感が不足している。
- 前後の章へ1アクションで移動しにくい。

## 改修方針

- Mobile firstで、本文幅・文字サイズ・行間を読書優先にする。
- サイト全体をDark theme基調へ変更し、明るいBootstrap初期印象を消す。
- 各章内の見出しをIntersectionObserverで追跡し、現在章・現在節・進捗を表示する。
- スマホではsticky current barとbottom navigationを追加する。
- 目次はボタンからbottom sheetで開き、同一ページ内見出しへsmooth scrollする。
- Desktopでは左sidebarを残し、右側に現在位置・進捗・前後移動のreader railを追加する。

## 変更ファイル

- `_quarto.yml`
- `shared/styles/theme.scss`
- `shared/styles/custom.css`
- `shared/scripts/reader-ui.html`

## Quarto標準で使う部分

- website sidebar
- page navigation
- search
- MathJax
- generated heading anchors
- generated page prev/next links

## Custom CSS / JSが必要な部分

- Dark academic typography
- mobile sticky current section UI
- bottom navigation
- TOC bottom sheet
- desktop current-position rail
- scroll progress and active heading synchronization
