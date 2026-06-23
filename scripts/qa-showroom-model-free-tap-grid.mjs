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

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-model-free-tap-grid-2026-06-24';
const url = process.argv[3] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=free_tap_grid';

const points = [
  { name: 'tower-upper-left', x: 0.38, y: 0.30 },
  { name: 'tower-upper-center', x: 0.50, y: 0.31 },
  { name: 'tower-upper-right', x: 0.64, y: 0.34 },
  { name: 'tower-mid-left', x: 0.36, y: 0.48 },
  { name: 'tower-mid-center', x: 0.50, y: 0.50 },
  { name: 'tower-mid-right', x: 0.66, y: 0.50 },
  { name: 'podium-left', x: 0.27, y: 0.68 },
  { name: 'podium-center', x: 0.43, y: 0.69 },
  { name: 'podium-right', x: 0.61, y: 0.66 },
];

async function runPoint(browser, point) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 900 },
    deviceScaleFactor: 1,
    isMobile: true,
    hasTouch: true,
    locale: 'he-IL',
  });
  const page = await context.newPage();
  await page.goto(`${url}&point=${point.name}&t=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForSelector('.nlp3d-premium', { timeout: 30000 });
  await page.waitForTimeout(2500);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  const tap = await page.evaluate((pt) => {
    const scene = document.querySelector('.nlp3d-scene');
    const root = document.querySelector('.nlp3d');
    const r = scene.getBoundingClientRect();
    const x = r.left + r.width * pt.x;
    const y = r.top + r.height * pt.y;
    const at = document.elementFromPoint(x, y);
    return {
      x,
      y,
      sceneRect: {
        x: r.x,
        y: r.y,
        width: r.width,
        height: r.height,
      },
      beforeActiveUnit: root ? root.getAttribute('data-active-unit') : null,
      elementAtPoint: at ? {
        tag: at.tagName,
        className: String(at.className || '').slice(0, 140),
        markerUnit: at.closest && at.closest('.nlp3d-stage-pick') ? at.closest('.nlp3d-stage-pick').getAttribute('data-unit') : null,
        insideModelViewer: !!(at.closest && at.closest('model-viewer')),
      } : null,
    };
  }, point);
  await page.screenshot({ path: path.join(outDir, `mobile-390-before-${point.name}.png`), fullPage: false });
  await page.touchscreen.tap(tap.x, tap.y);
  await page.waitForTimeout(800);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(outDir, `mobile-390-after-${point.name}.png`), fullPage: false });
  const after = await page.evaluate(() => {
    const root = document.querySelector('.nlp3d');
    const mv = document.querySelector('model-viewer');
    return {
      activeUnit: root ? root.getAttribute('data-active-unit') : null,
      activeText: (document.querySelector('.nlp3d-stage-card')?.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 220),
      cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
      cameraTarget: mv ? mv.getAttribute('camera-target') : null,
    };
  });
  await context.close();
  return {
    point,
    tap,
    after,
    selected: !!after.activeUnit,
    modelSurfaceTap: !!(tap.elementAtPoint && tap.elementAtPoint.insideModelViewer && !tap.elementAtPoint.markerUnit),
  };
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = {
  createdAt: new Date().toISOString(),
  url,
  viewport: { width: 390, height: 900 },
  points: [],
};
for (const point of points) {
  results.points.push(await runPoint(browser, point));
}
await browser.close();
results.deadModelSurfacePoints = results.points.filter((item) => item.modelSurfaceTap && !item.selected).map((item) => item.point.name);
results.markerTapPoints = results.points.filter((item) => item.tap.elementAtPoint && item.tap.elementAtPoint.markerUnit).map((item) => ({
  point: item.point.name,
  markerUnit: item.tap.elementAtPoint.markerUnit,
}));
await fs.writeFile(path.join(outDir, 'showroom-model-free-tap-grid-report.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
