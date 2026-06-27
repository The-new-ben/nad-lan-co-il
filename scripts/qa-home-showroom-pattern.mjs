#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PATTERN = 'patterns/nadlan-home-showroom.php';
const OUT = 'docs/qa/home-showroom-pattern-report.json';

function textOf(file) {
	return readFileSync(path.resolve(ROOT, file), 'utf8');
}

function count(haystack, needle) {
	return haystack.split(needle).length - 1;
}

const pattern = textOf(PATTERN);
const publicBlock = pattern.split('<!-- wp:html -->')[1]?.split('<!-- /wp:html -->')[0] || pattern;
const visibleBlock = publicBlock.replace(/<[^>]*>/g, ' ');
const projectEngineStart = pattern.indexOf('class="nle-catalog nlh-home-project-engine"');
const languageStart = projectEngineStart === -1 ? -1 : pattern.indexOf('class="nlh-home-languages"', projectEngineStart);
const catalogHeadStart = projectEngineStart === -1 ? -1 : pattern.indexOf('class="nle-catalog-head"', projectEngineStart);
const functions = textOf('functions.php');
const homeTemplate = textOf('templates/home.html');
const engineJs = textOf('assets/js/nadlan-showroom-engine.js');
const homeCss = textOf('assets/css/nadlan-home-showroom.css');
const ashiraManifest = JSON.parse(textOf('docs/plans/2026-06-27-ashira-publication-manifest.json'));
const ashiraLanguageTargets = Object.fromEntries(
	ashiraManifest.languages.map((item) => [item.lang, new URL(item.public_url).pathname])
);
const languageRailLinksOk = Object.entries(ashiraLanguageTargets).every(([lang, pathname]) => {
	const expected = `href="${pathname}" data-nle-lang="${lang}"`;
	return pattern.includes(expected);
});

const checks = [
	{ name: 'pattern_marker', ok: pattern.includes('data-nle-home-showroom') },
	{ name: 'home_template_uses_pattern', ok: homeTemplate.includes('nadlan-revenue/nadlan-home-showroom') },
	{ name: 'home_template_drops_query_loop', ok: !homeTemplate.includes('template-query-loop') && !homeTemplate.includes('hidden-blog-heading') },
	{ name: 'project_data_url', ok: pattern.includes('assets/engine/projects.json') },
	{ name: 'asset_base_url', ok: pattern.includes('data-nle-asset-base') },
	{ name: 'one_h1', ok: count(pattern, '<h1 ') === 1 },
	{ name: 'project_grid', ok: pattern.includes('data-nle-project-grid') },
	{ name: 'project_language_rail', ok: pattern.includes('nlh-project-language-rail') && ['data-nle-lang="he"', 'data-nle-lang="en"', 'data-nle-lang="fr"', 'data-nle-lang="ru"', 'data-nle-lang="ar"'].every((value) => pattern.includes(value)) },
	{ name: 'project_language_rail_links_manifest_urls', ok: languageRailLinksOk },
	{ name: 'home_language_controls_inside_project_engine', ok: projectEngineStart !== -1 && languageStart > projectEngineStart && catalogHeadStart > languageStart },
	{ name: 'hero_language_controls', ok: ['data-nle-home-text="hero_eyebrow"', 'data-nle-home-text="hero_title"', 'data-nle-home-text="hero_lead"', 'data-nle-home-value="area_value"', 'data-nle-home-aria="area_aria"'].every((value) => pattern.includes(value)) },
	{ name: 'project_band_buyer_copy', ok: pattern.includes('השוואת פרויקטים חדשים לפי דירה, נוף ואומדן') && !pattern.includes('אזור הבחירה המרכזי של דף הבית') },
	{ name: 'model_mount', ok: pattern.includes('data-nle-model-wrap') },
	{ name: 'facade_mount', ok: pattern.includes('data-nle-facade-grid') },
	{ name: 'language_entries', ok: ['English', 'Français', 'Русский', 'العربية'].every((value) => pattern.includes(value)) && pattern.includes('nlh-home-languages') && pattern.includes('data-nle-lang="ar"') },
	{ name: 'language_targets', ok: ['id="english"', 'id="french"', 'id="russian"', 'id="arabic"'].every((value) => pattern.includes(value)) },
	{ name: 'buyer_path_cards', ok: count(pattern, '<article') >= 12 && pattern.includes('nlh-home-paths') && pattern.includes('מה כדאי לבדוק בכל פרויקט חדש') },
	{ name: 'public_buyer_copy', ok: /דירה|דירות|פרויקט|פרויקטים|מחיר|אומדן|זמינות/.test(pattern) },
	{ name: 'home_css_has_mobile_rules', ok: homeCss.includes('@media (max-width: 560px)') },
	{ name: 'functions_detects_marker', ok: functions.includes("data-nle-home-showroom") },
	{ name: 'functions_detects_home_template', ok: functions.includes("templates/home.html") && functions.includes("template_has_home") },
	{ name: 'functions_enqueues_engine_css', ok: functions.includes("assets/css/nadlan-showroom-engine.css") },
	{ name: 'functions_enqueues_home_css', ok: functions.includes("assets/css/nadlan-home-showroom.css") },
	{ name: 'functions_enqueues_engine_js', ok: functions.includes("assets/js/nadlan-showroom-engine.js") },
	{ name: 'engine_reads_root_config', ok: engineJs.includes('data-nle-home-showroom') && engineJs.includes('dataset.nleProjects') && engineJs.includes('dataset.nleAssetBase') },
	{ name: 'engine_switches_language', ok: engineJs.includes('data-nle-lang') && engineJs.includes('setLanguage') && engineJs.includes('applyLanguageChrome') && engineJs.includes('applyHomeLanguageChrome') && engineJs.includes('homeCopy') },
	{ name: 'no_public_internal_words', ok: !/(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה)/i.test(visibleBlock) }
];

const failures = checks.filter((check) => !check.ok).map((check) => check.name);
const report = {
	ok: failures.length === 0,
	pattern: PATTERN,
	out: OUT,
	checks,
	failures
};

mkdirSync(path.dirname(path.resolve(ROOT, OUT)), { recursive: true });
writeFileSync(path.resolve(ROOT, OUT), JSON.stringify(report, null, 2), 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures, out: OUT }, null, 2));

if (process.argv.includes('--strict') && failures.length) process.exitCode = 1;
