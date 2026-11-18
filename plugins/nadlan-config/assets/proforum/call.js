// nad-lan professionals' forum: one-tap video calls inside a discussion (inc/pro-forum-call.php, 12.11.2026).
//
// Loaded as a module on forum surfaces only, after window.NLFCALL (printed by pro-forum-call.php):
//   { rest, lib, member, topic, title, targets: [{ with, reply, name, label }], photo }
// What it does:
//   - puts a "שיחת וידאו" pill on the reply cards (and the discussion's own card) of the people the member may call, unless the
//     forum already printed buttons with data-nlf-call="<topic id>" data-nlf-with="<member id>" (those are used as they are);
//   - a press opens a bottom sheet (camera and microphone OFF, a preview and a level line only when switched on), then the call
//     full screen: the request pinned at the top, the other person's name and trade, self view, mic / camera / flip / more / end;
//   - "#call=<room>" on the discussion address (the mail link) and the in-forum notice (polled) join a room the member was invited to;
//   - the member's own switches (calls allowed, invitation mail) in any [data-nlf-callpref] box, or behind a "שיחות וידאו" link
//     added to the forum's member bar.
// The network goes only through livekitTransport() of assets/designer/call.js (the site's LiveKit stack, CALL-CONTRACT.md),
// imported on the first press. joinCall() is not used: it needs a mounted designer (store, 3D space, view), see CALL-NOTES.md.
// No library beyond that, and no HTML string holds text that comes from people (names and titles go in through textContent).

const C = typeof window !== 'undefined' ? window.NLFCALL : null;

const T = {
	btn: 'שיחת וידאו', btnWith: (n) => 'שיחת וידאו עם ' + n,
	startH: (n) => 'שיחת וידאו עם ' + n, joinH: 'שיחת וידאו על הבקשה', joinSub: (n) => n + ' מזמין אתכם לשיחה. נכנסים עם מצלמה ומיקרופון כבויים.',
	startGo: 'התחלת שיחה', joinGo: 'כניסה לשיחה', notNow: 'לא עכשיו', close: 'סגירה',
	cam: 'מצלמה', camSub: 'אפשר לכבות בכל רגע', mic: 'מיקרופון', micSub: 'אפשר להשתיק בכל רגע', you: 'אתם',
	meter: 'דברו, והקו זז. כך יודעים שישמעו אתכם.',
	note: 'השיחה לא מוקלטת. הדפדפן יבקש רשות למצלמה ולמיקרופון רק כשתפעילו אותם.',
	blocked: 'הדפדפן לא נתן גישה. אפשר להיכנס בלי, ולאשר אחר כך בהגדרות הדפדפן.',
	wait: 'מתחברים לשיחה…', fail: 'לא הצלחנו להתחבר לשיחה. נסו שוב בעוד רגע.',
	needH: 'כדי להצטרף לשיחה צריך להיכנס לפורום', needSub: 'זה צעד אחד: שם, מייל וקוד. אחר כך השיחה נפתחת כאן.', enter: 'כניסה',
	gone: 'השיחה הזו כבר הסתיימה.',
	tag: 'הבקשה', waitFor: (n) => 'מחכים ש' + n + ' יצטרף…', noCam: (n) => 'המצלמה של ' + n + ' כבויה',
	left: (n) => n + ' יצא/ה מהשיחה.', joined: (n) => n + ' הצטרף/ה לשיחה.',
	micOn: 'להפעיל את המיקרופון', micOff: 'להשתיק את המיקרופון', camOn: 'להפעיל את המצלמה', camOff: 'לכבות את המצלמה',
	flip: 'החלפת מצלמה', more: 'עוד אפשרויות', end: 'סיום שיחה',
	lMic: 'מיקרופון', lCam: 'מצלמה', lFlip: 'החלפה', lMore: 'עוד', lEnd: 'סיום',
	photo: 'צלמו תמונה לבקשה', invite: 'הזמינו עוד מישהו', inviteH: 'להזמין לשיחה', inviteSub: 'אפשר להזמין מי שענה בדיון ופתח שיחות וידאו.',
	invited: (n) => 'הזמנה נשלחה ל' + n + '.', noOne: 'אין כרגע עוד משתתפים שאפשר להזמין.',
	voice: 'קול בלבד, חוסך נתונים', voiceOn: 'הווידאו של האחרים מושהה. השמע ממשיך.', voiceOff: 'הווידאו חזר.',
	norec: 'השיחה לא מוקלטת.', audio: 'הקישו כדי לשמוע',
	reconnecting: 'החיבור נקטע, מתחברים שוב…', lost: 'השיחה נותקה.',
	denied: 'אין גישה למצלמה או למיקרופון. אפשר לאשר בהגדרות הדפדפן.',
	inviteToast: (n, t) => n + ' מזמין אתכם לשיחת וידאו על ' + t,
	prefH: 'שיחות וידאו', prefVideo: 'אפשר לפנות אליי בשיחת וידאו', prefVideoSub: 'חברי הפורום יוכלו להתקשר אליכם מהכרטיס שלכם ומדיון שכתבתם בו.',
	tagCard: 'כרטיס',
	prefMail: 'לשלוח לי מייל כשמזמינים אותי לשיחה', prefMailSub: 'מייל אחד לכל הזמנה. אפשר לכבות בכל רגע.',
	callAria: 'שיחת וידאו',
	// board 19: the open video room
	roomH: 'חדר וידאו', roomGo: 'פתיחת החדר', tagTopic: 'הדיון', roomTag: 'חדר וידאו',
	roomNeedH: 'כדי לפתוח חדר וידאו צריך להיכנס לפורום', roomNeedSub: 'זה צעד אחד: שם, מייל וקוד. אחר כך החדר נפתח כאן.',
	joinRoomNeedH: 'כדי להצטרף לחדר צריך להיכנס לפורום', joinRoomNeedSub: 'זה צעד אחד: שם, מייל וקוד. אחר כך החדר נפתח כאן.',
	joinRoomH: (n) => (n || 'חבר הפורום') + ' מזמין אתכם לחדר וידאו', inRoom: (k) => k + ' כבר בחדר', joinRoomGo: 'כניסה לחדר',
	joinRoomNote: 'נכנסים עם מצלמה ומיקרופון כבויים, ומדליקים כשרוצים.',
	roomWait: 'החדר פתוח. שלחו את הקישור למי שרוצים שיצטרף.',
	whoH: 'מי מצטרף?', linkLabel: 'הקישור לחדר', copy: 'העתקה', copied: 'הקישור הועתק', copySel: 'הקישור מסומן. העתיקו אותו מהשדה.',
	wa: 'שליחה בוואטסאפ', share: 'שיתוף אחר', waText: (t) => 'שיחת וידאו בנדל"ן: ' + t,
	fromHere: 'מהדיון הזה', fromHereSub: 'מופיע כאן רק מי שכתב בדיון ואישר שיחות וידאו. הוא מקבל הודעה בפורום ומייל.', inviteOne: 'הזמנה', invitedOne: 'הוזמן',
	lock: 'נעילת החדר', lockSub: 'אחרי שכולם בפנים, אף אחד לא נכנס עוד',
	lockOn: 'החדר נעול. אף אחד חדש לא נכנס.', lockOff: 'החדר פתוח שוב לכל מי שיש לו את הקישור.',
	linkNote: 'מי שמקבל קישור נכנס מהדפדפן, עם שם ומייל. הקישור תקף לשיחה הזו בלבד.',
	lockedToast: 'החדר נעול. בקשו ממי ששלח את הקישור לפתוח את הנעילה.', fullToast: 'החדר מלא. בחדר וידאו יש מקום לעד 6 אנשים.',
	goneToast: 'השיחה או החדר בקישור הזה כבר נסגרו.', newRoom: 'פתיחת חדר חדש', lInvite: 'הזמנה', inviteAria: 'מי מצטרף: קישור, וואטסאפ והזמנה מהדיון',
};
const ERR = 'משהו השתבש. נסו שוב.';

const ICON = {
	mic: '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
	micOff: '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M4 4l16 16"/>',
	cam: '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>',
	camOff: '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3zM3 3l18 18"/>',
	flip: '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><path d="M9 13a3 3 0 0 1 5-2M15 13a3 3 0 0 1-5 2"/>',
	more: '<circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/>',
	end: '<path d="M3 14c5-5 13-5 18 0l-2 3-4-2v-2a10 10 0 0 0-6 0v2l-4 2z"/>',
	video: '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>',
	x: '<path d="M6 6l12 12M18 6L6 18"/>',
	board: '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M7 13l3-3 2 2 4-4M8 21l4-4 4 4"/>',
	invite: '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-7 7-7s7 3 7 7M19 8v6M16 11h6"/>',
};
// the shared board (assets/proforum/board.js, 1.72.674, rebuilt to design boards 16 and 17), same version query as this file so a release reaches both
const BOARD_URL = (() => { try { const u = new URL(import.meta.url); return new URL('board.js' + u.search, u).href; } catch (e) { return ''; } })();

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
// the icons are constant strings of this file, never text from a person
function icon(k, size = 22) {
	const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
	s.setAttribute('aria-hidden', 'true'); s.setAttribute('width', size); s.setAttribute('height', size); s.setAttribute('viewBox', '0 0 24 24');
	s.setAttribute('fill', 'none'); s.setAttribute('stroke', 'currentColor'); s.setAttribute('stroke-width', '2'); s.setAttribute('stroke-linecap', 'round'); s.setAttribute('stroke-linejoin', 'round');
	s.innerHTML = ICON[k];
	return s;
}
const initials = (n) => String(n || '').trim().split(/\s+/).slice(0, 2).map((w) => w.charAt(0)).join('') || '?';
const face = (f) => (f && f.name ? f.name + (f.label ? ' · ' + f.label : '') : '');
const focusables = (root) => [...root.querySelectorAll('button:not([disabled]),input:not([disabled]),a[href],[tabindex="0"]')].filter((e) => !e.hidden && e.offsetParent !== null);
function trapTab(root, ev) {
	if (ev.key !== 'Tab') return;
	const f = focusables(root); if (!f.length) return;
	const first = f[0], last = f[f.length - 1];
	if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
	else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
}

/* ---------------------------------------------------------------- the site's routes */

const st = { member: null, nonce: '', inCall: false, dismissed: new Set(), pref: null };

async function req(method, path, data, retried) {
	const o = { method, credentials: 'same-origin', headers: { Accept: 'application/json' } };
	if (st.nonce) o.headers['X-NLF-Nonce'] = st.nonce;
	let url = C.rest + path;
	if (data && method === 'GET') url += (url.includes('?') ? '&' : '?') + new URLSearchParams(data).toString();
	else if (data) { o.headers['Content-Type'] = 'application/json'; o.body = JSON.stringify(data); }
	const r = await fetch(url, o);
	let j = null; try { j = await r.json(); } catch (e) { j = null; }
	if (!r.ok || !j || j.ok !== 1) {
		const code = (j && j.code) || '';
		if (!retried && (code === 'nlfc_nonce' || code === 'nlf_nonce')) { await loadState(); return req(method, path, data, true); } // a stale page: one quiet retry
		const e = new Error((j && j.message) || ERR); e.code = code; throw e;
	}
	return j;
}
async function loadState() { const j = await req('GET', 'state', null, true); st.member = j.member || null; st.nonce = j.nonce || ''; return j; }

/* ---------------------------------------------------------------- the entry sheet: camera and microphone OFF, then join */

function sheet(o) {
	const opener = document.activeElement;
	const msg = h('p', { cls: 'nlfc-msg', role: 'status', 'aria-live': 'polite' });
	const media = { cam: false, mic: false };
	let vStream = null, aStream = null, actx = null, raf = 0, busy = false;
	const pvVideo = h('video', { playsinline: true, autoplay: true, muted: true });
	pvVideo.muted = true;
	const pv = h('div', { cls: 'nlfc-pv' }, pvVideo, h('span', { text: T.you }));
	const bars = Array.from({ length: 14 }, () => h('i'));
	const meter = h('span', { cls: 'nlfc-meter', 'aria-hidden': 'true' }, ...bars);
	const stopV = () => { if (vStream) vStream.getTracks().forEach((t) => t.stop()); vStream = null; pvVideo.srcObject = null; pv.classList.remove('is-on'); };
	const stopA = () => { cancelAnimationFrame(raf); if (aStream) aStream.getTracks().forEach((t) => t.stop()); aStream = null; if (actx) actx.close().catch(() => {}); actx = null; bars.forEach((b) => b.classList.remove('is-lit')); };
	const say = (t, bad) => { msg.textContent = t || ''; msg.classList.toggle('is-bad', !!bad); };
	const sw = (key, label, sub) => {
		const inp = h('input', { type: 'checkbox', role: 'switch', cls: 'nlfc-swin' });
		inp.addEventListener('change', async () => {
			const on = inp.checked; media[key] = on;
			if (key === 'cam') {
				if (!on) { stopV(); return; }
				try { vStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } }); pvVideo.srcObject = vStream; pvVideo.play().catch(() => {}); pv.classList.add('is-on'); say(''); }
				catch (e) { inp.checked = false; media.cam = false; say(T.blocked, true); }
			} else {
				if (!on) { stopA(); return; }
				try {
					aStream = await navigator.mediaDevices.getUserMedia({ audio: true }); say('');
					const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
					actx = new AC(); const an = actx.createAnalyser(); an.fftSize = 512; actx.createMediaStreamSource(aStream).connect(an);
					const buf = new Uint8Array(an.fftSize);
					const loop = () => { an.getByteTimeDomainData(buf); let s = 0; for (const b of buf) s += ((b - 128) / 128) ** 2; const n = Math.round(Math.min(1, Math.sqrt(s / buf.length) * 6) * bars.length); bars.forEach((b, i) => b.classList.toggle('is-lit', i < n)); raf = requestAnimationFrame(loop); };
					loop();
				} catch (e) { inp.checked = false; media.mic = false; say(T.blocked, true); }
			}
		});
		return h('label', { cls: 'nlfc-swrow' }, h('span', { cls: 'nlfc-swt' }, h('b', { text: label }), h('small', { text: sub })), inp, h('span', { cls: 'nlfc-sw', 'aria-hidden': 'true' }, h('i')));
	};
	const go = h('button', { type: 'button', cls: 'nlfc-btn nlfc-pri' + (o.hot ? ' nlfc-hot' : ''), text: o.go });
	const no = h('button', { type: 'button', cls: 'nlfc-btn nlfc-plain', text: T.notNow });
	const x = h('button', { type: 'button', cls: 'nlfc-x', 'aria-label': T.close, title: T.close }, icon('x'));
	const hid = 'nlfc-h-' + Math.random().toString(36).slice(2, 8);
	// board 19, part ה: the person who sent the link heads the sheet (initials, "<name> מזמין אתכם לחדר וידאו", trade and how many are in)
	const head = o.host
		? h('div', { cls: 'nlfc-shh' }, h('div', { cls: 'nlfc-host' }, h('span', { cls: 'nlfc-ini', 'aria-hidden': 'true', text: initials(o.host.name) }),
			h('div', null, h('h2', { id: hid, text: o.heading }), o.host.sub ? h('span', { text: o.host.sub }) : null)), x)
		: h('div', { cls: 'nlfc-shh' }, h('h2', { id: hid, text: o.heading }), x);
	const card = h('section', { cls: 'nlfc-sheet' + (o.room ? ' is-room' : ''), role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': hid, dir: 'rtl', lang: 'he' },
		head,
		o.request ? h('p', { cls: 'nlfc-req' }, h('span', { cls: 'nlfc-tag', text: o.tag || T.tag }), h('span', { text: o.request })) : null,
		o.sub ? h('p', { cls: 'nlfc-sub', text: o.sub }) : null,
		o.media === false ? null : h('div', { cls: 'nlfc-prev' }, pv, h('div', { cls: 'nlfc-pm' }, meter, h('small', { text: T.meter }))),
		o.media === false ? null : sw('cam', T.cam, T.camSub),
		o.media === false ? null : sw('mic', T.mic, T.micSub),
		o.extra || null,
		go,
		o.fine ? h('p', { cls: 'nlfc-fine', text: o.fine }) : (o.media === false ? null : h('p', { cls: 'nlfc-fine', text: T.note })),
		msg, o.media === false ? null : no);
	const scrim = h('div', { cls: 'nlfc-scrim' }, card);
	const api = {
		media, say,
		busy(on, t) { busy = !!on; go.disabled = busy; if (t !== undefined) say(t); },
		error(m) { api.busy(false); say(m || T.fail, true); },
		release() { stopV(); stopA(); },
		close(back = true) { stopV(); stopA(); scrim.remove(); document.removeEventListener('keydown', onKey, true); if (back && opener && opener.focus) opener.focus(); },
	};
	const shut = () => { if (!busy) { api.close(); if (o.onClose) o.onClose(); } };
	const onKey = (ev) => { if (ev.key === 'Escape') { ev.stopPropagation(); shut(); } else trapTab(card, ev); };
	x.addEventListener('click', shut); no.addEventListener('click', shut);
	scrim.addEventListener('click', (ev) => { if (ev.target === scrim) shut(); });
	document.addEventListener('keydown', onKey, true);
	go.addEventListener('click', async () => {
		if (busy) return;
		if (o.onGo) { api.release(); api.busy(true, T.wait); try { await o.onGo(api); } catch (e) { api.error(e && e.message); } }
	});
	document.body.appendChild(scrim);
	setTimeout(() => go.focus({ preventScroll: true }), 30);
	return api;
}

/* ---------------------------------------------------------------- the call screen */

async function joinRoom(room, media, sh, opener) {
	const tk = await req('POST', 'call/token', { room });
	const mod = await import(C.lib);
	if (!mod || typeof mod.livekitTransport !== 'function') throw new Error(T.fail);
	const tr = mod.livekitTransport({ url: tk.url, token: tk.token });
	await tr.connect();
	sh.close(false);
	stage(tr, tk, media, opener);
}

function stage(tr, tk, media, opener) {
	st.inCall = true;
	const open = !!tk.open, host = open && !!tk.host; // board 19: an open video room, and whether I opened it
	const S = { mic: false, cam: false, voice: false, facing: 'user', t0: Date.now(), timers: [], vids: new Map(), main: '', hadRemote: false, names: new Map(), others: (tk.others || []).slice(), alive: true, locked: !!tk.locked, asked: new Set() };
	const faceOf = (p) => {
		const byId = S.others.find((o) => o.identity && o.identity === p.id);
		if (byId) return byId;
		const byName = S.others.find((o) => o.name === p.name);
		return byName || { name: p.name || '', label: '' };
	};
	const firstOther = S.others[0] || { name: '', label: '' };

	// layers
	const remote = h('div', { cls: 'nlfc-remote' });
	const waitP = h('p', { cls: 'nlfc-wait', text: T.waitFor(firstOther.name) });
	const timer = h('span', { cls: 'nlfc-time', role: 'timer', 'aria-label': 'משך השיחה', text: '00:00' });
	const top = h('div', { cls: 'nlfc-top' }, h('span', { cls: 'nlfc-tag' + (open ? ' is-room' : ''), text: open ? T.roomTag : (tk.card ? T.tagCard : T.tag) }), h('span', { cls: 'nlfc-title', text: open && !tk.topic ? '' : (tk.title || C.title || '') }), timer);
	const ini = h('span', { cls: 'nlfc-ini', 'aria-hidden': 'true', text: initials(firstOther.name) });
	const whoT = h('span', { cls: 'nlfc-whot', text: face(firstOther) });
	const who = h('div', { cls: 'nlfc-who' }, ini, whoT);
	const strip = h('div', { cls: 'nlfc-strip' });
	const banner = h('p', { cls: 'nlfc-banner', role: 'status', 'aria-live': 'polite', hidden: true });
	const audioB = h('button', { type: 'button', cls: 'nlfc-audio', hidden: true, text: T.audio });
	const selfV = h('video', { playsinline: true, autoplay: true, muted: true }); selfV.muted = true;
	const self = h('div', { cls: 'nlfc-self is-off' }, selfV, h('span', { text: T.you }));
	const photoB = h('button', { type: 'button', cls: 'nlfc-act nlfc-act-w', text: T.photo, hidden: !C.photo });
	const inviteB = h('button', { type: 'button', cls: 'nlfc-act', text: T.invite });
	const acts = h('div', { cls: 'nlfc-acts' }, photoB, inviteB);
	const ctl = (k, label, lab, cls) => h('button', { type: 'button', cls: 'nlfc-c ' + (cls || ''), 'aria-label': label }, icon(k), h('small', { 'aria-hidden': 'true', text: lab }));
	const bMic = ctl('micOff', T.micOn, T.lMic), bCam = ctl('camOff', T.camOn, T.lCam), bFlip = ctl('flip', T.flip, T.lFlip, 'nlfc-flip'), bMore = ctl('more', T.more, T.lMore), bEnd = ctl('end', T.end, T.lEnd, 'nlfc-end');
	const bBoard = ctl('board', 'לוח משותף: ציור, תמונה או תוכנית והערות עליה', 'לוח', 'nlfc-board');
	const bInv = ctl('invite', T.inviteAria, T.lInvite, 'nlfc-inv'); // board 19, part ד: "הזמנה" in the bar of an open room
	bInv.hidden = !open;
	let board = null;
	// the board shows its own copy of the call controls (design boards 16 and 17); they act only through these callbacks
	if (BOARD_URL) import(BOARD_URL).then((m) => {
		if (!S.alive || !m || !m.createBoard) return;
		board = m.createBoard({
			tr, title: tk.title || C.title || '', t0: S.t0,
			face: (id) => { const p = tr.participants().find((x) => x.id === id); return p ? faceOf(p) : null; },
			call: { mic: (on) => setMic(on), cam: (on) => setCam(on), leave: () => leave() },
			onClose: () => { if (S.alive && !bBoard.hidden) bBoard.focus({ preventScroll: true }); },
		});
	}).catch(() => { bBoard.hidden = true; });
	else bBoard.hidden = true;
	bBoard.setAttribute('aria-pressed', 'false');
	bBoard.addEventListener('click', () => { if (board) board.open(); });
	bMic.setAttribute('aria-pressed', 'false'); bCam.setAttribute('aria-pressed', 'false'); bMore.setAttribute('aria-expanded', 'false');
	const coarse = window.matchMedia && window.matchMedia('(pointer: coarse)').matches;
	bFlip.hidden = !coarse; bFlip.disabled = true;
	const voiceIn = h('input', { type: 'checkbox', role: 'switch', cls: 'nlfc-swin' });
	// the host's lock switch: in the "מי מצטרף?" sheet and in "עוד"; every copy shows the same state
	const lockIns = [];
	const lockRow = () => {
		for (let i = lockIns.length - 1; i >= 0; i--) if (!lockIns[i].isConnected) lockIns.splice(i, 1); // copies in sheets already closed
		const inp = h('input', { type: 'checkbox', role: 'switch', cls: 'nlfc-swin' });
		inp.checked = S.locked;
		lockIns.push(inp);
		inp.addEventListener('change', async () => {
			const want = inp.checked;
			lockIns.forEach((i) => { i.disabled = true; });
			try { const j = await req('POST', 'call/lock', { room: tk.room, lock: want ? 1 : 0 }); S.locked = !!j.lock; say(S.locked ? T.lockOn : T.lockOff, 4000); }
			catch (e) { say(e.message, 5000); }
			lockIns.forEach((i) => { i.disabled = false; i.checked = S.locked; });
		});
		return h('label', { cls: 'nlfc-swrow nlfc-lockrow' }, h('span', { cls: 'nlfc-swt' }, h('b', { text: T.lock }), h('small', { text: T.lockSub })), inp, h('span', { cls: 'nlfc-sw', 'aria-hidden': 'true' }, h('i')));
	};
	const menu = h('div', { cls: 'nlfc-menu', hidden: true, role: 'group', 'aria-label': T.more },
		h('label', { cls: 'nlfc-swrow' }, h('span', { cls: 'nlfc-swt' }, h('b', { text: T.voice })), voiceIn, h('span', { cls: 'nlfc-sw', 'aria-hidden': 'true' }, h('i'))),
		host ? lockRow() : null,
		h('p', { cls: 'nlfc-fine', text: T.norec }));
	const bar = h('div', { cls: 'nlfc-ctl' }, bMic, bCam, bFlip, bBoard, bInv, bMore, bEnd);
	const root = h('div', { cls: 'nlfc-stage', role: 'dialog', 'aria-modal': 'true', 'aria-label': T.callAria, dir: 'rtl', lang: 'he' },
		remote, waitP, top, who, strip, banner, audioB, h('div', { cls: 'nlfc-fill' }), self, acts, menu, bar, h('p', { cls: 'nlfc-norec', text: T.norec }));
	document.documentElement.classList.add('nlfc-open');
	document.body.appendChild(root);
	setTimeout(() => bMic.focus({ preventScroll: true }), 30);

	let bannerT = 0;
	const say = (t, ms) => { clearTimeout(bannerT); banner.textContent = t || ''; banner.hidden = !t; if (t && ms) bannerT = setTimeout(() => { banner.hidden = true; }, ms); };

	// the invite button: only people of this discussion who are not in the room yet
	const candidates = () => {
		if (tk.card || !tk.topic || (tk.topic | 0) !== (C.topic | 0)) return []; // a call from a card has no discussion to invite from
		const inRoom = new Set(S.others.map((o) => o.id | 0));
		return (C.targets || []).filter((t) => !inRoom.has(t.with | 0));
	};
	const paintInvite = () => { inviteB.hidden = open || !candidates().length; acts.hidden = inviteB.hidden && photoB.hidden; }; // an open room invites from the bar
	paintInvite();

	// board 19: a person who came in by the link is not in tk.others; ask the room once for the names of who is inside
	let peopleT = 0;
	const askPeople = (id) => {
		if (!open || S.asked.has(id)) return;
		S.asked.add(id);
		clearTimeout(peopleT);
		peopleT = setTimeout(async () => {
			try {
				const s = await req('GET', 'call/status', { room: tk.room });
				for (const p of s.people || []) {
					if (!p.identity || p.identity === tk.identity) continue;
					const o = S.others.find((x) => (x.id | 0) === (p.id | 0));
					if (o) o.identity = p.identity; else S.others.push({ id: p.id, identity: p.identity, name: p.name, label: p.label });
				}
				S.names.forEach((n, k) => { const f = S.others.find((o) => o.identity === k); if (f) S.names.set(k, f.name); });
				paint();
			} catch (e) { /* the LiveKit name stays */ }
		}, 700);
	};

	// board 19, part ד: "מי מצטרף?" the link, WhatsApp, other share, people of this discussion, and the host's lock
	function whoSheet() {
		const link = tk.link || location.href;
		const title = tk.title || C.title || T.roomH;
		const box = h('div', { cls: 'nlfc-pick' });
		const field = h('input', { type: 'text', readonly: true, value: link, 'aria-label': T.linkLabel, dir: 'ltr', spellcheck: 'false' });
		const copyB = h('button', { type: 'button', text: T.copy });
		box.appendChild(h('div', { cls: 'nlfc-linkrow' }, field, copyB));
		const wa = h('a', { cls: 'nlfc-wa', href: 'https://wa.me/?text=' + encodeURIComponent(T.waText(title) + '\n' + link), target: '_blank', rel: 'noopener', text: T.wa });
		const shareB = h('button', { type: 'button', cls: 'nlfc-share', text: T.share, hidden: typeof navigator.share !== 'function' });
		box.appendChild(h('div', { cls: 'nlfc-send' + (shareB.hidden ? ' is-one' : '') }, wa, shareB));
		const list = candidates();
		if (list.length) {
			const from = h('div', { cls: 'nlfc-from' }, h('b', { text: T.fromHere }));
			for (const t of list) {
				const b = h('button', { type: 'button', text: T.inviteOne, 'aria-label': T.inviteOne + ': ' + t.name });
				b.addEventListener('click', async () => {
					b.disabled = true;
					try {
						await req('POST', 'call/open', { topic: tk.topic, with: t.with, room: tk.room });
						S.others.push({ id: t.with, identity: '', name: t.name, label: t.label });
						b.textContent = T.invitedOne; sh.say(T.invited(t.name));
					} catch (e) { b.disabled = false; sh.say(e.message, true); }
				});
				from.appendChild(h('div', { cls: 'nlfc-person' }, h('span', { cls: 'nlfc-ini', 'aria-hidden': 'true', text: initials(t.name) }), h('span', { text: face(t) }), b));
			}
			from.appendChild(h('p', { cls: 'nlfc-fine', text: T.fromHereSub }));
			box.appendChild(from);
		}
		if (host) box.appendChild(lockRow());
		box.appendChild(h('p', { cls: 'nlfc-fine', text: T.linkNote }));
		const sh = sheet({ heading: T.whoH, go: T.close, media: false, extra: box, room: true, onGo: async (api) => api.close() });
		copyB.addEventListener('click', async () => {
			try { await navigator.clipboard.writeText(link); sh.say(T.copied); }
			catch (e) { field.focus(); field.select(); sh.say(T.copySel); }
		});
		field.addEventListener('focus', () => field.select());
		shareB.addEventListener('click', () => { navigator.share({ title: T.waText(title), text: T.waText(title), url: link }).catch(() => {}); });
		return sh;
	}
	bInv.addEventListener('click', () => whoSheet());

	S.timers.push(setInterval(() => { const s = Math.floor((Date.now() - S.t0) / 1000); timer.textContent = String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); }, 1000));

	function paint() {
		if (!S.alive) return;
		const ps = tr.participants(), me = ps.find((p) => p.local), rs = ps.filter((p) => !p.local);
		// one video element per person in the room, created once
		for (const p of rs) {
			if (!S.vids.has(p.id)) { const v = h('video', { playsinline: true, autoplay: true }); S.vids.set(p.id, v); remote.appendChild(v); }
			if (open && !S.others.find((o) => o.identity && o.identity === p.id)) askPeople(p.id);
			if (!S.names.has(p.id)) { S.names.set(p.id, faceOf(p).name); if (open || S.hadRemote || rs.length > 1) say(T.joined(faceOf(p).name), 3000); }
			if (p.cam && !S.voice) tr.attach(p.id, 'camera', S.vids.get(p.id));
		}
		for (const [id, v] of S.vids) if (!rs.find((p) => p.id === id)) { v.remove(); S.vids.delete(id); say(T.left(S.names.get(id) || firstOther.name), 6000); S.names.delete(id); }
		if (rs.length) S.hadRemote = true;
		// the large picture: whoever speaks, else the one already shown, else the first
		const speaking = rs.find((p) => p.speaking);
		const main = speaking || rs.find((p) => p.id === S.main) || rs[0] || null;
		S.main = main ? main.id : '';
		for (const [id, v] of S.vids) v.hidden = id !== S.main || !main.cam || S.voice; // no frozen last frame when the camera goes off
		const f = main ? faceOf(main) : firstOther;
		ini.textContent = initials(f.name); whoT.textContent = face(f);
		who.hidden = open && !main; // an open room with nobody else in: no empty name pill
		waitP.hidden = !!(main && main.cam && !S.voice);
		waitP.textContent = !main ? (open ? T.roomWait : (S.hadRemote ? T.left(f.name) : T.waitFor(f.name))) : (S.voice ? T.voiceOn : T.noCam(f.name));
		// the others (a third or fourth person) as small name discs
		strip.replaceChildren(...rs.filter((p) => p.id !== S.main).map((p) => h('span', { cls: 'nlfc-disc' + (p.speaking ? ' is-speaking' : ''), title: faceOf(p).name, text: initials(faceOf(p).name) })));
		// myself
		if (me) { S.mic = me.mic; S.cam = me.cam; }
		self.classList.toggle('is-off', !S.cam);
		self.classList.toggle('is-mirror', S.facing === 'user');
		if (S.cam && me) tr.attach(me.id, 'camera', selfV);
		bMic.replaceChildren(icon(S.mic ? 'mic' : 'micOff'), h('small', { 'aria-hidden': 'true', text: T.lMic }));
		bMic.setAttribute('aria-pressed', S.mic ? 'true' : 'false'); bMic.setAttribute('aria-label', S.mic ? T.micOff : T.micOn);
		bCam.replaceChildren(icon(S.cam ? 'cam' : 'camOff'), h('small', { 'aria-hidden': 'true', text: T.lCam }));
		bCam.setAttribute('aria-pressed', S.cam ? 'true' : 'false'); bCam.setAttribute('aria-label', S.cam ? T.camOff : T.camOn);
		bFlip.disabled = !S.cam;
	}

	tr.onParticipants(paint);
	tr.onSpeaking(paint);
	tr.onState((s) => {
		if (s === 'reconnecting') say(T.reconnecting);
		else if (s === 'connected') say('');
		else if (s === 'disconnected' && S.alive) say(T.lost);
		else if (s === 'audio-blocked') audioB.hidden = false;
	});
	try { if (tr.room && !tr.room.canPlaybackAudio) audioB.hidden = false; } catch (e) { /* none */ }
	audioB.addEventListener('click', async () => { try { await tr.startAudio(); } catch (e) { /* tried */ } audioB.hidden = true; });

	async function setMic(on) { try { await tr.setMicrophone(on); } catch (e) { say(T.denied, 7000); } paint(); }
	async function setCam(on) { try { await tr.setCamera(on); } catch (e) { say(T.denied, 7000); } paint(); }
	bMic.addEventListener('click', () => setMic(!S.mic));
	bCam.addEventListener('click', () => setCam(!S.cam));
	bFlip.addEventListener('click', async () => { if (!S.cam) return; try { S.facing = await tr.switchCamera(); } catch (e) { /* one camera only */ } paint(); });
	bMore.addEventListener('click', () => { menu.hidden = !menu.hidden; bMore.setAttribute('aria-expanded', menu.hidden ? 'false' : 'true'); if (!menu.hidden) voiceIn.focus(); });
	voiceIn.addEventListener('change', () => { S.voice = voiceIn.checked; try { tr.setVideoReceive(!S.voice); } catch (e) { /* older transport */ } say(S.voice ? T.voiceOn : T.voiceOff, 3000); paint(); });

	inviteB.addEventListener('click', () => {
		const list = candidates();
		if (!list.length) { say(T.noOne, 4000); return; }
		const box = h('div', { cls: 'nlfc-pick' });
		const sh = sheet({ heading: T.inviteH, sub: T.inviteSub, go: T.close, media: false, extra: box, onGo: async (api) => api.close() });
		for (const t of list) {
			const b = h('button', { type: 'button', cls: 'nlfc-btn nlfc-line', text: face(t) });
			b.addEventListener('click', async () => {
				b.disabled = true;
				try {
					await req('POST', 'call/open', { topic: tk.topic, with: t.with, room: tk.room });
					S.others.push({ id: t.with, identity: '', name: t.name, label: t.label });
					sh.close(); say(T.invited(t.name), 4000); paintInvite();
				} catch (e) { b.disabled = false; sh.say(e.message, true); }
			});
			box.appendChild(b);
		}
	});

	const onKey = (ev) => {
		if (ev.key === 'Escape' && !menu.hidden) { menu.hidden = true; bMore.setAttribute('aria-expanded', 'false'); bMore.focus(); ev.stopPropagation(); return; }
		if (document.querySelector('.nlfc-scrim')) return; // a sheet on top keeps the keys
		if (board && board.shown) return; // the shared board on top keeps the keys too
		trapTab(root, ev);
	};
	document.addEventListener('keydown', onKey, true);
	const onHide = () => { try { tr.disconnect(); } catch (e) { /* closing */ } };
	window.addEventListener('pagehide', onHide);

	async function leave() {
		if (!S.alive) return;
		S.alive = false; st.inCall = false;
		S.timers.forEach(clearInterval); clearTimeout(bannerT);
		if (board) { try { board.destroy(); } catch (e) { /* gone */ } board = null; }
		document.removeEventListener('keydown', onKey, true); window.removeEventListener('pagehide', onHide);
		try { await tr.disconnect(); } catch (e) { /* already apart */ }
		root.remove(); document.documentElement.classList.remove('nlfc-open');
		if (/^#call=/.test(location.hash)) history.replaceState(null, '', location.pathname + location.search);
		if (!open && (tk.topic | 0) !== (C.topic | 0) && tk.topic_url) { location.assign(tk.topic_url); return; } // back to the discussion (an open room stays on its page)
		const back = opener && document.contains(opener) ? opener : document.querySelector('.nlf-thread h1, .nlf-page h1');
		if (back) { if (!back.hasAttribute('tabindex') && back.tagName === 'H1') back.setAttribute('tabindex', '-1'); back.focus(); }
	}
	bEnd.addEventListener('click', leave);

	paint();
	if (media && media.mic) setMic(true);
	if (media && media.cam) setCam(true);
	// board 19: the host who comes into an empty room gets "מי מצטרף?" once, by itself
	if (host && !tr.participants().some((p) => !p.local)) setTimeout(() => { if (S.alive && !document.querySelector('.nlfc-scrim')) whoSheet(); }, 400);
}

/* ---------------------------------------------------------------- the three ways in */

function needEntry(heading, sub) {
	const enter = h('button', { type: 'button', cls: 'nlfc-btn nlfc-line', 'data-nlf-enter': true, text: T.enter }); // forum.js opens its entry on this attribute
	const sh = sheet({ heading, sub: sub || T.needSub, go: T.close, media: false, extra: enter, onGo: async (api) => api.close() });
	enter.addEventListener('click', () => sh.close(false));
}

// a guest who pressed a call button: after the forum's entry (which reloads the page, the #fragment kept) the call sheet opens by itself.
// board 19: the same for the open room ({room: 1, topic}): the lobby opens by itself on the same page.
const PENDING = 'nlfc_pending';
function savePending(target) {
	try { sessionStorage.setItem(PENDING, JSON.stringify({ room: target.room ? 1 : 0, topic: target.topic | 0, card: target.card | 0, with: target.with | 0, name: String(target.name || ''), label: String(target.label || ''), t: Date.now() })); } catch (e) { /* private mode: the member presses again */ }
}
function takePending() {
	let p = null;
	try { p = JSON.parse(sessionStorage.getItem(PENDING) || 'null'); sessionStorage.removeItem(PENDING); } catch (e) { p = null; }
	if (!p || Date.now() - (p.t | 0) > 15 * 60 * 1000) return null;
	if (p.room) return (p.topic | 0) === (C.topic | 0) && (p.card | 0) === (C.card | 0) ? p : null; // only on the page it was pressed on
	if (!p.with) return null;
	if (p.card ? (p.card | 0) !== (C.card | 0) : (p.topic | 0) !== (C.topic | 0)) return null; // only on the page it was pressed on
	return p;
}

/* ---------------------------------------------------------------- board 19: the open video room */

// part ג: the lobby (camera and microphone check), then the room opens; a guest enters the forum first
function roomLobby(topic, opener) {
	topic = topic | 0;
	if (!st.member) { savePending({ room: 1, topic, card: C.card }); needEntry(T.roomNeedH, T.roomNeedSub); return; }
	sheet({
		heading: T.roomH, tag: T.tagTopic, request: topic && topic === (C.topic | 0) ? (C.title || '') : '', go: T.roomGo, hot: true, room: true,
		onGo: async (sh) => {
			const o = await req('POST', 'call/room', topic ? { topic } : {});
			await joinRoom(o.room, sh.media, sh, opener);
		},
	});
}

// part ה: what the person who got the link sees
function roomJoin(room, s, opener) {
	const from = s.from || {};
	const sub = [from.label || '', (s.joined | 0) > 0 ? T.inRoom(s.joined | 0) : ''].filter(Boolean).join(' · ');
	sheet({
		heading: T.joinRoomH(from.name), host: { name: from.name || '', sub }, tag: T.tagTopic, request: (s.topic | 0) ? (s.title || '') : '',
		go: T.joinRoomGo, hot: true, room: true, media: false, fine: T.joinRoomNote,
		onGo: async (sh) => {
			if (!s.in) await req('POST', 'call/join', { room });
			await joinRoom(room, sh.media, sh, opener);
		},
	});
}

const clearHash = () => { if (/^#call=/.test(location.hash || '')) history.replaceState(null, '', location.pathname + location.search); };

function startWith(target, opener) {
	if (!st.member) { savePending(target); needEntry(T.needH); return; }
	const card = target.card | 0;
	sheet({
		heading: T.startH(target.name), request: card ? '' : (C.title || ''), sub: target.label || '', go: T.startGo,
		onGo: async (sh) => {
			const o = await req('POST', 'call/open', card ? { card, with: target.with } : { topic: target.topic, with: target.with });
			await joinRoom(o.room, sh.media, sh, opener);
		},
	});
}

function joinInvite(room, info, opener) {
	sheet({
		heading: T.joinH, request: info.title || '', sub: T.joinSub(face({ name: info.from, label: info.label }) || ''), go: T.joinGo,
		onGo: async (sh) => { await joinRoom(room, sh.media, sh, opener); },
	});
}

async function fromHash() {
	const m = /^#call=([a-z2-7]{12})$/.exec(location.hash || '');
	if (!m) return;
	// a guest cannot ask which kind of link this is; on the forum home only an open room's link lands, so the wording says "חדר"
	if (!st.member) { if (!(C.topic | 0) && !(C.card | 0)) needEntry(T.joinRoomNeedH, T.joinRoomNeedSub); else needEntry(T.needH); return; }
	if (st.inCall) return;
	try {
		const s = await req('GET', 'call/status', { room: m[1] });
		if (!s.exists) {
			clearHash();
			const btn = document.querySelector('[data-nlf-room]');
			toast(T.goneToast, btn ? [{ label: T.newRoom, primary: true, fn: () => roomLobby(btn.getAttribute('data-nlf-room'), btn) }, { label: T.close }] : null);
			return;
		}
		if (s.open) { // board 19: an open room
			if (!s.in && s.locked) { clearHash(); toast(T.lockedToast, [{ label: T.close }]); return; }
			if (!s.in && s.full) { clearHash(); toast(T.fullToast, [{ label: T.close }]); return; }
			roomJoin(m[1], s);
			return;
		}
		joinInvite(m[1], { title: s.title, from: s.from && s.from.name, label: s.from && s.from.label });
	} catch (e) { toast(e.message); }
}

/* the in-forum notice: a card at the bottom while the member is on any forum page */
let toastBox = null;
function toast(text, buttons) {
	if (!toastBox) { toastBox = h('div', { cls: 'nlfc-toasts', dir: 'rtl', lang: 'he', role: 'region', 'aria-label': T.prefH }); document.body.appendChild(toastBox); }
	const card = h('div', { cls: 'nlfc-toast', role: 'status' }, h('p', { text }));
	const row = h('div', { cls: 'nlfc-toastrow' });
	for (const b of buttons || [{ label: T.close }]) row.appendChild(h('button', { type: 'button', cls: 'nlfc-btn ' + (b.primary ? 'nlfc-pri' : 'nlfc-plain'), text: b.label, onclick: () => { card.remove(); if (b.fn) b.fn(); } }));
	card.appendChild(row);
	toastBox.appendChild(card);
	if (!buttons) setTimeout(() => card.remove(), 6000);
	return card;
}

async function poll() {
	if (!st.member || st.inCall || document.visibilityState !== 'visible') return;
	let s;
	try { s = await req('GET', 'call/status'); } catch (e) { if (/closed|need_entry|off/.test(e.code || '')) stopPoll(); return; }
	st.pref = s.pref || st.pref;
	paintPref();
	for (const i of s.invites || []) {
		if (st.dismissed.has(i.room)) continue;
		st.dismissed.add(i.room);
		toast(T.inviteToast(face({ name: i.from, label: i.label }), i.title), [
			{ label: T.joinGo, primary: true, fn: () => ((i.topic | 0) === (C.topic | 0) ? joinInvite(i.room, i) : location.assign(i.url)) },
			{ label: T.notNow },
		]);
	}
}
let pollT = 0;
const stopPoll = () => { clearInterval(pollT); pollT = 0; };

/* the member's own switches */
const prefBoxes = [];
function prefPanel() {
	const msg = h('p', { cls: 'nlfc-msg', role: 'status', 'aria-live': 'polite' });
	const mk = (key, label, sub) => {
		const inp = h('input', { type: 'checkbox', role: 'switch', cls: 'nlfc-swin', 'data-k': key });
		inp.addEventListener('change', async () => {
			inp.disabled = true;
			try { const j = await req('POST', 'call/pref', { [key]: inp.checked ? 1 : 0 }); st.pref = j.pref; msg.textContent = j.message || ''; }
			catch (e) { inp.checked = !inp.checked; msg.textContent = e.message; }
			inp.disabled = false; paintPref();
		});
		return h('label', { cls: 'nlfc-swrow' }, h('span', { cls: 'nlfc-swt' }, h('b', { text: label }), h('small', { text: sub })), inp, h('span', { cls: 'nlfc-sw', 'aria-hidden': 'true' }, h('i')));
	};
	const box = h('div', { cls: 'nlfc-pref' }, mk('video', T.prefVideo, T.prefVideoSub), mk('mail', T.prefMail, T.prefMailSub), msg);
	prefBoxes.push(box);
	paintPref();
	return box;
}
function paintPref() {
	if (!st.pref) return;
	for (const b of prefBoxes) b.querySelectorAll('input[data-k]').forEach((i) => { i.checked = !!st.pref[i.getAttribute('data-k')]; });
}
function mountPref() {
	if (!st.member) return;
	const spots = document.querySelectorAll('[data-nlf-callpref]');
	if (spots.length) { spots.forEach((s) => { s.replaceChildren(h('h3', { cls: 'nlfc-h3', text: T.prefH }), prefPanel()); }); return; }
	const bar = document.querySelector('.nlf-mebar');
	if (!bar || bar.querySelector('.nlfc-preflink')) return;
	const link = h('button', { type: 'button', cls: 'nlf-link nlfc-preflink', text: T.prefH });
	link.addEventListener('click', () => { sheet({ heading: T.prefH, go: T.close, media: false, extra: prefPanel(), onGo: async (api) => api.close() }); });
	bar.appendChild(link);
}

/* the pills (board 18, part D): on the author row of EVERY answer whose author switched video on, and of the opening message
   when its author did; shown to guests too (the press asks them to enter first). A row that already has one is left alone. */
function injectButtons() {
	if (!C.topic || !Array.isArray(C.targets) || !C.targets.length) return;
	for (const t of C.targets) {
		const rows = [];
		if (t.op) rows.push(document.querySelector('.nlf-op .nlf-arow'));
		for (const id of (Array.isArray(t.replies) ? t.replies : (t.reply ? [t.reply] : []))) rows.push(document.querySelector('#r' + (id | 0) + ' .nlf-arow'));
		for (const row of rows) {
			if (!row || row.querySelector('[data-nlf-call]')) continue;
			const b = h('button', { type: 'button', cls: 'nlf-pill nlfc-pill nlfm-vpill', 'data-nlf-call': C.topic | 0, 'data-nlf-with': t.with | 0, 'aria-label': T.btnWith(t.name) }, icon('video', 17), h('span', { text: T.btn }));
			row.insertBefore(b, row.querySelector(':scope > time'));
		}
	}
}

function onPress(ev) {
	const rb = ev.target.closest('[data-nlf-room]'); // board 19: the open video room's buttons (home band, discussion row, card row)
	if (rb) { ev.preventDefault(); if (!st.inCall) roomLobby(parseInt(rb.getAttribute('data-nlf-room'), 10) || 0, rb); return; }
	const b = ev.target.closest('[data-nlf-call],[data-nlf-callcard]');
	if (!b) return;
	ev.preventDefault();
	const card = parseInt(b.getAttribute('data-nlf-callcard'), 10) || 0;
	const topic = parseInt(b.getAttribute('data-nlf-call'), 10) || 0, w = parseInt(b.getAttribute('data-nlf-with'), 10) || 0;
	if ((!topic && !card) || !w || st.inCall) return;
	const known = (C.targets || []).find((t) => (t.with | 0) === w) || {};
	startWith({ topic, card, with: w, name: known.name || b.getAttribute('data-nlf-name') || '', label: known.label || b.getAttribute('data-nlf-label') || '' }, b);
}

async function boot() {
	if (!C || !C.rest || typeof fetch !== 'function' || window.__nlfcall) return;
	window.__nlfcall = true;
	document.addEventListener('click', onPress);
	injectButtons(); // the pills need no state: a guest sees them too
	try { await loadState(); } catch (e) { return; } // the forum is closed for this visitor: nothing to show
	mountPref();
	const pend = st.member && !/^#call=/.test(location.hash || '') ? takePending() : null;
	if (pend && pend.room) roomLobby(pend.topic, document.querySelector('[data-nlf-room]'));
	else if (pend) startWith(pend, document.querySelector(pend.card ? '[data-nlf-callcard]' : '[data-nlf-with="' + (pend.with | 0) + '"]'));
	fromHash();
	window.addEventListener('hashchange', fromHash);
	if (st.member) {
		poll();
		pollT = setInterval(poll, 25000);
		document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') poll(); });
	}
}

boot();
