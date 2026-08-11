/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Portable real-Chromium geometry fixture for the commercial decision scene,
 * its complete orientation-source pager, and the five-step RFP composer.
 * It loads only sibling proposal assets, makes no network requests and never
 * touches WordPress or the live site.
 *
 * Run:
 *   node commercial-rfp-beam.browser.fixture.mjs
 *
 * Optional screenshots:
 *   NADLAN_BROWSER_ARTIFACT_DIR=./browser-artifacts node commercial-rfp-beam.browser.fixture.mjs
 */
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const here = path.dirname(fileURLToPath(import.meta.url));
const cssPath = path.join(here, "commercial-decision-surface.css");
const i18nPath = path.join(here, "commercial-i18n-additions.js");
const decisionPath = path.join(here, "commercial-decision-surface.js");
const rfpPath = path.join(here, "commercial-rfp-composer.js");
const artifactDir = process.env.NADLAN_BROWSER_ARTIFACT_DIR
  ? path.resolve(process.env.NADLAN_BROWSER_ARTIFACT_DIR)
  : "";

const viewportMatrix = [
  { name: "small-phone", width: 320, height: 568, dpr: 1 },
  { name: "phone", width: 375, height: 812, dpr: 1 },
  { name: "short-landscape", width: 568, height: 320, dpr: 1 },
  { name: "desktop", width: 1280, height: 800, dpr: 1 }
];
const localeMatrix = ["he", "en", "fr", "ru", "ar"];
const sourceCountMatrix = [1, 2, 4, 6, 37];
const viewports = process.env.NADLAN_BROWSER_VIEWPORT
  ? viewportMatrix.filter((item) => `${item.width}x${item.height}` === process.env.NADLAN_BROWSER_VIEWPORT)
  : viewportMatrix;
const locales = process.env.NADLAN_BROWSER_LOCALE
  ? localeMatrix.filter((locale) => locale === process.env.NADLAN_BROWSER_LOCALE)
  : localeMatrix;
const sourceCounts = process.env.NADLAN_BROWSER_SOURCE_COUNT
  ? sourceCountMatrix.filter((count) => String(count) === process.env.NADLAN_BROWSER_SOURCE_COUNT)
  : sourceCountMatrix;
const tolerance = 1.25;

if (artifactDir) fs.mkdirSync(artifactDir, { recursive: true });

function caseName(viewport, locale, suffix) {
  return `${viewport.width}x${viewport.height}-${locale}-${suffix}`;
}

function assertCleanGeometry(name, geometry) {
  assert.deepEqual(geometry.clipped, [], `${name}: visible element clipped ${JSON.stringify(geometry.debug || {})}`);
  assert.deepEqual(geometry.overflowed, [], `${name}: content box overflowed ${JSON.stringify(geometry.debug || geometry.questionText || {})}`);
  assert.deepEqual(geometry.internalScrollers, [], `${name}: inner scroller introduced`);
  assert.deepEqual(geometry.undersizedTargets, [], `${name}: target below 44px`);
  assert.deepEqual(geometry.undersizedText, [], `${name}: visible buyer text below 12px`);
  assert(
    geometry.documentOverflow.width <= tolerance && geometry.documentOverflow.height <= tolerance,
    `${name}: document overflowed`
  );
}

async function createPage(browser, viewport) {
  const browserContext = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: viewport.dpr
  });
  const page = await browserContext.newPage();
  await page.setContent(`<!doctype html>
    <html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
    <body><div id="fixture-root"></div></body></html>`);
  await page.addStyleTag({ path: cssPath });
  await page.addStyleTag({ content: `
    html, body, #fixture-root { width: 100%; height: 100%; margin: 0; overflow: hidden; }
    body { font-family: Inter, Arial, sans-serif; }
    .fixture-model { display: grid !important; place-items: center; color: #fffaf0; background: #26322b; font-size: 12px; }
    .fixture-tool { display: grid; grid-template-rows: 54px minmax(0, 1fr); width: 100%; height: 100%; color: var(--nl-cds-text); background: var(--nl-cds-bg); }
    .fixture-tool__head { display: grid; align-items: center; min-height: 54px; padding-inline: 12px; border-bottom: 1px solid var(--nl-cds-border); }
    .fixture-tool__body { width: 100%; height: 100%; min-width: 0; min-height: 0; overflow: hidden; }
  ` });
  await page.addScriptTag({ path: i18nPath });
  await page.addScriptTag({ path: decisionPath });
  await page.addScriptTag({ path: rfpPath });
  await page.evaluate(() => {
    const expiresAt = "2099-01-01T00:00:00Z";
    const effectiveAt = "2026-08-10T08:00:00Z";

    window.__nadlanFixtureAsset = function buildAsset(sourceCount, locale) {
      const count = Math.max(1, Number(sourceCount) || 1);
      const compactLandmarkNames = {
        en: ["Hashalom", "Ayalon", "Sarona", "Red Line"],
        he: ["השלום", "איילון", "שרונה", "הקו האדום"],
        fr: ["Hashalom", "Ayalon", "Sarona", "Ligne rouge"],
        ru: ["Хашалом", "Аялон", "Сарона", "Красная"],
        ar: ["هشالوم", "أيالون", "سارونا", "الخط الأحمر"]
      };
      const compactNames = compactLandmarkNames[locale] || compactLandmarkNames.en;
      const fullNames = compactNames.map((name, index) => `${name} — complete evidenced landmark name ${index + 1}`);
      const sources = Array.from({ length: count }, (_, index) => ({
        type: "official_record",
        label: `Fixture evidence authority ${index + 1}`,
        uri: index === count - 1 && count > 4 ? "" : `https://example.invalid/orientation/${index + 1}`,
        documentId: `FIXTURE-ORIENTATION-${index + 1}`,
        revision: "fixture-r1"
      }));
      let cursor = 0;
      const sourced = (value) => ({
        __nlCommercialEvidence: true,
        state: "verified",
        value,
        sources: [sources[cursor++ % sources.length]],
        effectiveAt,
        expiresAt,
        caveat: "Illustrative decision aid"
      });
      const contextual = (value) => ({
        __nlCommercialEvidence: true,
        state: "verified",
        value,
        sources: [sources[0]],
        effectiveAt,
        expiresAt,
        caveat: "Illustrative decision aid"
      });
      const stableFact = (value) => ({
        __nlCommercialEvidence: true,
        state: "verified",
        value,
        sources: [sources[0]],
        effectiveAt,
        expiresAt,
        caveat: ""
      });
      const specs = [
        { id: "north", direction: "N", start: 315, end: 45, coordinate: { lat: 32.084, lng: 34.78 }, distance: 445, bearing: 0 },
        { id: "east", direction: "E", start: 45, end: 135, coordinate: { lat: 32.08, lng: 34.785 }, distance: 471, bearing: 90 },
        { id: "south", direction: "S", start: 135, end: 225, coordinate: { lat: 32.0762, lng: 34.78 }, distance: 423, bearing: 180 },
        { id: "west", direction: "W", start: 225, end: 315, coordinate: { lat: 32.08, lng: 34.7752 }, distance: 452, bearing: 270 }
      ];
      const exposures = specs.map((spec) => ({
        id: spec.id,
        direction: sourced(spec.direction),
        azimuthStartDeg: sourced(spec.start),
        azimuthEndDeg: sourced(spec.end),
        facadeSharePct: sourced(25),
        viewContext: contextual(["city", "transit"])
      }));
      const associations = specs.map((spec, index) => ({
        exposure: exposures[index],
        landmarks: [{
          id: `${spec.id}-landmark`,
          label: sourced(fullNames[index]),
          compactLabel: sourced(compactNames[index]),
          coordinates: sourced(spec.coordinate),
          distanceM: sourced(spec.distance),
          distanceMethod: sourced(index % 2 ? "routed_walking" : "straight_line_geodesic"),
          bearingDeg: sourced(spec.bearing),
          caveat: "Illustrative distance"
        }]
      }));
      const beamScene = {
        state: "ready",
        projectAnchor: sourced({ lat: 32.08, lng: 34.78 }),
        exposures: associations,
        caveat: "Illustrative orientation aid"
      };
      return {
        __nlCommercialAsset: true,
        id: "fixture-suite-a",
        kind: "suite",
        wpPostId: 991,
        projectId: "fixture-project-991",
        buildingId: "building-main",
        towerId: "tower-main",
        floorId: "floor-18",
        suiteId: "suite-a",
        projectName: "Fixture Commercial Project",
        buildingLabel: "Main Building",
        towerLabel: "Main Tower",
        floorLabel: "Floor 18",
        spaceLabel: "Suite A",
        availability: stableFact("verified_available"),
        exposures: stableFact(exposures),
        beamScene,
        rentableArea: stableFact(1250),
        planningCapacity: stableFact(120),
        monthlyAllIn: stableFact("ILS 210,000"),
        floorPackAvailable: stableFact(true),
        fitOutAvailable: stableFact(true),
        contextAvailable: stableFact(true),
        costAvailable: stableFact(true)
      };
    };
  });
  return { browserContext, page };
}

async function renderScene(page, locale, sourceCount) {
  await page.evaluate(({ locale, sourceCount }) => {
    const labels = window.NadlanCommercialI18n.get(locale);
    const asset = window.__nadlanFixtureAsset(sourceCount, locale);
    document.documentElement.lang = locale;
    document.documentElement.dir = labels.dir;
    const root = document.getElementById("fixture-root");
    root.innerHTML = '<main class="nl-commercial-scene"><div class="nl-commercial-scene__model"><div class="fixture-model">3D model remains visible</div></div><div class="nl-commercial-scene__decision"></div></main>';
    root.querySelector(".nl-commercial-scene__decision").innerHTML =
      window.NadlanCommercialDecisionSurface.renderDecisionSurface(asset, labels, { locale });
    window.__sceneFixtureAsset = asset;
  }, { locale, sourceCount });
}

async function renderOverlongCompactLabelScene(page) {
  return page.evaluate(() => {
    const locale = "en";
    const labels = window.NadlanCommercialI18n.get(locale);
    const asset = window.__nadlanFixtureAsset(6, locale);
    const rawBeam = {
      scene_state: "ready",
      projection: "north_up_local_equirectangular_v1",
      project_anchor: asset.beamScene.projectAnchor,
      illustrative_caveat: asset.beamScene.caveat,
      issues: [],
      exposures: asset.beamScene.exposures.map((association) => ({
        exposure_id: association.exposure.id,
        landmarks: association.landmarks.map((landmark) => ({
          landmark_id: landmark.id,
          exposure_id: landmark.exposureId,
          label: landmark.label,
          compact_label: landmark.compactLabel,
          coordinates: landmark.coordinates,
          distance_m: landmark.distanceM,
          distance_method: landmark.distanceMethod,
          bearing_deg: landmark.bearingDeg,
          caveat: landmark.caveat
        }))
      }))
    };
    rawBeam.exposures[0].landmarks[0].label = Object.assign({}, rawBeam.exposures[0].landmarks[0].label, {
      value: "L".repeat(1000)
    });
    rawBeam.exposures[0].landmarks[0].compact_label = Object.assign({}, rawBeam.exposures[0].landmarks[0].compact_label, {
      value: "C".repeat(13)
    });
    const neutralScene = window.NadlanCommercialContractAdapter.adaptBeamScene(
      rawBeam,
      asset.exposures,
      { now: Date.parse("2026-08-11T08:00:00Z") }
    );
    const neutralAsset = Object.assign({}, asset, { beamScene: neutralScene });
    document.documentElement.lang = locale;
    document.documentElement.dir = labels.dir;
    const root = document.getElementById("fixture-root");
    root.innerHTML = '<main class="nl-commercial-scene"><div class="nl-commercial-scene__model"><div class="fixture-model">3D model remains visible</div></div><div class="nl-commercial-scene__decision"></div></main>';
    root.querySelector(".nl-commercial-scene__decision").innerHTML =
      window.NadlanCommercialDecisionSurface.renderDecisionSurface(neutralAsset, labels, { locale });
    return {
      sceneState: neutralScene.state,
      exposureCount: neutralScene.exposures.length,
      compactIssue: neutralScene.issues.some((issue) => String(issue).indexOf("invalid_landmark_compact_label:") === 0),
      renderedState: root.querySelector(".nl-beam-scene")?.dataset.beamState || "",
      coneCount: root.querySelectorAll(".nl-beam-scene__cone").length,
      landmarkCount: root.querySelectorAll(".nl-beam-scene__landmark").length,
      requestCount: root.querySelectorAll('[data-act="request-field"]').length
    };
  });
}

async function sceneGeometry(page) {
  return page.evaluate((tolerance) => {
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return !element.hidden && style.display !== "none" && style.visibility !== "hidden" &&
        element.getClientRects().length > 0 && rect.width > 1 && rect.height > 1;
    };
    const within = (element, boundary) => {
      const rect = element.getBoundingClientRect();
      const limit = boundary.getBoundingClientRect();
      return rect.left >= limit.left - tolerance && rect.top >= limit.top - tolerance &&
        rect.right <= limit.right + tolerance && rect.bottom <= limit.bottom + tolerance;
    };
    const scene = document.querySelector(".nl-commercial-scene");
    const decision = document.querySelector(".nl-commercial-scene__decision");
    const cds = document.querySelector(".nl-cds");
    const exposure = document.querySelector(".nl-cds-exposure");
    const beam = document.querySelector('.nl-beam-scene[data-beam-state="ready"]');
    const visual = beam.querySelector(".nl-beam-scene__visual");
    const plot = beam.querySelector(".nl-beam-scene__plot");
    const legendPanel = beam.querySelector(".nl-beam-scene__legend-panel");
    const legend = beam.querySelector(".nl-beam-scene__legend");
    const legendDistancesPanel = beam.querySelector(".nl-beam-scene__legend-distances");
    const method = beam.querySelector(".nl-beam-scene__method");
    const sources = beam.querySelector(".nl-beam-scene__sources");
    const svg = beam.querySelector("svg");
    const bounded = [
      [document.querySelector(".nl-commercial-scene__model"), scene],
      [decision, scene],
      [cds, decision],
      [exposure, cds],
      [beam, exposure],
      [visual, beam],
      [plot, visual],
      [svg, plot],
      [legendPanel, visual],
      [legend, legendPanel],
      [legendDistancesPanel, legendPanel],
      [method, beam],
      [sources, beam],
      [document.querySelector(".nl-cds-facts"), cds],
      [document.querySelector(".nl-cds-doors"), cds],
      [document.querySelector(".nl-cds-actions"), cds],
      [document.querySelector(".nl-cds-cta"), cds]
    ];
    Array.from(legend.querySelectorAll(".nl-beam-scene__legend-item")).forEach((item) => bounded.push([item, legend]));
    const clipped = bounded.filter(([element]) => visible(element)).filter(([element, boundary]) => !within(element, boundary))
      .map(([element]) => ({ selector: element.className || element.tagName, rect: element.getBoundingClientRect().toJSON() }));
    const tracked = Array.from(document.querySelectorAll(
      ".nl-commercial-scene, .nl-commercial-scene__model, .nl-commercial-scene__decision, .nl-cds, .nl-cds-head, .nl-cds-exposure, .nl-beam-scene, .nl-beam-scene__visual, .nl-beam-scene__plot, .nl-beam-scene svg, .nl-beam-scene__legend-panel, .nl-beam-scene__legend, .nl-beam-scene__legend-item, .nl-beam-scene__legend-distances, .nl-beam-scene__legend-distance, .nl-beam-scene__method, .nl-beam-scene__sources, .nl-cds-facts, .nl-cds-fact, .nl-cds-doors, .nl-cds-door, .nl-cds-actions, .nl-cds-cta"
    )).filter(visible);
    const overflowed = tracked.filter((element) =>
      element.scrollHeight > element.clientHeight + tolerance ||
      element.scrollWidth > element.clientWidth + tolerance
    ).map((element) => ({
      selector: element.className || element.tagName,
      text: element.textContent.trim().replace(/\s+/g, " "),
      client: [element.clientWidth, element.clientHeight],
      scroll: [element.scrollWidth, element.scrollHeight]
    }));
    const internalScrollers = Array.from(document.querySelectorAll(".nl-cds, .nl-cds *"))
      .filter(visible)
      .filter((element) => [getComputedStyle(element).overflow, getComputedStyle(element).overflowX, getComputedStyle(element).overflowY]
        .some((value) => value === "auto" || value === "scroll"))
      .map((element) => element.className || element.tagName);
    const targets = Array.from(document.querySelectorAll(".nl-cds button, .nl-cds a[href]")).filter(visible);
    const undersizedTargets = targets.filter((element) => {
      const rect = element.getBoundingClientRect();
      return rect.width + tolerance < 44 || rect.height + tolerance < 44;
    }).map((element) => ({ selector: element.className || element.tagName, rect: element.getBoundingClientRect().toJSON() }));
    const textNodes = Array.from(document.querySelectorAll(
      ".nl-cds h2, .nl-cds h3, .nl-cds p, .nl-cds small, .nl-cds strong, .nl-cds span, .nl-cds button, .nl-cds a"
    )).filter(visible).filter((element) => element.textContent.trim());
    const undersizedText = textNodes.filter((element) => Number.parseFloat(getComputedStyle(element).fontSize) + 0.05 < 12)
      .map((element) => ({ selector: element.className || element.tagName, fontSize: getComputedStyle(element).fontSize }));
    const methodRect = method.getBoundingClientRect();
    const intersects = (a, b) => !(a.right <= b.left + tolerance || a.left >= b.right - tolerance || a.bottom <= b.top + tolerance || a.top >= b.bottom - tolerance);
    const svgText = Array.from(svg.querySelectorAll("text")).filter(visible);
    const methodOverlaps = svgText.filter((element) => intersects(element.getBoundingClientRect(), methodRect))
      .map((element) => element.textContent.trim());
    const sourceControls = Array.from(sources.querySelectorAll(".nl-beam-scene__source")).filter(visible);
    const sourceOverlaps = sourceControls.filter((element) => intersects(element.getBoundingClientRect(), methodRect))
      .map((element) => element.textContent.trim());
    const tinySvgText = svgText.filter((element) => element.getBoundingClientRect().height + tolerance < 12)
      .map((element) => ({ text: element.textContent.trim(), height: element.getBoundingClientRect().height }));
    const textLeaves = [
      ...svg.querySelectorAll(".nl-beam-scene__north, .nl-beam-scene__project-label, .nl-beam-scene__callout-number"),
      ...plot.querySelectorAll(".nl-beam-scene__plot-caption"),
      ...legend.querySelectorAll(".nl-beam-scene__legend-index, .nl-beam-scene__legend-name, .nl-beam-scene__legend-direction"),
      ...legendDistancesPanel.querySelectorAll(".nl-beam-scene__legend-distance, .nl-beam-scene__legend-unit")
    ].filter(visible);
    const textCollisions = [];
    for (let left = 0; left < textLeaves.length; left += 1) {
      for (let right = left + 1; right < textLeaves.length; right += 1) {
        const a = textLeaves[left];
        const b = textLeaves[right];
        if (intersects(a.getBoundingClientRect(), b.getBoundingClientRect())) {
          textCollisions.push([a.textContent.trim(), b.textContent.trim()]);
        }
      }
    }
    const cones = Array.from(svg.querySelectorAll(".nl-beam-scene__cone")).filter(visible);
    const coneSignatures = cones.map((cone) => {
      const style = getComputedStyle(cone);
      return [style.fill, style.stroke, style.strokeDasharray].join("|");
    });
    const coneHitSamples = cones.map((cone) => {
      const bearing = Number(cone.dataset.coneCenterBearing);
      const angle = (bearing - 90) * Math.PI / 180;
      const point = svg.createSVGPoint();
      point.x = 160 + Math.cos(angle) * 50;
      point.y = 78 + Math.sin(angle) * 50;
      const screen = point.matrixTransform(svg.getScreenCTM());
      return document.elementsFromPoint(screen.x, screen.y).includes(cone);
    });
    const coneIds = cones.map((cone) => cone.dataset.exposureId);
    const markerIds = Array.from(svg.querySelectorAll(".nl-beam-scene__landmark"), (item) => item.dataset.landmarkId);
    const legendIds = Array.from(legend.querySelectorAll(".nl-beam-scene__legend-item"), (item) => item.dataset.landmarkId);
    const leaderLengths = Array.from(svg.querySelectorAll(".nl-beam-scene__leader"), (leader) =>
      Math.hypot(
        Number(leader.getAttribute("x2")) - Number(leader.getAttribute("x1")),
        Number(leader.getAttribute("y2")) - Number(leader.getAttribute("y1"))
      )
    );
    const legendNames = Array.from(legend.querySelectorAll(".nl-beam-scene__legend-name"), (item) => item.textContent.trim());
    const legendArias = Array.from(legend.querySelectorAll(".nl-beam-scene__legend-item"), (item) => item.getAttribute("aria-label") || "");
    const legendDistances = Array.from(legendDistancesPanel.querySelectorAll(".nl-beam-scene__legend-distance"), (item) => item.textContent.trim());
    const legendDistanceArias = Array.from(legendDistancesPanel.querySelectorAll(".nl-beam-scene__legend-distance"), (item) => item.getAttribute("aria-label") || "");
    const expectedLandmarks = window.__sceneFixtureAsset.beamScene.exposures
      .flatMap((association) => association.landmarks)
      .slice()
      .sort((left, right) => Number(left.bearingDeg.value) - Number(right.bearingDeg.value));
    const fixtureFormatter = new Intl.NumberFormat(document.documentElement.lang || "en");
    const expectedLegendNames = expectedLandmarks.map((item) => String(item.compactLabel.value));
    const expectedFullLabels = expectedLandmarks.map((item) => String(item.label.value));
    const expectedLegendDistances = expectedLandmarks.map((item) => fixtureFormatter.format(item.distanceM.value));
    const expectedDistanceArias = expectedLandmarks.map((item) => `${fixtureFormatter.format(item.distanceM.value)} m`);
    const modelRect = document.querySelector(".nl-commercial-scene__model").getBoundingClientRect();
    return {
      clipped,
      overflowed,
      internalScrollers,
      undersizedTargets,
      undersizedText,
      methodOverlaps,
      sourceOverlaps,
      tinySvgText,
      textCollisions,
      coneCount: cones.length,
      coneIds,
      coneSignatureCount: new Set(coneSignatures).size,
      coneHitSamples,
      markerIds,
      legendIds,
      leaderLengths,
      legendNames,
      legendArias,
      legendDistances,
      legendDistanceArias,
      expectedLegendNames,
      expectedFullLabels,
      expectedLegendDistances,
      expectedDistanceArias,
      legendUnit: legendDistancesPanel.querySelector(".nl-beam-scene__legend-unit")?.textContent.trim() || "",
      projectAnchorAccessible: Boolean(svg.querySelector('.nl-beam-scene__anchor[role="img"][aria-label] title')),
      sourceCount: Number(beam.dataset.sourceCount),
      directLinks: sources.querySelectorAll("a.nl-beam-scene__source").length,
      allSourcesActions: sources.querySelectorAll("button.nl-beam-scene__source--all").length,
      sourceControlCount: sourceControls.length,
      methodText: method.textContent.trim(),
      methodAria: method.getAttribute("aria-label") || "",
      actionRowVisible: visible(document.querySelector(".nl-cds-actions")),
      factLabelCount: Array.from(document.querySelectorAll(".nl-cds-fact__head > span:first-child")).filter(visible).length,
      doorLongVisibleCount: Array.from(document.querySelectorAll(".nl-cds-door__title--long")).filter(visible).length,
      doorShortVisibleCount: Array.from(document.querySelectorAll(".nl-cds-door__title--short")).filter(visible).length,
      backIconVisible: visible(document.querySelector(".nl-cds-back__icon")),
      model: { width: modelRect.width, height: modelRect.height },
      debug: {
        cds: cds.getBoundingClientRect().toJSON(),
        exposure: exposure.getBoundingClientRect().toJSON(),
        beam: beam.getBoundingClientRect().toJSON(),
        visual: visual.getBoundingClientRect().toJSON(),
        plot: plot.getBoundingClientRect().toJSON(),
        legend: legend.getBoundingClientRect().toJSON(),
        legendPanel: legendPanel.getBoundingClientRect().toJSON(),
        sources: sources.getBoundingClientRect().toJSON()
      },
      documentOverflow: {
        width: document.documentElement.scrollWidth - innerWidth,
        height: document.documentElement.scrollHeight - innerHeight
      }
    };
  }, tolerance);
}

async function renderEvidenceTool(page, locale, sourceCount) {
  await page.evaluate(({ locale, sourceCount }) => {
    const labels = window.NadlanCommercialI18n.get(locale);
    const asset = window.__nadlanFixtureAsset(sourceCount, locale);
    document.documentElement.lang = locale;
    document.documentElement.dir = labels.dir;
    const root = document.getElementById("fixture-root");
    root.innerHTML = '<main class="nl-commercial-tool fixture-tool"><header class="fixture-tool__head">Orientation evidence fixture</header><div class="fixture-tool__body"></div></main>';
    root.querySelector(".fixture-tool__body").appendChild(
      window.NadlanCommercialDecisionSurface.createBeamEvidenceNode(asset, labels)
    );
  }, { locale, sourceCount });
}

async function evidenceGeometryAndReach(page, expectedCount) {
  return page.evaluate(({ expectedCount, tolerance }) => {
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return !element.hidden && style.display !== "none" && style.visibility !== "hidden" &&
        element.getClientRects().length > 0 && rect.width > 1 && rect.height > 1;
    };
    const body = document.querySelector(".fixture-tool__body");
    const boundary = body.getBoundingClientRect();
    const reached = new Set();
    const clipped = [];
    const overflowed = [];
    const undersizedTargets = [];
    const undersizedText = [];
    const internalScrollers = [];
    let unlinkedRecordIsHonest = false;
    let guard = 0;
    while (guard < expectedCount + 4) {
      guard += 1;
      const tracked = Array.from(document.querySelectorAll(
        ".nl-beam-evidence, .nl-beam-evidence__list, .nl-beam-evidence__record, .nl-beam-evidence__pagination"
      )).filter(visible);
      tracked.forEach((element) => {
        const rect = element.getBoundingClientRect();
        if (rect.left < boundary.left - tolerance || rect.top < boundary.top - tolerance ||
          rect.right > boundary.right + tolerance || rect.bottom > boundary.bottom + tolerance) {
          clipped.push(element.className || element.tagName);
        }
        if (element.scrollHeight > element.clientHeight + tolerance || element.scrollWidth > element.clientWidth + tolerance) {
          overflowed.push(element.className || element.tagName);
        }
      });
      Array.from(document.querySelectorAll(".nl-beam-evidence button, .nl-beam-evidence a[href]")).filter(visible)
        .forEach((element) => {
          const rect = element.getBoundingClientRect();
          if (rect.width + tolerance < 44 || rect.height + tolerance < 44) undersizedTargets.push(element.textContent.trim());
        });
      Array.from(document.querySelectorAll(".nl-beam-evidence h3, .nl-beam-evidence h4, .nl-beam-evidence p, .nl-beam-evidence small, .nl-beam-evidence span, .nl-beam-evidence button, .nl-beam-evidence a"))
        .filter(visible).filter((element) => element.textContent.trim())
        .forEach((element) => {
          if (Number.parseFloat(getComputedStyle(element).fontSize) + 0.05 < 12) undersizedText.push(element.textContent.trim());
        });
      Array.from(document.querySelectorAll(".nl-beam-evidence, .nl-beam-evidence *")).filter(visible)
        .forEach((element) => {
          if ([getComputedStyle(element).overflow, getComputedStyle(element).overflowX, getComputedStyle(element).overflowY]
            .some((value) => value === "auto" || value === "scroll")) internalScrollers.push(element.className || element.tagName);
        });
      Array.from(document.querySelectorAll(".nl-beam-evidence__record")).forEach((record) => {
        reached.add(Number(record.dataset.sourceIndex));
        const documentLabel = record.querySelector(".nl-beam-evidence__document");
        if (documentLabel) {
          unlinkedRecordIsHonest = Boolean(record.querySelector('button[data-act="request-field"]')) && !record.querySelector("a[href]");
        }
      });
      const next = document.querySelector(".nl-beam-evidence__pagination button:last-child");
      if (!next || next.disabled) break;
      next.click();
    }
    const section = document.querySelector(".nl-beam-evidence");
    return {
      clipped: Array.from(new Set(clipped)),
      overflowed: Array.from(new Set(overflowed)),
      internalScrollers: Array.from(new Set(internalScrollers)),
      undersizedTargets: Array.from(new Set(undersizedTargets)),
      undersizedText: Array.from(new Set(undersizedText)),
      reachedCount: reached.size,
      sourceCount: Number(section.dataset.sourceCount),
      pageSize: Number(section.dataset.pageSize),
      unlinkedRecordIsHonest,
      documentOverflow: {
        width: document.documentElement.scrollWidth - innerWidth,
        height: document.documentElement.scrollHeight - innerHeight
      }
    };
  }, { expectedCount, tolerance });
}

async function renderRfp(page, locale) {
  await page.evaluate((locale) => {
    const labels = window.NadlanCommercialI18n.get(locale);
    const asset = window.__nadlanFixtureAsset(6, locale);
    document.documentElement.lang = locale;
    document.documentElement.dir = labels.dir;
    const root = document.getElementById("fixture-root");
    root.innerHTML = '<main class="nl-commercial-tool fixture-tool"><header class="fixture-tool__head">RFP fixture</header><div class="fixture-tool__body"></div></main>';
    const composer = new window.NadlanCommercialRfpComposer.CommercialRfpComposer({
      asset,
      labels,
      locale,
      endpoint: "http://localhost:8080/wp-json/nadlan/v2/commercial-rfp-sandbox",
      environment: "test",
      sandboxPostId: 55,
      sandboxNonce: "fixture-signed-nonce",
      consentVersion: "fixture-v1",
      baseUrl: "http://localhost:8080/private-fixture/",
      allowInsecureLocalhost: true,
      fetchImpl() { throw new Error("The geometry fixture must never submit."); }
    });
    root.querySelector(".fixture-tool__body").appendChild(composer.render());
    window.__rfpFixture = composer;
  }, locale);
}

async function rfpGeometry(page, step) {
  return page.evaluate(({ step, tolerance }) => {
    const composer = window.__rfpFixture;
    composer.showStep(step, { focus: false });
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return !element.hidden && style.display !== "none" && style.visibility !== "hidden" &&
        element.getClientRects().length > 0 && rect.width > 1 && rect.height > 1;
    };
    const body = document.querySelector(".fixture-tool__body");
    const boundary = body.getBoundingClientRect();
    const tracked = Array.from(document.querySelectorAll(
      ".nl-rfp, .nl-rfp-context, .nl-rfp-form, .nl-rfp-progress, .nl-rfp-step, .nl-rfp-step__body, .nl-rfp-basket, .nl-rfp-question-chooser, .nl-rfp-question-choices, .nl-rfp-question-other, .nl-rfp-document-choices, .nl-rfp-choice-pager, .nl-rfp-field textarea, .nl-rfp-fields, .nl-rfp-consents, .nl-rfp-actions, .nl-rfp-feedback"
    )).filter(visible);
    const clipped = tracked.filter((element) => {
      const rect = element.getBoundingClientRect();
      return rect.left < boundary.left - tolerance || rect.top < boundary.top - tolerance ||
        rect.right > boundary.right + tolerance || rect.bottom > boundary.bottom + tolerance;
    }).map((element) => element.className || element.tagName);
    const overflowed = tracked.filter((element) =>
      element.scrollHeight > element.clientHeight + tolerance || element.scrollWidth > element.clientWidth + tolerance
    ).map((element) => ({ selector: element.className || element.tagName, client: [element.clientWidth, element.clientHeight], scroll: [element.scrollWidth, element.scrollHeight] }));
    const internalScrollers = Array.from(document.querySelectorAll(".nl-rfp, .nl-rfp *")).filter(visible)
      .filter((element) => [getComputedStyle(element).overflow, getComputedStyle(element).overflowX, getComputedStyle(element).overflowY]
        .some((value) => value === "auto" || value === "scroll"))
      .map((element) => element.className || element.tagName);
    const targetSelector = ".nl-rfp button, .nl-rfp-field input:not([type=checkbox]), .nl-rfp-field textarea, .nl-rfp-chip, .nl-rfp-consent";
    const undersizedTargets = Array.from(document.querySelectorAll(targetSelector)).filter(visible)
      .filter((element) => {
        const rect = element.getBoundingClientRect();
        return rect.width + tolerance < 44 || rect.height + tolerance < 44;
      }).map((element) => ({ selector: element.className || element.tagName, rect: element.getBoundingClientRect().toJSON() }));
    const undersizedText = Array.from(document.querySelectorAll(".nl-rfp h3, .nl-rfp p, .nl-rfp span, .nl-rfp dt, .nl-rfp dd, .nl-rfp legend, .nl-rfp label, .nl-rfp button"))
      .filter(visible).filter((element) => element.textContent.trim())
      .filter((element) => Number.parseFloat(getComputedStyle(element).fontSize) + 0.05 < 12)
      .map((element) => ({ selector: element.className || element.tagName, fontSize: getComputedStyle(element).fontSize }));
    const actions = document.querySelector(`.nl-rfp-step[data-rfp-step="${step}"] > .nl-rfp-actions`);
    const textarea = document.querySelector('textarea[name="question_text"]');
    const textareaVisible = textarea && visible(textarea);
    return {
      clipped,
      overflowed,
      internalScrollers,
      undersizedTargets,
      undersizedText,
      actionRowVisible: visible(actions),
      actionRowWithin: visible(actions) && actions.getBoundingClientRect().bottom <= boundary.bottom + tolerance,
      actionRect: actions ? actions.getBoundingClientRect().toJSON() : null,
      stepRect: document.querySelector(`.nl-rfp-step[data-rfp-step="${step}"]`)?.getBoundingClientRect().toJSON() || null,
      actionDisplay: actions ? getComputedStyle(actions).display : "missing",
      questionText: textareaVisible ? {
        valueLength: textarea.value.length,
        maxLength: textarea.maxLength,
        client: [textarea.clientWidth, textarea.clientHeight],
        scroll: [textarea.scrollWidth, textarea.scrollHeight],
        overflow: getComputedStyle(textarea).overflow,
        fullValueVisible: textarea.scrollWidth <= textarea.clientWidth + tolerance && textarea.scrollHeight <= textarea.clientHeight + tolerance
      } : null,
      documentOverflow: {
        width: document.documentElement.scrollWidth - innerWidth,
        height: document.documentElement.scrollHeight - innerHeight
      }
    };
  }, { step, tolerance });
}

async function traverseQuestionChoices(page) {
  return page.evaluate(() => {
    const seen = new Set();
    let guard = 0;
    while (guard < 10) {
      document.querySelectorAll('.nl-rfp-basket--paged .nl-rfp-chip:not([hidden]) input[name="question_ids"]').forEach((input) => seen.add(input.value));
      const next = document.querySelector('[data-rfp-action="question-page-next"]');
      if (!next || next.disabled) break;
      next.click();
      guard += 1;
    }
    return {
      values: Array.from(seen).sort(),
      pageStatus: document.querySelector(".nl-rfp-choice-pager__status")?.textContent.trim() || "",
      nextDisabled: Boolean(document.querySelector('[data-rfp-action="question-page-next"]')?.disabled)
    };
  });
}

async function traverseDocumentChoices(page) {
  return page.evaluate(() => {
    window.__rfpFixture.showStep(2, { focus: false });
    const seen = new Set();
    let guard = 0;
    while (guard < 10) {
      document.querySelectorAll('.nl-rfp-basket--documents .nl-rfp-chip:not([hidden]) input[name="document_ids"]').forEach((input) => seen.add(input.value));
      const next = document.querySelector('[data-rfp-action="document-page-next"]');
      if (!next || next.disabled) break;
      next.click();
      guard += 1;
    }
    return {
      values: Array.from(seen).sort(),
      pageStatus: document.querySelector(".nl-rfp-document-pager .nl-rfp-choice-pager__status")?.textContent.trim() || "",
      nextDisabled: Boolean(document.querySelector('[data-rfp-action="document-page-next"]')?.disabled)
    };
  });
}

async function openAndFillMaximumQuestion(page, locale) {
  const glyph = { he: "ש", en: "W", fr: "W", ru: "Ж", ar: "ش" }[locale];
  await page.locator('[data-rfp-action="question-other"]').click();
  const textarea = page.locator('textarea[name="question_text"]');
  const maxLength = await textarea.evaluate((element) => element.maxLength);
  await textarea.fill("");
  await textarea.pressSequentially(glyph.repeat(maxLength + 1));
  const entered = await textarea.inputValue();
  assert.equal(entered.length, maxLength, `${locale}: textarea maxlength must reject the extra unbroken character`);
  await page.locator('[data-rfp-action="question-choices"]').click();
  assert.equal(await textarea.isVisible(), false, `${locale}: one-tap return must restore the bounded choice view`);
  await page.locator('[data-rfp-action="question-other"]').click();
  assert.equal(await textarea.inputValue(), entered, `${locale}: leaving and reopening the free-question substate must preserve text`);
  return { maxLength, entered };
}

async function rfpRecoveryGeometry(page, failure) {
  await page.evaluate((failure) => {
    const composer = window.__rfpFixture;
    composer.hideRecovery();
    composer.message("");
    composer.presentFailure(failure);
  }, failure);
  return rfpGeometry(page, await page.evaluate(() => window.__rfpFixture.step));
}

const browser = await chromium.launch({ headless: true });
const sceneResults = [];
const evidenceResults = [];
const rfpResults = [];
const artifacts = [];

try {
  for (const viewport of viewports) {
    const { browserContext, page } = await createPage(browser, viewport);
    try {
      for (const locale of locales) {
        for (const sourceCount of sourceCounts) {
          const name = caseName(viewport, locale, `scene-${sourceCount}-sources`);
          await renderScene(page, locale, sourceCount);
          const geometry = await sceneGeometry(page);
          assertCleanGeometry(name, geometry);
          assert.equal(geometry.sourceCount, sourceCount, `${name}: source count contract changed`);
          assert.equal(geometry.directLinks, sourceCount > 4 ? 3 : sourceCount, `${name}: direct source count incorrect`);
          assert.equal(geometry.allSourcesActions, sourceCount > 4 ? 1 : 0, `${name}: All sources disclosure incorrect`);
          assert.equal(geometry.sourceControlCount, sourceCount > 4 ? 4 : sourceCount, `${name}: compact source controls incorrect`);
          assert.deepEqual(geometry.methodOverlaps, [], `${name}: method badge overlaps SVG labels`);
          assert.deepEqual(geometry.sourceOverlaps, [], `${name}: source controls overlap method badge`);
          assert.deepEqual(geometry.tinySvgText, [], `${name}: visible SVG buyer text is below 12px`);
          assert.deepEqual(geometry.textCollisions, [], `${name}: landmark/diagram text collides`);
          assert.equal(geometry.coneCount, 4, `${name}: all four evidenced facade cones must render`);
          assert.deepEqual(geometry.coneIds, ["north", "east", "south", "west"], `${name}: cone identity/order changed`);
          assert.equal(geometry.coneSignatureCount, 4, `${name}: cones are not visually distinguishable without relying on one shared style`);
          assert(geometry.coneHitSamples.every(Boolean), `${name}: a cone has no independently hittable painted interior`);
          assert.deepEqual(geometry.markerIds, ["north-landmark", "east-landmark", "south-landmark", "west-landmark"], `${name}: plotted landmark identity changed`);
          assert.deepEqual(geometry.legendIds, geometry.markerIds, `${name}: plot markers and landmark legend are not one-to-one`);
          assert(geometry.leaderLengths.length === 4 && geometry.leaderLengths.every((length) => length > 4), `${name}: every landmark needs a visible nonzero leader`);
          assert.deepEqual(geometry.legendNames, geometry.expectedLegendNames, `${name}: separately evidenced compact landmark names are not visible exactly`);
          geometry.expectedFullLabels.forEach((fullLabel, index) => {
            assert(geometry.legendArias[index].includes(fullLabel), `${name}: full sourced landmark name is missing from accessible legend output`);
          });
          assert.deepEqual(geometry.legendDistances, geometry.expectedLegendDistances, `${name}: full localized evidenced distances are not visible beside their callouts`);
          assert.deepEqual(geometry.legendDistanceArias, geometry.expectedDistanceArias, `${name}: distance cells lost their explicit metre units`);
          assert.equal(geometry.legendUnit, "m", `${name}: the shared visible distance unit is missing`);
          assert.equal(geometry.projectAnchorAccessible, true, `${name}: the project anchor lost its explicit accessible identity`);
          assert(geometry.methodText && geometry.methodAria, `${name}: compact method and full accessible method are required`);
          assert.equal(geometry.actionRowVisible, true, `${name}: save/compare/share row hidden`);
          assert.equal(geometry.factLabelCount, 3, `${name}: compact fact labels hidden`);
          const compactDoorTitles = viewport.name !== "desktop";
          assert.equal(geometry.doorLongVisibleCount, compactDoorTitles ? 0 : 4, `${name}: wrong long door-title mode`);
          assert.equal(geometry.doorShortVisibleCount, compactDoorTitles ? 4 : 0, `${name}: wrong compact door-title mode`);
          assert.equal(geometry.backIconVisible, true, `${name}: back icon hidden`);
          assert(geometry.model.width >= 70 && geometry.model.height >= 70, `${name}: 3D model ceased to be visibly present`);
          sceneResults.push({ name, sourceCount, controls: geometry.sourceControlCount, model: geometry.model });
          if (artifactDir && locale === "en" && sourceCount === 37) {
            const filename = `commercial-beam-${viewport.width}x${viewport.height}.png`;
            const output = path.join(artifactDir, filename);
            await page.screenshot({ path: output, fullPage: false });
            artifacts.push(output);
          }
        }

        for (const sourceCount of [6, 37]) {
          const name = caseName(viewport, locale, `evidence-${sourceCount}-sources`);
          await renderEvidenceTool(page, locale, sourceCount);
          const geometry = await evidenceGeometryAndReach(page, sourceCount);
          assertCleanGeometry(name, geometry);
          assert.equal(geometry.sourceCount, sourceCount, `${name}: evidence source count changed`);
          assert.equal(geometry.reachedCount, sourceCount, `${name}: not every source is reachable by bounded pagination`);
          assert.equal(geometry.unlinkedRecordIsHonest, true, `${name}: document-only source must be text plus request action, never a fake link`);
          evidenceResults.push({ name, sourceCount, pageSize: geometry.pageSize, reached: geometry.reachedCount });
          if (artifactDir && locale === "en" && sourceCount === 37 && viewport.name === "short-landscape") {
            const output = path.join(artifactDir, "commercial-beam-evidence-568x320.png");
            await page.screenshot({ path: output, fullPage: false });
            artifacts.push(output);
          }
        }

        await renderRfp(page, locale);
        const questionReach = await traverseQuestionChoices(page);
        assert.deepEqual(questionReach.values, [
          "asking_rent", "commute_and_transport", "live_availability", "nearby_facilities", "net_to_gross", "power_capacity"
        ], `${viewport.name}-${locale}: every question choice must be reachable through bounded pagination`);
        assert.equal(questionReach.nextDisabled, true, `${viewport.name}-${locale}: question pager must end honestly`);
        assert(questionReach.pageStatus, `${viewport.name}-${locale}: localized question-page status missing`);
        const choiceName = caseName(viewport, locale, "rfp-step-1-choices");
        const choiceGeometry = await rfpGeometry(page, 1);
        assertCleanGeometry(choiceName, choiceGeometry);
        assert.equal(choiceGeometry.actionRowVisible, true, `${choiceName}: action row hidden`);
        assert.equal(choiceGeometry.actionRowWithin, true, `${choiceName}: action row clipped`);

        const typedQuestion = await openAndFillMaximumQuestion(page, locale);
        const otherName = caseName(viewport, locale, "rfp-step-1-other-max-text");
        const otherGeometry = await rfpGeometry(page, 1);
        assertCleanGeometry(otherName, otherGeometry);
        assert(otherGeometry.questionText, `${otherName}: bounded free-question field missing`);
        assert.equal(otherGeometry.questionText.valueLength, typedQuestion.maxLength, `${otherName}: maximum text was not preserved`);
        assert.equal(otherGeometry.questionText.maxLength, 100, `${otherName}: bounded question contract changed`);
        assert.equal(otherGeometry.questionText.fullValueVisible, true, `${otherName}: maximum unbroken question text is not fully visible`);
        assert(!/auto|scroll/.test(otherGeometry.questionText.overflow), `${otherName}: textarea remains an inner scroller`);
        rfpResults.push({ name: choiceName, step: 1, substate: "choices" }, { name: otherName, step: 1, substate: "other-max-text" });

        const documentReach = await traverseDocumentChoices(page);
        assert.deepEqual(documentReach.values, [
          "availability_schedule", "floor_plan_pdf", "lease_draft", "measurement_report", "orientation_plan", "tenant_technical_manual"
        ], `${viewport.name}-${locale}: every document choice must be reachable through bounded pagination`);
        assert.equal(documentReach.nextDisabled, true, `${viewport.name}-${locale}: document pager must end honestly`);
        assert(documentReach.pageStatus, `${viewport.name}-${locale}: localized document-page status missing`);

        for (let step = 2; step <= windowStepCount(); step += 1) {
          const name = caseName(viewport, locale, `rfp-step-${step}`);
          const geometry = await rfpGeometry(page, step);
          assertCleanGeometry(name, geometry);
          assert.equal(geometry.actionRowVisible, true, `${name}: action row hidden ${JSON.stringify({ actionRect: geometry.actionRect, stepRect: geometry.stepRect, actionDisplay: geometry.actionDisplay, clipped: geometry.clipped, overflowed: geometry.overflowed })}`);
          assert.equal(geometry.actionRowWithin, true, `${name}: action row clipped`);
          rfpResults.push({ name, step });
          if (artifactDir && locale === "en" && step === 5 && viewport.name === "small-phone") {
            const output = path.join(artifactDir, "commercial-rfp-step5-320x568.png");
            await page.screenshot({ path: output, fullPage: false });
            artifacts.push(output);
          }
        }
        await page.evaluate(() => window.__rfpFixture.destroy());
      }

      const compactFailure = await renderOverlongCompactLabelScene(page);
      assert.equal(compactFailure.sceneState, "unknown", `${viewport.name}: overlong compact label must neutralize the adapted scene`);
      assert.equal(compactFailure.exposureCount, 0, `${viewport.name}: neutral compact-label scene leaked exposure data`);
      assert.equal(compactFailure.compactIssue, true, `${viewport.name}: compact-label failure lost its diagnostic issue`);
      assert.equal(compactFailure.renderedState, "unknown", `${viewport.name}: compact-label failure rendered a ready beam`);
      assert.equal(compactFailure.coneCount, 0, `${viewport.name}: compact-label failure leaked cones`);
      assert.equal(compactFailure.landmarkCount, 0, `${viewport.name}: compact-label failure leaked landmarks`);
      assert(compactFailure.requestCount >= 1, `${viewport.name}: compact-label failure must expose a request action`);

      await renderRfp(page, "en");
      const recoveryCases = [
        { code: "network", status: 0, field: "" },
        { code: "invalid_field", status: 422, field: "email" },
        { code: "consent_expired", status: 409, field: "privacy", consentVersion: "fixture-v2" },
        { code: "conflict", status: 409, field: "" }
      ];
      for (const failure of recoveryCases) {
        const name = caseName(viewport, "en", `rfp-recovery-${failure.code}`);
        const geometry = await rfpRecoveryGeometry(page, failure);
        assertCleanGeometry(name, geometry);
        assert.equal(geometry.actionRowWithin, true, `${name}: recovery action clipped`);
      }
      await page.evaluate(() => window.__rfpFixture.destroy());
    } finally {
      await browserContext.close();
    }
  }
} finally {
  await browser.close();
}

function windowStepCount() {
  return 5;
}

console.log(JSON.stringify({
  pass: true,
  matrix: {
    viewports: viewports.map(({ width, height }) => `${width}x${height}`),
    locales,
    sourceCounts,
    sceneCases: sceneResults.length,
    evidenceCases: evidenceResults.length,
    rfpStepCases: rfpResults.length
  },
  guarantees: [
    "3D model and decision surface remain visible in the same bounded viewport",
    "1/2/4 direct and 5+/37 source disclosures fit without inner scroll or clipping",
    "every orientation source is reachable in the bounded full-screen pager",
    "four independently styled and painted exposure cones retain one-to-one leaders, separately evidenced compact visible labels, and full accessible names",
    "method badge and every diagram/legend text box remain pairwise collision-free",
    "five RFP steps and stable recovery actions preserve visible 44px controls and 12px text"
  ],
  artifacts
}, null, 2));
