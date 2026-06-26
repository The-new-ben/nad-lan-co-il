#!/usr/bin/env node
import { readFileSync, writeFileSync } from 'node:fs';

const files = {
	header: 'patterns/header.php',
	footer: 'patterns/footer.php',
	css: 'assets/css/nadlan-premium-sitewide.css',
	preview: 'docs/previews/nadlan-home-showroom-preview.html'
};

const text = Object.fromEntries(
	Object.entries(files).map(([key, file]) => [key, readFileSync(file, 'utf8')])
);

const defaultThemeWords = [
	'Blog',
	'About',
	'FAQs',
	'Authors',
	'Events',
	'Shop',
	'Patterns',
	'Themes',
	'Designed with',
	'WordPress',
	'NadLan Revenue'
];

const publicInternalWords = [
	'SEO',
	'CMS',
	'CRM',
	'lead',
	'leads',
	'engine',
	'template',
	'prototype',
	'project manager',
	'supplier',
	'contractor',
	'internal',
	'strategy',
	'factory',
	'fallback',
	'placeholder',
	'mock',
	'monetization',
	'פאנל',
	'מנוע',
	'תבנית',
	'לידים',
	'משפך',
	'מוניטיז',
	'אסטרטג',
	'מקום שמור'
];

const report = {
	ok: false,
	files,
	checks: {}
};

function countMatches(haystack, needle) {
	return (haystack.match(new RegExp(needle, 'g')) || []).length;
}

function countAnchors(haystack) {
	return (haystack.match(/<a\b/gi) || []).length;
}

const publicSurface = `${text.header}\n${text.footer}\n${text.preview}`;
const publicText = publicSurface
	.replace(/<script[\s\S]*?<\/script>/gi, ' ')
	.replace(/<style[\s\S]*?<\/style>/gi, ' ')
	.replace(/<[^>]+>/g, ' ');
report.checks.headerRoutes = countAnchors(text.header);
report.checks.headerHasBrand = text.header.includes('NadLan') && text.header.includes('דירות, פרויקטים ושכונות בישראל');
report.checks.headerHasLanguages = ['HE', 'EN', 'FR', 'RU', 'AR'].every((label) => text.header.includes(`>${label}<`));
report.checks.footerLinks = countAnchors(text.footer);
report.checks.footerHasLegal = ['/accessibility/', '/privacy-policy/', '/terms/'].every((url) => text.footer.includes(url));
report.checks.footerHasTrustDisclaimer = text.footer.includes('אינו ייעוץ משפטי') && text.footer.includes('לאמת מחיר');
report.checks.cssHasScopedChrome = ['.nl-site-header', '.nl-site-footer', '.nl-site-nav', '.nl-site-lang'].every((selector) => text.css.includes(selector));
report.checks.cssHasMobileChrome = /@media\(max-width:680px\)[\s\S]*\.nl-site-header/.test(text.css);
report.checks.previewUsesChrome = text.preview.includes('class="nl-site-header"') && text.preview.includes('class="nl-site-footer"');
report.checks.noDefaultThemeWords = defaultThemeWords.filter((word) => publicText.includes(word));
report.checks.noPublicInternalWords = publicInternalWords.filter((word) => publicText.toLowerCase().includes(word.toLowerCase()));
report.checks.noMojibake = !(/Ãƒ|ï¿½|�|Ã—[^\s]*Ã—/.test(publicText));

const failures = [];
if (report.checks.headerRoutes < 15) failures.push(`header/footer combined route count too low: ${report.checks.headerRoutes}`);
if (!report.checks.headerHasBrand) failures.push('header brand/subtitle missing');
if (!report.checks.headerHasLanguages) failures.push('header language entries missing');
if (report.checks.footerLinks < 20) failures.push(`footer link count too low: ${report.checks.footerLinks}`);
if (!report.checks.footerHasLegal) failures.push('footer legal/accessibility links missing');
if (!report.checks.footerHasTrustDisclaimer) failures.push('footer trust disclaimer missing');
if (!report.checks.cssHasScopedChrome) failures.push('scoped chrome CSS missing');
if (!report.checks.cssHasMobileChrome) failures.push('mobile chrome CSS missing');
if (!report.checks.previewUsesChrome) failures.push('preview does not use real chrome classes');
if (report.checks.noDefaultThemeWords.length) failures.push(`default theme words found: ${report.checks.noDefaultThemeWords.join(', ')}`);
if (report.checks.noPublicInternalWords.length) failures.push(`public internal words found: ${report.checks.noPublicInternalWords.join(', ')}`);
if (!report.checks.noMojibake) failures.push('mojibake detected');

report.failures = failures;
report.ok = failures.length === 0;

writeFileSync('docs/qa/home-chrome-report.json', JSON.stringify(report, null, 2), 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
