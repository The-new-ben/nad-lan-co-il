// "The floor and paint in your room": the pure math (no DOM, runs in node too).
// Four taps on a photo become a rectangle on the floor; a pixel of the photo becomes a point on the floor in centimetres;
// the floor patterns are drawn by formula, filtered to the size of one pixel, so far joints stay smooth instead of jagged.
// Everything works on plain typed arrays, so the same code is checked in node (test-photowarp.mjs) and runs in the page.

export const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const SQRT2 = Math.SQRT2;

// ---------------------------------------------------------------- linear algebra
/** Gauss-Jordan with partial pivoting. A: n rows of n numbers, b: n numbers. null when singular. */
export function solve(A, b) {
  const n = b.length, M = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    if (Math.abs(M[p][c]) < 1e-12) return null;
    if (p !== c) { const t = M[c]; M[c] = M[p]; M[p] = t; }
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const k = M[r][c] / M[c][c];
      if (k) for (let j = c; j <= n; j++) M[r][j] -= k * M[c][j];
    }
  }
  return M.map((r, i) => r[n] / r[i]);
}

/** 3x3 matrices as 9 numbers, row major */
export function mul(A, B) {
  const o = new Array(9);
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) o[r * 3 + c] = A[r * 3] * B[c] + A[r * 3 + 1] * B[3 + c] + A[r * 3 + 2] * B[6 + c];
  return o;
}
export function invert(H) {
  const [a, b, c, d, e, f, g, h, i] = H;
  const A = e * i - f * h, B = -(d * i - f * g), C = d * h - e * g, det = a * A + b * B + c * C;
  if (Math.abs(det) < 1e-18) return null;
  const k = 1 / det;
  return [A * k, -(b * i - c * h) * k, (b * f - c * e) * k, B * k, (a * i - c * g) * k, -(a * f - c * d) * k, C * k, -(a * h - b * g) * k, (a * e - b * d) * k];
}
/** maps a point through a homography; null when the point goes to infinity */
export function apply(H, x, y) {
  const w = H[6] * x + H[7] * y + H[8];
  if (Math.abs(w) < 1e-12) return null;
  return [(H[0] * x + H[1] * y + H[2]) / w, (H[3] * x + H[4] * y + H[5]) / w];
}
function normT(pts) { // Hartley normalisation: centroid to the origin, mean distance sqrt(2)
  let cx = 0, cy = 0;
  for (const p of pts) { cx += p[0]; cy += p[1]; }
  cx /= pts.length; cy /= pts.length;
  let md = 0;
  for (const p of pts) md += Math.hypot(p[0] - cx, p[1] - cy);
  md /= pts.length;
  const s = md > 1e-12 ? SQRT2 / md : 1;
  return [s, 0, -s * cx, 0, s, -s * cy, 0, 0, 1];
}
/** the 3x3 projective map that sends the four src points onto the four dst points (null when three are on one line) */
export function homography(src, dst) {
  if (src.length !== 4 || dst.length !== 4) return null;
  for (const P of [src, dst]) for (let i = 0; i < 4; i++) { // three points on one line: no map
    const a = P[i], b = P[(i + 1) % 4], c = P[(i + 2) % 4], s = Math.max(Math.hypot(b[0] - a[0], b[1] - a[1]), Math.hypot(c[0] - a[0], c[1] - a[1]));
    if (Math.abs(cross(a, b, c)) <= 1e-9 * s * s) return null;
  }
  const Ts = normT(src), Td = normT(dst);
  const s = src.map((p) => apply(Ts, p[0], p[1])), d = dst.map((p) => apply(Td, p[0], p[1]));
  const A = [], b = [];
  for (let i = 0; i < 4; i++) {
    const [x, y] = s[i], [X, Y] = d[i];
    A.push([x, y, 1, 0, 0, 0, -X * x, -X * y]); b.push(X);
    A.push([0, 0, 0, x, y, 1, -Y * x, -Y * y]); b.push(Y);
  }
  const h = solve(A, b);
  if (!h) return null;
  const Tdi = invert(Td);
  if (!Tdi) return null;
  const H = mul(Tdi, mul([...h, 1], Ts));
  const k = Math.abs(H[8]) > 1e-12 ? 1 / H[8] : 1;
  return H.map((v) => v * k);
}

// ---------------------------------------------------------------- polygons
export function pointInPolygon(p, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if (yi > p[1] !== yj > p[1] && p[0] < ((xj - xi) * (p[1] - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
export function polygonArea(poly) {
  let a = 0;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) a += (poly[j][0] + poly[i][0]) * (poly[j][1] - poly[i][1]);
  return Math.abs(a) / 2;
}
const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
/** convex hull, monotone chain */
export function convexHull(pts) {
  const p = pts.map((q) => [q[0], q[1]]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  if (p.length < 3) return p;
  const lo = [], up = [];
  for (const q of p) { while (lo.length >= 2 && cross(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q); }
  for (let i = p.length - 1; i >= 0; i--) { const q = p[i]; while (up.length >= 2 && cross(up[up.length - 2], up[up.length - 1], q) <= 0) up.pop(); up.push(q); }
  return lo.slice(0, -1).concat(up.slice(0, -1));
}
export function segmentsCross(a, b, c, d) {
  const d1 = cross(c, d, a), d2 = cross(c, d, b), d3 = cross(a, b, c), d4 = cross(a, b, d);
  return ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0));
}
/** true when four points in this order make a convex shape that does not cross itself */
export function isConvexQuad(q) {
  if (q.length !== 4) return false;
  let sign = 0;
  for (let i = 0; i < 4; i++) {
    const c = cross(q[i], q[(i + 1) % 4], q[(i + 2) % 4]);
    if (Math.abs(c) < 1e-9) return false;
    const s = Math.sign(c);
    if (sign && s !== sign) return false;
    sign = s;
  }
  return true;
}
/**
 * The four floor taps in a fixed order, whatever order they were tapped in: A and B are the far edge (the line of the wall
 * in front of you, A on the left), D and C the near edge (the lowest edge in the photo). null when they do not make a floor.
 */
export function orderFloor(pts) {
  if (!pts || pts.length !== 4) return null;
  const cx = pts.reduce((a, p) => a + p[0], 0) / 4, cy = pts.reduce((a, p) => a + p[1], 0) / 4;
  const poly = pts.map((p) => [p[0], p[1]]).sort((a, b) => Math.atan2(a[1] - cy, a[0] - cx) - Math.atan2(b[1] - cy, b[0] - cx));
  if (!isConvexQuad(poly)) return null;
  let near = 0, best = -Infinity;
  for (let i = 0; i < 4; i++) { const m = (poly[i][1] + poly[(i + 1) % 4][1]) / 2; if (m > best) { best = m; near = i; } }
  let q = [poly[(near + 2) % 4], poly[(near + 3) % 4], poly[near], poly[(near + 1) % 4]];
  if (q[0][0] > q[1][0]) q = [q[1], q[0], q[3], q[2]];
  return q;
}

// ---------------------------------------------------------------- camera (the sample room and the checks use it)
/** a pinhole camera. World: X to the right, Y forward into the room, Z up, in centimetres. yaw turns to the right, pitch < 0 looks down. */
export function camera({ w, h, f, pos, yaw = 0, pitch = 0 }) {
  const cx = w / 2, cy = h / 2, cp = Math.cos(pitch), sp = Math.sin(pitch), cyw = Math.cos(yaw), syw = Math.sin(yaw);
  const fw = [syw * cp, cyw * cp, sp];
  const rt = [cyw, -syw, 0];
  const up = [rt[1] * fw[2] - rt[2] * fw[1], rt[2] * fw[0] - rt[0] * fw[2], rt[0] * fw[1] - rt[1] * fw[0]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  return {
    w, h, f, cx, cy, pos, fw, rt, up,
    /** [x, y, depth] in pixels; depth <= 0 is behind the camera */
    project(P) {
      const d = [P[0] - pos[0], P[1] - pos[1], P[2] - pos[2]], z = dot(d, fw);
      return [cx + (f * dot(d, rt)) / z, cy - (f * dot(d, up)) / z, z];
    },
    /** the direction of the ray through a pixel */
    ray(x, y) {
      const a = (x - cx) / f, b = -(y - cy) / f;
      return [fw[0] + a * rt[0] + b * up[0], fw[1] + a * rt[1] + b * up[1], fw[2] + a * rt[2] + b * up[2]];
    },
  };
}

// ---------------------------------------------------------------- the floor from four taps
export const CAMERA_HEIGHT = 145; // cm: a phone held at chest height, used only when no measure is given
const FOCAL_GUESS = 0.75; // the main camera of a phone: about 0.75 of the long side of the photo, in pixels

/**
 * What four floor taps say about the camera: the focal length (from the two vanishing points when the photo has them,
 * else the usual phone value), the proportion width/depth of the marked rectangle, and the camera height per unit of width.
 */
export function estimateCamera(q, iw, ih) {
  const L = Math.max(iw, ih), cx = iw / 2, cy = ih / 2;
  const c = q.map((p) => [p[0] - cx, p[1] - cy]);
  const H0 = homography([[0, 0], [1, 0], [1, 1], [0, 1]], c);
  if (!H0) return null;
  const h1 = [H0[0], H0[3], H0[6]], h2 = [H0[1], H0[4], H0[7]], h3 = [H0[2], H0[5], H0[8]];
  let f = null;
  // both vanishing points must be in reach (closer than 8 photo widths), else the photo cannot tell the lens
  const vp1 = Math.hypot(h1[0], h1[1]) / Math.abs(h1[2] || 1e-300), vp2 = Math.hypot(h2[0], h2[1]) / Math.abs(h2[2] || 1e-300);
  if (vp1 < 8 * L && vp2 < 8 * L) {
    const f2 = -(h1[0] * h2[0] + h1[1] * h2[1]) / (h1[2] * h2[2]);
    if (f2 > 0) { const ff = Math.sqrt(f2); if (ff > 0.35 * L && ff < 2.5 * L) f = ff; }
  }
  const fromPhoto = f != null;
  if (!f) f = FOCAL_GUESS * L;
  const r1 = [h1[0] / f, h1[1] / f, h1[2]], r2 = [h2[0] / f, h2[1] / f, h2[2]], t = [h3[0] / f, h3[1] / f, h3[2]];
  const n1 = Math.hypot(...r1), n2 = Math.hypot(...r2);
  const a = r1.map((v) => v / n1), b = r2.map((v) => v / n2);
  let r3 = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const n3 = Math.hypot(...r3);
  r3 = r3.map((v) => v / n3);
  const heightPerWidth = Math.abs(r3[0] * t[0] + r3[1] * t[1] + r3[2] * t[2]) / n1;
  return { f, fromPhoto, aspect: n1 / n2, heightPerWidth };
}

/**
 * The floor frame: the map from a pixel to the floor in centimetres. u runs along the far edge from A to B, v from the far
 * edge towards the camera. width (cm) is the far edge; depth (cm) is optional. Without width, the size comes from the usual
 * height of a phone camera, and `measured` is false.
 */
export function floorFrame(pts, iw, ih, m = {}) {
  const q = orderFloor(pts);
  if (!q) return null;
  const cam = estimateCamera(q, iw, ih);
  if (!cam || !isFinite(cam.aspect) || cam.aspect <= 0) return null;
  const width = m.width > 0 ? m.width : null, depth = m.depth > 0 ? m.depth : null;
  const W = width || CAMERA_HEIGHT / cam.heightPerWidth;
  const D = depth || W / cam.aspect;
  if (!isFinite(W) || !isFinite(D) || W <= 0 || D <= 0) return null;
  const H = homography(q, [[0, 0], [W, 0], [W, D], [0, D]]);
  const Hinv = H && invert(H);
  if (!H || !Hinv) return null;
  return { quad: q, W, D, f: cam.f, fromPhoto: cam.fromPhoto, aspect: cam.aspect, measured: !!width, depthMeasured: !!depth, H, Hinv, sqm: (W * D) / 10000 };
}

/**
 * The part of the photo to cover: the marked rectangle, plus the floor that runs on towards the camera and off the bottom
 * of the photo (the two side edges extended past the near edge). Falls back to the rectangle when the sides do not open up.
 */
export function floorRegion(q, iw, ih) {
  const [A, B, C, D] = q, L = 4 * Math.max(iw, ih);
  const ext = (from, to) => { const dx = to[0] - from[0], dy = to[1] - from[1], n = Math.hypot(dx, dy) || 1; return [to[0] + (dx / n) * L, to[1] + (dy / n) * L]; };
  const C2 = ext(B, C), D2 = ext(A, D);
  if (segmentsCross(B, C2, A, D2) || !isConvexQuad([A, B, C2, D2])) return q.map((p) => [...p]);
  return [A, B, C2, D2];
}

// ---------------------------------------------------------------- colour
const LIN8 = new Float32Array(256);
for (let i = 0; i < 256; i++) { const c = i / 255; LIN8[i] = c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
export const srgbToLinear = (c8) => LIN8[c8 | 0];
const OUT = new Uint8ClampedArray(4097);
for (let i = 0; i <= 4096; i++) { const c = i / 4096; OUT[i] = Math.round(255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055)); }
export const linearToSrgb = (v) => OUT[v <= 0 ? 0 : v >= 1 ? 4096 : (v * 4096 + 0.5) | 0];
export function hexToLinear(hex) {
  const h = hex.replace('#', '');
  return [0, 2, 4].map((i) => LIN8[parseInt(h.slice(i, i + 2), 16)]);
}
/** keeps a bright spot (a sun patch) bright without hard clipping */
export const shoulder = (v) => (v <= 0.82 ? v : 0.82 + 0.18 * (1 - Math.exp(-(v - 0.82) / 0.18)));

// ---------------------------------------------------------------- pattern helpers
export function hash(i, j) {
  let h = Math.imul(i | 0, 374761393) ^ Math.imul(j | 0, 668265263);
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967296;
}
const NT = new Float32Array(65536);
for (let j = 0; j < 256; j++) for (let i = 0; i < 256; i++) NT[i + (j << 8)] = hash(i, j);
/** smooth value noise in [0,1] (a 256 x 256 lattice that repeats every 256 units) */
export function vnoise(x, y) {
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const i0 = xi & 255, i1 = (xi + 1) & 255, j0 = (yi & 255) << 8, j1 = ((yi + 1) & 255) << 8;
  const a = NT[i0 + j0], b = NT[i1 + j0], c = NT[i0 + j1], d = NT[i1 + j1];
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}
/**
 * How much of a pixel is covered by joint lines: lines of width t start at every whole number of x; the pixel spans w
 * around x (all in units of the period). The exact box-filtered value, so a far joint fades to a faint line instead of
 * flickering on and off.
 */
export function lineCov(x, w, t) {
  if (w < 1e-4) w = 1e-4;
  const a = x + w * 0.5, b = x - w * 0.5, fa = Math.floor(a), fb = Math.floor(b), ra = a - fa, rb = b - fb;
  return ((fa - fb) * t + (ra < t ? ra : t) - (rb < t ? rb : t)) / w;
}
const mix3 = (a, b, k, o) => { o[0] = a[0] + (b[0] - a[0]) * k; o[1] = a[1] + (b[1] - a[1]) * k; o[2] = a[2] + (b[2] - a[2]) * k; return o; };

// ---------------------------------------------------------------- floor patterns (centimetres, linear colour)
/**
 * Makes the drawing function of one floor: fn(u, v, fu, fv, out) writes the linear colour at (u, v) cm, averaged over a
 * pixel that spans fu x fv cm. def = { tex: tile | wood | deck | terrazzo | concrete, w, h, a, b, ... }
 */
export function makePattern(def) {
  const A = hexToLinear(def.a), B = hexToLinear(def.b || def.a);
  if (def.tex === 'wood' || def.tex === 'deck') {
    const deck = def.tex === 'deck';
    const pw = def.pw || (deck ? 14 : 19), pl = def.pl || def.size || 150, gs = def.gs || (deck ? 0.6 : 0.12);
    const S = def.seam ? hexToLinear(def.seam) : B.map((v) => v * (deck ? 0.18 : 0.42)), gf = deck ? 0.7 : 1.15;
    const T = [0, 0, 0];
    return (u, v, fu, fv, o) => {
      const rv = v / pw, j = Math.floor(rv), off = hash(j, 91) * pl, uu = u + off, ru = uu / pl, i = Math.floor(ru);
      const rowFade = clamp01(1.5 - (2 * fv) / pw);
      const sv = lineCov(rv + gs / (2 * pw), fv / pw, gs / pw);
      const su = lineCov(ru + gs / (2 * pl), fu / pl, gs / pl) * rowFade;
      const seam = 1 - (1 - sv) * (1 - su);
      const tone = 0.5 + (hash(i, j) - 0.5) * 1.6 * rowFade * clamp01(1.5 - (2 * fu) / pl);
      mix3(A, B, clamp01(tone), T);
      const ga = clamp01(1 - fv * gf * 1.3) * (deck ? 0.06 : 0.11);
      const warp = vnoise(uu * 0.018, j * 7.1 + 0.3) * 3.2 + vnoise(uu * 0.09, j * 3.3 + 9) * 0.5;
      const grain = Math.sin((v * gf + warp) * 6.2832) * ga;
      const streak = (vnoise(uu * 0.025, v * 0.5 + j * 11) - 0.5) * clamp01(1 - Math.max(fu * 0.025, fv * 0.5)) * 0.22;
      const k = 1 + grain + streak;
      o[0] = T[0] * k; o[1] = T[1] * k; o[2] = T[2] * k;
      if (seam > 0) mix3(o, S, seam * 0.85, o);
      return o;
    };
  }
  if (def.tex === 'terrazzo') {
    const W = def.w || def.size || 60, g = def.g || 0.2, c = 1.7;
    const CH = [B, hexToLinear('#F4F3EF'), hexToLinear('#3A3E43'), hexToLinear('#9AA3A8')];
    const P = [0.34, 0.3, 0.16, 0.2], mean = [0, 0, 0];
    for (let k = 0; k < 4; k++) for (let n = 0; n < 3; n++) mean[n] += CH[k][n] * P[k];
    const avg = mix3(A, mean, 0.2, [0, 0, 0]), G = A.map((v) => v * 0.7), T = [0, 0, 0];
    return (u, v, fu, fv, o) => {
      const fw = Math.max(fu, fv), ci = Math.floor(u / c), cj = Math.floor(v / c);
      const h1 = hash(ci, cj), h2 = hash(ci + 11, cj - 7), h3 = hash(ci - 5, cj + 13), h4 = hash(ci * 3 + 1, cj * 5 + 2);
      const r = c * (0.1 + 0.27 * h1), px = (ci + r / c + (1 - (2 * r) / c) * h2) * c, py = (cj + r / c + (1 - (2 * r) / c) * h3) * c;
      const d = Math.hypot(u - px, v - py), cov = h4 < 0.12 ? 0 : clamp01((r - d) / Math.max(fw, 0.04) + 0.5);
      const ch = CH[h4 < 0.46 ? 0 : h4 < 0.76 ? 1 : h4 < 0.88 ? 2 : 3];
      const sharp = clamp01(1.5 - (2 * fw) / c);
      mix3(A, ch, cov, T);
      mix3(avg, T, sharp, o);
      const gu = lineCov(u / W + g / (2 * W), fu / W, g / W), gv = lineCov(v / W + g / (2 * W), fv / W, g / W), gr = 1 - (1 - gu) * (1 - gv);
      if (gr > 0) mix3(o, G, gr, o);
      return o;
    };
  }
  if (def.tex === 'concrete') {
    const J = def.joint || 300, g = 0.5, G = A.map((v) => v * 0.55);
    return (u, v, fu, fv, o) => {
      const fw = Math.max(fu, fv);
      let n = (vnoise(u / 90, v / 90) - 0.5) * 0.5;
      n += (vnoise(u / 22 + 5, v / 22) - 0.5) * 0.32 * clamp01(1 - fw / 14);
      n += (vnoise(u / 4 - 3, v / 4) - 0.5) * 0.22 * clamp01(1 - fw / 2.5);
      n += (vnoise(u / 0.9, v / 0.9) - 0.5) * 0.12 * clamp01(1 - fw / 0.6);
      const k = 1 + n * 0.32;
      mix3(A, B, clamp01(0.5 + n * 1.4) * 0.5, o);
      o[0] *= k; o[1] *= k; o[2] *= k;
      const gu = lineCov(u / J + g / (2 * J), fu / J, g / J), gv = lineCov(v / J + g / (2 * J), fv / J, g / J), gr = 1 - (1 - gu) * (1 - gv);
      if (gr > 0) mix3(o, G, gr * 0.8, o);
      return o;
    };
  }
  // porcelain tiles: a soft stone print per tile, a hint of a bevel at the edge, a thin joint
  const TW = def.w || def.size || 60, TH = def.h || TW, g = def.g || 0.3, e = 1.4;
  const G = def.grout ? hexToLinear(def.grout) : mix3(B, [0, 0, 0], 0.3, [0, 0, 0]);
  const ms = def.ms || 26, tv = def.tv ?? 0.06, T = [0, 0, 0];
  const iTW = 1 / TW, iTH = 1 / TH, ims = 1 / ms, ims2 = 1 / (ms * 0.22), eu = e / (2 * TW), ev = e / (2 * TH), et = e / TW, eh = e / TH;
  const gu0 = g / (2 * TW), gv0 = g / (2 * TH), gtu = g / TW, gtv = g / TH;
  const dR = B[0] - A[0], dG = B[1] - A[1], dB = B[2] - A[2];
  return (u, v, fu, fv, o) => {
    const tu = u * iTW, tw = v * iTH, i = Math.floor(tu), j = Math.floor(tw), big = fu > fv ? fu : fv;
    const ftu = fu * iTW, ftv = fv * iTH;
    const fade = clamp01(1.5 - 2 * (ftu > ftv ? ftu : ftv));
    const f1 = clamp01(1 - big * ims * 1.5), f2 = clamp01(1 - big * ims2 * 1.5);
    let mk = 0.22;
    if (f1 > 0) mk += (vnoise(u * ims + i * 3.7, v * ims + j * 5.3) - 0.5) * f1 * 0.585;
    if (f2 > 0) mk += (vnoise(u * ims2 + i, v * ims2 - j) - 0.5) * f2 * 0.27;
    const bu = lineCov(tu + eu, ftu, et), bv = lineCov(tw + ev, ftv, eh);
    const k = (1 + (fade > 0 ? (hash(i, j) - 0.5) * tv * fade : 0)) * (1 - 0.07 * (1 - (1 - bu) * (1 - bv)));
    o[0] = (A[0] + dR * mk) * k; o[1] = (A[1] + dG * mk) * k; o[2] = (A[2] + dB * mk) * k;
    const gu = lineCov(tu + gu0, ftu, gtu), gv = lineCov(tw + gv0, ftv, gtv), gr = 1 - (1 - gu) * (1 - gv);
    if (gr > 0) { o[0] += (G[0] - o[0]) * gr; o[1] += (G[1] - o[1]) * gr; o[2] += (G[2] - o[2]) * gr; }
    return o;
  };
}

// ---------------------------------------------------------------- image work on typed arrays
/** linear luminance of an RGBA buffer */
export function luminance(rgba, n) {
  const L = new Float32Array(n);
  for (let i = 0, j = 0; i < n; i++, j += 4) L[i] = 0.2126 * LIN8[rgba[j]] + 0.7152 * LIN8[rgba[j + 1]] + 0.0722 * LIN8[rgba[j + 2]];
  return L;
}
/** in-place box blur (one horizontal and one vertical pass), averaging only what is inside the picture */
export function boxBlur(a, w, h, r) {
  if (r < 1) return a;
  const s = new Float64Array(w + 1);
  for (let y = 0; y < h; y++) {
    const o = y * w;
    s[0] = 0;
    for (let x = 0; x < w; x++) s[x + 1] = s[x] + a[o + x];
    for (let x = 0; x < w; x++) { const x0 = x - r < 0 ? 0 : x - r, x1 = x + r >= w ? w - 1 : x + r; a[o + x] = (s[x1 + 1] - s[x0]) / (x1 - x0 + 1); }
  }
  // vertical: a window of whole rows slides down the picture (reads memory in order, fast on a phone)
  const src = a.slice(), acc = new Float64Array(w);
  let cnt = 0;
  for (let y = 0; y <= Math.min(r, h - 1); y++) { const o = y * w; for (let x = 0; x < w; x++) acc[x] += src[o + x]; cnt++; }
  for (let y = 0; y < h; y++) {
    const o = y * w, k = 1 / cnt;
    for (let x = 0; x < w; x++) a[o + x] = acc[x] * k;
    const add = y + r + 1, rem = y - r;
    if (add < h) { const p = add * w; for (let x = 0; x < w; x++) acc[x] += src[p + x]; cnt++; }
    if (rem >= 0) { const p = rem * w; for (let x = 0; x < w; x++) acc[x] -= src[p + x]; cnt--; }
  }
  return a;
}
/** softens the edge of a 0-255 mask by r pixels */
export function featherMask(m, w, h, r) {
  if (r < 1) return m;
  // only pixels near an edge change: find them, then average a (2r+1) square around each from the unchanged mask
  const edge = [];
  for (let y = 0; y < h; y++) {
    const o = y * w;
    for (let x = 0; x < w; x++) {
      const i = o + x, v = m[i];
      if ((x + 1 < w && m[i + 1] !== v) || (y + 1 < h && m[i + w] !== v) || v % 255 !== 0) edge.push(i);
    }
  }
  const src = new Uint8Array(m), seen = new Uint8Array(m.length), todo = [];
  for (const i of edge) {
    const x = i % w, y = (i / w) | 0;
    for (let yy = Math.max(0, y - r); yy <= Math.min(h - 1, y + r); yy++) for (let xx = Math.max(0, x - r); xx <= Math.min(w - 1, x + r); xx++) { const k = yy * w + xx; if (!seen[k]) { seen[k] = 1; todo.push(k); } }
  }
  for (const i of todo) {
    const x = i % w, y = (i / w) | 0;
    let s = 0, n = 0;
    for (let yy = Math.max(0, y - r); yy <= Math.min(h - 1, y + r); yy++) for (let xx = Math.max(0, x - r); xx <= Math.min(w - 1, x + r); xx++) { s += src[yy * w + xx]; n++; }
    m[i] = Math.round(s / n);
  }
  return m;
}
/**
 * The light on the floor: the brightness of the original floor, smoothed so that its own joints and grain disappear but
 * shadows, the patch of sun from a window and the darker corners stay. Only floor pixels are averaged (the wall above and
 * the sofa never leak into it). Returns the light map and the typical floor brightness to divide by.
 */
export function floorLight(L, mask, w, h, r, k = 4) {
  // worked on a grid k times smaller (the light is smooth anyway), then read back with bilinear weights
  const sw = Math.ceil(w / k), sh = Math.ceil(h / k), num = new Float32Array(sw * sh), den = new Float32Array(sw * sh);
  for (let y = 0; y < h; y++) {
    const so = ((y / k) | 0) * sw, o = y * w;
    for (let x = 0; x < w; x++) { const m = mask[o + x]; if (!m) continue; const si = so + ((x / k) | 0), mm = m / 255; num[si] += L[o + x] * mm; den[si] += mm; }
  }
  const rr = Math.max(1, Math.round(r / k));
  boxBlur(num, sw, sh, rr); boxBlur(num, sw, sh, rr);
  boxBlur(den, sw, sh, rr); boxBlur(den, sw, sh, rr);
  const light = new Float32Array(w * h), tiny = 0.02 * k * k * 0.05;
  const X0 = new Int32Array(w), X1 = new Int32Array(w), TX = new Float32Array(w);
  for (let x = 0; x < w; x++) { let fx = (x + 0.5) / k - 0.5; if (fx < 0) fx = 0; if (fx > sw - 1) fx = sw - 1; X0[x] = fx | 0; X1[x] = Math.min(X0[x] + 1, sw - 1); TX[x] = fx - X0[x]; }
  for (let y = 0; y < h; y++) {
    let fy = (y + 0.5) / k - 0.5; if (fy < 0) fy = 0; if (fy > sh - 1) fy = sh - 1;
    const y0 = fy | 0, y1 = Math.min(y0 + 1, sh - 1), ty = fy - y0, o = y * w, r0 = y0 * sw, r1 = y1 * sw;
    for (let x = 0; x < w; x++) {
      if (!mask[o + x]) continue;
      const tx = TX[x], a = r0 + X0[x], b = r0 + X1[x], c = r1 + X0[x], d = r1 + X1[x];
      const w00 = (1 - tx) * (1 - ty), w10 = tx * (1 - ty), w01 = (1 - tx) * ty, w11 = tx * ty;
      const N = num[a] * w00 + num[b] * w10 + num[c] * w01 + num[d] * w11, D = den[a] * w00 + den[b] * w10 + den[c] * w01 + den[d] * w11;
      light[o + x] = D > tiny ? N / D : L[o + x];
    }
  }
  // soften what is left of the old floor's own light and dark (a dark board, a stain) while shadows and sun stay
  const ref = maskMedian(light, mask), soften = 0.78;
  for (let i = 0; i < light.length; i++) if (mask[i]) light[i] = ref * Math.pow(light[i] / ref, soften);
  return { light, ref };
}
/** the median of values where the mask is solid (sampled, fast) */
export function maskMedian(a, mask, stride = 0) {
  if (!stride) stride = Math.max(7, Math.floor(a.length / 40000) | 1); // about 40 000 samples, an odd step so rows do not alias
  const buf = new Float32Array(Math.ceil(a.length / stride));
  let n = 0;
  for (let i = 0; i < a.length; i += stride) if (mask[i] > 200) buf[n++] = a[i];
  if (!n) return 0.18;
  const v = buf.subarray(0, n).sort();
  return Math.max(v[n >> 1], 1e-3);
}

/**
 * Draws the new floor into out (RGBA, in place). For each pixel inside the mask: the pixel's point on the floor (u, v) and
 * its footprint in cm from the homography, the pattern averaged over that footprint, times the original light.
 * H maps a pixel to floor cm; rot in radians; origin in floor cm; step 2 draws a quick preview in 2x2 blocks.
 */
export function renderFloor({ out, w, h, mask, light, ref, H, pattern, rot = 0, origin = [0, 0], step = 1, soft = 1.3, grain = 0.018 }) {
  const c = Math.cos(rot), s = Math.sin(rot), col = [0, 0, 0], inv = 1 / ref;
  const [h0, h1, h2, h3, h4, h5, h6, h7, h8] = H, ox = origin[0], oy = origin[1], k = soft * step;
  let painted = 0;
  const half = 0.5 * step, dxW = h6 * step, dxX = h0 * step, dxY = h3 * step;
  for (let y = 0; y < h; y += step) {
    const py = y + half, row = y * w;
    // the homography terms grow by a constant per pixel along a row
    let Wd = h6 * half + h7 * py + h8, Xn = h0 * half + h1 * py + h2, Yn = h3 * half + h4 * py + h5;
    for (let x = 0; x < w; x += step, Wd += dxW, Xn += dxX, Yn += dxY) {
      const i = row + x, m = mask[i];
      if (!m || (Wd < 1e-12 && Wd > -1e-12)) continue;
      const iw = 1 / Wd, X = Xn * iw, Y = Yn * iw;
      const Xx = (h0 - X * h6) * iw, Xy = (h1 - X * h7) * iw, Yx = (h3 - Y * h6) * iw, Yy = (h4 - Y * h7) * iw;
      const dx = X - ox, dy = Y - oy, u = c * dx + s * dy, v = -s * dx + c * dy;
      const ux = c * Xx + s * Yx, uy = c * Xy + s * Yy, vx = c * Yx - s * Xx, vy = c * Yy - s * Xy;
      pattern(u, v, ((ux < 0 ? -ux : ux) + (uy < 0 ? -uy : uy)) * k, ((vx < 0 ? -vx : vx) + (vy < 0 ? -vy : vy)) * k, col);
      const lt = light[i] * inv * (1 + ((((Math.imul(x, 0x9E3779B1) ^ Math.imul(y, 0x85EBCA77)) >>> 8) & 255) / 255 - 0.5) * grain);
      const r8 = linearToSrgb(shoulder(col[0] * lt)), g8 = linearToSrgb(shoulder(col[1] * lt)), b8 = linearToSrgb(shoulder(col[2] * lt));
      if (step === 1) {
        const j = i * 4;
        if (m === 255) { out[j] = r8; out[j + 1] = g8; out[j + 2] = b8; }
        else { const a = m / 255; out[j] += (r8 - out[j]) * a; out[j + 1] += (g8 - out[j + 1]) * a; out[j + 2] += (b8 - out[j + 2]) * a; }
      } else {
        const a = m / 255, yEnd = Math.min(y + step, h), xEnd = Math.min(x + step, w);
        for (let yy = y; yy < yEnd; yy++) for (let xx = x; xx < xEnd; xx++) {
          const j = (yy * w + xx) * 4;
          out[j] += (r8 - out[j]) * a; out[j + 1] += (g8 - out[j + 1]) * a; out[j + 2] += (b8 - out[j + 2]) * a;
        }
      }
      painted++;
    }
  }
  return painted;
}
/** paints a wall in a new colour, keeping the brightness of every pixel of the photo (shadows, light, texture) */
export function paintWall({ out, mask, L, ref, color, n }) {
  const inv = 1 / ref;
  for (let i = 0; i < n; i++) {
    const m = mask[i];
    if (!m) continue;
    const k = L[i] * inv, a = m / 255, j = i * 4;
    out[j] += (linearToSrgb(shoulder(color[0] * k)) - out[j]) * a;
    out[j + 1] += (linearToSrgb(shoulder(color[1] * k)) - out[j + 1]) * a;
    out[j + 2] += (linearToSrgb(shoulder(color[2] * k)) - out[j + 2]) * a;
  }
}
