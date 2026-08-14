/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Exact commercial floor selection for the existing vanilla-JS showroom engine.
 *
 * Replaces one overlapping 38px HTML hotspot per floor with:
 *   1) model-space hit testing against an explicit floor-range calibration;
 *   2) a native select as the accessible and low-power equivalent;
 *   3) previous/next controls that use the same canonical selection function.
 *
 * No framework or new library is required. model-viewer is already present.
 */
(function commercialFloorSelectionModule(window, document) {
  "use strict";

  var MODULE_EVENT = "nadlan:commercial-asset-selected";
  var ROUTE_EVENT = "nadlan:commercial-asset-route-change";

  function text(value) {
    return value == null ? "" : String(value);
  }

  function finite(value) {
    var number = Number(value);
    return Number.isFinite(number) ? number : null;
  }

  function contractAdapter() {
    if (
      !window.NadlanCommercialContractAdapter ||
      typeof window.NadlanCommercialContractAdapter.normalizeAvailabilityStatus !== "function"
    ) {
      throw new Error(
        "Load commercial-decision-surface.js before commercial-floor-selection.js."
      );
    }
    return window.NadlanCommercialContractAdapter;
  }

  function normalizeStatus(value) {
    return contractAdapter().normalizeAvailabilityStatus(value);
  }

  function identityKey(buildingId, towerId, floorId) {
    return [buildingId, towerId, floorId, ""].map(function (value) {
      return text(value).trim().toLowerCase();
    }).join("|");
  }

  function normalizeRange(raw, index) {
    raw = raw && typeof raw === "object" ? raw : {};
    var buildingId = text(raw.buildingId || raw.building_id).trim().toLowerCase();
    var towerId = text(raw.towerId || raw.tower_id).trim().toLowerCase();
    var towerLabel = text(raw.towerLabel || raw.tower_label).trim();
    var floorId = text(raw.floorId || raw.floor_id).trim();
    var canonicalIdentityKey = identityKey(buildingId, towerId, floorId);
    var suppliedIdentityKey = text(raw.identityKey || raw.identity_key).trim().toLowerCase();
    var minY = finite(raw.minY != null ? raw.minY : raw.min_y);
    var maxY = finite(raw.maxY != null ? raw.maxY : raw.max_y);
    if (
      !buildingId ||
      !towerId ||
      !towerLabel ||
      !floorId ||
      (suppliedIdentityKey && suppliedIdentityKey !== canonicalIdentityKey) ||
      minY == null ||
      maxY == null ||
      maxY <= minY
    ) {
      throw new Error("Invalid commercial floor range at index " + index);
    }
    var adapter = contractAdapter();
    var availability = adapter.normalizeEvidenceEnvelope(raw.availability);
    var calibrationEvidence = adapter.normalizeEvidenceEnvelope(
      raw.calibrationEvidence || raw.calibration_evidence
    );
    var status = normalizeStatus(raw.status);
    if (status !== "unknown" && availability.state !== "verified") status = "unknown";
    return {
      buildingId: buildingId,
      towerId: towerId,
      towerLabel: towerLabel,
      floorId: floorId,
      identityKey: canonicalIdentityKey,
      minY: minY,
      maxY: maxY,
      // Deliberately fail closed. Omitted, null, strings, 0 and false do not
      // become selectable; only the adapter's literal boolean true survives.
      selectable: raw.selectable === true && calibrationEvidence.state === "verified",
      displayOrder: finite(raw.displayOrder != null ? raw.displayOrder : raw.display_order),
      label: text(raw.label || floorId).trim() || floorId,
      zone: text(raw.zone).trim(),
      zoneEvidence: adapter.normalizeEvidenceEnvelope(raw.zoneEvidence || raw.zone_evidence),
      status: status,
      availability: availability,
      reportedArea: text(raw.reportedArea || raw.reported_area).trim(),
      areaEvidence: adapter.normalizeEvidenceEnvelope(raw.areaEvidence || raw.area_evidence),
      calibrationEvidence: calibrationEvidence
    };
  }

  function validateRanges(input) {
    var ranges = Array.isArray(input) ? input.map(normalizeRange) : [];
    ranges.sort(function (a, b) {
      return (
        a.buildingId.localeCompare(b.buildingId) ||
        a.towerId.localeCompare(b.towerId) ||
        a.minY - b.minY ||
        a.floorId.localeCompare(b.floorId)
      );
    });
    var identities = Object.create(null);
    ranges.forEach(function (range, index) {
      if (identities[range.identityKey]) {
        throw new Error("Duplicate commercial floor identity: " + range.identityKey);
      }
      identities[range.identityKey] = true;
      var previous = index ? ranges[index - 1] : null;
      if (
        previous &&
        previous.buildingId === range.buildingId &&
        previous.towerId === range.towerId &&
        range.minY < previous.maxY
      ) {
        throw new Error(
          "Overlapping model-space ranges: " +
            previous.identityKey +
            " and " +
            range.identityKey
        );
      }
    });
    return ranges;
  }

  function resolveFloorAtY(ranges, modelY, towerIdentity) {
    var y = finite(modelY);
    if (y == null) return null;
    towerIdentity = towerIdentity && typeof towerIdentity === "object" ? towerIdentity : {};
    var buildingId = text(towerIdentity.buildingId || towerIdentity.building_id).trim().toLowerCase();
    var towerId = text(towerIdentity.towerId || towerIdentity.tower_id).trim().toLowerCase();
    var scoped = ranges.filter(function (range) {
      return (!buildingId || range.buildingId === buildingId) && (!towerId || range.towerId === towerId);
    });
    var groups = scoped.reduce(function (index, range) {
      var key = identityKey(range.buildingId, range.towerId, "");
      if (!index[key]) index[key] = [];
      index[key].push(range);
      return index;
    }, Object.create(null));
    var matches = [];
    Object.keys(groups).forEach(function (key) {
      var group = groups[key].slice().sort(function (a, b) { return a.minY - b.minY; });
      group.forEach(function (range, index) {
        var isLast = index === group.length - 1;
        if (y >= range.minY && (y < range.maxY || (isLast && y <= range.maxY))) matches.push(range);
      });
    });
    // A hit without a tower calibration must never choose between stacked
    // towers that share the same visible Y interval.
    return matches.length === 1 ? matches[0] : null;
  }

  function selectionList(ranges) {
    return ranges
      .filter(function (range) {
        return range.selectable;
      })
      .slice()
      .sort(function (a, b) {
        var ao = a.displayOrder == null ? a.minY : a.displayOrder;
        var bo = b.displayOrder == null ? b.minY : b.displayOrder;
        return ao - bo;
      });
  }

  function optionLabel(range, labels) {
    labels = labels || {};
    var statusLabels = labels.status || {};
    var pieces = [range.label];
    pieces.push(statusLabels[range.status] || range.status.replace(/_/g, " "));
    if (range.reportedArea) pieces.push(range.reportedArea);
    return pieces.join(" — ");
  }

  function populateNativeSelect(select, ranges, labels) {
    if (!select) return;
    var fragment = document.createDocumentFragment();
    var placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = (labels && labels.chooseFloor) || "Choose a floor";
    fragment.appendChild(placeholder);

    var groups = Object.create(null);
    selectionList(ranges).forEach(function (range) {
      if (!groups[range.towerLabel]) {
        groups[range.towerLabel] = document.createElement("optgroup");
        groups[range.towerLabel].label = range.towerLabel;
        fragment.appendChild(groups[range.towerLabel]);
      }
      var parent = groups[range.towerLabel];
      var option = document.createElement("option");
      option.value = range.identityKey;
      option.textContent = (range.zone ? range.zone + " · " : "") + optionLabel(range, labels);
      parent.appendChild(option);
    });

    select.replaceChildren(fragment);
  }

  function isPrimaryPointer(event) {
    if (event.pointerType === "mouse" && event.button !== 0) return false;
    return event.isPrimary !== false;
  }

  function positionFromHit(hit) {
    if (!hit || typeof hit !== "object") return null;
    if (hit.position && finite(hit.position.y) != null) return hit.position;
    if (hit.point && finite(hit.point.y) != null) return hit.point;
    return null;
  }

  function CommercialFloorSelector(options) {
    options = options || {};
    if (!options.modelViewer) throw new Error("modelViewer is required");
    this.modelViewer = options.modelViewer;
    this.ranges = validateRanges(options.floorRanges || []);
    this.list = selectionList(this.ranges);
    this.selectElement = options.selectElement || null;
    this.previousButton = options.previousButton || null;
    this.nextButton = options.nextButton || null;
    this.liveRegion = options.liveRegion || null;
    this.labels = options.labels || {};
    this.projectId = text(options.projectId).trim();
    this.resolveTowerFromHit =
      typeof options.resolveTowerFromHit === "function" ? options.resolveTowerFromHit : null;
    this.onSelect = typeof options.onSelect === "function" ? options.onSelect : function () {};
    this.onUnavailableRange =
      typeof options.onUnavailableRange === "function" ? options.onUnavailableRange : function () {};
    this.highlightFloor =
      typeof options.highlightFloor === "function" ? options.highlightFloor : function () {};
    this.clearHighlight =
      typeof options.clearHighlight === "function" ? options.clearHighlight : function () {};
    this.selectedFloorId = "";
    this.selectedIdentityKey = "";
    this.abortController = null;
    this.pointerDown = null;
    this.hadSelectedFloorAttribute = this.modelViewer.hasAttribute("data-selected-floor");
    this.priorSelectedFloorAttribute = this.modelViewer.getAttribute("data-selected-floor");
  }

  CommercialFloorSelector.prototype.attach = function attach() {
    this.destroy();
    this.abortController = new AbortController();
    var signal = this.abortController.signal;
    var self = this;

    populateNativeSelect(this.selectElement, this.ranges, this.labels);

    this.modelViewer.addEventListener(
      "pointerdown",
      function (event) {
        if (!isPrimaryPointer(event)) return;
        self.pointerDown = { x: event.clientX, y: event.clientY, id: event.pointerId };
      },
      { signal: signal }
    );

    this.modelViewer.addEventListener(
      "pointerup",
      function (event) {
        if (!isPrimaryPointer(event) || !self.pointerDown || self.pointerDown.id !== event.pointerId) return;
        var distance = Math.hypot(event.clientX - self.pointerDown.x, event.clientY - self.pointerDown.y);
        self.pointerDown = null;
        // A drag rotates the model. Only a tap selects.
        if (distance > 9) return;
        self.selectFromPoint(event.clientX, event.clientY, "model");
      },
      { signal: signal }
    );

    // Back/Forward and a verified deep link use the same selector state as a
    // pointer or native picker selection, but do not emit the buyer-selection
    // event again. This prevents route/event recursion while keeping the model,
    // highlight, select value and previous/next controls coherent.
    this.modelViewer.addEventListener(
      ROUTE_EVENT,
      function (event) {
        var detail = event && event.detail && typeof event.detail === "object" ? event.detail : {};
        var projectContractId = text(detail.projectContractId).trim().toLowerCase();
        if (projectContractId && projectContractId !== self.projectId.toLowerCase()) return;
        if (detail.clear === true) {
          self.clearSelection();
          return;
        }
        var key = identityKey(detail.buildingId, detail.towerId, detail.floorId);
        if (!detail.buildingId || !detail.towerId || !detail.floorId) return;
        self.selectFloor(key, detail.origin || "route", { routeDetail: detail }, {
          emit: false,
          announce: false
        });
      },
      { signal: signal }
    );

    if (this.selectElement) {
      this.selectElement.addEventListener(
        "change",
        function () {
          if (self.selectElement.value) self.selectFloor(self.selectElement.value, "picker");
        },
        { signal: signal }
      );
    }

    if (this.previousButton) {
      this.previousButton.addEventListener(
        "click",
        function () {
          self.move(-1);
        },
        { signal: signal }
      );
    }
    if (this.nextButton) {
      this.nextButton.addEventListener(
        "click",
        function () {
          self.move(1);
        },
        { signal: signal }
      );
    }
    this.updateControls();
    return this;
  };

  CommercialFloorSelector.prototype.selectFromPoint = function selectFromPoint(clientX, clientY, origin) {
    var self = this;
    if (typeof this.modelViewer.positionAndNormalFromPoint !== "function") {
      this.announce(this.labels.modelSelectionUnavailable || "Use the floor picker to choose a floor.");
      return Promise.resolve(null);
    }
    try {
      return Promise.resolve(this.modelViewer.positionAndNormalFromPoint(clientX, clientY))
        .then(function (hit) {
          var position = positionFromHit(hit);
          var towerIdentity = null;
          if (self.resolveTowerFromHit) towerIdentity = self.resolveTowerFromHit(hit, position);
          var range = position ? resolveFloorAtY(self.ranges, position.y, towerIdentity) : null;
          if (!range) {
            self.announce(self.labels.noFloorAtPoint || "No selectable floor at this point.");
            return null;
          }
          if (!range.selectable) {
            self.onUnavailableRange(range, position);
            self.announce(
              (self.labels.nonSelectableFloor || "This building level is not offered for selection.") +
                " " +
                range.label
            );
            return null;
          }
          self.selectFloor(range.identityKey, origin || "model", { modelPosition: position });
          return range;
        })
        .catch(function () {
          self.announce(self.labels.modelSelectionUnavailable || "Use the floor picker to choose a floor.");
          return null;
        });
    } catch (error) {
      self.announce(self.labels.modelSelectionUnavailable || "Use the floor picker to choose a floor.");
      return Promise.resolve(null);
    }
  };

  CommercialFloorSelector.prototype.selectFloor = function selectFloor(selectionKey, origin, detail, behavior) {
    behavior = behavior || {};
    selectionKey = text(selectionKey).trim().toLowerCase();
    var range = this.ranges.find(function (item) {
      return item.identityKey === selectionKey;
    });
    if (!range || !range.selectable) return false;

    this.selectedFloorId = range.floorId;
    this.selectedIdentityKey = range.identityKey;
    if (this.selectElement) this.selectElement.value = range.identityKey;
    this.modelViewer.setAttribute("data-selected-floor", range.identityKey);
    this.highlightFloor(range, detail || {});
    this.updateControls();
    if (behavior.announce !== false) {
      this.announce(
        ((this.labels.selected || "Selected") + " " + optionLabel(range, this.labels)).trim()
      );
    }

    var payload = {
      projectId: this.projectId,
      buildingId: range.buildingId,
      towerId: range.towerId,
      towerLabel: range.towerLabel,
      floorId: range.floorId,
      identityKey: range.identityKey,
      origin: origin || "api",
      range: Object.assign({}, range),
      detail: detail || {}
    };
    if (behavior.emit !== false) {
      this.onSelect(payload);
      this.modelViewer.dispatchEvent(new CustomEvent(MODULE_EVENT, { detail: payload, bubbles: true }));
    }
    return true;
  };

  CommercialFloorSelector.prototype.clearSelection = function clearSelection() {
    var selected = this.ranges.find(
      function (item) { return item.identityKey === this.selectedIdentityKey; }.bind(this)
    ) || null;
    if (selected) this.clearHighlight(selected);
    this.selectedFloorId = "";
    this.selectedIdentityKey = "";
    if (this.selectElement) this.selectElement.value = "";
    this.modelViewer.removeAttribute("data-selected-floor");
    this.updateControls();
    return this;
  };

  CommercialFloorSelector.prototype.move = function move(delta) {
    if (!this.list.length) return;
    var currentIndex = this.list.findIndex(
      function (item) {
        return item.identityKey === this.selectedIdentityKey;
      }.bind(this)
    );
    var targetIndex = currentIndex < 0 ? (delta > 0 ? 0 : this.list.length - 1) : currentIndex + delta;
    if (targetIndex < 0 || targetIndex >= this.list.length) return;
    this.selectFloor(this.list[targetIndex].identityKey, delta < 0 ? "previous" : "next");
  };

  CommercialFloorSelector.prototype.updateControls = function updateControls() {
    var currentIndex = this.list.findIndex(
      function (item) {
        return item.identityKey === this.selectedIdentityKey;
      }.bind(this)
    );
    if (this.previousButton) this.previousButton.disabled = currentIndex <= 0;
    if (this.nextButton) this.nextButton.disabled = currentIndex < 0 || currentIndex >= this.list.length - 1;
  };

  CommercialFloorSelector.prototype.announce = function announce(message) {
    if (!this.liveRegion) return;
    this.liveRegion.textContent = "";
    window.requestAnimationFrame(
      function () {
        this.liveRegion.textContent = text(message);
      }.bind(this)
    );
  };

  CommercialFloorSelector.prototype.destroy = function destroy() {
    var selected = this.ranges.find(
      function (item) { return item.identityKey === this.selectedIdentityKey; }.bind(this)
    ) || null;
    if (this.abortController) this.abortController.abort();
    this.abortController = null;
    this.pointerDown = null;
    if (selected) this.clearHighlight(selected);
    this.selectedFloorId = "";
    this.selectedIdentityKey = "";
    if (this.selectElement) this.selectElement.value = "";
    if (this.hadSelectedFloorAttribute) {
      this.modelViewer.setAttribute("data-selected-floor", this.priorSelectedFloorAttribute);
    } else {
      this.modelViewer.removeAttribute("data-selected-floor");
    }
    this.updateControls();
  };

  window.NadlanCommercialFloorSelector = {
    CommercialFloorSelector: CommercialFloorSelector,
    validateRanges: validateRanges,
    resolveFloorAtY: resolveFloorAtY,
    normalizeStatus: normalizeStatus,
    normalizeRange: normalizeRange,
    eventName: MODULE_EVENT,
    routeEventName: ROUTE_EVENT
  };
})(window, document);
