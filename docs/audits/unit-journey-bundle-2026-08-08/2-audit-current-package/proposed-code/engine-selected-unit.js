/*
 * NADLAN SELECTED-UNIT SURFACE
 * PROPOSAL ONLY / NOT APPLIED
 *
 * This is a source fragment for the existing engine.js IIFE. It is not a
 * standalone bundle. Insert it only after the engine helpers and DIR_BEARING
 * exist. See integration-diff-guide.md before attempting a sandbox merge.
 */

/* Add `tool: null` to the existing state object. */
var UNIT_MQ = window.matchMedia(
  "(max-width:700px), " +
  "(max-width:900px) and (max-height:500px) and (pointer:coarse)"
);

var unitSurface = {
  source: null,
  beamMap: null,
  beamHost: null
};

function setInert(el, on) {
  if (!el) return;
  if ("inert" in el) el.inert = !!on;
  if (on) el.setAttribute("aria-hidden", "true");
  else el.removeAttribute("aria-hidden");
}

function preciseGeo() {
  var g = project().geo || {};
  var lat = Number(g.lat);
  var lng = Number(g.lng);

  return {
    ok: isFinite(lat) && isFinite(lng) && g.confidence !== "city",
    lat: lat,
    lng: lng
  };
}

function unitBearing(u) {
  var key = dirKey(u.dir);
  return key && Object.prototype.hasOwnProperty.call(DIR_BEARING, key)
    ? DIR_BEARING[key]
    : 0;
}

function beamPoint(bearing, radius) {
  var rad = bearing * Math.PI / 180;
  return {
    x: 50 + Math.sin(rad) * radius,
    y: 50 - Math.cos(rad) * radius
  };
}

function beamPath(bearing) {
  var left = beamPoint(bearing - 24, 44);
  var tip = beamPoint(bearing, 53);
  var right = beamPoint(bearing + 24, 44);

  return [
    "M 50 50",
    "L " + left.x.toFixed(2) + " " + left.y.toFixed(2),
    "Q " + tip.x.toFixed(2) + " " + tip.y.toFixed(2) +
      " " + right.x.toFixed(2) + " " + right.y.toFixed(2),
    "Z"
  ].join(" ");
}

function renderBeamScene(u) {
  var view = viewText(u) || dirLabel(u.dir);
  var bearing = unitBearing(u);

  return (
    '<figure class="nl-unit-beam" data-bearing="' + bearing + '">' +
      '<div class="nl-unit-beam__map" data-role="beam-map" ' +
        'role="img" aria-label="' +
        esc(t("unit_beam_title", { view: view })) + '"></div>' +
      '<svg class="nl-unit-beam__svg" viewBox="0 0 100 100" ' +
        'preserveAspectRatio="none" aria-hidden="true">' +
        '<defs>' +
          '<linearGradient id="nl-unit-beam-gold" x1="0" y1="1" x2="0" y2="0">' +
            '<stop offset="0" stop-color="#c9a34f" stop-opacity=".86"/>' +
            '<stop offset="1" stop-color="#f4df9d" stop-opacity=".18"/>' +
          '</linearGradient>' +
        '</defs>' +
        '<path d="' + beamPath(bearing) + '" fill="url(#nl-unit-beam-gold)"/>' +
        '<circle cx="50" cy="50" r="4.2" fill="#1b1a17" ' +
          'stroke="#f3d98c" stroke-width="1.4"/>' +
      '</svg>' +
      '<figcaption>' +
        '<strong>' + esc(t("unit_beam_title", { view: view })) + '</strong>' +
        '<span>' + esc(t("unit_beam_note")) + '</span>' +
      '</figcaption>' +
    '</figure>'
  );
}

function destroyBeamMap() {
  if (unitSurface.beamMap) {
    try { unitSurface.beamMap.remove(); } catch (e) {}
  }

  unitSurface.beamMap = null;
  unitSurface.beamHost = null;
}

function mountBeamScene(scope) {
  destroyBeamMap();

  var host = scope && scope.querySelector('[data-role="beam-map"]');
  var geo = preciseGeo();
  var figure = host && host.closest(".nl-unit-beam");

  if (!host || !figure) return;

  /* A city centroid is suitable for an area map, not for a truthful window. */
  if (!geo.ok || !SR.config.mapbox_token || !window.mapboxgl) {
    figure.classList.add("is-schematic");
    return;
  }

  try {
    window.mapboxgl.accessToken = SR.config.mapbox_token;

    var map = new window.mapboxgl.Map({
      container: host,
      style: "mapbox://styles/mapbox/light-v11",
      center: [geo.lng, geo.lat],
      zoom: 15.4,
      pitch: 0,
      bearing: 0,
      interactive: false,
      attributionControl: true
    });

    unitSurface.beamMap = map;
    unitSurface.beamHost = host;

    map.once("load", function () {
      if (unitSurface.beamMap !== map) return;
      figure.classList.add("is-map-ready");
      try { map.resize(); } catch (e) {}
    });

    map.once("error", function () {
      if (unitSurface.beamMap === map) {
        figure.classList.add("is-schematic");
      }
    });
  } catch (e) {
    figure.classList.add("is-schematic");
  }
}

function unitFactsMarkup(u) {
  return (
    '<dl class="nl-unit-facts">' +
      '<div><dt>' + esc(t("panel_floor")) + '</dt><dd>' + esc(u.floor) + '</dd></div>' +
      '<div><dt>' + esc(t("panel_rooms")) + '</dt><dd>' + esc(u.rooms) + '</dd></div>' +
      '<div><dt>' + esc(t("panel_sqm")) + '</dt><dd>' +
        esc(u.sqm + " " + t("sqm_unit")) + '</dd></div>' +
      '<div><dt>' + esc(t("panel_balcony")) + '</dt><dd>' +
        esc(u.balcony ? u.balcony + " " + t("sqm_unit") : "–") +
      '</dd></div>' +
    '</dl>'
  );
}

function unitDoorsMarkup(u) {
  var view = viewText(u) || dirLabel(u.dir);

  return (
    '<nav class="nl-unit-doors" aria-label="' + esc(t("unit_tools_aria")) + '">' +
      '<button type="button" data-act="unit-tool" data-tool="plan">' +
        esc(t("unit_door_plan")) +
      '</button>' +
      '<button type="button" data-act="unit-tool" data-tool="view">' +
        esc(t("unit_door_view", { view: view })) +
      '</button>' +
      '<button type="button" data-act="unit-tool" data-tool="tour">' +
        esc(t("unit_door_tour")) +
      '</button>' +
      (SR.config.studio !== "off"
        ? '<button type="button" data-act="unit-tool" data-tool="studio">' +
            esc(t("unit_door_studio")) +
          '</button>'
        : "") +
    '</nav>'
  );
}

function unitQuickActionsMarkup(u) {
  var fav = state.favs.indexOf(u.id) >= 0;
  var cmp = state.compare.indexOf(u.id) >= 0;

  return (
    '<div class="nl-unit-quick" role="group" aria-label="' +
      esc(t("unit_quick_actions")) + '">' +
      '<button type="button" data-act="fav" data-id="' + esc(u.id) + '" ' +
        'aria-pressed="' + (fav ? "true" : "false") + '">' +
        esc(fav ? t("btn_saved") : t("btn_save")) +
      '</button>' +
      '<button type="button" data-act="compare" data-id="' + esc(u.id) + '" ' +
        'aria-pressed="' + (cmp ? "true" : "false") + '">' +
        esc(cmp ? t("btn_compared") : t("btn_compare")) +
      '</button>' +
      '<button type="button" data-act="share" data-id="' + esc(u.id) + '">' +
        esc(t("btn_share")) +
      '</button>' +
      '<a href="' + esc(waShareUrl(u)) + '" target="_blank" rel="noopener">' +
        esc(t("btn_wa_share")) +
      '</a>' +
    '</div>'
  );
}

function unitSummaryMarkup(u, mode) {
  return (
    '<div class="nl-unit-summary nl-unit-summary--' + esc(mode) + '">' +
      '<header class="nl-unit-summary__head">' +
        '<button class="nl-unit-summary__back" type="button" data-act="unit-back">' +
          esc(t("unit_back_building")) +
        '</button>' +
        '<div>' +
          '<span>' + esc(t("unit_selected")) + '</span>' +
          '<h3 id="nl-selected-unit-title">' +
            esc(roomsLabel(u.rooms) + " · " + u.label) +
          '</h3>' +
        '</div>' +
        '<span class="nl-unit-summary__status">' +
          esc(statusLabel(u.status)) +
        '</span>' +
      '</header>' +
      renderBeamScene(u) +
      unitFactsMarkup(u) +
      unitDoorsMarkup(u) +
      unitQuickActionsMarkup(u) +
      '<button class="nl-unit-offer" type="button" ' +
        'data-act="scroll" data-id="inquiry">' +
        esc(t("unit_offer")) +
      '</button>' +
    '</div>'
  );
}

function renderUnitScreen(u, options) {
  options = options || {};

  var mobile = UNIT_MQ.matches;
  var theaterEl = ROOT.querySelector(".nl-theater");
  var screen = document.getElementById("nl-unit-screen");
  var panelEl = document.getElementById("nl-panel");
  var panelBodyEl = document.getElementById("nl-panel-body");
  var host;

  if (!u || !theaterEl || !screen || !panelEl || !panelBodyEl) return;

  destroyBeamMap();

  if (mobile) {
    theaterEl.classList.add("nl-theater--unit-selected");

    screen.innerHTML = unitSummaryMarkup(u, "screen");
    screen.hidden = false;
    setInert(screen, false);

    panelEl.hidden = true;
    panelEl.classList.remove("is-open", "nl-panel--unit-summary");
    setInert(panelEl, true);

    host = screen;
  } else {
    theaterEl.classList.remove("nl-theater--unit-selected");

    screen.hidden = true;
    screen.innerHTML = "";
    setInert(screen, true);

    panelBodyEl.innerHTML = unitSummaryMarkup(u, "panel");
    panelEl.hidden = false;
    panelEl.classList.add("is-open", "nl-panel--unit-summary");
    setInert(panelEl, false);

    host = panelBodyEl;
  }

  mountBeamScene(host);

  if (mobile && options.scroll) {
    requestAnimationFrame(function () {
      theaterEl.scrollIntoView({
        block: "start",
        behavior: window.matchMedia("(prefers-reduced-motion:reduce)").matches
          ? "auto"
          : "smooth"
      });
    });
  }

  if (options.focus) {
    requestAnimationFrame(function () {
      var back = host.querySelector('[data-act="unit-back"]');
      if (back) back.focus({ preventScroll: true });
    });
  }
}

function clearUnitScreen() {
  var theaterEl = ROOT.querySelector(".nl-theater");
  var screen = document.getElementById("nl-unit-screen");
  var panelEl = document.getElementById("nl-panel");
  var panelBodyEl = document.getElementById("nl-panel-body");

  destroyBeamMap();

  if (theaterEl) theaterEl.classList.remove("nl-theater--unit-selected");

  if (screen) {
    screen.hidden = true;
    screen.innerHTML = "";
    setInert(screen, true);
  }

  if (panelEl) {
    panelEl.classList.remove("is-open", "nl-panel--unit-summary");
    panelEl.hidden = UNIT_MQ.matches;
    setInert(panelEl, true);
  }

  if (panelBodyEl) panelBodyEl.innerHTML = panelEmpty();
}

function syncUnitBreakpoint() {
  var selected = unit(state.unitId);
  if (selected) renderUnitScreen(selected, { focus: false, scroll: false });
  else clearUnitScreen();
}

if (UNIT_MQ.addEventListener) {
  UNIT_MQ.addEventListener("change", syncUnitBreakpoint);
} else {
  UNIT_MQ.addListener(syncUnitBreakpoint);
}

/*
 * Integration seam required in theater():
 *   '<section class="nl-unit-screen" id="nl-unit-screen" hidden></section>'
 * Place it as a sibling immediately after .nl-stagewrap and before the dock.
 *
 * selectUnit(), closePanel(), toggleFav() and toggleCompare() replacement
 * excerpts live in integration-diff-guide.md so this fragment remains focused
 * on one responsibility: rendering and owning the selected-unit surface.
 */
