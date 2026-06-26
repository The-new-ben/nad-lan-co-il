#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = process.cwd();
const PREVIEW = 'docs/previews/nadlan-home-showroom-preview.html';
const OUT = 'docs/qa/screenshots/home-showroom-preview-2026-06-27';
const MIME = {
	'.html': 'text/html; charset=utf-8',
	'.css': 'text/css; charset=utf-8',
	'.js': 'text/javascript; charset=utf-8',
	'.json': 'application/json; charset=utf-8',
	'.png': 'image/png',
	'.jpg': 'image/jpeg',
	'.jpeg': 'image/jpeg',
	'.svg': 'image/svg+xml',
	'.glb': 'model/gltf-binary'
};

function arg(name, fallback) {
	const idx = process.argv.indexOf(name);
	return idx === -1 ? fallback : process.argv[idx + 1];
}

async function startServer() {
	const server = createServer(async (req, res) => {
		try {
			const url = new URL(req.url || '/', 'http://127.0.0.1');
			const clean = decodeURIComponent(url.pathname.replace(/^\/+/, '')) || PREVIEW;
			const file = path.resolve(ROOT, clean);
			if (!file.startsWith(ROOT) || !existsSync(file)) {
				res.writeHead(404);
				res.end('not found');
				return;
			}
			const ext = path.extname(file).toLowerCase();
			res.writeHead(200, { 'content-type': MIME[ext] || 'application/octet-stream' });
			res.end(await readFile(file));
		} catch (error) {
			res.writeHead(500);
			res.end(String(error && error.message || error));
		}
	});
	await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
	return { server, port: server.address().port };
}

function viewportList() {
	return [
		{ name: 'desktop-1440', width: 1440, height: 1200 },
		{ name: 'tablet-768', width: 768, height: 1100 },
		{ name: 'mobile-390', width: 390, height: 900, isMobile: true, hasTouch: true },
		{ name: 'edge-mobile-390', width: 390, height: 900, isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36 EdgA/124.0' }
	];
}

async function measure(page) {
	return page.evaluate(() => {
		const visibleText = document.body.innerText || '';
		const rect = (sel) => {
			const el = document.querySelector(sel);
			if (!el) return null;
			const r = el.getBoundingClientRect();
			return { x: r.x, y: r.y, width: r.width, height: r.height, right: r.right, bottom: r.bottom };
		};
		const publicTargetSelector = [
			'.nle-project-card',
			'.nle-facade-cell',
			'.nle-tabs button',
			'.nle-contact button',
			'.nlh-home-button',
			'.nlh-home-inline-search button',
			'.nlh-home-inline-search input',
			'.nlh-home-inline-search select',
			'.nlh-home-languages a',
			'.nlh-home-languages span',
			'.nle-nav a',
			'.nle-langs span'
		].join(',');
		const targetRows = [...document.querySelectorAll(publicTargetSelector)].map((el) => {
			const r = el.getBoundingClientRect();
			return {
				tag: el.tagName,
				className: String(el.className || ''),
				text: (el.textContent || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 48),
				width: r.width,
				height: r.height,
				min: Math.min(r.width, r.height)
			};
		}).filter(Boolean);
		const tapSizes = targetRows.map((row) => row.min);
		const catalog = rect('#projects');
		const showroom = rect('#showroom');
		return {
			title: document.title,
			h1s: [...document.querySelectorAll('h1')].map((h) => h.textContent.trim()),
			languageEntries: document.querySelectorAll('.nlh-home-languages a, .nlh-home-languages span, .nle-langs span').length,
			languageTargets: ['english', 'french', 'russian', 'arabic'].filter((id) => document.getElementById(id)).length,
			buyerPathCards: document.querySelectorAll('.nlh-home-paths article').length,
			projectCards: document.querySelectorAll('[data-nle-project]').length,
			modelViewerCount: document.querySelectorAll('model-viewer').length,
			modelViewerDefined: !!customElements.get('model-viewer'),
			facadeCells: document.querySelectorAll('.nle-facade-cell').length,
			activeCells: document.querySelectorAll('.nle-facade-cell.is-active, .nle-hotspot.is-active').length,
			overflow: Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth),
			minTap: tapSizes.length ? Math.min(...tapSizes) : 0,
			smallTargets: targetRows.filter((row) => row.min < 34).slice(0, 10),
			hasHebrew: /[\u0590-\u05ff]/.test(visibleText),
			hasForeignBuyerSignal: /(English|Français|Русский|العربية|משקיעים מחו״ל)/.test(visibleText),
			hasBuyerWords: /(דירה|דירות|פרויקט|פרויקטים|מחיר|אומדן|זמינות)/.test(visibleText),
			hasMojibake: /Ã|�|×[^\s]*×/.test(visibleText),
			hasInternalWords: /(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה)/i.test(visibleText),
			catalog,
			showroom
		};
	});
}

function failuresFor(viewName, before, after, errors, viewportHeight) {
	const failures = [];
	if (errors.length) failures.push(`${viewName}: console/page errors: ${errors.join(' | ')}`);
	if (before.h1s.length !== 1) failures.push(`${viewName}: expected one H1, got ${before.h1s.length}`);
	if (before.languageEntries < 5) failures.push(`${viewName}: expected at least 5 language entries`);
	if (before.languageTargets < 4) failures.push(`${viewName}: expected four language target cards`);
	if (before.buyerPathCards < 4) failures.push(`${viewName}: expected four buyer path cards`);
	if (before.projectCards < 3) failures.push(`${viewName}: expected at least 3 project cards`);
	if (before.modelViewerCount !== 1) failures.push(`${viewName}: expected one model-viewer`);
	if (!before.modelViewerDefined) failures.push(`${viewName}: model-viewer custom element not defined`);
	if (before.facadeCells < 3) failures.push(`${viewName}: expected facade cells`);
	if (before.overflow > 1 || after.overflow > 1) failures.push(`${viewName}: horizontal overflow before=${before.overflow} after=${after.overflow}`);
	if (before.minTap < 34 || after.minTap < 34) failures.push(`${viewName}: tap targets too small before=${before.minTap} after=${after.minTap}`);
	if (!before.hasHebrew) failures.push(`${viewName}: Hebrew text missing`);
	if (!before.hasForeignBuyerSignal) failures.push(`${viewName}: foreign-buyer language signal missing`);
	if (!before.hasBuyerWords) failures.push(`${viewName}: buyer/project words missing`);
	if (before.hasMojibake || after.hasMojibake) failures.push(`${viewName}: mojibake detected`);
	if (before.hasInternalWords || after.hasInternalWords) failures.push(`${viewName}: public internal wording detected`);
	if (!before.catalog || before.catalog.y > viewportHeight) failures.push(`${viewName}: project section is not above the first viewport`);
	if (viewName === 'desktop-1440' && (!before.showroom || before.showroom.y > viewportHeight * 1.55)) failures.push(`${viewName}: showroom starts too low for homepage flow`);
	return failures;
}

async function run() {
	const outDir = path.resolve(ROOT, arg('--out', OUT));
	const preview = arg('--preview', PREVIEW);
	mkdirSync(outDir, { recursive: true });
	const { server, port } = await startServer();
	const browser = await chromium.launch({ channel: 'chrome', headless: !process.argv.includes('--headed') });
	const report = { ok: false, preview, out_dir: outDir, viewports: [] };
	const allFailures = [];
	try {
		for (const vp of viewportList()) {
			const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch, userAgent: vp.userAgent });
			const page = await context.newPage();
			const errors = [];
			page.on('pageerror', (err) => errors.push(err.message));
			page.on('console', (msg) => {
				if (msg.type() === 'error') errors.push(msg.text());
			});
			await page.goto(`http://127.0.0.1:${port}/${preview}`, { waitUntil: 'networkidle' });
			await page.waitForSelector('[data-nle-project]', { timeout: 20000 });
			await page.screenshot({ path: path.join(outDir, `${vp.name}-home.png`), fullPage: true });
			const before = await measure(page);
			const projectCards = page.locator('[data-nle-project]');
			if (await projectCards.count() > 1) await projectCards.nth(1).click();
			await page.waitForTimeout(500);
			const unitButtons = page.locator('.nle-facade-cell');
			if (await unitButtons.count() > 1) await unitButtons.nth(1).click();
			await page.waitForTimeout(500);
			await page.screenshot({ path: path.join(outDir, `${vp.name}-selected.png`), fullPage: true });
			const after = await measure(page);
			const failures = failuresFor(vp.name, before, after, errors, vp.height);
			allFailures.push(...failures);
			report.viewports.push({ name: vp.name, before, after, failures });
			await context.close();
		}
		report.ok = allFailures.length === 0;
		report.failures = allFailures;
		writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2), 'utf8');
		console.log(JSON.stringify({ ok: report.ok, failures: allFailures, out_dir: outDir }, null, 2));
		if (process.argv.includes('--strict') && allFailures.length) process.exitCode = 1;
	} finally {
		await browser.close();
		server.close();
	}
}

run().catch((error) => {
	console.error(error);
	process.exit(1);
});
