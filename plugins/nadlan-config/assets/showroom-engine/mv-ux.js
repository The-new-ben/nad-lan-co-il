/**
 * mv-ux.js - shared 3D-viewer control layer (owner order 2026-07-13).
 *
 * Applies to EVERY <model-viewer> on the page:
 * 1. NO self-spinning: auto-rotate is stripped unless data-keep-spin is set.
 *    The model moves only when the user moves it.
 * 2. DETENTS: when the user releases a drag, the azimuth snaps to the nearest
 *    22.5deg step (16 compass points) - the "click" feel the owner asked for.
 *    Programmatic camera flights (unit selection, presets) are not affected.
 * 3. COMPASS: a small rose overlay shows where the camera looks relative to
 *    north. Convention (engine.js:1030): model -z axis = north, bearing =
 *    -theta. Override per model with data-north-deg.
 * 4. GUIDANCE: one non-interfering hint chip ("drag to rotate - locks to an
 *    angle"), fades on first interaction or after 7s. Engine stages (#nl-mv)
 *    get a second line about hotspots.
 */
(function () {
	"use strict";
	var LANG = (document.documentElement.lang || "he").slice(0, 2).toLowerCase();
	var T = {
		he: { drag: "גררו לסיבוב - המבט ננעל לזווית", hs: "לחצו על נקודה בבניין לפרטי דירה", n: "צ" },
		en: { drag: "Drag to rotate - the view locks to an angle", hs: "Tap a hotspot to open an apartment", n: "N" },
		fr: { drag: "Faites glisser pour pivoter - la vue se verrouille", hs: "Touchez un point pour ouvrir un appartement", n: "N" },
		ru: { drag: "Потяните для поворота - вид фиксируется", hs: "Нажмите на точку, чтобы открыть квартиру", n: "С" },
		ar: { drag: "اسحبوا للتدوير - يثبت العرض على زاوية", hs: "انقروا على نقطة لفتح شقة", n: "ش" }
	};
	var S = T[LANG] || T.he;
	var STEP = 22.5;

	function css() {
		if (document.getElementById("nlux-css")) { return; }
		var st = document.createElement("style");
		st.id = "nlux-css";
		st.textContent = ".nlux-compass{position:absolute;inset-inline-start:12px;bottom:12px;width:46px;height:46px;border-radius:50%;background:rgba(20,19,15,.72);border:1px solid rgba(230,212,174,.35);z-index:6;pointer-events:none;backdrop-filter:blur(3px)}" +
			".nlux-compass svg{width:100%;height:100%;display:block}" +
			".nlux-needle{transform-origin:50% 50%;transition:transform .2s cubic-bezier(.22,1,.36,1)}" +
			".nlux-hint{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);z-index:6;pointer-events:none;background:rgba(20,19,15,.72);color:#EFE7D6;font:600 11.5px/1.5 Heebo,sans-serif;border:1px solid rgba(230,212,174,.28);border-radius:999px;padding:7px 14px;white-space:nowrap;max-width:88%;overflow:hidden;text-overflow:ellipsis;opacity:1;transition:opacity .6s;backdrop-filter:blur(3px)}" +
			".nlux-hint.is-off{opacity:0}" +
			"@media(max-width:560px){.nlux-compass{width:38px;height:38px;bottom:10px}.nlux-hint{font-size:10.5px;padding:6px 11px;bottom:10px;max-width:74%}}";
		document.head.appendChild(st);
	}

	function compassSVG() {
		return '<svg viewBox="0 0 46 46" aria-hidden="true">' +
			'<circle cx="23" cy="23" r="20.5" fill="none" stroke="rgba(230,212,174,.28)" stroke-width="1"/>' +
			'<g class="nlux-needle"><path d="M23 7 L26.4 23 L23 20.4 L19.6 23 Z" fill="#C2563A"/><path d="M23 39 L19.6 23 L23 25.6 L26.4 23 Z" fill="rgba(239,231,214,.5)"/>' +
			'<text x="23" y="5.6" text-anchor="middle" font-size="6.5" font-weight="700" fill="#E6D4AE" font-family="Heebo,sans-serif">' + S.n + "</text></g></svg>";
	}

	function enhance(mv) {
		if (mv.dataset.nlux) { return; }
		mv.dataset.nlux = "1";
		if (!mv.hasAttribute("data-keep-spin")) {
			mv.removeAttribute("auto-rotate");
			mv.removeAttribute("auto-rotate-delay");
			mv.removeAttribute("rotation-per-second");
		}
		// no-tumble law: a building is viewed like a building - never from underneath.
		if (!mv.hasAttribute("min-camera-orbit")) { mv.setAttribute("min-camera-orbit", "-Infinity 48deg auto"); }
		if (!mv.hasAttribute("max-camera-orbit")) { mv.setAttribute("max-camera-orbit", "Infinity 88deg auto"); }
		if (!mv.hasAttribute("camera-controls")) { return; } // display-only: stop after de-spin
		var wrap = mv.parentElement || mv;
		if (getComputedStyle(wrap).position === "static") { wrap.style.position = "relative"; }
		css();

		// compass rose - tracks every camera move, programmatic or manual
		var comp = document.createElement("div");
		comp.className = "nlux-compass";
		comp.innerHTML = compassSVG();
		wrap.appendChild(comp);
		var needle = comp.querySelector(".nlux-needle");
		var north = parseFloat(mv.dataset.northDeg || "0") || 0;
		function updCompass() {
			try {
				var th = mv.getCameraOrbit().theta * 180 / Math.PI;
				needle.style.transform = "rotate(" + (-th + north) + "deg)"; // bearing = -theta (model -z = north)
			} catch (e) {}
		}
		mv.addEventListener("camera-change", updCompass);
		updCompass();

		// detents: after the user releases, snap azimuth to the nearest step
		var dragging = false;
		mv.addEventListener("pointerdown", function () { dragging = true; }, { passive: true });
		function release() {
			if (!dragging) { return; }
			dragging = false;
			setTimeout(function () {
				try {
					var o = mv.getCameraOrbit();
					var deg = o.theta * 180 / Math.PI;
					var snap = Math.round(deg / STEP) * STEP;
					if (Math.abs(snap - deg) > 0.4) {
						mv.cameraOrbit = snap + "deg " + (o.phi * 180 / Math.PI).toFixed(2) + "deg " + o.radius.toFixed(2) + "m";
					}
				} catch (e) {}
			}, 140);
		}
		window.addEventListener("pointerup", release, { passive: true });
		window.addEventListener("pointercancel", release, { passive: true });

		// one quiet hint line; engine stage gets the hotspot line appended
		var hint = document.createElement("div");
		hint.className = "nlux-hint";
		hint.textContent = S.drag + ("nl-mv" === mv.id ? " · " + S.hs : "");
		wrap.appendChild(hint);
		var kill = function () {
			hint.classList.add("is-off");
			setTimeout(function () { if (hint.parentNode) { hint.parentNode.removeChild(hint); } }, 800);
		};
		mv.addEventListener("pointerdown", kill, { once: true, passive: true });
		setTimeout(kill, 7000);
	}

	function scan(root) {
		(root || document).querySelectorAll("model-viewer").forEach(enhance);
	}
	if ("loading" === document.readyState) {
		document.addEventListener("DOMContentLoaded", function () { scan(); });
	} else { scan(); }
	// engine re-renders and lazy bands mount viewers later
	new MutationObserver(function (muts) {
		for (var i = 0; i < muts.length; i++) {
			for (var j = 0; j < muts[i].addedNodes.length; j++) {
				var n = muts[i].addedNodes[j];
				if (1 !== n.nodeType) { continue; }
				if ("MODEL-VIEWER" === n.tagName) { enhance(n); }
				else if (n.querySelectorAll) { scan(n); }
			}
		}
	}).observe(document.documentElement, { childList: true, subtree: true });
})();
