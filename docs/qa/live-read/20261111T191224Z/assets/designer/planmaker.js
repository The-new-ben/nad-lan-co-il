// "My plan" (התוכנית שלי): a person loads the plan of their own apartment (or a whole floor), goes over the walls, and the
// designer opens on THEIR apartment. Phone first. Nothing leaves the device: the picture stays in this browser
// (IndexedDB), the drawing in localStorage ('nd-myplan'), a PDF is read here by pdf.js.
//
//   import { mountPlanMaker, loadMyPlan } from '.../assets/designer/planmaker.js';
//   const pm = await mountPlanMaker(host, { lang, version, project, helpUrl, draft, onDone(plan, draft), onCancel() });
//   pm.getDraft(); pm.propose({ segments, cmPerPx }); pm.destroy();
//
// It draws inside the host's shadow root (the same one the designer uses) with the designer's own look (designer.css).
import { analyzeDraft, cleanGraph, roomChoices, OPEN_TYPES, WALL_T, DRAW_KINDS, segDist, pip, planAxis, innerLengths } from './planbuild.js';
import { strings } from './strings.js';
import { createStore, emptyDesign } from './core.js';

const BASE = new URL('.', import.meta.url).href;
const FONTS = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&display=swap';
export const PDFJS_VERSION = '4.10.38';
const PDF_LIB = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@' + PDFJS_VERSION + '/build/pdf.min.mjs';
const PDF_WORKER = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@' + PDFJS_VERSION + '/build/pdf.worker.min.mjs';
const KEY = 'nd-myplan', DB = 'nd-myplan', MAXPX = 2400;
const C = { sheet: '#F2F5F7', grid: '#DCE4E9', ink: '#0F2233', ink2: '#46596A', blue: '#1F5FA8', blue2: '#D6E5F6', dim: '#B5302A', rail: '#7F93A3', line: '#B9C6CF' };
const SNAP = 18, LOUPE = 132, ZOOM = 2.6; // snap reach in screen px; the magnifier's size and power
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const clone = (o) => JSON.parse(JSON.stringify(o));
const sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
const add = (a, b) => [a[0] + b[0], a[1] + b[1]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);
const rotv = (v, a) => [v[0] * Math.cos(a) - v[1] * Math.sin(a), v[0] * Math.sin(a) + v[1] * Math.cos(a)];
const wrap90 = (a) => { const q = Math.PI / 2; let r = a % q; if (r > q / 2) r -= q; if (r <= -q / 2) r += q; return r; };

function ensureFonts() {
  if (document.querySelector('link[data-nd-fonts]')) return;
  const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = FONTS; l.setAttribute('data-nd-fonts', ''); document.head.appendChild(l);
}
// ---- what is kept on the device ----
function readStore() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
function writeStore(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); return true; } catch (e) { return false; } }
/** the plan this browser finished last time (onDone), or null */
export function loadMyPlan() {
  const s = readStore();
  return s && s.plan && s.plan.schema === 'nadlan-apartment' && s.plan.v === 1 ? s.plan : null;
}
function idb() {
  return new Promise((res, rej) => {
    if (typeof indexedDB === 'undefined') { rej(new Error('no idb')); return; }
    const r = indexedDB.open(DB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore('img');
    r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
  });
}
async function idbDo(mode, fn) {
  const db = await idb();
  try { return await new Promise((res, rej) => { const tx = db.transaction('img', mode), q = fn(tx.objectStore('img')); tx.oncomplete = () => res(q && q.result); tx.onerror = () => rej(tx.error); }); } finally { db.close(); }
}
const putImage = (blob) => idbDo('readwrite', (s) => s.put(blob, 'photo')).catch(() => null);
const getImage = () => idbDo('readonly', (s) => s.get('photo')).catch(() => null);
const dropImage = () => idbDo('readwrite', (s) => s.delete('photo')).catch(() => null);

// ---- pictures ----
function fitCanvas(src, w, h) { // never more than 2400 px on the long side; white under a transparent picture
  const s = Math.min(1, MAXPX / Math.max(w, h)), c = document.createElement('canvas');
  c.width = Math.max(1, Math.round(w * s)); c.height = Math.max(1, Math.round(h * s));
  const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); x.drawImage(src, 0, 0, c.width, c.height);
  return c;
}
async function blobToCanvas(blob) {
  if (typeof createImageBitmap === 'function') {
    const b = await createImageBitmap(blob); const c = fitCanvas(b, b.width, b.height); if (b.close) b.close(); return c;
  }
  const url = URL.createObjectURL(blob);
  try { const im = new Image(); im.src = url; await im.decode(); return fitCanvas(im, im.naturalWidth, im.naturalHeight); } finally { URL.revokeObjectURL(url); }
}
const toBlob = (c) => new Promise((r) => c.toBlob(r, 'image/jpeg', 0.9));
let pdfLib = null;
async function pdfjs() {
  if (!pdfLib) { pdfLib = await import(/* lazy, only when a PDF is picked */ PDF_LIB); pdfLib.GlobalWorkerOptions.workerSrc = PDF_WORKER; }
  return pdfLib;
}
async function pdfPageCanvas(doc, n) {
  const page = await doc.getPage(n), v1 = page.getViewport({ scale: 1 }), s = Math.min(6, MAXPX / Math.max(v1.width, v1.height)), v = page.getViewport({ scale: s });
  const c = document.createElement('canvas'); c.width = Math.round(v.width); c.height = Math.round(v.height);
  const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height);
  await page.render({ canvasContext: x, viewport: v }).promise;
  return c;
}
// a photo of a page taken at an angle: the four corners the person marks become a straight rectangle
function solve(A, b) {
  const n = b.length, M = A.map((r, i) => [...r, b[i]]);
  for (let i = 0; i < n; i++) {
    let p = i; for (let r = i + 1; r < n; r++) if (Math.abs(M[r][i]) > Math.abs(M[p][i])) p = r;
    [M[i], M[p]] = [M[p], M[i]];
    for (let r = 0; r < n; r++) { if (r === i) continue; const f = M[r][i] / M[i][i]; for (let c = i; c <= n; c++) M[r][c] -= f * M[i][c]; }
  }
  return M.map((r, i) => r[n] / r[i]);
}
function homography(src, dst) {
  const A = [], b = [];
  for (let i = 0; i < 4; i++) { const [x, y] = src[i], [u, v] = dst[i]; A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u); A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v); }
  return [...solve(A, b), 1];
}
const hApply = (H, p) => { const w = H[6] * p[0] + H[7] * p[1] + H[8]; return [(H[0] * p[0] + H[1] * p[1] + H[2]) / w, (H[3] * p[0] + H[4] * p[1] + H[5]) / w]; };
function warp(photo, q) { // q: top-left, top-right, bottom-right, bottom-left, in picture pixels
  let W = Math.max(dist(q[0], q[1]), dist(q[3], q[2])), H = Math.max(dist(q[0], q[3]), dist(q[1], q[2]));
  const s = Math.min(1, MAXPX / Math.max(W, H)); W = Math.max(8, Math.round(W * s)); H = Math.max(8, Math.round(H * s));
  const dst = [[0, 0], [W, 0], [W, H], [0, H]], back = homography(dst, q), fwd = homography(q, dst);
  const sw = photo.width, sh = photo.height, sd = photo.getContext('2d').getImageData(0, 0, sw, sh).data;
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const cx = c.getContext('2d'), out = cx.createImageData(W, H), od = out.data;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const w = back[6] * x + back[7] * y + back[8], u = (back[0] * x + back[1] * y + back[2]) / w, v = (back[3] * x + back[4] * y + back[5]) / w;
    const o = (y * W + x) * 4;
    if (u < 0 || v < 0 || u > sw - 1 || v > sh - 1) { od[o] = od[o + 1] = od[o + 2] = 255; od[o + 3] = 255; continue; }
    const x0 = u | 0, y0 = v | 0, fx = u - x0, fy = v - y0, x1 = Math.min(x0 + 1, sw - 1), y1 = Math.min(y0 + 1, sh - 1);
    for (let k = 0; k < 3; k++) {
      const a = sd[(y0 * sw + x0) * 4 + k], b = sd[(y0 * sw + x1) * 4 + k], cc = sd[(y1 * sw + x0) * 4 + k], d = sd[(y1 * sw + x1) * 4 + k];
      od[o + k] = (a * (1 - fx) + b * fx) * (1 - fy) + (cc * (1 - fx) + d * fx) * fy;
    }
    od[o + 3] = 255;
  }
  cx.putImageData(out, 0, 0);
  return { canvas: c, map: (p) => hApply(fwd, p) };
}

function newDraft(mode) {
  return { schema: 'nadlan-myplan-draft', v: 1, mode, cmPerPx: mode === 'measure' ? 1 : null, scale: null, img: null, axis: mode === 'measure' ? 0 : null,
    nodes: {}, segs: [], openings: [], rooms: [], opacity: 0.6, step: mode === 'measure' ? 'walls' : 'scale' };
}
const okDraft = (d) => d && d.schema === 'nadlan-myplan-draft' && d.v === 1 && d.nodes && Array.isArray(d.segs);

export async function mountPlanMaker(host, opts = {}) {
  const lang = opts.lang || 'he', T = strings(lang), P = T.pm, RTL = T.dir === 'rtl';
  ensureFonts();
  const shadow = host.shadowRoot || host.attachShadow({ mode: 'open' });
  shadow.textContent = '';
  const links = ['designer.css', 'planmaker.css'].map((f) => { const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = BASE + f + '?v=' + (opts.version || '1'); return l; });
  const root = document.createElement('div'); root.className = 'nd pm'; root.dir = T.dir; root.lang = lang;
  const touchy = typeof matchMedia === 'function' && matchMedia('(pointer: coarse)').matches;
  root.innerHTML =
    '<header><div><h2 data-pm="head"></h2><p data-pm="hint"></p></div>' +
    '<button class="pm-hbtn" data-act="save" hidden>' + esc(P.save) + '</button>' +
    '<button class="hb" data-act="close" aria-label="' + esc(P.close) + '" title="' + esc(P.close) + '"><svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 6l12 12M18 6L6 18"/></svg></button></header>' +
    '<ol class="pm-steps" data-pm="steps" aria-label="' + esc(P.stepsLabel) + '" hidden></ol>' +
    '<div class="pm-body" data-pm="body"></div>' +
    '<div class="toast" data-pm="toast" role="status" hidden></div>' +
    '<input type="file" data-pm="file" accept="image/*,application/pdf,.pdf" hidden>' +
    '<input type="file" data-pm="cam" accept="image/*" capture="environment" hidden>' +
    '<input type="file" data-pm="json" accept="application/json,.json" hidden>';
  shadow.append(...links, root);
  await Promise.all(links.map((l) => new Promise((r) => { if (l.sheet) r(); else { l.addEventListener('load', r, { once: true }); l.addEventListener('error', r, { once: true }); } })));
  const $ = (k) => root.querySelector('[data-pm="' + k + '"]');
  root.addEventListener('scroll', () => { if (root.scrollTop || root.scrollLeft) { root.scrollTop = 0; root.scrollLeft = 0; } }, true);

  let draft = null, photo = null, alive = true, toastT = 0, ver = 0, analysis = null, analysisVer = -1;
  let cv = null, ctx = null, loupe = null, lctx = null, stage = null, ro = null, raf = 0, dpr = 1;
  const V = { z: 1, x: 0, y: 0, fit: 1 };
  let tool = 'line', kind = 'facade', otype = 'door', chain = null, rectA = null, pending = null, scaleTmp = null, straight = null;
  let selOpen = null, selFace = null, hover = null, g = null, labelBoxes = [], sureReset = 0, pdfDoc = null, chainStart = null, needFit = false;
  const undo = [], redo = [], ptr = new Map();

  const toast = (msg) => { const t = $('toast'); t.textContent = msg; t.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => (t.hidden = true), 3400); };
  const k = () => (draft && draft.cmPerPx) || 1;
  const ax = () => (draft && typeof draft.axis === 'number' ? draft.axis : 0);
  const toAxis = (v) => rotv(v, -ax()), fromAxis = (v) => rotv(v, ax());
  const toS = (p) => [p[0] * V.z + V.x, p[1] * V.z + V.y];
  const toD = (s) => [(s[0] - V.x) / V.z, (s[1] - V.y) / V.z];
  const cm = (len) => Math.round(len * k());
  const wallPx = (kd) => (draft.cmPerPx ? Math.max(2, ((WALL_T[kd] || 4) / draft.cmPerPx) * V.z) : 3);
  const seg = (id) => draft.segs.find((s) => s.id === id);
  const ends = (s) => [draft.nodes[s.a], draft.nodes[s.b]];

  // ---------- saving ----------
  let saveT = 0;
  const save = () => { clearTimeout(saveT); saveT = setTimeout(saveNow, 120); };
  function saveNow() { if (!alive || !draft) return; const o = readStore() || {}; o.v = 1; o.draft = draft; o.saved = Date.now(); writeStore(o); }
  const snapshot = () => JSON.stringify({ nodes: draft.nodes, segs: draft.segs, openings: draft.openings, rooms: draft.rooms, axis: draft.axis, cmPerPx: draft.cmPerPx, scale: draft.scale });
  function changed() { ver++; save(); panel(); paint(); }
  function tidy() {
    const ids = Object.keys(draft.nodes), idx = new Map(ids.map((id, i) => [id, i]));
    const segs = draft.segs.filter((s) => idx.has(s.a) && idx.has(s.b) && s.a !== s.b).map((s) => ({ a: idx.get(s.a), b: idx.get(s.b), kind: s.kind }));
    const gr = cleanGraph(ids.map((id) => draft.nodes[id]), segs, 0.4 / k());
    const rr = (v) => Math.round(v * 1000) / 1000;
    draft.nodes = {}; gr.pts.forEach((p, i) => (draft.nodes['n' + i] = [rr(p[0]), rr(p[1])]));
    draft.segs = gr.segs.map((s, i) => ({ id: 's' + i, a: 'n' + s.a, b: 'n' + s.b, kind: s.kind }));
    draft.openings = draft.openings.filter((o) => nearSeg(o.p, 30 / k(), null, true));
    if (selOpen && !draft.openings.some((o) => o.id === selOpen)) selOpen = null;
  }
  function commit(fn) {
    const before = snapshot();
    fn(); tidy();
    if (snapshot() !== before) { undo.push(before); if (undo.length > 300) undo.shift(); redo.length = 0; }
    changed();
  }
  const restore = (s) => Object.assign(draft, JSON.parse(s));
  function doUndo() { const s = undo.pop(); if (!s) return; redo.push(snapshot()); restore(s); chain = null; rectA = null; changed(); }
  function doRedo() { const s = redo.pop(); if (!s) return; undo.push(snapshot()); restore(s); chain = null; rectA = null; changed(); }
  const analyze = () => { if (analysisVer !== ver || !analysis) { analysis = analyzeDraft(draft, { project: opts.project || null }); analysisVer = ver; } return analysis; };

  // ---------- geometry helpers ----------
  function nearSeg(p, tol, skip, any) {
    let best = null;
    for (const s of draft.segs) {
      if (skip && skip.has(s.id)) continue;
      const [A, B] = ends(s), r = segDist(p, A, B), L = dist(A, B);
      if (!any && (r.t * L <= tol || (1 - r.t) * L <= tol)) continue; // near an end: that is the corner's business
      if (r.d <= tol && (!best || r.d < best.d)) best = { s, d: r.d, q: r.q, t: r.c, L };
    }
    return best;
  }
  function nodeAt(p, eps) { for (const id in draft.nodes) if (dist(draft.nodes[id], p) <= eps) return id; return null; }
  function addNode(p) { const id = nodeAt(p, 1e-6); if (id) return id; let n = 0; while (draft.nodes['m' + n]) n++; draft.nodes['m' + n] = [p[0], p[1]]; return 'm' + n; }
  function addSeg(a, b, kd) {
    if (dist(a, b) < 1e-6) return;
    if (draft.axis == null) { const v = sub(b, a); draft.axis = wrap90(Math.atan2(v[1], v[0])); }
    draft.segs.push({ id: 'x' + draft.segs.length + '-' + Date.now().toString(36), a: addNode(a), b: addNode(b), kind: kd });
  }
  /** where a finger point lands: on a corner, on a wall (a T), square to the plan's axis from `from`, lined up with corners */
  function snap(p, o = {}) {
    const tol = SNAP / V.z;
    let best = null;
    for (const id in draft.nodes) { if (o.skipNodes && o.skipNodes.has(id)) continue; const d = dist(p, draft.nodes[id]); if (d <= tol && (!best || d < best.d)) best = { d, id }; }
    if (o.extra) for (const q of o.extra) { const d = dist(p, q); if (d <= tol && (!best || d < best.d)) best = { d, q }; }
    if (best) return { p: best.id ? [...draft.nodes[best.id]] : [...best.q], how: 'node' };
    let r = [p[0], p[1]], how = null, line = null;
    const nodesA = Object.entries(draft.nodes).filter(([id]) => !(o.skipNodes && o.skipNodes.has(id))).map(([, q]) => toAxis(q));
    if (o.from) {
      const v = toAxis(sub(p, o.from)), f = toAxis(o.from), t = Math.tan((10 * Math.PI) / 180);
      let free = -1;
      if (Math.abs(v[1]) <= Math.abs(v[0]) * t) { v[1] = 0; free = 0; } else if (Math.abs(v[0]) <= Math.abs(v[1]) * t) { v[0] = 0; free = 1; }
      if (free >= 0) {
        how = 'square';
        const want = f[free] + v[free]; let bestA = null; // line up with a corner across the room
        for (const q of nodesA) { const d = Math.abs(q[free] - want); if (d <= tol && (!bestA || d < bestA.d)) bestA = { d, v: q[free] }; }
        if (bestA) v[free] = bestA.v - f[free];
        r = add(o.from, fromAxis(v)); line = [o.from, r];
      }
    } else if (o.align !== false) {
      const q0 = toAxis(p);
      for (const c of [0, 1]) { let b2 = null; for (const q of nodesA) { const d = Math.abs(q[c] - q0[c]); if (d <= tol && (!b2 || d < b2.d)) b2 = { d, v: q[c] }; } if (b2) { q0[c] = b2.v; how = how || 'align'; } }
      r = fromAxis(q0);
    }
    const w = nearSeg(r, tol, o.skipSegs);
    if (w) {
      const [A, B] = ends(w.s);
      if (line) { // the square line meets the wall: take the meeting point
        const d1 = sub(line[1], line[0]), d2 = sub(B, A), den = d1[0] * d2[1] - d1[1] * d2[0];
        if (Math.abs(den) > 1e-9) { const q = sub(A, line[0]), t = (q[0] * d2[1] - q[1] * d2[0]) / den, x = add(line[0], [d1[0] * t, d1[1] * t]); if (dist(x, r) <= tol * 2) return { p: x, how: 'wall' }; }
      } else return { p: w.q, how: 'wall' };
    }
    if (draft.mode === 'measure' && !how) r = [Math.round(r[0]), Math.round(r[1])];
    return { p: r, how };
  }

  // ---------- the drawing surface ----------
  function fit() {
    if (!stage) return;
    const W = stage.clientWidth, H = stage.clientHeight; if (!W || !H) { needFit = true; return; }
    needFit = false;
    let b;
    if (photo && draft.mode === 'image') b = [0, 0, photo.width, photo.height];
    else {
      const ps = Object.values(draft.nodes);
      b = ps.length ? [Math.min(...ps.map((p) => p[0])), Math.min(...ps.map((p) => p[1])), Math.max(...ps.map((p) => p[0])), Math.max(...ps.map((p) => p[1]))] : [0, 0, 1000 / k(), 800 / k()];
      if (b[2] - b[0] < 300 / k()) { const c = (b[0] + b[2]) / 2; b[0] = c - 400 / k(); b[2] = c + 400 / k(); }
      if (b[3] - b[1] < 300 / k()) { const c = (b[1] + b[3]) / 2; b[1] = c - 300 / k(); b[3] = c + 300 / k(); }
    }
    const m = 24, z = Math.min((W - 2 * m) / (b[2] - b[0]), (H - 2 * m) / (b[3] - b[1]));
    V.z = V.fit = z; V.x = (W - (b[2] - b[0]) * z) / 2 - b[0] * z; V.y = (H - (b[3] - b[1]) * z) / 2 - b[1] * z;
  }
  function resize() {
    if (!cv) return;
    dpr = Math.min(3, window.devicePixelRatio || 1);
    const W = stage.clientWidth, H = stage.clientHeight;
    cv.width = Math.max(1, Math.round(W * dpr)); cv.height = Math.max(1, Math.round(H * dpr));
    loupe.width = loupe.height = Math.round(LOUPE * dpr);
    paint();
  }
  const paint = () => { if (!raf && cv) raf = requestAnimationFrame(draw); };
  function seg2(s) { const [A, B] = ends(s); return { A, B, a: toS(A), b: toS(B), L: dist(A, B) }; }
  function hostOf(o) { const h = nearSeg(o.p, 40 / k(), null, true); return h; }

  function draw() {
    raf = 0; if (!cv || !draft) return;
    const W = cv.width / dpr, H = cv.height / dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = C.sheet; ctx.fillRect(0, 0, W, H);
    ctx.strokeStyle = C.grid; ctx.lineWidth = 1; ctx.beginPath();
    for (let x = ((V.x % 20) + 20) % 20; x < W; x += 20) { ctx.moveTo(Math.round(x) + 0.5, 0); ctx.lineTo(Math.round(x) + 0.5, H); }
    for (let y = ((V.y % 20) + 20) % 20; y < H; y += 20) { ctx.moveTo(0, Math.round(y) + 0.5); ctx.lineTo(W, Math.round(y) + 0.5); }
    ctx.stroke();
    if (photo && draft.mode === 'image') {
      ctx.globalAlpha = straight || draft.step === 'scale' ? 1 : draft.opacity; ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(photo, V.x, V.y, photo.width * V.z, photo.height * V.z); ctx.globalAlpha = 1;
    }
    labelBoxes = [];
    if (straight) drawStraight();
    else {
      if (draft.step === 'rooms') drawFaces();
      drawWalls();
      if (draft.step === 'walls') drawNodes();
      if (draft.step !== 'scale' && draft.step !== 'rooms') drawLabels();
      if (draft.step === 'scale') drawScale();
      drawPreview();
    }
    drawLoupe();
  }
  function drawWalls() {
    const fade = draft.step === 'scale' ? 0.45 : 0.9;
    for (const s of draft.segs) {
      const q = seg2(s);
      ctx.globalAlpha = fade; ctx.lineCap = s.kind === 'divider' ? 'butt' : 'square';
      ctx.strokeStyle = s.kind === 'facade' ? C.ink : s.kind === 'rail' ? C.rail : C.blue;
      ctx.lineWidth = s.kind === 'divider' ? 2.5 : wallPx(s.kind);
      ctx.setLineDash(s.kind === 'divider' ? [9, 7] : []);
      ctx.beginPath(); ctx.moveTo(q.a[0], q.a[1]); ctx.lineTo(q.b[0], q.b[1]); ctx.stroke();
    }
    ctx.setLineDash([]); ctx.globalAlpha = 1;
    // doors and windows: a gap in the wall and the drafting symbol
    for (const o of draft.openings) {
      const h = hostOf(o); if (!h) continue;
      const [A, B] = ends(h.s), d = [(B[0] - A[0]) / h.L, (B[1] - A[1]) / h.L], n = [-d[1], d[0]], half = o.w / k() / 2;
      const p0 = toS([o.p[0] - d[0] * half, o.p[1] - d[1] * half]), p1 = toS([o.p[0] + d[0] * half, o.p[1] + d[1] * half]), wpx = wallPx(h.s.kind);
      ctx.strokeStyle = C.sheet; ctx.lineWidth = wpx + 2; ctx.lineCap = 'butt';
      ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(p1[0], p1[1]); ctx.stroke();
      const on = o.id === selOpen, col = on ? C.blue : C.ink, wpxs = (o.w / k()) * V.z;
      ctx.strokeStyle = col; ctx.lineWidth = on ? 2.5 : 1.6;
      if (o.type === 'door' || o.type === 'entry') {
        const tip = [p0[0] + n[0] * wpxs, p0[1] + n[1] * wpxs];
        ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(tip[0], tip[1]); ctx.stroke();
        const a0 = Math.atan2(p1[1] - p0[1], p1[0] - p0[0]), a1 = Math.atan2(n[1], n[0]);
        ctx.beginPath(); ctx.arc(p0[0], p0[1], wpxs, a0, a1, (a1 - a0 + 2 * Math.PI) % (2 * Math.PI) > Math.PI); ctx.stroke();
      } else if (o.type === 'open') {
        for (const p of [p0, p1]) { ctx.beginPath(); ctx.moveTo(p[0] - n[0] * (wpx / 2 + 3), p[1] - n[1] * (wpx / 2 + 3)); ctx.lineTo(p[0] + n[0] * (wpx / 2 + 3), p[1] + n[1] * (wpx / 2 + 3)); ctx.stroke(); }
      } else {
        ctx.strokeStyle = on ? C.blue : C.blue; ctx.lineWidth = o.type === 'slider' ? 4 : 2;
        for (const sd of o.type === 'slider' ? [0] : [-1, 1]) { const off = sd * Math.min(wpx / 4, 4); ctx.beginPath(); ctx.moveTo(p0[0] + n[0] * off, p0[1] + n[1] * off); ctx.lineTo(p1[0] + n[0] * off, p1[1] + n[1] * off); ctx.stroke(); }
        ctx.strokeStyle = C.ink; ctx.lineWidth = 1.4;
        for (const p of [p0, p1]) { ctx.beginPath(); ctx.moveTo(p[0] - n[0] * wpx / 2, p[1] - n[1] * wpx / 2); ctx.lineTo(p[0] + n[0] * wpx / 2, p[1] + n[1] * wpx / 2); ctx.stroke(); }
      }
      if (on) { ctx.fillStyle = 'rgba(31,95,168,.16)'; ctx.strokeStyle = C.blue; ctx.lineWidth = 2; const r = Math.max(wpx, 14); ctx.beginPath(); ctx.moveTo(p0[0] + n[0] * r, p0[1] + n[1] * r); ctx.lineTo(p1[0] + n[0] * r, p1[1] + n[1] * r); ctx.lineTo(p1[0] - n[0] * r, p1[1] - n[1] * r); ctx.lineTo(p0[0] - n[0] * r, p0[1] - n[1] * r); ctx.closePath(); ctx.fill(); ctx.stroke(); }
    }
  }
  function drawNodes() {
    const deg = {}; for (const s of draft.segs) { deg[s.a] = (deg[s.a] || 0) + 1; deg[s.b] = (deg[s.b] || 0) + 1; }
    for (const id in draft.nodes) {
      const p = toS(draft.nodes[id]);
      if (deg[id] === 1) { ctx.strokeStyle = C.blue; ctx.fillStyle = '#fff'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(p[0], p[1], 6, 0, 7); ctx.fill(); ctx.stroke(); }
      else { ctx.fillStyle = '#fff'; ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5; ctx.fillRect(p[0] - 3.5, p[1] - 3.5, 7, 7); ctx.strokeRect(p[0] - 3.5, p[1] - 3.5, 7, 7); }
    }
  }
  function tag(text, x, y, color, id, force) { // a measurement label: a white box, dimension red, mono
    ctx.font = '600 12px "IBM Plex Mono", monospace';
    const w = ctx.measureText(text).width + 10, h = 20, box = { x0: x - w / 2, y0: y - h / 2, x1: x + w / 2, y1: y + h / 2, id };
    if (!force && labelBoxes.some((b) => box.x0 < b.x1 && b.x0 < box.x1 && box.y0 < b.y1 && b.y0 < box.y1)) return false;
    ctx.fillStyle = '#fff'; ctx.fillRect(box.x0, box.y0, w, h); ctx.strokeStyle = color; ctx.lineWidth = 1; ctx.strokeRect(box.x0 + 0.5, box.y0 + 0.5, w - 1, h - 1);
    ctx.fillStyle = color; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, x, y + 0.5);
    labelBoxes.push(box); return true;
  }
  function drawLabels() {
    if (!draft.cmPerPx) return;
    const IL = innerLengths(draft.nodes, draft.segs, k());
    const list = draft.segs.map((s) => ({ s, q: seg2(s) })).filter((x) => dist(x.q.a, x.q.b) > 46).sort((a, b) => b.q.L - a.q.L);
    for (const { s, q } of list) {
      const m = [(q.a[0] + q.b[0]) / 2, (q.a[1] + q.b[1]) / 2], d = sub(q.b, q.a), L = Math.hypot(d[0], d[1]), n = [-d[1] / L, d[0] / L], off = (s.kind === 'divider' ? 2 : wallPx(s.kind)) / 2 + 17;
      const t = String(Math.round(IL[s.id] ? IL[s.id].inner : q.L * k())); // the inside size, between the wall faces
      if (!tag(t, m[0] + n[0] * off, m[1] + n[1] * off, C.dim, s.id)) tag(t, m[0] - n[0] * off, m[1] - n[1] * off, C.dim, s.id);
    }
  }
  function drawScale() {
    const sc = scaleTmp || draft.scale; if (!sc || !sc.a) return;
    const a = toS(sc.a), b = sc.b ? toS(sc.b) : null;
    ctx.strokeStyle = C.dim; ctx.fillStyle = C.dim; ctx.lineWidth = 2.5;
    for (const p of [a, b]) if (p) { ctx.beginPath(); ctx.arc(p[0], p[1], 5, 0, 7); ctx.fill(); }
    if (b) {
      const d = sub(b, a), L = Math.hypot(d[0], d[1]) || 1, n = [-d[1] / L * 9, d[0] / L * 9];
      ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]);
      for (const p of [a, b]) { ctx.moveTo(p[0] - n[0], p[1] - n[1]); ctx.lineTo(p[0] + n[0], p[1] + n[1]); }
      ctx.stroke();
      const v = sc.cm || (draft.step === 'scale' && $('in-len') && +$('in-len').value) || null;
      if (v) tag(v + ' ' + T.cm, (a[0] + b[0]) / 2 + n[0] * 2.4, (a[1] + b[1]) / 2 + n[1] * 2.4, C.dim, null, true);
    }
  }
  function drawFaces() {
    const a = analyze(), choices = roomChoices(lang);
    a.faces.forEach((f, i) => {
      const ps = f.poly.map(toS);
      ctx.beginPath(); ps.forEach((p, j) => (j ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.closePath();
      const on = selFace === i, named = f.key && f.key !== 'out';
      ctx.fillStyle = on ? C.blue2 : f.key === 'out' ? 'rgba(70,89,106,.22)' : named ? 'rgba(214,229,246,.72)' : 'rgba(255,255,255,.78)';
      ctx.fill();
      if (on || !f.key) { ctx.strokeStyle = C.blue; ctx.lineWidth = on ? 3 : 1.5; ctx.setLineDash(on ? [] : [7, 6]); ctx.stroke(); ctx.setLineDash([]); }
    });
    a.faces.forEach((f) => {
      const p = toS(f.at), ch = f.key && choices.find((c) => c.key === f.key);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.font = '700 14px "IBM Plex Sans Hebrew", Arial, sans-serif';
      const name = ch ? ch.label : P.roomAsk;
      ctx.lineWidth = 4; ctx.strokeStyle = 'rgba(242,245,247,.95)'; ctx.strokeText(name, p[0], p[1] - 9);
      ctx.fillStyle = ch ? C.ink : C.blue; ctx.fillText(name, p[0], p[1] - 9);
      if (f.key !== 'out') { ctx.font = '600 12px "IBM Plex Mono", monospace'; const t = f.net.toFixed(1) + ' ' + T.sqm; ctx.strokeText(t, p[0], p[1] + 10); ctx.fillStyle = C.ink2; ctx.fillText(t, p[0], p[1] + 10); }
    });
  }
  function drawStraight() {
    const q = straight.map(toS);
    ctx.strokeStyle = C.blue; ctx.lineWidth = 2; ctx.setLineDash([8, 6]);
    ctx.beginPath(); q.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.closePath(); ctx.stroke(); ctx.setLineDash([]);
    for (const p of q) { ctx.fillStyle = 'rgba(31,95,168,.18)'; ctx.beginPath(); ctx.arc(p[0], p[1], 22, 0, 7); ctx.fill(); ctx.fillStyle = '#fff'; ctx.strokeStyle = C.blue; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(p[0], p[1], 9, 0, 7); ctx.fill(); ctx.stroke(); }
  }
  function marker(p, how) {
    const s = toS(p);
    ctx.strokeStyle = C.blue; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(s[0], s[1], how === 'node' ? 9 : 7, 0, 7); ctx.stroke();
    if (how === 'wall') { ctx.beginPath(); ctx.moveTo(s[0] - 12, s[1]); ctx.lineTo(s[0] + 12, s[1]); ctx.moveTo(s[0], s[1] - 12); ctx.lineTo(s[0], s[1] + 12); ctx.stroke(); }
  }
  function rectCorners(a, b) { const qa = toAxis(a), qb = toAxis(b); return [[qa[0], qa[1]], [qb[0], qa[1]], [qb[0], qb[1]], [qa[0], qb[1]]].map(fromAxis); }
  function pendingCorners(at) { // the typed room, its top corner at the finger (top-right on a right-to-left page)
    const q = toAxis(at), x0 = RTL ? q[0] - pending.w : q[0];
    return [[x0, q[1]], [x0 + pending.w, q[1]], [x0 + pending.w, q[1] + pending.d], [x0, q[1] + pending.d]].map(fromAxis);
  }
  function poly(ps, dashed) {
    const q = ps.map(toS); ctx.strokeStyle = C.blue; ctx.lineWidth = 2.5; ctx.setLineDash(dashed ? [10, 7] : []);
    ctx.beginPath(); q.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.closePath(); ctx.stroke(); ctx.setLineDash([]);
  }
  function drawPreview() {
    const cur = g && g.kind === 'pick' ? g.cur : hover;
    if (draft.step === 'walls') {
      if (tool === 'line' && chain) {
        const a = toS(chain); ctx.fillStyle = C.blue; ctx.beginPath(); ctx.arc(a[0], a[1], 5, 0, 7); ctx.fill();
        if (cur) { const b = toS(cur.p); ctx.strokeStyle = C.blue; ctx.lineWidth = 3; ctx.setLineDash([10, 7]); ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); ctx.setLineDash([]);
          if (draft.cmPerPx && dist(a, b) > 30) tag(String(cm(dist(chain, cur.p))), (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 16, C.dim, null, true); }
      }
      if (tool === 'rect' && rectA) { const b = cur ? cur.p : rectA; poly(rectCorners(rectA, b), true); if (cur && draft.cmPerPx) { const q = sub(toAxis(b), toAxis(rectA)); const s = toS(b); tag(Math.abs(cm(q[0])) + ' × ' + Math.abs(cm(q[1])), s[0], s[1] - 26, C.dim, null, true); } }
      if (tool === 'rect' && pending && cur) poly(pendingCorners(cur.p), true);
    }
    if (draft.step === 'scale' && cur && !straight) { const s = toS(cur.p); ctx.strokeStyle = C.dim; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(s[0], s[1], 7, 0, 7); ctx.stroke(); }
    else if (cur && draft.step !== 'rooms') marker(cur.p, cur.how);
  }
  function drawLoupe() {
    if (!loupe) return;
    const show = g && g.touch && g.loupe;
    loupe.hidden = !show; if (!show) return;
    const c = toS(g.loupe), W = stage.clientWidth, H = stage.clientHeight, r = LOUPE / 2;
    let lx = g.s[0], ly = g.s[1] - r - 46; // above the finger
    if (ly - r < 4) { ly = g.s[1]; lx = g.s[0] + (g.s[0] > W / 2 ? -1 : 1) * (r + 46); } // too near the top: beside it
    lx = Math.max(r + 4, Math.min(W - r - 4, lx)); ly = Math.max(r + 4, Math.min(H - r - 4, ly));
    loupe.style.transform = 'translate(' + (lx - r) + 'px,' + (ly - r) + 'px)';
    const sz = (LOUPE * dpr) / ZOOM;
    lctx.setTransform(1, 0, 0, 1, 0, 0); lctx.fillStyle = C.sheet; lctx.fillRect(0, 0, loupe.width, loupe.height);
    lctx.imageSmoothingEnabled = false;
    lctx.drawImage(cv, c[0] * dpr - sz / 2, c[1] * dpr - sz / 2, sz, sz, 0, 0, loupe.width, loupe.height);
    lctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    lctx.strokeStyle = C.dim; lctx.lineWidth = 1.5; lctx.beginPath(); lctx.moveTo(r, 8); lctx.lineTo(r, r - 6); lctx.moveTo(r, r + 6); lctx.lineTo(r, LOUPE - 8); lctx.moveTo(8, r); lctx.lineTo(r - 6, r); lctx.moveTo(r + 6, r); lctx.lineTo(LOUPE - 8, r); lctx.stroke();
    lctx.fillStyle = C.dim; lctx.beginPath(); lctx.arc(r, r, 2, 0, 7); lctx.fill();
  }

  // ---------- touch, pen and mouse ----------
  const local = (e) => { const r = cv.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  function pickPoint(p) { // what a finger at p would set, per step and tool
    const st = draft.step;
    if (st === 'walls' && tool === 'line') return snap(p, { from: chain });
    if (st === 'walls' && tool === 'rect') return pending ? { p, how: null } : snap(p, rectA ? { from: rectA } : {});
    if (st === 'open') { const h = nearSeg(p, (SNAP * 1.6) / V.z, null, true); return h ? { p: h.q, how: 'wall', h } : { p, how: null }; }
    return { p, how: null };
  }
  function hitLabel(s, strict) { // strict (while drawing walls): only right on the label, never on the wall line beside it
    const m = strict ? 0 : 4, b = labelBoxes.find((x) => x.id && s[0] >= x.x0 - m && s[0] <= x.x1 + m && s[1] >= x.y0 - m && s[1] <= x.y1 + m) || null;
    if (b && strict) { const p = toD(s), w = nearSeg(p, 12 / V.z, null, true); if (w) return null; }
    return b;
  }
  function hitOpening(p) {
    for (const o of draft.openings) { const h = hostOf(o); if (!h) continue; const [A, B] = ends(h.s), d = [(B[0] - A[0]) / h.L, (B[1] - A[1]) / h.L], v = sub(p, o.p), along = Math.abs(dot(v, d)), across = Math.abs(v[0] * d[1] - v[1] * d[0]); if (along <= o.w / k() / 2 + 4 / V.z && across <= (SNAP + 4) / V.z) return { o, h, d }; }
    return null;
  }
  function startGesture(s, touch) {
    const p = toD(s), st = draft.step;
    if (straight) {
      const i = straight.findIndex((q) => dist(toS(q), s) <= 30);
      return i >= 0 ? { kind: 'corner', i, touch, s, loupe: straight[i] } : { kind: 'pan', s, v0: { ...V } };
    }
    if (st === 'walls' && (tool === 'move' || (tool === 'line' && !chain))) {
      const lb = hitLabel(s, tool === 'line'); if (lb) return { kind: 'label', id: lb.id, s, touch };
    }
    if (st === 'walls' && tool === 'move') {
      const tol = SNAP / V.z;
      let nid = null, nd = Infinity; for (const id in draft.nodes) { const d = dist(draft.nodes[id], p); if (d <= tol * 1.3 && d < nd) { nd = d; nid = id; } }
      const carry = draft.openings.map((o) => { const h = hostOf(o); return h ? { o, a: h.s.a, b: h.s.b, t: h.t } : null; }).filter(Boolean);
      if (nid) { const segs = draft.segs.filter((x) => x.a === nid || x.b === nid); return { kind: 'node', id: nid, before: snapshot(), touch, s, carry, loupe: draft.nodes[nid], from: segs.length ? draft.nodes[segs[0].a === nid ? segs[0].b : segs[0].a] : null, skipSegs: new Set(segs.map((x) => x.id)) }; }
      const w = nearSeg(p, tol * 1.3, null, true);
      if (w) { const [A, B] = ends(w.s), d = sub(B, A), L = Math.hypot(d[0], d[1]); return { kind: 'seg', id: w.s.id, before: snapshot(), touch, s, p0: p, n: [-d[1] / L, d[0] / L], A: [...A], B: [...B], carry }; }
      return touch ? null : { kind: 'pan', s, v0: { ...V } };
    }
    if (st === 'open') {
      const hit = hitOpening(p);
      if (hit) { selOpen = hit.o.id; panel(); return { kind: 'open', id: hit.o.id, before: snapshot(), touch, s, loupe: hit.o.p }; }
    }
    const c = pickPoint(p);
    return { kind: 'pick', s, s0: s, p, cur: c, loupe: c.p, touch, moved: false };
  }
  function moveGesture(s) {
    if (!g) return;
    const p = toD(s);
    if (g.kind === 'pan') { V.x = g.v0.x + s[0] - g.s[0]; V.y = g.v0.y + s[1] - g.s[1]; paint(); return; }
    if (g.kind === 'pick') {
      if (!g.touch && dist(s, g.s0) > 6) { g = { kind: 'pan', s: g.s0, v0: { ...V } }; moveGesture(s); return; }
      g.s = s; g.cur = pickPoint(p); g.loupe = g.cur.p; paint(); return;
    }
    if (g.kind === 'label') { if (dist(s, g.s) > 8) g = { kind: 'pan', s: g.s, v0: { ...V }, dead: g.touch }; return; }
    g.s = s;
    if (g.kind === 'corner') { straight[g.i] = [Math.max(0, Math.min(photo.width, p[0])), Math.max(0, Math.min(photo.height, p[1]))]; g.loupe = straight[g.i]; paint(); return; }
    if (g.kind === 'node') {
      const r = snap(p, { skipNodes: new Set([g.id]), skipSegs: g.skipSegs, from: g.from });
      draft.nodes[g.id] = r.p; g.loupe = r.p; g.how = r.how;
    }
    if (g.kind === 'seg') {
      const s0 = seg(g.id); if (!s0) return;
      const t = dot(sub(p, g.p0), g.n);
      draft.nodes[s0.a] = add(g.A, [g.n[0] * t, g.n[1] * t]); draft.nodes[s0.b] = add(g.B, [g.n[0] * t, g.n[1] * t]);
    }
    if (g.kind === 'open') {
      const o = draft.openings.find((x) => x.id === g.id), h = o && hostOf(o); if (!h) return;
      const [A, B] = ends(h.s), r = segDist(p, A, B), half = o.w / k() / 2, L = h.L, t = Math.max(Math.min(half / L, 0.5), Math.min(1 - Math.min(half / L, 0.5), r.t));
      o.p = [A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]; g.loupe = o.p;
    }
    if (g.carry) for (const c of g.carry) { const A = draft.nodes[c.a], B = draft.nodes[c.b]; if (A && B) c.o.p = [A[0] + (B[0] - A[0]) * c.t, A[1] + (B[1] - A[1]) * c.t]; }
    ver++; paint();
  }
  function endGesture(s, cancel) {
    const G = g; g = null;
    if (!G) { paint(); return; }
    if (G.kind === 'pick' && !cancel) act(G.cur);
    else if (G.kind === 'label' && !cancel) editLength(G.id);
    else if ((G.kind === 'node' || G.kind === 'seg' || G.kind === 'open') && G.before) {
      if (cancel) { restore(G.before); changed(); }
      else { const after = snapshot(); tidy(); if (snapshot() !== G.before) { undo.push(G.before); redo.length = 0; } void after; changed(); }
    } else if (G.kind === 'corner') paint();
    paint();
  }
  function act(c) {
    const st = draft.step, p = c.p;
    if (st === 'scale') {
      if (!scaleTmp || scaleTmp.b) scaleTmp = { a: p, b: null }; else scaleTmp.b = p;
      panel(); paint(); if (scaleTmp.b) { const i = $('in-len'); if (i && !touchy) i.focus(); }
      return;
    }
    if (st === 'walls') {
      if (tool === 'line') {
        if (!chain) { chain = p; chainStart = p; paint(); panel(); return; }
        if (dist(p, chain) * V.z < 4) return;
        const a = chain, closes = chainStart && dist(p, chainStart) < 1e-6;
        commit(() => addSeg(a, p, kind));
        chain = closes ? null : p; if (closes) chainStart = null;
        panel(); paint(); return;
      }
      if (tool === 'rect') {
        if (pending) { placePending(p); return; }
        if (!rectA) { rectA = p; paint(); return; }
        const q = rectCorners(rectA, p); rectA = null;
        if (dist(q[0], q[2]) * V.z < 8) { paint(); return; }
        commit(() => q.forEach((x, i) => addSeg(x, q[(i + 1) % 4], kind)));
        return;
      }
      if (tool === 'del') { delAt(p); return; }
    }
    if (st === 'open') {
      if (!c.h) { toast(P.openNoWall); return; }
      if (c.h.s.kind === 'rail' || c.h.s.kind === 'divider') { toast(P.openRail); return; }
      const spec = OPEN_TYPES[otype], Lcm = c.h.L * k();
      let w = Math.min(spec.w, Math.max(30, Math.round(Lcm - 10)));
      const half = w / k() / 2, [A, B] = ends(c.h.s), t = Math.max(half / c.h.L, Math.min(1 - half / c.h.L, c.h.t));
      const id = 'o' + Date.now().toString(36) + (draft.openings.length);
      commit(() => draft.openings.push({ id, p: [A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t], w, type: otype }));
      selOpen = id; panel(); paint(); return;
    }
    if (st === 'rooms') {
      const a = analyze(); let best = -1, ba = Infinity;
      a.faces.forEach((f, i) => { if (pip(p, f.poly)) { const ar = Math.abs(f.gross); if (ar < ba) { ba = ar; best = i; } } });
      selFace = best >= 0 ? best : null;
      if (selFace != null) { // keep the room in sight above the names sheet
        const s = toS(a.faces[selFace].at), H = stage.clientHeight, top = H * 0.36;
        if (s[1] > top) V.y -= s[1] - top * 0.7;
      }
      panel(); paint(); return;
    }
  }
  function placePending(at) {
    let cs = pendingCorners(at);
    let best = null; const tol = (SNAP * 1.5) / V.z;
    for (const c of cs) for (const id in draft.nodes) { const d = dist(c, draft.nodes[id]); if (d <= tol && (!best || d < best.d)) best = { d, v: sub(draft.nodes[id], c) }; }
    if (best) cs = cs.map((c) => add(c, best.v));
    commit(() => cs.forEach((x, i) => addSeg(x, cs[(i + 1) % 4], kind)));
    pending = null;
    fit(); // the whole drawing in sight
    panel(); paint();
  }
  function addTypedRoom(Wcm, Dcm) {
    const t = WALL_T[kind] || 0;
    pending = { w: (Wcm + t) / k(), d: (Dcm + t) / k() };
    if (!draft.segs.length) { // the first room goes to the top corner of the sheet; the next ones where the person taps
      placePending(fromAxis(RTL ? [pending.w, 0] : [0, 0])); fit(); paint(); return;
    }
    hover = null; panel(); paint();
  }
  function delAt(p) {
    const hit = hitOpening(p);
    if (hit) { commit(() => (draft.openings = draft.openings.filter((o) => o !== hit.o))); return; }
    const w = nearSeg(p, (SNAP * 1.2) / V.z, null, true);
    if (w) commit(() => { draft.segs = draft.segs.filter((s) => s !== w.s); const used = new Set(draft.segs.flatMap((s) => [s.a, s.b])); for (const id of Object.keys(draft.nodes)) if (!used.has(id)) delete draft.nodes[id]; });
  }
  function setLength(id, inner) { // the number typed is the inside size; the wall's centre line is that plus the half walls at its ends
    const s = seg(id); if (!s || !(inner > 0)) return;
    const il = innerLengths(draft.nodes, draft.segs, k())[id], want = inner + (il ? il.ta + il.tb : 0);
    const [A, B] = ends(s), L = dist(A, B), d = want / k() - L; if (!L || Math.abs(d) < 1e-9) return;
    const dir = [(B[0] - A[0]) / L, (B[1] - A[1]) / L], q = toAxis(dir), straightW = Math.abs(q[0]) < 1e-3 || Math.abs(q[1]) < 1e-3;
    commit(() => {
      if (straightW) { // everything beyond the far end moves with it, so square rooms stay square
        const lim = dot(sub(B, A), dir) - 1e-6, mv = (p) => (dot(sub(p, A), dir) >= lim ? add(p, [dir[0] * d, dir[1] * d]) : p);
        for (const nid in draft.nodes) draft.nodes[nid] = mv(draft.nodes[nid]);
        for (const o of draft.openings) o.p = mv(o.p);
        for (const r of draft.rooms) r.at = mv(r.at);
      } else draft.nodes[s.b] = add(B, [dir[0] * d, dir[1] * d]);
    });
  }
  function editLength(id) {
    const s = seg(id); if (!s) return;
    const box = labelBoxes.find((b) => b.id === id), ed = $('edit');
    ed.hidden = false; ed.dataset.seg = id;
    const W = stage.clientWidth, x = box ? (box.x0 + box.x1) / 2 : W / 2, y = box ? box.y1 + 6 : 10;
    ed.style.left = Math.max(4, Math.min(W - 228, x - 112)) + 'px'; ed.style.top = Math.max(4, Math.min(stage.clientHeight - 60, y)) + 'px';
    const il = innerLengths(draft.nodes, draft.segs, k())[id], i = ed.querySelector('input'); i.value = Math.round(il ? il.inner : cm(dist(...ends(s)))); i.focus(); i.select();
  }

  // ---------- the screens ----------
  const btn = (act, label, extra = '') => '<button data-act="' + act + '" ' + extra + '>' + esc(label) + '</button>';
  const field = (id, label, val) => '<label class="pm-field"><span>' + esc(label) + '</span><input data-pm="' + id + '" type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" value="' + (val == null ? '' : esc(val)) + '"></label>';
  function steps() {
    const ol = $('steps'), list = draft && draft.mode === 'measure' ? ['walls', 'open', 'rooms'] : ['scale', 'walls', 'open', 'rooms'], idx = { scale: 0, walls: 1, open: 2, rooms: 3 };
    ol.hidden = !draft || draft.step === 'start';
    if (ol.hidden) return;
    ol.innerHTML = list.map((st, i) => '<li><button data-act="go" data-step="' + st + '" aria-current="' + (draft.step === st ? 'step' : 'false') + '"><b class="mono">' + (i + 1) + '</b><span>' + esc(P.steps[idx[st]]) + '</span></button></li>').join('');
  }
  function headText() {
    const st = draft ? draft.step : 'start';
    const h = { start: [P.title, ''], scale: [P.scaleHead, straight ? P.straightHint : P.scaleHint], walls: [P.wallsHead, tool === 'rect' ? (pending ? P.rectPlace : !draft.segs.length && draft.mode === 'measure' ? P.rectFirst : P.rectHint) : tool === 'move' ? P.moveHint : tool === 'del' ? P.delHint : P.wallsHint], open: [P.openHead, P.openHint], rooms: [P.roomsHead, P.roomsHint] }[st];
    $('head').textContent = h[0]; $('hint').textContent = h[1]; $('hint').hidden = !h[1];
    root.querySelector('[data-act="save"]').hidden = !draft || st === 'start';
  }
  function startScreen() {
    const st = readStore(), saved = st && okDraft(st.draft) && st.draft.segs.length ? st.draft : null;
    $('body').innerHTML = '<div class="pm-start"><div class="pm-sheet-in">' +
      '<h3 class="pm-h">' + esc(P.startHead) + '</h3><p class="pm-lead">' + esc(P.startLine) + '</p>' +
      (saved ? '<section class="pm-opt pm-resume"><b class="pm-n mono">0</b><div><h4>' + esc(P.resume) + '</h4><p>' + esc(P.resumeSub(saved.segs.length)) + '</p><div class="pm-row">' + btn('resume', P.resume, 'class="pm-go"') + '</div></div></section>' : '') +
      '<section class="pm-opt"><b class="pm-n mono">1</b><div><h4>' + esc(P.optHave) + '</h4><p>' + esc(P.optHaveSub) + '</p><div class="pm-row">' + btn('pick', P.pickFile, 'class="pm-go"') + (touchy ? btn('camera', P.camera) : '') + '</div></div></section>' +
      '<section class="pm-opt"><b class="pm-n mono">2</b><div><h4>' + esc(P.optNone) + '</h4><p>' + esc(P.optNoneSub) + '</p><div class="pm-row">' + btn('measure', P.byMeasure) + '</div></div></section>' +
      '<section class="pm-opt"><b class="pm-n mono">3</b><div><h4>' + esc(P.optSaved) + '</h4><p>' + esc(P.optSavedSub) + '</p><div class="pm-row">' + btn('loadfile', P.loadFile) + '</div></div></section>' +
      '<p class="pm-privacy">' + esc(P.privacy) + '</p>' +
      (opts.helpUrl ? '<a class="pm-help" href="' + esc(opts.helpUrl) + '" target="_blank" rel="noopener">' + esc(P.help) + '</a>' : '') +
      '</div></div>';
  }
  function workArea() {
    if (stage && stage.isConnected) return;
    $('body').innerHTML = '<div class="pm-work"><div class="pm-stage" data-pm="stage"><canvas data-pm="cv" aria-label="' + esc(P.title) + '"></canvas><canvas class="pm-loupe" data-pm="loupe" hidden aria-hidden="true"></canvas>' +
      '<form class="pm-edit" data-pm="edit" hidden><label><span>' + esc(P.lenEdit) + '</span><input type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off"></label><button type="submit">' + esc(P.lenSet) + '</button></form>' +
      '<div class="pm-names" data-pm="names" hidden></div></div><div class="pm-panel" data-pm="panel"></div></div>';
    stage = $('stage'); cv = $('cv'); ctx = cv.getContext('2d'); loupe = $('loupe'); lctx = loupe.getContext('2d');
    bindStage();
    if (ro) ro.disconnect();
    ro = new ResizeObserver(() => { resize(); if (needFit) fit(); paint(); });
    ro.observe(stage);
  }
  function panel() {
    headText(); steps();
    const el = $('panel'); if (!el || !draft) return;
    const st = draft.step; let h = '';
    const ur = '<div class="pm-row pm-ur">' + btn('undo', P.undo, undo.length ? '' : 'disabled') + btn('redo', P.redo, redo.length ? '' : 'disabled') + (st === 'walls' ? btn('endline', P.endLine, chain || rectA || pending ? '' : 'disabled') : '') + '</div>';
    const opa = photo && draft.mode === 'image' ? '<label class="pm-range"><span>' + esc(P.opacity) + '</span><input type="range" data-pm="opa" min="10" max="100" value="' + Math.round(draft.opacity * 100) + '"></label>' : '';
    if (st === 'scale') {
      h += photo ? '<div class="pm-row">' + btn('rotate', P.rotate) + btn('straight', straight ? P.straightCancel : P.straight, 'aria-pressed="' + !!straight + '"') + '</div>' : '';
      if (straight) h += '<button class="pm-go" data-act="straight-apply">' + esc(P.straightApply) + '</button>';
      else {
        const v = scaleTmp && scaleTmp.cm ? scaleTmp.cm : draft.scale && !scaleTmp ? draft.scale.cm : '';
        h += '<div class="pm-row pm-scale">' + field('in-len', P.lenCm, v) + '<div class="pm-door"><small>' + esc(P.doorHint) + '</small><div class="pm-row">' + [70, 80, 90].map((v) => btn('door', String(v), 'data-v="' + v + '" aria-pressed="' + !!(scaleTmp && scaleTmp.door === v) + '"')).join('') + '</div></div></div>';
        h += '<button class="pm-go" data-act="scale-ok">' + esc(P.scaleOk) + '</button>';
      }
    }
    if (st === 'walls') {
      h += '<div class="pm-seg" role="group" aria-label="' + esc(P.toolsLabel) + '">' + [['line', P.tLine], ['rect', P.tRect], ['move', P.tMove], ['del', P.tDel]].map(([t, l]) => btn('tool', l, 'data-v="' + t + '" aria-pressed="' + (tool === t) + '"')).join('') + '</div>';
      h += '<div class="pm-seg pm-kinds" role="group" aria-label="' + esc(P.kindsLabel) + '">' + DRAW_KINDS.map((kd) => '<button data-act="kind" data-v="' + kd + '" aria-pressed="' + (kind === kd) + '"><i class="pm-sw ' + kd + '"></i><span>' + esc(P.kinds[kd]) + '</span></button>').join('') + '</div>';
      if (tool === 'rect') h += '<div class="pm-row pm-dims">' + field('in-w', P.rectW, '') + field('in-d', P.rectD, '') + btn('rect-add', P.rectAdd) + '</div>';
      h += ur + opa;
      h += '<button class="pm-go" data-act="go" data-step="open">' + esc(P.next) + '</button>';
    }
    if (st === 'open') {
      h += '<div class="pm-seg pm-otypes" role="group" aria-label="' + esc(P.openLabel) + '">' + Object.keys(OPEN_TYPES).map((t) => btn('otype', P.ot[t], 'data-v="' + t + '" aria-pressed="' + (otype === t) + '"')).join('') + '</div>';
      const o = selOpen && draft.openings.find((x) => x.id === selOpen);
      if (o) h += '<div class="pm-row pm-sel"><b>' + esc(P.ot[o.type]) + '</b>' + field('in-ow', P.widthCm, Math.round(o.w)) + btn('open-del', P.remove) + '</div>';
      h += ur + opa + '<button class="pm-go" data-act="go" data-step="rooms">' + esc(P.next) + '</button>';
    }
    if (st === 'rooms') {
      const a = analyze();
      if (!a.faces.length) h += '<p class="pm-msg">' + esc(P.roomsNone) + '</p>';
      else {
        const inside = a.faces.filter((f) => f.key !== 'out' && f.type !== 'balcony'), bal = a.faces.filter((f) => f.type === 'balcony');
        const net = inside.reduce((m, f) => m + f.net, 0), b = bal.reduce((m, f) => m + f.net, 0);
        const allNamed = !a.problems.some((x) => x.code === 'room.noname');
        h += '<p class="pm-sum" data-pm="sum"><b>' + esc(allNamed && a.plan ? P.sum(a.plan.unit.rooms, net.toFixed(1), b ? b.toFixed(1) : '') : P.spaces(a.faces.filter((f) => f.key !== 'out').length, (net + b).toFixed(1))) + '</b></p>';
      }
      const probs = a.problems;
      if (probs.length) h += '<ul class="pm-probs" data-pm="probs">' + probs.map((x) => { const f = P.problems[x.code]; return '<li>' + esc(typeof f === 'function' ? f(x.n || 1) : f || x.code) + '</li>'; }).join('') + '</ul>';
      if (draft.scale && draft.scale.door) h += '<p class="pm-msg" data-pm="bydoor">' + esc(P.byDoor) + '</p>';
      h += (draft.mode === 'image' ? '<p class="pm-fine">' + esc(P.areaOff) + '</p>' : '') + '<p class="pm-fine" data-pm="note">' + esc(P.note) + '</p>';
      h += opa + '<button class="pm-go" data-act="done"' + (a.plan ? '' : ' disabled') + '>' + esc(P.open3d) + '</button>';
    }
    h += '<button class="pm-reset" data-act="reset">' + esc(sureReset > Date.now() ? P.startOverSure : P.startOver) + '</button>';
    el.innerHTML = h;
    names();
  }
  function names() {
    const box = $('names'); if (!box) return;
    const under = (on) => { const pn = $('panel'); if (pn) pn.classList.toggle('pm-under', on); };
    if (!draft || draft.step !== 'rooms' || selFace == null) { box.hidden = true; under(false); return; }
    const f = analyze().faces[selFace]; if (!f) { box.hidden = true; selFace = null; return; }
    box.hidden = false; under(true);
    box.innerHTML = '<div class="pm-names-h"><h3>' + esc(P.roomPick) + (f.key === 'out' ? '' : ' <span class="mono">' + f.net.toFixed(1) + '</span> ' + esc(T.sqm)) + '</h3>' + btn('names-x', '', 'class="hb" aria-label="' + esc(P.close) + '"') + '</div><div class="pm-grid">' +
      roomChoices(lang).map((c) => btn('name', c.label, 'data-v="' + c.key + '" aria-pressed="' + (f.key === c.key) + '"' + (c.key === 'out' ? ' class="pm-out"' : ''))).join('') + '</div>';
    box.querySelector('[data-act="names-x"]').innerHTML = '<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  }
  function screen() {
    if (!draft || draft.step === 'start') { stage = null; cv = null; if (ro) { ro.disconnect(); ro = null; } startScreen(); headText(); steps(); return; }
    workArea(); panel(); paint();
  }
  function go(st) {
    if (!draft) return;
    if (st !== 'scale' && draft.mode === 'image' && !draft.cmPerPx) { toast(P.scaleFirst); st = 'scale'; }
    chain = null; rectA = null; pending = null; straight = null; selFace = null; selOpen = null; hover = null; $('edit') && ($('edit').hidden = true);
    if (st === 'scale') scaleTmp = draft.scale ? { ...draft.scale } : null;
    draft.step = st; save(); screen(); fit(); paint(); // the whole drawing in sight on every step
  }

  // ---------- loading a plan ----------
  async function usePhoto(c, keepDraft) {
    photo = c;
    if (!keepDraft) { draft = newDraft('image'); undo.length = redo.length = 0; }
    draft.img = { w: c.width, h: c.height };
    toBlob(c).then((b) => b && putImage(b));
    draft.step = 'scale'; scaleTmp = null; saveNow(); screen(); fit(); paint();
  }
  async function openFile(file) {
    if (!file) return;
    $('body').innerHTML = '<p class="pm-wait">' + esc(P.loading) + '</p>';
    const isPdf = /pdf$/i.test(file.type) || /\.pdf$/i.test(file.name || '');
    try {
      if (!isPdf) { await usePhoto(await blobToCanvas(file)); return; }
      const lib = await pdfjs();
      pdfDoc = await lib.getDocument({ data: new Uint8Array(await file.arrayBuffer()) }).promise;
      if (pdfDoc.numPages === 1) { await usePhoto(await pdfPageCanvas(pdfDoc, 1)); return; }
      $('body').innerHTML = '<div class="pm-start"><div class="pm-sheet-in"><h3 class="pm-h">' + esc(P.pdfPage) + '</h3><div class="pm-grid pm-pages">' +
        Array.from({ length: Math.min(pdfDoc.numPages, 40) }, (_, i) => btn('page', P.page(i + 1), 'data-v="' + (i + 1) + '"')).join('') + '</div></div></div>';
    } catch (e) { toast(P.pdfFail); draft = null; screen(); }
  }
  async function openSaved(file) {
    try {
      const o = JSON.parse(await file.text());
      if (o && o.schema === 'nadlan-apartment' && o.v === 1) { // a finished plan saved from the designer: it must open in the engine before it replaces anything
        createStore(o, emptyDesign(o)); // throws on a file that is not a plan the engine can open: the catch below says so
        if (opts.onDone) opts.onDone(o, null); return;
      }
      if (!o || o.schema !== 'nadlan-myplan' || !okDraft(o.draft)) throw new Error('bad');
      draft = o.draft; photo = null; dropImage(); undo.length = redo.length = 0; ver++;
      draft.step = analyzeDraft(draft).faces.length ? 'rooms' : draft.mode === 'image' && !draft.cmPerPx ? 'scale' : 'walls';
      saveNow(); screen(); fit(); paint();
    } catch (e) { toast(P.fileBad); }
  }
  function saveFile() {
    if (!draft) return;
    const a0 = analyze(), data = { schema: 'nadlan-myplan', v: 1, saved: new Date().toISOString(), draft: clone(draft), plan: a0.plan || null };
    const blob = new Blob([JSON.stringify(data, null, 1)], { type: 'application/json' }), url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'my-plan-' + new Date().toISOString().slice(0, 10) + '.json'; a.hidden = true;
    root.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 4000);
    toast(P.saved);
  }
  function rotatePhoto() { // 90 degrees clockwise: the picture and everything drawn on it
    if (!photo) return;
    const c = document.createElement('canvas'); c.width = photo.height; c.height = photo.width;
    const x = c.getContext('2d'); x.translate(c.width, 0); x.rotate(Math.PI / 2); x.drawImage(photo, 0, 0);
    const H = photo.height, f = (p) => [H - p[1], p[0]];
    transformDraft(f); if (draft.axis != null) draft.axis = wrap90(draft.axis + Math.PI / 2);
    usePhoto(c, true);
  }
  function transformDraft(f) {
    for (const id in draft.nodes) draft.nodes[id] = f(draft.nodes[id]);
    for (const o of draft.openings) o.p = f(o.p);
    for (const r of draft.rooms) r.at = f(r.at);
    if (draft.scale) { draft.scale.a = f(draft.scale.a); draft.scale.b = f(draft.scale.b); }
    undo.length = redo.length = 0; ver++;
  }
  function applyStraight() {
    if (!straight || !photo) return;
    const q = straight.slice(), w = warp(photo, q);
    transformDraft(w.map);
    if (draft.scale) { // a stretched picture changes its own scale: mark it again
      draft.scale = null; draft.cmPerPx = null;
    }
    if (draft.segs.length) { const ids = Object.keys(draft.nodes), ix = new Map(ids.map((id, i) => [id, i])); draft.axis = planAxis(ids.map((id) => draft.nodes[id]), draft.segs.map((x) => ({ a: ix.get(x.a), b: ix.get(x.b) }))); }
    straight = null; usePhoto(w.canvas, true);
  }

  // ---------- events ----------
  root.addEventListener('click', (e) => {
    const b = e.target.closest('[data-act]'); if (!b || !root.contains(b) || b.disabled) return;
    const a = b.dataset.act, v = b.dataset.v;
    if (a === 'close') { saveNow(); if (opts.onCancel) opts.onCancel(); return; }
    if (a === 'save') return saveFile();
    if (a === 'pick') return $('file').click();
    if (a === 'camera') return $('cam').click();
    if (a === 'loadfile') return $('json').click();
    if (a === 'measure') { draft = newDraft('measure'); photo = null; dropImage(); undo.length = redo.length = 0; tool = 'rect'; kind = 'partition'; saveNow(); screen(); fit(); paint(); return; }
    if (a === 'resume') { const st = readStore(); if (st && okDraft(st.draft)) { draft = st.draft; resumeImage().then(() => { screen(); fit(); paint(); }); } return; }
    if (a === 'page') { const n = +v; $('body').innerHTML = '<p class="pm-wait">' + esc(P.loading) + '</p>'; pdfPageCanvas(pdfDoc, n).then((c) => usePhoto(c)).catch(() => { toast(P.pdfFail); draft = null; screen(); }); return; }
    if (a === 'go') return go(b.dataset.step);
    if (a === 'rotate') return rotatePhoto();
    if (a === 'straight') { if (straight) straight = null; else { const W = photo.width, H = photo.height, m = 0.08; straight = [[W * m, H * m], [W * (1 - m), H * m], [W * (1 - m), H * (1 - m)], [W * m, H * (1 - m)]]; } panel(); paint(); return; }
    if (a === 'straight-apply') return applyStraight();
    if (a === 'door') { const n = +v, i = $('in-len'); if (i) i.value = String(n); if (scaleTmp) { scaleTmp.cm = n; scaleTmp.door = n; } panel(); paint(); return; }
    if (a === 'scale-ok') {
      const val = +(($('in-len') || {}).value || 0);
      if (!scaleTmp || !scaleTmp.b) { toast(P.scaleNeedLine); return; }
      if (!(val > 0)) { toast(P.scaleNeedLen); $('in-len').focus(); return; }
      const px = dist(scaleTmp.a, scaleTmp.b); if (px < 1) { toast(P.scaleNeedLine); return; }
      commit(() => { draft.cmPerPx = val / px; draft.scale = { a: scaleTmp.a, b: scaleTmp.b, cm: val, door: scaleTmp.door === val }; });
      go('walls'); return;
    }
    if (a === 'tool') { tool = v; chain = null; rectA = null; pending = null; panel(); paint(); return; }
    if (a === 'kind') { kind = v; panel(); return; }
    if (a === 'undo') return doUndo();
    if (a === 'redo') return doRedo();
    if (a === 'endline') { chain = null; chainStart = null; rectA = null; pending = null; panel(); paint(); return; }
    if (a === 'rect-add') {
      const W = +$('in-w').value, D = +$('in-d').value;
      if (!(W > 0 && D > 0)) { toast(P.rectFirst); return; }
      addTypedRoom(W, D); return;
    }
    if (a === 'otype') { otype = v; selOpen = null; panel(); paint(); return; }
    if (a === 'open-del') { const id = selOpen; selOpen = null; commit(() => (draft.openings = draft.openings.filter((o) => o.id !== id))); return; }
    if (a === 'name') {
      const f = analyze().faces[selFace]; if (!f) return;
      commit(() => { draft.rooms = draft.rooms.filter((r) => !pip(r.at, f.poly)); draft.rooms.push({ at: f.at.map((x) => Math.round(x * 1000) / 1000), key: v }); });
      selFace = null; names(); fit(); paint(); return;
    }
    if (a === 'names-x') { selFace = null; names(); fit(); paint(); return; }
    if (a === 'done') {
      const r = analyze();
      if (!r.plan) { const x = r.problems[0], f = x && P.problems[x.code]; toast(typeof f === 'function' ? f(x.n || 1) : f || P.roomsNone); return; }
      const o = readStore() || {}; o.v = 1; o.draft = draft; o.plan = r.plan; o.saved = Date.now(); writeStore(o);
      if (opts.onDone) opts.onDone(r.plan, clone(draft));
      return;
    }
    if (a === 'reset') {
      if (sureReset < Date.now()) { sureReset = Date.now() + 4000; panel(); setTimeout(() => alive && draft && panel(), 4100); return; }
      sureReset = 0; draft = null; photo = null; dropImage(); const o = readStore() || {}; delete o.draft; writeStore(o); undo.length = redo.length = 0; screen(); return;
    }
  });
  root.addEventListener('input', (e) => {
    const t = e.target;
    if (t.dataset.pm === 'opa') { draft.opacity = +t.value / 100; save(); paint(); }
    if (t.dataset.pm === 'in-len') { if (scaleTmp) { scaleTmp.cm = +t.value || null; scaleTmp.door = null; } paint(); }
  });
  root.addEventListener('change', (e) => {
    const t = e.target;
    if (t.dataset.pm === 'in-ow') { const o = draft.openings.find((x) => x.id === selOpen), w = +t.value; if (o && w >= 20) commit(() => (o.w = w)); }
  });
  root.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target.dataset && e.target.dataset.pm === 'in-ow') e.target.blur(); });
  root.addEventListener('submit', (e) => {
    e.preventDefault();
    const f = e.target; if (f.dataset.pm !== 'edit') return;
    const v = +f.querySelector('input').value; f.hidden = true;
    if (v > 0) setLength(f.dataset.seg, v);
  });
  for (const [k2, fn] of [['file', openFile], ['cam', openFile], ['json', openSaved]]) $(k2).addEventListener('change', (e) => { const f = e.target.files && e.target.files[0]; e.target.value = ''; if (f) fn(f); });
  const onKey = (e) => {
    if (!draft || draft.step === 'start' || (e.target && /INPUT|TEXTAREA/.test((e.composedPath()[0] || {}).tagName || ''))) return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z') { e.preventDefault(); e.shiftKey ? doRedo() : doUndo(); }
    if (e.key === 'Escape') { chain = null; rectA = null; pending = null; panel(); paint(); }
  };
  document.addEventListener('keydown', onKey);

  function bindStage() {
    cv.addEventListener('pointerdown', (e) => {
      if (e.button > 0 && e.pointerType === 'mouse') { g = { kind: 'pan', s: local(e), v0: { ...V } }; try { cv.setPointerCapture(e.pointerId); } catch (x) { /* synthetic */ } return; }
      ptr.set(e.pointerId, local(e)); try { cv.setPointerCapture(e.pointerId); } catch (x) { /* synthetic */ }
      $('edit').hidden = true;
      if (ptr.size === 2) { // two fingers: move and zoom, and whatever one finger started is dropped
        if (g && g.before) { restore(g.before); ver++; }
        const [a, b] = [...ptr.values()];
        g = { kind: 'pinch', d0: dist(a, b), m0: [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], v0: { ...V } }; paint(); return;
      }
      if (ptr.size > 2) return;
      g = startGesture(local(e), e.pointerType !== 'mouse'); paint();
    });
    cv.addEventListener('pointermove', (e) => {
      const s = local(e);
      if (ptr.has(e.pointerId)) ptr.set(e.pointerId, s);
      if (g && g.kind === 'pinch') {
        if (ptr.size < 2) return;
        const [a, b] = [...ptr.values()], m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], z = Math.max(V.fit * 0.25, Math.min(V.fit * 16, g.v0.z * (dist(a, b) / (g.d0 || 1))));
        const p0 = [(g.m0[0] - g.v0.x) / g.v0.z, (g.m0[1] - g.v0.y) / g.v0.z];
        V.z = z; V.x = m[0] - p0[0] * z; V.y = m[1] - p0[1] * z; paint(); return;
      }
      if (g) { moveGesture(s); return; }
      if (e.pointerType === 'mouse' && draft && draft.step !== 'start') { hover = pickPoint(toD(s)); paint(); }
    });
    const up = (e) => {
      const had = ptr.delete(e.pointerId);
      if (g && g.kind === 'pinch') { if (ptr.size === 0) g = null; return; }
      if (!had && !(g && g.kind === 'pan')) return;
      endGesture(local(e), e.type === 'pointercancel');
    };
    cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
    cv.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse' && !g) { hover = null; paint(); } });
    cv.addEventListener('wheel', (e) => {
      e.preventDefault();
      const s = local(e), z = Math.max(V.fit * 0.25, Math.min(V.fit * 16, V.z * Math.exp(-e.deltaY * 0.0015))), p = toD(s);
      V.z = z; V.x = s[0] - p[0] * z; V.y = s[1] - p[1] * z; paint();
    }, { passive: false });
    cv.addEventListener('contextmenu', (e) => e.preventDefault());
    // a tap that opens the names sheet must not also "click" the button that appears under the finger
    cv.addEventListener('touchend', (e) => { if (e.cancelable) e.preventDefault(); }, { passive: false });
  }
  async function resumeImage() {
    photo = null;
    if (draft && draft.mode === 'image') { const b = await getImage(); if (b) try { photo = await blobToCanvas(b); } catch (e) { photo = null; } }
  }

  // ---------- start ----------
  const stored = readStore();
  if (opts.draft && okDraft(opts.draft)) { draft = clone(opts.draft); if (!draft.step || draft.step === 'start') draft.step = 'rooms'; await resumeImage(); }
  else if (stored && okDraft(stored.draft) && stored.draft.step && stored.draft.step !== 'start' && (stored.draft.segs.length || stored.draft.mode === 'image')) {
    draft = stored.draft; await resumeImage();
    if (draft.mode === 'image' && !photo && !draft.segs.length) draft = null; // the picture is gone and nothing was drawn
    else setTimeout(() => alive && toast(P.resumed), 50);
  }
  if (draft && draft.mode === 'measure') { tool = draft.segs.length ? 'line' : 'rect'; kind = 'partition'; }
  screen();
  if (draft) { fit(); paint(); }

  return {
    getDraft: () => (draft ? clone(draft) : null),
    /** a proposal of walls from automatic recognition: shown as the draft the person then corrects */
    propose({ segments, cmPerPx } = {}) {
      if (!Array.isArray(segments) || !segments.length) return false;
      if (!draft) { draft = newDraft(photo ? 'image' : 'measure'); }
      const pts = [], segs = [];
      for (const s of segments) if (s && Array.isArray(s.a) && Array.isArray(s.b)) { pts.push(s.a, s.b); segs.push({ a: pts.length - 2, b: pts.length - 1, kind: DRAW_KINDS.includes(s.kind) ? s.kind : 'partition' }); }
      const before = snapshot();
      const gr = cleanGraph(pts, segs, 4);
      draft.nodes = {}; gr.pts.forEach((p, i) => (draft.nodes['n' + i] = [p[0], p[1]]));
      draft.segs = gr.segs.map((s, i) => ({ id: 's' + i, a: 'n' + s.a, b: 'n' + s.b, kind: s.kind }));
      draft.axis = planAxis(gr.pts, gr.segs);
      if (cmPerPx > 0) draft.cmPerPx = cmPerPx;
      undo.push(before); redo.length = 0; ver++;
      draft.step = draft.mode === 'image' && !draft.cmPerPx ? 'scale' : 'walls'; tool = 'move';
      saveNow(); screen(); fit(); paint();
      return true;
    },
    /** test hooks: where a draft point is on the screen (client pixels), and the state */
    screenOf(x, y) { if (!cv) return null; const r = cv.getBoundingClientRect(), s = toS([x, y]); return [r.left + s[0], r.top + s[1]]; },
    get step() { return draft ? draft.step : 'start'; },
    get loupeShown() { return !!(loupe && !loupe.hidden); },
    get hasPhoto() { return !!photo; },
    /** the length labels on the screen (client pixels) with the wall each one measures */
    labels() { if (!cv) return []; const r = cv.getBoundingClientRect(); return labelBoxes.filter((b) => b.id).map((b) => { const s = seg(b.id); const il = innerLengths(draft.nodes, draft.segs, k()); return { id: b.id, x: r.left + (b.x0 + b.x1) / 2, y: r.top + (b.y0 + b.y1) / 2, cm: s && il[b.id] ? Math.round(il[b.id].inner) : null }; }); },
    analyze: () => (draft ? analyze() : null),
    destroy() { alive = false; saveNow(); clearTimeout(toastT); if (raf) cancelAnimationFrame(raf); if (ro) ro.disconnect(); document.removeEventListener('keydown', onKey); shadow.textContent = ''; },
  };
}
