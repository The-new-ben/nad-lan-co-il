#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DEFAULT_MANIFEST = 'docs/plans/2026-06-27-ashira-publication-manifest.json';
const DEFAULT_OUT_JSON = 'docs/seo/ashira-hreflang-map.json';
const DEFAULT_OUT_HTML = 'docs/seo/ashira-hreflang-head.html';

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

function escapeAttr(value) {
	return String(value)
		.replace(/&/g, '&amp;')
		.replace(/"/g, '&quot;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;');
}

const manifestFile = argValue('--manifest', DEFAULT_MANIFEST);
const outJson = argValue('--out-json', DEFAULT_OUT_JSON);
const outHtml = argValue('--out-html', DEFAULT_OUT_HTML);
const manifest = readJson(manifestFile);
const languages = manifest.languages || [];
const defaultEntry = languages.find((entry) => entry.lang === manifest.x_default) || languages[0];

if (!languages.length) {
	throw new Error('Manifest has no languages');
}
if (!defaultEntry) {
	throw new Error('Manifest has no x-default language entry');
}

const alternates = languages.map((entry) => ({
	hreflang: entry.lang,
	locale: entry.locale || entry.lang,
	dir: entry.dir || '',
	href: entry.public_url,
	slug: entry.slug,
}));

alternates.push({
	hreflang: 'x-default',
	locale: '',
	dir: defaultEntry.dir || '',
	href: defaultEntry.public_url,
	slug: defaultEntry.slug,
});

const html = [
	'<!-- NadLan project localized-page preflight. Add to <head> only after every URL below is live and verified. -->',
	...alternates.map((entry) => `<link rel="alternate" hreflang="${escapeAttr(entry.hreflang)}" href="${escapeAttr(entry.href)}" />`),
	'',
].join('\n');

const map = {
	status: manifest.status,
	manifest: manifestFile,
	method: 'html_head_preflight',
	project_asset_slug: manifest.asset_slug,
	x_default: manifest.x_default,
	alternates,
	publish_rule: 'Do not emit these tags live until every target URL is published, indexable and verified with screenshot/content QA.',
	sources: [...new Set([
		'https://developers.google.com/search/docs/specialty/international/localized-versions',
		...(manifest.localized_version_sources || []),
	])],
};

mkdirSync(path.dirname(resolve(outJson)), { recursive: true });
mkdirSync(path.dirname(resolve(outHtml)), { recursive: true });
writeFileSync(resolve(outJson), `${JSON.stringify(map, null, 2)}\n`, 'utf8');
writeFileSync(resolve(outHtml), html, 'utf8');

console.log(JSON.stringify({
	ok: true,
	manifest: manifestFile,
	out_json: outJson,
	out_html: outHtml,
	alternates: alternates.length,
}, null, 2));
