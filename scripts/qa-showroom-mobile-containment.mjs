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

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-mobile-containment-2026-06-24';
const url = process.argv[3] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=mobile_containment';
const unitId = process.argv[4] || '';

function round(n) {
  return Math.round(n * 10) / 10;
}

async function inspect(page) {
  return page.evaluate(() => {
    const width = window.innerWidth;
    const pick = (el) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        tag: el.tagName,
        id: el.id || '',
        cls: String(el.className || '').slice(0, 140),
        x: Math.round(r.x * 10) / 10,
        right: Math.round(r.right * 10) / 10,
        width: Math.round(r.width * 10) / 10,
        position: cs.position,
        display: cs.display,
        maxWidth: cs.maxWidth,
        marginInlineStart: cs.marginInlineStart,
        marginInlineEnd: cs.marginInlineEnd,
        paddingInlineStart: cs.paddingInlineStart,
        paddingInlineEnd: cs.paddingInlineEnd,
        text: (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 120),
      };
    };

    const selectors = {
      body: 'body',
      main: 'main',
      entry: '.entry-content',
      profile: '.nlpf',
      introHero: '.nlp3d-hero-media',
      intro: '.nlp3d-intro',
      showroom: '.nlp3d.nlp3d-premium',
      shell: '.nlp3d-shell',
      stageWrap: '.nlp3d-stage-wrap',
      stage: '.nlp3d-stage',
      modelViewer: 'model-viewer',
      breadcrumbs: '.nlbc',
    };
    const measured = Object.fromEntries(Object.entries(selectors).map(([key, selector]) => {
      const el = document.querySelector(selector);
      return [key, el ? pick(el) : null];
    }));

    const offenders = Array.from(document.querySelectorAll('body *')).map((el) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      if (r.width < 1 || r.height < 1 || cs.display === 'none' || cs.visibility === 'hidden') return null;
      if (r.right > width + 2 || r.x < -2) return pick(el);
      return null;
    }).filter(Boolean).slice(0, 120);

    return {
      url: location.href,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body ? document.body.scrollWidth : null,
      horizontalOverflow: Math.max(0, document.documentElement.scrollWidth - window.innerWidth),
      offenderCount: offenders.length,
      measured,
      offenders,
    };
  });
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 1100 },
  isMobile: true,
  hasTouch: true,
  deviceScaleFactor: 1,
  locale: 'he-IL',
});
const page = await context.newPage();
await page.goto(`${url}&t=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await page.waitForSelector('.nlp3d-premium', { timeout: 30000 });
await page.waitForTimeout(2500);
await page.screenshot({ path: path.join(outDir, 'rainbow-mobile-390-before-selection.png'), fullPage: true });
if (unitId) {
  await page.locator(`.nlp3d-model-picks .nlp3d-stage-pick[data-unit="${unitId}"]`).click();
  await page.waitForTimeout(1000);
}
await page.screenshot({ path: path.join(outDir, unitId ? `rainbow-mobile-390-selected-${unitId}.png` : 'rainbow-mobile-390-containment.png'), fullPage: true });
const report = await inspect(page);
report.selectedUnit = unitId || null;
await fs.writeFile(path.join(outDir, 'rainbow-mobile-390-containment.json'), JSON.stringify(report, null, 2));
await browser.close();
console.log(JSON.stringify(report, null, 2));
