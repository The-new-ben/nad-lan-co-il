/* nad-lan professionals' forum: pictures, plans (PDF) and files in posts (inc/pro-forum-media.php, Claude Design board 21).
   What it adds, without a library and without HTML strings (every node is built, every text goes in through textContent):
   - the composer inside the forum's two forms (a new discussion and an answer): camera, pictures, plan / PDF, drag and drop,
     paste, thumbs with ×, order numbers, drag to reorder (pointer events; touch-action pan-y, so a phone still scrolls), a caption
     per file, progress per file. Every picture is drawn again on a canvas in the browser (at most 2560 px, JPEG or WebP), which
     leaves its location and camera data behind, then sent alone (XHR with progress) and kept by its id. forum.js reads
     form.nlfExtra(path) when the post is written; a post waits until every file is up.
   - the full-screen view: swipe, arrows, Escape, counter, author and time, caption, dots, the points other members marked (a
     press goes to their answer), "לסמן נקודה ולשאול" (a tap on the picture, then the answer form opens with a crop of the point),
     and "שיחת וידאו עליה" (the discussion's video room opens; its shared board gets the picture as its sheet through the
     'nlf:board' event of call.js and board.takeImage of board.js).
   - the member's picture: choose, drag to centre in the circle, zoom, 256 x 256, save or remove. */
(function () {
	'use strict';
	var C = window.NLFMD;
	if (!C || !C.rest || !C.on || !window.fetch || !window.FormData || !window.Promise) { return; }
	var NLF = window.NLF || {};
	var L = C.limits;
	var ERR = 'משהו השתבש. נסו שוב.';
	var BKEY = 'nlfmd_board';
	var T = {
		cam: 'מצלמה', pics: 'תמונות', pdf: 'תוכנית / PDF', more: 'עוד', moreAria: 'עוד תמונות',
		gps: 'המיקום הוסר מהתמונות', drag: 'גוררים כדי לשנות סדר', list: 'קבצים מצורפים',
		cap: 'כיתוב לתמונה (לא חובה)', capPdf: 'שם התוכנית (לא חובה)', capFor: function (n) { return 'כיתוב לקובץ ' + n; },
		item: function (n, pdf) { return (pdf ? 'קובץ PDF ' : 'תמונה ') + n; }, itemHint: 'לחיצה לכיתוב. Alt וחץ כדי להזיז',
		remove: function (n) { return 'הסרת קובץ ' + n; }, removed: function (n) { return 'קובץ ' + n + ' הוסר.'; }, moved: function (n) { return 'הקובץ עבר למקום ' + n + '.'; },
		drop: 'שחררו כאן כדי לצרף',
		big: 'התמונה גדולה מ-' + L.imgMb + 'MB.', bigPdf: 'הקובץ גדול מ-' + L.pdfMb + 'MB.', kind: 'אפשר לצרף רק תמונה או קובץ PDF.', notPdf: 'כאן מצרפים קובץ PDF בלבד.',
		bad: 'לא הצלחנו לפתוח את התמונה. נסו JPG או PNG.', max: function (n) { return 'אפשר לצרף עד ' + n + ' קבצים.'; },
		up: function (n, p) { return 'מעלים ' + (n === 1 ? 'קובץ אחד' : n + ' קבצים') + ' · ' + p + '%'; }, upDone: 'הקבצים מוכנים לשליחה.',
		upFail: 'קובץ אחד לא עלה. הסירו אותו ונסו שוב.', errShort: 'לא עלה', wait: 'רגע, הקבצים עוד עולים. ההודעה תישלח מיד אחריהם.',
		enter: 'כדי לצרף קבצים צריך להיכנס. זה צעד אחד.', enterBtn: 'כניסה', lost: 'החיבור נקטע. נסו שוב.',
		pinT: 'נקודה מסומנת על תמונה', unpin: 'ביטול הסימון', pinOn: 'סימנתם נקודה. כתבו מה תרצו לשאול עליה.',
		lb: 'תמונות במסך מלא', close: 'סגירה', prev: 'התמונה הקודמת', next: 'התמונה הבאה',
		mark: 'לסמן נקודה ולשאול', video: 'שיחת וידאו עליה', markHint: 'הקישו על הנקודה בתמונה שתרצו לשאול עליה', markGo: 'לשאול על הנקודה', markCancel: 'ביטול',
		pinOf: function (n) { return 'נקודה ש' + (n || 'חבר הפורום') + ' סימן/ה. מעבר לתשובה'; }, alt: 'תמונה מהדיון',
		avSaved: 'התמונה נשמרה. היא תופיע ליד השם שלכם בכל הפורום.', avPick: 'בחרו תמונה קודם.'
	};
	var $ = function (s, r) { return (r || document).querySelector(s); };
	var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
	function el(tag, a) {
		var n = document.createElement(tag);
		Object.keys(a || {}).forEach(function (k) {
			var v = a[k];
			if (k === 'cls') { n.className = v; } else if (k === 'text') { n.textContent = v; }
			else if (v === true) { n.setAttribute(k, ''); } else if (v !== false && v !== null && v !== undefined) { n.setAttribute(k, String(v)); }
		});
		for (var i = 2; i < arguments.length; i++) { if (arguments[i]) { n.appendChild(arguments[i]); } }
		return n;
	}
	function svg(d) {
		var NS = 'http://www.w3.org/2000/svg', s = document.createElementNS(NS, 'svg'), p = document.createElementNS(NS, 'path');
		s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('width', '26'); s.setAttribute('height', '26'); s.setAttribute('aria-hidden', 'true'); s.setAttribute('focusable', 'false');
		p.setAttribute('d', d); p.setAttribute('fill', 'none'); p.setAttribute('stroke', 'currentColor'); p.setAttribute('stroke-width', '2.4'); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round');
		s.appendChild(p);
		return s;
	}

	/* ---------------- the member and the network ---------------- */
	var st = { member: null, nonce: '', loaded: false, p: null };
	function state(force) {
		if (st.p && !force) { return st.p; }
		st.p = fetch(C.rest + 'state', { credentials: 'same-origin', headers: { Accept: 'application/json' } }).then(function (r) { return r.json(); }).then(function (j) {
			st.member = (j && j.member) || null; st.nonce = (j && j.nonce) || ''; st.loaded = true; return st;
		}).catch(function () { st.p = null; return st; });
		return st.p;
	}
	state();
	/* one request with the forum's header nonce; DELETE goes as POST + X-HTTP-Method-Override (some hosts drop DELETE) */
	function send(method, path, body, onProgress, hold, again) {
		return state().then(function () {
			return new Promise(function (res, rej) {
				var x = new XMLHttpRequest();
				if (hold) { hold.xhr = x; }
				x.open('POST', C.rest + path, true);
				x.setRequestHeader('Accept', 'application/json');
				if (st.nonce) { x.setRequestHeader('X-NLF-Nonce', st.nonce); }
				if (NLF.wpnonce) { x.setRequestHeader('X-WP-Nonce', NLF.wpnonce); }
				if (method !== 'POST') { x.setRequestHeader('X-HTTP-Method-Override', method); }
				if (onProgress && x.upload) { x.upload.onprogress = function (e) { if (e.lengthComputable && e.total) { onProgress(e.loaded / e.total); } }; }
				x.onload = function () {
					var j = null;
					try { j = JSON.parse(x.responseText); } catch (e) { j = null; }
					if (x.status >= 200 && x.status < 300 && j && j.ok === 1) { res(j); return; }
					var er = new Error((j && j.message) || ERR); er.code = j && j.code; rej(er);
				};
				x.onerror = function () { rej(new Error(T.lost)); };
				x.onabort = function () { var e = new Error(''); e.code = 'abort'; rej(e); };
				x.send(body || null);
			});
		}).catch(function (er) {
			if (er.code === 'nlf_nonce' && !again) { return state(true).then(function () { return send(method, path, body, onProgress, hold, true); }); } // a stale page: one quiet retry
			throw er;
		});
	}

	/* ---------------- pictures in the browser: decode, draw again, export (no location, no camera data) ---------------- */
	function viaImg(f) {
		return new Promise(function (res, rej) {
			var u = URL.createObjectURL(f), im = new Image();
			im.onload = function () { URL.revokeObjectURL(u); res(im); };
			im.onerror = function () { URL.revokeObjectURL(u); rej(new Error(T.bad)); };
			im.src = u;
		});
	}
	function decode(f) {
		if (!window.createImageBitmap) { return viaImg(f); }
		return createImageBitmap(f, { imageOrientation: 'from-image' }).catch(function () { return createImageBitmap(f); }).catch(function () { return viaImg(f); });
	}
	function toBlob(cv, type, q) {
		return new Promise(function (res) {
			cv.toBlob(function (b) {
				if (b && b.type === type) { res(b); return; }
				if (type !== 'image/jpeg') { cv.toBlob(function (b2) { res(b2); }, 'image/jpeg', q); return; } // Safari has no WebP encoder
				res(b);
			}, type, q);
		});
	}
	function shrink(f) {
		return decode(f).then(function (src) {
			var w = src.width || src.naturalWidth, h = src.height || src.naturalHeight;
			if (!w || !h) { throw new Error(T.bad); }
			var k = Math.min(1, L.long / Math.max(w, h)), cv = document.createElement('canvas');
			cv.width = Math.max(1, Math.round(w * k)); cv.height = Math.max(1, Math.round(h * k));
			var cx = cv.getContext('2d');
			cx.fillStyle = '#FFFFFF'; cx.fillRect(0, 0, cv.width, cv.height);
			cx.drawImage(src, 0, 0, cv.width, cv.height);
			if (src.close) { src.close(); }
			return toBlob(cv, C.webp ? 'image/webp' : 'image/jpeg', 0.85);
		}).then(function (b) { if (!b) { throw new Error(T.bad); } return b; });
	}

	/* ---------------- the composer (board 21 part א) ---------------- */
	var dragEnded = false;
	function composer(form, ctx) {
		var max = ctx === 'reply' ? L.reply : L.topic;
		var items = [], sel = null, seq = 0, active = 0, pin = null, waiters = [], sayT = 0, sending = false;
		var list = el('div', { cls: 'nlfmd-thumbs', role: 'list', 'aria-label': T.list, hidden: true });
		var addB = el('button', { type: 'button', cls: 'nlfmd-th-add', 'aria-label': T.moreAria }, el('span', { 'aria-hidden': 'true', text: '+' }), el('span', { 'aria-hidden': 'true', text: T.more }));
		var cap = el('input', { type: 'text', cls: 'nlfmd-cap', maxlength: L.caption, autocomplete: 'off', hidden: true });
		var chipGps = el('span', { cls: 'nlfmd-chip nlfmd-chip-ok', text: T.gps, hidden: true });
		var chipDrag = el('span', { cls: 'nlfmd-chip', text: T.drag, hidden: true });
		var inCam = el('input', { type: 'file', accept: 'image/*', capture: 'environment', hidden: true, tabindex: '-1', 'aria-hidden': 'true' });
		var inPics = el('input', { type: 'file', accept: 'image/*', multiple: true, hidden: true, tabindex: '-1', 'aria-hidden': 'true' });
		var inPdf = el('input', { type: 'file', accept: 'application/pdf,.pdf', multiple: true, hidden: true, tabindex: '-1', 'aria-hidden': 'true' });
		var bCam = el('button', { type: 'button', cls: 'nlfmd-pick', text: T.cam });
		var bPics = el('button', { type: 'button', cls: 'nlfmd-pick', text: T.pics });
		var bPdf = el('button', { type: 'button', cls: 'nlfmd-pick nlfmd-pick-wide', text: T.pdf });
		var msg = el('p', { cls: 'nlfmd-status', role: 'status', 'aria-live': 'polite' });
		var enterB = el('button', { type: 'button', cls: 'nlf-link nlfmd-enter', 'data-nlf-enter': true, text: T.enterBtn, hidden: true });
		var limits = el('p', { cls: 'nlfmd-limits', text: C.text[ctx] || '' });
		var over = el('div', { cls: 'nlfmd-over', hidden: true, 'aria-hidden': 'true' }, el('span', { text: T.drop }));
		var pinBox = null, pinCv = null;
		if (ctx === 'reply') {
			pinCv = el('canvas', { width: 120, height: 90, 'aria-hidden': 'true' });
			var unpin = el('button', { type: 'button', cls: 'nlf-link', text: T.unpin });
			pinBox = el('div', { cls: 'nlfmd-pinbox', hidden: true }, pinCv, el('span', { cls: 'nlfmd-pinbox-t', text: T.pinT }), unpin);
			unpin.addEventListener('click', function () { setPin(null); });
		}
		var box = el('div', { cls: 'nlfmd-comp' }, pinBox, list, cap, el('div', { cls: 'nlfmd-chips' }, chipGps, chipDrag),
			el('div', { cls: 'nlfmd-picks' }, bCam, bPics, bPdf), el('div', { cls: 'nlfmd-msgrow' }, msg, enterB), inCam, inPics, inPdf);
		var sub = ctx === 'reply' ? null : form.querySelector(':scope > button[type="submit"]');
		var row = ctx === 'reply' ? form.querySelector('.nlf-replyrow') : null;
		if (row) { row.parentNode.insertBefore(box, row.nextSibling); box.appendChild(limits); }
		else if (sub) { form.insertBefore(box, sub); sub.parentNode.insertBefore(limits, sub.nextSibling); }
		else { form.appendChild(box); box.appendChild(limits); }
		form.classList.add('nlfmd-dropzone');
		form.appendChild(over);

		function say(t, err, entry) {
			msg.textContent = t || '';
			msg.classList.toggle('is-err', !!err);
			enterB.hidden = !entry;
		}
		function busy() { return items.some(function (it) { return it.state === 'wait' || it.state === 'prep' || it.state === 'up'; }); }
		function failed() { return items.some(function (it) { return it.state === 'err'; }); }
		function settle() {
			if (busy()) { return; }
			var w = waiters; waiters = [];
			w.forEach(function (f) { f(); });
		}
		function idle() { return busy() ? new Promise(function (r) { waiters.push(r); }) : Promise.resolve(); }
		function needEntry() { say(T.enter, true, true); }
		function canPick() {
			if (st.loaded && !st.member) { needEntry(); return false; }
			return true;
		}
		function progress() {
			var up = items.filter(function (it) { return it.state === 'wait' || it.state === 'prep' || it.state === 'up'; });
			if (!up.length) { return; }
			var now = Date.now();
			if (now - sayT < 700) { return; }
			sayT = now;
			var p = Math.round(up.reduce(function (s, it) { return s + it.pct; }, 0) / up.length);
			say(T.up(up.length, p));
		}

		/* the thumbs */
		function thumb(it) {
			var face = it.kind === 'pdf' ? el('span', { cls: 'nlfmd-th-pdf', text: 'PDF' }) : el('img', { alt: '', width: 84, height: 84 });
			var num = el('span', { cls: 'nlfmd-th-n', 'aria-hidden': 'true' });
			var bar = el('i');
			var pct = el('span', { cls: 'nlfmd-th-pct', 'aria-hidden': 'true' });
			var b = el('button', { type: 'button', cls: 'nlfmd-th-sel' }, face, num, el('span', { cls: 'nlfmd-th-bar', 'aria-hidden': 'true' }, bar), pct);
			var x = el('button', { type: 'button', cls: 'nlfmd-th-x', text: '×' });
			var n = el('div', { cls: 'nlfmd-th', role: 'listitem' }, b, x);
			it.node = n; it.parts = { face: face, num: num, bar: bar, pct: pct, b: b, x: x };
			b.addEventListener('click', function () { if (dragEnded) { return; } sel = it; paint(); cap.focus(); });
			x.addEventListener('click', function () { remove(it); });
			b.addEventListener('keydown', function (e) {
				if (!e.altKey) { return; }
				var d = e.key === 'ArrowLeft' ? 1 : (e.key === 'ArrowRight' ? -1 : 0); // right to left: the next place is on the left
				if (!d) { return; }
				e.preventDefault();
				var to = items.indexOf(it) + d;
				if (to < 0 || to >= items.length) { return; }
				move(it, to); say(T.moved(to + 1)); b.focus();
			});
			dragInit(n, b, it);
			return n;
		}
		function fill(it, i) {
			var p = it.parts, up = it.state === 'wait' || it.state === 'prep' || it.state === 'up';
			p.num.textContent = String(i + 1);
			if (it.kind === 'image' && it.url && p.face.getAttribute('src') !== it.url) { p.face.setAttribute('src', it.url); }
			it.node.classList.toggle('is-up', up);
			it.node.classList.toggle('is-err', it.state === 'err');
			it.node.classList.toggle('is-sel', it === sel);
			p.bar.style.width = (up ? it.pct : 0) + '%';
			p.pct.textContent = it.state === 'err' ? T.errShort : (up ? it.pct + '%' : '');
			p.b.setAttribute('aria-label', T.item(i + 1, it.kind === 'pdf') + (it.caption ? ': ' + it.caption : '') + (it.state === 'err' ? ', ' + T.errShort : (up ? ', ' + it.pct + '%' : '')) + '. ' + T.itemHint);
			p.b.setAttribute('aria-pressed', it === sel ? 'true' : 'false');
			p.x.setAttribute('aria-label', T.remove(i + 1));
		}
		function paint() {
			var kids = [];
			items.forEach(function (it, i) { if (!it.node) { thumb(it); } fill(it, i); kids.push(it.node); });
			if (items.length && items.length < max) { kids.push(addB); }
			list.replaceChildren.apply(list, kids);
			list.hidden = !items.length;
			chipDrag.hidden = items.length < 2;
			chipGps.hidden = !items.some(function (it) { return it.kind === 'image' && it.blob; });
			if (sel && items.indexOf(sel) < 0) { sel = null; }
			cap.hidden = !sel;
			if (sel) {
				cap.value = sel.caption;
				cap.placeholder = sel.kind === 'pdf' ? T.capPdf : T.cap;
				cap.setAttribute('aria-label', T.capFor(items.indexOf(sel) + 1));
			}
		}
		function move(it, to) {
			var from = items.indexOf(it);
			if (from < 0) { return; }
			items.splice(from, 1);
			items.splice(Math.max(0, Math.min(items.length, to)), 0, it);
			paint();
		}
		function nearest(x, y, it) {
			var best = -1, bd = Infinity;
			items.forEach(function (o, i) {
				var r = o.node.getBoundingClientRect(), d = Math.hypot(r.left + r.width / 2 - x, r.top + r.height / 2 - y);
				if (d < bd) { bd = d; best = i; }
			});
			return bd < 80 ? best : -1;
		}
		/* drag to reorder: pointer events, after 8px of movement; the thumb has touch-action pan-y, so a vertical swipe still scrolls */
		function dragInit(n, b, it) {
			var sx = 0, sy = 0, pid = null, on = false;
			b.addEventListener('pointerdown', function (e) { if (e.button !== 0 || items.length < 2) { return; } sx = e.clientX; sy = e.clientY; pid = e.pointerId; on = false; });
			b.addEventListener('pointermove', function (e) {
				if (pid !== e.pointerId) { return; }
				var dx = e.clientX - sx, dy = e.clientY - sy;
				if (!on) {
					if (Math.abs(dx) + Math.abs(dy) < 8) { return; }
					on = true;
					try { b.setPointerCapture(pid); } catch (x) { /* an old browser */ }
					n.classList.add('is-drag');
				}
				n.style.transform = 'translate(' + dx + 'px,' + dy + 'px)';
				e.preventDefault();
			});
			function stop(e, keep) {
				if (pid !== e.pointerId) { return; }
				pid = null;
				if (!on) { return; }
				on = false;
				n.classList.remove('is-drag'); n.style.transform = '';
				dragEnded = true; setTimeout(function () { dragEnded = false; }, 0);
				if (!keep) { return; }
				var to = nearest(e.clientX, e.clientY, it);
				if (to > -1 && to !== items.indexOf(it)) { move(it, to); say(T.moved(to + 1)); }
			}
			b.addEventListener('pointerup', function (e) { stop(e, true); });
			b.addEventListener('pointercancel', function (e) { stop(e, false); });
		}

		/* adding, preparing, sending, removing */
		function isPdf(f) { return f.type === 'application/pdf' || /\.pdf$/i.test(f.name || ''); }
		function isImg(f) { return /^image\//.test(f.type || '') || /\.(jpe?g|png|webp|gif|heic|heif)$/i.test(f.name || ''); }
		function take(files, onlyPdf) {
			if (!canPick()) { return; }
			var arr = Array.prototype.slice.call(files || []), added = 0, full = false, err = '';
			arr.forEach(function (f) {
				if (items.length >= max) { full = true; return; }
				var pdf = isPdf(f), img = !pdf && isImg(f);
				if (onlyPdf && !pdf) { err = T.notPdf; return; }
				if (!pdf && !img) { err = T.kind; return; }
				if (pdf && f.size > L.pdf) { err = T.bigPdf; return; }
				if (img && f.size > L.img) { err = T.big; return; }
				var it = { key: ++seq, kind: pdf ? 'pdf' : 'image', file: f, caption: '', pct: 0, state: 'wait' };
				items.push(it); sel = it; added++;
			});
			if (full) { err = T.max(max); }
			if (err) { say(err, true); } else if (added) { say(''); }
			if (added) { paint(); pump(); }
		}
		function pump() {
			while (active < 2) {
				var it = null;
				for (var i = 0; i < items.length; i++) { if (items[i].state === 'wait') { it = items[i]; break; } }
				if (!it) { break; }
				active++;
				run(it).then(function () { active--; pump(); settle(); });
			}
			settle();
		}
		function gone(it) { return items.indexOf(it) < 0; }
		function run(it) {
			it.state = 'prep'; paint();
			return state().then(function () {
				if (!st.member) { var e = new Error(T.enter); e.code = 'nlf_need_entry'; throw e; }
				if (it.kind === 'pdf') { it.blob = it.file; return; }
				return shrink(it.file).then(function (b) { it.blob = b; it.url = URL.createObjectURL(b); });
			}).then(function () {
				if (gone(it)) { var e = new Error(''); e.code = 'abort'; throw e; }
				it.state = 'up'; paint();
				var fd = new FormData();
				fd.append('kind', 'post');
				fd.append('file', it.blob, it.kind === 'pdf' ? 'plan.pdf' : (it.blob.type === 'image/webp' ? 'image.webp' : 'image.jpg'));
				return send('POST', 'media', fd, function (f) { it.pct = Math.min(99, Math.round(f * 100)); fill(it, items.indexOf(it)); progress(); }, it);
			}).then(function (j) {
				it.media = j.media; it.id = j.media.id; it.pct = 100; it.state = 'done';
				if (gone(it)) { send('DELETE', 'media/' + it.id).catch(function () {}); return; }
				paint();
				if (!busy()) { say(failed() ? T.upFail : T.upDone, failed()); }
			}).catch(function (er) {
				if (er.code === 'abort' || gone(it)) { return; }
				it.state = 'err'; paint();
				say(er.message || ERR, true, er.code === 'nlf_need_entry');
			});
		}
		function remove(it) {
			var i = items.indexOf(it);
			if (i < 0) { return; }
			items.splice(i, 1);
			if (it.state === 'up' && it.xhr) { it.xhr.abort(); }
			if (it.id) { send('DELETE', 'media/' + it.id).catch(function () {}); }
			if (it.url) { URL.revokeObjectURL(it.url); }
			if (sel === it) { sel = items[Math.min(i, items.length - 1)] || null; }
			paint();
			say(T.removed(i + 1));
			var next = items[Math.min(i, items.length - 1)];
			(next ? next.parts.b : bPics).focus();
			settle();
		}

		/* the point an answer asks about: a small crop with the raspberry marker (board 21 part ג) */
		function setPin(p) {
			pin = p;
			if (!pinBox) { return; }
			pinBox.hidden = !p;
			if (!p) { return; }
			var im = new Image();
			im.onload = function () {
				var iw = im.naturalWidth, ih = im.naturalHeight, W = 120, H = Math.max(60, Math.min(150, Math.round(W * ih / iw)));
				var dpr = Math.min(2, window.devicePixelRatio || 1), rw = iw / 3, rh = rw * H / W;
				var sx = Math.max(0, Math.min(iw - rw, p.x * iw - rw / 2)), sy = Math.max(0, Math.min(ih - rh, p.y * ih - rh / 2));
				pinCv.width = W * dpr; pinCv.height = H * dpr; pinCv.style.width = W + 'px'; pinCv.style.height = H + 'px';
				var c = pinCv.getContext('2d');
				c.setTransform(dpr, 0, 0, dpr, 0, 0);
				c.drawImage(im, sx, sy, rw, rh, 0, 0, W, H);
				var mx = (p.x * iw - sx) / rw * W, my = (p.y * ih - sy) / rh * H;
				c.beginPath(); c.arc(mx, my, 9, 0, Math.PI * 2); c.fillStyle = '#B0144F'; c.fill(); c.lineWidth = 3; c.strokeStyle = '#FFFFFF'; c.stroke();
			};
			im.src = p.src;
			say(T.pinOn);
		}

		bCam.addEventListener('click', function () { if (canPick()) { inCam.click(); } });
		bPics.addEventListener('click', function () { if (canPick()) { inPics.click(); } });
		addB.addEventListener('click', function () { if (canPick()) { inPics.click(); } });
		bPdf.addEventListener('click', function () { if (canPick()) { inPdf.click(); } });
		[inCam, inPics].forEach(function (inp) { inp.addEventListener('change', function () { var f = inp.files; take(f, false); inp.value = ''; }); });
		inPdf.addEventListener('change', function () { take(inPdf.files, true); inPdf.value = ''; });
		cap.addEventListener('input', function () { if (sel) { sel.caption = cap.value.slice(0, L.caption); fill(sel, items.indexOf(sel)); } });
		/* drag and drop on the whole form, and paste from the clipboard */
		function hasFiles(e) { var t = e.dataTransfer && e.dataTransfer.types; return !!t && Array.prototype.indexOf.call(t, 'Files') > -1; }
		form.addEventListener('dragover', function (e) { if (!hasFiles(e)) { return; } e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; over.hidden = false; });
		form.addEventListener('dragleave', function (e) { if (!e.relatedTarget || !form.contains(e.relatedTarget)) { over.hidden = true; } });
		form.addEventListener('drop', function (e) { if (!hasFiles(e)) { return; } e.preventDefault(); over.hidden = true; take(e.dataTransfer.files, false); });
		form.addEventListener('paste', function (e) {
			var cd = e.clipboardData, fs = cd && cd.files ? Array.prototype.slice.call(cd.files).filter(function (f) { return isImg(f) || isPdf(f); }) : [];
			if (!fs.length) { return; }
			if (!cd.getData('text/plain')) { e.preventDefault(); }
			take(fs, false);
		});
		/* after an answer is sent forum.js resets the form: its files go into the new answer on the page, the composer empties */
		form.addEventListener('reset', function () {
			if (ctx !== 'reply') { return; }
			var done = items.filter(function (it) { return it.state === 'done' && it.media; });
			var art = $('#nlf-replies > .nlf-reply:last-child');
			if (done.length && art && !art.querySelector('.nlfmd-media')) {
				var who = art.querySelector('.nlf-who');
				art.appendChild(localMedia(done, who ? who.textContent.split(' · ')[0] : ''));
			}
			items.forEach(function (it) { if (done.indexOf(it) < 0 && it.url) { URL.revokeObjectURL(it.url); } });
			items = []; sel = null; setPin(null); paint(); say('');
		});
		form.nlfExtra = function (path) {
			if (path !== (ctx === 'reply' ? 'reply' : 'topic')) { return null; }
			var o = {}, media = items.filter(function (it) { return it.state === 'done' && it.id; }).map(function (it) { return { id: it.id, caption: it.caption }; });
			if (media.length) { o.media = media; }
			if (pin) { o.pin = { media: pin.media, x: pin.x, y: pin.y }; }
			return o;
		};
		form.__nlfmd = {
			busy: busy, failed: failed, idle: idle, say: say, setPin: setPin,
			get sending() { return sending; }, set sending(v) { sending = !!v; }
		};
	}
	/* a post waits until every file is up (the forum's own submit handler runs only after this one lets it through) */
	document.addEventListener('submit', function (e) {
		var f = e.target, c = f && f.__nlfmd;
		if (!c) { return; }
		if (c.busy()) {
			e.preventDefault(); e.stopImmediatePropagation();
			c.say(T.wait);
			if (c.sending) { return; }
			c.sending = true;
			c.idle().then(function () {
				c.sending = false;
				if (c.failed()) { c.say(T.upFail, true); return; }
				if (f.requestSubmit) { f.requestSubmit(); } else { f.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true })); }
			});
			return;
		}
		if (c.failed()) { e.preventDefault(); e.stopImmediatePropagation(); c.say(T.upFail, true); }
	}, true);

	/* the files of an answer just sent, drawn as the server draws them */
	function localMedia(done, by) {
		var wrap = el('div', { cls: 'nlfmd-media' });
		var imgs = done.filter(function (it) { return it.kind === 'image'; }), pdfs = done.filter(function (it) { return it.kind === 'pdf'; });
		if (imgs.length) {
			var n = imgs.length, lay = n === 1 ? 'one' : (n === 2 ? 'two' : 'three'), more = Math.max(0, n - 3);
			var g = el('div', { cls: 'nlfmd-gal nlfmd-gal-' + lay, 'data-nlfmd-gal': true, 'data-by': by, 'data-at': 'עכשיו' });
			imgs.forEach(function (it, i) {
				var m = it.media, x = i === 2 && more > 0;
				var a = el('a', { cls: 'nlfmd-tile' + (x ? ' is-more' : ''), href: m.url, 'data-nlfmd-id': m.id, 'data-w': m.w, 'data-h': m.h, 'data-cap': it.caption,
					'aria-label': 'פתיחת תמונה ' + (i + 1) + ' מתוך ' + n + ' במסך מלא', hidden: i >= 3 },
					el('img', { src: m.thumb || m.url, alt: it.caption || T.alt, width: m.w, height: m.h, decoding: 'async' }));
				if (x) { a.appendChild(el('span', { cls: 'nlfmd-plus', 'aria-hidden': 'true', text: '+' + more })); }
				g.appendChild(a);
			});
			wrap.appendChild(g);
		}
		pdfs.forEach(function (it) {
			var m = it.media;
			wrap.appendChild(el('div', { cls: 'nlfmd-pdf' },
				el('a', { cls: 'nlfmd-pdf-card', href: m.url, target: '_blank', rel: 'noopener' }, el('span', { cls: 'nlfmd-pdf-th', 'aria-hidden': 'true' }),
					el('span', { cls: 'nlfmd-pdf-tx' }, el('b', { text: it.caption || 'קובץ PDF' }), el('span', { text: m.meta || 'PDF' }))),
				el('div', { cls: 'nlfmd-pdf-acts' }, el('a', { cls: 'nlfmd-btn nlfmd-btn-line', href: m.url, download: true, text: 'הורדה' }))));
		});
		return wrap;
	}

	var cf = $('[data-nlf-composeform]'), rf = $('[data-nlf-replyform]');
	if (cf) { composer(cf, 'topic'); }
	if (rf) { composer(rf, 'reply'); }

	/* ---------------- the full-screen view (board 21 part ג) ---------------- */
	var PINS = [];
	try { var pj = $('#nlfmd-pins'); PINS = pj ? JSON.parse(pj.textContent || '[]') : []; } catch (e) { PINS = []; }
	var LB = null;
	function lightbox() {
		if (LB) { return LB; }
		var S = { set: [], i: 0, mark: false, pt: null, ret: null, hot: 0 };
		var d = el('dialog', { cls: 'nlfmd-lb', dir: 'rtl', lang: 'he', 'aria-label': T.lb });
		var x = el('button', { type: 'button', cls: 'nlfmd-lb-x', 'aria-label': T.close }, svg('M6 6l12 12M18 6L6 18'));
		var count = el('span', { cls: 'nlfmd-lb-count' });
		var who = el('span', { cls: 'nlfmd-lb-who' });
		var img = el('img', { cls: 'nlfmd-lb-img', alt: '', decoding: 'async' });
		var pins = el('div', { cls: 'nlfmd-lb-pins' });
		var dot = el('span', { cls: 'nlfmd-lb-mark', hidden: true, 'aria-hidden': 'true' });
		var fit = el('div', { cls: 'nlfmd-lb-fit' }, img, pins, dot);
		var prev = el('button', { type: 'button', cls: 'nlfmd-lb-nav nlfmd-lb-prev', 'aria-label': T.prev }, svg('M9 5l7 7-7 7'));
		var next = el('button', { type: 'button', cls: 'nlfmd-lb-nav nlfmd-lb-next', 'aria-label': T.next }, svg('M15 5l-7 7 7 7'));
		var stage = el('div', { cls: 'nlfmd-lb-stage' }, fit, prev, next);
		var capP = el('p', { cls: 'nlfmd-lb-cap' });
		var dots = el('div', { cls: 'nlfmd-lb-dots', 'aria-hidden': 'true' });
		var ask = el('button', { type: 'button', cls: 'nlfmd-lb-ask', text: T.mark });
		var video = el('button', { type: 'button', cls: 'nlfmd-lb-video', text: T.video });
		var acts = el('div', { cls: 'nlfmd-lb-acts' }, ask, video);
		var go = el('button', { type: 'button', cls: 'nlfmd-lb-ask', text: T.markGo, disabled: true });
		var cancel = el('button', { type: 'button', cls: 'nlfmd-lb-video', text: T.markCancel });
		var markbar = el('div', { cls: 'nlfmd-lb-markbar', hidden: true }, el('p', { cls: 'nlfmd-lb-hint', text: T.markHint }), el('div', { cls: 'nlfmd-lb-acts' }, go, cancel));
		var live = el('p', { cls: 'nlfmd-sr', 'aria-live': 'polite' });
		d.appendChild(el('div', { cls: 'nlfmd-lb-top' }, x, count, who));
		[stage, capP, dots, acts, markbar, live].forEach(function (n) { d.appendChild(n); });
		document.body.appendChild(d);
		if (C.rooms && C.topic) { video.setAttribute('data-nlf-room', String(C.topic)); } else { video.hidden = true; }

		function layout() {
			var it = S.set[S.i];
			if (!it) { return; }
			var r = stage.getBoundingClientRect(), k = Math.min(r.width / it.w, r.height / it.h);
			if (!isFinite(k) || k <= 0) { return; }
			fit.style.width = Math.floor(it.w * k) + 'px'; fit.style.height = Math.floor(it.h * k) + 'px';
		}
		function paintPins(it) {
			var kids = [];
			PINS.forEach(function (p) {
				if ((p.m | 0) !== it.id) { return; }
				var b = el('button', { type: 'button', cls: 'nlfmd-lb-pin' + ((p.r | 0) === S.hot ? ' is-on' : ''), 'aria-label': T.pinOf(p.n) });
				b.style.left = (p.x * 100) + '%'; b.style.top = (p.y * 100) + '%';
				b.addEventListener('click', function (e) {
					e.stopPropagation();
					d.close();
					var r = document.getElementById('r' + (p.r | 0));
					if (r) { r.setAttribute('tabindex', '-1'); r.scrollIntoView({ block: 'start' }); r.focus({ preventScroll: true }); }
				});
				kids.push(b);
			});
			pins.replaceChildren.apply(pins, kids);
		}
		function show(i) {
			var n = S.set.length;
			S.i = ((i % n) + n) % n;
			var it = S.set[S.i];
			markOff();
			img.src = it.full; img.alt = it.cap || T.alt;
			count.textContent = (S.i + 1) + ' / ' + n;
			who.textContent = [it.by, it.at].filter(Boolean).join(' · ');
			capP.textContent = it.cap; capP.hidden = !it.cap;
			var ds = [];
			for (var k = 0; k < n; k++) { ds.push(el('i', { cls: k === S.i ? 'is-on' : '' })); }
			dots.replaceChildren.apply(dots, ds);
			dots.hidden = n < 2; prev.hidden = n < 2; next.hidden = n < 2;
			paintPins(it);
			live.textContent = 'תמונה ' + (S.i + 1) + ' מתוך ' + n + (it.cap ? ': ' + it.cap : '');
			requestAnimationFrame(layout);
			[1, -1].forEach(function (o) { var j = S.set[((S.i + o) % n + n) % n]; if (j && j !== it) { var p = new Image(); p.src = j.full; } });
		}
		function markOn() {
			S.mark = true; S.pt = null; d.classList.add('is-marking');
			acts.hidden = true; markbar.hidden = false; go.disabled = true; dot.hidden = true;
			live.textContent = T.markHint;
			stage.focus();
		}
		function markOff() {
			S.mark = false; S.pt = null; d.classList.remove('is-marking');
			acts.hidden = false; markbar.hidden = true; dot.hidden = true;
		}
		function place(px, py) {
			S.pt = { x: Math.max(0, Math.min(1, px)), y: Math.max(0, Math.min(1, py)) };
			dot.style.left = (S.pt.x * 100) + '%'; dot.style.top = (S.pt.y * 100) + '%';
			dot.hidden = false; go.disabled = false;
		}
		stage.setAttribute('tabindex', '-1');
		/* swipe (right to left: a swipe to the right shows the next picture), a tap to mark */
		var sw = null;
		stage.addEventListener('pointerdown', function (e) { if (e.isPrimary) { sw = { x: e.clientX, y: e.clientY, t: Date.now() }; } });
		stage.addEventListener('pointerup', function (e) {
			if (!sw || !e.isPrimary) { return; }
			var dx = e.clientX - sw.x, dy = e.clientY - sw.y; sw = null;
			if (S.mark) {
				if (Math.abs(dx) + Math.abs(dy) > 12) { return; }
				var r = fit.getBoundingClientRect();
				if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) { return; }
				place((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height);
				return;
			}
			if (S.set.length > 1 && Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.3) { show(S.i + (dx > 0 ? 1 : -1)); }
		});
		stage.addEventListener('pointercancel', function () { sw = null; });
		d.addEventListener('keydown', function (e) {
			if (S.mark && /^Arrow/.test(e.key)) {
				e.preventDefault();
				var p = S.pt || { x: 0.5, y: 0.5 }, s = e.shiftKey ? 0.1 : 0.02;
				if (!S.pt) { place(0.5, 0.5); return; }
				place(p.x + (e.key === 'ArrowRight' ? s : (e.key === 'ArrowLeft' ? -s : 0)), p.y + (e.key === 'ArrowDown' ? s : (e.key === 'ArrowUp' ? -s : 0)));
				return;
			}
			if (S.mark && e.key === 'Enter' && S.pt && document.activeElement === stage) { e.preventDefault(); go.click(); return; }
			if (e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) { return; }
			if (e.key === 'ArrowLeft') { e.preventDefault(); show(S.i + 1); }
			if (e.key === 'ArrowRight') { e.preventDefault(); show(S.i - 1); }
		});
		d.addEventListener('cancel', function (e) { if (S.mark) { e.preventDefault(); markOff(); ask.focus(); } }); // Escape leaves the marking first
		d.addEventListener('close', function () {
			markOff(); img.removeAttribute('src');
			document.documentElement.classList.remove('nlfmd-lock');
			if (S.ret && S.ret.focus && document.contains(S.ret)) { S.ret.focus({ preventScroll: true }); }
		});
		d.addEventListener('click', function (e) { if (e.target === d) { d.close(); } });
		x.addEventListener('click', function () { d.close(); });
		prev.addEventListener('click', function () { show(S.i - 1); });
		next.addEventListener('click', function () { show(S.i + 1); });
		ask.addEventListener('click', markOn);
		cancel.addEventListener('click', function () { markOff(); ask.focus(); });
		go.addEventListener('click', function () {
			var it = S.set[S.i], f = $('[data-nlf-replyform]'), c = f && f.__nlfmd;
			if (!it || !S.pt || !c) { return; }
			var pt = S.pt;
			S.ret = null;
			d.close();
			c.setPin({ media: it.id, x: Math.round(pt.x * 10000) / 10000, y: Math.round(pt.y * 10000) / 10000, src: it.thumb || it.full });
			f.scrollIntoView({ block: 'center' });
			if (f.elements.body) { f.elements.body.focus({ preventScroll: true }); }
		});
		/* the discussion's video room opens (call.js, data-nlf-room); this picture becomes its board's sheet */
		video.addEventListener('click', function () { var it = S.set[S.i]; if (it) { toBoard(it.full); } S.ret = null; d.close(); });
		window.addEventListener('resize', function () { if (d.open) { requestAnimationFrame(layout); } });
		LB = {
			open: function (set, i, opener, hot) {
				S.set = set; S.ret = opener || null; S.hot = hot | 0;
				ask.hidden = !(C.topic && $('[data-nlf-replyform]') && $('[data-nlf-replyform]').__nlfmd);
				if (d.showModal) { if (!d.open) { d.showModal(); } } else { d.setAttribute('open', ''); }
				document.documentElement.classList.add('nlfmd-lock');
				show(i);
				x.focus();
			}
		};
		return LB;
	}
	function toBoard(src) {
		try { sessionStorage.setItem(BKEY, JSON.stringify({ src: src, topic: C.topic | 0, t: Date.now() })); } catch (e) { /* private mode: the room opens with a blank board */ }
	}
	function openFrom(tile, opener, hot) {
		var g = tile.closest('[data-nlfmd-gal]');
		if (!g) { return; }
		var tiles = $$('a.nlfmd-tile', g);
		var set = tiles.map(function (t) {
			var im = t.querySelector('img');
			return { id: +t.getAttribute('data-nlfmd-id'), full: t.getAttribute('href'), thumb: im ? im.getAttribute('src') : '', w: +t.getAttribute('data-w') || 1, h: +t.getAttribute('data-h') || 1,
				cap: t.getAttribute('data-cap') || '', by: g.getAttribute('data-by') || '', at: g.getAttribute('data-at') || '' };
		});
		lightbox().open(set, Math.max(0, tiles.indexOf(tile)), opener, hot);
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest && e.target.closest('[data-nlfmd-board]');
		if (b) { toBoard(b.getAttribute('data-nlfmd-board')); } // then call.js opens the room (data-nlf-room on the same button)
	}, true);
	document.addEventListener('click', function (e) {
		var a = e.target.closest && e.target.closest('a.nlfmd-tile, [data-nlfmd-open]');
		if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
		e.preventDefault();
		if (a.hasAttribute('data-nlfmd-open')) {
			var t = $('a.nlfmd-tile[data-nlfmd-id="' + (+a.getAttribute('data-nlfmd-open') | 0) + '"]');
			if (t) { openFrom(t, a, +a.getAttribute('data-nlfmd-pin')); }
			return;
		}
		openFrom(a, a, 0);
	});
	/* call.js made the board of a room: a picture or plan pressed a moment ago becomes its sheet, and the board opens */
	document.addEventListener('nlf:board', function (e) {
		var bd = e.detail, p = null;
		try { p = JSON.parse(sessionStorage.getItem(BKEY) || 'null'); sessionStorage.removeItem(BKEY); } catch (x) { p = null; }
		if (!bd || typeof bd.takeImage !== 'function' || !p || !p.src || Date.now() - p.t > 5 * 60000 || (p.topic | 0) !== (C.topic | 0)) { return; }
		fetch(p.src, { credentials: 'same-origin' }).then(function (r) { return r.ok ? r.blob() : null; }).then(function (bl) {
			if (!bl) { return null; }
			return Promise.resolve(bd.takeImage(bl)).then(function () { bd.open(); });
		}).catch(function () { /* the board stays blank; its own "העלאת תוכנית" still works */ });
	});

	/* ---------------- the member's picture (board 21 part ד) ---------------- */
	var av = $('#nlfmd-avatar');
	if (av) {
		var stage = $('[data-nlfmd-stage]', av), cv = $('canvas', stage), zoom = $('[data-nlfmd-zoom]', av), file = $('[data-nlfmd-avfile]', av);
		var save = $('[data-nlfmd-avsave]', av), rm = $('[data-nlfmd-avremove]', av), msg = $('.nlf-msg', av), empty = $('.nlfmd-stage-empty', av), meAv = $('[data-nlfmd-avme]', av);
		var A = { src: null, w: 0, h: 0, ox: 0, oy: 0, z: 1, drag: null };
		var SZ = 224, D = 200, dpr = Math.min(2, window.devicePixelRatio || 1);
		cv.width = SZ * dpr; cv.height = SZ * dpr;
		var say = function (t, err) { msg.textContent = t || ''; msg.classList.toggle('is-err', !!err); };
		var base = function () { return D / Math.min(A.w, A.h); };
		var clampO = function () {
			var s = base() * A.z, mx = Math.max(0, (A.w * s - D) / 2), my = Math.max(0, (A.h * s - D) / 2);
			A.ox = Math.max(-mx, Math.min(mx, A.ox)); A.oy = Math.max(-my, Math.min(my, A.oy));
		};
		var draw = function () {
			var c = cv.getContext('2d');
			c.setTransform(dpr, 0, 0, dpr, 0, 0);
			c.fillStyle = '#0B1117'; c.fillRect(0, 0, SZ, SZ);
			if (!A.src) { return; }
			var s = base() * A.z;
			c.drawImage(A.src, SZ / 2 + A.ox - A.w * s / 2, SZ / 2 + A.oy - A.h * s / 2, A.w * s, A.h * s);
		};
		draw();
		document.addEventListener('click', function (e) {
			var b = e.target.closest && e.target.closest('[data-nlfmd-avatar]');
			if (!b) { return; }
			av._ret = b;
			say('');
			if (av.showModal) { if (!av.open) { av.showModal(); } } else { av.setAttribute('open', ''); }
			setTimeout(function () { (A.src ? stage : $('[data-nlfmd-avpick]', av)).focus(); }, 30);
		});
		$$('[data-nlfmd-avpick]', av).forEach(function (b) { b.addEventListener('click', function () { file.click(); }); });
		file.addEventListener('change', function () {
			var f = file.files && file.files[0];
			file.value = '';
			if (!f) { return; }
			if (f.size > L.img) { say(T.big, true); return; }
			decode(f).then(function (src) {
				A.src = src; A.w = src.width || src.naturalWidth; A.h = src.height || src.naturalHeight; A.z = 1; A.ox = 0; A.oy = 0;
				if (!A.w || !A.h) { throw new Error(T.bad); }
				zoom.disabled = false; zoom.value = '100'; save.disabled = false; empty.hidden = true;
				draw(); say(''); stage.focus();
			}).catch(function () { say(T.bad, true); });
		});
		zoom.addEventListener('input', function () { A.z = (+zoom.value || 100) / 100; clampO(); draw(); });
		stage.addEventListener('pointerdown', function (e) {
			if (!A.src || e.target !== cv && e.target !== stage && !e.target.classList.contains('nlfmd-ring')) { return; }
			A.drag = { id: e.pointerId, x: e.clientX, y: e.clientY };
			try { stage.setPointerCapture(e.pointerId); } catch (x) { /* an old browser */ }
		});
		stage.addEventListener('pointermove', function (e) {
			if (!A.drag || A.drag.id !== e.pointerId) { return; }
			A.ox += e.clientX - A.drag.x; A.oy += e.clientY - A.drag.y; A.drag.x = e.clientX; A.drag.y = e.clientY;
			clampO(); draw();
		});
		['pointerup', 'pointercancel'].forEach(function (t) { stage.addEventListener(t, function () { A.drag = null; }); });
		stage.addEventListener('keydown', function (e) {
			if (!A.src) { return; }
			var k = e.key, s = e.shiftKey ? 20 : 6;
			if (k === 'ArrowLeft') { A.ox -= s; } else if (k === 'ArrowRight') { A.ox += s; } else if (k === 'ArrowUp') { A.oy -= s; } else if (k === 'ArrowDown') { A.oy += s; }
			else if (k === '+' || k === '=') { zoom.value = String(Math.min(400, +zoom.value + 10)); A.z = +zoom.value / 100; }
			else if (k === '-') { zoom.value = String(Math.max(100, +zoom.value - 10)); A.z = +zoom.value / 100; }
			else { return; }
			e.preventDefault(); clampO(); draw();
		});
		save.addEventListener('click', function () {
			if (!A.src) { say(T.avPick, true); return; }
			var s = base() * A.z, side = D / s, cx = A.w / 2 - A.ox / s, cy = A.h / 2 - A.oy / s, out = document.createElement('canvas');
			out.width = L.avatar; out.height = L.avatar;
			var c = out.getContext('2d');
			c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, L.avatar, L.avatar);
			c.drawImage(A.src, cx - side / 2, cy - side / 2, side, side, 0, 0, L.avatar, L.avatar);
			save.disabled = true; save.setAttribute('aria-busy', 'true');
			toBlob(out, 'image/jpeg', 0.9).then(function (b) {
				var fd = new FormData();
				fd.append('kind', 'avatar'); fd.append('file', b, 'avatar.jpg');
				return send('POST', 'media', fd);
			}).then(function (j) {
				say(T.avSaved);
				var u = j.media && j.media.url;
				if (u && meAv) { meAv.replaceChildren(el('img', { src: u, alt: '', width: 40, height: 40 })); }
				rm.hidden = false;
				setTimeout(function () { window.location.reload(); }, 900); // every face of mine on the page shows the new picture
			}).catch(function (er) { say(er.message || ERR, true); }).then(function () { save.disabled = false; save.removeAttribute('aria-busy'); });
		});
		rm.addEventListener('click', function () {
			rm.disabled = true;
			send('DELETE', 'media/avatar').then(function (j) { say(j.message || ''); setTimeout(function () { window.location.reload(); }, 900); })
				.catch(function (er) { say(er.message || ERR, true); }).then(function () { rm.disabled = false; });
		});
	}
})();
