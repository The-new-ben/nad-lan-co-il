/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Portable real-Chromium fixture for commercial fullscreen-tool history.
 * It uses a locally fulfilled example.invalid document and makes no network
 * request to WordPress, NadLan, analytics, mail, or CRM systems.
 *
 * Run:
 *   node commercial-tool-history.browser.fixture.mjs
 */
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const here = path.dirname(fileURLToPath(import.meta.url));
const decisionPath = path.join(here, "commercial-decision-surface.js");
const cssPath = path.join(here, "commercial-decision-surface.css");
const fixtureUrl = "https://example.invalid/commercial-tool-history-fixture/";

const browser = await chromium.launch({ headless: true });
const browserContext = await browser.newContext({ viewport: { width: 375, height: 812 } });
const page = await browserContext.newPage();

try {
  await page.route("https://example.invalid/**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "text/html; charset=utf-8",
      body: `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
        <body><div class="fixture-spacer" aria-hidden="true"></div><main id="decision-root"></main><div class="fixture-tail" aria-hidden="true"></div></body></html>`
    });
  });
  await page.goto(fixtureUrl);
  await page.addStyleTag({ path: cssPath });
  await page.addStyleTag({ content: `
    html { background: #0f1713; }
    body { margin: 0; min-height: 2600px; color: #fffaf0; background: #0f1713; }
    .fixture-spacer { height: 520px; }
    .fixture-tail { height: 1200px; }
    #decision-root { width: 375px; height: 812px; margin: 0 auto; }
    .nl-cds { width: 100%; height: 100%; }
    .fixture-tool-node { display: grid; place-items: center; width: 100%; height: 100%; font-size: 16px; }
  ` });
  await page.addScriptTag({ path: decisionPath });

  await page.evaluate(() => {
    history.scrollRestoration = "manual";
    const verified = (value) => ({
      __nlCommercialEvidence: true,
      state: "verified",
      value,
      sources: [{
        type: "official_record",
        label: "Synthetic fixture source",
        uri: "https://example.invalid/source/fixture",
        documentId: "FIXTURE-HISTORY-1",
        revision: "fixture-r1"
      }],
      effectiveAt: "2026-08-10T08:00:00Z",
      expiresAt: "2099-01-01T00:00:00Z",
      caveat: "Synthetic fixture only"
    });
    const unknown = () => ({
      __nlCommercialEvidence: true,
      state: "unknown",
      value: null,
      sources: [],
      effectiveAt: "",
      expiresAt: "",
      reason: "No synthetic value supplied.",
      caveat: ""
    });
    const asset = (towerId, towerLabel) => ({
      __nlCommercialAsset: true,
      id: `building-main|${towerId}|floor-10|`,
      identityKey: `building-main|${towerId}|floor-10|`,
      kind: "floor",
      wpPostId: 991,
      projectId: "fixture-commercial-contract",
      buildingId: "building-main",
      towerId,
      floorId: "floor-10",
      suiteId: null,
      projectName: "Fixture Commercial Project",
      buildingLabel: "Main Building",
      towerLabel,
      floorLabel: "Floor 10",
      spaceLabel: "",
      availability: verified("verified_available"),
      exposures: unknown(),
      beamScene: { state: "unknown", exposures: [], caveat: "Synthetic fixture only" },
      rentableArea: verified(1250),
      planningCapacity: verified(120),
      monthlyAllIn: verified("ILS 210,000"),
      floorPackAvailable: verified(true),
      fitOutAvailable: verified(true),
      contextAvailable: verified(true),
      costAvailable: verified(true)
    });
    window.__historyFixtureAssets = {
      a: asset("tower-a", "Tower A"),
      b: asset("tower-b", "Tower B")
    };
    const root = document.getElementById("decision-root");
    window.__historyFixtureController = new window.NadlanCommercialDecisionSurface.CommercialDecisionController({
      root,
      labels: { locale: "en", dir: "ltr" },
      renderTool(kind, selectedAsset) {
        const node = document.createElement("section");
        node.className = "fixture-tool-node";
        node.tabIndex = 0;
        node.textContent = `${kind}:${selectedAsset.towerId}:${selectedAsset.floorLabel}`;
        return node;
      }
    });
    window.__historyFixtureController.render(window.__historyFixtureAssets.a);
    window.scrollTo(0, 480);
    window.__historyFixtureInitialScroll = window.scrollY;
  });

  const costSelector = '[data-act="open-tool"][data-tool="cost"]';
  await page.click(costSelector);
  await page.waitForSelector("dialog.nl-commercial-tool[open]");

  const opened = await page.evaluate(() => {
    const marker = history.state && history.state.nlCommercialTool;
    const dialog = document.querySelector("dialog.nl-commercial-tool");
    return {
      marker,
      stateKeys: Object.keys(history.state || {}).sort(),
      markerKeys: Object.keys(marker || {}).sort(),
      rootInert: document.getElementById("decision-root").inert,
      htmlOverflow: document.documentElement.style.overflow,
      bodyPosition: document.body.style.position,
      bodyTop: document.body.style.top,
      focusInside: Boolean(dialog && dialog.contains(document.activeElement)),
      dialogText: dialog ? dialog.textContent : ""
    };
  });
  assert.deepEqual(opened.stateKeys, ["nlCommercialTool"], "tool entry must not retain the legacy asset-only marker");
  assert.deepEqual(opened.markerKeys, [
    "buildingId", "floorId", "projectContractId", "suiteId", "tool", "towerId", "version", "wpPostId"
  ]);
  assert.deepEqual(opened.marker, {
    version: 1,
    tool: "cost",
    wpPostId: 991,
    projectContractId: "fixture-commercial-contract",
    buildingId: "building-main",
    towerId: "tower-a",
    floorId: "floor-10",
    suiteId: null
  });
  assert.equal(opened.rootInert, true);
  assert.equal(opened.htmlOverflow, "hidden");
  assert.equal(opened.bodyPosition, "fixed");
  assert.equal(opened.bodyTop, "-480px");
  assert.equal(opened.focusInside, true);
  assert.match(opened.dialogText, /cost:tower-a:Floor 10/);

  await page.goBack();
  await page.waitForFunction(() => !document.querySelector("dialog.nl-commercial-tool"));
  await page.waitForFunction(() => document.activeElement && document.activeElement.dataset.tool === "cost");
  const afterBack = await page.evaluate(() => ({
    marker: history.state && history.state.nlCommercialTool,
    inert: document.getElementById("decision-root").inert,
    htmlOverflow: document.documentElement.style.overflow,
    bodyPosition: document.body.style.position,
    bodyTop: document.body.style.top,
    scrollY: window.scrollY,
    focusedTool: document.activeElement && document.activeElement.dataset.tool
  }));
  assert.equal(afterBack.marker == null, true);
  assert.equal(afterBack.inert, false);
  assert.equal(afterBack.htmlOverflow, "");
  assert.equal(afterBack.bodyPosition, "");
  assert.equal(afterBack.bodyTop, "");
  assert.equal(afterBack.scrollY, 480);
  assert.equal(afterBack.focusedTool, "cost");

  await page.goForward();
  await page.waitForSelector("dialog.nl-commercial-tool[open]");
  const coherentForward = await page.evaluate(() => ({
    towerId: history.state.nlCommercialTool.towerId,
    dialogText: document.querySelector("dialog.nl-commercial-tool").textContent,
    rootInert: document.getElementById("decision-root").inert,
    focusInside: document.querySelector("dialog.nl-commercial-tool").contains(document.activeElement)
  }));
  assert.equal(coherentForward.towerId, "tower-a");
  assert.match(coherentForward.dialogText, /cost:tower-a:Floor 10/);
  assert.equal(coherentForward.rootInert, true);
  assert.equal(coherentForward.focusInside, true);

  await page.goBack();
  await page.waitForFunction(() => !document.querySelector("dialog.nl-commercial-tool"));
  await page.evaluate(() => {
    window.__historyFixtureController.render(window.__historyFixtureAssets.b);
    const trigger = document.querySelector('[data-act="open-tool"][data-tool="cost"]');
    trigger.focus({ preventScroll: true });
  });
  await page.goForward();
  await page.waitForFunction(() => !history.state || !history.state.nlCommercialTool);
  const staleForward = await page.evaluate(() => ({
    hasDialog: Boolean(document.querySelector("dialog.nl-commercial-tool")),
    marker: history.state && history.state.nlCommercialTool,
    selectedTower: window.__historyFixtureController.asset.towerId,
    heading: document.querySelector("#nl-cds-title").textContent,
    inert: document.getElementById("decision-root").inert,
    bodyPosition: document.body.style.position,
    htmlOverflow: document.documentElement.style.overflow,
    scrollY: window.scrollY,
    focusedTool: document.activeElement && document.activeElement.dataset.tool
  }));
  assert.equal(staleForward.hasDialog, false, "stale Forward must never reopen another tower's tool");
  assert.equal(staleForward.marker, undefined, "stale marker must be replaced on its own history entry");
  assert.equal(staleForward.selectedTower, "tower-b");
  assert.match(staleForward.heading, /Tower B.*Floor 10/);
  assert.equal(staleForward.inert, false);
  assert.equal(staleForward.bodyPosition, "");
  assert.equal(staleForward.htmlOverflow, "");
  assert.equal(staleForward.scrollY, 480);
  assert.equal(staleForward.focusedTool, "cost");

  await page.goBack();
  await page.goForward();
  await page.waitForTimeout(50);
  assert.equal(await page.locator("dialog.nl-commercial-tool").count(), 0, "a stripped stale entry must stay inert on later traversal");

  await page.click(costSelector);
  await page.waitForSelector("dialog.nl-commercial-tool[open]");
  await page.evaluate(() => window.__historyFixtureController.destroy());
  const destroyed = await page.evaluate(() => {
    const oldMarker = {
      version: 1,
      tool: "cost",
      wpPostId: 991,
      projectContractId: "fixture-commercial-contract",
      buildingId: "building-main",
      towerId: "tower-b",
      floorId: "floor-10",
      suiteId: null
    };
    window.dispatchEvent(new PopStateEvent("popstate", { state: { nlCommercialTool: oldMarker } }));
    return {
      hasDialog: Boolean(document.querySelector("dialog.nl-commercial-tool")),
      marker: history.state && history.state.nlCommercialTool,
      rootInert: document.getElementById("decision-root").inert,
      bodyPosition: document.body.style.position,
      bodyTop: document.body.style.top,
      htmlOverflow: document.documentElement.style.overflow,
      scrollY: window.scrollY,
      focusInRemovedDialog: Boolean(document.activeElement && document.activeElement.closest("dialog.nl-commercial-tool"))
    };
  });
  assert.equal(destroyed.hasDialog, false);
  assert.equal(destroyed.marker, undefined);
  assert.equal(destroyed.rootInert, false);
  assert.equal(destroyed.bodyPosition, "");
  assert.equal(destroyed.bodyTop, "");
  assert.equal(destroyed.htmlOverflow, "");
  assert.equal(destroyed.scrollY, 480);
  assert.equal(destroyed.focusInRemovedDialog, false);

  const atomicFailures = await page.evaluate(async () => {
    const root = document.getElementById("decision-root");
    const asset = window.__historyFixtureAssets.b;
    const originalPushState = history.pushState;
    const originalReplaceState = history.replaceState;
    const originalShowModal = HTMLDialogElement.prototype.showModal;
    const nextFrame = () => new Promise((resolve) => requestAnimationFrame(resolve));
    history.replaceState({}, "", location.href);
    window.__atomicCleanupCalls = 0;
    window.__atomicThrowCleanup = false;
    const controller = new window.NadlanCommercialDecisionSurface.CommercialDecisionController({
      root,
      labels: { locale: "en", dir: "ltr" },
      renderTool(kind, selectedAsset) {
        const node = document.createElement("section");
        node.className = "fixture-tool-node";
        node.tabIndex = 0;
        node.textContent = `${kind}:${selectedAsset.towerId}:atomic`;
        node.__nlToolDestroy = function atomicToolCleanup() {
          window.__atomicCleanupCalls += 1;
          if (window.__atomicThrowCleanup) throw new Error("forced tool cleanup failure");
        };
        return node;
      }
    });
    controller.render(asset);
    const trigger = root.querySelector('[data-act="open-tool"][data-tool="cost"]');
    trigger.focus({ preventScroll: true });
    window.scrollTo(0, 480);
    const snapshot = () => ({
      hasDialog: Boolean(document.querySelector("dialog.nl-commercial-tool")),
      controllerDialog: Boolean(controller.toolDialog.dialog),
      rootInert: root.inert,
      htmlOverflow: document.documentElement.style.overflow,
      bodyPosition: document.body.style.position,
      bodyTop: document.body.style.top,
      scrollY: window.scrollY,
      focusedTool: document.activeElement && document.activeElement.dataset.tool,
      cleanupCalls: window.__atomicCleanupCalls,
      marker: history.state && history.state.nlCommercialTool,
      historyListener: controller.toolDialog.historyAbortController
    });
    const failures = {};

    let pushError = "";
    history.pushState = function forcedToolPushFailure() { throw new DOMException("forced tool push", "SecurityError"); };
    try { controller.toolDialog.open("cost", asset, trigger); } catch (error) { pushError = error.message; }
    history.pushState = originalPushState;
    await nextFrame();
    failures.push = Object.assign({ error: pushError }, snapshot());

    controller.toolDialog.open("cost", asset, trigger);
    failures.afterPushSubsequentOpen = Boolean(controller.toolDialog.dialog && controller.toolDialog.dialog.open);
    controller.toolDialog.close({ history: false, focus: true });
    originalReplaceState.call(history, {}, "", location.href);

    let modalError = "";
    HTMLDialogElement.prototype.showModal = function forcedShowModalFailure() { throw new DOMException("forced showModal", "InvalidStateError"); };
    try { controller.toolDialog.open("cost", asset, trigger); } catch (error) { modalError = error.message; }
    HTMLDialogElement.prototype.showModal = originalShowModal;
    await nextFrame();
    failures.showModal = Object.assign({ error: modalError }, snapshot());

    controller.toolDialog.open("cost", asset, trigger);
    window.__atomicThrowCleanup = true;
    let cleanupEscaped = false;
    try { controller.toolDialog.close({ history: false, focus: true }); } catch (error) { cleanupEscaped = true; }
    await nextFrame();
    window.__atomicThrowCleanup = false;
    originalReplaceState.call(history, {}, "", location.href);
    failures.cleanup = Object.assign({ escaped: cleanupEscaped }, snapshot());
    controller.toolDialog.open("cost", asset, trigger);
    failures.afterCleanupSubsequentOpen = Boolean(controller.toolDialog.dialog && controller.toolDialog.dialog.open);
    controller.toolDialog.close({ history: false, focus: true });
    originalReplaceState.call(history, {}, "", location.href);

    controller.toolDialog.open("cost", asset, trigger);
    originalReplaceState.call(history, { nlCommercialTool: { invalid: true } }, "", location.href);
    history.replaceState = function forcedCloseReplaceFailure() { throw new DOMException("forced close replace", "SecurityError"); };
    controller.toolDialog.close({ history: true, focus: true });
    history.replaceState = originalReplaceState;
    await nextFrame();
    failures.closeReplace = snapshot();
    originalReplaceState.call(history, {}, "", location.href);

    controller.toolDialog.open("cost", asset, trigger);
    history.replaceState = function forcedPopReplaceFailure() { throw new DOMException("forced pop replace", "SecurityError"); };
    window.dispatchEvent(new PopStateEvent("popstate", { state: { nlCommercialTool: { invalid: true } } }));
    history.replaceState = originalReplaceState;
    await nextFrame();
    failures.popReplace = snapshot();
    originalReplaceState.call(history, {}, "", location.href);

    controller.toolDialog.open("cost", asset, trigger);
    history.replaceState = function forcedDestroyReplaceFailure() { throw new DOMException("forced destroy replace", "SecurityError"); };
    controller.destroy();
    history.replaceState = originalReplaceState;
    failures.destroyReplace = snapshot();
    originalReplaceState.call(history, {}, "", location.href);
    return failures;
  });
  assert(atomicFailures.push.error, "pushState failure must surface to the caller");
  assert.equal(atomicFailures.push.hasDialog, false);
  assert.equal(atomicFailures.push.controllerDialog, false);
  assert.equal(atomicFailures.push.rootInert, false);
  assert.equal(atomicFailures.push.htmlOverflow, "");
  assert.equal(atomicFailures.push.bodyPosition, "");
  assert.equal(atomicFailures.push.bodyTop, "");
  assert.equal(atomicFailures.push.scrollY, 480);
  assert.equal(atomicFailures.push.focusedTool, "cost");
  assert.equal(atomicFailures.push.marker, undefined);
  assert.equal(atomicFailures.afterPushSubsequentOpen, true);
  assert(atomicFailures.showModal.error, "showModal failure must surface to the caller");
  assert.equal(atomicFailures.showModal.hasDialog, false);
  assert.equal(atomicFailures.showModal.controllerDialog, false);
  assert.equal(atomicFailures.showModal.rootInert, false);
  assert.equal(atomicFailures.showModal.htmlOverflow, "");
  assert.equal(atomicFailures.showModal.bodyPosition, "");
  assert.equal(atomicFailures.showModal.bodyTop, "");
  assert.equal(atomicFailures.showModal.focusedTool, "cost");
  assert.equal(atomicFailures.cleanup.escaped, false, "throwing __nlToolDestroy must be isolated");
  assert.equal(atomicFailures.cleanup.hasDialog, false);
  assert.equal(atomicFailures.cleanup.rootInert, false);
  assert.equal(atomicFailures.cleanup.htmlOverflow, "");
  assert.equal(atomicFailures.cleanup.bodyPosition, "");
  assert.equal(atomicFailures.afterCleanupSubsequentOpen, true);
  [atomicFailures.closeReplace, atomicFailures.popReplace, atomicFailures.destroyReplace].forEach((failure) => {
    assert.equal(failure.hasDialog, false);
    assert.equal(failure.controllerDialog, false);
    assert.equal(failure.rootInert, false);
    assert.equal(failure.htmlOverflow, "");
    assert.equal(failure.bodyPosition, "");
    assert.equal(failure.bodyTop, "");
  });
  assert.equal(atomicFailures.destroyReplace.historyListener, null, "destroy must abort the tool popstate listener despite replace failure");

  console.log(JSON.stringify({
    pass: true,
    cases: [
      "strict full-identity marker",
      "Back closes and restores focus/scroll/locks",
      "coherent Forward reopens exact tool",
      "same-label different-tower Forward strips stale marker",
      "destroy removes marker/listener/dialog/focus trap/locks",
      "pushState/showModal rollback restores focus/scroll/locks and permits a later open",
      "replaceState and throwing cleanup cannot block close/popstate/destroy cleanup"
    ]
  }, null, 2));
} finally {
  await browserContext.close();
  await browser.close();
}
