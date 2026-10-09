"""Generate deterministic SLE production-fixture figures without extra dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "sle-critical-phenomena" / "assets" / "figures"


def metadata(figure_id: str, animated: bool, fallback: str | None = None) -> str:
    payload = {
        "figure_id": figure_id,
        "generator": "scripts/generate_sle_figures.py",
        "deterministic": True,
        "animated": animated,
        "simulation": False,
        "print_fallback": fallback,
        "license": "repository content",
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def vertical_slit_svg() -> str:
    grid_left = "".join(
        f'<path d="M {x} 42 V 248" />' for x in range(56, 311, 32)
    ) + "".join(f'<path d="M 42 {y} H 326" />' for y in range(72, 249, 32))
    grid_right = "".join(
        f'<path d="M {x} 42 V 248" />' for x in range(414, 669, 32)
    ) + "".join(f'<path d="M 400 {y} H 684" />' for y in range(72, 249, 32))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 726 300" role="img" aria-labelledby="title desc">
<title id="title">縦スリット写像</title>
<desc id="desc">左の上半平面から縦スリットを除いた領域を、右の上半平面へ等角写像で戻す模式図。</desc>
<metadata>{metadata("fig-slit-map", False)}</metadata>
<defs>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#16283b"/><stop offset="1" stop-color="#0c1621"/></linearGradient>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#68d39b"/></marker>
</defs>
<rect width="726" height="300" rx="18" fill="#0b1118"/>
<g fill="url(#panel)" stroke="#314b64"><rect x="34" y="34" width="300" height="224" rx="12"/><rect x="392" y="34" width="300" height="224" rx="12"/></g>
<g fill="none" stroke="#27425c" stroke-width="1" opacity=".9">{grid_left}{grid_right}</g>
<g stroke="#9dccff" stroke-width="3"><path d="M42 248 H326"/><path d="M400 248 H684"/></g>
<path d="M184 248 V112" fill="none" stroke="#ffb86b" stroke-width="9" stroke-linecap="round"/>
<circle cx="184" cy="112" r="6" fill="#ffd19a"/>
<path d="M344 146 C360 126 374 126 390 146" fill="none" stroke="#68d39b" stroke-width="3" marker-end="url(#arrow)"/>
<circle cx="542" cy="248" r="7" fill="#ffb86b"/>
<g fill="#e7edf4" font-family="system-ui, sans-serif" font-size="15"><text x="54" y="60">ℍ \\ Kₜ</text><text x="412" y="60">ℍ</text><text x="321" y="116" text-anchor="end">2i√t</text><text x="363" y="112" text-anchor="middle" fill="#68d39b">gₜ</text><text x="184" y="278" text-anchor="middle">0</text><text x="542" y="278" text-anchor="middle">0</text></g>
</svg>
'''


def driving_trace_svg(animated: bool) -> str:
    animation = "" if not animated else '''
<circle r="6" fill="#ffd19a"><animateMotion dur="4s" repeatCount="indefinite" path="M108 242 C105 204 142 194 131 158 C120 124 163 104 154 62"/></circle>
<circle r="5" fill="#ffd19a"><animateMotion dur="4s" repeatCount="indefinite" path="M410 226 C452 204 425 180 470 158 C510 138 468 112 525 86"/></circle>
<path d="M108 242 C105 204 142 194 131 158 C120 124 163 104 154 62" fill="none" stroke="#ffb86b" stroke-width="7" stroke-linecap="round" stroke-dasharray="280" stroke-dashoffset="280"><animate attributeName="stroke-dashoffset" values="280;0;0" keyTimes="0;.85;1" dur="4s" repeatCount="indefinite"/></path>
<path d="M410 226 C452 204 425 180 470 158 C510 138 468 112 525 86" fill="none" stroke="#68d39b" stroke-width="4" stroke-linecap="round" stroke-dasharray="260" stroke-dashoffset="260"><animate attributeName="stroke-dashoffset" values="260;0;0" keyTimes="0;.85;1" dur="4s" repeatCount="indefinite"/></path>'''
    static_paths = "" if animated else '''
<path d="M108 242 C105 204 142 194 131 158 C120 124 163 104 154 62" fill="none" stroke="#ffb86b" stroke-width="7" stroke-linecap="round"/>
<circle cx="154" cy="62" r="6" fill="#ffd19a"/>
<path d="M410 226 C452 204 425 180 470 158 C510 138 468 112 525 86" fill="none" stroke="#68d39b" stroke-width="4" stroke-linecap="round"/>
<circle cx="525" cy="86" r="5" fill="#d6ffe9"/>'''
    figure_id = "fig-driving-trace" if animated else "fig-driving-trace-print"
    fallback = "assets/figures/driving-trace-print.svg" if animated else None
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 300" role="img" aria-labelledby="title desc">
<title id="title">hullと駆動関数</title>
<desc id="desc">左に上半平面で成長するhull、右に時間に対する実数値駆動関数を同期して示す。</desc>
<metadata>{metadata(figure_id, animated, fallback)}</metadata>
<rect width="640" height="300" rx="18" fill="#0b1118"/>
<g fill="#101d2a" stroke="#314b64"><rect x="26" y="34" width="270" height="224" rx="12"/><rect x="344" y="34" width="270" height="224" rx="12"/></g>
<g stroke="#9dccff" stroke-width="2.5"><path d="M42 242 H280"/><path d="M370 226 H594"/><path d="M390 244 V54"/></g>
<g stroke="#37536d" stroke-width="1"><path d="M108 242 V54" stroke-dasharray="4 5"/><path d="M390 158 H594" stroke-dasharray="4 5"/></g>
{static_paths}{animation}
<g fill="#e7edf4" font-family="system-ui, sans-serif" font-size="15"><text x="44" y="58">hull Kₜ</text><text x="362" y="58">driving Uₜ</text><text x="596" y="244">t</text><text x="372" y="62">U</text></g>
<text x="320" y="283" text-anchor="middle" fill="#9daabc" font-family="system-ui, sans-serif" font-size="13">標準化後の先端位置を一次元で記録する</text>
</svg>
'''


def percolation_svg() -> str:
    cells = []
    colors = ("#dce8f3", "#27394b")
    for row in range(5):
        for col in range(9):
            x = 46 + col * 58 + (row % 2) * 29
            y = 48 + row * 46
            color = colors[(row * 7 + col * 3 + row * col) % 2]
            cells.append(
                f'<polygon points="{x},{y-24} {x+25},{y-12} {x+25},{y+12} '
                f'{x},{y+24} {x-25},{y+12} {x-25},{y-12}" fill="{color}" '
                'stroke="#6f8599" stroke-width="1"/>'
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 310" role="img" aria-labelledby="title desc">
<title id="title">Percolation探索経路</title>
<desc id="desc">白黒の六角形セルの境界を、白を左、黒を右に見て進む橙色の探索経路。</desc>
<metadata>{metadata("fig-percolation", False)}</metadata>
<rect width="620" height="310" rx="18" fill="#0b1118"/>
<g>{''.join(cells)}</g>
<path d="M18 250 C70 244 65 205 118 204 S154 158 211 163 S246 117 302 120 S352 78 408 92 S478 54 598 62"
 fill="none" stroke="#ff9f5b" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="18" cy="250" r="8" fill="#ffd19a"/><circle cx="598" cy="62" r="8" fill="#ffd19a"/>
<g fill="#eef5fb" font-family="system-ui, sans-serif" font-size="15"><text x="18" y="285">aδ</text><text x="576" y="38">bδ</text></g>
</svg>
'''


def kappa_phases_svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 300" role="img" aria-labelledby="title desc">
<title id="title">SLEの三つの幾何相</title>
<desc id="desc">単純曲線、自己接触して領域を囲む曲線、空間充填曲線を三つのパネルで比較する。</desc>
<metadata>{metadata("fig-kappa-phases", False)}</metadata>
<rect width="780" height="300" rx="18" fill="#0b1118"/>
<g fill="#111f2c" stroke="#324b61"><rect x="20" y="36" width="230" height="224" rx="12"/><rect x="275" y="36" width="230" height="224" rx="12"/><rect x="530" y="36" width="230" height="224" rx="12"/></g>
<path d="M78 242 C61 205 128 196 91 155 C66 126 145 111 173 63" fill="none" stroke="#68d39b" stroke-width="7" stroke-linecap="round"/>
<path d="M333 242 C324 203 424 213 403 161 C392 135 329 151 343 104 C354 67 453 70 431 122 C416 160 361 130 373 93" fill="none" stroke="#ffb86b" stroke-width="7" stroke-linecap="round"/>
<path d="M553 236 H737 V62 H558 V207 H710 V89 H586 V181 H682 V116 H612 V154 H655" fill="none" stroke="#9dccff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M330 242 C320 202 426 214 406 160 C393 126 333 155 340 103 C346 65 456 65 438 126 C428 160 374 143 374 96 L374 242 Z" fill="#ffb86b" opacity=".16"/>
<g fill="#e7edf4" font-family="system-ui, sans-serif" text-anchor="middle"><text x="135" y="25">0 ≤ κ ≤ 4</text><text x="390" y="25">4 &lt; κ &lt; 8</text><text x="645" y="25">κ ≥ 8</text><text x="135" y="282">simple</text><text x="390" y="282">self-touching / hull</text><text x="645" y="282">space-filling</text></g>
</svg>
'''


def left_passage_svg() -> str:
    points = " ".join(
        f"{55 + i * 26},{235 - y}" for i, y in enumerate(
            [4, 7, 12, 20, 33, 51, 75, 102, 130, 154, 172, 185, 193, 198, 201, 203, 204, 205, 206, 206, 206]
        )
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 300" role="img" aria-labelledby="title desc">
<title id="title">Left-passage probability</title>
<desc id="desc">傾きx/yに対して0から1へ単調に増える左側通過確率。中心では2分の1。</desc>
<metadata>{metadata("fig-left-passage", False)}</metadata>
<rect width="640" height="300" rx="18" fill="#0b1118"/>
<g stroke="#344e64" stroke-width="1"><path d="M55 30 V245 H590"/><path d="M55 137 H590" stroke-dasharray="5 5"/><path d="M315 30 V245" stroke-dasharray="5 5"/></g>
<polyline points="{points}" fill="none" stroke="#68d39b" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="315" cy="132" r="6" fill="#ffd19a"/>
<g fill="#e7edf4" font-family="system-ui, sans-serif" font-size="14"><text x="20" y="38">1</text><text x="20" y="142">1/2</text><text x="28" y="246">0</text><text x="305" y="270">x/y</text><text x="326" y="120">p(0)=1/2</text></g>
</svg>
'''


def generate(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    assets = {
        "vertical-slit-map.svg": vertical_slit_svg(),
        "driving-trace.svg": driving_trace_svg(animated=True),
        "driving-trace-print.svg": driving_trace_svg(animated=False),
        "percolation-interface.svg": percolation_svg(),
        "kappa-phases.svg": kappa_phases_svg(),
        "left-passage.svg": left_passage_svg(),
    }
    written: list[Path] = []
    for name, content in assets.items():
        path = output_dir / name
        path.write_text(content, encoding="utf-8", newline="\n")
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    for path in generate(args.output_dir):
        print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


if __name__ == "__main__":
    main()
