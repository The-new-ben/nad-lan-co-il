#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

function parseArgs(argv) {
	const args = {
		pattern: 'patterns/project-showroom-ashira-v2.php',
		out: 'docs/previews/ashira-showroom-v2-preview.html',
		lang: 'he',
		dir: 'rtl',
		title: 'דירות למכירה באשירה שדה דב | NadLan',
		navLabel: 'ניווט',
		nav: ['פרויקטים', 'שכונות', 'מדריכים', 'אנשי מקצוע', 'צור קשר'],
		footer: [
			['NadLan', 'פרויקטים חדשים, שכונות, מדריכים וכלי בדיקה לקונים ומשקיעים.'],
			['מסלולים', 'קנייה | השקעה | משכנתא | אנשי מקצוע'],
			['הערה', 'המידע בדף ההמחשה אינו ייעוץ משפטי, פיננסי או שמאי.'],
		],
	};
	for (let i = 2; i < argv.length; i += 1) {
		const arg = argv[i];
		if (arg === '--pattern') args.pattern = argv[++i] || args.pattern;
		else if (arg === '--out') args.out = argv[++i] || args.out;
		else if (arg === '--lang') args.lang = argv[++i] || args.lang;
		else if (arg === '--dir') args.dir = argv[++i] || args.dir;
		else if (arg === '--title') args.title = argv[++i] || args.title;
		else if (arg === '--nav-label') args.navLabel = argv[++i] || args.navLabel;
		else if (arg === '--nav') args.nav = (argv[++i] || '').split('|').filter(Boolean);
		else if (arg === '--footer') {
			args.footer = (argv[++i] || '')
				.split('|')
				.filter(Boolean)
				.map((item) => {
					const parts = item.split('::');
					return [parts[0] || 'NadLan', parts.slice(1).join('::') || ''];
				});
		} else if (arg === '--help' || arg === '-h') {
			console.log('Usage: node scripts/build-ashira-showroom-preview.mjs --pattern patterns/project-showroom-ashira-v2.php --out docs/previews/ashira-showroom-v2-preview.html --lang he --dir rtl --title "..."');
			process.exit(0);
		} else {
			throw new Error(`Unknown argument: ${arg}`);
		}
	}
	return args;
}

function extractWpHtml(source) {
	const start = source.indexOf('<!-- wp:html -->');
	const endMarker = '<!-- /wp:html -->';
	const end = source.indexOf(endMarker);
	if (start < 0 || end < 0 || end <= start) {
		throw new Error('Pattern is missing wp:html markers');
	}
	return source.slice(start + '<!-- wp:html -->'.length, end).trim();
}

function localizePatternHtml(html) {
	return html
		.replace(/<\?php echo esc_url\( \$asset_base \. '([^']+)' \); \?>/g, '../../assets/projects/ashira-sde-dov/$1')
		.replace(/<\?php echo esc_url\( rest_url\( 'nadlan\/v1\/lead' \) \); \?>/g, '#lead-endpoint');
}

const args = parseArgs(process.argv);
const pattern = readFileSync(path.resolve(ROOT, args.pattern), 'utf8');
const main = localizePatternHtml(extractWpHtml(pattern));
const nav = args.nav.map((item) => `<a href="#">${item}</a>`).join('\n\t\t\t');
const footer = args.footer.map(([title, body]) => `<div><strong>${title}</strong><br>${body}</div>`).join('\n\t\t');

const html = `<!doctype html>
<html lang="${args.lang}" dir="${args.dir}">
<head>
\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>${args.title}</title>
\t<link rel="icon" href="data:,">
\t<link rel="preconnect" href="https://fonts.googleapis.com">
\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
\t<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800;900&family=Frank+Ruhl+Libre:wght@700;900&display=swap" rel="stylesheet">
\t<link rel="stylesheet" href="../../assets/css/nadlan-showroom-v2.css">
\t<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js"></script>
</head>
<body class="nlv2-site-shell">
\t<header class="nlv2-site-header">
\t\t<a class="nlv2-brand" href="#">NadLan</a>
\t\t<nav class="nlv2-nav" aria-label="${args.navLabel}">
\t\t\t${nav}
\t\t</nav>
\t</header>

\t${main}

\t<footer class="nlv2-site-footer">
\t\t${footer}
\t</footer>
\t<script src="../../assets/js/nadlan-showroom-v2.js"></script>
</body>
</html>
`;

mkdirSync(path.dirname(path.resolve(ROOT, args.out)), { recursive: true });
writeFileSync(path.resolve(ROOT, args.out), html, 'utf8');
console.log(JSON.stringify({ ok: true, out: args.out, chars: html.length }, null, 2));
