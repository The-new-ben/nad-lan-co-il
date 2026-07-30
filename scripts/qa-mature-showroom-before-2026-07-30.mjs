#!/usr/bin/env node

/**
 * Immutable, read-only live BEFORE baseline for the mature NadLan showrooms.
 *
 * Safety:
 * - launches the installed Google Chrome channel;
 * - allows GET requests only;
 * - aborts contact, WhatsApp, co-tour, RFP and video-call endpoints;
 * - never fills or submits a form;
 * - uses a fresh browser context for every matrix and deep-interaction case;
 * - refuses to overwrite the final 2026-07-30 baseline directory.
 *
 * Usage:
 *   node scripts/qa-mature-showroom-before-2026-07-30.mjs
 */

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { chromium } from "playwright";

const ROOT = process.cwd();
const STAMP = "2026-07-30";
const PHASE = "BEFORE";
const SITE_ORIGIN = "https://nad-lan.co.il";
const FINAL_DIR = path.join(
  ROOT,
  "docs",
  "qa",
  "screenshots",
  `mature-showroom-before-${STAMP}`
);
const STAGING_DIR = path.join(
  ROOT,
  "docs",
  "qa",
  "screenshots",
  `.mature-showroom-before-${STAMP}-staging-${process.pid}-${Date.now()}`
);
const REPORT_NAME = "report.json";
const SUMMARY_NAME = "summary.md";
const HASH_NAME = "artifact-manifest.sha256";
const DEEP_MATRIX_MODE =
  process.env.NADLAN_MATURE_QA_DEEP_MATRIX === "all-viewports";
const HEADED_MODE = process.env.NADLAN_MATURE_QA_HEADED === "1";

const LANGS = ["he", "en", "fr", "ru", "ar"];
const RTL_LANGS = new Set(["he", "ar"]);
const LOCALES = {
  he: "he-IL",
  en: "en-US",
  fr: "fr-FR",
  ru: "ru-RU",
  ar: "ar",
};
const VIEWPORTS = {
  desktop: {
    viewport: { width: 1440, height: 1000 },
    isMobile: false,
    hasTouch: false,
  },
  mobile: {
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true,
  },
};
const FAMILIES = [
  {
    key: "duo-tel-aviv",
    label: "DUO",
    heUrl: `${SITE_ORIGIN}/projects/duo-tel-aviv/`,
  },
  {
    key: "rainbow-tel-aviv",
    label: "Rainbow",
    heUrl: `${SITE_ORIGIN}/projects/rainbow-tel-aviv/`,
  },
  {
    key: "dimri-yama-sde-dov",
    label: "Dimri Yama",
    heUrl: `${SITE_ORIGIN}/projects/dimri-yama-sde-dov/`,
  },
  {
    key: "ashira-sde-dov",
    label: "Ashira",
    heUrl: `${SITE_ORIGIN}/projects/ashira-sde-dov/`,
  },
];

const UNSAFE_URL_PATTERNS = [
  /\bwa\.me\b/iu,
  /(?:^|\/)(?:lead|leads|rfp|request-for-proposal)(?:\/|[?#]|$)/iu,
  /(?:^|[?&])(cotour|video(?:_?call)?|whatsapp)=/iu,
  /(?:^|\/)(?:cotour|video-call)(?:\/|[?#]|$)/iu,
  /^mailto:/iu,
  /^tel:/iu,
];

function clean(value, max = 1200) {
  return String(value ?? "")
    .replace(/access_token=[^&\s"']+/giu, "access_token=[redacted]")
    .replace(/\bpk\.[A-Za-z0-9._-]+/gu, "[map-token-redacted]")
    .replace(/\s+/gu, " ")
    .trim()
    .slice(0, max);
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    url.username = "";
    url.password = "";
    url.search = "";
    url.hash = "";
    return url.href;
  } catch {
    return clean(value, 500);
  }
}

function normalizeUrl(value) {
  try {
    const url = new URL(value);
    url.search = "";
    url.hash = "";
    if (!url.pathname.endsWith("/")) url.pathname += "/";
    return url.href;
  } catch {
    return "";
  }
}

function relativeFinal(fileName) {
  return path
    .relative(ROOT, path.join(FINAL_DIR, fileName))
    .replaceAll("\\", "/");
}

function attrValue(value) {
  return String(value).replaceAll("\\", "\\\\").replaceAll('"', '\\"');
}

function sha256(bytes) {
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function deltaDegrees(a, b) {
  if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
  const raw = Math.abs((((b - a) % 360) + 540) % 360 - 180);
  return Math.round(raw * 100) / 100;
}

function capability(name, status, details = {}) {
  return { name, status, ...details };
}

function isUnsafeUrl(url) {
  return UNSAFE_URL_PATTERNS.some((pattern) => pattern.test(String(url)));
}

function isFirstParty(url) {
  try {
    return new URL(url).origin === SITE_ORIGIN;
  } catch {
    return false;
  }
}

function makeEventBucket() {
  return {
    console_errors: [],
    console_warnings: [],
    page_errors: [],
    response_failures: [],
    request_failures: [],
    guard_blocks: [],
    first_party_non_get_attempts: [],
  };
}

async function installReadOnlyGuard(context, events) {
  await context.route("**/*", async (route) => {
    const request = route.request();
    const method = request.method().toUpperCase();
    const url = request.url();
    const firstParty = isFirstParty(url);
    const unsafeUrl = isUnsafeUrl(url);
    const shouldBlock = method !== "GET" || unsafeUrl;
    if (shouldBlock) {
      const row = {
        method,
        url: safeUrl(url),
        resource_type: request.resourceType(),
        first_party: firstParty,
        reason: method !== "GET" ? "non-GET request" : "unsafe contact endpoint",
      };
      events.guard_blocks.push(row);
      if (firstParty && method !== "GET") {
        events.first_party_non_get_attempts.push(row);
      }
      await route.abort("blockedbyclient");
      return;
    }
    await route.continue();
  });
}

function wireEvents(page, events) {
  page.on("console", (message) => {
    const text = clean(message.text());
    if (message.type() === "error") events.console_errors.push(text);
    if (message.type() === "warning") events.console_warnings.push(text);
  });
  page.on("pageerror", (error) => {
    events.page_errors.push(clean(error?.message || error));
  });
  page.on("response", (response) => {
    if (response.status() < 400) return;
    events.response_failures.push({
      status: response.status(),
      method: response.request().method(),
      resource_type: response.request().resourceType(),
      first_party: isFirstParty(response.url()),
      url: safeUrl(response.url()),
    });
  });
  page.on("requestfailed", (request) => {
    const blocked = events.guard_blocks.some(
      (row) => row.method === request.method() && row.url === safeUrl(request.url())
    );
    events.request_failures.push({
      method: request.method(),
      resource_type: request.resourceType(),
      first_party: isFirstParty(request.url()),
      guard_blocked: blocked,
      error: clean(request.failure()?.errorText || "unknown request failure"),
      url: safeUrl(request.url()),
    });
  });
}

function firstPartyFailures(events) {
  return [
    ...events.response_failures.filter((row) => row.first_party),
    ...events.request_failures.filter(
      (row) => row.first_party && !row.guard_blocked
    ),
  ];
}

async function createGuardedContext(
  browser,
  { lang = "he", viewportName = "desktop" } = {}
) {
  const events = makeEventBucket();
  const vp = VIEWPORTS[viewportName];
  const context = await browser.newContext({
    viewport: vp.viewport,
    deviceScaleFactor: 1,
    isMobile: vp.isMobile,
    hasTouch: vp.hasTouch,
    locale: LOCALES[lang] || LOCALES.he,
    acceptDownloads: false,
    serviceWorkers: "block",
    extraHTTPHeaders: {
      "cache-control": "no-cache",
      pragma: "no-cache",
    },
  });
  await installReadOnlyGuard(context, events);
  const page = await context.newPage();
  page.setDefaultTimeout(10_000);
  wireEvents(page, events);
  return { context, page, events };
}

async function navigate(page, url) {
  const response = await page.goto(url, {
    waitUntil: "domcontentloaded",
    timeout: 60_000,
  });
  await page.waitForTimeout(1_350);
  return {
    status: response?.status() || 0,
    final_url: safeUrl(page.url()),
    redirected:
      Boolean(response) &&
      normalizeUrl(response.url()) !== normalizeUrl(url),
  };
}

async function discoverFamily(browser, family) {
  const { context, page, events } = await createGuardedContext(browser, {
    lang: "he",
    viewportName: "desktop",
  });
  try {
    const navigation = await navigate(page, family.heUrl);
    const discovery = await page.evaluate(() => {
      const absolute = (value) => {
        try {
          return new URL(value, location.href).href;
        } catch {
          return "";
        }
      };
      const hreflang = [
        ...document.querySelectorAll(
          'link[rel~="alternate"][hreflang][href]'
        ),
      ].map((link) => ({
        lang: String(link.getAttribute("hreflang") || "").toLowerCase(),
        href: absolute(link.getAttribute("href")),
      }));
      const showroomLinks = [
        ...document.querySelectorAll(
          '#nl-root a[data-act="lang"][data-id][href]'
        ),
      ].map((link) => ({
        lang: String(link.getAttribute("data-id") || "").toLowerCase(),
        href: absolute(link.getAttribute("href")),
      }));
      return {
        canonical: [
          ...document.querySelectorAll('link[rel~="canonical"][href]'),
        ].map((link) => absolute(link.getAttribute("href"))),
        hreflang,
        showroom_links: showroomLinks,
      };
    });
    const urls = {};
    const sources = {};
    for (const lang of LANGS) {
      const fromHreflang = discovery.hreflang.find(
        (row) => row.lang === lang && row.href
      );
      const fromShowroom = discovery.showroom_links.find(
        (row) => row.lang === lang && row.href
      );
      const chosen = fromHreflang || fromShowroom;
      if (chosen) {
        urls[lang] = normalizeUrl(chosen.href);
        sources[lang] = fromHreflang ? "hreflang" : "showroom-language-link";
      }
    }
    return {
      family: family.key,
      requested_url: family.heUrl,
      navigation,
      canonical: discovery.canonical.map(normalizeUrl),
      advertised_hreflang: discovery.hreflang.map((row) => ({
        lang: row.lang,
        href: normalizeUrl(row.href),
      })),
      advertised_showroom_links: discovery.showroom_links.map((row) => ({
        lang: row.lang,
        href: normalizeUrl(row.href),
      })),
      urls,
      sources,
      first_party_failures: firstPartyFailures(events),
      console_errors: events.console_errors,
      safety: {
        guard_blocks: events.guard_blocks,
        first_party_non_get_attempts: events.first_party_non_get_attempts,
      },
    };
  } catch (error) {
    return {
      family: family.key,
      requested_url: family.heUrl,
      navigation: { status: 0, final_url: "", redirected: false },
      canonical: [],
      advertised_hreflang: [],
      advertised_showroom_links: [],
      urls: {},
      sources: {},
      error: clean(error?.stack || error, 3000),
      first_party_failures: firstPartyFailures(events),
      console_errors: events.console_errors,
      safety: {
        guard_blocks: events.guard_blocks,
        first_party_non_get_attempts: events.first_party_non_get_attempts,
      },
    };
  } finally {
    await context.close();
  }
}

async function inspectStaticState(page) {
  return page.evaluate(() => {
    const cleanText = (value) =>
      String(value || "")
        .replace(/\s+/gu, " ")
        .trim();
    const absolute = (value) => {
      try {
        return new URL(value, location.href).href;
      } catch {
        return "";
      }
    };
    const visible = (element) => {
      if (!element) return false;
      const rect = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      return (
        rect.width > 0 &&
        rect.height > 0 &&
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        Number(style.opacity || 1) > 0
      );
    };
    const primaryRoot =
      document.querySelector("#nl-root") ||
      document.querySelector("[data-nlv2-showroom]") ||
      document.querySelector(".nlp3d");
    const models = [...document.querySelectorAll("model-viewer")];
    const model = models.find(visible) || models[0] || null;
    const modelRect = model?.getBoundingClientRect() || null;
    const canonicals = [
      ...document.querySelectorAll('link[rel~="canonical"][href]'),
    ].map((link) => absolute(link.getAttribute("href")));
    const hreflang = [
      ...document.querySelectorAll(
        'link[rel~="alternate"][hreflang][href]'
      ),
    ].map((link) => ({
      lang: cleanText(link.getAttribute("hreflang")).toLowerCase(),
      href: absolute(link.getAttribute("href")),
    }));
    const clientWidth = document.documentElement.clientWidth;
    const scrollWidth = Math.max(
      document.documentElement.scrollWidth,
      document.body?.scrollWidth || 0
    );
    return {
      title: document.title,
      location: location.href,
      html_lang: document.documentElement.lang,
      html_dir: document.documentElement.dir,
      computed_dir: getComputedStyle(document.documentElement).direction,
      canonical: canonicals,
      hreflang,
      h1_count: document.querySelectorAll("h1").length,
      h1_texts: [...document.querySelectorAll("h1")]
        .slice(0, 8)
        .map((node) => cleanText(node.textContent)),
      root_counts: {
        nl_root: document.querySelectorAll("#nl-root").length,
        nl_app: document.querySelectorAll("#nl-root.nl-app").length,
        nlp3d: document.querySelectorAll(".nlp3d").length,
        nlv2: document.querySelectorAll("[data-nlv2-showroom]").length,
        primary: primaryRoot ? 1 : 0,
      },
      model: {
        count: models.length,
        visible_count: models.filter(visible).length,
        loaded_count: models.filter((node) => node.loaded === true).length,
        visible_model_count: models.filter(
          (node) => node.modelIsVisible === true && visible(node)
        ).length,
        src: model ? absolute(model.getAttribute("src")) : "",
        rect: modelRect
          ? {
              left: Math.round(modelRect.left),
              right: Math.round(modelRect.right),
              top: Math.round(modelRect.top),
              bottom: Math.round(modelRect.bottom),
              width: Math.round(modelRect.width),
              height: Math.round(modelRect.height),
            }
          : null,
      },
      hotspot_counts: {
        unit_selectors: primaryRoot
          ? primaryRoot.querySelectorAll('[data-act="select"][data-id]').length
          : 0,
        model_unit_hotspots: primaryRoot
          ? primaryRoot.querySelectorAll(
              '.nl-hot[data-act="select"][data-id], model-viewer [slot^="hotspot-"][data-act="select"][data-id]'
            ).length
          : 0,
        facade_unit_hotspots: primaryRoot
          ? primaryRoot.querySelectorAll(
              '.nl-fsq[data-act="select"][data-id], .nlp3d-stage-pick[data-unit]'
            ).length
          : 0,
        building_hotspots: primaryRoot
          ? primaryRoot.querySelectorAll(
              '[data-act="building"], .nl-building-hot'
            ).length
          : 0,
      },
      exposed_controls: {
        studio: primaryRoot
          ? primaryRoot.querySelectorAll(
              '[data-act="studio"],[data-act="studio-any"]'
            ).length
          : 0,
        unit_tabs: primaryRoot
          ? primaryRoot.querySelectorAll('[data-act="tab"]').length
          : 0,
        map_layers: document.querySelectorAll(
          ".nlpjx-maplayers button[data-layer]"
        ).length,
        satellite: document.querySelectorAll(
          '.nlpjx-maplayers button[data-layer="sat"]'
        ).length,
        map_3d: document.querySelectorAll(
          '.nlpjx-maplayers button[data-layer="3d"]'
        ).length,
      },
      unified_map: {
        section_count: document.querySelectorAll("#nlpjx-map").length,
        host_count: document.querySelectorAll("#nlpjx-unimap").length,
        canvas_count: document.querySelectorAll(
          "#nlpjx-unimap .mapboxgl-canvas"
        ).length,
        global_ready:
          Boolean(window.NLPJX_MAP) &&
          typeof window.NLPJX_MAP.getBearing === "function",
      },
      client_width: clientWidth,
      scroll_width: scrollWidth,
      horizontal_overflow_px: Math.max(0, scrollWidth - clientWidth),
    };
  });
}

function staticHealth(caseRow, expectedLang, expectedDir, discoveredUrls) {
  const state = caseRow.state;
  const requested = normalizeUrl(caseRow.url);
  const canonical = state.canonical.map(normalizeUrl);
  const hreflangMap = {};
  for (const row of state.hreflang) {
    if (!hreflangMap[row.lang]) hreflangMap[row.lang] = [];
    hreflangMap[row.lang].push(normalizeUrl(row.href));
  }
  const expectedHreflangs = {
    ...discoveredUrls,
    "x-default": discoveredUrls.he || "",
  };
  const assertions = [
    {
      name: "browser document HTTP 200",
      pass: caseRow.navigation.status === 200,
      actual: caseRow.navigation.status,
      expected: 200,
    },
    {
      name: "no redirect",
      pass: caseRow.navigation.redirected === false,
      actual: caseRow.navigation.redirected,
      expected: false,
    },
    {
      name: "document language",
      pass:
        state.html_lang.toLowerCase().split("-")[0] === expectedLang,
      actual: state.html_lang,
      expected: expectedLang,
    },
    {
      name: "document direction",
      pass: (state.html_dir || state.computed_dir) === expectedDir,
      actual: state.html_dir || state.computed_dir,
      expected: expectedDir,
    },
    {
      name: "one self canonical",
      pass:
        canonical.length === 1 &&
        canonical[0] === requested,
      actual: canonical,
      expected: [requested],
    },
    {
      name: "one mature showroom root",
      pass: state.root_counts.nl_root === 1,
      actual: state.root_counts,
      expected: { nl_root: 1 },
    },
    {
      name: "at least one model-viewer",
      pass: state.model.count >= 1,
      actual: state.model.count,
      expected: ">=1",
    },
    {
      name: "at least one trusted unit selector",
      pass: state.hotspot_counts.unit_selectors >= 1,
      actual: state.hotspot_counts,
      expected: "unit_selectors>=1",
    },
    {
      name: "no horizontal overflow",
      pass: state.horizontal_overflow_px === 0,
      actual: state.horizontal_overflow_px,
      expected: 0,
    },
    {
      name: "no console errors",
      pass: caseRow.events.console_errors.length === 0,
      actual: caseRow.events.console_errors,
      expected: [],
    },
    {
      name: "no page errors",
      pass: caseRow.events.page_errors.length === 0,
      actual: caseRow.events.page_errors,
      expected: [],
    },
    {
      name: "no first-party network failures",
      pass: caseRow.first_party_failures.length === 0,
      actual: caseRow.first_party_failures,
      expected: [],
    },
    {
      name: "no first-party non-GET attempts",
      pass:
        caseRow.events.first_party_non_get_attempts.length === 0,
      actual: caseRow.events.first_party_non_get_attempts,
      expected: [],
    },
  ];
  for (const [lang, url] of Object.entries(expectedHreflangs)) {
    assertions.push({
      name: `one exact ${lang} hreflang`,
      pass:
        Boolean(url) &&
        JSON.stringify(hreflangMap[lang] || []) ===
          JSON.stringify([normalizeUrl(url)]),
      actual: hreflangMap[lang] || [],
      expected: url ? [normalizeUrl(url)] : ["advertised sibling URL"],
    });
  }
  return {
    status: assertions.every((row) => row.pass)
      ? "pass"
      : "baseline_defect",
    assertions,
    failed_assertions: assertions
      .filter((row) => !row.pass)
      .map((row) => row.name),
  };
}

async function runMatrixCase(
  browser,
  family,
  lang,
  url,
  viewportName,
  discoveredUrls
) {
  const { context, page, events } = await createGuardedContext(browser, {
    lang,
    viewportName,
  });
  const fileBase = `${family.key}-${lang}-${viewportName}`;
  const topFile = `${fileBase}-top.png`;
  const showroomFile = `${fileBase}-showroom.png`;
  try {
    const navigation = await navigate(page, url);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(120);
    await page.screenshot({
      path: path.join(STAGING_DIR, topFile),
      fullPage: false,
    });

    const root = page.locator("#nl-root");
    const rootCount = await root.count();
    let showroomScreenshot = null;
    if (rootCount === 1) {
      await root.scrollIntoViewIfNeeded();
      await page.waitForTimeout(350);
      await page.screenshot({
        path: path.join(STAGING_DIR, showroomFile),
        fullPage: false,
      });
      showroomScreenshot = relativeFinal(showroomFile);
    }

    const state = await inspectStaticState(page);
    const row = {
      family: family.key,
      label: family.label,
      lang,
      viewport: viewportName,
      viewport_size: VIEWPORTS[viewportName].viewport,
      url,
      navigation,
      state,
      events,
      first_party_failures: firstPartyFailures(events),
      screenshots: {
        top: relativeFinal(topFile),
        showroom: showroomScreenshot,
      },
    };
    row.health = staticHealth(
      row,
      lang,
      RTL_LANGS.has(lang) ? "rtl" : "ltr",
      discoveredUrls
    );
    return row;
  } catch (error) {
    return {
      family: family.key,
      label: family.label,
      lang,
      viewport: viewportName,
      viewport_size: VIEWPORTS[viewportName].viewport,
      url,
      navigation: { status: 0, final_url: "", redirected: false },
      state: null,
      events,
      first_party_failures: firstPartyFailures(events),
      screenshots: { top: null, showroom: null },
      health: {
        status: "baseline_capture_error",
        assertions: [],
        failed_assertions: ["case threw before static state was preserved"],
      },
      error: clean(error?.stack || error, 4000),
    };
  } finally {
    await context.close();
  }
}

function scoreCase(row) {
  if (!row?.state) return -1000;
  let score = 0;
  if (row.navigation.status === 200) score += 20;
  if (row.state.root_counts.nl_root === 1) score += 20;
  if (row.state.model.count >= 1) score += 15;
  if (row.state.hotspot_counts.unit_selectors >= 1) score += 15;
  if (row.state.exposed_controls.studio >= 1) score += 10;
  if (row.state.exposed_controls.map_layers >= 1) score += 10;
  if (row.state.horizontal_overflow_px === 0) score += 5;
  score -= row.events.console_errors.length * 2;
  score -= row.first_party_failures.length * 5;
  score -= LANGS.indexOf(row.lang) / 100;
  return score;
}

async function waitForFunction(page, fn, timeout = 15_000) {
  try {
    await page.waitForFunction(fn, null, { timeout });
    return true;
  } catch {
    return false;
  }
}

async function inspectDeepCore(page) {
  return page.evaluate(() => {
    const mv = document.querySelector("#nl-mv, #nl-root model-viewer");
    const orbit = () => {
      try {
        if (mv && typeof mv.getCameraOrbit === "function") {
          const value = mv.getCameraOrbit();
          return {
            theta: Number(value.theta),
            phi: Number(value.phi),
            radius: Number(value.radius),
          };
        }
      } catch {}
      return null;
    };
    return {
      selected_unit:
        window.NadLanEngine?.state?.unitId ||
        document.querySelector(
          '#nl-root [data-act="select"].is-active[data-id]'
        )?.getAttribute("data-id") ||
        "",
      panel_open: Boolean(
        document.querySelector("#nl-panel.is-open")
      ),
      panel_title: String(
        document.querySelector(".nl-panel__title")?.textContent || ""
      )
        .replace(/\s+/gu, " ")
        .trim(),
      active_selectors: document.querySelectorAll(
        '#nl-root [data-act="select"].is-active[data-id]'
      ).length,
      reset_visible: (() => {
        const el = document.querySelector("#nl-resetview");
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        return !el.hidden && rect.width > 0 && rect.height > 0;
      })(),
      scrim_on: Boolean(
        document.querySelector("#nl-scrim.is-on")
      ),
      lift_count: document.querySelectorAll(".nl-lift").length,
      interpolation_decay:
        mv && Number.isFinite(Number(mv.interpolationDecay))
          ? Number(mv.interpolationDecay)
          : null,
      camera_orbit_attribute: mv?.getAttribute("camera-orbit") || "",
      camera_target_attribute: mv?.getAttribute("camera-target") || "",
      camera_orbit_property: mv
        ? String(mv.cameraOrbit || "")
        : "",
      camera_target_property: mv
        ? String(mv.cameraTarget || "")
        : "",
      camera_orbit: orbit(),
      map_bearing:
        window.NLPJX_MAP &&
        typeof window.NLPJX_MAP.getBearing === "function"
          ? Number(window.NLPJX_MAP.getBearing())
          : null,
    };
  });
}

async function discoverUnitTarget(page) {
  return page.evaluate(() => {
    const visible = (element) => {
      if (!element) return false;
      const rect = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      return (
        rect.width > 0 &&
        rect.height > 0 &&
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        Number(style.opacity || 1) > 0
      );
    };
    const contracts = [
      {
        kind: "model-hotspot",
        selector: '#nl-root .nl-hot[data-act="select"][data-id]',
      },
      {
        kind: "facade-hotspot",
        selector: '#nl-root .nl-fsq[data-act="select"][data-id]',
      },
      {
        kind: "inventory-card",
        selector:
          '#nl-root .nl-ucard[role="button"][data-act="select"][data-id]',
      },
    ];
    for (const contract of contracts) {
      const nodes = [...document.querySelectorAll(contract.selector)];
      const selected = nodes.find(visible);
      if (selected) {
        return {
          kind: contract.kind,
          selector_contract: contract.selector,
          id: selected.getAttribute("data-id") || "",
          aria_label: selected.getAttribute("aria-label") || "",
          count: nodes.length,
        };
      }
    }
    return null;
  });
}

async function runStudio(page, selectedId, familyKey) {
  const launch = await page.evaluate((id) => {
    const visible = (element) => {
      if (!element) return false;
      const rect = element.getBoundingClientRect();
      const style = getComputedStyle(element);
      return (
        rect.width > 0 &&
        rect.height > 0 &&
        style.display !== "none" &&
        style.visibility !== "hidden"
      );
    };
    const exact = document.querySelector(
      `#nl-root [data-act="studio"][data-id="${CSS.escape(id)}"]`
    );
    if (exact && visible(exact)) {
      return {
        contract:
          '#nl-root [data-act="studio"][data-id="<selected-unit>"]',
        selector:
          '#nl-root [data-act="studio"][data-id="' +
          id.replaceAll("\\", "\\\\").replaceAll('"', '\\"') +
          '"]',
      };
    }
    const any = [
      ...document.querySelectorAll(
        '#nl-root [data-act="studio-any"]'
      ),
    ].find(visible);
    if (any) {
      return {
        contract: '#nl-root [data-act="studio-any"]',
        selector: '#nl-root [data-act="studio-any"]',
      };
    }
    return null;
  }, selectedId);
  if (!launch) {
    return capability("apartment_studio", "absent", {
      exposed: false,
      reason: "no visible live Studio launch control",
    });
  }

  const launchLocator = page.locator(launch.selector);
  const launchCount = await launchLocator.count();
  if (launchCount !== 1) {
    return capability("apartment_studio", "pre_existing_broken", {
      exposed: true,
      observed_selector: launch,
      reason: `live selector resolved to ${launchCount} controls`,
    });
  }

  try {
    await launchLocator.click();
    const opened = await waitForFunction(
      page,
      () => Boolean(document.querySelector("#nlst")),
      5_000
    );
    if (!opened) {
      return capability("apartment_studio", "pre_existing_broken", {
        exposed: true,
        observed_selector: launch,
        reason: "launch click did not open #nlst",
      });
    }
    const studioFile = `${familyKey}-deep-studio-open.png`;
    await page.screenshot({
      path: path.join(STAGING_DIR, studioFile),
      fullPage: false,
    });

    const addTarget = await page.evaluate(() => {
      const visible = (element) => {
        const rect = element.getBoundingClientRect();
        const style = getComputedStyle(element);
        return (
          rect.width > 0 &&
          rect.height > 0 &&
          style.display !== "none" &&
          style.visibility !== "hidden"
        );
      };
      const node = [
        ...document.querySelectorAll("#nlst [data-add]"),
      ].find(visible);
      return node
        ? {
            id: node.getAttribute("data-add"),
            count: document.querySelectorAll("#nlst [data-add]").length,
          }
        : null;
    });
    if (!addTarget?.id) {
      return capability("apartment_studio", "pre_existing_broken", {
        exposed: true,
        opened: true,
        reason: "Studio opened without an exposed add-item control",
        screenshot: relativeFinal(studioFile),
      });
    }

    const initialCount = await page.locator("#nlst .nlst-it").count();
    const addSelector = `#nlst [data-add="${attrValue(addTarget.id)}"]`;
    const addLocator = page.locator(addSelector);
    const addCount = await addLocator.count();
    const undoLocator = page.locator('#nlst [data-st="undo"]');
    const clearLocator = page.locator('#nlst [data-st="clear"]');
    const closeLocator = page.locator('#nlst [data-st="close"]');
    const controlCounts = {
      add: addCount,
      undo: await undoLocator.count(),
      clear: await clearLocator.count(),
      close: await closeLocator.count(),
    };
    if (Object.values(controlCounts).some((value) => value !== 1)) {
      return capability("apartment_studio", "pre_existing_broken", {
        exposed: true,
        opened: true,
        observed_selector: launch,
        control_counts: controlCounts,
        reason: "one or more observed Studio controls are not unique",
        screenshot: relativeFinal(studioFile),
      });
    }

    await addLocator.click();
    const afterAdd = await page.locator("#nlst .nlst-it").count();
    await undoLocator.click();
    const afterUndo = await page.locator("#nlst .nlst-it").count();

    await addLocator.click();
    const beforePersistClose = await page
      .locator("#nlst .nlst-it")
      .count();
    await closeLocator.click();
    const closed = (await page.locator("#nlst").count()) === 0;
    await launchLocator.click();
    await waitForFunction(
      page,
      () => Boolean(document.querySelector("#nlst")),
      5_000
    );
    const afterReopen = await page.locator("#nlst .nlst-it").count();
    const clearAgain = page.locator('#nlst [data-st="clear"]');
    const closeAgain = page.locator('#nlst [data-st="close"]');
    const clearAgainCount = await clearAgain.count();
    const closeAgainCount = await closeAgain.count();
    if (clearAgainCount === 1) await clearAgain.click();
    const afterClear = await page.locator("#nlst .nlst-it").count();
    if (closeAgainCount === 1) await closeAgain.click();

    const checks = {
      opened,
      add:
        afterAdd === initialCount + 1,
      undo: afterUndo === initialCount,
      persistence:
        closed &&
        beforePersistClose === initialCount + 1 &&
        afterReopen === beforePersistClose,
      clear: afterClear === 0,
    };
    return capability(
      "apartment_studio",
      Object.values(checks).every(Boolean)
        ? "passed"
        : "pre_existing_broken",
      {
        exposed: true,
        observed_selector: launch,
        add_item: addTarget,
        counts: {
          initial: initialCount,
          after_add: afterAdd,
          after_undo: afterUndo,
          before_persist_close: beforePersistClose,
          after_reopen: afterReopen,
          after_clear: afterClear,
        },
        checks,
        screenshot: relativeFinal(studioFile),
      }
    );
  } catch (error) {
    return capability("apartment_studio", "pre_existing_broken", {
      exposed: true,
      observed_selector: launch,
      reason: clean(error?.stack || error, 2500),
    });
  }
}

async function installMapInstrumentation(page) {
  return page.evaluate(() => {
    window.__MATURE_QA_MAP_CALLS =
      window.__MATURE_QA_MAP_CALLS || [];
    const proto = window.mapboxgl?.Map?.prototype;
    if (!proto) return false;
    if (proto.__matureQaWrapped) return true;
    const methods = [
      "setFreeCameraOptions",
      "setBearing",
      "easeTo",
      "setLayoutProperty",
    ];
    for (const method of methods) {
      const original = proto[method];
      if (typeof original !== "function") continue;
      proto[method] = function (...args) {
        try {
          window.__MATURE_QA_MAP_CALLS.push({
            method,
            at: Date.now(),
            args: args.map((arg) => {
              if (arg == null) return arg;
              if (
                typeof arg === "string" ||
                typeof arg === "number" ||
                typeof arg === "boolean"
              ) {
                return arg;
              }
              if (method === "easeTo") {
                return {
                  bearing: Number(arg.bearing),
                  pitch: Number(arg.pitch),
                  zoom: Number(arg.zoom),
                  duration: Number(arg.duration),
                };
              }
              return String(arg);
            }),
          });
        } catch {}
        return original.apply(this, args);
      };
    }
    Object.defineProperty(proto, "__matureQaWrapped", {
      value: true,
      configurable: true,
    });
    return true;
  });
}

async function runUnifiedMap(page, familyKey) {
  const exposure = await page.evaluate(() => ({
    section: document.querySelectorAll("#nlpjx-map").length,
    host: document.querySelectorAll("#nlpjx-unimap").length,
    controls: [
      ...document.querySelectorAll(
        ".nlpjx-maplayers button[data-layer]"
      ),
    ].map((button) => ({
      layer: button.getAttribute("data-layer") || "",
      text: String(button.textContent || "")
        .replace(/\s+/gu, " ")
        .trim(),
      active: button.classList.contains("is-on"),
      disabled: button.disabled,
    })),
  }));
  if (!exposure.section || !exposure.host) {
    return capability("unified_map", "absent", {
      exposed: false,
      exposure,
    });
  }

  const host = page.locator("#nlpjx-unimap");
  if ((await host.count()) !== 1) {
    return capability("unified_map", "pre_existing_broken", {
      exposed: true,
      exposure,
      reason: "#nlpjx-unimap is not unique",
    });
  }
  await host.scrollIntoViewIfNeeded();
  const ready = await waitForFunction(
    page,
    () =>
      Boolean(window.NLPJX_MAP) &&
      typeof window.NLPJX_MAP.getBearing === "function" &&
      Boolean(window.NLPJX_MAP.loaded?.()),
    25_000
  );
  const mapFile = `${familyKey}-deep-unified-map.png`;
  await page.screenshot({
    path: path.join(STAGING_DIR, mapFile),
    fullPage: false,
  });
  if (!ready) {
    return capability("unified_map", "pre_existing_broken", {
      exposed: true,
      exposure,
      ready: false,
      reason: "unified Mapbox instance did not become ready",
      screenshot: relativeFinal(mapFile),
    });
  }

  await installMapInstrumentation(page);
  const facility = await page.evaluate(() => {
    const candidates = [
      ...document.querySelectorAll(
        ".nlpjx-maplayers button[data-layer]"
      ),
    ].filter((button) =>
      ["schools", "parks", "transit", "shops", "health", "food"].includes(
        button.getAttribute("data-layer")
      )
    );
    const usable =
      candidates.find((button) => {
        const match = String(button.textContent || "").match(/\((\d+)\)\s*$/);
        return !button.disabled && (!match || Number(match[1]) > 0);
      }) || candidates.find((button) => !button.disabled);
    return usable
      ? {
          layer: usable.getAttribute("data-layer"),
          text: String(usable.textContent || "")
            .replace(/\s+/gu, " ")
            .trim(),
        }
      : null;
  });

  const toggles = {};
  if (facility?.layer) {
    const selector = `.nlpjx-maplayers button[data-layer="${attrValue(
      facility.layer
    )}"]`;
    const locator = page.locator(selector);
    const count = await locator.count();
    if (count === 1) {
      const before = await locator.evaluate((node) => ({
        active: node.classList.contains("is-on"),
        marker_count: document.querySelectorAll(
          "#nlpjx-unimap .mapboxgl-marker"
        ).length,
      }));
      await locator.click();
      await page.waitForTimeout(350);
      const after = await locator.evaluate((node) => ({
        active: node.classList.contains("is-on"),
        marker_count: document.querySelectorAll(
          "#nlpjx-unimap .mapboxgl-marker"
        ).length,
      }));
      toggles.facility = {
        observed_selector: selector,
        target: facility,
        before,
        after,
        pass: before.active !== after.active,
      };
      await locator.click();
    } else {
      toggles.facility = {
        observed_selector: selector,
        target: facility,
        count,
        pass: false,
      };
    }
  } else {
    toggles.facility = {
      pass: false,
      status: "absent",
      reason: "no observed facility layer control",
    };
  }

  for (const layer of ["sat", "3d"]) {
    const selector = `.nlpjx-maplayers button[data-layer="${layer}"]`;
    const locator = page.locator(selector);
    const count = await locator.count();
    if (count !== 1) {
      toggles[layer] = {
        observed_selector: selector,
        count,
        pass: false,
        status: "absent",
      };
      continue;
    }
    const before = await page.evaluate((targetLayer) => {
      const layerId = targetLayer === "sat" ? "nl-sat" : "nl-3d";
      const map = window.NLPJX_MAP;
      return {
        layer_exists: Boolean(map?.getLayer?.(layerId)),
        visibility: map?.getLayer?.(layerId)
          ? map.getLayoutProperty(layerId, "visibility")
          : null,
        pitch: Number(map?.getPitch?.()),
      };
    }, layer);
    await locator.click();
    await page.waitForTimeout(1_050);
    const after = await page.evaluate((targetLayer) => {
      const layerId = targetLayer === "sat" ? "nl-sat" : "nl-3d";
      const map = window.NLPJX_MAP;
      return {
        layer_exists: Boolean(map?.getLayer?.(layerId)),
        visibility: map?.getLayer?.(layerId)
          ? map.getLayoutProperty(layerId, "visibility")
          : null,
        pitch: Number(map?.getPitch?.()),
      };
    }, layer);
    toggles[layer] = {
      observed_selector: selector,
      before,
      after,
      pass:
        before.layer_exists &&
        after.visibility === "visible" &&
        before.visibility !== after.visibility,
    };
    if (after.visibility === "visible") {
      await locator.click();
      await page.waitForTimeout(250);
    }
  }

  return capability(
    "unified_map",
    Object.values(toggles).every((row) => row.pass)
      ? "passed"
      : "pre_existing_broken",
    {
      exposed: true,
      ready: true,
      exposure,
      toggles,
      screenshot: relativeFinal(mapFile),
    }
  );
}

async function runModelMapBearing(page) {
  const model = page.locator("#nl-mv");
  const modelCount = await model.count();
  const mapReady = await page.evaluate(
    () =>
      Boolean(window.NLPJX_MAP) &&
      typeof window.NLPJX_MAP.getBearing === "function"
  );
  if (modelCount !== 1 || !mapReady) {
    return capability("model_to_map_bearing", "skipped_prerequisite", {
      exposed: modelCount === 1,
      model_count: modelCount,
      map_ready: mapReady,
      reason:
        "requires one #nl-mv and a ready window.NLPJX_MAP instance",
    });
  }
  await model.scrollIntoViewIfNeeded();
  await page.evaluate(() => {
    window.__MATURE_QA_CAMERA_EVENTS = [];
    const mv = document.querySelector("#nl-mv");
    if (!mv || mv.dataset.matureQaCameraListener) return;
    mv.dataset.matureQaCameraListener = "1";
    mv.addEventListener("camera-change", (event) => {
      let orbit = null;
      try {
        const value = mv.getCameraOrbit();
        orbit = {
          theta: Number(value.theta),
          phi: Number(value.phi),
          radius: Number(value.radius),
        };
      } catch {}
      window.__MATURE_QA_CAMERA_EVENTS.push({
        source: event.detail?.source || "",
        orbit,
        at: Date.now(),
      });
    });
  });
  const before = await inspectDeepCore(page);
  const box = await model.boundingBox();
  if (!box || box.width < 80 || box.height < 80) {
    return capability("model_to_map_bearing", "pre_existing_broken", {
      exposed: true,
      reason: "model is present but has no usable drag box",
      box,
      before,
    });
  }
  const start = {
    x: box.x + box.width * 0.58,
    y: box.y + box.height * 0.52,
  };
  await page.mouse.move(start.x, start.y);
  await page.mouse.down();
  await page.mouse.move(start.x + Math.min(150, box.width * 0.22), start.y, {
    steps: 12,
  });
  await page.mouse.up();
  await page.waitForTimeout(850);
  const after = await inspectDeepCore(page);
  const cameraEvents = await page.evaluate(
    () => window.__MATURE_QA_CAMERA_EVENTS || []
  );
  const userEvents = cameraEvents.filter(
    (row) => row.source === "user-interaction"
  );
  const bearingDelta = deltaDegrees(
    before.map_bearing,
    after.map_bearing
  );
  const pass =
    userEvents.length > 0 &&
    Number.isFinite(bearingDelta) &&
    bearingDelta >= 0.1;
  return capability(
    "model_to_map_bearing",
    pass ? "passed" : "pre_existing_broken",
    {
      exposed: true,
      drag_box: box,
      before,
      after,
      bearing_delta_degrees: bearingDelta,
      camera_events: cameraEvents.slice(-20),
      user_interaction_events: userEvents.length,
    }
  );
}

async function runWindowView(page, selectedId, familyKey) {
  const tabSelector =
    '#nl-root [data-act="tab"][data-id="view"]';
  const tab = page.locator(tabSelector);
  const tabCount = await tab.count();
  if (tabCount === 0) {
    return capability("window_view", "absent", {
      exposed: false,
      observed_selector: tabSelector,
    });
  }
  if (tabCount !== 1) {
    return capability("window_view", "pre_existing_broken", {
      exposed: true,
      observed_selector: tabSelector,
      count: tabCount,
    });
  }

  await installMapInstrumentation(page);
  const callsBefore = await page.evaluate(
    () => (window.__MATURE_QA_MAP_CALLS || []).length
  );
  await tab.click();
  await page.waitForTimeout(450);
  const stageCount = await page.locator("#nl-root .nl-winstage").count();
  const pane = await page.evaluate(() => ({
    text: String(
      document.querySelector("#nl-root .nl-tabpane")?.textContent || ""
    )
      .replace(/\s+/gu, " ")
      .trim()
      .slice(0, 800),
    winlook_count: document.querySelectorAll(
      '#nl-root [data-act="winlook"]'
    ).length,
    winfs_count: document.querySelectorAll(
      '#nl-root [data-act="winfs"]'
    ).length,
  }));
  if (stageCount !== 1) {
    return capability("window_view", "not_exposed", {
      exposed: true,
      observed_selector: tabSelector,
      selected_unit: selectedId,
      stage_count: stageCount,
      pane,
      reason:
        "view tab exists but this live unit/page does not expose the window-map stage",
    });
  }

  const ready = await waitForFunction(
    page,
    () =>
      document.querySelectorAll(
        "#nl-root .nl-winstage .mapboxgl-canvas"
      ).length === 1,
    20_000
  );
  const windowFile = `${familyKey}-deep-window-view.png`;
  const stage = page.locator("#nl-root .nl-winstage");
  await stage.scrollIntoViewIfNeeded();
  await page.waitForTimeout(250);
  await page.screenshot({
    path: path.join(STAGING_DIR, windowFile),
    fullPage: false,
  });
  if (!ready) {
    return capability("window_view", "pre_existing_broken", {
      exposed: true,
      observed_selector: tabSelector,
      selected_unit: selectedId,
      stage_count: stageCount,
      pane,
      ready: false,
      reason: "window stage appeared but its Mapbox canvas did not",
      screenshot: relativeFinal(windowFile),
    });
  }

  const leftSelector = `#nl-root [data-act="winlook"][data-id="${attrValue(
    selectedId
  )}"][data-d="-30"]`;
  const rightSelector = `#nl-root [data-act="winlook"][data-id="${attrValue(
    selectedId
  )}"][data-d="30"]`;
  const fsSelector = '#nl-root [data-act="winfs"]';
  const left = page.locator(leftSelector);
  const right = page.locator(rightSelector);
  const fsButton = page.locator(fsSelector);
  const controlCounts = {
    left: await left.count(),
    right: await right.count(),
    fullscreen: await fsButton.count(),
  };
  if (Object.values(controlCounts).some((value) => value !== 1)) {
    return capability("window_view", "pre_existing_broken", {
      exposed: true,
      ready: true,
      observed_selectors: {
        tab: tabSelector,
        left: leftSelector,
        right: rightSelector,
        fullscreen: fsSelector,
      },
      control_counts: controlCounts,
      reason: "window view controls are not uniquely exposed",
      screenshot: relativeFinal(windowFile),
    });
  }

  const callCount0 = await page.evaluate(
    () => (window.__MATURE_QA_MAP_CALLS || []).length
  );
  await left.click();
  await page.waitForTimeout(350);
  const callCountLeft = await page.evaluate(
    () => (window.__MATURE_QA_MAP_CALLS || []).length
  );
  await right.click();
  await page.waitForTimeout(350);
  const callCountRight = await page.evaluate(
    () => (window.__MATURE_QA_MAP_CALLS || []).length
  );
  await fsButton.click();
  await page.waitForTimeout(450);
  const fullscreen = await page.evaluate(() => {
    const stageNode = document.querySelector("#nl-root .nl-winstage");
    return {
      fallback_class: Boolean(
        stageNode?.classList.contains("nl-winstage--fs")
      ),
      native: document.fullscreenElement === stageNode,
      body_locked: document.body.classList.contains("nl-winfs-lock"),
      label:
        document.querySelector(
          '#nl-root [data-act="winfs"]'
        )?.getAttribute("aria-label") || "",
    };
  });
  try {
    if (fullscreen.native) {
      await page.keyboard.press("Escape");
      await page.waitForTimeout(200);
    } else if (fullscreen.fallback_class) {
      await fsButton.click();
      await page.waitForTimeout(200);
    }
  } catch {}

  const calls = await page.evaluate((start) => {
    return (window.__MATURE_QA_MAP_CALLS || []).slice(start);
  }, callsBefore);
  const checks = {
    left_turn_called_map:
      callCountLeft > callCount0,
    right_turn_called_map:
      callCountRight > callCountLeft,
    fullscreen_entered:
      fullscreen.native || fullscreen.fallback_class,
  };
  return capability(
    "window_view",
    Object.values(checks).every(Boolean)
      ? "passed"
      : "pre_existing_broken",
    {
      exposed: true,
      ready: true,
      selected_unit: selectedId,
      observed_selectors: {
        tab: tabSelector,
        left: leftSelector,
        right: rightSelector,
        fullscreen: fsSelector,
      },
      checks,
      fullscreen,
      instrumented_map_calls: calls.slice(-30),
      screenshot: relativeFinal(windowFile),
    }
  );
}

async function runDeepCase(
  browser,
  family,
  lang,
  url,
  viewportName = "desktop"
) {
  const { context, page, events } = await createGuardedContext(browser, {
    lang,
    viewportName,
  });
  const artifactKey = DEEP_MATRIX_MODE
    ? `${family.key}-${lang}-${viewportName}`
    : family.key;
  const result = {
    family: family.key,
    label: family.label,
    lang,
    url,
    viewport_name: viewportName,
    viewport: VIEWPORTS[viewportName].viewport,
    fresh_context: true,
    navigation: null,
    observed_unit_target: null,
    capabilities: [],
    events,
    screenshots: {},
  };
  try {
    result.navigation = await navigate(page, url);
    const rootReady = await waitForFunction(
      page,
      () => document.querySelectorAll("#nl-root").length === 1,
      12_000
    );
    if (!rootReady) {
      result.capabilities.push(
        capability("trusted_unit_selection_cinematic", "absent", {
          exposed: false,
          reason: "one #nl-root was not present",
        })
      );
      return result;
    }

    const root = page.locator("#nl-root");
    await root.scrollIntoViewIfNeeded();
    await page.waitForTimeout(550);
    const target = await discoverUnitTarget(page);
    result.observed_unit_target = target;
    if (!target?.id) {
      result.capabilities.push(
        capability("trusted_unit_selection_cinematic", "absent", {
          exposed: false,
          reason: "no visible live unit selector was observed",
        })
      );
      result.capabilities.push(
        capability("apartment_studio", "skipped_prerequisite", {
          reason: "no selected live unit",
        })
      );
      result.capabilities.push(
        capability("window_view", "skipped_prerequisite", {
          reason: "no selected live unit",
        })
      );
    } else {
      const selector = `${target.selector_contract}[data-id="${attrValue(
        target.id
      )}"]`;
      const locator = page.locator(selector);
      const count = await locator.count();
      if (count !== 1) {
        result.capabilities.push(
          capability(
            "trusted_unit_selection_cinematic",
            "pre_existing_broken",
            {
              exposed: true,
              observed_selector: selector,
              count,
              reason:
                "observed visible target did not resolve uniquely",
            }
          )
        );
      } else {
        await locator.scrollIntoViewIfNeeded();
        const before = await inspectDeepCore(page);
        await locator.click();
        await page.waitForTimeout(90);
        const during = await inspectDeepCore(page);
        await page.waitForTimeout(360);
        const afterBeat = await inspectDeepCore(page);
        await page.waitForTimeout(1_150);
        const settled = await inspectDeepCore(page);
        const selectedFile = `${artifactKey}-deep-selected-unit.png`;
        await page.screenshot({
          path: path.join(STAGING_DIR, selectedFile),
          fullPage: false,
        });
        result.screenshots.selected_unit =
          relativeFinal(selectedFile);
        const cameraChanged =
          JSON.stringify(before.camera_orbit) !==
            JSON.stringify(settled.camera_orbit) ||
          before.camera_orbit_property !==
            settled.camera_orbit_property ||
          before.camera_target_property !==
            settled.camera_target_property;
        const cinematicObserved =
          during.lift_count > 0 ||
          during.interpolation_decay === 160 ||
          afterBeat.interpolation_decay === 160 ||
          cameraChanged;
        const checks = {
          panel_open: settled.panel_open,
          selected_unit_matches: settled.selected_unit === target.id,
          active_selector_present: settled.active_selectors >= 1,
          cinematic_observed: cinematicObserved,
          reset_control_visible: settled.reset_visible,
        };
        result.capabilities.push(
          capability(
            "trusted_unit_selection_cinematic",
            Object.values(checks).every(Boolean)
              ? "passed"
              : "pre_existing_broken",
            {
              exposed: true,
              observed_selector: selector,
              target,
              checks,
              before,
              during,
              after_first_beat: afterBeat,
              settled,
              screenshot: relativeFinal(selectedFile),
            }
          )
        );
      }

      result.capabilities.push(
        await runStudio(page, target.id, artifactKey)
      );
    }

    const mapCapability = await runUnifiedMap(page, artifactKey);
    result.capabilities.push(mapCapability);
    result.capabilities.push(await runModelMapBearing(page));

    if (target?.id) {
      result.capabilities.push(
        await runWindowView(page, target.id, artifactKey)
      );
    }
    result.first_party_failures = firstPartyFailures(events);
    result.safety = {
      first_party_non_get_attempts:
        events.first_party_non_get_attempts,
      guard_blocks: events.guard_blocks,
    };
    return result;
  } catch (error) {
    result.error = clean(error?.stack || error, 5000);
    result.capabilities.push(
      capability("deep_path", "error", {
        reason: result.error,
      })
    );
    result.first_party_failures = firstPartyFailures(events);
    result.safety = {
      first_party_non_get_attempts:
        events.first_party_non_get_attempts,
      guard_blocks: events.guard_blocks,
    };
    return result;
  } finally {
    await context.close();
  }
}

function summarize(report) {
  const capturedCases = report.matrix.filter(
    (row) => row.state && row.screenshots.top
  ).length;
  const cleanCases = report.matrix.filter(
    (row) => row.health.status === "pass"
  ).length;
  const brokenCases = report.matrix.filter(
    (row) => row.health.status === "baseline_defect"
  ).length;
  const captureErrors = report.matrix.filter(
    (row) => row.health.status === "baseline_capture_error"
  ).length;
  const deepCaps = report.deep.flatMap((row) =>
    row.capabilities.map((cap) => ({
      family: row.family,
      lang: row.lang,
      ...cap,
    }))
  );
  const capabilityCounts = {};
  for (const row of deepCaps) {
    capabilityCounts[row.status] =
      (capabilityCounts[row.status] || 0) + 1;
  }
  const advertisedSiblingCount = report.discovery.reduce(
    (sum, row) => sum + Object.keys(row.urls).length,
    0
  );
  const firstPartyWriteAttempts = [
    ...report.discovery.flatMap(
      (row) => row.safety?.first_party_non_get_attempts || []
    ),
    ...report.matrix.flatMap(
      (row) => row.events?.first_party_non_get_attempts || []
    ),
    ...report.deep.flatMap(
      (row) => row.events?.first_party_non_get_attempts || []
    ),
  ];
  const unsafeGuardBlocks = [
    ...report.discovery.flatMap(
      (row) => row.safety?.guard_blocks || []
    ),
    ...report.matrix.flatMap(
      (row) => row.events?.guard_blocks || []
    ),
    ...report.deep.flatMap(
      (row) => row.events?.guard_blocks || []
    ),
  ];
  const expectedDeepCases = DEEP_MATRIX_MODE ? 40 : 4;
  const regressionReady =
    report.matrix.length === 40 &&
    capturedCases === 40 &&
    report.deep.length === expectedDeepCases &&
    firstPartyWriteAttempts.length === 0;
  return {
    advertised_language_siblings: advertisedSiblingCount,
    expected_advertised_language_siblings: 20,
    matrix_cases: report.matrix.length,
    expected_matrix_cases: 40,
    captured_cases: capturedCases,
    clean_cases: cleanCases,
    baseline_defect_cases: brokenCases,
    capture_error_cases: captureErrors,
    deep_cases: report.deep.length,
    expected_deep_cases: expectedDeepCases,
    deep_families: new Set(report.deep.map((row) => row.family)).size,
    capability_status_counts: capabilityCounts,
    first_party_non_get_attempts: firstPartyWriteAttempts,
    guard_blocks: unsafeGuardBlocks,
    regression_ready: regressionReady,
    surface_health_pass: cleanCases === 40,
    interpretation:
      "regression_ready means the immutable BEFORE evidence is complete and safe to compare later; it does not relabel pre-existing defects as passes.",
  };
}

function markdownSummary(report) {
  const lines = [];
  lines.push(
    `# Mature showroom live baseline - ${PHASE} - ${STAMP}`,
    "",
    "Read-only Google Chrome baseline for DUO, Rainbow, Dimri Yama and Ashira across advertised HE/EN/FR/RU/AR siblings at 1440x1000 and 390x844.",
    "",
    `- Matrix captured: ${report.summary.captured_cases}/${report.summary.expected_matrix_cases}`,
    `- Static health clean: ${report.summary.clean_cases}/${report.summary.expected_matrix_cases}`,
    `- Pre-existing static defects: ${report.summary.baseline_defect_cases}`,
    `- Capture errors: ${report.summary.capture_error_cases}`,
    `- Deep journey cases: ${report.summary.deep_cases}/${report.summary.expected_deep_cases}`,
    `- First-party non-GET attempts: ${report.summary.first_party_non_get_attempts.length}`,
    `- Regression-ready BEFORE evidence: ${report.summary.regression_ready ? "YES" : "NO"}`,
    "",
    "Regression-ready means the BEFORE evidence can be compared after UTOPIA work. Missing or broken live capabilities remain explicitly classified and are never counted as passes.",
    "",
    "## Static matrix",
    "",
    "| Project | Language | Viewport | HTTP | Root | Model | Unit selectors | Overflow | Result |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---|"
  );
  for (const row of report.matrix) {
    lines.push(
      `| ${row.label} | ${row.lang} | ${row.viewport} | ${row.navigation.status} | ${row.state?.root_counts?.nl_root ?? "-"} | ${row.state?.model?.count ?? "-"} | ${row.state?.hotspot_counts?.unit_selectors ?? "-"} | ${row.state?.horizontal_overflow_px ?? "-"} | ${row.health.status} |`
    );
  }
  lines.push(
    "",
    "## Deep client-only paths",
    "",
    "| Project | Language | Capability | Classification |",
    "|---|---:|---|---|"
  );
  for (const row of report.deep) {
    for (const cap of row.capabilities) {
      lines.push(
        `| ${row.label} | ${row.lang} | ${cap.name} | ${cap.status} |`
      );
    }
  }
  lines.push(
    "",
    "## Safety boundary",
    "",
    "The runner allowed GET requests only. It did not fill or submit forms and did not click WhatsApp, RFP, video-call or co-tour controls. Every blocked request is preserved in the JSON report.",
    "",
    "## Re-run command",
    "",
    "```powershell",
    "node scripts/qa-mature-showroom-before-2026-07-30.mjs",
    "```",
    ""
  );
  return `${lines.join("\n")}\n`;
}

async function writeHashManifest() {
  const entries = [];
  const files = await fs.readdir(STAGING_DIR, {
    recursive: true,
    withFileTypes: true,
  });
  for (const entry of files) {
    if (!entry.isFile()) continue;
    const fullPath = path.join(entry.parentPath, entry.name);
    if (fullPath.endsWith(HASH_NAME)) continue;
    const bytes = await fs.readFile(fullPath);
    entries.push({
      relative: path.relative(STAGING_DIR, fullPath).replaceAll("\\", "/"),
      hash: sha256(bytes),
    });
  }
  entries.sort((a, b) => a.relative.localeCompare(b.relative));
  const body = entries
    .map((row) => `${row.hash}  ${row.relative}`)
    .join("\n");
  await fs.writeFile(
    path.join(STAGING_DIR, HASH_NAME),
    `${body}\n`,
    "utf8"
  );
  return entries;
}

if (await fs.stat(FINAL_DIR).then(() => true).catch(() => false)) {
  throw new Error(
    `Refusing to overwrite immutable BEFORE baseline: ${FINAL_DIR}`
  );
}
await fs.mkdir(STAGING_DIR, { recursive: true });

const browser = await chromium.launch({
  channel: "chrome",
  headless: !HEADED_MODE,
  args: ["--disable-background-networking"],
});

const report = {
  schema: "nadlan-mature-showroom-before/v1",
  phase: PHASE,
  stamp: STAMP,
  generated_at: new Date().toISOString(),
  site_origin: SITE_ORIGIN,
  browser: {
    requested_channel: "chrome",
    product: "Google Chrome",
    version: browser.version(),
    headless: !HEADED_MODE,
  },
  safety_contract: {
    request_methods_allowed: ["GET"],
    first_party_non_get: "aborted and reported",
    unsafe_contact_urls: "aborted and reported",
    forms_filled: false,
    forms_submitted: false,
    whatsapp_clicked: false,
    rfp_clicked: false,
    video_call_clicked: false,
    cotour_clicked: false,
  },
  families: FAMILIES,
  viewports: VIEWPORTS,
  discovery: [],
  missing_advertised_siblings: [],
  matrix: [],
  deep: [],
  deep_matrix_mode: DEEP_MATRIX_MODE
    ? "all-languages-and-viewports"
    : "best-desktop-language-per-family",
};

try {
  for (const family of FAMILIES) {
    const row = await discoverFamily(browser, family);
    report.discovery.push(row);
    console.log(
      `[discover] ${family.key}: ${Object.keys(row.urls).join(",") || "none"}`
    );
  }

  for (const family of FAMILIES) {
    const discovery = report.discovery.find(
      (row) => row.family === family.key
    );
    for (const lang of LANGS) {
      const url = discovery?.urls?.[lang];
      if (!url) {
        report.missing_advertised_siblings.push({
          family: family.key,
          lang,
          status: "not_advertised_on_live_he_page",
        });
        continue;
      }
      for (const viewportName of Object.keys(VIEWPORTS)) {
        const row = await runMatrixCase(
          browser,
          family,
          lang,
          url,
          viewportName,
          discovery.urls
        );
        report.matrix.push(row);
        console.log(
          `[matrix] ${family.key}/${lang}/${viewportName}: ${row.navigation.status} ${row.health.status}`
        );
      }
    }
  }

  if (DEEP_MATRIX_MODE) {
    for (const family of FAMILIES) {
      for (const lang of LANGS) {
        for (const viewportName of Object.keys(VIEWPORTS)) {
          const captured = report.matrix.find(
            (row) =>
              row.family === family.key &&
              row.lang === lang &&
              row.viewport === viewportName
          );
          if (!captured?.url) {
            report.deep.push({
              family: family.key,
              label: family.label,
              lang,
              url: null,
              viewport_name: viewportName,
              viewport: VIEWPORTS[viewportName].viewport,
              fresh_context: false,
              navigation: null,
              observed_unit_target: null,
              capabilities: [
                capability("deep_path", "skipped_prerequisite", {
                  reason: "no captured working language URL",
                }),
              ],
              events: makeEventBucket(),
            });
            continue;
          }
          const deep = await runDeepCase(
            browser,
            family,
            lang,
            captured.url,
            viewportName
          );
          report.deep.push(deep);
          console.log(
            `[deep] ${family.key}/${lang}/${viewportName}: ${deep.capabilities
              .map((row) => `${row.name}=${row.status}`)
              .join(", ")}`
          );
        }
      }
    }
  } else {
    for (const family of FAMILIES) {
      const candidates = report.matrix
        .filter(
          (row) =>
            row.family === family.key &&
            row.viewport === "desktop"
        )
        .sort((a, b) => scoreCase(b) - scoreCase(a));
      const best = candidates[0];
      if (!best?.url) {
        report.deep.push({
          family: family.key,
          label: family.label,
          lang: null,
          url: null,
          fresh_context: false,
          navigation: null,
          observed_unit_target: null,
          capabilities: [
            capability("deep_path", "skipped_prerequisite", {
              reason: "no captured working language URL",
            }),
          ],
          events: makeEventBucket(),
        });
        continue;
      }
      const deep = await runDeepCase(
        browser,
        family,
        best.lang,
        best.url
      );
      deep.language_selection = {
        strategy:
          "highest static live score, stable preference HE then EN/FR/RU/AR",
        candidate_scores: candidates.map((row) => ({
          lang: row.lang,
          score: scoreCase(row),
          health: row.health.status,
        })),
      };
      report.deep.push(deep);
      console.log(
        `[deep] ${family.key}/${best.lang}: ${deep.capabilities
          .map((row) => `${row.name}=${row.status}`)
          .join(", ")}`
      );
    }
  }
} finally {
  await browser.close();
}

report.summary = summarize(report);
report.artifact_manifest = relativeFinal(HASH_NAME);
await fs.writeFile(
  path.join(STAGING_DIR, REPORT_NAME),
  `${JSON.stringify(report, null, 2)}\n`,
  "utf8"
);
await fs.writeFile(
  path.join(STAGING_DIR, SUMMARY_NAME),
  markdownSummary(report),
  "utf8"
);
await writeHashManifest();
await fs.rename(STAGING_DIR, FINAL_DIR);

console.log(
  JSON.stringify(
    {
      phase: PHASE,
      stamp: STAMP,
      final_dir: FINAL_DIR,
      report: path.join(FINAL_DIR, REPORT_NAME),
      summary: path.join(FINAL_DIR, SUMMARY_NAME),
      hash_manifest: path.join(FINAL_DIR, HASH_NAME),
      regression_ready: report.summary.regression_ready,
      surface_health_pass: report.summary.surface_health_pass,
      matrix: `${report.summary.captured_cases}/${report.summary.expected_matrix_cases}`,
    },
    null,
    2
  )
);

process.exitCode = report.summary.regression_ready ? 0 : 1;
