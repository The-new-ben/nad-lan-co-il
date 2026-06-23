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

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-marker-hit-test-2026-06-24';
const url = process.argv[3] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=marker_hit_test';

async function markerState(page) {
  return page.evaluate(() => {
    const markerNodes = Array.from(document.querySelectorAll('.nlp3d-model-picks .nlp3d-stage-pick'));
    return markerNodes.map((el) => {
      const r = el.getBoundingClientRect();
      const x = r.left + r.width / 2;
      const y = r.top + r.height / 2;
      const top = document.elementFromPoint(x, y);
      const topMarker = top && top.closest ? top.closest('.nlp3d-stage-pick') : null;
      return {
        unit: el.getAttribute('data-unit') || '',
        text: (el.innerText || '').replace(/\s+/g, ' ').trim(),
        rect: {
          x: Math.round(r.x),
          y: Math.round(r.y),
          width: Math.round(r.width),
          height: Math.round(r.height),
          centerX: Math.round(x),
          centerY: Math.round(y),
        },
        topAtCenter: top ? {
          tag: top.tagName,
          className: String(top.className || '').slice(0, 120),
          markerUnit: topMarker ? topMarker.getAttribute('data-unit') : null,
        } : null,
        centerHitsSelf: !!(topMarker && topMarker === el),
      };
    });
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
  await page.screenshot({ path: path.join(outDir, `${label}-before-marker-taps.png`), fullPage: false });

  const before = await markerState(page);
  const taps = [];
  for (const marker of before) {
    if (!marker.unit) {
      continue;
    }
    if (width <= 480) {
      await page.touchscreen.tap(marker.rect.centerX, marker.rect.centerY);
    } else {
      await page.mouse.click(marker.rect.centerX, marker.rect.centerY);
    }
    await page.waitForTimeout(450);
    const after = await page.evaluate(() => {
      const root = document.querySelector('.nlp3d');
      const mv = document.querySelector('model-viewer');
      return {
        activeUnit: root ? root.getAttribute('data-active-unit') : null,
        cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
        cameraTarget: mv ? mv.getAttribute('camera-target') : null,
      };
    });
    taps.push({
      expectedUnit: marker.unit,
      topAtCenter: marker.topAtCenter,
      centerHitsSelf: marker.centerHitsSelf,
      selectedUnit: after.activeUnit,
      cameraOrbit: after.cameraOrbit,
      cameraTarget: after.cameraTarget,
      pass: marker.centerHitsSelf && after.activeUnit === marker.unit,
    });
  }

  await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
  await page.waitForTimeout(250);
  await page.screenshot({ path: path.join(outDir, `${label}-after-marker-taps.png`), fullPage: false });

  const result = {
    label,
    viewport: { width, height },
    before,
    taps,
    failed: taps.filter((tap) => !tap.pass),
  };
  await fs.writeFile(path.join(outDir, `${label}-marker-hit-report.json`), JSON.stringify(result, null, 2));
  await context.close();
  return result;
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = {
  createdAt: new Date().toISOString(),
  url,
  desktop: await runViewport(browser, 'desktop-1440', 1440, 1000),
  mobile: await runViewport(browser, 'mobile-390', 390, 900),
};
await browser.close();
await fs.writeFile(path.join(outDir, 'showroom-marker-hit-report.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
