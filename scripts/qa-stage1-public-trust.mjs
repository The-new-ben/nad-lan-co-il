import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

const repo = path.resolve(import.meta.dirname, '..');
const site = 'https://nad-lan.co.il';

const pages = [
  { name: 'home', url: '/' },
  { name: 'join-pro', url: '/join-pro/' },
  { name: 'sitemap', url: '/sitemap/' },
  { name: 'professionals', url: '/professionals/' },
  { name: 'dimri-yama-sde-dov', url: '/projects/dimri-yama-sde-dov/' },
];

const viewports = [
  { name: 'desktop-1440', width: 1440, height: 1000, mobile: false, deviceScaleFactor: 1 },
  { name: 'tablet-768', width: 768, height: 1000, mobile: false, deviceScaleFactor: 1 },
  { name: 'mobile-390', width: 390, height: 900, mobile: true, deviceScaleFactor: 2 },
];

function parseArgs(argv) {
  const out = { phase: 'before', outDir: '' };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--phase') out.phase = argv[++i] || out.phase;
    else if (arg === '--out') out.outDir = argv[++i] || out.outDir;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  if (!out.outDir) out.outDir = `docs/qa/screenshots/stage1-public-trust-${out.phase}`;
  return out;
}

function chromeCandidates() {
  if (process.env.CHROME_PATH) return [process.env.CHROME_PATH];
  if (process.platform === 'win32') {
    return [
      path.join(process.env.ProgramFiles || 'C:\\Program Files', 'Google\\Chrome\\Application\\chrome.exe'),
      path.join(process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)', 'Google\\Chrome\\Application\\chrome.exe'),
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

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForFile(file, timeoutMs = 10000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    if (fs.existsSync(file)) return fs.readFileSync(file, 'utf8');
    await delay(100);
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
      this.ws.addEventListener('open', () => {
        clearTimeout(timer);
        resolve();
      }, { once: true });
      this.ws.addEventListener('error', () => {
        clearTimeout(timer);
        reject(new Error('CDP WebSocket error'));
      }, { once: true });
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

  close() {
    try { this.ws.close(); } catch {}
  }
}

async function launchChrome() {
  const chrome = findChrome();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nadlan-stage1-trust-'));
  const proc = spawn(chrome, [
    '--headless=new',
    '--remote-debugging-port=0',
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-networking',
    '--disable-sync',
    '--mute-audio',
    'about:blank',
  ], { stdio: ['ignore', 'ignore', 'ignore'] });
  const [port] = (await waitForFile(path.join(userDataDir, 'DevToolsActivePort'))).trim().split(/\r?\n/);
  const targets = await fetch(`http://127.0.0.1:${port}/json/list`).then((response) => response.json());
  const page = targets.find((target) => target.type === 'page' && target.webSocketDebuggerUrl);
  if (!page) throw new Error('Chrome opened but no page target was available.');
  return { proc, userDataDir, wsUrl: page.webSocketDebuggerUrl };
}

function cleanup(session) {
  if (!session) return;
  try { session.proc.kill(); } catch {}
  try { fs.rmSync(session.userDataDir, { recursive: true, force: true }); } catch {}
}

function pageAuditExpression() {
  return `(() => {
    const visible = (el) => {
      if (!el) return false;
      const st = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return st.display !== 'none' && st.visibility !== 'hidden' && r.width > 0 && r.height > 0;
    };
    const html = document.documentElement.innerHTML || '';
    const text = document.body ? document.body.innerText || '' : '';
    const terms = [
      'WooCommerce',
      'woocommerce',
      'cart',
      'checkout',
      'Checkout',
      'my account',
      'Notifications',
      'notifications',
      'debug',
      'coming soon',
      'Coming soon',
      'More posts',
      'עמודי התשלום',
      'לא מוכנים',
      'עודכן לאחרונה: -',
      '...עמודים',
      '...אשכולות'
    ];
    const matches = [];
    for (const term of terms) {
      const textIndex = text.indexOf(term);
      const htmlIndex = html.indexOf(term);
      if (textIndex >= 0 || htmlIndex >= 0) {
        const source = textIndex >= 0 ? text : html;
        const index = textIndex >= 0 ? textIndex : htmlIndex;
        matches.push({
          term,
          source: textIndex >= 0 ? 'visibleText' : 'html',
          snippet: source.slice(Math.max(0, index - 90), index + term.length + 120).replace(/\\s+/g, ' ').trim(),
        });
      }
    }
    const wooSelectors = [
      '.woocommerce-notices-wrapper',
      '.woocommerce-message',
      '.woocommerce-info',
      '.woocommerce-error',
      '.wc-block-mini-cart',
      '.wc-block-cart',
      '.wp-block-woocommerce-mini-cart',
      '[class*="woocommerce"]',
      '[class*="wc-block"]'
    ];
    const components = [];
    for (const selector of wooSelectors) {
      const nodes = Array.from(document.querySelectorAll(selector)).filter(visible);
      if (nodes.length) {
        components.push({
          selector,
          count: nodes.length,
          samples: nodes.slice(0, 3).map((node) => (node.innerText || node.textContent || node.className || '').trim().slice(0, 180)),
        });
      }
    }
    const h1s = Array.from(document.querySelectorAll('h1')).filter(visible).map((node) => node.innerText.trim()).filter(Boolean);
    const buttons = Array.from(document.querySelectorAll('a,button')).filter(visible).map((node) => ({
      text: (node.innerText || node.textContent || node.getAttribute('aria-label') || '').trim().slice(0, 80),
      href: node.getAttribute('href') || '',
      className: String(node.className || '').slice(0, 100),
    })).filter((item) => /cart|checkout|add-to-cart|woocommerce|coming soon|debug|More posts/i.test(item.text + ' ' + item.href + ' ' + item.className));
    const width = document.documentElement.clientWidth;
    return {
      title: document.title,
      url: location.href,
      viewport: { width: innerWidth, height: innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: width,
      horizontalOverflow: document.documentElement.scrollWidth - width,
      h1s,
      matches,
      components,
      suspiciousButtons: buttons.slice(0, 12),
      bodyTextStart: text.slice(0, 500).replace(/\\s+/g, ' ').trim(),
      visibleLeakCount: matches.filter((match) => match.source === 'visibleText').length + components.length + buttons.length,
    };
  })()`;
}

async function evaluateJson(client, expression) {
  const res = await client.send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  return res.result ? res.result.value : null;
}

async function capturePage(client, page, viewport, outDir, phase, consoleErrors, networkFailures) {
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: viewport.width,
    height: viewport.height,
    deviceScaleFactor: viewport.deviceScaleFactor,
    mobile: viewport.mobile,
  });
  const url = `${site}${page.url}?stage1qa=${phase}-${Date.now()}-${viewport.name}`;
  const load = new Promise((resolve) => {
    const timeout = setTimeout(resolve, 30000);
    client.on('Page.loadEventFired', () => {
      clearTimeout(timeout);
      resolve();
    });
  });
  await client.send('Page.navigate', { url });
  await load;
  await delay(1800);
  await client.send('Runtime.evaluate', { expression: 'window.scrollTo(0,0)', awaitPromise: true });
  await delay(350);
  const audit = await evaluateJson(client, pageAuditExpression());
  const shot = await client.send('Page.captureScreenshot', {
    format: 'png',
    fromSurface: true,
    captureBeyondViewport: true,
  });
  const screenshot = path.join(outDir, `${page.name}-${viewport.name}.png`);
  fs.writeFileSync(screenshot, Buffer.from(shot.data, 'base64'));
  return {
    page: page.name,
    viewport: viewport.name,
    screenshot: path.relative(repo, screenshot).replace(/\\/g, '/'),
    audit,
    consoleErrors: consoleErrors.splice(0, consoleErrors.length),
    networkFailures: networkFailures.splice(0, networkFailures.length).slice(0, 20),
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = path.resolve(repo, args.outDir);
  fs.mkdirSync(outDir, { recursive: true });
  let session;
  let client;
  const consoleErrors = [];
  const networkFailures = [];
  try {
    session = await launchChrome();
    client = new CdpClient(session.wsUrl);
    await client.open();
    await client.send('Page.enable');
    await client.send('Runtime.enable');
    await client.send('Log.enable');
    await client.send('Network.enable');
    client.on('Runtime.exceptionThrown', (event) => {
      consoleErrors.push(event.exceptionDetails?.exception?.description || event.exceptionDetails?.text || 'runtime exception');
    });
    client.on('Log.entryAdded', (event) => {
      if (event.entry?.level === 'error') consoleErrors.push(event.entry.text || 'log error');
    });
    client.on('Network.loadingFailed', (event) => {
      networkFailures.push({ url: event.requestId, errorText: event.errorText, canceled: event.canceled });
    });
    const results = [];
    for (const page of pages) {
      for (const viewport of viewports) {
        results.push(await capturePage(client, page, viewport, outDir, args.phase, consoleErrors, networkFailures));
      }
    }
    const summary = {
      phase: args.phase,
      generatedAt: new Date().toISOString(),
      outDir: path.relative(repo, outDir).replace(/\\/g, '/'),
      pages: pages.map((page) => page.url),
      viewports: viewports.map((viewport) => viewport.name),
      leakCount: results.reduce((sum, item) => sum + item.audit.matches.length + item.audit.components.length + item.audit.suspiciousButtons.length, 0),
      visibleLeakCount: results.reduce((sum, item) => sum + item.audit.visibleLeakCount, 0),
      overflowCount: results.filter((item) => item.audit.horizontalOverflow > 2).length,
      consoleErrorCount: results.reduce((sum, item) => sum + item.consoleErrors.length, 0),
      results,
    };
    fs.writeFileSync(path.join(outDir, 'report.json'), `${JSON.stringify(summary, null, 2)}\n`);
    console.log(JSON.stringify({
      phase: summary.phase,
      outDir: summary.outDir,
      screenshots: results.length,
      leakCount: summary.leakCount,
      visibleLeakCount: summary.visibleLeakCount,
      overflowCount: summary.overflowCount,
      consoleErrorCount: summary.consoleErrorCount,
    }, null, 2));
  } finally {
    if (client) client.close();
    cleanup(session);
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
