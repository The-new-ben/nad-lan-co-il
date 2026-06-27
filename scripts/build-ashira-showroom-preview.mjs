#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PATTERN = 'patterns/project-showroom-ashira-v2.php';
const OUT = 'docs/previews/ashira-showroom-v2-preview.html';

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

const pattern = readFileSync(path.resolve(ROOT, PATTERN), 'utf8');
const main = localizePatternHtml(extractWpHtml(pattern));
const html = `<!doctype html>
<html lang="he" dir="rtl">
<head>
\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>דירות למכירה באשירה שדה דב | NadLan</title>
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
\t\t<nav class="nlv2-nav" aria-label="ניווט">
\t\t\t<a href="#">פרויקטים</a>
\t\t\t<a href="#">שכונות</a>
\t\t\t<a href="#">מדריכים</a>
\t\t\t<a href="#">אנשי מקצוע</a>
\t\t\t<a href="#">צור קשר</a>
\t\t</nav>
\t</header>

\t${main}

\t<footer class="nlv2-site-footer">
\t\t<div><strong>NadLan</strong><br>פרויקטים חדשים, שכונות, מדריכים וכלי בדיקה לקונים ומשקיעים.</div>
\t\t<div><strong>מסלולים</strong><br>קנייה | השקעה | משכנתא | אנשי מקצוע</div>
\t\t<div><strong>הערה</strong><br>המידע בדף ההמחשה אינו ייעוץ משפטי, פיננסי או שמאי.</div>
\t</footer>
\t<script src="../../assets/js/nadlan-showroom-v2.js"></script>
</body>
</html>
`;

mkdirSync(path.dirname(path.resolve(ROOT, OUT)), { recursive: true });
writeFileSync(path.resolve(ROOT, OUT), html, 'utf8');
console.log(JSON.stringify({ ok: true, out: OUT, chars: html.length }, null, 2));
