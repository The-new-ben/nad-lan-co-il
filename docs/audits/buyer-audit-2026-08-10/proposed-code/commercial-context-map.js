/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Evidence-aware context map using the Mapbox GL runtime already loaded by Nadlan.
 * It adds no library. If Mapbox is unavailable, the same evidence remains readable
 * as cards rather than failing to an empty black rectangle.
 */
(function commercialContextMapModule(window, document) {
  "use strict";

  var MODES = ["commute", "daily_life", "business", "market", "risk"];
  var OPERATING_STATES = [
    "operating",
    "under_construction",
    "planned",
    "temporarily_closed",
    "closed",
    "unknown"
  ];
  var STORED_OPERATING_STATES = OPERATING_STATES.slice(0, 5);
  var ACTION_EVENTS = {
    openSourceDocument: "nadlan:commercial-context-open-source-document",
    requestField: "nadlan:commercial-context-request-field"
  };
  var ROUTE_STYLES = {
    operating: { color: "#5fd19b", dash: null },
    planned: { color: "#8fc9ff", dash: [3, 2] },
    under_construction: { color: "#e4bd68", dash: [1, 1] },
    temporarily_closed: { color: "#f09a62", dash: [4, 2] },
    closed: { color: "#89918d", dash: [1, 3] },
    unknown: { color: "#c4cbc7", dash: [0.5, 2.5] }
  };
  var MARKER_GLYPHS = {
    operating: "✓",
    planned: "P",
    under_construction: "!",
    temporarily_closed: "‖",
    closed: "×",
    unknown: "?"
  };

  function str(value) {
    return value == null ? "" : String(value);
  }

  function escapeHtml(value) {
    return str(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function asArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function finite(value) {
    var number = Number(value);
    return Number.isFinite(number) ? number : null;
  }

  function firstPresent(primary, secondary) {
    return primary != null ? primary : secondary;
  }

  function nonNegativeFinite(value) {
    var number = finite(value);
    return number != null && number >= 0 ? number : null;
  }

  function boundedMapLoadTimeout(value) {
    var duration = finite(value);
    if (duration == null) return 8000;
    return Math.max(1000, Math.min(15000, Math.floor(duration)));
  }

  /**
   * `unknown` is a presentation state, not a stored business claim. The only
   * legacy compatibility mapping is the dictionary's former `open` value.
   * Concepts, proposals and all other missing/invalid values fail closed.
   */
  function normalizeOperatingState(value) {
    var normalized = str(value).trim().toLowerCase();
    if (normalized === "open") return "operating";
    return OPERATING_STATES.indexOf(normalized) >= 0 ? normalized : "unknown";
  }

  function evidenceValueOrRaw(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) return value;
    if (
      value.__nlCommercialEvidence !== true &&
      !Object.prototype.hasOwnProperty.call(value, "state") &&
      !Object.prototype.hasOwnProperty.call(value, "value")
    ) {
      return value;
    }
    var normalized = normalizeEvidence(value);
    return normalized.state === "verified" || normalized.state === "source_estimate"
      ? normalized.value
      : null;
  }

  function normalizedText(value) {
    return str(evidenceValueOrRaw(value)).trim();
  }

  function firstText() {
    for (var index = 0; index < arguments.length; index += 1) {
      var value = normalizedText(arguments[index]);
      if (value) return value;
    }
    return "";
  }

  function normalizeExpectedTiming(raw) {
    raw = raw && typeof raw === "object" ? raw : {};
    var date = firstText(
      raw.expected_date,
      raw.expectedDate,
      raw.expected_opening_date,
      raw.expectedOpeningDate,
      raw.expected_reopening_date,
      raw.expectedReopeningDate
    );
    var rangeRaw = firstPresent(
      firstPresent(raw.expected_range, raw.expectedRange),
      firstPresent(raw.expected_timing_range, raw.expectedTimingRange)
    );
    rangeRaw = evidenceValueOrRaw(rangeRaw);
    var range = "";
    if (rangeRaw && typeof rangeRaw === "object" && !Array.isArray(rangeRaw)) {
      range = firstText(rangeRaw.label);
      if (!range) {
        var from = firstText(rangeRaw.from, rangeRaw.start, rangeRaw.min);
        var to = firstText(rangeRaw.to, rangeRaw.end, rangeRaw.max);
        range = [from, to].filter(Boolean).join(" – ");
      }
    } else {
      range = normalizedText(rangeRaw);
    }
    return { date: date, range: range };
  }

  function safeExternalUrl(value) {
    var candidate = str(value).trim();
    return /^https?:\/\/[^\s]+$/i.test(candidate) ? candidate : "";
  }

  function recordsPerPageForViewport(width, height) {
    var viewportWidth = finite(width);
    var viewportHeight = finite(height);
    if (
      viewportWidth != null &&
      viewportHeight != null &&
      viewportWidth > viewportHeight &&
      viewportHeight <= 600
    ) {
      return 1;
    }
    return viewportWidth != null && viewportWidth <= 900 ? 2 : 4;
  }

  function validCoordinates(value) {
    if (!Array.isArray(value) || value.length < 2) return null;
    var lng = finite(value[0]);
    var lat = finite(value[1]);
    if (lng == null || lat == null || Math.abs(lng) > 180 || Math.abs(lat) > 90) return null;
    if (lng === 0 && lat === 0) return null;
    return [lng, lat];
  }

  function contractAdapter() {
    if (
      !window.NadlanCommercialContractAdapter ||
      typeof window.NadlanCommercialContractAdapter.normalizeEvidenceEnvelope !== "function"
    ) {
      throw new Error(
        "Load commercial-decision-surface.js before commercial-context-map.js."
      );
    }
    return window.NadlanCommercialContractAdapter;
  }

  function normalizeEvidence(raw) {
    var item = contractAdapter().normalizeEvidenceEnvelope(raw);
    var sources = asArray(item.sources);
    var locatedSource = sources.find(function (source) {
      return Boolean(
        source &&
        source.label &&
        (safeExternalUrl(source.uri) || source.documentId || source.document_id)
      );
    }) || null;
    return {
      state: item.state,
      value: item.value,
      sources: sources,
      observations: asArray(item.observations),
      sourceLabel: item.sourceLabel || (locatedSource && locatedSource.label) || "",
      sourceUrl: safeExternalUrl(item.sourceUrl) ||
        (locatedSource && safeExternalUrl(locatedSource.uri)) || "",
      sourceDocumentId: locatedSource &&
        str(locatedSource.documentId || locatedSource.document_id).trim(),
      observedAt: item.verifiedAt || item.effectiveAt,
      verifiedAt: item.verifiedAt,
      effectiveAt: item.effectiveAt,
      expiresAt: item.expiresAt,
      ownerLabel: item.ownerLabel,
      requiredDocumentIds: item.requiredDocumentIds,
      confidence: item.confidence,
      caveat: item.caveat,
      reason: item.reason,
      note: item.note,
      scope: item.scope,
      applicability: item.applicability,
      conflictIds: item.conflictIds,
      issues: item.issues
    };
  }

  /**
   * A context envelope governs the complete place/route record, including its
   * name, coordinates, geometry, distances and times. Verified records may be
   * claimed. Source estimates may be claimed only when the producer supplies
   * an explicit scope and the canonical envelope retained a located source.
   * Unknown, contradictory, expired or malformed evidence never reaches the
   * cards or map.
   */
  function isMaterialClaimAllowed(evidence, scope) {
    if (!evidence) return false;
    var hasLocatedSource = evidence.sources.some(function (source) {
      return Boolean(
        source &&
        source.label &&
        (safeExternalUrl(source.uri) || source.documentId || source.document_id)
      );
    });
    if (evidence.state === "verified") return hasLocatedSource;
    if (evidence.state !== "source_estimate" || !str(scope).trim()) return false;
    return hasLocatedSource;
  }

  function recordOperatingState(rawValue) {
    if (rawValue && typeof rawValue === "object" && !Array.isArray(rawValue)) {
      var evidence = normalizeEvidence(rawValue);
      if (evidence.state !== "verified" && evidence.state !== "source_estimate") {
        return "unknown";
      }
      return normalizeOperatingState(evidence.value);
    }
    return normalizeOperatingState(rawValue);
  }

  function recordCaveat(raw, evidence, labels) {
    var explicit = firstText(
      raw && raw.caveat,
      evidence && evidence.caveat,
      evidence && evidence.reason,
      evidence && evidence.note
    );
    if (explicit) return explicit;
    if (evidence && evidence.state === "source_estimate") {
      return labels.estimateCaveat ||
        "Source estimate only; confirm current conditions before relying on it.";
    }
    return labels.evidenceCaveat ||
      "Evidence applies to the stated scope and date; confirm current conditions before relying on it.";
  }

  function normalizePoint(raw, index) {
    raw = raw && typeof raw === "object" ? raw : {};
    var evidence = normalizeEvidence(raw.evidence);
    var evidenceScope = str(raw.evidence_scope || raw.evidenceScope || evidence.scope).trim();
    if (!isMaterialClaimAllowed(evidence, evidenceScope)) return null;
    var coordinates = validCoordinates(raw.coordinates);
    if (!coordinates) return null;
    var mode = str(raw.mode).toLowerCase();
    if (MODES.indexOf(mode) < 0) return null;
    var name = str(raw.name).trim();
    if (!name) return null;
    var minutesMin = nonNegativeFinite(
      firstPresent(raw.minutes_min, raw.minutes && raw.minutes.min)
    );
    var minutesMax = nonNegativeFinite(
      firstPresent(raw.minutes_max, raw.minutes && raw.minutes.max)
    );
    if (minutesMin != null && minutesMax != null && minutesMax < minutesMin) {
      minutesMin = null;
      minutesMax = null;
    }
    var timing = normalizeExpectedTiming(raw);
    var operatingState = recordOperatingState(
      firstPresent(raw.operating_state, raw.operatingState)
    );
    return {
      id: str(raw.id || "context-" + index),
      mode: mode,
      category: str(raw.category || mode),
      categoryLabel: firstText(raw.category_label, raw.categoryLabel),
      name: name,
      coordinates: coordinates,
      operatingState: operatingState,
      stage: firstText(raw.stage, raw.planning_stage, raw.planningStage),
      expectedDate: timing.date,
      expectedRange: timing.range,
      straightLineM: nonNegativeFinite(firstPresent(raw.straight_line_m, raw.straightLineM)),
      networkDistanceM: nonNegativeFinite(firstPresent(raw.network_distance_m, raw.networkDistanceM)),
      minutesMin: minutesMin,
      minutesMax: minutesMax,
      modeOfTravel: str(raw.travel_mode || raw.modeOfTravel),
      note: str(raw.note),
      caveat: firstText(raw.caveat, evidence.caveat, evidence.reason, evidence.note),
      evidenceScope: evidenceScope,
      evidence: evidence
    };
  }

  function normalizeRoute(raw, index) {
    raw = raw && typeof raw === "object" ? raw : {};
    var evidence = normalizeEvidence(raw.evidence);
    var evidenceScope = str(raw.evidence_scope || raw.evidenceScope || evidence.scope).trim();
    if (!isMaterialClaimAllowed(evidence, evidenceScope)) return null;
    var rawGeometry = asArray(raw.geometry);
    var geometry = rawGeometry.map(validCoordinates);
    if (
      geometry.length < 2 ||
      geometry.some(function (coordinates) { return !coordinates; })
    ) {
      return null;
    }
    var mode = str(raw.mode).toLowerCase();
    if (MODES.indexOf(mode) < 0) return null;
    var label = str(raw.label).trim();
    if (!label) return null;
    var minutesMin = nonNegativeFinite(
      firstPresent(raw.minutes_min, raw.minutes && raw.minutes.min)
    );
    var minutesMax = nonNegativeFinite(
      firstPresent(raw.minutes_max, raw.minutes && raw.minutes.max)
    );
    if (minutesMin != null && minutesMax != null && minutesMax < minutesMin) {
      minutesMin = null;
      minutesMax = null;
    }
    var transfers = nonNegativeFinite(raw.transfers);
    if (transfers != null && Math.floor(transfers) !== transfers) transfers = null;
    var timing = normalizeExpectedTiming(raw);
    var operatingState = recordOperatingState(
      firstPresent(raw.operating_state, raw.operatingState)
    );
    return {
      id: str(raw.id || "route-" + index),
      mode: mode,
      label: label,
      travelMode: str(raw.travel_mode || raw.travelMode || "transit"),
      operatingState: operatingState,
      stage: firstText(raw.stage, raw.planning_stage, raw.planningStage),
      expectedDate: timing.date,
      expectedRange: timing.range,
      departureWindow: str(raw.departure_window || raw.departureWindow),
      minutesMin: minutesMin,
      minutesMax: minutesMax,
      transfers: transfers,
      geometry: geometry,
      caveat: firstText(raw.caveat, evidence.caveat, evidence.reason, evidence.note),
      evidenceScope: evidenceScope,
      evidence: evidence
    };
  }

  function distanceLabel(point, labels) {
    var parts = [];
    var metres = labels.metresShort || "m";
    var minutes = labels.minutesShort || "min";
    if (point.networkDistanceM != null) parts.push(Math.round(point.networkDistanceM) + " " + metres + " " + (labels.network || "route"));
    else if (point.straightLineM != null) parts.push("≈" + Math.round(point.straightLineM) + " " + metres + " " + (labels.straightLine || "straight line"));
    if (point.minutesMin != null) {
      parts.push(
        point.minutesMax != null && point.minutesMax !== point.minutesMin
          ? point.minutesMin + "–" + point.minutesMax + " " + minutes
          : point.minutesMin + " " + minutes
      );
    }
    return parts.join(" · ");
  }

  function evidenceLabel(item, labels, scope) {
    var parts = [(labels.states && labels.states[item.state]) || item.state];
    if (item.state === "source_estimate" && scope) parts.push(scope);
    if (item.sourceLabel) parts.push(item.sourceLabel);
    if (item.observedAt) parts.push(item.observedAt);
    return parts.join(" · ");
  }

  function operatingStateLabel(state, labels) {
    var dictionary = labels.operatingStates || labels.operating_states || {};
    return dictionary[state] || state.replace(/_/g, " ");
  }

  function categoryLabel(point, labels) {
    var dictionary = labels.categories || {};
    return point.categoryLabel || dictionary[point.category] || point.category;
  }

  function travelModeLabel(mode, labels) {
    var dictionary = labels.travelModes || labels.travel_modes || {};
    return dictionary[mode] || mode;
  }

  function operatingStateBadge(state, labels) {
    var visible = operatingStateLabel(state, labels);
    var srPrefix = labels.operatingState || "Operating state";
    return (
      '<span class="nl-ccm-state-badge" data-operating-state="' + escapeHtml(state) + '">' +
      '<span class="nl-ccm-state-badge__visual" aria-hidden="true">' + escapeHtml(visible) + "</span>" +
      '<span class="nl-ccm-sr-only">' + escapeHtml(srPrefix + ": " + visible + ".") + "</span></span>"
    );
  }

  function expectedTimingLabel(record, labels) {
    if (
      ["planned", "under_construction", "temporarily_closed"].indexOf(record.operatingState) < 0
    ) {
      return "";
    }
    var timing = record.expectedRange || record.expectedDate;
    if (!timing) {
      return labels.expectedUnknown || "Expected timing not supplied";
    }
    return (labels.expected || "Expected") + ": " + timing;
  }

  function qualifyTravelLabel(record, value, labels) {
    if (!value) return "";
    if (record.operatingState === "operating") return value;
    if (
      record.operatingState === "planned" ||
      record.operatingState === "under_construction"
    ) {
      return (labels.projectedTravel || "Projected travel") + ": " + value;
    }
    if (record.operatingState === "temporarily_closed") {
      return (labels.closedServiceTravel || "Reference travel while service is closed") + ": " + value;
    }
    if (record.operatingState === "closed") {
      return (labels.historicalTravel || "Historical/reference travel") + ": " + value;
    }
    return (labels.unknownStateTravel || "Travel applicability not verified") + ": " + value;
  }

  function stateMetadata(record, labels) {
    var values = [];
    if (record.stage) values.push((labels.stage || "Stage") + ": " + record.stage);
    var expected = expectedTimingLabel(record, labels);
    if (expected) values.push(expected);
    if (!values.length) return "";
    return '<p class="nl-ccm-state-meta">' + escapeHtml(values.join(" · ")) + "</p>";
  }

  function sourceControl(evidence, labels) {
    if (evidence.sourceUrl) {
      return (
        '<a class="nl-ccm-source" href="' + escapeHtml(evidence.sourceUrl) +
        '" target="_blank" rel="noopener noreferrer">' +
        escapeHtml(labels.openSource || "Open source") + "</a>"
      );
    }
    if (evidence.sourceDocumentId) {
      return (
        '<button type="button" class="nl-ccm-source" data-act="open-source-document" data-document-id="' +
        escapeHtml(evidence.sourceDocumentId) + '">' +
        escapeHtml(labels.openSourceRecord || "Open source record") + "</button>"
      );
    }
    return '<span class="nl-ccm-source-missing">' +
      escapeHtml(labels.sourceNotLinked || "Source reference is not linked") + "</span>";
  }

  function evidenceDetails(record, labels) {
    return (
      '<small class="nl-ccm-evidence-label">' +
      escapeHtml(evidenceLabel(record.evidence, labels, record.evidenceScope)) + "</small>" +
      '<p class="nl-ccm-evidence-caveat">' +
      escapeHtml(recordCaveat(record, record.evidence, labels)) + "</p>" +
      sourceControl(record.evidence, labels)
    );
  }

  function modeButton(mode, labels, active) {
    return (
      '<button type="button" data-map-mode="' + escapeHtml(mode) + '" aria-pressed="' + (active ? "true" : "false") + '">' +
      escapeHtml((labels.modes && labels.modes[mode]) || mode.replace(/_/g, " ")) + "</button>"
    );
  }

  function pointCard(point, labels) {
    var travel = qualifyTravelLabel(point, distanceLabel(point, labels), labels);
    return (
      '<article class="nl-ccm-card" data-context-record-id="' + escapeHtml(point.id) + '" data-evidence-state="' +
      escapeHtml(point.evidence.state) + '" data-operating-state="' + escapeHtml(point.operatingState) + '">' +
      '<div class="nl-ccm-record__main"><div class="nl-ccm-card__state">' + operatingStateBadge(point.operatingState, labels) + "</div>" +
      '<button type="button" class="nl-ccm-card__focus" data-context-id="' +
      escapeHtml(point.id) + '"><span class="nl-ccm-card__category">' + escapeHtml(categoryLabel(point, labels)) + "</span>" +
      '<strong>' + escapeHtml(point.name) + "</strong>" +
      '<span>' + escapeHtml(travel || point.note || labels.noRoute || "Route not calculated") + "</span></button>" +
      (point.note && distanceLabel(point, labels) ? '<p class="nl-ccm-card__note">' + escapeHtml(point.note) + "</p>" : "") +
      stateMetadata(point, labels) + "</div>" +
      '<div class="nl-ccm-record__evidence">' + evidenceDetails(point, labels) + "</div>" +
      "</article>"
    );
  }

  function routeCard(route, labels) {
    var minutes = labels.minutesShort || "min";
    var durationValue = route.minutesMin == null
      ? labels.notCalculated || "Not calculated"
      : route.minutesMax != null && route.minutesMax !== route.minutesMin
      ? route.minutesMin + "–" + route.minutesMax + " " + minutes
      : route.minutesMin + " " + minutes;
    var duration = route.minutesMin == null
      ? durationValue
      : qualifyTravelLabel(route, durationValue, labels);
    return (
      '<article class="nl-ccm-route" data-route-id="' + escapeHtml(route.id) + '" data-evidence-state="' +
      escapeHtml(route.evidence.state) + '" data-operating-state="' + escapeHtml(route.operatingState) + '">' +
      '<div class="nl-ccm-record__main"><div class="nl-ccm-route__state">' + operatingStateBadge(route.operatingState, labels) + "</div>" +
      '<div class="nl-ccm-route__head"><strong>' +
      escapeHtml(route.label) + "</strong><span>" + escapeHtml(travelModeLabel(route.travelMode, labels)) + "</span></div>" +
      '<b>' + escapeHtml(duration) + "</b>" +
      '<p>' + escapeHtml([route.departureWindow, route.transfers == null ? "" : route.transfers + " " + (labels.transfers || "transfers")].filter(Boolean).join(" · ")) + "</p>" +
      stateMetadata(route, labels) + "</div>" +
      '<div class="nl-ccm-record__evidence">' + evidenceDetails(route, labels) + "</div></article>"
    );
  }

  function CommercialContextMap(options) {
    options = options || {};
    if (!options.root) throw new Error("root is required");
    this.root = options.root;
    this.labels = options.labels || {};
    this.centerEvidence = normalizeEvidence(options.centerEvidence || options.center_evidence);
    this.centerEvidenceScope = str(
      options.centerEvidenceScope || options.center_evidence_scope
    ).trim();
    this.center = isMaterialClaimAllowed(
      this.centerEvidence,
      this.centerEvidenceScope
    )
      ? validCoordinates(options.center)
      : null;
    this.points = asArray(options.points).map(normalizePoint).filter(Boolean);
    this.routes = asArray(options.routes).map(normalizeRoute).filter(Boolean);
    this.activeMode = MODES.indexOf(options.initialMode) >= 0 ? options.initialMode : "commute";
    this.mapOptions = options.mapOptions || {};
    this.map = null;
    this.mapReady = false;
    this.mapState = "idle";
    this.markers = [];
    this.abortController = null;
    this.mapContainer = null;
    this.mapStatus = null;
    this.mapLoadTimer = null;
    this.mapLoadHandler = null;
    this.mapErrorHandler = null;
    this.pageByMode = Object.create(null);
    this.configuredPageSize = nonNegativeFinite(options.pageSize);
    this.onOpenSourceDocument = typeof options.onOpenSourceDocument === "function"
      ? options.onOpenSourceDocument
      : null;
    this.onRequestField = typeof options.onRequestField === "function"
      ? options.onRequestField
      : null;
    this.mapLoadTimeoutMs = boundedMapLoadTimeout(
      firstPresent(options.mapLoadTimeoutMs, this.mapOptions.loadTimeoutMs)
    );
  }

  CommercialContextMap.prototype.render = function render() {
    this.destroy(false);
    this.abortController = new AbortController();
    this.root.innerHTML =
      '<section class="nl-ccm"><div class="nl-ccm-modes" role="group" aria-label="' +
      escapeHtml(this.labels.modeLabel || "Map mode") + '">' +
      MODES.map(
        function (mode) { return modeButton(mode, this.labels, mode === this.activeMode); }.bind(this)
      ).join("") +
      '</div><p class="nl-ccm-map-status" data-role="map-status" role="status" hidden></p>' +
      '<div class="nl-ccm-layout"><div class="nl-ccm-map" data-role="map" role="region" aria-label="' +
      escapeHtml(this.labels.mapLabel || "Project context map") + '"></div><div class="nl-ccm-results" data-role="results"></div></div>' +
      '<p class="nl-ccm-caveat">' +
      escapeHtml(this.labels.caveat || "Travel times are ranges. Operating and planned transport are shown separately.") +
      "</p></section>";
    this.mapContainer = this.root.querySelector('[data-role="map"]');
    this.mapStatus = this.root.querySelector('[data-role="map-status"]');
    var self = this;
    this.root.addEventListener(
      "click",
      function (event) {
        var sourceDocument = event.target.closest('[data-act="open-source-document"]');
        if (sourceDocument) {
          event.preventDefault();
          event.stopPropagation();
          self.activateContextAction(
            sourceDocument,
            "openSourceDocument",
            {
              documentId: str(sourceDocument.dataset.documentId),
              recordId: self.recordIdForControl(sourceDocument)
            },
            event
          );
          return;
        }
        var requestField = event.target.closest('[data-act="request-field"]');
        if (requestField) {
          event.preventDefault();
          event.stopPropagation();
          self.activateContextAction(
            requestField,
            "requestField",
            { fieldId: str(requestField.dataset.fieldId), mode: self.activeMode },
            event
          );
          return;
        }
        var mode = event.target.closest("[data-map-mode]");
        if (mode) {
          self.setMode(mode.dataset.mapMode);
          return;
        }
        var page = event.target.closest("[data-map-page]");
        if (page) {
          self.setResultPage(Number(page.dataset.mapPage));
          return;
        }
        var card = event.target.closest("[data-context-id]");
        if (card) self.focusPoint(card.dataset.contextId);
      },
      { signal: this.abortController.signal }
    );
    this.renderResults();
    this.initializeMap();
    return this;
  };

  CommercialContextMap.prototype.recordIdForControl = function recordIdForControl(control) {
    if (!control || typeof control.closest !== "function") return "";
    var record = control.closest("[data-context-record-id], [data-route-id]");
    return record
      ? str(record.dataset.contextRecordId || record.dataset.routeId)
      : "";
  };

  /**
   * Integration seam for controls whose behavior belongs to WordPress/the
   * parent decision controller, not this map. An explicit option callback wins.
   * Without one, a named, cancelable CustomEvent bubbles from the activated
   * control. The original click is stopped so a legacy `[data-act]` delegate
   * cannot submit the same request twice.
   */
  CommercialContextMap.prototype.activateContextAction = function activateContextAction(
    control,
    action,
    detail,
    originalEvent
  ) {
    var callback = action === "openSourceDocument"
      ? this.onOpenSourceDocument
      : action === "requestField"
      ? this.onRequestField
      : null;
    var eventName = ACTION_EVENTS[action];
    if (!eventName) return false;
    var payload = Object.assign(
      { action: action, activeMode: this.activeMode },
      detail || {}
    );
    if (callback) {
      callback(payload, originalEvent || null, control, this);
      return true;
    }
    if (!control || typeof control.dispatchEvent !== "function") return false;
    var customEvent = new window.CustomEvent(eventName, {
      bubbles: true,
      cancelable: true,
      detail: payload
    });
    return control.dispatchEvent(customEvent);
  };

  CommercialContextMap.prototype.initializeMap = function initializeMap() {
    var mapboxgl = window.mapboxgl;
    if (!this.center || !mapboxgl || typeof mapboxgl.Map !== "function") {
      this.failMap("unavailable");
      return;
    }
    try {
      this.mapState = "loading";
      this.mapReady = false;
      this.setMapPresentationState("loading");
      this.map = new mapboxgl.Map({
        container: this.mapContainer,
        style: this.mapOptions.style || "mapbox://styles/mapbox/streets-v12",
        center: this.center,
        zoom: Number(this.mapOptions.zoom) || 14,
        attributionControl: true,
        cooperativeGestures: true
      });
      if (
        typeof mapboxgl.NavigationControl === "function" &&
        typeof this.map.addControl === "function"
      ) {
        this.map.addControl(new mapboxgl.NavigationControl({ showCompass: true }), "top-left");
      }
      var self = this;
      this.mapLoadHandler = function onFirstMapLoad() {
        if (self.mapState !== "loading") return;
        self.mapReady = true;
        self.mapState = "ready";
        self.clearMapLoadWatch();
        self.setMapPresentationState("ready");
        try {
          self.refreshMapData();
          // Keep Mapbox attribution and privacy affordances in their native
          // keyboard order. Do not set tabindex=-1 on legal links.
          if (self.mapContainer && typeof self.mapContainer.querySelectorAll === "function") {
            self.mapContainer
              .querySelectorAll(".mapboxgl-ctrl-attrib a, .mapboxgl-ctrl-logo")
              .forEach(function (node) { node.removeAttribute("tabindex"); });
          }
        } catch (error) {
          self.failMap("render_error");
        }
      };
      this.mapErrorHandler = function onFirstMapError() {
        if (self.mapState === "loading") self.failMap("load_error");
      };
      if (typeof this.map.on !== "function" || typeof this.map.off !== "function") {
        throw new Error("Map runtime does not expose removable event listeners.");
      }
      this.map.on("load", this.mapLoadHandler);
      this.map.on("error", this.mapErrorHandler);
      this.mapLoadTimer = window.setTimeout(function onMapLoadTimeout() {
        if (self.mapState === "loading") self.failMap("timeout");
      }, this.mapLoadTimeoutMs);
    } catch (error) {
      this.failMap("initialization_error");
    }
  };

  CommercialContextMap.prototype.clearMapLoadWatch = function clearMapLoadWatch() {
    // Clear owned references before calling third-party code. A Mapbox/runtime
    // teardown hook is allowed to throw, but it must not keep our timer or
    // listener closures alive and must not prevent the other listener cleanup.
    var timer = this.mapLoadTimer;
    var map = this.map;
    var loadHandler = this.mapLoadHandler;
    var errorHandler = this.mapErrorHandler;
    this.mapLoadTimer = null;
    this.mapLoadHandler = null;
    this.mapErrorHandler = null;
    if (timer != null) {
      try { window.clearTimeout(timer); } catch (error) { /* Continue teardown. */ }
    }
    if (map && typeof map.off === "function") {
      if (loadHandler) {
        try { map.off("load", loadHandler); } catch (error) { /* Continue teardown. */ }
      }
      if (errorHandler) {
        try { map.off("error", errorHandler); } catch (error) { /* Continue teardown. */ }
      }
    }
  };

  CommercialContextMap.prototype.setMapPresentationState = function setMapPresentationState(state) {
    var section = this.root && typeof this.root.querySelector === "function"
      ? this.root.querySelector(".nl-ccm")
      : null;
    if (section) section.dataset.mapState = state;
    if (this.mapContainer) {
      this.mapContainer.hidden = state === "unavailable";
      if (state === "unavailable") this.mapContainer.setAttribute("aria-hidden", "true");
      else this.mapContainer.removeAttribute("aria-hidden");
    }
    if (this.mapStatus) {
      this.mapStatus.hidden = state !== "unavailable";
      if (state === "unavailable") {
        this.mapStatus.textContent =
          (this.labels.mapUnavailable || "Map unavailable") + ". " +
          (this.labels.mapFallback || "The sourced route and place cards remain available.");
      } else {
        this.mapStatus.textContent = "";
      }
    }
    this.updateMapAffordances();
  };

  CommercialContextMap.prototype.updateMapAffordances = function updateMapAffordances() {
    if (!this.root || typeof this.root.querySelectorAll !== "function") return;
    var unavailable = this.mapState === "unavailable";
    var unavailableLabel = this.labels.mapFocusUnavailable || "Map focus unavailable";
    this.root.querySelectorAll("[data-context-id]").forEach(function (control) {
      control.disabled = unavailable;
      if (unavailable) {
        control.setAttribute("aria-disabled", "true");
        control.dataset.mapUnavailableLabel = unavailableLabel;
      } else {
        control.removeAttribute("aria-disabled");
        delete control.dataset.mapUnavailableLabel;
      }
    });
  };

  CommercialContextMap.prototype.failMap = function failMap(reason) {
    this.clearMapLoadWatch();
    var failedMap = this.map;
    this.map = null;
    this.mapReady = false;
    this.mapState = "unavailable";
    this.markers.forEach(function (marker) { marker.remove(); });
    this.markers = [];
    if (failedMap && typeof failedMap.remove === "function") {
      try { failedMap.remove(); } catch (error) { /* Proposal fallback remains readable. */ }
    }
    if (this.mapContainer && typeof this.mapContainer.replaceChildren === "function") {
      this.mapContainer.replaceChildren();
    }
    if (this.mapContainer) this.mapContainer.dataset.failureReason = str(reason || "unavailable");
    this.setMapPresentationState("unavailable");
  };

  CommercialContextMap.prototype.filteredPoints = function filteredPoints() {
    return this.points.filter(
      function (point) { return point.mode === this.activeMode; }.bind(this)
    );
  };

  CommercialContextMap.prototype.filteredRoutes = function filteredRoutes() {
    return this.routes.filter(
      function (route) { return route.mode === this.activeMode; }.bind(this)
    );
  };

  CommercialContextMap.prototype.renderResults = function renderResults() {
    var results = this.root.querySelector('[data-role="results"]');
    if (!results) return;
    var routes = this.filteredRoutes();
    var points = this.filteredPoints();
    var records = routes.map(function (route) {
      return { kind: "route", value: route };
    }).concat(points.map(function (point) {
      return { kind: "point", value: point };
    }));
    if (!records.length) {
      results.innerHTML =
        '<div class="nl-ccm-empty"><strong>' + escapeHtml(this.labels.noEvidence || "No sourced evidence in this mode") +
        '</strong><button type="button" data-act="request-field" data-field-id="context.' + escapeHtml(this.activeMode) + '">' +
        escapeHtml(this.labels.askForLayer || "Request this context layer") + "</button></div>";
      this.updateMapAffordances();
      return;
    }

    var pageSize = this.resultPageSize();
    var pageCount = Math.ceil(records.length / pageSize);
    var page = Math.max(0, Math.min(pageCount - 1, Number(this.pageByMode[this.activeMode]) || 0));
    this.pageByMode[this.activeMode] = page;
    var visible = records.slice(page * pageSize, page * pageSize + pageSize);
    var cards = visible.map(function (record) {
      return record.kind === "route"
        ? routeCard(record.value, this.labels)
        : pointCard(record.value, this.labels);
    }, this).join("");
    var status =
      (this.labels.results || "Results") + ": " + records.length + ". " +
      (this.labels.page || "Page") + " " + (page + 1) + " / " + pageCount + ".";
    results.innerHTML =
      '<div class="nl-ccm-record-list">' + cards + "</div>" +
      '<nav class="nl-ccm-pagination" aria-label="' + escapeHtml(this.labels.pagination || "Context result pages") + '">' +
      '<button type="button" data-map-page="' + (page - 1) + '"' + (page === 0 ? " disabled" : "") + ">" +
      escapeHtml(this.labels.previous || "Previous") + "</button>" +
      '<span role="status" aria-live="polite">' + escapeHtml(status) + "</span>" +
      '<button type="button" data-map-page="' + (page + 1) + '"' + (page + 1 >= pageCount ? " disabled" : "") + ">" +
      escapeHtml(this.labels.next || "Next") + "</button></nav>";
    this.updateMapAffordances();
  };

  CommercialContextMap.prototype.resultPageSize = function resultPageSize() {
    var responsiveLimit = recordsPerPageForViewport(window.innerWidth, window.innerHeight);
    // A short landscape tool has room for one fully disclosed evidence card
    // plus 44px pagination. Configuration may reduce, never raise, that limit.
    if (responsiveLimit === 1) return 1;
    if (this.configuredPageSize && this.configuredPageSize >= 1) {
      return Math.max(1, Math.min(responsiveLimit, 6, Math.floor(this.configuredPageSize)));
    }
    return responsiveLimit;
  };

  CommercialContextMap.prototype.setResultPage = function setResultPage(page) {
    var numericPage = finite(page);
    if (numericPage == null || numericPage < 0) return;
    this.pageByMode[this.activeMode] = Math.floor(numericPage);
    this.renderResults();
  };

  CommercialContextMap.prototype.setMode = function setMode(mode) {
    if (MODES.indexOf(mode) < 0 || mode === this.activeMode) return;
    this.activeMode = mode;
    this.root.querySelectorAll("[data-map-mode]").forEach(function (button) {
      button.setAttribute("aria-pressed", button.dataset.mapMode === mode ? "true" : "false");
    });
    this.renderResults();
    this.refreshMapData();
  };

  CommercialContextMap.prototype.refreshMapData = function refreshMapData() {
    if (!this.map || !this.mapReady) return;
    if (typeof this.map.loaded === "function" && !this.map.loaded()) return;
    var mapboxgl = window.mapboxgl;
    this.markers.forEach(function (marker) { marker.remove(); });
    this.markers = [];
    var self = this;
    this.filteredPoints().forEach(function (point) {
      var element = document.createElement("button");
      element.type = "button";
      element.className = "nl-ccm-marker";
      element.dataset.contextId = point.id;
      element.dataset.operatingState = point.operatingState;
      element.textContent = MARKER_GLYPHS[point.operatingState];
      var markerDescription = [
        point.name,
        (self.labels.operatingState || "Operating state") + ": " +
          operatingStateLabel(point.operatingState, self.labels),
        expectedTimingLabel(point, self.labels),
        qualifyTravelLabel(point, distanceLabel(point, self.labels), self.labels)
      ].filter(Boolean).join(". ");
      element.setAttribute("aria-label", markerDescription);
      var marker = new mapboxgl.Marker({ element: element, anchor: "bottom" }).setLngLat(point.coordinates).addTo(self.map);
      self.markers.push(marker);
    });

    OPERATING_STATES.map(function (state) {
      return "nl-commercial-routes-" + state;
    }).forEach(function (layerId) {
      if (self.map.getLayer(layerId)) self.map.removeLayer(layerId);
    });
    ["nl-commercial-routes"].forEach(function (sourceId) {
      if (self.map.getSource(sourceId)) self.map.removeSource(sourceId);
    });

    var routes = this.filteredRoutes();
    if (routes.length) {
      this.map.addSource("nl-commercial-routes", {
        type: "geojson",
        data: {
          type: "FeatureCollection",
          features: routes.map(function (route) {
            return {
              type: "Feature",
              properties: { id: route.id, operating_state: route.operatingState },
              geometry: { type: "LineString", coordinates: route.geometry }
            };
          })
        }
      });
      OPERATING_STATES.forEach(function (state) {
        var style = ROUTE_STYLES[state];
        var paint = {
          "line-color": style.color,
          "line-width": state === "operating" ? 5 : 4,
          "line-opacity": state === "closed" ? 0.62 : 0.92
        };
        if (style.dash) paint["line-dasharray"] = style.dash;
        self.map.addLayer({
          id: "nl-commercial-routes-" + state,
          type: "line",
          source: "nl-commercial-routes",
          filter: ["==", ["get", "operating_state"], state],
          paint: paint
        });
      });
    }

    var coordinates = [this.center]
      .concat(this.filteredPoints().map(function (point) { return point.coordinates; }))
      .concat(routes.reduce(function (all, route) { return all.concat(route.geometry); }, []))
      .filter(Boolean);
    if (coordinates.length > 1) {
      var bounds = coordinates.reduce(function (box, coordinate) { return box.extend(coordinate); }, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]));
      this.map.fitBounds(bounds, { padding: 56, maxZoom: 15, duration: 0 });
    }
  };

  CommercialContextMap.prototype.focusPoint = function focusPoint(id) {
    var point = this.points.find(function (item) { return item.id === id; });
    if (!point || !this.map || !this.mapReady) return;
    this.map.easeTo({ center: point.coordinates, zoom: Math.max(this.map.getZoom(), 15), duration: 250 });
  };

  CommercialContextMap.prototype.destroy = function destroy(clearRoot) {
    var abortController = this.abortController;
    var markers = Array.isArray(this.markers) ? this.markers.slice() : [];
    var map = this.map;
    var root = this.root;

    // Detach every owned reference first. Even a hostile/partially loaded map
    // implementation cannot leave this controller appearing live after one of
    // its remove hooks throws.
    this.abortController = null;
    this.markers = [];
    this.clearMapLoadWatch();
    this.map = null;
    this.mapReady = false;
    this.mapState = "destroyed";
    this.mapContainer = null;
    this.mapStatus = null;

    if (abortController && typeof abortController.abort === "function") {
      try { abortController.abort(); } catch (error) { /* Continue teardown. */ }
    }
    markers.forEach(function (marker) {
      if (!marker || typeof marker.remove !== "function") return;
      try { marker.remove(); } catch (error) { /* Remove every remaining marker. */ }
    });
    if (map && typeof map.remove === "function") {
      try { map.remove(); } catch (error) { /* The readable DOM still tears down. */ }
    }
    if (clearRoot !== false) {
      // A public destroy releases the root reference as well as its contents.
      // render() deliberately calls destroy(false) so it can reuse its root.
      this.root = null;
      if (root && typeof root.replaceChildren === "function") {
        try { root.replaceChildren(); } catch (error) { /* References are already clear. */ }
      }
    }
  };

  window.NadlanCommercialContextMap = {
    CommercialContextMap: CommercialContextMap,
    validCoordinates: validCoordinates,
    normalizeEvidence: normalizeEvidence,
    isMaterialClaimAllowed: isMaterialClaimAllowed,
    normalizeOperatingState: normalizeOperatingState,
    normalizeExpectedTiming: normalizeExpectedTiming,
    normalizePoint: normalizePoint,
    normalizeRoute: normalizeRoute,
    pointCard: pointCard,
    routeCard: routeCard,
    operatingStateLabel: operatingStateLabel,
    qualifyTravelLabel: qualifyTravelLabel,
    boundedMapLoadTimeout: boundedMapLoadTimeout,
    recordsPerPageForViewport: recordsPerPageForViewport,
    modes: MODES.slice(),
    actionEvents: Object.assign({}, ACTION_EVENTS),
    operatingStates: OPERATING_STATES.slice(),
    storedOperatingStates: STORED_OPERATING_STATES.slice()
  };
})(window, document);
