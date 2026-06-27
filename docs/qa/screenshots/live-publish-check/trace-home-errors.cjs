const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: false });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  const events = [];
  page.on('requestfailed', req => events.push({type:'requestfailed', url:req.url(), failure:req.failure()?.errorText}));
  page.on('response', resp => { if (resp.status() >= 400) events.push({type:'response', status:resp.status(), url:resp.url()}); });
  page.on('console', msg => { if (msg.type() === 'error') events.push({type:'console', text:msg.text(), location:msg.location()}); });
  page.on('pageerror', err => events.push({type:'pageerror', text:err.message}));
  await page.goto('https://nad-lan.co.il/?cb=home-error-trace-20260627', { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(5000);
  await browser.close();
  console.log(JSON.stringify(events, null, 2));
})();
