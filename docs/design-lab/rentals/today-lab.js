/* Lab only (never shipped): the sample portfolio of the design lab, shaped for the slice-1 screens.
   - plans for three apartments (the 7th apartment of the board is Apt 7 = unit 11), none for unit 31 (the no-plan fallback);
   - scenes (?scene=urgent|soon|index|quiet) that move the sample's dates so each state of the main card can be pressed;
   - the two server jobs of inc/rentals/today.php, answered in memory (the real ones are PHP). */
(function () {
	"use strict";
	var N = window.NLRM, L = window.TodayLab = {};
	var PLAN = function () {
		var R = function (id, kind, x0, y0, x1, y1) { return { id: id, kind: kind, poly: [[x0, y0], [x1, y0], [x1, y1], [x0, y1]] }; };
		return { rooms: [R("r1", "living", 0, 0, 190, 160), R("r2", "kitchen", 188, 0, 342, 160), R("r3", "hall", 0, 158, 342, 202), R("r4", "bedroom", 0, 200, 112, 342), R("r5", "mamad", 108, 198, 204, 342), R("r6", "bath", 200, 200, 272, 342), R("r7", "laundry", 270, 200, 342, 342)] };
	};
	var AT = { a1: [306, 226], a2: [30, 30], a3: [250, 180], a4: [264, 126], a5: [218, 30] };
	L.install = function (q, lang) {
		window.__sliceOn = q.get("slice") === "1";
		if (q.get("slice") !== "1") { return; } /* the existing labs see the sample exactly as before */
		(function () { var st = document.createElement("style"); st.textContent = "li { margin: 8px 0; }"; document.head.appendChild(st); })(); /* what the live theme does to every list item (found pressing 1.72.723 live) */
		var scene = q.get("scene") || "", orig = N.demoData;
		N.demoData = function (lg) {
			var d = orig(lg), en = lg !== "he", T = N.todayIso();
			d.units.forEach(function (u) {
				if (u.id === 31) { return; }
				u.meta.plan = PLAN();
				(u.meta.assets || []).forEach(function (a) { if (AT[a.id]) { a.at = AT[a.id].slice(); } });
			});
			var tk = d.tickets.find(function (x) { return x.id === 501; }); if (tk) { tk.meta.asset = "a1"; }
			if (scene !== "urgent" && scene !== "") { d.tickets.forEach(function (x) { if (x.status !== "done") { x.status = "done"; x.closed_at = T + " 08:00:00"; } }); }
			var l201 = d.leases.find(function (x) { return x.id === 201; });
			if (scene === "index") { l201.linkage.every = 15; }
			if (scene === "soon" || scene === "index") {
				var l202 = d.leases.find(function (x) { return x.id === 202; }), due = N.addDays(T, 3);
				l202.pay_day = N.parse(due).getDate();
				d.ledger.forEach(function (r) { if (r.lease_id === 202 && r.auto_key === "rent:202:" + T.slice(0, 7)) { r.due_date = due; } });
				d.tasks.push({ id: 801, scope: "unit", scope_id: 12, title: en ? "Clean the A/C filters" : "ניקוי מסנני המזגן", due: due, done: false });
			}
			return d;
		};
	};
	/* since 1.72.725 the product itself serves the sample portfolio (rm-today.js demoApi and the sample index numbers);
	   the lab adds nothing here, so it presses exactly what a visitor of the sample presses */
	L.attach = function () {};
})();
