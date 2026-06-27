#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const OUT = 'docs/qa/home-seo-schema-report.json';

function textOf(file) {
	return readFileSync(path.resolve(ROOT, file), 'utf8');
}

function between(text, start, end) {
	const i = text.indexOf(start);
	if (i === -1) return '';
	const j = text.indexOf(end, i + start.length);
	return j === -1 ? text.slice(i + start.length) : text.slice(i + start.length, j);
}

function metaDescription(html) {
	const match = html.match(/<meta\s+[^>]*name=["']description["'][^>]*content=["']([^"']+)["'][^>]*>/i)
		|| html.match(/<meta\s+[^>]*content=["']([^"']+)["'][^>]*name=["']description["'][^>]*>/i);
	return match ? match[1] : '';
}

function schemaTypes(schema) {
	const out = [];
	const visit = (node) => {
		if (!node || typeof node !== 'object') return;
		if (node['@type']) out.push(node['@type']);
		if (Array.isArray(node['@graph'])) node['@graph'].forEach(visit);
		if (Array.isArray(node.itemListElement)) node.itemListElement.forEach(visit);
		if (node.potentialAction) visit(node.potentialAction);
	};
	visit(schema);
	return [...new Set(out.flat().filter(Boolean))];
}

function publicClean(text) {
	return !/(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|נדל״ן חכם|נדלן חכם|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה)/i.test(text);
}

const functions = textOf('functions.php');
const preview = textOf('docs/previews/nadlan-home-showroom-preview.html');
const pattern = textOf('patterns/nadlan-home-showroom.php');
const title = between(preview, '<title>', '</title>').trim();
const description = metaDescription(preview);
const schemaRaw = between(preview, '<script type="application/ld+json" id="nadlan-home-schema">', '</script>').trim();
let schema = null;
let schemaParseError = '';
try {
	schema = JSON.parse(schemaRaw);
} catch (error) {
	schemaParseError = error.message;
}
const types = schema ? schemaTypes(schema) : [];
const itemList = schema?.['@graph']?.find((node) => node['@type'] === 'ItemList');

const checks = [
	{ name: 'theme_has_title_helper', ok: functions.includes('function nadlan_revenue_home_seo_title()') },
	{ name: 'theme_has_description_helper', ok: functions.includes('function nadlan_revenue_home_seo_description()') },
	{ name: 'theme_has_jsonld_hook', ok: functions.includes("add_action( 'wp_head', 'nadlan_revenue_home_jsonld', 20 )") },
	{ name: 'theme_jsonld_uses_wp_json_encode', ok: functions.includes('wp_json_encode( $schema') },
	{ name: 'old_brand_absent_from_home_sources', ok: !/(נדל״ן חכם|נדלן חכם)/.test(functions + preview + pattern) },
	{ name: 'preview_title_present', ok: title.length >= 30 && title.length <= 70 && /דירות|פרויקטים/.test(title) && title.includes('NadLan') },
	{ name: 'preview_description_present', ok: description.length >= 110 && description.length <= 170 && /מחיר|אומדן|זמינות|דירות|פרויקטים/.test(description) },
	{ name: 'metadata_public_clean', ok: publicClean(`${title} ${description}`) },
	{ name: 'schema_parses', ok: !!schema && !schemaParseError },
	{ name: 'schema_has_organization', ok: types.includes('Organization') },
	{ name: 'schema_has_website', ok: types.includes('WebSite') },
	{ name: 'schema_has_webpage', ok: types.includes('WebPage') },
	{ name: 'schema_has_search_action', ok: types.includes('SearchAction') },
	{ name: 'schema_has_project_item_list', ok: types.includes('ItemList') && Array.isArray(itemList?.itemListElement) && itemList.itemListElement.length >= 3 },
	{ name: 'schema_public_clean', ok: publicClean(schemaRaw) }
];

const failures = checks.filter((check) => !check.ok).map((check) => check.name);
const report = {
	ok: failures.length === 0,
	out: OUT,
	title,
	title_length: title.length,
	description,
	description_length: description.length,
	schema_types: types,
	item_list_count: Array.isArray(itemList?.itemListElement) ? itemList.itemListElement.length : 0,
	schema_parse_error: schemaParseError,
	checks,
	failures
};

mkdirSync(path.dirname(path.resolve(ROOT, OUT)), { recursive: true });
writeFileSync(path.resolve(ROOT, OUT), JSON.stringify(report, null, 2), 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures, out: OUT }, null, 2));

if (process.argv.includes('--strict') && failures.length) process.exitCode = 1;
