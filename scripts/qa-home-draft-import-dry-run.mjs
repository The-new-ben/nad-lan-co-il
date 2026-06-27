#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import path from 'node:path';

const ROOT = process.cwd();
const MANIFEST = 'docs/plans/2026-06-27-homepage-publication-manifest.json';
const OUT = 'docs/qa/home-draft-import-dry-run-report.json';
const THEME_URL = 'https://nad-lan.co.il/wp-content/themes/nadlan-revenue/';
const PROJECTS_URL = `${THEME_URL}assets/engine/projects.json`;

function resolve(file) {
	return path.resolve(ROOT, file);
}

function readJson(file) {
	return JSON.parse(readFileSync(resolve(file), 'utf8'));
}

function stripAnsi(source) {
	return String(source || '').replace(/\u001b\[[0-9;]*m/g, '');
}

function parseApplyOutput(stdout) {
	const text = stripAnsi(stdout).trim();
	const first = text.indexOf('{');
	const last = text.lastIndexOf('}');
	if (first === -1 || last === -1 || last < first) {
		throw new Error(`No JSON object in apply output: ${text.slice(0, 400)}`);
	}
	return JSON.parse(text.slice(first, last + 1));
}

function stripTags(html) {
	return html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
		.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
		.replace(/<[^>]*>/g, ' ');
}

function addFailure(failures, name, details = '') {
	failures.push({ name, details });
}

function extractBlockPattern(source, file) {
	const start = source.indexOf('<!-- wp:html -->');
	const endMarker = '<!-- /wp:html -->';
	const end = source.indexOf(endMarker);
	if (start === -1 || end === -1 || end <= start) {
		throw new Error(`Could not find bounded wp:html block in ${file}`);
	}
	return source.slice(start, end + endMarker.length);
}

function expectedContentFromPattern(patternFile) {
	return extractBlockPattern(readFileSync(resolve(patternFile), 'utf8'), patternFile)
		.replace(/<\?php\s+echo\s+esc_url\(\s*\$projects_js\s*\);\s*\?>/g, PROJECTS_URL)
		.replace(/<\?php\s+echo\s+esc_url\(\s*\$theme_uri\s*\);\s*\?>/g, THEME_URL);
}

function sha256(value) {
	return createHash('sha256').update(value).digest('hex');
}

const manifest = readJson(MANIFEST);
const failures = [];
const draft = manifest.draft || {};
const draftPath = manifest.draft_payload || '';
let expectedContent = '';

if (manifest.status !== 'draft_preflight_only') addFailure(failures, 'manifest_not_preflight', manifest.status || '');
if (!draftPath) addFailure(failures, 'missing_draft_payload');
if (!draft.endpoint || !draft.slug) addFailure(failures, 'missing_manifest_draft_contract');
try {
	expectedContent = expectedContentFromPattern(manifest.pattern);
} catch (error) {
	addFailure(failures, 'pattern_extract_failed', error.message);
}

let payload = {};
let output = {};
let result = { status: 1, stderr: 'payload not executed' };

if (draftPath) {
	payload = readJson(draftPath);
	result = spawnSync(process.execPath, [
		'scripts/apply-wp-draft-payload.mjs',
		'--payload',
		draftPath,
		'--dry-run',
	], {
		cwd: ROOT,
		encoding: 'utf8',
		shell: false,
		env: {
			...process.env,
			WP_USER: '',
			WP_APP_PASSWORD: '',
		},
	});

	try {
		output = parseApplyOutput(result.stdout);
	} catch (error) {
		addFailure(failures, 'dry_run_output_not_json', error.message);
	}
}

const body = payload.body || {};
const content = String(body.content || '');
const visibleContent = stripTags(content);
const meta = body.meta || {};
const publicInternalWords = /(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה)/i;

if (result.status !== 0) addFailure(failures, 'dry_run_exit_nonzero', result.stderr || String(result.status));
if (output.mode !== 'dry-run') addFailure(failures, 'not_dry_run', output.mode || '');
if (output.status !== 'draft') addFailure(failures, 'status_not_draft', output.status || '');
if ((output.method || '').toUpperCase() !== 'POST') addFailure(failures, 'method_not_post', output.method || '');
if (output.endpoint !== draft.endpoint) addFailure(failures, 'endpoint_mismatch', `${output.endpoint || ''} != ${draft.endpoint || ''}`);
if (output.slug !== draft.slug) addFailure(failures, 'slug_mismatch', `${output.slug || ''} != ${draft.slug || ''}`);
if ((output.content_chars || 0) < 8000) addFailure(failures, 'content_too_short_for_homepage_import', String(output.content_chars || 0));
if ((output.meta_fields || 0) < 4) addFailure(failures, 'missing_meta_fields', String(output.meta_fields || 0));
if (result.stderr && result.stderr.trim()) addFailure(failures, 'dry_run_stderr', result.stderr.trim().slice(0, 500));

if (payload.endpoint !== draft.endpoint) addFailure(failures, 'payload_endpoint_mismatch', `${payload.endpoint || ''} != ${draft.endpoint || ''}`);
if (body.status !== 'draft') addFailure(failures, 'payload_status_not_draft', body.status || '');
if (body.slug !== draft.slug) addFailure(failures, 'payload_slug_mismatch', `${body.slug || ''} != ${draft.slug || ''}`);
if (!content.includes('data-nle-home-showroom')) addFailure(failures, 'missing_home_showroom_marker');
if (!content.includes('https://nad-lan.co.il/wp-content/themes/nadlan-revenue/assets/engine/projects.json')) addFailure(failures, 'missing_public_projects_json_url');
if (!content.includes('https://nad-lan.co.il/wp-content/themes/nadlan-revenue/')) addFailure(failures, 'missing_public_theme_asset_base');
if (/<\?php|get_template_directory_uri|trailingslashit/.test(content)) addFailure(failures, 'payload_contains_theme_php');
if (expectedContent && content !== expectedContent) addFailure(failures, 'payload_pattern_parity_mismatch', `payload=${content.length} expected=${expectedContent.length}`);
if (publicInternalWords.test(visibleContent)) addFailure(failures, 'visible_public_copy_has_internal_words');
if (/[\u00c2\u00c3]/.test(JSON.stringify(body))) addFailure(failures, 'payload_contains_mojibake_markers');
if (!meta._yoast_wpseo_title || !meta._yoast_wpseo_metadesc || !meta._yoast_wpseo_focuskw) addFailure(failures, 'missing_yoast_meta');

const report = {
	ok: failures.length === 0,
	manifest: MANIFEST,
	draft_payload: draftPath,
	mode: 'dry-run-only',
	pattern_parity: {
		pattern: manifest.pattern || '',
		ok: Boolean(expectedContent && content === expectedContent),
		payload_sha256: sha256(content),
		expected_sha256: sha256(expectedContent),
	},
	import: {
		exit_code: result.status,
		mode: output.mode || '',
		endpoint: output.endpoint || payload.endpoint || '',
		method: output.method || payload.method || '',
		status: output.status || body.status || '',
		slug: output.slug || body.slug || '',
		title: output.title || body.title || '',
		content_chars: output.content_chars || content.length,
		meta_fields: output.meta_fields || Object.keys(meta).length,
	},
	failures,
};

mkdirSync(path.dirname(resolve(OUT)), { recursive: true });
writeFileSync(resolve(OUT), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures: failures.length, out: OUT }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
