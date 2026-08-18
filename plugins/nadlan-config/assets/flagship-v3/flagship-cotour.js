(function attachFlagshipCoTour(globalScope, factory) {
  "use strict";
  var api = factory(globalScope || {});
  if (typeof module === "object" && module.exports) module.exports = api;
  if (globalScope && globalScope.document) {
    globalScope.NadlanFlagshipCoTour = api;
    api.install(globalScope.document);
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function flagshipCoTourFactory(globalScope) {
  "use strict";

  var REQUEST_SCHEMA = "nadlan-flagship-cotour-request/v1";
  var RESPONSE_SCHEMA = "nadlan-flagship-cotour-response/v1";
  var RUNTIME_SCHEMA = "nadlan-flagship-cotour-runtime/v1";
  var SPATIAL_STATE_SCHEMA = "nadlan-spatial-decision-state/v1";
  var STORAGE_SCHEMA = "nadlan-flagship-cotour-resume/v2";
  var instances = new WeakMap();

  function plain(value) { return !!value && typeof value === "object" && !Array.isArray(value); }
  function exactKeys(value, keys) {
    return plain(value) && Object.keys(value).sort().join("\n") === keys.slice().sort().join("\n");
  }
  function normalizeRoomCode(value) { return String(value || "").toUpperCase().replace(/[\s-]+/g, ""); }
  function validRoomCode(value) { return /^[A-F0-9]{12}$/.test(String(value || "")); }
  function currentOrigin() {
    return globalScope.location && typeof globalScope.location.origin === "string" ? globalScope.location.origin : "https://nad-lan.co.il";
  }
  function safeEndpoint(value, action, origin) {
    try {
      var url = new URL(String(value || ""), origin || currentOrigin());
      var expected = action === "join_poll" ? "join-poll" : action;
      return url.origin === (origin || currentOrigin()) && !url.search && !url.hash
        && new RegExp("/wp-json/nadlan/v1/flagship-cotour/" + expected + "$").test(url.pathname) ? url.href : "";
    } catch (_error) { return ""; }
  }
  function validCapacity(value) {
    return exactKeys(value, ["hosts", "followers", "total"]) && value.hosts === 1 && value.followers === 1 && value.total === 2;
  }
  function validRateMap(value, expected) {
    return exactKeys(value, Object.keys(expected)) && Object.keys(expected).every(function (key) { return value[key] === expected[key]; });
  }
  function validRateLimits(value) {
    return exactKeys(value, ["window_seconds", "global_per_ip", "room"]) && value.window_seconds === 60
      && validRateMap(value.global_per_ip, { create: 5, "join-poll": 90, update: 90, end: 15 })
      && validRateMap(value.room, { "join-poll": 75, update: 90, end: 10 });
  }
  function validAuthorization(value) {
    return exactKeys(value, ["transport", "secure", "same_site", "javascript_readable", "rotation"])
      && value.transport === "same_origin_http_only_cookie" && value.secure === true && value.same_site === "Strict"
      && value.javascript_readable === false && value.rotation === "create_resume_and_each_host_update";
  }
  function normalizeRuntimeContract(source, origin) {
    var rawKeys = ["schema", "enabled", "project_id", "project_contract_id", "endpoints", "ttl_seconds", "poll_interval_ms", "poll_backoff_ms", "max_state_bytes", "capacity", "rate_limits", "authorization"];
    if (!exactKeys(source, rawKeys) || source.schema !== RUNTIME_SCHEMA || source.enabled !== true
      || !Number.isSafeInteger(source.project_id) || source.project_id <= 0
      || !/^[a-z0-9][a-z0-9-]{7,127}$/.test(String(source.project_contract_id || ""))
      || !exactKeys(source.endpoints, ["create", "join_poll", "update", "end"])
      || source.ttl_seconds !== 600 || source.poll_interval_ms !== 1200 || source.max_state_bytes !== 65536
      || !Array.isArray(source.poll_backoff_ms) || source.poll_backoff_ms.join("|") !== "1200|1800|2700|4050|5000"
      || !validCapacity(source.capacity) || !validRateLimits(source.rate_limits) || !validAuthorization(source.authorization)) return null;
    var endpoints = {};
    ["create", "join_poll", "update", "end"].forEach(function (action) {
      endpoints[action] = safeEndpoint(source.endpoints[action], action, origin || currentOrigin());
    });
    if (Object.keys(endpoints).some(function (key) { return !endpoints[key]; })) return null;
    return Object.freeze({
      schema: RUNTIME_SCHEMA,
      enabled: true,
      projectId: source.project_id,
      projectContractId: source.project_contract_id,
      endpoints: Object.freeze(endpoints),
      ttlSeconds: 600,
      pollIntervalMs: 1200,
      pollBackoffMs: Object.freeze(source.poll_backoff_ms.slice()),
      maxStateBytes: 65536,
      capacity: Object.freeze({ hosts: 1, followers: 1, total: 2 }),
      rateLimits: Object.freeze(source.rate_limits),
      authorization: Object.freeze(source.authorization)
    });
  }
  function normalizeProtocolContract(source, origin) {
    if (!plain(source)) return null;
    if (Object.prototype.hasOwnProperty.call(source, "project_id")) return normalizeRuntimeContract(source, origin);
    var keys = ["schema", "enabled", "projectId", "projectContractId", "endpoints", "ttlSeconds", "pollIntervalMs", "pollBackoffMs", "maxStateBytes", "capacity", "rateLimits", "authorization"];
    if (!exactKeys(source, keys) || source.schema !== RUNTIME_SCHEMA || source.enabled !== true
      || !Number.isSafeInteger(source.projectId) || source.projectId <= 0
      || !/^[a-z0-9][a-z0-9-]{7,127}$/.test(String(source.projectContractId || ""))
      || !exactKeys(source.endpoints, ["create", "join_poll", "update", "end"])
      || source.ttlSeconds !== 600 || source.pollIntervalMs !== 1200 || source.maxStateBytes !== 65536
      || !Array.isArray(source.pollBackoffMs) || source.pollBackoffMs.join("|") !== "1200|1800|2700|4050|5000"
      || !validCapacity(source.capacity) || !validRateLimits(source.rateLimits) || !validAuthorization(source.authorization)) return null;
    var endpoints = {};
    ["create", "join_poll", "update", "end"].forEach(function (action) {
      endpoints[action] = safeEndpoint(source.endpoints[action], action, origin || currentOrigin());
    });
    if (Object.keys(endpoints).some(function (key) { return !endpoints[key]; })) return null;
    return Object.freeze(Object.assign({}, source, { endpoints: Object.freeze(endpoints), pollBackoffMs: Object.freeze(source.pollBackoffMs.slice()) }));
  }

  function ProtocolError(code, status, sequence, retryAfterSeconds) {
    this.name = "FlagshipCoTourProtocolError";
    this.code = String(code || "transport_failed");
    this.status = Number(status) || 0;
    this.sequence = Number.isSafeInteger(sequence) ? sequence : null;
    this.retryAfterSeconds = Number.isSafeInteger(retryAfterSeconds) ? retryAfterSeconds : null;
    this.message = this.code;
  }
  ProtocolError.prototype = Object.create(Error.prototype);
  ProtocolError.prototype.constructor = ProtocolError;

  function containsAuthorizationMaterial(value) {
    if (!plain(value)) return false;
    return Object.keys(value).some(function (key) { return /secret|token|credential|authorization/i.test(key); });
  }
  function createProtocolClient(runtimeContract, transport, origin) {
    var contract = normalizeProtocolContract(runtimeContract, origin);
    if (!contract || typeof transport !== "function") throw new Error("A valid co-tour contract and transport are required.");
    function post(action, fields) {
      var payload = Object.assign({ schema: REQUEST_SCHEMA, projectId: contract.projectId, projectContractId: contract.projectContractId }, fields || {});
      var body = JSON.stringify(payload);
      if (body.length > 73728) return Promise.reject(new ProtocolError("payload_too_large", 413));
      var attempt;
      try {
        attempt = transport(contract.endpoints[action], {
          method: "POST",
          credentials: "same-origin",
          cache: "no-store",
          redirect: "error",
          headers: { "Accept": "application/json", "Content-Type": "application/json", "X-Nadlan-Flagship-CoTour": "1" },
          body: body
        });
      } catch (_error) { return Promise.reject(new ProtocolError("transport_failed", 0)); }
      return Promise.resolve(attempt).then(function (response) {
        if (!response || typeof response.status !== "number" || typeof response.text !== "function") throw new ProtocolError("invalid_response", 0);
        if (response.redirected === true) throw new ProtocolError("redirect_rejected", response.status);
        if (response.url) {
          var responseUrl = new URL(response.url, origin || currentOrigin());
          if (responseUrl.origin !== (origin || currentOrigin())) throw new ProtocolError("cross_origin_response", response.status);
        }
        return Promise.resolve(response.text()).then(function (text) {
          if (typeof text !== "string" || text.length > 98304) throw new ProtocolError("invalid_response", response.status);
          var data;
          try { data = JSON.parse(text); } catch (_error) { throw new ProtocolError("invalid_response", response.status); }
          if (!plain(data) || data.schema !== RESPONSE_SCHEMA || typeof data.ok !== "boolean" || containsAuthorizationMaterial(data)) throw new ProtocolError("invalid_response", response.status);
          if (data.ok !== true || response.status < 200 || response.status >= 300) {
            throw new ProtocolError(typeof data.code === "string" ? data.code : "request_failed", response.status, data.sequence, data.retryAfterSeconds);
          }
          return data;
        });
      });
    }
    function followerRequest(intent, roomCode, afterSequence, consent) {
      if (!validRoomCode(roomCode) || !Number.isSafeInteger(afterSequence) || afterSequence < 0) return Promise.reject(new ProtocolError("invalid_join_request", 400));
      return post("join_poll", { roomCode: roomCode, afterSequence: afterSequence, intent: intent, consent: consent === true });
    }
    return Object.freeze({
      create: function () { return post("create", {}); },
      join: function (roomCode, afterSequence) { return followerRequest("join", roomCode, afterSequence, true); },
      poll: function (roomCode, afterSequence) { return followerRequest("poll", roomCode, afterSequence, false); },
      resume: function (roomCode, afterSequence) { return followerRequest("resume", roomCode, afterSequence, false); },
      leave: function (roomCode, afterSequence) { return followerRequest("leave", roomCode, afterSequence, false); },
      update: function (roomCode, sequence, state) {
        if (!validRoomCode(roomCode) || !Number.isSafeInteger(sequence) || sequence < 1 || !plain(state)
          || state.schema !== SPATIAL_STATE_SCHEMA || state.projectContractId !== contract.projectContractId) return Promise.reject(new ProtocolError("invalid_update_request", 400));
        var encoded;
        try { encoded = JSON.stringify(state); } catch (_error) { return Promise.reject(new ProtocolError("invalid_spatial_state", 400)); }
        if (encoded.length > contract.maxStateBytes) return Promise.reject(new ProtocolError("invalid_spatial_state", 400));
        return post("update", { roomCode: roomCode, sequence: sequence, state: state });
      },
      end: function (roomCode, sequence) {
        if (!validRoomCode(roomCode) || !Number.isSafeInteger(sequence) || sequence < 1) return Promise.reject(new ProtocolError("invalid_end_request", 400));
        return post("end", { roomCode: roomCode, sequence: sequence });
      },
      contract: contract
    });
  }

  function restoreFollowerState(flagshipApi, root, state, consentGranted) {
    if (consentGranted !== true || !flagshipApi || typeof flagshipApi.restoreState !== "function" || !root || !plain(state)) return false;
    return flagshipApi.restoreState(root, state, { allowDeeperMedia: true, history: "replace" }) === true;
  }
  function createFollowGate(applyState) {
    var consented = false;
    var manualPaused = false;
    var visibilityPaused = false;
    var destroyed = false;
    var pending = null;
    function flush() {
      if (destroyed || !consented || manualPaused || visibilityPaused || !pending) return false;
      var value = pending;
      pending = null;
      return applyState(value.state, value.sequence) === true;
    }
    return Object.freeze({
      receive: function (state, sequence) { if (destroyed) return false; pending = { state: state, sequence: sequence }; return flush(); },
      setConsent: function (value) { consented = value === true; if (!consented) pending = null; return flush(); },
      hasConsent: function () { return consented; },
      setManualPaused: function (value) { manualPaused = value === true; return flush(); },
      setVisibilityPaused: function (value) { visibilityPaused = value === true; return flush(); },
      isPaused: function () { return manualPaused || visibilityPaused; },
      hasPending: function () { return !!pending; },
      destroy: function () { destroyed = true; consented = false; pending = null; },
      isDestroyed: function () { return destroyed; }
    });
  }
  function createTimerBag(clock) {
    var source = clock || globalScope;
    var ids = new Set();
    return Object.freeze({
      set: function (callback, delay) { var id = source.setTimeout(function () { ids.delete(id); callback(); }, delay); ids.add(id); return id; },
      clear: function (id) { if (ids.has(id)) { source.clearTimeout(id); ids.delete(id); } },
      clearAll: function () { ids.forEach(function (id) { source.clearTimeout(id); }); ids.clear(); },
      size: function () { return ids.size; }
    });
  }

  function storageKey(contract) { return "nlfsct-resume:" + contract.projectContractId; }
  function readStoredSession(storage, contract, nowSeconds) {
    if (!storage || typeof storage.getItem !== "function") return null;
    var raw;
    try { raw = storage.getItem(storageKey(contract)); } catch (_error) { return null; }
    if (!raw || raw.length > 512) return null;
    var value;
    try { value = JSON.parse(raw); } catch (_error) { return null; }
    if (!exactKeys(value, ["schema", "role", "roomCode", "sequence", "expiresAt"]) || value.schema !== STORAGE_SCHEMA
      || ["host", "follower"].indexOf(value.role) < 0 || !validRoomCode(value.roomCode)
      || !Number.isSafeInteger(value.sequence) || value.sequence < 0 || !Number.isSafeInteger(value.expiresAt)
      || value.expiresAt <= nowSeconds || value.expiresAt > nowSeconds + contract.ttlSeconds + 60) return null;
    return value;
  }
  function writeStoredSession(storage, contract, value) {
    if (!storage || typeof storage.setItem !== "function") return false;
    try {
      storage.setItem(storageKey(contract), JSON.stringify({ schema: STORAGE_SCHEMA, role: value.role, roomCode: value.roomCode, sequence: value.sequence, expiresAt: value.expiresAt }));
      return true;
    } catch (_error) { return false; }
  }
  function clearStoredSession(storage, contract) {
    if (!storage || typeof storage.removeItem !== "function") return;
    try { storage.removeItem(storageKey(contract)); } catch (_error) {}
  }
  function runtimeConfig(root) {
    var node = root && root.querySelector ? root.querySelector("[data-nlfs-config]") : null;
    if (!node) return null;
    var data;
    try { data = JSON.parse(node.textContent || ""); } catch (_error) { return null; }
    return data && data.integrations ? normalizeRuntimeContract(data.integrations.co_tour, currentOrigin()) : null;
  }

  function mount(root) {
    if (!root || instances.has(root)) return instances.get(root) || null;
    var panel = root.querySelector("[data-nlfs-cotour]");
    var capabilitySlot = root.querySelector('[data-nlfs-capability-slot="co_tour"]');
    if (!panel) return null;
    var contract = runtimeConfig(root);
    var status = panel.querySelector("[data-nlfs-cotour-status]");
    var idle = panel.querySelector("[data-nlfs-cotour-idle]");
    var active = panel.querySelector("[data-nlfs-cotour-active]");
    var start = panel.querySelector("[data-nlfs-cotour-start]");
    var join = panel.querySelector("[data-nlfs-cotour-join]");
    var consent = panel.querySelector("[data-nlfs-cotour-consent]");
    var roomInput = panel.querySelector("[data-nlfs-cotour-room-input]");
    var roomOutput = panel.querySelector("[data-nlfs-cotour-room-output]");
    var roleOutput = panel.querySelector("[data-nlfs-cotour-role]");
    var presenceOutput = panel.querySelector("[data-nlfs-cotour-presence]");
    var follow = panel.querySelector("[data-nlfs-cotour-follow]");
    var reconnect = panel.querySelector("[data-nlfs-cotour-reconnect]");
    var end = panel.querySelector("[data-nlfs-cotour-end]");
    if (!contract || !status || !idle || !active || !start || !join || !consent || !roomInput || !roomOutput || !roleOutput || !presenceOutput || !follow || !reconnect || !end) {
      panel.dataset.state = "unavailable";
      if (capabilitySlot) capabilitySlot.dataset.runtimeState = "unavailable";
      if (status) status.textContent = "הסיור המרחבי המסונכרן אינו זמין כי חוזה החיבור לא אומת.";
      [start, join, follow, reconnect, end].forEach(function (button) { if (button) { button.disabled = true; button.setAttribute("aria-disabled", "true"); } });
      return null;
    }
    var lifecycle = new AbortController();
    var timers = createTimerBag(globalScope);
    var protocol = createProtocolClient(contract, function (url, options) {
      return globalScope.fetch(url, Object.assign({}, options, { signal: lifecycle.signal }));
    }, currentOrigin());
    var role = "idle";
    var roomCode = "";
    var sequence = 0;
    var expiresAt = 0;
    var presenceCount = 0;
    var destroyed = false;
    var requestBusy = false;
    var hostDirty = false;
    var updateTimer = 0;
    var pollTimer = 0;
    var pollBackoffIndex = 0;
    var degraded = false;

    function report(message, state) { status.textContent = message; status.dataset.state = state || "idle"; }
    function setButton(button, enabled) { button.disabled = !enabled; button.setAttribute("aria-disabled", enabled ? "false" : "true"); }
    function connectedRole() { return role === "host" || role === "follower"; }
    function paint() {
      var connected = connectedRole() || /-reconnect$/.test(role);
      idle.hidden = connected;
      active.hidden = !connected;
      panel.dataset.state = role;
      roomOutput.textContent = roomCode;
      roleOutput.textContent = role.indexOf("host") === 0 ? "מארח/ת" : role.indexOf("follower") === 0 ? "עוקב/ת בהסכמה" : "לא מחובר";
      presenceOutput.textContent = String(presenceCount) + " מתוך 2";
      follow.hidden = role !== "follower";
      follow.textContent = followGate.isPaused() ? "המשך מעקב" : "השהיית מעקב";
      reconnect.hidden = !(degraded || /-reconnect$/.test(role));
      end.textContent = role === "follower" ? "יציאה מהסיור" : /-reconnect$/.test(role) ? "ויתור על שחזור" : "סיום החדר";
      roomInput.disabled = connected;
      consent.disabled = connected;
      setButton(start, !connected && role === "idle" && !requestBusy);
      setButton(join, !connected && role === "idle" && !requestBusy && consent.checked === true);
      setButton(follow, role === "follower");
      setButton(reconnect, connected && !requestBusy);
      setButton(end, connected && !requestBusy);
    }
    function applyFollowerState(state) {
      var applied = restoreFollowerState(globalScope.NadlanFlagshipV3, root, state, followGate.hasConsent());
      report(applied ? "מצב המארח סונכרן לאחר ההסכמה, כולל הבחירה והכלי הפעיל." : "המצב התקבל אך לא התאים לחוזה המרחבי של העמוד.", applied ? "following" : "state-rejected");
      return applied;
    }
    var followGate = createFollowGate(applyFollowerState);
    function clearNetworkTimers() {
      if (updateTimer) timers.clear(updateTimer);
      if (pollTimer) timers.clear(pollTimer);
      updateTimer = 0;
      pollTimer = 0;
    }
    function rememberSession() {
      if (connectedRole()) writeStoredSession(globalScope.sessionStorage, contract, { role: role, roomCode: roomCode, sequence: sequence, expiresAt: expiresAt });
    }
    function updatePresence(result) {
      if (!result || result.capacity !== 2 || !Number.isSafeInteger(result.presenceCount) || result.presenceCount < 0 || result.presenceCount > 2) throw new ProtocolError("invalid_response", 0);
      presenceCount = result.presenceCount;
    }
    function localLeave(message, state) {
      clearNetworkTimers();
      clearStoredSession(globalScope.sessionStorage, contract);
      followGate.setConsent(false);
      role = "idle";
      roomCode = "";
      sequence = 0;
      expiresAt = 0;
      presenceCount = 0;
      requestBusy = false;
      degraded = false;
      hostDirty = false;
      pollBackoffIndex = 0;
      roomInput.value = "";
      consent.checked = false;
      report(message, state);
      paint();
    }
    function captureState() {
      var api = globalScope.NadlanFlagshipV3;
      if (!api || typeof api.getState !== "function") return null;
      var state = api.getState(root);
      if (!plain(state) || state.schema !== SPATIAL_STATE_SCHEMA || state.projectContractId !== contract.projectContractId) return null;
      try { return JSON.stringify(state).length <= contract.maxStateBytes ? state : null; } catch (_error) { return null; }
    }
    function handleProtocolError(error, context) {
      if (destroyed || (error && error.name === "AbortError")) return;
      requestBusy = false;
      if (error && ["room_expired", "room_unavailable", "resume_auth_failed", "host_auth_failed", "follower_auth_failed"].indexOf(error.code) >= 0) {
        localLeave("החדר הסתיים או שההרשאה הקצרה פגה. אפשר לפתוח חדר חדש או להצטרף מחדש בהסכמה.", "ended");
        return;
      }
      if (role === "idle") {
        var capacity = error && error.code === "capacity_reached";
        report(capacity ? "החדר מלא: מארח אחד ועוקב אחד בלבד." : error && error.code === "rate_limited" ? "קצב הבקשות הוגבל זמנית. המתינו חמש שניות ונסו שוב." : "החדר לא נפתח; לא מוצג מצב שווא. אפשר לנסות שוב.", capacity ? "capacity" : "request-failed");
        paint();
        return;
      }
      if (context === "host" && error && error.code === "sequence_conflict" && Number.isSafeInteger(error.sequence)) {
        sequence = error.sequence;
        rememberSession();
      }
      if (role === "follower" && error && error.code === "rate_limited") {
        pollBackoffIndex = contract.pollBackoffMs.length - 1;
        degraded = false;
        report("המעקב האט זמנית כדי לשמור על קנה מידה תקין.", "backing-off");
        paint();
        schedulePoll();
        return;
      }
      degraded = true;
      report("החיבור נעצר בלי להעמיד פנים שהוא פעיל. לחצו חיבור מחדש.", "reconnect-required");
      paint();
    }
    function sendHostState() {
      updateTimer = 0;
      if (destroyed || role !== "host" || globalScope.document.hidden) { hostDirty = true; return; }
      if (requestBusy) { hostDirty = true; return; }
      var state = captureState();
      if (!state) { report("מצב מרחבי תקין עדיין אינו זמין לסנכרון.", "state-unavailable"); return; }
      requestBusy = true;
      hostDirty = false;
      protocol.update(roomCode, sequence + 1, state).then(function (result) {
        if (destroyed || role !== "host") return;
        requestBusy = false;
        if (result.role !== "host" || result.status !== "updated" || !Number.isSafeInteger(result.sequence)) throw new ProtocolError("invalid_response", 0);
        sequence = result.sequence;
        expiresAt = result.expiresAt;
        updatePresence(result);
        degraded = false;
        rememberSession();
        report("המצב המרחבי מסונכרן. קוד החדר נשאר ידני ואינו כתובת אינטרנט.", "hosting");
        paint();
        if (hostDirty) queueHostState();
      }).catch(function (error) { handleProtocolError(error, "host"); });
    }
    function queueHostState() {
      if (role !== "host") return;
      hostDirty = true;
      if (!updateTimer && !globalScope.document.hidden) updateTimer = timers.set(sendHostState, 850);
    }
    function schedulePoll() {
      if (role !== "follower" || destroyed || globalScope.document.hidden || degraded) return;
      if (pollTimer) timers.clear(pollTimer);
      pollTimer = timers.set(pollFollower, contract.pollBackoffMs[pollBackoffIndex]);
    }
    function acceptPoll(result) {
      if (result.role !== "follower") throw new ProtocolError("invalid_response", 0);
      updatePresence(result);
      if (result.status === "ended") { localLeave("המארח סיים את החדר.", "ended"); return false; }
      if (!Number.isSafeInteger(result.sequence) || result.sequence < sequence || ["changed", "no_change"].indexOf(result.status) < 0) throw new ProtocolError("invalid_response", 0);
      sequence = result.sequence;
      expiresAt = result.expiresAt;
      if (result.status === "changed" && plain(result.state)) {
        pollBackoffIndex = 0;
        followGate.receive(result.state, result.sequence);
      } else {
        pollBackoffIndex = Math.min(contract.pollBackoffMs.length - 1, pollBackoffIndex + 1);
        if (!followGate.isPaused()) report("המעקב פעיל; אין שינוי חדש מהמארח.", "following");
      }
      rememberSession();
      return true;
    }
    function pollFollower() {
      pollTimer = 0;
      if (destroyed || role !== "follower" || globalScope.document.hidden || requestBusy) return;
      requestBusy = true;
      protocol.poll(roomCode, sequence).then(function (result) {
        if (destroyed || role !== "follower") return;
        requestBusy = false;
        degraded = false;
        if (acceptPoll(result)) { paint(); schedulePoll(); }
      }).catch(function (error) { handleProtocolError(error, "follower"); });
    }
    function startHost(event) {
      event.preventDefault();
      if (requestBusy || role !== "idle") return;
      requestBusy = true;
      report("פותחים חדר מרחבי קצר־חיים…", "working");
      paint();
      protocol.create().then(function (result) {
        if (destroyed) return;
        if (result.role !== "host" || result.status !== "active" || !validRoomCode(result.roomCode) || result.sequence !== 0) throw new ProtocolError("invalid_response", 0);
        updatePresence(result);
        requestBusy = false;
        role = "host";
        roomCode = result.roomCode;
        sequence = 0;
        expiresAt = result.expiresAt;
        degraded = false;
        rememberSession();
        report("החדר נפתח. מסרו בעל־פה או בהודעה רק את קוד החדר המוצג.", "hosting");
        paint();
        queueHostState();
      }).catch(function (error) { requestBusy = false; handleProtocolError(error, "create"); });
    }
    function joinFollower(event) {
      event.preventDefault();
      if (requestBusy || role !== "idle") return;
      if (consent.checked !== true) { report("יש לאשר מעקב מרחבי לפני נוכחות בחדר.", "consent-required"); paint(); return; }
      var supplied = normalizeRoomCode(roomInput.value);
      if (!validRoomCode(supplied)) { report("קוד חדר כולל 12 תווי A–F וספרות, ללא קישור.", "invalid-room"); return; }
      requestBusy = true;
      roomCode = supplied;
      sequence = 0;
      report("מתחברים בהסכמה לחדר המרחבי…", "working");
      paint();
      protocol.join(roomCode, 0).then(function (result) {
        if (destroyed) return;
        requestBusy = false;
        if (result.status === "ended") { role = "follower"; localLeave("החדר כבר הסתיים.", "ended"); return; }
        role = "follower";
        followGate.setConsent(true);
        degraded = false;
        if (acceptPoll(result)) { paint(); schedulePoll(); }
      }).catch(function (error) { roomCode = ""; requestBusy = false; handleProtocolError(error, "join"); });
    }
    function reconnectSession(event) {
      event.preventDefault();
      if (requestBusy || (!/-reconnect$/.test(role) && !connectedRole())) return;
      var expectedRole = role.indexOf("host") === 0 ? "host" : "follower";
      requestBusy = true;
      degraded = false;
      report("משחזרים הרשאה קצרה מהעוגייה המוגנת ומסובבים אותה…", "working");
      paint();
      protocol.resume(roomCode, sequence).then(function (result) {
        if (destroyed) return;
        requestBusy = false;
        if (result.role !== expectedRole || result.status === "ended") throw new ProtocolError("invalid_response", 0);
        updatePresence(result);
        role = result.role;
        sequence = result.sequence;
        expiresAt = result.expiresAt;
        degraded = false;
        if (role === "host") {
          rememberSession();
          report("חיבור המארח שוחזר וההרשאה המוגנת הוחלפה.", "hosting");
          paint();
          queueHostState();
        } else {
          followGate.setConsent(true);
          if (acceptPoll(result)) { report("המעקב חובר מחדש.", "following"); paint(); schedulePoll(); }
        }
      }).catch(function (error) { requestBusy = false; handleProtocolError(error, expectedRole); });
    }
    function toggleFollow(event) {
      event.preventDefault();
      if (role !== "follower") return;
      var pausing = !followGate.isPaused();
      followGate.setManualPaused(pausing);
      report(pausing ? "המעקב הושהה ידנית; השינוי האחרון ימתין כאן." : "המעקב חודש; השינוי האחרון הוחל.", pausing ? "paused" : "following");
      paint();
    }
    function endSession(event) {
      event.preventDefault();
      if (requestBusy) return;
      if (/-reconnect$/.test(role)) { localLeave("השחזור בוטל; ההרשאה נשארת בלתי־קריאה ותפוג עם החדר.", "left"); return; }
      if (role === "follower") {
        requestBusy = true;
        report("מפנים את מקום העוקב בחדר…", "working");
        paint();
        protocol.leave(roomCode, sequence).then(function () { if (!destroyed) localLeave("יצאתם מהסיור והמקום לעוקב התפנה.", "left"); })
          .catch(function (error) { requestBusy = false; handleProtocolError(error, "follower"); });
        return;
      }
      if (role !== "host") return;
      requestBusy = true;
      report("מסיימים את החדר ומודיעים לעוקב…", "working");
      paint();
      protocol.end(roomCode, sequence + 1).then(function () { if (!destroyed) localLeave("החדר הסתיים ולא ניתן להצטרף אליו מחדש.", "ended"); })
        .catch(function (error) { requestBusy = false; handleProtocolError(error, "host"); });
    }
    function stateChanged() { if (role === "host") queueHostState(); }
    function consentChanged() {
      if (role === "idle") {
        report(consent.checked ? "ההסכמה ניתנה; אפשר להצטרף עם קוד ידני." : "נדרשת הסכמה מפורשת לפני הצטרפות ונוכחות.", consent.checked ? "consent-ready" : "ready");
        paint();
      }
    }
    function visibilityChanged() {
      var hidden = globalScope.document.hidden === true;
      followGate.setVisibilityPaused(hidden);
      if (hidden) {
        clearNetworkTimers();
        if (role === "host") hostDirty = true;
        report("הסנכרון הושהה כי הלשונית אינה גלויה.", "visibility-paused");
      } else if (role === "host") {
        report("הלשונית חזרה; מכינים מצב מרחבי עדכני.", "reconnecting");
        queueHostState();
      } else if (role === "follower") {
        report("הלשונית חזרה; בודקים שינוי חדש מהמארח.", "reconnecting");
        pollBackoffIndex = 0;
        pollFollower();
      }
      paint();
    }
    function destroy() {
      if (destroyed) return;
      destroyed = true;
      clearNetworkTimers();
      timers.clearAll();
      lifecycle.abort();
      followGate.destroy();
      start.removeEventListener("click", startHost);
      join.removeEventListener("click", joinFollower);
      consent.removeEventListener("change", consentChanged);
      reconnect.removeEventListener("click", reconnectSession);
      follow.removeEventListener("click", toggleFollow);
      end.removeEventListener("click", endSession);
      root.removeEventListener("nadlan:flagship-v3:state-change", stateChanged);
      root.removeEventListener("nadlan:flagship-v3:destroyed", destroy);
      globalScope.document.removeEventListener("visibilitychange", visibilityChanged);
      if (capabilitySlot) capabilitySlot.dataset.runtimeState = "unmounted";
      instances.delete(root);
    }

    start.addEventListener("click", startHost);
    join.addEventListener("click", joinFollower);
    consent.addEventListener("change", consentChanged);
    reconnect.addEventListener("click", reconnectSession);
    follow.addEventListener("click", toggleFollow);
    end.addEventListener("click", endSession);
    root.addEventListener("nadlan:flagship-v3:state-change", stateChanged);
    root.addEventListener("nadlan:flagship-v3:destroyed", destroy);
    globalScope.document.addEventListener("visibilitychange", visibilityChanged);

    var stored = readStoredSession(globalScope.sessionStorage, contract, Math.floor(Date.now() / 1000));
    if (stored) {
      role = stored.role + "-reconnect";
      roomCode = stored.roomCode;
      sequence = stored.sequence;
      expiresAt = stored.expiresAt;
      presenceCount = stored.role === "host" ? 1 : 2;
      degraded = true;
      report("נמצא חדר קצר־חיים בלשונית הזו. לחצו חיבור מחדש; ההרשאה נמצאת רק בעוגייה מוגנת.", "reconnect-required");
    } else {
      clearStoredSession(globalScope.sessionStorage, contract);
      report("אפשר לפתוח חדר או להצטרף בהסכמה עם קוד ידני. אין וידאו, צ׳אט או הקלטה.", "ready");
    }
    paint();
    if (capabilitySlot) capabilitySlot.dataset.runtimeState = "materialized";
    var instance = Object.freeze({ destroy: destroy, getRole: function () { return role; }, getRoomCode: function () { return roomCode; }, getPresenceCount: function () { return presenceCount; } });
    instances.set(root, instance);
    return instance;
  }

  function mountAll(scope) {
    var target = scope && scope.querySelectorAll ? scope : globalScope.document;
    if (!target) return;
    target.querySelectorAll('[data-nl-flagship="v3"]').forEach(mount);
  }
  function destroyAll() {
    if (!globalScope.document) return;
    globalScope.document.querySelectorAll('[data-nl-flagship="v3"]').forEach(function (root) { var instance = instances.get(root); if (instance) instance.destroy(); });
  }
  function install(documentNode) {
    if (!documentNode || typeof documentNode.addEventListener !== "function") return;
    documentNode.addEventListener("DOMContentLoaded", function () { mountAll(documentNode); }, { once: true });
    documentNode.addEventListener("nadlan:flagship-v3:mounted", function (event) { mount(event.target); });
    if (documentNode.readyState !== "loading") mountAll(documentNode);
  }

  return Object.freeze({
    REQUEST_SCHEMA: REQUEST_SCHEMA,
    RESPONSE_SCHEMA: RESPONSE_SCHEMA,
    RUNTIME_SCHEMA: RUNTIME_SCHEMA,
    SPATIAL_STATE_SCHEMA: SPATIAL_STATE_SCHEMA,
    normalizeRuntimeContract: normalizeRuntimeContract,
    normalizeRoomCode: normalizeRoomCode,
    validRoomCode: validRoomCode,
    safeEndpoint: safeEndpoint,
    createProtocolClient: createProtocolClient,
    restoreFollowerState: restoreFollowerState,
    createFollowGate: createFollowGate,
    createTimerBag: createTimerBag,
    readStoredSession: readStoredSession,
    mount: mount,
    mountAll: mountAll,
    destroyAll: destroyAll,
    install: install,
    ProtocolError: ProtocolError
  });
});
