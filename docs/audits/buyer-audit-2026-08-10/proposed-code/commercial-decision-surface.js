/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Commercial selected-floor decision surface for the existing vanilla-JS engine.
 *
 * The functions are complete and intentionally isolated behind
 * window.NadlanCommercialDecisionSurface. They do not mutate the current engine
 * unless explicitly initialized by a future integration patch.
 */
(function commercialDecisionSurfaceModule(window, document) {
  "use strict";

  var CONTRACT_SCHEMA_VERSION = "1.0.0";
  var VALID_ASSET_TYPES = [
    "residential",
    "commercial_office",
    "retail",
    "mixed_use",
    "hospitality",
    "guide_only"
  ];
  var IMPLEMENTED_ASSET_TYPES = ["commercial_office"];
  var VALID_PRODUCT_FAMILIES = ["living", "premium", "commercial", "guide"];
  var VALID_APPLICABILITY_TAGS = [
    "three_d_showroom",
    "floor_selector",
    "suite_selector",
    "commercial_rfp",
    "context_map",
    "decision_surface"
  ];
  var VALID_EVIDENCE_STATES = ["unknown", "source_estimate", "verified", "contradictory"];
  var VALID_CONFIDENCE_LEVELS = ["unknown", "low", "medium", "high"];
  var VALID_BEAM_DISTANCE_METHODS = [
    "straight_line_geodesic",
    "routed_walking",
    "routed_cycling",
    "routed_driving",
    "routed_transit"
  ];
  var VALID_AVAILABILITY_STATUSES = [
    "unknown",
    "verified_available",
    "soft_hold",
    "under_offer",
    "under_loi",
    "leased",
    "delivered",
    "unavailable",
    "not_marketed"
  ];
  var VALID_COMPASS_SECTORS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  var TOOL_KINDS = ["floor-pack", "fit-out", "context", "cost", "compare", "inquiry", "beam-evidence"];
  var SUPPORTED_LANGUAGE_BASES = ["en", "he", "ar", "fr", "ru"];
  var BEAM_COMPACT_LABEL_MAX_CODE_POINTS = 12;
  var BEAM_FULL_LABEL_MAX_CODE_POINTS = 1000;

  function str(value) {
    return value == null ? "" : String(value);
  }

  function unicodeCodePointLength(value) {
    if (typeof value !== "string") return -1;
    var length = 0;
    for (var index = 0; index < value.length; index += 1) {
      var codeUnit = value.charCodeAt(index);
      if (codeUnit >= 0xD800 && codeUnit <= 0xDBFF) {
        if (index + 1 >= value.length) return -1;
        var next = value.charCodeAt(index + 1);
        if (next < 0xDC00 || next > 0xDFFF) return -1;
        index += 1;
      } else if (codeUnit >= 0xDC00 && codeUnit <= 0xDFFF) {
        return -1;
      }
      length += 1;
    }
    return length;
  }

  function validBeamLabelClaim(claim, maxCodePoints) {
    if (!isBeamClaimAllowed(claim) || typeof claim.value !== "string") return false;
    var text = claim.value;
    var length = unicodeCodePointLength(text);
    return text === text.trim() && length > 0 && length <= maxCodePoints &&
      !/[\u0000-\u001F\u007F]/.test(text);
  }

  function escapeHtml(value) {
    return str(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function safeId(value) {
    return str(value).replace(/[^a-zA-Z0-9_.:-]/g, "-");
  }

  function asArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function isObject(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
  }

  function finite(value) {
    var number = Number(value);
    return Number.isFinite(number) ? number : null;
  }

  function normalizeLocale(value) {
    var requested = str(value || "en").trim().replace(/_/g, "-");
    var base = requested.split("-")[0].toLowerCase();
    if (SUPPORTED_LANGUAGE_BASES.indexOf(base) < 0) return "en";
    try {
      var intlApi = window.Intl || Intl;
      return intlApi.getCanonicalLocales(requested)[0] || base;
    } catch (error) {
      return base;
    }
  }

  function logicalDirection(locale, explicitDirection) {
    var explicit = str(explicitDirection).trim().toLowerCase();
    if (explicit === "rtl" || explicit === "ltr") return explicit;
    var base = normalizeLocale(locale).split("-")[0].toLowerCase();
    return base === "he" || base === "ar" ? "rtl" : "ltr";
  }

  function resolveNumberFormatter(options) {
    options = options || {};
    var supplied = options.numberFormatter;
    if (supplied && typeof supplied.format === "function") return supplied;
    if (typeof supplied === "function") {
      return { format: supplied };
    }
    var locale = normalizeLocale(options.locale);
    var intlApi = window.Intl || Intl;
    return new intlApi.NumberFormat(locale, options.numberFormatOptions || {});
  }

  function formatLocalizedNumber(value, formatter) {
    var number = finite(value);
    return number == null ? "—" : formatter.format(number);
  }

  function logicalBackIcon(direction) {
    return direction === "rtl" ? "→" : "←";
  }

  function normalizedIso(value) {
    var text = str(value).trim();
    if (!text) return "";
    var epoch = Date.parse(text);
    return Number.isFinite(epoch) ? new Date(epoch).toISOString() : "";
  }

  function publicUrl(value) {
    var url = str(value).trim();
    return /^https?:\/\//i.test(url) ? url : "";
  }

  var COMMERCIAL_ROUTE_PARAMS = [
    "wp_post_id",
    "project_id",
    "project_contract_id",
    "building_id",
    "tower_id",
    "floor_id",
    "suite_id"
  ];

  function currentWindowOrigin() {
    try {
      return new URL(window.location.href).origin;
    } catch (error) {
      return "";
    }
  }

  function canonicalProjectBaseUrl(value) {
    var raw = publicUrl(value);
    var currentOrigin = currentWindowOrigin();
    if (!raw || !currentOrigin) return "";
    try {
      var url = new URL(raw);
      if (
        url.protocol !== "https:" || url.username || url.password || url.hash ||
        url.origin !== currentOrigin ||
        COMMERCIAL_ROUTE_PARAMS.some(function (name) { return url.searchParams.has(name); })
      ) {
        return "";
      }
      return url.toString();
    } catch (error) {
      return "";
    }
  }

  function contractId(value) {
    var id = str(value).trim().toLowerCase();
    return /^[a-z0-9][a-z0-9._:-]{0,127}$/.test(id) ? id : "";
  }

  function commercialIdentityKey(buildingId, towerId, floorId, suiteId) {
    return [buildingId, towerId, floorId || "", suiteId || ""].map(contractId).join("|");
  }

  function identityUrl(projectUrl, projectContractId, buildingId, towerId, floorId, suiteId) {
    var base = canonicalProjectBaseUrl(projectUrl);
    projectContractId = contractId(projectContractId);
    buildingId = contractId(buildingId);
    towerId = contractId(towerId);
    floorId = contractId(floorId);
    suiteId = suiteId == null || str(suiteId).trim() === "" ? null : contractId(suiteId);
    if (!base || !projectContractId || !buildingId || !towerId || !floorId || (suiteId === "")) return "";
    try {
      var url = new URL(base);
      if (url.protocol !== "https:" || url.username || url.password) return "";
      url.hash = "";
      url.searchParams.delete("wp_post_id");
      url.searchParams.delete("project_id");
      url.searchParams.set("project_contract_id", projectContractId);
      url.searchParams.set("building_id", buildingId);
      url.searchParams.set("tower_id", towerId);
      url.searchParams.set("floor_id", floorId);
      if (suiteId) url.searchParams.set("suite_id", suiteId);
      else url.searchParams.delete("suite_id");
      url.searchParams.sort();
      return url.toString();
    } catch (error) {
      return "";
    }
  }

  function normalizeSource(raw) {
    if (!isObject(raw)) return null;
    var label = str(raw.label).trim();
    var uri = publicUrl(raw.uri);
    var documentId = contractId(raw.document_id != null ? raw.document_id : raw.documentId);
    var retrievedAt = normalizedIso(raw.retrieved_at != null ? raw.retrieved_at : raw.retrievedAt);
    if (!label || (!uri && !documentId) || !retrievedAt) return null;
    return {
      type: contractId(raw.type) || "other",
      label: label,
      uri: uri,
      documentId: documentId,
      revision: str(raw.revision).trim(),
      publishedAt: normalizedIso(raw.published_at != null ? raw.published_at : raw.publishedAt),
      retrievedAt: retrievedAt
    };
  }

  function normalizeOwner(raw) {
    if (!isObject(raw)) return null;
    var team = str(raw.team).trim();
    var accountableRole = str(
      raw.accountable_role != null ? raw.accountable_role : raw.accountableRole
    ).trim();
    if (!team || !accountableRole) return null;
    return {
      team: team,
      accountableRole: accountableRole,
      contactRef: contractId(raw.contact_ref != null ? raw.contact_ref : raw.contactRef)
    };
  }

  function ownerLabel(owner) {
    if (!owner) return "";
    return [owner.team, owner.accountableRole].filter(Boolean).join(" — ");
  }

  function uniqueSources(sources) {
    var seen = Object.create(null);
    return sources.filter(Boolean).filter(function (source) {
      var key = [source.type, source.documentId, source.uri, source.revision].join("|");
      if (seen[key]) return false;
      seen[key] = true;
      return true;
    });
  }

  function normalizeObservation(raw) {
    if (!isObject(raw) || raw.value == null) return null;
    var source = normalizeSource(raw.source);
    var id = contractId(raw.observation_id != null ? raw.observation_id : raw.observationId);
    if (!source || !id) return null;
    return {
      id: id,
      value: raw.value,
      scope: str(raw.scope).trim(),
      source: source
    };
  }

  function normalizedDocumentIds(raw) {
    return asArray(raw).map(contractId).filter(Boolean).filter(function (id, index, list) {
      return list.indexOf(id) === index;
    });
  }

  function canonicalUnknown(reason, documents, details) {
    details = details || {};
    var sources = uniqueSources(asArray(details.sources));
    var owner = details.owner || null;
    var missingReason = str(reason || details.reason || "Not supplied.").trim();
    return {
      __nlCommercialEvidence: true,
      state: "unknown",
      originalState: str(details.originalState || "unknown"),
      value: null,
      unit: details.unit || "",
      scope: "",
      sources: sources,
      observations: asArray(details.observations),
      verifiedAt: "",
      expiresAt: "",
      owner: owner,
      ownerLabel: ownerLabel(owner),
      confidence: "unknown",
      reason: missingReason,
      applicability: normalizedDocumentIds(details.applicability || ["all"]),
      conflictIds: [],
      note: str(details.note).trim(),
      caveat: str(details.caveat).trim(),
      requiredDocumentIds: normalizedDocumentIds(documents),
      decisionGrade: false,
      issues: asArray(details.issues),
      sourceId: sources.length ? sources[0].documentId : "",
      sourceLabel: sources.length ? sources[0].label : "",
      sourceUrl: sources.length ? sources[0].uri : "",
      effectiveAt: ""
    };
  }

  /**
   * Canonical adapter for the exact envelope emitted by
   * nl_proposal_normalize_evidence_envelope().
   *
   * Unsupported, malformed, or client-expired claims fail closed to unknown.
   * originalState and issues retain diagnostic context without presenting the
   * rejected value as a fact.
   */
  function normalizeEvidenceEnvelope(value, options) {
    options = options || {};
    var now = Number.isFinite(Number(options.now)) ? Number(options.now) : Date.now();

    if (value && value.__nlCommercialEvidence === true) {
      var canonicalExpiry = Date.parse(value.expiresAt);
      if (
        (value.state === "verified" || value.state === "source_estimate") &&
        (!value.expiresAt || !Number.isFinite(canonicalExpiry) || canonicalExpiry <= now)
      ) {
        return canonicalUnknown(
          "Evidence expired in the open browser session.",
          value.requiredDocumentIds,
          {
            originalState: value.state,
            unit: value.unit,
            sources: value.sources,
            observations: value.observations,
            owner: value.owner,
            applicability: value.applicability,
            note: value.note,
            caveat: value.caveat,
            issues: asArray(value.issues).concat(["expired_in_browser"])
          }
        );
      }
      return value;
    }

    var raw = isObject(value) ? value : {};
    var requestedState = str(raw.state).trim().toLowerCase() || "unknown";
    var state = VALID_EVIDENCE_STATES.indexOf(requestedState) >= 0 ? requestedState : "unknown";
    var issues = [];
    if (state !== requestedState) issues.push("unsupported_evidence_state:" + requestedState);

    var sources = uniqueSources(asArray(raw.sources).map(normalizeSource).filter(Boolean));
    if (asArray(raw.sources).length !== sources.length) issues.push("invalid_source");

    var observations = asArray(raw.observations).map(normalizeObservation).filter(Boolean);
    if (asArray(raw.observations).length !== observations.length) issues.push("invalid_observation");

    var owner = normalizeOwner(raw.owner != null ? raw.owner : raw.ownerData);
    var verifiedAt = normalizedIso(raw.verified_at != null ? raw.verified_at : raw.verifiedAt);
    var expiresAt = normalizedIso(raw.expires_at != null ? raw.expires_at : raw.expiresAt);
    var requiredDocumentIds = normalizedDocumentIds(
      raw.required_document_ids != null ? raw.required_document_ids : raw.requiredDocumentIds
    );
    var unit = contractId(raw.unit);
    var scope = str(raw.scope).trim();
    var effectiveAt = normalizedIso(raw.effective_at != null ? raw.effective_at : raw.effectiveAt);
    var confidence = contractId(raw.confidence) || "unknown";
    var reason = str(raw.reason).trim();
    var applicability = normalizedDocumentIds(raw.applicability);
    var conflictIds = normalizedDocumentIds(
      raw.conflict_ids != null ? raw.conflict_ids : raw.conflictIds
    );
    var note = str(raw.note).trim();
    var caveat = str(raw.caveat).trim();
    var rawValue = raw.value == null || raw.value === "" ? null : raw.value;

    if (VALID_CONFIDENCE_LEVELS.indexOf(confidence) < 0) issues.push("invalid_confidence");
    if (!applicability.length) issues.push("missing_applicability");

    if (state === "unknown") {
      if (rawValue != null) issues.push("unknown_with_value");
      if (effectiveAt || verifiedAt || expiresAt) issues.push("unknown_with_verification");
      if (confidence !== "unknown") issues.push("unknown_with_confidence");
      if (conflictIds.length) issues.push("unknown_with_conflicts");
      if (!reason) issues.push("unknown_without_reason");
      return canonicalUnknown(reason || "Not supplied.", requiredDocumentIds, {
        originalState: requestedState,
        unit: unit,
        sources: sources,
        observations: observations,
        owner: owner,
        applicability: applicability,
        note: note,
        caveat: caveat,
        issues: issues
      });
    }

    if (state === "contradictory") {
      if (rawValue != null) issues.push("contradictory_with_value");
      if (observations.length < 2) issues.push("insufficient_observations");
      if (verifiedAt || expiresAt) issues.push("contradictory_with_verification");
      if (!owner) issues.push("missing_owner");
      if (!scope) issues.push("missing_scope");
      if (!effectiveAt || Date.parse(effectiveAt) > now + 300000) issues.push("missing_or_future_effective_at");
      if (confidence === "unknown") issues.push("missing_confidence");
      if (reason) issues.push("contradictory_with_reason");
      var observationIds = observations.map(function (item) { return item.id; }).slice().sort();
      var sortedConflictIds = conflictIds.slice().sort();
      if (JSON.stringify(observationIds) !== JSON.stringify(sortedConflictIds)) {
        issues.push("conflict_id_mismatch");
      }
      if (issues.length) {
        return canonicalUnknown("Contradictory evidence is malformed.", requiredDocumentIds, {
          originalState: requestedState,
          unit: unit,
          sources: sources.concat(observations.map(function (item) { return item.source; })),
          observations: observations,
          owner: owner,
          applicability: applicability,
          note: note,
          caveat: caveat,
          issues: issues
        });
      }
      sources = uniqueSources(sources.concat(observations.map(function (item) { return item.source; })));
      return {
        __nlCommercialEvidence: true,
        state: "contradictory",
        originalState: "contradictory",
        value: null,
        unit: unit,
        scope: scope,
        sources: sources,
        observations: observations,
        verifiedAt: "",
        expiresAt: "",
        owner: owner,
        ownerLabel: ownerLabel(owner),
        confidence: confidence,
        reason: "",
        applicability: applicability,
        conflictIds: conflictIds,
        note: note,
        caveat: caveat,
        requiredDocumentIds: requiredDocumentIds,
        decisionGrade: false,
        issues: [],
        sourceId: sources.length ? sources[0].documentId : "",
        sourceLabel: sources.length ? sources[0].label : "",
        sourceUrl: sources.length ? sources[0].uri : "",
        effectiveAt: effectiveAt
      };
    }

    if (rawValue == null) issues.push("missing_value");
    if (!sources.length) issues.push("missing_source");
    if (!owner) issues.push("missing_owner");
    if (!scope) issues.push("missing_scope");
    if (!effectiveAt || Date.parse(effectiveAt) > now + 300000) issues.push("missing_or_future_effective_at");
    if (confidence === "unknown") issues.push("missing_confidence");
    if (reason) issues.push("positive_claim_with_reason");
    if (conflictIds.length) issues.push("positive_claim_with_conflicts");
    if (!expiresAt || Date.parse(expiresAt) <= now) issues.push("missing_or_expired_expiry");
    if (effectiveAt && expiresAt && Date.parse(expiresAt) <= Date.parse(effectiveAt)) {
      issues.push("invalid_effective_window");
    }

    if (state === "verified") {
      if (!verifiedAt || Date.parse(verifiedAt) > now + 300000) issues.push("missing_or_future_verified_at");
      if (verifiedAt && expiresAt && Date.parse(expiresAt) <= Date.parse(verifiedAt)) {
        issues.push("invalid_verification_window");
      }
    } else if (verifiedAt) {
      issues.push("source_estimate_marked_verified");
    }

    if (issues.length) {
      return canonicalUnknown("Claim failed client contract validation.", requiredDocumentIds, {
        originalState: requestedState,
        unit: unit,
        sources: sources,
        observations: observations,
        owner: owner,
        applicability: applicability,
        note: note,
        caveat: caveat,
        issues: issues
      });
    }

    return {
      __nlCommercialEvidence: true,
      state: state,
      originalState: state,
      value: rawValue,
      unit: unit,
      scope: scope,
      sources: sources,
      observations: observations,
      verifiedAt: verifiedAt,
      expiresAt: expiresAt,
      owner: owner,
      ownerLabel: ownerLabel(owner),
      confidence: confidence,
      reason: "",
      applicability: applicability,
      conflictIds: [],
      note: note,
      caveat: caveat,
      requiredDocumentIds: requiredDocumentIds,
      decisionGrade: state === "verified",
      issues: [],
      sourceId: sources[0].documentId,
      sourceLabel: sources[0].label,
      sourceUrl: sources[0].uri,
      effectiveAt: effectiveAt
    };
  }

  function evidence(value, options) {
    return normalizeEvidenceEnvelope(value, options);
  }

  function normalizeAvailabilityStatus(value) {
    var status = str(value).trim().toLowerCase();
    return VALID_AVAILABILITY_STATUSES.indexOf(status) >= 0 ? status : "unknown";
  }

  function normalizeAvailability(value, options) {
    var item = normalizeEvidenceEnvelope(value, options);
    var status = normalizeAvailabilityStatus(item.value);
    if (status !== "unknown" && item.state !== "verified") status = "unknown";
    return { evidence: item, status: status };
  }

  function evidenceValue(item) {
    item = normalizeEvidenceEnvelope(item);
    return item.state === "unknown" || item.state === "contradictory" ? null : item.value;
  }

  function evidenceText(item, fallback) {
    var value = evidenceValue(item);
    return value == null || value === "" ? str(fallback) : str(value);
  }

  function missingEvidence(reason, documents) {
    return canonicalUnknown(reason, documents || [], {});
  }

  function aggregateExposureEvidence(exposures) {
    if (!exposures.length) {
      return missingEvidence("No verified facade exposure geometry was supplied.", ["orientation_plan"]);
    }
    var directions = exposures.map(function (entry) { return entry.direction; });
    if (directions.some(function (item) { return item.state !== "verified"; })) {
      return canonicalUnknown("One or more facade directions failed verification.", ["orientation_plan"], {
        originalState: "unknown",
        issues: ["unverified_exposure_direction"]
      });
    }
    var sources = uniqueSources(directions.reduce(function (all, item) {
      return all.concat(item.sources);
    }, []));
    var verifiedAt = directions.map(function (item) { return item.verifiedAt; }).filter(Boolean).sort()[0] || "";
    var effectiveAt = directions.map(function (item) { return item.effectiveAt; }).filter(Boolean).sort()[0] || "";
    var expiresAt = directions.map(function (item) { return item.expiresAt; }).filter(Boolean).sort()[0] || "";
    var owner = directions[0].owner;
    var confidenceOrder = { unknown: 0, low: 1, medium: 2, high: 3 };
    var confidence = directions.map(function (item) { return item.confidence; }).sort(function (a, b) {
      return (confidenceOrder[a] || 0) - (confidenceOrder[b] || 0);
    })[0] || "unknown";
    var applicability = directions.reduce(function (all, item) {
      return all.concat(item.applicability || []);
    }, []).filter(function (item, index, list) { return list.indexOf(item) === index; });
    return {
      __nlCommercialEvidence: true,
      state: "verified",
      originalState: "verified",
      value: exposures,
      unit: "",
      scope: directions.map(function (item) { return item.scope; }).filter(Boolean).join("; "),
      sources: sources,
      observations: [],
      verifiedAt: verifiedAt,
      expiresAt: expiresAt,
      owner: owner,
      ownerLabel: ownerLabel(owner),
      confidence: confidence,
      reason: "",
      applicability: applicability,
      conflictIds: [],
      note: "",
      caveat: "",
      requiredDocumentIds: ["orientation_plan"],
      decisionGrade: true,
      issues: [],
      sourceId: sources.length ? sources[0].documentId : "",
      sourceLabel: sources.length ? sources[0].label : "",
      sourceUrl: sources.length ? sources[0].uri : "",
      effectiveAt: effectiveAt
    };
  }

  function adaptExposure(raw, options) {
    raw = isObject(raw) ? raw : {};
    return {
      id: contractId(raw.exposure_id != null ? raw.exposure_id : raw.exposureId),
      direction: normalizeEvidenceEnvelope(raw.direction, options),
      azimuthStartDeg: normalizeEvidenceEnvelope(
        raw.azimuth_start_deg != null ? raw.azimuth_start_deg : raw.azimuthStartDeg,
        options
      ),
      azimuthEndDeg: normalizeEvidenceEnvelope(
        raw.azimuth_end_deg != null ? raw.azimuth_end_deg : raw.azimuthEndDeg,
        options
      ),
      facadeSharePct: normalizeEvidenceEnvelope(
        raw.facade_share_pct != null ? raw.facade_share_pct : raw.facadeSharePct,
        options
      ),
      viewContext: normalizeEvidenceEnvelope(
        raw.view_context != null ? raw.view_context : raw.viewContext,
        options
      ),
      obstructions: normalizeEvidenceEnvelope(raw.obstructions, options)
    };
  }

  function adaptExposures(raw, options) {
    var entries = asArray(raw).map(function (entry) {
      return adaptExposure(entry, options);
    }).filter(function (entry) {
      return Boolean(entry.id);
    });
    return aggregateExposureEvidence(entries);
  }

  function isBeamClaimAllowed(item) {
    return item && (item.state === "verified" || item.state === "source_estimate");
  }

  function coordinateValue(item) {
    var value = item && item.value;
    var lat = value && finite(value.lat);
    var lng = value && finite(value.lng);
    return lat != null && lng != null && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180
      ? { lat: lat, lng: lng }
      : null;
  }

  function normalizedAngle(value) {
    var number = finite(value);
    return number == null ? null : ((number % 360) + 360) % 360;
  }

  function bearingInSector(bearing, start, end) {
    bearing = normalizedAngle(bearing);
    start = normalizedAngle(start);
    end = normalizedAngle(end);
    if (bearing == null || start == null || end == null) return false;
    if (Math.abs(start - end) < 0.000001) return Math.abs(bearing - start) <= 1;
    return start < end ? bearing >= start && bearing <= end : bearing >= start || bearing <= end;
  }

  function geodesicMetrics(anchor, coordinate) {
    var radius = 6371008.8;
    var lat1 = anchor.lat * Math.PI / 180;
    var lat2 = coordinate.lat * Math.PI / 180;
    var dlat = lat2 - lat1;
    var dlng = (coordinate.lng - anchor.lng) * Math.PI / 180;
    var a = Math.sin(dlat / 2) * Math.sin(dlat / 2) +
      Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlng / 2) * Math.sin(dlng / 2);
    var distance = radius * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(Math.max(0, 1 - a)));
    var y = Math.sin(dlng) * Math.cos(lat2);
    var x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dlng);
    return {
      distanceM: distance,
      bearingDeg: normalizedAngle(Math.atan2(y, x) * 180 / Math.PI)
    };
  }

  function neutralBeamScene(anchor, caveat, issues) {
    return {
      __nlCommercialBeamScene: true,
      state: "unknown",
      projection: "north_up_local_equirectangular_v1",
      projectAnchor: anchor,
      exposures: [],
      caveat: str(caveat).trim(),
      issues: asArray(issues).filter(Boolean)
    };
  }

  function adaptBeamLandmark(raw, exposure, anchorValue, options) {
    raw = isObject(raw) ? raw : {};
    var id = contractId(raw.landmark_id);
    var exposureId = contractId(raw.exposure_id);
    var label = normalizeEvidenceEnvelope(raw.label, options);
    var compactLabel = normalizeEvidenceEnvelope(raw.compact_label, options);
    var coordinates = normalizeEvidenceEnvelope(raw.coordinates, options);
    var distance = normalizeEvidenceEnvelope(raw.distance_m, options);
    var method = normalizeEvidenceEnvelope(raw.distance_method, options);
    var bearing = normalizeEvidenceEnvelope(raw.bearing_deg, options);
    var coordinate = coordinateValue(coordinates);
    var reportedDistance = finite(distance.value);
    var reportedBearing = finite(bearing.value);
    var methodValue = str(method.value);
    var issues = [];
    var incompleteClaim = (
      !id ||
      exposureId !== exposure.id ||
      !validBeamLabelClaim(label, BEAM_FULL_LABEL_MAX_CODE_POINTS) ||
      !isBeamClaimAllowed(coordinates) ||
      !isBeamClaimAllowed(distance) ||
      !isBeamClaimAllowed(method) ||
      !isBeamClaimAllowed(bearing) ||
      !coordinate ||
      reportedDistance == null ||
      reportedDistance < 0 ||
      reportedBearing == null ||
      VALID_BEAM_DISTANCE_METHODS.indexOf(methodValue) < 0
    );
    if (incompleteClaim) {
      issues.push("incomplete_landmark_claim:" + (id || "unknown"));
    }
    if (!validBeamLabelClaim(compactLabel, BEAM_COMPACT_LABEL_MAX_CODE_POINTS)) {
      issues.push("invalid_landmark_compact_label:" + (id || "unknown"));
    }
    if (!incompleteClaim && validBeamLabelClaim(compactLabel, BEAM_COMPACT_LABEL_MAX_CODE_POINTS)) {
      var metrics = geodesicMetrics(anchorValue, coordinate);
      var bearingDelta = Math.abs(normalizedAngle(reportedBearing) - metrics.bearingDeg);
      bearingDelta = Math.min(bearingDelta, 360 - bearingDelta);
      if (bearingDelta > 8) issues.push("landmark_coordinate_bearing_mismatch:" + id);
      if (!bearingInSector(reportedBearing, exposure.azimuthStartDeg.value, exposure.azimuthEndDeg.value)) {
        issues.push("landmark_outside_exposure_sector:" + id);
      }
      if (
        methodValue === "straight_line_geodesic" &&
        Math.abs(reportedDistance - metrics.distanceM) > Math.max(30, metrics.distanceM * 0.15)
      ) {
        issues.push("landmark_geodesic_distance_mismatch:" + id);
      }
      if (methodValue.indexOf("routed_") === 0 && reportedDistance + 1 < metrics.distanceM * 0.95) {
        issues.push("routed_distance_shorter_than_geodesic:" + id);
      }
    }
    return {
      id: id,
      exposureId: exposureId,
      label: label,
      compactLabel: compactLabel,
      coordinates: coordinates,
      distanceM: distance,
      distanceMethod: method,
      bearingDeg: bearing,
      caveat: str(raw.caveat).trim(),
      issues: issues
    };
  }

  function adaptBeamScene(raw, exposures, options) {
    raw = isObject(raw) ? raw : {};
    var anchor = normalizeEvidenceEnvelope(raw.project_anchor, options);
    var caveat = str(raw.illustrative_caveat).trim();
    var anchorValue = coordinateValue(anchor);
    var facadeList = exposures && exposures.state === "verified" && Array.isArray(exposures.value)
      ? exposures.value : [];
    var facadeById = Object.create(null);
    var issues = asArray(raw.issues).map(str).filter(Boolean);
    facadeList.forEach(function (exposure) {
      if (!exposure.id || facadeById[exposure.id]) issues.push("duplicate_or_missing_facade_exposure_id");
      else facadeById[exposure.id] = exposure;
    });
    if (str(raw.scene_state) !== "ready") issues.push("server_scene_not_ready");
    if (str(raw.projection) !== "north_up_local_equirectangular_v1") issues.push("unsupported_beam_projection");
    if (!isBeamClaimAllowed(anchor) || !anchorValue) issues.push("project_anchor_not_current");

    var seenAssociations = Object.create(null);
    var seenLandmarks = Object.create(null);
    var landmarkCount = 0;
    var adaptedExposures = asArray(raw.exposures).map(function (association) {
      association = isObject(association) ? association : {};
      var exposureId = contractId(association.exposure_id);
      var exposure = facadeById[exposureId];
      if (!exposureId || seenAssociations[exposureId]) issues.push("duplicate_or_missing_beam_exposure_id");
      if (!exposure) issues.push("unknown_beam_exposure_id:" + (exposureId || "unknown"));
      seenAssociations[exposureId] = true;
      if (exposure) {
        [exposure.direction, exposure.azimuthStartDeg, exposure.azimuthEndDeg, exposure.facadeSharePct]
          .forEach(function (claim) {
            if (!isBeamClaimAllowed(claim)) issues.push("incomplete_facade_geometry:" + exposureId);
          });
      }
      var landmarks = exposure ? asArray(association.landmarks).map(function (landmark) {
        var adapted = adaptBeamLandmark(landmark, exposure, anchorValue || { lat: 0, lng: 0 }, options);
        if (!adapted.id || seenLandmarks[adapted.id]) issues.push("duplicate_or_missing_landmark_id");
        seenLandmarks[adapted.id] = true;
        landmarkCount += 1;
        if (landmarkCount > 4) issues.push("too_many_beam_landmarks");
        issues = issues.concat(adapted.issues);
        return adapted;
      }) : [];
      if (exposure && !landmarks.length) issues.push("missing_beam_landmarks:" + exposureId);
      return { exposureId: exposureId, exposure: exposure || null, landmarks: landmarks };
    });
    var expectedIds = Object.keys(facadeById).sort();
    var actualIds = Object.keys(seenAssociations).sort();
    if (JSON.stringify(expectedIds) !== JSON.stringify(actualIds)) issues.push("incomplete_exposure_association");
    if (issues.length) return neutralBeamScene(anchor, caveat, issues);
    return {
      __nlCommercialBeamScene: true,
      state: "ready",
      projection: "north_up_local_equirectangular_v1",
      projectAnchor: anchor,
      exposures: adaptedExposures,
      caveat: caveat,
      issues: []
    };
  }

  function adaptToolEvidence(raw, key, reason, documents, options) {
    var source = isObject(raw) && raw[key] != null ? raw[key] : null;
    return source == null
      ? missingEvidence(reason, documents)
      : normalizeEvidenceEnvelope(source, options);
  }

  function adaptTower(raw, options) {
    raw = isObject(raw) ? raw : {};
    var buildingId = contractId(raw.building_id);
    var towerId = contractId(raw.tower_id);
    var displayLabel = normalizeEvidenceEnvelope(raw.display_label, options);
    return {
      buildingId: buildingId,
      towerId: towerId,
      identityKey: commercialIdentityKey(buildingId, towerId),
      displayLabel: displayLabel,
      label: displayLabel.state === "verified" ? str(displayLabel.value).trim() : "",
      valid: Boolean(buildingId && towerId && displayLabel.state === "verified" && str(displayLabel.value).trim())
    };
  }

  function adaptSuite(raw, projectView, floorView, options) {
    raw = isObject(raw) ? raw : {};
    var id = contractId(raw.suite_id);
    var availability = normalizeAvailability(raw.availability, options);
    var label = normalizeEvidenceEnvelope(raw.label, options);
    var identityMatches =
      contractId(raw.building_id) === floorView.buildingId &&
      contractId(raw.tower_id) === floorView.towerId &&
      contractId(raw.floor_id) === floorView.id;
    var toolEvidence = options && isObject(options.toolEvidenceByAssetId)
      ? options.toolEvidenceByAssetId[id]
      : null;
    return {
      __nlCommercialAsset: true,
      kind: "suite",
      id: id,
      projectId: projectView.projectId,
      wpPostId: projectView.wpPostId,
      projectUrl: projectView.projectUrl,
      projectName: projectView.projectName,
      buildingId: floorView.buildingId,
      towerId: floorView.towerId,
      towerLabel: floorView.towerLabel,
      floorId: floorView.id,
      suiteId: id,
      floorLabel: floorView.floorLabel,
      spaceLabel: evidenceText(label, id),
      labelEvidence: label,
      identityKey: commercialIdentityKey(floorView.buildingId, floorView.towerId, floorView.id, id),
      url: identityUrl(projectView.projectUrl, projectView.projectId, floorView.buildingId, floorView.towerId, floorView.id, id),
      selectable:
        projectView.uiAdapterSupported &&
        identityMatches &&
        floorView.selectable &&
        raw.selectable === true &&
        label.state === "verified",
      availability: availability.evidence,
      status: availability.status,
      rentableArea: normalizeEvidenceEnvelope(raw.gross_rentable_sqm, options),
      usableArea: normalizeEvidenceEnvelope(raw.usable_sqm, options),
      askingRent: normalizeEvidenceEnvelope(raw.asking_rent_nis_sqm_month, options),
      serviceCharge: normalizeEvidenceEnvelope(raw.service_charge_nis_sqm_month, options),
      availableFrom: normalizeEvidenceEnvelope(raw.available_from, options),
      planningCapacity: normalizeEvidenceEnvelope(raw.test_fit_headcount, options),
      monthlyAllIn: missingEvidence(
        "No verified all-in cost schedule was supplied.",
        ["landlord_offer", "service_charge_budget", "arnona_assessment"]
      ),
      exposures: adaptExposures(raw.exposures, options),
      beamScene: raw.beam_scene
        ? adaptBeamScene(
            raw.beam_scene,
            adaptExposures(raw.exposures, options),
            options
          )
        : floorView.beamScene,
      floorPackAvailable: adaptToolEvidence(
        toolEvidence,
        "floor_pack_available",
        "No verified suite floor pack was supplied.",
        ["floor_plan_pdf", "measurement_report"],
        options
      ),
      fitOutAvailable: adaptToolEvidence(
        toolEvidence,
        "fit_out_available",
        "No verified suite fit-out pack was supplied.",
        ["tenant_technical_manual", "validated_test_fit"],
        options
      ),
      contextAvailable: adaptToolEvidence(
        toolEvidence,
        "context_available",
        "No evidence-backed context layer was supplied.",
        [],
        options
      ),
      costAvailable: adaptToolEvidence(
        toolEvidence,
        "cost_available",
        "No complete verified cost schedule was supplied.",
        ["landlord_offer", "service_charge_budget", "arnona_assessment"],
        options
      )
    };
  }

  function adaptFloor(raw, projectView, options) {
    raw = isObject(raw) ? raw : {};
    var id = contractId(raw.floor_id);
    var legalLabel = normalizeEvidenceEnvelope(raw.legal_floor_label, options);
    var elevatorLabel = normalizeEvidenceEnvelope(raw.elevator_label, options);
    var marketingLabel = normalizeEvidenceEnvelope(raw.marketing_label, options);
    var zone = normalizeEvidenceEnvelope(raw.zone, options);
    var availability = normalizeAvailability(raw.availability, options);
    var buildingId = contractId(raw.building_id);
    var towerId = contractId(raw.tower_id);
    var tower = projectView.towerByKey[commercialIdentityKey(buildingId, towerId)] || null;
    var towerDisplayLabel = normalizeEvidenceEnvelope(raw.tower_display_label, options);
    var towerLabelMatches = Boolean(
      tower &&
      tower.valid &&
      towerDisplayLabel.state === "verified" &&
      str(towerDisplayLabel.value).trim() === tower.label
    );
    var toolEvidence = options && isObject(options.toolEvidenceByAssetId)
      ? options.toolEvidenceByAssetId[id]
      : null;
    var exposures = adaptExposures(raw.exposures, options);
    var floorView = {
      __nlCommercialAsset: true,
      kind: "floor",
      id: id,
      projectId: projectView.projectId,
      wpPostId: projectView.wpPostId,
      projectUrl: projectView.projectUrl,
      projectName: projectView.projectName,
      buildingId: buildingId,
      towerId: towerId,
      towerLabel: tower && tower.valid ? tower.label : "",
      floorId: id,
      suiteId: null,
      floorLabel: evidenceText(elevatorLabel, evidenceText(legalLabel, evidenceText(marketingLabel, id))),
      spaceLabel: "",
      towerDisplayLabel: towerDisplayLabel,
      identityKey: commercialIdentityKey(buildingId, towerId, id),
      url: identityUrl(projectView.projectUrl, projectView.projectId, buildingId, towerId, id),
      legalFloorLabel: legalLabel,
      elevatorLabel: elevatorLabel,
      marketingLabel: marketingLabel,
      zone: zone,
      selectable:
        projectView.uiAdapterSupported &&
        towerLabelMatches &&
        raw.selectable === true &&
        legalLabel.state === "verified" &&
        elevatorLabel.state === "verified",
      availability: availability.evidence,
      status: availability.status,
      rentableArea: normalizeEvidenceEnvelope(raw.gross_rentable_sqm, options),
      usableArea: normalizeEvidenceEnvelope(raw.usable_sqm, options),
      clearHeight: normalizeEvidenceEnvelope(raw.clear_height_m, options),
      floorLoad: normalizeEvidenceEnvelope(raw.floor_load_kg_m2, options),
      tenantPower: normalizeEvidenceEnvelope(raw.tenant_power_va_m2, options),
      planningCapacity: missingEvidence(
        "No floor-level validated test-fit headcount was supplied.",
        ["validated_test_fit"]
      ),
      monthlyAllIn: missingEvidence(
        "No verified all-in cost schedule was supplied.",
        ["landlord_offer", "service_charge_budget", "arnona_assessment"]
      ),
      exposures: exposures,
      beamScene: adaptBeamScene(raw.beam_scene, exposures, options),
      floorPackAvailable: adaptToolEvidence(
        toolEvidence,
        "floor_pack_available",
        "No verified floor pack was supplied.",
        ["floor_plan_pdf", "measurement_report"],
        options
      ),
      fitOutAvailable: adaptToolEvidence(
        toolEvidence,
        "fit_out_available",
        "No verified fit-out and infrastructure pack was supplied.",
        ["tenant_technical_manual", "validated_test_fit"],
        options
      ),
      contextAvailable: adaptToolEvidence(
        toolEvidence,
        "context_available",
        "No evidence-backed context layer was supplied.",
        [],
        options
      ),
      costAvailable: adaptToolEvidence(
        toolEvidence,
        "cost_available",
        "No complete verified cost schedule was supplied.",
        ["landlord_offer", "service_charge_budget", "arnona_assessment"],
        options
      ),
      suites: []
    };
    floorView.suites = asArray(raw.suites).map(function (suite) {
      return adaptSuite(suite, projectView, floorView, options);
    });
    return floorView;
  }

  function compareVocabulary(received, expected, key, issues) {
    if (!Array.isArray(received)) {
      issues.push("missing_vocabulary:" + key);
      return;
    }
    var normalized = received.map(function (value) { return str(value); }).slice().sort();
    var canonical = expected.slice().sort();
    if (JSON.stringify(normalized) !== JSON.stringify(canonical)) {
      issues.push("vocabulary_mismatch:" + key);
    }
  }

  function adaptProjectContract(raw, options) {
    raw = isObject(raw) ? raw : {};
    options = options || {};
    var issues = [];
    if (str(raw.schema_version) !== CONTRACT_SCHEMA_VERSION) issues.push("schema_version_mismatch");
    var vocabularies = isObject(raw.vocabularies) ? raw.vocabularies : {};
    compareVocabulary(vocabularies.evidence_states, VALID_EVIDENCE_STATES, "evidence_states", issues);
    compareVocabulary(vocabularies.confidence_levels, VALID_CONFIDENCE_LEVELS, "confidence_levels", issues);
    compareVocabulary(vocabularies.beam_distance_methods, VALID_BEAM_DISTANCE_METHODS, "beam_distance_methods", issues);
    compareVocabulary(vocabularies.asset_types, VALID_ASSET_TYPES, "asset_types", issues);
    compareVocabulary(
      vocabularies.implemented_asset_types,
      IMPLEMENTED_ASSET_TYPES,
      "implemented_asset_types",
      issues
    );
    compareVocabulary(
      vocabularies.product_families,
      VALID_PRODUCT_FAMILIES,
      "product_families",
      issues
    );
    compareVocabulary(
      vocabularies.applicability_tags,
      VALID_APPLICABILITY_TAGS,
      "applicability_tags",
      issues
    );
    compareVocabulary(
      vocabularies.availability_statuses,
      VALID_AVAILABILITY_STATUSES,
      "availability_statuses",
      issues
    );
    compareVocabulary(vocabularies.compass_sectors, VALID_COMPASS_SECTORS, "compass_sectors", issues);

    var assetType = contractId(raw.asset_type);
    var productFamily = contractId(raw.product_family);
    var applicabilityTags = asArray(raw.applicability_tags).map(contractId).filter(Boolean);
    var uiAdapterSupported =
      raw.ui_adapter_supported === true &&
      IMPLEMENTED_ASSET_TYPES.indexOf(assetType) >= 0;
    if (VALID_ASSET_TYPES.indexOf(assetType) < 0) issues.push("unsupported_asset_type");
    if (VALID_PRODUCT_FAMILIES.indexOf(productFamily) < 0) issues.push("unsupported_product_family");
    if (applicabilityTags.some(function (tag) {
      return VALID_APPLICABILITY_TAGS.indexOf(tag) < 0;
    })) {
      issues.push("unsupported_applicability_tag");
    }
    if (!uiAdapterSupported) issues.push("ui_adapter_not_implemented:" + assetType);

    var projectView = {
      __nlCommercialProject: true,
      schemaVersion: str(raw.schema_version),
      projectId: contractId(raw.project_id),
      wpPostId: finite(raw.wp_post_id),
      projectUrl: canonicalProjectBaseUrl(raw.project_url),
      assetType: assetType,
      productFamily: productFamily,
      applicabilityTags: applicabilityTags,
      uiAdapterSupported: uiAdapterSupported,
      projectName: str(raw.title).trim(),
      generatedAt: normalizedIso(raw.generated_at),
      vocabularies: vocabularies,
      facts: {},
      floorInventory: normalizeEvidenceEnvelope(raw.floor_inventory, options),
      towers: [],
      towerByKey: Object.create(null),
      floors: [],
      floorById: Object.create(null),
      floorByKey: Object.create(null),
      assetByKey: Object.create(null),
      publicationBlockers: asArray(raw.publication_blockers).map(str).filter(Boolean),
      publicationAllowed: false,
      selectableFloorCount: 0,
      contractIssues: issues
    };

    projectView.towers = asArray(raw.towers).map(function (tower) {
      return adaptTower(tower, options);
    }).filter(function (tower) {
      if (!tower.valid || projectView.towerByKey[tower.identityKey]) {
        projectView.contractIssues.push("invalid_or_duplicate_tower_identity");
        return false;
      }
      projectView.towerByKey[tower.identityKey] = tower;
      return true;
    });
    if (!projectView.projectUrl) projectView.contractIssues.push("invalid_project_url");
    if (!projectView.towers.length) projectView.contractIssues.push("missing_tower_crosswalk");

    Object.keys(isObject(raw.project_facts) ? raw.project_facts : {}).forEach(function (key) {
      projectView.facts[key] = normalizeEvidenceEnvelope(raw.project_facts[key], options);
    });
    projectView.floors = asArray(raw.floors).map(function (floor) {
      return adaptFloor(floor, projectView, options);
    }).filter(function (floor) {
      if (!floor.id || !floor.buildingId || !floor.towerId || projectView.floorByKey[floor.identityKey]) {
        projectView.contractIssues.push("invalid_or_duplicate_floor_id");
        return false;
      }
      if (!floor.url) {
        projectView.contractIssues.push("invalid_floor_identity_url");
        floor.selectable = false;
      }
      projectView.floorByKey[floor.identityKey] = floor;
      projectView.assetByKey[floor.identityKey] = floor;
      floor.suites.forEach(function (suite) {
        if (!suite.id || !suite.identityKey || !suite.url || projectView.assetByKey[suite.identityKey]) {
          projectView.contractIssues.push("invalid_or_duplicate_suite_identity");
          suite.selectable = false;
          return;
        }
        projectView.assetByKey[suite.identityKey] = suite;
      });
      if (projectView.floorById[floor.id]) projectView.floorById[floor.id] = null;
      else if (!Object.prototype.hasOwnProperty.call(projectView.floorById, floor.id)) {
        projectView.floorById[floor.id] = floor;
      }
      return true;
    });
    projectView.selectableFloorCount = projectView.floors.filter(function (floor) {
      return floor.selectable;
    }).length;
    projectView.publicationAllowed =
      raw.publication_allowed === true &&
      projectView.uiAdapterSupported &&
      projectView.floorInventory.state === "verified" &&
      projectView.selectableFloorCount > 0 &&
      projectView.publicationBlockers.length === 0 &&
      projectView.contractIssues.length === 0;
    return projectView;
  }

  function adaptContractPayload(raw, options) {
    var projects = isObject(raw) && Array.isArray(raw.projects)
      ? raw.projects.map(function (project) { return adaptProjectContract(project, options); })
      : [adaptProjectContract(raw, options)];
    return {
      schemaVersion: str(raw && raw.schema_version),
      projects: projects,
      projectById: projects.reduce(function (index, project) {
        if (project.projectId) index[project.projectId] = project;
        return index;
      }, Object.create(null))
    };
  }

  function formatAreaForPicker(item, options) {
    item = normalizeEvidenceEnvelope(item);
    if (item.state === "unknown" || item.state === "contradictory" || item.value == null) return "";
    var formatter = resolveNumberFormatter(options);
    return (
      formatLocalizedNumber(item.value, formatter) +
      " m² (" +
      item.state.replace(/_/g, " ") +
      ")"
    );
  }

  function buildFloorRanges(projectView, calibration, options) {
    if (!projectView || projectView.__nlCommercialProject !== true) {
      throw new Error("A canonical commercial project view is required.");
    }
    return asArray(calibration).map(function (entry, index) {
      entry = isObject(entry) ? entry : {};
      var buildingId = contractId(entry.building_id != null ? entry.building_id : entry.buildingId);
      var towerId = contractId(entry.tower_id != null ? entry.tower_id : entry.towerId);
      var floorId = contractId(entry.floor_id != null ? entry.floor_id : entry.floorId);
      var identityKey = commercialIdentityKey(buildingId, towerId, floorId);
      var floor = projectView.floorByKey[identityKey];
      var minY = finite(entry.min_y != null ? entry.min_y : entry.minY);
      var maxY = finite(entry.max_y != null ? entry.max_y : entry.maxY);
      var calibrationEvidence = normalizeEvidenceEnvelope(entry.evidence, options);
      if (!floor || minY == null || maxY == null || maxY <= minY) {
        throw new Error("Invalid floor calibration at index " + index);
      }
      return {
        buildingId: buildingId,
        towerId: towerId,
        floorId: floorId,
        identityKey: identityKey,
        minY: minY,
        maxY: maxY,
        selectable: floor.selectable && calibrationEvidence.state === "verified",
        displayOrder: finite(entry.display_order != null ? entry.display_order : entry.displayOrder),
        label: floor.floorLabel,
        towerLabel: floor.towerLabel,
        zone: evidenceText(floor.zone, ""),
        zoneEvidence: floor.zone,
        status: floor.status,
        availability: floor.availability,
        reportedArea: formatAreaForPicker(floor.rentableArea, options),
        areaEvidence: floor.rentableArea,
        calibrationEvidence: calibrationEvidence
      };
    });
  }

  function truthLabel(item, labels) {
    labels = labels || {};
    return (labels.evidenceStates && labels.evidenceStates[item.state]) || item.state.replace(/_/g, " ");
  }

  function formatValue(item, formatter) {
    if (item.value == null) return "—";
    if (typeof formatter === "function") return formatter(item.value);
    return str(item.value);
  }

  function evidenceMeta(item, labels) {
    var pieces = [truthLabel(item, labels)];
    if (item.verifiedAt) pieces.push((labels.verified || "verified") + " " + item.verifiedAt);
    else if (item.effectiveAt) pieces.push((labels.effective || "effective") + " " + item.effectiveAt);
    if (item.sourceLabel) pieces.push(item.sourceLabel);
    if (item.sources.length > 1) pieces.push(item.sources.length + " " + (labels.sources || "sources"));
    return pieces.join(" · ");
  }

  function renderMissingAction(fieldId, item, labels) {
    labels = labels || {};
    return (
      '<button class="nl-cds-missing" type="button" data-act="request-field" data-field-id="' +
      escapeHtml(fieldId) +
      '">' +
      '<span class="nl-cds-missing__title">' +
      escapeHtml(labels.askThis || "Ask this question") +
      "</span>" +
      '<span class="nl-cds-missing__meta">' +
      escapeHtml(item.ownerLabel ? (labels.owner || "Owner") + ": " + item.ownerLabel : labels.ownerUnknown || "Answer owner not assigned") +
      "</span></button>"
    );
  }

  function renderContradictoryObservations(item, labels) {
    if (item.state !== "contradictory") return "";
    return (
      '<ul class="nl-cds-observations" aria-label="' +
      escapeHtml(labels.conflictingObservations || "Conflicting sourced observations") +
      '">' +
      item.observations.map(function (observation) {
        var source = observation.source || {};
        return (
          "<li><strong>" +
          escapeHtml(str(observation.value)) +
          "</strong><span>" +
          escapeHtml([observation.scope, source.label].filter(Boolean).join(" · ")) +
          "</span></li>"
        );
      }).join("") +
      "</ul>"
    );
  }

  function renderEvidenceFact(spec, labels) {
    var item = evidence(spec.evidence);
    var missing = item.state === "unknown";
    return (
      '<article class="nl-cds-fact" data-evidence-state="' + escapeHtml(item.state) + '">' +
      '<div class="nl-cds-fact__head"><span>' + escapeHtml(spec.label) + "</span>" +
      '<span class="nl-cds-state">' + escapeHtml(truthLabel(item, labels)) + "</span></div>" +
      (missing
        ? renderMissingAction(spec.fieldId, item, labels)
        : '<strong class="nl-cds-fact__value">' + escapeHtml(formatValue(item, spec.formatter)) + "</strong>" +
          '<span class="nl-cds-fact__meta">' + escapeHtml(evidenceMeta(item, labels)) + "</span>" +
          renderContradictoryObservations(item, labels) +
          (item.caveat ? '<span class="nl-cds-fact__caveat">' + escapeHtml(item.caveat) + "</span>" : "")) +
      "</article>"
    );
  }

  function statusClass(status) {
    return normalizeAvailabilityStatus(status);
  }

  function beamPoint(bearing, radius) {
    var angle = (finite(bearing) - 90) * Math.PI / 180;
    return {
      x: 160 + Math.cos(angle) * radius,
      y: 78 + Math.sin(angle) * radius
    };
  }

  function beamPath(startBearing, endBearing) {
    var start = ((finite(startBearing) % 360) + 360) % 360;
    var end = ((finite(endBearing) % 360) + 360) % 360;
    var delta = (end - start + 360) % 360;
    var startPoint = beamPoint(start, 68);
    var endPoint = beamPoint(end, 68);
    return (
      "M160 78 L" + startPoint.x.toFixed(2) + " " + startPoint.y.toFixed(2) +
      " A68 68 0 " + (delta > 180 ? "1" : "0") + " 1 " +
      endPoint.x.toFixed(2) + " " + endPoint.y.toFixed(2) + " Z"
    );
  }

  function normalizedBeamBearing(value) {
    return ((finite(value) % 360) + 360) % 360;
  }

  function beamExposureCenter(exposure) {
    var start = normalizedBeamBearing(exposure.azimuthStartDeg.value);
    var end = normalizedBeamBearing(exposure.azimuthEndDeg.value);
    return normalizedBeamBearing(start + ((end - start + 360) % 360) / 2);
  }

  /*
   * Stable clockwise ordering makes cone keys and landmark numbers independent
   * of object insertion order. Four fixed callout ports keep every numbered
   * marker apart; the complete evidenced text lives in normal-flow HTML below
   * (or beside) the plot, where the browser can wrap it without SVG collisions.
   */
  function orderedBeamAssociations(associations) {
    return asArray(associations).slice().sort(function (left, right) {
      var delta = beamExposureCenter(left.exposure) - beamExposureCenter(right.exposure);
      if (Math.abs(delta) > 0.000001) return delta;
      return str(left.exposure.id).localeCompare(str(right.exposure.id));
    });
  }

  function beamCalloutPort(index) {
    return [
      { x: 92, y: 48 },
      { x: 228, y: 48 },
      { x: 228, y: 108 },
      { x: 92, y: 108 }
    ][Math.max(0, Math.min(3, index))];
  }

  function projectBeamCoordinates(anchor, associations) {
    var radius = 6371008.8;
    var points = [];
    associations.forEach(function (association) {
      association.landmarks.forEach(function (landmark) {
        var coordinate = coordinateValue(landmark.coordinates);
        if (!coordinate) return;
        var meanLat = (anchor.lat + coordinate.lat) * Math.PI / 360;
        points.push({
          landmark: landmark,
          east: radius * (coordinate.lng - anchor.lng) * Math.PI / 180 * Math.cos(meanLat),
          north: radius * (coordinate.lat - anchor.lat) * Math.PI / 180
        });
      });
    });
    // A single metres-to-pixels scale preserves bearing and distance ratios.
    // Independent X/Y fitting would turn materially different geographies into
    // the same four-corner diagram and would no longer be a truthful local map.
    var maxRadius = Math.max.apply(Math, [1].concat(points.map(function (point) {
      return Math.sqrt(point.east * point.east + point.north * point.north);
    })));
    var scale = 55 / maxRadius;
    return points.map(function (point) {
      point.x = 160 + point.east * scale;
      point.y = 78 - point.north * scale;
      return point;
    });
  }

  function beamSourceKey(source) {
    return [source.type, source.documentId, source.uri, source.revision].join("|");
  }

  function beamSourceAria(entry, labels, numberFormatter) {
    var source = entry.source;
    var pieces = [
      entry.contexts.join(", "),
      source.label,
      source.documentId ? (labels.documentId || "Document") + " " + source.documentId : "",
      entry.distanceM != null ? numberFormatter.format(entry.distanceM) + " m" : "",
      entry.methodLabel,
      entry.effectiveAt ? (labels.effective || "Effective") + " " + entry.effectiveAt : "",
      entry.caveat
    ].filter(Boolean);
    return pieces.join(". ");
  }

  /**
   * Collect every unique source that materially supports the compact scene.
   * The fixed scene shows at most four controls; the complete collection is
   * available in the paginated fullscreen evidence tool.
   */
  function collectBeamEvidenceSources(scene, labels, numberFormatter) {
    labels = labels || {};
    numberFormatter = numberFormatter && typeof numberFormatter.format === "function"
      ? numberFormatter
      : resolveNumberFormatter({ locale: labels.locale || "en" });
    var index = Object.create(null);
    var records = [];

    function addEnvelope(item, contextLabel, detail) {
      item = item && item.__nlCommercialEvidence === true ? item : evidence(item);
      asArray(item.sources).forEach(function (source) {
        var key = beamSourceKey(source);
        if (!index[key]) {
          index[key] = {
            source: source,
            contexts: [],
            distanceM: detail && detail.distanceM != null ? detail.distanceM : null,
            methodLabel: detail && detail.methodLabel ? detail.methodLabel : "",
            effectiveAt: item.effectiveAt || (detail && detail.effectiveAt) || "",
            caveat: (detail && detail.caveat) || item.caveat || scene.caveat || ""
          };
          records.push(index[key]);
        }
        if (contextLabel && index[key].contexts.indexOf(contextLabel) < 0) {
          index[key].contexts.push(contextLabel);
        }
      });
    }

    if (!scene || scene.state !== "ready") return records;
    addEnvelope(scene.projectAnchor, labels.projectAnchor || "Project anchor", null);
    scene.exposures.forEach(function (association) {
      var exposure = association.exposure;
      var direction = str(exposure.direction.value).toUpperCase();
      var facadeContext = (labels.exposureCone || "Facade sector") + " " + direction;
      addEnvelope(exposure.direction, facadeContext, null);
      addEnvelope(exposure.azimuthStartDeg, facadeContext, null);
      addEnvelope(exposure.azimuthEndDeg, facadeContext, null);
      addEnvelope(exposure.facadeSharePct, facadeContext, null);
      association.landmarks.forEach(function (landmark) {
        var landmarkLabel = str(landmark.label.value);
        var method = str(landmark.distanceMethod.value);
        var methodLabel = labels.distanceMethods && labels.distanceMethods[method]
          ? labels.distanceMethods[method] : method.replace(/_/g, " ");
        var detail = {
          distanceM: finite(landmark.distanceM.value),
          methodLabel: methodLabel,
          effectiveAt: landmark.distanceM.effectiveAt || landmark.coordinates.effectiveAt,
          caveat: landmark.caveat || landmark.distanceM.caveat || landmark.coordinates.caveat || scene.caveat
        };
        [landmark.label, landmark.compactLabel, landmark.coordinates, landmark.distanceM, landmark.distanceMethod, landmark.bearingDeg]
          .forEach(function (item) { addEnvelope(item, landmarkLabel, detail); });
      });
    });
    records.forEach(function (entry) {
      entry.ariaLabel = beamSourceAria(entry, labels, numberFormatter);
    });
    return records;
  }

  function beamEvidencePage(total, requestedPage, pageSize) {
    var size = Math.max(1, Math.min(4, Math.floor(finite(pageSize) || 4)));
    var count = Math.max(0, Math.floor(finite(total) || 0));
    var totalPages = Math.max(1, Math.ceil(count / size));
    var page = Math.max(0, Math.min(totalPages - 1, Math.floor(finite(requestedPage) || 0)));
    return {
      page: page,
      pageSize: size,
      totalPages: totalPages,
      start: page * size,
      end: Math.min(count, page * size + size)
    };
  }

  function numberedSourceLabel(labels, number) {
    return (labels.source || labels.sources || "Source") + " " + number;
  }

  function renderBeamVisual(scene, labels, numberFormatter) {
    if (!scene || scene.state !== "ready" || !scene.exposures || !scene.exposures.length) {
      return (
        '<div class="nl-beam-scene" data-beam-state="unknown">' +
        '<svg viewBox="0 0 320 150" role="img" aria-label="' +
        escapeHtml(labels.beamUnknown || "Orientation scene awaiting verified anchor and facade calibration") +
        '" dir="ltr"><circle class="nl-beam-scene__reference" cx="160" cy="78" r="54"/>' +
        '<line class="nl-beam-scene__reference" x1="160" y1="18" x2="160" y2="138"/>' +
        '<line class="nl-beam-scene__reference" x1="94" y1="78" x2="226" y2="78"/>' +
        '<circle class="nl-beam-scene__anchor nl-beam-scene__anchor--unknown" cx="160" cy="78" r="10"/>' +
        '<text class="nl-beam-scene__north" x="160" y="13" text-anchor="middle">N</text>' +
        "</svg></div>"
      );
    }
    var anchor = coordinateValue(scene.projectAnchor);
    var orderedAssociations = orderedBeamAssociations(scene.exposures);
    var projected = projectBeamCoordinates(anchor, orderedAssociations);
    var projectedById = projected.reduce(function (index, point) {
      index[point.landmark.id] = point;
      return index;
    }, Object.create(null));
    var exposureSlotById = Object.create(null);
    orderedAssociations.forEach(function (association, index) {
      exposureSlotById[association.exposure.id] = index;
    });
    var coneMarkup = orderedAssociations.map(function (association, index) {
      var exposure = association.exposure;
      var direction = str(exposure.direction.value).toUpperCase();
      var title = (labels.exposureCone || "Facade sector") + " " + direction;
      return (
        '<path class="nl-beam-scene__cone" data-exposure-id="' + escapeHtml(exposure.id) +
        '" data-cone-slot="' + index +
        '" data-cone-center-bearing="' + beamExposureCenter(exposure).toFixed(3) +
        '" role="img" aria-label="' + escapeHtml(title) + '" d="' +
        escapeHtml(beamPath(exposure.azimuthStartDeg.value, exposure.azimuthEndDeg.value)) +
        '"><title>' + escapeHtml(title) + "</title></path>"
      );
    }).join("");
    var landmarkRecords = orderedAssociations.reduce(function (records, association) {
      association.landmarks.forEach(function (landmark) {
        var point = projectedById[landmark.id];
        if (!point) return;
        records.push({
          association: association,
          landmark: landmark,
          point: point,
          bearing: normalizedBeamBearing(landmark.bearingDeg.value)
        });
      });
      return records;
    }, []).sort(function (left, right) {
      var delta = left.bearing - right.bearing;
      if (Math.abs(delta) > 0.000001) return delta;
      return str(left.landmark.id).localeCompare(str(right.landmark.id));
    });
    var landmarkMarkup = landmarkRecords.map(function (record, index) {
      var landmark = record.landmark;
      var point = record.point;
      var port = beamCalloutPort(index);
      var slot = exposureSlotById[record.association.exposure.id];
      var label = str(landmark.label.value);
      var distanceLabel = numberFormatter.format(finite(landmark.distanceM.value)) + " m";
      var accessibleLabel = [label, distanceLabel, str(record.association.exposure.direction.value).toUpperCase()]
        .filter(Boolean).join(". ");
      return (
        '<g class="nl-beam-scene__landmark" data-landmark-id="' + escapeHtml(landmark.id) +
        '" data-exposure-id="' + escapeHtml(record.association.exposure.id) +
        '" data-cone-slot="' + slot + '" aria-label="' + escapeHtml(accessibleLabel) + '">' +
        '<title>' + escapeHtml(accessibleLabel) + '</title>' +
        '<line class="nl-beam-scene__leader" data-cone-slot="' + slot + '" x1="' +
        point.x.toFixed(2) + '" y1="' + point.y.toFixed(2) + '" x2="' + port.x +
        '" y2="' + port.y + '"/>' +
        '<circle class="nl-beam-scene__landmark-point" cx="' + point.x.toFixed(2) +
        '" cy="' + point.y.toFixed(2) + '" r="4"/>' +
        '<circle class="nl-beam-scene__callout" data-cone-slot="' + slot + '" cx="' +
        port.x + '" cy="' + port.y + '" r="10"/>' +
        '<text class="nl-beam-scene__callout-number" x="' + port.x + '" y="' +
        (port.y + 5) + '" text-anchor="middle">' + (index + 1) + "</text></g>"
      );
    }).join("");
    var landmarkLegend = landmarkRecords.map(function (record, index) {
      var landmark = record.landmark;
      var exposure = record.association.exposure;
      var slot = exposureSlotById[exposure.id];
      var label = str(landmark.label.value);
      var compactLabel = str(landmark.compactLabel.value);
      var distanceLabel = numberFormatter.format(finite(landmark.distanceM.value)) + " m";
      var legendAria = [label, distanceLabel, str(exposure.direction.value).toUpperCase()].filter(Boolean).join(". ");
      return (
        '<li class="nl-beam-scene__legend-item" data-landmark-id="' + escapeHtml(landmark.id) +
        '" data-exposure-id="' + escapeHtml(exposure.id) + '" data-cone-slot="' + slot +
        '" aria-label="' + escapeHtml(legendAria) + '">' +
        '<span class="nl-beam-scene__legend-index" data-cone-slot="' + slot + '" aria-hidden="true">' +
        (index + 1) + '</span><span class="nl-beam-scene__legend-copy"><bdi class="nl-beam-scene__legend-name">' +
        escapeHtml(compactLabel) + "</bdi></span></li>"
      );
    }).join("");
    var landmarkDistances = landmarkRecords.map(function (record) {
      var landmark = record.landmark;
      var slot = exposureSlotById[record.association.exposure.id];
      return (
        '<bdi class="nl-beam-scene__legend-distance" data-landmark-id="' + escapeHtml(landmark.id) +
        '" data-cone-slot="' + slot + '" aria-label="' +
        escapeHtml(numberFormatter.format(finite(landmark.distanceM.value)) + " m") + '">' +
        escapeHtml(numberFormatter.format(finite(landmark.distanceM.value))) + "</bdi>"
      );
    }).join("");
    var methods = [];
    var shortMethods = [];
    scene.exposures.forEach(function (association) {
      association.landmarks.forEach(function (landmark) {
        var method = str(landmark.distanceMethod.value);
        var label = labels.distanceMethods && labels.distanceMethods[method]
          ? labels.distanceMethods[method] : method.replace(/_/g, " ");
        var shortLabel = labels.distanceMethodsShort && labels.distanceMethodsShort[method]
          ? labels.distanceMethodsShort[method] : label;
        if (methods.indexOf(label) < 0) methods.push(label);
        if (shortMethods.indexOf(shortLabel) < 0) shortMethods.push(shortLabel);
      });
    });
    var methodBadge = shortMethods.length === 1
      ? shortMethods[0]
      : str(labels.methodsCount || "{count} methods").replace("{count}", shortMethods.length);
    methodBadge += " · " + (labels.illustrativeBadge || "Illustrative");
    var methodAria = [
      labels.northUpSchematic || "North-up schematic using evidenced coordinates",
      methods.join(", "),
      scene.caveat || labels.beamIllustrativeCaveat || "Illustrative orientation aid"
    ].filter(Boolean).join(". ");
    var sourceEntries = collectBeamEvidenceSources(scene, labels, numberFormatter);
    var linkedEntries = sourceEntries.map(function (entry, index) {
      return { entry: entry, index: index };
    }).filter(function (item) { return Boolean(item.entry.source.uri); });
    var directLimit = sourceEntries.length > 4 ? 3 : 4;
    var directEntries = linkedEntries.slice(0, directLimit);
    var undisclosedCount = sourceEntries.length - directEntries.length;
    var sourceMarkup = directEntries.map(function (item) {
      return '<a class="nl-beam-scene__source" data-source-index="' + item.index + '" href="' +
        escapeHtml(item.entry.source.uri) + '" target="_blank" rel="noopener noreferrer" aria-label="' +
        escapeHtml((labels.openSource || "Open source") + ". " + item.entry.ariaLabel) + '">' +
        '<span class="nl-beam-scene__source-label nl-beam-scene__source-label--long">' +
        escapeHtml(numberedSourceLabel(labels, item.index + 1)) +
        '</span><span class="nl-beam-scene__source-label nl-beam-scene__source-label--compact" aria-hidden="true">' +
        (item.index + 1) + '</span></a>';
    }).join("");
    if (undisclosedCount > 0) {
      sourceMarkup += '<button class="nl-beam-scene__source nl-beam-scene__source--all" type="button" data-act="open-tool" data-tool="beam-evidence" aria-label="' +
        escapeHtml((labels.allSources || "All sources") + ". " + sourceEntries.length) + '">' +
        '<span class="nl-beam-scene__source-label nl-beam-scene__source-label--long">' +
        escapeHtml((labels.allSources || "All sources") + " (+" + undisclosedCount + ")") +
        '</span><span class="nl-beam-scene__source-label nl-beam-scene__source-label--compact" aria-hidden="true">+' +
        undisclosedCount + '</span></button>';
    }
    var aria = [
      labels.beamScene || "Window orientation scene",
      labels.northUpSchematic || "North-up schematic using evidenced coordinates",
      scene.exposures.map(function (association) {
        return str(association.exposure.direction.value).toUpperCase();
      }).join(", ")
    ].filter(Boolean).join(". ");
    return (
      '<div class="nl-beam-scene" data-beam-state="ready" data-projection="north_up_local_equirectangular_v1" data-source-count="' +
      sourceEntries.length + '"><div class="nl-beam-scene__visual"><div class="nl-beam-scene__plot"><span class="nl-beam-scene__plot-caption"><span class="nl-beam-scene__anchor-key" aria-hidden="true"></span>' +
      escapeHtml(labels.projectHere || "Project") + '</span><svg viewBox="40 0 240 150" preserveAspectRatio="xMidYMid meet" role="img" aria-label="' +
      escapeHtml(aria) + '" dir="ltr"><circle class="nl-beam-scene__reference" cx="160" cy="78" r="54"/>' +
      '<line class="nl-beam-scene__reference" x1="160" y1="18" x2="160" y2="138"/>' +
      '<line class="nl-beam-scene__reference" x1="94" y1="78" x2="226" y2="78"/>' +
      coneMarkup +
      '<circle class="nl-beam-scene__anchor" cx="160" cy="78" r="9" role="img" aria-label="' +
      escapeHtml(labels.projectHere || "Project") + '"><title>' + escapeHtml(labels.projectHere || "Project") +
      "</title></circle>" + landmarkMarkup +
      '<text class="nl-beam-scene__north" x="160" y="55" text-anchor="middle">N</text></svg></div>' +
      '<div class="nl-beam-scene__legend-panel"><ol class="nl-beam-scene__legend" aria-label="' + escapeHtml(labels.beamScene || "Landmarks") +
      '" style="--nl-beam-landmark-count:' + Math.max(1, landmarkRecords.length) + '">' +
      landmarkLegend + '</ol><div class="nl-beam-scene__legend-distances" aria-label="' +
      escapeHtml(labels.beamScene || "Landmark distances") + '">' + landmarkDistances +
      '<span class="nl-beam-scene__legend-unit" aria-hidden="true">m</span></div></div></div>' +
      '<span class="nl-beam-scene__method" aria-label="' + escapeHtml(methodAria) + '">' +
      escapeHtml(methodBadge) +
      '</span><div class="nl-beam-scene__sources" role="group" aria-label="' +
      escapeHtml(labels.sources || "Sources") + '">' + sourceMarkup + '</div></div>'
    );
  }

  function renderExposure(asset, labels, numberFormatter) {
    var exposures = evidence(asset.exposures);
    var beamScene = asset.beamScene || { state: "unknown", caveat: "" };
    var beamVisual = renderBeamVisual(beamScene, labels, numberFormatter);
    if (
      exposures.state === "unknown" ||
      !Array.isArray(exposures.value) ||
      !exposures.value.length ||
      beamScene.state !== "ready"
    ) {
      return (
        '<section class="nl-cds-exposure" data-evidence-state="unknown">' +
        beamVisual +
        '<div><h3>' + escapeHtml(labels.exposureUnknown || "Exposure not yet verified") + "</h3>" +
        '<p>' + escapeHtml(labels.beamUnknownBody || "The map stays neutral until the project anchor and facade azimuth are evidenced. No cone or landmark is guessed.") + "</p>" +
        renderMissingAction("orientation.exposures", exposures, labels) +
        '<small>' + escapeHtml(labels.beamIllustrativeCaveat || "Illustrative orientation aid; request the signed orientation and view pack for reliance.") + "</small>" +
        "</div></section>"
      );
    }
    var summary = exposures.value
      .map(function (entry) {
        var direction = evidence(entry.direction);
        var views = evidence(entry.viewContext);
        var directionText = direction.value == null
          ? labels.directionUnknown || "Direction unknown"
          : str(direction.value).toUpperCase() + " (" + truthLabel(direction, labels) + ")";
        var viewText = "";
        if (views.state === "contradictory") {
          viewText = labels.viewContradictory || "view context contradictory";
        } else if (Array.isArray(views.value) && views.value.length) {
          viewText = views.value.join(", ") + " (" + truthLabel(views, labels) + ")";
        } else {
          viewText = labels.viewUnknown || "view context unknown";
        }
        return directionText + " — " + viewText;
      })
      .join(" · ");
    return (
      '<section class="nl-cds-exposure" data-evidence-state="' + escapeHtml(exposures.state) + '">' +
      beamVisual +
      '<div><h3>' + escapeHtml(labels.exposures || "Facade exposures") + "</h3>" +
      '<p>' + escapeHtml(summary) + "</p>" +
      '<small>' + escapeHtml(evidenceMeta(exposures, labels)) + "</small>" +
      '<small>' + escapeHtml(beamScene.caveat || labels.beamIllustrativeCaveat || "Illustrative orientation aid; not a surveyed view guarantee.") + "</small></div></section>"
    );
  }

  function renderDoor(kind, title, shortTitle, body, availability, labels) {
    availability = evidence(availability);
    var isMissing = availability.state !== "verified" || availability.value !== true;
    var action = isMissing ? "request-tool-data" : "open-tool";
    var stateLabel = truthLabel(availability, labels);
    var actionDescription = isMissing ? labels.requestEvidence || "Request the verified evidence" : body;
    shortTitle = str(shortTitle) || title;
    return (
      '<button class="nl-cds-door" type="button" data-act="' + action + '" data-tool="' + escapeHtml(kind) + '"' +
      ' data-state="' + escapeHtml(availability.state) + '" aria-label="' +
      escapeHtml([title, actionDescription, stateLabel].filter(Boolean).join(". ")) + '">' +
      '<span class="nl-cds-door__title nl-cds-door__title--long" aria-hidden="true">' + escapeHtml(title) + "</span>" +
      '<span class="nl-cds-door__title nl-cds-door__title--short" aria-hidden="true">' + escapeHtml(shortTitle) + "</span>" +
      '<span class="nl-cds-door__body" aria-hidden="true">' + escapeHtml(actionDescription) + "</span>" +
      '<span class="nl-cds-door__state nl-cds-door__state--long" aria-hidden="true">' + escapeHtml(stateLabel) + "</span>" +
      '<span class="nl-cds-door__state nl-cds-door__state--short" aria-hidden="true"></span>' +
      "</button>"
    );
  }

  function renderDecisionSurface(asset, labels, options) {
    asset = asset && typeof asset === "object" ? asset : {};
    if (asset.__nlCommercialAsset !== true) {
      throw new Error("Use NadlanCommercialContractAdapter before rendering a commercial asset.");
    }
    labels = labels || {};
    options = options || {};
    var locale = normalizeLocale(options.locale || labels.locale);
    var direction = logicalDirection(locale, options.dir || labels.dir);
    var numberFormatter = resolveNumberFormatter({
      locale: locale,
      numberFormatter: options.numberFormatter,
      numberFormatOptions: options.numberFormatOptions
    });
    var availability = evidence(asset.availability);
    var status = statusClass(str(availability.value));
    var facts = [
      {
        fieldId: "area.rentable_sqm",
        label: labels.rentableArea || "Rentable area",
        evidence: asset.rentableArea,
        formatter: function (value) { return formatLocalizedNumber(value, numberFormatter) + " m²"; }
      },
      {
        fieldId: "fitout.planning_capacity",
        label: labels.planningCapacity || "Planning capacity",
        evidence: asset.planningCapacity,
        formatter: function (value) { return formatLocalizedNumber(value, numberFormatter) + " " + (labels.people || "people"); }
      },
      {
        fieldId: "commercial.monthly_all_in",
        label: labels.allInCost || "Monthly all-in cost",
        evidence: asset.monthlyAllIn,
        formatter: function (value) { return str(value); }
      }
    ];
    var identity = [asset.projectName, asset.towerLabel, asset.floorLabel, asset.spaceLabel].filter(Boolean).join(" · ");

    return (
      '<section class="nl-cds" lang="' + escapeHtml(locale) + '" dir="' + escapeHtml(direction) +
      '" data-asset-type="commercial_office" data-asset-id="' + escapeHtml(asset.id) + '">' +
      '<header class="nl-cds-head"><button type="button" class="nl-cds-back" data-act="back-to-building"><span class="nl-cds-back__icon" aria-hidden="true">' +
      escapeHtml(logicalBackIcon(direction)) + '</span><span class="nl-cds-back__label">' +
      escapeHtml(labels.backToBuilding || "Building") + "</span></button>" +
      '<div><p class="nl-cds-eyebrow">' + escapeHtml(labels.selectedOffice || "Your selected office space") + "</p>" +
      '<h2 id="nl-cds-title">' + escapeHtml(identity || labels.unidentifiedAsset || "Selected space") + "</h2>" +
      '<p class="nl-cds-status" data-status="' + escapeHtml(status) + '"><span>' +
      escapeHtml((labels.status && labels.status[status]) || status.replace(/_/g, " ")) + "</span>" +
      '<small>' + escapeHtml(evidenceMeta(availability, labels)) + "</small></p></div></header>" +
      renderExposure(asset, labels, numberFormatter) +
      '<div class="nl-cds-facts">' + facts.map(function (fact) { return renderEvidenceFact(fact, labels); }).join("") + "</div>" +
      '<div class="nl-cds-doors" aria-label="' + escapeHtml(labels.evidenceTools || "Evidence tools") + '">' +
      renderDoor("floor-pack", labels.floorPack || "Floor pack", labels.floorPackShort || "Floor pack", labels.floorPackBody || "Plan, area, core and documents", asset.floorPackAvailable, labels) +
      renderDoor("fit-out", labels.fitOut || "Fit-out & infrastructure", labels.fitOutShort || "Fit-out", labels.fitOutBody || "Capacity, MEP, telecoms and delivery", asset.fitOutAvailable, labels) +
      renderDoor("context", labels.context || "Commute & area", labels.contextShort || "Area", labels.contextBody || "Routes, daily life, market and risk", asset.contextAvailable, labels) +
      renderDoor("cost", labels.cost || "Cost & records", labels.costShort || "Full cost", labels.costBody || "All-in cost, compare, comps and evidence", asset.costAvailable, labels) +
      "</div>" +
      '<div class="nl-cds-actions" role="group" aria-label="' + escapeHtml(labels.actions || "Actions") + '">' +
      '<button type="button" data-act="save">' + escapeHtml(labels.save || "Save") + "</button>" +
      '<button type="button" data-act="open-tool" data-tool="compare">' + escapeHtml(labels.compare || "Compare") + "</button>" +
      '<button type="button" data-act="share">' + escapeHtml(labels.share || "Share") + "</button></div>" +
      '<button class="nl-cds-cta" type="button" data-act="open-tool" data-tool="inquiry">' +
      escapeHtml((labels.askAbout || "Ask about") + " " + (asset.floorLabel || labels.thisSpace || "this space")) +
      "</button></section>"
    );
  }

  function firstFocusable(root) {
    return root.querySelector(
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
  }

  function isTrustedToolNode(value) {
    return Boolean(window.Node) && value instanceof window.Node;
  }

  function focusables(root) {
    return Array.prototype.slice.call(
      root.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    ).filter(function (node) {
      var style = window.getComputedStyle(node);
      return style.display !== "none" && style.visibility !== "hidden" && node.getClientRects().length > 0;
    });
  }

  function lockDocument(state) {
    var html = document.documentElement;
    var body = document.body;
    state.scrollY = window.scrollY;
    state.htmlOverflow = html.style.overflow;
    state.bodyOverflow = body.style.overflow;
    state.bodyPosition = body.style.position;
    state.bodyTop = body.style.top;
    state.bodyWidth = body.style.width;
    html.style.overflow = "hidden";
    body.style.overflow = "hidden";
    body.style.position = "fixed";
    body.style.top = -state.scrollY + "px";
    body.style.width = "100%";
  }

  function unlockDocument(state) {
    var html = document.documentElement;
    var body = document.body;
    html.style.overflow = state.htmlOverflow || "";
    body.style.overflow = state.bodyOverflow || "";
    body.style.position = state.bodyPosition || "";
    body.style.top = state.bodyTop || "";
    body.style.width = state.bodyWidth || "";
    var prior = html.style.scrollBehavior;
    html.style.scrollBehavior = "auto";
    window.scrollTo(0, Number(state.scrollY) || 0);
    html.style.scrollBehavior = prior;
  }

  function toolTitle(kind, labels) {
    var map = {
      "floor-pack": labels.floorPack || "Floor pack",
      "fit-out": labels.fitOut || "Fit-out & infrastructure",
      context: labels.context || "Commute & area",
      cost: labels.cost || "Cost & records",
      compare: labels.compare || "Compare spaces",
      inquiry: labels.inquiry || "Ask about this space",
      "beam-evidence": labels.beamEvidenceTitle || "Orientation sources"
    };
    return map[kind] || kind;
  }

  var TOOL_HISTORY_VERSION = 1;
  var ASSET_ROUTE_VERSION = 1;
  var ASSET_ROUTE_EVENT = "nadlan:commercial-asset-route-change";
  var TOOL_HISTORY_FIELDS = [
    "buildingId",
    "floorId",
    "projectContractId",
    "suiteId",
    "tool",
    "towerId",
    "version",
    "wpPostId"
  ];
  var ASSET_ROUTE_FIELDS = [
    "buildingId",
    "floorId",
    "projectContractId",
    "suiteId",
    "towerId",
    "version",
    "wpPostId"
  ];

  function toolHistoryIdentity(asset) {
    asset = isObject(asset) ? asset : {};
    var wpPostId = finite(asset.wpPostId);
    var suiteId = asset.suiteId == null || str(asset.suiteId).trim() === ""
      ? null
      : contractId(asset.suiteId);
    var identity = {
      wpPostId: wpPostId,
      projectContractId: contractId(asset.projectId),
      buildingId: contractId(asset.buildingId),
      towerId: contractId(asset.towerId),
      floorId: contractId(asset.floorId),
      suiteId: suiteId
    };
    if (
      !Number.isInteger(wpPostId) ||
      wpPostId <= 0 ||
      !identity.projectContractId ||
      !identity.buildingId ||
      !identity.towerId ||
      !identity.floorId ||
      (asset.suiteId != null && str(asset.suiteId).trim() !== "" && !identity.suiteId)
    ) {
      return null;
    }
    return identity;
  }

  function createToolHistoryMarker(kind, asset) {
    if (TOOL_KINDS.indexOf(kind) < 0) return null;
    var identity = toolHistoryIdentity(asset);
    if (!identity) return null;
    return {
      version: TOOL_HISTORY_VERSION,
      tool: kind,
      wpPostId: identity.wpPostId,
      projectContractId: identity.projectContractId,
      buildingId: identity.buildingId,
      towerId: identity.towerId,
      floorId: identity.floorId,
      suiteId: identity.suiteId
    };
  }

  function normalizeToolHistoryMarker(state) {
    if (!isObject(state) || !isObject(state.nlCommercialTool)) return null;
    var raw = state.nlCommercialTool;
    var fields = Object.keys(raw).sort();
    if (JSON.stringify(fields) !== JSON.stringify(TOOL_HISTORY_FIELDS)) return null;
    if (raw.version !== TOOL_HISTORY_VERSION || TOOL_KINDS.indexOf(raw.tool) < 0) return null;
    if (typeof raw.wpPostId !== "number" || !Number.isInteger(raw.wpPostId) || raw.wpPostId <= 0) return null;

    var projectContractId = contractId(raw.projectContractId);
    var buildingId = contractId(raw.buildingId);
    var towerId = contractId(raw.towerId);
    var floorId = contractId(raw.floorId);
    var suiteId = raw.suiteId === null ? null : contractId(raw.suiteId);
    if (
      !projectContractId || projectContractId !== raw.projectContractId ||
      !buildingId || buildingId !== raw.buildingId ||
      !towerId || towerId !== raw.towerId ||
      !floorId || floorId !== raw.floorId ||
      (raw.suiteId !== null && (!suiteId || suiteId !== raw.suiteId))
    ) {
      return null;
    }
    return {
      version: TOOL_HISTORY_VERSION,
      tool: raw.tool,
      wpPostId: raw.wpPostId,
      projectContractId: projectContractId,
      buildingId: buildingId,
      towerId: towerId,
      floorId: floorId,
      suiteId: suiteId
    };
  }

  function toolHistoryMarkerMatchesAsset(marker, asset) {
    var identity = toolHistoryIdentity(asset);
    return Boolean(
      marker && identity &&
      marker.wpPostId === identity.wpPostId &&
      marker.projectContractId === identity.projectContractId &&
      marker.buildingId === identity.buildingId &&
      marker.towerId === identity.towerId &&
      marker.floorId === identity.floorId &&
      marker.suiteId === identity.suiteId
    );
  }

  function createCommercialAssetRouteMarker(asset) {
    var identity = toolHistoryIdentity(asset);
    if (!identity) return null;
    return {
      version: ASSET_ROUTE_VERSION,
      wpPostId: identity.wpPostId,
      projectContractId: identity.projectContractId,
      buildingId: identity.buildingId,
      towerId: identity.towerId,
      floorId: identity.floorId,
      suiteId: identity.suiteId
    };
  }

  function normalizeCommercialAssetRouteMarker(state) {
    if (!isObject(state) || !isObject(state.nlCommercialAsset)) return null;
    var raw = state.nlCommercialAsset;
    if (JSON.stringify(Object.keys(raw).sort()) !== JSON.stringify(ASSET_ROUTE_FIELDS)) return null;
    if (raw.version !== ASSET_ROUTE_VERSION) return null;
    var identity = toolHistoryIdentity({
      wpPostId: raw.wpPostId,
      projectId: raw.projectContractId,
      buildingId: raw.buildingId,
      towerId: raw.towerId,
      floorId: raw.floorId,
      suiteId: raw.suiteId
    });
    if (!identity) return null;
    var normalized = createCommercialAssetRouteMarker({
      wpPostId: identity.wpPostId,
      projectId: identity.projectContractId,
      buildingId: identity.buildingId,
      towerId: identity.towerId,
      floorId: identity.floorId,
      suiteId: identity.suiteId
    });
    return normalized && ASSET_ROUTE_FIELDS.every(function (field) {
      return normalized[field] === raw[field];
    }) ? normalized : null;
  }

  function commercialAssetRouteMarkerMatchesAsset(marker, asset) {
    var identity = createCommercialAssetRouteMarker(asset);
    return Boolean(
      marker && identity &&
      marker.wpPostId === identity.wpPostId &&
      marker.projectContractId === identity.projectContractId &&
      marker.buildingId === identity.buildingId &&
      marker.towerId === identity.towerId &&
      marker.floorId === identity.floorId &&
      marker.suiteId === identity.suiteId
    );
  }

  function parseCommercialAssetRoute(urlValue) {
    var names = ["project_contract_id", "building_id", "tower_id", "floor_id", "suite_id"];
    var url;
    try {
      url = new URL(str(urlValue), window.location && window.location.href ? window.location.href : undefined);
    } catch (error) {
      return { present: true, valid: false, identityKey: "" };
    }
    var present = names.some(function (name) { return url.searchParams.has(name); });
    if (!present) return { present: false, valid: true, identityKey: "" };
    var values = {};
    for (var index = 0; index < names.length; index += 1) {
      var name = names[index];
      var all = url.searchParams.getAll(name);
      if (all.length > 1) return { present: true, valid: false, identityKey: "" };
      values[name] = all.length ? all[0] : null;
    }
    if (
      values.project_contract_id == null || values.building_id == null ||
      values.tower_id == null || values.floor_id == null
    ) {
      return { present: true, valid: false, identityKey: "" };
    }
    var projectContractId = contractId(values.project_contract_id);
    var buildingId = contractId(values.building_id);
    var towerId = contractId(values.tower_id);
    var floorId = contractId(values.floor_id);
    var suiteId = values.suite_id == null ? null : contractId(values.suite_id);
    if (
      !projectContractId || projectContractId !== values.project_contract_id ||
      !buildingId || buildingId !== values.building_id ||
      !towerId || towerId !== values.tower_id ||
      !floorId || floorId !== values.floor_id ||
      (values.suite_id != null && (!suiteId || suiteId !== values.suite_id))
    ) {
      return { present: true, valid: false, identityKey: "" };
    }
    return {
      present: true,
      valid: true,
      projectContractId: projectContractId,
      buildingId: buildingId,
      towerId: towerId,
      floorId: floorId,
      suiteId: suiteId,
      identityKey: commercialIdentityKey(buildingId, towerId, floorId, suiteId),
      originPath: url.origin + url.pathname
    };
  }

  function commercialAssetRouteMatchesAsset(route, asset) {
    if (!route || !route.present || !route.valid || !asset || asset.__nlCommercialAsset !== true) return false;
    if (asset.selectable !== true) return false;
    var marker = createCommercialAssetRouteMarker(asset);
    if (
      !marker || route.projectContractId !== marker.projectContractId ||
      route.buildingId !== marker.buildingId || route.towerId !== marker.towerId ||
      route.floorId !== marker.floorId || route.suiteId !== marker.suiteId
    ) {
      return false;
    }
    try {
      var canonical = new URL(asset.url);
      return route.originPath === canonical.origin + canonical.pathname;
    } catch (error) {
      return false;
    }
  }

  function stripToolHistoryState(state) {
    var clean = {};
    if (!isObject(state)) return clean;
    Object.keys(state).forEach(function (key) {
      if (key !== "nlCommercialTool") clean[key] = state[key];
    });
    return clean;
  }

  function stripCommercialAssetRouteState(state) {
    var clean = {};
    if (!isObject(state)) return clean;
    Object.keys(state).forEach(function (key) {
      if (key !== "nlCommercialAsset" && key !== "nlCommercialTool") clean[key] = state[key];
    });
    return clean;
  }

  function CommercialToolDialog(options) {
    options = options || {};
    this.root = options.root;
    this.labels = options.labels || {};
    this.locale = normalizeLocale(options.locale || this.labels.locale);
    this.dir = logicalDirection(this.locale, options.dir || this.labels.dir);
    var defaultLabels = this.labels;
    this.renderTool =
      typeof options.renderTool === "function"
        ? options.renderTool
        : function (kind, asset) {
            return defaultToolNode(kind, asset, defaultLabels);
          };
    this.onRequestField =
      typeof options.onRequestField === "function" ? options.onRequestField : function () {};
    this.onClosed = typeof options.onClosed === "function" ? options.onClosed : function () {};
    this.dialog = null;
    this.kind = "";
    this.asset = null;
    this.trigger = null;
    this.lockState = {};
    this.abortController = null;
    this.historyAbortController = new AbortController();
    this.toolCleanup = null;
    this.rootInertBefore = false;
    this.historyMarker = "nlCommercialTool";
    this.getCurrentAsset =
      typeof options.getCurrentAsset === "function" ? options.getCurrentAsset : function () { return null; };
    var self = this;
    window.addEventListener(
      "popstate",
      function (event) { self.handlePopState(event); },
      { signal: this.historyAbortController.signal }
    );
  }

  CommercialToolDialog.prototype.open = function open(kind, asset, trigger, options) {
    options = options || {};
    if (TOOL_KINDS.indexOf(kind) < 0) throw new Error("Unsupported commercial tool: " + kind);
    if (this.dialog) this.close({ history: false, focus: false });
    var opener = trigger || document.activeElement;
    var abortController = new AbortController();
    var signal = abortController.signal;
    var dialog = null;
    var cleanup = null;
    var lockState = {};
    var locked = false;
    var rootInertBefore = this.root ? Boolean(this.root.inert) : false;
    var marker = null;
    if (!options.fromHistory) {
      marker = createToolHistoryMarker(kind, asset);
      if (!marker) {
        abortController.abort();
        throw new Error("Commercial tool history requires the exact immutable project/building/tower/floor/suite identity.");
      }
    }

    try {
      dialog = document.createElement("dialog");
      dialog.className = "nl-commercial-tool nl-commercial-tool--" + safeId(kind);
      dialog.id = "nl-commercial-tool";
      dialog.lang = this.locale;
      dialog.dir = this.dir;
      dialog.setAttribute("aria-labelledby", "nl-commercial-tool-title");
      dialog.innerHTML =
        '<div class="nl-commercial-tool__head"><button type="button" data-act="close-tool"><span class="nl-tool-back__icon" aria-hidden="true">' +
        escapeHtml(logicalBackIcon(this.dir)) + '</span><span>' +
        escapeHtml(this.labels.back || "Back") +
        '</span></button><div><p>' +
        escapeHtml([asset.projectName, asset.towerLabel, asset.floorLabel, asset.spaceLabel].filter(Boolean).join(" · ")) +
        '</p><h2 id="nl-commercial-tool-title">' + escapeHtml(toolTitle(kind, this.labels)) +
        '</h2></div></div><div class="nl-commercial-tool__body" data-role="tool-body"></div>';
      // Orientation provenance is a built-in safe/paginated surface. A custom
      // renderer cannot replace it with an unbounded or incomplete source list.
      var renderedTool = kind === "beam-evidence"
        ? defaultToolNode(kind, asset, this.labels)
        : this.renderTool(kind, asset, options);
      if (!isTrustedToolNode(renderedTool)) {
        throw new TypeError(
          "renderTool must return a trusted DOM Node or DocumentFragment; HTML strings are rejected."
        );
      }
      cleanup = typeof renderedTool.__nlToolDestroy === "function"
        ? renderedTool.__nlToolDestroy
        : null;
      dialog.querySelector('[data-role="tool-body"]').replaceChildren(renderedTool);
      document.body.appendChild(dialog);

      this.dialog = dialog;
      this.kind = kind;
      this.asset = asset;
      this.trigger = opener;
      this.abortController = abortController;
      this.toolCleanup = cleanup;
      this.lockState = lockState;
      this.rootInertBefore = rootInertBefore;

      locked = true;
      lockDocument(lockState);
      if (this.root) this.root.inert = true;

      var self = this;
      dialog.querySelector('[data-act="close-tool"]').addEventListener(
        "click",
        function () { self.close({ history: true, focus: true }); },
        { signal: signal }
      );
      dialog.addEventListener(
        "click",
        function (event) {
          var control = event.target.closest('[data-act="request-field"]');
          if (!control || !dialog.contains(control)) return;
          self.onRequestField(control.dataset.fieldId, asset, control);
        },
        { signal: signal }
      );
      dialog.addEventListener(
        "cancel",
        function (event) {
          event.preventDefault();
          self.close({ history: true, focus: true });
        },
        { signal: signal }
      );
      dialog.addEventListener(
        "close",
        function () {
          if (self.dialog === dialog) self.finishClose(true);
        },
        { signal: signal }
      );
      dialog.addEventListener(
        "keydown",
        function (event) { self.trapFocus(event); },
        { signal: signal }
      );

      dialog.showModal();
      if (marker) {
        var nextState = stripToolHistoryState(history.state);
        nextState.nlCommercialTool = marker;
        history.pushState(nextState, "", window.location.href);
      }
      window.requestAnimationFrame(function () {
        var target = firstFocusable(dialog);
        if (target) target.focus({ preventScroll: true });
      });
    } catch (error) {
      this.dialog = null;
      this.kind = "";
      this.asset = null;
      this.trigger = null;
      this.abortController = null;
      this.toolCleanup = null;
      this.lockState = {};
      this.rootInertBefore = false;
      try { abortController.abort(); } catch (abortError) {}
      try { if (cleanup) cleanup(); } catch (cleanupError) {}
      try { if (dialog && dialog.open) dialog.close(); } catch (closeError) {}
      try { if (dialog) dialog.remove(); } catch (removeError) {}
      try { if (this.root) this.root.inert = rootInertBefore; } catch (inertError) {}
      try { if (locked) unlockDocument(lockState); } catch (unlockError) {}
      if (opener && opener.isConnected && typeof opener.focus === "function") {
        window.requestAnimationFrame(function () { opener.focus({ preventScroll: true }); });
      }
      throw error;
    }
  };

  CommercialToolDialog.prototype.findHistoryTrigger = function findHistoryTrigger(kind) {
    if (!this.root || typeof this.root.querySelectorAll !== "function") return null;
    var controls = Array.prototype.slice.call(this.root.querySelectorAll("[data-act][data-tool]"));
    for (var index = 0; index < controls.length; index += 1) {
      if (controls[index].dataset.tool === kind && controls[index].dataset.act === "open-tool") return controls[index];
    }
    return null;
  };

  CommercialToolDialog.prototype.replaceHistoryStateWithoutTool = function replaceHistoryStateWithoutTool(state) {
    try {
      history.replaceState(stripToolHistoryState(state), "", window.location.href);
      return true;
    } catch (error) {
      return false;
    }
  };

  CommercialToolDialog.prototype.handlePopState = function handlePopState(event) {
    var state = event && event.state;
    var hasRawMarker = isObject(state) && Object.prototype.hasOwnProperty.call(state, this.historyMarker);
    var marker = normalizeToolHistoryMarker(state);
    if (!marker) {
      if (hasRawMarker) this.replaceHistoryStateWithoutTool(state);
      if (this.dialog) this.finishClose(true);
      return;
    }

    var currentAsset = this.getCurrentAsset();
    if (!toolHistoryMarkerMatchesAsset(marker, currentAsset)) {
      if (this.dialog) this.finishClose(true);
      this.replaceHistoryStateWithoutTool(state);
      return;
    }

    if (
      this.dialog &&
      this.kind === marker.tool &&
      toolHistoryMarkerMatchesAsset(marker, this.asset)
    ) {
      return;
    }
    if (this.dialog) this.finishClose(false);
    try {
      this.open(marker.tool, currentAsset, this.findHistoryTrigger(marker.tool), { fromHistory: true });
    } catch (error) {
      this.replaceHistoryStateWithoutTool(state);
    }
  };

  CommercialToolDialog.prototype.trapFocus = function trapFocus(event) {
    if (event.key !== "Tab" || !this.dialog) return;
    var items = focusables(this.dialog);
    if (!items.length) {
      event.preventDefault();
      return;
    }
    var first = items[0];
    var last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  };

  CommercialToolDialog.prototype.close = function close(options) {
    options = options || {};
    if (!this.dialog) return;
    var marker = normalizeToolHistoryMarker(history.state);
    if (
      options.history &&
      marker &&
      marker.tool === this.kind &&
      toolHistoryMarkerMatchesAsset(marker, this.asset)
    ) {
      try {
        history.back();
        return;
      } catch (error) {
        this.replaceHistoryStateWithoutTool(history.state);
      }
    }
    if (options.history && isObject(history.state) && Object.prototype.hasOwnProperty.call(history.state, this.historyMarker)) {
      this.replaceHistoryStateWithoutTool(history.state);
    }
    this.finishClose(options.focus !== false);
  };

  CommercialToolDialog.prototype.finishClose = function finishClose(restoreFocus) {
    var dialog = this.dialog;
    var trigger = this.trigger;
    var kind = this.kind;
    var cleanup = this.toolCleanup;
    var abortController = this.abortController;
    var lockState = this.lockState;
    var rootInertBefore = this.rootInertBefore;
    this.dialog = null;
    this.kind = "";
    this.asset = null;
    this.trigger = null;
    this.abortController = null;
    this.toolCleanup = null;
    this.lockState = {};
    this.rootInertBefore = false;
    try { if (abortController) abortController.abort(); } catch (abortError) {}
    try { if (cleanup) cleanup(); } catch (cleanupError) {}
    try { if (dialog && dialog.open) dialog.close(); } catch (closeError) {}
    try { if (dialog) dialog.remove(); } catch (removeError) {}
    try { if (this.root) this.root.inert = rootInertBefore; } catch (inertError) {}
    try { unlockDocument(lockState); } catch (unlockError) {}
    if (restoreFocus && trigger && trigger.isConnected) {
      window.requestAnimationFrame(function () { trigger.focus({ preventScroll: true }); });
    }
    try { this.onClosed(kind); } catch (closedError) {}
  };

  CommercialToolDialog.prototype.destroy = function destroy() {
    try {
      if (isObject(history.state) && Object.prototype.hasOwnProperty.call(history.state, this.historyMarker)) {
        this.replaceHistoryStateWithoutTool(history.state);
      }
    } finally {
      if (this.dialog) this.finishClose(false);
      try { if (this.abortController) this.abortController.abort(); } catch (abortError) {}
      this.abortController = null;
      try { if (this.historyAbortController) this.historyAbortController.abort(); } catch (historyAbortError) {}
      this.historyAbortController = null;
    }
  };

  function createNode(tag, className, textValue) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (textValue != null) node.textContent = str(textValue);
    return node;
  }

  function requestButton(label, fieldId) {
    var button = createNode("button", "", label);
    button.type = "button";
    button.dataset.act = "request-field";
    button.dataset.fieldId = fieldId;
    return button;
  }

  function beamEvidencePageSize() {
    var width = finite(window.innerWidth) || 1280;
    var height = finite(window.innerHeight) || 800;
    if (height <= 600) return 1;
    return width < 960 ? 2 : 4;
  }

  function createBeamEvidenceNode(asset, labels) {
    labels = labels || {};
    var section = createNode("section", "nl-beam-evidence");
    var numberFormatter = resolveNumberFormatter({ locale: labels.locale || "en" });
    var sources = collectBeamEvidenceSources(asset.beamScene, labels, numberFormatter);
    var heading = createNode("h3", "", labels.beamEvidenceTitle || "Orientation sources");
    var summary = createNode(
      "p",
      "nl-beam-evidence__summary",
      (labels.sources || "Sources") + ": " + numberFormatter.format(sources.length)
    );
    var list = createNode("div", "nl-beam-evidence__list");
    list.setAttribute("aria-live", "polite");
    var navigation = createNode("div", "nl-beam-evidence__pagination");
    var previous = createNode("button", "", labels.previous || "Previous");
    var status = createNode("span", "", "");
    var next = createNode("button", "", labels.next || "Next");
    previous.type = "button";
    next.type = "button";
    navigation.setAttribute("aria-label", labels.beamEvidencePagination || labels.sources || "Source pages");
    status.setAttribute("aria-live", "polite");
    navigation.appendChild(previous);
    navigation.appendChild(status);
    navigation.appendChild(next);
    section.appendChild(heading);
    section.appendChild(summary);
    section.appendChild(list);
    section.appendChild(navigation);
    section.dataset.sourceCount = str(sources.length);
    var page = 0;

    function sourceRecord(entry, index) {
      var source = entry.source;
      var article = createNode("article", "nl-beam-evidence__record");
      article.dataset.sourceIndex = str(index);
      article.appendChild(createNode("h4", "", numberedSourceLabel(labels, index + 1) + " · " + source.label));
      article.appendChild(createNode("p", "", entry.contexts.join(", ")));
      article.appendChild(
        createNode(
          "small",
          "",
          [entry.methodLabel, entry.distanceM != null ? numberFormatter.format(entry.distanceM) + " m" : "", entry.effectiveAt]
            .filter(Boolean).join(" · ")
        )
      );
      if (entry.caveat) article.appendChild(createNode("small", "", entry.caveat));
      if (source.uri) {
        var link = createNode("a", "", labels.openSource || "Open source");
        link.setAttribute("href", source.uri);
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", "noopener noreferrer");
        link.setAttribute("aria-label", entry.ariaLabel);
        article.appendChild(link);
      } else {
        article.appendChild(
          createNode("span", "nl-beam-evidence__document", (labels.documentId || "Document") + " " + source.documentId)
        );
        article.appendChild(
          requestButton(
            labels.requestSource || "Request this source record",
            "orientation.source." + (source.documentId || "unlinked")
          )
        );
      }
      return article;
    }

    function renderPage() {
      var bounds = beamEvidencePage(sources.length, page, beamEvidencePageSize());
      page = bounds.page;
      list.replaceChildren();
      sources.slice(bounds.start, bounds.end).forEach(function (entry, offset) {
        list.appendChild(sourceRecord(entry, bounds.start + offset));
      });
      status.textContent = (labels.page || "Page") + " " + (bounds.page + 1) + " / " + bounds.totalPages;
      previous.disabled = bounds.page <= 0;
      next.disabled = bounds.page >= bounds.totalPages - 1;
      section.dataset.pageSize = str(bounds.pageSize);
      section.dataset.page = str(bounds.page);
    }

    previous.addEventListener("click", function () { page -= 1; renderPage(); });
    next.addEventListener("click", function () { page += 1; renderPage(); });
    var onResize = function () { renderPage(); };
    if (typeof window.addEventListener === "function") window.addEventListener("resize", onResize);
    section.__nlToolDestroy = function () {
      if (typeof window.removeEventListener === "function") window.removeEventListener("resize", onResize);
    };
    renderPage();
    return section;
  }

  /**
   * Safe built-in tool renderer. Custom renderTool callbacks must follow the
   * same boundary and return a Node/DocumentFragment created by the current
   * document. Callback HTML strings are never inserted.
   */
  function defaultToolNode(kind, asset, labels) {
    labels = labels || {};
    if (kind === "beam-evidence") return createBeamEvidenceNode(asset, labels);
    if (
      kind === "inquiry" &&
      window.NadlanCommercialRfpComposer &&
      typeof window.NadlanCommercialRfpComposer.createNode === "function"
    ) {
      var rfpConfig = window.NadlanCommercialRfpConfig || {};
      return window.NadlanCommercialRfpComposer.createNode({
        asset: asset,
        labels: labels,
        locale: labels.locale,
        endpoint: rfpConfig.endpoint,
        environment: rfpConfig.environment,
        sandboxPostId: rfpConfig.sandboxPostId,
        sandboxNonce: rfpConfig.sandboxNonce,
        consentVersion: rfpConfig.consentVersion
      });
    }
    var section = createNode("section", "nl-tool-page");
    var title = toolTitle(kind, labels);
    section.appendChild(createNode("h3", "", title));

    if (kind === "floor-pack") {
      var empty = createNode("div", "nl-tool-empty");
      empty.appendChild(
        createNode("p", "", labels.noFloorPack || "No verified floor pack is attached.")
      );
      empty.appendChild(
        requestButton(
          labels.requestFloorPack || "Request the verified floor pack",
          "floor_pack.current"
        )
      );
      section.appendChild(empty);
      return section;
    }

    if (kind === "fit-out") {
      var grid = createNode("div", "nl-tool-grid");
      [
        { id: "capacity", fallback: "Capacity" },
        { id: "hvac", fallback: "HVAC" },
        { id: "power_backup", fallback: "Power & backup" },
        { id: "fiber", fallback: "Fiber" },
        { id: "lifts_loading", fallback: "Lifts & loading" },
        { id: "accessibility", fallback: "Accessibility" }
      ].forEach(
        function (topic) {
          var topicLabels = labels.fitOutTopics || {};
          var name = topicLabels[topic.id] || topic.fallback;
          var button = requestButton("", "infrastructure." + topic.id);
          button.appendChild(createNode("strong", "", name));
          button.appendChild(
            createNode(
              "span",
              "",
              labels.notVerified || "Not yet verified — ask this question"
            )
          );
          grid.appendChild(button);
        }
      );
      section.appendChild(grid);
      return section;
    }

    if (kind === "context") {
      var contextRequired = createNode("div", "nl-tool-empty");
      contextRequired.dataset.state = "adapter-required";
      contextRequired.appendChild(
        createNode(
          "p",
          "",
          labels.contextAdapterRequired ||
            "No evidence-backed context map is connected for this space yet."
        )
      );
      contextRequired.appendChild(
        requestButton(
          labels.requestContextPack || "Request the verified location and commute pack",
          "context.verified_pack"
        )
      );
      section.appendChild(contextRequired);
      return section;
    }

    if (kind === "cost") {
      section.appendChild(
        createNode(
          "p",
          "",
          labels.costUnknown ||
            "No verified commercial terms are attached. Build an estimate only after each assumption is visible."
        )
      );
      section.appendChild(
        requestButton(
          labels.requestTerms || "Request the full commercial schedule",
          "commercial.full_cost_schedule"
        )
      );
      return section;
    }

    if (kind === "compare") {
      section.appendChild(
        createNode(
          "p",
          "",
          labels.compareHelp ||
            "Compare availability, area basis, capacity, all-in cost, infrastructure, commute and unresolved questions."
        )
      );
      return section;
    }

    section.appendChild(
      createNode(
        "p",
        "",
        labels.inquiryHelp ||
          "Your selected floor and open questions will be attached automatically."
      )
    );
    return section;
  }

  function CommercialDecisionController(options) {
    options = options || {};
    if (!options.root) throw new Error("root is required");
    this.root = options.root;
    this.labels = options.labels || {};
    this.locale = normalizeLocale(options.locale || this.labels.locale);
    this.dir = logicalDirection(this.locale, options.dir || this.labels.dir);
    this.numberFormatter = resolveNumberFormatter({
      locale: this.locale,
      numberFormatter: options.numberFormatter,
      numberFormatOptions: options.numberFormatOptions
    });
    this.resolveAsset = typeof options.resolveAsset === "function" ? options.resolveAsset : function () { return null; };
    this.onRequestField = typeof options.onRequestField === "function" ? options.onRequestField : function () {};
    this.onSave = typeof options.onSave === "function" ? options.onSave : function () {};
    this.onShare = typeof options.onShare === "function" ? options.onShare : function () {};
    this.onBack = typeof options.onBack === "function" ? options.onBack : function () {};
    this.asset = null;
    this.abortController = null;
    var controller = this;
    this.toolDialog = new CommercialToolDialog({
      root: this.root,
      labels: this.labels,
      locale: this.locale,
      dir: this.dir,
      renderTool:
        options.renderTool ||
        function (kind, asset) {
          return defaultToolNode(kind, asset, options.labels || {});
        },
      onRequestField: this.onRequestField,
      onClosed: options.onToolClosed,
      getCurrentAsset: function () { return controller.asset; }
    });
  }

  CommercialDecisionController.prototype.render = function render(assetOrId) {
    var nextAsset = typeof assetOrId === "object" ? assetOrId : this.resolveAsset(assetOrId);
    if (!nextAsset || nextAsset.__nlCommercialAsset !== true) {
      throw new Error("Unknown or unadapted commercial asset");
    }
    // Compute all potentially throwing presentation work before publishing the
    // controller's asset pointer. CommercialSceneHost then treats the DOM
    // commit and browser route as one reversible mounted-selection transaction.
    var markup = renderDecisionSurface(nextAsset, this.labels, {
      locale: this.locale,
      dir: this.dir,
      numberFormatter: this.numberFormatter
    });
    this.root.innerHTML = markup;
    this.asset = nextAsset;
    this.bind();
    return this;
  };

  CommercialDecisionController.prototype.bind = function bind() {
    if (this.abortController) this.abortController.abort();
    this.abortController = new AbortController();
    var self = this;
    this.root.addEventListener(
      "click",
      function (event) {
        var control = event.target.closest("[data-act]");
        if (!control || !self.root.contains(control)) return;
        var action = control.dataset.act;
        if (action === "open-tool") {
          self.toolDialog.open(control.dataset.tool, self.asset, control);
        } else if (action === "request-tool-data") {
          self.onRequestField("tool." + control.dataset.tool, self.asset, control);
        } else if (action === "request-field") {
          self.onRequestField(control.dataset.fieldId, self.asset, control);
        } else if (action === "save") {
          self.onSave(self.asset, control);
        } else if (action === "share") {
          self.onShare(self.asset, control);
        } else if (action === "back-to-building") {
          self.onBack(self.asset, control);
        }
      },
      { signal: this.abortController.signal }
    );
  };

  CommercialDecisionController.prototype.destroy = function destroy() {
    if (this.abortController) this.abortController.abort();
    this.abortController = null;
    this.toolDialog.destroy();
    this.root.replaceChildren();
    this.asset = null;
  };

  function captureAttributes(node, names) {
    return names.reduce(function (snapshot, name) {
      snapshot[name] = node.hasAttribute(name) ? node.getAttribute(name) : null;
      return snapshot;
    }, {});
  }

  function restoreAttributes(node, snapshot) {
    Object.keys(snapshot).forEach(function (name) {
      if (snapshot[name] == null) node.removeAttribute(name);
      else node.setAttribute(name, snapshot[name]);
    });
  }

  /**
   * Pure viewport contract mirrored by the CSS below. It exists so the sacred
   * model+decision simultaneous-visibility promise is executable in fixtures.
   */
  function sceneGeometry(viewportWidth, viewportHeight) {
    var width = Math.max(1, finite(viewportWidth) || 1);
    var height = Math.max(1, finite(viewportHeight) || 1);
    if (width >= 960) {
      var railWidth = Math.max(390, Math.min(430, Math.round(width * 0.336)));
      return {
        mode: "desktop",
        modelWidth: width - railWidth,
        modelHeight: height,
        surfaceWidth: railWidth,
        surfaceHeight: height
      };
    }
    if (width > height && height <= 650) {
      var landscapeModelWidth = Math.round(width * 0.42);
      return {
        mode: "compact_landscape",
        modelWidth: landscapeModelWidth,
        modelHeight: height,
        surfaceWidth: width - landscapeModelWidth,
        surfaceHeight: height
      };
    }
    var modelHeight = Math.max(128, Math.min(210, Math.round(height * 0.28)));
    return {
      mode: "mobile_stack",
      modelWidth: width,
      modelHeight: modelHeight,
      surfaceWidth: width,
      surfaceHeight: height - modelHeight
    };
  }

  /**
   * Reparent the one existing live model node into one scene subtree. The node
   * is never cloned. destroy() restores its exact DOM position plus the style
   * and ARIA attributes that were present before mounting.
   */
  function CommercialSceneHost(options) {
    options = options || {};
    if (!isTrustedToolNode(options.modelNode)) {
      throw new Error("modelNode must be the existing live model DOM Node.");
    }
    if (!options.modelNode.parentNode) {
      throw new Error("modelNode must be connected to its original parent.");
    }
    this.modelNode = options.modelNode;
    this.labels = options.labels || {};
    this.locale = normalizeLocale(options.locale || this.labels.locale);
    this.dir = logicalDirection(this.locale, options.dir || this.labels.dir);
    this.resolveAsset =
      typeof options.resolveAsset === "function" ? options.resolveAsset : function () { return null; };
    this.onExit = typeof options.onExit === "function" ? options.onExit : function () {};
    this.onRouteSuspended =
      typeof options.onRouteSuspended === "function" ? options.onRouteSuspended : function () {};
    this.onInvalidRoute =
      typeof options.onInvalidRoute === "function" ? options.onInvalidRoute : function () {};
    this.expectedProjectContractId = contractId(options.projectContractId);
    if (!this.expectedProjectContractId || options.projectContractId !== this.expectedProjectContractId) {
      throw new Error("CommercialSceneHost requires one exact canonical projectContractId.");
    }
    this.routeHistoryEnabled = options.routeHistory !== false;
    if (
      this.routeHistoryEnabled &&
      (!window.history || typeof window.history.pushState !== "function" ||
        typeof window.history.replaceState !== "function" || !window.location ||
        typeof window.addEventListener !== "function")
    ) {
      throw new Error("Commercial asset routing requires the browser History and Location APIs.");
    }
    this.initialHistoryMode = options.initialHistoryMode === "push" ? "push" : "replace";
    this.controllerFactory =
      typeof options.controllerFactory === "function"
        ? options.controllerFactory
        : function (controllerOptions) {
            return new CommercialDecisionController(controllerOptions);
          };
    this.controllerOptions = options.controllerOptions || {};
    this.originalParent = null;
    this.originalNextSibling = null;
    this.originalAttributes = null;
    this.originalFocus = null;
    this.placeholder = null;
    this.scene = null;
    this.modelSlot = null;
    this.decisionSlot = null;
    this.decisionController = null;
    this.selectionHandler = null;
    this.routeAbortController = null;
    this.currentAsset = null;
    this.mounted = false;
    this.destroyed = false;
  }

  CommercialSceneHost.prototype.resolveAdaptedAsset = function resolveAdaptedAsset(assetOrId) {
    var asset = assetOrId && typeof assetOrId === "object" ? assetOrId : this.resolveAsset(assetOrId);
    if (!asset || asset.__nlCommercialAsset !== true || asset.selectable !== true) {
      throw new Error("The selected identity did not resolve to an explicitly selectable adapted asset.");
    }
    if (asset.projectId !== this.expectedProjectContractId) {
      throw new Error("The selected asset belongs to a different project contract.");
    }
    var projectBase = canonicalProjectBaseUrl(asset.projectUrl);
    var expectedAssetUrl = projectBase && identityUrl(
      projectBase,
      asset.projectId,
      asset.buildingId,
      asset.towerId,
      asset.floorId,
      asset.suiteId
    );
    if (!projectBase || projectBase !== asset.projectUrl || !expectedAssetUrl || expectedAssetUrl !== asset.url) {
      throw new Error("The adapted asset URL is not the canonical current-origin project route.");
    }
    var route = parseCommercialAssetRoute(asset.url);
    if (!commercialAssetRouteMatchesAsset(route, asset)) {
      throw new Error("The adapted asset is missing its exact canonical contract-tuple URL.");
    }
    return asset;
  };

  CommercialSceneHost.prototype.assetFromCurrentRoute = function assetFromCurrentRoute() {
    if (!this.routeHistoryEnabled) return { present: false, asset: null };
    var route = parseCommercialAssetRoute(window.location.href);
    if (!route.present) return { present: false, asset: null };
    if (!route.valid) throw new Error("The commercial asset URL tuple is incomplete or malformed.");
    var asset = this.resolveAdaptedAsset(this.resolveAsset(route.identityKey));
    if (!commercialAssetRouteMatchesAsset(route, asset)) {
      throw new Error("The commercial asset URL does not resolve to the exact adapted asset.");
    }
    return { present: true, asset: asset, route: route };
  };

  CommercialSceneHost.prototype.ensureRouteListener = function ensureRouteListener() {
    if (!this.routeHistoryEnabled || this.routeAbortController) return;
    this.routeAbortController = new AbortController();
    var self = this;
    window.addEventListener(
      "popstate",
      function (event) { self.handleAssetPopState(event); },
      { signal: this.routeAbortController.signal }
    );
  };

  CommercialSceneHost.prototype.mount = function mount(initialAssetOrId, mountOptions) {
    mountOptions = mountOptions || {};
    if (this.destroyed) throw new Error("A destroyed commercial scene host cannot be remounted.");
    if (this.mounted) {
      if (initialAssetOrId != null) this.render(initialAssetOrId, mountOptions);
      return this;
    }
    var routeSelection = this.assetFromCurrentRoute();
    var initialAsset = routeSelection.present
      ? routeSelection.asset
      : this.resolveAdaptedAsset(initialAssetOrId);
    var initialHistoryMode = routeSelection.present
      ? (mountOptions.fromHistory ? "none" : "replace")
      : (mountOptions.history || this.initialHistoryMode);
    try {
      this.ensureRouteListener();
      var modelNode = this.modelNode;
      this.originalParent = modelNode.parentNode;
      this.originalNextSibling = modelNode.nextSibling;
      this.originalAttributes = captureAttributes(modelNode, [
      "style",
      "class",
      "role",
      "aria-label",
      "aria-hidden",
      "tabindex",
      "inert",
      "data-selected-floor"
    ]);
      this.originalFocus = document.activeElement;
      this.placeholder = document.createComment("nl-commercial-scene-model-origin");

      var scene = createNode("section", "nl-commercial-scene");
    scene.lang = this.locale;
    scene.dir = this.dir;
    scene.setAttribute("data-commercial-scene", "true");
    var modelSlot = createNode("div", "nl-commercial-scene__model");
    modelSlot.setAttribute("role", "region");
    modelSlot.setAttribute(
      "aria-label",
      this.labels.modelRegion || "Interactive building and floor selection"
    );
    var decisionSlot = createNode("div", "nl-commercial-scene__decision");
    decisionSlot.setAttribute("role", "region");
    decisionSlot.setAttribute(
      "aria-label",
      this.labels.decisionRegion || "Selected space details and tools"
    );
    scene.appendChild(modelSlot);
    scene.appendChild(decisionSlot);

      this.scene = scene;
      this.modelSlot = modelSlot;
      this.decisionSlot = decisionSlot;
      this.mounted = true;
      this.originalParent.insertBefore(this.placeholder, modelNode);
      this.originalParent.insertBefore(scene, modelNode);
      modelSlot.appendChild(modelNode);

      var self = this;
      this.decisionController = this.controllerFactory(
      Object.assign({}, this.controllerOptions, {
        root: decisionSlot,
        labels: this.labels,
        locale: this.locale,
        dir: this.dir,
        resolveAsset: this.resolveAsset,
        onBack: function (asset, control) {
          self.exit(asset, control);
        }
      })
    );
      this.selectionHandler = function (event) {
      var detail = event && event.detail ? event.detail : {};
      if (!detail.floorId || !detail.buildingId || !detail.towerId) return;
      try {
        var hasSuiteId = Object.prototype.hasOwnProperty.call(detail, "suiteId");
        var suppliedSuiteId = null;
        if (hasSuiteId) {
          if (detail.suiteId === null) {
            suppliedSuiteId = null;
          } else {
            suppliedSuiteId = contractId(detail.suiteId);
            if (!suppliedSuiteId || suppliedSuiteId !== detail.suiteId) {
              throw new Error("Selection event suite identity is not canonical.");
            }
          }
        }
        var key = detail.identityKey || commercialIdentityKey(
          detail.buildingId,
          detail.towerId,
          detail.floorId,
          suppliedSuiteId
        );
        var selected = self.resolveAdaptedAsset(self.resolveAsset(key));
        if (
          selected.buildingId !== contractId(detail.buildingId) ||
          selected.towerId !== contractId(detail.towerId) ||
          selected.floorId !== contractId(detail.floorId) ||
          selected.suiteId !== suppliedSuiteId ||
          (detail.projectId && selected.projectId !== contractId(detail.projectId))
        ) {
          throw new Error("Selection event identity does not match the adapted asset.");
        }
        self.render(selected, { history: "push", origin: detail.origin || "selection" });
      } catch (error) {
        try {
          if (self.currentAsset) self.syncSelectionControls(self.currentAsset, "selection_rollback");
        } catch (rollbackError) {}
        self.onInvalidRoute({ reason: "selection_identity_invalid", error: error });
      }
      };
      scene.addEventListener("nadlan:commercial-asset-selected", this.selectionHandler);
      this.render(initialAsset, {
        history: "none",
        origin: routeSelection.present ? (mountOptions.fromHistory ? "history" : "deep-link") :
          (mountOptions.origin || "initial")
      });
      // History is the final commit. Any earlier listener/controller/render
      // failure has no route mutation; a History API exception rolls the whole
      // mounted subtree and external selection state back below.
      this.writeAssetRoute(initialAsset, initialHistoryMode);
      return this;
    } catch (error) {
      try { if (this.mounted) this.clearSelectionControls("mount_rollback"); } catch (clearError) {}
      try { this.unmount(true); } catch (unmountError) {}
      try { if (this.routeAbortController) this.routeAbortController.abort(); } catch (abortError) {}
      this.routeAbortController = null;
      throw error;
    }
  };

  CommercialSceneHost.prototype.writeAssetRoute = function writeAssetRoute(asset, mode) {
    if (!this.routeHistoryEnabled || mode === "none") return;
    var marker = createCommercialAssetRouteMarker(asset);
    if (!marker || !asset.url) {
      throw new Error("Cannot write a commercial asset route without its exact identity and URL.");
    }
    var nextState = stripToolHistoryState(window.history.state);
    nextState.nlCommercialAsset = marker;
    var current = normalizeCommercialAssetRouteMarker(window.history.state);
    var same = commercialAssetRouteMarkerMatchesAsset(current, asset) && window.location.href === asset.url;
    if (mode === "push" && !same) window.history.pushState(nextState, "", asset.url);
    else window.history.replaceState(nextState, "", asset.url);
  };

  CommercialSceneHost.prototype.syncSelectionControls = function syncSelectionControls(asset, origin) {
    this.modelNode.dispatchEvent(new CustomEvent(ASSET_ROUTE_EVENT, {
      bubbles: false,
      detail: {
        wpPostId: asset.wpPostId,
        projectContractId: asset.projectId,
        buildingId: asset.buildingId,
        towerId: asset.towerId,
        floorId: asset.floorId,
        suiteId: asset.suiteId,
        identityKey: asset.identityKey,
        floorIdentityKey: commercialIdentityKey(asset.buildingId, asset.towerId, asset.floorId),
        origin: origin || "route"
      }
    }));
  };

  CommercialSceneHost.prototype.clearSelectionControls = function clearSelectionControls(reason) {
    this.modelNode.dispatchEvent(new CustomEvent(ASSET_ROUTE_EVENT, {
      bubbles: false,
      detail: {
        projectContractId: this.expectedProjectContractId,
        clear: true,
        origin: reason || "route_suspend"
      }
    }));
  };

  CommercialSceneHost.prototype.render = function render(assetOrId, renderOptions) {
    renderOptions = renderOptions || {};
    if (!this.mounted || !this.decisionController) {
      throw new Error("Mount the commercial scene before rendering an asset.");
    }
    var asset = this.resolveAdaptedAsset(assetOrId);
    var sameAsset = Boolean(
      this.currentAsset && this.currentAsset.identityKey === asset.identityKey &&
      this.currentAsset.projectId === asset.projectId && this.currentAsset.wpPostId === asset.wpPostId
    );
    var priorAsset = this.currentAsset;
    var priorControllerAsset = Object.prototype.hasOwnProperty.call(this.decisionController, "asset")
      ? this.decisionController.asset
      : priorAsset;
    var priorMarkup = this.decisionSlot ? this.decisionSlot.innerHTML : "";
    var priorFocus = document.activeElement;
    var priorHref = window.location.href;
    var priorHistoryState = window.history ? window.history.state : null;
    var priorHistoryJson = "";
    try { priorHistoryJson = JSON.stringify(priorHistoryState); } catch (snapshotError) {}

    try {
      // Stage the potentially throwing renderer before the History API commit.
      // A failed mounted switch therefore creates no extra push entry and the
      // existing tool dialog/marker remains byte-for-byte in place.
      if (!sameAsset) this.decisionController.render(asset);
      this.writeAssetRoute(asset, renderOptions.history || "replace");
    } catch (error) {
      if (!sameAsset) {
        var restoredByController = false;
        if (priorAsset && typeof this.decisionController.render === "function") {
          try {
            this.decisionController.render(priorAsset);
            restoredByController = true;
          } catch (restoreError) {}
        }
        if (!restoredByController && this.decisionSlot) {
          try {
            this.decisionSlot.innerHTML = priorMarkup;
            if (Object.prototype.hasOwnProperty.call(this.decisionController, "asset")) {
              this.decisionController.asset = priorControllerAsset;
            }
            if (priorAsset && typeof this.decisionController.bind === "function") {
              this.decisionController.bind();
            }
          } catch (surfaceRestoreError) {}
        }
        var rollbackToolDialog = this.decisionController.toolDialog;
        if (
          priorAsset && rollbackToolDialog && rollbackToolDialog.dialog &&
          toolHistoryMarkerMatchesAsset(
            createToolHistoryMarker(rollbackToolDialog.kind, rollbackToolDialog.asset),
            priorAsset
          )
        ) {
          // Restoring the prior decision markup creates a new door Node. Keep
          // the actual open dialog/marker/locks, but remap its focus-return
          // target to that exact connected door for the restored asset.
          var restoredTrigger = rollbackToolDialog.findHistoryTrigger(rollbackToolDialog.kind);
          if (restoredTrigger && restoredTrigger.isConnected) {
            rollbackToolDialog.trigger = restoredTrigger;
          }
        }
      }
      this.currentAsset = priorAsset;
      if (priorAsset) {
        try { this.syncSelectionControls(priorAsset, "render_rollback"); } catch (selectionRestoreError) {}
      }
      var historyChanged = window.location.href !== priorHref;
      if (!historyChanged && priorHistoryJson) {
        try { historyChanged = JSON.stringify(window.history.state) !== priorHistoryJson; } catch (historySnapshotError) {}
      }
      if (historyChanged && window.history && typeof window.history.replaceState === "function") {
        try { window.history.replaceState(priorHistoryState, "", priorHref); } catch (historyRestoreError) {}
      }
      if (priorFocus && priorFocus.isConnected && typeof priorFocus.focus === "function") {
        try { priorFocus.focus({ preventScroll: true }); } catch (focusRestoreError) {}
      }
      throw error;
    }
    // Only a fully rendered and committed new route may close a child tool.
    if (!sameAsset && this.decisionController.toolDialog && this.decisionController.toolDialog.dialog) {
      this.decisionController.toolDialog.close({ history: false, focus: false });
    }
    this.currentAsset = asset;
    this.syncSelectionControls(asset, renderOptions.origin || "render");
    return this;
  };

  CommercialSceneHost.prototype.safeProjectUrl = function safeProjectUrl() {
    if (this.currentAsset) {
      var currentProjectUrl = canonicalProjectBaseUrl(this.currentAsset.projectUrl);
      if (currentProjectUrl) return currentProjectUrl;
    }
    try {
      var url = new URL(window.location.href);
      COMMERCIAL_ROUTE_PARAMS.forEach(function (name) {
        url.searchParams.delete(name);
      });
      url.hash = "";
      var safeBase = canonicalProjectBaseUrl(url.toString());
      return safeBase || new URL("/", currentWindowOrigin()).toString();
    } catch (error) {
      return new URL("/", currentWindowOrigin()).toString();
    }
  };

  CommercialSceneHost.prototype.replaceInvalidRoute = function replaceInvalidRoute(state, reason) {
    var safeUrl = this.safeProjectUrl();
    try {
      window.history.replaceState(stripCommercialAssetRouteState(state), "", safeUrl);
    } catch (historyError) {
      this.onInvalidRoute({ reason: "history_replace_failed", error: historyError });
    } finally {
      this.suspendForHistory(reason || "invalid_route");
    }
  };

  CommercialSceneHost.prototype.handleAssetPopState = function handleAssetPopState(event) {
    if (!this.routeHistoryEnabled || this.destroyed) return;
    var state = event && event.state;
    var hasRawMarker = isObject(state) && Object.prototype.hasOwnProperty.call(state, "nlCommercialAsset");
    var marker = normalizeCommercialAssetRouteMarker(state);
    var route = parseCommercialAssetRoute(window.location.href);
    if (!marker) {
      if (hasRawMarker || route.present) {
        this.replaceInvalidRoute(state, "stale_or_incomplete_route");
      } else {
        this.suspendForHistory("route_removed");
      }
      return;
    }
    if (!route.present || !route.valid) {
      this.replaceInvalidRoute(state, "route_state_url_mismatch");
      return;
    }
    var asset;
    try {
      asset = this.resolveAdaptedAsset(this.resolveAsset(route.identityKey));
    } catch (error) {
      this.replaceInvalidRoute(state, "route_asset_unavailable");
      return;
    }
    if (!commercialAssetRouteMatchesAsset(route, asset) || !commercialAssetRouteMarkerMatchesAsset(marker, asset)) {
      this.replaceInvalidRoute(state, "route_identity_mismatch");
      return;
    }
    if (!this.mounted) {
      this.mount(asset, { fromHistory: true, history: "none", origin: "history" });
    } else {
      this.render(asset, { history: "none", origin: "history" });
    }
  };

  CommercialSceneHost.prototype.exit = function exit(asset, control) {
    if (this.destroyed) return;
    if (this.routeHistoryEnabled) {
      var buildingState = stripCommercialAssetRouteState(window.history.state);
      var safeUrl = this.safeProjectUrl();
      try {
        window.history.pushState(buildingState, "", safeUrl);
        this.suspendForHistory("back_to_building");
      } catch (historyError) {
        try { window.history.replaceState(buildingState, "", safeUrl); } catch (replaceError) {}
        this.suspendForHistory("back_to_building_history_unavailable");
        this.onInvalidRoute({ reason: "building_history_unavailable", error: historyError });
      }
    } else {
      this.destroy();
    }
    this.onExit(asset, control);
  };

  CommercialSceneHost.prototype.unmount = function unmount(restoreFocus) {
    if (!this.mounted) return;
    var focusTarget = this.originalFocus;
    var scene = this.scene;
    var placeholder = this.placeholder;
    var controller = this.decisionController;
    var selectionHandler = this.selectionHandler;
    this.mounted = false;
    try {
      if (scene && selectionHandler) {
        scene.removeEventListener("nadlan:commercial-asset-selected", selectionHandler);
      }
    } catch (listenerError) {}
    try {
      if (controller && typeof controller.destroy === "function") controller.destroy();
    } catch (controllerError) {}
    try {
      if (this.originalParent) {
        if (placeholder && placeholder.parentNode === this.originalParent) {
          this.originalParent.insertBefore(this.modelNode, placeholder);
        } else if (
          this.originalNextSibling &&
          this.originalNextSibling.parentNode === this.originalParent
        ) {
          this.originalParent.insertBefore(this.modelNode, this.originalNextSibling);
        } else {
          this.originalParent.appendChild(this.modelNode);
        }
      }
    } catch (modelRestoreError) {
      try { if (this.originalParent) this.originalParent.appendChild(this.modelNode); } catch (appendError) {}
    }
    try { if (this.originalAttributes) restoreAttributes(this.modelNode, this.originalAttributes); } catch (attributeError) {}
    try { if (placeholder && placeholder.parentNode) placeholder.remove(); } catch (placeholderError) {}
    try { if (scene && scene.parentNode) scene.remove(); } catch (sceneError) {}
    this.scene = null;
    this.modelSlot = null;
    this.decisionSlot = null;
    this.placeholder = null;
    this.decisionController = null;
    this.selectionHandler = null;
    this.currentAsset = null;
    if (restoreFocus !== false && focusTarget && typeof focusTarget.focus === "function") {
      window.requestAnimationFrame(function () {
        focusTarget.focus({ preventScroll: true });
      });
    }
  };

  CommercialSceneHost.prototype.suspendForHistory = function suspendForHistory(reason) {
    var asset = this.currentAsset;
    var suspensionReason = reason || "route_removed";
    // Selection adapters and host callbacks are integration-owned. Neither is
    // allowed to keep the model subtree mounted or page locks alive when its
    // hook throws during Back/Forward or the Building transition.
    try { this.clearSelectionControls(suspensionReason); } catch (clearError) {}
    try { this.unmount(true); } catch (unmountError) {}
    try {
      this.onRouteSuspended(asset, { history: true, reason: suspensionReason });
    } catch (suspendedError) {}
  };

  CommercialSceneHost.prototype.destroy = function destroy() {
    if (this.destroyed) return;
    try {
      if (this.routeHistoryEnabled && window.history) {
        var hasAssetMarker = isObject(window.history.state) &&
          Object.prototype.hasOwnProperty.call(window.history.state, "nlCommercialAsset");
        if (hasAssetMarker) {
          try {
            window.history.replaceState(
              stripCommercialAssetRouteState(window.history.state),
              "",
              this.safeProjectUrl()
            );
          } catch (historyError) {
            this.onInvalidRoute({ reason: "destroy_history_unavailable", error: historyError });
          }
        }
      }
    } finally {
      try { if (this.mounted) this.clearSelectionControls("destroy"); } catch (clearError) {}
      try { this.unmount(true); } catch (unmountError) {}
      try { if (this.routeAbortController) this.routeAbortController.abort(); } catch (abortError) {}
      this.routeAbortController = null;
      this.destroyed = true;
    }
  };

  window.NadlanCommercialContractAdapter = {
    schemaVersion: CONTRACT_SCHEMA_VERSION,
    assetTypes: VALID_ASSET_TYPES.slice(),
    implementedAssetTypes: IMPLEMENTED_ASSET_TYPES.slice(),
    productFamilies: VALID_PRODUCT_FAMILIES.slice(),
    applicabilityTags: VALID_APPLICABILITY_TAGS.slice(),
    evidenceStates: VALID_EVIDENCE_STATES.slice(),
    confidenceLevels: VALID_CONFIDENCE_LEVELS.slice(),
    availabilityStatuses: VALID_AVAILABILITY_STATUSES.slice(),
    compassSectors: VALID_COMPASS_SECTORS.slice(),
    beamDistanceMethods: VALID_BEAM_DISTANCE_METHODS.slice(),
    beamCompactLabelMaxCodePoints: BEAM_COMPACT_LABEL_MAX_CODE_POINTS,
    commercialIdentityKey: commercialIdentityKey,
    canonicalProjectBaseUrl: canonicalProjectBaseUrl,
    identityUrl: identityUrl,
    normalizeEvidenceEnvelope: normalizeEvidenceEnvelope,
    normalizeAvailabilityStatus: normalizeAvailabilityStatus,
    normalizeAvailability: normalizeAvailability,
    adaptExposure: adaptExposure,
    adaptExposures: adaptExposures,
    adaptBeamScene: adaptBeamScene,
    adaptFloor: adaptFloor,
    adaptSuite: adaptSuite,
    adaptProjectContract: adaptProjectContract,
    adaptContractPayload: adaptContractPayload,
    buildFloorRanges: buildFloorRanges
  };

  window.NadlanCommercialDecisionSurface = {
    CommercialDecisionController: CommercialDecisionController,
    CommercialToolDialog: CommercialToolDialog,
    CommercialSceneHost: CommercialSceneHost,
    sceneGeometry: sceneGeometry,
    evidence: evidence,
    renderDecisionSurface: renderDecisionSurface,
    collectBeamEvidenceSources: collectBeamEvidenceSources,
    beamEvidencePage: beamEvidencePage,
    createBeamEvidenceNode: createBeamEvidenceNode,
    defaultToolNode: defaultToolNode,
    isTrustedToolNode: isTrustedToolNode,
    createToolHistoryMarker: createToolHistoryMarker,
    normalizeToolHistoryMarker: normalizeToolHistoryMarker,
    toolHistoryMarkerMatchesAsset: toolHistoryMarkerMatchesAsset,
    stripToolHistoryState: stripToolHistoryState,
    createCommercialAssetRouteMarker: createCommercialAssetRouteMarker,
    normalizeCommercialAssetRouteMarker: normalizeCommercialAssetRouteMarker,
    commercialAssetRouteMarkerMatchesAsset: commercialAssetRouteMarkerMatchesAsset,
    parseCommercialAssetRoute: parseCommercialAssetRoute,
    commercialAssetRouteMatchesAsset: commercialAssetRouteMatchesAsset,
    stripCommercialAssetRouteState: stripCommercialAssetRouteState,
    assetRouteEventName: ASSET_ROUTE_EVENT,
    normalizeLocale: normalizeLocale,
    logicalDirection: logicalDirection,
    resolveNumberFormatter: resolveNumberFormatter,
    logicalBackIcon: logicalBackIcon
  };
})(window, document);
