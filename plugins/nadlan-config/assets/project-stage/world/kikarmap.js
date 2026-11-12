/* Kikar HaMedina: the area map attached to the showroom, with the beam (HAD-712, Ben 11.11.2026 night: "put the map right next to the
 * showroom, in every language, so people tap and suddenly see the beam ... like the other projects, with many details on the map").
 *
 * The page's own area map (#nlpjx-map: streets and their names, the park, transport, schools, shops, its layer buttons; inc/project-
 * experience.php + assets/arealife/areamap.js) moves to sit right under the showroom (.nlsr) once the showroom is mounted. When the
 * visitor picks a floor and a side (the showroom's nl:facing {tower, floor, bearing}), the same wedge the other projects draw
 * (assets/project-stage/bridge.js showBeam, itself the shared engine's showViewCone, #C2563A) appears at that tower, turned to that
 * bearing, and the map turns so the chosen way is up. Drawn from outside the engine; the engine and the area map are not changed.
 *   window.__nlKikarMap = { data: 'hamedina/details.json url' }  (printed by inc/project-stage.php on the Kikar pages) */
(function () {
  var C = window.__nlKikarMap || {};
  var D = null, cone = null, moved = false, last = null;
  var norm = function (b) { return ((b % 360) + 360) % 360; };
  function data() {
    if (D) return Promise.resolve(D);
    return fetch(C.data).then(function (r) { return r.json(); }).then(function (j) { D = j; return j; }).catch(function () { return null; });
  }
  function areaMap() {
    if (window.NLPJX_MAP) return Promise.resolve(window.NLPJX_MAP);
    return new Promise(function (res) { document.addEventListener('nlpjx:map', function () { res(window.NLPJX_MAP); }, { once: true }); });
  }
  function attach() { // the map right under the showroom, once
    if (moved) return true;
    var sr = document.querySelector('.nlsr'), m = document.getElementById('nlpjx-map');
    if (!sr || !m) return false;
    sr.insertAdjacentElement('afterend', m);
    m.classList.add('nlkm-attached'); moved = true;
    if (window.NLPJX_MAP) setTimeout(function () { try { window.NLPJX_MAP.resize(); } catch (e) {} }, 80);
    return true;
  }
  function towerLngLat(k) {
    var t = D && D.towers && D.towers[k], o = D && D.origin;
    if (!t || !o) return null;
    var lat = o.lat - t.cz / 111320, lng = o.lng + t.cx / (111320 * Math.cos(o.lat * Math.PI / 180));
    return [lng, lat];
  }
  function beam(d) {
    Promise.all([areaMap(), data()]).then(function (r) {
      var map = r[0], gl = window.mapboxgl, ll = towerLngLat(d.tower);
      if (!map || !gl || !ll) return;
      try {
        if (!cone) {
          var el = document.createElement('div'); el.style.pointerEvents = 'none'; el.className = 'nlps-cone';
          el.innerHTML = '<svg width="150" height="150" viewBox="0 0 150 150" style="display:block" aria-hidden="true">'
            + '<defs><linearGradient id="nlkm-cone-g" x1="0" y1="0" x2="0" y2="1">'
            + '<stop offset="0" stop-color="#C2563A" stop-opacity="0"/>'
            + '<stop offset="1" stop-color="#C2563A" stop-opacity="0.55"/></linearGradient></defs>'
            + '<path d="M75 75 L44 8 A78 78 0 0 1 106 8 Z" fill="url(#nlkm-cone-g)" stroke="#C2563A" stroke-opacity="0.35" stroke-width="1"/></svg>';
          cone = new gl.Marker({ element: el, rotationAlignment: 'map', pitchAlignment: 'map', anchor: 'center' });
        }
        cone.setLngLat(ll).setRotation(norm(d.bearing)).addTo(map);
        var rr = norm(d.bearing) * Math.PI / 180, ahead = 450;
        var lat = ll[1] + (ahead * Math.cos(rr)) / 111320, lng = ll[0] + (ahead * Math.sin(rr)) / (111320 * Math.cos(ll[1] * Math.PI / 180));
        map.easeTo({ center: [lng, lat], zoom: 14.3, bearing: norm(d.bearing), pitch: 0, duration: 900 });
      } catch (e) { /* the map is optional */ }
    });
  }
  window.addEventListener('nl:facing', function (e) {
    var d = e.detail || {};
    if (!d.tower || d.bearing == null) return;
    last = d; attach(); beam(d);
  });
  // attach as soon as the showroom is on the page (it mounts after the page loads)
  var tries = 0, iv = setInterval(function () { if (attach() || ++tries > 60) clearInterval(iv); }, 500);
  var st = document.createElement('style'); st.id = 'nlkm-css';
  st.textContent = '#nlpjx-map.nlkm-attached{max-width:1100px;margin:14px auto 28px;padding:0 16px;box-sizing:border-box}';
  document.head.appendChild(st);
})();
