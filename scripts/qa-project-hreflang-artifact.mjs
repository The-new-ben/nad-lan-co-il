#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DEFAULT_MANIFEST = 'docs/plans/2026-06-27-ashira-publication-manifest.json';
const DEFAULT_MAP = 'docs/seo/ashira-hreflang-map.json';
const DEFAULT_HTML = 'docs/seo/ashira-hreflang-head.html';
const DEFAULT_OUT = 'docs/qa/project-hreflang-artifact-report.json';

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

function readText(file) {
	return readFileSync(resolve(file), 'utf8');
}

function attr(tag, name) {
	const match = tag.match(new RegExp(`${name}=["']([^"']+)["']`, 'i'));
	return match ? match[1] : '';
}

function addFailure(failures, name, details = '') {
	failures.push({ name, details });
}

const manifestFile = argValue('--manifest', DEFAULT_MANIFEST);
const mapFile = argValue('--map', DEFAULT_MAP);
const htmlFile = argValue('--html', DEFAULT_HTML);
const outFile = argValue('--out', DEFAULT_OUT);
const failures = [];

for (const file of [manifestFile, mapFile, htmlFile]) {
	if (!existsSync(resolve(file))) addFailure(failures, 'missing_file', file);
}

let manifest = {};
let map = {};
let html = '';

if (!failures.length) {
	manifest = readJson(manifestFile);
	map = readJson(mapFile);
	html = readText(htmlFile);
}

const languages = manifest.languages || [];
const expected = new Map(languages.map((entry) => [entry.lang, entry.public_url]));
expected.set('x-default', languages.find((entry) => entry.lang === manifest.x_default)?.public_url || '');

const htmlAlternates = [...html.matchAll(/<link\s+[^>]*rel=["']alternate["'][^>]*>/gi)].map((match) => ({
	hreflang: attr(match[0], 'hreflang'),
	href: attr(match[0], 'href'),
	tag: match[0],
}));
const mapAlternates = Array.isArray(map.alternates) ? map.alternates : [];

if (manifest.status !== 'draft_preflight_only') {
	addFailure(failures, 'manifest_not_preflight', manifest.status || '');
}
if (map.status !== manifest.status) addFailure(failures, 'map_status_mismatch', `${map.status || ''} != ${manifest.status || ''}`);
if (map.manifest !== manifestFile) addFailure(failures, 'map_manifest_mismatch', `${map.manifest || ''} != ${manifestFile}`);
if (map.method !== 'html_head_preflight') addFailure(failures, 'map_method_mismatch', map.method || '');
if (!manifest.x_default || !expected.get('x-default')) addFailure(failures, 'missing_x_default', manifest.x_default || '');
if ((manifest.localized_version_sources || []).length < 3) addFailure(failures, 'missing_source_basis');

for (const [hreflang, href] of expected) {
	if (!href) addFailure(failures, 'missing_expected_href', hreflang);
	const htmlMatch = htmlAlternates.find((entry) => entry.hreflang === hreflang);
	const mapMatch = mapAlternates.find((entry) => entry.hreflang === hreflang);
	if (!htmlMatch) addFailure(failures, 'missing_html_alternate', hreflang);
	if (!mapMatch) addFailure(failures, 'missing_map_alternate', hreflang);
	if (htmlMatch && htmlMatch.href !== href) addFailure(failures, 'html_href_mismatch', `${hreflang}: ${htmlMatch.href} != ${href}`);
	if (mapMatch && mapMatch.href !== href) addFailure(failures, 'map_href_mismatch', `${hreflang}: ${mapMatch.href} != ${href}`);
}

for (const entry of [...htmlAlternates, ...mapAlternates]) {
	if (!entry.hreflang) addFailure(failures, 'alternate_missing_hreflang', JSON.stringify(entry));
	if (!/^([a-z]{2,3}(?:-[A-Za-z0-9]{2,8})?|x-default)$/.test(entry.hreflang || '')) {
		addFailure(failures, 'invalid_hreflang', entry.hreflang || '');
	}
	if (!/^https:\/\/nad-lan\.co\.il\/projects\/[a-z0-9-]+\/$/.test(entry.href || '')) {
		addFailure(failures, 'invalid_project_url', `${entry.hreflang || ''}: ${entry.href || ''}`);
	}
}

const htmlKeys = htmlAlternates.map((entry) => entry.hreflang);
const mapKeys = mapAlternates.map((entry) => entry.hreflang);
for (const keys of [htmlKeys, mapKeys]) {
	const seen = new Set();
	for (const key of keys) {
		if (seen.has(key)) addFailure(failures, 'duplicate_hreflang', key);
		seen.add(key);
	}
}
if (htmlAlternates.length !== expected.size) addFailure(failures, 'html_alternate_count_mismatch', `${htmlAlternates.length} != ${expected.size}`);
if (mapAlternates.length !== expected.size) addFailure(failures, 'map_alternate_count_mismatch', `${mapAlternates.length} != ${expected.size}`);

const report = {
	ok: failures.length === 0,
	manifest: manifestFile,
	map: mapFile,
	html: htmlFile,
	alternate_count: expected.size,
	hreflangs: [...expected.keys()],
	failures,
};

mkdirSync(path.dirname(resolve(outFile)), { recursive: true });
writeFileSync(resolve(outFile), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures: failures.length, out: outFile, alternate_count: expected.size }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
