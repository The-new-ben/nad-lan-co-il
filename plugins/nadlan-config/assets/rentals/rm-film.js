/* The rentals tutorial film on /my-rentals/ (HAD-795, 23.11.2026). Nothing is requested before the press: the row carries only
   the poster; pressed, a <video> with the browser's own controls opens in place (no autoplay before the press, no full screen,
   no wheel or touch capture) and plays with sound. "Close" or Escape stops it and puts the row back. Captions are in the film. */
(function () {
  "use strict";
  var box = document.getElementById("nlrm-film");
  if (!box) { return; }
  var go = box.querySelector(".nlrm-film-go");
  var note = box.querySelector(".nlrm-film-n");
  var fig = null;
  var track = function (n, d) { try { if (window.nlTrack) { window.nlTrack(n, d || {}); } } catch (e) { /* the tracker never breaks the page */ } };
  var close = function () {
    if (!fig) { return; }
    var v = fig.querySelector("video");
    try { v.pause(); v.removeAttribute("src"); v.load(); } catch (e) { /* nothing */ }
    fig.parentNode.removeChild(fig); fig = null;
    go.hidden = false; if (note) { note.hidden = false; }
    go.focus();
  };
  go.addEventListener("click", function () {
    if (fig) { return; }
    fig = document.createElement("figure");
    fig.className = "nlrm-film-p";
    var v = document.createElement("video");
    v.controls = true; v.playsInline = true; v.preload = "auto";
    v.setAttribute("playsinline", ""); v.setAttribute("poster", box.getAttribute("data-poster"));
    v.src = box.getAttribute("data-src");
    var x = document.createElement("button");
    x.type = "button"; x.className = "nlrm-film-x"; x.setAttribute("aria-label", box.getAttribute("data-close")); x.textContent = "×";
    x.addEventListener("click", close);
    fig.appendChild(v); fig.appendChild(x);
    go.hidden = true; if (note) { note.hidden = true; }
    box.insertBefore(fig, go);
    var p = v.play(); if (p && p.catch) { p.catch(function () { /* the controls stay; the visitor presses play */ }); }
    v.focus();
    track("rentals_film_play", { lang: box.getAttribute("data-lang") });
  });
  box.addEventListener("keydown", function (e) { if (e.key === "Escape" && fig) { close(); } });
})();
