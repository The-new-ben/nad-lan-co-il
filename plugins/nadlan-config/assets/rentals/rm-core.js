/* ============================================================================
   NADLAN RENTALS v2 - core (HAD-383, 1.10.2026)
   window.NLRM: strings, formats, dates, the store (REST or demo adapter),
   derived state (status, balances, the attention list), WhatsApp texts,
   and a small UI kit (drawer, sheet, toast). No framework, no build step.
   Every visible word comes from the string table (he + en at full parity).
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM = window.NLRM || {};

	/* ---------- strings ---------- */
	N.lang = "he";
	N.T = {};
	N.setStrings = function (lang, table) { N.lang = lang || "he"; N.T = table || {}; N.rtl = N.lang === "he" || N.lang === "ar"; };
	N.t = function (key, vars) {
		var s = N.T[key];
		if (s == null) { s = key; }
		if (vars) { Object.keys(vars).forEach(function (k) { s = String(s).split("{" + k + "}").join(vars[k] == null ? "" : vars[k]); }); }
		return s;
	};
	/* plural: key_one / key_many, Hebrew "שנה אחת" vs "3 שנים" */
	N.tn = function (key, n, vars) {
		var v = Object.assign({ n: N.num(n) }, vars || {});
		return N.t(key + (Math.abs(n) === 1 ? "_one" : "_many"), v);
	};
	var esc = N.esc = function (s) {
		return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
	};

	/* ---------- numbers, money, dates ---------- */
	N.locale = function () { return { he: "he-IL", en: "en-GB", fr: "fr-FR", ru: "ru-RU", ar: "ar-IL" }[N.lang] || "he-IL"; };
	N.num = function (n) { return Number(n || 0).toLocaleString(N.lang === "he" ? "en-US" : N.locale() === "ar-IL" ? "en-US" : N.locale(), { maximumFractionDigits: 0 }); };
	/* shekels: Hebrew "7,800 ₪", English "₪7,800" (DS rule: number then ₪ in Hebrew) */
	N.money = function (shekels) {
		var n = Math.round(Number(shekels || 0)), s = N.num(Math.abs(n));
		var neg = n < 0 ? "-" : "";
		/* Hebrew: only the digits are isolated, so ₪ sits after the number in reading order (the site's own pattern, broker-drop.php) */
		return N.rtl ? '<span class="nlrm-money"><span class="nlrm-num">' + neg + s + "</span>&nbsp;₪</span>" : '<span class="nlrm-num">' + neg + "₪" + s + "</span>";
	};
	N.moneyText = function (shekels) {
		var n = Math.round(Number(shekels || 0)), s = N.num(Math.abs(n)), neg = n < 0 ? "-" : "";
		return N.rtl ? neg + s + " ₪" : neg + "₪" + s;
	};
	N.ag = function (agorot) { return N.money(Math.round((agorot || 0) / 100)); };
	N.agText = function (agorot) { return N.moneyText(Math.round((agorot || 0) / 100)); };

	N.today = function () { var d = new Date(); d.setHours(0, 0, 0, 0); return d; };
	N.iso = function (d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
	N.todayIso = function () { return N.iso(N.today()); };
	N.parse = function (s) { if (!s) { return null; } var p = String(s).slice(0, 10).split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); };
	N.addDays = function (iso, n) { var d = N.parse(iso); d.setDate(d.getDate() + n); return N.iso(d); };
	N.addMonths = function (iso, n) { var d = N.parse(iso), day = d.getDate(); d.setDate(1); d.setMonth(d.getMonth() + n); var last = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate(); d.setDate(Math.min(day, last)); return N.iso(d); };
	N.daysTo = function (iso) { if (!iso) { return null; } return Math.round((N.parse(iso) - N.today()) / 86400000); };
	N.ym = function (off) { var d = N.today(); d.setDate(1); d.setMonth(d.getMonth() + (off || 0)); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0"); };
	/* D.M.YYYY in Hebrew (DS rule), "1 Oct 2026" in English */
	N.date = function (iso) {
		if (!iso) { return ""; }
		var d = N.parse(iso);
		if (N.lang === "he" || N.lang === "ar") { return '<span class="nlrm-num">' + d.getDate() + "." + (d.getMonth() + 1) + "." + d.getFullYear() + "</span>"; }
		return d.toLocaleDateString(N.locale(), { day: "numeric", month: "short", year: "numeric" });
	};
	N.dateText = function (iso) { return String(N.date(iso)).replace(/<[^>]+>/g, ""); };
	/* ---------- money: the browser twin of inc/rentals/money.php ----------
	   Same rules, same order, same rounding (scripts/rentals/sim proves it:
	   parity.js folds every lease of the 10-year run and compares to PHP). */
	N.mx = {};
	N.mx.dayDiff = function (a, b) {
		var pa = String(a).split("-"), pb = String(b).split("-");
		return Math.round((Date.UTC(+pb[0], +pb[1] - 1, +pb[2]) - Date.UTC(+pa[0], +pa[1] - 1, +pa[2])) / 86400000);
	};
	N.mx.monthEnd = function (iso) { var y = +iso.slice(0, 4), m = +iso.slice(5, 7); return iso.slice(0, 8) + String(new Date(Date.UTC(y, m, 0)).getUTCDate()).padStart(2, "0"); };
	/* the rent periods of a lease due on or before horizon (nlrm_lease_periods) */
	N.mx.periods = function (l, horizon) {
		var out = [], start = l.start_date, end = l.end_date || "", pd = Math.max(1, Math.min(28, +l.pay_day || 1)), from = ((l.terms || {}).track_from) || "";
		if (!/^\d{4}-\d{2}-\d{2}$/.test(start || "")) { return out; }
		for (var k = 0; k < 1200; k++) {
			var ps = N.addMonths(start, k);
			if (end && ps > end) { break; }
			if (end && ps === end && k > 0 && +ps.slice(8) < +start.slice(8)) { break; }
			var nx = N.addMonths(start, k + 1), due = ps.slice(0, 8) + String(pd).padStart(2, "0");
			if (k === 0 && due < start) { due = start; }
			if (due > horizon) { break; }
			if (from && due < from) { continue; }
			var days = N.mx.dayDiff(ps, nx), used = days;
			if (end && end < N.addDays(nx, -1)) { used = N.mx.dayDiff(ps, end) + 1; }
			out.push({ k: k, start: ps, end: N.addDays(nx, -1), due: due, days: days, used: used, key: "rent:" + (l.id || 0) + ":" + ps.slice(0, 7) });
		}
		return out;
	};
	/* agorot for one period (nlrm_period_amount); factor(from, to) -> number or null */
	N.mx.amount = function (l, p, factor) {
		var base = Math.round((+l.rent || 0) * 100), amount = base, link = l.linkage || {}, note = "";
		if (link.mode === "cpi") {
			var every = Math.max(1, +link.every || 12), step = Math.floor(p.k / every) * every;
			if (step > 0) {
				var bd = link.base_date || l.start_date, adj = N.addMonths(l.start_date, step), f = factor ? factor(bd, adj) : null;
				if (f == null || !(f > 0)) { note = "cpi?" + bd + ">" + adj; }
				else {
					var pct = Math.max(0, Math.min(100, link.pct == null ? 100 : +link.pct)) / 100, nw = base * (1 + pct * (f - 1));
					if (link.floor == null || link.floor) { nw = Math.max(base, nw); }
					amount = N.mx.round(nw);
				}
			}
		}
		if (p.used < p.days) { amount = N.mx.round(amount * p.used / p.days); }
		return { amount: amount, note: note };
	};
	/* PHP's round(): half away from zero */
	N.mx.round = function (x) { return x < 0 ? -Math.round(-x) : Math.round(x); };
	/* the balance of ONE lease from all its lines (nlrm_money_fold) */
	N.mx.fold = function (rows, today) {
		var s = { due: 0, future: 0, credit: 0, balance: 0, pending: 0, pending_n: 0, deposit_in: 0, deposit_out: 0, deposit_applied: 0, deposit_held: 0, writeoff: 0, refunded: 0, oldest_due: null, late_days: 0, open_n: 0 };
		var charges = [], state = {};
		(rows || []).forEach(function (r) {
			var st = r.status, kind = r.kind, a = parseInt(r.amount, 10) || 0;
			if (st === "void") { return; }
			if (kind === "charge") {
				if (!r.due_date || r.due_date <= today) { s.due += a; } else { s.future += a; }
				charges.push({ id: +r.id, due: r.due_date || "0000-00-00", amount: a });
			} else if (kind === "payment") {
				var ok = st === "paid" || st === "deposited";
				if (r.category === "deposit") { if (ok) { s.deposit_in += a; } return; }
				if (ok) {
					s.credit += a;
					if (r.method === "deposit") { s.deposit_applied += a; }
					if (r.method === "writeoff") { s.writeoff += a; }
				} else if (st === "pending") { s.pending += a; s.pending_n++; }
			} else if (kind === "refund") {
				if (r.category === "deposit") { s.deposit_out += a; } else { s.credit -= a; s.refunded += a; }
			}
		});
		s.balance = s.due - s.credit;
		s.deposit_held = s.deposit_in - s.deposit_out - s.deposit_applied;
		charges.sort(function (x, y) { return x.due < y.due ? -1 : x.due > y.due ? 1 : x.id - y.id; });
		var left = s.credit;
		charges.forEach(function (c) {
			if (c.amount <= 0) { state[c.id] = ["paid", c.amount]; left -= c.amount; return; }
			var cover = Math.max(0, Math.min(c.amount, left));
			left -= cover;
			var st = cover >= c.amount ? "paid" : (cover > 0 ? "partial" : "open");
			state[c.id] = [st, cover];
			if (st !== "paid" && c.due <= today) {
				s.open_n++;
				if (s.oldest_due === null) { s.oldest_due = c.due === "0000-00-00" ? null : c.due; }
			}
		});
		if (s.oldest_due && s.balance > 0) { s.late_days = Math.max(0, N.mx.dayDiff(s.oldest_due, today)); }
		return { sum: s, state: state };
	};
	/* one line's effect on income (agorot): money that became the landlord's.
	   Deposits held are not income, a write-off is not money, a credit given back reduces it. */
	N.mx.incomeOf = function (r) {
		if (r.status !== "paid" && r.status !== "deposited") { return 0; }
		var a = parseInt(r.amount, 10) || 0;
		if (r.kind === "income") { return a; }
		if (r.kind === "payment") { return r.category === "deposit" || r.method === "writeoff" ? 0 : a; }
		if (r.kind === "refund") { return r.category === "deposit" ? 0 : -a; }
		return 0;
	};
	/* the reports' totals (nlrm_stats): income without deposits or write-offs, minus credits given back */
	N.mx.stats = function (ledger) {
		var out = {};
		(ledger || []).forEach(function (r) {
			if (r.status !== "paid" && r.status !== "deposited") { return; }
			if (["payment", "expense", "income", "refund"].indexOf(r.kind) < 0) { return; }
			var ym = String(r.paid_date || r.due_date || "").slice(0, 7);
			if (!ym) { return; }
			var o = out[ym] = out[ym] || { income: 0, expense: 0, by_cat: {}, by_prop: {} }, a = parseInt(r.amount, 10) || 0, pid = +r.property_id || 0;
			if (r.kind === "refund") { if (r.category === "deposit") { return; } o.income -= a; o.by_cat[r.category] = (o.by_cat[r.category] || 0) - a; o.by_prop[pid] = (o.by_prop[pid] || 0) - a; return; }
			if (r.kind === "expense") { o.expense += a; o.by_cat[r.category] = (o.by_cat[r.category] || 0) - a; o.by_prop[pid] = (o.by_prop[pid] || 0) - a; return; }
			if (r.category === "deposit" || r.method === "writeoff") { return; }
			o.income += a; o.by_cat[r.category] = (o.by_cat[r.category] || 0) + a; o.by_prop[pid] = (o.by_prop[pid] || 0) + a;
		});
		return out;
	};
	N.monthName = function (ym, short) {
		var d = new Date(+ym.slice(0, 4), +ym.slice(5, 7) - 1, 1);
		return d.toLocaleDateString(N.locale(), short ? { month: "short" } : { month: "long", year: "numeric" });
	};
	N.when = function (days) {
		if (days === 0) { return N.t("today"); }
		if (days === 1) { return N.t("tomorrow"); }
		if (days === -1) { return N.t("yesterday"); }
		return days > 0 ? N.tn("in_days", days) : N.tn("days_ago", -days);
	};

	/* ---------- phones and WhatsApp ---------- */
	N.phone = function (raw) {
		var d = String(raw || "").replace(/[^0-9+]/g, "");
		if (!d) { return ""; }
		if (d[0] === "+") { return d.slice(1).replace(/\D/g, ""); }
		if (d.slice(0, 2) === "00") { return d.slice(2); }
		if (d[0] === "0") { return "972" + d.slice(1); }
		return d;
	};
	N.phoneShow = function (e164) {
		var d = String(e164 || "");
		if (d.indexOf("972") === 0 && d.length >= 11) { d = "0" + d.slice(3); return d.slice(0, 3) + "-" + d.slice(3, 6) + "-" + d.slice(6); }
		return d ? "+" + d : "";
	};
	N.wa = function (phone, text) { return "https://wa.me/" + N.phone(phone) + (text ? "?text=" + encodeURIComponent(text) : ""); };
	/* message texts in the RECIPIENT's language (a tenant may be en while the landlord works in he) */
	N.msg = function (kind, lang, v) {
		var S = (N.MSG && (N.MSG[lang] || N.MSG.he)) || {};
		var s = S[kind] || "";
		Object.keys(v || {}).forEach(function (k) { s = s.split("{" + k + "}").join(v[k] == null ? "" : v[k]); });
		return s;
	};

	/* ---------- the store ---------- */
	var ENT = ["property", "unit", "contact", "lease", "ledger", "ticket", "task"];
	var COLL = { property: "properties", unit: "units", contact: "contacts", lease: "leases", ledger: "ledger", ticket: "tickets", task: "tasks" };
	N.COLL = COLL;
	N.store = {
		d: { properties: [], units: [], contacts: [], leases: [], ledger: [], tickets: [], tasks: [], docs: [], events: [], plan: { id: "free", limits: {} }, role: "owner" },
		adapter: null,
		listeners: [],
		on: function (fn) { this.listeners.push(fn); },
		emit: function (why) { N.derive(); this.listeners.forEach(function (fn) { try { fn(why); } catch (e) { console.error(e); } }); },
		load: function () {
			var self = this;
			return this.adapter.boot().then(function (d) { self.d = Object.assign(self.d, d); self.emit("load"); return self.d; });
		},
		byId: function (entity, id) { id = +id; return (this.d[COLL[entity]] || []).find(function (x) { return +x.id === id; }) || null; },
		/* a money action's answer: the lease's whole history and its summary */
		applyPack: function (p) {
			if (!p || !p.rows) { return; }
			var d = this.d, lid = +p.lease_id;
			d.ledger = d.ledger.filter(function (r) { return +r.lease_id !== lid; }).concat(p.rows);
			if (p.money && d.money) { Object.keys(p.money).forEach(function (k) { d.money[k] = p.money[k]; }); }
			if (p.lease) { var i = d.leases.findIndex(function (x) { return +x.id === +p.lease.id; }); if (i >= 0) { d.leases[i] = p.lease; } else { d.leases.push(p.lease); } }
			if (p.old) { this.applyPack(p.old); }
		},
		money: function (path, body) {
			var self = this;
			return this.adapter.money(path, body || {}).then(function (p) { self.applyPack(p); self.emit("money:" + path); return p; });
		},
		save: function (entity, obj) {
			var self = this;
			return this.adapter.save(entity, obj).then(function (res) {
				var row = res;
				if (res && res.rows && res.row) { row = res.row; self.applyPack(res); }
				var list = self.d[COLL[entity]], i = list.findIndex(function (x) { return +x.id === +row.id; });
				if (i >= 0) { list[i] = row; } else { list.push(row); }
				return (entity === "lease" && !res.rows && self.adapter.afterLease ? self.adapter.afterLease(row) : Promise.resolve()).then(function (extra) {
					if (extra && extra.ledger) { extra.ledger.forEach(function (r) { var j = self.d.ledger.findIndex(function (x) { return +x.id === +r.id; }); if (j < 0) { self.d.ledger.push(r); } }); }
					self.emit("save:" + entity);
					return row;
				});
			});
		},
		remove: function (entity, id) {
			var self = this;
			return this.adapter.del(entity, id).then(function () {
				self.d[COLL[entity]] = self.d[COLL[entity]].filter(function (x) { return +x.id !== +id; });
				self.emit("delete:" + entity);
			});
		},
		event: function (p) {
			var self = this;
			return this.adapter.event(p).then(function (ev) { if (ev) { self.d.events.unshift(ev); } self.emit("event"); return ev; });
		},
		upload: function (file, scope, scopeId, kind) {
			var self = this;
			return this.adapter.upload(file, scope, scopeId, kind).then(function (doc) { self.d.docs.unshift(doc); self.emit("doc"); return doc; });
		},
		removeDoc: function (id) {
			var self = this;
			return this.adapter.delDoc(id).then(function () { self.d.docs = self.d.docs.filter(function (x) { return +x.id !== +id; }); self.emit("doc"); });
		},
		link: function (p) {
			var self = this;
			return this.adapter.link(p).then(function (lk) {
				if (self.d.links && lk && lk.id) { self.d.links.unshift({ id: lk.id, purpose: p.purpose, scope: p.scope, scope_id: +p.scope_id || 0, contact_id: +p.contact_id || 0, expires_at: lk.expires_at, uses: 0, revoked_at: null, created_at: N.todayIso(), last_used_at: null }); }
				return lk;
			});
		},
		/* the personal links the landlord sent (HAD-401: the app promised "revoke any time" without a button) */
		links: function () { var self = this; return this.adapter.links().then(function (r) { self.d.links = (r && r.links) || []; self.emit("links"); return self.d.links; }); },
		revokeLink: function (id) {
			var self = this;
			return this.adapter.revokeLink(id).then(function (r) { (self.d.links || []).forEach(function (x) { if (+x.id === +id) { x.revoked_at = N.todayIso(); } }); self.emit("links"); return r; });
		},
		cpi: function (amount, from, to) { return this.adapter.cpi(amount, from, to); }
	};

	/* REST adapter (logged-in landlord) */
	N.RestAdapter = function (base, nonce) {
		var lang = N.lang;
		function call(path, opts) {
			opts = opts || {};
			opts.credentials = "same-origin";
			opts.headers = Object.assign({ "X-WP-Nonce": nonce, "X-NLRM-Lang": lang }, opts.body && !(opts.body instanceof FormData) ? { "Content-Type": "application/json" } : {}, opts.headers || {});
			return fetch(base + path, opts).then(function (r) {
				return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) { var e = new Error(j.message || ("HTTP " + r.status)); e.code = j.code; e.status = r.status; throw e; } return j; });
			});
		}
		return {
			boot: function () { return call("/rm/boot"); },
			save: function (entity, data) {
				/* one client_ref per user action, kept across a retry (Maya's B2) */
				var ref = "c" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
				var body = JSON.stringify({ entity: entity, data: data, client_ref: ref });
				return call("/rm/save", { method: "POST", body: body }).catch(function (e) { if (!e.status) { return call("/rm/save", { method: "POST", body: body }); } throw e; });
			},
			del: function (entity, id) { return call("/rm/delete", { method: "POST", body: JSON.stringify({ entity: entity, id: id }) }); },
			event: function (p) { return call("/rm/event", { method: "POST", body: JSON.stringify(p) }); },
			upload: function (file, scope, scopeId, kind) { var f = new FormData(); f.append("file", file); f.append("scope", scope); f.append("scope_id", scopeId); f.append("kind", kind || "other"); return call("/rm/doc", { method: "POST", body: f }); },
			delDoc: function (id) { return call("/rm/doc-delete", { method: "POST", body: JSON.stringify({ id: id }) }); },
			docUrl: function (id, inline) { return base + "/rm/doc/" + id + "?_wpnonce=" + encodeURIComponent(nonce) + (inline ? "&inline=1" : ""); },
			link: function (p) { return call("/rm/link", { method: "POST", body: JSON.stringify(p) }); },
			links: function () { return call("/rm/links"); },
			evidence: function (leaseId) { return call("/rm/evidence?lease_id=" + (+leaseId)); },
			revokeLink: function (id) { return call("/rm/link-revoke", { method: "POST", body: JSON.stringify({ id: id }) }); },
			cpi: function (amount, from, to) { return call("/rm/cpi?amount=" + amount + "&from=" + from + "&to=" + to); },
			money: function (path, b) {
				var body = JSON.stringify(Object.assign({ client_ref: "c" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8) }, b || {}));
				return call("/rm/" + path, { method: "POST", body: body }).catch(function (e) { if (!e.status) { return call("/rm/" + path, { method: "POST", body: body }); } throw e; });
			},
			exportAll: function () { return call("/rm/export"); }
		};
	};

	/* ---------- derived state ---------- */
	N.ix = {};
	N.derive = function () {
		var d = N.store.d, ix = { unitsByProp: {}, leaseByUnit: {}, leasesByUnit: {}, contact: {}, ledgerByLease: {}, ticketsByUnit: {}, docsBy: {}, unit: {}, prop: {} };
		d.properties.forEach(function (p) { ix.prop[p.id] = p; ix.unitsByProp[p.id] = []; });
		d.units.forEach(function (u) { ix.unit[u.id] = u; (ix.unitsByProp[u.property_id] = ix.unitsByProp[u.property_id] || []).push(u); });
		Object.keys(ix.unitsByProp).forEach(function (k) { ix.unitsByProp[k].sort(function (a, b) { return a.floor - b.floor || a.pos - b.pos; }); });
		d.contacts.forEach(function (c) { ix.contact[c.id] = c; });
		d.leases.forEach(function (l) {
			(ix.leasesByUnit[l.unit_id] = ix.leasesByUnit[l.unit_id] || []).push(l);
			if (l.status === "active") { ix.leaseByUnit[l.unit_id] = l; }
		});
		d.ledger.forEach(function (r) { if (r.lease_id) { (ix.ledgerByLease[r.lease_id] = ix.ledgerByLease[r.lease_id] || []).push(r); } });
		d.tickets.forEach(function (t) { (ix.ticketsByUnit[t.unit_id] = ix.ticketsByUnit[t.unit_id] || []).push(t); });
		d.docs.forEach(function (x) { var k = x.scope + ":" + x.scope_id; (ix.docsBy[k] = ix.docsBy[k] || []).push(x); });
		/* money: the server's summaries come from the FULL books; the sample folds its own lines */
		ix.money = {};
		var server = !!d.money && !d.demo, today = N.todayIso();
		d.leases.forEach(function (l) {
			if (server) { ix.money[l.id] = d.money[l.id] || N.mx.fold([], today).sum; return; }
			var f = N.mx.fold(ix.ledgerByLease[l.id] || [], today);
			ix.money[l.id] = f.sum;
			(ix.ledgerByLease[l.id] || []).forEach(function (r) { if (r.kind === "charge" && r.status !== "void" && f.state[r.id]) { r.status = f.state[r.id][0]; r.covered = f.state[r.id][1]; } });
		});
		N.ix = ix;
	};
	N.tenantsOf = function (lease) {
		var ids = ((lease && lease.parties) || {}).tenants || [];
		return ids.map(function (id) { return N.ix.contact[id]; }).filter(Boolean);
	};
	N.guarantorsOf = function (lease) {
		var ids = ((lease && lease.parties) || {}).guarantors || [];
		return ids.map(function (id) { return N.ix.contact[id]; }).filter(Boolean);
	};
	N.leaseOfContact = function (cid) {
		return N.store.d.leases.find(function (l) { return l.status === "active" && (((l.parties || {}).tenants || []).indexOf(+cid) >= 0); }) || null;
	};
	/* the money of a lease (agorot): balance, deposit held, pending, the oldest unpaid due */
	/* the monthly rent-tax exemption ceiling (Income Tax Exemption on Rental Income Law), ONE place to update each January:
	   2025 = 5,654 NIS; accountants quote the same for 2026 (the texts say so). Used by the tax card, the calculator and the yearly summary. */
	N.TAX_CEILING = { amount: 5654, year: 2025 };
	N.moneyOf = function (lease) { return (lease && N.ix.money && N.ix.money[lease.id]) || N.mx.fold([], N.todayIso()).sum; };
	/* balance of a lease in shekels: what is due until today minus what was received (negative = a credit) */
	N.balance = function (lease) { return lease ? Math.round(N.moneyOf(lease).balance / 100) : 0; };
	N.stats = function () { var d = N.store.d; return d.stats && !d.demo ? d.stats : N.mx.stats(d.ledger); };
	N.pendingCheques = function (lease) {
		return (N.ix.ledgerByLease[lease.id] || []).filter(function (r) { return r.kind === "payment" && r.method === "cheque" && r.status === "pending"; });
	};
	/* the colour story of an apartment: vacant / ok / due (this month open) / late (older month open) */
	N.unitStatus = function (u) {
		var l = N.ix.leaseByUnit[u.id];
		if (!l) { return "vacant"; }
		var m = N.moneyOf(l);
		if (m.balance <= 0) { return "ok"; }
		return m.late_days > 10 ? "late" : "due";
	};
	N.STATUS_COLOR = { ok: "#2e7d5b", due: "#b8860b", late: "#b3261e", vacant: "#8a94a0", ending: "#2f6f86" };

	/* the attention list: everything that needs the landlord, most legal risk first */
	N.attention = function () {
		var d = N.store.d, out = [], t = N.todayIso();
		d.units.forEach(function (u) {
			var p = N.ix.prop[u.property_id] || {}, l = N.ix.leaseByUnit[u.id], ten = l ? N.tenantsOf(l)[0] : null;
			var where = (u.label || "") + (p.address ? " · " + p.address : "");
			if (l) {
				var st = N.unitStatus(u), bal = N.balance(l);
				if (st === "late") { out.push({ s: 0, kind: "late", unit: u, lease: l, contact: ten, text: N.t("att_late", { where: where, amount: N.moneyText(bal) }) }); }
				else if (st === "due") { out.push({ s: 4, kind: "due", unit: u, lease: l, contact: ten, text: N.t("att_due", { where: where, amount: N.moneyText(bal) }) }); }
				var de = N.daysTo(l.end_date);
				if (de !== null && de < 0) { out.push({ s: 1, kind: "ended", unit: u, lease: l, contact: ten, text: N.t("att_ended", { where: where }) }); }
				else if (de !== null && de <= 90) { out.push({ s: 2, kind: "ending", unit: u, lease: l, contact: ten, text: N.t("att_ending", { where: where, when: N.when(de) }) }); }
				var dop = N.daysTo(l.option_until);
				if (dop !== null && dop >= 0 && dop <= 60) { out.push({ s: 2, kind: "option", unit: u, lease: l, contact: ten, text: N.t("att_option", { where: where, when: N.when(dop) }) }); }
				N.pendingCheques(l).forEach(function (c) {
					var dd = N.daysTo(c.due_date);
					if (dd !== null && dd <= 2) { out.push({ s: 3, kind: "cheque", unit: u, lease: l, row: c, text: N.t("att_cheque", { where: where, amount: N.agText(c.amount), when: N.when(dd) }) }); }
				});
				var sec = (l.securities || {}), cap = N.secCap(l);
				if (sec.deposit && cap > 0 && sec.deposit > cap) { out.push({ s: 1, kind: "sec", unit: u, lease: l, text: N.t("att_sec", { where: where }) }); }
				var sig = (l.signing || {}).parties || [];
				if (l.terms && l.terms.sign_sent && !sig.length) { out.push({ s: 5, kind: "unsigned", unit: u, lease: l, contact: ten, text: N.t("att_unsigned", { where: where }) }); }
			} else {
				out.push({ s: 6, kind: "vacant", unit: u, text: N.t("att_vacant", { where: where }) });
			}
		});
		d.tickets.forEach(function (tk) {
			if (tk.status === "done" || tk.status === "cancelled") { return; }
			var u = N.ix.unit[tk.unit_id] || {}, dd = N.daysTo(tk.due_by);
			var where = (u.label || "") + (tk.title ? " · " + tk.title : "");
			if (tk.urgency === "urgent") { out.push({ s: dd !== null && dd < 0 ? 0 : 1, kind: "repair_urgent", ticket: tk, unit: u, text: N.t(dd !== null && dd < 0 ? "att_repair_over" : "att_repair_urgent", { where: where, when: N.when(dd || 0) }) }); }
			else if (dd !== null && dd <= 7) { out.push({ s: dd < 0 ? 1 : 3, kind: "repair", ticket: tk, unit: u, text: N.t(dd < 0 ? "att_repair_over" : "att_repair", { where: where, when: N.when(dd) }) }); }
			else if (tk.status === "new") { out.push({ s: 5, kind: "repair_new", ticket: tk, unit: u, text: N.t("att_repair_new", { where: where }) }); }
		});
		d.ledger.forEach(function (r) {
			if (r.kind === "payment" && r.status === "pending" && r.method !== "cheque") {
				var u = N.ix.unit[r.unit_id] || {};
				out.push({ s: 3, kind: "confirm", row: r, unit: u, text: N.t("att_confirm", { where: u.label || "", amount: N.agText(r.amount) }) });
			}
		});
		/* former tenants: a debt is never hidden, a deposit has 60 days to go back (§25י(ה)), a credit goes back */
		d.leases.forEach(function (l) {
			if (l.status !== "ended") { return; }
			var m = N.moneyOf(l), u = N.ix.unit[l.unit_id] || {}, c = N.tenantsOf(l)[0], who = (u.label || "") + (c ? " · " + c.name : "");
			if (m.balance > 0) { out.push({ s: 1, kind: "former_debt", unit: u, lease: l, contact: c, text: N.t("att_former_debt", { where: who, amount: N.agText(m.balance) }) }); }
			if (m.balance < 0 && -m.balance > 100) { out.push({ s: 3, kind: "credit", unit: u, lease: l, contact: c, text: N.t("att_credit_refund", { where: who, amount: N.agText(-m.balance) }) }); }
			if (m.deposit_held > 0) {
				var due = ((l.terms || {}).ended || {}).deposit_due || N.addDays(l.end_date, 60), dd = N.daysTo(due);
				/* from the day the tenant leaves: the 60-day clock is visible, and urgent in its last two weeks */
				if (dd !== null) { out.push({ s: dd < 0 ? 0 : dd <= 14 ? 1 : 4, kind: "deposit_return", unit: u, lease: l, contact: c, text: N.t(dd < 0 ? "att_deposit_over" : "att_deposit_due", { where: who, amount: N.agText(m.deposit_held), when: N.when(dd) }) }); }
			}
		});
		var waiting = d.ledger.filter(function (r) { return r.kind === "charge" && r.status !== "void" && /^cpi\?/.test(r.note || ""); }).length;
		if (waiting) { out.push({ s: 4, kind: "cpi_wait", text: N.t("att_cpi_wait", { n: waiting }) }); }
		d.contacts.forEach(function (c) {
			if (c.kind === "prospect" && c.stage === "applied") { var au = (c.meta || {}).unit_id ? N.ix.unit[c.meta.unit_id] : null; out.push({ s: 5, kind: "applicant", contact: c, unit: au, text: N.t("att_applicant", { name: c.name, where: au ? au.label : "" }) }); }
		});
		var m = N.today().getMonth() + 1;
		if (m === 12 || m === 1) { out.push({ s: 2, kind: "tax", text: N.t("att_tax", { date: N.dateText((N.today().getFullYear() + (m === 12 ? 1 : 0)) + "-01-30") }) }); }
		out.sort(function (a, b) { return a.s - b.s; });
		return out;
	};
	/* חוק השכירות והשאילה s.25י(ב): securities capped at the lower of 3 months' rent or a third of the whole term's rent */
	N.secCap = function (l) {
		if (!l || !l.rent) { return 0; }
		var months = 12;
		if (l.start_date && l.end_date) { months = Math.max(1, Math.round((N.parse(l.end_date) - N.parse(l.start_date)) / (30.44 * 86400000))); }
		return Math.round(Math.min(3 * l.rent, months * l.rent / 3));
	};
	N.kpis = function () {
		var d = N.store.d, m = N.ym(0), expected = 0, collected = 0, open = 0, vacant = 0, units = d.units.length;
		d.ledger.forEach(function (r) {
			if (r.kind === "charge" && r.category === "rent" && r.due_date && r.due_date.slice(0, 7) === m && r.status !== "void") { expected += r.amount; }
			/* collected = money that came in this month for rent and bills (not deposits, not write-offs) */
			if (r.kind === "payment" && (r.status === "paid" || r.status === "deposited") && r.paid_date && r.paid_date.slice(0, 7) === m && r.category !== "deposit" && ["deposit", "writeoff", "renewal"].indexOf(r.method) < 0) { collected += r.amount; }
		});
		/* what tenants owe, including former tenants (a debt does not vanish when the lease ends) */
		d.leases.forEach(function (l) { open += Math.max(0, N.moneyOf(l).balance); });
		open = Math.round(open / 100);
		d.units.forEach(function (u) { if (!N.ix.leaseByUnit[u.id]) { vacant++; } });
		var repairs = d.tickets.filter(function (t) { return t.status !== "done" && t.status !== "cancelled"; }).length;
		return { expected: Math.round(expected / 100), collected: Math.round(collected / 100), open: open, vacant: vacant, units: units, repairs: repairs, props: d.properties.length };
	};

	/* ---------- the UI kit ---------- */
	N.ui = {};
	N.ui.toast = function (text, kind) {
		var host = document.getElementById("nlrm-toasts");
		if (!host) { host = document.createElement("div"); host.id = "nlrm-toasts"; host.setAttribute("role", "status"); host.setAttribute("aria-live", "polite"); document.body.appendChild(host); }
		var el = document.createElement("div");
		el.className = "nlrm-toast" + (kind ? " is-" + kind : "");
		el.textContent = text;
		host.appendChild(el);
		setTimeout(function () { el.classList.add("is-out"); setTimeout(function () { el.remove(); }, 400); }, 3200);
	};
	/* layers: a drawer (a 360 card) and, over it, a sheet (a form). A sheet
	   opened from a card returns to that card, refreshed, when it closes.
	   The phone's back button closes one layer at a time. */
	var layer = null, lastFocus = null, stack = [], selfBack = 0;
	function build(opts) {
		var wrap = document.createElement("div");
		wrap.className = "nlrm-layer nlrm-layer--" + (opts.kind || "drawer");
		wrap.setAttribute("dir", N.rtl ? "rtl" : "ltr");
		wrap.setAttribute("lang", N.lang);
		wrap.innerHTML = '<div class="nlrm-scrim" data-close></div><section class="nlrm-panel" role="dialog" aria-modal="true" aria-labelledby="nlrm-ptitle" tabindex="-1">' +
			'<header class="nlrm-phead"><div class="nlrm-phead-t"><h2 id="nlrm-ptitle">' + (opts.title || "") + "</h2>" + (opts.sub ? '<p class="nlrm-psub">' + opts.sub + "</p>" : "") + '</div><button type="button" class="nlrm-x" data-close aria-label="' + esc(N.t("close")) + '"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></button></header>' +
			(opts.actions ? '<div class="nlrm-pacts">' + opts.actions + "</div>" : "") +
			(opts.tabs ? '<nav class="nlrm-ptabs" role="tablist">' + opts.tabs.map(function (tb, i) { return '<button type="button" role="tab" data-tab="' + tb.id + '" aria-selected="' + (i === (opts.tab || 0) ? "true" : "false") + '">' + esc(tb.label) + (tb.badge ? ' <i class="nlrm-badge">' + tb.badge + "</i>" : "") + "</button>"; }).join("") + "</nav>" : "") +
			'<div class="nlrm-pbody"></div></section>';
		document.body.appendChild(wrap);
		document.documentElement.classList.add("nlrm-locked");
		var L = { el: wrap, opts: opts };
		var body = wrap.querySelector(".nlrm-pbody");
		L.show = function (id) {
			wrap.querySelectorAll("[data-tab]").forEach(function (b) { b.setAttribute("aria-selected", b.dataset.tab === id ? "true" : "false"); });
			var tb = (opts.tabs || []).find(function (x) { return x.id === id; });
			body.innerHTML = tb ? tb.render() : (opts.body || "");
			body.scrollTop = 0;
			if (tb && tb.wire) { tb.wire(body); }
			L.tab = id;
		};
		wrap.addEventListener("click", function (e) {
			if (e.target.closest("[data-close]")) { e.preventDefault(); N.ui.close(); return; }
			var tb = e.target.closest("[data-tab]");
			if (tb) { L.show(tb.dataset.tab); return; }
			if (e.target.closest("[data-sheet-act],[data-more],[data-send],[data-copy],[data-yes]")) { return; }
			var a = e.target.closest("[data-act]");
			if (a && N.act) { N.act(a.dataset.act, a, e); return; }
			var o = e.target.closest("[data-open]");
			if (o && N.open) { var oo = o.dataset.open.split(":"); N.open(oo[0], +oo[1]); return; }
			var g = e.target.closest("[data-go],[data-go-prop]");
			if (g && N.go) { stack = []; N.ui.close(true); if (g.dataset.goProp) { N.go("property", g.dataset.goProp); } else { N.go(g.dataset.go); } }
		});
		wrap.addEventListener("keydown", function (e) {
			if (e.key === "Tab") {
				var f = wrap.querySelectorAll('button,a[href],input,select,textarea,[tabindex]:not([tabindex="-1"])');
				if (!f.length) { return; }
				if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
				else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
			}
		});
		if (opts.tabs) { L.show(opts.tabs[Math.max(0, opts.tab || 0)].id); } else { body.innerHTML = opts.body || ""; if (opts.wire) { opts.wire(body, wrap); } }
		if (opts.actionsWire) { opts.actionsWire(wrap.querySelector(".nlrm-pacts")); }
		requestAnimationFrame(function () { wrap.classList.add("is-in"); if (!wrap.contains(document.activeElement)) { wrap.querySelector(".nlrm-panel").focus({ preventScroll: true }); } });
		return L;
	}
	function drop(L, instant) {
		if (!L) { return; }
		L.el.classList.remove("is-in");
		if (instant) { L.el.remove(); } else { setTimeout(function () { L.el.remove(); }, 220); }
	}
	N.ui.open = function (opts) {
		if (!opts) { return null; }
		if (!layer) { lastFocus = document.activeElement; stack = []; }
		else {
			if (opts.kind === "sheet" && layer.opts.kind !== "sheet") { stack.push({ opts: layer.opts, tab: layer.tab }); }
			drop(layer, true);
		}
		layer = build(opts);
		try { history.pushState({ nlrmLayer: 1 }, "", location.href); } catch (e) { /* sandboxed preview */ }
		return layer;
	};
	/* re-render the open layer with fresh data, on the same tab (after a save) */
	N.ui.refresh = function () {
		if (!layer || !layer.opts.refresh || layer.opts.kind === "sheet") { return; }
		var o = layer.opts.refresh();
		if (!o) { return; }
		var tab = layer.tab, top = layer.el.querySelector(".nlrm-pbody").scrollTop;
		o.tab = Math.max(0, (o.tabs || []).findIndex(function (x) { return x.id === tab; }));
		drop(layer, true);
		layer = build(o);
		layer.el.classList.add("is-in");
		layer.el.querySelector(".nlrm-pbody").scrollTop = top;
	};
	N.ui.close = function (silent) {
		if (!layer) { return; }
		var L = layer;
		layer = null;
		if (stack.length) {
			drop(L, true);
			var prev = stack.pop(), o = prev.opts.refresh ? (prev.opts.refresh() || prev.opts) : prev.opts;
			o.tab = Math.max(0, (o.tabs || []).findIndex(function (x) { return x.id === prev.tab; }));
			layer = build(o);
			layer.el.classList.add("is-in");
		} else {
			drop(L, false);
			document.documentElement.classList.remove("nlrm-locked");
			if (N.onLayersClosed) { try { N.onLayersClosed(); } catch (e) { /* the page moved on */ } }
			if (lastFocus && lastFocus.focus && document.body.contains(lastFocus)) { try { lastFocus.focus(); } catch (e) { /* gone */ } }
		}
		if (!silent) { try { if (history.state && history.state.nlrmLayer) { selfBack++; history.back(); } } catch (e) { /* sandboxed */ } }
	};
	document.addEventListener("keydown", function (e) { if (e.key === "Escape" && layer) { e.preventDefault(); N.ui.close(); } });
	window.addEventListener("popstate", function () {
		if (selfBack > 0) { selfBack--; return; }
		if (layer) { N.ui.close(true); }
	});
	N.ui.isOpen = function () { return !!layer; };

	/* form helpers: fields as data, values back as an object */
	N.ui.field = function (f) {
		var id = "nlf-" + f.name, v = f.value == null ? "" : f.value, req = f.required ? " required" : "";
		var lab = '<label class="nlrm-f" for="' + id + '"><span>' + esc(f.label) + (f.hint ? ' <em>' + esc(f.hint) + "</em>" : "") + "</span>";
		if (f.type === "select") {
			return lab + '<select id="' + id + '" name="' + f.name + '"' + req + ">" + f.options.map(function (o) { return '<option value="' + esc(o[0]) + '"' + (String(o[0]) === String(v) ? " selected" : "") + ">" + esc(o[1]) + "</option>"; }).join("") + "</select></label>";
		}
		if (f.type === "textarea") { return lab + '<textarea id="' + id + '" name="' + f.name + '" rows="' + (f.rows || 3) + '"' + req + ">" + esc(v) + "</textarea></label>"; }
		if (f.type === "check") { return '<label class="nlrm-check"><input type="checkbox" name="' + f.name + '"' + (v ? " checked" : "") + "> <span>" + esc(f.label) + (f.hint ? '<small class="nlrm-check-hint">' + esc(f.hint) + "</small>" : "") + "</span></label>"; }
		var dirAttr = (f.type === "tel" || f.type === "email" || f.type === "number" || f.ltr) ? ' dir="ltr"' : "";
		return lab + '<input id="' + id + '" name="' + f.name + '" type="' + (f.type || "text") + '" value="' + esc(v) + '"' + (f.min != null ? ' min="' + f.min + '"' : "") + (f.max != null ? ' max="' + f.max + '"' : "") + (f.step ? ' step="' + f.step + '"' : "") + (f.placeholder ? ' placeholder="' + esc(f.placeholder) + '"' : "") + (f.inputmode ? ' inputmode="' + f.inputmode + '"' : "") + (f.autocomplete ? ' autocomplete="' + f.autocomplete + '"' : "") + dirAttr + req + "></label>";
	};
	N.ui.values = function (form) {
		var o = {};
		form.querySelectorAll("[name]").forEach(function (el) {
			if (el.type === "checkbox") { o[el.name] = el.checked; }
			else if (el.type === "number") { o[el.name] = el.value === "" ? "" : Number(el.value); }
			else { o[el.name] = el.value.trim(); }
		});
		return o;
	};
	/* a sheet with a form: fields, a primary button, onSubmit(values) -> Promise */
	N.ui.form = function (opts) {
		var body = '<form class="nlrm-form" novalidate>' + (opts.intro ? '<p class="nlrm-lead">' + opts.intro + "</p>" : "") +
			'<div class="nlrm-fgrid">' + opts.fields.map(function (f) { return f.html != null ? f.html : N.ui.field(f); }).join("") + "</div>" +
			(opts.note ? '<p class="nlrm-note">' + opts.note + "</p>" : "") +
			'<p class="nlrm-ferr" role="alert" hidden></p><div class="nlrm-fbtns"><button type="submit" class="nlrm-btn nlrm-btn--primary">' + esc(opts.submit || N.t("save")) + '</button><button type="button" class="nlrm-btn nlrm-btn--quiet" data-close>' + esc(N.t("cancel")) + "</button></div></form>";
		return N.ui.open({ kind: "sheet", title: opts.title, sub: opts.sub, body: body, wire: function (b) {
			var form = b.querySelector("form"), err = b.querySelector(".nlrm-ferr"), btn = b.querySelector('[type="submit"]');
			if (opts.wire) { opts.wire(form); }
			var first = form.querySelector("input,select,textarea"); if (first) { setTimeout(function () { first.focus(); }, 60); }
			form.addEventListener("submit", function (e) {
				e.preventDefault();
				var v = N.ui.values(form), bad = null;
				(opts.fields || []).forEach(function (f) { if (f.required && !bad && (v[f.name] === "" || v[f.name] == null)) { bad = f; } });
				if (bad) { err.hidden = false; err.textContent = N.t("err_required", { field: bad.label }); var el = form.querySelector('[name="' + bad.name + '"]'); if (el) { el.focus(); el.setAttribute("aria-invalid", "true"); } return; }
				btn.disabled = true; btn.textContent = N.t("saving");
				Promise.resolve(opts.onSubmit(v, form)).then(function (res) {
					if (res !== false) { N.ui.close(); if (opts.done) { opts.done(res); } }
					else { btn.disabled = false; btn.textContent = opts.submit || N.t("save"); }
				}).catch(function (ex) { err.hidden = false; err.textContent = (ex && ex.message) || N.t("err_generic"); btn.disabled = false; btn.textContent = opts.submit || N.t("save"); });
			});
		} });
	};
	N.ui.confirm = function (text, yes) {
		return new Promise(function (resolve) {
			N.ui.open({ kind: "sheet", title: N.t("confirm_title"), body: '<p class="nlrm-lead">' + esc(text) + '</p><div class="nlrm-fbtns"><button type="button" class="nlrm-btn nlrm-btn--primary" data-yes>' + esc(yes || N.t("confirm_yes")) + '</button><button type="button" class="nlrm-btn nlrm-btn--quiet" data-close>' + esc(N.t("cancel")) + "</button></div>", wire: function (b) {
				b.querySelector("[data-yes]").addEventListener("click", function () { N.ui.close(); resolve(true); });
			} });
		});
	};
	N.copy = function (text) {
		if (navigator.clipboard && navigator.clipboard.writeText) { return navigator.clipboard.writeText(text).then(function () { N.ui.toast(N.t("copied")); }); }
		var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select();
		try { document.execCommand("copy"); N.ui.toast(N.t("copied")); } catch (e) { /* ignore */ }
		ta.remove();
		return Promise.resolve();
	};

	/* icons: line icons in currentColor (DS iconography: stroke 1.65 on 24, round caps) */
	var P = {
		today: '<path d="M4 7h16M4 7v12h16V7M4 7l2-3h12l2 3M9 12h6"/>',
		building: '<path d="M5 21V4h9v17M14 9h5v12M8 8h2M8 12h2M8 16h2M3 21h18"/>',
		people: '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 11a3 3 0 1 0 0-6M17 14c2.4.5 4 2.8 4 6"/>',
		money: '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9v.01M18 15v.01"/>',
		wrench: '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
		doc: '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6"/>',
		key: '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l2 2M15 8l2 2"/>',
		chart: '<path d="M4 20V4M4 20h16M8 16v-4M12 16V8M16 16v-6"/>',
		gear: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
		plus: '<path d="M12 5v14M5 12h14"/>',
		wa: '<path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9 9.5c.3 1.8 1.7 3.6 3.5 4.5l1.3-1.1 1.9.9-.4 1.6c-3 .2-6.6-3.2-6.8-6.3l1.5-.6.9 1.9z"/>',
		phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
		mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
		link: '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
		check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
		alert: '<path d="M12 3l9.5 17h-19zM12 10v4M12 17v.01"/>',
		cal: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
		search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
		upload: '<path d="M12 16V4M7 9l5-5 5 5M4 20h16"/>',
		sign: '<path d="M3 17c3-1 4-5 6-5s1 4 3 4 3-3 4-3 2 2 5 2M3 21h18"/>',
		cube: '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12v9M12 12L4 7.5"/>',
		eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
		trash: '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
		menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
		globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
		arrow: '<path d="M15 6l-6 6 6 6"/>',
		spark: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
		cheque: '<rect x="3" y="6" width="18" height="12" rx="1.5"/><path d="M6 10h7M6 14h4M15 14h3"/>',
		help: '<circle cx="12" cy="12" r="9"/><path d="M9.6 9.3a2.5 2.5 0 1 1 3.6 2.3c-.8.4-1.2 1-1.2 1.9v.4M12 17v.01"/>'
	};
	N.icon = function (name, size) {
		return '<svg class="nlrm-ico" viewBox="0 0 24 24" width="' + (size || 20) + '" height="' + (size || 20) + '" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (P[name] || "") + "</svg>";
	};
})();
