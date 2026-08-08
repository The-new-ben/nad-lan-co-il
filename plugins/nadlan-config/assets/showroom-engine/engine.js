/* ============================================================================
   NadLan Showroom - ENGINE (vanilla, data-driven)
   Renders entirely from window.NADLAN_SHOWROOM (engine/data.js) + window.NADLAN_I18N
   (engine/i18n.js). No chrome text or project value is hardcoded here. The page
   shell (#nl-root[data-page]) is the only HTML; everything below is built from data.
   ============================================================================ */
(function () {
  "use strict";
  var SR = window.NADLAN_SHOWROOM, I18N = window.NADLAN_I18N;
  var ROOT = document.getElementById("nl-root");
  if (!SR || !I18N || !ROOT) { console.warn("NadLan: missing data/i18n/root"); return; }

  /* ---------------- state ---------------- */
  var qs = new URLSearchParams(location.search);
  var state = {
    page: ROOT.dataset.page || "project",
    lang: qs.get("lang") || SR.config.default_lang,
    projectKey: (qs.get("project") && SR.projects[qs.get("project")]) ? qs.get("project") : SR.config.default_project,
    unitId: qs.get("unit") || null,
    view: "3d", tab: "plan", filter: "all", light: "day", sunMin: 720,
    favs: normalizeIdList(load("nl_favs", [])), compare: [],
    mvReady: false,
    tool: null
  };
  // Sketch-first: if a project has no 3D model, start in facade (sketch) view so
  // the page never shows an empty/broken model-viewer. (Antigravity, 2026-07-01)
  if (state.projectKey && SR.projects[state.projectKey] && !SR.projects[state.projectKey].model_glb) {
    state.view = "facade";
  }
  if (I18N.langs[state.lang] == null) state.lang = SR.config.default_lang;

  /* ---------------- i18n + helpers ---------------- */
  function t(key, vars) {
    var chain = [state.lang].concat(I18N.fallback), s = null;
    for (var i = 0; i < chain.length; i++) { var tb = I18N.langs[chain[i]]; if (tb && tb[key] != null) { s = tb[key]; break; } }
    if (s == null) s = key;
    if (vars) s = s.replace(/\{(\w+)\}/g, function (_, k) { return vars[k] != null ? vars[k] : ""; });
    return s;
  }
  function isRTL() { return SR.config.rtl_languages.indexOf(state.lang) >= 0; }
  function project() { return SR.projects[state.projectKey]; }
  function units() { return project().units; }
  function unit(id) { var u = units().filter(function (x) { return x.id === id; }); return u[0] || null; }
  function projName() { return t(project().name_key); }
  function content(k) { var c = project().content || {}; return (c[state.lang] && c[state.lang][k]) || (c.en && c.en[k]) || (c.he && c.he[k]) || ""; }
  var KNOWN_DIRS = { west:1, east:1, north:1, south:1, "south-west":1, "north-west":1, "south-east":1, "north-east":1 };
  // Never echo a raw "dir_xxx" key: translate known enums, else show the raw value.
  /* CMS units may carry Hebrew compass names; normalize so every language
     renders its own label (no Hebrew leaking onto EN/FR/RU pages). */
  var HE_DIRS = { "מערב": "west", "מזרח": "east", "צפון": "north", "דרום": "south", "דרום מערב": "south-west", "דרום-מערב": "south-west", "צפון מערב": "north-west", "צפון-מערב": "north-west", "דרום מזרח": "south-east", "דרום-מזרח": "south-east", "צפון מזרח": "north-east", "צפון-מזרח": "north-east", "מערב וצפון": "north-west" };
  function dirKey(d) { d = String(d == null ? "" : d).trim(); return KNOWN_DIRS[d] ? d : (HE_DIRS[d] || ""); }
  function dirLabel(d) { var k = dirKey(d); return k ? t("dir_" + k) : (d || ""); }
  function statusLabel(s) { return t("status_" + s); }
  function roomsLabel(n) { return t("rooms_label", { n: n }); }
  function viewText(u) {
    if (unitV2Enabled()) return unitV2View(u);
    return u.view_key ? t(u.view_key) : (u.view || "");
  }
  function area() { return (SR.areas && SR.areas[project().area]) || { map: { pins: [], project_pin: { x: 50, y: 50 }, coast_x: 16 }, spoke_groups: [], stats: [] }; }
  function spoke(id) { return (SR.spokes && SR.spokes[id]) || null; }

  function engineStorage() {
    /* The password lab must not write private names/URLs or cloned unit IDs
       into the production origin's persistent buyer history. */
    return unitV2Sandbox() ? window.sessionStorage : window.localStorage;
  }
  function load(k, d) { try { return JSON.parse(engineStorage().getItem(k)) || d; } catch (e) { return d; } }
  function normalizeIdList(value) {
    if (!Array.isArray(value)) return [];
    return value.map(function (id) { return String(id); })
      .filter(function (id, index, all) { return id && all.indexOf(id) === index; })
      .slice(0, 100);
  }
  function save(k, v) { try { engineStorage().setItem(k, JSON.stringify(v)); } catch (e) {} }
  function unitV2CompareStorageKey() {
    return "nl_unit_compare_v2:" + encodeURIComponent(String(state.projectKey || "project"));
  }
  function validUnitV2CompareIds(value) {
    var known = {};
    units().forEach(function (u) { known[String(u.id)] = true; });
    return normalizeIdList(value).filter(function (id) { return known[id]; }).slice(0, 3);
  }
  function loadUnitV2Compare() {
    if (!unitV2Enabled()) return [];
    try {
      return validUnitV2CompareIds(JSON.parse(
        window.sessionStorage.getItem(unitV2CompareStorageKey()) || "[]"
      ));
    } catch (e) {
      return [];
    }
  }
  function saveUnitV2Compare(ids) {
    if (!unitV2Enabled()) return;
    state.compare = validUnitV2CompareIds(ids);
    try {
      window.sessionStorage.setItem(
        unitV2CompareStorageKey(),
        JSON.stringify(state.compare)
      );
    } catch (e) {}
  }
  function prepareUnitV2Compare(current) {
    var ordered = [String(current.id)]
      .concat(validUnitV2CompareIds(state.compare), loadUnitV2Compare());
    var ids = ordered.filter(function (id, index, all) {
      return id && all.indexOf(id) === index && unit(id);
    });

    if (ids.length < 2) {
      units().some(function (candidate) {
        var id = String(candidate.id);
        if (ids.indexOf(id) < 0) ids.push(id);
        return ids.length >= 2;
      });
    }

    saveUnitV2Compare(ids.slice(0, 3));
    return state.compare.slice();
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function unitV2Enabled() {
    return !!(SR.config.selected_unit_surface && SR.config.selected_unit_surface_v2);
  }
  function unitV2Sandbox() {
    return unitV2Enabled() && SR.config.private_unit_journey_lab === true;
  }
  function safeHttpUrl(url) {
    var s = String(url || "").trim();
    if (!s) return ""; // empty input must stay empty: new URL("", origin) is the homepage
    try {
      var u = new URL(s, location.origin);
      return (u.protocol === "http:" || u.protocol === "https:") ? u.href : "";
    } catch (e) {
      return "";
    }
  }
  function money(n) { n = Math.round(Number(n) || 0); return "₪" + n.toLocaleString("en-US"); }

  /* ---------------- icons ---------------- */
  var ICON = {
    cube: '<path d="M12 2 21 7v10l-9 5-9-5V7z"/><path d="m3 7 9 5 9-5M12 12v10"/>',
    grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    wave: '<path d="M2 8c2 0 2 2 4 2s2-2 4-2 2 2 4 2 2-2 4-2 2 2 4 2M2 14c2 0 2 2 4 2s2-2 4-2 2 2 4 2 2-2 4-2 2 2 4 2"/>',
    train: '<rect x="5" y="3" width="14" height="13" rx="3"/><path d="M5 11h14M8 20l-2 2M16 20l2 2"/><circle cx="8.5" cy="13.5" r="1"/><circle cx="15.5" cy="13.5" r="1"/>',
    tree: '<path d="M12 2 6 11h4l-4 6h12l-4-6h4L12 2zM12 17v5"/>',
    school: '<path d="M3 9l9-5 9 5-9 5-9-5zM7 11v5c0 1 2.5 2.5 5 2.5s5-1.5 5-2.5v-5"/>',
    store: '<path d="M3 9l1.5-5h15L21 9M4 9v10h16V9M9 19v-5h6v5"/>',
    road: '<path d="M5 3 3 21M19 3l2 18M12 4v3M12 11v3M12 18v2"/>',
    landmark: '<path d="M12 3 4 8h16zM5 10v8M19 10v8M9.5 10v8M14.5 10v8M3 21h18"/>',
    compass: '<circle cx="12" cy="12" r="9"/><path d="m15 9-3 6-3-6 6 0z"/>',
    heart: '<path d="M12 21s-7-5.2-7-11a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.8-7 11-7 11z"/>',
    scale: '<path d="M12 3v18M5 7l-3 7h6zM19 7l-3 7h6zM7 14a3 3 0 0 1-6 0M23 14a3 3 0 0 1-6 0M3 7h18"/>',
    share: '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/>',
    check: '<path d="M20 6 9 17l-5-5"/>',
    shield: '<path d="M12 2 4 5v6c0 5 3.4 8.5 8 11 4.6-2.5 8-6 8-11V5z"/><path d="m9 12 2 2 4-4"/>',
    phone: '<path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    wa: '<path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.4A10 10 0 1 0 12 2z"/><path d="M8.5 7.5c-.3 0-.7.1-.9.5s-.9 1-.9 2.3.9 2.7 1.1 2.9 1.9 3 4.6 4.1c2.3.9 2.3.6 2.7.6s1.5-.6 1.7-1.2.2-1.1.1-1.2-.3-.2-.7-.4-1.5-.7-1.7-.8-.4-.1-.6.2-.7.8-.8 1-.3.2-.6.1a4.6 4.6 0 0 1-1.4-.9 5.4 5.4 0 0 1-1-1.2c-.1-.3 0-.4.1-.6l.4-.5.3-.5v-.5c0-.1-.6-1.5-.8-2z" fill="#fff" stroke="none"/>',
    pin: '<path d="M12 21s-6-5.7-6-10a6 6 0 0 1 12 0c0 4.3-6 10-6 10z"/><circle cx="12" cy="11" r="2"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>', play: '<path d="M8 5v14l11-7z"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 2.5 15 0 18M12 3c-2.5 2.5-2.5 15 0 18"/>'
  };
  function svg(name, w) { w = w || 18; return '<svg width="' + w + '" height="' + w + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + (ICON[name] || "") + "</svg>"; }

  /* ---------------- 3D placement (concept model derives from floor+dir) ---------------- */
  var DIRV = { west: [-1, 0], east: [1, 0], north: [0, 1], south: [0, -1], "south-west": [-0.71, -0.71], "north-west": [-0.71, 0.71], "south-east": [0.71, -0.71], "north-east": [0.71, 0.71] };
  function unitPos(u) {
    /* Explicit hotspot_position (authored per real model, e.g. offset towers,
       boutique buildings) wins; the floor+dir formula is the fallback for
       single-tower-at-origin models. */
    var hp = String(u.hotspot_position || "").trim().split(/\s+/);
    /* normals are unitless direction vectors (model-viewer parses them for
       facing/occlusion); default to the unit's own compass direction so
       far-side hotspots hide when the building rotates between them and us */
    var dv = DIRV[dirKey(u.dir)] || null;
    if (hp.length === 3 && hp.every(function (n) { return isFinite(parseFloat(n)); })) {
      var hn = String(u.hotspot_normal || "").trim().split(/\s+/);
      if (hn.length !== 3 || !hn.every(function (n) { return isFinite(parseFloat(n)); })) {
        hn = dv ? [String(dv[0]), "0", String(dv[1])] : ["0", "0", "1"];
      }
      return {
        pos: hp.map(function (n) { return parseFloat(n).toFixed(2) + "m"; }).join(" "),
        nrm: hn.map(function (n) { return String(parseFloat(n)); }).join(" ")
      };
    }
    /* With neither an authored position nor a normalized direction there is no
       truthful 3D face on which to place a unit. Inventory selection remains
       available; the model must not quietly invent a west-facing hotspot. */
    if (!dv) return null;
    var fh = parseFloat(project().floor_height_m) || 3.05, half = 13.2;
    var v = dv, y = u.floor * fh + fh * 0.4;
    return { pos: (v[0] * half).toFixed(2) + "m " + y.toFixed(2) + "m " + (v[1] * half).toFixed(2) + "m", nrm: v[0] + " 0 " + v[1] };
  }
  function orbitRadius(orbit, r) { var p = String(orbit).trim().split(/\s+/); if (p.length >= 3) p[2] = r + "m"; return p.join(" "); }

  /* =====================================================================
     RENDER
  ===================================================================== */
  function render() {
    /* teardown resources the selected-unit surface owns before the DOM under
       them disappears (language/project switch rebuilds #nl-root) */
    if (SR.config.selected_unit_surface) {
      if (typeof destroyBeamMap === "function") destroyBeamMap();
      if (state.tool && typeof finishUnitToolClose === "function") {
        if (typeof normalizeUnitToolHistory === "function") normalizeUnitToolHistory();
        finishUnitToolClose(false);
      }
      if (unitV2Enabled()) {
        document.body.classList.remove("nl-unit-v2-active", "nl-unit-journey-active");
      }
    }
    // The adopted unified map (#nlpjx-map) lives INSIDE nl-root next to the
    // theater; rescue it before innerHTML wipes it, re-adopt in afterRender().
    var uni = document.getElementById("nlpjx-map");
    if (uni && ROOT.contains(uni)) { ROOT.insertAdjacentElement("afterend", uni); }
    document.documentElement.lang = state.lang;
    document.documentElement.dir = isRTL() ? "rtl" : "ltr";
    if (unitV2Enabled() && state.page === "project") {
      document.body.classList.add("nl-unit-v2-enabled");
    }
    if (unitV2Sandbox()) {
      var labTitle = t("unit_lab_page_title", { project: projName() });
      document.title = labTitle + " · " + t("brand");
      var labHeading = document.getElementById("nl-unit-v2-page-title");
      if (labHeading) labHeading.textContent = labTitle;
    } else if (!unitV2Enabled()) {
      document.title = (state.page === "home" ? t("home_gallery_title") : (projName() + " · " + t("brand_sub")));
    }
    ROOT.className = "nl-app";
    ROOT.innerHTML = (state.page === "home")
      ? header() + homeMain() + footer()
      : unitV2Sandbox()
        ? header() + projectMainV2()
        : header() + secNav() + projectMain() + footer() + sticky() + compareTray();
    afterRender();
  }

  /* ---- header + language bar ---- */
  function pageLangs() {
    /* The private v2 sandbox is also the language acceptance surface. Its
       switcher must expose every implemented locale even before sibling posts
       exist; switchLang() safely falls back to an in-place query-param swap. */
    if (unitV2Sandbox()) {
      return ["he", "en", "fr", "ru", "ar"].filter(function (l) {
        return !!I18N.langs[l];
      });
    }
    // On a project page show only languages that have a real sibling post (plus the
    // current one); never render a dead button. On the gallery, show all configured.
    var p = project(), langs = SR.config.languages;
    if (state.page === "project" && p && p.lang_urls) {
      var avail = Object.keys(p.lang_urls);
      if (avail.length) { langs = langs.filter(function (l) { return avail.indexOf(l) >= 0 || l === state.lang; }); }
    }
    return langs;
  }
  function langHref(l) {
    var p = project();
    return (state.page === "project" && p && p.lang_urls && p.lang_urls[l]) ? p.lang_urls[l] : "#";
  }
  function homeHref() {
    if (!unitV2Enabled()) return "home.html";
    return safeHttpUrl(SR.config.home_url) || "/";
  }
  function langBar() {
    // ONE switcher law (owner 2026-08-08): the server-rendered topbar
    // (.nlptop-l) owns language switching on WordPress project pages; a second
    // row in this header read as "the page has three language switchers".
    if (!unitV2Sandbox() && document.querySelector(".nlptop-l")) { return ""; }
    var langs = pageLangs();
    return '<div class="nl-langs" role="group" aria-label="language">' + langs.map(function (l) {
      return '<button class="nl-lang" data-act="lang" data-id="' + l + '" aria-pressed="' + (l === state.lang) + '">' + esc(l.toUpperCase()) + "</button>";
    }).join("") + "</div>";
  }
  function header() {
    // On a project page the in-page navigation is the sticky section nav (secNav),
    // so the header is trimmed to brand + language bar to avoid a duplicate nav row.
    var nav = state.page === "home"
      ? '<div class="nl-nav__links"><a href="#projects" class="is-active">' + esc(t("nav_projects")) + '</a><a href="#areas">' + esc(t("nav_areas")) + '</a><a href="#list">' + esc(t("nav_list")) + "</a></div>"
      : "";
    return '<header class="nl-header"><div class="nl-wrap nl-header__row">' +
      '<a class="nl-brand" href="' + esc(homeHref()) + '"><span class="nl-brand__mark">N</span><span><span class="nl-brand__name">' + esc(t("brand")) + '</span> <span class="nl-brand__sub">' + esc(t("brand_sub")) + "</span></span></a>" +
      '<nav class="nl-nav">' + nav + langBar() + "</nav></div></header>";
  }

  /* sticky in-page section nav (the single in-page nav on a project page) */
  function secNav() {
    var items = [
      ["building", "secnav_building"], ["inventory", "secnav_apartments"], ["price", "secnav_price"],
      ["world", "secnav_environment"], ["media", "secnav_media"], ["about", "secnav_info"]
    ];
    return '<nav class="nl-secnav" id="nl-secnav" aria-label="' + esc(t("secnav_aria")) + '">' + items.map(function (it) {
      return '<a href="#' + it[0] + '" data-act="scroll" data-id="' + it[0] + '" data-spy="' + it[0] + '">' + esc(t(it[1])) + "</a>";
    }).join("") + "</nav>";
  }

  /* ---- project page ---- */
  function projectMainV2() {
    /* The private lab measures one product journey, not the accumulated
       editorial/project template. Keeping only the flagship theater and its
       semantic inventory also removes unrelated sticky bars, horizontal
       section scrollers and untranslated legacy modules from acceptance. */
    return '<main class="nl-unit-v2-main" id="nl-unit-v2-main">' +
      '<section class="nl-wrap" id="building">' + theater() + "</section>" +
      '<section class="nl-sec nl-wrap" id="inventory">' + inventory() + "</section>" +
      "</main>";
  }

  function projectMain() {
    return "<main>" +
      '<section class="nl-sec nl-wrap" id="top">' + hero() + "</section>" +
      '<section class="nl-wrap" id="building" style="padding-bottom:clamp(40px,6vw,80px)">' + theater() + "</section>" +
      '<section class="nl-sec nl-wrap" id="inventory">' + inventory() + "</section>" +
      '<section class="nl-sec nl-wrap" id="price">' + price() + "</section>" +
      '<section class="nl-sec nl-wrap" id="world">' + world() + "</section>" +
      '<section class="nl-sec nl-wrap" id="media">' + media() + "</section>" +
      '<section class="nl-sec nl-wrap" id="investor">' + investor() + "</section>" +
      '<section class="nl-sec nl-wrap" id="about">' + seoBody() + faq() + "</section>" +
      '<section class="nl-wrap" id="inquiry" style="padding-bottom:clamp(40px,6vw,80px)">' + inquiry() + "</section>" +
      '<section class="nl-wrap" style="padding-bottom:clamp(40px,6vw,80px)">' + disclaimer() + "</section>" +
      "</main>";
  }

  /* block 2 - hero */
  function hero() {
    var p = project(), avail = units().filter(function (u) { return u.status === "available"; }).length;
    var hi = units().reduce(function (m, u) { return Math.max(m, u.floor); }, 0);
    /* SEO: exactly ONE h1 per page. Project pages already carry the
       server-rendered h1 (.nlpf-name, directory.php) - the engine hero then
       renders as a same-styled h2. Pages without a server h1 keep the h1. */
    var hasServerH1 = false;
    try {
      var h1s = document.querySelectorAll("h1");
      for (var hi2 = 0; hi2 < h1s.length; hi2++) { if (!ROOT.contains(h1s[hi2])) { hasServerH1 = true; break; } }
    } catch (e) {}
    var hTag = hasServerH1 ? "h2" : "h1";
    return '<div class="nl-hero">' +
      "<div>" +
        '<span class="nl-eyebrow">' + esc(t("hero_eyebrow")) + "</span>" +
        '<hr class="nl-rule">' +
        "<" + hTag + ' class="nl-hero__h1">' + esc(projName()) + "</" + hTag + ">" +
        '<p class="nl-lede" style="margin-top:14px">' + esc(content("tagline")) + "</p>" +
        '<div class="nl-hero__cta"><button class="nl-btn nl-btn--accent" data-act="scroll" data-id="inquiry">' + esc(t("hero_cta_primary")) + '</button><button class="nl-btn nl-btn--ghost" data-act="scroll" data-id="inventory">' + esc(t("hero_cta_secondary")) + "</button></div>" +
        '<div class="nl-hero__facts">' +
          '<div><div class="nl-fact__n">' + esc(p.floors) + '</div><div class="nl-fact__l">' + esc(t("fact_floors")) + "</div></div>" +
          '<div><div class="nl-fact__n">' + esc(units().length) + '</div><div class="nl-fact__l">' + esc(t("fact_homes")) + "</div></div>" +
          '<div><div class="nl-fact__n">' + esc(hi) + '</div><div class="nl-fact__l">' + esc(t("fact_from_floor")) + "</div></div>" +
        "</div>" +
      "</div>" +
      '<div class="nl-hero__media"><img src="' + esc(p.hero_image || p.model_poster) + '" alt="' + esc(projName()) + '" loading="eager">' + (SR.config.demo ? '<span class="nl-badge nl-badge--demo nl-hero__badge">' + esc(t("demo_badge")) + "</span>" : "") + "</div>" +
    "</div>";
  }

  /* block 3 + 4 - theater (3D) and facade backup */
  function theater() {
    var p = project();
    var hots = units().map(function (u) {
      var pos = unitPos(u), cls = "nl-hot" + (u.status === "reserved" ? " nl-hot--reserved" : u.status === "sold" ? " nl-hot--sold" : "") + (u.recommended ? " nl-hot--rec" : "");
      if (!pos) return "";
      return '<button slot="hotspot-' + esc(u.id) + '" data-position="' + pos.pos + '" data-normal="' + pos.nrm + '" data-visibility-attribute="visible" class="' + cls + '" data-act="select" data-id="' + esc(u.id) + '" aria-label="' + esc(unitTitleAria(u)) + '">' + esc(u.floor) + "</button>";
    }).join("");
    var orient = p.orientation || {};
    function opin(side, key, pos) { return orient[key] ? '<span class="nl-orient" style="' + pos + '">' + svg(side, 12) + esc(t(orient[key])) + "</span>" : ""; }
    var orientPins =
      opin("wave", "west", "inset-block-start:50%;inset-inline-start:14px;transform:translateY(-50%)") +
      opin("landmark", "south", "inset-block-end:58px;inset-inline-start:50%;transform:translateX(-50%)") +
      opin("compass", "east", "inset-block-start:50%;inset-inline-end:14px;transform:translateY(-50%)");
    var fsq = units().map(function (u) {
      var cls = "nl-fsq" + (u.status === "reserved" ? " nl-fsq--reserved" : u.status === "sold" ? " nl-fsq--sold" : "");
      /* physical left/top, NOT inset-inline-start: tiles anchor to a photo, and the
         photo does not mirror in RTL - logical coords put units on the wrong tower */
      return '<button class="' + cls + '" data-act="select" data-id="' + esc(u.id) + '" style="left:' + u.stage_x + "%;top:" + u.stage_y + "%;width:" + u.stage_w + "%;height:" + u.stage_h + '%" aria-label="' + esc(unitTitleAria(u)) + '"><b>' + esc(unitDisplayLabel(u)) + "</b><span>" + esc(roomsLabel(u.rooms)) + "</span></button>";
    }).join("");
    var facadeInner = "";
    if (p.facade_image) {
      facadeInner = '<div class="nl-facade__frame" style="background-image:url(' + esc(p.facade_image) + ')">' + fsq + "</div>";
    } else if (p.facade_concept_image) {
      facadeInner = '<div class="nl-facade__frame nl-facade__concept" style="background-image:url(' + esc(p.facade_concept_image) + ')"><div class="nl-facade__notice"><span>' + esc(t("concept_badge")) + "</span><strong>" + esc(t("facade_missing_title")) + "</strong><p>" + esc(t("facade_concept_note")) + "</p></div></div>";
    } else {
      facadeInner = '<div class="nl-facade__frame nl-facade__missing" role="status"><strong>' + esc(t("facade_missing_title")) + "</strong><p>" + esc(t("facade_missing_text")) + "</p></div>";
    }

    /* THE DOCK (owner 2026-07-11: "labels are too much on the frame" + most
       were click-dead): the top bar keeps ONLY title + 3d/facade toggle; the
       working controls live in a normal-flow strip UNDER the stage - no
       overlay, no pointer-events traps. Filters live at the inventory head
       (with counts); a small on-stage flag appears while a filter is active. */
    var dock = p.model_glb ? '<div class="nl-theater__dock">' +
        '<div class="nl-sundial" role="group" aria-label="' + esc(t("sun_sim_label")) + '">' +
          '<span class="nl-sundial__sun" aria-hidden="true">&#9728;</span>' +
          '<input type="range" id="nl-sunslider" min="360" max="1140" step="15" value="' + state.sunMin + '" aria-label="' + esc(t("sun_time_aria")) + '">' +
          '<output class="nl-sundial__time" id="nl-suntime">' + fmtTime(state.sunMin) + "</output>" +
        "</div>" +
        (SR.config.studio !== "off" ? '<button class="nl-cotour-btn nl-studio-launch" data-act="studio-any" type="button">' + esc(t("nlst_open")) + "</button>" : "") +
        '<button class="nl-cotour-btn" data-act="cotour" type="button">' + esc(t("cotour_start")) + "</button>" +
        '<p class="nl-sundial__note">' + esc(t("sun_sim_note")) + "</p>" +
      "</div>" : "";
    return '<div class="nl-theater">' +
      '<div class="nl-theater__top"><div class="nl-theater__title"><span class="e">' + esc(t("theater_eyebrow")) + "</span><h2>" + esc(t("theater_title")) + "</h2></div>" +
        (p.model_glb ? '<div class="nl-toggle" role="group" aria-label="view"><button data-act="view" data-id="3d" aria-pressed="true">' + esc(t("view_3d")) + '</button><button data-act="view" data-id="facade" aria-pressed="false">' + esc(t("view_facade")) + "</button></div>" : "") + "</div>" +
      '<div class="nl-stagewrap">' +
        (p.model_glb ? '<model-viewer id="nl-mv" class="nl-stage" src="' + esc(p.model_glb) + '" loading="lazy" reveal="auto" camera-controls interaction-prompt="none" environment-image="neutral" exposure="1.02" shadow-intensity="0.55" shadow-softness="1"' + (p.default_orbit ? ' camera-orbit="' + esc(p.default_orbit) + '"' : '') + (p.default_target ? ' camera-target="' + esc(p.default_target) + '"' : '') + ' min-camera-orbit="auto 48deg auto" max-camera-orbit="auto 86deg auto" min-field-of-view="16deg" max-field-of-view="68deg" touch-action="pan-y">' + hots + "</model-viewer>" : "") +
        '<div class="nl-poster" id="nl-poster" style="background-image:url(' + esc(p.model_poster) + ')"></div>' +
        '<div class="nl-spinner" id="nl-spin"><i></i>' + esc(t("loading_model")) + "</div>" +
        (p.model_glb && p.model_generic ? '<div class="nl-generic-chip">' + esc(t("generic_model")) + "</div>" : "") +
        '<div class="nlp3d-model-error nl-model-error" id="nl-model-error" role="status" aria-live="polite" hidden>' + esc(t("model_error")) + "</div>" +
        orientPins +
        '<div class="nl-legend"><span><span class="nl-dot s-available"></span>' + esc(t("legend_available")) + '</span><span><span class="nl-dot s-reserved"></span>' + esc(t("legend_reserved")) + '</span><span><span class="nl-dot s-sold"></span>' + esc(t("legend_sold")) + "</span></div>" +
        '<div class="nl-facade" id="nl-facade">' + facadeInner + "</div>" +
        '<div class="nl-scrim" id="nl-scrim"></div>' +
        (p.model_glb ? '<button class="nl-resetview" id="nl-resetview" data-act="resetview" type="button" hidden>' + esc(t("reset_view")) + "</button>" : "") +
        (p.model_glb ? '<div class="nl-sunmark" id="nl-sunmark" aria-hidden="true" hidden></div>' : "") +
        (p.model_glb ? '<button class="nl-filterflag" id="nl-filterflag" data-act="filter" data-id="all" type="button" hidden></button>' : "") +
        panel() +
      "</div>" +
      /* selected-unit scene seam (audit 2026-08-08): a SIBLING of .nl-stagewrap,
         so it is never clipped by its overflow or jailed by its transform */
      '<section class="nl-unit-screen" id="nl-unit-screen" hidden></section>' +
      dock +
    "</div>";
  }
  function unitTitleAria(u) {
    if (unitV2Enabled()) {
      return t("unit_v2_identity", {
        rooms: u.rooms,
        floor: u.floor,
        direction: unitV2Direction(u)
      }) + ", " + statusLabel(u.status);
    }
    return roomsLabel(u.rooms) + ", " + t("floor_label", { n: u.floor }) + ", " + dirLabel(u.dir) + ", " + statusLabel(u.status);
  }

  /* block 5 - slide-out panel (filled on select) */
  function panel() {
    return '<aside class="nl-panel" id="nl-panel" aria-live="polite"><div class="nl-panel__scroll" id="nl-panel-body">' + panelEmpty() + "</div></aside>";
  }
  function panelEmpty() {
    return '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;gap:10px;color:var(--theater-sub);padding:30px">' + svg("grid", 26) + "<p>" + esc(t("panel_prompt")) + "</p></div>";
  }
  function panelBody(u) {
    var fav = state.favs.indexOf(u.id) >= 0, cmp = state.compare.indexOf(u.id) >= 0, p = project();
    return '<div class="nl-panel__head"><div><span class="nl-badge" style="background:rgba(255,255,255,.08);color:#fff"><span class="nl-dot s-' + esc(u.status) + '"></span>' + esc(statusLabel(u.status)) + '</span>' +
        '<h3 class="nl-panel__title" style="margin-top:8px">' + esc(roomsLabel(u.rooms)) + '</h3><div class="nl-muted" style="color:var(--theater-sub);font-size:13px;margin-top:3px">' + esc(projName()) + " · " + esc(dirLabel(u.dir)) + " · " + esc(unitDisplayLabel(u)) + "</div></div>" +
        '<div class="nl-panel__floor"><div style="color:#d8c79a;font-size:12px;font-weight:600">' + esc(t("panel_floor")) + '</div><b>' + esc(u.floor) + "</b>" +
        '<button class="nl-panel__close" data-act="close" aria-label="' + esc(t("btn_close")) + '">' + svg("close", 16) + "</button></div></div>" +
      '<div class="nl-grid2">' +
        stat(t("panel_rooms"), u.rooms) + stat(t("panel_sqm"), u.sqm + " " + t("sqm_unit")) +
        stat(t("panel_balcony"), u.balcony ? (u.balcony + " " + t("sqm_unit")) : "-") + stat(t("panel_view"), viewText(u) || dirLabel(u.dir)) +
      "</div>" + sunLine(u) + scarcityLine(u) + mortgageStrip(u) +
      '<div class="nl-tabs" role="tablist">' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="plan" aria-selected="' + (state.tab === "plan") + '">' + esc(t("tab_plan")) + '</button>' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="view" aria-selected="' + (state.tab === "view") + '">' + esc(dirKey(u.dir) ? t("tab_view_dir", { d: dirLabel(u.dir) }) : t("tab_view")) + '</button>' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="tour" aria-selected="' + (state.tab === "tour") + '">' + esc(t("tab_tour")) + "</button></div>" +
      '<div class="nl-tabpane">' + tabPane(u) + "</div>" +
      '<div class="nl-panel__actions">' +
        '<button class="nl-iconbtn' + (fav ? " is-on" : "") + '" data-act="fav" data-id="' + esc(u.id) + '">' + svg("heart", 16) + esc(fav ? t("btn_saved") : t("btn_save")) + "</button>" +
        '<button class="nl-iconbtn' + (cmp ? " is-on" : "") + '" data-act="compare" data-id="' + esc(u.id) + '">' + svg("scale", 16) + esc(cmp ? t("btn_compared") : t("btn_compare")) + "</button>" +
        '<button class="nl-iconbtn" data-act="share" data-id="' + esc(u.id) + '">' + svg("share", 16) + esc(t("btn_share")) + "</button>" +
        '<a class="nl-iconbtn nl-iconbtn--wa" href="' + esc(waShareUrl(u)) + '" target="_blank" rel="noopener">' + svg("wa", 16) + esc(t("btn_wa_share")) + "</a>" +
      "</div>" +
      '<button class="nl-btn nl-btn--gold nl-btn--block" style="margin-top:14px" data-act="rfp" data-id="' + esc(u.id) + '">' + esc(t("btn_rfp")) + "</button>" +
      (SR.config.brochure_endpoint && p.wp_id ? '<a class="nl-btn nl-btn--block" style="margin-top:9px;text-align:center" href="' + esc(SR.config.brochure_endpoint) + '?p=' + p.wp_id + '&u=' + encodeURIComponent(u.id) + '&lang=' + (state.lang === 'he' ? 'he' : 'en') + '" target="_blank" rel="noopener">' + esc(t("btn_brochure")) + "</a>" : "") +
      (SR.config.studio !== "off" ? '<button class="nl-btn nl-btn--block nl-btn--studio" style="margin-top:9px" data-act="studio" data-id="' + esc(u.id) + '">' + esc(t("nlst_open")) + "</button>" : "") +
      '<button class="nl-btn nl-btn--accent nl-btn--block" style="margin-top:9px" data-act="scroll" data-id="inquiry">' + esc(t("btn_inquire")) + " · " + esc(t("unit_short", { label: unitDisplayLabel(u), floor: u.floor })) + "</button>";
  }
  function stat(k, v) { return '<div class="nl-stat"><div class="k">' + esc(k) + '</div><div class="v">' + esc(v) + "</div></div>"; }
  function sunLine(u) {
    var h = sunHours(u);
    if (h === null || h <= 0) return "";
    return '<div class="nl-sun">&#9728; ' + esc(t("sun_hours", { h: h })) + '<span class="nl-sun__note">' + esc(t("sun_note")) + "</span></div>";
  }
  /* honest scarcity (booking-law): computed from the real inventory array,
     stated plainly, no timers. The cohort link fires the facade filter so
     hesitation about THIS unit becomes a look at its real alternatives. */
  function scarcityLine(u) {
    if (u.status !== "available") return "";
    var same = units().filter(function (x) { return String(x.rooms) === String(u.rooms) && x.status === "available"; }).length;
    if (same === 1) return '<div class="nl-scarce">' + esc(t("scarcity_last", { rooms: u.rooms })) + "</div>";
    if (same > 1 && same <= 3) return '<div class="nl-scarce">' + esc(t("scarcity_left", { n: same, rooms: u.rooms })) +
      ' <button class="nl-scarce__link" data-act="filter" data-id="' + esc(String(u.rooms)) + '" type="button">' + esc(t("scarcity_show")) + "</button></div>";
    return "";
  }
  /* per-apartment WhatsApp share: the deep link opens THIS unit selected. */
  function waShareUrl(u) {
    var url = location.origin + location.pathname + "?project=" + encodeURIComponent(state.projectKey) + "&unit=" + encodeURIComponent(u.id) + "&lang=" + encodeURIComponent(state.lang);
    var msg = projName() + " · " + t("unit_short", { label: unitDisplayLabel(u), floor: u.floor }) + " · " + roomsLabel(u.rooms) + "\n" + url;
    return "https://wa.me/?text=" + encodeURIComponent(msg);
  }
  /* est. monthly payment (the number every buyer computes anyway): 70%
     financing, 25 years, 5.0% - stated in the note, estimate only. */
  function mortgageStrip(u) {
    var p0 = Number(u.price) || Number(u.price_estimate) || 0;
    if (p0 <= 0) return "";
    var loan = p0 * 0.70, r = 0.05 / 12, n = 300;
    var m = loan * r / (1 - Math.pow(1 + r, -n));
    return '<div class="nl-mortg"><b>' + esc(t("mortgage_est", { v: money(Math.round(m / 50) * 50) })) + "</b>" +
      '<span class="nl-mortg__note">' + esc(t("mortgage_note")) + "</span></div>";
  }
  function tabPane(u) {
    if (state.tab === "plan") return u.plan ? '<img src="' + esc(u.plan) + '" alt="' + esc(t("tab_plan")) + '">' : "<p>" + esc(t("plan_coming")) + "</p>";
    if (state.tab === "view") {
      /* THE VIEW TAB IS THE WINDOW (owner intent 2026-07-06): an inline
         real-world viewport standing at this unit's floor height, looking in
         its real direction - satellite + 3D buildings, so the buyer sees WHAT
         is outside (a building? a school? the sea?) without visiting. The
         interior render is secondary; the live POI map is the continuation. */
      // city-centroid coordinates are fine for the area map but a specific
      // window view from a city center would be a lie - require better geo.
      var g = project().geo || {};
      var geoOk = Number(g.lat) && g.confidence !== "city";
      var int1 = u.interior_url || project().default_interior;
      if (geoOk && SR.config.mapbox_token) {
        var html = '<div class="nl-winstage" data-id="' + esc(u.id) + '">' +
          '<div class="nl-winstage__map"></div>' +
          '<div class="nl-winstage__bar">' +
            '<button class="nl-winstage__turn" data-act="winlook" data-id="' + esc(u.id) + '" data-d="-30" aria-label="' + esc(t("winview_turn_left")) + '">&#8634;</button>' +
            '<span class="nl-winstage__meta"><b>' + esc(t("winview_title")) + "</b> \u00B7 " + esc(t("floor_label", { n: u.floor })) + " \u00B7 " + esc(dirLabel(u.dir)) + "</span>" +
            '<button class="nl-winstage__turn" data-act="winlook" data-id="' + esc(u.id) + '" data-d="30" aria-label="' + esc(t("winview_turn_right")) + '">&#8635;</button>' +
            '<button class="nl-winstage__turn nl-winstage__fs" data-act="winfs" aria-label="' + esc(t("winview_fs")) + '" title="' + esc(t("winview_fs")) + '">&#x26F6;</button>' +
          "</div>" +
          '<p class="nl-winstage__note">' + esc(t("winview_note")) + "</p></div>" +
          '<button class="nl-btn nl-btn--gold nl-btn--block" style="margin-top:10px" data-act="winview" data-id="' + esc(u.id) + '">' + esc(t("btn_winview")) + "</button>";
        if (int1) {
          html += '<details class="nl-winstage__int"><summary>' + esc(t("view_interior_label")) + "</summary>" +
            '<img src="' + esc(int1) + '" alt="" loading="lazy">' +
            (u.interior_url ? "" : '<span class="nl-defint__note">' + esc(t("interior_generic_note")) + "</span>") + "</details>";
        }
        return html;
      }
      // no verified location (or no map token) yet: honest interior fallback
      if (u.interior_url) return '<img src="' + esc(u.interior_url) + '" alt="">';
      if (int1) return '<div class="nl-defint"><img src="' + esc(int1) + '" alt=""><span class="nl-defint__note">' + esc(t("interior_generic_note")) + "</span></div>";
      return "<p>" + esc(t("view_coming")) + "</p>";
    }
    var tour = safeHttpUrl(u.tour_url || project().tour_url);
    if (tour) return '<a class="nl-btn nl-btn--gold" href="' + esc(tour) + '" target="_blank" rel="noopener">' + esc(t("tour_open")) + "</a>";
    // no developer tour yet -> the schematic walk-inside, built from THIS
    // unit's real data (rooms, sqm, direction), honestly labeled.
    return fpMarkup(u);
  }

  /* Recently viewed is persistent across public projects. In the private lab,
     the same UI is isolated to sessionStorage and disappears with the session. */
  function recentStrip() {
    var rec = load("nl_recent", []).filter(function (r) { return r && r.u && !(r.p === state.projectKey && r.u === state.unitId); }).slice(0, 5);
    if (!rec.length) return "";
    var items = rec.map(function (r) {
      var storedLabel = unitV2Enabled()
        ? t("unit_v2_marker", { floor: r.f })
        : r.l;
      var label = esc(r.n || "") + " · " + esc(t("unit_short", { label: storedLabel, floor: r.f }));
      return r.p === state.projectKey
        ? '<button class="nl-recent__it" data-act="select" data-id="' + esc(r.u) + '" type="button">' + label + "</button>"
        : '<a class="nl-recent__it" href="' + esc(r.url || "#") + '">' + label + "</a>";
    }).join("");
    return '<div class="nl-recent"><span class="nl-recent__t">' + esc(t("recent_title")) + "</span>" + items + "</div>";
  }
  function recordRecent(u) {
    try {
      var rec = load("nl_recent", []).filter(function (r) { return r && !(r.p === state.projectKey && r.u === u.id); });
      rec.unshift({ p: state.projectKey, u: u.id, l: unitDisplayLabel(u), f: u.floor, r: u.rooms, n: String(projName()).split(" - ")[0],
        url: location.pathname + "?project=" + encodeURIComponent(state.projectKey) + "&unit=" + encodeURIComponent(u.id) + "&lang=" + encodeURIComponent(state.lang) });
      save("nl_recent", rec.slice(0, 6));
      var w = document.getElementById("nl-recentwrap"); if (w) w.innerHTML = recentStrip();
    } catch (e) {}
  }

  /* block 6 - inventory */
  function inventory() {
    var list = filtered();
    var cards = list.map(function (u) {
      var fav = state.favs.indexOf(u.id) >= 0;
      if (unitV2Enabled()) {
        return '<article class="nl-ucard' + (u.id === state.unitId ? " is-active" : "") +
          (u.status === "sold" ? " is-sold" : "") + '" data-id="' + esc(u.id) + '">' +
          '<button class="nl-ucard__select" type="button" data-act="select" data-id="' +
            esc(u.id) + '" aria-label="' + esc(unitTitleAria(u)) + '">' +
            '<div class="nl-ucard__top"><span style="display:inline-flex;align-items:center;gap:6px">' +
              '<span class="nl-dot s-' + esc(u.status) + '"></span>' +
              esc(statusLabel(u.status)) + '</span><span>' +
              esc(t("floor_label", { n: u.floor })) + '</span></div>' +
            '<div class="nl-ucard__rooms">' + esc(roomsLabel(u.rooms)) + '</div>' +
            '<div class="nl-muted" style="font-size:13px">' +
              esc(u.sqm + " " + t("sqm_unit")) + " · " +
              esc(unitV2Direction(u)) + '</div>' +
          '</button>' +
          '<button class="nl-ucard__fav' + (fav ? " is-on" : "") +
            '" type="button" data-act="fav" data-id="' + esc(u.id) +
            '" aria-label="' + esc(t("btn_save")) + '">' + svg("heart", 18) + '</button>' +
        '</article>';
      }
      return '<div class="nl-ucard' + (u.id === state.unitId ? " is-active" : "") + (u.status === "sold" ? " is-sold" : "") + '" data-act="select" data-id="' + esc(u.id) + '" tabindex="0" role="button" aria-label="' + esc(unitTitleAria(u)) + '">' +
        '<button class="nl-ucard__fav' + (fav ? " is-on" : "") + '" data-act="fav" data-id="' + esc(u.id) + '" aria-label="' + esc(t("btn_save")) + '">' + svg("heart", 18) + "</button>" +
        '<div class="nl-ucard__top"><span style="display:inline-flex;align-items:center;gap:6px"><span class="nl-dot s-' + esc(u.status) + '"></span>' + esc(statusLabel(u.status)) + "</span><span>" + esc(t("floor_label", { n: u.floor })) + "</span></div>" +
        '<div class="nl-ucard__rooms">' + esc(roomsLabel(u.rooms)) + "</div>" +
        '<div class="nl-muted" style="font-size:13px">' + esc(u.sqm + " " + t("sqm_unit")) + " · " + esc(dirLabel(u.dir)) + "</div></div>";
    }).join("");
    var keys = ["all", "available", "3", "4", "5"];
    if (filterCount("favs") > 0) keys.push("favs");
    var chips = keys.map(function (f) {
      return '<button class="nl-chip" data-act="filter" data-id="' + f + '" aria-pressed="' + (state.filter === f) + '">' + esc(t("filter_" + f)) + '<span class="nl-chip__n">' + filterCount(f) + "</span></button>";
    }).join("");
    return '<div class="nl-invhead"><div><span class="nl-eyebrow">' + esc(t("inventory_title")) + '</span><hr class="nl-rule"><p class="nl-muted" style="max-width:46ch">' + esc(t("inventory_sub")) + '</p></div><div class="nl-filters">' + chips + "</div></div>" +
      '<div id="nl-recentwrap">' + recentStrip() + "</div>" +
      '<div class="nl-invgrid">' + cards + "</div>" +
      '<div class="nl-muted" style="margin-top:14px;font-size:13px">' + esc(t("results_count", { n: list.length })) + "</div>";
  }



  /* LIVE CO-TOURING (2026-07-07): host broadcasts camera + selection + light +
     filter every 1.6s; viewers follow. ?cotour=host|join&room=<code>. */
  var cotour = { role: qs.get("cotour") || "", room: (qs.get("room") || "").replace(/[^a-z0-9]/gi, ""), timer: 0 };
  function cotourState() {
    var mv = document.getElementById("nl-mv"), o = "";
    try { if (mv && mv.getCameraOrbit) { var c = mv.getCameraOrbit(); o = c.theta.toFixed(3) + "rad " + c.phi.toFixed(3) + "rad " + c.radius.toFixed(2) + "m"; } } catch (e) {}
    return { p: state.projectKey, u: state.unitId || "", o: o, l: state.light, s: state.sunMin, f: state.filter, v: state.view };
  }
  function cotourBar(txt, cls) {
    var b = document.getElementById("nl-cotour-bar");
    if (!b) { b = document.createElement("div"); b.id = "nl-cotour-bar"; document.body.appendChild(b); }
    b.className = cls || ""; b.textContent = txt;
  }
  function cotourStart() {
    if (!SR.config.cotour_endpoint) return;
    cotour.role = "host";
    cotour.room = cotour.room || Math.random().toString(36).slice(2, 8);
    var join = new URL(location.href);
    join.searchParams.set("cotour", "join"); join.searchParams.set("room", cotour.room);
    try { navigator.clipboard.writeText(join.toString()); } catch (e) {}
    cotourBar(t("cotour_live") + " · " + cotour.room + " · " + t("cotour_copied"), "is-host");
    cotourRun();
  }
  function cotourRun() {
    if (cotour.timer) return;
    if (cotour.role === "host") {
      cotour.timer = setInterval(function () {
        try {
          fetch(SR.config.cotour_endpoint, { method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ room: cotour.room, state: cotourState() }) }).catch(function () {});
        } catch (e) {}
      }, 1600);
    } else if (cotour.role === "join") {
      cotourBar(t("cotour_following"), "is-viewer");
      var lastU = null, lastO = "";
      cotour.timer = setInterval(function () {
        try {
          fetch(SR.config.cotour_endpoint + "?room=" + encodeURIComponent(cotour.room)).then(function (r) { return r.json(); }).then(function (d) {
            if (!d || !d.ok || !d.state) return;
            var st = d.state, mv = document.getElementById("nl-mv");
            if (st.u && st.u !== lastU) {
              lastU = st.u;
              if (unitV2Enabled()) selectUnit(st.u, true, document.getElementById("nl-mv"));
              else selectUnit(st.u, true);
            }
            if (st.o && st.o !== lastO && mv) { lastO = st.o; mv.cameraOrbit = st.o; }
            if (st.s != null && parseInt(st.s, 10) !== state.sunMin) { state.sunMin = parseInt(st.s, 10) || 720; applyLight(); }
            else if (st.s == null && st.l && st.l !== state.light) { state.sunMin = ({ day: 720, dusk: 1110, night: 1200 })[st.l] || 720; applyLight(); }
            if (st.f && st.f !== state.filter) { state.filter = st.f; refresh("inventory"); applyStageFilter(); }
          }).catch(function () {});
        } catch (e) {}
      }, 1600);
    }
  }
  /* SUN ENGINE (2026-07-11, owner: "I expected the sun angle simulated").
     Real equinox solar geometry for the project's latitude drives everything:
     exposure + color grade from sun ELEVATION, a stage sun marker at the real
     AZIMUTH (tracks camera), and a gold ring on facades in direct sun.
     model-viewer is IBL-only (no rotatable light), so this simulates exactly
     what is true and the label says so. Geometric only, no obstructions. */
  function sunPos(min) {
    var lat = (project().geo && Number(project().geo.lat)) || 32.08, phi = lat * Math.PI / 180;
    var H = (min / 60 - 12) * 15 * Math.PI / 180;
    return {
      el: Math.asin(Math.cos(phi) * Math.cos(H)),
      az: Math.PI + Math.atan2(Math.sin(H), Math.cos(H) * Math.sin(phi))
    };
  }
  function fmtTime(min) { var h = Math.floor(min / 60), m2 = min % 60; return (h < 10 ? "0" : "") + h + ":" + (m2 < 10 ? "0" : "") + m2; }
  function updateSunMark() {
    var mark = document.getElementById("nl-sunmark"), mv = document.getElementById("nl-mv");
    if (!mark) return;
    var s = sunPos(state.sunMin);
    if (s.el <= 0) { mark.hidden = true; return; }
    mark.hidden = false;
    var theta = 0;
    try { if (mv && mv.getCameraOrbit) theta = mv.getCameraOrbit().theta * 180 / Math.PI; } catch (e) {}
    // screen angle: sun azimuth in the model's frame, rotated with the camera
    // (same convention as map sync: bearing = -theta; calibrated live)
    var sc = (s.az * 180 / Math.PI + theta) * Math.PI / 180;
    var x = 50 + 44 * Math.sin(sc);
    var y = 50 - 36 * Math.cos(sc) - 26 * Math.sin(s.el);
    mark.style.left = Math.max(3, Math.min(97, x)) + "%";
    mark.style.top = Math.max(5, Math.min(88, y)) + "%";
  }
  function applyLight() {
    var mv = document.getElementById("nl-mv");
    var s = sunPos(state.sunMin), elDeg = s.el * 180 / Math.PI;
    var phi = (((project().geo && Number(project().geo.lat)) || 32.08)) * Math.PI / 180;
    var maxUp = Math.cos(phi) || 1;
    var k = Math.min(1, Math.max(0, Math.sin(s.el)) / maxUp);
    var night = elDeg <= 0, golden = !night && elDeg < 12;
    state.light = night ? "night" : (golden ? "dusk" : "day"); // legacy field (cotour, css hooks)
    var flt = "";
    if (night) flt = "brightness(.5) saturate(.6) contrast(1.08)";
    else if (golden) {
      var g = 1 - elDeg / 12;
      flt = "sepia(" + (0.35 * g).toFixed(2) + ") saturate(.85) brightness(" + (1 - 0.2 * g).toFixed(2) + ") contrast(1.04)";
    }
    if (mv) {
      mv.setAttribute("exposure", (0.22 + 0.8 * k).toFixed(2));
      mv.setAttribute("shadow-intensity", (0.12 + 0.43 * k).toFixed(2));
      mv.style.filter = flt;
    }
    var stage = mv && mv.closest(".nl-stagewrap") || mv && mv.parentElement;
    if (stage) {
      stage.classList.toggle("nl-light--dusk", golden);
      stage.classList.toggle("nl-light--night", night);
    }
    // direct-sun facades: sun above 5deg and facade within 70deg of azimuth
    var lit = {};
    if (elDeg > 5) {
      units().forEach(function (u) {
        var dk = dirKey(u.dir); if (!dk || !(dk in DIR_BEARING)) return;
        if (Math.cos(s.az - DIR_BEARING[dk] * Math.PI / 180) > Math.cos(70 * Math.PI / 180)) lit[u.id] = true;
      });
    }
    [].forEach.call(document.querySelectorAll(".nl-hot[data-id], .nl-fsq[data-id]"), function (el2) {
      var on = !!lit[el2.getAttribute("data-id")];
      el2.classList.toggle("nl-sunlit", on);
      if (on) { el2.setAttribute("title", t("sun_direct_now")); } else { el2.removeAttribute("title"); }
    });
    var out = document.getElementById("nl-suntime"); if (out) out.textContent = fmtTime(state.sunMin);
    var sl = document.getElementById("nl-sunslider"); if (sl && parseInt(sl.value, 10) !== state.sunMin) sl.value = state.sunMin;
    updateSunMark();
  }
  /* FILTER THE BUILDING (2026-07-07): the inventory filter is fused into the
     3D stage and the facade - matching apartments stay lit, the rest dim.
     Works on the live DOM (hotspots persist across inventory refreshes). */
  function applyStageFilter() {
    var match = {};
    filtered().forEach(function (u) { match[u.id] = true; });
    var active = state.filter !== "all";
    [].forEach.call(document.querySelectorAll(".nl-hot[data-id], .nl-fsq[data-id]"), function (el) {
      el.classList.toggle("nl-unit-dim", active && !match[el.getAttribute("data-id")]);
    });
    [].forEach.call(document.querySelectorAll('[data-act="filter"]'), function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-id") === state.filter));
    });
    // on-stage flag while a filter is active (the chips live at the inventory head)
    var flag = document.getElementById("nl-filterflag");
    if (flag) {
      if (active) {
        flag.hidden = false;
        flag.textContent = t("filter_active", { f: t("filter_" + state.filter) }) + " · " + t("filter_show_all");
      } else { flag.hidden = true; }
    }
  }
  function filtered() {
    return units().filter(function (u) {
      if (state.filter === "all") return true;
      if (state.filter === "available") return u.status === "available";
      if (state.filter === "favs") return state.favs.indexOf(u.id) >= 0;
      return String(u.rooms) === state.filter;
    });
  }
  /* honest facet counts (booking-style): every chip states how many real
     units it matches, straight from the inventory data. */
  function filterCount(f) {
    if (f === "all") return units().length;
    if (f === "available") return units().filter(function (u) { return u.status === "available"; }).length;
    if (f === "favs") return units().filter(function (u) { return state.favs.indexOf(u.id) >= 0; }).length;
    return units().filter(function (u) { return String(u.rooms) === f; }).length;
  }

  /* block 6.5 - price + comps (PR5). Data-driven, honest: range + non-binding
     label + source + date; comps only when real; else an explicit pending state. */
  function price() {
    var pr = project().price || {};
    var comps = (pr.comps || []).map(function (r) {
      return { date: r.date || "", rooms: r.rooms, sqm: r.sqm != null ? r.sqm : r.size_sqm,
               total: Number(r.total != null ? r.total : r.price_total_nis) || 0,
               psqm: Number(r.psqm != null ? r.psqm : r.price_per_sqm_nis) || 0 };
    }).filter(function (r) { return r.total || r.psqm; });
    var head = '<span class="nl-eyebrow">' + esc(t("price_eyebrow")) + '</span><hr class="nl-rule"><h2>' + esc(t("price_title")) + "</h2>";

    if (!pr.avg_psqm && !comps.length) {
      return head + '<div class="nl-empty">' + esc(t("price_pending")) + "</div>";
    }

    // ranges (recorded transactions preferred; else avg ±12%)
    var totals = comps.map(function (r) { return r.total; }).filter(Boolean);
    var psqms = comps.map(function (r) { return r.psqm; }).filter(Boolean);
    var loT = totals.length ? Math.min.apply(null, totals) : 0, hiT = totals.length ? Math.max.apply(null, totals) : 0;
    var loP = psqms.length ? Math.min.apply(null, psqms) : (pr.avg_psqm ? Math.round(pr.avg_psqm * 0.88) : 0);
    var hiP = psqms.length ? Math.max.apply(null, psqms) : (pr.avg_psqm ? Math.round(pr.avg_psqm * 1.12) : 0);

    var big = totals.length ? (money(loT) + " - " + money(hiT))
                            : (money(loP) + " - " + money(hiP) + " " + t("per_sqm_short"));
    var chips = "";
    if (loP && hiP) { chips += '<span class="nl-pchip">' + esc(money(loP) + " - " + money(hiP) + " " + t("per_sqm_short")) + "</span>"; }
    if (pr.avg_psqm) { chips += '<span class="nl-pchip">' + esc(t("price_avg_psqm", { v: money(pr.avg_psqm) })) + "</span>"; }
    var metaBits = [];
    if (pr.date) { metaBits.push(t("price_updated_label") + " " + pr.date); }
    if (pr.source) { metaBits.push(pr.source); }
    var note = t("price_nonbinding") + (metaBits.length ? " · " + metaBits.join(" · ") : "");
    var card = '<div class="nl-pcard2"><div class="nl-pcard2__lbl">' + esc(totals.length ? t("price_estimate_label") : t("price_estimate_label_psqm")) + "</div>" +
      '<div class="nl-pcard2__big">' + esc(big) + "</div>" +
      '<div class="nl-pchips">' + chips + "</div>" +
      '<p class="nl-pnote">' + esc(note) + "</p></div>";

    var compsHtml = '<h3 class="nl-comps__h">' + esc(t("comps_title")) + "</h3>";
    if (comps.length) {
      var rows = comps.map(function (r) {
        return "<tr><td>" + esc(r.date) + "</td><td>" + esc(roomsLabel(r.rooms)) + "</td><td>" +
          esc((r.sqm != null ? r.sqm : "") + " " + t("sqm_unit")) + "</td><td>" + esc(money(r.total)) +
          "</td><td>" + esc(money(r.psqm) + " " + t("per_sqm_short")) + "</td></tr>";
      }).join("");
      compsHtml += '<div class="nl-comps__wrap"><table class="nl-comps"><thead><tr><th>' + esc(t("comps_col_date")) +
        "</th><th>" + esc(t("comps_col_rooms")) + "</th><th>" + esc(t("comps_col_sqm")) + "</th><th>" +
        esc(t("comps_col_total")) + "</th><th>" + esc(t("comps_col_psqm")) + "</th></tr></thead><tbody>" + rows +
        "</tbody></table></div><p class=\"nl-comps__src\">" + esc(t("comps_source")) + "</p>";
    } else {
      compsHtml += '<div class="nl-empty">' + esc(t("comps_pending")) + "</div>";
    }
    return head + '<div class="nl-pricewrap">' + card + compsHtml + "</div>";
  }

  /* block 8 - the complete world (map + spokes + stats + nearby) */
  function world() {
    var a = area(), m = a.map;
    var pins = m.pins.map(function (p) {
      var sp = spoke(p.ref); if (!sp) return "";
      return '<div class="nl-pin" data-act="pin" data-id="' + esc(p.ref) + '" style="inset-inline-start:' + p.x + "%;inset-block-start:" + p.y + '%"><span class="nl-pin__dot">' + svg(sp.icon, 12) + '</span><span class="nl-pin__lbl">' + esc(t(sp.label_key)) + "</span></div>";
    }).join("");
    var projPin = '<div class="nl-pin nl-pin--project" style="inset-inline-start:' + m.project_pin.x + "%;inset-block-start:" + m.project_pin.y + '%"><span class="nl-pin__dot">' + svg("pin", 14) + '</span><span class="nl-pin__lbl">' + esc(t("map_project_here")) + "</span></div>";
    var spokeCards = a.spoke_groups.map(function (g) {
      var items = g.items.map(function (id) { var sp = spoke(id); return sp ? "<span>" + esc(t(sp.label_key)) + "</span>" : ""; }).join("");
      return '<div class="nl-spoke"><div class="nl-spoke__h"><span class="ic">' + svg(g.icon, 16) + "</span>" + esc(t(g.label_key)) + '</div><div class="nl-spoke__items">' + items + "</div></div>";
    }).join("");
    var stats = a.stats.map(function (s) { return '<div class="nl-statbig"><b>' + esc(s.value) + "</b><span>" + esc(t(s.label_key)) + "</span></div>"; }).join("");
    var nearby = SR.order.filter(function (k) { return k !== state.projectKey; }).map(function (k) {
      var pr = SR.projects[k];
      return '<a class="nl-card" href="' + esc(pr.url || ("?project=" + k)) + '" style="text-decoration:none;display:block"><div class="ic">' + svg("cube", 18) + '</div><h4>' + esc(t(pr.name_key) || pr.name || "") + '</h4><p>' + esc(((pr.content && (pr.content[state.lang] || pr.content.en)) || {}).tagline || "") + "</p></a>";
    }).join("");
    return '<span class="nl-eyebrow">' + esc(t("world_eyebrow")) + '</span><hr class="nl-rule"><h2>' + esc(t("world_title")) + '</h2><p class="nl-lede" style="margin:10px 0 22px">' + esc(t("world_sub")) + "</p>" +
      '<div class="nl-world"><div class="nl-map">' + mapSVG(m) + projPin + pins + '<span class="nl-badge nl-badge--demo" style="position:absolute;inset-block-start:10px;inset-inline-end:10px">' + esc(t("map_title")) + "</span></div>" +
      '<div class="nl-spokes">' + spokeCards + "</div></div>" +
      '<div class="nl-stats">' + stats + "</div>" +
      '<h3 style="margin:32px 0 14px">' + esc(t("nearby_projects")) + '</h3><div class="nl-cards">' + nearby + "</div>";
  }
  function mapSVG(m) {
    var cx = m.coast_x || 16;
    return '<svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' +
      '<rect width="400" height="300" fill="#eef2e9"/>' +
      '<rect x="0" y="0" width="' + (cx / 100 * 400) + '" height="300" fill="#bcd7d8"/>' +
      '<path d="M' + (cx / 100 * 400) + ' 0 q 18 80 -6 150 q -16 80 10 150 L0 300 L0 0 Z" fill="#c7dedd"/>' +
      '<path d="M' + (cx / 100 * 400) + ' 0 q 18 80 -6 150 q -16 80 10 150" fill="none" stroke="#a9c7c6" stroke-width="2"/>' +
      '<path d="M70 300 Q120 200 110 120 Q104 60 150 0" fill="none" stroke="#7fae8e" stroke-width="10" opacity=".35"/>' +
      '<g stroke="#dcd6c7" stroke-width="6">' +
        '<path d="M90 0 V300"/><path d="M170 0 V300"/><path d="M250 0 V300"/><path d="M330 0 V300"/>' +
        '<path d="M60 70 H400"/><path d="M60 150 H400"/><path d="M60 230 H400"/>' +
      "</g>" +
      '<g stroke="#e7e1d2" stroke-width="2">' +
        '<path d="M130 0 V300"/><path d="M210 0 V300"/><path d="M290 0 V300"/><path d="M60 110 H400"/><path d="M60 190 H400"/>' +
      "</g></svg>";
  }

  /* block 7 - media + interior tour (PR6). Interior tour lazy-loads on click only;
     real assets only (tour_url / interior_panoramas); honest placeholder otherwise. */
  function media() {
    var p = project();
    var head = '<span class="nl-eyebrow">' + esc(t("media_title")) + '</span><hr class="nl-rule">';
    var tiles = "";
    if (p.video_url) { tiles += '<div class="nl-card"><div class="ic">' + svg("play", 18) + "</div><h4>" + esc(t("media_video")) + "</h4></div>"; }
    (p.gallery || []).forEach(function (g) { tiles += '<div class="nl-card" style="padding:0;aspect-ratio:4/3;background:#ddd center/cover url(' + esc(g) + ')"></div>'; });
    var galleryHtml = tiles ? '<div class="nl-cards" style="margin-top:18px">' + tiles + "</div>" : "";
    return head + interiorTour() + galleryHtml;
  }
  function interiorTour() {
    var p = project();
    var top = '<div class="nl-interior"><div class="nl-interior__head"><span class="nl-eyebrow">' + esc(t("tour_title")) + "</span></div>";
    var tour = safeHttpUrl(p.tour_url);
    if (tour) {
      return top + '<div class="nl-interior__stage" data-tour-url="' + esc(tour) + '"><button class="nl-btn nl-btn--gold" data-act="loadtour">' + esc(t("tour_open")) + '</button></div><p class="nl-interior__note">' + esc(t("tour_lazy_hint")) + "</p></div>";
    }
    if (p.interior_panoramas && p.interior_panoramas.length) {
      return top + '<div class="nl-interior__stage" data-pano="' + esc(JSON.stringify(p.interior_panoramas)) + '"><button class="nl-btn nl-btn--gold" data-act="loadpano">' + esc(t("tour_open_pano")) + '</button></div><p class="nl-interior__note">' + esc(t("tour_lazy_hint")) + "</p></div>";
    }
    // walk priority: the project's OWN pictures always beat the standard set.
    var pw = p.project_walk || [];
    if (pw.length) return top + dtMarkup(pw, t("dtour_tag_dedicated")) + "</div>";
    var us = units().filter(function (u2) { return u2.interior_url; }).map(function (u2) {
      return { key: "unit-" + u2.id, label: roomsLabel(u2.rooms) + " \u00B7 " + t("floor_label", { n: u2.floor }), url: u2.interior_url };
    });
    if (us.length) return top + dtMarkup(us, t("dtour_tag_units")) + "</div>";
    var dt = p.default_tour || [];
    if (dt.length) return top + dtMarkup(dt, t(p.default_tour_tier === "premium" ? "dtour_tag_premium" : "dtour_tag")) + "</div>";
    return top + '<div class="nl-empty">' + esc(t("tour_pending")) + "</div></div>";
  }
  /* ---- the DEFAULT walk (owner law: a default, not a fallback): first-person
     step-through of the standard apartment + building set. Drag pans the gaze,
     arrows and door chips walk between spaces. Replaced per-project the moment
     a developer tour arrives. ---- */
  function dtLabel(key) {
    var k = "dt_" + String(key).replace(/-/g, "_");
    var v = t(k);
    return v === k ? key.replace(/-/g, " ") : v;
  }
  function dtStepLabel(s2) { return s2.label || dtLabel(s2.key); }
  function dtMarkup(dt, tagText) {
    var chips = dt.map(function (s2, i) {
      return '<button class="nl-dtour__door' + (i === 0 ? " is-on" : "") + '" data-dt-i="' + i + '">' + esc(dtStepLabel(s2)) + "</button>";
    }).join("");
    return '<div class="nl-dtour" data-steps="' + esc(JSON.stringify(dt)) + '">' +
      '<div class="nl-dtour__stage" tabindex="0" role="application" aria-label="' + esc(t("dtour_hint")) + '">' +
        '<img class="nl-dtour__img" src="' + esc(dt[0].url) + '" alt="" draggable="false">' +
        '<button class="nl-dtour__nav nl-dtour__nav--prev" data-dt-step="-1" aria-label="' + esc(t("dtour_prev")) + '">&#8249;</button>' +
        '<button class="nl-dtour__nav nl-dtour__nav--next" data-dt-step="1" aria-label="' + esc(t("dtour_next")) + '">&#8250;</button>' +
        '<div class="nl-dtour__hud"><span class="nl-dtour__room">' + esc(dtStepLabel(dt[0])) + '</span><span class="nl-dtour__hint">' + esc(t("dtour_hint")) + "</span></div>" +
        '<span class="nl-dtour__tag">' + esc(tagText || t("dtour_tag")) + "</span>" +
      "</div>" +
      '<div class="nl-dtour__doors">' + chips + "</div></div>";
  }
  function dtInit() {
    var root = document.querySelector(".nl-dtour");
    if (!root || root.dataset.dtReady) return;
    root.dataset.dtReady = "1";
    var steps = []; try { steps = JSON.parse(root.dataset.steps || "[]"); } catch (e) {}
    if (!steps.length) return;
    var img = root.querySelector(".nl-dtour__img"), roomEl = root.querySelector(".nl-dtour__room");
    var doors = [].slice.call(root.querySelectorAll(".nl-dtour__door"));
    var stage = root.querySelector(".nl-dtour__stage");
    var i = 0, pan = 0, dragging = false, sx = 0, p0 = 0;
    // preload the next space so the walk never stutters
    function preload(n) { if (steps[n]) { var im = new Image(); im.src = steps[n].url; } }
    function apply() { img.style.transform = "translateX(" + pan + "%) scale(1.12)"; }
    var walkToken = 0;
    function go(n) {
      n = (n + steps.length) % steps.length;
      if (n === i) return;
      i = n; pan = 0;
      var tok = ++walkToken, target = steps[i];
      // stay "in the doorway" (faded) until the next space has actually
      // loaded - never show the old room under the new label.
      root.classList.add("is-walking");
      roomEl.textContent = dtStepLabel(target);
      doors.forEach(function (d2, j) { d2.classList.toggle("is-on", j === i); });
      var revealed = false;
      var reveal = function () {
        if (revealed || tok !== walkToken) return;
        revealed = true; apply();
        root.classList.remove("is-walking");
        preload(i + 1);
      };
      setTimeout(function () {
        if (tok !== walkToken) return;
        img.onload = reveal; img.onerror = reveal;
        img.src = target.url;
        if (img.complete && img.naturalWidth) reveal();
        setTimeout(reveal, 6000);
      }, 200);
    }
    root.addEventListener("click", function (e) {
      var st = e.target.closest("[data-dt-step]");
      if (st) { go(i + parseInt(st.dataset.dtStep, 10)); return; }
      var dr = e.target.closest("[data-dt-i]");
      if (dr) go(parseInt(dr.dataset.dtI, 10));
    });
    function down(x) { dragging = true; sx = x; p0 = pan; }
    function move(x) { if (!dragging) return; pan = Math.max(-9, Math.min(9, p0 + (x - sx) / 14)); apply(); }
    function up() { dragging = false; }
    stage.addEventListener("mousedown", function (e) { down(e.clientX); e.preventDefault(); });
    window.addEventListener("mousemove", function (e) { move(e.clientX); });
    window.addEventListener("mouseup", up);
    stage.addEventListener("touchstart", function (e) { down(e.touches[0].clientX); }, { passive: true });
    stage.addEventListener("touchmove", function (e) { move(e.touches[0].clientX); }, { passive: true });
    stage.addEventListener("touchend", up);
    stage.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") go(i + (isRTL() ? -1 : 1));
      if (e.key === "ArrowLeft") go(i + (isRTL() ? 1 : -1));
    });
    apply(); preload(1);
  }
  function loadTour(node) {
    var stage = node.closest(".nl-interior__stage"); if (!stage) return;
    var url = safeHttpUrl(stage.getAttribute("data-tour-url")); if (!url) return;
    var f = document.createElement("iframe");
    f.src = url; f.loading = "lazy"; f.title = t("tour_title"); f.className = "nl-interior__frame";
    f.setAttribute("allow", "fullscreen; xr-spatial-tracking; gyroscope; accelerometer");
    f.setAttribute("allowfullscreen", "");
    f.setAttribute("referrerpolicy", "no-referrer-when-downgrade");
    stage.innerHTML = ""; stage.appendChild(f);
  }
  function ensurePannellum(cb) {
    if (window.pannellum) { cb(); return; }
    var css = document.createElement("link"); css.rel = "stylesheet";
    css.href = "https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css"; document.head.appendChild(css);
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js";
    s.onload = cb; s.onerror = function () { cb(); }; document.head.appendChild(s);
  }
  function loadPano(node) {
    var stage = node.closest(".nl-interior__stage"); if (!stage) return;
    var data; try { data = JSON.parse(stage.getAttribute("data-pano") || "[]"); } catch (e) { data = []; }
    if (!data.length) return;
    stage.innerHTML = '<div class="nl-pano__loading">' + esc(t("loading_model")) + "</div>";
    ensurePannellum(function () {
      if (!window.pannellum) { stage.innerHTML = '<div class="nl-empty">' + esc(t("tour_pending")) + "</div>"; return; }
      stage.innerHTML = '<div id="nl-pano-view" style="width:100%;height:100%"></div>';
      var scenes = {}, first = null;
      data.forEach(function (s, i) {
        var id = "s" + i; if (i === 0) { first = id; }
        scenes[id] = { type: "equirectangular", panorama: s.url || s.image || s, title: s.title || "" };
      });
      try { window.pannellum.viewer("nl-pano-view", { default: { firstScene: first, autoLoad: true, showControls: true }, scenes: scenes }); }
      catch (e) { stage.innerHTML = '<div class="nl-empty">' + esc(t("tour_pending")) + "</div>"; }
    });
  }

  /* block 9 - investor */
  function investor() {
    var pts = [["shield", "investor_pt_process"], ["scale", "investor_pt_legal"], ["globe", "investor_pt_finance"]];
    return '<div class="nl-card--dark nl-card" style="padding:clamp(22px,4vw,40px)"><div style="display:grid;grid-template-columns:1fr 1.2fr;gap:28px;align-items:center" class="nl-investorgrid">' +
      '<div><span class="nl-eyebrow" style="color:#e9d9a9">' + esc(t("seo_eyebrow")) + '</span><h2 style="color:#fff;margin-top:8px">' + esc(t("investor_title")) + '</h2><p style="color:#d3ccbd;margin-top:10px">' + esc(t("investor_sub")) + '</p><button class="nl-btn nl-btn--gold" style="margin-top:18px" data-act="scroll" data-id="inquiry">' + esc(t("investor_cta")) + "</button></div>" +
      '<div class="nl-cards" style="grid-template-columns:1fr">' + pts.map(function (p) { return '<div style="display:flex;gap:12px;align-items:flex-start"><span style="color:#e9d9a9;flex:none">' + svg(p[0], 20) + "</span><b style=\"color:#fff;font-weight:600\">" + esc(t(p[1])) + "</b></div>"; }).join("") + "</div>" +
      "</div></div>";
  }

  /* block 10 - SEO body (placeholder content from data) */
  function seoBody() {
    return '<div style="max-width:760px"><span class="nl-eyebrow">' + esc(t("seo_eyebrow")) + '</span><hr class="nl-rule"><h2>' + esc(content("seo_h")) + '</h2><p class="nl-lede" style="margin-top:14px">' + esc(content("seo_p")) + "</p></div>";
  }
  /* visible FAQ accordion (the FAQPage JSON-LD is emitted server-side from the same meta) */
  function faq() {
    var items = (project().faq || []).filter(function (r) { return (r.q || r.question) && (r.a || r.answer); });
    if (!items.length) { return ""; }
    var rows = items.map(function (r) {
      return '<details class="nl-faq__item"><summary>' + esc(r.q || r.question) + "</summary><p>" + esc(r.a || r.answer) + "</p></details>";
    }).join("");
    return '<div class="nl-faq" style="max-width:760px;margin-top:36px"><span class="nl-eyebrow">' + esc(t("faq_title")) + '</span><hr class="nl-rule">' + rows + "</div>";
  }

  /* block 11 - inquiry (money moment) */
  function inquiry() {
    return '<div class="nl-inquiry"><div class="nl-inquiry__grid">' +
      '<div><span class="nl-eyebrow" style="color:#e9d9a9">' + esc(t("hero_cta_primary")) + '</span><h2 style="margin-top:8px">' + esc(t("form_title")) + '</h2><p class="nl-lede" style="margin-top:12px">' + esc(t("form_sub")) + "</p>" +
        '<div class="nl-trust"><span>' + svg("shield", 16) + esc(t("form_consent")) + "</span></div></div>" +
      '<form class="nl-form" id="nl-form" novalidate>' +
        '<div class="nl-ctxchip" id="nl-formctx"><span class="d"></span>' + esc(t("form_no_unit")) + "</div>" +
        '<input class="nl-input" name="name" placeholder="' + esc(t("form_name")) + '" autocomplete="name">' +
        '<div class="nl-form__row"><input class="nl-input" name="phone" inputmode="tel" placeholder="' + esc(t("form_phone")) + '" autocomplete="tel"><input class="nl-input" name="email" inputmode="email" placeholder="' + esc(t("form_email")) + '" autocomplete="email"></div>' +
        '<button class="nl-btn nl-btn--accent nl-btn--block" type="submit" style="min-height:52px">' + esc(t("form_submit")) + "</button>" +
        '<div id="nl-formmsg" hidden></div>' +
        '<p class="nl-consent">' + esc(t("form_consent")) + "</p>" +
      "</form></div></div>";
  }

  /* block 12 - disclaimer */
  function disclaimer() {
    return '<div class="nl-disclaimer"><b>' + esc(t("disclaimer_title")) + "</b><p>" + esc(t("disclaimer_text")) + "</p></div>";
  }

  /* sticky inquire + whatsapp */
  function sticky() {
    var wa = SR.config.whatsapp ? '<a class="nl-sticky__wa" id="nl-wa" href="#" target="_blank" rel="noopener">' + svg("wa", 16) + esc(t("whatsapp_cta")) + "</a>" : "";
    return '<div class="nl-sticky" id="nl-sticky"><button class="nl-sticky__main" data-act="scroll" data-id="inquiry"><span>' + svg("phone", 16) + '</span><span>' + esc(t("sticky_cta")) + '<span class="nl-sticky__ctx" id="nl-stickyctx"></span></span></button>' + wa + "</div>";
  }

  /* compare tray - top pick ranked with TOPSIS (Hwang & Yoon 1981):
     vector-normalized closeness to the ideal over sqm, floor and balcony
     (equal weights, all benefit criteria; price joins when all have one). */
  function topsisTop(ids) {
    var us = ids.map(unit).filter(Boolean); if (us.length < 2) return null;
    var crit = [
      function (u) { return Number(u.sqm) || 0; },
      function (u) { return Number(u.floor) || 0; },
      function (u) { return Number(u.balcony) || 0; }
    ];
    var scores = us.map(function () { return { p: 0, m: 0 }; });
    crit.forEach(function (get) {
      var vals = us.map(get), norm = Math.sqrt(vals.reduce(function (a, v) { return a + v * v; }, 0)) || 1;
      var nv = vals.map(function (v) { return v / norm; });
      var best = Math.max.apply(null, nv), worst = Math.min.apply(null, nv);
      nv.forEach(function (v, i) { scores[i].p += (v - best) * (v - best); scores[i].m += (v - worst) * (v - worst); });
    });
    var top = null, topc = -1;
    scores.forEach(function (sc, i) {
      var den = Math.sqrt(sc.p) + Math.sqrt(sc.m);
      var c = den ? Math.sqrt(sc.m) / den : 0;
      if (c > topc) { topc = c; top = us[i].id; }
    });
    return top;
  }
  function compareTray() {
    /* v2 owns comparison inside its body-level dialog. Never render the
       legacy fixed tray, even when the private session has selected units. */
    if (unitV2Enabled()) return "";
    if (!state.compare.length) return '<div class="nl-compare" id="nl-compare"></div>';
    var top = topsisTop(state.compare);
    var items = state.compare.map(function (id) { var u = unit(id); return u ? '<span class="nl-cmpitem' + (id === top && state.compare.length > 1 ? " is-top" : "") + '">' + (id === top && state.compare.length > 1 ? '<i class="nl-cmptop">★ ' + esc(t("compare_top")) + "</i>" : "") + '<b>' + esc(unitDisplayLabel(u)) + "</b> " + esc(roomsLabel(u.rooms)) + " · " + esc(u.sqm + t("sqm_unit")) + ' <button data-act="compare" data-id="' + esc(id) + '" aria-label="' + esc(unitV2Enabled() ? t("unit_compare_remove") : "remove") + '">×</button></span>' : ""; }).join("");
    return '<div class="nl-compare is-on" id="nl-compare"><div class="nl-wrap nl-compare__row"><b>' + esc(t("compare_title")) + '</b><div class="nl-compare__items">' + items + '</div><button class="nl-btn nl-btn--sm nl-btn--ghost" data-act="compare-clear" style="color:#cfc8b6;border-color:rgba(242,236,222,.2)">' + esc(t("compare_clear")) + '</button><button class="nl-btn nl-btn--sm nl-btn--accent" data-act="scroll" data-id="inquiry">' + esc(t("compare_inquire")) + "</button></div></div>";
  }

  /* footer */
  function footer() {
    var projLinks = SR.order.map(function (k) {
      var p = SR.projects[k];
      var href = unitV2Enabled()
        ? (safeHttpUrl(p.url) || homeHref())
        : ("project.html?project=" + k);
      return '<li><a href="' + esc(href) + '">' + esc(t(p.name_key)) + "</a></li>";
    }).join("");
    // ONE switcher law (owner 2026-08-08): when the server topbar owns language
    // switching, this footer column was the page's THIRD language switcher.
    var langLinks = document.querySelector(".nlptop-l") ? "" : pageLangs().map(function (l) { return '<li><a href="' + esc(langHref(l)) + '" data-act="lang" data-id="' + l + '">' + esc(t("lang_" + l)) + "</a></li>"; }).join("");
    return '<footer class="nl-footer"><div class="nl-wrap"><div class="nl-footer__row">' +
      '<div><a class="nl-brand" href="' + esc(homeHref()) + '"><span class="nl-brand__mark">N</span><span class="nl-brand__name" style="color:#efe7d6">' + esc(t("brand")) + '</span></a><p style="color:#b8b1a2;font-size:14px;margin-top:12px;max-width:34ch">' + esc(t("footer_tagline")) + "</p></div>" +
      "<div><h5>" + esc(t("footer_col_projects")) + "</h5><ul>" + projLinks + "</ul></div>" +
      "<div><h5>" + esc(t("footer_col_areas")) + '</h5><ul><li><a href="#world">' + esc(t("area_sde_dov")) + "</a></li></ul></div>" +
      "<div><h5>" + esc(t("footer_col_langs")) + "</h5><ul>" + langLinks + "</ul></div>" +
      '</div><div class="nl-footer__bottom">' + esc(t("footer_rights")) + "</div></div></footer>";
  }

  /* ---------------- home page ---------------- */
  function homeMain() {
    var cards = SR.order.map(function (k) {
      var p = SR.projects[k], avail = p.units.filter(function (u) { return u.status === "available"; }).length;
      return '<a class="nl-pcard" href="' + esc(p.url || ("?project=" + k)) + '"><div class="nl-pcard__img" style="background-image:url(' + esc(p.model_poster) + ')"><span class="nl-badge nl-badge--demo" style="position:absolute;inset-block-start:10px;inset-inline-end:10px">' + esc(t("demo_badge")) + '</span></div><div class="nl-pcard__body"><div class="nl-pcard__name">' + esc(t(p.name_key) || p.name || "") + '</div><p class="nl-muted" style="font-size:14px;margin-top:4px">' + esc(((p.content && (p.content[state.lang] || p.content.en)) || {}).tagline || "") + '</p><div class="nl-pcard__meta"><span class="nl-muted" style="font-size:13px">' + esc(t("card_units", { n: (p.units || []).length })) + '</span><span style="color:var(--terracotta);font-weight:600;font-size:13px">' + esc(t("card_explore")) + "</span></div></div></a>";
    }).join("");
    return "<main>" +
      '<section class="nl-wrap nl-homehero"><span class="nl-eyebrow">' + esc(t("home_hero_eyebrow")) + '</span><h1 style="margin-top:12px">' + esc(t("home_hero_title")) + '</h1><p class="nl-lede">' + esc(t("home_hero_sub")) + "</p></section>" +
      '<section class="nl-sec nl-wrap" id="projects"><span class="nl-eyebrow">' + esc(t("home_gallery_eyebrow")) + '</span><hr class="nl-rule"><h2>' + esc(t("home_gallery_title")) + '</h2><p class="nl-lede" style="margin:10px 0 22px">' + esc(t("home_gallery_sub")) + '</p><div class="nl-gallery">' + cards + "</div></section>" +
      '<section class="nl-sec nl-wrap" id="list"><div class="nl-inquiry"><div class="nl-inquiry__grid"><div><span class="nl-eyebrow" style="color:#e9d9a9">' + esc(t("nav_list")) + '</span><h2 style="margin-top:8px">' + esc(t("home_list_title")) + '</h2><p class="nl-lede" style="margin-top:12px">' + esc(t("home_list_sub")) + '</p></div><div style="display:flex;align-items:center;justify-content:center"><button class="nl-btn nl-btn--gold" style="min-height:54px">' + esc(t("home_list_cta")) + "</button></div></div></div></section>" +
      "</main>";
  }

  /* =====================================================================
     INTERACTIONS
  ===================================================================== */
  function afterRender() {
    var mv = document.getElementById("nl-mv");
    if (mv) {
      var fr = project() ? (project().frame_radius_m || 150) : 150;
      try { mv.minCameraOrbit = "auto 46deg " + Math.round(fr * 0.5) + "m"; mv.maxCameraOrbit = "auto 87deg " + Math.round(fr * 1.9) + "m"; } catch (e) {}
      var poster = document.getElementById("nl-poster"), spin = document.getElementById("nl-spin"), modelError = document.getElementById("nl-model-error");
      var reveal = function () {
        state.mvReady = true;
        if (poster) poster.classList.add("is-hidden");
        if (spin) spin.style.opacity = "0";
        if (modelError) modelError.hidden = true;
        mv.classList.remove("nlp3d-model-error-source");
      };
      var fail = function () {
        state.mvReady = false;
        if (spin) spin.style.opacity = "0";
        if (poster) poster.classList.remove("is-hidden");
        if (modelError) { modelError.hidden = false; modelError.textContent = t("model_error"); }
        mv.classList.add("nlp3d-model-error-source");
      };
      if (mv.loaded) reveal(); else mv.addEventListener("load", reveal, { once: true });
      mv.addEventListener("error", fail);
      // safety: never leave poster forever if load is delayed
      setTimeout(function () { if (!state.mvReady && mv.modelIsVisible) reveal(); }, 6000);
    }
    document.querySelectorAll('[data-act="lang"], .nl-brand, model-viewer, .nl-lang, .nlhv2-langbar').forEach(function (el) {
      el.setAttribute("translate", "no"); el.classList.add("notranslate");
      if (el.parentElement && el.getAttribute("data-act") === "lang") { el.parentElement.setAttribute("translate", "no"); el.parentElement.classList.add("notranslate"); }
    });
    if (state.page === "project") {
      // ONE contact bar: the engine sticky (call + WhatsApp) owns this page;
      // the global floating CTA cluster would stack on the same corner.
      document.body.classList.add("nl-has-engine");
      dtInit();
      updateFormCtx(); updateSticky();
      if (state.unitId && unit(state.unitId)) {
        if (unitV2Enabled()) selectUnit(state.unitId, true, document.getElementById("nl-mv"));
        else selectUnit(state.unitId, true);
      }
      else if (SR.config.selected_unit_surface) clearUnitScreen();
      var form = document.getElementById("nl-form");
      if (form) form.addEventListener("submit", onSubmit);
      window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
      setupSpy();
      adoptUnifiedMap(); wireMapSync();
    }
  }

  /* ---- ONE-map doctrine: the unified POI map (project-experience) is THE map.
     The engine adopts it right under the theater so a buyer spinning the model
     reads the surroundings in the same glance, and gives up its own plain map. */
  function adoptUnifiedMap() {
    var uni = document.getElementById("nlpjx-map");
    if (!uni) return;
    var building = document.getElementById("building");
    if (building) {
      building.insertAdjacentElement("afterend", uni);
      uni.classList.add("nl-adopted-map");
    }
    var em = ROOT.querySelector(".nl-map");
    if (em) { em.style.display = "none"; }
  }
  /* model orbit -> map bearing (user gestures only; auto-rotate must not spin
     the map). Convention: model -z axis = north, so bearing = -theta. */
  function wireMapSync() {
    var mv = document.getElementById("nl-mv");
    if (!mv || mv.dataset.nlMapSync) return;
    mv.dataset.nlMapSync = "1";
    var last = 0;
    mv.addEventListener("camera-change", function (ev) {
      var now = Date.now(); if (now - last < 120) return; last = now;
      updateSunMark(); // the sun marker tracks every rotation, auto-rotate included
      if (!ev.detail || ev.detail.source !== "user-interaction") return;
      var map = window.NLPJX_MAP;
      if (!map || typeof mv.getCameraOrbit !== "function") return;
      try { map.setBearing(-(mv.getCameraOrbit().theta * 180 / Math.PI) % 360); } catch (e) {}
    });
  }
  var DIR_BEARING = { north: 0, "north-east": 45, east: 90, "south-east": 135, south: 180, "south-west": 225, west: 270, "north-west": 315 };
  /* Direct-sun estimate (solar geometry per Michalsky 1988; exposure language
     per EN 17037): equinox reference day, declination 0, 5-degree low-sun
     cutoff, numeric integration in 6-minute steps. Geometric only - the
     label says so: no surrounding-obstruction modeling. */
  function sunHours(u) {
    var k = dirKey(u.dir); if (!k || !(k in DIR_BEARING)) return null;
    var p = project(), lat = (p.geo && Number(p.geo.lat)) || 32.08;
    var A = DIR_BEARING[k] * Math.PI / 180, phi = lat * Math.PI / 180, mins = 0;
    for (var m = 4 * 60; m <= 20 * 60; m += 6) {
      var H = (m / 60 - 12) * 15 * Math.PI / 180;
      var sinEl = Math.cos(phi) * Math.cos(H);
      if (sinEl <= Math.sin(5 * Math.PI / 180)) continue;
      var azn = Math.PI + Math.atan2(Math.sin(H), Math.cos(H) * Math.sin(phi));
      if (Math.cos(azn - A) > 0) mins += 6;
    }
    return Math.round(mins / 30) / 2;
  }
  var viewCone = null;
  /* A translucent terracotta cone anchored on the building pin, rotated with the
     terrain (rotationAlignment map), pointing where the selected apartment looks. */
  function showViewCone(bearing) {
    var map = window.NLPJX_MAP, gl = window.mapboxgl, p = project();
    if (!map || !gl || !p || !p.geo || !Number(p.geo.lat) || !Number(p.geo.lng)) return;
    try {
      if (!viewCone) {
        var el = document.createElement("div");
        el.style.pointerEvents = "none";
        el.innerHTML = '<svg width="150" height="150" viewBox="0 0 150 150" style="display:block">' +
          '<defs><linearGradient id="nl-cone-g" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0" stop-color="#C2563A" stop-opacity="0"/>' +
          '<stop offset="1" stop-color="#C2563A" stop-opacity="0.55"/></linearGradient></defs>' +
          '<path d="M75 75 L44 8 A78 78 0 0 1 106 8 Z" fill="url(#nl-cone-g)" stroke="#C2563A" stroke-opacity="0.35" stroke-width="1"/></svg>';
        viewCone = new gl.Marker({ element: el, rotationAlignment: "map", pitchAlignment: "map", anchor: "center" })
          .setLngLat([Number(p.geo.lng), Number(p.geo.lat)]);
      }
      viewCone.setRotation(bearing).addTo(map);
    } catch (e) {}
  }
  function easeMapToUnitView(u) {
    var k = dirKey(u.dir);
    if (!k || !(k in DIR_BEARING)) return;
    showViewCone(DIR_BEARING[k]);
    var map = window.NLPJX_MAP;
    if (!map) return;
    try { map.easeTo({ bearing: DIR_BEARING[k], duration: 900 }); } catch (e) {}
  }
  // the map boots lazily; when it arrives, honor a selection made before it
  document.addEventListener("nlpjx:map", function () {
    var u = state.unitId && unit(state.unitId);
    if (u) easeMapToUnitView(u);
  });

  /* ---- walk-inside (FP walkthrough) built from real unit data. JS port of
     nadlan_ifp_rooms (interior-fp.php); assets print server-side on project
     pages and window.nadlanInitFP re-initializes injected walkthroughs. ---- */
  function fpRooms(u) {
    var count = Math.max(1, Math.min(8, parseFloat(u.rooms) || 4));
    var sqm = Math.max(30, parseInt(u.sqm, 10) || 85);
    var bedrooms = Math.max(0, Math.ceil(count) - 1);
    /* A protected room is a material safety/purchase fact, not a layout
       convention.  Only label one when the unit payload explicitly confirms
       it; older showroom payloads do not carry this datum. */
    var hasMamad = u.protected_room === true || u.protected_room === 1 ||
      u.protected_room === "1" || u.has_mamad === true || u.has_mamad === 1 ||
      u.has_mamad === "1";
    var salonA = sqm * 0.40, bedA = bedrooms ? (sqm * 0.42) / bedrooms : 0;
    var k = dirKey(u.dir), wall = "";
    if (k && k.indexOf("south") >= 0) wall = "s";
    else if (k && k.indexOf("north") >= 0) wall = "n";
    else if (k && k.indexOf("east") >= 0) wall = "e";
    else if (k && k.indexOf("west") >= 0) wall = "w";
    var out = [{ key: "salon", label: t("fp_salon"), w: +Math.sqrt(salonA * 1.4).toFixed(1), d: +Math.sqrt(salonA / 1.4).toFixed(1), win: wall }];
    out.push({ key: "kitchen", label: t("fp_kitchen"), w: 3.4, d: +Math.max(2.4, sqm * 0.12 / 3.4).toFixed(1), win: wall });
    for (var i = 1; i <= bedrooms; i++) {
      var isMamad = hasMamad && i === bedrooms;
      out.push({ key: "bed" + i, label: isMamad ? t("fp_mamad") : (i === 1 ? t("fp_master") : t("fp_bed") + " " + i),
        w: +Math.sqrt(bedA * 1.15).toFixed(1), d: +Math.sqrt(bedA / 1.15).toFixed(1),
        win: isMamad || !wall ? "" : (wall === "n" ? "e" : wall) });
    }
    var bal = parseInt(u.balcony, 10) || 0;
    if (bal > 0) out.push({ key: "balcony", label: t("fp_balcony") + " (" + bal + " " + t("sqm_unit") + ")", w: +Math.sqrt(bal * 2.2).toFixed(1), d: +Math.sqrt(bal / 2.2).toFixed(1), win: "open" });
    return out;
  }
  function fpMarkup(u) {
    return '<div class="nlifp" data-rooms="' + esc(JSON.stringify(fpRooms(u))) + '" ' +
      'data-to-template="' + esc(t("fp_to_room")) + '" ' +
      'data-area-template="' + esc(t("fp_area_approx")) + '">' +
      '<div class="nlifp-stage" tabindex="0" role="application" aria-label="' + esc(t("fp_aria")) + '">' +
      '<div class="nlifp-cam"><div class="nlifp-world"></div></div>' +
      '<div class="nlifp-hud"><span class="nlifp-room"></span><span class="nlifp-hint">' + esc(t("fp_hint")) + "</span></div>" +
      '<span class="nlifp-tag">' + esc(t("fp_tag")) + "</span></div>" +
      '<div class="nlifp-doors"></div></div>';
  }
  function fpInit() { try { if (window.nadlanInitFP) window.nadlanInitFP(); } catch (e) {} }

  /* ---- the inline window viewport (the mvt tab IS the window): a small
     satellite + 3D-buildings map standing at the unit's floor height, looking
     out in its direction. Look buttons rotate the gaze in 30deg steps. ---- */
  var winState = { map: null, bearing: null, vert: 0, unit: null };
  function winCam(map, u, brOverride, vert) {
    var gl = window.mapboxgl, p = project();
    var k = dirKey(u.dir), br = (brOverride != null) ? brOverride : ((k && k in DIR_BEARING) ? DIR_BEARING[k] : 270);
    var fh = parseFloat(p.floor_height_m) || 3.05;
    var alt = Math.max(10, (parseInt(u.floor, 10) || 1) * fh + 1.6);
    try {
      var cam = map.getFreeCameraOptions();
      cam.position = gl.MercatorCoordinate.fromLngLat({ lng: Number(p.geo.lng), lat: Number(p.geo.lat) }, alt);
      // standing at the window: pitch 86 = eye level at the horizon; vertical
      // drag tilts the gaze down toward the street or up toward the sky.
      var pitch = Math.max(35, Math.min(90, 86 + (vert || 0)));
      cam.setPitchBearing(pitch, br);
      map.setFreeCameraOptions(cam);
    } catch (e) {}
    return br;
  }
  function winStageInit(u) {
    var host = document.querySelector(".nl-tabpane .nl-winstage__map");
    if (!host || !u || !SR.config.mapbox_token) return;
    var boot = function () {
      var gl = window.mapboxgl; if (!gl || !document.contains(host)) return;
      if (winState.map) { try { winState.map.remove(); } catch (e) {} winState.map = null; }
      gl.accessToken = SR.config.mapbox_token;
      var bootBr = (function () { var k = dirKey(u.dir); return (k && k in DIR_BEARING) ? DIR_BEARING[k] : 270; })();
      var map = new gl.Map({ container: host, style: "mapbox://styles/mapbox/satellite-streets-v12",
        center: [Number(project().geo.lng), Number(project().geo.lat)], zoom: 16.5,
        pitch: 70, bearing: bootBr, maxPitch: 85,
        interactive: false, attributionControl: false });
      winState.map = map; winState.unit = u.id; winState.bearing = null;
      map.on("load", function () {
        try { map.addLayer({ id: "nl-win-sky", type: "sky", paint: { "sky-type": "atmosphere", "sky-atmosphere-sun-intensity": 8 } }); } catch (e) {}
        try {
          var layers = map.getStyle().layers, lab;
          for (var i = 0; i < layers.length; i++) { if (layers[i].type === "symbol" && layers[i].layout && layers[i].layout["text-field"]) { lab = layers[i].id; break; } }
          map.addLayer({ id: "nl-win-3d", source: "composite", "source-layer": "building", filter: ["==", "extrude", "true"], type: "fill-extrusion", minzoom: 13,
            paint: { "fill-extrusion-color": "#d8d2c4", "fill-extrusion-height": ["get", "height"], "fill-extrusion-base": ["get", "min_height"], "fill-extrusion-opacity": 0.85 } }, lab);
        } catch (e) {}
        winState.vert = 0;
        winState.bearing = winCam(map, u, null, 0);
      });
      // free look: drag turns the head - sideways changes bearing, up/down
      // tilts the gaze. This is a window, not a still.
      var dragging = false, lx = 0, ly = 0;
      var lookStart = function (x, y) { dragging = true; lx = x; ly = y; };
      var lookMove = function (x, y) {
        if (!dragging || !winState.map || winState.unit !== u.id) return;
        winState.bearing = ((winState.bearing == null ? 270 : winState.bearing) + (x - lx) * 0.35 + 360) % 360;
        winState.vert = Math.max(-45, Math.min(10, (winState.vert || 0) - (y - ly) * 0.22));
        lx = x; ly = y;
        winCam(winState.map, u, winState.bearing, winState.vert);
      };
      var lookEnd = function () { dragging = false; };
      host.style.cursor = "grab";
      host.addEventListener("mousedown", function (e) { lookStart(e.clientX, e.clientY); e.preventDefault(); });
      window.addEventListener("mousemove", function (e) { lookMove(e.clientX, e.clientY); });
      window.addEventListener("mouseup", lookEnd);
      host.addEventListener("touchstart", function (e) { lookStart(e.touches[0].clientX, e.touches[0].clientY); }, { passive: true });
      host.addEventListener("touchmove", function (e) { lookMove(e.touches[0].clientX, e.touches[0].clientY); e.preventDefault(); }, { passive: false });
      host.addEventListener("touchend", lookEnd);
      host.addEventListener("dblclick", function (e) { e.preventDefault(); winFs(); });
    };
    if (window.mapboxgl) { boot(); return; }
    var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css"; document.head.appendChild(l);
    var sc = document.createElement("script"); sc.src = "https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"; sc.onload = boot; document.head.appendChild(sc);
  }
  function winLook(u, delta) {
    if (!winState.map || winState.unit !== u.id) return;
    var base = winState.bearing == null ? 270 : winState.bearing;
    winState.bearing = (base + delta + 360) % 360;
    winCam(winState.map, u, winState.bearing, winState.vert);
  }
  /* Fullscreen window view (owner 2026-07-11: "this window is too small").
     Native element fullscreen where it exists; iPhone Safari has none for
     divs, so a fixed-overlay fallback with an explicit exit. */
  function winFs() {
    var stage = document.querySelector(".nl-tabpane .nl-winstage");
    if (!stage) return;
    var resize = function () { try { if (winState.map) winState.map.resize(); } catch (e) {} };
    var isOn = stage.classList.contains("nl-winstage--fs") || document.fullscreenElement === stage;
    var fsBtn = stage.querySelector(".nl-winstage__fs");
    var setLabel = function (on) { if (fsBtn) { var l = t(on ? "winview_fs_exit" : "winview_fs"); fsBtn.setAttribute("aria-label", l); fsBtn.setAttribute("title", l); } };
    if (isOn) {
      if (document.fullscreenElement === stage && document.exitFullscreen) { try { document.exitFullscreen(); } catch (e) {} }
      stage.classList.remove("nl-winstage--fs");
      document.body.classList.remove("nl-noscroll");
      setLabel(false);
      setTimeout(resize, 80);
      return;
    }
    var overlay = function () {
      stage.classList.add("nl-winstage--fs");
      document.body.classList.add("nl-noscroll");
      setLabel(true);
      setTimeout(resize, 80);
    };
    if (!/iPhone/.test(navigator.userAgent) && stage.requestFullscreen) {
      try { stage.requestFullscreen().then(function () { setLabel(true); setTimeout(resize, 80); }).catch(overlay); } catch (e) { overlay(); }
    } else { overlay(); }
  }
  document.addEventListener("fullscreenchange", function () {
    try { if (winState.map) winState.map.resize(); } catch (e) {}
    if (!document.fullscreenElement) {
      var st2 = document.querySelector(".nl-winstage--fs");
      if (st2) { st2.classList.remove("nl-winstage--fs"); document.body.classList.remove("nl-noscroll"); }
    }
  });

  /* ---- the view FROM the window, on the live map: FreeCamera at the unit's
     real floor height, looking out in the apartment's direction. ---- */
  function winView(u) {
    var run = function () {
      var map = window.NLPJX_MAP, gl = window.mapboxgl, p = project();
      if (!map || !gl || !p || !p.geo || !Number(p.geo.lat) || p.geo.confidence === "city") return;
      var k = dirKey(u.dir), br = (k && k in DIR_BEARING) ? DIR_BEARING[k] : 270;
      var fh = parseFloat(p.floor_height_m) || 3.05;
      var alt = Math.max(10, (parseInt(u.floor, 10) || 1) * fh + 1.6);
      var band = document.getElementById("nlpjx-map");
      if (band) band.scrollIntoView({ behavior: "smooth", block: "center" });
      setTimeout(function () {
        try {
          var cam = map.getFreeCameraOptions();
          cam.position = gl.MercatorCoordinate.fromLngLat({ lng: Number(p.geo.lng), lat: Number(p.geo.lat) }, alt);
          var rad = br * Math.PI / 180, d = 700;
          var tLat = Number(p.geo.lat) + (Math.cos(rad) * d) / 111320;
          var tLng = Number(p.geo.lng) + (Math.sin(rad) * d) / (111320 * Math.cos(Number(p.geo.lat) * Math.PI / 180));
          cam.lookAtPoint({ lng: tLng, lat: tLat });
          map.setFreeCameraOptions(cam);
          showViewCone(br);
        } catch (e) {}
      }, 750);
    };
    if (window.NLPJX_MAP) { run(); return; }
    // boot the lazy map by bringing it into view, then run once ready
    var band = document.getElementById("nlpjx-map");
    if (band) band.scrollIntoView({ behavior: "smooth", block: "center" });
    document.addEventListener("nlpjx:map", function once() {
      document.removeEventListener("nlpjx:map", once);
      setTimeout(run, 900);
    });
  }

  ROOT.addEventListener("click", function (e) {
    var node = e.target.closest("[data-act]"); if (!node) return;
    var act = node.dataset.act, id = node.dataset.id;
    if (act === "lang") { e.preventDefault(); switchLang(id); }
    else if (act === "select") selectUnit(id, false, node);
    else if (act === "close") closePanel();
    else if (act === "unit-back") closePanel();
    else if (act === "unit-tool") { openUnitTool(node.dataset.tool, unit(state.unitId), node); }
    else if (act === "view") setView(id);
    else if (act === "tab") setTab(id);
    else if (act === "filter") { state.filter = id; refresh("inventory"); applyStageFilter(); }
    else if (act === "light") { state.sunMin = ({ day: 720, dusk: 1110, night: 1200 })[id] || 720; applyLight(); }
    else if (act === "cotour") { cotourStart(); }
    else if (act === "winfs") { winFs(); }
    else if (act === "resetview") { resetView(); }
    else if (act === "studio") { openStudio(id); }
    else if (act === "studio-any") {
      var avail = units().filter(function (x) { return x.status === "available"; });
      openStudio(state.unitId || (avail[0] || units()[0] || {}).id);
    }
    else if (act === "fav") { e.stopPropagation(); toggleFav(id); }
    else if (act === "compare") { e.stopPropagation(); toggleCompare(id); }
    else if (act === "compare-clear") { state.compare = []; refreshCompare(); }
    else if (act === "share") share(id);
    else if (act === "scroll") { e.preventDefault(); scrollTo(id); }
    else if (act === "loadtour") loadTour(node);
    else if (act === "loadpano") loadPano(node);
    else if (act === "pin") highlightPin(node);
    else if (act === "winview") { var wu = unit(node.dataset.id); if (wu) winView(wu); }
    else if (act === "winlook") { var wl = unit(node.dataset.id); if (wl) winLook(wl, parseInt(node.dataset.d, 10) || 0); }
  });
  ROOT.addEventListener("input", function (e) {
    if (e.target && e.target.id === "nl-sunslider") {
      state.sunMin = parseInt(e.target.value, 10) || 720;
      applyLight();
    }
  });
  ROOT.addEventListener("keydown", function (e) {
    var node = e.target.closest('[role="button"][data-act="select"]');
    if (node && (e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      if (unitV2Enabled()) selectUnit(node.dataset.id, false, node);
      else selectUnit(node.dataset.id);
    }
    if (e.key === "Escape") closePanel();
  });

  function setView(v) {
    state.view = v;
    document.querySelectorAll('[data-act="view"]').forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.id === v); });
    var fac = document.getElementById("nl-facade"); if (fac) fac.classList.toggle("is-on", v === "facade");
  }
  function setTab(tb) {
    state.tab = tb; var u = unit(state.unitId); if (!u) return;
    document.querySelectorAll(".nl-tab").forEach(function (b) { b.setAttribute("aria-selected", b.dataset.id === tb); });
    var pane = document.querySelector(".nl-tabpane"); if (pane) pane.innerHTML = tabPane(u);
    if (tb === "tour") fpInit();
    if (tb === "view") winStageInit(u);
  }


  /* ---- audit fragment: selected-unit surface ---- */
/* Add `tool: null` to the existing state object. */
var UNIT_MQ = window.matchMedia(
  "(max-width:700px), " +
  "(max-width:900px) and (max-height:500px) and (pointer:coarse)"
);

/* v2 deliberately uses a wider phone/tablet boundary and a landscape escape
   hatch. This is JS-owned so only one complete layout exists in the DOM. */
var UNIT_V2_MQ = window.matchMedia(
  "(max-width:900px), " +
  "(max-width:1024px) and (max-height:600px)"
);

var unitSurface = {
  source: null,
  beamMap: null,
  beamHost: null,
  beamRetry: 0,
  beamReadyHandler: null,
  mode: null,
  viewportSyncPending: false
};

function setInert(el, on) {
  if (!el) return;
  if ("inert" in el) el.inert = !!on;
  if (on) el.setAttribute("aria-hidden", "true");
  else el.removeAttribute("aria-hidden");
}

function preciseGeo() {
  var g = project().geo || {};
  var rawLat = String(g.lat == null ? "" : g.lat).trim();
  var rawLng = String(g.lng == null ? "" : g.lng).trim();
  var lat = Number(g.lat);
  var lng = Number(g.lng);
  var valid = rawLat !== "" && rawLng !== "" &&
    isFinite(lat) && isFinite(lng) &&
    Math.abs(lat) <= 90 && Math.abs(lng) <= 180 &&
    !(lat === 0 && lng === 0);

  return {
    ok: valid && g.confidence !== "city",
    lat: lat,
    lng: lng
  };
}

function unitBearing(u) {
  var key = dirKey(u.dir);
  return key && Object.prototype.hasOwnProperty.call(DIR_BEARING, key)
    ? DIR_BEARING[key]
    : null;
}

function beamPoint(bearing, radius) {
  var rad = bearing * Math.PI / 180;
  return {
    x: 50 + Math.sin(rad) * radius,
    y: 50 - Math.cos(rad) * radius
  };
}

function beamPath(bearing) {
  var left = beamPoint(bearing - 24, 44);
  var tip = beamPoint(bearing, 53);
  var right = beamPoint(bearing + 24, 44);

  return [
    "M 50 50",
    "L " + left.x.toFixed(2) + " " + left.y.toFixed(2),
    "Q " + tip.x.toFixed(2) + " " + tip.y.toFixed(2) +
      " " + right.x.toFixed(2) + " " + right.y.toFixed(2),
    "Z"
  ].join(" ");
}

function beamShapeMarkup(bearing, gradientId, centerFill) {
  var direction = bearing == null
    ? '<circle cx="50" cy="50" r="31" fill="none" stroke="#f3d98c" ' +
        'stroke-opacity=".58" stroke-width="1.4" stroke-dasharray="4 5"/>'
    : '<path d="' + beamPath(bearing) + '" fill="url(#' + gradientId + ')"/>';
  return direction + '<circle cx="50" cy="50" r="4.2" fill="' + centerFill + '" ' +
    'stroke="#f3d98c" stroke-width="1.4"/>';
}

function renderBeamScene(u) {
  var view = viewText(u) || dirLabel(u.dir);
  var bearing = unitBearing(u);

  return (
    '<figure class="nl-unit-beam' + (bearing == null ? ' is-direction-unknown' : '') +
      '" data-bearing="' + (bearing == null ? '' : bearing) + '">' +
      '<div class="nl-unit-beam__map" data-role="beam-map" ' +
        'role="img" aria-label="' +
        esc(t("unit_beam_title", { view: view })) + '"></div>' +
      '<svg class="nl-unit-beam__svg" viewBox="0 0 100 100" ' +
        'preserveAspectRatio="none" aria-hidden="true">' +
        '<defs>' +
          '<linearGradient id="nl-unit-beam-gold" x1="0" y1="1" x2="0" y2="0">' +
            '<stop offset="0" stop-color="#c9a34f" stop-opacity=".86"/>' +
            '<stop offset="1" stop-color="#f4df9d" stop-opacity=".18"/>' +
          '</linearGradient>' +
        '</defs>' +
        beamShapeMarkup(bearing, "nl-unit-beam-gold", "#1b1a17") +
      '</svg>' +
      '<figcaption>' +
        '<strong>' + esc(t("unit_beam_title", { view: view })) + '</strong>' +
        '<span>' + esc(t("unit_beam_note")) + '</span>' +
      '</figcaption>' +
    '</figure>'
  );
}

function destroyBeamMap() {
  if (unitSurface.beamRetry) clearTimeout(unitSurface.beamRetry);
  if (unitSurface.beamReadyHandler) {
    document.removeEventListener("nlpjx:map", unitSurface.beamReadyHandler);
  }
  if (unitSurface.beamMap) {
    try { unitSurface.beamMap.remove(); } catch (e) {}
  }

  unitSurface.beamMap = null;
  unitSurface.beamHost = null;
  unitSurface.beamRetry = 0;
  unitSurface.beamReadyHandler = null;
}

function restoreMapAttributionTabbing(scope) {
  if (!scope) return;
  scope.querySelectorAll(
    ".mapboxgl-ctrl-attrib a, .mapboxgl-ctrl-logo, .mapboxgl-ctrl-attrib-button"
  ).forEach(function (link) {
    if (link.getAttribute("tabindex") === "-1") link.removeAttribute("tabindex");
  });
}

function mountBeamScene(scope) {
  destroyBeamMap();

  var host = scope && scope.querySelector('[data-role="beam-map"]');
  var geo = preciseGeo();
  var figure = host && host.closest(".nl-unit-beam");

  if (!host || !figure) return;

  /* A city centroid is suitable for an area map, not for a truthful window. */
  if (!geo.ok || !SR.config.mapbox_token) {
    figure.classList.add("is-schematic");
    return;
  }

  /* The engine and the deferred map library race on cold/deep-linked loads.
     Keep the current host pending for a bounded four seconds instead of
     permanently mislabelling a valid map as schematic. No DOM observer and no
     stale-host mount: every retry verifies both identity and connectivity. */
  if (!window.mapboxgl) {
    if (!unitV2Enabled()) {
      figure.classList.add("is-schematic");
      return;
    }
    var attempts = 0;
    unitSurface.beamHost = host;
    figure.classList.add("is-map-pending");

    var retry = function () {
      if (unitSurface.beamHost !== host || !document.contains(host)) return;
      if (window.mapboxgl) {
        mountBeamScene(scope);
        return;
      }
      attempts += 1;
      if (attempts >= 40) {
        figure.classList.remove("is-map-pending");
        figure.classList.add("is-schematic");
        unitSurface.beamRetry = 0;
        return;
      }
      unitSurface.beamRetry = setTimeout(retry, 100);
    };

    unitSurface.beamReadyHandler = function () {
      if (unitSurface.beamHost === host && document.contains(host) && window.mapboxgl) {
        mountBeamScene(scope);
      }
    };
    document.addEventListener("nlpjx:map", unitSurface.beamReadyHandler, { once: true });
    unitSurface.beamRetry = setTimeout(retry, 100);
    return;
  }

  try {
    window.mapboxgl.accessToken = SR.config.mapbox_token;

    var map = new window.mapboxgl.Map({
      container: host,
      style: figure.classList.contains("nl-unit-beam--v2")
        ? "mapbox://styles/mapbox/dark-v11"
        : "mapbox://styles/mapbox/light-v11",
      center: [geo.lng, geo.lat],
      zoom: 15.4,
      pitch: 0,
      bearing: 0,
      interactive: false,
      attributionControl: true
    });

    unitSurface.beamMap = map;
    unitSurface.beamHost = host;

    map.once("load", function () {
      if (unitSurface.beamMap !== map) return;
      figure.classList.remove("is-map-pending", "is-schematic");
      figure.classList.add("is-map-ready");
      try { map.resize(); } catch (e) {}
      if (unitV2Enabled()) restoreMapAttributionTabbing(figure);
    });

    map.once("error", function () {
      if (unitSurface.beamMap === map) {
        figure.classList.add("is-schematic");
      }
    });
  } catch (e) {
    figure.classList.add("is-schematic");
  }
}

function unitFactsMarkup(u) {
  return (
    '<dl class="nl-unit-facts">' +
      '<div><dt>' + esc(t("panel_floor")) + '</dt><dd>' + esc(u.floor) + '</dd></div>' +
      '<div><dt>' + esc(t("panel_rooms")) + '</dt><dd>' + esc(u.rooms) + '</dd></div>' +
      '<div><dt>' + esc(t("panel_sqm")) + '</dt><dd>' +
        esc(u.sqm + " " + t("sqm_unit")) + '</dd></div>' +
      '<div><dt>' + esc(t("panel_balcony")) + '</dt><dd>' +
        esc(u.balcony ? u.balcony + " " + t("sqm_unit") : "–") +
      '</dd></div>' +
    '</dl>'
  );
}

function unitDoorsMarkup(u) {
  var view = viewText(u) || dirLabel(u.dir);

  return (
    '<nav class="nl-unit-doors" aria-label="' + esc(t("unit_tools_aria")) + '">' +
      '<button type="button" data-act="unit-tool" data-tool="plan">' +
        esc(t("unit_door_plan")) +
      '</button>' +
      '<button type="button" data-act="unit-tool" data-tool="view">' +
        esc(t("unit_door_view", { view: view })) +
      '</button>' +
      '<button type="button" data-act="unit-tool" data-tool="tour">' +
        esc(t("unit_door_tour")) +
      '</button>' +
      (SR.config.studio !== "off"
        ? '<button type="button" data-act="unit-tool" data-tool="studio">' +
            esc(t("unit_door_studio")) +
          '</button>'
        : "") +
    '</nav>'
  );
}

function unitQuickActionsMarkup(u) {
  var fav = state.favs.indexOf(u.id) >= 0;
  var cmp = state.compare.indexOf(u.id) >= 0;

  return (
    '<div class="nl-unit-quick" role="group" aria-label="' +
      esc(t("unit_quick_actions")) + '">' +
      '<button type="button" data-act="fav" data-id="' + esc(u.id) + '" ' +
        'aria-pressed="' + (fav ? "true" : "false") + '">' +
        esc(fav ? t("btn_saved") : t("btn_save")) +
      '</button>' +
      '<button type="button" data-act="compare" data-id="' + esc(u.id) + '" ' +
        'aria-pressed="' + (cmp ? "true" : "false") + '">' +
        esc(cmp ? t("btn_compared") : t("btn_compare")) +
      '</button>' +
      '<button type="button" data-act="share" data-id="' + esc(u.id) + '">' +
        esc(t("btn_share")) +
      '</button>' +
      '<a href="' + esc(waShareUrl(u)) + '" target="_blank" rel="noopener">' +
        esc(t("btn_wa_share")) +
      '</a>' +
    '</div>'
  );
}

/* v2 never falls back to CMS-authored free text for directional chrome. A
   project may still carry a Hebrew `view` string, so non-HE locales derive a
   truthful, translated description from the normalized compass enum. */
function unitV2Direction(u) {
  var key = dirKey(u.dir);
  return key ? t("dir_" + key) : t("unit_direction_unknown");
}

function unitV2Label(u) {
  var raw = String(u.label == null ? "" : u.label);
  return state.lang === "he"
    ? raw
    : t("unit_v2_marker", { floor: u.floor });
}

function unitDisplayLabel(u) {
  return unitV2Enabled() ? unitV2Label(u) : u.label;
}

function unitV2View(u) {
  if (u.view_key) {
    var translated = t(u.view_key);
    if (
      translated && translated !== u.view_key &&
      (state.lang === "he" || !/[\u0590-\u05ff]/.test(translated))
    ) return translated;
  }
  return unitV2Direction(u);
}

function renderBeamSceneV2(u) {
  var view = unitV2View(u);
  var bearing = unitBearing(u);
  /* Keep the compact caption opposite the cone so the directional evidence is
     never hidden by its own call-to-action. South-facing cones get a top
     caption; north/east/west and unknown states use the bottom edge. */
  var captionClass = bearing != null && bearing > 90 && bearing < 270
    ? " is-caption-top"
    : " is-caption-bottom";

  return (
    '<figure class="nl-unit-beam nl-unit-beam--v2' +
      (bearing == null ? ' is-direction-unknown' : '') + captionClass +
      '" data-bearing="' +
      (bearing == null ? '' : bearing) + '">' +
      '<div class="nl-unit-beam__map" data-role="beam-map" role="img" ' +
        'aria-label="' + esc(t("unit_beam_title", { view: view })) + '"></div>' +
      '<svg class="nl-unit-beam__svg" viewBox="0 0 100 100" ' +
        'preserveAspectRatio="none" aria-hidden="true">' +
        '<defs>' +
          '<linearGradient id="nl-unit-beam-gold" x1="0" y1="1" x2="0" y2="0">' +
            '<stop offset="0" stop-color="#c9a34f" stop-opacity=".92"/>' +
            '<stop offset="1" stop-color="#f4df9d" stop-opacity=".12"/>' +
          '</linearGradient>' +
        '</defs>' +
        beamShapeMarkup(bearing, "nl-unit-beam-gold", "#11130f") +
      '</svg>' +
      '<figcaption>' +
        '<button class="nl-unit-beam__open" type="button" data-act="unit-tool" ' +
          'data-tool="area" aria-label="' + esc(t("unit_area_open_aria")) + '">' +
           '<strong>' + esc(t("unit_beam_title", { view: view })) + '</strong>' +
           '<span>' + esc(t("unit_beam_open_short")) + '</span>' +
         '</button>' +
      '</figcaption>' +
    '</figure>'
  );
}

function unitV2FactsMarkup(u) {
  var fav = state.favs.indexOf(u.id) >= 0;

  return (
    '<section class="nl-unit-journey__facts" aria-labelledby="nl-selected-unit-title">' +
      '<div class="nl-unit-journey__identity">' +
        '<span class="nl-unit-summary__status">' + esc(statusLabel(u.status)) + '</span>' +
        '<h3 id="nl-selected-unit-title">' +
          esc(t("unit_v2_identity", {
            rooms: u.rooms,
            floor: u.floor,
            direction: unitV2Direction(u)
          })) +
        '</h3>' +
      '</div>' +
      '<dl class="nl-unit-facts">' +
        '<div><dt>' + esc(t("panel_floor")) + '</dt><dd>' + esc(u.floor) + '</dd></div>' +
        '<div><dt>' + esc(t("panel_rooms")) + '</dt><dd>' + esc(u.rooms) + '</dd></div>' +
        '<div><dt>' + esc(t("panel_sqm")) + '</dt><dd>' +
          esc(u.sqm + " " + t("sqm_unit")) + '</dd></div>' +
        '<div><dt>' + esc(t("panel_balcony")) + '</dt><dd>' +
          esc(u.balcony ? u.balcony + " " + t("sqm_unit") : "–") + '</dd></div>' +
      '</dl>' +
      '<div class="nl-unit-quick" role="group" aria-label="' +
        esc(t("unit_quick_actions_v2")) + '">' +
        '<button type="button" data-act="fav" data-id="' + esc(u.id) + '" ' +
          'aria-pressed="' + (fav ? "true" : "false") + '">' +
          svg("heart", 17) + esc(fav ? t("btn_saved") : t("btn_save")) +
        '</button>' +
        '<button type="button" data-act="share" data-id="' + esc(u.id) + '">' +
          svg("share", 17) + esc(t("btn_share")) +
        '</button>' +
        '<a href="' + esc(waShareUrl(u)) + '" target="_blank" rel="noopener">' +
          svg("wa", 17) + esc(t("btn_wa_share")) +
        '</a>' +
        '<button type="button" data-act="unit-tool" data-tool="compare">' +
          svg("scale", 17) + esc(t("unit_compare_open")) +
        '</button>' +
      '</div>' +
      '<button class="nl-unit-contact" type="button" data-act="unit-tool" ' +
        'data-tool="contact">' + esc(t("unit_contact_cta")) + '</button>' +
    '</section>'
  );
}

function unitV2DoorsMarkup(u) {
  var view = unitV2View(u);
  var doors = [
    ["plan", "unit_door_plan", "grid"],
    ["view", "unit_door_view", "eye"],
    ["tour", "unit_door_tour", "play"],
    ["studio", "unit_door_studio", "cube"]
  ].filter(function (door) {
    return door[0] !== "studio" || SR.config.studio !== "off";
  });

  return (
    '<nav class="nl-unit-journey__doors nl-unit-doors" aria-label="' +
      esc(t("unit_tools_aria")) + '">' +
      doors.map(function (door) {
        var copy = door[0] === "view"
          ? t(door[1], { view: view })
          : t(door[1]);
        var shortCopy = t(door[1] + "_short");
        return (
          '<button class="nl-unit-door nl-unit-door--' + door[0] + '" type="button" ' +
            'data-act="unit-tool" data-tool="' + door[0] + '">' +
            '<span class="nl-unit-door__icon" aria-hidden="true">' + svg(door[2], 22) + '</span>' +
            '<span class="nl-unit-door__copy nl-unit-door__copy--long">' + esc(copy) + '</span>' +
            '<span class="nl-unit-door__copy nl-unit-door__copy--short">' + esc(shortCopy) + '</span>' +
          '</button>'
        );
      }).join("") +
    '</nav>'
  );
}

function unitV2ScreenMarkup(u) {
  return (
    '<header class="nl-unit-journey__head">' +
      '<button class="nl-unit-summary__back" type="button" data-act="unit-back">' +
        esc(t("unit_back_building")) +
      '</button>' +
      '<p><strong>' + esc(t("unit_selected")) + '</strong><span>' +
        esc(t("unit_v2_instruction")) + '</span></p>' +
    '</header>' +
    '<section class="nl-unit-journey__beam" aria-label="' +
      esc(t("unit_beam_region")) + '">' + renderBeamSceneV2(u) + '</section>' +
    unitV2FactsMarkup(u) +
    unitV2DoorsMarkup(u)
  );
}

function unitSummaryMarkup(u, mode) {
  return (
    '<div class="nl-unit-summary nl-unit-summary--' + esc(mode) + '">' +
      '<header class="nl-unit-summary__head">' +
        '<button class="nl-unit-summary__back" type="button" data-act="unit-back">' +
          esc(t("unit_back_building")) +
        '</button>' +
        '<div>' +
          '<span>' + esc(t("unit_selected")) + '</span>' +
          '<h3 id="nl-selected-unit-title">' +
            esc(roomsLabel(u.rooms) + " · " + unitDisplayLabel(u)) +
          '</h3>' +
        '</div>' +
        '<span class="nl-unit-summary__status">' +
          esc(statusLabel(u.status)) +
        '</span>' +
      '</header>' +
      renderBeamScene(u) +
      unitFactsMarkup(u) +
      unitDoorsMarkup(u) +
      unitQuickActionsMarkup(u) +
      '<button class="nl-unit-offer" type="button" ' +
        'data-act="scroll" data-id="inquiry">' +
        esc(t("unit_offer")) +
      '</button>' +
    '</div>'
  );
}

function unitV2TopOffset() {
  var max = 0;
  ["#wpadminbar", ".nlptop", ".nl-header", "#nl-secnav"].forEach(function (selector) {
    var el = document.querySelector(selector);
    if (!el) return;
    var cs = window.getComputedStyle(el);
    var rect = el.getBoundingClientRect();
    if (cs.position === "fixed" && rect.top <= 2) {
      max = Math.max(max, rect.bottom);
    } else if (cs.position === "sticky") {
      var stickyTop = parseFloat(cs.top);
      if (!isFinite(stickyTop)) stickyTop = max;
      max = Math.max(max, stickyTop + rect.height);
    }
  });
  return Math.max(0, max) + 8;
}

function alignUnitV2Theater(instant, singlePass) {
  var theaterEl = ROOT.querySelector(".nl-theater");
  if (!theaterEl) return;
  var alignmentToken = (Number(theaterEl.dataset.nlAlignToken) || 0) + 1;
  theaterEl.dataset.nlAlignToken = String(alignmentToken);

  function snap() {
    if (!document.contains(theaterEl) ||
        Number(theaterEl.dataset.nlAlignToken) !== alignmentToken) return;
    var offset = unitV2TopOffset();
    theaterEl.style.setProperty("--nl-unit-v2-top", offset + "px");
    var top = Math.max(
      0,
      theaterEl.getBoundingClientRect().top + window.pageYOffset - offset
    );
    /* Deterministic visibility is more valuable than a scroll animation here.
       A second layout pass can move normal-flow content during rotation. */
    window.scrollTo({ top: top, left: 0, behavior: "auto" });
  }

  snap();
  if (singlePass) return;
  requestAnimationFrame(function () {
    snap();
    requestAnimationFrame(snap);
  });
  window.setTimeout(snap, instant ? 80 : 140);
}

function renderUnitScreenV2(u, options) {
  options = options || {};

  var mobile = UNIT_V2_MQ.matches;
  var mode = mobile ? "mobile" : "desktop";
  var theaterEl = ROOT.querySelector(".nl-theater");
  var screen = document.getElementById("nl-unit-screen");
  var panelEl = document.getElementById("nl-panel");
  var panelBodyEl = document.getElementById("nl-panel-body");

  if (!u || !theaterEl || !screen || !panelEl || !panelBodyEl) return;

  /* Breakpoint changes replace one complete subtree. The inactive v1 panel is
     emptied first, so IDs such as nl-selected-unit-title can never coexist. */
  destroyBeamMap();
  theaterEl.classList.add("nl-unit-v2-transitioning");
  theaterEl.style.setProperty("--nl-unit-v2-top", unitV2TopOffset() + "px");
  panelBodyEl.innerHTML = panelEmpty();
  panelEl.classList.remove("is-open", "nl-panel--unit-summary");
  panelEl.hidden = true;
  setInert(panelEl, true);

  screen.hidden = true;
  screen.innerHTML = "";
  screen.className = "nl-unit-screen nl-unit-screen--v2";
  screen.setAttribute("data-mode", mode);
  screen.setAttribute("role", "region");
  screen.setAttribute("aria-labelledby", "nl-selected-unit-title");
  screen.innerHTML = unitV2ScreenMarkup(u);
  screen.hidden = false;
  setInert(screen, false);

  theaterEl.classList.remove(
    "nl-theater--unit-selected",
    "nl-theater--unit-v2-mobile",
    "nl-theater--unit-v2-desktop"
  );
  theaterEl.classList.add(
    "nl-theater--unit-v2",
    "nl-theater--unit-v2-" + mode
  );
  document.body.classList.add("nl-unit-v2-active", "nl-unit-journey-active");
  unitSurface.mode = mode;

  mountBeamScene(screen);
  requestAnimationFrame(function () {
    if (options.align) {
      alignUnitV2Theater(!!options.instant);
      requestAnimationFrame(function () {
        theaterEl.classList.remove("nl-unit-v2-transitioning");
      });
    } else {
      theaterEl.classList.remove("nl-unit-v2-transitioning");
    }
  });

  if (options.focus) {
    requestAnimationFrame(function () {
      var back = screen.querySelector('[data-act="unit-back"]');
      if (back) back.focus({ preventScroll: true });
    });
  }
}

function clearUnitScreenV2() {
  var theaterEl = ROOT.querySelector(".nl-theater");
  var screen = document.getElementById("nl-unit-screen");
  var panelEl = document.getElementById("nl-panel");
  var panelBodyEl = document.getElementById("nl-panel-body");

  destroyBeamMap();
  unitSurface.mode = null;
  unitSurface.viewportSyncPending = false;
  document.body.classList.remove("nl-unit-v2-active", "nl-unit-journey-active");

  if (theaterEl) {
    theaterEl.classList.remove(
      "nl-theater--unit-selected",
      "nl-theater--unit-v2",
      "nl-theater--unit-v2-mobile",
      "nl-theater--unit-v2-desktop",
      "nl-unit-v2-transitioning"
    );
    theaterEl.style.removeProperty("--nl-unit-v2-top");
  }

  if (screen) {
    screen.hidden = true;
    screen.innerHTML = "";
    screen.className = "nl-unit-screen";
    screen.removeAttribute("data-mode");
    screen.removeAttribute("role");
    screen.removeAttribute("aria-labelledby");
    setInert(screen, true);
  }

  /* A v2 page never revives the legacy selected-unit panel. The building and
     its hotspots remain the sole pre-selection surface. */
  if (panelEl) {
    panelEl.classList.remove("is-open", "nl-panel--unit-summary");
    panelEl.hidden = true;
    setInert(panelEl, true);
  }
  if (panelBodyEl) panelBodyEl.innerHTML = panelEmpty();
}

function renderUnitScreen(u, options) {
  if (unitV2Enabled()) {
    renderUnitScreenV2(u, options);
    return;
  }
  options = options || {};

  var mobile = UNIT_MQ.matches;
  var theaterEl = ROOT.querySelector(".nl-theater");
  var screen = document.getElementById("nl-unit-screen");
  var panelEl = document.getElementById("nl-panel");
  var panelBodyEl = document.getElementById("nl-panel-body");
  var host;

  if (!u || !theaterEl || !screen || !panelEl || !panelBodyEl) return;

  destroyBeamMap();

  if (mobile) {
    theaterEl.classList.add("nl-theater--unit-selected");

    screen.innerHTML = unitSummaryMarkup(u, "screen");
    screen.hidden = false;
    setInert(screen, false);

    panelEl.hidden = true;
    panelEl.classList.remove("is-open", "nl-panel--unit-summary");
    setInert(panelEl, true);

    host = screen;
  } else {
    theaterEl.classList.remove("nl-theater--unit-selected");

    screen.hidden = true;
    screen.innerHTML = "";
    setInert(screen, true);

    panelBodyEl.innerHTML = unitSummaryMarkup(u, "panel");
    panelEl.hidden = false;
    panelEl.classList.add("is-open", "nl-panel--unit-summary");
    setInert(panelEl, false);

    host = panelBodyEl;
  }

  mountBeamScene(host);

  if (mobile && options.scroll) {
    requestAnimationFrame(function () {
      theaterEl.scrollIntoView({
        block: "start",
        behavior: window.matchMedia("(prefers-reduced-motion:reduce)").matches
          ? "auto"
          : "smooth"
      });
    });
  }

  if (options.focus) {
    requestAnimationFrame(function () {
      var back = host.querySelector('[data-act="unit-back"]');
      if (back) back.focus({ preventScroll: true });
    });
  }
}

function clearUnitScreen() {
  if (unitV2Enabled()) {
    clearUnitScreenV2();
    return;
  }
  var theaterEl = ROOT.querySelector(".nl-theater");
  var screen = document.getElementById("nl-unit-screen");
  var panelEl = document.getElementById("nl-panel");
  var panelBodyEl = document.getElementById("nl-panel-body");

  destroyBeamMap();

  if (theaterEl) theaterEl.classList.remove("nl-theater--unit-selected");

  if (screen) {
    screen.hidden = true;
    screen.innerHTML = "";
    setInert(screen, true);
  }

  if (panelEl) {
    panelEl.classList.remove("is-open", "nl-panel--unit-summary");
    panelEl.hidden = UNIT_MQ.matches;
    setInert(panelEl, true);
  }

  if (panelBodyEl) panelBodyEl.innerHTML = panelEmpty();
}

function syncUnitBreakpoint() {
  if (unitV2Enabled()) return;
  var selected = unit(state.unitId);
  if (selected) renderUnitScreen(selected, { focus: false, scroll: false });
  else clearUnitScreen();
}

function syncUnitV2Breakpoint(options) {
  if (!unitV2Enabled()) return;
  options = options || {};
  unitSurface.viewportSyncPending = false;
  var selected = unit(state.unitId);
  if (selected) {
    var active = document.activeElement;
    var oldScreen = document.getElementById("nl-unit-screen");
    var focusTool = oldScreen && oldScreen.contains(active) && active.dataset
      ? active.dataset.tool
      : "";
    var focusAct = oldScreen && oldScreen.contains(active) && active.dataset
      ? active.dataset.act
      : "";
    var focusId = oldScreen && oldScreen.contains(active) && active.dataset
      ? active.dataset.id
      : "";

    renderUnitScreenV2(selected, {
      focus: false,
      align: options.align !== false,
      instant: true
    });

    if (focusTool || focusAct) {
      requestAnimationFrame(function () {
        var screen = document.getElementById("nl-unit-screen");
        var replacement = focusTool
          ? screen && screen.querySelector('[data-tool="' + cssesc(focusTool) + '"]')
          : screen && screen.querySelector(
              '[data-act="' + cssesc(focusAct) + '"]' +
              (focusId ? '[data-id="' + cssesc(focusId) + '"]' : "")
            );
        if (replacement) replacement.focus({ preventScroll: true });
      });
    }
  }
  else clearUnitScreenV2();
}

if (UNIT_MQ.addEventListener) {
  UNIT_MQ.addEventListener("change", syncUnitBreakpoint);
} else {
  UNIT_MQ.addListener(syncUnitBreakpoint);
}

var unitV2ViewportTimer = 0;
function unitV2ExpectedMode() {
  return UNIT_V2_MQ.matches ? "mobile" : "desktop";
}

function unitV2ViewportStateMismatch() {
  var expected = unitV2ExpectedMode();
  var screen = document.getElementById("nl-unit-screen");
  var theaterEl = ROOT.querySelector(".nl-theater--unit-v2");
  return !screen || screen.hidden || screen.getAttribute("data-mode") !== expected ||
    unitSurface.mode !== expected || !theaterEl ||
    !theaterEl.classList.contains("nl-theater--unit-v2-" + expected);
}

function handleUnitV2BreakpointChange() {
  if (!unitV2Enabled() || !state.unitId) return;
  if (state.tool) {
    unitSurface.viewportSyncPending = true;
    return;
  }
  syncUnitV2Breakpoint();
}

if (UNIT_V2_MQ.addEventListener) {
  UNIT_V2_MQ.addEventListener("change", handleUnitV2BreakpointChange);
} else {
  UNIT_V2_MQ.addListener(handleUnitV2BreakpointChange);
}

function scheduleUnitV2ViewportSync() {
  if (!unitV2Enabled() || !state.unitId) return;
  if (state.tool) {
    unitSurface.viewportSyncPending = true;
    clearTimeout(unitV2ViewportTimer);
    unitV2ViewportTimer = 0;
    return;
  }
  /* Mobile browsers fire resize/visualViewport for URL-bar collapse, pinch
     zoom and the keyboard - many times during one ordinary reading scroll.
     A re-render here force-aligns the theater (window.scrollTo), so acting
     on that noise teleports a reader back up on every scroll gesture. Only
     a genuine rendered-mode mismatch (rotation, split-screen) may proceed;
     plain breakpoint crossings are already owned by the UNIT_V2_MQ change
     listener. */
  if (!unitV2ViewportStateMismatch()) {
    clearTimeout(unitV2ViewportTimer);
    unitV2ViewportTimer = 0;
    return;
  }
  var theaterEl = ROOT.querySelector(".nl-theater--unit-v2");
  if (theaterEl) theaterEl.classList.add("nl-unit-v2-transitioning");
  clearTimeout(unitV2ViewportTimer);
  unitV2ViewportTimer = setTimeout(function () {
    unitV2ViewportTimer = 0;
    if (unitV2Enabled() && state.unitId && state.tool) {
      unitSurface.viewportSyncPending = true;
    } else if (unitV2Enabled() && state.unitId &&
               unitV2ViewportStateMismatch()) {
      syncUnitV2Breakpoint();
    } else {
      var settled = ROOT.querySelector(".nl-theater--unit-v2");
      if (settled) settled.classList.remove("nl-unit-v2-transitioning");
    }
  }, 48);
}

function flushUnitV2ViewportSyncAfterTool() {
  clearTimeout(unitV2ViewportTimer);
  unitV2ViewportTimer = 0;

  if (!unitV2Enabled() || !state.unitId) {
    unitSurface.viewportSyncPending = false;
    return false;
  }

  var needsSync = unitSurface.viewportSyncPending || unitV2ViewportStateMismatch();
  unitSurface.viewportSyncPending = false;
  if (!needsSync) return false;

  /* Replace the inactive scene subtree once, without touching URL/history.
     The close lifecycle aligns it after the transition frame has completed. */
  syncUnitV2Breakpoint({ align: false });
  return true;
}
window.addEventListener("resize", scheduleUnitV2ViewportSync, { passive: true });
window.addEventListener("orientationchange", scheduleUnitV2ViewportSync, { passive: true });
if (window.visualViewport) {
  window.visualViewport.addEventListener("resize", scheduleUnitV2ViewportSync, { passive: true });
}

/*
 * Integration seam required in theater():
 *   '<section class="nl-unit-screen" id="nl-unit-screen" hidden></section>'
 * Place it as a sibling immediately after .nl-stagewrap and before the dock.
 *
 * selectUnit(), closePanel(), toggleFav() and toggleCompare() replacement
 * excerpts live in integration-diff-guide.md so this fragment remains focused
 * on one responsibility: rendering and owning the selected-unit surface.
 */

  /* ---- audit fragment: body-level fullscreen tools ---- */
var unitTool = {
  dialog: null,
  cleanup: null,
  returnFocus: null,
  returnKind: null,
  historyMarker: null,
  pendingFocusRestore: true,
  scrollY: 0,
  closing: false,
  fromHistory: false
};

function unitToolFocusable(dialog) {
  return Array.prototype.slice.call(dialog.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), ' +
    'select:not([disabled]), [tabindex]:not([tabindex="-1"])'
  )).filter(function (el) {
    return !el.hidden && el.getAttribute("aria-hidden") !== "true" &&
      el.getClientRects().length > 0;
  });
}

function ensureUnitToolDialog() {
  if (unitTool.dialog) return unitTool.dialog;

  var dialog = document.createElement("dialog");
  dialog.id = "nl-unit-tool";
  dialog.className = "nl-unit-tool";
  document.body.appendChild(dialog);

  dialog.addEventListener("cancel", function (event) {
    event.preventDefault();
    closeUnitTool(true, false);
  });

  dialog.addEventListener("click", function (event) {
    var button = event.target.closest('[data-act="unit-tool-back"]');
    if (button) closeUnitTool(true, false);
  });

  /* Native dialog.close() can also be called by browser integrations or
     future tools. It must never leave ROOT inert or the page scroll-locked. */
  dialog.addEventListener("close", function () {
    if (state.tool) closeUnitTool(true, false);
  });

  dialog.addEventListener("keydown", function (event) {
    if (!unitV2Enabled() || !state.tool) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closeUnitTool(true, false);
      return;
    }
    if (event.key !== "Tab") return;

    var focusable = unitToolFocusable(dialog);
    if (!focusable.length) {
      event.preventDefault();
      dialog.focus({ preventScroll: true });
      return;
    }

    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    var active = document.activeElement;
    if (!dialog.contains(active)) {
      event.preventDefault();
      (event.shiftKey ? last : first).focus({ preventScroll: true });
    } else if (event.shiftKey && active === first) {
      event.preventDefault();
      last.focus({ preventScroll: true });
    } else if (!event.shiftKey && active === last) {
      event.preventDefault();
      first.focus({ preventScroll: true });
    }
  });

  unitTool.dialog = dialog;
  return dialog;
}

function toolTitle(kind) {
  if (kind === "plan") return t("tab_plan");
  if (kind === "view") return t("tab_view");
  if (kind === "tour") return t("tab_tour");
  if (kind === "area") return t("unit_area_title");
  if (kind === "contact") return t("unit_contact_title");
  if (kind === "compare") return t("unit_compare_title");
  if (kind === "studio") return t("unit_studio_title");
  return t("unit_selected");
}

function designerToolUrl(u) {
  var configured = u.designer_url || project().designer_url ||
    SR.config.designer_url || SR.config.studio_url || "";
  var base = safeHttpUrl(configured);

  if (!base) {
    try {
      base = new URL("/tour/designer/", SR.config.home_url || location.origin).href;
    } catch (e) {
      base = "";
    }
  }

  if (!base) return "";
  try {
    var url = new URL(base);
    url.searchParams.set("project", state.projectKey);
    url.searchParams.set("unit", u.id);
    url.searchParams.set("lang", state.lang);
    url.searchParams.set("embed", "1");
    return safeHttpUrl(url.href);
  } catch (e2) {
    return safeHttpUrl(base);
  }
}

function unitAreaExternalUrl() {
  var geo = preciseGeo();
  if (!geo.ok) return "";
  return "https://www.google.com/maps/search/?api=1&query=" +
    encodeURIComponent(geo.lat + "," + geo.lng);
}

function unitV2CompareHasValue(value) {
  return value !== null && value !== undefined && String(value).trim() !== "";
}

function unitV2CompareOptionLabel(u) {
  var label = unitV2Label(u) || t("unit_v2_marker", { floor: u.floor });
  return t("unit_compare_option", {
    label: label,
    rooms: u.rooms,
    floor: u.floor
  });
}

function unitV2CompareOptionsMarkup(selectedId, selectedIds, optional) {
  var blank = optional
    ? '<option value="">' + esc(t("unit_compare_optional_empty")) + '</option>'
    : "";
  return blank + units().map(function (u) {
    var id = String(u.id);
    var selected = id === String(selectedId || "");
    var disabled = !selected && selectedIds.indexOf(id) >= 0;
    return '<option value="' + esc(id) + '"' +
      (selected ? ' selected' : '') +
      (disabled ? ' disabled' : '') + '>' +
      esc(unitV2CompareOptionLabel(u)) + '</option>';
  }).join("");
}

function unitV2CompareFact(u, key) {
  var raw;
  var value;

  if (key === "floor") {
    raw = u.floor;
    value = unitV2CompareHasValue(raw) ? String(raw) : t("unit_compare_not_provided");
  } else if (key === "rooms") {
    raw = u.rooms;
    value = unitV2CompareHasValue(raw)
      ? roomsLabel(raw)
      : t("unit_compare_not_provided");
  } else if (key === "sqm") {
    raw = u.sqm;
    value = unitV2CompareHasValue(raw)
      ? String(raw) + " " + t("sqm_unit")
      : t("unit_compare_not_provided");
  } else if (key === "balcony") {
    raw = u.balcony;
    value = unitV2CompareHasValue(raw)
      ? String(raw) + " " + t("sqm_unit")
      : t("unit_compare_not_provided");
  } else {
    raw = u.status;
    value = unitV2CompareHasValue(raw)
      ? statusLabel(raw)
      : t("unit_compare_not_provided");
  }

  return {
    raw: unitV2CompareHasValue(raw) ? String(raw).trim().toLowerCase() : "__missing__",
    value: value
  };
}

function unitV2CompareSummaryMarkup(ids) {
  var compared = ids.map(unit).filter(Boolean).slice(0, 3);
  var fields = [
    ["floor", t("panel_floor")],
    ["rooms", t("panel_rooms")],
    ["sqm", t("panel_sqm")],
    ["balcony", t("panel_balcony")],
    ["status", t("unit_compare_status")]
  ];
  var count = Math.max(1, compared.length);
  var head = '<div class="nl-unit-compare-row nl-unit-compare-row--head" role="row">' +
    '<span role="columnheader">' + esc(t("unit_compare_field")) + '</span>' +
    compared.map(function (u) {
      return '<strong role="columnheader">' + esc(unitV2Label(u)) + '</strong>';
    }).join("") + '</div>';

  var rows = fields.map(function (field) {
    var facts = compared.map(function (u) { return unitV2CompareFact(u, field[0]); });
    var values = facts.map(function (fact) { return fact.raw; });
    var different = values.length > 1 && values.some(function (value) {
      return value !== values[0];
    });
    return '<div class="nl-unit-compare-row' + (different ? ' is-different' : '') +
      '" role="row">' +
      '<span class="nl-unit-compare-row__label" role="rowheader">' +
        esc(field[1]) +
        (different
          ? '<small>' + esc(t("unit_compare_difference")) + '</small>'
          : "") +
      '</span>' +
      facts.map(function (fact) {
        return '<span class="nl-unit-compare-row__value" role="cell">' +
          esc(fact.value) + '</span>';
      }).join("") +
    '</div>';
  }).join("");

  return '<div class="nl-unit-compare-summary" data-role="compare-summary" ' +
    'role="table" aria-label="' + esc(t("unit_compare_summary_aria")) + '" ' +
    'aria-live="polite" style="--nl-unit-compare-count:' + count + '">' +
    head + rows + '</div>';
}

function unitV2CompareToolMarkup(current) {
  var ids = prepareUnitV2Compare(current);
  if (units().length < 2) {
    return '<div class="nl-unit-compare-tool" data-role="compare-tool">' +
      '<p class="nl-unit-compare-tool__empty">' +
        esc(t("unit_compare_unavailable")) + '</p></div>';
  }

  var slotLabels = [
    t("unit_compare_slot_current"),
    t("unit_compare_slot_second"),
    t("unit_compare_slot_third")
  ];
  var slots = slotLabels.map(function (label, index) {
    var selectedId = ids[index] || "";
    var inputId = "nl-unit-compare-slot-" + index;
    return '<label class="nl-unit-compare-slot" for="' + inputId + '">' +
      '<span>' + esc(label) + '</span>' +
      '<select id="' + inputId + '" data-compare-slot="' + index + '"' +
        (index === 0 ? ' disabled aria-disabled="true"' : '') + '>' +
        unitV2CompareOptionsMarkup(selectedId, ids, index === 2) +
      '</select></label>';
  }).join("");

  return '<div class="nl-unit-compare-tool" data-role="compare-tool">' +
    '<p class="nl-unit-compare-tool__intro">' + esc(t("unit_compare_intro")) + '</p>' +
    '<div class="nl-unit-compare-slots" role="group" aria-label="' +
      esc(t("unit_compare_slots_aria")) + '">' + slots + '</div>' +
    unitV2CompareSummaryMarkup(ids) +
  '</div>';
}

function mountUnitV2Compare(scope, current) {
  var root = scope.querySelector('[data-role="compare-tool"]');
  if (!root || units().length < 2) return function () {};

  var controller = new AbortController();
  var signal = controller.signal;

  function selectedIdsFromControls() {
    var ids = [String(current.id)];
    root.querySelectorAll("[data-compare-slot]").forEach(function (select, index) {
      if (index === 0) return;
      var id = String(select.value || "");
      if (id && unit(id) && ids.indexOf(id) < 0) ids.push(id);
    });
    if (ids.length < 2) {
      units().some(function (candidate) {
        var id = String(candidate.id);
        if (ids.indexOf(id) < 0) ids.push(id);
        return ids.length >= 2;
      });
    }
    return ids.slice(0, 3);
  }

  function renderSelection(ids) {
    saveUnitV2Compare(ids);
    root.querySelectorAll("[data-compare-slot]").forEach(function (select, index) {
      var selectedId = state.compare[index] || "";
      select.innerHTML = unitV2CompareOptionsMarkup(
        selectedId,
        state.compare,
        index === 2
      );
      select.value = selectedId;
    });
    var summary = root.querySelector('[data-role="compare-summary"]');
    if (summary) summary.outerHTML = unitV2CompareSummaryMarkup(state.compare);
  }

  root.querySelectorAll("[data-compare-slot]").forEach(function (select) {
    select.addEventListener("change", function () {
      renderSelection(selectedIdsFromControls());
    }, { signal: signal });
  });

  return function () { controller.abort(); };
}

function unitToolMarkupV2(kind, u) {
  var content = "";

  if (kind === "plan") {
    var plan = safeHttpUrl(u.plan);
    content = plan
      ? '<div class="nl-unit-plan-tool">' +
          '<div class="nl-unit-plan-tool__viewport" data-role="plan-viewport" ' +
            'tabindex="0" aria-label="' + esc(t("unit_plan_canvas_aria")) + '">' +
            '<img class="nl-unit-plan-tool__image" data-role="plan-image" ' +
              'src="' + esc(plan) + '" alt="' + esc(t("unit_plan_alt", {
                floor: u.floor,
                rooms: u.rooms
              })) + '" draggable="false">' +
          '</div>' +
          '<div class="nl-unit-plan-tool__controls" role="group" aria-label="' +
            esc(t("unit_plan_controls")) + '">' +
            '<button type="button" data-plan-zoom="out" aria-label="' +
              esc(t("unit_plan_zoom_out")) + '">−</button>' +
            '<button type="button" data-plan-zoom="reset">' +
              esc(t("unit_plan_reset")) + '</button>' +
            '<button type="button" data-plan-zoom="in" aria-label="' +
              esc(t("unit_plan_zoom_in")) + '">+</button>' +
          '</div>' +
          '<p class="nl-unit-plan-tool__hint">' + esc(t("unit_plan_hint")) + '</p>' +
        '</div>'
      : '<p class="nl-unit-tool__empty">' + esc(t("plan_coming")) + '</p>';
  }

  if (kind === "view") {
    content =
      '<div class="nl-window-tool">' +
        '<div class="nl-window-tool__map" data-role="window-map" tabindex="0" ' +
          'aria-label="' + esc(t("unit_window_canvas_aria")) + '"></div>' +
        '<p class="nl-window-tool__fallback" data-role="window-fallback" hidden></p>' +
        '<div class="nl-window-tool__controls">' +
          '<button type="button" data-turn="-30" aria-label="' +
            esc(t("winview_turn_left")) + '">↶</button>' +
          '<span>' + esc(t("floor_label", { n: u.floor })) +
            " · " + esc(unitV2Direction(u)) + '</span>' +
          '<button type="button" data-turn="30" aria-label="' +
            esc(t("winview_turn_right")) + '">↷</button>' +
        '</div>' +
        '<p class="nl-window-tool__note">' + esc(t("unit_window_hint")) + '</p>' +
      '</div>';
  }

  if (kind === "tour") {
    var tour = safeHttpUrl(u.tour_url || project().tour_url);
    content = tour
      ? '<div class="nl-unit-tool__tour nl-unit-tool__tour--fill">' +
          '<iframe src="' + esc(tour) + '" title="' + esc(t("tab_tour")) + '" ' +
            'allow="fullscreen; gyroscope; accelerometer" allowfullscreen></iframe>' +
          '<a href="' + esc(tour) + '" target="_blank" rel="noopener">' +
            esc(t("tour_open")) + '</a>' +
        '</div>'
      : '<div class="nl-unit-tool__tour nl-unit-tool__tour--fill">' +
          fpMarkup(u) +
        '</div>';
  }

  if (kind === "studio") {
    var designer = designerToolUrl(u);
    content = designer
      ? '<div class="nl-unit-tool__studio">' +
          '<iframe src="' + esc(designer) + '" title="' +
            esc(t("unit_studio_iframe_title")) + '" ' +
            'allow="fullscreen; clipboard-write" allowfullscreen></iframe>' +
          '<a href="' + esc(designer) + '" target="_blank" rel="noopener">' +
            esc(t("unit_studio_external")) + '</a>' +
        '</div>'
      : '<p class="nl-unit-tool__empty">' + esc(t("unit_studio_unavailable")) + '</p>';
  }

  if (kind === "area") {
    var external = unitAreaExternalUrl();
    content =
      '<div class="nl-unit-area-tool">' +
        '<div class="nl-unit-area-tool__map" data-role="area-map" tabindex="0" ' +
          'aria-label="' + esc(t("unit_area_map_aria")) + '"></div>' +
        '<p class="nl-unit-area-tool__fallback" data-role="area-fallback" hidden></p>' +
        '<div class="nl-unit-area-tool__copy"><strong>' +
          esc(t("unit_beam_title", { view: unitV2View(u) })) + '</strong><span>' +
          esc(t("unit_area_note")) + '</span></div>' +
        (external
          ? '<a class="nl-unit-area-tool__external" href="' + esc(external) +
              '" target="_blank" rel="noopener">' + esc(t("unit_area_external")) + '</a>'
          : "") +
      '</div>';
  }

  if (kind === "contact") {
    content =
      '<div class="nl-unit-contact-tool">' +
        '<p>' + esc(t("unit_contact_intro", {
          floor: u.floor,
          rooms: u.rooms,
          sqm: u.sqm
        })) + '</p>' +
        '<form class="nl-unit-contact-form" data-role="unit-contact-form" novalidate>' +
          '<label><span>' + esc(t("form_name")) + '</span>' +
            '<input name="name" autocomplete="name" required></label>' +
          '<label><span>' + esc(t("form_phone")) + '</span>' +
            '<input name="phone" inputmode="tel" autocomplete="tel"></label>' +
          '<label><span>' + esc(t("form_email")) + '</span>' +
            '<input name="email" type="email" inputmode="email" autocomplete="email"></label>' +
          '<label><span>' + esc(t("unit_contact_message")) + '</span>' +
            '<textarea name="message" rows="3"></textarea></label>' +
          '<label class="nl-unit-contact-form__consent">' +
            '<input name="consent" type="checkbox" required> <span>' +
              esc(t("form_consent")) + '</span></label>' +
          '<button type="submit">' + esc(t("unit_contact_submit")) + '</button>' +
          '<div class="nl-unit-contact-form__feedback" data-role="contact-feedback" ' +
            'role="status" aria-live="polite" hidden></div>' +
        '</form>' +
      '</div>';
  }

  if (kind === "compare") {
    content = unitV2CompareToolMarkup(u);
  }

  return (
    '<div class="nl-unit-tool__frame">' +
      '<header class="nl-unit-tool__head">' +
        '<button type="button" data-act="unit-tool-back">' +
          esc(t("unit_tool_back")) +
        '</button>' +
        '<h2 id="nl-unit-tool-title">' + esc(toolTitle(kind)) + '</h2>' +
      '</header>' +
      '<div class="nl-unit-tool__body">' + content + '</div>' +
    '</div>'
  );
}

function unitToolMarkup(kind, u) {
  if (unitV2Enabled()) return unitToolMarkupV2(kind, u);
  var content = "";

  if (kind === "plan") {
    var plan = safeHttpUrl(u.plan);
    content = plan
      ? '<figure class="nl-unit-tool__plan">' +
          '<img src="' + esc(plan) + '" alt="' + esc(t("tab_plan")) + '">' +
        '</figure>'
      : '<p class="nl-unit-tool__empty">' + esc(t("plan_coming")) + '</p>';
  }

  if (kind === "view") {
    content =
      '<div class="nl-window-tool">' +
        '<div class="nl-window-tool__map" data-role="window-map" tabindex="0" ' +
          'aria-label="' + esc(t("tab_view")) + '"></div>' +
        '<p class="nl-window-tool__fallback" data-role="window-fallback" hidden></p>' +
        '<div class="nl-window-tool__controls">' +
          '<button type="button" data-turn="-30" aria-label="' +
            esc(t("winview_turn_left")) + '">↶</button>' +
          '<span>' + esc(t("floor_label", { n: u.floor })) +
            " · " + esc(dirLabel(u.dir)) + '</span>' +
          '<button type="button" data-turn="30" aria-label="' +
            esc(t("winview_turn_right")) + '">↷</button>' +
        '</div>' +
      '</div>';
  }

  if (kind === "tour") {
    var tour = safeHttpUrl(u.tour_url || project().tour_url);

    content = tour
      ? '<div class="nl-unit-tool__tour">' +
          '<iframe src="' + esc(tour) + '" title="' + esc(t("tab_tour")) + '" ' +
            'allow="fullscreen; gyroscope; accelerometer" allowfullscreen></iframe>' +
          '<a href="' + esc(tour) + '" target="_blank" rel="noopener">' +
            esc(t("tour_open")) +
          '</a>' +
        '</div>'
      : fpMarkup(u);
  }

  return (
    '<div class="nl-unit-tool__frame">' +
      '<header class="nl-unit-tool__head">' +
        '<button type="button" data-act="unit-tool-back">' +
          esc(t("unit_tool_back")) +
        '</button>' +
        '<h2 id="nl-unit-tool-title">' + esc(toolTitle(kind)) + '</h2>' +
      '</header>' +
      '<div class="nl-unit-tool__body">' + content + '</div>' +
    '</div>'
  );
}

function mountPlanTool(scope) {
  var viewport = scope.querySelector('[data-role="plan-viewport"]');
  var image = scope.querySelector('[data-role="plan-image"]');
  if (!viewport || !image) return function () {};

  var controller = new AbortController();
  var signal = controller.signal;
  var scale = 1;
  var x = 0;
  var y = 0;
  var pointers = {};
  var dragX = 0;
  var dragY = 0;
  var pinchDistance = 0;
  var pinchScale = 1;

  viewport.style.touchAction = "none";

  function pointerValues() {
    return Object.keys(pointers).map(function (key) { return pointers[key]; });
  }

  function distance(a, b) {
    var dx = a.x - b.x;
    var dy = a.y - b.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  function apply() {
    image.style.transform = "translate3d(" + x.toFixed(1) + "px," +
      y.toFixed(1) + "px,0) scale(" + scale.toFixed(3) + ")";
  }

  function setScale(next) {
    scale = Math.max(1, Math.min(4, next));
    if (scale === 1) { x = 0; y = 0; }
    apply();
  }

  function reset() {
    scale = 1;
    x = 0;
    y = 0;
    apply();
  }

  viewport.addEventListener("pointerdown", function (event) {
    pointers[event.pointerId] = { x: event.clientX, y: event.clientY };
    var values = pointerValues();
    if (values.length === 1) {
      dragX = event.clientX;
      dragY = event.clientY;
    } else if (values.length === 2) {
      pinchDistance = distance(values[0], values[1]) || 1;
      pinchScale = scale;
    }
    try { viewport.setPointerCapture(event.pointerId); } catch (e) {}
    event.preventDefault();
  }, { signal: signal });

  viewport.addEventListener("pointermove", function (event) {
    if (!pointers[event.pointerId]) return;
    pointers[event.pointerId] = { x: event.clientX, y: event.clientY };
    var values = pointerValues();

    if (values.length >= 2) {
      setScale(pinchScale * (distance(values[0], values[1]) / pinchDistance));
    } else if (values.length === 1) {
      x += event.clientX - dragX;
      y += event.clientY - dragY;
      dragX = event.clientX;
      dragY = event.clientY;
      apply();
    }
    event.preventDefault();
  }, { signal: signal });

  function release(event) {
    delete pointers[event.pointerId];
    var values = pointerValues();
    if (values.length === 1) {
      dragX = values[0].x;
      dragY = values[0].y;
    }
    try { viewport.releasePointerCapture(event.pointerId); } catch (e) {}
  }

  viewport.addEventListener("pointerup", release, { signal: signal });
  viewport.addEventListener("pointercancel", release, { signal: signal });

  viewport.addEventListener("wheel", function (event) {
    event.preventDefault();
    setScale(scale + (event.deltaY < 0 ? 0.25 : -0.25));
  }, { passive: false, signal: signal });

  viewport.addEventListener("keydown", function (event) {
    var handled = true;
    if (event.key === "+" || event.key === "=") setScale(scale + 0.25);
    else if (event.key === "-") setScale(scale - 0.25);
    else if (event.key === "0" || event.key === "Home") reset();
    else if (event.key === "ArrowLeft") { x -= 24; apply(); }
    else if (event.key === "ArrowRight") { x += 24; apply(); }
    else if (event.key === "ArrowUp") { y -= 24; apply(); }
    else if (event.key === "ArrowDown") { y += 24; apply(); }
    else handled = false;
    if (handled) event.preventDefault();
  }, { signal: signal });

  scope.querySelectorAll("[data-plan-zoom]").forEach(function (button) {
    button.addEventListener("click", function () {
      var action = button.dataset.planZoom;
      if (action === "in") setScale(scale + 0.4);
      else if (action === "out") setScale(scale - 0.4);
      else reset();
    }, { signal: signal });
  });

  apply();
  return function () { controller.abort(); };
}

function mountAreaTool(scope) {
  var host = scope.querySelector('[data-role="area-map"]');
  var fallback = scope.querySelector('[data-role="area-fallback"]');
  var geo = preciseGeo();
  var selectedBearing = unitBearing(unit(state.unitId) || {});
  var map = null;

  if (!host) return function () {};
  if (!geo.ok || !SR.config.mapbox_token || !window.mapboxgl) {
    host.hidden = true;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = t("unit_area_unavailable");
    }
    return function () {};
  }

  try {
    window.mapboxgl.accessToken = SR.config.mapbox_token;
    map = new window.mapboxgl.Map({
      container: host,
      style: "mapbox://styles/mapbox/dark-v11",
      center: [geo.lng, geo.lat],
      zoom: 15.2,
      pitch: 42,
      bearing: selectedBearing == null ? 0 : selectedBearing,
      interactive: true,
      attributionControl: true
    });
    if (window.mapboxgl.NavigationControl) {
      map.addControl(new window.mapboxgl.NavigationControl({
        visualizePitch: true,
        showCompass: true
      }), "top-left");
    }
    if (window.mapboxgl.Marker) {
      new window.mapboxgl.Marker({ color: "#c9a34f" })
        .setLngLat([geo.lng, geo.lat])
        .addTo(map);
    }
    map.once("load", function () {
      try { map.resize(); } catch (e) {}
      restoreMapAttributionTabbing(scope);
    });
    map.once("idle", function () { restoreMapAttributionTabbing(scope); });
  } catch (error) {
    host.hidden = true;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = t("unit_area_unavailable");
    }
  }

  return function () {
    if (map) {
      try { map.remove(); } catch (e) {}
    }
    map = null;
  };
}

function mountContactTool(scope, u) {
  var form = scope.querySelector('[data-role="unit-contact-form"]');
  var feedback = scope.querySelector('[data-role="contact-feedback"]');
  if (!form) return function () {};

  var controller = new AbortController();
  var signal = controller.signal;

  function report(kind, message) {
    if (!feedback) return;
    feedback.hidden = false;
    feedback.className = "nl-unit-contact-form__feedback is-" + kind;
    feedback.textContent = message;
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var name = form.elements.namedItem("name");
    var phone = form.elements.namedItem("phone");
    var email = form.elements.namedItem("email");
    var consent = form.elements.namedItem("consent");
    var cleanName = name.value.trim();
    var cleanPhone = phone.value.trim();
    var cleanEmail = email.value.trim();

    name.setCustomValidity("");
    phone.setCustomValidity("");
    email.setCustomValidity("");
    consent.setCustomValidity("");
    name.setCustomValidity(cleanName.length >= 2 ? "" : t("unit_contact_name_error"));
    phone.setCustomValidity(
      cleanPhone || cleanEmail ? "" : t("unit_contact_channel_error")
    );
    if (cleanEmail && email.validity.typeMismatch) {
      email.setCustomValidity(t("unit_contact_email_error"));
    }
    consent.setCustomValidity(consent.checked ? "" : t("unit_contact_consent_error"));

    if (!form.checkValidity()) {
      report("error", t("unit_contact_validation_error"));
      form.reportValidity();
      return;
    }

    var endpoint = safeHttpUrl(SR.config.lead_endpoint);
    if (!endpoint) {
      report("error", t("unit_contact_unavailable"));
      return;
    }

    var p = project();
    var button = form.querySelector('button[type="submit"]');
    var originalLabel = button.textContent;
    var customMessage = form.elements.namedItem("message").value.trim();
    var payload = {
      source: "showroom_unit_journey_v2",
      project_slug: state.projectKey,
      project_title: projName(),
      project_wp_id: Number(p.wp_id) || 0,
      wp_id: Number(p.wp_id) || 0,
      card_id: Number(p.card_id || p.wp_id) || 0,
      lang: state.lang,
      name: cleanName,
      phone: cleanPhone,
      email: cleanEmail,
      unit: u.id,
      floor: u.floor,
      rooms: u.rooms,
      sqm: u.sqm,
      direction: dirKey(u.dir) || "",
      status: u.status || "",
      consent: true,
      consent_text: t("form_consent"),
      message: customMessage || t("unit_contact_payload", {
        floor: u.floor,
        rooms: u.rooms,
        sqm: u.sqm
      })
    };

    button.disabled = true;
    button.textContent = t("form_submitting");
    if (feedback) feedback.hidden = true;

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: signal
    }).then(function (response) {
      return response.text().then(function (text) {
        var data = {};
        try { data = text ? JSON.parse(text) : {}; } catch (e) {}
        if (!response.ok || data.ok !== true) throw new Error("lead_rejected");
        return data;
      });
    }).then(function () {
      report("success", t("unit_contact_success"));
      form.reset();
      button.disabled = false;
      button.textContent = originalLabel;
    }).catch(function (error) {
      if (error && error.name === "AbortError") return;
      report("error", t("unit_contact_failure"));
      button.disabled = false;
      button.textContent = originalLabel;
    });
  }, { signal: signal });

  return function () { controller.abort(); };
}

function openUnitTool(kind, u, trigger, options) {
  if (!u) return;
  options = options || {};

  /* The current Studio already owns a body-level overlay. Do not nest it. */
  if (!unitV2Enabled() && kind === "studio") {
    openStudio(u.id);
    return;
  }

  var allowed = unitV2Enabled()
    ? ["plan", "view", "tour", "studio", "area", "contact", "compare"]
    : ["plan", "view", "tour"];
  if (kind === "studio" && SR.config.studio === "off") return;
  if (allowed.indexOf(kind) < 0) return;

  var dialog = ensureUnitToolDialog();

  /* Defensive only: normal UI cannot open a second tool while ROOT is inert. */
  if (state.tool) return;

  state.tool = kind;
  unitTool.returnFocus = trigger || document.activeElement;
  unitTool.returnKind = kind;
  unitTool.pendingFocusRestore = true;
  unitTool.scrollY = window.pageYOffset;
  unitTool.closing = false;
  unitTool.fromHistory = options.fromHistory === true;

  dialog.setAttribute("dir", isRTL() ? "rtl" : "ltr");
  dialog.setAttribute("aria-labelledby", "nl-unit-tool-title");
  if (unitV2Enabled()) {
    dialog.setAttribute("tabindex", "-1");
    dialog.setAttribute("aria-modal", "true");
    dialog.className = "nl-unit-tool nl-unit-tool--" + kind;
  } else {
    dialog.removeAttribute("tabindex");
    dialog.removeAttribute("aria-modal");
    dialog.className = "nl-unit-tool";
  }
  dialog.innerHTML = unitToolMarkup(kind, u);

  setInert(ROOT, true);
  document.documentElement.classList.add("nl-unit-tool-open");
  document.body.classList.add("nl-unit-tool-open");

  if (typeof dialog.showModal === "function") dialog.showModal();
  else dialog.setAttribute("open", "");

  if (kind === "view") {
    unitTool.cleanup = mountUnitMapToolWhenReady("view", dialog, u);
  } else if (unitV2Enabled() && kind === "plan") {
    unitTool.cleanup = mountPlanTool(dialog);
  } else if (unitV2Enabled() && kind === "area") {
    unitTool.cleanup = mountUnitMapToolWhenReady("area", dialog, u);
  } else if (unitV2Enabled() && kind === "contact") {
    unitTool.cleanup = mountContactTool(dialog, u);
  } else if (unitV2Enabled() && kind === "compare") {
    unitTool.cleanup = mountUnitV2Compare(dialog, u);
  } else if (kind === "tour" && !(u.tour_url || project().tour_url)) {
    fpInit();
  }

  unitTool.historyMarker = options.historyMarker ||
    "nl-unit-tool-" + Date.now().toString(36);

  if (!unitTool.fromHistory) {
    history.pushState(
      Object.assign({}, history.state || {}, {
        nlUnitTool: unitTool.historyMarker,
        nlUnitToolKind: kind,
        nlUnitToolUnit: u.id
      }),
      "",
      location.href
    );
  }

  requestAnimationFrame(function () {
    var back = dialog.querySelector('[data-act="unit-tool-back"]');
    if (back) back.focus({ preventScroll: true });
  });
}

/*
 * UI close first walks back across the synthetic tool history entry. The
 * popstate handler performs teardown. fromHistory=true is reserved for the
 * popstate path and controlled sandbox teardown.
 */
function closeUnitTool(restoreFocus, fromHistory) {
  if (!state.tool) return;
  if (unitV2Enabled() && unitTool.closing) return;

  unitTool.pendingFocusRestore = restoreFocus !== false;

  if (
    !fromHistory &&
    unitTool.historyMarker &&
    history.state &&
    history.state.nlUnitTool === unitTool.historyMarker
  ) {
    if (unitV2Enabled()) unitTool.closing = true;
    history.back();
    return;
  }

  finishUnitToolClose(unitTool.pendingFocusRestore);
}

/* A language/project rerender cannot wait for an asynchronous history.back().
   Convert the current synthetic entry into an ordinary entry before teardown,
   so Forward/Back never lands on an orphaned tool marker. */
function normalizeUnitToolHistory() {
  var current = history.state || {};
  if (!current.nlUnitTool) return;
  var clean = Object.assign({}, current);
  delete clean.nlUnitTool;
  delete clean.nlUnitToolKind;
  delete clean.nlUnitToolUnit;
  history.replaceState(clean, "", location.href);
}

/* Mapbox is intentionally loaded after the core engine by WordPress. A buyer
 * can select a unit and open a map tool before that script has executed; do
 * not turn that harmless load race into a permanent fallback. The retry is
 * bounded, cancellable, and owns no DOM outside the body-level dialog. */
function mountUnitMapToolWhenReady(kind, scope, u) {
  var cancelled = false;
  var timer = 0;
  var cleanup = null;
  var attempts = 0;
  var geo = preciseGeo();

  function mount() {
    if (cancelled || !document.contains(scope)) return;
    if (!geo.ok || !SR.config.mapbox_token || window.mapboxgl) {
      cleanup = kind === "area"
        ? mountAreaTool(scope)
        : mountWindowViewport(scope, u);
      return;
    }
    attempts += 1;
    if (attempts >= 40) {
      cleanup = kind === "area"
        ? mountAreaTool(scope)
        : mountWindowViewport(scope, u);
      return;
    }
    timer = window.setTimeout(mount, 100);
  }

  mount();
  return function () {
    cancelled = true;
    if (timer) window.clearTimeout(timer);
    if (cleanup) cleanup();
  };
}

function visibleFocusable(el) {
  if (!el || !document.contains(el) || el.disabled) return false;
  var rect = el.getBoundingClientRect();
  var style = window.getComputedStyle(el);
  return rect.width > 0 && rect.height > 0 &&
    rect.bottom > 0 && rect.right > 0 &&
    rect.top < window.innerHeight && rect.left < window.innerWidth &&
    style.visibility !== "hidden" && style.opacity !== "0" &&
    style.pointerEvents !== "none";
}

function unitV2ReturnTarget(original, kind) {
  if (visibleFocusable(original)) return original;
  var screen = document.getElementById("nl-unit-screen");
  if (!screen || screen.hidden) return null;
  var exact = screen.querySelector(
    '[data-act="unit-tool"][data-tool="' + cssesc(kind || "") + '"]'
  );
  if (visibleFocusable(exact)) return exact;
  var stable = screen.querySelector(
    ".nl-unit-door, [data-act=\"unit-back\"], .nl-unit-contact"
  );
  return visibleFocusable(stable) ? stable : null;
}

function restoreUnitV2Scroll(y, focusTarget) {
  var rootStyle = document.documentElement.style;
  var previousBehavior = rootStyle.scrollBehavior;
  rootStyle.scrollBehavior = "auto";
  window.scrollTo(0, y);
  requestAnimationFrame(function () {
    window.scrollTo(0, y);
    if (focusTarget) focusTarget.focus({ preventScroll: true });
    window.scrollTo(0, y);
    rootStyle.scrollBehavior = previousBehavior;
  });
}

function restoreUnitV2AfterViewportSync(returnKind, restoreFocus) {
  var attempts = 0;

  function settle() {
    var theaterEl = ROOT.querySelector(".nl-theater--unit-v2");
    /* The atomic render removes this transition marker in its queued frame.
       Do not decide visibility/focus from the intermediate geometry. */
    if (theaterEl && theaterEl.classList.contains("nl-unit-v2-transitioning") &&
        attempts < 3) {
      attempts += 1;
      requestAnimationFrame(settle);
      return;
    }

    /* `behavior: auto` still inherits a stylesheet's smooth scroll behavior.
       Keep this whole geometry/focus transaction synchronous so the freshly
       rendered return target is measured only after the theater is aligned. */
    var rootStyle = document.documentElement.style;
    var previousBehavior = rootStyle.scrollBehavior;
    rootStyle.scrollBehavior = "auto";
    try {
      alignUnitV2Theater(true, true);
      var focusTarget = restoreFocus ? unitV2ReturnTarget(null, returnKind) : null;
      if (focusTarget) focusTarget.focus({ preventScroll: true });
      /* Scene visibility wins over a pre-rotation scroll coordinate. A final
         single-pass alignment also neutralizes browser focus anchoring. */
      alignUnitV2Theater(true, true);
    } finally {
      rootStyle.scrollBehavior = previousBehavior;
    }
  }

  requestAnimationFrame(settle);
}

function finishUnitToolClose(restoreFocus) {
  var dialog = unitTool.dialog;
  var returnFocus = unitTool.returnFocus;
  var returnKind = unitTool.returnKind;
  var savedScrollY = unitTool.scrollY;
  var wasV2 = unitV2Enabled();

  if (unitTool.cleanup) {
    try { unitTool.cleanup(); } catch (e) {}
  }

  unitTool.cleanup = null;
  unitTool.returnFocus = null;
  unitTool.returnKind = null;
  unitTool.historyMarker = null;
  unitTool.closing = false;
  unitTool.fromHistory = false;
  state.tool = null;

  if (dialog) {
    if (dialog.open && typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
    dialog.innerHTML = "";
    dialog.className = "nl-unit-tool";
    if (wasV2) {
      dialog.removeAttribute("tabindex");
      dialog.removeAttribute("aria-modal");
    }
  }

  setInert(ROOT, false);
  document.documentElement.classList.remove("nl-unit-tool-open");
  document.body.classList.remove("nl-unit-tool-open");

  if (wasV2) {
    /* A resize/orientation event may have arrived while the modal correctly
       kept the inactive scene frozen. Reconcile that subtree before resolving
       the replacement focus target and before restoring the saved scroll. */
    var didViewportSync = flushUnitV2ViewportSyncAfterTool();
    if (didViewportSync) {
      restoreUnitV2AfterViewportSync(returnKind, restoreFocus);
    } else {
      restoreUnitV2Scroll(
        savedScrollY,
        restoreFocus ? unitV2ReturnTarget(returnFocus, returnKind) : null
      );
    }
  } else if (restoreFocus && returnFocus && document.contains(returnFocus)) {
    requestAnimationFrame(function () {
      returnFocus.focus({ preventScroll: true });
    });
  }
}

window.addEventListener("popstate", function (event) {
  if (state.tool) {
    finishUnitToolClose(unitTool.pendingFocusRestore);
    return;
  }

  /* Browser Forward re-enters the synthetic entry and truthfully reopens the
     tool instead of creating an invisible, trapping history step. */
  var markerState = event.state || {};
  if (!unitV2Enabled() || !markerState.nlUnitTool) return;
  var u = unit(markerState.nlUnitToolUnit);
  var kind = markerState.nlUnitToolKind;
  var activeScreen = document.getElementById("nl-unit-screen");
  if (!u || state.unitId !== markerState.nlUnitToolUnit ||
      !activeScreen || activeScreen.hidden ||
      ["plan", "view", "tour", "studio", "area", "contact", "compare"].indexOf(kind) < 0) {
    normalizeUnitToolHistory();
    if (typeof deeplink === "function") deeplink();
    return;
  }
  var trigger = document.querySelector(
    '[data-act="unit-tool"][data-tool="' + cssesc(kind) + '"]'
  );
  openUnitTool(kind, u, trigger, {
    fromHistory: true,
    historyMarker: markerState.nlUnitTool
  });
});

function mountWindowViewport(scope, u) {
  var host = scope.querySelector('[data-role="window-map"]');
  var fallback = scope.querySelector('[data-role="window-fallback"]');
  var geo = preciseGeo();
  var bearing = unitBearing(u);

  if (!host) return function () {};

  if (bearing == null || !geo.ok || !SR.config.mapbox_token || !window.mapboxgl) {
    host.hidden = true;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = bearing == null
        ? t("unit_window_direction_unavailable")
        : t("unit_map_unverified");
    }
    return function () {};
  }

  var controller = new AbortController();
  var signal = controller.signal;
  var dragging = false;
  var lastX = 0;
  var lastY = 0;
  var vertical = 0;
  var map = null;

  function applyCamera() {
    if (map) winCam(map, u, bearing, vertical);
  }

  function turn(delta) {
    bearing = (bearing + delta + 360) % 360;
    applyCamera();
  }

  try {
    window.mapboxgl.accessToken = SR.config.mapbox_token;

    map = new window.mapboxgl.Map({
      container: host,
      style: "mapbox://styles/mapbox/satellite-streets-v12",
      center: [geo.lng, geo.lat],
      zoom: 16.5,
      pitch: 70,
      bearing: bearing,
      maxPitch: 85,
      interactive: false,
      attributionControl: true
    });
  } catch (error) {
    host.hidden = true;
    if (fallback) {
      fallback.hidden = false;
      fallback.textContent = t("unit_map_unverified");
    }
    controller.abort();
    return function () {};
  }

  map.once("load", function () {
    try {
      var layers = map.getStyle().layers;
      var labelLayer;

      for (var i = 0; i < layers.length; i++) {
        if (
          layers[i].type === "symbol" &&
          layers[i].layout &&
          layers[i].layout["text-field"]
        ) {
          labelLayer = layers[i].id;
          break;
        }
      }

      map.addLayer({
        id: "nl-unit-window-buildings",
        source: "composite",
        "source-layer": "building",
        filter: ["==", "extrude", "true"],
        type: "fill-extrusion",
        minzoom: 13,
        paint: {
          "fill-extrusion-color": "#d8d2c4",
          "fill-extrusion-height": ["get", "height"],
          "fill-extrusion-base": ["get", "min_height"],
          "fill-extrusion-opacity": 0.86
        }
      }, labelLayer);
    } catch (e) {}

    applyCamera();
    if (unitV2Enabled()) restoreMapAttributionTabbing(scope);
  });

  map.once("error", function () {
    if (fallback && !fallback.textContent) {
      fallback.hidden = false;
      fallback.textContent = t("unit_map_unverified");
    }
  });

  host.addEventListener("pointerdown", function (event) {
    dragging = true;
    lastX = event.clientX;
    lastY = event.clientY;
    host.setPointerCapture(event.pointerId);
    event.preventDefault();
  }, { signal: signal });

  host.addEventListener("pointermove", function (event) {
    if (!dragging) return;

    bearing = (bearing + (event.clientX - lastX) * 0.35 + 360) % 360;
    vertical = Math.max(
      -45,
      Math.min(10, vertical - (event.clientY - lastY) * 0.22)
    );

    lastX = event.clientX;
    lastY = event.clientY;
    applyCamera();
    event.preventDefault();
  }, { signal: signal });

  host.addEventListener("pointerup", function (event) {
    dragging = false;
    try { host.releasePointerCapture(event.pointerId); } catch (e) {}
  }, { signal: signal });

  host.addEventListener("pointercancel", function () {
    dragging = false;
  }, { signal: signal });

  host.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      turn(isRTL() ? 15 : -15);
    }

    if (event.key === "ArrowRight") {
      event.preventDefault();
      turn(isRTL() ? -15 : 15);
    }
  }, { signal: signal });

  scope.querySelectorAll("[data-turn]").forEach(function (button) {
    button.addEventListener("click", function () {
      turn(parseInt(button.dataset.turn, 10) || 0);
    }, { signal: signal });
  });

  return function () {
    controller.abort();
    if (map) {
      try { map.remove(); } catch (e) {}
    }
    map = null;
  };
}

  /* ============ SELECTED-UNIT SURFACE (audit 2026-08-08, flag-gated) ============
     Active only when SR.config.selected_unit_surface is true (sandbox meta).
     With the flag off every path below routes to the untouched legacy code. */

  function selectUnit(id, instant, source) {
    if (!SR.config.selected_unit_surface) { selectUnitLegacy(id, instant); return; }
    var u = unit(id); if (!u) return;
    var v2 = unitV2Enabled();
    var theaterEl = ROOT.querySelector(".nl-theater");
    var cameFromOutsideTheater = !!(source && theaterEl && !theaterEl.contains(source));
    var scrim = document.getElementById("nl-scrim");
    var srcEl = document.querySelector('.nl-hot[data-id="' + cssesc(id) + '"]') || document.querySelector('.nl-fsq[data-id="' + cssesc(id) + '"]');
    var srcRect = null, wrapRect = null;
    /* geometry reads before renderUnitScreen writes the DOM (no forced reflow) */
    if (srcEl) { srcRect = srcEl.getBoundingClientRect(); if (!srcRect.width) { srcEl = null; srcRect = null; } }
    if (scrim && scrim.parentElement) wrapRect = scrim.parentElement.getBoundingClientRect();
    unitSurface.source = v2
      ? (source || srcEl || null)
      : (srcEl || source || null);
    state.unitId = id; state.tab = "plan";
    document.querySelectorAll(".nl-hot,.nl-fsq,.nl-ucard").forEach(function (n) { n.classList.toggle("is-active", n.dataset.id === id); });
    if (scrim) {
      if (srcRect && wrapRect && wrapRect.width && wrapRect.height) {
        scrim.style.setProperty("--sx", ((srcRect.left + srcRect.width / 2 - wrapRect.left) / wrapRect.width * 100) + "%");
        scrim.style.setProperty("--sy", ((srcRect.top + srcRect.height / 2 - wrapRect.top) / wrapRect.height * 100) + "%");
      }
      scrim.classList.add("is-on");
    }
    if (v2) {
      /* Selection is a scene transition, regardless of mouse/touch/keyboard or
         whether it originated in the model or the inventory. */
      renderUnitScreen(u, {
        align: true,
        instant: !!instant,
        focus: !instant
      });
    } else {
      renderUnitScreen(u, { scroll: UNIT_MQ.matches && (cameFromOutsideTheater || instant), focus: !instant });
    }
    easeMapToUnitView(u);
    var mv = document.getElementById("nl-mv");
    if (mv && u.camera_orbit) {
      try {
        if (instant) { mv.cameraOrbit = orbitRadius(u.camera_orbit, Math.round((project().frame_radius_m || 150) * 0.66)); mv.cameraTarget = unitPos(u).pos; }
        else { flyCamera(mv, u); }
      } catch (e) {}
    }
    if (!v2 && !UNIT_MQ.matches && !instant && srcEl) liftCard(srcEl, u);
    updateFormCtx(); updateSticky(); deeplink(); recordRecent(u);
    var rv = document.getElementById("nl-resetview"); if (rv) rv.hidden = false;
  }

  function closePanel() {
    if (!SR.config.selected_unit_surface) { closePanelLegacy(); return; }
    /* one back action closes the tool first; a second returns to the building */
    if (state.tool) { closeUnitTool(true, false); return; }
    var closingUnitId = state.unitId;
    var v2 = unitV2Enabled();
    var returnTarget = v2 ? null : unitSurface.source;
    clearUnitScreen();
    state.unitId = null; state.tool = null;
    var scrim = document.getElementById("nl-scrim"); if (scrim) scrim.classList.remove("is-on");
    document.querySelectorAll(".is-active").forEach(function (n) { n.classList.remove("is-active"); });
    var mv = document.getElementById("nl-mv");
    if (mv) { try { mv.interpolationDecay = 50; mv.fieldOfView = "auto"; mv.cameraOrbit = project().default_orbit; mv.cameraTarget = project().default_target; } catch (e) {} }
    updateFormCtx(); updateSticky(); deeplink();
    if (v2) {
      requestAnimationFrame(function () {
        var stage = ROOT.querySelector(".nl-stagewrap");
        var hotspot = stage && stage.querySelector(
          '.nl-hot[data-id="' + cssesc(closingUnitId || "") + '"], ' +
          '.nl-fsq[data-id="' + cssesc(closingUnitId || "") + '"]'
        );
        var target = visibleFocusable(hotspot)
          ? hotspot
          : document.getElementById("nl-mv");
        if (target && document.contains(target)) {
          if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "0");
          target.focus({ preventScroll: true });
        }
      });
    } else if (returnTarget && document.contains(returnTarget)) {
      requestAnimationFrame(function () { returnTarget.focus({ preventScroll: true }); });
    }
  }


  function selectUnitLegacy(id, instant) {
    var u = unit(id); if (!u) return;
    var prev = state.unitId; state.unitId = id; state.tab = "plan";
    // panel
    var body = document.getElementById("nl-panel-body"), panelEl = document.getElementById("nl-panel");
    if (body) body.innerHTML = panelBody(u);
    if (panelEl) panelEl.classList.add("is-open");
    // active markers
    document.querySelectorAll(".nl-hot,.nl-fsq,.nl-ucard").forEach(function (n) { n.classList.toggle("is-active", n.dataset.id === id); });
    // the map turns to face what this apartment sees
    easeMapToUnitView(u);
    // scrim + spotlight origin
    var scrim = document.getElementById("nl-scrim");
    var srcEl = document.querySelector('.nl-hot[data-id="' + cssesc(id) + '"]') || document.querySelector('.nl-fsq[data-id="' + cssesc(id) + '"]');
    if (srcEl && !srcEl.getBoundingClientRect().width) { srcEl = null; }
    if (scrim) {
      var wrap = scrim.parentElement.getBoundingClientRect();
      if (srcEl) { var r = srcEl.getBoundingClientRect(); scrim.style.setProperty("--sx", ((r.left + r.width / 2 - wrap.left) / wrap.width * 100) + "%"); scrim.style.setProperty("--sy", ((r.top + r.height / 2 - wrap.top) / wrap.height * 100) + "%"); }
      scrim.classList.add("is-on");
    }
    // camera fly (two-beat cinematic move per design spec 4B-1; instant selects skip it)
    var mv = document.getElementById("nl-mv");
    if (mv && u.camera_orbit) {
      try {
        if (instant) { mv.cameraOrbit = orbitRadius(u.camera_orbit, Math.round((project().frame_radius_m || 150) * 0.66)); mv.cameraTarget = unitPos(u).pos; }
        else { flyCamera(mv, u); }
      } catch (e) {}
    }
    // cinematic lift-out apartment card (the "drawer")
    if (!instant && srcEl) liftCard(srcEl, u);
    // context + deep link
    updateFormCtx(); updateSticky();
    deeplink();
    recordRecent(u);
    var rv = document.getElementById("nl-resetview"); if (rv) rv.hidden = false;
  }
  /* Apartment Studio bridge: hand the overlay everything it needs */
  function openStudio(id) {
    var u = unit(id || state.unitId); if (!u || !window.NLStudio) return;
    window.NLStudio.open({
      unit: u, t: t, projectKey: state.projectKey, projectName: projName(),
      whatsapp: SR.config.whatsapp || "", leadEndpoint: SR.config.lead_endpoint || "",
      homeUrl: (SR.config.home_url || "")
    });
  }
  /* the "way back" pill (seat-map ergonomics): one tap returns the camera to
     the full building after a unit dive - pinch-hunting never required. */
  function resetView() {
    var mv = document.getElementById("nl-mv"), p = project();
    if (mv && p) { try { mv.cameraOrbit = p.default_orbit; mv.cameraTarget = p.default_target || "auto auto auto"; } catch (e) {} }
    var scrim = document.getElementById("nl-scrim"); if (scrim) scrim.classList.remove("is-on");
    var rv = document.getElementById("nl-resetview"); if (rv) rv.hidden = true;
  }
  /* Two-beat camera choreography (design spec 4B-1): pull back to a wide orbit
     on the unit's bearing, then dive to the unit face while retargeting.
     interpolationDecay=160 is what makes the move filmic instead of snappy. */
  function flyCamera(mv, u) {
    var p = project();
    var fr = p.frame_radius_m || 150;
    var end = orbitRadius(u.camera_orbit, Math.round(fr * 0.62));
    var endTarget = unitPos(u).pos;
    var mid = orbitRadius(u.camera_orbit, Math.round(fr * 1.15));
    mv.interpolationDecay = 160;
    mv.cameraOrbit = mid;
    setTimeout(function () {
      try { mv.cameraTarget = endTarget; mv.cameraOrbit = end; mv.fieldOfView = "28deg"; } catch (e) {}
    }, 300);
    setTimeout(function () { try { mv.interpolationDecay = 50; } catch (e) {} }, 1400);
  }
  /* Lift-out apartment card (design spec 4B-2): a card visually lifts from the
     unit's position on the facade, scales up while the scene dims, then docks
     into the panel header. Pure DOM - works with any model. */
  function liftCard(srcEl, u) {
    var panelEl = document.getElementById("nl-panel"); if (!panelEl || !srcEl) return;
    var s = srcEl.getBoundingClientRect();
    var card = document.createElement("div");
    card.className = "nl-lift";
    card.innerHTML =
      '<div class="nl-lift__floor">' + esc(u.floor) + '</div>' +
      '<div class="nl-lift__meta">' + esc(roomsLabel(u.rooms)) + ' · ' + esc(u.sqm) + ' ' + esc(t('sqm_unit')) + '</div>' +
      '<div class="nl-lift__dir">' + esc(dirLabel(u.dir)) + '</div>';
    document.body.appendChild(card);
    var head = panelEl.querySelector('.nl-panel__title') || panelEl;
    requestAnimationFrame(function () {
      var d = head.getBoundingClientRect();
      var x0 = s.left + s.width / 2, y0 = s.top + s.height / 2;
      var x1 = d.left + d.width / 2, y1 = d.top + d.height / 2;
      card.animate([
        { transform: 'translate(' + (x0 - 90) + 'px,' + (y0 - 60) + 'px) scale(.32)', opacity: 0 },
        { transform: 'translate(' + (x0 - 90) + 'px,' + (y0 - 130) + 'px) scale(1)', opacity: 1, offset: 0.38 },
        { transform: 'translate(' + ((x0 + x1) / 2 - 90) + 'px,' + (Math.min(y0, y1) - 150) + 'px) scale(1.02)', opacity: 1, offset: 0.7 },
        { transform: 'translate(' + (x1 - 90) + 'px,' + (y1 - 60) + 'px) scale(.45)', opacity: 0 }
      ], { duration: 920, easing: 'cubic-bezier(.22,.61,.36,1)' }).onfinish = function () { card.remove(); };
    });
  }
  function closePanelLegacy() {
    state.unitId = null;
    var p = document.getElementById("nl-panel"); if (p) p.classList.remove("is-open");
    var s = document.getElementById("nl-scrim"); if (s) s.classList.remove("is-on");
    document.querySelectorAll(".is-active").forEach(function (n) { n.classList.remove("is-active"); });
    var mv = document.getElementById("nl-mv"); if (mv) { try { mv.interpolationDecay = 50; mv.fieldOfView = "auto"; mv.cameraOrbit = project().default_orbit; mv.cameraTarget = project().default_target; } catch (e) {} }
    updateFormCtx(); updateSticky(); deeplink();
  }
  function restoreQuickActionFocus(action, id, shouldRestore) {
    if (!shouldRestore) return;
    requestAnimationFrame(function () {
      var next = document.querySelector(
        '[data-act="' + cssesc(action) + '"][data-id="' + cssesc(id) + '"]'
      );
      if (visibleFocusable(next)) next.focus({ preventScroll: true });
    });
  }
  function toggleFav(id) {
    var restoreFocus = !!(document.activeElement &&
      document.activeElement.matches('[data-act="fav"][data-id="' + cssesc(id) + '"]'));
    var i = state.favs.indexOf(id); if (i >= 0) state.favs.splice(i, 1); else state.favs.push(id);
    save("nl_favs", state.favs);
    if (state.filter === "favs" && !state.favs.length) state.filter = "all";
    refresh("inventory"); // hearts, the saved chip and its count stay truthful
    if (state.unitId === id) {
      if (SR.config.selected_unit_surface) renderUnitScreen(unit(id), { focus: false, scroll: false });
      else { var body = document.getElementById("nl-panel-body"); if (body) body.innerHTML = panelBody(unit(id)); }
    }
    restoreQuickActionFocus("fav", id, restoreFocus);
  }
  function toggleCompare(id) {
    var restoreFocus = !!(document.activeElement &&
      document.activeElement.matches('[data-act="compare"][data-id="' + cssesc(id) + '"]'));
    var i = state.compare.indexOf(id);
    if (i >= 0) state.compare.splice(i, 1);
    else { if (state.compare.length >= 3) state.compare.shift(); state.compare.push(id); }
    refreshCompare();
    if (state.unitId === id) {
      if (SR.config.selected_unit_surface) renderUnitScreen(unit(id), { focus: false, scroll: false });
      else { var body2 = document.getElementById("nl-panel-body"); if (body2) body2.innerHTML = panelBody(unit(id)); }
    }
    restoreQuickActionFocus("compare", id, restoreFocus);
  }
  function refreshCompare() {
    var old = document.getElementById("nl-compare"); if (old) old.outerHTML = compareTray();
  }
  function refresh(sectionId) {
    var sec = document.getElementById(sectionId); if (sec) sec.innerHTML = inventory();
  }
  function share(id) {
    var url = location.origin + location.pathname + "?project=" + state.projectKey + (id ? "&unit=" + id : "") + "&lang=" + state.lang;
    if (navigator.share) { navigator.share({ url: url, title: projName() }).catch(function () {}); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(url).then(toastCopied, function () {});
  }
  function toastCopied() { var b = document.querySelector('[data-act="share"]'); if (b) { var o = b.innerHTML; b.innerHTML = svg("check", 16) + t("link_copied"); setTimeout(function () { b.innerHTML = o; }, 1600); } }
  function switchLang(l) {
    // Each language is its own crawlable post. Navigate to the sibling URL when we
    // have it (real page, real SEO); only fall back to a client swap if no sibling.
    var p = project();
    if (!unitV2Sandbox() && p && p.lang_urls && p.lang_urls[l]) { location.href = p.lang_urls[l]; return; }
    if (!I18N.langs[l]) return; state.lang = l;
    var u = new URL(location.href); u.searchParams.set("lang", l); history.replaceState(null, "", u);
    render();
  }
  function scrollTo(id) { var t2 = document.getElementById(id); if (t2) window.scrollTo({ top: t2.getBoundingClientRect().top + window.pageYOffset - 112, behavior: "smooth" }); }
  function setupSpy() {
    var nav = document.getElementById("nl-secnav");
    if (!nav || !("IntersectionObserver" in window)) return;
    var links = {};
    nav.querySelectorAll("a[data-spy]").forEach(function (a) { links[a.getAttribute("data-spy")] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.id;
        Object.keys(links).forEach(function (k) { links[k].classList.toggle("is-active", k === id); });
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
    Object.keys(links).forEach(function (id) { var el = document.getElementById(id); if (el) obs.observe(el); });
  }
  function highlightPin(node) { document.querySelectorAll(".nl-pin").forEach(function (p) { p.classList.remove("is-on"); }); node.classList.add("is-on"); }

  function updateFormCtx() {
    var ctx = document.getElementById("nl-formctx"); if (!ctx) return;
    var u = unit(state.unitId);
    ctx.innerHTML = '<span class="d"></span>' + (u ? esc(t("form_unit_ctx", { label: unitDisplayLabel(u), floor: u.floor, rooms: u.rooms })) : esc(t("form_no_unit")));
  }
  function updateSticky() {
    var c = document.getElementById("nl-stickyctx"); if (!c) return;
    var u = unit(state.unitId); c.textContent = u ? (" · " + t("unit_short", { label: unitDisplayLabel(u), floor: u.floor })) : "";
    var wa = document.getElementById("nl-wa");
    if (wa && SR.config.whatsapp) {
      var msg = (u ? t("form_unit_ctx", { label: unitDisplayLabel(u), floor: u.floor, rooms: u.rooms }) : t("form_no_unit")) + " · " + projName();
      wa.href = "https://wa.me/" + SR.config.whatsapp + "?text=" + encodeURIComponent(msg);
    }
  }
  function onScroll() {
    var s = document.getElementById("nl-sticky"); if (!s) return;
    s.classList.toggle("is-on", window.pageYOffset > 540);
  }
  function onSubmit(e) {
    e.preventDefault();
    var f = e.target, name = f.name.value.trim(), phone = f.phone.value.trim(), email = f.email.value.trim();
    var msg = document.getElementById("nl-formmsg");
    if (!name || (!phone && !email)) { show(msg, "err", t("form_error")); return; }
    var u = unit(state.unitId);
    var payload = {
      source: "showroom_engine", project_slug: state.projectKey, project_title: projName(), lang: state.lang,
      name: name, phone: phone, email: email,
      unit: u ? u.id : "", floor: u ? u.floor : "", rooms: u ? u.rooms : "", sqm: u ? u.sqm : "", direction: u ? u.dir : "", status: u ? u.status : "",
      message: u ? t("form_unit_ctx", { label: unitDisplayLabel(u), floor: u.floor, rooms: u.rooms }) : t("form_no_unit")
    };
    var btn = f.querySelector('button[type="submit"]'); btn.disabled = true; btn.textContent = t("form_submitting");
    var done = function () { show(msg, "ok", t("form_success")); f.reset(); btn.disabled = false; btn.textContent = t("form_submit"); updateFormCtx(); };
    var ep = SR.config.lead_endpoint;
    if (unitV2Enabled()) {
      var projectData = project();
      payload.source = "showroom_unit_journey_v2_page_form";
      payload.project_wp_id = Number(projectData.wp_id) || 0;
      payload.wp_id = Number(projectData.wp_id) || 0;
      payload.card_id = Number(projectData.card_id || projectData.wp_id) || 0;
      var fail = function () {
        show(msg, "err", t("unit_contact_failure"));
        btn.disabled = false;
        btn.textContent = t("form_submit");
      };
      var safeEndpoint = safeHttpUrl(ep);
      if (!safeEndpoint) { fail(); return; }
      try {
        fetch(safeEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }).then(function (response) {
          return response.text().then(function (text) {
            var data = {};
            try { data = text ? JSON.parse(text) : {}; } catch (e) {}
            if (!response.ok || data.ok !== true) throw new Error("lead_rejected");
          });
        }).then(done).catch(fail);
      } catch (error) { fail(); }
      return;
    }
    try {
      fetch(ep, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { return r.ok ? r.json().catch(function () { return {}; }) : Promise.reject(0); })
        .then(done).catch(done);
    } catch (_) { done(); }
  }
  function show(el2, kind, txt) { if (!el2) return; el2.hidden = false; el2.className = "nl-feedback " + kind; el2.textContent = txt; }

  function deeplink() {
    var u = new URL(location.href);
    u.searchParams.set("project", state.projectKey); u.searchParams.set("lang", state.lang);
    if (state.unitId) u.searchParams.set("unit", state.unitId); else u.searchParams.delete("unit");
    history.replaceState(null, "", u);
  }
  function cssesc(s) { return String(s).replace(/["\\]/g, "\\$&"); }

  render();
  if (cotour.role === 'host' || cotour.role === 'join') { setTimeout(cotourRun, 1200); if (cotour.role === 'host') { setTimeout(function () { cotourBar(t('cotour_live') + ' · ' + cotour.room, 'is-host'); }, 1300); } }
  window.NadLanEngine = { render: render, state: state, t: t };
})();
