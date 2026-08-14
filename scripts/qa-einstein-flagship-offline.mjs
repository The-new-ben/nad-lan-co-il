import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, "..");
const previewPath = "docs/previews/einstein-tower-flagship-offline.html";
const runtimePath = path.join(repoRoot, "assets/showroom/flagship-showroom-runtime.js");
const modelPath = path.join(repoRoot, "assets/projects/einstein-tower/model-hd.glb");
const posterPath = path.join(repoRoot, "assets/projects/einstein-tower/poster.webp");
const experienceFiles = [
  { name: "representative-apartment-living-v1.webp", size: 103748, sha: "1ad84512b5cb938450b5124c199ba09d00697da605ef46214434cef80649319b", group: "interior", id: "living" },
  { name: "representative-apartment-bedroom-v1.webp", size: 79384, sha: "1c4d71c6b1308867a2a9c9d1d03eec947ba6f85b9800fa1f88ae5028acf06aea", group: "interior", id: "bedroom" },
  { name: "facility-arrival-gallery-v1.webp", size: 170750, sha: "cc50acc2570612165bf20442849ac9fcdf00658c0835f2130d6824d8b2c50e9a", group: "facilities", id: "arrival" },
  { name: "facility-landscaped-terrace-v1.webp", size: 264926, sha: "717a33f6deb118e3d60539152147a7d1c791e84b69e77861f6086ae246cc8e0b", group: "facilities", id: "open-frame" }
];
const artifactDir = path.join(repoRoot, "output/playwright/einstein-flagship-offline");
const writeArtifacts = process.env.NL_EINSTEIN_WRITE_ARTIFACTS === "1";
const chromePath = process.env.NL_EINSTEIN_CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const viewports = [
  { name: "320x568", width: 320, height: 568, touch: true },
  { name: "390x844", width: 390, height: 844, touch: true },
  { name: "568x320", width: 568, height: 320, touch: true },
  { name: "1280x800", width: 1280, height: 800, touch: false }
].filter((viewport) => !process.env.NL_EINSTEIN_VIEWPORT || viewport.name === process.env.NL_EINSTEIN_VIEWPORT);
if (!viewports.length) throw new Error("NL_EINSTEIN_VIEWPORT did not match a configured viewport.");

function fixtureData(projectContractId = "einstein-tower-6885-32") {
  const common = { decision_grade: false, open_label: "פתחו", disclosure: "מידע נגיש בלבד" };
  return {
    identity: { project_contract_id: projectContractId, public_slug: "einstein-tower", representation_name: "Einstein 33A" },
    decision: { owner_decision_id: "OWNER-2026-08-13-VISUAL-PLAYGROUND", approved_by: "site_owner", decision_grade: false, version: "visual-playground-v1", effective_at: "2026-08-13T00:00:00+03:00", expires_at: "2026-12-15T23:59:59+02:00" },
    experience_decision: { owner_decision_id: "OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO", approved_by: "site_owner", representation_kind: "owner_approved_illustration", decision_grade: false, version: "einstein-interior-facilities-demo-v1", effective_at: "2026-08-14T00:00:00+03:00", expires_at: "2027-08-14T00:00:00+03:00" },
    experience_assets: {
      interior: { representation_kind: "representative_concept", experience_kind: "representative_concept", mapping_state: "owner_approved_illustrative_mapping", decision_grade: false, scenes: [
        { id: "living", asset_id: "representative-apartment-living-v1", label: "חלל מגורים", url: "/assets/projects/einstein-tower/experience/representative-apartment-living-v1.webp", sha256: "1ad84512b5cb938450b5124c199ba09d00697da605ef46214434cef80649319b", bytes: 103748, width: 1536, height: 1024, experience_kind: "representative_concept", hotspot_id: "representative-interior-concept", open_surface_tool_id: "interior", illustrative_position: [16, 34.7, 5.8], mapping_state: "owner_approved_illustrative_mapping", decision_grade: false },
        { id: "bedroom", asset_id: "representative-apartment-bedroom-v1", label: "חדר ושולחן עבודה", url: "/assets/projects/einstein-tower/experience/representative-apartment-bedroom-v1.webp", sha256: "1c4d71c6b1308867a2a9c9d1d03eec947ba6f85b9800fa1f88ae5028acf06aea", bytes: 79384, width: 1523, height: 1024, experience_kind: "representative_concept", hotspot_id: "representative-interior-concept", open_surface_tool_id: "interior", illustrative_position: [16, 34.7, 5.8], mapping_state: "owner_approved_illustrative_mapping", decision_grade: false }
      ] },
      facilities: { representation_kind: "selectable_concept_gallery", experience_kind: "selectable_concept_gallery", mapping_state: "owner_approved_illustrative_mapping", decision_grade: false, scenes: [
        { id: "arrival", asset_id: "facility-arrival-gallery-v1", label: "מרחב כניסה משותף", url: "/assets/projects/einstein-tower/experience/facility-arrival-gallery-v1.webp", sha256: "cc50acc2570612165bf20442849ac9fcdf00658c0835f2130d6824d8b2c50e9a", bytes: 170750, width: 1524, height: 1024, experience_kind: "selectable_concept_gallery", hotspot_id: "facility-arrival-concept", open_surface_tool_id: "interior", illustrative_position: [12, 9.5, -13.25], mapping_state: "owner_approved_illustrative_mapping", decision_grade: false },
        { id: "open-frame", asset_id: "facility-landscaped-terrace-v1", label: "מרחב פתוח משותף", url: "/assets/projects/einstein-tower/experience/facility-landscaped-terrace-v1.webp", sha256: "717a33f6deb118e3d60539152147a7d1c791e84b69e77861f6086ae246cc8e0b", bytes: 264926, width: 1518, height: 1024, experience_kind: "selectable_concept_gallery", hotspot_id: "facility-landscaped-open-space-concept", open_surface_tool_id: "interior", illustrative_position: [27, 10, 14], mapping_state: "owner_approved_illustrative_mapping", decision_grade: false }
      ] }
    },
    experience_mapping: {
      active_state: "owner_approved_illustrative_mapping", future_verified_state: "source_cited_mapping", coordinate_space: "model_metres_y_up", source_cited: false, decision_grade: false, real_world_orientation_calibrated: false,
      anchors: [
        { hotspot_id: "representative-interior-concept", tool_id: "interior", open_surface_tool_id: "interior", kind: "interior_walkthrough", experience_kind: "representative_concept", scene_ids: ["living", "bedroom"], model_component_ids: ["Tower_28_Level_Massing", "Glass_Terrace_Strips", "Champagne_Fins"], illustrative_zone_id: "tower_local_plus_z_glass_terrace_face", position: [16,34.7,5.8], surface_normal: [0,0,1], visual_offset_along_normal_m: .7, confidence: "model_zone_fit_high__source_spatial_confidence_none", placement_confidence: { zone: .68, exact_point: .18 }, evidence_basis: { primary_reference_ids: ["MR001"], corroborating_reference_ids: ["MR002","MR003","MR018"], supports: "Authored tower component and local glass/terrace facade family only; no room or spatial placement." }, ambiguity: "Owner interpolation on the authored glass/terrace facade family. The marker alone is offset outward for visibility; model +Z is not a calibrated real-world direction.", prohibited_inferences: ["floor number","unit or room identity","interior specification","balcony access","compass or street aspect","sea or city view","availability"] },
        { hotspot_id: "facility-arrival-concept", tool_id: "facilities", open_surface_tool_id: "interior", kind: "facility_arrival_concept", experience_kind: "selectable_concept_gallery", scene_ids: ["arrival"], model_component_ids: ["Tower_28_Level_Massing", "Podium_Double_Level"], illustrative_zone_id: "tower_podium_local_minus_z_residential_level_seam", position: [12,9.5,-13.25], surface_normal: [0,0,-1], visual_offset_along_normal_m: .45, confidence: "model_zone_fit_high__source_spatial_confidence_none", placement_confidence: { zone: .63, exact_point: .20 }, evidence_basis: { primary_reference_ids: ["MR008"], corroborating_reference_ids: ["MR002","MR003","MR019"], source_anchors: ["MR008 PDF p57 lines 1564-1567"], supports: "Municipal protocol separates residential/public entrances at neighborhood level from commerce at Einstein street level; the exact door/anchor remains owner interpolation on the authored tower/podium seam." }, ambiguity: "Owner interpolation at an authored tower/podium seam. Model -Z is not a calibrated frontage or real-world direction.", prohibited_inferences: ["verified facility existence","official lobby or named amenity","official entrance or doorway","floor or room location","street frontage","plaza or cycle path","accessible route","delivery commitment"] },
        { hotspot_id: "facility-landscaped-open-space-concept", tool_id: "facilities", open_surface_tool_id: "interior", kind: "facility_landscaped_open_space_concept", experience_kind: "selectable_concept_gallery", scene_ids: ["open-frame"], model_component_ids: ["Landscape_Terraces", "Podium_Double_Level"], illustrative_zone_id: "landscape_terrace_local_top_surface", position: [27,10,14], surface_normal: [0,1,0], visual_offset_along_normal_m: .35, confidence: "model_zone_fit_high__source_spatial_confidence_none", placement_confidence: { zone: .86, exact_point: .24 }, evidence_basis: { primary_reference_ids: ["MR003","MR008"], corroborating_reference_ids: ["MR019"], source_anchors: ["MR008 PDF p55 lines 1495-1499","MR008 PDF p51 lines 1396-1404","MR008 PDF pp62-63 lines 1653-1657"], supports: "Municipal protocol requires an accessible active commercial roof/fifth facade, pedestrian/cycle grade transition and planted/seated lot-33 open space; the exact authored landscape-volume anchor remains owner interpolation and is not a named amenity." }, ambiguity: "Owner interpolation on an authored landscape volume. It is not a verified roof amenity, view location or delivered public realm.", prohibited_inferences: ["verified facility existence","named roof or amenity","official floor or location","private or shared ownership","view promise","landscape specification","plaza or cycle path","delivery commitment"] }
      ]
    },
    tools: [
      { ...common, id: "view", preview_kind: "schematic_live_map", title: "מבט", description: "מפה" },
      { ...common, id: "interior", preview_kind: "first_person_door", title: "פנים", description: "מסלול" },
      { ...common, id: "design", preview_kind: "illustrative_plan_drag", title: "עיצוב", description: "תוכנית" },
      { ...common, id: "comments", preview_kind: "visual_annotation_request", title: "הערות", description: "שאלה" }
    ]
  };
}

const require = createRequire(import.meta.url);
const runtime = require(runtimePath);
const frozenNow = Date.parse("2026-08-14T12:00:00+03:00");
const allowedEvidenceReferenceIds = ["MR001", "MR002", "MR003", "MR008", "MR018", "MR019"];
const allowedAssetPrefix = "/assets/projects/einstein-tower/experience/";
const normalizeFixture = (data = fixtureData(), evidenceIds = allowedEvidenceReferenceIds, assetPrefix = allowedAssetPrefix) => runtime.normalizeConfig(data, frozenNow, "einstein-tower-6885-32", evidenceIds, assetPrefix);
assert.throws(() => runtime.normalizeConfig(fixtureData(), frozenNow), /expectedProjectContractId/);
assert.throws(() => runtime.normalizeConfig(fixtureData("wrong-project"), frozenNow, "einstein-tower-6885-32", allowedEvidenceReferenceIds, allowedAssetPrefix), /does not match/);
const wrongExperience = fixtureData(); wrongExperience.experience_decision.owner_decision_id = "wrong";
assert.throws(() => normalizeFixture(wrongExperience), /experience decision/);
const externalAsset = fixtureData(); externalAsset.experience_assets.interior.scenes[0].url = "https://example.com/tracker.webp";
assert.throws(() => normalizeFixture(externalAsset), /experience scene/);
const crossProjectAsset = fixtureData(); crossProjectAsset.experience_assets.interior.scenes[0].url = "/assets/projects/another-project/experience/representative-apartment-living-v1.webp";
assert.throws(() => normalizeFixture(crossProjectAsset), /experience scene/);
for (const field of ["asset_id", "sha256", "bytes", "width", "height"]) {
  const invalidEvidence = fixtureData(); delete invalidEvidence.experience_assets.interior.scenes[0][field];
  assert.throws(() => normalizeFixture(invalidEvidence), /experience scene/, `missing ${field} must fail closed`);
}
for (const [field, value] of [["sha256", "ABC"], ["bytes", 0], ["width", -1], ["height", 1.5], ["asset_id", "../escape"]]) {
  const invalidEvidence = fixtureData(); invalidEvidence.experience_assets.interior.scenes[0][field] = value;
  assert.throws(() => normalizeFixture(invalidEvidence), /experience scene/, `invalid ${field} must fail closed`);
}
const duplicateAssetId = fixtureData(); duplicateAssetId.experience_assets.facilities.scenes[0].asset_id = duplicateAssetId.experience_assets.interior.scenes[0].asset_id; duplicateAssetId.experience_assets.facilities.scenes[0].url = duplicateAssetId.experience_assets.interior.scenes[0].url;
assert.throws(() => normalizeFixture(duplicateAssetId), /experience scene/);
const duplicateAssetUrl = fixtureData(); duplicateAssetUrl.experience_assets.facilities.scenes[0].url = duplicateAssetUrl.experience_assets.interior.scenes[0].url;
assert.throws(() => normalizeFixture(duplicateAssetUrl), /experience scene/);
for (const value of [undefined, "facilities"]) {
  const invalidSurface = fixtureData();
  if (value === undefined) delete invalidSurface.experience_assets.interior.scenes[0].open_surface_tool_id;
  else invalidSurface.experience_assets.interior.scenes[0].open_surface_tool_id = value;
  assert.throws(() => normalizeFixture(invalidSurface), /experience scene/, "scene open_surface_tool_id must fail closed");
}
for (const value of [undefined, "facilities"]) {
  const invalidSurface = fixtureData();
  if (value === undefined) delete invalidSurface.experience_mapping.anchors[0].open_surface_tool_id;
  else invalidSurface.experience_mapping.anchors[0].open_surface_tool_id = value;
  assert.throws(() => normalizeFixture(invalidSurface), /mapping anchor/, "anchor open_surface_tool_id must fail closed");
}
const missingAnchor = fixtureData(); missingAnchor.experience_mapping.anchors.pop();
assert.throws(() => normalizeFixture(missingAnchor), /mapping policy/);
const extraAnchor = fixtureData(); extraAnchor.experience_mapping.anchors.push({ ...extraAnchor.experience_mapping.anchors[2], hotspot_id: "extra-anchor" });
assert.throws(() => normalizeFixture(extraAnchor), /mapping policy/);
const fifthTool = fixtureData(); fifthTool.tools.push({ decision_grade: false, id: "facilities", preview_kind: "facility_concept_gallery", title: "חללים", description: "רעיונות", open_label: "פתחו", disclosure: "נגיש" });
assert.throws(() => normalizeFixture(fifthTool), /exactly view/);
const duplicateTool = fixtureData(); duplicateTool.tools[3] = { ...duplicateTool.tools[0] };
assert.throws(() => normalizeFixture(duplicateTool), /exactly view/);
const missingTool = fixtureData(); missingTool.tools.pop();
assert.throws(() => normalizeFixture(missingTool), /exactly view/);
const wrongExpiry = fixtureData(); wrongExpiry.experience_decision.expires_at = "2026-08-14T11:00:00+03:00";
assert.throws(() => normalizeFixture(wrongExpiry), /experience decision/);
assert.throws(() => runtime.normalizeConfig(fixtureData(), frozenNow, "einstein-tower-6885-32", undefined, allowedAssetPrefix), /allowedEvidenceReferenceIds/);
for (const invalidList of [[], ["MR001", "MR001"], ["bad ref"]]) assert.throws(() => normalizeFixture(fixtureData(), invalidList), /allowedEvidenceReferenceIds/);
assert.throws(() => normalizeFixture(fixtureData(), allowedEvidenceReferenceIds.slice(1)), /mapping anchor|exactly match/);
assert.throws(() => normalizeFixture(fixtureData(), allowedEvidenceReferenceIds.concat("UNUSED")), /exactly match/);
const unauthorizedEvidence = fixtureData(); unauthorizedEvidence.experience_mapping.anchors[0].evidence_basis.primary_reference_ids[0] = "UNAUTHORIZED";
assert.throws(() => normalizeFixture(unauthorizedEvidence), /mapping anchor/);
for (const invalidConfidence of [undefined, { zone: -0.01, exact_point: .18 }, { zone: .68, exact_point: 1.01 }, { zone: "0.68", exact_point: .18 }]) {
  const invalidPlacement = fixtureData();
  if (invalidConfidence === undefined) delete invalidPlacement.experience_mapping.anchors[0].placement_confidence;
  else invalidPlacement.experience_mapping.anchors[0].placement_confidence = invalidConfidence;
  assert.throws(() => normalizeFixture(invalidPlacement), /mapping anchor/, "placement confidence must fail closed");
}
assert.throws(() => runtime.normalizeConfig(fixtureData(), frozenNow, "einstein-tower-6885-32", allowedEvidenceReferenceIds, undefined), /allowedAssetPrefix/);
for (const invalidPrefix of ["", "https://example.com/assets/", "//example.com/assets/", "/assets/../escape/", "/assets/%2e%2e/escape/", "/assets/%2fescape/", "/assets//escape/", "/assets\\escape/", "/assets/path/?q=1", "/assets/path/#fragment"]) assert.throws(() => normalizeFixture(fixtureData(), allowedEvidenceReferenceIds, invalidPrefix), /allowedAssetPrefix/);
assert.throws(() => normalizeFixture(fixtureData(), allowedEvidenceReferenceIds, "/assets/projects/another-project/experience/"), /experience scene/);
const normalizedFixture = normalizeFixture();
assert.equal(normalizedFixture.identity.projectContractId, "einstein-tower-6885-32");
assert.deepEqual(normalizedFixture.tools.map((tool) => tool.id), ["view", "interior", "design", "comments"]);
assert.ok(normalizedFixture.experienceAssets.interior.scenes.concat(normalizedFixture.experienceAssets.facilities.scenes).every((scene) => scene.openSurfaceToolId === "interior"));
assert.deepEqual(normalizedFixture.experienceMapping.anchors.map((anchor) => anchor.placementConfidence), [{ zone: .68, exactPoint: .18 }, { zone: .63, exactPoint: .20 }, { zone: .86, exactPoint: .24 }]);

const [modelStat, posterStat, runtimeSource, modelBytes, posterBytes] = await Promise.all([
  fs.stat(modelPath), fs.stat(posterPath), fs.readFile(runtimePath, "utf8"), fs.readFile(modelPath), fs.readFile(posterPath)
]);
assert.ok(modelStat.size > 1024, "The real local GLB must be present and nontrivial.");
assert.ok(posterStat.size > 1024, "The local poster must be present and nontrivial.");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
assert.equal(modelStat.size, 2420492); assert.equal(sha256(modelBytes), "71fcca8a0f58743b5f2257684c79957fbbff8e0169f5438bdc78231f27968a53");
assert.equal(posterStat.size, 23996); assert.equal(sha256(posterBytes), "5588d09e28f95ac5d6655626027c3ad41f17c5c5c78153ecb2ba138821aa8c85");
const experienceEvidence = await Promise.all(experienceFiles.map(async (asset) => {
  const assetPath = path.join(repoRoot, "assets/projects/einstein-tower/experience", asset.name);
  const [stat, bytes] = await Promise.all([fs.stat(assetPath), fs.readFile(assetPath)]);
  assert.equal(stat.size, asset.size, `${asset.name}: frozen byte length`);
  assert.equal(sha256(bytes), asset.sha, `${asset.name}: frozen sha256`);
  return { ...asset, path: assetPath };
}));
function glbJson(buffer) {
  assert.equal(buffer.readUInt32LE(0), 0x46546c67, "Model must be a GLB.");
  let offset = 12;
  while (offset < buffer.length) {
    const length = buffer.readUInt32LE(offset), type = buffer.readUInt32LE(offset + 4);
    if (type === 0x4e4f534a) return JSON.parse(buffer.subarray(offset + 8, offset + 8 + length).toString("utf8").replace(/\0+$/, ""));
    offset += 8 + length;
  }
  throw new Error("GLB JSON chunk is missing.");
}
const modelJson = glbJson(modelBytes);
const triangleCount = (modelJson.meshes || []).flatMap((mesh) => mesh.primitives || []).reduce((sum, primitive) => {
  if (primitive.mode != null && primitive.mode !== 4) return sum;
  const accessor = primitive.indices == null ? modelJson.accessors?.[primitive.attributes?.POSITION] : modelJson.accessors?.[primitive.indices];
  return sum + Math.floor((accessor?.count || 0) / 3);
}, 0);
assert.equal(triangleCount, 39912);
const sceneExtras = modelJson.scenes?.[modelJson.scene || 0]?.extras || {};
assert.equal(sceneExtras.placement_calibration_state, "not_municipally_crosswalked");
const mappedHotspotEvidence = (sceneExtras.concept_hotspots || []).map((hotspot) => ({
  hotspotId: hotspot.hotspot_id, toolId: hotspot.tool_id, openSurfaceToolId: hotspot.open_surface_tool_id, kind: hotspot.kind, experienceKind: hotspot.experience_kind,
  sceneIds: hotspot.scene_ids, modelComponentIds: hotspot.model_component_ids, illustrativeZoneId: hotspot.illustrative_zone_id,
  position: hotspot.position, surfaceNormal: hotspot.surface_normal, visualOffsetAlongNormalM: hotspot.visual_offset_along_normal_m,
  confidence: hotspot.confidence, placementConfidence: { zone: hotspot.placement_confidence.zone, exactPoint: hotspot.placement_confidence.exact_point }, evidenceReferenceIds: (hotspot.evidence_basis.primary_reference_ids || []).concat(hotspot.evidence_basis.corroborating_reference_ids || []),
  sourceAnchors: hotspot.evidence_basis.source_anchors || [], evidenceSupports: hotspot.evidence_basis.supports,
  ambiguity: hotspot.ambiguity, prohibitedInferences: hotspot.prohibited_inferences,
  mappingState: hotspot.mapping_state, futureVerifiedState: hotspot.future_verified_state, coordinateSpace: hotspot.coordinate_space,
  realWorldOrientationCalibrated: hotspot.real_world_orientation_calibrated, sourceCited: hotspot.source_cited, decisionGrade: hotspot.decision_grade,
  ownerDecisionId: hotspot.owner_decision_id, version: hotspot.version, effectiveAt: hotspot.effective_at, expiresAt: hotspot.expires_at
}));
assert.deepEqual(mappedHotspotEvidence, normalizedFixture.experienceMapping.anchors.map((anchor) => ({
  ...anchor, mappingState: "owner_approved_illustrative_mapping", futureVerifiedState: "source_cited_mapping", coordinateSpace: "model_metres_y_up",
  realWorldOrientationCalibrated: false, sourceCited: false, decisionGrade: false,
  ownerDecisionId: "OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO", version: "einstein-interior-facilities-demo-v1",
  effectiveAt: "2026-08-14T00:00:00+03:00", expiresAt: "2027-08-14T00:00:00+03:00"
})));
for (const forbidden of [/\bfetch\s*\(/, /XMLHttpRequest/, /sendBeacon/, /\bWebSocket\b/, /localStorage/, /sessionStorage/]) {
  assert.equal(forbidden.test(runtimeSource), false, `Runtime contains forbidden I/O surface: ${forbidden}`);
}

const mime = new Map([
  [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
  [".css", "text/css; charset=utf-8"], [".glb", "model/gltf-binary"], [".webp", "image/webp"]
]);
const requests = [];
const server = http.createServer(async (request, response) => {
  try {
    const url = new URL(request.url || "/", "http://127.0.0.1");
    if (url.pathname === "/favicon.ico") { response.writeHead(204); response.end(); return; }
    const relative = decodeURIComponent(url.pathname.replace(/^\/+/, "")) || previewPath;
    const resolved = path.resolve(repoRoot, relative);
    if (resolved !== repoRoot && !resolved.startsWith(repoRoot + path.sep)) throw new Error("unsafe path");
    const bytes = await fs.readFile(resolved);
    requests.push({ method: request.method, pathname: url.pathname, status: 200, bytes: bytes.length });
    response.writeHead(200, { "content-type": mime.get(path.extname(resolved).toLowerCase()) || "application/octet-stream", "content-length": bytes.length, "cache-control": "no-store" });
    response.end(bytes);
  } catch (_error) {
    requests.push({ method: request.method, pathname: request.url, status: 404, bytes: 0 });
    response.writeHead(404); response.end("not found");
  }
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const origin = `http://127.0.0.1:${server.address().port}`;

let browser;
try {
  browser = await chromium.launch({ headless: true, executablePath: chromePath, args: ["--use-angle=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"] });
  if (writeArtifacts) { await fs.rm(artifactDir, { recursive: true, force: true }); await fs.mkdir(artifactDir, { recursive: true }); }

  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, hasTouch: viewport.touch, locale: "he-IL", colorScheme: "light" });
    await context.addInitScript(() => {
      window.__ioAudit = { fetch: [], xhr: [], beacon: [], socket: [], storage: [] };
      const nativeFetch = window.fetch.bind(window);
      window.fetch = function (...args) { window.__ioAudit.fetch.push({ url: String(args[0]), method: String(args[1]?.method || "GET") }); return nativeFetch(...args); };
      const nativeOpen = XMLHttpRequest.prototype.open;
      XMLHttpRequest.prototype.open = function (method, url, ...rest) { window.__ioAudit.xhr.push({ method: String(method), url: String(url) }); return nativeOpen.call(this, method, url, ...rest); };
      const nativeBeacon = navigator.sendBeacon?.bind(navigator);
      if (nativeBeacon) navigator.sendBeacon = function (...args) { window.__ioAudit.beacon.push(String(args[0])); return nativeBeacon(...args); };
      const NativeWebSocket = window.WebSocket;
      window.WebSocket = function (...args) { window.__ioAudit.socket.push(String(args[0])); return new NativeWebSocket(...args); };
      window.WebSocket.prototype = NativeWebSocket.prototype;
      for (const method of ["setItem", "removeItem", "clear"]) {
        const native = Storage.prototype[method];
        Storage.prototype[method] = function (...args) { window.__ioAudit.storage.push({ name: this === localStorage ? "local" : "session", method, key: String(args[0] || "") }); return native.apply(this, args); };
      }
    });
    const page = await context.newPage();
    const pageErrors = [];
    const consoleErrors = [];
    const browserRequests = [];
    const experienceResponses = [];
    page.on("pageerror", (error) => pageErrors.push(error.message));
    page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); });
    page.on("request", (request) => browserRequests.push(request.url()));
    page.on("response", (response) => {
      const pathname = new URL(response.url()).pathname;
      const asset = experienceEvidence.find((candidate) => pathname.endsWith(`/assets/projects/einstein-tower/experience/${candidate.name}`));
      if (asset) experienceResponses.push(response.body().then((bytes) => ({ name: asset.name, status: response.status(), bytes: bytes.length, sha: sha256(bytes) })));
    });
    await page.goto(`${origin}/${previewPath}`, { waitUntil: "networkidle" });
    await page.waitForFunction(() => document.querySelector("[data-nlvt-protected-model]")?.dataset.modelLoad === "loaded", null, { timeout: 20000 });
    assert.deepEqual(pageErrors, [], `${viewport.name}: page errors`);
    assert.deepEqual(consoleErrors, [], `${viewport.name}: console errors`);

    const base = await page.evaluate((expectedBytes) => {
      const protectedStage = document.querySelector("[data-nlvt-protected-model]");
      const root = document.querySelector("[data-nlvt-root]");
      const stageRect = protectedStage.getBoundingClientRect();
      const rootRect = root.getBoundingClientRect();
      const hit = document.elementFromPoint(stageRect.left + stageRect.width / 2, stageRect.top + stageRect.height / 2);
      const visibleTeasers = [...root.querySelectorAll(".nlvt-teaser")].filter((node) => !node.hidden && getComputedStyle(node).display !== "none");
      const smallText = [...document.querySelectorAll("body *")].filter((node) => {
        if (!node.childNodes || ![...node.childNodes].some((child) => child.nodeType === Node.TEXT_NODE && child.textContent.trim())) return false;
        if (node.closest(".nlvt-visually-hidden,.nlef-visually-hidden,[hidden]")) return false;
        const style = getComputedStyle(node), rect = node.getBoundingClientRect();
        return style.display !== "none" && style.visibility !== "hidden" && rect.width > 2 && rect.height > 2 && parseFloat(style.fontSize) < 12;
      }).map((node) => ({ tag: node.tagName, text: node.textContent.trim().slice(0, 60), size: getComputedStyle(node).fontSize }));
      const targets = [...root.querySelectorAll("button")].filter((node) => { const rect=node.getBoundingClientRect(); return !node.closest("[hidden]") && getComputedStyle(node).display !== "none" && rect.width > 0 && rect.height > 0; }).map((node) => ({ text: node.textContent.trim(), width: node.getBoundingClientRect().width, height: node.getBoundingClientRect().height }));
      const demonstrationLabels = [...document.querySelectorAll("body *")].filter((node) => {
        if (node.closest(".nlvt-visually-hidden,.nlef-visually-hidden,[hidden]")) return false;
        const ownText=[...node.childNodes].filter((child)=>child.nodeType===Node.TEXT_NODE).map((child)=>child.textContent).join(" ").trim();
        if (!/(?:המחשה|הדגמה)/.test(ownText)) return false;
        const style=getComputedStyle(node),rect=node.getBoundingClientRect();
        return style.display!=="none"&&style.visibility!=="hidden"&&rect.width>2&&rect.height>2;
      }).map((node)=>node.textContent.trim());
      const clipped = visibleTeasers.filter((node) => { const rect=node.getBoundingClientRect(); return rect.left < -1 || rect.right > innerWidth + 1 || rect.top < -1 || rect.bottom > innerHeight + 1; }).map((node) => { const rect=node.getBoundingClientRect(),scene=document.querySelector(".nlef-scene").getBoundingClientRect(),model=document.querySelector(".nlef-model").getBoundingClientRect(),rootRect=root.getBoundingClientRect(); return { tool:node.dataset.nlvtTool,left:rect.left,right:rect.right,top:rect.top,bottom:rect.bottom,innerWidth,innerHeight,landscape:matchMedia("(orientation: landscape) and (max-height: 640px)").matches,scene:{top:scene.top,bottom:scene.bottom,height:scene.height},model:{top:model.top,bottom:model.bottom,height:model.height},root:{top:rootRect.top,bottom:rootRect.bottom,height:rootRect.height} }; });
      const scrollers = [...document.querySelectorAll("body *")].filter((node) => {
        if (node === document.body || node === document.documentElement) return false;
        const style = getComputedStyle(node), y = style.overflowY, x = style.overflowX;
        return ((y === "auto" || y === "scroll") && node.scrollHeight > node.clientHeight + 1) || ((x === "auto" || x === "scroll") && node.scrollWidth > node.clientWidth + 1);
      }).map((node) => node.className || node.tagName);
      return {
        modelLoad: protectedStage.dataset.modelLoad, modelHttpStatus: protectedStage.dataset.modelHttpStatus,
        modelBytes: Number(protectedStage.dataset.modelBytes), modelMeshes: Number(protectedStage.dataset.modelMeshes), expectedBytes,
        sibling: protectedStage.closest(".nlef-model").nextElementSibling === root,
        overlap: stageRect.left < rootRect.right - .5 && stageRect.right > rootRect.left + .5 && stageRect.top < rootRect.bottom - .5 && stageRect.bottom > rootRect.top + .5,
        hitInside: protectedStage.contains(hit), protectedDecision: protectedStage.dataset.modelDecision,
        protectedGrade: protectedStage.dataset.decisionGrade, teaserCount: root.querySelectorAll(".nlvt-teaser").length,
        visibleTeaserCount: visibleTeasers.length, smallText, targets, scrollers, clipped,
        disclosureCount: [...root.querySelectorAll(".nlvt-disclosure")].filter((node) => { const rect=node.getBoundingClientRect(); return rect.width > 0 && rect.height > 0; }).length, demonstrationLabels,
        bodyOverflowX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        title: document.querySelector("h1")?.textContent || "", bodyText: document.body.innerText
      };
    }, modelStat.size);
    assert.equal(base.modelLoad, "loaded", `${viewport.name}: model load`);
    assert.equal(base.modelHttpStatus, "200", `${viewport.name}: real GLB HTTP status`);
    assert.equal(base.modelBytes, base.expectedBytes, `${viewport.name}: complete GLB bytes`);
    assert.ok(base.modelMeshes > 0, `${viewport.name}: parsed GLB meshes`);
    assert.equal(base.sibling, true, `${viewport.name}: teaser root follows protected model component`);
    assert.equal(base.overlap, false, `${viewport.name}: teasers overlap protected model`);
    assert.equal(base.hitInside, true, `${viewport.name}: model center remains hit-testable`);
    assert.equal(base.protectedDecision, "OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING");
    assert.equal(base.protectedGrade, "false");
    assert.equal(base.teaserCount, 4);
    assert.equal(base.visibleTeaserCount, viewport.width <= 700 || viewport.height <= 640 ? 1 : 4);
    assert.equal(await page.locator('[data-nlvt-root] [data-nlvt-tool="facilities"],[data-nlvt-root] [data-nlvt-open="facilities"]').count(), 0, `${viewport.name}: facilities must not be a top-level tile`);
    assert.deepEqual(base.smallText, [], `${viewport.name}: visible text below 12px`);
    assert.ok(base.targets.every((target) => target.width >= 43.5 && target.height >= 43.5), `${viewport.name}: 44px target failure ${JSON.stringify(base.targets)}`);
    assert.deepEqual(base.scrollers, [], `${viewport.name}: inner scrollers`);
    assert.deepEqual(base.clipped, [], `${viewport.name}: clipped teaser`);
    assert.equal(base.disclosureCount, 1, `${viewport.name}: exactly one visible showroom illustration disclosure`);
    assert.deepEqual(base.demonstrationLabels, ["הדגמה חזותית מאושרת · אינה מידע תכנוני או מלאי"], `${viewport.name}: repeated visible demonstration caveat`);
    assert.ok(base.bodyOverflowX <= 1, `${viewport.name}: horizontal overflow ${base.bodyOverflowX}px`);
    assert.match(base.title, /Einstein Tower \/ Einstein 33A/);
    assert.doesNotMatch(base.bodyText, /Einstein 18/i);
    assert.equal(await page.locator('[data-nlvt-root] [data-unit],[data-nlvt-root] [data-floor],[data-nlvt-root] [data-inventory]').count(), 0);

    const mappedHotspots = await page.evaluate(() => window.__EinsteinFlagshipPreview.getMappedHotspots());
    assert.equal(mappedHotspots.length, 3, `${viewport.name}: governed model hotspot count`);
    assert.deepEqual(mappedHotspots.map((hotspot) => hotspot.hotspotId), ["representative-interior-concept", "facility-arrival-concept", "facility-landscaped-open-space-concept"]);
    assert.ok(mappedHotspots.every((hotspot) => hotspot.openSurfaceToolId === "interior" && hotspot.mappingState === "owner_approved_illustrative_mapping" && hotspot.futureVerifiedState === "source_cited_mapping" && hotspot.sourceCited === false));
    assert.equal(await page.locator("[data-model-hotspots]").getAttribute("aria-hidden"), "true");
    assert.equal(await page.locator("[data-model-hotspots]").evaluate((node) => getComputedStyle(node).pointerEvents), "none", `${viewport.name}: overlay canvas must not intercept model input`);
    assert.equal(await page.locator("[data-nlvt-protected-model]").getAttribute("data-model-hotspot-count"), "3");
    const hotspotRegions = await page.evaluate(() => window.__EinsteinFlagshipPreview.getModelHotspotRegions());
    assert.equal(hotspotRegions.length, 3);
    for (let a = 0; a < hotspotRegions.length; a++) for (let b = a + 1; b < hotspotRegions.length; b++) assert.ok(Math.hypot(hotspotRegions[a].x-hotspotRegions[b].x,hotspotRegions[a].y-hotspotRegions[b].y)>=47.5, `${viewport.name}: projected hotspot collision`);

    for (const hotspot of mappedHotspots) {
      const modelBefore = await page.evaluate((hotspotId) => {
        const state=window.__EinsteinFlagshipPreview.viewer.getState();state.camera.azimuth=.88;state.camera.elevation=.31;state.entity="model-hotspot-origin:"+hotspotId;window.__EinsteinFlagshipPreview.viewer.setState(state);document.querySelector("[data-model-canvas]").focus();return{state:window.__EinsteinFlagshipPreview.viewer.getState(),scrollX,scrollY};
      }, hotspot.hotspotId);
      assert.equal(await page.evaluate((hotspotId) => window.__EinsteinFlagshipPreview.activateMappedHotspot(hotspotId), hotspot.hotspotId), true, `${viewport.name}/${hotspot.hotspotId}: model hotspot activation`);
      const mappedDialog = page.locator(`body > dialog.nlvt-dialog[data-nlvt-tool="${hotspot.openSurfaceToolId}"]`);
      await mappedDialog.waitFor({ state: "visible" });
      assert.equal(await mappedDialog.getAttribute("data-mapping-hotspot-id"), hotspot.hotspotId);
      assert.equal(await mappedDialog.locator('[data-nlvt-experience-visual="interior"]').getAttribute("data-nlvt-experience-scene"), hotspot.sceneIds[0], `${viewport.name}/${hotspot.hotspotId}: exact bound scene preselection`);
      await mappedDialog.locator('[data-nlvt-action="back"]').click();
      await mappedDialog.waitFor({ state: "detached" });
      const modelAfter=await page.evaluate(()=>({state:window.__EinsteinFlagshipPreview.viewer.getState(),scrollX,scrollY,focus:document.activeElement?.hasAttribute("data-model-canvas")}));
      assert.deepEqual(modelAfter.state, modelBefore.state, `${viewport.name}/${hotspot.hotspotId}: mapped Back exact model state`);
      assert.equal(modelAfter.scrollX,modelBefore.scrollX);assert.equal(modelAfter.scrollY,modelBefore.scrollY);assert.equal(modelAfter.focus,true,`${viewport.name}/${hotspot.hotspotId}: mapped Back focus canvas`);
    }

    const teaser = page.locator('.nlvt-teaser[data-nlvt-tool="view"]');
    if (viewport.touch) await teaser.dispatchEvent("pointerdown", { pointerType: "touch", pointerId: 2, clientX: 30, clientY: 30 });
    else await teaser.hover();
    assert.equal(await teaser.getAttribute("data-preview-active"), "true", `${viewport.name}: preview intent`);
    assert.equal(await page.locator("dialog.nlvt-dialog").count(), 0, `${viewport.name}: preview navigated/opened dialog`);

    for (const tool of ["view", "interior", "design", "comments"]) {
      if (viewport.width <= 700 || viewport.height <= 640) {
        while (!(await page.locator(`.nlvt-teaser[data-nlvt-tool="${tool}"]`).isVisible())) await page.locator('[data-nlvt-page="next"]').click();
      }
      const trigger = page.locator(`[data-nlvt-open="${tool}"]`);
      await trigger.focus();
      const snapshot = await page.evaluate(() => {
        const state = window.__EinsteinFlagshipPreview.viewer.getState();
        state.camera.azimuth = 1.2345; state.camera.elevation = .4567; state.camera.distance *= .91; state.entity = "einstein-tower-6885-32";
        window.__EinsteinFlagshipPreview.viewer.setState(state);
        return { model: window.__EinsteinFlagshipPreview.viewer.getState(), scrollX: scrollX, scrollY: scrollY, trigger: document.activeElement.getAttribute("data-nlvt-open"), mainInert: document.querySelector("main").inert, mainAria: document.querySelector("main").getAttribute("aria-hidden") };
      });
      const ioBefore = await page.evaluate(() => JSON.parse(JSON.stringify(window.__ioAudit)));
      await trigger.click();
      const dialog = page.locator(`body > dialog.nlvt-dialog[data-nlvt-tool="${tool}"]`);
      await dialog.waitFor({ state: "visible" });
      const modal = await page.evaluate((toolId) => {
        const dialog = document.querySelector(`body > dialog.nlvt-dialog[data-nlvt-tool="${toolId}"]`), rect = dialog.getBoundingClientRect(), main = document.querySelector("main");
        const scrollers = [...dialog.querySelectorAll("*")].filter((node) => { const style=getComputedStyle(node); return ((style.overflowY==="auto"||style.overflowY==="scroll")&&node.scrollHeight>node.clientHeight+1)||((style.overflowX==="auto"||style.overflowX==="scroll")&&node.scrollWidth>node.clientWidth+1); });
        const buttons=[...dialog.querySelectorAll("button")].filter((node)=>{const box=node.getBoundingClientRect();return getComputedStyle(node).display!=="none"&&box.width>0&&box.height>0;}).map((node)=>({w:node.getBoundingClientRect().width,h:node.getBoundingClientRect().height}));
        const smallText=[...dialog.querySelectorAll("*")].filter((node)=>{if(![...node.childNodes].some((child)=>child.nodeType===Node.TEXT_NODE&&child.textContent.trim()))return false;if(node.closest(".nlvt-visually-hidden,[hidden]"))return false;const style=getComputedStyle(node),box=node.getBoundingClientRect();return style.display!=="none"&&style.visibility!=="hidden"&&box.width>2&&box.height>2&&parseFloat(style.fontSize)<12;}).map((node)=>({text:node.textContent.trim().slice(0,50),size:getComputedStyle(node).fontSize}));
        const visibleDisclosures=[...document.querySelectorAll(".nlvt-disclosure")].filter((node)=>{const style=getComputedStyle(node),box=node.getBoundingClientRect();return style.display!=="none"&&style.visibility!=="hidden"&&box.width>2&&box.height>2;});
        const repeatedCaveats=[...document.querySelectorAll("body *")].filter((node)=>{if(node.closest(".nlvt-disclosure,.nlvt-visually-hidden,.nlef-visually-hidden,[hidden]"))return false;const own=[...node.childNodes].filter((child)=>child.nodeType===Node.TEXT_NODE).map((child)=>child.textContent).join(" ").trim();if(!/(?:להמחשה בלבד|המחשה בלבד|לא נמסרו רשימה|אינה מידע תכנוני|אינו פנים מאושר|אין בה מידות)/.test(own))return false;const style=getComputedStyle(node),box=node.getBoundingClientRect();return style.display!=="none"&&style.visibility!=="hidden"&&box.width>2&&box.height>2;}).map((node)=>node.textContent.trim());
        const clippedControls=[...dialog.querySelectorAll("button,.nlvt-disclosure,.nlvt-tool h2")].filter((node)=>{const style=getComputedStyle(node),box=node.getBoundingClientRect();return style.display!=="none"&&style.visibility!=="hidden"&&box.width>2&&box.height>2&&(box.left<-.5||box.top<-.5||box.right>innerWidth+.5||box.bottom>innerHeight+.5);}).map((node)=>({text:node.textContent.trim(),left:node.getBoundingClientRect().left,top:node.getBoundingClientRect().top,right:node.getBoundingClientRect().right,bottom:node.getBoundingClientRect().bottom}));
        return { parent:dialog.parentElement===document.body, width:rect.width, height:rect.height, x:rect.x, y:rect.y, grade:dialog.dataset.decisionGrade, owner:dialog.dataset.ownerDecisionId, experience:dialog.dataset.experienceDecisionId, mainInert:main.inert, mainAria:main.getAttribute("aria-hidden"), scrollers:scrollers.length, targets:buttons, smallText, disclosureCount:visibleDisclosures.length, disclosureInsideDialog:visibleDisclosures[0]?.closest("dialog")===dialog, repeatedCaveats, clippedControls };
      }, tool);
      assert.equal(modal.parent, true); assert.ok(Math.abs(modal.width - viewport.width) <= 1 && Math.abs(modal.height - viewport.height) <= 1 && Math.abs(modal.x) <= 1 && Math.abs(modal.y) <= 1, `${viewport.name}/${tool}: fullscreen geometry`);
      assert.equal(modal.grade, "false"); assert.equal(modal.owner, "OWNER-2026-08-13-VISUAL-PLAYGROUND");
      assert.equal(modal.experience, "OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO");
      assert.equal(modal.mainInert, true); assert.equal(modal.mainAria, "true"); assert.equal(modal.scrollers, 0);
      assert.equal(modal.disclosureCount, 1, `${viewport.name}/${tool}: exactly one visible showroom disclosure`);
      assert.equal(modal.disclosureInsideDialog, true, `${viewport.name}/${tool}: the one disclosure follows the active surface`);
      assert.deepEqual(modal.repeatedCaveats, [], `${viewport.name}/${tool}: repeated visible per-tool caveat`);
      assert.deepEqual(modal.clippedControls, [], `${viewport.name}/${tool}: clipped fullscreen control/title/disclosure`);
      assert.deepEqual(modal.smallText, [], `${viewport.name}/${tool}: fullscreen visible text below 12px`);
      assert.ok(modal.targets.every((target) => target.w >= 43.5 && target.h >= 43.5), `${viewport.name}/${tool}: fullscreen target`);
      await page.evaluate(() => { const state=window.__EinsteinFlagshipPreview.viewer.getState();state.camera.azimuth=-2.5;state.camera.distance*=1.3;state.entity="mutated-while-open";window.__EinsteinFlagshipPreview.viewer.setState(state); });
      if (tool === "design") {
        const sofa = dialog.locator("[data-nlvt-sofa]"); const box = await sofa.boundingBox();
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2); await page.mouse.down(); await page.mouse.move(box.x + box.width / 2 + 24, box.y + box.height / 2 - 12); await page.mouse.up();
        assert.ok(await sofa.getAttribute("data-x"), `${viewport.name}: sofa drag`);
      }
      if (tool === "interior") {
        const interior = dialog.locator("[data-nlvt-interior-state]");
        assert.deepEqual(await dialog.locator("button[data-nlvt-experience-scene]").evaluateAll((buttons) => buttons.map((button) => button.dataset.nlvtExperienceScene)), ["living", "bedroom", "arrival", "open-frame"], `${viewport.name}: exact four-scene Interior selector`);
        for (const scene of experienceEvidence) {
          await dialog.locator(`button[data-nlvt-experience-scene="${scene.id}"]`).click();
          assert.equal(await interior.getAttribute("data-nlvt-experience-scene"), scene.id);
          assert.equal(await interior.getAttribute("data-experience-asset-id"), scene.name.replace(/\.webp$/, ""));
          assert.equal(await interior.getAttribute("data-experience-asset-sha256"), scene.sha);
          assert.equal(await interior.getAttribute("data-mapping-state"), "owner_approved_illustrative_mapping");
          assert.match(await interior.evaluate((node) => getComputedStyle(node).getPropertyValue("--nlvt-experience-image")), new RegExp(scene.name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
          assert.equal(await dialog.getAttribute("data-nlvt-scene-kind"), scene.group === "interior" ? "representative_concept" : "selectable_concept_gallery");
          if (writeArtifacts && viewport.name === "390x844" && scene.id === "bedroom") await page.screenshot({ path: path.join(artifactDir, `einstein-flagship-${viewport.name}-interior.png`), fullPage: false });
          if (writeArtifacts && viewport.name === "390x844" && scene.id === "open-frame") await page.screenshot({ path: path.join(artifactDir, `einstein-flagship-${viewport.name}-facilities.png`), fullPage: false });
        }
        await dialog.locator('button[data-nlvt-experience-scene="living"]').click();
        await interior.focus(); await page.keyboard.press("ArrowUp"); await page.keyboard.press("ArrowRight"); await page.keyboard.press("Enter"); await page.keyboard.press("l");
        assert.equal(await interior.getAttribute("data-nlvt-interior-state"), "step-1");
        assert.equal(await interior.getAttribute("data-turn"), "1"); assert.equal(await interior.getAttribute("data-door-open"), "true"); assert.equal(await interior.getAttribute("data-light-on"), "true");
        assert.match(await dialog.locator("[data-nlvt-interior-status]").innerText(), /צעד 1.*דלת פתוחה.*אור דלוק/);
        await dialog.locator('[data-nlvt-action="step"]').click();
        assert.equal(await interior.getAttribute("data-nlvt-interior-state"), "step-2");
      }
      if (tool === "comments") {
        await dialog.locator('[data-nlvt-action="annotate"]').click();
        assert.equal(await dialog.locator("[data-nlvt-user-pin]").getAttribute("aria-hidden"), "false");
        await dialog.locator('[data-nlvt-action="prepare"]').click();
        assert.equal(await dialog.getAttribute("data-comment-state"), "prepared_no_write");
        assert.match(await dialog.locator("[data-nlvt-status]").innerText(), /השאלה הוכנה במכשיר זה בלבד.*לא נשמר.*לא נשלח/);
      }
      const postInteractionGeometry = await dialog.evaluate((node) => {
        const header=node.querySelector(".nlvt-tool > header"),back=node.querySelector('[data-nlvt-action="back"]'),title=node.querySelector("h2"),disclosure=node.querySelector(".nlvt-disclosure"),box=(item)=>{const rect=item.getBoundingClientRect();return{left:rect.left,top:rect.top,right:rect.right,bottom:rect.bottom,width:rect.width,height:rect.height};};
        const items=[back,title,disclosure].map(box), overlap=(a,b)=>a.left<b.right-.5&&a.right>b.left+.5&&a.top<b.bottom-.5&&a.bottom>b.top+.5;
        return{dialogScrollTop:node.scrollTop,toolScrollTop:node.querySelector(".nlvt-tool").scrollTop,header:box(header),items,overlaps:[[0,1],[0,2],[1,2]].filter(([a,b])=>overlap(items[a],items[b]))};
      });
      assert.equal(postInteractionGeometry.dialogScrollTop,0,`${viewport.name}/${tool}: dialog shifted after interaction`);
      assert.equal(postInteractionGeometry.toolScrollTop,0,`${viewport.name}/${tool}: tool shifted after interaction`);
      assert.ok(postInteractionGeometry.header.top>=-.5&&postInteractionGeometry.header.bottom<=viewport.height+.5,`${viewport.name}/${tool}: header outside viewport ${JSON.stringify(postInteractionGeometry)}`);
      assert.deepEqual(postInteractionGeometry.overlaps,[],`${viewport.name}/${tool}: Back/title/disclosure overlap ${JSON.stringify(postInteractionGeometry)}`);
      await dialog.locator('[data-nlvt-action="back"]').click();
      await dialog.waitFor({ state: "detached" });
      const restored = await page.evaluate(() => ({ model: window.__EinsteinFlagshipPreview.viewer.getState(), scrollX, scrollY, focus: document.activeElement?.getAttribute("data-nlvt-open"), mainInert: document.querySelector("main").inert, mainAria: document.querySelector("main").getAttribute("aria-hidden"), io: window.__ioAudit }));
      assert.deepEqual(restored.model, snapshot.model, `${viewport.name}/${tool}: exact model restore`);
      assert.equal(restored.scrollX, snapshot.scrollX); assert.equal(restored.scrollY, snapshot.scrollY);
      assert.equal(restored.focus, snapshot.trigger, `${viewport.name}/${tool}: exact focus restore`);
      assert.equal(restored.mainInert, snapshot.mainInert); assert.equal(restored.mainAria, snapshot.mainAria);
      assert.deepEqual(restored.io, ioBefore, `${viewport.name}/${tool}: tool caused I/O`);
    }

    const io = await page.evaluate(() => window.__ioAudit);
    assert.equal(io.fetch.length, 1, `${viewport.name}: only GLB fetch is allowed`);
    assert.match(io.fetch[0].url, /assets\/projects\/einstein-tower\/model-hd\.glb$/);
    assert.deepEqual(io.xhr, []); assert.deepEqual(io.beacon, []); assert.deepEqual(io.socket, []); assert.deepEqual(io.storage, []);
    assert.ok(browserRequests.every((url) => url.startsWith(origin + "/")), `${viewport.name}: external request ${JSON.stringify(browserRequests)}`);
    await page.waitForFunction((assetPaths) => assetPaths.every((assetPath) => performance.getEntriesByName(location.origin + assetPath).some((entry) => entry.responseEnd > 0)), experienceEvidence.map((asset) => `/assets/projects/einstein-tower/experience/${asset.name}`));
    const interceptedAssets = await Promise.all(experienceResponses);
    for (const asset of experienceEvidence) {
      const evidence = interceptedAssets.find((candidate) => candidate.name === asset.name);
      assert.deepEqual(evidence, { name: asset.name, status: 200, bytes: asset.size, sha: asset.sha }, `${viewport.name}/${asset.name}: browser response body evidence`);
    }
    if (viewport.width <= 700 || viewport.height <= 640) while (!(await page.locator('[data-nlvt-page="previous"]').isDisabled())) await page.locator('[data-nlvt-page="previous"]').click();
    if (writeArtifacts) await page.screenshot({ path: path.join(artifactDir, `einstein-flagship-${viewport.name}.png`), fullPage: false });
    await context.close();
  }

  const external = requests.filter((request) => !String(request.pathname).startsWith("/"));
  assert.deepEqual(external, []);
  assert.ok(requests.some((request) => request.pathname.endsWith("/assets/projects/einstein-tower/model-hd.glb") && request.status === 200 && request.bytes === modelStat.size), "Server did not deliver the complete real GLB.");
  for (const asset of experienceEvidence) assert.ok(requests.some((request) => request.pathname.endsWith(`/assets/projects/einstein-tower/experience/${asset.name}`) && request.status === 200 && request.bytes === asset.size), `Server did not deliver ${asset.name}.`);
  assert.equal(requests.some((request) => request.status === 404), false, `Static asset 404: ${JSON.stringify(requests.filter((request) => request.status === 404))}`);
  console.log(`PASS Einstein flagship offline: canonical zero-inventory HE surface, real local GLB, protected model, exactly four permanent teasers, four selectable Interior scenes, three mapped model anchors, exact Back state, no tool I/O, 44px/12px/no-inner-scroll at ${viewports.map((viewport) => viewport.name).join(", ")}.`);
} finally {
  if (browser) await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
