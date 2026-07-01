/* ============================================================================
   NadLan Showroom — ENGINE (vanilla, data-driven)
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
    view: "3d", tab: "plan", filter: "all",
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
  function dirLabel(d) { return KNOWN_DIRS[d] ? t("dir_" + d) : (d || ""); }
  function statusLabel(s) { return t("status_" + s); }
  function roomsLabel(n) { return t("rooms_label", { n: n }); }
  function viewText(u) { return u.view_key ? t(u.view_key) : ""; }
  function area() { return (SR.areas && SR.areas[project().area]) || { map: { pins: [], project_pin: { x: 50, y: 50 }, coast_x: 16 }, spoke_groups: [], stats: [] }; }
  function spoke(id) { return (SR.spokes && SR.spokes[id]) || null; }

  function load(k, d) { try { return JSON.parse(localStorage.getItem(k)) || d; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
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
    var fh = parseFloat(project().floor_height_m) || 3.05, half = 13.2;
    var v = DIRV[u.dir] || [-1, 0], y = u.floor * fh + fh * 0.4;
    return { pos: (v[0] * half).toFixed(2) + "m " + y.toFixed(2) + "m " + (v[1] * half).toFixed(2) + "m", nrm: v[0] + "m 0m " + v[1] + "m" };
  }
  function orbitRadius(orbit, r) { var p = String(orbit).trim().split(/\s+/); if (p.length >= 3) p[2] = r + "m"; return p.join(" "); }

  /* =====================================================================
     RENDER
  ===================================================================== */
  function render() {
    document.documentElement.lang = state.lang;
    document.documentElement.dir = isRTL() ? "rtl" : "ltr";
    document.title = (state.page === "home" ? t("home_gallery_title") : (projName() + " · " + t("brand_sub")));
    ROOT.className = "nl-app";
    ROOT.innerHTML = (state.page === "home")
      ? header() + homeMain() + footer()
      : header() + secNav() + projectMain() + footer() + sticky() + compareTray();
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
      '<a class="nl-brand" href="home.html"><span class="nl-brand__mark">N</span><span><span class="nl-brand__name">' + esc(t("brand")) + '</span> <span class="nl-brand__sub">' + esc(t("brand_sub")) + "</span></span></a>" +
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

  /* block 2 — hero */
  function hero() {
    var p = project(), avail = units().filter(function (u) { return u.status === "available"; }).length;
    var hi = units().reduce(function (m, u) { return Math.max(m, u.floor); }, 0);
    return '<div class="nl-hero">' +
      "<div>" +
        '<span class="nl-eyebrow">' + esc(t("hero_eyebrow")) + "</span>" +
        '<hr class="nl-rule">' +
        '<h1 class="nl-hero__h1">' + esc(projName()) + "</h1>" +
        '<p class="nl-lede" style="margin-top:14px">' + esc(content("tagline")) + "</p>" +
        '<div class="nl-hero__cta"><button class="nl-btn nl-btn--accent" data-act="scroll" data-id="inquiry">' + esc(t("hero_cta_primary")) + '</button><button class="nl-btn nl-btn--ghost" data-act="scroll" data-id="inventory">' + esc(t("hero_cta_secondary")) + "</button></div>" +
        '<div class="nl-hero__facts">' +
          '<div><div class="nl-fact__n">' + esc(p.floors) + '</div><div class="nl-fact__l">' + esc(t("fact_floors")) + "</div></div>" +
          '<div><div class="nl-fact__n">' + esc(units().length) + '</div><div class="nl-fact__l">' + esc(t("fact_homes")) + "</div></div>" +
          '<div><div class="nl-fact__n">' + esc(hi) + '</div><div class="nl-fact__l">' + esc(t("fact_from_floor")) + "</div></div>" +
        "</div>" +
      "</div>" +
      '<div class="nl-hero__media"><img src="' + esc(p.model_poster) + '" alt="' + esc(projName()) + '" loading="eager">' + (SR.config.demo ? '<span class="nl-badge nl-badge--demo nl-hero__badge">' + esc(t("demo_badge")) + "</span>" : "") + "</div>" +
    "</div>";
  }

  /* block 3 + 4 — theater (3D) and facade backup */
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
      return '<button class="' + cls + '" data-act="select" data-id="' + esc(u.id) + '" style="inset-inline-start:' + u.stage_x + "%;inset-block-start:" + u.stage_y + "%;width:" + u.stage_w + "%;height:" + u.stage_h + '%" aria-label="' + esc(unitTitleAria(u)) + '"><b>' + esc(u.label) + "</b><span>" + esc(roomsLabel(u.rooms)) + "</span></button>";
    }).join("");
    var facadeBg = p.facade_image ? ' style="background-image:url(' + esc(p.facade_image) + ')"' : "";

    return '<div class="nl-theater">' +
      '<div class="nl-theater__top"><div class="nl-theater__title"><span class="e">' + esc(t("theater_eyebrow")) + "</span><h2>" + esc(t("theater_title")) + "</h2></div>" +
        (p.model_glb ? '<div class="nl-toggle" role="group" aria-label="view"><button data-act="view" data-id="3d" aria-pressed="true">' + esc(t("view_3d")) + '</button><button data-act="view" data-id="facade" aria-pressed="false">' + esc(t("view_facade")) + "</button></div>" : "") + "</div>" +
      '<div class="nl-stagewrap">' +
        (p.model_glb ? '<model-viewer id="nl-mv" class="nl-stage" src="' + esc(p.model_glb) + '" loading="lazy" reveal="interaction" camera-controls auto-rotate auto-rotate-delay="800" rotation-per-second="14deg" interaction-prompt="basic" environment-image="neutral" exposure="1.02" shadow-intensity="0.55" shadow-softness="1" camera-orbit="' + esc(p.default_orbit) + '" camera-target="' + esc(p.default_target) + '" min-camera-orbit="auto 48deg auto" max-camera-orbit="auto 86deg auto" min-field-of-view="16deg" max-field-of-view="44deg" touch-action="pan-y">' + hots + "</model-viewer>" : "") +
        '<div class="nl-poster" id="nl-poster" style="background-image:url(' + esc(p.model_poster) + ')"></div>' +
        '<div class="nl-spinner" id="nl-spin"><i></i>' + esc(t("loading_model")) + "</div>" +
        orientPins +
        '<div class="nl-legend"><span><span class="nl-dot s-available"></span>' + esc(t("legend_available")) + '</span><span><span class="nl-dot s-reserved"></span>' + esc(t("legend_reserved")) + '</span><span><span class="nl-dot s-sold"></span>' + esc(t("legend_sold")) + "</span></div>" +
        '<div class="nl-facade" id="nl-facade"><div class="nl-facade__frame"' + facadeBg + ">" + fsq + "</div></div>" +
        '<div class="nl-scrim" id="nl-scrim"></div>' +
        panel() +
      "</div>" +
    "</div>";
  }
  function unitTitleAria(u) { return roomsLabel(u.rooms) + ", " + t("floor_label", { n: u.floor }) + ", " + dirLabel(u.dir) + ", " + statusLabel(u.status); }

  /* block 5 — slide-out panel (filled on select) */
  function panel() {
    return '<aside class="nl-panel" id="nl-panel" aria-live="polite"><div class="nl-panel__scroll" id="nl-panel-body">' + panelEmpty() + "</div></aside>";
  }
  function panelEmpty() {
    return '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;gap:10px;color:var(--theater-sub);padding:30px">' + svg("grid", 26) + "<p>" + esc(t("panel_prompt")) + "</p></div>";
  }
  function panelBody(u) {
    var fav = state.favs.indexOf(u.id) >= 0, cmp = state.compare.indexOf(u.id) >= 0;
    return '<div class="nl-panel__head"><div><span class="nl-badge" style="background:rgba(255,255,255,.08);color:#fff"><span class="nl-dot s-' + esc(u.status) + '"></span>' + esc(statusLabel(u.status)) + '</span>' +
        '<h3 class="nl-panel__title" style="margin-top:8px">' + esc(roomsLabel(u.rooms)) + '</h3><div class="nl-muted" style="color:var(--theater-sub);font-size:13px;margin-top:3px">' + esc(projName()) + " · " + esc(dirLabel(u.dir)) + " · " + esc(u.label) + "</div></div>" +
        '<div class="nl-panel__floor"><div style="color:#d8c79a;font-size:12px;font-weight:600">' + esc(t("panel_floor")) + '</div><b>' + esc(u.floor) + "</b>" +
        '<button class="nl-panel__close" data-act="close" aria-label="' + esc(t("btn_close")) + '">' + svg("close", 16) + "</button></div></div>" +
      '<div class="nl-grid2">' +
        stat(t("panel_rooms"), u.rooms) + stat(t("panel_sqm"), u.sqm + " " + t("sqm_unit")) +
        stat(t("panel_balcony"), u.balcony ? (u.balcony + " " + t("sqm_unit")) : "—") + stat(t("panel_view"), viewText(u) || dirLabel(u.dir)) +
      "</div>" +
      '<div class="nl-tabs" role="tablist">' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="plan" aria-selected="' + (state.tab === "plan") + '">' + esc(t("tab_plan")) + '</button>' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="view" aria-selected="' + (state.tab === "view") + '">' + esc(t("tab_view")) + '</button>' +
        '<button class="nl-tab" role="tab" data-act="tab" data-id="tour" aria-selected="' + (state.tab === "tour") + '">' + esc(t("tab_tour")) + "</button></div>" +
      '<div class="nl-tabpane">' + tabPane(u) + "</div>" +
      '<div class="nl-panel__actions">' +
        '<button class="nl-iconbtn' + (fav ? " is-on" : "") + '" data-act="fav" data-id="' + esc(u.id) + '">' + svg("heart", 16) + esc(fav ? t("btn_saved") : t("btn_save")) + "</button>" +
        '<button class="nl-iconbtn' + (cmp ? " is-on" : "") + '" data-act="compare" data-id="' + esc(u.id) + '">' + svg("scale", 16) + esc(cmp ? t("btn_compared") : t("btn_compare")) + "</button>" +
        '<button class="nl-iconbtn" data-act="share" data-id="' + esc(u.id) + '">' + svg("share", 16) + esc(t("btn_share")) + "</button>" +
      "</div>" +
      '<button class="nl-btn nl-btn--accent nl-btn--block" style="margin-top:14px" data-act="scroll" data-id="inquiry">' + esc(t("btn_inquire")) + " · " + esc(t("unit_short", { label: u.label, floor: u.floor })) + "</button>";
  }
  function stat(k, v) { return '<div class="nl-stat"><div class="k">' + esc(k) + '</div><div class="v">' + esc(v) + "</div></div>"; }
  function tabPane(u) {
    if (state.tab === "plan") return u.plan ? '<img src="' + esc(u.plan) + '" alt="' + esc(t("tab_plan")) + '">' : "<p>" + esc(t("plan_coming")) + "</p>";
    if (state.tab === "view") return u.interior_url ? '<img src="' + esc(u.interior_url) + '" alt="">' : "<p>" + esc(t("view_coming")) + "</p>";
    return "<p>" + esc(t("tour_coming")) + "</p>";
  }

  /* block 6 — inventory */
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
    var chips = ["all", "available", "3", "4", "5"].map(function (f) {
      return '<button class="nl-chip" data-act="filter" data-id="' + f + '" aria-pressed="' + (state.filter === f) + '">' + esc(t("filter_" + f)) + "</button>";
    }).join("");
    return '<div class="nl-invhead"><div><span class="nl-eyebrow">' + esc(t("inventory_title")) + '</span><hr class="nl-rule"><p class="nl-muted" style="max-width:46ch">' + esc(t("inventory_sub")) + '</p></div><div class="nl-filters">' + chips + "</div></div>" +
      '<div class="nl-invgrid">' + cards + "</div>" +
      '<div class="nl-muted" style="margin-top:14px;font-size:13px">' + esc(t("results_count", { n: list.length })) + "</div>";
  }
  function filtered() {
    return units().filter(function (u) {
      if (state.filter === "all") return true;
      if (state.filter === "available") return u.status === "available";
      return String(u.rooms) === state.filter;
    });
  }

  /* block 6.5 — price + comps (PR5). Data-driven, honest: range + non-binding
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

    var big = totals.length ? (money(loT) + " – " + money(hiT))
                            : (money(loP) + " – " + money(hiP) + " " + t("per_sqm_short"));
    var chips = "";
    if (loP && hiP) { chips += '<span class="nl-pchip">' + esc(money(loP) + " – " + money(hiP) + " " + t("per_sqm_short")) + "</span>"; }
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

  /* block 8 — the complete world (map + spokes + stats + nearby) */
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

  /* block 7 — media + interior tour (PR6). Interior tour lazy-loads on click only;
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
    if (p.tour_url) {
      return top + '<div class="nl-interior__stage" data-tour-url="' + esc(p.tour_url) + '"><button class="nl-btn nl-btn--gold" data-act="loadtour">' + esc(t("tour_open")) + '</button></div><p class="nl-interior__note">' + esc(t("tour_lazy_hint")) + "</p></div>";
    }
    if (p.interior_panoramas && p.interior_panoramas.length) {
      return top + '<div class="nl-interior__stage" data-pano="' + esc(JSON.stringify(p.interior_panoramas)) + '"><button class="nl-btn nl-btn--gold" data-act="loadpano">' + esc(t("tour_open_pano")) + '</button></div><p class="nl-interior__note">' + esc(t("tour_lazy_hint")) + "</p></div>";
    }
    return top + '<div class="nl-empty">' + esc(t("tour_pending")) + "</div></div>";
  }
  function loadTour(node) {
    var stage = node.closest(".nl-interior__stage"); if (!stage) return;
    var url = stage.getAttribute("data-tour-url"); if (!url) return;
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

  /* block 9 — investor */
  function investor() {
    var pts = [["shield", "investor_pt_process"], ["scale", "investor_pt_legal"], ["globe", "investor_pt_finance"]];
    return '<div class="nl-card--dark nl-card" style="padding:clamp(22px,4vw,40px)"><div style="display:grid;grid-template-columns:1fr 1.2fr;gap:28px;align-items:center" class="nl-investorgrid">' +
      '<div><span class="nl-eyebrow" style="color:#e9d9a9">' + esc(t("seo_eyebrow")) + '</span><h2 style="color:#fff;margin-top:8px">' + esc(t("investor_title")) + '</h2><p style="color:#d3ccbd;margin-top:10px">' + esc(t("investor_sub")) + '</p><button class="nl-btn nl-btn--gold" style="margin-top:18px" data-act="scroll" data-id="inquiry">' + esc(t("investor_cta")) + "</button></div>" +
      '<div class="nl-cards" style="grid-template-columns:1fr">' + pts.map(function (p) { return '<div style="display:flex;gap:12px;align-items:flex-start"><span style="color:#e9d9a9;flex:none">' + svg(p[0], 20) + "</span><b style=\"color:#fff;font-weight:600\">" + esc(t(p[1])) + "</b></div>"; }).join("") + "</div>" +
      "</div></div>";
  }

  /* block 10 — SEO body (placeholder content from data) */
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

  /* block 11 — inquiry (money moment) */
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

  /* block 12 — disclaimer */
  function disclaimer() {
    return '<div class="nl-disclaimer"><b>' + esc(t("disclaimer_title")) + "</b><p>" + esc(t("disclaimer_text")) + "</p></div>";
  }

  /* sticky inquire + whatsapp */
  function sticky() {
    var wa = SR.config.whatsapp ? '<a class="nl-sticky__wa" id="nl-wa" href="#" target="_blank" rel="noopener">' + svg("wa", 16) + esc(t("whatsapp_cta")) + "</a>" : "";
    return '<div class="nl-sticky" id="nl-sticky"><button class="nl-sticky__main" data-act="scroll" data-id="inquiry"><span>' + svg("phone", 16) + '</span><span>' + esc(t("sticky_cta")) + '<span class="nl-sticky__ctx" id="nl-stickyctx"></span></span></button>' + wa + "</div>";
  }

  /* compare tray */
  function compareTray() {
    if (!state.compare.length) return '<div class="nl-compare" id="nl-compare"></div>';
    var items = state.compare.map(function (id) { var u = unit(id); return u ? '<span class="nl-cmpitem"><b>' + esc(u.label) + "</b> " + esc(roomsLabel(u.rooms)) + " · " + esc(u.sqm + t("sqm_unit")) + ' <button data-act="compare" data-id="' + esc(id) + '" aria-label="remove">×</button></span>' : ""; }).join("");
    return '<div class="nl-compare is-on" id="nl-compare"><div class="nl-wrap nl-compare__row"><b>' + esc(t("compare_title")) + '</b><div class="nl-compare__items">' + items + '</div><button class="nl-btn nl-btn--sm nl-btn--ghost" data-act="compare-clear" style="color:#cfc8b6;border-color:rgba(242,236,222,.2)">' + esc(t("compare_clear")) + '</button><button class="nl-btn nl-btn--sm nl-btn--accent" data-act="scroll" data-id="inquiry">' + esc(t("compare_inquire")) + "</button></div></div>";
  }

  /* footer */
  function footer() {
    var projLinks = SR.order.map(function (k) { return '<li><a href="project.html?project=' + esc(k) + '">' + esc(t(SR.projects[k].name_key)) + "</a></li>"; }).join("");
    var langLinks = pageLangs().map(function (l) { return '<li><a href="' + esc(langHref(l)) + '" data-act="lang" data-id="' + l + '">' + esc(t("lang_" + l)) + "</a></li>"; }).join("");
    return '<footer class="nl-footer"><div class="nl-wrap"><div class="nl-footer__row">' +
      '<div><a class="nl-brand" href="home.html"><span class="nl-brand__mark">N</span><span class="nl-brand__name" style="color:#efe7d6">' + esc(t("brand")) + '</span></a><p style="color:#b8b1a2;font-size:14px;margin-top:12px;max-width:34ch">' + esc(t("footer_tagline")) + "</p></div>" +
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
      var poster = document.getElementById("nl-poster"), spin = document.getElementById("nl-spin");
      var reveal = function () { state.mvReady = true; if (poster) poster.classList.add("is-hidden"); if (spin) spin.style.opacity = "0"; };
      if (mv.loaded) reveal(); else mv.addEventListener("load", reveal, { once: true });
      // safety: never leave poster forever if load is delayed
      setTimeout(function () { if (!state.mvReady && mv.modelIsVisible) reveal(); }, 6000);
    }
    if (state.page === "project") {
      updateFormCtx(); updateSticky();
      if (state.unitId && unit(state.unitId)) selectUnit(state.unitId, true);
      var form = document.getElementById("nl-form");
      if (form) form.addEventListener("submit", onSubmit);
      window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
      setupSpy();
    }
  }

  ROOT.addEventListener("click", function (e) {
    var node = e.target.closest("[data-act]"); if (!node) return;
    var act = node.dataset.act, id = node.dataset.id;
    if (act === "lang") { e.preventDefault(); switchLang(id); }
    else if (act === "select") selectUnit(id);
    else if (act === "close") closePanel();
    else if (act === "view") setView(id);
    else if (act === "tab") setTab(id);
    else if (act === "filter") { state.filter = id; refresh("inventory"); }
    else if (act === "fav") { e.stopPropagation(); toggleFav(id); }
    else if (act === "compare") { e.stopPropagation(); toggleCompare(id); }
    else if (act === "compare-clear") { state.compare = []; refreshCompare(); }
    else if (act === "share") share(id);
    else if (act === "scroll") { e.preventDefault(); scrollTo(id); }
    else if (act === "loadtour") loadTour(node);
    else if (act === "loadpano") loadPano(node);
    else if (act === "pin") highlightPin(node);
  });
  ROOT.addEventListener("keydown", function (e) {
    var node = e.target.closest('[role="button"][data-act="select"]');
    if (node && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); selectUnit(node.dataset.id); }
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
  }

  function selectUnit(id, instant) {
    var u = unit(id); if (!u) return;
    var prev = state.unitId; state.unitId = id; state.tab = "plan";
    // panel
    var body = document.getElementById("nl-panel-body"), panelEl = document.getElementById("nl-panel");
    if (body) body.innerHTML = panelBody(u);
    if (panelEl) panelEl.classList.add("is-open");
    // active markers
    document.querySelectorAll(".nl-hot,.nl-fsq,.nl-ucard").forEach(function (n) { n.classList.toggle("is-active", n.dataset.id === id); });
    // scrim + spotlight origin
    var scrim = document.getElementById("nl-scrim");
    var srcEl = document.querySelector('.nl-hot[data-id="' + cssesc(id) + '"]') || document.querySelector('.nl-fsq[data-id="' + cssesc(id) + '"]');
    if (scrim) {
      var wrap = scrim.parentElement.getBoundingClientRect();
      if (srcEl) { var r = srcEl.getBoundingClientRect(); scrim.style.setProperty("--sx", ((r.left + r.width / 2 - wrap.left) / wrap.width * 100) + "%"); scrim.style.setProperty("--sy", ((r.top + r.height / 2 - wrap.top) / wrap.height * 100) + "%"); }
      scrim.classList.add("is-on");
    }
    // camera fly
    var mv = document.getElementById("nl-mv");
    if (mv && u.camera_orbit) { try { mv.cameraOrbit = orbitRadius(u.camera_orbit, Math.round((project().frame_radius_m || 150) * 0.66)); mv.cameraTarget = unitPos(u).pos; } catch (e) {} }
    // cinematic fly chip
    if (!instant && srcEl) flyChip(srcEl, u);
    // context + deep link
    updateFormCtx(); updateSticky();
    deeplink();
  }
  function flyChip(srcEl, u) {
    var panelEl = document.getElementById("nl-panel"); if (!panelEl) return;
    var s = srcEl.getBoundingClientRect();
    var chip = document.createElement("div"); chip.className = "nl-fly"; chip.style.width = "120px"; chip.style.height = "78px";
    chip.innerHTML = "<b>" + esc(u.floor) + "</b><span>" + esc(roomsLabel(u.rooms)) + "</span>";
    document.body.appendChild(chip);
    requestAnimationFrame(function () {
      var head = panelEl.querySelector(".nl-panel__title") || panelEl;
      var d = head.getBoundingClientRect();
      var x0 = s.left + s.width / 2 - 60, y0 = s.top + s.height / 2 - 39;
      var x1 = d.left + d.width / 2 - 60, y1 = d.top - 10;
      chip.style.transform = "translate(" + x0 + "px," + y0 + "px) scale(.5)";
      chip.animate(
        [{ transform: "translate(" + x0 + "px," + y0 + "px) scale(.5)", opacity: 0.2 },
         { transform: "translate(" + ((x0 + x1) / 2) + "px," + (Math.min(y0, y1) - 50) + "px) scale(1.12)", opacity: 1, offset: 0.55 },
         { transform: "translate(" + x1 + "px," + y1 + "px) scale(.7)", opacity: 0 }],
        { duration: 720, easing: "cubic-bezier(.22,.61,.36,1)" }
      ).onfinish = function () { chip.remove(); };
    });
  }
  function closePanel() {
    state.unitId = null;
    var p = document.getElementById("nl-panel"); if (p) p.classList.remove("is-open");
    var s = document.getElementById("nl-scrim"); if (s) s.classList.remove("is-on");
    document.querySelectorAll(".is-active").forEach(function (n) { n.classList.remove("is-active"); });
    var mv = document.getElementById("nl-mv"); if (mv) { try { mv.cameraOrbit = project().default_orbit; mv.cameraTarget = project().default_target; } catch (e) {} }
    updateFormCtx(); updateSticky(); deeplink();
  }
  function toggleFav(id) {
    var i = state.favs.indexOf(id); if (i >= 0) state.favs.splice(i, 1); else state.favs.push(id);
    save("nl_favs", state.favs);
    document.querySelectorAll('.nl-ucard__fav[data-id="' + cssesc(id) + '"]').forEach(function (b) { b.classList.toggle("is-on", state.favs.indexOf(id) >= 0); });
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
  window.NadLanEngine = { render: render, state: state, t: t };
})();
