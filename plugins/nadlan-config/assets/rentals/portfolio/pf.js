/* ============================================================================
   The opening of /my-rentals/: the example landlord's portfolio on a 3D map (HAD-795, board 5, 20.11.2026).
   The data and every word come from the server (inc/rentals/portfolio.php, data-pf); EVERYTHING is an example
   and the frame and each item say so. No example person has a phone or an e-mail.
   - the tray of pictures and the building panel work at once, with or without the map;
   - the map (Mapbox GL, globe, the Standard style with our own colours) arrives after first paint: marks follow it,
     far marks join into one with their count and worst state, a press flies to the building, which stands there in 3D
     with its floors, the example apartment's floor lit in the colour of its state;
   - the building comes forward in a panel: the Kikar HaMedina tower is the existing HAD-712 render and turns under the
     finger (24 frames, loaded read-only); the others show their picture; the apartment's card opens under it.
   No wheel or touch capture: cooperative gestures, so one finger scrolls the page and the wheel scrolls the page.
============================================================================ */
(function () {
	"use strict";
	var root = document.getElementById("nlpf");
	if (!root || root.dataset.wired) { return; }
	root.dataset.wired = "1";
	var D;
	try { D = JSON.parse(root.dataset.pf || "{}"); } catch (e0) { D = {}; }
	var P = D.props || [], W = D.w || {};
	if (!P.length) { return; }
	var LANG = root.dataset.lang || "he", BASE = root.dataset.base || "", TURN = root.dataset.turn || "", GO = root.dataset.go || "#", TOKEN = root.dataset.token || "", SAMPLE = root.dataset.sample || "";
	var QL = root.dataset.lab ? new URLSearchParams(location.search) : null;
	var RTL = LANG === "he", GL = "https://api.mapbox.com/mapbox-gl-js/v" + ((QL && QL.get("gl")) || "3.14.0") + "/";
	var RM = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
	var S = { filter: "all", sel: null, open: null, busyUntil: 0, orbiting: false, tracked: false };
	var map = null, marks = [], PAD = null;
	var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
	var $ = function (s) { return root.querySelector(s); };
	var byId = function (id) { return P.filter(function (p) { return p.id === id; })[0] || null; };
	var shown = function (p) { return S.filter === "all" || p.st === S.filter; };
	var wide = function () { return root.clientWidth >= 880; };
	var t = function (k, n) { return String(W[k] == null ? k : W[k]).replace("{n}", n); };
	var COL = { care: "#d5311f", due: "#f2a900", ok: "#12996b" };
	/* how close the camera stands: a low building needs a closer look than a tower */
	var near = function (p) { return p.b === "kikar" ? 16.1 : (p.floors > 8 ? 16.9 : 17.5); };
	var thumb = function (p) { return '<span class="nlpf-th"><img src="' + esc(BASE + "img/" + p.pic + "-192.webp") + '" alt="" width="96" height="96" decoding="async"></span>'; };
	var badge = function (st) { return '<i class="nlpf-bd nlpf-bd--' + st + '" aria-hidden="true">' + (st === "care" ? "!" : "") + "</i>"; };
	var track = function (name, data) { try { if (window.nlTrack) { window.nlTrack(name, data || {}); } } catch (e1) { /* the tracker never breaks the page */ } };

	/* ---------- the frame: filter, sentence, tray ---------- */
	var layer = $(".nlpf-marks"), chips = $(".nlpf-chips"), say = $(".nlpf-say"), cards = $(".nlpf-cards"), panel = $(".nlpf-panel");
	var world = document.createElement("button");
	world.type = "button"; world.className = "nlpf-world"; world.setAttribute("data-world", "1"); world.hidden = true;
	world.innerHTML = '<i aria-hidden="true"></i>' + esc(t("world"));
	$(".nlpf-h").appendChild(world);

	function draw() {
		var n = { all: P.length, care: 0, due: 0, ok: 0 };
		P.forEach(function (p) { n[p.st]++; });
		chips.innerHTML = [["all", t("all")], ["care", t("c_care")], ["due", t("c_due")], ["ok", t("c_ok")]].map(function (c) {
			return '<button type="button" class="nlpf-chip nlpf-chip--' + c[0] + (S.filter === c[0] ? " is-on" : "") + '" data-f="' + c[0] + '" aria-pressed="' + (S.filter === c[0]) + '">' + (c[0] !== "all" ? '<i aria-hidden="true"></i>' : "") + esc(c[1]) + " <b>" + n[c[0]] + "</b></button>";
		}).join("");
		var sel = S.sel && byId(S.sel), care1 = P.filter(function (p) { return p.st === "care"; })[0], h;
		if (sel) {
			h = '<div class="nlpf-say-t"><b>' + esc(sel.name) + "</b><span>" + esc(sel.city + " · " + sel.line) + '</span></div><button type="button" class="nlpf-go" data-open="' + sel.id + '">' + esc(sel.st === "care" ? t("fix") : t("enter_b")) + "</button>";
		} else if (care1 && (S.filter === "all" || S.filter === "care")) {
			h = '<div class="nlpf-say-t"><b>' + esc(t("one_care")) + "</b><span>" + esc(care1.city + " · " + care1.line) + '</span></div><button type="button" class="nlpf-go" data-pick="' + care1.id + '">' + esc(t("see")) + "</button>";
		} else {
			h = '<div class="nlpf-say-t"><b>' + esc(t("n_props", P.filter(shown).length)) + "</b><span>" + esc(t("hint")) + "</span></div>";
		}
		say.innerHTML = h;
		var ord = { care: 0, due: 1, ok: 2 };
		cards.innerHTML = P.filter(shown).slice().sort(function (a, b) { return (a.id === S.sel ? -1 : 0) - (b.id === S.sel ? -1 : 0) || ord[a.st] - ord[b.st]; }).map(function (p) {
			return '<button type="button" class="nlpf-card is-' + p.st + (S.sel === p.id ? " is-sel" : "") + '" data-id="' + p.id + '" aria-label="' + esc(p.name + ", " + p.city + ", " + t(p.st)) + '">' + thumb(p) + badge(p.st) + '<span class="nlpf-card-t"><b>' + esc(p.name) + "</b><small>" + esc(p.city + " · " + t(p.st)) + '</small><em class="nlpf-mono">' + esc(p.rent) + "</em></span></button>";
		}).join("");
		world.hidden = !(map && (S.sel || map.getZoom() > 3.2));
		cluster();
	}

	/* ---------- marks on the map ---------- */
	function visible(ll) {
		var c = map.getCenter(), r = Math.PI / 180, d = Math.acos(Math.min(1, Math.sin(c.lat * r) * Math.sin(ll[1] * r) + Math.cos(c.lat * r) * Math.cos(ll[1] * r) * Math.cos((ll[0] - c.lng) * r))) / r;
		if (map.getZoom() > 4.5) { var b = map.getBounds(); return d < 12 && ll[0] > b.getWest() - 0.2 && ll[0] < b.getEast() + 0.2 && ll[1] > b.getSouth() - 0.2 && ll[1] < b.getNorth() + 0.2; }
		return d < 78;
	}
	function cluster() {
		if (!map) { return; }
		var pts = P.filter(shown).filter(function (p) { return visible(p.ll); }).map(function (p) { var xy = map.project(p.ll); return { p: p, x: xy.x, y: xy.y }; });
		var R = 62, groups = [];
		pts.forEach(function (a) {
			var g = groups.filter(function (g1) { return Math.hypot(g1.x - a.x, g1.y - a.y) < R; })[0];
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
				el.className = "nlpf-pin is-" + st + (S.sel === p.id ? " is-sel" : "");
				el.setAttribute("aria-label", p.name + ", " + p.city + ", " + t(st));
				el.setAttribute("data-id", p.id);
				el.innerHTML = '<span class="nlpf-ring" aria-hidden="true"></span><span class="nlpf-ring nlpf-ring--2" aria-hidden="true"></span>' + thumb(p) + badge(st) + '<em class="nlpf-nm">' + esc(map.getZoom() > 9 ? p.bname : p.city) + "</em>";
			} else {
				var uniq = function (k) { return g.m.map(function (x) { return x[k]; }).filter(function (c, i, a) { return a.indexOf(c) === i; }); };
				var cities = uniq("city"), regs = uniq("region"), same = uniq("b").length === 1;
				var label = same ? p.bname : (cities.length === 1 ? cities[0] : (regs.length === 1 ? (W.places || {})[regs[0]] : (W.places || {}).near));
				el.className = "nlpf-grp is-" + st;
				el.setAttribute("aria-label", label + ", " + t("n_props", g.m.length) + ", " + t(st));
				el.setAttribute("data-grp", g.m.map(function (x) { return x.id; }).join(","));
				el.innerHTML = '<span class="nlpf-ring" aria-hidden="true"></span><span class="nlpf-ring nlpf-ring--2" aria-hidden="true"></span><b>' + g.m.length + "</b><small>" + esc(label) + "</small>";
			}
			layer.appendChild(el);
			marks.push({ el: el, ll: ll });
		});
		place();
	}
	function place() {
		if (!map) { return; }
		var up = map.getZoom() > 13 ? 1 : 0;
		marks.forEach(function (m) { var xy = map.project(m.ll); m.el.classList.toggle("is-up", !!up); m.el.style.transform = "translate(" + Math.round(xy.x) + "px," + Math.round(xy.y - up * 118) + "px) translate(-50%,-50%)"; });
	}

	/* ---------- moving ---------- */
	/* phones: the site keeps floating buttons over the bottom of every page (a WhatsApp bar, the basket, accessibility).
	   The stage takes the height that is free above them, so that no part of it has to live under them; they are found
	   by asking the browser what is drawn over the bottom band of the screen. Nothing of theirs is touched. */
	var strip = 0, fitW = 0, fitH = 0;
	function fixedAt(x, y) {
		var el = document.elementFromPoint(x, y), cs;
		if (!el || root.contains(el)) { return false; }
		for (; el && el !== document.body && el !== document.documentElement; el = el.parentElement) { cs = window.getComputedStyle(el).position; if (cs === "fixed" || cs === "sticky") { return true; } }
		return false;
	}
	function fitPhone(force) {
		var W0 = window.innerWidth, H0 = window.innerHeight, x, y, s = 0;
		if (W0 > 700) { root.classList.remove("is-tight"); if (root.style.height) { root.style.height = ""; if (map) { map.resize(); } } return; }
		if (!force && W0 === fitW && Math.abs(H0 - fitH) < 120) { return; }
		fitW = W0; fitH = H0;
		for (x = 10; x < W0; x += 14) { for (y = H0 - 3; y > H0 - 230 && y > H0 / 2; y -= 6) { if (fixedAt(x, y)) { s = Math.max(s, H0 - y + 6); } } }
		strip = s;
		var h = Math.max(440, Math.min(660, H0 - 72, H0 - strip - 6));
		root.classList.toggle("is-tight", h < 520);
		if (Math.abs(root.offsetHeight - h) > 2) { root.style.height = h + "px"; if (map) { map.resize(); map.setPadding(pad()); } if (S.open) { layoutTurn(); } }
	}
	function pad() {
		var w = wide(), p = w ? { top: 104, bottom: 196, left: 40, right: 40 } : { top: 176, bottom: 140, left: 20, right: 20 };
		if (w && S.open) { p.bottom = 40; if (RTL) { p.right = 440; } else { p.left = 440; } }
		return p;
	}
	function worldView() { return { center: [-19.5, 30], zoom: wide() ? 1.45 : 0.8, pitch: 0, bearing: 0 }; }
	function fly(v, ms) {
		if (!map) { return; }
		v.padding = pad();
		S.busyUntil = Date.now() + (RM ? 0 : (ms || 2600)) + 900;
		if (RM) { map.jumpTo(v); return; }
		map.flyTo(Object.assign({ duration: ms || 2600, essential: true, curve: 1.5 }, v));
	}
	function pick(id, how) {
		var p = byId(id); if (!p) { return; }
		if (!map) { openPanel(id); return; }
		if (S.sel === id && how !== "say") { openPanel(id); return; }
		S.sel = id;
		fly({ center: p.ll, zoom: near(p), pitch: 62, bearing: -24 }, 3000);
		draw();
		var c = cards.querySelector('.nlpf-card[data-id="' + id + '"]');
		if (c) { cards.scrollTo({ left: c.offsetLeft - (cards.clientWidth - c.offsetWidth) / 2, behavior: RM ? "auto" : "smooth" }); }
		if (!S.tracked) { S.tracked = true; track("rent_example_open", { property: id, how: how || "press" }); }
	}

	/* ---------- the building comes forward ---------- */
	function floorTop(p) { return (1000 - (p.floor - 0.5) * 23.1) / 1080 * 100; }
	function sheetHtml(p) {
		return '<div class="nlpf-sheet"><div class="nlpf-s-h"><b>' + esc(p.short) + '</b><span class="nlpf-st is-' + p.st + '">' + esc(t(p.st)) + "</span></div>" +
			'<div class="nlpf-s-sub">' + esc(t("floor") + " " + p.floor + " " + t("of") + " " + p.floors + " · " + p.rooms + " " + t("rooms") + " · " + p.sqm + " " + t("sqm")) + "</div>" +
			'<div class="nlpf-s-line is-' + p.st + '"><i aria-hidden="true"></i>' + esc(p.line) + "</div>" +
			'<div class="nlpf-facts"><div class="nlpf-fact"><small>' + esc(p.tenant ? t("rent") : t("ask")) + '</small><b class="nlpf-mono">' + esc(p.rent) + '</b></div><div class="nlpf-fact"><small>' + esc(t("tenant")) + "</small><b>" + esc(p.tenant || t("vacant")) + "</b></div></div>" +
			'<div class="nlpf-s-l">' + esc(t("home")) + '</div><div class="nlpf-parts">' + (p.parts || []).map(function (a) {
				return '<span class="nlpf-part is-' + a[2] + '" role="img" aria-label="' + esc(a[1] + ", " + (a[2] === "care" ? t("p_care") : t("p_ok"))) + '"><img src="' + esc(BASE + "img/p-" + a[0] + "-192.webp") + '" alt="" width="64" height="64" loading="lazy" decoding="async"><i aria-hidden="true">' + (a[2] === "care" ? "!" : "") + "</i><em>" + esc(a[1]) + "</em></span>";
			}).join("") + "</div>" +
			'<div class="nlpf-s-cta">' + (SAMPLE ? '<a class="nlpf-btn nlpf-btn--go" href="' + esc(SAMPLE + (SAMPLE.indexOf("?") < 0 ? "?" : "&") + "u=" + p.unit + "#/today/" + p.unit) + '" data-enter="' + p.unit + '">' + esc(t("enter")) + "</a>" : "") + '<a class="nlpf-btn ' + (SAMPLE ? "nlpf-btn--line" : "nlpf-btn--go") + '" href="' + esc(GO) + '" data-cta="1">' + esc(t("cta")) + "</a></div></div>";
	}
	function panelHtml(id) {
		var p = byId(id), sibs = P.filter(function (x) { return x.b === p.b; }), kikar = p.b === "kikar", h = "";
		h += '<div class="nlpf-p-head"><button type="button" class="nlpf-back" data-back="1" aria-label="' + esc(t("back_map")) + '"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 4l6 6-6 6"/></svg></button>' +
			'<div class="nlpf-p-t"><b>' + esc(p.bname) + "</b><small>" + esc(p.city + " · " + (sibs.length > 1 ? t("apts", sibs.length) : t("apt1"))) + '</small></div><span class="nlpf-ex">' + esc(t("ex1")) + "</span></div>";
		if (kikar) {
			h += '<div class="nlpf-vis nlpf-vis--turn"><div class="nlpf-turn" data-turn="1"><img src="' + esc(TURN + "A-00.webp") + '" alt="" draggable="false">' +
				sibs.map(function (x) { return '<i class="nlpf-fl is-' + x.st + (x.id === id ? " is-on" : "") + '" data-fl="' + x.id + '" style="top:' + floorTop(x).toFixed(1) + '%"></i>'; }).join("") + "</div>" +
				sibs.map(function (x, i) { return '<button type="button" class="nlpf-tag nlpf-tag--' + (i % 2 ? "b" : "a") + " is-" + x.st + (x.id === id ? " is-on" : "") + '" data-apt="' + x.id + '" aria-pressed="' + (x.id === id) + '" aria-label="' + esc(x.short + ", " + t("floor") + " " + x.floor + ", " + t(x.st)) + '"><i aria-hidden="true"></i>' + esc(x.tag || x.short) + "<small>" + esc(t("floor") + " " + x.floor) + "</small></button>"; }).join("") +
				'<span class="nlpf-hint">' + esc(t("turn")) + '</span><span class="nlpf-note">' + esc(t("note")) + "</span></div>";
		} else {
			h += '<div class="nlpf-vis"><img class="nlpf-pic" src="' + esc(BASE + "img/" + p.pic + "-720.webp") + '" alt="" decoding="async">' +
				sibs.map(function (x) { return '<button type="button" class="nlpf-tag is-' + x.st + (x.id === id ? " is-on" : "") + '" data-apt="' + x.id + '" style="top:' + Math.round(74 - (x.floor / x.floors) * 46) + '%;left:10px" aria-pressed="' + (x.id === id) + '"><i aria-hidden="true"></i>' + esc(x.short) + "<small>" + esc(t("floor") + " " + x.floor) + "</small></button>"; }).join("") +
				'<span class="nlpf-note">' + esc(t("note")) + "</span></div>";
		}
		return h + sheetHtml(p);
	}
	/* the tower stands large in its window, cut above and below, with the open apartment's floor in the middle;
	   a press on the other apartment slides the tower to its floor */
	function layoutTurn() {
		var vis = panel.querySelector(".nlpf-vis--turn"), p = S.open && byId(S.open);
		if (!vis || !p) { return; }
		var tr = vis.querySelector(".nlpf-turn"), vw = vis.clientWidth, vh = vis.clientHeight;
		root.classList.toggle("is-low", vh < 190);
		var tw = Math.min(vw * 0.7, 320), th = tw * 1080 / 756;
		if (th < vh) { th = vh; tw = th * 756 / 1080; }
		var top = Math.max(vh - th, Math.min(0, vh / 2 - floorTop(p) / 100 * th));
		tr.style.width = Math.round(tw) + "px"; tr.style.height = Math.round(th) + "px"; tr.style.top = Math.round(top) + "px";
		[].forEach.call(vis.querySelectorAll(".nlpf-tag"), function (el) {
			var x = byId(el.getAttribute("data-apt")), y = top + (floorTop(x) + 1) / 100 * th;
			el.style.top = Math.round(Math.max(26, Math.min(vh - (vh < 190 ? 50 : 76), y))) + "px";
			el.style.maxWidth = Math.max(96, Math.round(vw / 2 - tw * 0.15 - 14)) + "px";
		});
	}
	var turnStop = null;
	function turntable(el) {
		var img = el.querySelector("img"), N = 24, i = 0, fr = [], loaded = 0, x0 = null, i0 = 0, auto = 0, dead = false;
		var set = function (k) { k = ((k % N) + N) % N; if (fr[k] && fr[k].complete && fr[k].naturalWidth) { i = k; img.src = fr[k].src; } };
		var k;
		for (k = 0; k < N; k++) {
			fr[k] = new Image(); fr[k].decoding = "async";
			fr[k].onload = function () { loaded++; if (loaded === N && !RM && !dead && x0 === null) { spin(); } };
			fr[k].src = TURN + "A-" + (k < 10 ? "0" : "") + k + ".webp";
		}
		function spin() {
			var t0 = performance.now(), D1 = 3600;
			var step = function (now) {
				if (dead || x0 !== null) { return; }
				var q = Math.min(1, (now - t0) / D1), e = q < 0.5 ? 2 * q * q : 1 - Math.pow(-2 * q + 2, 2) / 2;
				set(Math.round(e * N));
				if (q < 1) { auto = requestAnimationFrame(step); }
			};
			auto = requestAnimationFrame(step);
		}
		el.addEventListener("pointerdown", function (e) { x0 = e.clientX; i0 = i; cancelAnimationFrame(auto); el.classList.add("is-drag"); try { el.setPointerCapture(e.pointerId); } catch (e2) { /* older browsers */ } });
		el.addEventListener("pointermove", function (e) { if (x0 === null) { return; } set(i0 + Math.round((e.clientX - x0) / 9) * (RTL ? 1 : 1)); });
		var up = function () { x0 = null; el.classList.remove("is-drag"); };
		el.addEventListener("pointerup", up); el.addEventListener("pointercancel", up);
		turnStop = function () { dead = true; cancelAnimationFrame(auto); };
	}
	var lastFocus = null;
	function openPanel(id) {
		var p = byId(id); if (!p) { return; }
		if (!S.open) { lastFocus = document.activeElement; }
		var was = S.open && byId(S.open), slide = !!(was && was.b === p.b && was.id !== id && panel.querySelector(".nlpf-vis--turn"));
		if (!slide && turnStop) { turnStop(); turnStop = null; }
		S.sel = id; S.open = id;
		if (slide) {
			/* the same tower, the other apartment: the render stays and slides, only the card changes */
			var old = panel.querySelector(".nlpf-sheet"), box = document.createElement("div");
			box.innerHTML = sheetHtml(p); old.parentNode.replaceChild(box.firstChild, old);
			[].forEach.call(panel.querySelectorAll(".nlpf-tag"), function (el) { var on = el.getAttribute("data-apt") === id; el.classList.toggle("is-on", on); el.setAttribute("aria-pressed", String(on)); });
			[].forEach.call(panel.querySelectorAll(".nlpf-fl"), function (el) { el.classList.toggle("is-on", el.getAttribute("data-fl") === id); });
			layoutTurn();
			if (map) { fly({ center: p.ll, zoom: near(p), pitch: 62, bearing: map.getBearing() }, 900); }
			draw();
			return;
		}
		panel.innerHTML = panelHtml(id);
		panel.hidden = false;
		panel.style.animation = "none"; void panel.offsetWidth; panel.style.animation = "";
		root.classList.add("has-panel");
		var tt = panel.querySelector("[data-turn]"); if (tt) { layoutTurn(); turntable(tt); }
		/* a phone: the building opens with the stage at the top of the screen, clear of the site's floating buttons */
		if (window.innerWidth <= 700) {
			fitPhone(true);
			var rb = root.getBoundingClientRect();
			if (rb.top < -2 || rb.top > 6) { window.scrollBy({ top: rb.top - 2, behavior: RM ? "auto" : "smooth" }); }
		}
		if (map) { fly({ center: p.ll, zoom: near(p), pitch: 62, bearing: map.getBearing() }, 1400); }
		draw();
		var b = panel.querySelector(".nlpf-back"); if (b && b.focus) { try { b.focus({ preventScroll: true }); } catch (e3) { b.focus(); } }
		track("rent_example_open", { property: id, how: "building" });
	}
	function closePanel() {
		if (!S.open) { return; }
		if (turnStop) { turnStop(); turnStop = null; }
		if (!map) { S.sel = null; }
		S.open = null; panel.hidden = true; panel.innerHTML = ""; root.classList.remove("has-panel");
		if (map && S.sel) { var p = byId(S.sel); fly({ center: p.ll, zoom: near(p), pitch: 62, bearing: map.getBearing() }, 900); }
		draw();
		if (lastFocus && lastFocus.focus && document.contains(lastFocus)) { try { lastFocus.focus({ preventScroll: true }); } catch (e4) { /* nothing */ } }
	}

	/* ---------- presses ---------- */
	root.addEventListener("click", function (e) {
		var x = e.target.closest ? e.target : e.target.parentElement, el;
		if (!x || !x.closest) { return; }
		if ((el = x.closest("[data-f]"))) { S.filter = el.getAttribute("data-f"); if (S.sel && !shown(byId(S.sel))) { S.sel = null; } draw(); return; }
		if ((el = x.closest("[data-back]"))) { closePanel(); return; }
		if ((el = x.closest("[data-apt]"))) { if (el.getAttribute("data-apt") !== S.open) { openPanel(el.getAttribute("data-apt")); } return; }
		if ((el = x.closest("[data-enter]"))) { track("rent_example_open", { property: S.open || "", how: "enter" }); return; }
		if ((el = x.closest("[data-open]"))) { openPanel(el.getAttribute("data-open")); return; }
		if ((el = x.closest("[data-pick]"))) { pick(el.getAttribute("data-pick"), "say"); return; }
		if ((el = x.closest("[data-world]"))) { S.sel = null; if (S.open) { closePanel(); } fly(worldView(), 2600); draw(); return; }
		if ((el = x.closest(".nlpf-card[data-id], .nlpf-pin[data-id]"))) { pick(el.getAttribute("data-id"), el.classList.contains("nlpf-pin") ? "mark" : "card"); return; }
		if ((el = x.closest("[data-grp]"))) {
			var ids = el.getAttribute("data-grp").split(","), g = ids.map(byId), same = g.every(function (q) { return q.b === g[0].b; });
			if (same) { var need = g.filter(function (q) { return q.st !== "ok"; })[0] || g[0]; pick(need.id, "mark"); return; }
			var bb = new window.mapboxgl.LngLatBounds(); g.forEach(function (q) { bb.extend(q.ll); });
			var pd = pad(); S.busyUntil = Date.now() + 3200;
			map.fitBounds(bb, { padding: { top: pd.top + 40, bottom: pd.bottom + 40, left: pd.left + 50, right: pd.right + 50 }, pitch: 45, bearing: -12, maxZoom: 15.2, duration: RM ? 0 : 2400, essential: true });
		}
	});
	document.addEventListener("keydown", function (e) { if (e.key === "Escape" && S.open) { closePanel(); } });
	window.addEventListener("resize", function () { fitPhone(false); if (S.open) { layoutTurn(); } });

	/* ---------- the map ---------- */
	function ring(ll, m, n, rot) {
		var out = [], R = 6378137, i, a;
		for (i = 0; i <= n; i++) { a = i / n * Math.PI * 2 + (rot || 0); out.push([ll[0] + (m * Math.cos(a)) / (R * Math.cos(ll[1] * Math.PI / 180)) * 180 / Math.PI, ll[1] + (m * Math.sin(a)) / R * 180 / Math.PI]); }
		return out;
	}
	function arc(a, b, n) {
		var r = Math.PI / 180, la1 = a[1] * r, lo1 = a[0] * r, la2 = b[1] * r, lo2 = b[0] * r, out = [], i;
		var d = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin((la2 - la1) / 2), 2) + Math.cos(la1) * Math.cos(la2) * Math.pow(Math.sin((lo2 - lo1) / 2), 2)));
		if (!d) { return [a, b]; }
		for (i = 0; i <= n; i++) {
			var f = i / n, A = Math.sin((1 - f) * d) / Math.sin(d), B = Math.sin(f * d) / Math.sin(d);
			var x = A * Math.cos(la1) * Math.cos(lo1) + B * Math.cos(la2) * Math.cos(lo2), y = A * Math.cos(la1) * Math.sin(lo1) + B * Math.cos(la2) * Math.sin(lo2), z = A * Math.sin(la1) + B * Math.sin(la2);
			out.push([Math.atan2(y, x) / r, Math.atan2(z, Math.sqrt(x * x + y * y)) / r]);
		}
		return out;
	}
	function layers() {
		if (map.getSource("nlpf-floors")) { return; }
		var floors = { type: "FeatureCollection", features: [] }, glow = { type: "FeatureCollection", features: [] }, arcs = { type: "FeatureCollection", features: [] }, seen = {}, FH = 3.3;
		P.forEach(function (p) {
			if (seen[p.b]) { return; }
			seen[p.b] = 1;
			var sibs = P.filter(function (x) { return x.b === p.b; }), c = [sibs.reduce(function (s, x) { return s + x.ll[0]; }, 0) / sibs.length, sibs.reduce(function (s, x) { return s + x.ll[1]; }, 0) / sibs.length];
			var rad = p.b === "kikar" ? 19 : (p.floors > 8 ? 15 : 12), foot = [ring(c, rad, 4, Math.PI / 4)], f;
			var worst = sibs.some(function (x) { return x.st === "care"; }) ? "care" : (sibs.some(function (x) { return x.st === "due"; }) ? "due" : "ok");
			for (f = 1; f <= p.floors; f++) {
				var own = sibs.filter(function (x) { return x.floor === f; })[0];
				floors.features.push({ type: "Feature", properties: { b: p.b, first: sibs[0].id, own: own ? own.id : "", col: own ? COL[own.st] : "#ffffff", base: (f - 1) * FH, h: f * FH - (own ? 0.2 : 0.55) }, geometry: { type: "Polygon", coordinates: foot } });
			}
			glow.features.push({ type: "Feature", properties: { col: COL[worst] }, geometry: { type: "Polygon", coordinates: [ring(c, rad * 2.6, 48)] } });
		});
		var hub = byId("u21").ll;
		["u31", "u51", "u61", "u71", "u41"].forEach(function (id) { var q = byId(id); if (q) { arcs.features.push({ type: "Feature", properties: {}, geometry: { type: "LineString", coordinates: arc(hub, q.ll, 72) } }); } });
		try {
			map.addSource("nlpf-arcs", { type: "geojson", data: arcs }); map.addSource("nlpf-glow", { type: "geojson", data: glow }); map.addSource("nlpf-floors", { type: "geojson", data: floors });
			map.addLayer({ id: "nlpf-arcs", type: "line", slot: "top", source: "nlpf-arcs", maxzoom: 7, layout: { "line-cap": "round" }, paint: { "line-color": "#7fd3e6", "line-width": 1.8, "line-opacity": ["interpolate", ["linear"], ["zoom"], 0, 0.9, 4.5, 0.8, 6.5, 0], "line-dasharray": [1.2, 2.2], "line-emissive-strength": 1 } });
			map.addLayer({ id: "nlpf-glow", type: "fill", slot: "middle", source: "nlpf-glow", minzoom: 13, paint: { "fill-color": ["get", "col"], "fill-opacity": 0.26, "fill-emissive-strength": 1 } });
			map.addLayer({ id: "nlpf-glow-line", type: "line", slot: "middle", source: "nlpf-glow", minzoom: 13, paint: { "line-color": ["get", "col"], "line-width": 3, "line-emissive-strength": 1 } });
			map.addLayer({ id: "nlpf-floors", type: "fill-extrusion", slot: "top", source: "nlpf-floors", minzoom: 13, filter: ["==", ["get", "own"], ""], paint: { "fill-extrusion-color": "#ffffff", "fill-extrusion-height": ["get", "h"], "fill-extrusion-base": ["get", "base"], "fill-extrusion-opacity": 1, "fill-extrusion-emissive-strength": 0.5 } });
			map.addLayer({ id: "nlpf-own", type: "fill-extrusion", slot: "top", source: "nlpf-floors", minzoom: 13, filter: ["!=", ["get", "own"], ""], paint: { "fill-extrusion-color": ["get", "col"], "fill-extrusion-height": ["get", "h"], "fill-extrusion-base": ["get", "base"], "fill-extrusion-opacity": 1, "fill-extrusion-emissive-strength": 1 } });
		} catch (e5) { if (window.console) { console.warn("nlpf layers", e5 && e5.message); } }
	}
	function boot() {
		if (map || !window.mapboxgl) { return; }
		var mb = window.mapboxgl, v = worldView();
		try {
			if (mb.supported && !mb.supported()) { throw new Error("no webgl"); }
			mb.accessToken = TOKEN;
			map = new mb.Map({ container: "nlpf-map", style: "mapbox://styles/mapbox/standard", projection: "globe", center: v.center, zoom: v.zoom, pitch: 0, bearing: 0, attributionControl: true, antialias: true, language: LANG,
				cooperativeGestures: true, locale: { "TouchPanBlocker.Message": t("gesture"), "ScrollZoomBlocker.CtrlMessage": t("ctrl"), "ScrollZoomBlocker.CmdMessage": t("cmd") },
				config: { basemap: Object.assign({ lightPreset: (QL && QL.get("light")) || "day", showPointOfInterestLabels: false, showTransitLabels: false, showRoadLabels: false }, QL && QL.get("theme") ? { theme: QL.get("theme") } : {}) } });
		} catch (e6) { map = null; root.classList.add("no-map"); return; }
		map.setPadding(pad());
		map.on("style.load", function () {
			try { map.setFog({ color: "#dfeaf1", "high-color": "#4f8fb3", "horizon-blend": 0.06, "space-color": "#0d2129", "star-intensity": 0.14 }); } catch (e7) { /* older style */ }
			[["colorWater", "#1c5a78"], ["colorGreenspace", "#c9ddd0"], ["colorAdminBoundaries", "#7f97a6"], ["colorLand", "#eef2f5"]].forEach(function (c) { try { map.setConfigProperty("basemap", c[0], c[1]); } catch (e8) { /* a property the style lacks */ } });
			layers();
		});
		map.on("load", function () { root.classList.add("is-map"); draw(); });
		map.on("error", function (e) { if (!root.classList.contains("is-map") && e && e.error && /401|403|token|access/i.test(String(e.error.message || ""))) { root.classList.add("no-map"); } });
		map.on("move", place);
		map.on("moveend", function () { if (!S.orbiting) { draw(); } });
		var quiet = function () { S.busyUntil = Date.now() + 6000; };
		["mousedown", "touchstart", "wheel", "dragstart"].forEach(function (ev) { map.on(ev, quiet); });
		map.on("click", "nlpf-own", function (e) { var f = e.features && e.features[0]; if (f) { e.originalEvent.nlpfHit = 1; openPanel(f.properties.own); } });
		map.on("click", "nlpf-floors", function (e) { var f = e.features && e.features[0]; if (f && !e.originalEvent.nlpfHit) { e.originalEvent.nlpfHit = 1; if (S.sel && byId(S.sel).b === f.properties.b) { openPanel(S.sel); } else { pick(f.properties.first, "building"); } } });
		["nlpf-own", "nlpf-floors"].forEach(function (id) {
			map.on("mouseenter", id, function () { map.getCanvas().style.cursor = "pointer"; });
			map.on("mouseleave", id, function () { map.getCanvas().style.cursor = ""; });
		});
		map.on("click", function (e) { window.setTimeout(function () { if (!e.originalEvent.nlpfHit && S.sel && !S.open) { S.sel = null; draw(); } }, 0); });
		window.addEventListener("resize", function () { if (map) { map.resize(); map.setPadding(pad()); } });
		/* a selected building turns slowly, so it reads as a solid thing; it stops for any touch and when the stage is off screen */
		var onScreen = true;
		if (window.IntersectionObserver) { new IntersectionObserver(function (en) { onScreen = en[0].isIntersecting; }, { threshold: 0.15 }).observe(root); }
		var loop = function () {
			if (map && S.sel && !RM && onScreen && !document.hidden && Date.now() > S.busyUntil && map.getZoom() > 15 && !map.isMoving()) {
				S.orbiting = true; map.setBearing(map.getBearing() + 0.05); S.orbiting = false;
			}
			window.requestAnimationFrame(loop);
		};
		window.requestAnimationFrame(loop);
		window.__nlpfMap = map;
	}
	function lib() {
		if (window.__nlMbx) { return window.__nlMbx; }
		window.__nlMbx = new Promise(function (res, rej) {
			if (window.mapboxgl) { res(); return; }
			var l = document.createElement("link"); l.rel = "stylesheet"; l.href = GL + "mapbox-gl.css"; document.head.appendChild(l);
			var s = document.createElement("script"); s.src = GL + "mapbox-gl.js"; s.async = true; s.onload = function () { res(); }; s.onerror = function () { rej(new Error("map library")); }; document.head.appendChild(s);
		});
		return window.__nlMbx;
	}
	function start() {
		if (!TOKEN) { root.classList.add("no-map"); return; }
		lib().then(function () {
			var mb = window.mapboxgl, done = false, go = function () { if (!done) { done = true; boot(); } };
			if (!RTL) { go(); return; }
			/* Hebrew labels need the right-to-left text plugin BEFORE the first tiles are laid out */
			try {
				if (mb.getRTLTextPluginStatus && mb.getRTLTextPluginStatus() !== "unavailable") { go(); return; }
				mb.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.3/mapbox-gl-rtl-text.js", function () { go(); }, false);
			} catch (e9) { go(); }
			window.setTimeout(go, 4000);
		}, function () { root.classList.add("no-map"); });
	}

	draw();
	fitPhone(true);
	[700, 2200, 5000].forEach(function (ms) { window.setTimeout(function () { fitPhone(true); }, ms); });
	if ("requestIdleCallback" in window) { window.requestIdleCallback(start, { timeout: 1200 }); } else { window.setTimeout(start, 200); }
})();
