// HAD-803 climate lab: the sun, the wind and the rain inside one apartment. LAB ONLY: nothing here is loaded by the live site.
// It works on the lab's own copy of the designer (./designer/), whose space.js hands over the 3D scene (space.lab).
// Sun: the NOAA solar position equations for the site, by date and Israel time. Light patches are real shadows of the plan's
// walls and the floor slab above; the numbers (hours of direct sun, how deep it reaches) are traced on the plan the same way.
// Wind and rain: directions from published sources (see SOURCES); drawn as an illustration of direction and path, not a
// calculation of air flow.
import { route, nearestFree } from './designer/walknav.js';

export const SITE = { name_he: 'שדה דב, תל אביב', lat: 32.10, lon: 34.785 };

export const SOURCES = [
  { id: 'noaa', he: 'מיקום השמש: משוואות NOAA (Solar Calculator), חישוב מלא לפי תאריך, שעה, קו רוחב ואורך', url: 'https://gml.noaa.gov/grad/solcalc/calcdetails.html' },
  { id: 'ims-bg', he: 'רוח לפי עונה ושעה: השירות המטאורולוגי, סיכום אקלים תעופתי נמל התעופה בן גוריון, תצפיות 1999 עד 2009 (התחנה כ-16 ק״מ מהחוף)', url: 'https://ims.gov.il/themes/imst/ims/static-files/climate_airport_ben_gurion.pdf' },
  { id: 'ba-2018', he: 'רוח בסערות חורף: ברקוביץ ואלפרט, אוניברסיטת תל אביב, The Open Atmospheric Science Journal 2018, תחנת בית דגן 1974 עד 2012', url: 'https://tau.ac.il/~pinhas/papers/2018/TOASCJ-12-80.pdf' },
];

// Wind cases, each a range of directions the wind comes FROM (compass degrees), with the source's own words.
export const WIND = {
  'summer-noon': { he: 'קיץ, צהריים ואחר הצהריים', from: [270, 315], kn: '10 עד 15 קשר', src: 'ims-bg', note: 'בריזת ים ממערב עד צפון-מערב, מתחזקת אחר הצהריים' },
  'summer-night': { he: 'קיץ, סוף הלילה ובוקר', from: [135, 180], kn: 'רוח קלה', src: 'ims-bg', note: 'בריזת יבשה קלה מדרום-מזרח עד דרום' },
  'winter-noon': { he: 'חורף, צהריים', from: [255, 285], kn: '', src: 'ims-bg', note: 'נטייה לרוח מערבית בצהריים, פחות קבועה מבקיץ' },
  'winter-night': { he: 'חורף, לילה ובוקר', from: [135, 180], kn: '', src: 'ims-bg', note: 'נטייה לרוח מדרום-מזרח עד דרום' },
};
// A winter storm: south-west while the low approaches, then west and north-west once it has passed east of Israel.
export const STORM = [
  { t: 0, from: 225, he: 'הסערה מתקרבת: רוח דרום-מערבית' },
  { t: 0.5, from: 270, he: 'החזית עוברת: רוח מערבית' },
  { t: 1, from: 305, he: 'אחרי החזית: רוח צפון-מערבית' },
];
export const MARKS = [ // the days marked on the year slider
  { m: 3, d: 20, he: 'השוויון האביבי' }, { m: 6, d: 21, he: 'היום הארוך' }, { m: 9, d: 23, he: 'השוויון הסתווי' }, { m: 12, d: 21, he: 'היום הקצר' },
];

// ---------------------------------------------------------------- astronomy ----------------------------------------------------------------
const rad = Math.PI / 180, deg = 180 / Math.PI;
/** NOAA solar position. Returns azimuth (compass degrees, clockwise from north) and altitude (degrees, refraction included). */
export function solar(utcMs, lat = SITE.lat, lon = SITE.lon) {
  const jd = utcMs / 86400000 + 2440587.5, T = (jd - 2451545) / 36525;
  const L0 = (280.46646 + T * (36000.76983 + T * 0.0003032)) % 360;
  const Mg = 357.52911 + T * (35999.05029 - 0.0001537 * T);
  const e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T);
  const C = Math.sin(Mg * rad) * (1.914602 - T * (0.004817 + 0.000014 * T)) + Math.sin(2 * Mg * rad) * (0.019993 - 0.000101 * T) + Math.sin(3 * Mg * rad) * 0.000289;
  const om = 125.04 - 1934.136 * T, lam = L0 + C - 0.00569 - 0.00478 * Math.sin(om * rad);
  const eps0 = 23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60) / 60, eps = eps0 + 0.00256 * Math.cos(om * rad);
  const decl = Math.asin(Math.sin(eps * rad) * Math.sin(lam * rad));
  const y = Math.tan((eps / 2) * rad) ** 2;
  const eot = 4 * deg * (y * Math.sin(2 * L0 * rad) - 2 * e * Math.sin(Mg * rad) + 4 * e * y * Math.sin(Mg * rad) * Math.cos(2 * L0 * rad) - 0.5 * y * y * Math.sin(4 * L0 * rad) - 1.25 * e * e * Math.sin(2 * Mg * rad));
  const d = new Date(utcMs), mins = d.getUTCHours() * 60 + d.getUTCMinutes() + d.getUTCSeconds() / 60;
  let tst = (mins + eot + 4 * lon) % 1440; if (tst < 0) tst += 1440;
  const ha = tst / 4 - 180, la = lat * rad;
  const cz = Math.min(1, Math.max(-1, Math.sin(la) * Math.sin(decl) + Math.cos(la) * Math.cos(decl) * Math.cos(ha * rad)));
  const zen = Math.acos(cz) * deg;
  let az = (Math.atan2(Math.sin(ha * rad), Math.cos(ha * rad) * Math.sin(la) - Math.tan(decl) * Math.cos(la)) * deg + 180) % 360;
  let alt = 90 - zen;
  if (alt < 85) { // atmospheric refraction, NOAA's piecewise fit (arc seconds)
    const te = Math.tan(alt * rad);
    const r = alt > 5 ? 58.1 / te - 0.07 / te ** 3 + 0.000086 / te ** 5 : alt > -0.575 ? 1735 + alt * (-518.2 + alt * (103.4 + alt * (-12.79 + alt * 0.711))) : -20.774 / te;
    alt += r / 3600;
  }
  return { az, alt, decl: decl * deg };
}
/** minutes Israel time is ahead of UTC on a given instant (summer time included), from the browser's own time-zone table */
export function ilOffset(utcMs) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Jerusalem', hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }).formatToParts(new Date(utcMs)).map((x) => [x.type, x.value]));
  return (Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute) - Math.floor(utcMs / 60000) * 60000) / 60000;
}
/** the UTC instant of an Israel local day (year, month 1-12, day) and minute of the day */
export function ilToUtc(y, m, d, minute) {
  let u = Date.UTC(y, m - 1, d, 0, 0) + minute * 60000 - 120 * 60000;
  for (let i = 0; i < 2; i++) u = Date.UTC(y, m - 1, d, 0, 0) + minute * 60000 - ilOffset(u) * 60000;
  return u;
}
export const compassHe = (a) => ['צפון', 'צפון-מזרח', 'מזרח', 'דרום-מזרח', 'דרום', 'דרום-מערב', 'מערב', 'צפון-מערב'][Math.round((((a % 360) + 360) % 360) / 45) % 8];

// ---------------------------------------------------------------- the plan ----------------------------------------------------------------
const pip = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const a = poly[i], b = poly[j]; if ((a[1] > p[1]) !== (b[1] > p[1]) && p[0] < ((b[0] - a[0]) * (p[1] - a[1])) / (b[1] - a[1]) + a[0]) c = !c; } return c; };
/** plan vector (x right, y down) of a compass bearing, given the sheet's north (the bearing of plan up) */
export const planDir = (bearing, north) => { const t = (bearing - north) * rad; return [Math.sin(t), -Math.cos(t)]; };
export const bearingOf = (v, north) => (((Math.atan2(v[0], -v[1]) * deg + north) % 360) + 360) % 360;

/** what the climate needs from the plan: rooms with floor samples, the walls a ray of light meets, the openings in the facade */
export function readPlan(store) {
  const dv = store.derived, apt = store.apt, north = apt.north_deg || 0, H = apt.levels[0].height;
  const faces = dv.faces.filter((f) => f.room), inner = faces.filter((f) => f.room.type !== 'balcony');
  const walls = dv.walls.filter((w) => w.kind !== 'divider' && w.L >= 1);
  const env = [];
  for (const w of walls) {
    if (w.kind !== 'facade') continue;
    for (const o of w.openings || []) {
      if (o.type === 'door') continue; // the front door opens to the stair hall: closed for light and air
      const s = o.at + o.w / 2, c = [w.pa[0] + w.dir[0] * s, w.pa[1] + w.dir[1] * s];
      let n = [-w.dir[1], w.dir[0]];
      if (inner.some((f) => pip([c[0] + n[0] * 30, c[1] + n[1] * 30], f.poly))) n = [-n[0], -n[1]];
      const room = inner.find((f) => pip([c[0] - n[0] * 30, c[1] - n[1] * 30], f.poly)) || null;
      const a = [w.pa[0] + w.dir[0] * o.at, w.pa[1] + w.dir[1] * o.at], b = [w.pa[0] + w.dir[0] * (o.at + o.w), w.pa[1] + w.dir[1] * (o.at + o.w)];
      const toBalcony = faces.some((f) => f.room.type === 'balcony' && pip([c[0] + n[0] * 60, c[1] + n[1] * 60], f.poly));
      env.push({ id: o.id, type: o.type, w, o, c, n, a, b, width: o.w, sill: o.sill || 0, head: o.head || 210, room, toBalcony, bearing: bearingOf(n, north) });
    }
  }
  const rooms = inner.map((f) => {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const p of f.poly) { x0 = Math.min(x0, p[0]); y0 = Math.min(y0, p[1]); x1 = Math.max(x1, p[0]); y1 = Math.max(y1, p[1]); }
    const pts = [], step = 40;
    for (let y = y0 + step / 2; y < y1; y += step) for (let x = x0 + step / 2; x < x1; x += step) if (pip([x, y], f.poly)) pts.push([x, y]);
    return { id: f.id, face: f, type: f.room.type, name_he: f.room.name_he, net: f.net, pts, wins: env.filter((e) => e.room === f) };
  });
  return { north, H, faces, inner, walls, env, rooms };
}

/** does a ray from a plan point at height z0 (cm) toward the sun leave the apartment without meeting a wall, a closed door or the
 *  slab of the floor above (which also covers the balcony: we assume the same balcony one floor up)? */
export function sunReaches(P, z0, sun, plan) {
  if (sun.alt <= 0) return false;
  const d = planDir(sun.az, plan.north), t = Math.tan(sun.alt * rad), hits = [];
  for (const w of plan.walls) {
    const ex = w.pb[0] - w.pa[0], ey = w.pb[1] - w.pa[1], den = d[0] * ey - d[1] * ex;
    if (Math.abs(den) < 1e-9) continue;
    const qx = w.pa[0] - P[0], qy = w.pa[1] - P[1];
    const s = (qx * ey - qy * ex) / den, u = (qx * d[1] - qy * d[0]) / den;
    if (s > 0.5 && u >= -0.001 && u <= 1.001) hits.push([s, w, u * w.L]);
  }
  hits.sort((a, b) => a[0] - b[0]);
  for (const [s, w, u] of hits) {
    const h = z0 + s * t;
    if (h >= plan.H) return false; // the ceiling slab, inside or above the balcony
    if (w.kind === 'rail') continue; // a balcony railing (taken as glass or open bars)
    const o = (w.openings || []).find((q) => u >= q.at - 1 && u <= q.at + q.w + 1);
    const open = o && (o.type !== 'door' || w.kind === 'partition');
    if (!open || h < (o.sill || 0) || h > (o.head || 210)) return false;
  }
  return true;
}

/** per room on one day: minutes of direct sun on the floor (any of it, at least 3% of the floor), and the first and last sunny time */
export function sunDay(plan, y, m, d, stepMin = 10) {
  const out = Object.fromEntries(plan.rooms.map((r) => [r.id, { minutes: 0, first: null, last: null, peak: 0 }]));
  for (let min = 240; min <= 1230; min += stepMin) {
    const s = solar(ilToUtc(y, m, d, min));
    if (s.alt <= 0.5) continue;
    for (const r of plan.rooms) {
      if (!r.wins.length || !r.pts.length) continue;
      let lit = 0; for (const p of r.pts) if (sunReaches(p, 5, s, plan)) lit++;
      const f = lit / r.pts.length, o = out[r.id];
      if (f >= 0.03) { o.minutes += stepMin; if (o.first == null) o.first = min; o.last = min; }
      o.peak = Math.max(o.peak, f);
    }
  }
  return out;
}
/** the sunset from inside, month by month (the 15th): the Israel time the sun sets, where it sets, and the rooms from which a person
 *  standing (eye 160 cm) sees the low sun through a window in the last half hour. Neighbouring towers are NOT in the model. */
export function sunsetYear(plan, y = 2026) {
  const out = [];
  for (let m = 1; m <= 12; m++) {
    let set = null; for (let min = 900; min <= 1290; min += 2) if (solar(ilToUtc(y, m, 15, min)).alt <= 0.5) { set = min; break; }
    const rooms = new Set(), az = solar(ilToUtc(y, m, 15, set)).az;
    for (const back of [6, 16, 30]) {
      const s = solar(ilToUtc(y, m, 15, set - back));
      for (const r of plan.rooms) if (r.wins.length && !rooms.has(r) && r.pts.some((p) => sunReaches(p, 160, s, plan))) rooms.add(r);
    }
    out.push({ m, set, az, rooms: [...rooms] });
  }
  return out;
}
/** the balcony railings that face a wind direction (rain driven onto the balcony floor) */
export function balconyRain(plan, from) {
  const vT = planDir((from + 180) % 360, plan.north), bal = plan.faces.filter((f) => f.room.type === 'balcony');
  return plan.walls.filter((w) => w.kind === 'rail').filter((w) => {
    const c = [(w.pa[0] + w.pb[0]) / 2, (w.pa[1] + w.pb[1]) / 2]; let n = [-w.dir[1], w.dir[0]];
    if (bal.some((f) => pip([c[0] + n[0] * 30, c[1] + n[1] * 30], f.poly))) n = [-n[0], -n[1]]; // outward, away from the balcony floor
    return n[0] * -vT[0] + n[1] * -vT[1] > 0.17;
  });
}
/** which way a wind case moves the air through a window: 'in', 'out' or null */
export function windAt(plan, key, e) {
  const w = WIND[key], vT = planDir(((w.from[0] + w.from[1]) / 2 + 180) % 360, plan.north), k = e.n[0] * vT[0] + e.n[1] * vT[1];
  return k < -0.2 ? 'in' : k > 0.2 ? 'out' : null;
}
/** right now: the lit share of each room's floor and how far in from its window the sun reaches (cm) */
export function sunNow(plan, sun) {
  const out = {};
  for (const r of plan.rooms) {
    let lit = 0, deep = 0;
    for (const p of r.pts) if (sunReaches(p, 5, sun, plan)) {
      lit++;
      for (const e of r.wins) { const dd = Math.abs((p[0] - e.c[0]) * e.n[0] + (p[1] - e.c[1]) * e.n[1]); deep = Math.max(deep, dd); }
    }
    out[r.id] = { share: r.pts.length ? lit / r.pts.length : 0, deep: lit ? deep : 0 };
  }
  return out;
}

// ---------------------------------------------------------------- the scene ----------------------------------------------------------------
/**
 * mountClimate(space, store, opts) -> controller. space = the lab designer's space (with .lab), store = the designer's store.
 * The controller: setDate(y,m,d), setMinute(min), setMode('sun'|'wind'|'rain'), setWind(key), setStorm(0..1), state(), step(dt).
 */
export function mountClimate(space, store, opts = {}) {
  const L = space.lab, { THREE, scene, M, mid } = L, plan = readPlan(store), H = plan.H;
  const st = { y: 2026, m: 12, d: 21, minute: 9 * 60, mode: 'sun', wind: 'summer-noon', storm: 0.3, manual: !!opts.manual, t: 0, sun: null };

  // the slab of the floor above, over the rooms and the balcony: invisible, it only casts the shadow a real ceiling casts
  const slab = new THREE.Group();
  {
    const m = new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false, side: THREE.DoubleSide }); m.shadowSide = THREE.DoubleSide;
    for (const f of plan.faces) {
      const sh = new THREE.Shape(f.poly.map((p) => new THREE.Vector2(p[0] * M, p[1] * M)));
      const g = new THREE.ShapeGeometry(sh); g.rotateX(Math.PI / 2);
      const mesh = new THREE.Mesh(g, m); mesh.position.y = H * M + 0.005; mesh.castShadow = true; mesh.receiveShadow = false; mesh.renderOrder = -1; slab.add(mesh);
    }
    scene.add(slab);
  }
  // the sea to the west of Sde Dov, in place of the generic city on that side (an illustration, like the rest of the view)
  {
    const low = -26, coast = planDir(20, plan.north), toSea = planDir(290, plan.north);
    const sea = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshPhysicalMaterial({ color: 0x1B4A66, roughness: 0.12, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.08, envMapIntensity: 1.2 }));
    sea.rotation.x = -Math.PI / 2; sea.rotation.z = -Math.atan2(coast[1], coast[0]);
    sea.position.set(mid.x + toSea[0] * (55 + 200) , low + 0.06, mid.z + toSea[1] * (55 + 200)); L.outside.add(sea);
    for (const g of L.outside.children) if (g.type === 'Group') for (const b of g.children) { const v = [b.position.x - mid.x, b.position.z - mid.z]; if (v[0] * toSea[0] + v[1] * toSea[1] > 40) b.visible = false; }
  }

  // facade openings: a thin coloured pane just outside each, shown by mode (air in, air out, rain on the glass)
  const panes = new THREE.Group(); scene.add(panes);
  const paneMat = { in: new THREE.MeshBasicMaterial({ color: 0x0B7285, transparent: true, opacity: 0.34, side: THREE.DoubleSide, depthWrite: false }),
    out: new THREE.MeshBasicMaterial({ color: 0x66C2D0, transparent: true, opacity: 0.30, side: THREE.DoubleSide, depthWrite: false }),
    rain: new THREE.MeshBasicMaterial({ color: 0x3B4CC0, transparent: true, opacity: 0.38, side: THREE.DoubleSide, depthWrite: false }) };
  for (const e of plan.env) {
    const g = new THREE.PlaneGeometry(e.width * M, (e.head - e.sill) * M), mesh = new THREE.Mesh(g, paneMat.in);
    const off = (e.w.t || 25) / 2 + 2; mesh.position.set((e.c[0] + e.n[0] * off) * M, ((e.sill + e.head) / 2) * M, (e.c[1] + e.n[1] * off) * M);
    mesh.rotation.y = -Math.atan2(e.w.dir[1], e.w.dir[0]); mesh.visible = false; mesh.userData.env = e; panes.add(mesh);
  }

  // streaks: one instanced thin rod per particle (wind lines and rain drops)
  const rod = (n, r, len, color, op) => {
    const g = new THREE.CylinderGeometry(r, r, len, 5, 1, true); g.rotateZ(Math.PI / 2); // along +x
    const mm = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: op, depthWrite: false });
    const im = new THREE.InstancedMesh(g, mm, n); im.frustumCulled = false; im.visible = false; scene.add(im); return im;
  };
  const windIm = rod(900, 0.012, 0.42, 0x0B7285, 0.9), rainIm = rod(1600, 0.008, 0.3, 0x3B4CC0, 0.85);
  const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpS = new THREE.Vector3(), tmpP = new THREE.Vector3(), X = new THREE.Vector3(1, 0, 0), tmpD = new THREE.Vector3();
  const rnd = (() => { let s = 803; return () => ((s = (s * 16807) % 2147483647) / 2147483647); })();

  // ---- wind paths for the current case ----
  let paths = [], windParts = [], vent = { inlets: [], outlets: [], cross: false, pairs: [] };
  const polyLen = (pts) => { const c = [0]; for (let i = 1; i < pts.length; i++) c.push(c[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1], (pts[i][2] || 0) - (pts[i - 1][2] || 0))); return c; };
  function buildWind() {
    const w = WIND[st.wind], mean = (w.from[0] + w.from[1]) / 2, vT = planDir((mean + 180) % 360, plan.north); // the direction the air travels
    const inlets = plan.env.filter((e) => e.n[0] * -vT[0] + e.n[1] * -vT[1] > 0.2), outlets = plan.env.filter((e) => e.n[0] * vT[0] + e.n[1] * vT[1] > 0.2);
    const nav = L.getNav(); paths = []; const pairs = [];
    const inside = (e, k) => [e.c[0] - e.n[0] * k, e.c[1] - e.n[1] * k];
    for (const a of inlets) {
      let best = null, bs = -Infinity;
      for (const b of outlets) { const sc = (b.c[0] - a.c[0]) * vT[0] + (b.c[1] - a.c[1]) * vT[1]; if (sc > bs) { bs = sc; best = b; } }
      const h = Math.min(Math.max(a.sill + 40, 110), a.head - 30);
      const start = [a.c[0] + a.n[0] * (a.toBalcony ? 420 : 260), a.c[1] + a.n[1] * (a.toBalcony ? 420 : 260), h];
      if (best && bs > 150) {
        const r = nav ? route(nav, inside(a, 70), inside(best, 70)) : null;
        const mid3 = (r || [inside(a, 70), inside(best, 70)]).map((p) => [p[0], p[1], h]);
        const hb = Math.min(Math.max(best.sill + 40, 110), best.head - 30);
        const pts = [start, [a.c[0], a.c[1], h], ...mid3, [best.c[0], best.c[1], hb], [best.c[0] + best.n[0] * 300, best.c[1] + best.n[1] * 300, hb + 40]];
        paths.push({ pts, cum: polyLen(pts), kind: 'cross', a, b: best }); pairs.push([a, best]);
      } else { // one side only: the air comes in a little and turns back out
        const p1 = inside(a, 180), side = [a.w.dir[0] * a.width * 0.3, a.w.dir[1] * a.width * 0.3];
        const pts = [start, [a.c[0] + side[0], a.c[1] + side[1], h], [p1[0] + side[0], p1[1] + side[1], h], [p1[0] - side[0], p1[1] - side[1], h + 20], [a.c[0] - side[0], a.c[1] - side[1], h + 30], [a.c[0] - side[0] + a.n[0] * 260, a.c[1] - side[1] + a.n[1] * 260, h + 60]];
        paths.push({ pts, cum: polyLen(pts), kind: 'single', a });
      }
    }
    // the air passing outside, on both sides of the apartment (context only)
    const perp = [-vT[1], vT[0]], R = L.R / M;
    for (let k = -6; k <= 6; k++) {
      const off = (k / 6) * (R + 900); if (Math.abs(off) < R + 120) continue;
      const c = [mid.x / M + perp[0] * off, mid.z / M + perp[1] * off], z = 60 + ((k + 6) % 4) * 70;
      const pts = [[c[0] - vT[0] * 1500, c[1] - vT[1] * 1500, z], [c[0] + vT[0] * 1500, c[1] + vT[1] * 1500, z]];
      paths.push({ pts, cum: polyLen(pts), kind: 'outside' });
    }
    vent = { inlets, outlets, cross: pairs.length > 0, pairs, vT, mean };
    windParts = [];
    const n = windIm.count;
    for (let i = 0; i < n; i++) {
      const p = paths[i % paths.length]; if (!p) break;
      windParts.push({ p, u: rnd(), sp: (p.kind === 'outside' ? 0.07 : 0.11) * (0.75 + rnd() * 0.5), j: [(rnd() - 0.5) * 70, (rnd() - 0.5) * 50] });
    }
    paintPanes();
  }
  function at(p, u) {
    const L0 = p.cum[p.cum.length - 1], s = u * L0; let i = 1; while (i < p.cum.length - 1 && p.cum[i] < s) i++;
    const a = p.pts[i - 1], b = p.pts[i], f = (s - p.cum[i - 1]) / Math.max(1e-6, p.cum[i] - p.cum[i - 1]);
    return [[a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, (a[2] || 0) + ((b[2] || 0) - (a[2] || 0)) * f], [b[0] - a[0], b[1] - a[1], (b[2] || 0) - (a[2] || 0)]];
  }
  function stepWind(dt) {
    let i = 0;
    for (const q of windParts) {
      q.u += (q.sp * dt * 1000) / q.p.cum[q.p.cum.length - 1] * (q.p.kind === 'outside' ? 6 : 1.6); if (q.u > 1) q.u -= 1;
      const [pos, dir] = at(q.p, q.u), l = Math.hypot(dir[0], dir[1], dir[2]) || 1, perp = [-dir[1] / l, dir[0] / l];
      const fade = Math.min(1, q.u * 8, (1 - q.u) * 8);
      tmpP.set((pos[0] + perp[0] * q.j[0]) * M, (pos[2] + q.j[1]) * M, (pos[1] + perp[1] * q.j[0]) * M);
      tmpD.set(dir[0], dir[2], dir[1]).normalize(); tmpQ.setFromUnitVectors(X, tmpD); tmpS.set(Math.max(0.05, fade), 1, 1);
      tmpM.compose(tmpP, tmpQ, tmpS); windIm.setMatrixAt(i++, tmpM);
    }
    for (; i < windIm.count; i++) { tmpM.makeScale(0, 0, 0); windIm.setMatrixAt(i, tmpM); }
    windIm.instanceMatrix.needsUpdate = true;
  }
  // ---- rain ----
  const drops = []; for (let i = 0; i < rainIm.count; i++) drops.push({ x: (rnd() - 0.5) * 2600, z: (rnd() - 0.5) * 2600, y: rnd() * 1300 - 600 });
  const stormFrom = () => { let a = STORM[0], b = STORM[STORM.length - 1]; for (let i = 1; i < STORM.length; i++) if (st.storm <= STORM[i].t) { a = STORM[i - 1]; b = STORM[i]; break; } const f = (st.storm - a.t) / Math.max(1e-6, b.t - a.t); return a.from + (b.from - a.from) * f; };
  const inFoot = (x, y) => plan.faces.some((f) => pip([x, y], f.poly));
  function stepRain(dt) {
    const vT = planDir((stormFrom() + 180) % 360, plan.north), fall = 750, hor = 420; // cm per second
    tmpD.set(vT[0] * hor, -fall, vT[1] * hor).normalize(); tmpQ.setFromUnitVectors(X, tmpD);
    let i = 0;
    for (const q of drops) {
      q.y -= fall * dt; q.x += vT[0] * hor * dt; q.z += vT[1] * hor * dt;
      if (q.y < -600) { q.y += 1300; q.x = (rnd() - 0.5) * 2600 - vT[0] * 500; q.z = (rnd() - 0.5) * 2600 - vT[1] * 500; }
      const px = mid.x / M + q.x, pz = mid.z / M + q.z, hide = q.y < H + 30 && inFoot(px, pz);
      tmpP.set(px * M, q.y * M, pz * M); tmpS.setScalar(hide ? 0 : 1); tmpM.compose(tmpP, tmpQ, tmpS); rainIm.setMatrixAt(i++, tmpM);
    }
    rainIm.instanceMatrix.needsUpdate = true;
  }
  const rainWindows = () => { const vT = planDir((stormFrom() + 180) % 360, plan.north); return plan.env.filter((e) => e.n[0] * -vT[0] + e.n[1] * -vT[1] > 0.17); };
  function paintPanes() {
    const rw = st.mode === 'rain' ? new Set(rainWindows()) : null;
    for (const mesh of panes.children) {
      const e = mesh.userData.env;
      if (st.mode === 'wind') { const isIn = vent.inlets.includes(e), isOut = vent.outlets.includes(e); mesh.visible = isIn || isOut; mesh.material = isIn ? paneMat.in : paneMat.out; }
      else if (st.mode === 'rain') { mesh.visible = rw.has(e); mesh.material = paneMat.rain; }
      else mesh.visible = false;
    }
  }

  // ---- the sky: three's physical atmosphere (Preetham), the same sun position as the light; it also lights and reflects into
  //      the room (an environment map rebuilt from it a few times a second at most), so a sunset turns the floor and the sea warm ----
  let sky = null, envSky = null, envScene = null, pmrem = null, envTex = null, envAt = 0, envTimer = 0;
  const skyReady = import('three/addons/objects/Sky.js').then(({ Sky }) => {
    const tune = (k) => { const u = k.material.uniforms; u.turbidity.value = 3.2; u.rayleigh.value = 1.4; u.mieCoefficient.value = 0.004; u.mieDirectionalG.value = 0.86; };
    sky = new Sky(); sky.scale.setScalar(340); sky.position.copy(mid); tune(sky); L.outside.add(sky);
    const dome = L.outside.children.find((o) => o.geometry && o.geometry.type === 'SphereGeometry'); if (dome) dome.visible = false;
    envSky = new Sky(); envSky.scale.setScalar(900); tune(envSky); envScene = new THREE.Scene(); envScene.add(envSky);
    pmrem = new THREE.PMREMGenerator(L.renderer);
    applySun();
  }).catch(() => { /* without it the plain sky dome stays */ });
  function rebuildEnv() {
    if (!pmrem) return;
    const now = performance.now();
    if (now - envAt < 280) { clearTimeout(envTimer); envTimer = setTimeout(rebuildEnv, 300); return; }
    envAt = now; const old = envTex; envTex = pmrem.fromScene(envScene, 0, 0.1, 1000).texture; scene.environment = envTex; if (old) old.dispose(); L.touch(true);
  }

  // ---- the sun ----
  const warm = new THREE.Color(0xFFB868), white = new THREE.Color(0xFFE4B8); // the sun's light stays golden inside, as in the board
  // the sun itself in the sky, where it really is (inside the sky dome of radius 180 m, so it is drawn on top of it)
  const disc = new THREE.Mesh(new THREE.SphereGeometry(3.2, 24, 12), new THREE.MeshBasicMaterial({ color: 0xFFE08A, fog: false, depthWrite: false, toneMapped: false }));
  const halo = new THREE.Mesh(new THREE.SphereGeometry(7, 24, 12), new THREE.MeshBasicMaterial({ color: 0xFFD27A, transparent: true, opacity: 0.28, fog: false, depthWrite: false, toneMapped: false }));
  disc.renderOrder = halo.renderOrder = 1; scene.add(disc, halo);
  function applySun() {
    const s = solar(ilToUtc(st.y, st.m, st.d, st.minute)); st.sun = s;
    const d = planDir(s.az, plan.north), ca = Math.cos(Math.max(s.alt, 0.5) * rad);
    L.sun.position.set(mid.x + d[0] * ca * 30, Math.sin(Math.max(s.alt, 0.5) * rad) * 30, mid.z + d[1] * ca * 30); L.sun.target.position.copy(mid); L.sun.target.updateMatrixWorld();
    const day = Math.min(1, Math.max(0, (s.alt + 2) / 14));
    L.sun.intensity = s.alt > 0 ? 8 * Math.min(1, s.alt / 10 + 0.15) : 0; // strong sun, low fill: the patch of sun on the floor must read
    L.sun.color.copy(warm).lerp(white, Math.min(1, Math.max(0, s.alt / 25)));
    { const dd = planDir(s.az, plan.north), c = Math.cos(s.alt * rad), R0 = 150; disc.position.set(mid.x + dd[0] * c * R0, Math.sin(s.alt * rad) * R0 + 1.6, mid.z + dd[1] * c * R0); halo.position.copy(disc.position);
      disc.visible = halo.visible = s.alt > -0.8 && st.mode === 'sun'; disc.material.color.copy(warm).lerp(new THREE.Color(0xFFF6D8), Math.min(1, Math.max(0, s.alt / 20))); }
    L.hemi.intensity = 0.3 + day * 0.28;
    scene.environmentIntensity = sky ? 0.16 + 0.34 * day : 0.07 + 0.15 * day;
    if (sky) { const v = new THREE.Vector3(d[0] * Math.cos(s.alt * rad), Math.sin(s.alt * rad), d[1] * Math.cos(s.alt * rad));
      sky.material.uniforms.sunPosition.value.copy(v); envSky.material.uniforms.sunPosition.value.copy(v); L.renderer.toneMappingExposure = 1.0; rebuildEnv(); }
    const dome = L.outside.children.find((o) => o.geometry && o.geometry.type === 'SphereGeometry');
    if (dome) { const k = 0.18 + 0.82 * day; dome.material.color.setRGB(k * (0.85 + 0.15 * day), k * (0.9 + 0.1 * day), k); }
    L.touch(true);
  }

  // ---- public ----
  function setMode(m) {
    st.mode = m; windIm.visible = m === 'wind'; rainIm.visible = m === 'rain';
    if (m === 'wind') buildWind(); else paintPanes();
    if (m !== 'sun') disc.visible = halo.visible = false;
    if (m === 'rain') { L.sun.intensity = 0.25; L.hemi.intensity = space.mode === 'walk' ? 0.7 : 0.4; L.touch(true); } else applySun();
  }
  let last = performance.now(), raf = 0;
  function step(dt) {
    st.t += dt;
    if (st.mode === 'wind') stepWind(dt);
    if (st.mode === 'rain') stepRain(dt);
    if (st.mode !== 'sun') L.touch(false);
    opts.onFrame && opts.onFrame(api);
  }
  function loop(now) { const dt = Math.min(0.05, (now - last) / 1000); last = now; if (!st.manual) step(dt); raf = requestAnimationFrame(loop); }
  raf = requestAnimationFrame(loop);
  const dayCache = new Map();
  const api = {
    plan, st, SOURCES, WIND, STORM, MARKS, skyReady,
    setDate(y, m, d) { st.y = y; st.m = m; st.d = d; if (st.mode === 'sun') applySun(); },
    setMinute(min) { st.minute = min; if (st.mode === 'sun') applySun(); },
    setMode, setWind(k) { st.wind = k; if (st.mode === 'wind') buildWind(); }, setStorm(v) { st.storm = v; if (st.mode === 'rain') paintPanes(); },
    stormFrom, rainWindows, vent: () => vent,
    sun: () => st.sun || solar(ilToUtc(st.y, st.m, st.d, st.minute)),
    now: () => sunNow(plan, st.sun || solar(ilToUtc(st.y, st.m, st.d, st.minute))),
    day(y, m, d) { const k = y + '-' + m + '-' + d; if (!dayCache.has(k)) dayCache.set(k, sunDay(plan, y, m, d)); return dayCache.get(k); },
    /** compass bearing the camera looks at (for the ring) */
    heading() { const v = space.getView(); return bearingOf([Math.cos(v.yaw), Math.sin(v.yaw)], plan.north); },
    manual(on) { st.manual = !!on; }, step,
    destroy() { cancelAnimationFrame(raf); },
  };
  applySun();
  return api;
}
