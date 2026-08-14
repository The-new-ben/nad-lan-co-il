/** Executable PHP-adapter -> canonical playground runtime contract gate. */

import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "..");
const require = createRequire(import.meta.url);
const runtime = require(path.join(repoRoot, "plugins/nadlan-config/assets/flagship-v3/flagship-playground.js"));
const raw = execFileSync("php", [path.join(here, "qa-flagship-v3-php.php"), "--emit-runtime-config"], {
  cwd: repoRoot,
  encoding: "utf8"
});
const config = JSON.parse(raw);
const normalized = runtime.normalizeConfig(
  config.playground,
  Date.parse("2026-08-14T12:00:00+03:00"),
  config.identity.project_contract_id,
  config.playground_trust.allowed_evidence_reference_ids,
  config.playground_trust.allowed_asset_prefix
);
const scenes = normalized.experienceAssets.interior.scenes.concat(normalized.experienceAssets.facilities.scenes);

assert.deepEqual(normalized.tools.map((tool) => tool.id), ["view", "interior", "design", "comments"]);
assert.deepEqual(scenes.map((scene) => scene.id), ["living", "bedroom", "arrival", "open-frame"]);
assert.ok(scenes.every((scene) => scene.openSurfaceToolId === "interior"));
assert.deepEqual(normalized.experienceMapping.anchors.map((anchor) => anchor.hotspotId), [
  "representative-interior-concept",
  "facility-arrival-concept",
  "facility-landscaped-open-space-concept"
]);
assert.deepEqual(normalized.experienceMapping.anchors.map((anchor) => anchor.sceneIds), [
  ["living", "bedroom"], ["arrival"], ["open-frame"]
]);
assert.deepEqual(normalized.experienceMapping.anchors.map((anchor) => anchor.placementConfidence), [
  { zone: 0.68, exactPoint: 0.18 }, { zone: 0.63, exactPoint: 0.20 }, { zone: 0.86, exactPoint: 0.24 }
]);
assert.equal(normalized.experienceMapping.sourceCited, false);
assert.equal(normalized.experienceMapping.decisionGrade, false);
assert.equal(normalized.experienceMapping.futureVerifiedState, "source_cited_mapping");

process.stdout.write("flagship-v3 WordPress adapter runtime fixture: PASS\n");
