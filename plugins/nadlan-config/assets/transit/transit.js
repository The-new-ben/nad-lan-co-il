/* nadlan-config - the transit map (HAD-816). MapLibre + OpenFreeMap positron, the same stack as the deals map; no keys.
   Lines and stations: transit-data.json (official open data, see inc/transit.php). Projects: assets/deals/projects.json.
   The map never holds the page's scroll: phones move it with two fingers, a mouse zooms only after resting on it or a click. */
(function () {
	'use strict';
	var C = window.NLTR_CFG || {};
	var EN = C.lang === 'en';
	var root = document.getElementById('nltr');
	if (!root) { return; }
	var box = document.getElementById('nltr-map'), card = document.getElementById('nltr-card');
	var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
	var W = EN ? { open: 'running', build: 'under construction', plan: 'planned', walk: 'min walk', near: 'New projects within walking distance', none: 'No project from our catalogue within a 15 minute walk.', other: 'Other stations within a 15 minute walk', nearest: 'Nearest station on each line', close: 'Close', est: 'Walking minutes: an estimate from the straight-line distance at about 80 metres a minute.', under: 'underground station', proj: 'New project', page: 'To the project page', addr: 'Search this address', noaddr: 'No address found', ring: 'min', src: 'Station data: Ministry of Transport', planned: 'Planned positions (file of 12.2021), may change.' }
		: { open: 'פועל', build: 'בבנייה', plan: 'מתוכנן', walk: 'דק׳ הליכה', near: 'פרויקטים חדשים במרחק הליכה', none: 'אין פרויקט מהקטלוג שלנו עד 15 דקות הליכה מהתחנה.', other: 'תחנות נוספות עד 15 דקות הליכה', nearest: 'התחנה הקרובה בכל קו', close: 'סגירה', est: 'דקות הליכה: הערכה לפי מרחק בקו אווירי, בקצב של כ־80 מטר לדקה.', under: 'תחנה תת־קרקעית', proj: 'פרויקט חדש', page: 'לעמוד הפרויקט', addr: 'חיפוש הכתובת', noaddr: 'לא נמצאה כתובת', ring: 'דק׳', src: 'נתוני התחנות: משרד התחבורה', planned: 'מיקום מתוכנן (קובץ 12.2021), עשוי להשתנות.' };
	var T = null, P = [], map = null, lines = {}, stations = [], byId = {}, show = { lrt: true, metro: true, rail: true, proj: true };
	function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) { e.className = cls; } if (txt != null) { e.textContent = txt; } return e; }
	function m(a, b) { var k = Math.cos((a[1] + b[1]) / 2 * Math.PI / 180); return Math.sqrt(Math.pow((a[0] - b[0]) * 111320 * k, 2) + Math.pow((a[1] - b[1]) * 110540, 2)); }
	function walk(d) { return Math.max(1, Math.round(d * 1.3 / 80)); }
	function sname(s) { return EN && s.en ? s.en : s.he; }
	function lname(id) { var l = lines[id]; return l ? (EN ? l.en : l.he) : ''; }
	function kindOf(s) { return s.kind === 'metro' ? 'metro' : s.kind; }
	function stOn(s) { return show[kindOf(s)]; }

	/* ---------- data ---------- */
	function getJSON(u) { return fetch(u, { credentials: 'omit' }).then(function (r) { if (!r.ok) { throw new Error(r.status); } return r.json(); }); }
	var ready = Promise.all([getJSON(C.data), getJSON(C.projects).catch(function () { return []; })]).then(function (r) {
		T = r[0];
		T.lines.forEach(function (l) { lines[l.id] = l; });
		stations = T.stations; stations.forEach(function (s) { byId[s.id] = s; });
		/* the same choice as nltr_projects() in PHP: no private review page; Hebrew pages, or the English twin on /en/ */
		var base = {}, twin = {}, order = [];
		(r[1] || []).forEach(function (p) {
			if (!p || p.length < 4 || String(p[3]).indexOf('sandbox') >= 0 || !(p[1] > 29 && p[1] < 34)) { return; }
			var mm = /^(.*)-(en|fr|ru|ar)\/$/.exec(String(p[3]));
			if (mm) { if (mm[2] === 'en') { twin[mm[1] + '/'] = p; } return; }
			if (!base[p[3]]) { order.push(p[3]); } base[p[3]] = p;
		});
		/* a point shared by 3 or more projects is a city centre placed for lack of an address: left out (as in PHP) */
		var cnt = {}; function ck(p) { return p[0].toFixed(4) + ',' + p[1].toFixed(4); }
		order.forEach(function (k) { var c = ck(base[k]); cnt[c] = (cnt[c] || 0) + 1; });
		order = order.filter(function (k) { return cnt[ck(base[k])] < 3; });
		P = order.map(function (k, i) { var p = (EN && twin[k]) ? twin[k] : base[k]; return { id: 'p' + i, p: [p[0], p[1]], name: String(p[2]), url: String(p[3]) }; });
		P.forEach(function (p) { p.best = nearestByKind(p.p); });
	});
	function nearestByKind(pt) {
		var best = {};
		stations.forEach(function (s) {
			if (s.line === 'red-ext') { return; }
			var k = s.kind === 'lrt' ? s.line : s.kind; // per light-rail line, one Metro, one rail
			var d = m(pt, s.p);
			if (!best[k] || d < best[k].d) { best[k] = { d: d, s: s }; }
		});
		return best;
	}
	function bestLabel(p) {
		var b = null;
		Object.keys(p.best).forEach(function (k) { var x = p.best[k]; if (x.s.status !== 'plan' && (!b || x.d < b.d)) { b = x; } });
		if (!b) { return p.name; }
		return p.name + ' · ' + walk(b.d) + ' ' + (EN ? 'min to ' : 'דק׳ ל') + (b.s.kind === 'rail' ? (EN ? 'the train' : 'רכבת') : lname(b.s.line).replace(/^הקו /, ''));
	}

	/* ---------- the map ---------- */
	function circle(c, r, n) {
		var pts = [], k = Math.cos(c[1] * Math.PI / 180);
		for (var i = 0; i <= (n || 64); i++) { var a = i / (n || 64) * 2 * Math.PI; pts.push([c[0] + r * Math.cos(a) / (111320 * k), c[1] + r * Math.sin(a) / 110540]); }
		return pts;
	}
	function rings(c) {
		return { type: 'FeatureCollection', features: [15, 10, 5].map(function (min) {
			var r = min * 80 / 1.3;
			return { type: 'Feature', properties: { min: min, t: min + ' ' + W.ring }, geometry: { type: 'Polygon', coordinates: [circle(c, r)] } };
		}).concat([15, 10, 5].map(function (min) {
			var r = min * 80 / 1.3, k = Math.cos(c[1] * Math.PI / 180);
			return { type: 'Feature', properties: { t: min + ' ' + W.ring }, geometry: { type: 'Point', coordinates: [c[0], c[1] + r / 110540] } };
		})) };
	}
	function fcLines() {
		var f = [];
		T.lines.forEach(function (l) { l.paths.forEach(function (p) { f.push({ type: 'Feature', properties: { id: l.id, kind: l.kind, st: l.status, c: l.color }, geometry: { type: 'LineString', coordinates: p } }); }); });
		return { type: 'FeatureCollection', features: f };
	}
	var RANK = { open: 0, build: 1, plan: 2 };
	function fcStations() {
		/* an interchange (the same name within 250 m on two lines, e.g. אבן גבירול - ארלוזורוב on the Purple and Green lines) carries ONE
		   label on its most advanced line; the other dots stay, silent, so names never pile up */
		var silent = {};
		stations.forEach(function (a) {
			stations.forEach(function (b) {
				if (a === b || silent[a.id] || silent[b.id]) { return; }
				if (norm(a.he) === norm(b.he) && m(a.p, b.p) < 250) {
					silent[(RANK[b.status] > RANK[a.status] || (RANK[b.status] === RANK[a.status] && b.id > a.id)) ? b.id : a.id] = 1;
				}
			});
		});
		return { type: 'FeatureCollection', features: stations.map(function (s) {
			var l = lines[s.line] || {};
			var sub = s.kind === 'rail' ? (s.status === 'build' ? W.build : '') : (s.status === 'open' ? '' : W[s.status]);
			var t = silent[s.id] ? '' : sname(s);
			return { type: 'Feature', properties: { id: s.id, kind: s.kind, st: s.status, c: l.color || '#4b5a66', t: t, t2: t && sub ? t + '\n' + sub : t, r: s.kind === 'rail' ? 1 : 0 }, geometry: { type: 'Point', coordinates: s.p } };
		}) };
	}
	function fcProjects() {
		return { type: 'FeatureCollection', features: P.map(function (p) { return { type: 'Feature', properties: { id: p.id, t: bestLabel(p) }, geometry: { type: 'Point', coordinates: p.p } }; }) };
	}
	var FONT = ['Noto Sans Bold'], FONTR = ['Noto Sans Regular'];
	function addLayers() {
		map.addSource('tl', { type: 'geojson', data: fcLines() });
		map.addSource('ts', { type: 'geojson', data: fcStations() });
		map.addSource('tp', { type: 'geojson', data: fcProjects() });
		map.addSource('tr', { type: 'geojson', data: { type: 'FeatureCollection', features: [] } });
		map.addLayer({ id: 'tr-fill', type: 'fill', source: 'tr', filter: ['==', ['geometry-type'], 'Polygon'], paint: { 'fill-color': '#2f6f86', 'fill-opacity': 0.06 } });
		map.addLayer({ id: 'tr-line', type: 'line', source: 'tr', filter: ['==', ['geometry-type'], 'Polygon'], paint: { 'line-color': '#2f6f86', 'line-width': 1.2, 'line-dasharray': [3, 3] } });
		map.addLayer({ id: 'tl-rail', type: 'line', source: 'tl', filter: ['==', ['get', 'kind'], 'rail'], layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': '#4b5a66', 'line-width': ['interpolate', ['linear'], ['zoom'], 7, 1.4, 12, 3, 15, 4.5] } });
		map.addLayer({ id: 'tl-metro', type: 'line', source: 'tl', filter: ['==', ['get', 'kind'], 'metro'], layout: { 'line-join': 'round' }, paint: { 'line-color': ['get', 'c'], 'line-width': ['interpolate', ['linear'], ['zoom'], 9, 1.6, 12, 3, 15, 4.5], 'line-dasharray': [2.2, 1.6] } });
		map.addLayer({ id: 'tl-lrt-plan', type: 'line', source: 'tl', filter: ['all', ['==', ['get', 'kind'], 'lrt'], ['==', ['get', 'st'], 'plan']], paint: { 'line-color': ['get', 'c'], 'line-width': ['interpolate', ['linear'], ['zoom'], 9, 1.6, 15, 4], 'line-dasharray': [1.5, 1.5] } });
		map.addLayer({ id: 'tl-lrt', type: 'line', source: 'tl', filter: ['all', ['==', ['get', 'kind'], 'lrt'], ['!=', ['get', 'st'], 'plan']], layout: { 'line-cap': 'round', 'line-join': 'round' }, paint: { 'line-color': ['get', 'c'], 'line-width': ['interpolate', ['linear'], ['zoom'], 9, ['case', ['==', ['get', 'st'], 'open'], 2.6, 2], 12, ['case', ['==', ['get', 'st'], 'open'], 4.4, 3.4], 15, 6] } });
		map.addLayer({ id: 'tp-dot', type: 'circle', source: 'tp', minzoom: 10.5, paint: { 'circle-radius': ['interpolate', ['linear'], ['zoom'], 11, 2.4, 15, 5], 'circle-color': '#14212b', 'circle-opacity': 0.75, 'circle-stroke-color': '#fff', 'circle-stroke-width': 1 } });
		map.addLayer({ id: 'ts-dot', type: 'circle', source: 'ts', paint: {
			'circle-radius': ['interpolate', ['linear'], ['zoom'], 8, ['case', ['==', ['get', 'r'], 1], 3, 1.6], 12, ['case', ['==', ['get', 'st'], 'plan'], 3.2, 4.4], 15, 7],
			'circle-color': '#ffffff', 'circle-stroke-color': ['get', 'c'], 'circle-stroke-width': ['interpolate', ['linear'], ['zoom'], 8, 1.2, 12, 2.4, 15, 3.4] } });
		map.addLayer({ id: 'tp-lab', type: 'symbol', source: 'tp', minzoom: 13.4, layout: { 'text-field': ['get', 't'], 'text-font': FONTR, 'text-size': 11.5, 'text-variable-anchor': ['top', 'bottom'], 'text-radial-offset': 0.8, 'text-padding': 6, 'text-max-width': 14, 'text-optional': true },
			paint: { 'text-color': '#14212b', 'text-halo-color': '#ffffff', 'text-halo-width': 1.6 } });
		map.addLayer({ id: 'ts-lab', type: 'symbol', source: 'ts', layout: {
			/* collisions (Ben's taste: one clear label, never a pile): MapLibre places by symbol-sort-key (running first, then under construction,
			   then planned), tries four anchors, and hides a label that would touch another; planned stations and the state line come with zoom */
			'text-field': ['step', ['zoom'], ['case', ['==', ['get', 'st'], 'plan'], '', ['get', 't']], 12.4, ['get', 't'], 13.8, ['get', 't2']], 'text-font': FONT,
			'text-size': ['interpolate', ['linear'], ['zoom'], 10, 10.5, 14, 13],
			'text-variable-anchor': ['top', 'bottom', 'right', 'left'], 'text-radial-offset': 0.75, 'text-justify': 'auto', 'text-padding': 7,
			'text-allow-overlap': false, 'text-ignore-placement': false, 'text-optional': true, 'text-max-width': 9,
			'symbol-sort-key': ['case', ['==', ['get', 'st'], 'open'], 0, ['==', ['get', 'st'], 'build'], 1, 2] },
			paint: { 'text-color': '#14212b', 'text-halo-color': '#ffffff', 'text-halo-width': 1.8 }, minzoom: 10.6 });
		map.addLayer({ id: 'tr-lab', type: 'symbol', source: 'tr', filter: ['==', ['geometry-type'], 'Point'], layout: { 'text-field': ['get', 't'], 'text-font': FONT, 'text-size': 11, 'text-allow-overlap': true }, paint: { 'text-color': '#255c70', 'text-halo-color': '#fff', 'text-halo-width': 1.6 } });
		['ts-dot', 'ts-lab'].forEach(function (id) {
			map.on('click', id, function (e) { var f = e.features && e.features[0]; if (f) { openStation(byId[f.properties.id]); } });
			map.on('mouseenter', id, function () { map.getCanvas().style.cursor = 'pointer'; });
			map.on('mouseleave', id, function () { map.getCanvas().style.cursor = ''; });
		});
		['tp-dot', 'tp-lab'].forEach(function (id) {
			map.on('click', id, function (e) { var f = e.features && e.features[0]; if (f) { openProject(P[+f.properties.id.slice(1)]); } });
			map.on('mouseenter', id, function () { map.getCanvas().style.cursor = 'pointer'; });
			map.on('mouseleave', id, function () { map.getCanvas().style.cursor = ''; });
		});
		applyShow();
		fromHash();
	}
	function applyShow() {
		if (!map || !map.getLayer('ts-dot')) { return; }
		var kinds = Object.keys(show).filter(function (k) { return show[k] && k !== 'proj'; });
		var lf = ['in', ['get', 'kind'], ['literal', kinds]];
		map.setFilter('tl-rail', ['all', ['==', ['get', 'kind'], 'rail'], lf]);
		map.setFilter('tl-metro', ['all', ['==', ['get', 'kind'], 'metro'], lf]);
		map.setFilter('tl-lrt', ['all', ['==', ['get', 'kind'], 'lrt'], ['!=', ['get', 'st'], 'plan'], lf]);
		map.setFilter('tl-lrt-plan', ['all', ['==', ['get', 'kind'], 'lrt'], ['==', ['get', 'st'], 'plan'], lf]);
		map.setFilter('ts-dot', lf); map.setFilter('ts-lab', lf);
		['tp-dot', 'tp-lab'].forEach(function (id) { map.setLayoutProperty(id, 'visibility', show.proj ? 'visible' : 'none'); });
	}
	function setRing(c) { if (map && map.getSource('tr')) { map.getSource('tr').setData(c ? rings(c) : { type: 'FeatureCollection', features: [] }); } }
	function fly(c, z) { if (!map) { return; } map.flyTo({ center: c, zoom: Math.max(map.getZoom(), z || 14.2), duration: RM ? 0 : 900, padding: padFor() }); }
	function padFor() { var w = window.innerWidth; return w >= 900 ? { right: EN ? 0 : 0, left: 0, top: 20, bottom: 20 } : { top: 10, bottom: Math.round(box.clientHeight * 0.45), left: 10, right: 10 }; }

	/* ---------- the card ---------- */
	function head(kicker, color, title, sub) {
		card.innerHTML = '';
		var top = el('div', 'nltr-card-top'), k = el('div', 'nltr-kick'), sw = el('i', 'nltr-sw'); sw.style.background = color; k.appendChild(sw); k.appendChild(document.createTextNode(kicker));
		var x = el('button', 'nltr-x', '×'); x.type = 'button'; x.setAttribute('aria-label', W.close); x.addEventListener('click', closeCard);
		var tt = el('div'); tt.appendChild(k); tt.appendChild(el('h2', 'nltr-card-h', title)); if (sub) { tt.appendChild(el('p', 'nltr-card-sub', sub)); }
		top.appendChild(tt); top.appendChild(x); card.appendChild(top);
	}
	function showCard() {
		card.hidden = false; root.classList.add('has-card'); card.scrollTop = 0;
		if (window.innerWidth >= 900) { return; }
		/* the sheet sits at the bottom of the map; scroll the page so the map's bottom edge rests above the floating WhatsApp bar */
		if (document.activeElement && document.activeElement.blur && document.activeElement.id === 'nltr-q') { document.activeElement.blur(); }
		setTimeout(function () {
			var r = card.parentNode.getBoundingClientRect(), dy = r.bottom - (window.innerHeight - barGap());
			if (Math.abs(dy) > 8) { window.scrollTo(0, window.scrollY + dy); }
		}, 60);
	}
	function barGap() {
		/* the height the site's own floating bars take at the bottom of the screen (measured, so a change in the bar needs no release) */
		var h = 0, els = document.querySelectorAll('body *');
		for (var i = 0; i < els.length; i++) {
			var e = els[i]; if (root.contains(e)) { continue; }
			var cs = getComputedStyle(e); if (cs.position !== 'fixed' || cs.display === 'none' || cs.visibility === 'hidden') { continue; }
			var b = e.getBoundingClientRect(); if (b.width < 120 || b.height < 30 || b.height > 160 || b.top < window.innerHeight * 0.55 || b.bottom > window.innerHeight + 2) { continue; }
			h = Math.max(h, window.innerHeight - b.top);
		}
		return Math.min(200, h + 10);
	}
	function closeCard() { card.hidden = true; root.classList.remove('has-card'); setRing(null); try { history.replaceState(null, '', location.pathname + location.search); } catch (e) { /* fine */ } }
	function openStation(s) {
		if (!s) { return; }
		var l = lines[s.line] || {};
		var stWord = s.kind === 'rail' ? (s.status === 'build' ? W.build : W.open) : W[s.status];
		var sub = [EN ? (s.he !== sname(s) ? s.he : '') : (s.en || ''), s.under ? W.under : ''].filter(Boolean).join(' · ');
		head(lname(s.line) + ' · ' + stWord, l.color || '#4b5a66', (EN ? '' : 'תחנת ') + sname(s) + (EN ? ' station' : ''), sub);
		if (s.status === 'plan' && s.kind === 'metro') { card.appendChild(el('p', 'nltr-note', W.planned)); }
		var others = stations.filter(function (o) { return o !== s && o.line !== s.line && m(o.p, s.p) * 1.3 / 80 <= 15; }).map(function (o) { return { o: o, d: m(o.p, s.p) }; }).sort(function (a, b) { return a.d - b.d; }).slice(0, 6);
		if (others.length) {
			card.appendChild(el('h3', 'nltr-card-h3', W.other));
			var chips = el('div', 'nltr-mini');
			others.forEach(function (x) {
				var b = el('button', 'nltr-mchip'); b.type = 'button'; var sw = el('i', 'nltr-sw'); sw.style.background = (lines[x.o.line] || {}).color; b.appendChild(sw);
				b.appendChild(document.createTextNode(sname(x.o) + ' · ' + walk(x.d) + ' ' + W.walk));
				b.addEventListener('click', function () { openStation(x.o); fly(x.o.p); });
				chips.appendChild(b);
			});
			card.appendChild(chips);
		}
		var near = P.map(function (p) { return { p: p, d: m(p.p, s.p) }; }).filter(function (x) { return walk(x.d) <= 15; }).sort(function (a, b) { return a.d - b.d; }).slice(0, 12);
		card.appendChild(el('h3', 'nltr-card-h3', W.near));
		if (!near.length) { card.appendChild(el('p', 'nltr-note', W.none)); }
		else {
			var ol = el('ol', 'nltr-list');
			near.forEach(function (x) {
				var li = el('li'), a = el('a', null, x.p.name); a.href = x.p.url; li.appendChild(a); li.appendChild(el('span', 'nltr-min', walk(x.d) + ' ' + W.walk)); ol.appendChild(li);
			});
			card.appendChild(ol);
		}
		card.appendChild(el('p', 'nltr-fine', W.est + ' ' + W.src + '.'));
		showCard(); setRing(s.p); fly(s.p);
		try { history.replaceState(null, '', '#st-' + s.id); } catch (e) { /* fine */ }
	}
	function openProject(p) {
		if (!p) { return; }
		head(W.proj, '#14212b', p.name, '');
		var a = el('a', 'nltr-go', W.page); a.href = p.url; card.appendChild(a);
		card.appendChild(el('h3', 'nltr-card-h3', W.nearest));
		var ol = el('ol', 'nltr-list');
		Object.keys(p.best).map(function (k) { return p.best[k]; }).filter(function (x) { return show[kindOf(x.s)] && walk(x.d) <= 40; }).sort(function (a, b) { return a.d - b.d; }).forEach(function (x) {
			var li = el('li'), b = el('button', 'nltr-link'); b.type = 'button';
			var sw = el('i', 'nltr-sw'); sw.style.background = (lines[x.s.line] || {}).color; b.appendChild(sw);
			b.appendChild(document.createTextNode(sname(x.s) + ' · ' + lname(x.s.line) + ' · ' + (x.s.kind === 'rail' ? (x.s.status === 'build' ? W.build : W.open) : W[x.s.status])));
			b.addEventListener('click', function () { openStation(x.s); });
			li.appendChild(b); li.appendChild(el('span', 'nltr-min', walk(x.d) + ' ' + W.walk)); ol.appendChild(li);
		});
		card.appendChild(ol);
		card.appendChild(el('p', 'nltr-fine', W.est));
		showCard(); setRing(p.p); fly(p.p, 14.6);
		try { history.replaceState(null, '', '#pr-' + p.id); } catch (e) { /* fine */ }
	}
	function fromHash() {
		var h = location.hash || '';
		if (h.indexOf('#st-') === 0 && byId[decodeURIComponent(h.slice(4))]) { openStation(byId[decodeURIComponent(h.slice(4))]); }
	}

	/* ---------- search: stations and projects here, an address through Photon (OpenStreetMap) on request ---------- */
	var form = root.querySelector('.nltr-search'), q = document.getElementById('nltr-q'), res = root.querySelector('.nltr-res');
	function norm(s) { return String(s || '').toLowerCase().replace(/["'״׳\-–]/g, '').replace(/\s+/g, ' ').trim(); }
	function results(v) {
		var n = norm(v); if (n.length < 2) { return []; }
		var out = [];
		stations.forEach(function (s) { if (norm(s.he).indexOf(n) >= 0 || norm(s.en).indexOf(n) >= 0) { out.push({ t: sname(s) + ' · ' + lname(s.line), s: s }); } });
		P.forEach(function (p) { if (norm(p.name).indexOf(n) >= 0) { out.push({ t: p.name, p: p }); } });
		return out.slice(0, 8);
	}
	function pick(r) {
		res.hidden = true;
		if (r.s) { openStation(r.s); } else if (r.p) { openProject(r.p); } else if (r.addr) { openAddress(r.addr, r.t); }
	}
	function list(rs, withAddr) {
		res.innerHTML = '';
		rs.forEach(function (r) { var li = el('li'), b = el('button', null, r.t); b.type = 'button'; b.addEventListener('click', function () { pick(r); }); li.appendChild(b); res.appendChild(li); });
		if (withAddr) { var li = el('li'), b = el('button', 'is-addr', W.addr + ': ' + q.value.trim()); b.type = 'button'; b.addEventListener('click', geocode); li.appendChild(b); res.appendChild(li); }
		res.hidden = !res.children.length;
	}
	var qt = 0;
	if (q) {
		q.addEventListener('input', function () { clearTimeout(qt); qt = setTimeout(function () { ready.then(function () { list(results(q.value), q.value.trim().length > 2); }); }, 120); });
		form.addEventListener('submit', function (e) { e.preventDefault(); ready.then(function () { var r = results(q.value); if (r.length) { pick(r[0]); } else { geocode(); } }); });
		document.addEventListener('click', function (e) { if (!form.contains(e.target)) { res.hidden = true; } });
	}
	function geocode() {
		var v = q.value.trim(); if (v.length < 3 || !C.geo) { return; }
		var u = C.geo + '?limit=5&lang=' + (EN ? 'en' : 'default') + '&bbox=34.2,29.4,35.95,33.35&q=' + encodeURIComponent(v);
		fetch(u, { credentials: 'omit', referrerPolicy: 'no-referrer' }).then(function (r) { return r.json(); }).then(function (d) {
			var f = (d && d.features) || [];
			if (!f.length) { list([{ t: W.noaddr }], false); return; }
			list(f.map(function (x) { var p = x.properties || {}; return { t: [p.name, p.street && p.housenumber ? p.street + ' ' + p.housenumber : p.street, p.city].filter(Boolean).join(', '), addr: x.geometry.coordinates }; }), false);
		}).catch(function () { list([{ t: W.noaddr }], false); });
	}
	function openAddress(c, label) {
		var p = { id: 'addr', p: c, name: label, url: '' };
		p.best = nearestByKind(c);
		head(EN ? 'Address' : 'כתובת', '#2f6f86', label, '');
		card.appendChild(el('h3', 'nltr-card-h3', W.nearest));
		var ol = el('ol', 'nltr-list');
		Object.keys(p.best).map(function (k) { return p.best[k]; }).sort(function (a, b) { return a.d - b.d; }).slice(0, 7).forEach(function (x) {
			var li = el('li'), b = el('button', 'nltr-link'); b.type = 'button';
			var sw = el('i', 'nltr-sw'); sw.style.background = (lines[x.s.line] || {}).color; b.appendChild(sw);
			b.appendChild(document.createTextNode(sname(x.s) + ' · ' + lname(x.s.line) + ' · ' + (x.s.kind === 'rail' ? (x.s.status === 'build' ? W.build : W.open) : W[x.s.status])));
			b.addEventListener('click', function () { openStation(x.s); });
			li.appendChild(b); li.appendChild(el('span', 'nltr-min', walk(x.d) + ' ' + W.walk)); ol.appendChild(li);
		});
		card.appendChild(ol); card.appendChild(el('p', 'nltr-fine', W.est));
		showCard(); setRing(c); fly(c, 14.6);
	}

	/* ---------- chips ---------- */
	Array.prototype.forEach.call(root.querySelectorAll('.nltr-chip'), function (b) {
		b.addEventListener('click', function () { var k = b.dataset.k; show[k] = !show[k]; b.setAttribute('aria-pressed', show[k] ? 'true' : 'false'); applyShow(); });
	});

	/* ---------- the map never holds the page's scroll ---------- */
	function wheelIntent(mp, area) {
		if (!window.matchMedia || !matchMedia('(hover: hover) and (pointer: fine)').matches || window.innerWidth < 768) { return; }
		var inAt = 0, page = 0, on = false, hint = null, ht = 0;
		function arm(v) { on = v; try { if (v) { mp.scrollZoom.enable(); } else { mp.scrollZoom.disable(); } } catch (e) { /* gone */ } }
		arm(false);
		addEventListener('scroll', function () { page = Date.now(); }, { passive: true });
		area.addEventListener('mouseenter', function () { inAt = Date.now(); });
		area.addEventListener('mouseleave', function () { inAt = 0; arm(false); });
		area.addEventListener('mousedown', function () { arm(true); });
		area.addEventListener('wheel', function () {
			if (on) { return; }
			var n = Date.now();
			if (inAt && n - inAt > 500 && n - page > 400) { arm(true); return; }
			if (!hint) { hint = el('div', 'nltr-whint', EN ? 'Rest the pointer on the map, or click it, to zoom with the wheel' : 'השאירו את העכבר על המפה, או לחצו עליה, כדי להתקרב בגלגלת'); hint.setAttribute('aria-hidden', 'true'); area.appendChild(hint); }
			hint.classList.add('is-on'); clearTimeout(ht); ht = setTimeout(function () { hint.classList.remove('is-on'); }, 1400);
		}, { capture: true, passive: true });
	}
	function initMap() {
		var css = el('link'); css.rel = 'stylesheet'; css.href = C.mlCss; document.head.appendChild(css);
		var js = el('script'); js.src = C.mlJs; js.async = true;
		js.onload = function () {
			ready.then(function () {
				box.innerHTML = '';
				try { if (!EN && C.rtl && maplibregl.getRTLTextPluginStatus && maplibregl.getRTLTextPluginStatus() === 'unavailable') { var rp = maplibregl.setRTLTextPlugin(C.rtl, false); if (rp && rp.catch) { rp.catch(function () {}); } } } catch (e) { /* labels stay as drawn */ }
				var phone = window.innerWidth < 768;
				map = new maplibregl.Map({ container: box, style: C.style, center: [34.81, 32.07], zoom: phone ? 11.2 : 11.6, minZoom: 7, maxZoom: 17.5,
					attributionControl: { compact: true }, cooperativeGestures: phone, dragRotate: false, pitchWithRotate: false,
					locale: EN ? {} : { 'CooperativeGesturesHandler.MobileHelpText': 'כדי להזיז את המפה, השתמשו בשתי אצבעות', 'CooperativeGesturesHandler.WindowsHelpText': 'כדי להתקרב, החזיקו Ctrl וגללו', 'CooperativeGesturesHandler.MacHelpText': 'כדי להתקרב, החזיקו ⌘ וגללו', 'NavigationControl.ZoomIn': 'הגדלה', 'NavigationControl.ZoomOut': 'הקטנה' } });
				map.addControl(new maplibregl.NavigationControl({ showCompass: false }), EN ? 'bottom-right' : 'bottom-left');
				map.touchZoomRotate.disableRotation();
				map.on('load', function () {
					/* calm base: the positron style keeps its own labels; ours sit on top in the lines' colours */
					try { addLayers(); } catch (e) { if (window.console) { console.warn('nltr layers', e); } }
				});
				wheelIntent(map, box);
			}).catch(function () { box.innerHTML = ''; box.appendChild(el('p', 'nltr-wait', EN ? 'The map could not load. The station lists below have every station.' : 'המפה לא נטענה. ברשימות למטה יש את כל התחנות.')); });
		};
		document.head.appendChild(js);
	}
	if ('IntersectionObserver' in window) {
		var io = new IntersectionObserver(function (en) { if (en.some(function (x) { return x.isIntersecting; })) { io.disconnect(); initMap(); } }, { rootMargin: '400px' });
		io.observe(box);
	} else { initMap(); }
	addEventListener('keydown', function (e) { if (e.key === 'Escape' && !card.hidden) { closeCard(); } });
}());
