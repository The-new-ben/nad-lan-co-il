import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const playwrightPackage = require.resolve('playwright', {
  paths: [process.cwd(), process.env.PLAYWRIGHT_NODE_PATH].filter(Boolean),
});
const playwright = await import(pathToFileURL(playwrightPackage).href);
const chromium = playwright.chromium || (playwright.default && playwright.default.chromium);
if (!chromium) {
  throw new Error('Unable to load Playwright chromium launcher');
}

const outDir = process.argv[2] || 'docs/qa/screenshots/showroom-surface-mesh-pick-live-16916-2026-06-24';
const url = process.argv[3] || 'https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=surface_mesh_pick_16916';

const candidates = [
  { name: 'tower-upper-center', x: 0.50, y: 0.34 },
  { name: 'tower-mid-center', x: 0.52, y: 0.52 },
  { name: 'tower-mid-right', x: 0.62, y: 0.50 },
  { name: 'tower-mid-left', x: 0.39, y: 0.50 },
  { name: 'podium-center', x: 0.48, y: 0.70 },
  { name: 'podium-right', x: 0.61, y: 0.67 },
  { name: 'podium-left', x: 0.31, y: 0.67 },
];

function serializeError(error) {
  if (!error) {
    return null;
  }
  return {
    name: error.name || 'Error',
    message: error.message || String(error),
  };
}

async function inspect(page) {
  return page.evaluate(() => {
    const root = document.querySelector('.nlp3d');
    const mv = document.querySelector('model-viewer');
    const card = document.querySelector('.nlp3d-stage-card');
    return {
      viewport: { width: window.innerWidth, height: window.innerHeight },
      scrollWidth: document.documentElement.scrollWidth,
      bodyScrollWidth: document.body ? document.body.scrollWidth : null,
      activeUnit: root ? root.getAttribute('data-active-unit') : null,
      activePick: document.querySelector('.nlp3d-stage-pick.is-active, .nlp3d-stage-pick[aria-pressed="true"]')?.getAttribute('data-unit') || null,
      cameraOrbit: mv ? mv.getAttribute('camera-orbit') : null,
      cameraTarget: mv ? mv.getAttribute('camera-target') : null,
      stageCardHidden: card ? card.hidden : null,
      stageCardText: card ? card.innerText.replace(/\s+/g, ' ').trim().slice(0, 500) : '',
      meshPickLog: window.__nadlanMeshPickLog || [],
    };
  });
}

async function scanCandidates(page, beforeActiveUnit) {
  return page.evaluate(({ points, before }) => {
    const parseVector = (raw) => {
      const nums = String(raw || '').replace(/m/g, '').trim().split(/\s+/).map((part) => Number(part));
      if (nums.length < 3 || nums.some((n) => !Number.isFinite(n))) {
        return null;
      }
      return { x: nums[0], y: nums[1], z: nums[2] };
    };
    const serializeVector = (value) => value ? {
      x: Number(value.x),
      y: Number(value.y),
      z: Number(value.z),
    } : null;
    const nearestUnit = (position) => {
      const hotspots = Array.from(document.querySelectorAll('.nlp3d-mv-hotspot'));
      let best = null;
      let bestScore = Infinity;
      hotspots.forEach((el) => {
        if (el.classList.contains('is-sold') || el.classList.contains('nlp3d-status-sold')) {
          return;
        }
        const vector = parseVector(el.getAttribute('data-position'));
        if (!vector) {
          return;
        }
        const dx = vector.x - position.x;
        const dy = Math.abs(vector.y - position.y);
        const dz = vector.z - position.z;
        const horizontal = Math.sqrt(dx * dx + dz * dz);
        const score = (dy * 1.7) + (horizontal * 0.28);
        if (score < bestScore) {
          bestScore = score;
          best = {
            unit: el.getAttribute('data-unit'),
            label: el.innerText.replace(/\s+/g, ' ').trim(),
            score,
            yDelta: dy,
            horizontal,
            vector,
          };
        }
      });
      return best;
    };

    const scene = document.querySelector('.nlp3d-scene');
    const mv = document.querySelector('model-viewer');
    if (!scene || !mv || typeof mv.positionAndNormalFromPoint !== 'function') {
      return { error: 'missing scene or positionAndNormalFromPoint', candidates: [] };
    }
    const sceneRect = scene.getBoundingClientRect();
    const modelRect = mv.getBoundingClientRect();
    const scanned = points.map((point) => {
      const x = sceneRect.left + sceneRect.width * point.x;
      const y = sceneRect.top + sceneRect.height * point.y;
      const top = document.elementFromPoint(x, y);
      let hit = null;
      let hitError = null;
      try {
        hit = mv.positionAndNormalFromPoint(x, y);
      } catch (error) {
        hitError = error.message || String(error);
      }
      const position = hit && hit.position ? serializeVector(hit.position) : null;
      const nearest = position ? nearestUnit(position) : null;
      return {
        ...point,
        screen: { x, y },
        sceneRect: {
          x: sceneRect.x,
          y: sceneRect.y,
          width: sceneRect.width,
          height: sceneRect.height,
        },
        modelRect: {
          x: modelRect.x,
          y: modelRect.y,
          width: modelRect.width,
          height: modelRect.height,
        },
        elementAtPoint: top ? {
          tag: top.tagName,
          className: String(top.className || '').slice(0, 180),
          markerUnit: top.closest && top.closest('.nlp3d-stage-pick') ? top.closest('.nlp3d-stage-pick').getAttribute('data-unit') : null,
          insideModelViewer: !!(top.closest && top.closest('model-viewer')),
        } : null,
        hitError,
        hitPosition: position,
        nearest,
        selectableSurface: !!(
          position &&
          nearest &&
          (!top || !(top.closest && top.closest('.nlp3d-stage-pick'))) &&
          top &&
          top.closest &&
          top.closest('model-viewer')
        ),
      };
    });

    const preferred = scanned
      .filter((item) => item.selectableSurface)
      .sort((a, b) => {
        const aDiff = a.nearest && a.nearest.unit !== before ? 0 : 1;
        const bDiff = b.nearest && b.nearest.unit !== before ? 0 : 1;
        if (aDiff !== bDiff) {
          return aDiff - bDiff;
        }
        return (a.nearest?.score || Infinity) - (b.nearest?.score || Infinity);
      })[0] || null;

    return { beforeActiveUnit: before, candidates: scanned, chosen: preferred };
  }, { points: candidates, before: beforeActiveUnit });
}

async function installMeshPickLogger(page) {
  return page.evaluate(() => {
    const mv = document.querySelector('model-viewer');
    window.__nadlanMeshPickLog = [];
    if (!mv || typeof mv.positionAndNormalFromPoint !== 'function') {
      return { installed: false, reason: 'missing positionAndNormalFromPoint' };
    }
    if (mv.__nadlanQaMeshPickWrapped) {
      return { installed: true, alreadyInstalled: true };
    }
    const original = mv.positionAndNormalFromPoint.bind(mv);
    const serializeVector = (value) => value ? {
      x: Number(value.x),
      y: Number(value.y),
      z: Number(value.z),
    } : null;
    mv.positionAndNormalFromPoint = function wrappedPositionAndNormalFromPoint(x, y) {
      let result = null;
      let error = null;
      try {
        result = original(x, y);
      } catch (err) {
        error = err;
        throw err;
      } finally {
        window.__nadlanMeshPickLog.push({
          x,
          y,
          hit: result && result.position ? {
            position: serializeVector(result.position),
            normal: serializeVector(result.normal),
          } : null,
          error: error ? (error.message || String(error)) : null,
          at: Date.now(),
        });
      }
      return result;
    };
    mv.__nadlanQaMeshPickWrapped = true;
    return { installed: true };
  });
}

async function runViewport(browser, label, width, height) {
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    isMobile: width <= 480,
    hasTouch: width <= 480,
    locale: 'he-IL',
  });
  const page = await context.newPage();
  const result = {
    label,
    viewport: { width, height },
    url: `${url}&viewport=${label}&t=${Date.now()}`,
  };
  try {
    await page.goto(result.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.nlp3d-premium model-viewer', { timeout: 45000 });
    await page.waitForFunction(() => document.querySelector('.nlp3d')?.classList.contains('has-model-viewer-loaded'), null, { timeout: 45000 }).catch(() => null);
    await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
    await page.waitForTimeout(800);
    result.before = await inspect(page);
    result.scan = await scanCandidates(page, result.before.activeUnit);
    result.logger = await installMeshPickLogger(page);
    await page.screenshot({ path: path.join(outDir, `${label}-before-surface-mesh-pick.png`), fullPage: false });

    if (!result.scan.chosen) {
      result.pass = false;
      result.reason = 'No candidate point landed on the model surface without hitting an overlay marker.';
      await page.screenshot({ path: path.join(outDir, `${label}-no-surface-candidate.png`), fullPage: false });
      return result;
    }

    const point = result.scan.chosen.screen;
    if (width <= 480) {
      await page.touchscreen.tap(point.x, point.y);
    } else {
      await page.mouse.click(point.x, point.y);
    }
    await page.waitForTimeout(1400);
    await page.locator('.nlp3d-stage-wrap').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(outDir, `${label}-after-surface-mesh-pick.png`), fullPage: false });
    result.after = await inspect(page);
    result.expectedUnitFromMesh = result.scan.chosen.nearest?.unit || null;
    result.pass = !!(
      result.logger.installed &&
      result.after.meshPickLog &&
      result.after.meshPickLog.length > 0 &&
      result.after.activeUnit &&
      result.after.activeUnit === result.expectedUnitFromMesh &&
      result.after.cameraOrbit &&
      result.after.cameraTarget &&
      result.after.stageCardHidden === false
    );
    if (!result.pass) {
      result.reason = 'Tap did not fully prove mesh-surface selection, active unit, camera orbit, camera target and visible unit card.';
    }
  } catch (error) {
    result.pass = false;
    result.error = serializeError(error);
    await page.screenshot({ path: path.join(outDir, `${label}-error.png`), fullPage: false }).catch(() => null);
  } finally {
    await context.close();
  }
  return result;
}

await fs.mkdir(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const results = {
  createdAt: new Date().toISOString(),
  url,
  desktop: await runViewport(browser, 'desktop-1440', 1440, 1000),
  mobile: await runViewport(browser, 'mobile-390', 390, 900),
};
await browser.close();
results.pass = !!(results.desktop.pass && results.mobile.pass);
await fs.writeFile(path.join(outDir, 'showroom-surface-mesh-pick-report.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
