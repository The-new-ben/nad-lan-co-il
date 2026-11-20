/* Rentals: the example portfolio on a 3D map. DESIGN LAB ONLY (HAD-795, Ben's order of 20.11.2026), not site code.
   The example landlord: two apartments in Kikar HaMedina, two more in Tel Aviv, Eilat, Cyprus, Greece, New York.
   Every name, address detail and number here is an EXAMPLE and the screen says so.
   The map key comes in the address (?t=...) and is never stored. ?view=world|il|tlv|<id>  ?filter=all|care|due|ok  ?still=1 */
(function () {
	"use strict";
	var q = new URLSearchParams(location.search), STILL = q.get("still") === "1";
	var P = [
		{ id: "k1", name: "כיכר המדינה · דירה 142", city: "תל אביב", region: "il", ll: [34.78985, 32.08672], rent: "21,500 ₪", st: "ok", line: "שכר הדירה נכנס ב-1.11", build: "kikar" },
		{ id: "k2", name: "כיכר המדינה · דירה 87", city: "תל אביב", region: "il", ll: [34.79035, 32.08655], rent: "17,800 ₪", st: "due", line: "שכר דירה בעוד 3 ימים", build: "kikar" },
		{ id: "t1", name: "ארלוזורוב 78 · דירה 7", city: "תל אביב", region: "il", ll: [34.78370, 32.08760], rent: "7,800 ₪", st: "ok", line: "הכול בסדר" },
		{ id: "t2", name: "פלורנטין 12 · דירה 3", city: "תל אביב", region: "il", ll: [34.77020, 32.05630], rent: "6,400 ₪", st: "ok", line: "הכול בסדר" },
		{ id: "e1", name: "שחמון 5 · דירה 5", city: "אילת", region: "il", ll: [34.93700, 29.55000], rent: "4,900 ₪", st: "care", line: "המזגן לא מקרר · יום 2 מתוך 30" },
		{ id: "c1", name: "לימסול, מול הים", city: "קפריסין", region: "med", ll: [33.04500, 34.68500], rent: "1,450 €", st: "ok", line: "הכול בסדר" },
		{ id: "g1", name: "אתונה, קולונאקי", city: "יוון", region: "med", ll: [23.74300, 37.97900], rent: "1,200 €", st: "ok", line: "הכול בסדר" },
		{ id: "n1", name: "מנהטן, רחוב 38", city: "ניו יורק", region: "ny", ll: [-73.98400, 40.75100], rent: "4,300 $", st: "ok", line: "הכול בסדר" }
	];
	var ST = { care: "צריך טיפול", due: "לתשלום השבוע", ok: "תקין" }, CH = { care: "טיפול", due: "לתשלום", ok: "תקין" }, WIDE0 = innerWidth >= 900;
	var VIEW = {
		world: { center: [-19.5, 30], zoom: WIDE0 ? 1.9 : 0.92, pitch: 0, bearing: 0 },
		il: { center: [34.86, 31.2], zoom: 6.3, pitch: 38, bearing: -8 },
		tlv: { center: [34.7825, 32.0760], zoom: 12.6, pitch: 55, bearing: -18 },
		med: { center: [28.5, 36.4], zoom: 5.1, pitch: 30, bearing: 0 }
	};
	var S = { filter: q.get("filter") || "all", sel: null, view: q.get("view") || "world" };
	var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
	var $ = function (s) { return document.querySelector(s); };
	var byId = function (id) { return P.find(function (p) { return p.id === id; }); };
	var shown = function (p) { return S.filter === "all" || p.st === S.filter; };
	var thumb = function (p) { return '<span class="pf-th pf-th--' + p.id + '"><img src="img/' + p.id + '.jpg" alt="" loading="eager" onerror="this.remove()"></span>'; };
	var badge = function (st) {
		if (st === "care") { return '<i class="pf-bd pf-bd--care" aria-hidden="true">!</i>'; }
		if (st === "due") { return '<i class="pf-bd pf-bd--due" aria-hidden="true"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="#14212b" stroke-width="1.7" stroke-linecap="round"><path d="M5 2v3l2 1.3"/></svg></i>'; }
		return '<i class="pf-bd pf-bd--ok" aria-hidden="true"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M2 5.3l2 2 4-4.4"/></svg></i>';
	};

	mapboxgl.accessToken = q.get("t") || "";
	/* Hebrew labels need the right-to-left text plugin BEFORE the first tiles are laid out, so the map starts only when it is in */
	var booted = false;
	try { mapboxgl.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.3/mapbox-gl-rtl-text.js", function () { boot(); }, false); } catch (e) { boot(); }
	setTimeout(boot, 5000);
	function boot() {
	if (booted) { return; }
	booted = true;
	var WIDE = innerWidth >= 900, PAD = WIDE ? { top: 110, bottom: 190, left: 40, right: 40 } : { top: 124, bottom: 236, left: 24, right: 24 };
	var v0 = VIEW[S.view] || null, p0 = v0 ? null : byId(S.view);
	var start = v0 || (p0 ? { center: p0.ll, zoom: 16.4, pitch: 62, bearing: -24 } : VIEW.world);
	var map = new mapboxgl.Map({ container: "pf-map", style: "mapbox://styles/mapbox/standard", projection: "globe", center: start.center, zoom: start.zoom, pitch: start.pitch, bearing: start.bearing, attributionControl: true, antialias: true, language: "he", config: { basemap: Object.assign({ lightPreset: q.get("light") || "day", showPointOfInterestLabels: false, showTransitLabels: false, showRoadLabels: false }, q.get("theme") ? { theme: q.get("theme") } : {}) } });
	map.setPadding(PAD);
	window.__map = map;
	map.on("style.load", function () {
		try { map.setFog({ color: "#dfeaf1", "high-color": "#4f8fb3", "horizon-blend": 0.06, "space-color": "#0d2129", "star-intensity": 0.12 }); } catch (e) {}
		[["colorWater", "#1c5a78"], ["colorGreenspace", "#c9ddd0"], ["colorAdminBoundaries", "#7f97a6"], ["colorLand", "#eef2f5"]].forEach(function (c) { if (q.get("plain") === "1") { return; } try { map.setConfigProperty("basemap", c[0], c[1]); } catch (e) {} });
		tower();
	});

	/* marks: properties that sit close on the screen join into one mark with their count and their worst state;
	   it is recomputed when the camera rests, and every mark follows the map while it moves */
	var layer = document.createElement("div"); layer.className = "pf-marks"; $("#pf").insertBefore(layer, $(".pf-top"));
	var marks = [];
	function visible(ll) {
		var c = map.getCenter(), r = Math.PI / 180, d = Math.acos(Math.min(1, Math.sin(c.lat * r) * Math.sin(ll[1] * r) + Math.cos(c.lat * r) * Math.cos(ll[1] * r) * Math.cos((ll[0] - c.lng) * r))) / r;
		if (map.getZoom() > 4.5) { var b = map.getBounds(); return d < 12 && ll[0] > b.getWest() - 0.2 && ll[0] < b.getEast() + 0.2 && ll[1] > b.getSouth() - 0.2 && ll[1] < b.getNorth() + 0.2; }
		return d < 78;
	}
	function cluster() {
		var pts = P.filter(shown).filter(function (p) { return visible(p.ll); }).map(function (p) { var xy = map.project(p.ll); return { p: p, x: xy.x, y: xy.y }; });
		var R = 62, groups = [];
		pts.forEach(function (a) {
			var g = groups.find(function (g) { return Math.hypot(g.x - a.x, g.y - a.y) < R; });
			if (g) { g.m.push(a.p); g.x = (g.x * (g.m.length - 1) + a.x) / g.m.length; g.y = (g.y * (g.m.length - 1) + a.y) / g.m.length; }
			else { groups.push({ m: [a.p], x: a.x, y: a.y }); }
		});
		layer.innerHTML = ""; marks = [];
		groups.forEach(function (g) {
			var el = document.createElement("button"), one = g.m.length === 1, p = g.m[0];
			var st = g.m.some(function (x) { return x.st === "care"; }) ? "care" : (g.m.some(function (x) { return x.st === "due"; }) ? "due" : "ok");
			var ll = [g.m.reduce(function (s, x) { return s + x.ll[0]; }, 0) / g.m.length, g.m.reduce(function (s, x) { return s + x.ll[1]; }, 0) / g.m.length];
			el.type = "button";
			if (one) {
				el.className = "pf-pin is-" + st + (S.sel === p.id ? " is-sel" : "");
				el.setAttribute("aria-label", p.name + ", " + p.city + ", " + ST[st]);
				el.innerHTML = '<span class="pf-ring" aria-hidden="true"></span><span class="pf-ring pf-ring--2" aria-hidden="true"></span>' + thumb(p) + badge(st);
				el.addEventListener("click", function (e) { e.stopPropagation(); pick(p.id); });
			} else {
				var cities = g.m.map(function (x) { return x.city; }).filter(function (c, i, a) { return a.indexOf(c) === i; }), regs = g.m.map(function (x) { return x.region; }).filter(function (c, i, a) { return a.indexOf(c) === i; });
				var label = cities.length === 1 ? cities[0] : (regs.length === 1 ? { il: "ישראל", med: "קפריסין ויוון", ny: "ניו יורק" }[regs[0]] : "ישראל והסביבה");
				var same = g.m.every(function (x) { return x.build && x.build === p.build; });
				if (same) { label = "כיכר המדינה"; }
				el.className = "pf-grp is-" + st;
				el.setAttribute("aria-label", label + ", " + g.m.length + " נכסים, " + ST[st]);
				el.innerHTML = '<span class="pf-ring" aria-hidden="true"></span><span class="pf-ring pf-ring--2" aria-hidden="true"></span><b>' + g.m.length + "</b><small>" + esc(label) + "</small>";
				el.addEventListener("click", function (e) {
					e.stopPropagation();
					if (same) { pick(g.m.find(function (x) { return x.st !== "ok"; }) ? g.m.find(function (x) { return x.st !== "ok"; }).id : p.id); return; }
					var bb = new mapboxgl.LngLatBounds(); g.m.forEach(function (x) { bb.extend(x.ll); });
					map.fitBounds(bb, { padding: { top: PAD.top + 40, bottom: PAD.bottom + 40, left: 70, right: 70 }, pitch: 45, bearing: -12, maxZoom: 15.2, duration: STILL ? 0 : 2400 });
				});
			}
			layer.appendChild(el);
			marks.push({ el: el, ll: ll });
		});
		place();
	}
	function place() {
		var up = map.getZoom() > 13 ? 1 : 0;
		marks.forEach(function (m) { var xy = map.project(m.ll); m.el.classList.toggle("is-up", !!up); m.el.style.transform = "translate(" + Math.round(xy.x) + "px," + Math.round(xy.y - up * 118) + "px) translate(-50%,-50%)"; });
	}
	map.on("move", place);

	function ring(ll, m, n) { var out = [], R = 6378137, i; for (i = 0; i <= n; i++) { var a = i / n * Math.PI * 2; out.push([ll[0] + (m * Math.cos(a)) / (R * Math.cos(ll[1] * Math.PI / 180)) * 180 / Math.PI, ll[1] + (m * Math.sin(a)) / R * 180 / Math.PI]); } return out; }
	function tower() {
		var fc = { type: "FeatureCollection", features: [] }, gl = { type: "FeatureCollection", features: [] };
		P.forEach(function (p) {
			var h = p.build === "kikar" ? 150 : (p.region === "ny" ? 120 : (p.id === "e1" ? 18 : 30)), col = p.st === "care" ? "#d5311f" : (p.st === "due" ? "#f2a900" : "#12996b");
			fc.features.push({ type: "Feature", properties: { id: p.id, h: h }, geometry: { type: "Polygon", coordinates: [ring(p.ll, p.build === "kikar" ? 17 : 12, 4).map(function (c, i, a) { return c; })] } });
			gl.features.push({ type: "Feature", properties: { id: p.id, col: col }, geometry: { type: "Polygon", coordinates: [ring(p.ll, 46, 48)] } });
		});
		try {
			if (map.getSource("pf-own")) { return; }
			map.addSource("pf-glow", { type: "geojson", data: gl }); map.addSource("pf-own", { type: "geojson", data: fc });
			map.addLayer({ id: "pf-glow", type: "fill", slot: "middle", source: "pf-glow", minzoom: 13, paint: { "fill-color": ["get", "col"], "fill-opacity": 0.28, "fill-emissive-strength": 1 } });
			map.addLayer({ id: "pf-glow-line", type: "line", slot: "middle", source: "pf-glow", minzoom: 13, paint: { "line-color": ["get", "col"], "line-width": 3, "line-emissive-strength": 1 } });
			map.addLayer({ id: "pf-own", type: "fill-extrusion", slot: "top", source: "pf-own", minzoom: 13, paint: { "fill-extrusion-color": "#ffffff", "fill-extrusion-height": ["get", "h"], "fill-extrusion-base": 0, "fill-extrusion-opacity": 1, "fill-extrusion-emissive-strength": 0.55 } });
		} catch (e) { console.warn("tower", e && e.message); }
	}
	function fly(v, ms) {
		if (STILL) { map.jumpTo(v); return; }
		map.flyTo(Object.assign({ duration: ms || 2600, essential: false, curve: 1.5 }, v));
	}
	function pick(id) {
		var p = byId(id); if (!p) { return; }
		S.sel = id;
		fly({ center: p.ll, zoom: 16.4, pitch: 62, bearing: -24, padding: PAD }, 3200);
		draw();
		var c = document.querySelector('.pf-card[data-id="' + id + '"]'); if (c && c.scrollIntoView) { c.scrollIntoView({ behavior: STILL ? "auto" : "smooth", inline: "center", block: "nearest" }); }
	}
	function level() { var z = map.getZoom(); return z < 4.2 ? "world" : (z < 9.5 ? "region" : "city"); }
	var drawing = false;
	function draw() {
		var lv = level(), n = { all: P.length, care: 0, due: 0, ok: 0 };
		P.forEach(function (p) { n[p.st]++; });
		$("#pf").className = "pf pf-lv-" + lv + (S.sel ? " has-sel" : "");
		$(".pf-chips").innerHTML = [["all", "הכול"], ["care", CH.care], ["due", CH.due], ["ok", CH.ok]].map(function (c) {
			return '<button type="button" class="pf-chip pf-chip--' + c[0] + (S.filter === c[0] ? " is-on" : "") + '" data-f="' + c[0] + '" aria-pressed="' + (S.filter === c[0]) + '">' + (c[0] !== "all" ? '<i aria-hidden="true"></i>' : "") + esc(c[1]) + ' <b>' + n[c[0]] + "</b></button>";
		}).join("");
		cluster();
		var sel = S.sel && byId(S.sel), care1 = P.find(function (p) { return p.st === "care"; }), say;
		if (sel) {
			say = '<div class="pf-say-t"><b>' + esc(sel.name) + "</b><span>" + esc(sel.city) + " · " + esc(sel.line) + '</span></div><button type="button" class="pf-go" data-open="' + sel.id + '">' + (sel.st === "care" ? "לטפל עכשיו" : "להיכנס לבניין") + "</button>";
		} else if (care1 && (S.filter === "all" || S.filter === "care")) {
			say = '<div class="pf-say-t"><b>נכס אחד צריך טיפול</b><span>' + esc(care1.city) + " · " + esc(care1.line) + '</span></div><button type="button" class="pf-go" data-pick="' + care1.id + '">לראות</button>';
		} else { say = '<div class="pf-say-t"><b>' + P.filter(shown).length + ' נכסים</b><span>לחצו על נכס כדי לטוס אליו.</span></div>'; }
		$(".pf-say").innerHTML = say;
		$(".pf-cards").innerHTML = P.filter(shown).sort(function (a, b) { var o = { care: 0, due: 1, ok: 2 }; return (a.id === S.sel ? -1 : 0) - (b.id === S.sel ? -1 : 0) || o[a.st] - o[b.st]; }).map(function (p) {
			return '<button type="button" class="pf-card is-' + p.st + (S.sel === p.id ? " is-sel" : "") + '" data-id="' + p.id + '">' + thumb(p) + badge(p.st) + '<span class="pf-card-t"><b>' + esc(p.name) + "</b><small>" + esc(p.city) + '</small><em class="pf-mono">' + esc(p.rent) + "</em></span></button>";
		}).join("");
	}
	document.addEventListener("click", function (e) {
		var c = e.target.closest("[data-f]"); if (c) { S.filter = c.getAttribute("data-f"); if (S.sel && !shown(byId(S.sel))) { S.sel = null; } draw(); return; }
		var k = e.target.closest(".pf-card[data-id], [data-pick]"); if (k) { pick(k.getAttribute("data-id") || k.getAttribute("data-pick")); return; }
	});
	map.on("zoomend", draw); map.on("moveend", draw);
	map.on("click", function () { if (S.sel) { S.sel = null; draw(); } });
	if (p0) { S.sel = p0.id; }
	draw();
	map.once("idle", function () { document.documentElement.setAttribute("data-ready", "1"); });
	}
})();
