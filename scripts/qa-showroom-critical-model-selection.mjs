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

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-critical-model-selection-2026-06-24';
const url = process.argv[3] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=critical_model_selection';

const surfacePoints = [
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

async function state(page) {
  return page.evaluate(() => {
    const root = document.querySelector('.nlp3d');
    const mv = document.querySelector('model-viewer');
    const card = document.querySelector('.nlp3d-stage-card');
    return {
      activeUnit: root ? root.getAttribute('data-active-unit') : null,
      cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
      cameraTarget: mv ? mv.getAttribute('camera-target') : null,
      cardText: card ? card.innerText.replace(/\s+/g, ' ').trim().slice(0, 320) : '',
    };
  });
}

async function pageGeometry(page, point) {
  return page.evaluate((pt) => {
    const visible = (el) => {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' && Number(cs.opacity || 1) !== 0;
    };
    const scene = document.querySelector('.nlp3d-scene');
    const sceneRect = scene.getBoundingClientRect();
    const x = sceneRect.left + sceneRect.width * pt.x;
    const y = sceneRect.top + sceneRect.height * pt.y;
    const at = document.elementFromPoint(x, y);
    const markerAtPoint = at && at.closest ? at.closest('.nlp3d-stage-pick,.nlp3d-mv-hotspot') : null;
    const markers = Array.from(document.querySelectorAll('.nlp3d-model-picks .nlp3d-stage-pick')).filter(visible).map((el) => {
      const r = el.getBoundingClientRect();
      return {
        unit: el.getAttribute('data-unit') || '',
        rect: {
          left: r.left,
          right: r.right,
          top: r.top,
          bottom: r.bottom,
          width: r.width,
          height: r.height,
          centerX: r.left + r.width / 2,
          centerY: r.top + r.height / 2,
        },
      };
    });
    let expected = null;
    let bestScore = Infinity;
    const baseLimit = window.innerWidth && window.innerWidth <= 480 ? 92 : 76;
    markers.forEach((marker) => {
      const cx = marker.rect.centerX;
      const cy = marker.rect.centerY;
      const dx = x - cx;
      const dy = y - cy;
      const ax = Math.abs(dx);
      const ay = Math.abs(dy);
      const distance = Math.sqrt(dx * dx + dy * dy);
      const limit = Math.max(baseLimit, Math.min(104, Math.max(marker.rect.width, marker.rect.height) * 1.35));
      const score = ay * 3 + ax + distance * 0.12;
      if (distance <= limit && score < bestScore) {
        expected = marker.unit;
        bestScore = score;
      }
    });
    const resetUnit = markers.map((m) => m.unit).find((unit) => unit && unit !== expected) || markers[0]?.unit || '';
    const resetMarker = resetUnit ? markers.find((m) => m.unit === resetUnit) : null;
    return {
      point: pt,
      tap: { x, y },
      sceneRect: {
        left: sceneRect.left,
        top: sceneRect.top,
        width: sceneRect.width,
        height: sceneRect.height,
      },
      elementAtPoint: at ? {
        tag: at.tagName,
        className: String(at.className || '').slice(0, 160),
        insideModelViewer: !!(at.closest && at.closest('model-viewer')),
        markerUnit: markerAtPoint ? markerAtPoint.getAttribute('data-unit') : null,
      } : null,
      expectedNearestUnit: expected,
      resetUnit,
      resetMarker,
      markers,
    };
  }, point);
}

async function tap(page, x, y, isMobile) {
  if (isMobile) {
    await page.touchscreen.tap(x, y);
  } else {
    await page.mouse.click(x, y);
  }
}

async function resetTo(page, geometry, isMobile) {
  if (!geometry.resetMarker) {
    return null;
  }
  await tap(page, geometry.resetMarker.rect.centerX, geometry.resetMarker.rect.centerY, isMobile);
  await page.waitForTimeout(500);
  return state(page);
}

async function runViewport(browser, label, width, height) {
  const isMobile = width <= 480;
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    isMobile,
    hasTouch: isMobile,
    locale: 'he-IL',
  });
  const page = await context.newPage();
  await page.goto(`${url}&viewport=${label}&t=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForSelector('.nlp3d-premium', { timeout: 30000 });
  await page.waitForTimeout(2500);
  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(outDir, `${label}-before-critical-taps.png`), fullPage: false });

  const results = [];
  for (const point of surfacePoints) {
    await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
    await page.waitForTimeout(150);
    const geometry = await pageGeometry(page, point);
    const resetState = await resetTo(page, geometry, isMobile);
    await page.waitForTimeout(150);
    await tap(page, geometry.tap.x, geometry.tap.y, isMobile);
    await page.waitForTimeout(900);
    const after = await state(page);
    const rawModelTap = !!(geometry.elementAtPoint && geometry.elementAtPoint.insideModelViewer && !geometry.elementAtPoint.markerUnit);
    const expected = geometry.expectedNearestUnit;
    const pass = expected ? after.activeUnit === expected : after.activeUnit === (resetState && resetState.activeUnit);
    results.push({
      point,
      rawModelTap,
      elementAtPoint: geometry.elementAtPoint,
      expectedNearestUnit: expected,
      resetUnit: geometry.resetUnit,
      resetActiveUnit: resetState ? resetState.activeUnit : null,
      after,
      pass,
    });
    if (!pass || rawModelTap) {
      await page.screenshot({ path: path.join(outDir, `${label}-after-${point.name}.png`), fullPage: false });
    }
  }

  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(outDir, `${label}-after-critical-taps.png`), fullPage: false });
  await context.close();
  return {
    label,
    viewport: { width, height },
    results,
    failed: results.filter((item) => !item.pass),
    rawModelFailures: results.filter((item) => item.rawModelTap && !item.pass),
  };
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const report = {
  createdAt: new Date().toISOString(),
  url,
  desktop: await runViewport(browser, 'desktop-1440', 1440, 1000),
  mobile: await runViewport(browser, 'mobile-390', 390, 900),
};
await browser.close();
report.failed = [...report.desktop.failed.map((item) => ({ viewport: 'desktop-1440', ...item })), ...report.mobile.failed.map((item) => ({ viewport: 'mobile-390', ...item }))];
report.rawModelFailures = [...report.desktop.rawModelFailures.map((item) => ({ viewport: 'desktop-1440', ...item })), ...report.mobile.rawModelFailures.map((item) => ({ viewport: 'mobile-390', ...item }))];
await fs.writeFile(path.join(outDir, 'critical-model-selection-report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
