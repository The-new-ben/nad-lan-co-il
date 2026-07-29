#!/usr/bin/env node

import { spawn } from 'node:child_process';
import crypto from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = process.cwd();
const BASE_URL = process.env.UTOPIA_PREVIEW_BASE || 'http://127.0.0.1:4173';
const OUT_DIR = path.resolve(
	ROOT,
	'docs/qa/screenshots/utopia-preview-2026-07-29'
);
const MODEL_RELATIVE_PATH = 'plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb';
const MODEL_PATH = path.resolve(ROOT, MODEL_RELATIVE_PATH);
const EXPECTED_MODEL_SHA256 = 'ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24';
const MODEL_BYTES = await readFile(MODEL_PATH);
const MODEL_SHA256 = crypto.createHash('sha256').update(MODEL_BYTES).digest('hex');

const LANGUAGES = {
	he: {
		title: 'UTOPIA שדה דב תל אביב - מחירים, דירות ובחירה מהבניין',
		dir: 'rtl',
		secnavBuilding: 'בניין',
		buildingTitle: 'ארבעת מבני הפרויקט',
		buildingPrompt: 'לחצו על מבנה כדי לראות את נתוני התכנון שפורסמו.',
		plansTitle: 'תוכניות דוגמה שפורסמו',
		floorsLabel: 'קומות שפורסמו',
		heightLabel: 'גובה מרבי מתוכנן',
		sourceLabel: 'מסמך התכנון העירוני',
		n1: 'בניין N1',
	},
	en: {
		title: 'UTOPIA Sde Dov Tel Aviv - Apartments for Sale, Prices and Choosing a Home',
		dir: 'ltr',
		secnavBuilding: 'Building',
		buildingTitle: "The project's four buildings",
		buildingPrompt: 'Select a building to view its published planning data.',
		plansTitle: 'Published sample plans',
		floorsLabel: 'Published floors',
		heightLabel: 'Planned maximum height',
		sourceLabel: 'Municipal planning document',
		n1: 'N1 building',
	},
	fr: {
		title: "UTOPIA Sde Dov Tel Aviv - Appartements à vendre, prix et choix d'un logement",
		dir: 'ltr',
		secnavBuilding: 'Immeuble',
		buildingTitle: 'Les quatre bâtiments du projet',
		buildingPrompt: "Sélectionnez un bâtiment pour consulter les données d'urbanisme publiées.",
		plansTitle: "Plans d'exemple publiés",
		floorsLabel: 'Étages publiés',
		heightLabel: 'Hauteur maximale projetée',
		sourceLabel: "Document municipal d'urbanisme",
		n1: 'Bâtiment N1',
	},
	ru: {
		title: 'UTOPIA Sde Dov Тель-Авив - квартиры на продажу, цены и выбор квартиры',
		dir: 'ltr',
		secnavBuilding: 'Здание',
		buildingTitle: 'Четыре здания проекта',
		buildingPrompt: 'Выберите здание, чтобы увидеть опубликованные параметры планирования.',
		plansTitle: 'Опубликованные примеры планов',
		floorsLabel: 'Опубликованная этажность',
		heightLabel: 'Планируемая предельная высота',
		sourceLabel: 'Муниципальный документ планирования',
		n1: 'Здание N1',
	},
	ar: {
		title: 'UTOPIA Sde Dov تل أبيب - شقق للبيع والأسعار واختيار الشقة',
		dir: 'rtl',
		secnavBuilding: 'المبنى',
		buildingTitle: 'المباني الأربعة في المشروع',
		buildingPrompt: 'اختر مبنى للاطلاع على بيانات التخطيط المنشورة.',
		plansTitle: 'نماذج المخططات المنشورة',
		floorsLabel: 'الطوابق المنشورة',
		heightLabel: 'الارتفاع الأقصى المخطط',
		sourceLabel: 'وثيقة التخطيط البلدية',
		n1: 'المبنى N1',
	},
};

const ENGLISH_UI_PHRASES = [
	'Building',
	'Published sample plans',
	'Orientation model',
	"The project's four buildings",
	'Select a building to view its published planning data.',
	'Published floors',
	'Planned maximum height',
	'Municipal planning document',
	'Close building details',
	'Request information',
];

const CASES = [
	...Object.keys(LANGUAGES).map((lang) => ({
		lang,
		viewportName: 'desktop-1440x1000',
		viewport: { width: 1440, height: 1000 },
		isMobile: false,
	})),
	...Object.keys(LANGUAGES).map((lang) => ({
		lang,
		viewportName: 'mobile-390x844',
		viewport: { width: 390, height: 844 },
		isMobile: true,
	})),
];

function normalizedText(value) {
	return String(value || '').replace(/\s+/g, ' ').trim();
}

function addAssertion(assertions, name, actual, expected, pass = actual === expected) {
	assertions.push({ name, pass, expected, actual });
}

async function fetchPreview() {
	try {
		const response = await fetch(
			`${BASE_URL}/docs/previews/utopia-sde-dov-he-preview.html`,
			{ signal: AbortSignal.timeout(5000) }
		);
		return response.ok;
	} catch {
		return false;
	}
}

async function ensurePreviewServer() {
	if (await fetchPreview()) {
		return { startedByQa: false, process: null };
	}

	const url = new URL(BASE_URL);
	if (url.hostname !== '127.0.0.1' && url.hostname !== 'localhost') {
		throw new Error(`Preview server is unavailable and is not local: ${BASE_URL}`);
	}

	const serverProcess = spawn(
		'php',
		['-S', `${url.hostname}:${url.port || '80'}`, '-t', ROOT],
		{
			cwd: ROOT,
			detached: false,
			stdio: 'ignore',
			windowsHide: true,
		}
	);

	const deadline = Date.now() + 15000;
	while (Date.now() < deadline) {
		if (await fetchPreview()) {
			return { startedByQa: true, process: serverProcess };
		}
		await new Promise((resolve) => setTimeout(resolve, 300));
	}

	serverProcess.kill();
	throw new Error(`Could not start PHP preview server at ${BASE_URL}`);
}

async function waitForModel(page) {
	await page.locator('#building').scrollIntoViewIfNeeded();
	await page.waitForFunction(
		() => Boolean(customElements.get('model-viewer')),
		null,
		{ timeout: 30000 }
	);
	await page.waitForFunction(
		() => {
			const model = document.querySelector('#nl-mv');
			return Boolean(model && model.loaded === true && model.modelIsVisible === true);
		},
		null,
		{ timeout: 45000 }
	);
	await page.waitForTimeout(600);
}

async function inspectInitial(page, lang) {
	return page.evaluate(({ expectedLang, englishPhrases }) => {
		const visible = (element) => {
			if (!element) return false;
			const rect = element.getBoundingClientRect();
			const style = getComputedStyle(element);
			return (
				rect.width > 0 &&
				rect.height > 0 &&
				style.display !== 'none' &&
				style.visibility !== 'hidden' &&
				Number(style.opacity || 1) > 0
			);
		};
		const text = (selector) => {
			const element = document.querySelector(selector);
			return element ? element.textContent.replace(/\s+/g, ' ').trim() : '';
		};
		const article = document.querySelector('.nadlan-project-article');
		const app = document.querySelector('#nl-root.nl-app');
		const model = document.querySelector('#nl-mv');
		const modelRect = model ? model.getBoundingClientRect() : null;
		const appText = app ? app.innerText.replace(/\s+/g, ' ').trim() : '';
		const untranslatedEnglish = expectedLang === 'en'
			? []
			: englishPhrases.filter((phrase) => appText.includes(phrase));
		const mediaImages = [...document.querySelectorAll('.utopia-media-gallery img')];
		const modelError = document.querySelector('#nl-model-error');
		const clientWidth = document.documentElement.clientWidth;
		const leadParagraph = document.querySelector('.nadlan-project-lead > p:first-of-type');
		const parseRgb = (value) => {
			const parts = String(value || '').match(/[\d.]+/g);
			return parts && parts.length >= 3 ? parts.slice(0, 3).map(Number) : [0, 0, 0];
		};
		const luminance = (rgb) => rgb
			.map((channel) => channel / 255)
			.map((channel) => channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4)
			.reduce((sum, channel, index) => sum + channel * [0.2126, 0.7152, 0.0722][index], 0);
		const textLum = luminance(parseRgb(leadParagraph ? getComputedStyle(leadParagraph).color : 'rgb(0,0,0)'));
		const backgroundLum = luminance(parseRgb(getComputedStyle(document.body).backgroundColor));
		const leadContrastRatio = (Math.max(textLum, backgroundLum) + 0.05) / (Math.min(textLum, backgroundLum) + 0.05);
		const emptyHeadings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')]
			.filter((heading) => !heading.textContent.replace(/\s+/g, ' ').trim())
			.map((heading) => heading.outerHTML.slice(0, 180));
		const legacyBlocks = [...document.querySelectorAll('.nlpf,.nlpjx-nav,.nlpjx-intro,.nlpjx-price,.nlpjx,.nlcard,.nlms,.nlpe')]
			.map((element) => element.className);
		const templateRelativeHrefs = [...document.querySelectorAll('#nl-root a[href]')]
			.map((anchor) => anchor.getAttribute('href'))
			.filter((href) => /(?:^|\/)(?:home|project)\.html(?:[?#]|$)/i.test(href || ''));
		const h1 = document.querySelector('h1');
		const root = document.querySelector('#nl-root');
		const heroImage = document.querySelector('.nl-hero__media img');
		const buildingHotspots = [...document.querySelectorAll('.nl-building-hot[data-act="building"]')];
		const utopiaStylesheets = [...document.querySelectorAll('link[rel="stylesheet"]')]
			.map((link) => link.getAttribute('href') || '')
			.filter((href) => /\/projects\/utopia-sde-dov\/utopia\.css(?:[?#]|$)/.test(href));
		const overflowingElements = [...document.querySelectorAll('body *')]
			.map((element) => {
				const rect = element.getBoundingClientRect();
				return {
					tag: element.tagName.toLowerCase(),
					id: element.id || null,
					className: String(element.className || '').slice(0, 120),
					left: Math.round(rect.left),
					right: Math.round(rect.right),
					width: Math.round(rect.width),
					text: (element.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 120),
				};
			})
			.filter((element) => element.width > 0 && element.right > clientWidth + 1)
			.sort((a, b) => b.right - a.right)
			.slice(0, 12);

		return {
			url: location.href,
			title: document.title,
			documentLang: document.documentElement.lang,
			documentDir: document.documentElement.dir,
			articleComputedDir: article ? getComputedStyle(article).direction : null,
			appComputedDir: app ? getComputedStyle(app).direction : null,
			h1Count: document.querySelectorAll('h1').length,
			h1Text: text('h1'),
			h1PrecedesShowroom: Boolean(h1 && root && (h1.compareDocumentPosition(root) & Node.DOCUMENT_POSITION_FOLLOWING)),
			leadTextColor: leadParagraph ? getComputedStyle(leadParagraph).color : null,
			leadBackgroundColor: getComputedStyle(document.body).backgroundColor,
			leadContrastRatio: Number(leadContrastRatio.toFixed(2)),
			emptyHeadings,
			legacyBlocks,
			templateRelativeHrefs,
			heroImageAlt: heroImage ? heroImage.getAttribute('alt') : '',
			buildingHotspots: buildingHotspots.length,
			buildingHotspotLabels: buildingHotspots.map((hotspot) => hotspot.textContent.replace(/\s+/g, ' ').trim()),
			buildingHotspotAriaLabels: buildingHotspots.map((hotspot) => hotspot.getAttribute('aria-label')),
			buildingModeClass: Boolean(app && app.classList.contains('nl-app--building')),
			utopiaStylesheetCount: utopiaStylesheets.length,
			unitHotspots: document.querySelectorAll('.nl-hot[data-act="select"], [slot^="hotspot-unit-"], [data-act="select"][data-id]').length,
			samplePlanCards: document.querySelectorAll('.nl-plan-card').length,
			articleMediaImages: mediaImages.length,
			articleMediaImagesLoaded: mediaImages.filter((image) => image.complete && image.naturalWidth > 0).length,
			modelViewerCount: document.querySelectorAll('model-viewer').length,
			modelCustomElementDefined: Boolean(customElements.get('model-viewer')),
			modelSrc: model ? model.getAttribute('src') : null,
			modelLoaded: Boolean(model && model.loaded === true),
			modelIsVisible: Boolean(model && model.modelIsVisible === true),
			modelVisibleBox: modelRect
				? {
					x: Math.round(modelRect.x),
					y: Math.round(modelRect.y),
					width: Math.round(modelRect.width),
					height: Math.round(modelRect.height),
					visible: visible(model),
				}
				: null,
			modelErrorVisible: Boolean(modelError && visible(modelError) && !modelError.hidden),
			firstSectionNavLabel: text('#nl-secnav a'),
			buildingTitle: text('.nl-theater__title h2'),
			buildingPrompt: text('.nl-building-prompt'),
			plansTitle: text('#inventory h2'),
			untranslatedEnglish,
			documentClientWidth: clientWidth,
			documentScrollWidth: document.documentElement.scrollWidth,
			horizontalOverflowPx: Math.max(0, document.documentElement.scrollWidth - clientWidth),
			overflowingElements,
		};
	}, { expectedLang: lang, englishPhrases: ENGLISH_UI_PHRASES });
}

async function inspectSelected(page) {
	return page.evaluate(() => {
		const text = (selector) => {
			const element = document.querySelector(selector);
			return element ? element.textContent.replace(/\s+/g, ' ').trim() : '';
		};
		const panel = document.querySelector('#nl-panel');
		const close = document.querySelector('.nl-panel__close');
		const factLabels = [...document.querySelectorAll('.nl-building-facts span')]
			.map((node) => node.textContent.replace(/\s+/g, ' ').trim());
		return {
			panelOpen: Boolean(panel && panel.classList.contains('is-open')),
			panelTitle: text('.nl-panel__title'),
			factLabels,
			sourceLabel: text('.nl-building-source'),
			panelPlanLinks: document.querySelectorAll('.nl-building-plan').length,
			closeAriaLabel: close ? close.getAttribute('aria-label') : null,
			activeBuildingHotspots: document.querySelectorAll('.nl-building-hot.is-active').length,
			activeBuildingId: document.querySelector('.nl-building-hot.is-active')?.getAttribute('data-id') || null,
		};
	});
}

function assertionsFor(testCase, initial, selected, browserEvents) {
	const expected = LANGUAGES[testCase.lang];
	const assertions = [];
	addAssertion(assertions, 'exact document title', initial.title, expected.title);
	addAssertion(assertions, 'document language', initial.documentLang, testCase.lang);
	addAssertion(assertions, 'document direction', initial.documentDir, expected.dir);
	addAssertion(assertions, 'article inherited direction', initial.articleComputedDir, expected.dir);
	addAssertion(assertions, 'showroom inherited direction', initial.appComputedDir, expected.dir);
	addAssertion(assertions, 'one H1', initial.h1Count, 1);
	addAssertion(assertions, 'H1 equals SEO title', initial.h1Text, expected.title);
	addAssertion(assertions, 'buyer H1 precedes showroom', initial.h1PrecedesShowroom, true);
	addAssertion(assertions, 'opening paragraph contrast at least 4.5:1', initial.leadContrastRatio >= 4.5, true);
	addAssertion(assertions, 'no empty headings', initial.emptyHeadings, [], initial.emptyHeadings.length === 0);
	addAssertion(assertions, 'no legacy project blocks', initial.legacyBlocks, [], initial.legacyBlocks.length === 0);
	addAssertion(assertions, 'no template-relative home or project URLs', initial.templateRelativeHrefs, [], initial.templateRelativeHrefs.length === 0);
	addAssertion(assertions, 'concept disclosure in hero image alt', /concept|הדמי|концептуаль|تصور|illustration/i.test(initial.heroImageAlt), true);
	addAssertion(assertions, 'four building hotspots', initial.buildingHotspots, 4);
	addAssertion(
		assertions,
		'stable building hotspot labels',
		initial.buildingHotspotLabels,
		['S1', 'N1', 'N2', 'S2'],
		JSON.stringify(initial.buildingHotspotLabels) === JSON.stringify(['S1', 'N1', 'N2', 'S2'])
	);
	addAssertion(
		assertions,
		'localized N1 hotspot accessible label',
		initial.buildingHotspotAriaLabels[1] || null,
		expected.n1
	);
	addAssertion(assertions, 'UTOPIA building-mode root class', initial.buildingModeClass, true);
	addAssertion(assertions, 'one route-scoped UTOPIA stylesheet', initial.utopiaStylesheetCount, 1);
	addAssertion(assertions, 'zero unit hotspots', initial.unitHotspots, 0);
	addAssertion(assertions, 'seven sample plan cards', initial.samplePlanCards, 7);
	addAssertion(assertions, 'four article media images', initial.articleMediaImages, 4);
	addAssertion(assertions, 'four article media images loaded', initial.articleMediaImagesLoaded, 4);
	addAssertion(assertions, 'one model viewer', initial.modelViewerCount, 1);
	addAssertion(assertions, 'model-viewer custom element defined', initial.modelCustomElementDefined, true);
	addAssertion(
		assertions,
		'UTOPIA GLB source',
		initial.modelSrc,
		'/plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb'
	);
	addAssertion(assertions, 'one optimized GLB request', browserEvents.modelAssetRequests, 1);
	addAssertion(
		assertions,
		'optimized GLB SHA-256',
		browserEvents.modelAssetSha256,
		EXPECTED_MODEL_SHA256
	);
	addAssertion(assertions, 'GLB loaded', initial.modelLoaded, true);
	addAssertion(assertions, 'GLB visible', initial.modelIsVisible, true);
	addAssertion(
		assertions,
		'model has visible dimensions',
		Boolean(initial.modelVisibleBox?.visible && initial.modelVisibleBox.width > 0 && initial.modelVisibleBox.height > 0),
		true
	);
	addAssertion(assertions, 'model error hidden', initial.modelErrorVisible, false);
	addAssertion(assertions, 'localized building section navigation', initial.firstSectionNavLabel, expected.secnavBuilding);
	addAssertion(assertions, 'localized building title', initial.buildingTitle, expected.buildingTitle);
	addAssertion(assertions, 'localized building prompt', initial.buildingPrompt, expected.buildingPrompt);
	addAssertion(assertions, 'localized sample plans heading', initial.plansTitle, expected.plansTitle);
	addAssertion(
		assertions,
		'no obvious untranslated English UI labels',
		initial.untranslatedEnglish,
		[],
		initial.untranslatedEnglish.length === 0
	);
	addAssertion(assertions, 'building click opens detail panel', selected.panelOpen, true);
	addAssertion(assertions, 'localized selected building title', selected.panelTitle, expected.n1);
	addAssertion(
		assertions,
		'localized floor label',
		selected.factLabels[0] || null,
		expected.floorsLabel
	);
	addAssertion(
		assertions,
		'localized height label',
		selected.factLabels[1] || null,
		expected.heightLabel
	);
	addAssertion(assertions, 'localized source label', selected.sourceLabel, expected.sourceLabel);
	addAssertion(assertions, 'N1 sample plan links in panel', selected.panelPlanLinks, 4);
	addAssertion(assertions, 'one active building hotspot', selected.activeBuildingHotspots, 1);
	addAssertion(assertions, 'N1 hotspot active', selected.activeBuildingId, 'n1');
	addAssertion(
		assertions,
		'no console errors',
		browserEvents.consoleErrors,
		[],
		browserEvents.consoleErrors.length === 0
	);
	addAssertion(
		assertions,
		'no page errors',
		browserEvents.pageErrors,
		[],
		browserEvents.pageErrors.length === 0
	);
	if (testCase.isMobile) {
		addAssertion(assertions, 'no mobile horizontal overflow', initial.horizontalOverflowPx, 0);
	}

	return assertions;
}

async function runCase(browser, testCase) {
	const expected = LANGUAGES[testCase.lang];
	const context = await browser.newContext({
		viewport: testCase.viewport,
		deviceScaleFactor: 1,
		isMobile: testCase.isMobile,
		hasTouch: testCase.isMobile,
		locale: testCase.lang === 'he'
			? 'he-IL'
			: testCase.lang === 'ar'
				? 'ar'
				: `${testCase.lang}-${testCase.lang === 'en' ? 'US' : testCase.lang.toUpperCase()}`,
	});
	const page = await context.newPage();
	const browserEvents = {
		consoleErrors: [],
		pageErrors: [],
		requestFailures: [],
		locallyRoutedMedia: [],
		modelAssetRequests: 0,
		modelAssetSha256: null,
	};

	await page.route(
		'**/plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb',
		async (route) => {
			browserEvents.modelAssetRequests += 1;
			browserEvents.modelAssetSha256 = MODEL_SHA256;
			await route.fulfill({
				status: 200,
				contentType: 'model/gltf-binary',
				body: MODEL_BYTES,
			});
		}
	);

	await page.route(
		/^https:\/\/nad-lan\.co\.il\/wp-content\/plugins\/nadlan-config\/assets\/showroom-engine\/projects\/utopia-sde-dov\/[^?]+$/,
		async (route) => {
			const requestUrl = new URL(route.request().url());
			const localRelativePath = decodeURIComponent(requestUrl.pathname).replace(/^\/wp-content\//, '');
			const localPath = path.resolve(ROOT, localRelativePath);
			if (!localPath.startsWith(ROOT)) {
				await route.abort('blockedbyclient');
				return;
			}
			browserEvents.locallyRoutedMedia.push(localRelativePath);
			await route.fulfill({
				status: 200,
				contentType: 'image/webp',
				body: await readFile(localPath),
			});
		}
	);

	page.on('console', (message) => {
		if (message.type() === 'error') {
			browserEvents.consoleErrors.push(normalizedText(message.text()));
		}
	});
	page.on('pageerror', (error) => {
		browserEvents.pageErrors.push(normalizedText(error.message));
	});
	page.on('requestfailed', (request) => {
		browserEvents.requestFailures.push({
			url: request.url(),
			error: request.failure()?.errorText || 'unknown request failure',
		});
	});

	const conflictingLang = { he: 'fr', en: 'ar', fr: 'he', ru: 'en', ar: 'ru' }[testCase.lang];
	const url = `${BASE_URL}/docs/previews/utopia-sde-dov-${testCase.lang}-preview.html?lang=${conflictingLang}`;
	await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
	await page.waitForSelector('#nl-root.nl-app', { timeout: 30000 });
	await page.locator('h1').scrollIntoViewIfNeeded();
	await page.waitForTimeout(250);
	const prefix = `${testCase.lang}-${testCase.viewportName}`;
	const topScreenshot = path.join(OUT_DIR, `${prefix}-top.png`);
	await page.screenshot({ path: topScreenshot, fullPage: false });
	await waitForModel(page);
	const articleMedia = page.locator('.utopia-media-gallery img');
	for (let index = 0; index < await articleMedia.count(); index += 1) {
		await articleMedia.nth(index).scrollIntoViewIfNeeded();
	}
	await page.waitForFunction(
		() => [...document.querySelectorAll('.utopia-media-gallery img')]
			.every((image) => image.complete && image.naturalWidth > 0),
		null,
		{ timeout: 30000 }
	);
	await page.locator('#building').scrollIntoViewIfNeeded();
	await page.waitForTimeout(300);

	const initialScreenshot = path.join(OUT_DIR, `${prefix}-initial.png`);
	const selectedScreenshot = path.join(OUT_DIR, `${prefix}-selected-n1.png`);
	await page.screenshot({ path: initialScreenshot, fullPage: false });
	const initial = await inspectInitial(page, testCase.lang);

	const n1 = page.locator('.nl-building-hot[data-id="n1"]');
	if (await n1.count() === 1) {
		await n1.click({ timeout: 15000 });
		await page.waitForFunction(
			(label) => {
				const panel = document.querySelector('#nl-panel');
				const title = document.querySelector('.nl-panel__title');
				return Boolean(
					panel?.classList.contains('is-open') &&
					title?.textContent.replace(/\s+/g, ' ').trim() === label
				);
			},
			expected.n1,
			{ timeout: 15000 }
		);
		await page.waitForTimeout(900);
	}

	await page.screenshot({ path: selectedScreenshot, fullPage: false });
	const selected = await inspectSelected(page);
	const assertions = assertionsFor(testCase, initial, selected, browserEvents);
	const failures = assertions
		.filter((assertion) => !assertion.pass)
		.map((assertion) => ({
			name: assertion.name,
			expected: assertion.expected,
			actual: assertion.actual,
		}));
	const warnings = [];
	if (initial.horizontalOverflowPx > 1) {
		warnings.push({
			name: 'document horizontal overflow',
			detail: `${initial.horizontalOverflowPx}px wider than the ${initial.documentClientWidth}px viewport`,
			overflowingElements: initial.overflowingElements,
		});
	}
	if (browserEvents.requestFailures.length) {
		warnings.push({
			name: 'failed network requests',
			detail: browserEvents.requestFailures,
		});
	}

	await context.close();
	return {
		lang: testCase.lang,
		viewport: testCase.viewportName,
		dimensions: testCase.viewport,
		url,
		pass: failures.length === 0,
		initial,
		selected,
		browserEvents,
		assertions,
		failures,
		warnings,
		screenshots: {
			top: path.relative(ROOT, topScreenshot).replaceAll('\\', '/'),
			initial: path.relative(ROOT, initialScreenshot).replaceAll('\\', '/'),
			selected: path.relative(ROOT, selectedScreenshot).replaceAll('\\', '/'),
		},
	};
}

async function main() {
	await mkdir(OUT_DIR, { recursive: true });
	const server = await ensurePreviewServer();
	const browser = await chromium.launch({ channel: 'chrome', headless: true });
	const report = {
		createdAt: new Date().toISOString(),
		baseUrl: BASE_URL,
		evidenceDirectory: path.relative(ROOT, OUT_DIR).replaceAll('\\', '/'),
		serverStartedByQa: server.startedByQa,
		previewAssetNote: 'The four not-yet-deployed public media URLs were fulfilled from the exact local UTOPIA release WebP files during static preview QA.',
		modelAsset: {
			path: MODEL_RELATIVE_PATH,
			bytes: MODEL_BYTES.length,
			expectedSha256: EXPECTED_MODEL_SHA256,
			actualSha256: MODEL_SHA256,
			exactExpectedAsset: MODEL_SHA256 === EXPECTED_MODEL_SHA256,
		},
		cases: [],
		pass: false,
	};

	try {
		for (const testCase of CASES) {
			const result = await runCase(browser, testCase);
			report.cases.push(result);
			console.log(
				`${result.pass ? 'PASS' : 'FAIL'} ${result.lang} ${result.viewport}` +
				(result.failures.length ? ` - ${result.failures.map((failure) => failure.name).join(', ')}` : '')
			);
		}
		report.pass = report.cases.every((result) => result.pass);
		report.summary = {
			totalCases: report.cases.length,
			passedCases: report.cases.filter((result) => result.pass).length,
			failedCases: report.cases.filter((result) => !result.pass).length,
			totalAssertions: report.cases.reduce((sum, result) => sum + result.assertions.length, 0),
			failedAssertions: report.cases.reduce((sum, result) => sum + result.failures.length, 0),
			warningCases: report.cases.filter((result) => result.warnings.length > 0).length,
			totalWarnings: report.cases.reduce((sum, result) => sum + result.warnings.length, 0),
		};
	} finally {
		await browser.close();
		if (server.process) {
			server.process.kill();
		}
	}

	const reportPath = path.join(OUT_DIR, 'utopia-preview-browser-qa-report.json');
	await writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
	console.log(JSON.stringify({ pass: report.pass, summary: report.summary, report: reportPath }, null, 2));

	if (!report.pass) {
		process.exitCode = 1;
	}
}

main().catch(async (error) => {
	const failurePath = path.join(OUT_DIR, 'utopia-preview-browser-qa-fatal.json');
	await mkdir(OUT_DIR, { recursive: true });
	await writeFile(
		failurePath,
		`${JSON.stringify({ createdAt: new Date().toISOString(), error: error.stack || error.message }, null, 2)}\n`,
		'utf8'
	);
	console.error(error);
	process.exit(1);
});
