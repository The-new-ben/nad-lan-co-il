/* The browser twin (rm-core.js N.mx.fold) against the PHP engine (nlrm_money_fold),
   on every lease of the 10-year run (out/parity.json, written by sim10.php).
   node scripts/rentals/sim/parity.js [out/parity.json] */
"use strict";
var fs = require("fs"), path = require("path");
var file = process.argv[2] || path.join(__dirname, "out", "parity.json");
global.window = global;
global.document = { addEventListener: function () {}, getElementById: function () { return null; }, documentElement: { classList: { add: function () {}, remove: function () {} } } };
global.addEventListener = function () {};
global.history = { pushState: function () {} };
eval(fs.readFileSync(path.join(__dirname, "../../../plugins/nadlan-config/assets/rentals/rm-core.js"), "utf8"));
var N = window.NLRM, data = JSON.parse(fs.readFileSync(file, "utf8"));
var keys = ["due", "future", "credit", "balance", "pending", "pending_n", "deposit_in", "deposit_out", "deposit_applied", "deposit_held", "writeoff", "refunded", "oldest_due", "late_days", "open_n"];
var ok = 0, bad = 0, fields = 0, t0 = Date.now();
data.leases.forEach(function (l) {
	var js = N.mx.fold(l.rows, data.today).sum, php = l.php, diff = [];
	keys.forEach(function (k) { fields++; var a = js[k], b = php ? php[k] : undefined; if (k === "oldest_due") { a = a || null; b = b || null; } else { b = +b; } if (a !== b) { diff.push(k + " js=" + a + " php=" + b); } });
	if (diff.length) { bad++; if (bad <= 10) { console.log("lease " + l.id + ": " + diff.join(", ")); } } else { ok++; }
});
/* the calendar: JS periods = PHP periods on the traps (31st, leap day, 15th) */
var cal = [["2027-01-31", "2028-01-30", 28], ["2028-02-29", "2030-02-28", 28], ["2026-11-15", "2027-11-14", 15], ["2026-10-01", "2036-09-30", 1]];
var calOk = cal.every(function (c) { var p = N.mx.periods({ id: 1, start_date: c[0], end_date: c[1], pay_day: c[2], rent: 1000 }, "2040-01-01"); return p.length === (c[0] === "2026-10-01" ? 120 : c[0] === "2028-02-29" ? 24 : 12); });
console.log("leases " + data.leases.length + ", summaries identical " + ok + ", different " + bad + ", fields compared " + fields + " (" + (Date.now() - t0) + " ms); calendar traps " + (calOk ? "OK" : "FAIL"));
process.exit(bad || !calOk ? 1 : 0);
