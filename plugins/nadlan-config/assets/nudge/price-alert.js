/* nadlan-config - PRICE ALERT window (HAD-684, Claude Design v106 PriceAlert). Loaded with defer on Hebrew project pages and
 * listings that inc/price-nudge.php switched on. The markup waits inside <template id="nlpa-tpl"> (no text in the indexed page)
 * and is cloned only when the window opens. */
(function () {
	'use strict';
	var root = document.getElementById('nlnu');
	if (!root || window.__nlpa) { return; }
	window.__nlpa = 1;
	var C = {};
	try { C = JSON.parse(root.getAttribute('data-c') || '{}'); } catch (e) { return; }
	if (!/^he/i.test(document.documentElement.lang || 'he')) { return; }
	var LS = { g: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, s: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
	var SS = { g: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }, s: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} } };
	function ev(n, x) {
		var p = { pa_type: C.t, pa_id: C.id };
		for (var k in (x || {})) { p[k] = x[k]; }
		try {
			if (typeof window.nadlanGA === 'function') { window.nadlanGA(n, p); }
			else if (typeof window.gtag === 'function') { window.gtag('event', n, p); }
			else if (window.dataLayer) { window.dataLayer.push(Object.assign({ event: n }, p)); }
		} catch (e) {}
	}
	var DAY = 864e5, now = Date.now();
	var PV = /[?&]nudge=show(?:&|#|$)/.test(location.search);
	/* ?nudge=show: the owner's viewing link, the window after 2 s whatever the holdout, the quiet days or the session say */
	if (!PV && ((+(LS.g('nlpa_done') || 0)) > now || (+(LS.g('nlpa_q') || 0)) > now || SS.g('nlpa_s'))) { return; }
	var b = null;
	try { b = JSON.parse(LS.g('nlpa_b') || 'null'); } catch (e) { b = null; }
	if (!b || typeof b.v !== 'number' || !(b.t > now)) { b = { v: Math.floor(Math.random() * 100), t: now + 30 * DAY }; LS.s('nlpa_b', JSON.stringify(b)); }
	if (!PV && b.v < C.h) { if (!SS.g('nlpa_h')) { SS.s('nlpa_h', '1'); ev('pa_holdout'); } return; }
	/* at most two showings in 30 days for someone who did not sign up (the third converts at a third of the first) */
	var cap = null;
	try { cap = JSON.parse(LS.g('nlpa_n') || 'null'); } catch (e) { cap = null; }
	if (!cap || typeof cap.n !== 'number' || !(cap.t > now)) { cap = { n: 0, t: now + 30 * DAY }; }
	if (!PV && cap.n >= 2) { return; }

	var state = 'idle', vis = 0, maxD = 0, maxPx = 0, lastY = window.scrollY, lastT = performance.now(), awayAt = 0, waTapped = false;
	var el = null, card = null, interest = '', trigger = '', opener = null, desk = false, drag = null, touched = false, ignT = null;
	var mqDesk = window.matchMedia('(min-width: 760px)');
	document.addEventListener('click', function (e) {
		var a = e.target && e.target.closest && e.target.closest('a[href*="wa.me/"],a[href*="api.whatsapp.com"]');
		if (a && !(card && card.contains(a))) { waTapped = true; }
	}, true);
	function depth() { var h = document.documentElement.scrollHeight - innerHeight; return h > 0 ? scrollY / h : 0; }
	function read() { return maxD >= C.dp || maxPx >= innerHeight; } // a quarter of the page or one screen, the smaller
	function otherDialog() {
		var ds = document.querySelectorAll('[aria-modal="true"],dialog[open]');
		for (var i = 0; i < ds.length; i++) { var d = ds[i]; if (card && card.contains(d)) { continue; } if (d.offsetParent !== null || getComputedStyle(d).position === 'fixed') { var r = d.getBoundingClientRect(); if (r.width > 40 && r.height > 40) { return true; } } }
		return false;
	}
	function busy() {
		var a = document.activeElement;
		if (a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)) { return true; }
		if (a && a.isContentEditable) { return true; }
		if (document.fullscreenElement || document.webkitFullscreenElement) { return true; }
		if (waTapped) { return true; }
		return otherDialog();
	}

	/* ---------- show / hide ---------- */
	function build() {
		var tpl = document.getElementById('nlpa-tpl');
		if (!tpl || !tpl.content) { return false; }
		root.appendChild(tpl.content.cloneNode(true));
		card = root.querySelector('.nlpa');
		el = root;
		wire();
		return !!card;
	}
	function show(tr) {
		if (state !== 'idle' || (!PV && busy())) { return; }
		if (!card && !build()) { return; }
		state = 'in'; trigger = tr;
		if (!PV) { SS.s('nlpa_s', '1'); cap.n++; LS.s('nlpa_n', JSON.stringify(cap)); }
		desk = mqDesk.matches;
		opener = document.activeElement;
		root.classList.toggle('is-desk', desk);
		card.setAttribute('aria-modal', desk ? 'true' : 'false');
		root.hidden = false;
		void root.offsetWidth;
		root.classList.add('is-in');
		document.body.classList.add('nlnu-on');
		setH();
		if (desk) { try { card.focus({ preventScroll: true }); } catch (e) {} }
		ev('pa_shown', { pa_trigger: PV ? 'preview' : tr, pa_down: C.down });
		/* ignored on a phone: no touch inside it for 30 s while the reader keeps scrolling -> it leaves, 1 day of quiet */
		if (!desk) { ignT = setTimeout(function () { if (!touched && state === 'in') { hide('ignored'); } }, 30000); }
	}
	function hide(how) {
		if (state !== 'in') { return; }
		state = 'out';
		clearTimeout(ignT);
		if (!PV) {
			if (how === 'done') { LS.s('nlpa_done', String(Date.now() + 365 * DAY)); }
			else { LS.s('nlpa_q', String(Date.now() + (how === 'ignored' ? C.qi : C.q) * DAY)); }
		}
		root.classList.remove('is-in');
		setTimeout(function () {
			root.hidden = true; card.style.transform = '';
			document.body.classList.remove('nlnu-on');
			if (desk && opener && opener.focus) { try { opener.focus({ preventScroll: true }); } catch (e) {} }
		}, 420);
		if (how !== 'done') { ev('pa_close', { pa_how: how, pa_step: card.getAttribute('data-step') }); }
	}
	function setH() { if (card) { document.body.style.setProperty('--nlnu-h', card.offsetHeight + 'px'); } }
	function step(n) {
		card.setAttribute('data-step', String(n));
		setH(); kb();
		if (n === 2) { var t = card.querySelector('#nlpa-tel'); if (t) { try { t.focus({ preventScroll: true }); } catch (e) {} } }
		if (n === 3) { var d = card.querySelector('.nlpa-done'); if (d) { try { d.focus({ preventScroll: true }); } catch (e) {} } }
	}

	/* the phone keyboard: keep the sheet above it (iOS leaves fixed bottoms under the keyboard) */
	function kb() {
		var vv = window.visualViewport;
		if (!vv || desk || !card) { root.style.removeProperty('--nlpa-kb'); root.style.removeProperty('--nlpa-vh'); return; }
		var off = Math.max(0, window.innerHeight - vv.height - vv.offsetTop);
		root.style.setProperty('--nlpa-kb', Math.round(off) + 'px');
		root.style.setProperty('--nlpa-vh', Math.round(vv.height) + 'px');
	}
	if (window.visualViewport) { window.visualViewport.addEventListener('resize', kb); window.visualViewport.addEventListener('scroll', kb); }

	/* ---------- the form ---------- */
	var TYPO = { 'gmial.com': 'gmail.com', 'gmal.com': 'gmail.com', 'gmai.com': 'gmail.com', 'gamil.com': 'gmail.com', 'gmail.co': 'gmail.com', 'gmail.co.il': 'gmail.com', 'gmaill.com': 'gmail.com', 'hotmial.com': 'hotmail.com', 'hotmal.com': 'hotmail.com', 'hotmail.co': 'hotmail.com', 'walla.co': 'walla.co.il', 'wala.co.il': 'walla.co.il', 'walla.com': 'walla.co.il', 'yahooo.com': 'yahoo.com', 'yaho.com': 'yahoo.com', 'outlok.com': 'outlook.com', 'icloud.co': 'icloud.com' };
	function normPhone(s) {
		var d = String(s || '').replace(/\D+/g, '');
		if (d.indexOf('00972') === 0) { d = d.slice(5); } else if (d.indexOf('972') === 0) { d = d.slice(3); }
		if (d && d.charAt(0) !== '0') { d = '0' + d; }
		return /^05\d{8}$/.test(d) || /^0(?:[23489]|7\d)\d{7}$/.test(d) ? d : '';
	}
	function err(id, msg) {
		var p = card.querySelector('#' + id), f = p && p.previousElementSibling;
		if (p) { p.textContent = msg || ''; }
		if (f && f.tagName === 'INPUT') { f.setAttribute('aria-invalid', msg ? 'true' : 'false'); }
	}
	function wire() {
		var x = card.querySelector('.nlpa-x');
		x.addEventListener('click', function () { hide('button'); });
		[].forEach.call(card.querySelectorAll('.nlpa-later'), function (l) { l.addEventListener('click', function () { hide(card.getAttribute('data-step') === '3' ? 'done_close' : 'later'); }); });
		root.addEventListener('click', function (e) { if (desk && e.target === root) { hide('scrim'); } });
		[].forEach.call(card.querySelectorAll('.nlpa-chip'), function (c) {
			c.addEventListener('click', function () {
				interest = c.getAttribute('data-i') || '';
				[].forEach.call(card.querySelectorAll('.nlpa-chip'), function (o) { o.setAttribute('aria-pressed', o === c ? 'true' : 'false'); });
				ev('pa_step2', { pa_interest: interest });
				step(2);
			});
		});
		var f = card.querySelector('.nlpa-s2'), tel = card.querySelector('#nlpa-tel'), mail = card.querySelector('#nlpa-mail'), ok = card.querySelector('input[name="consent"]');
		var go = card.querySelector('.nlpa-go'), fe = card.querySelector('.nlpa-e--form'), t0 = 0;
		tel.addEventListener('focus', function () { if (!t0) { t0 = Date.now(); } });
		tel.addEventListener('blur', function () { if (tel.value && !normPhone(tel.value)) { err('nlpa-tel-e', 'מספר הטלפון לא נראה תקין. למשל: 050-1234567'); } else { err('nlpa-tel-e', ''); } });
		tel.addEventListener('input', function () { if (normPhone(tel.value)) { err('nlpa-tel-e', ''); } });
		mail.addEventListener('blur', function () {
			var v = mail.value.trim(), at = v.lastIndexOf('@'), dom = at > 0 ? v.slice(at + 1).toLowerCase() : '';
			if (v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { err('nlpa-mail-e', 'כתובת המייל לא נראית תקינה.'); return; }
			if (TYPO[dom]) {
				var fix = v.slice(0, at + 1) + TYPO[dom], p = card.querySelector('#nlpa-mail-e');
				p.textContent = ''; mail.setAttribute('aria-invalid', 'false');
				var q = document.createElement('button'), bd = document.createElement('bdi'); q.type = 'button'; q.className = 'nlpa-fix';
				bd.textContent = fix; q.appendChild(document.createTextNode('התכוונתם ל־')); q.appendChild(bd); q.appendChild(document.createTextNode('?'));
				q.addEventListener('click', function () { mail.value = fix; p.textContent = ''; mail.focus(); });
				p.appendChild(q);
				return;
			}
			err('nlpa-mail-e', '');
		});
		mail.addEventListener('input', function () { if (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim())) { err('nlpa-mail-e', ''); } });
		ok.addEventListener('change', function () { if (ok.checked) { err('nlpa-ok-e', ''); } });
		f.addEventListener('submit', function (e) {
			e.preventDefault();
			if (go.disabled) { return; }
			var ph = normPhone(tel.value), em = mail.value.trim(), bad = null;
			if (!ph) { err('nlpa-tel-e', tel.value ? 'מספר הטלפון לא נראה תקין. למשל: 050-1234567' : 'צריך מספר טלפון כדי לשלוח עדכונים.'); bad = bad || tel; }
			if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) { err('nlpa-mail-e', em ? 'כתובת המייל לא נראית תקינה.' : 'צריך כתובת מייל כדי לשלוח עדכונים.'); bad = bad || mail; }
			if (!ok.checked) { err('nlpa-ok-e', 'סמנו את האישור כדי שנוכל לשלוח לכם עדכונים.'); bad = bad || ok; }
			if (bad) { ev('pa_error', { pa_code: bad === tel ? 'phone' : bad === mail ? 'email' : 'consent' }); try { bad.focus(); } catch (x) {} return; }
			go.disabled = true; card.classList.add('is-sending'); fe.textContent = '';
			ev('pa_submit', { pa_interest: interest });
			var hp = card.querySelector('.nlpa-hp');
			fetch(C.api, {
				method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ id: C.id, phone: ph, email: em, consent: 1, interest: interest, trigger: trigger, v: C.v, company: hp ? hp.value : '', ms: t0 ? Date.now() - t0 : 0 })
			}).then(function (r) { return r.json().catch(function () { return { ok: false, error: 'net' }; }).then(function (j) { j.status = r.status; return j; }); })
				.then(function (j) {
					go.disabled = false; card.classList.remove('is-sending');
					if (j && j.ok) {
						ev('pa_done', { pa_interest: interest, pa_trigger: trigger });
						ev('generate_lead', { method: 'price_alert', lead_source: 'price_alert' });
						if (!PV) { LS.s('nlpa_done', String(Date.now() + 365 * DAY)); }
						step(3);
						return;
					}
					var c = (j && j.error) || 'net';
					ev('pa_error', { pa_code: c });
					if (c === 'phone') { err('nlpa-tel-e', 'מספר הטלפון לא נראה תקין. למשל: 050-1234567'); tel.focus(); }
					else if (c === 'email') { err('nlpa-mail-e', 'כתובת המייל לא נראית תקינה.'); mail.focus(); }
					else if (c === 'consent') { err('nlpa-ok-e', 'סמנו את האישור כדי שנוכל לשלוח לכם עדכונים.'); }
					else if (c === 'rate') { fe.textContent = 'נשלחו מכאן כמה הרשמות בזמן קצר. נסו שוב בעוד שעה.'; }
					else { fe.textContent = 'משהו השתבש בשליחה. נסו שוב בעוד רגע.'; }
				})
				.catch(function () { go.disabled = false; card.classList.remove('is-sending'); fe.textContent = 'אין חיבור כרגע. נסו שוב בעוד רגע.'; ev('pa_error', { pa_code: 'net' }); });
		});
		var wa = card.querySelector('.nlpa-wa');
		if (wa) { wa.addEventListener('click', function () { ev('pa_wa'); setTimeout(function () { hide('done_wa'); }, 300); }); }
		card.addEventListener('pointerdown', function () { touched = true; clearTimeout(ignT); });
		card.addEventListener('focusin', function () { touched = true; clearTimeout(ignT); });
		/* swipe down on the dark board closes the sheet on a phone */
		var board = card.querySelector('.nlpa-board');
		board.addEventListener('pointerdown', function (e) { if (desk || e.target.closest('button,a')) { return; } drag = { y0: e.clientY, t0: performance.now(), dy: 0 }; card.classList.add('is-drag'); try { board.setPointerCapture(e.pointerId); } catch (x) {} });
		board.addEventListener('pointermove', function (e) { if (!drag) { return; } var d = e.clientY - drag.y0; drag.dy = Math.max(0, d); card.style.transform = 'translateY(' + (d < 0 ? d * 0.2 : d) + 'px)'; });
		function end() {
			if (!drag) { return; }
			var h = card.offsetHeight, v = drag.dy / Math.max(1, performance.now() - drag.t0);
			card.classList.remove('is-drag');
			if (drag.dy > h * 0.3 || v > 0.5) { card.style.transform = 'translateY(' + (h + 40) + 'px)'; drag = null; hide('swipe'); }
			else { card.style.transform = ''; drag = null; }
		}
		board.addEventListener('pointerup', end); board.addEventListener('pointercancel', end);
		/* a modal on desktop keeps Tab inside */
		card.addEventListener('keydown', function (e) {
			if (e.key !== 'Tab' || !desk) { return; }
			var fs = [].filter.call(card.querySelectorAll('button,a[href],input:not(.nlpa-hp),[tabindex="0"]'), function (n) { return n.offsetParent !== null && !n.disabled; });
			if (!fs.length) { return; }
			var first = fs[0], last = fs[fs.length - 1];
			if (e.shiftKey && (document.activeElement === first || document.activeElement === card)) { e.preventDefault(); last.focus(); }
			else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
		});
	}
	document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && state === 'in') { hide('esc'); } });

	/* ---------- the signals ---------- */
	setInterval(function () { if (document.hidden || state !== 'idle') { return; } vis++; if (vis >= C.d && read()) { show('time'); } }, 1000);
	addEventListener('scroll', function () {
		var t = performance.now(), y = scrollY, d = depth();
		if (d > maxD) { maxD = d; }
		if (y > maxPx) { maxPx = y; }
		var v = (lastY - y) / Math.max(1, t - lastT);
		if (state === 'idle' && maxPx >= 1.5 * innerHeight && vis >= C.d && v > 1.2) { show('scroll_up'); }
		lastY = y; lastT = t;
	}, { passive: true });
	document.addEventListener('visibilitychange', function () {
		if (document.hidden) { awayAt = Date.now(); }
		else if (awayAt && Date.now() - awayAt >= 15000 && vis >= C.d) { show('tab_return'); }
	});
	document.addEventListener('mouseout', function (e) {
		if (!e.relatedTarget && e.clientY <= 0 && vis >= C.d && matchMedia('(pointer:fine)').matches) { show('leave_desktop'); }
	});
	/* a price in view for 2.5 s: the moment the reader is looking at money */
	if ('IntersectionObserver' in window) {
		var seen = null, io = new IntersectionObserver(function (es) {
			es.forEach(function (x) {
				if (x.isIntersecting && x.intersectionRatio >= 0.6) { if (!seen) { seen = setTimeout(function () { if (vis >= C.d) { show('price_view'); } seen = null; }, 2500); } }
				else if (seen) { clearTimeout(seen); seen = null; }
			});
		}, { threshold: [0, 0.6] });
		setTimeout(function () {
			var n = 0, all = document.querySelectorAll('main td, main dd, main strong, main b, .nlpjx-price, [id*="price"] strong, [class*="price"] b, [class*="price"] strong');
			for (var i = 0; i < all.length && n < 40; i++) {
				var s = all[i];
				if (s.closest && s.closest('#nlnu,#nlcta,header,footer,nav')) { continue; }
				var tx = s.textContent || '';
				if (tx.length < 40 && /₪/.test(tx) && /\d/.test(tx)) { io.observe(s); n++; }
			}
		}, 1500);
	}
	if (PV) { setTimeout(function () { show('preview'); }, 2000); }
})();
