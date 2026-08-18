/*
 * Nadlan flagship visual tools — isolated, data-driven proposal runtime.
 * No beacon, storage, form submission, inventory inference or shared-engine mutation.
 */
(function attachFlagshipVisualTools(globalScope, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (globalScope) globalScope.NadlanFlagshipShowroom = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function flagshipFactory() {
  "use strict";

  var OWNER_DECISION_ID = "OWNER-2026-08-15-EINSTEIN-PARITY-TOOLS";
  var EXPERIENCE_DECISION_ID = "OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO";
  var HISTORY_SCHEMA = "nadlan-flagship-tool-history/v1";
  var MEDIA_STATE_SCHEMA = "nadlan-flagship-media-state/v1";
  var HISTORY_STATE_KEY = "__nadlanFlagshipToolHistory";
  var historyMountSequence = 0;
  var ALLOWED_TOOLS = Object.freeze({
    view: "satellite_window_view",
    interior: "governed_scene_walkthrough",
    design: "illustrative_plan_drag"
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
    /* The extensionless edge alias serves the same governed .webp payload. */
    return value === assetPrefix + assetId + ".webp" || value === assetPrefix + assetId;
  }

  function normalizeExperienceScenes(source, groupId, representationKind, assetPrefix, seenAssets, allowedEvidenceReferenceIds) {
    var group = source && typeof source === "object" ? source[groupId] : null;
    var scenes = group && Array.isArray(group.scenes) ? group.scenes : [];
    if (
      !group || group.representation_kind !== representationKind ||
      group.experience_kind !== representationKind ||
      group.mapping_state !== "owner_approved_illustrative_mapping" || group.decision_grade !== false || scenes.length !== 2
    ) throw new Error("The " + groupId + " experience assets are invalid.");
    var seen = Object.create(null);
    return Object.freeze(scenes.map(function (scene) {
      var placementConfidence = scene && scene.placement_confidence;
      var placementRefs = scene && Array.isArray(scene.placement_source_refs) ? scene.placement_source_refs : [];
      if (
        !scene || !/^[a-z0-9][a-z0-9-]*$/.test(scene.id) || seen[scene.id] ||
        !/^[a-z0-9][a-z0-9-]*$/.test(scene.asset_id) || seenAssets.ids[scene.asset_id] || seenAssets.urls[scene.url] ||
        !scene.label || !validLocalAssetUrl(scene.url, assetPrefix, scene.asset_id) ||
        !/^[a-f0-9]{64}$/.test(scene.sha256) || !Number.isSafeInteger(scene.bytes) || scene.bytes <= 0 ||
        !Number.isSafeInteger(scene.width) || scene.width <= 0 || !Number.isSafeInteger(scene.height) || scene.height <= 0 ||
        !/^[a-z0-9][a-z0-9-]*$/.test(scene.hotspot_id) || !Array.isArray(scene.illustrative_position) ||
        scene.illustrative_position.length !== 3 || !scene.illustrative_position.every(Number.isFinite) ||
        scene.open_surface_tool_id !== "interior" || scene.mapping_owner_decision_id !== EXPERIENCE_DECISION_ID ||
        !placementRefs.length || placementRefs.some(function (id, refIndex) { return allowedEvidenceReferenceIds.indexOf(id) < 0 || placementRefs.indexOf(id) !== refIndex; }) ||
        !placementConfidence || typeof placementConfidence !== "object" || Array.isArray(placementConfidence) ||
        Object.keys(placementConfidence).sort().join("\n") !== ["exact_point", "zone"].join("\n") ||
        !Number.isFinite(placementConfidence.zone) || placementConfidence.zone < 0 || placementConfidence.zone > 1 ||
        !Number.isFinite(placementConfidence.exact_point) || placementConfidence.exact_point < 0 || placementConfidence.exact_point > 1 ||
        typeof scene.placement_basis !== "string" || !scene.placement_basis || typeof scene.placement_ambiguity !== "string" || !scene.placement_ambiguity ||
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
        mappingState: "owner_approved_illustrative_mapping", decisionGrade: false,
        mappingOwnerDecisionId: EXPERIENCE_DECISION_ID,
        placementSourceRefs: Object.freeze(placementRefs.slice()),
        placementConfidence: Object.freeze({ zone: placementConfidence.zone, exactPoint: placementConfidence.exact_point }),
        placementBasis: String(scene.placement_basis), placementAmbiguity: String(scene.placement_ambiguity)
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
        scenes: normalizeExperienceScenes(experienceAssetsSource, "interior", "representative_concept", assetPrefix, seenExperienceAssets, allowedEvidenceReferenceIds)
      }),
      facilities: Object.freeze({
        representationKind: "selectable_concept_gallery",
        experienceKind: "selectable_concept_gallery",
        mappingState: "owner_approved_illustrative_mapping",
        decisionGrade: false,
        scenes: normalizeExperienceScenes(experienceAssetsSource, "facilities", "selectable_concept_gallery", assetPrefix, seenExperienceAssets, allowedEvidenceReferenceIds)
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
    ) throw new Error("Illustrative tools must contain exactly view, interior and design once each.");
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
      return '<div class="nlvt-preview nlvt-preview--interior" data-nlvt-experience-visual="interior" aria-hidden="true"></div>';
    }
    if (tool.id === "design") {
      return '<div class="nlvt-preview nlvt-preview--design" aria-hidden="true"><span class="nlvt-plan-room"></span><i class="nlvt-plan-sofa"></i><i class="nlvt-plan-table"></i></div>';
    }
    return "";
  }

  function sceneButtonsMarkup(groupId, scenes) {
    return '<div class="nlvt-experience-scenes" aria-label="בחירת תמונה">' + scenes.map(function (scene, index) {
      return '<button type="button" data-nlvt-' + groupId + '-scene="' + escapeHtml(scene.id) + '" aria-pressed="' + (index === 0 ? "true" : "false") + '">' + escapeHtml(scene.label) + '</button>';
    }).join("") + '</div>';
  }

  function applyExperienceAsset(node, group, scene) {
    if (!node || !group || !scene) return;
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
    var image = node.querySelector("[data-nlvt-experience-image]");
    if (!image) { node.style.setProperty("--nlvt-experience-image", 'url("' + scene.url + '")'); return; }
    var requestId = String((Number(node.dataset.nlvtAssetRequest || 0) || 0) + 1);
    node.dataset.nlvtAssetRequest = requestId;
    node.dataset.nlvtExperienceAssetState = "loading";
    node.setAttribute("aria-busy", "true");
    image.hidden = false;
    image.alt = scene.label + ". המחשה מאושרת שאינה תוכנית מכר או דירה מסוימת.";
    image.width = scene.width;
    image.height = scene.height;
    image.onload = function () {
      if (node.dataset.nlvtAssetRequest !== requestId || node.dataset.nlvtExperienceScene !== scene.id) return;
      node.style.setProperty("--nlvt-experience-image", 'url("' + scene.url + '")');
      node.dataset.nlvtExperienceAssetState = "ready";
      node.removeAttribute("aria-busy");
      node.dispatchEvent(new CustomEvent("nadlan:flagship-v3:experience-asset-state", { bubbles: true, detail: { sceneId: scene.id, state: "ready" } }));
    };
    image.onerror = function () {
      if (node.dataset.nlvtAssetRequest !== requestId || node.dataset.nlvtExperienceScene !== scene.id) return;
      node.style.removeProperty("--nlvt-experience-image");
      node.dataset.nlvtExperienceAssetState = "failed";
      node.removeAttribute("aria-busy");
      image.hidden = true;
      node.dispatchEvent(new CustomEvent("nadlan:flagship-v3:experience-asset-state", { bubbles: true, detail: { sceneId: scene.id, state: "failed" } }));
    };
    image.src = scene.url;
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

  function toolBodyMarkup(tool, config, links) {
    var visual = previewMarkup(tool);
    var controls = "";
    if (tool.id === "view") {
      visual = '<div class="nlfs-window-view" data-nlfs-window-view-host></div>';
      controls = '<div class="nlvt-discovery-links"><a href="' + escapeHtml(links.districtTourUrl) + '">לסיור ברובע שדה דב</a></div><p data-nlfs-unit-bridge-status role="status">אין מלאי דירות מאומת; המבט אינו משויך לדירה, קומה או חזית.</p>';
    }
    if (tool.id === "design") {
      visual = '<div class="nlvt-preview nlvt-preview--design nlvt-tool-design"><span class="nlvt-plan-room" aria-hidden="true"></span><button class="nlvt-plan-sofa" type="button" data-nlvt-sofa data-x="52" data-y="58" aria-label="מיקום ספה בהמחשה" aria-keyshortcuts="ArrowUp ArrowDown ArrowLeft ArrowRight Home" aria-valuetext="52 אחוז לרוחב, 58 אחוז לגובה"></button><i class="nlvt-plan-table" aria-hidden="true"></i></div>';
      controls = '<p class="nlvt-tool-hint">גררו את הספה או השתמשו במקשי החצים. Home מחזיר למיקום הפתיחה.</p><p data-nlvt-design-status role="status">מיקום הספה: 52% לרוחב, 58% לגובה.</p><a class="nlvt-designer-link" href="' + escapeHtml(links.designUrl) + '">להמשך בכלי מעצב הדירה</a>';
    }
    if (tool.id === "interior") {
      visual = '<div class="nlvt-preview nlvt-preview--interior nlvt-interior-play" data-nlvt-experience-visual="interior" data-nlvt-focus="interior-gallery" data-nlvt-interior-state="scene-0" tabindex="0" aria-keyshortcuts="ArrowLeft ArrowRight Home End" aria-label="סיור מודרך בארבע תמונות המחשה מאושרות. השתמשו בחצים למעבר בין התמונות."><img data-nlvt-experience-image alt="" decoding="async"></div>';
      controls = sceneButtonsMarkup("experience", config.experienceAssets.interior.scenes.concat(config.experienceAssets.facilities.scenes)) + '<div class="nlvt-interior-controls" aria-label="מעבר בין תמונות"><button type="button" data-nlvt-action="previous-scene">התמונה הקודמת</button><button type="button" data-nlvt-action="next-scene">התמונה הבאה</button><button type="button" data-nlvt-action="retry-scene" hidden>ניסיון טעינה נוסף</button></div><p class="nlvt-interior-status" data-nlvt-interior-status role="status">טוענים תמונת המחשה 1 מתוך 4…</p><details class="nlfs__evidence nlvt-interior-evidence" data-nlvt-interior-evidence data-decision-grade="false"><summary>מקורות ומגבלות לתמונה</summary><dl><div><dt>החלטה</dt><dd data-nlvt-interior-evidence-decision></dd></div><div><dt>בתוקף מ־</dt><dd data-nlvt-interior-evidence-effective></dd></div><div><dt>אסמכתאות</dt><dd data-nlvt-interior-evidence-sources></dd></div><div><dt>ביטחון</dt><dd data-nlvt-interior-evidence-confidence></dd></div><div><dt>בסיס המיקום</dt><dd data-nlvt-interior-evidence-basis></dd></div><div><dt>מגבלה</dt><dd data-nlvt-interior-evidence-limitation lang="en"></dd></div></dl></details>';
    }
    return '<div class="nlvt-tool-body"><div class="nlvt-tool-visual">' + visual + '</div><div class="nlvt-tool-copy"><p>' + escapeHtml(tool.description) + '</p><span class="nlvt-visually-hidden">' + escapeHtml(tool.disclosure + " " + config.illustrationLabel + ". " + config.decision.version + ", בתוקף עד " + config.decision.expiresAt.slice(0, 10)) + '</span>' + controls + '</div></div>';
  }

  function mount(root, options) {
    if (!root || root.nodeType !== 1) throw new Error("A visual-tools root element is required.");
    var opts = options && typeof options === "object" ? options : {};
    var config = normalizeConfig(opts.data, opts.now, opts.expectedProjectContractId, opts.allowedEvidenceReferenceIds, opts.allowedAssetPrefix);
    function safeLocalLink(value, expectedPath) {
      try { var url = new URL(String(value || ""), window.location.origin); return url.origin === window.location.origin && url.pathname === expectedPath && !url.search && !url.hash ? url.href : ""; } catch (_error) { return ""; }
    }
    var integrationLinks = {
      designUrl: safeLocalLink(opts.designUrl, "/tour/designer/"),
      districtTourUrl: safeLocalLink(opts.districtTourUrl, "/tour/sde-dov/")
    };
    if (!integrationLinks.designUrl || !integrationLinks.districtTourUrl || typeof opts.mountWindowView !== "function") throw new Error("The Einstein integration links are invalid.");
    var compactQuery = typeof matchMedia === "function" ? matchMedia("(max-width: 700px), (max-height: 640px)") : null;
    var activeTool = null;
    var activePreview = config.tools[0].id;
    var page = 0;
    var destroyed = false;
    var historyInstanceId = config.identity.projectContractId + ":" + String(++historyMountSequence);
    var historyRevision = 0;
    var historyReady = false;
    var historyRestoring = false;
    var historySyncTimer = null;
    var historyClosePending = false;
    var departedToolHistory = null;
    var deferredMediaState = null;

    root.classList.add("nlvt-root");
    root.dataset.projectContractId = config.identity.projectContractId;
    root.dataset.decisionGrade = "false";
    root.dataset.ownerDecisionId = config.decision.ownerDecisionId;
    root.dataset.experienceDecisionId = config.experienceDecision.ownerDecisionId;
    root.dataset.mappingState = "owner_approved_illustrative_mapping";
    root.dataset.sourceCitedMappingState = "not_available";
    root.dataset.sourceCited = "false";
    root.dataset.mappingAnchorCount = String(config.experienceMapping.anchors.length);
    root.dataset.nlvtHistorySchema = HISTORY_SCHEMA;
    root.dataset.nlvtHistoryState = "initializing";
    root.dataset.nlvtMediaStateSchema = MEDIA_STATE_SCHEMA;

    function isCompact() { return !!(compactQuery && compactQuery.matches); }

    function cloneOrNull(value) {
      try { return cloneSnapshot(value); } catch (_error) { return null; }
    }

    function captureModelState() {
      if (typeof opts.captureModelState !== "function") throw new Error("A model-state reader is required.");
      return cloneSnapshot(opts.captureModelState());
    }

    function validModelState(value) {
      var camera = value && typeof value === "object" && value.camera && typeof value.camera === "object" ? value.camera : null;
      if (!camera || !Number.isFinite(camera.azimuth) || !Number.isFinite(camera.elevation) || !Number.isFinite(camera.distance) || camera.distance <= 0 || !Number.isFinite(camera.fieldOfView) || camera.fieldOfView <= 0) return false;
      if (!Array.isArray(camera.target) || camera.target.length !== 3 || !camera.target.every(Number.isFinite)) return false;
      try { return JSON.stringify(value).length <= 65536; } catch (_error) { return false; }
    }

    function plainRecord(value) { return !!value && typeof value === "object" && !Array.isArray(value); }

    function exactKeys(value, keys) {
      return plainRecord(value) && Object.keys(value).sort().join("\n") === keys.slice().sort().join("\n");
    }

    function boundedString(value, maximum) { return typeof value === "string" && value.length <= maximum; }

    function validElementToken(token) {
      if (!exactKeys(token, token && token.kind === "attribute" ? ["kind", "name", "value", "scope", "tag", "index"] : token && token.kind === "tag-index" ? ["kind", "value", "index"] : ["kind", "value"])) return false;
      if (token.kind === "none") return token.value === "";
      if (token.kind === "document") return token.value === "html" || token.value === "body";
      if (token.kind === "id") return boundedString(token.value, 256) && token.value.length > 0;
      if (token.kind === "attribute") {
        return ["data-nlvt-open", "data-nlfs-scene", "data-nlvt-page", "data-nlfs-action", "data-nlvt-action", "data-nlvt-focus", "data-nlvt-experience-scene", "data-nlvt-sofa", "data-nlfs-einstein-view-action"].indexOf(token.name) >= 0
          && boundedString(token.value, 256) && (token.scope === "document" || token.scope === "dialog")
          && /^[a-z][a-z0-9-]*$/.test(token.tag) && Number.isSafeInteger(token.index) && token.index >= 0 && token.index <= 10000;
      }
      return token.kind === "tag-index" && /^[a-z][a-z0-9-]*$/.test(String(token.value || "")) && Number.isSafeInteger(token.index) && token.index >= 0 && token.index <= 10000;
    }

    function validScrollFocus(value) {
      return exactKeys(value, ["scrollX", "scrollY", "dialogScrollTop", "dialogScrollLeft", "focus"])
        && Number.isFinite(value.scrollX) && Math.abs(value.scrollX) <= 10000000
        && Number.isFinite(value.scrollY) && Math.abs(value.scrollY) <= 10000000
        && Number.isFinite(value.dialogScrollTop) && Math.abs(value.dialogScrollTop) <= 10000000
        && Number.isFinite(value.dialogScrollLeft) && Math.abs(value.dialogScrollLeft) <= 10000000
        && validElementToken(value.focus);
    }

    function validPager(value) {
      return exactKeys(value, ["page", "activePreview"])
        && Number.isInteger(value.page) && value.page >= 0 && value.page < config.tools.length
        && config.tools.some(function (tool) { return tool.id === value.activePreview; });
    }

    function validDocumentContract(contract, locked) {
      if (!exactKeys(contract, ["htmlOverflow", "bodyOverflow", "bodyToolOpen", "background"])
        || !boundedString(contract.htmlOverflow, 128) || !boundedString(contract.bodyOverflow, 128)
        || typeof contract.bodyToolOpen !== "boolean" || !Array.isArray(contract.background)
        || contract.background.length > 128 || contract.bodyToolOpen !== (locked === true)) return false;
      if (locked === true && (contract.htmlOverflow !== "hidden" || contract.bodyOverflow !== "hidden")) return false;
      return contract.background.every(function (record, index) {
        if (!exactKeys(record, ["index", "id", "tag", "hadInert", "inert", "ariaHidden"])
          || record.index !== index || !boundedString(record.id, 256) || !/^[a-z][a-z0-9-]*$/.test(record.tag)
          || typeof record.hadInert !== "boolean" || typeof record.inert !== "boolean"
          || !(record.ariaHidden === null || boundedString(record.ariaHidden, 256))) return false;
        return locked !== true || (record.hadInert === true && record.inert === true && record.ariaHidden === "true");
      });
    }

    function validBaseHistoryState(value) {
      return exactKeys(value, ["pager", "modelCamera", "scrollFocus", "inertLocks"])
        && validPager(value.pager) && validModelState(value.modelCamera)
        && validScrollFocus(value.scrollFocus) && validDocumentContract(value.inertLocks, false);
    }

    function validToolHistoryState(value, toolId) {
      if (!exactKeys(value, ["tool", "scene", "selection", "pager", "modelCamera", "scrollFocus", "inertLocks", "material"])
        || !exactKeys(value.tool, ["id", "activation"]) || value.tool.id !== toolId || !Object.prototype.hasOwnProperty.call(ALLOWED_TOOLS, toolId)
        || !exactKeys(value.tool.activation, ["sceneId", "hotspotId"]) || !boundedString(value.tool.activation.sceneId, 128) || !boundedString(value.tool.activation.hotspotId, 128)
        || !exactKeys(value.scene, ["id", "kind"]) || !boundedString(value.scene.id, 128) || !boundedString(value.scene.kind, 128)
        || !exactKeys(value.selection, ["pressedSceneIds", "mappingHotspotId", "mappingZoneId", "designPosition"])
        || !Array.isArray(value.selection.pressedSceneIds) || value.selection.pressedSceneIds.length > 1 || !value.selection.pressedSceneIds.every(function (id) { return boundedString(id, 128); })
        || !boundedString(value.selection.mappingHotspotId, 128) || !boundedString(value.selection.mappingZoneId, 128)
        || !validPager(value.pager) || !validModelState(value.modelCamera) || !validScrollFocus(value.scrollFocus)
        || !validDocumentContract(value.inertLocks, true)
        || !exactKeys(value.material, ["interior", "design", "windowView"])) return false;
      var design = value.material.design;
      var selectionDesign = value.selection.designPosition;
      var windowView = value.material.windowView;
      if (toolId === "design") {
        if (!exactKeys(design, ["x", "y"]) || !exactKeys(selectionDesign, ["x", "y"])
          || !Number.isFinite(design.x) || !Number.isFinite(design.y) || design.x < 10 || design.x > 82 || design.y < 20 || design.y > 78
          || design.x !== selectionDesign.x || design.y !== selectionDesign.y) return false;
      } else if (design !== null || selectionDesign !== null) return false;
      if (toolId === "view") {
        if (!exactKeys(windowView, ["bearing", "pitch"])
          || !Number.isFinite(windowView.bearing) || windowView.bearing < 0 || windowView.bearing >= 360
          || !Number.isFinite(windowView.pitch) || windowView.pitch < 62 || windowView.pitch > 85) return false;
      } else if (windowView !== null) return false;
      if (toolId === "interior") {
        var experience = findExperienceScene(config, value.scene.id);
        var interior = value.material.interior;
        var anchor = experience && config.experienceMapping.anchors.find(function (candidate) { return candidate.sceneIds.indexOf(experience.scene.id) >= 0; });
        if (!experience || !anchor || value.scene.kind !== experience.scene.experienceKind
          || value.tool.activation.sceneId !== value.scene.id || value.tool.activation.hotspotId !== anchor.hotspotId
          || value.selection.pressedSceneIds.length !== 1 || value.selection.pressedSceneIds[0] !== value.scene.id
          || value.selection.mappingHotspotId !== anchor.hotspotId || value.selection.mappingZoneId !== anchor.illustrativeZoneId
          || !exactKeys(interior, ["sceneIndex"])
          || !Number.isInteger(interior.sceneIndex) || interior.sceneIndex < 0
          || interior.sceneIndex >= config.experienceAssets.interior.scenes.length + config.experienceAssets.facilities.scenes.length
          || config.experienceAssets.interior.scenes.concat(config.experienceAssets.facilities.scenes)[interior.sceneIndex].id !== value.scene.id) return false;
      } else if (value.scene.id !== "" || value.scene.kind !== "" || value.tool.activation.sceneId !== "" || value.tool.activation.hotspotId !== ""
        || value.selection.pressedSceneIds.length !== 0 || value.selection.mappingHotspotId !== "" || value.selection.mappingZoneId !== "" || value.material.interior !== null) return false;
      return true;
    }

    function validMediaState(value) {
      if (!exactKeys(value, ["schema", "mode", "toolId", "sceneId", "hotspotId", "page", "activePreview", "material", "decisionGrade"])
        || value.schema !== MEDIA_STATE_SCHEMA || ["surface", "tool", "deferred"].indexOf(value.mode) < 0
        || value.decisionGrade !== false || !Number.isInteger(value.page) || value.page < 0 || value.page >= config.tools.length
        || !config.tools.some(function (tool) { return tool.id === value.activePreview; })
        || !boundedString(value.toolId, 64) || !boundedString(value.sceneId, 128) || !boundedString(value.hotspotId, 128)
        || !exactKeys(value.material, ["interior", "design", "windowView"])) return false;
      if (value.mode === "surface") {
        return value.toolId === "" && value.sceneId === "" && value.hotspotId === ""
          && value.material.interior === null && value.material.design === null && value.material.windowView === null;
      }
      if (!Object.prototype.hasOwnProperty.call(ALLOWED_TOOLS, value.toolId)) return false;
      if (value.toolId === "interior") {
        var experience = findExperienceScene(config, value.sceneId);
        var anchor = experience && config.experienceMapping.anchors.find(function (candidate) { return candidate.sceneIds.indexOf(experience.scene.id) >= 0; });
        return !!experience && !!anchor && anchor.hotspotId === value.hotspotId
          && exactKeys(value.material.interior, ["sceneId"]) && value.material.interior.sceneId === value.sceneId
          && value.material.design === null && value.material.windowView === null;
      }
      if (value.sceneId !== "" || value.hotspotId !== "" || value.material.interior !== null) return false;
      if (value.toolId === "design") {
        return exactKeys(value.material.design, ["x", "y"])
          && Number.isFinite(value.material.design.x) && value.material.design.x >= 10 && value.material.design.x <= 82
          && Number.isFinite(value.material.design.y) && value.material.design.y >= 20 && value.material.design.y <= 78
          && value.material.windowView === null;
      }
      return value.material.design === null && exactKeys(value.material.windowView, ["bearing", "pitch"])
        && Number.isFinite(value.material.windowView.bearing) && value.material.windowView.bearing >= 0 && value.material.windowView.bearing < 360
        && Number.isFinite(value.material.windowView.pitch) && value.material.windowView.pitch >= 62 && value.material.windowView.pitch <= 85;
    }

    function surfaceMediaState() {
      return {
        schema: MEDIA_STATE_SCHEMA,
        mode: "surface",
        toolId: "",
        sceneId: "",
        hotspotId: "",
        page: page,
        activePreview: activePreview,
        material: { interior: null, design: null, windowView: null },
        decisionGrade: false
      };
    }

    function currentMediaState() {
      if (activeTool && typeof activeTool.captureMediaState === "function") return activeTool.captureMediaState();
      return deferredMediaState ? cloneSnapshot(deferredMediaState) : surfaceMediaState();
    }

    function notifyMediaStateChange() {
      var state;
      try { state = currentMediaState(); } catch (_error) { return; }
      if (typeof opts.onMediaStateChange === "function") {
        try { opts.onMediaStateChange(cloneSnapshot(state)); } catch (_error) {}
      }
      root.dispatchEvent(new CustomEvent("nadlan:flagship-v3:media-state-change", { bubbles: false, detail: cloneSnapshot(state) }));
    }

    function elementToken(node) {
      if (!node || node.nodeType !== 1 || !node.isConnected) return { kind: "none", value: "" };
      if (node === document.documentElement) return { kind: "document", value: "html" };
      if (node === document.body) return { kind: "document", value: "body" };
      if (node.id && document.getElementById(node.id) === node) return { kind: "id", value: String(node.id) };
      var attributes = ["data-nlvt-open", "data-nlfs-scene", "data-nlvt-page", "data-nlfs-action", "data-nlvt-action", "data-nlvt-focus", "data-nlvt-experience-scene", "data-nlvt-sofa", "data-nlfs-einstein-view-action"];
      for (var index = 0; index < attributes.length; index += 1) {
        var value = node.getAttribute(attributes[index]);
        if (value !== null) {
          var dialog = node.closest("dialog.nlvt-dialog");
          var attributeScope = dialog || document;
          var attributeTag = String(node.tagName || "").toLowerCase();
          var matches = Array.prototype.slice.call(attributeScope.querySelectorAll("[" + attributes[index] + "]")).filter(function (candidate) {
            return String(candidate.tagName || "").toLowerCase() === attributeTag && candidate.getAttribute(attributes[index]) === value;
          });
          return { kind: "attribute", name: attributes[index], value: value, scope: dialog ? "dialog" : "document", tag: attributeTag, index: Math.max(0, matches.indexOf(node)) };
        }
      }
      var tag = String(node.tagName || "").toLowerCase();
      var candidates = Array.prototype.slice.call(document.querySelectorAll(tag));
      return { kind: "tag-index", value: tag, index: Math.max(0, candidates.indexOf(node)) };
    }

    function resolveElementToken(token, scope) {
      if (!validElementToken(token)) return null;
      if (token.kind === "document") return token.value === "html" ? document.documentElement : token.value === "body" ? document.body : null;
      if (token.kind === "id") return document.getElementById(String(token.value || ""));
      if (token.kind === "attribute") {
        var attributeScope = token.scope === "dialog" ? scope : document;
        if (!attributeScope || (token.scope === "dialog" && !attributeScope.matches("dialog.nlvt-dialog"))) return null;
        var matches = Array.prototype.slice.call(attributeScope.querySelectorAll("[" + token.name + "]")).filter(function (candidate) {
          return String(candidate.tagName || "").toLowerCase() === token.tag && candidate.getAttribute(token.name) === token.value;
        });
        return matches[token.index] || null;
      }
      if (token.kind === "tag-index" && /^[a-z][a-z0-9-]*$/.test(String(token.value || ""))) {
        return document.querySelectorAll(token.value)[Number(token.index) || 0] || null;
      }
      return null;
    }

    function backgroundToken(node, index) {
      return {
        index: index,
        id: node.id ? String(node.id) : "",
        tag: String(node.tagName || "").toLowerCase(),
        hadInert: node.hasAttribute("inert"),
        inert: node.inert === true,
        ariaHidden: node.getAttribute("aria-hidden")
      };
    }

    function captureDocumentContract(dialog) {
      return {
        htmlOverflow: document.documentElement.style.overflow,
        bodyOverflow: document.body.style.overflow,
        bodyToolOpen: document.body.classList.contains("nlvt-tool-open"),
        background: Array.prototype.slice.call(document.body.children).filter(function (node) { return node !== dialog; }).map(backgroundToken)
      };
    }

    function resolveBackgroundToken(record, dialog) {
      var children = Array.prototype.slice.call(document.body.children).filter(function (node) { return node !== dialog; });
      if (record.id) {
        var byId = document.getElementById(record.id);
        if (byId && children.indexOf(byId) >= 0 && String(byId.tagName || "").toLowerCase() === record.tag) return byId;
      }
      var candidate = children[Number(record.index) || 0];
      return candidate && String(candidate.tagName || "").toLowerCase() === record.tag ? candidate : null;
    }

    function documentContractExact(contract, dialog) {
      if (!validDocumentContract(contract, !!dialog)) return false;
      try { return JSON.stringify(captureDocumentContract(dialog)) === JSON.stringify(contract); } catch (_error) { return false; }
    }

    function restoreScrollFocus(contract, scope, fallback, scrollNode) {
      if (!validScrollFocus(contract)) return false;
      var focus = resolveElementToken(contract.focus, scope);
      if (scope && (!focus || !scope.contains(focus))) focus = fallback || null;
      var apply = function () {
        try { window.scrollTo(contract.scrollX, contract.scrollY); } catch (_error) {}
        if (scrollNode && scrollNode.isConnected) {
          scrollNode.scrollTop = contract.dialogScrollTop;
          scrollNode.scrollLeft = contract.dialogScrollLeft;
        }
        if (focus && focus.isConnected && typeof focus.focus === "function") {
          try { focus.focus({ preventScroll: true }); } catch (_error) { focus.focus(); }
          try { window.scrollTo(contract.scrollX, contract.scrollY); } catch (_error) {}
        }
      };
      window.requestAnimationFrame(function () { apply(); window.requestAnimationFrame(apply); });
      return !!focus;
    }

    function baseHistoryState(snapshot, trigger) {
      var modelState = snapshot ? cloneSnapshot(snapshot.modelState) : captureModelState();
      return {
        pager: { page: snapshot ? snapshot.page : page, activePreview: snapshot ? snapshot.activePreview : activePreview },
        modelCamera: modelState,
        scrollFocus: {
          scrollX: snapshot ? snapshot.scrollX : window.scrollX,
          scrollY: snapshot ? snapshot.scrollY : window.scrollY,
          dialogScrollTop: 0,
          dialogScrollLeft: 0,
          focus: elementToken(trigger || document.activeElement)
        },
        inertLocks: snapshot && snapshot.documentContract ? cloneSnapshot(snapshot.documentContract) : captureDocumentContract(null)
      };
    }

    function historyEnvelope(phase, payload) {
      return {
        schema: HISTORY_SCHEMA,
        projectContractId: config.identity.projectContractId,
        instanceId: historyInstanceId,
        revision: ++historyRevision,
        phase: phase,
        payload: cloneSnapshot(payload)
      };
    }

    function ownedHistoryEntry(state) {
      var entry = state && typeof state === "object" ? state[HISTORY_STATE_KEY] : null;
      if (!entry || entry.schema !== HISTORY_SCHEMA || entry.projectContractId !== config.identity.projectContractId || entry.instanceId !== historyInstanceId) return null;
      if (!Number.isSafeInteger(entry.revision) || entry.revision <= 0 || !plainRecord(entry.payload)) return null;
      if (entry.phase === "base") {
        if (!exactKeys(entry.payload, ["base"]) || !validBaseHistoryState(entry.payload.base)) return null;
      } else if (entry.phase === "tool") {
        var toolId = entry.payload.state && entry.payload.state.tool && entry.payload.state.tool.id;
        if (!exactKeys(entry.payload, ["before", "state"]) || !validBaseHistoryState(entry.payload.before) || !validToolHistoryState(entry.payload.state, toolId)) return null;
      } else return null;
      historyRevision = Math.max(historyRevision, entry.revision);
      return entry;
    }

    function mergedHistoryState(entry) {
      var current = window.history.state;
      var next = current && typeof current === "object" && !Array.isArray(current) ? cloneOrNull(current) : {};
      if (!next || typeof next !== "object" || Array.isArray(next)) next = {};
      if (current !== null && (typeof current !== "object" || Array.isArray(current))) next.__nadlanPreviousHistoryState = cloneOrNull(current);
      next[HISTORY_STATE_KEY] = entry;
      return next;
    }

    function writeHistory(method, entry) {
      if (!window.history || typeof window.history[method] !== "function") return false;
      try {
        window.history[method](mergedHistoryState(entry), "", window.location.href);
        historyReady = true;
        root.dataset.nlvtHistoryState = entry.phase;
        return true;
      } catch (_error) {
        historyReady = false;
        root.dataset.nlvtHistoryState = "error";
        return false;
      }
    }

    function replaceBaseHistory(state) {
      if (historyRestoring || activeTool) return false;
      return writeHistory("replaceState", historyEnvelope("base", { base: state || baseHistoryState() }));
    }

    function restoreBaseHistory(state) {
      if (!validBaseHistoryState(state)) return false;
      page = state.pager.page;
      activePreview = state.pager.activePreview;
      applyPage();
      try { opts.restoreModelState(cloneSnapshot(state.modelCamera)); } catch (_error) { return false; }
      var locksExact = documentContractExact(state.inertLocks, null);
      var focusRestored = restoreScrollFocus(state.scrollFocus, null, null);
      root.dataset.nlvtHistoryLocksRestored = locksExact ? "true" : "false";
      return locksExact && focusRestored;
    }

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
      var previousPreview = activePreview;
      var previousPage = page;
      activePreview = teaser.dataset.nlvtTool;
      var nextPage = Number(teaser.dataset.nlvtIndex);
      if (Number.isInteger(nextPage) && isCompact()) page = nextPage;
      applyPage();
      if (historyReady && !historyRestoring && !activeTool && (previousPreview !== activePreview || previousPage !== page)) replaceBaseHistory(baseHistoryState());
      if (previousPreview !== activePreview || previousPage !== page) notifyMediaStateChange();
    }

    function installDrag(dialog, onChange) {
      var sofa = dialog.querySelector("[data-nlvt-sofa]");
      if (!sofa) return function () {};
      var drag = null;
      var status = dialog.querySelector("[data-nlvt-design-status]");
      function paint(x, y) {
        x = Math.max(10, Math.min(82, x)); y = Math.max(20, Math.min(78, y));
        sofa.dataset.x = x.toFixed(2); sofa.dataset.y = y.toFixed(2);
        sofa.style.setProperty("--nlvt-sofa-x", x + "%"); sofa.style.setProperty("--nlvt-sofa-y", y + "%");
        sofa.setAttribute("aria-valuetext", Math.round(x) + " אחוז לרוחב, " + Math.round(y) + " אחוז לגובה");
        if (status) status.textContent = "מיקום הספה: " + Math.round(x) + "% לרוחב, " + Math.round(y) + "% לגובה.";
      }
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
        paint(x, y);
      }
      function up() { if (drag && typeof onChange === "function") onChange(); drag = null; }
      function keys(event) {
        var x = Number(sofa.dataset.x || 52), y = Number(sofa.dataset.y || 58), handled = true;
        if (event.key === "ArrowLeft") x -= 2;
        else if (event.key === "ArrowRight") x += 2;
        else if (event.key === "ArrowUp") y -= 2;
        else if (event.key === "ArrowDown") y += 2;
        else if (event.key === "Home") { x = 52; y = 58; }
        else handled = false;
        if (handled) { event.preventDefault(); paint(x, y); if (typeof onChange === "function") onChange(); }
      }
      sofa.addEventListener("pointerdown", down); sofa.addEventListener("pointermove", move);
      sofa.addEventListener("pointerup", up); sofa.addEventListener("pointercancel", up);
      sofa.addEventListener("keydown", keys);
      return function () {
        sofa.removeEventListener("pointerdown", down); sofa.removeEventListener("pointermove", move);
        sofa.removeEventListener("pointerup", up); sofa.removeEventListener("pointercancel", up);
        sofa.removeEventListener("keydown", keys);
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

    function closeToolInternal(restoreFocus) {
      if (!activeTool) return false;
      var state = activeTool;
      activeTool = null;
      if (historySyncTimer !== null) { window.clearTimeout(historySyncTimer); historySyncTimer = null; }
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
      root.dataset.nlvtHistoryState = "base";
      notifyMediaStateChange();
      return true;
    }

    function syncActiveToolHistory(method) {
      if (!activeTool || historyRestoring || !historyReady) return false;
      var toolState;
      try { toolState = activeTool.captureHistory(); } catch (_error) { return false; }
      var entry = historyEnvelope("tool", { before: activeTool.beforeHistory, state: toolState });
      var written = writeHistory(method || "replaceState", entry);
      if (written) activeTool.historyEntry = entry;
      return written;
    }

    function scheduleActiveToolHistory() {
      if (!activeTool || historyRestoring) return;
      if (historySyncTimer !== null) { window.clearTimeout(historySyncTimer); historySyncTimer = null; }
      syncActiveToolHistory("replaceState");
    }

    function scheduleActiveToolScrollHistory() {
      if (!activeTool || historyRestoring) return;
      if (historySyncTimer === null) syncActiveToolHistory("replaceState");
      else window.clearTimeout(historySyncTimer);
      historySyncTimer = window.setTimeout(function () {
        historySyncTimer = null;
        syncActiveToolHistory("replaceState");
      }, 100);
    }

    function requestCloseTool() {
      if (!activeTool) return false;
      if (historyClosePending) return true;
      scheduleActiveToolHistory();
      var entry = ownedHistoryEntry(window.history && window.history.state);
      if (historyReady && entry && entry.phase === "tool" && typeof window.history.back === "function") {
        root.dataset.nlvtHistoryState = "closing";
        historyClosePending = true;
        try { window.history.back(); return true; } catch (_error) { historyClosePending = false; }
      }
      var before = activeTool.beforeHistory;
      closeToolInternal(true);
      restoreBaseHistory(before);
      replaceBaseHistory(before);
      return true;
    }

    function openTool(toolId, trigger, activation, restoredEntry) {
      var tool = config.tools.find(function (candidate) { return candidate.id === toolId; });
      var requestedExperience = toolId === "interior" ? findExperienceScene(config, activation && activation.sceneId || config.experienceAssets.interior.scenes[0].id) : null;
      var requestedScene = requestedExperience && requestedExperience.scene;
      var requestedAnchor = activation && activation.hotspotId
        ? config.experienceMapping.anchors.find(function (anchor) { return anchor.hotspotId === activation.hotspotId && anchor.openSurfaceToolId === toolId && (!requestedScene || anchor.sceneIds.indexOf(requestedScene.id) >= 0); })
        : toolId === "interior" && requestedScene
          ? config.experienceMapping.anchors.find(function (anchor) { return anchor.openSurfaceToolId === toolId && anchor.sceneIds.indexOf(requestedScene.id) >= 0; })
          : null;
      var activationNow = Number.isFinite(opts.now) ? opts.now : Date.now();
      var experienceCurrent = toolId !== "interior" || Date.parse(config.experienceDecision.expiresAt) > activationNow;
      if (!tool || Date.parse(config.decision.expiresAt) <= activationNow || !experienceCurrent || (toolId === "interior" && !requestedExperience) || (activation && activation.hotspotId && !requestedAnchor)) return false;
      if (typeof opts.captureModelState !== "function" || typeof opts.restoreModelState !== "function") return false;
      if (activeTool) {
        if (activeTool.toolId !== toolId) return false;
        if (restoredEntry && restoredEntry.payload && restoredEntry.payload.state) return activeTool.restoreHistory(restoredEntry.payload.state);
        if (activeTool.dialog && activeTool.dialog.open) {
          var currentBack = activeTool.dialog.querySelector('[data-nlvt-action="back"]');
          if (currentBack) currentBack.focus();
        }
        return true;
      }
      var modelState;
      try { modelState = cloneSnapshot(opts.captureModelState()); } catch (_error) { return false; }
      var snapshot = {
        modelState: modelState, scrollX: window.scrollX, scrollY: window.scrollY,
        htmlOverflow: document.documentElement.style.overflow, bodyOverflow: document.body.style.overflow,
        page: page, activePreview: activePreview, documentContract: captureDocumentContract(null)
      };
      var beforeHistory = restoredEntry && restoredEntry.payload && restoredEntry.payload.before ? cloneOrNull(restoredEntry.payload.before) : baseHistoryState(snapshot, trigger);
      if (!validBaseHistoryState(beforeHistory)) return false;
      if (!restoredEntry) departedToolHistory = null;
      if (restoredEntry) {
        snapshot.modelState = cloneSnapshot(beforeHistory.modelCamera);
        snapshot.scrollX = Number(beforeHistory.scrollFocus && beforeHistory.scrollFocus.scrollX) || 0;
        snapshot.scrollY = Number(beforeHistory.scrollFocus && beforeHistory.scrollFocus.scrollY) || 0;
        snapshot.page = Number(beforeHistory.pager && beforeHistory.pager.page) || 0;
        snapshot.activePreview = beforeHistory.pager && beforeHistory.pager.activePreview;
        snapshot.documentContract = cloneSnapshot(beforeHistory.inertLocks);
      } else if (!replaceBaseHistory(beforeHistory)) {
        return false;
      }
      var showroomDisclosure = root.querySelector(".nlvt-disclosure");
      if (showroomDisclosure) snapshot.disclosure = { node: showroomDisclosure, parent: showroomDisclosure.parentNode, next: showroomDisclosure.nextSibling };
      var dialog = document.createElement("dialog");
      var headingId = "nlvt-tool-title-" + tool.id;
      dialog.className = "nlvt-dialog"; dialog.dir = root.dir || document.documentElement.dir || "rtl";
      dialog.setAttribute("role", "dialog"); dialog.setAttribute("aria-modal", "true"); dialog.setAttribute("aria-labelledby", headingId);
      dialog.dataset.nlvtTool = tool.id; dialog.dataset.decisionGrade = "false";
      dialog.dataset.ownerDecisionId = config.decision.ownerDecisionId;
      dialog.dataset.experienceDecisionId = config.experienceDecision.ownerDecisionId;
      dialog.dataset.mappingState = config.experienceMapping.activeState;
      dialog.dataset.sourceCited = "false";
      if (requestedScene) dialog.dataset.nlvtSceneKind = requestedScene.experienceKind;
      if (requestedAnchor) { dialog.dataset.mappingHotspotId = requestedAnchor.hotspotId; dialog.dataset.mappingZoneId = requestedAnchor.illustrativeZoneId; }
      dialog.innerHTML = '<article class="nlvt-tool" aria-labelledby="' + headingId + '"><header><button type="button" data-nlvt-action="back">' + escapeHtml(config.backLabel) + '</button><div><h2 id="' + headingId + '">' + escapeHtml(tool.title) + '</h2></div></header>' + toolBodyMarkup(tool, config, integrationLinks) + '</article>';
      if (showroomDisclosure) dialog.querySelector(".nlvt-tool > header > div").appendChild(showroomDisclosure);
      if (tool.id === "interior") applyExperienceAsset(dialog.querySelector('[data-nlvt-experience-visual="interior"]'), requestedExperience.group, requestedScene);
      applySceneButtons(dialog, "data-nlvt-experience-scene", config.experienceAssets.interior);
      applySceneButtons(dialog, "data-nlvt-experience-scene", config.experienceAssets.facilities);
      if (tool.id === "interior" && requestedScene) dialog.querySelectorAll("button[data-nlvt-experience-scene]").forEach(function (button) {
        var sceneId = button.dataset.nlvtExperienceScene;
        button.setAttribute("aria-pressed", sceneId === requestedScene.id ? "true" : "false");
      });
      function materialChanged() { scheduleActiveToolHistory(); notifyMediaStateChange(); }
      var cleanupDrag = installDrag(dialog, materialChanged);
      var windowViewController = tool.id === "view"
        ? opts.mountWindowView(dialog.querySelector("[data-nlfs-window-view-host]"), materialChanged)
        : { destroy: function () {}, getState: function () { return null; }, restoreState: function () { return false; } };
      if (!windowViewController || typeof windowViewController.destroy !== "function" || typeof windowViewController.getState !== "function" || typeof windowViewController.restoreState !== "function") return false;
      function click(event) {
        var control = event.target.closest("[data-nlvt-action]");
        if (!control) return;
        if (control.dataset.nlvtAction === "back") { event.preventDefault(); requestCloseTool(); return; }
        if (control.dataset.nlvtAction === "retry-scene" && interior) {
          var retryScene = interiorScenes[interiorState.sceneIndex];
          var retryExperience = retryScene && findExperienceScene(config, retryScene.id);
          if (retryExperience) applyExperienceAsset(interior, retryExperience.group, retryExperience.scene);
          paintInterior();
          return;
        }
        if (["previous-scene", "next-scene"].indexOf(control.dataset.nlvtAction) >= 0) updateInterior(control.dataset.nlvtAction);
        scheduleActiveToolHistory();
      }
      function cancel(event) { event.preventDefault(); requestCloseTool(); }
      function trapFocus(event) {
        if (event.key !== "Tab") return;
        var focusable = Array.prototype.slice.call(dialog.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])')).filter(function (node) { return !node.hidden && node.getClientRects().length > 0; });
        if (!focusable.length) { event.preventDefault(); dialog.focus(); return; }
        var first = focusable[0], last = focusable[focusable.length - 1];
        if (!dialog.contains(document.activeElement)) { event.preventDefault(); (event.shiftKey ? last : first).focus(); }
        else if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
      dialog.addEventListener("click", click); dialog.addEventListener("cancel", cancel); dialog.addEventListener("keydown", trapFocus);
      var interior = dialog.querySelector("[data-nlvt-interior-state]");
      var interiorScenes = config.experienceAssets.interior.scenes.concat(config.experienceAssets.facilities.scenes);
      var interiorState = { sceneIndex: Math.max(0, interiorScenes.findIndex(function (scene) { return requestedScene && scene.id === requestedScene.id; })) };
      function paintInteriorEvidence(activeScene) {
        if (!activeScene) return;
        var decision = dialog.querySelector("[data-nlvt-interior-evidence-decision]");
        var effective = dialog.querySelector("[data-nlvt-interior-evidence-effective]");
        var sources = dialog.querySelector("[data-nlvt-interior-evidence-sources]");
        var confidence = dialog.querySelector("[data-nlvt-interior-evidence-confidence]");
        var basis = dialog.querySelector("[data-nlvt-interior-evidence-basis]");
        var limitation = dialog.querySelector("[data-nlvt-interior-evidence-limitation]");
        var placement = activeScene.placementConfidence || { zone: 0, exactPoint: 0 };
        if (decision) decision.textContent = activeScene.mappingOwnerDecisionId;
        if (effective) effective.textContent = config.experienceDecision.effectiveAt.slice(0, 10);
        if (sources) sources.textContent = activeScene.placementSourceRefs.length ? activeScene.placementSourceRefs.join(", ") : "לא סופק מקור מרחבי";
        if (confidence) confidence.textContent = "אזור " + Math.round(100 * Number(placement.zone || 0)) + "% · נקודה " + Math.round(100 * Number(placement.exactPoint || 0)) + "%";
        if (basis) basis.textContent = activeScene.placementBasis;
        if (limitation) limitation.textContent = activeScene.placementAmbiguity;
      }
      function paintInterior() {
        if (!interior) return;
        var activeScene = interiorScenes[interiorState.sceneIndex];
        interior.dataset.nlvtInteriorState = "scene-" + interiorState.sceneIndex;
        var interiorStatus = dialog.querySelector("[data-nlvt-interior-status]");
        var retry = dialog.querySelector('[data-nlvt-action="retry-scene"]');
        var assetState = interior.dataset.nlvtExperienceAssetState || "loading";
        if (retry) retry.hidden = assetState !== "failed";
        if (interiorStatus && activeScene) {
          if (assetState === "ready") interiorStatus.textContent = activeScene.label + ". תמונת המחשה " + (interiorState.sceneIndex + 1) + " מתוך " + interiorScenes.length + ".";
          else if (assetState === "failed") interiorStatus.textContent = "תמונת ההמחשה לא נטענה. אפשר לנסות שוב או לבחור תמונה אחרת; לא מוצג תחליף מומצא.";
          else interiorStatus.textContent = "טוענים את " + activeScene.label + ", תמונה " + (interiorState.sceneIndex + 1) + " מתוך " + interiorScenes.length + "…";
        }
        paintInteriorEvidence(activeScene);
      }
      paintInterior();
      function updateInterior(action) {
        if (!interior) return;
        var delta = action === "previous-scene" ? -1 : 1;
        var nextIndex = (interiorState.sceneIndex + delta + interiorScenes.length) % interiorScenes.length;
        selectExperienceScene(interiorScenes[nextIndex].id);
        scheduleActiveToolHistory();
      }
      function interiorKeys(event) {
        if (!interior) return;
        var action = event.key === "ArrowLeft" ? "previous-scene" : event.key === "ArrowRight" ? "next-scene" : "";
        if (action) { event.preventDefault(); updateInterior(action); return; }
        if (event.key === "Home" || event.key === "End") {
          event.preventDefault();
          selectExperienceScene(interiorScenes[event.key === "Home" ? 0 : interiorScenes.length - 1].id);
          scheduleActiveToolHistory();
        }
      }
      if (interior) interior.addEventListener("keydown", interiorKeys);
      function selectExperienceScene(sceneId) {
        if (!interior) return false;
        var experience = findExperienceScene(config, sceneId);
        if (!experience) return false;
        var selectedIndex = interiorScenes.findIndex(function (scene) { return scene.id === sceneId; });
        if (selectedIndex < 0) return false;
        interiorState.sceneIndex = selectedIndex;
        applyExperienceAsset(interior, experience.group, experience.scene);
        dialog.dataset.nlvtSceneKind = experience.scene.experienceKind;
        var anchor = config.experienceMapping.anchors.find(function (candidate) { return candidate.sceneIds.indexOf(experience.scene.id) >= 0; });
        if (anchor) { dialog.dataset.mappingHotspotId = anchor.hotspotId; dialog.dataset.mappingZoneId = anchor.illustrativeZoneId; }
        dialog.querySelectorAll("button[data-nlvt-experience-scene]").forEach(function (candidate) { candidate.setAttribute("aria-pressed", candidate.dataset.nlvtExperienceScene === experience.scene.id ? "true" : "false"); });
        paintInterior();
        notifyMediaStateChange();
        return true;
      }
      function experienceSceneClick(event) {
        var button = event.target.closest("[data-nlvt-experience-scene]");
        if (!button || !selectExperienceScene(button.dataset.nlvtExperienceScene)) return;
        scheduleActiveToolHistory();
      }
      dialog.addEventListener("click", experienceSceneClick);
      function experienceAssetState(event) {
        if (!interior || event.target !== interior || !event.detail || event.detail.sceneId !== interior.dataset.nlvtExperienceScene) return;
        dialog.dataset.nlvtExperienceAssetState = event.detail.state;
        root.dataset.nlvtHistoryAssetRestored = event.detail.state === "ready" ? "true" : "false";
        if (event.detail.state === "failed") root.dataset.nlvtHistoryState = "asset-failed";
        else if (root.dataset.nlvtHistoryState === "asset-failed") root.dataset.nlvtHistoryState = "tool";
        paintInterior();
      }
      dialog.addEventListener("nadlan:flagship-v3:experience-asset-state", experienceAssetState);
      function focusChange() { scheduleActiveToolHistory(); }
      function scrollChange() { scheduleActiveToolScrollHistory(); }
      document.body.appendChild(dialog);
      lockBackground(dialog, snapshot);
      document.documentElement.style.overflow = "hidden"; document.body.style.overflow = "hidden";
      document.body.classList.add("nlvt-tool-open");
      activeTool = {
        toolId: tool.id,
        dialog: dialog,
        trigger: trigger,
        snapshot: snapshot,
        beforeHistory: beforeHistory,
        historyEntry: restoredEntry || null,
        captureMediaState: function () {
          var visual = dialog.querySelector('[data-nlvt-experience-visual="interior"]');
          var sofa = dialog.querySelector("[data-nlvt-sofa]");
          return {
            schema: MEDIA_STATE_SCHEMA,
            mode: "tool",
            toolId: tool.id,
            sceneId: visual ? visual.dataset.nlvtExperienceScene || "" : "",
            hotspotId: visual ? dialog.dataset.mappingHotspotId || "" : "",
            page: page,
            activePreview: activePreview,
            material: {
              interior: visual ? { sceneId: visual.dataset.nlvtExperienceScene || "" } : null,
              design: sofa ? { x: Number(sofa.dataset.x || 52), y: Number(sofa.dataset.y || 58) } : null,
              windowView: tool.id === "view" ? windowViewController.getState() : null
            },
            decisionGrade: false
          };
        },
        restoreMediaState: function (value) {
          if (!validMediaState(value) || value.mode === "surface" || value.toolId !== tool.id) return false;
          page = value.page;
          activePreview = value.activePreview;
          applyPage();
          if (tool.id === "interior" && !selectExperienceScene(value.sceneId)) return false;
          var sofa = dialog.querySelector("[data-nlvt-sofa]");
          if (tool.id === "design") {
            if (!sofa || !value.material.design) return false;
            var x = value.material.design.x, y = value.material.design.y;
            sofa.dataset.x = x.toFixed(2); sofa.dataset.y = y.toFixed(2);
            sofa.style.setProperty("--nlvt-sofa-x", x + "%"); sofa.style.setProperty("--nlvt-sofa-y", y + "%");
            sofa.setAttribute("aria-valuetext", Math.round(x) + " אחוז לרוחב, " + Math.round(y) + " אחוז לגובה");
            var designStatus = dialog.querySelector("[data-nlvt-design-status]");
            if (designStatus) designStatus.textContent = "מיקום הספה: " + Math.round(x) + "% לרוחב, " + Math.round(y) + "% לגובה.";
          }
          if (tool.id === "view" && !windowViewController.restoreState(value.material.windowView)) return false;
          scheduleActiveToolHistory();
          notifyMediaStateChange();
          return true;
        },
        captureHistory: function () {
          var visual = dialog.querySelector('[data-nlvt-experience-visual="interior"]');
          var sofa = dialog.querySelector("[data-nlvt-sofa]");
          var toolBody = dialog.querySelector(".nlvt-tool-body");
          var model = captureModelState();
          if (!validModelState(model)) throw new Error("Current model/camera state is invalid.");
          return {
            tool: { id: tool.id, activation: { sceneId: visual ? visual.dataset.nlvtExperienceScene || "" : "", hotspotId: dialog.dataset.mappingHotspotId || "" } },
            scene: { id: visual ? visual.dataset.nlvtExperienceScene || "" : "", kind: dialog.dataset.nlvtSceneKind || "" },
            selection: {
              pressedSceneIds: Array.prototype.slice.call(dialog.querySelectorAll('button[data-nlvt-experience-scene][aria-pressed="true"]')).map(function (button) { return button.dataset.nlvtExperienceScene; }),
              mappingHotspotId: dialog.dataset.mappingHotspotId || "",
              mappingZoneId: dialog.dataset.mappingZoneId || "",
              designPosition: sofa ? { x: Number(sofa.dataset.x || 52), y: Number(sofa.dataset.y || 58) } : null
            },
            pager: { page: page, activePreview: activePreview },
            modelCamera: model,
            scrollFocus: { scrollX: window.scrollX, scrollY: window.scrollY, dialogScrollTop: toolBody ? toolBody.scrollTop : 0, dialogScrollLeft: toolBody ? toolBody.scrollLeft : 0, focus: elementToken(document.activeElement) },
            inertLocks: captureDocumentContract(dialog),
            material: {
              interior: interior ? { sceneIndex: interiorState.sceneIndex } : null,
              design: sofa ? { x: Number(sofa.dataset.x || 52), y: Number(sofa.dataset.y || 58) } : null,
              windowView: tool.id === "view" ? windowViewController.getState() : null
            }
          };
        },
        restoreHistory: function (value) {
          if (!validToolHistoryState(value, tool.id)) return false;
          historyRestoring = true;
          try {
            page = value.pager.page;
            activePreview = value.pager.activePreview;
            applyPage();
            if (tool.id === "interior" && (!value.scene || !selectExperienceScene(value.scene.id))) return false;
            if (interior && value.material && value.material.interior) {
              var nextInterior = value.material.interior;
              if (!Number.isInteger(nextInterior.sceneIndex) || nextInterior.sceneIndex < 0 || nextInterior.sceneIndex >= interiorScenes.length) return false;
              interiorState = { sceneIndex: nextInterior.sceneIndex };
              paintInterior();
            }
            var sofa = dialog.querySelector("[data-nlvt-sofa]");
            if (sofa && value.material && value.material.design) {
              var x = Number(value.material.design.x), y = Number(value.material.design.y);
              if (!Number.isFinite(x) || !Number.isFinite(y) || x < 10 || x > 82 || y < 20 || y > 78) return false;
              sofa.dataset.x = x.toFixed(2); sofa.dataset.y = y.toFixed(2);
              sofa.style.setProperty("--nlvt-sofa-x", x + "%"); sofa.style.setProperty("--nlvt-sofa-y", y + "%");
              sofa.setAttribute("aria-valuetext", Math.round(x) + " אחוז לרוחב, " + Math.round(y) + " אחוז לגובה");
              var designStatus = dialog.querySelector("[data-nlvt-design-status]");
              if (designStatus) designStatus.textContent = "מיקום הספה: " + Math.round(x) + "% לרוחב, " + Math.round(y) + "% לגובה.";
            }
            if (tool.id === "view" && (!value.material || !windowViewController.restoreState(value.material.windowView))) return false;
            opts.restoreModelState(cloneSnapshot(value.modelCamera));
            var locksRestored = documentContractExact(value.inertLocks, dialog);
            var focusRestored = restoreScrollFocus(value.scrollFocus, dialog, dialog.querySelector('[data-nlvt-action="back"]'), dialog.querySelector(".nlvt-tool-body"));
            var restoredModel = captureModelState();
            var modelRestored = JSON.stringify(restoredModel) === JSON.stringify(value.modelCamera);
            root.dataset.nlvtHistoryLocksRestored = locksRestored ? "true" : "false";
            root.dataset.nlvtHistoryModelRestored = modelRestored ? "true" : "false";
            root.dataset.nlvtHistoryRestoredTool = tool.id;
            root.dataset.nlvtHistoryState = "tool";
            return locksRestored && modelRestored && focusRestored;
          } catch (_error) {
            return false;
          } finally {
            historyRestoring = false;
          }
        },
        cleanup: function () {
          cleanupDrag();
          windowViewController.destroy();
          if (interior) interior.removeEventListener("keydown", interiorKeys);
          dialog.removeEventListener("click", experienceSceneClick);
          dialog.removeEventListener("nadlan:flagship-v3:experience-asset-state", experienceAssetState);
          dialog.removeEventListener("click", click);
          dialog.removeEventListener("cancel", cancel);
          dialog.removeEventListener("keydown", trapFocus);
          dialog.removeEventListener("focusin", focusChange);
          dialog.removeEventListener("scroll", scrollChange, true);
        }
      };
      if (trigger && document.activeElement === trigger) trigger.blur();
      try { dialog.showModal(); } catch (_error) { closeToolInternal(false); return false; }
      var back = dialog.querySelector('[data-nlvt-action="back"]'); if (back) back.focus();
      if (restoredEntry) {
        if (!activeTool.restoreHistory(restoredEntry.payload.state)) { closeToolInternal(true); return false; }
        activeTool.historyEntry = restoredEntry;
      } else if (!syncActiveToolHistory("pushState")) {
        closeToolInternal(true);
        replaceBaseHistory(beforeHistory);
        return false;
      }
      dialog.addEventListener("focusin", focusChange);
      dialog.addEventListener("scroll", scrollChange, true);
      deferredMediaState = null;
      delete root.dataset.nlvtDeferredTool;
      notifyMediaStateChange();
      return true;
    }

    function openToolWithDeferredState(toolId, trigger, activation) {
      var deferred = deferredMediaState && deferredMediaState.toolId === toolId ? cloneSnapshot(deferredMediaState) : null;
      var requestedActivation = activation || (deferred ? { sceneId: deferred.sceneId, hotspotId: deferred.hotspotId } : null);
      if (!openTool(toolId, trigger, requestedActivation)) return false;
      if (!deferred) return true;
      if (activeTool && activeTool.restoreMediaState(deferred)) return true;

      // A deferred deep link is all-or-nothing. Never leave a dialog open in a
      // default state while claiming that the requested camera/material loaded.
      var before = activeTool && activeTool.beforeHistory ? cloneOrNull(activeTool.beforeHistory) : null;
      if (activeTool) closeToolInternal(true);
      if (before) replaceBaseHistory(before);
      deferredMediaState = deferred;
      deferredMediaState.mode = "deferred";
      root.dataset.nlvtDeferredTool = deferred.toolId;
      root.dataset.nlvtHistoryState = "error";
      notifyMediaStateChange();
      return false;
    }

    function onClick(event) {
      var open = event.target.closest("[data-nlvt-open]");
      if (open && root.contains(open)) {
        openToolWithDeferredState(open.dataset.nlvtOpen, open, null);
        return;
      }
      var pager = event.target.closest("[data-nlvt-page]");
      if (!pager || !root.contains(pager)) return;
      page += pager.dataset.nlvtPage === "next" ? 1 : -1;
      activePreview = config.tools[Math.max(0, Math.min(config.tools.length - 1, page))].id;
      applyPage();
      if (historyReady && !historyRestoring && !activeTool) replaceBaseHistory(baseHistoryState());
      notifyMediaStateChange();
    }
    function restoreMediaState(value, restoreOptions) {
      if (!validMediaState(value)) return false;
      page = value.page;
      activePreview = value.activePreview;
      applyPage();
      if (value.mode === "surface") {
        if (activeTool) return false;
        deferredMediaState = null;
        delete root.dataset.nlvtDeferredTool;
        notifyMediaStateChange();
        return true;
      }
      if (activeTool) return activeTool.toolId === value.toolId && activeTool.restoreMediaState(value);
      var shouldOpen = restoreOptions && restoreOptions.allowToolOpen === true;
      if (!shouldOpen) {
        deferredMediaState = cloneSnapshot(value);
        deferredMediaState.mode = "deferred";
        root.dataset.nlvtDeferredTool = value.toolId;
        notifyMediaStateChange();
        return true;
      }
      var trigger = root.querySelector('[data-nlvt-open="' + value.toolId + '"]');
      var activation = { sceneId: value.sceneId, hotspotId: value.hotspotId };
      if (!trigger || !openTool(value.toolId, trigger, activation) || !activeTool) return false;
      return activeTool.restoreMediaState(value);
    }
    function onIntent(event) { activatePreview(event.target.closest && event.target.closest(".nlvt-teaser")); }
    function onCompactChange() { applyPage(); }
    function onPopState(event) {
      if (destroyed) return;
      historyClosePending = false;
      var entry = ownedHistoryEntry(event.state);
      if (!entry || entry.phase === "base") {
        var fallback = activeTool && activeTool.beforeHistory;
        if (activeTool) {
          if (historySyncTimer !== null) { window.clearTimeout(historySyncTimer); historySyncTimer = null; }
          try {
            departedToolHistory = {
              sourceRevision: activeTool.historyEntry && activeTool.historyEntry.revision,
              toolId: activeTool.toolId,
              before: cloneSnapshot(activeTool.beforeHistory),
              state: activeTool.captureHistory()
            };
          } catch (_error) { departedToolHistory = null; }
        }
        historyRestoring = true;
        if (activeTool) closeToolInternal(true);
        var base = entry && entry.payload && entry.payload.base ? entry.payload.base : fallback;
        if (base) restoreBaseHistory(base);
        historyRestoring = false;
        root.dataset.nlvtHistoryState = "base";
        return;
      }
      var reconciledDeparted = departedToolHistory
        && departedToolHistory.sourceRevision === entry.revision
        && departedToolHistory.toolId === entry.payload.state.tool.id;
      var restoredEntry = reconciledDeparted
        ? historyEnvelope("tool", { before: departedToolHistory.before, state: departedToolHistory.state })
        : entry;
      var state = restoredEntry.payload && restoredEntry.payload.state;
      var toolId = state && state.tool && state.tool.id;
      var activation = state && state.tool && state.tool.activation ? {
        sceneId: state.tool.activation.sceneId || "",
        hotspotId: state.tool.activation.hotspotId || ""
      } : {};
      var trigger = resolveElementToken(entry.payload && entry.payload.before && entry.payload.before.scrollFocus && entry.payload.before.scrollFocus.focus);
      if (!trigger || !trigger.isConnected) trigger = root.querySelector('[data-nlvt-open="' + String(toolId || "") + '"]');
      historyRestoring = true;
      var restored = false;
      try {
        if (activeTool && activeTool.toolId !== toolId) closeToolInternal(false);
        restored = !!toolId && openTool(toolId, trigger, activation, restoredEntry);
        if (restored && reconciledDeparted) {
          restored = writeHistory("replaceState", restoredEntry);
          if (restored && activeTool) activeTool.historyEntry = restoredEntry;
          departedToolHistory = null;
        }
      } catch (_error) {
        restored = false;
      }
      historyRestoring = false;
      if (!restored) {
        if (activeTool) closeToolInternal(true);
        var before = entry.payload && entry.payload.before;
        if (before) restoreBaseHistory(before);
        writeHistory("replaceState", historyEnvelope("base", { base: before || baseHistoryState() }));
        root.dataset.nlvtHistoryState = "error";
      }
    }
    root.addEventListener("click", onClick); root.addEventListener("pointerover", onIntent);
    root.addEventListener("pointerdown", onIntent); root.addEventListener("focusin", onIntent);
    window.addEventListener("popstate", onPopState);
    if (compactQuery) {
      if (compactQuery.addEventListener) compactQuery.addEventListener("change", onCompactChange);
      else compactQuery.addListener(onCompactChange);
    }
    paint();
    try {
      if (!replaceBaseHistory(baseHistoryState())) throw new Error("History initialization failed.");
    } catch (_error) {
      historyReady = false;
      root.dataset.nlvtHistoryState = "error";
      root.querySelectorAll("[data-nlvt-open]").forEach(function (button) { button.disabled = true; button.setAttribute("aria-disabled", "true"); });
    }
    notifyMediaStateChange();

    return Object.freeze({
      config: config,
      openTool: function (toolId, trigger, activation) {
        var safeTrigger = trigger && trigger.nodeType === 1 && trigger.isConnected ? trigger : root.querySelector('[data-nlvt-open="' + toolId + '"]');
        return openToolWithDeferredState(toolId, safeTrigger, activation);
      },
      closeTool: function () { return requestCloseTool(); },
      isHistoryReady: function () { return historyReady && root.dataset.nlvtHistoryState !== "error"; },
      getState: function () { return cloneSnapshot(currentMediaState()); },
      restoreState: function (value, restoreOptions) {
        try { return restoreMediaState(cloneSnapshot(value), restoreOptions); } catch (_error) { return false; }
      },
      getCapabilities: function () {
        return {
          schema: "nadlan-flagship-media-capabilities/v1",
          portableStateSchema: MEDIA_STATE_SCHEMA,
          automaticFullscreenFromDeepLink: false,
          deferredExplicitOpen: true,
          browserHistory: historyReady
        };
      },
      syncHistory: function () {
        if (!historyReady || historyRestoring) return false;
        if (activeTool) { scheduleActiveToolHistory(); return historyReady; }
        return replaceBaseHistory(baseHistoryState());
      },
      destroy: function () {
        if (destroyed) return; destroyed = true;
        departedToolHistory = null;
        deferredMediaState = null;
        window.removeEventListener("popstate", onPopState);
        var before = activeTool && activeTool.beforeHistory;
        if (activeTool) closeToolInternal(false);
        if (before && ownedHistoryEntry(window.history && window.history.state)) writeHistory("replaceState", historyEnvelope("base", { base: before }));
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

  return Object.freeze({ OWNER_DECISION_ID: OWNER_DECISION_ID, EXPERIENCE_DECISION_ID: EXPERIENCE_DECISION_ID, HISTORY_SCHEMA: HISTORY_SCHEMA, MEDIA_STATE_SCHEMA: MEDIA_STATE_SCHEMA, ALLOWED_TOOLS: ALLOWED_TOOLS, normalizeConfig: normalizeConfig, mount: mount });
});
