/*
 * Nadlan flagship visual tools — isolated, data-driven proposal runtime.
 * No fetch, beacon, storage, form submission, inventory inference or engine mutation.
 */
(function attachFlagshipVisualTools(globalScope, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (globalScope) globalScope.NadlanFlagshipShowroom = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function flagshipFactory() {
  "use strict";

  var OWNER_DECISION_ID = "OWNER-2026-08-13-VISUAL-PLAYGROUND";
  var EXPERIENCE_DECISION_ID = "OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO";
  var ALLOWED_TOOLS = Object.freeze({
    view: "schematic_live_map",
    interior: "first_person_door",
    design: "illustrative_plan_drag",
    comments: "visual_annotation_request"
  });

  function escapeHtml(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (character) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character];
    });
  }

  function cloneSnapshot(value) {
    if (value === undefined) throw new Error("Model snapshot is required.");
    if (typeof structuredClone === "function") return structuredClone(value);
    return JSON.parse(JSON.stringify(value));
  }

  function validIsoDate(value) {
    return typeof value === "string" && value.length > 0 && Number.isFinite(Date.parse(value));
  }

  function validLocalAssetUrl(value, assetPrefix, assetId) {
    if (typeof value !== "string" || !value.startsWith(assetPrefix) || !/^\/(?!\/)[A-Za-z0-9._~%/-]+$/.test(value) || /(?:^|\/)\.\.?\//.test(value)) return false;
    return value === assetPrefix + assetId + ".webp";
  }

  function normalizeExperienceScenes(source, groupId, representationKind, assetPrefix, seenAssets) {
    var group = source && typeof source === "object" ? source[groupId] : null;
    var scenes = group && Array.isArray(group.scenes) ? group.scenes : [];
    if (
      !group || group.representation_kind !== representationKind ||
      group.experience_kind !== representationKind ||
      group.mapping_state !== "owner_approved_illustrative_mapping" || group.decision_grade !== false || scenes.length !== 2
    ) throw new Error("The " + groupId + " experience assets are invalid.");
    var seen = Object.create(null);
    return Object.freeze(scenes.map(function (scene) {
      if (
        !scene || !/^[a-z0-9][a-z0-9-]*$/.test(scene.id) || seen[scene.id] ||
        !/^[a-z0-9][a-z0-9-]*$/.test(scene.asset_id) || seenAssets.ids[scene.asset_id] || seenAssets.urls[scene.url] ||
        !scene.label || !validLocalAssetUrl(scene.url, assetPrefix, scene.asset_id) ||
        !/^[a-f0-9]{64}$/.test(scene.sha256) || !Number.isSafeInteger(scene.bytes) || scene.bytes <= 0 ||
        !Number.isSafeInteger(scene.width) || scene.width <= 0 || !Number.isSafeInteger(scene.height) || scene.height <= 0 ||
        !/^[a-z0-9][a-z0-9-]*$/.test(scene.hotspot_id) || !Array.isArray(scene.illustrative_position) ||
        scene.illustrative_position.length !== 3 || !scene.illustrative_position.every(Number.isFinite) ||
        scene.open_surface_tool_id !== "interior" ||
        scene.experience_kind !== representationKind || scene.mapping_state !== "owner_approved_illustrative_mapping" ||
        scene.decision_grade !== false
      ) throw new Error("The " + groupId + " experience scene is invalid.");
      seen[scene.id] = true;
      seenAssets.ids[scene.asset_id] = true;
      seenAssets.urls[scene.url] = true;
      return Object.freeze({
        id: String(scene.id), assetId: String(scene.asset_id), label: String(scene.label), url: String(scene.url),
        sha256: String(scene.sha256), bytes: scene.bytes, width: scene.width, height: scene.height,
        experienceKind: representationKind, hotspotId: String(scene.hotspot_id), openSurfaceToolId: "interior", illustrativePosition: Object.freeze(scene.illustrative_position.slice()),
        mappingState: "owner_approved_illustrative_mapping", decisionGrade: false
      });
    }));
  }

  function normalizeExperienceMapping(source, experienceAssets, allowedEvidenceReferenceIds) {
    var mapping = source && typeof source === "object" ? source : {};
    var anchors = Array.isArray(mapping.anchors) ? mapping.anchors : [];
    if (
      mapping.active_state !== "owner_approved_illustrative_mapping" || mapping.future_verified_state !== "source_cited_mapping" ||
      mapping.coordinate_space !== "model_metres_y_up" || mapping.source_cited !== false || mapping.decision_grade !== false ||
      mapping.real_world_orientation_calibrated !== false || anchors.length !== 3
    ) throw new Error("The illustrative experience mapping policy is invalid.");
    var allScenes = experienceAssets.interior.scenes.concat(experienceAssets.facilities.scenes);
    var coveredScenes = Object.create(null), seenHotspots = Object.create(null);
    var normalized = anchors.map(function (anchor) {
      var expectedKind = anchor && anchor.tool_id === "interior" ? "interior_walkthrough" : anchor && anchor.tool_id === "facilities" ? anchor.kind : "";
      var expectedExperience = anchor && anchor.tool_id === "interior" ? "representative_concept" : anchor && anchor.tool_id === "facilities" ? "selectable_concept_gallery" : "";
      var placementConfidence = anchor && anchor.placement_confidence;
      var referenceIds = anchor && anchor.evidence_basis && Array.isArray(anchor.evidence_basis.primary_reference_ids) && Array.isArray(anchor.evidence_basis.corroborating_reference_ids) ? anchor.evidence_basis.primary_reference_ids.concat(anchor.evidence_basis.corroborating_reference_ids) : [];
      var sourceAnchors = anchor && anchor.evidence_basis && Array.isArray(anchor.evidence_basis.source_anchors) ? anchor.evidence_basis.source_anchors : [];
      if (
        !anchor || !/^[a-z0-9][a-z0-9-]*$/.test(anchor.hotspot_id) || seenHotspots[anchor.hotspot_id] ||
        anchor.open_surface_tool_id !== "interior" ||
        !expectedKind || anchor.kind !== expectedKind || anchor.experience_kind !== expectedExperience ||
        !Array.isArray(anchor.scene_ids) || !anchor.scene_ids.length || !Array.isArray(anchor.model_component_ids) || !anchor.model_component_ids.length ||
        !anchor.model_component_ids.every(function (id) { return /^[A-Za-z0-9][A-Za-z0-9_-]*$/.test(id); }) ||
        !/^[a-z0-9][a-z0-9_+-]*$/.test(anchor.illustrative_zone_id) || !Array.isArray(anchor.position) || anchor.position.length !== 3 || !anchor.position.every(Number.isFinite) ||
        !Array.isArray(anchor.surface_normal) || anchor.surface_normal.length !== 3 || !anchor.surface_normal.every(Number.isFinite) ||
        Math.abs(Math.hypot.apply(Math, anchor.surface_normal) - 1) > 0.001 || !Number.isFinite(anchor.visual_offset_along_normal_m) || anchor.visual_offset_along_normal_m < 0 ||
        anchor.confidence !== "model_zone_fit_high__source_spatial_confidence_none" || !referenceIds.length || !referenceIds.every(function (id) { return allowedEvidenceReferenceIds.indexOf(id) >= 0; }) ||
        !placementConfidence || !Number.isFinite(placementConfidence.zone) || placementConfidence.zone < 0 || placementConfidence.zone > 1 ||
        !Number.isFinite(placementConfidence.exact_point) || placementConfidence.exact_point < 0 || placementConfidence.exact_point > 1 ||
        !sourceAnchors.every(function (item) { return typeof item === "string" && item.length > 0; }) ||
        !anchor.evidence_basis.supports || !anchor.ambiguity || !Array.isArray(anchor.prohibited_inferences) || !anchor.prohibited_inferences.length
      ) throw new Error("An illustrative experience mapping anchor is invalid.");
      seenHotspots[anchor.hotspot_id] = true;
      anchor.scene_ids.forEach(function (sceneId) {
        var scene = allScenes.find(function (candidate) { return candidate.id === sceneId; });
        if (!scene || scene.experienceKind !== expectedExperience || scene.hotspotId !== anchor.hotspot_id || scene.openSurfaceToolId !== anchor.open_surface_tool_id || coveredScenes[sceneId] || JSON.stringify(scene.illustrativePosition) !== JSON.stringify(anchor.position)) throw new Error("The mapped scene binding is invalid.");
        coveredScenes[sceneId] = true;
      });
      return Object.freeze({
        hotspotId: String(anchor.hotspot_id), toolId: String(anchor.tool_id), openSurfaceToolId: "interior", kind: String(anchor.kind), experienceKind: String(anchor.experience_kind),
        sceneIds: Object.freeze(anchor.scene_ids.slice()), modelComponentIds: Object.freeze(anchor.model_component_ids.slice()), illustrativeZoneId: String(anchor.illustrative_zone_id),
        position: Object.freeze(anchor.position.slice()), surfaceNormal: Object.freeze(anchor.surface_normal.slice()), visualOffsetAlongNormalM: anchor.visual_offset_along_normal_m,
        confidence: String(anchor.confidence), placementConfidence: Object.freeze({ zone: placementConfidence.zone, exactPoint: placementConfidence.exact_point }), evidenceReferenceIds: Object.freeze(referenceIds.slice()), evidenceSupports: String(anchor.evidence_basis.supports),
        sourceAnchors: Object.freeze(sourceAnchors.slice()),
        ambiguity: String(anchor.ambiguity), prohibitedInferences: Object.freeze(anchor.prohibited_inferences.map(String)), sourceCited: false, decisionGrade: false
      });
    });
    if (Object.keys(coveredScenes).length !== allScenes.length) throw new Error("Every experience scene must bind to exactly one illustrative mapping anchor.");
    var usedEvidenceReferenceIds = Object.keys(normalized.reduce(function (used, anchor) {
      anchor.evidenceReferenceIds.forEach(function (id) { used[id] = true; });
      return used;
    }, Object.create(null))).sort();
    if (JSON.stringify(usedEvidenceReferenceIds) !== JSON.stringify(allowedEvidenceReferenceIds.slice().sort())) throw new Error("The mapping evidence references must exactly match the trusted allowlist.");
    return Object.freeze({ activeState: "owner_approved_illustrative_mapping", futureVerifiedState: "source_cited_mapping", coordinateSpace: "model_metres_y_up", sourceCited: false, decisionGrade: false, realWorldOrientationCalibrated: false, anchors: Object.freeze(normalized) });
  }

  function normalizeConfig(input, nowValue, expectedProjectContractId, allowedEvidenceReferenceIds, allowedAssetPrefix) {
    var source = input && typeof input === "object" ? input : {};
    var identity = source.identity && typeof source.identity === "object" ? source.identity : {};
    var decision = source.decision && typeof source.decision === "object" ? source.decision : {};
    var experienceDecision = source.experience_decision && typeof source.experience_decision === "object" ? source.experience_decision : {};
    var experienceAssetsSource = source.experience_assets && typeof source.experience_assets === "object" ? source.experience_assets : {};
    var now = Number.isFinite(nowValue) ? nowValue : Date.now();
    if (typeof expectedProjectContractId !== "string" || !expectedProjectContractId) throw new Error("A trusted expectedProjectContractId is required.");
    if (
      !Array.isArray(allowedEvidenceReferenceIds) || !allowedEvidenceReferenceIds.length ||
      allowedEvidenceReferenceIds.some(function (id, index) { return typeof id !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/.test(id) || allowedEvidenceReferenceIds.indexOf(id) !== index; })
    ) throw new Error("A trusted, unique allowedEvidenceReferenceIds list is required.");
    if (
      typeof allowedAssetPrefix !== "string" || !/^\/(?:[A-Za-z0-9._~-]+\/)+$/.test(allowedAssetPrefix) ||
      allowedAssetPrefix.split("/").some(function (segment) { return segment === "." || segment === ".."; })
    ) throw new Error("A trusted same-origin allowedAssetPrefix is required.");
    if (identity.project_contract_id !== expectedProjectContractId) throw new Error("project_contract_id does not match the trusted host identity.");
    if (!/^[a-z0-9][a-z0-9-]*$/.test(identity.public_slug) || !identity.representation_name) throw new Error("Canonical project identity is incomplete.");
    if (
      decision.owner_decision_id !== OWNER_DECISION_ID ||
      decision.approved_by !== "site_owner" ||
      decision.decision_grade !== false ||
      typeof decision.version !== "string" || !decision.version ||
      !validIsoDate(decision.effective_at) || !validIsoDate(decision.expires_at) ||
      Date.parse(decision.effective_at) > now || Date.parse(decision.expires_at) <= now ||
      Date.parse(decision.expires_at) <= Date.parse(decision.effective_at)
    ) throw new Error("The illustrative owner-decision record is invalid or expired.");
    if (
      experienceDecision.owner_decision_id !== EXPERIENCE_DECISION_ID ||
      experienceDecision.approved_by !== "site_owner" ||
      experienceDecision.representation_kind !== "owner_approved_illustration" ||
      experienceDecision.decision_grade !== false ||
      typeof experienceDecision.version !== "string" || !experienceDecision.version ||
      !validIsoDate(experienceDecision.effective_at) || !validIsoDate(experienceDecision.expires_at) ||
      Date.parse(experienceDecision.effective_at) > now || Date.parse(experienceDecision.expires_at) <= now ||
      Date.parse(experienceDecision.expires_at) <= Date.parse(experienceDecision.effective_at)
    ) throw new Error("The interiors/facilities experience decision is invalid or expired.");

    var assetPrefix = allowedAssetPrefix;
    var seenExperienceAssets = { ids: Object.create(null), urls: Object.create(null) };
    var experienceAssets = Object.freeze({
      interior: Object.freeze({
        representationKind: "representative_concept",
        experienceKind: "representative_concept",
        mappingState: "owner_approved_illustrative_mapping",
        decisionGrade: false,
        scenes: normalizeExperienceScenes(experienceAssetsSource, "interior", "representative_concept", assetPrefix, seenExperienceAssets)
      }),
      facilities: Object.freeze({
        representationKind: "selectable_concept_gallery",
        experienceKind: "selectable_concept_gallery",
        mappingState: "owner_approved_illustrative_mapping",
        decisionGrade: false,
        scenes: normalizeExperienceScenes(experienceAssetsSource, "facilities", "selectable_concept_gallery", assetPrefix, seenExperienceAssets)
      })
    });
    var experienceMapping = normalizeExperienceMapping(source.experience_mapping, experienceAssets, allowedEvidenceReferenceIds);

    var incomingTools = Array.isArray(source.tools) ? source.tools : [];
    var allowedToolIds = Object.keys(ALLOWED_TOOLS);
    var incomingToolIds = incomingTools.map(function (tool) { return tool && tool.id; });
    if (
      incomingTools.length !== allowedToolIds.length ||
      incomingToolIds.some(function (toolId, index) { return !ALLOWED_TOOLS[toolId] || incomingToolIds.indexOf(toolId) !== index; }) ||
      allowedToolIds.some(function (toolId) { return incomingToolIds.indexOf(toolId) < 0; })
    ) throw new Error("Illustrative tools must contain exactly view, interior, design and comments once each.");
    var tools = Object.keys(ALLOWED_TOOLS).map(function (toolId) {
      var tool = incomingTools.find(function (candidate) { return candidate && candidate.id === toolId; });
      if (!tool || tool.preview_kind !== ALLOWED_TOOLS[toolId] || tool.decision_grade !== false) {
        throw new Error("Missing or invalid illustrative tool: " + toolId);
      }
      if (!tool.title || !tool.description || !tool.open_label || !tool.disclosure) {
        throw new Error("Illustrative tool copy is incomplete: " + toolId);
      }
      return Object.freeze({
        id: toolId,
        previewKind: tool.preview_kind,
        title: String(tool.title),
        description: String(tool.description),
        openLabel: String(tool.open_label),
        disclosure: String(tool.disclosure),
        decisionGrade: false
      });
    });

    return Object.freeze({
      identity: Object.freeze({
        projectContractId: String(identity.project_contract_id),
        publicSlug: String(identity.public_slug),
        representationName: String(identity.representation_name)
      }),
      decision: Object.freeze({
        ownerDecisionId: OWNER_DECISION_ID,
        approvedBy: "site_owner",
        version: String(decision.version),
        effectiveAt: String(decision.effective_at),
        expiresAt: String(decision.expires_at),
        decisionGrade: false
      }),
      experienceDecision: Object.freeze({
        ownerDecisionId: EXPERIENCE_DECISION_ID,
        approvedBy: "site_owner",
        representationKind: "owner_approved_illustration",
        version: String(experienceDecision.version),
        effectiveAt: String(experienceDecision.effective_at),
        expiresAt: String(experienceDecision.expires_at),
        decisionGrade: false
      }),
      experienceAssets: experienceAssets,
      experienceMapping: experienceMapping,
      heading: String(source.heading || "הצצה לפני שנכנסים"),
      hint: String(source.hint || "נגיעה או מיקוד מעירים את ההצצה. הכפתור פותח מסך מלא."),
      illustrationLabel: String(source.illustration_label || "המחשה מאושרת · אינה מידע תכנוני או מלאי"),
      backLabel: String(source.back_label || "חזרה לבניין"),
      pageLabel: String(source.page_label || "{current} מתוך {total}"),
      previousLabel: String(source.previous_label || "הקודם"),
      nextLabel: String(source.next_label || "הבא"),
      tools: Object.freeze(tools)
    });
  }

  function previewMarkup(tool) {
    if (tool.id === "view") {
      return '<div class="nlvt-preview nlvt-preview--view" aria-hidden="true"><span class="nlvt-map-road"></span><i class="nlvt-map-anchor"></i><i class="nlvt-map-beam"></i><b>N</b></div>';
    }
    if (tool.id === "interior") {
      return '<div class="nlvt-preview nlvt-preview--interior" data-nlvt-experience-visual="interior" aria-hidden="true"><span class="nlvt-corridor"></span><i class="nlvt-door"></i><i class="nlvt-door-light"></i><span class="nlvt-walk-line"></span></div>';
    }
    if (tool.id === "design") {
      return '<div class="nlvt-preview nlvt-preview--design" aria-hidden="true"><span class="nlvt-plan-room"></span><i class="nlvt-plan-sofa"></i><i class="nlvt-plan-table"></i></div>';
    }
    if (tool.id === "comments") return '<div class="nlvt-preview nlvt-preview--comments" aria-hidden="true"><span class="nlvt-comment-building"></span><i class="nlvt-comment-pin nlvt-comment-pin--a"></i><i class="nlvt-comment-pin nlvt-comment-pin--b"></i><i class="nlvt-comment-line"></i></div>';
    return "";
  }

  function sceneButtonsMarkup(groupId, scenes) {
    return '<div class="nlvt-experience-scenes" aria-label="בחירת תמונה">' + scenes.map(function (scene, index) {
      return '<button type="button" data-nlvt-' + groupId + '-scene="' + escapeHtml(scene.id) + '" aria-pressed="' + (index === 0 ? "true" : "false") + '">' + escapeHtml(scene.label) + '</button>';
    }).join("") + '</div>';
  }

  function applyExperienceAsset(node, group, scene) {
    if (!node || !group || !scene) return;
    node.style.setProperty("--nlvt-experience-image", 'url("' + scene.url + '")');
    node.dataset.nlvtExperienceAsset = scene.url;
    node.dataset.nlvtExperienceScene = scene.id;
    node.dataset.experienceAssetId = scene.assetId;
    node.dataset.experienceAssetSha256 = scene.sha256;
    node.dataset.experienceAssetBytes = String(scene.bytes);
    node.dataset.experienceAssetWidth = String(scene.width);
    node.dataset.experienceAssetHeight = String(scene.height);
    node.dataset.experienceKind = scene.experienceKind;
    node.dataset.mappingHotspotId = scene.hotspotId;
    node.dataset.illustrativePosition = JSON.stringify(scene.illustrativePosition);
    node.dataset.representationKind = group.representationKind;
    node.dataset.mappingState = group.mappingState;
    node.dataset.decisionGrade = "false";
  }

  function applySceneButtons(scope, attributeName, group) {
    if (!scope) return;
    group.scenes.forEach(function (scene) {
      var button = scope.querySelector("[" + attributeName + '=\"' + scene.id + '\"]');
      if (!button) return;
      button.style.setProperty("--nlvt-scene-image", 'url("' + scene.url + '")');
      button.dataset.experienceAssetId = scene.assetId;
      button.dataset.experienceAssetSha256 = scene.sha256;
      button.dataset.experienceAssetBytes = String(scene.bytes);
    });
  }

  function findExperienceScene(config, sceneId) {
    var groups = [config.experienceAssets.interior, config.experienceAssets.facilities];
    for (var index = 0; index < groups.length; index += 1) {
      var scene = groups[index].scenes.find(function (candidate) { return candidate.id === sceneId; });
      if (scene) return { group: groups[index], scene: scene };
    }
    return null;
  }

  function toolBodyMarkup(tool, config) {
    var visual = previewMarkup(tool);
    var controls = "";
    if (tool.id === "design") {
      visual = '<div class="nlvt-preview nlvt-preview--design nlvt-tool-design"><span class="nlvt-plan-room" aria-hidden="true"></span><button class="nlvt-plan-sofa" type="button" data-nlvt-sofa aria-label="גררו את הספה"></button><i class="nlvt-plan-table" aria-hidden="true"></i></div>';
      controls = '<p class="nlvt-tool-hint">גררו את הספה ובדקו סידור אחר.</p>';
    }
    if (tool.id === "comments") {
      visual = '<div class="nlvt-preview nlvt-preview--comments nlvt-tool-comments"><span class="nlvt-comment-building" aria-hidden="true"></span><i class="nlvt-comment-pin nlvt-comment-pin--a" aria-hidden="true"></i><i class="nlvt-comment-pin nlvt-comment-pin--b" aria-hidden="true"></i><i class="nlvt-comment-line" aria-hidden="true"></i><i class="nlvt-user-pin" data-nlvt-user-pin hidden aria-hidden="true"></i></div>';
      controls = '<div class="nlvt-comment-actions"><button type="button" data-nlvt-action="annotate">הוסיפו סימון</button><button type="button" data-nlvt-action="prepare">סמנו שאלה</button></div><p class="nlvt-comment-status" data-nlvt-status role="status">דבר אינו נשמר או נשלח החוצה.</p>';
    }
    if (tool.id === "interior") {
      visual = '<div class="nlvt-preview nlvt-preview--interior nlvt-interior-play" data-nlvt-experience-visual="interior" data-nlvt-interior-state="entry" tabindex="0" aria-label="מסלול פנימי מייצג. השתמשו בחצים כדי להתקדם ולהסתובב."><span class="nlvt-corridor"></span><i class="nlvt-door"></i><i class="nlvt-door-light"></i><span class="nlvt-walk-line"></span><i class="nlvt-interior-reticle" aria-hidden="true"></i></div>';
      controls = sceneButtonsMarkup("experience", config.experienceAssets.interior.scenes.concat(config.experienceAssets.facilities.scenes)) + '<div class="nlvt-interior-controls" aria-label="שליטה במסלול"><button type="button" data-nlvt-action="turn-right" aria-label="פנו ימינה">↷</button><button type="button" data-nlvt-action="step">צעד קדימה</button><button type="button" data-nlvt-action="door">פתחו דלת</button><button type="button" data-nlvt-action="light">הדליקו אור</button></div><p class="nlvt-interior-status" data-nlvt-interior-status role="status">אתם בכניסה לחלל.</p>';
    }
    return '<div class="nlvt-tool-body"><div class="nlvt-tool-visual">' + visual + '</div><div class="nlvt-tool-copy"><p>' + escapeHtml(tool.description) + '</p><span class="nlvt-visually-hidden">' + escapeHtml(tool.disclosure + " " + config.illustrationLabel + ". " + config.decision.version + ", בתוקף עד " + config.decision.expiresAt.slice(0, 10)) + '</span>' + controls + '</div></div>';
  }

  function mount(root, options) {
    if (!root || root.nodeType !== 1) throw new Error("A visual-tools root element is required.");
    var opts = options && typeof options === "object" ? options : {};
    var config = normalizeConfig(opts.data, opts.now, opts.expectedProjectContractId, opts.allowedEvidenceReferenceIds, opts.allowedAssetPrefix);
    var compactQuery = typeof matchMedia === "function" ? matchMedia("(max-width: 700px), (max-height: 640px)") : null;
    var activeTool = null;
    var activePreview = config.tools[0].id;
    var page = 0;
    var destroyed = false;

    root.classList.add("nlvt-root");
    root.dataset.projectContractId = config.identity.projectContractId;
    root.dataset.decisionGrade = "false";
    root.dataset.ownerDecisionId = config.decision.ownerDecisionId;
    root.dataset.experienceDecisionId = config.experienceDecision.ownerDecisionId;
    root.dataset.mappingState = "owner_approved_illustrative_mapping";
    root.dataset.sourceCitedMappingState = "not_available";
    root.dataset.sourceCited = "false";
    root.dataset.mappingAnchorCount = String(config.experienceMapping.anchors.length);

    function isCompact() { return !!(compactQuery && compactQuery.matches); }

    function paint() {
      var tiles = config.tools.map(function (tool, index) {
        return '<article class="nlvt-teaser" data-nlvt-tool="' + escapeHtml(tool.id) + '" data-nlvt-index="' + index + '" data-preview-active="' + (tool.id === activePreview ? "true" : "false") + '" data-decision-grade="false" aria-label="' + escapeHtml(tool.title + ". " + tool.description + ". " + config.illustrationLabel + ".") + '">' + previewMarkup(tool) + '<div class="nlvt-teaser-copy"><strong>' + escapeHtml(tool.title) + '</strong><small>' + escapeHtml(tool.description) + '</small></div><button type="button" data-nlvt-open="' + escapeHtml(tool.id) + '" aria-label="' + escapeHtml(tool.openLabel + ": " + tool.title) + '">' + escapeHtml(tool.openLabel) + '</button></article>';
      }).join("");
      root.innerHTML = '<section class="nlvt-surface" aria-labelledby="nlvt-heading"><header><div><strong id="nlvt-heading">' + escapeHtml(config.heading) + '</strong><small>' + escapeHtml(config.hint) + '</small></div><span class="nlvt-disclosure">' + escapeHtml(config.illustrationLabel) + '</span></header><div class="nlvt-track">' + tiles + '</div><nav class="nlvt-pager" aria-label="מעבר בין ההצצות"><button type="button" data-nlvt-page="previous">' + escapeHtml(config.previousLabel) + '</button><span data-nlvt-page-count></span><button type="button" data-nlvt-page="next">' + escapeHtml(config.nextLabel) + '</button></nav></section>';
      applyExperienceAsset(root.querySelector('[data-nlvt-experience-visual="interior"]'), config.experienceAssets.interior, config.experienceAssets.interior.scenes[0]);
      applyPage();
    }

    function applyPage() {
      var teasers = Array.prototype.slice.call(root.querySelectorAll(".nlvt-teaser"));
      page = Math.max(0, Math.min(teasers.length - 1, page));
      teasers.forEach(function (teaser, index) {
        teaser.hidden = isCompact() && index !== page;
        teaser.dataset.previewActive = teaser.dataset.nlvtTool === activePreview ? "true" : "false";
      });
      var count = root.querySelector("[data-nlvt-page-count]");
      if (count) count.textContent = config.pageLabel.replace("{current}", String(page + 1)).replace("{total}", String(teasers.length));
      var previous = root.querySelector('[data-nlvt-page="previous"]');
      var next = root.querySelector('[data-nlvt-page="next"]');
      if (previous) previous.disabled = page === 0;
      if (next) next.disabled = page === teasers.length - 1;
    }

    function activatePreview(teaser) {
      if (!teaser || !root.contains(teaser)) return;
      activePreview = teaser.dataset.nlvtTool;
      var nextPage = Number(teaser.dataset.nlvtIndex);
      if (Number.isInteger(nextPage) && isCompact()) page = nextPage;
      applyPage();
    }

    function installDrag(dialog) {
      var sofa = dialog.querySelector("[data-nlvt-sofa]");
      if (!sofa) return function () {};
      var drag = null;
      function down(event) {
        var box = sofa.parentElement.getBoundingClientRect();
        drag = { startX: event.clientX, startY: event.clientY, x: Number(sofa.dataset.x || 52), y: Number(sofa.dataset.y || 58), width: box.width, height: box.height };
        try { sofa.setPointerCapture(event.pointerId); } catch (_error) {}
        event.preventDefault();
      }
      function move(event) {
        if (!drag) return;
        var x = Math.max(10, Math.min(82, drag.x + (event.clientX - drag.startX) / Math.max(1, drag.width) * 100));
        var y = Math.max(20, Math.min(78, drag.y + (event.clientY - drag.startY) / Math.max(1, drag.height) * 100));
        sofa.dataset.x = x.toFixed(2); sofa.dataset.y = y.toFixed(2);
        sofa.style.setProperty("--nlvt-sofa-x", x + "%"); sofa.style.setProperty("--nlvt-sofa-y", y + "%");
      }
      function up() { drag = null; }
      sofa.addEventListener("pointerdown", down); sofa.addEventListener("pointermove", move);
      sofa.addEventListener("pointerup", up); sofa.addEventListener("pointercancel", up);
      return function () {
        sofa.removeEventListener("pointerdown", down); sofa.removeEventListener("pointermove", move);
        sofa.removeEventListener("pointerup", up); sofa.removeEventListener("pointercancel", up);
      };
    }

    function restoreDocument(snapshot) {
      document.documentElement.style.overflow = snapshot.htmlOverflow;
      document.body.style.overflow = snapshot.bodyOverflow;
      document.body.classList.remove("nlvt-tool-open");
      try { window.scrollTo(snapshot.scrollX, snapshot.scrollY); } catch (_error) {}
    }

    function lockBackground(dialog, snapshot) {
      snapshot.background = Array.prototype.slice.call(document.body.children).filter(function (node) { return node !== dialog; }).map(function (node) {
        var record = { node: node, hadInert: node.hasAttribute("inert"), inert: node.inert === true, ariaHidden: node.getAttribute("aria-hidden") };
        node.inert = true; node.setAttribute("inert", ""); node.setAttribute("aria-hidden", "true");
        return record;
      });
    }

    function restoreBackground(snapshot) {
      (snapshot.background || []).forEach(function (record) {
        if (!record.node || !record.node.isConnected) return;
        record.node.inert = record.inert;
        if (!record.hadInert) record.node.removeAttribute("inert");
        if (record.ariaHidden === null) record.node.removeAttribute("aria-hidden");
        else record.node.setAttribute("aria-hidden", record.ariaHidden);
      });
    }

    function closeTool(restoreFocus) {
      if (!activeTool) return;
      var state = activeTool;
      activeTool = null;
      try { state.cleanup(); } catch (_error) {}
      try { state.dialog.close(); } catch (_error) {}
      if (state.snapshot.disclosure && state.snapshot.disclosure.node) {
        var disclosure = state.snapshot.disclosure;
        if (disclosure.next && disclosure.next.parentNode === disclosure.parent) disclosure.parent.insertBefore(disclosure.node, disclosure.next);
        else disclosure.parent.appendChild(disclosure.node);
      }
      state.dialog.remove();
      restoreBackground(state.snapshot);
      restoreDocument(state.snapshot);
      try { opts.restoreModelState(cloneSnapshot(state.snapshot.modelState)); } catch (_error) {}
      page = state.snapshot.page; activePreview = state.snapshot.activePreview; applyPage();
      if (restoreFocus !== false && state.trigger && state.trigger.isConnected) {
        try { state.trigger.focus({ preventScroll: true }); } catch (_error) { state.trigger.focus(); }
        try { window.scrollTo(state.snapshot.scrollX, state.snapshot.scrollY); } catch (_error) {}
      }
    }

    function openTool(toolId, trigger, activation) {
      var tool = config.tools.find(function (candidate) { return candidate.id === toolId; });
      var requestedExperience = toolId === "interior" ? findExperienceScene(config, activation && activation.sceneId || config.experienceAssets.interior.scenes[0].id) : null;
      var requestedScene = requestedExperience && requestedExperience.scene;
      var requestedAnchor = activation && activation.hotspotId ? config.experienceMapping.anchors.find(function (anchor) { return anchor.hotspotId === activation.hotspotId && anchor.openSurfaceToolId === toolId && (!requestedScene || anchor.sceneIds.indexOf(requestedScene.id) >= 0); }) : null;
      var activationNow = Number.isFinite(opts.now) ? opts.now : Date.now();
      var experienceCurrent = toolId !== "interior" || Date.parse(config.experienceDecision.expiresAt) > activationNow;
      if (!tool || Date.parse(config.decision.expiresAt) <= activationNow || !experienceCurrent || (toolId === "interior" && !requestedExperience) || (activation && activation.hotspotId && !requestedAnchor)) return false;
      if (typeof opts.captureModelState !== "function" || typeof opts.restoreModelState !== "function") return false;
      closeTool(false);
      var modelState;
      try { modelState = cloneSnapshot(opts.captureModelState()); } catch (_error) { return false; }
      var snapshot = {
        modelState: modelState, scrollX: window.scrollX, scrollY: window.scrollY,
        htmlOverflow: document.documentElement.style.overflow, bodyOverflow: document.body.style.overflow,
        page: page, activePreview: activePreview
      };
      var showroomDisclosure = root.querySelector(".nlvt-disclosure");
      if (showroomDisclosure) snapshot.disclosure = { node: showroomDisclosure, parent: showroomDisclosure.parentNode, next: showroomDisclosure.nextSibling };
      var dialog = document.createElement("dialog");
      var headingId = "nlvt-tool-title-" + tool.id;
      dialog.className = "nlvt-dialog"; dialog.dir = root.dir || document.documentElement.dir || "rtl";
      dialog.dataset.nlvtTool = tool.id; dialog.dataset.decisionGrade = "false";
      dialog.dataset.ownerDecisionId = config.decision.ownerDecisionId;
      dialog.dataset.experienceDecisionId = config.experienceDecision.ownerDecisionId;
      dialog.dataset.mappingState = config.experienceMapping.activeState;
      dialog.dataset.sourceCited = "false";
      if (requestedScene) dialog.dataset.nlvtSceneKind = requestedScene.experienceKind;
      if (requestedAnchor) { dialog.dataset.mappingHotspotId = requestedAnchor.hotspotId; dialog.dataset.mappingZoneId = requestedAnchor.illustrativeZoneId; }
      dialog.innerHTML = '<article class="nlvt-tool" aria-labelledby="' + headingId + '"><header><button type="button" data-nlvt-action="back">' + escapeHtml(config.backLabel) + '</button><div><h2 id="' + headingId + '">' + escapeHtml(tool.title) + '</h2></div></header>' + toolBodyMarkup(tool, config) + '</article>';
      if (showroomDisclosure) dialog.querySelector(".nlvt-tool > header > div").appendChild(showroomDisclosure);
      if (tool.id === "interior") applyExperienceAsset(dialog.querySelector('[data-nlvt-experience-visual="interior"]'), requestedExperience.group, requestedScene);
      applySceneButtons(dialog, "data-nlvt-experience-scene", config.experienceAssets.interior);
      applySceneButtons(dialog, "data-nlvt-experience-scene", config.experienceAssets.facilities);
      if (tool.id === "interior" && requestedScene) dialog.querySelectorAll("[data-nlvt-experience-scene]").forEach(function (button) {
        var sceneId = button.dataset.nlvtExperienceScene;
        button.setAttribute("aria-pressed", sceneId === requestedScene.id ? "true" : "false");
      });
      var cleanupDrag = installDrag(dialog);
      function click(event) {
        var control = event.target.closest("[data-nlvt-action]");
        if (!control) return;
        if (control.dataset.nlvtAction === "back") closeTool(true);
        if (control.dataset.nlvtAction === "annotate") {
          var pin = dialog.querySelector("[data-nlvt-user-pin]");
          if (pin) { pin.hidden = false; pin.setAttribute("aria-hidden", "false"); }
        }
        if (control.dataset.nlvtAction === "prepare") {
          var status = dialog.querySelector("[data-nlvt-status]");
          dialog.dataset.commentState = "prepared_no_write";
          dialog.dataset.idempotencyReference = "proposal:" + config.identity.projectContractId + ":comments:" + config.decision.version;
          if (status) status.textContent = "השאלה הוכנה במכשיר זה בלבד; דבר לא נשמר ולא נשלח החוצה.";
        }
        if (["turn-right", "step", "door", "light"].indexOf(control.dataset.nlvtAction) >= 0) updateInterior(control.dataset.nlvtAction);
      }
      function cancel(event) { event.preventDefault(); closeTool(true); }
      dialog.addEventListener("click", click); dialog.addEventListener("cancel", cancel);
      var interior = dialog.querySelector("[data-nlvt-interior-state]");
      var interiorState = { step: 0, turn: 0, door: false, light: false };
      function updateInterior(action) {
        if (!interior) return;
        if (action === "step") interiorState.step = Math.min(3, interiorState.step + 1);
        if (action === "turn-right") interiorState.turn = (interiorState.turn + 1) % 4;
        if (action === "door") interiorState.door = !interiorState.door;
        if (action === "light") interiorState.light = !interiorState.light;
        interior.dataset.nlvtInteriorState = "step-" + interiorState.step;
        interior.dataset.turn = String(interiorState.turn); interior.dataset.doorOpen = String(interiorState.door); interior.dataset.lightOn = String(interiorState.light);
        interior.style.setProperty("--nlvt-walk-step", String(interiorState.step)); interior.style.setProperty("--nlvt-turn", interiorState.turn * 5 + "deg");
        var interiorStatus = dialog.querySelector("[data-nlvt-interior-status]");
        if (interiorStatus) interiorStatus.textContent = "מיקום בחלל: צעד " + interiorState.step + ", דלת " + (interiorState.door ? "פתוחה" : "סגורה") + ", אור " + (interiorState.light ? "דלוק" : "כבוי") + ".";
      }
      function interiorKeys(event) {
        if (!interior) return;
        var action = event.key === "ArrowUp" ? "step" : event.key === "ArrowRight" ? "turn-right" : event.key === "Enter" ? "door" : event.key.toLowerCase() === "l" ? "light" : "";
        if (action) { event.preventDefault(); updateInterior(action); }
      }
      if (interior) interior.addEventListener("keydown", interiorKeys);
      function experienceSceneClick(event) {
        var button = event.target.closest("[data-nlvt-experience-scene]");
        if (!button || !interior) return;
        var experience = findExperienceScene(config, button.dataset.nlvtExperienceScene);
        if (!experience) return;
        applyExperienceAsset(interior, experience.group, experience.scene);
        dialog.dataset.nlvtSceneKind = experience.scene.experienceKind;
        var anchor = config.experienceMapping.anchors.find(function (candidate) { return candidate.sceneIds.indexOf(experience.scene.id) >= 0; });
        if (anchor) { dialog.dataset.mappingHotspotId = anchor.hotspotId; dialog.dataset.mappingZoneId = anchor.illustrativeZoneId; }
        dialog.querySelectorAll("[data-nlvt-experience-scene]").forEach(function (candidate) { candidate.setAttribute("aria-pressed", candidate === button ? "true" : "false"); });
      }
      dialog.addEventListener("click", experienceSceneClick);
      document.body.appendChild(dialog);
      lockBackground(dialog, snapshot);
      document.documentElement.style.overflow = "hidden"; document.body.style.overflow = "hidden";
      document.body.classList.add("nlvt-tool-open");
      activeTool = { dialog: dialog, trigger: trigger, snapshot: snapshot, cleanup: function () { cleanupDrag(); if (interior) interior.removeEventListener("keydown", interiorKeys); dialog.removeEventListener("click", experienceSceneClick); dialog.removeEventListener("click", click); dialog.removeEventListener("cancel", cancel); } };
      if (trigger && document.activeElement === trigger) trigger.blur();
      try { dialog.showModal(); } catch (_error) { closeTool(false); return false; }
      var back = dialog.querySelector('[data-nlvt-action="back"]'); if (back) back.focus();
      return true;
    }

    function onClick(event) {
      var open = event.target.closest("[data-nlvt-open]");
      if (open && root.contains(open)) { openTool(open.dataset.nlvtOpen, open); return; }
      var pager = event.target.closest("[data-nlvt-page]");
      if (!pager || !root.contains(pager)) return;
      page += pager.dataset.nlvtPage === "next" ? 1 : -1;
      activePreview = config.tools[Math.max(0, Math.min(config.tools.length - 1, page))].id;
      applyPage();
    }
    function onIntent(event) { activatePreview(event.target.closest && event.target.closest(".nlvt-teaser")); }
    function onCompactChange() { applyPage(); }
    root.addEventListener("click", onClick); root.addEventListener("pointerover", onIntent);
    root.addEventListener("pointerdown", onIntent); root.addEventListener("focusin", onIntent);
    if (compactQuery) {
      if (compactQuery.addEventListener) compactQuery.addEventListener("change", onCompactChange);
      else compactQuery.addListener(onCompactChange);
    }
    paint();

    return Object.freeze({
      config: config,
      openTool: function (toolId, trigger, activation) {
        var safeTrigger = trigger && trigger.nodeType === 1 && trigger.isConnected ? trigger : root.querySelector('[data-nlvt-open="' + toolId + '"]');
        return openTool(toolId, safeTrigger, activation);
      },
      closeTool: function () { closeTool(true); },
      destroy: function () {
        if (destroyed) return; destroyed = true; closeTool(false);
        root.removeEventListener("click", onClick); root.removeEventListener("pointerover", onIntent);
        root.removeEventListener("pointerdown", onIntent); root.removeEventListener("focusin", onIntent);
        if (compactQuery) {
          if (compactQuery.removeEventListener) compactQuery.removeEventListener("change", onCompactChange);
          else compactQuery.removeListener(onCompactChange);
        }
        root.replaceChildren();
      }
    });
  }

  return Object.freeze({ OWNER_DECISION_ID: OWNER_DECISION_ID, EXPERIENCE_DECISION_ID: EXPERIENCE_DECISION_ID, ALLOWED_TOOLS: ALLOWED_TOOLS, normalizeConfig: normalizeConfig, mount: mount });
});
