# Release check

作成日: 2026-10-11

## Scope

対象は `gauge-theory-smooth-topology` のみである。他教材、公開設定、外部サービス、PR、デプロイは変更していない。

## Decision

ローカル教材成果物として、旧18章・95ページ版を退避し、22章新稿へ全面再構成した。公開反映はこの作業では実施していない。PDF/Webの機械生成は通過したが、全ページ目視QAとスマホ実表示QAは未実施であるため、公開可能な最終合格ではなくローカル再構成完了と判定する。

## Re-run results

| Check | Result |
|---|---|
| Gauge authoring validation and audit bundle | PASS |
| Unit tests | PASS, 8 tests |
| Site validation | PASS |
| PDF build | PASS |
| Target Quarto render | PASS |
| PDF metadata | PASS, 48 pages, A4, 1,345,553 bytes |
| PDF text regression scan | PASS, no matches |
| Visual PDF review | NOT RUN |
| Mobile browser review | NOT RUN |

## Evidence files

- `production/manifest.json`
- `contracts/*.json`
- `production/PRODUCTION_BOOTSTRAP_REPORT.md`
- `production/environment-inventory.md`
- `production/curriculum-from-scratch.md`
- `production/reader-dependency-map.md`
- `production/chapter-blueprints.md`
- `production/source-reuse-manifest.md`
- `production/old-to-new-coverage-map.md`
- `production/issue-register.md`
- `production/render-qa.md`

## Completion criteria

- 数学的P0: 現在の機械検査と重点語句スキャンでは0。全文専門査読は継続課題。
- 主要説明断絶P1: 22章新稿で主要経路を再配置。完全な読者通読監査は未実施。
- 自然な日本語・用語監査: スキャン対象はPASS。全段落の詳細校閲は未実施。
- 図・演習・解答: 章本文、図版registry、付録Bに配置済み。
- PDF/Web: 機械生成はPASS。全ページ目視とスマホ実表示は未実施。
- 独立査読記録: サブエージェント2件の監査メモと本制作記録を併用する。
- 他教材への影響: 対象外教材は編集しない。

