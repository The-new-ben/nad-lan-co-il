/* ============================================================================
   NADLAN RENTALS MANAGER v2 - the digital lease file (2026-07-12).
   Research-driven upgrade: six health cards, a "my next action" feed sorted
   by legal risk, securities register with the statutory cap
   (min(3 months rent, term rent / 3)), CPI adjustment calculator, the 2026
   rent-tax estimator (exemption band + 10% route + the 2023 renter-lessor
   deduction), statutory repair deadlines (3 / 30 days), notice windows
   (90 / 60 days) - every number labeled as an estimate, sources on the
   server side (nadlan_rm_law()). Fully bilingual via data-i18n (HE/EN).
   Flow unchanged: portfolio map -> building 3D -> apartment panel.
============================================================================ */
(function () {
	"use strict";
	var root = document.getElementById("nlrm-mount");
	if (!root || root.dataset.wired) { return; }
	root.dataset.wired = "1";

	var MODE = root.dataset.mode || "live";
	var LANG = root.dataset.lang || "he";
	var QS = LANG !== "he" ? "?lang=" + LANG : "";
	var REST = root.dataset.rest;
	var NONCE = root.dataset.nonce || "";
	var GLB = root.dataset.glb || "";
	var TOKEN = root.dataset.mapbox || "";
	var T = {};
	try { T = JSON.parse(root.dataset.i18n || "{}"); } catch (e) { T = {}; }
	var PROPS = [], CUR = null, LAW = null, map = null;

	function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
	function t(k) { return T[k] != null ? T[k] : k; }
	function tpl(k, vars) {
		var s = t(k);
		Object.keys(vars || {}).forEach(function (v) { s = s.split("{" + v + "}").join(vars[v]); });
		return s;
	}
	function api(path, opts) {
		opts = opts || {};
		opts.headers = Object.assign({ "Content-Type": "application/json" }, NONCE ? { "X-WP-Nonce": NONCE } : {}, opts.headers || {});
		return fetch(REST + path, opts).then(function (r) { return r.json().then(function (j) { if (!r.ok) { throw j; } return j; }); });
	}
	function ym(off) {
		var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + off);
		return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0");
	}
	function daysTo(dateStr) {
		if (!dateStr) { return null; }
		return Math.round((new Date(dateStr + "T00:00:00") - new Date()) / 86400000);
	}
	function daysSince(dateStr) { var d = daysTo(dateStr); return d === null ? null : -d; }
	function nis(n) { return "₪" + (n || 0).toLocaleString(); }
	function termMonths(u) {
		if (!u.start || !u.end) { return 12; }
		var a = new Date(u.start), b = new Date(u.end);
		return Math.max(1, Math.round((b - a) / (30.44 * 86400000)));
	}
	function secCap(u) { return Math.round(Math.min(3 * (u.rent || 0), termMonths(u) * (u.rent || 0) / 3)); }
	function unitStatus(u) {
		if (!u.tenant_name) { return "vacant"; }
		var led = u.ledger || {};
		if (u.start && u.start <= ym(-1) + "-28" && led[ym(-1)] !== "paid") { return "late"; }
		if (led[ym(0)] !== "paid") { return "due"; }
		return "ok";
	}
	function docsMissing(u) {
		var keys = Object.keys(CUR ? CUR.doc_keys : {});
		return keys.filter(function (k) { return !(u.docs || {})[k]; }).length;
	}

	/* ---------- boot ---------- */
	function load() {
		var p = MODE === "demo" ? api("/rental-demo" + QS) : api("/rental-props" + QS);
		p.then(function (d) {
			PROPS = d.props || [];
			if (!PROPS.length) { root.innerHTML = '<p class="nlrm-note">' + esc(t("none_yet")) + "</p>"; root.removeAttribute("data-loading"); return; }
			CUR = PROPS[0]; LAW = CUR.law || {};
			render();
		}).catch(function () { root.innerHTML = '<p class="nlrm-note">' + esc(t("load_fail")) + "</p>"; });
	}

	/* ---------- render ---------- */
	function render() {
		var h = "";
		h += '<div class="nlrm-map" id="nlrm-map"></div>';
		h += '<div class="nlrm-props" id="nlrm-props">';
		PROPS.forEach(function (p, i) {
			h += '<button type="button" data-i="' + i + '" class="' + (p === CUR ? "is-on" : "") + '">' + esc(p.address + ", " + p.city) + " · " + (p.units || []).length + " " + esc(t("units")) + "</button>";
		});
		h += "</div>";
		h += '<div class="nlrm-health" id="nlrm-health"></div>';
		h += '<div class="nlrm-3d" id="nlrm-3d"></div>';
		h += '<div class="nlrm-legend">';
		Object.keys(CUR.statuses).forEach(function (k) { h += "<span><i style=\"background:" + CUR.statuses[k][1] + '"></i>' + esc(CUR.statuses[k][0]) + "</span>"; });
		h += "</div>";
		h += '<div class="nlrm-grid">';
		h += '<div class="nlrm-card" id="nlrm-unit"><h4>' + esc(t("sel_title")) + '</h4><p class="nlrm-note">' + esc(CUR.can_manage ? t("sel_hint_mgr") : t("sel_hint_ro")) + "</p></div>";
		h += '<div class="nlrm-card" id="nlrm-actions"></div>';
		h += '<div class="nlrm-card" id="nlrm-summary"></div>';
		h += '<div class="nlrm-card" id="nlrm-tax"></div>';
		h += "</div>";
		root.innerHTML = h;
		root.removeAttribute("data-loading");
		if (!document.getElementById("nlrm-v2css")) {
			var st = document.createElement("style");
			st.id = "nlrm-v2css";
			st.textContent = ".nlrm-health{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:12px 0 4px}@media(max-width:760px){.nlrm-health{grid-template-columns:repeat(3,1fr)}}" +
				".nlrm-hcard{border:1px solid #E2DCD0;border-radius:12px;padding:10px 8px;text-align:center;background:#fff}" +
				".nlrm-hcard b{display:block;font:700 12px Heebo;color:#51483A}" +
				".nlrm-hcard i{display:block;width:12px;height:12px;border-radius:50%;margin:6px auto 0;font-style:normal}" +
				".nlrm-acts li{font:400 13px/1.6 Heebo;padding:7px 0;border-bottom:1px solid #F3EEE3;list-style:none;display:flex;gap:8px;align-items:baseline}" +
				".nlrm-acts li i{flex:0 0 9px;width:9px;height:9px;border-radius:50%;font-style:normal;margin-top:4px}" +
				".nlrm-sec{background:#FAF7F1;border:1px solid #E2DCD0;border-radius:12px;padding:12px;margin:10px 0}" +
				".nlrm-calcrow{display:flex;justify-content:space-between;gap:8px;font:400 13px Heebo;padding:4px 0}" +
				".nlrm-calcrow b{font-variant-numeric:tabular-nums}";
			document.head.appendChild(st);
		}
		wireProps(); boot3d(); bootMap(); renderHealth(); renderActions(); renderSummary(); renderTax();
	}

	function wireProps() {
		document.querySelectorAll("#nlrm-props button").forEach(function (b) {
			b.addEventListener("click", function () { CUR = PROPS[parseInt(b.dataset.i, 10)]; render(); });
		});
	}

	/* ---------- health cards (six, portfolio-wide, traffic-light) ---------- */
	function healthState() {
		var H = { contract: "g", rent: "g", security: "g", repairs: "g", tax: "g", renewal: "g" };
		PROPS.forEach(function (p) {
			(p.units || []).forEach(function (u) {
				var st = unitStatus(u);
				if ("late" === st) { H.rent = "r"; } else if ("due" === st && "r" !== H.rent) { H.rent = "a"; }
				if (u.tenant_name && !(u.docs || {}).contract) { H.contract = "r"; }
				else if (u.tenant_name && docsMissing(u) > 0 && "r" !== H.contract) { H.contract = "a"; }
				var cap = secCap(u), dep = ((u.securities || {}).deposit_amount || 0);
				if (u.tenant_name && dep > cap && cap > 0) { H.security = "r"; }
				else if (u.tenant_name && !((u.securities || {}).check || (u.securities || {}).shtar || (u.securities || {}).arev || (u.securities || {}).bank) && "r" !== H.security) { H.security = "a"; }
				(u.maintenance || []).forEach(function (m) {
					if ("done" === m.status) { return; }
					var lim = "urgent" === m.urgency ? (LAW.repair_urgent_days || 3) : (LAW.repair_standard_days || 30);
					var since = daysSince(String(m.at).slice(0, 10));
					if (since !== null && since > lim) { H.repairs = "r"; }
					else if ("a" !== H.repairs && "r" !== H.repairs) { H.repairs = "a"; }
				});
				var d = daysTo(u.end);
				if (u.tenant_name && d !== null && d < 0) { H.renewal = "r"; }
				else if (d !== null && d <= (LAW.notice_landlord_days || 90) && d >= 0 && "r" !== H.renewal) { H.renewal = "a"; }
			});
		});
		var mth = new Date().getMonth() + 1;
		if (12 === mth || 1 === mth) { H.tax = "a"; }
		return H;
	}
	function renderHealth() {
		var H = healthState(), C = { g: "#517048", a: "#9C7A3C", r: "#C2563A" };
		var labels = t("health") || {};
		var h = "";
		Object.keys(H).forEach(function (k) {
			h += '<div class="nlrm-hcard"><b>' + esc(labels[k] || k) + '</b><i style="background:' + C[H[k]] + '"></i></div>';
		});
		document.getElementById("nlrm-health").innerHTML = h;
	}

	/* ---------- "my next action" feed, sorted by legal risk ---------- */
	function collectActions() {
		var acts = [];
		PROPS.forEach(function (p) {
			(p.units || []).forEach(function (u) {
				var v = { label: u.label, city: p.city };
				var st = unitStatus(u);
				if ("late" === st) { acts.push({ s: 0, txt: tpl("act_late", v) }); }
				else if ("due" === st) { acts.push({ s: 4, txt: tpl("act_due", v) }); }
				(u.maintenance || []).forEach(function (m) {
					if ("done" === m.status) { return; }
					var lim = "urgent" === m.urgency ? (LAW.repair_urgent_days || 3) : (LAW.repair_standard_days || 30);
					var since = daysSince(String(m.at).slice(0, 10));
					if ("urgent" === m.urgency) { acts.push({ s: 1, txt: tpl("act_repair", { label: u.label, d: lim }) }); }
					else if (since !== null && since > lim - 7) { acts.push({ s: 3, txt: tpl("act_repair_std", v) }); }
				});
				var d = daysTo(u.end);
				if (u.tenant_name && d !== null && d < 0) { acts.push({ s: 1, txt: tpl("act_ended", v) }); }
				else if (d !== null && d >= 0 && d <= (LAW.notice_landlord_days || 90)) { acts.push({ s: 2, txt: tpl("act_end", { label: u.label, d: d }) }); }
				var o = daysTo(u.option_until);
				if (o !== null && o >= 0 && o <= (LAW.notice_tenant_days || 60)) { acts.push({ s: 2, txt: tpl("act_opt", { label: u.label, d: o }) }); }
				var cap = secCap(u), dep = ((u.securities || {}).deposit_amount || 0);
				if (u.tenant_name && cap > 0 && dep > cap) { acts.push({ s: 1, txt: tpl("act_sec", v) }); }
				if (u.tenant_name && docsMissing(u) > 0) { acts.push({ s: 5, txt: tpl("act_docs", v) }); }
			});
		});
		var mth = new Date().getMonth() + 1;
		if (12 === mth || 1 === mth) { acts.push({ s: 2, txt: tpl("act_tax", { date: LAW.tax_deadline || "" }) }); }
		acts.sort(function (a, b) { return a.s - b.s; });
		return acts.slice(0, 10);
	}
	function renderActions() {
		var acts = collectActions();
		var C = ["#C2563A", "#C2563A", "#9C7A3C", "#9C7A3C", "#9C7A3C", "#A79E8D"];
		var h = "<h4>" + esc(t("next_actions")) + "</h4>";
		if (!acts.length) { h += '<p class="nlrm-note">' + esc(t("no_actions")) + "</p>"; }
		else {
			h += '<ul class="nlrm-acts" style="margin:0;padding:0">';
			acts.forEach(function (a) { h += '<li><i style="background:' + (C[a.s] || "#A79E8D") + '"></i>' + esc(a.txt) + "</li>"; });
			h += "</ul>";
		}
		h += '<p class="nlrm-note">' + esc(t("derived_note")) + "</p>";
		document.getElementById("nlrm-actions").innerHTML = h;
	}

	/* ---------- portfolio summary ---------- */
	function renderSummary() {
		var box = document.getElementById("nlrm-summary");
		var units = 0, rent = 0, counts = { ok: 0, due: 0, late: 0, vacant: 0 };
		PROPS.forEach(function (p) { (p.units || []).forEach(function (u) { units++; rent += u.rent || 0; counts[unitStatus(u)]++; }); });
		var h = "<h4>" + esc(t("portfolio")) + "</h4>";
		h += '<div class="nlrm-chips">';
		h += '<span class="nlrm-chip">' + units + " " + esc(t("units")) + " · " + PROPS.length + " " + esc(t("buildings")) + "</span>";
		h += '<span class="nlrm-chip">' + esc(t("monthly_rent")) + ": " + nis(rent) + "</span>";
		if (counts.late) { h += '<span class="nlrm-chip nlrm-chip--warn">' + counts.late + " " + esc(t("late_n")) + "</span>"; }
		if (counts.due) { h += '<span class="nlrm-chip nlrm-chip--gold">' + counts.due + " " + esc(t("due_n")) + "</span>"; }
		if (counts.vacant) { h += '<span class="nlrm-chip">' + counts.vacant + " " + esc(t("vacant_n")) + "</span>"; }
		h += "</div>";
		h += "<p class='nlrm-note'>" + esc(tpl("notice_l", { d: LAW.notice_landlord_days || 90 })) + " · " + esc(tpl("notice_t", { d: LAW.notice_tenant_days || 60 })) + "</p>";
		box.innerHTML = h;
	}

	/* ---------- tax estimator (2026 numbers from the server, all estimates) ---------- */
	function renderTax() {
		var box = document.getElementById("nlrm-tax");
		var totalRent = 0;
		PROPS.forEach(function (p) { (p.units || []).forEach(function (u) { totalRent += u.rent || 0; }); });
		var C = LAW.tax_ceiling || 5654;
		var h = "<h4>" + esc(tpl("tax_title", { year: LAW.tax_year || "" })) + "</h4>";
		h += '<label style="font:600 12px Heebo;color:#51483A">' + esc(t("tax_total")) + '<input type="number" id="nlrm-taxrent" value="' + totalRent + '"></label>';
		h += '<label style="font:600 12px Heebo;color:#51483A">' + esc(t("tax_paid_rent")) + '<input type="number" id="nlrm-taxpaid" value="0"></label>';
		h += '<div id="nlrm-taxout"></div>';
		h += '<p class="nlrm-note">' + esc(tpl("tax_note", { year: LAW.tax_year || "", ceiling: C.toLocaleString() })) + "</p>";
		box.innerHTML = h;
		var calc = function () {
			var G = parseInt(document.getElementById("nlrm-taxrent").value, 10) || 0;
			var P = parseInt(document.getElementById("nlrm-taxpaid").value, 10) || 0;
			var E = G <= C ? G : (G < 2 * C ? 2 * C - G : 0);
			var Tm = G - E;
			var R = G * 12;
			var D = Math.min(P, R, LAW.renter_lessor_cap || 90000);
			var ten = Math.round(0.10 * Math.max(0, R - D));
			var o = '<div class="nlrm-calcrow"><span>' + esc(t("tax_exempt")) + '</span><b>' + nis(E) + "/mo</b></div>";
			o += '<div class="nlrm-calcrow"><span>' + esc(t("tax_taxable")) + '</span><b>' + nis(Tm) + "/mo</b></div>";
			o += '<div class="nlrm-calcrow"><span>' + esc(t("tax_ten")) + '</span><b>' + nis(ten) + "</b></div>";
			o += '<p class="nlrm-note">' + esc(tpl("tax_deadline", { year: LAW.tax_year || "", date: LAW.tax_deadline || "" })) + "</p>";
			document.getElementById("nlrm-taxout").innerHTML = o;
		};
		["nlrm-taxrent", "nlrm-taxpaid"].forEach(function (id) { document.getElementById(id).addEventListener("input", calc); });
		calc();
	}

	/* ---------- the map ---------- */
	function bootMap() {
		var host = document.getElementById("nlrm-map");
		if (!TOKEN) { host.style.display = "none"; return; }
		function start() {
			mapboxgl.accessToken = TOKEN;
			var first = CUR.centroid || [34.85, 32.05];
			map = new mapboxgl.Map({ container: "nlrm-map", style: "mapbox://styles/mapbox/light-v11", center: [first[0], first[1]], zoom: 11, cooperativeGestures: true });
			map.addControl(new mapboxgl.NavigationControl());
			var bounds = new mapboxgl.LngLatBounds(); var placed = 0;
			PROPS.forEach(function (p, i) {
				var place = function (lnglat) {
					var el = document.createElement("div");
					el.style.cssText = "width:22px;height:22px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:" + (p === CUR ? "#C2563A" : "#9C7A3C") + ";border:2px solid #FAF7F1;box-shadow:0 4px 10px rgba(27,26,23,.35);cursor:pointer";
					el.title = p.address + ", " + p.city;
					el.addEventListener("click", function () { CUR = PROPS[i]; render(); });
					new mapboxgl.Marker({ element: el, anchor: "bottom" }).setLngLat(lnglat).addTo(map);
					bounds.extend(lnglat); placed++;
					if (placed === PROPS.length && placed > 1) { map.fitBounds(bounds, { padding: 60, maxZoom: 13 }); }
				};
				if (p.address && p.city) {
					fetch("https://api.mapbox.com/geocoding/v5/mapbox.places/" + encodeURIComponent(p.address + ", " + p.city + ", Israel") + ".json?access_token=" + TOKEN + "&country=il&limit=1&language=he")
						.then(function (r) { return r.json(); })
						.then(function (g) {
							if (g && g.features && g.features[0]) { place(g.features[0].center); }
							else if (p.centroid) { place(p.centroid); }
						}).catch(function () { if (p.centroid) { place(p.centroid); } });
				} else if (p.centroid) { place(p.centroid); }
			});
		}
		if (window.mapboxgl) { start(); return; }
		var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css"; document.head.appendChild(l);
		var s = document.createElement("script"); s.src = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"; s.onload = start; document.head.appendChild(s);
	}

	/* ---------- the 3D building ---------- */
	var FH = 3.05, HALF = 13.2, DIRV = { west: [-1, 0], east: [1, 0], north: [0, 1], south: [0, -1] };
	var DIR_BY_POS = ["west", "south", "east", "north"];
	function posOf(floor, pos, dir) {
		var v = DIRV[dir] || [-1, 0];
		var off = (pos % 3 - 1) * 7;
		var x = v[0] * HALF + (v[1] !== 0 ? off : 0), z = v[1] * HALF + (v[0] !== 0 ? off : 0);
		return x.toFixed(2) + "m " + (floor * FH + FH * 0.4).toFixed(2) + "m " + z.toFixed(2) + "m";
	}
	function boot3d() {
		var host = document.getElementById("nlrm-3d");
		if (!host || !GLB) { return; }
		var build = function () {
			var mv = document.createElement("model-viewer");
			mv.setAttribute("src", GLB);
			mv.setAttribute("camera-controls", ""); mv.setAttribute("interaction-prompt", "none");
			mv.setAttribute("environment-image", "neutral"); mv.setAttribute("exposure", "0.95");
			mv.setAttribute("shadow-intensity", "0.5"); mv.setAttribute("touch-action", "pan-y"); mv.setAttribute("disable-zoom", "");
			if (MODE === "demo") { }
			var fls = CUR.floors || 4, upf = CUR.units_per_floor || 3;
			/* owner 2026-07-12: opened too zoomed-in - start wider, allow pulling back further */
			mv.setAttribute("camera-target", "0 " + Math.min(18, fls * FH * 0.4).toFixed(1) + " 0");
			mv.setAttribute("camera-orbit", "-28deg 74deg " + Math.max(56, fls * FH * 2.2).toFixed(0) + "m");
			mv.setAttribute("min-camera-orbit", "auto 48deg 30m");
			mv.setAttribute("max-camera-orbit", "auto 86deg 110m");
			var owned = {};
			(CUR.units || []).forEach(function (u) { owned[u.floor + "-" + u.pos] = u; });
			for (var f = 1; f <= fls; f++) {
				for (var p = 0; p < upf; p++) {
					var key = f + "-" + p, u = owned[key];
					var b = document.createElement("button");
					b.setAttribute("slot", "hotspot-" + key);
					var dir = u ? u.dir : DIR_BY_POS[p % 4];
					b.setAttribute("data-position", posOf(f, p, dir));
					var v = DIRV[dir] || [-1, 0];
					b.setAttribute("data-normal", v[0] + " 0 " + v[1]);
					b.setAttribute("data-visibility-attribute", "visible");
					if (u) {
						b.className = "nlrm-hot";
						b.style.background = (CUR.statuses[unitStatus(u)] || CUR.statuses.vacant)[1];
						b.textContent = f; b.title = u.label;
						(function (uu) { b.addEventListener("click", function () { selectUnit(uu); }); })(u);
					} else if (CUR.can_manage) {
						b.className = "nlrm-hot is-ghost";
						b.textContent = "+";
						(function (ff, pp, dd) { b.addEventListener("click", function () { claimUnit(ff, pp, dd); }); })(f, p, dir);
					} else { continue; }
					mv.appendChild(b);
				}
			}
			host.innerHTML = "";
			host.appendChild(mv);
		};
		if (window.customElements && customElements.get("model-viewer")) { build(); return; }
		var s = document.createElement("script"); s.type = "module";
		s.src = "https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";
		s.onload = build; document.head.appendChild(s);
	}

	function claimUnit(floor, pos, dir) {
		var u = { id: "f" + floor + "-" + (pos + 1), floor: floor, pos: pos, dir: dir,
			label: (LANG === "en" ? "Apartment, floor " : "דירה בקומה ") + floor, tenant_name: "", tenant_phone: "", rent: 0,
			start: "", end: "", option_until: "", linkage: "none", base_index: 0, linked_pct: 100, floor_clause: true,
			securities: {}, docs: {}, ledger: {}, maintenance: [], note: "" };
		CUR.units.push(u);
		save(function () { selectUnit(u); boot3d(); renderAll(); });
	}
	function renderAll() { renderHealth(); renderActions(); renderSummary(); renderTax(); }

	/* ---------- the unit panel ---------- */
	function selectUnit(u) {
		var box = document.getElementById("nlrm-unit");
		var can = CUR.can_manage, dis = can ? "" : " disabled";
		var st = unitStatus(u);
		var h = "<h4>" + esc(u.label || "") + ' <span class="nlrm-chip" style="background:' + CUR.statuses[st][1] + ';color:#FAF7F1;border-color:transparent">' + esc(CUR.statuses[st][0]) + "</span></h4>";
		h += '<div class="nlrm-f">';
		h += "<label>" + esc(t("label")) + "<input id=\"nlu-label\" type=\"text\" value=\"" + esc(u.label) + '"' + dis + "></label>";
		h += "<label>" + esc(t("tenant")) + "<input id=\"nlu-tenant\" type=\"text\" value=\"" + esc(u.tenant_name) + '"' + dis + "></label>";
		h += "<label>" + esc(t("phone")) + "<input id=\"nlu-phone\" type=\"tel\" dir=\"ltr\" value=\"" + esc(u.tenant_phone) + '"' + dis + "></label>";
		h += "<label>" + esc(t("rent")) + "<input id=\"nlu-rent\" type=\"number\" value=\"" + (u.rent || "") + '"' + dis + "></label>";
		h += "<label>" + esc(t("start")) + "<input id=\"nlu-start\" type=\"date\" value=\"" + esc(u.start) + '"' + dis + "></label>";
		h += "<label>" + esc(t("end")) + "<input id=\"nlu-end\" type=\"date\" value=\"" + esc(u.end) + '"' + dis + "></label>";
		h += "<label>" + esc(t("opt")) + "<input id=\"nlu-opt\" type=\"date\" value=\"" + esc(u.option_until) + '"' + dis + "></label>";
		h += "<label>" + esc(t("linkage")) + '<select id="nlu-link"' + dis + '><option value="none"' + ("none" === u.linkage ? " selected" : "") + ">" + esc(t("link_none")) + '</option><option value="madad"' + ("madad" === u.linkage ? " selected" : "") + ">" + esc(t("link_madad")) + "</option></select></label>";
		h += "</div>";

		/* CPI calculator (visible when linked) */
		h += '<div class="nlrm-sec" id="nlu-cpi" ' + ("madad" === u.linkage ? "" : "hidden") + "><b style='font:700 13px Heebo'>" + esc(t("cpi_title")) + "</b>";
		h += '<div class="nlrm-f">';
		h += "<label>" + esc(t("cpi_base")) + "<input id=\"nlu-cpibase\" type=\"number\" step=\"0.1\" value=\"" + (u.base_index || "") + '"' + dis + "></label>";
		h += "<label>" + esc(t("cpi_cur")) + '<input id="nlu-cpicur" type="number" step="0.1" value=""></label>';
		h += "<label>" + esc(t("cpi_pct")) + "<input id=\"nlu-cpipct\" type=\"number\" min=\"0\" max=\"100\" value=\"" + (u.linked_pct || 100) + '"' + dis + "></label>";
		h += "<label style='flex-direction:row;align-items:center;gap:8px'><input type=\"checkbox\" id=\"nlu-cpifloor\" style=\"width:auto\"" + (u.floor_clause ? " checked" : "") + dis + "> " + esc(t("cpi_floor")) + "</label>";
		h += "</div><div id='nlu-cpiout'></div><p class='nlrm-note'>" + esc(t("cpi_note")) + "</p></div>";

		/* securities register with the statutory cap */
		var cap = secCap(u);
		h += '<div class="nlrm-sec"><b style="font:700 13px Heebo">' + esc(t("sec_title")) + "</b>";
		["check", "shtar", "arev", "bank"].forEach(function (k) {
			h += '<label class="nlrm-docrow"><input type="checkbox" data-sec="' + k + '"' + ((u.securities || {})[k] ? " checked" : "") + dis + "> " + esc(t("sec_" + k)) + "</label>";
		});
		h += "<label style='font:600 12px Heebo;color:#51483A'>" + esc(t("sec_amount")) + "<input id=\"nlu-secamt\" type=\"number\" value=\"" + ((u.securities || {}).deposit_amount || "") + '"' + dis + "></label>";
		if (u.rent) {
			h += '<div class="nlrm-calcrow"><span>' + esc(t("sec_cap")) + " (" + esc(t("sec_cap_f")) + ')</span><b id="nlu-seccap">' + nis(cap) + "</b></div>";
			h += '<p class="nlrm-note nlrm-chip--warn" id="nlu-secwarn" style="display:' + (((u.securities || {}).deposit_amount || 0) > cap ? "block" : "none") + ';padding:6px 10px;border-radius:8px">' + esc(t("sec_over")) + "</p>";
		}
		h += "</div>";

		/* ledger */
		h += "<p style='font:700 13px Heebo;margin:10px 0 4px'>" + esc(t("ledger")) + '</p><div class="nlrm-ledger">';
		for (var i = -11; i <= 0; i++) {
			var m = ym(i), paid = (u.ledger || {})[m] === "paid";
			h += '<button type="button" data-m="' + m + '" class="' + (paid ? "is-paid" : "") + '"' + dis + ">" + m.slice(5) + "/" + m.slice(2, 4) + (paid ? " ✓" : "") + "</button>";
		}
		h += "</div>";

		/* documents */
		h += "<p style='font:700 13px Heebo;margin:10px 0 4px'>" + esc(t("docs")) + "</p>";
		Object.keys(CUR.doc_keys).forEach(function (k) {
			h += '<label class="nlrm-docrow"><input type="checkbox" data-doc="' + k + '"' + ((u.docs || {})[k] ? " checked" : "") + dis + "> " + esc(CUR.doc_keys[k]) + "</label>";
		});

		/* maintenance with statutory deadlines */
		h += "<p style='font:700 13px Heebo;margin:10px 0 4px'>" + esc(t("maint")) + '</p><ul class="nlrm-maint">';
		(u.maintenance || []).forEach(function (mnt, idx) {
			var lim = "urgent" === mnt.urgency ? (LAW.repair_urgent_days || 3) : (LAW.repair_standard_days || 30);
			var since = daysSince(String(mnt.at).slice(0, 10));
			var over = since !== null && since > lim && "done" !== mnt.status;
			h += '<li class="' + ("done" === mnt.status ? "is-done" : "") + '"><span>' + esc(mnt.text) +
				' <span class="nlrm-note">' + esc(String(mnt.at).slice(0, 10)) + " · " + esc("urgent" === mnt.urgency ? t("urgent") : t("standard")) + " · " + esc(t("fix_by")) + ": " + lim + (LANG === "en" ? "d" : " ימים") + "</span>" +
				(over ? ' <span class="nlrm-chip nlrm-chip--warn">' + esc(t("overdue_fix")) + "</span>" : "") + "</span>" +
				(can ? '<button type="button" class="nlrm-btn nlrm-btn--ghost" style="margin:0;padding:4px 10px;font-size:11px" data-mnt="' + idx + '">' + ("done" === mnt.status ? esc(t("reopen")) : esc(t("mark_done"))) + "</button>" : "") + "</li>";
		});
		h += "</ul>";
		if (can) {
			h += '<div class="nlrm-f"><label>' + esc(t("maint_new")) + '<input type="text" id="nlu-mnt"></label>' +
				"<label>" + esc(t("urgent")) + "?" + '<select id="nlu-mnturg"><option value="standard">' + esc(t("standard")) + '</option><option value="urgent">' + esc(t("urgent")) + "</option></select></label></div>" +
				'<button type="button" class="nlrm-btn nlrm-btn--ghost" id="nlu-mntadd" style="margin:0 0 8px">' + esc(t("add")) + "</button>";
		}
		h += "<label style='font:600 12px Heebo;color:#51483A'>" + esc(t("notes")) + "<textarea id=\"nlu-note\" rows=\"2\"" + dis + ">" + esc(u.note) + "</textarea></label>";

		/* connected actions - the one-platform promise */
		h += '<div class="nlrm-actions">';
		if (u.tenant_phone) {
			var waTxt = tpl("wa_text", { name: u.tenant_name || "", month: ym(0).slice(5) + "/" + ym(0).slice(0, 4) });
			h += '<a target="_blank" rel="noopener" href="https://wa.me/' + esc(u.tenant_phone.replace(/^0/, "972")) + "?text=" + encodeURIComponent(waTxt) + '">' + esc(t("wa_btn")) + "</a>";
		}
		h += '<a href="' + esc(root.dataset.pros) + '?context=maintenance">' + esc(t("pro_btn")) + "</a>";
		h += '<a href="' + esc(root.dataset.wizard) + '">' + esc(t("list_btn")) + "</a>";
		h += '<a href="' + esc(root.dataset.studio) + '">' + esc(t("studio_btn")) + "</a>";
		h += '<a href="#" id="nlu-export">' + esc(t("export_btn")) + "</a>";
		h += "</div>";
		if (can) { h += '<button type="button" class="nlrm-btn" id="nlu-save">' + esc(t("save")) + '</button> <span class="nlrm-note" id="nlu-msg" aria-live="polite"></span>'; }
		box.innerHTML = h;
		box.scrollIntoView({ behavior: "smooth", block: "nearest" });

		/* evidence export: a printable, self-contained summary of the lease file */
		var exp = document.getElementById("nlu-export");
		if (exp) {
			exp.addEventListener("click", function (ev) {
				ev.preventDefault();
				var rtl = LANG !== "en";
				var rows = function (obj, labels) {
					return Object.keys(labels).map(function (k) {
						return "<tr><td>" + esc(labels[k]) + "</td><td>" + esc(obj[k] == null || obj[k] === "" ? "-" : String(obj[k])) + "</td></tr>";
					}).join("");
				};
				var d = '<!doctype html><html dir="' + (rtl ? "rtl" : "ltr") + '"><head><meta charset="utf-8"><title>' + esc(t("export_doc")) + "</title>" +
					"<style>body{font-family:Arial,Heebo,sans-serif;max-width:760px;margin:24px auto;color:#1B1A17;font-size:13px;line-height:1.6}h1{font-size:20px;border-bottom:2px solid #1B1A17;padding-bottom:8px}h2{font-size:15px;margin:18px 0 6px}table{width:100%;border-collapse:collapse}td{border:1px solid #ddd;padding:6px 9px;vertical-align:top}td:first-child{font-weight:700;width:38%;background:#faf7f1}ul{margin:4px 0;padding-inline-start:18px}.note{color:#777;font-size:11px;margin-top:18px;border-top:1px solid #ddd;padding-top:8px}</style></head><body>";
				d += "<h1>" + esc(t("export_doc")) + " - " + esc(u.label) + "</h1>";
				d += "<p>" + esc(CUR.address + ", " + CUR.city) + " · " + esc(t("export_gen")) + ": " + new Date().toLocaleString(rtl ? "he-IL" : "en-GB") + "</p>";
				d += "<h2>" + esc(t("sel_title")) + "</h2><table>" + rows({
					a: u.tenant_name, b: u.tenant_phone, c: nis(u.rent), d: u.start, e: u.end, f: u.option_until,
					g: ("madad" === u.linkage ? t("link_madad") + " (" + (u.linked_pct || 100) + "%, " + t("cpi_base") + " " + (u.base_index || "-") + ")" : t("link_none"))
				}, { a: t("tenant"), b: t("phone"), c: t("rent"), d: t("start"), e: t("end"), f: t("opt"), g: t("linkage") }) + "</table>";
				d += "<h2>" + esc(t("sec_title")) + "</h2><ul>";
				["check", "shtar", "arev", "bank"].forEach(function (k) { if ((u.securities || {})[k]) { d += "<li>" + esc(t("sec_" + k)) + "</li>"; } });
				if ((u.securities || {}).deposit_amount) { d += "<li>" + esc(t("sec_amount")) + ": " + nis(u.securities.deposit_amount) + " (" + esc(t("sec_cap")) + ": " + nis(secCap(u)) + ")</li>"; }
				d += "</ul>";
				d += "<h2>" + esc(t("ledger")) + "</h2><table><tr>";
				for (var i = -11; i <= 0; i++) { d += "<td style='width:auto;background:none;font-weight:400;text-align:center'>" + ym(i).slice(5) + "/" + ym(i).slice(2, 4) + "<br><b>" + ((u.ledger || {})[ym(i)] === "paid" ? "✓" : "-") + "</b></td>"; }
				d += "</tr></table>";
				d += "<h2>" + esc(t("docs")) + "</h2><ul>";
				Object.keys(CUR.doc_keys).forEach(function (k) { d += "<li>" + esc(CUR.doc_keys[k]) + ": <b>" + ((u.docs || {})[k] ? "✓" : "-") + "</b></li>"; });
				d += "</ul><h2>" + esc(t("maint")) + "</h2><ul>";
				(u.maintenance || []).forEach(function (m) { d += "<li>" + esc(String(m.at).slice(0, 10)) + " · " + esc(m.text) + " · " + esc("done" === m.status ? t("mark_done") : ("urgent" === m.urgency ? t("urgent") : t("standard"))) + "</li>"; });
				if (!(u.maintenance || []).length) { d += "<li>-</li>"; }
				d += "</ul>";
				if (u.note) { d += "<h2>" + esc(t("notes")) + "</h2><p>" + esc(u.note) + "</p>"; }
				d += '<p class="note">' + esc(t("export_note")) + "</p></body></html>";
				var w = window.open("", "_blank");
				if (w) { w.document.write(d); w.document.close(); setTimeout(function () { try { w.print(); } catch (e) { /* user prints manually */ } }, 400); }
			});
		}

		/* CPI live calc (works read-only too - current index is a local input) */
		var cpiCalc = function () {
			var out = document.getElementById("nlu-cpiout");
			var base = parseFloat(document.getElementById("nlu-cpibase").value) || 0;
			var cur = parseFloat(document.getElementById("nlu-cpicur").value) || 0;
			var pct = (parseInt(document.getElementById("nlu-cpipct").value, 10) || 0) / 100;
			var flo = document.getElementById("nlu-cpifloor").checked;
			if (!base || !cur || !u.rent) { out.innerHTML = ""; return; }
			var r = u.rent * (1 + pct * (cur / base - 1));
			if (flo) { r = Math.max(u.rent, r); }
			out.innerHTML = '<div class="nlrm-calcrow"><span>' + esc(t("cpi_res")) + "</span><b>" + nis(Math.round(r)) + "</b></div>";
		};
		["nlu-cpibase", "nlu-cpicur", "nlu-cpipct", "nlu-cpifloor"].forEach(function (id) {
			var el = document.getElementById(id); if (el) { el.addEventListener("input", cpiCalc); el.addEventListener("change", cpiCalc); }
		});
		var linkSel = document.getElementById("nlu-link");
		if (linkSel) { linkSel.addEventListener("change", function () { document.getElementById("nlu-cpi").hidden = "madad" !== linkSel.value; }); }

		if (!can) { return; }
		box.querySelectorAll(".nlrm-ledger button").forEach(function (bt) {
			bt.addEventListener("click", function () {
				u.ledger = u.ledger || {};
				u.ledger[bt.dataset.m] = u.ledger[bt.dataset.m] === "paid" ? "open" : "paid";
				selectUnit(u);
			});
		});
		box.querySelectorAll("[data-mnt]").forEach(function (bt) {
			bt.addEventListener("click", function () {
				var mnt = u.maintenance[parseInt(bt.dataset.mnt, 10)];
				mnt.status = "done" === mnt.status ? "open" : "done";
				selectUnit(u);
			});
		});
		var madd = document.getElementById("nlu-mntadd");
		if (madd) {
			madd.addEventListener("click", function () {
				var txt = document.getElementById("nlu-mnt").value.trim();
				if (!txt) { return; }
				u.maintenance = u.maintenance || [];
				u.maintenance.unshift({ text: txt, at: new Date().toISOString().slice(0, 10), status: "open", urgency: document.getElementById("nlu-mnturg").value });
				selectUnit(u);
			});
		}
		var secAmt = document.getElementById("nlu-secamt");
		if (secAmt) {
			secAmt.addEventListener("input", function () {
				var w = document.getElementById("nlu-secwarn");
				if (w) { w.style.display = (parseInt(secAmt.value, 10) || 0) > secCap(u) ? "block" : "none"; }
			});
		}
		document.getElementById("nlu-save").addEventListener("click", function () {
			u.label = document.getElementById("nlu-label").value;
			u.tenant_name = document.getElementById("nlu-tenant").value;
			u.tenant_phone = document.getElementById("nlu-phone").value;
			u.rent = parseInt(document.getElementById("nlu-rent").value, 10) || 0;
			u.start = document.getElementById("nlu-start").value;
			u.end = document.getElementById("nlu-end").value;
			u.option_until = document.getElementById("nlu-opt").value;
			u.linkage = document.getElementById("nlu-link").value;
			u.base_index = parseFloat(document.getElementById("nlu-cpibase").value) || 0;
			u.linked_pct = parseInt(document.getElementById("nlu-cpipct").value, 10) || 100;
			u.floor_clause = document.getElementById("nlu-cpifloor").checked;
			u.securities = u.securities || {};
			box.querySelectorAll("[data-sec]").forEach(function (cb) { u.securities[cb.dataset.sec] = cb.checked; });
			u.securities.deposit_amount = parseInt(document.getElementById("nlu-secamt").value, 10) || 0;
			u.docs = u.docs || {};
			box.querySelectorAll("[data-doc]").forEach(function (cb) { u.docs[cb.dataset.doc] = cb.checked; });
			u.note = document.getElementById("nlu-note").value;
			document.getElementById("nlu-msg").textContent = t("saving");
			save(function () {
				document.getElementById("nlu-msg").textContent = t("saved");
				boot3d(); renderAll();
			});
		});
	}

	function save(done) {
		api("/rental-prop/" + CUR.id + "/units" + QS, { method: "POST", body: JSON.stringify({ units: CUR.units }) })
			.then(function (d) {
				CUR.units = d.units;
				if (done) { done(); }
			})
			.catch(function () { var m = document.getElementById("nlu-msg"); if (m) { m.textContent = t("save_fail"); } });
	}

	load();
})();
