#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { chromium } from 'playwright';

const ROOT = process.cwd();
const RELEASE_VERSION = '1.72.128';
const DEFAULT_SITE = 'https://nad-lan.co.il';
const MODEL_SHA256 = 'ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24';
const MODEL_BYTES = 309148;
const MODEL_TRIANGLES = 21416;
const MODEL_MESHES = 14;
const ARTICLE_SECTION_IDS = [
	'overview',
	'location',
	'buildings-apartments',
	'prices',
	'developer',
	'stages',
	'buyers',
	'questions',
	'sources',
];

const LANGUAGES = {
	he: {
		slug: 'utopia-sde-dov',
		dir: 'rtl',
		firstChapterId: 'overview',
		title: 'UTOPIA שדה דב תל אביב - מחירים, דירות ובחירה מהבניין',
		n1: 'בניין N1',
		leadSignals: [
			['project and city', /UTOPIA[\s\S]*שדה דב[\s\S]*תל אביב/u],
			['apartments', /דירות/u],
			['price', /מחיר/u],
			['purchase', /קנייה/u],
		],
		conceptAlt: /עצמאי|קונספט|הדמיה/u,
	},
	en: {
		slug: 'utopia-sde-dov-en',
		dir: 'ltr',
		firstChapterId: 'overview',
		title: 'UTOPIA Sde Dov Tel Aviv - Apartments for Sale, Prices and Choosing a Home',
		n1: 'N1 building',
		leadSignals: [
			['project and city', /UTOPIA Sde Dov Tel Aviv/i],
			['apartments', /apartments?/i],
			['price', /price/i],
			['purchase', /purchase|buy/i],
		],
		conceptAlt: /concept|illustration/i,
	},
	fr: {
		slug: 'utopia-sde-dov-fr',
		dir: 'ltr',
		firstChapterId: 'vue-ensemble',
		title: "UTOPIA Sde Dov Tel Aviv - Appartements à vendre, prix et choix d'un logement",
		n1: 'Bâtiment N1',
		leadSignals: [
			['project and city', /UTOPIA Sde Dov Tel Aviv/i],
			['apartments', /appartements?/i],
			['price', /prix/i],
			['purchase', /achat|acheter/i],
		],
		conceptAlt: /concept|illustration/i,
	},
	ru: {
		slug: 'utopia-sde-dov-ru',
		dir: 'ltr',
		firstChapterId: 'overview',
		title: 'UTOPIA Sde Dov Тель-Авив - квартиры на продажу, цены и выбор квартиры',
		n1: 'Здание N1',
		leadSignals: [
			['project and city', /UTOPIA Sde Dov[\s\S]*Тель-Авив/iu],
			['apartments', /квартир/iu],
			['price', /цен/iu],
			['purchase', /купить|покуп/iu],
		],
		conceptAlt: /концепт|иллюстрац/iu,
	},
	ar: {
		slug: 'utopia-sde-dov-ar',
		dir: 'rtl',
		firstChapterId: 'overview',
		title: 'UTOPIA Sde Dov تل أبيب - شقق للبيع والأسعار واختيار الشقة',
		n1: 'المبنى N1',
		leadSignals: [
			['project and city', /UTOPIA Sde Dov[\s\S]*تل أبيب/u],
			['apartments', /شقق|شقة/u],
			['price', /سعر|أسعار/u],
			['purchase', /شراء/u],
		],
		conceptAlt: /تصور|مستقل|مفاهيم/u,
	},
};

const MEDIA = [
	{
		file: 'utopia-concept-exterior-v1.webp',
		bytes: 344680,
		sha256: '55122e051450af3e2715af36df05837e06f96f73db9f8291bf4a3f3e8dc263c6',
	},
	{
		file: 'utopia-concept-interior-v1.webp',
		bytes: 192086,
		sha256: 'd89457f00cd52385107072902e7df06fab3750f16b9b18a923396398b59d7c6b',
	},
	{
		file: 'utopia-concept-window-view-v1.webp',
		bytes: 226098,
		sha256: '995a982ea8aed6ded92f3ac30c86c86b20737dd5f20b371a9cf8a4aea2c5f9f4',
	},
	{
		file: 'utopia-concept-wellness-v1.webp',
		bytes: 241988,
		sha256: 'c1d1a1a53b85fc61ad1c39598f4a0a404b92cb4144d3a51c2093cbaabe046a61',
	},
];

const REQUIRED_CHILD_SCRIPTS = [
	'scripts/qa-utopia-comparison-regression.mjs',
	'scripts/qa-utopia-live-comparison-screenshots.mjs',
];

function help() {
	console.log(`Usage:
  node scripts/qa-utopia-postdeploy.mjs --version 1.72.128
  node scripts/qa-utopia-postdeploy.mjs --version 1.72.128 --site https://nad-lan.co.il
  node scripts/qa-utopia-postdeploy.mjs --version 1.72.128 --dry-run

This is a read-only public acceptance gate. It never deploys or writes to
WordPress. A normal run verifies the live five-language UTOPIA family in Google
Chrome, then runs the post-release comparison hash gate and after screenshots.
--dry-run checks the pinned local assets, GLB geometry and Chrome availability
without contacting the public site.`);
}

function parseArgs(argv) {
	const args = {
		version: RELEASE_VERSION,
		site: DEFAULT_SITE,
		out: '',
		evidenceDir: '',
		dryRun: false,
		headed: false,
		timeoutMs: 60000,
	};
	for (let index = 2; index < argv.length; index += 1) {
		const arg = argv[index];
		if (arg === '--version') args.version = argv[++index] || '';
		else if (arg === '--site') args.site = argv[++index] || '';
		else if (arg === '--out') args.out = argv[++index] || '';
		else if (arg === '--evidence-dir') args.evidenceDir = argv[++index] || '';
		else if (arg === '--timeout-ms') args.timeoutMs = Number(argv[++index] || 0);
		else if (arg === '--dry-run') args.dryRun = true;
		else if (arg === '--headed') args.headed = true;
		else if (arg === '--help' || arg === '-h') {
			help();
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}
	if (args.version !== RELEASE_VERSION) {
		throw new Error(
			`This gate is pinned to UTOPIA ${RELEASE_VERSION}; received ${args.version || '(empty)'}. ` +
			'A later release requires an explicit review of the migration identity and asset contract.'
		);
	}
	if (!Number.isFinite(args.timeoutMs) || args.timeoutMs < 10000 || args.timeoutMs > 180000) {
		throw new Error('--timeout-ms must be between 10000 and 180000.');
	}
	const siteUrl = new URL(args.site);
	if (siteUrl.protocol !== 'https:') throw new Error('--site must use HTTPS.');
	args.site = siteUrl.origin + siteUrl.pathname.replace(/\/+$/, '');
	if (args.site !== DEFAULT_SITE) {
		throw new Error(
			`This production acceptance gate is pinned to ${DEFAULT_SITE}; received ${args.site}.`
		);
	}
	if (!args.out) args.out = `docs/qa/utopia-postdeploy-${args.version}${args.dryRun ? '-dry-run' : ''}.json`;
	if (!args.evidenceDir) {
		args.evidenceDir = `docs/qa/screenshots/utopia-live-${args.version}`;
	}
	args.out = path.resolve(ROOT, args.out);
	args.evidenceDir = path.resolve(ROOT, args.evidenceDir);
	return args;
}

function sha256(buffer) {
	return crypto.createHash('sha256').update(buffer).digest('hex');
}

function safeUrl(value) {
	try {
		const url = new URL(value);
		url.search = '';
		url.hash = '';
		return url.href;
	} catch {
		return String(value || '').slice(0, 500);
	}
}

function normalizeUrl(value, base = DEFAULT_SITE) {
	try {
		const url = new URL(value, base);
		url.hash = '';
		return url.href;
	} catch {
		return '';
	}
}

function expectedPageUrls(site) {
	return Object.fromEntries(
		Object.entries(LANGUAGES).map(([lang, spec]) => [
			lang,
			`${site}/projects/${spec.slug}/`,
		])
	);
}

function expectedModelUrl(site) {
	return `${site}/wp-content/plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb`;
}

function expectedMediaUrls(site) {
	return MEDIA.map(
		(asset) =>
			`${site}/wp-content/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/${asset.file}`
	);
}

function localAssetPath(relativePath) {
	return path.resolve(ROOT, relativePath);
}

function parseGlbGeometry(buffer) {
	if (buffer.length < 20 || buffer.toString('utf8', 0, 4) !== 'glTF') {
		throw new Error('GLB header is invalid.');
	}
	const version = buffer.readUInt32LE(4);
	const declaredLength = buffer.readUInt32LE(8);
	if (version !== 2 || declaredLength !== buffer.length) {
		throw new Error(`Unexpected GLB header version=${version} length=${declaredLength}.`);
	}
	let offset = 12;
	let json = null;
	while (offset + 8 <= buffer.length) {
		const chunkLength = buffer.readUInt32LE(offset);
		const chunkType = buffer.readUInt32LE(offset + 4);
		const start = offset + 8;
		const end = start + chunkLength;
		if (end > buffer.length) throw new Error('GLB chunk extends beyond the file.');
		if (chunkType === 0x4e4f534a) {
			json = JSON.parse(buffer.toString('utf8', start, end).replace(/\u0000+$/u, '').trim());
		}
		offset = end;
	}
	if (!json) throw new Error('GLB JSON chunk is missing.');
	let triangles = 0;
	let primitives = 0;
	for (const mesh of json.meshes || []) {
		for (const primitive of mesh.primitives || []) {
			primitives += 1;
			const mode = primitive.mode ?? 4;
			if (mode !== 4) throw new Error(`Unsupported GLB primitive mode ${mode}.`);
			const accessorIndex = Number.isInteger(primitive.indices)
				? primitive.indices
				: primitive.attributes?.POSITION;
			const count = json.accessors?.[accessorIndex]?.count;
			if (!Number.isInteger(count) || count < 0 || count % 3 !== 0) {
				throw new Error(`Invalid triangle accessor count ${count}.`);
			}
			triangles += count / 3;
		}
	}
	return {
		version,
		declaredBytes: declaredLength,
		meshes: (json.meshes || []).length,
		primitives,
		triangles,
	};
}

async function inspectLocalAssets() {
	const rows = [];
	const modelRelative = 'plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb';
	const modelBuffer = await readFile(localAssetPath(modelRelative));
	const geometry = parseGlbGeometry(modelBuffer);
	rows.push({
		kind: 'model',
		path: modelRelative,
		bytes: modelBuffer.length,
		expectedBytes: MODEL_BYTES,
		sha256: sha256(modelBuffer),
		expectedSha256: MODEL_SHA256,
		geometry,
		pass:
			modelBuffer.length === MODEL_BYTES &&
			sha256(modelBuffer) === MODEL_SHA256 &&
			geometry.triangles === MODEL_TRIANGLES &&
			geometry.meshes === MODEL_MESHES,
	});
	for (const asset of MEDIA) {
		const relative = `plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/${asset.file}`;
		const buffer = await readFile(localAssetPath(relative));
		rows.push({
			kind: 'media',
			path: relative,
			bytes: buffer.length,
			expectedBytes: asset.bytes,
			sha256: sha256(buffer),
			expectedSha256: asset.sha256,
			pass: buffer.length === asset.bytes && sha256(buffer) === asset.sha256,
		});
	}
	return rows;
}

async function fetchBytes(url, { timeoutMs, attempts = 4, redirect = 'manual' }) {
	let lastError = null;
	for (let attempt = 1; attempt <= attempts; attempt += 1) {
		try {
			const response = await fetch(url, {
				redirect,
				headers: {
					'user-agent': `NadLan-UTOPIA-live-QA/${RELEASE_VERSION}`,
					'cache-control': 'no-cache',
					pragma: 'no-cache',
					accept: '*/*',
				},
				signal: AbortSignal.timeout(timeoutMs),
			});
			const body = Buffer.from(await response.arrayBuffer());
			const row = {
				attempt,
				status: response.status,
				url: safeUrl(response.url),
				redirected: response.redirected,
				location: response.headers.get('location') || '',
				contentType: response.headers.get('content-type') || '',
				body,
			};
			if (![429, 500, 502, 503, 504].includes(response.status) || attempt === attempts) {
				return row;
			}
		} catch (error) {
			lastError = error;
			if (attempt === attempts) throw error;
		}
		await new Promise((resolve) => setTimeout(resolve, attempt * 800));
	}
	throw lastError || new Error(`Could not fetch ${safeUrl(url)}.`);
}

async function inspectHealth(args) {
	const url = `${args.site}/wp-json/nadlan/v1/healthcheck?utopia_qa=${Date.now()}`;
	try {
		const response = await fetchBytes(url, {
			timeoutMs: args.timeoutMs,
			redirect: 'follow',
		});
		let payload = null;
		let parseError = null;
		try {
			payload = JSON.parse(response.body.toString('utf8'));
		} catch (error) {
			parseError = error.message;
		}
		const utopia = payload?.utopia_sde_dov || null;
		const assertions = [
			['HTTP 200', response.status === 200, 200, response.status],
			['JSON response', payload !== null, true, parseError || false],
			['plugin identity', payload?.plugin === 'nadlan-config', 'nadlan-config', payload?.plugin],
			['exact plugin version', payload?.version === args.version, args.version, payload?.version],
			['UTOPIA release marker', utopia?.release === args.version, args.version, utopia?.release],
			['five-language marker', utopia?.five_languages === true, true, utopia?.five_languages],
			['model validation marker', utopia?.model_asset_validated === true, true, utopia?.model_asset_validated],
			['independent model truth marker', utopia?.official_model === false, false, utopia?.official_model],
			['triangle marker', utopia?.model_triangles === MODEL_TRIANGLES, MODEL_TRIANGLES, utopia?.model_triangles],
			['building interaction marker', utopia?.building_mode === true, true, utopia?.building_mode],
			['no fabricated inventory marker', utopia?.empty_apartment_inventory === true, true, utopia?.empty_apartment_inventory],
		].map(([name, pass, expected, actual]) => ({ name, pass, expected, actual }));
		return {
			url: safeUrl(url),
			status: response.status,
			contentType: response.contentType,
			assertions,
			pass: assertions.every((row) => row.pass),
		};
	} catch (error) {
		return {
			url: safeUrl(url),
			status: 0,
			error: error.stack || error.message,
			assertions: [],
			pass: false,
		};
	}
}

async function inspectExactPageResponses(args, pages) {
	const rows = [];
	for (const [lang, url] of Object.entries(pages)) {
		try {
			const response = await fetchBytes(url, {
				timeoutMs: args.timeoutMs,
				redirect: 'manual',
			});
			rows.push({
				lang,
				url,
				status: response.status,
				finalUrl: response.url,
				redirected: response.redirected,
				location: response.location,
				contentType: response.contentType,
				bytes: response.body.length,
				pass:
					response.status === 200 &&
					response.url === url &&
					!response.redirected &&
					!response.location &&
					/text\/html/i.test(response.contentType) &&
					response.body.length > 10000,
			});
		} catch (error) {
			rows.push({
				lang,
				url,
				status: 0,
				error: error.stack || error.message,
				pass: false,
			});
		}
	}
	return rows;
}

async function inspectRemoteAssets(args) {
	const expected = [
		{
			kind: 'model',
			url: expectedModelUrl(args.site),
			bytes: MODEL_BYTES,
			sha256: MODEL_SHA256,
			contentType: /model\/gltf-binary|application\/octet-stream/i,
		},
		...MEDIA.map((asset, index) => ({
			kind: 'media',
			url: expectedMediaUrls(args.site)[index],
			bytes: asset.bytes,
			sha256: asset.sha256,
			contentType: /image\/webp/i,
		})),
	];
	const rows = [];
	for (const asset of expected) {
		const requestUrl = new URL(asset.url);
		requestUrl.searchParams.set('utopia_qa', String(Date.now()));
		try {
			const response = await fetchBytes(requestUrl.href, {
				timeoutMs: args.timeoutMs,
				redirect: 'manual',
			});
			const actualHash = sha256(response.body);
			rows.push({
				kind: asset.kind,
				url: asset.url,
				status: response.status,
				redirected: response.redirected,
				location: response.location,
				contentType: response.contentType,
				bytes: response.body.length,
				expectedBytes: asset.bytes,
				sha256: actualHash,
				expectedSha256: asset.sha256,
				pass:
					response.status === 200 &&
					!response.redirected &&
					!response.location &&
					asset.contentType.test(response.contentType) &&
					response.body.length === asset.bytes &&
					actualHash === asset.sha256,
			});
		} catch (error) {
			rows.push({
				kind: asset.kind,
				url: asset.url,
				status: 0,
				error: error.stack || error.message,
				pass: false,
			});
		}
	}
	return rows;
}

function addAssertion(assertions, name, actual, expected, pass = actual === expected) {
	assertions.push({ name, pass, expected, actual });
}

function classifyNetworkEvent(siteOrigin, url, detail) {
	let firstParty = false;
	try {
		firstParty = new URL(url).origin === siteOrigin;
	} catch {
		firstParty = false;
	}
	return {
		...detail,
		url: safeUrl(url),
		firstParty,
	};
}

async function inspectPageState(page) {
	return page.evaluate(() => {
		const clean = (value) => String(value || '').replace(/\s+/gu, ' ').trim();
		const absolute = (value) => {
			try {
				return new URL(value, location.href).href;
			} catch {
				return '';
			}
		};
		const visible = (element) => {
			if (!element) return false;
			const style = getComputedStyle(element);
			const rect = element.getBoundingClientRect();
			return (
				style.display !== 'none' &&
				style.visibility !== 'hidden' &&
				Number(style.opacity) > 0 &&
				rect.width > 0 &&
				rect.height > 0
			);
		};
		const precedes = (first, second) =>
			Boolean(first && second && (first.compareDocumentPosition(second) & Node.DOCUMENT_POSITION_FOLLOWING));
		const lead = document.querySelector('.nadlan-project-lead');
		const leadH1 = lead?.querySelector('h1') || null;
		const leadParagraph = lead?.querySelector('p') || null;
		const root = document.querySelector('#nl-root');
		const articleTocs = [...document.querySelectorAll('.utopia-project-content nav')]
			.filter((nav) => nav.querySelectorAll('a[href^="#"]').length > 0);
		const toc = articleTocs[0] || null;
		const canonical = [...document.querySelectorAll('link[rel~="canonical"]')]
			.map((link) => absolute(link.getAttribute('href')));
		const alternates = [...document.querySelectorAll('link[rel~="alternate"][hreflang]')]
			.map((link) => ({
				lang: clean(link.getAttribute('hreflang')).toLowerCase(),
				url: absolute(link.getAttribute('href')),
			}));
		const tocHrefs = toc
			? [...toc.querySelectorAll('a[href^="#"]')].map((anchor) => anchor.getAttribute('href'))
			: [];
		const media = [...document.querySelectorAll('.utopia-media-gallery img')].map((image) => ({
			src: absolute(image.getAttribute('src')),
			currentSrc: absolute(image.currentSrc || image.src),
			alt: image.getAttribute('alt') || '',
			complete: image.complete,
			naturalWidth: image.naturalWidth,
			naturalHeight: image.naturalHeight,
		}));
		const model = document.querySelector('#nl-mv, model-viewer');
		const modelRect = model?.getBoundingClientRect() || null;
		const modelSrc = model ? absolute(model.getAttribute('src')) : '';
		const clientWidth = document.documentElement.clientWidth;
		const jsonLd = [];
		const jsonLdErrors = [];
		for (const script of document.querySelectorAll('script[type="application/ld+json"]')) {
			try {
				jsonLd.push(JSON.parse(script.textContent || ''));
			} catch (error) {
				jsonLdErrors.push(error.message);
			}
		}
		const schemaTypes = [];
		const collectTypes = (value) => {
			if (!value || typeof value !== 'object') return;
			if (Array.isArray(value)) {
				value.forEach(collectTypes);
				return;
			}
			if (value['@type']) {
				const types = Array.isArray(value['@type']) ? value['@type'] : [value['@type']];
				schemaTypes.push(...types.map(String));
			}
			if (value['@graph']) collectTypes(value['@graph']);
		};
		jsonLd.forEach(collectTypes);
		const buildingTargets = [...document.querySelectorAll('.nl-building-hot[data-act="building"]')];
		return {
			location: location.href,
			title: document.title,
			lang: document.documentElement.lang,
			dir: document.documentElement.dir,
			canonical,
			alternates,
			h1Count: document.querySelectorAll('h1').length,
			h1Text: clean(document.querySelector('h1')?.textContent),
			leadH1Text: clean(leadH1?.textContent),
			leadText: clean(leadParagraph?.textContent),
			leadWordCount: clean(leadParagraph?.textContent).split(/\s+/u).filter(Boolean).length,
			h1BeforeShowroom: precedes(leadH1, root),
			leadBeforeShowroom: precedes(leadParagraph, root),
			showroomBeforeArticleToc: precedes(root, toc),
			engineRootCount: document.querySelectorAll('#nl-root.nl-app').length,
			articleTocCount: articleTocs.length,
			articleTocLinks: tocHrefs.length,
			articleTocTargetsValid: tocHrefs.every((href) => {
				try {
					return document.querySelectorAll(href).length === 1;
				} catch {
					return false;
				}
			}),
			nlwTocCount: document.querySelectorAll('.nlw-toc').length,
			articleH2Ids: [...document.querySelectorAll('.utopia-project-content h2[id]')]
				.map((heading) => heading.id),
			emptyHeadings: [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')]
				.filter((heading) => !clean(heading.textContent))
				.map((heading) => heading.outerHTML.slice(0, 180)),
			legacyBlocks: document.querySelectorAll(
				'.nlpf,.nlpjx-nav,.nlpjx-intro,.nlpjx-price,.nlpjx,.nlcard,.nlms,.nlpe'
			).length,
			relativeTemplateHrefs: [...document.querySelectorAll('a[href]')]
				.map((anchor) => anchor.getAttribute('href') || '')
				.filter((href) => /(?:^|\/)(?:home|project)\.html(?:[?#]|$)/i.test(href)),
			media,
			mediaCaptions: document.querySelectorAll('.utopia-media-gallery figcaption').length,
			heroImageAlt: document.querySelector('.nl-hero__media img')?.getAttribute('alt') || '',
			modelViewerCount: document.querySelectorAll('model-viewer').length,
			modelSrc,
			modelLoaded: Boolean(model && model.loaded === true),
			modelVisible: Boolean(model && model.modelIsVisible === true && visible(model)),
			modelRect: modelRect
				? {
					left: Math.round(modelRect.left),
					right: Math.round(modelRect.right),
					top: Math.round(modelRect.top),
					bottom: Math.round(modelRect.bottom),
					width: Math.round(modelRect.width),
					height: Math.round(modelRect.height),
				}
				: null,
			modelErrorVisible: visible(document.querySelector('#nl-model-error')),
			buildingHotspots: buildingTargets.length,
			buildingLabels: buildingTargets.map((target) => clean(target.textContent)),
			buildingAriaLabels: buildingTargets.map((target) => target.getAttribute('aria-label') || ''),
			buildingTargetSizes: buildingTargets.map((target) => {
				const rect = target.getBoundingClientRect();
				return { width: Math.round(rect.width), height: Math.round(rect.height) };
			}),
			unitHotspots: document.querySelectorAll(
				'.nl-hot[data-act="select"],[slot^="hotspot-unit-"],[data-act="select"][data-id]'
			).length,
			samplePlans: document.querySelectorAll('.nl-plan-card').length,
			utopiaStylesheets: [...document.querySelectorAll('link[rel="stylesheet"]')]
				.map((link) => absolute(link.getAttribute('href')))
				.filter((href) => /\/projects\/utopia-sde-dov\/utopia\.css(?:[?#]|$)/.test(href)),
			clientWidth,
			scrollWidth: document.documentElement.scrollWidth,
			horizontalOverflowPx: Math.max(0, document.documentElement.scrollWidth - clientWidth),
			jsonLdErrors,
			schemaTypes,
		};
	});
}

async function inspectSelectedBuilding(page) {
	return page.evaluate(() => {
		const clean = (value) => String(value || '').replace(/\s+/gu, ' ').trim();
		const panel = document.querySelector('#nl-panel');
		const active = document.querySelector('.nl-building-hot.is-active');
		return {
			panelOpen: Boolean(panel?.classList.contains('is-open')),
			panelTitle: clean(document.querySelector('.nl-panel__title')?.textContent),
			activeBuildingId: active?.getAttribute('data-id') || '',
			activeBuildingCount: document.querySelectorAll('.nl-building-hot.is-active').length,
			planLinks: document.querySelectorAll('.nl-building-plan').length,
		};
	});
}

function buildAssertions({ lang, spec, pageUrl, pageResponse, state, selected, events, site, isMobile }) {
	const assertions = [];
	const pages = expectedPageUrls(site);
	const expectedAlternates = { ...pages, 'x-default': pages.he };
	const alternateMap = {};
	for (const alternate of state.alternates) {
		if (!alternateMap[alternate.lang]) alternateMap[alternate.lang] = [];
		alternateMap[alternate.lang].push(alternate.url);
	}
	addAssertion(assertions, 'browser document HTTP 200', pageResponse.status, 200);
	addAssertion(assertions, 'browser document had no redirect', pageResponse.redirected, false);
	addAssertion(assertions, 'exact live URL stayed selected', normalizeUrl(state.location), pageUrl);
	addAssertion(assertions, 'document language', state.lang.toLowerCase().split('-')[0], lang);
	addAssertion(assertions, 'document direction', state.dir, spec.dir);
	addAssertion(assertions, 'exact document title', state.title, spec.title);
	addAssertion(assertions, 'one H1', state.h1Count, 1);
	addAssertion(assertions, 'exact buyer H1', state.h1Text, spec.title);
	addAssertion(assertions, 'H1 belongs to the factual lead', state.leadH1Text, spec.title);
	addAssertion(assertions, 'H1 precedes showroom', state.h1BeforeShowroom, true);
	addAssertion(assertions, 'opening factual paragraph precedes showroom', state.leadBeforeShowroom, true);
	addAssertion(assertions, 'showroom precedes article navigation', state.showroomBeforeArticleToc, true);
	addAssertion(assertions, 'opening paragraph has useful depth', state.leadWordCount >= 80, true);
	for (const [label, pattern] of spec.leadSignals) {
		addAssertion(
			assertions,
			`opening paragraph contains ${label}`,
			pattern.test(state.leadText),
			true
		);
	}
	for (const fact of ['337', '34', '15', '7']) {
		addAssertion(
			assertions,
			`opening paragraph contains factual number ${fact}`,
			new RegExp(`(?:^|\\D)${fact}(?:\\D|$)`, 'u').test(state.leadText),
			true
		);
	}
	addAssertion(assertions, 'one canonical', state.canonical.length, 1);
	addAssertion(assertions, 'self canonical', state.canonical[0] || '', pageUrl);
	addAssertion(
		assertions,
		'exact hreflang key set',
		Object.keys(alternateMap).sort(),
		Object.keys(expectedAlternates).sort(),
		JSON.stringify(Object.keys(alternateMap).sort()) === JSON.stringify(Object.keys(expectedAlternates).sort())
	);
	for (const [code, expectedUrl] of Object.entries(expectedAlternates)) {
		addAssertion(
			assertions,
			`one exact ${code} alternate`,
			alternateMap[code] || [],
			[expectedUrl],
			JSON.stringify(alternateMap[code] || []) === JSON.stringify([expectedUrl])
		);
	}
	addAssertion(assertions, 'one composed showroom root', state.engineRootCount, 1);
	addAssertion(assertions, 'one article-authored table of contents', state.articleTocCount, 1);
	addAssertion(assertions, 'nine article navigation links', state.articleTocLinks, 9);
	addAssertion(assertions, 'all article navigation targets resolve once', state.articleTocTargetsValid, true);
	addAssertion(assertions, 'no generated duplicate TOC', state.nlwTocCount, 0);
	addAssertion(
		assertions,
		'nine buyer-article chapter IDs',
		state.articleH2Ids.length,
		9
	);
	addAssertion(
		assertions,
		'article starts with its expected overview chapter and ends with sources',
		[state.articleH2Ids[0], state.articleH2Ids.at(-1)],
		[spec.firstChapterId, ARTICLE_SECTION_IDS.at(-1)],
		state.articleH2Ids[0] === spec.firstChapterId && state.articleH2Ids.at(-1) === ARTICLE_SECTION_IDS.at(-1)
	);
	addAssertion(assertions, 'no empty headings', state.emptyHeadings, [], state.emptyHeadings.length === 0);
	addAssertion(assertions, 'no legacy project blocks', state.legacyBlocks, 0);
	addAssertion(
		assertions,
		'no template-relative home or project URLs',
		state.relativeTemplateHrefs,
		[],
		state.relativeTemplateHrefs.length === 0
	);
	addAssertion(assertions, 'one route-scoped UTOPIA stylesheet', state.utopiaStylesheets.length, 1);
	addAssertion(assertions, 'four media images', state.media.length, 4);
	addAssertion(assertions, 'four media captions', state.mediaCaptions, 4);
	addAssertion(
		assertions,
		'exact media URLs',
		state.media.map((row) => row.src),
		expectedMediaUrls(site),
		JSON.stringify(state.media.map((row) => row.src)) === JSON.stringify(expectedMediaUrls(site))
	);
	addAssertion(
		assertions,
		'all media images loaded at 1536 by 1024',
		state.media.map((row) => [row.complete, row.naturalWidth, row.naturalHeight]),
		Array.from({ length: 4 }, () => [true, 1536, 1024]),
		state.media.every((row) => row.complete && row.naturalWidth === 1536 && row.naturalHeight === 1024)
	);
	addAssertion(
		assertions,
		'all media images have buyer-facing alt text',
		state.media.map((row) => row.alt),
		'four non-empty localized alt values',
		state.media.every((row) => row.alt.trim().length >= 12)
	);
	addAssertion(
		assertions,
		'hero image discloses concept status',
		spec.conceptAlt.test(state.heroImageAlt),
		true
	);
	addAssertion(assertions, 'one model-viewer', state.modelViewerCount, 1);
	addAssertion(assertions, 'exact UTOPIA model URL', state.modelSrc, expectedModelUrl(site));
	addAssertion(assertions, 'GLB loaded', state.modelLoaded, true);
	addAssertion(assertions, 'GLB visibly rendered', state.modelVisible, true);
	addAssertion(assertions, 'model error is hidden', state.modelErrorVisible, false);
	addAssertion(
		assertions,
		'model has visible geometry box',
		Boolean(state.modelRect && state.modelRect.width > 0 && state.modelRect.height > 0),
		true
	);
	addAssertion(assertions, 'four building hotspots', state.buildingHotspots, 4);
	addAssertion(
		assertions,
		'stable building labels',
		state.buildingLabels,
		['S1', 'N1', 'N2', 'S2'],
		JSON.stringify(state.buildingLabels) === JSON.stringify(['S1', 'N1', 'N2', 'S2'])
	);
	addAssertion(assertions, 'localized N1 accessible label', state.buildingAriaLabels[1] || '', spec.n1);
	addAssertion(assertions, 'zero invented unit hotspots', state.unitHotspots, 0);
	addAssertion(assertions, 'seven published sample plans', state.samplePlans, 7);
	addAssertion(assertions, 'N1 click opens building panel', selected.panelOpen, true);
	addAssertion(assertions, 'localized selected-building title', selected.panelTitle, spec.n1);
	addAssertion(assertions, 'N1 is the only active building', [selected.activeBuildingId, selected.activeBuildingCount], ['n1', 1], selected.activeBuildingId === 'n1' && selected.activeBuildingCount === 1);
	addAssertion(assertions, 'N1 panel exposes four plan links', selected.planLinks, 4);
	addAssertion(
		assertions,
		'browser requested the exact GLB',
		events.modelResponses.filter((row) => row.status === 200).length >= 1,
		true
	);
	addAssertion(
		assertions,
		'browser loaded all four exact media assets',
		new Set(events.mediaResponses.filter((row) => row.status === 200).map((row) => row.url)).size,
		4
	);
	addAssertion(assertions, 'no console errors', events.consoleErrors, [], events.consoleErrors.length === 0);
	addAssertion(assertions, 'no page errors', events.pageErrors, [], events.pageErrors.length === 0);
	addAssertion(
		assertions,
		'no first-party network failures',
		events.networkErrors.filter((row) => row.firstParty),
		[],
		events.networkErrors.filter((row) => row.firstParty).length === 0
	);
	addAssertion(assertions, 'no horizontal overflow', state.horizontalOverflowPx, 0);
	addAssertion(assertions, 'all JSON-LD parses', state.jsonLdErrors, [], state.jsonLdErrors.length === 0);
	addAssertion(
		assertions,
		'visible FAQ has FAQPage schema',
		state.schemaTypes.includes('FAQPage'),
		true
	);
	if (isMobile) {
		addAssertion(
			assertions,
			'mobile model stays within viewport',
			Boolean(
				state.modelRect &&
				state.modelRect.left >= -1 &&
				state.modelRect.right <= state.clientWidth + 1
			),
			true
		);
	}
	return assertions;
}

async function runBrowserCase(browser, args, lang, viewportName, viewport, isMobile) {
	const spec = LANGUAGES[lang];
	const pageUrl = expectedPageUrls(args.site)[lang];
	const siteOrigin = new URL(args.site).origin;
	const expectedModel = expectedModelUrl(args.site);
	const mediaSet = new Set(expectedMediaUrls(args.site));
	const context = await browser.newContext({
		viewport,
		deviceScaleFactor: 1,
		isMobile,
		hasTouch: isMobile,
		locale: {
			he: 'he-IL',
			en: 'en-US',
			fr: 'fr-FR',
			ru: 'ru-RU',
			ar: 'ar',
		}[lang],
		extraHTTPHeaders: {
			'cache-control': 'no-cache',
			pragma: 'no-cache',
		},
	});
	const page = await context.newPage();
	const events = {
		consoleErrors: [],
		pageErrors: [],
		networkErrors: [],
		modelResponses: [],
		mediaResponses: [],
	};
	page.on('console', (message) => {
		if (message.type() === 'error') {
			events.consoleErrors.push(message.text().replace(/\s+/gu, ' ').trim().slice(0, 1200));
		}
	});
	page.on('pageerror', (error) => {
		events.pageErrors.push(String(error.message || error).replace(/\s+/gu, ' ').trim().slice(0, 1200));
	});
	page.on('requestfailed', (request) => {
		events.networkErrors.push(
			classifyNetworkEvent(siteOrigin, request.url(), {
				kind: 'requestfailed',
				resourceType: request.resourceType(),
				error: request.failure()?.errorText || 'unknown request failure',
			})
		);
	});
	page.on('response', (response) => {
		const cleanUrl = safeUrl(response.url());
		if (response.status() >= 400) {
			events.networkErrors.push(
				classifyNetworkEvent(siteOrigin, response.url(), {
					kind: 'http',
					status: response.status(),
				})
			);
		}
		if (cleanUrl === expectedModel) {
			events.modelResponses.push({ url: cleanUrl, status: response.status() });
		}
		if (mediaSet.has(cleanUrl)) {
			events.mediaResponses.push({ url: cleanUrl, status: response.status() });
		}
	});

	const prefix = `${lang}-${viewportName}`;
	const topScreenshot = path.join(args.evidenceDir, `${prefix}-top.png`);
	const modelScreenshot = path.join(args.evidenceDir, `${prefix}-model.png`);
	const selectedScreenshot = path.join(args.evidenceDir, `${prefix}-selected-n1.png`);
	let pageResponse = { status: 0, redirected: false, finalUrl: '' };
	let state = null;
	let selected = null;
	let fatal = null;
	try {
		const response = await page.goto(pageUrl, {
			waitUntil: 'domcontentloaded',
			timeout: args.timeoutMs,
		});
		pageResponse = {
			status: response?.status() || 0,
			redirected: Boolean(response?.request().redirectedFrom()),
			finalUrl: safeUrl(response?.url() || ''),
		};
		await page.waitForSelector('#nl-root.nl-app', { timeout: args.timeoutMs });
		await page.locator('.nadlan-project-lead h1').scrollIntoViewIfNeeded();
		await page.waitForTimeout(350);
		await page.screenshot({ path: topScreenshot, fullPage: false });

		const media = page.locator('.utopia-media-gallery img');
		for (let index = 0; index < await media.count(); index += 1) {
			await media.nth(index).scrollIntoViewIfNeeded();
		}
		await page.waitForFunction(
			() =>
				[...document.querySelectorAll('.utopia-media-gallery img')].length === 4 &&
				[...document.querySelectorAll('.utopia-media-gallery img')]
					.every((image) => image.complete && image.naturalWidth > 0),
			null,
			{ timeout: args.timeoutMs }
		);
		await page.locator('#building').scrollIntoViewIfNeeded();
		await page.waitForFunction(
			() => Boolean(customElements.get('model-viewer')),
			null,
			{ timeout: args.timeoutMs }
		);
		await page.waitForFunction(
			() => {
				const model = document.querySelector('#nl-mv');
				return Boolean(model && model.loaded === true && model.modelIsVisible === true);
			},
			null,
			{ timeout: args.timeoutMs }
		);
		await page.waitForTimeout(500);
		await page.screenshot({ path: modelScreenshot, fullPage: false });
		state = await inspectPageState(page);

		const n1 = page.locator('.nl-building-hot[data-act="building"][data-id="n1"]');
		await n1.click({ timeout: args.timeoutMs });
		await page.waitForFunction(
			(expectedTitle) => {
				const panel = document.querySelector('#nl-panel');
				const title = document.querySelector('.nl-panel__title');
				return Boolean(
					panel?.classList.contains('is-open') &&
					title?.textContent.replace(/\s+/gu, ' ').trim() === expectedTitle
				);
			},
			spec.n1,
			{ timeout: args.timeoutMs }
		);
		await page.waitForTimeout(700);
		await page.screenshot({ path: selectedScreenshot, fullPage: false });
		selected = await inspectSelectedBuilding(page);
	} catch (error) {
		fatal = error.stack || error.message;
	}

	const assertions =
		state && selected
			? buildAssertions({
				lang,
				spec,
				pageUrl,
				pageResponse,
				state,
				selected,
				events,
				site: args.site,
				isMobile,
			})
			: [];
	const failures = assertions
		.filter((assertion) => !assertion.pass)
		.map(({ name, expected, actual }) => ({ name, expected, actual }));
	if (fatal) failures.unshift({ name: 'browser case completed', expected: true, actual: fatal });
	const externalNetworkWarnings = events.networkErrors.filter((row) => !row.firstParty);
	await context.close();
	return {
		lang,
		viewport: viewportName,
		dimensions: viewport,
		url: pageUrl,
		pass: failures.length === 0,
		pageResponse,
		state,
		selected,
		events,
		assertions,
		failures,
		warnings: externalNetworkWarnings.length
			? [{ name: 'external network failures', detail: externalNetworkWarnings }]
			: [],
		screenshots: {
			top: path.relative(ROOT, topScreenshot).replaceAll('\\', '/'),
			model: path.relative(ROOT, modelScreenshot).replaceAll('\\', '/'),
			selected: path.relative(ROOT, selectedScreenshot).replaceAll('\\', '/'),
		},
	};
}

function runChild(name, command, commandArgs) {
	const startedAt = new Date().toISOString();
	const result = spawnSync(command, commandArgs, {
		cwd: ROOT,
		encoding: 'utf8',
		maxBuffer: 20 * 1024 * 1024,
	});
	return {
		name,
		command: [command, ...commandArgs].join(' '),
		startedAt,
		exitCode: result.status,
		signal: result.signal || null,
		ok: result.status === 0,
		stdoutTail: String(result.stdout || '').slice(-6000),
		stderrTail: String(result.stderr || '').slice(-6000),
	};
}

function inspectComparisonReport() {
	const reportPath = path.join(ROOT, 'docs', 'qa', 'utopia-comparison-regression-report.json');
	try {
		const payload = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
		return {
			path: path.relative(ROOT, reportPath).replaceAll('\\', '/'),
			phase: payload.phase,
			restUnchanged: payload.rest_unchanged,
			restTotal: payload.rest_total,
			modelsUnchanged: payload.models_unchanged,
			modelsTotal: payload.models_total,
			reportPass: payload.pass === true,
			pass:
				payload.phase === 'post-release' &&
				payload.pass === true &&
				payload.rest_unchanged === payload.rest_total &&
				payload.models_unchanged === payload.models_total,
		};
	} catch (error) {
		return {
			path: path.relative(ROOT, reportPath).replaceAll('\\', '/'),
			error: error.message,
			pass: false,
		};
	}
}

function inspectAfterScreenshots() {
	const reportPath = path.join(
		ROOT,
		'docs',
		'qa',
		'screenshots',
		'utopia-comparison-after-2026-07-29',
		'report.json'
	);
	try {
		const payload = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
		const expectedKeys = [
			'utopia-sde-dov',
			'duo-tel-aviv',
			'rainbow-tel-aviv',
			'dimri-yama-sde-dov',
			'ashira-sde-dov',
		];
		const pageChecks = payload.pages.map((row) => {
			const screenshotPaths = Object.values(row.screenshots || {}).filter(Boolean);
			const screenshots = screenshotPaths.map((relative) => {
				const absolute = path.resolve(ROOT, relative);
				return {
					path: relative,
					exists: fs.existsSync(absolute),
					bytes: fs.existsSync(absolute) ? fs.statSync(absolute).size : 0,
				};
			});
			return {
				key: row.key,
				httpStatus: row.http_status,
				h1Count: row.h1Texts?.length || 0,
				engineRoots: row.engineRoots,
				horizontalOverflowPx: row.horizontal_overflow_px,
				errors: row.errors || [],
				screenshots,
				pass:
					row.http_status === 200 &&
					row.h1Texts?.length === 1 &&
					row.engineRoots === 1 &&
					row.horizontal_overflow_px === 0 &&
					(row.errors || []).length === 0 &&
					screenshots.length === 2 &&
					screenshots.every((shot) => shot.exists && shot.bytes > 1000),
			};
		});
		return {
			path: path.relative(ROOT, reportPath).replaceAll('\\', '/'),
			phase: payload.phase,
			pageChecks,
			pass:
				payload.phase === 'after' &&
				JSON.stringify(payload.pages.map((row) => row.key)) === JSON.stringify(expectedKeys) &&
				pageChecks.every((row) => row.pass),
		};
	} catch (error) {
		return {
			path: path.relative(ROOT, reportPath).replaceAll('\\', '/'),
			error: error.message,
			pass: false,
		};
	}
}

async function writeReport(report, outputPath) {
	await mkdir(path.dirname(outputPath), { recursive: true });
	await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
}

async function runDryRun(args, report) {
	report.localAssets = await inspectLocalAssets();
	report.requiredScripts = REQUIRED_CHILD_SCRIPTS.map((relative) => ({
		path: relative,
		exists: fs.existsSync(path.join(ROOT, relative)),
	}));
	let browser = null;
	try {
		browser = await chromium.launch({ channel: 'chrome', headless: true });
		report.googleChrome = { available: true, version: await browser.version() };
	} catch (error) {
		report.googleChrome = { available: false, error: error.message };
	} finally {
		if (browser) await browser.close();
	}
	report.pass =
		report.localAssets.every((row) => row.pass) &&
		report.requiredScripts.every((row) => row.exists) &&
		report.googleChrome.available;
	report.summary = {
		mode: 'dry-run',
		localAssetsPassed: report.localAssets.filter((row) => row.pass).length,
		localAssetsTotal: report.localAssets.length,
		requiredScriptsPresent: report.requiredScripts.filter((row) => row.exists).length,
		requiredScriptsTotal: report.requiredScripts.length,
		googleChromeAvailable: report.googleChrome.available,
	};
}

async function runLive(args, report) {
	const pages = expectedPageUrls(args.site);
	await mkdir(args.evidenceDir, { recursive: true });
	report.health = await inspectHealth(args);
	report.exactPageResponses = await inspectExactPageResponses(args, pages);
	report.remoteAssets = await inspectRemoteAssets(args);

	let browser = null;
	report.browserCases = [];
	try {
		browser = await chromium.launch({ channel: 'chrome', headless: !args.headed });
		const cases = [
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
		for (const testCase of cases) {
			const result = await runBrowserCase(
				browser,
				args,
				testCase.lang,
				testCase.viewportName,
				testCase.viewport,
				testCase.isMobile
			);
			report.browserCases.push(result);
			console.log(
				`${result.pass ? 'PASS' : 'FAIL'} ${result.lang} ${result.viewport}` +
				(result.failures.length
					? ` - ${result.failures.map((failure) => failure.name).join(', ')}`
					: '')
			);
		}
	} catch (error) {
		report.browserFatal = error.stack || error.message;
	} finally {
		if (browser) await browser.close();
	}

	const comparisonStep = runChild(
		'post-release comparison hashes',
		process.execPath,
		['scripts/qa-utopia-comparison-regression.mjs', '--post-release']
	);
	console.log(`${comparisonStep.ok ? 'PASS' : 'FAIL'} post-release comparison hashes`);
	const screenshotsStep = runChild(
		'after comparison screenshots',
		process.execPath,
		['scripts/qa-utopia-live-comparison-screenshots.mjs', '--phase=after']
	);
	console.log(`${screenshotsStep.ok ? 'PASS' : 'FAIL'} after comparison screenshots`);
	report.childQa = {
		steps: [comparisonStep, screenshotsStep],
		comparison: inspectComparisonReport(),
		afterScreenshots: inspectAfterScreenshots(),
	};

	report.pass =
		report.health.pass &&
		report.exactPageResponses.every((row) => row.pass) &&
		report.remoteAssets.every((row) => row.pass) &&
		report.browserCases.length === 10 &&
		report.browserCases.every((row) => row.pass) &&
		!report.browserFatal &&
		report.childQa.steps.every((row) => row.ok) &&
		report.childQa.comparison.pass &&
		report.childQa.afterScreenshots.pass;
	report.summary = {
		mode: 'postdeploy',
		healthPassed: report.health.pass,
		exactPagesPassed: report.exactPageResponses.filter((row) => row.pass).length,
		exactPagesTotal: report.exactPageResponses.length,
		remoteAssetsPassed: report.remoteAssets.filter((row) => row.pass).length,
		remoteAssetsTotal: report.remoteAssets.length,
		browserCasesPassed: report.browserCases.filter((row) => row.pass).length,
		browserCasesTotal: report.browserCases.length,
		assertions: report.browserCases.reduce((sum, row) => sum + row.assertions.length, 0),
		failedAssertions: report.browserCases.reduce((sum, row) => sum + row.failures.length, 0),
		warningCases: report.browserCases.filter((row) => row.warnings.length > 0).length,
		comparisonRestUnchanged: `${report.childQa.comparison.restUnchanged ?? 0}/${report.childQa.comparison.restTotal ?? 0}`,
		comparisonModelsUnchanged: `${report.childQa.comparison.modelsUnchanged ?? 0}/${report.childQa.comparison.modelsTotal ?? 0}`,
		afterScreenshotPagesPassed: report.childQa.afterScreenshots.pageChecks?.filter((row) => row.pass).length || 0,
		afterScreenshotPagesTotal: report.childQa.afterScreenshots.pageChecks?.length || 0,
	};
}

async function main() {
	const args = parseArgs(process.argv);
	const report = {
		schema: 'nadlan-utopia-postdeploy/v1',
		generatedAt: new Date().toISOString(),
		release: args.version,
		site: args.site,
		mode: args.dryRun ? 'dry-run' : 'postdeploy',
		evidenceDirectory: path.relative(ROOT, args.evidenceDir).replaceAll('\\', '/'),
		readOnlyPublicQa: true,
		deploymentPerformed: false,
		pass: false,
	};
	try {
		if (args.dryRun) await runDryRun(args, report);
		else await runLive(args, report);
	} catch (error) {
		report.fatal = error.stack || error.message;
		report.pass = false;
	}
	await writeReport(report, args.out);
	console.log(
		JSON.stringify(
			{
				pass: report.pass,
				mode: report.mode,
				summary: report.summary || null,
				report: path.relative(ROOT, args.out).replaceAll('\\', '/'),
				evidenceDirectory: report.evidenceDirectory,
			},
			null,
			2
		)
	);
	if (!report.pass) process.exitCode = 1;
}

main().catch((error) => {
	console.error(error.stack || error.message);
	process.exit(1);
});
