#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PATTERN = 'patterns/project-showroom-ashira-v2.php';
const DRAFT = 'docs/wp-drafts/ashira-sde-dov-v2-draft.json';
const OUT = 'docs/qa/ashira-content-depth-report.json';

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
	return String(text || '').match(/[\u0590-\u05ffA-Za-z0-9][\u0590-\u05ffA-Za-z0-9"'׳״-]*/g) || [];
}

const pattern = read(PATTERN);
const draft = JSON.parse(read(DRAFT));
const draftContent = draft.body?.content || '';
const visible = stripHtml(draftContent);
const links = [...draftContent.matchAll(/https:\/\/[^\s"')<>]+/g)].map((m) => m[0]);
const h2Count = [...draftContent.matchAll(/<h2(\s|>)/gi)].length;
const failures = [];
const banned = /(SEO|CMS|CRM|lead|leads|engine|template|prototype|project manager|supplier|contractor|internal|strategy|factory|fallback|placeholder|mock|monetization|פאנל|מנוע|תבנית|לידים|משפך|מוניטיז|אסטרטג|מקום שמור|פרויקטים לבדיקה|Codex|Claude)/i;
const requiredPhrases = [
	'אשירה שדה דב',
	'רובע שדה דב',
	'אביסרור',
	'תא/4444',
	'16,000',
	'1,300',
	'דיור בר-השגה',
	'רידינג',
	'פארק הירקון',
	'קונים מחו"ל',
	'אומדן לא מחייב',
];

if (!pattern.includes('מקורות ובדיקת אמינות')) failures.push('pattern missing sources section');
if (words(visible).length < 3000) failures.push(`visible word count below 3000: ${words(visible).length}`);
if (h2Count < 12) failures.push(`expected at least 12 H2 headings, got ${h2Count}`);
if (links.length < 3) failures.push(`expected at least 3 source links, got ${links.length}`);
for (const phrase of requiredPhrases) {
	if (!visible.includes(phrase)) failures.push(`missing required buyer/source phrase: ${phrase}`);
}
if (banned.test(visible)) failures.push(`visible text leaks internal wording: ${visible.match(banned)?.[0]}`);
if (/[\u00c3\u00c2\ufffd]|\u00d7[\u0080-\u00ff]|\u00c2\u00b7|\u00c3\u0097/.test(visible)) failures.push('visible text contains mojibake markers');

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
