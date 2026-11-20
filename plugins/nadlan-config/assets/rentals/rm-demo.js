/* ============================================================================
   NADLAN RENTALS v2 - the sample portfolio (HAD-383, 1.10.2026)
   Every date is computed from TODAY, so the sample never goes stale (v1's
   seed froze in July and showed an expired lease by October). Nothing here
   is a real person; phone numbers are in the 050-000-xxxx sample range.
   The demo adapter keeps edits in memory only: try anything, nothing is sent.
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM;

	N.demoData = function (lang) {
		var en = lang !== "he";
		var T = N.todayIso(), id = 0, now = T + " 09:00:00";
		var first = function (iso) { return iso.slice(0, 8) + "01"; };
		var props = [
			{ id: 1, title: "", address: en ? "78 Arlozorov St" : "ארלוזורוב 78", city: en ? "Tel Aviv-Yafo" : "תל אביב-יפו", lat: 32.0866, lng: 34.7807, floors: 5, units_per_floor: 3, meta: { year_built: 1972, elevator: true, shelter: "mamad", parking: false, solar: true, orientation: 0 } },
			{ id: 2, title: "", address: en ? "12 Jabotinsky Rd" : "ז'בוטינסקי 12", city: en ? "Ramat Gan" : "רמת גן", lat: 32.0839, lng: 34.8031, floors: 8, units_per_floor: 4, meta: { year_built: 2009, elevator: true, shelter: "mamad", parking: true, solar: true, orientation: 15 } },
			{ id: 3, title: "", address: en ? "30 HaNevi'im St" : "הנביאים 30", city: en ? "Haifa" : "חיפה", lat: 32.8136, lng: 34.9958, floors: 4, units_per_floor: 2, meta: { year_built: 1958, elevator: false, shelter: "shared", parking: false, solar: true, orientation: -20 } }
		];
		var assets = function (extra) {
			return [
				{ id: "a1", kind: "boiler", label: en ? "Water heater" : "דוד שמש", brand: "Amcor", model: "120L", installed: "2019-05", warranty_until: "2024-05-31", last_service: N.addMonths(T, -8) },
				{ id: "a2", kind: "ac", label: en ? "Living room A/C" : "מזגן בסלון", brand: "Electra", model: "1.25 HP", installed: "2022-06", warranty_until: "2027-06-30", last_service: N.addMonths(T, -11) },
				{ id: "a3", kind: "panel", label: en ? "Electric panel" : "לוח חשמל", brand: "", model: "", installed: "", warranty_until: "", last_service: "" },
				{ id: "a4", kind: "water_meter", label: en ? "Water meter" : "מונה מים", brand: "", model: "", installed: "", warranty_until: "", last_service: "" }
			].concat(extra || []);
		};
		var units = [
			{ id: 11, property_id: 1, label: en ? "Apt 7" : "דירה 7", floor: 3, pos: 0, dir: "west", rooms: 3, sqm: 72, meta: { assets: assets(), furnished: false, parking: false, storage: true } },
			{ id: 12, property_id: 1, label: en ? "Apt 14" : "דירה 14", floor: 5, pos: 1, dir: "south", rooms: 4, sqm: 95, meta: { assets: assets([{ id: "a5", kind: "dishwasher", label: en ? "Dishwasher" : "מדיח כלים", brand: "Bosch", model: "SMS4", installed: "2023-02", warranty_until: "2026-12-31", last_service: "" }]), furnished: true } },
			{ id: 21, property_id: 2, label: en ? "Apt 7" : "דירה 7", floor: 2, pos: 2, dir: "east", rooms: 3.5, sqm: 80, meta: { assets: assets(), parking: true } },
			{ id: 22, property_id: 2, label: en ? "Apt 21" : "דירה 21", floor: 6, pos: 0, dir: "north", rooms: 4, sqm: 100, meta: { assets: assets(), asking_rent: 7200, available_from: N.addDays(T, 14), parking: true, storage: true } },
			{ id: 31, property_id: 3, label: en ? "Apt 3" : "דירה 3", floor: 2, pos: 1, dir: "west", rooms: 2.5, sqm: 60, meta: { assets: assets(), furnished: true } }
		];
		var C = function (o) { return Object.assign({ email: "", idno: "", notes: "", tags: "", meta: {}, stage: "", created_at: now, updated_at: now }, o); };
		var contacts = [
			C({ id: 101, kind: "tenant", name: en ? "The Levi family" : "משפחת לוי", phone: "972500000101", email: "levi.sample@example.com", lang: "he" }),
			C({ id: 102, kind: "tenant", name: en ? "Dana Cohen" : "דנה כהן", phone: "972500000102", lang: "he" }),
			C({ id: 103, kind: "tenant", name: en ? "Ron Mizrahi" : "רון מזרחי", phone: "972500000103", lang: "he" }),
			C({ id: 104, kind: "tenant", name: "Daniel Brooks", phone: "972500000104", email: "daniel.sample@example.com", lang: "en", notes: en ? "Relocated from London, prefers English." : "עבר מלונדון, מעדיף אנגלית." }),
			C({ id: 105, kind: "guarantor", name: en ? "Avi Levi" : "אבי לוי", phone: "972500000105", lang: "he" }),
			C({ id: 106, kind: "prospect", stage: "applied", name: en ? "Noa S." : "נועה ש.", phone: "972500000106", lang: "he", meta: { unit_id: 22, household: en ? "Couple, one child" : "זוג ותינוק", move_in: N.addDays(T, 20) } }),
			C({ id: 107, kind: "prospect", stage: "viewing", name: "Michael R.", phone: "972500000107", lang: "en", meta: { unit_id: 22, viewing_at: N.addDays(T, 2) + " 18:30" } }),
			C({ id: 108, kind: "prospect", stage: "new", name: en ? "Yael B." : "יעל ב.", phone: "972500000108", lang: "he", meta: { unit_id: 22 } }),
			C({ id: 109, kind: "vendor", name: en ? "Yossi Plumbing" : "יוסי אינסטלציה", phone: "972500000109", lang: "he", tags: "plumbing" }),
			C({ id: 110, kind: "vendor", name: en ? "Or Electric" : "אור חשמל", phone: "972500000110", lang: "he", tags: "electric" })
		];
		var L = function (o) { return Object.assign({ status: "active", option_until: null, pay_day: 1, linkage: { mode: "none" }, securities: {}, parties: {}, terms: {}, signing: {}, created_at: now, updated_at: now }, o); };
		var s1 = first(N.addMonths(T, -14)), s2 = N.addMonths(T, -8), s3 = first(N.addMonths(T, -20)), s5 = first(N.addMonths(T, -5));
		var payDay2 = Math.max(1, Math.min(28, N.parse(N.addDays(T, -3)).getDate()));
		var leases = [
			L({ id: 201, unit_id: 11, start_date: s1, end_date: N.addDays(N.addMonths(s1, 24), -1), option_until: N.addDays(N.addMonths(s1, 24), -61), rent: 7800, pay_day: 1,
				linkage: { mode: "cpi", base_date: s1, every: 12, pct: 100, floor: true }, securities: { cheque: 23400, note: 46800, guarantors: true, deposit: 0 },
				parties: { tenants: [101], guarantors: [105] }, terms: { method: "cheque", option_years: 1, pets: false, shared_docs: [301, 302] },
				signing: { parties: [{ name: en ? "The Levi family" : "משפחת לוי", role: "tenant", at: s1 + " 10:12:00", text_sha256: "sample" }] } }),
			L({ id: 202, unit_id: 12, start_date: N.addDays(N.addMonths(T, -10), 0), end_date: N.addDays(T, 75), rent: 6400, pay_day: payDay2,
				securities: { cheque: 19200, deposit: 0 }, parties: { tenants: [102] }, terms: { method: "transfer", option_years: 0, shared_docs: [] } }),
			L({ id: 203, unit_id: 21, start_date: s3, end_date: N.addDays(N.addMonths(s3, 24), -1), rent: 5900, pay_day: 10,
				linkage: { mode: "cpi", base_date: s3, every: 12, pct: 50, floor: true }, securities: { deposit: 21000, bank: true },
				parties: { tenants: [103] }, terms: { method: "transfer", shared_docs: [] } }),
			L({ id: 204, unit_id: 31, start_date: s5, end_date: N.addDays(N.addMonths(s5, 12), -1), rent: 4300, pay_day: 5,
				securities: { cheque: 12900, deposit: 0 }, parties: { tenants: [104] }, terms: { method: "bit", shared_docs: [303] } })
		];
		var ledger = [], add = function (o) { ledger.push(Object.assign({ id: ++id, property_id: 0, unit_id: 0, lease_id: 0, kind: "charge", category: "rent", amount: 0, due_date: null, paid_date: null, method: "", ref: "", status: "open", applies_to: 0, note: "", doc_id: 0, created_at: now, updated_at: now }, o)); return ledger[ledger.length - 1]; };
		id = 1000;
		var curM = N.ym(0);
		leases.forEach(function (l) {
			var u = units.find(function (x) { return x.id === l.unit_id; });
			var m = l.start_date.slice(0, 7), endM = N.ym(0), k = 0;
			while (m <= endM && k++ < 40) {
				var due = m + "-" + String(l.pay_day).padStart(2, "0");
				var amt = l.rent;
				if (l.linkage.mode === "cpi" && m >= N.addMonths(l.start_date, 12).slice(0, 7)) { amt = Math.round(l.rent * (1 + (l.linkage.pct / 100) * 0.031)); }
				var ch = add({ property_id: u.property_id, unit_id: u.id, lease_id: l.id, kind: "charge", amount: amt * 100, due_date: due, auto_key: "rent:" + l.id + ":" + m, note: amt !== l.rent ? (en ? "CPI linkage +3.1%" : "הצמדה למדד +3.1%") : "" });
				var paid = true;
				if (l.id === 202 && m === curM) { paid = false; }
				if (l.id === 203 && m >= N.ym(-1)) { paid = false; }
				if (l.id === 204 && m === curM) { paid = false; add({ property_id: u.property_id, unit_id: u.id, lease_id: l.id, kind: "payment", amount: amt * 100, paid_date: N.addDays(T, -1), method: "bit", status: "pending", note: en ? "Reported by the tenant" : "דווח על ידי השוכר" }); }
				if (l.terms.method === "cheque") {
					add({ property_id: u.property_id, unit_id: u.id, lease_id: l.id, kind: "payment", amount: amt * 100, due_date: due, paid_date: due <= T ? due : null, method: "cheque", ref: String(400120 + k), status: due <= T ? "deposited" : "pending", applies_to: ch.id });
					ch.status = due <= T ? "paid" : "open";
				} else if (paid && due <= T) {
					add({ property_id: u.property_id, unit_id: u.id, lease_id: l.id, kind: "payment", amount: amt * 100, paid_date: N.addDays(due, 1), method: l.terms.method, status: "paid", applies_to: ch.id });
					ch.status = "paid";
				}
				m = N.addMonths(m + "-01", 1).slice(0, 7);
			}
			if (l.terms.method === "cheque") {
				for (var j = 1; j <= 3; j++) {
					var fm = N.ym(j), fdue = fm + "-" + String(l.pay_day).padStart(2, "0");
					add({ property_id: u.property_id, unit_id: u.id, lease_id: l.id, kind: "payment", amount: Math.round(l.rent * 1.031) * 100, due_date: fdue, method: "cheque", ref: String(400140 + j), status: "pending" });
				}
			}
		});
		/* a cheque that should be deposited tomorrow */
		var tom = ledger.find(function (r) { return r.lease_id === 201 && r.kind === "payment" && r.status === "pending"; });
		if (tom) { tom.due_date = N.addDays(T, 1); }
		for (var e = 0; e < 3; e++) {
			add({ property_id: 2, unit_id: 22, kind: "expense", category: "arnona", amount: 52000, paid_date: N.addDays(first(N.addMonths(T, -e)), 4), status: "paid", note: en ? "Municipal tax while vacant" : "ארנונה בזמן שהדירה פנויה" });
		}
		add({ property_id: 1, unit_id: 11, kind: "expense", category: "repair", amount: 180000, paid_date: N.addMonths(T, -2), status: "paid", note: en ? "Bedroom painting" : "צביעת חדר שינה" });
		add({ property_id: 1, kind: "expense", category: "insurance", amount: 110000, paid_date: N.addMonths(T, -4), status: "paid", note: en ? "Building insurance, yearly" : "ביטוח מבנה, שנתי" });
		add({ property_id: 2, unit_id: 21, kind: "expense", category: "vaad", amount: 32000, paid_date: N.addDays(first(T), 2), status: "paid", note: en ? "Building committee" : "ועד בית" });

		var tickets = [
			{ id: 501, property_id: 2, unit_id: 21, title: en ? "Water heater does not heat" : "הדוד לא מחמם מים", body: en ? "No hot water since yesterday evening." : "אין מים חמים מאתמול בערב.", category: "boiler", urgency: "urgent", status: "new", reporter: "tenant", vendor_id: 0, cost: 0, due_by: N.addDays(T, 2), opened_at: N.addDays(T, -1) + " 08:10:00", closed_at: null, meta: { triage: { category: "boiler", urgency: "urgent", pro: en ? "Water-heater technician" : "טכנאי דודים", by: "rules" }, asset: "a1" }, updated_at: now },
			{ id: 502, property_id: 1, unit_id: 12, title: en ? "Kitchen tap drips" : "טפטוף בברז המטבח", body: "", category: "plumbing", urgency: "standard", status: "scheduled", reporter: "tenant", vendor_id: 109, cost: 0, due_by: N.addDays(T, 5), opened_at: N.addDays(T, -25) + " 19:40:00", closed_at: null, meta: { visit_at: N.addDays(T, 1) + " 16:00" }, updated_at: now },
			{ id: 503, property_id: 1, unit_id: 11, title: en ? "Bedroom painting" : "צביעת חדר שינה", body: "", category: "paint", urgency: "standard", status: "done", reporter: "owner", vendor_id: 0, cost: 1800, due_by: N.addMonths(T, -2), opened_at: N.addMonths(T, -3) + " 10:00:00", closed_at: N.addMonths(T, -2) + " 17:00:00", meta: {}, updated_at: now },
			{ id: 504, property_id: 3, unit_id: 31, title: "Bathroom fan not working", body: "The fan makes noise and stopped.", category: "electric", urgency: "standard", status: "progress", reporter: "tenant", vendor_id: 110, cost: 0, due_by: N.addDays(T, 24), opened_at: N.addDays(T, -6) + " 12:00:00", closed_at: null, meta: {}, updated_at: now }
		];
		var docs = [
			{ id: 301, scope: "lease", scope_id: 201, kind: "lease", name: en ? "Signed lease.pdf" : "חוזה שכירות חתום.pdf", mime: "application/pdf", size: 412000, created_by: "u:1", created_at: s1 + " 10:15:00" },
			{ id: 302, scope: "lease", scope_id: 201, kind: "protocol", name: en ? "Move-in protocol with photos.pdf" : "פרוטוקול מסירה עם תמונות.pdf", mime: "application/pdf", size: 2380000, created_by: "u:1", created_at: s1 + " 12:00:00" },
			{ id: 303, scope: "lease", scope_id: 204, kind: "lease", name: "Lease - Hebrew and English.pdf", mime: "application/pdf", size: 380000, created_by: "u:1", created_at: s5 + " 11:00:00" },
			{ id: 304, scope: "property", scope_id: 1, kind: "insurance", name: en ? "Building insurance policy.pdf" : "פוליסת ביטוח מבנה.pdf", mime: "application/pdf", size: 220000, created_by: "u:1", created_at: N.addMonths(T, -4) + " 09:00:00" },
			{ id: 305, scope: "unit", scope_id: 11, kind: "nesach", name: en ? "Land registry extract.pdf" : "נסח טאבו.pdf", mime: "application/pdf", size: 98000, created_by: "u:1", created_at: N.addMonths(T, -14) + " 09:00:00" },
			{ id: 306, scope: "ticket", scope_id: 501, kind: "photo", name: en ? "Heater photo.jpg" : "תמונת הדוד.jpg", mime: "image/jpeg", size: 640000, created_by: "link:7", created_at: N.addDays(T, -1) + " 08:11:00" }
		];
		var ev = function (o) { return Object.assign({ id: ++id, actor: "u:1", meta: {}, channel: "", body: "" }, o); };
		var events = [
			ev({ scope: "ticket", scope_id: 501, type: "msg_in", channel: "portal", body: en ? "No hot water since yesterday evening." : "אין מים חמים מאתמול בערב.", at: N.addDays(T, -1) + " 08:10:00", actor: "link:7" }),
			ev({ scope: "lease", scope_id: 203, type: "msg_out", channel: "whatsapp", body: en ? "Friendly reminder about the rent." : "תזכורת ידידותית לשכר הדירה.", at: N.addDays(T, -12) + " 10:00:00" }),
			ev({ scope: "lease", scope_id: 204, type: "msg_in", channel: "portal", body: "Paid via Bit this morning, thanks!", at: N.addDays(T, -1) + " 09:30:00", actor: "link:9" }),
			ev({ scope: "contact", scope_id: 106, type: "note", body: en ? "Called, very serious. Works at a hospital." : "דיברנו בטלפון, רצינית מאוד. עובדת בבית חולים.", at: N.addDays(T, -2) + " 17:20:00" }),
			ev({ scope: "lease", scope_id: 201, type: "sign", channel: "portal", body: en ? "The Levi family" : "משפחת לוי", at: s1 + " 10:12:00", actor: "link:3" })
		];
		return { properties: props, units: units, contacts: contacts, leases: leases, ledger: ledger, tickets: tickets, tasks: [], docs: docs, events: events, plan: { id: "pro", limits: { units: 50 } }, role: "owner", key_ok: true, demo: true };
	};

	/* the demo adapter: same interface as REST, everything in memory */
	N.DemoAdapter = function (lang) {
		var seq = 9000, data = null;
		var err = function (k, v) { var e = new Error(N.t(k, v)); e.status = 409; return e; };
		var leaseOf = function (id) { var l = data.leases.find(function (x) { return +x.id === +id; }); if (!l) { throw err("err_generic"); } return l; };
		var unitOf = function (l) { return data.units.find(function (x) { return +x.id === +l.unit_id; }) || {}; };
		var rowsOf = function (lid) { return data.ledger.filter(function (r) { return +r.lease_id === +lid; }); };
		var sumOf = function (lid) { return N.mx.fold(rowsOf(lid), N.todayIso()).sum; };
		var line = function (l, o) {
			var u = unitOf(l), r = Object.assign({ id: ++seq, property_id: u.property_id || 0, unit_id: l.unit_id, lease_id: l.id, kind: "payment", category: "rent", amount: 0, due_date: null, paid_date: N.todayIso(), method: "", ref: "", status: "paid", applies_to: 0, note: "", doc_id: 0, auto_key: "", created_at: N.todayIso() + " 12:00:00", updated_at: N.todayIso() + " 12:00:00" }, o);
			data.ledger.push(r);
			return r;
		};
		var pack = function (lid, row) {
			var f = N.mx.fold(rowsOf(lid), N.todayIso()), m = {};
			m[lid] = f.sum;
			return { lease_id: +lid, money: m, rows: rowsOf(lid), lease: data.leases.find(function (x) { return +x.id === +lid; }), row: row };
		};
		/* the sample's rent run: the server's periods; linkage in the sample uses its fixed sample index */
		var rentRun = function (l) {
			if (!l.start_date || !l.rent || (l.status !== "active" && l.status !== "ended")) { return []; }
			var made = [], u = unitOf(l);
			N.mx.periods(l, N.mx.monthEnd(N.todayIso())).forEach(function (p) {
				if (data.ledger.some(function (r) { return r.auto_key === p.key || r.auto_key === p.key + ":p"; })) { return; }
				var a = N.mx.amount(l, p, function (from, to) { return Math.pow(1.0025, Math.max(0, N.mx.dayDiff(from, to)) / 30.44); });
				made.push(line(l, { kind: "charge", amount: a.amount, due_date: p.due, paid_date: null, status: "open", auto_key: p.key, note: p.used < p.days ? p.used + "/" + p.days : "" }));
			});
			return made;
		};
		var money = function (path, b) {
			var d = b.data || {}, t = N.todayIso(), ag = Math.round((+d.amount || 0) * 100), l, sum, r;
			if (path === "pay") {
				l = leaseOf(d.lease_id);
				if (ag <= 0) { throw err("err_amount"); }
				var date = d.paid_date || t, cheque = d.method === "cheque";
				r = line(l, { kind: "payment", category: d.category || "rent", amount: ag, paid_date: cheque && date > t ? null : date, due_date: cheque ? date : null, method: d.method || "transfer", ref: d.ref || "", note: d.note || "", status: (cheque && date > t) || d.status === "pending" ? "pending" : "paid" });
				return pack(l.id, r);
			}
			if (path === "ledger-act") {
				r = data.ledger.find(function (x) { return +x.id === +b.id; });
				if (!r) { throw err("err_generic"); }
				if (b.act === "deposit" || b.act === "confirm") { if (r.status !== "pending") { throw err("err_generic"); } r.status = r.method === "cheque" ? "deposited" : "paid"; r.paid_date = r.paid_date || (d.date || t); }
				else if (b.act === "bounce") {
					r.status = "bounced";
					var fee = Math.round((+d.fee || 0) * 100);
					if (fee > 0 && r.lease_id) { line(leaseOf(r.lease_id), { kind: "charge", category: "fee", amount: fee, due_date: d.date || t, paid_date: null, status: "open", applies_to: r.id, note: "bounce " + (r.ref || "") }); }
				} else if (b.act === "void") {
					if (!d.reason) { throw err("err_required", { field: N.t("f_void_reason") }); }
					r.status = "void"; r.note = (r.note ? r.note + " · " : "") + "void: " + d.reason;
				}
				return pack(r.lease_id, r);
			}
			if (path === "deposit") {
				l = leaseOf(b.lease_id); sum = sumOf(l.id);
				if (ag <= 0) { throw err("err_amount"); }
				if (b.act === "receive") {
					var cap = Math.min(3 * l.rent * 100, Math.floor(Math.max(1, Math.round(N.mx.dayDiff(l.start_date, N.addDays(l.end_date || N.addMonths(l.start_date, 12), 1)) / 30.44)) * l.rent * 100 / 3));
					if (sum.deposit_held + ag > cap) { throw err("dep_over_cap", { cap: N.agText(cap) }); }
					return pack(l.id, line(l, { kind: "payment", category: "deposit", amount: ag, method: d.method || "transfer", paid_date: d.date || t, note: d.note || "" }));
				}
				if (ag > sum.deposit_held) { throw err("dep_over_held", { held: N.agText(sum.deposit_held) }); }
				if (b.act === "apply") { return pack(l.id, line(l, { kind: "payment", category: d.category || "rent", amount: ag, method: "deposit", paid_date: d.date || t, note: d.note || "" })); }
				return pack(l.id, line(l, { kind: "refund", category: "deposit", amount: ag, method: d.method || "transfer", paid_date: d.date || t, note: d.note || "" }));
			}
			if (path === "writeoff") {
				l = leaseOf(b.lease_id); sum = sumOf(l.id);
				ag = d.amount ? ag : sum.balance;
				if (ag <= 0 || ag > sum.balance) { throw err("err_amount"); }
				return pack(l.id, line(l, { kind: "payment", amount: ag, method: "writeoff", note: d.note || "" }));
			}
			if (path === "refund") {
				l = leaseOf(b.lease_id); sum = sumOf(l.id);
				if (ag <= 0 || ag > -sum.balance - sum.future) { throw err("err_amount"); }
				return pack(l.id, line(l, { kind: "refund", category: "rent", amount: ag, method: d.method || "transfer", note: d.note || "" }));
			}
			if (path === "lease-end") {
				l = leaseOf(b.lease_id);
				var end = d.date || t, prorate = d.prorate !== false;
				if (!prorate) { N.mx.periods(Object.assign({}, l, { end_date: null, terms: {} }), "9999-12-31").some(function (p) { if (p.start <= end && p.end >= end) { end = p.end; return true; } return p.start > end; }); }
				l.terms = Object.assign({}, l.terms || {}, { ended: { date: d.date || t, reason: d.reason || "term", contract_end: l.end_date, charged_to: end, deposit_due: N.addDays(d.date || t, 60) } });
				l.status = "ended"; l.end_date = end;
				var per = {};
				N.mx.periods(Object.assign({}, l, { end_date: null, terms: {} }), N.mx.monthEnd(N.addMonths(end, 2))).forEach(function (p) { per[p.key] = p; });
				rowsOf(l.id).forEach(function (x) {
					if (x.kind !== "charge" || x.category !== "rent" || x.status === "void" || !/^rent:/.test(x.auto_key || "")) { return; }
					var key = x.auto_key.replace(/:p$/, ""), p = per[key];
					if (!p || p.start > end) { x.status = "void"; x.note = (x.note ? x.note + " · " : "") + "void: after end"; return; }
					if (p.end > end && key === x.auto_key) {
						var used = N.mx.dayDiff(p.start, end) + 1, amt = N.mx.round(x.amount * used / p.days);
						if (amt !== x.amount) { x.status = "void"; line(l, { kind: "charge", amount: amt, due_date: x.due_date, paid_date: null, status: "open", auto_key: x.auto_key + ":p", note: used + "/" + p.days }); }
					}
				});
				rentRun(l);
				return pack(l.id, null);
			}
			if (path === "lease-renew") {
				l = leaseOf(b.lease_id); sum = sumOf(l.id);
				var start = d.start_date || N.addDays(l.end_date, 1), fin = d.end_date || N.addDays(N.addMonths(start, 12), -1);
				money("lease-end", { lease_id: l.id, data: { date: N.addDays(start, -1), reason: "renewal" } });
				var nl = Object.assign(clone(l), { id: ++seq, status: "active", start_date: start, end_date: fin, rent: +d.rent || l.rent, option_until: null, linkage: Object.assign({}, l.linkage || {}, l.linkage && l.linkage.mode === "cpi" ? { base_date: start } : {}), terms: Object.assign({}, l.terms || {}, { renews: l.id }), signing: {} });
				delete nl.terms.ended;
				data.leases.push(nl);
				l.terms.renewed_by = nl.id;
				if (sum.deposit_held > 0) { line(l, { kind: "refund", category: "deposit", amount: sum.deposit_held, method: "renewal", paid_date: start }); line(nl, { kind: "payment", category: "deposit", amount: sum.deposit_held, method: "renewal", paid_date: start }); }
				rentRun(nl);
				var out = pack(nl.id, null);
				out.old = pack(l.id, null);
				return out;
			}
			throw err("err_generic");
		};
		var clone = function (o) { return JSON.parse(JSON.stringify(o)); };
		var coll = N.COLL;
		return {
			demo: true,
			boot: function () { data = N.demoData(lang); return Promise.resolve(clone(data)); },
			save: function (entity, obj) {
				var list = data[coll[entity]], row;
				if (obj.id) { row = list.find(function (x) { return +x.id === +obj.id; }); Object.assign(row, clone(obj), { updated_at: N.todayIso() + " 12:00:00" }); }
				else { row = Object.assign({ id: ++seq, created_at: N.todayIso() + " 12:00:00", updated_at: N.todayIso() + " 12:00:00", meta: {} }, clone(obj)); if (entity === "ticket") { row.opened_at = row.created_at; } list.push(row); }
				if (entity === "ticket" && (row.status === "done" || row.status === "cancelled")) { row.closed_at = N.todayIso() + " 12:00:00"; }
				return new Promise(function (res) { setTimeout(function () { res(clone(row)); }, 120); });
			},
			afterLease: function (l) {
				return Promise.resolve({ ledger: rentRun(l).map(clone) });
			},
			/* the money actions, in memory, by the server's rules (inc/rentals/money.php) */
			money: function (path, b) {
				b = b || {};
				var res;
				try { res = money(path, b); } catch (e) { return Promise.reject(e); }
				return new Promise(function (ok) { setTimeout(function () { ok(clone(res)); }, 120); });
			},
			del: function (entity, id) { data[coll[entity]] = data[coll[entity]].filter(function (x) { return +x.id !== +id; }); return Promise.resolve({ deleted: true }); },
			event: function (p) { var e = Object.assign({ id: ++seq, actor: "u:1", at: N.todayIso() + " " + new Date().toTimeString().slice(0, 8), meta: {} }, p); data.events.unshift(e); return Promise.resolve(clone(e)); },
			upload: function (file, scope, scopeId, kind) {
				var d = { id: ++seq, scope: scope, scope_id: +scopeId, kind: kind || "other", name: file.name, mime: file.type, size: file.size, created_by: "u:1", created_at: N.todayIso() + " 12:00:00", _url: URL.createObjectURL(file) };
				data.docs.unshift(d); return Promise.resolve(d);
			},
			delDoc: function (id) { data.docs = data.docs.filter(function (x) { return +x.id !== +id; }); return Promise.resolve({ deleted: true }); },
			docUrl: function (id) { var d = data.docs.find(function (x) { return +x.id === +id; }); return d && d._url ? d._url : null; },
			link: function (p) {
				var tok = "sample-" + Math.random().toString(36).slice(2, 12), fr = { tenant: "t", owner: "q", apply: "a", sign: "s", vendor: "v" }[p.purpose] || "t", id = ++seq, until = N.addDays(N.todayIso(), p.purpose === "tenant" ? 365 : 14);
				(data.links = data.links || []).unshift({ id: id, purpose: p.purpose, scope: p.scope, scope_id: +p.scope_id || 0, contact_id: +p.contact_id || 0, expires_at: until, uses: 0, revoked_at: null, created_at: N.todayIso(), last_used_at: null });
				return Promise.resolve({ id: id, url: location.origin + "/my-rentals/?l=1#" + fr + "=" + tok, expires_at: until, demo: true });
			},
			links: function () { return Promise.resolve({ links: clone(data.links || []) }); },
			evidence: function (leaseId) {
				var l = data.leases.find(function (x) { return x.id === +leaseId; }) || {}, ten = ((l.parties || {}).tenants || []);
				return Promise.resolve(clone({ lease_id: +leaseId, rows: data.ledger.filter(function (r) { return r.lease_id === +leaseId; }), events: data.events.filter(function (e) { return (e.scope === "lease" && e.scope_id === +leaseId) || (e.scope === "contact" && ten.indexOf(e.scope_id) >= 0); }).slice().reverse() }));
			},
			revokeLink: function (id) { (data.links || []).forEach(function (x) { if (+x.id === +id) { x.revoked_at = N.todayIso(); } }); return Promise.resolve({ revoked: true }); },
			cpi: function (amount, from, to) {
				/* sample factor; the live account asks the CBS calculator itself */
				var months = Math.max(0, (N.parse(to) - N.parse(from)) / (30.44 * 86400000));
				var f = Math.pow(1.0025, months);
				return Promise.resolve({ factor: f, amount: Math.round(amount * f * 100) / 100, change_percent: Math.round((f - 1) * 1000) / 10, from_index_date: from.slice(0, 7), to_index_date: to.slice(0, 7), source: "sample", demo: true });
			}
		};
	};
})();
