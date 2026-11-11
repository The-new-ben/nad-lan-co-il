// "Measure with the camera" (מדידה במצלמה): on Chrome for Android a person walks through the apartment, points the phone at
// every corner on the floor line, presses "corner", goes from room to room, and gets a plan in real centimetres. No install.
//
//   import { scanSupported, mountRoomScan } from '.../assets/designer/roomscan.js';
//   const s = await scanSupported();                  // { ok, why: null | 'https' | 'noxr' | 'noar' }
//   const scan = await mountRoomScan(host, { lang, version, onDone(result), onCancel() });
//   scan.destroy();
//
// result = roomsToSegments(...) from roomgeom.js plus meta: { points, rooms, seconds, anchored }.
//   result.segments  -> planmaker's pm.propose({ segments: result.segments, cmPerPx: 1 })   (walls only)
//   result.draft     -> mountPlanMaker(host, { draft: result.draft, ... })                  (walls, doors, windows, names)
//
// WebXR use: an 'immersive-ar' session with 'hit-test' and 'dom-overlay' (required) and 'anchors' (optional). The camera
// picture is composed by the browser itself and never reaches this page: nothing is recorded, stored or sent.
// The explanation and the result screens draw inside a shadow root under `host`; while measuring, the controls live in
// one element directly under document.body (the DOM overlay root, classes nlscan-*), removed when the session ends.
// three.js comes from the page's import map; it is fetched only on a device that can measure, while the person reads.
import { snapCorner, closeRoom, worldToPlan, roomsToSegments, ROOM_CHOICES, segDist } from './roomgeom.js';

const BASE = new URL('.', import.meta.url).href;
const FONTS = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&display=swap';
const C = { sheet: '#F2F5F7', grid: '#DCE4E9', ink: '#0F2233', ink2: '#46596A', blue: '#1F5FA8', blue2: '#D6E5F6', dim: '#B5302A', rail: '#9FB2C0', line: '#B9C6CF' };
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const TX = {
  he: {
    dir: 'rtl', title: 'מודדים את הדירה במצלמה',
    steps: ['מכוונים את הטלפון לרצפה עד שמופיע סימון', 'מכוונים לכל פינה של החדר, על קו הרצפה, ולוחצים פינה', 'עוברים לחדר הבא וממשיכים. בסוף לוחצים סיום והתוכנית נפתחת'],
    works: 'עובד בכרום באנדרואיד. צריך אור טוב.', privacy: 'הצילום נשאר במכשיר. שום תמונה לא נשמרת ולא נשלחת.',
    start: 'להתחיל מדידה', back: 'חזרה', retry: 'לנסות שוב', starting: 'פותחים את המצלמה',
    why: {
      https: 'המדידה במצלמה עובדת רק בחיבור מאובטח לאתר.',
      noxr: 'בדפדפן הזה המדידה במצלמה לא זמינה. היא עובדת בכרום בטלפון אנדרואיד.',
      noar: 'המכשיר הזה לא תומך במדידה במצלמה. היא עובדת ברוב טלפוני האנדרואיד החדשים, בכרום.',
      nofeature: 'במכשיר הזה חסר רכיב שהמדידה צריכה. אפשר לנסות בטלפון אנדרואיד אחר, בכרום.',
      denied: 'לא התקבל אישור להשתמש במצלמה. אפשר לאשר ולנסות שוב.',
      failed: 'המצלמה לא נפתחה הפעם. אפשר לנסות שוב.',
    },
    whyHead: 'כאן המדידה במצלמה לא תעבוד', whyAlt: 'בינתיים אפשר לשרטט את הדירה ידנית לפי מידות.',
    corner: 'פינה', mark: 'סימון', undo: 'ביטול', close: 'סגירת חדר', door: 'דלת', window: 'חלון', finish: 'סיום', exit: 'יציאה', square: 'זווית ישרה',
    m: 'מ׳', sqm: 'מ״ר', cm: 'ס״מ',
    aimFloor: 'מכוונים את הטלפון לרצפה ומזיזים אותו לאט עד שמופיע סימון',
    first: 'מכוונים לפינה הראשונה של החדר, על קו הרצפה, ולוחצים פינה',
    next: 'ממשיכים לפינה הבאה, מסביב לחדר. אחרי הפינה האחרונה לוחצים סגירת חדר',
    hold: 'מחזיקים את הטלפון יציב רגע', notFloor: 'זה לא הרצפה. מכוונים לקו שבין הקיר לרצפה',
    lost: 'הזיזו את הטלפון לאט, ליד משהו עם פרטים',
    closing: 'הסימון על הפינה הראשונה. לוחצים סגירת חדר',
    saved: 'החדר נשמר. עוברים לחדר הבא ומסמנים את הפינה הראשונה שלו',
    doorA: 'דלת: מכוונים לצד אחד של הפתח, על קו הרצפה, ולוחצים סימון', doorB: 'עכשיו לצד השני של הפתח, ולוחצים סימון',
    winA: 'חלון: מכוונים לרצפה מתחת לצד אחד של החלון, ולוחצים סימון', winB: 'עכשיו מתחת לצד השני של החלון, ולוחצים סימון',
    openSaved: (d) => (d ? 'הדלת נשמרה' : 'החלון נשמר'),
    few: 'צריך לפחות שלוש פינות כדי לסגור חדר', cross: 'הקווים של החדר נחתכים. אפשר לבטל את הפינה האחרונה ולסמן שוב',
    small: 'החדר יצא קטן מדי. אפשר לבטל ולסמן שוב', nothing: 'עדיין לא נמדד אף חדר', openFirst: 'קודם מודדים חדר, ואז מסמנים בו דלתות וחלונות',
    exitAgain: 'לוחצים שוב על יציאה כדי לצאת בלי לשמור', squareOn: 'זווית ישרה פועלת', squareOff: 'זווית ישרה כבויה',
    namesHead: 'איך קוראים לחדר?', skip: 'דילוג',
    count: (n, k) => 'חדר ' + n + ' · ' + (k === 1 ? 'פינה אחת' : k + ' פינות'),
    rooms: (n) => (n === 1 ? 'חדר אחד' : n + ' חדרים'), room: 'חדר',
    resHead: 'התוכנית מוכנה', resArea: 'שטח רצפה',
    truth: 'המידות נמדדו במצלמה ויכולות לסטות בכמה סנטימטרים. לפני שמזמינים רהיט או מטבח מודדים שוב את הקיר הקובע.',
    go: 'להמשיך לתיקון ולתלת ממד', again: 'למדוד שוב', none: 'לא נסגר אף חדר, אז אין עדיין תוכנית. אפשר למדוד שוב.',
    warn: {
      'room.alone': (n) => (n || 'חדר') + ': לא נמצא קיר משותף עם חדר אחר. אם יש ביניהם קיר, מתקנים בשרטוט.',
      'room.overlap': () => 'שני חדרים נמדדו זה על זה. כדאי לבדוק אותם בשרטוט.',
      'room.few': () => 'חדר שלא נסגר לא נכנס לתוכנית.', 'room.small': () => 'חדר קטן מדי לא נכנס לתוכנית.',
      'room.cross': () => 'חדר שהקווים שלו נחתכים לא נכנס לתוכנית.', 'room.shape': (n) => (n || 'חדר') + ': הצורה נשארה כפי שנמדדה.',
      'opening.off': () => 'דלת או חלון שסומנו רחוק מקיר לא נכנסו.', 'opening.narrow': () => 'פתח צר מ-30 ס״מ לא נכנס.',
      'open.dropped': () => 'הפינות של החדר האחרון שלא נסגר לא נכנסו.',
    },
  },
  en: {
    dir: 'ltr', title: 'Measure the apartment with the camera',
    steps: ['Point the phone at the floor until a marker appears', 'Aim at each corner of the room, on the floor line, and press Corner', 'Move to the next room and carry on. At the end press Finish and the plan opens'],
    works: 'Works in Chrome on Android. Needs good light.', privacy: 'The camera view stays on the device. No picture is kept or sent.',
    start: 'Start measuring', back: 'Back', retry: 'Try again', starting: 'Opening the camera',
    why: {
      https: 'Measuring with the camera works only over a secure connection to the site.',
      noxr: 'Measuring with the camera is not available in this browser. It works in Chrome on an Android phone.',
      noar: 'This device does not support measuring with the camera. It works on most recent Android phones, in Chrome.',
      nofeature: 'This device lacks a part the measurement needs. You can try another Android phone, in Chrome.',
      denied: 'Permission to use the camera was not given. You can allow it and try again.',
      failed: 'The camera did not open this time. You can try again.',
    },
    whyHead: 'Measuring with the camera will not work here', whyAlt: 'Meanwhile you can draw the apartment by hand from measurements.',
    corner: 'Corner', mark: 'Mark', undo: 'Undo', close: 'Close room', door: 'Door', window: 'Window', finish: 'Finish', exit: 'Exit', square: 'Right angle',
    m: 'm', sqm: 'm²', cm: 'cm',
    aimFloor: 'Point the phone at the floor and move it slowly until a marker appears',
    first: 'Aim at the first corner of the room, on the floor line, and press Corner',
    next: 'Go on to the next corner, around the room. After the last corner press Close room',
    hold: 'Hold the phone still for a moment', notFloor: 'That is not the floor. Aim at the line where the wall meets the floor',
    lost: 'Move the phone slowly, near something with detail',
    closing: 'The marker is on the first corner. Press Close room',
    saved: 'Room saved. Go to the next room and mark its first corner',
    doorA: 'Door: aim at one side of the opening, on the floor line, and press Mark', doorB: 'Now the other side of the opening, and press Mark',
    winA: 'Window: aim at the floor under one side of the window and press Mark', winB: 'Now under the other side of the window, and press Mark',
    openSaved: (d) => (d ? 'Door saved' : 'Window saved'),
    few: 'A room needs at least three corners', cross: 'The room lines cross. Undo the last corner and mark it again',
    small: 'The room came out too small. Undo and mark again', nothing: 'No room measured yet', openFirst: 'Measure a room first, then mark its doors and windows',
    exitAgain: 'Press Exit again to leave without saving', squareOn: 'Right angle on', squareOff: 'Right angle off',
    namesHead: 'What is this room?', skip: 'Skip',
    count: (n, k) => 'Room ' + n + ' · ' + k + (k === 1 ? ' corner' : ' corners'),
    rooms: (n) => (n === 1 ? '1 room' : n + ' rooms'), room: 'Room',
    resHead: 'The plan is ready', resArea: 'Floor area',
    truth: 'The sizes were measured with the camera and can be off by a few centimetres. Before ordering furniture or a kitchen, measure the deciding wall again.',
    go: 'Continue to corrections and 3D', again: 'Measure again', none: 'No room was closed, so there is no plan yet. You can measure again.',
    warn: {
      'room.alone': (n) => (n || 'A room') + ': no shared wall with another room was found. If there is a wall between them, fix it in the drawing.',
      'room.overlap': () => 'Two rooms were measured on top of each other. Check them in the drawing.',
      'room.few': () => 'A room that was not closed is not in the plan.', 'room.small': () => 'A room too small to use is not in the plan.',
      'room.cross': () => 'A room whose lines cross is not in the plan.', 'room.shape': (n) => (n || 'A room') + ': the shape stays as measured.',
      'opening.off': () => 'A door or window marked away from any wall was left out.', 'opening.narrow': () => 'An opening narrower than 30 cm was left out.',
      'open.dropped': () => 'The corners of the last room, which was not closed, were left out.',
    },
  },
};
const CHOICE_LABEL = (lang, c) => (lang === 'en' ? c.en : c.he);

// ---------- small helpers ----------
let cssUsers = 0;
function ensureHeadCss(version) {
  if (!document.querySelector('link[data-nd-fonts]')) { const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = FONTS; l.setAttribute('data-nd-fonts', ''); document.head.appendChild(l); }
  cssUsers++;
  if (document.querySelector('link[data-nlscan-css]')) return;
  const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = BASE + 'roomscan.css?v=' + (version || '1'); l.setAttribute('data-nlscan-css', ''); document.head.appendChild(l);
}
function dropHeadCss() { if (--cssUsers <= 0) { cssUsers = 0; const l = document.querySelector('link[data-nlscan-css]'); if (l) l.remove(); } }
const qrot = (q, v) => { // rotate v by the unit quaternion q
  const { x, y, z, w } = q, ix = w * v[0] + y * v[2] - z * v[1], iy = w * v[1] + z * v[0] - x * v[2], iz = w * v[2] + x * v[1] - y * v[0], iw = -x * v[0] - y * v[1] - z * v[2];
  return [ix * w + iw * -x + iy * -z - iz * -y, iy * w + iw * -y + iz * -x - ix * -z, iz * w + iw * -z + ix * -y - iy * -x];
};
const fmtM = (cm) => (cm / 100).toFixed(2);
const d2 = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);

const ICONS = [
  // the phone pointed at the floor, the marker on it
  '<svg viewBox="0 0 64 64" aria-hidden="true"><path class="i-ln" d="M6 54h52"/><rect class="i-ln" x="24" y="8" width="18" height="30" transform="rotate(28 33 23)"/><path class="i-bl" d="M36 40l6 10"/><ellipse class="i-bl" cx="44" cy="54" rx="9" ry="3.5"/></svg>',
  // a room outline, the marker on one corner
  '<svg viewBox="0 0 64 64" aria-hidden="true"><path class="i-ln" d="M10 14h44v38H10z"/><circle class="i-bl" cx="54" cy="52" r="5"/><path class="i-bl" d="M54 42v4M54 58v4M44 52h4M60 52h4"/><circle class="i-dot" cx="10" cy="14" r="3"/><circle class="i-dot" cx="54" cy="14" r="3"/><circle class="i-dot" cx="10" cy="52" r="3"/></svg>',
  // two rooms and the way from one to the next
  '<svg viewBox="0 0 64 64" aria-hidden="true"><path class="i-ln" d="M4 14h26v36H4zM34 14h26v36H34z"/><path class="i-bl" d="M14 32h34M42 26l6 6-6 6"/></svg>',
];

/** { ok, why }: why = 'https' (no secure page), 'noxr' (no WebXR in this browser), 'noar' (no camera measuring on this device) */
export async function scanSupported() {
  if (typeof window === 'undefined' || typeof navigator === 'undefined') return { ok: false, why: 'noxr' };
  if (!window.isSecureContext) return { ok: false, why: 'https' };
  if (!navigator.xr || typeof navigator.xr.isSessionSupported !== 'function') return { ok: false, why: 'noxr' };
  try { if (!(await navigator.xr.isSessionSupported('immersive-ar'))) return { ok: false, why: 'noar' }; } catch (e) { return { ok: false, why: 'noar' }; }
  return { ok: true, why: null };
}

export async function mountRoomScan(host, opts = {}) {
  const lang = opts.lang === 'en' ? 'en' : 'he', T = TX[lang];
  ensureHeadCss(opts.version);
  const box = document.createElement('div'); box.className = 'nlscan-host';
  // a host that already carries a shadow root (the designer's frame) shows only what is inside that root
  if (host.shadowRoot) { box.style.cssText = 'display:block;position:absolute;inset:0'; host.shadowRoot.appendChild(box); } else host.appendChild(box);
  const shadow = box.attachShadow({ mode: 'open' });
  const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = BASE + 'roomscan.css?v=' + (opts.version || '1');
  const page = document.createElement('div'); page.className = 'nlscan-page'; page.dir = T.dir; page.lang = lang;
  shadow.append(css, page);
  let alive = true, sup = null, xr = null, threeP = null;

  // ---------- the explanation screen ----------
  function intro(why) {
    const steps = T.steps.map((s, i) => '<li>' + ICONS[i] + '<span><b class="nlscan-n">' + (i + 1) + '</b>' + esc(s) + '</span></li>').join('');
    page.innerHTML =
      '<header class="nlscan-head"><h2>' + esc(T.title) + '</h2></header>' +
      '<div class="nlscan-body">' +
      (why ? '<div class="nlscan-why" role="status"><b>' + esc(T.whyHead) + '</b><p>' + esc(T.why[why] || T.why.noar) + '</p><p>' + esc(T.whyAlt) + '</p></div>' : '') +
      '<ol class="nlscan-steps">' + steps + '</ol>' +
      '<p class="nlscan-fine">' + esc(T.works) + '</p><p class="nlscan-fine">' + esc(T.privacy) + '</p></div>' +
      '<div class="nlscan-actions">' +
      (!why || why === 'denied' || why === 'failed' ? '<button class="nlscan-btn nlscan-go" data-a="start">' + esc(why ? T.retry : T.start) + '</button>' : '') +
      '<button class="nlscan-btn" data-a="back">' + esc(T.back) + '</button></div>';
    page.querySelector('[data-a="back"]').onclick = () => { if (opts.onCancel) opts.onCancel(); };
    const go = page.querySelector('[data-a="start"]');
    if (go) go.onclick = () => { go.disabled = true; go.textContent = T.starting; start(); };
  }

  // ---------- the result screen ----------
  function resultScreen(res) {
    const named = res.rooms.map((r, i) => ({ ...r, label: r.key ? CHOICE_LABEL(lang, ROOM_CHOICES.find((c) => c.key === r.key) || { he: r.name_he, en: r.name_he }) : T.room + ' ' + (i + 1) }));
    const total = res.rooms.reduce((s, r) => s + r.area, 0);
    const warn = [...new Set((res.warnings || []).map((w) => (T.warn[w.code] ? T.warn[w.code](w.name_he && lang === 'he' ? w.name_he : null) : null)).filter(Boolean))];
    page.innerHTML =
      '<header class="nlscan-head"><h2>' + esc(res.rooms.length ? T.resHead : T.title) + '</h2></header>' +
      '<div class="nlscan-body">' +
      (res.rooms.length
        ? '<p class="nlscan-sum"><b>' + esc(T.rooms(res.rooms.length)) + '</b> · ' + esc(T.resArea) + ' <b class="nlscan-mono">' + total.toFixed(1) + '</b> ' + esc(T.sqm) + '</p>' +
          '<div class="nlscan-plan">' + planSvg(res, named) + '</div>' +
          '<p class="nlscan-truth">' + esc(T.truth) + '</p>' + warn.map((w) => '<p class="nlscan-fine">' + esc(w) + '</p>').join('')
        : '<p class="nlscan-truth">' + esc(T.none) + '</p>') +
      '</div><div class="nlscan-actions">' +
      (res.rooms.length ? '<button class="nlscan-btn nlscan-go" data-a="done">' + esc(T.go) + '</button>' : '') +
      '<button class="nlscan-btn" data-a="again">' + esc(T.again) + '</button></div>';
    const done = page.querySelector('[data-a="done"]');
    if (done) done.onclick = () => { if (opts.onDone) opts.onDone(res); };
    page.querySelector('[data-a="again"]').onclick = () => intro(null);
  }
  function planSvg(res, named) {
    const xs = [], ys = [];
    for (const s of res.segments) { xs.push(s.a[0], s.b[0]); ys.push(s.a[1], s.b[1]); }
    const x0 = Math.min(...xs) - 30, y0 = Math.min(...ys) - 30, w = Math.max(...xs) - x0 + 30, h = Math.max(...ys) - y0 + 30, fs = Math.max(w, h) * 0.034;
    const quad = (s, grow) => { const v = [s.b[0] - s.a[0], s.b[1] - s.a[1]], L = Math.hypot(v[0], v[1]) || 1, n = [(-v[1] / L) * (s.t / 2 + (grow || 0)), (v[0] / L) * (s.t / 2 + (grow || 0))]; return [[s.a[0] + n[0], s.a[1] + n[1]], [s.b[0] + n[0], s.b[1] + n[1]], [s.b[0] - n[0], s.b[1] - n[1]], [s.a[0] - n[0], s.a[1] - n[1]]].map((p) => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' '); };
    let out = '<svg viewBox="' + [x0, y0, w, h].map((v) => v.toFixed(1)).join(' ') + '" role="img" aria-label="' + esc(T.resHead) + '">';
    for (const r of named) out += '<polygon class="p-room" points="' + r.poly.map((p) => p.join(',')).join(' ') + '"/>';
    for (const s of res.segments) out += '<polygon class="p-w ' + s.kind + '" points="' + quad(s) + '"/>';
    for (const o of res.openings) {
      const s = { a: o.a, b: o.b, t: 40 };
      out += '<polygon class="p-gap" points="' + quad(s) + '"/><line class="p-op ' + o.type + '" x1="' + o.a[0] + '" y1="' + o.a[1] + '" x2="' + o.b[0] + '" y2="' + o.b[1] + '"/>';
    }
    for (const r of named) {
      out += '<text class="p-name" x="' + r.at[0] + '" y="' + (r.at[1] - fs * 0.15) + '" font-size="' + fs.toFixed(1) + '">' + esc(r.label) + '</text>';
      out += '<text class="p-area" x="' + r.at[0] + '" y="' + (r.at[1] + fs * 1.05) + '" font-size="' + (fs * 0.85).toFixed(1) + '">' + r.area.toFixed(1) + ' ' + esc(T.sqm) + '</text>';
    }
    return out + '</svg>';
  }

  // ---------- measuring ----------
  async function start() {
    const root = document.createElement('div');
    root.className = 'nlscan-root'; root.dir = T.dir; root.lang = lang; root.style.display = 'none';
    document.body.appendChild(root);
    let session = null;
    try {
      session = await navigator.xr.requestSession('immersive-ar', { requiredFeatures: ['hit-test', 'dom-overlay'], optionalFeatures: ['anchors'], domOverlay: { root } });
    } catch (e) {
      root.remove();
      if (alive) intro(e && (e.name === 'NotAllowedError' || e.name === 'SecurityError') ? 'denied' : e && e.name === 'NotSupportedError' ? 'nofeature' : 'failed');
      return;
    }
    if (!alive) { session.end().catch(() => {}); root.remove(); return; }
    page.innerHTML = '<header class="nlscan-head"><h2>' + esc(T.title) + '</h2></header><div class="nlscan-body"><p class="nlscan-fine">' + esc(T.starting) + '</p></div>';
    try { xr = await runSession(session, root); } catch (e) {
      console.warn('roomscan: the session could not start', e);
      try { await session.end(); } catch (x) { /* already over */ }
      root.remove(); if (alive) intro('failed');
    }
  }

  async function runSession(session, root) {
    const THREE = await (threeP || (threeP = import('three')));
    const t0 = performance.now();
    // ---- state (positions in WebXR metres; the plan frame is metres x 100 = cm) ----
    const rooms = [], openings = [], hist = [];
    let cur = [], axis = null, squareOn = true, floorY = null, floorMin = null, mode = 'corner', side = null, want = false, wantAt = 0;
    let discard = false, lostAt = 0, exitArmed = 0, toastText = '', toastUntil = 0, ended = false, finishing = false, naming = null, lastUi = 0, mapDirty = true;
    const buf = []; let aim = null, aimSnap = null, hitRes = null, rejected = false, viewer = null;
    const anchorsOn = !session.enabledFeatures || session.enabledFeatures.includes('anchors');
    const live = []; // every anchored point, so each frame can read where the anchor is now
    const pt = (c) => (c.a0 && c.an ? [c.w[0] + c.an[0] - c.a0[0], c.w[1], c.w[2] + c.an[2] - c.a0[2]] : c.w); // the corner as tracking now sees it
    const plan = (w) => worldToPlan(w);

    // ---- the overlay ----
    const B = (k, label, cls) => '<button class="nlscan-btn ' + (cls || '') + '" data-k="' + k + '">' + esc(label) + '</button>';
    root.innerHTML =
      '<div class="nlscan-top"><div class="nlscan-line">' + B('exit', T.exit, 'nlscan-exit') + '<p class="nlscan-msg" data-r="msg" aria-live="polite"></p></div>' +
      '<div class="nlscan-line nlscan-sub"><span data-r="count"></span><b class="nlscan-dist" data-r="dist"></b></div></div>' +
      '<div class="nlscan-side">' + B('square', T.square, 'nlscan-chip') + '<canvas class="nlscan-map" data-r="map" width="10" height="10" aria-hidden="true"></canvas></div>' +
      '<div class="nlscan-aim" aria-hidden="true"></div>' +
      '<p class="nlscan-warn" data-r="warn" role="alert" hidden>' + esc(T.lost) + '</p>' +
      '<div class="nlscan-names" data-r="names" hidden><p>' + esc(T.namesHead) + '</p><div class="nlscan-grid">' +
      ROOM_CHOICES.map((c) => '<button class="nlscan-btn" data-name="' + c.key + '">' + esc(CHOICE_LABEL(lang, c)) + '</button>').join('') +
      '<button class="nlscan-btn" data-name="">' + esc(T.skip) + '</button></div></div>' +
      '<div class="nlscan-bar"><div class="nlscan-row">' + B('undo', T.undo) + B('corner', T.corner, 'nlscan-main') + B('close', T.close) + '</div>' +
      '<div class="nlscan-row">' + B('door', T.door) + B('window', T.window) + B('finish', T.finish, 'nlscan-fin') + '</div></div>';
    const $ = (s) => root.querySelector(s), btn = (k) => root.querySelector('[data-k="' + k + '"]');
    const mapC = $('[data-r="map"]');
    root.addEventListener('beforexrselect', (e) => e.preventDefault()); // a tap on the controls is not a tap in the room
    const toast = (s, ms) => { toastText = s; toastUntil = performance.now() + (ms || 2600); lastUi = 0; };

    // ---- the 3D marks on the floor ----
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(window.devicePixelRatio || 1);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.xr.enabled = true;
    renderer.xr.setReferenceSpaceType('local');
    const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.01, 40);
    const mat = (c, o) => new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o == null ? 1 : o, depthTest: false, depthWrite: false, side: THREE.DoubleSide });
    const M = { blue: mat(C.blue), blueSoft: mat(C.blue, 0.55), ink: mat(C.ink), white: mat(0xffffff), dim: mat(C.dim) };
    const flat = (g) => { g.rotateX(-Math.PI / 2); return g; };
    const reticle = new THREE.Group();
    reticle.add(new THREE.Mesh(flat(new THREE.RingGeometry(0.075, 0.095, 40)), M.ink), new THREE.Mesh(flat(new THREE.RingGeometry(0.052, 0.075, 40)), M.white), new THREE.Mesh(flat(new THREE.CircleGeometry(0.012, 16)), M.blue));
    reticle.visible = false; reticle.renderOrder = 3; scene.add(reticle);
    const unit = flat(new THREE.PlaneGeometry(1, 1));
    const bar = (a, b, w, m) => { const dx = b[0] - a[0], dz = b[2] - a[2], L = Math.hypot(dx, dz), o = new THREE.Mesh(unit, m); o.scale.set(Math.max(L, 0.001), 1, w); o.position.set((a[0] + b[0]) / 2, (floorY == null ? a[1] : floorY) + 0.004, (a[2] + b[2]) / 2); o.rotation.y = -Math.atan2(dz, dx); o.renderOrder = 1; return o; };
    const dotGeo = flat(new THREE.CircleGeometry(0.03, 20)), dotIn = flat(new THREE.CircleGeometry(0.018, 20));
    const marks = new THREE.Group(); scene.add(marks);
    const preview = new THREE.Mesh(unit, M.blueSoft); preview.visible = false; preview.renderOrder = 2; scene.add(preview);
    function redraw() {
      for (const c of [...marks.children]) marks.remove(c);
      const y = (p) => [p[0], floorY == null ? p[1] : floorY, p[2]];
      const ring = (list, closed) => {
        const P = list.map((c) => y(pt(c)));
        for (let i = 0; i < P.length - (closed ? 0 : 1); i++) marks.add(bar(P[i], P[(i + 1) % P.length], 0.022, M.blue));
        for (const p of P) { const a = new THREE.Mesh(dotGeo, M.blue), b = new THREE.Mesh(dotIn, M.white); a.position.set(p[0], p[1] + 0.005, p[2]); b.position.set(p[0], p[1] + 0.006, p[2]); a.renderOrder = b.renderOrder = 2; marks.add(a, b); }
      };
      for (const r of rooms) ring(r.corners, true);
      ring(cur, false);
      for (const o of openings) marks.add(bar(y(pt(o.a)), y(pt(o.b)), 0.06, o.type === 'door' ? M.ink : M.white));
      if (side) { const p = y(pt(side)), a = new THREE.Mesh(dotGeo, M.ink); a.position.set(p[0], p[1] + 0.005, p[2]); marks.add(a); }
      mapDirty = true;
    }

    await renderer.xr.setSession(session);
    const ref = renderer.xr.getReferenceSpace();
    const viewerSpace = await session.requestReferenceSpace('viewer');
    const hitSource = await session.requestHitTestSource({ space: viewerSpace });
    root.style.display = '';

    // ---- what the phone points at, each frame ----
    function readAnchors(frame) {
      for (const c of live) {
        if (!c.anchor) continue;
        if (frame.trackedAnchors && !frame.trackedAnchors.has(c.anchor)) continue;
        const p = frame.getPose(c.anchor.anchorSpace, ref);
        if (!p) continue;
        const q = [p.transform.position.x, p.transform.position.y, p.transform.position.z];
        if (!c.a0) c.a0 = q; else { if (!c.an || d2([c.an[0], c.an[2]], [q[0], q[2]]) > 0.002) mapDirty = true; c.an = q; }
      }
    }
    function look(frame, pose) {
      hitRes = null; rejected = false;
      let cand = null, near = Infinity;
      const eye = pose ? pose.transform.position : null;
      for (const h of frame.getHitTestResults(hitSource)) {
        const hp = h.getPose(ref); if (!hp) continue;
        if (qrot(hp.transform.orientation, [0, 1, 0])[1] < 0.85) { // a wall or a slope, not a floor
          if (eye) near = Math.min(near, Math.hypot(hp.transform.position.x - eye.x, hp.transform.position.y - eye.y, hp.transform.position.z - eye.z));
          continue;
        }
        const p = hp.transform.position;
        if (floorY == null && (floorMin == null || p.y < floorMin)) floorMin = p.y;
        const base = floorY != null ? floorY : floorMin;
        if (p.y - base > 0.1) { rejected = true; continue; } // a table or a bed top
        cand = [p.x, p.y, p.z]; hitRes = h; break;
      }
      if (!cand && !rejected && floorY != null && pose) { // the floor is known: where the centre of the screen meets it, even where no surface was found
        const o = pose.transform.position, d = qrot(pose.transform.orientation, [0, 0, -1]);
        if (d[1] < -0.08) {
          const t = (floorY - o.y) / d[1];
          if (t > near + 0.15) rejected = true; // a wall stands before that point: the aim is above the floor line
          else if (t > 0 && t < 8) cand = [o.x + d[0] * t, floorY, o.z + d[2] * t];
        }
      }
      return cand;
    }
    function snapNow(cand) {
      const c = plan(cand);
      if (mode !== 'corner') { // a door or window side goes onto the nearest measured wall line
        let best = null;
        for (const r of rooms) { const P = r.corners.map((x) => plan(pt(x))); for (let i = 0; i < P.length; i++) { const s = segDist(c, P[i], P[(i + 1) % P.length]); if (s.d < 25 && (!best || s.d < best.d)) best = s; } }
        return { p: best ? best.q : c, snap: best ? 'wall' : null };
      }
      const P = cur.map((x) => plan(pt(x)));
      if (!P.length) return { p: c, snap: null };
      return snapCorner(P[P.length - 1], c, axis, { square: squareOn, reach: 15, corners: P.length >= 3 ? [P[0]] : [], next: P.length >= 2 ? P[0] : null });
    }
    function capture(frame) {
      const p = aimSnap.p, w = [p[0] / 100, floorY == null ? aim[1] : floorY, p[1] / 100];
      const c = { w, anchor: null, a0: null, an: null };
      if (anchorsOn) {
        try {
          const pr = hitRes && typeof hitRes.createAnchor === 'function' ? hitRes.createAnchor()
            : typeof frame.createAnchor === 'function' && typeof XRRigidTransform !== 'undefined' ? frame.createAnchor(new XRRigidTransform({ x: w[0], y: w[1], z: w[2] }), ref) : null;
          if (pr) { live.push(c); pr.then((a) => { if (ended) { try { a.delete(); } catch (e) { /* gone */ } } else c.anchor = a; }, () => {}); }
        } catch (e) { /* no anchor for this point: it keeps the place it was marked at */ }
      }
      if (mode === 'corner') {
        toastUntil = 0;
        if (floorY == null) floorY = aim[1];
        if (aimSnap.snap === 'corner' && cur.length >= 3) { closeNow(); return; } // the first corner again: the room is closed
        cur.push(c); hist.push('corner');
        if (axis == null && rooms.length === 0 && cur.length === 2) { const a = plan(cur[0].w), b = plan(cur[1].w); axis = Math.atan2(b[1] - a[1], b[0] - a[0]); }
      } else if (!side) { side = c; }
      else { openings.push({ type: mode, a: side, b: c }); hist.push('opening'); toast(T.openSaved(mode === 'door')); side = null; mode = 'corner'; }
      redraw(); lastUi = 0;
    }
    function closeNow(thenFinish) {
      if (cur.length < 3) { toast(T.few); return false; }
      const chk = closeRoom(cur.map((c) => plan(pt(c))));
      if (!chk.ok) { toast(T[chk.why] || T.few); return false; }
      naming = { corners: cur, thenFinish: !!thenFinish };
      $('[data-r="names"]').hidden = false; lastUi = 0;
      return true;
    }
    function named(key) {
      const ch = ROOM_CHOICES.find((c) => c.key === key) || null;
      rooms.push({ corners: naming.corners, key: ch ? ch.key : null, name_he: ch ? ch.name_he : null, type: ch ? ch.type : null });
      hist.push('close'); cur = []; const fin = naming.thenFinish; naming = null;
      $('[data-r="names"]').hidden = true; redraw(); toast(T.saved, 3200);
      if (fin) finish();
    }
    function undo() {
      if (naming) { naming = null; $('[data-r="names"]').hidden = true; lastUi = 0; return; }
      if (mode !== 'corner') { if (side) side = null; else mode = 'corner'; redraw(); lastUi = 0; return; }
      const k = hist.pop();
      if (k === 'corner') { const c = cur.pop(); drop(c); if (!rooms.length && cur.length < 2) axis = null; }
      else if (k === 'close') { const r = rooms.pop(); cur = r.corners; }
      else if (k === 'opening') { const o = openings.pop(); drop(o.a); drop(o.b); }
      redraw(); lastUi = 0;
    }
    const drop = (c) => { if (!c) return; const i = live.indexOf(c); if (i >= 0) live.splice(i, 1); if (c.anchor) try { c.anchor.delete(); } catch (e) { /* gone */ } };
    function finish() {
      if (naming) return;
      if (cur.length >= 3 && closeRoom(cur.map((c) => plan(pt(c)))).ok) { closeNow(true); return; }
      if (!rooms.length) { toast(T.nothing); return; }
      finishing = true; end();
    }
    function build() {
      const list = rooms.map((r) => ({ points: r.corners.map((c) => plan(pt(c))), name_he: r.name_he, type: r.type, key: r.key }));
      const ops = openings.map((o) => ({ a: plan(pt(o.a)), b: plan(pt(o.b)), type: o.type }));
      const res = roomsToSegments(list, { openings: ops });
      if (cur.length) res.warnings.push({ code: 'open.dropped' });
      const all = rooms.flatMap((r) => r.corners);
      res.meta = { points: all.length, rooms: rooms.length, seconds: Math.round((performance.now() - t0) / 1000), anchored: all.filter((c) => c.a0 && c.an).length };
      return res;
    }
    let result = null;
    function end() { if (!ended) { result = build(); session.end().catch(() => onEnd()); } }
    function onEnd() {
      if (ended) return; ended = true;
      if (!result && !discard) result = rooms.length ? build() : null; // the system back button ends the session: keep what was measured
      renderer.setAnimationLoop(null);
      for (const c of live) if (c.anchor) try { c.anchor.delete(); } catch (e) { /* gone */ }
      try { hitSource.cancel(); } catch (e) { /* gone */ }
      renderer.dispose(); root.remove(); xr = null;
      if (!alive) return;
      if (result) resultScreen(result); else intro(null);
    }
    session.addEventListener('end', onEnd);

    root.addEventListener('click', (e) => {
      const b = e.target.closest('button'); if (!b || b.disabled) return;
      if (b.hasAttribute('data-name')) { if (naming) named(b.getAttribute('data-name') || null); return; }
      const k = b.getAttribute('data-k');
      if (k !== 'exit') exitArmed = 0;
      if (k !== 'corner') toastUntil = 0; // the last note gives way to what this press asks for
      if (k === 'corner') { want = true; wantAt = performance.now(); }
      else if (k === 'undo') undo();
      else if (k === 'close') { if (!naming) closeNow(false); }
      else if (k === 'door' || k === 'window') { if (!rooms.length) toast(T.openFirst); else { mode = mode === k ? 'corner' : k; side = null; redraw(); } }
      else if (k === 'finish') finish();
      else if (k === 'square') { squareOn = !squareOn; toast(squareOn ? T.squareOn : T.squareOff, 1600); }
      else if (k === 'exit') { if (exitArmed && performance.now() - exitArmed < 4000) { result = null; discard = true; finishing = false; session.end().catch(() => onEnd()); } else if (!rooms.length && !cur.length) { discard = true; session.end().catch(() => onEnd()); } else { exitArmed = performance.now(); toast(T.exitAgain, 4000); } }
      lastUi = 0;
    });

    // ---- the frame loop ----
    function ui(now, stable) {
      const lost = lostAt && now - lostAt > 500;
      $('[data-r="warn"]').hidden = !lost;
      let msg;
      if (now < toastUntil) msg = toastText;
      else if (naming) msg = T.namesHead;
      else if (lost) msg = T.lost;
      else if (mode !== 'corner') msg = mode === 'door' ? (side ? T.doorB : T.doorA) : side ? T.winB : T.winA;
      else if (!aim) msg = rejected ? T.notFloor : floorY == null ? T.aimFloor : T.notFloor;
      else if (aimSnap && aimSnap.snap === 'corner') msg = T.closing;
      else if (!stable) msg = T.hold;
      else msg = cur.length ? T.next : T.first;
      $('[data-r="msg"]').textContent = msg;
      $('[data-r="count"]').textContent = T.count(rooms.length + 1, cur.length);
      const from = mode !== 'corner' ? side : cur[cur.length - 1];
      const dist = from && aimSnap && !naming ? fmtM(d2(plan(pt(from)), aimSnap.p)) : '', de = $('[data-r="dist"]');
      if (de.dataset.v !== dist) { de.dataset.v = dist; de.innerHTML = dist ? '<span class="nlscan-num">' + dist + '</span> <span class="nlscan-unit">' + esc(T.m) + '</span>' : ''; }
      const main = btn('corner');
      main.textContent = mode === 'corner' ? T.corner : T.mark;
      main.disabled = !!(lost || !aim || naming); // pressed while the hand still moves: it waits up to 1.5 s for a steady aim
      main.classList.toggle('nlscan-wait', !stable);
      btn('close').disabled = !!(naming || mode !== 'corner' || cur.length < 3);
      btn('undo').disabled = !!(!naming && mode === 'corner' && !hist.length);
      btn('door').setAttribute('aria-pressed', String(mode === 'door')); btn('window').setAttribute('aria-pressed', String(mode === 'window'));
      btn('square').setAttribute('aria-pressed', String(squareOn));
    }
    function drawMap() {
      const dpr = window.devicePixelRatio || 1, W = mapC.clientWidth || 132, H = mapC.clientHeight || 132;
      if (mapC.width !== Math.round(W * dpr)) { mapC.width = Math.round(W * dpr); mapC.height = Math.round(H * dpr); }
      const g = mapC.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
      g.strokeStyle = C.grid; g.lineWidth = 1;
      for (let i = 12; i < W; i += 12) { g.beginPath(); g.moveTo(i + 0.5, 0); g.lineTo(i + 0.5, H); g.stroke(); }
      for (let i = 12; i < H; i += 12) { g.beginPath(); g.moveTo(0, i + 0.5); g.lineTo(W, i + 0.5); g.stroke(); }
      const ax = axis || 0, R = (p) => [p[0] * Math.cos(-ax) - p[1] * Math.sin(-ax), p[0] * Math.sin(-ax) + p[1] * Math.cos(-ax)];
      const polys = rooms.map((r) => r.corners.map((c) => R(plan(pt(c))))), line = cur.map((c) => R(plan(pt(c))));
      const extra = []; if (aimSnap) extra.push(R(aimSnap.p)); if (viewer) extra.push(R(plan(viewer)));
      const all = polys.flat().concat(line, extra);
      if (!all.length) return;
      let x0 = Math.min(...all.map((p) => p[0])), x1 = Math.max(...all.map((p) => p[0])), y0 = Math.min(...all.map((p) => p[1])), y1 = Math.max(...all.map((p) => p[1]));
      const span = Math.max(300, x1 - x0, y1 - y0), k = (Math.min(W, H) - 22) / span, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
      const S = (p) => [W / 2 + (p[0] - cx) * k, H / 2 + (p[1] - cy) * k];
      g.lineJoin = 'miter';
      for (const P of polys) { g.beginPath(); P.forEach((p, i) => { const s = S(p); i ? g.lineTo(s[0], s[1]) : g.moveTo(s[0], s[1]); }); g.closePath(); g.fillStyle = C.blue2; g.fill(); g.strokeStyle = C.ink; g.lineWidth = 2; g.stroke(); }
      for (const o of openings) { const a = S(R(plan(pt(o.a)))), b = S(R(plan(pt(o.b)))); g.strokeStyle = o.type === 'door' ? '#fff' : C.blue; g.lineWidth = 4; g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke(); }
      if (line.length) {
        g.strokeStyle = C.blue; g.lineWidth = 2; g.beginPath(); line.forEach((p, i) => { const s = S(p); i ? g.lineTo(s[0], s[1]) : g.moveTo(s[0], s[1]); });
        if (aimSnap && mode === 'corner') { const s = S(R(aimSnap.p)); g.lineTo(s[0], s[1]); }
        g.stroke();
      }
      // wall lengths, red, on every wall of half a metre or more
      g.font = '600 10px "IBM Plex Mono", monospace'; g.textAlign = 'center'; g.textBaseline = 'middle';
      // each length sits just inside its own room, so the two sides of a shared wall do not cover each other
      const taken = [];
      const lab = (a, b, sgn) => {
        const L = d2(a, b); if (L < 50) return;
        const sa = S(a), sb = S(b), v = [sb[0] - sa[0], sb[1] - sa[1]], l = Math.hypot(v[0], v[1]) || 1, t = fmtM(L), w = g.measureText(t).width + 4;
        if (l < 16) return;
        const n = [(-v[1] / l) * sgn, (v[0] / l) * sgn], off = Math.abs(n[0]) * (w / 2 + 3) + Math.abs(n[1]) * 8;
        const x = Math.max(w / 2 + 1, Math.min(W - w / 2 - 1, (sa[0] + sb[0]) / 2 + n[0] * off)), y = Math.max(7, Math.min(H - 7, (sa[1] + sb[1]) / 2 + n[1] * off));
        const box = [x - w / 2, y - 6, x + w / 2, y + 6];
        if (taken.some((r) => box[0] < r[2] && r[0] < box[2] && box[1] < r[3] && r[1] < box[3])) return; // no label on top of another
        taken.push(box);
        g.fillStyle = 'rgba(255,255,255,.92)'; g.fillRect(box[0], box[1], w, 12); g.fillStyle = C.dim; g.fillText(t, x, y + 0.5);
      };
      const area2 = (P) => { let A = 0; for (let i = 0; i < P.length; i++) { const p = P[i], q = P[(i + 1) % P.length]; A += p[0] * q[1] - q[0] * p[1]; } return A; };
      line.forEach((p, i) => { if (i) lab(line[i - 1], p, 1); }); // the room being measured first: that is what the person checks now
      for (const P of polys.slice().reverse()) { const sgn = area2(P) > 0 ? 1 : -1; P.forEach((p, i) => lab(p, P[(i + 1) % P.length], sgn)); }
      for (const p of line) { const s = S(p); g.fillStyle = C.blue; g.fillRect(s[0] - 2.5, s[1] - 2.5, 5, 5); }
      if (aimSnap) { const s = S(R(aimSnap.p)); g.strokeStyle = C.blue; g.lineWidth = 2; g.beginPath(); g.arc(s[0], s[1], 4, 0, Math.PI * 2); g.stroke(); }
      if (viewer) { const s = S(R(plan(viewer))); g.fillStyle = C.ink; g.beginPath(); g.arc(s[0], s[1], 3.5, 0, Math.PI * 2); g.fill(); }
    }

    let lastMap = 0;
    renderer.setAnimationLoop((time, frame) => {
      if (!frame || ended) return;
      const now = performance.now(), pose = frame.getViewerPose(ref), tracking = !!pose && !pose.emulatedPosition;
      if (!tracking) { if (!lostAt) lostAt = now; } else lostAt = 0;
      viewer = pose ? [pose.transform.position.x, pose.transform.position.y, pose.transform.position.z] : viewer;
      readAnchors(frame);
      const cand = tracking ? look(frame, pose) : null;
      if (cand) { buf.push({ t: now, p: cand }); while (buf.length && now - buf[0].t > 400) buf.shift(); } else buf.length = 0;
      const stable = !!cand && buf.length >= 3 && now - buf[0].t >= 250 && buf.every((b) => Math.hypot(b.p[0] - cand[0], b.p[2] - cand[2]) < 0.02);
      aim = cand; aimSnap = cand ? snapNow(cand) : null;
      if (want && now - wantAt > 1500) want = false; // a press waits a moment for a steady aim, then is forgotten
      if (want && stable && aimSnap && !naming) { want = false; capture(frame); }
      if (aimSnap) {
        const y = floorY == null ? cand[1] : floorY, w = [aimSnap.p[0] / 100, y, aimSnap.p[1] / 100];
        reticle.visible = true; reticle.position.set(w[0], y + 0.006, w[2]);
        reticle.children[2].material = stable ? M.blue : M.ink;
        const from = mode !== 'corner' ? side : cur[cur.length - 1];
        if (from) { const f = pt(from), b = bar([f[0], y, f[2]], w, 0.016, M.blueSoft); preview.scale.copy(b.scale); preview.position.copy(b.position); preview.rotation.copy(b.rotation); preview.visible = true; } else preview.visible = false;
        if (!lastMap || now - lastMap > 150) mapDirty = true;
      } else { reticle.visible = false; preview.visible = false; }
      if (now - lastUi > 120) { ui(now, stable); lastUi = now; }
      if (mapDirty && now - lastMap > 100) { drawMap(); mapDirty = false; lastMap = now; }
      renderer.render(scene, camera);
    });
    return { end: () => { result = null; discard = true; session.end().catch(() => onEnd()); } };
  }

  // ---------- go ----------
  sup = await scanSupported();
  if (alive) intro(sup.ok ? null : sup.why);
  if (sup.ok) threeP = import('three').catch(() => null); // fetched while the person reads, so the camera opens fast

  return {
    destroy() {
      if (!alive) return; alive = false;
      if (xr) xr.end();
      box.remove(); dropHeadCss();
    },
  };
}
