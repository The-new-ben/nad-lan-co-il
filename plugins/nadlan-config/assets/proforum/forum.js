/* nad-lan professionals' forum, version one (inc/pro-forum*.php). No library. Reading works without this file; it adds writing:
   the one-step entry (name + email + code), the compose sheet with a local draft and similar discussions, replies, thanks,
   follow, report, the reply that helped, the professional's window and his own switches. Every write solves a small
   proof-of-work challenge first (Web Crypto, SHA-256, in batches), so no outside service is called. No wheel or touch capture. */
(function () {
	'use strict';
	var C = window.NLF || {};
	if (!C.rest || !window.fetch) { return; }
	var st = { member: null, nonce: '', ch: '', ts: '' };
	var $ = function (s, r) { return (r || document).querySelector(s); };
	var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
	var ERR = 'משהו השתבש. נסו שוב.';

	function req(method, path, data) {
		var o = { method: method, credentials: 'same-origin', headers: { Accept: 'application/json' } };
		if (st.nonce) { o.headers['X-NLF-Nonce'] = st.nonce; }
		if (C.wpnonce) { o.headers['X-WP-Nonce'] = C.wpnonce; }
		var url = C.rest + path;
		if (data && method === 'GET') { url += (url.indexOf('?') < 0 ? '?' : '&') + new URLSearchParams(data).toString(); }
		else if (data) { o.headers['Content-Type'] = 'application/json'; o.body = JSON.stringify(data); }
		return fetch(url, o).then(function (r) {
			return r.json().catch(function () { return {}; }).then(function (j) {
				var d = (j && j.data) || {};
				if (j && j.ch) { st.ch = j.ch; st.ts = j.ts; } else if (d.ch) { st.ch = d.ch; st.ts = d.ts; }
				if (!r.ok || !j || j.ok !== 1) { var e = new Error((j && j.message) || ERR); e.code = j && j.code; throw e; }
				return j;
			});
		});
	}
	function loadState() { return req('GET', 'state').then(function (j) { st.member = j.member; st.nonce = j.nonce || ''; return j; }); }
	var ready = loadState().catch(function () {});

	/* proof of work: SHA-256(salt + nonce) must start with N zero bits */
	function zeroOk(buf, bits) {
		var a = new Uint8Array(buf), n = 0;
		for (var i = 0; i < a.length; i++) {
			if (a[i] === 0) { n += 8; if (n >= bits) { return true; } continue; }
			for (var k = 7; k >= 0; k--) { if (a[i] & (1 << k)) { return n >= bits; } n++; }
		}
		return n >= bits;
	}
	function solve(ch) {
		var p = String(ch || '').split('.'), salt = p[0], bits = +p[1];
		if (!salt || !bits) { return Promise.reject(new Error(ERR)); }
		if (!window.crypto || !crypto.subtle || !window.TextEncoder) { return Promise.reject(new Error('הדפדפן הזה לא תומך בבדיקת האבטחה. נסו דפדפן אחר.')); }
		var enc = new TextEncoder(), start = 0, B = 64;
		function batch() {
			var jobs = [];
			for (var i = 0; i < B; i++) { jobs.push(crypto.subtle.digest('SHA-256', enc.encode(salt + (start + i)))); }
			return Promise.all(jobs).then(function (hs) {
				for (var i = 0; i < hs.length; i++) { if (zeroOk(hs[i], bits)) { return String(start + i); } }
				start += B;
				if (start > 4000000) { throw new Error('בדיקת האבטחה לא הושלמה. נסו שוב.'); }
				return batch();
			});
		}
		return batch();
	}
	function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
	/* every write: fresh challenge solved, form time, trap value; one quiet retry for "too fast" and a stale page nonce */
	function write(path, data, form, retried) {
		return ready.then(function () { return st.ch ? null : loadState(); }).then(function () {
			var trap = form && form.querySelector('[name="website"]');
			return solve(st.ch).then(function (n) {
				var d = Object.assign({}, data, { ch: st.ch, n: n, ts: st.ts, website: trap ? trap.value : '' });
				return req('POST', path, d);
			});
		}).catch(function (e) {
			if (retried) { throw e; }
			if (e.code === 'nlf_ts' && /רגע/.test(e.message)) { return wait(3200).then(function () { return write(path, data, form, true); }); }
			if (e.code === 'nlf_nonce') { return loadState().then(function () { return write(path, data, form, true); }); }
			if (e.code === 'nlf_need_entry') { st.member = null; return requireMember().then(function () { return write(path, data, form, true); }); }
			throw e;
		});
	}
	function say(el, msg, err) {
		if (!el) { return; }
		el.textContent = msg || '';
		el.classList.toggle('is-err', !!err);
	}
	function busy(btn, on) { if (btn) { btn.disabled = !!on; btn.setAttribute('aria-busy', on ? 'true' : 'false'); } }
	function liveEl(from) {
		var box = from && from.closest('.nlf');
		return (box && $('.nlf-live', box)) || $('#nlf-live');
	}

	/* dialogs: native <dialog> (Escape closes, focus returns to the opener) */
	function openDlg(d) {
		if (!d) { return; }
		d._ret = document.activeElement;
		if (d.showModal) { if (!d.open) { d.showModal(); } } else { d.setAttribute('open', ''); }
		var f = $('input:not([type="hidden"]):not([tabindex="-1"]):not([type="radio"]),select,textarea', d) || $('input[type="radio"]', d);
		if (f) { setTimeout(function () { f.focus(); }, 30); }
	}
	function closeDlg(d) { if (!d) { return; } if (d.close) { if (d.open) { d.close(); } } else { d.removeAttribute('open'); onClose(d); } }
	function onClose(d) {
		if (d.id === 'nlf-entry' && entryWait) { var w = entryWait; entryWait = null; var e = new Error(''); e.code = 'cancel'; w.rej(e); }
		if (d._ret && d._ret.focus) { d._ret.focus(); }
	}
	$$('dialog.nlf').forEach(function (d) {
		d.addEventListener('close', function () { onClose(d); });
		d.addEventListener('click', function (e) { if (e.target === d) { closeDlg(d); } });
		$$('[data-nlf-close]', d).forEach(function (b) { b.addEventListener('click', function () { closeDlg(d); }); });
		if (!d.showModal) { d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeDlg(d); } }); }
	});

	/* ---------------- the one-step entry ---------------- */
	var entry = $('#nlf-entry'), entryWait = null, entryData = {}, timer = null;
	function requireMember(opts) {
		opts = opts || {};
		return ready.then(function () {
			if (st.member) { return st.member; }
			if (!entry) { throw new Error(ERR); }
			return new Promise(function (res, rej) {
				entryWait = { res: res, rej: rej };
				entryData.claim = opts.claim || 0;
				var s1 = $('[data-nlf-step1]', entry), s2 = $('[data-nlf-step2]', entry);
				s1.hidden = false; s2.hidden = true;
				say($('.nlf-msg', entry), '');
				openDlg(entry);
			});
		});
	}
	function countdown() {
		var again = $('[data-nlf-again]', entry), out = $('[data-nlf-count]', entry), left = 60;
		again.disabled = true;
		clearInterval(timer);
		timer = setInterval(function () {
			left--;
			out.textContent = left > 0 ? 'בעוד 0:' + (left < 10 ? '0' : '') + left : '';
			if (left <= 0) { clearInterval(timer); again.disabled = false; }
		}, 1000);
	}
	function sendCode(form) {
		var msg = $('.nlf-msg', entry);
		return write('code', { name: entryData.name, email: entryData.email, role: entryData.role, consent: '1' }, form).then(function (j) {
			say(msg, j.message);
			$('[data-nlf-step1]', entry).hidden = true;
			var s2 = $('[data-nlf-step2]', entry);
			s2.hidden = false;
			$$('.nlf-digits input', s2).forEach(function (i) { i.value = ''; });
			$('.nlf-digits input', s2).focus();
			countdown();
		});
	}
	if (entry) {
		var s1 = $('[data-nlf-step1]', entry), s2 = $('[data-nlf-step2]', entry), digits = $$('.nlf-digits input', s2);
		/* "בעל מקצוע" opens the trade list (inc/pro-forum-trades.php); "תחום אחר" opens a free-text field kept for review */
		var tBox = $('[data-nlf-trade]', s1), oBox = $('[data-nlf-trade-other]', s1);
		var tradeView = function () {
			var pro = s1.elements.role.value === 'pro';
			if (tBox) { tBox.hidden = !pro; }
			if (oBox) { oBox.hidden = !(pro && s1.elements.trade && s1.elements.trade.value === 'other'); }
		};
		s1.elements.role.addEventListener('change', tradeView);
		if (s1.elements.trade) { s1.elements.trade.addEventListener('change', tradeView); }
		tradeView();
		s1.addEventListener('submit', function (e) {
			e.preventDefault();
			var msg = $('.nlf-msg', entry), btn = $('button[type="submit"]', s1);
			entryData.name = s1.elements.name.value.trim();
			entryData.email = s1.elements.email.value.trim();
			entryData.role = s1.elements.role.value;
			entryData.trade = entryData.role === 'pro' && s1.elements.trade ? s1.elements.trade.value : '';
			entryData.trade_other = entryData.trade === 'other' && s1.elements.trade_other ? s1.elements.trade_other.value.trim() : '';
			if (entryData.trade === 'other') { entryData.trade = ''; }
			if (entryData.name.length < 2) { say(msg, 'כתבו שם.', true); s1.elements.name.focus(); return; }
			if (!/^\S+@\S+\.\S+$/.test(entryData.email)) { say(msg, 'כתבו כתובת מייל תקינה.', true); s1.elements.email.focus(); return; }
			if (!s1.elements.consent.checked) { say(msg, 'כדי להמשיך צריך לאשר את כללי הפורום ואת מדיניות הפרטיות.', true); return; }
			busy(btn, true); say(msg, 'שולחים קוד...');
			sendCode(s1).catch(function (er) { say(msg, er.message, true); }).then(function () { busy(btn, false); });
		});
		digits.forEach(function (inp, i) {
			inp.addEventListener('input', function () {
				var v = inp.value.replace(/\D/g, '');
				if (v.length > 1) { // a pasted or autofilled code
					v.split('').slice(0, 6 - i).forEach(function (ch, k) { digits[i + k].value = ch; });
				} else { inp.value = v; }
				var next = digits.filter(function (x) { return !x.value; })[0];
				if (next) { if (inp.value) { next.focus(); } } else if (s2.requestSubmit) { s2.requestSubmit(); } else { s2.dispatchEvent(new Event('submit', { cancelable: true })); }
			});
			inp.addEventListener('keydown', function (e) { if (e.key === 'Backspace' && !inp.value && i > 0) { digits[i - 1].focus(); } });
		});
		s2.addEventListener('submit', function (e) {
			e.preventDefault();
			var code = digits.map(function (x) { return x.value; }).join(''), msg = $('.nlf-msg', entry), btn = $('button[type="submit"]', s2);
			if (!/^\d{6}$/.test(code)) { say(msg, 'הקוד הוא 6 ספרות.', true); return; }
			if (btn.disabled) { return; }
			busy(btn, true); say(msg, 'בודקים...');
			write('enter', { email: entryData.email, code: code, name: entryData.name, role: entryData.role, trade: entryData.trade || '', trade_other: entryData.trade_other || '', claim_pro: entryData.claim || 0 }, s2).then(function (j) {
				st.member = j.member; st.nonce = j.nonce || '';
				st.claimMismatch = !!j.claim_mismatch;
				var w = entryWait; entryWait = null;
				say(msg, j.message);
				closeDlg(entry);
				if (w) { w.res(st.member); }
			}).catch(function (er) {
				say(msg, er.message, true);
				digits.forEach(function (x) { x.value = ''; }); digits[0].focus();
			}).then(function () { busy(btn, false); });
		});
		$('[data-nlf-again]', entry).addEventListener('click', function () {
			var msg = $('.nlf-msg', entry);
			say(msg, 'שולחים שוב...');
			sendCode(s1).catch(function (er) { say(msg, er.message, true); });
		});
	}
	function reload() { window.location.reload(); }
	/* the menu's "הצטרפות לבעלי מקצוע" (/forum/?join=1): the entry opens on its own with "בעל מקצוע" chosen and the trade list shown */
	if (entry && /[?&]join=1(&|$)/.test(window.location.search)) {
		ready.then(function () {
			if (st.member) { return; }
			var r = $('[data-nlf-step1]', entry).elements.role;
			if (r) {
				if (r.length) { Array.prototype.forEach.call(r, function (x) { if (x.value === 'pro') { x.checked = true; } }); } else { r.value = 'pro'; }
				r.dispatchEvent ? (r.length ? r[0] : r).dispatchEvent(new Event('change', { bubbles: true })) : null;
			}
			requireMember().then(reload).catch(function () {});
		});
	}
	document.addEventListener('click', function (e) {
		var t = e.target.closest('[data-nlf-enter],[data-nlf-leave]');
		if (!t) { return; }
		if (t.hasAttribute('data-nlf-enter')) { requireMember().then(reload).catch(function () {}); return; }
		var leave = function () { return req('POST', 'leave', {}); };
		ready.then(leave).catch(function (er) {
			if (er.code === 'nlf_nonce') { return loadState().then(leave); } // a stale page: one quiet retry with a fresh nonce
			throw er;
		}).then(reload).catch(function (er) { say(liveEl(t), er.message, true); });
	});

	/* ---------------- compose ---------------- */
	var comp = $('#nlf-compose'), cf = comp && $('[data-nlf-composeform]', comp), DKEY = 'nlf_draft';
	function store(k, v) { try { if (v === null) { localStorage.removeItem(k); } else { localStorage.setItem(k, JSON.stringify(v)); } } catch (x) {} }
	function load(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (x) { return null; } }
	function setKind(k) { $$('.nlf-kinds button', cf).forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-kind') === k ? 'true' : 'false'); }); }
	function getKind() { var b = $('.nlf-kinds button[aria-pressed="true"]', cf); return b ? b.getAttribute('data-kind') : 'question'; }
	function setTo(pro, name) {
		cf.elements.pro_id.value = pro || '';
		var box = $('[data-nlf-tobox]', cf);
		box.hidden = !pro;
		$('span', box).textContent = pro ? 'אל: ' + (name || '') : '';
	}
	function openCompose(pre) {
		if (!cf) { return; }
		pre = pre || {};
		var d = pre.title ? null : load(DKEY);
		setKind(pre.kind || (d && d.kind) || 'question');
		cf.elements.cat.value = pre.cat || (d && d.cat) || 'general';
		cf.elements.title.value = pre.title || (d && d.title) || '';
		cf.elements.body.value = (d && !pre.title && d.body) || '';
		cf.elements.city.value = (d && !pre.title && d.city) || '';
		setTo(pre.pro || 0, pre.proName || '');
		say($('.nlf-msg', cf), '');
		$('[data-nlf-draft]', cf).textContent = d && !pre.title ? 'הטיוטה שוחזרה' : '';
		$('[data-nlf-similar]', cf).hidden = true;
		openDlg(comp);
		if (cf.elements.title.value) { similar(); }
	}
	var dTimer = null, sTimer = null;
	function saveDraft() {
		clearTimeout(dTimer);
		dTimer = setTimeout(function () {
			store(DKEY, { kind: getKind(), cat: cf.elements.cat.value, title: cf.elements.title.value, body: cf.elements.body.value, city: cf.elements.city.value });
			$('[data-nlf-draft]', cf).textContent = 'הטיוטה נשמרה';
		}, 600);
	}
	function similar() {
		var q = cf.elements.title.value.trim(), box = $('[data-nlf-similar]', cf);
		if (q.length < 8) { box.hidden = true; return; }
		ready.then(function () { return req('GET', 'similar', { q: q }); }).then(function (j) {
			var ul = $('ul', box);
			ul.textContent = '';
			(j.items || []).forEach(function (it) {
				var li = document.createElement('li'), a = document.createElement('a');
				a.href = it.url; a.textContent = it.title + (it.replies ? ' · ' + it.replies : '');
				li.appendChild(a); ul.appendChild(li);
			});
			box.hidden = !(j.items && j.items.length);
		}).catch(function () { box.hidden = true; });
	}
	if (cf) {
		$$('.nlf-kinds button', cf).forEach(function (b) { b.addEventListener('click', function () { setKind(b.getAttribute('data-kind')); saveDraft(); }); });
		cf.addEventListener('input', function (e) {
			saveDraft();
			if (e.target === cf.elements.title) { clearTimeout(sTimer); sTimer = setTimeout(similar, 450); }
		});
		$('[data-nlf-to-all]', cf).addEventListener('click', function () { setTo(0); });
		cf.addEventListener('submit', function (e) {
			e.preventDefault();
			var msg = $('.nlf-msg', cf), btn = $('button[type="submit"]', cf), title = cf.elements.title.value.trim();
			if (title.length < 8) { say(msg, 'הכותרת קצרה מדי. כתבו לפחות 8 תווים.', true); cf.elements.title.focus(); return; }
			busy(btn, true); say(msg, 'שולחים...');
			requireMember().then(function () {
				return write('topic', { kind: getKind(), cat: cf.elements.cat.value, title: title, body: cf.elements.body.value, city: cf.elements.city.value, pro_id: cf.elements.pro_id.value || 0 }, cf);
			}).then(function (j) {
				store(DKEY, null);
				say(msg, j.message);
				window.location.assign(j.url);
			}).catch(function (er) { if (er.code !== 'cancel') { say(msg, er.message, true); } }).then(function () { busy(btn, false); });
		});
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-nlf-compose]');
		if (!b) { return; }
		openCompose({ kind: b.getAttribute('data-kind') || '', cat: b.getAttribute('data-cat') || '' });
	});

	/* ---------------- one discussion ---------------- */
	var thread = $('.nlf-thread'), tid = thread ? +thread.getAttribute('data-topic') : 0;
	if (thread && thread.getAttribute('data-live') === '1') {
		ready.then(function () { return req('POST', 'view', { topic_id: tid }); }).catch(function () {});
	}
	var rep = $('#nlf-report'), rf = rep && $('[data-nlf-reportform]', rep), repTarget = null;
	if (rf) {
		rf.addEventListener('submit', function (e) {
			e.preventDefault();
			var msg = $('.nlf-msg', rf), r = rf.querySelector('input[name="reason"]:checked'), btn = $('button[type="submit"]', rf);
			if (!r) { say(msg, 'בחרו סיבה.', true); return; }
			busy(btn, true);
			write('report', { type: repTarget.type, id: repTarget.id, reason: r.value }, rf).then(function (j) {
				say(msg, j.message);
				setTimeout(function () { closeDlg(rep); }, 1400);
			}).catch(function (er) { say(msg, er.message, true); }).then(function () { busy(btn, false); });
		});
	}
	function thankLabel(b, n) {
		var s = $('span', b) || b;
		s.textContent = b.getAttribute('data-label') + (n > 0 ? ' · ' + n : '');
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-nlf-thank],[data-nlf-follow],[data-nlf-quote],[data-nlf-unquote],[data-nlf-solve],[data-nlf-report]');
		if (!b || !b.closest('.nlf')) { return; }
		var live = liveEl(b);
		if (b.hasAttribute('data-nlf-report')) {
			if (!rep) { return; }
			requireMember().then(function () {
				repTarget = { type: b.getAttribute('data-nlf-report'), id: +b.getAttribute('data-id') };
				rf.reset(); say($('.nlf-msg', rf), '');
				openDlg(rep);
			}).catch(function () {});
			return;
		}
		if (b.hasAttribute('data-nlf-quote')) {
			var art = b.closest('.nlf-reply'), form = $('[data-nlf-replyform]');
			if (!art || !form) { return; }
			form.elements.quote_id.value = art.getAttribute('data-id');
			var q = $('.nlf-quoting', form);
			$('span', q).textContent = 'מצטטים את ' + art.getAttribute('data-name') + ': "' + art.getAttribute('data-text') + '"';
			q.hidden = false;
			form.elements.body.focus();
			return;
		}
		if (b.hasAttribute('data-nlf-unquote')) {
			var f = b.closest('form');
			f.elements.quote_id.value = ''; $('.nlf-quoting', f).hidden = true; f.elements.body.focus();
			return;
		}
		busy(b, true);
		requireMember().then(function () {
			if (b.hasAttribute('data-nlf-thank')) {
				return write('thank', { type: b.getAttribute('data-nlf-thank'), id: +b.getAttribute('data-id') }).then(function (j) {
					b.setAttribute('aria-pressed', j.on ? 'true' : 'false'); b.classList.toggle('is-on', !!j.on); thankLabel(b, j.count);
				});
			}
			if (b.hasAttribute('data-nlf-follow')) {
				var on = b.getAttribute('aria-pressed') !== 'true';
				return write('follow', { topic_id: tid, on: on ? '1' : '0' }).then(function (j) {
					b.setAttribute('aria-pressed', j.on ? 'true' : 'false'); b.classList.toggle('is-on', !!j.on);
					b.textContent = j.on ? 'במעקב' : 'מעקב'; say(live, j.message);
				});
			}
			if (b.hasAttribute('data-nlf-solve')) {
				return write('solve', { topic_id: tid, reply_id: +b.getAttribute('data-nlf-solve') }).then(reload);
			}
		}).catch(function (er) { if (er.code !== 'cancel') { say(live, er.message, true); } }).then(function () { busy(b, false); });
	});
	var rform = $('[data-nlf-replyform]');
	if (rform) {
		rform.addEventListener('submit', function (e) {
			e.preventDefault();
			var body = rform.elements.body.value.trim(), btn = $('button[type="submit"]', rform), live = liveEl(rform);
			if (body.length < 2) { say(live, 'כתבו כמה מילים לפני השליחה.', true); rform.elements.body.focus(); return; }
			busy(btn, true);
			requireMember().then(function () {
				return write('reply', { topic_id: tid, body: body, quote_id: +rform.elements.quote_id.value || 0 }, rform);
			}).then(function (j) {
				var art = document.createElement('article'), who = document.createElement('span'), p = document.createElement('p');
				art.className = 'nlf-reply'; art.id = 'r' + j.id;
				who.className = 'nlf-who'; who.textContent = j.author;
				p.className = 'nlf-body'; p.style.whiteSpace = 'pre-line'; p.textContent = body;
				art.appendChild(who); art.appendChild(p);
				if (j.status !== 'live') { var n = document.createElement('p'); n.className = 'nlf-note'; n.textContent = 'ההודעה תעלה אחרי בדיקה קצרה'; art.appendChild(n); }
				var list = $('#nlf-replies'), none = $('[data-nlf-noreplies]');
				if (none) { none.remove(); }
				list.appendChild(art);
				rform.reset(); $('.nlf-quoting', rform).hidden = true;
				say(live, j.message);
			}).catch(function (er) { if (er.code !== 'cancel') { say(live, er.message, true); } }).then(function () { busy(btn, false); });
		});
	}

	/* ---------------- the professional's window, the card box and the owner's switches ---------------- */
	$$('.nlf-tabs').forEach(function (list) {
		var tabs = $$('[role="tab"]', list);
		function pick(t) {
			tabs.forEach(function (x) {
				var on = x === t;
				x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1;
				var p = document.getElementById(x.getAttribute('aria-controls')); if (p) { p.hidden = !on; }
			});
		}
		tabs.forEach(function (t, i) {
			t.addEventListener('click', function () { pick(t); });
			t.addEventListener('keydown', function (e) {
				var k = e.key, j = -1;
				if (k === 'ArrowLeft') { j = (i + 1) % tabs.length; } else if (k === 'ArrowRight') { j = (i - 1 + tabs.length) % tabs.length; }
				else if (k === 'Home') { j = 0; } else if (k === 'End') { j = tabs.length - 1; }
				if (j > -1) { e.preventDefault(); pick(tabs[j]); tabs[j].focus(); }
			});
		});
	});
	$$('[data-nlf-ask]').forEach(function (f) {
		f.addEventListener('submit', function (e) {
			e.preventDefault();
			var w = f.closest('.nlf-win'), to = f.querySelector('input[name="to"]:checked');
			var only = to && to.value === 'pro';
			openCompose({ kind: 'question', cat: w.getAttribute('data-cat'), title: f.elements.q.value.trim(),
				pro: only ? +w.getAttribute('data-pro') : 0, proName: w.getAttribute('data-pro-name') });
		});
	});
	var rq = $('#nlf-request'), rqf = rq && $('[data-nlf-requestform]', rq);
	function openRequest(pro, kind, mismatch) {
		if (!rqf) { return; }
		rqf.reset();
		rqf.elements.pro_id.value = pro;
		$$('input[name="kind"]', rqf).forEach(function (x) { x.checked = x.value === kind; });
		$('[data-nlf-mismatch]', rqf).hidden = !mismatch;
		say($('.nlf-msg', rqf), '');
		openDlg(rq);
	}
	if (rqf) {
		rqf.addEventListener('submit', function (e) {
			e.preventDefault();
			var msg = $('.nlf-msg', rqf), btn = $('button[type="submit"]', rqf), k = rqf.querySelector('input[name="kind"]:checked');
			if (rqf.elements.body.value.trim().length < 5) { say(msg, 'כתבו במשפט מה תרצו שנעשה.', true); rqf.elements.body.focus(); return; }
			busy(btn, true);
			write('request', { pro_id: +rqf.elements.pro_id.value, kind: k ? k.value : 'ownership', body: rqf.elements.body.value, phone: rqf.elements.phone.value }, rqf).then(function (j) {
				say(msg, j.message);
			}).catch(function (er) { say(msg, er.message, true); }).then(function () { busy(btn, false); });
		});
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-nlf-join],[data-nlf-removal]');
		if (!b) { return; }
		var join = b.hasAttribute('data-nlf-join'), pro = +b.getAttribute(join ? 'data-nlf-join' : 'data-nlf-removal');
		var had = !!st.member;
		requireMember({ claim: pro }).then(function (m) {
			if (m && +m.pro === pro) { reload(); return; } // the email matches the card: the page shows his own switches
			openRequest(pro, join ? 'ownership' : 'removal', join && (had || st.claimMismatch));
		}).catch(function () {});
	});
	$$('[data-nlf-owner]').forEach(function (box) {
		var live = $('.nlf-live', box), on = $('[data-nlf-owner-live]', box), off = $('[data-nlf-removed]', box), conf = $('[data-nlf-confirm]', box);
		function act(d, v, el) {
			busy(el, true);
			return write('owner', { do: d, value: v ? '1' : '0' }).then(function (j) {
				say(live, j.message);
				var vis = $('[data-nlf-own="visible"]', box), ph = $('[data-nlf-own="phone"]', box);
				vis.checked = !!j.state.visible; ph.checked = !!j.state.phone;
				on.hidden = !!j.state.removed; off.hidden = !j.state.removed;
				return j;
			}).catch(function (er) { say(live, er.message, true); throw er; }).then(function (j) { busy(el, false); return j; }, function () { busy(el, false); });
		}
		$$('[data-nlf-own]', box).forEach(function (c) {
			c.addEventListener('change', function () { act(c.getAttribute('data-nlf-own'), c.checked, c); });
		});
		$('[data-nlf-remove]', box).addEventListener('click', function () { conf.hidden = false; $('[data-nlf-remove-yes]', box).focus(); });
		$('[data-nlf-remove-no]', box).addEventListener('click', function () { conf.hidden = true; $('[data-nlf-remove]', box).focus(); });
		$('[data-nlf-remove-yes]', box).addEventListener('click', function () {
			act('remove', true, this).then(function () { conf.hidden = true; var r = $('[data-nlf-restore]', box); if (r) { r.focus(); } });
		});
		$('[data-nlf-restore]', box).addEventListener('click', function () { act('restore', true, this); });
	});
})();
