#!/usr/bin/env node
/**
 * Local browser gate for the Rainbow GLB prototype preview.
 *
 * This runs before the CMS wire-in exists on production. It proves that the
 * committed model/poster/preview assets render in a real browser at desktop
 * and mobile widths, that hotspots exist, and that a buyer action changes the
 * selected-unit readout.
 */

import { spawn } from 'node:child_process';
import { createReadStream, existsSync } from 'node:fs';
import { mkdir, writeFile } from 'node:fs/promises';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DEFAULT_PREVIEW = '/docs/previews/rainbow-model-viewer-prototype.html';
const DEFAULT_OUT = 'docs/qa/screenshots-rainbow-prototype-preview';

function parseArgs(argv) {
  const args = {
    preview: DEFAULT_PREVIEW,
    out: DEFAULT_OUT,
    keepBrowser: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--preview') args.preview = argv[++i];
    else if (arg === '--out') args.out = argv[++i];
    else if (arg === '--keep-browser') args.keepBrowser = true;
    else if (arg === '--help') {
      console.log('Usage: node scripts/check-rainbow-prototype-preview.mjs [--preview PATH] [--out DIR]');
      process.exit(0);
    }
  }
  return args;
}

function chromeCandidates() {
  const env = process.env.CHROME_PATH ? [process.env.CHROME_PATH] : [];
  if (process.platform === 'win32') {
    return [
      ...env,
      'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
      `${process.env.LOCALAPPDATA || ''}\\Google\\Chrome\\Application\\chrome.exe`,
      'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
      'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    ];
  }
  if (process.platform === 'darwin') {
    return [
      ...env,
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
    ];
  }
  return [
    ...env,
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/usr/bin/microsoft-edge',
  ];
}

function findChrome() {
  const found = chromeCandidates().find((candidate) => candidate && existsSync(candidate));
  if (!found) throw new Error('Chrome/Edge executable not found. Set CHROME_PATH to run this gate.');
  return found;
}

function mimeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.html') return 'text/html; charset=utf-8';
  if (ext === '.js' || ext === '.mjs') return 'text/javascript; charset=utf-8';
  if (ext === '.css') return 'text/css; charset=utf-8';
  if (ext === '.json') return 'application/json; charset=utf-8';
  if (ext === '.png') return 'image/png';
  if (ext === '.svg') return 'image/svg+xml; charset=utf-8';
  if (ext === '.glb') return 'model/gltf-binary';
  if (ext === '.gltf') return 'model/gltf+json';
  return 'application/octet-stream';
}

function startStaticServer(root) {
  const server = http.createServer((request, response) => {
    try {
      const url = new URL(request.url || '/', 'http://127.0.0.1');
      const decoded = decodeURIComponent(url.pathname);
      const normalized = path.normalize(decoded).replace(/^([/\\])+/, '');
      const filePath = path.resolve(root, normalized || 'index.html');
      if (!filePath.startsWith(root) || !existsSync(filePath)) {
        response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        response.end('not found');
        return;
      }
      response.writeHead(200, {
        'Content-Type': mimeFor(filePath),
        'Cache-Control': 'no-store',
        'Access-Control-Allow-Origin': '*',
      });
      createReadStream(filePath).pipe(response);
    } catch (error) {
      response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end(String(error?.stack || error));
    }
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      resolve({ server, port: address.port });
    });
  });
}

async function waitForJson(url, timeoutMs = 10000) {
  const start = Date.now();
  let lastError;
  while (Date.now() - start < timeoutMs) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
      lastError = new Error(`HTTP ${response.status}`);
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolve) => setTimeout(resolve, 150));
  }
  throw lastError || new Error(`Timed out waiting for ${url}`);
}

async function createTarget(port, url) {
  const endpoint = `http://127.0.0.1:${port}/json/new?${encodeURIComponent(url)}`;
  let response = await fetch(endpoint, { method: 'PUT' });
  if (!response.ok) response = await fetch(endpoint);
  if (!response.ok) throw new Error(`Could not create Chrome target: HTTP ${response.status}`);
  return response.json();
}

class CdpTarget {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.nextId = 1;
    this.pending = new Map();
    this.events = [];
  }

  async open() {
    await new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });
    this.ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(`${msg.error.message || 'CDP error'} ${JSON.stringify(msg.error)}`));
        else resolve(msg.result);
        return;
      }
      if (msg.method) this.events.push(msg);
    });
  }

  send(method, params = {}) {
    const id = this.nextId++;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
    });
  }

  close() {
    this.ws.close();
  }
}

const PRELOAD = `
  window.__rainbowPreviewErrors = [];
  window.addEventListener('error', (event) => {
    window.__rainbowPreviewErrors.push(String(event.message || event.error || 'error').slice(0, 160));
  });
  window.addEventListener('unhandledrejection', (event) => {
    window.__rainbowPreviewErrors.push(String(event.reason || 'unhandled rejection').slice(0, 160));
  });
`;

const WAIT_MODEL_EXPRESSION = `(async () => {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const start = Date.now();
  while (Date.now() - start < 25000) {
    const model = document.querySelector('model-viewer');
    if (customElements.get('model-viewer') && model) {
      if (typeof model.dismissPoster === 'function') {
        try { model.dismissPoster(); } catch (error) {}
      }
      if (model.loaded || model.modelIsVisible || model.getAttribute('loaded') !== null) {
        return true;
      }
    }
    await sleep(250);
  }
  return false;
})()`;

const WAIT_DATA_EXPRESSION = `(async () => {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const start = Date.now();
  while (Date.now() - start < 10000) {
    if (window.__rainbowPreviewDataReady === true) return true;
    if (window.__rainbowPreviewDataReady === false) return false;
    await sleep(150);
  }
  return false;
})()`;

const METRICS_EXPRESSION = `(() => {
  const rect = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return {
      x: Math.round(r.x),
      y: Math.round(r.y),
      width: Math.round(r.width),
      height: Math.round(r.height),
      display: s.display,
      visibility: s.visibility,
      opacity: Number(s.opacity || 0),
    };
  };
  const visible = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && s.display !== 'none' && s.visibility !== 'hidden' && Number(s.opacity || 0) > 0.01;
  };
  const model = document.querySelector('model-viewer');
  const stage = document.querySelector('.stage');
  const hotspots = Array.from(document.querySelectorAll('[data-unit]'));
  const smallTargets = hotspots.filter((el) => {
    if (!visible(el)) return false;
    const r = el.getBoundingClientRect();
    return r.width < 44 || r.height < 44;
  }).map((el) => {
    const r = el.getBoundingClientRect();
    return { unit: el.getAttribute('data-unit'), width: Math.round(r.width), height: Math.round(r.height) };
  });
  return {
    title: document.title,
    lang: document.documentElement.lang,
    dir: document.documentElement.dir,
    viewport: { width: innerWidth, height: innerHeight },
    scrollWidth: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
    overflowX: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - innerWidth,
    h1: Array.from(document.querySelectorAll('h1')).map((el) => (el.innerText || '').trim()).filter(Boolean),
    stageRect: rect(stage),
    modelRect: rect(model),
    modelDefined: Boolean(customElements.get('model-viewer')),
    modelLoaded: Boolean(model && (model.loaded || model.modelIsVisible || model.getAttribute('loaded') !== null)),
    hotspots: hotspots.length,
    visibleHotspots: hotspots.filter(visible).length,
    smallTargets,
    errors: window.__rainbowPreviewErrors || [],
    bodyHasFatal: /Fatal error|Parse error|Warning:/.test(document.body?.innerText || ''),
    dataReady: window.__rainbowPreviewDataReady === true,
    insightsRect: rect(document.querySelector('.insights')),
    drawingCards: document.querySelectorAll('[data-preview-drawing]').length,
    environmentCards: document.querySelectorAll('[data-preview-environment-item]').length,
    mediaSlots: document.querySelectorAll('[data-preview-media-slot]').length,
    pendingMediaSlots: document.querySelectorAll('[data-preview-media-slot][data-state="pending"]').length,
    viewLayerUserOpenOnly: document.querySelector('[data-preview-view-layer]')?.dataset.userOpenOnly === 'true',
  };
})()`;

const INTERACTION_EXPRESSION = `(() => {
  const button = document.querySelector('[data-unit]');
  const before = (document.querySelector('#readout')?.innerText || '').trim();
  if (button) button.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
  const after = (document.querySelector('#readout')?.innerText || '').trim();
  return {
    attempted: Boolean(button),
    targetUnit: button ? button.getAttribute('data-unit') : '',
    before,
    after,
    changed: Boolean(button && after && after !== before && after.includes('CMS')),
  };
})()`;

function evaluate(metrics, interaction) {
  const checks = [];
  const add = (status, name, detail) => checks.push({ status, name, detail });
  add(metrics.h1.length === 1 ? 'PASS' : 'FAIL', 'single preview H1', `${metrics.h1.length}`);
  add(metrics.dir === 'rtl' ? 'PASS' : 'FAIL', 'RTL document', metrics.dir || '(empty)');
  add(metrics.overflowX <= 2 ? 'PASS' : 'FAIL', 'no horizontal overflow', `${metrics.overflowX}px`);
  add(metrics.modelDefined ? 'PASS' : 'FAIL', 'model-viewer custom element defined', String(metrics.modelDefined));
  const modelVisible = metrics.modelRect && metrics.modelRect.width >= 320 && metrics.modelRect.height >= 320;
  add(modelVisible ? 'PASS' : 'FAIL', 'model-viewer visible area', JSON.stringify(metrics.modelRect));
  add(metrics.modelLoaded ? 'PASS' : 'FAIL', 'GLB loaded/revealed', String(metrics.modelLoaded));
  add(metrics.hotspots >= 6 ? 'PASS' : 'FAIL', 'hotspots present', `${metrics.hotspots}`);
  add(metrics.visibleHotspots >= 1 ? 'PASS' : 'WARN', 'at least one visible hotspot', `${metrics.visibleHotspots}`);
  add(metrics.smallTargets.length === 0 ? 'PASS' : 'FAIL', '44px hotspot targets', metrics.smallTargets.length ? JSON.stringify(metrics.smallTargets) : 'all visible hotspots >=44px');
  add(interaction.changed ? 'PASS' : 'FAIL', 'hotspot click updates readout', JSON.stringify(interaction));
  add(metrics.errors.length === 0 ? 'PASS' : 'FAIL', 'no browser errors', metrics.errors.join(' | ') || 'none');
  add(metrics.bodyHasFatal ? 'FAIL' : 'PASS', 'no visible fatal text', metrics.bodyHasFatal ? 'fatal text found' : 'none');
  add(metrics.dataReady ? 'PASS' : 'FAIL', 'CMS-backed preview data loaded', String(metrics.dataReady));
  const insightsVisible = metrics.insightsRect && metrics.insightsRect.width >= 320 && metrics.insightsRect.height >= 160;
  add(insightsVisible ? 'PASS' : 'FAIL', 'material insight panels visible', JSON.stringify(metrics.insightsRect));
  add(metrics.drawingCards >= 3 ? 'PASS' : 'FAIL', 'drawing cards rendered', `${metrics.drawingCards}`);
  add(metrics.environmentCards >= 6 ? 'PASS' : 'FAIL', 'surroundings cards rendered', `${metrics.environmentCards}`);
  add(metrics.mediaSlots === 3 ? 'PASS' : 'FAIL', 'media/view slots rendered', `${metrics.mediaSlots} slots, ${metrics.pendingMediaSlots} pending`);
  add(metrics.viewLayerUserOpenOnly ? 'PASS' : 'FAIL', 'view layer stays user-opened/lazy', String(metrics.viewLayerUserOpenOnly));
  return checks;
}

async function runViewport(chromePort, url, outDir, viewport) {
  const target = await createTarget(chromePort, 'about:blank');
  const cdp = new CdpTarget(target.webSocketDebuggerUrl);
  await cdp.open();
  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: PRELOAD });
  await cdp.send('Emulation.setDeviceMetricsOverride', {
    width: viewport.width,
    height: viewport.height,
    deviceScaleFactor: viewport.scale || 1,
    mobile: Boolean(viewport.mobile),
  });
  if (viewport.userAgent) {
    await cdp.send('Network.setUserAgentOverride', { userAgent: viewport.userAgent });
  }
  await cdp.send('Page.navigate', { url });
  await cdp.send('Runtime.evaluate', {
    expression: WAIT_MODEL_EXPRESSION,
    awaitPromise: true,
    returnByValue: true,
  });
  await cdp.send('Runtime.evaluate', {
    expression: WAIT_DATA_EXPRESSION,
    awaitPromise: true,
    returnByValue: true,
  });
  const interactionResult = await cdp.send('Runtime.evaluate', {
    expression: INTERACTION_EXPRESSION,
    returnByValue: true,
  });
  const metricsResult = await cdp.send('Runtime.evaluate', {
    expression: METRICS_EXPRESSION,
    returnByValue: true,
  });
  const metrics = metricsResult.result.value;
  const interaction = interactionResult.result.value;
  const screenshot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  const screenshotPath = path.join(outDir, `${viewport.name}.png`);
  await writeFile(screenshotPath, Buffer.from(screenshot.data, 'base64'));
  cdp.close();
  return {
    viewport: viewport.name,
    screenshot: path.relative(ROOT, screenshotPath).replaceAll('\\', '/'),
    metrics,
    interaction,
    checks: evaluate(metrics, interaction),
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const outDir = path.resolve(ROOT, args.out);
  await mkdir(outDir, { recursive: true });

  const { server, port: staticPort } = await startStaticServer(ROOT);
  const url = `http://127.0.0.1:${staticPort}${args.preview.startsWith('/') ? args.preview : `/${args.preview}`}`;
  const chrome = findChrome();
  const chromePort = 9400 + Math.floor(Math.random() * 400);
  const userDataDir = path.join(os.tmpdir(), `rainbow-prototype-preview-${Date.now()}`);
  const proc = spawn(chrome, [
    '--headless=new',
    `--remote-debugging-port=${chromePort}`,
    `--user-data-dir=${userDataDir}`,
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });

  try {
    await waitForJson(`http://127.0.0.1:${chromePort}/json/version`);
    const viewports = [
      { name: 'prototype-desktop-1440', width: 1440, height: 1000, scale: 1 },
      {
        name: 'prototype-mobile-390',
        width: 390,
        height: 1000,
        scale: 2,
        mobile: true,
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
      },
    ];
    const results = [];
    for (const viewport of viewports) {
      results.push(await runViewport(chromePort, url, outDir, viewport));
    }
    const reportPath = path.join(outDir, 'rainbow-prototype-preview-report.json');
    await writeFile(reportPath, `${JSON.stringify({ url, results }, null, 2)}\n`, 'utf8');
    let failed = false;
    for (const result of results) {
      console.log(`\n# ${result.viewport}`);
      console.log(`screenshot: ${result.screenshot}`);
      for (const check of result.checks) {
        console.log(`[${check.status}] ${check.name}: ${check.detail}`);
        if (check.status === 'FAIL') failed = true;
      }
    }
    console.log(`\nReport: ${path.relative(ROOT, reportPath).replaceAll('\\', '/')}`);
    process.exitCode = failed ? 1 : 0;
  } finally {
    if (!args.keepBrowser) proc.kill();
    server.close();
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
