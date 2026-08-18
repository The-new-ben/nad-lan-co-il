/* Einstein-only flagship v3 integration adapter. No storage, analytics or invented inventory. */
(function () {
  "use strict";

  var PROJECT_ID = "einstein-tower-6885-32";
  var VIEW_SCHEMA = "nadlan-einstein-window-view/v1";
  var LEAD_SCHEMA = "nadlan-einstein-project-inquiry/v1";
  var UNIT_SCHEMA = "nadlan-einstein-unit-map-bridge/v1";
  var MAP_ADAPTER_SCHEMA = "nadlan-einstein-canonical-map-adapter/v1";
  var MAP_STATE_SCHEMA = "nadlan-einstein-canonical-map-state/v1";
  var INTEGRATION_STATE_SCHEMA = "nadlan-einstein-integration-state/v1";
  var SPATIAL_ENTITY_SCHEMA = "nadlan-flagship-spatial-entity/v1";
  var MAPBOX_RTL_URL = "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.4.0/mapbox-gl-rtl-text.js";
  var WINDOW_MIN_PITCH = 62;
  var WINDOW_MAX_PITCH = 85;
  var mapboxLoader = null;
  var mapboxRtlLoader = null;

  function plain(value) { return !!value && typeof value === "object" && !Array.isArray(value); }
  function finite(value) { return typeof value === "number" && Number.isFinite(value); }
  function clone(value) {
    if (value === undefined) return undefined;
    if (typeof structuredClone === "function") return structuredClone(value);
    return JSON.parse(JSON.stringify(value));
  }
  function validSourceIds(value) {
    return Array.isArray(value) && value.length > 0 && value.length <= 32 && value.every(function (id, index) {
      return typeof id === "string" && /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/.test(id) && value.indexOf(id) === index;
    });
  }
  function evidencePoint(value) {
    if (!plain(value) || (value.verification_state !== "verified" && value.verification_state !== "source_cited")
      || !finite(value.lat) || Math.abs(value.lat) > 90 || !finite(value.lng) || Math.abs(value.lng) > 180
      || !validSourceIds(value.source_ids)) return null;
    return Object.freeze({ lat: value.lat, lng: value.lng, sourceIds: Object.freeze(value.source_ids.slice()), verificationState: value.verification_state });
  }
  function verifiedBearing(value) {
    return plain(value) && value.bearing_state === "verified" && finite(value.bearing) && value.bearing >= 0 && value.bearing < 360
      && validSourceIds(value.bearing_source_ids);
  }
  function safeSameOriginUrl(value, expectedPath) {
    try {
      var url = new URL(String(value || ""), window.location.origin);
      return url.origin === window.location.origin && url.pathname === expectedPath && !url.search && !url.hash ? url.href : "";
    } catch (_error) { return ""; }
  }
  function safeSitePath(value, expectedPath) {
    try {
      var url = new URL(String(value || ""), window.location.origin);
      return url.origin === window.location.origin && url.pathname === expectedPath && !url.search && !url.hash ? url.href : "";
    } catch (_error) { return ""; }
  }
  function validView(value) {
    return plain(value) && value.schema === VIEW_SCHEMA && finite(value.lat) && finite(value.lng)
      && Math.abs(value.lat) <= 90 && Math.abs(value.lng) <= 180
      && validSourceIds(value.location_source_ids)
      && finite(value.illustrative_tower_height_m) && value.illustrative_tower_height_m === 93.22
      && value.height_basis === "owner_approved_model_bounds"
      && value.bearing_state === "unknown" && value.unknown_bearing_fallback === "honest_360"
      && value.map_style === "mapbox://styles/mapbox/satellite-streets-v12"
      && value.earth_state === "adjacent_district_context_only"
      && value.earth_url === "/earth/sde-dov/"
      && value.earth_context_label === "שדה דב הסמוך — הקשר רובעי, לא מיקום איינשטיין"
      && (value.mapbox_public_token === "" || /^pk\.[A-Za-z0-9._-]{20,512}$/.test(value.mapbox_public_token));
  }
  function validLead(value) {
    return plain(value) && value.schema === LEAD_SCHEMA && value.source === "showroom_unit_journey_v2"
      && value.card_id === 4867 && value.project_slug === "einstein-tower"
      && value.project_title === "EINSTEIN TOWER תל אביב" && value.lang === "he"
      && value.source_path === "/projects/einstein-tower/"
      && typeof value.consent_version === "string" && value.consent_version.length >= 10
      && typeof value.consent_text === "string" && value.consent_text.length >= 20
      && value.data_controller === "nad-lan.co.il" && value.purpose === "project_inquiry_follow_up"
      && value.retention_policy === "manual_review_until_resolution_or_erasure_request"
      && value.rights_path === "/contact/" && value.automated_expiry === false
      && !!safeSameOriginUrl(value.rights_url, "/contact/") && value.routing_state === "site_admin_fallback"
      && value.success_state === "recorded_not_routed"
      && !!safeSameOriginUrl(value.source_url, "/projects/einstein-tower/")
      && !!safeSameOriginUrl(value.endpoint, "/wp-json/nadlan/v1/lead");
  }
  function validUnitBridge(value) {
    return plain(value) && value.schema === UNIT_SCHEMA && value.inventory_state === "not_supplied"
      && value.production_enabled === false
      && Array.isArray(value.required_methods)
      && value.required_methods.join("|") === "showViewCone|easeMapToUnitView";
  }
  function validCoTourRuntime(value) {
    return plain(value) && value.schema === "nadlan-flagship-cotour-runtime/v1" && value.enabled === true
      && value.project_id === 4867 && value.project_contract_id === PROJECT_ID
      && value.ttl_seconds === 600 && value.poll_interval_ms === 1200 && value.max_state_bytes === 65536
      && plain(value.endpoints)
      && !!safeSameOriginUrl(value.endpoints.create, "/wp-json/nadlan/v1/flagship-cotour/create")
      && !!safeSameOriginUrl(value.endpoints.join_poll, "/wp-json/nadlan/v1/flagship-cotour/join-poll")
      && !!safeSameOriginUrl(value.endpoints.update, "/wp-json/nadlan/v1/flagship-cotour/update")
      && !!safeSameOriginUrl(value.endpoints.end, "/wp-json/nadlan/v1/flagship-cotour/end");
  }

  function loadMapboxOnIntent() {
    if (mapboxLoader) return mapboxLoader;
    mapboxLoader = new Promise(function (resolve, reject) {
      var style = document.querySelector('link[data-nlfs-mapbox="3.7.0"],link[href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css"]');
      if (!style) {
        style = document.createElement("link");
        style.rel = "stylesheet";
        style.href = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";
        style.dataset.nlfsMapbox = "3.7.0";
        document.head.appendChild(style);
      }
      var script = document.querySelector('script[data-nlfs-mapbox="3.7.0"],script[src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"]');
      if (!script) {
        script = document.createElement("script");
        script.src = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";
        script.dataset.nlfsMapbox = "3.7.0";
        script.async = true;
        document.head.appendChild(script);
      }
      var settled = false;
      var scriptReady = !!(window.mapboxgl && typeof window.mapboxgl.Map === "function");
      var styleReady = false;
      var stylePoll = 0;
      var timeout = window.setTimeout(function () { finish(new Error("mapbox_timeout")); }, 12000);
      function stylesheetReady() {
        try { return !!(style && style.sheet); } catch (_error) { return true; }
      }
      function maybeReady() {
        if (settled) return;
        styleReady = styleReady || stylesheetReady();
        scriptReady = scriptReady || !!(window.mapboxgl && typeof window.mapboxgl.Map === "function");
        if (styleReady && scriptReady) finish(null);
      }
      function finish(error) {
        if (settled) return;
        settled = true;
        window.clearTimeout(timeout);
        if (stylePoll) window.clearInterval(stylePoll);
        if (!error && window.mapboxgl && typeof window.mapboxgl.Map === "function") resolve(window.mapboxgl);
        else reject(error || new Error("mapbox_unavailable"));
      }
      function scriptLoaded() { scriptReady = true; maybeReady(); }
      function styleLoaded() { styleReady = true; maybeReady(); }
      script.addEventListener("load", scriptLoaded, { once: true });
      script.addEventListener("error", function () { finish(new Error("mapbox_failed")); }, { once: true });
      style.addEventListener("load", styleLoaded, { once: true });
      style.addEventListener("error", function () { finish(new Error("mapbox_css_failed")); }, { once: true });
      stylePoll = window.setInterval(maybeReady, 50);
      maybeReady();
    }).catch(function (error) { mapboxLoader = null; throw error; });
    return mapboxLoader;
  }

  function loadMapboxRtl(mapboxgl) {
    if (!mapboxgl || typeof mapboxgl.setRTLTextPlugin !== "function") return Promise.reject(new Error("mapbox_rtl_api_missing"));
    var status = typeof mapboxgl.getRTLTextPluginStatus === "function" ? mapboxgl.getRTLTextPluginStatus() : "unavailable";
    if (status === "loaded") return Promise.resolve(mapboxgl);
    if (status === "deferred") return Promise.resolve(mapboxgl);
    if (mapboxRtlLoader) return mapboxRtlLoader.then(function () { return mapboxgl; });
    mapboxRtlLoader = new Promise(function (resolve, reject) {
      var settled = false;
      var timeout = window.setTimeout(function () { finish(new Error("mapbox_rtl_timeout")); }, 12000);
      function finish(error) {
        if (settled) return;
        settled = true;
        window.clearTimeout(timeout);
        if (error) reject(error);
        else resolve(true);
      }
      if (status === "loading") {
        (function poll() {
          if (settled) return;
          var current = typeof mapboxgl.getRTLTextPluginStatus === "function" ? mapboxgl.getRTLTextPluginStatus() : "error";
          if (current === "loaded") { finish(null); return; }
          if (current === "error" || current === "unavailable") { finish(new Error("mapbox_rtl_failed")); return; }
          if (!settled) window.setTimeout(poll, 40);
        })();
        return;
      }
      try {
        mapboxgl.setRTLTextPlugin(MAPBOX_RTL_URL, function (error) { finish(error || null); }, false);
      } catch (error) { finish(error); }
    }).catch(function (error) { mapboxRtlLoader = null; throw error; });
    return mapboxRtlLoader.then(function () { return mapboxgl; });
  }

  function bridgeVerifiedUnit(contract, mapAdapter, unit) {
    if (!plain(contract) || contract.schema !== UNIT_SCHEMA || contract.production_enabled !== true
      || contract.inventory_state !== "verified" || !plain(unit) || unit.verified !== true
      || typeof unit.id !== "string" || !unit.id || !Number.isInteger(unit.floor)
      || !Array.isArray(contract.verified_unit_ids) || contract.verified_unit_ids.indexOf(unit.id) < 0
      || !verifiedBearing(unit)
      || !mapAdapter || typeof mapAdapter.showViewCone !== "function" || typeof mapAdapter.easeMapToUnitView !== "function") return false;
    if (mapAdapter.showViewCone(unit) !== true) return false;
    if (mapAdapter.easeMapToUnitView(unit) !== true) return false;
    return true;
  }

  function createUnitMapAdapter(map, projectPoint) {
    var canonicalPoint = evidencePoint(projectPoint);
    if (!map || typeof map.easeTo !== "function" || !canonicalPoint) return null;
    var viewCone = null;
    var selectedEntityId = "";
    var correlationState = "idle";
    function removeViewCone() {
      if (viewCone) { try { viewCone.remove(); } catch (_error) {} viewCone = null; }
    }
    function mapCamera() {
      try {
        var center = typeof map.getCenter === "function" ? map.getCenter() : null;
        var lng = center && finite(Number(center.lng)) ? Number(center.lng) : null;
        var lat = center && finite(Number(center.lat)) ? Number(center.lat) : null;
        var zoom = typeof map.getZoom === "function" ? Number(map.getZoom()) : null;
        var bearing = typeof map.getBearing === "function" ? Number(map.getBearing()) : null;
        var pitch = typeof map.getPitch === "function" ? Number(map.getPitch()) : null;
        if (!finite(lng) || Math.abs(lng) > 180 || !finite(lat) || Math.abs(lat) > 90 || !finite(zoom) || zoom < 0 || zoom > 24
          || !finite(bearing) || Math.abs(bearing) > 3600 || !finite(pitch) || pitch < 0 || pitch > 85) return null;
        return { lng: lng, lat: lat, zoom: zoom, bearing: bearing, pitch: pitch };
      } catch (_error) { return null; }
    }
    function validMapState(value) {
      var camera = value && value.camera;
      return plain(value) && value.schema === MAP_STATE_SCHEMA && (value.available === true || value.available === false)
        && typeof value.selectedEntityId === "string" && value.selectedEntityId.length <= 128
        && ["idle", "panned", "cone", "unavailable-no-source", "unavailable-no-bearing"].indexOf(value.correlationState) >= 0
        && (value.available === false ? camera === null : plain(camera)
          && finite(camera.lng) && Math.abs(camera.lng) <= 180 && finite(camera.lat) && Math.abs(camera.lat) <= 90
          && finite(camera.zoom) && camera.zoom >= 0 && camera.zoom <= 24
          && finite(camera.bearing) && Math.abs(camera.bearing) <= 3600
          && finite(camera.pitch) && camera.pitch >= 0 && camera.pitch <= 85);
    }
    function entityPoint(entity) {
      return evidencePoint(entity && (entity.mapPosition || entity.map_position));
    }
    function showViewCone(entity) {
      if (!verifiedBearing(entity) || !window.mapboxgl || typeof window.mapboxgl.Marker !== "function") return false;
      var point = entityPoint(entity) || canonicalPoint;
      try {
        if (!viewCone) {
          var element = document.createElement("div");
          element.className = "nlfs-map-view-cone";
          element.setAttribute("aria-hidden", "true");
          element.innerHTML = '<svg width="150" height="150" viewBox="0 0 150 150"><path d="M75 75 L44 8 A78 78 0 0 1 106 8 Z" fill="rgba(194,86,58,.38)" stroke="#C2563A" stroke-opacity=".55"/></svg>';
          viewCone = new window.mapboxgl.Marker({ element: element, rotationAlignment: "map", pitchAlignment: "map", anchor: "center" }).setLngLat([point.lng, point.lat]);
        }
        viewCone.setLngLat([point.lng, point.lat]).setRotation(entity.bearing).addTo(map);
        correlationState = "cone";
        return true;
      } catch (_error) { return false; }
    }
    function motionDuration(duration) {
      try { return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : duration; }
      catch (_error) { return duration; }
    }
    return Object.freeze({
      schema: MAP_ADAPTER_SCHEMA,
      showViewCone: showViewCone,
      easeMapToUnitView: function (unit) {
        if (!plain(unit) || unit.verified !== true || !verifiedBearing(unit)) return false;
        try {
          selectedEntityId = String(unit.id || "").slice(0, 128);
          map.easeTo({ center: [canonicalPoint.lng, canonicalPoint.lat], bearing: unit.bearing, zoom: 15.2, duration: motionDuration(900) });
          correlationState = "cone";
          return true;
        } catch (_error) { return false; }
      },
      selectEntity: function (entity) {
        if (!plain(entity) || entity.schema !== SPATIAL_ENTITY_SCHEMA || typeof entity.id !== "string" || !entity.id || entity.id.length > 128) return false;
        selectedEntityId = entity.id;
        removeViewCone();
        var point = entityPoint(entity);
        if (!point) { correlationState = "unavailable-no-source"; return false; }
        var options = { center: [point.lng, point.lat], duration: motionDuration(700) };
        if (finite(entity.mapZoom) && entity.mapZoom >= 0 && entity.mapZoom <= 24) options.zoom = entity.mapZoom;
        if (verifiedBearing(entity)) options.bearing = entity.bearing;
        try { map.easeTo(options); } catch (_error) { correlationState = "unavailable-no-source"; return false; }
        correlationState = "panned";
        if (verifiedBearing(entity) && showViewCone(entity)) correlationState = "cone";
        else if (entity.bearing_state && entity.bearing_state !== "verified") correlationState = "unavailable-no-bearing";
        return true;
      },
      clearSelection: function () {
        selectedEntityId = "";
        correlationState = "idle";
        removeViewCone();
        return true;
      },
      getState: function () {
        var camera = mapCamera();
        return {
          schema: MAP_STATE_SCHEMA,
          available: !!camera,
          camera: camera,
          selectedEntityId: selectedEntityId,
          correlationState: correlationState
        };
      },
      restoreState: function (value) {
        if (!validMapState(value) || value.available !== true || !value.camera) return false;
        try {
          map.jumpTo({ center: [value.camera.lng, value.camera.lat], zoom: value.camera.zoom, bearing: value.camera.bearing, pitch: value.camera.pitch });
          selectedEntityId = "";
          correlationState = "idle";
          removeViewCone();
          return true;
        } catch (_error) { return false; }
      },
      getCapabilities: function () {
        return {
          schema: MAP_ADAPTER_SCHEMA,
          canonicalHandleAdopted: true,
          canonicalHandleReplaced: false,
          privateEngineClosuresAssumedPublic: false,
          beamMechanismMutated: false,
          panRequiresSourceCitedCoordinates: true,
          coneRequiresVerifiedBearing: true
        };
      },
      destroy: function () {
        removeViewCone();
      }
    });
  }

  function createWindowView(host, contract, stateChanged) {
    var noopController = Object.freeze({ destroy: function () {}, getState: function () { return { bearing: 0, pitch: WINDOW_MAX_PITCH }; }, restoreState: function () { return false; } });
    if (!host || !validView(contract)) return noopController;
    host.dataset.nlfsWindowView = "initializing";
    host.dataset.bearingState = "unknown";
    host.dataset.heightBasis = contract.height_basis;
    host.innerHTML = '<div class="nlfs-window-view__map" data-nlfs-window-map role="application" tabindex="0" aria-keyshortcuts="ArrowLeft ArrowRight ArrowUp ArrowDown Home" aria-label="מבט לוויין אינטראקטיבי מגובה המחשה של המגדל. גררו להביט או השתמשו בחצים."></div>'
      + '<div class="nlfs-window-view__controls" aria-label="סיבוב מבט 360 מעלות">'
      + '<button type="button" data-nlfs-window-turn="-45" aria-label="סיבוב שמאלה 45 מעלות">−45°</button>'
      + '<button type="button" data-nlfs-window-turn="45" aria-label="סיבוב ימינה 45 מעלות">+45°</button>'
      + '<button type="button" data-nlfs-window-reset>360°</button></div>'
      + '<p class="nlfs-window-view__disclosure">גובה המבט 93.22 מ׳ מבוסס על גבולות מודל המחשה מאושר, לא על דירה או קומה. זווית המצלמה כמעט אנכית (85°). כיוון דירה לא סופק ולכן המבט הוא 360°.</p>'
      + '<p data-nlfs-window-status role="status">טוענים שכבת לוויין…</p>';
    var mapNode = host.querySelector("[data-nlfs-window-map]");
    var status = host.querySelector("[data-nlfs-window-status]");
    var controller = new AbortController();
    var signal = controller.signal;
    var map = null;
    var bearing = 0;
    var pitch = WINDOW_MAX_PITCH;
    var drag = null;
    var resizeFrames = [];
    var panoramaFrame = 0;
    var panoramaStartedAt = 0;
    var panoramaElapsed = 0;
    var panoramaActive = false;
    var panoramaSkip = false;
    var available = false;
    var terminalUnavailable = false;
    var restoredCamera = null;
    var mapLoadTimer = 0;
    var readinessTimer = 0;
    var readinessDeadline = 0;
    var readyCompleted = false;
    var reducedMotion = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

    function setStatus(text) { if (status) status.textContent = text; }
    function notify() { if (typeof stateChanged === "function") stateChanged(); }
    function camera() {
      if (!map || !window.mapboxgl || !window.mapboxgl.MercatorCoordinate) return;
      try {
        var options = map.getFreeCameraOptions();
        options.position = window.mapboxgl.MercatorCoordinate.fromLngLat({ lng: contract.lng, lat: contract.lat }, contract.illustrative_tower_height_m);
        options.setPitchBearing(pitch, bearing);
        map.setFreeCameraOptions(options);
        if (typeof map.getBearing === "function") bearing = ((Number(map.getBearing()) || 0) % 360 + 360) % 360;
        if (typeof map.getPitch === "function") pitch = Math.max(WINDOW_MIN_PITCH, Math.min(WINDOW_MAX_PITCH, Number(map.getPitch()) || pitch));
        host.dataset.currentBearing = bearing.toFixed(2);
        host.dataset.currentPitch = pitch.toFixed(2);
      } catch (_error) {}
    }
    function currentBearing() {
      try { return map && typeof map.getBearing === "function" ? Number(map.getBearing()) || 0 : bearing; } catch (_error) { return bearing; }
    }
    function stopPanorama(commit) {
      if (panoramaFrame) window.cancelAnimationFrame(panoramaFrame);
      panoramaFrame = 0;
      panoramaStartedAt = 0;
      panoramaElapsed = 0;
      panoramaActive = false;
      if (commit) notify();
    }
    function turn(delta) { if (!available || terminalUnavailable) return; stopPanorama(false); bearing = (currentBearing() + delta + 360) % 360; camera(); notify(); }
    function beginPanorama() {
      if (!available || terminalUnavailable) return;
      stopPanorama(false);
      bearing = 0;
      pitch = WINDOW_MAX_PITCH;
      camera();
      if (reducedMotion) {
        setStatus("מבט 360° מוכן. גררו את המבט או השתמשו בכפתורי הסיבוב.");
        notify();
        return;
      }
      panoramaActive = true;
      panoramaElapsed = 0;
      if (document.hidden) {
        setStatus("מבט 360° מושהה כשהעמוד מוסתר; הוא יתחדש בחזרה לעמוד.");
        notify();
        return;
      }
      resumePanorama();
    }
    function resumePanorama() {
      if (!available || terminalUnavailable || !panoramaActive || reducedMotion || document.hidden || signal.aborted || panoramaFrame) return;
      setStatus("מבט 360° נע באיטיות. כל מגע עוצר את הסיבוב.");
      panoramaStartedAt = performance.now();
      function frame(now) {
        if (signal.aborted || !panoramaActive || !panoramaStartedAt) return;
        if (document.hidden) { pausePanorama(); return; }
        panoramaSkip = !panoramaSkip;
        if (!panoramaSkip) {
          var elapsed = Math.min(30000, Math.max(0, panoramaElapsed + now - panoramaStartedAt));
          bearing = (elapsed * 0.012) % 360;
          camera();
          if (elapsed >= 30000) { bearing = 0; camera(); stopPanorama(true); setStatus("הושלם סיבוב 360°. אפשר לגרור או להשתמש בכפתורים."); return; }
        }
        panoramaFrame = window.requestAnimationFrame(frame);
      }
      panoramaFrame = window.requestAnimationFrame(frame);
    }
    function pausePanorama() {
      if (!panoramaActive) return;
      if (panoramaStartedAt) panoramaElapsed = Math.min(30000, panoramaElapsed + Math.max(0, performance.now() - panoramaStartedAt));
      if (panoramaFrame) window.cancelAnimationFrame(panoramaFrame);
      panoramaFrame = 0;
      panoramaStartedAt = 0;
      setStatus("מבט 360° מושהה כשהעמוד מוסתר; הוא יתחדש בחזרה לעמוד.");
    }
    function setMapControlsEnabled(enabled) {
      host.querySelectorAll("[data-nlfs-window-turn],[data-nlfs-window-reset]").forEach(function (control) {
        control.disabled = !enabled;
        control.setAttribute("aria-disabled", enabled ? "false" : "true");
      });
    }
    function clearMapDeadlines() {
      if (mapLoadTimer) window.clearTimeout(mapLoadTimer);
      if (readinessTimer) window.clearTimeout(readinessTimer);
      mapLoadTimer = 0;
      readinessTimer = 0;
    }
    function unavailable(reason) {
      if (terminalUnavailable) return;
      terminalUnavailable = true;
      available = false;
      stopPanorama(false);
      clearMapDeadlines();
      host.dataset.nlfsWindowView = "unavailable";
      host.dataset.rtlTextState = "unavailable";
      host.dataset.mapStyleLoaded = "false";
      host.dataset.mapTilesLoaded = "false";
      host.dataset.mapFailure = String(reason && reason.message ? reason.message : reason || "unavailable").slice(0, 80);
      if (mapNode) mapNode.hidden = true;
      setMapControlsEnabled(false);
      if (map) { try { map.remove(); } catch (_error) {} map = null; }
      setStatus("מפת הלוויין אינה זמינה כרגע. לא הומצא כיוון חלופי.");
    }

    setMapControlsEnabled(false);

    host.addEventListener("click", function (event) {
      if (!available || terminalUnavailable) return;
      var turnButton = event.target.closest("[data-nlfs-window-turn]");
      if (turnButton) turn(Number(turnButton.dataset.nlfsWindowTurn) || 0);
      if (event.target.closest("[data-nlfs-window-reset]")) beginPanorama();
    }, { signal: signal });

    mapNode.addEventListener("pointerdown", function (event) {
      if (!available || terminalUnavailable) return;
      stopPanorama(false);
      drag = { id: event.pointerId, x: event.clientX, y: event.clientY, bearing: bearing, pitch: pitch };
      try { mapNode.setPointerCapture(event.pointerId); } catch (_error) {}
      event.preventDefault();
    }, { signal: signal });
    mapNode.addEventListener("pointermove", function (event) {
      if (!drag || drag.id !== event.pointerId) return;
      bearing = (drag.bearing + (event.clientX - drag.x) * 0.28 + 3600) % 360;
      pitch = Math.max(WINDOW_MIN_PITCH, Math.min(WINDOW_MAX_PITCH, drag.pitch - (event.clientY - drag.y) * 0.12));
      camera();
      event.preventDefault();
    }, { signal: signal });
    function finishDrag(event) {
      if (!drag || drag.id !== event.pointerId) return;
      drag = null;
      notify();
    }
    mapNode.addEventListener("pointerup", finishDrag, { signal: signal });
    mapNode.addEventListener("pointercancel", finishDrag, { signal: signal });
    mapNode.addEventListener("keydown", function (event) {
      if (!available || terminalUnavailable) return;
      if (event.key === "ArrowLeft") turn(-8);
      else if (event.key === "ArrowRight") turn(8);
      else if (event.key === "ArrowUp") { stopPanorama(false); pitch = Math.min(WINDOW_MAX_PITCH, pitch + 3); camera(); notify(); }
      else if (event.key === "ArrowDown") { stopPanorama(false); pitch = Math.max(WINDOW_MIN_PITCH, pitch - 3); camera(); notify(); }
      else if (event.key === "Home") beginPanorama();
      else return;
      event.preventDefault();
    }, { signal: signal });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) pausePanorama();
      else resumePanorama();
    }, { signal: signal });

    if (!contract.mapbox_public_token) {
      unavailable();
      return Object.freeze({
        destroy: function () { controller.abort(); host.replaceChildren(); },
        getState: function () { return { bearing: bearing, pitch: pitch }; },
        restoreState: function (value) {
          if (!plain(value) || !finite(value.bearing) || value.bearing < 0 || value.bearing >= 360 || !finite(value.pitch) || value.pitch < WINDOW_MIN_PITCH || value.pitch > WINDOW_MAX_PITCH) return false;
          bearing = value.bearing; pitch = value.pitch; return true;
        }
      });
    }
    function boot(mapboxgl) {
      if (signal.aborted) return;
      try {
        mapboxgl.accessToken = contract.mapbox_public_token;
        host.dataset.rtlTextState = "loading";
        host.dataset.mapboxCssReady = "true";
        host.dataset.mapStyle = contract.map_style;
        host.dataset.mapStyleLoaded = "false";
        host.dataset.mapTilesLoaded = "false";
        map = new mapboxgl.Map({
        container: mapNode,
        style: contract.map_style,
        center: [contract.lng, contract.lat],
        zoom: 16.7,
        pitch: 70,
        bearing: 0,
        maxPitch: WINDOW_MAX_PITCH,
        attributionControl: true,
        interactive: false
      });
        mapLoadTimer = window.setTimeout(function () { unavailable("map_load_timeout"); }, 15000);
        map.once("load", function () {
          if (signal.aborted) return;
          if (mapLoadTimer) window.clearTimeout(mapLoadTimer);
          mapLoadTimer = 0;
          var labelLayer = (map.getStyle().layers || []).find(function (layer) { return layer.type === "symbol" && layer.layout && layer.layout["text-field"]; });
          try {
            map.addLayer({ id: "nlfs-einstein-buildings", source: "composite", "source-layer": "building", filter: ["==", "extrude", "true"], type: "fill-extrusion", minzoom: 13,
              paint: { "fill-extrusion-color": "#d8d2c4", "fill-extrusion-height": ["get", "height"], "fill-extrusion-base": ["get", "min_height"], "fill-extrusion-opacity": 0.72 } }, labelLayer && labelLayer.id);
          } catch (_error) {}
          try {
            map.addSource("nlfs-einstein-site", { type: "geojson", data: { type: "FeatureCollection", features: [{ type: "Feature", properties: { name: "מגדל איינשטיין" }, geometry: { type: "Point", coordinates: [contract.lng, contract.lat] } }] } });
            map.addLayer({ id: "nlfs-einstein-site-dot", type: "circle", source: "nlfs-einstein-site", paint: { "circle-radius": 6, "circle-color": "#c2563a", "circle-stroke-width": 2, "circle-stroke-color": "#ffffff" } });
            map.addLayer({ id: "nlfs-einstein-site-label", type: "symbol", source: "nlfs-einstein-site", layout: { "text-field": ["get", "name"], "text-size": 14, "text-offset": [0, 1.25], "text-anchor": "top" }, paint: { "text-color": "#ffffff", "text-halo-color": "#092f2e", "text-halo-width": 1.5 } });
          } catch (_error) { unavailable("einstein_label_failed"); return; }
          readinessDeadline = performance.now() + 15000;
          function finishReadyWhenMaterialized() {
            if (signal.aborted || terminalUnavailable || readyCompleted) return;
            var rtlStatus = typeof mapboxgl.getRTLTextPluginStatus === "function" ? mapboxgl.getRTLTextPluginStatus() : "loaded";
            host.dataset.rtlTextState = rtlStatus;
            var styleLoaded = false;
            var tilesLoaded = false;
            try {
              styleLoaded = typeof map.isStyleLoaded !== "function" || map.isStyleLoaded() === true;
              tilesLoaded = typeof map.areTilesLoaded !== "function" || map.areTilesLoaded() === true;
            } catch (_error) {}
            host.dataset.mapStyleLoaded = styleLoaded ? "true" : "false";
            host.dataset.mapTilesLoaded = tilesLoaded ? "true" : "false";
            /* rtlStatus stays honestly recorded in the dataset above, but only
               style and tiles gate readiness — see the boot-chain note. */
            if (!styleLoaded || !tilesLoaded) {
              if (performance.now() >= readinessDeadline) { unavailable("map_materialization_timeout"); return; }
              readinessTimer = window.setTimeout(finishReadyWhenMaterialized, 80);
              return;
            }
            readinessTimer = 0;
            readyCompleted = true;
            available = true;
            host.dataset.nlfsWindowView = "ready";
            setMapControlsEnabled(true);
            if (restoredCamera) {
              bearing = restoredCamera.bearing;
              pitch = restoredCamera.pitch;
              restoredCamera = null;
              stopPanorama(false);
              camera();
              setStatus("מבט 360° שוחזר. גררו את המבט או השתמשו בכפתורי הסיבוב.");
            } else beginPanorama();
            try { map.resize(); } catch (_error) {}
            resizeFrames.push(window.requestAnimationFrame(function () {
              resizeFrames.push(window.requestAnimationFrame(function () { try { map.resize(); camera(); } catch (_error) {} }));
            }));
          }
          map.on("idle", finishReadyWhenMaterialized);
          finishReadyWhenMaterialized();
        });
        map.on("error", function (event) {
          host.dataset.mapErrorObserved = "true";
          unavailable(event && event.error ? event.error : "map_runtime_error");
        });
      } catch (_error) { unavailable(_error); }
    }
    /* RTL text shaping is an enhancement, not a boot requirement: mapbox-gl v3
       renders Hebrew labels correctly without the plugin (proven on the attached
       area map), and the plugin worker import can fail when another map on the
       page already claimed the single global RTL slot. The satellite view must
       not die for a label plugin. */
    loadMapboxOnIntent().then(function (mapboxgl) {
      return loadMapboxRtl(mapboxgl).catch(function () { return mapboxgl; });
    }).then(boot).catch(unavailable);

    return Object.freeze({
      destroy: function () {
        controller.abort();
        stopPanorama(false);
        clearMapDeadlines();
        resizeFrames.splice(0).forEach(function (frame) { window.cancelAnimationFrame(frame); });
        if (map) { try { map.remove(); } catch (_error) {} }
        host.replaceChildren();
      },
      getState: function () { return { bearing: bearing, pitch: pitch }; },
      restoreState: function (value) {
        if (!plain(value) || !finite(value.bearing) || value.bearing < 0 || value.bearing >= 360 || !finite(value.pitch) || value.pitch < WINDOW_MIN_PITCH || value.pitch > WINDOW_MAX_PITCH || terminalUnavailable) return false;
        stopPanorama(false);
        bearing = value.bearing; pitch = value.pitch;
        if (available && map) camera();
        else restoredCamera = { bearing: bearing, pitch: pitch };
        return true;
      }
    });
  }

  function mountLeadForm(root, contract, transport, runtimeConfig) {
    var form = root.querySelector("[data-nlfs-inquiry]");
    if (!form || !validLead(contract)) return function () {};
    var status = form.querySelector("[data-nlfs-inquiry-status]");
    var contextNode = form.querySelector("[data-nlfs-inquiry-context]");
    var button = form.querySelector('button[type="submit"]');
    var fields = Array.prototype.slice.call(form.querySelectorAll("[data-nlfs-lead-field]"));
    var expectedProjectContractId = runtimeConfig && runtimeConfig.identity && runtimeConfig.identity.project_contract_id;
    var scenes = runtimeConfig && runtimeConfig.experiences && Array.isArray(runtimeConfig.experiences.scenes) ? runtimeConfig.experiences.scenes : [];
    var experienceDecision = runtimeConfig && runtimeConfig.experiences && plain(runtimeConfig.experiences.decision) ? runtimeConfig.experiences.decision : {};
    if (!status || !contextNode || !button || !fields.length || typeof expectedProjectContractId !== "string" || !expectedProjectContractId) return function () {};
    var endpoint = safeSameOriginUrl(contract.endpoint, "/wp-json/nadlan/v1/lead");
    var send = typeof transport === "function" ? transport : function (url, options) { return window.fetch(url, options); };
    var controller = new AbortController();
    var activeRequest = null;
    var requestSequence = 0;
    var inquiryContext = null;
    function report(text, state) { status.textContent = text; status.dataset.state = state; }
    function contextMessage() {
      if (!inquiryContext) return "";
      return "הקשר בחירה המחשתית: " + inquiryContext.title + " [" + inquiryContext.id + "]; החלטה " + inquiryContext.decisionId
        + "; אסמכתאות " + inquiryContext.sourceRefs.join(", ") + "; מצב ראיות " + inquiryContext.evidenceLane
        + ". אין זו בחירת דירה, קומה, כיוון או מיקום מתקן מאומת.";
    }
    function consumeSpatialState(event) {
      var state = event && event.detail;
      var selected = state && state.selectedEntity;
      if (!plain(state) || state.schema !== "nadlan-spatial-decision-state/v1" || state.projectContractId !== expectedProjectContractId || state.historyVersion !== 1) return;
      if (selected === null) {
        inquiryContext = null;
        contextNode.dataset.contextState = "project";
        delete contextNode.dataset.contextSceneId;
        contextNode.textContent = "הפנייה מתייחסת לפרויקט כולו. בחירה המחשתית תצורף כהקשר בלבד, בלי דירה, קומה, כיוון או מיקום מומצאים.";
        return;
      }
      if (!plain(selected) || selected.type !== "scene" || typeof selected.id !== "string" || typeof selected.hotspotId !== "string"
        || ["verified", "illustrative"].indexOf(selected.evidenceLane) < 0) return;
      var scene = scenes.find(function (candidate) { return candidate && candidate.id === selected.id; });
      if (!scene || String(scene.model_hotspot_group || "") !== selected.hotspotId) return;
      var refs = Array.isArray(scene.placement_source_refs) ? scene.placement_source_refs.filter(function (id) { return typeof id === "string"; }) : [];
      inquiryContext = {
        id: selected.id,
        title: String(scene.title || selected.id),
        evidenceLane: selected.evidenceLane,
        decisionId: String(scene.mapping_owner_decision_id || experienceDecision.owner_decision_id || "not-supplied"),
        sourceRefs: refs
      };
      contextNode.dataset.contextState = "scene";
      contextNode.dataset.contextSceneId = selected.id;
      contextNode.textContent = "הקשר נוכחי: " + inquiryContext.title + " · " + inquiryContext.evidenceLane + " · החלטה " + inquiryContext.decisionId
        + " · אסמכתאות " + (refs.length ? refs.join(", ") : "לא סופקו") + ". ההקשר יישלח כהמחשה בלבד; שדות דירה, קומה וכיוון נשארים ריקים.";
    }
    root.addEventListener("nadlan:flagship-v3:state-change", consumeSpatialState, { signal: controller.signal });
    fields.forEach(function (field) { field.disabled = false; });
    button.disabled = false;
    button.removeAttribute("aria-disabled");
    report("הטופס מוכן. לא תישלח פנייה לפני הסכמה ולחיצה על שליחה.", "ready");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var name = String(data.get("name") || "").trim();
      var phone = String(data.get("phone") || "").trim();
      var email = String(data.get("email") || "").trim();
      var consent = data.get("consent") === "1";
      if (String(data.get("company") || "").trim()) return;
      var normalizedPhone = phone.replace(/[^0-9+]/g, "");
      if (name.length < 2 || (!phone && !email) || (phone && !/^\+?[0-9]{7,15}$/.test(normalizedPhone)) || !consent || !form.reportValidity()) {
        report("נדרשים שם, טלפון או אימייל, והסכמה פעילה להעברת הפנייה.", "error");
        return;
      }
      var typedMessage = String(data.get("message") || "").trim();
      var synchronizedContext = contextMessage();
      var payload = {
        source: contract.source,
        source_url: contract.source_url,
        project_slug: contract.project_slug,
        project_title: contract.project_title,
        project_wp_id: contract.card_id,
        wp_id: contract.card_id,
        card_id: contract.card_id,
        lang: contract.lang,
        name: name,
        phone: normalizedPhone,
        email: email,
        company: "",
        unit: "",
        floor: "",
        rooms: "",
        sqm: "",
        direction: "",
        status: "",
        consent: true,
        consent_version: contract.consent_version,
        consent_text: contract.consent_text,
        message: (typedMessage
          ? typedMessage + (synchronizedContext ? "\n\n" + synchronizedContext : "")
          : synchronizedContext || "בקשת מידע על פרויקט EINSTEIN TOWER; לא נבחרה דירה משום שאין מלאי מאומת.").slice(0, 4000)
      };
      button.disabled = true;
      report("שולחים את הפנייה…", "pending");
      if (activeRequest) activeRequest.abort();
      var requestController = new AbortController();
      activeRequest = requestController;
      var sequence = ++requestSequence;
      var timeout = window.setTimeout(function () { requestController.abort(); }, 12000);
      Promise.resolve(send(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload), signal: requestController.signal }))
        .then(function (response) { if (!response || !response.ok || typeof response.json !== "function") throw new Error("lead_failed"); return response.json(); })
        .then(function (data) { if (sequence !== requestSequence) return; if (!data || data.ok !== true) throw new Error("lead_rejected"); form.reset(); report("הפנייה נקלטה במערכת. אין בכך התחייבות למועד מענה או להעברה ליזם.", "success"); })
        .catch(function (error) { if (sequence !== requestSequence) return; report(error && error.name === "AbortError" ? "הפנייה לא נשלחה בזמן. אפשר לנסות שוב." : "הפנייה לא נשלחה. אפשר לנסות שוב.", "error"); })
        .finally(function () { window.clearTimeout(timeout); if (sequence === requestSequence) { activeRequest = null; button.disabled = false; } });
    }, { signal: controller.signal });
    form.dataset.nlfsLeadReady = "true";
    return function () {
      controller.abort();
      requestSequence += 1;
      if (activeRequest) activeRequest.abort();
      activeRequest = null;
      fields.forEach(function (field) { field.disabled = true; });
      button.disabled = true;
      button.setAttribute("aria-disabled", "true");
      delete form.dataset.nlfsLeadReady;
      report("הטופס אינו פעיל. אפשר להשתמש בקישור יצירת הקשר בלי להזין כאן פרטים.", "unavailable");
    };
  }

  function mountPrimaryActions(root, decision) {
    var interestButton = root.querySelector('[data-nlfs-primary-action="interest"]');
    var whatsappButton = root.querySelector('[data-nlfs-primary-action="whatsapp"]');
    var status = root.querySelector("[data-nlfs-primary-actions-status]");
    if (!interestButton || !whatsappButton || !status) return function () {};
    var actions = plain(decision) && plain(decision.primary_actions) ? decision.primary_actions : null;
    var interestContract = actions && actions.interest;
    var whatsappContract = actions && actions.whatsapp;
    var contractValid = plain(interestContract) && interestContract.mode === "adopt_existing" && interestContract.target === "#nl-form"
      && plain(whatsappContract) && whatsappContract.mode === "adopt_existing" && whatsappContract.selector === ".nlwa-float, [data-nl-whatsapp]"
      && interestButton.dataset.nlfsAdoptTarget === "#nl-form"
      && whatsappButton.dataset.nlfsAdoptSelector === ".nlwa-float, [data-nl-whatsapp]";
    var controller = new AbortController();
    var signal = controller.signal;
    var observer = null;
    var interestTarget = null;
    var whatsappTarget = null;
    function enable(button, enabled) {
      if (button.disabled !== !enabled) button.disabled = !enabled;
      var aria = enabled ? "false" : "true";
      if (button.getAttribute("aria-disabled") !== aria) button.setAttribute("aria-disabled", aria);
      var state = enabled ? "ready" : "unavailable";
      if (button.dataset.nlfsAdoptState !== state) button.dataset.nlfsAdoptState = state;
    }
    function report(text, state) {
      if (status.textContent !== text) status.textContent = text;
      if (status.dataset.state !== state) status.dataset.state = state;
    }
    function safeWhatsappTarget() {
      var candidates = Array.prototype.slice.call(document.querySelectorAll(".nlwa-float, [data-nl-whatsapp]")).filter(function (node) {
        return node && node.isConnected && node !== whatsappButton && !root.querySelector("[data-nlfs-primary-actions-status]").contains(node);
      });
      return candidates.find(function (node) {
        if (!node.matches("a[href]")) return typeof node.click === "function";
        try {
          var url = new URL(node.href, window.location.href);
          return url.protocol === "whatsapp:" || (url.protocol === "https:" && ["wa.me", "api.whatsapp.com"].indexOf(url.hostname) >= 0)
            || url.origin === window.location.origin;
        } catch (_error) { return false; }
      }) || null;
    }
    function reconcile() {
      if (!contractValid) {
        enable(interestButton, false); enable(whatsappButton, false);
        report("בקרי הקשר החתומים אינם זמינים; הפעולות נשארות כבויות ולא מוצג קישור חלופי מומצא.", "contract-unavailable");
        return;
      }
      interestTarget = document.getElementById("nl-form");
      whatsappTarget = safeWhatsappTarget();
      enable(interestButton, !!interestTarget);
      enable(whatsappButton, !!whatsappTarget);
      var state = interestTarget && whatsappTarget ? "ready" : interestTarget || whatsappTarget ? "partial" : "unavailable";
      var text = interestTarget && whatsappTarget
        ? "הפעולות מחוברות לבקרי הקשר הקיימים בעמוד."
        : interestTarget
          ? "טופס הפנייה מחובר; בקר WhatsApp הקיים אינו זמין כרגע."
          : whatsappTarget
            ? "WhatsApp מחובר; טופס הפנייה הקיים אינו זמין כרגע."
            : "בקרי הקשר הקיימים אינם זמינים כרגע; לא נוצר יעד חלופי.";
      report(text, state);
    }
    interestButton.addEventListener("click", function () {
      reconcile();
      if (!interestTarget || interestButton.disabled) return;
      var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      try { interestTarget.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" }); } catch (_error) { interestTarget.scrollIntoView(); }
      var focus = interestTarget.matches("input,select,textarea,button,a[href]") ? interestTarget : interestTarget.querySelector("input:not([disabled]),select:not([disabled]),textarea:not([disabled]),button:not([disabled]),a[href]");
      if (focus && typeof focus.focus === "function") {
        try { focus.focus({ preventScroll: true }); } catch (_error) { focus.focus(); }
      }
    }, { signal: signal });
    whatsappButton.addEventListener("click", function () {
      reconcile();
      if (!whatsappTarget || whatsappButton.disabled || typeof whatsappTarget.click !== "function") return;
      whatsappTarget.click();
    }, { signal: signal });
    if (window.MutationObserver) {
      observer = new MutationObserver(reconcile);
      observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["href", "hidden", "class"] });
    }
    reconcile();
    return function () {
      controller.abort();
      if (observer) observer.disconnect();
      enable(interestButton, false); enable(whatsappButton, false);
      report("הפעולות אינן פעילות כרגע.", "unavailable");
    };
  }

  function mountRouteCompatibility(root, links) {
    document.body.classList.add("nlfs-route-active");
    var header = document.querySelector(".nlpc-site-header");
    var toggle = header && header.querySelector(".nlpc-nav-toggle");
    var nav = header && header.querySelector(".nlpc-primary-nav");
    var a11y = document.getElementById("nla11y-btn");
    var stage = root.querySelector("[data-nlfs-protected-stage]");
    var observer = null;
    var layoutObserver = null;
    var navLinks = nav ? Array.prototype.slice.call(nav.querySelectorAll("a[href]")) : [];
    var navTabIndexes = navLinks.map(function (link) { return link.hasAttribute("tabindex") ? link.getAttribute("tabindex") : null; });
    function restoreNavTabIndexes() {
      navLinks.forEach(function (link, index) { if (navTabIndexes[index] === null) link.removeAttribute("tabindex"); else link.setAttribute("tabindex", navTabIndexes[index]); });
    }
    function syncNav() {
      if (header && toggle && nav) {
        var compact = window.matchMedia && window.matchMedia("(max-width: 760px)").matches;
        var open = compact && toggle.getAttribute("aria-expanded") === "true";
        header.dataset.nlfsRouteNav = compact ? (open ? "open" : "closed") : "desktop";
        if (open || !compact) restoreNavTabIndexes();
        else navLinks.forEach(function (link) { link.setAttribute("tabindex", "-1"); });
      }
      if (a11y && stage) {
        document.documentElement.style.setProperty("--nlfs-stage-after", Math.ceil(stage.getBoundingClientRect().bottom + window.scrollY + 12) + "px");
        a11y.dataset.nlfsOutsideStage = "true";
      }
    }
    if (toggle && window.MutationObserver) {
      observer = new MutationObserver(syncNav);
      observer.observe(toggle, { attributes: true, attributeFilter: ["aria-expanded"] });
    }
    if (stage && window.ResizeObserver) {
      layoutObserver = new ResizeObserver(syncNav);
      layoutObserver.observe(stage);
      layoutObserver.observe(root);
    }
    syncNav();
    window.addEventListener("resize", syncNav);
    var discovery = document.querySelector('a.nlfb-i[data-k="model"][href="#"]');
    var discoveryHref = discovery ? discovery.getAttribute("href") : null;
    var discoveryTo = discovery ? discovery.getAttribute("data-to") : null;
    if (discovery) {
      discovery.setAttribute("href", "#nlfs-4867-showroom-title");
      discovery.setAttribute("data-to", "#nlfs-4867-showroom-title");
      discovery.dataset.nlfsEinsteinStageLink = "true";
    }
    var viewDiscovery = document.querySelector('.nlfb-i[data-k="view"]');
    var viewSnapshot = viewDiscovery ? {
      className: viewDiscovery.className,
      role: viewDiscovery.getAttribute("role"),
      tabindex: viewDiscovery.getAttribute("tabindex"),
      ariaLabel: viewDiscovery.getAttribute("aria-label"),
      label: viewDiscovery.querySelector("b") ? viewDiscovery.querySelector("b").textContent : "",
      subcopy: viewDiscovery.querySelector("s") ? viewDiscovery.querySelector("s").textContent : ""
    } : null;
    function openViewFromDiscovery(event) {
      if (event && event.type === "keydown" && event.key !== "Enter" && event.key !== " ") return;
      if (event) event.preventDefault();
      root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:open-tool", {
        bubbles: false,
        detail: { toolId: "view", trigger: viewDiscovery }
      }));
    }
    if (viewDiscovery) {
      viewDiscovery.classList.remove("off");
      viewDiscovery.setAttribute("role", "button");
      viewDiscovery.setAttribute("tabindex", "0");
      viewDiscovery.setAttribute("aria-label", "פתיחת מבט חלון לווייני 360 מעלות של איינשטיין");
      viewDiscovery.dataset.nlfsEinsteinViewAction = "true";
      if (viewDiscovery.querySelector("b")) viewDiscovery.querySelector("b").textContent = "מבט חלון 360°";
      if (viewDiscovery.querySelector("s")) viewDiscovery.querySelector("s").textContent = "לוויין חי בגובה המחשה; ללא שיוך לדירה";
      viewDiscovery.addEventListener("click", openViewFromDiscovery);
      viewDiscovery.addEventListener("keydown", openViewFromDiscovery);
    }
    var earthDiscovery = document.querySelector('.nlfb-i[data-k="earth"]');
    var earthLink = null;
    var earthLabel = earthDiscovery && earthDiscovery.querySelector("b") ? earthDiscovery.querySelector("b").textContent : "";
    var earthSubcopy = earthDiscovery && earthDiscovery.querySelector("s") ? earthDiscovery.querySelector("s").textContent : "";
    if (earthDiscovery && links && links.earthUrl && links.earthContextLabel && earthDiscovery.parentNode) {
      earthLink = document.createElement("a");
      Array.prototype.slice.call(earthDiscovery.attributes).forEach(function (attribute) { earthLink.setAttribute(attribute.name, attribute.value); });
      earthLink.classList.remove("off");
      earthLink.href = links.earthUrl;
      earthLink.setAttribute("aria-label", "פתיחת סצנת Earth של שדה דב הסמוך; זהו הקשר רובעי ולא מיקום איינשטיין");
      earthLink.dataset.nlfsEinsteinEarthAction = "true";
      while (earthDiscovery.firstChild) earthLink.appendChild(earthDiscovery.firstChild);
      if (earthLink.querySelector("b")) earthLink.querySelector("b").textContent = "Earth · שדה דב הסמוך";
      if (earthLink.querySelector("s")) earthLink.querySelector("s").textContent = links.earthContextLabel;
      earthDiscovery.parentNode.replaceChild(earthLink, earthDiscovery);
    }
    return function () {
      if (observer) observer.disconnect();
      if (layoutObserver) layoutObserver.disconnect();
      window.removeEventListener("resize", syncNav);
      if (header) delete header.dataset.nlfsRouteNav;
      restoreNavTabIndexes();
      if (a11y) delete a11y.dataset.nlfsOutsideStage;
      if (discovery) {
        discovery.setAttribute("href", discoveryHref || "#");
        if (discoveryTo === null) discovery.removeAttribute("data-to"); else discovery.setAttribute("data-to", discoveryTo);
        delete discovery.dataset.nlfsEinsteinStageLink;
      }
      if (viewDiscovery && viewSnapshot) {
        viewDiscovery.removeEventListener("click", openViewFromDiscovery);
        viewDiscovery.removeEventListener("keydown", openViewFromDiscovery);
        viewDiscovery.className = viewSnapshot.className;
        if (viewSnapshot.role === null) viewDiscovery.removeAttribute("role"); else viewDiscovery.setAttribute("role", viewSnapshot.role);
        if (viewSnapshot.tabindex === null) viewDiscovery.removeAttribute("tabindex"); else viewDiscovery.setAttribute("tabindex", viewSnapshot.tabindex);
        if (viewSnapshot.ariaLabel === null) viewDiscovery.removeAttribute("aria-label"); else viewDiscovery.setAttribute("aria-label", viewSnapshot.ariaLabel);
        if (viewDiscovery.querySelector("b")) viewDiscovery.querySelector("b").textContent = viewSnapshot.label;
        if (viewDiscovery.querySelector("s")) viewDiscovery.querySelector("s").textContent = viewSnapshot.subcopy;
        delete viewDiscovery.dataset.nlfsEinsteinViewAction;
      }
      if (earthLink && earthLink.parentNode) {
        while (earthLink.firstChild) earthDiscovery.appendChild(earthLink.firstChild);
        if (earthDiscovery.querySelector("b")) earthDiscovery.querySelector("b").textContent = earthLabel;
        if (earthDiscovery.querySelector("s")) earthDiscovery.querySelector("s").textContent = earthSubcopy;
        earthLink.parentNode.replaceChild(earthDiscovery, earthLink);
      }
      document.documentElement.style.removeProperty("--nlfs-stage-after");
      document.body.classList.remove("nlfs-route-active");
    };
  }

  function create(root, config, options) {
    if (!root || root.dataset.projectContractId !== PROJECT_ID || !plain(config) || !plain(config.integrations)) throw new Error("Einstein integration contract missing.");
    var view = config.integrations.window_view;
    var lead = config.integrations.lead;
    var unit = config.integrations.unit_bridge;
    if (!validView(view) || !validLead(lead) || !validUnitBridge(unit) || !validCoTourRuntime(config.integrations.co_tour)
      || !safeSitePath(config.integrations.design_url, "/tour/designer/")
      || !safeSitePath(config.integrations.district_tour_url, "/tour/sde-dov/")
      || !safeSitePath(config.integrations.earth_url, "/earth/sde-dov/")
      || config.integrations.earth_context_label !== "שדה דב הסמוך — הקשר רובעי, לא מיקום איינשטיין") throw new Error("Einstein integration contract rejected.");
    var cleanups = [
      mountRouteCompatibility(root, {
        earthUrl: config.integrations.earth_url,
        earthContextLabel: config.integrations.earth_context_label
      }),
      mountLeadForm(root, lead, options && options.transport, config),
      mountPrimaryActions(root, config.decision_experience)
    ];
    var unitMapAdapter = null;
    var canonicalMap = null;
    var pendingMapState = null;
    var mapBeforeSelection = null;
    var selectedEntity = null;
    var mapElementSnapshot = null;
    var mapElementObserver = null;
    var mapResizeFrames = [];
    var mapReadinessCleanup = null;
    var coTourCapability = Object.freeze({
      schema: "nadlan-einstein-cotour-capability/v1",
      state: "ready_dedicated_adapter",
      enabled: true,
      transport: "same_origin_ephemeral_rest",
      privateEngineClosuresUsed: false,
      roomIdentifiersInUrl: false,
      hostSecretInUrlOrDom: false,
      ttlSeconds: 600
    });
    function unavailableMapState() {
      return { schema: MAP_STATE_SCHEMA, available: false, camera: null, selectedEntityId: selectedEntity ? selectedEntity.id : "", correlationState: selectedEntity ? "unavailable-no-source" : "idle" };
    }
    function currentMapState() {
      return unitMapAdapter && typeof unitMapAdapter.getState === "function" ? unitMapAdapter.getState() : unavailableMapState();
    }
    function notifyMapState() {
      root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:map-state-change", {
        bubbles: false,
        detail: clone(currentMapState())
      }));
    }
    function scheduleCanonicalResize() {
      if (!canonicalMap || typeof canonicalMap.resize !== "function") return;
      mapResizeFrames.push(window.requestAnimationFrame(function () {
        try { canonicalMap.resize(); } catch (_error) {}
        mapResizeFrames.push(window.requestAnimationFrame(function () { try { canonicalMap.resize(); } catch (_error) {} }));
      }));
    }
    function canonicalMapIsReady() {
      if (!canonicalMap) return false;
      try {
        if (typeof canonicalMap.loaded === "function" && canonicalMap.loaded() !== true) return false;
        if (typeof canonicalMap.isStyleLoaded === "function" && canonicalMap.isStyleLoaded() !== true) return false;
        if (typeof canonicalMap.areTilesLoaded === "function" && canonicalMap.areTilesLoaded() !== true) return false;
        return true;
      } catch (_error) { return false; }
    }
    function paintCanonicalMapReadiness(state) {
      var mount = root.querySelector("[data-nlfs-map-mount]");
      if (!mount) return;
      var ready = state === "ready";
      mount.setAttribute("aria-busy", ready ? "false" : state === "error" ? "false" : "true");
      root.dataset.canonicalMapReadiness = state;
      var status = mount.querySelector("[data-nlfs-map-slot-status]");
      if (status) status.textContent = ready
        ? "מפת הסביבה מחוברת למודל. תנועה לפי בחירה תתבצע רק עם קואורדינטות מאומתות."
        : state === "error"
          ? "מפת הסביבה לא הושלמה. המודל נשאר זמין, ולא תוצג תנועת מפה מדומה."
          : "מפת הסביבה נטענת וממתינה לאימות הסגנון והאריחים.";
    }
    function checkCanonicalMapReadiness() {
      paintCanonicalMapReadiness(canonicalMapIsReady() ? "ready" : "loading");
    }
    function bindCanonicalMapReadiness() {
      if (mapReadinessCleanup) { mapReadinessCleanup(); mapReadinessCleanup = null; }
      paintCanonicalMapReadiness("loading");
      if (!canonicalMap || typeof canonicalMap.on !== "function" || typeof canonicalMap.off !== "function") {
        paintCanonicalMapReadiness("error");
        return;
      }
      var boundMap = canonicalMap;
      var check = function () { checkCanonicalMapReadiness(); };
      var fail = function () { paintCanonicalMapReadiness("error"); };
      ["load", "idle", "styledata", "sourcedata"].forEach(function (eventName) { boundMap.on(eventName, check); });
      boundMap.on("error", fail);
      mapReadinessCleanup = function () {
        ["load", "idle", "styledata", "sourcedata"].forEach(function (eventName) { try { boundMap.off(eventName, check); } catch (_error) {} });
        try { boundMap.off("error", fail); } catch (_error) {}
      };
      checkCanonicalMapReadiness();
    }
    function adoptCanonicalMapElement() {
      var mount = root.querySelector("[data-nlfs-map-mount]");
      var element = document.getElementById("nlpjx-map") || document.querySelector("[data-nlpjx-map]");
      if (!mount || !element || element === mount || element.contains(mount)) return false;
      if (!mount.contains(element)) {
        if (!mapElementSnapshot) mapElementSnapshot = { element: element, parent: element.parentNode, next: element.nextSibling };
        mount.appendChild(element);
      }
      root.dataset.canonicalMapElementState = "adopted";
      if (mapElementObserver) { mapElementObserver.disconnect(); mapElementObserver = null; }
      scheduleCanonicalResize();
      checkCanonicalMapReadiness();
      return true;
    }
    function watchCanonicalMapElement() {
      if (adoptCanonicalMapElement() || mapElementObserver || !window.MutationObserver) return;
      mapElementObserver = new MutationObserver(adoptCanonicalMapElement);
      mapElementObserver.observe(document.body, { childList: true, subtree: true });
    }
    function restoreCanonicalMapElement() {
      if (mapElementObserver) { mapElementObserver.disconnect(); mapElementObserver = null; }
      if (mapReadinessCleanup) { mapReadinessCleanup(); mapReadinessCleanup = null; }
      mapResizeFrames.splice(0).forEach(function (frame) { window.cancelAnimationFrame(frame); });
      if (mapElementSnapshot && mapElementSnapshot.element && mapElementSnapshot.parent) {
        var snapshot = mapElementSnapshot;
        if (snapshot.next && snapshot.next.parentNode === snapshot.parent) snapshot.parent.insertBefore(snapshot.element, snapshot.next);
        else snapshot.parent.appendChild(snapshot.element);
      }
      mapElementSnapshot = null;
      delete root.dataset.canonicalMapElementState;
      try { if (canonicalMap && typeof canonicalMap.resize === "function") canonicalMap.resize(); } catch (_error) {}
    }
    function bindCanonicalMap() {
      if (canonicalMap === window.NLPJX_MAP && unitMapAdapter) return;
      if (unitMapAdapter) unitMapAdapter.destroy();
      canonicalMap = window.NLPJX_MAP || null;
      unitMapAdapter = createUnitMapAdapter(canonicalMap, {
        lat: view.lat,
        lng: view.lng,
        verification_state: "source_cited",
        source_ids: view.location_source_ids
      });
      root.dataset.unitMapAdapterState = unitMapAdapter ? "bound" : "unavailable";
      watchCanonicalMapElement();
      bindCanonicalMapReadiness();
      if (unitMapAdapter && pendingMapState) {
        if (unitMapAdapter.restoreState(pendingMapState)) pendingMapState = null;
      }
      if (unitMapAdapter && selectedEntity) unitMapAdapter.selectEntity(selectedEntity);
      notifyMapState();
    }
    document.addEventListener("nlpjx:map", bindCanonicalMap);
    watchCanonicalMapElement();
    if (window.NLPJX_MAP) bindCanonicalMap();
    function unitSelected(event) {
      var status = root.querySelector("[data-nlfs-unit-bridge-status]");
      if (!unit.production_enabled) {
        if (status) status.textContent = "אין מלאי דירות מאומת; לא הופעל מבט דירה.";
        root.dataset.unitBridgeState = "inventory-unavailable";
        return;
      }
      root.dataset.unitBridgeState = bridgeVerifiedUnit(unit, unitMapAdapter, event.detail) ? "invoked" : "rejected";
      notifyMapState();
    }
    root.addEventListener("nadlan:flagship-v3:unit-selected", unitSelected);
    return Object.freeze({
      mountWindowView: function (host, stateChanged) { return createWindowView(host, view, stateChanged); },
      selectEntity: function (entity) {
        if (!plain(entity) || entity.schema !== SPATIAL_ENTITY_SCHEMA || typeof entity.id !== "string" || !entity.id || entity.id.length > 128
          || ["verified", "illustrative", "unavailable"].indexOf(entity.evidenceLane) < 0 || entity.decisionGrade !== false) return false;
        if (!selectedEntity && unitMapAdapter) mapBeforeSelection = unitMapAdapter.getState();
        selectedEntity = clone(entity);
        root.dataset.mapCorrelationState = unitMapAdapter && unitMapAdapter.selectEntity(selectedEntity) ? "correlated" : "unavailable-no-source";
        notifyMapState();
        return root.dataset.mapCorrelationState === "correlated";
      },
      clearSelection: function (restoreCamera) {
        selectedEntity = null;
        if (unitMapAdapter) {
          unitMapAdapter.clearSelection();
          if (restoreCamera !== false && mapBeforeSelection) unitMapAdapter.restoreState(mapBeforeSelection);
        }
        mapBeforeSelection = null;
        root.dataset.mapCorrelationState = "idle";
        notifyMapState();
        return true;
      },
      getState: function () {
        return {
          schema: INTEGRATION_STATE_SCHEMA,
          map: clone(currentMapState()),
          selectedEntityId: selectedEntity ? selectedEntity.id : "",
          coTour: clone(coTourCapability)
        };
      },
      restoreState: function (value) {
        if (!plain(value) || value.schema !== INTEGRATION_STATE_SCHEMA || !plain(value.map)) return false;
        pendingMapState = clone(value.map);
        if (!unitMapAdapter) return true;
        var restored = unitMapAdapter.restoreState(pendingMapState);
        if (restored) pendingMapState = null;
        notifyMapState();
        return restored;
      },
      getCapabilities: function () {
        return {
          schema: "nadlan-einstein-integration-capabilities/v1",
          canonicalMap: unitMapAdapter && typeof unitMapAdapter.getCapabilities === "function" ? unitMapAdapter.getCapabilities() : {
            schema: MAP_ADAPTER_SCHEMA,
            canonicalHandleAdopted: false,
            canonicalHandleReplaced: false,
            privateEngineClosuresAssumedPublic: false,
            beamMechanismMutated: false,
            panRequiresSourceCitedCoordinates: true,
            coneRequiresVerifiedBearing: true
          },
          coTour: clone(coTourCapability)
        };
      },
      destroy: function () {
        root.removeEventListener("nadlan:flagship-v3:unit-selected", unitSelected);
        document.removeEventListener("nlpjx:map", bindCanonicalMap);
        if (unitMapAdapter) unitMapAdapter.destroy();
        restoreCanonicalMapElement();
        unitMapAdapter = null;
        canonicalMap = null;
        pendingMapState = null;
        mapBeforeSelection = null;
        selectedEntity = null;
        cleanups.splice(0).reverse().forEach(function (cleanup) { try { cleanup(); } catch (_error) {} });
      }
    });
  }

  window.NadlanFlagshipIntegrations = Object.freeze({
    create: create,
    bridgeVerifiedUnit: bridgeVerifiedUnit,
    createUnitMapAdapter: createUnitMapAdapter,
    validView: validView,
    validLead: validLead,
    validUnitBridge: validUnitBridge,
    MAP_ADAPTER_SCHEMA: MAP_ADAPTER_SCHEMA,
    MAP_STATE_SCHEMA: MAP_STATE_SCHEMA,
    INTEGRATION_STATE_SCHEMA: INTEGRATION_STATE_SCHEMA,
    SPATIAL_ENTITY_SCHEMA: SPATIAL_ENTITY_SCHEMA
  });
})();
