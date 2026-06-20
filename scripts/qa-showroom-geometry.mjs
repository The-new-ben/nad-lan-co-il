import fs from 'node:fs';
import path from 'node:path';
import { chromium, devices } from '@playwright/test';

const DEFAULT_SITE = 'https://nad-lan.co.il';
const DEFAULT_SLUG = 'dimri-yama-sde-dov';
const DEFAULT_OUT = 'docs/qa/screenshots/showroom-geometry';

const VIEWPORTS = [
  { name: 'desktop-1440', width: 1440, height: 1000, deviceScaleFactor: 1, isMobile: false },
  { name: 'tablet-768', width: 768, height: 1000, deviceScaleFactor: 1, isMobile: false },
  { name: 'mobile-390', width: 390, height: 900, deviceScaleFactor: 2, isMobile: true },
  {
    name: 'edge-mobile-390',
    width: 390,
    height: 900,
    deviceScaleFactor: 2,
    isMobile: true,
    userAgent: devices['Pixel 7'].userAgent.replace('Chrome/', 'EdgA/'),
  },
];

function parseArgs(argv) {
  const args = { site: DEFAULT_SITE, slug: DEFAULT_SLUG, outDir: DEFAULT_OUT, strict: false, injectCss: '' };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--site') args.site = argv[++i] || args.site;
    else if (a === '--slug') args.slug = argv[++i] || args.slug;
    else if (a === '--out') args.outDir = argv[++i] || args.outDir;
    else if (a === '--inject-css') args.injectCss = argv[++i] || args.injectCss;
    else if (a === '--strict') args.strict = true;
    else if (a === '--help' || a === '-h') {
      console.log(`Usage:
  node scripts/qa-showroom-geometry.mjs --slug dimri-yama-sde-dov --strict

Captures viewport screenshots and a JSON geometry report for core showroom surfaces.
Use --inject-css path/to/file.css to preview an unreleased containment layer on the live DOM.`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  args.site = args.site.replace(/\/+$/, '');
  if (args.injectCss) args.injectCss = path.resolve(process.cwd(), args.injectCss);
  return args;
}

function overlapArea(a, b) {
  if (!a || !b) return 0;
  const left = Math.max(a.x, b.x);
  const right = Math.min(a.right, b.right);
  const top = Math.max(a.y, b.y);
  const bottom = Math.min(a.bottom, b.bottom);
  return Math.max(0, right - left) * Math.max(0, bottom - top);
}

async function collectGeometry(page) {
  return page.evaluate(() => {
    const visible = (el) => {
      if (!el) return false;
      const st = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return st.display !== 'none' && st.visibility !== 'hidden' && Number(st.opacity || 1) > 0.01 && r.width > 0 && r.height > 0;
    };
    const rect = (el) => {
      if (!el || !visible(el)) return null;
      const r = el.getBoundingClientRect();
      return {
        x: Math.round(r.x * 10) / 10,
        y: Math.round(r.y * 10) / 10,
        width: Math.round(r.width * 10) / 10,
        height: Math.round(r.height * 10) / 10,
        right: Math.round(r.right * 10) / 10,
        bottom: Math.round(r.bottom * 10) / 10,
      };
    };
    const rects = (selector, limit = 30) => Array.from(document.querySelectorAll(selector)).filter(visible).slice(0, limit).map((el, index) => ({
      index,
      selector,
      text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90),
      rect: rect(el),
      className: typeof el.className === 'string' ? el.className : '',
      id: el.id || '',
    }));
    const tapTargets = rects('.nlp3d-cell,.nlp3d-stage-pick,.nlp3d-fp-close,.nlp3d-stage-card button,.nlp3d-lead-form button,.nlp3d-owner-form button,.nlaction-rail button,.nlp3d-tool,.nlp3d-view-toggle', 80);
    return {
      title: document.title,
      url: location.href,
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scroll: {
        width: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        overflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      },
      root: rect(document.querySelector('.nlp3d-premium,.nlp3d')),
      stage: rect(document.querySelector('.nlp3d-stage-wrap')),
      model: rect(document.querySelector('.nlp3d-model-viewer,model-viewer')),
      facade: rect(document.querySelector('.nlp3d-facade-plane')),
      facadeImage: rect(document.querySelector('.nlp3d-fp-image')),
      missing: rect(document.querySelector('.nlp3d-facade-missing')),
      card: rect(document.querySelector('.nlp3d-stage-card:not([hidden])')),
      leadForm: rect(document.querySelector('.nlp3d-lead-form')),
      ownerForm: rect(document.querySelector('.nlp3d-owner-form')),
      floatingRail: rect(document.querySelector('.nlaction-rail,#nlrx-action-rail,.nlrx-action-rail,.nl-floating-actions,.nlai-widget,#nlai')),
      closeButtons: rects('.nlp3d-fp-close,.nlp3d-stage-card button,[data-nlps-close]', 20),
      cells: rects('.nlp3d-cell,.nlp3d-stage-pick', 80),
      media: rects('.nlp3d img,.nlp3d-premium img,.nlp3d video,.nlp3d model-viewer,.nlp3d-fp-image,.nlp3d-model-viewer', 80),
      visibleFacadeSurfaces: rects('.nlp3d-facade-plane,.nlp3d-facade,.nlp3d-facade-missing', 10),
      tapTargets,
      minTap: tapTargets.reduce((min, item) => Math.min(min, item.rect?.width || Infinity, item.rect?.height || Infinity), tapTargets.length ? Infinity : 0),
    };
  });
}

function analyzeGeometry(g) {
  const failures = [];
  const warnings = [];
  const viewportRect = { x: 0, y: 0, right: g.viewport.width, bottom: g.viewport.height };

  if (g.scroll.overflowX > 2) failures.push(`document horizontal overflow ${g.scroll.overflowX}px`);
  for (const [name, r] of Object.entries({ root: g.root, stage: g.stage, model: g.model, facade: g.facade, card: g.card, leadForm: g.leadForm })) {
    if (!r) continue;
    if (r.x < -2 || r.right > g.viewport.width + 2) failures.push(`${name} outside viewport: ${JSON.stringify(r)}`);
  }
  if (g.facade && g.stage) {
    if (g.facade.x < g.stage.x - 2 || g.facade.right > g.stage.right + 2 || g.facade.y < g.stage.y - 2 || g.facade.bottom > g.stage.bottom + 2) {
      failures.push(`facade outside stage: facade=${JSON.stringify(g.facade)} stage=${JSON.stringify(g.stage)}`);
    }
  }
  if (g.model && g.stage) {
    if (g.model.x < g.stage.x - 2 || g.model.right > g.stage.right + 2 || g.model.y < g.stage.y - 2 || g.model.bottom > g.stage.bottom + 2) {
      warnings.push(`model outside stage: model=${JSON.stringify(g.model)} stage=${JSON.stringify(g.stage)}`);
    }
  }
  if (g.card && g.facade) {
    const area = overlapArea(g.card, g.facade);
    const facadeArea = Math.max(1, g.facade.width * g.facade.height);
    const ratio = area / facadeArea;
    if (ratio > 0.18) failures.push(`selected card covers facade by ${(ratio * 100).toFixed(1)}%`);
    else if (ratio > 0.08) warnings.push(`selected card overlaps facade by ${(ratio * 100).toFixed(1)}%`);
  }
  for (const cell of g.cells) {
    if (!cell.rect) continue;
    if (overlapArea(cell.rect, viewportRect) < cell.rect.width * cell.rect.height * 0.9) {
      failures.push(`cell outside viewport: ${cell.text || cell.className} ${JSON.stringify(cell.rect)}`);
    }
    if (g.card && overlapArea(cell.rect, g.card) > cell.rect.width * cell.rect.height * 0.55) {
      warnings.push(`selected card covers cell: ${cell.text || cell.className}`);
    }
  }
  for (const item of g.media || []) {
    if (!item.rect) continue;
    if (item.rect.x < -2 || item.rect.right > g.viewport.width + 2) {
      failures.push(`media outside viewport: ${item.selector} ${JSON.stringify(item.rect)}`);
    }
    if (g.root && (item.rect.x < g.root.x - 2 || item.rect.right > g.root.right + 2)) {
      failures.push(`media outside showroom root: ${item.selector} ${JSON.stringify(item.rect)} root=${JSON.stringify(g.root)}`);
    }
  }
  if ((g.visibleFacadeSurfaces || []).length > 1) {
    failures.push(`multiple visible facade surfaces: ${g.visibleFacadeSurfaces.length}`);
  }
  if (g.floatingRail) {
    for (const [name, r] of Object.entries({ leadForm: g.leadForm, ownerForm: g.ownerForm, card: g.card })) {
      if (r && overlapArea(g.floatingRail, r) > 1200) warnings.push(`floating rail overlaps ${name}`);
    }
  }
  if (Number.isFinite(g.minTap) && g.minTap > 0 && g.minTap < 44) failures.push(`tap target below 44px: ${Math.round(g.minTap * 10) / 10}px`);
  return { failures, warnings };
}

async function runViewport(browser, args, viewport, outDir) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: viewport.deviceScaleFactor,
    isMobile: viewport.isMobile,
    userAgent: viewport.userAgent,
  });
  const page = await context.newPage();
  const pageErrors = [];
  page.on('pageerror', (err) => pageErrors.push(err.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error') pageErrors.push(msg.text());
  });
  const url = `${args.site}/projects/${args.slug}/?cb=geometry-${Date.now()}-${viewport.name}`;
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  if (args.injectCss) {
    await page.addStyleTag({ content: fs.readFileSync(args.injectCss, 'utf8') });
  }
  await page.locator('.nlp3d-premium,.nlp3d').scrollIntoViewIfNeeded({ timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(900);
  const firstCell = page.locator('.nlp3d-cell,.nlp3d-stage-pick').first();
  if (await firstCell.count()) {
    await firstCell.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(500);
  }
  const geometry = await collectGeometry(page);
  const analysis = analyzeGeometry(geometry);
  if (pageErrors.length) analysis.failures.push(`page errors: ${pageErrors.slice(0, 3).join(' | ')}`);
  const screenshot = path.join(outDir, `${viewport.name}.png`);
  await page.screenshot({ path: screenshot, fullPage: false });
  await context.close();
  return { name: viewport.name, screenshot, geometry, ...analysis };
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = path.resolve(process.cwd(), args.outDir);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    const viewports = [];
    for (const viewport of VIEWPORTS) {
      viewports.push(await runViewport(browser, args, viewport, outDir));
    }
    const failed = viewports.filter((v) => v.failures.length);
    const report = {
      site: args.site,
      slug: args.slug,
      generated_at: new Date().toISOString(),
      out_dir: args.outDir,
      injected_css: args.injectCss ? path.relative(process.cwd(), args.injectCss) : null,
      summary: { passed: viewports.length - failed.length, failed: failed.length },
      viewports,
    };
    fs.writeFileSync(path.join(outDir, 'geometry-report.json'), `${JSON.stringify(report, null, 2)}\n`);
    console.log(JSON.stringify(report, null, 2));
    if (args.strict && failed.length) process.exitCode = 1;
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
