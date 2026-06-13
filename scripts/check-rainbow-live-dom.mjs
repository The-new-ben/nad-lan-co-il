#!/usr/bin/env node
/**
 * Live DOM/browser gate for the Rainbow showroom.
 *
 * Dependency-free: uses Chrome/Edge DevTools Protocol directly, not Playwright.
 * It captures screenshots and checks the rendered page at desktop/mobile sizes.
 */

import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const DEFAULT_URL = 'https://nad-lan.co.il/projects/rainbow-tel-aviv/';
const DEFAULT_OUT = 'docs/qa/screenshots-rainbow-live-dom';

function parseArgs(argv) {
  const args = {
    url: `${DEFAULT_URL}?cb=${Date.now()}`,
    out: DEFAULT_OUT,
    expectGlb: false,
    keepBrowser: false,
    fullPage: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--url') args.url = argv[++i];
    else if (arg === '--out') args.out = argv[++i];
    else if (arg === '--expect-glb') args.expectGlb = true;
    else if (arg === '--keep-browser') args.keepBrowser = true;
    else if (arg === '--full-page') args.fullPage = true;
    else if (arg === '--help') {
      console.log(`Usage: node scripts/check-rainbow-live-dom.mjs [--url URL] [--out DIR] [--expect-glb] [--full-page]`);
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
  if (!found) {
    throw new Error('Chrome/Edge executable not found. Set CHROME_PATH to run the live DOM gate.');
  }
  return found;
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
      }
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

async function waitForLoad(cdp) {
  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', {
    source: 'Object.defineProperty(navigator, "webdriver", {get: () => false});',
  });
  await new Promise((resolve) => setTimeout(resolve, 4000));
  await cdp.send('Runtime.evaluate', {
    expression: 'document.readyState',
    returnByValue: true,
  });
}

const METRICS_EXPRESSION = `(() => {
  const rect = (el) => {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return {
      x: Math.round(r.x),
      y: Math.round(r.y),
      width: Math.round(r.width),
      height: Math.round(r.height),
      display: style.display,
      visibility: style.visibility,
      opacity: Number(style.opacity || 0),
    };
  };
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && s.display !== 'none' && s.visibility !== 'hidden' && Number(s.opacity || 0) > 0.01;
  };
  const q = (s) => document.querySelector(s);
  const qa = (s) => Array.from(document.querySelectorAll(s));
  const bodyText = document.body ? document.body.innerText || '' : '';
  const nlp3d = q('.nlp3d');
  const stage = q('.nlp3d-stage-wrap, .nlp3d-stage, .nlp3d-model-shell, .nlp3d-model-viewer, .nlp3d');
  const model = q('model-viewer');
  const featured = q('.wp-block-post-featured-image');
  const rawLeakPatterns = ['class="nlpf', "class='nlpf", 'function(', 'const ', '<script', '</div>'];
  const tapSmall = qa('.nlp3d button, .nlp3d a, .nlp3d input, .nlp3d [role="button"]').filter((el) => {
    if (!visible(el)) return false;
    const r = el.getBoundingClientRect();
    return r.width < 44 || r.height < 44;
  }).slice(0, 20).map((el) => {
    const r = el.getBoundingClientRect();
    return {
      tag: el.tagName.toLowerCase(),
      text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim().slice(0, 40),
      width: Math.round(r.width),
      height: Math.round(r.height),
      className: String(el.className || '').slice(0, 80),
    };
  });
  return {
    url: location.href,
    title: document.title,
    dir: document.documentElement.dir || document.body.dir || '',
    viewport: { width: innerWidth, height: innerHeight },
    scroll: {
      width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
      height: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
      overflowX: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - innerWidth,
    },
    h1: qa('h1').map((el) => (el.innerText || '').trim()).filter(Boolean),
    hasNlp3d: Boolean(nlp3d),
    nlp3dRect: rect(nlp3d),
    stageRect: rect(stage),
    hasModelViewer: Boolean(model),
    modelViewerRect: rect(model),
    hasFallbackTower: Boolean(q('.nlp3d-building, .nlp3d-tower, .nlp3d-facade, .nlp3d-floor-stack')),
    hasMapboxCanvas: Boolean(q('.mapboxgl-canvas')),
    hasUnitButtons: qa('.nlp3d button, .nlp3d [role="button"]').length,
    featuredImageRect: rect(featured),
    featuredImageVisible: Boolean(featured && visible(featured)),
    rawLeak: rawLeakPatterns.filter((pattern) => bodyText.includes(pattern)),
    smallTapTargets: tapSmall,
    pageErrorsVisible: bodyText.includes('Fatal error') || bodyText.includes('Warning:') || bodyText.includes('Parse error'),
  };
})()`;

function evaluateChecks(metrics, expectGlb) {
  const checks = [];
  const add = (status, name, detail) => checks.push({ status, name, detail });
  add(metrics.h1.length === 1 ? 'PASS' : 'FAIL', 'single H1', `${metrics.h1.length}`);
  add(metrics.hasNlp3d ? 'PASS' : 'FAIL', 'showroom present', String(metrics.hasNlp3d));
  add(metrics.scroll.overflowX <= 2 ? 'PASS' : 'FAIL', 'no horizontal overflow', `${metrics.scroll.overflowX}px`);
  add(metrics.rawLeak.length === 0 ? 'PASS' : 'FAIL', 'no raw code leak', metrics.rawLeak.join(', ') || 'none');
  add(metrics.pageErrorsVisible ? 'FAIL' : 'PASS', 'no visible PHP/JS error text', metrics.pageErrorsVisible ? 'error text found' : 'none');
  if (expectGlb) {
    const goodModel = metrics.hasModelViewer && metrics.modelViewerRect && metrics.modelViewerRect.width >= 300 && metrics.modelViewerRect.height >= 280;
    add(goodModel ? 'PASS' : 'FAIL', 'model-viewer visible', JSON.stringify(metrics.modelViewerRect));
  } else {
    add(metrics.hasModelViewer ? 'PASS' : 'WARN', 'model-viewer visible', metrics.hasModelViewer ? JSON.stringify(metrics.modelViewerRect) : 'not wired yet');
  }
  add(metrics.hasFallbackTower || metrics.hasModelViewer ? 'PASS' : 'FAIL', 'model or fallback visible', `fallback=${metrics.hasFallbackTower}, model=${metrics.hasModelViewer}`);
  add(metrics.featuredImageVisible ? 'WARN' : 'PASS', 'static featured image suppressed', metrics.featuredImageVisible ? JSON.stringify(metrics.featuredImageRect) : 'not visible');
  add(metrics.smallTapTargets.length === 0 ? 'PASS' : 'WARN', '44px tap targets in showroom', metrics.smallTapTargets.length ? JSON.stringify(metrics.smallTapTargets.slice(0, 5)) : 'all visible targets >=44px');
  return checks;
}

async function runViewport(browserPort, url, outDir, viewport, expectGlb, fullPage) {
  const target = await createTarget(browserPort, 'about:blank');
  const cdp = new CdpTarget(target.webSocketDebuggerUrl);
  await cdp.open();
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
  await waitForLoad(cdp);
  const evalResult = await cdp.send('Runtime.evaluate', {
    expression: METRICS_EXPRESSION,
    returnByValue: true,
    awaitPromise: true,
  });
  const metrics = evalResult.result.value;
  const screenshot = await cdp.send('Page.captureScreenshot', {
    format: 'png',
    captureBeyondViewport: Boolean(fullPage),
  });
  const screenshotPath = path.join(outDir, `${viewport.name}.png`);
  await writeFile(screenshotPath, Buffer.from(screenshot.data, 'base64'));
  cdp.close();
  return {
    viewport: viewport.name,
    screenshot: screenshotPath.replaceAll('\\\\', '/'),
    metrics,
    checks: evaluateChecks(metrics, expectGlb),
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const chrome = findChrome();
  const userDataDir = path.join(os.tmpdir(), `rainbow-live-dom-${Date.now()}`);
  const port = 9300 + Math.floor(Math.random() * 500);
  await mkdir(args.out, { recursive: true });
  const proc = spawn(chrome, [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--hide-scrollbars=false',
    'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });

  try {
    await waitForJson(`http://127.0.0.1:${port}/json/version`);
    const viewports = [
      { name: 'desktop-1440', width: 1440, height: 1200, scale: 1 },
      {
        name: 'mobile-390',
        width: 390,
        height: 1200,
        scale: 2,
        mobile: true,
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
      },
    ];
    const results = [];
    for (const viewport of viewports) {
      results.push(await runViewport(port, args.url, args.out, viewport, args.expectGlb, args.fullPage));
    }
    const reportPath = path.join(args.out, 'rainbow-live-dom-report.json');
    await writeFile(reportPath, `${JSON.stringify({ url: args.url, expectGlb: args.expectGlb, results }, null, 2)}\n`, 'utf8');
    let failed = false;
    for (const result of results) {
      console.log(`\n# ${result.viewport}`);
      console.log(`screenshot: ${result.screenshot}`);
      for (const check of result.checks) {
        console.log(`[${check.status}] ${check.name}: ${check.detail}`);
        if (check.status === 'FAIL') failed = true;
      }
    }
    console.log(`\nReport: ${reportPath.replaceAll('\\\\', '/')}`);
    process.exitCode = failed ? 1 : 0;
  } finally {
    if (!args.keepBrowser) proc.kill();
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exit(1);
});
