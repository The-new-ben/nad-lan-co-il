import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:[A-Za-z]:)/, p => p.slice(1))), '..');
const readJson = rel => JSON.parse(fs.readFileSync(path.join(root, rel), 'utf8'));
const sha256 = buffer => crypto.createHash('sha256').update(buffer).digest('hex');
const failures = [];
const assertions = [];
const assert = (condition, message) => { assertions.push({ pass: Boolean(condition), message }); if (!condition) failures.push(message); };

const checklist = readJson('03-DATA/atomic-checklist-v2.json');
const facilityData = readJson('03-DATA/aurelia-facilities.json');
const assets = readJson('04-ASSETS/asset-manifest.json');
const excerpts = readJson('05-CODE/canonical-code-excerpts.json');

assert(checklist.mode === 'non-blocking-lights', 'Checklist is explicitly non-blocking.');
assert(checklist.definitions.length >= 700, 'At least 700 atomic checks exist.');
assert(new Set(checklist.definitions.map(item => item.id)).size === checklist.definitions.length, 'Every checklist ID is unique.');
assert(facilityData.facilities.length === 12, 'Exactly 12 detailed facilities exist.');
assert(assets.assets.length === 12, 'Asset manifest contains 12 panorama assets.');
assert(excerpts.extracts.length >= 11, 'Canonical code map contains at least 11 exact repository excerpts.');

for (const facility of facilityData.facilities) {
  const target = path.join(root, facility.asset);
  assert(fs.existsSync(target), `${facility.id}: panorama file exists.`);
  if (!fs.existsSync(target)) continue;
  const buffer = fs.readFileSync(target);
  assert(buffer.subarray(1,4).toString() === 'PNG', `${facility.id}: asset is PNG.`);
  const width = buffer.readUInt32BE(16);
  const height = buffer.readUInt32BE(20);
  assert(Math.abs(width / height - 2) < 0.02, `${facility.id}: panorama is 2:1 (${width}x${height}).`);
  assert(facility.sceneHotspots.length >= 6, `${facility.id}: at least six functional scene hotspots are specified.`);
  assert(facility.equipment.length >= 7, `${facility.id}: at least seven equipment/features are specified.`);
  assert(facility.modelAnchor?.type === 'gltf-node', `${facility.id}: semantic GLB node contract exists.`);
  const manifest = assets.assets.find(item => item.facilityId === facility.id);
  assert(manifest?.sha256 === sha256(buffer), `${facility.id}: asset SHA-256 matches manifest.`);
}

const report = { verifiedAt: new Date().toISOString(), root, summary: { assertions: assertions.length, passed: assertions.filter(x=>x.pass).length, failed: failures.length }, failures, assertions };
fs.writeFileSync(path.join(root, '01-EVIDENCE', 'package-verification.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(report.summary, null, 2));
if (failures.length) process.exitCode = 1;
