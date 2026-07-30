#!/usr/bin/env node

/**
 * Strict, real-Google-Chrome acceptance gate for the isolated UTOPIA showroom.
 *
 * Scope:
 * - static previews in all five languages;
 * - desktop 1440x1000 and mobile 390x844;
 * - buyer interactions, isolation, SEO head, media, model and network safety.
 *
 * This script deliberately knows nothing about #nl-root, NADLAN_SHOWROOM or
 * NLPJX_MAP except that they must not exist on a UTOPIA page.
 */

import { spawn } from 'node:child_process';
import crypto from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT = process.cwd();
const BASE_URL = process.env.UTOPIA_PREVIEW_BASE || 'http://127.0.0.1:4173';
const BASE_ORIGIN = new URL(BASE_URL).origin;
const RUN_DATE = new Date().toISOString().slice(0, 10);
const OUT_DIR = path.resolve(
	ROOT,
	`docs/qa/screenshots/utopia-isolated-browser-gate-${RUN_DATE}`
);
const REPORT_PATH = path.resolve(
	ROOT,
	'docs/qa/utopia-isolated-browser-report.json'
);
const CHROME_EXECUTABLE = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const MODEL_RELATIVE_PATH =
	'plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb';
const MODEL_PATH = path.resolve(ROOT, MODEL_RELATIVE_PATH);
const MODEL_URL_PATH = `/${MODEL_RELATIVE_PATH.replaceAll('\\', '/')}`;
const EXPECTED_MODEL_SHA256 =
	'ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24';
const EXPECTED_TRIANGLES = 21416;
const MODEL_BYTES = await readFile(MODEL_PATH);
const MODEL_SHA256 = crypto
	.createHash('sha256')
	.update(MODEL_BYTES)
	.digest('hex');

const LANGUAGE_ORDER = ['he', 'en', 'fr', 'ru', 'ar'];
const LANGUAGE_CONFIG = {
	he: {
		htmlLang: 'he-IL',
		rootLang: 'he',
		dir: 'rtl',
		canonical: 'https://nad-lan.co.il/projects/utopia-sde-dov/',
		switchPath: '/docs/previews/utopia-sde-dov-he-preview.html',
		locale: 'he-IL',
	},
	en: {
		htmlLang: 'en-US',
		rootLang: 'en',
		dir: 'ltr',
		canonical: 'https://nad-lan.co.il/projects/utopia-sde-dov-en/',
		switchPath: '/docs/previews/utopia-sde-dov-en-preview.html',
		locale: 'en-US',
	},
	fr: {
		htmlLang: 'fr-FR',
		rootLang: 'fr',
		dir: 'ltr',
		canonical: 'https://nad-lan.co.il/projects/utopia-sde-dov-fr/',
		switchPath: '/docs/previews/utopia-sde-dov-fr-preview.html',
		locale: 'fr-FR',
	},
	ru: {
		htmlLang: 'ru-RU',
		rootLang: 'ru',
		dir: 'ltr',
		canonical: 'https://nad-lan.co.il/projects/utopia-sde-dov-ru/',
		switchPath: '/docs/previews/utopia-sde-dov-ru-preview.html',
		locale: 'ru-RU',
	},
	ar: {
		htmlLang: 'ar',
		rootLang: 'ar',
		dir: 'rtl',
		canonical: 'https://nad-lan.co.il/projects/utopia-sde-dov-ar/',
		switchPath: '/docs/previews/utopia-sde-dov-ar-preview.html',
		locale: 'ar',
	},
};

const EXPECTED_HREFLANG = {
	he: 'https://nad-lan.co.il/projects/utopia-sde-dov/',
	en: 'https://nad-lan.co.il/projects/utopia-sde-dov-en/',
	fr: 'https://nad-lan.co.il/projects/utopia-sde-dov-fr/',
	ru: 'https://nad-lan.co.il/projects/utopia-sde-dov-ru/',
	ar: 'https://nad-lan.co.il/projects/utopia-sde-dov-ar/',
	'x-default': 'https://nad-lan.co.il/projects/utopia-sde-dov/',
};

const EXPECTED_PLAN_URL =
	'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-5E-404448525660-copy.pdf';

const VIEWPORTS = [
	{
		name: 'desktop-1440x1000',
		width: 1440,
		height: 1000,
		isMobile: false,
		hasTouch: false,
	},
	{
		name: 'mobile-390x844',
		width: 390,
		height: 844,
		isMobile: true,
		hasTouch: true,
	},
];

const CASES = VIEWPORTS.flatMap((viewport) =>
	LANGUAGE_ORDER.map((lang) => ({ lang, viewport }))
);

function normalizeText(value) {
	return String(value || '')
		.replace(/\s+/g, ' ')
		.trim();
}

function plainUrl(value) {
	try {
		const url = new URL(value);
		url.hash = '';
		return url.href;
	} catch {
		return String(value || '');
	}
}

function isFirstParty(value) {
	try {
		return new URL(value).origin === BASE_ORIGIN;
	} catch {
		return false;
	}
}

function isExpectedThirdPartyWarning(url, detail = '') {
	const host = (() => {
		try {
			return new URL(url).hostname;
		} catch {
			return '';
		}
	})();
	if (
		host === 'ajax.googleapis.com' ||
		host === 'utopiatlv.co.il' ||
		host.endsWith('.utopiatlv.co.il')
	) {
		return true;
	}
	return /ajax\.googleapis\.com|utopiatlv\.co\.il/i.test(
		`${url} ${detail}`
	);
}

function assertion(name, actual, expected, pass = actual === expected) {
	return { name, actual, expected, pass: Boolean(pass) };
}

function parseGlb(buffer) {
	if (buffer.length < 20) {
		throw new Error('GLB is too short');
	}
	const magic = buffer.readUInt32LE(0);
	const version = buffer.readUInt32LE(4);
	const declaredLength = buffer.readUInt32LE(8);
	if (magic !== 0x46546c67) {
		throw new Error(`Unexpected GLB magic 0x${magic.toString(16)}`);
	}
	if (version !== 2) {
		throw new Error(`Expected GLB version 2, received ${version}`);
	}
	if (declaredLength !== buffer.length) {
		throw new Error(
			`GLB declared ${declaredLength} bytes but file has ${buffer.length}`
		);
	}

	let offset = 12;
	let json = null;
	const chunks = [];
	while (offset + 8 <= buffer.length) {
		const length = buffer.readUInt32LE(offset);
		const type = buffer.readUInt32LE(offset + 4);
		const start = offset + 8;
		const end = start + length;
		if (end > buffer.length) {
			throw new Error('GLB chunk exceeds declared file length');
		}
		chunks.push({ type, length });
		if (type === 0x4e4f534a) {
			json = JSON.parse(
				buffer
					.subarray(start, end)
					.toString('utf8')
					.replace(/[\0\s]+$/u, '')
			);
		}
		offset = end;
	}
	if (!json) {
		throw new Error('GLB has no JSON chunk');
	}

	const primitives = [];
	let triangles = 0;
	for (const [meshIndex, mesh] of (json.meshes || []).entries()) {
		for (const [primitiveIndex, primitive] of (
			mesh.primitives || []
		).entries()) {
			const accessorIndex =
				primitive.indices ?? primitive.attributes?.POSITION;
			const count = json.accessors?.[accessorIndex]?.count;
			const mode = primitive.mode ?? 4;
			if (!Number.isFinite(count)) {
				throw new Error(
					`Missing accessor count for mesh ${meshIndex}, primitive ${primitiveIndex}`
				);
			}
			const primitiveTriangles =
				mode === 4
					? Math.floor(count / 3)
					: mode === 5 || mode === 6
						? Math.max(0, count - 2)
						: 0;
			triangles += primitiveTriangles;
			primitives.push({
				meshIndex,
				primitiveIndex,
				mode,
				indexOrVertexCount: count,
				triangles: primitiveTriangles,
			});
		}
	}

	return {
		magic: 'glTF',
		version,
		declaredLength,
		actualLength: buffer.length,
		chunks,
		meshes: (json.meshes || []).length,
		primitives,
		triangles,
	};
}

const MODEL_PARSE = parseGlb(MODEL_BYTES);

async function previewAvailable() {
	try {
		const response = await fetch(
			`${BASE_URL}/docs/previews/utopia-sde-dov-en-preview.html`,
			{ signal: AbortSignal.timeout(4000) }
		);
		return response.ok;
	} catch {
		return false;
	}
}

async function ensurePreviewServer() {
	if (await previewAvailable()) {
		return { startedByQa: false, process: null };
	}
	const url = new URL(BASE_URL);
	if (!['127.0.0.1', 'localhost'].includes(url.hostname)) {
		throw new Error(
			`Preview server is unavailable and is not local: ${BASE_URL}`
		);
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
		if (await previewAvailable()) {
			return { startedByQa: true, process: serverProcess };
		}
		await new Promise((resolve) => setTimeout(resolve, 250));
	}
	serverProcess.kill();
	throw new Error(`Could not start preview server at ${BASE_URL}`);
}

async function waitForModel(page) {
	await page.waitForFunction(
		() => Boolean(customElements.get('model-viewer')),
		null,
		{ timeout: 30000 }
	);
	// Routing is enabled so first-party writes can be blocked. That can delay the
	// external custom-element definition; scroll the upgraded element itself
	// only after the definition exists so model-viewer's lazy loader observes it.
	await page.locator('#utopia-model-viewer').scrollIntoViewIfNeeded();
	await page.waitForFunction(
		() => {
			const model = document.querySelector('#utopia-model-viewer');
			return Boolean(model && model.loaded === true);
		},
		null,
		{ timeout: 45000 }
	);
	await page.waitForTimeout(400);
}

async function waitForGallery(page) {
	const galleryImages = page.locator('.utopia-media-gallery img');
	const count = await galleryImages.count();
	for (let index = 0; index < count; index += 1) {
		await galleryImages.nth(index).scrollIntoViewIfNeeded();
	}
	await page.waitForFunction(
		() => {
			const images = [
				...document.querySelectorAll('.utopia-media-gallery img'),
			];
			return (
				images.length === 4 &&
				images.every(
					(image) =>
						image.complete &&
						image.naturalWidth > 0 &&
						image.naturalHeight > 0
				)
			);
		},
		null,
		{ timeout: 30000 }
	);
}

async function inspectInitial(page) {
	return page.evaluate(
		({ expectedHreflang, expectedSwitches }) => {
			const root = document.querySelector('#utopia-showroom');
			const model = document.querySelector('#utopia-model-viewer');
			const modelRect = model?.getBoundingClientRect() || null;
			const hreflangEntries = [
				...document.querySelectorAll(
					'head link[rel="alternate"][hreflang]'
				),
			].map((link) => ({
				lang: link.getAttribute('hreflang'),
				href: link.href,
			}));
			const hreflangMap = Object.fromEntries(
				hreflangEntries.map(({ lang, href }) => [lang, href])
			);
			const languageLinks = [
				...document.querySelectorAll(
					'#utopia-showroom .utopia-languages a[hreflang]'
				),
			].map((link) => ({
				lang: link.getAttribute('hreflang'),
				href: link.getAttribute('href'),
				resolvedHref: link.href,
				current: link.getAttribute('aria-current'),
			}));
			const payload = JSON.parse(
				document.querySelector('#utopia-showroom-data')?.textContent ||
					'{}'
			);
			const galleries = [
				...document.querySelectorAll('.utopia-media-gallery img'),
			].map((image) => ({
				src: image.currentSrc || image.src,
				complete: image.complete,
				naturalWidth: image.naturalWidth,
				naturalHeight: image.naturalHeight,
			}));
			const visible = (element) => {
				if (!element) return false;
				const rect = element.getBoundingClientRect();
				const style = getComputedStyle(element);
				return (
					rect.width > 0 &&
					rect.height > 0 &&
					style.display !== 'none' &&
					style.visibility !== 'hidden'
				);
			};
			const legacySelectors = [
				'.nl-hot',
				'[slot^="hotspot-unit-"]',
				'[data-act="select"][data-id]',
				'.nl-view-cone',
				'.nlpjx-view-cone',
				'[data-view-cone]',
			];
			const width = document.documentElement.clientWidth;
			const overflows = [...document.querySelectorAll('body *')]
				.map((element) => {
					const rect = element.getBoundingClientRect();
					return {
						tag: element.tagName.toLowerCase(),
						id: element.id || '',
						className: String(element.className || '').slice(0, 100),
						left: Math.round(rect.left),
						right: Math.round(rect.right),
						width: Math.round(rect.width),
					};
				})
				.filter(
					(item) =>
						item.width > 0 &&
						(item.right > width + 1 || item.left < -1)
				)
				.slice(0, 20);

			return {
				url: location.href,
				statusReady: document.readyState,
				viewport: {
					innerWidth,
					innerHeight,
					clientWidth: width,
					scrollWidth: document.documentElement.scrollWidth,
					overflow:
						document.documentElement.scrollWidth -
						document.documentElement.clientWidth,
				},
				htmlLang: document.documentElement.lang,
				htmlDir: document.documentElement.dir,
				rootLang: root?.getAttribute('lang') || null,
				rootDir: root?.getAttribute('dir') || null,
				rootDirection: root ? getComputedStyle(root).direction : null,
				rootCount: document.querySelectorAll('#utopia-showroom').length,
				sharedRootCount: document.querySelectorAll('#nl-root').length,
				nadlanShowroomGlobal: typeof window.NADLAN_SHOWROOM,
				nlpjxMapGlobal: typeof window.NLPJX_MAP,
				h1Count: document.querySelectorAll('h1').length,
				h1Text:
					document.querySelector('h1')?.textContent
						.replace(/\s+/g, ' ')
						.trim() || '',
				canonicalEntries: [
					...document.querySelectorAll('head link[rel="canonical"]'),
				].map((link) => link.href),
				hreflangEntries,
				hreflangMap,
				expectedHreflang,
				languageLinks,
				expectedSwitches,
				currentLanguageLinks: languageLinks.filter(
					(link) => link.current === 'page'
				).length,
				buildingHotspots: document.querySelectorAll(
					'#utopia-showroom .utopia-model-hotspot[data-building]'
				).length,
				buildingButtons: document.querySelectorAll(
					'#utopia-showroom [data-utopia-building]'
				).length,
				planCards: document.querySelectorAll(
					'#utopia-showroom [data-plan-card]'
				).length,
				references: document.querySelectorAll(
					'#utopia-showroom [data-utopia-reference]'
				).length,
				legacyApartmentUi: Object.fromEntries(
					legacySelectors.map((selector) => [
						selector,
						document.querySelectorAll(
							`#utopia-showroom ${selector}`
						).length,
					])
				),
				legacyApartmentTotal: legacySelectors.reduce(
					(sum, selector) =>
						sum +
						document.querySelectorAll(
							`#utopia-showroom ${selector}`
						).length,
					0
				),
				payload: {
					lang: payload.lang,
					rtl: payload.rtl,
					modelTriangles: payload.project?.model_triangles,
					modelUrl: payload.project?.model_url,
					mapToken: payload.map?.token,
					plans: payload.sample_plans?.length,
					references: (payload.sample_plans || []).reduce(
						(sum, plan) =>
							sum + (plan.references || []).length,
						0
					),
				},
				model: {
					count: document.querySelectorAll(
						'#utopia-model-viewer'
					).length,
					src: model?.getAttribute('src') || null,
					loaded: Boolean(model?.loaded),
					visible: visible(model),
					hidden: Boolean(model?.hidden),
					box: modelRect
						? {
								width: Math.round(modelRect.width),
								height: Math.round(modelRect.height),
							}
						: null,
				},
				galleryImages: galleries,
				overflows,
			};
		},
		{
			expectedHreflang: EXPECTED_HREFLANG,
			expectedSwitches: Object.fromEntries(
				Object.entries(LANGUAGE_CONFIG).map(([lang, config]) => [
					lang,
					config.switchPath,
				])
			),
		}
	);
}

async function auditMobileControls(page, stateName) {
	return page.evaluate((state) => {
		const root = document.querySelector('#utopia-showroom');
		if (!root) return { state, controls: [], undersized: [] };
		const selectors =
			'a[href],button,input,select,textarea,[role="button"],[tabindex]:not([tabindex="-1"])';
		const controls = [...root.querySelectorAll(selectors)]
			.filter((element, index, list) => list.indexOf(element) === index)
			.filter((element) => {
				const rect = element.getBoundingClientRect();
				const style = getComputedStyle(element);
				return (
					rect.width > 0 &&
					rect.height > 0 &&
					style.display !== 'none' &&
					style.visibility !== 'hidden' &&
					!element.closest('[hidden]')
				);
			})
			.map((element) => {
				const rect = element.getBoundingClientRect();
				return {
					tag: element.tagName.toLowerCase(),
					id: element.id || '',
					className: String(element.className || '').slice(0, 100),
					label:
						element.getAttribute('aria-label') ||
						element.getAttribute('placeholder') ||
						element.textContent.replace(/\s+/g, ' ').trim().slice(0, 100),
					width: Number(rect.width.toFixed(2)),
					height: Number(rect.height.toFixed(2)),
					disabled: Boolean(element.disabled),
				};
			});
		return {
			state,
			controls,
			undersized: controls.filter(
				(control) => control.width < 43.5 || control.height < 43.5
			),
		};
	}, stateName);
}

async function inspectBuildingState(page, id) {
	return page.evaluate((buildingId) => {
		const root = document.querySelector('#utopia-showroom');
		const model = document.querySelector('#utopia-model-viewer');
		const selectedButton = root?.querySelector(
			`[data-utopia-building="${buildingId}"]`
		);
		const selectedHotspot = root?.querySelector(
			`.utopia-model-hotspot[data-building="${buildingId}"]`
		);
		return {
			activeBuildingButtons: root?.querySelectorAll(
				'[data-utopia-building].is-active'
			).length,
			activeBuildingHotspots: root?.querySelectorAll(
				'.utopia-model-hotspot.is-active'
			).length,
			buttonActive: Boolean(selectedButton?.classList.contains('is-active')),
			buttonPressed: selectedButton?.getAttribute('aria-pressed'),
			hotspotActive: Boolean(
				selectedHotspot?.classList.contains('is-active')
			),
			hotspotPressed: selectedHotspot?.getAttribute('aria-pressed'),
			panelTitle:
				root
					?.querySelector('#utopia-building-title')
					?.textContent.replace(/\s+/g, ' ')
					.trim() || '',
			metricsVisible: !root?.querySelector(
				'#utopia-building-metrics'
			)?.hidden,
			sourceVisible: !root?.querySelector(
				'#utopia-building-source'
			)?.hidden,
			cameraTarget: String(model?.cameraTarget || ''),
			cameraOrbit: String(model?.cameraOrbit || ''),
		};
	}, id);
}

async function exerciseInteractions(page, testCase) {
	const interactions = {
		concept: null,
		model: null,
		building: null,
		cinematic: null,
		reset: null,
		reference: null,
		dialog: null,
		fullscreen: null,
		mapFallback: null,
		languageSwitch: null,
		mobileControlAudits: [],
	};
	const root = page.locator('#utopia-showroom');

	if (testCase.viewport.isMobile) {
		interactions.mobileControlAudits.push(
			await auditMobileControls(page, 'initial')
		);
	}

	await page
		.locator('[data-utopia-view="concept"]')
		.scrollIntoViewIfNeeded();
	await page.locator('[data-utopia-view="concept"]').click();
	await page.waitForTimeout(120);
	interactions.concept = await page.evaluate(() => {
		const model = document.querySelector('#utopia-model-viewer');
		const frame = document.querySelector('.utopia-concept-frame');
		const image = frame?.querySelector('img');
		return {
			modelHidden: Boolean(model?.hidden),
			frameHidden: Boolean(frame?.hidden),
			frameVisible:
				Boolean(frame) &&
				frame.getBoundingClientRect().width > 0 &&
				frame.getBoundingClientRect().height > 0,
			imageLoaded: Boolean(image?.complete && image?.naturalWidth === 1536),
			activeConceptButtons: document.querySelectorAll(
				'#utopia-showroom [data-utopia-view="concept"].is-active'
			).length,
		};
	});

	await page.locator('[data-utopia-view="model"]').click();
	await page.waitForTimeout(120);
	interactions.model = await page.evaluate(() => {
		const model = document.querySelector('#utopia-model-viewer');
		const frame = document.querySelector('.utopia-concept-frame');
		return {
			modelHidden: Boolean(model?.hidden),
			frameHidden: Boolean(frame?.hidden),
			activeModelButtons: document.querySelectorAll(
				'#utopia-showroom [data-utopia-view="model"].is-active'
			).length,
		};
	});

	await page
		.locator('[data-utopia-building="n1"]')
		.scrollIntoViewIfNeeded();
	await page.locator('[data-utopia-building="n1"]').click();
	await page.waitForTimeout(650);
	interactions.building = await inspectBuildingState(page, 'n1');

	await page.locator('[data-utopia-action="reset"]').click();
	await page.waitForTimeout(150);
	const resetCamera = await page.evaluate(() => {
		const model = document.querySelector('#utopia-model-viewer');
		return {
			cameraTarget: String(model?.cameraTarget || ''),
			cameraOrbit: String(model?.cameraOrbit || ''),
		};
	});
	await page.locator('[data-utopia-action="cinematic"]').click();
	await page.waitForTimeout(180);
	interactions.cinematic = {
		...(await inspectBuildingState(page, 's1')),
		cameraBefore: resetCamera,
	};

	await page.locator('[data-utopia-action="reset"]').click();
	await page.waitForTimeout(180);
	interactions.reset = await page.evaluate(() => {
		const root = document.querySelector('#utopia-showroom');
		const model = document.querySelector('#utopia-model-viewer');
		return {
			activeBuildingButtons: root?.querySelectorAll(
				'[data-utopia-building].is-active'
			).length,
			activeBuildingHotspots: root?.querySelectorAll(
				'.utopia-model-hotspot.is-active'
			).length,
			metricsHidden: Boolean(
				root?.querySelector('#utopia-building-metrics')?.hidden
			),
			sourceHidden: Boolean(
				root?.querySelector('#utopia-building-source')?.hidden
			),
			cameraTarget: String(model?.cameraTarget || ''),
			cameraOrbit: String(model?.cameraOrbit || ''),
		};
	});

	const reference = page.locator(
		'[data-utopia-reference="n1-5e-40"]'
	);
	await reference.scrollIntoViewIfNeeded();
	await reference.click();
	await page.waitForTimeout(650);
	interactions.reference = await page.evaluate(() => {
		const root = document.querySelector('#utopia-showroom');
		const payload = JSON.parse(
			root?.querySelector('#utopia-showroom-data')?.textContent || '{}'
		);
		const plan = payload.sample_plans?.find(
			(candidate) => candidate.id === 'n1-5e'
		);
		const expected =
			`${payload.copy?.selected_prefix || ''} ` +
			`${String(plan?.building || '').toUpperCase()} ${plan?.type || ''} · ` +
			`${payload.copy?.floor || ''} 9 · ` +
			`${payload.copy?.apartment || ''} 40`;
		const actual =
			root
				?.querySelector('[data-utopia-form-context]')
				?.textContent.replace(/\s+/g, ' ')
				.trim() || '';
		return {
			activeReferences: root?.querySelectorAll(
				'[data-utopia-reference].is-active'
			).length,
			activeReferenceId: root
				?.querySelector('[data-utopia-reference].is-active')
				?.getAttribute('data-utopia-reference'),
			selectedPlanCards: root?.querySelectorAll(
				'[data-plan-card].is-selected'
			).length,
			selectedPlanId: root
				?.querySelector('[data-plan-card].is-selected')
				?.getAttribute('data-plan-card'),
			activeBuildingId: root
				?.querySelector('[data-utopia-building].is-active')
				?.getAttribute('data-utopia-building'),
			formContext: actual,
			expectedFormContext: expected.replace(/\s+/g, ' ').trim(),
			legacyApartmentHotspots: root?.querySelectorAll(
				'.nl-hot,[slot^="hotspot-unit-"],[data-act="select"][data-id]'
			).length,
			viewCones: root?.querySelectorAll(
				'.nl-view-cone,.nlpjx-view-cone,[data-view-cone]'
			).length,
		};
	});

	if (testCase.viewport.isMobile) {
		interactions.mobileControlAudits.push(
			await auditMobileControls(page, 'reference-selected')
		);
	}

	const planButton = page.locator('[data-utopia-plan="n1-5e"]');
	await planButton.scrollIntoViewIfNeeded();
	await planButton.click();
	await page.waitForFunction(
		() => Boolean(document.querySelector('#utopia-plan-dialog')?.open),
		null,
		{ timeout: 5000 }
	);
	await page.waitForTimeout(100);
	interactions.dialog = await page.evaluate(() => {
		const dialog = document.querySelector('#utopia-plan-dialog');
		const frame = dialog?.querySelector('iframe');
		const fallback = dialog?.querySelector(
			'.utopia-plan-dialog__fallback a'
		);
		return {
			open: Boolean(dialog?.open),
			frameSrc: frame?.src || '',
			fallbackHref: fallback?.href || '',
			title:
				dialog
					?.querySelector('[data-plan-dialog-title]')
					?.textContent.replace(/\s+/g, ' ')
					.trim() || '',
		};
	});
	if (testCase.viewport.isMobile) {
		interactions.mobileControlAudits.push(
			await auditMobileControls(page, 'plan-dialog-open')
		);
	}
	await page.locator('[data-utopia-dialog-close]').click();
	await page.waitForFunction(
		() => !document.querySelector('#utopia-plan-dialog')?.open,
		null,
		{ timeout: 5000 }
	);

	const fullScreenButton = page.locator(
		'[data-utopia-action="fullscreen"]'
	);
	await fullScreenButton.scrollIntoViewIfNeeded();
	await fullScreenButton.click();
	await page.waitForFunction(
		() => {
			const root = document.querySelector('#utopia-showroom');
			return Boolean(
				document.fullscreenElement === root ||
					root?.classList.contains('is-fallback-fullscreen')
			);
		},
		null,
		{ timeout: 5000 }
	);
	// Native Chrome updates fullscreenElement immediately and dispatches the
	// fullscreenchange handler on the following task. Sample only after the
	// buyer-visible label/lock state has caught up; retain the assertion below
	// as the actual gate if that synchronization does not occur.
	await page
		.waitForFunction(
			() => {
				const root = document.querySelector('#utopia-showroom');
				const button = root?.querySelector(
					'[data-utopia-action="fullscreen"]'
				);
				return Boolean(
					document.body.classList.contains('utopia-body-locked') &&
						button?.getAttribute('aria-pressed') === 'true' &&
						button.textContent.replace(/\s+/g, ' ').trim() ===
							button.getAttribute('data-label-exit')
				);
			},
			null,
			{ timeout: 2000 }
		)
		.catch(() => {});
	interactions.fullscreen = await page.evaluate(() => {
		const root = document.querySelector('#utopia-showroom');
		const button = root?.querySelector(
			'[data-utopia-action="fullscreen"]'
		);
		return {
			native: document.fullscreenElement === root,
			fallback: Boolean(
				root?.classList.contains('is-fallback-fullscreen')
			),
			bodyLocked: document.body.classList.contains('utopia-body-locked'),
			buttonPressed: button?.getAttribute('aria-pressed'),
			enterLabel: button?.getAttribute('data-label-enter'),
			exitLabel: button?.getAttribute('data-label-exit'),
			currentLabel: button?.textContent.replace(/\s+/g, ' ').trim(),
		};
	});
	await fullScreenButton.click();
	await page.waitForFunction(
		() => {
			const root = document.querySelector('#utopia-showroom');
			return (
				document.fullscreenElement !== root &&
				!root?.classList.contains('is-fallback-fullscreen')
			);
		},
		null,
		{ timeout: 5000 }
	);
	interactions.fullscreen.exited = await page.evaluate(() => {
		const root = document.querySelector('#utopia-showroom');
		const button = root?.querySelector(
			'[data-utopia-action="fullscreen"]'
		);
		return {
			native: document.fullscreenElement === root,
			fallback: Boolean(
				root?.classList.contains('is-fallback-fullscreen')
			),
			bodyLocked: document.body.classList.contains('utopia-body-locked'),
			buttonPressed: button?.getAttribute('aria-pressed'),
			currentLabel: button?.textContent.replace(/\s+/g, ' ').trim(),
		};
	});

	await page.locator('#utopia-map-section').scrollIntoViewIfNeeded();
	await page.waitForFunction(
		() => {
			const host = document.querySelector('#utopia-context-map');
			const fallback = document.querySelector('.utopia-map-fallback');
			return Boolean(host?.hidden && fallback && !fallback.hidden);
		},
		null,
		{ timeout: 5000 }
	);
	interactions.mapFallback = await page.evaluate(() => {
		const root = document.querySelector('#utopia-showroom');
		const payload = JSON.parse(
			root?.querySelector('#utopia-showroom-data')?.textContent || '{}'
		);
		const fallback = root?.querySelector('.utopia-map-fallback');
		return {
			token: payload.map?.token,
			hostHidden: Boolean(
				root?.querySelector('#utopia-context-map')?.hidden
			),
			fallbackVisible: Boolean(
				fallback &&
					!fallback.hidden &&
					fallback.getBoundingClientRect().height > 0
			),
			mapCanvases: root?.querySelectorAll(
				'#utopia-context-map canvas'
			).length,
			mapboxMaps: root?.querySelectorAll('.mapboxgl-map').length,
			nadlanShowroomGlobal: typeof window.NADLAN_SHOWROOM,
			nlpjxMapGlobal: typeof window.NLPJX_MAP,
		};
	});
	if (testCase.viewport.isMobile) {
		interactions.mobileControlAudits.push(
			await auditMobileControls(page, 'map-fallback')
		);
	}

	await root.scrollIntoViewIfNeeded();
	const nextIndex =
		(LANGUAGE_ORDER.indexOf(testCase.lang) + 1) % LANGUAGE_ORDER.length;
	const nextLang = LANGUAGE_ORDER[nextIndex];
	const nextConfig = LANGUAGE_CONFIG[nextLang];
	const switchLink = page.locator(
		`#utopia-showroom .utopia-languages a[hreflang="${nextLang}"]`
	);
	const switchHref = await switchLink.getAttribute('href');
	const [navigationResponse] = await Promise.all([
		page.waitForNavigation({
			waitUntil: 'domcontentloaded',
			timeout: 15000,
		}),
		switchLink.click(),
	]);
	await page.waitForSelector('#utopia-showroom', { timeout: 10000 });
	interactions.languageSwitch = await page.evaluate(
		({ targetLang, targetHtmlLang, targetDir }) => {
			const root = document.querySelector('#utopia-showroom');
			return {
				url: location.href,
				htmlLang: document.documentElement.lang,
				htmlDir: document.documentElement.dir,
				rootLang: root?.getAttribute('lang'),
				rootDir: root?.getAttribute('dir'),
				targetLang,
				targetHtmlLang,
				targetDir,
			};
		},
		{
			targetLang: nextLang,
			targetHtmlLang: nextConfig.htmlLang,
			targetDir: nextConfig.dir,
		}
	);
	interactions.languageSwitch.clickedHref = switchHref;
	interactions.languageSwitch.status = navigationResponse?.status() || null;
	interactions.languageSwitch.expectedPath = nextConfig.switchPath;

	return interactions;
}

function buildAssertions(testCase, initial, interactions, events) {
	const expected = LANGUAGE_CONFIG[testCase.lang];
	const assertions = [];
	const add = (...args) => assertions.push(assertion(...args));

	add(
		'viewport is exact',
		[initial.viewport.innerWidth, initial.viewport.innerHeight],
		[testCase.viewport.width, testCase.viewport.height],
		initial.viewport.innerWidth === testCase.viewport.width &&
			initial.viewport.innerHeight === testCase.viewport.height
	);
	add('one UTOPIA root', initial.rootCount, 1);
	add('one H1', initial.h1Count, 1);
	add(
		'H1 starts with UTOPIA',
		initial.h1Text,
		'UTOPIA…',
		/^UTOPIA\b/u.test(initial.h1Text)
	);
	add('correct html language', initial.htmlLang, expected.htmlLang);
	add('correct html direction', initial.htmlDir, expected.dir);
	add('correct showroom language', initial.rootLang, expected.rootLang);
	add('correct showroom direction', initial.rootDir, expected.dir);
	add('computed showroom direction', initial.rootDirection, expected.dir);
	add(
		'exactly one canonical',
		initial.canonicalEntries.length,
		1
	);
	add(
		'correct canonical',
		initial.canonicalEntries[0] || null,
		expected.canonical
	);
	add(
		'exactly six head hreflang entries',
		initial.hreflangEntries.length,
		6
	);
	add(
		'exact hreflang map',
		initial.hreflangMap,
		EXPECTED_HREFLANG,
		JSON.stringify(initial.hreflangMap) ===
			JSON.stringify(EXPECTED_HREFLANG)
	);
	add(
		'five local language links',
		initial.languageLinks.length,
		5
	);
	add(
		'language links use expected local preview paths',
		Object.fromEntries(
			initial.languageLinks.map((link) => [link.lang, link.href])
		),
		initial.expectedSwitches,
		JSON.stringify(
			Object.fromEntries(
				initial.languageLinks.map((link) => [link.lang, link.href])
			)
		) === JSON.stringify(initial.expectedSwitches)
	);
	add(
		'one current language link',
		initial.currentLanguageLinks,
		1
	);
	add('four building hotspots', initial.buildingHotspots, 4);
	add('four building buttons', initial.buildingButtons, 4);
	add('seven plan cards', initial.planCards, 7);
	add('29 plan references', initial.references, 29);
	add('payload has seven plans', initial.payload.plans, 7);
	add('payload has 29 references', initial.payload.references, 29);
	add(
		'payload declares 21,416 triangles',
		initial.payload.modelTriangles,
		EXPECTED_TRIANGLES
	);
	add(
		'GLB parses to exactly 21,416 triangles',
		MODEL_PARSE.triangles,
		EXPECTED_TRIANGLES
	);
	add(
		'GLB SHA-256 is the reviewed asset',
		MODEL_SHA256,
		EXPECTED_MODEL_SHA256
	);
	add('no #nl-root', initial.sharedRootCount, 0);
	add(
		'no NADLAN_SHOWROOM global',
		initial.nadlanShowroomGlobal,
		'undefined'
	);
	add('no NLPJX_MAP global', initial.nlpjxMapGlobal, 'undefined');
	add('no legacy apartment UI', initial.legacyApartmentTotal, 0);
	add('no horizontal overflow', initial.viewport.overflow, 0);
	add('one isolated model viewer', initial.model.count, 1);
	add('correct model URL', initial.model.src, MODEL_URL_PATH);
	add('GLB loaded in Chrome', initial.model.loaded, true);
	add('model is visible', initial.model.visible, true);
	add('model is not hidden', initial.model.hidden, false);
	add(
		'model has useful rendered dimensions',
		initial.model.box,
		'>= 280x240',
		Boolean(
			initial.model.box?.width >= 280 &&
				initial.model.box?.height >= 240
		)
	);
	add(
		'GLB requested in Chrome',
		events.glbRequests,
		'>= 1',
		events.glbRequests >= 1
	);
	add(
		'four gallery images',
		initial.galleryImages.length,
		4
	);
	add(
		'all gallery images are 1536px wide',
		initial.galleryImages.map((image) => image.naturalWidth),
		[1536, 1536, 1536, 1536],
		initial.galleryImages.length === 4 &&
			initial.galleryImages.every(
				(image) => image.complete && image.naturalWidth === 1536
			)
	);

	add('concept hides model', interactions.concept.modelHidden, true);
	add('concept frame displays', interactions.concept.frameVisible, true);
	add(
		'concept image is the 1536px asset',
		interactions.concept.imageLoaded,
		true
	);
	add(
		'one active concept button',
		interactions.concept.activeConceptButtons,
		1
	);
	add('model view restores model', interactions.model.modelHidden, false);
	add(
		'model view hides concept frame',
		interactions.model.frameHidden,
		true
	);
	add(
		'one active model button',
		interactions.model.activeModelButtons,
		1
	);

	add(
		'building click activates one button',
		interactions.building.activeBuildingButtons,
		1
	);
	add(
		'building click activates one hotspot',
		interactions.building.activeBuildingHotspots,
		1
	);
	add('N1 building button active', interactions.building.buttonActive, true);
	add(
		'N1 building hotspot active',
		interactions.building.hotspotActive,
		true
	);
	add(
		'building metrics display',
		interactions.building.metricsVisible,
		true
	);
	add(
		'building source displays',
		interactions.building.sourceVisible,
		true
	);
	add(
		'cinematic selects S1',
		interactions.cinematic.buttonActive &&
			interactions.cinematic.hotspotActive,
		true
	);
	add(
		'cinematic changes camera from reset',
		{
			before: interactions.cinematic.cameraBefore,
			after: {
				target: interactions.cinematic.cameraTarget,
				orbit: interactions.cinematic.cameraOrbit,
			},
		},
		'camera state changes',
		interactions.cinematic.cameraTarget !==
				interactions.cinematic.cameraBefore.cameraTarget ||
			interactions.cinematic.cameraOrbit !==
				interactions.cinematic.cameraBefore.cameraOrbit
	);
	add(
		'reset clears active building buttons',
		interactions.reset.activeBuildingButtons,
		0
	);
	add(
		'reset clears active model hotspots',
		interactions.reset.activeBuildingHotspots,
		0
	);
	add('reset hides metrics', interactions.reset.metricsHidden, true);
	add('reset hides source', interactions.reset.sourceHidden, true);

	add(
		'n1-5e-40 is sole active reference',
		{
			count: interactions.reference.activeReferences,
			id: interactions.reference.activeReferenceId,
		},
		{ count: 1, id: 'n1-5e-40' },
		interactions.reference.activeReferences === 1 &&
			interactions.reference.activeReferenceId === 'n1-5e-40'
	);
	add(
		'n1-5e plan card is selected',
		{
			count: interactions.reference.selectedPlanCards,
			id: interactions.reference.selectedPlanId,
		},
		{ count: 1, id: 'n1-5e' },
		interactions.reference.selectedPlanCards === 1 &&
			interactions.reference.selectedPlanId === 'n1-5e'
	);
	add(
		'reference selects N1 building',
		interactions.reference.activeBuildingId,
		'n1'
	);
	add(
		'localized form context is exact',
		interactions.reference.formContext,
		interactions.reference.expectedFormContext
	);
	add(
		'selection creates no legacy apartment hotspots',
		interactions.reference.legacyApartmentHotspots,
		0
	);
	add(
		'selection creates no view cones',
		interactions.reference.viewCones,
		0
	);

	add('official plan dialog opens', interactions.dialog.open, true);
	add(
		'official PDF iframe has expected URL',
		plainUrl(interactions.dialog.frameSrc),
		EXPECTED_PLAN_URL
	);
	add(
		'official PDF fallback has expected URL',
		plainUrl(interactions.dialog.fallbackHref),
		EXPECTED_PLAN_URL
	);
	add('plan dialog title is N1 5E / C5', interactions.dialog.title, 'N1 5E / C5');

	add(
		'fullscreen enters native or isolated fallback mode',
		interactions.fullscreen.native || interactions.fullscreen.fallback,
		true
	);
	add(
		'fullscreen locks body',
		interactions.fullscreen.bodyLocked,
		true
	);
	add(
		'fullscreen button is pressed',
		interactions.fullscreen.buttonPressed,
		'true'
	);
	add(
		'fullscreen uses exit label',
		interactions.fullscreen.currentLabel,
		interactions.fullscreen.exitLabel
	);
	add(
		'fullscreen exits',
		{
			native: interactions.fullscreen.exited.native,
			fallback: interactions.fullscreen.exited.fallback,
			bodyLocked: interactions.fullscreen.exited.bodyLocked,
		},
		{ native: false, fallback: false, bodyLocked: false },
		!interactions.fullscreen.exited.native &&
			!interactions.fullscreen.exited.fallback &&
			!interactions.fullscreen.exited.bodyLocked
	);
	add(
		'fullscreen restores enter label',
		interactions.fullscreen.exited.currentLabel,
		interactions.fullscreen.enterLabel
	);

	add('map token is empty', interactions.mapFallback.token, '');
	add(
		'empty-token map host is hidden',
		interactions.mapFallback.hostHidden,
		true
	);
	add(
		'empty-token map fallback is visible',
		interactions.mapFallback.fallbackVisible,
		true
	);
	add(
		'map fallback creates no canvas',
		interactions.mapFallback.mapCanvases,
		0
	);
	add(
		'map fallback creates no Mapbox map',
		interactions.mapFallback.mapboxMaps,
		0
	);
	add(
		'map fallback does not create shared globals',
		[
			interactions.mapFallback.nadlanShowroomGlobal,
			interactions.mapFallback.nlpjxMapGlobal,
		],
		['undefined', 'undefined'],
		interactions.mapFallback.nadlanShowroomGlobal === 'undefined' &&
			interactions.mapFallback.nlpjxMapGlobal === 'undefined'
	);

	add(
		'language switch request succeeds',
		interactions.languageSwitch.status,
		200
	);
	add(
		'language switch clicked expected local path',
		interactions.languageSwitch.clickedHref,
		interactions.languageSwitch.expectedPath
	);
	add(
		'language switch reaches expected path',
		new URL(interactions.languageSwitch.url).pathname,
		interactions.languageSwitch.expectedPath
	);
	add(
		'language switch updates html language',
		interactions.languageSwitch.htmlLang,
		interactions.languageSwitch.targetHtmlLang
	);
	add(
		'language switch updates showroom language',
		interactions.languageSwitch.rootLang,
		interactions.languageSwitch.targetLang
	);
	add(
		'language switch updates direction',
		[
			interactions.languageSwitch.htmlDir,
			interactions.languageSwitch.rootDir,
		],
		[
			interactions.languageSwitch.targetDir,
			interactions.languageSwitch.targetDir,
		],
		interactions.languageSwitch.htmlDir ===
				interactions.languageSwitch.targetDir &&
			interactions.languageSwitch.rootDir ===
				interactions.languageSwitch.targetDir
	);

	if (testCase.viewport.isMobile) {
		const undersized = interactions.mobileControlAudits.flatMap((audit) =>
			audit.undersized.map((control) => ({
				state: audit.state,
				...control,
			}))
		);
		add(
			'all visible UTOPIA mobile controls are at least 44x44',
			undersized,
			[],
			undersized.length === 0
		);
	}

	const unclassifiedConsoleErrors = events.consoleErrors.filter(
		(event) => event.classification === 'failure'
	);
	const unclassifiedPageErrors = events.pageErrors.filter(
		(event) => event.classification === 'failure'
	);
	const unclassifiedRequestFailures = events.requestFailures.filter(
		(event) => event.classification === 'failure'
	);
	const firstPartyHttpErrors = events.httpErrors.filter(
		(event) => event.firstParty
	);
	const unclassifiedHttpErrors = events.httpErrors.filter(
		(event) => event.classification === 'failure'
	);
	add(
		'no first-party non-GET requests',
		events.firstPartyNonGet,
		[],
		events.firstPartyNonGet.length === 0
	);
	add(
		'no first-party HTTP errors',
		firstPartyHttpErrors,
		[],
		firstPartyHttpErrors.length === 0
	);
	add(
		'no unclassified HTTP errors',
		unclassifiedHttpErrors,
		[],
		unclassifiedHttpErrors.length === 0
	);
	add(
		'no unclassified console errors',
		unclassifiedConsoleErrors,
		[],
		unclassifiedConsoleErrors.length === 0
	);
	add(
		'no page errors',
		unclassifiedPageErrors,
		[],
		unclassifiedPageErrors.length === 0
	);
	add(
		'no unclassified request failures',
		unclassifiedRequestFailures,
		[],
		unclassifiedRequestFailures.length === 0
	);

	return assertions;
}

async function runCase(browser, testCase) {
	const config = LANGUAGE_CONFIG[testCase.lang];
	const context = await browser.newContext({
		viewport: {
			width: testCase.viewport.width,
			height: testCase.viewport.height,
		},
		screen: {
			width: testCase.viewport.width,
			height: testCase.viewport.height,
		},
		deviceScaleFactor: 1,
		isMobile: testCase.viewport.isMobile,
		hasTouch: testCase.viewport.hasTouch,
		locale: config.locale,
		colorScheme: 'light',
		reducedMotion: 'reduce',
	});
	const page = await context.newPage();
	const events = {
		consoleErrors: [],
		pageErrors: [],
		requestFailures: [],
		httpErrors: [],
		firstPartyNonGet: [],
		glbRequests: 0,
		previewShellFaviconStubs: 0,
	};

	await page.route('**/*', async (route) => {
		const request = route.request();
		const url = request.url();
		const method = request.method().toUpperCase();
		if (isFirstParty(url) && method !== 'GET') {
			events.firstPartyNonGet.push({
				method,
				url,
				resourceType: request.resourceType(),
				action: 'blockedbyclient',
			});
			await route.abort('blockedbyclient');
			return;
		}
		if (
			isFirstParty(url) &&
			new URL(url).pathname === MODEL_URL_PATH
		) {
			events.glbRequests += 1;
			// Let the local preview server return the reviewed file itself.
			// MODEL_BYTES are parsed and hashed independently above.
			await route.continue();
			return;
		}
		if (
			isFirstParty(url) &&
			new URL(url).pathname === '/favicon.ico'
		) {
			// The minimal static preview shell has no theme favicon markup.
			// Chrome requests /favicon.ico implicitly, so keep that shell-only
			// request from obscuring actual page network failures.
			events.previewShellFaviconStubs += 1;
			await route.fulfill({ status: 204, body: '' });
			return;
		}
		await route.continue();
	});

	page.on('console', (message) => {
		if (message.type() !== 'error') return;
		const location = message.location();
		const event = {
			text: normalizeText(message.text()),
			url: location.url || '',
			line: location.lineNumber,
			column: location.columnNumber,
			classification: 'failure',
		};
		if (isExpectedThirdPartyWarning(event.url, event.text)) {
			event.classification = 'classified-third-party-warning';
		}
		events.consoleErrors.push(event);
	});
	page.on('pageerror', (error) => {
		events.pageErrors.push({
			text: normalizeText(error.message),
			stack: normalizeText(error.stack),
			classification: 'failure',
		});
	});
	page.on('requestfailed', (request) => {
		const url = request.url();
		events.requestFailures.push({
			url,
			method: request.method(),
			resourceType: request.resourceType(),
			error: request.failure()?.errorText || 'unknown request failure',
			firstParty: isFirstParty(url),
			classification: isExpectedThirdPartyWarning(
				url,
				request.failure()?.errorText
			)
				? 'classified-third-party-warning'
				: 'failure',
		});
	});
	page.on('response', (response) => {
		if (response.status() < 400) return;
		const url = response.url();
		events.httpErrors.push({
			url,
			status: response.status(),
			firstParty: isFirstParty(url),
			classification: isExpectedThirdPartyWarning(
				url,
				String(response.status())
			)
				? 'classified-third-party-warning'
				: 'failure',
		});
	});

	const previewUrl =
		`${BASE_URL}/docs/previews/utopia-sde-dov-` +
		`${testCase.lang}-preview.html`;
	const response = await page.goto(previewUrl, {
		waitUntil: 'domcontentloaded',
		timeout: 45000,
	});
	if (!response || response.status() !== 200) {
		throw new Error(
			`Preview navigation failed for ${previewUrl}: ${response?.status()}`
		);
	}
	await page.waitForSelector('#utopia-showroom', { timeout: 15000 });
	await waitForModel(page);
	await waitForGallery(page);

	const screenshotPrefix = `${testCase.lang}-${testCase.viewport.name}`;
	const topScreenshot = path.join(
		OUT_DIR,
		`${screenshotPrefix}-seo-top.png`
	);
	await page.locator('h1').scrollIntoViewIfNeeded();
	await page.screenshot({
		path: topScreenshot,
		fullPage: false,
		animations: 'disabled',
	});

	const modelScreenshot = path.join(
		OUT_DIR,
		`${screenshotPrefix}-showroom-model.png`
	);
	await page.locator('#utopia-showroom').scrollIntoViewIfNeeded();
	await page.screenshot({
		path: modelScreenshot,
		fullPage: false,
		animations: 'disabled',
	});

	const initial = await inspectInitial(page);
	const interactions = await exerciseInteractions(page, testCase);

	// Re-open the original preview for a stable selected-reference screenshot.
	await page.goto(previewUrl, {
		waitUntil: 'domcontentloaded',
		timeout: 45000,
	});
	await page.waitForSelector('#utopia-showroom', { timeout: 15000 });
	await page
		.locator('[data-utopia-reference="n1-5e-40"]')
		.scrollIntoViewIfNeeded();
	await page.locator('[data-utopia-reference="n1-5e-40"]').click();
	await page.waitForTimeout(250);
	const referenceScreenshot = path.join(
		OUT_DIR,
		`${screenshotPrefix}-reference-n1-5e-40.png`
	);
	await page.screenshot({
		path: referenceScreenshot,
		fullPage: false,
		animations: 'disabled',
	});

	const assertions = buildAssertions(
		testCase,
		initial,
		interactions,
		events
	);
	const failures = assertions
		.filter((item) => !item.pass)
		.map(({ name, actual, expected }) => ({ name, actual, expected }));
	const warnings = [
		...events.consoleErrors,
		...events.requestFailures,
		...events.httpErrors,
	].filter(
		(event) =>
			event.classification === 'classified-third-party-warning'
	);

	await context.close();
	return {
		lang: testCase.lang,
		viewport: testCase.viewport.name,
		dimensions: {
			width: testCase.viewport.width,
			height: testCase.viewport.height,
		},
		browserMode: {
			isMobile: testCase.viewport.isMobile,
			hasTouch: testCase.viewport.hasTouch,
		},
		url: previewUrl,
		pass: failures.length === 0,
		initial,
		interactions,
		events,
		assertions,
		failures,
		warnings,
		screenshots: {
			seoTop: path.relative(ROOT, topScreenshot).replaceAll('\\', '/'),
			showroomModel: path
				.relative(ROOT, modelScreenshot)
				.replaceAll('\\', '/'),
			referenceSelection: path
				.relative(ROOT, referenceScreenshot)
				.replaceAll('\\', '/'),
		},
	};
}

async function main() {
	if (!existsSync(CHROME_EXECUTABLE)) {
		throw new Error(
			`Installed Google Chrome was not found at ${CHROME_EXECUTABLE}`
		);
	}
	await mkdir(OUT_DIR, { recursive: true });
	const server = await ensurePreviewServer();
	const browser = await chromium.launch({
		channel: 'chrome',
		headless: true,
	});
	const report = {
		createdAt: new Date().toISOString(),
		command: 'node scripts/qa-utopia-preview-browser.mjs',
		baseUrl: BASE_URL,
		evidenceDirectory: path
			.relative(ROOT, OUT_DIR)
			.replaceAll('\\', '/'),
		serverStartedByQa: server.startedByQa,
		browser: {
			name: 'Google Chrome',
			channel: 'chrome',
			executablePath: CHROME_EXECUTABLE,
			version: browser.version(),
			headless: true,
			note: 'Playwright drove the installed Google Chrome channel, not bundled Chromium.',
		},
		modelAsset: {
			path: MODEL_RELATIVE_PATH,
			bytes: MODEL_BYTES.length,
			expectedSha256: EXPECTED_MODEL_SHA256,
			actualSha256: MODEL_SHA256,
			exactExpectedAsset: MODEL_SHA256 === EXPECTED_MODEL_SHA256,
			parse: MODEL_PARSE,
			expectedTriangles: EXPECTED_TRIANGLES,
			exactExpectedTriangles:
				MODEL_PARSE.triangles === EXPECTED_TRIANGLES,
		},
		networkPolicy: {
			firstPartyOrigin: BASE_ORIGIN,
			allowedFirstPartyMethods: ['GET'],
			nonGetAction: 'block and fail the case',
			classifiedThirdPartyWarningHosts: [
				'ajax.googleapis.com',
				'utopiatlv.co.il',
			],
		},
		cases: [],
		pass: false,
	};

	try {
		for (const testCase of CASES) {
			const result = await runCase(browser, testCase);
			report.cases.push(result);
			console.log(
				`${result.pass ? 'PASS' : 'FAIL'} ` +
					`${result.lang} ${result.viewport}` +
					(result.failures.length
						? ` - ${result.failures
								.map((failure) => failure.name)
								.join(', ')}`
						: '')
			);
		}
		report.pass =
			report.modelAsset.exactExpectedAsset &&
			report.modelAsset.exactExpectedTriangles &&
			report.cases.every((result) => result.pass);
		report.summary = {
			totalCases: report.cases.length,
			passedCases: report.cases.filter((result) => result.pass).length,
			failedCases: report.cases.filter((result) => !result.pass).length,
			totalAssertions: report.cases.reduce(
				(sum, result) => sum + result.assertions.length,
				0
			),
			failedAssertions: report.cases.reduce(
				(sum, result) => sum + result.failures.length,
				0
			),
			classifiedThirdPartyWarnings: report.cases.reduce(
				(sum, result) => sum + result.warnings.length,
				0
			),
			firstPartyNonGetBlocked: report.cases.reduce(
				(sum, result) =>
					sum + result.events.firstPartyNonGet.length,
				0
			),
			modelTriangles: MODEL_PARSE.triangles,
			browser: `${report.browser.name} ${report.browser.version}`,
		};
	} finally {
		await browser.close();
		if (server.process) {
			server.process.kill();
		}
	}

	const json = `${JSON.stringify(report, null, 2)}\n`;
	await writeFile(REPORT_PATH, json, 'utf8');
	await writeFile(
		path.join(OUT_DIR, 'utopia-isolated-browser-report.json'),
		json,
		'utf8'
	);
	console.log(
		JSON.stringify(
			{
				pass: report.pass,
				summary: report.summary,
				report: REPORT_PATH,
				evidence: OUT_DIR,
			},
			null,
			2
		)
	);

	if (!report.pass) {
		process.exitCode = 1;
	}
}

main().catch(async (error) => {
	const fatal = {
		createdAt: new Date().toISOString(),
		command: 'node scripts/qa-utopia-preview-browser.mjs',
		error: error.stack || error.message,
		browserRequested: {
			name: 'Google Chrome',
			channel: 'chrome',
			executablePath: CHROME_EXECUTABLE,
		},
	};
	await mkdir(OUT_DIR, { recursive: true });
	await writeFile(
		path.join(OUT_DIR, 'utopia-isolated-browser-fatal.json'),
		`${JSON.stringify(fatal, null, 2)}\n`,
		'utf8'
	);
	console.error(error);
	process.exit(1);
});
