#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DOC = 'docs/plans/2026-06-27-ashira-multilingual-architecture.md';
const OUT = 'docs/qa/ashira-i18n-architecture-report.json';

function read(file) {
	return readFileSync(path.resolve(ROOT, file), 'utf8');
}

function countMatches(text, re) {
	return [...text.matchAll(re)].length;
}

const text = read(DOC);
const requiredSlugs = [
	'ashira-sde-dov',
	'ashira-sde-dov-en',
	'ashira-sde-dov-fr',
	'ashira-sde-dov-ru',
	'ashira-sde-dov-ar',
];
const requiredHreflang = ['hreflang="he"', 'hreflang="en"', 'hreflang="fr"', 'hreflang="ru"', 'hreflang="ar"', 'hreflang="x-default"'];
const checks = [
	{ name: 'preflight_only', ok: /preflight only/i.test(text) && /Do not publish/i.test(text) },
	{ name: 'no_broad_plugin_migration', ok: /do not install a sitewide multilingual plugin/i.test(text) },
	{ name: 'ascii_slugs', ok: requiredSlugs.every((slug) => text.includes(`\`${slug}\``) && /^[a-z0-9-]+$/.test(slug)) },
	{ name: 'five_languages', ok: ['Hebrew', 'English', 'French', 'Russian', 'Arabic'].every((label) => text.includes(label)) },
	{ name: 'hreflang_complete_set', ok: requiredHreflang.every((item) => text.includes(item)) },
	{ name: 'hreflang_sources', ok: text.includes('https://developers.google.com/search/docs/specialty/international/localized-versions') && text.includes('https://yoast.com/hreflang-ultimate-guide/') },
	{ name: 'wordpress_source', ok: text.includes('https://www.liquidweb.com/wordpress/seo/add-hreflang-tags/') },
	{ name: 'javascript_seo_source', ok: text.includes('https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics') },
	{ name: 'content_depth_per_language', ok: /3,000\+ visible words/i.test(text) },
	{ name: 'source_facts', ok: ['TA/4444', '16,000', '1,300', '40,000'].every((item) => text.includes(item)) },
	{ name: 'screenshot_gate', ok: /desktop, tablet, mobile and Edge-mobile/i.test(text) },
	{ name: 'no_fake_language_promises', ok: /No fake language promises/i.test(text) && /No auto-translation without review/i.test(text) },
	{ name: 'links', ok: countMatches(text, /https:\/\/[^\s)]+/g) >= 4 },
];

const failures = checks.filter((check) => !check.ok).map((check) => check.name);
const report = {
	ok: failures.length === 0,
	document: DOC,
	links: countMatches(text, /https:\/\/[^\s)]+/g),
	slugs: requiredSlugs,
	checks,
	failures,
};

mkdirSync(path.dirname(path.resolve(ROOT, OUT)), { recursive: true });
writeFileSync(path.resolve(ROOT, OUT), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures, out: OUT, links: report.links, slugs: report.slugs.length }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
