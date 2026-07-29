#!/usr/bin/env node

import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const root = process.cwd();
const baseCommit = "8a0bec48cd8666bee978660a33592bf74015e4bd";
const enginePath = "plugins/nadlan-config/assets/showroom-engine/engine.js";
const sharedStylePaths = [
  "plugins/nadlan-config/assets/showroom-engine/showroom.css",
  "plugins/nadlan-config/assets/showroom-engine/editorial.css"
];
const utopiaStylePath = "plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia.css";
const previewPath = "docs/previews/utopia-sde-dov-he-preview.html";
const outputPath = path.join(root, "docs", "qa", "utopia-shared-engine-isolation-report.json");
const fixtures = [
  "duo-tel-aviv",
  "rainbow-tel-aviv",
  "dimri-yama-sde-dov",
  "ashira-sde-dov",
  "first-sde-dov",
  "zohi-sde-dov",
  "gindi-vogue-sde-dov",
  "migdalei-hayam-sde-dov",
  "shikun-binui-sde-dov",
  "einstein-tower",
  "einstein-19",
  "ashdar-einstein"
].map((slug) => ({
  slug,
  url: `https://nad-lan.co.il/projects/${slug}/`
}));

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function firstDifference(left, right) {
  const length = Math.min(left.length, right.length);
  for (let index = 0; index < length; index += 1) {
    if (left[index] !== right[index]) {
      return {
        index,
        baseline: left.slice(Math.max(0, index - 120), index + 240),
        current: right.slice(Math.max(0, index - 120), index + 240)
      };
    }
  }
  return left.length === right.length
    ? null
    : {
      index: length,
      baseline: left.slice(Math.max(0, length - 120), length + 240),
      current: right.slice(Math.max(0, length - 120), length + 240)
    };
}

function gitBlob(relativePath) {
  return execFileSync(
    "git",
    ["show", `${baseCommit}:${relativePath}`],
    { cwd: root, encoding: "utf8", maxBuffer: 20 * 1024 * 1024 }
  );
}

function baselineBlobId(relativePath) {
  return execFileSync(
    "git",
    ["rev-parse", `${baseCommit}:${relativePath}`],
    { cwd: root, encoding: "utf8" }
  ).trim();
}

function workingTreeBlobId(relativePath) {
  return execFileSync(
    "git",
    ["hash-object", "--path", relativePath, relativePath],
    { cwd: root, encoding: "utf8" }
  ).trim();
}

function read(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

function parsePreviewPayload() {
  const html = read(previewPath);
  const marker = "window.NADLAN_SHOWROOM=";
  const start = html.indexOf(marker);
  const endMarker = ';</script><script src="/plugins/nadlan-config/assets/showroom-engine/engine.js"';
  const end = html.indexOf(endMarker, start);
  if (start < 0 || end < 0) {
    throw new Error(`Could not extract NADLAN_SHOWROOM from ${previewPath}`);
  }
  return JSON.parse(html.slice(start + marker.length, end));
}

async function captureLivePayload(context, fixture) {
  const page = await context.newPage();
  try {
    const response = await page.goto(fixture.url, {
      waitUntil: "domcontentloaded",
      timeout: 60000
    });
    await page.waitForFunction(
      () => Boolean(window.NADLAN_SHOWROOM && window.NADLAN_I18N),
      null,
      { timeout: 30000 }
    );
    const captured = await page.evaluate(() => ({
      payload: JSON.parse(JSON.stringify(window.NADLAN_SHOWROOM)),
      i18n: JSON.parse(JSON.stringify(window.NADLAN_I18N)),
      sourceTitle: document.title
    }));
    return {
      ...captured,
      status: response ? response.status() : null
    };
  } finally {
    await page.close();
  }
}

async function evaluateUtopiaI18n(browser) {
  const context = await browser.newContext();
  const page = await context.newPage();
  try {
    await page.setContent("<!doctype html><html><body></body></html>");
    await page.addScriptTag({
      content: read("plugins/nadlan-config/assets/showroom-engine/i18n.js")
    });
    await page.addScriptTag({
      content: read("plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-i18n.js")
    });
    return await page.evaluate(() => JSON.parse(JSON.stringify(window.NADLAN_I18N)));
  } finally {
    await context.close();
  }
}

async function renderEngine(browser, {
  engine,
  payload,
  i18n,
  pageKind = "project",
  query = "",
  seedTitle = "Compatibility fixture"
}) {
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];

  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => pageErrors.push(error.message));
  await page.route("**/*", async (route) => {
    if (route.request().isNavigationRequest()) {
      await route.fulfill({
        status: 200,
        contentType: "text/html; charset=utf-8",
        body: `<!doctype html><html lang="he" dir="rtl"><head><title>${seedTitle}</title></head><body><div id="nl-root" data-page="${pageKind}"></div></body></html>`
      });
      return;
    }
    await route.fulfill({ status: 204, body: "" });
  });

  try {
    await page.goto(`https://qa.nad-lan.local/${query}`, {
      waitUntil: "domcontentloaded",
      timeout: 30000
    });
    await page.evaluate(
      ({ showroom, translations }) => {
        window.NADLAN_SHOWROOM = showroom;
        window.NADLAN_I18N = translations;
      },
      { showroom: payload, translations: i18n }
    );
    await page.addScriptTag({ content: engine });
    await page.waitForSelector("#nl-root.nl-app");
    await page.waitForTimeout(100);
    const result = await page.evaluate(() => {
      const rootNode = document.querySelector("#nl-root");
      return {
        html: rootNode?.outerHTML || "",
        rootClass: rootNode?.className || "",
        documentLang: document.documentElement.lang,
        documentDir: document.documentElement.dir,
        documentTitle: document.title,
        h1Count: document.querySelectorAll("#nl-root h1").length,
        unitCards: document.querySelectorAll("#nl-root .nl-ucard").length,
        unitHotspots: document.querySelectorAll("#nl-root [data-act=\"select\"]").length,
        buildingHotspots: document.querySelectorAll("#nl-root [data-act=\"building\"]").length,
        buildingHotspotLabels: [...document.querySelectorAll("#nl-root [data-act=\"building\"]")]
          .map((node) => node.textContent.trim()),
        buildingHotspotAriaLabels: [...document.querySelectorAll("#nl-root [data-act=\"building\"]")]
          .map((node) => node.getAttribute("aria-label")),
        studioLaunches: document.querySelectorAll("#nl-root .nl-studio-launch").length,
        brandHrefs: [...document.querySelectorAll("#nl-root .nl-brand[href]")]
          .map((anchor) => anchor.getAttribute("href")),
        templateRelativeLinks: [...document.querySelectorAll("#nl-root a[href]")]
          .map((anchor) => anchor.getAttribute("href"))
          .filter((href) => /(?:^|\/)(?:home|project)\.html(?:[?#]|$)/i.test(href || ""))
      };
    });
    return { ...result, consoleErrors, pageErrors };
  } finally {
    await context.close();
  }
}

function comparableResult(result) {
  const { html, ...rest } = result;
  return {
    ...rest,
    domSha256: sha256(html)
  };
}

function compareRenders(baseline, current) {
  const scalarKeys = [
    "rootClass",
    "documentLang",
    "documentDir",
    "documentTitle",
    "h1Count",
    "unitCards",
    "unitHotspots",
    "buildingHotspots",
    "studioLaunches"
  ];
  const scalarParity = Object.fromEntries(
    scalarKeys.map((key) => [key, baseline[key] === current[key]])
  );
  const exactDomParity = baseline.html === current.html;
  return {
    exactDomParity,
    scalarParity,
    baseline: comparableResult(baseline),
    current: comparableResult(current),
    firstDifference: exactDomParity ? null : firstDifference(baseline.html, current.html),
    pass:
      exactDomParity &&
      Object.values(scalarParity).every(Boolean) &&
      baseline.consoleErrors.length === 0 &&
      baseline.pageErrors.length === 0 &&
      current.consoleErrors.length === 0 &&
      current.pageErrors.length === 0
  };
}

const baselineEngine = gitBlob(enginePath);
const currentEngine = read(enginePath);
const browser = await chromium.launch({ channel: "chrome", headless: true });
const liveContext = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
await liveContext.route("**/*", async (route) => {
  if (["image", "media", "font"].includes(route.request().resourceType())) {
    await route.abort("blockedbyclient");
    return;
  }
  await route.continue();
});

const report = {
  schema: "nadlan-utopia-shared-engine-isolation/v2",
  generatedAt: new Date().toISOString(),
  baseCommit,
  baselineEngineSha256: sha256(baselineEngine),
  currentEngineSha256: sha256(currentEngine),
  nonUtopiaFixtures: [],
  galleryParity: null,
  utopiaLanguageLock: null,
  cssIsolation: null,
  summary: null,
  pass: false
};

try {
  for (const fixture of fixtures) {
    const live = await captureLivePayload(liveContext, fixture);
    const project = live.payload.projects[live.payload.config.default_project];
    const baseline = await renderEngine(browser, {
      engine: baselineEngine,
      payload: live.payload,
      i18n: live.i18n
    });
    const current = await renderEngine(browser, {
      engine: currentEngine,
      payload: live.payload,
      i18n: live.i18n
    });
    const comparison = compareRenders(baseline, current);
    const row = {
      slug: fixture.slug,
      sourceUrl: fixture.url,
      sourceStatus: live.status,
      defaultProject: live.payload.config.default_project,
      units: Array.isArray(project?.units) ? project.units.length : null,
      studioSetting: live.payload.config.studio,
      ...comparison
    };
    report.nonUtopiaFixtures.push(row);
    console.log(
      `${row.pass ? "PASS" : "FAIL"} exact DOM parity ${row.slug} (${row.units} units, ${row.current.studioLaunches} Studio launch)`
    );
  }

  const utopiaPayload = parsePreviewPayload();
  const utopiaI18n = await evaluateUtopiaI18n(browser);
  const galleryBaseline = await renderEngine(browser, {
    engine: baselineEngine,
    payload: utopiaPayload,
    i18n: utopiaI18n,
    pageKind: "home",
    query: "?lang=fr",
    seedTitle: "WordPress gallery fixture"
  });
  const galleryCurrent = await renderEngine(browser, {
    engine: currentEngine,
    payload: utopiaPayload,
    i18n: utopiaI18n,
    pageKind: "home",
    query: "?lang=fr",
    seedTitle: "WordPress gallery fixture"
  });
  report.galleryParity = compareRenders(galleryBaseline, galleryCurrent);
  console.log(
    `${report.galleryParity.pass ? "PASS" : "FAIL"} exact DOM parity UTOPIA payload on shared home gallery`
  );

  const configuredLanguage = utopiaPayload.config.default_lang;
  const conflictingLanguage = configuredLanguage === "fr" ? "he" : "fr";
  const languageLockRender = await renderEngine(browser, {
    engine: currentEngine,
    payload: utopiaPayload,
    i18n: utopiaI18n,
    pageKind: "project",
    query: `?lang=${conflictingLanguage}`,
    seedTitle: "Server-owned UTOPIA SEO title"
  });
  report.utopiaLanguageLock = {
    configuredLanguage,
    conflictingLanguage,
    documentLang: languageLockRender.documentLang,
    documentDir: languageLockRender.documentDir,
    documentTitle: languageLockRender.documentTitle,
    rootClass: languageLockRender.rootClass,
    buildingHotspotLabels: languageLockRender.buildingHotspotLabels,
    buildingHotspotAriaLabels: languageLockRender.buildingHotspotAriaLabels,
    consoleErrors: languageLockRender.consoleErrors,
    pageErrors: languageLockRender.pageErrors,
    pass:
      languageLockRender.documentLang === configuredLanguage &&
      languageLockRender.documentTitle === "Server-owned UTOPIA SEO title" &&
      languageLockRender.rootClass.split(/\s+/).includes("nl-app--building") &&
      JSON.stringify(languageLockRender.buildingHotspotLabels) === JSON.stringify(["S1", "N1", "N2", "S2"]) &&
      languageLockRender.consoleErrors.length === 0 &&
      languageLockRender.pageErrors.length === 0
  };
  console.log(
    `${report.utopiaLanguageLock.pass ? "PASS" : "FAIL"} UTOPIA server-language lock against ?lang=${conflictingLanguage}`
  );

  const sharedStyles = sharedStylePaths.map((relativePath) => {
    const baselineGitBlob = baselineBlobId(relativePath);
    const currentGitBlob = workingTreeBlobId(relativePath);
    return {
      path: relativePath,
      exactBaseBlob: baselineGitBlob === currentGitBlob,
      baselineGitBlob,
      currentGitBlob
    };
  });
  const shortcodeSource = read("plugins/nadlan-config/inc/showroom-engine.php");
  report.cssIsolation = {
    sharedStyles,
    utopiaStyle: {
      path: utopiaStylePath,
      exists: fs.existsSync(path.join(root, utopiaStylePath)),
      sha256: fs.existsSync(path.join(root, utopiaStylePath)) ? sha256(read(utopiaStylePath)) : null
    },
    conditionalEnqueuePresent:
      /if\s*\(\s*\$is_utopia_family\s*\)\s*\{[\s\S]*?wp_enqueue_style\s*\([\s\S]*?utopia\.css/.test(shortcodeSource),
    pass:
      sharedStyles.every((style) => style.exactBaseBlob) &&
      fs.existsSync(path.join(root, utopiaStylePath)) &&
      /if\s*\(\s*\$is_utopia_family\s*\)\s*\{[\s\S]*?wp_enqueue_style\s*\([\s\S]*?utopia\.css/.test(shortcodeSource)
  };
  console.log(
    `${report.cssIsolation.pass ? "PASS" : "FAIL"} shared CSS byte parity and UTOPIA-only enqueue`
  );

  const nonUtopiaPassed = report.nonUtopiaFixtures.filter((fixture) => fixture.pass).length;
  const zeroUnitFixtures = report.nonUtopiaFixtures.filter((fixture) => fixture.units === 0);
  const zeroUnitStudioParity = zeroUnitFixtures.every(
    (fixture) =>
      fixture.baseline.studioLaunches === fixture.current.studioLaunches &&
      (fixture.studioSetting === "off" || fixture.current.studioLaunches === 1)
  );
  report.summary = {
    totalNonUtopiaFixtures: report.nonUtopiaFixtures.length,
    passedNonUtopiaFixtures: nonUtopiaPassed,
    failedNonUtopiaFixtures: report.nonUtopiaFixtures.length - nonUtopiaPassed,
    zeroUnitFixtures: zeroUnitFixtures.map((fixture) => fixture.slug),
    zeroUnitStudioParity,
    galleryExactDomParity: report.galleryParity.exactDomParity,
    utopiaLanguageLock: report.utopiaLanguageLock.pass,
    sharedCssByteParity: report.cssIsolation.sharedStyles.every((style) => style.exactBaseBlob)
  };
  report.pass =
    nonUtopiaPassed === report.nonUtopiaFixtures.length &&
    zeroUnitStudioParity &&
    report.galleryParity.pass &&
    report.utopiaLanguageLock.pass &&
    report.cssIsolation.pass;
} finally {
  await liveContext.close();
  await browser.close();
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ pass: report.pass, summary: report.summary, report: outputPath }, null, 2));
process.exit(report.pass ? 0 : 1);
