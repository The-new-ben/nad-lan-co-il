import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

const repo = path.resolve(import.meta.dirname, '..');
const outDir = path.join(repo, 'docs/qa/screenshots/floating-actions-2026-06-19');
const urls = [
  { slug: 'dimri-yama-sde-dov', url: 'https://nad-lan.co.il/projects/dimri-yama-sde-dov/' },
  { slug: 'rainbow-tel-aviv', url: 'https://nad-lan.co.il/projects/rainbow-tel-aviv/' },
];
const viewports = [
  { name: 'desktop-1440', width: 1440, height: 900, mobile: false, deviceScaleFactor: 1 },
  { name: 'tablet-768', width: 768, height: 900, mobile: false, deviceScaleFactor: 1 },
  { name: 'mobile-390', width: 390, height: 820, mobile: true, deviceScaleFactor: 2 },
];

function chromeCandidates() {
  if (process.env.CHROME_PATH) return [process.env.CHROME_PATH];
  if (process.platform === 'win32') {
    return [
      path.join(process.env.ProgramFiles || 'C:\\Program Files', 'Google\\Chrome\\Application\\chrome.exe'),
      path.join(process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)', 'Google\\Chrome\\Application\\chrome.exe'),
      path.join(process.env.LOCALAPPDATA || '', 'Google\\Chrome\\Application\\chrome.exe'),
      path.join(process.env.ProgramFiles || 'C:\\Program Files', 'Microsoft\\Edge\\Application\\msedge.exe'),
    ];
  }
  return ['/usr/bin/google-chrome', '/usr/bin/chromium', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'];
}
function findChrome() {
  const found = chromeCandidates().find((candidate) => candidate && fs.existsSync(candidate));
  if (!found) throw new Error('Chrome/Edge not found. Set CHROME_PATH.');
  return found;
}
function delay(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }
async function waitForFile(file, timeoutMs = 10000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (fs.existsSync(file)) return fs.readFileSync(file, 'utf8');
    await delay(80);
  }
  throw new Error(`Timed out waiting for ${file}`);
}
class CdpClient {
  constructor(wsUrl) {
    this.id = 0;
    this.pending = new Map();
    this.listeners = new Map();
    this.ws = new WebSocket(wsUrl);
  }
  async open() {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('Timed out opening CDP WebSocket')), 10000);
      this.ws.addEventListener('open', () => { clearTimeout(timer); resolve(); }, { once: true });
      this.ws.addEventListener('error', () => { clearTimeout(timer); reject(new Error('CDP WebSocket error')); }, { once: true });
    });
    this.ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const item = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) item.reject(new Error(`${msg.error.message || 'CDP error'} ${JSON.stringify(msg.error.data || '')}`));
        else item.resolve(msg.result || {});
        return;
      }
      if (msg.method && this.listeners.has(msg.method)) {
        for (const listener of this.listeners.get(msg.method)) listener(msg.params || {});
      }
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          reject(new Error(`Timed out waiting for ${method}`));
        }
      }, 30000);
    });
  }
  on(method, fn) {
    if (!this.listeners.has(method)) this.listeners.set(method, new Set());
    this.listeners.get(method).add(fn);
  }
  close() { try { this.ws.close(); } catch {} }
}
async function launchChrome() {
  const chrome = findChrome();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nadlan-action-rail-'));
  const args = [
    '--headless=new', '--remote-debugging-port=0', `--user-data-dir=${userDataDir}`,
    '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
    '--disable-sync', '--mute-audio', 'about:blank',
  ];
  const proc = spawn(chrome, args, { stdio: ['ignore', 'ignore', 'ignore'] });
  const [port] = (await waitForFile(path.join(userDataDir, 'DevToolsActivePort'))).trim().split(/\r?\n/);
  const targets = await fetch(`http://127.0.0.1:${port}/json/list`).then((r) => r.json());
  const page = targets.find((target) => target.type === 'page' && target.webSocketDebuggerUrl);
  return { proc, userDataDir, wsUrl: page.webSocketDebuggerUrl };
}
function cleanup(session) {
  if (!session) return;
  try { session.proc.kill(); } catch {}
  try { fs.rmSync(session.userDataDir, { recursive: true, force: true }); } catch {}
}
function visibleFixedExpression() {
  return `(() => {
    const visible = (el) => {
      const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
      return cs.position === 'fixed' && cs.display !== 'none' && cs.visibility !== 'hidden' && Number(cs.opacity || 1) > 0.01 && r.width > 8 && r.height > 8;
    };
    const items = Array.from(document.querySelectorAll('*')).filter(visible).map((el) => {
      const r = el.getBoundingClientRect();
      return { tag: el.tagName, id: el.id, cls: String(el.className).slice(0,80), text: (el.textContent || '').trim().slice(0,40), left: Math.round(r.left), top: Math.round(r.top), width: Math.round(r.width), height: Math.round(r.height), z: getComputedStyle(el).zIndex };
    });
    return {
      url: location.href,
      title: document.title,
      width: innerWidth,
      height: innerHeight,
      overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      railExists: !!document.querySelector('#nlrx-action-rail'),
      railOpen: !!document.querySelector('#nlrx-action-rail.is-open'),
      launcher: document.querySelector('.nlrx-action-launcher') ? document.querySelector('.nlrx-action-launcher').getBoundingClientRect().toJSON() : null,
      fixedCount: items.length,
      fixed: items,
      consoleErrorCount: window.__nlrxConsoleErrors ? window.__nlrxConsoleErrors.length : 0,
      consoleErrors: window.__nlrxConsoleErrors || []
    };
  })()`;
}
async function capture(client, name) {
  const shot = await client.send('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false });
  const file = path.join(outDir, `${name}.png`);
  fs.writeFileSync(file, Buffer.from(shot.data, 'base64'));
  return path.relative(repo, file).replace(/\\/g, '/');
}
async function main() {
  fs.mkdirSync(outDir, { recursive: true });
  const cssFull = fs.readFileSync(path.join(repo, 'assets/css/nadlan-premium-sitewide.css'), 'utf8');
  const jsFull = fs.readFileSync(path.join(repo, 'assets/js/nadlan-premium-revenue.js'), 'utf8');
  const cssPatch = cssFull.slice(cssFull.indexOf('/* Unified floating action rail'));
  const jsPatch = jsFull.slice(jsFull.indexOf('/* Unified floating action rail'));
  if (!cssPatch || !jsPatch) throw new Error('Local rail patch was not found in theme CSS/JS.');

  let session;
  const report = [];
  try {
    session = await launchChrome();
    const client = new CdpClient(session.wsUrl);
    await client.open();
    await client.send('Page.enable');
    await client.send('Runtime.enable');
    client.on('Runtime.exceptionThrown', (event) => {
      // Stored in-page later through the same array for report simplicity.
      void event;
    });

    for (const page of urls) {
      for (const viewport of viewports) {
        await client.send('Emulation.setDeviceMetricsOverride', {
          width: viewport.width,
          height: viewport.height,
          deviceScaleFactor: viewport.deviceScaleFactor,
          mobile: viewport.mobile,
          screenWidth: viewport.width,
          screenHeight: viewport.height,
        });
        await client.send('Page.navigate', { url: `${page.url}?railqa=${Date.now()}` });
        await delay(2600);
        await client.send('Runtime.evaluate', { expression: `window.scrollTo(0,0); window.__nlrxConsoleErrors=[]; window.addEventListener('error', e => window.__nlrxConsoleErrors.push(String(e.message || e.error || 'error')));`, awaitPromise: false });
        const before = await client.send('Runtime.evaluate', { expression: visibleFixedExpression(), returnByValue: true });
        await client.send('Runtime.evaluate', {
          expression: `(() => { const st=document.createElement('style'); st.id='nlrx-local-rail-css'; st.textContent=${JSON.stringify(cssPatch)}; document.head.appendChild(st); ${jsPatch}; return !!document.querySelector('#nlrx-action-rail'); })()`,
          returnByValue: true,
          awaitPromise: true,
        });
        await delay(500);
        await client.send('Runtime.evaluate', { expression: `window.scrollTo(0,0);`, awaitPromise: false });
        const collapsed = await client.send('Runtime.evaluate', { expression: visibleFixedExpression(), returnByValue: true });
        const collapsedShot = await capture(client, `${page.slug}-${viewport.name}-collapsed`);
        await client.send('Runtime.evaluate', { expression: `document.querySelector('.nlrx-action-launcher')?.click();`, awaitPromise: false });
        await delay(350);
        const open = await client.send('Runtime.evaluate', { expression: visibleFixedExpression(), returnByValue: true });
        const openShot = await capture(client, `${page.slug}-${viewport.name}-open`);
        report.push({ page: page.slug, viewport: viewport.name, before: before.result.value, collapsed: collapsed.result.value, open: open.result.value, screenshots: { collapsed: collapsedShot, open: openShot } });
      }
    }
    client.close();
  } finally {
    cleanup(session);
  }
  const reportPath = path.join(outDir, 'report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ outDir: path.relative(repo, outDir).replace(/\\/g, '/'), report: path.relative(repo, reportPath).replace(/\\/g, '/'), captures: report.length * 2 }, null, 2));
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});