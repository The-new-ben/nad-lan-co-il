import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const packagePath = "assets/projects/einstein-tower/contracts/flagship-project.json";
const stagePath = "docs/wp-drafts/einstein-tower-flagship-v3-private-stage.json";
const reportPath = "docs/qa/einstein-tower-flagship-stage-validation.json";
const read = (relative) => fs.readFileSync(path.join(ROOT, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const fileSha = (relative) => sha256(fs.readFileSync(path.join(ROOT, relative)));
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const project = readJson(packagePath);
const stage = readJson(stagePath);
const registry = readJson("plugins/nadlan-config/assets/flagship-v3/contracts/registry.json");
const contract = registry.contracts.find((row) => row.project_contract_id === project.project_contract_id);
assert(contract, "Trusted Einstein contract is missing.");
assert(project.schema === "nadlan-flagship-project-package/v1", "Project-package schema mismatch.");
assert(stage.schema === "nadlan-wordpress-private-stage-request/v1", "Private-stage schema mismatch.");
assert(project.project_contract_id === "einstein-tower-6885-32", "Project identity mismatch.");
assert(project.canonical.post_id === 4867 && project.canonical.slug === "einstein-tower", "Canonical target mismatch.");
assert(project.canonical.public_release_enabled === false, "Public release must remain disabled.");
assert(stage.lookup.exact_slug === "sandbox-einstein-tower-flagship-v3-review", "Sandbox slug mismatch.");
assert(stage.body.status === "publish" && !Object.hasOwn(stage.body, "password"), "Stage must be a password-injected published sandbox without a serialized secret.");
assert(stage.secret_injection.post_password.environment_variable === "SANDBOX_POST_PASSWORD", "Password injection contract mismatch.");

const serialized = `${JSON.stringify(project)}\n${JSON.stringify(stage)}`;
assert(!/C:\\Users\\|\/Users\/|access[_-]?token|authorization\s*[:=]|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY/i.test(serialized), "Secret or local path found.");
assert(!/(?:olp|crm|webhook|tracking_pixel)/i.test(JSON.stringify(project.contracts)), "Internal delivery terminology found in public contracts.");

for (const component of Object.values(project.component_hashes)) {
  assert(fs.existsSync(path.join(ROOT, component.path)), `Missing component ${component.path}.`);
  assert(fileSha(component.path) === component.sha256, `Hash drift for ${component.path}.`);
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
  assert(representation.url.startsWith("https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/flagship-v3/projects/einstein-tower/"), "Representation path is not same-origin and project-scoped.");
}
for (const scene of experiences.scenes) {
  const trusted = contract.authorized_experience_assets.find((row) => row.asset_id === scene.asset_id);
  const mapping = contract.authorized_illustrative_mappings.find((row) => row.asset_id === scene.asset_id);
  assert(trusted && trusted.scene_id === scene.id, `Untrusted scene ${scene.id}.`);
  assert(mapping && mapping.model_hotspot_group === scene.model_hotspot_group, `Untrusted hotspot for ${scene.id}.`);
  assert(mapping.position === scene.model_hotspot.position && mapping.normal === scene.model_hotspot.normal, `Hotspot vector drift for ${scene.id}.`);
  assert(JSON.stringify(mapping.placement_confidence) === JSON.stringify(scene.placement_confidence), `Placement-confidence drift for ${scene.id}.`);
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
assert(stage.contract_hashes.project_package_sha256 === fileSha(packagePath), "Stage does not pin current project package.");
assert(stage.contract_hashes.article_sha256 === fileSha("docs/wp-drafts/einstein-tower-he-content.html"), "Stage article hash mismatch.");
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
  counts: { buyer_sources: buyer.sources.length, tools: visual.tools.length, scenes: experiences.scenes.length, model_hotspots: expectedHotspots.length, inventory_rows: 0 },
  gates: {
    project_identity: "pass", current_permit_state: "pass", zero_inventory: "pass", model_hashes: "pass",
    four_tool_hierarchy: "pass", interior_facilities: "pass", illustrative_mapping: "pass", no_write: "pass",
    sandbox_catalog_dedupe: "pass", password_secret_excluded: "pass", article_h1_and_disclosure_ownership: "pass",
  },
  hashes: { project_package_sha256: fileSha(packagePath), private_stage_sha256: fileSha(stagePath) },
};
fs.writeFileSync(path.join(ROOT, reportPath), `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ ...report, report: reportPath, report_sha256: fileSha(reportPath) }));
