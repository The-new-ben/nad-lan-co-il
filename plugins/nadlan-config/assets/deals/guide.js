/* HAD-743 + HAD-682: the guide of the developer deals map (nad-lan.co.il /developer-deals/, Claude Design canvas board 13).
   A small computer-made face that reacts to what the visitor does on THIS page (cash, deal, pause, return visit), says one true
   fact from the published deal, what is worth checking, that she does not recommend, and then acts through window.NLDM.
   Data: window.NLDG (inc/deals-guide.php). Every line is fixed text; a recorded clip plays only when the server says it matches.
   Rules kept in code: sound only after a tap; at most one unasked line every 40 s and three a visit; never while scrolling or
   typing; one tap closes her for good (a small face stays); nothing leaves the device (the return-visit memory is localStorage). */
(function () {
	'use strict';
	var G = window.NLDG;
	if (!G || !G.lines || !document.body) { return; }
	var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	var LS = {
		get: function (k) { try { return JSON.parse(window.localStorage.getItem(k)); } catch (e) { return null; } },
		set: function (k, v) { try { window.localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
	};
	var now = function () { return Date.now(); };
	var st = { closed: !!LS.get('nldg-closed'), muted: !!LS.get('nldg-muted'), unlocked: false, panel: false, lastPro: 0, pro: 0,
		lastReact: 0, react: 0, onceDone: {}, saidNr: false, lastScroll: 0, lastAct: now(), cashT: 0, cashMoved: false, picked: null };
	var api = null;
	var lineText = function (id) { return G.lines[id] ? G.lines[id][0] : ''; };
	var lineClip = function (id) { return G.lines[id] && G.lines[id][1] ? G.lines[id][1] : ''; };

	/* ---------- the face, the bubble, the panel ---------- */
	var el = function (tag, cls, txt) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (txt != null) { e.textContent = txt; } return e; };
	var wrap = el('div', 'nldg' + (st.closed ? ' is-mini' : '')); wrap.dir = 'rtl';
	var face = el('button', 'nldg-face'); face.type = 'button';
	face.setAttribute('aria-label', 'המדריכה של מפת המבצעים, דמות ממוחשבת. לחצו כדי לשאול אותה');
	var img = el('span', 'nldg-img');
	var fBase = el('img'), fB = el('img', 'm b'), fC = el('img', 'm c'), fK = el('img', 'k');
	[fBase, fB, fC, fK].forEach(function (i, n) { i.src = G.face[n]; i.alt = ''; i.decoding = 'async'; i.draggable = false; img.appendChild(i); });
	face.appendChild(img);
	var bars = el('span', 'nldg-bars'); bars.innerHTML = '<i></i><i></i><i></i>'; bars.setAttribute('aria-hidden', 'true');
	face.appendChild(bars);

	var bub = el('div', 'nldg-bub'); bub.setAttribute('role', 'status'); bub.setAttribute('aria-live', 'polite'); bub.hidden = true;
	var bSay = el('p', 'nldg-say'), bChk = el('p', 'nldg-chk'), bActs = el('div', 'nldg-acts'), bMeta = el('p', 'nldg-meta', 'דמות ממוחשבת · לא ממליצה על מבצע מסוים · זה לא ייעוץ');
	var bX = el('button', 'nldg-bx', '×'); bX.type = 'button'; bX.setAttribute('aria-label', 'הסתרת ההודעה');
	bChk.hidden = true;
	[bX, bSay, bChk, bActs, bMeta].forEach(function (n) { bub.appendChild(n); });

	var pan = el('div', 'nldg-pan'); pan.hidden = true; pan.setAttribute('role', 'dialog'); pan.setAttribute('aria-label', 'שאלו את המדריכה על מבצעי הקבלנים');
	pan.innerHTML = '<div class="nldg-ph"><b>על מה לספר לכם?</b><span>השאלות משתנות לפי מה שעשיתם בעמוד</span><button type="button" class="nldg-pc" aria-label="סגירה">×</button></div>' +
		'<div class="nldg-ans" aria-live="polite" hidden><p class="nldg-say"></p><p class="nldg-chk" hidden></p><div class="nldg-acts"></div></div>' +
		'<form class="nldg-lead" autocomplete="on" hidden novalidate><b class="nldg-lh">השאירו פרטים, ונחזור אליכם</b><span class="nldg-lt"></span>' +
		'<label for="nldg-ln">השם שלכם</label><input id="nldg-ln" name="name" type="text" maxlength="60" autocomplete="name" required>' +
		'<label for="nldg-lp">טלפון נייד</label><input id="nldg-lp" name="phone" type="tel" inputmode="tel" maxlength="14" autocomplete="tel" dir="ltr" placeholder="05X-XXXXXXX" required>' +
		'<input class="nldg-sr" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">' +
		'<p class="nldg-lc"></p><p class="nldg-lm" role="status" aria-live="polite"></p><button type="submit" class="nldg-ls">שלחו, ונחזור אליכם</button></form>' +
		'<div class="nldg-chips"></div>' +
		'<form class="nldg-ask" autocomplete="off"><label class="nldg-sr" for="nldg-q">שאלה למדריכה</label><input id="nldg-q" name="q" type="text" maxlength="160" placeholder="כתבו שאלה, למשל: מה זה 20/80?" enterkeyhint="send"><button type="button" class="nldg-mic" aria-label="שאלו בקול" hidden>דברו</button><button type="submit" class="nldg-go" aria-label="שליחה">שאלו</button></form>' +
		'<div class="nldg-pf"><button type="button" class="nldg-tolead">השאירו פרטים</button><button type="button" class="nldg-mute"></button><button type="button" class="nldg-off">הסתירו אותה</button><span>דמות ממוחשבת · זה לא ייעוץ · שאלה בקול הופכת לטקסט בדפדפן ולא נשמרת</span></div>';
	var pAns = pan.querySelector('.nldg-ans'), pSay = pAns.querySelector('.nldg-say'), pChk = pAns.querySelector('.nldg-chk'), pActs = pAns.querySelector('.nldg-acts');
	var pChips = pan.querySelector('.nldg-chips'), pForm = pan.querySelector('form.nldg-ask'), pQ = pan.querySelector('#nldg-q'), pMic = pan.querySelector('.nldg-mic');
	var pMute = pan.querySelector('.nldg-mute');

	wrap.appendChild(pan); wrap.appendChild(bub); wrap.appendChild(face);
	document.body.appendChild(wrap);

	/* stays clear of the site's WhatsApp bar and the accessibility button, whatever their place on this width */
	function place() {
		var vw = window.innerWidth, vh = window.innerHeight, size = st.closed ? 46 : (vw < 768 ? 66 : 78), right = 14, b = 14;
		['nlcta', 'nla11y'].forEach(function (id) {
			var o = document.getElementById(id); if (!o) { return; }
			var r = o.getBoundingClientRect(); if (!r.width || r.bottom < 0 || r.top > vh) { return; }
			var L = vw - right - size, R = vw - right;
			if (r.right > L - 4 && r.left < R + 4) { b = Math.max(b, Math.round(vh - r.top + 10)); }
		});
		wrap.style.setProperty('--b', b + 'px'); wrap.style.setProperty('--s', size + 'px');
	}
	place();
	window.addEventListener('resize', place);
	setInterval(place, 1500);

	/* ---------- voice and lips (only with a recorded clip, only after a tap) ---------- */
	var au = null, actx = null, an = null, buf = null, raf = 0, queue = [];
	function unlock() {
		if (st.unlocked) { return; }
		st.unlocked = true;
		try { var AC = window.AudioContext || window.webkitAudioContext; if (AC) { actx = new AC(); } } catch (e) { actx = null; }
	}
	['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { document.addEventListener(ev, unlock, { capture: true, passive: true }); });
	function talking(on) { wrap.classList.toggle('is-talk', !!on); if (!on) { fB.style.opacity = 0; fC.style.opacity = 0; cancelAnimationFrame(raf); } }
	function lips() {
		var v = 0;
		if (an) { an.getByteTimeDomainData(buf); var s = 0; for (var i = 0; i < buf.length; i++) { var x = (buf[i] - 128) / 128; s += x * x; } v = Math.sqrt(s / buf.length); }
		else { v = 0.06 + 0.05 * Math.sin(performance.now() / 70); }
		/* subtle on purpose (Ben 7.11): the slightly parted shape, the wider one only on loud syllables */
		fB.style.opacity = Math.min(0.55, v * 5).toFixed(2);
		fC.style.opacity = v > 0.14 ? '0.4' : '0';
		raf = requestAnimationFrame(lips);
	}
	function stopVoice() { queue = []; if (au) { au.pause(); } talking(false); }
	function playNext() {
		var url = queue.shift();
		if (!url) { talking(false); return; }
		if (!au) {
			au = new Audio(); au.preload = 'auto'; au.crossOrigin = 'anonymous';
			if (actx) { try { var src = actx.createMediaElementSource(au); an = actx.createAnalyser(); an.fftSize = 512; buf = new Uint8Array(an.fftSize); src.connect(an); an.connect(actx.destination); } catch (e) { an = null; } }
			au.addEventListener('ended', function () { talking(false); setTimeout(playNext, 220); });
		}
		au.src = url;
		if (actx && actx.state === 'suspended') { actx.resume(); }
		var p = au.play();
		if (p && p.then) { p.then(function () { talking(true); cancelAnimationFrame(raf); if (!RM) { lips(); } }).catch(function () { talking(false); }); }
	}
	function voice(ids) {
		if (!st.unlocked || st.muted || st.closed) { return; }
		var urls = ids.map(lineClip).filter(Boolean);
		if (!urls.length) { return; }
		stopVoice(); queue = urls; playNext();
	}

	/* ---------- saying something ---------- */
	var hideT = 0;
	function reveal(p, text) {
		p.textContent = '';
		if (RM) { p.textContent = text; return; }
		var w = text.split(' '), i = 0;
		(function step() { if (i >= w.length) { return; } p.textContent += (i ? ' ' : '') + w[i++]; setTimeout(step, 38); })();
	}
	function acts(box, list) {
		box.innerHTML = '';
		(list || []).forEach(function (a) {
			var b = a.href ? el('a', 'nldg-act', a.label) : el('button', 'nldg-act', a.label);
			if (a.href) { b.href = a.href; b.target = '_blank'; b.rel = 'noopener' + (a.nofollow ? ' nofollow' : ''); } else { b.type = 'button'; }
			b.addEventListener('click', function () { st.lastAct = now(); if (a.fn) { a.fn(); } if (!a.keep) { hideBub(); } });
			box.appendChild(b);
		});
	}
	function hideBub() { clearTimeout(hideT); bub.classList.remove('is-in'); setTimeout(function () { if (!bub.classList.contains('is-in')) { bub.hidden = true; } }, 260); }
	/* o: { chk: line id, acts: [...], voice: [extra line ids] } */
	function say(id, o) {
		o = o || {};
		var text = lineText(id); if (!text) { return; }
		var chk = o.chk ? lineText(o.chk) : '';
		var ids = [id].concat(o.chk ? [o.chk] : []);
		if (o.deal && !st.saidNr) { ids.push('nr'); st.saidNr = true; }
		if (st.panel) {
			pAns.hidden = false; reveal(pSay, text);
			pChk.hidden = !chk; pChk.innerHTML = chk ? '<b>מה שווה לבדוק:</b> ' : ''; if (chk) { pChk.appendChild(document.createTextNode(chk)); }
			acts(pActs, o.acts);
		} else {
			bub.hidden = false; void bub.offsetWidth; bub.classList.add('is-in');
			reveal(bSay, text);
			bChk.hidden = !chk; bChk.innerHTML = chk ? '<b>מה שווה לבדוק:</b> ' : ''; if (chk) { bChk.appendChild(document.createTextNode(chk)); }
			acts(bActs, o.acts);
			clearTimeout(hideT);
			hideT = setTimeout(function () { if (!bub.matches(':hover') && !bub.contains(document.activeElement)) { hideBub(); } }, Math.max(7000, (text + chk).split(' ').length * 420 + 3500));
		}
		voice(ids);
		if (!RM) { face.classList.remove('is-nod'); void face.offsetWidth; face.classList.add('is-nod'); }
	}
	bX.addEventListener('click', function () { hideBub(); stopVoice(); });

	/* the two clocks that keep her polite: unasked lines (40 s apart, 3 a visit) and reactions to a visitor's act (12 s, 6 a visit) */
	var busyNow = function () {
		var a = document.activeElement;
		return (now() - st.lastScroll < 1200) || (a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName) && !pan.contains(a));
	};
	function unasked(id, o, tries) {
		if (st.closed || st.panel || st.onceDone[id]) { return; }
		if (now() - st.lastPro < 40000 || st.pro >= 3) { return; }
		if (busyNow()) { if ((tries || 0) < 3) { setTimeout(function () { unasked(id, o, (tries || 0) + 1); }, 1600); } return; }
		st.onceDone[id] = true; st.lastPro = now(); st.pro++;
		say(id, o);
	}
	function react(id, o) {
		if (st.closed) { return; }
		if (!st.panel && (now() - st.lastReact < 12000 || st.react >= 6)) { return; }
		st.lastReact = now(); st.react++;
		say(id, o);
	}
	window.addEventListener('scroll', function () { st.lastScroll = now(); st.lastAct = now(); }, { passive: true });
	['pointerdown', 'keydown'].forEach(function (ev) { document.addEventListener(ev, function () { st.lastAct = now(); }, { passive: true }); });

	/* ---------- what she does ---------- */
	var wa = function (t) { return 'https://wa.me/' + G.wa + '?text=' + encodeURIComponent(t); };
	function dealActs(d) {
		var a = [{ label: 'השאירו פרטים על המבצע', fn: function () { openLead('מבצע: ' + d.project + ' (' + d.devFull + ')'); } }];
		if (d.calcOk && d.price) { a.push({ label: 'חשבו כמה זה שווה', fn: function () { api.calc(d.id); } }); }
		a.push({ label: 'התראה לאזור הזה', fn: function () { api.alert(d.id); } });
		return a;
	}
	function tellDeal(id, show) {
		var d = api && api.byId[id]; if (!d) { return false; }
		if (show) { api.show(id); }
		(st.panel ? say : react)('d-' + id, { chk: 'c-' + id, acts: dealActs(d), deal: true });
		return true;
	}
	function cashLine(cash) {
		var fits = api.fits(cash), ids = fits.map(function (d) { return d.id; }), n = ids.length;
		var max = 0; while (G.lines['cash' + (max + 1)]) { max++; }
		if (n) { api.light(ids); }
		return { id: 'cash' + Math.min(n, max), o: { acts: n ? [{ label: 'התראה כשנפתח עוד', fn: function () { api.alert(); } }, { label: 'השאירו פרטים', fn: function () { openLead('יש לי ביד כ-' + Math.round(cash / 1000) + ' אלף ₪, מבצעי קבלנים שמתאימים'); } }] : [] } };
	}
	function near(name) {
		var c = G.cities[name]; if (!c || !api) { return null; }
		var km = function (d) { var k = Math.cos(c[0] * Math.PI / 180) * 111.32; return Math.sqrt(Math.pow((d.lng - c[1]) * k, 2) + Math.pow((d.lat - c[0]) * 110.57, 2)); };
		var list = api.deals.filter(function (d) { return km(d) <= 6 || String(d.city).indexOf(name) >= 0; });
		return list;
	}

	/* ---------- understanding a question: plain rules on the visitor's words, then the map's own data ---------- */
	var TOP = [
		['who', /מי את|מה את|רובוט|בן אדם|אמיתית\?|בינה מלאכותית|\bai\b/],
		['best', /מומלץ|ממליצ|הכי טוב|הכי שווה|הכי משתלם|מה כדאי|כדאי לי|איזה מבצע|מה לקנות|מה עדיף/],
		['q2080', /20\s*[\/\\-]?\s*80|80\s*[\/\\-]?\s*20|10\s*[\/\\-]?\s*90|90\s*[\/\\-]?\s*10|מדורג|לוח תשלומים|תשלום מדורג/],
		['qzero', /0\s*%|אפס|בלי הון|ללא הון|הון עצמי|בלי לשלם|לא משלמים|בלי מקדמה/],
		['qtrue', /הנחה אמיתית|שווה באמת|כמה שווה|מחשבון|לחשב|באמת הנחה/],
		['qloan', /הלוואת קבלן|הלוואה|קרדיט/],
		['qindex', /מדד|הצמדה|צמוד/],
		['qbank', /בנק|משכנת|אישור עקרוני|יועץ/],
		['qvalid', /בתוקף|עדיין|נגמר|עד מתי|מעודכן|רלוונטי/],
		['qrent', /שכר דירה|שכירות|הטבה חודשית|כל חודש/],
		['alert', /התראה|תודיעי|תעדכני|עדכון במייל|מייל/]
	];
	function answer(raw) {
		var q = String(raw || '').toLowerCase().replace(/[֑-ׇ]/g, '').replace(/["'״׳?!.,]/g, ' ').replace(/\s+/g, ' ').trim();
		if (!q || !api) { return; }
		st.lastAct = now();
		/* a developer or a project by name */
		var hit = api.deals.filter(function (d) {
			return [d.dev, d.devFull, d.project.split(',')[0]].some(function (n) { n = String(n || '').toLowerCase().replace(/["'״׳]/g, ' ').trim(); return n.length > 2 && q.indexOf(n) >= 0; });
		});
		if (hit.length) { if (hit.length > 1) { api.light(hit.map(function (d) { return d.id; })); } tellDeal((hit.filter(function (d) { return d.hot; })[0] || hit[0]).id, true); return; }
		/* a place */
		var city = Object.keys(G.cities).filter(function (c) { return q.indexOf(c) >= 0; })[0];
		if (city) {
			var list = near(city), n = list.length, ids = list.map(function (d) { return d.id; });
			if (n) { api.light(ids); }
			say(n ? 'near' + Math.min(n, 8) : 'near0', { acts: n === 1 ? dealActs(list[0]) : [{ label: 'התראה על מבצע חדש כאן', fn: function () { api.alert(); } }] });
			return;
		}
		for (var i = 0; i < TOP.length; i++) {
			if (TOP[i][1].test(q)) { topic(TOP[i][0]); return; }
		}
		say('unknown', { acts: [{ label: 'השאירו פרטים, ונחזור עם תשובה', fn: function () { openLead('שאלה: ' + String(raw).slice(0, 160)); } }] });
	}
	function topic(id) {
		var o = {};
		if (id === 'qzero') { var z = api.deals.filter(function (d) { return api.need(d) === 0; }).map(function (d) { return d.id; }); api.light(z); }
		if (id === 'qrent') { api.light(api.deals.filter(function (d) { return d.k === 'rent'; }).map(function (d) { return d.id; })); }
		if (id === 'qtrue') { api.calc(api.state().sel); }
		if (id === 'q2080') { o.acts = [{ label: 'הראו לי מבצעים כאלה', fn: function () { api.kind('pay'); } }]; }
		if (id === 'qbank' || id === 'qloan' || id === 'qindex') { o.acts = [{ label: 'השאירו פרטים לייעוץ משכנתא', fn: function () { openLead('ייעוץ משכנתא על מבצע קבלן'); } }]; }
		if (id === 'qvalid') { var d = api.byId[api.state().sel]; o.acts = [{ label: 'השאירו פרטים, ונבדוק', fn: function () { openLead('לבדוק אם המבצע ' + (d ? 'ב' + d.project : 'של הקבלן') + ' עדיין בתוקף'); } }]; }
		if (id === 'alert') { api.alert(); }
		if (id === 'best') { o.acts = [{ label: 'לסכום שלי', fn: function () { var c = document.getElementById('nldm-cash'); if (c) { c.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' }); c.focus({ preventScroll: true }); } } }]; }
		say(id, o);
	}

	/* ---------- the panel: questions that follow what the visitor did ---------- */
	function chips() {
		pChips.innerHTML = '';
		var s = api ? api.state() : {}, list = [];
		if (st.picked && api && api.byId[st.picked]) { var d = api.byId[st.picked]; list.push(['ספרי לי על ' + d.project.split(',')[0], function () { tellDeal(d.id, true); }]); }
		if (st.cashMoved) { list.push(['מה פתוח עם הסכום שלי?', function () { var c = cashLine(s.cash); say(c.id, c.o); }]); }
		list.push(['מה זה 20/80?', function () { topic('q2080'); }]);
		list.push(['איפה יש 0% הון עצמי?', function () { topic('qzero'); }]);
		list.push(['מה ההבדל בין מבצע להנחה אמיתית?', function () { topic('qtrue'); }]);
		list.push(['הבנק יאשר לי משכנתא?', function () { topic('qbank'); }]);
		list.slice(0, 5).forEach(function (c) { var b = el('button', 'nldg-chip', c[0]); b.type = 'button'; b.addEventListener('click', function () { c[1](); }); pChips.appendChild(b); });
	}
	function muteLabel() { pMute.textContent = st.muted ? 'הפעלת הקול' : 'השתקת הקול'; pMute.setAttribute('aria-pressed', st.muted ? 'true' : 'false'); }
	function openPanel() {
		if (st.closed) { st.closed = false; LS.set('nldg-closed', false); wrap.classList.remove('is-mini'); place(); }
		st.panel = true; hideBub(); chips(); muteLabel(); pAns.hidden = true;
		pan.hidden = false; void pan.offsetWidth; pan.classList.add('is-in'); wrap.classList.add('is-open');
		face.setAttribute('aria-expanded', 'true');
		if (!st.onceDone.hello) { st.onceDone.hello = true; say('hello'); }
	}
	function closePanel() {
		st.panel = false; closeLead(); pan.classList.remove('is-in'); wrap.classList.remove('is-open'); face.setAttribute('aria-expanded', 'false');
		setTimeout(function () { if (!st.panel) { pan.hidden = true; } }, 260);
		stopVoice();
	}
	face.addEventListener('click', function () { unlock(); if (st.panel) { closePanel(); } else { openPanel(); } });
	pan.querySelector('.nldg-pc').addEventListener('click', function () { closePanel(); face.focus(); });
	pan.querySelector('.nldg-off').addEventListener('click', function () {
		st.closed = true; LS.set('nldg-closed', true); closePanel(); hideBub(); wrap.classList.add('is-mini'); place();
	});
	/* ---------- leaving details: an ordinary site lead (Lead Inbox), with the site's consent line ---------- */
	var lf = pan.querySelector('form.nldg-lead'), lTopic = '', lMsg = lf.querySelector('.nldg-lm');
	lf.querySelector('.nldg-lc').textContent = G.consent || '';
	function openLead(topicText) {
		if (!st.panel) { openPanel(); }
		lTopic = String(topicText || 'מבצעי קבלנים');
		lf.querySelector('.nldg-lt').textContent = lTopic;
		pAns.hidden = true; pChips.hidden = true; pForm.hidden = true; lf.hidden = false; lMsg.textContent = ''; wrap.classList.add('is-lead');
		setTimeout(function () { lf.querySelector('#nldg-ln').focus(); }, 280);
	}
	function closeLead() { lf.hidden = true; pChips.hidden = false; pForm.hidden = false; wrap.classList.remove('is-lead'); }
	pan.querySelector('.nldg-tolead').addEventListener('click', function () { openLead(st.picked && api && api.byId[st.picked] ? 'מבצע: ' + api.byId[st.picked].project : 'מבצעי קבלנים'); });
	lf.addEventListener('submit', function (e) {
		e.preventDefault();
		var name = lf.name.value.trim(), phone = lf.phone.value.replace(/[^0-9]/g, ''), btn = lf.querySelector('.nldg-ls');
		if (phone.indexOf('972') === 0) { phone = '0' + phone.slice(3); }
		if (name.length < 2) { lMsg.textContent = 'כתבו שם, בבקשה.'; lf.name.focus(); return; }
		if (!/^05\d{8}$/.test(phone)) { lMsg.textContent = 'מספר נייד ישראלי: 10 ספרות שמתחילות ב-05.'; lf.phone.focus(); return; }
		btn.disabled = true; lMsg.textContent = 'שולחים...';
		var s = api ? api.state() : {}, d = api && s.sel ? api.byId[s.sel] : null;
		fetch(G.lead, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin',
			body: JSON.stringify({ name: name, phone: phone, goal: 'מבצעי קבלנים', source: 'deals_guide', company: lf.company.value || '',
				message: lTopic + (d ? '\nהמבצע שנבחר במפה: ' + d.project + ' (' + d.devFull + ')' : '') + (st.cashMoved ? '\nסכום ביד שבחר: ' + Math.round(s.cash / 1000) + ' אלף ₪' : '') + '\nמהעמוד: ' + location.pathname,
				consent: 1, consent_text: G.consent || '' }) })
			.then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }).catch(function () { return { ok: r.ok, j: {} }; }); })
			.then(function (x) {
				btn.disabled = false;
				if (x.ok) {
					lf.reset(); closeLead(); pAns.hidden = false; pChk.hidden = true; pActs.innerHTML = '';
					pSay.textContent = 'תודה, ' + name + '. קיבלנו, ונחזור אליכם לנייד ' + phone.replace(/^(\d{3})/, '$1-') + '.';
				} else { lMsg.textContent = x.j && x.j.code === 'rate' ? 'נשלחו כבר כמה פניות. נסו שוב בעוד שעה.' : 'משהו לא עבד. נסו שוב.'; }
			})
			.catch(function () { btn.disabled = false; lMsg.textContent = 'אין חיבור. נסו שוב.'; });
	});
	pMute.addEventListener('click', function () { st.muted = !st.muted; LS.set('nldg-muted', st.muted); if (st.muted) { stopVoice(); } muteLabel(); });
	pForm.addEventListener('submit', function (e) { e.preventDefault(); var v = pQ.value; pQ.value = ''; answer(v); });
	document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && st.panel) { closePanel(); face.focus(); } });

	/* speaking a question: the browser turns speech into text (Chrome, Edge, Safari); we keep no recording */
	var SR = window.SpeechRecognition || window.webkitSpeechRecognition, rec = null;
	if (SR) {
		pMic.hidden = false;
		pMic.addEventListener('click', function () {
			unlock(); stopVoice();
			if (rec) { rec.stop(); return; }
			rec = new SR(); rec.lang = 'he-IL'; rec.interimResults = true; rec.maxAlternatives = 1;
			pMic.classList.add('is-on'); pMic.textContent = 'מקשיבה'; pQ.placeholder = 'מקשיבה...';
			var fin = '';
			rec.onresult = function (e) { var t = ''; for (var i = e.resultIndex; i < e.results.length; i++) { t += e.results[i][0].transcript; if (e.results[i].isFinal) { fin = t; } } pQ.value = t; };
			rec.onerror = function () { pQ.placeholder = 'לא שמעתי. אפשר לכתוב.'; };
			rec.onend = function () { pMic.classList.remove('is-on'); pMic.textContent = 'דברו'; rec = null; if (pQ.placeholder === 'מקשיבה...') { pQ.placeholder = 'כתבו שאלה, למשל: מה זה 20/80?'; } if (fin || pQ.value) { var v = fin || pQ.value; pQ.value = ''; answer(v); } };
			try { rec.start(); } catch (e) { rec = null; pMic.classList.remove('is-on'); }
		});
	}

	/* ---------- reading the page (the "she knows what you are doing" part) ---------- */
	function start() {
		api = window.NLDM; if (!api) { return; }
		/* return visits: what changed since the last visit, kept on this device only */
		var mem = LS.get('nldg-v'), ids = api.deals.map(function (d) { return d.id; });
		LS.set('nldg-v', { t: now(), ids: ids });
		setTimeout(function () { wrap.classList.add('is-in'); place(); }, RM ? 0 : 1200);
		if (st.closed) { return; }
		if (mem && mem.t && now() - mem.t > 3 * 3600 * 1000 && Array.isArray(mem.ids)) {
			var fresh = ids.filter(function (i) { return mem.ids.indexOf(i) < 0; });
			setTimeout(function () {
				if (fresh.length) { api.light(fresh); unasked('ret' + Math.min(fresh.length, 8), { acts: [{ label: 'הראי את החדש', fn: function () { api.show(fresh[0]); } }] }); }
				else { unasked('ret0'); }
			}, 2600);
		} else {
			setTimeout(function () { unasked('greet', { acts: [{ label: 'לסכום שלי', fn: function () { var c = document.getElementById('nldm-cash'); if (c) { c.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' }); } } }] }); }, 2600);
		}
		document.addEventListener('nldm:cash', function (e) {
			st.cashMoved = true;
			clearTimeout(st.cashT);
			st.cashT = setTimeout(function () { var c = cashLine(e.detail.cash); react(c.id, c.o); }, 1100);
		});
		document.addEventListener('nldm:pick', function (e) { if (e.detail.quiet) { return; } st.picked = e.detail.id; tellDeal(e.detail.id, false); });
		/* a pause on the map: one gentle line, once */
		var mapEl = document.getElementById('nldm-map'), mapSeen = false;
		if (mapEl && 'IntersectionObserver' in window) {
			new IntersectionObserver(function (en) { mapSeen = en[0].isIntersecting; }, { threshold: 0.5 }).observe(mapEl);
			setInterval(function () { if (mapSeen && now() - st.lastAct > 22000) { unasked('idle', { acts: [{ label: 'סננו לי', fn: function () { api.kind('pay'); } }] }); } }, 4000);
		}
		/* reaching the calculator or the alert for the first time */
		[['nldm-calc', 'calc'], ['nldm-alert', 'alert']].forEach(function (p) {
			var t = document.getElementById(p[0]); if (!t || !('IntersectionObserver' in window)) { return; }
			var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { io.disconnect(); setTimeout(function () { unasked(p[1]); }, 1500); } }, { threshold: 0.35 });
			io.observe(t);
		});
	}
	if (window.NLDM) { start(); } else { document.addEventListener('nldm:ready', start); }
})();
