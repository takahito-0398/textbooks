# Revision Change Log

作業日: 2026-10-13

対象: `gauge-theory-smooth-topology`

## 取り込み元

- `gauge_theory_104p_redesign_independent_reaudit_v2.md`
- `gauge_theory_104p_redesign_codex_revision_prompt_v2.md`
- `gauge_theory_104p_rereview_after_revision_2026-10-13.md`

## 変更一覧

| ID | 旧状態 | 今回の変更 | 対応ソース | 最終PDF確認 |
|---|---|---|---|---|
| GT-V10-01 | p.5/p.29の小見出しがページ末尾に孤立。p.84の随伴公式後に述語が次ページへ流れる | PDF用の弱い改ページを2箇所追加。随伴公式は「次が成り立つ」と前置して、式後に述語だけを置かない形へ変更 | `01-smooth-structures.qmd`, `06-yang-mills-asd.qmd`, `18-kahler-symplectic.qmd` | p.5/6, p.29/30, p.84/85 |
| GT-V10-02 | 引用定理の一部が赤い警告風の `important` 表示 | 引用定理系のcalloutを `note` に統一し、タイトルを `引用定理｜...` へ変更 | `02`, `03`, `07`, `11`, `14`, `18`章 | p.17など |
| GT-V10-03 | `μ-類` が一部残存 | `μ類` へ統一 | `appendix-notation-exercises.qmd` | p.102 |
| GT-V10-05 | 用語対照表の `expected dimension, virtual dimension` が窮屈 | `expected/virtual dimension` へ短縮 | `appendix-notation-exercises.qmd` | p.95 |
| 再レビュー微修正 | 序論の `self-dual / anti-self-dual` が英語主 | 日本語主、英語は文献語として括弧内へ移動 | `index.qmd` | 序論 |
| 再レビュー微修正 | `Spin-c` 表記が付録に残存 | `Spin$^c$` へ統一 | `appendix-analysis.qmd` | 付録A |
| 再レビュー微修正 | 第13章の3列表の読み方が初読者に少し重い | 「初読では右列の結論を先に押さえる」旨を表前に追加 | `13-donaldson-outputs.qmd` | p.55 |

## 最終PDF

- ページ数: 104
- PDFしおり: 28件、最大2階層
- SHA-256: `C702B4B44E3B7658AF4255E318433BFA940F8B89EDE0C229186C65B277C49F7B`
