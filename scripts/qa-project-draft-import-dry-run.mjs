#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';

const ROOT = process.cwd();
const DEFAULT_MANIFEST = 'docs/plans/2026-06-27-ashira-publication-manifest.json';
const DEFAULT_OUT = 'docs/qa/project-draft-import-dry-run-report.json';

function argValue(name, fallback) {
	const index = process.argv.indexOf(name);
	if (index === -1) return fallback;
	const value = process.argv[index + 1];
	return value && !value.startsWith('--') ? value : fallback;
}

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

function addFailure(failures, lang, name, details = '') {
	failures.push({ lang, name, details });
}

const manifestFile = argValue('--manifest', DEFAULT_MANIFEST);
const outFile = argValue('--out', DEFAULT_OUT);
const manifest = readJson(manifestFile);
const failures = [];
const imports = [];

if (manifest.status !== 'draft_preflight_only') {
	addFailure(failures, 'manifest', 'manifest_not_preflight', manifest.status || '');
}
if (!Array.isArray(manifest.languages) || !manifest.languages.length) {
	addFailure(failures, 'manifest', 'missing_languages');
}

for (const entry of manifest.languages || []) {
	const lang = entry.lang || 'unknown';
	if (!entry.draft) {
		addFailure(failures, lang, 'missing_draft_path');
		continue;
	}
	const payload = readJson(entry.draft);
	const result = spawnSync(process.execPath, [
		'scripts/apply-wp-draft-payload.mjs',
		'--payload',
		entry.draft,
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

	let output = {};
	try {
		output = parseApplyOutput(result.stdout);
	} catch (error) {
		addFailure(failures, lang, 'dry_run_output_not_json', error.message);
	}

	const body = payload.body || {};
	const meta = body.meta || {};
	imports.push({
		lang,
		draft: entry.draft,
		exit_code: result.status,
		mode: output.mode || '',
		endpoint: output.endpoint || payload.endpoint || '',
		method: output.method || payload.method || '',
		status: output.status || body.status || '',
		slug: output.slug || body.slug || '',
		title: output.title || body.title || '',
		content_chars: output.content_chars || String(body.content || '').length,
		meta_fields: output.meta_fields || Object.keys(meta).length,
	});

	if (result.status !== 0) addFailure(failures, lang, 'dry_run_exit_nonzero', result.stderr || String(result.status));
	if (output.mode !== 'dry-run') addFailure(failures, lang, 'not_dry_run', output.mode || '');
	if (output.status !== 'draft') addFailure(failures, lang, 'status_not_draft', output.status || '');
	if ((output.method || '').toUpperCase() !== 'POST') addFailure(failures, lang, 'method_not_post', output.method || '');
	if (output.endpoint !== manifest.endpoint) addFailure(failures, lang, 'endpoint_mismatch', `${output.endpoint || ''} != ${manifest.endpoint || ''}`);
	if (output.slug !== entry.slug) addFailure(failures, lang, 'slug_mismatch', `${output.slug || ''} != ${entry.slug || ''}`);
	if ((output.content_chars || 0) < 15000) addFailure(failures, lang, 'content_too_short_for_import', String(output.content_chars || 0));
	if ((output.meta_fields || 0) < 3) addFailure(failures, lang, 'missing_meta_fields', String(output.meta_fields || 0));
	if (result.stderr && result.stderr.trim()) addFailure(failures, lang, 'dry_run_stderr', result.stderr.trim().slice(0, 500));
}

const report = {
	ok: failures.length === 0,
	manifest: manifestFile,
	mode: 'dry-run-only',
	language_count: (manifest.languages || []).length,
	imports,
	failures,
};

mkdirSync(path.dirname(resolve(outFile)), { recursive: true });
writeFileSync(resolve(outFile), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures: failures.length, out: outFile, language_count: report.language_count }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
