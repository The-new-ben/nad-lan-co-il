// nad-lan professionals' forum: the shared board inside a video call (HAD-726). Rebuilt 12.11.2026 night to follow the Claude
// Design boards 16 (phone) and 17 (desktop) exactly, after the owner rejected the first look as cheap.
// Imported by assets/proforum/call.js when a call starts. Everything goes through the call's own transport (publishData /
// onData of livekitTransport, assets/designer/call.js): nothing is uploaded or stored on the site; the board lives only in the
// call and in the PNG a person saves to his own device.
// Identity: a site drawing sheet. Paper #F7F9FA with a fine #E3E8EB grid, ink chrome #101820, a title block in the corner
// (sheet, scale), one colour per person by join order: raspberry #B0144F, sea #2F6F86, site green #2E7D5B, marking yellow
// #E8B400 (yellow carries ink text). Faces: Rubik for numbers, measures and headings, Assistant for text.
// Safety: text from people goes in only through textContent and SVG text nodes; every incoming message is validated (types,
// lengths, finite numbers, id pattern, caps). A person can remove only his own marks; notes can be marked agreed by anyone.

const NS = 'http://www.w3.org/2000/svg';
const TOPIC = 'nlfsb';
const PENS = ['#B0144F', '#2F6F86', '#2E7D5B', '#E8B400'];
const DARK = { '#B0144F': '#8C0F3E', '#2F6F86': '#1F5566', '#2E7D5B': '#1B4D33', '#E8B400': '#5E4A00' };
const CNAME = { '#B0144F': 'פטל', '#2F6F86': 'כחול ים', '#2E7D5B': 'ירוק', '#E8B400': 'צהוב' };
const ink = (c) => (c === '#E8B400' ? '#101820' : '#FFFFFF');
const PID = /^[A-Za-z0-9_.:@-]{1,64}$/, OID = /^[a-z0-9]{4,12}$/;
const KINDS = ['pen', 'mark', 'arrow', 'rect', 'ell', 'note', 'measure'];
const MAXOBJ = 3000, MAXNOTES = 200, MAXIMG = 1500000;
// the look lives in board.css next to this file, with the same version query so one release reaches both
const CSS_URL = (() => { try { const u = new URL(import.meta.url); return new URL('board.css' + u.search, u).href; } catch (e) { return ''; } })();
const T = {
	sub: 'לוח משותף · השיחה לא מוקלטת', subD: 'שיחת וידאו מתוך הדיון · לוח משותף · השיחה לא מוקלטת', back: 'חזרה לווידאו מלא', board: 'לוח משותף',
	tools: 'כלי סימון', tn: { pen: 'עט', mark: 'מרקר', arrow: 'חץ', shape: 'מלבן או עיגול', note: 'הערה ממוספרת', measure: 'מידה', laser: 'לייזר', erase: 'מחק, רק סימונים שלכם', hand: 'הזזת הדף' },
	rect: 'צורה: מלבן. לחיצה נוספת מחליפה לעיגול', ell: 'צורה: עיגול. לחיצה נוספת מחליפה למלבן', myc: (c) => 'הצבע שלי: ' + CNAME[c], undo: 'ביטול הסימון האחרון שלי',
	photo: 'צלמו או העלו תוכנית', photoD: 'העלאת תוכנית או תמונה', notes: 'הערות', more: 'עוד פעולות', save: 'שמירה כתמונה',
	clear: 'ניקוי הסימונים שלי', clearAgain: 'לחצו שוב כדי לנקות את הסימונים שלכם', cleared: 'הסימונים שלכם נוקו',
	follow: 'עקבו אחריי', leading: 'כולם עוקבים אחריכם · הפסקה', following: (n) => 'עוקבים אחרי ' + n + ' · הפסקה',
	sheet: 'גיליון', scale: 'קנה מידה', blank: 'דף משבצות', planOf: (n) => (n ? 'תוכנית ששיתף/ה ' + n : 'תוכנית'),
	noScale: 'עוד אין. מדדו קו שאורכו ידוע', scaleBy: (m) => 'לפי קו של ' + m + ' מ׳', approx: ' המידות בערך.',
	recal: 'כיול מחדש', recalA: 'כיול מחדש של קנה המידה', recalGo: 'עכשיו מדדו קו שאורכו ידוע לכם',
	lenQ: 'מה האורך האמיתי של הקו הזה?', lenPh: 'למשל 0.80 או 80 ס״מ', lenBad: 'כתבו אורך במטרים, למשל 0.80, או בס״מ, למשל 80 ס״מ', lenSkip: 'בלי מידה',
	noteQ: 'מה כתוב בהערה?', notePh: 'למשל: קיר נושא? צריך מהנדס', ok: 'הוספה', set: 'קביעה', cancel: 'ביטול', close: 'סגירה',
	notesH: 'הערות על התוכנית', none: 'עוד אין הערות. בחרו בכלי ההערה ולחצו על התוכנית.', done: 'סוכם', reopen: 'פתיחה מחדש', doneTag: 'סוכם בשיחה', del: 'מחיקה',
	deskIn: 'הערה חדשה, ואז לחיצה על התוכנית', deskInL: 'הערה חדשה על התוכנית', placeNow: 'עכשיו לחצו על המקום בתוכנית',
	photoH: 'תוכנית או תמונה ללוח', camera: 'צילום במצלמה', file: 'בחירת תמונה או תוכנית מהמכשיר', toBlank: 'חזרה לדף משבצות',
	replaceQ: 'להחליף את התוכנית? כל הסימונים וההערות על הלוח יימחקו אצל כולם.', replace: 'החלפה', blankQ: 'לחזור לדף משבצות? כל הסימונים וההערות יימחקו אצל כולם.', blankGo: 'חזרה לדף',
	sent: 'התוכנית נשלחה לכולם', big: 'התמונה גדולה מדי. נסו תמונה אחרת.', got: (n) => n + ' שיתף/ה תוכנית', saved: 'הלוח נשמר כתמונה במכשיר שלכם', saveFail: 'לא הצלחנו לשמור. נסו שוב.',
	notMine: 'אפשר למחוק רק סימונים שלכם', open: (n) => n + ' פתח/ה את הלוח המשותף', see: 'לפתוח את הלוח',
	micOn: 'להשתיק את המיקרופון', micOff: 'להפעיל את המיקרופון', camOn: 'לכבות את המצלמה', camOff: 'להפעיל את המצלמה', boardOn: 'הלוח המשותף פתוח. לחיצה חוזרת לווידאו', end: 'סיום שיחה', lBoard: 'לוח',
	speaking: 'מדבר/ת', zin: 'הגדלה', zout: 'הקטנה', hint: 'ציירו, סמנו והעירו. כולם רואים מיד. שום דבר לא נשמר באתר.', you: 'אתם', timer: 'משך השיחה',
	count: (n, d) => (n === 1 ? 'הערה אחת' : n + ' הערות') + (d ? ' · ' + (d === 1 ? 'אחת טופלה' : d + ' טופלו') : ''), sheetA: 'הגיליון המשותף. ציור בעכבר או באצבע, שתי אצבעות להזזה ולהגדלה',
};
const ICONS = {
	pen: '<path d="M4 20l4-1 11-11-3-3L5 16z"/>', mark: '<path d="M6 20h12M8 16l8-8 3 3-8 8H8z"/>', arrow: '<path d="M5 19L19 5M10 5h9v9"/>',
	shape: '<rect x="3" y="8" width="12" height="12" rx="1"/><circle cx="16" cy="9" r="5"/>', rect: '<rect x="4" y="6" width="16" height="12" rx="1"/>', ell: '<ellipse cx="12" cy="12" rx="8" ry="6"/>',
	note: '<path d="M5 4h14v11l-5 5H5z"/><path d="M14 20v-5h5"/>', measure: '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
	laser: '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>', erase: '<path d="M7 20h12M5 15l8-8 6 6-5 5H9z"/>',
	hand: '<path d="M8 13V5a1.5 1.5 0 0 1 3 0v6m0-1V4a1.5 1.5 0 0 1 3 0v7m0-5a1.5 1.5 0 0 1 3 0v8c0 4-3 7-7 7s-6-2-7-5l-1-4a1.5 1.5 0 0 1 3-1l1 2"/>',
	undo: '<path d="M9 7L4 12l5 5"/><path d="M4 12h10a5 5 0 0 1 0 10h-2"/>', back: '<path d="M9 5l7 7-7 7"/>', camera: '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
	eye: '<circle cx="12" cy="12" r="3"/><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/>', list: '<path d="M10 6h10M10 12h10M10 18h10"/><circle cx="5" cy="6" r="1.5"/><circle cx="5" cy="12" r="1.5"/><circle cx="5" cy="18" r="1.5"/>',
	more: '<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>', plus: '<path d="M12 5v14M5 12h14"/>', minus: '<path d="M5 12h14"/>',
	check: '<path d="M4 12l5 5L20 6"/>', save: '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>', x: '<path d="M6 6l12 12M18 6L6 18"/>', file: '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/>',
	grid: '<path d="M4 4h16v16H4zM4 10h16M4 15h16M10 4v16M15 4v16"/>', trash: '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
	mic: '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>', micOff: '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M4 4l16 16"/>',
	cam: '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>', camOff: '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3zM3 3l18 18"/>',
	board: '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M7 13l3-3 2 2 4-4M8 21l4-4 4 4"/>', end: '<path d="M3 14c5-5 13-5 18 0l-2 3-4-2v-2a10 10 0 0 0-6 0v2l-4 2z"/>',
};

function el(tag, props, ...kids) {
	const e = document.createElement(tag);
	for (const [k, v] of Object.entries(props || {})) {
		if (v == null || v === false) continue;
		if (k === 'text') e.textContent = String(v); else if (k === 'cls') e.className = v; else e.setAttribute(k, v === true ? '' : String(v));
	}
	for (const c of kids) if (c) e.appendChild(c);
	return e;
}
function sv(tag, attrs) { const e = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs || {})) if (v != null) e.setAttribute(k, String(v)); return e; }
function ico(k, size = 21, w = 2) { const s = sv('svg', { 'aria-hidden': 'true', width: size, height: size, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }); s.innerHTML = ICONS[k]; return s; } // constant strings of this file only
const btn = (cls, label, ...kids) => el('button', { type: 'button', cls, 'aria-label': label || null }, ...kids);
const rid = () => Math.random().toString(36).slice(2, 10);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const n1 = (v) => Math.round(v * 10) / 10;
const n3 = (v) => Math.round(v * 1000) / 1000;
const fin = (v) => typeof v === 'number' && Number.isFinite(v) && Math.abs(v) < 1e6;
const pt = (q) => Array.isArray(q) && q.length === 2 && fin(q[0]) && fin(q[1]);
const clip = (s, n) => (typeof s === 'string' ? s.replace(/[\u0000-\u001F\u007F‪-‮⁦-⁩]/g, ' ').trim().slice(0, n) : '');
const initials = (n) => String(n || '').trim().split(/\s+/).slice(0, 2).map((w) => w.charAt(0)).join('') || '?';
const first = (n) => String(n || '').trim().split(/\s+/)[0] || '';
const fmtM = (m) => (Math.round(m * 100) / 100).toFixed(2);
const segD = (p, a, b) => { const dx = b[0] - a[0], dy = b[1] - a[1], l = dx * dx + dy * dy; const t = l ? clamp(((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l, 0, 1) : 0; return Math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy); };
const len = (o) => Math.hypot(o.b[0] - o.a[0], o.b[1] - o.a[1]);
/** "0.80", "0,8", "80 ס״מ", "80cm", "800 מ״מ" to metres; 0 when it is not a length */
export function parseLen(s) {
	s = String(s || '').replace(',', '.').trim(); const m = /(\d+(?:\.\d+)?|\.\d+)/.exec(s); if (!m) return 0;
	let v = parseFloat(m[1]); if (/ס\s*["״'׳]?\s*מ|cm/i.test(s)) v /= 100; else if (/מ\s*["״'׳]\s*מ|mm/i.test(s)) v /= 1000;
	return v >= 0.01 && v <= 500 ? n3(v) : 0;
}
// a mark from the network, copied field by field so nothing else travels on in a sync
function clean(o) {
	if (!o || typeof o !== 'object' || typeof o.id !== 'string' || !OID.test(o.id) || !KINDS.includes(o.k) || !PENS.includes(o.c) || !fin(o.s) || o.s <= 0 || !Number.isFinite(o.ts) || o.ts < 0 || o.ts > 1e14) return null;
	const c = { id: o.id, k: o.k, c: o.c, s: clamp(o.s, 0.02, 40), ts: o.ts, by: typeof o.by === 'string' && PID.test(o.by) ? o.by : '' };
	if (o.k === 'pen' || o.k === 'mark') { if (!Array.isArray(o.p) || o.p.length < 2 || o.p.length > 4000 || !o.p.every(pt)) return null; c.p = o.p.map((q) => [n1(q[0]), n1(q[1])]); }
	else { if (!pt(o.a) || (o.k !== 'note' && !pt(o.b))) return null; c.a = [n1(o.a[0]), n1(o.a[1])]; if (o.k !== 'note') c.b = [n1(o.b[0]), n1(o.b[1])]; }
	if (o.k === 'note') { c.t = clip(o.t, 160); if (!c.t) return null; c.n = clip(o.n, 40); c.l = clip(o.l, 40); c.d = o.d === true; }
	if (o.k === 'measure' && o.ref != null) { if (!fin(o.ref) || o.ref < 0.01 || o.ref > 500) return null; c.ref = n3(o.ref); }
	return c;
}
function cleanBg(bg) {
	if (!bg || typeof bg !== 'object' || typeof bg.src !== 'string' || bg.src.length > MAXIMG || !/^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/]+=*$/.test(bg.src)) return null;
	if (!fin(bg.w) || !fin(bg.h)) return null;
	return { src: bg.src, w: clamp(Math.round(bg.w), 100, 4000), h: clamp(Math.round(bg.h), 100, 4000), n: clip(bg.n, 40) };
}

/**
 * The board of one call. Created when the call starts (it listens from the first moment), shown on open().
 * @param {object} o
 * @param {object} o.tr      the call transport (livekitTransport of assets/designer/call.js)
 * @param {string} [o.title] the discussion title for the bar
 * @param {number} [o.t0]    call start time (ms) for the timer
 * @param {function} [o.face] id => { name, label } as the call screen knows the person
 * @param {object} [o.call]  { mic(on), cam(on), leave() } the call screen's own controls; a missing one is not shown
 * @param {function} [o.onClose] called after the board closes (the call screen returns the focus to its "לוח" button)
 */
export function createBoard({ tr, title = '', t0 = Date.now(), face, call = {}, onClose } = {}) {
	const S = { W: 1200, H: 1200, bg: null, objs: new Map(), order: [], tool: 'pen', shape: 'rect', shown: false, view: null, vw: 0, vh: 0, peers: new Map(), alive: true,
		scale: null, recal: false, lead: false, follow: '', fv: null, clearArm: 0, desk: false, big: '', hinted: false, nums: new Map(), callout: '', place: '' };
	const parts = () => { try { return tr.participants() || []; } catch (e) { return []; } };
	const meId = () => { const p = parts().find((x) => x.local); return p ? p.id : ''; };
	const who = (id) => { let f = null; try { f = face ? face(id) : null; } catch (e) { f = null; } const p = parts().find((x) => x.id === id); return { name: clip((f && f.name) || (p && p.name) || '', 40), label: clip((f && f.label) || '', 40) }; };
	const colorOf = (id) => { const ps = parts().slice().sort((a, b) => (a.joined || 0) - (b.joined || 0) || (a.id < b.id ? -1 : 1)); const i = ps.findIndex((p) => p.id === id); return PENS[(i < 0 ? 0 : i) % PENS.length]; };
	const myColor = () => colorOf(meId());
	const send = (m, reliable = true, to) => { try { tr.publishData(TOPIC, m, { reliable, to }); } catch (e) { /* the call went away */ } };
	const mq = window.matchMedia ? window.matchMedia('(min-width:900px)') : { matches: false };

	/* ---------------- the DOM, built once ---------------- */
	const svg = sv('svg', { class: 'nlfsb-svg', role: 'img', 'aria-label': T.sheetA });
	const defs = sv('defs'), pat = sv('pattern', { id: 'nlfsb-grid', width: 20, height: 20, patternUnits: 'userSpaceOnUse' }), patP = sv('path', { fill: 'none', stroke: '#E3E8EB', 'stroke-width': 1 });
	pat.appendChild(patP); defs.appendChild(pat);
	const gBg = sv('g'), gObj = sv('g'), gPin = sv('g'), gLive = sv('g', { class: 'nlfsb-live', 'pointer-events': 'none' });
	svg.append(defs, gBg, gObj, gPin, gLive);
	const backB = btn('nlfsb-back', T.back, ico('back', 20, 2.2));
	const titleT = el('b', { text: title || T.board }), subT = el('small', { text: T.sub }), timerT = el('span', { cls: 'nlfsb-time', role: 'timer', 'aria-label': T.timer, text: '00:00' });
	const hPhoto = btn('nlfsb-hb', null, el('span', { text: T.photoD })), hClear = btn('nlfsb-hb', null, el('span', { text: T.clear })), hSave = btn('nlfsb-hb', null, el('span', { text: T.save }));
	const head = el('div', { cls: 'nlfsb-head' }, backB, el('div', { cls: 'nlfsb-tt' }, titleT, subT), timerT, el('div', { cls: 'nlfsb-hbs' }, hPhoto, hClear, hSave));
	// the tool dock (phone) / rail (desktop)
	const toolB = {};
	const toolsBox = el('div', { cls: 'nlfsb-tools' });
	for (const k of ['pen', 'mark', 'arrow', 'shape', 'note', 'measure', 'laser', 'erase', 'hand']) { const b = btn('nlfsb-tb', T.tn[k], ico(k === 'shape' ? 'shape' : k)); b.setAttribute('aria-pressed', 'false'); b.dataset.k = k; toolB[k] = b; toolsBox.appendChild(b); }
	const meDot = el('span', { cls: 'nlfsb-dot' }), meB = btn('nlfsb-tb nlfsb-meb', '', meDot);
	const undoB = btn('nlfsb-tb nlfsb-undo', T.undo, ico('undo'));
	const dock = el('div', { cls: 'nlfsb-dock', role: 'toolbar', 'aria-label': T.tools }, toolsBox, el('span', { cls: 'nlfsb-sep', 'aria-hidden': 'true' }), meB, undoB);
	// the sheet
	const tilesBox = el('div', { cls: 'nlfsb-tiles' });
	const followB = btn('nlfsb-follow', null, ico('eye', 16, 2.2), el('span'));
	const row = el('div', { cls: 'nlfsb-row' }, tilesBox, followB);
	const blockSheet = el('span', { cls: 'nlfsb-v' }), blockScale = el('span', { cls: 'nlfsb-v' });
	const block = el('div', { cls: 'nlfsb-block' }, el('span', { cls: 'nlfsb-k', text: T.sheet }), blockSheet, el('span', { cls: 'nlfsb-k', text: T.scale }), blockScale);
	const zIn = btn('nlfsb-zb', T.zin, ico('plus', 20, 2.4)), zOut = btn('nlfsb-zb', T.zout, ico('minus', 20, 2.4)), zRecal = btn('nlfsb-zb nlfsb-zr', T.recalA, el('span', { text: T.recal }));
	const zoomBox = el('div', { cls: 'nlfsb-zoom' }, zIn, zOut, zRecal);
	const toast = el('p', { cls: 'nlfsb-toast', role: 'status', 'aria-live': 'polite', hidden: true });
	const callout = el('div', { cls: 'nlfsb-call', hidden: true });
	const sheet = el('div', { cls: 'nlfsb-sheet' }, svg, row, callout, block, zoomBox, toast);
	// notes (desktop side column; the same list opens in a sheet on a phone)
	const notesCount = el('span', { cls: 'nlfsb-cnt' }), notesList = el('ol', { cls: 'nlfsb-list' });
	const deskIn = el('input', { id: 'nlfsb-din', type: 'text', maxlength: 160, autocomplete: 'off', placeholder: T.deskIn });
	const notesPanel = el('section', { cls: 'nlfsb-notes', 'aria-labelledby': 'nlfsb-nh' }, el('div', { cls: 'nlfsb-nhd' }, el('h2', { id: 'nlfsb-nh', text: T.notesH }), notesCount), notesList,
		el('div', { cls: 'nlfsb-nin' }, el('label', { for: 'nlfsb-din', cls: 'nlfsb-sr', text: T.deskInL }), deskIn));
	const deskTiles = el('div', { cls: 'nlfsb-dtiles' });
	// call controls
	const cMic = btn('nlfsb-cb', ''), cCam = btn('nlfsb-cb', ''), cBoard = btn('nlfsb-cbb', T.boardOn, ico('board', 20), el('span', { text: T.lBoard })), cEnd = btn('nlfsb-cend', T.end, ico('end', 24));
	cBoard.setAttribute('aria-pressed', 'true');
	cMic.hidden = typeof call.mic !== 'function'; cCam.hidden = typeof call.cam !== 'function'; cEnd.hidden = typeof call.leave !== 'function';
	const ctl = el('div', { cls: 'nlfsb-ctl' }, cMic, cCam, cBoard, cEnd);
	const aside = el('aside', { cls: 'nlfsb-aside' }, deskTiles, notesPanel);
	const main = el('div', { cls: 'nlfsb-main' }, dock, sheet, aside);
	const pPhoto = btn('nlfsb-ob', null, ico('camera', 19), el('span', { text: T.photo })), pNotes = btn('nlfsb-ob', null, ico('list', 19), el('span', { text: T.notes }), el('b', { cls: 'nlfsb-badge', hidden: true }));
	const pMore = btn('nlfsb-ob nlfsb-om', T.more, ico('more', 20));
	const acts = el('div', { cls: 'nlfsb-acts' }, pPhoto, pNotes, pMore);
	const ctlHome = el('div', { cls: 'nlfsb-ctlh' }, ctl);
	const camIn = el('input', { type: 'file', accept: 'image/*', capture: 'environment', hidden: true, tabindex: '-1' }), fileIn = el('input', { type: 'file', accept: 'image/*', hidden: true, tabindex: '-1' });
	const modal = el('div', { cls: 'nlfsb-mod', hidden: true });
	const root = el('div', { cls: 'nlfsb', dir: 'rtl', lang: 'he', role: 'dialog', 'aria-modal': 'true', 'aria-label': T.board, hidden: true }, head, main, acts, ctlHome, camIn, fileIn, modal);
	const nudgeT = el('span'), nudgeDot = el('i', { cls: 'nlfsb-ndot', 'aria-hidden': 'true' }), nudgeGo = btn('nlfsb-ngo', null, el('span', { text: T.see })), nudgeX = btn('nlfsb-nx', T.close, ico('x', 18));
	const nudge = el('div', { cls: 'nlfsb-nudge', dir: 'rtl', lang: 'he', role: 'status', hidden: true }, nudgeDot, nudgeT, nudgeGo, nudgeX);
	const style = el('link', { rel: 'stylesheet', href: CSS_URL });
	if (CSS_URL && !document.querySelector('link[href="' + CSS_URL + '"]')) document.head.appendChild(style);
	document.body.append(root, nudge);

	let toastT = 0;
	const flash = (t, ms = 3200) => { clearTimeout(toastT); toast.textContent = t; toast.hidden = false; toastT = setTimeout(() => { toast.hidden = true; }, ms); };

	/* ---------------- view (viewBox) ---------------- */
	const pxU = () => (S.view && S.vw ? S.view.w / S.vw : 1);
	const applyView = () => {
		const v = S.view; if (!v) return;
		svg.setAttribute('viewBox', [v.x, v.y, v.w, v.h].map(n3).join(' '));
		const k = pxU(), gs = n3(18 * Math.pow(2, Math.round(Math.log2(k)))); // the grid stays about 16 to 20 screen pixels like squared paper
		pat.setAttribute('width', gs); pat.setAttribute('height', gs); patP.setAttribute('d', 'M' + gs + ' 0H0V' + gs); patP.setAttribute('stroke-width', n3(k));
		for (const p of S.peers.values()) p.g.setAttribute('transform', 'translate(' + p.x + ' ' + p.y + ') scale(' + n3(k) + ')');
		placeCallout();
		if (S.lead) sendView();
	};
	const stageR = () => { const r = sheet.getBoundingClientRect(); S.vw = r.width; S.vh = r.height; return r; };
	function fit() {
		const r = stageR(); if (!r.width || !r.height) return;
		const top = S.desk ? 0 : Math.min(140, r.height * 0.25); // on a phone the video tiles float on the sheet's top edge
		const a = r.width / (r.height - top), W = S.W * 1.06, H = S.H * 1.06;
		let w, h; if (W / H > a) { w = W; h = W / a; } else { h = H; w = H * a; }
		const k = w / r.width; S.view = { x: S.W / 2 - w / 2, y: S.H / 2 - h / 2 - top * k, w, h: h + top * k }; applyView();
	}
	function reView() { // a resize keeps the centre and the zoom
		const v = S.view, k = pxU(), r = stageR(); if (!v || !r.width) return fit();
		const cx = v.x + v.w / 2, cy = v.y + v.h / 2; S.view = { w: r.width * k, h: r.height * k, x: cx - r.width * k / 2, y: cy - r.height * k / 2 }; applyView();
	}
	const toBoard = (cx, cy) => { const m = svg.getScreenCTM(); if (!m) return [0, 0]; const p = new DOMPoint(cx, cy).matrixTransform(m.inverse()); return [n1(p.x), n1(p.y)]; };
	function zoomAt(cx, cy, f) {
		const v = S.view; if (!v) return; const [bx, by] = toBoard(cx, cy), M = Math.max(S.W, S.H);
		const nw = clamp(v.w / f, M / 25, M * 6), k = nw / v.w; S.view = { w: nw, h: v.h * k, x: bx - (bx - v.x) * k, y: by - (by - v.y) * k }; applyView();
	}
	const zoomMid = (f) => { const r = sheet.getBoundingClientRect(); zoomAt(r.left + r.width / 2, r.top + r.height / 2, f); };
	const vArr = () => [S.view.x, S.view.y, S.view.w, S.view.h].map(n1);
	let lvT = 0, lvQ = 0;
	function sendView() { if (!S.view) return; const now = Date.now(); clearTimeout(lvQ); if (now - lvT > 110) { lvT = now; send({ t: 'view', v: vArr() }, false); } lvQ = setTimeout(() => send({ t: 'view', v: vArr() }), 350); }
	function followTo(v) {
		S.fv = v; if (!S.shown) return; const r = stageR(); if (!r.width) return; const a = r.width / r.height;
		let w = v[2], h = v[3]; if (w / h > a) h = w / a; else w = h * a; S.view = { x: v[0] + v[2] / 2 - w / 2, y: v[1] + v[3] / 2 - h / 2, w, h }; applyView();
	}

	/* ---------------- drawing ---------------- */
	function paintBg() {
		const big = { x: -1e5, y: -1e5, width: 2e5, height: 2e5 };
		gBg.replaceChildren(sv('rect', { ...big, fill: '#F7F9FA' }), sv('rect', { ...big, fill: 'url(#nlfsb-grid)' }));
		if (S.bg) {
			const im = sv('image', { x: 0, y: 0, width: S.W, height: S.H, preserveAspectRatio: 'none' }); im.setAttribute('href', S.bg.src);
			gBg.append(sv('rect', { x: 0, y: 0, width: S.W, height: S.H, fill: '#FFFFFF' }), im, sv('rect', { x: 0, y: 0, width: S.W, height: S.H, fill: 'none', stroke: '#101820', 'stroke-width': 1.5, 'vector-effect': 'non-scaling-stroke' }));
		}
	}
	const pathD = (p) => { let d = 'M' + p[0][0] + ' ' + p[0][1]; for (let i = 1; i < p.length; i++) { const a = p[i - 1], b = p[i]; d += 'Q' + a[0] + ' ' + a[1] + ' ' + n1((a[0] + b[0]) / 2) + ' ' + n1((a[1] + b[1]) / 2); } const l = p[p.length - 1]; return d + 'L' + l[0] + ' ' + l[1]; };
	const txt = (s, a) => { const t = sv('text', { 'font-family': 'Rubik, Assistant, Arial, sans-serif', 'font-weight': 700, 'text-anchor': 'middle', ...a }); t.textContent = s; return t; };
	function pill(g, x, y, s, c, u) { const fs = 13 * u, w = (s.length * 7.3 + 18) * u, h = 20 * u; g.append(sv('rect', { x: n1(x - w / 2), y: n1(y - h / 2), width: n1(w), height: n1(h), rx: n1(h / 2), fill: c }), txt(s, { x: n1(x), y: n1(y + fs * 0.36), 'font-size': n1(fs), fill: ink(c), direction: 'rtl' })); }
	function shape(o) {
		const c = o.c, u = o.s, g = sv('g', { 'data-id': o.id }), st = { fill: 'none', stroke: c, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
		if (o.k === 'pen' || o.k === 'mark') g.appendChild(sv('path', { ...st, d: pathD(o.p), 'stroke-width': n1((o.k === 'mark' ? 16 : 3.2) * u), 'stroke-opacity': o.k === 'mark' ? 0.4 : 1 }));
		else if (o.k === 'arrow') {
			const [x1, y1] = o.a, [x2, y2] = o.b, an = Math.atan2(y2 - y1, x2 - x1), L = 13 * u, hd = (d) => n1(x2 - L * Math.cos(an + d)) + ' ' + n1(y2 - L * Math.sin(an + d));
			g.appendChild(sv('path', { ...st, 'stroke-width': n1(3.2 * u), d: 'M' + x1 + ' ' + y1 + 'L' + x2 + ' ' + y2 + 'M' + hd(0.5) + 'L' + x2 + ' ' + y2 + 'L' + hd(-0.5) }));
		} else if (o.k === 'rect') g.appendChild(sv('rect', { ...st, x: Math.min(o.a[0], o.b[0]), y: Math.min(o.a[1], o.b[1]), width: n1(Math.abs(o.b[0] - o.a[0])), height: n1(Math.abs(o.b[1] - o.a[1])), rx: n1(3 * u), fill: c, 'fill-opacity': 0.08, 'stroke-width': n1(3 * u) }));
		else if (o.k === 'ell') g.appendChild(sv('ellipse', { ...st, cx: n1((o.a[0] + o.b[0]) / 2), cy: n1((o.a[1] + o.b[1]) / 2), rx: n1(Math.abs(o.b[0] - o.a[0]) / 2), ry: n1(Math.abs(o.b[1] - o.a[1]) / 2), fill: c, 'fill-opacity': 0.08, 'stroke-width': n1(3 * u) }));
		else if (o.k === 'measure') {
			const [x1, y1] = o.a, [x2, y2] = o.b, an = Math.atan2(y2 - y1, x2 - x1), nx = -Math.sin(an) * 8 * u, ny = Math.cos(an) * 8 * u;
			g.appendChild(sv('path', { ...st, 'stroke-width': n1(2.6 * u), d: 'M' + x1 + ' ' + y1 + 'L' + x2 + ' ' + y2 + 'M' + n1(x1 - nx) + ' ' + n1(y1 - ny) + 'L' + n1(x1 + nx) + ' ' + n1(y1 + ny) + 'M' + n1(x2 - nx) + ' ' + n1(y2 - ny) + 'L' + n1(x2 + nx) + ' ' + n1(y2 + ny) }));
			const lab = o.ref ? fmtM(o.ref) + ' מ׳' : S.scale ? 'בערך ' + fmtM(len(o) / S.scale.u) + ' מ׳' : '';
			if (lab) pill(g, (x1 + x2) / 2, (y1 + y2) / 2, lab, c, u);
		} else if (o.k === 'note') {
			const r = 11 * u; g.setAttribute('opacity', o.d ? 0.45 : 1);
			g.append(sv('circle', { cx: o.a[0], cy: o.a[1], r: n1(r), fill: c, stroke: '#FFFFFF', 'stroke-width': n1(2 * u) }), txt(String(S.nums.get(o.id) || ''), { x: o.a[0], y: n1(o.a[1] + 4.3 * u), 'font-size': n1(12 * u), fill: ink(c) }));
		}
		return g;
	}
	const notes = () => S.order.map((id) => S.objs.get(id)).filter((o) => o && o.k === 'note').sort((a, b) => a.ts - b.ts || (a.id < b.id ? -1 : 1));
	function rescale() {
		let best = null; for (const o of S.objs.values()) if (o.k === 'measure' && o.ref && (!best || o.ts > best.ts || (o.ts === best.ts && o.id > best.id))) best = o;
		S.scale = best && len(best) > 0 ? { u: len(best) / best.ref, ref: best.ref } : null;
		S.nums = new Map(notes().map((o, i) => [o.id, i + 1]));
	}
	function paintObjs() {
		if (!S.shown) return;
		const all = S.order.map((id) => S.objs.get(id)).filter(Boolean);
		gObj.replaceChildren(...all.filter((o) => o.k !== 'note').map(shape)); gPin.replaceChildren(...all.filter((o) => o.k === 'note').map(shape));
		paintNotes(); paintBlock(); placeCallout();
	}

	/* ---------------- the marks: add, remove, ownership ---------------- */
	function addObj(raw, by) {
		const o = clean(raw); if (!o || S.objs.has(o.id) || S.objs.size >= MAXOBJ) return null;
		if (by) o.by = by; if (!o.by) return null;
		if (o.k === 'note') { if (notes().length >= MAXNOTES) return null; const f = who(o.by); if (f.name) { o.n = f.name; o.l = f.label || o.l; } }
		S.objs.set(o.id, o); S.order.push(o.id);
		if (o.k === 'note' || o.k === 'measure') { rescale(); paintObjs(); } else if (S.shown) gObj.appendChild(shape(o));
		return o;
	}
	function delObj(id, by) {
		const o = S.objs.get(id); if (!o || o.by !== by) return false;
		S.objs.delete(id); S.order = S.order.filter((x) => x !== id);
		if (S.callout === id) closeCallout();
		if (o.k === 'note' || o.k === 'measure') { rescale(); paintObjs(); } else { const n = gObj.querySelector('[data-id="' + id + '"]'); if (n) n.remove(); }
		return true;
	}
	function delMine(by) { for (const id of S.order.slice()) if (S.objs.get(id).by === by) { S.objs.delete(id); if (S.callout === id) closeCallout(); } S.order = S.order.filter((id) => S.objs.has(id)); rescale(); paintObjs(); }
	function clearAll() { S.objs.clear(); S.order = []; closeCallout(); rescale(); paintObjs(); }
	function setBg(bg) { S.bg = bg; S.W = bg ? bg.w : 1200; S.H = bg ? bg.h : 1200; paintBg(); paintBlock(); if (S.shown && !S.follow) fit(); }
	function commit(o) { o.by = meId(); o.ts = Date.now(); const c = addObj(o, o.by); if (c) send({ t: 'add', o: c }); return c; }
	const mine = () => S.order.filter((id) => S.objs.get(id).by === meId());

	/* ---------------- the other people: cursors, lasers ---------------- */
	function peer(id) {
		let p = S.peers.get(id); if (p) return p;
		const c = colorOf(id), g = sv('g'), trail = sv('path', { fill: 'none', stroke: c, 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-opacity': 0.35 }), tag = sv('text', { x: 0, y: -9, 'font-size': 12.5, 'font-weight': 700, fill: ink(c), 'text-anchor': 'middle', 'font-family': 'Assistant, Rubik, Arial, sans-serif', direction: 'rtl' });
		const pillR = sv('rect', { y: -22, height: 19, rx: 9.5, fill: c });
		const dot = sv('g'); dot.append(sv('circle', { r: 6, fill: c, stroke: '#FFFFFF', 'stroke-width': 2 }), pillR, tag);
		g.appendChild(dot); gLive.append(trail, g);
		p = { g, trail, tag, pillR, at: 0, x: 0, y: 0, pts: [] }; S.peers.set(id, p); return p;
	}
	function cursor(id, x, y) {
		const p = peer(id), name = first(who(id).name), w = name.length * 7 + 16, k = pxU();
		p.tag.textContent = name; p.tag.setAttribute('x', n1(8 + w / 2)); p.pillR.setAttribute('x', 8); p.pillR.setAttribute('width', n1(w));
		p.x = x; p.y = y; p.g.setAttribute('transform', 'translate(' + x + ' ' + y + ') scale(' + n3(k) + ')'); p.g.style.opacity = 1; p.trail.style.opacity = 1; p.at = Date.now();
		const l = p.pts[p.pts.length - 1]; if (l && Math.hypot(l[0] - x, l[1] - y) > 120 * k) p.pts = []; // a jump is not a trail
		p.pts.push([x, y]); if (p.pts.length > 10) p.pts.shift();
		if (p.pts.length > 1) { p.trail.setAttribute('d', pathD(p.pts)); p.trail.setAttribute('stroke-width', n1(5 * k)); }
	}
	const lasers = [];
	function laser(c, p) { if (p.length < 2) return; const path = sv('path', { class: 'nlfsb-las', d: pathD(p), fill: 'none', stroke: c, 'stroke-width': n1(5 * pxU()), 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-opacity': 0.9 }); gLive.appendChild(path); lasers.push({ path, t: Date.now() }); }
	const tick = setInterval(() => {
		const now = Date.now();
		for (let i = lasers.length - 1; i >= 0; i--) { const a = (now - lasers[i].t) / 1400; if (a >= 1) { lasers[i].path.remove(); lasers.splice(i, 1); } else lasers[i].path.setAttribute('stroke-opacity', String(n3(0.9 * (1 - a)))); }
		const ids = new Set(parts().map((x) => x.id));
		for (const [id, p] of S.peers) { if (now - p.at > 700 && p.pts.length) { p.pts = []; p.trail.setAttribute('d', ''); } if (now - p.at > 5000) { p.g.style.opacity = 0; p.trail.style.opacity = 0; p.pts = []; } if (!ids.has(id)) { p.g.remove(); p.trail.remove(); S.peers.delete(id); } }
		if (S.follow && !ids.has(S.follow)) stopFollow();
	}, 90);
	const clock = setInterval(() => { if (!S.shown) return; const s = Math.max(0, Math.floor((Date.now() - t0) / 1000)); timerT.textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); }, 1000);

	/* ---------------- what arrives from the others ---------------- */
	const onData = (topic, m, from) => {
		if (topic !== TOPIC || !m || typeof m !== 'object' || !S.alive || typeof from !== 'string' || !PID.test(from) || from === meId()) return;
		const t = m.t;
		if (t === 'add') addObj(m.o, from);
		else if (t === 'del' && typeof m.id === 'string') delObj(m.id, from);
		else if (t === 'mine') delMine(from);
		else if (t === 'done' && typeof m.id === 'string') { const o = S.objs.get(m.id); if (o && o.k === 'note') { o.d = m.v === true; paintObjs(); } }
		else if (t === 'bg') { const bg = m.bg == null ? null : cleanBg(m.bg); if (m.bg != null && !bg) return; if (bg) bg.n = who(from).name || bg.n; clearAll(); setBg(bg); if (bg) flash(T.got(first(bg.n))); }
		else if (t === 'cur' && S.shown && fin(m.x) && fin(m.y)) cursor(from, m.x, m.y);
		else if (t === 'las' && S.shown && Array.isArray(m.p) && m.p.length <= 400 && m.p.every(pt)) laser(colorOf(from), m.p);
		else if (t === 'open' && !S.shown) showNudge(from);
		else if (t === 'sync?') answerSync(from);
		else if (t === 'sync' && Array.isArray(m.objs)) { if (m.bg != null) { const bg = cleanBg(m.bg); if (bg && !S.bg) setBg(bg); } m.objs.slice(0, MAXOBJ).forEach((o) => addObj(o, null)); }
		else if (t === 'lead') { if (m.on === true) { S.lead = false; S.follow = from; paintFollow(); if (Array.isArray(m.v) && m.v.length === 4 && m.v.every(fin) && m.v[2] > 0 && m.v[3] > 0) followTo(m.v); } else if (S.follow === from) stopFollow(); }
		else if (t === 'view' && S.follow === from && Array.isArray(m.v) && m.v.length === 4 && m.v.every(fin) && m.v[2] > 0 && m.v[3] > 0) followTo(m.v);
	};
	tr.onData(onData);
	// a newcomer asks once; the person who has been in the room longest (among those who are not asking) answers with everything
	function answerSync(from) {
		if (S.lead) send({ t: 'lead', on: true, v: S.view ? vArr() : null }, true, [from]);
		if (!S.bg && !S.objs.size) return;
		const ps = parts().filter((p) => p.id !== from).sort((a, b) => (a.joined || 0) - (b.joined || 0) || (a.id < b.id ? -1 : 1));
		if (!ps.length || !ps[0].local) return;
		send({ t: 'sync', bg: S.bg, objs: S.order.map((id) => S.objs.get(id)) }, true, [from]);
	}
	send({ t: 'sync?' });
	if (typeof tr.onState === 'function') tr.onState((s) => { if (s === 'connected' && S.alive) send({ t: 'sync?' }); }); // a reconnect keeps the board and fills what was missed

	/* ---------------- the pointer ---------------- */
	const pts = new Map(); let G = null, pinch = null, lastCur = 0, notMineT = 0;
	function drawDraft(o) { gLive.querySelectorAll('.nlfsb-draft').forEach((n) => n.remove()); if (!o) return; const g = shape(o); g.setAttribute('class', 'nlfsb-draft'); gLive.appendChild(g); }
	function hitObj(x, y, list) {
		const tol = 10 * pxU(), p = [x, y];
		for (let i = list.length - 1; i >= 0; i--) {
			const o = S.objs.get(list[i]); if (!o) continue; const w = tol + (o.k === 'mark' ? 8 : 2) * o.s;
			if (o.k === 'note') { if (Math.hypot(x - o.a[0], y - o.a[1]) < Math.max(14 * o.s, 16 * pxU())) return o; continue; }
			if (o.p) { for (let j = 1; j < o.p.length; j++) if (segD(p, o.p[j - 1], o.p[j]) < w) return o; continue; }
			if (o.k === 'arrow' || o.k === 'measure') { if (segD(p, o.a, o.b) < w) return o; continue; }
			const x0 = Math.min(o.a[0], o.b[0]), x1 = Math.max(o.a[0], o.b[0]), y0 = Math.min(o.a[1], o.b[1]), y1 = Math.max(o.a[1], o.b[1]);
			if (o.k === 'rect' && x >= x0 - w && x <= x1 + w && y >= y0 - w && y <= y1 + w) return o;
			if (o.k === 'ell') { const rx = (x1 - x0) / 2 + w, ry = (y1 - y0) / 2 + w; if (((x - (x0 + x1) / 2) / rx) ** 2 + ((y - (y0 + y1) / 2) / ry) ** 2 <= 1) return o; }
		}
		return null;
	}
	const hitPin = (x, y) => hitObj(x, y, notes().map((o) => o.id));
	function eraseAt(x, y) {
		const o = hitObj(x, y, mine());
		if (o) { delObj(o.id, o.by); send({ t: 'del', id: o.id }); return; }
		if (hitObj(x, y, S.order) && Date.now() - notMineT > 2500) { notMineT = Date.now(); flash(T.notMine); }
	}
	svg.addEventListener('pointerdown', (ev) => {
		if (ev.pointerType === 'mouse' && ev.button !== 0 && ev.button !== 1) return;
		try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* a pointer the browser no longer tracks */ }
		if (ev.isPrimary) { pts.clear(); pinch = null; }
		pts.set(ev.pointerId, [ev.clientX, ev.clientY]);
		if (S.follow) stopFollow();
		if (pts.size === 2) { G = null; drawDraft(null); const [a, b] = [...pts.values()]; pinch = { d: Math.hypot(a[0] - b[0], a[1] - b[1]), m: [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2] }; return; }
		if (pts.size > 2) return;
		const [x, y] = toBoard(ev.clientX, ev.clientY), u = n3(pxU()), c = myColor(), tool = ev.button === 1 ? 'hand' : S.tool;
		G = { sx: ev.clientX, sy: ev.clientY, x, y, moved: false, tool, v: { ...S.view } };
		if (tool === 'erase') eraseAt(x, y);
		else if (tool === 'laser') { G.las = [[x, y]]; G.sent = 0; }
		else if (tool === 'pen' || tool === 'mark') G.o = { id: rid(), k: tool, c, s: u, p: [[x, y]] };
		else if (tool === 'arrow' || tool === 'shape' || tool === 'measure') G.o = { id: rid(), k: tool === 'shape' ? S.shape : tool, c, s: u, a: [x, y], b: [x, y] };
	});
	svg.addEventListener('pointermove', (ev) => {
		if (pts.has(ev.pointerId)) pts.set(ev.pointerId, [ev.clientX, ev.clientY]);
		const [x, y] = toBoard(ev.clientX, ev.clientY), now = Date.now();
		if (S.shown && now - lastCur > 70) { lastCur = now; send({ t: 'cur', x, y }, false); }
		if (pinch && pts.size === 2) {
			const [a, b] = [...pts.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]), m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
			if (d > 10) { zoomAt(m[0], m[1], d / pinch.d); const k = pxU(); S.view.x -= (m[0] - pinch.m[0]) * k; S.view.y -= (m[1] - pinch.m[1]) * k; applyView(); pinch = { d, m }; }
			return;
		}
		if (!G || !pts.has(ev.pointerId)) return;
		if (Math.hypot(ev.clientX - G.sx, ev.clientY - G.sy) > 6) G.moved = true;
		if (G.tool === 'hand') { const k = G.v.w / (S.vw || 1); S.view = { ...G.v, x: G.v.x - (ev.clientX - G.sx) * k, y: G.v.y - (ev.clientY - G.sy) * k }; applyView(); return; }
		if (G.tool === 'erase') { eraseAt(x, y); return; }
		if (G.las) { G.las.push([x, y]); if (G.las.length - G.sent >= 4) { const part = G.las.slice(Math.max(0, G.sent - 1)).slice(-400); laser(myColor(), part); send({ t: 'las', p: part }, false); G.sent = G.las.length; } return; }
		if (!G.o || !G.moved) return;
		if (G.o.p) { const l = G.o.p[G.o.p.length - 1]; if (Math.hypot(l[0] - x, l[1] - y) > 1.5 * pxU() && G.o.p.length < 4000) G.o.p.push([x, y]); } else G.o.b = [x, y];
		drawDraft(G.o);
	});
	const up = async (ev) => {
		pts.delete(ev.pointerId);
		if (pinch) { if (pts.size < 2) pinch = null; G = null; return; }
		const g = G; G = null; drawDraft(null); if (!g) return;
		if (!g.moved && g.tool !== 'erase') { const pin = hitPin(g.x, g.y); if (pin) { openCallout(pin.id); return; } if (g.tool === 'note') { placeNote(g.x, g.y); return; } }
		const o = g.o; if (!o || !g.moved) return;
		if (o.p ? o.p.length < 2 : Math.hypot(o.b[0] - o.a[0], o.b[1] - o.a[1]) < 8 * pxU()) return;
		if (o.k === 'measure' && (!S.scale || S.recal)) { drawDraft(o); const v = await askLen(); drawDraft(null); S.recal = false; if (v === null) return; if (v) o.ref = v; }
		commit(o);
	};
	svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', (ev) => { pts.delete(ev.pointerId); G = null; pinch = null; drawDraft(null); });
	svg.addEventListener('wheel', (ev) => { ev.preventDefault(); if (S.follow) stopFollow(); zoomAt(ev.clientX, ev.clientY, Math.exp(-clamp(ev.deltaY, -120, 120) / 300)); }, { passive: false });
	async function placeNote(x, y) {
		let t = clip(deskIn.value, 160);
		if (t) deskIn.value = ''; else t = clip(await askText(T.noteQ, T.notePh, T.ok), 160);
		if (!t) return; const f = who(meId());
		const o = commit({ id: rid(), k: 'note', c: myColor(), s: n3(pxU()), a: [x, y], t, n: f.name, l: f.label });
		if (o && !S.desk) openCallout(o.id);
	}

	/* ---------------- the small dialogs (text, length, confirm, menus) ---------------- */
	let modalBack = null, modalDone = null;
	function openModal(nodes, done, label) {
		closeModal(); modalBack = document.activeElement; modalDone = done || null;
		const card = el('div', { cls: 'nlfsb-card', role: 'dialog', 'aria-modal': 'true', 'aria-label': label || null }, ...nodes);
		modal.replaceChildren(card); modal.hidden = false;
		setTimeout(() => { const f = card.querySelector('input,button'); if (f) f.focus({ preventScroll: true }); }, 30);
		return card;
	}
	function closeModal(v) { if (modal.hidden) return; modal.hidden = true; modal.replaceChildren(); const d = modalDone; modalDone = null; if (d) d(v); if (modalBack && modalBack.focus && root.contains(modalBack)) modalBack.focus({ preventScroll: true }); }
	modal.addEventListener('click', (ev) => { if (ev.target === modal) closeModal(); });
	function askText(q, ph, go, check) {
		return new Promise((res) => {
			const inp = el('input', { type: 'text', maxlength: 160, autocomplete: 'off', placeholder: ph, id: 'nlfsb-ask' }), err = el('p', { cls: 'nlfsb-err', role: 'alert' });
			const f = el('form', { cls: 'nlfsb-form' }, el('label', { for: 'nlfsb-ask', cls: 'nlfsb-q', text: q }), inp, err,
				el('div', { cls: 'nlfsb-2' }, el('button', { type: 'submit', cls: 'nlfsb-pri', text: go }), el('button', { type: 'button', cls: 'nlfsb-sec', text: T.cancel })));
			f.addEventListener('submit', (ev) => { ev.preventDefault(); const v = inp.value.trim(); if (check) { const r = check(v); if (r === false) { err.textContent = T.lenBad; inp.focus(); return; } closeModal(r); } else closeModal(v); });
			f.querySelector('.nlfsb-sec').addEventListener('click', () => closeModal(check ? null : ''));
			openModal([f], (v) => res(v == null ? (check ? null : '') : v), q);
		});
	}
	const askLen = () => askText(T.lenQ, T.lenPh, T.set, (v) => (v ? parseLen(v) || false : 0)); // empty = a line without a number
	function confirmBox(q, yes) {
		return new Promise((res) => {
			const y = el('button', { type: 'button', cls: 'nlfsb-pri nlfsb-danger', text: yes }), n = el('button', { type: 'button', cls: 'nlfsb-sec', text: T.cancel });
			y.addEventListener('click', () => closeModal(true)); n.addEventListener('click', () => closeModal(false));
			openModal([el('p', { cls: 'nlfsb-q', text: q }), el('div', { cls: 'nlfsb-2' }, y, n)], (v) => res(v === true), q);
		});
	}
	function menu(head, items) {
		const list = items.filter(Boolean).map((it) => { const b = el('button', { type: 'button', cls: 'nlfsb-mi' + (it.danger ? ' is-danger' : '') }, ico(it.i, 20), el('span', { text: it.l })); b.addEventListener('click', () => { closeModal(); it.f(); }); return b; });
		const x = el('button', { type: 'button', cls: 'nlfsb-sec', text: T.close }); x.addEventListener('click', () => closeModal());
		openModal([el('h2', { cls: 'nlfsb-mh', text: head }), ...list, x], null, head);
	}

	/* ---------------- notes: list, callout, agreed, delete ---------------- */
	function noteRow(o, inSheet) {
		const c = o.c, f = { name: o.n, label: o.l }, isMine = o.by === meId();
		const dB = el('button', { type: 'button', cls: 'nlfsb-lk', 'aria-pressed': o.d ? 'true' : 'false', text: o.d ? T.reopen : T.done });
		dB.addEventListener('click', () => setDone(o.id, !o.d));
		const tools = el('div', { cls: 'nlfsb-nts' }, dB);
		if (isMine) { const x = el('button', { type: 'button', cls: 'nlfsb-lk is-danger', text: T.del }); x.addEventListener('click', () => delNote(o.id)); tools.appendChild(x); }
		const body = el('div', { cls: 'nlfsb-nb' }, el('div', { cls: 'nlfsb-nah' }, el('span', { cls: 'nlfsb-na', style: 'color:' + DARK[c], text: [f.name, f.label].filter(Boolean).join(' · ') }), tools), el('span', { cls: 'nlfsb-nt' + (o.d ? ' is-done' : ''), text: o.t }));
		if (o.d) body.appendChild(el('span', { cls: 'nlfsb-ndone' }, ico('check', 14, 3), el('span', { text: T.doneTag })));
		const num = el('button', { type: 'button', cls: 'nlfsb-num', style: 'background-color:' + c + ' !important;color:' + ink(c) + ' !important', 'aria-label': 'הערה ' + S.nums.get(o.id) + ' על התוכנית', text: String(S.nums.get(o.id)) });
		num.addEventListener('click', () => { if (inSheet) closeModal(); goPin(o.id); });
		return el('li', { cls: 'nlfsb-ni' }, num, body);
	}
	function paintNotes() {
		const ns = notes(), d = ns.filter((o) => o.d).length;
		notesCount.textContent = ns.length ? T.count(ns.length, d) : '';
		notesList.replaceChildren(...(ns.length ? ns.map((o) => noteRow(o)) : [el('li', { cls: 'nlfsb-none', text: T.none })]));
		const open = ns.length - d, badge = pNotes.querySelector('.nlfsb-badge'); badge.textContent = String(open); badge.hidden = !open;
		pNotes.setAttribute('aria-label', T.notes + (ns.length ? ', ' + T.count(ns.length, d) : ''));
	}
	function notesSheet() { const ns = notes(); openModal([el('h2', { cls: 'nlfsb-mh', text: T.notesH }), el('p', { cls: 'nlfsb-cnt', text: ns.length ? T.count(ns.length, ns.filter((o) => o.d).length) : '' }), el('ol', { cls: 'nlfsb-list' }, ...(ns.length ? ns.map((o) => noteRow(o, true)) : [el('li', { cls: 'nlfsb-none', text: T.none })])), (() => { const x = el('button', { type: 'button', cls: 'nlfsb-sec', text: T.close }); x.addEventListener('click', () => closeModal()); return x; })()], null, T.notesH); }
	function setDone(id, v) { const o = S.objs.get(id); if (!o || o.k !== 'note') return; o.d = v; paintObjs(); send({ t: 'done', id, v }); if (!modal.hidden && !S.desk) notesSheet(); if (S.callout === id) openCallout(id); }
	function delNote(id) { const o = S.objs.get(id); if (!o || o.by !== meId()) return; delObj(id, o.by); send({ t: 'del', id }); if (!modal.hidden && !S.desk) notesSheet(); }
	function goPin(id) { const o = S.objs.get(id); if (!o || !S.view) return; if (S.follow) stopFollow(); S.view = { ...S.view, x: o.a[0] - S.view.w / 2, y: o.a[1] - S.view.h / 2 }; applyView(); openCallout(id); }
	function openCallout(id) {
		const o = S.objs.get(id); if (!o || o.k !== 'note') return; S.callout = id;
		const c = o.c, x = btn('nlfsb-cx', T.close, ico('x', 16, 2.4)); x.addEventListener('click', closeCallout);
		const dB = el('button', { type: 'button', cls: 'nlfsb-lk', 'aria-pressed': o.d ? 'true' : 'false', text: o.d ? T.reopen : T.done }); dB.addEventListener('click', () => setDone(id, !o.d));
		const tools = el('div', { cls: 'nlfsb-nts' }, dB);
		if (o.by === meId()) { const d = el('button', { type: 'button', cls: 'nlfsb-lk is-danger', text: T.del }); d.addEventListener('click', () => delNote(id)); tools.appendChild(d); }
		callout.style.setProperty('--c', c);
		callout.replaceChildren(el('span', { cls: 'nlfsb-ch', style: 'color:' + DARK[c] }, el('span', { cls: 'nlfsb-cn', style: 'background:' + c + ';color:' + ink(c), text: String(S.nums.get(id)) }), el('span', { text: [first(o.n), o.l].filter(Boolean).join(' · ') })),
			el('span', { cls: 'nlfsb-ct' + (o.d ? ' is-done' : ''), text: o.t }), tools, x);
		callout.hidden = false; placeCallout();
	}
	function closeCallout() { S.callout = ''; callout.hidden = true; }
	function placeCallout() {
		if (callout.hidden || !S.callout || !S.view) return; const o = S.objs.get(S.callout); if (!o) return closeCallout();
		const k = pxU(), px = (o.a[0] - S.view.x) / k, py = (o.a[1] - S.view.y) / k, w = callout.offsetWidth || 220, h = callout.offsetHeight || 120;
		const left = clamp(px - w + 16, 8, S.vw - w - 8), top = py + 18 + h > S.vh - 8 ? clamp(py - h - 18, 8, S.vh - h - 8) : py + 18;
		callout.style.left = n1(left) + 'px'; callout.style.top = n1(top) + 'px';
	}

	/* ---------------- the title block, follow, tiles, call controls ---------------- */
	function paintBlock() {
		blockSheet.textContent = S.bg ? T.planOf(first(S.bg.n)) : T.blank;
		blockScale.textContent = S.scale ? T.scaleBy(fmtM(S.scale.ref)) + (S.desk ? T.approx : '') : T.noScale;
		zRecal.hidden = !S.scale;
	}
	function paintFollow() {
		const s = followB.querySelector('span');
		if (S.follow) { s.textContent = T.following(first(who(S.follow).name)); followB.setAttribute('aria-pressed', 'true'); }
		else if (S.lead) { s.textContent = T.leading; followB.setAttribute('aria-pressed', 'true'); }
		else { s.textContent = T.follow; followB.setAttribute('aria-pressed', 'false'); }
		followB.classList.toggle('is-on', !!(S.follow || S.lead));
	}
	function stopFollow() { if (!S.follow) return; S.follow = ''; S.fv = null; paintFollow(); }
	function stopLead() { if (!S.lead) return; S.lead = false; send({ t: 'lead', on: false }); paintFollow(); }
	followB.addEventListener('click', () => {
		if (S.follow) return stopFollow();
		if (S.lead) return stopLead();
		S.lead = true; send({ t: 'lead', on: true, v: S.view ? vArr() : null }); paintFollow();
	});
	const vids = new Map();
	function tile(p) {
		const c = colorOf(p.id), f = who(p.id), big = p.id === S.big;
		let v = vids.get(p.id); if (!v) { v = el('video', { playsinline: true, autoplay: true }); v.muted = true; vids.set(p.id, v); }
		if (p.cam) { if (v.dataset.on !== '1') { try { if (typeof tr.attach === 'function' && tr.attach(p.id, 'camera', v) !== false) v.dataset.on = '1'; } catch (e) { /* the track is not there yet */ } } }
		else v.dataset.on = '';
		v.hidden = !p.cam || v.dataset.on !== '1';
		const lab = (S.desk ? [f.name, f.label].filter(Boolean).join(' · ') : first(f.name)) + (p.speaking ? ' · ' + T.speaking : '');
		const t = el('div', { cls: 'nlfsb-tile' + (big ? ' is-big' : '') + (p.speaking ? ' is-sp' : ''), style: '--c:' + c + ';--i:' + ink(c), role: 'img', 'aria-label': lab },
			el('span', { cls: 'nlfsb-ini', 'aria-hidden': 'true', text: initials(f.name) }), v, el('span', { cls: 'nlfsb-tn', 'aria-hidden': 'true', text: lab }));
		if (!v.hidden && v.paused) v.play().catch(() => {});
		return t;
	}
	function paintTiles() {
		if (!S.shown) return;
		const ps = parts().filter((p) => !p.local), sp = ps.find((p) => p.speaking);
		if (sp) S.big = sp.id; if (!ps.some((p) => p.id === S.big)) S.big = ps[0] ? ps[0].id : '';
		const list = ps.slice().sort((a, b) => (b.id === S.big) - (a.id === S.big)).slice(0, S.desk ? 5 : 3);
		tilesBox.replaceChildren(...list.map(tile));
		for (const id of [...vids.keys()]) if (!ps.some((p) => p.id === id)) vids.delete(id);
	}
	function paintCtl() {
		const me = parts().find((p) => p.local) || {}, c = myColor();
		cMic.replaceChildren(ico(me.mic ? 'mic' : 'micOff', 22)); cMic.setAttribute('aria-pressed', me.mic ? 'true' : 'false'); cMic.setAttribute('aria-label', me.mic ? T.micOn : T.micOff); cMic.classList.toggle('is-off', !me.mic);
		cCam.replaceChildren(ico(me.cam ? 'cam' : 'camOff', 22)); cCam.setAttribute('aria-pressed', me.cam ? 'true' : 'false'); cCam.setAttribute('aria-label', me.cam ? T.camOn : T.camOff); cCam.classList.toggle('is-off', !me.cam);
		meDot.style.background = c; meB.setAttribute('aria-label', T.myc(c));
	}
	cMic.addEventListener('click', async () => { const me = parts().find((p) => p.local) || {}; try { await call.mic(!me.mic); } catch (e) { /* the call screen says why */ } paintCtl(); });
	cCam.addEventListener('click', async () => { const me = parts().find((p) => p.local) || {}; try { await call.cam(!me.cam); } catch (e) { /* the call screen says why */ } paintCtl(); paintTiles(); });
	cEnd.addEventListener('click', () => { try { call.leave(); } catch (e) { /* closing */ } });
	cBoard.addEventListener('click', () => close());
	const onPeople = () => { if (!S.shown) return; paintTiles(); paintCtl(); };
	tr.onParticipants(onPeople);
	if (typeof tr.onSpeaking === 'function') tr.onSpeaking(onPeople);

	/* ---------------- the bar: tools, undo, clear, photo, save ---------------- */
	function pickTool(k) {
		if (k === 'shape' && S.tool === 'shape') S.shape = S.shape === 'rect' ? 'ell' : 'rect';
		S.tool = k; for (const [t, b] of Object.entries(toolB)) b.setAttribute('aria-pressed', t === k ? 'true' : 'false');
		toolB.shape.replaceChildren(ico(S.tool === 'shape' ? S.shape : 'shape', S.desk ? 22 : 21)); toolB.shape.setAttribute('aria-label', S.tool === 'shape' ? T[S.shape] : T.tn.shape);
		svg.dataset.tool = k;
	}
	toolsBox.addEventListener('click', (ev) => { const b = ev.target.closest('[data-k]'); if (b) pickTool(b.dataset.k); });
	meB.addEventListener('click', () => flash(T.myc(myColor())));
	function undo() { const ids = mine(); const id = ids[ids.length - 1]; if (id) { delObj(id, meId()); send({ t: 'del', id }); } }
	undoB.addEventListener('click', undo);
	function clearMine(b) {
		if (!mine().length) return;
		if (Date.now() - S.clearArm > 4000) { S.clearArm = Date.now(); flash(T.clearAgain, 4000); if (b) b.classList.add('is-armed'); setTimeout(() => b && b.classList.remove('is-armed'), 4000); return; }
		S.clearArm = 0; if (b) b.classList.remove('is-armed'); delMine(meId()); send({ t: 'mine' }); flash(T.cleared);
	}
	hClear.addEventListener('click', () => clearMine(hClear));
	async function toBlank() { if (S.objs.size && !(await confirmBox(T.blankQ, T.blankGo))) return; clearAll(); setBg(null); send({ t: 'bg', bg: null }); }
	function photoMenu() { menu(T.photoH, [{ i: 'camera', l: T.camera, f: () => camIn.click() }, { i: 'file', l: T.file, f: () => fileIn.click() }, S.bg && { i: 'grid', l: T.toBlank, f: toBlank }]); }
	pPhoto.addEventListener('click', photoMenu);
	hPhoto.addEventListener('click', () => (S.bg ? menu(T.photoH, [{ i: 'file', l: T.file, f: () => fileIn.click() }, { i: 'grid', l: T.toBlank, f: toBlank }]) : fileIn.click()));
	pNotes.addEventListener('click', notesSheet);
	function recal() { S.recal = true; pickTool('measure'); flash(T.recalGo, 4000); }
	pMore.addEventListener('click', () => {
		const b = pMore;
		menu(T.more, [{ i: 'save', l: T.save, f: saveImage }, mine().length && { i: 'trash', l: T.clear, danger: true, f: () => { S.clearArm = Date.now(); clearMine(b); } }, S.scale && { i: 'measure', l: T.recalA, f: recal }, S.bg && { i: 'grid', l: T.toBlank, f: toBlank }]);
	});
	zIn.addEventListener('click', () => zoomMid(1.25)); zOut.addEventListener('click', () => zoomMid(0.8)); zRecal.addEventListener('click', recal);
	deskIn.addEventListener('input', () => { if (deskIn.value.trim() && S.tool !== 'note') { pickTool('note'); flash(T.placeNow); } });
	deskIn.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); if (deskIn.value.trim()) { pickTool('note'); flash(T.placeNow); } } });
	async function takeImage(f) {
		if (!f || !/^image\//.test(f.type)) return;
		try {
			let bmp; try { bmp = await createImageBitmap(f, { imageOrientation: 'from-image' }); } catch (e) { bmp = await createImageBitmap(f); }
			const k = Math.min(1, 1600 / Math.max(bmp.width, bmp.height)), cv = document.createElement('canvas'); cv.width = Math.max(1, Math.round(bmp.width * k)); cv.height = Math.max(1, Math.round(bmp.height * k));
			const cx = cv.getContext('2d'); cx.fillStyle = '#FFFFFF'; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(bmp, 0, 0, cv.width, cv.height);
			let src = ''; for (const q of [0.82, 0.68, 0.55]) { src = cv.toDataURL('image/jpeg', q); if (src.length <= 1100000) break; }
			if (src.length > MAXIMG) { flash(T.big); return; }
			if (S.objs.size && !(await confirmBox(T.replaceQ, T.replace))) return;
			const bg = cleanBg({ src, w: cv.width, h: cv.height, n: who(meId()).name }); if (!bg) { flash(T.big); return; }
			clearAll(); setBg(bg); send({ t: 'bg', bg }); flash(T.sent);
		} catch (e) { flash(T.big); }
	}
	for (const inp of [camIn, fileIn]) inp.addEventListener('change', () => { const f = inp.files && inp.files[0]; inp.value = ''; takeImage(f); });

	/* ---------------- save as a picture: the sheet with the marks, the numbered notes under it ---------------- */
	async function saveImage() {
		try {
			let a; if (S.bg) a = { x: 0, y: 0, w: S.W, h: S.H };
			else { let b = null; try { b = gObj.getBBox(); const p = gPin.getBBox(); if (p.width || p.height) b = b.width || b.height ? { x: Math.min(b.x, p.x), y: Math.min(b.y, p.y), width: Math.max(b.x + b.width, p.x + p.width) - Math.min(b.x, p.x), height: Math.max(b.y + b.height, p.y + p.height) - Math.min(b.y, p.y) } : p; } catch (e) { b = null; }
				const x0 = Math.min(0, b && b.width ? b.x - 40 : 0), y0 = Math.min(0, b && b.width ? b.y - 40 : 0); a = { x: x0, y: y0, w: Math.max(S.W, b && b.width ? b.x + b.width + 40 : 0) - x0, h: Math.max(S.H, b && b.width ? b.y + b.height + 40 : 0) - y0 }; }
			const k = 1600 / Math.max(a.w, a.h), cw = Math.round(a.w * k), ch = Math.round(a.h * k);
			const out = svg.cloneNode(true); out.querySelectorAll('.nlfsb-live').forEach((n) => n.remove());
			out.setAttribute('viewBox', [a.x, a.y, a.w, a.h].join(' ')); out.setAttribute('width', cw); out.setAttribute('height', ch); out.setAttribute('xmlns', NS);
			const op = out.querySelector('pattern'); if (op) { const gs = n1(18 / k * Math.pow(2, Math.round(Math.log2(k)))); op.setAttribute('width', gs); op.setAttribute('height', gs); op.firstChild.setAttribute('d', 'M' + gs + ' 0H0V' + gs); op.firstChild.setAttribute('stroke-width', n3(1 / k)); }
			const url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(out)], { type: 'image/svg+xml' }));
			const img = new Image(); img.src = url; await img.decode();
			const ns = notes(), W = Math.max(cw, 1000), pad = 40, tw = W - pad * 2 - 56, probe = document.createElement('canvas').getContext('2d');
			probe.font = '600 26px Assistant, Arial, sans-serif';
			const wrapT = (s) => { const out2 = []; let line = ''; for (const w of s.split(/\s+/)) { const t = line ? line + ' ' + w : w; if (probe.measureText(t).width > tw && line) { out2.push(line); line = w; } else line = t; } if (line) out2.push(line); return out2; };
			const rows = ns.map((o) => ({ o, lines: wrapT(o.t) })), nh = ns.length ? 130 + rows.reduce((s, r) => s + 44 + r.lines.length * 34, 0) : 70;
			const cv = document.createElement('canvas'); cv.width = W; cv.height = ch + nh; const c = cv.getContext('2d');
			c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, cv.height); c.drawImage(img, Math.round((W - cw) / 2), 0); URL.revokeObjectURL(url);
			c.fillStyle = '#101820'; c.fillRect(0, ch, W, 3); c.direction = 'rtl'; c.textAlign = 'right'; c.textBaseline = 'alphabetic';
			let y = ch + 56; c.font = '700 30px Rubik, Arial, sans-serif'; c.fillText(ns.length ? T.notesH + ' · ' + T.count(ns.length, ns.filter((o) => o.d).length) : T.board + ' · ' + (title || ''), W - pad, y);
			c.textAlign = 'left'; c.font = '500 20px Rubik, Arial, sans-serif'; c.fillStyle = '#3A4650'; c.fillText(new Date().toLocaleDateString('he-IL'), pad, y); c.textAlign = 'right';
			y += 30;
			for (const r of rows) {
				y += 14; const col = r.o.c; c.fillStyle = col; c.beginPath(); c.arc(W - pad - 16, y + 14, 16, 0, Math.PI * 2); c.fill();
				c.fillStyle = ink(col); c.textAlign = 'center'; c.font = '700 18px Rubik, Arial, sans-serif'; c.fillText(String(S.nums.get(r.o.id)), W - pad - 16, y + 20); c.textAlign = 'right';
				c.fillStyle = DARK[col]; c.font = '700 20px Assistant, Arial, sans-serif'; c.fillText([r.o.n, r.o.l].filter(Boolean).join(' · ') + (r.o.d ? ' · ' + T.doneTag : ''), W - pad - 48, y + 20);
				c.fillStyle = r.o.d ? '#5B6770' : '#101820'; c.font = '600 26px Assistant, Arial, sans-serif';
				r.lines.forEach((l, i) => { const ly = y + 54 + i * 34; c.fillText(l, W - pad - 48, ly); if (r.o.d) { const lw = c.measureText(l).width; c.fillRect(W - pad - 48 - lw, ly - 9, lw, 2); } });
				y += 30 + r.lines.length * 34;
			}
			const href = cv.toDataURL('image/png'), dl = document.createElement('a'); dl.href = href; dl.download = 'לוח-נדלן-' + new Date().toISOString().slice(0, 10) + '.png';
			document.body.appendChild(dl); dl.click(); dl.remove(); flash(T.saved); return href;
		} catch (e) { flash(T.saveFail); return ''; }
	}
	hSave.addEventListener('click', saveImage);

	/* ---------------- the notice to the others ---------------- */
	let nudgeTm = 0;
	function showNudge(from) { nudgeT.textContent = T.open(first(who(from).name)); nudgeDot.style.background = colorOf(from); nudge.hidden = false; clearTimeout(nudgeTm); nudgeTm = setTimeout(() => { nudge.hidden = true; }, 15000); }
	nudgeGo.addEventListener('click', () => { nudge.hidden = true; open(true); });
	nudgeX.addEventListener('click', () => { nudge.hidden = true; });

	/* ---------------- open / close / layout ---------------- */
	function layout() {
		S.desk = !!mq.matches; root.classList.toggle('is-desk', S.desk);
		subT.textContent = S.desk ? T.subD : T.sub;
		if (S.desk) { deskTiles.appendChild(tilesBox); aside.appendChild(ctl); } else { row.insertBefore(tilesBox, followB); ctlHome.appendChild(ctl); }
		pickTool(S.tool); paintBlock();
	}
	const onMq = () => { if (!S.shown) return; layout(); paintTiles(); requestAnimationFrame(reView); };
	if (mq.addEventListener) mq.addEventListener('change', onMq);
	const onKey = (ev) => {
		if (!S.shown) return;
		if (ev.key === 'Escape') { ev.stopPropagation(); ev.preventDefault(); if (!modal.hidden) closeModal(); else if (!callout.hidden) closeCallout(); else close(); return; }
		if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === 'z' && modal.hidden && document.activeElement !== deskIn) { ev.preventDefault(); undo(); }
	};
	document.addEventListener('keydown', onKey, true);
	const onResize = () => { if (S.shown) requestAnimationFrame(() => (S.follow && S.fv ? followTo(S.fv) : reView())); };
	window.addEventListener('resize', onResize);
	function open(quiet) {
		if (S.shown || !S.alive) return; S.shown = true; nudge.hidden = true; root.hidden = false;
		layout(); paintBg(); rescale(); paintObjs(); paintTiles(); paintCtl(); paintFollow();
		requestAnimationFrame(() => { if (S.follow && S.fv) followTo(S.fv); else if (S.view) reView(); else fit(); });
		if (!quiet) send({ t: 'open' });
		if (!S.hinted && !S.objs.size) { S.hinted = true; flash(T.hint, 5000); }
		setTimeout(() => backB.focus({ preventScroll: true }), 30);
	}
	function close() {
		if (!S.shown) return; closeModal(); closeCallout(); stopLead(); S.shown = false; root.hidden = true;
		for (const p of S.peers.values()) { p.g.remove(); p.trail.remove(); } S.peers.clear();
		if (typeof onClose === 'function') { try { onClose(); } catch (e) { /* the call screen is gone */ } }
	}
	backB.addEventListener('click', close);
	function destroy() {
		S.alive = false; clearInterval(tick); clearInterval(clock); clearTimeout(toastT); clearTimeout(nudgeTm); clearTimeout(lvQ);
		document.removeEventListener('keydown', onKey, true); window.removeEventListener('resize', onResize); if (mq.removeEventListener) mq.removeEventListener('change', onMq);
		root.remove(); nudge.remove(); style.remove();
	}
	paintBg(); paintBlock(); paintFollow();
	return { open, close, destroy, saveImage, get shown() { return S.shown; }, get size() { return S.objs.size; } };
}
