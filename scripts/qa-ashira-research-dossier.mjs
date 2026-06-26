#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DOC = 'docs/research/2026-06-27-ashira-serp-source-dossier.md';
const OUT = 'docs/qa/ashira-research-dossier-report.json';

function read(file) {
	return readFileSync(path.resolve(ROOT, file), 'utf8');
}

function countMatches(text, re) {
	return [...text.matchAll(re)].length;
}

const text = read(DOC);
const checks = [
	{ name: 'has_length', ok: text.length > 7000 },
	{ name: 'source_links', ok: countMatches(text, /https:\/\/[^\s)]+/g) >= 10 },
	{ name: 'preflight_only', ok: /preflight only/i.test(text) && /not public copy/i.test(text) },
	{ name: 'languages', ok: ['Hebrew', 'English', 'French', 'Russian', 'Arabic'].every((label) => text.includes(`### ${label}`)) },
	{ name: 'asset_truth_table', ok: text.includes('## Asset Truth Table') },
	{ name: 'official_project_source', ok: text.includes('https://ashirabyavisror.com/') },
	{ name: 'municipal_source', ok: text.includes('https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx') },
	{ name: 'hreflang_source', ok: text.includes('https://developers.google.com/search/docs/specialty/international/localized-versions') },
	{ name: 'javascript_seo_source', ok: text.includes('https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics') },
	{ name: 'model_sources', ok: text.includes('https://modelviewer.dev/docs/') && text.includes('https://github.com/xeokit/xeokit-bim-viewer') },
	{ name: 'glb_reality', ok: /per-apartment meshes|precise GLB hotspot data|separate apartment\/floor meshes/i.test(text) },
	{ name: 'no_publish_instruction', ok: !/publish now|deploy now|upload now|activate now/i.test(text) },
	{ name: 'readiness_checklist', ok: countMatches(text, /^- \[ \]/gm) >= 10 },
];

const failures = checks.filter((check) => !check.ok).map((check) => check.name);
const report = {
	ok: failures.length === 0,
	document: DOC,
	links: countMatches(text, /https:\/\/[^\s)]+/g),
	characters: text.length,
	checks,
	failures,
};

mkdirSync(path.dirname(path.resolve(ROOT, OUT)), { recursive: true });
writeFileSync(path.resolve(ROOT, OUT), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures, out: OUT, links: report.links }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
