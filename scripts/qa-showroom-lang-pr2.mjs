import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const OUT = path.join(process.cwd(), 'docs', 'qa', 'screenshots', 'showroom-lang-pr2');
fs.mkdirSync(OUT, { recursive: true });
const LOCAL_ENGINE = process.env.NADLAN_QA_LOCAL_ENGINE === '1';
const localEngineSource = LOCAL_ENGINE
  ? fs.readFileSync(path.join(process.cwd(), 'plugins', 'nadlan-config', 'assets', 'showroom-engine', 'engine.js'), 'utf8')
  : null;

const langs = [
  { code: 'he', url: 'https://nad-lan.co.il/projects/ashira-sde-dov/', dir: 'rtl' },
  { code: 'en', url: 'https://nad-lan.co.il/projects/ashira-sde-dov-en/', dir: 'ltr' },
  { code: 'fr', url: 'https://nad-lan.co.il/projects/ashira-sde-dov-fr/', dir: 'ltr' },
  { code: 'ru', url: 'https://nad-lan.co.il/projects/ashira-sde-dov-ru/', dir: 'ltr' },
  { code: 'ar', url: 'https://nad-lan.co.il/projects/ashira-sde-dov-ar/', dir: 'rtl' },
];

const viewports = [
  { name: 'desktop-1440', width: 1440, height: 1200 },
  { name: 'mobile-390', width: 390, height: 1200, isMobile: true },
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function cacheBust(url) {
  const u = new URL(url);
  u.searchParams.set('cb', `lang-pr2-${Date.now()}`);
  return u.toString();
}

async function collectPageFacts(page) {
  return page.evaluate(() => {
    const alternates = Array.from(document.querySelectorAll('link[rel="alternate"]')).map((n) => ({
      hreflang: n.getAttribute('hreflang'),
      href: n.getAttribute('href'),
    }));
    return {
      url: location.href,
      htmlLang: document.documentElement.lang,
      htmlDir: document.documentElement.dir,
      nlv2Showroom: document.querySelectorAll('.nlv2-showroom').length,
      nlRoot: document.querySelectorAll('#nl-root').length,
      langButtons: Array.from(document.querySelectorAll('[data-act="lang"]')).map((n) => ({
        id: n.getAttribute('data-id'),
        pressed: n.getAttribute('aria-pressed'),
        text: n.textContent.trim(),
      })),
      footerLangLinks: Array.from(document.querySelectorAll('.nl-footer [data-act="lang"]')).map((n) => ({
        id: n.getAttribute('data-id'),
        href: n.getAttribute('href'),
        text: n.textContent.trim(),
      })),
      alternates,
      bodyTextSample: document.body.innerText.slice(0, 500),
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
    };
  });
}

async function waitForShowroom(page) {
  await page.waitForSelector('#nl-root', { timeout: 30000 });
  await page.waitForFunction(() => {
    const root = document.querySelector('#nl-root');
    return root && root.innerText && root.innerText.length > 300;
  }, null, { timeout: 30000 });
}

async function gateLanguagePage(browser, lang, viewport) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    isMobile: Boolean(viewport.isMobile),
    hasTouch: Boolean(viewport.isMobile),
    locale: lang.code === 'he' ? 'he-IL' : lang.code === 'ar' ? 'ar' : lang.code,
  });
  const page = await context.newPage();
  if (LOCAL_ENGINE) {
    await page.route('**/assets/showroom-engine/engine.js*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/javascript; charset=utf-8',
        body: localEngineSource,
      });
    });
  }
  const errors = [];
  page.on('pageerror', (err) => errors.push(`pageerror: ${err.message}`));
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push(`console: ${msg.text()}`);
  });

  await page.goto(cacheBust(lang.url), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await waitForShowroom(page);
  await page.screenshot({
    path: path.join(OUT, `${lang.code}-${viewport.name}.png`),
    fullPage: true,
  });
  const facts = await collectPageFacts(page);
  assert(facts.htmlLang === lang.code, `${lang.code}: expected html lang ${lang.code}, got ${facts.htmlLang}`);
  assert(facts.htmlDir === lang.dir, `${lang.code}: expected dir ${lang.dir}, got ${facts.htmlDir}`);
  assert(facts.nlv2Showroom === 0, `${lang.code}: legacy .nlv2-showroom rendered ${facts.nlv2Showroom} times`);
  assert(facts.nlRoot === 1, `${lang.code}: expected exactly one #nl-root, got ${facts.nlRoot}`);
  assert(facts.scrollWidth <= facts.clientWidth + 1, `${lang.code}: horizontal overflow ${facts.scrollWidth}/${facts.clientWidth}`);

  const alternateLangs = new Set(facts.alternates.map((a) => a.hreflang));
  for (const required of ['he', 'en', 'fr', 'ru', 'ar', 'x-default']) {
    assert(alternateLangs.has(required), `${lang.code}: missing hreflang ${required}`);
  }
  const visibleButtonIds = facts.langButtons.map((b) => b.id);
  for (const required of ['he', 'en', 'fr', 'ru', 'ar']) {
    assert(visibleButtonIds.includes(required), `${lang.code}: missing language button ${required}`);
  }
  assert(facts.langButtons.some((b) => b.id === lang.code && b.pressed === 'true'), `${lang.code}: current language button not active`);
  for (const link of facts.footerLangLinks) {
    assert(link.href && link.href !== '#', `${lang.code}: footer language ${link.id} still points to #`);
    if (link.id && ['he', 'en', 'fr', 'ru', 'ar'].includes(link.id)) {
      assert(link.href.includes('/projects/ashira-sde-dov'), `${lang.code}: footer language ${link.id} has unexpected href ${link.href}`);
    }
  }

  // PR2 critical path: on EN page the HE button must navigate to the HE sibling,
  // not merely swap strings in-place.
  let clickResult = null;
  if (lang.code === 'en' && viewport.name === 'desktop-1440') {
    await Promise.all([
      page.waitForURL(/\/projects\/ashira-sde-dov\/(\?|$)/, { timeout: 30000 }),
      page.click('[data-act="lang"][data-id="he"]'),
    ]);
    await waitForShowroom(page);
    clickResult = await collectPageFacts(page);
    assert(clickResult.htmlLang === 'he', `EN -> HE click: expected html lang he, got ${clickResult.htmlLang}`);
    assert(clickResult.htmlDir === 'rtl', `EN -> HE click: expected rtl, got ${clickResult.htmlDir}`);
    assert(/\/projects\/ashira-sde-dov\/(\?|$)/.test(clickResult.url), `EN -> HE click: wrong URL ${clickResult.url}`);
  }

  assert(errors.length === 0, `${lang.code} ${viewport.name}: browser errors:\n${errors.join('\n')}`);
  await context.close();
  return { lang: lang.code, viewport: viewport.name, facts, clickResult, errors };
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const viewport of viewports) {
      for (const lang of langs) {
        results.push(await gateLanguagePage(browser, lang, viewport));
      }
    }
  } finally {
    await browser.close();
  }
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify({
    checkedAt: new Date().toISOString(),
    localEngine: LOCAL_ENGINE,
    results,
  }, null, 2));
  console.log(`PR2 language QA passed. Screenshots and report written to ${OUT}`);
})();
