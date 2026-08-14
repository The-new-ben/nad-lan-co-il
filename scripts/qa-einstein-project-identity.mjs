import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const readJson = (relative) => JSON.parse(fs.readFileSync(path.join(ROOT, relative), 'utf8'));
const einstein = readJson('data/projects/einstein-tower.json');
const ashdar = readJson('data/projects/einstein-ramat-aviv.json');
const index = readJson('data/projects/index.json');
const catalog = fs.readFileSync(path.join(ROOT, 'plugins/nadlan-config/inc/premium-catalog.php'), 'utf8');

assert.equal(einstein.id, 'einstein-tower');
assert.equal(einstein.identity.project_contract_id, 'einstein-tower-6885-32');
assert.equal(einstein.identity.wp_post_id, 4867);
assert.equal(einstein.identity.public_slug, 'einstein-tower');
assert.match(einstein.identity.developer, /חג/);
assert.equal(String(einstein.location.gush), '6885');
assert.equal(String(einstein.location.helka), '32');
assert.equal(einstein.building_form.num_buildings, 3);
assert.equal(einstein.building_form.floors, 28);
assert.equal(einstein.units.total_units, 215);
assert.equal(einstein.units.inventory_state, 'not_supplied');
assert.equal(einstein.units.inventory_decision_grade, false);
assert.deepEqual(einstein.units.inventory, []);
assert.equal(einstein.assets_3d.calibration.north_degrees, 0);
assert.equal(einstein.assets_3d.decision_grade, false);
assert.equal(einstein.assets_3d.representation_kind, 'owner_approved_illustration');
assert.equal(einstein.assets_3d.decision_id, 'OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING');
assert.equal(einstein.visual_playground.decision_id, 'OWNER-2026-08-13-VISUAL-PLAYGROUND');
assert.notEqual(einstein.assets_3d.decision_id, einstein.visual_playground.decision_id);

const alias18 = einstein.identity.aka.find((alias) => alias.value === 'Einstein 18');
assert(alias18);
assert.equal(alias18.confirmed, false);
assert.match(alias18.note, /6885\/40/);
const phonetic = einstein.identity.aka.find((alias) => alias.value === 'Levichko');
assert(phonetic);
assert.equal(phonetic.confirmed, false);

assert.notEqual(ashdar.id, einstein.id);
assert(!/חג/.test(ashdar.identity.developer));
assert.notEqual(ashdar.location.helka, '32');

assert.equal(index.projects.length, index.count);
assert.equal(new Set(index.projects.map((project) => project.id)).size, index.projects.length);
const indexed = index.projects.find((project) => project.id === 'einstein-tower');
assert(indexed);
assert.equal(indexed.developer, einstein.identity.developer);
assert.equal(indexed.ready_for_page, einstein.db_meta.ready_for_page);
assert(index.projects.some((project) => project.id === 'einstein-ramat-aviv'));

for (const [field, sources] of Object.entries(einstein.field_sources)) {
  assert(Array.isArray(sources) && sources.length > 0, `${field} must have sources`);
  for (const value of sources) {
    const url = new URL(value);
    assert.equal(url.protocol, 'https:', `${field} source must use https`);
    assert.equal(url.username, '');
    assert.equal(url.password, '');
  }
}

assert.match(catalog, /'slug'\s*=>\s*'einstein-tower'/);
assert.match(catalog, /'units'\s*=>\s*215/);
assert.match(catalog, /'floors'\s*=>\s*28/);
assert.match(catalog, /הערכת החברה: רבעון 3, 2030/);
assert.match(catalog, /'rooms'\s*=>\s*array\(\)/);
assert.match(catalog, /'experience_label'\s*=>\s*'מודל החלטה תלת-ממדי'/);

for (const forbidden of [
  /אבן גבירול/,
  /'units'\s*=>\s*515/,
  /'slug'\s*=>\s*'hagag-einstein-18'/,
]) {
  assert(!forbidden.test(JSON.stringify(einstein)), `project record contains forbidden legacy identity ${forbidden}`);
}

console.log('PASS Einstein identity: post 4867/in-place slug, parcel 6885/32, 3 buildings/215 units, zero inventory, unconfirmed aliases, distinct Ashdar record, and premium catalog row reconcile.');
