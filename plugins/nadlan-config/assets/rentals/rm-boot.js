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
	var base = { lang: cfg.lang, strings: strings, msg: msg, mapbox: cfg.mapbox, urls: cfg.urls, langUrls: cfg.langUrls, me: me, assets: cfg.assets, ver: cfg.ver };
	if (cfg.mode === "app") {
		var adapter = N.RestAdapter(cfg.rest, cfg.nonce);
		base.adapter = adapter;
		base.inPlaceLang = false;
		base.saveMe = function (m) {
			return fetch(cfg.rest + "/rm/me", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-WP-Nonce": cfg.nonce }, body: JSON.stringify({ display: m.display, phone: m.phone, pay: m.pay, notify: m.notify !== false, lang: N.lang === "he" ? "he" : "en" }) }).then(function (r) { if (!r.ok) { throw new Error(N.t("err_generic")); } return r.json(); });
		};
		adapter.erase = function () { return fetch(cfg.rest + "/rm/erase", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-WP-Nonce": cfg.nonce }, body: JSON.stringify({ confirm: "ERASE" }) }); };
		N.mount(root, base);
	} else {
		base.adapter = N.DemoAdapter(cfg.lang || "he");
		base.inPlaceLang = true;
		base.me = { display: cfg.lang === "en" ? "Dan Cohen" : "דני כהן", phone: "972500000999", pay: { bit: "972500000999" } };
		N.mount(root, base);
	}
})();
