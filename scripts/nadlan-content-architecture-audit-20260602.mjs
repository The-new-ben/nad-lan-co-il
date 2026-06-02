import fs from "node:fs/promises";
import path from "node:path";

const BASE = "https://nad-lan.co.il";
const OUT = path.resolve("docs/nadlan-content-audit-data-2026-06-02.json");
const MAX_HTML_PER_GROUP = {
  page: 90,
  product: 10,
  nadlan_term: 20,
  nadlan_project: 20,
  nadlan_professional: 20,
  nadlan_professional2: 12,
  nadlan_professional3: 12,
  product_cat: 10,
  nadlan_term_cat: 10,
  "sitemap-nadlan-hubs": 30,
};

const INTERNAL_PUBLIC_RISK_TERMS = [
  "SEO",
  "CRM",
  "UTM",
  "money page",
  "lead routing",
  "paid lead",
  "supplier",
  "Lovable",
  "ChatGPT",
  "Gemini",
  "Codex",
];

function decodeHtml(input = "") {
  return String(input)
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)));
}

function stripTags(html = "") {
  return decodeHtml(
    String(html)
      .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
      .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim()
  );
}

function textOfFirst(html, regex) {
  const match = html.match(regex);
  return match ? stripTags(match[1] || match[0]) : "";
}

function allMatches(html, regex, mapper) {
  return [...html.matchAll(regex)].map(mapper).filter(Boolean);
}

function wordCount(text = "") {
  const cleaned = text.replace(/[^\p{L}\p{N}\s'"\-]/gu, " ");
  return cleaned.split(/\s+/).filter((w) => w.length > 1).length;
}

function pathOf(url) {
  try {
    return new URL(url).pathname;
  } catch {
    return url;
  }
}

function classifyUrl(url) {
  const p = pathOf(url);
  if (p === "/") return "home";
  if (p.includes("/professionals/")) return "professionals";
  if (p.includes("/projects/")) return "projects";
  if (p.includes("/glossary/") || p.includes("/term/")) return "glossary";
  if (p.includes("/mortgage")) return "mortgage";
  if (p.includes("/investment")) return "investment";
  if (p.includes("tax") || p.includes("lawyer") || p.includes("tabu") || p.includes("legal")) return "legal-tax";
  if (p.includes("property-value") || p.includes("prices") || p.includes("price")) return "price-value";
  if (p.includes("urban-renewal") || p.includes("tama") || p.includes("pinui")) return "urban-renewal";
  if (p.includes("buying")) return "buying";
  if (p.includes("selling")) return "selling";
  if (p.includes("commercial-real-estate")) return "commercial";
  return "other";
}

function topTokens(value = "") {
  return stripTags(value)
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s-]/gu, " ")
    .split(/[\s-]+/)
    .filter((token) => token.length > 2)
    .filter((token) => !["https", "nad", "lan", "co", "il", "www", "2026"].includes(token));
}

async function fetchText(url, opts = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), opts.timeoutMs || 25000);
  try {
    const res = await fetch(url, {
      redirect: "follow",
      signal: controller.signal,
      headers: {
        "User-Agent": "Codex-Nadlan-Content-Audit/2026-06-02",
      },
    });
    const text = await res.text();
    return { url, finalUrl: res.url, status: res.status, headers: res.headers, text };
  } catch (error) {
    return { url, finalUrl: url, status: 0, headers: new Map(), text: "", error: String(error.message || error) };
  } finally {
    clearTimeout(timeout);
  }
}

async function mapLimit(items, limit, mapper) {
  const out = new Array(items.length);
  let cursor = 0;
  async function worker() {
    while (cursor < items.length) {
      const index = cursor;
      cursor += 1;
      out[index] = await mapper(items[index], index);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return out;
}

function parseXmlLocs(xml = "") {
  return allMatches(xml, /<loc>([\s\S]*?)<\/loc>/gi, (m) => decodeHtml(m[1]).trim());
}

function analyzeHtml(fetchResult) {
  const html = fetchResult.text || "";
  const clean = stripTags(html);
  const title = textOfFirst(html, /<title[^>]*>([\s\S]*?)<\/title>/i);
  const description = decodeHtml((html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i) || [])[1] || "");
  const robots = decodeHtml((html.match(/<meta[^>]+name=["']robots["'][^>]+content=["']([^"']*)["']/i) || [])[1] || "");
  const canonical = decodeHtml((html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']*)["']/i) || [])[1] || "");
  const h1 = allMatches(html, /<h1\b[^>]*>([\s\S]*?)<\/h1>/gi, (m) => stripTags(m[1]));
  const h2 = allMatches(html, /<h2\b[^>]*>([\s\S]*?)<\/h2>/gi, (m) => stripTags(m[1])).slice(0, 18);
  const hrefs = allMatches(html, /<a\b[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi, (m) => {
    const href = decodeHtml(m[1]).trim();
    if (!href || href.startsWith("#") || href.startsWith("mailto:") || href.startsWith("tel:")) return null;
    let absolute = href;
    try {
      absolute = new URL(href, fetchResult.finalUrl || BASE).toString();
    } catch {}
    return { href: absolute, anchor: stripTags(m[2]).slice(0, 120) };
  });
  const internalLinks = hrefs.filter((l) => {
    try {
      return new URL(l.href).hostname === "nad-lan.co.il";
    } catch {
      return false;
    }
  });
  const imageCount = [...html.matchAll(/<img\b/gi)].length;
  const imagesMissingAlt = [...html.matchAll(/<img\b[^>]*>/gi)].filter((m) => !/\salt=["'][^"']+["']/i.test(m[0])).length;
  const forms = allMatches(html, /<form\b[^>]*>[\s\S]*?<\/form>/gi, (m) => {
    const form = m[0];
    const action = decodeHtml((form.match(/\saction=["']([^"']*)["']/i) || [])[1] || "");
    const method = decodeHtml((form.match(/\smethod=["']([^"']*)["']/i) || [])[1] || "get").toLowerCase();
    const fields = allMatches(form, /<(?:input|select|textarea)\b[^>]*\sname=["']([^"']+)["'][^>]*>/gi, (fm) => decodeHtml(fm[1]));
    return { action, method, fields: [...new Set(fields)].slice(0, 40) };
  });
  const schemaTypes = [...new Set(allMatches(html, /"@type"\s*:\s*"([^"]+)"/g, (m) => m[1]))].slice(0, 20);
  const riskTerms = INTERNAL_PUBLIC_RISK_TERMS.filter((term) => clean.includes(term));
  const sameTitleH1 = h1.some((x) => x && title && title.includes(x) && x.length > 18);

  return {
    url: fetchResult.url,
    finalUrl: fetchResult.finalUrl,
    status: fetchResult.status,
    title,
    description,
    robots,
    canonical,
    h1,
    h1Count: h1.length,
    h2,
    wordCount: wordCount(clean),
    cleanTextSample: clean.slice(0, 400),
    internalLinkCount: internalLinks.length,
    uniqueInternalTargets: [...new Set(internalLinks.map((l) => pathOf(l.href)))].slice(0, 80),
    topInternalAnchors: internalLinks.slice(0, 30),
    imageCount,
    imagesMissingAlt,
    forms,
    schemaTypes,
    riskTerms,
    sameTitleH1,
    class: classifyUrl(fetchResult.finalUrl || fetchResult.url),
    error: fetchResult.error || null,
  };
}

async function restCollection(restBase, maxPages = 1) {
  const collected = [];
  let total = null;
  for (let page = 1; page <= maxPages; page += 1) {
    const url = `${BASE}/wp-json/wp/v2/${restBase}?per_page=100&page=${page}&_fields=id,link,slug,title,excerpt,content,parent,modified,date,status`;
    const res = await fetchText(url);
    if (res.status < 200 || res.status >= 300) {
      return { restBase, total, fetched: collected.length, rows: collected, error: res.error || `HTTP ${res.status}` };
    }
    if (total === null) total = Number(res.headers.get("x-wp-total") || 0) || null;
    try {
      const rows = JSON.parse(res.text);
      if (!Array.isArray(rows) || rows.length === 0) break;
      collected.push(...rows);
      if (rows.length < 100) break;
    } catch (error) {
      return { restBase, total, fetched: collected.length, error: `JSON parse failed: ${error.message}` };
    }
  }
  return { restBase, total, fetched: collected.length, rows: collected };
}

function summarizeRestRows(rows = []) {
  return rows.map((row) => {
    const title = stripTags(row.title?.rendered || "");
    const excerpt = stripTags(row.excerpt?.rendered || "");
    const body = stripTags(row.content?.rendered || "");
    return {
      id: row.id,
      slug: row.slug,
      link: row.link,
      title,
      excerpt,
      parent: row.parent || 0,
      modified: row.modified,
      wordCount: wordCount(body),
      class: classifyUrl(row.link || row.slug),
      titleTokens: topTokens(`${row.slug} ${title}`).slice(0, 14),
      hasInternalRiskTerm: INTERNAL_PUBLIC_RISK_TERMS.some((term) => (row.content?.rendered || row.excerpt?.rendered || "").includes(term)),
    };
  });
}

function groupBy(items, keyFn) {
  const out = {};
  for (const item of items) {
    const key = keyFn(item);
    out[key] ||= [];
    out[key].push(item);
  }
  return out;
}

function detectCannibalization(pageRows = []) {
  const clusters = {};
  for (const page of pageRows) {
    const slug = page.slug || pathOf(page.link);
    const tokens = new Set(topTokens(slug));
    const signals = [];
    for (const signal of ["mortgage", "investment", "property", "value", "prices", "tax", "lawyer", "tabu", "buying", "selling", "urban", "renewal", "commercial", "tel", "aviv", "herzliya", "raanana", "savyon"]) {
      if (tokens.has(signal)) signals.push(signal);
    }
    const key = signals.join("+") || page.class || "other";
    clusters[key] ||= [];
    clusters[key].push(page);
  }
  return Object.fromEntries(
    Object.entries(clusters)
      .filter(([, rows]) => rows.length > 1)
      .sort((a, b) => b[1].length - a[1].length)
      .slice(0, 30)
      .map(([key, rows]) => [key, rows.map((r) => ({
        slug: r.slug,
        title: r.title,
        link: r.link,
        wordCount: r.wordCount,
      }))])
  );
}

async function main() {
  const startedAt = new Date().toISOString();
  const sitemapIndex = await fetchText(`${BASE}/sitemap_index.xml`);
  const sitemapUrls = parseXmlLocs(sitemapIndex.text).map((u) => u.replace(/^http:\/\//, "https://"));
  const sitemapGroups = {};
  for (const sitemapUrl of sitemapUrls) {
    const key = path.basename(new URL(sitemapUrl).pathname).replace("-sitemap", "").replace(".xml", "");
    const xml = await fetchText(sitemapUrl);
    sitemapGroups[key] = {
      sitemapUrl,
      status: xml.status,
      count: parseXmlLocs(xml.text).length,
      urls: parseXmlLocs(xml.text).map((u) => u.replace(/^http:\/\//, "https://")),
    };
  }

  const typeResult = await fetchText(`${BASE}/wp-json/wp/v2/types`);
  let restTypes = {};
  try {
    restTypes = JSON.parse(typeResult.text);
  } catch {}
  const publicRestTypes = Object.fromEntries(
    Object.entries(restTypes)
      .filter(([, value]) => value?.rest_base)
      .map(([key, value]) => [key, {
        name: value.name,
        slug: value.slug,
        restBase: value.rest_base,
        hasArchive: value.has_archive,
        hierarchical: value.hierarchical,
      }])
  );

  const restBasesToFetch = [
    ["pages", 4],
    ["posts", 2],
    ["product", 1],
    ["nadlan_term", 2],
    ["nadlan_project", 2],
    ["nadlan_professional", 2],
  ].filter(([base]) => Object.values(publicRestTypes).some((t) => t.restBase === base) || ["pages", "posts"].includes(base));

  const restCollections = {};
  for (const [base, maxPages] of restBasesToFetch) {
    const collection = await restCollection(base, maxPages);
    restCollections[base] = {
      restBase: collection.restBase,
      total: collection.total,
      fetched: collection.fetched,
      error: collection.error || null,
      rows: summarizeRestRows(collection.rows || []),
    };
  }

  const htmlUrls = [];
  for (const [group, data] of Object.entries(sitemapGroups)) {
    const limit = MAX_HTML_PER_GROUP[group] || 25;
    for (const url of data.urls.slice(0, limit)) htmlUrls.push(url);
  }
  for (const critical of [
    `${BASE}/`,
    `${BASE}/professionals/`,
    `${BASE}/projects/`,
    `${BASE}/properties/`,
    `${BASE}/catalog/`,
    `${BASE}/glossary/`,
    `${BASE}/urban-renewal/`,
    `${BASE}/investment-apartment/`,
    `${BASE}/property-value-estimator/`,
  ]) htmlUrls.push(critical);

  const uniqueHtmlUrls = [...new Set(htmlUrls)];
  const pageAnalyses = await mapLimit(uniqueHtmlUrls, 8, async (url) => {
    const result = await fetchText(url);
    return analyzeHtml(result);
  });

  const homepage = pageAnalyses.find((p) => p.url === `${BASE}/`);
  const homepageLinkCounts = homepage
    ? Object.entries(groupBy(homepage.topInternalAnchors || [], (l) => pathOf(l.href)))
        .map(([target, links]) => ({ target, count: links.length, anchors: [...new Set(links.map((l) => l.anchor).filter(Boolean))].slice(0, 6) }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 40)
    : [];

  const glossaryIndex = pageAnalyses.find((p) => p.url === `${BASE}/glossary/`);
  const glossaryTargets = glossaryIndex
    ? [...new Set((glossaryIndex.topInternalAnchors || []).map((l) => l.href).filter((href) => pathOf(href) !== "/glossary/"))].slice(0, 25)
    : [];
  const glossaryTargetChecks = [];
  for (const url of glossaryTargets) {
    const result = await fetchText(url);
    glossaryTargetChecks.push({
      url,
      finalUrl: result.finalUrl,
      status: result.status,
      path: pathOf(result.finalUrl),
      title: textOfFirst(result.text, /<title[^>]*>([\s\S]*?)<\/title>/i),
      h1: allMatches(result.text, /<h1\b[^>]*>([\s\S]*?)<\/h1>/gi, (m) => stripTags(m[1])).slice(0, 3),
    });
  }

  const pageRows = restCollections.pages?.rows || [];
  const wordCountBuckets = {
    under500: pageRows.filter((p) => p.wordCount < 500).map((p) => ({ slug: p.slug, title: p.title, wordCount: p.wordCount, link: p.link })),
    under1200: pageRows.filter((p) => p.wordCount >= 500 && p.wordCount < 1200).map((p) => ({ slug: p.slug, title: p.title, wordCount: p.wordCount, link: p.link })),
    strong2000plus: pageRows.filter((p) => p.wordCount >= 2000).map((p) => ({ slug: p.slug, title: p.title, wordCount: p.wordCount, link: p.link })),
  };

  const report = {
    auditStamp: startedAt,
    base: BASE,
    noContentWriteAudit: true,
    sitemapIndex: {
      status: sitemapIndex.status,
      urlCount: sitemapUrls.length,
      sitemaps: Object.fromEntries(Object.entries(sitemapGroups).map(([k, v]) => [k, { sitemapUrl: v.sitemapUrl, status: v.status, count: v.count }])),
    },
    publicRestTypes,
    restCollections,
    htmlSample: {
      crawled: pageAnalyses.length,
      statusCounts: Object.entries(groupBy(pageAnalyses, (p) => String(p.status))).map(([status, rows]) => ({ status, count: rows.length })),
      classCounts: Object.entries(groupBy(pageAnalyses, (p) => p.class)).map(([klass, rows]) => ({ class: klass, count: rows.length })),
      issues: {
        non200: pageAnalyses.filter((p) => p.status !== 200).map((p) => ({ url: p.url, finalUrl: p.finalUrl, status: p.status, error: p.error })),
        noH1: pageAnalyses.filter((p) => p.status === 200 && p.h1Count === 0).map((p) => ({ url: p.url, title: p.title })),
        multiH1: pageAnalyses.filter((p) => p.h1Count > 1).map((p) => ({ url: p.url, h1: p.h1 })),
        noCanonical: pageAnalyses.filter((p) => p.status === 200 && !p.canonical).map((p) => ({ url: p.url, title: p.title })),
        internalRiskTerms: pageAnalyses.filter((p) => p.riskTerms.length).map((p) => ({ url: p.url, terms: p.riskTerms })),
        duplicateTitleH1Signals: pageAnalyses.filter((p) => p.sameTitleH1).map((p) => ({ url: p.url, title: p.title, h1: p.h1 })),
        imagesMissingAlt: pageAnalyses.filter((p) => p.imagesMissingAlt).map((p) => ({ url: p.url, imageCount: p.imageCount, imagesMissingAlt: p.imagesMissingAlt })),
      },
      importantPages: pageAnalyses
        .filter((p) => [`${BASE}/`, `${BASE}/professionals/`, `${BASE}/projects/`, `${BASE}/properties/`, `${BASE}/catalog/`, `${BASE}/glossary/`].includes(p.url))
        .map((p) => ({
          url: p.url,
          status: p.status,
          finalUrl: p.finalUrl,
          title: p.title,
          h1: p.h1,
          h2: p.h2,
          wordCount: p.wordCount,
          internalLinkCount: p.internalLinkCount,
          imageCount: p.imageCount,
          forms: p.forms,
          schemaTypes: p.schemaTypes,
          canonical: p.canonical,
        })),
      homepageLinkCounts,
      glossaryTargetChecks,
      sampledPages: pageAnalyses.map((p) => ({
        url: p.url,
        status: p.status,
        finalUrl: p.finalUrl,
        class: p.class,
        title: p.title,
        h1: p.h1,
        wordCount: p.wordCount,
        internalLinkCount: p.internalLinkCount,
        imageCount: p.imageCount,
        schemaTypes: p.schemaTypes,
      })),
    },
    contentInventory: {
      pageCount: pageRows.length,
      wordCountBuckets,
      cannibalizationCandidates: detectCannibalization(pageRows),
      riskTermRows: pageRows.filter((p) => p.hasInternalRiskTerm).map((p) => ({ slug: p.slug, title: p.title, link: p.link })),
    },
  };

  await fs.mkdir(path.dirname(OUT), { recursive: true });
  await fs.writeFile(OUT, `${JSON.stringify(report, null, 2)}\n`, "utf8");
  console.log(JSON.stringify({
    wrote: OUT,
    sitemapGroups: report.sitemapIndex.sitemaps,
    restCollections: Object.fromEntries(Object.entries(report.restCollections).map(([k, v]) => [k, { total: v.total, fetched: v.fetched, error: v.error }])),
    htmlCrawled: report.htmlSample.crawled,
    issueCounts: Object.fromEntries(Object.entries(report.htmlSample.issues).map(([k, v]) => [k, v.length])),
  }, null, 2));
}

await main();
