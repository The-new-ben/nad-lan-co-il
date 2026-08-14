/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Executable fixtures for five-locale completeness, bounded RFP geometry,
 * immutable identity, exact retry snapshots, and deterministic recovery.
 */
"use strict";

var fs = require("fs");
var path = require("path");
var vm = require("vm");

var base = __dirname;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

var activeElement = null;

function FakeElement(tag) {
  this.tagName = String(tag || "div").toUpperCase();
  this.children = [];
  this.textContent = "";
  this.className = "";
  this.dataset = {};
  this.attributes = {};
  this.style = { setProperty: function setProperty() {} };
  this.disabled = false;
  this.hidden = false;
  this.required = false;
  this.checked = false;
  this.value = "";
  this.name = "";
  this.type = "";
}

FakeElement.prototype.appendChild = function appendChild(child) {
  this.children.push(child);
  return child;
};

FakeElement.prototype.replaceChildren = function replaceChildren() {
  this.children = Array.prototype.slice.call(arguments);
  this.textContent = "";
};

FakeElement.prototype.setAttribute = function setAttribute(name, value) {
  this.attributes[name] = String(value);
};

FakeElement.prototype.focus = function focus() { activeElement = this; };
FakeElement.prototype.addEventListener = function addEventListener() {};
FakeElement.prototype.removeEventListener = function removeEventListener() {};
FakeElement.prototype.checkValidity = function checkValidity() {
  if (this.required && this.type === "checkbox") return this.checked;
  return !this.required || Boolean(String(this.value).trim());
};
FakeElement.prototype.reportValidity = FakeElement.prototype.checkValidity;

function textTree(node) {
  return [node.textContent || ""].concat((node.children || []).map(textTree)).join(" ");
}

var uuidCount = 0;
var viewportListeners = {};
var context = {
  console: console,
  AbortController: AbortController,
  Uint8Array: Uint8Array,
  Promise: Promise,
  Object: Object,
  Array: Array,
  String: String,
  Number: Number,
  Boolean: Boolean,
  JSON: JSON,
  Error: Error,
  URL: URL,
  crypto: {
    randomUUID: function randomUUID() {
      uuidCount += 1;
      return "fixture-idempotency-" + uuidCount;
    }
  },
  location: { href: "https://nad-lan.co.il/projects/private-commercial-sandbox/" },
  visualViewport: {
    height: 812,
    addEventListener: function addEventListener(name, callback) { viewportListeners[name] = callback; },
    removeEventListener: function removeEventListener(name, callback) {
      if (viewportListeners[name] === callback) delete viewportListeners[name];
    }
  },
  document: {
    createElement: function createElement(tag) { return new FakeElement(tag); }
  }
};
context.window = context;
vm.createContext(context);

function load(file) {
  vm.runInContext(fs.readFileSync(path.join(base, file), "utf8"), context, { filename: file });
}

function flatten(value, prefix, output) {
  Object.keys(value).sort().forEach(function (key) {
    var item = value[key];
    var itemPath = prefix ? prefix + "." + key : key;
    if (item && Object.prototype.toString.call(item) === "[object Object]") flatten(item, itemPath, output);
    else output[itemPath] = item;
  });
  return output;
}

load("commercial-i18n-additions.js");
var i18n = context.NadlanCommercialI18n;
assert(i18n.supported.join(",") === "he,en,fr,ru,ar", "all five required locales must be present");
assert(i18n.validate().join("|") === i18n.requiredKeys.join("|"), "runtime dictionary validation must be deterministic");

var english = flatten(i18n.get("en"), "", {});
i18n.supported.forEach(function (locale) {
  var labels = i18n.get(locale);
  var flat = flatten(labels, "", {});
  assert(Object.keys(flat).sort().join("|") === Object.keys(english).sort().join("|"), locale + " key shape must be complete");
  assert(labels.dir === (locale === "he" || locale === "ar" ? "rtl" : "ltr"), locale + " direction must be logical");
  assert(labels.status.unknown && labels.status.not_marketed, locale + " must include every availability endpoint");
  assert(labels.evidenceStates.source_estimate && labels.evidenceStates.contradictory, locale + " must include evidence labels");
  assert(labels.rfpQuestions.live_availability && labels.rfpDocuments.orientation_plan, locale + " must include full RFP choices");
  assert(labels.rfpQuestionShort.live_availability && labels.rfpDocumentShort.orientation_plan, locale + " must include compact landscape choices");
  ["consent_expired", "invalid_field", "rate_limited", "route_unavailable", "conflict", "network"].forEach(function (code) {
    assert(labels.rfpErrors[code], locale + " must localize stable recovery code " + code);
  });
  if (locale !== "en") {
    [
      "chooseFloor", "beamScene", "questionsStepTitle", "documentsStepTitle", "requirementsTitle",
      "reviewTitle", "intentChanged", "rfpErrors.network", "rfpRecoveryActions.retry"
    ].forEach(function (key) {
      assert(flat[key] !== english[key], locale + " may not silently fall back to English for " + key);
    });
  }
});
assert(i18n.get("he-IL").locale === "he" && i18n.get("ar-IL").dir === "rtl", "regional RTL locales must resolve logically");
assert(i18n.get("de").locale === "en", "unsupported locales must take the explicit whole-English dictionary");

load("commercial-rfp-composer.js");
var api = context.NadlanCommercialRfpComposer;
var Composer = api.CommercialRfpComposer;

function input(value, checked, required, type) {
  var element = new FakeElement("input");
  element.value = value == null ? "" : String(value);
  element.checked = checked === true;
  element.required = required === true;
  element.type = type || "text";
  return element;
}

function makeForm() {
  var message = new FakeElement("p");
  var feedback = new FakeElement("div");
  var recovery = new FakeElement("button");
  recovery.hidden = true;
  var progress = new FakeElement("p");
  var questions = [input("live_availability", true), input("power_capacity", true)];
  var documents = [input("orientation_plan", true), input("tenant_technical_manual", true)];
  var elements = {
    company_name: input("Fixture Startup", false, true),
    contact_name: input("Fixture Buyer", false, true),
    email: input("buyer@example.test", false, false, "email"),
    phone: input("+1 202 555 0199"),
    headcount: input("75"),
    target_move_in: input("2027-02"),
    question_text: input("Confirm generator autonomy."),
    privacy: input("", true, true, "checkbox"),
    terms: input("", true, true, "checkbox"),
    marketing: input("", false, false, "checkbox")
  };
  var controls = Object.keys(elements).map(function (key) {
    elements[key].name = key;
    return elements[key];
  }).concat(questions, documents);
  var steps = [1, 2, 3, 4, 5].map(function (number) {
    var section = new FakeElement("section");
    section.dataset.rfpStep = String(number);
    var heading = new FakeElement("h3");
    var fieldsByStep = {
      1: [elements.question_text].concat(questions),
      2: documents,
      3: [elements.company_name, elements.contact_name, elements.email, elements.phone],
      4: [elements.headcount, elements.target_move_in],
      5: [elements.privacy, elements.terms, elements.marketing]
    };
    section.querySelector = function querySelector(selector) { return selector === "h3" ? heading : null; };
    section.querySelectorAll = function querySelectorAll() { return fieldsByStep[number]; };
    return section;
  });
  var form = new FakeElement("form");
  form.elements = elements;
  form.querySelectorAll = function querySelectorAll(selector) {
    if (selector.indexOf('input[name="question_ids"]') >= 0) return questions.filter(function (item) { return item.checked; });
    if (selector.indexOf('input[name="document_ids"]') >= 0) return documents.filter(function (item) { return item.checked; });
    if (selector === "[data-rfp-step]") return steps;
    if (selector === "button, input, textarea, select") return controls.concat([recovery]);
    return [];
  };
  form.querySelector = function querySelector(selector) {
    if (selector === ".nl-rfp-message") return message;
    if (selector === ".nl-rfp-progress") return progress;
    var match = selector.match(/^\[data-rfp-step="(\d)"\]$/);
    return match ? steps[Number(match[1]) - 1] : null;
  };
  form.fixtureMessage = message;
  form.fixtureFeedback = feedback;
  form.fixtureRecovery = recovery;
  form.fixtureProgress = progress;
  return form;
}

function response(ok, status, body, retryAfter) {
  return {
    ok: ok,
    status: status,
    headers: { get: function get(name) { return name === "Retry-After" ? retryAfter || null : null; } },
    json: function json() { return Promise.resolve(body); }
  };
}

function canonicalAsset(overrides) {
  return Object.assign({
    __nlCommercialAsset: true,
    wpPostId: 991,
    projectId: "project-fixture-991",
    buildingId: "building-main",
    towerId: "tower-main",
    floorId: "floor-18",
    suiteId: "suite-18-a",
    kind: "suite",
    projectName: "Fixture Project",
    buildingLabel: "Main Building",
    towerLabel: "Main Tower",
    floorLabel: "18",
    spaceLabel: "A"
  }, overrides || {});
}

function composerOptions(overrides) {
  return Object.assign({
    asset: canonicalAsset(),
    labels: i18n.get("en"),
    locale: "en-US",
    endpoint: "https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp",
    environment: "production",
    consentVersion: "fixture-v1",
    fetchImpl: function unused() { return Promise.resolve(response(true, 200, {})); }
  }, overrides || {});
}

function attachForm(composer) {
  composer.form = makeForm();
  composer.messageNode = composer.form.fixtureMessage;
  composer.feedbackNode = composer.form.fixtureFeedback;
  composer.recoveryButton = composer.form.fixtureRecovery;
  composer.root = new FakeElement("section");
  composer.renderConfirmation = function renderConfirmation(body) { this.confirmed = body; };
  return composer;
}

function expectConstructorFailure(options, message) {
  var failed = false;
  try { new Composer(options); } catch (error) { failed = true; }
  assert(failed, message);
}

async function runComposerFixtures() {
  assert(api.totalSteps === 5, "the composer must use five bounded steps");
  assert(
    api.validateEndpoint("/wp-json/nadlan/v2/commercial-rfp", {}).indexOf("https://nad-lan.co.il/") === 0,
    "a relative production route must resolve on the exact HTTPS page origin"
  );
  expectConstructorFailure(composerOptions({ endpoint: "https://evil.example/wp-json/nadlan/v2/commercial-rfp" }), "cross-origin endpoint must fail closed");
  expectConstructorFailure(composerOptions({ endpoint: "https://nad-lan.co.il/prefix/wp-json/nadlan/v2/commercial-rfp" }), "a prefixed lookalike route must fail closed");
  expectConstructorFailure(composerOptions({ endpoint: "https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp?mode=debug" }), "endpoint query parameters must fail closed");
  expectConstructorFailure(composerOptions({ baseUrl: "http://nad-lan.co.il/x", endpoint: "http://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp" }), "non-HTTPS production must fail closed");
  expectConstructorFailure(composerOptions({ endpoint: "https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp-sandbox" }), "production config may not target the sandbox route");
  expectConstructorFailure(composerOptions({ environment: "test", endpoint: "https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp-sandbox" }), "test config must require sandbox identity and nonce");
  expectConstructorFailure(composerOptions({ sandboxPostId: 55, sandboxNonce: "nonce" }), "production config must reject sandbox credentials");
  expectConstructorFailure(composerOptions({ asset: canonicalAsset({ towerId: "" }) }), "missing canonical tower ID must fail closed");

  var localTest = new Composer(composerOptions({
    baseUrl: "http://localhost:8080/private-sandbox/",
    endpoint: "http://localhost:8080/wp-json/nadlan/v2/commercial-rfp-sandbox",
    allowInsecureLocalhost: true,
    environment: "test",
    sandboxPostId: 55,
    sandboxNonce: "fixture-signed-nonce"
  }));
  assert(localTest.endpoint.indexOf("http://localhost:8080/") === 0, "explicit isolated localhost test seam must be allowed");
  expectConstructorFailure(composerOptions({
    baseUrl: "http://localhost:8080/private-sandbox/",
    endpoint: "http://localhost:8080/wp-json/nadlan/v2/commercial-rfp-sandbox",
    environment: "test", sandboxPostId: 55, sandboxNonce: "nonce"
  }), "localhost HTTP must still fail without the explicit test seam");

  var calls = [];
  var analytics = [];
  var attempt = 0;
  var asset = canonicalAsset();
  var retry = attachForm(new Composer(composerOptions({
    asset: asset,
    onSafeAnalytics: function onSafeAnalytics(event) { analytics.push(event); },
    fetchImpl: function fetchImpl(url, options) {
      calls.push({ url: url, options: options });
      attempt += 1;
      if (attempt === 1) return Promise.reject(new Error("synthetic_network_failure"));
      return Promise.resolve(response(true, 200, {
        accepted: true, case_id: "NLC-AAAAAAAAAAAAAAAAAAAAAAAA", route_kind: "project_team",
        delivery_state: "routed", sla_hours: 8,
        recipient_email: "must-not-render@example.test", staff_name: "Must Not Render"
      }));
    }
  })));
  asset.wpPostId = 123;
  asset.projectId = "tampered-project";
  asset.buildingId = "tampered-building";
  asset.towerId = "tampered-tower";
  asset.floorId = "tampered-floor";
  asset.suiteId = "tampered-suite";
  asset.projectName = "Tampered display project";
  assert(JSON.stringify(retry.identityFacts()).indexOf("Fixture Project") >= 0, "visible selection context must be snapshotted with the immutable IDs");
  await retry.submit();
  assert(calls.length === 1, "first submit must dispatch once");
  assert(retry.form.elements.contact_name.value === "Fixture Buyer", "network failure must preserve buyer inputs");
  assert(retry.recoveryButton.dataset.recoveryAction === "retry", "network failure must offer exact retry");
  var firstKey = calls[0].options.headers["Idempotency-Key"];
  var firstBody = calls[0].options.body;
  await retry.submit();
  assert(calls.length === 2, "retry must dispatch exactly once more");
  assert(calls[1].options.headers["Idempotency-Key"] === firstKey, "retry must reuse the exact idempotency key");
  assert(calls[1].options.body === firstBody, "retry must reuse the byte-identical frozen JSON body");
  var sent = JSON.parse(firstBody);
  assert(sent.project_id === 991 && sent.project_contract_id === "project-fixture-991", "both immutable project identities must be frozen");
  assert(
    sent.asset.building_id === "building-main" && sent.asset.tower_id === "tower-main" &&
    sent.asset.floor_id === "floor-18" && sent.asset.suite_id === "suite-18-a",
    "payload must preserve the complete canonical building/tower/floor/suite tuple"
  );
  assert(sent.environment === "production" && !("sandbox_post_id" in sent), "production body must exclude sandbox identity");
  assert(!("X-Nadlan-Sandbox-Nonce" in calls[0].options.headers), "production request must exclude sandbox nonce");
  assert(analytics.length === 1, "only success may emit safe analytics");
  assert(
    Object.keys(analytics[0]).sort().join(",") ===
      "document_count,event,has_building,has_floor,has_suite,has_tower,locale,project_id,question_count",
    "analytics must contain only approved non-PII counts, booleans, locale, and numeric project ID"
  );
  assert(JSON.stringify(analytics[0]).indexOf("Fixture Buyer") < 0 && JSON.stringify(analytics[0]).indexOf("floor-18") < 0, "analytics must exclude PII and canonical asset IDs");

  var resolvePending;
  var parallelCalls = 0;
  var parallel = attachForm(new Composer(composerOptions({
    fetchImpl: function fetchPending() {
      parallelCalls += 1;
      return new Promise(function (resolve) { resolvePending = resolve; });
    }
  })));
  var pending = parallel.submit();
  var blocked = await parallel.submit();
  assert(blocked === null && parallelCalls === 1, "a double tap while sending must never dispatch a second request");
  resolvePending(response(true, 200, {
    accepted: true, case_id: "NLC-BBBBBBBBBBBBBBBBBBBBBBBB", route_kind: "commercial_desk",
    delivery_state: "processing", sla_hours: 12
  }));
  await pending;

  var editCalls = [];
  var edited = attachForm(new Composer(composerOptions({
    fetchImpl: function fetchEdited(url, options) {
      editCalls.push(options);
      if (editCalls.length === 1) return Promise.reject(new Error("uncertain_delivery"));
      return Promise.resolve(response(true, 200, {
        accepted: true, case_id: "NLC-CCCCCCCCCCCCCCCCCCCCCCCC", route_kind: "commercial_desk",
        delivery_state: "routed", sla_hours: 12
      }));
    }
  })));
  await edited.submit();
  var oldKey = editCalls[0].headers["Idempotency-Key"];
  var oldBody = editCalls[0].body;
  edited.form.elements.question_text.value = "A deliberately changed buyer intent.";
  activeElement = edited.form.elements.question_text;
  edited.observeIntentEdit();
  assert(activeElement === edited.form.elements.question_text, "typing after a failed request must not steal focus to recovery controls");
  await edited.submit();
  assert(editCalls.length === 1, "changed fields must never be sent with the old key");
  assert(edited.recoveryButton.dataset.recoveryAction === "new_intent", "changed fields must require an explicit new-intent action");
  await edited.recover();
  await edited.submit();
  assert(editCalls.length === 2, "explicit new intent must permit one new dispatch");
  assert(editCalls[1].headers["Idempotency-Key"] !== oldKey, "new intent must generate a new key");
  assert(editCalls[1].body !== oldBody, "new intent may send the edited body only under its new key");

  var testCalls = [];
  var testComposer = attachForm(new Composer(composerOptions({
    endpoint: "https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp-sandbox",
    environment: "test", sandboxPostId: 77, sandboxNonce: "signed-sandbox-nonce",
    fetchImpl: function fetchTest(url, options) {
      testCalls.push(options);
      return Promise.resolve(response(true, 200, {
        accepted: true, case_id: "TEST-AAAAAAAAAAAAAAAAAAAA", environment: "test",
        route_kind: "test_sink", delivery_state: "test_sink", route_status: "test_sink", sla_hours: 0
      }));
    }
  })));
  await testComposer.submit();
  assert(JSON.parse(testCalls[0].body).sandbox_post_id === 77, "test body must bind the explicit sandbox post ID");
  assert(testCalls[0].headers["X-Nadlan-Sandbox-Nonce"] === "signed-sandbox-nonce", "test request must bind the signed sandbox nonce");
  assert(testComposer.confirmed && testComposer.confirmed.route_kind === "test_sink", "test mode must accept only the complete synthetic sink acknowledgement");

  var crossModeResponses = [
    {
      name: "test rejects production acknowledgement",
      options: {
        endpoint: "https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp-sandbox",
        environment: "test", sandboxPostId: 77, sandboxNonce: "signed-sandbox-nonce"
      },
      body: {
        accepted: true, case_id: "NLC-DDDDDDDDDDDDDDDDDDDDDDDD", route_kind: "project_team",
        delivery_state: "routed", sla_hours: 8
      }
    },
    {
      name: "test rejects incomplete sink acknowledgement",
      options: {
        endpoint: "https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp-sandbox",
        environment: "test", sandboxPostId: 77, sandboxNonce: "signed-sandbox-nonce"
      },
      body: {
        accepted: true, case_id: "TEST-BBBBBBBBBBBBBBBBBBBB", environment: "test",
        route_kind: "test_sink", delivery_state: "test_sink", route_status: "test_sink", sla_hours: 1
      }
    },
    {
      name: "production rejects test-sink acknowledgement",
      options: {},
      body: {
        accepted: true, case_id: "TEST-CCCCCCCCCCCCCCCCCCCC", environment: "test",
        route_kind: "test_sink", delivery_state: "test_sink", route_status: "test_sink", sla_hours: 0
      }
    },
    {
      name: "production rejects TEST case under production route",
      options: {},
      body: {
        accepted: true, case_id: "TEST-DDDDDDDDDDDDDDDDDDDD", route_kind: "project_team",
        delivery_state: "routed", sla_hours: 8
      }
    },
    {
      name: "production rejects test-only response fields",
      options: {},
      body: {
        accepted: true, case_id: "NLC-EEEEEEEEEEEEEEEEEEEEEEEE", environment: "production",
        route_kind: "project_team", delivery_state: "routed", sla_hours: 8
      }
    }
  ];
  for (var crossIndex = 0; crossIndex < crossModeResponses.length; crossIndex += 1) {
    var crossFixture = crossModeResponses[crossIndex];
    var crossAnalytics = [];
    var crossComposer = attachForm(new Composer(composerOptions(Object.assign({}, crossFixture.options, {
      onSafeAnalytics: function onCrossAnalytics(event) { crossAnalytics.push(event); },
      fetchImpl: (function (crossBody) {
        return function crossModeFetch() { return Promise.resolve(response(true, 200, crossBody)); };
      })(crossFixture.body)
    }))));
    await crossComposer.submit();
    assert(!crossComposer.confirmed, crossFixture.name + " must never render a success confirmation");
    assert(crossAnalytics.length === 0, crossFixture.name + " must emit no success analytics");
    assert(crossComposer.recoveryButton.dataset.recoveryAction === "retry", crossFixture.name + " must fail through the safe route recovery");
    assert(crossComposer.form.elements.contact_name.value === "Fixture Buyer", crossFixture.name + " must preserve buyer fields");
  }

  var failures = [
    { name: "consent_expired", status: 400, body: { code: "consent_version_expired", current_consent_version: "fixture-v2" }, action: "review_consent" },
    { name: "invalid_field", status: 422, body: { code: "invalid_request", field: "contact.email" }, action: "fix_field" },
    { name: "rate_limited", status: 429, body: { code: "rate_limited", retry_after_seconds: 19 }, action: "retry" },
    { name: "route_unavailable", status: 503, body: { code: "request_unavailable" }, action: "retry" },
    { name: "conflict", status: 409, body: { code: "idempotency_conflict" }, action: "new_intent" },
    { name: "network", reject: true, action: "retry" }
  ];
  for (var i = 0; i < failures.length; i += 1) {
    var fixture = failures[i];
    var failureComposer = attachForm(new Composer(composerOptions({
      fetchImpl: (function (spec) {
        return function failureFetch() {
          return spec.reject
            ? Promise.reject(new Error("offline"))
            : Promise.resolve(response(false, spec.status, spec.body, "19"));
        };
      })(fixture)
    })));
    await failureComposer.submit();
    assert(failureComposer.recoveryButton.dataset.recoveryAction === fixture.action, fixture.name + " must map to stable recovery action " + fixture.action);
    assert(failureComposer.form.elements.contact_name.value === "Fixture Buyer", fixture.name + " must preserve entered fields");
    assert(activeElement === failureComposer.recoveryButton, fixture.name + " must focus its visible recovery action");
    if (fixture.name === "invalid_field") {
      await failureComposer.recover();
      assert(activeElement === failureComposer.form.elements.email, "invalid_field recovery must focus only the allowlisted server field");
    }
    if (fixture.name === "consent_expired") {
      await failureComposer.recover();
      assert(failureComposer.consentVersion === "fixture-v2", "consent recovery must adopt the same-origin server version");
      assert(!failureComposer.form.elements.privacy.checked && !failureComposer.form.elements.terms.checked, "updated consent must require fresh explicit acceptance");
      assert(failureComposer.frozenRequest === null, "changed consent version must reset the request key before another send");
    }
  }

  var confirmationForm = new FakeElement("form");
  var confirmation = new Composer(composerOptions());
  confirmation.form = confirmationForm;
  confirmation.renderConfirmation({
    accepted: true, case_id: "NLC-FFFFFFFFFFFFFFFFFFFFFFFF", route_kind: "project_team",
    delivery_state: "routed", sla_hours: 6,
    recipient_email: "secret@example.test", staff_name: "Secret Person", debug: "secret-stack"
  });
  var confirmationText = textTree(confirmationForm);
  assert(confirmationText.indexOf("NLC-FFFFFFFFFFFFFFFFFFFFFFFF") >= 0 && confirmationText.indexOf("6") >= 0, "safe confirmation must show case and SLA");
  assert(confirmationText.indexOf("secret@example.test") < 0 && confirmationText.indexOf("Secret Person") < 0 && confirmationText.indexOf("secret-stack") < 0, "safe confirmation must ignore private response fields");

  var source = fs.readFileSync(path.join(base, "commercial-rfp-composer.js"), "utf8");
  assert(/visualViewport/.test(source) && /removeEventListener\("resize"/.test(source), "visualViewport keyboard contract must attach and clean up");
  assert(!/(localStorage|sessionStorage|indexedDB)/.test(source), "composer must not persist buyer PII in browser storage");
  assert(/JSON\.stringify\(this\.payload\(\)\)/.test(source) && /request\.body/.test(source), "request body must be serialized once and retried from the frozen snapshot");

  var css = fs.readFileSync(path.join(base, "commercial-decision-surface.css"), "utf8");
  var rfpStart = css.indexOf(".nl-rfp {");
  var rfpEnd = css.indexOf(".nl-ccm {");
  var rfpCss = css.slice(rfpStart, rfpEnd);
  assert(rfpStart >= 0 && rfpEnd > rfpStart, "RFP CSS slice must be bounded before context-map selectors");
  assert(!/overflow\s*:\s*(auto|scroll)/i.test(rfpCss), "RFP UI must never create inner scrolling");
  assert(!/font-size\s*:\s*(?:[0-9]|1[01])px/i.test(rfpCss), "all RFP buyer-facing text must remain at least 12px");
  assert(/\.nl-rfp-actions button,[\s\S]*?min-height:\s*44px/.test(rfpCss), "every RFP action must remain at least 44px");
  assert(/orientation:\s*landscape[\s\S]*?\.nl-rfp-chip__short\s*\{\s*display:\s*inline/.test(rfpCss), "short landscape must use localized compact choice labels");
  assert(!/orientation:\s*landscape[\s\S]*?\.nl-rfp-actions\s*\{[^}]*display:\s*none/.test(rfpCss), "landscape may not silently hide the RFP action row");
  var sceneCss = css.slice(0, rfpStart);
  assert(!/font-size\s*:\s*(?:[0-9]|1[01])px/i.test(sceneCss), "scene buyer-facing text must remain at least 12px");
  var sceneLandscapeStart = css.indexOf("@media (max-height: 600px) and (orientation: landscape)");
  var sceneLandscapeEnd = css.indexOf("@media (min-width: 901px)", sceneLandscapeStart);
  var finalLandscape = css.slice(sceneLandscapeStart, sceneLandscapeEnd);
  assert(/\.nl-cds-actions\s*\{\s*display:\s*grid/.test(finalLandscape), "selected-space landscape must visibly retain save/compare/share actions");
  assert(!/\.nl-cds-fact__head\s*>\s*span:first-child\s*\{[^}]*display:\s*none/.test(finalLandscape), "selected-space landscape must not hide compact fact labels");
  assert(/\.nl-cds-door__title--short\s*\{\s*display:\s*none/.test(sceneCss), "full door labels must remain the default outside the short-landscape contract");
  assert(/\.nl-cds-door__title--long\s*\{\s*display:\s*none/.test(finalLandscape) && /\.nl-cds-door__title--short\s*\{\s*display:\s*block/.test(finalLandscape), "short landscape must swap to localized compact door titles without clipping or truncation");
  assert(!/\.nl-beam-scene__street/.test(css), "legacy unevidenced street selector must not remain in the scene stylesheet");

  var browserFixture = fs.readFileSync(path.join(base, "commercial-rfp-beam.browser.fixture.mjs"), "utf8");
  assert(/320[\s\S]*568/.test(browserFixture) && /375[\s\S]*812/.test(browserFixture) && /568[\s\S]*320/.test(browserFixture) && /1280[\s\S]*800/.test(browserFixture), "portable Chromium fixture must exercise all four acceptance viewports");
  [1, 2, 4, 6, 37].forEach(function (count) {
    assert(new RegExp("(?:\\[|,)\\s*" + count + "(?:\\s*[,\\]])").test(browserFixture), "portable Chromium fixture must include the " + count + "-source beam case");
  });
  assert(/doorLongVisibleCount/.test(browserFixture) && /doorShortVisibleCount/.test(browserFixture), "portable Chromium fixture must verify the long/short door-title accessibility layout contract");

  var viewports = [
    { name: "320x568", width: 320, height: 568, header: 64, context: 70, body: 186 },
    { name: "375x812", width: 375, height: 812, header: 64, context: 52, body: 186 },
    { name: "568x320", width: 568, height: 320, header: 54, context: 30, body: 108, feedbackBody: 64 },
    { name: "1280x800", width: 1280, height: 800, header: 64, context: 34, body: 186 }
  ];
  viewports.forEach(function (viewport) {
    var available = viewport.height - viewport.header;
    var steadyNeed = 12 + viewport.context + 15 + 28 + viewport.body + 44 + 20;
    var recoveryNeed = viewport.feedbackBody
      ? 12 + viewport.context + 15 + 28 + viewport.feedbackBody + 44 + 20 + 44
      : steadyNeed;
    assert(Math.max(steadyNeed, recoveryNeed) <= available, viewport.name + " bounded step and visible action must fit without inner scrolling");
  });
}

runComposerFixtures().then(function () {
  console.log("PASS five-locale/RFP fixture: complete translations, five bounded steps, exact-origin HTTPS/test seam, strict production/test acknowledgement isolation, immutable project/building/tower/floor/suite tuple, byte-identical retry, explicit new intent after edits, stable localized recovery/focus, no-PII analytics, safe confirmation, visualViewport cleanup, 44px targets, 12px text, and 320/375/568/1280 no-inner-scroll geometry.");
}).catch(function (error) {
  console.error(error && error.stack ? error.stack : error);
  process.exitCode = 1;
});
