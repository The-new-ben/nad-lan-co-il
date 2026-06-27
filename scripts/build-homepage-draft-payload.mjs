#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PATTERN = 'patterns/nadlan-home-showroom.php';
const OUT = 'docs/wp-drafts/nadlan-home-showroom-v2-draft.json';
const THEME_URL = 'https://nad-lan.co.il/wp-content/themes/nadlan-revenue/';
const PROJECTS_URL = `${THEME_URL}assets/engine/projects.json`;

function resolve(file) {
	return path.resolve(ROOT, file);
}

function extractBlockPattern(source) {
	const start = source.indexOf('<!-- wp:html -->');
	const endMarker = '<!-- /wp:html -->';
	const end = source.indexOf(endMarker);
	if (start === -1 || end === -1 || end <= start) {
		throw new Error(`Could not find bounded wp:html block in ${PATTERN}`);
	}
	return source.slice(start, end + endMarker.length);
}

const pattern = readFileSync(resolve(PATTERN), 'utf8');
const content = extractBlockPattern(pattern)
	.replace(/<\?php\s+echo\s+esc_url\(\s*\$projects_js\s*\);\s*\?>/g, PROJECTS_URL)
	.replace(/<\?php\s+echo\s+esc_url\(\s*\$theme_uri\s*\);\s*\?>/g, THEME_URL);

if (content.includes('<?php') || content.includes('get_template_directory_uri') || content.includes('trailingslashit')) {
	throw new Error('Homepage draft payload still contains PHP/theme-only code');
}
if (!content.includes('data-nle-home-showroom')) {
	throw new Error('Homepage draft payload is missing data-nle-home-showroom');
}
if (!content.includes(PROJECTS_URL) || !content.includes(THEME_URL)) {
	throw new Error('Homepage draft payload is missing resolved public asset URLs');
}

const payload = {
	endpoint: 'https://nad-lan.co.il/wp-json/wp/v2/pages',
	method: 'POST',
	body: {
		status: 'draft',
		slug: 'nadlan-home-showroom-v2',
		title: 'NadLan | Compare New Projects and Apartments in Israel',
		content,
		comment_status: 'closed',
		ping_status: 'closed',
		meta: {
			_yoast_wpseo_title: 'NadLan | New Projects and Apartments in Israel',
			_yoast_wpseo_metadesc: 'Compare new apartments in Israel by project, floor, view, non-binding estimate and buyer path, with multilingual entry points for investors from Israel and abroad.',
			_yoast_wpseo_focuskw: 'new apartments in Israel',
			_yoast_wpseo_is_cornerstone: '1',
		},
	},
	notes: [
		'Create as a draft page only. Do not publish and do not set as the front page until screenshot QA, live preview QA, header/footer QA and owner approval pass.',
		'This payload is generated from patterns/nadlan-home-showroom.php so the homepage stays theme-first and does not duplicate plugin presentation logic.',
		'The payload resolves theme PHP asset URLs into public URLs because WordPress page content cannot execute PHP.',
	],
};

mkdirSync(path.dirname(resolve(OUT)), { recursive: true });
writeFileSync(resolve(OUT), `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({
	ok: true,
	out: OUT,
	status: payload.body.status,
	slug: payload.body.slug,
	content_chars: payload.body.content.length,
	meta_fields: Object.keys(payload.body.meta).length,
}, null, 2));
