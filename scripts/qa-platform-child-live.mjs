import { chromium } from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const base = 'https://nad-lan.co.il';
const outDir = process.argv[2] || 'docs/qa/screenshots/platform-rebuild-2026-06-29/01-live-after-child-0.1.4';
const stamp = Date.now();

const pages = [
  { key: 'home', url: '/' },
  { key: 'projects', url: '/projects/' },
  { key: 'ashira-he', url: '/projects/ashira-sde-dov/' },
  { key: 'ashira-en', url: '/projects/ashira-sde-dov-en/' },
  { key: 'calculator', url: '/mortgage-calculator/' },
  { key: 'professionals', url: '/professionals/' },
  { key: 'guide', url: '/buying-apartment/' },
];

const viewports = [
  { key: 'desktop-1440', width: 1440, height: 1200 },
  { key: 'mobile-390', width: 390, height: 1100 },
];

const leaks = [
  'GLB',
  'BIM',
  'mesh',
  'hotspot',
  'token',
  'Codex',
  'Lovable',
  'AI Generated',
  'prompt',
  'CMS',
  'funnel',
  'internal',
  'Featured',
  'Sponsored',
];

function withCacheBust(url) {
  const full = new URL(url, base);
  full.searchParams.set('codexqa', String(stamp));
  return full.toString();
}

await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch({ channel: 'chrome', headless: true });
const results = [];

for (const vp of viewports) {
  const context = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: 1,
    isMobile: vp.width < 600,
    hasTouch: vp.width < 600,
  });

  for (const item of pages) {
    const page = await context.newPage();
    const consoleErrors = [];
    const failedRequests = [];

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });
    page.on('pageerror', (err) => {
      consoleErrors.push(err.message);
    });
    page.on('requestfailed', (request) => {
      failedRequests.push(request.url());
    });

    const url = withCacheBust(item.url);
    const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await page.screenshot({ path: path.join(outDir, `${item.key}-${vp.key}.png`), fullPage: true });

    const metrics = await page.evaluate((leakTerms) => {
      const text = document.body ? document.body.innerText : '';
      const offscreen = Array.from(document.querySelectorAll('a,button,input,select,textarea,[role="button"]'))
        .filter((el) => {
          const rect = el.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0 && (rect.left < -2 || rect.right > window.innerWidth + 2);
        })
        .slice(0, 12)
        .map((el) => ({
          tag: el.tagName,
          text: (el.innerText || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 80),
          left: Math.round(el.getBoundingClientRect().left),
          right: Math.round(el.getBoundingClientRect().right),
        }));

      return {
        lang: document.documentElement.lang,
        dir: document.documentElement.dir,
        title: document.title,
        h1: document.querySelectorAll('h1').length,
        nlRoot: document.querySelectorAll('#nl-root').length,
        oldNlv2: document.querySelectorAll('.nlv2-showroom').length,
        oldP3d: document.querySelectorAll('.nlp3d').length,
        homeBand: document.querySelectorAll('[data-nlpo-home-projects]').length,
        overflow: document.documentElement.scrollWidth > window.innerWidth + 2,
        scrollWidth: document.documentElement.scrollWidth,
        innerWidth: window.innerWidth,
        textLeaks: leakTerms.filter((term) => text.includes(term)),
        emDash: (text.match(/—/g) || []).length,
        stickyHeader: !!document.querySelector('.nlpc-site-header, header, #masthead'),
        footer: !!document.querySelector('.nlpc-site-footer, footer'),
        offscreen,
      };
    }, leaks);

    results.push({
      key: item.key,
      viewport: vp.key,
      url,
      status: response ? response.status() : null,
      screenshot: `${item.key}-${vp.key}.png`,
      consoleErrors,
      failedRequests,
      ...metrics,
    });

    await page.close();
  }

  await context.close();
}

await browser.close();

await fs.writeFile(path.join(outDir, 'report.json'), JSON.stringify(results, null, 2), 'utf8');

const lines = [
  '# NadLan Platform Child Live QA',
  '',
  `Date: ${new Date().toISOString()}`,
  '',
  '| Page | Viewport | Status | H1 | #nl-root | .nlv2 | .nlp3d | Home band | Overflow | Lang | Dir | Leaks | Console errors | Screenshot |',
  '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | ---: | --- |',
  ...results.map((r) => `| ${r.key} | ${r.viewport} | ${r.status} | ${r.h1} | ${r.nlRoot} | ${r.oldNlv2} | ${r.oldP3d} | ${r.homeBand} | ${r.overflow ? 'FAIL' : 'OK'} | ${r.lang} | ${r.dir} | ${r.textLeaks.join(', ') || 'none'} | ${r.consoleErrors.length} | ${r.screenshot} |`),
  '',
  '## Notes',
  '',
  '- Screenshots were captured with installed Google Chrome via Playwright channel `chrome`.',
  '- Cache-busting query parameters were used on each public URL.',
  '- This report checks live public rendering only. It does not rewrite content or change settings.',
];

await fs.writeFile(path.join(outDir, 'REPORT.md'), lines.join('\n'), 'utf8');
console.log(JSON.stringify({ outDir, count: results.length }, null, 2));
