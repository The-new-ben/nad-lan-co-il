#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const MANIFEST = 'docs/plans/2026-06-27-homepage-publication-manifest.json';
const OUT = 'docs/qa/home-publication-readiness-report.json';

function resolve(file) {
	return path.resolve(ROOT, file);
}

function textOf(file) {
	return readFileSync(resolve(file), 'utf8');
}

function jsonOf(file) {
	return JSON.parse(textOf(file));
}

function stripTags(html) {
	return html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
		.replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
		.replace(/<[^>]*>/g, ' ');
}

function check(list, name, ok, details = {}) {
	list.push({ name, ok: Boolean(ok), ...details });
}

function languagePaths(projectManifest) {
	return Object.fromEntries(projectManifest.languages.map((item) => [
		item.lang,
		new URL(item.public_url).pathname
	]));
}

const checks = [];
const manifest = jsonOf(MANIFEST);
const requiredFiles = [
	MANIFEST,
	manifest.preview,
	manifest.pattern,
	manifest.template,
	manifest.project_publication_manifest,
	...Object.values(manifest.required_reports)
];

for (const file of requiredFiles) {
	check(checks, `file_exists:${file}`, existsSync(resolve(file)));
}

const pattern = textOf(manifest.pattern);
const preview = textOf(manifest.preview);
const template = textOf(manifest.template);
const visiblePattern = stripTags(pattern);
const visiblePreview = stripTags(preview);
const projectManifest = jsonOf(manifest.project_publication_manifest);
const patternReport = jsonOf(manifest.required_reports.pattern);
const screenshotReport = jsonOf(manifest.required_reports.screenshots);
const chromeReport = jsonOf(manifest.required_reports.chrome);
const seoReport = jsonOf(manifest.required_reports.seo_schema);
const draftReport = manifest.required_reports.draft_import_dry_run ? jsonOf(manifest.required_reports.draft_import_dry_run) : null;
const projectPublicationReport = jsonOf(manifest.required_reports.project_publication);
const langPaths = languagePaths(projectManifest);

check(checks, 'manifest_is_draft_only', manifest.status === 'draft_preflight_only');
check(checks, 'home_template_uses_showroom_pattern', template.includes('nadlan-revenue/nadlan-home-showroom'));
check(checks, 'pattern_has_home_marker', pattern.includes('data-nle-home-showroom'));
check(checks, 'preview_has_home_shell', preview.includes('class="nle-page nlh-home"'));
check(checks, 'pattern_report_green', patternReport.ok === true && (!patternReport.failures || patternReport.failures.length === 0));
check(checks, 'screenshot_report_green', screenshotReport.ok === true && (!screenshotReport.failures || screenshotReport.failures.length === 0));
check(checks, 'chrome_report_green', chromeReport.ok === true && (!chromeReport.failures || chromeReport.failures.length === 0));
check(checks, 'seo_schema_report_green', seoReport.ok === true && (!seoReport.failures || seoReport.failures.length === 0));
check(checks, 'draft_import_dry_run_report_green', draftReport && draftReport.ok === true && (!draftReport.failures || draftReport.failures.length === 0));
check(checks, 'draft_payload_manifest_aligned', draftReport && draftReport.draft_payload === manifest.draft_payload);
check(checks, 'draft_payload_pages_endpoint', draftReport && draftReport.import && draftReport.import.endpoint === manifest.draft.endpoint);
check(checks, 'draft_payload_status_draft', draftReport && draftReport.import && draftReport.import.status === 'draft');
check(checks, 'draft_payload_slug_aligned', draftReport && draftReport.import && draftReport.import.slug === manifest.draft.slug);
check(checks, 'draft_payload_has_body', draftReport && draftReport.import && draftReport.import.content_chars >= 8000, {
	content_chars: draftReport?.import?.content_chars || 0
});
check(checks, 'project_publication_report_green', projectPublicationReport.ok === true && (!projectPublicationReport.failures || projectPublicationReport.failures.length === 0));
check(checks, 'project_manifest_has_five_languages', projectManifest.languages.length === 5);
check(checks, 'project_manifest_urls_under_projects', projectManifest.languages.every((item) => new URL(item.public_url).pathname.startsWith('/projects/')));
check(checks, 'pattern_language_links_match_project_manifest', Object.entries(langPaths).every(([lang, href]) => pattern.includes(`href="${href}" data-nle-lang="${lang}"`)), { langPaths });
check(checks, 'preview_language_links_match_project_manifest', Object.entries(langPaths).every(([lang, href]) => preview.includes(`href="${href}" data-nle-lang="${lang}"`)), { langPaths });

const publicInternalWords = /(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה)/i;
check(checks, 'pattern_public_copy_clean', !publicInternalWords.test(visiblePattern));
check(checks, 'preview_public_copy_clean', !publicInternalWords.test(visiblePreview));
check(checks, 'seo_schema_public_clean', Array.isArray(seoReport.checks) && seoReport.checks.some((item) => item.name === 'schema_public_clean' && item.ok));
check(checks, 'chrome_public_clean', chromeReport.checks && Array.isArray(chromeReport.checks.noPublicInternalWords) && chromeReport.checks.noPublicInternalWords.length === 0);

const viewportNames = new Set((screenshotReport.viewports || []).map((item) => item.name));
check(checks, 'required_viewports_present', manifest.required_viewports.every((name) => viewportNames.has(name)), { required: manifest.required_viewports, actual: [...viewportNames] });
for (const viewport of screenshotReport.viewports || []) {
	const before = viewport.before || {};
	check(checks, `viewport:${viewport.name}:one_h1`, Array.isArray(before.h1s) && before.h1s.length === 1);
	check(checks, `viewport:${viewport.name}:project_cards`, before.projectCards >= 3, { projectCards: before.projectCards });
	check(checks, `viewport:${viewport.name}:language_project_targets`, before.languageProjectTargetsOk === true && before.catalogLanguageLinks === projectManifest.languages.length, {
		catalogLanguageLinks: before.catalogLanguageLinks,
		catalogLanguageUrls: before.catalogLanguageUrls
	});
	check(checks, `viewport:${viewport.name}:no_overflow`, before.overflow <= 1, { overflow: before.overflow });
	check(checks, `viewport:${viewport.name}:no_internal_words`, before.hasInternalWords === false);
	check(checks, `viewport:${viewport.name}:no_mojibake`, before.hasMojibake === false);
	check(checks, `viewport:${viewport.name}:model_ready`, before.modelViewerCount === 1 && before.modelViewerDefined === true);
	check(checks, `viewport:${viewport.name}:project_selector_before_showroom`, before.catalog && before.showroom && before.catalog.y < before.showroom.y, {
		catalogY: before.catalog && before.catalog.y,
		showroomY: before.showroom && before.showroom.y
	});
}

const failures = checks.filter((item) => !item.ok);
const report = {
	ok: failures.length === 0,
	manifest: MANIFEST,
	out: OUT,
	language_targets: langPaths,
	checks,
	failures: failures.map((item) => item.name)
};

mkdirSync(path.dirname(resolve(OUT)), { recursive: true });
writeFileSync(resolve(OUT), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures: report.failures.length, out: OUT }, null, 2));

if (process.argv.includes('--strict') && failures.length) process.exitCode = 1;
