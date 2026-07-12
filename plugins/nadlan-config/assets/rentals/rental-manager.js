/* ============================================================================
   NADLAN RENTALS MANAGER (v1, 2026-07-12).
   The wow-flow (owner order): portfolio MAP on top -> click a building ->
   its 3D model -> click your apartment -> manage everything (tenant, rent
   ledger, deadline chips, documents, maintenance, real actions).
   Modes: demo (public read-only portfolio on the landing) / live (owner).
   Honest v1: tracking + reminders. No payments, no screening.
============================================================================ */
(function () {
	"use strict";
	var root = document.getElementById("nlrm-mount");
	if (!root || root.dataset.wired) { return; }
	root.dataset.wired = "1";

	var MODE = root.dataset.mode || "live";
	var REST = root.dataset.rest;
	var NONCE = root.dataset.nonce || "";
	var GLB = root.dataset.glb || "";
	var TOKEN = root.dataset.mapbox || "";
	var PROPS = [], CUR = null, SEL = null, map = null, markers = [];

	function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
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

	/* derived unit status: the color IS the state of the rent */
	function unitStatus(u) {
		if (!u.tenant_name) { return "vacant"; }
		var led = u.ledger || {};
		if (u.start && u.start <= ym(-1) + "-28" && led[ym(-1)] !== "paid") { return "late"; }
		if (led[ym(0)] !== "paid") { return "due"; }
		return "ok";
	}

	function load() {
		var p = MODE === "demo" ? api("/rental-demo") : api("/rental-props");
		p.then(function (d) {
			PROPS = d.props || [];
			if (!PROPS.length) { root.innerHTML = '<p class="nlrm-note">אין נכסים עדיין - הוסיפו את הראשון למטה.</p>'; root.removeAttribute("data-loading"); return; }
			CUR = PROPS[0];
			render();
		}).catch(function () { root.innerHTML = '<p class="nlrm-note">לא הצלחנו לטעון את הנכסים.</p>'; });
	}

	function render() {
		var h = "";
		h += '<div class="nlrm-map" id="nlrm-map"></div>';
		h += '<div class="nlrm-props" id="nlrm-props">';
		PROPS.forEach(function (p, i) {
			h += '<button type="button" data-i="' + i + '" class="' + (p === CUR ? "is-on" : "") + '">' + esc(p.address + ", " + p.city) + " · " + (p.units || []).length + " דירות</button>";
		});
		h += "</div>";
		h += '<div class="nlrm-3d" id="nlrm-3d"></div>';
		h += '<div class="nlrm-legend">';
		Object.keys(CUR.statuses).forEach(function (k) { h += "<span><i style=\"background:" + CUR.statuses[k][1] + '"></i>' + esc(CUR.statuses[k][0]) + "</span>"; });
		h += "</div>";
		h += '<div class="nlrm-grid">';
		h += '<div class="nlrm-card" id="nlrm-unit"><h4>הדירה שנבחרה</h4><p class="nlrm-note">' +
			(CUR.can_manage ? "הקישו על דירה במודל. דירה מקווקוות = עדיין לא סומנה כשלכם - הקישו כדי להוסיף אותה לתיק." : "הקישו על דירה צבועה במודל כדי לראות את ניהול ההשכרה שלה.") + "</p></div>";
		h += '<div class="nlrm-card" id="nlrm-summary"></div>';
		h += "</div>";
		root.innerHTML = h;
		root.removeAttribute("data-loading");
		wireProps(); boot3d(); bootMap(); renderSummary();
	}

	function wireProps() {
		document.querySelectorAll("#nlrm-props button").forEach(function (b) {
			b.addEventListener("click", function () {
				CUR = PROPS[parseInt(b.dataset.i, 10)]; SEL = null;
				render();
			});
		});
	}

	/* ---------- portfolio summary (the whole point: one glance) ---------- */
	function renderSummary() {
		var box = document.getElementById("nlrm-summary");
		var units = [], rent = 0, counts = { ok: 0, due: 0, late: 0, vacant: 0 };
		PROPS.forEach(function (p) { (p.units || []).forEach(function (u) { units.push(u); rent += u.rent || 0; counts[unitStatus(u)]++; }); });
		var h = "<h4>תמונת התיק</h4>";
		h += '<div class="nlrm-chips">';
		h += '<span class="nlrm-chip">' + units.length + " דירות ב-" + PROPS.length + " בניינים</span>";
		h += '<span class="nlrm-chip">שכר דירה חודשי: ₪' + rent.toLocaleString() + "</span>";
		if (counts.late) { h += '<span class="nlrm-chip nlrm-chip--warn">' + counts.late + " בפיגור</span>"; }
		if (counts.due) { h += '<span class="nlrm-chip nlrm-chip--gold">' + counts.due + " טרם סומנו החודש</span>"; }
		if (counts.vacant) { h += '<span class="nlrm-chip">' + counts.vacant + " פנויות</span>"; }
		h += "</div>";
		/* the deadline engine: every unit's chips, portfolio-wide */
		var chips = [];
		PROPS.forEach(function (p) {
			(p.units || []).forEach(function (u) {
				var d = daysTo(u.end);
				if (null !== d && d >= 0 && d <= 90) { chips.push('<span class="nlrm-chip nlrm-chip--gold">' + esc(u.label) + ", " + esc(p.city) + ": החוזה מסתיים בעוד " + d + " ימים</span>"); }
				if (null !== d && d < 0 && u.tenant_name) { chips.push('<span class="nlrm-chip nlrm-chip--warn">' + esc(u.label) + ", " + esc(p.city) + ": החוזה הסתיים - חידוש?</span>"); }
				var o = daysTo(u.option_until);
				if (null !== o && o >= 0 && o <= 60) { chips.push('<span class="nlrm-chip nlrm-chip--gold">' + esc(u.label) + ": חלון האופציה נסגר בעוד " + o + " ימים</span>"); }
			});
		});
		var now = new Date(), mth = now.getMonth() + 1;
		if (12 === mth || 1 === mth) { chips.push('<span class="nlrm-chip nlrm-chip--gold">תזכורת: דיווח ותשלום במסלול 10% עד 30 בינואר (בדקו מול רשות המסים)</span>'); }
		if (chips.length) { h += "<p style='font:700 13px Heebo;margin:10px 0 4px'>תזכורות</p><div class='nlrm-chips'>" + chips.join("") + "</div>"; }
		h += '<p class="nlrm-note">נגזר אוטומטית מהנתונים שהזנתם. תזכורות בלבד - לא ייעוץ מס או ייעוץ משפטי.</p>';
		box.innerHTML = h;
	}

	/* ---------- the map (click a building -> its 3D loads) ---------- */
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
					el.addEventListener("click", function () { CUR = PROPS[i]; SEL = null; render(); });
					markers.push(new mapboxgl.Marker({ element: el, anchor: "bottom" }).setLngLat(lnglat).addTo(map));
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
			if (MODE === "demo") { mv.setAttribute("auto-rotate", ""); mv.setAttribute("rotation-per-second", "8deg"); }
			var fls = CUR.floors || 4, upf = CUR.units_per_floor || 3;
			mv.setAttribute("camera-target", "0 " + Math.min(20, fls * FH * 0.45).toFixed(1) + " 0");
			mv.setAttribute("camera-orbit", "-28deg 76deg " + Math.max(40, fls * FH * 1.6).toFixed(0) + "m");
			mv.setAttribute("min-camera-orbit", "auto 48deg 26m");
			mv.setAttribute("max-camera-orbit", "auto 86deg 90m");
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
						b.textContent = "+"; b.title = "סימון כדירה שלי";
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
			label: "דירה בקומה " + floor, tenant_name: "", tenant_phone: "", rent: 0,
			start: "", end: "", option_until: "", linkage: "none", docs: {}, ledger: {}, maintenance: [], note: "" };
		CUR.units.push(u);
		save(function () { selectUnit(u); boot3d(); renderSummary(); });
	}

	/* ---------- the unit management panel ---------- */
	function selectUnit(u) {
		SEL = u;
		var box = document.getElementById("nlrm-unit");
		var can = CUR.can_manage;
		var dis = can ? "" : " disabled";
		var st = unitStatus(u);
		var h = "<h4>" + esc(u.label || "דירה") + ' <span class="nlrm-chip" style="background:' + CUR.statuses[st][1] + ';color:#FAF7F1;border-color:transparent">' + esc(CUR.statuses[st][0]) + "</span></h4>";
		h += '<div class="nlrm-f">';
		h += "<label>שם הדירה<input id=\"nlu-label\" type=\"text\" value=\"" + esc(u.label) + '"' + dis + "></label>";
		h += "<label>שוכר<input id=\"nlu-tenant\" type=\"text\" value=\"" + esc(u.tenant_name) + '"' + dis + "></label>";
		h += "<label>טלפון שוכר<input id=\"nlu-phone\" type=\"tel\" dir=\"ltr\" value=\"" + esc(u.tenant_phone) + '"' + dis + "></label>";
		h += "<label>שכר דירה חודשי (₪)<input id=\"nlu-rent\" type=\"number\" value=\"" + (u.rent || "") + '"' + dis + "></label>";
		h += "<label>תחילת חוזה<input id=\"nlu-start\" type=\"date\" value=\"" + esc(u.start) + '"' + dis + "></label>";
		h += "<label>סיום חוזה<input id=\"nlu-end\" type=\"date\" value=\"" + esc(u.end) + '"' + dis + "></label>";
		h += "<label>אופציה עד<input id=\"nlu-opt\" type=\"date\" value=\"" + esc(u.option_until) + '"' + dis + "></label>";
		h += '<label>הצמדה<select id="nlu-link"' + dis + '><option value="none"' + ("none" === u.linkage ? " selected" : "") + '>ללא</option><option value="madad"' + ("madad" === u.linkage ? " selected" : "") + '>צמוד מדד</option></select></label>';
		h += "</div>";
		/* rent ledger: last 12 months, one tap = paid */
		h += "<p style='font:700 13px Heebo;margin:10px 0 4px'>מעקב תשלומים (12 חודשים)</p><div class=\"nlrm-ledger\">";
		for (var i = -11; i <= 0; i++) {
			var m = ym(i), paid = (u.ledger || {})[m] === "paid";
			h += '<button type="button" data-m="' + m + '" class="' + (paid ? "is-paid" : "") + '"' + dis + ">" + m.slice(5) + "/" + m.slice(2, 4) + (paid ? " ✓" : "") + "</button>";
		}
		h += "</div>";
		h += "<p style='font:700 13px Heebo;margin:10px 0 4px'>תיק מסמכים</p>";
		Object.keys(CUR.doc_keys).forEach(function (k) {
			h += '<label class="nlrm-docrow"><input type="checkbox" data-doc="' + k + '"' + ((u.docs || {})[k] ? " checked" : "") + dis + "> " + esc(CUR.doc_keys[k]) + "</label>";
		});
		h += "<p style='font:700 13px Heebo;margin:10px 0 4px'>תחזוקה</p><ul class=\"nlrm-maint\">";
		(u.maintenance || []).forEach(function (mnt, idx) {
			h += '<li class="' + ("done" === mnt.status ? "is-done" : "") + '"><span>' + esc(mnt.text) + ' <span class="nlrm-note">' + esc(mnt.at) + "</span></span>" +
				(can ? '<button type="button" class="nlrm-btn nlrm-btn--ghost" style="margin:0;padding:4px 10px;font-size:11px" data-mnt="' + idx + '">' + ("done" === mnt.status ? "פתיחה" : "טופל") + "</button>" : "") + "</li>";
		});
		h += "</ul>";
		if (can) { h += '<div class="nlrm-f"><label>תקלה חדשה<input type="text" id="nlu-mnt"></label><label>&nbsp;<button type="button" class="nlrm-btn nlrm-btn--ghost" id="nlu-mntadd" style="margin:0">הוספה</button></label></div>'; }
		h += "<label style='font:600 12px Heebo;color:#51483A'>הערות<textarea id=\"nlu-note\" rows=\"2\"" + dis + ">" + esc(u.note) + "</textarea></label>";
		/* real actions - no placeholders */
		h += '<div class="nlrm-actions">';
		if (u.tenant_phone) { h += '<a target="_blank" rel="noopener" href="https://wa.me/' + esc(u.tenant_phone.replace(/^0/, "972")) + "?text=" + encodeURIComponent("היי " + (u.tenant_name || "") + ", תזכורת ידידותית לשכר הדירה של " + ym(0).slice(5) + "/" + ym(0).slice(0, 4) + ". תודה!") + '">תזכורת בוואטסאפ</a>'; }
		h += '<a href="' + esc(root.dataset.pros) + '?context=maintenance">מציאת בעל מקצוע</a>';
		h += '<a href="' + esc(root.dataset.wizard) + '">פרסום הדירה</a>';
		h += "</div>";
		if (can) { h += '<button type="button" class="nlrm-btn" id="nlu-save">שמירה</button> <span class="nlrm-note" id="nlu-msg" aria-live="polite"></span>'; }
		box.innerHTML = h;
		box.scrollIntoView({ behavior: "smooth", block: "nearest" });
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
				var t = document.getElementById("nlu-mnt").value.trim();
				if (!t) { return; }
				u.maintenance = u.maintenance || [];
				u.maintenance.unshift({ text: t, at: new Date().toISOString().slice(0, 10), status: "open" });
				selectUnit(u);
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
			u.note = document.getElementById("nlu-note").value;
			document.getElementById("nlu-msg").textContent = "שומרים...";
			save(function () {
				document.getElementById("nlu-msg").textContent = "נשמר";
				boot3d(); renderSummary();
			});
		});
	}

	function save(done) {
		api("/rental-prop/" + CUR.id + "/units", { method: "POST", body: JSON.stringify({ units: CUR.units }) })
			.then(function (d) {
				CUR.units = d.units;
				var i = PROPS.indexOf(CUR); if (i > -1) { PROPS[i] = Object.assign(CUR, d); }
				if (done) { done(); }
			})
			.catch(function () { var m = document.getElementById("nlu-msg"); if (m) { m.textContent = "השמירה נכשלה, נסו שוב"; } });
	}

	load();
})();
