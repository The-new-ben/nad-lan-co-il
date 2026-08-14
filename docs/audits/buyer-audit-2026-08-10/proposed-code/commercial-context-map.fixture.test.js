/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Dependency-free context-map truth and failure fixture; it performs no network
 * requests and never touches WordPress or the live site.
 *
 * Run:
 *   node commercial-context-map.fixture.test.js
 */
"use strict";

var assert = require("assert");
var fs = require("fs");
var path = require("path");
var vm = require("vm");

function evidence(value, note) {
  return {
    state: "verified",
    value: value,
    sources: [
      {
        label: "Official fixture source",
        uri: "https://example.invalid/context-source",
        documentId: "fixture-context-source"
      }
    ],
    observations: [],
    sourceLabel: "Official fixture source",
    sourceUrl: "https://example.invalid/context-source",
    verifiedAt: "2026-08-10T08:00:00Z",
    effectiveAt: "2026-08-10T07:55:00Z",
    expiresAt: "2026-09-10T08:00:00Z",
    confidence: "high",
    applicability: ["all"],
    conflictIds: [],
    scope: "Fixture identity, geometry, status and dated travel claim.",
    caveat: note === undefined ? "Dated fixture evidence; verify live conditions." : note
  };
}

function FakeElement() {
  this.dataset = {};
  this.attributes = {};
  this.hidden = false;
  this.disabled = false;
  this.textContent = "";
  this.childrenReplaced = 0;
  this.dispatchedEvents = [];
}

FakeElement.prototype.setAttribute = function setAttribute(name, value) {
  this.attributes[name] = String(value);
};
FakeElement.prototype.removeAttribute = function removeAttribute(name) {
  delete this.attributes[name];
};
FakeElement.prototype.remove = function remove() {};
FakeElement.prototype.replaceChildren = function replaceChildren() {
  this.childrenReplaced += 1;
};
FakeElement.prototype.querySelectorAll = function querySelectorAll() {
  return [];
};
FakeElement.prototype.dispatchEvent = function dispatchEvent(event) {
  this.dispatchedEvents.push(event);
  return !event.defaultPrevented;
};

function FakeCustomEvent(type, options) {
  options = options || {};
  this.type = type;
  this.bubbles = Boolean(options.bubbles);
  this.cancelable = Boolean(options.cancelable);
  this.detail = options.detail;
  this.defaultPrevented = false;
}
FakeCustomEvent.prototype.preventDefault = function preventDefault() {
  if (this.cancelable) this.defaultPrevented = true;
};

function createRoot() {
  var section = new FakeElement();
  var map = new FakeElement();
  var status = new FakeElement();
  status.hidden = true;
  var results = new FakeElement();
  results.innerHTML = "READABLE PAGED CARDS";
  var focusControl = new FakeElement();
  var root = new FakeElement();
  root.cleared = false;
  root.querySelector = function querySelector(selector) {
    if (selector === ".nl-ccm") return section;
    if (selector === '[data-role="map"]') return map;
    if (selector === '[data-role="map-status"]') return status;
    if (selector === '[data-role="results"]') return results;
    return null;
  };
  root.querySelectorAll = function querySelectorAll(selector) {
    return selector === "[data-context-id]" ? [focusControl] : [];
  };
  root.replaceChildren = function replaceChildren() {
    root.cleared = true;
  };
  return {
    root: root,
    section: section,
    map: map,
    status: status,
    results: results,
    focusControl: focusControl
  };
}

function TimerHarness() {
  this.nextId = 1;
  this.entries = new Map();
  this.cleared = [];
}
TimerHarness.prototype.setTimeout = function setTimeoutHarness(callback, delay) {
  var id = this.nextId++;
  this.entries.set(id, { callback: callback, delay: delay });
  return id;
};
TimerHarness.prototype.clearTimeout = function clearTimeoutHarness(id) {
  if (this.entries.delete(id)) this.cleared.push(id);
};
TimerHarness.prototype.fireOnly = function fireOnly() {
  assert.strictEqual(this.entries.size, 1, "Expected one bounded first-load timer.");
  var pair = Array.from(this.entries.entries())[0];
  this.entries.delete(pair[0]);
  pair[1].callback();
  return pair[1].delay;
};

function FakeMap() {
  this.listeners = Object.create(null);
  this.offCalls = [];
  this.removeCalls = 0;
  this.isLoaded = false;
  this.layers = Object.create(null);
  this.sources = Object.create(null);
  FakeMap.instances.push(this);
}
FakeMap.instances = [];
FakeMap.prototype.on = function on(type, callback) {
  this.listeners[type] = callback;
};
FakeMap.prototype.off = function off(type, callback) {
  this.offCalls.push(type);
  if (this.listeners[type] === callback) delete this.listeners[type];
};
FakeMap.prototype.emit = function emit(type) {
  if (type === "load") this.isLoaded = true;
  var callback = this.listeners[type];
  if (callback) callback({ type: type });
};
FakeMap.prototype.remove = function remove() {
  this.removeCalls += 1;
};
FakeMap.prototype.loaded = function loaded() { return this.isLoaded; };
FakeMap.prototype.addControl = function addControl() {};
FakeMap.prototype.getLayer = function getLayer(id) { return this.layers[id] || null; };
FakeMap.prototype.removeLayer = function removeLayer(id) { delete this.layers[id]; };
FakeMap.prototype.getSource = function getSource(id) { return this.sources[id] || null; };
FakeMap.prototype.removeSource = function removeSource(id) { delete this.sources[id]; };
FakeMap.prototype.addSource = function addSource(id, source) { this.sources[id] = source; };
FakeMap.prototype.addLayer = function addLayer(layer) { this.layers[layer.id] = layer; };
FakeMap.prototype.fitBounds = function fitBounds(bounds, options) {
  this.lastBounds = bounds;
  this.lastFitOptions = options;
};

function FakeMarker(options) {
  this.element = options.element;
  this.removed = false;
  FakeMarker.instances.push(this);
}
FakeMarker.instances = [];
FakeMarker.prototype.setLngLat = function setLngLat(coordinates) {
  this.coordinates = coordinates;
  return this;
};
FakeMarker.prototype.addTo = function addTo(map) {
  this.map = map;
  return this;
};
FakeMarker.prototype.remove = function remove() { this.removed = true; };

function FakeBounds(first) { this.coordinates = [first]; }
FakeBounds.prototype.extend = function extend(coordinate) {
  this.coordinates.push(coordinate);
  return this;
};

function makeContext(timer, width, height) {
  var document = {
    createElement: function createElement() { return new FakeElement(); }
  };
  var window = {
    document: document,
    innerWidth: width || 375,
    innerHeight: height || 812,
    CustomEvent: FakeCustomEvent,
    mapboxgl: { Map: FakeMap, Marker: FakeMarker, LngLatBounds: FakeBounds },
    setTimeout: timer.setTimeout.bind(timer),
    clearTimeout: timer.clearTimeout.bind(timer),
    NadlanCommercialContractAdapter: {
      normalizeEvidenceEnvelope: function normalizeEvidenceEnvelope(raw) {
        raw = raw && typeof raw === "object" ? raw : {};
        return {
          state: raw.state || "unknown",
          value: Object.prototype.hasOwnProperty.call(raw, "value") ? raw.value : null,
          sources: raw.sources || [],
          observations: raw.observations || [],
          sourceLabel: raw.sourceLabel || "",
          sourceUrl: raw.sourceUrl || "",
          verifiedAt: raw.verifiedAt || "",
          effectiveAt: raw.effectiveAt || "",
          expiresAt: raw.expiresAt || "",
          ownerLabel: raw.ownerLabel || "",
          requiredDocumentIds: raw.requiredDocumentIds || [],
          confidence: raw.confidence || null,
          scope: raw.scope || "",
          applicability: raw.applicability || [],
          conflictIds: raw.conflictIds || [],
          caveat: raw.caveat || "",
          reason: raw.reason || "",
          note: raw.note || "",
          issues: raw.issues || []
        };
      }
    }
  };
  window.window = window;
  var context = vm.createContext({
    window: window,
    document: document,
    console: console,
    Number: Number,
    String: String,
    Boolean: Boolean,
    Array: Array,
    Object: Object,
    JSON: JSON,
    Math: Math,
    Error: Error,
    TypeError: TypeError,
    Map: Map,
    Set: Set
  });
  var i18nSource = fs.readFileSync(path.join(__dirname, "commercial-i18n-additions.js"), "utf8");
  vm.runInContext(i18nSource, context, { filename: "commercial-i18n-additions.js" });
  var source = fs.readFileSync(path.join(__dirname, "commercial-context-map.js"), "utf8");
  vm.runInContext(source, context, { filename: "commercial-context-map.js" });
  return context;
}

function rawPoint(state) {
  return {
    id: "place-" + (state || "missing"),
    mode: "commute",
    category: "rail",
    name: "Fixture place",
    coordinates: [34.8, 32.1],
    operating_state: state,
    network_distance_m: 420,
    minutes_min: 5,
    minutes_max: 8,
    evidence_scope: "Identity, coordinate, operating state and dated route.",
    caveat: "Point caveat: verify the named entrance and operating status.",
    evidence: evidence(true)
  };
}

function rawRoute(state) {
  return {
    id: "route-" + (state || "missing"),
    mode: "commute",
    label: "Fixture route",
    travel_mode: "walk",
    operating_state: state,
    geometry: [[34.8, 32.1], [34.81, 32.11]],
    minutes_min: 5,
    minutes_max: 8,
    evidence_scope: "Geometry, state and dated travel-time range.",
    caveat: "Route caveat: travel time is a dated range, not a guarantee.",
    evidence: evidence(true)
  };
}

var timer = new TimerHarness();
var context = makeContext(timer);
var api = context.window.NadlanCommercialContextMap;
var states = [
  "operating",
  "under_construction",
  "planned",
  "temporarily_closed",
  "closed",
  "unknown"
];
var i18n = context.window.NadlanCommercialI18n;
assert(i18n, "The complete commercial dictionary was not loaded.");
assert.deepStrictEqual(Array.from(i18n.supported), ["he", "en", "fr", "ru", "ar"]);
var localizedCoreKeys = [
  "operatingState", "stage", "expected", "expectedUnknown", "projectedTravel",
  "closedServiceTravel", "historicalTravel", "unknownStateTravel",
  "mapFocusUnavailable", "openSourceRecord", "sourceNotLinked",
  "estimateCaveat", "evidenceCaveat", "transfers"
];
var englishLabels = i18n.get("en");
i18n.supported.forEach(function (locale) {
  var labels = i18n.get(locale);
  localizedCoreKeys.forEach(function (key) {
    assert.strictEqual(typeof labels[key], "string", "Missing context label: " + locale + "." + key);
    assert(labels[key].trim(), "Empty context label: " + locale + "." + key);
    if (locale !== "en") {
      assert.notStrictEqual(labels[key], englishLabels[key], "English leaked into " + locale + "." + key);
    }
  });
  assert.deepStrictEqual(Object.keys(labels.operatingStates).sort(), states.slice().sort());
  ["walk", "transit", "bike", "drive"].forEach(function (mode) {
    assert(labels.travelModes[mode], "Missing travel mode: " + locale + "." + mode);
  });
  ["rail", "bus", "metro", "light_rail", "food", "pharmacy", "medical", "gym", "parking", "hotel", "airport", "office", "market", "risk"].forEach(function (category) {
    assert(labels.categories[category], "Missing category: " + locale + "." + category);
  });
});

assert.deepStrictEqual(Array.from(api.operatingStates), states);
assert.deepStrictEqual(Array.from(api.storedOperatingStates), states.slice(0, 5));
var preservedEvidence = api.normalizeEvidence(evidence(true));
assert.strictEqual(preservedEvidence.effectiveAt, "2026-08-10T07:55:00Z");
assert.strictEqual(preservedEvidence.expiresAt, "2026-09-10T08:00:00Z");
assert.strictEqual(preservedEvidence.confidence, "high");
assert.deepStrictEqual(Array.from(preservedEvidence.applicability), ["all"]);
assert.deepStrictEqual(Array.from(preservedEvidence.conflictIds), []);
states.forEach(function (state, index) {
  var point = api.normalizePoint(rawPoint(state), index);
  var route = api.normalizeRoute(rawRoute(state), index);
  assert(point && route, "State fixture was rejected: " + state);
  assert.strictEqual(point.operatingState, state);
  assert.strictEqual(route.operatingState, state);
  var pointHtml = api.pointCard(point, {});
  var routeHtml = api.routeCard(route, {});
  [pointHtml, routeHtml].forEach(function (html) {
    assert(html.indexOf('data-operating-state="' + state + '"') >= 0);
    assert(html.indexOf("nl-ccm-state-badge__visual") >= 0, "Visible badge missing.");
    assert(html.indexOf("nl-ccm-sr-only") >= 0, "Screen-reader state missing.");
    assert(html.indexOf("Operating state:") >= 0, "Screen-reader prefix missing.");
    assert(html.indexOf("nl-ccm-evidence-caveat") >= 0, "Evidence caveat missing.");
    assert(html.indexOf("https://example.invalid/context-source") >= 0, "One-click source missing.");
  });
  var qualifier = {
    operating: "",
    under_construction: "Projected travel:",
    planned: "Projected travel:",
    temporarily_closed: "Reference travel while service is closed:",
    closed: "Historical/reference travel:",
    unknown: "Travel applicability not verified:"
  }[state];
  if (qualifier) {
    assert(pointHtml.indexOf(qualifier) >= 0, "Point travel qualifier missing: " + state);
    assert(routeHtml.indexOf(qualifier) >= 0, "Route travel qualifier missing: " + state);
  }
});

assert.strictEqual(api.normalizeOperatingState("open"), "operating");
[undefined, null, "", "active", "proposal", "concept", "approved", "temporarily-closed"].forEach(
  function (invalid) {
    assert.strictEqual(api.normalizeOperatingState(invalid), "unknown", "Invalid state leaked: " + invalid);
  }
);
var missingState = api.normalizePoint(rawPoint(undefined), 0);
assert.strictEqual(missingState.operatingState, "unknown");
var evidenceWrappedUnknown = rawPoint("operating");
evidenceWrappedUnknown.operating_state = { state: "unknown", value: null };
assert.strictEqual(api.normalizePoint(evidenceWrappedUnknown, 0).operatingState, "unknown");

var planned = rawPoint("planned");
planned.stage = "approved planning stage";
planned.expected_range = { from: "2030-01", to: "2031-06" };
var plannedRecord = api.normalizePoint(planned, 0);
var plannedHtml = api.pointCard(plannedRecord, {});
assert.strictEqual(plannedRecord.expectedRange, "2030-01 – 2031-06");
assert(plannedHtml.indexOf("Stage: approved planning stage") >= 0);
assert(plannedHtml.indexOf("Expected: 2030-01 – 2031-06") >= 0);
assert(plannedHtml.indexOf("Projected travel:") >= 0, "Planned travel looked current.");
var construction = rawRoute("under_construction");
construction.stage = "systems installation";
construction.expected_date = "2028-12-31";
var constructionHtml = api.routeCard(api.normalizeRoute(construction, 0), {});
assert(constructionHtml.indexOf("Expected: 2028-12-31") >= 0);
assert(constructionHtml.indexOf("Projected travel:") >= 0, "Construction travel looked current.");
assert(constructionHtml.indexOf("Route caveat: travel time is a dated range") >= 0);
assert(constructionHtml.indexOf('class="nl-ccm-source"') >= 0);

var noCaveatRaw = rawPoint("operating");
delete noCaveatRaw.caveat;
noCaveatRaw.evidence.caveat = "";
noCaveatRaw.evidence.note = "";
noCaveatRaw.evidence.reason = "";
var noCaveatRecord = api.normalizePoint(noCaveatRaw, 0);
assert.strictEqual(noCaveatRecord.caveat, "", "Normalization froze a fallback language.");
assert(
  api.pointCard(noCaveatRecord, i18n.get("he")).indexOf(i18n.get("he").evidenceCaveat) >= 0,
  "The current Hebrew labels did not resolve the caveat at render time."
);

i18n.supported.forEach(function (locale) {
  var labels = i18n.get(locale);
  var localizedPointRaw = rawPoint("planned");
  localizedPointRaw.stage = locale === "en" ? "approved" : "•";
  localizedPointRaw.expected_date = "2030-01";
  var localizedPoint = api.normalizePoint(localizedPointRaw, 0);
  localizedPoint.caveat = "";
  localizedPoint.evidence.caveat = "";
  localizedPoint.evidence.note = "";
  localizedPoint.evidence.reason = "";
  localizedPoint.evidence.sourceLabel = "";
  localizedPoint.evidence.observedAt = "";
  localizedPoint.evidenceScope = "";
  var localizedRouteRaw = rawRoute("planned");
  localizedRouteRaw.transfers = 2;
  var localizedRoute = api.normalizeRoute(localizedRouteRaw, 0);
  localizedRoute.caveat = "";
  localizedRoute.evidence.caveat = "";
  localizedRoute.evidence.note = "";
  localizedRoute.evidence.reason = "";
  localizedRoute.evidence.sourceLabel = "";
  localizedRoute.evidence.observedAt = "";
  localizedRoute.evidenceScope = "";
  var localizedHtml = api.pointCard(localizedPoint, labels) + api.routeCard(localizedRoute, labels);
  assert(localizedHtml.indexOf(labels.operatingStates.planned) >= 0);
  assert(localizedHtml.indexOf(labels.projectedTravel) >= 0);
  assert(localizedHtml.indexOf(labels.evidenceCaveat) >= 0, "Render-time caveat missing: " + locale);
  assert(localizedHtml.indexOf(labels.categories.rail) >= 0);
  assert(localizedHtml.indexOf(labels.travelModes.walk) >= 0);
  assert(localizedHtml.indexOf("2 " + labels.transfers) >= 0);
  if (locale !== "en") {
    ["Operating state:", "Projected travel:", "Evidence applies to the stated scope", "Stage:", "Expected:", ">Open source<", " transfers<"].forEach(function (english) {
      assert.strictEqual(localizedHtml.indexOf(english), -1, "Mixed English render in " + locale + ": " + english);
    });
  }
});

assert.strictEqual(api.boundedMapLoadTimeout(undefined), 8000);
assert.strictEqual(api.boundedMapLoadTimeout(20), 1000);
assert.strictEqual(api.boundedMapLoadTimeout(999999), 15000);
assert.strictEqual(api.recordsPerPageForViewport(375, 812), 2);
assert.strictEqual(api.recordsPerPageForViewport(1280, 800), 4);
assert.strictEqual(api.recordsPerPageForViewport(568, 320), 1);
assert.strictEqual(api.recordsPerPageForViewport(640, 400), 1);

var callbackActivations = [];
var callbackMap = new api.CommercialContextMap({
  root: new FakeElement(),
  onOpenSourceDocument: function onOpenSourceDocument(payload, originalEvent) {
    callbackActivations.push({ payload: payload, originalEvent: originalEvent });
  }
});
var sourceControl = new FakeElement();
var originalClick = { type: "click" };
assert.strictEqual(
  callbackMap.activateContextAction(
    sourceControl,
    "openSourceDocument",
    { documentId: "source-document-1", recordId: "place-operating" },
    originalClick
  ),
  true
);
assert.strictEqual(callbackActivations.length, 1, "Source callback was not activated exactly once.");
assert.strictEqual(callbackActivations[0].payload.documentId, "source-document-1");
assert.strictEqual(callbackActivations[0].originalEvent, originalClick);
assert.strictEqual(sourceControl.dispatchedEvents.length, 0, "Callback path also emitted a duplicate event.");

var requestControl = new FakeElement();
var eventMap = new api.CommercialContextMap({ root: new FakeElement() });
assert.strictEqual(
  eventMap.activateContextAction(
    requestControl,
    "requestField",
    { fieldId: "context.commute", mode: "commute" },
    originalClick
  ),
  true
);
assert.strictEqual(requestControl.dispatchedEvents.length, 1, "Request event was not activated exactly once.");
assert.strictEqual(requestControl.dispatchedEvents[0].type, api.actionEvents.requestField);
assert.strictEqual(requestControl.dispatchedEvents[0].bubbles, true);
assert.strictEqual(requestControl.dispatchedEvents[0].cancelable, true);
assert.strictEqual(requestControl.dispatchedEvents[0].detail.fieldId, "context.commute");

function makeMapFixture(mapTimer, records) {
  FakeMap.instances.length = 0;
  FakeMarker.instances.length = 0;
  var fixtureContext = makeContext(mapTimer);
  var fixtureApi = fixtureContext.window.NadlanCommercialContextMap;
  var dom = createRoot();
  var instance = new fixtureApi.CommercialContextMap({
    root: dom.root,
    center: [34.8, 32.1],
    center_evidence: evidence("Project entrance"),
    points: records && records.points,
    routes: records && records.routes,
    mapLoadTimeoutMs: 1000
  });
  instance.mapContainer = dom.map;
  instance.mapStatus = dom.status;
  instance.initializeMap();
  return { api: fixtureApi, dom: dom, instance: instance, map: FakeMap.instances[0] };
}

var errorTimer = new TimerHarness();
var errorFixture = makeMapFixture(errorTimer);
assert.strictEqual(errorFixture.instance.mapState, "loading");
assert(errorFixture.map.listeners.load && errorFixture.map.listeners.error);
errorFixture.map.emit("error");
assert.strictEqual(errorFixture.instance.mapState, "unavailable");
assert.strictEqual(errorFixture.instance.map, null);
assert.strictEqual(errorFixture.map.removeCalls, 1, "Failed map was not removed.");
assert.strictEqual(errorFixture.dom.map.hidden, true, "Failed map was not hidden.");
assert.strictEqual(errorFixture.dom.map.childrenReplaced, 1, "Failed map DOM was not cleared.");
assert.strictEqual(errorFixture.dom.status.hidden, false, "Readable fallback status was not exposed.");
assert.strictEqual(errorFixture.dom.section.dataset.mapState, "unavailable");
assert.strictEqual(errorFixture.dom.results.innerHTML, "READABLE PAGED CARDS", "Fallback erased readable cards.");
assert.strictEqual(errorFixture.dom.focusControl.disabled, true);
assert.deepStrictEqual(errorFixture.map.offCalls.sort(), ["error", "load"]);
assert.strictEqual(errorTimer.entries.size, 0, "Async-error fallback leaked its timeout.");

var timeoutTimer = new TimerHarness();
var timeoutFixture = makeMapFixture(timeoutTimer);
var timeoutDelay = timeoutTimer.fireOnly();
assert.strictEqual(timeoutDelay, 1000);
assert.strictEqual(timeoutFixture.instance.mapState, "unavailable");
assert.strictEqual(timeoutFixture.map.removeCalls, 1);
assert.strictEqual(timeoutFixture.dom.results.innerHTML, "READABLE PAGED CARDS");
assert.deepStrictEqual(timeoutFixture.map.offCalls.sort(), ["error", "load"]);

var successTimer = new TimerHarness();
var successFixture = makeMapFixture(successTimer);
successFixture.map.emit("load");
assert.strictEqual(successFixture.instance.mapState, "ready");
assert.strictEqual(successFixture.instance.mapReady, true);
assert.strictEqual(successTimer.entries.size, 0, "Successful load leaked its timeout.");
assert.deepStrictEqual(successFixture.map.offCalls.sort(), ["error", "load"]);
successFixture.instance.destroy();
assert.strictEqual(successFixture.map.removeCalls, 1);
assert.strictEqual(successFixture.instance.mapState, "destroyed");
assert.strictEqual(successFixture.dom.root.cleared, true);

var styledTimer = new TimerHarness();
var styledFixture = makeMapFixture(styledTimer, {
  points: states.map(rawPoint),
  routes: states.map(rawRoute)
});
styledFixture.map.emit("load");
assert.strictEqual(styledFixture.instance.mapState, "ready");
assert.strictEqual(styledFixture.instance.markers.length, states.length);
states.forEach(function (state) {
  var layer = styledFixture.map.layers["nl-commercial-routes-" + state];
  assert(layer, "Rendered route layer missing: " + state);
  assert.strictEqual(
    JSON.stringify(layer.filter),
    JSON.stringify(["==", ["get", "operating_state"], state])
  );
  assert(
    styledFixture.instance.markers.some(function (marker) {
      return marker.element.dataset.operatingState === state &&
        marker.element.attributes["aria-label"].indexOf("Operating state:") >= 0;
    }),
    "Visible/SR marker state missing: " + state
  );
});
assert.strictEqual(
  styledFixture.map.sources["nl-commercial-routes"].data.features.length,
  states.length
);
styledFixture.instance.destroy();
assert(
  FakeMarker.instances.every(function (marker) { return marker.removed; }),
  "Destroy did not remove all state-styled markers."
);

var destroyTimer = new TimerHarness();
var destroyFixture = makeMapFixture(destroyTimer);
destroyFixture.instance.destroy();
assert.strictEqual(destroyTimer.entries.size, 0, "Destroy leaked its first-load timer.");
assert.deepStrictEqual(destroyFixture.map.offCalls.sort(), ["error", "load"]);
assert.strictEqual(destroyFixture.map.removeCalls, 1);

// Third-party teardown hooks are not trusted. One throwing marker, listener,
// map, abort hook, or root must not prevent the remaining cleanup or retain a
// live-looking controller. A second destroy remains a harmless no-op.
var atomicDestroyTimer = new TimerHarness();
var atomicDestroyFixture = makeMapFixture(atomicDestroyTimer);
var teardownCalls = [];
atomicDestroyFixture.instance.markers = [
  {
    remove: function removeThrowingMarker() {
      teardownCalls.push("marker-throw");
      throw new Error("fixture marker remove failure");
    }
  },
  {
    remove: function removeLaterMarker() {
      teardownCalls.push("marker-later");
    }
  }
];
atomicDestroyFixture.instance.abortController = {
  abort: function abortThrowingController() {
    teardownCalls.push("abort");
    throw new Error("fixture abort failure");
  }
};
atomicDestroyFixture.map.off = function offThrowingListener(type) {
  this.offCalls.push(type);
  teardownCalls.push("off-" + type);
  if (type === "load") throw new Error("fixture listener removal failure");
};
atomicDestroyFixture.map.remove = function removeThrowingMap() {
  this.removeCalls += 1;
  teardownCalls.push("map");
  throw new Error("fixture map remove failure");
};
atomicDestroyFixture.dom.root.replaceChildren = function replaceThrowingRoot() {
  atomicDestroyFixture.dom.root.cleared = true;
  teardownCalls.push("root");
  throw new Error("fixture root cleanup failure");
};
assert.doesNotThrow(function destroyWithHostileHooks() {
  atomicDestroyFixture.instance.destroy();
});
assert.deepStrictEqual(
  teardownCalls,
  ["off-load", "off-error", "abort", "marker-throw", "marker-later", "map", "root"],
  "A throwing teardown hook skipped a later cleanup stage."
);
assert.strictEqual(atomicDestroyTimer.entries.size, 0, "Atomic destroy retained its timer.");
assert.strictEqual(atomicDestroyFixture.instance.abortController, null);
assert.strictEqual(atomicDestroyFixture.instance.markers.length, 0);
assert.strictEqual(atomicDestroyFixture.instance.map, null);
assert.strictEqual(atomicDestroyFixture.instance.mapReady, false);
assert.strictEqual(atomicDestroyFixture.instance.mapState, "destroyed");
assert.strictEqual(atomicDestroyFixture.instance.mapContainer, null);
assert.strictEqual(atomicDestroyFixture.instance.mapStatus, null);
assert.strictEqual(atomicDestroyFixture.instance.mapLoadHandler, null);
assert.strictEqual(atomicDestroyFixture.instance.mapErrorHandler, null);
assert.strictEqual(atomicDestroyFixture.instance.root, null);
assert.strictEqual(atomicDestroyFixture.map.removeCalls, 1);
assert.strictEqual(atomicDestroyFixture.dom.root.cleared, true);
assert.doesNotThrow(function repeatedDestroyIsIdempotent() {
  atomicDestroyFixture.instance.destroy();
});
assert.strictEqual(atomicDestroyFixture.map.removeCalls, 1, "Repeated destroy removed the old map twice.");

var css = fs.readFileSync(path.join(__dirname, "commercial-decision-surface.css"), "utf8");
var js = fs.readFileSync(path.join(__dirname, "commercial-context-map.js"), "utf8");
states.forEach(function (state) {
  assert(css.indexOf('.nl-ccm-marker[data-operating-state="' + state + '"]') >= 0,
    "Marker style missing for " + state);
  assert(css.indexOf('.nl-ccm-card[data-operating-state="' + state + '"]') >= 0,
    "Card style missing for " + state);
  assert(js.indexOf('"nl-commercial-routes-" + state') >= 0,
    "State-specific route layer construction missing.");
});
assert(/\.nl-ccm-marker\s*\{[^}]*min-height:\s*44px/s.test(css), "Marker target is below 44px.");
assert(/\.nl-ccm \.nl-ccm-source\s*\{[^}]*min-height:\s*44px/s.test(css), "Source target is below 44px.");
assert.strictEqual(/overflow\s*:\s*(?:auto|scroll)\s*;/i.test(css), false, "Nested scrolling was introduced.");
assert(js.indexOf('this.map.on("error"') >= 0, "First-load async error listener missing.");
assert(js.indexOf("mapLoadTimeoutMs") >= 0, "Bounded first-load timeout missing.");

console.log(
  "PASS context-map fixture: five-locale parity and render-time fallbacks, six truth states, one-record short-landscape paging, exact-once source/request seams, future timing, visible/SR marker/route styles, async fallback cleanup, and hostile-hook atomic destroy with no network."
);
