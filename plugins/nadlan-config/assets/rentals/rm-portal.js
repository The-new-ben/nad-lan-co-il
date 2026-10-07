/* ============================================================================
   NADLAN RENTALS v2 - the link pages (HAD-383, 1.10.2026)
   Opened from a WhatsApp link, no password: #t= tenant · #s= sign ·
   #a= apply · #v= professional · #q= the landlord's quick link.
   The token never leaves the fragment except in the X-NLRM-Link header,
   so a link preview cannot see or use it.
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM, esc = N.esc, I = N.icon, t = function (k, v) { return N.t(k, v); };
	var P = { token: "", purpose: "", data: null, rest: "", root: null, cfg: {} };
	var KIND = { t: "tenant", s: "sign", a: "apply", v: "vendor", q: "owner" };

	N.portalToken = function () {
		var m = /^#([tsavq])=([A-Za-z0-9_\-]{20,80})/.exec(location.hash || "");
		if (m) {
			try { sessionStorage.setItem("nlrm_link", m[1] + "=" + m[2]); } catch (e) { /* private mode */ }
			try { history.replaceState(null, "", location.pathname + location.search + "#" + m[1] + "=" + m[2]); } catch (e) { /* sandbox */ }
			return { kind: KIND[m[1]], token: m[2] };
		}
		return null;
	};

	function call(path, opts) {
		opts = opts || {};
		opts.headers = Object.assign({ "X-NLRM-Link": P.token, "X-NLRM-Lang": N.lang }, opts.body && !(opts.body instanceof FormData) ? { "Content-Type": "application/json" } : {});
		opts.credentials = "omit";
		return fetch(P.rest + path, opts).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) { var e = new Error(j.message || "HTTP " + r.status); e.status = r.status; throw e; } return j; }); });
	}
	function act(name, data) { return call("/rm/portal/act", { method: "POST", body: JSON.stringify({ act: name, data: data }) }); }
	function upload(file, kind, extra) {
		var f = new FormData(); f.append("file", file); f.append("kind", kind || "photo");
		Object.keys(extra || {}).forEach(function (k) { f.append(k, extra[k]); });
		return call("/rm/portal/doc", { method: "POST", body: f });
	}
	/* shrink a phone photo before upload: 1600px, JPEG 0.82; EXIF (incl. GPS) is dropped by the canvas */
	function shrink(file) {
		if (!file || !/^image\//.test(file.type) || /heic/i.test(file.type)) { return Promise.resolve(file); }
		return new Promise(function (res) {
			var img = new Image(), url = URL.createObjectURL(file);
			img.onload = function () {
				var k = Math.min(1, 1600 / Math.max(img.width, img.height)), c = document.createElement("canvas");
				c.width = Math.round(img.width * k); c.height = Math.round(img.height * k);
				c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
				c.toBlob(function (b) { URL.revokeObjectURL(url); res(b ? new File([b], (file.name || "photo").replace(/\.\w+$/, "") + ".jpg", { type: "image/jpeg" }) : file); }, "image/jpeg", 0.82);
			};
			img.onerror = function () { res(file); };
			img.src = url;
		});
	}

	N.mountPortal = function (el, cfg, link) {
		P.root = el; P.cfg = cfg; P.rest = cfg.rest; P.token = link.token; P.purpose = link.kind;
		N.STR = cfg.strings; N.MSG = cfg.msg;
		el.classList.add("nlrm-app", "nlrm-portal");
		el.innerHTML = '<p class="nlrm-empty">' + esc(N.t("loading")) + "</p>";
		call("/rm/portal").then(function (d) {
			P.data = d;
			var lang = (d.tenant && d.tenant.lang) || cfg.lang || "he";
			try { var pick = sessionStorage.getItem("nlrm_plang"); if (pick && cfg.strings[pick]) { lang = pick; } } catch (e) { /* private */ }
			setLang(lang);
		}).catch(function (e) {
			N.setStrings(cfg.lang || "he", cfg.strings[cfg.lang || "he"]);
			el.setAttribute("dir", N.rtl ? "rtl" : "ltr");
			el.innerHTML = '<div class="nlrm-card nlrm-empty" style="margin-top:24px"><h2 style="font-size:22px">' + esc(N.t("p_dead_title")) + "</h2><p>" + esc(e.message || N.t("p_dead")) + "</p></div>";
		});
	};
	function setLang(lang) {
		N.setStrings(lang, P.cfg.strings[lang] || P.cfg.strings.he);
		P.root.setAttribute("dir", N.rtl ? "rtl" : "ltr"); P.root.setAttribute("lang", lang);
		try { sessionStorage.setItem("nlrm_plang", lang); } catch (e) { /* private */ }
		render();
	}
	function langSwitch() {
		return '<div class="nlrm-lang" role="group" aria-label="' + esc(t("language")) + '">' + Object.keys(P.cfg.strings).map(function (l) { return '<button type="button" data-plang="' + l + '" aria-current="' + (l === N.lang) + '" lang="' + l + '">' + esc(P.cfg.strings[l].lang_name || l) + "</button>"; }).join("") + "</div>";
	}
	function head(title, sub) {
		return '<header class="nlrm-top"><div class="nlrm-brand"><b>' + esc(title) + "</b>" + (sub ? "<small>" + esc(sub) + "</small>" : "") + "</div>" + langSwitch() + "</header>";
	}
	function render() {
		var d = P.data, h = "";
		if (P.purpose === "tenant" || P.purpose === "sign") { h = tenantView(d); }
		else if (P.purpose === "apply") { h = applyView(d); }
		else if (P.purpose === "vendor") { h = vendorView(d); }
		else if (P.purpose === "owner") { h = ownerView(d); }
		P.root.innerHTML = h + '<p class="nlrm-note" style="text-align:center;margin:24px 0">' + esc(t("p_footer", { until: N.dateText(d.expires_at) })) + "</p>";
		wire();
	}

	/* ---------- the tenant ---------- */
	function tenantView(d) {
		var p = d.property || {}, u = d.unit || {}, l = d.lease || {}, ll = d.landlord || {}, bal = Math.round((d.balance || 0) / 100);
		var next = (d.ledger || []).filter(function (r) { return r.kind === "charge" && (r.status === "open" || r.status === "partial"); }).sort(function (a, b) { return a.due_date < b.due_date ? -1 : 1; })[0];
		var h = head(t("p_home_title", { address: p.address || "" }), [u.label, p.city].filter(Boolean).join(" · "));
		if (d.tenant) { h += '<p class="nlrm-lead">' + esc(t("p_hello", { name: (d.tenant.name || "").split(" ")[0], landlord: ll.name || t("the_landlord") })) + "</p>"; }
		var signed = ((l.signing || {}).parties || []).length > 0;
		if (P.purpose === "sign" || (!signed && l.doc)) { h += signBlock(l); }
		h += '<section class="nlrm-card"><h3>' + I("money", 20) + esc(t("p_pay_title")) + " " + (bal > 0 ? N.chip("due", t("owes", { amount: N.moneyText(bal) })) : N.chip("ok", t("paid_up"))) + "</h3>";
		h += '<dl class="nlrm-facts"><div><dt>' + esc(t("f_rent")) + "</dt><dd>" + N.money(l.rent) + " " + esc(t("per_month")) + "</dd></div><div><dt>" + esc(t("f_payday")) + "</dt><dd>" + esc(t("payday_n", { n: l.pay_day })) + "</dd></div>" + (next ? "<div><dt>" + esc(t("p_next")) + "</dt><dd>" + N.ag(next.amount) + " · " + N.date(next.due_date) + "</dd></div>" : "") + "</dl>";
		var pay = ll.pay || {};
		if (pay.bank || pay.bit || pay.link) {
			h += '<div class="nlrm-hint" style="margin-top:12px"><b>' + esc(t("p_how_pay")) + "</b>" + (pay.bank ? "<br>" + esc(pay.bank) : "") + (pay.bit ? "<br>" + esc(t("p_bit", { bit: N.phoneShow(pay.bit) })) : "") + (pay.link ? '<br><a href="' + esc(pay.link) + '" target="_blank" rel="noopener">' + esc(t("p_pay_link")) + "</a>" : "") + "</div>";
		}
		h += '<div class="nlrm-tools" style="margin-top:12px"><button type="button" class="nlrm-btn nlrm-btn--primary" data-p="paid">' + I("check", 18) + esc(t("p_i_paid")) + "</button></div>";
		var pays = (d.ledger || []).filter(function (r) { return r.kind === "payment"; }).slice(0, 6);
		if (pays.length) { h += '<ul class="nlrm-list" style="margin-top:10px">' + pays.map(function (r) { return '<li class="nlrm-item"><div class="nlrm-item-main"><b>' + N.ag(r.amount) + "</b><small>" + N.date(r.paid_date) + " · " + esc(t("m_" + (r.method || "transfer"))) + "</small></div>" + N.chip(r.status === "pending" ? "info" : "ok", t("ls_" + r.status)) + "</li>"; }).join("") + "</ul>"; }
		h += "</section>";
		h += '<section class="nlrm-card"><h3>' + I("wrench", 20) + esc(t("p_repair_title")) + '</h3><p class="nlrm-lead">' + esc(t("p_repair_lead")) + '</p><button type="button" class="nlrm-btn nlrm-btn--primary" data-p="ticket">' + I("plus", 18) + esc(t("p_repair_btn")) + "</button>";
		if ((d.tickets || []).length) { h += '<ul class="nlrm-list" style="margin-top:10px">' + d.tickets.slice().reverse().map(function (x) { return '<li class="nlrm-item"><div class="nlrm-item-main"><b>' + esc(x.title) + "</b><small>" + N.date((x.opened_at || "").slice(0, 10)) + (x.due_by && x.status !== "done" ? " · " + esc(t("p_fix_by", { date: N.dateText(x.due_by) })) : "") + "</small></div>" + N.chip(x.status === "done" ? "ok" : x.urgency === "urgent" ? "late" : "info", t("ts_" + x.status)) + "</li>"; }).join("") + "</ul>"; }
		h += '<p class="nlrm-note">' + esc(t("p_repair_law")) + "</p></section>";
		h += '<section class="nlrm-card"><h3>' + I("doc", 20) + esc(t("p_lease_title")) + '</h3><dl class="nlrm-facts"><div><dt>' + esc(t("f_start")) + "</dt><dd>" + N.date(l.start_date) + "</dd></div><div><dt>" + esc(t("f_end")) + "</dt><dd>" + N.date(l.end_date) + "</dd></div>" + (l.option_until ? "<div><dt>" + esc(t("f_option")) + "</dt><dd>" + N.date(l.option_until) + "</dd></div>" : "") + "<div><dt>" + esc(t("f_linkage")) + "</dt><dd>" + esc(l.linkage && l.linkage.mode === "cpi" ? t("linked_cpi", { pct: l.linkage.pct || 100 }) : t("not_linked")) + "</dd></div></dl>";
		if ((d.docs || []).length) { h += '<ul class="nlrm-list" style="margin-top:10px">' + d.docs.map(function (x) { return '<li class="nlrm-item">' + I("doc", 20) + '<div class="nlrm-item-main"><b>' + esc(x.name) + "</b><small>" + esc(t("dk_" + x.kind)) + '</small></div><button type="button" class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" data-p="doc" data-id="' + x.id + '">' + esc(t("open")) + "</button></li>"; }).join("") + "</ul>"; }
		h += '<p class="nlrm-note">' + esc(t("p_rights")) + "</p></section>";
		h += '<section class="nlrm-card"><h3>' + I("mail", 20) + esc(t("p_msg_title", { name: ll.name || t("the_landlord") })) + '</h3><div class="nlrm-tools">' + (ll.phone ? '<a class="nlrm-btn nlrm-btn--wa" href="' + esc(N.wa(ll.phone)) + '" target="_blank" rel="noopener">' + I("wa", 18) + esc(t("whatsapp")) + "</a>" : "") + '<button type="button" class="nlrm-btn nlrm-btn--secondary" data-p="message">' + esc(t("p_msg_btn")) + "</button></div></section>";
		return h;
	}
	function signBlock(l) {
		var doc = l.doc;
		if (!doc) { return ""; }
		var signed = ((l.signing || {}).parties || []);
		var h = '<section class="nlrm-card" id="nlrm-sign"><h3>' + I("sign", 20) + esc(t("p_sign_title")) + (signed.length ? " " + N.chip("ok", t("signed_n", { n: signed.length })) : "") + "</h3>";
		h += '<details' + (signed.length ? "" : " open") + '><summary class="nlrm-btn nlrm-btn--quiet">' + esc(t("p_read_lease")) + '</summary><article class="nlrm-leasedoc" dir="' + (doc.lang === "he" ? "rtl" : "ltr") + '" lang="' + doc.lang + '">' + N.leaseDocHtml(doc, signed) + "</article></details>";
		if (!signed.length) {
			h += '<form class="nlrm-form" id="nlrm-signform"><div class="nlrm-fgrid">' + N.ui.field({ name: "name", label: t("p_full_name"), required: true, autocomplete: "name", value: (P.data.tenant || {}).name || "" }) + '</div><label class="nlrm-f is-wide"><span>' + esc(t("p_sign_here")) + '</span><canvas id="nlrm-pad" width="600" height="180" style="width:100%;height:180px;background:#fbfaf7;border:1px solid #d9d5cc;border-radius:10px;touch-action:none"></canvas></label><button type="button" class="nlrm-btn nlrm-btn--quiet nlrm-btn--sm" data-p="clearpad">' + esc(t("p_clear")) + "</button>" + N.ui.field({ name: "agree", label: t("p_agree"), type: "check" }) + '<p class="nlrm-ferr" role="alert" hidden></p><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + I("sign", 18) + esc(t("p_sign_btn")) + '</button></div><p class="nlrm-note">' + esc(t("p_sign_note")) + "</p></form>";
		}
		return h + "</section>";
	}

	/* ---------- the applicant ---------- */
	function applyView(d) {
		var p = d.property || {}, u = d.unit || {}, ll = d.landlord || {};
		var h = head(t("p_apply_title", { address: p.address || "" }), [u.label, p.city].filter(Boolean).join(" · "));
		h += '<section class="nlrm-card"><dl class="nlrm-facts">' + (u.rooms ? "<div><dt>" + esc(t("f_rooms")) + "</dt><dd>" + esc(String(u.rooms)) + "</dd></div>" : "") + (u.sqm ? "<div><dt>" + esc(t("f_sqm")) + "</dt><dd>" + esc(String(u.sqm)) + "</dd></div>" : "") + (u.asking_rent ? "<div><dt>" + esc(t("f_asking")) + "</dt><dd>" + N.money(u.asking_rent) + "</dd></div>" : "") + (u.available_from ? "<div><dt>" + esc(t("f_available")) + "</dt><dd>" + N.date(u.available_from) + "</dd></div>" : "") + "</dl></section>";
		if (P.applied) {
			return h + '<section class="nlrm-card"><h3>' + I("check", 20) + esc(t("p_apply_done")) + '</h3><p class="nlrm-lead">' + esc(t("p_apply_docs")) + '</p><form class="nlrm-form" id="nlrm-appdocs"><div class="nlrm-fgrid">' + N.ui.field({ name: "kind", label: t("f_doc_kind"), type: "select", value: "payslip", options: ["payslip", "bank", "id", "other"].map(function (k) { return [k, t("dk_" + k)]; }) }) + '<label class="nlrm-f is-wide"><span>' + esc(t("f_file")) + '</span><input type="file" name="file" accept="image/*,.pdf"></label></div><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + I("upload", 18) + esc(t("upload")) + '</button></div><ul class="nlrm-list" id="nlrm-uploaded"></ul></form></section>';
		}
		h += '<section class="nlrm-card"><h3>' + esc(t("p_apply_form")) + '</h3><form class="nlrm-form" id="nlrm-apply"><div class="nlrm-fgrid">' +
			N.ui.field({ name: "name", label: t("f_name"), required: true, autocomplete: "name" }) + N.ui.field({ name: "phone", label: t("f_phone"), type: "tel", required: true, autocomplete: "tel" }) +
			N.ui.field({ name: "email", label: t("f_email"), type: "email", autocomplete: "email" }) + N.ui.field({ name: "lang", label: t("f_lang"), type: "select", value: N.lang, options: Object.keys(P.cfg.strings).map(function (l) { return [l, P.cfg.strings[l].lang_name || l]; }) }) +
			N.ui.field({ name: "household", label: t("f_household"), placeholder: t("p_household_ph") }) + N.ui.field({ name: "move_in", label: t("f_movein"), type: "date" }) +
			N.ui.field({ name: "notes", label: t("p_about"), type: "textarea" }) + N.ui.field({ name: "pets", label: t("p_pets"), type: "check" }) +
			'</div><div class="nlrm-hint" style="font-size:13.5px">' + esc(t("p_privacy", { landlord: ll.name || t("the_landlord") })) + "</div>" + N.ui.field({ name: "privacy_ok", label: t("p_privacy_ok"), type: "check" }) +
			'<p class="nlrm-ferr" role="alert" hidden></p><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + esc(t("p_apply_send")) + "</button></div></form></section>";
		return h;
	}

	/* ---------- the professional ---------- */
	function vendorView(d) {
		var x = d.ticket || {}, p = d.property || {}, u = d.unit || {}, ll = d.landlord || {}, ten = d.tenant;
		var h = head(x.title || "", [u.label, p.address, p.city].filter(Boolean).join(" · "));
		h += '<section class="nlrm-card"><dl class="nlrm-facts"><div><dt>' + esc(t("f_urgency")) + "</dt><dd>" + esc(x.urgency === "urgent" ? t("urgent") : t("standard")) + "</dd></div><div><dt>" + esc(t("f_category")) + "</dt><dd>" + esc(t("tc_" + x.category)) + "</dd></div><div><dt>" + esc(t("f_opened")) + "</dt><dd>" + N.date((x.opened_at || "").slice(0, 10)) + "</dd></div>" + (x.due_by ? "<div><dt>" + esc(t("f_due")) + "</dt><dd>" + N.date(x.due_by) + "</dd></div>" : "") + "</dl>" + (x.body ? '<p style="white-space:pre-wrap">' + esc(x.body) + "</p>" : "") + "</section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("p_contacts")) + '</h3><div class="nlrm-tools">' + (ll.phone ? '<a class="nlrm-btn nlrm-btn--wa" href="' + esc(N.wa(ll.phone)) + '" target="_blank" rel="noopener">' + I("wa", 18) + esc(t("p_landlord_wa", { name: ll.name || t("the_landlord") })) + "</a>" : "") + (ten && ten.phone ? '<a class="nlrm-btn nlrm-btn--secondary" href="tel:+' + esc(ten.phone) + '">' + I("phone", 18) + esc(t("p_tenant_call", { name: ten.name })) + "</a>" : "") + "</div></section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("p_update")) + '</h3><form class="nlrm-form" id="nlrm-vupd"><div class="nlrm-seg" role="group">' + ["scheduled", "progress", "waiting", "done"].map(function (s) { return '<button type="button" data-vst="' + s + '" aria-pressed="' + (x.status === s) + '">' + esc(t("ts_" + s)) + "</button>"; }).join("") + '</div><div class="nlrm-fgrid">' + N.ui.field({ name: "note", label: t("f_note_body"), type: "textarea" }) + N.ui.field({ name: "cost", label: t("f_cost"), type: "number" }) + '<label class="nlrm-f"><span>' + esc(t("add_photo")) + '</span><input type="file" name="file" accept="image/*"></label></div><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + esc(t("p_send_update")) + "</button></div></form></section>";
		return h;
	}

	/* ---------- the landlord's quick link ---------- */
	function ownerView(d) {
		N.store.d = Object.assign(N.store.d, d, { docs: [], events: [] });
		N.derive();
		var att = N.attention(), k = N.kpis();
		var h = head(t("app_title"), t("p_quick_sub"));
		h += '<div class="nlrm-kpis"><div class="nlrm-kpi"><span>' + esc(t("kpi_collected")) + "</span><b>" + N.money(k.collected) + "</b><small>" + t("kpi_of", { total: N.money(k.expected) }) + '</small></div><div class="nlrm-kpi"><span>' + esc(t("kpi_open")) + "</span><b>" + N.money(k.open) + "</b></div></div>";
		h += '<section class="nlrm-card"><h3>' + esc(t("att_title")) + '</h3><ul class="nlrm-list">' + (att.length ? att.slice(0, 20).map(function (a) {
			var btns = "";
			if ((a.kind === "late" || a.kind === "due") && a.lease) {
				var ch = (N.ix.ledgerByLease[a.lease.id] || []).filter(function (r) { return r.kind === "charge" && (r.status === "open" || r.status === "partial"); }).sort(function (x, y) { return x.due_date < y.due_date ? -1 : 1; })[0];
				if (ch) { btns += '<button type="button" class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" data-q="mark_paid" data-id="' + ch.id + '">' + I("check", 18) + esc(t("act_paid")) + "</button>"; }
				if (a.contact && a.contact.phone) { btns += '<a class="nlrm-btn nlrm-btn--wa nlrm-btn--sm" target="_blank" rel="noopener" href="' + esc(N.wa(a.contact.phone, N.msg("rent_reminder", a.contact.lang || "he", { name: (a.contact.name || "").split(" ")[0], month: N.monthName(N.ym(0)), unit: a.unit.label, amount: N.moneyText(N.balance(a.lease)), pay: "" }))) + '">' + I("wa", 18) + esc(t("act_remind")) + "</a>"; }
			}
			if (a.kind === "confirm") { btns += '<button type="button" class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" data-q="confirm" data-id="' + a.row.id + '">' + esc(t("act_confirm")) + "</button>"; }
			if (a.ticket) { btns += ["progress", "done"].map(function (s) { return '<button type="button" class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" data-q="ticket_status" data-id="' + a.ticket.id + '" data-st="' + s + '">' + esc(t("ts_" + s)) + "</button>"; }).join(""); }
			return '<li class="nlrm-item"><span class="nlrm-dot s' + a.s + '"></span><div class="nlrm-item-main"><b>' + esc(a.text) + '</b></div><div class="nlrm-item-acts">' + btns + "</div></li>";
		}).join("") : '<li class="nlrm-empty">' + esc(t("att_none")) + "</li>") + "</ul></section>";
		h += '<section class="nlrm-card"><h3>' + esc(t("new_expense")) + '</h3><form class="nlrm-form" id="nlrm-qexp"><div class="nlrm-fgrid">' + N.ui.field({ name: "property_id", label: t("f_property"), type: "select", options: d.properties.map(function (p) { return [p.id, p.address]; }) }) + N.ui.field({ name: "category", label: t("f_category"), type: "select", value: "repair", options: ["repair", "arnona", "vaad", "insurance", "water", "electric", "other"].map(function (c) { return [c, t("cat_" + c)]; }) }) + N.ui.field({ name: "amount", label: t("f_amount"), type: "number", required: true }) + N.ui.field({ name: "note", label: t("notes") }) + '</div><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + esc(t("save")) + "</button></div></form></section>";
		h += '<p class="nlrm-note">' + esc(t("p_quick_note")) + "</p>";
		return h;
	}

	/* ---------- wiring ---------- */
	function sheetForm(opts) { return N.ui.form(opts); }
	function wire() {
		var r = P.root;
		r.onclick = function (e) {
			var lb = e.target.closest("[data-plang]"); if (lb) { setLang(lb.dataset.plang); return; }
			var b = e.target.closest("[data-p],[data-q],[data-vst]"); if (!b) { return; }
			if (b.dataset.vst) { r.querySelectorAll("[data-vst]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); return; }
			if (b.dataset.q) {
				b.disabled = true;
				var data = b.dataset.q === "mark_paid" ? { charge_id: +b.dataset.id } : b.dataset.q === "confirm" ? { id: +b.dataset.id } : { id: +b.dataset.id, status: b.dataset.st };
				act(b.dataset.q, data).then(function () { N.ui.toast(t("saved")); return call("/rm/portal"); }).then(function (d) { P.data = d; render(); }).catch(function (ex) { b.disabled = false; N.ui.toast(ex.message, "bad"); });
				return;
			}
			var k = b.dataset.p;
			if (k === "paid") {
				sheetForm({ title: t("p_i_paid"), fields: [{ name: "amount", label: t("f_amount"), type: "number", required: true, value: Math.max(0, Math.round((P.data.balance || 0) / 100)) || P.data.lease.rent }, { name: "date", label: t("f_paid_date"), type: "date", value: N.todayIso() }, { name: "method", label: t("f_method"), type: "select", value: "transfer", options: ["transfer", "standing", "bit", "paybox", "cheque", "cash", "other"].map(function (m) { return [m, t("m_" + m)]; }) }, { name: "ref", label: t("f_ref"), hint: t("f_ref_hint") }], note: esc(t("p_paid_note")), onSubmit: function (v) {
					return act("paid", v).then(function () { N.ui.toast(t("p_paid_thanks")); return call("/rm/portal"); }).then(function (d) { P.data = d; render(); });
				} });
			}
			if (k === "ticket") {
				sheetForm({ title: t("p_repair_btn"), fields: [{ name: "title", label: t("f_ticket_title"), required: true, placeholder: t("f_ticket_ph") }, { name: "body", label: t("f_ticket_body"), type: "textarea" }, { html: '<label class="nlrm-f is-wide"><span>' + esc(t("add_photo")) + '</span><input type="file" name="photo" accept="image/*" capture="environment"></label>' }, { name: "urgency", label: t("p_urgent_q"), type: "select", value: "auto", options: [["auto", t("p_urgency_auto")], ["urgent", t("p_urgency_yes")], ["standard", t("p_urgency_no")]] }], note: esc(t("p_gas_note")), onSubmit: function (v, form) {
					var f = form.querySelector('[name="photo"]').files[0];
					return act("ticket", { title: v.title, body: v.body, urgency: v.urgency === "auto" ? "" : v.urgency }).then(function (res) {
						return f ? shrink(f).then(function (ff) { return upload(ff, "photo", { ticket_id: res.ticket.id }); }) : null;
					}).then(function () { N.ui.toast(t("p_repair_sent")); return call("/rm/portal"); }).then(function (d) { P.data = d; render(); });
				} });
			}
			if (k === "message") {
				sheetForm({ title: t("p_msg_btn"), fields: [{ name: "body", label: t("wa_text"), type: "textarea", required: true }], onSubmit: function (v) { return act("message", v).then(function () { N.ui.toast(t("p_msg_sent")); }); } });
			}
			if (k === "doc") {
				fetch(P.rest + "/rm/doc/" + b.dataset.id + "?inline=1", { headers: { "X-NLRM-Link": P.token }, credentials: "omit" }).then(function (res) { if (!res.ok) { throw new Error(t("err_generic")); } return res.blob(); }).then(function (bl) { window.open(URL.createObjectURL(bl), "_blank", "noopener"); }).catch(function (ex) { N.ui.toast(ex.message, "bad"); });
			}
			if (k === "clearpad") { var c = r.querySelector("#nlrm-pad"); c.getContext("2d").clearRect(0, 0, c.width, c.height); c.dataset.inked = ""; }
		};
		var pad = r.querySelector("#nlrm-pad");
		if (pad) { signaturePad(pad); }
		var sf = r.querySelector("#nlrm-signform");
		if (sf) {
			sf.addEventListener("submit", function (e) {
				e.preventDefault();
				var v = N.ui.values(sf), err = sf.querySelector(".nlrm-ferr");
				if (!v.name || !v.agree || !pad.dataset.inked) { err.hidden = false; err.textContent = t("p_sign_missing"); return; }
				var btn = sf.querySelector("[type=submit]"); btn.disabled = true;
				act("sign", { name: v.name, agree: true, signature: pad.toDataURL("image/png") }).then(function () { N.ui.toast(t("p_signed")); return call("/rm/portal"); }).then(function (d) { P.data = d; render(); }).catch(function (ex) { btn.disabled = false; err.hidden = false; err.textContent = ex.message; });
			});
		}
		var ap = r.querySelector("#nlrm-apply");
		if (ap) {
			ap.addEventListener("submit", function (e) {
				e.preventDefault();
				var v = N.ui.values(ap), err = ap.querySelector(".nlrm-ferr");
				if (!v.name || !v.phone || !v.privacy_ok) { err.hidden = false; err.textContent = t("p_apply_missing"); return; }
				var btn = ap.querySelector("[type=submit]"); btn.disabled = true;
				act("apply", v).then(function (res) { P.applied = res.contact_id; render(); }).catch(function (ex) { btn.disabled = false; err.hidden = false; err.textContent = ex.message; });
			});
		}
		var ad = r.querySelector("#nlrm-appdocs");
		if (ad) {
			ad.addEventListener("submit", function (e) {
				e.preventDefault();
				var f = ad.querySelector('[type="file"]').files[0], kind = ad.querySelector('[name="kind"]').value;
				if (!f) { return; }
				shrink(f).then(function (ff) { return upload(ff, kind, { contact_id: P.applied }); }).then(function (doc) {
					ad.querySelector("#nlrm-uploaded").insertAdjacentHTML("beforeend", '<li class="nlrm-item">' + I("check", 18) + '<div class="nlrm-item-main"><b>' + esc(doc.name) + "</b><small>" + esc(t("dk_" + doc.kind)) + "</small></div></li>");
					ad.querySelector('[type="file"]').value = "";
				}).catch(function (ex) { N.ui.toast(ex.message, "bad"); });
			});
		}
		var vu = r.querySelector("#nlrm-vupd");
		if (vu) {
			vu.addEventListener("submit", function (e) {
				e.preventDefault();
				var v = N.ui.values(vu), st = (vu.querySelector('[data-vst][aria-pressed="true"]') || {}).dataset, f = vu.querySelector('[type="file"]').files[0];
				act("vendor_update", { status: st ? st.vst : "progress", note: v.note, cost: v.cost }).then(function () { return f ? shrink(f).then(function (ff) { return upload(ff, "photo"); }) : null; }).then(function () { N.ui.toast(t("p_update_sent")); return call("/rm/portal"); }).then(function (d) { P.data = d; render(); }).catch(function (ex) { N.ui.toast(ex.message, "bad"); });
			});
		}
		var qe = r.querySelector("#nlrm-qexp");
		if (qe) {
			qe.addEventListener("submit", function (e) {
				e.preventDefault();
				var v = N.ui.values(qe);
				act("expense", v).then(function () { N.ui.toast(t("saved")); qe.reset(); }).catch(function (ex) { N.ui.toast(ex.message, "bad"); });
			});
		}
	}
	function signaturePad(c) {
		var ctx = c.getContext("2d"), down = false, last = null;
		ctx.lineWidth = 2.4; ctx.lineCap = "round"; ctx.strokeStyle = "#14212b";
		var pos = function (e) { var b = c.getBoundingClientRect(); return [(e.clientX - b.left) * c.width / b.width, (e.clientY - b.top) * c.height / b.height]; };
		c.addEventListener("pointerdown", function (e) { down = true; last = pos(e); c.setPointerCapture(e.pointerId); });
		c.addEventListener("pointermove", function (e) { if (!down) { return; } var p = pos(e); ctx.beginPath(); ctx.moveTo(last[0], last[1]); ctx.lineTo(p[0], p[1]); ctx.stroke(); last = p; c.dataset.inked = "1"; });
		["pointerup", "pointercancel", "pointerleave"].forEach(function (ev) { c.addEventListener(ev, function () { down = false; }); });
	}
})();
