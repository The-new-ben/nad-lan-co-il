/* ============================================================================
   NADLAN RENTALS v2 - slice 1 (HAD-795): the landing screen "Today" of one apartment,
   the camera-first repair, the index update that saves, and the tenancy axis in its
   simplest form (the folding ruler of twelve months and the next-due sheet).
   It sits over the existing app as a phone-first layer and answers only the routes
   #/today and #/rent; every other tab goes to the existing v2 routes. The old today
   view stays reachable at #/today-classic (or ?today=classic, or localStorage nlrm_today2=off).
   Every visible word comes from the string table (t2_*, he + en). Nothing is sent to a
   tenant. Money moves only through the existing routes (/rm/pay, /rm/ledger-act) and
   the two routes of inc/rentals/today.php.
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM;
	if (!N) { return; }
	var esc = N.esc, T2 = N.today2 = {};
	var S = { unitId: null, sheet: null, sel: null, busy: false, idx: null };
	var host = null, body = null, sheetEl = null, cfg = {}, inputs = {}, started = false;
	var SYS_CATS = ["boiler", "ac", "electric", "plumbing"];
	var SYSTEMS = ["boiler", "ac", "panel", "water_meter", "gas", "shutter"];
	/* the parts offered first to a home that has none recorded (one press adds one) */
	var FIRST_KINDS = ["boiler", "ac", "panel", "fridge", "oven", "washer"];
	var KIND_CAT = { boiler: "boiler", ac: "ac", panel: "electric", water_meter: "plumbing", oven: "appliance", fridge: "appliance", washer: "appliance", dishwasher: "appliance", heater: "appliance" };

	function t(k, v) { return N.t(k, v); }
	/* a string with ready-made HTML values (every value is escaped by the caller) */
	function T(k, v) { return t(k, v); }
	function uid() { return "c" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
	function mono(s) { return '<span dir="ltr" class="nt2-mono">' + s + "</span>"; }
	function dhe(iso) { var d = N.parse(iso); return d.getDate() + "." + (d.getMonth() + 1) + "." + d.getFullYear(); }
	function D(iso) { return N.rtl ? mono(dhe(iso)) : esc(N.dateText(iso)); }
	function dshort(iso) { var d = N.parse(iso), s = d.getDate() + "." + (d.getMonth() + 1); return d.getFullYear() !== N.today().getFullYear() ? s + "." + String(d.getFullYear()).slice(2) : s; }
	function M(shekels) { var n = Math.round(Number(shekels || 0)), s = N.num(Math.abs(n)), neg = n < 0 ? "-" : ""; return N.rtl ? mono(neg + s + "&nbsp;₪") : '<span class="nt2-mono">' + neg + "₪" + s + "</span>"; }
	function mname(ym) { return new Date(+ym.slice(0, 4), +ym.slice(5, 7) - 1, 1).toLocaleDateString(N.locale(), { month: "long" }); }
	function mnum(ym) { return +ym.slice(5, 7); }
	function and2(a, b) { return t("t2_and", { a: a, b: b }); }
	function ico(name) {
		var P = {
			cam: '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
			doc: '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/>',
			today: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
			home: '<path d="M4 11.5 12 4l8 7.5V20H4z"/><path d="M10 20v-5h4v5"/>',
			rent: '<path d="M3 9h18v6H3z"/><path d="M7 9v3M11 9v2M15 9v3M19 9v2"/>',
			money: '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/>',
			docs: '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
			up: '<path d="M4 11l5-5 5 5"/>', down: '<path d="M4 7l5 5 5-5"/>', swap: '<path d="M7 4 3 8l4 4M3 8h14M17 20l4-4-4-4M21 16H7"/>', x: '<path d="M4 4l10 10M14 4 4 14"/>'
		};
		var sw = name === "rent" ? 1.9 : 1.7, sz = name === "cam" || name === "doc" ? 20 : (name === "up" || name === "down" || name === "x" ? 18 : 22), vb = (name === "up" || name === "down" || name === "x") ? "0 0 18 18" : "0 0 24 24";
		return '<svg aria-hidden="true" width="' + sz + '" height="' + sz + '" viewBox="' + vb + '" fill="none" stroke="currentColor" stroke-width="' + (name === "cam" || name === "doc" ? 1.9 : sw) + '" stroke-linecap="round" stroke-linejoin="round">' + P[name] + "</svg>";
	}

	/* ---------- the data of one apartment ---------- */
	function units() { return N.store.d.units || []; }
	function pickUnit() {
		var h = (location.hash || "").replace(/^#\/?/, "").split("/"), want = +h[1] || S.unitId, us = units(), u = us.find(function (x) { return +x.id === +want; });
		if (!u) { u = us.find(function (x) { return N.ix.leaseByUnit[x.id]; }) || us[0] || null; }
		S.unitId = u ? u.id : null;
		return u;
	}
	function rentRows(l) { return (N.ix.ledgerByLease[l.id] || []).filter(function (r) { return r.kind === "charge" && r.category === "rent" && r.status !== "void"; }); }
	function autoOf(r) { return String(r.auto || r.auto_key || ""); }
	function rowFor(l, p) { return rentRows(l).find(function (r) { return autoOf(r) === p.key; }) || null; }
	/* the periods near today with their state: paid / partial / open / none (no charge yet) */
	function periods(l, horizon) {
		var bal = N.moneyOf(l).balance, adv = Math.max(0, -bal), base = null;
		var last = rentRows(l).filter(function (r) { return r.amount > 0 && /^rent:/.test(autoOf(r)); }).sort(function (a, b) { return (a.due_date || "") < (b.due_date || "") ? -1 : 1; }).pop();
		return N.mx.periods(l, horizon).map(function (p) {
			var row = rowFor(l, p), amount = row ? row.amount : (last ? last.amount : Math.round((+l.rent || 0) * 100)), st, covered = row ? (row.covered || 0) : 0;
			if (row) { st = row.status === "paid" ? "paid" : (row.status === "partial" ? "partial" : "open"); if (st === "paid") { covered = amount; } }
			else if (p.due <= N.todayIso()) { st = bal <= 0 ? "paid" : "none"; covered = amount; }
			else if (adv >= amount) { st = "paid"; adv -= amount; covered = amount; }
			else { st = "none"; }
			return { key: p.key, ym: p.start.slice(0, 7), start: p.start, due: p.due, k: p.k, amount: amount, state: st, covered: covered, remaining: Math.max(0, amount - covered), row: row };
		});
	}
	function nextDue(l) {
		var h = N.addDays(N.todayIso(), 62), ps = periods(l, h);
		return ps.find(function (p) { return p.state !== "paid" && (p.row || p.due >= N.todayIso()); }) || null;
	}
	/* the landlord's confirmations of an index update: events of the apartment's journal (never ledger lines) */
	function confirms(l) { return (N.store.d.events || []).filter(function (e) { return e.type === "index_confirmed" && e.scope === "lease" && +e.scope_id === +l.id; }); }
	/* the latest confirmation of the last week, for the sentence on the card */
	function confirmedNote(l) {
		var T0 = N.todayIso(), e = confirms(l).filter(function (x) { return String(x.at).slice(0, 10) >= N.addDays(T0, -7); }).sort(function (a, b) { return a.at < b.at ? 1 : -1; })[0];
		return e && e.meta ? '<p class="nt2-ok" role="status">' + esc(t("t2_idx_done", { month: N.monthName(e.meta.start_month), amount: N.moneyText(Math.round(e.meta.new_amount / 100)) })) + "</p>" : "";
	}
	/* the next index adjustment of a linked lease that the landlord has not confirmed yet */
	function nextIndex(l) {
		var k = l && l.linkage;
		if (!k || k.mode !== "cpi" || !l.start_date) { return null; }
		var every = Math.max(1, +k.every || 12), conf = {};
		confirms(l).forEach(function (e) { if ((e.meta || {}).start_month) { conf[e.meta.start_month] = 1; } });
		for (var n = 1; n < 80; n++) {
			var d = N.addMonths(l.start_date, every * n);
			if (l.end_date && d > l.end_date) { return null; }
			if (d < N.addDays(N.todayIso(), -14)) { continue; }
			if (conf[d.slice(0, 7)]) { continue; }
			return { date: d, ym: d.slice(0, 7), n: n };
		}
		return null;
	}
	/* for the tenancy screen: the latest update date already reached that the landlord has not confirmed (however long ago),
	   and only when there is none, the next one ahead */
	function indexDue(l) {
		var k = l && l.linkage;
		if (!k || k.mode !== "cpi" || !l.start_date) { return null; }
		var every = Math.max(1, +k.every || 12), conf = {}, T0 = N.todayIso(), past = null;
		confirms(l).forEach(function (e) { if ((e.meta || {}).start_month) { conf[e.meta.start_month] = 1; } });
		for (var n = 1; n < 80; n++) {
			var d = N.addMonths(l.start_date, every * n);
			if ((l.end_date && d > l.end_date) || d > T0) { break; }
			past = conf[d.slice(0, 7)] ? null : { date: d, ym: d.slice(0, 7), n: n, past: true };
		}
		return past || nextIndex(l);
	}
	function openTickets(u) {
		return (N.ix.ticketsByUnit[u.id] || []).filter(function (x) { return x.status !== "done" && x.status !== "cancelled"; }).sort(function (a, b) {
			if ((a.urgency === "urgent") !== (b.urgency === "urgent")) { return a.urgency === "urgent" ? -1 : 1; }
			return (a.due_by || "9999") < (b.due_by || "9999") ? -1 : 1;
		});
	}
	function assetsOf(u) { return ((u.meta || {}).assets || []); }
	function partLabel(a) { return a.label || t("ak_" + a.kind); }
	function ticketPart(u, tk) {
		var as = assetsOf(u), id = (tk.meta || {}).asset, a = id && as.find(function (x) { return x.id === id; });
		if (!a) { a = as.find(function (x) { return KIND_CAT[x.kind] === tk.category; }); }
		return a || null;
	}
	function parts(u) {
		var tks = openTickets(u), T0 = N.todayIso();
		return assetsOf(u).filter(function (a) { return a.kind; }).map(function (a) {
			var state = "ok";
			if (tks.some(function (x) { var p = ticketPart(u, x); return p && p.id === a.id; })) { state = "fault"; }
			else if (a.warranty_until && a.warranty_until >= T0 && a.warranty_until <= N.addDays(T0, 30)) { state = "soon"; }
			return { id: a.id, kind: a.kind, label: partLabel(a), room: a.room, layers: (N.plan2d.KIND_LAYERS[a.kind] || []), state: state, x: a.at && isFinite(a.at[0]) ? +a.at[0] : null, y: a.at && isFinite(a.at[1]) ? +a.at[1] : null, asset: a };
		});
	}
	/* the plan of the unit, as rectangles in the 342 box (a plan the designer made: polygons of rooms); none = null */
	function planOf(u) {
		var p = (u.meta || {}).plan;
		if (!p || !Array.isArray(p.rooms) || !p.rooms.length) { return null; }
		var bb = [1e9, 1e9, -1e9, -1e9], rs = [];
		p.rooms.forEach(function (r) {
			if (!Array.isArray(r.poly) || r.poly.length < 3) { return; }
			var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
			r.poly.forEach(function (q) { x0 = Math.min(x0, +q[0]); y0 = Math.min(y0, +q[1]); x1 = Math.max(x1, +q[0]); y1 = Math.max(y1, +q[1]); });
			rs.push({ r: r, x0: x0, y0: y0, x1: x1, y1: y1 });
			bb = [Math.min(bb[0], x0), Math.min(bb[1], y0), Math.max(bb[2], x1), Math.max(bb[3], y1)];
		});
		if (!rs.length) { return null; }
		var W = bb[2] - bb[0] || 1, H = bb[3] - bb[1] || 1, k = Math.min(338 / W, 338 / H), ox = (342 - W * k) / 2, oy = (342 - H * k) / 2;
		var tr = function (x, y) { return [ox + (x - bb[0]) * k, oy + (y - bb[1]) * k]; };
		return {
			rooms: rs.map(function (e) { var a = tr(e.x0, e.y0), b = tr(e.x1, e.y1), kind = e.r.kind || ""; return { id: e.r.id, kind: kind, x: Math.round(a[0]), y: Math.round(a[1]), w: Math.round(b[0] - a[0]), h: Math.round(b[1] - a[1]), label: e.r.label || (kind && N.T["t2_room_" + kind] ? t("t2_room_" + kind) : "") }; }),
			tr: tr
		};
	}
	function planData(u, ps) {
		var pl = planOf(u);
		if (!pl) { return { rooms: [], parts: ps, addKinds: FIRST_KINDS, addPlanUrl: ((cfg.urls || {}).designer) || "/tour/designer/" }; }
		ps = ps.map(function (p) { if (p.x != null && p.y != null) { var q = pl.tr(p.x, p.y); return Object.assign({}, p, { x: Math.round(q[0]), y: Math.round(q[1]) }); } return p; });
		return { rooms: pl.rooms, parts: ps };
	}

	/* the year's received rent and the months paid on time in a row (shown only when true) */
	function earned(u, l) {
		var yr = String(N.today().getFullYear()), rows = (N.store.d.ledger || []).filter(function (r) { return +r.unit_id === +u.id; }), sum = 0;
		rows.forEach(function (r) { if (r.kind === "payment" && r.category === "rent" && (r.paid_date || "").slice(0, 4) === yr && (r.status === "paid" || r.status === "deposited")) { sum += N.mx.incomeOf(r); } });
		var streak = 0;
		if (l) {
			var T0 = N.todayIso(), ch = rentRows(l).filter(function (r) { return r.amount > 0 && (r.due_date || "9999") <= T0; }).sort(function (a, b) { return a.due_date < b.due_date ? -1 : (a.due_date > b.due_date ? 1 : a.id - b.id); });
			var pay = (N.ix.ledgerByLease[l.id] || []).filter(function (r) { return r.kind === "payment" && r.category === "rent" && (r.status === "paid" || r.status === "deposited") && r.paid_date; }).sort(function (a, b) { return a.paid_date < b.paid_date ? -1 : 1; });
			var cum = 0, i = 0, tot = 0, ok = [];
			ch.forEach(function (c) {
				cum += c.amount;
				while (tot < cum && i < pay.length) { tot += pay[i].amount; i++; }
				ok.push(tot >= cum && pay[i - 1] && pay[i - 1].paid_date <= c.due_date);
			});
			for (var j = ok.length - 1; j >= 0 && ok[j]; j--) { streak++; }
		}
		return { year: Math.round(sum / 100), streak: streak };
	}
	function recentItems(u, l) {
		var out = [], d = N.store.d, ten = {};
		(N.ix.ledgerByLease[l ? l.id : 0] || []).forEach(function (r) {
			if (r.kind === "payment" && r.category === "rent" && (r.status === "paid" || r.status === "deposited") && r.paid_date && r.method !== "deposit") {
				var ch = r.applies_to ? (N.ix.ledgerByLease[l.id] || []).find(function (x) { return +x.id === +r.applies_to; }) : null;
				out.push({ d: r.paid_date, t: t("t2_recent_rent", { month: mname((ch && ch.due_date ? ch.due_date : r.paid_date).slice(0, 7)) }) });
			}
		});
		if (l) { confirms(l).forEach(function (e) { out.push({ d: String(e.at).slice(0, 10), t: t("t2_recent_idx") }); }); }
		(N.ix.ticketsByUnit[u.id] || []).forEach(function (x) {
			var nm = esc(x.title);
			if (x.closed_at && x.status === "done") { out.push({ d: String(x.closed_at).slice(0, 10), t: t("t2_recent_closed", { name: nm }) }); }
			if (x.opened_at) { out.push({ d: String(x.opened_at).slice(0, 10), t: (x.meta || {}).via === "today-camera" ? nm : t("t2_recent_opened", { name: nm }) }); }
		});
		(d.docs || []).forEach(function (x) {
			var mine = (x.scope === "unit" && +x.scope_id === +u.id) || (x.scope === "lease" && l && +x.scope_id === +l.id) || (x.scope === "property" && +x.scope_id === +u.property_id);
			if (mine && x.created_at) { out.push({ d: String(x.created_at).slice(0, 10), t: t("t2_recent_doc", { kind: esc(t("dk_" + x.kind)) }) }); }
		});
		out.sort(function (a, b) { return a.d < b.d ? 1 : (a.d > b.d ? -1 : 0); });
		var seen = {};
		return out.filter(function (x) { var k = x.d + x.t; if (seen[k]) { return false; } seen[k] = 1; return true; }).slice(0, 5);
	}
	function taskItems(u, l) {
		var T0 = N.todayIso(), lim = N.addDays(T0, 7), tk = (N.ix.ticketsByUnit[u.id] || []).map(function (x) { return +x.id; });
		return (N.store.d.tasks || []).filter(function (x) {
			if (x.done || !x.due || x.due > lim) { return false; }
			if (!x.scope) { return true; }
			return (x.scope === "unit" && +x.scope_id === +u.id) || (x.scope === "lease" && l && +x.scope_id === +l.id) || (x.scope === "ticket" && tk.indexOf(+x.scope_id) >= 0) || (x.scope === "property" && +x.scope_id === +u.property_id);
		}).sort(function (a, b) { return a.due < b.due ? -1 : 1; });
	}

	/* the whole model of the screen: one of three states, computed from the real data */
	function model(u) {
		var l = N.ix.leaseByUnit[u.id] || null, T0 = N.todayIso(), tks = openTickets(u), ps = parts(u), m = { u: u, l: l, parts: ps, tickets: tks, date: T0 };
		m.recent = recentItems(u, l);
		var soon = [];
		if (l) {
			var nd = nextDue(l);
			if (nd && nd.due <= N.addDays(T0, 7)) { soon.push({ kind: "rent", date: nd.due, p: nd }); }
			var ni = nextIndex(l);
			if (ni && ni.date <= N.addDays(T0, 7)) { soon.push({ kind: "idx", date: ni.date, ni: ni }); }
		}
		taskItems(u, l).forEach(function (x) { soon.push({ kind: "task", date: x.due, task: x }); });
		soon.sort(function (a, b) { return (a.kind === "rent" ? 0 : 1) - (b.kind === "rent" ? 0 : 1) || (a.date < b.date ? -1 : 1); });
		m.soon = soon;
		m.state = tks.length ? "urgent" : (soon.length ? "soon" : "quiet");
		m.layer = "all"; m.lit = null;
		var nowN = N.today().getMonth();
		if (m.state === "urgent") {
			var tk = tks[0], pt = ticketPart(u, tk);
			m.tk = tk; m.part = pt;
			if (pt) { m.lit = pt.id; m.layer = (N.plan2d.KIND_LAYERS[pt.kind] || ["all"])[0]; }
		}
		m.earned = earned(u, l);
		void nowN;
		return m;
	}

	/* ---------- the pieces of the screen ---------- */
	function saying(m) {
		var say, sub, color = "";
		if (m.state === "urgent") {
			var tk = m.tk, nm = esc(m.part ? partLabel(m.part) : tk.title);
			say = m.tickets.length > 1 ? t("t2_say_urgent_many", { n: N.num(m.tickets.length), name: nm }) : t("t2_say_urgent_one", { name: nm });
			sub = tk.due_by ? t("t2_sub_urgent", { date: D(tk.due_by) }) : t("t2_sub_urgent_nodate");
			color = " is-fault";
		} else if (m.state === "soon") {
			var f = m.soon[0], names = m.soon.slice(0, 2).map(function (s) { return soonName(m, s); }), days = N.daysTo(f.date);
			var late = f.kind === "rent" && days < 0;
			say = late ? t("t2_say_late", { month: esc(mname(f.p.ym)) }) : t("t2_say_none");
			sub = t("t2_sub_soon", { when: esc(N.when(days)), what: names.length > 1 ? and2(names[0], names[1]) : names[0] });
		} else {
			say = m.l ? t("t2_say_quiet") : t("t2_say_vacant");
			sub = t("t2_sub_next", { what: nextThing(m) });
		}
		return { say: say, sub: sub, color: color };
	}
	function soonName(m, s) {
		if (s.kind === "rent") { return esc(t("t2_rent_for", { month: mname(s.p.ym) })); }
		if (s.kind === "idx") { return esc(t("t2_idx_row")); }
		return esc(s.task.title);
	}
	function nextThing(m) {
		var l = m.l, c = [];
		if (!l) { return esc(t("t2_next_none")); }
		var nd = nextDue(l), ni = nextIndex(l);
		if (nd) { c.push({ d: nd.due, s: t("t2_next_rent", { date: D(nd.due) }) }); }
		if (ni) { c.push({ d: ni.date, s: t("t2_next_index", { date: D(ni.date) }) }); }
		if (l.option_until && l.option_until >= m.date) { c.push({ d: l.option_until, s: t("t2_next_option", { date: D(l.option_until) }) }); }
		if (l.end_date && l.end_date >= m.date) { c.push({ d: l.end_date, s: t("t2_next_end", { date: D(l.end_date) }) }); }
		c.sort(function (a, b) { return a.d < b.d ? -1 : 1; });
		return c.length ? c[0].s : esc(t("t2_next_none"));
	}
	function rulerHtml(m) {
		var l = m.l;
		if (!l || !l.start_date) { return ""; }
		var T0 = N.todayIso(), sinceM = Math.max(0, Math.round((N.parse(T0) - N.parse(l.start_date)) / (30.44 * 86400000))), w0 = Math.floor(sinceM / 12) * 12;
		var months = [], ps = periods(l, N.addMonths(l.start_date, w0 + 12));
		for (var i = 0; i < 12; i++) { months.push(N.addMonths(l.start_date, w0 + i).slice(0, 7)); }
		var paid = 0, going = true;
		months.forEach(function (ym) { var p = ps.find(function (x) { return x.ym === ym; }); if (going && p && p.state === "paid") { paid++; } else { going = false; } });
		var cur = months.indexOf(T0.slice(0, 7)), dim = new Date(N.today().getFullYear(), N.today().getMonth() + 1, 0).getDate();
		var needle = cur < 0 ? (T0 < months[0] ? 0 : 12) : cur + (N.today().getDate() - 1) / dim;
		var ni = nextIndex(l), ix = ni ? months.indexOf(ni.ym) : -1;
		var h = '<div class="nt2-ruler" role="img" aria-label="' + esc(t("t2_ruler_aria")) + '"><div class="nt2-rl" dir="ltr" aria-hidden="true"><div class="nt2-rl-box"></div><div class="nt2-rl-paid" style="width:' + (paid / 12 * 100) + '%"></div>';
		if (ix >= 0) { h += '<div class="nt2-rl-idx" style="left:' + (ix / 12 * 100) + '%"></div>'; }
		h += '<div class="nt2-rl-needle" style="left:calc(' + (needle / 12 * 100) + '% - 1.5px)"></div><div class="nt2-rl-n">' + months.map(function (ym) { return "<span>" + mnum(ym) + "</span>"; }).join("") + "</div></div>";
		h += '<div class="nt2-rl-cap">' + esc(t(ix >= 0 ? "t2_ruler_cap_idx" : "t2_ruler_cap", { from: mname(months[0]), to: mname(months[11]) })) + "</div></div>";
		return h;
	}
	function planBlock(m) {
		return '<div class="nt2-tb-draw" id="nt2-plan"></div>';
	}
	function cardHtml(m) {
		var h = "", ok = m.l ? confirmedNote(m.l) : "";
		if (m.state === "urgent") {
			var tk = m.tk, opened = (tk.opened_at || N.todayIso()).slice(0, 10), total = tk.due_by ? Math.max(1, N.mx.dayDiff(opened, tk.due_by)) : 30, day = Math.max(0, N.mx.dayDiff(opened, N.todayIso())) + 1;
			var pct = Math.max(2, Math.min(100, Math.round(100 * (day - 1) / total))), detail = tk.body ? esc(String(tk.body).replace(/\s+/g, " ").split(/[.!?]/)[0].slice(0, 26)) + " · " : "";
			var isSys = m.part ? SYSTEMS.indexOf(m.part.kind) >= 0 : SYS_CATS.indexOf(tk.category) >= 0, isApp = m.part ? !isSys : tk.category === "appliance";
			h += '<section class="nt2-card is-fault" aria-label="' + esc(t("t2_open_fault")) + '">' + ok + '<div class="nt2-card-h"><span class="nt2-bang" aria-hidden="true">!</span><h2>' + esc(m.part ? partLabel(m.part) : tk.title) + '</h2><span class="nt2-pill">' + esc(t("t2_open_fault")) + "</span></div>";
			h += '<div class="nt2-card-l">' + detail + t("t2_fault_day", { d: mono(N.num(day)), n: mono(N.num(total)) }) + (tk.due_by ? " · " + t("t2_fault_until", { date: D(tk.due_by) }) : "") + "</div>";
			h += '<div class="nt2-bar" aria-hidden="true"><i style="width:' + pct + '%"></i></div>';
			h += legalHtml(isSys, isApp);
			h += '<div class="nt2-btns"><button type="button" class="nt2-btn nt2-btn--go" data-act="ticket" data-id="' + tk.id + '">' + esc(t("t2_send_pro")) + '</button><button type="button" class="nt2-btn nt2-btn--line" data-act="ticket" data-id="' + tk.id + '">' + esc(t("t2_fixed_invoice")) + "</button></div></section>";
		} else if (m.state === "soon") {
			h += '<section class="nt2-card">' + ok + '<h2 class="nt2-card-k">' + esc(t("t2_soon_h")) + "</h2>";
			m.soon.slice(0, 2).forEach(function (s, i) {
				var days = N.daysTo(s.date), title, sub, btn;
				if (s.kind === "rent") {
					title = t("t2_rent_for", { month: esc(mname(s.p.ym)) });
					sub = M(s.p.remaining / 100) + " · " + esc(days < 0 ? t("t2_was_due", { when: N.when(days) }) : N.when(days));
					btn = '<button type="button" class="nt2-btn nt2-btn--go nt2-btn--sm" data-act="rent" data-ym="' + s.p.ym + '">' + esc(t("t2_received")) + "</button>";
				} else if (s.kind === "idx") {
					title = esc(t("t2_idx_row")); sub = esc(t("t2_idx_sub"));
					btn = '<button type="button" class="nt2-btn nt2-btn--line nt2-btn--sm" data-act="index">' + esc(t("t2_calc_index")) + "</button>";
				} else {
					title = esc(s.task.title); sub = esc(t("t2_reminder_sub"));
					btn = '<button type="button" class="nt2-btn nt2-btn--line nt2-btn--sm" data-act="task" data-id="' + s.task.id + '">' + esc(t("t2_done")) + "</button>";
				}
				h += '<div class="nt2-soon' + (i === 0 && m.soon.length > 1 ? " has-line" : "") + '"><span class="nt2-mono nt2-soon-d">' + esc(dshort(s.date)) + '</span><span class="nt2-soon-t"><b>' + title + "</b><small>" + sub + "</small></span>" + btn + "</div>";
			});
			h += "</section>";
		} else {
			var e = m.earned, fact = "";
			if (e.year > 0) { fact = '<div class="nt2-earn"><span class="nt2-big">' + M(e.year) + "</span><span>" + t("t2_earned_year", { year: mono(String(N.today().getFullYear())) }) + (e.streak >= 2 ? " " + t("t2_earned_streak", { n: mono(N.num(e.streak)) }) : "") + "</span></div>"; }
			h += '<section class="nt2-card">' + ok + fact + '<h2 class="nt2-card-k">' + esc(t("t2_state")) + "</h2>";
			var l = m.l, rentTxt = "";
			if (l) {
				var ps = periods(l, N.addMonths(N.todayIso(), 1)).filter(function (p) { return p.state === "paid"; }), lastPaid = ps.length ? ps[ps.length - 1] : null;
				rentTxt = lastPaid ? t("t2_paid_until", { month: esc(mname(lastPaid.ym)) }) : esc(t("t2_rent_none"));
			} else { rentTxt = esc(t("t2_no_lease")); }
			var kinds = {}; (N.store.d.docs || []).forEach(function (x) { if ((x.scope === "unit" && +x.scope_id === +m.u.id) || (x.scope === "lease" && l && +x.scope_id === +l.id)) { kinds[x.kind] = 1; } });
			var kl = Object.keys(kinds).filter(function (k) { return k !== "photo"; }).slice(0, 3).map(function (k) { return esc(t("dk_" + k)); });
			h += '<div class="nt2-row"><b>' + esc(t("t2_rent")) + "</b><span>" + rentTxt + '</span></div><div class="nt2-row"><b>' + esc(t("t2_faults")) + "</b><span>" + esc(t("t2_none_open")) + '</span></div><div class="nt2-row"><b>' + esc(t("t2_file")) + "</b><span>" + (kl.length ? kl.join(", ") : esc(t("t2_file_none"))) + "</span></div>";
			var miss = assetsOf(m.u).filter(function (a) { return !a.model && !a.plate; });
			if (miss.length) { h += '<div class="nt2-spare"><span>' + esc(t(miss.length === 1 ? "t2_spare_one" : "t2_spare_many", { n: N.num(miss.length) })) + '</span><button type="button" class="nt2-btn nt2-btn--line nt2-btn--sm" data-act="plate" data-asset="' + esc(miss[0].id) + '">' + esc(t("t2_plate")) + "</button></div>"; }
			h += "</section>";
		}
		return h;
	}
	/* s.25ח in its own words, for a building system only; an appliance the landlord left points to the contract */
	function legalHtml(isSystem, isAppliance) {
		if (isSystem) { return '<p class="nt2-law">' + esc(t("t2_law_a")) + " " + esc(t("t2_law_b")) + "<small>" + esc(t("t2_law_src")) + "</small></p>"; }
		if (isAppliance) { return '<p class="nt2-law">' + esc(t("t2_law_appliance")) + "</p>"; }
		return "";
	}

	/* ---------- the two screens ---------- */
	function head(m, sub) {
		var u = m.u, p = N.ix.prop[u.property_id] || {}, multi = units().length > 1;
		return '<header class="nt2-head' + (multi ? " has-sw" : "") + '"><h1>' + esc((p.address ? p.address + ", " : "") + (u.label || "")) + "</h1>" + (N.store.d.demo ? '<span class="nt2-chip">' + esc(t("t2_example")) + "</span>" : "") +
			(multi ? '<button type="button" class="nt2-iconbtn" data-act="units" aria-label="' + esc(t("t2_units")) + '">' + ico("swap") + "</button>" : "") + (sub ? "<p>" + sub + "</p>" : "") + "</header>";
	}
	function nav(active, m) {
		var T = [["today", "today", "t2_nav_today"], ["home", "home", "t2_nav_home"], ["rent", "rent", "t2_nav_rent"], ["money", "money", "t2_nav_money"], ["docs", "docs", "t2_nav_docs"]];
		return '<nav class="nt2-nav" aria-label="' + esc(t("t2_nav_label")) + '">' + T.map(function (x) {
			return '<a href="#/' + (x[0] === "home" ? "property/" + (m ? m.u.property_id : "") : x[0]) + '" data-nav="' + x[0] + '"' + (x[0] === active ? ' aria-current="page"' : "") + ">" + ico(x[1]) + esc(t(x[2])) + "</a>";
		}).join("") + "</nav>";
	}
	function todayHtml(m) {
		var s = saying(m), h = head(m);
		h += '<div class="nt2-tb"><div class="nt2-tb-l">' + planBlock(m) + '<button type="button" class="nt2-tb-open" data-act="drawing" aria-label="' + esc(t("t2_plan_open")) + '"></button></div>';
		h += '<div class="nt2-tb-r"><div class="nt2-tb-d"><small>' + esc(t("t2_today")) + "</small><b>" + D(m.date) + '</b></div><div class="nt2-tb-s"><small>' + esc(t("t2_waiting")) + '</small><p class="nt2-say' + s.color + '">' + s.say + '</p></div><div class="nt2-tb-f">' + s.sub + "</div></div></div>";
		h += rulerHtml(m);
		h += '<div class="nt2-mid"><div class="nt2-recent"><h3>' + esc(t("t2_recent")) + "</h3>" + m.recent.map(function (r) { return '<div class="nt2-rec"><span class="nt2-tick" aria-hidden="true"><svg width="8" height="8" viewBox="0 0 12 12" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 6.3 5 8.8l4.5-5.2"/></svg></span><span>' + r.t + '</span><span class="nt2-mono nt2-rec-d">' + esc(dshort(r.d)) + "</span></div>"; }).join("") + "</div>" + cardHtml(m) + "</div>";
		h += '<div class="nt2-cam"><button type="button" class="nt2-btn nt2-btn--ink" data-act="cam-repair">' + ico("cam") + esc(t("t2_cam_fault")) + '</button><button type="button" class="nt2-btn nt2-btn--line" data-act="cam-doc">' + ico("doc") + esc(t("t2_cam_doc")) + "</button></div>";
		return h + nav("today", m);
	}
	function axisModel(l) {
		var T0 = N.todayIso(), sinceM = Math.max(0, Math.round((N.parse(T0) - N.parse(l.start_date)) / (30.44 * 86400000))), w0 = Math.floor(sinceM / 12) * 12;
		var ps = periods(l, N.addMonths(l.start_date, w0 + 12)), nd = nextDue(l), months = [];
		for (var i = 0; i < 12; i++) {
			var ym = N.addMonths(l.start_date, w0 + i).slice(0, 7), p = ps.find(function (x) { return x.ym === ym; }), st = "none";
			if (p) { st = p.state === "paid" ? "paid" : (p.state === "partial" ? "part" : (p.state === "open" && p.due < T0 ? "late" : "none")); }
			months.push({ ym: ym, p: p || null, st: st, now: ym === T0.slice(0, 7) });
		}
		return { months: months, nd: nd };
	}
	function rentHtml(m) {
		var l = m.l, h = head(m);
		if (!l) { return h + '<p class="nt2-empty">' + esc(t("t2_no_lease")) + "</p>" + nav("rent", m); }
		var A = axisModel(l), ten = N.tenantsOf(l), ni = nextIndex(l);
		var sel = S.sel && A.months.some(function (x) { return x.ym === S.sel; }) ? S.sel : (A.nd ? A.nd.ym : (A.months.find(function (x) { return x.now; }) || A.months[0]).ym);
		S.sel = sel;
		h = h.replace("</header>", "<p>" + t("t2_axis_sub", { names: esc(ten.map(function (c) { return c.name; }).join(", ") || "-"), rent: M(l.rent) }) + "</p></header>");
		h += '<div class="nt2-axis"><div class="nt2-ax-h"><b>' + esc(t("t2_axis_contract")) + "</b><span dir=\"ltr\">" + mono(dhe(l.start_date)) + (l.end_date ? " → " + mono(dhe(l.end_date)) : "") + "</span></div>";
		h += '<div class="nt2-ax-g" dir="ltr">' + A.months.map(function (x) {
			var aria = t("t2_m_aria", { month: mname(x.ym) }) + (x.st === "paid" ? ", " + t("t2_m_paid") : x.st === "part" ? ", " + t("t2_m_part") : x.st === "late" ? ", " + t("t2_m_late") : "") + (x.now ? ", " + t("t2_m_now") : "");
			return '<button type="button" class="nt2-mo is-' + x.st + (x.now ? " is-now" : "") + (x.ym === sel ? " is-sel" : "") + '" data-act="month" data-ym="' + x.ym + '" aria-label="' + esc(aria) + '" aria-pressed="' + (x.ym === sel) + '"><span class="nt2-mono">' + mnum(x.ym) + "</span>" + (ni && x.ym === ni.ym ? '<i class="nt2-mo-idx" aria-hidden="true"></i>' : "") + "</button>";
		}).join("") + "</div>";
		h += '<div class="nt2-ax-lg"><span><i class="lg-paid"></i>' + esc(t("t2_m_paid")) + '</span><span><i class="lg-part"></i>' + esc(t("t2_m_part")) + '</span><span><i class="lg-late"></i>' + esc(t("t2_m_late")) + '</span><span><i class="lg-now"></i>' + esc(t("t2_m_now")) + "</span>" + (ni ? '<span><i class="lg-idx"></i>' + esc(t("t2_idx_row")) + "</span>" : "") + "</div></div>";
		/* three honest numbers from the books */
		var mo = N.moneyOf(l), yr = 0; (N.ix.ledgerByLease[l.id] || []).forEach(function (r) { if (r.kind === "payment" && r.category === "rent" && (r.status === "paid" || r.status === "deposited")) { yr += N.mx.incomeOf(r); } });
		h += '<ul class="nt2-sum"><li><span>' + esc(t("t2_sum_rent")) + "</span><b>" + M(l.rent) + "</b></li><li><span>" + esc(t("t2_sum_got")) + "</span><b>" + M(Math.round(yr / 100)) + "</b></li><li><span>" + esc(t("t2_sum_open")) + "</span><b>" + M(Math.max(0, Math.round(mo.balance / 100))) + "</b></li>" + indexRow(l, indexDue(l)) + "</ul>";
		h += sheetNext(l, A, sel);
		return h + nav("rent", m);
	}
	/* an index-linked lease always shows its index line here: the next update with one button, or that none is left */
	function indexRow(l, ni) {
		if (!l || !l.linkage || l.linkage.mode !== "cpi") { return ""; }
		if (!ni) { return '<li class="nt2-sum-idx"><span>' + esc(t("t2_idx_row")) + "</span><b>" + esc(t("t2_idx_none")) + "</b></li>"; }
		return '<li class="nt2-sum-idx' + (ni.past ? " is-past" : "") + '"><button type="button" class="nt2-sum-btn" data-act="index" data-due="1"><span>' + (ni.past ? esc(t("t2_idx_past", { date: N.dateText(ni.date) })) : esc(t("t2_idx_line")) + " · " + D(ni.date)) + "</span><b>" + esc(t("t2_idx_calc")) + "</b></button></li>";
	}
	function sheetNext(l, A, sel) {
		var cur = A.months.find(function (x) { return x.ym === sel; }), p = cur && cur.p, isNext = A.nd && A.nd.ym === sel, paid = cur && cur.st === "paid", ten = N.tenantsOf(l)[0];
		var idx = A.months.indexOf(cur), kick = paid ? t("t2_k_done") : (isNext ? t("t2_k_next") : t("t2_k_sel"));
		var h = '<section class="nt2-next" aria-live="polite"><div class="nt2-grab" aria-hidden="true"></div><div class="nt2-next-h"><div><div class="nt2-kick">' + esc(kick) + "</div><h2>" + esc(t("t2_rent_for", { month: mname(sel) })) + '</h2></div><button type="button" class="nt2-round" data-act="prev" aria-label="' + esc(t("t2_prev")) + '"' + (idx <= 0 ? " disabled" : "") + ">" + ico("up") + '</button><button type="button" class="nt2-round" data-act="next" aria-label="' + esc(t("t2_next")) + '"' + (idx >= 11 ? " disabled" : "") + ">" + ico("down") + "</button></div>";
		if (p) {
			var days = N.daysTo(p.due);
			h += '<div class="nt2-next-l">' + D(p.due) + " · " + esc(paid ? t("t2_paid_full") : N.when(days)) + "</div><div class=\"nt2-next-l\">" + M((paid ? p.amount : p.remaining) / 100) + (cur.st === "part" ? " · " + esc(t("t2_m_part")) : "") + "</div>";
		} else { h += '<div class="nt2-next-l">' + esc(t("t2_no_charge")) + "</div>"; }
		if (isNext && !paid) { h += '<div class="nt2-next-l"><b class="nt2-step">' + esc(t("t2_step")) + "</b> " + esc(t("t2_step_rent")) + '</div><button type="button" class="nt2-btn nt2-btn--go nt2-btn--pill" data-act="rent" data-ym="' + sel + '">' + esc(t("t2_received")) + "</button>"; }
		if (!paid && N.canMsg(ten)) { h += '<button type="button" class="nt2-btn nt2-btn--line nt2-btn--pill" data-act="remind">' + esc(t("t2_remind")) + "</button>"; }
		return h + "</section>";
	}

	/* ---------- sheets ---------- */
	function openSheet(title, html, o) {
		closeSheet(true);
		o = o || {};
		var el = document.createElement("div");
		el.className = "nt2-sw";
		el.innerHTML = '<div class="nt2-scrim" data-close></div><section class="nt2-sheet" role="dialog" aria-modal="true" aria-labelledby="nt2-st" tabindex="-1"><div class="nt2-grab" aria-hidden="true"></div><div class="nt2-sheet-h"><h2 id="nt2-st">' + title + '</h2><button type="button" class="nt2-round" data-close aria-label="' + esc(t("close")) + '">' + ico("x") + '</button></div><div class="nt2-sheet-b">' + html + "</div></section>";
		host.appendChild(el);
		sheetEl = el;
		el.addEventListener("click", function (e) { if (e.target.closest("[data-close]")) { closeSheet(); } });
		requestAnimationFrame(function () { el.classList.add("is-in"); var f = el.querySelector(".nt2-sheet"); if (f) { f.focus({ preventScroll: true }); } });
		return el;
	}
	function closeSheet(instant) {
		if (!sheetEl) { return; }
		var el = sheetEl; sheetEl = null; S.sheet = null;
		if (instant) { el.remove(); } else { el.classList.remove("is-in"); setTimeout(function () { el.remove(); }, 180); }
	}
	function setSheetBody(html) { if (sheetEl) { sheetEl.querySelector(".nt2-sheet-b").innerHTML = html; } }

	function drawingSheet(u, focus) {
		var m = model(u), ps = m.parts;
		var el = openSheet(esc(t("t2_plan_title")), '<div class="nt2-dr" id="nt2-dr"></div><div id="nt2-part"></div>');
		var box = el.querySelector("#nt2-dr");
		var show = function (id) {
			var p = ps.find(function (x) { return x.id === id; });
			if (!p) { return; }
			var tk = openTickets(u).find(function (x) { var q = ticketPart(u, x); return q && q.id === p.id; });
			var sys = SYSTEMS.indexOf(p.kind) >= 0, h = '<div class="nt2-pd"><h3>' + esc(p.label) + '</h3><p class="nt2-pd-s is-' + p.state + '">' + esc(t("t2_ps_" + p.state)) + "</p>" + legalHtml(sys, !sys) + '<div class="nt2-btns">';
			if (tk) { h += '<button type="button" class="nt2-btn nt2-btn--go" data-act="ticket" data-id="' + tk.id + '">' + esc(t("t2_open_repair")) + "</button>"; }
			else { h += '<button type="button" class="nt2-btn nt2-btn--ink" data-act="cam-part" data-asset="' + esc(p.id) + '">' + ico("cam") + esc(t("t2_cam_fault")) + "</button>"; }
			h += "</div></div>";
			el.querySelector("#nt2-part").innerHTML = h;
			N.plan2d.draw(box, planData(u, ps), { scale: 1, lit: p.id, layer: "all", interactive: true, onPick: show });
		};
		N.plan2d.draw(box, planData(u, ps), { scale: 1, lit: focus || m.lit, layer: "all", interactive: true, onPick: show });
		if (focus || m.lit) { show(focus || m.lit); }
	}
	/* a part of the home in one press: the kind is the whole form, the details can be filled later in the apartment's page */
	function addPart(u, kind) {
		if (!u || S.busy || !N.plan2d.KIND_LAYERS[kind]) { return; }
		S.busy = true;
		var m = Object.assign({}, u.meta || {}), list = (m.assets || []).slice(), name = t("ak_" + kind);
		list.push({ id: "a" + Date.now().toString(36), kind: kind, label: name });
		m.assets = list;
		N.store.save("unit", { id: u.id, property_id: u.property_id, meta: m }).then(function () {
			S.busy = false; closeSheet(true); N.ui.toast(t("t2_part_added", { name: name })); render();
		}).catch(function (e) { S.busy = false; N.ui.toast((e && e.message) || t("err_generic"), "bad"); });
	}
	function addPartSheet() {
		var h = '<p class="nt2-p">' + esc(t("t2_add_hint")) + '</p><div class="nt2-kinds">' + Object.keys(N.plan2d.KIND_LAYERS).map(function (k) {
			return '<button type="button" class="nt2-btn nt2-btn--line nt2-kind" data-act="add-kind" data-kind="' + k + '">' + N.plan2d.icon(k, 22) + "<span>" + esc(t("ak_" + k)) + "</span></button>";
		}).join("") + "</div>";
		openSheet(esc(t("t2_add_title")), h);
	}
	function unitsSheet() {
		var us = units(), h = '<ul class="nt2-ul">' + us.map(function (u) {
			var p = N.ix.prop[u.property_id] || {};
			return '<li><button type="button" class="nt2-btn nt2-btn--line nt2-btn--wide' + (+u.id === +S.unitId ? " is-on" : "") + '" data-act="unit" data-id="' + u.id + '">' + esc((p.address ? p.address + ", " : "") + (u.label || "")) + "</button></li>";
		}).join("") + "</ul>";
		openSheet(esc(t("t2_units")), h);
	}

	/* ---------- the index update that saves ---------- */
	function indexSheet(u, fromRow) {
		var l = N.ix.leaseByUnit[u.id], ni = fromRow ? indexDue(l) : nextIndex(l);
		if (!l || !ni) { return; }
		var ref = uid(), T0 = N.todayIso(), k = l.linkage, base = k.base_date || l.start_date, to = ni.date <= T0 ? ni.date : T0, due = ni.date <= N.addDays(T0, 7);
		var last = rentRows(l).filter(function (r) { return r.amount > 0 && /^rent:/.test(autoOf(r)) && (r.due_date || "") <= T0; }).sort(function (a, b) { return a.due_date < b.due_date ? -1 : 1; }).pop();
		var today = last ? last.amount / 100 : +l.rent;
		var rows = function (extra) {
			return '<dl class="nt2-kv"><div><dt>' + esc(t("t2_idx_today")) + "</dt><dd>" + M(today) + "</dd></div>" + extra + "</dl>";
		};
		var el = openSheet(esc(t("t2_idx_title")), '<p class="nt2-p">' + esc(t("t2_loading")) + "</p>");
		S.sheet = "index";
		N.store.cpi(+l.rent, base, to).then(function (r) {
			if (S.sheet !== "index" || !sheetEl) { return; }
			var bi = +r.from_index_value, ai = +r.to_index_value;
			/* the sample portfolio has a ratio only: shown on a base of 100, and the sheet says these are sample numbers */
			if (!(bi > 0 && ai > 0) && r.demo && +r.factor > 0) { bi = 100; ai = Math.round(100 * r.factor * 10) / 10; }
			if (!(bi > 0 && ai > 0)) { return noIndex(rows("")); }
			var pct = Math.max(0, Math.min(100, k.pct == null ? 100 : +k.pct)) / 100, nw = +l.rent * (1 + pct * (ai / bi - 1));
			if (k.floor == null || k.floor) { nw = Math.max(+l.rent, nw); }
			nw = Math.round(nw);
			var h = rows('<div><dt>' + esc(t("t2_idx_base")) + "</dt><dd>" + mono(bi.toFixed(1)) + '</dd></div><div><dt>' + esc(t("t2_idx_latest")) + "</dt><dd>" + mono(ai.toFixed(1)) + '</dd></div><div class="is-new"><dt>' + esc(t(due ? "t2_idx_new" : "t2_idx_asof", { date: N.dateText(ni.ym + "-01") })) + "</dt><dd>" + M(nw) + "</dd></div>");
			h += '<p class="nt2-p">' + esc(t("t2_idx_formula")) + (pct < 1 ? " " + esc(t("t2_idx_pct", { pct: N.num(Math.round(pct * 100)) })) : "") + ((k.floor == null || k.floor) ? " " + esc(t("t2_idx_floor")) : "") + '</p><p class="nt2-p nt2-small">' + esc(t(r.demo ? "t2_idx_demo" : "t2_idx_source")) + '</p><p class="nt2-err" role="alert" hidden></p>' + (due ? '<button type="button" class="nt2-btn nt2-btn--go nt2-btn--pill" data-act="idx-save">' + esc(t("t2_idx_save")) + "</button>" : '<p class="nt2-p nt2-wait" role="note">' + esc(t("t2_idx_wait", { date: N.dateText(ni.date) })) + '</p><button type="button" class="nt2-btn nt2-btn--line nt2-btn--pill" data-close>' + esc(t("close")) + "</button>");
			setSheetBody(h);
			S.idx = due ? { lease: l, unit: u, base: bi, applied: ai, amount: nw, ym: ni.ym, ref: ref } : null;
		}).catch(function () { if (S.sheet === "index" && sheetEl) { noIndex(rows("")); } });
		void el;
	}
	function noIndex(rowsHtml) {
		setSheetBody(rowsHtml + '<p class="nt2-p">' + esc(t("t2_idx_na")) + '</p><button type="button" class="nt2-btn nt2-btn--line nt2-btn--pill" data-act="idx-manual">' + esc(t("t2_idx_manual")) + "</button>");
	}
	function saveIndex(btn) {
		var X = S.idx;
		if (!X || S.busy) { return; }
		S.busy = true; btn.disabled = true; btn.textContent = t("saving");
		api().indexConfirm({ lease_id: X.lease.id, base_index: X.base, applied_index: X.applied, new_amount: X.amount, start_month: X.ym, client_ref: X.ref }).then(function (res) {
			S.busy = false;
			var d = N.store.d, ev = res && res.event;
			if (ev && !d.events.some(function (x) { return +x.id === +ev.id; })) { d.events.unshift(ev); }
			S.idx = null;
			setSheetBody('<p class="nt2-ok" role="status">' + esc(t("t2_idx_done", { month: N.monthName(X.ym), amount: N.moneyText(X.amount) })) + '</p><button type="button" class="nt2-btn nt2-btn--line nt2-btn--pill" data-close>' + esc(t("close")) + "</button>");
			N.store.emit("t2:index");
		}).catch(function (e) {
			S.busy = false; btn.disabled = false; btn.textContent = t("t2_idx_save");
			var er = sheetEl && sheetEl.querySelector(".nt2-err"); if (er) { er.hidden = false; er.textContent = (e && e.message) || t("err_generic"); }
		});
	}

	/* ---------- the one-press jobs ---------- */
	function markReceived(ym) {
		var u = units().find(function (x) { return +x.id === +S.unitId; }), l = u && N.ix.leaseByUnit[u.id];
		if (!l || S.busy) { return; }
		var p = periods(l, N.addMonths(N.todayIso(), 2)).find(function (x) { return x.ym === ym; });
		if (!p) { return; }
		var chq = N.pendingCheques(l).filter(function (c) { return (c.due_date || "").slice(0, 7) === ym; })[0], call;
		S.busy = true;
		/* a cheque of that month still waiting is deposited (it is the same money); otherwise the expected amount, dated today */
		if (chq) { call = N.store.money("ledger-act", { id: chq.id, act: "deposit", data: { date: N.todayIso() } }); }
		else { call = N.store.money("pay", { data: { lease_id: l.id, amount: p.remaining / 100, paid_date: N.todayIso(), method: ((l.terms || {}).method && l.terms.method !== "cheque") ? l.terms.method : "transfer", category: "rent", applies_to: p.row ? p.row.id : 0, note: "" } }); }
		call.then(function () {
			S.busy = false;
			N.ui.toast(t("t2_rent_saved"));
		}).catch(function (e) { S.busy = false; N.ui.toast((e && e.message) || t("err_generic"), "bad"); });
	}
	function takePhoto(kind, asset) {
		var inp = inputs[kind === "doc" ? "doc" : (kind === "plate" ? "plate" : "repair")];
		inp.dataset.asset = asset || "";
		inp.value = "";
		inp.click();
	}
	function onFile(kind, inp) {
		var f = inp.files && inp.files[0], u = units().find(function (x) { return +x.id === +S.unitId; });
		if (!f || !u || S.busy) { return; }
		var asset = inp.dataset.asset || "";
		S.busy = true;
		if (kind === "repair") {
			closeSheet(true);
			api().repair({ unit_id: u.id, title: t("t2_photo_title"), file: f, client_ref: uid(), asset: asset }).then(function (res) {
				S.busy = false;
				var d = N.store.d;
				if (res && res.ticket) { var i = d.tickets.findIndex(function (x) { return +x.id === +res.ticket.id; }); if (i >= 0) { d.tickets[i] = res.ticket; } else { d.tickets.push(res.ticket); } }
				if (res && res.doc) { d.docs.unshift(res.doc); }
				N.store.emit("t2:repair");
				N.ui.toast(t("t2_repair_saved"));
			}).catch(function (e) { S.busy = false; N.ui.toast((e && e.message) || t("err_generic"), "bad"); });
		} else if (kind === "doc") {
			N.store.upload(f, "unit", u.id, "other").then(function () { S.busy = false; N.ui.toast(t("t2_doc_saved")); }).catch(function (e) { S.busy = false; N.ui.toast((e && e.message) || t("err_generic"), "bad"); });
		} else {
			N.store.upload(f, "unit", u.id, "photo").then(function (doc) {
				var mt = Object.assign({}, u.meta || {}), list = (mt.assets || []).map(function (a) { return a.id === asset ? Object.assign({}, a, { plate: doc.id }) : a; });
				mt.assets = list;
				return N.store.save("unit", { id: u.id, property_id: u.property_id, meta: mt });
			}).then(function () { S.busy = false; N.ui.toast(t("t2_plate_saved")); }).catch(function (e) { S.busy = false; N.ui.toast((e && e.message) || t("err_generic"), "bad"); });
		}
	}

	/* ---------- the server ---------- */
	function restApi(c) {
		function call(path, opts) {
			opts.credentials = "same-origin";
			opts.headers = Object.assign({ "X-WP-Nonce": c.nonce || "", "X-NLRM-Lang": N.lang }, opts.json ? { "Content-Type": "application/json" } : {});
			return fetch(c.rest + path, opts).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) { var e = new Error(j.message || ("HTTP " + r.status)); e.status = r.status; throw e; } return j; }); });
		}
		return {
			repair: function (p) {
				var f = new FormData(); f.append("file", p.file); f.append("unit_id", p.unit_id); f.append("title", p.title); f.append("client_ref", p.client_ref); if (p.asset) { f.append("asset", p.asset); }
				var go = function () { return call("/rm/today/repair", { method: "POST", body: f }); };
				return go().catch(function (e) { if (!e.status) { return go(); } throw e; });
			},
			indexConfirm: function (p) {
				var go = function () { return call("/rm/today/index-confirm", { method: "POST", json: true, body: JSON.stringify(p) }); };
				return go().catch(function (e) { if (!e.status) { return go(); } throw e; });
			}
		};
	}
	/* the sample portfolio never talks to the server: its repair and its index confirmation live in the sample's own memory
	   (before 1.72.725 these two went to the real routes with the sample's ids) */
	function demoApi(ad) {
		return {
			repair: function (p) {
				var u = N.ix.unit[p.unit_id];
				return ad.save("ticket", { property_id: u.property_id, unit_id: u.id, title: p.title, body: "", category: "general", urgency: "standard", status: "new", reporter: "owner", vendor_id: 0, cost: 0, due_by: N.addDays(N.todayIso(), 30), meta: { via: "today-camera", asset: p.asset || "" } }).then(function (tk) {
					return ad.upload(p.file, "ticket", tk.id, "photo").then(function (doc) { return { ticket: tk, doc: doc }; });
				});
			},
			indexConfirm: function (p) {
				var l = N.ix.leaseByUnit[(S.idx && S.idx.unit || {}).id] || (N.store.d.leases || []).find(function (x) { return +x.id === +p.lease_id; });
				return ad.event({ scope: "lease", scope_id: l.id, type: "index_confirmed", channel: "", body: "", meta: { lease_id: l.id, start_month: p.start_month, base_index: p.base_index, applied_index: p.applied_index, old_amount: Math.round(l.rent * 100), new_amount: Math.round(p.new_amount * 100), client_ref: p.client_ref } }).then(function (ev) { return { lease_id: l.id, event: ev }; });
			}
		};
	}
	function api() { var ad = N.store.adapter; return (ad && ad.today2) || (ad && ad.demo ? demoApi(ad) : restApi(cfg)); }

	/* ---------- the layer's place on the screen (1.72.726) ----------
	   The site's own floating things (the WhatsApp bar, the basket, the accessibility button, the admin bar) are drawn ABOVE this
	   layer. The layer measures the ones that stand over its column and keeps a free strip for them, top and bottom, so nothing of
	   the screen sits under them at any width; and when what is left is short, the screen scrolls like a page (.is-short). */
	var keepT = 0, keepB = 0, probed = false, fitT = 0;
	/* what covers the layer's column is found by asking the browser, point by point, what is drawn on top (so it does not matter
	   how the covering thing is positioned: the admin bar is fixed on a desktop and absolute on a phone) */
	function probe() {
		var H = window.innerHeight, W = window.innerWidth, cw = Math.min(480, W), c0 = (W - cw) / 2, kt = 0, kb = 0, x, y;
		var mine = function (px, py) { var t = document.elementFromPoint(px, py); return !t || host.contains(t); };
		for (x = c0 + 4; x < c0 + cw; x += 12) {
			for (y = 2; y < 122; y += 4) { if (!mine(x, y)) { kt = Math.max(kt, y + 4); } }
			for (y = H - 2; y > H - 202 && y > H / 2; y -= 4) { if (!mine(x, y)) { kb = Math.max(kb, H - y + 12); } }
		}
		keepT = Math.min(kt, 120); keepB = Math.min(kb, 210); probed = true;
	}
	function fit(rescan) {
		if (!host || host.hidden) { return; }
		if (rescan || !probed) { probe(); }
		var H = window.innerHeight, kt = keepT, kb = keepB, eff = H - kt - kb;
		host.style.setProperty("--nt2-kt", kt + "px"); host.style.setProperty("--nt2-kb", kb + "px");
		host.setAttribute("data-keep", kt + "," + kb);
		host.classList.toggle("is-h700", eff <= 700); host.classList.toggle("is-h760", eff <= 760);
		/* short = under 600 px left, or a part of this screen does not fit what is left (measured, so no button can end under another).
		   A part that hides its overflow must fit exactly; a part that shows it may run over by the card's own bottom padding (12 px). */
		host.classList.remove("is-short");
		var over = body.scrollHeight > body.clientHeight + 1 || Array.prototype.some.call(body.children, function (c) { return c.scrollHeight > c.clientHeight + (window.getComputedStyle(c).overflowY === "hidden" ? 1 : 12); });
		host.classList.toggle("is-short", eff < 600 || over);
	}
	function fitSoon() { window.clearTimeout(fitT); fitT = window.setTimeout(function () { fit(true); }, 120); }

	/* ---------- the layer: mount, route, render ---------- */
	function route() {
		var h = (location.hash || "").replace(/^#\/?/, "");
		if (/^[tqasv]=/.test(h)) { return null; }
		var p = h.split("/")[0];
		return p === "" || p === "today" ? "today" : (p === "rent" ? "rent" : null);
	}
	function enabled() {
		try { if (new URLSearchParams(location.search).get("today") === "classic" || localStorage.getItem("nlrm_today2") === "off") { return false; } } catch (e) { /* private mode */ }
		return cfg.today2 !== false;
	}
	function render() {
		if (!host || !N.store.d || !N.ix.unit) { return; }
		var r = enabled() ? route() : null, u = r ? pickUnit() : null, de = document.documentElement;
		if (!r || !u) { host.hidden = true; de.classList.remove("nt2-on"); return; }
		var d = N.store.d;
		if (!d.properties.length && !d.demo) { host.hidden = true; de.classList.remove("nt2-on"); return; } /* a new landlord keeps the onboarding of the app */
		var wasHidden = host.hidden;
		host.hidden = false; de.classList.add("nt2-on");
		host.setAttribute("dir", N.rtl ? "rtl" : "ltr"); host.setAttribute("lang", N.lang);
		var m = model(u), f = document.activeElement, fk = f && f.closest && f.closest("#nt2-body") ? (f.getAttribute("data-act") || "") + "|" + (f.getAttribute("data-ym") || "") : "";
		body.innerHTML = r === "rent" ? rentHtml(m) : todayHtml(m);
		body.className = "nt2-app nt2-s-" + r + " nt2-m-" + m.state;
		if (r === "today") {
			var box = body.querySelector("#nt2-plan");
			N.plan2d.draw(box, planData(u, m.parts), { scale: m.parts.length && planOf(u) ? 0.62 : 1, lit: m.lit, layer: m.layer, interactive: !planOf(u), max: 6, onPick: function (id) { drawingSheet(u, id); } });
			box.classList.toggle("is-row", !planOf(u));
		}
		if (fk) { var again = Array.prototype.find.call(body.querySelectorAll("[data-act]"), function (x) { return (x.getAttribute("data-act") || "") + "|" + (x.getAttribute("data-ym") || "") === fk; }); if (again && !sheetEl) { again.focus({ preventScroll: true }); } }
		fit(wasHidden); /* after the content is in: the strips, and whether this screen must scroll */
	}
	function onClick(e) {
		var b = e.target.closest("[data-act]");
		if (!b) { return; }
		var a = b.getAttribute("data-act"), u = units().find(function (x) { return +x.id === +S.unitId; });
		switch (a) {
			case "cam-repair": takePhoto("repair"); break;
			case "cam-part": takePhoto("repair", b.getAttribute("data-asset")); break;
			case "cam-doc": takePhoto("doc"); break;
			case "plate": takePhoto("plate", b.getAttribute("data-asset")); break;
			case "ticket": closeSheet(true); N.open("ticket", +b.getAttribute("data-id")); break;
			case "drawing": if (u) { drawingSheet(u, null); } break;
			case "units": unitsSheet(); break;
			case "add-kind": addPart(u, b.getAttribute("data-kind")); break;
			case "add-part": addPartSheet(); break;
			case "unit": closeSheet(true); S.unitId = +b.getAttribute("data-id"); S.sel = null; render(); break;
			case "index": if (u) { indexSheet(u, b.hasAttribute("data-due")); } break;
			case "idx-save": saveIndex(b); break;
			case "idx-manual": closeSheet(true); N.state.mtab = "cpi"; N.go("money"); break;
			case "rent": markReceived(b.getAttribute("data-ym")); break;
			case "task": N.store.save("task", { id: +b.getAttribute("data-id"), done: true }).then(function () { N.ui.toast(t("saved")); }).catch(function (er) { N.ui.toast((er && er.message) || t("err_generic"), "bad"); }); break;
			case "month": S.sel = b.getAttribute("data-ym"); render(); break;
			case "prev": case "next": step(a === "next" ? 1 : -1); break;
			case "remind": var l = u && N.ix.leaseByUnit[u.id]; if (l) { var el = document.createElement("i"); el.dataset.lease = l.id; N.act("wa-remind", el, e); } break;
		}
	}
	function step(dir) {
		var u = units().find(function (x) { return +x.id === +S.unitId; }), l = u && N.ix.leaseByUnit[u.id];
		if (!l) { return; }
		var A = axisModel(l), i = A.months.findIndex(function (x) { return x.ym === S.sel; }), j = Math.max(0, Math.min(11, i + dir));
		S.sel = A.months[j].ym; render();
	}
	N.mountToday = function (root, o) {
		if (started) { return; }
		started = true;
		cfg = o || {};
		host = document.createElement("div");
		host.id = "nt2"; host.className = "nt2"; host.hidden = true;
		host.innerHTML = '<div id="nt2-body" class="nt2-app"></div>';
		body = host.querySelector("#nt2-body");
		["repair", "doc", "plate"].forEach(function (k) {
			var i = document.createElement("input"); i.type = "file"; i.accept = "image/*"; i.setAttribute("capture", "environment"); i.className = "nt2-file"; i.tabIndex = -1; i.setAttribute("aria-hidden", "true");
			i.addEventListener("change", function () { onFile(k, i); });
			host.appendChild(i); inputs[k] = i;
		});
		(root && root.parentNode ? root.parentNode : document.body).insertBefore(host, root || null);
		host.addEventListener("click", onClick);
		document.addEventListener("keydown", function (e) { if (e.key === "Escape" && sheetEl) { closeSheet(); } });
		N.store.on(function () { render(); });
		window.addEventListener("hashchange", function () { closeSheet(true); render(); });
		window.addEventListener("resize", fitSoon);
		[400, 1500, 3500, 7000, 12000].forEach(function (ms) { window.setTimeout(function () { fit(true); }, ms); }); /* the site's buttons arrive late */
		render();
	};
	T2.model = function () { var u = units().find(function (x) { return +x.id === +S.unitId; }); return u ? model(u) : null; };
	T2.state = S;
})();
