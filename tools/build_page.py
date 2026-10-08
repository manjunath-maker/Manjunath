"""Render layout.json into th5-farming-base.html (self-contained)."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
d = json.loads((root / "layout.json").read_text())
G = d["grid"]
K = d["kinds"]

svg = [f'<svg viewBox="-1 -1 {G + 2} {G + 2}" role="img" aria-label="Tile map of the TH5 farming base">']
svg.append(f'<rect x="0" y="0" width="{G}" height="{G}" class="field"/>')
for i in range(0, G + 1, 4):
    svg.append(f'<line x1="{i}" y1="0" x2="{i}" y2="{G}" class="grid"/>')
    svg.append(f'<line x1="0" y1="{i}" x2="{G}" y2="{i}" class="grid"/>')
for x, y in d["walls"]:
    svg.append(f'<rect x="{x + .08}" y="{y + .08}" width=".84" height=".84" class="wall"/>')
for it in sorted(d["items"], key=lambda i: -K[i["code"]]["size"]):
    k = K[it["code"]]
    s = k["size"]
    x, y = it["x"], it["y"]
    pad = .12 if s > 1 else .18
    svg.append(
        f'<g class="b {k["cat"]}"><title>{k["name"]} (tile {x},{y})</title>'
        f'<rect x="{x + pad}" y="{y + pad}" width="{s - 2 * pad}" height="{s - 2 * pad}" rx="{.35 if s > 1 else .32}"/>'
    )
    if s > 1:
        fs = 1.0 if len(it["code"]) <= 2 else .8
        svg.append(f'<text x="{x + s / 2}" y="{y + s / 2}" font-size="{fs}">{it["code"]}</text>')
    svg.append("</g>")
svg.append("</svg>")

legend_cats = [
    ("core", "Town Hall & Clan Castle"),
    ("storage", "Storages (what raiders want)"),
    ("splash", "Splash defense"),
    ("ground", "Cannon / Archer Tower"),
    ("air", "Air Defense"),
    ("collector", "Mines & collectors"),
    ("army", "Army buildings"),
    ("trap", "Traps"),
]
legend = "".join(
    f'<li><span class="sw {c}"></span>{label}</li>' for c, label in legend_cats
)
codes = "".join(
    f"<li><b>{c}</b> {v['name']}</li>" for c, v in K.items() if v["size"] > 1
)

page = (root / "tools" / "page_template.html").read_text()
page = page.replace("{{SVG}}", "\n".join(svg)).replace("{{LEGEND}}", legend).replace("{{CODES}}", codes)
(root / "th5-farming-base.html").write_text(page)
print("wrote th5-farming-base.html")
