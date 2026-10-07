/* ============================================================================
   NADLAN RENTALS v2 - the app shell and its screens (HAD-383, 1.10.2026)
   Today · Properties (map, the building in 3D, floors) · People (tenants,
   prospects, guarantors, professionals) · Money · Repairs · Documents ·
   Leasing · Reports · Settings. Every apartment, tenant and repair opens
   its full card (rm-drawers.js) in one tap.
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM, t = N.t, esc = N.esc, I = N.icon;
	var S = N.state = { route: "today", param: null, seg: "tenant", month: N.ym(0), mtab: "ledger", dfilter: "all", cfg: {} };
	var root = null;

	var NAV = [
		{ id: "today", icon: "today" }, { id: "properties", icon: "building" }, { id: "people", icon: "people" },
		{ id: "money", icon: "money" }, { id: "repairs", icon: "wrench" },
		{ id: "leasing", icon: "key", extra: true }, { id: "docs", icon: "doc", extra: true },
		{ id: "reports", icon: "chart", extra: true }, { id: "settings", icon: "gear", extra: true }, { id: "help", icon: "help", extra: true }
	];

	/* ---------- mount ---------- */
	N.mount = function (el, cfg) {
		root = el;
		S.cfg = cfg || {};
		N.STR = cfg.strings || {};
		N.MSG = cfg.msg || {};
		var lang = cfg.lang || "he";
		try { var saved = localStorage.getItem("nlrm_lang"); if (cfg.inPlaceLang && saved && N.STR[saved]) { lang = saved; } } catch (e) { /* private mode */ }
		N.setStrings(lang, N.STR[lang] || N.STR.he);
		N.store.adapter = cfg.adapter;
		root.classList.add("nlrm-app");
		root.setAttribute("dir", N.rtl ? "rtl" : "ltr");
		root.setAttribute("lang", N.lang);
		root.innerHTML = '<p class="nlrm-empty">' + esc(t("loading")) + "</p>";
		N.store.on(function () { render(); N.ui.refresh(); });
		N.store.load().catch(function (e) { root.innerHTML = '<p class="nlrm-empty">' + esc(t("load_fail")) + (e && e.message ? " · " + esc(e.message) : "") + "</p>"; });
		window.addEventListener("hashchange", function () { readRoute(); render(); });
		readRoute();
		root.addEventListener("click", onClick);
		document.addEventListener("click", function (e) { var r = root.querySelector(".nlrm-results"); if (r && !e.target.closest(".nlrm-search")) { r.remove(); } });
	};
	N.relang = function (lang) {
		if (!N.STR[lang]) { return; }
		if (S.cfg.langUrls && S.cfg.langUrls[lang] && !S.cfg.inPlaceLang) { location.href = S.cfg.langUrls[lang] + location.hash; return; }
		N.setStrings(lang, N.STR[lang]);
		try { localStorage.setItem("nlrm_lang", lang); } catch (e) { /* private mode */ }
		root.setAttribute("dir", N.rtl ? "rtl" : "ltr");
		root.setAttribute("lang", lang);
		N.ui.close(true);
		if (N.store.adapter && N.store.adapter.demo) { N.store.adapter = N.DemoAdapter(lang); N.store.load(); return; }
		render();
		if (S.cfg.onLang) { S.cfg.onLang(lang); }
	};
	function readRoute() {
		var h = (location.hash || "").replace(/^#\/?/, "");
		if (/^[tqasv]=/.test(h)) { return; }
		var p = h.split("/");
		S.route = NAV.some(function (n) { return n.id === p[0]; }) || p[0] === "property" ? p[0] : "today";
		S.param = p[1] || null;
	}
	N.go = function (route, param) { location.hash = "#/" + route + (param ? "/" + param : ""); };

	/* ---------- the frame ---------- */
	function render() {
		if (!N.store.d || !N.ix.unit) { return; }
		var att = N.attention(), urgent = att.filter(function (a) { return a.s <= 1; }).length;
		var openRep = N.store.d.tickets.filter(function (x) { return x.urgency === "urgent" && x.status !== "done" && x.status !== "cancelled"; }).length;
		var applicants = N.store.d.contacts.filter(function (c) { return c.kind === "prospect" && c.stage === "applied"; }).length;
		var badge = { today: urgent, repairs: openRep, leasing: applicants };
		var k = N.kpis();
		var h = '<header class="nlrm-top">' +
			'<div class="nlrm-brand"><b>' + esc(t("app_title")) + "</b>" + (k.props ? "<small>" + esc(t("app_sub", { props: k.props, units: k.units })) + "</small>" : "") + "</div>" +
			'<div class="nlrm-search"><input type="search" id="nlrm-q" placeholder="' + esc(t("search_ph")) + '" aria-label="' + esc(t("search_ph")) + '" autocomplete="off">' + I("search", 18) + "</div>" +
			'<div class="nlrm-lang" role="group" aria-label="' + esc(t("language")) + '">' + Object.keys(N.STR).filter(function (l) { return ["he", "en", "fr", "ru", "ar"].indexOf(l) >= 0; }).map(function (l) {
				return '<button type="button" data-lang="' + l + '" aria-current="' + (l === N.lang ? "true" : "false") + '" lang="' + l + '">' + esc(N.STR[l].lang_name || l) + "</button>";
			}).join("") + "</div>" +
			'<button type="button" class="nlrm-btn nlrm-btn--primary" data-act="new">' + I("plus", 18) + esc(t("add")) + "</button></header>";
		if (N.store.d.demo) { h += '<div class="nlrm-demo-flag">' + I("eye", 18) + "<span><b>" + esc(t("demo_flag")) + "</b> " + esc(t("demo_flag_sub")) + "</span>" + (S.cfg.adapterReal ? ' <button type="button" class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" data-act="my-data">' + esc(t("ob_back")) + "</button>" : "") + "</div>"; }
		if (N.store.d.key_ok === false) { h += '<div class="nlrm-demo-flag" style="background:var(--bad-g);color:var(--bad)">' + esc(t("key_bad")) + "</div>"; }
		h += '<div class="nlrm-shell"><nav class="nlrm-nav" aria-label="' + esc(t("nav_label")) + '">';
		NAV.forEach(function (n) {
			var cur = S.route === n.id || (S.route === "property" && n.id === "properties");
			h += '<button type="button" data-go="' + n.id + '"' + (cur ? ' aria-current="page"' : "") + (n.extra ? ' class="is-extra"' : "") + ">" + I(n.icon, 20) + "<span>" + esc(t("nav_" + n.id)) + "</span>" + (badge[n.id] ? '<i class="nlrm-badge">' + badge[n.id] + "</i>" : "") + "</button>";
		});
		h += '<button type="button" class="nlrm-nav-more" data-act="more">' + I("menu", 20) + "<span>" + esc(t("nav_more")) + "</span></button>";
		h += '</nav><main class="nlrm-main" id="nlrm-main">' + screen(att, k) + "</main></div>";
		var q = root.querySelector("#nlrm-q"), qv = q ? q.value : "", qf = document.activeElement === q;
		root.innerHTML = h;
		if (qf) { var nq = root.querySelector("#nlrm-q"); nq.value = qv; nq.focus(); }
		wireScreen();
	}
	function screen(att, k) {
		switch (S.route) {
			case "properties": return vProperties();
			case "property": return vProperty(+S.param);
			case "people": return vPeople();
			case "money": return vMoney();
			case "repairs": return vRepairs();
			case "docs": return vDocs();
			case "leasing": return vLeasing();
			case "reports": return vReports();
			case "settings": return vSettings();
			case "help": return vHelp();
			default: return vToday(att, k);
		}
	}
	function head(title, sub, tools) {
		return '<div class="nlrm-screen-head"><div><h2>' + esc(title) + "</h2>" + (sub ? "<p>" + sub + "</p>" : "") + "</div>" + (tools ? '<div class="nlrm-tools">' + tools + "</div>" : "") + "</div>";
	}
	function btn(act, label, kind, icon, data) {
		return '<button type="button" class="nlrm-btn nlrm-btn--' + (kind || "secondary") + ' nlrm-btn--sm" data-act="' + act + '"' + (data || "") + ">" + (icon ? I(icon, 18) : "") + esc(label) + "</button>";
	}
	N.btn = btn;
	function chip(status, label) { return '<span class="nlrm-chip is-' + status + '"><i></i>' + esc(label || t("st_" + status)) + "</span>"; }
	N.chip = chip;
	function ava(c) { var n = (c && c.name) || "?"; return '<span class="nlrm-ava is-' + (c ? c.kind : "") + '" aria-hidden="true">' + esc(n.trim().charAt(0)) + "</span>"; }
	N.ava = ava;
	function where(u) { var p = N.ix.prop[u.property_id] || {}; return (u.label || "") + (p.address ? " · " + p.address : ""); }
	N.where = where;

	/* ---------- TODAY ---------- */
	function vToday(att, k) {
		if (!N.store.d.properties.length && !N.store.d.demo) { return onboarding(); }
		var d = N.today();
		var dayLine = d.toLocaleDateString(N.locale(), { weekday: "long", day: "numeric", month: "long", year: "numeric" });
		var pct = k.expected ? Math.min(100, Math.round(100 * k.collected / k.expected)) : 0;
		var h = head(t("nav_today"), esc(dayLine));
		h += '<div class="nlrm-kpis">' +
			'<button type="button" class="nlrm-kpi" data-go="money"><span>' + esc(t("kpi_collected")) + "</span><b>" + N.money(k.collected) + '</b><small>' + t("kpi_of", { total: N.money(k.expected) }) + '</small><div class="nlrm-bar" aria-hidden="true"><i style="width:' + pct + '%"></i></div></button>' +
			'<button type="button" class="nlrm-kpi" data-go="money"><span>' + esc(t("kpi_open")) + "</span><b>" + N.money(k.open) + "</b><small>" + esc(t("kpi_open_sub")) + "</small></button>" +
			'<button type="button" class="nlrm-kpi" data-go="leasing"><span>' + esc(t("kpi_vacant")) + "</span><b>" + N.num(k.vacant) + "</b><small>" + esc(t("kpi_of_units", { n: k.units })) + "</small></button>" +
			'<button type="button" class="nlrm-kpi" data-go="repairs"><span>' + esc(t("kpi_repairs")) + "</span><b>" + N.num(k.repairs) + "</b><small>" + esc(t("kpi_repairs_sub")) + "</small></button></div>";
		h += '<div class="nlrm-grid2"><section class="nlrm-card" aria-labelledby="nlrm-att-h"><h3 id="nlrm-att-h">' + esc(t("att_title")) + (att.length ? ' <span class="nlrm-chip">' + att.length + "</span>" : "") + "</h3>";
		if (!att.length) { h += '<p class="nlrm-empty">' + esc(t("att_none")) + "</p>"; }
		else {
			h += '<ul class="nlrm-list">' + att.slice(0, S.attAll ? 60 : 8).map(attItem).join("") + "</ul>";
			if (att.length > 8 && !S.attAll) { h += btn("att-all", t("show_all", { n: att.length }), "quiet"); }
		}
		h += '<p class="nlrm-note">' + esc(t("att_note")) + "</p></section>";
		h += '<section class="nlrm-card" aria-labelledby="nlrm-month-h"><h3 id="nlrm-month-h">' + esc(t("month_units", { month: N.monthName(N.ym(0)) })) + '</h3><ul class="nlrm-list">';
		N.store.d.units.slice().sort(function (a, b) { var o = { late: 0, due: 1, ok: 2, vacant: 3 }; return o[N.unitStatus(a)] - o[N.unitStatus(b)]; }).forEach(function (u) {
			var l = N.ix.leaseByUnit[u.id], ten = l ? N.tenantsOf(l)[0] : null, st = N.unitStatus(u);
			h += '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main" data-open="unit:' + u.id + '"><b>' + esc(where(u)) + "</b><small>" + (ten ? esc(ten.name) + " · " + N.money(l.rent) : esc(t("vacant_since_hint"))) + "</small></button>" + chip(st) + "</li>";
		});
		h += "</ul></section></div>";
		h += '<section class="nlrm-card"><h3>' + I("wa", 20) + esc(t("quick_title")) + '</h3><p class="nlrm-lead">' + esc(t("quick_lead")) + '</p><div class="nlrm-tools">' + btn("quick-link", t("quick_btn"), "wa", "wa") + btn("go-settings", t("quick_settings"), "quiet") + "</div></section>";
		return h;
	}
	/* a new landlord: three steps, the Excel shortcut, and the sample to look around first */
	function onboarding() {
		var h = '<section class="nlrm-card" style="padding:28px"><h2 style="font-size:28px;margin-bottom:8px">' + esc(t("ob_title")) + '</h2><p class="nlrm-lead">' + esc(t("ob_lead")) + "</p>";
		h += '<ol class="nlrm-list">' + ["ob_s1", "ob_s2", "ob_s3"].map(function (k, i) { return '<li class="nlrm-item"><span class="nlrm-ava" aria-hidden="true">' + (i + 1) + '</span><div class="nlrm-item-main"><b>' + esc(t(k)) + "</b><small>" + esc(t(k + "_sub")) + "</small></div></li>"; }).join("") + "</ol>";
		h += '<div class="nlrm-tools" style="margin-top:14px">' + btn("new-property", t("new_property"), "primary", "plus") + btn("import", t("imp_title"), "secondary", "upload") + btn("sample", t("ob_sample"), "quiet", "eye") + "</div></section>";
		return h;
	}
	function attItem(a) {
		var acts = "", open = a.ticket ? "ticket:" + a.ticket.id : a.kind === "applicant" ? "contact:" + a.contact.id : a.unit && a.unit.id ? "unit:" + a.unit.id : a.contact ? "contact:" + a.contact.id : "";
		var cid = a.contact ? a.contact.id : 0, lid = a.lease ? a.lease.id : 0;
		if (a.kind === "late" || a.kind === "due") { acts = btn("wa-remind", t("act_remind"), "wa", "wa", ' data-lease="' + lid + '"') + btn("pay", t("act_paid"), "secondary", "check", ' data-lease="' + lid + '"'); }
		else if (a.kind === "ending" || a.kind === "option" || a.kind === "ended") { acts = btn("wa-renew", t("act_renew"), "wa", "wa", ' data-lease="' + lid + '"') + btn("open", t("act_open"), "quiet", "", ' data-open="unit:' + a.unit.id + '"'); }
		else if (a.kind === "cheque") { acts = btn("cheque-dep", t("act_deposited"), "secondary", "check", ' data-row="' + a.row.id + '"'); }
		else if (a.kind === "confirm") { acts = btn("confirm-pay", t("act_confirm"), "secondary", "check", ' data-row="' + a.row.id + '"'); }
		else if (a.kind === "vacant") { acts = btn("apply-link", t("act_apply_link"), "wa", "wa", ' data-unit="' + a.unit.id + '"') + btn("publish", t("act_publish"), "quiet", "", ' data-unit="' + a.unit.id + '"'); }
		else if (a.kind === "unsigned") { acts = btn("sign-link", t("act_sign_resend"), "wa", "wa", ' data-lease="' + lid + '"'); }
		else if (a.kind === "tax") { acts = btn("go-tax", t("act_tax"), "secondary"); }
		else if (open) { acts = btn("open", t("act_open"), "secondary", "", ' data-open="' + open + '"'); }
		return '<li class="nlrm-item"><span class="nlrm-dot s' + a.s + '" aria-hidden="true"></span><button type="button" class="nlrm-link nlrm-item-main" ' + (open ? 'data-open="' + open + '"' : 'data-act="go-tax"') + "><b>" + esc(a.text) + "</b>" + (a.contact && a.kind !== "applicant" ? "<small>" + esc(a.contact.name) + "</small>" : "") + '</button><div class="nlrm-item-acts">' + acts + "</div></li>";
	}

	/* ---------- PROPERTIES ---------- */
	function vProperties() {
		var d = N.store.d;
		var h = head(t("nav_properties"), esc(t("props_sub")), btn("new-property", t("new_property"), "primary", "plus") + btn("import", t("imp_title"), "secondary", "upload"));
		h += S.cfg.mapbox ? '<div class="nlrm-map" id="nlrm-map" aria-label="' + esc(t("map_label")) + '"></div>' : "";
		if (!d.properties.length) { return h + '<div class="nlrm-card nlrm-empty"><p>' + esc(t("props_none")) + "</p>" + btn("new-property", t("new_property"), "primary", "plus") + "</div>"; }
		h += '<div class="nlrm-props">';
		d.properties.forEach(function (p) {
			var us = N.ix.unitsByProp[p.id] || [], rent = 0, alerts = 0;
			us.forEach(function (u) { var l = N.ix.leaseByUnit[u.id]; if (l) { rent += l.rent; } var s = N.unitStatus(u); if (s === "late") { alerts++; } });
			h += '<button type="button" class="nlrm-prop" data-go-prop="' + p.id + '"><h3>' + esc(p.address) + '</h3><span class="nlrm-note" style="margin:0">' + esc(p.city) + " · " + esc(t("floors_n", { n: p.floors })) + "</span>" +
				'<span class="nlrm-mini" aria-hidden="true">' + us.map(function (u) { var s = N.unitStatus(u); return '<i style="background:' + N.STATUS_COLOR[s] + '"></i>'; }).join("") + "</span>" +
				"<span>" + esc(t("units_n", { n: us.length })) + " · " + N.money(rent) + " " + esc(t("per_month")) + "</span>" + (alerts ? chip("late", t("late_n", { n: alerts })) : chip("ok", t("all_on_track"))) + "</button>";
		});
		h += "</div>";
		return h;
	}
	function vProperty(id) {
		var p = N.ix.prop[id];
		if (!p) { return vProperties(); }
		var us = N.ix.unitsByProp[p.id] || [], m = p.meta || {};
		var facts = [m.year_built ? t("built_in", { y: m.year_built }) : "", t("floors_n", { n: p.floors }), m.elevator ? t("has_elevator") : "", m.parking ? t("has_parking") : "", m.shelter === "mamad" ? t("has_mamad") : (m.shelter ? t("has_shelter") : "")].filter(Boolean);
		var h = '<p style="margin:0 0 6px">' + btn("go-properties", t("back_props"), "quiet", "arrow") + "</p>";
		h += head(p.address + ", " + p.city, esc(facts.join(" · ")), btn("new-unit", t("new_unit"), "primary", "plus", ' data-prop="' + p.id + '"') + btn("edit-property", t("edit"), "secondary", "", ' data-prop="' + p.id + '"'));
		h += '<div class="nlrm-stage"><div><div class="nlrm-3d" id="nlrm-3d" data-prop="' + p.id + '"><div class="nlrm-3d-wait">' + esc(t("loading_3d")) + "</div></div>" +
			'<p class="nlrm-legend">' + ["ok", "due", "late", "vacant"].map(function (s) { return '<span><i style="background:' + N.STATUS_COLOR[s] + '"></i>' + esc(t("st_" + s)) + "</span>"; }).join("") + '<span><i style="background:transparent;border:1px dashed #9a948a"></i>' + esc(t("st_notmine")) + "</span></p></div>";
		h += '<div class="nlrm-card"><h3>' + esc(t("floors_title")) + '</h3><div class="nlrm-stack" role="grid" aria-label="' + esc(t("floors_title")) + '">';
		for (var f = p.floors; f >= 1; f--) {
			h += '<div class="nlrm-floor" role="row"><button type="button" class="nlrm-link nlrm-floor-btn" data-act="floor" data-prop="' + p.id + '" data-floor="' + f + '" aria-label="' + esc(t("floor_open_aria", { n: f })) + '">' + esc(t("floor_n", { n: f })) + '</button><div style="grid-template-columns:repeat(' + p.units_per_floor + ',minmax(0,1fr))">';
			for (var pos = 0; pos < p.units_per_floor; pos++) {
				var u = us.find(function (x) { return x.floor === f && x.pos === pos; });
				if (u) { var s = N.unitStatus(u); h += '<button type="button" role="gridcell" class="nlrm-cell is-mine is-' + s + '" data-open="unit:' + u.id + '" aria-label="' + esc(u.label + ", " + t("st_" + s)) + '">' + esc(u.label) + "</button>"; }
				else { h += '<button type="button" role="gridcell" class="nlrm-cell" data-act="claim" data-prop="' + p.id + '" data-floor="' + f + '" data-pos="' + pos + '" aria-label="' + esc(t("claim_aria", { f: f })) + '">+</button>'; }
			}
			h += "</div></div>";
		}
		h += '</div><p class="nlrm-note">' + esc(t("floors_hint")) + "</p></div></div>";
		h += '<section class="nlrm-card" style="margin-top:14px"><h3>' + esc(t("units_title")) + "</h3>" + unitsTable(us) + "</section>";
		var exp = N.store.d.ledger.filter(function (r) { return r.kind === "expense" && +r.property_id === p.id; }).slice(-8).reverse();
		h += '<div class="nlrm-grid2" style="margin-top:14px"><section class="nlrm-card"><h3>' + esc(t("building_expenses")) + "</h3>" + (exp.length ? '<ul class="nlrm-list">' + exp.map(function (r) { return '<li class="nlrm-item"><div class="nlrm-item-main"><b>' + esc(t("cat_" + r.category)) + (r.note ? " · " + esc(r.note) : "") + "</b><small>" + N.date(r.paid_date) + "</small></div><span class=\"nlrm-amt-out\">" + N.ag(r.amount) + "</span></li>"; }).join("") + "</ul>" : '<p class="nlrm-empty">' + esc(t("none_yet")) + "</p>") + btn("expense", t("new_expense"), "quiet", "plus", ' data-prop="' + p.id + '"') + "</section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("docs_title")) + "</h3>" + N.docList("property", p.id) + btn("upload", t("upload"), "quiet", "upload", ' data-scope="property" data-id="' + p.id + '"') + "</section></div>";
		return h;
	}
	function unitsTable(us) {
		if (!us.length) { return '<p class="nlrm-empty">' + esc(t("units_none")) + "</p>"; }
		return '<table class="nlrm-table"><thead><tr><th>' + esc(t("col_unit")) + "</th><th>" + esc(t("col_tenant")) + '</th><th class="is-num">' + esc(t("col_rent")) + "</th><th>" + esc(t("col_end")) + "</th><th>" + esc(t("col_status")) + "</th></tr></thead><tbody>" +
			us.map(function (u) {
				var l = N.ix.leaseByUnit[u.id], ten = l ? N.tenantsOf(l)[0] : null;
				return '<tr><td data-l="' + esc(t("col_unit")) + '"><button type="button" class="nlrm-link" data-open="unit:' + u.id + '"><b>' + esc(u.label) + "</b></button> <small>" + esc(t("floor_n", { n: u.floor })) + '</small></td><td data-l="' + esc(t("col_tenant")) + '">' + (ten ? '<button type="button" class="nlrm-link" data-open="contact:' + ten.id + '">' + esc(ten.name) + "</button>" : "-") + '</td><td class="is-num" data-l="' + esc(t("col_rent")) + '">' + (l ? N.money(l.rent) : "-") + '</td><td data-l="' + esc(t("col_end")) + '">' + (l && l.end_date ? N.date(l.end_date) : "-") + '</td><td data-l="' + esc(t("col_status")) + '">' + chip(N.unitStatus(u)) + "</td></tr>";
			}).join("") + "</tbody></table>";
	}

	/* ---------- PEOPLE ---------- */
	function vPeople() {
		var segs = ["tenant", "prospect", "guarantor", "vendor", "all"];
		var h = head(t("nav_people"), esc(t("people_sub")), btn("new-contact", t("new_contact"), "primary", "plus", ' data-kind="' + (S.seg === "all" ? "tenant" : S.seg) + '"'));
		h += '<div class="nlrm-seg" role="group">' + segs.map(function (s) { var n = s === "all" ? N.store.d.contacts.length : N.store.d.contacts.filter(function (c) { return c.kind === s; }).length; return '<button type="button" data-seg="' + s + '" aria-pressed="' + (S.seg === s) + '">' + esc(t("seg_" + s)) + " · " + n + "</button>"; }).join("") + "</div>";
		var list = N.store.d.contacts.filter(function (c) { return S.seg === "all" || c.kind === S.seg; });
		if (S.seg === "prospect") { return h + prospectBoard(list); }
		h += '<section class="nlrm-card">';
		if (!list.length) { h += '<p class="nlrm-empty">' + esc(t("people_none")) + "</p>"; }
		else {
			h += '<ul class="nlrm-list">' + list.map(function (c) {
				var l = c.kind === "tenant" ? N.leaseOfContact(c.id) : null, u = l ? N.ix.unit[l.unit_id] : null, bal = l ? N.balance(l) : 0;
				var sub = [t("kind_" + c.kind), u ? where(u) : "", c.lang !== N.lang ? t("speaks", { lang: (N.STR[c.lang] || {}).lang_name || c.lang }) : "", c.tags && c.kind === "vendor" ? t("trade_" + c.tags) : ""].filter(Boolean).join(" · ");
				return '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main nlrm-person" data-open="contact:' + c.id + '">' + ava(c) + "<span><b>" + esc(c.name) + "</b><small>" + esc(sub) + "</small></span></button>" +
					(bal > 0 ? chip(u ? N.unitStatus(u) : "due", t("owes", { amount: N.moneyText(bal) })) : "") +
					'<div class="nlrm-item-acts">' + (c.phone ? '<a class="nlrm-btn nlrm-btn--wa nlrm-btn--sm" data-act="wa-contact" data-id="' + c.id + '" href="' + esc(N.wa(c.phone)) + '" target="_blank" rel="noopener" aria-label="' + esc(t("wa_to", { name: c.name })) + '">' + I("wa", 18) + "</a>" + '<a class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" href="tel:+' + esc(c.phone) + '" aria-label="' + esc(t("call_to", { name: c.name })) + '">' + I("phone", 18) + "</a>" : "") + "</div></li>";
			}).join("") + "</ul>";
		}
		return h + "</section>";
	}
	function prospectBoard(list) {
		var stages = ["new", "contacted", "viewing", "applied", "approved", "signed"];
		var h = '<div class="nlrm-board" style="--cols:3">';
		stages.forEach(function (st) {
			var col = list.filter(function (c) { return (c.stage || "new") === st; });
			h += '<section class="nlrm-col" aria-label="' + esc(t("stage_" + st)) + '"><h4><span>' + esc(t("stage_" + st)) + "</span><span>" + col.length + "</span></h4>";
			col.forEach(function (c) {
				var m = c.meta || {}, u = m.unit_id ? N.ix.unit[m.unit_id] : null;
				h += '<button type="button" class="nlrm-tcard" data-open="contact:' + c.id + '"><b>' + esc(c.name) + "</b><small>" + esc([u ? where(u) : "", m.household || "", m.viewing_at ? t("viewing_at", { when: m.viewing_at.replace(" ", " · ") }) : ""].filter(Boolean).join(" · ")) + "</small></button>";
			});
			h += "</section>";
		});
		return h + "</div>";
	}

	/* ---------- MONEY ---------- */
	function vMoney() {
		var m = S.month, d = N.store.d, inM = function (iso) { return iso && iso.slice(0, 7) === m; };
		var exp = 0, col = 0, due = 0, otherExp = 0;
		d.ledger.forEach(function (r) {
			if (r.kind === "charge" && r.status !== "void" && inM(r.due_date)) { due += r.amount; }
			if (inM(r.paid_date)) { col += N.mx.incomeOf(r); }
			if (r.kind === "expense" && r.status !== "void" && inM(r.paid_date)) { otherExp += r.amount; }
		});
		exp = otherExp;
		var h = head(t("nav_money"), esc(t("money_sub")), btn("pay", t("new_payment"), "primary", "plus") + btn("expense", t("new_expense"), "secondary", "plus") + btn("charge", t("new_charge"), "quiet", "plus"));
		h += '<div class="nlrm-tools" style="justify-content:space-between;margin-bottom:12px"><div class="nlrm-month"><button type="button" class="nlrm-btn nlrm-btn--quiet nlrm-btn--sm" data-act="m-prev" aria-label="' + esc(t("prev_month")) + '">' + (N.rtl ? "›" : "‹") + "</button><b>" + esc(N.monthName(m)) + '</b><button type="button" class="nlrm-btn nlrm-btn--quiet nlrm-btn--sm" data-act="m-next" aria-label="' + esc(t("next_month")) + '">' + (N.rtl ? "‹" : "›") + "</button></div></div>";
		h += '<div class="nlrm-kpis"><div class="nlrm-kpi"><span>' + esc(t("kpi_expected")) + "</span><b>" + N.ag(due) + '</b></div><div class="nlrm-kpi"><span>' + esc(t("kpi_collected_m")) + '</span><b class="nlrm-amt-in">' + N.ag(col) + '</b></div><div class="nlrm-kpi"><span>' + esc(t("kpi_expenses")) + '</span><b class="nlrm-amt-out">' + N.ag(exp) + '</b></div><div class="nlrm-kpi"><span>' + esc(t("kpi_net")) + "</span><b>" + N.ag(col - exp) + "</b></div></div>";
		var tabs = ["ledger", "cheques", "expenses", "pnl", "cpi", "tax"];
		h += '<div class="nlrm-seg" role="group">' + tabs.map(function (x) { return '<button type="button" data-mtab="' + x + '" aria-pressed="' + (S.mtab === x) + '">' + esc(t("mtab_" + x)) + "</button>"; }).join("") + "</div>";
		h += '<section class="nlrm-card">' + ({ ledger: mLedger, cheques: mCheques, expenses: mExpenses, pnl: mPnl, cpi: mCpi, tax: mTax }[S.mtab] || mLedger)(m) + "</section>";
		return h;
	}
	function ledgerRows(rows) {
		if (!rows.length) { return '<p class="nlrm-empty">' + esc(t("none_this_month")) + "</p>"; }
		return '<table class="nlrm-table"><thead><tr><th>' + esc(t("col_date")) + "</th><th>" + esc(t("col_unit")) + "</th><th>" + esc(t("col_what")) + '</th><th class="is-num">' + esc(t("col_amount")) + "</th><th>" + esc(t("col_status")) + "</th><th></th></tr></thead><tbody>" +
			rows.map(function (r) {
				var u = N.ix.unit[r.unit_id], p = N.ix.prop[r.property_id];
				var what = t("kind_" + r.kind) + " · " + t("cat_" + r.category) + (r.method ? " · " + t("m_" + r.method) : "") + (r.ref ? " #" + r.ref : "");
				var stc = { open: "due", paid: "ok", partial: "due", pending: "info", deposited: "ok", bounced: "late", void: "vacant" }[r.status] || "info";
				var act = N.rowActs ? N.rowActs(r) : "";
				var amt = r.kind === "payment" || r.kind === "income" ? '<span class="nlrm-amt-in">' + N.ag(r.amount) + "</span>" : r.kind === "expense" || r.kind === "refund" ? '<span class="nlrm-amt-out">' + N.ag(r.amount) + "</span>" : N.ag(r.amount);
				return '<tr><td data-l="' + esc(t("col_date")) + '">' + N.date(r.paid_date || r.due_date) + '</td><td data-l="' + esc(t("col_unit")) + '">' + (u ? '<button type="button" class="nlrm-link" data-open="unit:' + u.id + '">' + esc(where(u)) + "</button>" : esc(p ? p.address : "-")) + '</td><td data-l="' + esc(t("col_what")) + '">' + esc(what) + (r.note ? '<br><small class="nlrm-note" style="margin:0">' + esc(r.note) + "</small>" : "") + '</td><td class="is-num" data-l="' + esc(t("col_amount")) + '">' + amt + '</td><td data-l="' + esc(t("col_status")) + '">' + chip(stc, t("ls_" + r.status)) + "</td><td>" + act + "</td></tr>";
			}).join("") + "</tbody></table>";
	}
	function mLedger(m) {
		var rows = N.store.d.ledger.filter(function (r) { return ((r.paid_date || r.due_date) || "").slice(0, 7) === m && r.kind !== "expense"; }).sort(function (a, b) { return (a.due_date || a.paid_date) < (b.due_date || b.paid_date) ? -1 : 1; });
		return "<h3>" + esc(t("mtab_ledger")) + "</h3>" + ledgerRows(rows);
	}
	function mCheques() {
		var rows = N.store.d.ledger.filter(function (r) { return r.method === "cheque" && r.kind === "payment" && (r.status === "pending" || r.status === "bounced"); }).sort(function (a, b) { return a.due_date < b.due_date ? -1 : 1; });
		return "<h3>" + esc(t("cheques_title")) + '</h3><p class="nlrm-lead">' + esc(t("cheques_lead")) + "</p>" + ledgerRows(rows);
	}
	function mExpenses() {
		var y = S.month.slice(0, 4), rows = N.store.d.ledger.filter(function (r) { return r.kind === "expense" && (r.paid_date || "").slice(0, 4) === y; });
		var by = {}; rows.forEach(function (r) { by[r.category] = (by[r.category] || 0) + r.amount; });
		var h = "<h3>" + esc(t("expenses_year", { y: y })) + '</h3><dl class="nlrm-facts">' + Object.keys(by).map(function (c) { return "<div><dt>" + esc(t("cat_" + c)) + "</dt><dd>" + N.ag(by[c]) + "</dd></div>"; }).join("") + "</dl>";
		return h + '<div style="margin-top:12px">' + ledgerRows(rows.slice().reverse()) + "</div>";
	}
	function mPnl() {
		var d = N.store.d, months = [];
		for (var i = -11; i <= 0; i++) { months.push(N.ym(i)); }
		var h = "<h3>" + esc(t("pnl_title")) + '</h3><table class="nlrm-table"><thead><tr><th>' + esc(t("col_property")) + '</th><th class="is-num">' + esc(t("pnl_income")) + '</th><th class="is-num">' + esc(t("pnl_expenses")) + '</th><th class="is-num">' + esc(t("pnl_net")) + "</th></tr></thead><tbody>";
		var tot = [0, 0];
		d.properties.forEach(function (p) {
			var inc = 0, ex = 0;
			d.ledger.forEach(function (r) {
				var mm = (r.paid_date || "").slice(0, 7);
				if (+r.property_id !== p.id || months.indexOf(mm) < 0) { return; }
				inc += N.mx.incomeOf(r);
				if (r.kind === "expense" && r.status !== "void") { ex += r.amount; }
			});
			tot[0] += inc; tot[1] += ex;
			h += '<tr><td data-l="' + esc(t("col_property")) + '"><button type="button" class="nlrm-link" data-go-prop="' + p.id + '">' + esc(p.address) + '</button></td><td class="is-num" data-l="' + esc(t("pnl_income")) + '">' + N.ag(inc) + '</td><td class="is-num" data-l="' + esc(t("pnl_expenses")) + '">' + N.ag(ex) + '</td><td class="is-num" data-l="' + esc(t("pnl_net")) + '"><b>' + N.ag(inc - ex) + "</b></td></tr>";
		});
		h += '<tr><td data-l=""><b>' + esc(t("total")) + '</b></td><td class="is-num" data-l="' + esc(t("pnl_income")) + '"><b>' + N.ag(tot[0]) + '</b></td><td class="is-num" data-l="' + esc(t("pnl_expenses")) + '"><b>' + N.ag(tot[1]) + '</b></td><td class="is-num" data-l="' + esc(t("pnl_net")) + '"><b>' + N.ag(tot[0] - tot[1]) + "</b></td></tr></tbody></table>";
		return h + '<p class="nlrm-note">' + esc(t("pnl_note")) + "</p>";
	}
	function mCpi() {
		var h = "<h3>" + esc(t("cpi_title")) + '</h3><p class="nlrm-lead">' + esc(t("cpi_lead")) + "</p>";
		h += '<form class="nlrm-form" id="nlrm-cpi"><div class="nlrm-fgrid">' + N.ui.field({ name: "amount", label: t("cpi_amount"), type: "number", value: 6000, inputmode: "numeric" }) + N.ui.field({ name: "from", label: t("cpi_from"), type: "date", value: N.addMonths(N.todayIso(), -12) }) + N.ui.field({ name: "to", label: t("cpi_to"), type: "date", value: N.todayIso() }) + '</div><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + esc(t("cpi_calc")) + '</button></div><div id="nlrm-cpi-out" aria-live="polite"></div></form>';
		var linked = N.store.d.leases.filter(function (l) { return l.status === "active" && l.linkage && l.linkage.mode === "cpi"; });
		if (linked.length) {
			h += '<h3 style="margin-top:18px">' + esc(t("cpi_leases")) + '</h3><ul class="nlrm-list">' + linked.map(function (l) {
				var u = N.ix.unit[l.unit_id], every = l.linkage.every || 12, next = l.start_date;
				while (next <= N.todayIso()) { next = N.addMonths(next, every); }
				return '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main" data-open="unit:' + u.id + '"><b>' + esc(where(u)) + "</b><small>" + esc(t("cpi_next", { date: N.dateText(next), pct: l.linkage.pct || 100 })) + "</small></button>" + btn("cpi-lease", t("cpi_check_now"), "secondary", "", ' data-lease="' + l.id + '"') + "</li>";
			}).join("") + "</ul>";
		}
		return h;
	}
	function mTax() {
		var y = S.month.slice(0, 4), rent = 0;
		N.store.d.leases.forEach(function (l) { if (l.status === "active") { rent += l.rent; } });
		var C = N.TAX_CEILING.amount;
		var h = "<h3>" + esc(t("tax_title", { y: y })) + '</h3><p class="nlrm-lead">' + esc(t("tax_lead")) + "</p>";
		h += '<form class="nlrm-form" id="nlrm-tax"><div class="nlrm-fgrid">' + N.ui.field({ name: "rent", label: t("tax_monthly"), type: "number", value: rent, hint: t("tax_monthly_hint") }) + N.ui.field({ name: "paid", label: t("tax_paid_rent"), type: "number", value: 0 }) + '</div><div id="nlrm-tax-out" aria-live="polite"></div></form>';
		h += '<p class="nlrm-note">' + esc(t("tax_note", { ceiling: N.moneyText(C) })) + "</p>";
		return h;
	}

	/* ---------- REPAIRS ---------- */
	function vRepairs() {
		var cols = ["new", "scheduled", "progress", "waiting", "done"];
		var h = head(t("nav_repairs"), esc(t("repairs_sub")), btn("new-ticket", t("new_ticket"), "primary", "plus"));
		h += '<div class="nlrm-board" style="--cols:5">';
		cols.forEach(function (st) {
			var list = N.store.d.tickets.filter(function (x) { return x.status === st && (st !== "done" || N.daysTo((x.closed_at || "").slice(0, 10)) > -90); });
			h += '<section class="nlrm-col" aria-label="' + esc(t("ts_" + st)) + '"><h4><span>' + esc(t("ts_" + st)) + "</span><span>" + list.length + "</span></h4>";
			list.forEach(function (x) {
				var u = N.ix.unit[x.unit_id], dd = N.daysTo(x.due_by), v = x.vendor_id ? N.ix.contact[x.vendor_id] : null;
				var dueChip = st === "done" ? chip("ok", t("ts_done")) : dd === null ? "" : dd < 0 ? chip("late", t("overdue_by", { n: -dd })) : chip(x.urgency === "urgent" || dd <= 5 ? "due" : "info", t("due_in", { when: N.when(dd) }));
				h += '<button type="button" class="nlrm-tcard" data-open="ticket:' + x.id + '"><b>' + esc(x.title) + "</b><small>" + esc(u ? where(u) : "") + "</small>" + '<span style="display:flex;gap:6px;flex-wrap:wrap">' + (x.urgency === "urgent" ? chip("late", t("urgent")) : "") + dueChip + "</span>" + (v ? "<small>" + esc(t("vendor_is", { name: v.name })) + "</small>" : "") + "</button>";
			});
			h += "</section>";
		});
		return h + '</div><p class="nlrm-note">' + esc(t("repairs_law")) + "</p>";
	}

	/* ---------- DOCUMENTS ---------- */
	function vDocs() {
		var kinds = ["all", "lease", "protocol", "id", "receipt", "insurance", "photo", "other"];
		var docs = N.store.d.docs.filter(function (x) { return S.dfilter === "all" || x.kind === S.dfilter || (S.dfilter === "other" && kinds.indexOf(x.kind) < 0); });
		var h = head(t("nav_docs"), esc(t("docs_sub")), btn("upload", t("upload"), "primary", "upload"));
		h += '<div class="nlrm-seg" role="group">' + kinds.map(function (k) { return '<button type="button" data-dfilter="' + k + '" aria-pressed="' + (S.dfilter === k) + '">' + esc(t("dk_" + k)) + "</button>"; }).join("") + "</div>";
		h += '<section class="nlrm-card">' + N.docTable(docs) + '<p class="nlrm-note">' + esc(t("docs_privacy")) + "</p></section>";
		return h;
	}

	/* ---------- LEASING ---------- */
	function vLeasing() {
		var vac = N.store.d.units.filter(function (u) { return !N.ix.leaseByUnit[u.id]; });
		var h = head(t("nav_leasing"), esc(t("leasing_sub")), btn("new-lease", t("new_lease"), "primary", "plus") + btn("new-contact", t("new_prospect"), "secondary", "plus", ' data-kind="prospect"'));
		h += '<section class="nlrm-card"><h3>' + esc(t("vacant_title")) + "</h3>";
		if (!vac.length) { h += '<p class="nlrm-empty">' + esc(t("vacant_none")) + "</p>"; }
		h += '<ul class="nlrm-list">' + vac.map(function (u) {
			var m = u.meta || {}, apps = N.store.d.contacts.filter(function (c) { return c.kind === "prospect" && (c.meta || {}).unit_id === u.id; }).length;
			return '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main" data-open="unit:' + u.id + '"><b>' + esc(where(u)) + "</b><small>" + esc([u.rooms ? t("rooms_n", { n: u.rooms }) : "", m.asking_rent ? t("asking", { amount: N.moneyText(m.asking_rent) }) : "", m.available_from ? t("available_from", { date: N.dateText(m.available_from) }) : "", t("applicants_n", { n: apps })].filter(Boolean).join(" · ")) + '</small></button><div class="nlrm-item-acts">' + btn("apply-link", t("act_apply_link"), "wa", "wa", ' data-unit="' + u.id + '"') + btn("publish", t("act_publish"), "secondary", "", ' data-unit="' + u.id + '"') + btn("new-lease", t("new_lease"), "quiet", "", ' data-unit="' + u.id + '"') + "</div></li>";
		}).join("") + "</ul></section>";
		h += '<h3 style="margin:18px 0 10px;font-size:20px">' + esc(t("pipeline_title")) + "</h3>" + prospectBoard(N.store.d.contacts.filter(function (c) { return c.kind === "prospect"; }));
		h += '<p class="nlrm-note">' + esc(t("leasing_law")) + "</p>";
		return h;
	}

	/* ---------- REPORTS ---------- */
	function vReports() {
		var y = String(N.today().getFullYear());
		var h = head(t("nav_reports"), esc(t("reports_sub")));
		h += '<div class="nlrm-grid2">';
		h += '<section class="nlrm-card"><h3>' + esc(t("rep_roll")) + '</h3><p class="nlrm-lead">' + esc(t("rep_roll_lead")) + '</p><div class="nlrm-tools">' + btn("rep-roll", t("rep_open"), "primary") + btn("csv-roll", t("rep_csv"), "secondary") + "</div></section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("rep_year", { y: y })) + '</h3><p class="nlrm-lead">' + esc(t("rep_year_lead")) + '</p><div class="nlrm-tools">' + btn("rep-year", t("rep_open"), "primary") + btn("csv-ledger", t("rep_csv"), "secondary") + "</div></section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("rep_evidence")) + '</h3><p class="nlrm-lead">' + esc(t("rep_evidence_lead")) + '</p><div class="nlrm-tools">' + btn("rep-evidence", t("rep_choose"), "primary") + "</div></section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("rep_export")) + '</h3><p class="nlrm-lead">' + esc(t("rep_export_lead")) + '</p><div class="nlrm-tools">' + btn("export-all", t("rep_export_btn"), "secondary") + "</div></section>";
		return h + "</div>";
	}

	/* ---------- SETTINGS ---------- */
	/* the guide: the manual's fragment in the interface language (assets/rentals/help/<lang>.html) */
	function vHelp() {
		var pdf = (S.cfg.assets || "/wp-content/plugins/nadlan-config/assets/rentals/") + "help/manual-" + (N.lang === "he" ? "he" : "en") + ".pdf" + (S.cfg.ver ? "?ver=" + S.cfg.ver : "");
		return head(t("nav_help"), esc(t("help_sub"))) + '<p style="margin:0 0 12px"><a class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" href="' + esc(pdf) + '" target="_blank" rel="noopener">' + I("doc", 18) + esc(t("help_pdf")) + "</a></p>" +
			'<div class="nlrm-card nlrm-help-host" id="nlrm-help"><p class="nlrm-empty">' + esc(t("loading")) + "</p></div>";
	}
	function mountHelp() {
		var host = root.querySelector("#nlrm-help");
		if (!host) { return; }
		var base = (S.cfg.assets || "/wp-content/plugins/nadlan-config/assets/rentals/") + "help/", lang = N.lang === "he" ? "he" : "en";
		fetch(base + lang + ".html" + (S.cfg.ver ? "?ver=" + S.cfg.ver : ""), { credentials: "omit" }).then(function (r) { if (!r.ok) { throw new Error(String(r.status)); } return r.text(); }).then(function (html) {
			if (!document.body.contains(host)) { return; }
			host.innerHTML = html;
			host.querySelectorAll("img").forEach(function (im) { var src = im.getAttribute("src") || ""; if (!/^(https?:|\/|data:)/.test(src)) { im.src = base + src; } im.loading = "lazy"; im.decoding = "async"; });
			host.querySelectorAll('a[href^="#h-"]').forEach(function (a) {
				a.addEventListener("click", function (e) { e.preventDefault(); var to = host.querySelector(a.getAttribute("href")); if (to) { to.scrollIntoView({ behavior: "smooth", block: "start" }); to.setAttribute("tabindex", "-1"); to.focus({ preventScroll: true }); } });
			});
		}).catch(function () { host.innerHTML = '<p class="nlrm-empty">' + esc(t("help_fail")) + "</p>"; });
	}
	/* the personal links: live ones first, each with who, until, uses and Cancel (the server refuses a cancelled link at once) */
	function linksCard() {
		var all = N.store.d.links, today = N.todayIso();
		if (!all) { return '<section class="nlrm-card" id="nlrm-links"><h3>' + I("link", 20) + esc(t("links_title")) + '</h3><p class="nlrm-empty">' + esc(t("loading")) + "</p></section>"; }
		var live = all.filter(function (k) { return !k.revoked_at && String(k.expires_at).slice(0, 10) >= today; });
		var who = function (k) {
			var c = k.contact_id ? N.ix.contact[k.contact_id] : null, where = "";
			if (k.scope === "lease") { var l = N.store.d.leases.find(function (x) { return x.id === k.scope_id; }); if (l) { where = N.where(N.ix.unit[l.unit_id] || {}); if (!c) { c = N.tenantsOf(l)[0]; } } }
			else if (k.scope === "unit") { where = N.where(N.ix.unit[k.scope_id] || {}); }
			else if (k.scope === "property") { where = (N.ix.prop[k.scope_id] || {}).address || ""; }
			return [c ? c.name : "", where].filter(Boolean).join(" · ");
		};
		var rows = live.map(function (k) {
			return '<li class="nlrm-item"><div class="nlrm-item-main"><b>' + esc(t("link_p_" + k.purpose)) + (who(k) ? " · " + esc(who(k)) : "") + "</b><small>" +
				esc(t("link_until", { date: N.dateText(String(k.expires_at).slice(0, 10)) })) + " · " + esc(+k.uses ? N.tn("link_uses", +k.uses) : t("link_uses_zero")) +
				(k.last_used_at ? " · " + esc(t("link_last", { date: N.dateText(String(k.last_used_at).slice(0, 10)) })) : "") +
				'</small></div><div class="nlrm-item-acts" style="width:auto">' + btn("link-revoke", t("link_revoke"), "quiet", "", ' data-link="' + k.id + '"') + "</div></li>";
		}).join("");
		var gone = all.length - live.length;
		return '<section class="nlrm-card" id="nlrm-links"><h3>' + I("link", 20) + esc(t("links_title")) + '</h3><p class="nlrm-lead">' + esc(t("links_lead")) + "</p>" +
			(rows ? '<ul class="nlrm-list">' + rows + "</ul>" : '<p class="nlrm-empty">' + esc(t("links_none")) + "</p>") +
			(gone ? '<p class="nlrm-note">' + esc(N.tn("links_gone", gone)) + "</p>" : "") + "</section>";
	}
	function vSettings() {
		var me = S.cfg.me || {}, pay = me.pay || {};
		var h = head(t("nav_settings"), "");
		h += '<div class="nlrm-grid2"><section class="nlrm-card"><h3>' + esc(t("set_profile")) + '</h3><form class="nlrm-form" id="nlrm-set-profile"><div class="nlrm-fgrid">' +
			N.ui.field({ name: "display", label: t("set_display"), value: me.display || "", hint: t("set_display_hint") }) +
			N.ui.field({ name: "phone", label: t("set_phone"), type: "tel", value: me.phone ? N.phoneShow(me.phone) : "", hint: t("set_phone_hint"), autocomplete: "tel" }) +
			N.ui.field({ name: "notify", label: t("set_notify"), type: "check", value: me.notify !== false, hint: t("set_notify_hint") }) +
			'</div><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + esc(t("save")) + "</button></div></form></section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("set_pay")) + '</h3><p class="nlrm-lead">' + esc(t("set_pay_lead")) + '</p><form class="nlrm-form" id="nlrm-set-pay"><div class="nlrm-fgrid">' +
			N.ui.field({ name: "bank", label: t("set_bank"), type: "textarea", rows: 2, value: pay.bank || "", hint: t("set_bank_hint") }) +
			N.ui.field({ name: "bit", label: t("set_bit"), type: "tel", value: pay.bit ? N.phoneShow(pay.bit) : "" }) +
			N.ui.field({ name: "link", label: t("set_link"), type: "url", value: pay.link || "", ltr: true }) +
			'</div><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + esc(t("save")) + "</button></div></form></section></div>";
		h += '<section class="nlrm-card" style="margin-top:14px"><h3>' + I("wa", 20) + esc(t("quick_title")) + '</h3><p class="nlrm-lead">' + esc(t("quick_lead_long")) + "</p>" + btn("quick-link", t("quick_btn"), "wa", "wa") + "</section>";
		h += linksCard();
		h += '<section class="nlrm-card"><h3>' + esc(t("set_privacy")) + '</h3><p class="nlrm-lead">' + esc(t("set_privacy_lead")) + '</p><div class="nlrm-tools">' + btn("export-all", t("rep_export_btn"), "secondary") + btn("erase", t("set_erase"), "danger") + "</div></section>";
		var plan = N.store.d.plan || { id: "free" }, offer = plan.offer || null;
		h += '<section class="nlrm-card"><h3>' + esc(t("set_plan")) + " " + chip(plan.state === "grace" ? "due" : "info", t("plan_" + plan.id)) + '</h3><p class="nlrm-lead">' + esc(t("plan_lead_" + plan.id)) + "</p>" +
			(plan.until ? '<p class="nlrm-note">' + esc(t(plan.state === "grace" ? "plan_grace" : "plan_until", { date: N.dateText(plan.until) })) + "</p>" : "") +
			/* the offer: only when the site sells it (the server decides: billing on, or a test for administrators) */
			(offer ? '<div class="nlrm-grid2" style="margin-top:12px">' + ["pro", "business"].filter(function (k) { return offer[k]; }).map(function (k) {
				var o = offer[k];
				return '<div class="nlrm-kpi"><span>' + esc(t("plan_" + k)) + "</span><b>" + N.money(o.price) + " <small>" + esc(t("per_month")) + "</small></b><small>" + esc(t("plan_units", { n: N.num(o.units) })) + '</small><a class="nlrm-btn nlrm-btn--primary nlrm-btn--sm" style="margin-top:8px" href="' + esc(o.buy) + '">' + esc(t(plan.id === k ? "plan_renew" : "plan_buy")) + "</a></div>";
			}).join("") + "</div>" + '<p class="nlrm-note">' + esc(t(offer[Object.keys(offer)[0]].test ? "plan_test_note" : "plan_pay_note")) + "</p>" : "") + "</section>";
		return h;
	}

	/* ---------- interactions ---------- */
	function wireScreen() {
		var q = root.querySelector("#nlrm-q");
		if (q) { q.addEventListener("input", function () { search(q); }); q.addEventListener("keydown", function (e) { if (e.key === "Escape") { q.value = ""; search(q); } }); }
		if (S.route === "property") { mount3d(+S.param); }
		if (S.route === "help") { mountHelp(); }
		if (S.route === "settings" && !N.store.d.links && N.store.adapter.links) { N.store.links().catch(function () { N.store.d.links = []; render(); }); }
		if (S.route === "properties" && S.cfg.mapbox) { mountMap(); }
		var cpi = root.querySelector("#nlrm-cpi");
		if (cpi) {
			cpi.addEventListener("submit", function (e) {
				e.preventDefault();
				var v = N.ui.values(cpi), out = cpi.querySelector("#nlrm-cpi-out");
				out.innerHTML = '<p class="nlrm-note">' + esc(t("loading")) + "</p>";
				N.store.cpi(v.amount, v.from, v.to).then(function (r) {
					out.innerHTML = '<div class="nlrm-hint" style="margin-top:10px"><b>' + N.money(r.amount) + "</b> · " + esc(t("cpi_result", { pct: r.change_percent, from: r.from_index_date, to: r.to_index_date })) + (r.demo ? "<br>" + esc(t("cpi_demo")) : "<br>" + esc(t("cpi_source"))) + "</div>";
				}).catch(function () { out.innerHTML = '<p class="nlrm-ferr">' + esc(t("cpi_fail")) + "</p>"; });
			});
		}
		var tax = root.querySelector("#nlrm-tax");
		if (tax) {
			var calc = function () {
				var v = N.ui.values(tax), G = +v.rent || 0, C = N.TAX_CEILING.amount, P = +v.paid || 0;
				var E = G <= C ? G : (G < 2 * C ? 2 * C - G : 0), R = G * 12, D = Math.min(P, R);
				var ten = Math.round(0.10 * Math.max(0, R - D));
				tax.querySelector("#nlrm-tax-out").innerHTML = '<dl class="nlrm-facts" style="margin-top:10px"><div><dt>' + esc(t("tax_exempt")) + "</dt><dd>" + N.money(E) + " " + esc(t("per_month")) + "</dd></div><div><dt>" + esc(t("tax_taxable")) + "</dt><dd>" + N.money(G - E) + " " + esc(t("per_month")) + "</dd></div><div><dt>" + esc(t("tax_ten")) + "</dt><dd>" + N.money(ten) + " " + esc(t("per_year")) + "</dd></div></dl>";
			};
			tax.addEventListener("input", calc); calc();
		}
		["nlrm-set-profile", "nlrm-set-pay"].forEach(function (id) {
			var f = root.querySelector("#" + id);
			if (!f) { return; }
			f.addEventListener("submit", function (e) {
				e.preventDefault();
				var v = N.ui.values(f);
				S.cfg.me = S.cfg.me || {};
				if (id === "nlrm-set-profile") { S.cfg.me.display = v.display; S.cfg.me.phone = N.phone(v.phone); S.cfg.me.notify = !!v.notify; } else { S.cfg.me.pay = { bank: v.bank, bit: N.phone(v.bit), link: v.link }; }
				(S.cfg.saveMe ? S.cfg.saveMe(S.cfg.me) : Promise.resolve()).then(function () { N.ui.toast(t("saved")); }).catch(function (ex) { N.ui.toast(ex.message || t("err_generic"), "bad"); });
			});
		});
	}
	function search(q) {
		var v = q.value.trim().toLowerCase(), host = q.parentNode, old = host.querySelector(".nlrm-results");
		if (old) { old.remove(); }
		if (v.length < 2) { return; }
		var res = [];
		N.store.d.contacts.forEach(function (c) { if ((c.name || "").toLowerCase().indexOf(v) >= 0 || (c.phone || "").indexOf(v.replace(/\D/g, "") || "~") >= 0) { res.push({ o: "contact:" + c.id, a: c.name, b: t("kind_" + c.kind) }); } });
		N.store.d.units.forEach(function (u) { var w = where(u); if (w.toLowerCase().indexOf(v) >= 0) { res.push({ o: "unit:" + u.id, a: w, b: (N.ix.prop[u.property_id] || {}).city }); } });
		N.store.d.tickets.forEach(function (x) { if ((x.title || "").toLowerCase().indexOf(v) >= 0) { res.push({ o: "ticket:" + x.id, a: x.title, b: t("nav_repairs") }); } });
		var box = document.createElement("div");
		box.className = "nlrm-results";
		box.innerHTML = res.length ? res.slice(0, 12).map(function (r) { return '<button type="button" data-open="' + r.o + '"><span><b>' + esc(r.a) + "</b><br><small>" + esc(r.b || "") + "</small></span></button>"; }).join("") : '<p class="nlrm-note" style="padding:8px 10px">' + esc(t("search_none")) + "</p>";
		host.appendChild(box);
	}
	function mount3d(pid) {
		var host = root.querySelector("#nlrm-3d");
		if (!host) { return; }
		var go = function () {
			var p = N.ix.prop[pid], us = N.ix.unitsByProp[pid] || [];
			if (!p || !window.NLRM3D) { return; }
			host.innerHTML = "";
			if (N._b3d) { try { N._b3d.dispose(); } catch (e) { /* gone */ } }
			N._b3d = window.NLRM3D.mountBuilding(host, {
				floors: p.floors, unitsPerFloor: p.units_per_floor, orientation: (p.meta || {}).orientation || 0, meta: p.meta || {},
				units: us.map(function (u) { var l = N.ix.leaseByUnit[u.id], ten = l ? N.tenantsOf(l)[0] : null; return { id: u.id, label: u.label, floor: u.floor, pos: u.pos, dir: u.dir, status: N.unitStatus(u), tenant: ten ? ten.name : "", badges: N.unitBadges(u) }; }),
				lang: N.lang, rtl: N.rtl, labels: { floor: t("floor_n", { n: "{n}" }), ground: t("ground_floor"), roof: t("roof") },
				onPick: function (id) { N.open("unit", id); },
				/* drill-down: building -> floor (its card) -> apartment -> tenant, lease, payments, repairs */
				onPickFloor: function (f) { N.forms.floorCard(pid, f); },
				onPickEmpty: function (f, pos) { N.forms.unit({ property_id: pid, floor: f, pos: pos }); }
			});
		};
		N.onLayersClosed = function () { if (N._b3d && N._b3d.clearFloor && document.body.contains(host)) { N._b3d.clearFloor(); } };
		if (window.NLRM3D) { go(); } else { window.addEventListener("nlrm3d:ready", go, { once: true }); setTimeout(function () { if (!window.NLRM3D) { host.querySelector(".nlrm-3d-wait") && (host.querySelector(".nlrm-3d-wait").textContent = t("no_3d")); } }, 9000); }
	}
	function mountMap() {
		var host = root.querySelector("#nlrm-map");
		var start = function () {
			if (!window.mapboxgl || !host) { return; }
			window.mapboxgl.accessToken = S.cfg.mapbox;
			var pts = N.store.d.properties.filter(function (p) { return p.lat && p.lng; });
			var map = new window.mapboxgl.Map({ container: host, style: "mapbox://styles/mapbox/light-v11", center: pts[0] ? [pts[0].lng, pts[0].lat] : [34.85, 32.05], zoom: 10, cooperativeGestures: true });
			var b = new window.mapboxgl.LngLatBounds();
			pts.forEach(function (p) {
				var el = document.createElement("button");
				el.type = "button"; el.className = "nlrm-pin"; el.setAttribute("aria-label", p.address);
				el.style.cssText = "width:30px;height:30px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#2f6f86;border:2px solid #fff;box-shadow:0 4px 10px rgba(20,33,43,.3);cursor:pointer";
				el.addEventListener("click", function () { N.go("property", p.id); });
				new window.mapboxgl.Marker({ element: el, anchor: "bottom" }).setLngLat([p.lng, p.lat]).setPopup(new window.mapboxgl.Popup({ offset: 18 }).setText(p.address + ", " + p.city)).addTo(map);
				b.extend([p.lng, p.lat]);
			});
			if (pts.length > 1) { map.fitBounds(b, { padding: 60, maxZoom: 13 }); }
		};
		if (window.mapboxgl) { start(); return; }
		var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css"; document.head.appendChild(l);
		var s = document.createElement("script"); s.src = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"; s.onload = start; document.head.appendChild(s);
	}

	function onClick(e) {
		var el = e.target.closest("[data-go],[data-go-prop],[data-open],[data-act],[data-seg],[data-mtab],[data-dfilter],[data-lang]");
		if (!el || !root.contains(el)) { return; }
		if (el.dataset.lang) { N.relang(el.dataset.lang); return; }
		if (el.dataset.go) { S.attAll = false; N.go(el.dataset.go); return; }
		if (el.dataset.goProp) { N.go("property", el.dataset.goProp); return; }
		if (el.dataset.seg) { S.seg = el.dataset.seg; render(); return; }
		if (el.dataset.mtab) { S.mtab = el.dataset.mtab; render(); return; }
		if (el.dataset.dfilter) { S.dfilter = el.dataset.dfilter; render(); return; }
		if (el.dataset.open && !el.dataset.act) { var o = el.dataset.open.split(":"); N.open(o[0], +o[1]); var r = root.querySelector(".nlrm-results"); if (r) { r.remove(); } return; }
		if (el.dataset.act) { N.act(el.dataset.act, el, e); }
	}
	N.render = render;
})();
