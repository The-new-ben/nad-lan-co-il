import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const testsDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(testsDir, '..');
const dataDir = path.join(root, 'data');

const readJson = (name) => JSON.parse(fs.readFileSync(path.join(dataDir, name), 'utf8'));
const writeJson = (name, value) => fs.writeFileSync(path.join(dataDir, name), JSON.stringify(value, null, 2) + '\n');

const checklistSource = readJson('checklist-source.json');
const project = readJson('project.json');
const units = readJson('units.json');
const facilities = readJson('facilities.json');
const environment = readJson('environment.json');
const drawings = readJson('drawings.json');
const translations = readJson('translations.json');
const bom = readJson('engineering-bom.json');
const wordpress = readJson('wordpress-contract.json');
const sequence = readJson('page-sequence.json');
const seo = readJson('seo-intent-map.json');

const devices = [
  { id: 'm320', width: 320, height: 720, pointer: 'touch' },
  { id: 'm360', width: 360, height: 800, pointer: 'touch' },
  { id: 'm390', width: 390, height: 844, pointer: 'touch' },
  { id: 'm430', width: 430, height: 932, pointer: 'touch' },
  { id: 'tablet768', width: 768, height: 1024, pointer: 'touch' },
  { id: 'desktop1440', width: 1440, height: 1000, pointer: 'mouse' }
];
const languages = [
  { id: 'he', dir: 'rtl' },
  { id: 'en', dir: 'ltr' },
  { id: 'fr', dir: 'ltr' },
  { id: 'ru', dir: 'ltr' },
  { id: 'ar', dir: 'rtl' }
];
const networks = [
  { id: 'wifi', latencyMs: 20, downMbps: 100 },
  { id: '4g', latencyMs: 80, downMbps: 12 },
  { id: 'slow4g', latencyMs: 160, downMbps: 1.6 }
];

const hooks = {
  R01: ['post_title', 'post_name', 'project_address', 'nadlan_city', 'nadlan_compound'],
  R02: ['_yoast_wpseo_title', '_yoast_wpseo_metadesc', 'wp_head', 'public View Source'],
  R03: ['theme breadcrumbs', 'project status meta', 'scroll state'],
  R04: ['hero_image', 'project_3d_poster', 'project_eyebrow_*'],
  R05: ['project_3d_model_url', 'project_3d_units_json', 'engine.js'],
  R06: ['project_3d_units_json', 'engine.js', 'mv-ux.js'],
  R07: ['project_3d_drawings_json', 'unit.plan_id', 'engine.js'],
  R08: ['lat', 'lng', 'unit.directionAzimuth', 'mapbox-init.js'],
  R09: ['unit.tour_url', 'studio.js', 'project_3d_drawings_json'],
  R10: ['project_3d_facilities_json', 'facility.id', 'facility.hotspot'],
  R11: ['project_3d_environment_json', 'lat', 'lng', 'Cesium/Mapbox module'],
  R12: ['engineering-bom.json', 'studio option codes', 'admin BOM panel'],
  R13: ['post_content', 'entity links', 'FAQ fields'],
  R14: ['/wp-json/nadlan/v1/lead', '/brochure', '/cotour', 'buyflow.js'],
  R15: ['translations.json', 'i18n.js', 'hreflang/canonical'],
  R16: ['mv-ux.js', 'responsive CSS', 'performance evidence'],
  R17: ['admin checklist meta box', 'source snapshots', 'recipe version']
};

function inferredMode(domainId, title) {
  if (domainId === 'R02') return 'source';
  if (domainId === 'R12' || domainId === 'R17') return 'data+admin';
  if (/עובד|נטען|נשמר|מתעדכן|מסונכר|פותח|מעביר|מחזיר|משמר/.test(title)) return 'interaction';
  if (/44px|גלילה|פולד|מובייל|focus|ESC|layout shift|רשת/.test(title)) return 'viewport+accessibility';
  if (/יחיד|אחד|אין|קיים|תואם|עקבי|משויך|מחובר/.test(title)) return 'data+DOM';
  return 'manual-evidence';
}

function evidenceFor(domainId, mode) {
  if (mode === 'source') return ['saved public HTML', 'line reference', 'parsed value'];
  if (mode === 'interaction') return ['replay step', 'before/after state', 'selected IDs'];
  if (mode === 'viewport+accessibility') return ['viewport', 'DOMRect', 'focus/keyboard result', 'screenshot'];
  if (domainId === 'R12') return ['BOM component code', 'assembly', 'performance', 'inspection', 'maintenance'];
  if (domainId === 'R17') return ['admin field', 'evidence link', 'owner', 'timestamp'];
  return ['field or data path', 'expected value', 'observed value'];
}

function axesFor(domainId) {
  if (domainId === 'R02') return { devices: [{ id: 'public-source' }], languages, networks: [{ id: 'origin' }] };
  if (domainId === 'R12' || domainId === 'R17') return { devices: [{ id: 'admin' }], languages: [{ id: 'he', dir: 'rtl' }], networks: [{ id: 'origin' }] };
  if (['R01', 'R13'].includes(domainId)) return { devices: devices.filter((d) => ['m390', 'desktop1440'].includes(d.id)), languages, networks: [{ id: 'wifi' }] };
  return { devices, languages, networks };
}

const definitions = [];
for (const domain of checklistSource.domains) {
  domain.checks.forEach((title, index) => {
    const id = `${domain.id}-${String(index + 1).padStart(3, '0')}`;
    const mode = inferredMode(domain.id, title);
    definitions.push({
      id,
      domainId: domain.id,
      domain: domain.name,
      title,
      mode,
      nonBlocking: true,
      failLight: /אינה עובדת|חסר|לא נטען|אין /.test(title) ? 'red' : mode === 'manual-evidence' ? 'yellow' : 'orange',
      passLight: 'green',
      wordpressHooks: hooks[domain.id],
      evidenceRequired: evidenceFor(domain.id, mode),
      remediationRule: 'The light links to the owning field or component; saving and publishing are never blocked by this mechanism.'
    });
  });
}

const matrixCases = [];
for (const definition of definitions) {
  const axes = axesFor(definition.domainId);
  for (const device of axes.devices) {
    for (const language of axes.languages) {
      for (const network of axes.networks) {
        matrixCases.push({
          id: `${definition.id}@${device.id}@${language.id}@${network.id}`,
          baseCheckId: definition.id,
          domainId: definition.domainId,
          device: device.id,
          language: language.id,
          direction: language.dir ?? 'n/a',
          network: network.id,
          action: definition.title,
          expected: 'The requirement is observable, linked to evidence and produces a nonblocking light.',
          evidenceRequired: definition.evidenceRequired
        });
      }
    }
  }
}

const master = {
  schemaVersion: '1.0.0',
  project: project.id,
  purpose: 'Executable specification for the buyer page, WordPress implementation, admin lights and forensic evidence.',
  statusModel: checklistSource.statusMeaning,
  counts: {
    domains: checklistSource.domains.length,
    baseDefinitions: definitions.length,
    expandedCases: matrixCases.length,
    devices: devices.length,
    languages: languages.length,
    networks: networks.length
  },
  profiles: { devices, languages, networks },
  domains: checklistSource.domains.map(({ id, name }) => ({ id, name })),
  definitions
};

writeJson('master-checklist.json', master);
writeJson('matrix-test-cases.json', matrixCases);

const csvEscape = (value) => `"${String(value ?? '').replaceAll('"', '""')}"`;
const csvRows = [
  ['id', 'domain', 'title', 'mode', 'failLight', 'wordpressHooks', 'evidenceRequired'],
  ...definitions.map((item) => [item.id, item.domain, item.title, item.mode, item.failLight, item.wordpressHooks.join(' | '), item.evidenceRequired.join(' | ')])
];
fs.writeFileSync(path.join(dataDir, 'master-checklist.csv'), '\uFEFF' + csvRows.map((row) => row.map(csvEscape).join(',')).join('\n') + '\n');

const results = [];
function record(id, title, pass, evidence, lightOnFail = 'red') {
  results.push({ id, title, status: pass ? 'green' : lightOnFail, pass, evidence });
}
const unique = (values) => new Set(values).size === values.length;
const componentList = bom.systems.flatMap((system) => system.assemblies.flatMap((assembly) => assembly.components));
const assemblyList = bom.systems.flatMap((system) => system.assemblies);
const drawingIds = new Set(drawings.map((item) => item.id));

record('DATA-PROJECT-001', 'Project identity is owned by Aurelia Sde Dov', project.id === 'aurelia-sde-dov' && project.identity.neighborhood === 'שדה דב', `${project.id} · ${project.identity.address}`);
record('DATA-UNITS-002', 'Exactly 320 unit records are present', units.length === 320, `${units.length} units`);
record('DATA-UNITS-003', 'Every unit ID is unique', unique(units.map((item) => item.id)), `${new Set(units.map((item) => item.id)).size}/${units.length} unique`);
record('DATA-UNITS-004', 'Every unit has a positive price, area and floor', units.every((item) => item.price > 0 && item.sqm > 0 && item.floor > 0), 'price/sqm/floor scan');
record('DATA-PLAN-005', 'Every unit plan_id resolves to a drawing', units.every((item) => drawingIds.has(item.plan_id)), `${drawingIds.size} drawing IDs checked against ${units.length} units`);
record('DATA-FAC-006', 'Twelve facilities have valid hotspot coordinates', facilities.length === 12 && facilities.every((item) => Array.isArray(item.hotspot) && item.hotspot.length === 2 && item.hotspot.every((n) => Number.isFinite(n))), `${facilities.length} facilities`);
record('DATA-ENV-007', 'Twelve environment points have valid coordinates', environment.length === 12 && environment.every((item) => Number.isFinite(item.lat) && Number.isFinite(item.lng)), `${environment.length} environment points`);
record('DATA-LANG-008', 'Five language dictionaries exist', ['he', 'en', 'fr', 'ru', 'ar'].every((code) => translations[code]), Object.keys(translations).join(', '));
record('DATA-LANG-009', 'Every language includes the primary CTA', ['he', 'en', 'fr', 'ru', 'ar'].every((code) => translations[code]?.selectUnit && translations[code]?.getPlans), 'selectUnit + getPlans');
record('BOM-SYS-010', 'Seventeen engineering systems exist', bom.systems.length === 17, `${bom.systems.length} systems`);
record('BOM-ASM-011', 'Thirty-three assemblies exist', assemblyList.length === 33, `${assemblyList.length} assemblies`);
record('BOM-CMP-012', 'Eighty BOM components exist', componentList.length === 80, `${componentList.length} components`);
record('BOM-CMP-013', 'Every component has code, specification, unit, quantity basis, performance, inspection and maintenance', componentList.every((item) => ['code', 'item', 'spec', 'unit', 'quantityBasis', 'performance', 'qa', 'maintenance'].every((key) => String(item[key] ?? '').trim())), `${componentList.length} component records scanned`);
record('RECIPE-SEQ-014', 'The page recipe has twenty ordered sections', sequence.sections.length === 20 && sequence.sections.every((item, index) => item.order === index + 1), `${sequence.sections.length} ordered sections`);
record('RECIPE-SEQ-015', 'Every page section explains desktop, mobile, placement and SEO role', sequence.sections.every((item) => item.desktop && item.mobile && item.whyHere && item.seoRole && item.conversionRole), 'placement fields scan');
record('SEO-TITLE-016', 'SEO title is within the target display range', seo.serp.title.length >= 50 && seo.serp.title.length <= 65, `${seo.serp.title.length} characters`, 'yellow');
record('SEO-META-017', 'Meta description is within the target display range', seo.serp.metaDescription.length >= 120 && seo.serp.metaDescription.length <= 170, `${seo.serp.metaDescription.length} characters`, 'yellow');
record('SEO-H1-018', 'H1 contains both project identities and Sde Dov', /Aurelia Sde Dov/.test(seo.serp.h1) && /אורליה שדה דב/.test(seo.serp.h1), seo.serp.h1);
record('WP-TYPE-019', 'WordPress contract targets nadlan_project', JSON.stringify(wordpress).includes('nadlan_project'), 'wordpress-contract.json');
record('WP-RUNTIME-020', 'WordPress contract references NADLAN_SHOWROOM', JSON.stringify(wordpress).includes('NADLAN_SHOWROOM'), 'wordpress-contract.json');
record('CHECK-DEF-021', 'Every base check has evidence and WordPress hooks', definitions.every((item) => item.evidenceRequired.length && item.wordpressHooks.length), `${definitions.length} definitions`);
record('CHECK-MATRIX-022', 'The checklist expands into thousands of explicit cases', matrixCases.length >= 5000, `${matrixCases.length} matrix cases`);

const summary = results.reduce((acc, item) => ({ ...acc, [item.status]: (acc[item.status] ?? 0) + 1 }), {});
const report = {
  schemaVersion: '1.0.0',
  generatedAt: new Date().toISOString(),
  scope: 'data, recipe, SEO, BOM and WordPress-contract validation; browser replay is recorded separately',
  summary,
  results
};
writeJson('test-results.json', report);

const md = [
  '# Automated recipe validation',
  '',
  `Generated: ${report.generatedAt}`,
  '',
  `Base checklist definitions: ${definitions.length}`,
  `Expanded matrix cases: ${matrixCases.length}`,
  `Green: ${summary.green ?? 0} · Yellow: ${summary.yellow ?? 0} · Orange: ${summary.orange ?? 0} · Red: ${summary.red ?? 0}`,
  '',
  '| ID | Light | Check | Evidence |',
  '|---|---|---|---|',
  ...results.map((item) => `| ${item.id} | ${item.status} | ${item.title} | ${String(item.evidence).replaceAll('|', '\\|')} |`),
  '',
  'Browser, public View Source and live WordPress evidence are separate evidence classes. They are never reported as green merely because the data package is valid.'
].join('\n');
fs.writeFileSync(path.join(testsDir, 'automated-validation-report.md'), md + '\n');

console.log(JSON.stringify({ master: master.counts, validation: summary }, null, 2));
