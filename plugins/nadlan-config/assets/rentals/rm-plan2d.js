/* ============================================================================
   NADLAN RENTALS v2 - the flat services drawing of an apartment (slice 1, HAD-795)
   N.plan2d.draw(el, data, opts) draws rooms as ink rectangles on a 12 px grid,
   the parts of the home (a line icon in a 44 px button) and the service runs
   (cold water blue, hot water red dashed, gas yellow, electricity violet), in the
   look of the Plan board. No plan: one row of the parts' icons with their states
   and a link to add a plan. Every visible word comes from the string table (t2_*).
   data = { rooms:[{id,kind,x,y,w,h,label}], parts:[{id,kind,label,room,layers,state,x,y}],
            runs:[{layer,pts:[[x,y],...],dashed}], size:342, addPlanUrl }
   opts = { scale (1), lit (part id), layer ('all'|'w'|'e'|'g'|'ac'), interactive (true), onPick(id) }
   One file, no framework, no 3D, about 9 KB.
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM = window.NLRM || {};
	var SIZE = 342, INK = "#14212b", INK2 = "#3b4753";
	var COLOR = { w: "#1565c0", h: "#c62828", g: "#f5b800", e: "#6a3fc8" };

	/* the line icons (24 x 24, stroke 1.7) of the Plan board, plus two more in the same hand */
	var IC = {
		ac: '<rect x="3" y="6" width="18" height="8" rx="2"/><path d="M6 11h12M8 17v2M12 17v2M16 17v2"/>',
		shutter: '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M4 8h16M4 12h16M4 16h16"/>',
		cooktop: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2.2"/><circle cx="15.5" cy="10" r="2.2"/><path d="M7 16h10"/>',
		fridge: '<rect x="6" y="2.5" width="12" height="19" rx="2"/><path d="M6 9.5h12M9 6v1.5M9 12.5v3"/>',
		tap: '<path d="M5 20h14M8 20v-9a4 4 0 0 1 8 0v1M16 12h3M12 4v3"/>',
		panel: '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8v4M12 8v4M16 8v4M8 16h8"/>',
		boiler: '<rect x="5" y="3.5" width="14" height="6" rx="3"/><path d="M6 12.5h12l2.5 8h-17zM12 12.5v8M8 9.5v3M16 9.5v3"/>',
		washer: '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="13" r="4"/><path d="M7 6.5h2"/>',
		heater: '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 9v6M11 9v6M15 9v6M19 9v6"/>',
		gas: '<path d="M12 3c1 3 4 5 4 9a4 4 0 0 1-8 0c0-2 1-3 2-4 0 2 1 2 1 2 1-2 1-4 1-7z"/>'
	};
	var KIND_ICON = { boiler: "boiler", ac: "ac", panel: "panel", water_meter: "tap", gas: "gas", fridge: "fridge", oven: "cooktop", washer: "washer", dishwasher: "washer", heater: "heater", shutter: "shutter" };
	var KIND_LAYERS = { boiler: ["w", "e"], ac: ["e", "ac"], panel: ["e"], water_meter: ["w"], gas: ["g"], fridge: ["e"], oven: ["g", "e"], washer: ["w", "e"], dishwasher: ["w", "e"], heater: ["e"], shutter: ["e"] };
	/* where a part lives when the plan does not say: the first room of these kinds */
	var KIND_ROOMS = { boiler: ["balcony", "bath", "laundry"], ac: ["living", "bedroom"], panel: ["hall", "living"], water_meter: ["kitchen", "bath"], gas: ["kitchen"], fridge: ["kitchen"], oven: ["kitchen"], washer: ["laundry", "bath", "balcony"], dishwasher: ["kitchen"], heater: ["bedroom", "living"], shutter: ["living", "bedroom"] };
	N.plan2d = N.plan2d || {};
	N.plan2d.KIND_LAYERS = KIND_LAYERS;
	N.plan2d.KIND_ICON = KIND_ICON;

	/* every home part is a picture, the same family as the apartment card in the opening of /my-rentals/ (HAD-795, 21.11.2026):
	   one studio picture per kind, assets/rentals/portfolio/img/p-<kind>-192.webp. The drawn glyph is only the stand-in for a kind
	   that has no picture. */
	var SELF = (document.currentScript && document.currentScript.src) || "";
	var PIC = { boiler: 1, ac: 1, panel: 1, water_meter: 1, gas: 1, fridge: 1, oven: 1, washer: 1, dishwasher: 1, heater: 1, shutter: 1 };
	function picUrl(kind) {
		var c = (N.state && N.state.cfg) || {}, base = c.assets || SELF.replace(/[^\/]*(\?.*)?$/, ""), v = c.ver || "";
		return base + "portfolio/img/p-" + kind + "-192.webp" + (v ? "?v=" + encodeURIComponent(v) : "");
	}
	N.plan2d.pic = picUrl;
	function icon(kind, size) {
		if (PIC[kind]) { return '<img class="np2-pic" src="' + esc(picUrl(kind)) + '" alt="" width="' + (size || 24) + '" height="' + (size || 24) + '" decoding="async">'; }
		return '<svg aria-hidden="true" width="' + (size || 24) + '" height="' + (size || 24) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + (IC[KIND_ICON[kind] || "panel"]) + "</svg>";
	}
	N.plan2d.icon = icon;
	var esc = function (s) { return N.esc ? N.esc(s) : String(s); };
	var tt = function (k, v) { return N.t(k, v); };

	function badge(state) {
		if (state === "fault") { return '<span aria-hidden="true" class="np2-bd np2-bd--fault">!</span>'; }
		if (state === "soon") { return '<span aria-hidden="true" class="np2-bd np2-bd--soon"><svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="#14212b" stroke-width="1.6" stroke-linecap="round"><path d="M5 2.2V5l1.8 1.2"/></svg></span>'; }
		return '<span aria-hidden="true" class="np2-bd np2-bd--ok"></span>';
	}
	function partBtn(p, o, style) {
		var lit = o.lit === p.id, st = p.state || "ok";
		var inLayer = o.layer === "all" || !o.layer || (p.layers || []).indexOf(o.layer) >= 0 || lit;
		var cls = "np2-part np2-part--" + st + (lit ? " is-lit" : "") + (inLayer ? "" : " is-dim");
		var aria = esc(p.label) + ", " + esc(tt("t2_ps_" + st));
		var inner = icon(p.kind) + badge(st);
		if (o.interactive === false) { return '<span class="' + cls + '" aria-hidden="true" style="' + style + '">' + inner + "</span>"; }
		return '<button type="button" class="' + cls + '" data-part="' + esc(p.id) + '" aria-label="' + aria + '" style="' + style + '">' + inner + "</button>";
	}
	function tag(p, o, x, y) {
		var st = p.state || "ok", lit = o.lit === p.id;
		if (st === "ok" && !lit) { return ""; }
		var left = Math.max(0, Math.min(SIZE - 84, x - 42));
		return '<span aria-hidden="true" class="np2-tag np2-tag--' + (lit ? "lit" : st) + '" style="left:' + left + "px;top:" + (y + 25) + 'px">' + esc(p.label) + "</span>";
	}

	/* parts with no position get one inside their room, in a small grid */
	N.plan2d.place = function (parts, rooms) {
		var used = {}, byKind = function (kinds) { for (var i = 0; i < kinds.length; i++) { var r = rooms.find(function (x) { return x.kind === kinds[i]; }); if (r) { return r; } } return null; };
		return parts.map(function (p) {
			if (isFinite(p.x) && isFinite(p.y) && p.x != null && p.y != null) { return p; }
			var r = (p.room != null && rooms.find(function (x) { return String(x.id) === String(p.room); })) || byKind(KIND_ROOMS[p.kind] || []) || rooms[0];
			if (!r) { return Object.assign({}, p, { x: 30, y: 30 }); }
			var n = used[r.id] = (used[r.id] || 0) + 1 - 1, cols = Math.max(1, Math.floor((r.w - 4) / 48));
			used[r.id] = n + 1;
			var cx = r.x + 28 + (n % cols) * 48, cy = r.y + 28 + Math.floor(n / cols) * 48;
			cx = Math.min(cx, r.x + r.w - 26); cy = Math.min(cy, r.y + r.h - 26);
			return Object.assign({}, p, { x: Math.max(26, Math.min(SIZE - 26, cx)), y: Math.max(26, Math.min(SIZE - 26, cy)) });
		});
	};
	/* orthogonal runs: one horizontal trunk per layer, one vertical drop to every part of it */
	N.plan2d.runs = function (parts) {
		var out = [];
		["w", "e", "g"].forEach(function (L) {
			var ps = parts.filter(function (p) { return (p.layers || []).indexOf(L) >= 0; });
			if (ps.length < 2) { return; }
			var ys = ps.map(function (p) { return p.y; }).sort(function (a, b) { return a - b; }), ty = Math.round(ys[Math.floor(ys.length / 2)]);
			var xs = ps.map(function (p) { return p.x; }), x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
			out.push({ layer: L, pts: [[x0, ty], [x1, ty]] });
			ps.forEach(function (p) { if (Math.abs(p.y - ty) > 1) { out.push({ layer: L, pts: [[p.x, ty], [p.x, p.y]] }); } });
			if (L === "w") {
				var b = ps.find(function (p) { return p.kind === "boiler"; });
				if (b) { var hy = ty + 6; out.push({ layer: "h", pts: [[x0, hy], [x1, hy]], dashed: true }); if (Math.abs(b.y - hy) > 1) { out.push({ layer: "h", pts: [[b.x + 6, hy], [b.x + 6, b.y]], dashed: true }); } }
			}
		});
		return out;
	};
	function seg(a, b, color, dashed, op) {
		var x = Math.min(a[0], b[0]), y = Math.min(a[1], b[1]), w = Math.abs(a[0] - b[0]), h = Math.abs(a[1] - b[1]);
		if (dashed) { return '<i class="np2-run" style="left:' + x + "px;top:" + y + "px;width:" + (w || 0) + "px;height:" + (h || 0) + "px;" + (w ? "border-top" : "border-left") + ":3px dashed " + color + ";opacity:" + op + '"></i>'; }
		return '<i class="np2-run" style="left:' + x + "px;top:" + y + "px;width:" + (w || 3) + "px;height:" + (h || 3) + "px;background:" + color + ";opacity:" + op + '"></i>';
	}

	N.plan2d.draw = function (el, data, opts) {
		var o = Object.assign({ scale: 1, lit: null, layer: "all", interactive: true }, opts || {});
		data = data || {};
		var rooms = data.rooms || [], parts = data.parts || [], html;
		if (!rooms.length) { html = fallback(parts, data, o); el.innerHTML = html; wire(el, o); return; }
		var P = N.plan2d.place(parts, rooms), runs = data.runs || N.plan2d.runs(P);
		var g = '<div class="np2-sheet" dir="ltr" style="width:' + SIZE + "px;height:" + SIZE + "px;transform:scale(" + o.scale + ')">';
		rooms.forEach(function (r) {
			g += '<i class="np2-room' + (r.kind === "mamad" ? " np2-room--heavy" : "") + '" aria-hidden="true" style="left:' + r.x + "px;top:" + r.y + "px;width:" + r.w + "px;height:" + r.h + 'px"></i>';
		});
		runs.forEach(function (s) {
			var on = o.layer === "all" || !o.layer ? 0.55 : ((s.layer === o.layer || (s.layer === "h" && o.layer === "w")) ? 1 : 0.06);
			for (var i = 0; i < s.pts.length - 1; i++) { g += seg(s.pts[i], s.pts[i + 1], COLOR[s.layer] || INK, s.dashed, on); }
		});
		/* a room's name sits at the bottom centre; when a tile (or its state tag) would cover it, it moves to the room's free corner */
		var hit = [];
		P.forEach(function (p) { hit.push([p.x - 22, p.y - 22, p.x + 22, p.y + 22]); if ((p.state || "ok") !== "ok" || o.lit === p.id) { hit.push([Math.max(0, Math.min(SIZE - 84, p.x - 42)), p.y + 3, Math.max(0, Math.min(SIZE - 84, p.x - 42)) + 84, p.y + 20]); } });
		var free = function (x, y, w) { return !hit.some(function (q) { return x < q[2] && x + w > q[0] && y < q[3] && y + 18 > q[1]; }); };
		rooms.forEach(function (r) {
			if (!r.label) { return; }
			var w = Math.min(r.w - 6, Math.round(String(r.label).length * 7 + 8)), y1 = r.y + r.h - 22, y0 = r.y + 4;
			var c = [[r.x + (r.w - w) / 2, y1, "center"], [r.x + 3, y1, "left"], [r.x + r.w - w - 3, y1, "right"], [r.x + 3, y0, "left"], [r.x + r.w - w - 3, y0, "right"]];
			var pick = c.find(function (q) { return free(q[0], q[1], w); }) || c[0];
			g += '<span class="np2-rl' + (r.kind === "mamad" ? " np2-rl--heavy" : "") + '" aria-hidden="true" style="left:' + Math.round(pick[0]) + "px;top:" + Math.round(pick[1]) + "px;width:" + w + "px;text-align:" + pick[2] + '">' + esc(r.label) + "</span>";
		});
		var tags = "";
		P.forEach(function (p) {
			g += partBtn(p, o, "left:" + (p.x - 22) + "px;top:" + (p.y - 22) + "px");
			tags += tag(p, o, p.x, p.y - 22);
		});
		g += tags + "</div>";
		el.innerHTML = '<div class="np2 np2--plan" style="width:' + Math.round(SIZE * o.scale) + "px;height:" + Math.round(SIZE * o.scale) + 'px">' + g + "</div>";
		wire(el, o);
	};
	/* no plan: the parts' icons in one row, their states, and a link to add a plan (never a made-up floor) */
	function fallback(parts, data, o) {
		var max = +o.max || 0, shown = parts, more = 0, first = !parts.length ? (data.addKinds || []) : [];
		if (max && parts.length > max - 1) {
			shown = parts.slice().sort(function (a, b) { return (a.state === "fault" ? 0 : 1) - (b.state === "fault" ? 0 : 1); }).slice(0, max - 1);
			more = parts.length - shown.length;
		}
		var h = '<div class="np2 np2--row">';
		if (first.length) { h += '<p class="np2-hint">' + esc(tt("t2_first_part")) + "</p>"; }
		else if (!parts.length) { h += '<p class="np2-none">' + esc(tt("t2_no_parts")) + "</p>"; }
		h += '<ul class="np2-list" dir="' + (N.rtl ? "rtl" : "ltr") + '">';
		shown.forEach(function (p) {
			var st = p.state || "ok";
			h += '<li>' + partBtn(p, Object.assign({}, o, { layer: "all" }), "position:relative") + '<span class="np2-cap np2-cap--' + st + '">' + esc(p.label) + "</span></li>";
		});
		/* nothing recorded yet: the common parts, one press adds one */
		first.slice(0, max || first.length).forEach(function (k) {
			h += '<li class="np2-new"><button type="button" class="np2-part np2-part--new" data-act="add-kind" data-kind="' + esc(k) + '" aria-label="' + esc(tt("t2_add_aria", { name: tt("ak_" + k) })) + '" style="position:relative">' + icon(k) + '<span aria-hidden="true" class="np2-bd np2-bd--add">+</span></button><span class="np2-cap">' + esc(tt("t2_k_" + k)) + "</span></li>";
		});
		if (more) { h += '<li><button type="button" class="np2-part np2-part--more" data-act="drawing" aria-label="' + esc(tt("t2_more_parts", { n: more })) + '" style="position:relative">+' + more + '</button><span class="np2-cap">' + esc(tt("t2_more_cap")) + "</span></li>"; }
		else if (parts.length && data.addKinds) { h += '<li><button type="button" class="np2-part np2-part--new" data-act="add-part" aria-label="' + esc(tt("t2_add_title")) + '" style="position:relative"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><path d="M10 4v12M4 10h12"/></svg></button><span class="np2-cap">' + esc(tt("t2_add_cap")) + "</span></li>"; }
		h += "</ul>";
		h += '<a class="np2-add" href="' + esc(data.addPlanUrl || "/tour/designer/") + '">' + esc(tt("t2_add_plan")) + "</a></div>";
		return h;
	}
	function wire(el, o) {
		if (o.interactive === false || !o.onPick) { return; }
		el.querySelectorAll("[data-part]").forEach(function (b) { b.addEventListener("click", function (e) { e.stopPropagation(); o.onPick(b.getAttribute("data-part")); }); });
	}
})();
