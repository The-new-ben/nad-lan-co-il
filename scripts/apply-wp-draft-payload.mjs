import fs from 'node:fs/promises';

function usage() {
	return `Usage:
  node scripts/apply-wp-draft-payload.mjs --payload docs/wp-drafts/dimri-yama-project-draft.json --dry-run
  WP_USER=<user> WP_APP_PASSWORD=<app-password> node scripts/apply-wp-draft-payload.mjs --payload docs/wp-drafts/dimri-yama-project-draft.json --apply

Creates a WordPress draft from a prepared REST payload.
Default mode is dry-run. It never publishes; it posts the payload status exactly as stored.`;
}

function parseArgs(argv) {
	const args = { payload: '', apply: false, dryRun: true };
	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === '--payload') args.payload = argv[++i] || '';
		else if (arg === '--apply') {
			args.apply = true;
			args.dryRun = false;
		} else if (arg === '--dry-run') {
			args.apply = false;
			args.dryRun = true;
		} else if (arg === '--help' || arg === '-h') {
			console.log(usage());
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}
	if (!args.payload) throw new Error('Missing --payload');
	return args;
}

function validatePayload(payload) {
	const errors = [];
	const content = String(payload.body?.content || '');
	const supportedMarkers = [
		'data-nlps-showroom',
		'data-nlv2-showroom',
		'data-nle-home-showroom',
	];
	if (!payload || typeof payload !== 'object') errors.push('payload must be an object');
	if (!/^https:\/\/nad-lan\.co\.il\/wp-json\/wp\/v2\//.test(payload.endpoint || '')) {
		errors.push('endpoint must be a nad-lan.co.il WordPress REST create endpoint');
	}
	if ((payload.method || '').toUpperCase() !== 'POST') errors.push('method must be POST');
	if (!payload.body || typeof payload.body !== 'object') errors.push('body is required');
	if (payload.body && payload.body.status !== 'draft') errors.push('body.status must stay draft');
	if (payload.body && !payload.body.slug) errors.push('body.slug is required');
	if (payload.body && !payload.body.title) errors.push('body.title is required');
	if (payload.body && !supportedMarkers.some((marker) => content.includes(marker))) {
		errors.push('content is missing a supported showroom root marker');
	}
	if (payload.body && /[\u00c2\u00c3]/.test(JSON.stringify(payload.body))) {
		errors.push('body contains mojibake markers');
	}
	if (errors.length) throw new Error(`Invalid payload:\n${errors.map((e) => `- ${e}`).join('\n')}`);
}

function authHeader() {
	const user = process.env.WP_USER || '';
	const appPassword = process.env.WP_APP_PASSWORD || '';
	if (!user || !appPassword) {
		throw new Error('WP_USER and WP_APP_PASSWORD are required for --apply');
	}
	return `Basic ${Buffer.from(`${user}:${appPassword}`).toString('base64')}`;
}

const args = parseArgs(process.argv);
const payload = JSON.parse(await fs.readFile(args.payload, 'utf8'));
validatePayload(payload);

if (args.dryRun) {
	console.log(JSON.stringify({
		ok: true,
		mode: 'dry-run',
		endpoint: payload.endpoint,
		method: payload.method,
		status: payload.body.status,
		slug: payload.body.slug,
		title: payload.body.title,
		content_chars: String(payload.body.content || '').length,
		meta_fields: Object.keys(payload.body.meta || {}).length,
	}, null, 2));
	process.exit(0);
}

const response = await fetch(payload.endpoint, {
	method: 'POST',
	headers: {
		Authorization: authHeader(),
		'Content-Type': 'application/json',
		Accept: 'application/json',
	},
	body: JSON.stringify(payload.body),
});

const text = await response.text();
let data;
try {
	data = JSON.parse(text);
} catch {
	data = { raw: text };
}

if (!response.ok) {
	console.error(JSON.stringify({ ok: false, status: response.status, data }, null, 2));
	process.exit(1);
}

console.log(JSON.stringify({
	ok: true,
	status: response.status,
	id: data.id,
	slug: data.slug,
	link: data.link,
	status_text: data.status,
}, null, 2));
