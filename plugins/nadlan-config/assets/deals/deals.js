/* HAD-743 developer deals map (nad-lan.co.il /developer-deals/). No build step, no globals besides maplibregl from cdnjs. */
(function () {
	'use strict';
	var root = document.getElementById('nldm');
	var dataEl = document.getElementById('nldm-data');
	if (!root || !dataEl) { return; }
	var D;
	try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
	var RM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	var deals = D.deals || [];
	var byId = {};
	deals.forEach(function (d) { byId[d.id] = d; });
	var S = { cash: 600000, kind: 'all', sel: D.hotId || (deals[0] && deals[0].id), tilt: true };
	var map = null, markers = {}, raf = 0;
	var $ = function (sel, el) { return (el || root).querySelector(sel); };
	var $$ = function (sel, el) { return Array.prototype.slice.call((el || root).querySelectorAll(sel)); };
	var tagOf = function (id) { return markers[id] ? markers[id].getElement().firstChild : null; };

	function fmt(n) {
		if (n >= 1000000) { return (Math.round(n / 10000) / 100).toString() + ' מיליון ₪'; }
		return Math.round(n / 1000).toLocaleString('he-IL') + ' אלף ₪';
	}
	function need(d) {
		if (d.firstAbs != null) { return d.firstAbs; }
		if (d.first != null && d.price) { return Math.round(d.price * d.first); }
		if (d.first === 0) { return 0; }
		return null;
	}
	function status(d) { var n = need(d); return n == null ? 'unk' : (n <= S.cash ? 'fit' : 'no'); }
	function needText(d) { var n = need(d); return n == null ? 'בקשו מחיר ›' : (n === 0 ? '0 ₪ בחתימה' : fmt(n) + ' ביד'); }
	function wa(t) { return 'https://wa.me/' + D.wa + '?text=' + encodeURIComponent(t); }
	function shown(d) { return S.kind === 'all' || d.k === S.kind; }

	/* number roll: animates a text number toward a target */
	function roll(el, from, to, f) {
		if (RM || from === to) { el.textContent = f(to); return; }
		var t0 = performance.now(), dur = 420;
		(function step(t) {
			var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
			el.textContent = f(Math.round(from + (to - from) * e));
			if (p < 1) { requestAnimationFrame(step); }
		})(t0);
	}

	/* particles: diamonds in the developer's colour, balloons for the hot deal */
	function burst(x, y, color, hot) {
		if (RM) { return; }
		var wrap = document.createElement('div');
		wrap.className = 'nldm-burst';
		var n = hot ? 22 : 10, cols = hot ? ['#C8102E', '#0E4C63', '#17694A', '#F2B705', color] : [color, '#0E4C63', '#C8102E'];
		for (var i = 0; i < n; i++) {
			var p = document.createElement('i');
			var balloon = hot && i % 4 === 0;
			if (balloon) { p.className = 'b'; }
			p.style.background = cols[i % cols.length];
			p.style.left = x + 'px'; p.style.top = y + 'px';
			wrap.appendChild(p);
			var ang = (Math.PI * 2 * i) / n + Math.random() * 0.5, dist = (hot ? 70 : 44) + Math.random() * 40;
			var dx = Math.cos(ang) * dist, dy = Math.sin(ang) * dist - (balloon ? 90 : 20);
			p.animate([
				{ transform: (balloon ? '' : 'rotate(45deg) ') + 'translate(0,0) scale(.3)', opacity: 1 },
				{ transform: (balloon ? '' : 'rotate(' + (45 + Math.random() * 300) + 'deg) ') + 'translate(' + dx + 'px,' + dy + 'px) scale(1)', opacity: balloon ? 0.95 : 0 }
			], { duration: balloon ? 1600 : 800 + Math.random() * 300, easing: 'cubic-bezier(.15,.8,.3,1)', fill: 'forwards' });
		}
		document.body.appendChild(wrap);
		setTimeout(function () { wrap.remove(); }, 1800);
	}

	/* cash slider */
	var cashIn = $('#nldm-cash'), cashOut = $('#nldm-cash-out'), think = $('.nldm-think'), thinkT = 0;
	function counts() {
		var c = { fit: 0, no: 0, unk: 0 };
		deals.forEach(function (d) { c[status(d)]++; });
		Object.keys(c).forEach(function (k) {
			var el = $('[data-n=' + k + ']');
			if (el) { roll(el, parseInt(el.textContent, 10) || 0, c[k], String); }
		});
	}
	function paintStatus(flip) {
		deals.forEach(function (d) {
			var st = status(d), el = tagOf(d.id);
			if (el) {
				if (el.getAttribute('data-st') !== st) {
					el.setAttribute('data-st', st);
					if (flip && !RM) { el.classList.remove('is-flip'); void el.offsetWidth; el.classList.add('is-flip'); }
				}
				el.querySelector('.t2').textContent = needText(d);
			}
			var li = root.querySelector('.nldm-list li[data-id="' + d.id + '"] .nldm-need');
			if (li) { li.className = 'nldm-need is-' + st; li.textContent = st === 'unk' ? 'בקשו מחיר' : needText(d).replace(' ביד', ''); }
		});
		var ol = $('.nldm-list ol'), order = { fit: 0, unk: 1, no: 2 };
		$$('.nldm-list li').sort(function (a, b) { return order[status(byId[a.dataset.id])] - order[status(byId[b.dataset.id])]; }).forEach(function (li) { ol.appendChild(li); });
	}
	if (cashIn) {
		cashIn.addEventListener('input', function () {
			var v = Number(cashIn.value);
			roll(cashOut, S.cash, v, fmt);
			cashOut.classList.add('is-bump'); setTimeout(function () { cashOut.classList.remove('is-bump'); }, 180);
			S.cash = v;
			if (think) { think.hidden = false; }
			clearTimeout(thinkT);
			thinkT = setTimeout(function () { if (think) { think.hidden = true; } counts(); paintStatus(true); renderSheet(false); }, 380);
		});
	}

	/* chips */
	$$('.nldm-chips button').forEach(function (b) {
		b.addEventListener('click', function () {
			S.kind = b.dataset.k;
			$$('.nldm-chips button').forEach(function (x) { var on = x === b; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
			deals.forEach(function (d) {
				var m = markers[d.id]; if (m) { m.getElement().classList.toggle('is-hidden', !shown(d)); }
				var li = root.querySelector('.nldm-list li[data-id="' + d.id + '"]'); if (li) { li.hidden = !shown(d); }
			});
			declutter();
			var vis = deals.filter(shown);
			if (map && vis.length) { fitTo(vis); }
		});
	});

	/* the sheet */
	var sheet = $('.nldm-sheet');
	function setF(name, v) { var el = sheet.querySelector('[data-f=' + name + ']'); if (el) { el.textContent = v; } return el; }
	function renderSheet(anim) {
		var d = byId[S.sel]; if (!d || !sheet) { return; }
		var chip = sheet.querySelector('[data-f=init]');
		chip.textContent = d.dev.slice(0, 2); chip.style.background = d.color;
		setF('sub', d.devFull + ' · ' + d.city + (d.hot ? ' · מבצע חם' : ''));
		setF('project', d.project); setF('kind', d.kind); setF('terms', d.terms);
		var bar = sheet.querySelector('[data-f=bar]'); bar.innerHTML = '';
		d.bar.forEach(function (b, i) {
			var s = document.createElement('span'); s.className = b[2]; s.textContent = b[0] >= 18 ? b[1] : '';
			bar.appendChild(s);
			setTimeout(function () { s.style.width = 'calc(' + b[0] + '% - 2px)'; }, RM ? 0 : 60 + i * 120);
		});
		setF('price', d.price ? fmt(d.price) : 'לא פורסם');
		var n = need(d), st = status(d), needEl = setF('need', n == null ? 'לא פורסם' : fmt(n));
		needEl.style.color = st === 'fit' ? '#17694A' : (st === 'no' ? '#A10D25' : '#4A5863');
		var worthEl = sheet.querySelector('[data-f=worth]');
		if (d.worth) { roll(worthEl, 0, d.worth, function (v) { return 'כ-' + fmt(v) + ' לפי פרסום'; }); } else { worthEl.textContent = 'לא פורסם'; }
		var ch = sheet.querySelector('[data-f=check]');
		ch.classList.toggle('is-ok', !!d.checked);
		ch.innerHTML = '';
		ch.appendChild(document.createTextNode(d.checked ? 'בדקנו שהמבצע עדיין מוצע ב-' + d.checked + '. ' : 'פורסם: ' + d.pub + '. עוד לא אישרנו שהוא עדיין בתוקף: לחצו ונבדוק מול היזם. '));
		if (d.link) { var pl = document.createElement('a'); pl.href = d.link; pl.textContent = 'לעמוד הפרויקט'; ch.appendChild(pl); ch.appendChild(document.createTextNode(' · ')); }
		if (d.src) { var a = document.createElement('a'); a.href = d.src; a.target = '_blank'; a.rel = 'noopener nofollow'; a.textContent = 'המקור'; ch.appendChild(a); }
		var w1 = sheet.querySelector('[data-f=wa1]'), w2 = sheet.querySelector('[data-f=wa2]');
		w1.href = wa('היי, אשמח לבדוק אם המבצע ב' + d.project + ' (' + d.kind + ') עדיין בתוקף ולקבל מחירון ותוכניות');
		w2.href = wa('היי, אשמח לייעוץ משכנתא והשלמת הון למבצע ב' + d.project);
		$$('.nldm-list li').forEach(function (li) { li.classList.toggle('is-sel', li.dataset.id === d.id); });
		if (anim && !RM) { sheet.classList.remove('is-swap'); void sheet.offsetWidth; sheet.classList.add('is-swap'); }
	}
	function pick(id, fromList) {
		S.sel = id;
		Object.keys(markers).forEach(function (k) { tagOf(k).classList.toggle('is-sel', k === id); markers[k].getElement().style.zIndex = k === id ? '5' : ''; });
		renderSheet(true);
		var d = byId[id];
		if (map && d) { map.easeTo({ center: [d.lng, d.lat], zoom: Math.max(map.getZoom(), 12.4), duration: RM ? 0 : 900 }); }
		if (fromList && map) { root.querySelector('.nldm-stage').scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' }); }
	}
	$$('.nldm-list [data-pick]').forEach(function (b) {
		b.addEventListener('click', function (e) { var r = b.getBoundingClientRect(); burst(r.left + 20, r.top + r.height / 2, byId[b.dataset.pick].color, false); pick(b.dataset.pick, true); });
	});

	/* the map */
	function fitTo(list) {
		var b = new maplibregl.LngLatBounds();
		list.forEach(function (d) { b.extend([d.lng, d.lat]); });
		var cam = map.cameraForBounds(b, { padding: { top: 90, bottom: 60, left: 40, right: 40 }, maxZoom: 13 });
		if (!cam) { return; }
		map.easeTo({ center: cam.center, zoom: cam.zoom - (S.tilt ? 0.35 : 0), pitch: S.tilt ? 52 : 0, bearing: S.tilt ? -14 : 0, duration: RM ? 0 : 1100 });
	}
	function tagEl(d) {
		var el = document.createElement('button');
		el.type = 'button'; el.className = 'nldm-tag' + (d.hot ? ' is-hot' : '') + (d.id === S.sel ? ' is-sel' : '');
		el.setAttribute('data-st', status(d));
		el.setAttribute('aria-label', d.project + ', ' + d.kind);
		el.innerHTML = '<span class="bar" style="background:' + d.color + '"></span><span class="tx"><span class="t1"></span><span class="t2"></span></span>';
		el.querySelector('.t1').textContent = d.dev + ' · ' + d.short;
		el.querySelector('.t2').textContent = needText(d);
		if (d.hot) {
			var h = document.createElement('span'); h.className = 'hot';
			h.innerHTML = '<svg viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2c1 4 5 5.5 5 11a5 5 0 0 1-10 0c0-2.5 1.2-4 2.5-5 .2 1.8 1 2.8 2 3.2C11 8.5 11 5 12 2z"/></svg>';
			h.appendChild(document.createTextNode('מבצע חם'));
			el.appendChild(h);
			if (!RM) {
				for (var i = 0; i < 5; i++) {
					var s = document.createElement('span'); s.className = 'nldm-spark';
					s.style.background = ['#C8102E', '#F2B705', '#0E4C63', '#17694A', '#C8102E'][i];
					s.style.left = (10 + i * 22) + '%'; s.style.top = '-4px';
					s.style.setProperty('--dx', (i % 2 ? 8 : -8) + 'px');
					s.style.animationDelay = (i * 0.5) + 's';
					el.appendChild(s);
				}
			}
		}
		el.addEventListener('click', function (e) {
			e.stopPropagation();
			if (el.classList.contains('is-tuck')) { map.easeTo({ center: [d.lng, d.lat], zoom: map.getZoom() + 1.6, duration: RM ? 0 : 700 }); return; }
			var r = el.getBoundingClientRect();
			burst(r.left + r.width / 2, r.top, d.color, !!d.hot);
			pick(d.id, false);
		});
		var wrap = document.createElement('div'); wrap.className = 'nldm-mk'; wrap.appendChild(el);
		return wrap;
	}
	/* keeps every tag readable: higher priority first, an overlapping tag folds to a dot in its colour */
	function declutter() {
		if (!map) { return; }
		cancelAnimationFrame(raf);
		raf = requestAnimationFrame(function () {
			var pr = { fit: 1, unk: 2, no: 3 };
			var list = deals.filter(shown).sort(function (a, b) {
				var pa = (a.id === S.sel ? -2 : 0) + (a.hot ? -1 : 0) + pr[status(a)], pb = (b.id === S.sel ? -2 : 0) + (b.hot ? -1 : 0) + pr[status(b)];
				return pa - pb;
			});
			var kept = [];
			list.forEach(function (d) {
				var el = tagOf(d.id), p = map.project([d.lng, d.lat]);
				var w = 128, h = 44, box = [p.x - w / 2, p.y - h - 8, p.x + w / 2, p.y];
				var hit = kept.some(function (k) { return !(box[2] < k[0] || box[0] > k[2] || box[3] < k[1] || box[1] > k[3]); });
				el.classList.toggle('is-tuck', hit);
				if (!hit) { kept.push(box); }
			});
		});
	}
	function addLayers() {
		try {
			var src = Object.keys(map.getStyle().sources).filter(function (k) { return map.getStyle().sources[k].type === 'vector'; })[0];
			if (src) {
				map.addLayer({ id: 'nldm-3d', type: 'fill-extrusion', source: src, 'source-layer': 'building', minzoom: 13,
					paint: { 'fill-extrusion-color': ['interpolate', ['linear'], ['coalesce', ['get', 'render_height'], 0], 0, '#DCE3E8', 60, '#C6D2DA', 150, '#AFC0CB'],
						'fill-extrusion-height': ['interpolate', ['linear'], ['zoom'], 13, 0, 14.5, ['coalesce', ['get', 'render_height'], 0]],
						'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0], 'fill-extrusion-opacity': 0.82 } });
			}
		} catch (e) { /* the style has no building layer: the map stays flat */ }
		fetch(D.pointsUrl).then(function (r) { return r.json(); }).then(function (pts) {
			map.addSource('nldm-pts', { type: 'geojson', data: { type: 'FeatureCollection', features: pts.map(function (p) {
				return { type: 'Feature', geometry: { type: 'Point', coordinates: [p[0], p[1]] }, properties: { t: p[2], u: p[3] } };
			}) } });
			map.addLayer({ id: 'nldm-pts', type: 'circle', source: 'nldm-pts', paint: {
				'circle-radius': ['interpolate', ['linear'], ['zoom'], 8, 1.6, 12, 3.4, 15, 6], 'circle-color': '#6F7E88', 'circle-opacity': 0.55,
				'circle-stroke-color': '#FFFFFF', 'circle-stroke-width': ['interpolate', ['linear'], ['zoom'], 10, 0, 13, 1] } });
			map.on('click', 'nldm-pts', function (e) {
				var f = e.features && e.features[0]; if (!f) { return; }
				var box = document.createElement('div'), a = document.createElement('a');
				a.href = f.properties.u; a.textContent = f.properties.t;
				box.appendChild(a); box.appendChild(document.createElement('br'));
				var s = document.createElement('span'); s.textContent = 'פרויקט חדש מהמאגר שלנו'; box.appendChild(s);
				new maplibregl.Popup({ closeButton: false, offset: 8 }).setLngLat(f.geometry.coordinates).setDOMContent(box).addTo(map);
			});
			map.on('mouseenter', 'nldm-pts', function () { map.getCanvas().style.cursor = 'pointer'; });
			map.on('mouseleave', 'nldm-pts', function () { map.getCanvas().style.cursor = ''; });
		}).catch(function () {});
	}
	function initMap() {
		var css = document.createElement('link'); css.rel = 'stylesheet'; css.href = D.mlCss; document.head.appendChild(css);
		var js = document.createElement('script'); js.src = D.mlJs; js.async = true;
		js.onload = function () {
			var box = document.getElementById('nldm-map'); box.innerHTML = '';
			map = new maplibregl.Map({ container: box, style: D.style, center: [34.82, 32.07], zoom: 10.4, pitch: 52, bearing: -14,
				attributionControl: { compact: true }, cooperativeGestures: window.innerWidth < 768, maxPitch: 70 });
			map.on('load', function () {
				addLayers();
				deals.forEach(function (d) {
					markers[d.id] = new maplibregl.Marker({ element: tagEl(d), anchor: 'bottom' }).setLngLat([d.lng, d.lat]).addTo(map);
				});
				var center = deals.filter(function (d) { return d.lat > 31.85 && d.lat < 32.25 && d.lng < 35; });
				fitTo(center.length ? center : deals);
				declutter();
				setTimeout(function () { var h = byId[D.hotId]; if (h && markers[h.id] && !RM) { var r = tagOf(h.id).getBoundingClientRect(); if (r.top > 0 && r.top < window.innerHeight) { burst(r.left + r.width / 2, r.top, h.color, true); } } }, 1500);
			});
			map.on('move', declutter);
		};
		document.head.appendChild(js);
	}
	$$('.nldm-mapbar button').forEach(function (b) {
		b.addEventListener('click', function () {
			if (!map) { return; }
			var act = b.dataset.act;
			if (act === 'tilt') { S.tilt = !S.tilt; map.easeTo({ pitch: S.tilt ? 52 : 0, bearing: S.tilt ? -14 : 0, duration: RM ? 0 : 800 }); b.textContent = S.tilt ? 'מבט מלמעלה' : 'תלת ממד'; }
			if (act === 'all') { fitTo(deals.filter(shown)); }
			if (act === 'near' && navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(function (p) { map.easeTo({ center: [p.coords.longitude, p.coords.latitude], zoom: 12.5, duration: RM ? 0 : 1000 }); });
			}
		});
	});
	/* ---- the true-discount calculator: present value of the deal's payment schedule against a regular developer schedule ---- */
	var calc = $('#nldm-calc');
	var C = null;
	function calcFrom(d) {
		var c = (d && d.calc) || {};
		var P = (d && d.price) || 2500000;
		var s = d && d.firstAbs != null && d.price ? Math.round(100 * d.firstAbs / d.price) : (d && d.first != null ? Math.round(100 * d.first) : 20);
		return { id: d ? d.id : 'mine', P: P, s: s, T: c.T || 30, i: 3, r: 5, R: c.R || 0, M: c.M || 0, prem: 0, cut: c.cut || 0, ex: !!c.ex, tail: c.tail || 0, tailM: c.tailM || 0, tailAll: !!c.tailAll, same: !!c.same };
	}
	function solve(q) {
		var m = q.r / 100 / 12, ig = Math.pow(1 + q.i / 100, 1 / 12) - 1, d = function (k) { return Math.pow(1 + m, -k); };
		var reg0 = 0.2 * q.P, regI = 0, k, pay = 0.8 * q.P / q.T;
		for (k = 1; k <= q.T; k++) { reg0 += pay * d(k); regI += pay * 0.5 * (Math.pow(1 + ig, k) - 1) * d(k); }
		var first = q.s / 100 * q.P, tail = q.tailAll ? q.P - first : (q.tail || 0) / 100 * q.P, mid = q.P - first - tail;
		/* a tail is paid tailM months after occupancy, without interest or indexation (Gindi 20/50/30, Hagag: the balance 3 years after) */
		var deal0 = first + mid * d(q.T) + tail * d(q.T + (q.tailM || 0)), dealI = q.ex ? 0 : mid * 0.5 * (Math.pow(1 + ig, q.T) - 1) * d(q.T);
		var rent = 0; for (k = 1; k <= q.M; k++) { rent += q.R * d(k); }
		/* same: no payment schedule was published for this deal, so it is counted as a regular schedule and only its published benefit counts */
		var tv = q.same ? 0 : reg0 - deal0, idx = q.same ? 0 : regI - dealI, total = tv + idx + rent + q.cut - q.prem;
		return { tv: tv, idx: idx, rent: rent, cut: q.cut, prem: q.prem, total: total, pct: Math.round(1000 * total / q.P) / 10 };
	}
	function money(n) { var a = Math.abs(n), t = a >= 1000000 ? (Math.round(a / 10000) / 100) + ' מיליון ₪' : Math.round(a / 1000).toLocaleString('he-IL') + ' אלף ₪'; return (n < -500 ? '−' : '') + t; }
	var FIELDS = [
		['P', 'מחיר הדירה', 800000, 12000000, 10000, money], ['s', 'משלמים בחתימה', 0, 60, 1, function (v) { return v + '%'; }],
		['T', 'חודשים עד האכלוס', 6, 60, 1, function (v) { return v + ' חודשים'; }], ['i', 'מדד תשומות הבנייה לשנה', 0, 8, 0.5, function (v) { return v + '%'; }],
		['r', 'ריבית אלטרנטיבית (משכנתא)', 2, 8, 0.25, function (v) { return v + '%'; }], ['R', 'שכר דירה מהיזם לחודש', 0, 15000, 500, money],
		['M', 'לכמה חודשים', 0, 60, 1, String], ['cut', 'הנחה ישירה במחיר', 0, 800000, 10000, money], ['prem', 'תוספת למחיר בגלל המבצע', 0, 800000, 10000, money]
	];
	function renderCalc(anim) {
		if (!calc || !C) { return; }
		var R = solve(C);
		var tot = calc.querySelector('.nldm-calc-total'), gn = calc.querySelector('.nldm-gauge-n'), g1 = calc.querySelector('.g1');
		roll(tot, Number(tot.dataset.v || 0), Math.round(R.total), money); tot.dataset.v = Math.round(R.total);
		gn.textContent = R.pct + '%';
		calc.querySelector('.nldm-calc-pct').textContent = 'שהם ' + R.pct + '% הנחה אמיתית ממחיר הדירה';
		g1.style.strokeDasharray = Math.max(0, Math.min(251, 251 * R.pct / 20)).toFixed(1) + ' 251';
		calc.classList.toggle('is-neg', R.total < 0);
		var parts = [
			[C.tail || C.tailAll ? 'כסף שנשאר אצלכם, גם אחרי האכלוס' : 'כסף שנשאר אצלכם עד האכלוס', R.tv, C.tail || C.tailAll ? 'חלק מהמחיר משולם ' + Math.round(C.tailM / 12) + ' שנים אחרי האכלוס, בלי ריבית והצמדה' : 'משלמים מאוחר יותר, והכסף עובד בינתיים בריבית ' + C.r + '%', 'a'],
			[R.idx >= 0 ? 'הצמדה למדד שנחסכה' : 'הצמדה נוספת בגלל הדחייה', R.idx, C.ex ? 'פטור מלא מהצמדה ליתרה' : 'בלי פטור, היתרה הדחויה צמודה עד האכלוס', 'b'],
			['שכר דירה או הטבה חודשית מהיזם', R.rent, C.M ? C.M + ' חודשים של ' + (C.same ? 'עד ' : '') + money(C.R) + (C.same ? ', לפי פרסום. לוח התשלומים לא פורסם ולכן נספר כרגיל' : '') : 'אין במבצע הזה', 'c'],
			['הנחה ישירה במחיר', R.cut, R.cut ? 'כפי שפורסם' : 'אין במבצע הזה', 'c'],
			['תוספת למחיר בגלל המבצע', -R.prem, 'שאלו את היזם מחיר בלי המבצע', 'd']
		];
		var max = Math.max.apply(null, parts.map(function (p) { return Math.abs(p[1]); }).concat([1]));
		var box = calc.querySelector('.nldm-calc-parts'); box.innerHTML = '';
		parts.forEach(function (p, n) {
			if (!p[1] && n >= 2) { return; }
			var row = document.createElement('div'); row.className = 'nldm-part';
			row.innerHTML = '<div class="l"><span></span><b></b></div><div class="t"><i class="' + p[3] + (p[1] < 0 ? ' is-neg' : '') + '"></i></div><small></small>';
			row.querySelector('span').textContent = p[0]; row.querySelector('b').textContent = money(p[1]);
			row.querySelector('b').className = p[1] < 0 ? 'is-neg' : '';
			row.querySelector('small').textContent = p[2];
			box.appendChild(row);
			var bar = row.querySelector('i');
			setTimeout(function () { bar.style.width = Math.max(2, Math.round(100 * Math.abs(p[1]) / max)) + '%'; }, RM || !anim ? 0 : 40 + n * 90);
		});
		FIELDS.forEach(function (f) { var o = calc.querySelector('[data-o="' + f[0] + '"]'); if (o) { o.textContent = f[5](C[f[0]]); } var inp = calc.querySelector('[data-k="' + f[0] + '"]'); if (inp && Number(inp.value) !== C[f[0]]) { inp.value = C[f[0]]; } });
		var ex = calc.querySelector('.nldm-ex'); if (ex) { ex.textContent = C.ex ? 'פטור מהצמדה: כן' : 'פטור מהצמדה: לא'; ex.setAttribute('aria-pressed', C.ex ? 'true' : 'false'); }
	}
	function calcPick(id) {
		C = calcFrom(byId[id] || null);
		$$('.nldm-calc-pre button').forEach(function (b) { var on = b.dataset.id === id; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
		renderCalc(true);
	}
	if (calc) {
		var pre = calc.querySelector('.nldm-calc-pre');
		deals.filter(function (d) { return d.calcOk && d.price; }).concat([{ id: 'mine', project: 'המבצע שלי' }]).forEach(function (d) {
			var b = document.createElement('button'); b.type = 'button'; b.dataset.id = d.id;
			b.textContent = d.id === 'mine' ? 'המבצע שלי' : d.dev + ' · ' + d.project.split(',')[0];
			b.addEventListener('click', function () { calcPick(d.id); });
			pre.appendChild(b);
		});
		var fl = calc.querySelector('.nldm-calc-fields');
		FIELDS.forEach(function (f) {
			var w = document.createElement('div'); w.className = 'nldm-field';
			w.innerHTML = '<div><label></label><output></output></div><input type="range">';
			var id = 'nldm-c-' + f[0];
			w.querySelector('label').textContent = f[1]; w.querySelector('label').htmlFor = id;
			w.querySelector('output').dataset.o = f[0];
			var inp = w.querySelector('input'); inp.id = id; inp.min = f[2]; inp.max = f[3]; inp.step = f[4]; inp.dataset.k = f[0];
			inp.addEventListener('input', function () { C[f[0]] = Number(inp.value); renderCalc(false); });
			fl.appendChild(w);
		});
		var exb = document.createElement('button'); exb.type = 'button'; exb.className = 'nldm-ex';
		exb.addEventListener('click', function () { C.ex = !C.ex; renderCalc(false); });
		fl.appendChild(exb);
		calcPick((deals.filter(function (d) { return d.calcOk && d.price; })[0] || {}).id || 'mine');
	}
	var toCalc = $('.nldm-tocalc');
	if (toCalc) { toCalc.addEventListener('click', function () { calcPick(byId[S.sel] && byId[S.sel].calcOk && byId[S.sel].price ? S.sel : 'mine'); calc.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' }); }); }

	var mapBox = document.getElementById('nldm-map');
	if ('IntersectionObserver' in window) {
		var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { io.disconnect(); initMap(); } }, { rootMargin: '300px' });
		io.observe(mapBox);
	} else { initMap(); }
	counts(); paintStatus(false); renderSheet(false);
})();
