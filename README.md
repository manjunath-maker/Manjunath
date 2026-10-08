# Manju's TH5 Farming Base

A Clash of Clans home village layout for Town Hall 5, built to protect loot.
Open `th5-farming-base.html` in a browser to see the tile map and step-by-step build guide.

- Two closed wall rings (96 walls): Town Hall, a Gold Storage, an Elixir Storage and the Clan Castle in the inner box. The other storages and all defenses go in the ring around it.
- Mines, collectors and army buildings outside the walls as bait.
- `tools/gen_layout.py` places every building on the 44×44 grid and fails if anything overlaps.
  `tools/build_page.py` renders the page from `layout.json`.

Rebuild after editing the layout:

```sh
python3 tools/gen_layout.py && python3 tools/build_page.py
```
