/* NadLan flagship v3 bootstrap. First-party viewer with governed Einstein-only integrations. */
(function () {
  "use strict";

  var instances = new Map();
  var SPATIAL_STATE_SCHEMA = "nadlan-spatial-decision-state/v1";
  var SPATIAL_HISTORY_SCHEMA = "nadlan-flagship-spatial-history/v1";
  var SPATIAL_HISTORY_KEY = "__nadlanFlagshipSpatialHistory";
  var SPATIAL_ENTITY_SCHEMA = "nadlan-flagship-spatial-entity/v1";
  var LIGHTING_SCHEMA = "nadlan-flagship-viewer-lighting/v1";
  var DEEP_LINK_PARAMETER = "nlfs";

  function plain(value) { return !!value && typeof value === "object" && !Array.isArray(value); }
  function finite(value) { return typeof value === "number" && Number.isFinite(value); }
  function exactKeys(value, keys) {
    return plain(value) && Object.keys(value).sort().join("\n") === keys.slice().sort().join("\n");
  }
  function clone(value) {
    if (value === undefined) return undefined;
    if (typeof structuredClone === "function") return structuredClone(value);
    return JSON.parse(JSON.stringify(value));
  }
  function encodePortableState(value) {
    var json = JSON.stringify(value);
    if (json.length > 65536) throw new Error("Portable state is too large.");
    var bytes = new TextEncoder().encode(json);
    var binary = "";
    for (var index = 0; index < bytes.length; index += 1) binary += String.fromCharCode(bytes[index]);
    return window.btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
  }
  function decodePortableState(value) {
    if (typeof value !== "string" || !value || value.length > 65536 || !/^[A-Za-z0-9_-]+$/.test(value)) return null;
    try {
      var padded = value.replace(/-/g, "+").replace(/_/g, "/");
      while (padded.length % 4) padded += "=";
      var binary = window.atob(padded);
      var bytes = new Uint8Array(binary.length);
      for (var index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
      return JSON.parse(new TextDecoder().decode(bytes));
    } catch (_error) { return null; }
  }

  function readConfig(root) {
    var node = root.querySelector("[data-nlfs-config]");
    if (!node) return null;
    try {
      var config = JSON.parse(node.textContent || "");
      if (!config || config.schema !== "nadlan-flagship-runtime/v3") return null;
      if (!config.capabilities || config.capabilities.content_writes_enabled !== false) return null;
      if (config.capabilities.lead_submission !== true || config.capabilities.comment_submission !== false || config.capabilities.inventory_selection !== false) return null;
      if (!config.integrations || !config.integrations.window_view || !config.integrations.lead || !config.integrations.unit_bridge) return null;
      if (!config.inventory || config.inventory.decision_grade !== false) return null;
      if (!config.experiences || config.experiences.schema !== "nadlan-project-experience-registry/v1") return null;
      if (!Array.isArray(config.experiences.scenes) || !config.experiences.scenes.length) return null;
      return config;
    } catch (_error) {
      return null;
    }
  }

  function mount(root) {
    if (!root || instances.has(root)) return;
    var config = readConfig(root);
    var model = root.querySelector("[data-nlfs-model]");
    var poster = root.querySelector("[data-nlfs-poster]");
    var status = root.querySelector("[data-nlfs-model-status]");
    var playground = root.querySelector("[data-nlfs-playground]");
    if (!config || !model || !poster || !status || !playground) {
      root.hidden = true;
      return;
    }

    var controller = new AbortController();
    var signal = controller.signal;
    var viewer = null;
    var visualInstance = null;
    var integrationInstance = null;
    var scenes = new Map();
    config.experiences.scenes.forEach(function (scene) { scenes.set(scene.id, scene); });
    var saveData = !!(navigator.connection && navigator.connection.saveData);
    var lodLoad = null;
    var hdLoad = null;
    var lodLoaded = false;
    var hdLoaded = false;
    var modelReady = false;
    var modelFailed = false;
    var posterState = "loading";
    var toolsAvailable = false;
    var visibilityObserver = null;
    var modelBearing = root.querySelector("[data-nlfs-model-bearing]");
    var selectedScene = null;
    var selectionTrigger = null;
    var selectionNode = null;
    var selectionNodeInjected = false;
    var shareButton = null;
    var shareStatus = null;
    var shareFallback = null;
    var pendingModelState = null;
    var pendingSpatialRollback = null;
    var spatialHistoryRevision = 0;
    var spatialHistoryRestoring = false;
    var stateChangeFrame = 0;

    function ensureSelectionSurface() {
      var node = root.querySelector("[data-nlfs-selection-card]");
      if (!node) {
        node = document.createElement("section");
        node.className = "nlfs__selection";
        node.dataset.nlfsSelectionCard = "";
        node.dataset.selectionState = "idle";
        node.hidden = true;
        node.tabIndex = -1;
        node.setAttribute("role", "region");
        node.setAttribute("aria-live", "polite");
        node.setAttribute("aria-label", "בחירה מתוך מודל ההמחשה");
        node.innerHTML = '<button type="button" data-nlfs-selection-back>← חזרה לבניין</button><div class="nlfs__selection-copy"><span data-nlfs-selection-truth></span><h3 data-nlfs-selection-title></h3><p data-nlfs-selection-summary></p><p data-nlfs-selection-map-state role="status"></p></div><div data-nlfs-selection-actions></div>';
        var insertion = root.querySelector(".nlfs__controls") || root.querySelector("[data-nlfs-protected-stage]");
        if (insertion && insertion.parentNode) insertion.parentNode.insertBefore(node, insertion.nextSibling);
        else playground.parentNode.insertBefore(node, playground);
        selectionNodeInjected = true;
      }
      if (!node.hasAttribute("tabindex")) node.tabIndex = -1;
      var actions = node.querySelector("[data-nlfs-selection-actions]");
      if (actions && !actions.querySelector("[data-nlfs-selection-open]")) {
        var open = document.createElement("button");
        open.type = "button";
        open.dataset.nlfsSelectionOpen = "";
        open.textContent = "לפתיחת חומר ההמחשה";
        actions.appendChild(open);
      }
      return node;
    }

    selectionNode = ensureSelectionSurface();

    function validSourceIds(value) {
      return Array.isArray(value) && value.length > 0 && value.length <= 32 && value.every(function (id, index) {
        return typeof id === "string" && /^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/.test(id) && value.indexOf(id) === index;
      });
    }

    function governedMapPosition(scene) {
      var value = scene && scene.map_position;
      if (!plain(value) || (value.verification_state !== "verified" && value.verification_state !== "source_cited")
        || !finite(value.lat) || Math.abs(value.lat) > 90 || !finite(value.lng) || Math.abs(value.lng) > 180
        || !validSourceIds(value.source_ids)) return null;
      return { lat: value.lat, lng: value.lng, verification_state: value.verification_state, source_ids: value.source_ids.slice() };
    }

    function sceneEntity(scene) {
      var mapPosition = governedMapPosition(scene);
      var sourceIds = Array.isArray(scene.source_ids) ? scene.source_ids.filter(function (id) { return typeof id === "string"; }) : [];
      var sourceCited = scene.source_cited_mapping === true && validSourceIds(sourceIds);
      var entity = {
        schema: SPATIAL_ENTITY_SCHEMA,
        type: "scene",
        id: String(scene.id),
        sceneId: String(scene.id),
        hotspotId: String(scene.model_hotspot_group || ""),
        kind: String(scene.kind || ""),
        evidenceLane: sourceCited ? "verified" : "illustrative",
        sourceIds: sourceIds,
        mapPosition: mapPosition,
        decisionGrade: false
      };
      if (scene.bearing_state === "verified" && finite(scene.bearing) && scene.bearing >= 0 && scene.bearing < 360 && validSourceIds(scene.bearing_source_ids)) {
        entity.bearing_state = "verified";
        entity.bearing = scene.bearing;
        entity.bearing_source_ids = scene.bearing_source_ids.slice();
      }
      return entity;
    }

    function selectedHistoryState(returnMode) {
      return {
        schema: SPATIAL_HISTORY_SCHEMA,
        projectContractId: config.identity.project_contract_id,
        revision: ++spatialHistoryRevision,
        selectedSceneId: selectedScene ? selectedScene.id : "",
        returnMode: returnMode === "back" ? "back" : "local"
      };
    }

    function validSpatialHistory(value) {
      return plain(value) && value.schema === SPATIAL_HISTORY_SCHEMA && value.projectContractId === config.identity.project_contract_id
        && Number.isSafeInteger(value.revision) && value.revision > 0 && typeof value.selectedSceneId === "string"
        && (value.returnMode === "back" || value.returnMode === "local")
        && (value.selectedSceneId === "" || scenes.has(value.selectedSceneId));
    }

    function currentSpatialHistory() {
      var value = window.history && plain(window.history.state) ? window.history.state[SPATIAL_HISTORY_KEY] : null;
      if (!validSpatialHistory(value)) return null;
      spatialHistoryRevision = Math.max(spatialHistoryRevision, value.revision);
      return value;
    }

    function writeSpatialHistory(method, returnMode) {
      if (spatialHistoryRestoring || !window.history || typeof window.history[method] !== "function") return false;
      try {
        var current = plain(window.history.state) ? clone(window.history.state) : {};
        current[SPATIAL_HISTORY_KEY] = selectedHistoryState(returnMode);
        window.history[method](current, "", window.location.href);
        return true;
      } catch (_error) { return false; }
    }

    function compactSelectionState() {
      return selectedScene ? {
        type: "scene",
        id: selectedScene.id,
        hotspotId: selectedScene.model_hotspot_group || "",
        evidenceLane: sceneEntity(selectedScene).evidenceLane
      } : null;
    }

    function captureSpatialState() {
      var modelState = viewer && typeof viewer.getState === "function" ? viewer.getState() : null;
      var mapState = integrationInstance && typeof integrationInstance.getState === "function" ? integrationInstance.getState() : null;
      var mediaState = visualInstance && typeof visualInstance.getState === "function" ? visualInstance.getState() : null;
      return {
        schema: SPATIAL_STATE_SCHEMA,
        projectContractId: config.identity.project_contract_id,
        historyVersion: 1,
        selectedEntity: compactSelectionState(),
        model: modelState,
        map: mapState,
        media: mediaState
      };
    }

    function scheduleStateChange() {
      if (stateChangeFrame) return;
      stateChangeFrame = window.requestAnimationFrame(function () {
        stateChangeFrame = 0;
        var state;
        try { state = captureSpatialState(); } catch (_error) { return; }
        root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:state-change", { bubbles: true, detail: clone(state) }));
      });
    }

    function updateStatus(value) { status.textContent = value; }
    function captureModelState() {
      if (!viewer || typeof viewer.getState !== "function") throw new Error("The governed model state is unavailable.");
      return viewer.getState();
    }
    function restoreModelState(state) {
      if (!viewer || !state || typeof viewer.setState !== "function") throw new Error("The governed model state cannot be restored.");
      return viewer.setState(state);
    }
    function syncVisualHistory() {
      if (visualInstance && typeof visualInstance.syncHistory === "function") visualInstance.syncHistory();
      scheduleStateChange();
    }
    function paintSelection(scene) {
      if (!selectionNode || !scene) return;
      var entity = sceneEntity(scene);
      var title = selectionNode.querySelector("[data-nlfs-selection-title]");
      var summary = selectionNode.querySelector("[data-nlfs-selection-summary]");
      var disclosure = selectionNode.querySelector("[data-nlfs-selection-disclosure]");
      var evidence = selectionNode.querySelector("[data-nlfs-selection-truth]");
      var mapStatus = selectionNode.querySelector("[data-nlfs-selection-map-state]");
      var open = selectionNode.querySelector("[data-nlfs-selection-open]");
      var decisionNode = selectionNode.querySelector("[data-nlfs-selection-decision]");
      var effectiveNode = selectionNode.querySelector("[data-nlfs-selection-effective]");
      var sourcesNode = selectionNode.querySelector("[data-nlfs-selection-sources]");
      var confidenceNode = selectionNode.querySelector("[data-nlfs-selection-confidence]");
      var basisNode = selectionNode.querySelector("[data-nlfs-selection-basis]");
      var limitationNode = selectionNode.querySelector("[data-nlfs-selection-limitation]");
      if (title) title.textContent = scene.title || "חומר המחשה";
      if (summary) summary.textContent = scene.summary || "";
      if (evidence) evidence.textContent = entity.evidenceLane === "verified" ? "מיפוי מצוטט למקור" : "המחשה מאושרת · לא מיקום רשמי";
      if (disclosure) disclosure.textContent = entity.evidenceLane === "verified"
        ? "הבחירה נשארת ליד הבניין והמפה. החומר העמוק נפתח רק לאחר פעולה מפורשת."
        : "נקודת העניין מסמנת אזור המחשה בלבד; היא אינה מוכיחה דירה, קומה, חזית, כיוון או מיקום מתקן רשמי.";
      if (mapStatus) mapStatus.textContent = entity.mapPosition
        ? "לנקודה זו קיימות קואורדינטות מצוטטות; מפת האזור יכולה לעבור אליהן."
        : "אין לנקודה קואורדינטות מצוטטות, ולכן המפה אינה מוזזת ולא מוצג כיוון מומצא.";
      if (open) {
        open.textContent = scene.open_label || "לפתיחת חומר ההמחשה";
        open.dataset.nlfsSelectionScene = scene.id;
      }
      var experienceDecision = plain(config.experiences && config.experiences.decision) ? config.experiences.decision : {};
      var sourceRefs = Array.isArray(scene.placement_source_refs) ? scene.placement_source_refs : Array.isArray(scene.source_ids) ? scene.source_ids : [];
      var confidence = plain(scene.placement_confidence) ? scene.placement_confidence : {};
      if (decisionNode) decisionNode.textContent = String(scene.mapping_owner_decision_id || experienceDecision.owner_decision_id || "לא סופק");
      if (effectiveNode) effectiveNode.textContent = String(experienceDecision.effective_at || "לא סופק");
      if (sourcesNode) sourcesNode.textContent = sourceRefs.length ? sourceRefs.join(", ") : "לא סופק מקור מרחבי";
      if (confidenceNode) confidenceNode.textContent = "אזור " + Math.round(100 * Number(confidence.zone || 0)) + "% · נקודה " + Math.round(100 * Number(confidence.exact_point || 0)) + "%";
      if (basisNode) basisNode.textContent = String(scene.placement_basis || "המחשה שאושרה להצגה; לא נמסר בסיס מרחבי מאומת.");
      if (limitationNode) limitationNode.textContent = String(scene.placement_ambiguity || "No verified unit, floor, bearing or exact facility coordinate is supplied.");
      selectionNode.dataset.selectedSceneId = scene.id;
      selectionNode.dataset.selectedHotspotId = entity.hotspotId;
      selectionNode.dataset.evidenceLane = entity.evidenceLane;
      selectionNode.dataset.selectionState = "selected";
      selectionNode.hidden = false;
      root.dataset.selectedEntityId = scene.id;
      root.querySelectorAll("[data-nlfs-model-hotspots] [data-nlfs-scene]").forEach(function (hotspot) {
        hotspot.setAttribute("aria-pressed", hotspot.dataset.nlfsSceneGroup === entity.hotspotId ? "true" : "false");
      });
    }
    function selectSceneInPlace(scene, trigger, options) {
      if (!scene || !scenes.has(scene.id)) return false;
      var previousId = selectedScene ? selectedScene.id : "";
      if (options && options.history === "push" && previousId !== scene.id && visualInstance && typeof visualInstance.syncHistory === "function") {
        visualInstance.syncHistory();
      }
      selectedScene = scene;
      if (trigger && trigger.nodeType === 1 && trigger.isConnected) selectionTrigger = trigger;
      paintSelection(scene);
      var entity = sceneEntity(scene);
      if (integrationInstance && typeof integrationInstance.selectEntity === "function") integrationInstance.selectEntity(entity);
      if (options && options.focus === true && selectionNode) {
        try { selectionNode.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "auto" }); } catch (_scrollError) { selectionNode.scrollIntoView(); }
        try { selectionNode.focus({ preventScroll: true }); } catch (_error) { selectionNode.focus(); }
      }
      if (options && options.history === "push" && previousId !== scene.id) writeSpatialHistory("pushState", "back");
      else if (options && options.history === "replace") writeSpatialHistory("replaceState", "local");
      scheduleStateChange();
      return true;
    }
    function clearSelection(focusTrigger, restoreMap) {
      var trigger = selectionTrigger;
      selectedScene = null;
      selectionTrigger = null;
      if (selectionNode) {
        selectionNode.hidden = true;
        delete selectionNode.dataset.selectedSceneId;
        delete selectionNode.dataset.selectedHotspotId;
        delete selectionNode.dataset.evidenceLane;
        selectionNode.dataset.selectionState = "idle";
      }
      delete root.dataset.selectedEntityId;
      root.querySelectorAll("[data-nlfs-model-hotspots] [data-nlfs-scene]").forEach(function (hotspot) { hotspot.setAttribute("aria-pressed", "false"); });
      if (integrationInstance && typeof integrationInstance.clearSelection === "function") integrationInstance.clearSelection(restoreMap !== false);
      if (focusTrigger && trigger && trigger.isConnected) {
        try { trigger.focus({ preventScroll: true }); } catch (_error) { trigger.focus(); }
      }
      scheduleStateChange();
      return true;
    }
    function requestClearSelection() {
      // The visible card action means “back to the building”, not “visit the
      // previously sampled hotspot”. Browser Back still traverses history.
      clearSelection(true, true);
      writeSpatialHistory("replaceState", "local");
      return true;
    }
    function validPortableSelection(value) {
      if (value === null) return true;
      if (!plain(value) || value.type !== "scene" || typeof value.id !== "string" || !scenes.has(value.id)
        || typeof value.hotspotId !== "string" || ["verified", "illustrative"].indexOf(value.evidenceLane) < 0) return false;
      var scene = scenes.get(value.id);
      var entity = sceneEntity(scene);
      return value.hotspotId === entity.hotspotId && value.evidenceLane === entity.evidenceLane;
    }
    function validPortableModel(value) {
      var camera = value && value.camera;
      var lighting = value && value.lighting;
      return plain(value) && plain(camera)
        && finite(camera.azimuth) && Math.abs(camera.azimuth) <= Math.PI * 1000
        && finite(camera.elevation) && camera.elevation >= -0.08 && camera.elevation <= 1.18
        && finite(camera.distance) && camera.distance > 0 && camera.distance <= 1000000
        && finite(camera.fieldOfView) && camera.fieldOfView >= 10 && camera.fieldOfView <= 100
        && Array.isArray(camera.target) && camera.target.length === 3 && camera.target.every(function (item) { return finite(item) && Math.abs(item) <= 1000000; })
        && plain(lighting) && lighting.schema === LIGHTING_SCHEMA && lighting.mode === "illustrative_directional"
        && Array.isArray(lighting.direction) && lighting.direction.length === 3
        && lighting.direction.every(function (item) { return finite(item) && Math.abs(item) <= 1; })
        && Math.hypot.apply(Math, lighting.direction) >= 0.001
        && finite(lighting.ambient) && lighting.ambient >= 0 && lighting.ambient <= 1
        && finite(lighting.diffuse) && lighting.diffuse >= 0 && lighting.diffuse <= 1
        && lighting.ambient + lighting.diffuse <= 1.5
        && lighting.decisionGrade === false && lighting.sunSimulation === false;
    }
    function validPortableMapProjection(value, selected) {
      var selectedId = selected ? selected.id : "";
      var mapState = value && value.map;
      var camera = mapState && mapState.camera;
      var coTour = value && value.coTour;
      if (!exactKeys(value, ["schema", "map", "selectedEntityId", "coTour"])
        || value.schema !== "nadlan-einstein-integration-state/v1" || value.selectedEntityId !== selectedId
        || !exactKeys(mapState, ["schema", "available", "camera", "selectedEntityId", "correlationState"])
        || mapState.schema !== "nadlan-einstein-canonical-map-state/v1" || mapState.selectedEntityId !== selectedId
        || (mapState.available !== true && mapState.available !== false)
        || ["idle", "panned", "cone", "unavailable-no-source", "unavailable-no-bearing"].indexOf(mapState.correlationState) < 0
        || (selectedId === "" ? mapState.correlationState !== "idle" : mapState.correlationState === "idle")
        || !exactKeys(coTour, ["schema", "state", "enabled", "transport", "privateEngineClosuresUsed", "roomIdentifiersInUrl", "hostSecretInUrlOrDom", "ttlSeconds"])
        || coTour.schema !== "nadlan-einstein-cotour-capability/v1" || coTour.state !== "ready_dedicated_adapter" || coTour.enabled !== true
        || coTour.transport !== "same_origin_ephemeral_rest" || coTour.privateEngineClosuresUsed !== false
        || coTour.roomIdentifiersInUrl !== false || coTour.hostSecretInUrlOrDom !== false || coTour.ttlSeconds !== 600) return false;
      // This contract carries no verified Einstein facility coordinates or
      // bearings. An illustrative selection can therefore never arrive from a
      // deep link/co-tour state as an already panned or coned map projection.
      if (selected && selected.evidenceLane === "illustrative" && mapState.correlationState !== "unavailable-no-source") return false;
      if (mapState.available === false) return camera === null;
      return exactKeys(camera, ["lng", "lat", "zoom", "bearing", "pitch"])
        && finite(camera.lng) && Math.abs(camera.lng) <= 180 && finite(camera.lat) && Math.abs(camera.lat) <= 90
        && finite(camera.zoom) && camera.zoom >= 0 && camera.zoom <= 24
        && finite(camera.bearing) && Math.abs(camera.bearing) <= 3600
        && finite(camera.pitch) && camera.pitch >= 0 && camera.pitch <= 85;
    }
    function validPortableMediaProjection(value, selected) {
      if (!exactKeys(value, ["schema", "mode", "toolId", "sceneId", "hotspotId", "page", "activePreview", "material", "decisionGrade"])
        || value.schema !== "nadlan-flagship-media-state/v1" || ["surface", "tool", "deferred"].indexOf(value.mode) < 0
        || value.decisionGrade !== false || !Number.isInteger(value.page) || value.page < 0 || value.page >= 3
        || typeof value.activePreview !== "string" || ["view", "interior", "design"].indexOf(value.activePreview) < 0
        || typeof value.toolId !== "string" || typeof value.sceneId !== "string" || typeof value.hotspotId !== "string"
        || !exactKeys(value.material, ["interior", "design", "windowView"])) return false;
      if (value.mode === "surface") return value.toolId === "" && value.sceneId === "" && value.hotspotId === ""
        && value.material.interior === null && value.material.design === null && value.material.windowView === null;
      if (["view", "interior", "design"].indexOf(value.toolId) < 0) return false;
      if (value.toolId === "interior") {
        return !!selected && value.sceneId === selected.id && value.hotspotId === selected.hotspotId
          && exactKeys(value.material.interior, ["sceneId"]) && value.material.interior.sceneId === selected.id
          && value.material.design === null && value.material.windowView === null;
      }
      if (value.sceneId !== "" || value.hotspotId !== "" || value.material.interior !== null) return false;
      if (value.toolId === "design") {
        return exactKeys(value.material.design, ["x", "y"])
          && finite(value.material.design.x) && value.material.design.x >= 10 && value.material.design.x <= 82
          && finite(value.material.design.y) && value.material.design.y >= 20 && value.material.design.y <= 78
          && value.material.windowView === null;
      }
      return value.material.design === null && exactKeys(value.material.windowView, ["bearing", "pitch"])
        && finite(value.material.windowView.bearing) && value.material.windowView.bearing >= 0 && value.material.windowView.bearing < 360
        && finite(value.material.windowView.pitch) && value.material.windowView.pitch >= 62 && value.material.windowView.pitch <= 85;
    }
    function validSpatialState(value) {
      if (!exactKeys(value, ["schema", "projectContractId", "historyVersion", "selectedEntity", "model", "map", "media"])
        || value.schema !== SPATIAL_STATE_SCHEMA || value.projectContractId !== config.identity.project_contract_id
        || value.historyVersion !== 1 || !validPortableSelection(value.selectedEntity) || !validPortableModel(value.model)
        || !validPortableMapProjection(value.map, value.selectedEntity) || !validPortableMediaProjection(value.media, value.selectedEntity)) return false;
      try { return JSON.stringify(value).length <= 65536; } catch (_error) { return false; }
    }
    function rollbackSpatialRestore(previous) {
      try {
        if (previous && previous.selectedEntity) {
          var previousScene = scenes.get(previous.selectedEntity.id);
          var previousHotspot = root.querySelector('[data-nlfs-model-hotspots] [data-nlfs-scene="' + previous.selectedEntity.id + '"]');
          selectSceneInPlace(previousScene, previousHotspot, { focus: false });
        } else clearSelection(false, false);
        if (integrationInstance && previous && previous.map && typeof integrationInstance.restoreState === "function") integrationInstance.restoreState(clone(previous.map));
        if (visualInstance && previous && previous.media && typeof visualInstance.restoreState === "function") visualInstance.restoreState(clone(previous.media), { allowToolOpen: true });
        if (modelReady && previous && previous.model) restoreModelState(clone(previous.model));
        else pendingModelState = previous && previous.model ? clone(previous.model) : null;
        root.dataset.deepLinkRollbackState = "restored-previous";
        return true;
      } catch (_rollbackError) {
        root.dataset.deepLinkRollbackState = "failed-closed";
        return false;
      }
    }
    function restoreSpatialState(value, options) {
      if (!validSpatialState(value)) return false;
      var previous;
      try { previous = captureSpatialState(); } catch (_captureError) { return false; }
      if (!integrationInstance || typeof integrationInstance.restoreState !== "function"
        || !integrationInstance.restoreState(clone(value.map))) {
        rollbackSpatialRestore(previous);
        return false;
      }
      if (value.selectedEntity) {
        var selected = scenes.get(value.selectedEntity.id);
        var hotspot = root.querySelector('[data-nlfs-model-hotspots] [data-nlfs-scene="' + value.selectedEntity.id + '"]');
        if (!selectSceneInPlace(selected, hotspot, { focus: false })) {
          rollbackSpatialRestore(previous);
          return false;
        }
      } else clearSelection(false, false);
      if (!visualInstance || typeof visualInstance.restoreState !== "function") {
        rollbackSpatialRestore(previous);
        return false;
      }
      var mediaRestored = visualInstance.restoreState(clone(value.media), { allowToolOpen: !!(options && options.allowDeeperMedia) });
      root.dataset.deepLinkMediaState = mediaRestored
        ? (value.media.mode === "surface" ? "restored-surface" : ((options && options.allowDeeperMedia) ? "restored" : "deferred-explicit-open"))
        : "unavailable";
      if (!mediaRestored) {
        rollbackSpatialRestore(previous);
        return false;
      }
      if (modelReady) {
        if (!restoreModelState(clone(value.model))) {
          rollbackSpatialRestore(previous);
          return false;
        }
        pendingSpatialRollback = null;
      } else {
        pendingModelState = clone(value.model);
        pendingSpatialRollback = clone(previous);
      }
      delete root.dataset.deepLinkRollbackState;
      if (options && options.history === "push") writeSpatialHistory("pushState", "back");
      else writeSpatialHistory("replaceState", "local");
      scheduleStateChange();
      return true;
    }
    function createDeepLink(value) {
      var state = value || captureSpatialState();
      if (!validSpatialState(state)) throw new Error("The governed spatial state is not portable.");
      var url = new URL(window.location.href);
      Array.from(url.searchParams.keys()).forEach(function (key) { url.searchParams.delete(key); });
      url.hash = "";
      url.searchParams.set(DEEP_LINK_PARAMETER, encodePortableState(state));
      return url.href;
    }
    function capabilityState(capabilityId) {
      var capabilities = config.decision_experience && config.decision_experience.capabilities;
      return plain(capabilities) && typeof capabilities[capabilityId] === "string" ? capabilities[capabilityId] : "";
    }
    function setCapabilityRuntimeState(capabilityId, runtimeState) {
      var slot = root.querySelector('[data-nlfs-capability-slot="' + capabilityId + '"]');
      if (slot) slot.dataset.runtimeState = runtimeState;
    }
    function setShareStatus(message, state) {
      if (!shareStatus) return;
      shareStatus.textContent = message || "";
      shareStatus.hidden = !message;
      shareStatus.dataset.state = state || "idle";
    }
    function finishShareAttempt() {
      if (!shareButton || !shareButton.isConnected) return;
      shareButton.disabled = false;
      shareButton.setAttribute("aria-disabled", "false");
    }
    function revealShareFallback(url) {
      if (!shareFallback || !shareFallback.isConnected) return;
      shareFallback.value = url;
      shareFallback.hidden = false;
      setShareStatus("לא ניתן היה להעתיק אוטומטית. הקישור מוכן להעתקה ידנית.", "manual-copy");
      try { shareFallback.focus({ preventScroll: true }); } catch (_error) { shareFallback.focus(); }
      shareFallback.select();
      finishShareAttempt();
    }
    function copyProjectLink(url) {
      if (!navigator.clipboard || typeof navigator.clipboard.writeText !== "function") {
        revealShareFallback(url);
        return;
      }
      Promise.resolve(navigator.clipboard.writeText(url)).then(function () {
        if (!shareButton || !shareButton.isConnected) return;
        setShareStatus("הקישור למצב הנוכחי הועתק.", "copied");
        finishShareAttempt();
      }).catch(function () { revealShareFallback(url); });
    }
    function onProjectShare(event) {
      event.preventDefault();
      var url;
      try { url = createDeepLink(); } catch (_error) {
        setShareStatus("לא ניתן ליצור קישור עד שמצב המודל זמין.", "unavailable");
        return;
      }
      if (shareFallback) {
        shareFallback.hidden = true;
        shareFallback.value = "";
      }
      shareButton.disabled = true;
      shareButton.setAttribute("aria-disabled", "true");
      setShareStatus("מכין קישור למצב הנוכחי…", "working");
      if (typeof navigator.share !== "function") {
        copyProjectLink(url);
        return;
      }
      Promise.resolve(navigator.share({
        title: document.title || "EINSTEIN TOWER",
        text: "מצב שמור בחוויית EINSTEIN TOWER",
        url: url
      })).then(function () {
        if (!shareButton || !shareButton.isConnected) return;
        setShareStatus("הקישור למצב הנוכחי שותף.", "shared");
        finishShareAttempt();
      }).catch(function (error) {
        if (error && error.name === "AbortError") {
          setShareStatus("השיתוף בוטל.", "cancelled");
          finishShareAttempt();
          return;
        }
        copyProjectLink(url);
      });
    }
    function mountProjectShare() {
      setCapabilityRuntimeState("co_tour", capabilityState("co_tour") === "ready" ? "awaiting-dedicated-adapter" : "unavailable");
      var buttons = root.querySelector('[data-nlfs-page-slot="primary_actions"] .nlfs__cta-band-buttons');
      var section = buttons && buttons.closest('[data-nlfs-page-slot="primary_actions"]');
      if (capabilityState("project_share") !== "ready" || !buttons || !section) {
        setCapabilityRuntimeState("project_share", "unavailable");
        return false;
      }
      shareButton = document.createElement("button");
      shareButton.type = "button";
      shareButton.dataset.nlfsShare = "";
      shareButton.textContent = "שיתוף מצב";
      shareButton.setAttribute("aria-label", "שיתוף קישור למצב הנוכחי של הפרויקט");
      shareStatus = document.createElement("p");
      shareStatus.className = "nlfs__cta-band-status nlfs__share-status";
      shareStatus.dataset.nlfsShareStatus = "";
      shareStatus.setAttribute("role", "status");
      shareStatus.setAttribute("aria-live", "polite");
      shareStatus.hidden = true;
      shareFallback = document.createElement("input");
      shareFallback.type = "url";
      shareFallback.readOnly = true;
      shareFallback.hidden = true;
      shareFallback.dataset.nlfsShareLink = "";
      shareFallback.setAttribute("aria-label", "קישור לשיתוף ידני");
      shareFallback.setAttribute("dir", "ltr");
      buttons.appendChild(shareButton);
      section.appendChild(shareStatus);
      section.appendChild(shareFallback);
      shareButton.addEventListener("click", onProjectShare, { signal: signal });
      setCapabilityRuntimeState("project_share", "materialized");
      return true;
    }
    function openExternalTool(event) {
      var detail = event && event.detail;
      if (!detail || detail.toolId !== "view" || !detail.trigger || !detail.trigger.isConnected
        || !visualInstance || typeof visualInstance.openTool !== "function") return;
      if (!visualInstance.openTool("view", detail.trigger)) {
        updateStatus(config.copy.error);
        setInteractionAvailability(false);
      }
    }
    function paintMediaDock(activeTarget, sceneId) {
      root.querySelectorAll("[data-nlfs-media-dock] button[data-nlfs-media-target]").forEach(function (button) {
        var selected = button.dataset.nlfsMediaTarget === activeTarget
          && (activeTarget !== "scene" || button.dataset.nlfsMediaScene === sceneId);
        button.setAttribute("aria-pressed", selected ? "true" : "false");
      });
    }
    function onVisualMediaStateChange(state) {
      if (plain(state) && state.toolId === "interior" && typeof state.sceneId === "string" && scenes.has(state.sceneId)) {
        var scene = scenes.get(state.sceneId);
        if (!selectedScene || selectedScene.id !== scene.id) selectSceneInPlace(scene, null, { focus: false });
        paintMediaDock("scene", scene.id);
      } else if (plain(state) && state.toolId === "view") {
        paintMediaDock("view", "");
      } else if (plain(state) && state.mode === "surface") {
        // Closing a deep tool must reconcile the dock with the visible surface.
        // Keep an in-place scene selection highlighted; otherwise return to Model.
        paintMediaDock(selectedScene ? "scene" : "model", selectedScene ? selectedScene.id : "");
      }
      scheduleStateChange();
    }
    function mountMediaDock() {
      var dock = root.querySelector("[data-nlfs-media-dock]");
      if (!dock) return false;
      dock.addEventListener("click", function (event) {
        var sourceLink = event.target.closest('a[href^="#"]');
        if (sourceLink && dock.contains(sourceLink)) {
          var sourceTarget = document.getElementById(sourceLink.getAttribute("href").slice(1));
          if (!sourceTarget) return;
          event.preventDefault();
          var sourceReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
          sourceTarget.scrollIntoView({ block: "start", behavior: sourceReducedMotion ? "auto" : "smooth" });
          try { sourceTarget.focus({ preventScroll: true }); } catch (_error) { sourceTarget.focus(); }
          return;
        }
        var button = event.target.closest("button[data-nlfs-media-target]");
        if (!button || !dock.contains(button)) return;
        var target = button.dataset.nlfsMediaTarget || "";
        if (target === "model") {
          clearSelection(false, true);
          writeSpatialHistory("replaceState", "local");
          var stage = root.querySelector("[data-nlfs-protected-stage]");
          var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
          if (stage) stage.scrollIntoView({ block: "nearest", behavior: reducedMotion ? "auto" : "smooth" });
          var modelControl = root.querySelector('[data-nlfs-action="reset"]');
          if (modelControl && !modelControl.disabled) modelControl.focus({ preventScroll: true });
          paintMediaDock("model", "");
          return;
        }
        if (target === "view") {
          if (visualInstance && typeof visualInstance.openTool === "function" && visualInstance.openTool("view", button)) paintMediaDock("view", "");
          else {
            updateStatus(config.copy.error);
            setInteractionAvailability(false);
          }
          return;
        }
        var sceneId = button.dataset.nlfsMediaScene || "";
        var scene = scenes.get(sceneId);
        if (target === "scene" && scene && selectSceneInPlace(scene, button, { history: "push", focus: false })) {
          paintMediaDock("scene", scene.id);
          openSelectedMaterial(button);
        }
      }, { signal: signal });
      paintMediaDock("model", "");
      return true;
    }
    function openSelectedMaterial(trigger) {
      if (!selectedScene || !visualInstance || typeof visualInstance.openTool !== "function") return false;
      var opened = visualInstance.openTool("interior", trigger, {
        sceneId: selectedScene.id,
        hotspotId: selectedScene.model_hotspot_group
      });
      if (!opened) {
        root.dataset.interactionState = "tool-unavailable";
        updateStatus(config.copy.error);
        setInteractionAvailability(false);
      }
      return !!opened;
    }
    function onSpatialPopState(event) {
      var entry = plain(event.state) ? event.state[SPATIAL_HISTORY_KEY] : null;
      spatialHistoryRestoring = true;
      try {
        if (validSpatialHistory(entry) && entry.selectedSceneId) {
          var scene = scenes.get(entry.selectedSceneId);
          var hotspot = root.querySelector('[data-nlfs-model-hotspots] [data-nlfs-scene="' + entry.selectedSceneId + '"]');
          selectSceneInPlace(scene, hotspot, { focus: false });
          spatialHistoryRevision = Math.max(spatialHistoryRevision, entry.revision);
        } else clearSelection(true, true);
      } finally {
        spatialHistoryRestoring = false;
      }
    }
    function restoreStateEvent(event) {
      var detail = event && event.detail;
      if (!detail || !detail.state) return;
      restoreSpatialState(detail.state, { allowDeeperMedia: detail.allowDeeperMedia === true, history: detail.history === "push" ? "push" : "replace" });
    }
    function updateHotspots() {
      root.querySelectorAll("[data-nlfs-model-hotspots] [data-nlfs-scene][data-position]").forEach(function (button) {
        var projected = modelReady && viewer && typeof viewer.project === "function" ? viewer.project(button.dataset.position || "") : { visible: false };
        var usable = projected.visible && toolsAvailable;
        button.hidden = !usable;
        button.disabled = !usable;
        button.setAttribute("aria-disabled", usable ? "false" : "true");
        if (usable) {
          button.style.setProperty("--nlfs-x", projected.x + "%");
          button.style.setProperty("--nlfs-y", projected.y + "%");
        }
      });
    }
    function updateModelBearing() {
      if (!modelBearing || !viewer || typeof viewer.getState !== "function") return;
      try {
        var state = viewer.getState();
        var radians = Number(state && state.camera && state.camera.azimuth);
        if (!Number.isFinite(radians)) return;
        var degrees = ((radians * 180 / Math.PI) % 360 + 360) % 360;
        modelBearing.value = String(Math.round(degrees));
        modelBearing.textContent = "אזימוט המחשה: " + Math.round(degrees) + "°";
      } catch (_error) {}
    }
    function setModelAvailability(available) {
      modelReady = available === true;
      root.querySelectorAll("[data-nlfs-action]").forEach(function (control) {
        control.disabled = !modelReady;
        control.setAttribute("aria-disabled", modelReady ? "false" : "true");
      });
      model.tabIndex = modelReady ? 0 : -1;
      model.setAttribute("aria-disabled", modelReady ? "false" : "true");
      updateHotspots();
    }
    function setInteractionAvailability(available) {
      toolsAvailable = available === true;
      root.dataset.interactionState = available ? "ready" : "unavailable";
      root.querySelectorAll(".nlfs__experience-card [data-nlfs-scene],[data-nlvt-open],[data-nlfs-media-dock] button[data-nlfs-media-target=\"view\"],[data-nlfs-media-dock] button[data-nlfs-media-target=\"scene\"]").forEach(function (control) {
        if ("disabled" in control) control.disabled = !available;
        if (available) control.removeAttribute("aria-disabled");
        else {
          control.setAttribute("aria-disabled", "true");
          if (control.hasAttribute("aria-pressed")) control.setAttribute("aria-pressed", "false");
        }
      });
      if (!available) paintMediaDock("model", "");
      updateHotspots();
    }
    function reconcileVisualFallback() {
      if (modelReady) {
        poster.hidden = true;
        return;
      }
      setModelAvailability(false);
      if (posterState === "ready") {
        poster.hidden = false;
        root.dataset.modelState = modelFailed ? "poster" : "loading";
        updateStatus(modelFailed ? config.copy.error : config.copy.loading);
      } else if (posterState === "loading") {
        poster.hidden = false;
        root.dataset.modelState = modelFailed ? "poster-loading" : "loading";
        updateStatus(config.copy.loading);
      } else {
        poster.hidden = true;
        root.dataset.modelState = "unavailable";
        updateStatus("לא ניתן לטעון כרגע את מודל ההמחשה או את תמונת הגיבוי.");
      }
    }
    function performModelLoad(url, quality) {
      if (!viewer || !url) { modelFailed = true; onError(); return Promise.resolve(false); }
      root.dataset.modelRequestedQuality = quality;
      var request;
      try { request = viewer.loadUrl(url); } catch (_error) { request = Promise.reject(_error); }
      return Promise.resolve(request).then(function () {
        hdLoaded = quality === "hd" || hdLoaded;
        lodLoaded = quality === "lod" || lodLoaded;
        modelFailed = false;
        onLoad();
        return true;
      }).catch(function () {
        if (quality === "hd" && lodLoaded) {
          poster.hidden = true;
          root.dataset.modelState = "ready-lod";
          updateStatus("מודל ההמחשה הקל נשאר פעיל; גרסת HD אינה זמינה כרגע.");
          updateHotspots();
        } else {
          modelFailed = true;
          onError();
        }
        return false;
      });
    }
    function loadVisibleLod() {
      if (lodLoaded || hdLoaded) return Promise.resolve(true);
      if (config.model.lod && config.model.lod.url) {
        if (!lodLoad) lodLoad = performModelLoad(config.model.lod.url, "lod");
        return lodLoad;
      }
      if (!hdLoad) hdLoad = performModelLoad(config.model.hd.url, "hd");
      return hdLoad;
    }
    function upgradeHd() {
      if (saveData || hdLoaded || !config.model.hd || !config.model.hd.url) return Promise.resolve(hdLoaded);
      if (hdLoad) return hdLoad;
      var prerequisite = lodLoad || (lodLoaded ? Promise.resolve(true) : loadVisibleLod());
      hdLoad = Promise.resolve(prerequisite).catch(function () { return false; }).then(function () {
        if (hdLoaded) return true;
        return performModelLoad(config.model.hd.url, "hd");
      });
      return hdLoad;
    }
    function onClick(event) {
      var returnDecision = event.target.closest("[data-nlfs-return-decision]");
      if (returnDecision && root.contains(returnDecision)) {
        var decisionRoom = root.querySelector("[data-nlfs-decision-hero]");
        if (decisionRoom) {
          event.preventDefault();
          var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
          try { decisionRoom.scrollIntoView({ block: "start", behavior: reduced ? "auto" : "smooth" }); } catch (_scrollError) { decisionRoom.scrollIntoView(); }
          try { decisionRoom.focus({ preventScroll: true }); } catch (_focusError) { decisionRoom.focus(); }
        }
        return;
      }
      var selectionBack = event.target.closest("[data-nlfs-selection-back]");
      if (selectionBack && root.contains(selectionBack)) { event.preventDefault(); requestClearSelection(); return; }
      var selectionOpen = event.target.closest("[data-nlfs-selection-open]");
      if (selectionOpen && root.contains(selectionOpen)) { event.preventDefault(); openSelectedMaterial(selectionOpen); return; }
      var sceneTrigger = event.target.closest("[data-nlfs-scene]");
      if (sceneTrigger && root.contains(sceneTrigger)) {
        var sceneId = sceneTrigger.dataset.nlfsScene || "";
        var scene = scenes.get(sceneId);
        var isModelHotspot = sceneTrigger.dataset.nlfsSelectionMode === "in-place" || !!sceneTrigger.closest("[data-nlfs-model-hotspots]");
        if (scene && isModelHotspot) {
          event.preventDefault();
          upgradeHd();
          selectSceneInPlace(scene, sceneTrigger, { focus: true, history: "push" });
          return;
        }
        if (scene) selectSceneInPlace(scene, sceneTrigger, { focus: false, history: "push" });
        var openedByPlayground = !!(scene && visualInstance && typeof visualInstance.openTool === "function" && visualInstance.openTool("interior", sceneTrigger, {
          sceneId: sceneId,
          hotspotId: scene.model_hotspot_group
        }));
        if (!openedByPlayground) {
          updateStatus(config.copy.error);
          setInteractionAvailability(false);
          root.dataset.interactionState = "history-unavailable";
        }
        return;
      }
      var action = event.target.closest("[data-nlfs-action]");
      if (!action || !root.contains(action)) return;
      upgradeHd();
      if (action.dataset.nlfsAction === "reset" && viewer) viewer.reset();
      if (action.dataset.nlfsAction === "north" && viewer && typeof viewer.getState === "function" && typeof viewer.setState === "function") {
        var northState = viewer.getState();
        if (northState && northState.camera) { northState.camera.azimuth = 0; viewer.setState(northState); updateModelBearing(); }
      }
      if (action.dataset.nlfsAction === "zoom-in" && viewer) viewer.zoom(-1);
      if (action.dataset.nlfsAction === "zoom-out" && viewer) viewer.zoom(1);
    }
    function onLoad() {
      modelFailed = false; poster.hidden = true; updateStatus(""); root.dataset.modelState = hdLoaded ? "ready-hd" : "ready-lod"; setModelAvailability(true);
      if (pendingModelState && viewer && typeof viewer.setState === "function") {
        if (viewer.setState(pendingModelState)) {
          pendingModelState = null;
          pendingSpatialRollback = null;
          if (root.dataset.deepLinkState === "pending-model") root.dataset.deepLinkState = "restored-no-teleport";
        } else {
          var rollbackState = pendingSpatialRollback;
          pendingModelState = null;
          pendingSpatialRollback = null;
          rollbackSpatialRestore(rollbackState);
          if (root.dataset.deepLinkState === "pending-model") root.dataset.deepLinkState = "rejected-model-state";
        }
      }
      updateModelBearing(); scheduleStateChange();
    }
    function onError() { modelFailed = true; reconcileVisualFallback(); }
    function onPosterLoad() { posterState = "ready"; root.dataset.posterState = "ready"; reconcileVisualFallback(); }
    function onPosterError() { posterState = "failed"; root.dataset.posterState = "failed"; reconcileVisualFallback(); }

    root.addEventListener("click", onClick, { signal: signal });
    root.addEventListener("nadlan:flagship-v3:open-tool", openExternalTool, { signal: signal });
    root.addEventListener("nadlan:flagship-v3:restore-state", restoreStateEvent, { signal: signal });
    root.addEventListener("nadlan:flagship-v3:map-state-change", scheduleStateChange, { signal: signal });
    window.addEventListener("popstate", onSpatialPopState, { signal: signal });
    root.querySelector("[data-nlfs-protected-stage]").addEventListener("pointerdown", upgradeHd, { signal: signal, once: true });
    poster.addEventListener("error", onPosterError, { signal: signal });
    poster.addEventListener("load", onPosterLoad, { signal: signal });
    if (poster.complete) {
      if (poster.naturalWidth > 0) onPosterLoad();
      else onPosterError();
    } else {
      root.dataset.posterState = "loading";
      reconcileVisualFallback();
    }
    try {
      if (!window.NadlanFlagshipLocalViewer || typeof window.NadlanFlagshipLocalViewer.create !== "function") throw new Error("Local viewer missing");
      viewer = window.NadlanFlagshipLocalViewer.create(model, { defaultOrbit: config.model.default_orbit, defaultTarget: config.model.default_target, onChange: function () { updateHotspots(); updateModelBearing(); }, onStateChange: syncVisualHistory });
      if (window.IntersectionObserver) {
        visibilityObserver = new IntersectionObserver(function (entries) {
          if (entries.some(function (entry) { return entry.isIntersecting && entry.intersectionRatio >= 0.1; })) { visibilityObserver.disconnect(); loadVisibleLod(); }
        }, { threshold: [0.1] });
        visibilityObserver.observe(root.querySelector("[data-nlfs-protected-stage]"));
      } else {
        window.setTimeout(loadVisibleLod, 0);
      }
    } catch (_error) {
      onError();
    }
    setModelAvailability(false);

    if (window.NadlanFlagshipIntegrations && typeof window.NadlanFlagshipIntegrations.create === "function") {
      try { integrationInstance = window.NadlanFlagshipIntegrations.create(root, config); } catch (_error) { integrationInstance = null; }
    }
    if (window.NadlanFlagshipShowroom && typeof window.NadlanFlagshipShowroom.mount === "function" && integrationInstance) {
      try {
        visualInstance = window.NadlanFlagshipShowroom.mount(playground, {
          data: config.playground,
          expectedProjectContractId: config.identity.project_contract_id,
          allowedAssetPrefix: config.playground_trust.allowed_asset_prefix,
          allowedEvidenceReferenceIds: config.playground_trust.allowed_evidence_reference_ids,
          direction: config.direction,
          locale: config.locale,
          captureModelState: captureModelState,
          restoreModelState: restoreModelState,
          onMediaStateChange: onVisualMediaStateChange,
          mountWindowView: integrationInstance.mountWindowView,
          designUrl: config.integrations.design_url,
          districtTourUrl: config.integrations.district_tour_url
        });
      } catch (_error) {
        playground.hidden = true;
      }
    } else {
      playground.hidden = true;
    }
    setInteractionAvailability(!!viewer && !!visualInstance && typeof visualInstance.isHistoryReady === "function" && visualInstance.isHistoryReady());
    mountProjectShare();
    mountMediaDock();
    writeSpatialHistory("replaceState", "local");

    function destroy() {
      if (!instances.has(root)) return;
      controller.abort();
      if (visibilityObserver) visibilityObserver.disconnect();
      if (stateChangeFrame) window.cancelAnimationFrame(stateChangeFrame);
      stateChangeFrame = 0;
      if (viewer && typeof viewer.destroy === "function") viewer.destroy();
      if (visualInstance && typeof visualInstance.destroy === "function") visualInstance.destroy();
      if (integrationInstance && typeof integrationInstance.destroy === "function") integrationInstance.destroy();
      if (selectionNodeInjected && selectionNode && selectionNode.isConnected) selectionNode.remove();
      if (shareButton && shareButton.isConnected) shareButton.remove();
      if (shareStatus && shareStatus.isConnected) shareStatus.remove();
      if (shareFallback && shareFallback.isConnected) shareFallback.remove();
      setCapabilityRuntimeState("project_share", "unmounted");
      selectionNode = null;
      shareButton = null;
      shareStatus = null;
      shareFallback = null;
      pendingModelState = null;
      pendingSpatialRollback = null;
      instances.delete(root);
      root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:destroyed", { bubbles: true }));
    }
    var instance = {
      destroy: destroy,
      config: config,
      getState: function () { return clone(captureSpatialState()); },
      restoreState: function (value, restoreOptions) { return restoreSpatialState(clone(value), restoreOptions || {}); },
      createDeepLink: function (value) { return createDeepLink(value ? clone(value) : null); },
      parseDeepLink: function (value) {
        var decoded = decodePortableState(value);
        return validSpatialState(decoded) ? decoded : null;
      },
      getLightingState: function () { return viewer && typeof viewer.getLightingState === "function" ? viewer.getLightingState() : null; },
      setIllustrativeLighting: function (value) {
        var changed = !!(viewer && typeof viewer.setLightingState === "function" && viewer.setLightingState(value));
        if (changed) scheduleStateChange();
        return changed;
      },
      getCapabilities: function () {
        return {
          schema: "nadlan-flagship-spatial-capabilities/v1",
          stateSchema: SPATIAL_STATE_SCHEMA,
          deepLinks: true,
          automaticFullscreenFromDeepLink: false,
          projectShare: {
            enabled: !!(shareButton && shareButton.isConnected),
            stripsExistingQueryAndFragment: true,
            transport: typeof navigator.share === "function" ? "web-share-with-copy-fallback" : "copy-link"
          },
          viewer: viewer && typeof viewer.getCapabilities === "function" ? viewer.getCapabilities() : null,
          integrations: integrationInstance && typeof integrationInstance.getCapabilities === "function" ? integrationInstance.getCapabilities() : null,
          media: visualInstance && typeof visualInstance.getCapabilities === "function" ? visualInstance.getCapabilities() : null
        };
      }
    };
    instances.set(root, instance);
    var deepLinkValue = new URL(window.location.href).searchParams.get(DEEP_LINK_PARAMETER);
    if (deepLinkValue) {
      var deepLinkState = instance.parseDeepLink(deepLinkValue);
      var deepLinkRestored = !!(deepLinkState && instance.restoreState(deepLinkState, { allowDeeperMedia: false, history: "push" }));
      root.dataset.deepLinkState = deepLinkRestored ? (modelReady ? "restored-no-teleport" : "pending-model") : "rejected";
    }
    scheduleStateChange();
    root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:mounted", { bubbles: true, detail: { schema: config.schema, stateSchema: SPATIAL_STATE_SCHEMA } }));
  }

  function mountAll(scope) {
    (scope || document).querySelectorAll('[data-nl-flagship="v3"]').forEach(mount);
  }
  function destroyAll() {
    Array.from(instances.values()).forEach(function (instance) { instance.destroy(); });
  }
  function resolveInstance(target) {
    if (target && target.nodeType === 1) return instances.get(target) || null;
    if (typeof target === "string" && target) {
      var node = document.querySelector(target);
      return node ? instances.get(node) || null : null;
    }
    var first = instances.values().next();
    return first.done ? null : first.value;
  }
  function getState(target) {
    var instance = resolveInstance(target);
    return instance ? instance.getState() : null;
  }
  function restoreState(target, value, options) {
    var instance = resolveInstance(target);
    if (!instance) return false;
    try { return instance.restoreState(value, options || {}); } catch (_error) { return false; }
  }
  function createDeepLink(target, value) {
    var instance = resolveInstance(target);
    if (!instance) return "";
    try { return instance.createDeepLink(value); } catch (_error) { return ""; }
  }
  function parseDeepLink(target, value) {
    var instance = resolveInstance(target);
    if (!instance) return null;
    try {
      var token = String(value || "");
      if (/^(?:https?:)?\/\//i.test(token) || token.charAt(0) === "/") token = new URL(token, window.location.href).searchParams.get(DEEP_LINK_PARAMETER) || "";
      return instance.parseDeepLink(token);
    } catch (_error) { return null; }
  }
  function getCapabilities(target) {
    var instance = resolveInstance(target);
    return instance ? clone(instance.getCapabilities()) : null;
  }
  function getLightingState(target) {
    var instance = resolveInstance(target);
    return instance ? instance.getLightingState() : null;
  }
  function setIllustrativeLighting(target, value) {
    var instance = resolveInstance(target);
    return !!(instance && instance.setIllustrativeLighting(value));
  }

  document.addEventListener("DOMContentLoaded", function () { mountAll(document); }, { once: true });
  document.addEventListener("nadlan:flagship-v3:mount", function (event) { mountAll(event.target || document); });
  document.addEventListener("nadlan:flagship-v3:teardown", destroyAll);
  window.addEventListener("pagehide", function (event) { if (!event.persisted) destroyAll(); });
  window.addEventListener("pageshow", function (event) { if (event.persisted) mountAll(document); });

  window.NadlanFlagshipV3 = Object.freeze({
    mountAll: mountAll,
    destroyAll: destroyAll,
    getState: getState,
    restoreState: restoreState,
    createDeepLink: createDeepLink,
    parseDeepLink: parseDeepLink,
    getCapabilities: getCapabilities,
    getLightingState: getLightingState,
    setIllustrativeLighting: setIllustrativeLighting,
    SPATIAL_STATE_SCHEMA: SPATIAL_STATE_SCHEMA,
    SPATIAL_ENTITY_SCHEMA: SPATIAL_ENTITY_SCHEMA
  });
})();
