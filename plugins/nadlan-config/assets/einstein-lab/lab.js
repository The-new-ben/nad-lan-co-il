/* Einstein showroom lab runtime - scoped to body.nlx-einstein-lab.
 * Two jobs, both outside the frozen engine:
 * 1. A tap on a floor pill must not throw the page - if anything scrolls the
 *    viewport away right after the tap, we put it back (mobile only; the
 *    theater is full-height there so the answer is already on screen).
 * 2. The unit-screen tool doors get the approved renders as image tiles.
 *    URLs are baked at deploy time; decoration is idempotent. */
(function () {
	"use strict";
	if (!document.body || !document.body.classList.contains("nlx-einstein-lab")) return;

	var TILE_IMAGES = {
		view: "https://nad-lan.co.il/wp-content/uploads/2026/08/einstein-tile-view.webp",
		tour: "https://nad-lan.co.il/wp-content/uploads/2026/08/einstein-tile-tour.webp",
		studio: "https://nad-lan.co.il/wp-content/uploads/2026/08/einstein-tile-studio.webp",
		plan: "https://nad-lan.co.il/wp-content/uploads/2026/08/einstein-tile-plan.webp"
	};

	/* ---- scroll-jump suppressor (mobile) ---- */
	var mobile = window.matchMedia("(max-width: 820px)");
	var holdY = null;
	var holdUntil = 0;
	document.addEventListener("pointerdown", function (e) {
		if (!mobile.matches) return;
		var pill = e.target.closest && e.target.closest("button.nl-hot, .nl-hot");
		if (!pill) return;
		holdY = window.scrollY;
		holdUntil = performance.now() + 900;
	}, { passive: true, capture: true });
	window.addEventListener("scroll", function () {
		if (holdY == null || performance.now() > holdUntil) return;
		if (Math.abs(window.scrollY - holdY) > 80) {
			var y = holdY;
			window.requestAnimationFrame(function () { window.scrollTo(0, y); });
		}
	}, { passive: true });

	/* ---- door tiles ---- */
	function decorate(root) {
		(root || document).querySelectorAll(".nl-unit-door").forEach(function (door) {
			if (door.dataset.nlxTiled) return;
			var tool = door.dataset.tool || "";
			var img = TILE_IMAGES[tool] || "";
			if (img && img.indexOf("http") === 0) {
				door.style.backgroundImage = "url('" + img + "')";
				door.classList.add("nlx-tile");
			}
			door.dataset.nlxTiled = "1";
		});
	}
	var screenEl = document.getElementById("nl-unit-screen");
	if (screenEl) {
		new MutationObserver(function () { decorate(screenEl); }).observe(screenEl, { childList: true, subtree: true, attributes: true, attributeFilter: ["hidden"] });
	}
	decorate(document);
})();
