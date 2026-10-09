# SLE教材 Independent Audit

監査日: 2026-10-09

## 判定

**SLE教材source: PASS**

全18章と4付録を、本文執筆とは別の通読・render確認として監査した。重大な数学的status混同、未解決Reader Stop-Point、欠落source、SLE正規化違反、SLE内のbroken linkは残っていない。

## 検出して修正した重大問題

1. 正式章がMarkdownのインライン・別行数式記法を誤り、Typst PDFで \(\kappa\)、集合、行列が欠落した。全18章をQuarto契約の数式記法へ変換し、全29ページを再renderして修正を確認した。
2. 初稿は18章が各1ページ程度で、確率解析・収束位相・Bessel/Hausdorff・数値誤差の説明が不足した。4付録を追加し、本文の技術的行間を埋めた。
3. \(\kappa=8\) のspace-filling相をRohde--Schrammだけへ帰属していた。UST Peano curveのSLE\(_8\)収束を扱うLawler--Schramm--Wernerもsourceとtheorem registryへ追加した。
4. 収束証明のtightness sourceがregistryになかった。Kemppainen--Smirnovのrandom curve frameworkを一次資料として追加した。

## 数学監査

- hydrodynamic normalizationは \(g_t(z)=z+2t/z+O(|z|^{-2})\)、\(\operatorname{hcap}(K_t)=2t\) で統一。
- Brown駆動は \(U_t=\sqrt\kappa B_t\)。
- Bessel次元は \(1+4/\kappa\)、境界swallowing閾値は \(\kappa=4\)。
- trace次元は \(\min(2,1+\kappa/8)\)。
- curve / trace / hull / driving functionを別対象として扱う。
- Schramm分類と格子模型収束を別の定理として扱う。
- theorem / assumption / black-box theorem / numerical evidence / heuristicを表示する。

## Missing Explanation / Reader Stop-Point

- 新概念は既存方法の不足を示した後に導入している。
- Itô補正、停止時刻、tightness、kernel convergence、drivingからcurveへの回収を付録で補った。
- black boxは入力、出力、難所、下流の利用を説明する。
- 各章末で証明していない範囲と次章の問いを明示する。

## Rendering QA

- SLE authoring validation: PASS（18章、23契約、14 source、5 figure、17 bridge）。
- unittest: 5/5 PASS。
- SLE Web: 23正式ページをrender。375px幅でdocument overflow 0、長い数式は内部scroll、図版欠落0、MathJax表示、dark mode、console warning/error 0。
- PDF: A4、29ページ、PDF 1.7。全ページPNG化し、表紙、数式導出、図版、後半章、付録、参考文献を目視確認。
- portal root render: 178/178 source変換と \(_site/index.html\) 生成に成功。

## Publish Gate

SLE外の既存作業で、4次元ゲージ理論教材が参照する category-layers.svg、gauge-slice.svg、bubbling.svg が欠落しており、repository-wide validate_site.py はFAILする。このためGitHub Pagesへpushしていない。SLE教材自身のlocal link/asset検査では欠落はない。

