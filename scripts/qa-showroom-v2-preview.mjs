import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';

const DEFAULT_PREVIEW = 'docs/previews/ashira-showroom-v2-preview.html';
const DEFAULT_OUT = 'docs/qa/screenshots/ashira-v2-preview-factory-gate';

const VIEWPORTS = [
	{ name: 'desktop-1440', width: 1440, height: 1000, isMobile: false, deviceScaleFactor: 1 },
	{ name: 'tablet-768', width: 768, height: 1000, isMobile: false, deviceScaleFactor: 1 },
	{ name: 'mobile-390', width: 390, height: 900, isMobile: true, deviceScaleFactor: 2 },
	{
		name: 'edge-mobile-390',
		width: 390,
		height: 900,
		isMobile: true,
		deviceScaleFactor: 2,
		userAgent:
			'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Mobile Safari/537.36 EdgA/125.0',
	},
];

const ALLOWED_CONSOLE_WARNINGS = [
	/^rAF timed out in updateSource$/,
];

function usage() {
	return `Usage:
  node scripts/qa-showroom-v2-preview.mjs --preview docs/previews/ashira-showroom-v2-preview.html --out docs/qa/screenshots/ashira-v2-preview-factory-gate --strict

Runs a local HTTP preview in Google Chrome via Playwright, captures desktop/tablet/mobile
screenshots, checks the clean v2 showroom contract, and writes report.json. It does not contact
WordPress or change the live site.`;
}

function parseArgs(argv) {
	const args = {
		preview: DEFAULT_PREVIEW,
		out: DEFAULT_OUT,
		strict: false,
		headed: false,
	};
	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === '--preview') args.preview = argv[++i] || args.preview;
		else if (arg === '--out') args.out = argv[++i] || args.out;
		else if (arg === '--strict') args.strict = true;
		else if (arg === '--headed') args.headed = true;
		else if (arg === '--help' || arg === '-h') {
			console.log(usage());
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}
	return args;
}

function contentType(filePath) {
	const ext = path.extname(filePath).toLowerCase();
	if (ext === '.html') return 'text/html; charset=utf-8';
	if (ext === '.css') return 'text/css; charset=utf-8';
	if (ext === '.js' || ext === '.mjs') return 'text/javascript; charset=utf-8';
	if (ext === '.json') return 'application/json; charset=utf-8';
	if (ext === '.svg') return 'image/svg+xml; charset=utf-8';
	if (ext === '.png') return 'image/png';
	if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
	if (ext === '.webp') return 'image/webp';
	if (ext === '.glb') return 'model/gltf-binary';
	if (ext === '.usdz') return 'model/vnd.usdz+zip';
	return 'application/octet-stream';
}

function safePath(root, urlPath) {
	const decoded = decodeURIComponent(urlPath.split('?')[0] || '/').replace(/^\/+/, '');
	const absolute = path.resolve(root, decoded || 'index.html');
	const rootWithSep = root.endsWith(path.sep) ? root : root + path.sep;
	if (absolute !== root && !absolute.startsWith(rootWithSep)) {
		return null;
	}
	return absolute;
}

async function createServer(root) {
	const server = http.createServer(async (req, res) => {
		try {
			const filePath = safePath(root, req.url || '/');
			if (!filePath) {
				res.writeHead(403);
				res.end('Forbidden');
				return;
			}
			const data = await fs.readFile(filePath);
			res.writeHead(200, {
				'content-type': contentType(filePath),
				'cache-control': 'no-store',
				'access-control-allow-origin': '*',
			});
			res.end(data);
		} catch {
			res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
			res.end('Not found');
		}
	});

	await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
	const address = server.address();
	return {
		server,
		origin: `http://127.0.0.1:${address.port}`,
		close: () => new Promise((resolve) => server.close(resolve)),
	};
}

function metricsExpression() {
	return `(() => {
		const round = (value) => Math.round(Number(value || 0) * 10) / 10;
		const rect = (selector) => {
			const el = document.querySelector(selector);
			if (!el) return null;
			const r = el.getBoundingClientRect();
			return { x: round(r.x), y: round(r.y), width: round(r.width), height: round(r.height), right: round(r.right), bottom: round(r.bottom) };
		};
		const intersects = (a, b) => !!(a && b && a.right > b.x && a.x < b.right && a.bottom > b.y && a.y < b.bottom);
		const tapRects = [...document.querySelectorAll('[data-nlv2-unit]')].map((el) => {
			const r = el.getBoundingClientRect();
			return { width: round(r.width), height: round(r.height) };
		});
		const text = (document.title || '') + '\\n' + (document.body ? document.body.innerText : '');
		const root = document.querySelector('[data-nlv2-showroom]');
		const model = document.querySelector('model-viewer');
		const facade = rect('.nlv2-facade');
		const card = rect('[data-nlv2-card]');
		return {
			title: document.title,
			dir: document.documentElement.dir,
			lang: document.documentElement.lang,
			hasRoot: !!root,
			oldRootCount: document.querySelectorAll('[data-nlps-showroom], .nlps, .nlp3d').length,
			h1Count: document.querySelectorAll('h1').length,
			h2Count: document.querySelectorAll('h2').length,
			scroll: {
				width: document.documentElement.scrollWidth,
				client: document.documentElement.clientWidth,
				overflow: Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth),
			},
			rects: {
				root: rect('.nlv2-showroom'),
				hero: rect('.nlv2-hero'),
				stage: rect('.nlv2-stage'),
				model: rect('.nlv2-model'),
				picker: rect('.nlv2-picker'),
				facade,
				card,
				contact: rect('.nlv2-contact'),
			},
			modelViewer: {
				count: document.querySelectorAll('model-viewer').length,
				defined: !!customElements.get('model-viewer'),
				src: model ? model.getAttribute('src') : '',
				poster: model ? model.getAttribute('poster') : '',
				cameraControls: model ? model.hasAttribute('camera-controls') : false,
			},
			units: {
				count: document.querySelectorAll('[data-nlv2-unit]').length,
				active: document.querySelectorAll('[data-nlv2-unit].is-active').length,
				featured: document.querySelectorAll('[data-nlv2-unit].is-featured').length,
				minTapWidth: tapRects.length ? Math.min(...tapRects.map((r) => r.width)) : 0,
				minTapHeight: tapRects.length ? Math.min(...tapRects.map((r) => r.height)) : 0,
			},
			selected: {
				cardHidden: document.querySelector('[data-nlv2-card]')?.hidden || false,
				unitInput: document.querySelector('[data-nlv2-selected-unit]')?.value || '',
				title: document.querySelector('[data-nlv2-title]')?.textContent?.trim() || '',
			},
			overlap: {
				cardOverFacade: intersects(card, facade),
			},
			copy: {
				hasHebrew: /[\\u0590-\\u05ff]/.test(text),
				hasMojibake: /[\\u00c3\\u00c2\\ufffd]|\\u00d7[\\u0080-\\u00ff]|\\u00c2\\u00b7|\\u00c3\\u0097/.test(text),
				hasInternalWords: /SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|פאנל|מנוע|תבנית|לידים|מקום שמור|פרויקטים לבדיקה|מוניטיז|אסטרטג|Codex|Claude|fallback|placeholder|mock/i.test(text),
			},
		};
	})()`;
}

function evaluateChecks(view) {
	const m = view.metrics;
	const failures = [];

	if (!m.hasRoot) failures.push('missing data-nlv2-showroom root');
	if (m.oldRootCount > 0) failures.push(`old showroom selectors leaked into v2: ${m.oldRootCount}`);
	if (m.h1Count !== 1) failures.push(`expected exactly one H1, got ${m.h1Count}`);
	if (m.scroll.overflow > 1) failures.push(`horizontal overflow: ${m.scroll.overflow}px`);
	if (m.modelViewer.count !== 1) failures.push(`expected one model-viewer, got ${m.modelViewer.count}`);
	if (!m.modelViewer.defined) failures.push('model-viewer custom element was not registered');
	if (!m.modelViewer.cameraControls) failures.push('model-viewer is missing camera-controls');
	if (m.units.count < 3) failures.push(`expected at least 3 apartment cells, got ${m.units.count}`);
	if (m.units.active !== 1) failures.push(`expected one active apartment cell, got ${m.units.active}`);
	if (m.units.minTapWidth < 44 || m.units.minTapHeight < 44) {
		failures.push(`tap target below 44px: ${m.units.minTapWidth}x${m.units.minTapHeight}`);
	}
	if (m.overlap.cardOverFacade) failures.push('selected-apartment card overlaps the facade picker');
	if (!m.copy.hasHebrew) failures.push('visible page text has no Hebrew');
	if (m.copy.hasMojibake) failures.push('visible page text contains mojibake');
	if (m.copy.hasInternalWords) failures.push('visible public copy leaks internal wording');

	return failures;
}

async function main() {
	const args = parseArgs(process.argv);
	const cwd = process.cwd();
	const previewPath = path.resolve(cwd, args.preview);
	await fs.access(previewPath);
	await fs.mkdir(args.out, { recursive: true });

	const { chromium } = await import('playwright');
	const server = await createServer(cwd);
	const previewUrl = `${server.origin}/${path.relative(cwd, previewPath).replace(/\\/g, '/')}`;
	const report = {
		generated_at: new Date().toISOString(),
		preview: args.preview,
		url: previewUrl,
		out_dir: args.out,
		strict: args.strict,
		viewports: [],
		failures: [],
	};

	let browser;
	try {
		browser = await chromium.launch({
			channel: 'chrome',
			headless: !args.headed,
		});

		for (const vp of VIEWPORTS) {
			const context = await browser.newContext({
				viewport: { width: vp.width, height: vp.height },
				deviceScaleFactor: vp.deviceScaleFactor,
				isMobile: vp.isMobile,
				hasTouch: vp.isMobile,
				userAgent: vp.userAgent,
				locale: 'he-IL',
			});
			const page = await context.newPage();
			const consoleErrors = [];
			const allowedConsoleWarnings = [];
			const pageErrors = [];
			page.on('console', (msg) => {
				if (['error', 'warning'].includes(msg.type())) {
					const entry = { type: msg.type(), text: msg.text() };
					if (msg.type() === 'warning' && ALLOWED_CONSOLE_WARNINGS.some((re) => re.test(entry.text))) {
						allowedConsoleWarnings.push(entry);
					} else {
						consoleErrors.push(entry);
					}
				}
			});
			page.on('pageerror', (error) => pageErrors.push(error.message));

			await page.goto(previewUrl, { waitUntil: 'networkidle', timeout: 45000 });
			await page.waitForTimeout(1200);
			await page.waitForFunction(() => !!customElements.get('model-viewer'), null, { timeout: 15000 }).catch(() => {});

			const initialPath = path.resolve(args.out, `${vp.name}-initial.png`);
			await page.screenshot({ path: initialPath, fullPage: true });

			const secondUnit = page.locator('[data-nlv2-unit]').nth(1);
			if (await secondUnit.count()) {
				await secondUnit.click({ timeout: 10000 });
				await page.waitForTimeout(350);
			}
			const selectedPath = path.resolve(args.out, `${vp.name}-selected.png`);
			await page.screenshot({ path: selectedPath, fullPage: true });

			const metrics = await page.evaluate(metricsExpression());
			const viewportFailures = evaluateChecks({ metrics });
			if (consoleErrors.length) viewportFailures.push(`console warnings/errors: ${consoleErrors.length}`);
			if (pageErrors.length) viewportFailures.push(`page errors: ${pageErrors.length}`);

			report.viewports.push({
				name: vp.name,
				viewport: vp,
				screenshots: {
					initial: initialPath,
					selected: selectedPath,
				},
				metrics,
				consoleErrors,
				allowedConsoleWarnings,
				pageErrors,
				failures: viewportFailures,
			});
			report.failures.push(...viewportFailures.map((failure) => `${vp.name}: ${failure}`));
			await context.close();
		}
	} finally {
		if (browser) await browser.close();
		await server.close();
	}

	const reportPath = path.resolve(args.out, 'report.json');
	await fs.writeFile(reportPath, JSON.stringify(report, null, 2) + '\n', 'utf8');
	console.log(JSON.stringify({
		ok: report.failures.length === 0,
		report: reportPath,
		out_dir: path.resolve(args.out),
		viewports: report.viewports.length,
		failures: report.failures,
	}, null, 2));

	if (args.strict && report.failures.length) {
		process.exit(1);
	}
}

main().catch((error) => {
	console.error(error);
	process.exit(1);
});
