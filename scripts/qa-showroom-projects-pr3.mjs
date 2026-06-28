import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const args = new Set(process.argv.slice(2));
const EXPECT_REDIRECT = args.has('--expect-redirect');
const BASE = process.env.NADLAN_QA_BASE || 'https://nad-lan.co.il';
const OUT = path.join(process.cwd(), 'docs', 'qa', 'screenshots', 'showroom-projects-pr3');
fs.mkdirSync(OUT, { recursive: true });

const viewports = [
  { name: 'desktop-1440', width: 1440, height: 1200 },
  { name: 'mobile-390', width: 390, height: 1200, isMobile: true },
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function urlFor(pathname) {
  const url = new URL(pathname, BASE);
  url.searchParams.set('cb', `projects-pr3-${Date.now()}`);
  return url.toString();
}

async function facts(page) {
  return page.evaluate(() => {
    const text = document.body.innerText || '';
    const anchors = Array.from(document.querySelectorAll('a[href]')).map((a) => a.href);
    return {
      url: location.href,
      title: document.title,
      htmlLang: document.documentElement.lang || '',
      htmlDir: document.documentElement.dir || '',
      h1: document.querySelector('h1')?.textContent?.trim() || '',
      has404: /Page not found|Nothing found|404|לא נמצא|העמוד לא נמצא/i.test(text),
      projectLinks: anchors.filter((href) => href.includes('/projects/')),
      deadHomeLinks: anchors.filter((href) => href.includes('/home.html')),
      deadEnglishHomeLinks: anchors.filter((href) => /\/en\/?$/.test(new URL(href).pathname)),
      cardishCount: document.querySelectorAll('article, .nadlan-card, .nl-project-card, .project-card, .wp-block-post, .nl-card').length,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      bodySample: text.slice(0, 800),
    };
  });
}

async function openPage(context, pathname, screenshotName) {
  const page = await context.newPage();
  const errors = [];
  const knownErrors = [];
  const recordError = (message) => {
    if (message.includes('@wordpress/interactivity')) {
      knownErrors.push(message);
      return;
    }
    errors.push(message);
  };
  page.on('pageerror', (err) => recordError(`pageerror: ${err.message}`));
  page.on('console', (msg) => {
    if (msg.type() === 'error') recordError(`console: ${msg.text()}`);
  });
  const response = await page.goto(urlFor(pathname), { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForLoadState('networkidle', { timeout: 45000 }).catch(() => {});
  await page.screenshot({ path: path.join(OUT, screenshotName), fullPage: true });
  const result = await facts(page);
  result.status = response?.status() || 0;
  result.errors = errors;
  result.knownErrors = knownErrors;
  await page.close();
  return result;
}

async function runViewport(browser, viewport) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    isMobile: Boolean(viewport.isMobile),
    hasTouch: Boolean(viewport.isMobile),
    locale: 'he-IL',
  });
  try {
    const home = await openPage(context, '/', `home-${viewport.name}.png`);
    const projects = await openPage(context, '/projects/', `projects-${viewport.name}.png`);
    const stale = await openPage(context, '/home.html', `home-html-${viewport.name}.png`);

    assert(home.status < 400, `${viewport.name}: homepage status ${home.status}`);
    assert(projects.status < 400, `${viewport.name}: /projects/ status ${projects.status}`);
    assert(!home.has404, `${viewport.name}: homepage rendered 404 text`);
    assert(!projects.has404, `${viewport.name}: /projects/ rendered 404 text`);
    assert(home.projectLinks.some((href) => new URL(href).pathname === '/projects/'), `${viewport.name}: homepage missing /projects/ link`);
    assert(projects.projectLinks.length >= 3 || projects.cardishCount >= 3, `${viewport.name}: /projects/ catalog has too few project links/cards`);
    assert(home.deadHomeLinks.length === 0, `${viewport.name}: homepage still links to home.html`);
    assert(projects.deadHomeLinks.length === 0, `${viewport.name}: /projects/ still links to home.html`);
    assert(home.deadEnglishHomeLinks.length === 0, `${viewport.name}: homepage links dead /en/ route`);
    assert(projects.deadEnglishHomeLinks.length === 0, `${viewport.name}: /projects/ links dead /en/ route`);
    assert(home.scrollWidth <= home.clientWidth + 1, `${viewport.name}: homepage horizontal overflow ${home.scrollWidth}/${home.clientWidth}`);
    assert(projects.scrollWidth <= projects.clientWidth + 1, `${viewport.name}: /projects/ horizontal overflow ${projects.scrollWidth}/${projects.clientWidth}`);
    assert(home.errors.length === 0, `${viewport.name}: homepage browser errors:\n${home.errors.join('\n')}`);
    assert(projects.errors.length === 0, `${viewport.name}: /projects/ browser errors:\n${projects.errors.join('\n')}`);

    if (EXPECT_REDIRECT) {
      assert(stale.status < 400, `${viewport.name}: /home.html final status ${stale.status}`);
      assert(new URL(stale.url).pathname === '/projects/', `${viewport.name}: /home.html did not land on /projects/: ${stale.url}`);
      assert(!stale.has404, `${viewport.name}: /home.html still rendered 404 text`);
    }

    return { viewport: viewport.name, home, projects, stale };
  } finally {
    await context.close();
  }
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];
  try {
    for (const viewport of viewports) {
      results.push(await runViewport(browser, viewport));
    }
  } finally {
    await browser.close();
  }
  const report = {
    checkedAt: new Date().toISOString(),
    base: BASE,
    expectRedirect: EXPECT_REDIRECT,
    results,
  };
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2), 'utf8');
  console.log(`PR3 project catalog QA passed. Screenshots and report written to ${OUT}`);
})();
