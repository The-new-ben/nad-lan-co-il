const urls = [
  "https://nad-lan.co.il/professionals/",
  "https://nad-lan.co.il/projects/",
  "https://nad-lan.co.il/properties/",
  "https://nad-lan.co.il/glossary/",
  "https://nad-lan.co.il/real-estate-professionals-guide/",
];

function strip(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function attr(html, selector) {
  const match = html.match(selector);
  return match ? match[1].trim() : "";
}

function snippets(html, tag) {
  return [...html.matchAll(new RegExp(`<${tag}\\b[^>]*>[\\s\\S]*?<\\/${tag}>`, "gi"))]
    .map((match) => match[0].replace(/\s+/g, " ").slice(0, 420));
}

function classHits(html) {
  const classes = [
    "nl-archive-hub",
    "nl-archive-hero",
    "nadlan-archive",
    "nadlan-card",
    "nlfacets",
    "wp-block-query",
    "wp-block-query-title",
    "wp-site-blocks",
    "nadlan-footer",
  ];
  return Object.fromEntries(classes.map((name) => [name, html.includes(name)]));
}

for (const url of urls) {
  const res = await fetch(url, {
    headers: { "User-Agent": "Codex-Nadlan-Archive-Inspector/2026-06-02" },
  });
  const html = await res.text();
  const text = strip(html);
  const title = attr(html, /<title[^>]*>([\s\S]*?)<\/title>/i);
  const canonical = attr(html, /<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)/i);
  const robots = attr(html, /<meta[^>]+name=["']robots["'][^>]+content=["']([^"']+)/i);
  const bodyClass = attr(html, /<body[^>]+class=["']([^"']+)/i);
  const h1Texts = [...html.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)]
    .map((match) => strip(match[1]));
  const archiveWords = ["Archive", "NadLan Projects", "NadLan Properties", "NadLan Professionals", "ארכיון"];

  console.log(JSON.stringify({
    url,
    status: res.status,
    title,
    bodyClass,
    viewport: /<meta[^>]+name=["']viewport["']/i.test(html),
    canonical,
    robots,
    h1Count: h1Texts.length,
    h1Texts,
    h1Snippets: snippets(html, "h1"),
    classHits: classHits(html),
    wordCount: text.split(/\s+/).filter(Boolean).length,
    archiveWordsFound: archiveWords.filter((word) => (title + " " + text).includes(word)),
  }, null, 2));
}
