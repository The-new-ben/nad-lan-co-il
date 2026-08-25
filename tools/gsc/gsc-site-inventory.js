#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const fsp = fs.promises;
const path = require('path');

const SCRIPT_VERSION = '1.0.0';
const DEFAULT_BASE_URL = 'https://nad-lan.co.il';
const USER_AGENT = `NadLan-GSC-Inventory/${SCRIPT_VERSION} (read-only)`;
const MAX_RETRIES = 4;
const PUBLIC_CONTENT_TYPES = new Set([
  'post',
  'page',
  'product',
  'nadlan_term',
  'nadlan_property',
  'nadlan_project',
  'nadlan_professional',
]);

function parseArgs(argv) {
  const result = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith('--')) continue;
    const equal = token.indexOf('=');
    const rawKey = token.slice(2, equal === -1 ? undefined : equal);
    const key = rawKey.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
    if (equal !== -1) result[key] = token.slice(equal + 1);
    else if (argv[index + 1] && !argv[index + 1].startsWith('--')) result[key] = argv[++index];
    else result[key] = true;
  }
  return result;
}

function usage() {
  return [
    'Read-only WordPress and XML sitemap inventory',
    '',
    'Required:',
    '  --output-dir=<absolute GSC run directory>',
    '',
    'Optional:',
    `  --base-url=${DEFAULT_BASE_URL}`,
    '  --help',
  ].join('\n');
}

async function ensureDir(directory) {
  await fsp.mkdir(directory, { recursive: true });
}

function csvEscape(value) {
  if (value === null || value === undefined) return '';
  const text = String(value);
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

async function writeCsv(file, columns, rows) {
  await ensureDir(path.dirname(file));
  const lines = [columns.join(',')];
  for (const row of rows) lines.push(columns.map((column) => csvEscape(row[column])).join(','));
  await fsp.writeFile(file, `\uFEFF${lines.join('\r\n')}\r\n`, 'utf8');
}

async function writeJson(file, value) {
  await ensureDir(path.dirname(file));
  await fsp.writeFile(file, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function sha256(file) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const input = fs.createReadStream(file);
    input.on('error', reject);
    input.on('data', (chunk) => hash.update(chunk));
    input.on('end', () => resolve(hash.digest('hex')));
  });
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function fetchWithRetry(url, options = {}) {
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt += 1) {
    let response;
    try {
      response = await fetch(url, {
        ...options,
        headers: { 'user-agent': USER_AGENT, accept: '*/*', ...(options.headers || {}) },
      });
    } catch (error) {
      if (attempt === MAX_RETRIES) throw error;
      await delay(500 * (2 ** attempt));
      continue;
    }
    if (response.ok) return response;
    if ((response.status === 429 || response.status >= 500) && attempt < MAX_RETRIES) {
      await delay(500 * (2 ** attempt));
      continue;
    }
    throw new Error(`HTTP ${response.status} for ${url}`);
  }
  throw new Error(`Request failed after retries: ${url}`);
}

function decodeEntities(value) {
  return String(value || '')
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, decimal) => String.fromCodePoint(Number.parseInt(decimal, 10)))
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&quot;/gi, '"')
    .replace(/&#039;|&apos;/gi, "'")
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>');
}

function stripHtml(value) {
  return decodeEntities(String(value || '')
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' '))
    .replace(/\s+/g, ' ')
    .trim();
}

function wordCount(value) {
  const text = stripHtml(value);
  return text ? text.split(/\s+/u).filter(Boolean).length : 0;
}

function extractH1(value) {
  const match = String(value || '').match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/i);
  return match ? stripHtml(match[1]) : '';
}

function xmlLocations(xml) {
  return [...String(xml || '').matchAll(/<loc>([\s\S]*?)<\/loc>/gi)]
    .map((match) => decodeEntities(match[1].trim()));
}

function normalizeUrl(raw, baseUrl = DEFAULT_BASE_URL) {
  try {
    const url = new URL(raw, baseUrl);
    url.hash = '';
    if (url.hostname.toLowerCase() !== new URL(baseUrl).hostname.toLowerCase()) return url.href;
    url.protocol = 'https:';
    url.hostname = url.hostname.toLowerCase();
    url.pathname = url.pathname.replace(/%[0-9a-f]{2}/gi, (escape) => escape.toUpperCase());
    if (!url.pathname.endsWith('/') && !/\.[a-z0-9]{2,6}$/i.test(url.pathname)) url.pathname += '/';
    return url.href;
  } catch {
    return String(raw || '').trim();
  }
}

function inferLanguage(rawUrl) {
  try {
    const match = new URL(rawUrl).pathname.match(/^\/(en|fr|ru|ar)(?:\/|$)/i);
    return match ? match[1].toLowerCase() : 'he';
  } catch {
    return 'he';
  }
}

function extractInternalLinks(html, baseUrl) {
  const host = new URL(baseUrl).hostname.toLowerCase();
  const links = new Set();
  for (const match of String(html || '').matchAll(/\bhref\s*=\s*(["'])(.*?)\1/gi)) {
    try {
      const url = new URL(decodeEntities(match[2]), baseUrl);
      if (url.hostname.toLowerCase() !== host) continue;
      if (!/^https?:$/.test(url.protocol)) continue;
      links.add(normalizeUrl(url.href, baseUrl));
    } catch {
      // Ignore malformed links in rendered content.
    }
  }
  return [...links];
}

function inferSitemapType(sitemapUrl) {
  const name = new URL(sitemapUrl).pathname.split('/').pop().replace(/-sitemap\d*\.xml$/i, '');
  const taxonomyTypes = new Set([
    'category', 'post_tag', 'product_cat', 'product_tag', 'product_brand',
    'nadlan_term_cat', 'nadlan_compound', 'nadlan_city', 'nadlan_profession', 'author',
  ]);
  return taxonomyTypes.has(name) ? `taxonomy:${name}` : name;
}

async function fetchJson(url) {
  return (await fetchWithRetry(url, { headers: { accept: 'application/json' } })).json();
}

async function fetchTaxonomyTerms(baseUrl, taxonomies) {
  const termMaps = {};
  for (const [taxonomy, descriptor] of Object.entries(taxonomies)) {
    const restBase = descriptor.rest_base;
    if (!restBase || restBase.includes('(?P<')) continue;
    const values = new Map();
    let pageNumber = 1;
    for (;;) {
      const url = new URL(`${baseUrl}/wp-json/wp/v2/${restBase}`);
      url.searchParams.set('per_page', '100');
      url.searchParams.set('page', String(pageNumber));
      url.searchParams.set('_fields', 'id,name,slug');
      let response;
      try {
        response = await fetchWithRetry(url.href, { headers: { accept: 'application/json' } });
      } catch {
        break;
      }
      const rows = await response.json();
      for (const row of rows) values.set(Number(row.id), stripHtml(row.name));
      const totalPages = Number(response.headers.get('x-wp-totalpages') || 1);
      if (pageNumber >= totalPages || rows.length === 0) break;
      pageNumber += 1;
    }
    termMaps[taxonomy] = values;
  }
  return termMaps;
}

function itemTaxonomies(item, typeDescriptor, termMaps) {
  const values = [];
  for (const taxonomy of typeDescriptor.taxonomies || []) {
    const ids = Array.isArray(item[taxonomy]) ? item[taxonomy] : [];
    const names = ids.map((id) => termMaps[taxonomy]?.get(Number(id)) || `id:${id}`);
    if (names.length) values.push(`${taxonomy}=${names.join('|')}`);
  }
  return values.join('; ');
}

async function fetchContentType(baseUrl, type, descriptor, termMaps) {
  const rows = [];
  const taxonomyFields = descriptor.taxonomies || [];
  const fields = [
    'id', 'type', 'slug', 'parent', 'status', 'link', 'date_gmt', 'modified_gmt',
    'title', 'content', 'yoast_head_json', ...taxonomyFields,
  ];
  let pageNumber = 1;
  let reportedTotal = 0;
  for (;;) {
    const url = new URL(`${baseUrl}/wp-json/wp/v2/${descriptor.rest_base}`);
    url.searchParams.set('per_page', '100');
    url.searchParams.set('page', String(pageNumber));
    url.searchParams.set('context', 'view');
    url.searchParams.set('_fields', [...new Set(fields)].join(','));
    const response = await fetchWithRetry(url.href, { headers: { accept: 'application/json' } });
    const batch = await response.json();
    reportedTotal = Number(response.headers.get('x-wp-total') || reportedTotal || batch.length);
    for (const item of batch) {
      const rendered = item.content?.rendered || '';
      const yoast = item.yoast_head_json || {};
      const robots = yoast.robots || {};
      rows.push({
        normalized_url: normalizeUrl(item.link, baseUrl),
        url: item.link || '',
        post_id: Number(item.id),
        content_type: item.type || type,
        language: inferLanguage(item.link),
        title: stripHtml(item.title?.rendered || yoast.title || ''),
        h1: extractH1(rendered),
        slug: item.slug || '',
        parent: Number(item.parent || 0) || '',
        taxonomies: itemTaxonomies(item, descriptor, termMaps),
        wp_status: item.status || '',
        http_status: item.status === 'publish' ? 200 : '',
        http_status_source: item.status === 'publish' ? 'INFERRED_WP_REST_PUBLISHED' : '',
        indexability: robots.index || '',
        robots_directives: [robots.index, robots.follow, robots['max-snippet'], robots['max-image-preview'], robots['max-video-preview']].filter(Boolean).join(', '),
        canonical: yoast.canonical || '',
        sitemap_presence: 'FALSE',
        sitemap_source: '',
        published_date: item.date_gmt || '',
        modified_date: item.modified_gmt || '',
        word_count: wordCount(rendered),
        internal_inlinks: 0,
        internal_outlinks: 0,
        source: 'WP_REST',
        internal_links: extractInternalLinks(rendered, baseUrl),
      });
    }
    const totalPages = Number(response.headers.get('x-wp-totalpages') || 1);
    if (pageNumber >= totalPages || batch.length === 0) break;
    pageNumber += 1;
  }
  return { rows, reportedTotal };
}

async function fetchSitemaps(baseUrl) {
  const indexUrl = `${baseUrl}/sitemap_index.xml`;
  const indexXml = await (await fetchWithRetry(indexUrl, { headers: { accept: 'application/xml,text/xml' } })).text();
  const sitemapUrls = xmlLocations(indexXml);
  const entries = [];
  const sitemaps = [];
  for (const sitemapUrl of sitemapUrls) {
    const response = await fetchWithRetry(sitemapUrl, { headers: { accept: 'application/xml,text/xml' } });
    const xml = await response.text();
    const locations = xmlLocations(xml);
    const sitemapType = inferSitemapType(sitemapUrl);
    sitemaps.push({ url: sitemapUrl, http_status: response.status, content_type: sitemapType, url_count: locations.length });
    for (const url of locations) entries.push({ url, normalized_url: normalizeUrl(url, baseUrl), sitemapUrl, sitemapType });
  }
  return { indexUrl, sitemapUrls, entries, sitemaps };
}

function mergeInventory(restRows, sitemapEntries, baseUrl) {
  const merged = new Map();
  for (const row of restRows) merged.set(row.normalized_url, row);
  for (const entry of sitemapEntries) {
    let row = merged.get(entry.normalized_url);
    if (!row) {
      const parsed = new URL(entry.url);
      const slug = decodeURIComponent(parsed.pathname.split('/').filter(Boolean).pop() || '');
      row = {
        normalized_url: entry.normalized_url,
        url: entry.url,
        post_id: '',
        content_type: entry.sitemapType,
        language: inferLanguage(entry.url),
        title: '',
        h1: '',
        slug,
        parent: '',
        taxonomies: '',
        wp_status: '',
        http_status: 200,
        http_status_source: 'INFERRED_XML_SITEMAP_ENTRY',
        indexability: 'index',
        robots_directives: '',
        canonical: '',
        sitemap_presence: 'TRUE',
        sitemap_source: entry.sitemapUrl,
        published_date: '',
        modified_date: '',
        word_count: '',
        internal_inlinks: 0,
        internal_outlinks: '',
        source: 'XML_SITEMAP',
        internal_links: [],
      };
      merged.set(entry.normalized_url, row);
    } else {
      row.sitemap_presence = 'TRUE';
      row.sitemap_source = row.sitemap_source ? `${row.sitemap_source}; ${entry.sitemapUrl}` : entry.sitemapUrl;
      row.source = 'WP_REST+XML_SITEMAP';
    }
  }

  const inlinks = new Map();
  for (const row of merged.values()) {
    const unique = new Set(row.internal_links || []);
    row.internal_outlinks = unique.size;
    for (const target of unique) inlinks.set(target, (inlinks.get(target) || 0) + 1);
  }
  for (const row of merged.values()) row.internal_inlinks = inlinks.get(row.normalized_url) || 0;

  return [...merged.values()].sort((a, b) => a.normalized_url.localeCompare(b.normalized_url, 'en'));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(`${usage()}\n`);
    return;
  }
  if (!args.outputDir || !path.isAbsolute(args.outputDir)) throw new Error('--output-dir must be an absolute path.');
  const baseUrl = String(args.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, '');
  const outputDirectory = path.join(args.outputDir, 'analysis');
  await ensureDir(outputDirectory);

  const startedAt = new Date().toISOString();
  const types = await fetchJson(`${baseUrl}/wp-json/wp/v2/types`);
  const taxonomies = await fetchJson(`${baseUrl}/wp-json/wp/v2/taxonomies`);
  const termMaps = await fetchTaxonomyTerms(baseUrl, taxonomies);
  const selectedTypes = Object.entries(types).filter(([type, descriptor]) =>
    PUBLIC_CONTENT_TYPES.has(type) && descriptor.rest_namespace === 'wp/v2' && descriptor.rest_base);

  const restRows = [];
  const restCounts = [];
  for (const [type, descriptor] of selectedTypes) {
    process.stdout.write(`Reading WordPress REST type ${type}...\n`);
    const result = await fetchContentType(baseUrl, type, descriptor, termMaps);
    restRows.push(...result.rows);
    restCounts.push({ type, rest_base: descriptor.rest_base, reported_total: result.reportedTotal, received_rows: result.rows.length });
  }

  process.stdout.write('Reading XML sitemaps...\n');
  const sitemapResult = await fetchSitemaps(baseUrl);
  const inventory = mergeInventory(restRows, sitemapResult.entries, baseUrl);
  const csvFile = path.join(outputDirectory, 'page-inventory-source.csv');
  const columns = [
    'url', 'normalized_url', 'post_id', 'content_type', 'language', 'title', 'h1', 'slug', 'parent',
    'taxonomies', 'wp_status', 'http_status', 'http_status_source', 'indexability', 'robots_directives',
    'canonical', 'sitemap_presence', 'sitemap_source', 'published_date', 'modified_date', 'word_count',
    'internal_inlinks', 'internal_outlinks', 'source',
  ];
  await writeCsv(csvFile, columns, inventory);

  const summaryFile = path.join(outputDirectory, 'page-inventory-source-summary.json');
  const summary = {
    script: 'gsc-site-inventory.js',
    scriptVersion: SCRIPT_VERSION,
    startedAt,
    completedAt: new Date().toISOString(),
    mode: 'READ_ONLY',
    baseUrl,
    wordpressRest: { selectedTypes: restCounts, receivedRows: restRows.length },
    xmlSitemaps: { indexUrl: sitemapResult.indexUrl, sitemaps: sitemapResult.sitemaps, entries: sitemapResult.entries.length },
    merged: {
      uniqueUrls: inventory.length,
      inSitemap: inventory.filter((row) => row.sitemap_presence === 'TRUE').length,
      fromWordPressRest: inventory.filter((row) => row.source.includes('WP_REST')).length,
    },
    caveats: [
      'HTTP 200 for published REST items and sitemap entries is inferred from the read-only source and is marked in http_status_source; page URLs were not individually crawled.',
      'Internal link counts are derived only from rendered content returned by the public WordPress REST API.',
      'Sitemap-only taxonomy, author, and unexposed custom-type URLs can lack title, H1, word count, and post ID.',
    ],
  };
  await writeJson(summaryFile, summary);
  const hashes = {
    'page-inventory-source.csv': await sha256(csvFile),
    'page-inventory-source-summary.json': await sha256(summaryFile),
  };
  await writeJson(path.join(outputDirectory, 'page-inventory-source.sha256.json'), hashes);
  process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`ERROR: ${error.message}\n`);
  process.exitCode = 1;
});
