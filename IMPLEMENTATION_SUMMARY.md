# Implementation Summary

## Before / Problem / After / Rationale

| Before | Problem | After | Rationale |
|---|---|---|---|
| Homeを含む全ページにReader UI | カタログに無効な前後・目次操作が出る | Active sidebar itemのある教材ページだけ生成 | Reader UIの責務を読書画面へ限定 |
| Mobile上部が章名・小章名・進捗の可変高 | 390pxで72–94px、章名を本文H1と重複表示 | 小章名・進捗の42px固定 | 現在地を残しつつ本文面積を増やす |
| 下部ナビが読書中に縮小し、文字を消す | 操作対象がスクロールで変形する | 約60pxの同一形状を常時表示 | 視界と操作の一貫性を優先 |
| 境界ページは`href="#"` | 無効操作が先頭へ飛ぶ | 教材トップはPortalへ接続、最終章は非link disabled | 遷移contractを明確化 |
| Navbarに全教材リンク | 1280/1440pxで約120pxへ折返す | 教材リンクをPortal/Sidebarへ集約、Navbarは58px | 重複情報を削減 |
| 目次はClose focusのみ | 背景scroll・focus流出が可能 | 背景scroll抑止、Tab循環、Escape、focus復帰 | Dialogとしてのkeyboard contractを満たす |
| 下部の目次はページ内見出しのみ | 別章へ移動したい読者にとって、教材全体の位置関係が見えない | 現在の教材Sidebarから章一覧を生成し、現在ページを強調 | Mobileでも他章へ直接移動できるReader navigationにする |
| Anchor offsetは見出し要素のみ | Quartoの`section[id]`へ跳ぶと固定バーに隠れる | Section anchorにもscroll marginを適用 | 直接リンクと目次リンクの着地点を揃える |
| Document全体で進捗計算 | UI paddingを読書進捗に含む | `main.content`基準 | 読了感覚と表示を合わせる |

## 変更ファイル

- `_quarto.yml`: Navbarから重複する教材リンク群を削除。
- `shared/styles/custom.css`: 固定UI寸法、Mobile typography、安定したbottom navigation、Dialog、reduced motionを整理。
- `shared/scripts/reader-ui.html`: 適用範囲、前後navigation contract、進捗、教材全体の目次、focus管理を整理。
- `AUDIT_REPORT.md`: Production監査、Severity、採否、残存リスク。
- `IMPLEMENTATION_SUMMARY.md`: 実装のBefore / Problem / After / Rationale。

## Verification

- `python scripts/validate_site.py`
- Quarto 1.10.18 portableによる全133ページの`quarto render`
- 360 / 375 / 390 / 412 / 430 / 768 / 1280 / 1440pxでlocal renderを実測
- Portal、教材トップ、最初・中間・最終章、数式、表、コード、目次、前後navigationを確認
- 390pxでscroll前後のbottom navigation寸法が同一であることを確認
- 1280 / 1440pxでNavbarが58pxかつ本文・Sidebar・railが重ならないことを確認

Production検証結果とGitHub Actions runは、main反映後に確認して最終報告へ記載する。
