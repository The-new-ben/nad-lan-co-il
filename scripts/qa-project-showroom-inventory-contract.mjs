import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = process.cwd();
const VALIDATOR = path.join(ROOT, 'scripts', 'validate-project-showroom-payload.mjs');
const SCHEMA = path.join(ROOT, 'docs', 'templates', 'project-showroom-payload.schema.json');
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'nadlan-inventory-contract-'));

function basePayload() {
  return {
    schema: 'nadlan-project-showroom-payload/v1',
    project_slug: 'fixture-project',
    post_id: 0,
    public_use_policy: 'בדיקת חוזה מלאי',
    meta: {
      project_3d_image: '',
      project_3d_viewbox: '0 0 1000 1000',
      project_3d_floor_height_m: '3.1',
      project_3d_ground_elevation_m: '0',
      project_3d_avg_price_per_sqm: '',
      project_3d_price_source_note: '',
      project_3d_model_type: 'gltf',
      project_model_glb: 'https://nad-lan.co.il/model.glb',
      project_model_usdz: '',
      project_model_poster: 'https://nad-lan.co.il/poster.webp',
      project_3d_video_url: '',
      project_3d_tour_url: '',
      project_3d_cesium_tiles_url: '',
      project_3d_drawings_json: [],
      project_3d_environment_json: {},
      project_3d_units: [],
      project_3d_demo: '1',
    },
  };
}

function validate(name, payload) {
  const file = path.join(temp, `${name}.json`);
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  const result = spawnSync(process.execPath, [VALIDATOR, '--schema', SCHEMA, '--payload', file], {
    cwd: ROOT,
    encoding: 'utf8',
  });
  const output = JSON.parse(result.stdout);
  return { code: result.status, errors: output.errors };
}

try {
  const missing = validate('missing-contract', basePayload());
  assert.equal(missing.code, 1);
  assert(missing.errors.some((error) => error.includes('inventory_contract is required')));

  const unsafe = basePayload();
  unsafe.inventory_contract = {
    state: 'not_verified',
    decision_grade: true,
    effective_at: '2026-08-14',
    source_ids: ['fixture-source'],
    note: 'אין מלאי מאומת',
  };
  const unsafeResult = validate('unsafe-contract', unsafe);
  assert.equal(unsafeResult.code, 1);
  assert(unsafeResult.errors.some((error) => error.includes('decision_grade must be false')));

  const safe = basePayload();
  safe.inventory_contract = {
    state: 'not_supplied',
    decision_grade: false,
    effective_at: '2026-08-14',
    source_ids: ['fixture-source'],
    note: 'הבניין וכלי ההמחשה מוצגים ללא מלאי דירות לבחירה.',
  };
  const safeResult = validate('safe-contract', safe);
  assert.equal(safeResult.code, 0, safeResult.errors.join('\n'));

  const legacy = basePayload();
  legacy.meta.project_3d_units = [{
    id: 'fixture-unit',
    title: 'דירת בדיקה',
    floor: 1,
    rooms: 3,
    sqm: 80,
    status: 'demo',
    hotspot_position: '0 1 0',
    hotspot_normal: '0 0 1',
  }];
  const legacyResult = validate('legacy-unit', legacy);
  assert.equal(legacyResult.code, 0, legacyResult.errors.join('\n'));

  console.log('PASS project showroom inventory contract: zero units fail closed; explicit non-decision inventory passes; legacy unit payload remains compatible.');
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
