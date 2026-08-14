#!/usr/bin/env node

/**
 * End-to-end acceptance runner for the password-protected unit-journey sandbox.
 *
 * Required environment variables:
 *   SANDBOX_URL
 *   SANDBOX_POST_PASSWORD
 * Optional:
 *   OUTPUT_DIR
 *
 * Security contract:
 * - The post password is read only from the environment and is never printed or
 *   serialized. Error messages are redacted defensively before they are stored.
 * - Empty validation must emit zero lead POSTs. One valid submission is locally
 *   intercepted and fulfilled by Playwright; it never reaches the server.
 * - The reports contain measurements and public URLs, but no cookies, request
 *   headers, form values, HTML snapshots, or browser storage.
 *
 * Important: Playwright viewport/orientation emulation is a deterministic
 * browser gate. It is not a substitute for acceptance on the owner's physical
 * phone, its browser chrome, virtual keyboard, GPU, network, or cache state.
 */

import { chromium } from "playwright";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const SANDBOX_URL = String(process.env.SANDBOX_URL || "").trim();
const POST_PASSWORD = String(process.env.SANDBOX_POST_PASSWORD || "");
const OUTPUT_DIR = path.resolve(
  process.cwd(),
  String(process.env.OUTPUT_DIR || "docs/qa/private-unit-journey").trim() ||
    "docs/qa/private-unit-journey"
);

const VIEWPORTS = [
  { width: 320, height: 568, name: "320x568" },
  { width: 360, height: 640, name: "360x640" },
  { width: 375, height: 812, name: "375x812" },
  { width: 430, height: 932, name: "430x932" },
  { width: 568, height: 320, name: "568x320" },
  { width: 812, height: 375, name: "812x375" },
  { width: 1280, height: 800, name: "1280x800" }
];
const LANGUAGES = ["he", "en", "fr", "ru", "ar"];
const RTL_LANGUAGES = new Set(["he", "ar"]);
const TOOL_KINDS = ["plan", "view", "tour", "studio", "area", "contact", "compare"];
const OPTIONAL_TOOLS = new Set(["tour", "studio"]);
const SCREENSHOT_DIR = path.join(OUTPUT_DIR, "screenshots");

if (!SANDBOX_URL || !POST_PASSWORD) {
  const missing = [];
  if (!SANDBOX_URL) missing.push("SANDBOX_URL");
  if (!POST_PASSWORD) missing.push("SANDBOX_POST_PASSWORD");
  console.error(`Missing required environment variable(s): ${missing.join(", ")}`);
  process.exit(2);
}

let parsedSandboxUrl;
try {
  parsedSandboxUrl = new URL(SANDBOX_URL);
  if (!/^https?:$/.test(parsedSandboxUrl.protocol)) throw new Error("unsupported protocol");
  if (parsedSandboxUrl.username || parsedSandboxUrl.password) {
    throw new Error("URL userinfo is not allowed");
  }
} catch {
  console.error("SANDBOX_URL must be an absolute HTTP(S) URL.");
  process.exit(2);
}
const REPORT_TARGET_URL = `${parsedSandboxUrl.origin}${parsedSandboxUrl.pathname}`;

const startedAt = new Date();
const report = {
  schemaVersion: 1,
  runner: "scripts/qa-private-unit-journey.mjs",
  startedAt: startedAt.toISOString(),
  finishedAt: null,
  target: {
    url: REPORT_TARGET_URL,
    passwordProvided: true
  },
  environment: {
    browser: "chromium",
    emulationDisclaimer:
      "Chromium viewport/orientation emulation is not acceptance on a physical phone."
  },
  gate: null,
  privacyAfterUnlock: null,
  discovery: null,
  storageIsolation: null,
  mockedLead: null,
  sourceContract: null,
  matrix: [],
  hotspotChecks: [],
  rotation: null,
  isolation: [],
  runtime: {
    pageErrors: [],
    consoleErrors: []
  },
  hardFailures: [],
  warnings: [],
  totals: null
};

function redact(value) {
  let text = String(value == null ? "" : value);
  if (POST_PASSWORD) {
    text = text.split(POST_PASSWORD).join("[REDACTED]");
    const encodedPassword = encodeURIComponent(POST_PASSWORD);
    text = text.split(encodedPassword).join("[REDACTED]");
  }
  return text.replace(
    /([?&](?:post_password|password|token|access_token|api_key|key|nonce)=)[^&\s]+/gi,
    "$1[REDACTED]"
  );
}

function compactDetails(details) {
  if (details == null) return undefined;
  return JSON.parse(JSON.stringify(details, (_key, value) => {
    if (typeof value === "string") return redact(value);
    return value;
  }));
}

function hard(code, message, context = {}, details) {
  report.hardFailures.push({
    code,
    message: redact(message),
    context: compactDetails(context),
    details: compactDetails(details)
  });
}

function warn(code, message, context = {}, details) {
  report.warnings.push({
    code,
    message: redact(message),
    context: compactDetails(context),
    details: compactDetails(details)
  });
}

function safeError(error) {
  return redact(error && (error.stack || error.message) ? (error.stack || error.message) : error);
}

async function auditSourcePrivacyContract() {
  try {
    const source = await readFile(
      new URL("../plugins/nadlan-config/inc/showroom-engine.php", import.meta.url),
      "utf8"
    );
    const start = source.indexOf("/* A private marker without a core post password");
    const end = source.indexOf("/* Project modules enqueue globally", start);
    const failClosedBlock = start >= 0 && end > start ? source.slice(start, end) : "";
    const helperDeclared = source.includes(
      "function nadlan_unit_journey_private_lab_has_password( $post_id )"
    );
    const helperOwnsBoundary = failClosedBlock.includes(
      "nadlan_unit_journey_private_lab_has_password( $post_id )"
    );
    const frontRoleBypass = /current_user_can\s*\(|is_user_logged_in\s*\(/.test(failClosedBlock);
    const passed = helperDeclared && helperOwnsBoundary && !frontRoleBypass;
    report.sourceContract = { helperDeclared, helperOwnsBoundary, frontRoleBypass, passed };
    if (!passed) {
      hard("source.fail-closed-password", "The private-marker/missing-password front-end boundary is not role-independent.", {}, {
        helperDeclared,
        helperOwnsBoundary,
        frontRoleBypass
      });
    }
  } catch (error) {
    report.sourceContract = { passed: false };
    hard("source.contract-inspection", "The QA runner could not inspect the fail-closed password helper.", {}, {
      error: safeError(error)
    });
  }
}

async function auditLeadContextSourceContract() {
  const required = [
    "project_slug", "project_title", "project_wp_id", "direction",
    "unit_status", "consent", "consent_text", "consent_recorded"
  ];
  try {
    const [e2e, routing, conversion] = await Promise.all([
      readFile(new URL("../plugins/nadlan-config/inc/lead-e2e.php", import.meta.url), "utf8"),
      readFile(new URL("../plugins/nadlan-config/inc/lead-routing.php", import.meta.url), "utf8"),
      readFile(new URL("../plugins/nadlan-config/inc/conversion-cta.php", import.meta.url), "utf8")
    ]);
    const e2eStart = e2e.indexOf("function nadlan_lead_e2e_clean_fields");
    const e2eEnd = e2e.indexOf("function nadlan_lead_e2e_fingerprint_base", e2eStart);
    const routeStart = routing.indexOf("function nadlan_lead_route_fields");
    const routeEnd = routing.indexOf("function nadlan_lead_routing_log", routeStart);
    const e2eBlock = e2e.slice(e2eStart, e2eEnd);
    const routeBlock = routing.slice(routeStart, routeEnd);
    const missingE2e = required.filter((key) => !e2eBlock.includes(`'${key}'`));
    const missingRouting = required.filter((key) => !routeBlock.includes(`'${key}'`));
    const privateGuard = conversion.indexOf("$is_private_lab") >= 0;
    const invalidCardGuard = conversion.indexOf("$requested_card_id > 0 && $card_id <= 0") >= 0;
    const routeEmailHasUnit = routing.includes("$fields['unit']") &&
      routing.includes("$fields['project_title']");
    const fallbackEmailHasUnit = e2e.includes("$fields['unit']") &&
      e2e.includes("$fields['project_title']");
    const passed = !missingE2e.length && !missingRouting.length && privateGuard &&
      invalidCardGuard && routeEmailHasUnit && fallbackEmailHasUnit;
    report.leadSourceContract = {
      missingE2e,
      missingRouting,
      privateGuard,
      invalidCardGuard,
      routeEmailHasUnit,
      fallbackEmailHasUnit,
      passed
    };
    if (!passed) {
      hard("source.lead-context", "The lead capture/routing source contract drops private-unit context or lacks the pre-mutation privacy boundary.", {}, report.leadSourceContract);
    }
  } catch (error) {
    report.leadSourceContract = { passed: false };
    hard("source.lead-contract-inspection", "The QA runner could not inspect the lead context/privacy contract.", {}, {
      error: safeError(error)
    });
  }
}

function urlForLanguage(language = "he") {
  const url = new URL(parsedSandboxUrl.href);
  url.searchParams.delete("unit");
  url.searchParams.delete("project");
  url.searchParams.set("lang", language);
  return url.href;
}

function publicSibling(pathname) {
  return new URL(pathname, parsedSandboxUrl.origin).href;
}

async function settle(page, milliseconds = 180) {
  await page.waitForTimeout(milliseconds);
  await page.evaluate(() => new Promise((resolve) => {
    requestAnimationFrame(() => requestAnimationFrame(resolve));
  })).catch(() => {});
}

async function waitForJourney(page) {
  await page.waitForSelector("#nl-root", { state: "attached", timeout: 30_000 });
  await page.waitForFunction(() => {
    const root = document.getElementById("nl-root");
    const config = window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config;
    return Boolean(root && config && config.selected_unit_surface_v2 === true);
  }, null, { timeout: 30_000 });
}

async function auditPasswordGate(page) {
  /* A newly-created browser context proves the gate without relying on a
     password cookie left by an earlier acceptance run. Cookie values are
     never read into, or written to, the report. */
  const cookiesBefore = await page.context().cookies(parsedSandboxUrl.origin);
  const requestedAssets = [];
  const onRequest = (request) => requestedAssets.push(request.url());
  page.on("request", onRequest);

  const response = await page.goto(parsedSandboxUrl.href, {
    waitUntil: "domcontentloaded",
    timeout: 45_000
  });
  await settle(page, 250);

  const result = await page.evaluate(() => {
    const formSelector = ".post-password-form, form[action*='wp-login.php?action=postpass']";
    const forms = Array.from(document.querySelectorAll(formSelector));
    const form = forms[0] || null;
    const shell = form && (form.closest(
      ".entry-content, .wp-block-post-content, .post-content, main article"
    ) || form.parentElement);
    const remainder = shell ? shell.cloneNode(true) : null;
    if (remainder) {
      remainder.querySelectorAll(`${formSelector}, script, style, template, noscript`).forEach((node) => node.remove());
      Array.from(remainder.querySelectorAll("*")).reverse().forEach((node) => {
        if (!String(node.textContent || "").trim() &&
            !node.matches("img,svg,video,audio,iframe,input,button,select,textarea") &&
            !node.querySelector("img,svg,video,audio,iframe,input,button,select,textarea")) {
          node.remove();
        }
      });
    }
    const visible = (element) => {
      if (!element) return false;
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    };
    const projectMarkerSelector = [
      "#nl-root", ".nlpjx", ".nlptop", ".nlfb", ".nlcard", ".nl-projnotice",
      ".nl-apl", ".nlms", ".nlfc", "[data-role='unit-journey']", ".nlifp"
    ].join(",");
    const schemaTypes = Array.from(document.querySelectorAll("script[type='application/ld+json']"))
      .map((node) => String(node.textContent || ""))
      .filter((text) => /ApartmentComplex|FAQPage|BreadcrumbList|RealEstateListing/i.test(text)).length;
    return {
      passwordForm: Boolean(form),
      passwordFormCount: forms.length,
      contentShellOnlyForm: Boolean(shell && remainder &&
        !String(remainder.textContent || "").trim() && !remainder.querySelector("*")),
      headerVisible: visible(document.querySelector("header, #masthead, .site-header")),
      footerVisible: visible(document.querySelector("footer, #colophon, .site-footer")),
      sandboxBodyClass: document.body.classList.contains("nl-unit-v2-sandbox"),
      projectModuleNodes: document.querySelectorAll(projectMarkerSelector).length,
      projectSchemaBlocks: schemaTypes,
      hreflangLinks: document.querySelectorAll("link[rel='alternate'][hreflang]").length,
      canonicalLinks: document.querySelectorAll("link[rel='canonical']").length,
      leafletNodes: document.querySelectorAll("link[href*='leaflet'], script[src*='leaflet']").length,
      rootPresent: Boolean(document.getElementById("nl-root")),
      payloadPresent: Object.prototype.hasOwnProperty.call(window, "NADLAN_SHOWROOM"),
      sourceMentionsPayload: document.documentElement.innerHTML.includes("NADLAN_SHOWROOM"),
      walkthroughProviderPresent: typeof window.nadlanInitFP === "function" ||
        /nadlanInitFP|nlifp-world/.test(document.documentElement.innerHTML),
      robotsMeta: Array.from(document.querySelectorAll("meta[name='robots']"))
        .map((node) => String(node.content || "").toLowerCase())
    };
  });
  page.off("request", onRequest);

  const headers = response ? await response.allHeaders() : {};
  const xRobots = String(headers["x-robots-tag"] || "").toLowerCase();
  const referrerPolicy = String(headers["referrer-policy"] || "").toLowerCase();
  const contentTypeOptions = String(headers["x-content-type-options"] || "").toLowerCase();
  const frameOptions = String(headers["x-frame-options"] || "").toLowerCase();
  const cookiesAfter = await page.context().cookies(parsedSandboxUrl.origin);
  const cookieNamesAfter = cookiesAfter.map((cookie) => cookie.name);
  const passwordCookieBeforeUnlock = cookieNamesAfter.some((name) => /^wp-postpass_/i.test(name));
  const engineAssets = requestedAssets.filter((url) =>
    /\/showroom-engine\/(?:engine|i18n|showroom|unit-(?:surface|journey))[^/]*\.(?:js|css)(?:[?#]|$)/i.test(url)
  );
  const projectAssets = requestedAssets.filter((url) =>
    /leaflet|nadlan-pjx|feature-bar|milestones|interior-fp|walkthrough/i.test(url)
  );

  report.gate = {
    status: response ? response.status() : null,
    passwordForm: result.passwordForm,
    passwordFormCount: result.passwordFormCount,
    contentShellOnlyForm: result.contentShellOnlyForm,
    normalChromeVisible: result.headerVisible && result.footerVisible,
    sandboxBodyClass: result.sandboxBodyClass,
    projectModuleNodes: result.projectModuleNodes,
    projectSchemaBlocks: result.projectSchemaBlocks,
    hreflangLinks: result.hreflangLinks,
    canonicalLinks: result.canonicalLinks,
    leafletNodes: result.leafletNodes,
    rootPresent: result.rootPresent,
    payloadPresent: result.payloadPresent || result.sourceMentionsPayload,
    walkthroughProviderPresent: result.walkthroughProviderPresent,
    engineAssetRequests: engineAssets.length,
    projectAssetRequests: projectAssets.length,
    xRobotsTag: xRobots,
    referrerPolicy,
    contentTypeOptions,
    frameOptions,
    robotsMeta: result.robotsMeta,
    cleanContextCookieCount: cookiesBefore.length,
    cookieCountSetBeforeUnlock: cookieNamesAfter.length,
    passwordCookieBeforeUnlock,
    passed: false
  };

  if (!response || response.status() >= 400) {
    hard("gate.http", "The unauthenticated sandbox did not return a successful page.", {}, {
      status: response ? response.status() : null
    });
  }
  if (!result.passwordForm) {
    hard("gate.password-form", "The unauthenticated page did not expose the WordPress password form.");
  }
  if (result.passwordFormCount !== 1 || !result.contentShellOnlyForm) {
    hard("gate.fresh-form-only", "The locked content body was not exactly one fresh password form.", {}, {
      passwordFormCount: result.passwordFormCount,
      contentShellOnlyForm: result.contentShellOnlyForm
    });
  }
  if (!result.headerVisible || !result.footerVisible || result.sandboxBodyClass) {
    hard("gate.trustworthy-shell", "The locked page did not retain normal site chrome around the password gate.", {}, {
      headerVisible: result.headerVisible,
      footerVisible: result.footerVisible,
      sandboxBodyClass: result.sandboxBodyClass
    });
  }
  if (result.rootPresent) {
    hard("gate.root-leak", "#nl-root was present before the post password was accepted.");
  }
  if (result.payloadPresent || result.sourceMentionsPayload) {
    hard("gate.payload-leak", "The showroom payload was exposed before authentication.");
  }
  if (engineAssets.length) {
    hard("gate.engine-asset-leak", "Showroom engine assets were requested before authentication.", {}, {
      count: engineAssets.length,
      assetPaths: engineAssets.map((item) => {
        const url = new URL(item);
        return `${url.origin}${url.pathname}`;
      })
    });
  }
  if (projectAssets.length || result.projectModuleNodes || result.projectSchemaBlocks ||
      result.hreflangLinks || result.canonicalLinks || result.leafletNodes) {
    hard("gate.project-module-leak", "Project modules, structured data or map assets leaked into the locked page.", {}, {
      projectAssetRequests: projectAssets.length,
      projectModuleNodes: result.projectModuleNodes,
      projectSchemaBlocks: result.projectSchemaBlocks,
      hreflangLinks: result.hreflangLinks,
      canonicalLinks: result.canonicalLinks,
      leafletNodes: result.leafletNodes
    });
  }
  if (result.walkthroughProviderPresent) {
    hard("gate.walkthrough-provider-leak", "The schematic Tour provider was emitted before password unlock.");
  }
  if (!xRobots.includes("noindex")) {
    hard("gate.x-robots", "The unauthenticated response was missing X-Robots-Tag: noindex.", {}, {
      xRobotsTag: xRobots
    });
  }
  if (referrerPolicy !== "no-referrer") {
    hard("gate.referrer-policy", "The private password response was missing Referrer-Policy: no-referrer.", {}, {
      referrerPolicy
    });
  }
  if (contentTypeOptions !== "nosniff" || frameOptions !== "sameorigin") {
    hard("gate.response-hardening", "The private password response lost its MIME/frame response guards.", {}, {
      contentTypeOptions,
      frameOptions
    });
  }
  if (!result.robotsMeta.some((content) => content.includes("noindex"))) {
    hard("gate.robots-meta", "The unauthenticated password page was missing robots meta noindex.", {}, {
      robotsMeta: result.robotsMeta
    });
  }
  if (cookiesBefore.length) {
    hard("gate.dirty-context", "The password gate was not tested from a cookie-free browser context.", {}, {
      cookieCount: cookiesBefore.length
    });
  }
  if (passwordCookieBeforeUnlock) {
    hard("gate.password-cookie", "A WordPress post-password cookie existed before the unlock action.");
  }

  report.gate.passed = !report.hardFailures.some((item) => item.code.startsWith("gate."));
}

async function auditUnlockedPrivacy(page, response) {
  const headers = response ? await response.allHeaders() : {};
  const xRobotsTag = String(headers["x-robots-tag"] || "").toLowerCase();
  const referrerPolicy = String(headers["referrer-policy"] || "").toLowerCase();
  const state = await page.evaluate(() => ({
    robotsMeta: Array.from(document.querySelectorAll("meta[name='robots']"))
      .map((node) => String(node.content || "").toLowerCase()),
    payloadPresent: Boolean(window.NADLAN_SHOWROOM && document.getElementById("nl-root")),
    privateLabConfig: Boolean(window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config &&
      window.NADLAN_SHOWROOM.config.private_unit_journey_lab === true),
    projectModuleNodes: document.querySelectorAll(
      ".nlpjx, .nlptop, .nlfb, .nlcard, .nl-projnotice, .nl-apl, .nlms, .nlfc"
    ).length,
    projectSchemaBlocks: Array.from(document.querySelectorAll("script[type='application/ld+json']"))
      .map((node) => String(node.textContent || ""))
      .filter((text) => /ApartmentComplex|FAQPage|BreadcrumbList|RealEstateListing/i.test(text)).length,
    hreflangLinks: document.querySelectorAll("link[rel='alternate'][hreflang]").length,
    canonicalLinks: document.querySelectorAll("link[rel='canonical']").length,
    leafletNodes: document.querySelectorAll("link[href*='leaflet'], script[src*='leaflet']").length
  }));
  const cookieNames = (await page.context().cookies(parsedSandboxUrl.origin))
    .map((cookie) => cookie.name);
  const postPasswordCookie = cookieNames.some((name) => /^wp-postpass_/i.test(name));
  report.privacyAfterUnlock = {
    status: response ? response.status() : null,
    xRobotsTag,
    referrerPolicy,
    robotsMeta: state.robotsMeta,
    protectedPayloadAvailableAfterUnlock: state.payloadPresent,
    privateLabConfig: state.privateLabConfig,
    projectModuleNodes: state.projectModuleNodes,
    projectSchemaBlocks: state.projectSchemaBlocks,
    hreflangLinks: state.hreflangLinks,
    canonicalLinks: state.canonicalLinks,
    leafletNodes: state.leafletNodes,
    postPasswordCookiePresent: postPasswordCookie,
    cookieCount: cookieNames.length,
    passed: false
  };

  if (!xRobotsTag.includes("noindex")) {
    hard("privacy.unlocked-x-robots", "The unlocked private page lost X-Robots-Tag: noindex.");
  }
  if (referrerPolicy !== "no-referrer") {
    hard("privacy.unlocked-referrer-policy", "The unlocked private page lost Referrer-Policy: no-referrer.");
  }
  if (!state.robotsMeta.some((content) => content.includes("noindex"))) {
    hard("privacy.unlocked-robots-meta", "The unlocked private page lost robots meta noindex.", {}, {
      robotsMeta: state.robotsMeta
    });
  }
  if (!state.payloadPresent) {
    hard("privacy.unlocked-payload", "The protected showroom payload was unavailable after valid unlock.");
  }
  if (!state.privateLabConfig) {
    hard("privacy.private-config", "The unlocked payload is missing the dedicated private lab flag.");
  }
  if (state.projectModuleNodes || state.projectSchemaBlocks || state.hreflangLinks ||
      state.canonicalLinks || state.leafletNodes) {
    hard("privacy.unlocked-module-leak", "The unlocked focused lab retained public project modules, schema, hreflang or Leaflet.", {}, {
      projectModuleNodes: state.projectModuleNodes,
      projectSchemaBlocks: state.projectSchemaBlocks,
      hreflangLinks: state.hreflangLinks,
      canonicalLinks: state.canonicalLinks,
      leafletNodes: state.leafletNodes
    });
  }
  if (!postPasswordCookie) {
    hard("privacy.unlock-cookie", "WordPress did not retain the successful post-password unlock in its expected cookie.");
  }
  report.privacyAfterUnlock.passed = xRobotsTag.includes("noindex") && referrerPolicy === "no-referrer" &&
    state.robotsMeta.some((content) => content.includes("noindex")) &&
    state.payloadPresent && state.privateLabConfig && postPasswordCookie &&
    state.projectModuleNodes === 0 && state.projectSchemaBlocks === 0 &&
    state.hreflangLinks === 0 && state.canonicalLinks === 0 && state.leafletNodes === 0;
}

async function auditPostUnlockCacheGate(browserInstance) {
  /* The unlocked response has now crossed the live cache stack. Re-enter from
     a brand-new cookie jar both at the canonical URL and at a cache-busted URL
     to prove that no personalized payload was cached for anonymous visitors. */
  const clean = await browserInstance.newContext({
    viewport: { width: 375, height: 812 },
    locale: "he-IL"
  });
  const cleanPage = await clean.newPage();
  const assetRequests = [];
  cleanPage.on("request", (request) => {
    if (/\/showroom-engine\/(?:engine|i18n|showroom|unit-(?:surface|journey))[^/]*\.(?:js|css)(?:[?#]|$)/i.test(request.url())) {
      assetRequests.push(request.url());
    }
  });
  const cacheBusted = new URL(parsedSandboxUrl.href);
  cacheBusted.searchParams.set("nlqa_private_cache", Date.now().toString(36));
  const checks = [];
  try {
    for (const [label, url] of [
      ["canonical", parsedSandboxUrl.href],
      ["cache-busted", cacheBusted.href]
    ]) {
      const beforeAssets = assetRequests.length;
      let response = null;
      let error = null;
      try {
        response = await cleanPage.goto(url, {
          waitUntil: "domcontentloaded",
          timeout: 45_000
        });
        await settle(cleanPage, 180);
      } catch (caught) {
        error = safeError(caught);
      }
      const state = await cleanPage.evaluate(() => ({
        passwordForms: document.querySelectorAll(
          ".post-password-form, form[action*='wp-login.php?action=postpass']"
        ).length,
        root: Boolean(document.getElementById("nl-root")),
        payload: Object.prototype.hasOwnProperty.call(window, "NADLAN_SHOWROOM") ||
          document.documentElement.innerHTML.includes("NADLAN_SHOWROOM"),
        projectModules: document.querySelectorAll(
          ".nlpjx, .nlptop, .nlfb, .nlcard, .nl-projnotice, .nl-apl, .nlms, .nlfc, .nlifp"
        ).length
      })).catch(() => ({ passwordForms: 0, root: true, payload: true, projectModules: -1 }));
      const headers = response ? await response.allHeaders() : {};
      const cacheControl = String(headers["cache-control"] || "").toLowerCase();
      const xRobots = String(headers["x-robots-tag"] || "").toLowerCase();
      const newAssets = assetRequests.length - beforeAssets;
      const passed = !error && response && response.status() === 200 &&
        state.passwordForms === 1 && !state.root && !state.payload &&
        state.projectModules === 0 && newAssets === 0 &&
        xRobots.includes("noindex") &&
        (cacheControl.includes("no-cache") || cacheControl.includes("no-store") ||
          cacheControl.includes("max-age=0"));
      const result = {
        label,
        status: response ? response.status() : null,
        passwordForms: state.passwordForms,
        root: state.root,
        payload: state.payload,
        projectModules: state.projectModules,
        engineAssetRequests: newAssets,
        xRobots,
        cacheControl,
        passed
      };
      checks.push(result);
      if (!passed) {
        hard("privacy.post-unlock-cache", `The clean ${label} request received an unlocked or cacheable private response after warm-up.`, {
          probe: label
        }, { ...result, error });
      }
    }
  } finally {
    await clean.close().catch(() => {});
  }
  report.postUnlockCacheGate = {
    cleanContext: true,
    checks,
    passed: checks.length === 2 && checks.every((item) => item.passed)
  };
}

async function unlockSandbox(page) {
  const form = page.locator(
    ".post-password-form, form[action*='wp-login.php?action=postpass']"
  ).first();
  const passwordInput = form.locator("input[name='post_password']");
  await passwordInput.fill(POST_PASSWORD);

  const submit = form.locator("input[type='submit'], button[type='submit']").first();
  await Promise.all([
    page.waitForNavigation({ waitUntil: "domcontentloaded", timeout: 45_000 }).catch(() => null),
    submit.click()
  ]);
  await waitForJourney(page);
  await settle(page, 250);

  const unlocked = await page.evaluate(() => ({
    protectedFormStillPresent: Boolean(document.querySelector(".post-password-form")),
    bodyClass: document.body.className,
    enabled: Boolean(
      window.NADLAN_SHOWROOM &&
      window.NADLAN_SHOWROOM.config &&
      window.NADLAN_SHOWROOM.config.selected_unit_surface_v2 === true
    ),
    privateLab: Boolean(
      window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config &&
      window.NADLAN_SHOWROOM.config.private_unit_journey_lab === true
    )
  }));

  if (unlocked.protectedFormStillPresent || !unlocked.enabled || !unlocked.privateLab) {
    hard("unlock.failed", "The sandbox did not unlock into the v2 journey.");
    throw new Error("Sandbox password unlock failed");
  }
  if (!unlocked.bodyClass.split(/\s+/).includes("nl-unit-v2-sandbox")) {
    hard("unlock.body-class", "The private sandbox body is missing nl-unit-v2-sandbox.");
  }
}

async function privateTargetContext(page) {
  return page.evaluate(() => {
    const payload = window.NADLAN_SHOWROOM || {};
    const key = payload.config && payload.config.default_project;
    const project = key && payload.projects ? payload.projects[key] : null;
    const firstUnit = project && Array.isArray(project.units) ? project.units[0] : null;
    return project ? {
      wpId: Number(project.wp_id) || 0,
      slug: String(project.slug || key || ""),
      title: String(project.name || ""),
      url: String(project.url || location.href),
      unitId: firstUnit ? String(firstUnit.id || "") : ""
    } : null;
  });
}

async function auditAnonymousDiscovery(browserInstance, target) {
  if (!target || !target.wpId || !target.slug) {
    hard("discovery.target-context", "The unlocked payload did not expose enough in-memory context for anonymous discovery probes.");
    return;
  }

  const anonymous = await browserInstance.newContext({ locale: "he-IL" });
  const checks = [];
  const query = encodeURIComponent(target.title || target.slug);
  const targetUrl = new URL(target.url || parsedSandboxUrl.href, parsedSandboxUrl.origin).href;
  const directFeedUrl = new URL(targetUrl);
  directFeedUrl.pathname = `${directFeedUrl.pathname.replace(/\/$/, "")}/feed/`;
  directFeedUrl.search = "";
  directFeedUrl.hash = "";
  const endpoints = [
    { label: "core-rest-search", url: `/wp-json/wp/v2/search?search=${query}&subtype=nadlan_project`, status: 200 },
    { label: "project-rest-collection", url: `/wp-json/wp/v2/nadlan_project?search=${query}`, status: 200 },
    { label: "project-rest-direct", url: `/wp-json/wp/v2/nadlan_project/${target.wpId}`, status: 404 },
    { label: "custom-project-search", url: `/wp-json/nadlan/v1/projects?q=${query}`, status: 200 },
    { label: "autocomplete-project-search", url: `/wp-json/nadlan/v1/suggest?type=project&q=${query}`, status: 200 },
    /* Two sequential aggregate probes catch both a poisoned/pre-existing
       response and the endpoint's normal cache-hit path. */
    { label: "project-map-cache-pass-1", url: "/wp-json/nadlan/v1/project-map", status: 200 },
    { label: "project-map-cache-pass-2", url: "/wp-json/nadlan/v1/project-map", status: 200 },
    { label: "matcher-data-cache-pass-1", url: "/wp-json/nadlan/v1/matcher-data", status: 200 },
    { label: "matcher-data-cache-pass-2", url: "/wp-json/nadlan/v1/matcher-data", status: 200 },
    { label: "comps", url: `/wp-json/nadlan/v1/comps?id=${target.wpId}`, status: 404 },
    { label: "appointment-slots", url: `/wp-json/nadlan/v1/appt-slots?card=${target.wpId}`, status: 404, jsonCode: "not_found" },
    { label: "brochure", url: `/wp-json/nadlan/v1/brochure?p=${target.wpId}&u=${encodeURIComponent(target.unitId)}`, status: 404 },
    { label: "og-image", url: `/wp-json/nadlan/v1/og/${target.wpId}.svg`, status: 404 },
    { label: "oembed", url: `/wp-json/oembed/1.0/embed?url=${encodeURIComponent(targetUrl)}`, status: 404 },
    { label: "project-archive", url: "/projects/", statuses: [200] },
    { label: "site-search", url: `/?s=${query}&post_type=nadlan_project`, statuses: [200] },
    { label: "home", url: "/", statuses: [200] },
    { label: "project-feed", url: "/?post_type=nadlan_project&feed=rss2", statuses: [200] },
    { label: "private-direct-feed", url: directFeedUrl.href, status: 404 },
    { label: "private-query-feed", url: `/?feed=rss2&post_type=nadlan_project&p=${target.wpId}`, status: 404 },
    { label: "core-project-sitemap", url: "/wp-sitemap-posts-nadlan_project-1.xml", statuses: [200, 404], feasible: true },
    { label: "yoast-project-sitemap", url: "/nadlan_project-sitemap.xml", statuses: [200, 404], feasible: true }
  ];

  try {
    for (const endpoint of endpoints) {
      let response;
      let body = "";
      let error = null;
      try {
        response = await anonymous.request.get(new URL(endpoint.url, parsedSandboxUrl.origin).href, {
          timeout: 30_000,
          maxRedirects: 5
        });
        body = await response.text();
      } catch (caught) {
        error = safeError(caught);
      }
      const status = response ? response.status() : null;
      const normalized = body.toLowerCase();
      let responseJson = null;
      try { responseJson = body ? JSON.parse(body) : null; } catch {}
      const exposed = Boolean(
        target.slug && normalized.includes(target.slug.toLowerCase()) ||
        new URL(targetUrl).pathname !== "/" && normalized.includes(new URL(targetUrl).pathname.toLowerCase())
      );
      const accepted = endpoint.status != null
        ? status === endpoint.status
        : (endpoint.statuses || []).includes(status);
      const guardCodeMatched = !endpoint.jsonCode || Boolean(
        responseJson && responseJson.code === endpoint.jsonCode
      );
      const passed = !error && accepted && guardCodeMatched && !exposed;
      checks.push({
        label: endpoint.label,
        status,
        identityExposed: exposed,
        guardCodeMatched,
        feasible: Boolean(endpoint.feasible),
        passed
      });
      if (endpoint.feasible && status === 404 && !exposed) {
        warn("discovery.sitemap-unavailable", `${endpoint.label} is not installed at its conventional path; exclusion could not be inspected there.`, {
          endpoint: endpoint.label
        });
      } else if (!passed) {
        hard("discovery.exposure", `Anonymous ${endpoint.label} did not satisfy its private-lab visibility contract.`, {
          endpoint: endpoint.label
        }, { status, identityExposed: exposed, guardCodeMatched, error });
      }
    }

    /* Minimal body deliberately omits `unit`: if the private guard regresses,
       the server's post-guard validation returns 400 before any RFP row can be
       created. A correct boundary wins first with the opaque 404. */
    let rfpResponse;
    let rfpBody = "";
    let rfpError = null;
    try {
      rfpResponse = await anonymous.request.post(
        new URL("/wp-json/nadlan/v1/rfp", parsedSandboxUrl.origin).href,
        { data: { project: target.slug }, timeout: 30_000, maxRedirects: 0 }
      );
      rfpBody = await rfpResponse.text();
    } catch (caught) {
      rfpError = safeError(caught);
    }
    let rfpJson = null;
    try { rfpJson = rfpBody ? JSON.parse(rfpBody) : null; } catch {}
    const rfpStatus = rfpResponse ? rfpResponse.status() : null;
    const rfpIdentityExposed = Boolean(
      target.slug && rfpBody.toLowerCase().includes(target.slug.toLowerCase()) ||
      new URL(targetUrl).pathname !== "/" &&
        rfpBody.toLowerCase().includes(new URL(targetUrl).pathname.toLowerCase())
    );
    const rfpTokenIssued = Boolean(
      rfpJson && typeof rfpJson === "object" &&
      (rfpJson.token || rfpJson.url || (rfpJson.data && (rfpJson.data.token || rfpJson.data.url)))
    );
    const rfpGuardCodeMatched = Boolean(rfpJson && rfpJson.code === "not_found");
    const rfpPassed = !rfpError && rfpStatus === 404 && rfpGuardCodeMatched &&
      !rfpIdentityExposed && !rfpTokenIssued;
    checks.push({
      label: "rfp-private-guard",
      status: rfpStatus,
      identityExposed: rfpIdentityExposed,
      tokenIssued: rfpTokenIssued,
      mutationProofInput: true,
      passed: rfpPassed
    });
    if (!rfpPassed) {
      hard("discovery.rfp-guard", "The mutation-proof private RFP probe did not receive the endpoint's opaque pre-mutation 404.", {
        endpoint: "rfp-private-guard"
      }, {
        status: rfpStatus,
        guardCodeMatched: rfpGuardCodeMatched,
        identityExposed: rfpIdentityExposed,
        tokenIssued: rfpTokenIssued,
        error: rfpError
      });
    }

    /* The honeypot makes this probe mutation-proof if the privacy guard ever
       disappears: the legacy path returns a fake success without inserting a
       lead.  The correct ordering rejects the private card first with 404. */
    let leadResponse;
    let leadBody = "";
    let leadError = null;
    try {
      leadResponse = await anonymous.request.post(
        new URL("/wp-json/nadlan/v1/lead", parsedSandboxUrl.origin).href,
        {
          data: {
            card_id: target.wpId,
            name: "QA privacy probe",
            company: "qa-privacy-probe"
          },
          timeout: 30_000,
          maxRedirects: 0
        }
      );
      leadBody = await leadResponse.text();
    } catch (caught) {
      leadError = safeError(caught);
    }
    let leadJson = null;
    try { leadJson = leadBody ? JSON.parse(leadBody) : null; } catch {}
    const leadStatus = leadResponse ? leadResponse.status() : null;
    const leadGuardCodeMatched = Boolean(leadJson && leadJson.code === "not_found");
    let invalidLeadResponse;
    let invalidLeadBody = "";
    let invalidLeadError = null;
    try {
      invalidLeadResponse = await anonymous.request.post(
        new URL("/wp-json/nadlan/v1/lead", parsedSandboxUrl.origin).href,
        {
          data: {
            card_id: 2147483000,
            name: "QA privacy control",
            company: "qa-privacy-probe"
          },
          timeout: 30_000,
          maxRedirects: 0
        }
      );
      invalidLeadBody = await invalidLeadResponse.text();
    } catch (caught) {
      invalidLeadError = safeError(caught);
    }
    let invalidLeadJson = null;
    try { invalidLeadJson = invalidLeadBody ? JSON.parse(invalidLeadBody) : null; } catch {}
    const invalidLeadStatus = invalidLeadResponse ? invalidLeadResponse.status() : null;
    const invalidLeadGuardCodeMatched = Boolean(
      invalidLeadJson && invalidLeadJson.code === "not_found"
    );
    const differentialOpaque = leadStatus === invalidLeadStatus &&
      leadGuardCodeMatched === invalidLeadGuardCodeMatched;
    const leadPassed = !leadError && !invalidLeadError && leadStatus === 404 &&
      leadGuardCodeMatched && invalidLeadStatus === 404 &&
      invalidLeadGuardCodeMatched && differentialOpaque;
    checks.push({
      label: "lead-private-password-guard",
      status: leadStatus,
      guardCodeMatched: leadGuardCodeMatched,
      invalidControlStatus: invalidLeadStatus,
      differentialOpaque,
      mutationProofInput: true,
      passed: leadPassed
    });
    if (!leadPassed) {
      hard("discovery.lead-guard", "The mutation-proof anonymous lead probe did not receive the private card's pre-mutation 404.", {
        endpoint: "lead-private-password-guard"
      }, {
        status: leadStatus,
        guardCodeMatched: leadGuardCodeMatched,
        invalidControlStatus: invalidLeadStatus,
        invalidControlCodeMatched: invalidLeadGuardCodeMatched,
        differentialOpaque,
        error: leadError || invalidLeadError
      });
    }
  } finally {
    await anonymous.close().catch(() => {});
  }

  report.discovery = {
    cleanContext: true,
    checks,
    passed: checks.every((item) => item.passed || (item.feasible && item.status === 404 && !item.identityExposed))
  };
}

async function auditUnlockedLeadCookieBridge(page, target) {
  if (!target || !target.wpId) {
    hard("contact.cookie-bridge-context", "The unlocked lead-cookie probe has no private project ID.");
    return;
  }
  const result = await page.evaluate(async ({ wpId }) => {
    const config = window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config;
    const endpoint = config && config.lead_endpoint;
    if (!endpoint) return { status: null, authorizedPastGuard: false, endpointPresent: false };
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
          card_id: wpId,
          name: "QA unlocked cookie probe",
          company: "qa-privacy-probe"
        })
      });
      let data = null;
      try { data = await response.json(); } catch {}
      return {
        status: response.status,
        code: data && typeof data.code === "string" ? data.code : null,
        /* The non-empty honeypot must stop the request after the password
           boundary and before rate counters, inserts or notifications. A 400
           spam response therefore proves the cookie crossed the private-card
           guard without mutating production data. */
        authorizedPastGuard: Boolean(
          response.status === 400 && data && data.code === "spam"
        ),
        endpointPresent: true
      };
    } catch (error) {
      return {
        status: null,
        authorizedPastGuard: false,
        endpointPresent: true,
        error: String(error)
      };
    }
  }, { wpId: target.wpId });
  report.unlockedLeadCookieBridge = {
    ...result,
    mutationProofInput: true,
    passed: result.authorizedPastGuard
  };
  if (!result.authorizedPastGuard) {
    hard("contact.cookie-bridge", "The unlocked page's wp-postpass cookie did not pass the private-card guard before the mutation-proof honeypot rejection.", {}, result);
  }
}

async function auditPrivateStorageIsolation(page) {
  const localRecentSentinel = '{"sentinel":"qa-local-recent"}';
  const localFavsSentinel = '["qa-local-favorite-sentinel"]';
  await page.evaluate(({ recent, favs }) => {
    localStorage.setItem("nl_recent", recent);
    localStorage.setItem("nl_favs", favs);
    sessionStorage.removeItem("nl_recent");
    sessionStorage.removeItem("nl_favs");
  }, { recent: localRecentSentinel, favs: localFavsSentinel });

  await page.goto(urlForLanguage("he"), { waitUntil: "domcontentloaded", timeout: 45_000 });
  await waitForJourney(page);
  const selectedId = await selectFirstInventoryUnit(page, "click", {
    probe: "private-storage-isolation"
  });
  const save = page.locator(`.nl-unit-screen--v2 [data-act="fav"][data-id="${selectedId}"]`).first();
  if (!(await save.count())) {
    hard("storage.save-control", "The selected scene did not expose its Save quick action.");
    report.storageIsolation = { passed: false };
    return;
  }
  await save.focus();
  await save.press("Enter");
  await settle(page, 220);

  const state = await page.evaluate(({ expectedRecent, expectedFavs, unitId }) => {
    let recent = [];
    let favs = [];
    try { recent = JSON.parse(sessionStorage.getItem("nl_recent") || "[]"); } catch {}
    try { favs = JSON.parse(sessionStorage.getItem("nl_favs") || "[]"); } catch {}
    const active = document.activeElement;
    return {
      localRecentUnchanged: localStorage.getItem("nl_recent") === expectedRecent,
      localFavsUnchanged: localStorage.getItem("nl_favs") === expectedFavs,
      sessionRecentHasSelection: Array.isArray(recent) && recent.some((item) => item && String(item.u) === unitId),
      sessionFavsHasSelection: Array.isArray(favs) && favs.some((item) => String(item) === unitId),
      saveFocusPersisted: Boolean(active && active.matches &&
        active.matches(`[data-act="fav"][data-id="${CSS.escape(unitId)}"]`)),
      compareControls: document.querySelectorAll(
        ".nl-unit-screen--v2 [data-act='unit-tool'][data-tool='compare']"
      ).length
    };
  }, { expectedRecent: localRecentSentinel, expectedFavs: localFavsSentinel, unitId: String(selectedId) });

  const passed = state.localRecentUnchanged && state.localFavsUnchanged &&
    state.sessionRecentHasSelection && state.sessionFavsHasSelection &&
    state.saveFocusPersisted && state.compareControls === 1;
  report.storageIsolation = { ...state, passed };
  if (!state.localRecentUnchanged || !state.localFavsUnchanged) {
    hard("storage.local-mutation", "The private lab mutated public localStorage state.");
  }
  if (!state.sessionRecentHasSelection || !state.sessionFavsHasSelection) {
    hard("storage.session-missing", "Private selection/Save state was not retained in sessionStorage.");
  }
  if (!state.saveFocusPersisted) {
    hard("storage.save-focus", "Save re-rendering did not preserve keyboard focus.");
  }
  if (state.compareControls !== 1) {
    hard("scene.compare-control", "The private v2 scene does not expose exactly one Compare action.", {}, {
      compareControls: state.compareControls
    });
  }
}

async function setLanguageThroughUi(page, language, context) {
  const buttons = page.locator(".nl-lang");
  const ids = await buttons.evaluateAll((nodes) => nodes.map((node) => node.dataset.id));
  const uniqueIds = [...new Set(ids)];
  const expected = [...LANGUAGES].sort();
  const actual = [...uniqueIds].sort();
  const fiveLanguages = JSON.stringify(actual) === JSON.stringify(expected) && ids.length === 5;

  if (!fiveLanguages) {
    hard("language.buttons", "The v2 language control does not expose exactly five unique languages.", context, {
      count: ids.length,
      ids
    });
  }

  const target = page.locator(`.nl-lang[data-id="${language}"]`).first();
  if (await target.count()) {
    await target.click();
    await page.waitForFunction((expectedLanguage) => {
      return document.documentElement.lang.toLowerCase().split("-")[0] === expectedLanguage;
    }, language, { timeout: 10_000 }).catch(() => {});
    await settle(page, 100);
  } else {
    hard("language.target-missing", `Language button ${language} is missing.`, context);
  }

  const state = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    dir: document.documentElement.dir,
    pressed: Array.from(document.querySelectorAll(".nl-lang[aria-pressed='true']"))
      .map((node) => node.dataset.id)
  }));
  const normalizedLang = state.lang.toLowerCase().split("-")[0];
  const expectedDir = RTL_LANGUAGES.has(language) ? "rtl" : "ltr";

  if (normalizedLang !== language) {
    hard("language.html-lang", `html[lang] did not switch to ${language}.`, context, state);
  }
  if (state.dir !== expectedDir) {
    hard("language.html-dir", `html[dir] should be ${expectedDir} for ${language}.`, context, state);
  }
  if (state.pressed.length !== 1 || state.pressed[0] !== language) {
    hard("language.pressed-state", `The active language state is not unique for ${language}.`, context, state);
  }

  return {
    buttonCount: ids.length,
    buttonIds: ids,
    htmlLang: state.lang,
    htmlDir: state.dir,
    activeButtons: state.pressed,
    passed: fiveLanguages && normalizedLang === language && state.dir === expectedDir &&
      state.pressed.length === 1 && state.pressed[0] === language
  };
}

async function selectFirstInventoryUnit(page, method, context) {
  const button = page.locator(".nl-invgrid .nl-ucard__select").first();
  if (!(await button.count())) {
    hard("selection.inventory-missing", "No real inventory selection button was found.", context);
    throw new Error("Inventory selection button missing");
  }

  const unitId = await button.getAttribute("data-id");
  await button.scrollIntoViewIfNeeded();
  if (method === "click") {
    await button.click();
  } else {
    await button.focus();
    await button.press(method === "space" ? "Space" : "Enter");
  }

  await page.waitForSelector(".nl-theater--unit-v2 .nl-unit-screen--v2", {
    state: "attached",
    timeout: 15_000
  });
  await page.waitForFunction(() => document.body.classList.contains("nl-unit-v2-active"), null, {
    timeout: 15_000
  });
  await settle(page, 650);
  return unitId;
}

async function sceneMeasurements(page) {
  return page.evaluate(() => {
    const viewport = { width: window.innerWidth, height: window.innerHeight };
    const theater = document.querySelector(".nl-theater--unit-v2");
    const screen = document.querySelector(".nl-unit-screen--v2");
    const title = document.getElementById("nl-selected-unit-title");
    const essentialSelectors = [
      ["model", ".nl-theater--unit-v2 > .nl-stagewrap"],
      ["head", ".nl-unit-journey__head"],
      ["beam", ".nl-unit-journey__beam"],
      ["facts", ".nl-unit-journey__facts"],
      ["doors", ".nl-unit-journey__doors"]
    ];

    function rectFor(element) {
      if (!element) return null;
      const rect = element.getBoundingClientRect();
      return {
        x: Number(rect.x.toFixed(2)),
        y: Number(rect.y.toFixed(2)),
        top: Number(rect.top.toFixed(2)),
        right: Number(rect.right.toFixed(2)),
        bottom: Number(rect.bottom.toFixed(2)),
        left: Number(rect.left.toFixed(2)),
        width: Number(rect.width.toFixed(2)),
        height: Number(rect.height.toFixed(2))
      };
    }

    function visible(element) {
      if (!element) return false;
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return !element.hidden && style.display !== "none" && style.visibility !== "hidden" &&
        Number(style.opacity) !== 0 && rect.width > 0 && rect.height > 0;
    }

    function intersection(a, b) {
      if (!a || !b) return null;
      const width = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const height = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (width <= 2 || height <= 2) return null;
      return { width: Number(width.toFixed(2)), height: Number(height.toFixed(2)) };
    }

    function visibleRatio(rect) {
      if (!rect || rect.width <= 0 || rect.height <= 0) return 0;
      const width = Math.max(0, Math.min(rect.right, viewport.width) - Math.max(rect.left, 0));
      const height = Math.max(0, Math.min(rect.bottom, viewport.height) - Math.max(rect.top, 0));
      return Number(((width * height) / (rect.width * rect.height)).toFixed(4));
    }

    function parseRgb(value) {
      const match = String(value).match(/rgba?\(([^)]+)\)/i);
      if (!match) return null;
      const parts = match[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
      if (parts.length < 3 || parts.slice(0, 3).some((part) => !Number.isFinite(part))) return null;
      return { r: parts[0], g: parts[1], b: parts[2], a: Number.isFinite(parts[3]) ? parts[3] : 1 };
    }

    function composite(foreground, background) {
      const alpha = foreground.a + background.a * (1 - foreground.a);
      if (!alpha) return { r: 255, g: 255, b: 255, a: 1 };
      return {
        r: (foreground.r * foreground.a + background.r * background.a * (1 - foreground.a)) / alpha,
        g: (foreground.g * foreground.a + background.g * background.a * (1 - foreground.a)) / alpha,
        b: (foreground.b * foreground.a + background.b * background.a * (1 - foreground.a)) / alpha,
        a: alpha
      };
    }

    function effectiveBackground(element) {
      const layers = [];
      let node = element;
      while (node && node.nodeType === Node.ELEMENT_NODE) {
        const color = parseRgb(getComputedStyle(node).backgroundColor);
        if (color && color.a > 0) layers.push(color);
        node = node.parentElement;
      }
      let output = { r: 255, g: 255, b: 255, a: 1 };
      for (let index = layers.length - 1; index >= 0; index -= 1) {
        output = composite(layers[index], output);
      }
      return output;
    }

    function luminance(color) {
      const values = [color.r, color.g, color.b].map((channel) => {
        const value = channel / 255;
        return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
      });
      return values[0] * 0.2126 + values[1] * 0.7152 + values[2] * 0.0722;
    }

    function contrast(element) {
      if (!element) return null;
      const foreground = parseRgb(getComputedStyle(element).color);
      const background = effectiveBackground(element);
      if (!foreground || !background) return null;
      const fg = luminance(foreground);
      const bg = luminance(background);
      return Number(((Math.max(fg, bg) + 0.05) / (Math.min(fg, bg) + 0.05)).toFixed(2));
    }

    function scanOverflow(root) {
      if (!root) return { scrollers: [], clipped: [] };
      const scrollers = [];
      const clipped = [];
      const elements = [root, ...root.querySelectorAll("*")];
      for (const element of elements) {
        if (element.matches("textarea, select, option, canvas, model-viewer, .mapboxgl-map, .mapboxgl-canvas-container") ||
            element.closest(".mapboxgl-control-container")) continue;
        if (!visible(element)) continue;
        const extra = element.scrollHeight - element.clientHeight;
        if (extra <= 3) continue;
        const overflowY = getComputedStyle(element).overflowY;
        const item = {
          tag: element.tagName.toLowerCase(),
          id: element.id || null,
          className: typeof element.className === "string" ? element.className.slice(0, 180) : "",
          clientHeight: element.clientHeight,
          scrollHeight: element.scrollHeight,
          overflowY
        };
        if (/auto|scroll/.test(overflowY)) scrollers.push(item);
        if (/hidden|clip/.test(overflowY)) clipped.push(item);
      }
      return { scrollers, clipped };
    }

    const regions = essentialSelectors.map(([name, selector]) => {
      const element = document.querySelector(selector);
      return { name, rect: rectFor(element), visible: visible(element) };
    });
    const overlaps = [];
    for (let first = 0; first < regions.length; first += 1) {
      for (let second = first + 1; second < regions.length; second += 1) {
        if (!regions[first].visible || !regions[second].visible) continue;
        const overlap = intersection(regions[first].rect, regions[second].rect);
        if (overlap) overlaps.push({
          first: regions[first].name,
          second: regions[second].name,
          ...overlap
        });
      }
    }

    const obstructionSelectors = ["#nl-sticky", ".nl-sticky", "#nla11y-btn"];
    const obstructions = [];
    for (const selector of obstructionSelectors) {
      for (const element of document.querySelectorAll(selector)) {
        if (!visible(element)) continue;
        const obstructionRect = rectFor(element);
        for (const region of regions.filter((item) => ["beam", "facts", "doors"].includes(item.name))) {
          const overlap = intersection(obstructionRect, region.rect);
          if (overlap) obstructions.push({ selector, region: region.name, ...overlap });
        }
      }
    }

    const idCounts = {};
    for (const element of document.querySelectorAll("[id]")) {
      idCounts[element.id] = (idCounts[element.id] || 0) + 1;
    }
    const duplicateIds = Object.entries(idCounts)
      .filter(([, count]) => count > 1)
      .map(([id, count]) => ({ id, count }));

    const theaterRect = rectFor(theater);
    const overflow = scanOverflow(theater);
    const titleStyle = title ? getComputedStyle(title) : null;
    const titleFontSize = titleStyle ? parseFloat(titleStyle.fontSize) : null;
    const titleFontWeight = titleStyle ? Number(titleStyle.fontWeight) || 400 : null;
    const titleLarge = titleFontSize != null &&
      (titleFontSize >= 24 || (titleFontSize >= 18.66 && titleFontWeight >= 700));

    return {
      viewport,
      mode: screen ? screen.getAttribute("data-mode") : null,
      theaterRect,
      theaterVisibleRatio: visibleRatio(theaterRect),
      regions,
      overlaps,
      obstructions,
      duplicateIds,
      nestedVerticalScrollers: overflow.scrollers,
      clippedContainers: overflow.clipped,
      compareControls: screen ? screen.querySelectorAll(
        "[data-act='unit-tool'][data-tool='compare']"
      ).length : 0,
      titleContrast: {
        ratio: contrast(title),
        threshold: titleLarge ? 3 : 4.5,
        largeText: titleLarge
      },
      pageScrollPolicy: {
        rule: "Normal document scrolling is allowed; nested selected-scene scrolling is not.",
        scrollingElement: document.scrollingElement === document.documentElement ? "html" :
          document.scrollingElement === document.body ? "body" : "other",
        htmlOverflowY: getComputedStyle(document.documentElement).overflowY,
        bodyOverflowY: getComputedStyle(document.body).overflowY,
        scrollY: window.scrollY
      },
      bodyClasses: document.body.className
    };
  });
}

function assessScene(measurements, context, prefix = "scene") {
  const rect = measurements.theaterRect;
  const maximumAlignedTop = Math.max(165, measurements.viewport.height * 0.32);
  const aligned = Boolean(
    rect &&
    rect.top >= -3 &&
    rect.top <= maximumAlignedTop &&
    measurements.theaterVisibleRatio >= 0.95
  );
  if (!aligned) {
    hard(`${prefix}.alignment`, "The selected theater is not aligned as one visible scene.", context, {
      theaterRect: rect,
      visibleRatio: measurements.theaterVisibleRatio,
      maximumAlignedTop
    });
  }
  if (measurements.duplicateIds.length) {
    hard(`${prefix}.duplicate-ids`, "Duplicate DOM IDs exist after unit selection.", context,
      measurements.duplicateIds);
  }
  if (measurements.overlaps.length) {
    hard(`${prefix}.region-overlap`, "Essential selected-scene regions overlap.", context,
      measurements.overlaps);
  }
  if (measurements.obstructions.length) {
    hard(`${prefix}.floating-obstruction`, "A legacy/floating control obstructs the selected scene.", context,
      measurements.obstructions);
  }
  if (measurements.nestedVerticalScrollers.length) {
    hard(`${prefix}.nested-scroll`, "The selected theater contains a vertical nested scroller.", context,
      measurements.nestedVerticalScrollers);
  }
  if (measurements.clippedContainers.length) {
    hard(`${prefix}.clipped-content`, "Selected-scene content is vertically clipped instead of fitting.", context,
      measurements.clippedContainers.slice(0, 12));
  }
  if (measurements.compareControls !== 1) {
    hard(`${prefix}.compare-control`, "The selected scene does not expose exactly one Compare action.", context, {
      compareControls: measurements.compareControls
    });
  }
  const contrast = measurements.titleContrast;
  if (!contrast || contrast.ratio == null || contrast.ratio < contrast.threshold) {
    hard(`${prefix}.title-contrast`, "The selected-unit title fails WCAG text contrast.", context, contrast);
  }
  return {
    aligned,
    passed: aligned &&
      !measurements.duplicateIds.length &&
      !measurements.overlaps.length &&
      !measurements.obstructions.length &&
      !measurements.nestedVerticalScrollers.length &&
      !measurements.clippedContainers.length &&
      measurements.compareControls === 1 &&
      contrast && contrast.ratio != null && contrast.ratio >= contrast.threshold
  };
}

async function toolMeasurements(page) {
  return page.evaluate(() => {
    const dialog = document.getElementById("nl-unit-tool");
    if (!dialog) return null;
    const rect = dialog.getBoundingClientRect();
    function visible(element) {
      const style = getComputedStyle(element);
      const box = element.getBoundingClientRect();
      return !element.hidden && style.display !== "none" && style.visibility !== "hidden" &&
        Number(style.opacity) !== 0 && box.width > 0 && box.height > 0;
    }
    function parseColor(value) {
      const match = String(value || "").match(/rgba?\(([^)]+)\)/i);
      if (!match) return null;
      const parts = match[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
      if (parts.length < 3 || parts.slice(0, 3).some((part) => !Number.isFinite(part))) return null;
      return {
        r: parts[0], g: parts[1], b: parts[2],
        a: Number.isFinite(parts[3]) ? parts[3] : 1
      };
    }
    function composite(foreground, background) {
      const alpha = foreground.a + background.a * (1 - foreground.a);
      if (!alpha) return { r: 255, g: 255, b: 255, a: 1 };
      return {
        r: (foreground.r * foreground.a + background.r * background.a * (1 - foreground.a)) / alpha,
        g: (foreground.g * foreground.a + background.g * background.a * (1 - foreground.a)) / alpha,
        b: (foreground.b * foreground.a + background.b * background.a * (1 - foreground.a)) / alpha,
        a: alpha
      };
    }
    function mix(foreground, background, opacity) {
      return {
        r: foreground.r * opacity + background.r * (1 - opacity),
        g: foreground.g * opacity + background.g * (1 - opacity),
        b: foreground.b * opacity + background.b * (1 - opacity),
        a: 1
      };
    }
    function backgroundAt(element) {
      const layers = [];
      let node = element;
      while (node && node.nodeType === Node.ELEMENT_NODE) {
        const color = parseColor(getComputedStyle(node).backgroundColor);
        if (color && color.a > 0) layers.push(color);
        node = node.parentElement;
      }
      let output = { r: 255, g: 255, b: 255, a: 1 };
      for (let index = layers.length - 1; index >= 0; index -= 1) {
        output = composite(layers[index], output);
      }
      return output;
    }
    function luminance(color) {
      const values = [color.r, color.g, color.b].map((channel) => {
        const value = channel / 255;
        return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
      });
      return values[0] * 0.2126 + values[1] * 0.7152 + values[2] * 0.0722;
    }
    function ratio(foreground, background) {
      const first = luminance(foreground);
      const second = luminance(background);
      return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
    }
    function textContrast(element) {
      if (!element) return null;
      const style = getComputedStyle(element);
      const color = parseColor(style.color);
      const background = backgroundAt(element);
      if (!color || !background) return null;
      const opacity = Math.max(0, Math.min(1, Number(style.opacity) || 0));
      const opaqueText = composite(color, background);
      const finalText = mix(opaqueText, background, opacity);
      return {
        ratio: Number(ratio(finalText, background).toFixed(2)),
        threshold: 4.5,
        color: style.color,
        backgroundColor: style.backgroundColor,
        opacity
      };
    }
    const scrollers = [];
    const clipped = [];
    for (const element of [dialog, ...dialog.querySelectorAll("*")]) {
      if (element.matches("textarea, select, option, canvas, .mapboxgl-map, .mapboxgl-canvas-container") ||
          element.closest(".mapboxgl-control-container")) continue;
      if (!visible(element)) continue;
      if (element.scrollHeight - element.clientHeight <= 3) continue;
      const overflowY = getComputedStyle(element).overflowY;
      const item = {
        tag: element.tagName.toLowerCase(),
        id: element.id || null,
        className: typeof element.className === "string" ? element.className.slice(0, 180) : "",
        clientHeight: element.clientHeight,
        scrollHeight: element.scrollHeight,
        overflowY
      };
      if (/auto|scroll/.test(overflowY)) scrollers.push(item);
      if (/hidden|clip/.test(overflowY)) clipped.push(item);
    }
    const focusable = Array.from(dialog.querySelectorAll(
      "a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), " +
      "select:not([disabled]), [tabindex]:not([tabindex='-1'])"
    )).filter(visible);
    return {
      open: dialog.open || dialog.hasAttribute("open"),
      bodyLevel: dialog.parentElement === document.body,
      rect: {
        top: Number(rect.top.toFixed(2)),
        right: Number(rect.right.toFixed(2)),
        bottom: Number(rect.bottom.toFixed(2)),
        left: Number(rect.left.toFixed(2)),
        width: Number(rect.width.toFixed(2)),
        height: Number(rect.height.toFixed(2))
      },
      viewport: { width: innerWidth, height: innerHeight },
      nestedVerticalScrollers: scrollers,
      clippedContainers: clipped,
      pageRoots: {
        htmlOverflowY: getComputedStyle(document.documentElement).overflowY,
        bodyOverflowY: getComputedStyle(document.body).overflowY,
        htmlLocked: /hidden|clip/.test(getComputedStyle(document.documentElement).overflowY),
        bodyLocked: /hidden|clip/.test(getComputedStyle(document.body).overflowY),
        windowScrollY: window.scrollY
      },
      focusableCount: focusable.length,
      activeInside: dialog.contains(document.activeElement),
      activeIsBody: document.activeElement === document.body,
      titleContrast: textContrast(dialog.querySelector("#nl-unit-tool-title"))
    };
  });
}

async function probeFocusTrap(page) {
  const setup = await page.evaluate(() => {
    const dialog = document.getElementById("nl-unit-tool");
    if (!dialog) return { count: 0, prepared: false };
    const visible = (element) => {
      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return !element.hidden && style.display !== "none" && style.visibility !== "hidden" &&
        rect.width > 0 && rect.height > 0;
    };
    const items = Array.from(dialog.querySelectorAll(
      "a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), " +
      "select:not([disabled]), [tabindex]:not([tabindex='-1'])"
    )).filter(visible);
    if (items[0]) items[0].focus({ preventScroll: true });
    return { count: items.length, prepared: Boolean(items[0]) };
  });

  const escaped = [];
  if (!setup.prepared) return { ...setup, escaped, passed: false };

  await page.keyboard.press("Shift+Tab");
  let state = await page.evaluate(() => {
    const dialog = document.getElementById("nl-unit-tool");
    return {
      body: document.activeElement === document.body,
      inside: Boolean(dialog && dialog.contains(document.activeElement))
    };
  });
  if (state.body || !state.inside) escaped.push({ step: "shift-tab", ...state });

  for (let index = 0; index < Math.min(setup.count + 2, 18); index += 1) {
    await page.keyboard.press("Tab");
    state = await page.evaluate(() => {
      const dialog = document.getElementById("nl-unit-tool");
      return {
        body: document.activeElement === document.body,
        inside: Boolean(dialog && dialog.contains(document.activeElement))
      };
    });
    if (state.body || !state.inside) escaped.push({ step: index, ...state });
  }
  return { ...setup, escaped, passed: !escaped.length };
}

async function exerciseMockedLead(page, leadEndpoint, context) {
  if (!leadEndpoint) {
    hard("contact.mock-endpoint", "The private journey has no lead endpoint to intercept.", context);
    return { requestCount: 0, contractPassed: false, successFeedback: false, passed: false };
  }

  const expected = await page.evaluate(() => {
    const payload = window.NADLAN_SHOWROOM || {};
    const key = payload.config && payload.config.default_project;
    const project = key && payload.projects ? payload.projects[key] : null;
    const save = document.querySelector(".nl-unit-screen--v2 [data-act='fav'][data-id]");
    const unitId = save ? String(save.getAttribute("data-id") || "") : "";
    const unit = project && Array.isArray(project.units)
      ? project.units.find((item) => String(item.id) === unitId)
      : null;
    return {
      projectSlug: String(key || ""),
      projectWpId: Number(project && project.wp_id) || 0,
      unitId,
      unitStatus: String(unit && unit.status || "")
    };
  });

  let requestCount = 0;
  let contractPassed = false;
  const routeMatcher = (url) => url.href.startsWith(leadEndpoint);
  const routeHandler = async (route) => {
    requestCount += 1;
    let payload = null;
    try { payload = route.request().postDataJSON(); } catch {}
    contractPassed = Boolean(payload &&
      payload.source === "showroom_unit_journey_v2" &&
      payload.project_slug === expected.projectSlug &&
      Number(payload.project_wp_id) === expected.projectWpId &&
      String(payload.unit) === expected.unitId &&
      typeof payload.direction === "string" && payload.direction.length > 0 &&
      String(payload.status) === expected.unitStatus &&
      payload.consent === true &&
      typeof payload.consent_text === "string" && payload.consent_text.trim().length > 0);
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ ok: true })
    });
  };

  await page.route(routeMatcher, routeHandler);
  let successFeedback = false;
  try {
    const form = page.locator("#nl-unit-tool form[data-role='unit-contact-form']");
    await form.locator("[name='name']").fill("QA Sandbox");
    await form.locator("[name='phone']").fill("0500000000");
    await form.locator("[name='consent']").check();
    await form.locator("button[type='submit']").click();
    await page.waitForFunction(() => {
      const feedback = document.querySelector("#nl-unit-tool [data-role='contact-feedback']");
      return Boolean(feedback && !feedback.hidden && feedback.classList.contains("is-success"));
    }, null, { timeout: 10_000 }).catch(() => {});
    successFeedback = await page.locator(
      "#nl-unit-tool [data-role='contact-feedback'].is-success"
    ).isVisible().catch(() => false);
  } finally {
    await page.unroute(routeMatcher, routeHandler).catch(() => {});
  }

  const passed = requestCount === 1 && contractPassed && successFeedback;
  if (!passed) {
    hard("contact.mock-contract", "The locally intercepted valid lead did not satisfy the v2 payload/success contract.", context, {
      requestCount,
      contractPassed,
      successFeedback
    });
  }
  return { requestCount, contractPassed, successFeedback, passed };
}

async function auditTourSurface(page, context) {
  await page.waitForFunction(() => {
    const scope = document.querySelector("#nl-unit-tool[open]");
    if (!scope) return false;
    const world = scope.querySelector(".nlifp-world");
    const doors = scope.querySelector(".nlifp-doors");
    const unavailable = scope.querySelector(
      ".nl-unit-tool__empty, [data-role='tour-fallback'], [data-role='tool-fallback']"
    );
    return Boolean(
      scope.querySelector(".nl-unit-tool__tour iframe") ||
      (world && world.childElementCount > 0 && doors && doors.querySelectorAll("button").length > 0) ||
      (unavailable && String(unavailable.textContent || "").trim())
    );
  }, null, { timeout: 4_000 }).catch(() => {});

  const state = await page.evaluate(() => {
    const scope = document.querySelector("#nl-unit-tool[open]");
    const schematic = scope && scope.querySelector(".nlifp");
    const world = schematic && schematic.querySelector(".nlifp-world");
    const doors = schematic && schematic.querySelector(".nlifp-doors");
    const unavailable = scope && scope.querySelector(
      ".nl-unit-tool__empty, [data-role='tour-fallback'], [data-role='tool-fallback']"
    );
    const iframe = scope && scope.querySelector(".nl-unit-tool__tour iframe");
    const sr = window.NADLAN_SHOWROOM || {};
    const projectKey = sr.config && sr.config.default_project;
    const project = (sr.projects && sr.projects[projectKey]) || {};
    const unitId = new URL(window.location.href).searchParams.get("unit");
    const selectedUnit = Array.isArray(project.units)
      ? project.units.find((item) => String(item.id) === String(unitId))
      : null;
    const hasExplicitProtectedRoom = Boolean(selectedUnit && (
      selectedUnit.protected_room === true || selectedUnit.protected_room === 1 ||
      selectedUnit.protected_room === "1" || selectedUnit.has_mamad === true ||
      selectedUnit.has_mamad === 1 || selectedUnit.has_mamad === "1"
    ));
    const lang = document.documentElement.lang || "he";
    const dict = window.NADLAN_I18N && window.NADLAN_I18N.langs &&
      window.NADLAN_I18N.langs[lang];
    const protectedRoomLabel = String((dict && dict.fp_mamad) || "").trim();
    const doorText = String((doors && doors.textContent) || "").replace(/\s+/g, " ").trim();
    return {
      providerAvailable: typeof window.nadlanInitFP === "function",
      externalTour: Boolean(iframe),
      schematicPresent: Boolean(schematic),
      worldChildren: world ? world.childElementCount : 0,
      doorButtons: doors ? doors.querySelectorAll("button").length : 0,
      explicitUnavailable: Boolean(unavailable && String(unavailable.textContent || "").trim()),
      hasExplicitProtectedRoom,
      inventedProtectedRoom: Boolean(
        schematic && !hasExplicitProtectedRoom && protectedRoomLabel &&
        doorText.includes(protectedRoomLabel)
      )
    };
  });
  const populatedSchematic = state.schematicPresent && state.providerAvailable &&
    state.worldChildren > 0 && state.doorButtons > 0;
  const passed = state.externalTour || populatedSchematic || state.explicitUnavailable;
  const result = { ...state, populatedSchematic, passed };
  if (!passed) {
    hard("tour.blank", "The Tour tool opened without a populated walkthrough or an explicit unavailable state.",
      context, result);
  }
  if (state.inventedProtectedRoom) {
    hard("tour.invented-protected-room", "The schematic Tour labels a protected room without an explicit unit datum.",
      context, result);
  }
  return result;
}

async function auditCompareSurface(page, context) {
  const before = await page.evaluate(() => {
    const dialog = document.getElementById("nl-unit-tool");
    const body = dialog && dialog.querySelector(".nl-unit-tool__body");
    const root = dialog && dialog.querySelector('[data-role="compare-tool"]');
    const summary = root && root.querySelector('[data-role="compare-summary"]');
    const selects = root ? Array.from(root.querySelectorAll("[data-compare-slot]")) : [];
    const projectKey = new URL(location.href).searchParams.get("project") ||
      (window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config &&
        window.NADLAN_SHOWROOM.config.default_project) || "";
    const project = window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.projects &&
      window.NADLAN_SHOWROOM.projects[projectKey];
    const unitIds = project && Array.isArray(project.units)
      ? project.units.map((item) => String(item.id))
      : [];
    const selectedIds = selects.map((select) => String(select.value || "")).filter(Boolean);
    const optionSets = selects.map((select) =>
      Array.from(select.options).map((option) => String(option.value)).filter(Boolean)
    );
    const rows = summary ? Array.from(summary.querySelectorAll('[role="row"]')) : [];

    function rect(element) {
      if (!element) return null;
      const value = element.getBoundingClientRect();
      return {
        top: value.top, right: value.right, bottom: value.bottom, left: value.left,
        width: value.width, height: value.height
      };
    }
    function contains(outer, inner) {
      return Boolean(outer && inner && inner.top >= outer.top - 2 &&
        inner.left >= outer.left - 2 && inner.right <= outer.right + 2 &&
        inner.bottom <= outer.bottom + 2);
    }
    function parseColor(value) {
      const match = String(value || "").match(/rgba?\(([^)]+)\)/i);
      if (!match) return null;
      const parts = match[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
      if (parts.length < 3 || parts.slice(0, 3).some((part) => !Number.isFinite(part))) return null;
      return {
        r: parts[0], g: parts[1], b: parts[2],
        a: Number.isFinite(parts[3]) ? parts[3] : 1
      };
    }
    function composite(foreground, background) {
      const alpha = foreground.a + background.a * (1 - foreground.a);
      if (!alpha) return { r: 255, g: 255, b: 255, a: 1 };
      return {
        r: (foreground.r * foreground.a + background.r * background.a * (1 - foreground.a)) / alpha,
        g: (foreground.g * foreground.a + background.g * background.a * (1 - foreground.a)) / alpha,
        b: (foreground.b * foreground.a + background.b * background.a * (1 - foreground.a)) / alpha,
        a: alpha
      };
    }
    function mix(foreground, background, opacity) {
      return {
        r: foreground.r * opacity + background.r * (1 - opacity),
        g: foreground.g * opacity + background.g * (1 - opacity),
        b: foreground.b * opacity + background.b * (1 - opacity),
        a: 1
      };
    }
    function ancestorBackground(element) {
      const layers = [];
      let node = element && element.parentElement;
      while (node && node.nodeType === Node.ELEMENT_NODE) {
        const color = parseColor(getComputedStyle(node).backgroundColor);
        if (color && color.a > 0) layers.push(color);
        node = node.parentElement;
      }
      let output = { r: 255, g: 255, b: 255, a: 1 };
      for (let index = layers.length - 1; index >= 0; index -= 1) {
        output = composite(layers[index], output);
      }
      return output;
    }
    function luminance(color) {
      const values = [color.r, color.g, color.b].map((channel) => {
        const value = channel / 255;
        return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
      });
      return values[0] * 0.2126 + values[1] * 0.7152 + values[2] * 0.0722;
    }
    function contrastRatio(foreground, background) {
      const first = luminance(foreground);
      const second = luminance(background);
      return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05);
    }
    function selectContrast(select, index) {
      const style = getComputedStyle(select);
      const color = parseColor(style.color);
      const ownBackground = parseColor(style.backgroundColor);
      const backdrop = ancestorBackground(select);
      if (!color || !ownBackground || !backdrop) {
        return { index, disabled: select.disabled, ratio: null, threshold: 4.5 };
      }
      const opacity = Math.max(0, Math.min(1, Number(style.opacity) || 0));
      const insideBackground = composite(ownBackground, backdrop);
      const insideText = composite(color, insideBackground);
      const finalBackground = mix(insideBackground, backdrop, opacity);
      const finalText = mix(insideText, backdrop, opacity);
      return {
        index,
        disabled: select.disabled,
        ratio: Number(contrastRatio(finalText, finalBackground).toFixed(2)),
        threshold: 4.5,
        color: style.color,
        backgroundColor: style.backgroundColor,
        opacity
      };
    }

    const bodyRect = rect(body);
    const rootRect = rect(root);
    const summaryRect = rect(summary);
    let change = null;
    if (selects[1]) {
      const candidate = Array.from(selects[1].options).find((option) =>
        option.value && !option.disabled && option.value !== selects[1].value
      );
      if (candidate) change = { slot: 1, value: candidate.value };
    }
    if (!change && selects[2]) {
      if (selects[2].value) {
        change = { slot: 2, value: "" };
      } else {
        const candidate = Array.from(selects[2].options).find((option) =>
          option.value && !option.disabled
        );
        if (candidate) change = { slot: 2, value: candidate.value };
      }
    }

    return {
      rootPresent: Boolean(root),
      selectCount: selects.length,
      firstLocked: Boolean(selects[0] && selects[0].disabled),
      unitCount: unitIds.length,
      allUnitsInEverySelect: selects.length === 3 && optionSets.every((set) =>
        unitIds.every((id) => set.includes(id))
      ),
      selectedIds,
      selectedDistinct: new Set(selectedIds).size === selectedIds.length,
      selectedAtLeastTwo: selectedIds.length >= 2,
      rowCount: rows.length,
      rowShapeValid: rows.length === 6 && rows.every((row) =>
        row.children.length === selectedIds.length + 1
      ),
      differenceRows: summary ? summary.querySelectorAll(".is-different").length : 0,
      summaryText: String(summary && summary.textContent || "").replace(/\s+/g, " ").trim(),
      fitsBody: contains(bodyRect, rootRect) && contains(rootRect, summaryRect),
      rootOverflow: root ? root.scrollHeight - root.clientHeight : null,
      summaryOverflow: summary ? summary.scrollHeight - summary.clientHeight : null,
      selectContrasts: selects.map(selectContrast),
      change,
      sessionKeys: Object.keys(sessionStorage).filter((key) => key.startsWith("nl_unit_compare_v2:")),
      localKeys: Object.keys(localStorage).filter((key) => key.startsWith("nl_unit_compare_v2:")),
      projectKey
    };
  });

  let changed = { feasible: Boolean(before.change), updated: false };
  if (before.change) {
    const select = page.locator(
      `#nl-unit-tool [data-compare-slot="${before.change.slot}"]`
    );
    await select.selectOption({ value: before.change.value });
    await settle(page, 120);
    changed = await page.evaluate(({ slot, value, previousText }) => {
      const control = document.querySelector(
        `#nl-unit-tool [data-compare-slot="${slot}"]`
      );
      const summary = document.querySelector(
        '#nl-unit-tool [data-role="compare-summary"]'
      );
      const nextText = String(summary && summary.textContent || "").replace(/\s+/g, " ").trim();
      return {
        feasible: true,
        slot,
        requestedValue: value,
        actualValue: control ? control.value : null,
        summaryChanged: nextText !== previousText,
        updated: Boolean(control && control.value === value && nextText !== previousText)
      };
    }, {
      slot: before.change.slot,
      value: before.change.value,
      previousText: before.summaryText
    });
  }

  const after = await page.evaluate(() => {
    const selects = Array.from(document.querySelectorAll(
      '#nl-unit-tool [data-compare-slot]'
    ));
    const selectedIds = selects.map((select) => String(select.value || "")).filter(Boolean);
    const key = Object.keys(sessionStorage).find((candidate) =>
      candidate.startsWith("nl_unit_compare_v2:")
    );
    let stored = [];
    try { stored = key ? JSON.parse(sessionStorage.getItem(key) || "[]") : []; } catch {}
    return {
      selectedIds,
      stored,
      sessionKey: key || "",
      localKeyCount: Object.keys(localStorage).filter((candidate) =>
        candidate.startsWith("nl_unit_compare_v2:")
      ).length
    };
  });

  const storagePassed = after.sessionKey ===
      `nl_unit_compare_v2:${encodeURIComponent(before.projectKey)}` &&
    after.localKeyCount === 0 &&
    JSON.stringify(after.stored) === JSON.stringify(after.selectedIds);
  const selectContrastPassed = before.selectContrasts.length === 3 &&
    before.selectContrasts.every((measurement) =>
      measurement.ratio != null && measurement.ratio >= measurement.threshold
    );
  const passed = before.rootPresent && before.selectCount === 3 && before.firstLocked &&
    before.unitCount >= 2 && before.allUnitsInEverySelect &&
    before.selectedDistinct && before.selectedAtLeastTwo &&
    before.rowShapeValid && before.differenceRows > 0 && before.summaryText.length > 0 &&
    before.fitsBody && before.rootOverflow <= 3 && before.summaryOverflow <= 3 &&
    selectContrastPassed && changed.feasible && changed.updated && storagePassed;
  const result = {
    before, changed, after, storagePassed, selectContrastPassed, passed
  };
  if (!passed) {
    hard("compare.contract", "The v2 Compare tool did not satisfy its selector, facts, fit, update or session-state contract.",
      context, result);
  }
  return result;
}

async function exerciseTool(page, kind, scenario, scenarioIndex) {
  const context = { viewport: scenario.viewport, language: scenario.language, tool: kind };
  const triggerSelector = kind === "area"
    ? ".nl-unit-beam__open[data-tool='area']"
    : kind === "contact"
      ? ".nl-unit-contact[data-tool='contact']"
      : kind === "compare"
        ? ".nl-unit-quick [data-act='unit-tool'][data-tool='compare']"
      : `.nl-unit-door[data-tool="${kind}"]`;
  const trigger = page.locator(triggerSelector).first();
  if (!(await trigger.count()) || !(await trigger.isVisible().catch(() => false))) {
    const message = `The ${kind} tool trigger is unavailable for this unit.`;
    if (OPTIONAL_TOOLS.has(kind)) warn("tool.optional-unavailable", message, context);
    else hard("tool.trigger-missing", message, context);
    return { kind, available: false, optional: OPTIONAL_TOOLS.has(kind), passed: OPTIONAL_TOOLS.has(kind) };
  }

  const scrollBefore = await page.evaluate(() => window.scrollY);
  let leadEndpoint = "";
  if (kind === "contact") {
    leadEndpoint = await page.evaluate(() => {
      const raw = String(
        (window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config &&
          window.NADLAN_SHOWROOM.config.lead_endpoint) || ""
      );
      if (!raw) return "";
      try { return new URL(raw, location.origin).href; } catch { return ""; }
    });
  }
  const contactPosts = [];
  const allPosts = [];
  const onRequest = (request) => {
    if (request.method() !== "POST") return;
    allPosts.push(request.url());
    if (leadEndpoint && request.url().startsWith(leadEndpoint)) contactPosts.push(request.url());
  };
  if (kind === "contact") page.on("request", onRequest);

  try {
    await trigger.click();
    await page.waitForSelector("#nl-unit-tool[open]", { state: "visible", timeout: 12_000 });
    await settle(page, 180);

    const tourState = kind === "tour" ? await auditTourSurface(page, context) : null;
    const compareState = kind === "compare" ? await auditCompareSurface(page, context) : null;
    const measurements = await toolMeasurements(page);
    const focusTrap = await probeFocusTrap(page);
    const rect = measurements && measurements.rect;
    const viewport = measurements && measurements.viewport;
    const fullViewport = Boolean(rect && viewport &&
      Math.abs(rect.top) <= 2 && Math.abs(rect.left) <= 2 &&
      Math.abs(rect.width - viewport.width) <= 2 &&
      Math.abs(rect.height - viewport.height) <= 2);

    if (!measurements || !measurements.open || !measurements.bodyLevel || !fullViewport) {
      hard("tool.viewport", `The ${kind} tool is not a body-level full-viewport dialog.`, context,
        measurements);
    }
    if (!measurements || !measurements.titleContrast ||
        measurements.titleContrast.ratio < measurements.titleContrast.threshold) {
      hard("tool.title-contrast", `The ${kind} dialog title fails 4.5:1 computed contrast.`, context,
        measurements && measurements.titleContrast);
    }
    if (measurements && measurements.nestedVerticalScrollers.length) {
      hard("tool.nested-scroll", `The ${kind} tool contains a nested vertical scroller.`, context,
        measurements.nestedVerticalScrollers);
    }
    if (measurements && measurements.clippedContainers.length) {
      hard("tool.clipped-content", `The ${kind} tool clips content instead of fitting it.`, context,
        measurements.clippedContainers.slice(0, 12));
    }
    if (!measurements || !measurements.pageRoots.htmlLocked || !measurements.pageRoots.bodyLocked ||
        Math.abs(measurements.pageRoots.windowScrollY - scrollBefore) > 2) {
      hard("tool.root-scroll-lock",
        `Opening ${kind} did not lock html/body while preserving the document position.`, context, {
          scrollBefore,
          pageRoots: measurements && measurements.pageRoots
        });
    }
    if (!focusTrap.passed) {
      hard("tool.focus-trap", `Keyboard focus escaped the ${kind} dialog.`, context, focusTrap);
    }

    let contactValidation = null;
    let emptyLeadPosts = null;
    let mockedLead = null;
    if (kind === "contact") {
      const submit = page.locator("#nl-unit-tool form[data-role='unit-contact-form'] button[type='submit']");
      await submit.click();
      await settle(page, 180);
      contactValidation = await page.evaluate(() => {
        const form = document.querySelector("#nl-unit-tool form[data-role='unit-contact-form']");
        const feedback = document.querySelector("#nl-unit-tool [data-role='contact-feedback']");
        return {
          invalidControls: form ? Array.from(form.elements).filter((field) => field.willValidate && !field.validity.valid).length : 0,
          formValid: form ? form.checkValidity() : null,
          feedbackVisible: Boolean(feedback && !feedback.hidden),
          feedbackHasText: Boolean(feedback && feedback.textContent.trim())
        };
      });
      if (contactValidation.formValid !== false || contactValidation.invalidControls < 1 ||
          !contactValidation.feedbackVisible || !contactValidation.feedbackHasText) {
        hard("contact.empty-validation", "The empty contact form did not expose a usable validation state.",
          context, contactValidation);
      }
      if (contactPosts.length) {
        hard("contact.lead-post", "An empty contact-form probe emitted a lead POST request.", context, {
          leadPostCount: contactPosts.length,
          allPostCount: allPosts.length
        });
      }
      emptyLeadPosts = contactPosts.length;
      if (scenarioIndex === 0) {
        mockedLead = await exerciseMockedLead(page, leadEndpoint, context);
        report.mockedLead = mockedLead;
      }
    }

    if (scenarioIndex === 0) {
      await page.screenshot({
        path: path.join(SCREENSHOT_DIR, `${scenario.viewport}-${scenario.language}-tool-${kind}.png`),
        fullPage: false
      });
    }

    const closeMethod = kind === "contact" || TOOL_KINDS.indexOf(kind) % 2 === 0
      ? "button"
      : "escape";
    if (closeMethod === "button") {
      await page.locator("#nl-unit-tool [data-act='unit-tool-back']").first().click();
    } else {
      await page.keyboard.press("Escape");
    }
    await page.waitForFunction(() => {
      const dialog = document.getElementById("nl-unit-tool");
      return !dialog || !dialog.open;
    }, null, { timeout: 12_000 });
    await settle(page, 180);

    const afterClose = await page.evaluate(({ expectedKind }) => {
      const active = document.activeElement;
      return {
        scrollY: window.scrollY,
        activeIsBody: active === document.body,
        activeInsideScene: Boolean(active && active.closest && active.closest(".nl-unit-screen--v2")),
        activeKind: active && active.getAttribute ? active.getAttribute("data-tool") : null,
        expectedKind
      };
    }, { expectedKind: kind });
    const scrollDelta = Math.abs(afterClose.scrollY - scrollBefore);
    const focusRestored = !afterClose.activeIsBody && afterClose.activeInsideScene &&
      afterClose.activeKind === kind;
    if (scrollDelta > 2) {
      hard("tool.scroll-restore", `Closing ${kind} changed page scroll by ${scrollDelta}px.`, context, {
        scrollBefore,
        scrollAfter: afterClose.scrollY,
        scrollDelta,
        closeMethod
      });
    }
    if (!focusRestored) {
      hard("tool.focus-restore", `Closing ${kind} did not restore focus to its scene trigger.`, context,
        afterClose);
    }

    return {
      kind,
      available: true,
      optional: OPTIONAL_TOOLS.has(kind),
      fullViewport,
      nestedVerticalScrollers: measurements.nestedVerticalScrollers,
      clippedContainers: measurements.clippedContainers,
      focusTrap,
      closeMethod,
      scrollDelta,
      focusRestored,
      contactValidation,
      emptyContactLeadPosts: emptyLeadPosts,
      mockedLead,
      tourState,
      compareState,
      passed: Boolean(measurements.bodyLevel) && fullViewport &&
        measurements.titleContrast &&
        measurements.titleContrast.ratio >= measurements.titleContrast.threshold &&
        !measurements.nestedVerticalScrollers.length &&
        !measurements.clippedContainers.length &&
        measurements.pageRoots.htmlLocked && measurements.pageRoots.bodyLocked &&
        Math.abs(measurements.pageRoots.windowScrollY - scrollBefore) <= 2 &&
        focusTrap.passed && scrollDelta <= 2 && focusRestored &&
        (!tourState || tourState.passed) &&
        (!compareState || compareState.passed) &&
        (!contactValidation || (
          contactValidation.formValid === false &&
          contactValidation.invalidControls > 0 &&
          emptyLeadPosts === 0 && (scenarioIndex !== 0 || (mockedLead && mockedLead.passed))
        ))
    };
  } finally {
    if (kind === "contact") page.off("request", onRequest);
    const stillOpen = await page.locator("#nl-unit-tool[open]").count().catch(() => 0);
    if (stillOpen) {
      await page.keyboard.press("Escape").catch(() => {});
      await settle(page, 100);
    }
  }
}

async function exerciseBrowserBack(page, scenario) {
  const context = { viewport: scenario.viewport, language: scenario.language, tool: "plan" };
  const trigger = page.locator(".nl-unit-door[data-tool='plan']").first();
  if (!(await trigger.count()) || !(await trigger.isVisible().catch(() => false))) {
    hard("browser-back.trigger", "The plan trigger needed for Browser Back acceptance is unavailable.", context);
    return { available: false, passed: false };
  }

  const scrollBefore = await page.evaluate(() => window.scrollY);
  const firstUnitId = await page.locator(".nl-unit-screen--v2 [data-act='fav'][data-id]")
    .first().getAttribute("data-id");
  await trigger.click();
  await page.waitForSelector("#nl-unit-tool[open]", { state: "visible", timeout: 12_000 });
  await settle(page, 120);
  const before = await page.evaluate(() => ({
    marker: Boolean(history.state && history.state.nlUnitTool),
    dialogOpen: Boolean(document.getElementById("nl-unit-tool")?.open),
    activeInsideDialog: Boolean(
      document.getElementById("nl-unit-tool")?.contains(document.activeElement)
    )
  }));
  if (!before.marker) {
    hard("browser-back.history-marker", "Opening a fullscreen tool did not create its scoped history entry.",
      context, before);
  }

  let navigationError = null;
  try {
    await page.goBack({ waitUntil: "commit", timeout: 12_000 });
  } catch (error) {
    navigationError = safeError(error);
  }
  await page.waitForFunction(() => {
    const dialog = document.getElementById("nl-unit-tool");
    return !dialog || !dialog.open;
  }, null, { timeout: 12_000 }).catch(() => {});
  await settle(page, 180);

  const after = await page.evaluate(() => {
    const dialog = document.getElementById("nl-unit-tool");
    const active = document.activeElement;
    return {
      dialogOpen: Boolean(dialog && dialog.open),
      bodyToolClass: document.body.classList.contains("nl-unit-tool-open"),
      htmlToolClass: document.documentElement.classList.contains("nl-unit-tool-open"),
      selectedSceneStillOpen: document.body.classList.contains("nl-unit-v2-active"),
      activeIsBody: active === document.body,
      activeKind: active && active.getAttribute ? active.getAttribute("data-tool") : null,
      activeInsideScene: Boolean(active && active.closest && active.closest(".nl-unit-screen--v2")),
      scrollY: window.scrollY
    };
  });
  const scrollDelta = Math.abs(after.scrollY - scrollBefore);
  const focusRestored = !after.activeIsBody && after.activeInsideScene && after.activeKind === "plan";
  const backPassed = !navigationError && before.marker && !after.dialogOpen &&
    !after.bodyToolClass && !after.htmlToolClass && after.selectedSceneStillOpen &&
    focusRestored && scrollDelta <= 2;
  if (!backPassed) {
    hard("browser-back.close", "Browser Back did not close exactly one tool and restore its scene state.", context, {
      navigationError,
      before,
      after,
      scrollBefore,
      scrollDelta,
      focusRestored
    });
  }

  let forwardError = null;
  try {
    await page.goForward({ waitUntil: "commit", timeout: 12_000 });
  } catch (error) {
    forwardError = safeError(error);
  }
  await page.waitForSelector("#nl-unit-tool[open].nl-unit-tool--plan", {
    state: "visible",
    timeout: 12_000
  }).catch(() => {});
  await settle(page, 140);
  const forward = await page.evaluate(() => ({
    dialogOpen: Boolean(document.getElementById("nl-unit-tool")?.open),
    planClass: document.getElementById("nl-unit-tool")?.classList.contains("nl-unit-tool--plan") || false,
    marker: Boolean(history.state && history.state.nlUnitTool),
    selectedSceneStillOpen: document.body.classList.contains("nl-unit-v2-active")
  }));
  const forwardPassed = !forwardError && forward.dialogOpen && forward.planClass &&
    forward.marker && forward.selectedSceneStillOpen;
  if (!forwardPassed) {
    hard("browser-forward.reopen", "Browser Forward did not truthfully reopen the same plan tool.", context, {
      forwardError,
      forward
    });
  }

  if (forward.dialogOpen) {
    await page.locator("#nl-unit-tool [data-act='unit-tool-back']").first().click();
    await page.waitForFunction(() => !document.getElementById("nl-unit-tool")?.open, null, {
      timeout: 12_000
    }).catch(() => {});
    await settle(page, 140);
  }

  let staleForwardPassed = true;
  let staleForward = { feasible: false };
  const unitBack = page.locator(".nl-unit-screen--v2 [data-act='unit-back']").first();
  if (firstUnitId && await unitBack.count()) {
    await unitBack.click();
    await page.waitForFunction(() => !document.body.classList.contains("nl-unit-v2-active"), null, {
      timeout: 12_000
    });
    const choices = page.locator(".nl-invgrid .nl-ucard__select");
    const choiceCount = await choices.count();
    let second = null;
    for (let index = 0; index < choiceCount; index += 1) {
      const candidate = choices.nth(index);
      if (await candidate.getAttribute("data-id") !== firstUnitId) {
        second = candidate;
        break;
      }
    }
    if (second) {
      const secondUnitId = await second.getAttribute("data-id");
      await second.click();
      await page.waitForFunction(() => document.body.classList.contains("nl-unit-v2-active"), null, {
        timeout: 12_000
      });
      await settle(page, 140);
      const urlBeforeForward = page.url();
      await page.goForward({ waitUntil: "commit", timeout: 4_000 }).catch(() => null);
      await settle(page, 180);
      staleForward = await page.evaluate(({ expectedUnit, expectedUrl }) => {
        const selected = document.querySelector(".nl-unit-screen--v2 [data-act='fav'][data-id]");
        return {
          feasible: true,
          dialogOpen: Boolean(document.getElementById("nl-unit-tool")?.open),
          selectedUnitPreserved: Boolean(selected && selected.getAttribute("data-id") === expectedUnit),
          urlPreserved: location.href === expectedUrl,
          selectedSceneOpen: document.body.classList.contains("nl-unit-v2-active")
        };
      }, { expectedUnit: secondUnitId, expectedUrl: urlBeforeForward });
      staleForwardPassed = !staleForward.dialogOpen && staleForward.selectedUnitPreserved &&
        staleForward.urlPreserved && staleForward.selectedSceneOpen;
      if (!staleForwardPassed) {
        hard("browser-forward.stale-tool", "Forward reopened stale unit A after unit B replaced the selection.", context,
          staleForward);
      }
    }
  }

  const passed = backPassed && forwardPassed && staleForwardPassed;
  return {
    available: true,
    before,
    after,
    navigationError,
    scrollDelta,
    focusRestored,
    forward,
    forwardError,
    staleForward,
    passed
  };
}

async function tryHotspotSelection(page, viewport) {
  const context = { viewport: viewport.name, language: "he", source: "hotspot" };
  const back = page.locator(".nl-unit-screen--v2 [data-act='unit-back']").first();
  if (await back.count()) {
    await back.click();
    await page.waitForFunction(() => !document.body.classList.contains("nl-unit-v2-active"), null, {
      timeout: 10_000
    });
    await settle(page, 140);
  }

  const candidates = page.locator(".nl-stagewrap .nl-hot[data-act='select']");
  const count = await candidates.count();
  let hotspot = null;
  for (let index = 0; index < count; index += 1) {
    const candidate = candidates.nth(index);
    const box = await candidate.boundingBox().catch(() => null);
    if (box && box.width >= 8 && box.height >= 8 && await candidate.isVisible().catch(() => false)) {
      hotspot = candidate;
      break;
    }
  }
  if (!hotspot) {
    warn("selection.hotspot-unavailable",
      "No model hotspot had a usable visible hit target at this emulated viewport.", context, { count });
    const result = { viewport: viewport.name, feasible: false, passed: true };
    report.hotspotChecks.push(result);
    return result;
  }

  await hotspot.click();
  await page.waitForFunction(() => document.body.classList.contains("nl-unit-v2-active"), null, {
    timeout: 12_000
  });
  await settle(page, 650);
  const measurements = await sceneMeasurements(page);
  const assessment = assessScene(measurements, context, "hotspot");
  await page.screenshot({
    path: path.join(SCREENSHOT_DIR, `${viewport.name}-he-hotspot-selected.png`),
    fullPage: false
  });
  const result = {
    viewport: viewport.name,
    feasible: true,
    assessment,
    measurements,
    passed: assessment.passed
  };
  report.hotspotChecks.push(result);
  return result;
}

async function runScenario(page, viewport, language, scenarioIndex) {
  const context = { viewport: viewport.name, language };
  await page.setViewportSize({ width: viewport.width, height: viewport.height });
  const response = await page.goto(urlForLanguage("he"), {
    waitUntil: "domcontentloaded",
    timeout: 45_000
  });
  if (!response || response.status() >= 400) {
    hard("matrix.http", "The unlocked sandbox failed to load for a matrix scenario.", context, {
      status: response ? response.status() : null
    });
  }
  await waitForJourney(page);
  await settle(page, 180);

  if (scenarioIndex === 0) await auditUnlockedPrivacy(page, response);

  const languageState = await setLanguageThroughUi(page, language, context);
  const methodIndex = scenarioIndex % 3;
  const interaction = methodIndex === 0 ? "click" : methodIndex === 1 ? "enter" : "space";
  const unitId = await selectFirstInventoryUnit(page, interaction, context);
  const measurements = await sceneMeasurements(page);
  const scene = assessScene(measurements, context);

  await page.screenshot({
    path: path.join(SCREENSHOT_DIR, `${viewport.name}-${language}-selected.png`),
    fullPage: false
  });

  const tools = [];
  for (const kind of TOOL_KINDS) {
    try {
      tools.push(await exerciseTool(page, kind, { viewport: viewport.name, language }, scenarioIndex));
    } catch (error) {
      hard("tool.exception", `The ${kind} tool probe raised an exception.`, { ...context, tool: kind }, {
        error: safeError(error)
      });
      tools.push({ kind, available: null, passed: false, error: safeError(error) });
      await page.keyboard.press("Escape").catch(() => {});
      await settle(page, 100);
    }
  }

  const browserBack = language === "he"
    ? await exerciseBrowserBack(page, { viewport: viewport.name, language })
    : null;

  const scenario = {
    viewport: viewport.name,
    width: viewport.width,
    height: viewport.height,
    language,
    languageState,
    interaction,
    unitSelected: Boolean(unitId),
    scene,
    measurements,
    tools,
    browserBack,
    passed: languageState.passed && scene.passed && tools.every((tool) => tool.passed) &&
      (!browserBack || browserBack.passed)
  };
  report.matrix.push(scenario);
  return scenario;
}

async function runRotationProbe(page) {
  const states = [];
  const portrait = { width: 375, height: 812, name: "portrait" };
  const landscapeMobile = { width: 812, height: 375, name: "landscape-mobile" };
  const landscapeDesktop = { width: 1280, height: 800, name: "landscape-desktop" };

  await page.setViewportSize({ width: portrait.width, height: portrait.height });
  await page.goto(urlForLanguage("he"), { waitUntil: "domcontentloaded", timeout: 45_000 });
  await waitForJourney(page);
  await selectFirstInventoryUnit(page, "click", { probe: "rotation", phase: "portrait-before" });

  async function rotateWithCompareOpen(from, to) {
    const context = {
      probe: "rotation-with-tool",
      phase: `${from.name}-to-${to.name}`,
      viewport: `${to.width}x${to.height}`
    };
    const trigger = page.locator(
      ".nl-unit-screen--v2 .nl-unit-quick [data-act='unit-tool'][data-tool='compare']"
    ).first();
    const scrollBefore = await page.evaluate(() => window.scrollY);
    const source = await page.evaluate(() => {
      const screen = document.getElementById("nl-unit-screen");
      window.__nlQaRotationTrigger = screen && screen.querySelector(
        ".nl-unit-quick [data-act='unit-tool'][data-tool='compare']"
      );
      return {
        mode: screen && screen.getAttribute("data-mode"),
        expectedMode: matchMedia(
          "(max-width:900px), (max-width:1024px) and (max-height:600px)"
        ).matches ? "mobile" : "desktop"
      };
    });

    await trigger.click();
    await page.waitForSelector("#nl-unit-tool[open].nl-unit-tool--compare", {
      state: "visible",
      timeout: 12_000
    });
    await page.setViewportSize({ width: to.width, height: to.height });
    await page.waitForFunction(({ width, height }) =>
      window.innerWidth === width && window.innerHeight === height,
    to, { timeout: 5_000 });
    await settle(page, 220);

    const during = await page.evaluate(() => {
      const dialog = document.getElementById("nl-unit-tool");
      const screen = document.getElementById("nl-unit-screen");
      return {
        dialogOpen: Boolean(dialog && dialog.open),
        mode: screen && screen.getAttribute("data-mode"),
        historyMarker: Boolean(history.state && history.state.nlUnitTool),
        triggerPreserved: Boolean(window.__nlQaRotationTrigger &&
          window.__nlQaRotationTrigger === screen?.querySelector(
            ".nl-unit-quick [data-act='unit-tool'][data-tool='compare']"
          ))
      };
    });

    await page.locator("#nl-unit-tool [data-act='unit-tool-back']").first().click();
    await page.waitForFunction(() => !document.getElementById("nl-unit-tool")?.open, null, {
      timeout: 12_000
    });
    await settle(page, 550);

    const measurements = await sceneMeasurements(page);
    const assessment = assessScene(measurements, context, "rotation-tool-close");
    const lifecycle = await page.evaluate(() => {
      const active = document.activeElement;
      const screen = document.getElementById("nl-unit-screen");
      const theater = document.querySelector(".nl-theater--unit-v2");
      const expectedMode = matchMedia(
        "(max-width:900px), (max-width:1024px) and (max-height:600px)"
      ).matches ? "mobile" : "desktop";
      const replacementTrigger = screen && screen.querySelector(
        ".nl-unit-quick [data-act='unit-tool'][data-tool='compare']"
      );
      const subtreeReplaced = Boolean(window.__nlQaRotationTrigger && replacementTrigger &&
        window.__nlQaRotationTrigger !== replacementTrigger);
      delete window.__nlQaRotationTrigger;
      return {
        expectedMode,
        dataMode: screen && screen.getAttribute("data-mode"),
        modeClass: Boolean(theater && theater.classList.contains(
          `nl-theater--unit-v2-${expectedMode}`
        )),
        oppositeClass: Boolean(theater && theater.classList.contains(
          `nl-theater--unit-v2-${expectedMode === "mobile" ? "desktop" : "mobile"}`
        )),
        focusRestored: Boolean(active && active.closest(".nl-unit-screen--v2") &&
          active.getAttribute("data-tool") === "compare"),
        activeIsBody: active === document.body,
        historyMarker: Boolean(history.state && history.state.nlUnitTool),
        htmlToolClass: document.documentElement.classList.contains("nl-unit-tool-open"),
        bodyToolClass: document.body.classList.contains("nl-unit-tool-open"),
        subtreeReplaced,
        scrollY: window.scrollY
      };
    });
    const scrollDelta = Math.abs(lifecycle.scrollY - scrollBefore);
    const deferredWhileOpen = during.dialogOpen && during.historyMarker && during.triggerPreserved &&
      during.mode === source.mode && source.mode === source.expectedMode;
    const modePassed = lifecycle.dataMode === lifecycle.expectedMode &&
      lifecycle.modeClass && !lifecycle.oppositeClass;
    /* A geometry-changing close intentionally realigns the selected scene;
       its pre-resize scroll coordinate is stale. Normal no-resize tool closes
       remain covered by exerciseTool's exact <=2px scroll assertion. */
    const passed = deferredWhileOpen && lifecycle.subtreeReplaced && modePassed && assessment.passed &&
      measurements.duplicateIds.length === 0 && lifecycle.focusRestored &&
      !lifecycle.activeIsBody && !lifecycle.historyMarker &&
      !lifecycle.htmlToolClass && !lifecycle.bodyToolClass;
    const result = {
      from, to, source, during, lifecycle, scrollBefore, scrollDelta,
      scrollContract: "realign-current-scene-after-viewport-change",
      deferredWhileOpen, modePassed, measurements, assessment, passed
    };
    if (!passed) {
      hard("rotation.tool-lifecycle",
        "Resize while Compare was open did not defer, atomically resync on close, or restore scene state.",
        context, result);
    }
    states.push(result);
    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, `rotation-tool-${to.name}-${to.width}x${to.height}.png`),
      fullPage: false
    });
    return result;
  }

  await rotateWithCompareOpen(portrait, landscapeMobile);
  await rotateWithCompareOpen(landscapeMobile, portrait);
  await rotateWithCompareOpen(portrait, landscapeDesktop);
  await rotateWithCompareOpen(landscapeDesktop, portrait);

  const sameModeMobilePassed = states.slice(0, 2).length === 2 &&
    states.slice(0, 2).every((state) => state.passed &&
      state.source.expectedMode === "mobile" && state.lifecycle.expectedMode === "mobile");
  const modeCrossingPassed = states.slice(2, 4).length === 2 &&
    states.slice(2, 4).every((state) => state.passed) &&
    states[2].lifecycle.expectedMode === "desktop" &&
    states[3].lifecycle.expectedMode === "mobile";
  const returnedToMobile = states[3] && states[3].measurements.mode === "mobile";
  if (!sameModeMobilePassed) {
    hard("rotation.same-mode-mobile",
      "A real mobile portrait-landscape rotation did not flush its deferred scene sync on close.",
      { probe: "rotation-with-tool" }, { states: states.slice(0, 2) });
  }
  if (!modeCrossingPassed) {
    hard("rotation.mode-crossing",
      "The mobile-desktop viewport crossing did not flush its deferred scene sync on close.",
      { probe: "rotation-with-tool" }, { states: states.slice(2, 4) });
  }
  if (!returnedToMobile) {
    hard("rotation.mode-return",
      "Portrait-landscape-portrait with Compare open did not return to one mobile scene subtree.",
      { probe: "rotation-with-tool" }, {
        finalMode: states[1] && states[1].measurements.mode
      });
  }
  report.rotation = {
    states,
    sameModeMobilePassed,
    modeCrossingPassed,
    returnedToMobile,
    passed: returnedToMobile && sameModeMobilePassed && modeCrossingPassed &&
      states.length === 4 && states.every((state) => state.passed)
  };
}

async function auditSiblingIsolation(context) {
  const pages = [
    { name: "legacy-sandbox", url: publicSibling("/projects/sandbox-unit-scene/") },
    { name: "rainbow", url: publicSibling("/projects/rainbow-tel-aviv/") }
  ];

  for (const target of pages) {
    const page = await context.newPage();
    try {
      await page.setViewportSize({ width: 1280, height: 800 });
      const response = await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 45_000 });
      await page.waitForSelector("#nl-root", { state: "attached", timeout: 30_000 });
      await settle(page, 250);
      const before = await page.evaluate(() => ({
        bodyClasses: document.body.className,
        configV2: Boolean(window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config &&
          window.NADLAN_SHOWROOM.config.selected_unit_surface_v2),
        root: Boolean(document.getElementById("nl-root")),
        model: Boolean(document.getElementById("nl-mv")),
        inventoryButtons: document.querySelectorAll(
          ".nl-invgrid [data-act='select']"
        ).length
      }));
      const v2ClassBefore = /(?:^|\s)nl-unit-v2-(?:sandbox|enabled|active)(?:\s|$)/.test(before.bodyClasses);

      let selection = null;
      const inventory = page.locator(".nl-invgrid [data-act='select']").first();
      if (await inventory.count()) {
        await inventory.click();
        await settle(page, 500);
        selection = await page.evaluate(() => ({
          v2Screen: Boolean(document.querySelector(".nl-unit-screen--v2:not([hidden])")),
          v2BodyClass: /(?:^|\s)nl-unit-v2-(?:sandbox|enabled|active)(?:\s|$)/.test(document.body.className),
          legacyPanelOpen: Boolean(document.querySelector("#nl-panel.is-open")),
          legacySelectedScreen: Boolean(document.querySelector("#nl-unit-screen:not(.nl-unit-screen--v2):not([hidden])"))
        }));
      }

      const normalSelection = !selection || (
        !selection.v2Screen && !selection.v2BodyClass &&
        (selection.legacyPanelOpen || selection.legacySelectedScreen)
      );
      const passed = Boolean(response && response.status() < 400 && before.root && before.model &&
        before.inventoryButtons > 0 && !before.configV2 && !v2ClassBefore && normalSelection);
      const result = {
        name: target.name,
        url: target.url,
        status: response ? response.status() : null,
        before,
        selection,
        passed
      };
      report.isolation.push(result);
      if (!passed) {
        hard("isolation.regression", `${target.name} no longer behaves as a non-v2 showroom.`,
          { page: target.name }, result);
      }
      await page.screenshot({
        path: path.join(SCREENSHOT_DIR, `isolation-${target.name}.png`),
        fullPage: false
      });
    } catch (error) {
      hard("isolation.exception", `Could not complete the ${target.name} isolation probe.`,
        { page: target.name }, { error: safeError(error) });
      report.isolation.push({ name: target.name, url: target.url, passed: false, error: safeError(error) });
    } finally {
      await page.close().catch(() => {});
    }
  }
}

function summarizeTotals() {
  const tools = report.matrix.flatMap((scenario) => scenario.tools || []);
  return {
    scenarios: report.matrix.length,
    scenariosPassed: report.matrix.filter((scenario) => scenario.passed).length,
    toolsProbed: tools.length,
    toolsPassed: tools.filter((tool) => tool.passed).length,
    browserBackProbes: report.matrix.filter((scenario) => scenario.browserBack).length,
    browserBackPassed: report.matrix.filter((scenario) => scenario.browserBack && scenario.browserBack.passed).length,
    hotspotProbes: report.hotspotChecks.length,
    isolationPages: report.isolation.length,
    hardFailures: report.hardFailures.length,
    warnings: report.warnings.length
  };
}

function markdownReport() {
  const lines = [];
  const status = report.hardFailures.length ? "FAIL" : "PASS";
  lines.push("# Private unit journey QA");
  lines.push("");
  lines.push(`Outcome: **${status}**`);
  lines.push("");
  lines.push(`Target: ${report.target.url}`);
  lines.push(`Started: ${report.startedAt}`);
  lines.push(`Finished: ${report.finishedAt}`);
  lines.push("");
  lines.push("> Chromium viewport and orientation emulation is not acceptance on a physical phone. The owner still needs to approve the journey on the real target device.");
  lines.push("");
  lines.push("The password, cookies, form values, request headers and browser storage are deliberately absent from this report.");
  lines.push("");
  lines.push("## Unauthenticated gate");
  lines.push("");
  if (report.gate) {
    lines.push("| HTTP | Clean context | One form only | Normal chrome | Sandbox class | Payload leak | Engine/project assets | X-Robots | Referrer | Result |");
    lines.push("|---:|---|---|---|---|---|---:|---|---|---|");
    lines.push(`| ${report.gate.status ?? "n/a"} | ${report.gate.cleanContextCookieCount === 0 ? "yes" : "no"} | ${report.gate.passwordFormCount === 1 && report.gate.contentShellOnlyForm ? "yes" : "no"} | ${report.gate.normalChromeVisible ? "yes" : "no"} | ${report.gate.sandboxBodyClass ? "yes" : "no"} | ${report.gate.payloadPresent ? "yes" : "no"} | ${report.gate.engineAssetRequests}/${report.gate.projectAssetRequests} | ${report.gate.xRobotsTag || "missing"} | ${report.gate.referrerPolicy || "missing"} | ${report.gate.passed ? "PASS" : "FAIL"} |`);
  } else {
    lines.push("Gate did not run.");
  }
  lines.push("");
  lines.push(`Unlocked noindex persistence: ${report.privacyAfterUnlock && report.privacyAfterUnlock.passed ? "PASS" : "FAIL"}.`);
  lines.push(`Anonymous discovery/API exclusion: ${report.discovery && report.discovery.passed ? "PASS" : "FAIL"}.`);
  lines.push(`Private sessionStorage isolation + Save focus: ${report.storageIsolation && report.storageIsolation.passed ? "PASS" : "FAIL"}.`);
  lines.push(`Locally mocked valid lead contract: ${report.mockedLead && report.mockedLead.passed ? "PASS" : "FAIL"}.`);
  lines.push(`Missing-password fail-closed source contract: ${report.sourceContract && report.sourceContract.passed ? "PASS" : "FAIL"}.`);
  if (report.discovery) {
    for (const check of report.discovery.checks) {
      lines.push(`- ${check.label}: HTTP ${check.status ?? "n/a"}, identity ${check.identityExposed ? "EXPOSED" : "hidden"}, ${check.passed ? "PASS" : (check.feasible && check.status === 404 ? "not installed" : "FAIL")}.`);
    }
  }
  lines.push("");
  lines.push("## Viewport and language matrix");
  lines.push("");
  lines.push("| Viewport | Language | Selection | Scene visible | Duplicate IDs | Nested scroll | Title contrast | Tools | Browser Back | Result |");
  lines.push("|---|---|---|---|---:|---:|---:|---:|---|---|");
  for (const scenario of report.matrix) {
    const measurements = scenario.measurements || {};
    const toolsPassed = (scenario.tools || []).filter((tool) => tool.passed).length;
    lines.push(`| ${scenario.viewport} | ${scenario.language} | ${scenario.interaction} | ${scenario.scene && scenario.scene.aligned ? "yes" : "no"} | ${(measurements.duplicateIds || []).length} | ${(measurements.nestedVerticalScrollers || []).length} | ${measurements.titleContrast && measurements.titleContrast.ratio != null ? measurements.titleContrast.ratio : "n/a"} | ${toolsPassed}/${(scenario.tools || []).length} | ${scenario.browserBack ? (scenario.browserBack.passed ? "PASS" : "FAIL") : "-"} | ${scenario.passed ? "PASS" : "FAIL"} |`);
  }
  lines.push("");
  lines.push("## Rotation and isolation");
  lines.push("");
  lines.push(`- Portrait-landscape-portrait: ${report.rotation && report.rotation.passed ? "PASS" : "FAIL"}.`);
  for (const item of report.isolation) {
    lines.push(`- ${item.name}: ${item.passed ? "PASS" : "FAIL"}.`);
  }
  lines.push("");
  lines.push("## Hard failures");
  lines.push("");
  if (!report.hardFailures.length) lines.push("None.");
  for (const item of report.hardFailures) {
    const context = item.context && Object.keys(item.context).length
      ? ` (${Object.entries(item.context).map(([key, value]) => `${key}=${value}`).join(", ")})`
      : "";
    lines.push(`- \`${item.code}\`${context}: ${item.message}`);
  }
  lines.push("");
  lines.push("## Warnings");
  lines.push("");
  if (!report.warnings.length) lines.push("None.");
  for (const item of report.warnings) {
    const context = item.context && Object.keys(item.context).length
      ? ` (${Object.entries(item.context).map(([key, value]) => `${key}=${value}`).join(", ")})`
      : "";
    lines.push(`- \`${item.code}\`${context}: ${item.message}`);
  }
  lines.push("");
  lines.push("## Totals");
  lines.push("");
  for (const [key, value] of Object.entries(report.totals || {})) lines.push(`- ${key}: ${value}`);
  lines.push("");
  lines.push(`Screenshots: \`${path.relative(OUTPUT_DIR, SCREENSHOT_DIR) || "screenshots"}/\``);
  lines.push("");
  return `${lines.join("\n")}\n`;
}

async function writeReports() {
  await mkdir(SCREENSHOT_DIR, { recursive: true });
  report.finishedAt = new Date().toISOString();
  report.totals = summarizeTotals();
  await writeFile(
    path.join(OUTPUT_DIR, "summary.json"),
    `${JSON.stringify(report, null, 2)}\n`,
    "utf8"
  );
  await writeFile(path.join(OUTPUT_DIR, "summary.md"), markdownReport(), "utf8");
}

let browser;
let context;
let page;

try {
  await mkdir(SCREENSHOT_DIR, { recursive: true });
  await auditSourcePrivacyContract();
  await auditLeadContextSourceContract();
  browser = await chromium.launch({ headless: true });
  context = await browser.newContext({
    viewport: { width: 375, height: 812 },
    reducedMotion: "reduce",
    locale: "he-IL"
  });
  page = await context.newPage();
  page.on("pageerror", (error) => {
    const message = safeError(error);
    report.runtime.pageErrors.push(message);
    if (/showroom-engine|engine\.js|nl-unit|nadlan/i.test(message)) {
      hard("runtime.pageerror", "An uncaught first-party page error occurred.", {}, { error: message });
    } else {
      warn("runtime.third-party-pageerror", "An uncaught error occurred outside an identified showroom stack.", {}, {
        error: message
      });
    }
  });
  page.on("console", (entry) => {
    if (entry.type() !== "error") return;
    const message = redact(entry.text());
    report.runtime.consoleErrors.push(message);
    if (/showroom-engine|engine\.js|nl-unit|nadlan/i.test(message)) {
      hard("runtime.console-error", "A first-party console error occurred.", {}, { error: message });
    } else {
      warn("runtime.third-party-console", "A console error occurred outside an identified showroom stack.", {}, {
        error: message
      });
    }
  });

  await auditPasswordGate(page);
  await unlockSandbox(page);
  const targetContext = await privateTargetContext(page);
  await auditPostUnlockCacheGate(browser);
  await auditPrivateStorageIsolation(page);
  await auditAnonymousDiscovery(browser, targetContext);
  await auditUnlockedLeadCookieBridge(page, targetContext);

  let scenarioIndex = 0;
  for (const viewport of VIEWPORTS) {
    for (const language of LANGUAGES) {
      try {
        await runScenario(page, viewport, language, scenarioIndex);
      } catch (error) {
        hard("matrix.exception", "A viewport/language scenario raised an exception.", {
          viewport: viewport.name,
          language
        }, { error: safeError(error) });
        report.matrix.push({
          viewport: viewport.name,
          width: viewport.width,
          height: viewport.height,
          language,
          passed: false,
          error: safeError(error),
          tools: []
        });
      }
      scenarioIndex += 1;
    }

    try {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(urlForLanguage("he"), { waitUntil: "domcontentloaded", timeout: 45_000 });
      await waitForJourney(page);
      await selectFirstInventoryUnit(page, "enter", {
        viewport: viewport.name,
        language: "he",
        probe: "pre-hotspot-keyboard"
      });
      await tryHotspotSelection(page, viewport);
    } catch (error) {
      warn("selection.hotspot-probe-exception", "The optional hotspot probe could not complete.", {
        viewport: viewport.name
      }, { error: safeError(error) });
    }
  }

  await runRotationProbe(page);
  await auditSiblingIsolation(context);
} catch (error) {
  hard("runner.fatal", "The QA runner stopped before completing every gate.", {}, {
    error: safeError(error)
  });
} finally {
  await page?.close().catch(() => {});
  await context?.close().catch(() => {});
  await browser?.close().catch(() => {});
  await writeReports();
}

const resultWord = report.hardFailures.length ? "FAIL" : "PASS";
console.log(`${resultWord}: ${report.hardFailures.length} hard failure(s), ${report.warnings.length} warning(s).`);
console.log(`Credential-free reports: ${path.join(OUTPUT_DIR, "summary.json")} and ${path.join(OUTPUT_DIR, "summary.md")}`);
process.exitCode = report.hardFailures.length ? 1 : 0;
