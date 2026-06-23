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

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-model-tap-2026-06-24';
const unitId = process.argv[3] || 'unit-38-penthouse';
const url = process.argv[4] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=model_tap';

async function inspect(page) {
  return page.evaluate(() => {
    const root = document.querySelector('.nlp3d');
    const mv = document.querySelector('model-viewer');
    const isVisible = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && Number(cs.opacity || 1) !== 0;
    };
    return {
      url: location.href,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body ? document.body.scrollWidth : null,
      rootActiveUnit: root ? root.getAttribute('data-active-unit') : null,
      activePicks: Array.from(document.querySelectorAll('.nlp3d-stage-pick.is-active, .nlp3d-stage-pick[aria-pressed="true"]')).map((el) => el.getAttribute('data-unit')),
      visibleStagePins: Array.from(document.querySelectorAll('.nlp3d-model-picks .nlp3d-stage-pick')).filter(isVisible).map((el) => el.getAttribute('data-unit')),
      visibleModelHotspots: Array.from(document.querySelectorAll('.nlp3d-mv-hotspot')).filter(isVisible).map((el) => el.getAttribute('data-unit')),
      cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
      cameraTarget: mv ? mv.getAttribute('camera-target') : null,
      stageCardHidden: document.querySelector('.nlp3d-stage-card') ? document.querySelector('.nlp3d-stage-card').hidden : null,
      stageCardText: document.querySelector('.nlp3d-stage-card') ? document.querySelector('.nlp3d-stage-card').innerText.replace(/\s+/g, ' ').trim().slice(0, 500) : '',
    };
  });
}

async function modelSurfacePoint(page, unitId) {
  return page.locator(`.nlp3d-model-picks .nlp3d-stage-pick[data-unit="${unitId}"]`).evaluate((el) => {
    const r = el.getBoundingClientRect();
    const scene = document.querySelector('.nlp3d-scene').getBoundingClientRect();
    const offset = window.innerWidth <= 480 ? 24 : 34;
    const x = Math.min(scene.right - 8, r.right + offset);
    const y = r.top + r.height / 2;
    const at = document.elementFromPoint(x, y);
    return {
      x,
      y,
      unitRect: { x: r.x, y: r.y, right: r.right, bottom: r.bottom, width: r.width, height: r.height },
      sceneRect: { x: scene.x, y: scene.y, right: scene.right, bottom: scene.bottom, width: scene.width, height: scene.height },
      elementAtPoint: at ? {
        tag: at.tagName,
        className: String(at.className || '').slice(0, 160),
        insideStagePick: !!(at.closest && at.closest('.nlp3d-stage-pick')),
        insideModelViewer: !!(at.closest && at.closest('model-viewer')),
      } : null,
    };
  });
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
  await page.goto(`${url}&viewport=${label}&t=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForSelector('.nlp3d-premium', { timeout: 30000 });
  await page.waitForTimeout(2500);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, `${label}-before-model-surface-tap.png`), fullPage: false });

  const point = await modelSurfacePoint(page, unitId);
  if (point.elementAtPoint && point.elementAtPoint.insideStagePick) {
    throw new Error(`${label}: computed tap point still lands inside a stage marker`);
  }
  if (width <= 480) {
    await page.touchscreen.tap(point.x, point.y);
  } else {
    await page.mouse.click(point.x, point.y);
  }
  await page.waitForTimeout(1200);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(outDir, `${label}-after-model-surface-tap-${unitId}.png`), fullPage: false });

  const state = await inspect(page);
  state.tapPoint = point;
  state.expectedUnit = unitId;
  state.pass = state.rootActiveUnit === unitId && state.activePicks.includes(unitId);
  await fs.writeFile(path.join(outDir, `${label}-model-tap-report.json`), JSON.stringify(state, null, 2));
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
await fs.writeFile(path.join(outDir, 'showroom-model-tap-report.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
