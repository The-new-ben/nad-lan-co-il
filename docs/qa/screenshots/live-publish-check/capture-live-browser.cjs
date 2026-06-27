const fs = require('fs');
const path = require('path');
const { chromium, devices } = require('playwright');

const outDir = path.resolve('docs/qa/screenshots/live-publish-check/browser');
fs.mkdirSync(outDir, { recursive: true });

const pages = [
  ['home', 'https://nad-lan.co.il/?cb=live-visual-qa-20260627'],
  ['ashira-he', 'https://nad-lan.co.il/projects/ashira-sde-dov/?cb=live-visual-qa-20260627'],
  ['ashira-en', 'https://nad-lan.co.il/projects/ashira-sde-dov-en/?cb=live-visual-qa-20260627'],
  ['ashira-fr', 'https://nad-lan.co.il/projects/ashira-sde-dov-fr/?cb=live-visual-qa-20260627'],
  ['ashira-ru', 'https://nad-lan.co.il/projects/ashira-sde-dov-ru/?cb=live-visual-qa-20260627'],
  ['ashira-ar', 'https://nad-lan.co.il/projects/ashira-sde-dov-ar/?cb=live-visual-qa-20260627'],
];

const viewports = [
  ['desktop-1440', { viewport: { width: 1440, height: 1100 }, deviceScaleFactor: 1, isMobile: false }],
  ['mobile-390', { viewport: { width: 390, height: 900 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }],
];

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: false });
  const report = [];
  for (const [vpName, vp] of viewports) {
    const context = await browser.newContext({ ...vp, locale: 'he-IL' });
    for (const [name, url] of pages) {
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(String(e.message || e)));
      page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await page.waitForTimeout(3500);
      const metrics = await page.evaluate(() => {
        const html = document.documentElement;
        const body = document.body;
        const h1s = Array.from(document.querySelectorAll('h1')).map(h => h.textContent.trim()).filter(Boolean);
        return {
          title: document.title,
          h1s,
          hasHomeHero: !!document.querySelector('.nlux-hero'),
          hasShowroom: !!document.querySelector('.nlp3d-premium, [data-nlps-showroom], [data-nlv2-showroom]'),
          hasModel: !!document.querySelector('model-viewer, .nlp3d-stage, .nlp3d-model'),
          hasFacade: !!document.querySelector('.nlp3d-facade, .nlp3d-stage-picks, .nlp3d-facade-plane'),
          scrollWidth: html.scrollWidth,
          clientWidth: html.clientWidth,
          bodyTextStart: (body.innerText || '').slice(0, 240),
        };
      });
      const shot = path.join(outDir, `${name}-${vpName}.png`);
      await page.screenshot({ path: shot, fullPage: true });
      report.push({ name, viewport: vpName, url, screenshot: shot, errors, metrics, ok: errors.length === 0 && metrics.scrollWidth <= metrics.clientWidth + 4 });
      await page.close();
    }
    await context.close();
  }
  await browser.close();
  const reportPath = path.join(outDir, 'report.json');
  fs.writeFileSync(reportPath, JSON.stringify({ ok: report.every(r => r.ok), generated_at: new Date().toISOString(), report }, null, 2));
  console.log(JSON.stringify({ ok: report.every(r => r.ok), reportPath, screenshots: report.map(r => r.screenshot) }, null, 2));
  if (!report.every(r => r.ok)) process.exit(2);
})().catch(err => { console.error(err); process.exit(1); });
