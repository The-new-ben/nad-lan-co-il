/* ============================================================================
   NADLAN URBAN RENEWAL - the management room (RenewalRoomPro, 26.10.2026; v2 layout of 2026-07-12 kept inside it).
   One app, three modes:
     mode=demo  - the public read-only sample room (REST /renewal-demo) on the /my-renewal/ landing
     mode=live  - one room (REST /renewal-space/{id}); what it shows depends on the role the server returns
     mode=org   - an organizing company: the portfolio of complexes (REST /renewal-org/{id}/portfolio) and each complex
   Screens: portfolio, complex (consent, the law, the building facade, the selected apartment, the ten stages,
   deadlines, tasks, documents, neighbours), updates (feed, WhatsApp, invite, what a neighbour sees), report (print).
   A neighbour gets one phone screen: the building totals, the stage, the updates and their own apartment.
   The server filters the payload by role (inc/renewal-room.php); this script never receives what a role may not see.
   Additive law: the 3D building and the map of the v2 room stay, one tap away from the facade.
   All words arrive in data-i18n (HE/EN/RU), none are written here.
============================================================================ */
(function () {
	"use strict";
	var root = document.getElementById("nlurd-mount");
	if (!root || root.dataset.wired) { return; }
	root.dataset.wired = "1";

	var D = root.dataset;
	var MODE = D.mode || "live";
	var REST = D.rest || "";
	var NONCE = D.nonce || "";
	var GLB = D.glb || "";
	var LANG = D.lang || "he";
	var QS = LANG !== "he" ? "?lang=" + LANG : "";
	var TODAY = D.today || new Date().toISOString().slice(0, 10);
	var I = {};
	try { I = JSON.parse(D.i18n || "{}"); } catch (e) { I = {}; }
	var ST = ["consented", "partial", "in_process", "missing_docs", "refused", "unreached"];
	var CLS = { consented: "s-yes", partial: "s-part", in_process: "s-proc", missing_docs: "s-docs", refused: "s-no", unreached: "s-none" };
	var st = { tab: null, space: parseInt(D.space || "0", 10) || 0, org: D.org || "", S: null, P: null, apt: null, hi: null, stageOpen: null, view: "facade", bld: null, newcx: false };
	var map = null, mapMarker = null;

	/* ---------- helpers ---------- */
	function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
	function t(k, v) {
		var s = I[k] != null ? String(I[k]) : k;
		if (v) { Object.keys(v).forEach(function (x) { s = s.split("{" + x + "}").join(String(v[x])); }); }
		return s;
	}
	function $(s, el) { return (el || root).querySelector(s); }
	function $$(s, el) { return [].slice.call((el || root).querySelectorAll(s)); }
	function api(path, opts) {
		opts = opts || {};
		opts.headers = Object.assign({ "Content-Type": "application/json" }, NONCE ? { "X-WP-Nonce": NONCE } : {}, opts.headers || {});
		opts.credentials = "same-origin";
		return fetch(REST + path, opts).then(function (r) {
			return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) { j = j || {}; j._status = r.status; throw j; } return j; });
		});
	}
	function post(path, body) { return api(path + QS, { method: "POST", body: JSON.stringify(body || {}) }); }
	function dmy(s) {
		if (!s) { return ""; }
		var m = String(s).match(/^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2}))?/);
		if (!m) { return String(s); }
		return (+m[3]) + "." + (+m[2]) + "." + m[1] + (m[4] ? " " + m[4] + ":" + m[5] : "");
	}
	function daysSince(s) {
		if (!s) { return null; }
		var a = new Date(String(s).slice(0, 10) + "T00:00:00Z"), b = new Date(TODAY + "T00:00:00Z");
		return Math.round((b - a) / 864e5);
	}
	function N(n) { return '<span class="num" dir="ltr">' + esc(n) + "</span>"; }
	function pct(yes, total) { return total ? Math.round(yes / total * 1000) / 10 : 0; }
	function stLabel(k) {
		if (k === "partial") { return t("st_partial"); }
		var s = st.S && st.S.statuses && st.S.statuses[k];
		return s ? s[0] : k;
	}
	function trackLabel(k) { var s = t("track_" + (k || "unclear")); return s.indexOf("track_") === 0 ? (k || "") : s; }
	function bName(b, i) { return b.label || (t("building") + " " + (i + 1)); }
	function caps() { return (st.S && st.S.caps) || {}; }
	function isMgr() { return !!caps().private; }
	function buildings() { return (st.S && st.S.buildings) || []; }
	function aptById(id) { return ((st.S && st.S.apartments) || []).filter(function (a) { return a.id === id; })[0] || null; }
	function shown(a) { return a.shown || (a.consent_status === "consented" && (a.owners || []).some(function (o) { return !o.signed; }) ? "partial" : a.consent_status); }
	function counts() {
		if (st.S.counts) { return st.S.counts; }
		var c = { total: 0, yes: 0 }; ST.forEach(function (k) { c[k] = 0; });
		(st.S.apartments || []).forEach(function (a) { var s = shown(a); c[s] = (c[s] || 0) + 1; c.total++; if (s === "consented") { c.yes++; } });
		return c;
	}
	function setUrl() {
		try {
			var q = [];
			if (st.space && st.tab !== "portfolio") { q.push("space=" + st.space); }
			if (LANG !== "he") { q.push("lang=" + LANG); }
			if (MODE !== "demo") { history.replaceState(null, "", location.pathname + (q.length ? "?" + q.join("&") : "") + (st.tab ? "#" + st.tab : "")); }
		} catch (e) { /* history optional */ }
	}

	/* ---------- shell ---------- */
	function tabsFor() {
		if (MODE === "demo") { return ["complex", "updates", "report"]; }
		if (!st.S) { return st.P ? ["portfolio"] : []; }
		var r = st.S ? st.S.role : "";
		if (r === "neighbor") { return []; }
		var list = ["complex", "updates", "report"];
		if (st.P) { list.unshift("portfolio"); }
		return list;
	}
	function shell() {
		var S = st.S, org = (st.P && st.P.org) || (S && S.org) || null;
		var sample = (S && (S.is_demo || S.is_sample)) || (st.P && (st.P.complexes || []).some(function (c) { return c.is_sample; }));
		var neighbor = S && S.role === "neighbor";
		var title = MODE === "demo" ? t("room_demo") : neighbor ? t("room_building") : t("room_title");
		var h = '<div class="rrp" dir="' + (LANG === "he" ? "rtl" : "ltr") + '" lang="' + esc(LANG) + '">';
		h += '<header class="rrp-bar"><div class="rrp-bar__in">';
		h += '<div class="rrp-brand"><i aria-hidden="true">' + esc(t("brand_mark")) + "</i><div><b>" + esc(title) + "</b>" + (sample ? '<span class="rrp-sample">' + esc(t("demo_badge")) + "</span>" : "") +
			"<span>" + esc(t("brand_sub")) + "</span></div></div>";
		h += '<div class="rrp-org">' + (org ? t("managed_by", { org: "<b>" + esc(org.name) + "</b>" }) + "<br>" + esc(t("org_line", { s: org.staff || 0, c: st.P ? (st.P.complexes || []).length : 1 })) : "") + "</div>";
		var tabs = tabsFor();
		if (tabs.length) {
			h += '<nav class="rrp-tabs" role="tablist" aria-label="' + esc(t("tabs_label")) + '">';
			tabs.forEach(function (k) { h += '<button type="button" class="rrp-tab" role="tab" data-tab="' + k + '" aria-selected="' + (st.tab === k ? "true" : "false") + '">' + esc(t("tab_" + k)) + "</button>"; });
			h += "</nav>";
		}
		h += '</div></header><div class="rrp-main" data-main></div>';
		if (S && S.caps && S.caps.read_only) { h += '<p class="rrp-lapsed">' + esc(t("read_only")) + "</p>"; }
		h += "</div>";
		root.innerHTML = h;
		root.removeAttribute("data-loading");
	}
	function show(tab) {
		var tabs = tabsFor();
		if (tabs.length && tabs.indexOf(tab) < 0) { tab = tabs[0]; }
		st.tab = tab || null;
		shell();
		var m = $("[data-main]");
		if (st.S && st.S.role === "neighbor") { m.innerHTML = vNeighbor(st.S, false); afterNeighbor(); setUrl(); return; }
		if (tab === "portfolio") { m.innerHTML = vPortfolio(); }
		else if (tab === "complex") { m.innerHTML = vComplex(); fillComplex(); }
		else if (tab === "updates") { m.innerHTML = vUpdates(); }
		else if (tab === "report") { m.innerHTML = vReport(); }
		setUrl();
	}

	/* ---------- boot ---------- */
	function loadSpace(id, tab) {
		var p = MODE === "demo" ? api("/renewal-demo" + QS) : api("/renewal-space/" + id + QS);
		return p.then(function (d) {
			st.S = d; st.space = d.id; st.apt = null; st.stageOpen = null; st.view = "facade"; st.bld = null;
			if (MODE === "demo") { var f = (d.apartments || [])[0]; st.apt = f ? f.id : null; }
			show(tab || (d.role === "neighbor" ? null : "complex"));
		});
	}
	function loadPortfolio(tab) {
		return api("/renewal-org/" + (st.org || "mine") + "/portfolio" + QS).then(function (d) { st.P = d; if (tab) { show(tab); } return d; });
	}
	function fail() { root.innerHTML = '<p class="rrp-fail">' + esc(t("load_fail")) + "</p>"; root.removeAttribute("data-loading"); }
	function boot() {
		var want = (location.hash || "").replace("#", "");
		if (MODE === "demo") { loadSpace(0, "complex").catch(fail); return; }
		if (MODE === "org") {
			loadPortfolio(null).then(function () {
				if (st.space) { return loadSpace(st.space, ["complex", "updates", "report"].indexOf(want) >= 0 ? want : "complex"); }
				show("portfolio");
			}).catch(fail);
			return;
		}
		loadSpace(st.space, ["complex", "updates", "report"].indexOf(want) >= 0 ? want : null).catch(fail);
	}

	/* ---------- portfolio ---------- */
	function ladMini(stage, ladder) {
		var h = '<span class="rrp-ladmini" role="img" aria-label="' + esc(t("stage_of", { n: stage + 1 })) + '">';
		for (var i = 0; i < 10; i++) { h += "<i" + (i < stage ? ' class="d"' : i === stage ? ' class="n"' : "") + "></i>"; }
		return h + "<em>" + esc((ladder || [])[stage] || "") + "</em></span>";
	}
	function meter(c, track) {
		var p = pct(c.yes, c.total);
		return '<div class="rrp-mrow"><span class="rrp-pct"><span dir="ltr">' + Math.round(p) + '%</span> <small dir="ltr">' + c.yes + "/" + c.total + '</small></span><div class="rrp-meter"><i style="width:' + p + '%"></i>' +
			(track === "pinui_binui" ? '<u style="inset-inline-start:66.67%" title="' + esc(t("two_thirds")) + '"></u>' : "") + "</div></div>";
	}
	function why(c) {
		return (c.attention || []).map(function (w) { return t("attn_" + w.code, { n: w.n, label: w.label || "" }); }).join(" · ");
	}
	function nextAction(c) {
		if (c.law && c.law.applies && c.law.short > 0 && c.stage <= 2) { return t("next_two_thirds", { n: c.law.short }); }
		if (c.counts.unreached > 0 && c.stage <= 2) { return t("next_reach", { n: c.counts.unreached }); }
		if (c.next_deadline && c.next_deadline.days >= 0 && c.next_deadline.days <= 30) { return t("next_deadline", { label: c.next_deadline.label, n: c.next_deadline.days }); }
		return ((st.P && st.P.first_action) || [])[c.stage] || "";
	}
	function vPortfolio() {
		var P = st.P || { complexes: [] }, L = P.complexes || [];
		var f = st.pf || "all";
		var tot = { cx: L.length, bld: 0, apt: 0, yes: 0, miss: 0, attn: 0 };
		L.forEach(function (c) { tot.bld += c.buildings; tot.apt += c.counts.total; tot.yes += c.counts.yes; tot.miss += c.counts.docs_missing_apts; if ((c.attention || []).length) { tot.attn++; } });
		var h = '<section aria-labelledby="rrp-pf-h"><div class="rrp-h"><div><h2 id="rrp-pf-h">' + esc(t("tab_portfolio")) + "</h2><p>" + esc(t("pf_sub")) + "</p></div>" +
			(P.can_create ? '<button class="rrp-btn pri" type="button" data-newcx>' + esc(t("new_complex")) + "</button>" : "") + "</div>";
		if (st.newcx) { h += vNewComplex(); }
		h += '<div class="rrp-kpis">' +
			kpi(tot.cx, t("kpi_cx")) + kpi(tot.bld, t("kpi_bld")) + kpi(tot.apt, t("kpi_apt")) +
			kpi((tot.apt ? Math.round(tot.yes / tot.apt * 100) : 0) + "%", t("kpi_yes")) + kpi(tot.miss, t("kpi_miss")) + kpi(tot.attn, t("kpi_attn"), tot.attn > 0) + "</div>";
		h += '<div class="rrp-filters" role="group" aria-label="' + esc(t("filter_label")) + '">';
		["all", "pinui_binui", "tama", "attn"].forEach(function (k) { h += '<button type="button" class="rrp-filter" data-pf="' + k + '" aria-pressed="' + (f === k ? "true" : "false") + '">' + esc(t("f_" + k)) + "</button>"; });
		h += "</div>";
		var list = L.filter(function (c) { return f === "all" || (f === "attn" ? (c.attention || []).length > 0 : f === "tama" ? c.track.indexOf("tama") === 0 : c.track === f); });
		if (!L.length) { h += '<p class="rrp-empty">' + esc(t("pf_empty")) + "</p>"; }
		var rows = "", cards = "";
		list.forEach(function (c) {
			var w = why(c), sub = esc(c.street) + " · " + esc(c.buildings === 1 ? t("one_building") : t("n_buildings", { n: c.buildings })) + " · " + esc(t("updated_on", { d: dmy(c.last_activity) }));
			rows += '<tr class="row" tabindex="0" data-open="' + c.id + '"><td class="nm"><b>' + esc(c.name) + " · " + esc(c.city) + "</b><span>" + sub + "</span></td>" +
				'<td><span class="rrp-chip t-' + esc(c.track) + '">' + esc(trackLabel(c.track)) + "</span></td><td>" + ladMini(c.stage, P.ladder) + "</td><td>" + meter(c.counts, c.track) + "</td>" +
				'<td><span class="rrp-pct">' + c.counts.docs_missing_apts + "</span>" + (w ? '<div class="rrp-flag">' + esc(t("attn_lead")) + " " + esc(w) + "</div>" : "") + '</td><td class="rrp-next">' + esc(nextAction(c)) + "</td></tr>";
			cards += '<button type="button" class="rrp-card" data-open="' + c.id + '"><span class="top"><span><b>' + esc(c.name) + " · " + esc(c.city) + "</b><span>" + sub + '</span></span><span class="rrp-chip t-' + esc(c.track) + '">' + esc(trackLabel(c.track)) + "</span></span>" +
				ladMini(c.stage, P.ladder) + meter(c.counts, c.track) + '<span class="rrp-next">' + esc(nextAction(c)) + (w ? ' <span class="rrp-flag">' + esc(t("attn_lead")) + " " + esc(w) + "</span>" : "") + "</span></button>";
		});
		if (L.length) {
			h += '<div class="rrp-panel rrp-portwrap"><table class="rrp-port"><thead><tr><th scope="col">' + esc(t("col_cx")) + '</th><th scope="col">' + esc(t("col_track")) + '</th><th scope="col">' + esc(t("col_stage")) +
				'</th><th scope="col">' + esc(t("col_signed")) + '</th><th scope="col">' + esc(t("col_miss")) + '</th><th scope="col">' + esc(t("col_next")) + "</th></tr></thead><tbody>" + rows + "</tbody></table></div>";
			h += '<div class="rrp-cards">' + cards + "</div>";
		}
		h += '<p class="rrp-note rrp-foot">' + esc(t("pf_foot")) + "</p></section>";
		return h;
	}
	function kpi(v, l, warn) { return '<div class="rrp-kpi' + (warn ? " warn" : "") + '"><b class="num">' + esc(v) + "</b><span>" + esc(l) + "</span></div>"; }
	function bRow(i, b) {
		b = b || {};
		return '<div class="rrp-nbrow" data-nb-row><label class="rrp-field">' + esc(t("f_b_label")) + '<input type="text" data-nb="label" maxlength="40" value="' + esc(b.label || (t("building") + " " + (i + 1))) + '"></label>' +
			'<label class="rrp-field">' + esc(t("f_b_addr")) + '<input type="text" data-nb="address" maxlength="120" value="' + esc(b.address || "") + '"></label>' +
			'<label class="rrp-field rrp-sm">' + esc(t("f_floors")) + '<input type="number" inputmode="numeric" data-nb="floors" min="1" max="40" value="' + (b.floors || 4) + '"></label>' +
			'<label class="rrp-field rrp-sm">' + esc(t("f_upf")) + '<input type="number" inputmode="numeric" data-nb="upf" min="1" max="12" value="' + (b.upf || 4) + '"></label></div>';
	}
	function vNewComplex() {
		var h = '<form class="rrp-panel rrp-newcx" data-newcx-form><h3>' + esc(t("new_complex")) + "</h3>";
		h += '<div class="rrp-grid2"><label class="rrp-field">' + esc(t("f_cx_name")) + '<input type="text" data-nc="name" maxlength="80" required></label>' +
			'<label class="rrp-field">' + esc(t("f_city")) + '<input type="text" data-nc="city" maxlength="60" required></label>' +
			'<label class="rrp-field">' + esc(t("col_track")) + '<select data-nc="track">' + ["pinui_binui", "tama38_1", "tama38_2", "unclear"].map(function (k) { return '<option value="' + k + '">' + esc(trackLabel(k)) + "</option>"; }).join("") + "</select></label></div>";
		h += '<div data-nb-list>' + bRow(0) + "</div>";
		h += '<div class="rrp-row"><button type="button" class="rrp-btn" data-nb-add>' + esc(t("add_building")) + '</button><button type="submit" class="rrp-btn pri">' + esc(t("create_cx")) + "</button></div>";
		h += '<p class="rrp-note">' + esc(t("new_cx_note")) + '</p><div class="rrp-saved" data-nc-msg aria-live="polite"></div></form>';
		return h;
	}

	/* ---------- complex ---------- */
	function vComplex() {
		var S = st.S, c = counts(), B = buildings();
		var name = S.complex_name || S.title;
		var h = '<section aria-labelledby="rrp-cx-h"><div class="rrp-cxhead"><div><h2 id="rrp-cx-h">' + esc(name) + (S.city && name.indexOf(S.city) < 0 ? " · " + esc(S.city) : "") + "</h2><p>" +
			esc(S.street_line || (B[0] && B[0].address) || S.address || "") + " · " + esc(B.length === 1 ? t("one_building") : t("n_buildings", { n: B.length })) + " · " + esc(t("n_apts", { n: c.total })) +
			' · <span class="rrp-chip t-' + esc(S.track) + '">' + esc(trackLabel(S.track)) + "</span> · " + esc(t("stage_of", { n: S.stage + 1 })) + ": " + esc((S.ladder || [])[S.stage] || "") + "</p></div>";
		if (st.P && (st.P.complexes || []).length > 1) {
			h += '<label class="rrp-note rrp-pick">' + esc(t("pick_cx")) + '<select class="rrp-sel" data-cx-pick>' + st.P.complexes.map(function (x) { return '<option value="' + x.id + '"' + (x.id === S.id ? " selected" : "") + ">" + esc(x.name + " · " + x.city) + "</option>"; }).join("") + "</select></label>";
		}
		h += "</div>";
		h += '<div class="rrp-cx"><div class="rrp-cxmain">';
		h += '<div class="rrp-panel rrp-consent" data-o="1" data-consent></div>';
		if (S.law && S.law.applies) { h += '<div class="rrp-panel rrp-law" data-o="2" data-law></div>'; }
		h += '<div class="rrp-panel rrp-sheet" data-o="2">' +
			'<div class="rrp-sheet__h"><h3>' + esc(t("facade_t")) + '</h3><div class="rrp-views" role="group" aria-label="' + esc(t("views_label")) + '">' + viewBtn("facade") + (GLB ? viewBtn("3d") : "") + (D.mapbox && (S.centroid || S.city) ? viewBtn("map") : "") + "</div></div>" +
			'<div data-stage-host></div></div>';
		h += '<div class="rrp-panel rrp-ladder" data-o="4"><div class="rrp-sheet__h"><h3>' + esc(t("ladder_t")) + '</h3><span class="rrp-note">' + esc(t("ladder_note")) + '</span></div><div class="rrp-steps" data-steps role="group" aria-label="' + esc(t("ladder_t")) + '"></div><div class="rrp-stagecard" data-stagecard></div></div>';
		if (isMgr() || S.deadlines) { h += '<div class="rrp-panel rrp-dl" data-o="5" data-deadlines></div>'; }
		h += '<div class="rrp-2col" data-o="5"><div class="rrp-panel rrp-tasks"><h3>' + esc(t("todo_title")) + '</h3><ul data-tasks></ul><p class="rrp-note">' + esc(t("todo_note")) + "</p></div>" +
			'<div class="rrp-panel rrp-docsum"><h3>' + esc(t("docs_title")) + '</h3><div data-docsum></div><p class="rrp-note">' + esc(t("docs_hint")) + "</p></div></div>";
		if (isMgr()) { h += '<div class="rrp-panel rrp-members" data-o="6" data-members></div>'; }
		h += '</div><aside class="rrp-panel rrp-drawer" data-drawer aria-live="polite" aria-label="' + esc(t("apt_title")) + '"></aside></div></section>';
		return h;
	}
	function viewBtn(k) { return '<button type="button" class="rrp-vbtn" data-view="' + k + '" aria-pressed="' + (st.view === k ? "true" : "false") + '">' + esc(t("view_" + k)) + "</button>"; }
	function fillComplex() { fillConsent(); fillLaw(); fillStage(); fillLadder(); fillDeadlines(); fillTasks(); fillDocs(); fillMembers(); fillDrawer(); }
	function fillConsent() {
		var S = st.S, c = counts(), el = $("[data-consent]");
		if (!el) { return; }
		var gap;
		if (S.law && S.law.applies) {
			gap = S.law.complex.short > 0 ? t("gap_two_thirds", { n: N(S.law.complex.short) }) : t("gap_two_thirds_ok");
		} else { gap = esc(t("tama_note")); }
		var mix = "";
		ST.forEach(function (k) { if (c[k]) { mix += '<span class="' + CLS[k] + '" style="flex:' + c[k] + '" title="' + esc(stLabel(k) + ": " + c[k]) + '"></span>'; } });
		var h = '<div class="rrp-consent__top"><div><span class="rrp-note">' + esc(t("signed_of_all")) + '</span><div class="rrp-consent__big num"><span dir="ltr">' + Math.round(pct(c.yes, c.total)) + "%</span></div>" +
			'<div class="rrp-note">' + t("yes_of", { y: N(c.yes), n: N(c.total) }) + '</div></div><div class="rrp-gap">' + gap + "</div></div>";
		h += '<div class="rrp-mix" role="img" aria-label="' + esc(ST.map(function (k) { return stLabel(k) + " " + (c[k] || 0); }).join(", ")) + '">' + mix + "</div>";
		if (S.law && S.law.applies) { h += '<div class="rrp-mark"><u style="inset-inline-start:66.67%"></u><em style="inset-inline-start:66.67%">' + esc(t("mark_two_thirds")) + "</em></div>"; }
		h += '<div class="rrp-legend" role="group" aria-label="' + esc(t("legend_label")) + '">';
		ST.forEach(function (k) {
			if (!c[k] && st.hi !== k) { return; } /* no "0" chips (language-dna: no zero counts on visible UI) */
			h += '<button type="button" class="rrp-leg" data-hi="' + k + '" aria-pressed="' + (st.hi === k ? "true" : "false") + '"' + (caps().see_grid ? "" : " disabled") + '><i class="rrp-sw ' + CLS[k] + '"></i>' + esc(stLabel(k)) + " <b class=\"num\">" + (c[k] || 0) + "</b></button>";
		});
		h += "</div>";
		el.innerHTML = h;
	}
	function fillLaw() {
		var el = $("[data-law]"), L = st.S.law;
		if (!el || !L) { return; }
		var ok = '<span class="rrp-ok">' + esc(t("met")) + "</span>", no = function (n) { return '<span class="rrp-short">' + esc(t("short_n", { n: n })) + "</span>"; };
		var h = '<h3>' + esc(t("law_t")) + '</h3><ol class="rrp-lawlist">';
		h += "<li><div><b>" + esc(t("law_c1")) + '</b><span class="rrp-note">' + t("law_c1_d", { y: N(L.complex.yes), n: N(L.complex.total), need: N(L.complex.need) }) + "</span></div>" + (L.complex.met ? ok : no(L.complex.short)) + "</li>";
		h += "<li><div><b>" + esc(t("law_c2")) + '</b><span class="rrp-note">' + esc(t("law_c2_d")) + '</span></div><span></span><ul class="rrp-lawb">';
		L.buildings.forEach(function (b, i) {
			var r;
			if (b.rule === "not_computed") { r = '<span class="rrp-unk">' + esc(t("law_not_computed")) + "</span>"; }
			else if (b.met === true) { r = ok; }
			else if (b.met === false) { r = b.short > 0 ? no(b.short) : '<span class="rrp-short">' + esc(t("law_owners_short")) + "</span>"; }
			else { r = '<span class="rrp-unk">' + esc(t("law_owners_unknown")) + "</span>"; }
			h += "<li><span><bdi>" + esc(bName(b, i)) + "</bdi>" + ' <span class="num">' + b.yes + "/" + b.total + "</span>" + (b.need != null ? ' <small class="rrp-note">' + esc(t(b.rule === "small_building" ? "law_need_small" : "law_need", { n: b.need })) + "</small>" : "") + "</span>" + r + "</li>";
		});
		h += "</ul></li>";
		h += "<li><div><b>" + esc(t("law_c3")) + '</b><span class="rrp-note">' + esc(t("law_c3_d")) + '</span></div><span></span><ul class="rrp-lawb">';
		L.buildings.forEach(function (b, i) {
			var r = b.common.known ? (b.common.met ? ok : '<span class="rrp-short">' + esc(t("law_common_short")) + "</span>") : '<span class="rrp-unk">' + esc(t("law_common_missing", { n: b.common.missing })) + "</span>";
			h += "<li><span><bdi>" + esc(bName(b, i)) + "</bdi>" + (b.common.pct_yes != null && b.common.known ? ' <span class="num" dir="ltr">' + b.common.pct_yes + "%</span>" : "") + "</span>" + r + "</li>";
		});
		h += "</ul></li></ol>";
		h += '<p class="rrp-note">' + esc(t("law_note")) + "</p>";
		el.innerHTML = h;
	}
	function fillStage() {
		var host = $("[data-stage-host]");
		if (!host) { return; }
		$$("[data-view]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.view === st.view ? "true" : "false"); });
		if (st.view === "3d") { host.innerHTML = '<div class="rrp-3d" id="nlurd-3dhost"><div class="rrp-3dhint">' + esc(t("hint_3d")) + "</div></div>" + bPicker(); boot3d(); return; }
		if (st.view === "map") { host.innerHTML = '<div class="rrp-map" id="nlurd-map"></div><div class="rrp-mapchips" id="nlurd-mapchips"></div>'; bootMap(); return; }
		host.innerHTML = facade();
	}
	function bPicker() {
		var B = buildings();
		if (B.length < 2) { return ""; }
		return '<div class="rrp-filters rrp-bpick" role="group">' + B.map(function (b, i) { return '<button type="button" class="rrp-filter" data-bld="' + esc(b.key) + '" aria-pressed="' + ((st.bld || B[0].key) === b.key ? "true" : "false") + '">' + esc(bName(b, i)) + "</button>"; }).join("") + "</div>";
	}
	function facade() {
		var S = st.S, B = buildings(), A = S.apartments || [];
		if (!caps().see_grid || !A.length) {
			return '<p class="rrp-note">' + esc(t("grid_hidden")) + "</p>" + totalsTable();
		}
		var law = S.law && S.law.applies ? S.law.buildings : [];
		var tag = S.role === "neighbor" ? "span" : "button";
		var h = '<p class="rrp-note rrp-tap">' + esc(t(isMgr() ? "facade_hint" : S.role === "neighbor" ? "facade_hint_nb" : "facade_hint_ro")) + '</p><div class="rrp-blds">';
		B.forEach(function (b, bi) {
			var list = A.filter(function (a) { return a.building === b.key; });
			var floors = {}, maxF = 0, minF = 99, perRow = 1;
			list.forEach(function (a) { (floors[a.floor] = floors[a.floor] || []).push(a); maxF = Math.max(maxF, a.floor); minF = Math.min(minF, a.floor); });
			Object.keys(floors).forEach(function (f) { floors[f].sort(function (x, y) { return (x.pos || 0) - (y.pos || 0); }); perRow = Math.max(perRow, floors[f].length); });
			var yes = list.filter(function (a) { return shown(a) === "consented"; }).length;
			var lb = law[bi];
			h += '<figure class="rrp-bld"><div class="rrp-facade" style="grid-template-columns:20px repeat(' + perRow + ',var(--cell))">';
			for (var f = maxF; f >= minF; f--) {
				h += '<span class="rrp-flr num">' + f + "</span>";
				var row = floors[f] || [];
				for (var p = 0; p < perRow; p++) {
					var a = row[p];
					if (!a) { h += '<span class="rrp-apt-empty"></span>'; continue; }
					var s = shown(a), dim = st.hi && st.hi !== s ? " dim" : "";
					h += "<" + tag + (tag === "button" ? ' type="button" data-apt="' + esc(a.id) + '" aria-pressed="' + (st.apt === a.id ? "true" : "false") + '"' : ' role="img"') + ' class="rrp-apt ' + CLS[s] + dim + '" aria-label="' +
						esc(t("apt_aria", { b: bName(b, bi), n: a.num, f: a.floor, s: stLabel(s) })) + '"><span class="num">' + a.num + "</span></" + tag + ">";
				}
			}
			h += '</div><div class="rrp-ground"></div><figcaption><bdi>' + esc(bName(b, bi)) + (b.address ? " · " + esc(b.address) : "") + '</bdi>' + '<span>' + esc(t("b_signed", { y: yes, n: list.length })) +
				(lb && lb.met === true ? " · " + esc(t("b_35_ok")) : lb && lb.met === false && lb.short > 0 ? " · " + esc(t("b_35_short", { n: lb.short })) : "") + "</span></figcaption></figure>";
		});
		return h + "</div>";
	}
	function totalsTable() {
		var L = st.S.law, B = buildings();
		var rows = (L ? L.buildings : B.map(function (b) { return { key: b.key, label: b.label, total: 0, yes: 0 }; })).map(function (b, i) { return "<tr><td>" + esc(bName(b, i)) + '</td><td class="num">' + b.yes + "/" + b.total + "</td></tr>"; }).join("");
		return '<table class="rrp-mini"><thead><tr><th scope="col">' + esc(t("building")) + '</th><th scope="col">' + esc(t("col_signed")) + "</th></tr></thead><tbody>" + rows + "</tbody></table>";
	}
	function fillLadder() {
		var S = st.S, steps = $("[data-steps]"), card = $("[data-stagecard]");
		if (!steps) { return; }
		var open = st.stageOpen === null ? S.stage : st.stageOpen, h = "";
		(S.ladder || []).forEach(function (l, i) {
			h += '<button type="button" class="rrp-step' + (i < S.stage ? " d" : i === S.stage ? " n" : "") + '" data-stage="' + i + '" aria-pressed="' + (open === i ? "true" : "false") + '"><i class="num">' + (i + 1) + "</i><span>" + esc(l) + "</span></button>";
		});
		steps.innerHTML = h;
		var note = (S.stage_notes || [])[open] || {}, reached = "";
		(S.stage_log || []).forEach(function (l) { if (l.stage === open && !reached) { reached = l.at; } });
		var c = "<div><h4>" + (open === S.stage ? esc(t("now")) + " " : "") + esc((S.ladder || [])[open] || "") + "</h4><p>" + esc(note.desc || "") + "</p>";
		if (note.duration) { c += '<p class="rrp-dur"><span class="num">' + esc(note.duration) + "</span> · " + esc(t("avg_note")) + "</p>"; }
		if (reached) { c += '<p class="rrp-note">' + esc(t("reached_at")) + ": " + N(dmy(reached)) + "</p>"; }
		c += "</div><div><h4>" + esc(t("next_actions")) + "</h4><ul>" + (note.actions || []).map(function (a) { return "<li>" + esc(a) + "</li>"; }).join("") + "</ul>";
		if (caps().manage && open !== S.stage) { c += '<button type="button" class="rrp-btn" data-setstage="' + open + '">' + esc(t("set_stage")) + "</button>"; }
		card.innerHTML = c + "</div>";
	}
	function fillDeadlines() {
		var el = $("[data-deadlines]");
		if (!el) { return; }
		var L = st.S.deadlines || [];
		var h = "<h3>" + esc(t("dl_t")) + "</h3>";
		if (!L.length) { h += '<p class="rrp-note">' + esc(t("dl_empty")) + "</p>"; }
		else {
			h += '<ul class="rrp-dlist">' + L.map(function (d) {
				var cls = d.days < 0 ? "past" : d.days <= 30 ? "soon" : "";
				var when = d.days < 0 ? t("dl_past", { n: -d.days }) : d.days === 0 ? t("dl_today") : t("dl_in", { n: d.days });
				return '<li class="' + cls + '"><b>' + esc(d.label) + '</b><span class="num">' + esc(dmy(d.date)) + "</span><em>" + esc(when) + "</em>" + (d.note ? '<small class="rrp-note">' + esc(d.note) + "</small>" : "") +
					(caps().manage ? '<button type="button" class="rrp-x" data-dl-del="' + esc(d.id) + '" aria-label="' + esc(t("remove")) + '">×</button>' : "") + "</li>";
			}).join("") + "</ul>";
		}
		if (caps().manage) {
			h += '<form class="rrp-dlform" data-dl-form><label class="rrp-field">' + esc(t("dl_label")) + '<input type="text" data-dl="label" maxlength="80" placeholder="' + esc(t("dl_ph")) + '" required></label>' +
				'<label class="rrp-field rrp-sm">' + esc(t("dl_date")) + '<input type="date" data-dl="date" required></label><button type="submit" class="rrp-btn">' + esc(t("dl_add")) + "</button></form>";
		}
		h += '<p class="rrp-note">' + esc(t("dl_note")) + "</p>";
		el.innerHTML = h;
	}
	function fillTasks() {
		var el = $("[data-tasks]");
		if (!el) { return; }
		var S = st.S, c = counts(), L = S.law, items = [];
		items.push({ ok: !c.unreached, x: c.unreached ? t("td_reach", { n: c.unreached }) : t("td_reach_ok") });
		if (L && L.applies) {
			items.push({ ok: L.complex.met, x: L.complex.met ? t("td_23_ok") : t("td_23", { n: L.complex.short }) });
			L.buildings.forEach(function (b, i) { if (b.met === false && b.short > 0) { items.push({ ok: false, x: t("td_35", { b: bName(b, i), n: b.short }) }); } });
			var miss = L.buildings.reduce(function (s, b) { return s + (b.common.known ? 0 : b.common.missing); }, 0);
			if (miss) { items.push({ ok: false, x: t("td_common", { n: miss }) }); }
		}
		if (c.partial) { items.push({ ok: false, x: t("td_partial", { n: c.partial }) }); }
		items.push({ ok: !c.docs_missing_apts, x: c.docs_missing_apts ? t("td_docs", { n: c.docs_missing_apts }) : t("td_docs_ok") });
		items.push({ ok: !c.refused, x: c.refused ? t("td_refused", { n: c.refused }) : t("td_refused_ok") });
		(S.deadlines || []).forEach(function (d) { if (d.days != null && d.days >= 0 && d.days <= 30) { items.push({ ok: false, x: t("td_deadline", { label: d.label, n: d.days }) }); } });
		items.push({ ok: S.stage > 3, x: t("td_pros") });
		items.push({ ok: S.stage > 4, x: t("td_dev") });
		el.innerHTML = items.map(function (x) { return '<li class="' + (x.ok ? "ok" : "") + '"><i aria-hidden="true"></i><span>' + esc(x.x) + "</span></li>"; }).join("");
	}
	function fillDocs() {
		var el = $("[data-docsum]");
		if (!el) { return; }
		var R = st.S.docs_rollup || { per: {}, base: 0 }, K = st.S.doc_keys || {};
		el.innerHTML = Object.keys(K).map(function (k) {
			var have = R.per[k] || 0;
			return '<div class="rrp-docrow"><span>' + esc(K[k]) + '</span><b class="num">' + have + "/" + R.base + '</b><div class="rrp-meter"><i style="width:' + (R.base ? Math.round(have / R.base * 100) : 0) + '%"></i></div></div>';
		}).join("");
	}
	function fillMembers() {
		var el = $("[data-members]");
		if (!el) { return; }
		var S = st.S, M = S.members || [], pend = M.filter(function (m) { return m.claim_apt && !m.approved && !m.rejected; });
		var h = "<h3>" + esc(t("mem_t")) + '</h3><p class="rrp-note">' + esc(t("mem_count", { n: M.length, p: pend.length })) + "</p>";
		if (pend.length) {
			h += '<ul class="rrp-claims">' + pend.map(function (m) {
				var a = aptById(m.claim_apt), b = a ? buildings().filter(function (x) { return x.key === a.building; })[0] : null;
				return "<li><span>" + esc(t("claim_line", { who: m.email, n: a ? a.num : m.claim_apt, b: b ? bName(b, buildings().indexOf(b)) : "" })) + '</span><span class="rrp-row"><button type="button" class="rrp-btn pri" data-mem="approve" data-email="' + esc(m.email) + '">' + esc(t("approve")) +
					'</button><button type="button" class="rrp-btn" data-mem="reject" data-email="' + esc(m.email) + '">' + esc(t("reject")) + "</button></span></li>";
			}).join("") + "</ul>";
		}
		if (M.length) {
			h += '<ul class="rrp-memlist">' + M.map(function (m) {
				var a = m.approved ? aptById(m.claim_apt) : null;
				return "<li><span>" + esc(m.email) + (a ? ' · <span class="num">' + esc(t("apt_n", { n: a.num })) + "</span>" : "") + '</span><label class="rrp-note">' + esc(t("mem_role")) + ' <select data-mem-role data-email="' + esc(m.email) + '">' +
					'<option value="neighbor"' + (m.role !== "committee" ? " selected" : "") + ">" + esc(t("role_neighbor")) + '</option><option value="committee"' + (m.role === "committee" ? " selected" : "") + ">" + esc(t("role_committee")) + "</option></select></label></li>";
			}).join("") + "</ul>";
		}
		h += '<label class="rrp-check"><input type="checkbox" data-grid-setting' + ((S.settings || {}).neighbor_grid === "statuses" ? " checked" : "") + "> " + esc(t("grid_setting")) + "</label>";
		el.innerHTML = h;
	}

	/* ---------- the selected apartment ---------- */
	function ownerRow(o) {
		o = o || {};
		return '<div class="rrp-own" data-own><input type="text" data-o="n" maxlength="40" value="' + esc(o.n || "") + '" placeholder="' + esc(t("own_ph")) + '" aria-label="' + esc(t("own_name")) + '">' +
			'<input type="text" data-o="share" maxlength="12" dir="ltr" value="' + esc(o.share || "") + '" placeholder="1/2" aria-label="' + esc(t("own_share")) + '">' +
			'<label><input type="checkbox" data-o="heir"' + (o.heir ? " checked" : "") + "> " + esc(t("own_heir")) + "</label>" +
			'<label><input type="checkbox" data-o="signed"' + (o.signed ? " checked" : "") + "> " + esc(t("own_signed")) + "</label>" +
			'<button type="button" class="rrp-x" data-o-del aria-label="' + esc(t("remove")) + '">×</button></div>';
	}
	function fillDrawer(msg, events) {
		var d = $("[data-drawer]");
		if (!d) { return; }
		var a = st.apt ? aptById(st.apt) : null;
		if (!a) { d.innerHTML = "<h3>" + esc(t("apt_title")) + '</h3><p class="sub">' + esc(t(caps().see_grid ? (isMgr() ? "apt_hint" : "apt_hint_ro") : "apt_hint_hidden")) + "</p>"; return; }
		var B = buildings(), bi = 0;
		B.forEach(function (b, i) { if (b.key === a.building) { bi = i; } });
		var b = B[bi] || {}, s = shown(a), K = st.S.doc_keys || {};
		var h = "<h3>" + esc(t("apt_n", { n: a.num })) + " · " + esc(t("floor")) + " " + N(a.floor) + '</h3><p class="sub">' + esc(bName(b, bi) + (b.address ? " · " + b.address : "") + (st.S.city ? " · " + st.S.city : "")) + "</p>";
		if (!isMgr()) {
			h += '<p class="rrp-status"><i class="rrp-sw ' + CLS[s] + '"></i> ' + esc(stLabel(s)) + "</p>";
			if (a.docs) { h += '<ul class="rrp-docs ro">' + Object.keys(K).map(function (k) { return "<li>" + (a.docs[k] ? "✓ " : "· ") + esc(K[k]) + "</li>"; }).join("") + "</ul>"; }
			d.innerHTML = h + '<p class="rrp-note">' + esc(t("ro_note")) + "</p>";
			return;
		}
		if (s === "partial") { h += '<p class="rrp-warn">' + esc(t("partial_warn")) + "</p>"; }
		h += '<fieldset class="rrp-owners-ed"><legend>' + esc(t("owners_t")) + '</legend><div data-own-list>' + (a.owners || []).map(ownerRow).join("") + "</div>" +
			((a.owners || []).length < 8 ? '<button type="button" class="rrp-btn rrp-sm" data-o-add>' + esc(t("own_add")) + "</button>" : "") + '<p class="rrp-note">' + esc(t("owners_note")) + "</p></fieldset>";
		h += '<label class="rrp-field">' + esc(t("status")) + '<select data-ed="status">' + Object.keys(st.S.statuses || {}).map(function (k) { return '<option value="' + k + '"' + (k === a.consent_status ? " selected" : "") + ">" + esc(st.S.statuses[k][0]) + "</option>"; }).join("") + "</select></label>";
		h += '<ul class="rrp-docs" aria-label="' + esc(t("docs_of")) + '">' + Object.keys(K).map(function (k) { return '<li><label><input type="checkbox" data-ed-doc="' + k + '"' + (a.docs && a.docs[k] ? " checked" : "") + "> " + esc(K[k]) + "</label></li>"; }).join("") + "</ul>";
		h += '<label class="rrp-field">' + esc(t("common_l")) + '<input type="text" data-ed="common" maxlength="16" dir="ltr" value="' + esc(a.common_share || "") + '" placeholder="28/1000"></label>';
		h += '<label class="rrp-field">' + esc(t("contact_l")) + '<input type="text" data-ed="contact" maxlength="200" value="' + esc(a.contact_note || "") + '"></label>';
		h += '<label class="rrp-field">' + esc(t("note_l")) + '<textarea data-ed="note" maxlength="400">' + esc(a.note || "") + "</textarea></label>";
		if (caps().manage) { h += '<button type="button" class="rrp-btn pri rrp-wide" data-ed-save>' + esc(t("save")) + "</button>"; }
		h += '<div class="rrp-saved" data-ed-msg>' + (msg || "") + "</div>";
		h += '<p class="rrp-note">' + esc(t("version_line", { v: a.v || 0 })) + (a.updated && a.v ? " · " + esc(t("updated_on", { d: dmy(a.updated) })) : "") + "</p>";
		h += '<h4 class="rrp-logh">' + esc(t("log_t")) + '</h4><ul class="rrp-log" data-ed-log><li class="rrp-note">' + esc(t("log_loading")) + "</li></ul>";
		d.innerHTML = h;
		if (events) { paintLog(events); } else if (MODE !== "demo") {
			api("/renewal-space/" + st.S.id + "/apartment/" + encodeURIComponent(a.id) + "/log" + QS).then(function (r) { if (st.apt === a.id) { paintLog(r.events || []); } }).catch(function () { paintLog([]); });
		}
	}
	function evText(e) {
		var who = e.who || t("someone"), f = String(e.f || "");
		if (f === "status") { return t("ev_status", { who: who, from: stLabel(e.from), to: stLabel(e.to) }); }
		if (f.indexOf("doc:") === 0) { var K = st.S.doc_keys || {}; return t(e.to ? "ev_doc_on" : "ev_doc_off", { who: who, doc: K[f.slice(4)] || f.slice(4) }); }
		if (f === "owners") { return t("ev_owners", { who: who, n: (e.to || {}).n || 0, s: (e.to || {}).signed || 0 }); }
		if (f === "common") { return t("ev_common", { who: who, to: e.to || "" }); }
		if (f === "claim") { return t(e.to === "approved" ? "ev_claim_ok" : "ev_claim_no", { who: who }); }
		return t("ev_" + f, { who: who });
	}
	function paintLog(list) {
		var ul = $("[data-ed-log]");
		if (!ul) { return; }
		ul.innerHTML = list.length ? list.map(function (e) { return '<li><time class="num" dir="ltr">' + esc(dmy(e.at)) + "</time> " + esc(evText(e)) + (e.v ? ' <small class="num">v' + e.v + "</small>" : "") + "</li>"; }).join("") : '<li class="rrp-note">' + esc(t("log_empty")) + "</li>";
	}
	function collectPatch() {
		var p = { consent_status: $("[data-ed='status']").value, docs: {}, note: $("[data-ed='note']").value, contact_note: $("[data-ed='contact']").value, common_share: $("[data-ed='common']").value, owners: [] };
		$$("[data-ed-doc]").forEach(function (cb) { p.docs[cb.dataset.edDoc] = cb.checked; });
		$$("[data-own]").forEach(function (r) {
			var n = $("[data-o='n']", r).value.trim();
			if (n) { p.owners.push({ n: n, share: $("[data-o='share']", r).value.trim(), heir: $("[data-o='heir']", r).checked, signed: $("[data-o='signed']", r).checked }); }
		});
		return p;
	}
	function replaceApt(a) {
		var L = st.S.apartments || [];
		for (var i = 0; i < L.length; i++) { if (L[i].id === a.id) { L[i] = a; return; } }
	}
	function saveApt(btn) {
		var a = aptById(st.apt);
		if (!a) { return; }
		var body = collectPatch(); body.v = a.v || 0;
		btn.disabled = true;
		$("[data-ed-msg]").textContent = t("saving");
		post("/renewal-space/" + st.S.id + "/apartment/" + encodeURIComponent(a.id), body).then(function (r) {
			replaceApt(r.apartment);
			st.S.counts = r.counts; st.S.law = r.law; st.S.docs_rollup = r.docs_rollup;
			st.S.consents = { yes: r.counts.yes, total: r.counts.total, pct: r.counts.pct };
			fillConsent(); fillLaw(); if (st.view === "facade") { fillStage(); } fillTasks(); fillDocs();
			fillDrawer(esc(r.code === "unchanged" ? t("unchanged") : t("saved_v", { v: r.apartment.v })), r.events);
		}).catch(function (e) {
			var data = (e && e.data) || {};
			if (e && e._status === 409 && data.apartment) {
				replaceApt(data.apartment);
				var last = (data.last || [])[0];
				fillConsent(); if (st.view === "facade") { fillStage(); }
				fillDrawer('<span class="rrp-warn">' + esc(t("conflict", { who: last && last.who ? last.who : t("someone"), at: last ? dmy(last.at) : "" })) + "</span>");
			} else {
				btn.disabled = false;
				$("[data-ed-msg]").textContent = (e && e.message) || t("save_fail");
			}
		});
	}

	/* ---------- updates ---------- */
	function waHref(text) {
		var link = (st.S && st.S.join_url) || "";
		return "https://wa.me/?text=" + encodeURIComponent(text + (link ? "\n\n" + t("wa_tail") + " " + link : ""));
	}
	function feedText(u) { return u.auto ? u.text : u.text; }
	function vUpdates() {
		var S = st.S, ups = S.updates || [];
		var h = '<section aria-labelledby="rrp-up-h"><div class="rrp-h"><div><h2 id="rrp-up-h">' + esc(t("tab_updates")) + "</h2><p>" + esc(t("up_sub", { name: S.complex_name || S.title })) + "</p></div></div>";
		h += '<div class="rrp-up"><div>';
		if (caps().post_updates) {
			h += '<div class="rrp-panel rrp-compose"><label class="rrp-field">' + esc(t("up_new")) + '<textarea data-up-text maxlength="1000" placeholder="' + esc(t("upd_ph")) + '"></textarea></label>' +
				'<div class="rrp-row"><span class="rrp-note">' + esc(t("up_note")) + '</span><span class="rrp-row"><button class="rrp-btn pri" type="button" data-up-send>' + esc(t("upd_send")) + "</button></span></div>" +
				'<div class="rrp-saved" data-up-msg aria-live="polite"></div></div>';
		}
		h += '<div class="rrp-panel"><ul class="rrp-feed">' + (ups.length ? ups.slice(0, 30).map(function (u, i) {
			return '<li><time class="num" dir="ltr">' + esc(dmy(u.at)) + "</time>" + esc(feedText(u)) + (u.auto ? '<span class="auto">' + esc(t("auto_badge")) + "</span>" : "") +
				(caps().post_updates ? '<a class="rrp-wa" href="' + esc(waHref(u.text)) + '" target="_blank" rel="noopener" data-wa="' + i + '">' + esc(t("wa_send")) + "</a>" : "") + "</li>";
		}).join("") : '<li class="rrp-note">' + esc(t("upd_none")) + "</li>") + "</ul></div>";
		if (caps().manage) {
			h += '<div class="rrp-panel rrp-invite"><h3>' + esc(t("inv_title")) + '</h3><p class="rrp-note">' + esc(t("inv_note")) + "</p>";
			if (S.join_url) {
				h += '<code dir="ltr">' + esc(S.join_url) + '</code><div class="rrp-row"><button class="rrp-btn" type="button" data-copy>' + esc(t("copy_link")) + '</button><a class="rrp-btn pri" href="' + esc("https://wa.me/?text=" + encodeURIComponent(t("wa_invite") + " " + S.join_url)) + '" target="_blank" rel="noopener">' + esc(t("wa_share_link")) + '</a><button class="rrp-btn" type="button" data-inv>' + esc(t("inv_new")) + "</button></div>";
				h += '<p class="rrp-note">' + esc(t("inv_new_note")) + "</p>";
			} else {
				h += '<button class="rrp-btn pri" type="button" data-inv>' + esc(t("inv_btn")) + "</button>";
			}
			h += "</div>";
		}
		h += "</div>";
		if (isMgr() || MODE === "demo") {
			h += '<div><p class="rrp-note rrp-center">' + esc(t("phone_caption")) + '</p><div class="rrp-phone">' + vNeighbor(sampleNeighbor(), true) + "</div></div>";
		}
		h += "</div></section>";
		return h;
	}
	function sampleNeighbor() {
		var S = st.S, L = S.apartments || [];
		var a = L.filter(function (x) { return x.consent_status === "in_process"; })[0] || L[0];
		var c = counts();
		return {
			role: "neighbor", preview: true, title: S.title, complex_name: S.complex_name, city: S.city, buildings: S.buildings, stage: S.stage, ladder: S.ladder, law: S.law, track: S.track,
			consents: { yes: c.yes, total: c.total }, updates: (S.updates || []).slice(0, 3), doc_keys: S.doc_keys, statuses: S.statuses,
			mine: a ? [{ id: a.id, building: a.building, num: a.num, floor: a.floor, consent_status: a.consent_status, shown: shown(a), docs: a.docs || {}, owners_n: (a.owners || []).length, owners_signed: (a.owners || []).filter(function (o) { return o.signed; }).length }] : [],
			caps: { see_grid: false, claim: true }
		};
	}

	/* ---------- the neighbour's screen (also the phone preview) ---------- */
	function vNeighbor(S, preview) {
		var B = S.buildings || [], mine = (S.mine || [])[0], c = S.consents || { yes: 0, total: 0 };
		var bk = mine ? mine.building : (B[0] && B[0].key), b = B.filter(function (x) { return x.key === bk; })[0] || B[0] || {}, bi = Math.max(0, B.indexOf(b));
		var p = pct(c.yes, c.total), K = S.doc_keys || {};
		var h = '<div class="rrp-nb' + (preview ? " is-preview" : "") + '">' + (preview ? '<div class="rrp-phone__bar"></div>' : "");
		h += (preview ? "<h4>" : '<h2 class="rrp-nb__h">') + esc((b.address || S.address || S.title) + (S.city ? ", " + S.city : "")) + (preview ? "</h4>" : "</h2>");
		h += '<p class="rrp-nb__s">' + esc(t("nb_room", { name: S.complex_name || S.title })) + "</p>";
		h += '<div class="blk"><b>' + esc(t("nb_signed")) + '</b><span class="big num" dir="ltr">' + Math.round(p) + "%</span> " + '<span class="rrp-note">' + t("yes_of", { y: N(c.yes), n: N(c.total) }) + '</span><div class="rrp-meter"><i style="width:' + p + '%"></i>' +
			(S.law && S.law.applies ? '<u style="inset-inline-start:66.67%"></u>' : "") + "</div>";
		if (S.law && S.law.applies) { h += "<p>" + (S.law.complex.short > 0 ? esc(t("nb_short", { n: S.law.complex.short })) : esc(t("gap_two_thirds_ok"))) + "</p>"; }
		h += "</div>";
		h += '<div class="blk"><b>' + esc(t("nb_stage")) + "</b><p>" + esc(t("stage_of", { n: S.stage + 1 })) + ": " + esc((S.ladder || [])[S.stage] || "") + "</p>" + ladMini(S.stage, []) + "</div>";
		h += '<div class="blk"><b>' + esc(t("nb_mine")) + "</b>";
		if (mine) {
			var have = [], miss = [];
			Object.keys(K).forEach(function (k) { (mine.docs && mine.docs[k] ? have : miss).push(K[k]); });
			h += "<p>" + esc(t("apt_n", { n: mine.num }) + " · " + t("floor") + " " + mine.floor + (B.length > 1 ? " · " + bName(b, bi) : "")) + "</p>";
			h += '<p class="rrp-status"><i class="rrp-sw ' + CLS[mine.shown || mine.consent_status] + '"></i> ' + esc(stLabel(mine.shown || mine.consent_status)) + "</p>";
			if (mine.owners_n) { h += '<p class="rrp-note">' + esc(t("nb_owners", { n: mine.owners_n, s: mine.owners_signed })) + "</p>"; }
			h += "<p>" + (!miss.length ? '<span class="ok">' + esc(t("nb_full")) + "</span>" : (have.length ? '<span class="ok">' + esc(t("nb_have")) + " " + esc(have.join(", ")) + "</span><br>" : "") + '<span class="miss">' + esc(t("nb_miss")) + " " + esc(miss.join(", ")) + "</span>") + "</p>";
		} else if (preview) {
			h += '<p class="rrp-note">' + esc(t("nb_claim_hint")) + "</p>";
		} else if (S.my_claim && S.my_claim.state === "pending") {
			h += "<p>" + esc(t("nb_pending", { n: claimNum(S, S.my_claim.apt) })) + "</p>";
		} else {
			if (S.my_claim && S.my_claim.state === "rejected") { h += '<p class="miss">' + esc(t("nb_rejected")) + "</p>"; }
			h += claimForm(S);
		}
		h += "</div>";
		if (!preview && S.caps && S.caps.see_grid && (S.apartments || []).length) { h += '<div class="blk rrp-nbgrid">' + facade() + "</div>"; }
		var ups = (S.updates || []).slice(0, preview ? 1 : 8);
		h += '<div class="blk"><b>' + esc(t(preview ? "nb_last" : "nb_updates")) + "</b>" + (ups.length ? ups.map(function (u) { return '<p><time class="num" dir="ltr">' + esc(dmy(u.at)) + "</time> " + esc(u.text) + "</p>"; }).join("") : "<p>" + esc(t("upd_none")) + "</p>") + "</div>";
		h += '<p class="rrp-note">' + esc(t("nb_privacy")) + "</p></div>";
		return h;
	}
	function claimNum(S, id) {
		var o = S.claim_options || {}, n = id;
		Object.keys(o).forEach(function (k) { o[k].forEach(function (x) { if (x.id === id) { n = x.num; } }); });
		return n;
	}
	function claimForm(S) {
		var o = S.claim_options || {}, B = S.buildings || [];
		var h = '<form class="rrp-claim" data-claim-form><p>' + esc(t("nb_claim_q")) + "</p>";
		h += '<label class="rrp-field">' + esc(t("apt_title")) + '<select data-claim-apt required><option value="">' + esc(t("choose")) + "</option>";
		B.forEach(function (b, i) {
			var L = o[b.key] || [];
			h += '<optgroup label="' + esc(bName(b, i) + (b.address ? " · " + b.address : "")) + '">' + L.map(function (x) { return '<option value="' + esc(x.id) + '">' + esc(t("apt_n", { n: x.num }) + " · " + t("floor") + " " + x.floor) + "</option>"; }).join("") + "</optgroup>";
		});
		h += '</select></label><button type="submit" class="rrp-btn pri">' + esc(t("nb_claim_send")) + '</button><p class="rrp-note">' + esc(t("nb_claim_note")) + "</p></form>";
		return h;
	}
	function afterNeighbor() { /* nothing to boot: the neighbour screen is static */ }

	/* ---------- report ---------- */
	function vReport() {
		var S = st.S, c = counts(), L = S.law, B = buildings(), org = (st.P && st.P.org) || S.org;
		var rows = "", A = S.apartments || [];
		B.forEach(function (b, i) {
			var k = { consented: 0, partial: 0, in_process: 0, missing_docs: 0, refused: 0, unreached: 0 }, list = A.filter(function (a) { return a.building === b.key; });
			list.forEach(function (a) { k[shown(a)]++; });
			var lb = L && L.applies ? L.buildings[i] : null;
			var f35 = lb ? (lb.met === true ? t("met") : lb.met === false ? t("short_n", { n: lb.short || 0 }) : t("unknown")) : "";
			rows += "<tr><td>" + esc(bName(b, i) + (b.address ? " · " + b.address : "")) + "</td><td>" + list.length + "</td><td>" + k.consented + "</td><td>" + (k.partial + k.in_process + k.missing_docs) + "</td><td>" + k.refused + "</td><td>" + k.unreached + "</td>" + (L && L.applies ? "<td>" + esc(f35) + "</td>" : "") + "</tr>";
		});
		rows += '<tr class="sum"><td>' + esc(t("total")) + "</td><td>" + c.total + "</td><td>" + c.consented + "</td><td>" + ((c.partial || 0) + c.in_process + c.missing_docs) + "</td><td>" + c.refused + "</td><td>" + c.unreached + "</td>" + (L && L.applies ? "<td>" + esc(L.complex.met ? t("met") : t("short_n", { n: L.complex.short })) + "</td>" : "") + "</tr>";
		var mix = "";
		ST.forEach(function (k) { if (c[k]) { mix += '<span class="' + CLS[k] + '" style="flex:' + c[k] + '"></span>'; } });
		var recent = (S.updates || []).filter(function (u) { return !u.auto && daysSince(u.at) <= 31; }).slice(0, 5);
		var dl = (S.deadlines || []).filter(function (d) { return d.days != null && d.days >= 0; }).slice(0, 4);
		var R = S.docs_rollup || { per: {}, base: 0 }, K = S.doc_keys || {};
		var h = '<section aria-label="' + esc(t("tab_report")) + '"><div class="rrp-reptools"><button class="rrp-btn pri" type="button" data-print>' + esc(t("print")) + "</button>" + (isMgr() ? '<button class="rrp-btn" type="button" data-csv>' + esc(t("csv")) + "</button>" : "") + "</div>";
		h += '<article class="rrp-rep"><header class="rrp-rep__h"><div><h2>' + esc(t("rep_t", { name: S.complex_name || S.title })) + "</h2><p>" + esc((S.street_line || (B[0] && B[0].address) || "") + (S.city ? ", " + S.city : "") + " · " + trackLabel(S.track) + " · " + t("stage_of", { n: S.stage + 1 }) + ": " + ((S.ladder || [])[S.stage] || "")) + "</p>" +
			"<p>" + esc(org ? t("rep_by", { org: org.name }) : t("rep_by_room")) + '</p></div><div class="stamp">' + esc(t("as_of")) + " " + N(dmy(TODAY)) + ((S.is_demo || S.is_sample) ? "<br>" + esc(t("demo_badge")) : "") + "</div></header>";
		h += "<h3>" + esc(t("rep_consents")) + "</h3><p>" + t("rep_consents_p", { y: "<b class=\"num\">" + c.yes + "</b>", n: "<b class=\"num\">" + c.total + "</b>", p: Math.round(pct(c.yes, c.total)) }) + (c.partial ? " " + esc(t("rep_partial", { n: c.partial })) : "") + "</p>";
		h += '<div class="rrp-mix">' + mix + "</div>";
		h += '<div class="rrp-tblwrap"><table><thead><tr><th scope="col">' + esc(t("building")) + '</th><th scope="col">' + esc(t("kpi_apt")) + '</th><th scope="col">' + esc(stLabel("consented")) + '</th><th scope="col">' + esc(t("rep_inproc")) +
			'</th><th scope="col">' + esc(stLabel("refused")) + '</th><th scope="col">' + esc(stLabel("unreached")) + "</th>" + (L && L.applies ? '<th scope="col">' + esc(t("rep_35")) + "</th>" : "") + "</tr></thead><tbody>" + rows + "</tbody></table></div>";
		if (L && L.applies) {
			h += "<h3>" + esc(t("law_t")) + "</h3><ol><li>" + esc(t("law_c1")) + ": " + esc(L.complex.met ? t("met") : t("short_n", { n: L.complex.short })) + " (" + L.complex.yes + "/" + L.complex.total + ", " + esc(t("law_need", { n: L.complex.need })) + ")</li>";
			h += "<li>" + esc(t("law_c2")) + ": " + esc(L.buildings.map(function (b, i) { return bName(b, i) + " " + (b.met === true ? t("met") : b.met === false ? t("short_n", { n: b.short || 0 }) : t("unknown")); }).join(" · ")) + "</li>";
			h += "<li>" + esc(t("law_c3")) + ": " + esc(L.buildings.map(function (b, i) { return bName(b, i) + " " + (b.common.known ? (b.common.met ? t("met") : t("law_common_short")) : t("law_common_missing", { n: b.common.missing })); }).join(" · ")) + "</li></ol>";
		} else { h += '<p class="rrp-note">' + esc(t("tama_note")) + "</p>"; }
		h += "<h3>" + esc(t("docs_title")) + "</h3><ul>" + Object.keys(K).map(function (k) { return "<li>" + esc(K[k]) + ": " + N((R.per[k] || 0) + "/" + R.base) + "</li>"; }).join("") + "</ul>";
		if (dl.length) { h += "<h3>" + esc(t("dl_t")) + "</h3><ul>" + dl.map(function (d) { return "<li>" + esc(d.label) + ": " + N(dmy(d.date)) + " (" + esc(t("dl_in", { n: d.days })) + ")</li>"; }).join("") + "</ul>"; }
		h += "<h3>" + esc(t("rep_month")) + "</h3>" + (recent.length ? "<ol>" + recent.map(function (u) { return "<li>" + esc(u.text) + ' <span class="num">(' + esc(dmy(u.at).split(" ")[0]) + ")</span></li>"; }).join("") + "</ol>" : '<p class="rrp-note">' + esc(t("rep_month_none")) + "</p>");
		h += "<h3>" + esc(t("next_actions")) + "</h3><ol>" + (((S.stage_notes || [])[S.stage] || {}).actions || []).map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ol>";
		h += '<div class="rrp-rep__f">' + esc(t("rep_foot")) + "</div></article></section>";
		return h;
	}
	function csv() {
		var S = st.S, B = buildings(), K = S.doc_keys || {}, q = function (v) { return '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"'; };
		var head = [t("building"), t("f_b_addr"), t("floor"), t("apt_title"), t("status"), t("csv_counted"), t("owners_t")].concat(Object.keys(K).map(function (k) { return K[k]; })).concat([t("common_l"), t("note_l"), t("csv_updated")]);
		var lines = [head.map(q).join(",")];
		(S.apartments || []).forEach(function (a) {
			var b = B.filter(function (x) { return x.key === a.building; })[0] || {}, bi = B.indexOf(b);
			lines.push([bName(b, bi), b.address || "", a.floor, a.num, stLabel(shown(a)), shown(a) === "consented" ? "1" : "0",
				(a.owners || []).map(function (o) { return o.n + (o.share ? " " + o.share : "") + (o.heir ? " (" + t("own_heir") + ")" : "") + (o.signed ? " ✓" : ""); }).join("; ")]
				.concat(Object.keys(K).map(function (k) { return a.docs && a.docs[k] ? "1" : "0"; })).concat([a.common_share || "", a.note || "", a.updated || ""]).map(q).join(","));
		});
		var blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
		var link = document.createElement("a");
		link.href = URL.createObjectURL(blob);
		link.download = "renewal-" + S.id + "-" + TODAY + ".csv";
		document.body.appendChild(link); link.click();
		setTimeout(function () { URL.revokeObjectURL(link.href); link.remove(); }, 500);
	}

	/* ---------- 3D (the v2 room's generic building, kept one tap away) ---------- */
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
		var B = buildings(), bk = st.bld || (B[0] && B[0].key);
		var list = (st.S.apartments || []).filter(function (a) { return a.building === bk; });
		var fls = (B.filter(function (b) { return b.key === bk; })[0] || {}).floors || st.S.floors || 4;
		var build = function () {
			if (!document.getElementById("nlurd-3dhost")) { return; }
			var mv = document.createElement("model-viewer");
			mv.setAttribute("src", GLB);
			mv.setAttribute("camera-controls", ""); mv.setAttribute("interaction-prompt", "none");
			mv.setAttribute("environment-image", "neutral"); mv.setAttribute("exposure", "0.95");
			mv.setAttribute("shadow-intensity", "0.5"); mv.setAttribute("touch-action", "pan-y");
			mv.setAttribute("camera-target", "0 " + Math.min(20, fls * FH * 0.45).toFixed(1) + " 0");
			mv.setAttribute("camera-orbit", "-28deg 76deg " + Math.max(40, fls * FH * 1.6).toFixed(0) + "m");
			mv.setAttribute("min-camera-orbit", "auto 48deg 26m");
			mv.setAttribute("max-camera-orbit", "auto 86deg 90m");
			list.forEach(function (a) {
				var b = document.createElement("button");
				b.setAttribute("slot", "hotspot-" + a.id);
				b.setAttribute("data-position", aptPos(a));
				var v = DIRV[a.dir] || [-1, 0];
				b.setAttribute("data-normal", v[0] + " 0 " + v[1]);
				b.setAttribute("data-visibility-attribute", "visible");
				b.className = "nlur-apt rrp-dot " + CLS[shown(a)];
				b.textContent = a.num; b.title = t("apt_n", { n: a.num }) + " · " + stLabel(shown(a));
				b.addEventListener("click", function () { st.apt = a.id; fillDrawer(); });
				mv.appendChild(b);
			});
			var hint = host.querySelector(".rrp-3dhint");
			host.insertBefore(mv, host.firstChild);
			mv.addEventListener("load", function () { if (hint) { hint.classList.add("is-off"); } });
		};
		if (window.customElements && customElements.get("model-viewer")) { build(); return; }
		var s = document.createElement("script"); s.type = "module";
		s.src = "https://unpkg.com/@google/model-viewer@3.5.0/dist/model-viewer.min.js";
		s.onload = build; document.head.appendChild(s);
	}

	/* ---------- map (the v2 room's city map, kept one tap away) ---------- */
	function bootMap() {
		var S = st.S, token = D.mapbox || "";
		var cent = S.centroid && S.centroid.length === 2 ? S.centroid : null;
		if (!token || (!cent && !S.city)) { return; }
		var chips = document.getElementById("nlurd-mapchips"), ch = "";
		if (S.city) { ch += '<a class="rrp-chip" href="' + esc(D.maplink || "#") + '">' + esc(S.city) + "</a>"; }
		if (typeof S.compounds_in_city === "number" && S.compounds_in_city > 0) { ch += '<a class="rrp-chip" href="' + esc(D.maplink || "#") + '">' + esc(t("compounds")) + ": " + S.compounds_in_city + "</a>"; }
		chips.innerHTML = ch;
		var addr = (buildings()[0] || {}).address || S.address;
		function start() {
			if (!document.getElementById("nlurd-map")) { return; }
			mapboxgl.accessToken = token;
			var center = cent ? [cent[0], cent[1]] : [34.9, 32.0];
			map = new mapboxgl.Map({ container: "nlurd-map", style: "mapbox://styles/mapbox/light-v11", center: center, zoom: cent ? 12 : 7, cooperativeGestures: true, attributionControl: true });
			map.addControl(new mapboxgl.NavigationControl());
			function place(lnglat, precise) {
				var el = document.createElement("div"); el.className = "rrp-pin";
				mapMarker = new mapboxgl.Marker({ element: el, anchor: "bottom" }).setLngLat(lnglat)
					.setPopup(new mapboxgl.Popup({ offset: 18 }).setHTML("<b>" + esc(addr || S.title) + "</b><br>" + esc(S.city) + "<br>" + esc(t("gauge")) + ": " + Math.round(pct(counts().yes, counts().total)) + "%" + (precise ? "" : "<br><i>" + esc(t("map_approx")) + "</i>"))).addTo(map);
				map.flyTo({ center: lnglat, zoom: precise ? 15.4 : 12.4, essential: true });
			}
			/* the sample rooms never geocode their made-up address: the pin stays at the city, marked approximate (HAD-396) */
			if (addr && S.city && !S.is_demo && !S.is_sample) {
				fetch("https://api.mapbox.com/geocoding/v5/mapbox.places/" + encodeURIComponent(addr + ", " + S.city + ", Israel") + ".json?access_token=" + token + "&country=il&limit=1&language=he")
					.then(function (r) { return r.json(); })
					.then(function (g) { if (g && g.features && g.features[0] && g.features[0].relevance > 0.6) { place(g.features[0].center, true); } else if (cent) { place(center, false); } })
					.catch(function () { if (cent) { place(center, false); } });
			} else if (cent) { place(center, false); }
		}
		if (window.mapboxgl) { start(); return; }
		var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css"; document.head.appendChild(l);
		var s = document.createElement("script"); s.src = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"; s.onload = start; document.head.appendChild(s);
	}

	/* ---------- events ---------- */
	root.addEventListener("click", function (e) {
		var x, el = e.target;
		if ((x = el.closest("[data-tab]"))) { show(x.dataset.tab); return; }
		if ((x = el.closest("[data-open]"))) { loadSpace(+x.dataset.open, "complex").then(function () { window.scrollTo(0, root.getBoundingClientRect().top + window.scrollY - 8); }).catch(fail); return; }
		if ((x = el.closest("[data-pf]"))) { st.pf = x.dataset.pf; show("portfolio"); return; }
		if ((x = el.closest("[data-newcx]"))) { st.newcx = !st.newcx; show("portfolio"); return; }
		if ((x = el.closest("[data-nb-add]"))) { var l = $("[data-nb-list]"); if ($$("[data-nb-row]", l).length < 12) { l.insertAdjacentHTML("beforeend", bRow($$("[data-nb-row]", l).length)); } return; }
		if ((x = el.closest("[data-view]"))) { st.view = x.dataset.view; fillStage(); return; }
		if ((x = el.closest("[data-bld]"))) { st.bld = x.dataset.bld; fillStage(); return; }
		if ((x = el.closest("[data-apt]"))) {
			if (!caps().see_grid) { return; }
			st.apt = x.dataset.apt;
			$$("[data-apt]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.apt === st.apt ? "true" : "false"); });
			fillDrawer();
			if (window.innerWidth < 1000) { var dr = $("[data-drawer]"); if (dr) { dr.scrollIntoView({ behavior: "smooth", block: "start" }); } }
			return;
		}
		if ((x = el.closest("[data-hi]"))) { st.hi = st.hi === x.dataset.hi ? null : x.dataset.hi; fillConsent(); if (st.view === "facade") { fillStage(); } return; }
		if ((x = el.closest("[data-stage]"))) { st.stageOpen = +x.dataset.stage; fillLadder(); return; }
		if ((x = el.closest("[data-setstage]"))) {
			x.disabled = true;
			post("/renewal-space/" + st.S.id + "/stage", { stage: +x.dataset.setstage }).then(function (d) { st.S = d; st.stageOpen = null; show("complex"); }).catch(function () { x.disabled = false; });
			return;
		}
		if ((x = el.closest("[data-o-add]"))) { var ol = $("[data-own-list]"); if ($$("[data-own]", ol).length < 8) { ol.insertAdjacentHTML("beforeend", ownerRow({})); $$("[data-own]", ol).pop().querySelector("input").focus(); } return; }
		if ((x = el.closest("[data-o-del]"))) { x.closest("[data-own]").remove(); return; }
		if ((x = el.closest("[data-ed-save]"))) { saveApt(x); return; }
		if ((x = el.closest("[data-dl-del]"))) { post("/renewal-space/" + st.S.id + "/deadline", { action: "remove", did: x.dataset.dlDel }).then(function (d) { st.S = d; fillDeadlines(); fillTasks(); }); return; }
		if ((x = el.closest("[data-mem]"))) { post("/renewal-space/" + st.S.id + "/member", { email: x.dataset.email, action: x.dataset.mem }).then(function (d) { st.S = d; fillMembers(); }); return; }
		if ((x = el.closest("[data-up-send]"))) {
			var ta = $("[data-up-text]"), v = ta.value.trim();
			if (!v) { ta.focus(); return; }
			x.disabled = true;
			post("/renewal-space/" + st.S.id + "/update", { text: v }).then(function (d) {
				st.S = d; show("updates");
				var m = $("[data-up-msg]");
				if (m) { m.innerHTML = esc(t("up_done")) + ' <a class="rrp-wa" href="' + esc(waHref(v)) + '" target="_blank" rel="noopener">' + esc(t("wa_send")) + "</a>"; }
			}).catch(function () { x.disabled = false; });
			return;
		}
		if ((x = el.closest("[data-inv]"))) {
			api("/renewal-space/" + st.S.id + "/invite", { method: "POST" }).then(function (d) { st.S.join_url = d.join_url; show("updates"); });
			return;
		}
		if ((x = el.closest("[data-copy]"))) { try { navigator.clipboard.writeText(st.S.join_url); } catch (er) { /* clipboard optional */ } x.textContent = t("copied"); return; }
		if ((x = el.closest("[data-print]"))) { window.print(); return; }
		if ((x = el.closest("[data-csv]"))) { csv(); return; }
	});
	root.addEventListener("change", function (e) {
		var el = e.target;
		if (el.matches("[data-cx-pick]")) { loadSpace(+el.value, "complex").catch(fail); return; }
		if (el.matches("[data-mem-role]")) { post("/renewal-space/" + st.S.id + "/member", { email: el.dataset.email, action: el.value }).then(function (d) { st.S = d; fillMembers(); }); return; }
		if (el.matches("[data-grid-setting]")) { post("/renewal-space/" + st.S.id + "/settings", { neighbor_grid: el.checked ? "statuses" : "totals" }).then(function (d) { st.S = d; fillMembers(); }); }
	});
	root.addEventListener("submit", function (e) {
		var f = e.target;
		if (f.matches("[data-dl-form]")) {
			e.preventDefault();
			post("/renewal-space/" + st.S.id + "/deadline", { label: $("[data-dl='label']", f).value, date: $("[data-dl='date']", f).value }).then(function (d) { st.S = d; fillDeadlines(); fillTasks(); });
			return;
		}
		if (f.matches("[data-claim-form]")) {
			e.preventDefault();
			var v = $("[data-claim-apt]", f).value;
			if (!v) { return; }
			post("/renewal-space/" + st.S.id + "/claim", { apt: v }).then(function (d) { st.S = d; show(null); });
			return;
		}
		if (f.matches("[data-newcx-form]")) {
			e.preventDefault();
			var g = function (k) { return $("[data-nc='" + k + "']", f).value; };
			var bl = $$("[data-nb-row]", f).map(function (r) { return { label: $("[data-nb='label']", r).value, address: $("[data-nb='address']", r).value, floors: +$("[data-nb='floors']", r).value, upf: +$("[data-nb='upf']", r).value }; });
			$("[data-nc-msg]", f).textContent = t("opening");
			post("/renewal-space", { org_id: +st.org || 0, name: g("name"), city: g("city"), track: g("track"), buildings: bl, address: bl[0] ? bl[0].address : "" }).then(function (d) {
				st.newcx = false;
				return loadPortfolio(null).then(function () { return loadSpace(d.id, "complex"); });
			}).catch(function (er) { $("[data-nc-msg]", f).textContent = (er && er.message) || t("save_fail"); });
		}
	});
	root.addEventListener("keydown", function (e) {
		var r = e.target.closest && e.target.closest("tr[data-open]");
		if (r && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); r.click(); }
	});

	boot();
})();
