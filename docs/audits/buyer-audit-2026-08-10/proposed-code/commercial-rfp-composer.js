/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Bounded, DOM-only commercial RFP composer for the proposed REST contract.
 *
 * Retry rule: one idempotency key is permanently paired with one exact JSON
 * body. A buyer edit never reuses that key. The buyer must explicitly accept
 * the edit as a new intent before a new key can be generated.
 */
(function commercialRfpComposerModule(window, document) {
  "use strict";

  var QUESTION_IDS = [
    "live_availability",
    "asking_rent",
    "net_to_gross",
    "power_capacity",
    "commute_and_transport",
    "nearby_facilities"
  ];
  var DOCUMENT_IDS = [
    "availability_schedule",
    "floor_plan_pdf",
    "measurement_report",
    "tenant_technical_manual",
    "orientation_plan",
    "lease_draft"
  ];
  var TOTAL_STEPS = 5;
  var QUESTION_TEXT_LIMIT = 100;
  var SERVER_FIELD_NAMES = Object.freeze({
    "company.name": "company_name",
    company_name: "company_name",
    "contact.name": "contact_name",
    contact_name: "contact_name",
    "contact.email": "email",
    email: "email",
    "contact.phone": "phone",
    phone: "phone",
    "requirements.headcount": "headcount",
    headcount: "headcount",
    "requirements.target_move_in": "target_move_in",
    target_move_in: "target_move_in",
    "consent.privacy": "privacy",
    privacy: "privacy",
    "consent.terms": "terms",
    terms: "terms",
    "consent.marketing": "marketing",
    marketing: "marketing",
    question_ids: "question_ids",
    document_ids: "document_ids",
    question_text: "question_text"
  });
  var SERVER_CODE_ALIASES = Object.freeze({
    consent_expired: "consent_expired",
    nadlan_rfp_consent_expired: "consent_expired",
    invalid_consent_version: "consent_expired",
    consent_version_expired: "consent_expired",
    invalid_field: "invalid_field",
    nadlan_rfp_invalid_field: "invalid_field",
    rest_invalid_param: "invalid_field",
    invalid_request: "invalid_field",
    invalid_asset: "invalid_field",
    invalid_project: "invalid_field",
    consent_required: "invalid_field",
    rate_limited: "rate_limited",
    nadlan_rfp_rate_limited: "rate_limited",
    route_unavailable: "route_unavailable",
    nadlan_rfp_route_unavailable: "route_unavailable",
    service_unavailable: "route_unavailable",
    request_unavailable: "route_unavailable",
    request_in_progress: "route_unavailable",
    conflict: "conflict",
    idempotency_conflict: "conflict",
    nadlan_rfp_idempotency_conflict: "conflict"
  });

  function str(value) {
    return value == null ? "" : String(value);
  }

  function localeBase(value) {
    var base = str(value || "en").toLowerCase().split(/[-_]/)[0];
    return ["he", "en", "fr", "ru", "ar"].indexOf(base) >= 0 ? base : "en";
  }

  function node(tag, className, text) {
    var element = document.createElement(tag);
    if (className) element.className = className;
    if (text != null) element.textContent = str(text);
    return element;
  }

  function setAttribute(element, name, value) {
    if (element && typeof element.setAttribute === "function") {
      element.setAttribute(name, str(value));
    }
  }

  function replaceTokens(template, values) {
    return str(template).replace(/\{([a-z_]+)\}/gi, function (_, key) {
      return Object.prototype.hasOwnProperty.call(values, key) ? str(values[key]) : "";
    });
  }

  function canonicalId(value, name) {
    var id = str(value).trim();
    if (!id || id.length > 180 || /[\u0000-\u001f\u007f]/.test(id)) {
      throw new Error("Missing or invalid immutable " + name + ".");
    }
    return id;
  }

  function optionalCanonicalId(value, name) {
    if (value == null || value === "") return null;
    return canonicalId(value, name);
  }

  function isLoopback(hostname) {
    var host = str(hostname).toLowerCase().replace(/^\[|\]$/g, "");
    return host === "localhost" || host === "127.0.0.1" || host === "::1";
  }

  function validateEndpoint(rawEndpoint, options) {
    options = options || {};
    var Url = window.URL;
    if (typeof Url !== "function") throw new Error("URL validation is unavailable.");
    if (options.baseUrl && options.allowInsecureLocalhost !== true) {
      throw new Error("A location override is allowed only by the isolated localhost test seam.");
    }
    var baseHref = str(options.baseUrl || (window.location && window.location.href));
    var base;
    var target;
    try {
      base = new Url(baseHref);
      target = new Url(str(rawEndpoint), base);
    } catch (error) {
      throw new Error("The RFP endpoint is invalid.");
    }
    if (options.baseUrl && (!isLoopback(base.hostname) || !isLoopback(target.hostname))) {
      throw new Error("The isolated test location override must remain on loopback.");
    }
    var insecureLocalTest =
      options.allowInsecureLocalhost === true &&
      base.protocol === "http:" &&
      target.protocol === "http:" &&
      isLoopback(base.hostname) &&
      isLoopback(target.hostname);
    if (target.origin !== base.origin) {
      throw new Error("The RFP endpoint must have the exact page origin.");
    }
    if (base.protocol !== "https:" && !insecureLocalTest) {
      throw new Error("The RFP page must use HTTPS.");
    }
    if (target.protocol !== "https:" && !insecureLocalTest) {
      throw new Error("The RFP endpoint must use HTTPS.");
    }
    if (target.username || target.password || target.hash || target.search) {
      throw new Error("The RFP endpoint may not contain credentials, a query, or a fragment.");
    }
    return target.href;
  }

  function validateEndpointRoute(endpoint, environment) {
    var pathname = new window.URL(endpoint).pathname.replace(/\/+$/, "");
    var expected = environment === "test"
      ? /^\/(?:wp-json\/)?nadlan\/v2\/commercial-rfp-sandbox$/
      : /^\/(?:wp-json\/)?nadlan\/v2\/commercial-rfp$/;
    if (!expected.test(pathname)) {
      throw new Error("The RFP endpoint does not match the explicit " + environment + " route.");
    }
  }

  function field(label, name, type, required, autocomplete, attributes) {
    var wrapper = node("label", "nl-rfp-field");
    wrapper.appendChild(node("span", "nl-rfp-field__label", label));
    var input = document.createElement("input");
    input.name = name;
    input.type = type || "text";
    input.required = Boolean(required);
    if (autocomplete) input.autocomplete = autocomplete;
    Object.keys(attributes || {}).forEach(function (key) {
      setAttribute(input, key, attributes[key]);
    });
    wrapper.appendChild(input);
    return wrapper;
  }

  function idempotencyKey() {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return window.crypto.randomUUID();
    }
    if (window.crypto && typeof window.crypto.getRandomValues === "function") {
      var bytes = new Uint8Array(16);
      window.crypto.getRandomValues(bytes);
      return Array.prototype.map.call(bytes, function (value) {
        return value.toString(16).padStart(2, "0");
      }).join("");
    }
    throw new Error("Secure idempotency generation is unavailable.");
  }

  function checkedValues(root, name) {
    return Array.prototype.slice.call(
      root.querySelectorAll('input[name="' + name + '"]:checked')
    ).map(function (input) { return input.value; });
  }

  function basket(title, name, ids, labels, shortLabels, checkedId) {
    var fieldset = node("fieldset", "nl-rfp-basket");
    fieldset.appendChild(node("legend", "", title));
    ids.forEach(function (id) {
      var label = node("label", "nl-rfp-chip");
      var input = document.createElement("input");
      input.type = "checkbox";
      input.name = name;
      input.value = id;
      input.checked = id === checkedId;
      label.appendChild(input);
      label.appendChild(node("span", "nl-rfp-chip__long", (labels && labels[id]) || id.replace(/_/g, " ")));
      label.appendChild(node("span", "nl-rfp-chip__short", (shortLabels && shortLabels[id]) || (labels && labels[id]) || id.replace(/_/g, " ")));
      fieldset.appendChild(label);
    });
    return fieldset;
  }

  function actionButton(label, action, primary) {
    var button = node("button", primary ? "nl-rfp-primary" : "", label);
    button.type = "button";
    button.dataset.rfpAction = action;
    return button;
  }

  function compactPagerButton(label, action, symbol) {
    var button = actionButton("", action, false);
    setAttribute(button, "aria-label", label);
    button.appendChild(node("span", "nl-rfp-pager-label nl-rfp-pager-label--long", label));
    button.appendChild(node("span", "nl-rfp-pager-label nl-rfp-pager-label--short", symbol));
    setAttribute(button.lastChild, "aria-hidden", "true");
    setAttribute(button.firstChild, "aria-hidden", "true");
    return button;
  }

  function isObject(value) {
    return Boolean(value) && Object.prototype.toString.call(value) === "[object Object]";
  }

  function safeServerCode(status, body) {
    var raw = str(
      isObject(body) && (body.error_code || body.code || (isObject(body.data) && body.data.code))
    ).toLowerCase();
    if (SERVER_CODE_ALIASES[raw]) return SERVER_CODE_ALIASES[raw];
    if (status === 429) return "rate_limited";
    if (status === 503) return "route_unavailable";
    if (status === 409) return "conflict";
    if (status === 400 || status === 422) return "invalid_field";
    return "network";
  }

  function safeRetryAfter(response, body) {
    var raw = isObject(body) ? body.retry_after_seconds : null;
    if (raw == null && response && response.headers && typeof response.headers.get === "function") {
      raw = response.headers.get("Retry-After");
    }
    var seconds = Number(raw);
    return Number.isFinite(seconds) ? Math.max(1, Math.min(3600, Math.ceil(seconds))) : null;
  }

  function safeFieldName(body) {
    var raw = str(
      isObject(body) && (body.field || body.param || (isObject(body.data) && (body.data.field || body.data.param)))
    );
    return SERVER_FIELD_NAMES[raw] || "";
  }

  function stepForField(name) {
    if (name === "question_ids" || name === "question_text") return 1;
    if (name === "document_ids") return 2;
    if (["company_name", "contact_name", "email", "phone"].indexOf(name) >= 0) return 3;
    if (["headcount", "target_move_in"].indexOf(name) >= 0) return 4;
    return 5;
  }

  function CommercialRfpComposer(options) {
    options = options || {};
    if (!options.asset || options.asset.__nlCommercialAsset !== true) {
      throw new Error("An adapted immutable asset is required.");
    }
    this.asset = options.asset;
    this.labels = options.labels || {};
    this.locale = localeBase(options.locale || this.labels.locale);
    this.consentVersion = canonicalId(options.consentVersion, "consent version");
    this.fetchImpl = options.fetchImpl || window.fetch;
    this.refreshConsentVersion =
      typeof options.refreshConsentVersion === "function" ? options.refreshConsentVersion : null;
    this.onSafeAnalytics =
      typeof options.onSafeAnalytics === "function" ? options.onSafeAnalytics : function () {};
    var environment = canonicalId(options.environment, "request environment");
    if (["test", "production"].indexOf(environment) < 0) {
      throw new Error("The request environment must be explicitly test or production.");
    }
    this.endpoint = validateEndpoint(options.endpoint, {
      baseUrl: options.baseUrl,
      allowInsecureLocalhost: options.allowInsecureLocalhost === true
    });
    validateEndpointRoute(this.endpoint, environment);
    var sandboxPostId = options.sandboxPostId == null ? null : Number(options.sandboxPostId);
    var sandboxNonce = options.sandboxNonce == null ? "" : canonicalId(options.sandboxNonce, "sandbox nonce");
    if (
      (environment === "test" &&
        (!Number.isInteger(sandboxPostId) || sandboxPostId < 1 || !sandboxNonce)) ||
      (environment === "production" && (sandboxPostId !== null || sandboxNonce))
    ) {
      throw new Error("Sandbox identity and nonce must exist only for the explicit test environment.");
    }
    this.requestConfig = Object.freeze({
      environment: environment,
      sandboxPostId: sandboxPostId,
      sandboxNonce: sandboxNonce
    });
    this.context = Object.freeze({
      projectId: Number(this.asset.wpPostId),
      projectContractId: canonicalId(this.asset.projectId, "project contract ID"),
      buildingId: canonicalId(this.asset.buildingId, "building ID"),
      towerId: canonicalId(this.asset.towerId, "tower ID"),
      floorId: canonicalId(this.asset.floorId, "floor ID"),
      suiteId: this.asset.kind === "suite"
        ? canonicalId(this.asset.suiteId, "suite ID")
        : optionalCanonicalId(this.asset.suiteId, "suite ID")
    });
    this.displayContext = Object.freeze({
      projectName: str(this.asset.projectName).trim(),
      buildingLabel: str(this.asset.buildingLabel).trim(),
      towerLabel: str(this.asset.towerLabel).trim(),
      floorLabel: str(this.asset.floorLabel).trim(),
      spaceLabel: str(this.asset.spaceLabel).trim()
    });
    if (
      !Number.isInteger(this.context.projectId) ||
      this.context.projectId < 1 ||
      typeof this.fetchImpl !== "function"
    ) {
      throw new Error("Fetch and an immutable numeric WordPress project ID are required.");
    }
    this.root = null;
    this.form = null;
    this.step = 1;
    this.submitting = false;
    this.key = "";
    this.frozenRequest = null;
    this.intentChanged = false;
    this.lastFailure = null;
    this.abortController = null;
    this.messageNode = null;
    this.feedbackNode = null;
    this.recoveryButton = null;
    this.viewport = window.visualViewport || null;
    this.initialViewportHeight = Math.max(
      this.viewport ? Number(this.viewport.height) || 0 : 0,
      document.documentElement ? Number(document.documentElement.clientHeight) || 0 : 0
    );
    this.boundViewport = null;
    this.boundClick = null;
    this.boundSubmit = null;
    this.boundEdit = null;
  }

  CommercialRfpComposer.prototype.identityFacts = function identityFacts() {
    var labels = this.labels;
    var facts = [
      [labels.projectLabel || "Project", this.displayContext.projectName || this.context.projectContractId],
      [labels.buildingLabel || "Building", this.displayContext.buildingLabel || this.context.buildingId],
      [labels.towerLabel || "Tower", this.displayContext.towerLabel || this.context.towerId],
      [labels.floorLabel || "Floor", this.displayContext.floorLabel || this.context.floorId]
    ];
    if (this.context.suiteId) {
      facts.push([labels.suiteLabel || "Suite", this.displayContext.spaceLabel || this.context.suiteId]);
    }
    return facts;
  };

  CommercialRfpComposer.prototype.buildContext = function buildContext() {
    var labels = this.labels;
    var wrapper = node("section", "nl-rfp-context");
    setAttribute(wrapper, "aria-label", labels.selectedContext || "Selected space");
    wrapper.appendChild(node("strong", "nl-rfp-context__title", labels.selectedContext || "Selected space"));
    var list = node("dl", "nl-rfp-context__facts");
    this.identityFacts().forEach(function (fact) {
      var item = node("div", "nl-rfp-context__fact");
      item.appendChild(node("dt", "", fact[0]));
      item.appendChild(node("dd", "", fact[1]));
      list.appendChild(item);
    });
    wrapper.appendChild(list);
    return wrapper;
  };

  CommercialRfpComposer.prototype.buildStepShell = function buildStepShell(number, title) {
    var step = node("section", "nl-rfp-step");
    step.dataset.rfpStep = str(number);
    var titleNode = node("h3", "", title);
    titleNode.id = "nl-rfp-step-title-" + number;
    titleNode.tabIndex = -1;
    setAttribute(step, "aria-labelledby", titleNode.id);
    step.appendChild(titleNode);
    var body = node("div", "nl-rfp-step__body");
    step.appendChild(body);
    var actions = node("div", "nl-rfp-actions");
    if (number > 1) actions.appendChild(actionButton(this.labels.back || "Back", "back", false));
    if (number < TOTAL_STEPS) {
      actions.appendChild(actionButton(this.labels.continue || "Continue", "next", true));
    } else {
      var submit = actionButton(this.labels.send || "Ask the commercial team", "submit", true);
      submit.type = "submit";
      actions.appendChild(submit);
    }
    step.appendChild(actions);
    return { step: step, body: body };
  };

  CommercialRfpComposer.prototype.buildStepOne = function buildStepOne() {
    var labels = this.labels;
    var shell = this.buildStepShell(1, labels.questionsStepTitle || labels.questionsTitle || "Questions to answer");
    shell.body.className += " nl-rfp-step__body--questions";
    var chooser = node("div", "nl-rfp-question-chooser");
    var choices = node("div", "nl-rfp-question-choices");
    var questionBasket = basket(
      labels.questions || "Questions",
      "question_ids",
      QUESTION_IDS,
      labels.rfpQuestions,
      labels.rfpQuestionShort,
      "live_availability"
    );
    questionBasket.className += " nl-rfp-basket--paged";
    var questionChips = Array.prototype.slice.call(questionBasket.querySelectorAll(".nl-rfp-chip"));
    var pageSize = 2;
    var pageIndex = 0;
    var pager = node("div", "nl-rfp-choice-pager");
    setAttribute(pager, "role", "group");
    setAttribute(pager, "aria-label", labels.questionsPagination || "Question pages");
    var isRtl = this.locale === "he" || this.locale === "ar";
    var previous = compactPagerButton(labels.previous || "Previous", "question-page-previous", isRtl ? "›" : "‹");
    var pageStatus = node("span", "nl-rfp-choice-pager__status");
    setAttribute(pageStatus, "aria-live", "polite");
    setAttribute(pageStatus, "aria-atomic", "true");
    var next = compactPagerButton(labels.next || "Next", "question-page-next", isRtl ? "‹" : "›");
    pager.appendChild(previous);
    pager.appendChild(pageStatus);
    pager.appendChild(next);
    var showOther = actionButton(labels.writeOtherQuestion || labels.otherQuestion || "Write another question", "question-other", false);
    showOther.className += " nl-rfp-other-toggle";
    choices.appendChild(questionBasket);
    choices.appendChild(pager);
    choices.appendChild(showOther);

    var other = node("div", "nl-rfp-question-other");
    other.hidden = true;
    var free = node("label", "nl-rfp-field nl-rfp-field--wide");
    var questionLimit = replaceTokens(
      labels.questionTextLimit || "Up to {max} characters; the complete text stays visible.",
      { max: QUESTION_TEXT_LIMIT }
    );
    free.appendChild(node(
      "span",
      "nl-rfp-field__label",
      (labels.otherQuestion || "What else should the team answer?") + " — " + questionLimit
    ));
    var textarea = document.createElement("textarea");
    textarea.name = "question_text";
    textarea.maxLength = QUESTION_TEXT_LIMIT;
    textarea.rows = 6;
    free.appendChild(textarea);
    var backToChoices = actionButton(
      labels.backToQuestionChoices || labels.back || "Back to question choices",
      "question-choices",
      false
    );
    backToChoices.className += " nl-rfp-other-back";
    other.appendChild(free);
    other.appendChild(backToChoices);

    function updateQuestionPage(nextPage) {
      var pageCount = Math.ceil(questionChips.length / pageSize);
      pageIndex = Math.max(0, Math.min(pageCount - 1, nextPage));
      var start = pageIndex * pageSize;
      var end = Math.min(start + pageSize, questionChips.length);
      questionChips.forEach(function (chip, index) {
        chip.hidden = index < start || index >= end;
      });
      previous.disabled = pageIndex === 0;
      next.disabled = pageIndex === pageCount - 1;
      pageStatus.textContent = replaceTokens(
        labels.questionPageStatus || "Questions {start}-{end} of {total}",
        { start: start + 1, end: end, total: questionChips.length }
      );
    }

    previous.addEventListener("click", function () { updateQuestionPage(pageIndex - 1); });
    next.addEventListener("click", function () { updateQuestionPage(pageIndex + 1); });
    showOther.addEventListener("click", function () {
      choices.hidden = true;
      other.hidden = false;
      if (typeof textarea.focus === "function") textarea.focus({ preventScroll: true });
    });
    backToChoices.addEventListener("click", function () {
      other.hidden = true;
      choices.hidden = false;
      if (typeof showOther.focus === "function") showOther.focus({ preventScroll: true });
    });
    updateQuestionPage(0);
    chooser.appendChild(choices);
    chooser.appendChild(other);
    shell.body.appendChild(chooser);
    return shell.step;
  };

  CommercialRfpComposer.prototype.buildStepTwo = function buildStepTwo() {
    var labels = this.labels;
    var shell = this.buildStepShell(2, labels.documentsStepTitle || labels.documents || "Documents to receive");
    var choices = node("div", "nl-rfp-document-choices");
    var documentBasket = basket(
      labels.documents || "Documents",
      "document_ids",
      DOCUMENT_IDS,
      labels.rfpDocuments,
      labels.rfpDocumentShort,
      ""
    );
    documentBasket.className += " nl-rfp-basket--paged nl-rfp-basket--documents";
    var documentChips = Array.prototype.slice.call(documentBasket.querySelectorAll(".nl-rfp-chip"));
    var pageSize = 2;
    var pageIndex = 0;
    var pager = node("div", "nl-rfp-choice-pager nl-rfp-document-pager");
    setAttribute(pager, "role", "group");
    setAttribute(pager, "aria-label", labels.documentsPagination || "Document pages");
    var isRtl = this.locale === "he" || this.locale === "ar";
    var previous = compactPagerButton(labels.previous || "Previous", "document-page-previous", isRtl ? "›" : "‹");
    var pageStatus = node("span", "nl-rfp-choice-pager__status");
    setAttribute(pageStatus, "aria-live", "polite");
    setAttribute(pageStatus, "aria-atomic", "true");
    var next = compactPagerButton(labels.next || "Next", "document-page-next", isRtl ? "‹" : "›");
    pager.appendChild(previous);
    pager.appendChild(pageStatus);
    pager.appendChild(next);

    function updateDocumentPage(nextPage) {
      var pageCount = Math.ceil(documentChips.length / pageSize);
      pageIndex = Math.max(0, Math.min(pageCount - 1, nextPage));
      var start = pageIndex * pageSize;
      var end = Math.min(start + pageSize, documentChips.length);
      documentChips.forEach(function (chip, index) {
        chip.hidden = index < start || index >= end;
      });
      previous.disabled = pageIndex === 0;
      next.disabled = pageIndex === pageCount - 1;
      pageStatus.textContent = replaceTokens(
        labels.documentPageStatus || "Documents {start}-{end} of {total}",
        { start: start + 1, end: end, total: documentChips.length }
      );
    }

    previous.addEventListener("click", function () { updateDocumentPage(pageIndex - 1); });
    next.addEventListener("click", function () { updateDocumentPage(pageIndex + 1); });
    updateDocumentPage(0);
    choices.appendChild(documentBasket);
    choices.appendChild(pager);
    shell.body.appendChild(choices);
    return shell.step;
  };

  CommercialRfpComposer.prototype.buildStepThree = function buildStepThree() {
    var labels = this.labels;
    var shell = this.buildStepShell(3, labels.contactTitle || "Where should the complete answer reach you?");
    var fields = node("div", "nl-rfp-fields");
    fields.appendChild(field(labels.companyName || "Company", "company_name", "text", true, "organization"));
    fields.appendChild(field(labels.contactName || "Contact name", "contact_name", "text", true, "name"));
    fields.appendChild(field(labels.email || "Email", "email", "email", false, "email", { inputmode: "email" }));
    fields.appendChild(field(labels.internationalPhone || "International phone", "phone", "tel", false, "tel", { inputmode: "tel" }));
    shell.body.appendChild(fields);
    return shell.step;
  };

  CommercialRfpComposer.prototype.buildStepFour = function buildStepFour() {
    var labels = this.labels;
    var shell = this.buildStepShell(4, labels.requirementsTitle || "Timing and team size");
    var fields = node("div", "nl-rfp-fields nl-rfp-fields--requirements");
    fields.appendChild(field(labels.headcount || "Headcount", "headcount", "number", false, "", { min: "1", step: "1", inputmode: "numeric" }));
    fields.appendChild(field(labels.moveIn || "Target move-in (YYYY-MM)", "target_move_in", "month", false, ""));
    shell.body.appendChild(fields);
    return shell.step;
  };

  CommercialRfpComposer.prototype.buildStepFive = function buildStepFive() {
    var labels = this.labels;
    var shell = this.buildStepShell(5, labels.reviewTitle || "Review consent and send");
    var consents = node("div", "nl-rfp-consents");
    ["privacy", "terms", "marketing"].forEach(function (name) {
      var label = node("label", "nl-rfp-consent");
      var input = document.createElement("input");
      input.type = "checkbox";
      input.name = name;
      input.required = name !== "marketing";
      label.appendChild(input);
      label.appendChild(
        node(
          "span",
          "",
          labels[name + "Consent"] ||
            (name === "marketing" ? "Send useful project updates" : "Required consent")
        )
      );
      consents.appendChild(label);
    });
    shell.body.appendChild(consents);
    return shell.step;
  };

  CommercialRfpComposer.prototype.render = function render() {
    var self = this;
    var root = node("section", "nl-rfp");
    root.lang = this.locale;
    root.dir = this.locale === "he" || this.locale === "ar" ? "rtl" : "ltr";
    root.dataset.rfpStep = "1";
    root.appendChild(this.buildContext());

    var form = node("form", "nl-rfp-form");
    form.noValidate = false;
    var progress = node("p", "nl-rfp-progress");
    setAttribute(progress, "aria-live", "polite");
    form.appendChild(progress);
    form.appendChild(this.buildStepOne());
    form.appendChild(this.buildStepTwo());
    form.appendChild(this.buildStepThree());
    form.appendChild(this.buildStepFour());
    form.appendChild(this.buildStepFive());

    var feedback = node("div", "nl-rfp-feedback");
    feedback.hidden = true;
    var message = node("p", "nl-rfp-message");
    setAttribute(message, "role", "status");
    setAttribute(message, "aria-live", "polite");
    setAttribute(message, "aria-atomic", "true");
    var recovery = actionButton("", "recover", false);
    recovery.className = "nl-rfp-recovery";
    recovery.hidden = true;
    feedback.appendChild(message);
    feedback.appendChild(recovery);
    form.appendChild(feedback);
    root.appendChild(form);

    this.root = root;
    this.form = form;
    this.messageNode = message;
    this.feedbackNode = feedback;
    this.recoveryButton = recovery;
    root.__nlRfpComposer = this;
    root.__nlToolDestroy = function destroyRfpTool() { self.destroy(); };

    this.boundClick = function onClick(event) {
      var action = event.target && typeof event.target.closest === "function"
        ? event.target.closest("[data-rfp-action]")
        : null;
      if (!action) return;
      var kind = action.dataset.rfpAction;
      if (kind === "next") self.nextStep();
      if (kind === "back") self.showStep(self.step - 1);
      if (kind === "recover") self.recover();
    };
    this.boundSubmit = function onSubmit(event) {
      event.preventDefault();
      self.submit();
    };
    this.boundEdit = function onEdit() { self.observeIntentEdit(); };
    form.addEventListener("click", this.boundClick);
    form.addEventListener("submit", this.boundSubmit);
    form.addEventListener("input", this.boundEdit);
    form.addEventListener("change", this.boundEdit);
    this.attachVisualViewport();
    this.showStep(1, { focus: false });
    return root;
  };

  CommercialRfpComposer.prototype.attachVisualViewport = function attachVisualViewport() {
    var self = this;
    if (!this.viewport || typeof this.viewport.addEventListener !== "function") return;
    this.boundViewport = function onViewportChange() { self.syncVisualViewport(); };
    this.viewport.addEventListener("resize", this.boundViewport);
    this.viewport.addEventListener("scroll", this.boundViewport);
    this.syncVisualViewport();
  };

  CommercialRfpComposer.prototype.syncVisualViewport = function syncVisualViewport() {
    if (!this.root || !this.viewport) return;
    var height = Math.max(220, Math.floor(Number(this.viewport.height) || 0));
    if (this.root.style && typeof this.root.style.setProperty === "function") {
      this.root.style.setProperty("--nl-rfp-visual-height", height + "px");
    }
    var baseline = this.initialViewportHeight || height;
    this.root.dataset.keyboard = height < baseline * 0.78 ? "open" : "closed";
  };

  CommercialRfpComposer.prototype.updateProgress = function updateProgress() {
    if (!this.form) return;
    var progress = this.form.querySelector(".nl-rfp-progress");
    if (!progress) return;
    progress.textContent = replaceTokens(
      this.labels.stepProgress || "Step {current} of {total}",
      { current: this.step, total: TOTAL_STEPS }
    );
  };

  CommercialRfpComposer.prototype.focusElement = function focusElement(element) {
    if (element && typeof element.focus === "function") {
      try { element.focus({ preventScroll: true }); } catch (error) { element.focus(); }
    }
  };

  CommercialRfpComposer.prototype.showStep = function showStep(step, options) {
    options = options || {};
    if (!this.form || step < 1 || step > TOTAL_STEPS) return;
    this.step = step;
    if (this.root) this.root.dataset.rfpStep = str(step);
    var active = null;
    Array.prototype.forEach.call(this.form.querySelectorAll("[data-rfp-step]"), function (section) {
      var shown = Number(section.dataset.rfpStep) === step;
      section.hidden = !shown;
      setAttribute(section, "aria-hidden", shown ? "false" : "true");
      if (shown) active = section;
    });
    this.updateProgress();
    if (!options.keepMessage) this.message("");
    if (options.focus !== false && active) {
      this.focusElement(options.focusElement || active.querySelector("h3"));
    }
  };

  CommercialRfpComposer.prototype.validateVisibleControls = function validateVisibleControls(step) {
    var section = this.form.querySelector('[data-rfp-step="' + step + '"]');
    if (!section) return false;
    var controls = Array.prototype.slice.call(section.querySelectorAll("input, textarea, select"));
    for (var i = 0; i < controls.length; i += 1) {
      if (typeof controls[i].checkValidity === "function" && !controls[i].checkValidity()) {
        if (typeof controls[i].reportValidity === "function") controls[i].reportValidity();
        this.focusElement(controls[i]);
        return false;
      }
    }
    return true;
  };

  CommercialRfpComposer.prototype.validateChoice = function validateChoice() {
    var questions = checkedValues(this.form, "question_ids");
    var documents = checkedValues(this.form, "document_ids");
    var text = str(this.form.elements.question_text.value).trim();
    if (questions.length || documents.length || text) return true;
    this.message(this.labels.chooseOne || "Choose a question, document, or write a request.", "error");
    return false;
  };

  CommercialRfpComposer.prototype.validateContact = function validateContact() {
    if (!this.validateVisibleControls(3)) return false;
    var elements = this.form.elements;
    if (str(elements.email.value).trim() || str(elements.phone.value).trim()) return true;
    this.message(this.labels.contactRequired || "Add an email or international phone number.", "error");
    this.focusElement(elements.email);
    return false;
  };

  CommercialRfpComposer.prototype.nextStep = function nextStep() {
    if (this.step === 2 && !this.validateChoice()) return;
    if (this.step === 3 && !this.validateContact()) return;
    if (!this.validateVisibleControls(this.step)) return;
    this.showStep(this.step + 1);
  };

  CommercialRfpComposer.prototype.payload = function payload() {
    var elements = this.form.elements;
    var request = {
      schema_version: "1.0.0",
      environment: this.requestConfig.environment,
      project_id: this.context.projectId,
      project_contract_id: this.context.projectContractId,
      asset: {
        building_id: this.context.buildingId,
        tower_id: this.context.towerId,
        floor_id: this.context.floorId,
        suite_id: this.context.suiteId
      },
      locale: this.locale,
      company: {
        name: str(elements.company_name.value).trim(),
        registration_country: "",
        website: "",
        size_band: ""
      },
      contact: {
        name: str(elements.contact_name.value).trim(),
        role: "",
        email: str(elements.email.value).trim(),
        phone: str(elements.phone.value).trim(),
        preferred_channel: elements.email.value ? "email" : "phone"
      },
      requirements: {
        headcount: elements.headcount.value ? Number(elements.headcount.value) : null,
        target_move_in: str(elements.target_move_in.value) || null,
        lease_term_months: null,
        area_min_sqm: null,
        area_max_sqm: null,
        budget_monthly: null,
        budget_currency: "",
        attendance_ratio_pct: null,
        special_uses: []
      },
      question_ids: checkedValues(this.form, "question_ids"),
      document_ids: checkedValues(this.form, "document_ids"),
      question_text: str(elements.question_text.value).trim(),
      consent: {
        privacy: elements.privacy.checked === true,
        terms: elements.terms.checked === true,
        marketing: elements.marketing.checked === true,
        text_version: this.consentVersion
      },
      page_url: window.location ? str(window.location.href).split("#")[0] : "",
      website_confirm: ""
    };
    if (this.requestConfig.environment === "test") {
      request.sandbox_post_id = this.requestConfig.sandboxPostId;
    }
    return request;
  };

  CommercialRfpComposer.prototype.message = function message(text, state) {
    if (!this.messageNode && this.form) this.messageNode = this.form.querySelector(".nl-rfp-message");
    if (!this.messageNode) return;
    this.messageNode.textContent = str(text);
    this.messageNode.dataset.state = state || "";
    if (this.feedbackNode) {
      this.feedbackNode.hidden = !str(text) && (!this.recoveryButton || this.recoveryButton.hidden);
    }
  };

  CommercialRfpComposer.prototype.hideRecovery = function hideRecovery() {
    if (this.recoveryButton) {
      this.recoveryButton.hidden = true;
      this.recoveryButton.textContent = "";
      this.recoveryButton.dataset.recoveryAction = "";
    }
    if (this.feedbackNode) this.feedbackNode.hidden = !this.messageNode || !this.messageNode.textContent;
  };

  CommercialRfpComposer.prototype.showRecovery = function showRecovery(action, label, focus) {
    if (!this.recoveryButton) return;
    this.recoveryButton.hidden = false;
    this.recoveryButton.dataset.recoveryAction = action;
    this.recoveryButton.textContent = str(label);
    if (this.feedbackNode) this.feedbackNode.hidden = false;
    if (focus !== false) this.focusElement(this.recoveryButton);
  };

  CommercialRfpComposer.prototype.observeIntentEdit = function observeIntentEdit() {
    if (!this.frozenRequest || this.submitting || !this.form) return;
    var changed = JSON.stringify(this.payload()) !== this.frozenRequest.body;
    this.intentChanged = changed;
    if (!changed) {
      this.hideRecovery();
      this.message(this.labels.retryPreserved || "Nothing was cleared. Retry the unchanged request.", "info");
      return;
    }
    this.message(
      this.labels.intentChanged || "Your edits are preserved. Confirm them as a new request before sending.",
      "error"
    );
    this.showRecovery("new_intent", this.labels.useChangesAsNewIntent || "Use my edits as a new request", false);
  };

  CommercialRfpComposer.prototype.beginNewIntent = function beginNewIntent() {
    if (this.submitting) return false;
    this.key = "";
    this.frozenRequest = null;
    this.intentChanged = false;
    this.lastFailure = null;
    this.hideRecovery();
    this.message(this.labels.newIntentReady || "Your fields are preserved. The next send will use a new request key.", "info");
    return true;
  };

  CommercialRfpComposer.prototype.freezeRequest = function freezeRequest() {
    var body = JSON.stringify(this.payload());
    var key = idempotencyKey();
    this.key = key;
    this.frozenRequest = Object.freeze({ key: key, body: body });
    this.intentChanged = false;
    return this.frozenRequest;
  };

  CommercialRfpComposer.prototype.setBusy = function setBusy(busy) {
    if (!this.form) return;
    Array.prototype.forEach.call(
      this.form.querySelectorAll("button, input, textarea, select"),
      function (control) {
        if (busy) {
          control.dataset.rfpWasDisabled = control.disabled ? "1" : "0";
          control.disabled = true;
        } else if (control.dataset.rfpWasDisabled != null) {
          control.disabled = control.dataset.rfpWasDisabled === "1";
          delete control.dataset.rfpWasDisabled;
        }
      }
    );
  };

  CommercialRfpComposer.prototype.failureMessage = function failureMessage(failure) {
    var labels = this.labels;
    var errors = labels.rfpErrors || {};
    var text = errors[failure.code] || errors.network || labels.retryPreserved || "Nothing was cleared. Retry the unchanged request.";
    if (failure.code === "rate_limited" && failure.retryAfter) {
      text = replaceTokens(errors.rate_limited_wait || text, { seconds: failure.retryAfter });
    }
    return text;
  };

  CommercialRfpComposer.prototype.presentFailure = function presentFailure(failure) {
    this.lastFailure = failure;
    this.message(this.failureMessage(failure), "error");
    var actions = this.labels.rfpRecoveryActions || {};
    if (failure.code === "consent_expired") {
      this.showStep(5, { keepMessage: true, focus: false });
      this.showRecovery("review_consent", actions.review_consent || "Review updated consent");
      return;
    }
    if (failure.code === "invalid_field") {
      var fieldName = failure.field || "contact_name";
      this.showStep(stepForField(fieldName), { keepMessage: true, focus: false });
      this.showRecovery("fix_field", actions.fix_field || "Review this field");
      return;
    }
    if (failure.code === "conflict") {
      this.showRecovery("new_intent", actions.new_intent || "Start a new request intent");
      return;
    }
    this.showRecovery("retry", actions.retry || "Retry the unchanged request");
  };

  CommercialRfpComposer.prototype.recover = function recover() {
    var self = this;
    var action = this.recoveryButton && this.recoveryButton.dataset.recoveryAction;
    if (action === "retry") return this.submit();
    if (action === "new_intent") {
      this.beginNewIntent();
      return Promise.resolve(null);
    }
    if (action === "fix_field") {
      var name = this.lastFailure && this.lastFailure.field ? this.lastFailure.field : "contact_name";
      var control = this.form.elements[name];
      this.hideRecovery();
      this.message("");
      this.focusElement(control);
      return Promise.resolve(null);
    }
    if (action === "review_consent") {
      var supplied = this.lastFailure && this.lastFailure.consentVersion;
      var refresh = supplied
        ? Promise.resolve(supplied)
        : this.refreshConsentVersion
          ? Promise.resolve().then(function () { return self.refreshConsentVersion(); })
          : Promise.reject(new Error("consent_refresh_unavailable"));
      return refresh.then(function (version) {
        var nextVersion = canonicalId(version, "refreshed consent version");
        self.beginNewIntent();
        self.consentVersion = nextVersion;
        self.form.elements.privacy.checked = false;
        self.form.elements.terms.checked = false;
        self.showStep(5, { keepMessage: true, focus: false });
        self.message(self.labels.consentUpdated || "Consent was updated. Review and accept it before sending.", "info");
        self.focusElement(self.form.elements.privacy);
        return nextVersion;
      }).catch(function () {
        self.hideRecovery();
        self.message(
          (self.labels.rfpErrors && self.labels.rfpErrors.consent_refresh_unavailable) ||
            "The updated consent could not be loaded. Your fields remain here.",
          "error"
        );
        self.focusElement(self.form.elements.privacy);
        return null;
      });
    }
    return Promise.resolve(null);
  };

  CommercialRfpComposer.prototype.submit = function submit() {
    var self = this;
    if (this.submitting || !this.form) return Promise.resolve(null);
    if (!this.validateChoice() || !this.validateContact() || !this.validateVisibleControls(5)) {
      return Promise.resolve(null);
    }
    if (this.frozenRequest && JSON.stringify(this.payload()) !== this.frozenRequest.body) {
      this.intentChanged = true;
      this.message(
        this.labels.intentChanged || "Your edits are preserved. Confirm them as a new request before sending.",
        "error"
      );
      this.showRecovery("new_intent", this.labels.useChangesAsNewIntent || "Use my edits as a new request");
      return Promise.resolve(null);
    }
    var request;
    try {
      request = this.frozenRequest || this.freezeRequest();
    } catch (error) {
      this.message(this.labels.secureRetryUnavailable || "Secure submission is unavailable.", "error");
      return Promise.resolve(null);
    }
    this.submitting = true;
    this.abortController = typeof window.AbortController === "function" ? new window.AbortController() : null;
    this.setBusy(true);
    this.hideRecovery();
    this.message(this.labels.sending || "Sending your selected questions...", "pending");
    var requestOptions = {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "Idempotency-Key": request.key
      },
      body: request.body
    };
    if (this.requestConfig.environment === "test") {
      requestOptions.headers["X-Nadlan-Sandbox-Nonce"] = this.requestConfig.sandboxNonce;
    }
    if (this.abortController) requestOptions.signal = this.abortController.signal;
    return this.fetchImpl(this.endpoint, requestOptions)
      .then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (body) {
          if (!response.ok) {
            throw {
              __nlRfpFailure: true,
              code: safeServerCode(Number(response.status), body),
              status: Number(response.status) || 0,
              field: safeFieldName(body),
              retryAfter: safeRetryAfter(response, body),
              consentVersion: canonicalConsentVersion(body)
            };
          }
          if (!validSafeSuccessResponse(body, self.requestConfig.environment)) {
            throw { __nlRfpFailure: true, code: "route_unavailable", status: 0 };
          }
          return body;
        });
      })
      .then(function (body) {
        var frozenPayload = JSON.parse(request.body);
        self.renderConfirmation(body);
        self.onSafeAnalytics({
          event: "commercial_rfp_received",
          project_id: self.context.projectId,
          has_building: Boolean(self.context.buildingId),
          has_tower: Boolean(self.context.towerId),
          has_floor: Boolean(self.context.floorId),
          has_suite: Boolean(self.context.suiteId),
          question_count: frozenPayload.question_ids.length,
          document_count: frozenPayload.document_ids.length,
          locale: self.locale
        });
        return body;
      })
      .catch(function (error) {
        if (error && error.name === "AbortError") return null;
        var failure = error && error.__nlRfpFailure
          ? error
          : { __nlRfpFailure: true, code: "network", status: 0, field: "", retryAfter: null };
        self.submitting = false;
        self.setBusy(false);
        self.presentFailure(failure);
        return null;
      })
      .finally(function () {
        self.submitting = false;
        self.setBusy(false);
      });
  };

  function validSafeSuccessResponse(body, environment) {
    if (!isObject(body) || body.accepted !== true) return false;
    var caseId = str(body.case_id).trim();
    var routeKind = str(body.route_kind);
    var deliveryState = str(body.delivery_state);
    var slaHours = body.sla_hours;
    if (typeof slaHours !== "number" || !Number.isInteger(slaHours)) return false;

    if (environment === "test") {
      return (
        /^TEST-[A-F0-9]{20}$/.test(caseId) &&
        body.environment === "test" &&
        routeKind === "test_sink" &&
        deliveryState === "test_sink" &&
        body.route_status === "test_sink" &&
        slaHours === 0
      );
    }

    if (environment !== "production") return false;
    var testOnlyFields = ["environment", "route_status", "recipient_label"];
    if (testOnlyFields.some(function (field) {
      return Object.prototype.hasOwnProperty.call(body, field);
    })) {
      return false;
    }
    return (
      /^NLC-[A-F0-9]{24}$/.test(caseId) &&
      ["project_team", "commercial_desk"].indexOf(routeKind) >= 0 &&
      ["routed", "processing"].indexOf(deliveryState) >= 0 &&
      slaHours >= 1 &&
      slaHours <= 168
    );
  }

  function canonicalConsentVersion(body) {
    var value = str(
      isObject(body) &&
      (body.current_consent_version || (isObject(body.data) && body.data.current_consent_version))
    ).trim();
    return value && value.length <= 180 && !/[\u0000-\u001f\u007f]/.test(value) ? value : "";
  }

  CommercialRfpComposer.prototype.renderConfirmation = function renderConfirmation(body) {
    var labels = this.labels;
    this.form.replaceChildren();
    var confirmation = node("section", "nl-rfp-confirmation");
    confirmation.tabIndex = -1;
    confirmation.appendChild(node("h3", "", labels.received || "Your request reached the commercial team"));
    confirmation.appendChild(node("p", "", (labels.caseId || "Case") + ": " + str(body.case_id)));
    confirmation.appendChild(
      node(
        "p",
        "",
        (labels.recipient || "Responsible recipient") + ": " +
          (body.route_kind === "test_sink"
            ? labels.sandboxTestSink || "Sandbox test sink - no message delivered"
            : labels.routeKinds && labels.routeKinds[body.route_kind]
            ? labels.routeKinds[body.route_kind]
            : labels.commercialTeam || "Commercial response team")
      )
    );
    confirmation.appendChild(
      node(
        "p",
        "",
        (labels.sla || "Response target") + ": " + str(body.sla_hours) + " " +
          (labels.hours || "hours")
      )
    );
    confirmation.appendChild(
      node("small", "", labels.safeConfirmation || "The confirmation does not expose a private mailbox or staff identity.")
    );
    this.form.appendChild(confirmation);
    this.focusElement(confirmation);
  };

  CommercialRfpComposer.prototype.destroy = function destroy() {
    if (this.abortController) this.abortController.abort();
    if (this.viewport && this.boundViewport && typeof this.viewport.removeEventListener === "function") {
      this.viewport.removeEventListener("resize", this.boundViewport);
      this.viewport.removeEventListener("scroll", this.boundViewport);
    }
    if (this.form && typeof this.form.removeEventListener === "function") {
      this.form.removeEventListener("click", this.boundClick);
      this.form.removeEventListener("submit", this.boundSubmit);
      this.form.removeEventListener("input", this.boundEdit);
      this.form.removeEventListener("change", this.boundEdit);
    }
    this.abortController = null;
    this.submitting = false;
    if (this.root) this.root.__nlRfpComposer = null;
  };

  function createNode(options) {
    var composer = new CommercialRfpComposer(options);
    return composer.render();
  }

  window.NadlanCommercialRfpComposer = {
    CommercialRfpComposer: CommercialRfpComposer,
    createNode: createNode,
    questionIds: QUESTION_IDS.slice(),
    documentIds: DOCUMENT_IDS.slice(),
    createIdempotencyKey: idempotencyKey,
    validateEndpoint: validateEndpoint,
    totalSteps: TOTAL_STEPS
  };
})(window, document);
