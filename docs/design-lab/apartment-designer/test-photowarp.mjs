// node test-photowarp.mjs
// Checks the pure math of "the floor and paint in your room" (plugins/nadlan-config/assets/designer/photowarp.js) with no browser.
import * as W from '../../../plugins/nadlan-config/assets/designer/photowarp.js';

let n = 0, fails = 0;
const check = (name, ok, detail) => { n++; if (!ok) fails++; console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : '')); };
const near = (a, b, e) => Math.abs(a - b) <= e;
const DEG = Math.PI / 180;

// ---- solve and matrices
const x = W.solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]);
check('solve: a known 3x3 system', near(x[0], 2, 1e-9) && near(x[1], 3, 1e-9) && near(x[2], -1, 1e-9), x);
check('solve: a singular system returns null', W.solve([[1, 2], [2, 4]], [1, 2]) === null);
const M = [2, 0.3, 5, -0.1, 1.5, 7, 0.001, 0.0004, 1];
const I = W.mul(M, W.invert(M));
check('invert: M times its inverse is the identity', I.every((v, i) => near(v, i % 4 === 0 ? 1 : 0, 1e-9)));

// ---- homography round trip on many point sets
let worst = 0, sets = 0;
for (let k = 0; k < 200; k++) {
  const r = (a) => a * (W.hash(k, sets++) - 0.5);
  const src = [[0, 0], [400 + r(80), r(30)], [400 + r(80), 300 + r(60)], [r(30), 300 + r(60)]];
  const dst = [[100 + r(200), 900 + r(100)], [2300 + r(100), 950 + r(100)], [2400 + r(200), 1750 + r(50)], [r(200), 1700 + r(100)]];
  const H = W.homography(src, dst), Hi = W.invert(H);
  for (const p of src) { const q = W.apply(H, ...p); worst = Math.max(worst, Math.hypot(q[0] - dst[src.indexOf(p)][0], q[1] - dst[src.indexOf(p)][1])); }
  for (let t = 0; t < 10; t++) {
    const p = [W.hash(t, k) * 400, W.hash(k, t + 50) * 300], q = W.apply(H, ...p), b = W.apply(Hi, ...q);
    worst = Math.max(worst, Math.hypot(b[0] - p[0], b[1] - p[1]));
  }
}
check('homography: 200 random maps hit their four corners and come back (< 0.01 px)', worst < 0.01, { worst_px: +worst.toExponential(2) });
const H1 = W.homography([[0, 0], [1, 0], [1, 1], [0, 1]], [[0, 0], [1, 0], [1, 1], [0, 1]]);
check('homography: the identity', H1.every((v, i) => near(v, i % 4 === 0 ? 1 : 0, 1e-12)));
const Hs = W.homography([[0, 0], [1, 0], [1, 1], [0, 1]], [[10, 20], [30, 20], [30, 60], [10, 60]]);
check('homography: a scale and shift is affine (no perspective terms)', near(Hs[6], 0, 1e-12) && near(Hs[7], 0, 1e-12) && near(Hs[0], 20, 1e-9) && near(Hs[4], 40, 1e-9));
check('homography: three points on a line give null', W.homography([[0, 0], [1, 1], [2, 2], [0, 1]], [[0, 0], [1, 0], [1, 1], [0, 1]]) === null);
check('apply: a point at infinity gives null', W.apply([1, 0, 0, 0, 1, 0, 1, 0, 0], 0, 5) === null);

// ---- a known rectangle in a known perspective
const cam = W.camera({ w: 2400, h: 1800, f: 1800, pos: [210, -40, 150], pitch: -10 * DEG });
const room = { W: 420, D: 520 }, nearY = 280;
const corners = [[0, room.D, 0], [room.W, room.D, 0], [room.W, nearY, 0], [0, nearY, 0]].map((P) => cam.project(P).slice(0, 2));
check('camera: the far corners project above the near corners', corners[0][1] < corners[3][1] && corners[1][1] < corners[2][1], corners.map((p) => p.map(Math.round)));
check('camera: a point straight ahead lands in the middle of the photo', (() => { const p = cam.project([210, 1000, 150 + Math.tan(-10 * DEG) * 1040]); return near(p[0], 1200, 1e-6) && near(p[1], 900, 1e-6); })());
const ray = cam.ray(700, 1300), t = -cam.pos[2] / ray[2], hit = [cam.pos[0] + ray[0] * t, cam.pos[1] + ray[1] * t, 0], back = cam.project(hit);
check('camera: ray and projection agree', near(back[0], 700, 1e-6) && near(back[1], 1300, 1e-6));
const shuffled = [corners[2], corners[0], corners[3], corners[1]];
const q = W.orderFloor(shuffled);
check('orderFloor: any tap order gives far-left, far-right, near-right, near-left', q.every((p, i) => near(p[0], corners[i][0], 1e-9) && near(p[1], corners[i][1], 1e-9)));
check('orderFloor: a crossed or missing set is refused', W.orderFloor([[0, 0], [10, 0]]) === null && W.orderFloor([[0, 0], [10, 0], [5, 0], [0, 10]]) === null);
const fr = W.floorFrame(shuffled, 2400, 1800, { width: room.W, depth: room.D - nearY });
let err = 0;
for (let X = 0; X <= room.W; X += 35) for (let Y = nearY; Y <= room.D; Y += 30) {
  const p = cam.project([X, Y, 0]), uv = W.apply(fr.H, p[0], p[1]);
  err = Math.max(err, Math.abs(uv[0] - X), Math.abs(uv[1] - (room.D - Y)));
}
check('floorFrame with width and depth: every floor point lands on its true centimetre (< 0.01 cm)', err < 0.01, { worst_cm: +err.toExponential(2) });
const g = cam.project([210 + 60, 350, 0]), uvg = W.apply(fr.H, g[0], g[1]);
check('floorFrame: the joint 60 cm right of the centre is at u = W/2 + 60', near(uvg[0], room.W / 2 + 60, 1e-6), uvg);
const back2 = W.apply(fr.Hinv, room.W / 2 + 60, room.D - 350);
check('floorFrame: and back to the same pixel (< 0.01 px)', Math.hypot(back2[0] - g[0], back2[1] - g[1]) < 0.01);
check('floorFrame: area from the measures', near(fr.sqm, (420 * 240) / 10000, 1e-9) && fr.measured && fr.depthMeasured, fr.sqm);

// one-point view (the far edge is level): the lens is the usual phone value, the depth comes from it
const fr1 = W.floorFrame(corners, 2400, 1800, { width: 420 });
check('one-point photo: the lens is the phone guess (0.75 of the long side)', !fr1.fromPhoto && near(fr1.f, 1800, 1e-9), { f: fr1.f });
check('one-point photo: the depth comes out right when the lens is the usual one (< 1 cm)', near(fr1.D, 240, 1), { D: fr1.D });
const fr0 = W.floorFrame(corners, 2400, 1800, {});
check('no measure: the size comes from a chest-height camera (145 cm vs the true 150 cm, within 5%)', near(fr0.W, 420 * (145 / 150), 420 * 0.05) && !fr0.measured, { W: Math.round(fr0.W) });

// two-point view: the lens comes from the photo itself
const cam2 = W.camera({ w: 2400, h: 1800, f: 1500, pos: [80, -60, 140], yaw: 22 * DEG, pitch: -14 * DEG });
const c2 = [[0, 400, 0], [300, 400, 0], [300, 150, 0], [0, 150, 0]].map((P) => cam2.project(P).slice(0, 2));
const fr2 = W.floorFrame(c2, 2400, 1800, { width: 300 });
check('two-point photo: the lens is read from the photo (within 2%)', fr2.fromPhoto && near(fr2.f, 1500, 30), { f: Math.round(fr2.f) });
check('two-point photo: the proportion of the rectangle is right (within 2%)', near(fr2.aspect, 300 / 250, 0.024), { aspect: +fr2.aspect.toFixed(4) });
check('two-point photo: no measure, the height of the camera gives the size (within 3%)', near(W.floorFrame(c2, 2400, 1800, {}).W, 300 * (145 / 140), 300 * 0.03));

// the region to cover continues to the bottom of the photo
const reg = W.floorRegion(fr.quad, 2400, 1800);
check('floorRegion: the side edges run on past the bottom of the photo', reg[2][1] > 1800 && reg[3][1] > 1800, reg.map((p) => p.map(Math.round)));
check('floorRegion: a floor point below the marked rectangle is inside the region', W.pointInPolygon(cam.project([210, 200, 0]).slice(0, 2), reg));
check('floorRegion: a wall point is not', !W.pointInPolygon(cam.project([0, 300, 100]).slice(0, 2), reg) && !W.pointInPolygon(cam.project([210, 520, 50]).slice(0, 2), reg));

// ---- polygons
const sq = [[0, 0], [10, 0], [10, 10], [0, 10]];
check('pointInPolygon: inside, outside', W.pointInPolygon([5, 5], sq) && !W.pointInPolygon([15, 5], sq) && !W.pointInPolygon([5, -1], sq));
const L = [[0, 0], [10, 0], [10, 4], [4, 4], [4, 10], [0, 10]];
check('pointInPolygon: a concave L shape', W.pointInPolygon([2, 8], L) && !W.pointInPolygon([8, 8], L));
check('polygonArea: square 100, L shape 64', W.polygonArea(sq) === 100 && W.polygonArea(L) === 64);
check('convexHull: the corners of a cloud', W.convexHull([[0, 0], [5, 5], [10, 0], [10, 10], [0, 10], [3, 7]]).length === 4);
check('isConvexQuad: a bow tie is refused', W.isConvexQuad(sq) && !W.isConvexQuad([[0, 0], [10, 10], [10, 0], [0, 10]]));

// ---- joints and patterns
check('lineCov: a point on a joint is covered, a point mid tile is not', near(W.lineCov(0.0004, 0.0001, 0.005), 1, 1e-9) && W.lineCov(0.5, 0.0001, 0.005) === 0);
check('lineCov: a pixel wider than many tiles averages to the joint share', near(W.lineCov(0.37, 40, 0.005), 0.005, 1e-3));
check('lineCov: a pixel twice the joint width is half covered', near(W.lineCov(0.0025, 0.01, 0.005), 0.5, 1e-9));
const tile = W.makePattern({ tex: 'tile', w: 60, h: 60, g: 0.3, a: '#D9DBD6', b: '#BFC3BD' }), o = [0, 0, 0];
const lum = (c) => 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
const mid = lum(tile(30, 30, 0.05, 0.05, o).slice()), seam = lum(tile(60, 30, 0.05, 0.05, o).slice());
check('tile pattern: the joint between two 60 cm tiles is darker than the tile', seam < mid * 0.8, { mid: +mid.toFixed(3), seam: +seam.toFixed(3) });
let sumFar = 0, sumNear = 0;
for (let k = 0; k < 400; k++) { const u = W.hash(k, 1) * 600, v = W.hash(k, 2) * 600; sumFar += lum(tile(u, v, 120, 120, o)); }
for (let k = 0; k < 20000; k++) { const u = W.hash(k, 3) * 600, v = W.hash(k, 4) * 600; sumNear += lum(tile(u, v, 0.05, 0.05, o)); }
check('tile pattern: seen from far away it averages to the same tone (no shimmer, within 4%)', near(sumFar / 400, sumNear / 20000, (sumNear / 20000) * 0.04), { far: +(sumFar / 400).toFixed(4), near: +(sumNear / 20000).toFixed(4) });
const wood = W.makePattern({ tex: 'wood', pw: 19, pl: 160, a: '#B98F5E', b: '#8E6A41' });
const wa = lum(wood(80, 9, 0.05, 0.05, o).slice()), ws = lum(wood(80, 19, 0.02, 0.02, o).slice());
check('wood pattern: the long joint between boards is darker', ws < wa * 0.75, { board: +wa.toFixed(3), joint: +ws.toFixed(3) });
for (const tex of ['terrazzo', 'concrete', 'deck']) {
  const p = W.makePattern({ tex, w: 60, a: '#D8D2C8', b: '#6E7B85' });
  let ok = true;
  for (let k = 0; k < 500; k++) { const c = p(W.hash(k, 9) * 500, W.hash(k, 8) * 500, W.hash(k, 7) * 30, W.hash(k, 6) * 30, o); if (!c.every((v) => isFinite(v) && v >= 0 && v < 1.5)) ok = false; }
  check('pattern ' + tex + ': finite colours at every distance', ok);
}

// ---- the light is kept
const w = 64, h = 48, n2 = w * h, Lm = new Float32Array(n2), mask = new Uint8Array(n2);
for (let y = 0; y < h; y++) for (let xx = 0; xx < w; xx++) { const i = y * w + xx; mask[i] = y > 16 ? 255 : 0; Lm[i] = y > 16 ? (xx > 20 && xx < 36 && y > 26 && y < 40 ? 0.6 : 0.2) + ((xx % 8) === 0 ? -0.08 : 0) : 0.9; }
const { light, ref } = W.floorLight(Lm, mask, w, h, 3);
check('floorLight: the sun patch stays brighter than the floor around it', light[33 * w + 28] > light[33 * w + 8] * 2, { patch: +light[33 * w + 28].toFixed(3), around: +light[33 * w + 8].toFixed(3) });
check('floorLight: the bright wall above does not leak into the floor', light[18 * w + 8] < 0.3, light[18 * w + 8]);
check('floorLight: the typical floor brightness is the plain floor', near(ref, 0.19, 0.03), ref);
const out = new Uint8ClampedArray(n2 * 4).fill(128);
const Hfl = W.homography([[0, 17], [w, 17], [w, h], [0, h]], [[0, 0], [400, 0], [400, 200], [0, 200]]);
W.renderFloor({ out, w, h, mask, light, ref, H: Hfl, pattern: tile, grain: 0 });
check('renderFloor: the wall pixels are untouched', out[(5 * w + 5) * 4] === 128 && out[(10 * w + 40) * 4 + 2] === 128);
const pl = (xx, y) => 0.2126 * out[(y * w + xx) * 4] + 0.7152 * out[(y * w + xx) * 4 + 1];
check('renderFloor: the floor under the sun patch is brighter than the floor beside it', pl(28, 33) > pl(10, 33) * 1.15, { patch: Math.round(pl(28, 33)), beside: Math.round(pl(10, 33)) });
const wm = new Uint8Array(n2).fill(0); for (let i = 0; i < w * 16; i++) wm[i] = 255;
const wo = new Uint8ClampedArray(n2 * 4).fill(200), Lw = new Float32Array(n2).fill(0.5); Lw[3 * w + 3] = 0.25;
W.paintWall({ out: wo, mask: wm, L: Lw, ref: 0.5, color: W.hexToLinear('#A8B5A0'), n: n2 });
check('paintWall: a wall pixel takes the colour, a darker pixel stays darker', wo[(2 * w + 2) * 4 + 1] === 181 && wo[(3 * w + 3) * 4 + 1] < 150 && wo[(30 * w + 3) * 4] === 200, [wo[(2 * w + 2) * 4], wo[(2 * w + 2) * 4 + 1], wo[(2 * w + 2) * 4 + 2]]);

// ---- real tile size when a width is given
const pix = (X) => cam.project([X, 400, 0])[0];
const tilePx = pix(210 + 60) - pix(210), wallPx = pix(420) - pix(0);
check('size: with a width of 420 cm, a 60 cm tile takes 60/420 of the width at the same depth', near(tilePx / wallPx, 60 / 420, 1e-9));
const uvA = W.apply(fr.H, pix(210), cam.project([210, 400, 0])[1]), uvB = W.apply(fr.H, pix(270), cam.project([270, 400, 0])[1]);
check('size: the floor frame measures that tile as 60 cm (< 0.01 cm)', near(uvB[0] - uvA[0], 60, 0.01), uvB[0] - uvA[0]);
check('colour: sRGB round trip of every byte', Array.from({ length: 256 }, (_, i) => W.linearToSrgb(W.srgbToLinear(i)) === i).every(Boolean));

console.log('\n' + (n - fails) + ' of ' + n + ' passed');
process.exit(fails ? 1 : 0);
