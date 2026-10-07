/* ============================================================================
   NADLAN RENTALS v2 - the lease document (HAD-383, 1.10.2026)
   Renders assets/rentals/i18n/lease.json (one template, Hebrew authoritative,
   English translation) from a lease. inc/rentals/lease.php renders the same
   template the same way on the server; the server's text is the one signed.
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM, esc = N.esc;
	N.LEASE = N.LEASE || null;

	function fill(s, v) { return String(s || "").replace(/\{\{([a-z_]+)\}\}/g, function (m, k) { return v[k] == null ? "" : String(v[k]); }); }
	function money(n, lang) { n = Math.round(+n || 0); var s = n.toLocaleString("en-US"); return lang === "he" ? s + " ₪" : "₪" + s; }
	function dateOf(iso, lang) {
		if (!iso) { return ""; }
		var p = String(iso).slice(0, 10).split("-");
		if (lang === "he") { return +p[2] + "." + +p[1] + "." + p[0]; }
		return new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
	}
	/* the flags and values both renderers compute the same way */
	N.leaseVars = function (data, lang) {
		var T = N.LEASE, W = T.words[lang] || T.words.he, l = data.lease, u = data.unit || {}, p = data.property || {}, m = u.meta || {};
		var sec = l.securities || {}, terms = l.terms || {}, link = l.linkage || {};
		var flags = { cpi: link.mode === "cpi", option: !!l.option_until, pets: !!terms.pets, nopets: !terms.pets, deposit: !!sec.deposit, cheque: !!sec.cheque, note: !!sec.note, guarantors: !!sec.guarantors, bank: !!sec.bank, furnished: !!m.furnished, parking: !!m.parking, storage: !!m.storage };
		var secs = [];
		if (sec.cheque) { secs.push(fill(W.cheque, { n: money(sec.cheque, lang) })); }
		if (sec.note) { secs.push(fill(W.note, { n: money(sec.note, lang) })); }
		if (sec.deposit) { secs.push(fill(W.deposit, { n: money(sec.deposit, lang) })); }
		if (sec.guarantors) { secs.push(W.guarantors); }
		if (sec.bank) { secs.push(W.bank); }
		var methodWords = (data.methods || {})[terms.method || "transfer"] || terms.method || "";
		var v = {
			date: dateOf(data.date, lang), landlord: data.landlord || "", landlord_id: data.landlord_id ? fill(W.id, { id: data.landlord_id }) : "",
			tenants: (data.tenants || []).map(function (c) { return c.name + (c.idno ? fill(W.id, { id: c.idno }) : ""); }).join(W.and),
			address: p.address || "", city: p.city || "", unit_label: u.label || "",
			floor_txt: u.floor ? fill(W.floor, { n: u.floor }) : "", rooms_txt: u.rooms ? fill(W.rooms, { n: u.rooms }) : "",
			extras: (flags.furnished ? W.furnished : "") + (flags.parking ? W.parking : "") + (flags.storage ? W.storage : ""),
			start: dateOf(l.start_date, lang), end: dateOf(l.end_date, lang), option_until: dateOf(l.option_until, lang),
			rent: money(l.rent, lang), pay_day: l.pay_day || 1, method: methodWords,
			link_pct: link.pct || 100, link_base: dateOf(link.base_date || l.start_date, lang), link_every: link.every || 12, link_floor: link.floor ? W.floor_clause : "",
			securities: secs.length ? secs.join(lang === "he" ? ", " : ", ") : W.none
		};
		return { flags: flags, v: v };
	};
	/* -> { title, intro, sections:[{h, ps:[...]}], signatures, footer } */
	N.leaseDoc = function (data, lang) {
		var T = N.LEASE;
		if (!T) { return null; }
		lang = T.title[lang] ? lang : "he";
		var fv = N.leaseVars(data, lang);
		return {
			version: T.version, lang: lang,
			title: T.title[lang], intro: fill(T.intro[lang], fv.v),
			/* the clause numbers run in order whatever optional clause is left out (the same rule as lease.php) */
			sections: (function () { var num = 0; return T.sections.filter(function (s) { return !s.when || fv.flags[s.when]; }).map(function (s) { var h = s.h[lang]; if (/^\d+\.\s*/.test(h)) { num++; h = num + ". " + h.replace(/^\d+\.\s*/, ""); } return { h: h, ps: s.p.map(function (x) { return fill(x[lang], fv.v); }) }; }); })(),
			signatures: T.signatures[lang], footer: T.footer[lang]
		};
	};
	N.leaseDocHtml = function (doc, sigs) {
		if (!doc) { return ""; }
		var h = "<h1>" + esc(doc.title) + "</h1><p>" + esc(doc.intro) + "</p>";
		doc.sections.forEach(function (s) { h += "<h2>" + esc(s.h) + "</h2>" + s.ps.map(function (p) { return "<p>" + esc(p) + "</p>"; }).join(""); });
		h += "<h2>" + esc(doc.signatures) + "</h2>";
		h += (sigs && sigs.length ? sigs : [{ name: "", role: "landlord" }, { name: "", role: "tenant" }]).map(function (s) { return '<p style="margin-top:28px;border-top:1px solid #999;padding-top:6px;max-width:320px">' + esc(s.name || "") + (s.at ? " · " + esc(String(s.at).slice(0, 16)) : "") + "</p>"; }).join("");
		h += '<p style="color:#6b7680;font-size:12px">' + esc(doc.footer) + " · v" + esc(doc.version) + "</p>";
		return h;
	};
	/* the landlord's print view, in the tenant's language when he prefers another */
	N.leaseHtml = function (lease, lang) {
		var d = N.store.d, u = N.ix.unit[lease.unit_id] || {}, p = N.ix.prop[u.property_id] || {}, me = (N.state && N.state.cfg.me) || {};
		var methods = {}; ["transfer", "standing", "cheque", "bit", "paybox", "cash", "card", "other"].forEach(function (k) { methods[k] = ((N.STR[lang || N.lang] || N.T)["m_" + k] || k).toLowerCase(); });
		var doc = N.leaseDoc({ lease: lease, unit: u, property: p, tenants: N.tenantsOf(lease), landlord: me.display || "", landlord_id: me.idno || "", date: N.todayIso(), methods: methods }, lang || N.lang);
		return doc ? N.leaseDocHtml(doc, (lease.signing || {}).parties) : "";
	};
})();
