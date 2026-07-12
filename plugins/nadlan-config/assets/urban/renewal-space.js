/* ============================================================================
   NADLAN URBAN RENEWAL - project space app (v2 layout, 2026-07-12).
   One app, two modes:
     mode=live  - authenticated member/owner space (REST /renewal-space/{id})
     mode=demo  - public read-only demo space (REST /renewal-demo), mounted on
                  the /my-renewal/ product landing so visitors see the WORKING
                  system before signing up.
   Layout law (owner order): 3D model FULL WIDTH ON TOP, interactive progress
   stepper attached right under it, then cards: selected apartment, live map
   (responds to clicks), auto to-do list, documents rollup, updates, invite.
   All UI strings arrive via data-i18n JSON (HE/EN) - no hardcoded copy here.
============================================================================ */
(function () {
	"use strict";
	var root = document.getElementById("nlurd-mount");
	if (!root || root.dataset.wired) { return; }
	root.dataset.wired = "1";

	var MODE = root.dataset.mode || "live";
	var REST = root.dataset.rest;
	var NONCE = root.dataset.nonce || "";
	var GLB = root.dataset.glb || "";
	var LANG = root.dataset.lang || "he";
	var QS = LANG !== "he" ? "?lang=" + LANG : "";
	var I = {};
	try { I = JSON.parse(root.dataset.i18n || "{}"); } catch (e) { I = {}; }
	var S = null, selApt = null, map = null, mapMarker = null;

	function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
	function t(k) { return I[k] || k; }
	function api(path, opts) {
		opts = opts || {};
		opts.headers = Object.assign({ "Content-Type": "application/json" }, NONCE ? { "X-WP-Nonce": NONCE } : {}, opts.headers || {});
		return fetch(REST + path, opts).then(function (r) { return r.json().then(function (j) { if (!r.ok) { throw j; } return j; }); });
	}

	/* ---------- boot ---------- */
	function load() {
		var p = MODE === "demo" ? api("/renewal-demo" + QS) : api("/renewal-space/" + root.dataset.space + QS);
		p.then(function (d) { S = d; render(); }).catch(function () {
			root.innerHTML = '<p class="nlurd-note">' + esc(t("load_fail")) + "</p>";
		});
	}

	/* ---------- derived ---------- */
	function counts() {
		var c = {};
		(S.apartments || []).forEach(function (a) { c[a.consent_status] = (c[a.consent_status] || 0) + 1; });
		return c;
	}
	function docsRollup() {
		var keys = Object.keys(S.doc_keys || {}), per = {}, done = 0, total = 0;
		keys.forEach(function (k) { per[k] = 0; });
		(S.apartments || []).forEach(function (a) {
			keys.forEach(function (k) { total++; if (a.docs && a.docs[k]) { per[k]++; done++; } });
		});
		return { per: per, done: done, total: total, apts: (S.apartments || []).length };
	}

	/* ---------- render ---------- */
	function render() {
		var c = counts(), pct = S.consents.pct;
		var bar = '<div class="nlurd-break" role="img" aria-label="' + esc(t("consent_mix")) + '">';
		Object.keys(S.statuses).forEach(function (k) {
			var n = c[k] || 0; if (!n) { return; }
			bar += '<i style="flex:' + n + ";background:" + S.statuses[k][1] + '" title="' + esc(S.statuses[k][0]) + ": " + n + '"></i>';
		});
		bar += "</div>";

		var h = "";
		/* top strip: identity + gauge */
		h += '<div class="nlurd-top"><div><h2 class="nlurd-title">' + esc(S.title) + "</h2>" +
			'<p class="nlurd-sub">' + esc(S.address ? S.address + ", " + S.city : S.city) +
			(S.track ? ' <span class="nlurd-chip">' + esc(t("track_" + S.track) === "track_" + S.track ? S.track : t("track_" + S.track)) + "</span>" : "") +
			(S.is_demo ? ' <span class="nlurd-chip nlurd-chip--demo">' + esc(t("demo_badge")) + "</span>" : "") + "</p></div>" +
			'<div class="nlurd-gauge"><b>' + esc(String(pct)) + "%</b> " + esc(t("gauge")) + " · " + S.consents.yes + "/" + S.consents.total + "</div></div>";
		h += bar;

		/* 3D stage - full width, on top */
		h += '<div class="nlurd-3d" id="nlurd-3dhost"><div class="nlurd-3dhint">' + esc(t("hint_3d")) + "</div></div>";
		h += '<div class="nlurd-legend">';
		Object.keys(S.statuses).forEach(function (k) { h += '<span><i style="background:' + S.statuses[k][1] + '"></i>' + esc(S.statuses[k][0]) + "</span>"; });
		h += "</div>";

		/* interactive stepper */
		h += '<div class="nlurd-stepper" id="nlurd-stepper" role="tablist">';
		(S.ladder || []).forEach(function (l, i) {
			var cls = i < S.stage ? "is-done" : i === S.stage ? "is-now" : "";
			h += '<button type="button" role="tab" class="nlurd-step ' + cls + '" data-st="' + i + '"><i>' + (i + 1) + "</i><span>" + esc(l) + "</span></button>";
		});
		h += "</div>";
		h += '<div class="nlurd-stepcard nlurd-card" id="nlurd-stepcard" hidden></div>';

		/* cards grid */
		h += '<div class="nlurd-grid">';
		h += '<div class="nlurd-card" id="nlurd-apt"><h4>' + esc(t("apt_title")) + '</h4><p class="nlurd-note">' + esc(t("apt_hint")) + "</p></div>";
		h += '<div class="nlurd-card nlurd-mapcard" id="nlurd-mapcard"><h4>' + esc(t("map_title")) + '</h4><div class="nlurd-map" id="nlurd-map"></div><div class="nlurd-mapchips" id="nlurd-mapchips"></div></div>';
		h += '<div class="nlurd-card" id="nlurd-todo"></div>';
		h += '<div class="nlurd-card" id="nlurd-docs"></div>';
		h += '<div class="nlurd-card"><h4>' + esc(t("updates")) + "</h4>" +
			(S.can_manage ? '<textarea id="nlurd-uptext" rows="2" placeholder="' + esc(t("upd_ph")) + '"></textarea><button class="nlurd-btn" id="nlurd-upsend">' + esc(t("upd_send")) + "</button>" : "") +
			'<ul class="nlurd-updates">';
		(S.updates || []).forEach(function (u) { h += "<li>" + esc(u.text) + "<time>" + esc(u.at) + "</time></li>"; });
		if (!(S.updates || []).length) { h += '<li class="nlurd-note">' + esc(t("upd_none")) + "</li>"; }
		h += "</ul></div>";
		if (S.can_manage) {
			h += '<div class="nlurd-card nlurd-invite"><h4>' + esc(t("inv_title")) + '</h4><p class="nlurd-note">' + esc(t("inv_note")) + '</p><button class="nlurd-btn" id="nlurd-invbtn">' + esc(t("inv_btn")) + '</button><input type="text" id="nlurd-invurl" readonly hidden></div>';
		}
		if (S.stage_log && S.stage_log.length) {
			h += '<div class="nlurd-card"><h4>' + esc(t("history")) + '</h4><ul class="nlurd-updates">';
			S.stage_log.forEach(function (l) { h += "<li>" + esc((S.ladder || [])[l.stage] || l.stage) + "<time>" + esc(l.at) + "</time></li>"; });
			h += "</ul></div>";
		}
		h += "</div>";

		root.innerHTML = h;
		root.removeAttribute("data-loading");
		boot3d(); wire(); renderTodo(); renderDocs(); bootMap();
	}

	/* ---------- stepper ---------- */
	function stepCard(i) {
		var box = document.getElementById("nlurd-stepcard");
		var note = (S.stage_notes || [])[i] || {};
		var hist = "";
		(S.stage_log || []).forEach(function (l) { if (l.stage === i && !hist) { hist = l.at; } });
		var h = "<h4><i>" + (i + 1) + "</i> " + esc((S.ladder || [])[i] || "") + "</h4>";
		if (note.desc) { h += "<p>" + esc(note.desc) + "</p>"; }
		if (note.duration) { h += '<p class="nlurd-note">' + esc(t("typical")) + ": " + esc(note.duration) + " · " + esc(t("avg_note")) + "</p>"; }
		if (note.actions && note.actions.length) {
			h += "<p><b>" + esc(t("next_actions")) + ":</b></p><ul class='nlurd-acts'>";
			note.actions.forEach(function (a) { h += "<li>" + esc(a) + "</li>"; });
			h += "</ul>";
		}
		if (hist) { h += '<p class="nlurd-note">' + esc(t("reached_at")) + ": " + esc(hist) + "</p>"; }
		if (S.can_manage && i !== S.stage) {
			h += '<button class="nlurd-btn" id="nlurd-setstage" data-st="' + i + '">' + esc(t("set_stage")) + "</button>";
		}
		box.innerHTML = h;
		box.hidden = false;
		var set = document.getElementById("nlurd-setstage");
		if (set) {
			set.addEventListener("click", function () {
				api("/renewal-space/" + S.id + "/stage" + QS, { method: "POST", body: JSON.stringify({ stage: set.dataset.st }) })
					.then(function (d) { S = d; render(); });
			});
		}
	}

	/* ---------- to-do (derived honestly from the room's data) ---------- */
	function renderTodo() {
		var box = document.getElementById("nlurd-todo");
		var c = counts(), pct = S.consents.pct, r = docsRollup();
		var items = [
			{ txt: t("td_map"), done: !c.unreached },
			{ txt: t("td_66"), done: pct >= 66 },
			{ txt: t("td_67"), done: pct >= 67 },
			{ txt: t("td_80"), done: pct >= 80 },
			{ txt: t("td_docs"), done: r.total > 0 && r.done === r.total },
			{ txt: t("td_pros"), done: S.stage >= 3 },
			{ txt: t("td_dev"), done: S.stage >= 5 }
		];
		var h = "<h4>" + esc(t("todo_title")) + "</h4><ul class='nlurd-todos'>";
		items.forEach(function (it) {
			h += '<li class="' + (it.done ? "is-done" : "") + '"><i>' + (it.done ? "&#10003;" : "") + "</i>" + esc(it.txt) + "</li>";
		});
		h += "</ul>";
		var note = (S.stage_notes || [])[S.stage];
		if (note && note.actions && note.actions.length) {
			h += "<p><b>" + esc(t("now_actions")) + ":</b></p><ul class='nlurd-acts'>";
			note.actions.forEach(function (a) { h += "<li>" + esc(a) + "</li>"; });
			h += "</ul>";
		}
		h += '<p class="nlurd-note">' + esc(t("todo_note")) + "</p>";
		box.innerHTML = h;
	}

	/* ---------- documents rollup ---------- */
	function renderDocs() {
		var box = document.getElementById("nlurd-docs");
		var r = docsRollup();
		var pctd = r.total ? Math.round(r.done / r.total * 100) : 0;
		var h = "<h4>" + esc(t("docs_title")) + "</h4>";
		h += '<div class="nlurd-meter"><i style="width:' + pctd + '%"></i></div>';
		h += '<p class="nlurd-note">' + r.done + " / " + r.total + " · " + pctd + "%</p>";
		Object.keys(S.doc_keys || {}).forEach(function (k) {
			h += '<div class="nlurd-docrow"><span>' + esc(S.doc_keys[k]) + "</span><b>" + r.per[k] + "/" + r.apts + "</b></div>";
		});
		h += '<p class="nlurd-note">' + esc(t("docs_hint")) + "</p>";
		box.innerHTML = h;
	}

	/* ---------- live map (responds to clicks) ---------- */
	function bootMap() {
		var card = document.getElementById("nlurd-mapcard");
		var token = root.dataset.mapbox || "";
		var cent = S.centroid && S.centroid.length === 2 ? S.centroid : null;
		if (!token || (!cent && !S.city)) { card.hidden = true; return; }
		var chips = document.getElementById("nlurd-mapchips");
		var ch = "";
		if (S.city) { ch += '<a class="nlurd-chip" href="' + esc(root.dataset.maplink || "#") + '">' + esc(S.city) + "</a>"; }
		if (typeof S.compounds_in_city === "number" && S.compounds_in_city > 0) {
			ch += '<a class="nlurd-chip" href="' + esc(root.dataset.maplink || "#") + '">' + esc(t("compounds")) + ": " + S.compounds_in_city + "</a>";
		}
		chips.innerHTML = ch;
		function start() {
			mapboxgl.accessToken = token;
			var center = cent ? [cent[0], cent[1]] : [34.9, 32.0];
			map = new mapboxgl.Map({ container: "nlurd-map", style: "mapbox://styles/mapbox/light-v11", center: center, zoom: cent ? 12 : 7, cooperativeGestures: true, attributionControl: true });
			map.addControl(new mapboxgl.NavigationControl());
			function place(lnglat, precise) {
				var el = document.createElement("div");
				el.className = "nlurd-pin";
				mapMarker = new mapboxgl.Marker({ element: el, anchor: "bottom" }).setLngLat(lnglat)
					.setPopup(new mapboxgl.Popup({ offset: 18 }).setHTML(
						"<b>" + esc(S.address || S.title) + "</b><br>" + esc(S.city) +
						"<br>" + esc(t("gauge")) + ": " + S.consents.pct + "%" +
						(precise ? "" : "<br><i>" + esc(t("map_approx")) + "</i>")
					)).addTo(map);
				map.flyTo({ center: lnglat, zoom: precise ? 15.4 : 12.4, essential: true });
			}
			/* try a precise forward geocode of the address; degrade to centroid honestly */
			if (S.address && S.city) {
				fetch("https://api.mapbox.com/geocoding/v5/mapbox.places/" + encodeURIComponent(S.address + ", " + S.city + ", Israel") + ".json?access_token=" + token + "&country=il&limit=1&language=he")
					.then(function (r) { return r.json(); })
					.then(function (g) {
						if (g && g.features && g.features[0] && g.features[0].relevance > 0.6) { place(g.features[0].center, true); }
						else if (cent) { place(center, false); }
					}).catch(function () { if (cent) { place(center, false); } });
			} else if (cent) { place(center, false); }
		}
		if (window.mapboxgl) { start(); return; }
		var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css"; document.head.appendChild(l);
		var s = document.createElement("script"); s.src = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"; s.onload = start; document.head.appendChild(s);
	}
	function pingMap() { if (mapMarker && map) { mapMarker.togglePopup(); if (!mapMarker.getPopup().isOpen()) { mapMarker.togglePopup(); } } }

	/* ---------- 3D ---------- */
	var FH = 3.05, HALF = 13.2, DIRV = { west: [-1, 0], east: [1, 0], north: [0, 1], south: [0, -1] };
	function aptPos(a) {
		var v = DIRV[a.dir] || [-1, 0];
		var off = (a.pos % 3 - 1) * 7;
		var x = v[0] * HALF + (v[1] !== 0 ? off : 0), z = v[1] * HALF + (v[0] !== 0 ? off : 0);
		return x.toFixed(2) + "m " + (a.floor * FH + FH * 0.4).toFixed(2) + "m " + z.toFixed(2) + "m";
	}
	function boot3d() {
		var host = document.getElementById("nlurd-3dhost");
		if (!host || !GLB) { return; }
		var build = function () {
			var mv = document.createElement("model-viewer");
			mv.setAttribute("src", GLB);
			mv.setAttribute("camera-controls", ""); mv.setAttribute("interaction-prompt", "none");
			mv.setAttribute("environment-image", "neutral"); mv.setAttribute("exposure", "0.95");
			mv.setAttribute("shadow-intensity", "0.5"); mv.setAttribute("touch-action", "pan-y");
			if (MODE === "demo") { mv.setAttribute("auto-rotate", ""); mv.setAttribute("rotation-per-second", "8deg"); }
			var fls = S.floors || 4;
			mv.setAttribute("camera-target", "0 " + Math.min(20, fls * FH * 0.45).toFixed(1) + " 0");
			mv.setAttribute("camera-orbit", "-28deg 76deg " + Math.max(40, fls * FH * 1.6).toFixed(0) + "m");
			mv.setAttribute("min-camera-orbit", "auto 48deg 26m");
			mv.setAttribute("max-camera-orbit", "auto 86deg 90m");
			(S.apartments || []).forEach(function (a) {
				var b = document.createElement("button");
				b.setAttribute("slot", "hotspot-" + a.id);
				b.setAttribute("data-position", aptPos(a));
				var v = DIRV[a.dir] || [-1, 0];
				b.setAttribute("data-normal", v[0] + " 0 " + v[1]);
				b.setAttribute("data-visibility-attribute", "visible");
				b.className = "nlur-apt";
				b.style.background = (S.statuses[a.consent_status] || S.statuses.unreached)[1];
				b.textContent = a.floor; b.title = a.label;
				b.addEventListener("click", function () { selectApt(a.id); });
				mv.appendChild(b);
			});
			var hint = host.querySelector(".nlurd-3dhint");
			host.insertBefore(mv, host.firstChild);
			mv.addEventListener("load", function () { if (hint) { hint.classList.add("is-off"); } });
		};
		if (window.customElements && customElements.get("model-viewer")) { build(); return; }
		var s = document.createElement("script"); s.type = "module";
		s.src = "https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";
		s.onload = build; document.head.appendChild(s);
	}

	/* ---------- apartment panel ---------- */
	function selectApt(id) {
		selApt = (S.apartments || []).filter(function (a) { return a.id === id; })[0];
		if (!selApt) { return; }
		var box = document.getElementById("nlurd-apt");
		var done = 0, total = 0, rows = "";
		Object.keys(S.doc_keys).forEach(function (k) {
			total++;
			var on = selApt.docs && selApt.docs[k];
			if (on) { done++; }
			rows += '<label class="nlurd-docrow"><input type="checkbox" data-doc="' + k + '"' + (on ? " checked" : "") + (S.can_manage ? "" : " disabled") + "> " + esc(S.doc_keys[k]) + "</label>";
		});
		var pctd = total ? Math.round(done / total * 100) : 0;
		var h = "<h4>" + esc(selApt.label) + " · " + esc(t("floor")) + " " + selApt.floor + "</h4>";
		if (S.can_manage) {
			h += '<select id="nlurd-aptstatus">';
			Object.keys(S.statuses).forEach(function (k) { h += '<option value="' + k + '"' + (k === selApt.consent_status ? " selected" : "") + ">" + esc(S.statuses[k][0]) + "</option>"; });
			h += "</select>";
		} else {
			h += "<p><b>" + esc((S.statuses[selApt.consent_status] || [])[0] || "") + "</b></p>";
		}
		if (selApt.note) { h += '<p class="nlurd-note">' + esc(selApt.note) + "</p>"; }
		h += '<div class="nlurd-meter"><i style="width:' + pctd + '%"></i></div><p class="nlurd-note">' + esc(t("docs_of")) + ": " + done + "/" + total + "</p>" + rows;
		if (S.can_manage) { h += '<button class="nlurd-btn" id="nlurd-aptsave">' + esc(t("save")) + "</button>"; }
		box.innerHTML = h;
		box.scrollIntoView({ behavior: "smooth", block: "nearest" });
		pingMap();
		var save = document.getElementById("nlurd-aptsave");
		if (save) {
			save.addEventListener("click", function () {
				selApt.consent_status = document.getElementById("nlurd-aptstatus").value;
				selApt.docs = selApt.docs || {};
				box.querySelectorAll("[data-doc]").forEach(function (cb) { selApt.docs[cb.dataset.doc] = cb.checked; });
				api("/renewal-space/" + S.id + "/apartments" + QS, { method: "POST", body: JSON.stringify({ apartments: S.apartments }) })
					.then(function (d) { S = d; render(); });
			});
		}
	}

	/* ---------- wiring ---------- */
	function wire() {
		document.querySelectorAll(".nlurd-step").forEach(function (el) {
			el.addEventListener("click", function () {
				document.querySelectorAll(".nlurd-step").forEach(function (x) { x.classList.toggle("is-open", x === el); });
				stepCard(parseInt(el.dataset.st, 10));
			});
		});
		var us = document.getElementById("nlurd-upsend");
		if (us) {
			us.addEventListener("click", function () {
				var txt = document.getElementById("nlurd-uptext").value;
				if (!txt) { return; }
				api("/renewal-space/" + S.id + "/update" + QS, { method: "POST", body: JSON.stringify({ text: txt }) }).then(function (d) { S = d; render(); });
			});
		}
		var inv = document.getElementById("nlurd-invbtn");
		if (inv) {
			inv.addEventListener("click", function () {
				api("/renewal-space/" + S.id + "/invite", { method: "POST" }).then(function (d) {
					var i = document.getElementById("nlurd-invurl");
					i.hidden = false; i.value = d.join_url; i.select();
					try { navigator.clipboard.writeText(d.join_url); } catch (e) { /* clipboard optional */ }
				});
			});
		}
	}

	load();
})();
