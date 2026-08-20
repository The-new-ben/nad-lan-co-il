/* Unit-scene bottom sheet controller (owner UX order 20.8.2026).
 * Around-engine layer: watches the frozen engine's v2 mobile scene and turns
 * it into a two-detent bottom sheet (peek / full). Re-applies itself after
 * every engine re-render (floor switching keeps the current detent, so
 * comparing floors never closes the card). No engine.js internals touched. */
(function () {
  "use strict";
  var MQ = window.matchMedia("(max-width: 900px) and (orientation: portrait)");
  var state = { detent: "peek" };

  function theater() {
    return document.querySelector(".nl-theater.nl-theater--unit-v2-mobile");
  }

  function sheet(th) {
    return th ? th.querySelector(".nl-unit-screen--v2") : null;
  }

  function setDetent(th, detent) {
    state.detent = detent === "full" ? "full" : "peek";
    th.classList.toggle("nl-usheet-full", state.detent === "full");
    var g = th.querySelector(".nl-usheet-grab");
    if (g) {
      g.setAttribute("aria-expanded", state.detent === "full" ? "true" : "false");
    }
  }

  function ensure() {
    var th = theater();
    if (!th || !MQ.matches) { return; }
    var sc = sheet(th);
    if (!sc) { return; }
    th.classList.add("nl-usheet-on");
    th.classList.toggle("nl-usheet-full", state.detent === "full");
    if (!sc.querySelector(".nl-usheet-grab")) {
      var g = document.createElement("button");
      g.type = "button";
      g.className = "nl-usheet-grab";
      g.setAttribute("aria-label", "הרחבה וכיווץ של כרטיס הדירה");
      g.setAttribute("aria-expanded", state.detent === "full" ? "true" : "false");
      g.innerHTML = "<i></i>";
      g.addEventListener("click", function () {
        setDetent(th, th.classList.contains("nl-usheet-full") ? "peek" : "full");
      });
      g.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          g.click();
        }
      });
      wireDrag(g, sc, th);
      sc.insertBefore(g, sc.firstChild);
    }
  }

  function wireDrag(grab, sc, th) {
    var y0 = null, scroll0 = 0;
    function start(e) {
      y0 = (e.touches ? e.touches[0] : e).clientY;
      scroll0 = sc.scrollTop || 0;
    }
    function end(e) {
      if (y0 == null) { return; }
      var y1 = (e.changedTouches ? e.changedTouches[0] : e).clientY;
      var dy = y1 - y0;
      y0 = null;
      var t2 = theater();
      if (!t2) { return; }
      if (dy < -45) { setDetent(t2, "full"); }
      else if (dy > 45 && scroll0 <= 0) { setDetent(t2, "peek"); }
    }
    grab.addEventListener("touchstart", start, { passive: true });
    grab.addEventListener("touchend", end, { passive: true });
    grab.addEventListener("mousedown", start);
    grab.addEventListener("mouseup", end);
    /* drag anywhere on the sheet header strip too */
    sc.addEventListener("touchstart", function (e) {
      if (e.target.closest("button, a, input, [data-act]") &&
          !e.target.closest(".nl-usheet-grab")) { return; }
      start(e);
    }, { passive: true });
    sc.addEventListener("touchend", function (e) {
      if (e.target.closest("button, a, input, [data-act]") &&
          !e.target.closest(".nl-usheet-grab")) { y0 = null; return; }
      end(e);
    }, { passive: true });
  }

  function off() {
    var th = document.querySelector(".nl-usheet-on");
    if (th && !MQ.matches) {
      th.classList.remove("nl-usheet-on", "nl-usheet-full");
    }
  }

  var pending = false;
  function schedule() {
    if (pending) { return; }
    pending = true;
    requestAnimationFrame(function () {
      pending = false;
      ensure();
      off();
    });
  }

  function boot() {
    var root = document.getElementById("nl-root");
    if (!root) { return; }
    new MutationObserver(schedule).observe(root, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ["class", "data-mode", "hidden"],
    });
    if (MQ.addEventListener) { MQ.addEventListener("change", schedule); }
    schedule();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
