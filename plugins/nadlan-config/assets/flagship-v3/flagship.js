/* NadLan flagship v3 bootstrap. First-party viewer; no beacon, storage, form or write path. */
(function () {
  "use strict";

  var instances = new Map();

  function readConfig(root) {
    var node = root.querySelector("[data-nlfs-config]");
    if (!node) return null;
    try {
      var config = JSON.parse(node.textContent || "");
      if (!config || config.schema !== "nadlan-flagship-runtime/v3") return null;
      if (!config.capabilities || config.capabilities.writes_enabled !== false) return null;
      if (config.capabilities.lead_submission !== false || config.capabilities.comment_submission !== false) return null;
      if (!config.inventory || config.inventory.decision_grade !== false) return null;
      if (!config.experiences || config.experiences.schema !== "nadlan-project-experience-registry/v1") return null;
      if (!Array.isArray(config.experiences.scenes) || !config.experiences.scenes.length) return null;
      return config;
    } catch (_error) {
      return null;
    }
  }

  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (typeof text === "string") node.textContent = text;
    return node;
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
    var activeDialog = null;
    var scenes = new Map();
    config.experiences.scenes.forEach(function (scene) { scenes.set(scene.id, scene); });
    var saveData = !!(navigator.connection && navigator.connection.saveData);
    var selectedModelUrl = saveData && config.model.lod && config.model.lod.url ? config.model.lod.url : config.model.hd.url;

    function updateStatus(value) { status.textContent = value; }
    function captureModelState() { return viewer && typeof viewer.getState === "function" ? viewer.getState() : null; }
    function restoreModelState(state) { if (viewer && state && typeof viewer.setState === "function") viewer.setState(state); }
    function updateHotspots() {
      root.querySelectorAll("[data-nlfs-model-hotspots] [data-nlfs-scene][data-position]").forEach(function (button) {
        var projected = viewer && typeof viewer.project === "function" ? viewer.project(button.dataset.position || "") : { visible: false };
        button.hidden = !projected.visible;
        if (projected.visible) {
          button.style.setProperty("--nlfs-x", projected.x + "%");
          button.style.setProperty("--nlfs-y", projected.y + "%");
        }
      });
    }
    function restorePage(state) {
      document.documentElement.style.overflow = state.htmlOverflow;
      document.body.style.overflow = state.bodyOverflow;
      window.requestAnimationFrame(function () {
        window.scrollTo(state.scrollX, state.scrollY);
        restoreModelState(state.model);
        if (state.focus && state.focus.isConnected && typeof state.focus.focus === "function") state.focus.focus({ preventScroll: true });
      });
    }
    function closeExperience() {
      if (!activeDialog || activeDialog.closing) return;
      activeDialog.closing = true;
      var current = activeDialog;
      activeDialog = null;
      if (current.dialog.open && typeof current.dialog.close === "function") current.dialog.close();
      current.dialog.remove();
      restorePage(current.state);
    }
    function openExperience(sceneId) {
      var scene = scenes.get(sceneId);
      if (!scene) return;
      if (activeDialog) closeExperience();

      var groupIds = Array.isArray(scene.model_hotspot_scene_ids) ? scene.model_hotspot_scene_ids.filter(function (id) { return scenes.has(id); }) : [];
      if (!groupIds.length) groupIds = [scene.id];
      if (groupIds.indexOf(scene.id) === -1) groupIds.unshift(scene.id);
      var groupIndex = Math.max(0, groupIds.indexOf(scene.id));

      var state = {
        model: captureModelState(),
        scrollX: window.scrollX,
        scrollY: window.scrollY,
        focus: document.activeElement,
        htmlOverflow: document.documentElement.style.overflow,
        bodyOverflow: document.body.style.overflow
      };
      var dialog = element("dialog", "nlfs-dialog");
      dialog.dir = config.direction;
      dialog.lang = config.locale;
      dialog.setAttribute("aria-labelledby", root.id + "-scene-dialog-title");
      var shell = element("div", "nlfs-dialog__shell");
      var header = element("header", "nlfs-dialog__header");
      var back = element("button", "nlfs-dialog__back", config.experiences.back_label);
      back.type = "button";
      back.setAttribute("data-nlfs-dialog-back", "");
      var heading = element("h2", "", scene.title);
      heading.id = root.id + "-scene-dialog-title";
      var navigation = element("div", "nlfs-dialog__nav");
      var previous = element("button", "", config.experiences.previous_label);
      var next = element("button", "", config.experiences.next_label);
      previous.type = "button";
      next.type = "button";
      navigation.append(previous, next);
      if (groupIds.length < 2) navigation.hidden = true;
      header.append(back, heading, navigation);

      var stage = element("div", "nlfs-dialog__stage");
      var image = element("img", "nlfs-dialog__image");
      image.decoding = "async";
      stage.appendChild(image);
      var detail = element("p", "nlfs-dialog__detail");
      detail.setAttribute("role", "status");
      function applyScene(nextScene) {
        heading.textContent = nextScene.title;
        image.src = nextScene.fullscreen_url;
        image.alt = nextScene.title;
        detail.textContent = nextScene.summary;
        stage.querySelectorAll(".nlfs-dialog__hotspot").forEach(function (hotspotNode) { hotspotNode.remove(); });
        nextScene.image_hotspots.forEach(function (hotspot, index) {
          var button = element("button", "nlfs-dialog__hotspot", String(index + 1));
          button.type = "button";
          button.setAttribute("aria-label", hotspot.label);
          button.style.setProperty("--nlfs-x", hotspot.x_percent + "%");
          button.style.setProperty("--nlfs-y", hotspot.y_percent + "%");
          button.addEventListener("click", function () { detail.textContent = hotspot.label + " — " + hotspot.detail; });
          stage.appendChild(button);
        });
        dialog.dataset.nlfsActiveScene = nextScene.id;
      }
      function moveScene(delta) {
        groupIndex = (groupIndex + delta + groupIds.length) % groupIds.length;
        applyScene(scenes.get(groupIds[groupIndex]));
      }
      previous.addEventListener("click", function () { moveScene(-1); }, { signal: signal });
      next.addEventListener("click", function () { moveScene(1); }, { signal: signal });
      applyScene(scene);
      shell.append(header, stage, detail);
      dialog.appendChild(shell);
      dialog.addEventListener("cancel", function (event) { event.preventDefault(); closeExperience(); }, { signal: signal });
      back.addEventListener("click", closeExperience, { signal: signal });
      document.body.appendChild(dialog);
      activeDialog = { dialog: dialog, state: state, closing: false };
      document.documentElement.style.overflow = "hidden";
      document.body.style.overflow = "hidden";
      if (typeof dialog.showModal === "function") dialog.showModal();
      else dialog.setAttribute("open", "");
      back.focus({ preventScroll: true });
    }
    function onClick(event) {
      var sceneTrigger = event.target.closest("[data-nlfs-scene]");
      if (sceneTrigger && root.contains(sceneTrigger)) {
        var sceneId = sceneTrigger.dataset.nlfsScene || "";
        var scene = scenes.get(sceneId);
        var openedByPlayground = !!(scene && visualInstance && typeof visualInstance.openTool === "function" && visualInstance.openTool("interior", sceneTrigger, {
          sceneId: sceneId,
          hotspotId: scene.model_hotspot_group
        }));
        if (!openedByPlayground) openExperience(sceneId);
        return;
      }
      var action = event.target.closest("[data-nlfs-action]");
      if (!action || !root.contains(action)) return;
      if (action.dataset.nlfsAction === "reset" && viewer) viewer.reset();
      if (action.dataset.nlfsAction === "zoom-in" && viewer) viewer.zoom(-1);
      if (action.dataset.nlfsAction === "zoom-out" && viewer) viewer.zoom(1);
    }
    function onLoad() { poster.hidden = true; updateStatus(""); root.dataset.modelState = "ready"; updateHotspots(); }
    function onError() { poster.hidden = false; updateStatus(config.copy.error); root.dataset.modelState = "poster"; updateHotspots(); }

    root.addEventListener("click", onClick, { signal: signal });
    try {
      if (!window.NadlanFlagshipLocalViewer || typeof window.NadlanFlagshipLocalViewer.create !== "function") throw new Error("Local viewer missing");
      viewer = window.NadlanFlagshipLocalViewer.create(model, { defaultOrbit: config.model.default_orbit, defaultTarget: config.model.default_target, onChange: updateHotspots });
      viewer.loadUrl(selectedModelUrl).then(onLoad).catch(onError);
    } catch (_error) {
      onError();
    }

    var visualInstance = null;
    if (window.NadlanFlagshipShowroom && typeof window.NadlanFlagshipShowroom.mount === "function") {
      try {
        visualInstance = window.NadlanFlagshipShowroom.mount(playground, {
          data: config.playground,
          expectedProjectContractId: config.identity.project_contract_id,
          allowedAssetPrefix: config.playground_trust.allowed_asset_prefix,
          allowedEvidenceReferenceIds: config.playground_trust.allowed_evidence_reference_ids,
          direction: config.direction,
          locale: config.locale,
          captureModelState: captureModelState,
          restoreModelState: restoreModelState
        });
      } catch (_error) {
        playground.hidden = true;
      }
    } else {
      playground.hidden = true;
    }

    function destroy() {
      if (!instances.has(root)) return;
      closeExperience();
      controller.abort();
      if (viewer && typeof viewer.destroy === "function") viewer.destroy();
      if (visualInstance && typeof visualInstance.destroy === "function") visualInstance.destroy();
      instances.delete(root);
      root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:destroyed", { bubbles: true }));
    }
    instances.set(root, { destroy: destroy, config: config });
    root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:mounted", { bubbles: true, detail: { schema: config.schema } }));
  }

  function mountAll(scope) {
    (scope || document).querySelectorAll('[data-nl-flagship="v3"]').forEach(mount);
  }
  function destroyAll() {
    Array.from(instances.values()).forEach(function (instance) { instance.destroy(); });
  }

  document.addEventListener("DOMContentLoaded", function () { mountAll(document); }, { once: true });
  document.addEventListener("nadlan:flagship-v3:mount", function (event) { mountAll(event.target || document); });
  document.addEventListener("nadlan:flagship-v3:teardown", destroyAll);
  window.addEventListener("pagehide", destroyAll, { once: true });

  window.NadlanFlagshipV3 = Object.freeze({ mountAll: mountAll, destroyAll: destroyAll });
})();
