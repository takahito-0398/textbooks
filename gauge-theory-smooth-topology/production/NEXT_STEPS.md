# 次の制作単位

2026-10-09 20:44 +09:00時点で、全章ドラフト・render・独立監査後の第一増補を実施した。Chapter 7--12にSobolev設定、局所sliceの非線形項、ASD変形複体のsymbol計算、Fredholm estimate、具体的index計算、Kuranishi模型、transversalityの限界、BPST scale collapse、energy量子化、Uhlenbeck stratumのcodimension、parameterized moduli、wall-crossing、$\mu$-mapの説明を追加した。確認問題も7問から12問へ増やした。

Web 21ページと統合PDFは再生成済みで、PDFは29ページから37ページになった。validator、unit test、site validation、対象HTML render、PDF render、PDF代表ページ目視は通過した。

ただし完成判定は引き続きFAILである。確定監査が要求するCore 300--380頁、Appendix 100--150頁に対し、現在の37ページはまだ詳細アウトラインの範囲に留まる。

次回は章数を増やさず、既存18章を次の順で増補する。

1. Chapter 7--12の第二増補: 各章にworked example、補題単位の証明、Reader Stop-Point、章末演習をさらに追加し、このPartだけで独立した解析入門として読める厚さにする。
2. Chapter 1--6: handle・intersection formの具体計算、Chern--Weil導出、BPST instantonの局所計算を追加する。
3. Chapter 15--18: Spin-c構造、Weitzenbock formula、SW compactness、Kahler reduction、Taubesの証明アーキテクチャを増補する。
4. Appendix: Sobolev解析、格子、特性類、Spin-c、gluing、演習と解答を独立参照できる厚さにする。
5. source coverage: Atiyah--Singer、Sard--Smale、Donaldson不変量、SW構成、adjunction inequalityの標準文献をregistryとbibliographyへ追加する。
6. 増補後にReader Stop-Point、数学、出典、後半品質を再監査し、PDF頁数ではなく説明欠落の解消を根拠にacceptする。

publish、commit、pushは、独立監査の重大FAILが解消するまで行わない。
