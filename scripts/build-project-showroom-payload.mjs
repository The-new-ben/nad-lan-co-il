import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const FIELD_CONTRACT = [
  'project_3d_image',
  'project_3d_viewbox',
  'project_3d_floor_height_m',
  'project_3d_ground_elevation_m',
  'project_3d_avg_price_per_sqm',
  'project_3d_price_source_note',
  'project_3d_model_type',
  'project_model_glb',
  'project_model_usdz',
  'project_model_poster',
  'project_3d_video_url',
  'project_3d_tour_url',
  'project_3d_cesium_tiles_url',
  'project_3d_drawings_json',
  'project_3d_environment_json',
  'project_3d_units',
  'project_3d_demo',
];

function readJson(file, fallback = null) {
  if (!fs.existsSync(file)) return fallback;
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function asItems(value, nestedKey) {
  if (Array.isArray(value)) return value;
  if (value && Array.isArray(value[nestedKey])) return value[nestedKey];
  if (value && Array.isArray(value.items)) return value.items;
  return [];
}

function validateUrl(value, field, errors) {
  if (!value) return;
  try {
    const u = new URL(String(value));
    if (!['https:', 'http:'].includes(u.protocol)) {
      errors.push(`${field} must be http(s): ${value}`);
    }
  } catch {
    errors.push(`${field} is not a valid URL: ${value}`);
  }
}

function validatePayload(payload) {
  const errors = [];
  if (!payload || payload.schema !== 'nadlan-project-showroom-payload/v1') {
    errors.push('schema must be nadlan-project-showroom-payload/v1');
  }
  if (!payload.meta || typeof payload.meta !== 'object' || Array.isArray(payload.meta)) {
    errors.push('meta object is required');
    return errors;
  }
  for (const field of FIELD_CONTRACT) {
    if (!(field in payload.meta)) errors.push(`missing meta field: ${field}`);
  }
  const unknown = Object.keys(payload.meta).filter((field) => !FIELD_CONTRACT.includes(field));
  for (const field of unknown) errors.push(`unknown meta field: ${field}`);

  const units = payload.meta.project_3d_units;
  if (!Array.isArray(units) || units.length < 1) {
    errors.push('project_3d_units must be a non-empty array');
  } else {
    units.forEach((unit, index) => {
      for (const key of ['id', 'title', 'floor', 'rooms', 'sqm', 'status', 'hotspot_position', 'hotspot_normal', 'points', 'stage_x', 'stage_w']) {
        if (unit[key] === undefined || unit[key] === '') errors.push(`unit ${index} missing ${key}`);
      }
      validateUrl(unit.plan, `unit ${index} plan`, errors);
      validateUrl(unit.interior_url, `unit ${index} interior_url`, errors);
      validateUrl(unit.tour_url, `unit ${index} tour_url`, errors);
    });
  }

  for (const field of ['project_model_glb', 'project_model_poster', 'project_model_usdz', 'project_3d_image', 'project_3d_video_url', 'project_3d_tour_url', 'project_3d_cesium_tiles_url']) {
    validateUrl(payload.meta[field], field, errors);
  }

  if (!['procedural', 'facade', 'sprite360', 'gltf', 'bim'].includes(payload.meta.project_3d_model_type)) {
    errors.push('project_3d_model_type must match the plugin allow-list');
  }
  return errors;
}

function buildPayload(slug) {
  const dir = path.join(ROOT, 'assets', 'projects', slug);
  if (!fs.existsSync(dir)) throw new Error(`Missing project asset directory: ${dir}`);

  const metaExample = readJson(path.join(dir, 'project-meta-example.json'), {});
  const unitMap = readJson(path.join(dir, 'unit-map.json'), metaExample.project_3d_units || []);
  const drawings = readJson(path.join(dir, 'drawings.json'), metaExample.project_3d_drawings_json || []);
  const environment = readJson(path.join(dir, 'environment.json'), metaExample.project_3d_environment_json || {});
  const viewLayer = readJson(path.join(dir, 'view-layer-config.json'), {});
  const mapbox = viewLayer.providers && viewLayer.providers.mapbox ? viewLayer.providers.mapbox : {};

  const meta = {};
  for (const field of FIELD_CONTRACT) meta[field] = '';

  Object.assign(meta, {
    project_3d_image: metaExample.project_3d_image || '',
    project_3d_viewbox: metaExample.project_3d_viewbox || '0 0 1000 1000',
    project_3d_floor_height_m: String(metaExample.project_3d_floor_height_m || mapbox.floor_height_m || 3.05),
    project_3d_ground_elevation_m: String(metaExample.project_3d_ground_elevation_m || mapbox.ground_elevation_m || 0),
    project_3d_avg_price_per_sqm: String(metaExample.project_3d_avg_price_per_sqm || ''),
    project_3d_price_source_note: metaExample.project_3d_price_source_note || '',
    project_3d_model_type: metaExample.project_3d_model_type || 'gltf',
    project_model_glb: metaExample.project_model_glb || '',
    project_model_usdz: metaExample.project_model_usdz || '',
    project_model_poster: metaExample.project_model_poster || '',
    project_3d_video_url: metaExample.project_3d_video_url || '',
    project_3d_tour_url: metaExample.project_3d_tour_url || '',
    project_3d_cesium_tiles_url: metaExample.project_3d_cesium_tiles_url || '',
    project_3d_drawings_json: asItems(drawings, 'drawings'),
    project_3d_environment_json: environment || {},
    project_3d_units: asItems(unitMap, 'units'),
    project_3d_demo: String(metaExample.project_3d_demo || '1'),
  });

  return {
    $schema: 'docs/templates/project-showroom-payload.schema.json',
    schema: 'nadlan-project-showroom-payload/v1',
    project_slug: slug,
    post_id: Number(viewLayer.post_id || 0) || (slug === 'rainbow-tel-aviv' ? 4464 : 0),
    generated_from: [
      'project-meta-example.json',
      'unit-map.json',
      'drawings.json',
      'environment.json',
      'view-layer-config.json',
    ],
    public_use_policy: 'Prototype showroom data. Replace GLB, drawings, prices and inventory with developer-approved material before removing illustrative labels.',
    meta,
  };
}

const slug = process.argv[2] || 'rainbow-tel-aviv';
const shouldWrite = process.argv.includes('--write');
const payload = buildPayload(slug);
const errors = validatePayload(payload);
if (errors.length) {
  console.error(errors.map((e) => `- ${e}`).join('\n'));
  process.exit(1);
}

const out = JSON.stringify(payload, null, 2) + '\n';
if (shouldWrite) {
  const target = path.join(ROOT, 'assets', 'projects', slug, 'showroom-payload.json');
  fs.writeFileSync(target, out, 'utf8');
  console.log(`Wrote ${target}`);
} else {
  process.stdout.write(out);
}
