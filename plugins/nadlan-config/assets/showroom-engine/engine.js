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
    view: "3d", tab: "plan", filter: "all", light: "day",
    favs: load("nl_favs", []), compare: [],
    mvReady: false
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
  function projectStatusLabel(s) {
    return ["planning", "permit", "marketing", "construction", "completed"].indexOf(s) >= 0
      ? t("project_status_" + s)
      : "";
  }
  function roomsLabel(n) { return t("rooms_label", { n: n }); }
  function viewText(u) { return u.view_key ? t(u.view_key) : ""; }
  function area() { return (SR.areas && SR.areas[project().area]) || { map: { pins: [], project_pin: { x: 50, y: 50 }, coast_x: 16 }, spoke_groups: [], stats: [] }; }
  function spoke(id) { return (SR.spokes && SR.spokes[id]) || null; }

  function load(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
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
    if (hp.length === 3 && hp.every(function (n) { return isFinite(parseFloat(n)); })) {
      var hn = String(u.hotspot_normal || "0 0 1").trim().split(/\s+/);
      if (hn.length !== 3 || !hn.every(function (n) { return isFinite(parseFloat(n)); })) hn = ["0", "0", "1"];
      return {
        pos: hp.map(function (n) { return parseFloat(n).toFixed(2) + "m"; }).join(" "),
        nrm: hn.map(function (n) { return parseFloat(n) + "m"; }).join(" ")
      };
    }
    var fh = parseFloat(project().floor_height_m) || 3.05, half = 13.2;
    var v = DIRV[dirKey(u.dir) || u.dir] || [-1, 0], y = u.floor * fh + fh * 0.4;
    return { pos: (v[0] * half).toFixed(2) + "m " + y.toFixed(2) + "m " + (v[1] * half).toFixed(2) + "m", nrm: v[0] + "m 0m " + v[1] + "m" };
  }
  function orbitRadius(orbit, r) { var p = String(orbit).trim().split(/\s+/); if (p.length >= 3) p[2] = r + "m"; return p.join(" "); }

  /* =====================================================================
     RENDER
  ===================================================================== */
  function render() {
    // The adopted unified map (#nlpjx-map) lives INSIDE nl-root next to the
    // theater; rescue it before innerHTML wipes it, re-adopt in afterRender().
    var uni = document.getElementById("nlpjx-map");
    if (uni && ROOT.contains(uni)) { ROOT.insertAdjacentElement("afterend", uni); }
    document.documentElement.lang = state.lang;
    document.documentElement.dir = isRTL() ? "rtl" : "ltr";
    document.title = (state.page === "home" ? t("home_gallery_title") : (projName() + " · " + t("brand_sub")));
    ROOT.className = "nl-app";
    ROOT.innerHTML = (state.page === "home")
      ? header() + homeMain() + footer()
      : (project().composed
        ? projectBar() + secNav() + projectMain() + sticky() + compareTray()
        : header() + secNav() + projectMain() + footer() + sticky() + compareTray());
    afterRender();
  }

  /* ---- header + language bar ---- */
  function pageLangs() {
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
  function langBar() {
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
      '<a class="nl-brand" href="' + esc(SR.config.home_url || "/") + '"><span class="nl-brand__mark">N</span><span><span class="nl-brand__name">' + esc(t("brand")) + '</span> <span class="nl-brand__sub">' + esc(t("brand_sub")) + "</span></span></a>" +
      '<nav class="nl-nav">' + nav + langBar() + "</nav></div></header>";
  }

  function projectBar() {
    var home = SR.config.home_url || "/";
    var projects = SR.config.projects_url || (home.replace(/\/$/, "") + "/projects/");
    return '<div class="nl-projectbar"><div class="nl-wrap nl-projectbar__row">' +
      '<nav class="nl-breadcrumb" aria-label="' + esc(t("breadcrumb_aria")) + '">' +
        '<a href="' + esc(home) + '">' + esc(t("breadcrumb_home")) + '</a><span aria-hidden="true">/</span>' +
        '<a href="' + esc(projects) + '">' + esc(t("breadcrumb_projects")) + '</a><span aria-hidden="true">/</span>' +
        '<span aria-current="page">' + esc(projName()) + '</span></nav>' +
      langBar() + '</div></div>';
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
  function projectMain() {
    return "<main>" +
      '<section class="nl-sec nl-wrap" id="top">' + hero() + "</section>" +
      projectMilestone() +
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
    var projectMeta = p.composed ? [p.developer_name, projectStatusLabel(p.project_status), p.completion_year ? t("handover_estimated", { n: p.completion_year }) : ""].filter(Boolean) : [];
    return '<div class="nl-hero">' +
      "<div>" +
        '<span class="nl-eyebrow">' + esc(t("hero_eyebrow")) + "</span>" +
        '<hr class="nl-rule">' +
        '<h1 class="nl-hero__h1">' + esc(projName()) + "</h1>" +
        (projectMeta.length ? '<div class="nl-hero__meta">' + projectMeta.map(function (value) { return '<span>' + esc(value) + '</span>'; }).join("") + '</div>' : "") +
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

  /* The buyer-facing progress tracker replaces the older standalone band on
     composed pages, retaining the capability inside one project hierarchy. */
  function projectMilestone() {
    var p = project(), stage = parseInt(p.project_stage, 10);
    if (!p.composed) return "";
    if (!isFinite(stage)) stage = -1;
    if (stage < 0 && !p.completion_year) return "";
    var labels = ["timeline_planning", "timeline_permit", "timeline_marketing", "timeline_construction", "timeline_handover"];
    var current = Math.max(0, Math.min(4, stage));
    return '<section class="nl-wrap nl-progress" aria-labelledby="nl-progress-title">' +
      '<div class="nl-progress__head"><div><span class="nl-eyebrow">' + esc(t("timeline_eyebrow")) + '</span><h2 id="nl-progress-title">' + esc(t("timeline_title")) + '</h2></div>' +
      (p.completion_year ? '<div class="nl-progress__delivery"><span>' + esc(t("handover_label")) + '</span><strong>' + esc(t("handover_estimated", { n: p.completion_year })) + '</strong></div>' : "") + '</div>' +
      '<ol class="nl-progress__steps" style="--nl-progress:' + (current * 25) + '%">' + labels.map(function (key, index) {
        var cls = index < current ? "is-done" : (index === current ? "is-current" : "");
        return '<li class="' + cls + '"><i aria-hidden="true"></i><span>' + esc(t(key)) + '</span></li>';
      }).join("") + '</ol>' +
      '<p class="nl-progress__note">' + esc(t("timeline_note")) + '</p></section>';
  }

  /* block 3 + 4 - theater (3D) and facade backup */
  function theater() {
    var p = project();
    var hots = units().map(function (u) {
      var pos = unitPos(u), cls = "nl-hot" + (u.status === "reserved" ? " nl-hot--reserved" : u.status === "sold" ? " nl-hot--sold" : "") + (u.recommended ? " nl-hot--rec" : "");
      return '<button slot="hotspot-' + esc(u.id) + '" data-position="' + pos.pos + '" data-normal="' + pos.nrm + '" class="' + cls + '" data-act="select" data-id="' + esc(u.id) + '" aria-label="' + esc(unitTitleAria(u)) + '">' + esc(u.floor) + "</button>";
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
      return '<button class="' + cls + '" data-act="select" data-id="' + esc(u.id) + '" style="left:' + u.stage_x + "%;top:" + u.stage_y + "%;width:" + u.stage_w + "%;height:" + u.stage_h + '%" aria-label="' + esc(unitTitleAria(u)) + '"><b>' + esc(u.label) + "</b><span>" + esc(roomsLabel(u.rooms)) + "</span></button>";
    }).join("");
    var facadeInner = "";
    if (p.facade_image) {
      facadeInner = '<div class="nl-facade__frame" style="background-image:url(' + esc(p.facade_image) + ')">' + fsq + "</div>";
    } else if (p.facade_concept_image) {
      facadeInner = '<div class="nl-facade__frame nl-facade__concept" style="background-image:url(' + esc(p.facade_concept_image) + ')"><div class="nl-facade__notice"><span>' + esc(t("concept_badge")) + "</span><strong>" + esc(t("facade_missing_title")) + "</strong><p>" + esc(t("facade_concept_note")) + "</p></div></div>";
    } else {
      facadeInner = '<div class="nl-facade__frame nl-facade__missing" role="status"><strong>' + esc(t("facade_missing_title")) + "</strong><p>" + esc(t("facade_missing_text")) + "</p></div>";
    }

    return '<div class="nl-theater">' +
      '<div class="nl-theater__top"><div class="nl-theater__title"><span class="e">' + esc(t("theater_eyebrow")) + "</span><h2>" + esc(t("theater_title")) + "</h2></div>" +
        (p.model_glb && SR.config.studio !== "off" ? '<button class="nl-cotour-btn nl-studio-launch" data-act="studio-any" type="button">' + esc(t("nlst_open")) + "</button>" : "") +
        (p.model_glb ? '<button class="nl-cotour-btn" data-act="cotour" type="button">' + esc(t("cotour_start")) + "</button>" : "") +
        (p.model_glb ? '<div class="nl-filters nl-tabs nl-filters--stage nl-light" role="group" aria-label="light">' + ["day","dusk","night"].map(function (m) {
          return '<button data-act="light" data-id="' + m + '" aria-pressed="' + (state.light === m) + '">' + esc(t("light_" + m)) + "</button>";
        }).join("") + "</div>" : "") +
        (p.model_glb ? '<div class="nl-filters nl-tabs nl-filters--stage" role="group" aria-label="filter">' + ["all","available","3","4","5"].map(function (f) {
          return '<button data-act="filter" data-id="' + f + '" aria-pressed="' + (state.filter === f) + '">' + esc(t("filter_" + f)) + "</button>";
        }).join("") + "</div>" : "") +
        (p.model_glb ? '<div class="nl-toggle" role="group" aria-label="view"><button data-act="view" data-id="3d" aria-pressed="true">' + esc(t("view_3d")) + '</button><button data-act="view" data-id="facade" aria-pressed="false">' + esc(t("view_facade")) + "</button></div>" : "") + "</div>" +
      '<div class="nl-stagewrap">' +
        (p.model_glb ? '<model-viewer id="nl-mv" class="nl-stage" src="' + esc(p.model_glb) + '" loading="lazy" reveal="auto" camera-controls auto-rotate auto-rotate-delay="2400" rotation-per-second="8deg" interaction-prompt="basic" environment-image="neutral" exposure="1.02" shadow-intensity="0.55" shadow-softness="1" camera-orbit="' + esc(p.default_orbit) + '" camera-target="' + esc(p.default_target) + '" min-camera-orbit="-Infinity 56deg auto" max-camera-orbit="Infinity 82deg auto" min-field-of-view="16deg" max-field-of-view="68deg" touch-action="pan-y">' + hots + "</model-viewer>" : "") +
        '<div class="nl-poster" id="nl-poster" style="background-image:url(' + esc(p.model_poster) + ')"></div>' +
        '<div class="nl-spinner" id="nl-spin"><i></i>' + esc(t("loading_model")) + "</div>" +
        (p.model_glb && p.model_generic ? '<div class="nl-generic-chip">' + esc(t("generic_model")) + "</div>" : "") +
        '<div class="nlp3d-model-error nl-model-error" id="nl-model-error" role="status" aria-live="polite" hidden>' + esc(t("model_error")) + "</div>" +
        orientPins +
        '<div class="nl-legend"><span><span class="nl-dot s-available"></span>' + esc(t("legend_available")) + '</span><span><span class="nl-dot s-reserved"></span>' + esc(t("legend_reserved")) + '</span><span><span class="nl-dot s-sold"></span>' + esc(t("legend_sold")) + "</span></div>" +
        '<div class="nl-facade" id="nl-facade">' + facadeInner + "</div>" +
        '<div class="nl-scrim" id="nl-scrim"></div>' +
        (p.model_glb ? '<button class="nl-resetview" id="nl-resetview" data-act="resetview" type="button" hidden>' + esc(t("reset_view")) + "</button>" : "") +
        panel() +
      "</div>" +
    "</div>";
  }
  function unitTitleAria(u) { return roomsLabel(u.rooms) + ", " + t("floor_label", { n: u.floor }) + ", " + dirLabel(u.dir) + ", " + statusLabel(u.status); }

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
        '<h3 class="nl-panel__title" style="margin-top:8px">' + esc(roomsLabel(u.rooms)) + '</h3><div class="nl-muted" style="color:var(--theater-sub);font-size:13px;margin-top:3px">' + esc(projName()) + " · " + esc(dirLabel(u.dir)) + " · " + esc(u.label) + "</div></div>" +
        '<div class="nl-panel__floor"><div style="color:#d8c79a;font-size:12px;font-weight:600">' + esc(t("panel_floor")) + '</div><b>' + esc(u.floor) + "</b>" +
        '<button class="nl-panel__close" data-act="close" aria-label="' + esc(t("btn_close")) + '">' + svg("close", 16) + "</button></div></div>" +
      '<div class="nl-grid2">' +
        stat(t("panel_rooms"), u.rooms) + stat(t("panel_sqm"), u.sqm + " " + t("sqm_unit")) +
        stat(t("panel_balcony"), u.balcony ? (u.balcony + " " + t("sqm_unit")) : "-") + stat(t("panel_view"), viewText(u) || dirLabel(u.dir)) +
      "</div>" + sunLine(u) + scarcityLine(u) + mortgageStrip(u) +
      '<div class="nl-tabs" role="tablist">' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="plan" aria-selected="' + (state.tab === "plan") + '">' + esc(t("tab_plan")) + '</button>' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="view" aria-selected="' + (state.tab === "view") + '">' + esc(t("tab_view")) + '</button>' +
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
      '<button class="nl-btn nl-btn--accent nl-btn--block" style="margin-top:9px" data-act="scroll" data-id="inquiry">' + esc(t("btn_inquire")) + " · " + esc(t("unit_short", { label: u.label, floor: u.floor })) + "</button>";
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
    var msg = projName() + " · " + t("unit_short", { label: u.label, floor: u.floor }) + " · " + roomsLabel(u.rooms) + "\n" + url;
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
            '<span class="nl-winstage__meta">' + esc(t("floor_label", { n: u.floor })) + " \u00B7 " + esc(dirLabel(u.dir)) + "</span>" +
            '<button class="nl-winstage__turn" data-act="winlook" data-id="' + esc(u.id) + '" data-d="30" aria-label="' + esc(t("winview_turn_right")) + '">&#8635;</button>' +
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

  /* recently viewed (cross-project, localStorage): the multi-session buyer
     resumes in one tap. Current selection is filtered out at render time. */
  function recentStrip() {
    var rec = load("nl_recent", []).filter(function (r) { return r && r.u && !(r.p === state.projectKey && r.u === state.unitId); }).slice(0, 5);
    if (!rec.length) return "";
    var items = rec.map(function (r) {
      var label = esc(r.n || "") + " · " + esc(t("unit_short", { label: r.l, floor: r.f }));
      return r.p === state.projectKey
        ? '<button class="nl-recent__it" data-act="select" data-id="' + esc(r.u) + '" type="button">' + label + "</button>"
        : '<a class="nl-recent__it" href="' + esc(r.url || "#") + '">' + label + "</a>";
    }).join("");
    return '<div class="nl-recent"><span class="nl-recent__t">' + esc(t("recent_title")) + "</span>" + items + "</div>";
  }
  function recordRecent(u) {
    try {
      var rec = load("nl_recent", []).filter(function (r) { return r && !(r.p === state.projectKey && r.u === u.id); });
      rec.unshift({ p: state.projectKey, u: u.id, l: u.label, f: u.floor, r: u.rooms, n: String(projName()).split(" - ")[0],
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
    return { p: state.projectKey, u: state.unitId || "", o: o, l: state.light, f: state.filter, v: state.view };
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
            if (st.u && st.u !== lastU) { lastU = st.u; selectUnit(st.u, true); }
            if (st.o && st.o !== lastO && mv) { lastO = st.o; mv.cameraOrbit = st.o; }
            if (st.l && st.l !== state.light) { state.light = st.l; applyLight(); }
            if (st.f && st.f !== state.filter) { state.filter = st.f; refresh("inventory"); applyStageFilter(); }
          }).catch(function () {});
        } catch (e) {}
      }, 1600);
    }
  }
  /* SUNSET ENGINE (2026-07-07): day / dusk / night lighting on the model.
     Exposure drop makes the baked emissive windows and storefronts glow;
     a stage tone class shifts the backdrop. Honest: a lighting preview. */
  function applyLight() {
    var mv = document.getElementById("nl-mv");
    var map = { day: ["1.02", "0.55"], dusk: ["0.5", "0.3"], night: ["0.22", "0.12"] };
    var v = map[state.light] || map.day;
    // owner 2026-07-07: exposure alone reads as "nothing changed" - a CSS
    // filter on the viewer makes dusk/night unmistakable at a glance
    var flt = { day: "", dusk: "sepia(.35) saturate(.85) brightness(.8) contrast(1.04)", night: "brightness(.5) saturate(.6) contrast(1.08)" };
    if (mv) { mv.setAttribute("exposure", v[0]); mv.setAttribute("shadow-intensity", v[1]); mv.style.filter = flt[state.light] || ""; }
    var stage = mv && mv.closest(".nl-stagewrap") || mv && mv.parentElement;
    if (stage) {
      stage.classList.toggle("nl-light--dusk", state.light === "dusk");
      stage.classList.toggle("nl-light--night", state.light === "night");
    }
    [].forEach.call(document.querySelectorAll('[data-act="light"]'), function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-id") === state.light));
    });
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
    if (!state.compare.length) return '<div class="nl-compare" id="nl-compare"></div>';
    var top = topsisTop(state.compare);
    var items = state.compare.map(function (id) { var u = unit(id); return u ? '<span class="nl-cmpitem' + (id === top && state.compare.length > 1 ? " is-top" : "") + '">' + (id === top && state.compare.length > 1 ? '<i class="nl-cmptop">★ ' + esc(t("compare_top")) + "</i>" : "") + '<b>' + esc(u.label) + "</b> " + esc(roomsLabel(u.rooms)) + " · " + esc(u.sqm + t("sqm_unit")) + ' <button data-act="compare" data-id="' + esc(id) + '" aria-label="remove">×</button></span>' : ""; }).join("");
    return '<div class="nl-compare is-on" id="nl-compare"><div class="nl-wrap nl-compare__row"><b>' + esc(t("compare_title")) + '</b><div class="nl-compare__items">' + items + '</div><button class="nl-btn nl-btn--sm nl-btn--ghost" data-act="compare-clear" style="color:#cfc8b6;border-color:rgba(242,236,222,.2)">' + esc(t("compare_clear")) + '</button><button class="nl-btn nl-btn--sm nl-btn--accent" data-act="scroll" data-id="inquiry">' + esc(t("compare_inquire")) + "</button></div></div>";
  }

  /* footer */
  function footer() {
    var projLinks = SR.order.map(function (k) { return '<li><a href="' + esc(SR.projects[k].url || ("?project=" + k)) + '">' + esc(t(SR.projects[k].name_key) || SR.projects[k].name || "") + "</a></li>"; }).join("");
    var langLinks = pageLangs().map(function (l) { return '<li><a href="' + esc(langHref(l)) + '" data-act="lang" data-id="' + l + '">' + esc(t("lang_" + l)) + "</a></li>"; }).join("");
    return '<footer class="nl-footer"><div class="nl-wrap"><div class="nl-footer__row">' +
      '<div><a class="nl-brand" href="' + esc(SR.config.home_url || "/") + '"><span class="nl-brand__mark">N</span><span class="nl-brand__name" style="color:#efe7d6">' + esc(t("brand")) + '</span></a><p style="color:#b8b1a2;font-size:14px;margin-top:12px;max-width:34ch">' + esc(t("footer_tagline")) + "</p></div>" +
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
        if (project() && (project().facade_image || project().facade_concept_image)) { setView("facade"); }
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
      if (state.unitId && unit(state.unitId)) selectUnit(state.unitId, true);
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
      if (!ev.detail || ev.detail.source !== "user-interaction") return;
      var map = window.NLPJX_MAP;
      if (!map || typeof mv.getCameraOrbit !== "function") return;
      var now = Date.now(); if (now - last < 120) return; last = now;
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
    var salonA = sqm * 0.40, bedA = bedrooms ? (sqm * 0.42) / bedrooms : 0;
    var k = dirKey(u.dir), wall = "n";
    if (k.indexOf("south") >= 0) wall = "s"; else if (k.indexOf("east") >= 0) wall = "e"; else if (k.indexOf("west") >= 0) wall = "w";
    var out = [{ key: "salon", label: t("fp_salon"), w: +Math.sqrt(salonA * 1.4).toFixed(1), d: +Math.sqrt(salonA / 1.4).toFixed(1), win: wall }];
    out.push({ key: "kitchen", label: t("fp_kitchen"), w: 3.4, d: +Math.max(2.4, sqm * 0.12 / 3.4).toFixed(1), win: "n" });
    for (var i = 1; i <= bedrooms; i++) {
      var isMamad = i === bedrooms;
      out.push({ key: "bed" + i, label: isMamad ? t("fp_mamad") : (i === 1 ? t("fp_master") : t("fp_bed") + " " + i),
        w: +Math.sqrt(bedA * 1.15).toFixed(1), d: +Math.sqrt(bedA / 1.15).toFixed(1),
        win: isMamad ? "" : (wall === "n" ? "e" : wall) });
    }
    var bal = parseInt(u.balcony, 10) || 0;
    if (bal > 0) out.push({ key: "balcony", label: t("fp_balcony") + " (" + bal + " " + t("sqm_unit") + ")", w: +Math.sqrt(bal * 2.2).toFixed(1), d: +Math.sqrt(bal / 2.2).toFixed(1), win: "open" });
    return out;
  }
  function fpMarkup(u) {
    return '<div class="nlifp" data-rooms="' + esc(JSON.stringify(fpRooms(u))) + '">' +
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
      var pitch = Math.max(35, Math.min(96, 86 + (vert || 0)));
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
      var map = new gl.Map({ container: host, style: "mapbox://styles/mapbox/satellite-streets-v12",
        center: [Number(project().geo.lng), Number(project().geo.lat)], zoom: 15,
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
    else if (act === "select") selectUnit(id, false, node.classList.contains("nl-ucard"));
    else if (act === "close") closePanel();
    else if (act === "view") setView(id);
    else if (act === "tab") setTab(id);
    else if (act === "filter") { state.filter = id; refresh("inventory"); applyStageFilter(); }
    else if (act === "light") { state.light = id; applyLight(); }
    else if (act === "cotour") { cotourStart(); }
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
  ROOT.addEventListener("keydown", function (e) {
    var node = e.target.closest('[role="button"][data-act="select"]');
    if (node && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); selectUnit(node.dataset.id, false, node.classList.contains("nl-ucard")); }
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

  function selectUnit(id, instant, focusStage) {
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
    if (focusStage) { setTimeout(function () { scrollTo("building"); }, 20); }
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
  function closePanel() {
    state.unitId = null;
    var p = document.getElementById("nl-panel"); if (p) p.classList.remove("is-open");
    var s = document.getElementById("nl-scrim"); if (s) s.classList.remove("is-on");
    document.querySelectorAll(".is-active").forEach(function (n) { n.classList.remove("is-active"); });
    var mv = document.getElementById("nl-mv"); if (mv) { try { mv.interpolationDecay = 50; mv.fieldOfView = "auto"; mv.cameraOrbit = project().default_orbit; mv.cameraTarget = project().default_target; } catch (e) {} }
    updateFormCtx(); updateSticky(); deeplink();
  }
  function toggleFav(id) {
    var i = state.favs.indexOf(id); if (i >= 0) state.favs.splice(i, 1); else state.favs.push(id);
    save("nl_favs", state.favs);
    if (state.filter === "favs" && !state.favs.length) state.filter = "all";
    refresh("inventory"); // hearts, the saved chip and its count stay truthful
    if (state.unitId === id) { var body = document.getElementById("nl-panel-body"); if (body) body.innerHTML = panelBody(unit(id)); }
  }
  function toggleCompare(id) {
    var i = state.compare.indexOf(id);
    if (i >= 0) state.compare.splice(i, 1);
    else { if (state.compare.length >= 3) state.compare.shift(); state.compare.push(id); }
    refreshCompare();
    if (state.unitId === id) { var body = document.getElementById("nl-panel-body"); if (body) body.innerHTML = panelBody(unit(id)); }
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
    if (p && p.lang_urls && p.lang_urls[l]) { location.href = p.lang_urls[l]; return; }
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
    ctx.innerHTML = '<span class="d"></span>' + (u ? esc(t("form_unit_ctx", { label: u.label, floor: u.floor, rooms: u.rooms })) : esc(t("form_no_unit")));
  }
  function updateSticky() {
    var c = document.getElementById("nl-stickyctx"); if (!c) return;
    var u = unit(state.unitId); c.textContent = u ? (" · " + t("unit_short", { label: u.label, floor: u.floor })) : "";
    var wa = document.getElementById("nl-wa");
    if (wa && SR.config.whatsapp) {
      var msg = (u ? t("form_unit_ctx", { label: u.label, floor: u.floor, rooms: u.rooms }) : t("form_no_unit")) + " · " + projName();
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
      message: u ? t("form_unit_ctx", { label: u.label, floor: u.floor, rooms: u.rooms }) : t("form_no_unit")
    };
    var btn = f.querySelector('button[type="submit"]'); btn.disabled = true; btn.textContent = t("form_submitting");
    var done = function () { show(msg, "ok", t("form_success")); f.reset(); btn.disabled = false; btn.textContent = t("form_submit"); updateFormCtx(); };
    var ep = SR.config.lead_endpoint;
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
