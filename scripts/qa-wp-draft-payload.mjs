import fs from 'node:fs/promises';
import path from 'node:path';

const MOJIBAKE_RE = /[\u00c3\u00c2\ufffd]|\u00d7[\u0080-\u00ff]|\u00c2\u00b7|\u00c3\u0097/;
const INTERNAL_RE = /\b(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization)\b|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה/i;

function usage() {
	return `Usage:
  node scripts/qa-wp-draft-payload.mjs --draft docs/wp-drafts/ashira-sde-dov-v2-draft.json --payload assets/projects/ashira-sde-dov/showroom-payload.json --out docs/qa/ashira-v2-draft-readiness-report.json --strict

Validates a prepared WordPress REST draft payload without contacting WordPress. It checks draft
status, supported showroom root, visible buyer copy, SEO meta copy, and optional preview/payload
unit id sync.`;
}

function parseArgs(argv) {
	const args = {
		draft: '',
		payload: '',
		out: '',
		strict: false,
	};
	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === '--draft') args.draft = argv[++i] || '';
		else if (arg === '--payload') args.payload = argv[++i] || '';
		else if (arg === '--out') args.out = argv[++i] || '';
		else if (arg === '--strict') args.strict = true;
		else if (arg === '--help' || arg === '-h') {
			console.log(usage());
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}
	if (!args.draft) throw new Error('Missing --draft');
	return args;
}

async function readJson(file) {
	const text = await fs.readFile(path.resolve(process.cwd(), file), 'utf8');
	return JSON.parse(text.replace(/^\uFEFF/, ''));
}

function stripVisibleText(source) {
	return String(source || '')
		.replace(/<\?php[\s\S]*?\?>/g, ' ')
		.replace(/<script[\s\S]*?<\/script>/gi, ' ')
		.replace(/<style[\s\S]*?<\/style>/gi, ' ')
		.replace(/<!--[\s\S]*?-->/g, ' ')
		.replace(/<[^>]+>/g, ' ')
		.replace(/&nbsp;/g, ' ')
		.replace(/&quot;/g, '"')
		.replace(/&#039;/g, "'")
		.replace(/&amp;/g, '&')
		.replace(/\s+/g, ' ')
		.trim();
}

function pushFailure(report, code, message, details = {}) {
	report.failures.push({ code, message, details });
}

function checkBuyerText(report, label, text, { requireHebrew = true } = {}) {
	const value = String(text || '').trim();
	if (!value) {
		pushFailure(report, 'empty-text', `${label} is empty`);
		return;
	}
	if (requireHebrew && !/[\u0590-\u05ff]/.test(value)) {
		pushFailure(report, 'missing-hebrew', `${label} has no Hebrew buyer-facing text`);
	}
	if (MOJIBAKE_RE.test(value)) {
		pushFailure(report, 'mojibake', `${label} contains mojibake`);
	}
	const internal = value.match(INTERNAL_RE);
	if (internal) {
		pushFailure(report, 'internal-copy', `${label} leaks non-buyer language`, { term: internal[0] });
	}
}

function extractUnitIds(content) {
	const ids = new Set();
	const re = /data-unit-id="([^"]+)"/g;
	let match;
	while ((match = re.exec(content))) {
		ids.add(match[1]);
	}
	return [...ids];
}

function countTag(content, tag) {
	const re = new RegExp(`<${tag}(\\s|>)`, 'gi');
	return [...String(content || '').matchAll(re)].length;
}

function validateDraft(report, draft) {
	const body = draft.body || {};
	const content = String(body.content || body.content?.raw || '');
	const visibleText = stripVisibleText(content);
	report.draft = {
		endpoint: draft.endpoint || '',
		method: draft.method || '',
		status: body.status || '',
		slug: body.slug || '',
		title: body.title || '',
		content_chars: content.length,
		visible_chars: visibleText.length,
		h1_count: countTag(content, 'h1'),
		unit_ids: extractUnitIds(content),
	};

	if (!/^https:\/\/nad-lan\.co\.il\/wp-json\/wp\/v2\//.test(draft.endpoint || '')) {
		pushFailure(report, 'endpoint', 'Draft endpoint must be a NadLan WordPress REST endpoint');
	}
	if (String(draft.method || '').toUpperCase() !== 'POST') {
		pushFailure(report, 'method', 'Draft method must be POST');
	}
	if (body.status !== 'draft') {
		pushFailure(report, 'status', 'Draft payload must stay draft');
	}
	if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(body.slug || '')) {
		pushFailure(report, 'slug', 'Draft slug must be ASCII lowercase words separated by hyphens');
	}
	if (!content.includes('data-nlv2-showroom') && !content.includes('data-nlps-showroom')) {
		pushFailure(report, 'root', 'Draft content is missing a supported showroom root marker');
	}
	if (!content.includes('/wp-json/nadlan/v1/lead')) {
		pushFailure(report, 'lead-endpoint', 'Draft content is missing the shared inquiry endpoint');
	}
	if (report.draft.h1_count !== 1) {
		pushFailure(report, 'h1-count', `Draft content should have exactly one H1, got ${report.draft.h1_count}`);
	}
	if (report.draft.unit_ids.length < 3) {
		pushFailure(report, 'unit-count', `Draft should expose at least 3 clickable apartment cells, got ${report.draft.unit_ids.length}`);
	}
	checkBuyerText(report, 'draft visible text', visibleText);
	checkBuyerText(report, 'draft title', String(body.title || ''));
	const meta = body.meta || {};
	for (const key of ['_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw']) {
		if (meta[key]) checkBuyerText(report, `draft meta ${key}`, String(meta[key]), { requireHebrew: key !== '_yoast_wpseo_focuskw' });
	}
	if (!/דיר|דירות|apartment/i.test(`${visibleText} ${body.title || ''}`)) {
		pushFailure(report, 'buyer-intent', 'Draft copy does not clearly mention apartments');
	}
	if (!/אומדן|מחיר|זמינ|availability|price/i.test(visibleText)) {
		pushFailure(report, 'price-availability-intent', 'Draft copy does not clearly mention estimate, price or availability');
	}
}

async function validatePayloadSync(report, payloadFile, draftUnitIds) {
	if (!payloadFile) return;
	const payload = await readJson(payloadFile);
	const payloadIds = new Set((payload.meta?.project_3d_units || []).map((unit) => unit.id));
	const missingFromPayload = draftUnitIds.filter((id) => !payloadIds.has(id));
	const missingFromDraft = [...payloadIds].filter((id) => !draftUnitIds.includes(id));
	report.payload_sync = {
		payload: payloadFile,
		draft_units: draftUnitIds.length,
		payload_units: payloadIds.size,
		missing_from_payload: missingFromPayload,
		missing_from_draft: missingFromDraft,
	};
	if (missingFromPayload.length) {
		pushFailure(report, 'draft-payload-sync', 'Draft has clickable unit cells missing from payload', { ids: missingFromPayload });
	}
	if (missingFromDraft.length) {
		pushFailure(report, 'payload-draft-sync', 'Payload has units missing from draft content', { ids: missingFromDraft });
	}
}

async function main() {
	const args = parseArgs(process.argv);
	const draft = await readJson(args.draft);
	const report = {
		generated_at: new Date().toISOString(),
		check: 'wp-draft-payload-readiness',
		draft_file: args.draft,
		failures: [],
	};

	validateDraft(report, draft);
	await validatePayloadSync(report, args.payload, report.draft.unit_ids);
	report.ok = report.failures.length === 0;

	if (args.out) {
		await fs.mkdir(path.dirname(path.resolve(process.cwd(), args.out)), { recursive: true });
		await fs.writeFile(path.resolve(process.cwd(), args.out), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
	}

	console.log(JSON.stringify({
		ok: report.ok,
		draft: args.draft,
		out: args.out ? path.resolve(process.cwd(), args.out) : '',
		units: report.draft.unit_ids.length,
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
