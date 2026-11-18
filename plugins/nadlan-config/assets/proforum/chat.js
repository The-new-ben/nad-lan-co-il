// nad-lan professionals' forum: the chat inside a video room (inc/pro-forum-chat.php, Claude Design board 22, 18.11.2026).
//
// Imported by assets/proforum/call.js on the call screen (same version query, like board.js): createChat(o) with
//   { tr, tk, req, nonce, rest, root, button, sheet, host }
//   tr      the LiveKit transport of assets/designer/call.js (publishData / onData / participants / onParticipants)
//   tk      the call/token answer (room, title, topic)            req     call.js's request helper (header nonce, one quiet retry)
//   root    the call screen                                       button  the "צ'אט" control of the bar (the unread count goes on it)
//   sheet   call.js's bottom sheet (the end-of-call sheet uses it) host    I opened this room
// What it does (board 22): a new message while the chat is closed shows for 4 seconds over the video and counts on the button;
// the chat opens on half the screen of a phone (the video keeps playing above it) and as a side panel from 900px; history from the
// server ("הודעות מלפני שנכנסת"), the pinned message, pictures and plans through the media module (POST media), the two word
// reactions, report and delete; the host's end-of-call sheet puts "מה סוכם בשיחה" into the discussion.
// Live delivery: the server saves a message first, then the saved row goes on the LiveKit data topic 'chat'. A row is shown only
// when its author's LiveKit identity is the one that sent it; pins, deletes and reactions send {t:'sync'} and every page asks the
// server again. No HTML string anywhere: every node is built and every text goes in through textContent; no library.

const T = {
	lChat: "צ'אט", btnAria: (n) => (n ? "צ'אט החדר, " + n + ' הודעות חדשות' : "צ'אט החדר"),
	head: "צ'אט החדר", inRoom: (n) => n + ' בחדר', close: 'סגירה', pinned: 'נעוץ:', before: 'הודעות מלפני שנכנסת',
	ph: 'כתבו לחדר...', inAria: 'הודעה לחדר', send: 'שליחה', add: 'צירוף תמונה או תוכנית',
	useful: 'מועיל', thanks: 'תודה', you: 'אתם', empty: 'עוד אין הודעות בחדר.',
	more: 'פעולות על ההודעה', pin: 'נעיצה', unpin: 'ביטול הנעיצה', del: 'מחיקה', delSure: 'כן, למחוק', report: 'דיווח', reportH: 'למה לדווח?',
	deleted: 'ההודעה נמחקה.', img: 'תמונה', pdf: 'תוכנית PDF', imgOf: (n) => 'תמונה ששלח/ה ' + n, openImg: 'פתיחת התמונה במסך מלא',
	up: 'מעלים את הקובץ…', upFail: 'הקובץ לא עלה. נסו שוב.', wait: 'רגע, הקובץ עוד עולה.', kind: 'אפשר לצרף תמונה או קובץ PDF.',
	big: 'הקובץ גדול מ-25MB.', bad: 'לא הצלחנו לפתוח את התמונה. נסו JPG או PNG.', drop: 'הסרת הקובץ',
	stars: (n) => n + ' כוכבים',
	// part ג, word for word
	endH: (n) => 'השיחה הסתיימה · ' + (n === 1 ? 'דקה אחת' : n + ' דקות'), endQ: (t) => 'מה לצרף לדיון "' + t + '"?',
	endRest: (n) => 'כל שאר ההודעות (' + n + ')', endGo: 'לצרף לדיון כ"מה סוכם בשיחה"',
	endFine: "רק מי שפתח את החדר מצרף. בלי הצירוף, הצ'אט נשאר בחדר בלבד ונמחק אחרי 7 ימים.",
	endSkip: 'לא עכשיו', endBusy: 'מצרפים לדיון…', endNone: 'סמנו מה לצרף.',
};
const REASONS = [['spam', 'פרסום או ספאם'], ['abuse', 'פגיעה או העלבה'], ['private', 'פרטים אישיים של מישהו'], ['wrong', 'מידע מטעה'], ['other', 'סיבה אחרת']]; // the forum's nlf_report_reasons()
const ERR = 'משהו השתבש. נסו שוב.';
const MAX_BODY = 1000, LONG = 2560, PDF_MAX = 25 * 1048576;

/* ---------------------------------------------------------------- small DOM helpers (text only through textContent) */

function h(tag, props, ...kids) {
	const e = document.createElement(tag);
	for (const [k, v] of Object.entries(props || {})) {
		if (v == null || v === false) continue;
		if (k === 'text') e.textContent = String(v);
		else if (k === 'cls') e.className = v;
		else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
		else e.setAttribute(k, v === true ? '' : String(v));
	}
	for (const c of kids) if (c) e.appendChild(c);
	return e;
}
// the two icons are built node by node from constants of this file
function ico(kind) {
	const NS = 'http://www.w3.org/2000/svg', s = document.createElementNS(NS, 'svg');
	s.setAttribute('aria-hidden', 'true'); s.setAttribute('focusable', 'false'); s.setAttribute('width', '20'); s.setAttribute('height', '20'); s.setAttribute('viewBox', '0 0 24 24');
	s.setAttribute('fill', 'none'); s.setAttribute('stroke', 'currentColor'); s.setAttribute('stroke-width', '2.2'); s.setAttribute('stroke-linecap', 'round');
	if (kind === 'more') {
		for (const cx of [5, 12, 19]) { const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', cx); c.setAttribute('cy', 12); c.setAttribute('r', 1.6); c.setAttribute('fill', 'currentColor'); s.appendChild(c); }
	} else {
		const p = document.createElementNS(NS, 'path'); p.setAttribute('d', 'M6 6l12 12M18 6L6 18'); s.appendChild(p);
	}
	return s;
}
function avatar(who) {
	const w = who || {};
	if (w.pic) return h('span', { cls: 'nlfch-av is-pic', 'aria-hidden': 'true' }, h('img', { src: w.pic, alt: '', width: 30, height: 30, loading: 'lazy', decoding: 'async' }));
	const a = h('span', { cls: 'nlfch-av', 'aria-hidden': 'true', text: w.initials || '?' });
	if (w.bg) a.style.background = w.bg;
	if (w.fg) a.style.color = w.fg;
	return a;
}

/* ---------------------------------------------------------------- a picture is drawn again in the browser before it goes (no location, no camera data) */

function decode(f) {
	const viaImg = () => new Promise((res, rej) => { const u = URL.createObjectURL(f), im = new Image(); im.onload = () => { URL.revokeObjectURL(u); res(im); }; im.onerror = () => { URL.revokeObjectURL(u); rej(new Error(T.bad)); }; im.src = u; });
	if (!window.createImageBitmap) return viaImg();
	return createImageBitmap(f, { imageOrientation: 'from-image' }).catch(() => createImageBitmap(f)).catch(viaImg);
}
async function shrink(f) {
	const src = await decode(f);
	const w = src.width || src.naturalWidth, hh = src.height || src.naturalHeight;
	if (!w || !hh) throw new Error(T.bad);
	const k = Math.min(1, LONG / Math.max(w, hh)), cv = document.createElement('canvas');
	cv.width = Math.max(1, Math.round(w * k)); cv.height = Math.max(1, Math.round(hh * k));
	const cx = cv.getContext('2d');
	cx.fillStyle = '#FFFFFF'; cx.fillRect(0, 0, cv.width, cv.height);
	cx.drawImage(src, 0, 0, cv.width, cv.height);
	if (src.close) src.close();
	const b = await new Promise((res) => cv.toBlob(res, 'image/jpeg', 0.85));
	if (!b) throw new Error(T.bad);
	return b;
}

/* ---------------------------------------------------------------- the chat of one call screen */

export function createChat(o) {
	const room = o.tk.room;
	const S = { rows: [], open: false, unread: 0, before: 0, loaded: false, alive: true, acts: 0, report: 0, sure: 0, file: null, sending: false, toastT: 0, syncT: 0, me: 0, host: !!o.host, ending: false };
	const els = new Map(); // message id -> { el, sig }

	// the badge on the bar's "צ'אט" control (raspberry, board 22 part א)
	const badge = h('b', { cls: 'nlfch-badge', 'aria-hidden': 'true', hidden: true });
	o.button.classList.add('nlfch-btn');
	o.button.appendChild(badge);
	o.button.setAttribute('aria-expanded', 'false');

	// the message that shows for 4 seconds over the video
	const toastW = h('div', { cls: 'nlfch-toastw', role: 'status', 'aria-live': 'polite' });

	// the chat (part ב)
	const hid = 'nlfch-h-' + Math.random().toString(36).slice(2, 8);
	const countEl = h('span', { cls: 'nlfch-count' });
	const x = h('button', { type: 'button', cls: 'nlfch-x', 'aria-label': T.close, title: T.close }, ico('x'));
	const pinText = h('span', { cls: 'nlfch-pintext' });
	const pinBar = h('div', { cls: 'nlfch-pin', hidden: true }, h('b', { text: T.pinned }), pinText);
	const list = h('div', { cls: 'nlfch-list', role: 'log', 'aria-live': 'polite', 'aria-labelledby': hid, tabindex: '0' });
	const emptyP = h('p', { cls: 'nlfch-empty', text: T.empty, hidden: true });
	const status = h('p', { cls: 'nlfch-status', role: 'status', 'aria-live': 'polite' });
	const att = h('div', { cls: 'nlfch-att', hidden: true });
	const fileIn = h('input', { type: 'file', accept: 'image/*,application/pdf,.pdf', hidden: true, tabindex: '-1', 'aria-hidden': 'true' });
	const addB = h('button', { type: 'button', cls: 'nlfch-add', 'aria-label': T.add, title: T.add }, h('span', { 'aria-hidden': 'true', text: '+' }));
	const input = h('textarea', { cls: 'nlfch-in', rows: '1', maxlength: String(MAX_BODY), placeholder: T.ph, 'aria-label': T.inAria, enterkeyhint: 'send', dir: 'auto', autocomplete: 'off' });
	const sendB = h('button', { type: 'button', cls: 'nlfch-send', text: T.send });
	const panel = h('section', { cls: 'nlfch-panel', role: 'region', 'aria-labelledby': hid, hidden: true, dir: 'rtl', lang: 'he' },
		h('div', { cls: 'nlfch-head' }, h('h2', { id: hid, cls: 'nlfch-h', text: T.head }), countEl, x),
		pinBar, emptyP, list, att, status,
		h('div', { cls: 'nlfch-form' }, addB, input, sendB, fileIn));
	o.root.appendChild(panel);
	o.root.appendChild(toastW);

	let sayT = 0;
	const say = (t, bad) => { clearTimeout(sayT); status.textContent = t || ''; status.classList.toggle('is-bad', !!bad); if (t && !bad) sayT = setTimeout(() => { status.textContent = ''; }, 4000); };
	const pub = (obj) => { try { o.tr.publishData('chat', obj, { reliable: true }); } catch (e) { /* the server has it; the others see it on their next sync */ } };
	const people = () => { try { return o.tr.participants().length; } catch (e) { return 1; } };
	const paintCount = () => { countEl.textContent = T.inRoom(people()); };
	const paintBadge = () => {
		badge.textContent = S.unread > 99 ? '99+' : String(S.unread);
		badge.hidden = !S.unread;
		o.button.setAttribute('aria-label', T.btnAria(S.unread));
	};
	const nearEnd = () => list.scrollHeight - list.scrollTop - list.clientHeight < 80;
	const toEnd = () => { list.scrollTop = list.scrollHeight; };
	const label = (r) => r.body || (r.media ? (r.media.kind === 'pdf' ? T.pdf : T.img) : '');

	/* ---------------- one message */
	function mediaEl(r) {
		const m = r.media;
		if (m.kind === 'pdf') {
			return h('a', { cls: 'nlfch-pdf', href: m.url, target: '_blank', rel: 'noopener' }, h('span', { cls: 'nlfch-pdf-ic', 'aria-hidden': 'true', text: 'PDF' }), h('span', { text: m.meta || T.pdf }));
		}
		// the media module's full-screen view opens on a.nlfmd-tile inside [data-nlfmd-gal] (media.js); without it the picture opens in a new tab
		const w = m.w | 0 || 4, hh = m.h | 0 || 3;
		const a = h('a', { cls: 'nlfmd-tile nlfch-thumb', href: m.url, target: '_blank', rel: 'noopener', 'data-nlfmd-id': m.id, 'data-w': w, 'data-h': hh, 'data-cap': '', 'aria-label': T.openImg },
			h('img', { src: m.thumb || m.url, alt: T.imgOf(r.who.name), width: 150, height: Math.round(150 * hh / w), loading: 'lazy', decoding: 'async' }));
		return h('div', { cls: 'nlfch-media', 'data-nlfmd-gal': true, 'data-by': r.who.name, 'data-at': r.time }, a);
	}
	function reacts(r) {
		const kids = [];
		for (const k of ['useful', 'thanks']) {
			const n = (r.reacts && r.reacts[k]) | 0;
			if (r.mine) { if (n) kids.push(h('span', { cls: 'nlfch-pill', text: T[k] + ' ' + n })); continue; }
			const b = h('button', { type: 'button', cls: 'nlfch-rxb', 'aria-pressed': r.my === k ? 'true' : 'false' }, h('span', { cls: 'nlfch-pill' + (r.my === k ? ' is-on' : ''), text: n ? T[k] + ' ' + n : T[k] }));
			b.addEventListener('click', () => react(r, k));
			kids.push(b);
		}
		if (r.mine) kids.push(h('span', { cls: 'nlfch-mtime', text: r.time }));
		const more = h('button', { type: 'button', cls: 'nlfch-more', 'aria-label': T.more, title: T.more, 'aria-expanded': S.acts === r.id ? 'true' : 'false' }, ico('more'));
		more.addEventListener('click', () => { S.acts = S.acts === r.id ? 0 : r.id; S.report = 0; S.sure = 0; paint(); refocus(r.id, S.acts ? '.nlfch-acts button' : '.nlfch-more'); });
		kids.push(more);
		return h('div', { cls: 'nlfch-rx' }, ...kids);
	}
	function actions(r) {
		const btn = (text, fn, cls) => h('button', { type: 'button', cls: 'nlfch-act' + (cls ? ' ' + cls : ''), text, onclick: fn });
		if (S.report === r.id) {
			return h('div', { cls: 'nlfch-acts', role: 'group', 'aria-label': T.reportH }, h('b', { cls: 'nlfch-acth', text: T.reportH }), ...REASONS.map(([k, t]) => btn(t, () => report(r, k))));
		}
		const kids = [];
		if (S.host) kids.push(btn(r.pinned ? T.unpin : T.pin, () => pin(r)));
		if (r.del) kids.push(S.sure === r.id ? btn(T.delSure, () => del(r), 'is-bad') : btn(T.del, () => { S.sure = r.id; paint(); refocus(r.id, '.nlfch-act.is-bad'); }));
		if (!r.mine) kids.push(btn(T.report, () => { S.report = r.id; paint(); refocus(r.id, '.nlfch-acts button'); }));
		return h('div', { cls: 'nlfch-acts', role: 'group', 'aria-label': T.more }, ...kids);
	}
	function msgEl(r) {
		const text = r.body ? h('p', { cls: 'nlfch-text', dir: 'auto', text: r.body }) : null;
		const media = r.media ? mediaEl(r) : null;
		const acts = S.acts === r.id ? actions(r) : null;
		if (r.mine) {
			return h('div', { cls: 'nlfch-m is-mine', 'data-id': r.id },
				h('div', { cls: 'nlfch-bub' }, h('span', { cls: 'nlfch-sr', text: T.you + ': ' }), text, media), reacts(r), acts);
		}
		const w = r.who || {};
		const meta = h('span', { cls: 'nlfch-meta' }, h('b', { text: w.name || '' }));
		if (w.label) meta.appendChild(document.createTextNode(' · ' + w.label));
		if (w.stars) { meta.appendChild(document.createTextNode(' · ')); meta.appendChild(h('span', { cls: 'nlfch-stars', role: 'img', 'aria-label': T.stars(w.stars.length), text: w.stars })); }
		if (r.time) meta.appendChild(document.createTextNode(' · ' + r.time));
		return h('div', { cls: 'nlfch-m', 'data-id': r.id }, avatar(w), h('div', { cls: 'nlfch-mb' }, meta, text, media, reacts(r), acts));
	}
	function refocus(id, sel) {
		const e = list.querySelector('[data-id="' + (id | 0) + '"] ' + sel) || list.querySelector('[data-id="' + (id | 0) + '"] .nlfch-more');
		if (e) e.focus({ preventScroll: true }); else input.focus({ preventScroll: true });
	}

	/* ---------------- the list: keyed, so a reaction redraws one message and a new one is added at its place (the log stays calm) */
	let divider = null;
	function paint() {
		const stick = nearEnd();
		const ids = new Set(S.rows.map((r) => r.id));
		for (const [id, v] of els) if (!ids.has(id)) { v.el.remove(); els.delete(id); }
		let cur = null;
		for (const r of S.rows) {
			const sig = JSON.stringify([r.body, r.pinned, r.reacts, r.my, r.del, r.mine, r.media && r.media.id, r.who && r.who.pic, S.acts === r.id, S.report === r.id, S.sure === r.id, S.host]);
			let v = els.get(r.id);
			if (!v) {
				v = { el: msgEl(r), sig };
				els.set(r.id, v);
				if (cur) cur.after(v.el); else if (divider && divider.parentNode === list) divider.after(v.el); else list.prepend(v.el);
			} else if (v.sig !== sig) { const n = msgEl(r); v.el.replaceWith(n); v.el = n; v.sig = sig; }
			cur = v.el;
		}
		// "הודעות מלפני שנכנסת" heads what was there before I came in
		const first = S.rows.find((r) => S.before && r.id <= S.before);
		if (first && !divider) { divider = h('span', { cls: 'nlfch-div', text: T.before }); els.get(first.id).el.before(divider); }
		if (divider && !first) { divider.remove(); divider = null; }
		emptyP.hidden = S.rows.length > 0;
		const p = S.rows.find((r) => r.pinned);
		pinBar.hidden = !p; pinText.textContent = p ? label(p) : '';
		if (stick) toEnd();
	}

	/* ---------------- the server */
	async function load(quiet) {
		try {
			const j = await o.req('GET', 'chat', { room });
			if (!S.alive) return;
			S.me = j.me | 0; S.host = !!j.host;
			const rows = Array.isArray(j.rows) ? j.rows : [];
			if (!S.loaded) { S.loaded = true; S.before = rows.length ? rows[rows.length - 1].id : 0; }
			S.rows = rows;
			paint();
		} catch (e) { if (!quiet) say(e.message || ERR, true); }
	}
	const sync = () => { clearTimeout(S.syncT); S.syncT = setTimeout(() => load(true), 300); };

	function addRow(row, remote) {
		if (!row || !row.id || S.rows.some((r) => r.id === row.id)) return;
		if (remote) { // the sender's server answer is about the sender: mine, delete and my reaction are mine to work out
			row.mine = row.who && (row.who.id | 0) === S.me ? 1 : 0;
			row.del = row.mine || S.host ? 1 : 0;
			row.my = '';
		}
		S.rows.push(row);
		S.rows.sort((a, b) => a.id - b.id);
		paint();
		if (remote && !S.open) { S.unread++; paintBadge(); toast(row); }
	}

	function toast(r) {
		clearTimeout(S.toastT);
		const b = h('button', { type: 'button', cls: 'nlfch-toast' }, avatar(r.who), h('span', { cls: 'nlfch-tt' }, h('b', { text: (r.who && r.who.name) || '' }), document.createTextNode(' ' + label(r))));
		b.addEventListener('click', () => { toastW.replaceChildren(); open(); });
		toastW.replaceChildren(b);
		S.toastT = setTimeout(() => { if (toastW.contains(b)) toastW.replaceChildren(); }, 4000);
	}

	async function send() {
		if (S.sending) return;
		const body = input.value;
		if (!body.trim() && !S.file) { input.focus(); return; }
		if (S.file && S.file.state !== 'done') { say(S.file.state === 'err' ? T.upFail : T.wait, S.file.state === 'err'); return; }
		S.sending = true; sendB.disabled = true;
		try {
			const j = await o.req('POST', 'chat/send', { room, body, media: S.file ? S.file.id : 0 });
			input.value = ''; grow(); S.file = null; paintAtt(); say('');
			addRow(j.row, false);
			pub({ t: 'msg', row: j.row });
			toEnd();
		} catch (e) { say(e.message || ERR, true); }
		S.sending = false; sendB.disabled = false;
		if (S.open) input.focus({ preventScroll: true });
	}
	async function react(r, k) {
		try {
			const j = await o.req('POST', 'chat/react', { room, id: r.id, kind: k });
			const x2 = S.rows.find((y) => y.id === r.id);
			if (x2) { x2.reacts = j.reacts; x2.my = j.mine || ''; }
			paint(); refocus(r.id, '.nlfch-rxb[aria-pressed="true"]');
			pub({ t: 'sync' });
		} catch (e) { say(e.message || ERR, true); }
	}
	async function pin(r) {
		try {
			const j = await o.req('POST', 'chat/pin', { room, id: r.id, on: r.pinned ? 0 : 1 });
			S.rows.forEach((y) => { y.pinned = y.id === (j.pinned | 0) ? 1 : 0; });
			S.acts = 0; paint(); refocus(r.id, '.nlfch-more');
			pub({ t: 'sync' });
		} catch (e) { say(e.message || ERR, true); }
	}
	async function del(r) {
		try {
			await o.req('POST', 'chat/delete', { room, id: r.id });
			S.rows = S.rows.filter((y) => y.id !== r.id); S.acts = 0; S.sure = 0;
			paint(); input.focus({ preventScroll: true }); say(T.deleted);
			pub({ t: 'sync' });
		} catch (e) { say(e.message || ERR, true); }
	}
	async function report(r, k) {
		try {
			const j = await o.req('POST', 'chat/report', { room, id: r.id, reason: k });
			S.acts = 0; S.report = 0;
			if (j.gone) { S.rows = S.rows.filter((y) => y.id !== r.id); pub({ t: 'sync' }); }
			paint(); refocus(r.id, '.nlfch-more'); say(j.message || '');
		} catch (e) { say(e.message || ERR, true); }
	}

	/* ---------------- "+": a picture or a plan through the media module (POST media), then the message carries its id */
	function paintAtt() {
		const f = S.file;
		att.hidden = !f;
		if (!f) { att.replaceChildren(); return; }
		const face = f.kind === 'pdf' || !f.thumb ? h('span', { cls: 'nlfch-att-ic', 'aria-hidden': 'true', text: f.kind === 'pdf' ? 'PDF' : '' }) : h('img', { src: f.thumb, alt: '', width: 44, height: 44 });
		const rm = h('button', { type: 'button', cls: 'nlfch-x nlfch-attx', 'aria-label': T.drop, title: T.drop }, ico('x'));
		rm.addEventListener('click', () => { S.file = null; paintAtt(); say(''); input.focus({ preventScroll: true }); });
		att.replaceChildren(face, h('span', { cls: 'nlfch-att-t', text: f.state === 'up' ? T.up : (f.state === 'err' ? T.upFail : f.name) }), rm);
	}
	async function pick(f) {
		const isPdf = f.type === 'application/pdf' || /\.pdf$/i.test(f.name || '');
		const isImg = /^image\//.test(f.type || '') || /\.(heic|heif|jpe?g|png|webp)$/i.test(f.name || '');
		if (!isPdf && !isImg) { say(T.kind, true); return; }
		if (isPdf && f.size > PDF_MAX) { say(T.big, true); return; }
		const it = { state: 'up', id: 0, kind: isPdf ? 'pdf' : 'image', name: f.name || (isPdf ? T.pdf : T.img), thumb: '' };
		S.file = it; paintAtt(); say(T.up);
		try {
			const blob = isPdf ? f : await shrink(f);
			const fd = new FormData();
			fd.append('file', blob, isPdf ? 'plan.pdf' : 'photo.jpg');
			const r = await fetch(o.rest + 'media', { method: 'POST', credentials: 'same-origin', headers: { Accept: 'application/json', 'X-NLF-Nonce': o.nonce() }, body: fd });
			let j = null; try { j = await r.json(); } catch (e) { j = null; }
			if (!r.ok || !j || j.ok !== 1 || !j.media) throw new Error((j && j.message) || T.upFail);
			if (S.file !== it) return;
			it.state = 'done'; it.id = j.media.id | 0; it.thumb = j.media.thumb || '';
			paintAtt(); say('');
			input.focus({ preventScroll: true });
		} catch (e) { if (S.file === it) { it.state = 'err'; paintAtt(); } say(e.message || T.upFail, true); }
	}
	addB.addEventListener('click', () => fileIn.click());
	fileIn.addEventListener('change', () => { const f = fileIn.files && fileIn.files[0]; fileIn.value = ''; if (f) pick(f); });

	/* ---------------- typing: Enter sends, Shift+Enter is a new line, the box grows to four lines */
	function grow() { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 120) + 'px'; }
	input.addEventListener('input', grow);
	input.addEventListener('keydown', (ev) => {
		if (ev.key === 'Enter' && !ev.shiftKey && !ev.isComposing && ev.keyCode !== 229) { ev.preventDefault(); send(); }
	});
	sendB.addEventListener('click', send);

	/* ---------------- open and close (Esc closes; the focus goes to the box when it opens and back to the button when it closes) */
	function open() {
		if (!S.alive) return;
		S.open = true; panel.hidden = false;
		o.root.classList.add('nlfch-on');
		o.button.setAttribute('aria-expanded', 'true'); o.button.setAttribute('aria-pressed', 'true');
		S.unread = 0; paintBadge(); paintCount();
		toastW.replaceChildren();
		if (!S.loaded) load(); else paint();
		toEnd();
		setTimeout(() => { if (S.open) input.focus({ preventScroll: true }); }, 30);
	}
	function close(back = true) {
		if (!S.open) return;
		S.open = false; panel.hidden = true; S.acts = 0; S.report = 0; S.sure = 0;
		o.root.classList.remove('nlfch-on');
		o.button.setAttribute('aria-expanded', 'false'); o.button.setAttribute('aria-pressed', 'false');
		paint();
		if (back) o.button.focus({ preventScroll: true });
	}
	x.addEventListener('click', () => close());
	panel.addEventListener('keydown', (ev) => {
		if (ev.key !== 'Escape') return;
		ev.preventDefault(); ev.stopPropagation();
		if (S.acts) { const id = S.acts; S.acts = 0; S.report = 0; S.sure = 0; paint(); refocus(id, '.nlfch-more'); return; }
		close();
	});

	/* ---------------- the network: a saved row from its own author, or "ask the server again" */
	o.tr.onData((topic, m, from) => {
		if (topic !== 'chat' || !S.alive || !m) return;
		if (m.t === 'msg' && m.row && m.row.who && m.row.who.identity && m.row.who.identity === from) { addRow(m.row, true); return; }
		if (m.t === 'msg' || m.t === 'sync') sync();
	});
	if (typeof o.tr.onParticipants === 'function') o.tr.onParticipants(() => { if (S.alive) paintCount(); });

	/* ---------------- part ג: the host's end-of-call sheet. Resolves with the attach answer, or null */
	function endSheet(minutes) {
		if (!S.host || S.ending || typeof o.sheet !== 'function') return Promise.resolve(null);
		S.ending = true;
		return o.req('GET', 'chat/summary', { room }).then((s) => new Promise((resolve) => {
			const media = s && s.media && (s.media.n | 0) > 0;
			if (!s || !s.can || (!s.pinned && !media && !(s.rest | 0))) { S.ending = false; resolve(null); return; }
			const opts = [];
			const row = (key, text, on, muted) => {
				const inp = h('input', { type: 'checkbox', cls: 'nlfch-cb' });
				inp.checked = on;
				opts.push([key, inp]);
				return h('label', { cls: 'nlfch-endrow' + (muted ? ' is-muted' : '') }, inp, h('span', { text }));
			};
			const box = h('div', { cls: 'nlfch-end' },
				s.pinned ? row('pin', s.pinned.text, true) : null,
				media ? row('media', s.media.label, true) : null,
				(s.rest | 0) ? row('rest', T.endRest(s.rest | 0), false, true) : null);
			let done = false, got = null;
			const fin = () => { if (done) return; done = true; S.ending = false; resolve(got); };
			o.sheet({
				heading: T.endH(Math.max(1, minutes | 0)), sub: T.endQ(s.title || ''), go: T.endGo, media: false, no: T.endSkip, extra: box, room: true, cls: 'nlfch-endsheet', fine: T.endFine,
				onClose: fin,
				onGo: async (api) => {
					api.say(T.endBusy);
					const want = {}; opts.forEach(([k, i]) => { want[k] = i.checked ? 1 : 0; });
					if (!want.pin && !want.media && !want.rest) { api.error(T.endNone); return; }
					got = await o.req('POST', 'chat/attach', { room, pin: want.pin | 0, media: want.media | 0, rest: want.rest | 0 });
					api.close();
					fin();
				},
			});
		})).catch(() => { S.ending = false; return null; });
	}

	function destroy() {
		S.alive = false;
		clearTimeout(S.toastT); clearTimeout(S.syncT); clearTimeout(sayT);
		panel.remove(); toastW.remove(); badge.remove();
		o.root.classList.remove('nlfch-on');
	}

	paintBadge(); paintCount();
	load(true); // the history is there before the first press, so a message that comes in now counts as new
	return { open, close, toggle: () => (S.open ? close() : open()), endSheet, destroy, get shown() { return S.open; } };
}
