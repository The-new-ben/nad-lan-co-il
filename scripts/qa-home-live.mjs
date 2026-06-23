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

const outDir = process.argv[2] || 'docs/qa/screenshots/home-live-audit-2026-06-24';
const url = process.argv[3] || 'https://nad-lan.co.il/?codex_qa=home_live';

async function inspect(page) {
  return page.evaluate(() => {
    const visible = (el) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden';
    };
    const box = (el) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        tag: el.tagName,
        cls: String(el.className || '').slice(0, 140),
        id: el.id || '',
        x: Math.round(r.x * 10) / 10,
        right: Math.round(r.right * 10) / 10,
        width: Math.round(r.width * 10) / 10,
        display: cs.display,
        position: cs.position,
        text: (el.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 180),
      };
    };
    const text = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
    const forbiddenPatterns = [
      'Lovable', 'Codex', 'Claude', 'prompt', 'token', 'Tailwind',
      'money page', 'KD', 'CRM', 'UTM', 'lead pipeline',
    ];
    return {
      url: location.href,
      title: document.title,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      horizontalOverflow: Math.max(0, document.documentElement.scrollWidth - window.innerWidth),
      h1: Array.from(document.querySelectorAll('h1')).map((h) => h.innerText.trim()),
      headings: Array.from(document.querySelectorAll('h1,h2,h3')).filter(visible).slice(0, 40).map((h) => ({
        tag: h.tagName,
        text: h.innerText.replace(/\s+/g, ' ').trim().slice(0, 160),
      })),
      visibleLinks: Array.from(document.querySelectorAll('a')).filter(visible).map((a) => ({
        text: (a.innerText || a.textContent || '').replace(/\s+/g, ' ').trim(),
        href: a.href,
      })).filter((a) => a.text).slice(0, 80),
      forbiddenPublicText: forbiddenPatterns.filter((pattern) => text.toLowerCase().includes(pattern.toLowerCase())),
      offenders: Array.from(document.querySelectorAll('body *')).map((el) => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        if (r.width < 1 || r.height < 1 || cs.display === 'none' || cs.visibility === 'hidden') return null;
        if (r.right > window.innerWidth + 2 || r.x < -2) return box(el);
        return null;
      }).filter(Boolean).slice(0, 80),
      hero: box(document.querySelector('main h1') || document.querySelector('h1')),
      firstScreenText: text.slice(0, 1800),
    };
  });
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const viewports = [
  { name: 'desktop-1440', width: 1440, height: 1000, isMobile: false },
  { name: 'mobile-390', width: 390, height: 1000, isMobile: true },
];
const results = {};

for (const vp of viewports) {
  const context = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    isMobile: vp.isMobile,
    hasTouch: vp.isMobile,
    deviceScaleFactor: 1,
    locale: 'he-IL',
  });
  const page = await context.newPage();
  await page.goto(`${url}&viewport=${vp.name}&t=${Date.now()}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(2500);
  await page.screenshot({ path: path.join(outDir, `${vp.name}.png`), fullPage: true });
  const report = await inspect(page);
  await fs.writeFile(path.join(outDir, `${vp.name}.json`), JSON.stringify(report, null, 2));
  results[vp.name] = report;
  await context.close();
}

await browser.close();
await fs.writeFile(path.join(outDir, 'home-live-report.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
