/* nad-lan professionals' forum: "הדירה שמדברים עליה" (inc/pro-forum-home.php, Claude Design board 23). No library.
   - The one-tap price vote (זול / הוגן / יקר) works without entry: the forum's proof-of-work challenge is solved ahead, in the
     background, so the tap answers at once; the results bar replaces the buttons.
   - The sheet "כמה הדירה שלכם שווה? תשאלו את הפורום": city, the city's neighbourhoods (from the public file, through the
     server), street without a number, rooms, m², floor, asking price, chips, a question, pictures through the media module
     (media.js adds its composer to form[data-nlfmd-compose]; this file reads form.nlfExtra('topic')). Entry first: the forum's
     own one-step entry opens, and the sheet opens by itself after the page comes back.
   - In an answer on a home discussion: the optional "ההערכה שלי (₪)" field; the media module's nlfExtra() is wrapped, never
     replaced. People's text enters the page only through textContent. Nothing is sent by itself. */
(function () {
	'use strict';
	var C = window.NLF || {}, H = window.NLFH || {};
	if (!C.rest || !window.fetch || !window.Promise) { return; }
	var st = { member: null, nonce: '', ch: '', ts: '' };
	var ERR = 'משהו השתבש. נסו שוב.', WORDS = { 1: 'זול', 2: 'הוגן', 3: 'יקר' };
	var $ = function (s, r) { return (r || document).querySelector(s); };
	var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
	function store(k, v) { try { if (v === null) { sessionStorage.removeItem(k); } else { sessionStorage.setItem(k, v); } } catch (x) {} }
	function load(k) { try { return sessionStorage.getItem(k); } catch (x) { return null; } }

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
	function say(el, msg, err) { if (!el) { return; } el.textContent = msg || ''; el.classList.toggle('is-err', !!err); }
	function busy(btn, on) { if (btn) { btn.disabled = !!on; btn.setAttribute('aria-busy', on ? 'true' : 'false'); } }

	/* a signed-in member, or the forum's own one-step entry (forum.js opens it and reloads the page after the code) */
	function needMember(reopen) {
		return ready.then(function () {
			if (st.member) { return st.member; }
			if (reopen) { store('nlfh_open', '1'); }
			var b = document.createElement('button');
			b.type = 'button'; b.hidden = true; b.setAttribute('data-nlf-enter', '');
			document.body.appendChild(b); b.click(); b.remove();
			var e = new Error(''); e.code = 'cancel'; throw e;
		});
	}
	function write(path, data, form, retried) {
		return needMember(false).then(function () { return st.ch ? null : loadState(); }).then(function () {
			var trap = form && form.querySelector('[name="website"]');
			return solve(st.ch).then(function (n) {
				var extra = form && form.nlfExtra ? form.nlfExtra('topic') : null; // HOOK (media module, media.js): the pictures and their captions
				return req('POST', path, Object.assign({}, data, extra, { ch: st.ch, n: n, ts: st.ts, website: trap ? trap.value : '' }));
			});
		}).catch(function (e) {
			if (retried || e.code === 'cancel') { throw e; }
			if (e.code === 'nlf_ts' && /רגע/.test(e.message)) { return wait(3200).then(function () { return write(path, data, form, true); }); }
			if (e.code === 'nlf_nonce') { return loadState().then(function () { return write(path, data, form, true); }); }
			throw e;
		});
	}

	/* ---------------- the one-tap vote (parts א and ב) ---------------- */
	var pre = null; // the next challenge, solved ahead: { ch, ts, n }
	function presolve() {
		if (pre || !st.ch || !$('[data-nlfh-votebox]')) { return; }
		var ch = st.ch, ts = st.ts;
		pre = solve(ch).then(function (n) { return { ch: ch, ts: ts, n: n }; }, function () { pre = null; return null; });
	}
	ready.then(presolve);
	function el(tag, cls, text) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (text != null) { e.textContent = text; } return e; }
	function barNode(j) {
		var res = el('div', 'nlfh-res'), total = +j.total || 0;
		if (total > 0) {
			var bar = el('div', 'nlfh-bar'), cls = { 1: 'cheap', 2: 'fair', 3: 'dear' };
			bar.setAttribute('role', 'img');
			bar.setAttribute('aria-label', 'זול ' + j.pct[1] + '%, הוגן ' + j.pct[2] + '%, יקר ' + j.pct[3] + '%');
			[1, 2, 3].forEach(function (k) {
				var p = +j.pct[k] || 0;
				if (p < 1) { return; }
				var s = el('span', 'nlfh-bar-' + cls[k], (p >= 22 ? WORDS[k] + ' ' : '') + p + '%');
				s.style.width = p + '%';
				bar.appendChild(s);
			});
			res.appendChild(bar);
		}
		res.appendChild(el('span', 'nlfh-res-s', [j.line || '', j.mine ? 'הצבעתם: ' + WORDS[j.mine] : ''].filter(Boolean).join(' · ')));
		return res;
	}
	function vote(box, v, btn, again) {
		var msg = $('.nlfh-msg', box), tid = +box.getAttribute('data-topic');
		$$('[data-nlfh-vote]', box).forEach(function (b) { busy(b, true); });
		btn.setAttribute('aria-pressed', 'true');
		say(msg, 'רגע...');
		return ready.then(function () { return st.ch ? null : loadState(); }).then(function () {
			var p = pre; pre = null;
			return (p || Promise.resolve(null)).then(function (x) {
				if (x && x.ch === st.ch) { return x; }
				var ch = st.ch, ts = st.ts;
				return solve(ch).then(function (n) { return { ch: ch, ts: ts, n: n }; });
			});
		}).then(function (x) {
			return req('POST', 'home/vote', { topic_id: tid, vote: v, ch: x.ch, n: x.n, ts: x.ts, website: '' });
		}).then(function (j) {
			var res = barNode(j);
			box.parentNode.replaceChild(res, box);
			var live = el('p', 'nlfh-msg', j.message || ''); live.setAttribute('role', 'status');
			res.insertBefore(live, res.firstChild);
			presolve();
		}).catch(function (e) {
			if (!again && (e.code === 'nlf_nonce' || e.code === 'nlf_pow' || (e.code === 'nlf_ts' && /רגע/.test(e.message)))) {
				return (e.code === 'nlf_nonce' ? loadState() : wait(e.code === 'nlf_ts' ? 1200 : 0)).then(function () { return vote(box, v, btn, true); });
			}
			$$('[data-nlfh-vote]', box).forEach(function (b) { busy(b, false); b.setAttribute('aria-pressed', 'false'); });
			say(msg, e.message || ERR, true);
			presolve();
		});
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-nlfh-vote]'), box = b && b.closest('[data-nlfh-votebox]');
		if (!box || b.disabled) { return; }
		vote(box, +b.getAttribute('data-nlfh-vote'), b);
	});

	/* ---------------- the sheet of part ד ---------------- */
	var dlg = $('#nlfh-compose'), form = dlg && $('[data-nlfh-form]', dlg);
	function openSheet() {
		if (!dlg) { return; }
		needMember(true).then(function () {
			dlg._ret = document.activeElement;
			if (dlg.showModal) { if (!dlg.open) { dlg.showModal(); } } else { dlg.setAttribute('open', ''); }
			setTimeout(function () { var c = form && form.elements.city; if (c) { c.focus(); } }, 30);
		}).catch(function () {});
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-nlfh-open]');
		if (b) { e.preventDefault(); openSheet(); }
	});
	/* "דירה לדיון" in the forum's own compose sheet opens this sheet instead (before forum.js marks the kind) */
	document.addEventListener('click', function (e) {
		var b = e.target.closest('#nlf-compose .nlf-kinds [data-kind="home"]');
		if (!b) { return; }
		e.preventDefault(); e.stopImmediatePropagation();
		var c = $('#nlf-compose');
		if (c && c.close && c.open) { c.close(); } else if (c) { c.removeAttribute('open'); }
		openSheet();
	}, true);
	if (load('nlfh_open') === '1') {
		store('nlfh_open', null);
		ready.then(function () { if (st.member) { openSheet(); } });
	}

	function digits(v) { return String(v || '').replace(/\D+/g, ''); }
	function money(v) { var d = digits(v); return d ? '₪' + Number(d).toLocaleString('en-US') : ''; }
	if (form) {
		var city = form.elements.city, nb = form.elements.nbhd, nbBox = $('[data-nlfh-nbhd]', form), otherBox = $('[data-nlfh-other]', form), msg = $('.nlf-msg', form);
		city.addEventListener('change', function () {
			var o = city.options[city.selectedIndex], code = o ? +o.getAttribute('data-code') : 0;
			otherBox.hidden = city.value !== 'other';
			nbBox.hidden = true;
			while (nb.options.length > 1) { nb.remove(1); }
			nb.value = '';
			if (!code) { return; }
			req('GET', 'home/nbhd', { code: code }).then(function (j) {
				var cur = city.options[city.selectedIndex];
				if (!cur || +cur.getAttribute('data-code') !== code) { return; } // the city changed meanwhile
				(j.items || []).forEach(function (it) { var op = document.createElement('option'); op.value = String(it.id); op.textContent = it.title; nb.appendChild(op); });
				nbBox.hidden = !(j.items && j.items.length);
			}).catch(function () { nbBox.hidden = true; });
		});
		$$('[data-nlfh-chip]', form).forEach(function (b) {
			b.addEventListener('click', function () {
				var on = b.getAttribute('aria-pressed') !== 'true', g = b.getAttribute('data-nlfh-chip');
				$$('[data-nlfh-chip="' + g + '"]', form).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
				b.setAttribute('aria-pressed', on ? 'true' : 'false');
			});
		});
		form.elements.asking.addEventListener('blur', function () { form.elements.asking.value = money(form.elements.asking.value); });
		function chip(g) { var b = $('[data-nlfh-chip="' + g + '"][aria-pressed="true"]', form); return b ? b.getAttribute('data-v') : ''; }
		form.addEventListener('submit', function (e) {
			e.preventDefault();
			var btn = $(':scope > button[type="submit"]', form) || $('button[type="submit"]', form);
			var cityName = city.value === 'other' ? form.elements.city_other.value.trim() : city.value;
			var street = form.elements.street.value.trim();
			if (!city.value) { say(msg, 'בחרו עיר.', true); city.focus(); return; }
			if (cityName.length < 2) { say(msg, 'כתבו את שם העיר.', true); form.elements.city_other.focus(); return; }
			if (!form.elements.rooms.value) { say(msg, 'בחרו כמה חדרים.', true); form.elements.rooms.focus(); return; }
			if (/\d\s*[א-ת]?['׳"]?\s*$/.test(street)) { say(msg, 'בלי מספר בית, רק שם הרחוב.', true); form.elements.street.focus(); return; }
			busy(btn, true); say(msg, 'שולחים...');
			write('home', {
				city: cityName, nbhd: nb.value || 0, street: street, rooms: form.elements.rooms.value, sqm: digits(form.elements.sqm.value),
				floor: form.elements.floor.value.trim(), floors: digits(form.elements.floors.value), asking: digits(form.elements.asking.value),
				state: chip('state'), intent: chip('intent'), body: form.elements.body.value
			}, form).then(function (j) {
				say(msg, j.message);
				window.location.assign(j.url);
			}).catch(function (er) { if (er.code !== 'cancel') { say(msg, er.message, true); } }).then(function () { busy(btn, false); });
		});
	}

	/* ---------------- the estimate in an answer (part ג) ---------------- */
	var rf = H.est ? $('[data-nlf-replyform]') : null, inp = null, last = '';
	if (rf) {
		var row = $('.nlf-replyrow', rf), f = el('div', 'nlf-field nlfh-estf'), lab = el('label', '', 'ההערכה שלי (₪, לא חובה)');
		inp = el('input');
		inp.id = 'nlfh-est'; inp.name = 'estimate'; inp.type = 'text'; inp.inputMode = 'numeric'; inp.maxLength = 14; inp.autocomplete = 'off'; inp.placeholder = 'למשל 3,250,000';
		lab.htmlFor = 'nlfh-est';
		f.appendChild(lab); f.appendChild(inp);
		if (row && row.parentNode) { row.parentNode.insertBefore(f, row.nextSibling); } else { rf.appendChild(f); }
		inp.addEventListener('blur', function () { inp.value = money(inp.value).replace('₪', ''); });
		var prev = rf.nlfExtra; // the media module's, when it is on
		rf.nlfExtra = function (path) {
			var o = prev ? prev.call(rf, path) : null;
			if (path !== 'reply') { return o; }
			last = digits(inp.value);
			return last ? Object.assign({}, o || {}, { estimate: last }) : o;
		};
		/* the answer forum.js draws after sending gets its chip; the next full page shows the summary */
		var list = $('#nlf-replies');
		if (list && window.MutationObserver) {
			new MutationObserver(function (ms) {
				ms.forEach(function (m) {
					Array.prototype.forEach.call(m.addedNodes, function (n) {
						if (!last || !n.classList || !n.classList.contains('nlf-reply') || n.querySelector('.nlfh-chip')) { return; }
						var who = $('.nlf-who', n), c = el('span', 'nlfh-chip', 'ההערכה שלי: ' + money(last));
						if (who && who.nextSibling) { n.insertBefore(c, who.nextSibling); } else { n.appendChild(c); }
						last = '';
					});
				});
			}).observe(list, { childList: true });
		}
	}
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-nlfh-estimate]');
		if (!b || !inp) { return; }
		e.preventDefault();
		inp.scrollIntoView({ block: 'center', behavior: 'auto' });
		inp.focus();
	});
})();
