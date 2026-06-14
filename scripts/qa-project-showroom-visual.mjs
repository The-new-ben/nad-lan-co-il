import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

const DEFAULT_SITE = 'https://nad-lan.co.il';
const DEFAULT_SLUG = 'rainbow-tel-aviv';
const DEFAULT_OUT = 'docs/qa/screenshots/rainbow-showroom-visual';

const VIEWPORTS = [
  { name: 'desktop-1440', width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false },
  { name: 'tablet-768', width: 768, height: 1000, deviceScaleFactor: 1, mobile: false },
  { name: 'mobile-390', width: 390, height: 900, deviceScaleFactor: 2, mobile: true },
  {
    name: 'edge-mobile-390',
    width: 390,
    height: 900,
    deviceScaleFactor: 2,
    mobile: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Mobile Safari/537.36 EdgA/125.0',
  },
];

function parseArgs(argv) {
  const out = {
    site: DEFAULT_SITE,
    slug: DEFAULT_SLUG,
    outDir: DEFAULT_OUT,
    strict: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--site') out.site = argv[++i] || out.site;
    else if (a === '--slug') out.slug = argv[++i] || out.slug;
    else if (a === '--out') out.outDir = argv[++i] || out.outDir;
    else if (a === '--strict') out.strict = true;
    else if (a === '--help' || a === '-h') {
      console.log(`Usage:
  node scripts/qa-project-showroom-visual.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv
  node scripts/qa-project-showroom-visual.mjs --strict

Uses local Chrome/Edge headless through the Chrome DevTools Protocol. Set CHROME_PATH to override
the browser executable. Screenshots and report are written under ${DEFAULT_OUT}.`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  out.site = out.site.replace(/\/+$/, '');
  return out;
}

function chromeCandidates() {
  if (process.env.CHROME_PATH) return [process.env.CHROME_PATH];
  if (process.platform === 'win32') {
    return [
      path.join(process.env.ProgramFiles || 'C:\\Program Files', 'Google\\Chrome\\Application\\chrome.exe'),
      path.join(process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)', 'Google\\Chrome\\Application\\chrome.exe'),
      path.join(process.env.LOCALAPPDATA || '', 'Google\\Chrome\\Application\\chrome.exe'),
      path.join(process.env.ProgramFiles || 'C:\\Program Files', 'Microsoft\\Edge\\Application\\msedge.exe'),
      path.join(process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)', 'Microsoft\\Edge\\Application\\msedge.exe'),
    ];
  }
  return ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/microsoft-edge'];
}

function findChrome() {
  const found = chromeCandidates().find((candidate) => candidate && fs.existsSync(candidate));
  if (!found) throw new Error('Could not find Chrome/Edge. Set CHROME_PATH to the browser executable.');
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
      this.ws.addEventListener('error', (event) => {
        clearTimeout(timer);
        reject(new Error(`CDP WebSocket error: ${event.message || 'unknown'}`));
      }, { once: true });
    });
    this.ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(`${msg.error.message || 'CDP error'} ${JSON.stringify(msg.error.data || '')}`));
        else resolve(msg.result || {});
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
    return () => this.listeners.get(method).delete(fn);
  }

  waitFor(method, timeoutMs = 30000) {
    return new Promise((resolve, reject) => {
      const off = this.on(method, (params) => {
        clearTimeout(timer);
        off();
        resolve(params);
      });
      const timer = setTimeout(() => {
        off();
        reject(new Error(`Timed out waiting for event ${method}`));
      }, timeoutMs);
    });
  }

  close() {
    try {
      this.ws.close();
    } catch {
      // ignore cleanup failures
    }
  }
}

async function launchChrome() {
  const chrome = findChrome();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nadlan-showroom-visual-'));
  const args = [
    '--headless=new',
    '--remote-debugging-port=0',
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-networking',
    '--disable-extensions',
    '--disable-sync',
    '--mute-audio',
    'about:blank',
  ];
  const proc = spawn(chrome, args, { stdio: ['ignore', 'ignore', 'ignore'] });
  const portFile = path.join(userDataDir, 'DevToolsActivePort');
  const portText = await waitForFile(portFile);
  const [port] = portText.trim().split(/\r?\n/);
  const targets = await fetch(`http://127.0.0.1:${port}/json/list`).then((r) => r.json());
  const pageTarget = targets.find((target) => target.type === 'page' && target.webSocketDebuggerUrl);
  if (!pageTarget) throw new Error('Chrome opened but no page target was available.');
  return { proc, userDataDir, wsUrl: pageTarget.webSocketDebuggerUrl };
}

function cleanupChrome(session) {
  if (!session) return;
  try {
    session.proc.kill();
  } catch {
    // ignore
  }
  try {
    fs.rmSync(session.userDataDir, { recursive: true, force: true });
  } catch {
    // ignore
  }
}

function metricsExpression() {
  return `(() => {
    const visible = (el) => {
      if (!el) return false;
      const st = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return st.display !== 'none' && st.visibility !== 'hidden' && r.width > 0 && r.height > 0;
    };
    const rect = (el) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: Math.round(r.x * 10) / 10, y: Math.round(r.y * 10) / 10, width: Math.round(r.width * 10) / 10, height: Math.round(r.height * 10) / 10, right: Math.round(r.right * 10) / 10, bottom: Math.round(r.bottom * 10) / 10 };
    };
    const text = document.body ? document.body.innerText : '';
    const root = document.querySelector('.nlp3d-premium,.nlp3d');
    const stage = document.querySelector('.nlp3d-stage-wrap');
    const scene = document.querySelector('.nlp3d-scene');
    const card = document.querySelector('.nlp3d-stage-card');
    const facadeHits = Array.from(document.querySelectorAll('.nlp3d-facade-hit')).filter(visible);
    const facadeCells = Array.from(document.querySelectorAll('.nlp3d-facade-cell')).filter(visible);
    const facadeLabels = Array.from(document.querySelectorAll('.nlp3d-facade-label')).filter(visible);
    const stagePicks = Array.from(document.querySelectorAll('.nlp3d-stage-pick')).filter(visible);
    const picks = facadeHits.length ? facadeHits : (facadeCells.length ? facadeCells : stagePicks);
    const firstPick = picks[0] || null;
    const firstPickRect = firstPick ? firstPick.getBoundingClientRect() : null;
    const activePressedCount = Array.from(document.querySelectorAll('.nlp3d-facade-hit[aria-pressed="true"],.nlp3d-facade-cell[aria-pressed="true"],.nlp3d-stage-pick[aria-pressed="true"]')).filter(visible).length;
    const facadeCellRects = facadeCells.map((el) => {
      const r = el.getBoundingClientRect();
      return { width: r.width, height: r.height };
    });
    const facadeHitRects = facadeHits.map((el) => {
      const r = el.getBoundingClientRect();
      return { width: r.width, height: r.height };
    });
    const minFacadeCellWidth = facadeCellRects.reduce((min, r) => Math.min(min, r.width), facadeCellRects.length ? Infinity : 0);
    const minFacadeCellHeight = facadeCellRects.reduce((min, r) => Math.min(min, r.height), facadeCellRects.length ? Infinity : 0);
    const minFacadeHitWidth = facadeHitRects.reduce((min, r) => Math.min(min, r.width), facadeHitRects.length ? Infinity : 0);
    const minFacadeHitHeight = facadeHitRects.reduce((min, r) => Math.min(min, r.height), facadeHitRects.length ? Infinity : 0);
    const tapTargets = Array.from(document.querySelectorAll('.nlp3d-facade-hit,.nlp3d-facade-cell,.nlp3d-stage-pick,.nlp3d-stage-card-actions button,.nlp3d-lead-form button,.nlp3d-owner-form button,.nlp3d-tool,.nlp3d-view-toggle')).filter(visible).map((el) => {
      const r = el.getBoundingClientRect();
      return { selector: el.className || el.getAttribute('data-action') || el.tagName, width: r.width, height: r.height };
    });
    const minTap = tapTargets.reduce((min, t) => Math.min(min, t.width, t.height), tapTargets.length ? Infinity : 0);
    const h1s = Array.from(document.querySelectorAll('h1')).filter(visible).map((h) => h.innerText.trim()).filter(Boolean);
    const errors = [];
    if (/Fatal error|Stack trace|Warning:|Notice:|Parse error/.test(document.documentElement.innerHTML)) errors.push('php-error-text');
    if (/class=&quot;|nlpf dl rdl|<code>class=/.test(document.documentElement.innerHTML)) errors.push('code-class-leak');
    if (/Ãƒ|Ã‚|\\uFFFD/.test(document.documentElement.innerHTML)) errors.push('mojibake-marker');
    return {
      title: document.title,
      url: location.href,
      viewport: { width: innerWidth, height: innerHeight },
      scroll: { x: document.documentElement.scrollWidth, client: document.documentElement.clientWidth, overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth },
      h1s,
      rootRect: rect(root),
      stageRect: rect(stage),
      sceneRect: rect(scene),
      cardRect: rect(card),
      cardHidden: !card || card.hidden || !visible(card),
      pickCount: picks.length,
      facadeHitCount: facadeHits.length,
      facadeCellCount: facadeCells.length,
      facadeLabelCount: facadeLabels.length,
      activePressedCount,
      facadeCells: {
        minWidth: Math.round(minFacadeCellWidth * 10) / 10,
        minHeight: Math.round(minFacadeCellHeight * 10) / 10
      },
      facadeHits: {
        minWidth: Math.round(minFacadeHitWidth * 10) / 10,
        minHeight: Math.round(minFacadeHitHeight * 10) / 10
      },
      stagePickCount: stagePicks.length,
      recommendedPickCount: picks.filter((p) => p.classList.contains('is-recommended')).length,
      firstPickCenter: firstPickRect ? { x: Math.round(firstPickRect.left + firstPickRect.width / 2), y: Math.round(firstPickRect.top + firstPickRect.height / 2) } : null,
      modelViewerDefined: !!customElements.get('model-viewer'),
      modelViewerCount: document.querySelectorAll('model-viewer').length,
      ownerFormVisible: visible(document.querySelector('.nlp3d-owner-form')),
      leadFormVisible: visible(document.querySelector('.nlp3d-lead-form')),
      tapTargets: { count: tapTargets.length, min: Math.round(minTap * 10) / 10 },
      textSignals: {
        hasBuyerCta: text.includes('דברו איתי על הדירה'),
        hasNonBindingPurchase: text.includes('לא מחייב'),
        hasOwnerCta: text.includes('מציגים פרויקט חדש'),
        hasFacadePrimaryCopy: text.includes('בוחרים על החזית') || text.includes('לחצו על תא דירה בחזית'),
        overpromisesSpinFirst: text.includes('1. מסובבים') || text.includes('בחירת דירה בתלת ממד'),
        hasInternalWords: /לידים|פאנל|CRM|monetization|paid placement/.test(text)
      },
      errors
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

async function waitForIdle(client, ms = 1200) {
  await client.send('Runtime.evaluate', {
    expression: `new Promise((resolve) => setTimeout(resolve, ${ms}))`,
    awaitPromise: true,
  });
}

async function runViewport(client, args, viewport, outDir, pageErrors) {
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: viewport.width,
    height: viewport.height,
    deviceScaleFactor: viewport.deviceScaleFactor,
    mobile: viewport.mobile,
  });
  if (viewport.userAgent) {
    await client.send('Network.setUserAgentOverride', { userAgent: viewport.userAgent });
  }
  const url = `${args.site}/projects/${args.slug}/?cb=${Date.now()}-${viewport.name}`;
  const load = client.waitFor('Page.loadEventFired', 45000).catch(() => null);
  await client.send('Page.navigate', { url });
  await load;
  await waitForIdle(client, 1800);
  await client.send('Runtime.evaluate', {
    expression: `document.querySelector('.nlp3d-premium,.nlp3d')?.scrollIntoView({block:'start', inline:'center'});`,
    awaitPromise: true,
  });
  await waitForIdle(client, 900);

  const before = await evaluateJson(client, metricsExpression());
  if (before.firstPickCenter) {
    await client.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: before.firstPickCenter.x, y: before.firstPickCenter.y });
    await client.send('Input.dispatchMouseEvent', { type: 'mousePressed', button: 'left', clickCount: 1, x: before.firstPickCenter.x, y: before.firstPickCenter.y });
    await client.send('Input.dispatchMouseEvent', { type: 'mouseReleased', button: 'left', clickCount: 1, x: before.firstPickCenter.x, y: before.firstPickCenter.y });
    await waitForIdle(client, 600);
  }
  const after = await evaluateJson(client, metricsExpression());
  const shot = await client.send('Page.captureScreenshot', { format: 'png', fromSurface: true });
  const screenshot = path.join(outDir, `${viewport.name}.png`);
  fs.writeFileSync(screenshot, Buffer.from(shot.data, 'base64'));

  const failures = [];
  if (!after.rootRect) failures.push('showroom root missing');
  if (after.scroll.overflow > 2) failures.push(`horizontal overflow ${after.scroll.overflow}px`);
  if (after.h1s.length !== 1) failures.push(`expected one H1, found ${after.h1s.length}`);
  if (after.pickCount < 1) failures.push('no visible facade/stage apartment selectors');
  if (after.facadeCellCount > 0 && after.facadeLabelCount < Math.min(2, after.facadeCellCount)) failures.push(`facade labels missing (${after.facadeLabelCount}/${after.facadeCellCount})`);
  if (after.facadeCellCount > 0) {
    const minVisualW = viewport.width <= 390 ? 24 : 36;
    const minVisualH = viewport.width <= 390 ? 10 : 14;
    if (after.facadeCells.minWidth < minVisualW || after.facadeCells.minHeight < minVisualH) {
      failures.push(`facade cells too thin (${after.facadeCells.minWidth}x${after.facadeCells.minHeight}px)`);
    }
  }
  if (after.facadeHitCount > 0 && (after.facadeHits.minWidth < 44 || after.facadeHits.minHeight < 44)) {
    failures.push(`facade hit target below 44px (${after.facadeHits.minWidth}x${after.facadeHits.minHeight}px)`);
  }
  if (after.firstPickCenter && after.cardHidden) failures.push('clicking apartment did not reveal selected card');
  if (after.firstPickCenter && after.activePressedCount < 1) failures.push('clicking apartment did not mark a selected apartment control');
  if (after.tapTargets.count && after.tapTargets.min < 44) failures.push(`tap target below 44px (${after.tapTargets.min}px)`);
  if (after.rootRect && viewport.width <= 768 && (after.rootRect.x < -2 || after.rootRect.right > viewport.width + 2)) failures.push(`showroom cropped on mobile/tablet: ${JSON.stringify(after.rootRect)}`);
  if (!after.textSignals.hasFacadePrimaryCopy) failures.push('showroom copy does not lead with facade apartment selection');
  if (after.textSignals.overpromisesSpinFirst) failures.push('showroom copy still leads with spin/3D wording before true per-apartment BIM exists');
  if (after.textSignals.hasInternalWords) failures.push('public text contains internal wording');
  if (after.errors.length) failures.push(`HTML leak markers: ${after.errors.join(', ')}`);
  const viewportErrors = pageErrors.splice(0, pageErrors.length);
  if (viewportErrors.length) failures.push(`console/page errors: ${viewportErrors.slice(0, 3).join(' | ')}`);

  return { name: viewport.name, screenshot, before, after, failures };
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = path.resolve(process.cwd(), args.outDir);
  fs.mkdirSync(outDir, { recursive: true });
  let session = null;
  let client = null;
  const pageErrors = [];
  try {
    session = await launchChrome();
    client = new CdpClient(session.wsUrl);
    await client.open();
    await client.send('Page.enable');
    await client.send('Runtime.enable');
    await client.send('Log.enable');
    await client.send('Network.enable');
    client.on('Runtime.exceptionThrown', (params) => {
      const text = params.exceptionDetails?.text || params.exceptionDetails?.exception?.description || 'runtime exception';
      pageErrors.push(text);
    });
    client.on('Log.entryAdded', (params) => {
      const entry = params.entry || {};
      if (entry.level === 'error') pageErrors.push(entry.text || 'log error');
    });

    const viewports = [];
    for (const viewport of VIEWPORTS) {
      viewports.push(await runViewport(client, args, viewport, outDir, pageErrors));
    }
    const failed = viewports.filter((v) => v.failures.length);
    const report = {
      site: args.site,
      slug: args.slug,
      generated_at: new Date().toISOString(),
      out_dir: args.outDir,
      summary: { passed: viewports.length - failed.length, failed: failed.length },
      viewports,
    };
    fs.writeFileSync(path.join(outDir, 'report.json'), `${JSON.stringify(report, null, 2)}\n`);
    console.log(JSON.stringify(report, null, 2));
    if (args.strict && failed.length) process.exitCode = 1;
  } finally {
    if (client) client.close();
    cleanupChrome(session);
  }
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
