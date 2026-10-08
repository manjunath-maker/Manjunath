"""Generate Manju's TH5 farming base (44x44 tile village) and check it.

Run: python3 tools/gen_layout.py
Writes layout.json at the repo root and prints building counts.
Exits non-zero if anything overlaps or falls off the map.
"""
import json
import sys
from pathlib import Path

GRID = 44

# code -> (name, size, category)
KINDS = {
    "TH": ("Town Hall", 4, "core"),
    "CC": ("Clan Castle", 3, "core"),
    "G": ("Gold Storage", 3, "storage"),
    "E": ("Elixir Storage", 3, "storage"),
    "M": ("Mortar", 3, "splash"),
    "WT": ("Wizard Tower", 3, "splash"),
    "AD": ("Air Defense", 3, "air"),
    "C": ("Cannon", 3, "ground"),
    "AT": ("Archer Tower", 3, "ground"),
    "GM": ("Gold Mine", 3, "collector"),
    "EC": ("Elixir Collector", 3, "collector"),
    "AC": ("Army Camp", 4, "army"),
    "B": ("Barracks", 3, "army"),
    "LAB": ("Laboratory", 3, "army"),
    "SF": ("Spell Factory", 3, "army"),
    "BH": ("Builder's Hut", 2, "army"),
    "SP": ("Spring Trap", 1, "trap"),
    "BO": ("Bomb", 1, "trap"),
    "AB": ("Air Bomb", 1, "trap"),
}

items = []


def put(code, x, y):
    items.append({"code": code, "x": x, "y": y})


# Inner core (walls on lines 17 and 25, inside 18..24)
put("TH", 18, 18)
put("G", 22, 18)
put("E", 18, 22)
put("CC", 22, 22)

# Middle ring (between walls 13 and 17 / 25 and 29), clockwise from top-left
ring = [
    ((14, 14), "C"), ((18, 14), "WT"), ((22, 14), "G"), ((26, 14), "AT"),
    ((26, 18), "M"), ((26, 22), "AT"),
    ((26, 26), "C"), ((22, 26), "E"), ((18, 26), "AD"), ((14, 26), "AT"),
    ((14, 22), "C"),
]
for (x, y), code in ring:
    put(code, x, y)
# (14, 18) left empty on purpose: room for the next defense you unlock

# Outside: collectors and army buildings as a buffer, 1 tile apart
outer = {
    "N": ["GM", "EC", "LAB", "EC", "GM"],
    "S": ["EC", "GM", "SF", "GM", "EC"],
    "W": ["GM", "EC", "B", "EC", "GM"],
    "E": ["EC", "GM", "", "GM", "EC"],
}
for side, codes in outer.items():
    for n, code in enumerate(codes):
        if not code:
            continue
        t = 12 + 4 * n
        pos = {"N": (t, 9), "S": (t, 31), "W": (9, t), "E": (31, t)}[side]
        put(code, *pos)
for x, y in [(4, 4), (36, 4), (4, 36)]:
    put("AC", x, y)
put("BH", 37, 37)
put("BH", 40, 37)

# Traps: springs in the gaps troops walk through to reach the wall,
# bombs just inside the outer wall, air bomb next to the Air Defense
for x, y in [(15, 12), (27, 30), (12, 27), (30, 15)]:
    put("SP", x, y)
for x, y in [(17, 15), (25, 27), (15, 25), (27, 17)]:
    put("BO", x, y)
put("AB", 21, 27)

# Walls: outer box (13..29) and inner box (17..25)
walls = set()
for lo, hi in [(13, 29), (17, 25)]:
    for t in range(lo, hi + 1):
        walls |= {(lo, t), (hi, t), (t, lo), (t, hi)}

# ---- validation -------------------------------------------------------
occ = {p: "wall" for p in walls}
errors = []
for it in items:
    name, size, _ = KINDS[it["code"]]
    for dx in range(size):
        for dy in range(size):
            p = (it["x"] + dx, it["y"] + dy)
            if not (0 <= p[0] < GRID and 0 <= p[1] < GRID):
                errors.append(f"{name} at {it['x']},{it['y']} off map")
            elif p in occ:
                errors.append(f"{name} at {it['x']},{it['y']} overlaps {occ[p]}")
            else:
                occ[p] = f"{name}@{it['x']},{it['y']}"

counts = {}
for it in items:
    counts[it["code"]] = counts.get(it["code"], 0) + 1
print("Walls", len(walls))
for code, n in sorted(counts.items()):
    print(f"{KINDS[code][0]:18s} {n}")
if errors:
    print("\n".join(sorted(set(errors))))
    sys.exit(1)

out = {
    "grid": GRID,
    "kinds": {k: {"name": v[0], "size": v[1], "cat": v[2]} for k, v in KINDS.items()},
    "items": items,
    "walls": sorted(walls),
}
Path(__file__).resolve().parent.parent.joinpath("layout.json").write_text(json.dumps(out))
print("ok")
