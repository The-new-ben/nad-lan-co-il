import fs from 'node:fs/promises';
import path from 'node:path';

const DEFAULT_PAYLOAD = 'assets/projects/ashira-sde-dov/showroom-payload.json';
const DEFAULT_OUT = 'docs/qa/ashira-v2-factory-readiness-report.json';
const DEFAULT_SCREENSHOT_REPORT = 'docs/qa/screenshots/ashira-v2-preview-factory-gate/report.json';

const REQUIRED_FILES = [
	{ file: 'patterns/project-showroom-ashira-v2.php', kind: 'pattern' },
	{ file: 'docs/previews/ashira-showroom-v2-preview.html', kind: 'preview' },
	{ file: 'assets/js/nadlan-showroom-v2.js', kind: 'runtime' },
	{ file: 'assets/css/nadlan-showroom-v2.css', kind: 'style' },
	{ file: 'assets/projects/ashira-sde-dov/showroom-payload.json', kind: 'payload', maxBytes: 200 * 1024 },
	{ file: 'assets/projects/ashira-sde-dov/model-context.glb', kind: 'model', maxBytes: 8 * 1024 * 1024 },
	{ file: 'assets/projects/ashira-sde-dov/ashira-hero-concept.jpg', kind: 'hero', maxBytes: 700 * 1024 },
	{ file: 'assets/projects/ashira-sde-dov/ashira-facade-concept.jpg', kind: 'facade', maxBytes: 700 * 1024 },
	{ file: 'assets/projects/ashira-sde-dov/source-notes.md', kind: 'sources' },
];

const REQUIRED_META_FIELDS = [
	'project_3d_image',
	'project_3d_facade_images',
	'project_3d_viewbox',
	'project_3d_model_type',
	'project_model_glb',
	'project_model_poster',
	'project_3d_drawings_json',
	'project_3d_environment_json',
	'project_3d_units',
];

const UNIT_REQUIRED_FIELDS = [
	'id',
	'title',
	'label',
	'floor',
	'rooms',
	'sqm',
	'dir',
	'view',
	'status',
	'availability',
	'price_estimate',
	'price_note',
	'stage_x',
	'stage_y',
];

const ALLOWED_STATUSES = new Set(['available', 'reserved', 'sold', 'checking', 'unavailable']);

const MOJIBAKE_RE = /[\u00c3\u00c2\ufffd]|\u00d7[\u0080-\u00ff]|\u00c2\u00b7|\u00c3\u0097/;
const INTERNAL_RE = /\b(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|Codex|Claude)\b|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה/i;

const URLISH_KEYS = new Set([
	'$schema',
	'schema',
	'project_slug',
	'post_id',
	'generated_from',
	'public_use_policy',
	'source',
	'source_policy',
	'id',
	'src',
	'url',
	'kind',
	'type',
	'approved',
	'concept',
	'project_3d_model_type',
	'project_3d_viewbox',
	'project_3d_floor_height_m',
	'project_3d_ground_elevation_m',
	'project_3d_avg_price_per_sqm',
	'project_model_glb',
	'project_model_usdz',
	'project_model_poster',
	'project_3d_image',
	'project_3d_video_url',
	'project_3d_tour_url',
	'project_3d_cesium_tiles_url',
	'hotspot_position',
	'hotspot_normal',
	'camera_orbit',
	'stage_x',
	'stage_y',
	'stage_w',
	'stage_h',
	'project_3d_demo',
]);

function parseArgs(argv) {
	const args = {
		payload: DEFAULT_PAYLOAD,
		out: DEFAULT_OUT,
		screenshotReport: DEFAULT_SCREENSHOT_REPORT,
		strict: false,
	};
	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === '--payload') args.payload = argv[++i] || args.payload;
		else if (arg === '--out') args.out = argv[++i] || args.out;
		else if (arg === '--screenshot-report') args.screenshotReport = argv[++i] || args.screenshotReport;
		else if (arg === '--strict') args.strict = true;
		else if (arg === '--help' || arg === '-h') {
			console.log(`Usage:
  node scripts/qa-ashira-factory-readiness.mjs --strict

Checks the Ashira clean v2 factory inputs before WordPress import:
assets, payload fields, buyer-facing copy hygiene, and the latest screenshot report.`);
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}
	return args;
}

async function readText(file) {
	return fs.readFile(path.resolve(process.cwd(), file), 'utf8');
}

async function readJson(file) {
	const text = await readText(file);
	return JSON.parse(text.replace(/^\uFEFF/, ''));
}

function pushFailure(report, code, message, details = {}) {
	report.failures.push({ code, message, details });
}

function stripVisibleText(source) {
	return source
		.replace(/<\?php[\s\S]*?\?>/g, ' ')
		.replace(/<script[\s\S]*?<\/script>/gi, ' ')
		.replace(/<style[\s\S]*?<\/style>/gi, ' ')
		.replace(/<[^>]+>/g, ' ')
		.replace(/&nbsp;/g, ' ')
		.replace(/&quot;/g, '"')
		.replace(/&#039;/g, "'")
		.replace(/&amp;/g, '&')
		.replace(/\s+/g, ' ')
		.trim();
}

function collectPublicPayloadStrings(value, bucket, keyPath = []) {
	if (Array.isArray(value)) {
		value.forEach((item, index) => collectPublicPayloadStrings(item, bucket, [...keyPath, String(index)]));
		return;
	}
	if (!value || typeof value !== 'object') {
		const key = keyPath[keyPath.length - 1] || '';
		if (typeof value === 'string' && value.trim() && !URLISH_KEYS.has(key) && !/_url$|_glb$|_poster$|_image$/.test(key)) {
			bucket.push({ path: keyPath.join('.'), text: value });
		}
		return;
	}
	for (const [key, child] of Object.entries(value)) {
		if (URLISH_KEYS.has(key)) continue;
		collectPublicPayloadStrings(child, bucket, [...keyPath, key]);
	}
}

function checkCopy(report, label, text, { requireHebrew = false } = {}) {
	const trimmed = String(text || '').trim();
	if (!trimmed) {
		pushFailure(report, 'empty-copy', `${label} has no readable copy`);
		return;
	}
	if (requireHebrew && !/[\u0590-\u05ff]/.test(trimmed)) {
		pushFailure(report, 'missing-hebrew', `${label} has no Hebrew buyer-facing text`);
	}
	if (MOJIBAKE_RE.test(trimmed)) {
		pushFailure(report, 'mojibake-copy', `${label} contains mojibake or replacement text`);
	}
	const internal = trimmed.match(INTERNAL_RE);
	if (internal) {
		pushFailure(report, 'internal-copy', `${label} leaks non-buyer language`, { term: internal[0] });
	}
}

async function checkFiles(report) {
	for (const item of REQUIRED_FILES) {
		try {
			const stat = await fs.stat(path.resolve(process.cwd(), item.file));
			report.files.push({ ...item, bytes: stat.size, ok: true });
			if (item.maxBytes && stat.size > item.maxBytes) {
				pushFailure(report, 'asset-budget', `${item.file} exceeds size budget`, {
					bytes: stat.size,
					maxBytes: item.maxBytes,
				});
			}
		} catch {
			report.files.push({ ...item, ok: false });
			pushFailure(report, 'missing-file', `${item.file} is missing`);
		}
	}
}

function checkPayload(report, payload) {
	if (payload.schema !== 'nadlan-project-showroom-payload/v1') {
		pushFailure(report, 'payload-schema', 'Payload schema marker is missing or wrong', { schema: payload.schema });
	}
	if (payload.project_slug !== 'ashira-sde-dov') {
		pushFailure(report, 'payload-project', 'Payload project slug is not Ashira', { project_slug: payload.project_slug });
	}
	const meta = payload.meta || {};
	for (const field of REQUIRED_META_FIELDS) {
		if (!(field in meta)) pushFailure(report, 'missing-meta', `Missing required meta field: ${field}`);
	}
	const units = Array.isArray(meta.project_3d_units) ? meta.project_3d_units : [];
	report.payload = {
		project_slug: payload.project_slug,
		meta_fields: Object.keys(meta).length,
		units: units.length,
		statuses: [...new Set(units.map((unit) => unit.status))],
	};
	if (units.length < 3) pushFailure(report, 'unit-count', `Expected at least 3 units, got ${units.length}`);
	if (!units.some((unit) => unit.status === 'available')) {
		pushFailure(report, 'no-available-unit', 'At least one selectable apartment must be available');
	}
	units.forEach((unit, index) => {
		for (const field of UNIT_REQUIRED_FIELDS) {
			if (unit[field] === undefined || unit[field] === '') {
				pushFailure(report, 'missing-unit-field', `Unit ${index} missing ${field}`, { id: unit.id || '' });
			}
		}
		if (!ALLOWED_STATUSES.has(unit.status)) {
			pushFailure(report, 'invalid-status', `Unit ${index} has invalid status`, { id: unit.id, status: unit.status });
		}
		for (const field of ['stage_x', 'stage_y']) {
			const n = Number(unit[field]);
			if (!Number.isFinite(n) || n < 0 || n > 100) {
				pushFailure(report, 'bad-stage-coordinate', `Unit ${index} ${field} must be 0-100`, { id: unit.id, value: unit[field] });
			}
		}
		checkCopy(report, `payload unit ${unit.id || index}`, [
			unit.title,
			unit.availability,
			unit.view,
			unit.price_estimate,
			unit.price_note,
			unit.source_note,
			unit.view_note,
		].filter(Boolean).join(' '), { requireHebrew: true });
	});

	const publicStrings = [];
	collectPublicPayloadStrings(meta, publicStrings);
	report.payload_public_string_count = publicStrings.length;
	for (const item of publicStrings) {
		checkCopy(report, `payload.${item.path}`, item.text);
	}
}

function extractPreviewUnitIds(source) {
	const ids = new Set();
	const re = /data-unit-id="([^"]+)"/g;
	let match;
	while ((match = re.exec(source))) {
		ids.add(match[1]);
	}
	return [...ids];
}

async function checkSourceCopy(report) {
	const sources = [
		{ file: 'patterns/project-showroom-ashira-v2.php', visible: true },
		{ file: 'docs/previews/ashira-showroom-v2-preview.html', visible: true },
		{ file: 'assets/js/nadlan-showroom-v2.js', visible: false },
	];
	for (const source of sources) {
		const text = await readText(source.file);
		const target = source.visible ? stripVisibleText(text) : text;
		checkCopy(report, source.file, target, { requireHebrew: true });
	}
}

async function checkPreviewPayloadSync(report, payload) {
	const preview = await readText('docs/previews/ashira-showroom-v2-preview.html');
	const previewIds = extractPreviewUnitIds(preview);
	const payloadIds = new Set((payload.meta?.project_3d_units || []).map((unit) => unit.id));
	const missingFromPayload = previewIds.filter((id) => !payloadIds.has(id));
	const missingFromPreview = [...payloadIds].filter((id) => !previewIds.includes(id));
	report.preview_payload_sync = {
		preview_units: previewIds.length,
		payload_units: payloadIds.size,
		missing_from_payload: missingFromPayload,
		missing_from_preview: missingFromPreview,
	};
	if (missingFromPayload.length) {
		pushFailure(report, 'preview-payload-sync', 'Preview has clickable cells missing from payload', { ids: missingFromPayload });
	}
	if (missingFromPreview.length) {
		pushFailure(report, 'payload-preview-sync', 'Payload has units missing from the preview facade', { ids: missingFromPreview });
	}
}

async function checkScreenshotReport(report, file) {
	let screenshot;
	try {
		screenshot = await readJson(file);
	} catch {
		pushFailure(report, 'missing-screenshot-report', `${file} is missing or invalid`);
		return;
	}
	const viewports = Array.isArray(screenshot.viewports) ? screenshot.viewports : [];
	report.screenshot_report = {
		file,
		viewports: viewports.length,
		failures: Array.isArray(screenshot.failures) ? screenshot.failures.length : null,
	};
	if (Array.isArray(screenshot.failures) && screenshot.failures.length) {
		pushFailure(report, 'screenshot-failures', 'Latest screenshot gate has failures', { failures: screenshot.failures });
	}
	if (viewports.length < 4) {
		pushFailure(report, 'screenshot-viewports', `Expected 4 screenshot viewports, got ${viewports.length}`);
	}
	for (const view of viewports) {
		const m = view.metrics || {};
		if ((m.scroll?.overflow || 0) > 1) pushFailure(report, 'screenshot-overflow', `${view.name} has horizontal overflow`);
		if (m.h1Count !== 1) pushFailure(report, 'screenshot-h1', `${view.name} does not have one H1`, { h1Count: m.h1Count });
		if (m.copy?.hasInternalWords) pushFailure(report, 'screenshot-internal-copy', `${view.name} leaks internal wording`);
		if (m.copy?.hasMojibake) pushFailure(report, 'screenshot-mojibake', `${view.name} has visible mojibake`);
		if ((m.units?.minTapWidth || 0) < 44 || (m.units?.minTapHeight || 0) < 44) {
			pushFailure(report, 'screenshot-tap-target', `${view.name} has tap targets below 44px`, {
				minTapWidth: m.units?.minTapWidth,
				minTapHeight: m.units?.minTapHeight,
			});
		}
	}
}

async function main() {
	const args = parseArgs(process.argv);
	const report = {
		generated_at: new Date().toISOString(),
		check: 'ashira-v2-factory-readiness',
		payload_file: args.payload,
		failures: [],
		files: [],
	};

	await checkFiles(report);
	const payload = await readJson(args.payload);
	checkPayload(report, payload);
	await checkSourceCopy(report);
	await checkPreviewPayloadSync(report, payload);
	await checkScreenshotReport(report, args.screenshotReport);

	report.ok = report.failures.length === 0;
	await fs.mkdir(path.dirname(path.resolve(process.cwd(), args.out)), { recursive: true });
	await fs.writeFile(path.resolve(process.cwd(), args.out), `${JSON.stringify(report, null, 2)}\n`, 'utf8');

	console.log(JSON.stringify({
		ok: report.ok,
		out: path.resolve(process.cwd(), args.out),
		files: report.files.length,
		units: report.payload?.units || 0,
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
