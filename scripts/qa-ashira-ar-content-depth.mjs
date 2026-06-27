#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PATTERN = 'patterns/project-showroom-ashira-v2-ar.php';
const DRAFT = 'docs/wp-drafts/ashira-sde-dov-ar-v2-draft.json';
const OUT = 'docs/qa/ashira-ar-content-depth-report.json';

function read(file) {
	return readFileSync(path.resolve(ROOT, file), 'utf8');
}

function stripHtml(source) {
	return String(source || '')
		.replace(/<script[\s\S]*?<\/script>/gi, ' ')
		.replace(/<style[\s\S]*?<\/style>/gi, ' ')
		.replace(/<\?php[\s\S]*?\?>/g, ' ')
		.replace(/<!--[\s\S]*?-->/g, ' ')
		.replace(/<[^>]+>/g, ' ')
		.replace(/&nbsp;/g, ' ')
		.replace(/&quot;/g, '"')
		.replace(/&#039;/g, "'")
		.replace(/&amp;/g, '&')
		.replace(/\s+/g, ' ')
		.trim();
}

function words(text) {
	return String(text || '').match(/[A-Za-z\u0600-\u06FF0-9][A-Za-z\u0600-\u06FF0-9"'.-]*/g) || [];
}

const pattern = read(PATTERN);
const draft = JSON.parse(read(DRAFT));
const draftContent = draft.body?.content || '';
const visible = stripHtml(draftContent);
const links = [...draftContent.matchAll(/https:\/\/[^\s"')<>]+/g)].map((m) => m[0]);
const h2Count = [...draftContent.matchAll(/<h2(\s|>)/gi)].length;
const failures = [];
const banned = /(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|Codex|Claude|قالب|نموذج أولي|مصنع|قمع|ليد|ليدات|مونيتايز|مورد)/i;
const requiredPhrases = [
	'Ashira Sde Dov',
	'Sde Dov',
	'Avisror',
	'TA/4444',
	'16,000',
	'1,300',
	'40,000',
	'السكن الميسر',
	'ريدينغ',
	'Park Hayarkon',
	'المشتري من الخارج',
	'تقدير غير ملزم',
];

if (!pattern.includes('مصادر وملاحظات موثوقية')) failures.push('pattern missing Arabic sources section');
if (words(visible).length < 3000) failures.push(`visible word count below 3000: ${words(visible).length}`);
if (h2Count < 12) failures.push(`expected at least 12 H2 headings, got ${h2Count}`);
if (links.length < 4) failures.push(`expected at least 4 source links, got ${links.length}`);
for (const phrase of requiredPhrases) {
	if (!visible.includes(phrase)) failures.push(`missing required buyer/source phrase: ${phrase}`);
}
if (banned.test(visible)) failures.push(`visible text leaks internal wording: ${visible.match(banned)?.[0]}`);
if (/[\u00c3\u00c2\ufffd]|\u00d7[\u0080-\u00ff]|\u00c2\u00b7|\u00c3\u0097/.test(visible)) failures.push('visible text contains mojibake markers');
if (/[\u0590-\u05ff]/.test(visible)) failures.push('Arabic page visible text contains Hebrew characters');
if (!/[\u0600-\u06FF]/.test(visible)) failures.push('Arabic page visible text contains no Arabic text');

const report = {
	ok: failures.length === 0,
	pattern: PATTERN,
	draft: DRAFT,
	visible_words: words(visible).length,
	visible_chars: visible.length,
	h2_count: h2Count,
	source_links: links,
	required_phrases: requiredPhrases,
	failures,
};

mkdirSync(path.dirname(path.resolve(ROOT, OUT)), { recursive: true });
writeFileSync(path.resolve(ROOT, OUT), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ ok: report.ok, failures, out: OUT, words: report.visible_words, h2: h2Count, links: links.length }, null, 2));

if (process.argv.includes('--strict') && failures.length) {
	process.exitCode = 1;
}
