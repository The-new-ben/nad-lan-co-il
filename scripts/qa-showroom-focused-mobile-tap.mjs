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

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-focused-mobile-tap-2026-06-24';
const url = process.argv[3] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=focused_mobile_tap';
const pointName = process.argv[4] || 'tower-upper-center';
const xRatio = Number(process.argv[5] || 0.5);
const yRatio = Number(process.argv[6] || 0.31);

async function inspect(page) {
  return page.evaluate(() => {
    const root = document.querySelector('.nlp3d');
    const mv = document.querySelector('model-viewer');
    const card = document.querySelector('.nlp3d-stage-card');
    const modelRect = mv ? mv.getBoundingClientRect() : null;
    return {
      activeUnit: root ? root.getAttribute('data-active-unit') : null,
      cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
      cameraTarget: mv ? mv.getAttribute('camera-target') : null,
      stageCardHidden: card ? card.hidden : null,
      modelRect: modelRect ? {
        x: Math.round(modelRect.x),
        y: Math.round(modelRect.y),
        width: Math.round(modelRect.width),
        height: Math.round(modelRect.height),
      } : null,
      selectedMarker: document.querySelector('.nlp3d-stage-pick.is-active, .nlp3d-stage-pick[aria-pressed="true"]')?.getAttribute('data-unit') || null,
    };
  });
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 900 },
  deviceScaleFactor: 1,
  isMobile: true,
  hasTouch: true,
  locale: 'he-IL',
});
const page = await context.newPage();
const result = {
  createdAt: new Date().toISOString(),
  url,
  point: { name: pointName, x: xRatio, y: yRatio },
  snapshots: [],
};

await page.goto(`${url}&point=${encodeURIComponent(pointName)}&t=${Date.now()}`, {
  waitUntil: 'domcontentloaded',
  timeout: 60000,
});
await page.waitForSelector('.nlp3d-premium model-viewer', { timeout: 45000 });
await page.waitForTimeout(2500);
await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
await page.waitForTimeout(500);

const tap = await page.evaluate(({ xRatio, yRatio }) => {
  const scene = document.querySelector('.nlp3d-scene');
  const r = scene.getBoundingClientRect();
  const x = r.left + r.width * xRatio;
  const y = r.top + r.height * yRatio;
  const at = document.elementFromPoint(x, y);
  return {
    x,
    y,
    sceneRect: {
      x: Math.round(r.x),
      y: Math.round(r.y),
      width: Math.round(r.width),
      height: Math.round(r.height),
    },
    elementAtPoint: at ? {
      tag: at.tagName,
      className: String(at.className || '').slice(0, 140),
      markerUnit: at.closest && at.closest('.nlp3d-stage-pick') ? at.closest('.nlp3d-stage-pick').getAttribute('data-unit') : null,
      insideModelViewer: !!(at.closest && at.closest('model-viewer')),
    } : null,
  };
}, { xRatio, yRatio });
result.tap = tap;

await page.screenshot({ path: path.join(outDir, `mobile-390-before-${pointName}.png`), fullPage: false });
await page.touchscreen.tap(tap.x, tap.y);

for (const wait of [800, 2500, 5000]) {
  await page.waitForTimeout(wait);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(250);
  const screenshot = `mobile-390-after-${pointName}-${wait}ms.png`;
  await page.screenshot({ path: path.join(outDir, screenshot), fullPage: false });
  result.snapshots.push({
    wait,
    screenshot,
    state: await inspect(page),
  });
}

await context.close();
await browser.close();
await fs.writeFile(path.join(outDir, 'focused-mobile-tap-report.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
