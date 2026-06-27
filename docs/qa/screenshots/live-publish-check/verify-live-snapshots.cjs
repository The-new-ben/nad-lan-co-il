const fs = require('fs');
const pages = [
  ['home', 'docs/qa/screenshots/live-publish-check/home-after-publish.html'],
  ['ashira-he', 'docs/qa/screenshots/live-publish-check/ashira-he-after-publish.html'],
  ['ashira-en', 'docs/qa/screenshots/live-publish-check/ashira-en-after-publish.html'],
  ['ashira-fr', 'docs/qa/screenshots/live-publish-check/ashira-fr-after-publish.html'],
  ['ashira-ru', 'docs/qa/screenshots/live-publish-check/ashira-ru-after-publish.html'],
  ['ashira-ar', 'docs/qa/screenshots/live-publish-check/ashira-ar-after-publish.html'],
];
const out = [];
for (const [page, file] of pages) {
  const html = fs.readFileSync(file, 'utf8');
  const h1Matches = html.match(/<h1\b/gi) || [];
  out.push({
    page,
    bytes: html.length,
    homeMarker: html.includes('data-nle-home-showroom'),
    projectMarker: html.includes('data-nlps-showroom') || html.includes('data-nlv2-showroom'),
    ashira: /Ashira|ASHIRA|אשירה|أشيرا|Ашира/i.test(html),
    codeLeak: /class=\"?nlpf dl|<\?php|Warning:|Fatal error/i.test(html),
    h1s: h1Matches.length,
  });
}
console.log(JSON.stringify(out, null, 2));
if (out.some((item) => item.codeLeak)) process.exit(2);
