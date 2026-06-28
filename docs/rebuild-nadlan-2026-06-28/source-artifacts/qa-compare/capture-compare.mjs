import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const root = 'C:/Users/pro/Documents/websites/nad-lan-co-il-pr2';
const outDir = 'C:/Users/pro/AppData/Local/Temp/nadlan-design-compare-2026-06-28';
fs.mkdirSync(outDir, { recursive: true });

const mockDir = path.join(root, 'handoff/claude-design/2026-06-27-showroom-engine');
const urls = {
  liveHome: 'https://nad-lan.co.il/?cb=visualcompare-20260628',
  liveAshira: 'https://nad-lan.co.il/projects/ashira-sde-dov/?cb=visualcompare-20260628',
  mockHome: pathToFileURL(path.join(mockDir, 'home.html')).href,
  mockAshira: pathToFileURL(path.join(mockDir, 'project.html')).href,
};

const browser = await chromium.launch({ headless: true });
const results = {};

async function capture(name, url, viewport, waitSelector) {
  const context = await browser.newContext({ viewport, deviceScaleFactor: 1, ignoreHTTPSErrors: true, isMobile: viewport.width < 600 });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e.message || e)));
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  if (waitSelector) {
    try { await page.waitForSelector(waitSelector, { timeout: 12000 }); } catch {}
  }
  await page.waitForTimeout(2500);
  const metrics = await page.evaluate(() => ({
    url: location.href,
    title: document.title,
    lang: document.documentElement.lang || '',
    dir: document.documentElement.dir || document.body.dir || '',
    h1Count: document.querySelectorAll('h1').length,
    nlRoot: document.querySelectorAll('#nl-root').length,
    nlv2: document.querySelectorAll('.nlv2-showroom').length,
    nlp3d: document.querySelectorAll('.nlp3d').length,
    modelViewer: document.querySelectorAll('model-viewer').length,
    horizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    bodyHeight: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
  }));
  const shotPath = path.join(outDir, `${name}.png`);
  await page.screenshot({ path: shotPath, fullPage: true });
  await context.close();
  results[name] = { url, shotPath, metrics, errorCount: errors.length, errors: errors.slice(0, 8) };
}

const desktop = { width: 1440, height: 1200 };
const mobile = { width: 390, height: 1200 };

await capture('live-home-desktop-full', urls.liveHome, desktop, 'body');
await capture('mock-home-desktop-full', urls.mockHome, desktop, 'body');
await capture('live-ashira-desktop-full', urls.liveAshira, desktop, '#nl-root');
await capture('mock-ashira-desktop-full', urls.mockAshira, desktop, '#nl-root');
await capture('live-home-mobile-full', urls.liveHome, mobile, 'body');
await capture('mock-home-mobile-full', urls.mockHome, mobile, 'body');
await capture('live-ashira-mobile-full', urls.liveAshira, mobile, '#nl-root');
await capture('mock-ashira-mobile-full', urls.mockAshira, mobile, '#nl-root');

function fileUrl(p) { return pathToFileURL(p).href; }
async function compare(name, leftPath, rightPath, leftLabel, rightLabel, viewport={ width: 1800, height: 1200 }) {
  const page = await browser.newPage({ viewport });
  await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>
    body{margin:0;background:#111;color:#fff;font:16px Arial,sans-serif;}
    .bar{position:sticky;top:0;z-index:2;display:grid;grid-template-columns:1fr 1fr;background:#111;border-bottom:2px solid #d8b35a;}
    .bar div{padding:14px 18px;font-weight:700;}
    .wrap{display:grid;grid-template-columns:1fr 1fr;align-items:start;gap:0;}
    .panel{border-right:2px solid #d8b35a;background:#222;}
    img{display:block;width:100%;height:auto;background:white;}
  </style></head><body><div class="bar"><div>${leftLabel}</div><div>${rightLabel}</div></div><div class="wrap"><div class="panel"><img src="${fileUrl(leftPath)}"></div><div class="panel"><img src="${fileUrl(rightPath)}"></div></div></body></html>`, { waitUntil: 'load' });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: true });
  await page.close();
}

await compare('compare-home-desktop-live-vs-mock', results['live-home-desktop-full'].shotPath, results['mock-home-desktop-full'].shotPath, 'LIVE HOME', 'CLAUDE DESIGN MOCK');
await compare('compare-ashira-desktop-live-vs-mock', results['live-ashira-desktop-full'].shotPath, results['mock-ashira-desktop-full'].shotPath, 'LIVE ASHIRA', 'CLAUDE DESIGN MOCK');
await compare('compare-home-mobile-live-vs-mock', results['live-home-mobile-full'].shotPath, results['mock-home-mobile-full'].shotPath, 'LIVE HOME MOBILE', 'MOCK HOME MOBILE', { width: 900, height: 1200 });
await compare('compare-ashira-mobile-live-vs-mock', results['live-ashira-mobile-full'].shotPath, results['mock-ashira-mobile-full'].shotPath, 'LIVE ASHIRA MOBILE', 'MOCK ASHIRA MOBILE', { width: 900, height: 1200 });

await browser.close();
fs.writeFileSync(path.join(outDir, 'playwright-metrics.json'), JSON.stringify({ urls, results }, null, 2), 'utf8');
console.log(JSON.stringify({ outDir, files: fs.readdirSync(outDir).sort() }, null, 2));
