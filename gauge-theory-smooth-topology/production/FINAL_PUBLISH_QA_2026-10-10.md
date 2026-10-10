# Final Publish QA

対象教材: 4次元ゲージ理論と滑らかな位相  
QA日: 2026-10-10  
状態: 公開投入済み差分の最終QA

## 取り込んだ監査指摘

- SW二次写像 `q(Phi)` の型規約を明示し、`rho(q(Phi))=i(Phi Phi*)_0` として曲率方程式の両辺が `i Lambda^2_+` のsectionになるよう固定した。
- 第8章のHodge型分解で、余核側の随伴像を `im d_A^{+,*}` と明示し、slice条件の `d_A^*` と区別した。
- 第12章に、固定した `SO(3)` 束、`mu`-class、cut-down、orientation、compactification、1-parameter cobordismを通すDonaldson不変量の最小経路を追加した。
- 第13章に、Donaldson対角化定理の束選択、低次元ASD moduli、reducible link、格子補題への翻訳を加えた。
- 第17章に、連結和消滅定理の標準的な仮定を明記した。
- 第18章に、Taubes定理とadjunction inequalityの使用版、仮定、例外、用途を明記した。
- 接続の局所自明化図、cut-down/cobordism図を追加し、manifestと章契約へ登録した。
- PDFビルダーを修正し、統合PDFの目次をPart、章、節の階層で出すようにした。

## 検証

- `python scripts/validate_gauge_authoring.py --audit-bundle dist/gauge-theory-audit`: PASS
- `python -m unittest tests.test_gauge_authoring`: PASS, 4 tests
- `python scripts/validate_site.py`: PASS
- `git diff --check -- . ':!gauge-theory-smooth-topology/assets/gauge-theory-smooth-topology.pdf'`: PASS
- `quarto render gauge-theory-smooth-topology`: PASS, 21 pages rendered to `_site/gauge-theory-smooth-topology/index.html`
- `python scripts/build_gauge_theory_pdf.py`: PASS
- `pdfinfo gauge-theory-smooth-topology/assets/gauge-theory-smooth-topology.pdf`: 63 pages, A4, 2,108,157 bytes
- `pdftotext` spot check: no `qquad` or stale `Phi\otimes` rendering residue detected
- PDF visual spot check: pages 1, 20, 35, 55, 63 inspected as PNG; no clipping, overlap, missing figure, or broken bibliography observed
- Web visual spot check: desktop 1280x900 and mobile 390x844 dark-mode screenshots captured through Playwright CLI

## Known limits

- Playwright JavaScript metric evaluation did not run because the temporary `npx` package was not available to `require()` from the repository process. CLI screenshots succeeded and visual inspection was performed.
- The repository still contains unrelated untracked `sle-critical-phenomena/production/` and `test-results/` entries; they were not included in the publication commit.
