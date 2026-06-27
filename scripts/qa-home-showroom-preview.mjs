#!/usr/bin/env node
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = process.cwd();
const PREVIEW = 'docs/previews/nadlan-home-showroom-preview.html';
const OUT = 'docs/qa/screenshots/home-showroom-preview-2026-06-27';
const ASHIRA_MANIFEST = 'docs/plans/2026-06-27-ashira-publication-manifest.json';
const ashiraManifest = JSON.parse(readFileSync(path.resolve(ROOT, ASHIRA_MANIFEST), 'utf8'));
const languageTargets = Object.fromEntries(
	ashiraManifest.languages.map((item) => [item.lang, new URL(item.public_url).pathname])
);
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
	return page.evaluate((expectedLanguageTargets) => {
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
			'.nlh-project-language-rail button',
			'.nlh-project-language-rail a',
			'.nlh-project-language-rail span',
			'.nlh-home-languages button',
			'.nlh-home-languages a',
			'.nlh-home-languages span',
			'.nle-nav a',
			'.nle-langs span',
			'.nl-site-nav a',
			'.nl-site-link',
			'.nl-site-cta',
			'.nl-site-lang a',
			'.nl-site-footer a'
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
		const hero = rect('.nlh-home-hero');
		const showroom = rect('#showroom');
		const activeLanguage = document.querySelector('.nlh-project-language-rail [data-nle-lang].is-active')?.getAttribute('data-nle-lang') || '';
		const catalogLanguageUrls = Object.fromEntries(
			[...document.querySelectorAll('.nle-catalog .nlh-project-language-rail a[data-nle-lang][href]')].map((link) => [
				link.getAttribute('data-nle-lang'),
				new URL(link.href, window.location.href).pathname
			])
		);
		const defaultChromeWords = [
			'Blog',
			'About',
			'FAQs',
			'Authors',
			'Events',
			'Shop',
			'Patterns',
			'Themes',
			'Designed with WordPress',
			'NadLan Revenue'
		];
		return {
			title: document.title,
			h1s: [...document.querySelectorAll('h1')].map((h) => h.textContent.trim()),
			headerRoutes: document.querySelectorAll('.nl-site-nav a').length,
			footerLinks: document.querySelectorAll('.nl-site-footer a').length,
			languageEntries: document.querySelectorAll('.nlh-home-languages button, .nlh-home-languages a, .nlh-home-languages span, .nle-langs span').length,
			catalogLanguageEntries: document.querySelectorAll('.nle-catalog .nlh-project-language-rail button, .nle-catalog .nlh-project-language-rail a, .nle-catalog .nlh-project-language-rail span').length,
			catalogLanguageButtons: document.querySelectorAll('.nle-catalog .nlh-project-language-rail button[data-nle-lang]').length,
			catalogLanguageLinks: document.querySelectorAll('.nle-catalog .nlh-project-language-rail a[data-nle-lang][href]').length,
			catalogLanguageUrls,
			languageProjectTargetsOk: Object.entries(expectedLanguageTargets).every(([lang, pathname]) => catalogLanguageUrls[lang] === pathname),
			activeLanguage,
			heroLang: document.querySelector('.nlh-home-hero')?.getAttribute('lang') || '',
			heroDir: document.querySelector('.nlh-home-hero')?.getAttribute('dir') || '',
			heroTitle: document.querySelector('[data-nle-home-text="hero_title"]')?.textContent.trim() || '',
			catalogTitle: document.querySelector('[data-nle-home-text="catalog_title"]')?.textContent.trim() || '',
			catalogDir: document.querySelector('.nle-catalog')?.getAttribute('dir') || '',
			showroomDir: document.querySelector('.nle-showroom')?.getAttribute('dir') || '',
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
			hasEnglishEngineText: /Quick apartment picker|Want to check this apartment|projects to compare|Estimate by request/.test(visibleText),
			hasBuyerWords: /(דירה|דירות|פרויקט|פרויקטים|מחיר|אומדן|זמינות)/.test(visibleText),
			hasProjectBandBuyerCopy: visibleText.includes('השוואת פרויקטים חדשים לפי דירה, נוף ואומדן') && visibleText.includes('בכל פרויקט מוצגים דגם תלת ממדי'),
			hasMojibake: /Ã|�|×[^\s]*×/.test(visibleText),
			hasInternalWords: /(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה|אזור הבחירה המרכזי של דף הבית)/i.test(visibleText),
			hasDefaultChromeWords: defaultChromeWords.some((word) => visibleText.includes(word)),
			hero,
			catalog,
			showroom
		};
	}, languageTargets);
}

function failuresFor(viewName, before, after, english, errors, viewportHeight) {
	const failures = [];
	if (errors.length) failures.push(`${viewName}: console/page errors: ${errors.join(' | ')}`);
	if (before.h1s.length !== 1) failures.push(`${viewName}: expected one H1, got ${before.h1s.length}`);
	if (before.headerRoutes < 7) failures.push(`${viewName}: expected at least 7 real-estate header routes`);
	if (before.footerLinks < 20) failures.push(`${viewName}: expected at least 20 footer links`);
	if (before.languageEntries < 5) failures.push(`${viewName}: expected at least 5 language entries`);
	if (before.catalogLanguageEntries < 5) failures.push(`${viewName}: expected multilingual entries inside the project selector`);
	if (before.catalogLanguageLinks < 5) failures.push(`${viewName}: expected real language links inside the project selector`);
	if (!before.languageProjectTargetsOk) failures.push(`${viewName}: project language links do not match Ashira publication target URLs`);
	if (!english || english.activeLanguage !== 'en') failures.push(`${viewName}: English project language control did not become active`);
	if (!english || english.heroLang !== 'en' || english.heroDir !== 'ltr') failures.push(`${viewName}: English homepage hero did not switch to ltr`);
	if (!english || !/Check the project/.test(english.heroTitle)) failures.push(`${viewName}: English homepage hero text did not render`);
	if (!english || !/Compare new projects/.test(english.catalogTitle)) failures.push(`${viewName}: English project comparison title did not render`);
	if (!english || english.catalogDir !== 'ltr' || english.showroomDir !== 'ltr') failures.push(`${viewName}: English project selector/showroom did not switch to ltr`);
	if (!english || !english.hasEnglishEngineText) failures.push(`${viewName}: English project selector text did not render`);
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
	if (!before.hasProjectBandBuyerCopy) failures.push(`${viewName}: buyer-facing project band copy missing`);
	if (before.hasMojibake || after.hasMojibake) failures.push(`${viewName}: mojibake detected`);
	if (before.hasInternalWords || after.hasInternalWords) failures.push(`${viewName}: public internal wording detected`);
	if (before.hasDefaultChromeWords || after.hasDefaultChromeWords) failures.push(`${viewName}: default theme chrome wording detected`);
	if (!before.catalog || before.catalog.y > viewportHeight) failures.push(`${viewName}: project comparison section is not above the first viewport`);
	if (!before.hero || !before.catalog || before.catalog.y < before.hero.bottom - 12) failures.push(`${viewName}: project selector must sit after the opening hero, not at the absolute top`);
	if (!before.hero || !before.showroom || before.showroom.y < before.hero.bottom - 12) failures.push(`${viewName}: interactive showroom must sit after the opening hero, not at the absolute top`);
	if (!before.catalog || !before.showroom || before.catalog.y > before.showroom.y) failures.push(`${viewName}: project comparison must appear before the interactive showroom`);
	if (!before.showroom || before.showroom.y > viewportHeight * 1.75) failures.push(`${viewName}: interactive showroom starts too low after the project comparison rail`);
	return failures;
}

async function proofLanguage(page, lang) {
	const button = page.locator(`[data-nle-lang="${lang}"]`).first();
	if (await button.count()) await button.click();
	await page.waitForTimeout(300);
	return page.evaluate((activeLang) => {
		const text = document.body.innerText || '';
		const expected = {
			fr: /Choix rapide|projets à comparer|Estimation sur demande/,
			ru: /Быстрый выбор|проектов для сравнения|Оценка по запросу/,
			ar: /اختيار سريع|مشاريع للمقارنة|تقدير حسب الطلب/
		};
		const expectedHero = {
			fr: /Verifier le projet/,
			ru: /Проверьте проект/,
			ar: /افحصوا المشروع/
		};
		return {
			lang: activeLang,
			activeLanguage: document.querySelector('.nlh-project-language-rail [data-nle-lang].is-active')?.getAttribute('data-nle-lang') || '',
			heroLang: document.querySelector('.nlh-home-hero')?.getAttribute('lang') || '',
			heroDir: document.querySelector('.nlh-home-hero')?.getAttribute('dir') || '',
			heroTitle: document.querySelector('[data-nle-home-text="hero_title"]')?.textContent.trim() || '',
			catalogTitle: document.querySelector('[data-nle-home-text="catalog_title"]')?.textContent.trim() || '',
			catalogDir: document.querySelector('.nle-catalog')?.getAttribute('dir') || '',
			showroomDir: document.querySelector('.nle-showroom')?.getAttribute('dir') || '',
			hasExpectedText: expected[activeLang] ? expected[activeLang].test(text) : true,
			hasExpectedHero: expectedHero[activeLang] ? expectedHero[activeLang].test(text) : true
		};
	}, lang);
}

function languageFailures(viewName, proofs) {
	const expectedDir = { fr: 'ltr', ru: 'ltr', ar: 'rtl' };
	const expectedCatalog = {
		fr: /Comparer les nouveaux projets/,
		ru: /Сравните новые проекты/,
		ar: /قارنوا المشاريع الجديدة/
	};
	return proofs.flatMap((proof) => {
		const failures = [];
		if (proof.activeLanguage !== proof.lang) failures.push(`${viewName}: ${proof.lang} language control did not become active`);
		if (proof.heroLang !== proof.lang || proof.heroDir !== expectedDir[proof.lang]) failures.push(`${viewName}: ${proof.lang} homepage hero language/direction mismatch`);
		if (proof.catalogDir !== expectedDir[proof.lang] || proof.showroomDir !== expectedDir[proof.lang]) failures.push(`${viewName}: ${proof.lang} direction mismatch`);
		if (!proof.hasExpectedText) failures.push(`${viewName}: ${proof.lang} translated project selector text did not render`);
		if (!proof.hasExpectedHero) failures.push(`${viewName}: ${proof.lang} translated homepage hero text did not render`);
		if (expectedCatalog[proof.lang] && !expectedCatalog[proof.lang].test(proof.catalogTitle)) failures.push(`${viewName}: ${proof.lang} translated project comparison title did not render`);
		return failures;
	});
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
			const englishButton = page.locator('[data-nle-lang="en"]').first();
			if (await englishButton.count()) await englishButton.click();
			await page.waitForTimeout(500);
			await page.screenshot({ path: path.join(outDir, `${vp.name}-english.png`), fullPage: true });
			const english = await measure(page);
			const otherLanguageProofs = [];
			for (const lang of ['fr', 'ru', 'ar']) {
				otherLanguageProofs.push(await proofLanguage(page, lang));
			}
			const failures = failuresFor(vp.name, before, after, english, errors, vp.height).concat(languageFailures(vp.name, otherLanguageProofs));
			allFailures.push(...failures);
			report.viewports.push({ name: vp.name, before, after, english, otherLanguageProofs, failures });
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
