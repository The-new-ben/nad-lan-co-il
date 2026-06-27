#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DEFAULT_MANIFEST = 'docs/plans/2026-06-27-ashira-publication-manifest.json';
const DEFAULT_OUT = 'docs/qa/project-publication-readiness-report.json';

function argValue(name, fallback) {
	const index = process.argv.indexOf(name);
	if (index === -1) return fallback;
	const value = process.argv[index + 1];
	return value && !value.startsWith('--') ? value : fallback;
}

const MANIFEST = argValue('--manifest', DEFAULT_MANIFEST);
const OUT = argValue('--out', DEFAULT_OUT);

function resolve(file) {
	return path.resolve(ROOT, file);
}

function readJson(file) {
	return JSON.parse(readFileSync(resolve(file), 'utf8'));
}

function countMatches(text, re) {
	return [...String(text || '').matchAll(re)].length;
}

function stripHtml(source) {
	return String(source || '')
		.replace(/<script[\s\S]*?<\/script>/gi, ' ')
		.replace(/<style[\s\S]*?<\/style>/gi, ' ')
		.replace(/<!--[\s\S]*?-->/g, ' ')
		.replace(/<[^>]+>/g, ' ')
		.replace(/\s+/g, ' ')
		.trim();
}

function addFailure(failures, lang, name, details = '') {
	failures.push({ lang, name, details });
}

const manifest = readJson(MANIFEST);
const failures = [];
const languages = manifest.languages || [];
const slugs = new Set();
const urls = new Set();
const langs = new Set(languages.map((entry) => entry.lang));
const expectedLangs = Array.isArray(manifest.required_languages) ? manifest.required_languages : [];
const requiredSourceLinks = Array.isArray(manifest.required_source_links) ? manifest.required_source_links : [];

if (manifest.status !== 'draft_preflight_only') {
	addFailure(failures, 'manifest', 'status_not_preflight', manifest.status);
}
if (manifest.wordpress_type && manifest.wordpress_type !== 'nadlan_project') {
	addFailure(failures, 'manifest', 'wordpress_type_mismatch', manifest.wordpress_type);
}
if (!manifest.endpoint || !manifest.endpoint.includes('/wp-json/wp/v2/nadlan_project')) {
	addFailure(failures, 'manifest', 'endpoint_mismatch', manifest.endpoint || '');
}
if (manifest.public_base_path !== '/projects/') {
	addFailure(failures, 'manifest', 'public_base_path_mismatch', manifest.public_base_path);
}
if (!manifest.site || !/^https:\/\/[^/]+$/.test(manifest.site)) {
	addFailure(failures, 'manifest', 'site_mismatch', manifest.site || '');
}
if (!manifest.asset_slug || !existsSync(resolve(`assets/projects/${manifest.asset_slug}`))) {
	addFailure(failures, 'manifest', 'missing_asset_folder', manifest.asset_slug || '');
}
for (const lang of expectedLangs) {
	if (!langs.has(lang)) addFailure(failures, lang, 'missing_language');
}
if (!manifest.x_default || !langs.has(manifest.x_default)) {
	addFailure(failures, 'manifest', 'x_default_missing_from_languages', manifest.x_default || '');
}
if ((manifest.localized_version_sources || []).length < 3) {
	addFailure(failures, 'manifest', 'missing_i18n_sources');
}

for (const entry of languages) {
	const lang = entry.lang || 'unknown';
	for (const key of ['pattern', 'draft', 'preview', 'content_report', 'screenshot_report']) {
		if (!entry[key] || !existsSync(resolve(entry[key]))) {
			addFailure(failures, lang, `missing_${key}`, entry[key] || '');
		}
	}
	if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(entry.slug || '')) {
		addFailure(failures, lang, 'non_ascii_slug', entry.slug || '');
	}
	if (slugs.has(entry.slug)) addFailure(failures, lang, 'duplicate_slug', entry.slug);
	slugs.add(entry.slug);

	const expectedUrl = `${manifest.site}${manifest.public_base_path}${entry.slug}/`;
	if (entry.public_url !== expectedUrl) {
		addFailure(failures, lang, 'public_url_mismatch', `${entry.public_url} != ${expectedUrl}`);
	}
	if (!entry.public_url?.includes('/projects/')) {
		addFailure(failures, lang, 'public_url_not_project_path', entry.public_url || '');
	}
	if (urls.has(entry.public_url)) addFailure(failures, lang, 'duplicate_public_url', entry.public_url);
	urls.add(entry.public_url);

	if (!existsSync(resolve(entry.draft))) continue;
	const draft = readJson(entry.draft);
	const body = draft.body || {};
	const content = String(body.content || '');
	const visible = stripHtml(content);
	const meta = body.meta || {};

	if (draft.endpoint !== manifest.endpoint) addFailure(failures, lang, 'draft_endpoint_mismatch', draft.endpoint || '');
	if (body.status !== 'draft') addFailure(failures, lang, 'draft_status_not_draft', body.status || '');
	if (body.slug !== entry.slug) addFailure(failures, lang, 'draft_slug_mismatch', `${body.slug} != ${entry.slug}`);
	for (const key of ['_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw']) {
		if (!String(meta[key] || '').trim()) addFailure(failures, lang, `missing_${key}`);
	}
	if (countMatches(content, /<h1[\s>]/gi) !== 1) addFailure(failures, lang, 'h1_count_not_one', String(countMatches(content, /<h1[\s>]/gi)));
	if (countMatches(content, /<h2[\s>]/gi) < 12) addFailure(failures, lang, 'h2_count_below_12', String(countMatches(content, /<h2[\s>]/gi)));
	if (!content.includes('data-nlv2-showroom')) addFailure(failures, lang, 'missing_showroom_root');
	if (!content.includes('<model-viewer')) addFailure(failures, lang, 'missing_model_viewer');
	if (countMatches(content, /data-nlv2-unit/g) < 5) addFailure(failures, lang, 'unit_count_below_5', String(countMatches(content, /data-nlv2-unit/g)));
	for (const source of requiredSourceLinks) {
		if (!content.includes(source)) addFailure(failures, lang, 'missing_source_link', source);
	}
	const assetSlugMatches = [...content.matchAll(/\/wp-content\/themes\/nadlan-revenue\/assets\/projects\/([^/]+)\//g)].map((match) => match[1]);
	for (const assetSlug of assetSlugMatches) {
		if (assetSlug !== manifest.asset_slug) addFailure(failures, lang, 'asset_slug_drift', assetSlug);
	}
	if (/SEO|CMS|CRM|lead panel|funnel|monetization|paid placement|Codex|Claude/i.test(visible)) {
		addFailure(failures, lang, 'public_copy_internal_word');
	}

	if (!existsSync(resolve(entry.content_report))) continue;
	const contentReport = readJson(entry.content_report);
	if (!contentReport.ok) addFailure(failures, lang, 'content_report_not_ok', JSON.stringify(contentReport.failures || []));
	if ((contentReport.visible_words || 0) < 3000) addFailure(failures, lang, 'content_words_below_3000', String(contentReport.visible_words || 0));

	if (!existsSync(resolve(entry.screenshot_report))) continue;
	const screenshotReport = readJson(entry.screenshot_report);
	if ((screenshotReport.failures || []).length) {
		addFailure(failures, lang, 'screenshot_report_failures', JSON.stringify(screenshotReport.failures));
	}
	for (const viewport of screenshotReport.viewports || []) {
		const metrics = viewport.metrics || {};
		if (metrics.lang !== lang) addFailure(failures, lang, 'screenshot_lang_mismatch', `${viewport.name}: ${metrics.lang}`);
		if (metrics.dir !== entry.dir) addFailure(failures, lang, 'screenshot_dir_mismatch', `${viewport.name}: ${metrics.dir}`);
		if (metrics.h1Count !== 1) addFailure(failures, lang, 'screenshot_h1_count_not_one', `${viewport.name}: ${metrics.h1Count}`);
		if ((metrics.scroll?.overflow || 0) > 0) addFailure(failures, lang, 'screenshot_horizontal_overflow', `${viewport.name}: ${metrics.scroll?.overflow}`);
		if ((metrics.units?.minTapHeight || 0) < 44 || (metrics.units?.minTapWidth || 0) < 44) {
			addFailure(failures, lang, 'tap_target_below_44', `${viewport.name}: ${metrics.units?.minTapWidth}x${metrics.units?.minTapHeight}`);
		}
		if (metrics.overlap?.cardOverFacade) addFailure(failures, lang, 'card_over_facade', viewport.name);
		if (!metrics.modelViewer?.defined || metrics.modelViewer?.count !== 1) {
			addFailure(failures, lang, 'model_viewer_not_ready', viewport.name);
		}
	}
}

const hreflang = Object.fromEntries(languages.map((entry) => [entry.lang, entry.public_url]));
hreflang['x-default'] = languages.find((entry) => entry.lang === manifest.x_default)?.public_url || '';
const report = {
	ok: failures.length === 0,
	manifest: MANIFEST,
	status: manifest.status,
	language_count: languages.length,
	hreflang,
	failures,
};

mkdirSync(path.dirname(resolve(OUT)), { recursive: true });
writeFileSync(resolve(OUT), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures: failures.length, out: OUT, language_count: languages.length }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
