/**
 * Reference contract, not auto-enqueued and not installed on production.
 * One state owner for model, list, floor selector, plan, map, view, tour and studio.
 */
(function (window) {
  'use strict';
  const subscribers = new Map();
  let resolver = null;
  let state = Object.freeze({ projectId: null, unitId: null, source: null, module: 'project', facilityId: null, configurationId: null, version: 0 });

  function configure(options) {
    resolver = options?.resolveUnit || resolver;
    if (options?.projectId) state = Object.freeze({ ...state, projectId: options.projectId });
    return api;
  }

  function getState() { return state; }

  function subscribe(name, handler) {
    if (!name || typeof handler !== 'function') throw new TypeError('subscribe(name, handler) is required');
    subscribers.set(name, handler);
    handler(state, null);
    return () => subscribers.delete(name);
  }

  function notify(previous) {
    for (const [name, handler] of subscribers) {
      try { handler(state, previous); }
      catch (error) { window.dispatchEvent(new CustomEvent('nadlan:journey-error', { detail: { subscriber: name, error } })); }
    }
    window.dispatchEvent(new CustomEvent('nadlan:journey-change', { detail: state }));
  }

  function setState(patch, options = {}) {
    const previous = state;
    const next = { ...state, ...patch, version: state.version + 1 };
    if (next.unitId && resolver && !resolver(next.unitId)) throw new Error(`Unknown unit_id: ${next.unitId}`);
    state = Object.freeze(next);
    if (options.writeUrl !== false && next.unitId) {
      const url = new URL(window.location.href);
      url.searchParams.set('unit', next.unitId);
      url.searchParams.delete('unit_id');
      window.history.replaceState(window.history.state, '', url);
    }
    notify(previous);
    return state;
  }

  function selectUnit(unitId, source = 'unknown') {
    if (!unitId) throw new TypeError('unitId is required');
    return setState({ unitId, source, module: 'unit' });
  }

  function openModule(module, extra = {}) { return setState({ module, ...extra }); }
  function selectFacility(facilityId, source = 'facilities-list') { return setState({ facilityId, source, module: 'facility' }); }
  function setConfiguration(configurationId) { return setState({ configurationId, module: 'studio' }); }

  function restoreFromUrl() {
    const url = new URL(window.location.href);
    const unitId = url.searchParams.get('unit') || url.searchParams.get('unit_id');
    if (unitId) setState({ unitId, source: 'url' }, { writeUrl: url.searchParams.has('unit_id') });
    return state;
  }

  const api = Object.freeze({ configure, getState, subscribe, setState, selectUnit, openModule, selectFacility, setConfiguration, restoreFromUrl });
  window.NLUnitJourney = api;
})(window);
