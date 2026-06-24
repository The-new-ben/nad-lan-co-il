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

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-overview-selection-live-16917-2026-06-24';
const unitId = process.argv[3] || 'unit-16-w';
const url = process.argv[4] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=overview_selection_16917';

function serializeError(error) {
  if (!error) {
    return null;
  }
  return {
    name: error.name || 'Error',
    message: error.message || String(error),
  };
}

async function inspect(page) {
  return page.evaluate(() => {
    const root = document.querySelector('.nlp3d');
    const mv = document.querySelector('model-viewer');
    const card = document.querySelector('.nlp3d-stage-card');
    const title = document.querySelector('.nlp3d-selected-title');
    const forbidden = /\b(Lovable|Codex|Claude|prompt|token|war room|money page|GLB stub|mock data)\b/i;
    const text = document.body ? document.body.innerText : '';
    return {
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      activeUnit: root ? root.getAttribute('data-active-unit') : null,
      activePick: document.querySelector('.nlp3d-stage-pick.is-active, .nlp3d-stage-pick[aria-pressed="true"]')?.getAttribute('data-unit') || null,
      activePickCount: document.querySelectorAll('.nlp3d-stage-pick.is-active, .nlp3d-stage-pick[aria-pressed="true"]').length,
      cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
      cameraTarget: mv ? mv.getAttribute('camera-target') : null,
      stageCardHidden: card ? card.hidden : null,
      selectedTitle: title ? title.innerText.replace(/\s+/g, ' ').trim() : '',
      stageCardText: card ? card.innerText.replace(/\s+/g, ' ').trim().slice(0, 500) : '',
      forbiddenLeak: forbidden.test(text),
      leakSample: (text.match(forbidden) || [null])[0],
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
  const result = {
    label,
    unitId,
    viewport: { width, height },
    url: `${url}&viewport=${label}&t=${Date.now()}`,
  };

  try {
    await page.goto(result.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.nlp3d-premium model-viewer', { timeout: 45000 });
    await page.waitForFunction(() => document.querySelector('.nlp3d')?.classList.contains('has-model-viewer-loaded'), null, { timeout: 45000 }).catch(() => null);
    await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
    await page.waitForTimeout(800);
    result.before = await inspect(page);
    await page.screenshot({ path: path.join(outDir, `${label}-overview-before-select.png`), fullPage: false });

    const pick = page.locator(`.nlp3d-stage-pick[data-unit="${unitId}"]`);
    const pickCount = await pick.count();
    result.pickCount = pickCount;
    if (pickCount !== 1) {
      result.pass = false;
      result.reason = `Expected one visible apartment pick for ${unitId}, found ${pickCount}.`;
      return result;
    }

    await pick.click({ timeout: 10000 });
    await page.waitForFunction(
      (expectedUnit) => document.querySelector('.nlp3d')?.getAttribute('data-active-unit') === expectedUnit,
      unitId,
      { timeout: 10000 }
    );
    await page.waitForTimeout(2200);
    result.after = await inspect(page);
    await page.screenshot({ path: path.join(outDir, `${label}-after-select-${unitId}.png`), fullPage: false });

    result.pass = !!(
      !result.before.forbiddenLeak &&
      !result.after.forbiddenLeak &&
      !result.before.activeUnit &&
      !result.before.activePick &&
      result.before.activePickCount === 0 &&
      result.before.stageCardHidden === true &&
      result.after.activeUnit === unitId &&
      result.after.activePick === unitId &&
      result.after.cameraOrbit &&
      result.after.cameraTarget &&
      result.after.stageCardHidden === false &&
      result.after.scrollWidth <= width
    );
    if (!result.pass) {
      result.reason = 'Overview state, apartment selection, camera movement, card visibility, leak scan or mobile width check failed.';
    }
  } catch (error) {
    result.pass = false;
    result.error = serializeError(error);
    await page.screenshot({ path: path.join(outDir, `${label}-error.png`), fullPage: false }).catch(() => null);
  } finally {
    await context.close();
  }

  return result;
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = {
  createdAt: new Date().toISOString(),
  url,
  unitId,
  desktop: await runViewport(browser, 'desktop-1440', 1440, 1000),
  mobile: await runViewport(browser, 'mobile-390', 390, 900),
};
await browser.close();
results.pass = !!(results.desktop.pass && results.mobile.pass);
await fs.writeFile(path.join(outDir, 'showroom-overview-selection-report.json'), JSON.stringify(results, null, 2));

const qa = [
  '# Showroom overview and apartment selection QA',
  '',
  `- Created: ${results.createdAt}`,
  `- URL: ${url}`,
  `- Selected unit tested: ${unitId}`,
  `- Overall pass: ${results.pass ? 'yes' : 'no'}`,
  '',
  '## What this proves',
  '',
  '- The first showroom frame opens on a building overview, with no apartment preselected.',
  '- A real buyer click on the visible model apartment target selects the unit.',
  '- The selected unit sets camera orbit and camera target, and opens the selected-apartment card.',
  '- Desktop and 390px mobile screenshots are saved in this folder.',
  '',
  '## Desktop',
  '',
  `- Pass: ${results.desktop.pass ? 'yes' : 'no'}`,
  `- Before active unit: ${results.desktop.before?.activeUnit || 'none'}`,
  `- After active unit: ${results.desktop.after?.activeUnit || 'none'}`,
  `- After camera orbit: ${results.desktop.after?.cameraOrbit || 'missing'}`,
  `- After camera target: ${results.desktop.after?.cameraTarget || 'missing'}`,
  '',
  '## Mobile 390',
  '',
  `- Pass: ${results.mobile.pass ? 'yes' : 'no'}`,
  `- Before active unit: ${results.mobile.before?.activeUnit || 'none'}`,
  `- After active unit: ${results.mobile.after?.activeUnit || 'none'}`,
  `- After camera orbit: ${results.mobile.after?.cameraOrbit || 'missing'}`,
  `- After camera target: ${results.mobile.after?.cameraTarget || 'missing'}`,
  '',
  '## Honesty',
  '',
  'This proves selection on the authored visible apartment targets and camera movement for the tested unit. It does not prove true click-any-window BIM picking because the project still has only authored unit points, not apartment-level mesh metadata.',
  '',
].join('\n');
await fs.writeFile(path.join(outDir, 'QA.md'), qa);

console.log(JSON.stringify(results, null, 2));
