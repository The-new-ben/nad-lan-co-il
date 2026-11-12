/* nad-lan professionals' forum: the social layer (inc/pro-forum-social.php, Claude Design board 11). No library.
   The five reactions and the private "לא עזר לי", the member sheet (פרגונים, skills, the response badge), the פרגון form,
   one-tap skill confirmations, and "עבדו יחד" tags on a finished work. Every write solves the forum's proof-of-work
   challenge and sends the forum's session nonce, exactly as forum.js does. People's text enters the page only through
   textContent. WhatsApp opens wa.me with no number: the person picks the recipient. Nothing is sent by itself. */
(function () {
	'use strict';
	var C = window.NLF || {}, S = window.NLFS || {};
	if (!C.rest || !window.fetch) { return; }
	var KINDS = S.kinds || {}, RELS = S.rels || {};
	var st = { member: null, nonce: '', ch: '', ts: '' };
	var ERR = 'משהו השתבש. נסו שוב.';
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

	/* a signed-in member, or the forum's own one-step entry (forum.js opens it and reloads the page after the code) */
	function needMember() {
		return ready.then(function () {
			if (st.member) { return st.member; }
			var b = document.createElement('button');
			b.type = 'button'; b.hidden = true; b.setAttribute('data-nlf-enter', '');
			document.body.appendChild(b); b.click(); b.remove();
			var e = new Error(''); e.code = 'cancel'; throw e;
		});
	}
	function write(path, data, form, retried) {
		return needMember().then(function () { return st.ch ? null : loadState(); }).then(function () {
			var trap = form && form.querySelector('[name="website"]');
			return solve(st.ch).then(function (n) {
				return req('POST', 'social/' + path, Object.assign({}, data, { ch: st.ch, n: n, ts: st.ts, website: trap ? trap.value : '' }));
			});
		}).catch(function (e) {
			if (retried || e.code === 'cancel') { throw e; }
			if (e.code === 'nlf_ts' && /רגע/.test(e.message)) { return wait(3200).then(function () { return write(path, data, form, true); }); }
			if (e.code === 'nlf_nonce' || e.code === 'nlf_pow') { return loadState().then(function () { return write(path, data, form, true); }); }
			if (e.code === 'nlf_need_entry') { st.member = null; return needMember(); }
			throw e;
		});
	}
	function say(el, msg, err) { if (!el) { return; } el.textContent = msg || ''; el.classList.toggle('is-err', !!err); }
	function busy(b, on) { if (b) { b.disabled = !!on; b.setAttribute('aria-busy', on ? 'true' : 'false'); } }
	function msgNear(el) {
		var box = el && el.closest('[data-nlfs-team],.nlfs-skills,.nlfs-mb,#nlfs-member,.nlf-reply,.nlf-op,.nlf');
		return (box && $('.nlfs-msg,[data-nlfs-sheetmsg],.nlf-live', box)) || $('#nlf-live');
	}
	function fail(el) { return function (er) { if (er.code !== 'cancel') { say(msgNear(el), er.message, true); } }; }
	function el(tag, cls, text) { var x = document.createElement(tag); if (cls) { x.className = cls; } if (text != null) { x.textContent = text; } return x; }
	var SVGNS = 'http://www.w3.org/2000/svg';
	function icon(d) {
		var s = document.createElementNS(SVGNS, 'svg'), p = document.createElementNS(SVGNS, 'path');
		s.setAttribute('width', '14'); s.setAttribute('height', '14'); s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('fill', 'none');
		s.setAttribute('stroke', 'currentColor'); s.setAttribute('stroke-width', '3'); s.setAttribute('stroke-linecap', 'round'); s.setAttribute('stroke-linejoin', 'round');
		s.setAttribute('aria-hidden', 'true'); s.setAttribute('focusable', 'false'); p.setAttribute('d', d); s.appendChild(p); return s;
	}
	var CHECK = 'M4 12l5 5L20 6', CROSS = 'M6 6l12 12M18 6L6 18';
	function num(n) { return Number(n).toLocaleString('he-IL'); }

	/* ---------------- reactions (board 11 pills, stacked dots, the total) ---------------- */
	function closePick(rx) {
		var p = $('.nlfs-pick', rx), b = $('[data-nlfs-rx-open]', rx);
		if (p) { p.hidden = true; } if (b) { b.setAttribute('aria-expanded', 'false'); }
		rx.classList.remove('is-open');
	}
	function paintRx(rx, j) {
		var b = $('[data-nlfs-rx-open]', rx), k = KINDS[j.mine];
		rx.setAttribute('data-mine', j.mine || '');
		if (b) {
			b.textContent = k ? k[0] : 'מפרגן';
			b.classList.toggle('is-on', !!k);
			if (k) { b.style.setProperty('--nlfs-bg', k[1]); b.style.setProperty('--nlfs-fg', k[2]); } else { b.removeAttribute('style'); }
		}
		$$('[data-nlfs-kind]', rx).forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-nlfs-kind') === j.mine ? 'true' : 'false'); });
		var sum = $('[data-nlfs-sum]', rx), dots = $('.nlfs-dots', sum);
		dots.textContent = '';
		(j.top || []).forEach(function (t) { var i = document.createElement('i'); if (KINDS[t]) { i.style.background = KINDS[t][3]; } dots.appendChild(i); });
		$('.nlfs-total', sum).textContent = j.total > 0 ? num(j.total) : '';
		$('.nlfs-sr', sum).textContent = j.words || '';
		sum.hidden = !(j.total > 0);
	}
	document.addEventListener('click', function (e) {
		var open = e.target.closest('[data-nlfs-rx-open]');
		$$('.nlfs-rx.is-open').forEach(function (rx) { if (!open || rx !== open.closest('.nlfs-rx')) { closePick(rx); } });
		if (open) {
			var rx = open.closest('.nlfs-rx'), p = $('.nlfs-pick', rx), show = p.hidden;
			p.hidden = !show; open.setAttribute('aria-expanded', show ? 'true' : 'false'); rx.classList.toggle('is-open', show);
			if (show) { var f = $('[aria-pressed="true"]', p) || $('[data-nlfs-kind]', p); if (f) { f.focus(); } }
			return;
		}
		var kb = e.target.closest('[data-nlfs-kind]');
		if (kb) {
			var r = kb.closest('.nlfs-rx');
			busy(kb, true);
			write('react', { type: r.getAttribute('data-nlfs-rx'), id: +r.getAttribute('data-id'), kind: kb.getAttribute('data-nlfs-kind') }).then(function (j) {
				paintRx(r, j); closePick(r); var ob = $('[data-nlfs-rx-open]', r); if (ob) { ob.focus(); }
			}).catch(fail(r)).then(function () { busy(kb, false); });
			return;
		}
		var u = e.target.closest('[data-nlfs-unhelpful]');
		if (u) {
			busy(u, true);
			write('unhelpful', { id: +u.getAttribute('data-nlfs-unhelpful') }).then(function (j) {
				u.setAttribute('aria-pressed', j.on ? 'true' : 'false'); u.classList.toggle('is-on', !!j.on); say(msgNear(u), j.message);
			}).catch(fail(u)).then(function () { busy(u, false); });
		}
	});
	document.addEventListener('keydown', function (e) {
		if (e.key !== 'Escape') { return; }
		var rx = e.target.closest && e.target.closest('.nlfs-rx.is-open');
		if (rx) { closePick(rx); var b = $('[data-nlfs-rx-open]', rx); if (b) { b.focus(); } }
	});

	/* ---------------- the member sheet ---------------- */
	var sheet = $('#nlfs-member'), body = sheet && $('[data-nlfs-body]', sheet), kform = sheet && $('[data-nlfs-kudosform]', sheet);
	var cur = { id: 0, data: null };
	function openDlg(d) { d._ret = document.activeElement; if (d.showModal) { if (!d.open) { d.showModal(); } } else { d.setAttribute('open', ''); } }
	function closeDlg(d) { if (d.close) { if (d.open) { d.close(); } } else { d.removeAttribute('open'); } if (d._ret && d._ret.focus) { d._ret.focus(); } }
	if (sheet) {
		$$('[data-nlf-close]', sheet).forEach(function (b) { b.addEventListener('click', function () { closeDlg(sheet); }); });
		sheet.addEventListener('click', function (e) { if (e.target === sheet) { closeDlg(sheet); } });
	}
	function kudoCard(k, d) {
		var a = el('article', 'nlfs-kudo'); a.setAttribute('data-nlfs-kudo', k.id); if (k.hidden) { a.setAttribute('data-hidden', '1'); }
		a.appendChild(el('span', 'nlfs-kudo-tag', 'פרגון' + (k.rel ? ' · ' + k.rel : '')));
		a.appendChild(el('p', 'nlfs-kudo-q', '"' + k.text + '"'));
		a.appendChild(el('span', 'nlfs-kudo-by', 'מאת ' + k.from.name + (k.from.label ? ', ' + k.from.label : '') + ', על ' + k.to.name + (k.to.label ? ', ' + k.to.label : '')));
		var row = el('div', 'nlfs-kudo-b'), wa = el('a', 'nlfs-kudo-wa', 'שלחו בוואטסאפ');
		wa.href = k.wa; wa.target = '_blank'; wa.rel = 'noopener';
		row.appendChild(wa);
		if (k.mine) {
			var h = el('button', 'nlfs-kudo-alt', k.hidden ? 'להחזיר לפרופיל' : 'הסתרה מהפרופיל'); h.type = 'button';
			h.setAttribute('data-nlfs-kudo-hide', k.id); h.setAttribute('aria-pressed', k.hidden ? 'true' : 'false'); row.appendChild(h);
		} else if (d.viewer !== k.from.id) {
			var g = el('button', 'nlfs-kudo-alt', 'גם אני מפרגן'); g.type = 'button'; g.setAttribute('data-nlfs-kudos-open', k.to.id); row.appendChild(g);
		}
		a.appendChild(row);
		return a;
	}
	function skillsBox(d) {
		var own = !!d.own, m = d.member;
		if (!d.skills.length && !(own && m.trade)) { return null; }
		var s = el('section', 'nlfs-skills'); s.setAttribute('data-nlfs-skills', m.id);
		s.appendChild(el('h3', 'nlfs-h', own ? 'המיומנויות שלי' : 'מכירים את העבודה של ' + m.first + '?'));
		s.appendChild(el('span', 'nlfs-sub', own ? 'עד 5 מיומנויות. משתתפים אחרים מאשרים אותן בלחיצה.' : 'אשרו מיומנות אחת בלחיצה. האישור מופיע בפרופיל שלו בפורום.'));
		var w = el('div', 'nlfs-chips');
		d.skills.forEach(function (k) {
			var tx = k.label + (k.n > 0 ? ' · ' + num(k.n) : '');
			if (own) {
				var c = el('span', 'nlfs-skill is-own', tx);
				if (k.status === 'pending') { c.appendChild(el('em', '', 'ממתינה לבדיקה')); }
				var x = el('button', 'nlfs-chip-x'); x.type = 'button'; x.setAttribute('data-nlfs-skill-del', k.id); x.setAttribute('aria-label', 'הסרת ' + k.label); x.appendChild(icon(CROSS));
				c.appendChild(x); w.appendChild(c);
			} else {
				var b = el('button', 'nlfs-skill' + (k.mine ? ' is-on' : '')); b.type = 'button';
				b.setAttribute('data-nlfs-endorse', k.id); b.setAttribute('data-label', k.label); b.setAttribute('aria-pressed', k.mine ? 'true' : 'false');
				if (k.mine) { b.appendChild(icon(CHECK)); }
				b.appendChild(el('span', '', tx)); w.appendChild(b);
			}
		});
		s.appendChild(w);
		if (own && d.skills.length < 5) {
			var f = el('form', 'nlfs-skill-add'); f.setAttribute('data-nlfs-skill-add', ''); f.noValidate = true;
			var lb = el('label', 'nlfs-sr', 'מיומנות חדשה'), inp = el('input'), sb = el('button', 'nlf-btn nlf-btn-line', 'הוספה');
			lb.htmlFor = 'nlfs-sk-sheet'; inp.id = 'nlfs-sk-sheet'; inp.type = 'text'; inp.name = 'label'; inp.maxLength = 40; inp.placeholder = 'למשל: שמאות לבנק'; inp.autocomplete = 'off';
			sb.type = 'submit';
			var trap = el('div', 'nlf-trap'), ti = el('input'); trap.setAttribute('aria-hidden', 'true'); ti.type = 'text'; ti.name = 'website'; ti.tabIndex = -1; ti.autocomplete = 'off'; trap.appendChild(ti);
			f.appendChild(lb); f.appendChild(inp); f.appendChild(sb); f.appendChild(trap); s.appendChild(f);
		}
		var msg = el('p', 'nlfs-msg'); msg.setAttribute('role', 'status'); msg.setAttribute('aria-live', 'polite'); s.appendChild(msg);
		return s;
	}
	var BLOCK = { guest: '', self: '', posts: 'פרגון אפשר לכתוב אחרי שתי הודעות שאושרו בפורום.', done: 'כבר פרגנתם לו. פרגון אחד לכל אחד.' };
	function paintSheet(d) {
		var m = d.member;
		cur.data = d;
		$('#nlfs-m-h').textContent = d.own ? 'הפרופיל שלי בפורום' : m.name;
		body.textContent = '';
		var head = el('div', 'nlfs-head'), av = el('span', 'nlf-av nlf-av-lg nlf-av-sq', (m.name || '?').trim().slice(0, 1));
		av.style.setProperty('--nlf-bg', m.bg); av.style.setProperty('--nlf-fg', m.fg); av.setAttribute('aria-hidden', 'true');
		var col = el('div', 'nlfs-head-c'), nm = el('span', 'nlfs-head-n', m.name);
		col.appendChild(nm);
		if (m.label) { col.appendChild(el('span', 'nlf-sub', m.label)); }
		if (m.badge) { var bd = el('span', 'nlfs-badge'); bd.appendChild(icon(CHECK)); bd.appendChild(document.createTextNode('עונה בדרך כלל תוך יום')); col.appendChild(bd); }
		head.appendChild(av); head.appendChild(col); body.appendChild(head);
		if (d.kudos.length) {
			if (d.own) { body.appendChild(el('h3', 'nlfs-h', 'הפרגונים עליי')); }
			d.kudos.forEach(function (k) { body.appendChild(kudoCard(k, d)); });
		} else if (d.own) {
			body.appendChild(el('p', 'nlf-sub', 'עוד אין פרגונים עליכם. מי שעבד איתכם יכול לפרגן מכאן.'));
		}
		if (!d.own) {
			var cta = el('div', 'nlfs-cta');
			cta.appendChild(el('span', '', d.kudos.length ? 'גם אתם מכירים את העבודה של ' + m.first + '?' : 'מכירים את העבודה של ' + m.first + '?'));
			var b = el('button', 'nlf-btn nlf-btn-line', d.kudos.length ? 'גם אני מפרגן' : 'פרגנו ל' + m.first); b.type = 'button'; b.setAttribute('data-nlfs-kudos-open', m.id);
			cta.appendChild(b); body.appendChild(cta);
		}
		var sk = skillsBox(d); if (sk) { body.appendChild(sk); }
		if (m.url && !/#nlfs-m/.test(m.url)) { var a = el('a', 'nlfs-card-link', 'לכרטיס של ' + m.first); a.href = m.url; body.appendChild(a); }
	}
	function loadSheet(id) {
		return ready.then(function () { return req('GET', 'social/member', { id: id }); }).then(function (j) { cur.id = id; paintSheet(j); return j; });
	}
	function openSheet(id, withForm) {
		if (!sheet) { return; }
		say($('[data-nlfs-sheetmsg]', sheet), '');
		kform.hidden = true;
		body.textContent = '';
		body.appendChild(el('p', 'nlf-sub', 'טוען...'));
		openDlg(sheet);
		loadSheet(id).then(function (d) {
			if (withForm) { showForm(d); }
			var f = $('button,a', body); if (f && !withForm) { f.focus(); }
		}).catch(function (er) { body.textContent = ''; say($('[data-nlfs-sheetmsg]', sheet), er.message, true); });
	}
	function showForm(d) {
		var msg = $('[data-nlfs-sheetmsg]', sheet);
		if (d.block === 'guest') { closeDlg(sheet); needMember().catch(function () {}); return; }
		if (d.block === 'self') { return; }
		if (BLOCK[d.block]) { say(msg, BLOCK[d.block], true); return; }
		kform.reset();
		$('[data-nlfs-kh]', kform).textContent = 'פרגון ל' + d.member.name;
		$('[data-nlfs-kcount]', kform).textContent = '';
		kform.hidden = false;
		var r = $('input[name="rel"]', kform); if (r) { r.focus(); }
	}
	if (kform) {
		var tb = kform.elements.body, cnt = $('[data-nlfs-kcount]', kform);
		tb.addEventListener('input', function () { var n = tb.value.trim().length; cnt.textContent = n ? n + ' מתוך 240' : ''; });
		kform.addEventListener('submit', function (e) {
			e.preventDefault();
			var msg = $('[data-nlfs-sheetmsg]', sheet), btn = $('button[type="submit"]', kform), rel = kform.querySelector('input[name="rel"]:checked'), text = tb.value.trim();
			if (!rel) { say(msg, 'בחרו איך אתם מכירים.', true); return; }
			if (text.length < 10) { say(msg, 'כתבו משפט, לפחות 10 תווים.', true); tb.focus(); return; }
			busy(btn, true); say(msg, 'שולחים...');
			write('kudos', { to: cur.id, rel: rel.value, body: text }, kform).then(function (j) {
				kform.hidden = true; say(msg, j.message);
				return loadSheet(cur.id);
			}).catch(function (er) { if (er.code !== 'cancel') { say(msg, er.message, true); } }).then(function () { busy(btn, false); });
		});
	}
	/* a name in a discussion opens the member's sheet (a joined professional's name keeps its link to his card) */
	$$('[data-nlfs-mid]').forEach(function (mk) {
		var who = mk.parentNode && $('.nlf-who', mk.parentNode);
		if (!who || who.tagName === 'A') { return; }
		who.setAttribute('role', 'button'); who.tabIndex = 0; who.setAttribute('aria-haspopup', 'dialog');
		who.classList.add('nlfs-who'); who.setAttribute('data-nlfs-member', mk.getAttribute('data-nlfs-mid'));
		who.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); who.click(); } });
	});
	document.addEventListener('click', function (e) {
		var o = e.target.closest('[data-nlfs-member],[data-nlfs-kudos-open]');
		if (!o) { return; }
		e.preventDefault();
		if (o.hasAttribute('data-nlfs-kudos-open')) {
			var id = +o.getAttribute('data-nlfs-kudos-open');
			if (sheet && sheet.open && cur.id === id && cur.data) { showForm(cur.data); return; }
			openSheet(id, true);
			return;
		}
		openSheet(+o.getAttribute('data-nlfs-member'), false);
	});
	var hm = /^#nlfs-m(\d+)$/.exec(window.location.hash);
	if (hm && sheet) { openSheet(+hm[1], false); }

	/* ---------------- my פרגונים, skills and confirmations ---------------- */
	function refresh(from) { if (sheet && sheet.contains(from) && cur.id) { return loadSheet(cur.id); } window.location.reload(); return null; }
	document.addEventListener('click', function (e) {
		var h = e.target.closest('[data-nlfs-kudo-hide]');
		if (h) {
			var hide = h.getAttribute('aria-pressed') !== 'true';
			busy(h, true);
			write('kudos-hide', { id: +h.getAttribute('data-nlfs-kudo-hide'), hide: hide ? '1' : '0' }).then(function (j) {
				h.setAttribute('aria-pressed', j.hidden ? 'true' : 'false'); h.textContent = j.hidden ? 'להחזיר לפרופיל' : 'הסתרה מהפרופיל';
				var card = h.closest('.nlfs-kudo'); if (card) { if (j.hidden) { card.setAttribute('data-hidden', '1'); } else { card.removeAttribute('data-hidden'); } }
				say(msgNear(h), j.message);
			}).catch(fail(h)).then(function () { busy(h, false); });
			return;
		}
		var en = e.target.closest('[data-nlfs-endorse]');
		if (en) {
			busy(en, true);
			write('endorse', { id: +en.getAttribute('data-nlfs-endorse') }).then(function (j) {
				en.setAttribute('aria-pressed', j.on ? 'true' : 'false'); en.classList.toggle('is-on', !!j.on);
				en.textContent = '';
				if (j.on) { en.appendChild(icon(CHECK)); }
				en.appendChild(el('span', '', en.getAttribute('data-label') + (j.n > 0 ? ' · ' + num(j.n) : '')));
			}).catch(fail(en)).then(function () { busy(en, false); });
			return;
		}
		var del = e.target.closest('[data-nlfs-skill-del]');
		if (del) {
			busy(del, true);
			write('skill-remove', { id: +del.getAttribute('data-nlfs-skill-del') }).then(function () { return refresh(del); }).catch(fail(del)).then(function () { busy(del, false); });
		}
	});
	document.addEventListener('submit', function (e) {
		var f = e.target.closest && e.target.closest('[data-nlfs-skill-add]');
		if (!f) { return; }
		e.preventDefault();
		var v = f.elements.label.value.trim(), btn = $('button[type="submit"]', f);
		if (v.length < 2) { say(msgNear(f), 'כתבו מיומנות, לפחות 2 תווים.', true); f.elements.label.focus(); return; }
		busy(btn, true);
		write('skill', { label: v }, f).then(function (j) {
			say(msgNear(f), j.message);
			return wait(900).then(function () { return refresh(f); });
		}).catch(fail(f)).then(function () { busy(btn, false); });
	});

	/* ---------------- "עבדו יחד": tags on a finished work ---------------- */
	var fTimer = null;
	function found(box, items) {
		var ul = $('[data-nlfs-found]', box);
		ul.textContent = '';
		items.forEach(function (it) {
			var li = el('li'), b = el('button', 'nlfs-found-b', it.name + (it.label ? ' · ' + it.label : ''));
			b.type = 'button'; b.setAttribute('data-nlfs-tag', it.id);
			li.appendChild(b); ul.appendChild(li);
		});
		if (!items.length) { ul.appendChild(el('li', 'nlf-sub', 'לא מצאנו משתתף בשם הזה בפורום.')); }
	}
	document.addEventListener('input', function (e) {
		var inp = e.target.closest && e.target.closest('[data-nlfs-find]');
		if (!inp) { return; }
		var box = inp.closest('.nlfs-find'), q = inp.value.trim();
		clearTimeout(fTimer);
		if (q.length < 2) { $('[data-nlfs-found]', box).textContent = ''; return; }
		fTimer = setTimeout(function () {
			ready.then(function () { return req('GET', 'social/find', { q: q }); }).then(function (j) { found(box, j.items || []); }).catch(fail(inp));
		}, 350);
	});
	document.addEventListener('click', function (e) {
		var op = e.target.closest('[data-nlfs-tag-open]');
		if (op) {
			var fb = document.getElementById(op.getAttribute('aria-controls')), show = fb.hidden;
			fb.hidden = !show; op.setAttribute('aria-expanded', show ? 'true' : 'false');
			if (show) { $('[data-nlfs-find]', fb).focus(); }
			return;
		}
		var tg = e.target.closest('[data-nlfs-tag]');
		if (tg) {
			var team = tg.closest('[data-nlfs-team]');
			busy(tg, true);
			write('tag', { topic: +team.getAttribute('data-nlfs-team'), member: +tg.getAttribute('data-nlfs-tag') }).then(function (j) {
				say(msgNear(team), j.message);
				return wait(900).then(function () { window.location.reload(); });
			}).catch(fail(team)).then(function () { busy(tg, false); });
			return;
		}
		var ut = e.target.closest('[data-nlfs-untag]');
		if (ut) {
			var tm = ut.closest('[data-nlfs-team]');
			busy(ut, true);
			write('untag', { topic: +tm.getAttribute('data-nlfs-team'), member: +ut.getAttribute('data-nlfs-untag') }).then(function (j) {
				var gone = ut.closest('.nlfs-chip') || ut.closest('li');
				say(msgNear(tm), j.message);
				if (gone && gone.tagName !== 'LI') { gone.remove(); } else if (gone) { ut.remove(); }
			}).catch(fail(tm)).then(function () { busy(ut, false); });
		}
	});
})();
