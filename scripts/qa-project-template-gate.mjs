import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const DEFAULT_SITE = 'https://nad-lan.co.il';
const DEFAULT_SLUG = 'rainbow-tel-aviv';
const DEFAULT_POST_ID = 4464;
const DEFAULT_MIN_VERSION = '1.66.3';

function parseArgs(argv) {
  const out = {
    site: DEFAULT_SITE,
    slug: DEFAULT_SLUG,
    postId: DEFAULT_POST_ID,
    minVersion: DEFAULT_MIN_VERSION,
    out: '',
    strict: false,
    visual: false,
    requireTranslations: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--site') out.site = argv[++i] || out.site;
    else if (a === '--slug') out.slug = argv[++i] || out.slug;
    else if (a === '--post-id') out.postId = Number(argv[++i] || 0) || out.postId;
    else if (a === '--min-version') out.minVersion = argv[++i] || out.minVersion;
    else if (a === '--out') out.out = argv[++i] || out.out;
    else if (a === '--strict') out.strict = true;
    else if (a === '--visual') out.visual = true;
    else if (a === '--require-translations') out.requireTranslations = true;
    else if (a === '--help' || a === '-h') {
      console.log(`Usage:
  node scripts/qa-project-template-gate.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464 --strict
  node scripts/qa-project-template-gate.mjs --visual --out docs/qa/rainbow-template-gate.json

Checks the rendered public project page, healthcheck, SEO/schema signals, public-copy leaks,
multilingual readiness state, and optionally the visual Chrome harness.`);
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
    .replace(/&gt;/g, '>')
    .replace(/&#8211;/g, '-');
}

function stripTags(value) {
  return decodeEntities(String(value || '').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
}

function visibleHtml(html) {
  return String(html || '')
    .replace(/<script\b[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style\b[\s\S]*?<\/style>/gi, ' ')
    .replace(/<noscript\b[\s\S]*?<\/noscript>/gi, ' ')
    .replace(/<template\b[\s\S]*?<\/template>/gi, ' ');
}

function attr(tag, name) {
  const re = new RegExp(`${name}=["']([^"']*)`, 'i');
  const m = String(tag || '').match(re);
  return m ? decodeEntities(m[1]) : '';
}

async function fetchText(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Codex-Project-Template-Gate/1.0' },
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`HTTP ${res.status} from ${url}: ${text.slice(0, 220)}`);
  return text.replace(/^\uFEFF/, '');
}

async function fetchJson(url) {
  return JSON.parse(await fetchText(url));
}

function extractSeo(html) {
  const noScripts = visibleHtml(html);
  const title = stripTags((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '');
  const descTag = (html.match(/<meta\s+[^>]*name=["']description["'][^>]*>/i)
    || html.match(/<meta\s+[^>]*content=["'][^"']*["'][^>]*name=["']description["'][^>]*>/i)
    || [])[0] || '';
  const canonicalTag = (html.match(/<link\s+[^>]*rel=["']canonical["'][^>]*>/i) || [])[0] || '';
  const robotsTag = (html.match(/<meta\s+[^>]*name=["']robots["'][^>]*>/i) || [])[0] || '';
  const h1s = [...noScripts.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)].map((m) => stripTags(m[1])).filter(Boolean);
  const h2s = [...noScripts.matchAll(/<h2\b[^>]*>([\s\S]*?)<\/h2>/gi)].map((m) => stripTags(m[1])).filter(Boolean);
  const og = [...html.matchAll(/<meta\s+[^>]*property=["']og:([^"']+)["'][^>]*>/gi)].map((m) => [m[1], attr(m[0], 'content')]);
  const hreflang = [...html.matchAll(/<link\s+[^>]*rel=["']alternate["'][^>]*hreflang=["']([^"']+)["'][^>]*>/gi)].map((m) => [m[1], attr(m[0], 'href')]);
  const jsonld = [...html.matchAll(/<script\s+[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1].trim());
  const schemaTypes = [];
  for (const raw of jsonld) {
    try {
      const parsed = JSON.parse(raw);
      const nodes = Array.isArray(parsed) ? parsed : [parsed];
      for (const node of nodes) {
        if (node && Array.isArray(node['@graph'])) {
          for (const graphNode of node['@graph']) schemaTypes.push(graphNode['@type']);
        } else if (node) {
          schemaTypes.push(node['@type']);
        }
      }
    } catch {
      schemaTypes.push('PARSE_ERROR');
    }
  }
  const visibleText = stripTags(noScripts);
  return {
    title,
    title_len: title.length,
    description: attr(descTag, 'content'),
    description_len: attr(descTag, 'content').length,
    canonical: attr(canonicalTag, 'href'),
    robots: attr(robotsTag, 'content'),
    h1s,
    h2_count: h2s.length,
    h2_first: h2s.slice(0, 10),
    og: Object.fromEntries(og),
    hreflang,
    jsonld_count: jsonld.length,
    schema_types: [...new Set(schemaTypes.flat().filter(Boolean))],
    visible_text_len: visibleText.length,
    visible_text: visibleText,
  };
}

function add(result, ok, name, detail = '', severity = 'blocker') {
  result.checks.push({ ok: !!ok, name, detail, severity });
}

function hasAll(value, words) {
  return words.every((word) => String(value || '').includes(word));
}

function runVisualGate(args, result) {
  const outDir = path.join('docs', 'qa', 'screenshots', `${args.slug}-template-gate-visual`);
  const proc = spawnSync(
    process.execPath,
    [
      'scripts/qa-project-showroom-visual.mjs',
      '--site',
      args.site,
      '--slug',
      args.slug,
      '--out',
      outDir,
      '--strict',
    ],
    { encoding: 'utf8' },
  );
  result.visual = {
    attempted: true,
    exit_code: proc.status,
    out_dir: outDir,
    stdout_tail: String(proc.stdout || '').slice(-3000),
    stderr_tail: String(proc.stderr || '').slice(-3000),
  };
  add(result, proc.status === 0, 'visual Chrome showroom gate passes', `exit ${proc.status}; out ${outDir}`);
}

async function main() {
  const args = parseArgs(process.argv);
  const result = {
    generated_at: new Date().toISOString(),
    site: args.site,
    slug: args.slug,
    post_id: args.postId,
    min_version: args.minVersion,
    strict: args.strict,
    require_translations: args.requireTranslations,
    checks: [],
  };

  const health = await fetchJson(`${args.site}/wp-json/nadlan/v1/healthcheck?cb=${Date.now()}`);
  const html = await fetchText(`${args.site}/projects/${args.slug}/?cb=${Date.now()}`);
  const seo = extractSeo(html);
  const p3d = health.project_3d || {};
  const assembly = health.project_page_assembly || {};

  result.live = {
    version: health.version,
    project_3d: {
      model_viewer_ready: !!p3d.model_viewer_ready,
      model_viewer_module_tag: !!p3d.model_viewer_module_tag,
      model_viewer_reveal: p3d.model_viewer_reveal || '',
      model_viewer_loading: p3d.model_viewer_loading || '',
      dual_showroom_v1661: !!p3d.dual_showroom_v1661,
      embedded_selector_with_glb_v1661: !!p3d.embedded_selector_with_glb_v1661,
      apartment_cell_selector_v1655: !!p3d.apartment_cell_selector_v1655,
      mobile_cell_polish_v1656: !!p3d.mobile_cell_polish_v1656,
      projects_with_glb: Number(p3d.projects_with_glb || 0),
      showroom_payload_api_v1652: !!p3d.showroom_payload_api_v1652,
      admin_unit_builder_v1650: !!p3d.admin_unit_builder_v1650,
      rest_showroom_fields_v1651: !!p3d.rest_showroom_fields_v1651,
    },
    assembly: {
      rainbow_id: assembly.rainbow_id || 0,
      rainbow_seo_v1634: !!assembly.rainbow_seo_v1634,
      rainbow_showroom_v1635: !!assembly.rainbow_showroom_v1635,
      rainbow_public_copy_v1663: !!assembly.rainbow_public_copy_v1663,
      faq_meta: !!assembly.faq_meta,
      price_meta: !!assembly.price_meta,
    },
    seo: {
      title: seo.title,
      description: seo.description,
      canonical: seo.canonical,
      robots: seo.robots,
      h1s: seo.h1s,
      h2_count: seo.h2_count,
      h2_first: seo.h2_first,
      og_image: seo.og.image || '',
      hreflang: seo.hreflang,
      schema_types: seo.schema_types,
      visible_text_len: seo.visible_text_len,
    },
  };

  add(result, compareVersions(health.version, args.minVersion) >= 0, 'plugin version meets template gate', `${health.version} >= ${args.minVersion}`);
  add(result, !!p3d.model_viewer_ready, 'model-viewer health marker is ready');
  add(result, !!p3d.model_viewer_module_tag, 'model-viewer module tag marker is ready');
  add(result, Number(p3d.projects_with_glb || 0) >= 1, 'at least one project has a GLB');
  add(result, !!p3d.dual_showroom_v1661 && !!p3d.embedded_selector_with_glb_v1661, 'dual GLB plus embedded facade selector is live');
  add(result, !!p3d.apartment_cell_selector_v1655, 'apartment-cell selector marker is live');
  add(result, !!p3d.showroom_payload_api_v1652 && !!p3d.rest_showroom_fields_v1651, 'payload and REST showroom contract is live');
  add(result, !!p3d.admin_unit_builder_v1650, 'owner unit builder is live');
  add(result, !!assembly.rainbow_public_copy_v1663, 'Rainbow public-copy cleanup v1.66.3 has run', 'healthcheck project_page_assembly.rainbow_public_copy_v1663');

  add(result, seo.h1s.length === 1, 'exactly one visible H1', `${seo.h1s.length}: ${seo.h1s.join(' | ')}`);
  add(result, hasAll(seo.title, ['Rainbow', 'שדה דב']) && /דירות למכירה|מחיר|מחירים/.test(seo.title), 'title is transaction-led and project-specific', seo.title);
  add(result, seo.description.length >= 120 && seo.description.length <= 165, 'meta description length is search-friendly', `${seo.description.length} chars`);
  add(result, /מחיר|מחירים|אומדן|למכירה/.test(seo.description), 'meta description has price or sale intent', seo.description);
  add(result, seo.canonical === `${args.site}/projects/${args.slug}/`, 'canonical is self-referencing', seo.canonical);
  add(result, /index/.test(seo.robots) && /follow/.test(seo.robots), 'robots allows index/follow', seo.robots);
  add(result, seo.schema_types.includes('FAQPage'), 'FAQPage schema exists');
  add(result, seo.schema_types.includes('ApartmentComplex'), 'ApartmentComplex schema exists');
  add(result, !!seo.og.image, 'OG image exists', seo.og.image);
  add(result, !seo.og.image || /^https:\/\//i.test(seo.og.image), 'OG image uses HTTPS', seo.og.image, 'major');
  add(result, !/(Fatal error|Stack trace|Warning:|Notice:|Parse error)/.test(html), 'no PHP error leak in HTML');
  add(result, !/(class=&quot;|nlpf dl rdl|<code>class=)/.test(html), 'no obvious visible code/class leak');
  add(result, !/(Ã|Â|\uFFFD)/.test(html), 'no mojibake/replacement characters');

  const internalWords = [
    'פאנל הלידים',
    'פאנל לידים',
    'לידים',
    'lead panel',
    'funnel',
    'CRM',
    'monetization',
    'paid placement',
  ].filter((word) => seo.visible_text.includes(word));
  add(result, internalWords.length === 0, 'public visible text has no internal operations words', internalWords.join(', '));

  if (args.requireTranslations) {
    add(result, seo.hreflang.length >= 2, 'translated pages expose hreflang alternates', JSON.stringify(seo.hreflang));
  } else {
    add(result, seo.hreflang.length === 0, 'hreflang absent until real translated pages exist', `${seo.hreflang.length} alternates`, 'info');
  }

  if (args.visual) runVisualGate(args, result);
  else {
    result.visual = { attempted: false, note: 'Run with --visual to execute the Chrome screenshot gate.' };
    add(result, false, 'visual Chrome showroom gate not run', 'run with --visual before declaring template-ready', 'major');
  }

  const blockingFailures = result.checks.filter((c) => !c.ok && c.severity !== 'info');
  result.summary = {
    passed: result.checks.filter((c) => c.ok).length,
    failed: blockingFailures.length,
    informational: result.checks.filter((c) => c.severity === 'info').length,
    template_ready: blockingFailures.length === 0,
  };

  if (args.out) {
    fs.mkdirSync(path.dirname(args.out), { recursive: true });
    fs.writeFileSync(args.out, `${JSON.stringify(result, null, 2)}\n`);
  }
  console.log(JSON.stringify(result, null, 2));
  if (args.strict && blockingFailures.length) process.exit(1);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
