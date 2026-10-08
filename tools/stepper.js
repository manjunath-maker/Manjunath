const STEPS = [
  { t: "Clear the map", d: "In your empty layout slot, use the remove-all option so every building and wall goes into the tray at the bottom. The dashed square marks the middle of your village." },
  { t: "Place the Town Hall", d: "Put the Town Hall just above the middle of the village, so its bottom corner touches the dashed centre square." },
  { t: "Fill the core around it", d: "Place a Gold Storage touching the Town Hall on its right, an Elixir Storage touching it on its left, and the Clan Castle directly below. Together the four make a small diamond with no gaps." },
  { t: "Wall in the core", d: "Wrap walls tightly around those four buildings, touching them on every side. That's 9 walls along each edge and 32 walls in total. Close all four corners." },
  { t: "Place the inner ring", d: "Every piece here touches the inner wall from the outside. Wizard Tower and the second Gold Storage go on the upper right edge, Mortar on the lower right edge, Air Defense and the second Elixir Storage on the lower left edge. Leave one empty tile between neighbours." },
  { t: "Add Cannons and Archer Towers", d: "Cannons go on the top corner, the bottom corner and the upper left edge. Archer Towers go on the right corner, the left corner and the lower right edge. The empty spot on the upper left edge is saved for your next new defense." },
  { t: "Close the outer wall", d: "Wrap a second wall box around the whole ring, touching it. That's 17 walls along each edge and 64 in total. Every gap you leave lets troops walk in, so check all four corners." },
  { t: "Put mines and collectors outside", d: "Spread Gold Mines and Elixir Collectors around all four sides. Leave one empty tile between the outer wall and each building, and one between buildings. Use as many spots as you own." },
  { t: "Army buildings and huts", d: "Army Camps go in the top, left and right corners. Barracks goes on the upper left side, the Laboratory on the upper right side, and the Spell Factory on the lower left side. Builder's Huts fit in the bottom corner." },
  { t: "Set the traps", d: "Spring Traps go in the empty lane just outside the outer wall, where Giants walk to it. Bombs go just inside the outer wall in the gaps between ring buildings. The Air Bomb goes next to the Air Defense." },
  { t: "Save and switch it on", d: "Check that both wall boxes are fully closed, then save. Set this layout as your active home village layout, or you'll still be defending with the old one." },
];

const K = LAYOUT.kinds, G = LAYOUT.grid, C = G / 2;
const RING5 = new Set(["WT", "M", "AD"]);
function stepOf(it) {
  const c = it.code;
  if (c === "TH") return 1;
  if (c === "CC" || ((c === "G" || c === "E") && it.x >= 18 && it.x <= 22 && it.y >= 18 && it.y <= 22)) return 2;
  if (RING5.has(c) || c === "G" || c === "E") return 4;
  if (c === "C" || c === "AT") return 5;
  if (c === "GM" || c === "EC") return 7;
  if (K[c].cat === "army") return 8;
  return 9;
}
const pieces = LAYOUT.items.map(it => ({ ...it, size: K[it.code].size, cat: K[it.code].cat, step: stepOf(it) }));
for (const [x, y] of LAYOUT.walls) {
  const inner = x >= 17 && x <= 25 && y >= 17 && y <= 25;
  pieces.push({ code: "", x, y, size: 1, cat: "wall", step: inner ? 3 : 6 });
}

const S = Math.SQRT1_2, SQ = 0.62;
const pt = (x, y) => { const px = x - C, py = y - C; return [(px - py) * S, (px + py) * S * SQ]; };
const poly = (x, y, w) => [pt(x, y), pt(x + w, y), pt(x + w, y + w), pt(x, y + w)].map(p => p.map(v => v.toFixed(2)).join(",")).join(" ");
const R = G * S + 1, H = G * S * SQ + 1;
const VAR = { core: "--c-core", storage: "--c-storage", splash: "--c-splash", ground: "--c-ground", air: "--c-air", collector: "--c-collector", army: "--c-army", trap: "--c-trap", wall: "--wall" };

function render(step) {
  let out = `<svg viewBox="${-R} ${-H} ${2 * R} ${2 * H}" role="img" aria-label="Village map for step ${step + 1}">`;
  out += `<polygon points="${poly(0, 0, G)}" fill="var(--ground)"/>`;
  for (let i = 0; i <= G; i += 4) {
    const a = pt(i, 0), b = pt(i, G), c = pt(0, i), d = pt(G, i);
    out += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="var(--grid)" stroke-width=".05"/>`;
    out += `<line x1="${c[0]}" y1="${c[1]}" x2="${d[0]}" y2="${d[1]}" stroke="var(--grid)" stroke-width=".05"/>`;
  }
  const shown = pieces.filter(p => p.step <= step).sort((a, b) => (a.x + a.y) - (b.x + b.y));
  const labels = [];
  for (const p of shown) {
    const pad = p.size > 1 ? .12 : .1;
    const cls = p.step === step ? "tile new" : "tile old";
    out += `<polygon class="${cls}" points="${poly(p.x + pad, p.y + pad, p.size - 2 * pad)}" fill="var(${VAR[p.cat]})"><title>${p.code ? K[p.code].name : "Wall"}</title></polygon>`;
    if (p.size > 1) {
      const [lx, ly] = pt(p.x + p.size / 2, p.y + p.size / 2);
      const dark = p.cat === "collector" || p.cat === "storage";
      labels.push(`<text x="${lx.toFixed(2)}" y="${ly.toFixed(2)}" font-size="${p.code.length > 2 ? .85 : 1}" class="${dark ? "dark" : ""}" opacity="${p.step === step ? 1 : .6}">${p.code}</text>`);
    }
  }
  if (step <= 1) out += `<polygon class="centre" points="${poly(C - 1, C - 1, 2)}"/>`;
  return out + labels.join("") + "</svg>";
}

const $ = id => document.getElementById(id);
let cur = 0;
const dots = STEPS.map((s, i) => {
  const b = document.createElement("button");
  b.type = "button"; b.setAttribute("role", "tab"); b.setAttribute("aria-label", `Step ${i + 1}: ${s.t}`);
  b.addEventListener("click", () => show(i));
  $("dots").appendChild(b);
  return b;
});
function show(i) {
  cur = Math.max(0, Math.min(STEPS.length - 1, i));
  $("step-count").textContent = `Step ${cur + 1} of ${STEPS.length}`;
  $("step-title").textContent = STEPS[cur].t;
  $("step-text").textContent = STEPS[cur].d;
  $("iso").innerHTML = render(cur === STEPS.length - 1 ? 99 : cur);
  dots.forEach((d, j) => d.setAttribute("aria-selected", j === cur ? "true" : "false"));
  $("prev").disabled = cur === 0;
  $("next").disabled = cur === STEPS.length - 1;
  try { localStorage.setItem("th5-step", cur); } catch (e) {}
}
$("prev").addEventListener("click", () => show(cur - 1));
$("next").addEventListener("click", () => show(cur + 1));
let saved = 0;
try { saved = +localStorage.getItem("th5-step") || 0; } catch (e) {}
show(saved);
