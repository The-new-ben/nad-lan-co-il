/* nad-lan professionals' forum: reputation (inc/pro-forum-rep.php, Claude Design board 20). No library, no build step.
   A press on a stars chip, a leader row or "הכוכבים שלי" opens the member's sheet (part ב), filled from the public read
   GET forum/rep/member; any [data-nlfr-rules] opens the rules (part ד), which the server printed as real HTML. The numbers
   come from window.NLFR (the same PHP functions that count). People's text enters the page only through textContent.
   Native modal dialogs: focus stays inside, Escape closes, focus returns to the button that opened the sheet. */
(function () {
	'use strict';
	var C = window.NLF || {}, R = window.NLFR || {};
	var MAX = R.max || 5;
	var $ = function (s, r) { return (r || document).querySelector(s); };
	var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
	var sheet = $('#nlfr-member'), rules = $('#nlfr-rules');
	if (!sheet && !rules) { return; }
	var ERR = 'משהו השתבש. נסו שוב.';

	function el(tag, cls, text) { var x = document.createElement(tag); if (cls) { x.className = cls; } if (text != null) { x.textContent = text; } return x; }
	function num(n) { return Number(n || 0).toLocaleString('he-IL'); }
	function stars(n) { var s = ''; for (var i = 0; i < Math.max(0, Math.min(MAX, n | 0)); i++) { s += '★'; } return s; }

	/* dialogs: native showModal (focus kept inside, Escape closes); a fallback for old browsers */
	function openDlg(d, opener) {
		if (!d) { return; }
		d._ret = opener || document.activeElement;
		if (d.showModal) { if (!d.open) { d.showModal(); } } else { d.setAttribute('open', ''); }
	}
	function closeDlg(d) {
		if (!d) { return; }
		if (d.close) { if (d.open) { d.close(); } } else { d.removeAttribute('open'); back(d); }
	}
	function back(d) { var r = d._ret; d._ret = null; if (r && r.focus && document.contains(r)) { r.focus(); } }
	[sheet, rules].forEach(function (d) {
		if (!d) { return; }
		d.addEventListener('close', function () { back(d); });
		d.addEventListener('click', function (e) { if (e.target === d) { closeDlg(d); } });
		$$('[data-nlf-close]', d).forEach(function (b) { b.addEventListener('click', function () { closeDlg(d); }); });
		if (!d.showModal) { d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeDlg(d); } }); }
	});

	/* part ד: the rules; the viewer's own level (or the open sheet's member) is marked among the five tiles */
	function openRules(opener) {
		if (!rules) { return; }
		var lv = -1;
		if (sheet && sheet.open && sheet._lv != null) { lv = sheet._lv; }
		else { var mine = $('.nlfr-mine[data-nlfr-level]'); if (mine) { lv = +mine.getAttribute('data-nlfr-level'); } }
		$$('[data-nlfr-tile]', rules).forEach(function (t) { t.classList.toggle('is-on', +t.getAttribute('data-nlfr-tile') === lv); });
		openDlg(rules, opener);
		var x = $('[data-nlf-close]', rules); if (x) { x.focus(); }
	}

	/* part ב: the member's sheet */
	function paint(j) {
		var m = j.member || {}, r = j.rep || {}, body = $('[data-nlfr-body]', sheet);
		sheet._lv = r.stars | 0;
		$('#nlfr-m-h', sheet).textContent = m.name || '';
		$('[data-nlfr-sub]', sheet).textContent = m.sub || '';
		var av = $('[data-nlfr-av]', sheet);
		av.textContent = m.initials || '';
		av.classList.toggle('nlf-av-sq', !!m.sq);
		av.style.setProperty('--nlf-bg', m.bg || '#E3E6E8'); av.style.setProperty('--nlf-fg', m.fg || '#22303A');
		body.textContent = '';
		var dark = el('div', 'nlfr-dark'), top = el('div', 'nlfr-dark-top');
		var big = el('span', 'nlfr-big', stars(r.stars)); big.setAttribute('aria-hidden', 'true');
		var off = el('i', '', stars(MAX - (r.stars | 0))); big.appendChild(off);
		top.appendChild(big);
		top.appendChild(el('span', 'nlfr-dark-lv', r.level || ''));
		var pt = el('span', 'nlfr-dark-pt', num(r.points) + ' '); pt.appendChild(el('small', '', 'נקודות')); top.appendChild(pt);
		top.appendChild(el('span', 'nlfr-sr', r.label || ''));
		dark.appendChild(top);
		var bar = el('div', 'nlfr-bar'), fill = el('i'); bar.setAttribute('aria-hidden', 'true'); fill.style.width = Math.max(0, Math.min(100, r.pct | 0)) + '%';
		bar.appendChild(fill); dark.appendChild(bar);
		dark.appendChild(el('span', 'nlfr-dark-tx', r.text || ''));
		body.appendChild(dark);
		var ul = el('ul', 'nlfr-rows');
		(j.rows || []).forEach(function (x) {
			var li = el('li');
			li.appendChild(el('span', '', x.label));
			li.appendChild(el('b', '', num(x.n)));
			li.appendChild(el('span', 'nlfr-pts-c', num(x.pts) + " נק'"));
			ul.appendChild(li);
		});
		body.appendChild(ul);
	}
	function openMember(id, opener) {
		if (!sheet || !C.rest || !window.fetch) { return; }
		var msg = $('[data-nlfr-msg]', sheet), body = $('[data-nlfr-body]', sheet);
		msg.textContent = ''; msg.classList.remove('is-err');
		$('#nlfr-m-h', sheet).textContent = 'כוכבים ודרגה';
		$('[data-nlfr-sub]', sheet).textContent = '';
		$('[data-nlfr-av]', sheet).textContent = '';
		sheet._lv = null;
		body.textContent = '';
		body.appendChild(el('p', 'nlfr-wait', 'טוען...'));
		openDlg(sheet, opener);
		var x = $('[data-nlf-close]', sheet); if (x) { x.focus(); }
		var o = { credentials: 'same-origin', headers: { Accept: 'application/json' } };
		if (C.wpnonce) { o.headers['X-WP-Nonce'] = C.wpnonce; }
		fetch(C.rest + 'rep/member?id=' + encodeURIComponent(id), o).then(function (res) {
			return res.json().catch(function () { return {}; }).then(function (j) {
				if (!res.ok || !j || j.ok !== 1) { throw new Error((j && j.message) || ERR); }
				return j;
			});
		}).then(paint).catch(function (er) {
			body.textContent = '';
			msg.textContent = er.message || ERR; msg.classList.add('is-err');
		});
	}

	document.addEventListener('click', function (e) {
		var t = e.target.closest && e.target.closest('[data-nlfr-rules],[data-nlfr-member]');
		if (!t) { return; }
		e.preventDefault();
		if (t.hasAttribute('data-nlfr-rules')) { openRules(t); return; }
		var id = +t.getAttribute('data-nlfr-member');
		if (id > 0) { openMember(id, t); }
	});
	if (window.location.hash === '#nlfr-rules') { openRules(null); }
})();
