/* nad-lan professionals' forum: a member opens his own professional card (inc/pro-forum-card.php, Claude Design board 18).
   The invitation and the "אני בעל מקצוע" link open the form sheet (#nlfm-form); the same sheet edits an existing card.
   Someone who joins through the forum's entry sheet as "בעל מקצוע" gets the form by itself right after the entry.
   Every write solves the forum's proof-of-work challenge and sends the forum's session nonce, exactly as forum.js does.
   People's text enters the page only through textContent and form values. No library, no wheel or touch capture. */
(function () {
	'use strict';
	var C = window.NLF || {}, M = window.NLFM || {};
	if (!C.rest || !window.fetch) { return; }
	var FORMS = M.forms || {};
	var cs = M.state || { member: 0 };
	var st = { member: null, nonce: '', ch: '', ts: '' };
	var ERR = 'משהו השתבש. נסו שוב.';
	var AUTO = 'nlfm_auto';
	var $ = function (s, r) { return (r || document).querySelector(s); };
	var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

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
	function loadCard() { return req('GET', 'card/me').then(function (j) { cs = j.card || { member: 0 }; return cs; }); }

	/* proof of work: SHA-256(salt + nonce) starts with N zero bits (the forum's own challenge) */
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
	function write(path, data, form, retried) {
		return ready.then(function () { return st.ch ? null : loadState(); }).then(function () {
			var trap = form && form.querySelector('[name="website"]');
			return solve(st.ch).then(function (n) {
				return req('POST', path, Object.assign({}, data, { ch: st.ch, n: n, ts: st.ts, website: trap ? trap.value : '' }));
			});
		}).catch(function (e) {
			if (retried) { throw e; }
			if (e.code === 'nlf_ts' && /רגע/.test(e.message)) { return wait(3200).then(function () { return write(path, data, form, true); }); }
			if (e.code === 'nlf_nonce' || e.code === 'nlf_pow') { return loadState().then(function () { return write(path, data, form, true); }); }
			throw e;
		});
	}
	function store(k, v) { try { if (v === null) { sessionStorage.removeItem(k); } else { sessionStorage.setItem(k, v); } } catch (x) { /* private mode */ } }
	function read(k) { try { return sessionStorage.getItem(k); } catch (x) { return null; } }

	/* ---------------- the form sheet ---------------- */
	var dlg = $('#nlfm-form'), f = dlg && $('[data-nlfm-form]', dlg);
	if (!f) { return; }
	var msg = $('.nlfm-msg', f), go = $('[data-nlfm-go]', f), formsBox = $('[data-nlfm-forms]', f), count = $('[data-nlfm-count]', f);
	function say(t, bad) { msg.textContent = t || ''; msg.classList.toggle('is-err', !!bad); }
	function paintForms() {
		var pair = FORMS[f.elements.trade.value];
		formsBox.hidden = !pair;
		if (pair) { $('[data-nlfm-fm]', f).textContent = pair[0]; $('[data-nlfm-ff]', f).textContent = pair[1]; }
	}
	function paintHow() { $$('.nlfm-how label', f).forEach(function (l) { var i = $('input', l); l.classList.toggle('is-on', !!(i && i.checked)); }); }
	function paintCount() { var n = f.elements.bio.value.length; count.textContent = n > 0 ? n + ' מתוך 300' : ''; }
	function setRadio(name, v) { $$('input[name="' + name + '"]', f).forEach(function (i) { i.checked = i.value === v; }); }
	function fill() {
		var c = cs.card;
		f.reset();
		f.elements.name.value = c ? c.name : (cs.name || '');
		f.elements.trade.value = c ? c.trade : (read('nlfm_trade') || cs.trade || '');
		if (f.elements.trade.selectedIndex < 0) { f.elements.trade.value = ''; }
		f.elements.city.value = c ? c.city : '';
		f.elements.bio.value = c ? c.bio : '';
		f.elements.phone.value = c ? c.phone : '';
		setRadio('form', c ? c.form : 'm');
		setRadio('how', c ? c.how : 'phone');
		f.elements.video.checked = c ? !!c.video : true; // checked by default: video is on only because he leaves it checked
		$('#nlfm-form-h', dlg).textContent = 'הכרטיס שלי';
		go.textContent = c ? 'שמירת הכרטיס' : 'פתיחת הכרטיס';
		say(c && c.status === 'pending' ? 'הכרטיס מחכה לבדיקה קצרה. אפשר לעדכן אותו בינתיים.' : '');
		paintForms(); paintHow(); paintCount();
	}
	function openForm() {
		fill();
		dlg._ret = document.activeElement;
		if (dlg.showModal) { if (!dlg.open) { dlg.showModal(); } } else { dlg.setAttribute('open', ''); }
		setTimeout(function () { (f.elements.name.value ? f.elements.trade : f.elements.name).focus(); }, 30);
	}
	/* a guest opens the forum's own entry first; the form comes right after it (the entry reloads the page) */
	function enterThenForm() {
		store(AUTO, '1');
		var b = document.createElement('button');
		b.type = 'button'; b.hidden = true; b.setAttribute('data-nlf-enter', '');
		document.body.appendChild(b); b.click(); b.remove();
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-nlfm-open]');
		if (!b) { return; }
		e.preventDefault();
		ready.then(function () { if (st.member) { openForm(); } else { enterThenForm(); } });
	});
	f.elements.trade.addEventListener('change', paintForms);
	f.addEventListener('change', function (e) { if (e.target.name === 'how') { paintHow(); } });
	f.elements.bio.addEventListener('input', paintCount);
	f.addEventListener('submit', function (e) {
		e.preventDefault();
		var el = f.elements, how = $('input[name="how"]:checked', f), form = $('input[name="form"]:checked', f);
		var data = { name: el.name.value.trim(), trade: el.trade.value, form: form ? form.value : 'm', city: el.city.value.trim(), bio: el.bio.value.trim(),
			phone: el.phone.value.trim(), how: how ? how.value : 'forum', video: el.video.checked ? '1' : '0' };
		if (data.name.length < 2) { say('כתבו שם, 2 עד 60 תווים.', true); el.name.focus(); return; }
		if (!data.trade) { say('בחרו מקצוע מהרשימה.', true); el.trade.focus(); return; }
		if (data.city.length < 2) { say('כתבו עיר או אזור.', true); el.city.focus(); return; }
		if (data.how === 'phone' && !data.phone) { say('כדי להציג טלפון ווואטסאפ, כתבו מספר טלפון. אפשר גם לבחור פנייה רק דרך הפורום.', true); el.phone.focus(); return; }
		go.disabled = true; go.setAttribute('aria-busy', 'true'); say('שומרים...');
		write('card/save', data, f).then(function (j) {
			cs = j.card || cs;
			say(j.message);
			$$('[data-nlfm-inv]').forEach(function (x) { x.remove(); });
			$$('.nlfm-iam').forEach(function (x) { x.remove(); });
			if (j.url) { setTimeout(function () { window.location.assign(j.url); }, 900); }
			else { go.textContent = 'שמירת הכרטיס'; }
		}).catch(function (er) { say(er.message, true); }).then(function () { go.disabled = false; go.setAttribute('aria-busy', 'false'); });
	});

	/* ---------------- right after an entry as "בעל מקצוע" ---------------- */
	document.addEventListener('submit', function (e) {
		var s1 = e.target.closest && e.target.closest('[data-nlf-step1]');
		if (!s1 || !s1.elements.role) { return; }
		if (s1.elements.role.value === 'pro') {
			store(AUTO, '1');
			var tr = s1.elements.trade ? s1.elements.trade.value : '';
			store('nlfm_trade', tr && tr !== 'other' ? tr : null);
		} else { store(AUTO, null); }
	}, true);
	function maybeAuto() {
		if (read(AUTO) !== '1') { return; }
		if ($('dialog[open]')) { return; } // another sheet is busy (a reply or a new discussion goes on); the form waits for the next page
		loadState().then(loadCard).then(function () {
			if (!cs.member) { return; }
			store(AUTO, null);
			if (cs.invite || (cs.card === null && cs.role === 'pro' && !cs.linked)) { openForm(); }
		}).catch(function () {});
	}
	var entry = $('#nlf-entry');
	if (entry) { entry.addEventListener('close', function () { setTimeout(maybeAuto, 500); }); }
	ready.then(maybeAuto);

	/* ---------------- the invitation right after his reply is sent ---------------- */
	var list = $('#nlf-replies'), tpl = $('#nlfm-inv-tpl'), shown = false;
	if (list && tpl && window.MutationObserver) {
		new MutationObserver(function (recs) {
			if (shown) { return; }
			recs.forEach(function (r) {
				Array.prototype.forEach.call(r.addedNodes, function (n) {
					if (shown || !n.classList || !n.classList.contains('nlf-reply') || n.hasAttribute('data-id')) { return; } // a reply this page just sent
					loadCard().then(function () {
						if (shown || !cs.invite) { return; }
						shown = true;
						var form = $('[data-nlf-replyform]');
						var before = form && form.previousElementSibling && form.previousElementSibling.hasAttribute('data-nlfm-inv') ? form.previousElementSibling : null;
						if (before) { before.remove(); } // the one above the form moves to right after his reply
						n.parentNode.insertBefore(tpl.content.cloneNode(true), n.nextSibling);
					}).catch(function () {});
				});
			});
		}).observe(list, { childList: true });
	}
})();
