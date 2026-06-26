import { chromium } from 'playwright';

const url = process.argv[2] || 'http://127.0.0.1:8765/docs/previews/ashira-showroom-preview.php';
const out = process.argv[3] || 'docs/qa/screenshots/ashira-showroom-factory-2026-06-26/desktop-clicked-15-02.png';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width: 1440, height: 1200 },
  deviceScaleFactor: 1,
});

const logs = [];
page.on('console', (message) => {
  if (['error', 'warning'].includes(message.type())) {
    logs.push({ type: message.type(), text: message.text() });
  }
});
page.on('pageerror', (error) => {
  logs.push({ type: 'pageerror', text: error.message });
});

await page.goto(url, { waitUntil: 'networkidle' });
await page.click('[data-unit-id="ashira-15-02"]');
await page.waitForTimeout(250);

const afterClick = await page.evaluate(() => ({
  title: document.querySelector('[data-nlps-title]')?.textContent.trim() || '',
  status: document.querySelector('[data-nlps-status]')?.textContent.trim() || '',
  rooms: document.querySelector('[data-nlps-rooms]')?.textContent.trim() || '',
  active: document.querySelector('[data-nlps-unit].is-active')?.dataset.unitId || '',
}));

await page.click('[data-nlps-tab="tour"]');
await page.waitForTimeout(150);
const panel = await page.locator('[data-nlps-media-panel]').innerText();

await page.click('[data-nlps-dismiss]');
await page.waitForTimeout(150);
const hidden = await page.locator('[data-nlps-card]').evaluate((element) => element.hidden);

await page.screenshot({ path: out, fullPage: true });
await browser.close();

console.log(JSON.stringify({ afterClick, panel, hidden, logs }, null, 2));

if (afterClick.active !== 'ashira-15-02') {
  throw new Error('Unit click did not activate ashira-15-02');
}
if (!afterClick.title.includes('15-02') || afterClick.rooms !== '5') {
  throw new Error('Selected apartment card did not update correctly');
}
if (!panel.includes('סיור פנים')) {
  throw new Error('Tour tab did not update the media panel');
}
if (!hidden) {
  throw new Error('Dismiss button did not hide the apartment card');
}
if (logs.some((entry) => entry.type === 'error' || entry.type === 'pageerror')) {
  throw new Error('Browser errors were emitted during interaction QA');
}
