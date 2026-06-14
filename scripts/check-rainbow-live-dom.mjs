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
    expectMaterials: false,
    keepBrowser: false,
    fullPage: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--url') args.url = argv[++i];
    else if (arg === '--out') args.out = argv[++i];
    else if (arg === '--expect-glb') args.expectGlb = true;
    else if (arg === '--expect-materials') args.expectMaterials = true;
    else if (arg === '--keep-browser') args.keepBrowser = true;
    else if (arg === '--full-page') args.fullPage = true;
    else if (arg === '--help') {
      console.log(`Usage: node scripts/check-rainbow-live-dom.mjs [--url URL] [--out DIR] [--expect-glb] [--expect-materials] [--full-page]`);
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
  const overlaps = (a, b) => Boolean(a && b && a.width > 0 && b.width > 0 && a.x < b.x + b.width && a.x + a.width > b.x && a.y < b.y + b.height && a.y + a.height > b.y);
  const q = (s) => document.querySelector(s);
  const qa = (s) => Array.from(document.querySelectorAll(s));
  const bodyText = document.body ? document.body.innerText || '' : '';
  const nlp3d = q('.nlp3d');
  const stage = q('.nlp3d-stage-wrap, .nlp3d-stage, .nlp3d-model-shell, .nlp3d-model-viewer, .nlp3d');
  const model = q('model-viewer');
  const featured = q('.wp-block-post-featured-image');
  const modelHotspots = qa('.nlp3d-mv-hotspot[data-unit]');
  const facadeHotspots = qa('.nlp3d-hotspot[data-unit], .nlp3d-hotspot-hit[data-unit]');
  const selectedTitle = q('.nlp3d-selected-title');
  const stageCard = q('.nlp3d-stage-card');
  const stageControls = qa('.nlp3d-toolbar button, .nlp3d-mv-hotspot, .nlp3d-hotspot, .nlp3d-hotspot-hit, .nlp3d-stage-card button, .nlp3d-stage-card a, .nlp3d-viewframe button, .nlp3d-lead-form input, .nlp3d-lead-form button').filter(visible).map(rect).filter(Boolean);
  const fixedWidgets = qa('.nlfab, #nlai, #nla-btn, [data-nadlan-floating], a[href^="tel:"], a[href*="wa.me"]').filter((el) => {
    const s = getComputedStyle(el);
    return visible(el) && (s.position === 'fixed' || s.position === 'sticky');
  }).map((el) => {
    const r = rect(el);
    return {
      selector: el.id ? '#'+el.id : (el.className ? '.'+String(el.className).trim().split(/\\s+/).slice(0, 2).join('.') : el.tagName.toLowerCase()),
      text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim().slice(0, 48),
      rect: r,
      overlapsStageControl: stageControls.some((control) => overlaps(r, control)),
    };
  });
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
    modelViewerLoaded: Boolean(nlp3d && nlp3d.classList.contains('has-model-viewer-loaded')),
    modelViewerError: Boolean(nlp3d && nlp3d.classList.contains('has-model-viewer-error')),
    modelHotspots: modelHotspots.length,
    visibleModelHotspots: modelHotspots.filter(visible).length,
    facadeHotspots: facadeHotspots.length,
    selectedTitle: selectedTitle ? (selectedTitle.innerText || '').trim() : '',
    stageCardHidden: stageCard ? (stageCard.hidden || !visible(stageCard)) : null,
    hasFallbackTower: Boolean(q('.nlp3d-building, .nlp3d-tower, .nlp3d-facade, .nlp3d-floor-stack')),
    hasMapboxCanvas: Boolean(q('.mapboxgl-canvas')),
    hasUnitButtons: qa('.nlp3d button, .nlp3d [role="button"]').length,
    featuredImageRect: rect(featured),
    featuredImageVisible: Boolean(featured && visible(featured)),
    fixedWidgets,
    fixedOverlapsStageControls: fixedWidgets.filter((item) => item.overlapsStageControl),
    rawLeak: rawLeakPatterns.filter((pattern) => bodyText.includes(pattern)),
    smallTapTargets: tapSmall,
    pageErrorsVisible: bodyText.includes('Fatal error') || bodyText.includes('Warning:') || bodyText.includes('Parse error'),
  };
})()`;

const INTERACTION_EXPRESSION = `(async () => {
  const visible = (el) => {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && s.display !== 'none' && s.visibility !== 'hidden' && Number(s.opacity || 0) > 0.01;
  };
  const q = (s) => document.querySelector(s);
  const before = (q('.nlp3d-selected-title')?.innerText || '').trim();
  const activeBefore = q('.nlp3d-mv-hotspot.is-active[data-unit], .nlp3d-hotspot.is-active[data-unit], .nlp3d-hotspot-hit.is-active[data-unit], .nlp3d-unit-card.is-active[data-unit]')?.getAttribute('data-unit') || '';
  const candidates = Array.from(document.querySelectorAll('.nlp3d-mv-hotspot[data-unit], .nlp3d-hotspot[data-unit], .nlp3d-hotspot-hit[data-unit], .nlp3d-unit-card[data-unit]'));
  const target = candidates.find((el) => (el.getAttribute('data-unit') || '') && el.getAttribute('data-unit') !== activeBefore) || candidates[0] || null;
  if (target) {
    target.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  const after = (q('.nlp3d-selected-title')?.innerText || '').trim();
  const stageTitle = (q('.nlp3d-stage-card-title')?.innerText || '').trim();
  const stageCard = q('.nlp3d-stage-card');
  const active = Array.from(document.querySelectorAll('.nlp3d-mv-hotspot.is-active, .nlp3d-hotspot.is-active, .nlp3d-hotspot-hit.is-active, .nlp3d-unit-card.is-active')).length;
  const targetUnit = target ? (target.getAttribute('data-unit') || '') : '';
  const clickedIsActive = Boolean(targetUnit && document.querySelector('.nlp3d-mv-hotspot.is-active[data-unit="'+CSS.escape(targetUnit)+'"], .nlp3d-hotspot.is-active[data-unit="'+CSS.escape(targetUnit)+'"], .nlp3d-hotspot-hit.is-active[data-unit="'+CSS.escape(targetUnit)+'"], .nlp3d-unit-card.is-active[data-unit="'+CSS.escape(targetUnit)+'"]'));
  const targetClass = target ? (typeof target.className === 'string' ? target.className : (target.getAttribute('class') || target.tagName.toLowerCase())) : '';
  const clickTool = async (action) => {
    const button = q('[data-action="'+action+'"]');
    if (!button || !visible(button)) {
      return {
        action,
        clicked: false,
        headline: '',
        cardCount: 0,
        cardTexts: [],
      };
    }
    button.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
    await new Promise((resolve) => setTimeout(resolve, 350));
    const cards = Array.from(document.querySelectorAll('.nlp3d-tool-panel .nlp3d-material-card')).filter(visible);
    return {
      action,
      clicked: true,
      headline: (q('.nlp3d-tool-panel strong')?.innerText || '').trim(),
      cardCount: cards.length,
      cardTexts: cards.slice(0, 6).map((card) => (card.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 90)),
    };
  };
  const toolChecks = {
    drawing: await clickTool('unit-drawing'),
    surroundings: await clickTool('unit-surroundings'),
    media: await clickTool('unit-media'),
  };
  return {
    attempted: Boolean(target),
    targetSelector: targetClass.trim().slice(0, 80),
    targetUnit,
    beforeTitle: before,
    afterTitle: after,
    stageTitle,
    stageCardVisible: Boolean(stageCard && visible(stageCard) && !stageCard.hidden),
    activeCount: active,
    clickedIsActive,
    toolChecks,
    changed: Boolean(target && after && !/^בחרו דירה/.test(after) && (after !== before || clickedIsActive)),
  };
})()`;

function evaluateChecks(metrics, expectGlb, expectMaterials, interaction) {
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
    add(metrics.modelViewerError ? 'FAIL' : 'PASS', 'model-viewer did not error', metrics.modelViewerError ? 'has-model-viewer-error present' : 'no error class');
    add(metrics.modelHotspots > 0 ? 'PASS' : 'FAIL', 'model-viewer hotspots present', `${metrics.modelHotspots}`);
  } else {
    add(metrics.hasModelViewer ? 'PASS' : 'WARN', 'model-viewer visible', metrics.hasModelViewer ? JSON.stringify(metrics.modelViewerRect) : 'not wired yet');
  }
  add(metrics.hasFallbackTower || metrics.hasModelViewer ? 'PASS' : 'FAIL', 'model or fallback visible', `fallback=${metrics.hasFallbackTower}, model=${metrics.hasModelViewer}`);
  add(metrics.featuredImageVisible ? 'WARN' : 'PASS', 'static featured image suppressed', metrics.featuredImageVisible ? JSON.stringify(metrics.featuredImageRect) : 'not visible');
  add(metrics.smallTapTargets.length === 0 ? 'PASS' : 'WARN', '44px tap targets in showroom', metrics.smallTapTargets.length ? JSON.stringify(metrics.smallTapTargets.slice(0, 5)) : 'all visible targets >=44px');
  const interactionStatus = interaction && interaction.changed && interaction.stageCardVisible && interaction.activeCount > 0;
  add(interactionStatus ? 'PASS' : (expectGlb ? 'FAIL' : 'WARN'), 'unit selection updates UI', interaction ? JSON.stringify(interaction) : 'interaction not run');
  if (expectMaterials) {
    const tools = interaction && interaction.toolChecks ? interaction.toolChecks : {};
    const drawing = tools.drawing || {};
    const surroundings = tools.surroundings || {};
    const media = tools.media || {};
    add(drawing.clicked && drawing.cardCount >= 2 ? 'PASS' : 'FAIL', 'drawing materials render after click', JSON.stringify(drawing));
    add(surroundings.clicked && surroundings.cardCount >= 4 ? 'PASS' : 'FAIL', 'surroundings materials render after click', JSON.stringify(surroundings));
    add(media.clicked ? 'PASS' : 'FAIL', 'media panel is reachable', JSON.stringify(media));
  }
  add(metrics.fixedOverlapsStageControls.length === 0 ? 'PASS' : (expectGlb ? 'FAIL' : 'WARN'), 'fixed contact widgets clear showroom controls', metrics.fixedOverlapsStageControls.length ? JSON.stringify(metrics.fixedOverlapsStageControls.slice(0, 5)) : 'no overlap with visible controls');
  return checks;
}

async function runViewport(browserPort, url, outDir, viewport, expectGlb, expectMaterials, fullPage) {
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
    expression: INTERACTION_EXPRESSION,
    returnByValue: true,
    awaitPromise: true,
  });
  const interaction = evalResult.result.value;
  const metricsResult = await cdp.send('Runtime.evaluate', {
    expression: METRICS_EXPRESSION,
    returnByValue: true,
    awaitPromise: true,
  });
  const metrics = metricsResult.result.value;
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
    interaction,
    checks: evaluateChecks(metrics, expectGlb, expectMaterials, interaction),
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
      results.push(await runViewport(port, args.url, args.out, viewport, args.expectGlb, args.expectMaterials, args.fullPage));
    }
    const reportPath = path.join(args.out, 'rainbow-live-dom-report.json');
    await writeFile(reportPath, `${JSON.stringify({ url: args.url, expectGlb: args.expectGlb, expectMaterials: args.expectMaterials, results }, null, 2)}\n`, 'utf8');
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
