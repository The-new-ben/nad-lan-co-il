/* ============================================================================
   NADLAN RENTALS v2 - start from Excel (HAD-383)
   The landlord copies rows from Excel or Google Sheets and pastes them here.
   Columns are recognised in Hebrew or English; a preview shows what will be
   created; then buildings, apartments, tenants and leases are created in order.
   A lease that started before this month is followed from this month (its
   money before that is the landlord's history, not a debt to invent).
============================================================================ */
(function () {
	"use strict";
	var N = window.NLRM, esc = N.esc, t = function (k, v) { return N.t(k, v); };
	var COLS = {
		address: ["כתובת", "רחוב", "address", "street"], city: ["עיר", "ישוב", "יישוב", "city", "town"],
		label: ["דירה", "שם הדירה", "מספר דירה", "apartment", "apt", "unit"], floor: ["קומה", "floor"],
		rooms: ["חדרים", "rooms"], tenant: ["שוכר", "שם השוכר", "tenant", "tenant name"], phone: ["טלפון", "נייד", "phone", "mobile"],
		rent: ["שכר דירה", "שכירות", "סכום", "rent", "monthly rent"], start: ["תחילת חוזה", "תחילה", "מתאריך", "start", "lease start"],
		end: ["סיום חוזה", "סיום", "עד תאריך", "end", "lease end"], pay_day: ["יום תשלום", "pay day"]
	};
	function norm(s) { return String(s || "").trim().toLowerCase().replace(/["'״׳]/g, ""); }
	function parse(text) {
		var lines = String(text || "").replace(/\r/g, "").split("\n").filter(function (l) { return l.trim(); });
		if (!lines.length) { return { rows: [], map: {} }; }
		var sep = lines[0].indexOf("\t") >= 0 ? "\t" : (lines[0].indexOf(";") >= 0 ? ";" : ",");
		var cells = lines.map(function (l) { return l.split(sep).map(function (c) { return c.trim().replace(/^"|"$/g, ""); }); });
		var head = cells[0].map(norm), map = {};
		Object.keys(COLS).forEach(function (k) { var i = head.findIndex(function (h) { return COLS[k].some(function (w) { return h === norm(w) || h.indexOf(norm(w)) === 0; }); }); if (i >= 0) { map[k] = i; } });
		return { rows: cells.slice(1), map: map };
	}
	function date(s) {
		s = String(s || "").trim();
		var m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/) || null;
		if (m) { return m[1] + "-" + m[2].padStart(2, "0") + "-" + m[3].padStart(2, "0"); }
		m = s.match(/^(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})$/);
		if (m) { var y = m[3].length === 2 ? "20" + m[3] : m[3]; return y + "-" + m[2].padStart(2, "0") + "-" + m[1].padStart(2, "0"); }
		return "";
	}
	function num(s) { var n = parseFloat(String(s || "").replace(/[^\d.]/g, "")); return isNaN(n) ? 0 : n; }
	/* importing again never doubles: what is already in the account is found and reused */
	function same(a, b) { return norm(a).replace(/\s+/g, " ").replace(/[,.]/g, "") === norm(b).replace(/\s+/g, " ").replace(/[,.]/g, ""); }
	function findProp(address, city) { return N.store.d.properties.find(function (p) { return same(p.address, address) && same(p.city, city); }) || null; }
	function findUnit(pid, x) { var lab = x.label || t("apt_floor", { n: x.floor }); return N.store.d.units.find(function (u) { return u.property_id === pid && same(u.label, lab) && (+u.floor === +x.floor || !x.label); }) || null; }
	function findContact(name, phone) { var ph = N.phone(phone); return N.store.d.contacts.find(function (c) { return (ph && c.phone && N.phone(c.phone) === ph) || (!ph && same(c.name, name)); }) || null; }
	N.forms.importSheet = function () {
		N.ui.open({ kind: "sheet", title: t("imp_title"), body: '<form class="nlrm-form" id="nlrm-imp"><p class="nlrm-lead">' + esc(t("imp_lead")) + '</p><label class="nlrm-f is-wide"><span>' + esc(t("imp_paste")) + '</span><textarea name="txt" rows="8" dir="auto" placeholder="' + esc(t("imp_ph")) + '"></textarea></label><div id="nlrm-imp-prev"></div><div class="nlrm-fbtns"><button type="button" class="nlrm-btn nlrm-btn--secondary" data-imp="check">' + esc(t("imp_check")) + '</button><button type="submit" class="nlrm-btn nlrm-btn--primary" disabled>' + esc(t("imp_go")) + '</button></div><p class="nlrm-ferr" role="alert" hidden></p></form>', wire: function (b) {
			var form = b.querySelector("form"), prev = b.querySelector("#nlrm-imp-prev"), go = b.querySelector('[type="submit"]'), err = b.querySelector(".nlrm-ferr"), plan = null;
			var check = function () {
				var p = parse(form.txt.value), m = p.map;
				err.hidden = true;
				if (m.address == null || m.city == null) { prev.innerHTML = ""; err.hidden = false; err.textContent = t("imp_need"); go.disabled = true; return; }
				plan = p.rows.map(function (r) {
					var g = function (k) { return m[k] != null ? r[m[k]] || "" : ""; };
					return { address: g("address"), city: g("city"), label: g("label"), floor: parseInt(g("floor"), 10) || 1, rooms: num(g("rooms")), tenant: g("tenant"), phone: g("phone"), rent: Math.round(num(g("rent"))), start: date(g("start")), end: date(g("end")), pay_day: parseInt(g("pay_day"), 10) || 1 };
				}).filter(function (x) { return x.address && x.city; });
				var buildings = {}; plan.forEach(function (x) { buildings[x.address + "|" + x.city] = 1; });
				var known = Object.keys(buildings).filter(function (k) { var a = k.split("|"); return !!findProp(a[0], a[1]); }).length;
				var dup = plan.filter(function (x) { var p = findProp(x.address, x.city); return p && findUnit(p.id, x); }).length;
				prev.innerHTML = '<p class="nlrm-hint">' + esc(t("imp_found", { b: Object.keys(buildings).length, u: plan.length, t: plan.filter(function (x) { return x.tenant; }).length })) +
					(known ? " " + esc(N.tn("imp_known", known)) : "") + (dup ? " " + esc(N.tn("imp_dup", dup)) : "") + '</p><table class="nlrm-table"><tbody>' + plan.slice(0, 8).map(function (x) { return "<tr><td>" + esc(x.address + ", " + x.city) + "</td><td>" + esc(x.label || "") + "</td><td>" + esc(x.tenant || "-") + '</td><td class="is-num">' + (x.rent ? N.money(x.rent) : "-") + "</td></tr>"; }).join("") + "</tbody></table>";
				go.disabled = !plan.length;
			};
			b.querySelector('[data-imp="check"]').addEventListener("click", check);
			form.txt.addEventListener("paste", function () { setTimeout(check, 30); });
			form.addEventListener("submit", function (e) {
				e.preventDefault();
				if (!plan || !plan.length) { return; }
				go.disabled = true; go.textContent = t("saving");
				var props = {}, chain = Promise.resolve(), made = 0, kept = 0;
				plan.forEach(function (x) {
					chain = chain.then(function () {
						var key = x.address + "|" + x.city, rows = plan.filter(function (y) { return y.address + "|" + y.city === key; });
						var floors = Math.max.apply(null, rows.map(function (y) { return y.floor; }).concat([1]));
						var perFloor = {}; rows.forEach(function (y) { perFloor[y.floor] = (perFloor[y.floor] || 0) + 1; });
						var upf = Math.min(24, Math.max.apply(null, [4].concat(Object.keys(perFloor).map(function (f) { return perFloor[f]; }))));
						var have = props[key] || findProp(x.address, x.city);
						var getProp = have ? Promise.resolve(have) : N.store.save("property", { address: x.address, city: x.city, title: x.address + ", " + x.city, floors: floors, units_per_floor: upf, meta: {} });
						return getProp.then(function (p) {
							props[key] = p;
							/* an existing building grows when the sheet has a higher floor or more apartments on a floor (never shrinks) */
							var onFloor = N.store.d.units.filter(function (u) { return u.property_id === p.id && u.floor === x.floor; }).length + 1;
							if (floors > (p.floors || 1) || onFloor > (p.units_per_floor || 4)) {
								return N.store.save("property", { id: p.id, floors: Math.max(floors, p.floors || 1), units_per_floor: Math.min(24, Math.max(onFloor, upf, p.units_per_floor || 4)) }).then(function (p2) { props[key] = p2; return p2; });
							}
							return p;
						}).then(function (p) {
							var u0 = findUnit(p.id, x);
							if (u0) { return { unit: u0, old: true }; }
							var taken = N.store.d.units.filter(function (u) { return u.property_id === p.id && u.floor === x.floor; }).length;
							return N.store.save("unit", { property_id: p.id, label: x.label || t("apt_floor", { n: x.floor }), floor: x.floor, pos: Math.min(23, taken), rooms: x.rooms || null, meta: {} }).then(function (u) { return { unit: u, old: false }; });
						}).then(function (r) {
							var u = r.unit;
							/* an apartment already rented is left as it is: importing the same sheet twice changes nothing */
							if (r.old && N.ix.leaseByUnit[u.id]) { kept++; return null; }
							if (!x.tenant) { if (r.old) { kept++; } else { made++; } return null; }
							var c0 = findContact(x.tenant, x.phone);
							return (c0 ? Promise.resolve(c0) : N.store.save("contact", { kind: "tenant", name: x.tenant, phone: N.phone(x.phone), lang: N.lang })).then(function (c) {
								made++;
								if (!x.rent || !x.start) { return null; }
								return N.store.save("lease", { unit_id: u.id, status: "active", start_date: x.start, end_date: x.end || N.addDays(N.addMonths(x.start, 12), -1), rent: x.rent, pay_day: x.pay_day, linkage: { mode: "none" }, securities: {}, parties: { tenants: [c.id] }, terms: { method: "transfer", track_from: x.start < N.todayIso().slice(0, 8) + "01" ? N.todayIso().slice(0, 8) + "01" : "" } });
							});
						});
					});
				});
				chain.then(function () { N.ui.close(); N.ui.toast(t("imp_done", { n: made }) + (kept ? " " + N.tn("imp_kept", kept) : "")); N.go("properties"); }).catch(function (ex) { err.hidden = false; err.textContent = (ex && ex.message) || t("err_generic"); go.disabled = false; go.textContent = t("imp_go"); });
			});
		} });
	};
})();
