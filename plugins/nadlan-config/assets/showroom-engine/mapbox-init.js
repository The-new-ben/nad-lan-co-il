/* NadLan showroom - real Mapbox mount.
 * Replaces the stylized .nl-map with a live Mapbox map when a token + coordinates
 * exist. If anything is missing, the map container shows a visible admin-facing
 * error instead of staying empty or silently falling back. */
(function () {
  function SR() { return window.NADLAN_SHOWROOM || {}; }
  function cfg() { return SR().config || {}; }
  function lang() {
    var qs = new URLSearchParams(location.search);
    return qs.get("lang") || cfg().default_lang || document.documentElement.lang || "he";
  }
  function text(key, fallback) {
    var i18n = window.NADLAN_I18N || {}, tables = i18n.langs || {}, chain = [lang()].concat(i18n.fallback || ["en", "he"]);
    for (var i = 0; i < chain.length; i++) {
      var table = tables[chain[i]];
      if (table && table[key]) return table[key];
    }
    return fallback;
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function showError(el, message) {
    if (!el) return;
    el.setAttribute("data-mb", "err");
    el.classList.add("nl-map--error");
    el.innerHTML = '<div class="nl-map-error" role="status" aria-live="polite">' + esc(message) + "</div>";
  }
  function activeProject() {
    var s = SR(), qs = new URLSearchParams(location.search);
    var key = qs.get("project") || (s.config && s.config.default_project);
    return (s.projects && s.projects[key]) || null;
  }
  function center() {
    var p = activeProject();
    if (p && p.geo && Number(p.geo.lat) && Number(p.geo.lng)) {
      return [Number(p.geo.lng), Number(p.geo.lat)];
    }
    return null;
  }
  function nearby() {
    var s = SR(), cur = activeProject(), out = [];
    (s.order || []).forEach(function (k) {
      var pr = s.projects && s.projects[k];
      if (!pr || pr === cur) return;
      if (pr.geo && Number(pr.geo.lat) && Number(pr.geo.lng)) out.push(pr);
    });
    return out;
  }
  function mount(el) {
    if (!el || el.getAttribute("data-mb")) return;
    var token = cfg().mapbox_token, c = center();
    if (!token) { showError(el, text("map_error_missing_token", "Mapbox token missing")); return; }
    if (!c) { showError(el, text("map_error_missing_coords", "חסרות קואורדינטות למפה")); return; }
    if (!window.mapboxgl) { showError(el, text("map_error_library", "מפה לא נטענה")); return; }
    el.setAttribute("data-mb", "1");
    el.classList.remove("nl-map--error");
    var holder = document.createElement("div");
    holder.style.position = "absolute";
    holder.style.inset = "0";
    el.innerHTML = "";
    el.appendChild(holder);
    try {
      mapboxgl.accessToken = token;
      if (mapboxgl.setRTLTextPlugin && !window.__nlRtlPlugin) {
        try {
          mapboxgl.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js", null, true);
          window.__nlRtlPlugin = 1;
        } catch (e) {}
      }
      var map = new mapboxgl.Map({
        container: holder,
        style: "mapbox://styles/mapbox/light-v11",
        center: c,
        zoom: 15.5,
        pitch: 45,
        bearing: -17.6,
        attributionControl: true,
      });

      map.on('style.load', function () {
        if (!map.getSource || !map.getSource('composite') || map.getLayer('add-3d-buildings')) return;
        var layers = map.getStyle().layers;
        var labelLayerId = null;
        for (var i = 0; i < layers.length; i++) {
          if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
            labelLayerId = layers[i].id;
            break;
          }
        }
        map.addLayer({
          'id': 'add-3d-buildings',
          'source': 'composite',
          'source-layer': 'building',
          'filter': ['==', 'extrude', 'true'],
          'type': 'fill-extrusion',
          'minzoom': 15,
          'paint': {
            'fill-extrusion-color': '#aaa',
            'fill-extrusion-height': ['interpolate', ['linear'], ['zoom'], 15, 0, 15.05, ['get', 'height']],
            'fill-extrusion-base': ['interpolate', ['linear'], ['zoom'], 15, 0, 15.05, ['get', 'min_height']],
            'fill-extrusion-opacity': 0.6
          }
        }, labelLayerId);
      });
      map.on("error", function () { showError(el, text("map_error_library", "מפה לא נטענה")); });
      map.addControl(new mapboxgl.NavigationControl({ showCompass: false }), "top-left");
      var cur = activeProject();
      new mapboxgl.Marker({ color: "#9C7A3C" })
        .setLngLat(c)
        .setPopup(new mapboxgl.Popup({ offset: 18 }).setText((cur && cur.name) || ""))
        .addTo(map);
      nearby().forEach(function (pr) {
        new mapboxgl.Marker({ color: "#C2563A" })
          .setLngLat([Number(pr.geo.lng), Number(pr.geo.lat)])
          .setPopup(new mapboxgl.Popup({ offset: 18 }).setHTML('<a href="' + (pr.url || "#") + '" style="font-weight:600;color:#1B1A17;text-decoration:none">' + (pr.name || "") + "</a>"))
          .addTo(map);
      });
      map.on("load", function () { map.resize(); });
    } catch (e) {
      showError(el, text("map_error_library", "מפה לא נטענה"));
      if (window.console) console.warn("nadlan map init failed", e);
    }
  }
  function scan() {
    /* ONE-map doctrine: when the unified POI map (project-experience) is on the
       page, the engine's plain map stands down - the engine hides it and we
       must not boot a hidden Mapbox instance into it. */
    if (document.getElementById("nlpjx-map")) return;
    Array.prototype.forEach.call(document.querySelectorAll(".nl-map"), mount);
  }
  function boot() { setTimeout(scan, 350); }
  if (document.readyState !== "loading") boot();
  else document.addEventListener("DOMContentLoaded", boot);
  var root = document.getElementById("nl-root");
  if (root && window.MutationObserver) {
    new MutationObserver(function () { scan(); }).observe(root, { childList: true, subtree: true });
  }
})();
