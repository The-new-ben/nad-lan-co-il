import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const packagePath = "assets/projects/einstein-tower/contracts/flagship-project.json";
const stagePath = "docs/wp-drafts/einstein-tower-flagship-v3-private-stage.json";
const reportPath = "docs/qa/einstein-tower-flagship-stage-validation.json";
const stageOperation = "create_exact_private_sandbox";
const read = (relative) => fs.readFileSync(path.join(ROOT, relative), "utf8").replace(/\r\n?/g, "\n");
const readJson = (relative) => JSON.parse(read(relative));
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const textFileSha = (relative) => sha256(Buffer.from(read(relative), "utf8"));
const binaryFileSha = (relative) => sha256(fs.readFileSync(path.join(ROOT, relative)));
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const privateAssetBase = "https://nad-lan.co.il/flagship-private-asset/einstein-tower-6885-32/";
const wrapperPrefix = Buffer.from(
  "<?php\n" +
  "while ( ob_get_level() > 0 ) {\n" +
  "\tob_end_clean();\n" +
  "}\n" +
  "http_response_code( 404 );\n" +
  "header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate' );\n" +
  "header( 'X-Robots-Tag: noindex, nofollow, noarchive' );\n" +
  "header( 'X-Content-Type-Options: nosniff' );\n" +
  "header( 'Referrer-Policy: no-referrer' );\n" +
  "header( 'Content-Length: 0' );\n" +
  "__halt_compiler();\n",
  "utf8",
);

const project = readJson(packagePath);
const stage = readJson(stagePath);
const registry = readJson("plugins/nadlan-config/assets/flagship-v3/contracts/registry.json");
const contract = registry.contracts.find((row) => row.project_contract_id === project.project_contract_id);
assert(contract, "Trusted Einstein contract is missing.");
assert(project.schema === "nadlan-flagship-project-package/v1", "Project-package schema mismatch.");
assert(stage.schema === "nadlan-wordpress-private-stage-request/v1", "Private-stage schema mismatch.");
assert(stage.operation === stageOperation, "Private-stage operation must be exact create-only.");
assert(project.project_contract_id === "einstein-tower-6885-32", "Project identity mismatch.");
assert(project.canonical.post_id === 4867 && project.canonical.slug === "einstein-tower", "Canonical target mismatch.");
assert(project.canonical.public_release_enabled === false, "Public release must remain disabled.");
assert(stage.lookup.exact_slug === "sandbox-einstein-tower-flagship-v3-review", "Sandbox slug mismatch.");
assert(stage.body.status === "publish" && !Object.hasOwn(stage.body, "password"), "Stage must be a password-injected published sandbox without a serialized secret.");
assert(stage.secret_injection.post_password.environment_variable === "SANDBOX_POST_PASSWORD", "Password injection contract mismatch.");
assert(project.asset_delivery.transport === "password_gated_wordpress_proxy" && project.asset_delivery.base_url === privateAssetBase, "Private asset transport mismatch.");

assert(Array.isArray(contract.private_assets) && contract.private_assets.length === 7, "Trusted registry must contain seven private asset descriptors.");
const privateAssets = new Map();
for (const asset of contract.private_assets) {
  assert(/^[a-z0-9][a-z0-9._/-]*$/.test(asset.requested_name) && !asset.requested_name.includes("//") && !asset.requested_name.split("/").includes(".."), `Unsafe private asset name ${asset.requested_name}.`);
  assert(asset.storage_file.startsWith("assets/flagship-v3/private-assets/einstein-tower/") && asset.storage_file.endsWith(".asset.php"), `Unsafe private storage ${asset.requested_name}.`);
  assert(Number.isSafeInteger(asset.bytes) && asset.bytes > 0 && /^[a-f0-9]{64}$/.test(asset.sha256), `Invalid private descriptor ${asset.requested_name}.`);
  assert(["model/gltf-binary", "image/webp"].includes(asset.mime), `Invalid private MIME ${asset.requested_name}.`);
  assert(!privateAssets.has(asset.requested_name), `Duplicate private asset ${asset.requested_name}.`);

  const sourcePath = `assets/projects/einstein-tower/${asset.requested_name}`;
  const storagePath = `plugins/nadlan-config/${asset.storage_file}`;
  const legacyPath = `plugins/nadlan-config/assets/flagship-v3/projects/einstein-tower/${asset.requested_name}`;
  assert(fs.existsSync(path.join(ROOT, sourcePath)), `Canonical private source missing ${asset.requested_name}.`);
  assert(!fs.existsSync(path.join(ROOT, legacyPath)), `Legacy raw plugin copy remains ${asset.requested_name}.`);
  assert(binaryFileSha(sourcePath) === asset.sha256 && fs.statSync(path.join(ROOT, sourcePath)).size === asset.bytes, `Canonical private source drift ${asset.requested_name}.`);
  const wrapper = fs.readFileSync(path.join(ROOT, storagePath));
  assert(wrapper.subarray(0, wrapperPrefix.length).equals(wrapperPrefix), `Private wrapper header drift ${asset.requested_name}.`);
  const payload = wrapper.subarray(wrapperPrefix.length);
  assert(payload.byteLength === asset.bytes && sha256(payload) === asset.sha256, `Private wrapper payload drift ${asset.requested_name}.`);
  const direct = spawnSync("php", [path.join(ROOT, storagePath)], { encoding: null, windowsHide: true });
  assert(direct.status === 0 && direct.stdout.byteLength === 0, `Direct wrapper execution exposed payload ${asset.requested_name}.`);
  privateAssets.set(asset.requested_name, asset);
}
assert(JSON.stringify(project.asset_delivery.private_assets) === JSON.stringify(contract.private_assets), "Project package does not pin the private asset allowlist.");

const serialized = `${JSON.stringify(project)}\n${JSON.stringify(stage)}`;
assert(!/C:\\Users\\|\/Users\/|access[_-]?token|authorization\s*[:=]|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY/i.test(serialized), "Secret or local path found.");
assert(!/(?:olp|crm|webhook|tracking_pixel)/i.test(JSON.stringify(project.contracts)), "Internal delivery terminology found in public contracts.");

for (const component of Object.values(project.component_hashes)) {
  assert(fs.existsSync(path.join(ROOT, component.path)), `Missing component ${component.path}.`);
  assert(textFileSha(component.path) === component.sha256, `Hash drift for ${component.path}.`);
}

const { identity, representations, visual, buyer_decision: buyer, experiences } = project.contracts;
assert(identity.source_id === "einstein-tower-6885-32" && stage.body.meta.source_id === "", "Sandbox/catalog identity boundary failed.");
assert(identity.inventory_contract.decision_grade === false && JSON.parse(stage.body.meta.project_3d_units).length === 0, "Zero-inventory gate failed.");
assert(stage.body.meta.project_surface_version === "flagship-v3", "Surface selector mismatch.");
assert(stage.body.meta._nadlan_flagship_source_post_id === 4867, "Canonical-source marker mismatch.");

const expectedTools = ["view", "interior", "design", "comments"];
const expectedScenes = ["living", "bedroom", "arrival", "open-frame"];
const expectedHotspots = ["representative-interior-concept", "facility-arrival-concept", "facility-landscaped-open-space-concept"];
assert(JSON.stringify(visual.tools.map((tool) => tool.id)) === JSON.stringify(expectedTools), "Four-tool hierarchy mismatch.");
assert(visual.comments_delivery === "prepared_no_write" && visual.writes_enabled === false, "Comments must remain no-write.");
assert(JSON.stringify(experiences.scenes.map((scene) => scene.id)) === JSON.stringify(expectedScenes), "Experience-scene identity mismatch.");
assert(JSON.stringify([...new Set(experiences.scenes.map((scene) => scene.model_hotspot_group))]) === JSON.stringify(expectedHotspots), "Three-hotspot identity mismatch.");
assert(experiences.scenes.filter((scene) => scene.kind === "interior").length === 2, "Two interior scenes required.");
assert(experiences.scenes.filter((scene) => scene.kind === "facility").length === 2, "Two facility scenes required.");
assert(experiences.scenes.every((scene) => scene.mapping_state === "owner_approved_illustrative_mapping" && scene.decision_grade === false && scene.source_ids.length === 0), "Illustrative mapping truth state failed.");
assert(JSON.stringify(contract.required_experience_hotspot_groups) === JSON.stringify(expectedHotspots), "Trusted hotspot registry mismatch.");
assert(JSON.stringify(project.asset_delivery.allowed_evidence_reference_ids) === JSON.stringify(contract.illustrative_mapping_reference_ids), "Evidence allowlist mismatch.");

for (const representation of representations.representations) {
  const trusted = contract.authorized_representations.find((row) => row.role === representation.role);
  assert(trusted && trusted.sha256 === representation.sha256, `Untrusted representation ${representation.role}.`);
  const representationUrl = new URL(representation.url);
  assert(representation.url === `${privateAssetBase}${trusted.file}` && representationUrl.origin === "https://nad-lan.co.il" && representationUrl.search === "" && representationUrl.hash === "", "Representation path is not the exact query-free private route.");
  const descriptor = privateAssets.get(trusted.file);
  assert(descriptor && descriptor.bytes === trusted.bytes && descriptor.sha256 === trusted.sha256, `Representation private descriptor mismatch ${representation.role}.`);
}
for (const scene of experiences.scenes) {
  const trusted = contract.authorized_experience_assets.find((row) => row.asset_id === scene.asset_id);
  const mapping = contract.authorized_illustrative_mappings.find((row) => row.asset_id === scene.asset_id);
  assert(trusted && trusted.scene_id === scene.id, `Untrusted scene ${scene.id}.`);
  assert(mapping && mapping.model_hotspot_group === scene.model_hotspot_group, `Untrusted hotspot for ${scene.id}.`);
  assert(mapping.position === scene.model_hotspot.position && mapping.normal === scene.model_hotspot.normal, `Hotspot vector drift for ${scene.id}.`);
  assert(JSON.stringify(mapping.placement_confidence) === JSON.stringify(scene.placement_confidence), `Placement-confidence drift for ${scene.id}.`);
  const requestedName = `experience/${trusted.preview_file}`;
  const descriptor = privateAssets.get(requestedName);
  assert(descriptor && descriptor.bytes === trusted.bytes && descriptor.sha256 === trusted.preview_sha256, `Experience private descriptor mismatch ${scene.id}.`);
  assert(scene.preview_url === `${privateAssetBase}${requestedName}` && scene.fullscreen_url === scene.preview_url, `Experience path is not the exact query-free private route ${scene.id}.`);
}

const buyerSourceIds = new Set(buyer.sources.map((source) => source.id));
assert(buyer.facts.some((fact) => fact.id === "permit" && fact.value.includes("20241734") && fact.value.includes("בתהליך היתר")), "Current permit fact missing exact number/date-stage boundary.");
assert(buyer.facts.some((fact) => fact.id === "enabling-permit" && fact.value.includes("20240229")), "Enabling permit fact missing.");
const sourceLists = [];
const collect = (value) => {
  if (Array.isArray(value)) value.forEach(collect);
  else if (value && typeof value === "object") {
    if (Array.isArray(value.source_ids)) sourceLists.push(value.source_ids);
    Object.values(value).forEach(collect);
  }
};
collect(buyer);
assert(sourceLists.every((ids) => ids.length > 0 && ids.every((id) => buyerSourceIds.has(id))), "Buyer source resolution failed.");
assert(buyer.sources.every((source) => /^https:\/\/[^\s]+$/.test(source.url) && !source.url.includes("#")), "Buyer-source URL gate failed.");

const metaContracts = {
  project_identity_contract_json: identity,
  project_representation_registry_json: representations,
  project_visual_playground_json: visual,
  project_buyer_decision_contract_json: buyer,
  project_experience_registry_json: experiences,
};
for (const [key, expected] of Object.entries(metaContracts)) {
  assert(JSON.stringify(JSON.parse(stage.body.meta[key])) === JSON.stringify(expected), `${key} is not a lossless package projection.`);
}
assert(stage.contract_hashes.project_package_sha256 === textFileSha(packagePath), "Stage does not pin current project package.");
assert(stage.contract_hashes.article_sha256 === textFileSha("docs/wp-drafts/einstein-tower-he-content.html"), "Stage article hash mismatch.");
assert((stage.body.content.match(/<h1\b/gi) || []).length === 0, "Article must not contain H1.");
assert((stage.body.content.match(/data-nlfs-dossier="nadlan-einstein-he-dossier-v1"/g) || []).length === 1, "Article dossier marker mismatch.");
assert((stage.body.content.match(/הדמיה מאושרת/g) || []).length === 0, "Article contains a duplicate global demo label.");

const report = {
  ok: true,
  check: "einstein-flagship-project-and-private-stage",
  generated_at: "2026-08-14",
  project_contract_id: project.project_contract_id,
  canonical_post_id: 4867,
  private_stage_slug: stage.body.slug,
  private_stage_operation: stage.operation,
  counts: { buyer_sources: buyer.sources.length, tools: visual.tools.length, scenes: experiences.scenes.length, model_hotspots: expectedHotspots.length, inventory_rows: 0 },
  gates: {
    project_identity: "pass", current_permit_state: "pass", zero_inventory: "pass", model_hashes: "pass",
    four_tool_hierarchy: "pass", interior_facilities: "pass", illustrative_mapping: "pass", no_write: "pass",
    create_only_operation: "pass", sandbox_catalog_dedupe: "pass", password_secret_excluded: "pass", article_h1_and_disclosure_ownership: "pass",
    private_asset_proxy: "pass", private_asset_storage_hashes: "pass", direct_wrapper_execution_zero_bytes: "pass",
  },
  hashes: { project_package_sha256: textFileSha(packagePath), private_stage_sha256: textFileSha(stagePath) },
};
fs.writeFileSync(path.join(ROOT, reportPath), `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ ...report, report: reportPath, report_sha256: textFileSha(reportPath) }));
