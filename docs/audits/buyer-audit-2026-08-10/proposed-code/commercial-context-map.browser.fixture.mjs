/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Real-Chromium geometry and delegated-action fixture. It loads only local
 * proposal assets, deliberately omits Mapbox (forcing the readable fallback),
 * makes no network request and never touches WordPress or the live site.
 *
 * Run:
 *   node commercial-context-map.browser.fixture.mjs
 */
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const here = path.dirname(fileURLToPath(import.meta.url));
const cssPath = path.join(here, "commercial-decision-surface.css");
const i18nPath = path.join(here, "commercial-i18n-additions.js");
const mapPath = path.join(here, "commercial-context-map.js");

const cases = [
  { name: "short-landscape-route-en", width: 568, height: 320, dpr: 1, locale: "en", recordKind: "route" },
  { name: "short-landscape-point-he-rtl", width: 568, height: 320, dpr: 1, locale: "he", recordKind: "point" },
  {
    name: "desktop-200-percent-effective-ar-rtl",
    width: 640,
    height: 400,
    dpr: 2,
    locale: "ar",
    recordKind: "route",
    physicalEquivalent: "1280x800"
  }
];

const browser = await chromium.launch({ headless: true });
const results = [];

try {
  for (const fixture of cases) {
    const browserContext = await browser.newContext({
      viewport: { width: fixture.width, height: fixture.height },
      deviceScaleFactor: fixture.dpr
    });
    const page = await browserContext.newPage();
    await page.setContent(`<!doctype html>
      <html><head><meta charset="utf-8"></head>
      <body>
        <main class="nl-commercial-tool fixture-tool">
          <header class="fixture-tool__head">Context fixture</header>
          <div class="fixture-tool__body"><div id="context-root"></div></div>
        </main>
      </body></html>`);
    await page.addStyleTag({ path: cssPath });
    await page.addStyleTag({ content: `
      html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }
      .fixture-tool { display: grid; grid-template-rows: 54px minmax(0, 1fr); width: 100%; height: 100%; background: var(--nl-cds-bg); }
      .fixture-tool__head { display: grid; align-items: center; min-height: 54px; padding-inline: 12px; color: var(--nl-cds-text); border-bottom: 1px solid var(--nl-cds-border); }
      .fixture-tool__body, #context-root { width: 100%; height: 100%; min-width: 0; min-height: 0; overflow: hidden; }
    ` });
    await page.evaluate(() => {
      window.NadlanCommercialContractAdapter = {
        normalizeEvidenceEnvelope(raw) {
          raw = raw && typeof raw === "object" ? raw : {};
          const sources = Array.isArray(raw.sources) ? raw.sources : [];
          const first = sources[0] || {};
          return {
            state: raw.state || "unknown",
            value: Object.prototype.hasOwnProperty.call(raw, "value") ? raw.value : null,
            sources,
            observations: raw.observations || [],
            sourceLabel: first.label || "",
            sourceUrl: first.uri || "",
            verifiedAt: raw.verifiedAt || "",
            effectiveAt: raw.effectiveAt || "",
            expiresAt: raw.expiresAt || "",
            ownerLabel: raw.ownerLabel || "",
            requiredDocumentIds: raw.requiredDocumentIds || [],
            confidence: raw.confidence || "high",
            scope: raw.scope || "",
            applicability: raw.applicability || ["all"],
            conflictIds: raw.conflictIds || [],
            caveat: raw.caveat || "",
            reason: raw.reason || "",
            note: raw.note || "",
            issues: raw.issues || []
          };
        }
      };
    });
    await page.addScriptTag({ path: i18nPath });
    await page.addScriptTag({ path: mapPath });

    await page.evaluate(({ locale, recordKind }) => {
      const labels = window.NadlanCommercialI18n.get(locale);
      document.documentElement.lang = locale;
      document.documentElement.dir = labels.dir;
      const sourced = (value, documentOnly = false) => ({
        state: "verified",
        value,
        scope: "Identity, state, geometry and dated travel range",
        sources: [{
          label: "Fixture authority",
          uri: documentOnly ? "" : "https://example.invalid/context",
          documentId: "fixture-context-document"
        }],
        verifiedAt: "2026-08-10T08:00:00Z",
        effectiveAt: "2026-08-10T07:55:00Z",
        expiresAt: "2027-08-10T08:00:00Z",
        confidence: "high",
        applicability: ["all"],
        caveat: ""
      });
      const route = (id, state, documentOnly) => ({
        id,
        mode: "commute",
        label: "HaShalom route",
        travel_mode: "walk",
        operating_state: state,
        stage: state === "planned" ? "approved" : "",
        expected_range: state === "planned" ? { from: "2030", to: "2031" } : "",
        geometry: [[34.79, 32.07], [34.8, 32.08]],
        minutes_min: 5,
        minutes_max: 8,
        transfers: 1,
        evidence: sourced(true, documentOnly)
      });
      const point = (id, state) => ({
        id,
        mode: "commute",
        category: "rail",
        name: "HaShalom station",
        coordinates: [34.8, 32.08],
        operating_state: state,
        network_distance_m: 420,
        minutes_min: 5,
        minutes_max: 8,
        evidence: sourced(true)
      });
      window.__contextActionCounts = { source: 0, request: 0 };
      const root = document.getElementById("context-root");
      root.addEventListener(
        window.NadlanCommercialContextMap.actionEvents.requestField,
        () => { window.__contextActionCounts.request += 1; }
      );
      window.__contextFixture = new window.NadlanCommercialContextMap.CommercialContextMap({
        root,
        labels,
        center: [34.8, 32.08],
        center_evidence: sourced("Project entrance"),
        routes: recordKind === "route" ? [
          route("route-document", "planned", true),
          route("route-operating", "operating", false)
        ] : [],
        points: recordKind === "point"
          ? [point("point-operating", "operating"), point("point-closed", "closed")]
          : [],
        onOpenSourceDocument() { window.__contextActionCounts.source += 1; }
      }).render();
    }, { locale: fixture.locale, recordKind: fixture.recordKind });

    const geometry = await page.evaluate(() => {
      const tolerance = 1.25;
      const body = document.querySelector(".fixture-tool__body");
      const boundary = body.getBoundingClientRect();
      const visible = (element) => {
        const style = getComputedStyle(element);
        return !element.hidden && style.display !== "none" && style.visibility !== "hidden" && element.getClientRects().length > 0;
      };
      const tracked = Array.from(document.querySelectorAll(
        ".nl-ccm-modes button, .nl-ccm-map-status, .nl-ccm-layout, .nl-ccm-results, .nl-ccm-record-list, .nl-ccm-card, .nl-ccm-route, .nl-ccm-pagination, .nl-ccm-source"
      )).filter(visible);
      const clipped = tracked.filter((element) => {
        const rect = element.getBoundingClientRect();
        return rect.left < boundary.left - tolerance || rect.top < boundary.top - tolerance ||
          rect.right > boundary.right + tolerance || rect.bottom > boundary.bottom + tolerance;
      }).map((element) => ({
        selector: element.className || element.tagName,
        rect: element.getBoundingClientRect().toJSON()
      }));
      const overflowed = Array.from(document.querySelectorAll(
        ".nl-ccm, .nl-ccm-map-status, .nl-ccm-layout, .nl-ccm-results, .nl-ccm-record-list, .nl-ccm-card, .nl-ccm-route, .nl-ccm-record__main, .nl-ccm-record__evidence, .nl-ccm-pagination, .nl-ccm-source"
      )).filter(visible).filter((element) =>
        element.scrollHeight > element.clientHeight + tolerance ||
        element.scrollWidth > element.clientWidth + tolerance
      ).map((element) => ({
        selector: element.className,
        client: [element.clientWidth, element.clientHeight],
        scroll: [element.scrollWidth, element.scrollHeight]
      }));
      const internalScrollers = Array.from(document.querySelectorAll(".nl-ccm, .nl-ccm *"))
        .filter(visible)
        .filter((element) => {
          const style = getComputedStyle(element);
          return [style.overflow, style.overflowX, style.overflowY].some((value) => value === "auto" || value === "scroll");
        })
        .map((element) => element.className || element.tagName);
      const undersizedTargets = Array.from(document.querySelectorAll(".nl-ccm button, .nl-ccm a[href]"))
        .filter(visible)
        .filter((element) => {
          const rect = element.getBoundingClientRect();
          return rect.width + tolerance < 44 || rect.height + tolerance < 44;
        })
        .map((element) => ({ selector: element.className || element.outerHTML.slice(0, 80), rect: element.getBoundingClientRect().toJSON() }));
      const undersizedText = Array.from(document.querySelectorAll(
        ".nl-ccm button, .nl-ccm a, .nl-ccm h4, .nl-ccm p, .nl-ccm small, .nl-ccm span"
      ))
        .filter(visible)
        .filter((element) => !element.closest(".nl-ccm-sr-only") && element.textContent.trim())
        .filter((element) => Number.parseFloat(getComputedStyle(element).fontSize) + 0.05 < 12)
        .map((element) => ({
          selector: element.className || element.tagName,
          fontSize: getComputedStyle(element).fontSize,
          text: element.textContent.trim().slice(0, 80)
        }));
      const section = document.querySelector(".nl-ccm");
      return {
        viewport: [innerWidth, innerHeight],
        dpr: devicePixelRatio,
        toolBody: boundary.toJSON(),
        directChildCount: section.children.length,
        gridRows: getComputedStyle(section).gridTemplateRows,
        mapHidden: document.querySelector('[data-role="map"]').hidden,
        mapState: section.dataset.mapState,
        recordCount: document.querySelectorAll(".nl-ccm-card, .nl-ccm-route").length,
        pagination: Boolean(document.querySelector(".nl-ccm-pagination")),
        clipped,
        overflowed,
        internalScrollers,
        undersizedTargets,
        undersizedText,
        documentOverflow: {
          width: document.documentElement.scrollWidth - innerWidth,
          height: document.documentElement.scrollHeight - innerHeight
        }
      };
    });

    assert.equal(geometry.directChildCount, 4, fixture.name + ": context grid must have four direct rows");
    assert.equal(geometry.mapHidden, true, fixture.name + ": failed map must be hidden");
    assert.equal(geometry.mapState, "unavailable", fixture.name + ": fallback state missing");
    assert.equal(geometry.recordCount, 1, fixture.name + ": short landscape must page one expanded record");
    assert.equal(geometry.pagination, true, fixture.name + ": pagination missing");
    assert.deepEqual(geometry.clipped, [], fixture.name + ": visible element clipped");
    assert.deepEqual(geometry.overflowed, [], fixture.name + ": content box overflowed");
    assert.deepEqual(geometry.internalScrollers, [], fixture.name + ": inner scroller introduced");
    assert.deepEqual(geometry.undersizedTargets, [], fixture.name + ": target below 44px");
    assert.deepEqual(geometry.undersizedText, [], fixture.name + ": visible buyer text below 12px");
    assert(geometry.documentOverflow.width <= 1 && geometry.documentOverflow.height <= 1, fixture.name + ": document overflowed");
    if (fixture.dpr === 2) {
      assert.equal(geometry.dpr, 2, fixture.name + ": 200%-effective DPR gate not active");
      assert.deepEqual(geometry.viewport, [640, 400], fixture.name + ": effective CSS viewport changed");
    }

    if (fixture === cases[0]) {
      await page.locator('[data-act="open-source-document"]').click();
      await page.locator('[data-map-mode="risk"]').click();
      await page.locator('[data-act="request-field"]').click();
      const actionCounts = await page.evaluate(() => window.__contextActionCounts);
      assert.deepEqual(actionCounts, { source: 1, request: 1 }, "Delegated actions did not fire exactly once each");
    }

    results.push({ ...fixture, geometry });
    await browserContext.close();
  }
} finally {
  await browser.close();
}

console.log(JSON.stringify({
  pass: true,
  note: "The DPR2 640x400 case is the effective CSS layout viewport of a 1280x800 surface at 200%.",
  cases: results
}, null, 2));
