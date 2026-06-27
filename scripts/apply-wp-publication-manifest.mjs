#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

function usage() {
	return `Usage:
  node scripts/apply-wp-publication-manifest.mjs --manifest docs/plans/2026-06-27-ashira-publication-manifest.json --dry-run
  WP_USER=<user> WP_APP_PASSWORD=<app-password> node scripts/apply-wp-publication-manifest.mjs --manifest docs/plans/2026-06-27-ashira-publication-manifest.json --apply
  WP_USER=<user> WP_APP_PASSWORD=<app-password> node scripts/apply-wp-publication-manifest.mjs --manifest docs/plans/2026-06-27-ashira-publication-manifest.json --apply --status publish --confirm-publish

Safely upserts prepared WordPress REST payloads from a publication manifest.
Default mode is dry-run. Existing posts are matched by slug before writing, so apply mode updates
instead of blindly creating duplicates. Publishing requires --status publish and --confirm-publish.`;
}

function parseArgs(argv) {
	const args = {
		manifest: '',
		apply: false,
		dryRun: true,
		status: 'draft',
		confirmPublish: false,
	};

	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === '--manifest') args.manifest = argv[++i] || '';
		else if (arg === '--apply') {
			args.apply = true;
			args.dryRun = false;
		} else if (arg === '--dry-run') {
			args.apply = false;
			args.dryRun = true;
		} else if (arg === '--status') args.status = argv[++i] || '';
		else if (arg === '--confirm-publish') args.confirmPublish = true;
		else if (arg === '--help' || arg === '-h') {
			console.log(usage());
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}

	if (!args.manifest) throw new Error('Missing --manifest');
	if (!['draft', 'publish'].includes(args.status)) throw new Error('--status must be draft or publish');
	if (args.status === 'publish' && !args.confirmPublish) {
		throw new Error('Publishing requires --confirm-publish');
	}
	return args;
}

function resolveFile(file) {
	return path.resolve(ROOT, file);
}

function readJson(file) {
	return JSON.parse(readFileSync(resolveFile(file), 'utf8'));
}

function sha256(value) {
	return createHash('sha256').update(String(value || '')).digest('hex');
}

function payloadEntries(manifestFile, manifest) {
	if (Array.isArray(manifest.languages)) {
		return manifest.languages.map((entry) => ({
			key: entry.lang || entry.slug || entry.draft,
			lang: entry.lang || '',
			slug: entry.slug || '',
			public_url: entry.public_url || '',
			draft: entry.draft || '',
			kind: manifest.wordpress_type || 'nadlan_project',
		}));
	}

	if (manifest.draft_payload) {
		return [{
			key: manifest.page || path.basename(manifestFile, '.json'),
			lang: manifest.x_default || '',
			slug: manifest.draft?.slug || '',
			public_url: manifest.site || '',
			draft: manifest.draft_payload,
			kind: 'page',
		}];
	}

	throw new Error('Manifest must contain languages[] or draft_payload');
}

function validatePayload(payload, expectedSlug = '') {
	const errors = [];
	const content = String(payload.body?.content || '');
	const supportedMarkers = [
		'data-nlps-showroom',
		'data-nlv2-showroom',
		'data-nle-home-showroom',
	];

	if (!payload || typeof payload !== 'object') errors.push('payload must be an object');
	if (!/^https:\/\/nad-lan\.co\.il\/wp-json\/wp\/v2\//.test(payload.endpoint || '')) {
		errors.push('endpoint must be a nad-lan.co.il WordPress REST endpoint');
	}
	if ((payload.method || '').toUpperCase() !== 'POST') errors.push('method must be POST');
	if (!payload.body || typeof payload.body !== 'object') errors.push('body is required');
	if (payload.body && !payload.body.slug) errors.push('body.slug is required');
	if (expectedSlug && payload.body?.slug !== expectedSlug) {
		errors.push(`payload slug ${payload.body?.slug || ''} does not match manifest slug ${expectedSlug}`);
	}
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

function endpointForPost(endpoint, id) {
	return `${String(endpoint || '').replace(/\/+$/, '')}/${id}`;
}

function queryEndpointForSlug(endpoint, slug) {
	const url = new URL(endpoint);
	url.searchParams.set('slug', slug);
	url.searchParams.set('status', 'any');
	url.searchParams.set('context', 'edit');
	url.searchParams.set('_fields', 'id,slug,status,link');
	return url.toString();
}

async function fetchJson(url, options = {}) {
	const response = await fetch(url, options);
	const text = await response.text();
	let data;
	try {
		data = JSON.parse(text);
	} catch {
		data = { raw: text.slice(0, 1000) };
	}
	return { response, data };
}

async function findExisting(payload, auth) {
	const slug = payload.body.slug;
	const { response, data } = await fetchJson(queryEndpointForSlug(payload.endpoint, slug), {
		headers: {
			Authorization: auth,
			Accept: 'application/json',
		},
	});
	if (!response.ok) {
		throw new Error(`Existing-post lookup failed for ${slug}: HTTP ${response.status}`);
	}
	if (!Array.isArray(data)) throw new Error(`Existing-post lookup for ${slug} did not return an array`);
	return data.find((item) => item.slug === slug) || null;
}

async function applyPayload(entry, payload, status, auth) {
	const existing = await findExisting(payload, auth);
	const body = { ...payload.body, status };
	const target = existing ? endpointForPost(payload.endpoint, existing.id) : payload.endpoint;
	const method = 'POST';
	const { response, data } = await fetchJson(target, {
		method,
		headers: {
			Authorization: auth,
			'Content-Type': 'application/json',
			Accept: 'application/json',
		},
		body: JSON.stringify(body),
	});

	if (!response.ok) {
		throw new Error(`Apply failed for ${entry.key || payload.body.slug}: HTTP ${response.status}`);
	}

	return {
		key: entry.key,
		lang: entry.lang,
		action: existing ? 'update' : 'create',
		id: data.id,
		slug: data.slug,
		status: data.status,
		link: data.link,
	};
}

const args = parseArgs(process.argv);
const manifest = readJson(args.manifest);
const entries = payloadEntries(args.manifest, manifest);

const payloads = entries.map((entry) => {
	if (!entry.draft) throw new Error(`Missing draft path for ${entry.key}`);
	const payload = readJson(entry.draft);
	validatePayload(payload, entry.slug);
	return {
		entry,
		payload,
		summary: {
			key: entry.key,
			lang: entry.lang,
			kind: entry.kind,
			endpoint: payload.endpoint,
			slug: payload.body.slug,
			title: payload.body.title,
			source_status: payload.body.status || '',
			target_status: args.status,
			content_chars: String(payload.body.content || '').length,
			meta_fields: Object.keys(payload.body.meta || {}).length,
			content_sha256: sha256(payload.body.content || ''),
		},
	};
});

if (args.dryRun) {
	console.log(JSON.stringify({
		ok: true,
		mode: 'dry-run',
		manifest: args.manifest,
		site: manifest.site || '',
		target_status: args.status,
		count: payloads.length,
		items: payloads.map((item) => item.summary),
	}, null, 2));
	process.exit(0);
}

const auth = authHeader();
const results = [];
for (const item of payloads) {
	results.push(await applyPayload(item.entry, item.payload, args.status, auth));
}

console.log(JSON.stringify({
	ok: true,
	mode: 'apply',
	manifest: args.manifest,
	target_status: args.status,
	count: results.length,
	results,
}, null, 2));
