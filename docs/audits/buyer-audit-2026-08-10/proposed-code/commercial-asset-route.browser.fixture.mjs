/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Portable real-Chromium fixture for the selected commercial asset URL,
 * picker/model equivalence, Back/Forward selection, and nested tool history.
 * All requests are fulfilled locally on example.invalid.
 *
 * Run:
 *   node commercial-asset-route.browser.fixture.mjs
 */
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const here = path.dirname(fileURLToPath(import.meta.url));
const decisionPath = path.join(here, "commercial-decision-surface.js");
const selectorPath = path.join(here, "commercial-floor-selection.js");
const cssPath = path.join(here, "commercial-decision-surface.css");
const baseUrl = "https://example.invalid/projects/fixture-commercial/";

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 375, height: 812 } });
const page = await context.newPage();

try {
  await page.route("https://example.invalid/**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "text/html; charset=utf-8",
      body: `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
        <body><div id="model-origin"><button id="origin-focus" type="button">Model origin</button><model-viewer id="model"></model-viewer><span id="model-after"></span></div>
        <label for="floor-picker">Floor</label><select id="floor-picker"></select><button id="previous" type="button">Previous</button><button id="next" type="button">Next</button><p id="live" aria-live="polite"></p></body></html>`
    });
  });
  await page.goto(baseUrl);
  await page.addStyleTag({ path: cssPath });
  await page.addStyleTag({ content: `
    html, body { margin: 0; min-height: 100%; background: #0f1713; color: #fff; }
    #model-origin { width: 375px; min-height: 220px; }
    #model { display: block; width: 100%; min-height: 180px; background: #18251f; }
    .nl-commercial-scene { width: 375px; height: 812px; }
  ` });
  await page.addScriptTag({ path: decisionPath });
  await page.addScriptTag({ path: selectorPath });

  // The host itself is project-scoped. Missing, null, or non-canonical project
  // identity must fail at construction, before a route listener is installed
  // or the one live model Node can be reparented.
  const projectScopeGate = await page.evaluate(() => {
    const model = document.getElementById("model");
    const originalAddEventListener = window.addEventListener;
    let popstateListeners = 0;
    window.addEventListener = function instrumentedAddEventListener(type) {
      if (type === "popstate") popstateListeners += 1;
      return originalAddEventListener.apply(this, arguments);
    };
    const attempts = [
      { name: "omitted", omit: true },
      { name: "null", value: null },
      { name: "invalid", value: "Not A Canonical Contract" }
    ].map((testCase) => {
      const options = { modelNode: model, routeHistory: true };
      if (!testCase.omit) options.projectContractId = testCase.value;
      let error = "";
      try {
        const candidate = new window.NadlanCommercialDecisionSurface.CommercialSceneHost(options);
        candidate.mount({});
      } catch (caught) {
        error = caught.message;
      }
      return { name: testCase.name, error };
    });
    window.addEventListener = originalAddEventListener;
    return {
      attempts,
      popstateListeners,
      modelParent: model.parentElement.id,
      modelCount: document.querySelectorAll("#model").length,
      sceneCount: document.querySelectorAll(".nl-commercial-scene").length
    };
  });
  projectScopeGate.attempts.forEach((attempt) => {
    assert.match(attempt.error, /projectContractId|project contract/i, `${attempt.name} project identity must fail closed`);
  });
  assert.equal(projectScopeGate.popstateListeners, 0, "invalid project scope must install no popstate listener");
  assert.equal(projectScopeGate.modelParent, "model-origin");
  assert.equal(projectScopeGate.modelCount, 1);
  assert.equal(projectScopeGate.sceneCount, 0);

  const atomicMountGate = await page.evaluate((fixtureBaseUrl) => {
    const model = document.getElementById("model");
    const adapter = window.NadlanCommercialContractAdapter;
    const originalAddEventListener = window.addEventListener;
    const originalAppendChild = Element.prototype.appendChild;
    const listenerSignals = [];
    let forceListenerFailure = false;
    window.addEventListener = function instrumentedAddEventListener(type, callback, options) {
      if (type === "popstate") listenerSignals.push(options && options.signal ? options.signal : null);
      if (type === "popstate" && forceListenerFailure) {
        forceListenerFailure = false;
        throw new Error("forced route listener failure");
      }
      return originalAddEventListener.apply(this, arguments);
    };
    const evidence = (value) => ({ __nlCommercialEvidence: true, state: "verified", value, sources: [] });
    const asset = {
      __nlCommercialAsset: true,
      kind: "floor",
      id: "floor-10",
      identityKey: "building-main|tower-a|floor-10|",
      selectable: true,
      wpPostId: 991,
      projectId: "fixture-commercial-contract",
      projectUrl: fixtureBaseUrl,
      url: adapter.identityUrl(fixtureBaseUrl, "fixture-commercial-contract", "building-main", "tower-a", "floor-10", null),
      buildingId: "building-main",
      towerId: "tower-a",
      floorId: "floor-10",
      suiteId: null,
      projectName: "Fixture Commercial Project",
      buildingLabel: "Main Building",
      towerLabel: "Tower A",
      floorLabel: "Floor 10",
      spaceLabel: "",
      availability: evidence("verified_available"),
      exposures: evidence([]),
      beamScene: { state: "unknown", exposures: [], caveat: "Synthetic fixture only." },
      rentableArea: evidence(1250),
      planningCapacity: evidence(120),
      monthlyAllIn: evidence("ILS 210,000"),
      floorPackAvailable: evidence(true),
      fitOutAvailable: evidence(true),
      contextAvailable: evidence(true),
      costAvailable: evidence(true)
    };
    const originalPushState = history.pushState;
    const originalReplaceState = history.replaceState;
    const attempts = [];
    const attempt = (name, options) => {
      const beforeHref = location.href;
      const beforeState = JSON.stringify(history.state);
      const listenerStart = listenerSignals.length;
      let error = "";
      let candidate = null;
      let targetAsset = asset;
      if (options.throwPush) history.pushState = function forcedPushFailure() { throw new DOMException("forced push", "SecurityError"); };
      if (options.throwReplace) history.replaceState = function forcedReplaceFailure() { throw new DOMException("forced replace", "SecurityError"); };
      if (options.throwListener) forceListenerFailure = true;
      if (options.throwModelReparent) {
        Element.prototype.appendChild = function forcedModelReparentFailure(node) {
          if (this.classList && this.classList.contains("nl-commercial-scene__model") && node === model) {
            throw new Error("forced model reparent failure");
          }
          return originalAppendChild.call(this, node);
        };
      }
      try {
        const hostOptions = {
          modelNode: model,
          projectContractId: "fixture-commercial-contract",
          initialHistoryMode: options.historyMode || "replace",
          resolveAsset(key) { return key === asset.identityKey ? asset : null; }
        };
        if (options.controllerFactoryThrows) {
          hostOptions.controllerFactory = function controllerFactoryFailure() { throw new Error("forced controller factory failure"); };
        } else if (options.controllerRenderThrows) {
          hostOptions.controllerFactory = function controllerRenderFailure() {
            return { render() { throw new Error("forced controller render failure"); }, destroy() {} };
          };
        }
        candidate = new window.NadlanCommercialDecisionSurface.CommercialSceneHost(hostOptions);
        targetAsset = options.foreign
          ? Object.assign({}, asset, {
              projectUrl: "https://foreign.invalid/projects/fixture-commercial/",
              url: "https://foreign.invalid/projects/fixture-commercial/?building_id=building-main&floor_id=floor-10&project_contract_id=fixture-commercial-contract&tower_id=tower-a"
            })
          : asset;
        candidate.mount(targetAsset);
      } catch (caught) {
        error = caught.message;
      } finally {
        history.pushState = originalPushState;
        history.replaceState = originalReplaceState;
        Element.prototype.appendChild = originalAppendChild;
        forceListenerFailure = false;
      }
      const attemptSignals = listenerSignals.slice(listenerStart);
      let safeProjectUrl = "";
      if (candidate) {
        const retainedAsset = candidate.currentAsset;
        if (options.foreign) candidate.currentAsset = targetAsset;
        safeProjectUrl = candidate.safeProjectUrl();
        candidate.currentAsset = retainedAsset;
      }
      attempts.push({
        name,
        error,
        hrefUnchanged: location.href === beforeHref,
        stateUnchanged: JSON.stringify(history.state) === beforeState,
        activePopstateListeners: attemptSignals.filter((signal) => !signal || !signal.aborted).length,
        sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
        modelParent: model.parentElement.id,
        modelCount: document.querySelectorAll("#model").length,
        safeProjectUrl,
        currentAsset: candidate && candidate.currentAsset,
        mounted: candidate && candidate.mounted
      });
      if (candidate) candidate.destroy();
    };
    attempt("foreign-origin", { foreign: true });
    attempt("route-listener", { throwListener: true });
    attempt("model-reparent", { throwModelReparent: true });
    attempt("forced-push", { throwPush: true, historyMode: "push" });
    attempt("forced-replace", { throwReplace: true, historyMode: "replace" });
    attempt("controller-factory", { controllerFactoryThrows: true });
    attempt("controller-render", { controllerRenderThrows: true });
    window.addEventListener = originalAddEventListener;
    return attempts;
  }, baseUrl);
  atomicMountGate.forEach((attempt) => {
    assert(attempt.error, `${attempt.name} must fail closed`);
    assert.equal(attempt.hrefUnchanged, true, `${attempt.name} must preserve URL`);
    assert.equal(attempt.stateUnchanged, true, `${attempt.name} must preserve history state`);
    assert.equal(attempt.activePopstateListeners, 0, `${attempt.name} must retain no active popstate listener`);
    assert.equal(attempt.sceneCount, 0, `${attempt.name} must leave no scene`);
    assert.equal(attempt.modelParent, "model-origin", `${attempt.name} must restore the model parent`);
    assert.equal(attempt.modelCount, 1, `${attempt.name} must retain one model`);
    assert.equal(new URL(attempt.safeProjectUrl).origin, new URL(baseUrl).origin, `${attempt.name} safe project URL must remain current-origin`);
    assert.equal(attempt.currentAsset, null, `${attempt.name} must retain no current asset`);
    assert.equal(attempt.mounted, false, `${attempt.name} must not remain mounted`);
  });

  await page.evaluate((fixtureBaseUrl) => {
    history.scrollRestoration = "manual";
    const verified = (value) => ({
      __nlCommercialEvidence: true,
      state: "verified",
      originalState: "verified",
      value,
      unit: null,
      scope: "Synthetic route fixture",
      effectiveAt: "2026-08-11T00:00:00Z",
      verifiedAt: "2026-08-11T00:00:00Z",
      expiresAt: "2099-01-01T00:00:00Z",
      sources: [{
        type: "official_record",
        label: "Synthetic route fixture source",
        uri: "https://example.invalid/source/route-fixture",
        documentId: "ROUTE-FIXTURE-1",
        revision: "fixture-r1"
      }],
      observations: [],
      owner: null,
      confidence: "high",
      reason: "",
      applicability: ["commercial_office"],
      conflictIds: [],
      note: "",
      caveat: "Synthetic fixture only.",
      requiredDocumentIds: [],
      decisionGrade: true,
      issues: []
    });
    const unknown = () => ({
      __nlCommercialEvidence: true,
      state: "unknown",
      originalState: "unknown",
      value: null,
      unit: null,
      scope: null,
      effectiveAt: "",
      verifiedAt: "",
      expiresAt: "",
      sources: [],
      observations: [],
      owner: null,
      confidence: "unknown",
      reason: "No synthetic value supplied.",
      applicability: ["commercial_office"],
      conflictIds: [],
      note: "",
      caveat: "",
      requiredDocumentIds: [],
      decisionGrade: false,
      issues: []
    });
    const adapter = window.NadlanCommercialContractAdapter;
    const makeAsset = (towerId, towerLabel, suiteId = null) => {
      const floorId = "floor-10";
      const projectId = "fixture-commercial-contract";
      const identityKey = adapter.commercialIdentityKey("building-main", towerId, floorId, suiteId);
      return {
        __nlCommercialAsset: true,
        kind: suiteId ? "suite" : "floor",
        id: suiteId || floorId,
        identityKey,
        selectable: true,
        wpPostId: 991,
        projectId,
        projectUrl: fixtureBaseUrl,
        url: adapter.identityUrl(fixtureBaseUrl, projectId, "building-main", towerId, floorId, suiteId),
        buildingId: "building-main",
        towerId,
        floorId,
        suiteId,
        projectName: "Fixture Commercial Project",
        buildingLabel: "Main Building",
        towerLabel,
        floorLabel: "Floor 10",
        spaceLabel: suiteId ? `Suite ${suiteId.slice(-1).toUpperCase()}` : "",
        availability: verified("verified_available"),
        exposures: unknown(),
        beamScene: { state: "unknown", exposures: [], caveat: "Synthetic fixture only." },
        rentableArea: verified(1250),
        planningCapacity: verified(120),
        monthlyAllIn: verified("ILS 210,000"),
        floorPackAvailable: verified(true),
        fitOutAvailable: verified(true),
        contextAvailable: verified(true),
        costAvailable: verified(true)
      };
    };
    const assets = {
      a: makeAsset("tower-a", "Tower A"),
      b: makeAsset("tower-b", "Tower B"),
      suiteA: makeAsset("tower-a", "Tower A", "suite-a"),
      suiteB: makeAsset("tower-a", "Tower A", "suite-b")
    };
    const byKey = Object.fromEntries(Object.values(assets).map((asset) => [asset.identityKey, asset]));
    const ranges = [assets.a, assets.b].map((asset) => ({
      buildingId: asset.buildingId,
      towerId: asset.towerId,
      towerLabel: asset.towerLabel,
      floorId: asset.floorId,
      identityKey: asset.identityKey,
      minY: 0,
      maxY: 10,
      selectable: true,
      displayOrder: asset.towerId === "tower-a" ? 1 : 2,
      label: asset.floorLabel,
      zone: "",
      status: "verified_available",
      availability: verified("verified_available"),
      calibrationEvidence: verified(true),
      zoneEvidence: unknown(),
      areaEvidence: verified(1250)
    }));
    const model = document.getElementById("model");
    model.positionAndNormalFromPoint = () => Promise.resolve({
      position: { y: 5 },
      towerId: window.__routeFixtureHitTower
    });
    window.__selectionLifecycle = { highlights: [], clears: [] };
    const selector = new window.NadlanCommercialFloorSelector.CommercialFloorSelector({
      modelViewer: model,
      floorRanges: ranges,
      selectElement: document.getElementById("floor-picker"),
      previousButton: document.getElementById("previous"),
      nextButton: document.getElementById("next"),
      liveRegion: document.getElementById("live"),
      projectId: "fixture-commercial-contract",
      highlightFloor(range) { window.__selectionLifecycle.highlights.push(range.identityKey); },
      clearHighlight(range) { window.__selectionLifecycle.clears.push(range.identityKey); },
      resolveTowerFromHit(hit) {
        return { buildingId: "building-main", towerId: hit.towerId };
      }
    }).attach();
    document.getElementById("origin-focus").focus();
    history.replaceState({ fixtureBase: true }, "", fixtureBaseUrl);
    window.__invalidRouteSelections = [];
    window.__buildingExitCount = 0;
    const host = new window.NadlanCommercialDecisionSurface.CommercialSceneHost({
      modelNode: model,
      labels: { locale: "en", dir: "ltr" },
      projectContractId: "fixture-commercial-contract",
      initialHistoryMode: "push",
      resolveAsset(key) { return byKey[key] || null; },
      onInvalidRoute(detail) { window.__invalidRouteSelections.push(detail.reason); },
      onExit() { window.__buildingExitCount += 1; }
    });
    host.mount(assets.a, { origin: "initial-model-selection" });
    window.__routeFixture = { assets, byKey, selector, host, model, baseUrl: fixtureBaseUrl };
  }, baseUrl);

  const initial = await page.evaluate(() => ({
    href: location.href,
    state: history.state,
    selected: window.__routeFixture.host.currentAsset.identityKey,
    expectedHref: window.__routeFixture.assets.a.url,
    picker: document.getElementById("floor-picker").value,
    model: window.__routeFixture.model.dataset.selectedFloor,
    sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
    modelCount: document.querySelectorAll("#model").length
  }));
  assert.equal(initial.href, initial.expectedHref);
  assert.equal(initial.state.nlCommercialAsset.projectContractId, "fixture-commercial-contract");
  assert.equal(initial.state.nlCommercialAsset.towerId, "tower-a");
  assert.equal(initial.state.nlCommercialAsset.floorId, "floor-10");
  assert.equal(initial.state.nlCommercialAsset.suiteId, null);
  assert.equal(new URL(initial.href).searchParams.get("project_contract_id"), "fixture-commercial-contract");
  assert.equal(new URL(initial.href).searchParams.has("wp_post_id"), false, "routing-only WP post ID must not enter the canonical browser URL");
  assert.equal(initial.selected, initial.picker);
  assert.equal(initial.selected, initial.model);
  assert.equal(initial.sceneCount, 1);
  assert.equal(initial.modelCount, 1);

  const forcedSelectionRollback = await page.evaluate(() => {
    const fixture = window.__routeFixture;
    const before = {
      href: location.href,
      state: JSON.stringify(history.state),
      identityKey: fixture.host.currentAsset.identityKey,
      picker: document.getElementById("floor-picker").value,
      model: fixture.model.dataset.selectedFloor,
      heading: document.querySelector("#nl-cds-title").textContent,
      invalidCount: window.__invalidRouteSelections.length
    };
    const originalPushState = history.pushState;
    history.pushState = function forcedSelectionPushFailure() { throw new DOMException("forced selection push", "SecurityError"); };
    try {
      fixture.selector.selectFloor(fixture.assets.b.identityKey, "picker");
    } finally {
      history.pushState = originalPushState;
    }
    return {
      before,
      after: {
        href: location.href,
        state: JSON.stringify(history.state),
        identityKey: fixture.host.currentAsset.identityKey,
        picker: document.getElementById("floor-picker").value,
        model: fixture.model.dataset.selectedFloor,
        heading: document.querySelector("#nl-cds-title").textContent,
        invalidCount: window.__invalidRouteSelections.length,
        sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
        modelCount: document.querySelectorAll("#model").length,
        dialogCount: document.querySelectorAll("dialog.nl-commercial-tool").length,
        htmlOverflow: document.documentElement.style.overflow,
        bodyOverflow: document.body.style.overflow
      }
    };
  });
  assert.equal(forcedSelectionRollback.after.href, forcedSelectionRollback.before.href);
  assert.equal(forcedSelectionRollback.after.state, forcedSelectionRollback.before.state);
  assert.equal(forcedSelectionRollback.after.identityKey, forcedSelectionRollback.before.identityKey);
  assert.equal(forcedSelectionRollback.after.picker, forcedSelectionRollback.before.picker);
  assert.equal(forcedSelectionRollback.after.model, forcedSelectionRollback.before.model);
  assert.equal(forcedSelectionRollback.after.heading, forcedSelectionRollback.before.heading);
  assert.equal(forcedSelectionRollback.after.invalidCount, forcedSelectionRollback.before.invalidCount + 1);
  assert.equal(forcedSelectionRollback.after.sceneCount, 1);
  assert.equal(forcedSelectionRollback.after.modelCount, 1);
  assert.equal(forcedSelectionRollback.after.dialogCount, 0);
  assert.equal(forcedSelectionRollback.after.htmlOverflow, "");
  assert.equal(forcedSelectionRollback.after.bodyOverflow, "");

  // A mounted asset renderer can fail after mutating its own root. Rendering
  // is staged before pushState, so the failed switch creates no semantic
  // history entry and restores the exact prior surface/selection. The already
  // open tool stays open with its original marker, focus, inert and scroll
  // lock; the next valid selection then succeeds and closes it normally.
  const mountedRenderRollback = await page.evaluate(async () => {
    const fixture = window.__routeFixture;
    const host = fixture.host;
    const controller = host.decisionController;
    const toolButton = document.querySelector('[data-act="open-tool"][data-tool="floor-pack"]');
    toolButton.click();
    await new Promise((resolve) => requestAnimationFrame(resolve));
    const dialog = document.querySelector("dialog.nl-commercial-tool");
    const before = {
      href: location.href,
      state: JSON.stringify(history.state),
      historyLength: history.length,
      identityKey: host.currentAsset.identityKey,
      controllerIdentityKey: controller.asset.identityKey,
      picker: document.getElementById("floor-picker").value,
      model: fixture.model.dataset.selectedFloor,
      markup: host.decisionSlot.innerHTML,
      heading: document.querySelector("#nl-cds-title").textContent,
      dialog,
      dialogOpen: Boolean(dialog && dialog.open),
      dialogAsset: controller.toolDialog.asset && controller.toolDialog.asset.identityKey,
      toolMarker: history.state && history.state.nlCommercialTool && history.state.nlCommercialTool.tool,
      rootInert: controller.root.inert,
      htmlOverflow: document.documentElement.style.overflow,
      bodyPosition: document.body.style.position,
      focusInsideDialog: Boolean(dialog && dialog.contains(document.activeElement)),
      triggerConnected: Boolean(controller.toolDialog.trigger && controller.toolDialog.trigger.isConnected),
      invalidCount: window.__invalidRouteSelections.length
    };
    const originalRender = controller.render;
    controller.render = function forcedMountedAssetRenderFailure(asset) {
      const result = originalRender.call(this, asset);
      if (asset.identityKey === fixture.assets.b.identityKey) {
        throw new Error("forced mounted asset render failure after DOM mutation");
      }
      return result;
    };
    try {
      fixture.selector.selectFloor(fixture.assets.b.identityKey, "picker");
    } finally {
      controller.render = originalRender;
    }
    const afterFailure = {
      href: location.href,
      state: JSON.stringify(history.state),
      historyLength: history.length,
      identityKey: host.currentAsset.identityKey,
      controllerIdentityKey: controller.asset.identityKey,
      picker: document.getElementById("floor-picker").value,
      model: fixture.model.dataset.selectedFloor,
      markup: host.decisionSlot.innerHTML,
      heading: document.querySelector("#nl-cds-title").textContent,
      sameDialog: dialog === document.querySelector("dialog.nl-commercial-tool"),
      dialogOpen: Boolean(dialog && dialog.open),
      dialogAsset: controller.toolDialog.asset && controller.toolDialog.asset.identityKey,
      toolMarker: history.state && history.state.nlCommercialTool && history.state.nlCommercialTool.tool,
      rootInert: controller.root.inert,
      htmlOverflow: document.documentElement.style.overflow,
      bodyPosition: document.body.style.position,
      focusInsideDialog: Boolean(dialog && dialog.contains(document.activeElement)),
      triggerConnected: Boolean(controller.toolDialog.trigger && controller.toolDialog.trigger.isConnected),
      triggerMatchesRestoredDoor: controller.toolDialog.trigger === document.querySelector('[data-act="open-tool"][data-tool="floor-pack"]'),
      invalidCount: window.__invalidRouteSelections.length
    };
    dialog.querySelector('[data-act="close-tool"]').click();
    await new Promise((resolve) => {
      function waitForToolClose() {
        if (!document.querySelector("dialog.nl-commercial-tool")) resolve();
        else requestAnimationFrame(waitForToolClose);
      }
      requestAnimationFrame(waitForToolClose);
    });
    await new Promise((resolve) => requestAnimationFrame(resolve));
    const restoredDoor = document.querySelector('[data-act="open-tool"][data-tool="floor-pack"]');
    const afterClose = {
      href: location.href,
      identityKey: host.currentAsset.identityKey,
      controllerIdentityKey: controller.asset.identityKey,
      picker: document.getElementById("floor-picker").value,
      model: fixture.model.dataset.selectedFloor,
      dialogCount: document.querySelectorAll("dialog.nl-commercial-tool").length,
      hasToolMarker: Boolean(history.state && history.state.nlCommercialTool),
      focusedRestoredDoor: document.activeElement === restoredDoor,
      restoredDoorConnected: Boolean(restoredDoor && restoredDoor.isConnected),
      rootInert: controller.root.inert,
      htmlOverflow: document.documentElement.style.overflow,
      bodyPosition: document.body.style.position
    };
    fixture.selector.selectFloor(fixture.assets.b.identityKey, "picker");
    const afterRecovery = {
      href: location.href,
      stateAsset: history.state && history.state.nlCommercialAsset && history.state.nlCommercialAsset.towerId,
      hasToolMarker: Boolean(history.state && history.state.nlCommercialTool),
      historyLength: history.length,
      identityKey: host.currentAsset.identityKey,
      controllerIdentityKey: controller.asset.identityKey,
      picker: document.getElementById("floor-picker").value,
      model: fixture.model.dataset.selectedFloor,
      dialogCount: document.querySelectorAll("dialog.nl-commercial-tool").length,
      rootInert: controller.root.inert,
      htmlOverflow: document.documentElement.style.overflow,
      bodyPosition: document.body.style.position
    };
    return { before, afterFailure, afterClose, afterRecovery };
  });
  assert.equal(mountedRenderRollback.afterFailure.href, mountedRenderRollback.before.href);
  assert.equal(mountedRenderRollback.afterFailure.state, mountedRenderRollback.before.state);
  assert.equal(mountedRenderRollback.afterFailure.historyLength, mountedRenderRollback.before.historyLength, "failed renderer must not add a push entry");
  assert.equal(mountedRenderRollback.afterFailure.identityKey, mountedRenderRollback.before.identityKey);
  assert.equal(mountedRenderRollback.afterFailure.controllerIdentityKey, mountedRenderRollback.before.controllerIdentityKey);
  assert.equal(mountedRenderRollback.afterFailure.picker, mountedRenderRollback.before.picker);
  assert.equal(mountedRenderRollback.afterFailure.model, mountedRenderRollback.before.model);
  assert.equal(mountedRenderRollback.afterFailure.markup, mountedRenderRollback.before.markup);
  assert.equal(mountedRenderRollback.afterFailure.heading, mountedRenderRollback.before.heading);
  assert.equal(mountedRenderRollback.afterFailure.sameDialog, true);
  assert.equal(mountedRenderRollback.afterFailure.dialogOpen, true);
  assert.equal(mountedRenderRollback.afterFailure.dialogAsset, mountedRenderRollback.before.dialogAsset);
  assert.equal(mountedRenderRollback.afterFailure.toolMarker, mountedRenderRollback.before.toolMarker);
  assert.equal(mountedRenderRollback.afterFailure.rootInert, mountedRenderRollback.before.rootInert);
  assert.equal(mountedRenderRollback.afterFailure.htmlOverflow, mountedRenderRollback.before.htmlOverflow);
  assert.equal(mountedRenderRollback.afterFailure.bodyPosition, mountedRenderRollback.before.bodyPosition);
  assert.equal(mountedRenderRollback.afterFailure.focusInsideDialog, true);
  assert.equal(mountedRenderRollback.before.triggerConnected, true);
  assert.equal(mountedRenderRollback.afterFailure.triggerConnected, true, "rollback must remap the tool focus target to a connected door");
  assert.equal(mountedRenderRollback.afterFailure.triggerMatchesRestoredDoor, true);
  assert.equal(mountedRenderRollback.afterFailure.invalidCount, mountedRenderRollback.before.invalidCount + 1);
  assert.equal(mountedRenderRollback.afterClose.href, mountedRenderRollback.before.href);
  assert.equal(mountedRenderRollback.afterClose.identityKey, mountedRenderRollback.before.identityKey);
  assert.equal(mountedRenderRollback.afterClose.controllerIdentityKey, mountedRenderRollback.before.controllerIdentityKey);
  assert.equal(mountedRenderRollback.afterClose.picker, mountedRenderRollback.before.picker);
  assert.equal(mountedRenderRollback.afterClose.model, mountedRenderRollback.before.model);
  assert.equal(mountedRenderRollback.afterClose.dialogCount, 0);
  assert.equal(mountedRenderRollback.afterClose.hasToolMarker, false);
  assert.equal(mountedRenderRollback.afterClose.focusedRestoredDoor, true, "Back must focus the connected replacement door");
  assert.equal(mountedRenderRollback.afterClose.restoredDoorConnected, true);
  assert.equal(mountedRenderRollback.afterClose.rootInert, false);
  assert.equal(mountedRenderRollback.afterClose.htmlOverflow, "");
  assert.equal(mountedRenderRollback.afterClose.bodyPosition, "");
  assert.equal(new URL(mountedRenderRollback.afterRecovery.href).searchParams.get("tower_id"), "tower-b");
  assert.equal(mountedRenderRollback.afterRecovery.stateAsset, "tower-b");
  assert.equal(mountedRenderRollback.afterRecovery.hasToolMarker, false);
  assert.equal(mountedRenderRollback.afterRecovery.historyLength, mountedRenderRollback.before.historyLength, "valid selection replaces the discarded forward tool entry with one asset entry");
  assert.equal(mountedRenderRollback.afterRecovery.identityKey, "building-main|tower-b|floor-10|");
  assert.equal(mountedRenderRollback.afterRecovery.controllerIdentityKey, mountedRenderRollback.afterRecovery.identityKey);
  assert.equal(mountedRenderRollback.afterRecovery.picker, mountedRenderRollback.afterRecovery.identityKey);
  assert.equal(mountedRenderRollback.afterRecovery.model, mountedRenderRollback.afterRecovery.identityKey);
  assert.equal(mountedRenderRollback.afterRecovery.dialogCount, 0);
  assert.equal(mountedRenderRollback.afterRecovery.rootInert, false);
  assert.equal(mountedRenderRollback.afterRecovery.htmlOverflow, "");
  assert.equal(mountedRenderRollback.afterRecovery.bodyPosition, "");

  // Return to Tower A so the remaining suite and picker history scenarios keep
  // their original deterministic baseline.
  await page.goBack();
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.identityKey === "building-main|tower-a|floor-10|");

  // A supplied suite identity is part of the immutable event tuple. A Suite A
  // identity key paired with Suite B or explicit null must fail closed without
  // changing URL/state; the exact matching event selects Suite A. Back then
  // restores the original floor entry before the floor-picker sequence.
  const suiteEvents = await page.evaluate(() => {
    const fixture = window.__routeFixture;
    const startInvalidCount = window.__invalidRouteSelections.length;
    const dispatchSuite = (suiteId) => {
      fixture.model.dispatchEvent(new CustomEvent("nadlan:commercial-asset-selected", {
        bubbles: true,
        detail: {
          projectId: "fixture-commercial-contract",
          buildingId: "building-main",
          towerId: "tower-a",
          floorId: "floor-10",
          suiteId,
          identityKey: fixture.assets.suiteA.identityKey,
          origin: "suite-fixture"
        }
      }));
    };
    const beforeHref = location.href;
    dispatchSuite("suite-b");
    const afterWrongSuite = {
      href: location.href,
      identityKey: fixture.host.currentAsset.identityKey,
      invalidCount: window.__invalidRouteSelections.length
    };
    dispatchSuite(null);
    const afterExplicitNull = {
      href: location.href,
      identityKey: fixture.host.currentAsset.identityKey,
      invalidCount: window.__invalidRouteSelections.length
    };
    dispatchSuite("suite-a");
    return {
      startInvalidCount,
      beforeHref,
      afterWrongSuite,
      afterExplicitNull,
      matched: {
        href: location.href,
        identityKey: fixture.host.currentAsset.identityKey,
        suiteId: fixture.host.currentAsset.suiteId,
        stateSuiteId: history.state.nlCommercialAsset.suiteId,
        picker: document.getElementById("floor-picker").value,
        model: fixture.model.dataset.selectedFloor
      }
    };
  });
  assert.equal(suiteEvents.afterWrongSuite.href, suiteEvents.beforeHref);
  assert.equal(suiteEvents.afterWrongSuite.identityKey, "building-main|tower-a|floor-10|");
  assert.equal(suiteEvents.afterWrongSuite.invalidCount, suiteEvents.startInvalidCount + 1);
  assert.equal(suiteEvents.afterExplicitNull.href, suiteEvents.beforeHref);
  assert.equal(suiteEvents.afterExplicitNull.identityKey, "building-main|tower-a|floor-10|");
  assert.equal(suiteEvents.afterExplicitNull.invalidCount, suiteEvents.startInvalidCount + 2);
  assert.equal(suiteEvents.matched.identityKey, "building-main|tower-a|floor-10|suite-a");
  assert.equal(suiteEvents.matched.suiteId, "suite-a");
  assert.equal(suiteEvents.matched.stateSuiteId, "suite-a");
  assert.equal(new URL(suiteEvents.matched.href).searchParams.get("suite_id"), "suite-a");
  assert.equal(suiteEvents.matched.picker, "building-main|tower-a|floor-10|");
  assert.equal(suiteEvents.matched.model, suiteEvents.matched.picker);
  await page.goBack();
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.suiteId === null);

  // Native picker selects Tower B / Floor 10 and writes its exact route.
  await page.selectOption("#floor-picker", "building-main|tower-b|floor-10|");
  await page.waitForFunction(() => history.state && history.state.nlCommercialAsset && history.state.nlCommercialAsset.towerId === "tower-b");
  const pickerSelection = await page.evaluate(() => ({
    href: location.href,
    state: history.state.nlCommercialAsset,
    selected: window.__routeFixture.host.currentAsset.identityKey,
    picker: document.getElementById("floor-picker").value,
    model: window.__routeFixture.model.dataset.selectedFloor
  }));
  assert.equal(pickerSelection.state.towerId, "tower-b");
  assert.equal(pickerSelection.selected, "building-main|tower-b|floor-10|");
  assert.equal(pickerSelection.selected, pickerSelection.picker);
  assert.equal(pickerSelection.selected, pickerSelection.model);
  assert.equal(new URL(pickerSelection.href).searchParams.get("tower_id"), "tower-b");

  // A model-space hit on the same visible floor label but Tower A selects the
  // distinct immutable identity and reaches the same canonical state machine.
  await page.evaluate(async () => {
    window.__routeFixtureHitTower = "tower-a";
    await window.__routeFixture.selector.selectFromPoint(20, 20, "model");
  });
  await page.waitForFunction(() => history.state.nlCommercialAsset.towerId === "tower-a");
  const modelSelection = await page.evaluate(() => ({
    href: location.href,
    state: history.state.nlCommercialAsset,
    selected: window.__routeFixture.host.currentAsset.identityKey,
    picker: document.getElementById("floor-picker").value,
    model: window.__routeFixture.model.dataset.selectedFloor
  }));
  assert.equal(modelSelection.state.towerId, "tower-a");
  assert.equal(modelSelection.selected, modelSelection.picker);
  assert.equal(modelSelection.selected, modelSelection.model);
  assert.equal(new URL(modelSelection.href).searchParams.get("tower_id"), "tower-a");

  // A fullscreen tool is a child history entry. It retains the exact asset
  // marker, Back closes only the tool, and Forward reopens only that tool/asset.
  await page.click('[data-act="open-tool"][data-tool="cost"]');
  await page.waitForSelector("dialog.nl-commercial-tool[open]");
  const toolState = await page.evaluate(() => history.state);
  assert.equal(toolState.nlCommercialAsset.towerId, "tower-a");
  assert.equal(toolState.nlCommercialTool.towerId, "tower-a");
  assert.equal(toolState.nlCommercialTool.projectContractId, toolState.nlCommercialAsset.projectContractId);
  await page.goBack();
  await page.waitForFunction(() => !document.querySelector("dialog.nl-commercial-tool"));
  assert.equal((await page.evaluate(() => history.state.nlCommercialAsset.towerId)), "tower-a");
  await page.goBack();
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-b");
  const selectionBack = await page.evaluate(() => ({
    tower: window.__routeFixture.host.currentAsset.towerId,
    picker: document.getElementById("floor-picker").value,
    model: window.__routeFixture.model.dataset.selectedFloor,
    tool: history.state.nlCommercialTool || null
  }));
  assert.equal(selectionBack.tower, "tower-b");
  assert.equal(selectionBack.picker, "building-main|tower-b|floor-10|");
  assert.equal(selectionBack.model, selectionBack.picker);
  assert.equal(selectionBack.tool, null);
  await page.goForward();
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset.towerId === "tower-a");
  await page.goForward();
  await page.waitForSelector("dialog.nl-commercial-tool[open]");
  assert.equal((await page.evaluate(() => history.state.nlCommercialTool.towerId)), "tower-a");
  await page.goBack();
  await page.waitForFunction(() => !document.querySelector("dialog.nl-commercial-tool"));

  // The visible Building action creates a route-free child entry and suspends
  // the host without destroying its popstate lifecycle. Back restores Tower B,
  // Back again restores Tower A, and Forward traverses both exact selections
  // plus the Building entry with one model, no stale tool, and no page lock.
  await page.goBack(); // Tower B.
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-b");
  const beforeBuildingCounts = await page.evaluate(() => ({
    highlights: window.__selectionLifecycle.highlights.length,
    clears: window.__selectionLifecycle.clears.length
  }));
  await page.click('[data-act="back-to-building"]');
  await page.waitForFunction(() => !document.querySelector(".nl-commercial-scene") && document.activeElement.id === "origin-focus");
  const buildingEntry = await page.evaluate(() => ({
    href: location.href,
    mounted: window.__routeFixture.host.mounted,
    destroyed: window.__routeFixture.host.destroyed,
    exitCount: window.__buildingExitCount,
    modelParent: document.getElementById("model").parentElement.id,
    modelCount: document.querySelectorAll("#model").length,
    sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
    assetMarker: history.state && history.state.nlCommercialAsset,
    toolMarker: history.state && history.state.nlCommercialTool,
    picker: document.getElementById("floor-picker").value,
    selectorIdentity: window.__routeFixture.selector.selectedIdentityKey,
    selectedAttribute: window.__routeFixture.model.hasAttribute("data-selected-floor"),
    clears: window.__selectionLifecycle.clears.length,
    dialogCount: document.querySelectorAll("dialog.nl-commercial-tool").length,
    htmlOverflow: document.documentElement.style.overflow,
    bodyOverflow: document.body.style.overflow
  }));
  assert.equal(buildingEntry.href, baseUrl);
  assert.equal(buildingEntry.mounted, false);
  assert.equal(buildingEntry.destroyed, false, "Building must suspend, not permanently destroy, the route host");
  assert.equal(buildingEntry.exitCount, 1);
  assert.equal(buildingEntry.modelParent, "model-origin");
  assert.equal(buildingEntry.modelCount, 1);
  assert.equal(buildingEntry.sceneCount, 0);
  assert.equal(buildingEntry.assetMarker, undefined);
  assert.equal(buildingEntry.toolMarker, undefined);
  assert.equal(buildingEntry.picker, "");
  assert.equal(buildingEntry.selectorIdentity, "");
  assert.equal(buildingEntry.selectedAttribute, false);
  assert.equal(buildingEntry.clears, beforeBuildingCounts.clears + 1, "Building suspension must clear the exact prior highlight once");
  assert.equal(buildingEntry.dialogCount, 0);
  assert.equal(buildingEntry.htmlOverflow, "");
  assert.equal(buildingEntry.bodyOverflow, "");

  await page.goBack(); // Exact Tower B selection.
  await page.waitForFunction(() => document.querySelector(".nl-commercial-scene") && window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-b");
  const buildingBackB = await page.evaluate(() => ({
    href: location.href,
    picker: document.getElementById("floor-picker").value,
    model: window.__routeFixture.model.dataset.selectedFloor,
    sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
    modelCount: document.querySelectorAll("#model").length,
    tool: history.state.nlCommercialTool || null,
    highlights: window.__selectionLifecycle.highlights.length,
    clears: window.__selectionLifecycle.clears.length,
    htmlOverflow: document.documentElement.style.overflow,
    bodyOverflow: document.body.style.overflow
  }));
  assert.equal(buildingBackB.href, pickerSelection.href);
  assert.equal(buildingBackB.picker, "building-main|tower-b|floor-10|");
  assert.equal(buildingBackB.model, buildingBackB.picker);
  assert.equal(buildingBackB.sceneCount, 1);
  assert.equal(buildingBackB.modelCount, 1);
  assert.equal(buildingBackB.tool, null);
  assert.equal(buildingBackB.highlights, beforeBuildingCounts.highlights + 1, "Back must restore the floor highlight exactly once");
  assert.equal(buildingBackB.clears, beforeBuildingCounts.clears + 1);
  assert.equal(buildingBackB.htmlOverflow, "");
  assert.equal(buildingBackB.bodyOverflow, "");

  await page.goBack(); // Initial Tower A.
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-a");
  assert.equal((await page.evaluate(() => location.href)), initial.expectedHref);
  await page.goForward(); // Tower B.
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-b");
  assert.equal((await page.evaluate(() => document.querySelectorAll(".nl-commercial-scene").length)), 1);
  await page.goForward(); // Route-free Building entry.
  await page.waitForFunction(() => !document.querySelector(".nl-commercial-scene"));
  const buildingForward = await page.evaluate(() => ({
    href: location.href,
    picker: document.getElementById("floor-picker").value,
    selectorIdentity: window.__routeFixture.selector.selectedIdentityKey,
    modelSelected: window.__routeFixture.model.hasAttribute("data-selected-floor"),
    modelCount: document.querySelectorAll("#model").length,
    clears: window.__selectionLifecycle.clears.length,
    dialogCount: document.querySelectorAll("dialog.nl-commercial-tool").length,
    htmlOverflow: document.documentElement.style.overflow,
    bodyOverflow: document.body.style.overflow
  }));
  assert.equal(buildingForward.href, baseUrl);
  assert.equal(buildingForward.picker, "");
  assert.equal(buildingForward.selectorIdentity, "");
  assert.equal(buildingForward.modelSelected, false);
  assert.equal(buildingForward.modelCount, 1);
  assert.equal(buildingForward.clears, beforeBuildingCounts.clears + 2, "Forward to Building must clear the restored highlight exactly once");
  assert.equal(buildingForward.dialogCount, 0);
  assert.equal(buildingForward.htmlOverflow, "");
  assert.equal(buildingForward.bodyOverflow, "");
  await page.goBack(); // Return to Tower B.
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-b");

  // The original route-free base entry uses the same exact-once clear/restore
  // lifecycle as the visible Building action.
  const beforeNaturalBase = await page.evaluate(() => ({
    highlights: window.__selectionLifecycle.highlights.length,
    clears: window.__selectionLifecycle.clears.length
  }));
  await page.goBack(); // Initial Tower A.
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-a");
  await page.goBack(); // Original route-free base.
  await page.waitForFunction(() => !document.querySelector(".nl-commercial-scene"));
  const naturalBaseBack = await page.evaluate(() => ({
    href: location.href,
    mounted: window.__routeFixture.host.mounted,
    destroyed: window.__routeFixture.host.destroyed,
    picker: document.getElementById("floor-picker").value,
    selectorIdentity: window.__routeFixture.selector.selectedIdentityKey,
    modelSelected: window.__routeFixture.model.hasAttribute("data-selected-floor"),
    modelParent: window.__routeFixture.model.parentElement.id,
    modelCount: document.querySelectorAll("#model").length,
    sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
    clears: window.__selectionLifecycle.clears.length,
    tool: history.state.nlCommercialTool || null,
    htmlOverflow: document.documentElement.style.overflow,
    bodyOverflow: document.body.style.overflow
  }));
  assert.equal(naturalBaseBack.href, baseUrl);
  assert.equal(naturalBaseBack.mounted, false);
  assert.equal(naturalBaseBack.destroyed, false);
  assert.equal(naturalBaseBack.picker, "");
  assert.equal(naturalBaseBack.selectorIdentity, "");
  assert.equal(naturalBaseBack.modelSelected, false);
  assert.equal(naturalBaseBack.modelParent, "model-origin");
  assert.equal(naturalBaseBack.modelCount, 1);
  assert.equal(naturalBaseBack.sceneCount, 0);
  assert.equal(naturalBaseBack.clears, beforeNaturalBase.clears + 1, "route-free Back must clear the active highlight once");
  assert.equal(naturalBaseBack.tool, null);
  assert.equal(naturalBaseBack.htmlOverflow, "");
  assert.equal(naturalBaseBack.bodyOverflow, "");
  await page.goForward(); // Initial Tower A remount.
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-a");
  const naturalForward = await page.evaluate(() => ({
    href: location.href,
    picker: document.getElementById("floor-picker").value,
    model: window.__routeFixture.model.dataset.selectedFloor,
    highlights: window.__selectionLifecycle.highlights.length,
    clears: window.__selectionLifecycle.clears.length,
    modelCount: document.querySelectorAll("#model").length,
    sceneCount: document.querySelectorAll(".nl-commercial-scene").length
  }));
  assert.equal(naturalForward.href, initial.expectedHref);
  assert.equal(naturalForward.picker, "building-main|tower-a|floor-10|");
  assert.equal(naturalForward.model, naturalForward.picker);
  assert.equal(naturalForward.highlights, beforeNaturalBase.highlights + 2, "Back to A then Forward remount must each synchronize one highlight");
  assert.equal(naturalForward.clears, beforeNaturalBase.clears + 1);
  assert.equal(naturalForward.modelCount, 1);
  assert.equal(naturalForward.sceneCount, 1);
  await page.goForward(); // Return to Tower B for the deep-link case.
  await page.waitForFunction(() => window.__routeFixture.host.currentAsset && window.__routeFixture.host.currentAsset.towerId === "tower-b");

  // A direct canonical deep link is equivalent to picker/model selection and
  // wins over a conflicting fallback initialAsset argument.
  await page.evaluate(() => {
    const fixture = window.__routeFixture;
    fixture.host.destroy();
    history.replaceState({}, "", fixture.assets.suiteB.url);
    const nextHost = new window.NadlanCommercialDecisionSurface.CommercialSceneHost({
      modelNode: fixture.model,
      labels: { locale: "en", dir: "ltr" },
      projectContractId: "fixture-commercial-contract",
      resolveAsset(key) { return fixture.byKey[key] || null; }
    });
    nextHost.mount(fixture.assets.a);
    fixture.host = nextHost;
  });
  const deepLink = await page.evaluate(() => ({
    href: location.href,
    tower: window.__routeFixture.host.currentAsset.towerId,
    suiteId: window.__routeFixture.host.currentAsset.suiteId,
    stateTower: history.state.nlCommercialAsset.towerId,
    stateSuiteId: history.state.nlCommercialAsset.suiteId,
    picker: document.getElementById("floor-picker").value,
    model: window.__routeFixture.model.dataset.selectedFloor,
    modelCount: document.querySelectorAll("#model").length
  }));
  assert.equal(deepLink.tower, "tower-a");
  assert.equal(deepLink.suiteId, "suite-b");
  assert.equal(deepLink.stateTower, "tower-a");
  assert.equal(deepLink.stateSuiteId, "suite-b");
  assert.equal(new URL(deepLink.href).searchParams.get("suite_id"), "suite-b");
  assert.equal(deepLink.picker, "building-main|tower-a|floor-10|");
  assert.equal(deepLink.model, deepLink.picker);
  assert.equal(deepLink.modelCount, 1);

  // Missing and stale tuples fail before the model is reparented or a surface
  // is rendered. They cannot fall through to a visible-label floor match.
  const invalidRoutes = await page.evaluate(() => {
    const fixture = window.__routeFixture;
    fixture.host.destroy();
    fixture.selector.destroy();
    const attempts = [];
    const tryRoute = (url) => {
      history.replaceState({}, "", url);
      const candidate = new window.NadlanCommercialDecisionSurface.CommercialSceneHost({
        modelNode: fixture.model,
        projectContractId: "fixture-commercial-contract",
        resolveAsset(key) { return fixture.byKey[key] || null; }
      });
      let error = "";
      try { candidate.mount(fixture.assets.a); } catch (caught) { error = caught.message; }
      attempts.push({
        error,
        sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
        modelParent: fixture.model.parentElement.id,
        modelCount: document.querySelectorAll("#model").length
      });
      candidate.destroy();
    };
    tryRoute(fixture.baseUrl + "?building_id=building-main&tower_id=tower-a");
    tryRoute(fixture.baseUrl + "?project_contract_id=fixture-commercial-contract&building_id=building-main&tower_id=tower-a&floor_id=floor-missing");
    return attempts;
  });
  invalidRoutes.forEach((attempt) => {
    assert.match(attempt.error, /tuple|resolve|selectable|asset/i);
    assert.equal(attempt.sceneCount, 0);
    assert.equal(attempt.modelParent, "model-origin");
    assert.equal(attempt.modelCount, 1);
  });

  const cleanupFailures = await page.evaluate(() => {
    const fixture = window.__routeFixture;
    const originalPushState = history.pushState;
    const originalReplaceState = history.replaceState;
    originalReplaceState.call(history, { atomicBase: true }, "", fixture.baseUrl);
    fixture.selector.attach();
    const invalidReasons = [];
    const host = new window.NadlanCommercialDecisionSurface.CommercialSceneHost({
      modelNode: fixture.model,
      labels: { locale: "en", dir: "ltr" },
      projectContractId: "fixture-commercial-contract",
      resolveAsset(key) { return fixture.byKey[key] || null; },
      onInvalidRoute(detail) { invalidReasons.push(detail.reason); }
    });
    host.mount(fixture.assets.a, { history: "replace" });

    const invalidUrl = fixture.baseUrl + "?project_contract_id=fixture-commercial-contract&building_id=building-main&tower_id=tower-a";
    const invalidState = { nlCommercialAsset: { invalid: true } };
    originalReplaceState.call(history, invalidState, "", invalidUrl);
    history.replaceState = function forcedInvalidRouteReplaceFailure() { throw new DOMException("forced invalid replace", "SecurityError"); };
    try { host.handleAssetPopState({ state: invalidState }); } finally { history.replaceState = originalReplaceState; }
    const invalidReplace = {
      mounted: host.mounted,
      destroyed: host.destroyed,
      listenerActive: Boolean(host.routeAbortController && !host.routeAbortController.signal.aborted),
      currentAsset: host.currentAsset,
      picker: document.getElementById("floor-picker").value,
      selectorIdentity: fixture.selector.selectedIdentityKey,
      modelSelected: fixture.model.hasAttribute("data-selected-floor"),
      modelParent: fixture.model.parentElement.id,
      modelCount: document.querySelectorAll("#model").length,
      sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
      invalidReasons: invalidReasons.slice()
    };

    originalReplaceState.call(history, { atomicBase: true }, "", fixture.baseUrl);
    host.mount(fixture.assets.a, { history: "replace" });
    history.pushState = function forcedBuildingPushFailure() { throw new DOMException("forced building push", "SecurityError"); };
    try { host.exit(host.currentAsset, null); } finally { history.pushState = originalPushState; }
    const buildingPush = {
      href: location.href,
      marker: history.state && history.state.nlCommercialAsset,
      mounted: host.mounted,
      destroyed: host.destroyed,
      listenerActive: Boolean(host.routeAbortController && !host.routeAbortController.signal.aborted),
      currentAsset: host.currentAsset,
      picker: document.getElementById("floor-picker").value,
      selectorIdentity: fixture.selector.selectedIdentityKey,
      modelSelected: fixture.model.hasAttribute("data-selected-floor"),
      modelParent: fixture.model.parentElement.id,
      modelCount: document.querySelectorAll("#model").length,
      sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
      invalidReasons: invalidReasons.slice()
    };

    host.mount(fixture.assets.a, { history: "replace" });
    const destroyBefore = { href: location.href, state: JSON.stringify(history.state) };
    history.replaceState = function forcedDestroyReplaceFailure() { throw new DOMException("forced destroy replace", "SecurityError"); };
    try { host.destroy(); } finally { history.replaceState = originalReplaceState; }
    const destroyFailure = {
      before: destroyBefore,
      href: location.href,
      state: JSON.stringify(history.state),
      mounted: host.mounted,
      destroyed: host.destroyed,
      listener: host.routeAbortController,
      currentAsset: host.currentAsset,
      picker: document.getElementById("floor-picker").value,
      selectorIdentity: fixture.selector.selectedIdentityKey,
      modelSelected: fixture.model.hasAttribute("data-selected-floor"),
      modelParent: fixture.model.parentElement.id,
      modelCount: document.querySelectorAll("#model").length,
      sceneCount: document.querySelectorAll(".nl-commercial-scene").length,
      invalidReasons: invalidReasons.slice()
    };
    fixture.selector.destroy();
    originalReplaceState.call(history, {}, "", fixture.baseUrl);
    return { invalidReplace, buildingPush, destroyFailure };
  });
  assert.equal(cleanupFailures.invalidReplace.mounted, false);
  assert.equal(cleanupFailures.invalidReplace.destroyed, false);
  assert.equal(cleanupFailures.invalidReplace.listenerActive, true, "invalid-route replacement failure must retain the reversible host listener");
  assert.equal(cleanupFailures.invalidReplace.currentAsset, null);
  assert.equal(cleanupFailures.invalidReplace.picker, "");
  assert.equal(cleanupFailures.invalidReplace.selectorIdentity, "");
  assert.equal(cleanupFailures.invalidReplace.modelSelected, false);
  assert.equal(cleanupFailures.invalidReplace.modelParent, "model-origin");
  assert.equal(cleanupFailures.invalidReplace.modelCount, 1);
  assert.equal(cleanupFailures.invalidReplace.sceneCount, 0);
  assert(cleanupFailures.invalidReplace.invalidReasons.includes("history_replace_failed"));
  assert.equal(cleanupFailures.buildingPush.href, baseUrl, "Building push failure must fall back to the safe same-origin base");
  assert.equal(cleanupFailures.buildingPush.marker, undefined);
  assert.equal(cleanupFailures.buildingPush.mounted, false);
  assert.equal(cleanupFailures.buildingPush.destroyed, false);
  assert.equal(cleanupFailures.buildingPush.listenerActive, true);
  assert.equal(cleanupFailures.buildingPush.currentAsset, null);
  assert.equal(cleanupFailures.buildingPush.picker, "");
  assert.equal(cleanupFailures.buildingPush.selectorIdentity, "");
  assert.equal(cleanupFailures.buildingPush.modelSelected, false);
  assert.equal(cleanupFailures.buildingPush.modelParent, "model-origin");
  assert.equal(cleanupFailures.buildingPush.modelCount, 1);
  assert.equal(cleanupFailures.buildingPush.sceneCount, 0);
  assert(cleanupFailures.buildingPush.invalidReasons.includes("building_history_unavailable"));
  assert.equal(cleanupFailures.destroyFailure.href, cleanupFailures.destroyFailure.before.href, "destroy history failure must not invent another URL");
  assert.equal(cleanupFailures.destroyFailure.state, cleanupFailures.destroyFailure.before.state, "destroy history failure leaves history untouched but cleans the lifecycle");
  assert.equal(cleanupFailures.destroyFailure.mounted, false);
  assert.equal(cleanupFailures.destroyFailure.destroyed, true);
  assert.equal(cleanupFailures.destroyFailure.listener, null);
  assert.equal(cleanupFailures.destroyFailure.currentAsset, null);
  assert.equal(cleanupFailures.destroyFailure.picker, "");
  assert.equal(cleanupFailures.destroyFailure.selectorIdentity, "");
  assert.equal(cleanupFailures.destroyFailure.modelSelected, false);
  assert.equal(cleanupFailures.destroyFailure.modelParent, "model-origin");
  assert.equal(cleanupFailures.destroyFailure.modelCount, 1);
  assert.equal(cleanupFailures.destroyFailure.sceneCount, 0);
  assert(cleanupFailures.destroyFailure.invalidReasons.includes("destroy_history_unavailable"));

  console.log("PASS commercial asset route browser fixture: current-origin canonical project binding, transactional mount and mounted-render/history rollback with no extra push entry or lost tool state, required project scope, exact nullable-suite identity, picker/model/deep-link equivalence, reversible Building and invalid/destroy history cleanup, exact two-tower Back/Forward composition, no partial surface/listener/selection/lock state and stale/missing tuple fail-closed.");
} finally {
  await context.close();
  await browser.close();
}
