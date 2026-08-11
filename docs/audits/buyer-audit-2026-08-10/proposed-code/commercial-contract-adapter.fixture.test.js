/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Executable PHP-normalized snake_case -> JS view-model seam fixture.
 * Run: node commercial-contract-adapter.fixture.test.js
 */
"use strict";

var assert = require("assert");
var fs = require("fs");
var path = require("path");
var vm = require("vm");

function FakeNode(tagName) {
  this.tagName = String(tagName || "").toUpperCase();
  this.children = [];
  this.parentNode = null;
  this.ownerDocument = null;
  this.attributes = Object.create(null);
  this.listeners = Object.create(null);
  this.dataset = {};
  this.className = "";
  this.textContent = "";
  this.value = "";
  this.disabled = false;
}
FakeNode.prototype.appendChild = function appendChild(child) {
  if (!(child instanceof FakeNode)) throw new TypeError("FakeNode child required.");
  if (child.tagName === "#FRAGMENT") {
    while (child.children.length) this.appendChild(child.children[0]);
    return child;
  }
  if (child.parentNode) child.parentNode.removeChild(child);
  this.children.push(child);
  child.parentNode = this;
  return child;
};
FakeNode.prototype.insertBefore = function insertBefore(child, reference) {
  if (child.parentNode) child.parentNode.removeChild(child);
  var index = reference == null ? -1 : this.children.indexOf(reference);
  if (index < 0) this.children.push(child);
  else this.children.splice(index, 0, child);
  child.parentNode = this;
  return child;
};
FakeNode.prototype.removeChild = function removeChild(child) {
  var index = this.children.indexOf(child);
  if (index < 0) throw new Error("Child not found.");
  this.children.splice(index, 1);
  child.parentNode = null;
  return child;
};
FakeNode.prototype.remove = function remove() {
  if (this.parentNode) this.parentNode.removeChild(this);
};
FakeNode.prototype.replaceChildren = function replaceChildren() {
  while (this.children.length) this.removeChild(this.children[0]);
  for (var i = 0; i < arguments.length; i += 1) this.appendChild(arguments[i]);
};
FakeNode.prototype.setAttribute = function setAttribute(name, value) {
  this.attributes[name] = String(value);
};
FakeNode.prototype.getAttribute = function getAttribute(name) {
  return Object.prototype.hasOwnProperty.call(this.attributes, name) ? this.attributes[name] : null;
};
FakeNode.prototype.hasAttribute = function hasAttribute(name) {
  return Object.prototype.hasOwnProperty.call(this.attributes, name);
};
FakeNode.prototype.removeAttribute = function removeAttribute(name) {
  delete this.attributes[name];
};
FakeNode.prototype.addEventListener = function addEventListener(type, callback) {
  if (!this.listeners[type]) this.listeners[type] = [];
  this.listeners[type].push(callback);
};
FakeNode.prototype.removeEventListener = function removeEventListener(type, callback) {
  this.listeners[type] = (this.listeners[type] || []).filter(function (item) { return item !== callback; });
};
FakeNode.prototype.dispatchEvent = function dispatchEvent(event) {
  event.target = this;
  (this.listeners[event.type] || []).slice().forEach(function (callback) { callback(event); });
  if (event.bubbles && this.parentNode) this.parentNode.dispatchEvent(event);
  return true;
};
FakeNode.prototype.focus = function focus() {
  if (this.ownerDocument) this.ownerDocument.activeElement = this;
};
Object.defineProperty(FakeNode.prototype, "nextSibling", {
  get: function getNextSibling() {
    if (!this.parentNode) return null;
    var index = this.parentNode.children.indexOf(this);
    return index >= 0 ? this.parentNode.children[index + 1] || null : null;
  }
});

function countNodes(root, predicate) {
  return (predicate(root) ? 1 : 0) + root.children.reduce(function (sum, child) {
    return sum + countNodes(child, predicate);
  }, 0);
}

function contextFixture() {
  var document = {
    activeElement: null,
    createElement: function (tag) {
      var node = new FakeNode(tag);
      node.ownerDocument = document;
      return node;
    },
    createComment: function (value) {
      var node = new FakeNode("#comment");
      node.textContent = value;
      node.ownerDocument = document;
      return node;
    },
    createDocumentFragment: function () {
      var node = new FakeNode("#fragment");
      node.ownerDocument = document;
      return node;
    }
  };
  document.body = document.createElement("body");
  var window = {
    Node: FakeNode,
    document: document,
    Intl: Intl,
    location: {
      href: "https://example.invalid/projects/fixture-commercial-project/",
      origin: "https://example.invalid"
    },
    requestAnimationFrame: function (callback) { callback(); }
  };
  window.window = window;
  function CustomEvent(type, options) {
    this.type = type;
    this.detail = options && options.detail;
    this.bubbles = Boolean(options && options.bubbles);
  }
  return vm.createContext({
    window: window,
    document: document,
    console: console,
    Date: Date,
    Number: Number,
    String: String,
    Boolean: Boolean,
    Array: Array,
    Object: Object,
    JSON: JSON,
    Math: Math,
    Error: Error,
    TypeError: TypeError,
    Promise: Promise,
    URL: URL,
    Intl: Intl,
    AbortController: AbortController,
    CustomEvent: CustomEvent
  });
}

function load(context, filename) {
  vm.runInContext(fs.readFileSync(path.join(__dirname, filename), "utf8"), context, { filename: filename });
}

var now = Date.now();
var effectiveAt = new Date(now - 2 * 60 * 60 * 1000).toISOString();
var retrievedAt = new Date(now - 90 * 60 * 1000).toISOString();
var verifiedAt = new Date(now - 60 * 60 * 1000).toISOString();
var expiresAt = new Date(now + 6 * 60 * 60 * 1000).toISOString();

function source(id) {
  return {
    type: "owner_crm",
    label: "Fixture source " + id,
    uri: "https://example.invalid/evidence/" + id,
    document_id: id,
    revision: "fixture-v1",
    published_at: effectiveAt,
    retrieved_at: retrievedAt
  };
}
function owner() {
  return { team: "Fixture data", accountable_role: "Fixture steward", contact_ref: "fixture-steward" };
}
function positive(state, value, unit, id) {
  return {
    state: state,
    value: value,
    unit: unit || null,
    scope: "fixture scope " + id,
    effective_at: effectiveAt,
    sources: [source(id)],
    observations: [],
    verified_at: state === "verified" ? verifiedAt : null,
    expires_at: expiresAt,
    owner: owner(),
    confidence: state === "verified" ? "high" : "medium",
    reason: "",
    applicability: ["commercial", id],
    conflict_ids: [],
    note: "Fixture note " + id,
    caveat: state === "source_estimate" ? "Fixture estimate caveat." : "",
    required_document_ids: [],
    decision_grade: state === "verified"
  };
}
function verified(value, unit, id) { return positive("verified", value, unit, id); }
function estimate(value, unit, id) { return positive("source_estimate", value, unit, id); }
function unknown(reason, documents, id) {
  return {
    state: "unknown",
    value: null,
    unit: null,
    scope: null,
    effective_at: null,
    sources: [],
    observations: [],
    verified_at: null,
    expires_at: null,
    owner: null,
    confidence: "unknown",
    reason: reason,
    applicability: [id || "commercial"],
    conflict_ids: [],
    note: "Unknown note remains separate.",
    caveat: "Unknown caveat remains separate.",
    required_document_ids: documents || [],
    decision_grade: false
  };
}
function contradictory(first, second, unit, id) {
  var ids = [id + "-a", id + "-b"];
  return {
    state: "contradictory",
    value: null,
    unit: unit || null,
    scope: "fixture contradiction scope " + id,
    effective_at: effectiveAt,
    sources: [],
    observations: [
      { observation_id: ids[0], value: first, scope: "A", source: source(ids[0]) },
      { observation_id: ids[1], value: second, scope: "B", source: source(ids[1]) }
    ],
    verified_at: null,
    expires_at: null,
    owner: owner(),
    confidence: "medium",
    reason: "",
    applicability: ["commercial", id],
    conflict_ids: ids,
    note: "Contradiction note.",
    caveat: "Do not choose either observation.",
    required_document_ids: ["measurement_report"],
    decision_grade: false
  };
}

function metrics(anchor, coordinate) {
  var radius = 6371008.8;
  var lat1 = anchor.lat * Math.PI / 180;
  var lat2 = coordinate.lat * Math.PI / 180;
  var dlat = lat2 - lat1;
  var dlng = (coordinate.lng - anchor.lng) * Math.PI / 180;
  var a = Math.sin(dlat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlng / 2) ** 2;
  var distance = radius * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var y = Math.sin(dlng) * Math.cos(lat2);
  var x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dlng);
  return { distance: distance, bearing: (Math.atan2(y, x) * 180 / Math.PI + 360) % 360 };
}

var anchor = { lat: 32.1, lng: 34.8 };
var exposureSpecs = [
  { id: "north", direction: "N", start: 315, end: 45, coordinate: { lat: 32.104, lng: 34.8 } },
  { id: "east", direction: "E", start: 45, end: 135, coordinate: { lat: 32.1, lng: 34.805 } },
  { id: "south", direction: "S", start: 135, end: 225, coordinate: { lat: 32.096, lng: 34.8 } },
  { id: "west", direction: "W", start: 225, end: 315, coordinate: { lat: 32.1, lng: 34.795 } }
];
function facade(spec) {
  return {
    exposure_id: spec.id,
    direction: verified(spec.direction, null, spec.id + "-direction"),
    azimuth_start_deg: verified(spec.start, "degrees_true_north", spec.id + "-start"),
    azimuth_end_deg: verified(spec.end, "degrees_true_north", spec.id + "-end"),
    facade_share_pct: estimate(25, "percent", spec.id + "-share"),
    view_context: unknown("No view study.", ["view_study"], spec.id + "-view"),
    obstructions: unknown("No obstruction study.", ["view_study"], spec.id + "-obstruction")
  };
}
function beamAssociation(spec) {
  var measured = metrics(anchor, spec.coordinate);
  var landmarkId = spec.id + "-landmark";
  return {
    exposure_id: spec.id,
    landmarks: [{
      landmark_id: landmarkId,
      exposure_id: spec.id,
      label: verified(spec.direction + " landmark with complete sourced name", null, landmarkId + "-label"),
      compact_label: verified(spec.direction + " mark", null, landmarkId + "-compact-label"),
      coordinates: verified(spec.coordinate, null, landmarkId + "-coordinate"),
      distance_m: verified(Math.round(measured.distance), "metres_ground", landmarkId + "-distance"),
      distance_method: verified("straight_line_geodesic", null, landmarkId + "-method"),
      bearing_deg: verified(measured.bearing, "degrees_true_north", landmarkId + "-bearing"),
      caveat: "North-up schematic; not a surveyed sightline."
    }]
  };
}
function readyBeam() {
  return {
    scene_state: "ready",
    projection: "north_up_local_equirectangular_v1",
    project_anchor: verified(anchor, null, "project-anchor"),
    exposures: exposureSpecs.map(beamAssociation),
    illustrative_caveat: "Evidenced coordinates; illustrative north-up schematic.",
    issues: []
  };
}

var statuses = [
  "unknown", "verified_available", "soft_hold", "under_offer", "under_loi",
  "leased", "delivered", "unavailable", "not_marketed"
];
function floor(status, index, towerId, floorId) {
  var prefix = towerId + "-" + floorId;
  var towerLabel = towerId === "tower-a" ? "Tower A" : "Tower B";
  return {
    building_id: "building-main",
    tower_id: towerId,
    tower_display_label: verified(towerLabel, null, prefix + "-tower-label"),
    floor_id: floorId,
    legal_floor_label: verified("Legal " + floorId, null, prefix + "-legal"),
    elevator_label: verified(floorId === "level-10" ? "10" : String(index + 10), null, prefix + "-elevator"),
    marketing_label: verified("Office " + floorId, null, prefix + "-marketing"),
    zone: verified("Core", null, prefix + "-zone"),
    selectable: true,
    availability: status === "unknown"
      ? unknown("No current availability.", ["availability_schedule"], prefix + "-availability")
      : verified(status, null, prefix + "-availability"),
    gross_rentable_sqm: verified(1000 + index, "sqm_rentable_gross", prefix + "-gross"),
    usable_sqm: estimate(800 + index, "sqm_usable", prefix + "-usable"),
    clear_height_m: unknown("Not supplied.", ["tenant_technical_manual"], prefix + "-height"),
    floor_load_kg_m2: unknown("Not supplied.", ["structural_load_schedule"], prefix + "-load"),
    tenant_power_va_m2: unknown("Not supplied.", ["power_single_line"], prefix + "-power"),
    exposures: towerId === "tower-a" && index === 0 ? exposureSpecs.map(facade) : [],
    beam_scene: towerId === "tower-a" && index === 0 ? readyBeam() : null,
    suites: [{
      building_id: "building-main",
      tower_id: towerId,
      floor_id: floorId,
      suite_id: "suite-1",
      label: verified("Suite 1", null, prefix + "-suite-label"),
      selectable: true,
      availability: verified("verified_available", null, prefix + "-suite-availability"),
      gross_rentable_sqm: verified(500, "sqm_rentable_gross", prefix + "-suite-gross"),
      usable_sqm: estimate(400, "sqm_usable", prefix + "-suite-usable"),
      exposures: []
    }]
  };
}

var vocabularies = {
  asset_types: ["residential", "commercial_office", "retail", "mixed_use", "hospitality", "guide_only"],
  implemented_asset_types: ["commercial_office"],
  product_families: ["living", "premium", "commercial", "guide"],
  applicability_tags: ["three_d_showroom", "floor_selector", "suite_selector", "commercial_rfp", "context_map", "decision_surface"],
  evidence_states: ["unknown", "source_estimate", "verified", "contradictory"],
  confidence_levels: ["unknown", "low", "medium", "high"],
  beam_distance_methods: ["straight_line_geodesic", "routed_walking", "routed_cycling", "routed_driving", "routed_transit"],
  availability_statuses: statuses.slice(),
  compass_sectors: ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
};
var floors = statuses.map(function (status, index) {
  return floor(status, index, "tower-a", index === 0 ? "level-10" : "level-" + (10 + index));
});
floors.push(floor("verified_available", 0, "tower-b", "level-10"));
var rawProject = {
  schema_version: "1.0.0",
  vocabularies: vocabularies,
  project_id: "fixture-commercial-project",
  wp_post_id: 999999,
  project_url: "https://example.invalid/projects/fixture-commercial-project/",
  asset_type: "commercial_office",
  product_family: "commercial",
  applicability_tags: vocabularies.applicability_tags.slice(),
  ui_adapter_supported: true,
  title: "Fixture commercial project",
  generated_at: new Date(now).toISOString(),
  towers: [
    { building_id: "building-main", tower_id: "tower-a", display_label: verified("Tower A", null, "tower-a-label") },
    { building_id: "building-main", tower_id: "tower-b", display_label: verified("Tower B", null, "tower-b-label") }
  ],
  project_facts: {
    office_floor_count: verified(10, "floors", "office-floor-count"),
    marketable_area_sqm: estimate(10000, "sqm", "marketable-area"),
    floor_count_total: contradictory(10, 11, "levels", "floor-count"),
    parking_stall_count: unknown("Not supplied.", ["parking_schedule"], "parking")
  },
  floor_inventory: verified("fixture-revision", null, "floor-inventory"),
  floors: floors,
  publication_blockers: [],
  publication_allowed: true,
  selectable_floor_count: floors.length
};

var context = contextFixture();
load(context, "commercial-decision-surface.js");
load(context, "commercial-floor-selection.js");
var adapter = context.window.NadlanCommercialContractAdapter;
var decision = context.window.NadlanCommercialDecisionSurface;
var selectorApi = context.window.NadlanCommercialFloorSelector;

assert.deepStrictEqual(Array.from(adapter.confidenceLevels), ["unknown", "low", "medium", "high"]);
assert.deepStrictEqual(Array.from(adapter.beamDistanceMethods), vocabularies.beam_distance_methods);
assert.deepStrictEqual(Array.from(adapter.availabilityStatuses), statuses);

// Exact evidence-envelope seam: state, scope, effective date, confidence,
// reason/applicability/conflicts and caveat survive without inference.
var verifiedRoundtrip = adapter.normalizeEvidenceEnvelope(verified(42, "sqm", "roundtrip-verified"), { now: now });
assert.strictEqual(verifiedRoundtrip.state, "verified");
assert.strictEqual(verifiedRoundtrip.scope, "fixture scope roundtrip-verified");
assert.strictEqual(verifiedRoundtrip.effectiveAt, effectiveAt);
assert.strictEqual(verifiedRoundtrip.confidence, "high");
assert.strictEqual(verifiedRoundtrip.reason, "");
assert.deepStrictEqual(Array.from(verifiedRoundtrip.applicability), ["commercial", "roundtrip-verified"]);
var estimateRoundtrip = adapter.normalizeEvidenceEnvelope(estimate(42, "sqm", "roundtrip-estimate"), { now: now });
assert.strictEqual(estimateRoundtrip.state, "source_estimate");
assert.strictEqual(estimateRoundtrip.confidence, "medium");
assert.strictEqual(estimateRoundtrip.caveat, "Fixture estimate caveat.");
var contradictionRoundtrip = adapter.normalizeEvidenceEnvelope(contradictory(10, 11, "levels", "roundtrip-conflict"), { now: now });
assert.strictEqual(contradictionRoundtrip.state, "contradictory");
assert.deepStrictEqual(Array.from(contradictionRoundtrip.conflictIds), ["roundtrip-conflict-a", "roundtrip-conflict-b"]);
assert.strictEqual(contradictionRoundtrip.effectiveAt, effectiveAt);
var unknownRoundtrip = adapter.normalizeEvidenceEnvelope(unknown("Explicit missing reason.", ["orientation_plan"], "roundtrip-unknown"), { now: now });
assert.strictEqual(unknownRoundtrip.state, "unknown");
assert.strictEqual(unknownRoundtrip.reason, "Explicit missing reason.");
assert.strictEqual(unknownRoundtrip.caveat, "Unknown caveat remains separate.");
assert.strictEqual(unknownRoundtrip.effectiveAt, "");
var expired = estimate(9, null, "expired");
expired.expires_at = new Date(now - 1000).toISOString();
var expiredRoundtrip = adapter.normalizeEvidenceEnvelope(expired, { now: now });
assert.strictEqual(expiredRoundtrip.state, "unknown");
assert.strictEqual(expiredRoundtrip.originalState, "source_estimate");
assert(expiredRoundtrip.issues.indexOf("missing_or_expired_expiry") >= 0);
var legacyScope = estimate(8, null, "legacy-scope");
delete legacyScope.scope;
legacyScope.evidence_scope = "must not be promoted";
assert.strictEqual(adapter.normalizeEvidenceEnvelope(legacyScope, { now: now }).state, "unknown");

var project = adapter.adaptProjectContract(rawProject, { now: now });
assert.deepStrictEqual(Array.from(project.contractIssues), []);
assert.strictEqual(project.publicationAllowed, true);
assert.strictEqual(project.towers.length, 2);
assert.strictEqual(project.floors.length, 10);
statuses.forEach(function (status, index) {
  assert.strictEqual(project.floors[index].status, status);
  assert.strictEqual(project.floors[index].selectable, true);
});

// Two towers may share a visible floor label and machine floor ID, but never
// the composite identity, URL, selection value or lead tuple.
var towerAFloor = project.floorByKey["building-main|tower-a|level-10|"];
var towerBFloor = project.floorByKey["building-main|tower-b|level-10|"];
assert(towerAFloor && towerBFloor);
assert.strictEqual(project.floorById["level-10"], null);
assert.strictEqual(towerAFloor.floorLabel, "10");
assert.strictEqual(towerBFloor.floorLabel, "10");
assert.notStrictEqual(towerAFloor.identityKey, towerBFloor.identityKey);
assert.notStrictEqual(towerAFloor.url, towerBFloor.url);
assert(towerAFloor.url.indexOf("tower_id=tower-a") >= 0);
assert(towerBFloor.url.indexOf("tower_id=tower-b") >= 0);
assert(towerAFloor.url.indexOf("project_contract_id=fixture-commercial-project") >= 0);
assert.strictEqual(new URL(towerAFloor.url).searchParams.has("wp_post_id"), false);
assert.strictEqual(towerAFloor.suites[0].towerId, "tower-a");
assert.strictEqual(towerBFloor.suites[0].towerId, "tower-b");
assert.strictEqual(towerAFloor.suiteId, null);
assert.strictEqual(towerAFloor.suites[0].suiteId, "suite-1");
assert.notStrictEqual(towerAFloor.suites[0].identityKey, towerBFloor.suites[0].identityKey);
assert.strictEqual(project.assetByKey[towerAFloor.identityKey], towerAFloor);
assert.strictEqual(project.assetByKey[towerBFloor.suites[0].identityKey], towerBFloor.suites[0]);

// Four facade exposures remain four independent, labelled cones. No .find()
// first-exposure collapse is allowed.
assert.strictEqual(towerAFloor.beamScene.state, "ready");
assert.strictEqual(towerAFloor.beamScene.exposures.length, 4);
assert.strictEqual(adapter.beamCompactLabelMaxCodePoints, 12);
assert.strictEqual(towerAFloor.beamScene.exposures[0].landmarks[0].compactLabel.value, "N mark");
assert.deepStrictEqual(
  Array.from(towerAFloor.beamScene.exposures.map(function (item) { return item.exposureId; })),
  ["north", "east", "south", "west"]
);
var labels = {
  exposureCone: "Facade sector",
  northUpSchematic: "North-up schematic using evidenced coordinates",
  distanceMethods: { straight_line_geodesic: "Straight-line geodesic" },
  distanceMethodsShort: { straight_line_geodesic: "Geodesic" },
  methodsCount: "{count} methods",
  illustrativeBadge: "Illustrative",
  openSource: "Open source",
  floorPack: "Open the complete floor pack",
  floorPackShort: "Floor pack",
  fitOut: "Explore fit-out and infrastructure",
  fitOutShort: "Fit-out",
  context: "See the commute and area",
  contextShort: "Area",
  cost: "Understand the full occupancy cost",
  costShort: "Full cost"
};
var rendered = decision.renderDecisionSurface(towerAFloor, labels, { locale: "en-US" });
assert.strictEqual((rendered.match(/class="nl-beam-scene__cone"/g) || []).length, 4);
assert(rendered.indexOf('class="nl-beam-scene__legend-name">N mark</bdi>') >= 0, "compact label must be the visible legend copy");
assert(rendered.indexOf('aria-label="N landmark with complete sourced name.') >= 0, "full sourced label must remain in accessible output");
exposureSpecs.forEach(function (spec) {
  assert(rendered.indexOf('data-exposure-id="' + spec.id + '"') >= 0);
});
assert(rendered.indexOf('data-projection="north_up_local_equirectangular_v1"') >= 0);
assert(rendered.indexOf("Straight-line geodesic") >= 0);
assert(rendered.indexOf('class="nl-beam-scene__method"') >= 0 && rendered.indexOf(">Geodesic · Illustrative</span>") >= 0);
assert.strictEqual(rendered.indexOf("nl-beam-scene__road"), -1);
var beamSources = decision.collectBeamEvidenceSources(
  towerAFloor.beamScene,
  labels,
  new Intl.NumberFormat("en-US")
);
assert(beamSources.length >= 5, "fixture must exercise bounded disclosure for five or more sources");
assert(beamSources.some(function (entry) {
  return entry.source.label === "Fixture source north-landmark-distance" && entry.effectiveAt === effectiveAt;
}), "the full source collection must retain landmark source identity and freshness");
assert.strictEqual((rendered.match(/<a class="nl-beam-scene__source"/g) || []).length, 3);
assert.strictEqual((rendered.match(/nl-beam-scene__source--all/g) || []).length, 1);
assert(rendered.indexOf('data-source-count="' + beamSources.length + '"') >= 0);
assert.strictEqual((rendered.match(/nl-cds-door__title--long/g) || []).length, 4);
assert.strictEqual((rendered.match(/nl-cds-door__title--short/g) || []).length, 4);
assert.strictEqual((rendered.match(/nl-cds-door__state--long/g) || []).length, 4);
assert.strictEqual((rendered.match(/nl-cds-door__state--short/g) || []).length, 4);
assert(rendered.indexOf('aria-label="Open the complete floor pack.') >= 0, "full long door copy must remain the accessible button name");
assert(rendered.indexOf('nl-cds-door__title--short" aria-hidden="true">Floor pack</span>') >= 0, "localized compact door copy must be a distinct visible-mode span");
assert(rendered.indexOf('nl-cds-door__state--short" aria-hidden="true"></span>') >= 0, "short-landscape state icon must not hide a localized text node at zero pixels");

// The fourth fixed-scene control opens a paginated, no-truncation tool. The
// exact pagination function used by that tool makes every source index
// reachable while keeping at most four records in one fullscreen view.
var reachedSourceIndexes = [];
for (var sourcePage = 0; sourcePage < Math.ceil(beamSources.length / 4); sourcePage += 1) {
  var sourceBounds = decision.beamEvidencePage(beamSources.length, sourcePage, 4);
  assert(sourceBounds.end - sourceBounds.start <= 4);
  for (var sourceIndex = sourceBounds.start; sourceIndex < sourceBounds.end; sourceIndex += 1) {
    reachedSourceIndexes.push(sourceIndex);
  }
}
assert.deepStrictEqual(reachedSourceIndexes, Array.from(beamSources, function (_, index) { return index; }));
var sourceTool = decision.defaultToolNode("beam-evidence", towerAFloor, Object.assign({ locale: "en" }, labels));
assert.strictEqual(Number(sourceTool.dataset.sourceCount), beamSources.length);
assert.strictEqual(countNodes(sourceTool, function (node) { return node.tagName === "ARTICLE"; }), 4);

var compactBoundaryBeam = readyBeam();
compactBoundaryBeam.exposures[0].landmarks[0].compact_label = estimate("אבגדהוזחטיכל", null, "compact-boundary-12");
var compactBoundaryScene = adapter.adaptBeamScene(compactBoundaryBeam, towerAFloor.exposures, { now: now });
assert.strictEqual(compactBoundaryScene.state, "ready", "12 Unicode code points from a current source estimate must be allowed");
assert.strictEqual(compactBoundaryScene.exposures[0].landmarks[0].compactLabel.value, "אבגדהוזחטיכל", "compact label is never rewritten or truncated");

// A stable document ID without a public URI remains a visible record/request
// in the evidence tool; it is never rendered as a fake source link.
var noUrlBeam = JSON.parse(JSON.stringify(readyBeam()));
noUrlBeam.project_anchor.sources[0].uri = "";
var noUrlScene = adapter.adaptBeamScene(noUrlBeam, towerAFloor.exposures, { now: now });
assert.strictEqual(noUrlScene.state, "ready");
var noUrlAsset = Object.assign({}, towerAFloor, { beamScene: noUrlScene });
var noUrlTool = decision.defaultToolNode("beam-evidence", noUrlAsset, Object.assign({ locale: "en" }, labels));
assert(countNodes(noUrlTool, function (node) {
  return node.tagName === "BUTTON" && String(node.dataset.fieldId || "").indexOf("orientation.source.") === 0;
}) >= 1, "unlinked source must expose an honest request action, not a fake link");

// The local projection uses actual evidenced coordinates: change a valid
// landmark coordinate and its matching geodesic values, and geometry changes.
var movedBeam = JSON.parse(JSON.stringify(readyBeam()));
var moved = { lat: 32.107, lng: 34.8 };
var movedMetrics = metrics(anchor, moved);
movedBeam.exposures[0].landmarks[0].coordinates.value = moved;
movedBeam.exposures[0].landmarks[0].distance_m.value = Math.round(movedMetrics.distance);
movedBeam.exposures[0].landmarks[0].bearing_deg.value = movedMetrics.bearing;
var movedScene = adapter.adaptBeamScene(movedBeam, towerAFloor.exposures, { now: now });
assert.strictEqual(movedScene.state, "ready");
var movedAsset = Object.assign({}, towerAFloor, { beamScene: movedScene });
var movedRendered = decision.renderDecisionSurface(movedAsset, labels, { locale: "en-US" });
function renderedLandmarkPoint(markup, landmarkId) {
  var pattern = new RegExp(
    'data-landmark-id="' + landmarkId + '"[^>]*>[\\s\\S]*?' +
    '<circle class="nl-beam-scene__landmark-point" cx="([^"]+)" cy="([^"]+)"'
  );
  var match = markup.match(pattern);
  assert(match, "rendered landmark point is missing for " + landmarkId);
  return match[1] + "," + match[2];
}
var originalPoint = renderedLandmarkPoint(rendered, "east-landmark");
var movedPoint = renderedLandmarkPoint(movedRendered, "east-landmark");
assert.notStrictEqual(originalPoint, movedPoint);

function neutralCase(mutator, name) {
  var raw = JSON.parse(JSON.stringify(readyBeam()));
  mutator(raw);
  var scene = adapter.adaptBeamScene(raw, towerAFloor.exposures, { now: now });
  assert.strictEqual(scene.state, "unknown", name);
  assert.strictEqual(scene.exposures.length, 0, name + " leaked partial exposure data");
  var html = decision.renderDecisionSurface(Object.assign({}, towerAFloor, { beamScene: scene }), labels, { locale: "en" });
  assert.strictEqual((html.match(/class="nl-beam-scene__cone"/g) || []).length, 0, name);
  assert.strictEqual((html.match(/class="nl-beam-scene__landmark"/g) || []).length, 0, name);
  assert(html.indexOf('data-act="request-field"') >= 0, name + " must expose the neutral request action");
}
neutralCase(function (raw) { raw.exposures.push(JSON.parse(JSON.stringify(raw.exposures[0]))); }, "duplicate association");
neutralCase(function (raw) { raw.exposures[0].exposure_id = "unknown-exposure"; }, "unknown association");
neutralCase(function (raw) { raw.exposures.pop(); }, "missing association");
neutralCase(function (raw) { delete raw.exposures[0].landmarks[0].exposure_id; }, "missing landmark association");
neutralCase(function (raw) { raw.exposures[0].landmarks[0].distance_method = unknown("Missing method.", [], "missing-method"); }, "missing distance method");
neutralCase(function (raw) { raw.exposures[0].landmarks[0].coordinates.sources = []; }, "missing coordinate source");
neutralCase(function (raw) { raw.exposures[0].landmarks[0].distance_m.effective_at = null; }, "missing effective date");
neutralCase(function (raw) { raw.exposures[0].landmarks[0].bearing_deg.value = 180; }, "out-of-sector landmark");
neutralCase(function (raw) { raw.project_anchor = contradictory(anchor, { lat: 32.11, lng: 34.81 }, null, "anchor-conflict"); }, "contradictory anchor");
neutralCase(function (raw) {
  raw.exposures[0].landmarks[0].label.value = "L".repeat(1000);
  raw.exposures[0].landmarks[0].compact_label.value = "C".repeat(13);
}, "1000-code-point full label with overlong compact label");
neutralCase(function (raw) { delete raw.exposures[0].landmarks[0].compact_label; }, "missing compact label");
neutralCase(function (raw) { raw.exposures[0].landmarks[0].compact_label = "bare compact label"; }, "malformed compact label evidence");
neutralCase(function (raw) {
  raw.exposures[0].landmarks[0].compact_label = unknown("Compact label not confirmed.", ["orientation_plan"], "compact-unknown");
}, "unknown compact label");
neutralCase(function (raw) {
  raw.exposures[0].landmarks[0].compact_label.expires_at = new Date(now - 1000).toISOString();
}, "expired compact label");
neutralCase(function (raw) {
  raw.exposures[0].landmarks[0].compact_label = contradictory("North mark", "North hub", null, "compact-conflict");
}, "contradictory compact label");
neutralCase(function (raw) {
  raw.exposures[0].landmarks[0].compact_label.value = "bad\uD800";
}, "malformed Unicode compact label");

// Composite calibration and picker: two towers can occupy the same model Y,
// so an unscoped hit is ambiguous and a tower-scoped hit is exact.
var calibration = project.floors.map(function (item, index) {
  var towerIndex = item.towerId === "tower-a" ? project.floors.filter(function (f) { return f.towerId === "tower-a"; }).indexOf(item) : 0;
  return {
    building_id: item.buildingId,
    tower_id: item.towerId,
    floor_id: item.id,
    min_y: towerIndex * 4,
    max_y: towerIndex * 4 + 3.5,
    display_order: index,
    evidence: verified("calibration", null, item.towerId + "-" + item.id + "-calibration")
  };
});
var ranges = adapter.buildFloorRanges(project, calibration, { now: now, locale: "fr-FR" });
var validatedRanges = selectorApi.validateRanges(ranges);
assert.strictEqual(selectorApi.resolveFloorAtY(validatedRanges, 1), null);
assert.strictEqual(
  selectorApi.resolveFloorAtY(validatedRanges, 1, { buildingId: "building-main", towerId: "tower-a" }).identityKey,
  towerAFloor.identityKey
);

var model = context.document.createElement("model-viewer");
model.positionAndNormalFromPoint = function () { return Promise.resolve({ position: { y: 1 } }); };
var select = context.document.createElement("select");
var selectedPayload = null;
var cleared = 0;
var floorSelector = new selectorApi.CommercialFloorSelector({
  modelViewer: model,
  floorRanges: ranges,
  selectElement: select,
  projectId: project.projectId,
  clearHighlight: function () { cleared += 1; },
  onSelect: function (payload) { selectedPayload = payload; }
}).attach();
assert.strictEqual(countNodes(select, function (node) { return node.tagName === "OPTGROUP"; }), 2);
assert.strictEqual(floorSelector.selectFloor(towerAFloor.identityKey, "fixture"), true);
assert.strictEqual(model.getAttribute("data-selected-floor"), towerAFloor.identityKey);
assert.strictEqual(selectedPayload.buildingId, "building-main");
assert.strictEqual(selectedPayload.towerId, "tower-a");
assert.strictEqual(selectedPayload.floorId, "level-10");
floorSelector.destroy();
assert.strictEqual(model.hasAttribute("data-selected-floor"), false);
assert.strictEqual(select.value, "");
assert.strictEqual(cleared, 1);

var preexistingModel = context.document.createElement("model-viewer");
preexistingModel.setAttribute("data-selected-floor", "legacy-value");
var preexistingSelector = new selectorApi.CommercialFloorSelector({
  modelViewer: preexistingModel,
  floorRanges: ranges,
  projectId: project.projectId
}).attach();
preexistingSelector.selectFloor(towerBFloor.identityKey, "fixture");
preexistingSelector.destroy();
assert.strictEqual(preexistingModel.getAttribute("data-selected-floor"), "legacy-value");

// Omitted/null/string/false selectability remains fail-closed; only literal
// true plus verified calibration survives.
[undefined, null, "true", false, true].forEach(function (selectable, index) {
  var raw = Object.assign({}, ranges[0], {
    building_id: "building-main",
    tower_id: "tower-a",
    tower_label: "Tower A",
    floor_id: "selectability-" + index,
    identity_key: "building-main|tower-a|selectability-" + index,
    min_y: 100 + index * 5,
    max_y: 104 + index * 5,
    calibration_evidence: verified("calibration", null, "selectability-calibration-" + index)
  });
  delete raw.selectable;
  if (selectable !== undefined) raw.selectable = selectable;
  assert.strictEqual(selectorApi.normalizeRange(raw, index).selectable, selectable === true);
});

// One live model node and its selected-floor attribute are restored exactly.
var parent = context.document.createElement("div");
var before = context.document.createElement("button");
var liveModel = context.document.createElement("model-viewer");
var after = context.document.createElement("div");
liveModel.setAttribute("style", "background: fixture");
liveModel.setAttribute("data-selected-floor", "pre-scene-value");
parent.appendChild(before);
parent.appendChild(liveModel);
parent.appendChild(after);
context.document.body.appendChild(parent);
before.focus();
var controller;
var host = new decision.CommercialSceneHost({
  modelNode: liveModel,
  locale: "he-IL",
  projectContractId: towerAFloor.projectId,
  routeHistory: false,
  resolveAsset: function (key) { return project.floorByKey[key] || null; },
  controllerFactory: function (options) {
    controller = { root: options.root, rendered: null, render: function (asset) { this.rendered = asset; }, destroy: function () {} };
    return controller;
  }
});
host.mount(towerAFloor.identityKey);
assert.strictEqual(countNodes(parent, function (node) { return node === liveModel; }), 1);
assert.strictEqual(controller.rendered.identityKey, towerAFloor.identityKey);
liveModel.setAttribute("data-selected-floor", towerBFloor.identityKey);
host.destroy();
assert.deepStrictEqual(parent.children, [before, liveModel, after]);
assert.strictEqual(liveModel.getAttribute("data-selected-floor"), "pre-scene-value");
assert.strictEqual(context.document.activeElement, before);

[
  { width: 320, height: 568, mode: "mobile_stack", modelWidth: 320, modelHeight: 159, surfaceWidth: 320, surfaceHeight: 409 },
  { width: 375, height: 812, mode: "mobile_stack", modelWidth: 375, modelHeight: 210, surfaceWidth: 375, surfaceHeight: 602 },
  { width: 568, height: 320, mode: "compact_landscape", modelWidth: 239, modelHeight: 320, surfaceWidth: 329, surfaceHeight: 320 },
  { width: 1280, height: 800, mode: "desktop", modelWidth: 850, modelHeight: 800, surfaceWidth: 430, surfaceHeight: 800 }
].forEach(function (fixture) {
  var geometry = decision.sceneGeometry(fixture.width, fixture.height);
  Object.keys(fixture).forEach(function (key) {
    if (key !== "width" && key !== "height") assert.strictEqual(geometry[key], fixture[key]);
  });
  assert(geometry.modelWidth > 0 && geometry.surfaceWidth > 0);
});

var rtl = decision.renderDecisionSurface(towerAFloor, labels, { locale: "he-IL" });
var ltr = decision.renderDecisionSurface(towerAFloor, labels, { locale: "fr-FR" });
assert(rtl.indexOf('lang="he-IL" dir="rtl"') >= 0);
assert(rtl.indexOf('aria-hidden="true">→</span>') >= 0);
assert(ltr.indexOf('lang="fr-FR" dir="ltr"') >= 0);
assert(ltr.indexOf('aria-hidden="true">←</span>') >= 0);

var capturedRfpOptions = null;
var capturedRfpAssets = [];
context.window.NadlanCommercialRfpConfig = {
  endpoint: "https://example.invalid/wp-json/nadlan/v2/commercial-rfp-sandbox",
  environment: "test",
  sandboxPostId: 55,
  sandboxNonce: "signed-fixture-nonce",
  consentVersion: "fixture-consent-v1"
};
context.window.NadlanCommercialRfpComposer = {
  createNode: function (options) {
    capturedRfpOptions = options;
    capturedRfpAssets.push(options.asset);
    return context.document.createElement("section");
  }
};
decision.defaultToolNode("inquiry", towerAFloor, { locale: "en" });
assert.strictEqual(capturedRfpOptions.environment, "test");
assert.strictEqual(capturedRfpOptions.sandboxPostId, 55);
assert.strictEqual(capturedRfpOptions.sandboxNonce, "signed-fixture-nonce");
assert.strictEqual(capturedRfpOptions.endpoint, context.window.NadlanCommercialRfpConfig.endpoint);
assert.strictEqual(capturedRfpOptions.consentVersion, "fixture-consent-v1");
decision.defaultToolNode("inquiry", towerBFloor, { locale: "en" });
assert.strictEqual(capturedRfpAssets[0].floorLabel, capturedRfpAssets[1].floorLabel);
assert.notStrictEqual(capturedRfpAssets[0].identityKey, capturedRfpAssets[1].identityKey);
assert.strictEqual(capturedRfpAssets[0].towerId, "tower-a");
assert.strictEqual(capturedRfpAssets[1].towerId, "tower-b");
assert.notStrictEqual(capturedRfpAssets[0].url, capturedRfpAssets[1].url);

console.log("PASS commercial contract adapter: exact envelope, 2 towers, 4 beams, selector lifecycle, locale and scene host.");
