/*
 * UTOPIA Sde Dov - isolated showroom runtime.
 *
 * It consumes only #utopia-showroom-data, writes only inside #utopia-showroom
 * and never touches the shared showroom, Studio or project-map globals.
 */
(function () {
  "use strict";

  var root = document.getElementById("utopia-showroom");
  var dataNode = document.getElementById("utopia-showroom-data");
  if (!root || !dataNode) return;

  var data;
  try {
    data = JSON.parse(dataNode.textContent || "{}");
  } catch (_) {
    return;
  }
  if (!data || !data.project || !Array.isArray(data.buildings) || !Array.isArray(data.sample_plans)) return;

  var copy = data.copy || {};
  var state = {
    buildingId: "",
    planId: "",
    referenceId: "",
    reference: null,
    view: "model",
    map: null,
    mapGroups: {},
    mapVisible: {},
    projectPopup: null,
    fallbackFullscreen: false,
    cinematicTimers: []
  };

  var buildings = {};
  var plans = {};
  data.buildings.forEach(function (building) { buildings[building.id] = building; });
  data.sample_plans.forEach(function (plan) { plans[plan.id] = plan; });

  function one(selector, scope) {
    return (scope || root).querySelector(selector);
  }
  function all(selector, scope) {
    return Array.prototype.slice.call((scope || root).querySelectorAll(selector));
  }
  function safeUrl(value) {
    try {
      var parsed = new URL(String(value || ""), location.href);
      return parsed.protocol === "https:" || parsed.protocol === "http:" ? parsed.href : "";
    } catch (_) {
      return "";
    }
  }
  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[ch];
    });
  }
  function formatNumber(value) {
    try {
      return new Intl.NumberFormat(data.lang || "he", { maximumFractionDigits: 2 }).format(Number(value));
    } catch (_) {
      return String(value);
    }
  }
  function clearCinematic() {
    state.cinematicTimers.forEach(function (timer) { clearTimeout(timer); });
    state.cinematicTimers = [];
  }

  function updateFormContext() {
    var context = one("[data-utopia-form-context]");
    if (!context) return;
    if (!state.reference || !state.planId) {
      context.textContent = copy.no_selection || "";
      return;
    }
    var plan = plans[state.planId];
    context.textContent =
      (copy.selected_prefix || "") + " " +
      (plan ? plan.building.toUpperCase() + " " + plan.type : state.planId) + " · " +
      (copy.floor || "") + " " + state.reference.floor + " · " +
      (copy.apartment || "") + " " + state.reference.apartment;
  }

  function model() {
    return one("#utopia-model-viewer");
  }
  function focusModelOnBuilding(building, cinematic) {
    var mv = model();
    if (!mv || !building) return;
    clearCinematic();
    try {
      mv.interpolationDecay = cinematic ? 160 : 105;
      if (cinematic) {
        mv.cameraTarget = "0m 35m 0m";
        mv.cameraOrbit = "92deg 74deg 260m";
        mv.fieldOfView = "42deg";
        state.cinematicTimers.push(setTimeout(function () {
          mv.cameraTarget = building.camera_target;
          mv.cameraOrbit = building.camera_orbit;
          mv.fieldOfView = "30deg";
        }, 520));
        state.cinematicTimers.push(setTimeout(function () {
          mv.interpolationDecay = 58;
        }, 1500));
      } else {
        mv.cameraTarget = building.camera_target;
        mv.cameraOrbit = building.camera_orbit;
        mv.fieldOfView = "30deg";
      }
    } catch (_) {}
  }

  function selectBuilding(id, options) {
    var building = buildings[id];
    if (!building) return;
    options = options || {};
    state.buildingId = id;

    all("[data-utopia-building]").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-utopia-building") === id);
      button.setAttribute("aria-pressed", button.getAttribute("data-utopia-building") === id ? "true" : "false");
    });
    all(".utopia-model-hotspot").forEach(function (button) {
      button.classList.toggle("is-active", button.getAttribute("data-building") === id);
      button.setAttribute("aria-pressed", button.getAttribute("data-building") === id ? "true" : "false");
    });
    all("[data-plan-card]").forEach(function (card) {
      card.classList.toggle("is-building-match", card.getAttribute("data-building") === id);
    });

    var title = one("#utopia-building-title");
    var facts = one("#utopia-building-facts");
    var metrics = one("#utopia-building-metrics");
    var source = one("#utopia-building-source");
    var floors = one("[data-building-floors]");
    var height = one("[data-building-height]");
    if (title) title.textContent = building.label || id.toUpperCase();
    if (facts) facts.textContent = building.facts || "";
    if (floors) floors.textContent = building.floors || "";
    if (height) height.textContent = building.height || "";
    if (metrics) metrics.hidden = false;
    if (source) {
      var sourceUrl = safeUrl(building.source_url);
      source.hidden = !sourceUrl;
      if (sourceUrl) source.href = sourceUrl;
    }

    focusModelOnBuilding(building, !!options.cinematic);
    if (state.projectPopup && state.map) {
      var popupText = (copy.map_project || data.project.title) + "<br><b>" +
        esc(copy.map_selected || "") + ": " + esc(building.label || id.toUpperCase()) + "</b>";
      state.projectPopup.setHTML(popupText);
    }
    try {
      root.dispatchEvent(new CustomEvent("utopia:building", { detail: { id: id, building: building } }));
    } catch (_) {}
  }

  function resetModel() {
    clearCinematic();
    state.buildingId = "";
    all("[data-utopia-building],.utopia-model-hotspot").forEach(function (button) {
      button.classList.remove("is-active");
      button.setAttribute("aria-pressed", "false");
    });
    all("[data-plan-card]").forEach(function (card) { card.classList.remove("is-building-match"); });
    var mv = model();
    if (mv) {
      try {
        mv.interpolationDecay = 80;
        mv.cameraTarget = "0m 42m 0m";
        mv.cameraOrbit = "-28deg 68deg 220m";
        mv.fieldOfView = "36deg";
      } catch (_) {}
    }
    var title = one("#utopia-building-title");
    var facts = one("#utopia-building-facts");
    var metrics = one("#utopia-building-metrics");
    var source = one("#utopia-building-source");
    if (title) title.textContent = copy.select_building || "";
    if (facts) facts.textContent = copy.building_prompt || "";
    if (metrics) metrics.hidden = true;
    if (source) source.hidden = true;
    if (state.projectPopup) state.projectPopup.setText(copy.map_project || data.project.title);
  }

  function setView(view) {
    if (view !== "model" && view !== "concept") return;
    state.view = view;
    var mv = model();
    var concept = one(".utopia-concept-frame");
    if (mv) mv.hidden = view !== "model";
    if (concept) concept.hidden = view !== "concept";
    all("[data-utopia-view]").forEach(function (button) {
      var active = button.getAttribute("data-utopia-view") === view;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function cinematic() {
    var building = buildings[state.buildingId] || data.buildings[0];
    if (building) selectBuilding(building.id, { cinematic: true });
  }

  function setFullscreenLabel(active) {
    var button = one("[data-utopia-action='fullscreen']");
    if (!button) return;
    button.textContent = active ? button.getAttribute("data-label-exit") : button.getAttribute("data-label-enter");
    button.setAttribute("aria-pressed", active ? "true" : "false");
  }
  function leaveFallbackFullscreen() {
    if (!state.fallbackFullscreen) return;
    state.fallbackFullscreen = false;
    root.classList.remove("is-fallback-fullscreen");
    document.body.classList.remove("utopia-body-locked");
    setFullscreenLabel(false);
  }
  function toggleFullscreen() {
    if (document.fullscreenElement === root) {
      document.exitFullscreen().catch(function () {});
      return;
    }
    if (state.fallbackFullscreen) {
      leaveFallbackFullscreen();
      return;
    }
    if (root.requestFullscreen) {
      root.requestFullscreen().catch(function () {
        state.fallbackFullscreen = true;
        root.classList.add("is-fallback-fullscreen");
        document.body.classList.add("utopia-body-locked");
        setFullscreenLabel(true);
      });
      return;
    }
    state.fallbackFullscreen = true;
    root.classList.add("is-fallback-fullscreen");
    document.body.classList.add("utopia-body-locked");
    setFullscreenLabel(true);
  }
  document.addEventListener("fullscreenchange", function () {
    var active = document.fullscreenElement === root;
    document.body.classList.toggle("utopia-body-locked", active);
    setFullscreenLabel(active);
  });

  function filterPlans(buildingId) {
    all("[data-plan-filter]").forEach(function (button) {
      var active = button.getAttribute("data-plan-filter") === buildingId;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
    all("[data-plan-card]").forEach(function (card) {
      card.hidden = buildingId !== "all" && card.getAttribute("data-building") !== buildingId;
    });
  }

  function selectReference(button) {
    var planId = button.getAttribute("data-plan");
    var plan = plans[planId];
    if (!plan) return;
    state.planId = planId;
    state.referenceId = button.getAttribute("data-utopia-reference") || "";
    state.reference = {
      floor: Number(button.getAttribute("data-floor") || 0),
      apartment: Number(button.getAttribute("data-apartment") || 0)
    };
    all("[data-utopia-reference]").forEach(function (node) {
      var active = node === button;
      node.classList.toggle("is-active", active);
      node.setAttribute("aria-pressed", active ? "true" : "false");
    });
    all("[data-plan-card]").forEach(function (card) {
      card.classList.toggle("is-selected", card.getAttribute("data-plan-card") === planId);
    });
    selectBuilding(plan.building, { cinematic: true });
    updateFormContext();
  }

  function openPlan(planId) {
    var plan = plans[planId];
    var dialog = one("#utopia-plan-dialog");
    if (!plan || !dialog) return;
    state.planId = planId;
    selectBuilding(plan.building, { cinematic: false });
    var title = one("[data-plan-dialog-title]", dialog);
    var frame = one("iframe", dialog);
    var fallback = one(".utopia-plan-dialog__fallback a", dialog);
    var url = safeUrl(plan.url);
    if (title) title.textContent = (plan.building || "").toUpperCase() + " " + (plan.type || "");
    if (fallback) fallback.href = url || "#";
    if (frame && url) frame.src = url;
    if (typeof dialog.showModal === "function") dialog.showModal();
    else dialog.setAttribute("open", "open");
  }
  function closePlan() {
    var dialog = one("#utopia-plan-dialog");
    if (!dialog) return;
    var frame = one("iframe", dialog);
    if (typeof dialog.close === "function" && dialog.open) dialog.close();
    else dialog.removeAttribute("open");
    if (frame) frame.removeAttribute("src");
  }

  function leadSubmit(event) {
    event.preventDefault();
    var form = event.currentTarget;
    var name = String(form.elements.name.value || "").trim();
    var phone = String(form.elements.phone.value || "").trim();
    var email = String(form.elements.email.value || "").trim();
    var message = one(".utopia-inquiry__message", form);
    var button = one("button[type='submit']", form);
    if (!name || (!phone && !email)) {
      if (message) {
        message.hidden = false;
        message.className = "utopia-inquiry__message is-error";
        message.textContent = copy.error || "";
      }
      return;
    }

    var plan = plans[state.planId] || null;
    var payload = {
      source: "utopia_project_showroom",
      project_slug: data.project.slug,
      project_title: data.project.title,
      lang: data.lang,
      name: name,
      phone: phone,
      email: email,
      unit: "",
      floor: state.reference ? state.reference.floor : "",
      rooms: plan ? plan.rooms : "",
      sqm: plan ? plan.interior_sqm : "",
      direction: "",
      status: "",
      message: state.reference && plan
        ? (copy.selected_prefix || "") + " " + plan.building.toUpperCase() + " " + plan.type +
          ", " + (copy.floor || "") + " " + state.reference.floor +
          ", " + (copy.apartment || "") + " " + state.reference.apartment +
          ". " + (copy.unknown_availability || "")
        : (copy.no_selection || "")
    };
    if (button) {
      button.disabled = true;
      button.textContent = button.getAttribute("data-label-sending") || copy.submitting || "";
    }
    fetch(data.lead_endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (response) {
      if (!response.ok) throw new Error("lead_failed");
      if (message) {
        message.hidden = false;
        message.className = "utopia-inquiry__message is-success";
        message.textContent = copy.success || "";
      }
      form.reset();
    }).catch(function () {
      if (message) {
        message.hidden = false;
        message.className = "utopia-inquiry__message is-error";
        message.textContent = copy.error || "";
      }
    }).finally(function () {
      if (button) {
        button.disabled = false;
        button.textContent = button.getAttribute("data-label-default") || copy.submit || "";
      }
    });
  }

  function mapFallback() {
    var fallback = one(".utopia-map-fallback");
    var host = one("#utopia-context-map");
    if (host) host.hidden = true;
    if (fallback) fallback.hidden = false;
  }
  function markerElement(className, label) {
    var node = document.createElement("button");
    node.type = "button";
    node.className = className;
    if (label) node.setAttribute("aria-label", label);
    return node;
  }
  function addMarker(group, marker) {
    if (!state.mapGroups[group]) state.mapGroups[group] = [];
    state.mapGroups[group].push(marker);
  }
  function setMarkerGroup(group, visible) {
    state.mapVisible[group] = visible;
    (state.mapGroups[group] || []).forEach(function (marker) {
      if (visible) marker.addTo(state.map);
      else marker.remove();
    });
  }
  function setMapButtonCount(group) {
    var button = one("[data-map-layer='" + group + "']");
    if (!button) return;
    var count = (state.mapGroups[group] || []).length;
    button.setAttribute("data-count", String(count));
    if (group !== "satellite" && group !== "buildings3d") {
      button.textContent = button.textContent.replace(/\s*\(\d+\)\s*$/, "") + " (" + count + ")";
      if (!count) {
        button.disabled = true;
        button.classList.remove("is-active");
      }
    }
  }
  function popupHtml(name, distance, url) {
    var html = "<b>" + esc(name || "") + "</b>";
    if (distance) html += "<br><span>" + esc(formatNumber(Math.round(distance))) + " m</span>";
    var safe = safeUrl(url);
    if (safe) html += '<br><a href="' + esc(safe) + '" target="_blank" rel="noopener noreferrer">' + esc(copy.map_open_external || "") + "</a>";
    return html;
  }

  function initMap() {
    var mapData = data.map || {};
    var host = one("#utopia-context-map");
    if (!host || !mapData.token || !window.mapboxgl) {
      mapFallback();
      return;
    }
    try {
      window.mapboxgl.accessToken = mapData.token;
      var map = new window.mapboxgl.Map({
        container: host,
        style: "mapbox://styles/mapbox/light-v11",
        center: [Number(mapData.lng), Number(mapData.lat)],
        zoom: 14.35,
        pitch: 0,
        bearing: 0,
        cooperativeGestures: true,
        attributionControl: true
      });
      state.map = map;
      map.addControl(new window.mapboxgl.NavigationControl({ visualizePitch: true }), "top-left");

      var projectElement = markerElement("utopia-map-marker utopia-map-marker--project", copy.map_project || data.project.title);
      var projectPopup = new window.mapboxgl.Popup({ offset: 18, maxWidth: "280px" }).setText(copy.map_project || data.project.title);
      state.projectPopup = projectPopup;
      new window.mapboxgl.Marker({ element: projectElement, anchor: "center" })
        .setLngLat([Number(mapData.lng), Number(mapData.lat)])
        .setPopup(projectPopup)
        .addTo(map);

      (mapData.nearby || []).forEach(function (project) {
        if (!project.lat || !project.lng) return;
        var element = markerElement("utopia-map-marker utopia-map-marker--nearby", project.name);
        var marker = new window.mapboxgl.Marker({ element: element, anchor: "center" })
          .setLngLat([Number(project.lng), Number(project.lat)])
          .setPopup(new window.mapboxgl.Popup({ offset: 14, maxWidth: "280px" }).setHTML(popupHtml(project.name, 0, project.url)));
        addMarker("nearby", marker);
      });

      var pois = mapData.pois || {};
      var groupMap = {
        schools: "education",
        kindergartens: "education",
        parks: "parks",
        transit: "transit",
        shops: "shops",
        health: "health",
        food: "food"
      };
      Object.keys(groupMap).forEach(function (sourceGroup) {
        (pois[sourceGroup] || []).forEach(function (item) {
          if (!item.lat || !item.lng) return;
          var group = groupMap[sourceGroup];
          var element = markerElement("utopia-map-marker utopia-map-marker--" + group, item.name);
          var marker = new window.mapboxgl.Marker({ element: element, anchor: "center" })
            .setLngLat([Number(item.lng), Number(item.lat)])
            .setPopup(new window.mapboxgl.Popup({ offset: 14, maxWidth: "260px" }).setHTML(popupHtml(item.name, item.d, "")));
          addMarker(group, marker);
        });
      });

      state.mapVisible = {
        nearby: true,
        education: true,
        parks: true,
        transit: false,
        shops: false,
        health: false,
        food: false
      };
      Object.keys(state.mapGroups).forEach(function (group) {
        setMarkerGroup(group, !!state.mapVisible[group]);
        setMapButtonCount(group);
      });

      map.on("load", function () {
        try {
          map.addSource("utopia-satellite", {
            type: "raster",
            tiles: ["https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.jpg90?access_token=" + window.mapboxgl.accessToken],
            tileSize: 256
          });
          map.addLayer({
            id: "utopia-satellite",
            type: "raster",
            source: "utopia-satellite",
            layout: { visibility: "none" }
          });
          var labelLayer = null;
          (map.getStyle().layers || []).some(function (layer) {
            if (layer.type === "symbol" && layer.layout && layer.layout["text-field"]) {
              labelLayer = layer.id;
              return true;
            }
            return false;
          });
          map.addLayer({
            id: "utopia-buildings-3d",
            source: "composite",
            "source-layer": "building",
            filter: ["==", "extrude", "true"],
            type: "fill-extrusion",
            minzoom: 14,
            layout: { visibility: "none" },
            paint: {
              "fill-extrusion-color": "#d8d0bf",
              "fill-extrusion-height": ["get", "height"],
              "fill-extrusion-base": ["get", "min_height"],
              "fill-extrusion-opacity": 0.74
            }
          }, labelLayer || undefined);
        } catch (_) {}
      });
    } catch (_) {
      mapFallback();
    }
  }

  function handleMapLayer(button) {
    var layer = button.getAttribute("data-map-layer");
    if (!state.map) return;
    if (layer === "satellite") {
      if (!state.map.getLayer("utopia-satellite")) return;
      var satelliteOn = state.map.getLayoutProperty("utopia-satellite", "visibility") === "visible";
      state.map.setLayoutProperty("utopia-satellite", "visibility", satelliteOn ? "none" : "visible");
      button.classList.toggle("is-active", !satelliteOn);
      button.setAttribute("aria-pressed", satelliteOn ? "false" : "true");
      return;
    }
    if (layer === "buildings3d") {
      if (!state.map.getLayer("utopia-buildings-3d")) return;
      var buildingsOn = state.map.getLayoutProperty("utopia-buildings-3d", "visibility") === "visible";
      state.map.setLayoutProperty("utopia-buildings-3d", "visibility", buildingsOn ? "none" : "visible");
      state.map.easeTo({ pitch: buildingsOn ? 0 : 58, zoom: buildingsOn ? 14.35 : 15.3, duration: 800 });
      button.classList.toggle("is-active", !buildingsOn);
      button.setAttribute("aria-pressed", buildingsOn ? "false" : "true");
      return;
    }
    if (!(layer in state.mapVisible)) return;
    state.mapVisible[layer] = !state.mapVisible[layer];
    setMarkerGroup(layer, state.mapVisible[layer]);
    button.classList.toggle("is-active", state.mapVisible[layer]);
    button.setAttribute("aria-pressed", state.mapVisible[layer] ? "true" : "false");
  }

  root.addEventListener("click", function (event) {
    var buildingHotspot = event.target.closest(".utopia-model-hotspot[data-building]");
    if (buildingHotspot && root.contains(buildingHotspot)) {
      selectBuilding(buildingHotspot.getAttribute("data-building"), { cinematic: true });
      return;
    }
    var buildingButton = event.target.closest("[data-utopia-building]");
    if (buildingButton && root.contains(buildingButton)) {
      selectBuilding(buildingButton.getAttribute("data-utopia-building"), { cinematic: true });
      return;
    }
    var viewButton = event.target.closest("[data-utopia-view]");
    if (viewButton && root.contains(viewButton)) {
      setView(viewButton.getAttribute("data-utopia-view"));
      return;
    }
    var actionButton = event.target.closest("[data-utopia-action]");
    if (actionButton && root.contains(actionButton)) {
      var action = actionButton.getAttribute("data-utopia-action");
      if (action === "reset") resetModel();
      if (action === "cinematic") cinematic();
      if (action === "fullscreen") toggleFullscreen();
      return;
    }
    var filterButton = event.target.closest("[data-plan-filter]");
    if (filterButton && root.contains(filterButton)) {
      filterPlans(filterButton.getAttribute("data-plan-filter"));
      return;
    }
    var referenceButton = event.target.closest("[data-utopia-reference]");
    if (referenceButton && root.contains(referenceButton)) {
      selectReference(referenceButton);
      return;
    }
    var planButton = event.target.closest("[data-utopia-plan]");
    if (planButton && root.contains(planButton)) {
      openPlan(planButton.getAttribute("data-utopia-plan"));
      return;
    }
    var closeButton = event.target.closest("[data-utopia-dialog-close]");
    if (closeButton && root.contains(closeButton)) {
      closePlan();
      return;
    }
    var mapButton = event.target.closest("[data-map-layer]");
    if (mapButton && root.contains(mapButton)) {
      handleMapLayer(mapButton);
    }
  });
  root.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closePlan();
      leaveFallbackFullscreen();
    }
  });
  var form = one("#utopia-inquiry-form");
  if (form) form.addEventListener("submit", leadSubmit);
  var dialog = one("#utopia-plan-dialog");
  if (dialog) {
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) closePlan();
    });
    dialog.addEventListener("close", function () {
      var frame = one("iframe", dialog);
      if (frame) frame.removeAttribute("src");
    });
  }

  var mv = model();
  if (mv) {
    mv.addEventListener("error", function () { setView("concept"); });
    if (window.customElements && window.customElements.whenDefined) {
      window.customElements.whenDefined("model-viewer").then(function () {
        mv.setAttribute("reveal", "auto");
      }).catch(function () {});
    }
  }

  var mapHost = one("#utopia-context-map");
  if (mapHost && "IntersectionObserver" in window) {
    var mapObserver = new IntersectionObserver(function (entries, observer) {
      if (!entries[0] || !entries[0].isIntersecting) return;
      observer.disconnect();
      initMap();
    }, { rootMargin: "360px 0px" });
    mapObserver.observe(mapHost);
  } else if (mapHost) {
    initMap();
  }

  all("[data-plan-filter],[data-map-layer],[data-utopia-view]").forEach(function (button) {
    button.setAttribute("aria-pressed", button.classList.contains("is-active") ? "true" : "false");
  });
  resetModel();
  updateFormContext();
})();
