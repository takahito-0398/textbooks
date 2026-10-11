# Japanese language audit

作成日: 2026-10-11

## Scope

本文、図版SVG、索引・演習、PDF抽出テキストで、英語混入、破損語、不自然な日英混成、過去レビューで確認された語を監査対象とした。

## Regression policy

`scripts/validate_gauge_authoring.py` の `CORRUPTION_PATTERNS` は、過去に確認された次の種類の欠陥を検出する。

- `インスタントンs`、`ららか` などの破損語
- `hyperbolic form`、`exact form`、`curvature項` などの日英混成
- Fintushel-Stern貼り合わせの誤説明
- `open dense`、`broken configuration`、`contraction mapping` などの未処理英語句

## Result

Round 7の検証記録では、章本文とPDF抽出テキストの対象語句スキャンはPASSである。人名、標準略号、文献検索に必要な原語は、意味を失わない範囲で保持する。

