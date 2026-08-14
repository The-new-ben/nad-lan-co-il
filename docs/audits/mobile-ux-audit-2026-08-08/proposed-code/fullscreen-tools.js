/*
 * NADLAN BODY-LEVEL FULLSCREEN TOOLS
 * PROPOSAL ONLY / NOT APPLIED
 *
 * Source fragment for the existing engine.js IIFE. Load/paste after
 * engine-selected-unit.js. WordPress, not this code, owns the Mapbox enqueue.
 */

var unitTool = {
  dialog: null,
  cleanup: null,
  returnFocus: null,
  historyMarker: null,
  pendingFocusRestore: true
};

function ensureUnitToolDialog() {
  if (unitTool.dialog) return unitTool.dialog;

  var dialog = document.createElement("dialog");
  dialog.id = "nl-unit-tool";
  dialog.className = "nl-unit-tool";
  document.body.appendChild(dialog);

  dialog.addEventListener("cancel", function (event) {
    event.preventDefault();
    closeUnitTool(true, false);
  });

  dialog.addEventListener("click", function (event) {
    var button = event.target.closest('[data-act="unit-tool-back"]');
    if (button) closeUnitTool(true, false);
  });

  unitTool.dialog = dialog;
  return dialog;
}

function toolTitle(kind) {
  if (kind === "plan") return t("tab_plan");
  if (kind === "view") return t("tab_view");
  if (kind === "tour") return t("tab_tour");
  return t("unit_selected");
}

function unitToolMarkup(kind, u) {
  var content = "";

  if (kind === "plan") {
    var plan = safeHttpUrl(u.plan);
    content = plan
      ? '<figure class="nl-unit-tool__plan">' +
          '<img src="' + esc(plan) + '" alt="' + esc(t("tab_plan")) + '">' +
        '</figure>'
      : '<p class="nl-unit-tool__empty">' + esc(t("plan_coming")) + '</p>';
  }

  if (kind === "view") {
    content =
      '<div class="nl-window-tool">' +
        '<div class="nl-window-tool__map" data-role="window-map" tabindex="0" ' +
          'aria-label="' + esc(t("tab_view")) + '"></div>' +
        '<p class="nl-window-tool__fallback" data-role="window-fallback" hidden></p>' +
        '<div class="nl-window-tool__controls">' +
          '<button type="button" data-turn="-30" aria-label="' +
            esc(t("winview_turn_left")) + '">↶</button>' +
          '<span>' + esc(t("floor_label", { n: u.floor })) +
            " · " + esc(dirLabel(u.dir)) + '</span>' +
          '<button type="button" data-turn="30" aria-label="' +
            esc(t("winview_turn_right")) + '">↷</button>' +
        '</div>' +
      '</div>';
  }

  if (kind === "tour") {
    var tour = safeHttpUrl(u.tour_url || project().tour_url);

    content = tour
      ? '<div class="nl-unit-tool__tour">' +
          '<iframe src="' + esc(tour) + '" title="' + esc(t("tab_tour")) + '" ' +
            'allow="fullscreen; gyroscope; accelerometer" allowfullscreen></iframe>' +
          '<a href="' + esc(tour) + '" target="_blank" rel="noopener">' +
            esc(t("tour_open")) +
          '</a>' +
        '</div>'
      : fpMarkup(u);
  }

  return (
    '<div class="nl-unit-tool__frame">' +
      '<header class="nl-unit-tool__head">' +
        '<button type="button" data-act="unit-tool-back">' +
          esc(t("unit_tool_back")) +
        '</button>' +
        '<h2 id="nl-unit-tool-title">' + esc(toolTitle(kind)) + '</h2>' +
      '</header>' +
      '<div class="nl-unit-tool__body">' + content + '</div>' +
    '</div>'
  );
}

function openUnitTool(kind, u, trigger) {
  if (!u) return;

  /* The current Studio already owns a body-level overlay. Do not nest it. */
  if (kind === "studio") {
    openStudio(u.id);
    return;
  }

  if (kind !== "plan" && kind !== "view" && kind !== "tour") return;

  var dialog = ensureUnitToolDialog();

  /* Defensive only: normal UI cannot open a second tool while ROOT is inert. */
  if (state.tool) return;

  state.tool = kind;
  unitTool.returnFocus = trigger || document.activeElement;
  unitTool.pendingFocusRestore = true;

  dialog.setAttribute("dir", isRTL() ? "rtl" : "ltr");
  dialog.setAttribute("aria-labelledby", "nl-unit-tool-title");
  dialog.innerHTML = unitToolMarkup(kind, u);

  setInert(ROOT, true);
  document.documentElement.classList.add("nl-unit-tool-open");
  document.body.classList.add("nl-unit-tool-open");

  if (typeof dialog.showModal === "function") dialog.showModal();
  else dialog.setAttribute("open", "");

  if (kind === "view") {
    unitTool.cleanup = mountWindowViewport(dialog, u);
  } else if (kind === "tour" && !(u.tour_url || project().tour_url)) {
    fpInit();
  }

  unitTool.historyMarker = "nl-unit-tool-" + Date.now().toString(36);

  history.pushState(
    Object.assign({}, history.state || {}, {
      nlUnitTool: unitTool.historyMarker
    }),
    "",
    location.href
  );

  requestAnimationFrame(function () {
    var back = dialog.querySelector('[data-act="unit-tool-back"]');
    if (back) back.focus({ preventScroll: true });
  });
}

/*
 * UI close first walks back across the synthetic tool history entry. The
 * popstate handler performs teardown. fromHistory=true is reserved for the
 * popstate path and controlled sandbox teardown.
 */
function closeUnitTool(restoreFocus, fromHistory) {
  if (!state.tool) return;

  unitTool.pendingFocusRestore = restoreFocus !== false;

  if (
    !fromHistory &&
    unitTool.historyMarker &&
    history.state &&
    history.state.nlUnitTool === unitTool.historyMarker
  ) {
    history.back();
    return;
  }

  finishUnitToolClose(unitTool.pendingFocusRestore);
}

function finishUnitToolClose(restoreFocus) {
  var dialog = unitTool.dialog;
  var returnFocus = unitTool.returnFocus;

  if (unitTool.cleanup) {
    try { unitTool.cleanup(); } catch (e) {}
  }

  unitTool.cleanup = null;
  unitTool.returnFocus = null;
  unitTool.historyMarker = null;
  state.tool = null;

  if (dialog) {
    if (dialog.open && typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
    dialog.innerHTML = "";
  }

  setInert(ROOT, false);
  document.documentElement.classList.remove("nl-unit-tool-open");
  document.body.classList.remove("nl-unit-tool-open");

  if (restoreFocus && returnFocus && document.contains(returnFocus)) {
    requestAnimationFrame(function () {
      returnFocus.focus({ preventScroll: true });
    });
  }
}

window.addEventListener("popstate", function () {
  if (state.tool) finishUnitToolClose(unitTool.pendingFocusRestore);
});

function mountWindowViewport(scope, u) {
  var host = scope.querySelector('[data-role="window-map"]');
  var fallback = scope.querySelector('[data-role="window-fallback"]');
  var geo = preciseGeo();

  if (!host) return function () {};

  if (!geo.ok || !SR.config.mapbox_token || !window.mapboxgl) {
    host.hidden = true;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = t("unit_map_unverified");
    }
    return function () {};
  }

  var controller = new AbortController();
  var signal = controller.signal;
  var dragging = false;
  var lastX = 0;
  var lastY = 0;
  var bearing = unitBearing(u);
  var vertical = 0;
  var map = null;

  function applyCamera() {
    if (map) winCam(map, u, bearing, vertical);
  }

  function turn(delta) {
    bearing = (bearing + delta + 360) % 360;
    applyCamera();
  }

  try {
    window.mapboxgl.accessToken = SR.config.mapbox_token;

    map = new window.mapboxgl.Map({
      container: host,
      style: "mapbox://styles/mapbox/satellite-streets-v12",
      center: [geo.lng, geo.lat],
      zoom: 16.5,
      pitch: 70,
      bearing: bearing,
      maxPitch: 85,
      interactive: false,
      attributionControl: true
    });
  } catch (error) {
    host.hidden = true;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = t("unit_map_unverified");
    }
    controller.abort();
    return function () {};
  }

  map.once("load", function () {
    try {
      var layers = map.getStyle().layers;
      var labelLayer;

      for (var i = 0; i < layers.length; i++) {
        if (
          layers[i].type === "symbol" &&
          layers[i].layout &&
          layers[i].layout["text-field"]
        ) {
          labelLayer = layers[i].id;
          break;
        }
      }

      map.addLayer({
        id: "nl-unit-window-buildings",
        source: "composite",
        "source-layer": "building",
        filter: ["==", "extrude", "true"],
        type: "fill-extrusion",
        minzoom: 13,
        paint: {
          "fill-extrusion-color": "#d8d2c4",
          "fill-extrusion-height": ["get", "height"],
          "fill-extrusion-base": ["get", "min_height"],
          "fill-extrusion-opacity": 0.86
        }
      }, labelLayer);
    } catch (e) {}

    applyCamera();
  });

  map.once("error", function () {
    if (fallback && !fallback.textContent) {
      fallback.hidden = false;
      fallback.textContent = t("unit_map_unverified");
    }
  });

  host.addEventListener("pointerdown", function (event) {
    dragging = true;
    lastX = event.clientX;
    lastY = event.clientY;
    host.setPointerCapture(event.pointerId);
    event.preventDefault();
  }, { signal: signal });

  host.addEventListener("pointermove", function (event) {
    if (!dragging) return;

    bearing = (bearing + (event.clientX - lastX) * 0.35 + 360) % 360;
    vertical = Math.max(
      -45,
      Math.min(10, vertical - (event.clientY - lastY) * 0.22)
    );

    lastX = event.clientX;
    lastY = event.clientY;
    applyCamera();
    event.preventDefault();
  }, { signal: signal });

  host.addEventListener("pointerup", function (event) {
    dragging = false;
    try { host.releasePointerCapture(event.pointerId); } catch (e) {}
  }, { signal: signal });

  host.addEventListener("pointercancel", function () {
    dragging = false;
  }, { signal: signal });

  host.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      turn(isRTL() ? 15 : -15);
    }

    if (event.key === "ArrowRight") {
      event.preventDefault();
      turn(isRTL() ? -15 : 15);
    }
  }, { signal: signal });

  scope.querySelectorAll("[data-turn]").forEach(function (button) {
    button.addEventListener("click", function () {
      turn(parseInt(button.dataset.turn, 10) || 0);
    }, { signal: signal });
  });

  return function () {
    controller.abort();
    if (map) {
      try { map.remove(); } catch (e) {}
    }
    map = null;
  };
}
