import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const playwrightPackage = require.resolve('playwright', {
  paths: [process.cwd(), process.env.PLAYWRIGHT_NODE_PATH].filter(Boolean),
});
const playwright = await import(pathToFileURL(playwrightPackage).href);
const chromium = playwright.chromium || (playwright.default && playwright.default.chromium);
if (!chromium) {
  throw new Error('Unable to load Playwright chromium launcher');
}

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-live-premium-pass-2026-06-24';
const unitId = process.argv[3] || 'unit-38-penthouse';
const url = process.argv[4] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=showroom_live';

const forbidden = [
  'Lovable',
  'Codex',
  'Claude',
  'prompt',
  'token',
  'war room',
  'money page',
  'KD',
  'CRM',
  'UTM',
  'Sponsored',
  'Featured',
  'Promoted',
  'Tailwind',
  'shadcn',
];

async function inspect(page) {
  return page.evaluate((badWords) => {
    const root = document.querySelector('.nlp3d');
    const mv = document.querySelector('model-viewer');
    const text = (document.body && document.body.innerText || '').slice(0, 50000);
    const visibleText = (sel) => {
      const node = document.querySelector(sel);
      return node ? node.innerText.replace(/\s+/g, ' ').trim() : '';
    };
    const offenders = Array.from(document.querySelectorAll('body *')).slice(0, 4000).map((el) => {
      const r = el.getBoundingClientRect();
      return {
        tag: el.tagName,
        cls: String(el.className || '').slice(0, 120),
        x: Math.round(r.x),
        right: Math.round(r.right),
        width: Math.round(r.width),
        text: (el.innerText || '').replace(/\s+/g, ' ').slice(0, 80),
      };
    }).filter((o) => o.width > 0 && (o.x < -1 || o.right > window.innerWidth + 1)).slice(0, 20);

    const tapTargets = Array.from(document.querySelectorAll('.nlp3d button, .nlp3d a, .nlp3d [role="button"]')).map((el) => {
      const r = el.getBoundingClientRect();
      return {
        tag: el.tagName,
        cls: String(el.className || '').slice(0, 100),
        unit: el.getAttribute('data-unit') || '',
        width: Math.round(r.width),
        height: Math.round(r.height),
        visible: r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden' && getComputedStyle(el).display !== 'none',
      };
    }).filter((o) => o.visible && (o.width < 44 || o.height < 44)).slice(0, 30);

    return {
      url: location.href,
      title: document.title,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body ? document.body.scrollWidth : null,
      hasRoot: !!root,
      rootClasses: root ? root.className : null,
      rootActiveUnit: root ? root.getAttribute('data-active-unit') : null,
      modelViewerCount: document.querySelectorAll('model-viewer').length,
      modelPickCount: document.querySelectorAll('.nlp3d-model-picks .nlp3d-stage-pick').length,
      activePicks: Array.from(document.querySelectorAll('.nlp3d-stage-pick.is-active, .nlp3d-stage-pick[aria-pressed="true"]')).map((el) => el.getAttribute('data-unit')),
      cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
      cameraTarget: mv ? mv.getAttribute('camera-target') : null,
      dockText: visibleText('.nlp3d-selection-dock'),
      stageText: visibleText('.nlp3d-stage-card'),
      detailTitle: visibleText('.nlp3d-selected-title'),
      publicLeakSample: badWords.find((word) => text.includes(word)) || null,
      offenders,
      smallTapTargets: tapTargets,
    };
  }, forbidden);
}

async function runViewport(browser, label, width, height) {
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    isMobile: width <= 480,
    hasTouch: width <= 480,
    locale: 'he-IL',
  });
  const page = await context.newPage();
  await page.goto(url + '&viewport=' + label + '&t=' + Date.now(), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForSelector('.nlp3d-premium', { timeout: 30000 });
  await page.waitForTimeout(2500);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, `${label}-before-click.png`), fullPage: false });

  const target = page.locator(`.nlp3d-model-picks .nlp3d-stage-pick[data-unit="${unitId}"]`);
  const targetCount = await target.count();
  if (targetCount !== 1) {
    const state = await inspect(page);
    state.clickError = `Expected one ${unitId} target, found ${targetCount}`;
    await fs.writeFile(path.join(outDir, `${label}-report.json`), JSON.stringify(state, null, 2));
    await context.close();
    return state;
  }

  await target.click({ timeout: 15000 });
  await page.waitForTimeout(1000);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, `${label}-after-click-${unitId}.png`), fullPage: false });

  const state = await inspect(page);
  await fs.writeFile(path.join(outDir, `${label}-report.json`), JSON.stringify(state, null, 2));
  await context.close();
  return state;
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = {
  createdAt: new Date().toISOString(),
  unitId,
  url,
  desktop: await runViewport(browser, 'desktop-1440', 1440, 1000),
  mobile: await runViewport(browser, 'mobile-390', 390, 900),
};
await browser.close();
await fs.writeFile(path.join(outDir, 'showroom-live-qa-report.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
