/* NadLan unit selection adapter 1.0.0
 * Layers on top of the current showroom contract. It does not replace engine.js.
 * One event is authoritative: nadlan:unit-selected.
 */
(function (window, document) {
  'use strict';

  const VERSION = '1.0.0';
  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
  const distance3 = (a, b) => Math.hypot(Number(a.x) - Number(b[0]), Number(a.y) - Number(b[1]), Number(a.z) - Number(b[2]));
  const dot3 = (a, b) => Number(a.x) * Number(b[0]) + Number(a.y) * Number(b[1]) + Number(a.z) * Number(b[2]);

  class SelectionStore {
    constructor(options) {
      this.projectId = options.projectId;
      this.getUnit = options.getUnit;
      this.onSelect = options.onSelect || function () {};
      this.unitId = options.initialUnitId || null;
    }

    select(unitId, origin, evidence) {
      const unit = this.getUnit(unitId);
      if (!unit) return false;
      const previousUnitId = this.unitId;
      this.unitId = unitId;
      const url = new URL(window.location.href);
      url.searchParams.set('unit_id', unitId);
      window.history.replaceState({ unit_id: unitId }, '', `${url.pathname}${url.search}${url.hash}`);
      const detail = {
        version: VERSION,
        project_id: this.projectId,
        unit_id: unitId,
        previous_unit_id: previousUnitId,
        origin,
        floor: unit.floor,
        line: unit.line,
        azimuth: unit.directionAzimuth,
        evidence: evidence || null,
        timestamp: new Date().toISOString()
      };
      window.NADLAN_SELECTION = detail;
      this.onSelect(unit, detail);
      document.dispatchEvent(new CustomEvent('nadlan:unit-selected', { detail }));
      return true;
    }
  }

  class ModelViewerSurfaceAdapter {
    constructor(options) {
      this.model = options.model;
      this.overlay = options.overlay;
      this.units = options.units;
      this.store = options.store;
      this.maxMovePx = options.maxMovePx || 6;
      this.maxTapMs = options.maxTapMs || 900;
      this.maxVisibleHotspots = options.maxVisibleHotspots || 5;
      this.pointerStart = null;
      this.frame = 0;
    }

    install() {
      this.model.addEventListener('load', () => this.render());
      this.model.addEventListener('camera-change', () => this.project());
      window.addEventListener('resize', () => this.project(), { passive: true });
      const captureTarget = this.model.parentElement;
      captureTarget.addEventListener('pointerdown', (event) => this.pointerDown(event), true);
      captureTarget.addEventListener('pointerup', (event) => this.pointerUp(event), true);
      if (this.model.loaded) this.render();
    }

    pointerDown(event) {
      if (!event.isPrimary || event.button !== 0 || event.composedPath().some((node) => node?.dataset?.projectedUnitId)) return;
      this.pointerStart = { id: event.pointerId, x: event.clientX, y: event.clientY, time: performance.now() };
    }

    pointerUp(event) {
      const start = this.pointerStart;
      this.pointerStart = null;
      if (!start || start.id !== event.pointerId || event.composedPath().some((node) => node?.dataset?.projectedUnitId)) return;
      const movement = Math.hypot(event.clientX - start.x, event.clientY - start.y);
      if (movement > this.maxMovePx || performance.now() - start.time > this.maxTapMs) return;
      const hit = this.model.positionAndNormalFromPoint?.(event.clientX, event.clientY);
      const resolved = this.resolveSurfaceHit(hit);
      if (!resolved) return;
      this.store.select(resolved.unit.id, 'model-surface', {
        point: [hit.position.x, hit.position.y, hit.position.z],
        normal: [hit.normal.x, hit.normal.y, hit.normal.z],
        distance_m: resolved.distance,
        normal_dot: resolved.normalDot
      });
      this.render();
    }

    resolveSurfaceHit(hit) {
      if (!hit?.position || !hit?.normal) return null;
      return this.units.map((unit) => {
        const selection = unit.selection;
        if (!selection?.anchor || !selection?.hitRegion) return null;
        const region = selection.hitRegion;
        if (hit.position.y < region.floorMinY || hit.position.y > region.floorMaxY) return null;
        const normalDot = dot3(hit.normal, selection.anchor.normal);
        if (normalDot < region.minNormalDot) return null;
        const distance = distance3(hit.position, selection.anchor.position);
        if (distance > region.maxSurfaceDistanceM) return null;
        return { unit, distance, normalDot, score: distance + (1 - normalDot) * 2.4 };
      }).filter(Boolean).sort((a, b) => a.score - b.score)[0] || null;
    }

    representatives() {
      const available = this.units.filter((unit) => unit.availability !== 'sold');
      const selected = available.find((unit) => unit.id === this.store.unitId);
      const quantiles = [0, .33, .66, 1].map((ratio) => available[Math.round((available.length - 1) * ratio)]).filter(Boolean);
      return [...new Map([selected, ...quantiles].filter(Boolean).map((unit) => [unit.id, unit])).values()].slice(0, this.maxVisibleHotspots);
    }

    render() {
      this.model.querySelectorAll('.nadlan-unit-anchor').forEach((node) => node.remove());
      this.representatives().forEach((unit) => {
        const anchor = unit.selection.anchor;
        const marker = document.createElement('button');
        marker.className = 'nadlan-unit-anchor';
        marker.slot = `hotspot-${unit.id}`;
        marker.dataset.position = anchor.position.map((value) => `${value}m`).join(' ');
        marker.dataset.normal = anchor.normal.join(' ');
        marker.dataset.unitId = unit.id;
        marker.setAttribute('aria-label', `${unit.label}, קומה ${unit.floor}, ${unit.rooms} חדרים`);
        marker.style.pointerEvents = 'none';
        marker.style.opacity = '0.001';
        this.model.append(marker);
      });
      this.overlay.innerHTML = [...this.model.querySelectorAll('.nadlan-unit-anchor')].map((marker) => {
        const unit = this.units.find((item) => item.id === marker.dataset.unitId);
        return `<button class="nadlan-projected-hotspot" data-projected-unit-id="${unit.id}" data-slot="${marker.slot}" aria-label="${unit.label}, קומה ${unit.floor}, ${unit.rooms} חדרים">${unit.floor}</button>`;
      }).join('');
      this.overlay.querySelectorAll('.nadlan-projected-hotspot').forEach((button) => button.addEventListener('click', (event) => {
        event.stopPropagation();
        this.store.select(button.dataset.projectedUnitId, 'projected-hotspot', { slot: button.dataset.slot });
        this.render();
      }));
      this.project();
    }

    project() {
      cancelAnimationFrame(this.frame);
      this.frame = requestAnimationFrame(() => {
        const rect = this.model.getBoundingClientRect();
        this.overlay.querySelectorAll('.nadlan-projected-hotspot').forEach((button) => {
          const projection = this.model.queryHotspot?.(button.dataset.slot);
          const point = projection?.canvasPosition;
          const inside = point && point.x >= 0 && point.y >= 0 && point.x <= this.model.clientWidth && point.y <= this.model.clientHeight;
          const hit = inside ? this.model.positionAndNormalFromPoint?.(rect.left + point.x, rect.top + point.y) : null;
          const surfaceDelta = hit && projection?.position ? distance3(hit.position, [projection.position.x, projection.position.y, projection.position.z]) : Infinity;
          button.hidden = !projection?.facingCamera || !inside || surfaceDelta > 4;
          if (!button.hidden) {
            button.style.left = `${clamp(point.x, 22, this.model.clientWidth - 22)}px`;
            button.style.top = `${clamp(point.y, 22, this.model.clientHeight - 22)}px`;
            button.dataset.surfaceDelta = surfaceDelta.toFixed(2);
          }
        });
      });
    }
  }

  class ThreeSemanticMeshAdapter {
    constructor(options) {
      this.THREE = options.THREE;
      this.camera = options.camera;
      this.domElement = options.domElement;
      this.pickRoot = options.pickRoot;
      this.store = options.store;
      this.raycaster = new options.THREE.Raycaster();
      this.pointer = new options.THREE.Vector2();
    }

    pick(clientX, clientY) {
      const rect = this.domElement.getBoundingClientRect();
      this.pointer.x = ((clientX - rect.left) / rect.width) * 2 - 1;
      this.pointer.y = -((clientY - rect.top) / rect.height) * 2 + 1;
      this.raycaster.setFromCamera(this.pointer, this.camera);
      const hit = this.raycaster.intersectObject(this.pickRoot, true).find((item) => this.unitId(item.object));
      if (!hit) return null;
      const unitId = this.unitId(hit.object);
      this.store.select(unitId, 'semantic-mesh', {
        object_name: hit.object.name,
        face_index: hit.faceIndex,
        instance_id: hit.instanceId ?? null,
        point: hit.point.toArray(),
        distance: hit.distance
      });
      return hit;
    }

    unitId(object) {
      let node = object;
      while (node) {
        if (node.userData?.unit_id) return node.userData.unit_id;
        const match = /^UNIT_PICK__(.+)$/.exec(node.name || '');
        if (match) return match[1];
        node = node.parent;
      }
      return null;
    }
  }

  window.NadlanUnitSelection = { VERSION, SelectionStore, ModelViewerSurfaceAdapter, ThreeSemanticMeshAdapter };
})(window, document);
