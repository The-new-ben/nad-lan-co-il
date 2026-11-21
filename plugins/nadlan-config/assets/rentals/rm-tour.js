/* ============================================================================
   NADLAN RENTALS - the tour of the example portfolio (HAD-795, 21.11.2026)
   Runs only on /my-rentals/?sample=1 (the bar #nlrm-tour is printed by inc/rentals/page.php).
   It walks the REAL screens of the app on the sample data, one press each, with no dead end:
   the apartment today, the tenant, rent and payments, the index update, the lease and its securities,
   repairs, documents, the tax estimate, and "start with my own apartment".
   It draws nothing of its own but the bar: every stop opens the app's own screen through the app's own
   router and cards. A stop for a function that does not exist is not listed.
   The bar stands at the top of the screen; the day screen measures what is drawn above it and makes room.
============================================================================ */
(function () {
	"use strict";
	var bar = document.getElementById("nlrm-tour"), N = window.NLRM;
	if (!bar || !N || bar.dataset.wired) { return; }
	bar.dataset.wired = "1";
	var HE = (bar.dataset.lang || "he") === "he", U = +bar.dataset.unit || 21, at = 0, ready = false;
	var T = function (he, en) { return HE ? he : en; };
	var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
	/* the bar stays above the app's own cards; a card opens under it, never behind it */
	/* the day screen hides the page's other parts while it is open (rm-today.css: html.nt2-on .nlrm-page > *); the bar is the
	   one part that must stay (found on the live page, 1.72.734; the lab page did not wrap the bar in .nlrm-page) */
	var css = "html.nlrm-touring .nlrm-layer{top:var(--nlrm-tour-h,0px)!important}html.nt2-on .nlrm-page>.nlrm-tour,html .nlrm-page>.nlrm-tour{visibility:visible!important}" +
		".nlrm-tour{position:fixed;inset-inline:0;top:var(--wp-admin--admin-bar--height,0px);z-index:100002;display:grid;grid-template-columns:auto auto 1fr;align-items:center;gap:6px 10px;padding:8px 14px;background:#0d2129;color:#fff;font-family:'Assistant','Heebo',sans-serif;box-shadow:0 6px 18px rgba(13,33,41,.35)}" +
		".nlrm-tour a{text-decoration:none!important}.nlrm-tour .nlrm-lk{margin:0;color:#fff;gap:8px;display:inline-flex;align-items:center;line-height:1}.nlrm-tour .nlrm-lk svg{fill:#fff;width:26px;height:26px}.nlrm-tour .nlrm-lk svg .nlrm-lk-lit{fill:#7fd3e6}" +
		".nlrm-tour .nlrm-lk b{font-weight:800;font-size:19px;color:#fff}.nlrm-tour .nlrm-lk i{font-style:normal;font-weight:600;font-size:19px;color:#7fd3e6}" +
		".nlrm-tour-ex{height:22px;padding:0 9px;display:inline-flex;align-items:center;border:1.5px solid #fff;border-radius:11px;font-size:12px;font-weight:700;white-space:nowrap}" +
		".nlrm-tour a.nlrm-tour-go{justify-self:end;height:40px;padding:0 14px;display:inline-flex;align-items:center;border-radius:20px;background:#7fd3e6!important;color:#0d2129!important;font-size:14px;font-weight:800;white-space:nowrap}" +
		".nlrm-tour-row{grid-column:1/-1;display:flex;align-items:center;gap:8px;min-width:0}" +
		".nlrm-tour button.nlrm-tour-b{flex:none;height:44px!important;min-width:44px!important;padding:0 14px!important;margin:0!important;border:0!important;border-radius:22px!important;background:#fff!important;color:#14212b!important;font:800 15px/1 'Assistant','Heebo',sans-serif!important;text-transform:none!important;letter-spacing:0!important;box-shadow:none!important;cursor:pointer;white-space:nowrap}" +
		".nlrm-tour button.nlrm-tour-b.is-next{background:#7fd3e6!important}.nlrm-tour button.nlrm-tour-b[disabled]{opacity:.45;cursor:default}" +
		".nlrm-tour-t{min-width:0;flex:1;display:flex;flex-direction:column;line-height:1.2}.nlrm-tour-t small{font:600 12px/1.3 'IBM Plex Mono',monospace;color:#cfdbe3;direction:ltr;text-align:start;unicode-bidi:isolate}" +
		".nlrm-tour-t b{font-size:16px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#fff}" +
		".nlrm-tour-dots{display:none;gap:6px;flex:none}.nlrm-tour-dots button{width:44px!important;height:44px!important;min-width:0!important;padding:0!important;margin:0!important;border:0!important;border-radius:22px!important;background:rgba(255,255,255,.12)!important;color:#fff!important;font:600 14px/1 'IBM Plex Mono',monospace!important;box-shadow:none!important;cursor:pointer}" +
		".nlrm-tour-dots button.is-on{background:#fff!important;color:#14212b!important}" +
		"@media(min-width:900px){.nlrm-tour{grid-template-columns:auto auto 1fr auto;padding:10px 24px}.nlrm-tour-row{grid-column:auto;grid-row:1;order:3;justify-self:stretch}.nlrm-tour a.nlrm-tour-go{order:4}.nlrm-tour-dots{display:flex}}" +
		".nlrm-tour-brand{min-width:0;overflow:hidden}" +
		"@media(max-width:420px){.nlrm-tour{gap:6px 7px;padding:8px 10px}.nlrm-tour .nlrm-lk{gap:6px}.nlrm-tour .nlrm-lk svg{width:22px;height:22px}.nlrm-tour .nlrm-lk b,.nlrm-tour .nlrm-lk i{font-size:16px}.nlrm-tour-ex{font-size:11px;padding:0 7px}.nlrm-tour a.nlrm-tour-go{padding:0 10px;font-size:13px}}";
	var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

	var D = function () { return N.store && N.store.d; };
	var closeAll = function () { try { N.ui.close(true); } catch (e) { /* nothing open */ } };
	var hash = function (h) { if (location.hash !== h) { location.hash = h; } else { window.dispatchEvent(new HashChangeEvent("hashchange")); } };
	var leaseOf = function (u) { return (D().leases || []).filter(function (l) { return +l.unit_id === +u && l.status !== "ended"; })[0] || null; };
	var later = function (fn, ms) { window.setTimeout(fn, ms || 350); };
	/* a stop on one of the app's long pages: bring the part the stop is about right under the bar (found on a phone on the live
	   page, 1.72.735: the documents, the tax estimate and the properties sat below the first screen). One scroll on a press;
	   no wheel or touch is captured. */
	var seat = function (pick, ms) {
		later(function () {
			var e = typeof pick === "function" ? pick() : document.querySelector(pick);
			if (!e) { return; }
			var y = e.getBoundingClientRect().top + window.pageYOffset - bar.getBoundingClientRect().bottom - 10;
			var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
			window.scrollTo({ top: Math.max(0, y), behavior: calm ? "auto" : "smooth" });
		}, ms || 450);
	};
	var taxBox = function () { var x = document.getElementById("nlrm-tax"); return x && (x.closest(".nlrm-card") || x); };
	var stops = [];
	function build() {
		var d = D();
		if (!d.units.some(function (u) { return +u.id === U; })) { U = 21; }
		var L = leaseOf(U) || leaseOf(21), LU = L ? +L.unit_id : U;
		var ten = L && L.parties && (L.parties.tenants || [])[0];
		var linked = (d.leases || []).filter(function (l) { return l.linkage && l.linkage.mode === "cpi"; })[0];
		var tick = (d.tickets || []).filter(function (x) { return +x.unit_id === LU && x.status !== "done"; })[0] || (d.tickets || []).filter(function (x) { return x.status !== "done"; })[0];
		stops = [
			{ t: T("הדירה: מה מחכה היום", "The apartment: what is waiting today"), go: function () { closeAll(); hash("#/today/" + U); } },
			ten ? { t: T("השוכר", "The tenant"), go: function () { hash("#/today/" + LU); later(function () { N.open("contact", ten); }); } } : null,
			L ? { t: T("שכר דירה ותשלומים", "Rent and payments"), go: function () { closeAll(); hash("#/rent/" + LU); } } : null,
			linked ? { t: T("עדכון מדד", "The index update"), go: function () { closeAll(); hash("#/rent/" + linked.unit_id); later(function () { var b = document.querySelector('#nt2 [data-act="index"]'); if (b) { b.scrollIntoView({ block: "center" }); b.click(); } }, 700); } } : null,
			L ? { t: T("החוזה והביטחונות", "The lease and its securities"), go: function () { closeAll(); hash("#/today/" + LU); later(function () { N.open("unit", LU); later(function () { var tb = document.querySelector('.nlrm-layer [data-tab="lease"]'); if (tb) { tb.click(); } }, 250); }); } } : null,
			tick ? { t: T("תיקונים", "Repairs"), go: function () { closeAll(); hash("#/repairs"); later(function () { N.open("ticket", tick.id); }); } } : null,
			{ t: T("מסמכים", "Documents"), go: function () { closeAll(); hash("#/docs"); seat(".nlrm-main"); } },
			{ t: T("אומדן מס על שכר הדירה", "The rent tax estimate"), go: function () { closeAll(); if (N.state) { N.state.mtab = "tax"; } hash("#/money"); seat(taxBox, 600); } },
			{ t: T("כל הנכסים: המפה והבניין", "All properties: the map and the building"), go: function () { closeAll(); hash("#/properties"); seat(".nlrm-main"); } },
			{ t: T("להתחיל עם הדירה שלי", "Start with my own apartment"), last: true, go: function () { closeAll(); hash("#/properties"); seat(".nlrm-top"); } }
		].filter(Boolean);
	}
	function draw() {
		var s = stops[at], row = bar.querySelector(".nlrm-tour-row");
		if (!row) {
			row = document.createElement("div"); row.className = "nlrm-tour-row"; bar.appendChild(row);
		}
		row.innerHTML = '<button type="button" class="nlrm-tour-b" data-tour="prev"' + (at === 0 ? " disabled" : "") + ' aria-label="' + esc(T("הקודם", "Previous")) + '">' + esc(T("הקודם", "Back")) + "</button>" +
			'<span class="nlrm-tour-t" aria-live="polite"><small>' + (at + 1) + " / " + stops.length + "</small><b>" + esc(s.t) + "</b></span>" +
			'<span class="nlrm-tour-dots" role="group" aria-label="' + esc(T("תחנות הסיור", "Tour stops")) + '">' + stops.map(function (x, i) { return '<button type="button" data-tour-at="' + i + '" class="' + (i === at ? "is-on" : "") + '" aria-label="' + esc(x.t) + '" title="' + esc(x.t) + '">' + (i + 1) + "</button>"; }).join("") + "</span>" +
			(s.last ? '<a class="nlrm-tour-b is-next nlrm-tour-go" style="justify-self:auto" href="' + esc(bar.dataset.go || "#") + '">' + esc(T("להירשם ולהתחיל", "Sign up and start")) + "</a>" : '<button type="button" class="nlrm-tour-b is-next" data-tour="next">' + esc(T("הבא", "Next")) + "</button>");
		document.body.style.paddingTop = bar.offsetHeight + "px";
		document.documentElement.style.scrollPaddingTop = (bar.offsetHeight + 8) + "px";
		document.documentElement.style.setProperty("--nlrm-tour-h", Math.round(bar.getBoundingClientRect().bottom) + "px");
		document.documentElement.classList.add("nlrm-touring");
	}
	function goTo(i) {
		at = Math.max(0, Math.min(stops.length - 1, i));
		draw();
		try { stops[at].go(); } catch (e) { if (window.console) { console.warn("tour", e && e.message); } }
		if (!/^#\/(today|rent)/.test(location.hash)) { later(function () { var r = document.getElementById("nlrm-root"); if (r && r.getBoundingClientRect().top < bar.offsetHeight) { window.scrollTo({ top: Math.max(0, r.getBoundingClientRect().top + window.scrollY - bar.offsetHeight - 8) }); } }, 200); }
	}
	bar.addEventListener("click", function (e) {
		var b = e.target.closest ? e.target.closest("[data-tour],[data-tour-at]") : null;
		if (!b || !ready) { return; }
		if (b.hasAttribute("data-tour-at")) { goTo(+b.getAttribute("data-tour-at")); return; }
		goTo(at + (b.getAttribute("data-tour") === "next" ? 1 : -1));
	});
	window.addEventListener("resize", function () { if (ready) { document.body.style.paddingTop = bar.offsetHeight + "px"; } });
	var tries = 0, wait = window.setInterval(function () {
		if (D() && N.ix && N.ix.unit && D().units && D().units.length) {
			window.clearInterval(wait); ready = true; build();
			/* the address may already name a screen (the opening's "enter the apartment" link): keep it, the tour starts at stop 1 */
			draw();
			if (!/^#\/(today|rent)\//.test(location.hash)) { stops[0].go(); }
			window.NLRMTour = { goTo: goTo, stops: function () { return stops.map(function (x) { return x.t; }); }, at: function () { return at; } };
		} else if (++tries > 200) { window.clearInterval(wait); }
	}, 100);
})();
