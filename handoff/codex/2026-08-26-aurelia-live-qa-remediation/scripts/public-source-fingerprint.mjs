import fs from 'node:fs';
import crypto from 'node:crypto';

const url = process.argv.find(arg => /^https?:\/\//.test(arg)) || 'https://nad-lan.co.il/projects/aurelia/';
const outArg = process.argv.indexOf('--out');
const out = outArg >= 0 ? process.argv[outArg + 1] : null;
const sha256 = value => crypto.createHash('sha256').update(value).digest('hex');

const response = await fetch(url, { redirect: 'follow', headers: { 'User-Agent': 'NadLan-Public-Source-Fingerprint/1.0' } });
const html = await response.text();

// Canonicalization is deliberately narrow and versioned. Do not add whitespace,
// line-ending or DOM serialization transforms: those would hide public-source drift.
const canonical = html
  .replace(
    /(לתיקון פרטים או להסרת פרויקט:\s*)<a\b[^>]*>[\s\S]*?<\/a>/g,
    '$1<a data-redacted="contact"></a>'
  )
  .replace(
    /("(?:mapbox_token|whatsapp|phone|email|nonce|rest_nonce)"\s*:\s*")[^"]*(")/g,
    '$1<redacted>$2'
  )
  .replace(
    /([?&](?:_wpnonce|nonce)=)[^&"'<\s]+/g,
    '$1<redacted>'
  );

const first = (regex, group = 1) => html.match(regex)?.[group]?.trim() || null;
const all = regex => [...html.matchAll(regex)].map(match => match[1]);
const jsonLd = all(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi);
const jsonLdTypes = [];
for (const block of jsonLd) {
  try {
    const value = JSON.parse(block);
    const visit = node => {
      if (!node || typeof node !== 'object') return;
      if (node['@type']) jsonLdTypes.push(node['@type']);
      for (const child of Object.values(node)) {
        if (Array.isArray(child)) child.forEach(visit);
        else if (child && typeof child === 'object') visit(child);
      }
    };
    visit(value);
  } catch {
    jsonLdTypes.push('[invalid-json]');
  }
}

const report = {
  schemaVersion: '1.0.0', canonicalizationVersion: 'nadlan-public-source-v1', capturedAt: new Date().toISOString(), requestedUrl: url,
  finalUrl: response.url, status: response.status, ok: response.ok,
  bytes: Buffer.byteLength(html), rawSha256: sha256(html),
  canonicalChars: canonical.length, canonicalBytes: Buffer.byteLength(canonical), canonicalSha256: sha256(canonical),
  title: first(/<title[^>]*>([\s\S]*?)<\/title>/i)?.replace(/\s+/g, ' '),
  canonical: first(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)/i),
  robots: first(/<meta[^>]+name=["']robots["'][^>]+content=["']([^"']+)/i),
  description: first(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)/i),
  h1Count: (html.match(/<h1\b/gi) || []).length,
  hreflang: all(/<link[^>]+hreflang=["']([^"']+)["'][^>]*>/gi),
  icons: all(/<link[^>]+rel=["'][^"']*icon[^"']*["'][^>]+href=["']([^"']+)/gi),
  jsonLd: { blocks: jsonLd.length, types: jsonLdTypes },
  scriptSources: all(/<script[^>]+src=["']([^"']+)/gi),
  headers: Object.fromEntries(response.headers.entries()),
  fingerprintRules: {
    compare: 'canonicalSha256', rawHash: 'single-response evidence only',
    neverStoreInPublicUploads: ['raw HTML containing tokens/contact data', 'WordPress nonces', 'private endpoint payloads']
  }
};

const serialized = `${JSON.stringify(report, null, 2)}\n`;
if (out) fs.writeFileSync(out, serialized, 'utf8');
process.stdout.write(serialized);
