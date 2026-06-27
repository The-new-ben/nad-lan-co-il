#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DEFAULT_SITE = 'https://nad-lan.co.il';
const DEFAULT_LANGUAGES = ['he', 'en', 'fr', 'ru', 'ar'];
const LANGUAGE_META = {
  he: { locale: 'he-IL', dir: 'rtl', suffix: '' },
  en: { locale: 'en', dir: 'ltr', suffix: '-en' },
  fr: { locale: 'fr', dir: 'ltr', suffix: '-fr' },
  ru: { locale: 'ru', dir: 'ltr', suffix: '-ru' },
  ar: { locale: 'ar', dir: 'rtl', suffix: '-ar' },
};
const I18N_SOURCES = [
  'https://developers.google.com/search/docs/specialty/international/localized-versions',
  'https://yoast.com/hreflang-ultimate-guide/',
  'https://www.liquidweb.com/wordpress/seo/add-hreflang-tags/',
];

function usage() {
  return `Usage:
  node scripts/init-project-publication-manifest.mjs <project-slug> --title "Project Name"
  node scripts/init-project-publication-manifest.mjs <project-slug> --asset-slug <asset-slug> --out docs/plans/<slug>-publication-manifest.json

Creates a draft-only multilingual project publication manifest. It does not import, publish,
generate page content, or touch WordPress. The generated manifest is the preflight contract for
content reports, screenshot reports, draft payloads, hreflang artifacts, and dry-run import proof.`;
}

function parseArgs(argv) {
  const args = {
    slug: '',
    title: '',
    assetSlug: '',
    site: DEFAULT_SITE,
    endpoint: '',
    out: '',
    languages: DEFAULT_LANGUAGES,
    force: false,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!args.slug && !arg.startsWith('--')) args.slug = arg;
    else if (arg === '--title') args.title = argv[++i] || '';
    else if (arg === '--asset-slug') args.assetSlug = argv[++i] || '';
    else if (arg === '--site') args.site = (argv[++i] || args.site).replace(/\/+$/, '');
    else if (arg === '--endpoint') args.endpoint = argv[++i] || '';
    else if (arg === '--out') args.out = argv[++i] || '';
    else if (arg === '--languages') args.languages = String(argv[++i] || '').split(',').map((item) => item.trim()).filter(Boolean);
    else if (arg === '--force') args.force = true;
    else if (arg === '--help' || arg === '-h') {
      console.log(usage());
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (!args.slug) throw new Error('Missing <project-slug>.');
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(args.slug)) {
    throw new Error('Project slug must be ASCII lowercase words separated by hyphens.');
  }
  if (args.assetSlug && !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(args.assetSlug)) {
    throw new Error('Asset slug must be ASCII lowercase words separated by hyphens.');
  }
  if (!args.assetSlug) args.assetSlug = args.slug;
  if (!args.endpoint) args.endpoint = `${args.site}/wp-json/wp/v2/nadlan_project`;
  if (!args.out) args.out = `docs/plans/${args.slug}-publication-manifest.json`;
  if (!args.languages.length) throw new Error('At least one language is required.');
  for (const lang of args.languages) {
    if (!LANGUAGE_META[lang]) throw new Error(`Unsupported language "${lang}". Supported: ${Object.keys(LANGUAGE_META).join(', ')}`);
  }
  return args;
}

function languageEntry(args, lang) {
  const meta = LANGUAGE_META[lang];
  const slug = `${args.slug}${meta.suffix}`;
  const patternSuffix = meta.suffix || '';
  const pathToken = `${args.slug}${patternSuffix}`;
  return {
    lang,
    locale: meta.locale,
    dir: meta.dir,
    slug,
    public_url: `${args.site}/projects/${slug}/`,
    pattern: `patterns/project-showroom-${pathToken}.php`,
    draft: `docs/wp-drafts/${pathToken}-draft.json`,
    preview: `docs/previews/${pathToken}-preview.html`,
    content_report: `docs/qa/${pathToken}-content-depth-report.json`,
    screenshot_report: `docs/qa/screenshots/${pathToken}-preview-factory-gate/report.json`,
  };
}

function buildManifest(args) {
  const languages = args.languages.map((lang) => languageEntry(args, lang));
  const xDefault = args.languages.includes('he') ? 'he' : args.languages[0];
  return {
    status: 'draft_preflight_only',
    site: args.site,
    wordpress_type: 'nadlan_project',
    endpoint: args.endpoint,
    public_base_path: '/projects/',
    asset_slug: args.assetSlug,
    project_title: args.title || args.slug,
    x_default: xDefault,
    required_languages: args.languages,
    required_source_links: [],
    hreflang_artifacts: {
      map: `docs/seo/${args.slug}-hreflang-map.json`,
      head: `docs/seo/${args.slug}-hreflang-head.html`,
      report: `docs/qa/${args.slug}-hreflang-artifact-report.json`,
    },
    import_dry_run_report: `docs/qa/${args.slug}-draft-import-dry-run-report.json`,
    publish_rule: 'Do not publish or add hreflang until every language page exists on the final URL and passes content, screenshot, metadata, internal-link and public-copy QA.',
    localized_version_sources: I18N_SOURCES,
    languages,
  };
}

const args = parseArgs(process.argv);
const manifest = buildManifest(args);
const outPath = path.resolve(ROOT, args.out);
if (fs.existsSync(outPath) && !args.force) {
  throw new Error(`Refusing to overwrite existing manifest: ${args.out}. Use --force only when intentionally regenerating.`);
}
fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');

console.log(JSON.stringify({
  ok: true,
  out: args.out,
  slug: args.slug,
  asset_slug: args.assetSlug,
  languages: manifest.languages.map((entry) => entry.lang),
  mode: 'draft-preflight-only',
}, null, 2));
