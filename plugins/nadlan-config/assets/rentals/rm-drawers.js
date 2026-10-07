/* ============================================================================
   NADLAN RENTALS v2 - the 360 cards, the forms and the actions (HAD-383)
   One tap on an apartment, a tenant or a repair opens everything about it.
   WhatsApp: every message is written in the RECIPIENT's language and sent
   from the landlord's own phone (wa.me), and logged in the journal.
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM, t = N.t, esc = N.esc, I = N.icon, D = function () { return N.store.d; };
	var btn = function () { return N.btn.apply(null, arguments); };
	N.forms = {};

	/* ---------- documents ---------- */
	N.docTable = function (docs, opts) {
		opts = opts || {};
		if (!docs.length) { return '<p class="nlrm-empty">' + esc(t("docs_none")) + "</p>"; }
		return '<ul class="nlrm-list">' + docs.map(function (x) {
			var rel = "";
			if (x.scope === "unit" && N.ix.unit[x.scope_id]) { rel = N.where(N.ix.unit[x.scope_id]); }
			if (x.scope === "lease") { var l = D().leases.find(function (y) { return y.id === x.scope_id; }); if (l && N.ix.unit[l.unit_id]) { rel = t("lease_of", { where: N.where(N.ix.unit[l.unit_id]) }); } }
			if (x.scope === "property" && N.ix.prop[x.scope_id]) { rel = N.ix.prop[x.scope_id].address; }
			if (x.scope === "contact" && N.ix.contact[x.scope_id]) { rel = N.ix.contact[x.scope_id].name; }
			if (x.scope === "ticket") { var tk = D().tickets.find(function (y) { return y.id === x.scope_id; }); if (tk) { rel = tk.title; } }
			var shared = x.scope === "lease" && isShared(x);
			return '<li class="nlrm-item">' + I(x.mime && x.mime.indexOf("image") === 0 ? "eye" : "doc", 22) + '<div class="nlrm-item-main"><b>' + esc(x.name) + "</b><small>" + esc([t("dk_" + x.kind), opts.noRel ? "" : rel, N.dateText((x.created_at || "").slice(0, 10)), Math.max(1, Math.round((x.size || 0) / 1024)) + " KB"].filter(Boolean).join(" · ")) + (shared ? " · " + esc(t("shared_with_tenant")) : "") + '</small></div><div class="nlrm-item-acts">' +
				btn("doc-open", t("open"), "secondary", "", ' data-id="' + x.id + '"') +
				(x.scope === "lease" ? btn("doc-share", shared ? t("unshare") : t("share_tenant"), "quiet", "", ' data-id="' + x.id + '"') : "") +
				btn("doc-del", t("delete"), "quiet", "trash", ' data-id="' + x.id + '" aria-label="' + esc(t("delete") + " " + x.name) + '"') + "</div></li>";
		}).join("") + "</ul>";
	};
	N.docList = function (scope, id) { return N.docTable(N.ix.docsBy[scope + ":" + id] || [], { noRel: true }); };
	function isShared(x) { var l = D().leases.find(function (y) { return y.id === x.scope_id; }); return !!(l && ((l.terms || {}).shared_docs || []).indexOf(x.id) >= 0); }

	/* ---------- the journal ---------- */
	function journal(scopes) {
		var ev = D().events.filter(function (e) { return scopes.some(function (s) { return e.scope === s[0] && +e.scope_id === +s[1]; }); });
		if (!ev.length) { return '<p class="nlrm-empty">' + esc(t("journal_none")) + "</p>"; }
		return '<ul class="nlrm-tl">' + ev.map(function (e) {
			var cls = e.channel === "whatsapp" ? "is-wa" : e.type === "msg_in" ? "is-in" : "";
			var ic = e.channel === "whatsapp" ? "wa" : e.type === "sign" ? "sign" : e.type === "msg_in" ? "mail" : e.type === "call" ? "phone" : "doc";
			return '<li class="' + cls + '"><span class="nlrm-tl-i">' + I(ic, 16) + "</span><div><small>" + esc(t("ev_" + e.type)) + (e.actor && e.actor.indexOf("link:") === 0 ? " · " + esc(t("via_link")) : "") + " · " + esc(N.dateText(e.at.slice(0, 10)) + " " + e.at.slice(11, 16)) + "</small>" + (e.body ? "<p>" + esc(e.body) + "</p>" : "") + "</div></li>";
		}).join("") + "</ul>";
	}

	/* ---------- open a 360 card ---------- */
	N.open = function (kind, id) {
		if (kind === "unit") { return N.ui.open(unitCard(id)); }
		if (kind === "contact") { return N.ui.open(contactCard(id)); }
		if (kind === "ticket") { return N.ui.open(ticketCard(id)); }
	};

	function unitCard(id) {
		var u = N.ix.unit[id];
		if (!u) { return null; }
		var p = N.ix.prop[u.property_id] || {}, l = N.ix.leaseByUnit[u.id], tens = l ? N.tenantsOf(l) : [], ten = tens[0], st = N.unitStatus(u);
		var tickets = (N.ix.ticketsByUnit[u.id] || []), open = tickets.filter(function (x) { return x.status !== "done" && x.status !== "cancelled"; }).length;
		var docs = (N.ix.docsBy["unit:" + u.id] || []).concat(l ? (N.ix.docsBy["lease:" + l.id] || []) : []);
		var sub = [p.address + ", " + p.city, t("floor_n", { n: u.floor }), u.rooms ? t("rooms_n", { n: u.rooms }) : "", u.sqm ? t("sqm_n", { n: u.sqm }) : "", u.dir ? t("dir_" + u.dir) : ""].filter(Boolean).map(esc).join(" · ") + " " + N.chip(st);
		var acts = l ? (ten && ten.phone ? btn("wa-remind", t("act_remind"), "wa", "wa", ' data-lease="' + l.id + '"') : "") + btn("pay", t("act_paid"), "secondary", "check", ' data-lease="' + l.id + '"') + btn("new-ticket", t("new_ticket"), "secondary", "wrench", ' data-unit="' + u.id + '"') + btn("portal-link", t("act_portal"), "quiet", "link", ' data-lease="' + l.id + '"')
			: btn("apply-link", t("act_apply_link"), "wa", "wa", ' data-unit="' + u.id + '"') + btn("new-lease", t("new_lease"), "secondary", "plus", ' data-unit="' + u.id + '"') + btn("publish", t("act_publish"), "quiet", "", ' data-unit="' + u.id + '"');
		var tabs = [
			{ id: "overview", label: t("tab_overview"), render: function () { return l ? unitOverview(u, l, tens) : vacantOverview(u); } },
			{ id: "lease", label: t("tab_lease"), render: function () { return l ? leaseTab(u, l) : '<p class="nlrm-empty">' + esc(t("no_lease")) + "</p>" + btn("new-lease", t("new_lease"), "primary", "plus", ' data-unit="' + u.id + '"'); } },
			{ id: "money", label: t("tab_money"), render: function () { return l ? moneyTab(l) : '<p class="nlrm-empty">' + esc(t("no_lease")) + "</p>"; } },
			{ id: "repairs", label: t("tab_repairs"), badge: open || "", render: function () { return repairsTab(u, tickets); } },
			{ id: "docs", label: t("tab_docs"), badge: "", render: function () { return N.docTable(docs, { noRel: true }) + btn("upload", t("upload"), "secondary", "upload", ' data-scope="' + (l ? "lease" : "unit") + '" data-id="' + (l ? l.id : u.id) + '"'); } },
			{ id: "journal", label: t("tab_journal"), render: function () { return btn("note", t("new_note"), "secondary", "plus", ' data-scope="' + (l ? "lease" : "unit") + '" data-id="' + (l ? l.id : u.id) + '"') + '<div style="margin-top:12px">' + journal([["unit", u.id]].concat(l ? [["lease", l.id]] : []).concat(tens.map(function (c) { return ["contact", c.id]; })).concat(tickets.map(function (x) { return ["ticket", x.id]; }))) + "</div>"; } },
			{ id: "home", label: t("tab_home"), render: function () { return homeTab(u); }, wire: function (b) { wireTwin(b, u); } }
		];
		return { kind: "drawer", title: esc(u.label) + (ten ? " · " + esc(ten.name) : ""), sub: sub, actions: acts, tabs: tabs, refresh: function () { return unitCard(id); } };
	}
	function factsDl(rows) { return '<dl class="nlrm-facts">' + rows.filter(function (r) { return r && r[1] !== "" && r[1] != null; }).map(function (r) { return "<div><dt>" + esc(r[0]) + "</dt><dd>" + r[1] + "</dd></div>"; }).join("") + "</dl>"; }
	function unitOverview(u, l, tens) {
		var bal = N.balance(l), h = "";
		h += '<div class="nlrm-card"><h3>' + esc(t("tenants")) + "</h3>" + tens.map(function (c) {
			return '<div class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main nlrm-person" data-open="contact:' + c.id + '">' + N.ava(c) + "<span><b>" + esc(c.name) + "</b><small>" + esc([N.phoneShow(c.phone), c.email, (N.STR[c.lang] || {}).lang_name].filter(Boolean).join(" · ")) + '</small></span></button><div class="nlrm-item-acts">' + (c.phone ? '<a class="nlrm-btn nlrm-btn--wa nlrm-btn--sm" href="' + esc(N.wa(c.phone)) + '" target="_blank" rel="noopener" data-act="wa-contact" data-id="' + c.id + '">' + I("wa", 18) + esc(t("whatsapp")) + '</a><a class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" href="tel:+' + esc(c.phone) + '">' + I("phone", 18) + esc(t("call")) + "</a>" : "") + "</div></div>";
		}).join("") + N.guarantorsOf(l).map(function (g) { return '<p class="nlrm-note">' + esc(t("guarantor_is", { name: g.name })) + "</p>"; }).join("") + "</div>";
		var dEnd = N.daysTo(l.end_date), notice = l.end_date ? N.addDays(l.end_date, -90) : "";
		h += '<div class="nlrm-card"><h3>' + esc(t("lease_now")) + " " + (bal > 0 ? N.chip(N.unitStatus(u), t("owes", { amount: N.moneyText(bal) })) : N.chip("ok", t("paid_up"))) + "</h3>" + factsDl([
			[t("f_rent"), N.money(l.rent) + " " + esc(t("per_month"))], [t("f_payday"), esc(t("payday_n", { n: l.pay_day }))], [t("f_method"), esc(t("m_" + ((l.terms || {}).method || "transfer")))],
			[t("f_start"), N.date(l.start_date)], [t("f_end"), l.end_date ? N.date(l.end_date) + (dEnd !== null ? " · " + esc(N.when(dEnd)) : "") : ""],
			[t("f_option"), l.option_until ? N.date(l.option_until) : ""], [t("f_notice"), notice ? N.date(notice) : ""],
			[t("f_linkage"), l.linkage && l.linkage.mode === "cpi" ? esc(t("linked_cpi", { pct: l.linkage.pct || 100 })) : esc(t("not_linked"))]
		]) + "</div>";
		var sec = l.securities || {}, cap = N.secCap(l), tot = (sec.cheque || 0) + (sec.deposit || 0);
		h += '<div class="nlrm-card"><h3>' + esc(t("securities")) + "</h3>" + factsDl([
			[t("sec_cheque"), sec.cheque ? N.money(sec.cheque) : ""], [t("sec_note"), sec.note ? N.money(sec.note) : ""], [t("sec_deposit"), sec.deposit ? N.money(sec.deposit) : ""],
			[t("sec_guarantors"), sec.guarantors ? esc(t("yes")) : ""], [t("sec_bank"), sec.bank ? esc(t("yes")) : ""], [t("sec_cap"), N.money(cap)]
		]) + (tot > cap ? '<p class="nlrm-hint is-warn">' + esc(t("sec_over")) + "</p>" : '<p class="nlrm-note">' + esc(t("sec_cap_note")) + "</p>") + "</div>";
		var last = (N.ix.ledgerByLease[l.id] || []).slice().sort(function (a, b) { return (b.paid_date || b.due_date || "") < (a.paid_date || a.due_date || "") ? -1 : 1; }).slice(0, 4);
		h += '<div class="nlrm-card"><h3>' + esc(t("last_moves")) + '</h3><ul class="nlrm-list">' + last.map(ledgerLi).join("") + "</ul></div>";
		return h + formerCard(u);
	}
	function vacantOverview(u) {
		var m = u.meta || {}, apps = D().contacts.filter(function (c) { return c.kind === "prospect" && (c.meta || {}).unit_id === u.id; });
		var h = '<div class="nlrm-card"><h3>' + esc(t("vacant_title_one")) + " " + N.chip("vacant") + "</h3>" + factsDl([[t("f_asking"), m.asking_rent ? N.money(m.asking_rent) : ""], [t("f_available"), m.available_from ? N.date(m.available_from) : ""]]) +
			'<p class="nlrm-note">' + esc(t("vacant_tip")) + "</p></div>";
		h += '<div class="nlrm-card"><h3>' + esc(t("applicants")) + " " + N.chip("info", String(apps.length)) + '</h3><ul class="nlrm-list">' + (apps.length ? apps.map(function (c) { return '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main nlrm-person" data-open="contact:' + c.id + '">' + N.ava(c) + "<span><b>" + esc(c.name) + "</b><small>" + esc(t("stage_" + (c.stage || "new"))) + "</small></span></button></li>"; }).join("") : '<li class="nlrm-empty">' + esc(t("applicants_none")) + "</li>") + "</ul></div>";
		return h + formerCard(u);
	}
	N.rowActs = function (r) {
		var act = r.kind === "charge" && (r.status === "open" || r.status === "partial") ? btn("pay", t("act_paid"), "secondary", "", ' data-charge="' + r.id + '"') : r.kind === "payment" && r.status === "pending" ? btn(r.method === "cheque" ? "cheque-dep" : "confirm-pay", r.method === "cheque" ? t("act_deposited") : t("act_confirm"), "secondary", "", ' data-row="' + r.id + '"') : "";
		var more = r.status !== "void" && ["charge", "payment", "refund", "expense", "income"].indexOf(r.kind) >= 0 ? '<button type="button" class="nlrm-btn nlrm-btn--quiet nlrm-btn--sm" data-act="row-more" data-row="' + r.id + '" aria-label="' + esc(t("row_actions")) + '">⋯</button>' : "";
		return act + more;
	};
	function ledgerLi(r) {
		var stc = { open: "due", paid: "ok", partial: "due", pending: "info", deposited: "ok", bounced: "late", void: "vacant" }[r.status] || "info";
		var amt = r.kind === "payment" ? '<span class="nlrm-amt-in">' + N.ag(r.amount) + "</span>" : r.kind === "expense" || r.kind === "refund" ? '<span class="nlrm-amt-out">' + N.ag(r.amount) + "</span>" : N.ag(r.amount);
		var act = N.rowActs(r);
		return '<li class="nlrm-item"><div class="nlrm-item-main"><b>' + esc(t("kind_" + r.kind) + " · " + t("cat_" + r.category)) + "</b><small>" + N.date(r.paid_date || r.due_date) + (r.method ? " · " + esc(t("m_" + r.method)) : "") + (r.ref ? " #" + esc(r.ref) : "") + (r.note ? " · " + esc(r.note) : "") + "</small></div>" + amt + N.chip(stc, t("ls_" + r.status)) + '<div class="nlrm-item-acts" style="width:auto">' + act + "</div></li>";
	}
	function leaseTab(u, l) {
		var sig = (l.signing || {}).parties || [];
		var h = '<div class="nlrm-card"><h3>' + esc(t("lease_terms")) + "</h3>" + factsDl([
			[t("f_start"), N.date(l.start_date)], [t("f_end"), N.date(l.end_date)], [t("f_option"), l.option_until ? N.date(l.option_until) : ""],
			[t("f_rent"), N.money(l.rent)], [t("f_payday"), esc(t("payday_n", { n: l.pay_day }))], [t("f_method"), esc(t("m_" + ((l.terms || {}).method || "transfer")))],
			[t("f_linkage"), l.linkage && l.linkage.mode === "cpi" ? esc(t("linkage_full", { pct: l.linkage.pct || 100, every: l.linkage.every || 12, base: N.dateText(l.linkage.base_date) })) + (l.linkage.floor ? " · " + esc(t("with_floor")) : "") : esc(t("not_linked"))]
		]) + '<div class="nlrm-tools" style="margin-top:12px">' + btn("edit-lease", t("edit"), "secondary", "", ' data-lease="' + l.id + '"') + (l.linkage && l.linkage.mode === "cpi" ? btn("cpi-lease", t("cpi_check_now"), "secondary", "", ' data-lease="' + l.id + '"') : "") + btn("renew-lease", t("renew_lease"), "secondary", "", ' data-lease="' + l.id + '"') + btn("end-lease", t("end_lease"), "quiet", "", ' data-lease="' + l.id + '"') + "</div></div>";
		h += '<div class="nlrm-card"><h3>' + I("sign", 20) + esc(t("signing")) + " " + (sig.length ? N.chip("ok", t("signed_n", { n: sig.length })) : N.chip("due", t("not_signed"))) + "</h3>" +
			(sig.length ? '<ul class="nlrm-list">' + sig.map(function (s) { return '<li class="nlrm-item"><div class="nlrm-item-main"><b>' + esc(s.name) + "</b><small>" + esc(N.dateText(String(s.at).slice(0, 10)) + " " + String(s.at).slice(11, 16)) + (s.text_sha256 && s.text_sha256 !== "sample" ? " · SHA-256 " + esc(s.text_sha256.slice(0, 12)) + "…" : "") + "</small></div></li>"; }).join("") + "</ul>" : '<p class="nlrm-lead">' + esc(t("sign_lead")) + "</p>") +
			'<div class="nlrm-tools">' + btn("lease-doc", t("lease_doc"), "secondary", "doc", ' data-lease="' + l.id + '"') + btn("sign-link", t("send_sign"), "wa", "wa", ' data-lease="' + l.id + '"') + "</div></div>";
		h += '<div class="nlrm-card"><h3>' + esc(t("deadlines")) + '</h3><ul class="nlrm-list">' + deadlines(l).map(function (d) { return '<li class="nlrm-item"><span class="nlrm-dot s' + d.s + '"></span><div class="nlrm-item-main"><b>' + esc(d.text) + "</b><small>" + N.date(d.date) + " · " + esc(N.when(N.daysTo(d.date))) + "</small></div></li>"; }).join("") + '</ul><p class="nlrm-note">' + esc(t("deadlines_law")) + "</p></div>";
		return h;
	}
	function deadlines(l) {
		var out = [];
		if (l.end_date) {
			out.push({ s: 2, text: t("dl_landlord_notice"), date: N.addDays(l.end_date, -90) });
			out.push({ s: 3, text: t("dl_tenant_notice"), date: N.addDays(l.end_date, -60) });
			out.push({ s: 1, text: t("dl_end"), date: l.end_date });
			out.push({ s: 4, text: t("dl_deposit_return"), date: N.addDays(l.end_date, 60) });
		}
		if (l.option_until) { out.push({ s: 2, text: t("dl_option"), date: l.option_until }); }
		if (l.linkage && l.linkage.mode === "cpi") { var nx = l.start_date; while (nx <= N.todayIso()) { nx = N.addMonths(nx, l.linkage.every || 12); } out.push({ s: 4, text: t("dl_cpi"), date: nx }); }
		return out.filter(function (d) { return N.daysTo(d.date) > -30; }).sort(function (a, b) { return a.date < b.date ? -1 : 1; });
	}
	N.moneyTab = moneyTab;
	function moneyTab(l) {
		var rows = (N.ix.ledgerByLease[l.id] || []).slice().sort(function (a, b) { return (b.due_date || b.paid_date || "") < (a.due_date || a.paid_date || "") ? -1 : 1; });
		var m = N.moneyOf(l), cheques = N.pendingCheques(l), credit = m.balance < 0;
		var h = '<div class="nlrm-kpis" style="grid-template-columns:repeat(3,minmax(0,1fr))"><div class="nlrm-kpi"><span>' + esc(t(credit ? "credit_balance" : "balance")) + "</span><b" + (credit ? ' class="nlrm-amt-in"' : "") + ">" + N.ag(Math.abs(m.balance)) + '</b></div><div class="nlrm-kpi"><span>' + esc(t("ontime_12")) + "</span><b>" + onTime(l) + '</b></div><div class="nlrm-kpi"><span>' + esc(t("cheques_held")) + "</span><b>" + cheques.length + "</b></div></div>";
		h += '<div class="nlrm-tools" style="margin-bottom:10px">' + btn("pay", t("new_payment"), "primary", "plus", ' data-lease="' + l.id + '"') + btn("charge", t("new_charge"), "secondary", "plus", ' data-lease="' + l.id + '"') + btn("receipt", t("payment_confirm_doc"), "quiet", "doc", ' data-lease="' + l.id + '"') +
			(l.status === "ended" && m.balance > 0 ? btn("writeoff", t("writeoff"), "quiet", "", ' data-lease="' + l.id + '"') : "") + (credit ? btn("refund", t("refund_credit"), "quiet", "", ' data-lease="' + l.id + '"') : "") + "</div>";
		h += depositCard(l, m);
		return h + '<ul class="nlrm-list">' + rows.map(ledgerLi).join("") + "</ul>";
	}
	/* the security deposit: what is held, the legal cap, the 60-day clock after the end */
	function depositCard(l, m) {
		var cap = N.secCap(l) * 100, ended = (l.terms || {}).ended, due = ended ? (ended.deposit_due || N.addDays(l.end_date, 60)) : null, dd = due ? N.daysTo(due) : null;
		var h = '<div class="nlrm-card"><h3>' + esc(t("deposit_title")) + " " + (m.deposit_held > 0 ? N.chip(ended ? (dd !== null && dd < 0 ? "late" : "due") : "info", N.agText(m.deposit_held)) : "") + "</h3>" + factsDl([
			[t("deposit_held"), N.ag(m.deposit_held)], [t("sec_cap"), N.ag(cap)], [t("deposit_back_by"), due ? N.date(due) + (dd !== null ? " · " + esc(N.when(dd)) : "") : ""]
		]) + '<div class="nlrm-tools">' + (l.status === "active" ? btn("dep-receive", t("dep_receive"), "secondary", "plus", ' data-lease="' + l.id + '"') : "") +
			(m.deposit_held > 0 ? btn("dep-apply", t("dep_apply"), "quiet", "", ' data-lease="' + l.id + '"') + btn("dep-return", t("dep_return"), ended ? "primary" : "quiet", "", ' data-lease="' + l.id + '"') : "") + "</div>" +
			'<p class="nlrm-note">' + esc(t("deposit_law")) + "</p></div>";
		return h;
	}
	/* former leases of an apartment that still have money matters (a debt, a deposit, a credit) */
	function formerCard(u) {
		var list = D().leases.filter(function (l) { if (l.unit_id !== u.id || l.status !== "ended") { return false; } var m = N.moneyOf(l); return m.balance !== 0 || m.deposit_held !== 0; });
		if (!list.length) { return ""; }
		return '<div class="nlrm-card"><h3>' + esc(t("former_title")) + '</h3><ul class="nlrm-list">' + list.map(function (l) {
			var m = N.moneyOf(l), c = N.tenantsOf(l)[0];
			var bits = [m.balance > 0 ? t("owes", { amount: N.agText(m.balance) }) : "", m.balance < 0 ? t("credit_of", { amount: N.agText(-m.balance) }) : "", m.deposit_held > 0 ? t("deposit_held_of", { amount: N.agText(m.deposit_held) }) : ""].filter(Boolean).join(" · ");
			return '<li class="nlrm-item"><div class="nlrm-item-main"><b>' + esc(c ? c.name : t("former_tenant")) + "</b><small>" + N.date(l.start_date) + " - " + N.date(l.end_date) + " · " + esc(bits) + '</small></div><div class="nlrm-item-acts" style="width:auto">' + btn("former-money", t("tab_money"), "secondary", "", ' data-lease="' + l.id + '"') + "</div></li>";
		}).join("") + "</ul></div>";
	}
	N.formerCard = formerCard;
	function onTime(l) {
		var charges = (N.ix.ledgerByLease[l.id] || []).filter(function (r) { return r.kind === "charge" && r.due_date && r.due_date <= N.todayIso() && r.due_date >= N.addMonths(N.todayIso(), -12); });
		var ok = charges.filter(function (r) { return r.status === "paid"; }).length;
		return charges.length ? ok + "/" + charges.length : "-";
	}
	function repairsTab(u, tickets) {
		var h = btn("new-ticket", t("new_ticket"), "primary", "plus", ' data-unit="' + u.id + '"');
		if (!tickets.length) { return h + '<p class="nlrm-empty">' + esc(t("repairs_none")) + "</p>"; }
		return h + '<ul class="nlrm-list" style="margin-top:10px">' + tickets.slice().reverse().map(function (x) {
			var dd = N.daysTo(x.due_by);
			return '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main" data-open="ticket:' + x.id + '"><b>' + esc(x.title) + "</b><small>" + esc(t("ts_" + x.status)) + (x.status !== "done" && dd !== null ? " · " + esc(dd < 0 ? t("overdue_by", { n: -dd }) : t("due_in", { when: N.when(dd) })) : "") + "</small></button>" + (x.urgency === "urgent" ? N.chip("late", t("urgent")) : "") + "</li>";
		}).join("") + "</ul>";
	}
	var ASSET_KINDS = ["boiler", "ac", "panel", "water_meter", "gas", "fridge", "oven", "washer", "dishwasher", "heater", "shutter"];
	function homeTab(u) {
		var m = u.meta || {}, assets = m.assets || [];
		var h = '<div class="nlrm-card"><h3>' + esc(t("home_facts")) + "</h3>" + factsDl([[t("f_label"), esc(u.label)], [t("f_floor"), esc(String(u.floor))], [t("f_rooms"), u.rooms ? esc(String(u.rooms)) : ""], [t("f_sqm"), u.sqm ? esc(String(u.sqm)) : ""], [t("f_dir"), u.dir ? esc(t("dir_" + u.dir)) : ""], [t("f_furnished"), m.furnished ? esc(t("yes")) : ""], [t("f_parking"), m.parking ? esc(t("yes")) : ""], [t("f_storage"), m.storage ? esc(t("yes")) : ""]]) + '<div class="nlrm-tools" style="margin-top:10px">' + btn("edit-unit", t("edit"), "secondary", "", ' data-unit="' + u.id + '"') + "</div></div>";
		h += '<div class="nlrm-card"><h3>' + I("cube", 20) + esc(t("twin_title")) + '</h3><p class="nlrm-lead">' + esc(t("twin_lead")) + '</p><div class="nlrm-3d" id="nlrm-twin" style="height:360px"><div class="nlrm-3d-wait">' + esc(t("loading_3d")) + "</div></div></div>";
		h += '<div class="nlrm-card"><h3>' + esc(t("assets_title")) + '</h3><ul class="nlrm-list">' + (assets.length ? assets.map(function (a) {
			var w = a.warranty_until ? N.daysTo(a.warranty_until) : null;
			return '<li class="nlrm-item" id="nlrm-asset-' + esc(a.id) + '"><div class="nlrm-item-main"><b>' + esc(a.label || t("ak_" + a.kind)) + "</b><small>" + esc([a.brand, a.model, a.installed ? t("installed_in", { d: a.installed }) : "", a.last_service ? t("serviced_on", { d: N.dateText(a.last_service) }) : ""].filter(Boolean).join(" · ")) + "</small></div>" + (w === null ? "" : w < 0 ? N.chip("due", t("warranty_over")) : N.chip("ok", t("warranty_until", { d: N.dateText(a.warranty_until) }))) + btn("asset-ticket", t("asset_repair"), "quiet", "wrench", ' data-unit="' + u.id + '" data-asset="' + esc(a.id) + '"') + btn("asset-edit", t("edit"), "quiet", "", ' data-unit="' + u.id + '" data-asset="' + esc(a.id) + '"') + "</li>";
		}).join("") : '<li class="nlrm-empty">' + esc(t("assets_none")) + "</li>") + "</ul>" + btn("new-asset", t("new_asset"), "secondary", "plus", ' data-unit="' + u.id + '"') + "</div>";
		h += '<div class="nlrm-card"><h3>' + esc(t("tour_title")) + "</h3>" + (m.tour_url ? '<p><a href="' + esc(m.tour_url) + '" target="_blank" rel="noopener">' + esc(t("tour_open")) + "</a></p>" : '<p class="nlrm-lead">' + esc(t("tour_lead")) + "</p>") + btn("edit-unit", t("tour_set"), "quiet", "", ' data-unit="' + u.id + '"') + "</div>";
		return h;
	}
	function wireTwin(b, u) {
		var host = b.querySelector("#nlrm-twin");
		if (!host) { return; }
		var go = function () {
			if (!window.NLRM3D || !document.body.contains(host)) { return; }
			host.innerHTML = "";
			var m = u.meta || {};
			window.NLRM3D.mountApartment(host, {
				plan: m.plan || null, rooms: u.rooms || 3, sqm: u.sqm || 75, dir: u.dir || "west", lang: N.lang, rtl: N.rtl,
				assets: (m.assets || []).map(function (a) {
					/* an appliance with an open repair is marked on the plan, and its pin opens that repair */
					var tk = (N.ix.ticketsByUnit[u.id] || []).filter(function (x) { return x.status !== "done" && x.status !== "cancelled" && (x.meta || {}).asset === a.id; })[0];
					return { id: a.id, kind: a.kind, label: a.label || t("ak_" + a.kind), room: a.room, at: a.at, warranty_until: a.warranty_until, last_service: a.last_service, open: !!tk, ticket: tk ? tk.id : 0, openText: tk ? t("asset_open_repair") : "" };
				}),
				onPickAsset: function (aid) {
					var a = (m.assets || []).find(function (x) { return x.id === aid; }), tk = a ? (N.ix.ticketsByUnit[u.id] || []).filter(function (x) { return x.status !== "done" && x.status !== "cancelled" && (x.meta || {}).asset === a.id; })[0] : null;
					if (tk) { N.open("ticket", tk.id); return; }
					var el = b.querySelector("#nlrm-asset-" + aid); if (el) { el.scrollIntoView({ behavior: "smooth", block: "center" }); el.style.background = "#e5eff3"; setTimeout(function () { el.style.background = ""; }, 1600); }
				}
			});
		};
		if (window.NLRM3D) { go(); } else { window.addEventListener("nlrm3d:ready", go, { once: true }); }
	}

	function contactCard(id) {
		var c = N.ix.contact[id];
		if (!c) { return null; }
		var l = c.kind === "tenant" ? N.leaseOfContact(c.id) : D().leases.find(function (x) { return ((x.parties || {}).guarantors || []).indexOf(c.id) >= 0; });
		var u = l ? N.ix.unit[l.unit_id] : ((c.meta || {}).unit_id ? N.ix.unit[c.meta.unit_id] : null);
		var acts = (c.phone ? '<a class="nlrm-btn nlrm-btn--wa nlrm-btn--sm" href="' + esc(N.wa(c.phone)) + '" target="_blank" rel="noopener" data-act="wa-contact" data-id="' + c.id + '">' + I("wa", 18) + esc(t("whatsapp")) + '</a><a class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" href="tel:+' + esc(c.phone) + '">' + I("phone", 18) + esc(t("call")) + "</a>" : "") + (c.email ? '<a class="nlrm-btn nlrm-btn--secondary nlrm-btn--sm" href="mailto:' + esc(c.email) + '">' + I("mail", 18) + esc(t("email")) + "</a>" : "");
		var tabs = [
			{ id: "overview", label: t("tab_overview"), render: function () {
				var h = '<div class="nlrm-card">' + factsDl([[t("f_kind"), esc(t("kind_" + c.kind))], [t("f_phone"), c.phone ? '<span class="nlrm-num">' + esc(N.phoneShow(c.phone)) + "</span>" : ""], [t("f_email"), esc(c.email || "")], [t("f_lang"), esc((N.STR[c.lang] || {}).lang_name || c.lang)], [t("f_unit"), u ? '<button type="button" class="nlrm-link" data-open="unit:' + u.id + '">' + esc(N.where(u)) + "</button>" : ""], [t("balance"), l && c.kind === "tenant" ? N.money(Math.max(0, N.balance(l))) : ""]]) + "</div>";
				if (c.kind === "prospect") {
					var m = c.meta || {};
					h += '<div class="nlrm-card"><h3>' + esc(t("prospect_file")) + "</h3>" + factsDl([[t("f_stage"), esc(t("stage_" + (c.stage || "new")))], [t("f_household"), esc(m.household || "")], [t("f_movein"), m.move_in ? N.date(m.move_in) : ""], [t("f_viewing"), esc(m.viewing_at || "")], [t("f_privacy"), m.privacy ? esc(t("privacy_given", { v: m.privacy.version })) : ""]]) +
						'<div class="nlrm-seg" role="group" style="margin-top:12px">' + ["new", "contacted", "viewing", "applied", "approved", "lost"].map(function (s) { return '<button type="button" data-act="stage" data-id="' + c.id + '" data-stage="' + s + '" aria-pressed="' + ((c.stage || "new") === s) + '">' + esc(t("stage_" + s)) + "</button>"; }).join("") + "</div>" +
						'<div class="nlrm-tools">' + (u ? btn("new-lease", t("lease_with", { name: c.name }), "primary", "plus", ' data-unit="' + u.id + '" data-contact="' + c.id + '"') : "") + btn("screen-tips", t("screen_tips"), "quiet") + "</div></div>";
				}
				if (c.notes) { h += '<div class="nlrm-card"><h3>' + esc(t("notes")) + "</h3><p style=\"white-space:pre-wrap;margin:0\">" + esc(c.notes) + "</p></div>"; }
				return h;
			} },
			{ id: "journal", label: t("tab_journal"), render: function () { return btn("note", t("new_note"), "secondary", "plus", ' data-scope="contact" data-id="' + c.id + '"') + '<div style="margin-top:12px">' + journal([["contact", c.id]].concat(l ? [["lease", l.id]] : [])) + "</div>"; } },
			{ id: "docs", label: t("tab_docs"), render: function () { return N.docList("contact", c.id) + btn("upload", t("upload"), "secondary", "upload", ' data-scope="contact" data-id="' + c.id + '"') + '<p class="nlrm-note">' + esc(t("docs_privacy")) + "</p>"; } },
			{ id: "edit", label: t("tab_details"), render: function () { return btn("edit-contact", t("edit"), "primary", "", ' data-id="' + c.id + '"') + " " + btn("del-contact", t("delete"), "danger", "trash", ' data-id="' + c.id + '"'); } }
		];
		return { kind: "drawer", title: esc(c.name), sub: esc(t("kind_" + c.kind)) + (u ? " · " + esc(N.where(u)) : ""), actions: acts, tabs: tabs, refresh: function () { return contactCard(id); } };
	}

	function ticketCard(id) {
		var x = D().tickets.find(function (y) { return y.id === id; });
		if (!x) { return null; }
		var u = N.ix.unit[x.unit_id], v = x.vendor_id ? N.ix.contact[x.vendor_id] : null, dd = N.daysTo(x.due_by), tri = (x.meta || {}).triage || null;
		var l = u ? N.ix.leaseByUnit[u.id] : null, ten = l ? N.tenantsOf(l)[0] : null;
		var acts = btn("vendor-link", t("send_vendor"), "wa", "wa", ' data-ticket="' + x.id + '"') + (ten && ten.phone ? btn("wa-ticket", t("update_tenant"), "secondary", "wa", ' data-ticket="' + x.id + '"') : "") + (u ? btn("open", t("tab_home"), "quiet", "", ' data-open="unit:' + u.id + '"') : "");
		var body = function () {
			var h = '<div class="nlrm-seg" role="group" aria-label="' + esc(t("f_status")) + '">' + ["new", "scheduled", "progress", "waiting", "done"].map(function (s) { return '<button type="button" data-act="tstatus" data-id="' + x.id + '" data-status="' + s + '" aria-pressed="' + (x.status === s) + '">' + esc(t("ts_" + s)) + "</button>"; }).join("") + "</div>";
			h += '<div class="nlrm-card">' + factsDl([[t("f_unit"), u ? '<button type="button" class="nlrm-link" data-open="unit:' + u.id + '">' + esc(N.where(u)) + "</button>" : ""], [t("f_opened"), N.date((x.opened_at || "").slice(0, 10))], [t("f_due"), x.due_by ? N.date(x.due_by) + " · " + esc(dd < 0 ? t("overdue_by", { n: -dd }) : N.when(dd)) : ""], [t("f_urgency"), esc(x.urgency === "urgent" ? t("urgent") : t("standard"))], [t("f_category"), esc(t("tc_" + x.category))], [t("f_reporter"), esc(t("rep_" + x.reporter))], [t("f_vendor"), v ? '<button type="button" class="nlrm-link" data-open="contact:' + v.id + '">' + esc(v.name) + "</button>" : ""], [t("f_cost"), x.cost ? N.money(x.cost) : ""]]) + (x.body ? '<p style="white-space:pre-wrap;margin:12px 0 0">' + esc(x.body) + "</p>" : "") + '<p class="nlrm-note">' + esc(x.urgency === "urgent" ? t("law_3") : t("law_30")) + "</p></div>";
			if (tri) { h += '<div class="nlrm-hint">' + I("spark", 18) + " " + esc(t("triage_says", { pro: tri.pro || t("tc_" + tri.category) })) + ' <a href="' + esc((N.state.cfg.urls || {}).pros || "/professionals/") + '?profession=' + encodeURIComponent(tri.category) + '" target="_blank" rel="noopener">' + esc(t("find_pro")) + "</a></div>"; }
			h += '<div class="nlrm-tools" style="margin:12px 0">' + btn("ticket-vendor", t("choose_vendor"), "secondary", "people", ' data-id="' + x.id + '"') + btn("ticket-cost", t("set_cost"), "secondary", "money", ' data-id="' + x.id + '"') + btn("upload", t("add_photo"), "secondary", "upload", ' data-scope="ticket" data-id="' + x.id + '"') + btn("note", t("new_note"), "quiet", "plus", ' data-scope="ticket" data-id="' + x.id + '"') + "</div>";
			h += N.docList("ticket", x.id);
			h += '<h3 style="margin:16px 0 8px;font-size:18px">' + esc(t("tab_journal")) + "</h3>" + journal([["ticket", x.id]]);
			return h;
		};
		return { kind: "drawer", title: esc(x.title), sub: (x.urgency === "urgent" ? N.chip("late", t("urgent")) + " " : "") + N.chip(x.status === "done" ? "ok" : "info", t("ts_" + x.status)), actions: acts, body: body(), refresh: function () { return ticketCard(id); } };
	}

	/* ---------- WhatsApp: compose in the recipient's language, send from the landlord's phone ---------- */
	N.sendWA = function (contact, kind, vars, scope) {
		if (!contact || !contact.phone) { N.ui.toast(t("no_phone"), "bad"); return; }
		var lang = contact.lang || "he", me = N.state.cfg.me || {};
		var text = N.msg(kind, lang, Object.assign({ name: (contact.name || "").split(" ")[0], landlord: me.display || "" }, vars || {}));
		N.ui.open({ kind: "sheet", title: t("wa_preview", { name: contact.name }), sub: esc(t("wa_in_lang", { lang: (N.STR[lang] || {}).lang_name || lang })),
			body: '<form class="nlrm-form"><label class="nlrm-f is-wide"><span>' + esc(t("wa_text")) + '</span><textarea name="txt" rows="8" dir="' + (lang === "he" || lang === "ar" ? "rtl" : "ltr") + '">' + esc(text) + '</textarea></label><div class="nlrm-fbtns"><a class="nlrm-btn nlrm-btn--wa" data-send target="_blank" rel="noopener" href="#">' + I("wa", 18) + esc(t("wa_send")) + '</a><button type="button" class="nlrm-btn nlrm-btn--secondary" data-copy>' + esc(t("copy")) + "</button></div>" + (D().demo ? '<p class="nlrm-note">' + esc(t("wa_demo")) + "</p>" : "") + "</form>",
			wire: function (b) {
				var ta = b.querySelector("textarea"), a = b.querySelector("[data-send]");
				var upd = function () { a.href = N.wa(contact.phone, ta.value); };
				ta.addEventListener("input", upd); upd();
				a.addEventListener("click", function (e) {
					if (D().demo) { e.preventDefault(); }
					N.store.event({ scope: scope ? scope[0] : "contact", scope_id: scope ? scope[1] : contact.id, type: "msg_out", channel: "whatsapp", body: ta.value });
					N.ui.close(); N.ui.toast(D().demo ? t("wa_logged_demo") : t("wa_logged"));
				});
				b.querySelector("[data-copy]").addEventListener("click", function () { N.copy(ta.value); });
			} });
	};
	/* a personal link: create it, then hand it over by WhatsApp (or copy) */
	N.shareLink = function (purpose, scope, scopeId, contact, msgKind, vars) {
		N.store.link({ purpose: purpose, scope: scope, scope_id: scopeId, contact_id: contact ? contact.id : 0 }).then(function (lk) {
			if (contact && contact.phone) { N.sendWA(contact, msgKind, Object.assign({ link: lk.url, until: N.dateText(lk.expires_at) }, vars || {}), [scope, scopeId]); }
			else {
				N.ui.open({ kind: "sheet", title: t("link_ready"), body: '<p class="nlrm-lead">' + esc(t("link_ready_lead", { until: N.dateText(lk.expires_at) })) + '</p><p class="nlrm-msg" dir="ltr">' + esc(lk.url) + '</p><div class="nlrm-fbtns"><button type="button" class="nlrm-btn nlrm-btn--primary" data-copy>' + esc(t("copy")) + '</button><a class="nlrm-btn nlrm-btn--wa" target="_blank" rel="noopener" href="' + esc(N.wa("", N.msg(msgKind, N.lang, Object.assign({ name: "", link: lk.url, until: N.dateText(lk.expires_at) }, vars || {})))) + '">' + I("wa", 18) + esc(t("wa_share")) + "</a></div>", wire: function (b) { b.querySelector("[data-copy]").addEventListener("click", function () { N.copy(lk.url); }); } });
			}
		}).catch(function (e) { N.ui.toast(e.message || t("err_generic"), "bad"); });
	};

	/* ---------- forms ---------- */
	var unitOpts = function () { return D().units.map(function (u) { return [u.id, N.where(u)]; }); };
	var propOpts = function () { return D().properties.map(function (p) { return [p.id, p.address + ", " + p.city]; }); };
	/* B21: the leases a payment or a charge can go to - every active lease, every ended lease that still
	   owes or is owed money, and always the lease the form was opened from (a former tenant's money sheet).
	   A list of active leases only put a former tenant's payment on someone else's lease. */
	var leaseOpts = function (keep) {
		return D().leases.filter(function (l) {
			if (l.status === "active" || (keep && l.id === keep.id)) { return true; }
			var m = N.moneyOf(l); return !!m && (m.balance !== 0 || m.pending > 0);
		}).map(function (l) {
			var c = N.tenantsOf(l)[0];
			return [l.id, N.where(N.ix.unit[l.unit_id]) + (c ? " · " + c.name : "") + (l.status === "active" ? "" : " · " + t("former_tenant"))];
		});
	};
	var methodOpts = function () { return ["transfer", "standing", "cheque", "bit", "paybox", "cash", "card", "other"].map(function (m) { return [m, t("m_" + m)]; }); };
	N.forms.property = function (p) {
		p = p || {};
		var m = p.meta || {};
		N.ui.form({ title: p.id ? t("edit_property") : t("new_property"), intro: p.id ? "" : esc(t("new_property_lead")), fields: [
			{ name: "address", label: t("f_address"), value: p.address, required: true, autocomplete: "street-address" }, { name: "city", label: t("f_city"), value: p.city, required: true },
			{ name: "floors", label: t("f_floors"), type: "number", value: p.floors || 4, min: 1, max: 80 }, { name: "units_per_floor", label: t("f_upf"), type: "number", value: p.units_per_floor || 3, min: 1, max: 24 },
			{ name: "year_built", label: t("f_year"), type: "number", value: m.year_built || "" }, { name: "shelter", label: t("f_shelter"), type: "select", value: m.shelter || "", options: [["", t("unknown")], ["mamad", t("has_mamad")], ["shared", t("has_shelter")]] },
			{ name: "elevator", label: t("has_elevator"), type: "check", value: m.elevator }, { name: "parking", label: t("has_parking"), type: "check", value: m.parking }, { name: "solar", label: t("has_solar"), type: "check", value: m.solar !== false }
		], onSubmit: function (v) {
			return N.store.save("property", { id: p.id, address: v.address, city: v.city, floors: v.floors, units_per_floor: v.units_per_floor, title: v.address + ", " + v.city, meta: Object.assign({}, m, { year_built: v.year_built || null, shelter: v.shelter, elevator: v.elevator, parking: v.parking, solar: v.solar }) }).then(function (row) { if (!p.id) { N.go("property", row.id); } N.ui.toast(t("saved")); });
		} });
	};
	N.forms.unit = function (u) {
		u = u || {};
		var m = u.meta || {}, p = N.ix.prop[u.property_id];
		N.ui.form({ title: u.id ? t("edit_unit") : t("new_unit"), sub: p ? esc(p.address) : "", fields: [
			{ name: "property_id", label: t("f_property"), type: "select", value: u.property_id, options: propOpts() },
			{ name: "label", label: t("f_label"), value: u.label || (u.floor ? t("apt_floor", { n: u.floor }) : ""), required: true },
			{ name: "floor", label: t("f_floor"), type: "number", value: u.floor != null ? u.floor : 1 }, { name: "pos", label: t("f_pos"), type: "number", value: u.pos || 0, min: 0, max: 23, hint: t("f_pos_hint") },
			{ name: "rooms", label: t("f_rooms"), type: "number", step: "0.5", value: u.rooms || "" }, { name: "sqm", label: t("f_sqm"), type: "number", value: u.sqm || "" },
			{ name: "dir", label: t("f_dir"), type: "select", value: u.dir || "", options: [["", t("unknown")]].concat(["north", "south", "east", "west", "ne", "nw", "se", "sw"].map(function (d) { return [d, t("dir_" + d)]; })) },
			{ name: "asking_rent", label: t("f_asking"), type: "number", value: m.asking_rent || "" }, { name: "available_from", label: t("f_available"), type: "date", value: m.available_from || "" },
			{ name: "tour_url", label: t("tour_title"), type: "url", value: m.tour_url || "", ltr: true, hint: t("tour_hint") },
			{ name: "furnished", label: t("f_furnished"), type: "check", value: m.furnished }, { name: "parking", label: t("f_parking"), type: "check", value: m.parking }, { name: "storage", label: t("f_storage"), type: "check", value: m.storage }
		], onSubmit: function (v) {
			return N.store.save("unit", { id: u.id, property_id: +v.property_id, label: v.label, floor: v.floor, pos: v.pos, rooms: v.rooms, sqm: v.sqm, dir: v.dir, meta: Object.assign({}, m, { asking_rent: v.asking_rent || 0, available_from: v.available_from, tour_url: v.tour_url, furnished: v.furnished, parking: v.parking, storage: v.storage }) }).then(function (row) { N.ui.toast(t("saved")); if (!u.id) { setTimeout(function () { N.open("unit", row.id); }, 250); } });
		} });
	};
	N.forms.contact = function (c, kind) {
		c = c || { kind: kind || "tenant", lang: N.lang };
		N.ui.form({ title: c.id ? t("edit_contact") : t("new_" + (c.kind || "contact")), fields: [
			{ name: "kind", label: t("f_kind"), type: "select", value: c.kind, options: ["tenant", "prospect", "guarantor", "vendor", "coowner", "other"].map(function (k) { return [k, t("kind_" + k)]; }) },
			{ name: "name", label: t("f_name"), value: c.name, required: true, autocomplete: "name" }, { name: "phone", label: t("f_phone"), type: "tel", value: c.phone ? N.phoneShow(c.phone) : "", autocomplete: "tel" },
			{ name: "email", label: t("f_email"), type: "email", value: c.email || "", autocomplete: "email" },
			{ name: "lang", label: t("f_lang"), type: "select", value: c.lang || "he", options: Object.keys(N.STR).map(function (l) { return [l, N.STR[l].lang_name || l]; }), hint: t("f_lang_hint") },
			{ name: "idno", label: t("f_idno"), value: c.idno || "", hint: t("f_idno_hint"), inputmode: "numeric" },
			{ name: "tags", label: t("f_trade"), type: "select", value: c.tags || "", options: [["", "-"]].concat(["plumbing", "electric", "ac", "boiler", "locks", "paint", "general"].map(function (k) { return [k, t("trade_" + k)]; })) },
			{ name: "notes", label: t("notes"), type: "textarea", value: c.notes || "" }
		], note: esc(t("contact_privacy")), onSubmit: function (v) {
			return N.store.save("contact", { id: c.id, kind: v.kind, name: v.name, phone: N.phone(v.phone), email: v.email, lang: v.lang, idno: v.idno, tags: v.tags, notes: v.notes, stage: c.stage || (v.kind === "prospect" ? "new" : ""), meta: c.meta || {} }).then(function () { N.ui.toast(t("saved")); });
		} });
	};
	N.forms.lease = function (l, unitId, contactId) {
		l = l || {};
		var link = l.linkage || {}, sec = l.securities || {}, terms = l.terms || {};
		var tenOpts = [[0, t("new_tenant_below")]].concat(D().contacts.filter(function (c) { return c.kind === "tenant" || c.kind === "prospect"; }).map(function (c) { return [c.id, c.name]; }));
		var cur = ((l.parties || {}).tenants || [])[0] || contactId || 0;
		var start = l.start_date || N.addDays(N.todayIso(), 14);
		N.ui.form({ title: l.id ? t("edit_lease") : t("new_lease"), intro: l.id ? "" : esc(t("new_lease_lead")), fields: [
			{ name: "unit_id", label: t("f_unit"), type: "select", value: l.unit_id || unitId, options: unitOpts() },
			{ name: "tenant", label: t("f_tenant"), type: "select", value: cur, options: tenOpts },
			{ name: "t_name", label: t("f_new_tenant_name"), value: "" }, { name: "t_phone", label: t("f_phone"), type: "tel", value: "" },
			{ name: "t_lang", label: t("f_lang"), type: "select", value: N.lang, options: Object.keys(N.STR).map(function (x) { return [x, N.STR[x].lang_name || x]; }) },
			{ html: '<p class="nlrm-fsec">' + esc(t("sec_dates_money")) + "</p>" },
			{ name: "start_date", label: t("f_start"), type: "date", value: start, required: true }, { name: "end_date", label: t("f_end"), type: "date", value: l.end_date || N.addDays(N.addMonths(start, 12), -1), required: true },
			{ name: "option_until", label: t("f_option"), type: "date", value: l.option_until || "" }, { name: "rent", label: t("f_rent"), type: "number", value: l.rent || "", required: true, inputmode: "numeric" },
			{ name: "pay_day", label: t("f_payday_n"), type: "number", value: l.pay_day || 1, min: 1, max: 28 }, { name: "method", label: t("f_method"), type: "select", value: terms.method || "transfer", options: methodOpts() },
			{ html: '<p class="nlrm-fsec">' + esc(t("f_linkage")) + "</p>" },
			{ name: "link_mode", label: t("f_linkage"), type: "select", value: link.mode || "none", options: [["none", t("not_linked")], ["cpi", t("linked_cpi_short")]] },
			{ name: "link_every", label: t("f_link_every"), type: "select", value: link.every || 12, options: [[12, t("every_12")], [6, t("every_6")], [3, t("every_3")], [1, t("every_1")]] },
			{ name: "link_pct", label: t("f_link_pct"), type: "number", value: link.pct || 100, min: 0, max: 100 }, { name: "link_floor", label: t("with_floor"), type: "check", value: link.floor !== false },
			{ html: '<p class="nlrm-fsec">' + esc(t("securities")) + "</p>" },
			{ name: "sec_cheque", label: t("sec_cheque"), type: "number", value: sec.cheque || "" }, { name: "sec_note", label: t("sec_note"), type: "number", value: sec.note || "" },
			{ name: "sec_deposit", label: t("sec_deposit"), type: "number", value: sec.deposit || "" }, { name: "sec_guarantors", label: t("sec_guarantors"), type: "check", value: sec.guarantors },
			{ html: '<p class="nlrm-hint" id="nlrm-capline"></p>' },
			{ name: "track_from", label: t("f_track_from"), type: "date", value: terms.track_from || "", hint: t("track_from_hint") },
			{ name: "pets", label: t("f_pets"), type: "check", value: terms.pets }
		], wire: function (form) {
			var cap = form.querySelector("#nlrm-capline");
			var upd = function () {
				var v = N.ui.values(form), c = N.secCap({ rent: +v.rent || 0, start_date: v.start_date, end_date: v.end_date }), tot = (+v.sec_cheque || 0) + (+v.sec_deposit || 0);
				cap.className = "nlrm-hint" + (tot > c && c > 0 ? " is-warn" : "");
				cap.textContent = c ? t(tot > c ? "cap_over" : "cap_line", { cap: N.moneyText(c) }) : t("cap_need_rent");
				form.querySelectorAll('[name="t_name"],[name="t_phone"],[name="t_lang"]').forEach(function (el) { el.closest("label").style.display = +v.tenant ? "none" : ""; });
				/* a lease that started before this month: money is followed from this month on, unless told otherwise */
				var tf = form.querySelector('[name="track_from"]'), first = N.todayIso().slice(0, 8) + "01";
				tf.closest("label").style.display = v.start_date && v.start_date < first ? "" : "none";
				if (v.start_date && v.start_date < first && !tf.value && !l.id) { tf.value = first; }
			};
			form.addEventListener("input", upd); form.addEventListener("change", upd); upd();
		}, onSubmit: function (v) {
			var mk = +v.tenant ? Promise.resolve({ id: +v.tenant }) : (v.t_name ? N.store.save("contact", { kind: "tenant", name: v.t_name, phone: N.phone(v.t_phone), lang: v.t_lang }) : Promise.reject(new Error(t("err_tenant"))));
			return mk.then(function (c) {
				var cc = N.ix.contact[c.id] || c;
				if (cc.kind === "prospect") { N.store.save("contact", { id: cc.id, kind: "tenant", stage: "signed", name: cc.name, phone: cc.phone, lang: cc.lang, meta: cc.meta || {} }); }
				return N.store.save("lease", { id: l.id, unit_id: +v.unit_id, status: l.status || "active", start_date: v.start_date, end_date: v.end_date, option_until: v.option_until || null, rent: +v.rent, pay_day: +v.pay_day,
					linkage: { mode: v.link_mode, base_date: link.base_date || v.start_date, every: +v.link_every, pct: +v.link_pct, floor: v.link_floor },
					securities: { cheque: +v.sec_cheque || 0, note: +v.sec_note || 0, deposit: +v.sec_deposit || 0, guarantors: v.sec_guarantors, bank: sec.bank || false },
					parties: Object.assign({}, l.parties || {}, { tenants: [c.id] }), terms: Object.assign({}, terms, { method: v.method, pets: v.pets, track_from: v.start_date < N.todayIso().slice(0, 8) + "01" ? (v.track_from || "") : "" }) });
			}).then(function (row) { N.ui.toast(t("saved")); setTimeout(function () { N.open("unit", row.unit_id); }, 250); });
		} });
	};
	N.forms.payment = function (o) {
		o = o || {};
		var charge = o.charge ? D().ledger.find(function (r) { return r.id === +o.charge; }) : null;
		var lease = charge ? D().leases.find(function (l) { return l.id === charge.lease_id; }) : o.lease ? D().leases.find(function (l) { return l.id === +o.lease; }) : null;
		var opts = leaseOpts(lease);
		if (!lease && !opts.length) { N.ui.toast(t("no_leases"), "bad"); return; }
		var bal = lease ? N.balance(lease) : 0;
		N.ui.form({ title: t("new_payment"), fields: [
			{ name: "lease_id", label: t("f_lease"), type: "select", value: lease ? lease.id : opts[0][0], options: opts },
			{ name: "amount", label: t("f_amount"), type: "number", value: charge ? Math.round(charge.amount / 100) : (bal > 0 ? bal : (lease ? lease.rent : "")), required: true, inputmode: "decimal" },
			{ name: "paid_date", label: t("f_paid_date"), type: "date", value: N.todayIso() }, { name: "method", label: t("f_method"), type: "select", value: (lease && (lease.terms || {}).method) || "transfer", options: methodOpts() },
			{ name: "ref", label: t("f_ref"), value: "", hint: t("f_ref_hint") }, { name: "note", label: t("notes"), value: "" }
		], onSubmit: function (v) {
			var l = D().leases.find(function (x) { return x.id === +v.lease_id; }), u = N.ix.unit[l.unit_id];
			return N.store.money("pay", { data: { lease_id: l.id, amount: +v.amount, paid_date: v.paid_date, method: v.method, ref: v.ref, note: v.note, applies_to: charge ? charge.id : 0, category: charge ? charge.category : "rent" } }).then(function () { N.ui.toast(t("pay_saved")); });
		} });
	};
	/* the end of a lease: the date the apartment is returned, why, and proration */
	N.forms.leaseEnd = function (l) {
		N.ui.form({ title: t("end_title"), intro: esc(t("end_lead")), fields: [
			{ name: "date", label: t("f_end_date"), type: "date", value: l.end_date && l.end_date < N.todayIso() ? l.end_date : N.todayIso(), required: true },
			{ name: "reason", label: t("f_end_reason"), type: "select", value: l.end_date && l.end_date <= N.todayIso() ? "term" : "early", options: ["term", "early", "mutual", "eviction"].map(function (k) { return [k, t("reason_" + k)]; }) },
			{ name: "prorate", label: t("f_prorate"), type: "check", value: true }
		], note: esc(t("end_note")), submit: t("end_lease"), onSubmit: function (v) {
			return N.store.money("lease-end", { lease_id: l.id, data: { date: v.date, reason: v.reason, prorate: v.prorate } }).then(function () { N.ui.toast(t("lease_ended")); });
		} });
	};
	/* a new term for the same tenant: the old lease closes the day before, the deposit moves */
	N.forms.leaseRenew = function (l) {
		var start = l.end_date ? N.addDays(l.end_date, 1) : N.todayIso();
		N.ui.form({ title: t("renew_title"), intro: esc(t("renew_lead")), fields: [
			{ name: "start_date", label: t("f_start"), type: "date", value: start, required: true },
			{ name: "end_date", label: t("f_end"), type: "date", value: N.addDays(N.addMonths(start, 12), -1), required: true },
			{ name: "rent", label: t("f_rent"), type: "number", value: l.rent, required: true, inputmode: "numeric" }
		], submit: t("renew_lease"), onSubmit: function (v) {
			return N.store.money("lease-renew", { lease_id: l.id, data: { start_date: v.start_date, end_date: v.end_date, rent: +v.rent } }).then(function (p) { N.ui.toast(t("renew_done")); if (p && p.lease) { setTimeout(function () { N.open("unit", p.lease.unit_id); }, 250); } });
		} });
	};
	N.forms.deposit = function (l, act) {
		var m = N.moneyOf(l), amount = act === "receive" ? "" : Math.round(Math.min(m.deposit_held, act === "apply" ? Math.max(0, m.balance) || m.deposit_held : m.deposit_held)) / 100;
		var fields = [{ name: "amount", label: t("f_amount"), type: "number", value: amount, required: true, inputmode: "decimal" }, { name: "date", label: t("f_paid_date"), type: "date", value: N.todayIso() }];
		if (act === "apply") { fields.push({ name: "category", label: t("f_dep_reason"), type: "select", value: m.balance > 0 ? "rent" : "repair", options: ["rent", "repair", "water", "electric", "gas", "arnona", "vaad", "other"].map(function (c) { return [c, t("cat_" + c)]; }) }); }
		if (act !== "apply") { fields.push({ name: "method", label: t("f_method"), type: "select", value: "transfer", options: ["transfer", "cheque", "cash", "bit", "other"].map(function (x) { return [x, t("m_" + x)]; }) }); }
		fields.push({ name: "note", label: t("notes"), value: "" });
		N.ui.form({ title: t("dep_" + act + "_title"), intro: esc(t("dep_" + act + "_lead", { held: N.agText(m.deposit_held), cap: N.moneyText(N.secCap(l)) })), fields: fields, onSubmit: function (v) {
			return N.store.money("deposit", { lease_id: l.id, act: act, data: v }).then(function () { N.ui.toast(t("dep_done")); });
		} });
	};
	N.forms.writeoff = function (l) {
		var m = N.moneyOf(l);
		N.ui.form({ title: t("writeoff_title"), intro: esc(t("writeoff_lead", { amount: N.agText(m.balance) })), fields: [{ name: "amount", label: t("f_amount"), type: "number", value: m.balance / 100, required: true }, { name: "note", label: t("notes"), value: "" }], submit: t("writeoff"), onSubmit: function (v) {
			return N.store.money("writeoff", { lease_id: l.id, data: v }).then(function () { N.ui.toast(t("writeoff_done")); });
		} });
	};
	N.forms.refund = function (l) {
		var m = N.moneyOf(l), credit = -m.balance - m.future;
		N.ui.form({ title: t("refund_title"), intro: esc(t("refund_lead", { amount: N.agText(Math.max(0, credit)) })), fields: [{ name: "amount", label: t("f_amount"), type: "number", value: Math.max(0, credit) / 100, required: true }, { name: "method", label: t("f_method"), type: "select", value: "transfer", options: ["transfer", "cheque", "cash", "bit", "other"].map(function (x) { return [x, t("m_" + x)]; }) }, { name: "note", label: t("notes"), value: "" }], submit: t("refund_credit"), onSubmit: function (v) {
			return N.store.money("refund", { lease_id: l.id, data: v }).then(function () { N.ui.toast(t("refund_done")); });
		} });
	};
	/* a line in the books: void it (with a reason, both stay visible) or mark a cheque as bounced */
	N.forms.rowMore = function (r) {
		if (!r) { return; }
		var acts = [];
		if (r.kind === "payment" && r.method === "cheque" && (r.status === "deposited" || r.status === "paid" || r.status === "pending")) { acts.push(["bounce", t("act_bounce")]); }
		acts.push(["void", t("act_void")]);
		N.ui.open({ kind: "sheet", title: t("row_actions"), body: '<p class="nlrm-lead">' + esc(t("kind_" + r.kind) + " · " + t("cat_" + r.category) + " · " + N.agText(r.amount)) + '</p><div class="nlrm-fbtns">' + acts.map(function (a) { return '<button type="button" class="nlrm-btn nlrm-btn--secondary" data-sheet-act="' + a[0] + '">' + esc(a[1]) + "</button>"; }).join("") + '</div><p class="nlrm-note">' + esc(t("books_note")) + "</p>", wire: function (b) {
			b.addEventListener("click", function (ev) {
				var x = ev.target.closest("[data-sheet-act]");
				if (!x) { return; }
				N.ui.close(true);
				if (x.dataset.sheetAct === "bounce") {
					N.ui.form({ title: t("bounce_title"), intro: esc(t("bounce_lead")), fields: [{ name: "fee", label: t("f_bounce_fee"), type: "number", value: "" }], submit: t("act_bounce"), onSubmit: function (v) {
						return N.store.money("ledger-act", { id: r.id, act: "bounce", data: { fee: +v.fee || 0, date: N.todayIso() } }).then(function () { N.ui.toast(t("bounced_done")); });
					} });
				} else {
					N.ui.form({ title: t("void_title"), intro: esc(t("void_lead")), fields: [{ name: "reason", label: t("f_void_reason"), required: true }], submit: t("act_void"), onSubmit: function (v) {
						return N.store.money("ledger-act", { id: r.id, act: "void", data: { reason: v.reason } }).then(function () { N.ui.toast(t("voided_done")); });
					} });
				}
			});
		} });
	};
	/* what the 3D label of an apartment carries: open repairs, a lease ending within 90 days */
	N.unitBadges = function (u) {
		var open = (N.ix.ticketsByUnit[u.id] || []).filter(function (x) { return x.status !== "done" && x.status !== "cancelled"; }).length;
		var l = N.ix.leaseByUnit[u.id], de = l ? N.daysTo(l.end_date) : null, ending = de !== null && de >= 0 && de <= 90;
		var text = [open ? N.tn("badge_repairs", open) : "", ending ? t("badge_ending") : ""].filter(Boolean).join(", ");
		return { repairs: open, ending: ending, text: text };
	};
	/* a floor of a building: its apartments with tenant, rent, money and repairs; every line opens deeper */
	N.forms.floorCard = function (pid, f) {
		var p = N.ix.prop[pid];
		if (!p) { return; }
		var us = (N.ix.unitsByProp[pid] || []).filter(function (u) { return +u.floor === +f; });
		var rent = 0, owed = 0, repairs = [];
		us.forEach(function (u) {
			var l = N.ix.leaseByUnit[u.id];
			if (l) { rent += +l.rent || 0; owed += Math.max(0, N.moneyOf(l).balance); }
			(N.ix.ticketsByUnit[u.id] || []).forEach(function (x) { if (x.status !== "done" && x.status !== "cancelled") { repairs.push(x); } });
		});
		if (N._b3d && N._b3d.focusFloor && N._b3d.focusedFloor() !== +f) { N._b3d.focusFloor(f); }
		var body = '<div class="nlrm-kpis" style="grid-template-columns:repeat(3,minmax(0,1fr))"><div class="nlrm-kpi"><span>' + esc(t("floor_units")) + "</span><b>" + us.length + '</b></div><div class="nlrm-kpi"><span>' + esc(t("floor_rent")) + "</span><b>" + N.money(rent) + '</b></div><div class="nlrm-kpi"><span>' + esc(t("floor_owed")) + "</span><b" + (owed > 0 ? ' class="nlrm-amt-out"' : "") + ">" + N.ag(owed) + "</b></div></div>";
		body += '<div class="nlrm-card"><h3>' + esc(t("floor_apts")) + '</h3><ul class="nlrm-list">' + (us.length ? us.map(function (u) {
			var l = N.ix.leaseByUnit[u.id], c = l ? N.tenantsOf(l)[0] : null, st = N.unitStatus(u), b = N.unitBadges(u), m = l ? N.moneyOf(l) : null;
			return '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main" data-open="unit:' + u.id + '"><b>' + esc(u.label) + (c ? " · " + esc(c.name) : "") + "</b><small>" + esc([l ? N.moneyText(l.rent) + " " + t("per_month") : t("st_vacant"), m && m.balance > 0 ? t("owes", { amount: N.agText(m.balance) }) : "", b.text].filter(Boolean).join(" · ")) + "</small></button>" + N.chip(st) + "</li>";
		}).join("") : '<li class="nlrm-empty">' + esc(t("floor_none")) + "</li>") + "</ul></div>";
		body += '<div class="nlrm-card"><h3>' + esc(t("floor_repairs")) + '</h3><ul class="nlrm-list">' + (repairs.length ? repairs.map(function (x) {
			var dd = N.daysTo(x.due_by), u = N.ix.unit[x.unit_id] || {};
			return '<li class="nlrm-item"><button type="button" class="nlrm-link nlrm-item-main" data-open="ticket:' + x.id + '"><b>' + esc(u.label + " · " + x.title) + "</b><small>" + esc(t("ts_" + x.status)) + (dd !== null ? " · " + esc(dd < 0 ? t("overdue_by", { n: -dd }) : t("due_in", { when: N.when(dd) })) : "") + "</small></button>" + (x.urgency === "urgent" ? N.chip("late", t("urgent")) : "") + "</li>";
		}).join("") : '<li class="nlrm-empty">' + esc(t("floor_repairs_none")) + "</li>") + "</ul></div>";
		N.ui.open({ kind: "drawer", title: esc(t("floor_card_title", { n: f })), sub: esc(p.address + ", " + p.city), body: body, actions: btn("floor-back", t("floor_back"), "quiet", "building"), refresh: function () { return null; } });
	};
	N.forms.expense = function (o) {
		o = o || {};
		N.ui.form({ title: t("new_expense"), fields: [
			{ name: "property_id", label: t("f_property"), type: "select", value: o.prop || (D().properties[0] || {}).id, options: propOpts() },
			{ name: "unit_id", label: t("f_unit_opt"), type: "select", value: o.unit || 0, options: [[0, t("whole_building")]].concat(unitOpts()) },
			{ name: "category", label: t("f_category"), type: "select", value: o.category || "repair", options: ["arnona", "vaad", "repair", "insurance", "mortgage", "water", "electric", "gas", "tax", "fee", "other"].map(function (c) { return [c, t("cat_" + c)]; }) },
			{ name: "amount", label: t("f_amount"), type: "number", value: o.amount || "", required: true, inputmode: "decimal" }, { name: "paid_date", label: t("f_paid_date"), type: "date", value: N.todayIso() },
			{ name: "note", label: t("notes"), value: o.note || "" }
		], note: esc(t("expense_note")), onSubmit: function (v) {
			return N.store.save("ledger", { property_id: +v.property_id, unit_id: +v.unit_id, kind: "expense", category: v.category, amount: Math.round(+v.amount * 100), paid_date: v.paid_date, status: "paid", note: v.note }).then(function () { N.ui.toast(t("saved")); });
		} });
	};
	N.forms.charge = function (o) {
		o = o || {};
		var from = o.lease ? D().leases.find(function (l) { return l.id === +o.lease; }) : null, opts = leaseOpts(from);
		if (!opts.length) { N.ui.toast(t("no_leases"), "bad"); return; }
		N.ui.form({ title: t("new_charge"), fields: [
			{ name: "lease_id", label: t("f_lease"), type: "select", value: from ? from.id : opts[0][0], options: opts },
			{ name: "category", label: t("f_category"), type: "select", value: "other", options: ["rent", "water", "electric", "gas", "arnona", "vaad", "repair", "other"].map(function (c) { return [c, t("cat_" + c)]; }) },
			{ name: "amount", label: t("f_amount"), type: "number", required: true }, { name: "due_date", label: t("f_due"), type: "date", value: N.todayIso() }, { name: "note", label: t("notes"), value: "" }
		], note: esc(t("charge_note")), onSubmit: function (v) {
			var l = D().leases.find(function (x) { return x.id === +v.lease_id; }), u = N.ix.unit[l.unit_id];
			return N.store.save("ledger", { property_id: u.property_id, unit_id: u.id, lease_id: l.id, kind: "charge", category: v.category, amount: Math.round(+v.amount * 100), due_date: v.due_date, status: "open", note: v.note }).then(function () { N.ui.toast(t("saved")); });
		} });
	};
	N.forms.ticket = function (o) {
		o = o || {};
		var asset = o.asset && o.unit ? ((N.ix.unit[o.unit].meta || {}).assets || []).find(function (a) { return a.id === o.asset; }) : null;
		N.ui.form({ title: t("new_ticket"), fields: [
			{ name: "unit_id", label: t("f_unit"), type: "select", value: o.unit || (D().units[0] || {}).id, options: unitOpts() },
			{ name: "title", label: t("f_ticket_title"), value: asset ? t("asset_fault", { a: asset.label || t("ak_" + asset.kind) }) : "", required: true, placeholder: t("f_ticket_ph") },
			{ name: "body", label: t("f_ticket_body"), type: "textarea", value: "" },
			{ html: '<p class="nlrm-hint" id="nlrm-tri"></p>' },
			{ name: "urgency", label: t("f_urgency"), type: "select", value: "auto", options: [["auto", t("urgency_auto")], ["urgent", t("urgent")], ["standard", t("standard")]] }
		], wire: function (form) {
			var tri = form.querySelector("#nlrm-tri");
			var upd = function () { var v = N.ui.values(form), r = N.triage(v.title + " " + v.body); tri.innerHTML = I("spark", 18) + " " + esc(t("triage_live", { cat: t("tc_" + r.category), urg: r.urgency === "urgent" ? t("urgent") : t("standard"), days: r.urgency === "urgent" ? 3 : 30 })); };
			form.addEventListener("input", upd); upd();
		}, onSubmit: function (v) {
			var u = N.ix.unit[+v.unit_id], r = N.triage(v.title + " " + v.body), urg = v.urgency === "auto" ? r.urgency : v.urgency;
			return N.store.save("ticket", { property_id: u.property_id, unit_id: u.id, title: v.title, body: v.body, category: r.category, urgency: urg, status: "new", reporter: "owner", due_by: N.addDays(N.todayIso(), urg === "urgent" ? 3 : 30), meta: { triage: r, asset: o.asset || "" } }).then(function (row) { N.ui.toast(t("saved")); setTimeout(function () { N.open("ticket", row.id); }, 250); });
		} });
	};
	/* the same rules as the server (portal.php nlrm_triage), so the landlord sees what the tenant's portal will decide */
	/* the shared rule table (i18n/triage.json, given by the page as N.TRIAGE), the
	   same one the server applies (portal.php nlrm_triage) */
	N.triage = function (text) {
		var s = String(text || "").toLowerCase(), cat = "general", urg = "standard", tb = N.TRIAGE || { categories: [], urgent: [] };
		tb.categories.some(function (c) { return c[1].some(function (w) { if (s.indexOf(String(w).toLowerCase()) >= 0) { cat = c[0]; return true; } return false; }); });
		tb.urgent.some(function (w) { if (s.indexOf(String(w).toLowerCase()) >= 0) { urg = "urgent"; return true; } return false; });
		return { category: cat, urgency: urg, pro: t("trade_" + cat), by: "rules" };
	};
	N.forms.upload = function (scope, id) {
		var opts = [];
		D().leases.forEach(function (l) { opts.push(["lease:" + l.id, t("lease_of", { where: N.where(N.ix.unit[l.unit_id] || {}) })]); });
		D().units.forEach(function (u) { opts.push(["unit:" + u.id, N.where(u)]); });
		D().properties.forEach(function (p) { opts.push(["property:" + p.id, p.address]); });
		D().contacts.forEach(function (c) { opts.push(["contact:" + c.id, c.name]); });
		D().tickets.forEach(function (x) { opts.push(["ticket:" + x.id, x.title]); });
		N.ui.form({ title: t("upload"), fields: [
			{ name: "target", label: t("f_attach_to"), type: "select", value: scope ? scope + ":" + id : (opts[0] || [])[0], options: opts },
			{ name: "kind", label: t("f_doc_kind"), type: "select", value: "other", options: ["lease", "protocol", "id", "payslip", "bank", "receipt", "invoice", "insurance", "nesach", "photo", "plan", "cheque", "other"].map(function (k) { return [k, t("dk_" + k)]; }) },
			{ html: '<label class="nlrm-f is-wide"><span>' + esc(t("f_file")) + '</span><input type="file" name="file" required accept="image/*,.pdf,.doc,.docx,.xls,.xlsx"></label>' }
		], note: esc(t("docs_privacy")), onSubmit: function (v, form) {
			var f = form.querySelector('[type="file"]').files[0];
			if (!f) { return Promise.reject(new Error(t("err_file"))); }
			var tg = v.target.split(":");
			return N.store.upload(f, tg[0], +tg[1], v.kind).then(function () { N.ui.toast(t("uploaded")); });
		} });
	};
	N.forms.note = function (scope, id) {
		N.ui.form({ title: t("new_note"), fields: [
			{ name: "type", label: t("f_note_type"), type: "select", value: "note", options: [["note", t("ev_note")], ["call", t("ev_call")], ["visit", t("ev_visit")], ["msg_in", t("ev_msg_in")]] },
			{ name: "body", label: t("f_note_body"), type: "textarea", required: true }
		], onSubmit: function (v) { return N.store.event({ scope: scope, scope_id: +id, type: v.type, channel: v.type === "call" ? "phone" : v.type === "visit" ? "inperson" : "", body: v.body }).then(function () { N.ui.toast(t("saved")); }); } });
	};
	/* an appliance of the apartment: new, or (aid) edited or removed - its repair history stays with the tickets */
	N.forms.asset = function (u, aid) {
		var a = aid ? ((u.meta || {}).assets || []).find(function (x) { return x.id === aid; }) : null;
		var fields = [
			{ name: "kind", label: t("f_asset_kind"), type: "select", value: a ? a.kind : "ac", options: ASSET_KINDS.map(function (k) { return [k, t("ak_" + k)]; }) },
			{ name: "label", label: t("f_asset_label"), value: a ? a.label || "" : "" }, { name: "brand", label: t("f_brand"), value: a ? a.brand || "" : "" }, { name: "model", label: t("f_model"), value: a ? a.model || "" : "" },
			{ name: "installed", label: t("f_installed"), type: "month", value: a ? a.installed || "" : "" }, { name: "warranty_until", label: t("f_warranty"), type: "date", value: a ? a.warranty_until || "" : "" }, { name: "last_service", label: t("f_service"), type: "date", value: a ? a.last_service || "" : "" }
		];
		if (a) { fields.push({ name: "remove", label: t("asset_remove"), type: "check", value: false }); }
		N.ui.form({ title: t(a ? "edit_asset" : "new_asset"), sub: esc(N.where(u)), fields: fields, onSubmit: function (v) {
			var m = Object.assign({}, u.meta || {}), list = (m.assets || []).slice();
			var row = { id: a ? a.id : "a" + Date.now().toString(36), kind: v.kind, label: v.label || t("ak_" + v.kind), brand: v.brand, model: v.model, installed: v.installed, warranty_until: v.warranty_until, last_service: v.last_service };
			if (a && v.remove) { list = list.filter(function (x) { return x.id !== a.id; }); }
			else if (a) { list = list.map(function (x) { return x.id === a.id ? Object.assign({}, x, row) : x; }); }
			else { list.push(row); }
			m.assets = list;
			return N.store.save("unit", { id: u.id, property_id: u.property_id, meta: m }).then(function () { N.ui.toast(t(a && v.remove ? "asset_removed" : "saved")); });
		} });
	};

	/* ---------- printable documents (a payment confirmation, the rent roll, the evidence file, the lease) ---------- */
	N.printDoc = function (title, html) {
		var w = window.open("", "_blank");
		if (!w) { N.ui.toast(t("popup_blocked"), "bad"); return; }
		if (html && typeof html.then === "function") {
			w.document.write('<!doctype html><meta charset="utf-8"><p style="font:16px Arial,sans-serif;margin:40px">' + esc(t("loading")) + "</p>"); w.document.close();
			html.then(function (h) { w.document.open(); N.printDoc.write(w, title, h); }, function () { w.document.open(); N.printDoc.write(w, title, '<p>' + esc(t("err_generic")) + "</p>"); });
			return;
		}
		N.printDoc.write(w, title, html);
	};
	N.printDoc.write = function (w, title, html) {
		w.document.write('<!doctype html><html dir="' + (N.rtl ? "rtl" : "ltr") + '" lang="' + N.lang + '"><head><meta charset="utf-8"><title>' + esc(title) + '</title><style>body{font-family:Assistant,Arial,sans-serif;max-width:800px;margin:28px auto;padding:0 18px;color:#14212b;font-size:14px;line-height:1.6}h1{font:600 24px "Noto Serif Hebrew",Georgia,serif;border-bottom:2px solid #14212b;padding-bottom:8px}h2{font:600 17px "Noto Serif Hebrew",Georgia,serif;margin:20px 0 6px}table{width:100%;border-collapse:collapse;margin:8px 0}td,th{border:1px solid #ddd;padding:6px 9px;text-align:start;vertical-align:top}th{background:#f7f6f2}.n{direction:ltr;unicode-bidi:isolate}.foot{color:#6b7680;font-size:12px;border-top:1px solid #ddd;margin-top:24px;padding-top:8px}@media print{button{display:none}}</style></head><body>' + html + '<p class="foot">' + esc(t("print_foot", { date: N.dateText(N.todayIso()) })) + '</p><button onclick="print()">' + esc(t("print")) + "</button></body></html>");
		w.document.close();
	};
	function rentRollHtml() {
		var rows = D().units.map(function (u) { var l = N.ix.leaseByUnit[u.id], c = l ? N.tenantsOf(l)[0] : null; return "<tr><td>" + esc(N.where(u)) + "</td><td>" + esc(c ? c.name : "-") + '</td><td class="n">' + (l ? N.moneyText(l.rent) : "-") + "</td><td>" + (l ? N.dateText(l.start_date) + " - " + N.dateText(l.end_date) : "-") + '</td><td class="n">' + (l ? N.moneyText(Math.max(0, N.balance(l))) : "-") + "</td><td>" + esc(t("st_" + N.unitStatus(u))) + "</td></tr>"; }).join("");
		return "<h1>" + esc(t("rep_roll")) + "</h1><table><tr><th>" + esc(t("col_unit")) + "</th><th>" + esc(t("col_tenant")) + "</th><th>" + esc(t("col_rent")) + "</th><th>" + esc(t("tab_lease")) + "</th><th>" + esc(t("balance")) + "</th><th>" + esc(t("col_status")) + "</th></tr>" + rows + "</table>";
	}
	function yearHtml(y) {
		var inc = {}, exp = {};
		D().ledger.forEach(function (r) {
			if ((r.paid_date || "").slice(0, 4) !== y) { return; }
			var p = N.ix.prop[r.property_id] || {}, k = p.address || "-";
			var x = N.mx.incomeOf(r);
			if (x) { inc[k] = (inc[k] || 0) + x; }
			if (r.kind === "expense" && r.status !== "void") { exp[k + " · " + t("cat_" + r.category)] = (exp[k + " · " + t("cat_" + r.category)] || 0) + r.amount; }
		});
		var tot = 0; Object.keys(inc).forEach(function (k) { tot += inc[k]; });
		return "<h1>" + esc(t("rep_year", { y: y })) + "</h1><h2>" + esc(t("pnl_income")) + "</h2><table>" + Object.keys(inc).map(function (k) { return "<tr><td>" + esc(k) + '</td><td class="n">' + N.agText(inc[k]) + "</td></tr>"; }).join("") + "<tr><th>" + esc(t("total")) + '</th><th class="n">' + N.agText(tot) + "</th></tr></table><h2>" + esc(t("pnl_expenses")) + "</h2><table>" + Object.keys(exp).map(function (k) { return "<tr><td>" + esc(k) + '</td><td class="n">' + N.agText(exp[k]) + "</td></tr>"; }).join("") + "</table><p>" + esc(t("tax_note", { ceiling: N.moneyText(N.TAX_CEILING.amount) })) + "</p>";
	}
	/* full = the server's whole history of the lease (rows + events); without it, what this screen holds */
	function evidenceHtml(l, full) {
		var u = N.ix.unit[l.unit_id], c = N.tenantsOf(l)[0];
		var led = ((full && full.rows) || N.ix.ledgerByLease[l.id] || []).slice().sort(function (a, b) { var x = a.due_date || a.paid_date || "", y = b.due_date || b.paid_date || ""; return x < y ? -1 : x > y ? 1 : a.id - b.id; });
		var tk = N.ix.ticketsByUnit[u.id] || [];
		var ev = (full && full.events) || D().events.filter(function (e) { return (e.scope === "lease" && e.scope_id === l.id) || (c && e.scope === "contact" && e.scope_id === c.id); });
		return "<h1>" + esc(t("rep_evidence")) + " · " + esc(N.where(u)) + "</h1><table><tr><th>" + esc(t("col_tenant")) + "</th><td>" + esc(c ? c.name : "") + "</td></tr><tr><th>" + esc(t("f_start")) + "</th><td>" + N.dateText(l.start_date) + "</td></tr><tr><th>" + esc(t("f_end")) + "</th><td>" + N.dateText(l.end_date) + "</td></tr><tr><th>" + esc(t("f_rent")) + '</th><td class="n">' + N.moneyText(l.rent) + "</td></tr></table>" +
			"<h2>" + esc(t("tab_money")) + "</h2><table>" + led.map(function (r) { return "<tr><td>" + N.dateText(r.paid_date || r.due_date) + "</td><td>" + esc(t("kind_" + r.kind) + " · " + t("cat_" + r.category) + (r.ref ? " #" + r.ref : "")) + '</td><td class="n">' + N.agText(r.amount) + "</td><td>" + esc(t("ls_" + r.status)) + "</td></tr>"; }).join("") + "</table>" +
			"<h2>" + esc(t("tab_repairs")) + "</h2><table>" + (tk.map(function (x) { return "<tr><td>" + N.dateText((x.opened_at || "").slice(0, 10)) + "</td><td>" + esc(x.title) + "</td><td>" + esc(t("ts_" + x.status)) + "</td><td>" + (x.closed_at ? N.dateText(x.closed_at.slice(0, 10)) : "") + "</td></tr>"; }).join("") || "<tr><td>-</td></tr>") + "</table>" +
			"<h2>" + esc(t("tab_journal")) + "</h2><table>" + (ev.map(function (e) { return "<tr><td>" + esc(e.at) + "</td><td>" + esc(t("ev_" + e.type)) + "</td><td>" + esc(e.body || "") + "</td></tr>"; }).join("") || "<tr><td>-</td></tr>") + "</table><p>" + esc(t("evidence_note")) + "</p>";
	}
	function receiptHtml(l) {
		var u = N.ix.unit[l.unit_id], c = N.tenantsOf(l)[0], me = N.state.cfg.me || {};
		var p = (N.ix.ledgerByLease[l.id] || []).filter(function (r) { return r.kind === "payment" && (r.status === "paid" || r.status === "deposited"); }).sort(function (a, b) { return a.paid_date < b.paid_date ? 1 : -1; })[0];
		if (!p) { return "<h1>" + esc(t("payment_confirm_doc")) + "</h1><p>" + esc(t("no_payments")) + "</p>"; }
		return "<h1>" + esc(t("payment_confirm_doc")) + "</h1><p>" + esc(t("receipt_body", { landlord: me.display || t("the_landlord"), tenant: c ? c.name : "", amount: N.agText(p.amount), date: N.dateText(p.paid_date), where: N.where(u), method: t("m_" + (p.method || "transfer")) + (p.ref ? " #" + p.ref : "") })) + "</p><p>" + esc(t("receipt_note")) + "</p>";
	}
	function csv(rows) { return rows.map(function (r) { return r.map(function (x) { x = String(x == null ? "" : x); return /[",\n]/.test(x) ? '"' + x.replace(/"/g, '""') + '"' : x; }).join(","); }).join("\r\n"); }
	function download(name, text, type) { var b = new Blob(["﻿" + text], { type: type || "text/csv;charset=utf-8" }), a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500); }

	/* ---------- actions ---------- */
	N.act = function (name, el, e) {
		var d = el.dataset, lease = d.lease ? D().leases.find(function (l) { return l.id === +d.lease; }) : null;
		var ten = lease ? N.tenantsOf(lease)[0] : null, u = lease ? N.ix.unit[lease.unit_id] : d.unit ? N.ix.unit[+d.unit] : null;
		var me = N.state.cfg.me || {};
		switch (name) {
			case "new":
				N.ui.open({ kind: "sheet", title: t("add_what"), body: '<div class="nlrm-grid2">' + [["new-property", "building", t("new_property")], ["new-unit", "cube", t("new_unit")], ["new-lease", "sign", t("new_lease")], ["new-contact", "people", t("new_contact")], ["pay", "money", t("new_payment")], ["expense", "money", t("new_expense")], ["new-ticket", "wrench", t("new_ticket")], ["upload", "upload", t("upload")], ["import", "upload", t("imp_title")]].map(function (x) { return '<button type="button" class="nlrm-kpi" data-sheet-act="' + x[0] + '">' + I(x[1], 22) + "<b style=\"font-size:16px\">" + esc(x[2]) + "</b></button>"; }).join("") + "</div>", wire: function (b) {
					b.addEventListener("click", function (ev) { var x = ev.target.closest("[data-sheet-act]"); if (!x) { return; } N.ui.close(true); setTimeout(function () { N.act(x.dataset.sheetAct, x, ev); }, 60); });
				} });
				return;
			case "more":
				N.ui.open({ kind: "sheet", title: t("nav_more"), body: '<div class="nlrm-grid2">' + ["leasing", "docs", "reports", "settings", "help"].map(function (r) { return '<button type="button" class="nlrm-kpi" data-more="' + r + '"><b style="font-size:16px">' + esc(t("nav_" + r)) + "</b></button>"; }).join("") + "</div>", wire: function (b) { b.addEventListener("click", function (ev) { var x = ev.target.closest("[data-more]"); if (x) { N.ui.close(true); N.go(x.dataset.more); } }); } });
				return;
			case "att-all": N.state.attAll = true; N.render(); return;
			case "import": if (N.forms.importSheet) { N.forms.importSheet(); } return;
			case "sample": N.state.cfg.adapterReal = N.store.adapter; N.store.adapter = N.DemoAdapter(N.lang); N.store.load(); return;
			case "my-data": N.store.adapter = N.state.cfg.adapterReal || N.store.adapter; N.state.cfg.adapterReal = null; N.store.d = { properties: [], units: [], contacts: [], leases: [], ledger: [], tickets: [], tasks: [], docs: [], events: [], plan: { id: "free", limits: {} }, role: "owner" }; N.store.load(); return;
			case "go-settings": N.go("settings"); return;
			case "go-properties": N.go("properties"); return;
			case "go-tax": N.state.mtab = "tax"; N.go("money"); return;
			case "m-prev": N.state.month = N.addMonths(N.state.month + "-01", -1).slice(0, 7); N.render(); return;
			case "m-next": N.state.month = N.addMonths(N.state.month + "-01", 1).slice(0, 7); N.render(); return;
			case "open": var o = d.open.split(":"); N.open(o[0], +o[1]); return;
			case "new-property": N.forms.property(); return;
			case "edit-property": N.forms.property(N.ix.prop[+d.prop]); return;
			case "new-unit": N.forms.unit({ property_id: +(d.prop || N.state.param || (D().properties[0] || {}).id), floor: 1, pos: 0 }); return;
			case "claim": N.forms.unit({ property_id: +d.prop, floor: +d.floor, pos: +d.pos, label: t("apt_floor", { n: d.floor }) }); return;
			case "edit-unit": N.forms.unit(N.ix.unit[+d.unit]); return;
			case "new-asset": N.forms.asset(N.ix.unit[+d.unit]); return;
			case "asset-ticket": N.forms.ticket({ unit: +d.unit, asset: d.asset }); return;
			case "asset-edit": N.forms.asset(N.ix.unit[+d.unit], d.asset); return;
			case "new-contact": N.forms.contact(null, d.kind || "tenant"); return;
			case "edit-contact": N.forms.contact(N.ix.contact[+d.id]); return;
			case "del-contact": N.ui.confirm(t("confirm_delete_contact")).then(function (y) { if (y) { N.store.remove("contact", +d.id).then(function () { N.ui.close(true); N.ui.toast(t("deleted")); }); } }); return;
			case "stage": var c0 = N.ix.contact[+d.id]; N.store.save("contact", { id: c0.id, kind: c0.kind, name: c0.name, phone: c0.phone, lang: c0.lang, stage: d.stage, meta: c0.meta || {} }); return;
			case "new-lease": N.forms.lease(null, +d.unit || (u && u.id), +d.contact || 0); return;
			case "edit-lease": N.forms.lease(lease); return;
			case "floor": N.forms.floorCard(+d.prop, +d.floor); return;
			case "floor-back": N.ui.close(); return;
			case "end-lease": N.forms.leaseEnd(lease); return;
			case "renew-lease": N.forms.leaseRenew(lease); return;
			case "dep-receive": case "dep-apply": case "dep-return": N.forms.deposit(lease, name.slice(4)); return;
			case "writeoff": N.forms.writeoff(lease); return;
			case "refund": N.forms.refund(lease); return;
			case "former-money": N.ui.open({ kind: "sheet", title: t("tab_money") + " · " + esc(N.where(N.ix.unit[lease.unit_id] || {})), body: N.moneyTab(lease) }); return;
			case "row-more": N.forms.rowMore(D().ledger.find(function (r) { return r.id === +d.row; })); return;
			case "pay": N.forms.payment({ lease: d.lease, charge: d.charge }); return;
			case "expense": N.forms.expense({ prop: +d.prop || 0 }); return;
			case "charge": N.forms.charge({ lease: d.lease }); return;
			case "new-ticket": N.forms.ticket({ unit: +d.unit || 0 }); return;
			case "upload": N.forms.upload(d.scope, d.id); return;
			case "note": N.forms.note(d.scope, d.id); return;
			case "cheque-dep": N.store.money("ledger-act", { id: +d.row, act: "deposit", data: { date: N.todayIso() } }).then(function () { N.ui.toast(t("cheque_deposited")); }).catch(function (x) { N.ui.toast(x.message, "bad"); }); return;
			case "confirm-pay": N.store.money("ledger-act", { id: +d.row, act: "confirm" }).then(function () { N.ui.toast(t("pay_confirmed")); }).catch(function (x) { N.ui.toast(x.message, "bad"); }); return;
			case "wa-remind": N.sendWA(ten, "rent_reminder", { amount: N.moneyText(Math.max(N.balance(lease), lease.rent)), month: N.monthName(N.ym(0)), unit: u.label, pay: payLine(me, ten) }, ["lease", lease.id]); return;
			case "wa-renew": N.sendWA(ten, "renewal", { unit: u.label, end: N.dateText(lease.end_date) }, ["lease", lease.id]); return;
			case "wa-contact": var c1 = N.ix.contact[+d.id]; if (c1) { e.preventDefault(); N.sendWA(c1, "hello", {}, ["contact", c1.id]); } return;
			case "wa-ticket": var tk = D().tickets.find(function (x) { return x.id === +d.ticket; }), uu = N.ix.unit[tk.unit_id], ll = N.ix.leaseByUnit[uu.id]; N.sendWA(N.tenantsOf(ll)[0], "ticket_update", { title: tk.title, status: N.msg("st_" + tk.status, (N.tenantsOf(ll)[0] || {}).lang || "he", {}) }, ["ticket", tk.id]); return;
			case "portal-link": N.shareLink("tenant", "lease", lease.id, ten, "portal_invite", { unit: u.label }); return;
			case "sign-link": var tl = Object.assign({}, lease.terms || {}, { sign_sent: N.todayIso() }); N.store.save("lease", { id: lease.id, unit_id: lease.unit_id, terms: tl }); N.shareLink("sign", "lease", lease.id, ten, "sign_invite", { unit: u.label }); return;
			case "apply-link": N.shareLink("apply", "unit", u.id, null, "apply_invite", { unit: N.where(u) }); return;
			case "vendor-link": var tv = D().tickets.find(function (x) { return x.id === +d.ticket; }); var vv = tv.vendor_id ? N.ix.contact[tv.vendor_id] : null; if (!vv) { N.ui.toast(t("choose_vendor_first"), "bad"); return; } N.shareLink("vendor", "ticket", tv.id, vv, "vendor_dispatch", { title: tv.title, where: N.where(N.ix.unit[tv.unit_id] || {}) }); return;
			case "quick-link":
				if (!me.phone && !D().demo) { N.ui.toast(t("quick_need_phone"), "bad"); N.go("settings"); return; }
				N.shareLink("owner", "", 0, { id: 0, name: me.display || t("me"), phone: me.phone || "972500000999", lang: N.lang }, "owner_quick", {}); return;
			case "publish": location.href = ((N.state.cfg.urls || {}).wizard || "/post-listing/") + "?from=rentals&unit=" + (u ? u.id : ""); return;
			case "tstatus": var tt = D().tickets.find(function (x) { return x.id === +d.id; }); N.store.save("ticket", { id: tt.id, status: d.status }).then(function () { N.ui.toast(t("saved")); if (d.status === "done" && tt.cost) { N.ui.confirm(t("cost_to_expense", { amount: N.moneyText(tt.cost) })).then(function (y) { if (y) { N.store.save("ledger", { property_id: tt.property_id, unit_id: tt.unit_id, kind: "expense", category: "repair", amount: tt.cost * 100, paid_date: N.todayIso(), status: "paid", note: tt.title }); } }); } }); return;
			case "ticket-vendor": var tq = D().tickets.find(function (x) { return x.id === +d.id; }); var vend = D().contacts.filter(function (c) { return c.kind === "vendor"; });
				N.ui.form({ title: t("choose_vendor"), fields: [{ name: "vendor", label: t("f_vendor"), type: "select", value: tq.vendor_id || (vend[0] || {}).id, options: vend.map(function (c) { return [c.id, c.name + (c.tags ? " · " + t("trade_" + c.tags) : "")]; }).concat([[0, t("vendor_new")]]) }, { name: "visit", label: t("f_visit"), type: "datetime-local", value: "" }], onSubmit: function (v) {
					if (!+v.vendor) { N.ui.close(true); N.forms.contact(null, "vendor"); return false; }
					return N.store.save("ticket", { id: tq.id, vendor_id: +v.vendor, status: v.visit ? "scheduled" : tq.status, meta: Object.assign({}, tq.meta || {}, { visit_at: v.visit.replace("T", " ") }) });
				} }); return;
			case "ticket-cost": var tc = D().tickets.find(function (x) { return x.id === +d.id; }); N.ui.form({ title: t("set_cost"), fields: [{ name: "cost", label: t("f_cost"), type: "number", value: tc.cost || "", required: true }], onSubmit: function (v) { return N.store.save("ticket", { id: tc.id, cost: +v.cost }); } }); return;
			case "cpi-lease":
				var lk = lease;
				N.store.cpi(lk.rent, lk.linkage.base_date || lk.start_date, N.todayIso()).then(function (r) {
					var pct = (lk.linkage.pct || 100) / 100, nw = lk.rent * (1 + pct * (r.factor - 1)); if (lk.linkage.floor) { nw = Math.max(lk.rent, nw); }
					N.ui.open({ kind: "sheet", title: t("cpi_title"), body: '<p class="nlrm-lead">' + esc(t("cpi_lease_result", { from: r.from_index_date, to: r.to_index_date, pct: r.change_percent, linked: lk.linkage.pct || 100 })) + '</p><div class="nlrm-kpis" style="grid-template-columns:1fr 1fr"><div class="nlrm-kpi"><span>' + esc(t("f_rent")) + "</span><b>" + N.money(lk.rent) + '</b></div><div class="nlrm-kpi"><span>' + esc(t("cpi_new_rent")) + "</span><b>" + N.money(Math.round(nw)) + "</b></div></div><p class=\"nlrm-note\">" + esc(r.demo ? t("cpi_demo") : t("cpi_source")) + "</p>" });
				}).catch(function () { N.ui.toast(t("cpi_fail"), "bad"); }); return;
			case "lease-doc": N.printDoc(t("lease_doc"), N.leaseHtml ? N.leaseHtml(lease, ten && ten.lang) : "<h1>" + esc(t("lease_doc")) + "</h1>"); return;
			case "receipt": N.printDoc(t("payment_confirm_doc"), receiptHtml(lease)); return;
			case "rep-roll": N.printDoc(t("rep_roll"), rentRollHtml()); return;
			case "rep-year":
				/* this year or last year (January to April the accountant needs last year's) */
				var y0 = N.today().getFullYear(), yo = [String(y0), String(y0 - 1)].map(function (y) { return [y, y]; });
				N.ui.form({ title: t("rep_year_pick"), fields: [{ name: "y", label: t("f_year"), type: "select", options: yo, value: String(N.today().getMonth() < 4 ? y0 - 1 : y0) }], submit: t("rep_open"), onSubmit: function (v) { N.printDoc(t("rep_year", { y: v.y }), yearHtml(v.y)); return Promise.resolve(); } }); return;
			case "rep-evidence": var lo = D().leases.map(function (l) { return [l.id, N.where(N.ix.unit[l.unit_id] || {}) + " · " + ((N.tenantsOf(l)[0] || {}).name || "")]; }); N.ui.form({ title: t("rep_evidence"), fields: [{ name: "l", label: t("f_lease"), type: "select", options: lo, value: (lo[0] || [])[0] }], submit: t("rep_open"), onSubmit: function (v) { var L = D().leases.find(function (x) { return x.id === +v.l; }); N.printDoc(t("rep_evidence"), N.store.adapter.evidence ? N.store.adapter.evidence(L.id).then(function (full) { return evidenceHtml(L, full); }) : evidenceHtml(L)); return Promise.resolve(); } }); return;
			case "csv-roll": download("rent-roll.csv", csv([[t("col_unit"), t("col_tenant"), t("col_rent"), t("f_start"), t("f_end"), t("balance")]].concat(D().units.map(function (u2) { var l2 = N.ix.leaseByUnit[u2.id], c2 = l2 ? N.tenantsOf(l2)[0] : null; return [N.where(u2), c2 ? c2.name : "", l2 ? l2.rent : "", l2 ? l2.start_date : "", l2 ? l2.end_date : "", l2 ? N.balance(l2) : ""]; })))); return;
			case "csv-ledger":
				/* for the accountant: headings and values in the interface language, not codes (HAD-401) */
				var tx = function (pre, v) { if (!v) { return ""; } var k = pre + v, o = t(k); return o === k ? v : o; };
				download(t("csv_ledger_name") + ".csv", csv([[t("col_date"), t("col_property"), t("col_unit"), t("col_kind"), t("f_category"), t("f_amount"), t("f_method"), t("f_ref"), t("col_status"), t("notes")]].concat(D().ledger.map(function (r) { return [r.paid_date || r.due_date, (N.ix.prop[r.property_id] || {}).address || "", (N.ix.unit[r.unit_id] || {}).label || "", tx("kind_", r.kind), tx("cat_", r.category), (r.amount / 100).toFixed(2), tx("m_", r.method), r.ref, tx("ls_", r.status), r.note]; })))); return;
			case "export-all": var ex = N.store.adapter.exportAll ? N.store.adapter.exportAll() : Promise.resolve(D()); ex.then(function (j) { download("nadlan-rentals-export.json", JSON.stringify(j, null, 2), "application/json"); }); return;
			case "link-revoke": N.ui.confirm(t("link_revoke_q"), t("link_revoke")).then(function (y) { if (y) { N.store.revokeLink(+d.link).then(function () { N.ui.toast(t("link_revoked")); }).catch(function (e) { N.ui.toast(e.message || t("err_generic"), "bad"); }); } }); return;
			case "erase":
				N.ui.form({ title: t("set_erase"), intro: esc(t("erase_lead")), fields: [{ name: "confirm", label: t("erase_type"), required: true, ltr: true }], submit: t("set_erase"), onSubmit: function (v) {
					if (v.confirm !== "ERASE") { return Promise.reject(new Error(t("erase_type"))); }
					return (N.store.adapter.erase ? N.store.adapter.erase() : Promise.resolve()).then(function () { location.reload(); });
				} }); return;
			case "screen-tips": N.ui.open({ kind: "sheet", title: t("screen_tips"), body: '<div class="nlrm-lead" style="white-space:pre-wrap">' + esc(t("screen_tips_body")) + '</div><p><a href="https://www.boi.org.il/" target="_blank" rel="noopener">' + esc(t("boi_check")) + "</a></p>" }); return;
			case "doc-open":
				var url = N.store.adapter.docUrl ? N.store.adapter.docUrl(+d.id, true) : null;
				if (url) { window.open(url, "_blank", "noopener"); } else { N.ui.toast(t("doc_demo")); } return;
			case "doc-share":
				var doc = D().docs.find(function (x) { return x.id === +d.id; }), ls = D().leases.find(function (l) { return l.id === doc.scope_id; }), terms = Object.assign({}, ls.terms || {}), sh = (terms.shared_docs || []).slice(), ix = sh.indexOf(doc.id);
				if (ix >= 0) { sh.splice(ix, 1); } else { sh.push(doc.id); }
				terms.shared_docs = sh;
				N.store.save("lease", { id: ls.id, unit_id: ls.unit_id, terms: terms }).then(function () { N.ui.toast(ix >= 0 ? t("unshared") : t("shared")); }); return;
			case "doc-del": N.ui.confirm(t("confirm_delete_doc")).then(function (y) { if (y) { N.store.removeDoc(+d.id).then(function () { N.ui.toast(t("deleted")); }); } }); return;
		}
	};
	function payLine(me, c) {
		var p = me.pay || {}, lang = (c && c.lang) || "he", out = [];
		if (p.bit) { out.push(N.msg("pay_bit", lang, { bit: N.phoneShow(p.bit) })); }
		if (p.bank) { out.push(N.msg("pay_bank", lang, { bank: p.bank })); }
		if (p.link) { out.push(p.link); }
		return out.join("\n");
	}
})();
