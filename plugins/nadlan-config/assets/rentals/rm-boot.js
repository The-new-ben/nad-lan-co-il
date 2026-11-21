/* NADLAN RENTALS v2 - boot (HAD-383): a personal link wins, then the landlord's app, then the sample. */
(function () {
	"use strict";
	var N = window.NLRM, root = document.getElementById("nlrm-root");
	if (!N || !root) { return; }
	var read = function (id) { var el = document.getElementById(id); try { return el ? JSON.parse(el.textContent) : null; } catch (e) { return null; } };
	var cfg = read("nlrm-cfg") || {}, i18n = read("nlrm-i18n") || {}, lease = read("nlrm-lease");
	N.LEASE = lease;
	N.TRIAGE = cfg.triage || null;
	var strings = {}, msg = {};
	Object.keys(i18n).forEach(function (l) { if (i18n[l] && i18n[l].ui) { strings[l] = i18n[l].ui; msg[l] = i18n[l].msg; } });
	N.setStrings(cfg.lang || "he", strings[cfg.lang] || strings.he);
	var link = N.portalToken ? N.portalToken() : null;
	if (link) {
		/* the link page replaces the landing on this visit */
		var page = document.querySelector(".nlrm-page");
		if (page) { page.querySelectorAll(".nlrm-hero,.nlrm-faq,.nlrm-legal,.nlrm-sample > h2,.nlrm-sample > p,.nlrm-h1").forEach(function (x) { x.hidden = true; }); }
		N.mountPortal(root, { rest: cfg.rest, lang: cfg.lang, strings: strings, msg: msg }, link);
		return;
	}
	var me = cfg.me || {};
	var base = { lang: cfg.lang, strings: strings, msg: msg, mapbox: cfg.mapbox, urls: cfg.urls, langUrls: cfg.langUrls, me: me, assets: cfg.assets, ver: cfg.ver, brand: cfg.brand || "", leaseMaker: !!cfg.leaseMaker };
	if (cfg.mode === "app") {
		var adapter = N.RestAdapter(cfg.rest, cfg.nonce);
		base.adapter = adapter;
		if (N.mountToday) { N.mountToday(root, { rest: cfg.rest, nonce: cfg.nonce, urls: cfg.urls, today2: cfg.today2 }); }
		base.inPlaceLang = false;
		base.saveMe = function (m) {
			return fetch(cfg.rest + "/rm/me", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-WP-Nonce": cfg.nonce }, body: JSON.stringify({ display: m.display, phone: m.phone, pay: m.pay, notify: m.notify !== false, lang: N.lang === "he" ? "he" : "en" }) }).then(function (r) { if (!r.ok) { throw new Error(N.t("err_generic")); } return r.json(); });
		};
		/* buyer events (names agreed with HAD-791): a landlord's first visit with nothing in his account, and his first property */
		var track = function (n) { try { if (window.nlTrack) { window.nlTrack(n, {}); } } catch (e) { /* the tracker never breaks the app */ } };
		var save0 = adapter.save;
		adapter.save = function (entity, data) {
			var first = entity === "property" && !(data && data.id) && N.store && N.store.d && !(N.store.d.properties || []).length;
			return save0.apply(adapter, arguments).then(function (r) { if (first) { track("rent_property_add"); } return r; });
		};
		var seen = 0, wait = window.setInterval(function () {
			if (N.store && N.store.d && N.store.d.properties) {
				window.clearInterval(wait);
				try { if (!N.store.d.demo && !N.store.d.properties.length && !window.localStorage.getItem("nlrm-signup")) { window.localStorage.setItem("nlrm-signup", "1"); track("rent_signup"); } } catch (e) { /* private mode */ }
			} else if (++seen > 100) { window.clearInterval(wait); }
		}, 200);
		adapter.erase = function () { return fetch(cfg.rest + "/rm/erase", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-WP-Nonce": cfg.nonce }, body: JSON.stringify({ confirm: "ERASE" }) }); };
		N.mount(root, base);
	} else {
		base.adapter = N.DemoAdapter(cfg.lang || "he");
		/* the sample shows the same day screen a landlord gets (the tour of /my-rentals/, 1.72.734) */
		if (N.mountToday && cfg.today2) { N.mountToday(root, { urls: cfg.urls, today2: true }); }
		base.inPlaceLang = true;
		base.me = { display: cfg.lang === "en" ? "Dan Cohen (example)" : "דני כהן (דוגמה)", phone: "", pay: {} };
		N.mount(root, base);
	}
})();
