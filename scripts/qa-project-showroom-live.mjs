const DEFAULT_SITE = 'https://nad-lan.co.il';
const DEFAULT_SLUG = 'rainbow-tel-aviv';
const DEFAULT_POST_ID = 4464;
const DEFAULT_MIN_VERSION = '1.65.2';

function parseArgs(argv) {
  const out = {
    site: DEFAULT_SITE,
    slug: DEFAULT_SLUG,
    postId: DEFAULT_POST_ID,
    minVersion: DEFAULT_MIN_VERSION,
    strict: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--site') out.site = argv[++i] || out.site;
    else if (a === '--slug') out.slug = argv[++i] || out.slug;
    else if (a === '--post-id') out.postId = Number(argv[++i] || 0) || out.postId;
    else if (a === '--min-version') out.minVersion = argv[++i] || out.minVersion;
    else if (a === '--strict') out.strict = true;
    else if (a === '--help' || a === '-h') {
      console.log(`Usage:
  node scripts/qa-project-showroom-live.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464
  node scripts/qa-project-showroom-live.mjs --strict

Optional authenticated CMS payload check:
  WP_USER=<wordpress user> WP_APP_PASSWORD=<application password> node scripts/qa-project-showroom-live.mjs --strict

Strict mode exits non-zero on any failed gate.`);
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  out.site = out.site.replace(/\/+$/, '');
  return out;
}

function compareVersions(a, b) {
  const aa = String(a || '').split('.').map((n) => Number(n) || 0);
  const bb = String(b || '').split('.').map((n) => Number(n) || 0);
  for (let i = 0; i < Math.max(aa.length, bb.length); i += 1) {
    const d = (aa[i] || 0) - (bb[i] || 0);
    if (d !== 0) return d;
  }
  return 0;
}

function decodeEntities(value) {
  return String(value || '')
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>');
}

function stripTags(value) {
  return decodeEntities(String(value || '').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
}

async function fetchText(url, options = {}) {
  const res = await fetch(url, {
    ...options,
    headers: {
      'User-Agent': 'Codex-Showroom-QA/1.0',
      ...(options.headers || {}),
    },
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`HTTP ${res.status} from ${url}: ${text.slice(0, 220)}`);
  return text;
}

async function fetchJson(url, options = {}) {
  const text = await fetchText(url, options);
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`Non-JSON response from ${url}: ${text.slice(0, 220)}`);
  }
}

function authHeader() {
  const user = process.env.WP_USER || '';
  const pass = process.env.WP_APP_PASSWORD || '';
  if (!user || !pass) return '';
  return `Basic ${Buffer.from(`${user}:${pass}`).toString('base64')}`;
}

function titleOf(html) {
  const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return stripTags(m ? m[1] : '');
}

function metaDescriptionOf(html) {
  const m = html.match(/<meta\s+[^>]*name=["']description["'][^>]*content=["']([^"']*)["'][^>]*>/i)
    || html.match(/<meta\s+[^>]*content=["']([^"']*)["'][^>]*name=["']description["'][^>]*>/i);
  return decodeEntities(m ? m[1] : '').trim();
}

function h1sOf(html) {
  const found = [];
  const re = /<h1\b[^>]*>([\s\S]*?)<\/h1>/gi;
  let m;
  while ((m = re.exec(html))) found.push(stripTags(m[1]));
  return found.filter(Boolean);
}

function scriptTagForModelViewer(html) {
  const scripts = html.match(/<script\b[^>]*nadlan-model-viewer[^>]*><\/script>/gi) || [];
  return scripts[0] || '';
}

function add(result, ok, name, detail = '') {
  result.checks.push({ ok, name, detail });
}

async function main() {
  const args = parseArgs(process.argv);
  const result = {
    site: args.site,
    slug: args.slug,
    post_id: args.postId,
    min_version: args.minVersion,
    checks: [],
  };

  const health = await fetchJson(`${args.site}/wp-json/nadlan/v1/healthcheck?cb=${Date.now()}`);
  const liveVersion = String(health.version || '');
  result.live_version = liveVersion;
  add(result, compareVersions(liveVersion, args.minVersion) >= 0, 'live plugin version is new enough', `${liveVersion} >= ${args.minVersion}`);
  add(result, !!(health.project_3d && health.project_3d.showroom_payload_api_v1652), 'payload API health marker is present', 'project_3d.showroom_payload_api_v1652');

  const html = await fetchText(`${args.site}/projects/${args.slug}/?cb=${Date.now()}`);
  const title = titleOf(html);
  const description = metaDescriptionOf(html);
  const h1s = h1sOf(html);
  const mvScript = scriptTagForModelViewer(html);
  const hotspotSlots = (html.match(/slot=["']hotspot-/g) || []).length;

  result.page = {
    title,
    description,
    h1s,
    has_nlp3d: html.includes('nlp3d-premium'),
    has_model_viewer: html.includes('<model-viewer'),
    hotspot_slots: hotspotSlots,
  };

  add(result, h1s.length === 1, 'exactly one H1', `${h1s.length}: ${h1s.join(' | ')}`);
  add(result, html.includes('nlp3d-premium'), 'showroom section exists', 'nlp3d-premium');
  add(result, html.includes('<model-viewer'), 'model-viewer element exists', '<model-viewer');
  add(result, /<model-viewer[\s\S]*\breveal=["']auto["']/i.test(html), 'model-viewer reveal auto', 'reveal="auto"');
  add(result, /<model-viewer[\s\S]*\bloading=["']auto["']/i.test(html), 'model-viewer loading auto', 'loading="auto"');
  add(result, mvScript !== '' && /\btype=["']module["']/i.test(mvScript), 'model-viewer script is type module', mvScript || 'missing');
  add(result, hotspotSlots >= 3, 'model-viewer hotspots exist', `${hotspotSlots} hotspot slots`);
  add(result, title.includes('Rainbow') && title.includes('שדה דב'), 'SEO title has Rainbow and Sde Dov', title);
  add(result, /מחיר|מחירים|למכירה/.test(title), 'SEO title is transaction-led', title);
  add(result, description.includes('Rainbow') && description.includes('שדה דב'), 'meta description has Rainbow and Sde Dov', description);
  add(result, /מחיר|מחירים|למכירה/.test(description), 'meta description mentions price/sale intent', description);
  add(result, !/(Fatal error|Stack trace|Warning:|Notice:|Parse error)/.test(html), 'no PHP error leak in HTML');
  add(result, !/(class=&quot;|nlpf dl rdl|<code>class=)/.test(html), 'no obvious visible code/class leak');
  add(result, !/(Ã|Â|\uFFFD)/.test(html), 'no obvious mojibake/replacement chars');

  const auth = authHeader();
  if (auth) {
    try {
      const payload = await fetchJson(`${args.site}/wp-json/nadlan/v1/project-showroom/${args.postId}`, {
        headers: { Authorization: auth },
      });
      result.payload_api = {
        fields: Array.isArray(payload.fields) ? payload.fields.length : 0,
        units_count: payload.units_count,
        has_glb: !!(payload.meta && payload.meta.project_model_glb),
      };
      add(result, Array.isArray(payload.fields) && payload.fields.length >= 17, 'authenticated payload API exports fields', `${result.payload_api.fields} fields`);
      add(result, Number(payload.units_count || 0) >= 1, 'authenticated payload API exports units', `${payload.units_count} units`);
      add(result, !!(payload.meta && payload.meta.project_model_glb), 'authenticated payload API has GLB URL');
    } catch (err) {
      add(result, false, 'authenticated payload API GET succeeds', err.message);
    }
  } else {
    add(result, true, 'authenticated payload API GET skipped', 'set WP_USER and WP_APP_PASSWORD to verify CMS round-trip');
  }

  const failed = result.checks.filter((c) => !c.ok);
  result.summary = {
    passed: result.checks.length - failed.length,
    failed: failed.length,
  };
  console.log(JSON.stringify(result, null, 2));
  if (args.strict && failed.length) process.exit(1);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
