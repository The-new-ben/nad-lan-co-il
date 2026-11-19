// Walking inside the apartment (HAD-792, gap 17: "the walk ends in front of a blank wall"). Pure functions over the store's
// derived model, no three.js: a walkable grid (inside the rooms, clear of the walls, open through doors and passages),
// a route between two places (A* on the grid, then straightened), and the best way to look from a place (the longest
// free view, a window counts double). Units: cm in the plan frame.
const CELL = 12, CLEAR = 24;

function segDist(px, py, ax, ay, bx, by) {
  const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy;
  let t = l2 ? ((px - ax) * dx + (py - ay) * dy) / l2 : 0; t = t < 0 ? 0 : t > 1 ? 1 : t;
  return Math.hypot(px - (ax + dx * t), py - (ay + dy * t));
}
const pip = (x, y, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const a = poly[i], b = poly[j]; if ((a[1] > y) !== (b[1] > y) && x < ((b[0] - a[0]) * (y - a[1])) / (b[1] - a[1]) + a[0]) c = !c; } return c; };

/** the solid parts of every wall (doors and passages cut out, windows stay solid) and the window spans */
function pieces(dv) {
  const solid = [], windows = [], doors = [];
  for (const w of dv.walls) {
    if (w.kind === 'divider' || w.L < 1) continue;
    const at = (s) => [w.pa[0] + w.dir[0] * s, w.pa[1] + w.dir[1] * s];
    let c = 0;
    const ops = [...(w.openings || [])].sort((a, b) => a.at - b.at);
    for (const o of ops) {
      if (o.type === 'window') { windows.push([...at(o.at), ...at(o.at + o.w), w]); continue; }
      if (w.kind === 'rail') continue; // a railing has no door
      if (o.at > c) solid.push([...at(c), ...at(o.at)]);
      doors.push({ a: at(o.at), b: at(o.at + o.w), n: [-w.dir[1], w.dir[0]], t: w.t || 10 });
      c = o.at + o.w;
    }
    if (w.L > c) solid.push([...at(c), ...at(w.L)]);
    if (w.kind === 'rail') { /* the railing is solid along its whole length */ }
  }
  return { solid, windows, doors };
}

export function buildNav(dv) {
  const faces = dv.faces.filter((f) => f.room);
  if (!faces.length) return null;
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const f of faces) for (const p of f.poly) { x0 = Math.min(x0, p[0]); y0 = Math.min(y0, p[1]); x1 = Math.max(x1, p[0]); y1 = Math.max(y1, p[1]); }
  x0 -= CELL * 2; y0 -= CELL * 2;
  const W = Math.ceil((x1 - x0) / CELL) + 4, H = Math.ceil((y1 - y0) / CELL) + 4;
  const { solid, windows, doors } = pieces(dv);
  const free = new Uint8Array(W * H), room = new Int16Array(W * H).fill(-1);
  for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
    const x = x0 + (i + 0.5) * CELL, y = y0 + (j + 0.5) * CELL;
    let r = -1;
    for (let k = 0; k < faces.length; k++) if (pip(x, y, faces[k].poly)) { r = k; break; }
    let inDoor = false;
    if (r < 0) for (const d of doors) { // the doorway itself, across the thickness of the wall
      const dx = d.b[0] - d.a[0], dy = d.b[1] - d.a[1], L = Math.hypot(dx, dy) || 1, s = ((x - d.a[0]) * dx + (y - d.a[1]) * dy) / L, n = Math.abs((x - d.a[0]) * d.n[0] + (y - d.a[1]) * d.n[1]);
      if (s > CLEAR * 0.6 && s < L - CLEAR * 0.6 && n < d.t / 2 + CELL) { inDoor = true; break; }
    }
    if (r < 0 && !inDoor) continue;
    let near = Infinity;
    for (const s of solid) { const d = segDist(x, y, s[0], s[1], s[2], s[3]); if (d < near) near = d; if (near < CLEAR) break; }
    for (const s of windows) { const d = segDist(x, y, s[0], s[1], s[2], s[3]); if (d < near) near = d; if (near < CLEAR) break; }
    const k = j * W + i;
    if (near >= CLEAR) { free[k] = 1; room[k] = r; }
  }
  const nav = { x0, y0, W, H, free, room, faces, windows, CELL };
  nav.cell = (x, y) => [Math.floor((x - x0) / CELL), Math.floor((y - y0) / CELL)];
  nav.at = (i, j) => [x0 + (i + 0.5) * CELL, y0 + (j + 0.5) * CELL];
  nav.isFree = (x, y) => { const [i, j] = nav.cell(x, y); return i >= 0 && j >= 0 && i < W && j < H && free[j * W + i] === 1; };
  return nav;
}

/** the free cell nearest to (x, y), optionally inside one room (face index) */
export function nearestFree(nav, x, y, faceIdx = -1) {
  const [ci, cj] = nav.cell(x, y);
  let best = null, bd = Infinity;
  for (let j = 0; j < nav.H; j++) for (let i = 0; i < nav.W; i++) {
    const k = j * nav.W + i;
    if (!nav.free[k] || (faceIdx >= 0 && nav.room[k] !== faceIdx)) continue;
    const d = (i - ci) * (i - ci) + (j - cj) * (j - cj);
    if (d < bd) { bd = d; best = [i, j]; }
  }
  return best ? nav.at(best[0], best[1]) : null;
}

function lineFree(nav, a, b) {
  const n = Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / (nav.CELL * 0.5));
  for (let s = 0; s <= n; s++) { const t = n ? s / n : 0; if (!nav.isFree(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)) return false; }
  return true;
}

/** a walkable route from a to b (cm), straightened; null when there is none. The end is moved to the nearest free place. */
export function route(nav, a, b) {
  if (!nav) return null;
  const A = nav.isFree(a[0], a[1]) ? a : nearestFree(nav, a[0], a[1]);
  const B = nav.isFree(b[0], b[1]) ? b : nearestFree(nav, b[0], b[1]);
  if (!A || !B) return null;
  const [si, sj] = nav.cell(A[0], A[1]), [ti, tj] = nav.cell(B[0], B[1]), W = nav.W, H = nav.H;
  const g = new Float32Array(W * H).fill(Infinity), from = new Int32Array(W * H).fill(-1), done = new Uint8Array(W * H);
  const open = [[0, sj * W + si]]; g[sj * W + si] = 0;
  const h = (k) => Math.hypot((k % W) - ti, Math.floor(k / W) - tj);
  const push = (f, k) => { open.push([f, k]); let i = open.length - 1; while (i > 0) { const p = (i - 1) >> 1; if (open[p][0] <= open[i][0]) break; [open[p], open[i]] = [open[i], open[p]]; i = p; } };
  const pop = () => { const top = open[0], last = open.pop(); if (open.length) { open[0] = last; let i = 0; for (;;) { const l = 2 * i + 1, r = l + 1; let m = i; if (l < open.length && open[l][0] < open[m][0]) m = l; if (r < open.length && open[r][0] < open[m][0]) m = r; if (m === i) break; [open[m], open[i]] = [open[i], open[m]]; i = m; } } return top; };
  const goal = tj * W + ti;
  let found = false;
  while (open.length) {
    const [, k] = pop();
    if (done[k]) continue; done[k] = 1;
    if (k === goal) { found = true; break; }
    const i = k % W, j = (k - i) / W;
    for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
      if (!di && !dj) continue;
      const ni = i + di, nj = j + dj; if (ni < 0 || nj < 0 || ni >= W || nj >= H) continue;
      const nk = nj * W + ni; if (!nav.free[nk] || done[nk]) continue;
      if (di && dj && (!nav.free[j * W + ni] || !nav.free[nj * W + i])) continue; // no corner cutting
      const ng = g[k] + (di && dj ? 1.4142 : 1);
      if (ng < g[nk]) { g[nk] = ng; from[nk] = k; push(ng + h(nk), nk); }
    }
  }
  if (!found) return null;
  const cells = []; for (let k = goal; k !== -1; k = from[k]) cells.push(k);
  cells.reverse();
  const pts = cells.map((k) => nav.at(k % W, Math.floor(k / W)));
  pts[0] = A; pts[pts.length - 1] = B;
  const out = [pts[0]]; let i = 0;
  while (i < pts.length - 1) { let j = pts.length - 1; while (j > i + 1 && !lineFree(nav, pts[i], pts[j])) j--; out.push(pts[j]); i = j; }
  return out;
}

/** how far you see from p looking along yaw, and whether a window is at the end of that look */
function look(nav, p, yaw) {
  const dx = Math.cos(yaw), dy = Math.sin(yaw);
  let d = 0;
  while (d < 2000 && nav.isFree(p[0] + dx * (d + nav.CELL), p[1] + dy * (d + nav.CELL))) d += nav.CELL;
  const ex = p[0] + dx * (d + CLEAR + 30), ey = p[1] + dy * (d + CLEAR + 30), qx = p[0] + dx * d, qy = p[1] + dy * d;
  let win = false;
  for (const s of nav.windows) { if (segDist(ex, ey, s[0], s[1], s[2], s[3]) < 40 || segDist(qx, qy, s[0], s[1], s[2], s[3]) < CLEAR + 30) { win = true; break; } }
  return { d, win };
}
/** the yaw (radians, plan frame: 0 = +x, clockwise on the sheet) that shows the most of the apartment from p, a window first */
export function bestYaw(nav, p, prefer = null) {
  let best = 0, score = -Infinity;
  for (let a = 0; a < 48; a++) {
    const yaw = (a / 48) * Math.PI * 2, l = look(nav, p, yaw);
    let wide = 0; for (let k = -4; k <= 4; k++) if (k) wide += look(nav, p, yaw + k * 0.14).d; // the whole picture, not one line: a room in view, not a wall
    let s = l.d * (l.win ? 1.5 : 1) + (l.win ? 160 : 0) + (wide / 8) * 1.2;
    if (prefer != null) s -= Math.abs(Math.atan2(Math.sin(yaw - prefer), Math.cos(yaw - prefer))) * 40; // keep close to the way you walked
    if (s > score) { score = s; best = yaw; }
  }
  return best;
}
/** how far a wall is straight ahead (cm) */
export const ahead = (nav, p, yaw) => look(nav, p, yaw).d;

/** where to stand in a room: its widest free spot (farthest from its own walls), so you see the room, not a wall */
export function roomSpot(nav, faceIdx) {
  let best = null, bd = -Infinity;
  const W = nav.W, f = nav.faces[faceIdx], cx = (f.bb.x0 + f.bb.x1) / 2, cy = (f.bb.y0 + f.bb.y1) / 2;
  for (let j = 0; j < nav.H; j++) for (let i = 0; i < W; i++) {
    const k = j * W + i; if (!nav.free[k] || nav.room[k] !== faceIdx) continue;
    let r = 0; // free radius in cells, capped
    for (; r < 10; r++) { if (!nav.free[Math.max(0, j - r) * W + i] || !nav.free[Math.min(nav.H - 1, j + r) * W + i] || !nav.free[j * W + Math.max(0, i - r)] || !nav.free[j * W + Math.min(W - 1, i + r)]) break; }
    const c = nav.at(i, j), sc = Math.min(r, 8) * 1000 - Math.hypot(c[0] - cx, c[1] - cy); // wide enough first, then the middle of the room
    if (sc > bd) { bd = sc; best = [i, j]; }
  }
  return best ? nav.at(best[0], best[1]) : null;
}
/** the room to start the walk in: the living room, else the largest room */
export function startFace(nav) {
  let li = nav.faces.findIndex((f) => f.room.type === 'living');
  if (li < 0) li = nav.faces.findIndex((f) => /סלון|דיור/.test(f.room.name_he || ''));
  if (li < 0) { let m = -1; nav.faces.forEach((f, i) => { if (f.room.type !== 'balcony' && f.net > m) { m = f.net; li = i; } }); }
  return li;
}
/** an order for a tour of every room: start, then always the nearest room not yet seen (tiny rooms under 2 m² skipped) */
export function tourOrder(nav, from) {
  const spots = nav.faces.map((f, i) => ({ i, p: f.net >= 2 ? roomSpot(nav, i) : null })).filter((s) => s.p);
  const out = [], left = new Set(spots.map((s) => s.i)); let cur = from;
  while (left.size) {
    let pick = null, pd = Infinity;
    for (const s of spots) if (left.has(s.i)) { const d = Math.hypot(s.p[0] - cur[0], s.p[1] - cur[1]); if (d < pd) { pd = d; pick = s; } }
    left.delete(pick.i); out.push(pick); cur = pick.p;
  }
  return out;
}
