/* Aurelia Sports showroom, round 2 (HAD-810, parent HAD-805; Ben 23.11.2026 night, memory ben-showroom-law-2026-11-23).
 *
 * The standard is the Ashira / Rainbow / DUO flat flow, and the tower is NEVER hidden:
 * 1. THE STAGE (inside the engine's #building, in the place of its 3D theater, which stays behind "סיבוב חופשי"): the photoreal
 *    tower from the promenade, from the pitch and in the pool hall, every balcony tappable through the invisible pick layer
 *    rendered from the same Blender camera. The view "from the sea" is out of this step: there the tower still reads as a box.
 * 2. A TAP ON A FLAT: the flat lights on the facade, a glass volume leaves the facade, turns and flies to the panel BESIDE the
 *    tower (desktop) or UNDER it (phone), where it opens from above into its furnished plan. One tap, a tap skips it, reduced
 *    motion = a fade. The panel then holds at once: the flat plan and the floor plan, rooms, size, floor, direction, the stage
 *    of the project in honest words, the closed-deal medians of the area, the view from that height with the real places
 *    tagged, and the request buttons. No layer over the page, no card inside a card, no inner scrolling.
 * 3. HIS MAP: the site's area map (#nlpjx-map, inc/project-experience.php + assets/arealife/areamap.js, places from the same
 *    source as every project) prints because the page now has its declared-concept location, and the engine adopts it right
 *    under #building. On every flat the fleet's beam (the same wedge as engine.js showViewCone and bridge.js showBeam, drawn
 *    from outside: neither file is touched) turns to where the flat faces, and the places inside it are listed under the stage.
 *    A tap on a place (in the view, in the list) lights it on the map.
 * 4. THE CALL at every stage: "שיחת וידאו עכשיו" pulses on the stage and in the panel; one tap opens the designer's live
 *    LiveKit call for this flat (the owner gets the designer's alert). When nobody is on duty (/room/available says so), the
 *    visitor is told that first and chooses: open the room and wait, or a call back. No date picker, no second call system.
 * Honesty: a declared concept; rooms, sizes per flat and availability are sample data ("דירה לדוגמה"); every picture
 * "הדמיה להמחשה"; no price for any Aurelia flat (the area's real closed deals instead); nothing prints a building total. */
(function () {
  'use strict';
  if (window.NLAS) return;
  var C = window.NLAS_CFG || {};
  var B = C.base || '', V = C.v || '1';
  var A = function (p) { return B + p + (p.indexOf('?') < 0 ? '?' : '&') + 'ver=' + encodeURIComponent(V); };
  var DECL = 'פרויקט קונספטואלי. אינו בבנייה ואינו משווק. הביקוש ייבחן מול הקבלנים הגדולים בישראל.';
  var RM = matchMedia('(prefers-reduced-motion: reduce)');
  var PHONE = function () { return matchMedia('(max-width: 900px)').matches; };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var fmt = function (n, d) { return Number(n).toLocaleString('he-IL', { maximumFractionDigits: d == null ? 1 : d }); };
  var track = function (n, p) { try { if (window.nlTrack) window.nlTrack(n, Object.assign({ project: 'aurelia' }, p || {})); } catch (e) { /* none */ } };
  var norm = function (b) { return ((Number(b) % 360) + 360) % 360; };
  var angOff = function (a, b) { var d = Math.abs(norm(a) - norm(b)); return Math.min(d, 360 - d); };
  var DIR = { 270: 'מערבה, לים', 90: 'מזרחה, לעיר', 180: 'דרומה, לרובע', 0: 'צפונה' };
  var DIRS = { 270: 'מערב', 90: 'מזרח', 180: 'דרום', 0: 'צפון' };
  var SIDE = { 270: 'ים', 90: 'עיר', 180: 'דרום' };
  var KIND = { sea: 'הים', beach: 'חוף', project: 'פרויקט ברובע', rail: 'רכבת קלה', school: 'חינוך', nature: 'טבע', park: 'פארק וספורט' };
  var KCOL = { sea: '#2f86b8', beach: '#d9b45a', project: '#36d1e0', rail: '#2f6f86', school: '#e0a03a', nature: '#4f9a6a', park: '#4f9a6a' };
  var CONE = '#C2563A';
  var wa = function () { return String(C.wa || (window.NADLAN_SHOWROOM && window.NADLAN_SHOWROOM.config && window.NADLAN_SHOWROOM.config.whatsapp) || '972525101555').replace(/\D/g, ''); };
  window.__nlas = { mounted: false, interactive: false, opened: 0, lastPull: null, beam: null };

  /* ---------------------------------------------------------------- data */
  var D = null, F = null, T = null, byId = {}, byFlatKey = {}, dataP = null, tagsP = null;
  function data() {
    if (dataP) return dataP;
    dataP = Promise.all([fetch(A('data.json')).then(function (r) { return r.json(); }), fetch(A('flats.json')).then(function (r) { return r.json(); })]).then(function (r) {
      D = r[0]; F = r[1];
      F.flats.forEach(function (f) { byId[f.id] = f; byFlatKey[f.flat] = f; });
      return D;
    });
    dataP.catch(function () { dataP = null; });
    return dataP;
  }
  function tags() { if (!tagsP) { tagsP = fetch(A('viewtags.json')).then(function (r) { return r.json(); }).then(function (j) { T = j; return j; }); tagsP.catch(function () { tagsP = null; }); } return tagsP; }
  function flatOfCard(c) { return c && c.flat ? byFlatKey[c.flat] || null : null; }
  function sameUnitOn(floor, f) {
    var L = F.flats.filter(function (x) { return x.f === floor; });
    if (!L.length) return null;
    return L.filter(function (x) { return x.u === f.u && x.b === f.b; })[0] || L.filter(function (x) { return x.b === f.b; })[0] || L[0];
  }
  function floors() { var s = {}; F.flats.forEach(function (x) { s[x.f] = 1; }); return Object.keys(s).map(Number).sort(function (a, b) { return a - b; }); }
  function eye(f) { return Math.round(f.z + 1.6); }
  function band(f) { return f.f <= 17 ? 10 : f.f <= 33 ? 25 : 42; }
  var AIVIEW = { 'b270-f10': 1, 'b270-f25': 1, 'b270-f42': 1, 'b90-f25': 1, 'b90-f10': 1, 'b90-f42': 1, 'b180-f10': 1, 'b180-f25': 1, 'b180-f42': 1 };
  var big = function () { return !PHONE() || (window.devicePixelRatio || 1) > 1.5; };
  function viewKey(f) { return 'b' + f.b + '-f' + band(f); }
  /* step 1b: the furnished, lit cut-away of the sample flat (ChatGPT from the flat's plan, D:/Media/Aurelia/v4/cut/ai): the pull-out
     lands on it; one picture per sample layout (rooms), labelled as an illustration */
  var CUT = (window.NLAS_CFG && window.NLAS_CFG.cut) || [5];
  function cutImg(f) { return f && CUT.indexOf(f.r) > -1 ? A('img/cut-r' + f.r + '-' + (big() ? 1600 : 1280) + '.webp') : null; }
  function viewImg(f) { return A('img/view-' + viewKey(f) + '-' + (big() ? 1600 : 1280) + '.webp'); }
  function title(f) { return 'קומה ' + f.f + ' · דירה ' + f.u; }

  /* ---------------------------------------------------------------- the stage */
  var S = { el: null, view: null, ids: null, idW: 0, idH: 0, k: 1, lay: null, hover: 0, sel: null, cache: {}, img: null, mode: 'intro' };
  var VIEWS = [['street', 'מהטיילת'], ['pitch', 'מהמגרש'], ['pool', 'בבריכה']];
  function picUrl(v) { return A('img/' + v + '-' + (big() ? 1600 : 1280) + '.webp'); }
  function idsOf(v) {
    if (S.cache[v]) return S.cache[v];
    var url = A('img/' + v + '-id' + (PHONE() ? '-960' : '') + '.png');
    S.cache[v] = fetch(url).then(function (r) { if (!r.ok) throw new Error('id'); return r.blob(); })
      .then(function (b) { return createImageBitmap(b, { colorSpaceConversion: 'none', premultiplyAlpha: 'none' }); })
      .then(function (bmp) {
        var cv = document.createElement('canvas'); cv.width = bmp.width; cv.height = bmp.height;
        var cx = cv.getContext('2d', { willReadFrequently: true }); cx.drawImage(bmp, 0, 0);
        var px = cx.getImageData(0, 0, bmp.width, bmp.height).data, ids = new Uint32Array(bmp.width * bmp.height);
        for (var i = 0, j = 0; i < ids.length; i++, j += 4) ids[i] = (px[j] << 16) | (px[j + 1] << 8) | px[j + 2];
        return { ids: ids, w: bmp.width, h: bmp.height };
      });
    S.cache[v].catch(function () { delete S.cache[v]; });
    return S.cache[v];
  }
  function $s(c) { return S.el.querySelector('.nlas-' + c); }
  function layout() {
    if (!S.view || !D || !S.img) return;
    var st = $s('stage'), W = st.clientWidth, H = st.clientHeight, vd = D.views[S.view];
    var s = Math.max(W / vd.w, H / vd.h), fx = vd.focus[0], fy = vd.focus[1];
    var dx = (W - vd.w * s) * fx, dy = (H - vd.h * s) * fy;
    // a chosen flat stays in the frame when the phone stage is compact: centre on its balcony, inside the picture
    var g = S.sel ? gidOfFlat(S.sel) : 0;
    if (g && PHONE() && S.el.classList.contains('has-flat')) {
      var b = vd.on[g], cx = (b[1] + b[3]) / 2 * s, cy = (b[2] + b[4]) / 2 * s;
      dx = Math.min(0, Math.max(W - vd.w * s, W * .5 - cx)); dy = Math.min(0, Math.max(H - vd.h * s, H * .46 - cy));
    }
    S.lay = { s: s, dx: dx, dy: dy, W: W, H: H };
    var box = { left: dx + 'px', top: dy + 'px', width: vd.w * s + 'px', height: vd.h * s + 'px' };
    Object.assign(S.img.style, box); Object.assign($s('ov').style, box);
  }
  function idAt(x, y) {
    if (!S.ids || !S.lay) return 0;
    var r = $s('stage').getBoundingClientRect(), vd = D.views[S.view];
    var ix = (x - r.left - S.lay.dx) / S.lay.s, iy = (y - r.top - S.lay.dy) / S.lay.s;
    if (ix < 0 || iy < 0 || ix >= vd.w || iy >= vd.h) return 0;
    var g = S.ids[Math.floor(iy * S.k) * S.idW + Math.floor(ix * S.k)];
    return vd.on[g] ? g : 0;
  }
  function gidOfFlat(f, v) {
    if (!D || !(v || S.view)) return 0;
    var on = D.views[v || S.view].on, ks = Object.keys(on);
    for (var i = 0; i < ks.length; i++) { var c = D.cards[ks[i]]; if (c && c.flat === f.flat) return +ks[i]; }
    return 0;
  }
  function glowCanvas(g, rgb, ids, idW, idH, k, vd) {
    var b = vd.on[g]; if (!b) return null;
    var pad = 10, x0 = Math.max(0, Math.floor(b[1] * k) - pad), y0 = Math.max(0, Math.floor(b[2] * k) - pad);
    var x1 = Math.min(idW - 1, Math.ceil(b[3] * k) + pad), y1 = Math.min(idH - 1, Math.ceil(b[4] * k) + pad);
    var bw = x1 - x0 + 1, bh = y1 - y0 + 1, im = new ImageData(bw, bh), d = im.data;
    for (var y = y0; y <= y1; y++) for (var x = x0; x <= x1; x++) {
      if (ids[y * idW + x] !== g) continue;
      var o = ((y - y0) * bw + (x - x0)) * 4; d[o] = rgb[0]; d[o + 1] = rgb[1]; d[o + 2] = rgb[2]; d[o + 3] = 255;
    }
    var t = document.createElement('canvas'); t.width = bw; t.height = bh; t.getContext('2d').putImageData(im, 0, 0);
    return { c: t, x0: x0, y0: y0 };
  }
  function redraw() {
    if (!S.view || !S.ids || !D) return;
    var ov = $s('ov'); if (ov.width !== S.idW || ov.height !== S.idH) { ov.width = S.idW; ov.height = S.idH; }
    var ctx = ov.getContext('2d'); ctx.clearRect(0, 0, ov.width, ov.height);
    var vd = D.views[S.view], px = Math.max(1, 2.4 * S.k / (S.lay ? S.lay.s : 1));
    var draw = function (g, rgb, a) {
      var o = glowCanvas(g, rgb, S.ids, S.idW, S.idH, S.k, vd); if (!o) return;
      ctx.save(); ctx.filter = 'blur(' + (px * 1.8).toFixed(2) + 'px)'; ctx.globalAlpha = a; ctx.drawImage(o.c, o.x0, o.y0);
      ctx.filter = 'blur(' + (px * .5).toFixed(2) + 'px)'; ctx.globalAlpha = a * .7; ctx.drawImage(o.c, o.x0, o.y0); ctx.restore();
    };
    var sg = S.sel ? gidOfFlat(S.sel) : 0;
    if (S.hover && S.hover !== sg) draw(S.hover, [54, 209, 224], .75);
    if (sg) draw(sg, [150, 240, 248], 1);
    var m = $s('mark');
    if (sg && S.lay) { var b = vd.on[sg]; m.hidden = false; m.style.left = (S.lay.dx + (b[1] + b[3]) / 2 * S.lay.s) + 'px'; m.style.top = (S.lay.dy + b[2] * S.lay.s) + 'px'; m.querySelector('b').textContent = 'דירה ' + S.sel.u + ' · קומה ' + S.sel.f; }
    else m.hidden = true;
  }
  function setView(v) {
    if (!D || !D.views[v]) return Promise.resolve();
    S.view = v; S.hover = 0;
    Array.prototype.forEach.call($s('views').querySelectorAll('[data-view]'), function (b) { b.setAttribute('aria-pressed', String(b.dataset.view === v)); });
    var img = new Image(); img.decoding = 'async'; img.alt = ''; img.className = 'nlas-pic'; img.src = picUrl(v);
    return Promise.all([img.decode().catch(function () {}), idsOf(v)]).then(function (r) {
      if (S.view !== v) return;
      var o = r[1]; S.ids = o.ids; S.idW = o.w; S.idH = o.h; S.k = o.w / D.views[v].w;
      if (S.img) S.img.replaceWith(img); else $s('stage').insertBefore(img, $s('ov'));
      S.img = img; layout(); redraw(); $s('loading').classList.add('done');
      if (!window.__nlas.interactive) { window.__nlas.interactive = true; window.__nlas.tInteractive = Math.round(performance.now()); }
    }, function () { $s('loading').textContent = 'התמונה לא נטענה. נסו שוב בעוד רגע.'; });
  }
  var thumb = function (img, pos, cls) { return '<i class="nlas-th ' + (cls || '') + '" style="background-image:url(' + esc(A('img/' + img)) + ');background-position:' + pos + '"></i>'; };
  function callBtn(cls, from) {
    return '<button type="button" class="nlas-call ' + (cls || '') + '" data-a="call" data-from="' + from + '">' + thumb('tile-call.webp', '50% 40%', 'cam') +
      '<span><b>שיחת וידאו עכשיו</b><small>נציג מצטרף, המשפחה בקישור</small></span></button>';
  }
  function mountStage() {
    var bld = document.getElementById('building');
    if (!bld || S.el) return !!S.el;
    var el = document.createElement('div'); el.className = 'nlas nlas'; el.id = 'nlas'; el.dir = 'rtl'; el.lang = 'he';
    el.innerHTML =
      '<div class="nlas-grid">' +
      '<div class="nlas-stage">' +
        '<canvas class="nlas-ov" aria-hidden="true"></canvas>' +
        '<div class="nlas-hit" role="img" aria-label="מגדל אורליה ספורט. נגיעה במרפסת בוחרת דירה, נגיעה בבריכה או במגרש פותחת אותם."></div>' +
        '<div class="nlas-mark" hidden><i></i><b></b></div>' +
        '<div class="nlas-head"><div class="nlas-k">AURELIA SPORTS · TEL AVIV</div><div class="nlas-h2" role="heading" aria-level="2">בוחרים דירה מתוך המגדל</div></div>' +
        '<div class="nlas-sim">הדמיה להמחשה</div>' +
        callBtn('fab', 'stage') +
        '<div class="nlas-facs" role="group" aria-label="המתקנים"><button type="button" data-fac="pool">' + thumb('pool-1280.webp', '50% 55%') + '<span>הבריכה האולימפית</span></button>' +
          '<button type="button" data-fac="pitch">' + thumb('pitch-1280.webp', '50% 60%') + '<span>מגרש הכדורגל</span></button></div>' +
        '<div class="nlas-hint">' + thumb('street-1280.webp', '58% 38%') + '<span>בחרו דירה על המגדל</span></div>' +
        '<div class="nlas-tip" hidden></div>' +
        '<div class="nlas-loading">טוענים את המגדל…</div>' +
        '<div class="nlas-views" role="toolbar" aria-label="נקודת מבט">' + VIEWS.map(function (v) { return '<button type="button" data-view="' + v[0] + '" aria-pressed="false">' + v[1] + '</button>'; }).join('') +
          '<button type="button" class="nlas-free" aria-pressed="false">סיבוב חופשי</button></div>' +
      '</div>' +
      '<div class="nlas-band" hidden></div>' +
      '<div class="nlas-mapslot compact"><button type="button" class="nlas-mapbig" data-a="mapbig" aria-expanded="false">המפה המלאה</button></div>' +
      '<div class="nlas-viewbig" hidden></div>' +
      '<div class="nlas-near" hidden></div>' +
      '<div class="nlas-panel" aria-live="polite"></div>' +
      '</div>';
    bld.insertBefore(el, bld.firstChild); bld.classList.add('nlas-on');
    S.el = el; window.__nlas.mounted = true;
    intro();
    dockMap();
    var root = document.getElementById('nl-root') || document.body;
    new MutationObserver(function () { dockMap(); }).observe(root, { childList: true, subtree: true });
    document.addEventListener('nlpjx:map', function () { mapTidy(); setTimeout(function () { mapResize(); if (S.sel) showBeam(S.sel.b); }, 60); });
    callBand();
    var hit = $s('hit'), tip = $s('tip');
    hit.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse' || !D) return;
      var g = idAt(e.clientX, e.clientY), c = g ? D.cards[g] : null, f = flatOfCard(c);
      var ok = !!(f || (c && c.fac));
      hit.classList.toggle('hov', ok);
      var hg = ok ? g : 0; if (hg !== S.hover) { S.hover = hg; redraw(); }
      if (ok) {
        var r = $s('stage').getBoundingClientRect(); tip.hidden = false;
        tip.innerHTML = f ? '<b>קומה ' + f.f + ' · דירה ' + f.u + '</b> ' + f.r + ' חדרים · ' + fmt(f.a, 0) + ' מ״ר · פונה ' + esc(DIRS[f.b]) + '<small>לחיצה פותחת את הדירה</small>' : esc(c.name) + '<small>לחיצה פותחת</small>';
        tip.style.left = (e.clientX - r.left) + 'px'; tip.style.top = (e.clientY - r.top) + 'px';
        tip.style.transform = 'translate(' + (e.clientX - r.left > r.width / 2 ? '-106%' : '10%') + ', -125%)';
      } else tip.hidden = true;
    });
    hit.addEventListener('pointerleave', function () { tip.hidden = true; if (S.hover) { S.hover = 0; redraw(); } });
    hit.addEventListener('click', function (e) {
      if (!D) return;
      var g = idAt(e.clientX, e.clientY), c = g ? D.cards[g] : null, f = flatOfCard(c);
      tip.hidden = true;
      if (f) { openFlat(f, true); return; }
      if (c && c.fac) facility(c.k.indexOf('POOL') >= 0 ? 'pool' : 'pitch');
    });
    el.addEventListener('click', onClick);
    addEventListener('resize', function () { layout(); redraw(); placeTags(); if (S.mode === 'flat') fitPhone(); });
    var go = function () { data().then(function () { setView('street'); }); };
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (en) { if (en.some(function (x) { return x.isIntersecting; })) { io.disconnect(); go(); } }, { rootMargin: '600px 0px' });
      io.observe(el);
    } else go();
    return true;
  }

  /* ---------------------------------------------------------------- the panel beside / under the tower */
  function $p(s) { return S.el.querySelector('.nlas-panel ' + s); }
  function intro() {
    S.mode = 'intro'; S.el.classList.remove('has-flat');
    $s('panel').innerHTML =
      '<div class="pn-intro">' +
        '<div class="pn-k">איך בוחרים דירה</div>' +
        '<ol class="pn-steps">' +
          '<li>' + thumb('street-1280.webp', '58% 38%') + '<span><b>נוגעים במרפסת במגדל</b>כל קומה, כל כיוון</span></li>' +
          '<li><i class="nlas-th plan">' + planSvg({ w: 16, d: 8.4, r: 5, a: 134, b: 270, sea: true }, 'mini') + '</i><span><b>הדירה יוצאת ונפתחת לתוכנית</b>מרוהטת, עם תוכנית הקומה</span></li>' +
          '<li>' + thumb('view-b270-f25-1280.webp', '50% 60%') + '<span><b>הנוף מהקומה, והכיוון על המפה</b>המקומות האמיתיים, במרחק הליכה</span></li>' +
        '</ol>' +
        '<div class="pn-k">המתקנים</div>' +
        '<div class="pn-facs"><button type="button" data-fac="pool">' + thumb('pool-1280.webp', '50% 55%') + '<b>הבריכה האולימפית</b><small>50 × 25 מ׳</small></button>' +
          '<button type="button" data-fac="pitch">' + thumb('pitch-1280.webp', '50% 60%') + '<b>מגרש הכדורגל</b><small>105 × 68 מ׳</small></button></div>' +
        '<div class="pn-cta">' + callBtn('', 'intro') + '<button type="button" class="pn-btn ghost" data-a="lead">השארת פרטים</button></div>' +
        '<div class="pn-decl">' + DECL + '</div>' +
      '</div>';
  }
  function facts(f) {
    return '<div class="pn-facts">' +
      '<div><b>' + f.r + '</b><span>חדרים</span></div>' +
      '<div><b>' + fmt(f.a, 0) + '</b><span>מ״ר</span></div>' +
      '<div><b>' + f.f + '</b><span>קומה</span></div>' +
      '<div><b>' + esc(DIRS[f.b]) + '</b><span>' + (f.sea ? 'לים' : f.b === 90 ? 'לעיר' : 'לרובע') + '</span></div>' +
      '<div class="st"><b>קונספט</b><span>שלב הפרויקט</span></div></div>';
  }
  function panelFlat(f, hold) {
    S.mode = 'flat'; S.el.classList.add('has-flat');
    var units = F.flats.filter(function (x) { return x.f === f.f; });
    $s('panel').innerHTML =
      '<div class="pn-flat' + (hold ? ' hold' : '') + '">' +
        '<div class="pn-top"><div class="pn-ttl"><b>' + title(f) + '</b><em class="nlas-tag">דירה לדוגמה</em></div>' +
          '<div class="pn-fl"><button type="button" data-fl="1" aria-label="אותה דירה, קומה אחת למעלה">▲</button><button type="button" data-fl="-1" aria-label="אותה דירה, קומה אחת למטה">▼</button></div></div>' +
        '<div class="pn-sides" role="group" aria-label="דירה אחרת בקומה">' + units.map(function (x) { return '<button type="button" data-unit="' + x.id + '" aria-pressed="' + (x.id === f.id) + '">' + SIDE[x.b] + ' ' + x.u + '</button>'; }).join('') + '</div>' +
        '<div class="pn-tabs" role="tablist">' + (cutImg(f) ? '<button type="button" role="tab" data-tab="cut" aria-selected="true">הדירה מרוהטת</button>' : '') + '<button type="button" role="tab" data-tab="plan" aria-selected="' + !cutImg(f) + '">התוכנית</button><button type="button" role="tab" data-tab="view" aria-selected="false"><i class="dot"></i>הנוף מהקומה</button></div>' +
        '<div class="pn-media" data-tab="' + (cutImg(f) ? 'cut' : 'plan') + '"></div>' +
        facts(f) +
        // the requests right under the facts (2 rows): on a desktop they end high in the panel, clear of the site's floating bars
        '<div class="pn-cta">' +
          '<a class="pn-btn pri" data-a="plan-wa" target="_blank" rel="noopener" href="' + esc(waLink(f, 'plan')) + '">לקבלת תוכנית הדירה</a>' +
          '<button type="button" class="pn-btn" data-a="pricelist">לקבלת מחירון כשייפתח</button>' +
          callBtn('', 'panel') +
          '<button type="button" class="pn-btn ghost" data-a="lead">השארת פרטים</button>' +
        '</div>' +
        '<div class="pn-price"><span class="lab">עסקאות שנסגרו באזור, ' + (f.r >= 5 ? '5 חדרים' : f.r + ' חדרים') + ' (חציון)</span><span class="val" data-med>…</span></div>' +
        '<div class="pn-decl">חדרים, שטח וחלוקה: נתוני דוגמה. פרויקט קונספטואלי, אינו בבנייה ואינו משווק.</div>' +
      '</div>';
    media(cutImg(f) ? 'cut' : 'plan');
    price(f);
    bandFlat(f, hold);
  }
  /* phones (Ben: a tap shows the facts AT ONCE): a slim band between the tower and his map, on the first screen with both:
     the flat's picture (its furnished plan; the pull-out lands on it), rooms · m² · floor · direction · stage, and the request */
  function bandFlat(f, hold) {
    var b = $s('band'); if (!b) return;
    b.hidden = false; b.classList.toggle('hold', !!hold);
    var pic = cutImg(f) ? '<img alt="" src="' + esc(cutImg(f)) + '">' : planSvg(f, 'mini');
    b.innerHTML = '<button type="button" class="bd-pic" data-a="toplan" aria-label="תוכנית הדירה, ' + f.r + ' חדרים">' + pic + '<span>תוכנית הדירה</span></button>' +
      '<div class="bd-facts"><div class="bd-l1"><b>' + f.r + '</b> חדרים · <b>' + fmt(f.a, 0) + '</b> מ״ר</div>' +
        '<div class="bd-l2">קומה <b>' + f.f + '</b> · פונה ' + esc(DIRS[f.b]) + (f.sea ? ', לים' : f.b === 90 ? ', לעיר' : '') + '</div>' +
        '<div class="bd-l3">שלב: <span class="st">קונספט</span> · <em>דירה לדוגמה</em></div></div>' +
      '<button type="button" class="bd-ask" data-a="lead">הדירה<br>מעניינת אותי</button>';
  }
  /* the site's own floating bars (WhatsApp, the lead row, the accessibility button) are never moved or restyled: they are measured,
     and the showroom keeps its controls clear of them (the transit map does the same, assets/transit/transit.js barGap) */
  function bars() {
    var out = [], els = document.querySelectorAll('body *');
    for (var i = 0; i < els.length; i++) {
      var e = els[i]; if (S.el && S.el.contains(e)) continue;
      var cs = getComputedStyle(e); if (cs.position !== 'fixed' || cs.display === 'none' || cs.visibility === 'hidden' || Number(cs.opacity) < .1) continue;
      var r = e.getBoundingClientRect(); if (r.width < 40 || r.height < 30 || r.height > 200 || r.top < innerHeight * .5 || r.top > innerHeight) continue;
      out.push(r);
    }
    return out;
  }
  function barTop() { var t = innerHeight; bars().forEach(function (r) { if (r.width >= 120) t = Math.min(t, r.top); }); return t; }
  function setBarVar() { if (S.el) S.el.style.setProperty('--nlas-barh', Math.round(Math.min(220, innerHeight - barTop() + 12)) + 'px'); }
  /* phones: after the tap the page settles with the tower, the band and his map on one screen; the map ends where the bars begin */
  function fitPhone() {
    if (!PHONE() || !S.el) return;
    setBarVar();
    var u = document.getElementById('nlpjx-unimap'), sl = S.el.querySelector('.nlas-mapslot'), bt = barTop();
    if (!u || !sl || !sl.classList.contains('compact')) return;
    // a short phone (the bars start high): the tower picture gets a little lower so 200 px of the map still show above the bars
    var st = $s('stage'), bd = $s('band'), room = bt - st.getBoundingClientRect().top - (bd ? bd.offsetHeight : 74) - 206;
    S.el.style.setProperty('--nlas-stageh', Math.round(Math.max(190, Math.min(innerHeight * .36, room))) + 'px'); layout(); redraw();
    var h = Math.round(Math.max(200, Math.min(340, bt - u.getBoundingClientRect().top)));
    S.el.style.setProperty('--nlas-maph', h + 'px'); mapResize();
  }
  function waLink(f, what) {
    var t = what === 'plan' ? 'שלום, אשמח לקבל את תוכנית הדירה באורליה ספורט: קומה ' + f.f + ', דירה ' + f.u + ' (' + f.r + ' חדרים, פונה ' + DIRS[f.b] + '). nad-lan.co.il'
      : 'שלום, אשמח לפרטים על אורליה ספורט. nad-lan.co.il';
    return 'https://wa.me/' + wa() + '?text=' + encodeURIComponent(t);
  }
  function media(tab) {
    var m = $p('.pn-media'); if (!m || !S.sel) return;
    var f = S.sel; m.dataset.tab = tab;
    Array.prototype.forEach.call(S.el.querySelectorAll('.pn-tabs [data-tab]'), function (b) { b.setAttribute('aria-selected', String(b.dataset.tab === tab)); });
    if (tab === 'cut' && cutImg(f)) {
      m.innerHTML = '<div class="pn-cut"><img alt="הדירה מרוהטת, מבט מלמעלה: ' + f.r + ' חדרים" src="' + esc(cutImg(f)) + '"></div>' + keyplan(f) +
        '<div class="pn-sim">הדמיה להמחשה · ריהוט וחלוקה לדוגמה</div>' +
        '<a class="pn-drag" href="' + esc(designerUrl(f)) + '" data-a="designer"><i class="hand"></i><span>גוררים את הספה, ומעצבים את הדירה</span></a>';
      dragDemo(m);
    } else if (tab === 'plan' || tab === 'cut') {
      tab = 'plan'; m.dataset.tab = 'plan';
      m.innerHTML = '<div class="pn-plan">' + planSvg(f, 'big') + '</div>' + keyplan(f) +
        '<div class="pn-sim">תוכנית לדוגמה · ריהוט להמחשה</div>' +
        '<a class="pn-drag" href="' + esc(designerUrl(f)) + '" data-a="designer"><i class="hand"></i><span>גוררים את הספה, ומעצבים את הדירה</span></a>';
      dragDemo(m);
    } else {
      var k = viewKey(f);
      m.innerHTML = '<div class="pn-view"><img alt="המבט מקומה ' + f.f + ' לכיוון ' + esc(DIRS[f.b]) + '" src="' + esc(viewImg(f)) + '"><div class="pn-tags"></div></div>' +
        '<div class="pn-sim">' + (AIVIEW[k] ? 'הדמיה להמחשה, על בסיס המפה' : 'מבט לפי המפה, הדמיה להמחשה') + ' · גובה העיניים כ-' + eye(f) + ' מ׳</div>' +
        '<div class="pn-tagcard" hidden></div>' + (CUE.view ? '' : '<div class="pn-cue">לחצו על מקום בנוף</div>');
      viewBig(f);
      tags().then(function () { drawTags(f); }).catch(function () {});
    }
    if (tab !== 'view') viewBig(null);
  }
  /* desktop: the view from the floor opens large under the tower and the panel (the tower and his map stay where they are) */
  function viewBig(f) {
    var vb = $s('viewbig'); if (!vb) return;
    if (!f || PHONE()) { vb.hidden = true; vb.innerHTML = ''; return; }
    var was = !vb.hidden; vb.hidden = false;
    vb.innerHTML = '<div class="vb-h"><b>הנוף מקומה ' + f.f + ', לכיוון ' + esc(DIRS[f.b]) + '</b><span>' + (AIVIEW[viewKey(f)] ? 'הדמיה להמחשה, על בסיס המפה' : 'מבט לפי המפה, הדמיה להמחשה') + ' · גובה העיניים כ-' + eye(f) + ' מ׳</span>' +
      '<button type="button" class="vb-x" data-a="vbclose" aria-label="סגירת הנוף הגדול">×</button></div>' +
      '<div class="pn-view vb-pic"><img alt="המבט מקומה ' + f.f + ' לכיוון ' + esc(DIRS[f.b]) + '" src="' + esc(A('img/view-' + viewKey(f) + '-1600.webp')) + '"><div class="pn-tags"></div>' +
      '<div class="pn-tagcard" hidden></div>' + (CUE.view ? '' : '<div class="pn-cue">לחצו על מקום בנוף</div>') + '</div>';
    if (!was) setTimeout(function () { var r = vb.getBoundingClientRect(); if (r.bottom > innerHeight) reveal(vb); }, 60);
  }
  /* the view's tags: placed in the frame with the camera of the first frame (scripts/aurelia/aurelia_viewtags.py) */
  function drawTags(f) {
    if (!T) return;
    Array.prototype.forEach.call(S.el.querySelectorAll('.pn-tags'), function (box) { drawTagsIn(box, f); });
    placeTags();
  }
  function drawTagsIn(box, f) {
    var v = T.views[viewKey(f)]; box.innerHTML = '';
    if (!v) return;
    v.tags.forEach(function (t) {
      var p = T.places[t.i], b = document.createElement('button'); b.type = 'button'; b.className = 'pn-tag k-' + p.k; b.dataset.place = t.i;
      b.dataset.x = t.x; b.dataset.y = t.y;
      b.innerHTML = '<i style="background:' + (KCOL[p.k] || '#9fb6c3') + '"></i><span>' + esc(label(p)) + (p.d ? ' · ' + dist(p.d) : '') + '</span>';
      box.appendChild(b);
    });
  }
  function placeTags() {
    if (!S.el) return;
    Array.prototype.forEach.call(S.el.querySelectorAll('.pn-tags'), placeIn);
  }
  function placeIn(box) {
    var W = box.clientWidth, H = box.clientHeight, s = Math.min(W / 16, H / 9), iw = 16 * s, ih = 9 * s, ox = (W - iw) / 2, oy = (H - ih) / 2; // the whole frame (contain): every tag stays
    Array.prototype.forEach.call(box.children, function (b) {
      var x = ox + Number(b.dataset.x) * iw, y = oy + Number(b.dataset.y) * ih;
      b.style.left = x + 'px'; b.style.top = y + 'px';
      b.classList.toggle('flip', x > W * .62);
      b.hidden = x < 4 || x > W - 4 || y < 4 || y > H - 4;
    });
  }
  function label(p) { return p.k === 'rail' && !/תחנ/.test(p.n) ? 'תחנת ' + p.n : p.n; }
  function dist(m) { return m < 1000 ? Math.round(m / 10) * 10 + ' מ׳' : fmt(m / 1000, 1) + ' ק״מ'; }
  function tagCard(i) {
    var p = T.places[i], cs = S.el.querySelectorAll('.pn-tagcard'); if (!cs.length) return;
    var html = '<b>' + esc(label(p)) + '</b><span>' + esc(KIND[p.k] || '') + (p.status ? ' · ' + esc(p.status) : '') +
      (p.d ? ' · ' + dist(p.d) + ' מהמגדל' + (p.walk ? ' · כ-' + p.walk + ' דק׳ הליכה' : '') : ' · מכל קומה בצד המערבי') + '</span>' +
      '<div class="row">' + (p.lat && p.d ? '<button type="button" data-a="onmap" data-place="' + i + '">לראות במפה</button>' : '') + (p.url ? '<a href="' + esc(p.url) + '">לעמוד הפרויקט</a>' : '') +
      '<button type="button" class="x" data-a="tagx" aria-label="סגירה">×</button></div>';
    Array.prototype.forEach.call(cs, function (c) { c.hidden = false; c.innerHTML = html; });
    Array.prototype.forEach.call(S.el.querySelectorAll('.pn-tag'), function (b) { b.classList.toggle('on', b.dataset.place === String(i)); });
    if (p.lat && p.d) mapFocus(p, false);
    cueOff('view');
    track('aurelia_view_tag', { place: p.n });
  }
  function price(f) {
    loadVal().then(function (j) {
      var c = j.cities && j.cities['תל אביב יפו'], m = $p('[data-med]'); if (!c || !m) return;
      var k = f.r >= 5 ? 'r5' : f.r === 4 ? 'r4' : 'r3';
      var hood = (c.hoods || []).filter(function (h) { return /^הצפון החדש החלק הצפ/.test(h.n); })[0];
      var hv = hood && hood[k] ? hood[k][0] : 0;
      m.innerHTML = (hv ? '<b>' + fmt(hv / 1e6, 2) + '</b> מיליון ש״ח בצפון החדש · ' : '') + '<b>' + fmt(c[k] / 1e6, 2) + '</b> בכל תל אביב' +
        '<a href="' + esc(c.page || '/tel-aviv-apartment-prices/') + '">לכל העסקאות</a><small>רשות המסים, ' + esc(c.q) + '. לדירות באורליה אין מחיר.</small>';
    }).catch(function () { var m = $p('[data-med]'); if (m) m.textContent = 'העסקאות לא נטענו.'; });
  }
  var VAL = null;
  function loadVal() { return VAL || (VAL = fetch((C.instruments || '') + 'data/value.json?ver=' + encodeURIComponent(V)).then(function (r) { return r.json(); })); }

  /* the plan: a furnished sample layout from the flat's real size and side (the window side on top) */
  function planSvg(f, cls) {
    var w = f.w, d = f.d, bal = 2.1, n = f.r, rooms = [];
    var front = +(d * .56).toFixed(2), back = +(d - front).toFixed(2);
    var mw = n >= 4 ? Math.min(5.2, w * .34) : n === 3 ? Math.min(3.8, w * .4) : 0;
    rooms.push({ x: mw, y: bal, w: w - mw, h: front, n: n >= 6 ? 'סלון ופינת אוכל' : 'סלון, אוכל ומטבח', t: 'liv' });
    if (mw) rooms.push({ x: 0, y: bal, w: mw, h: front, n: 'חדר הורים', t: 'master' });
    var list = [{ n: 'ממ״ד', w: 3.4, t: 'mmd' }], beds = Math.max(0, n - (mw ? 3 : 2));
    for (var i = 0; i < beds; i++) list.push({ n: 'חדר שינה', w: 3.3, t: 'bed' });
    if (n >= 6) list.push({ n: 'מטבח', w: 4.2, t: 'kit' });
    list.push({ n: 'רחצה', w: 2.4, t: 'bath' }); list.push({ n: 'כניסה', w: 2.2, t: 'entry' });
    var sum = list.reduce(function (a, r) { return a + r.w; }, 0), k = w / sum, x = w;
    list.forEach(function (r) { var rw = r.w * k; x -= rw; rooms.push({ x: x, y: bal + front, w: rw, h: back, n: r.n, t: r.t }); });
    var H = d + bal, mini = cls === 'mini';
    var o = '<svg class="nlas-plan ' + (cls || '') + '" viewBox="-0.5 -0.5 ' + (w + 1) + ' ' + (H + 1) + '" role="img" aria-label="תוכנית לדוגמה, ' + n + ' חדרים, ' + fmt(f.a, 0) + ' מ״ר">' +
      '<defs><filter id="nlas-sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx=".04" dy=".07" stdDeviation=".05" flood-color="#0b1b27" flood-opacity=".28"/></filter>' +
      '<pattern id="nlas-tile" width=".6" height=".6" patternUnits="userSpaceOnUse"><rect width=".6" height=".6" fill="#d9e2e5"/><path d="M0 0H.6M0 0V.6" stroke="#c3cfd3" stroke-width=".02"/></pattern>' +
      '<pattern id="nlas-deck" width="4" height=".22" patternUnits="userSpaceOnUse"><rect width="4" height=".22" fill="#c9d1d3"/><line x1="0" y1=".21" x2="4" y2=".21" stroke="#b3bdc0" stroke-width=".018"/></pattern>' +
      '<pattern id="nlas-oak" width="1.2" height=".18" patternUnits="userSpaceOnUse"><rect width="1.2" height=".18" fill="#ebe6dd"/><line x1="0" y1=".175" x2="1.2" y2=".175" stroke="#ddd6ca" stroke-width=".015"/><line x1=".7" y1="0" x2=".7" y2=".18" stroke="#ddd6ca" stroke-width=".012"/></pattern></defs>' +
      '<rect x="0" y="0" width="' + w + '" height="' + bal + '" fill="url(#nlas-deck)"/>';
    var FILL = { liv: 'url(#nlas-oak)', master: 'url(#nlas-oak)', bed: 'url(#nlas-oak)', mmd: '#e3e5e4', kit: 'url(#nlas-tile)', bath: 'url(#nlas-tile)', entry: '#e7e3dc' };
    rooms.forEach(function (r) { o += '<rect x="' + r.x.toFixed(2) + '" y="' + r.y.toFixed(2) + '" width="' + r.w.toFixed(2) + '" height="' + r.h.toFixed(2) + '" fill="' + FILL[r.t] + '"/>'; });
    // furniture (metres, top view), kept inside each room
    var fu = '';
    var R = function (x, y, ww, hh, fill, rx, extra) { return '<rect x="' + x.toFixed(2) + '" y="' + y.toFixed(2) + '" width="' + ww.toFixed(2) + '" height="' + hh.toFixed(2) + '" rx="' + (rx || .06) + '" fill="' + fill + '"' + (extra || '') + '/>'; };
    var plant = function (x, y, r) { return '<circle cx="' + x.toFixed(2) + '" cy="' + y.toFixed(2) + '" r="' + r + '" fill="#4f7d5a"/><circle cx="' + x.toFixed(2) + '" cy="' + y.toFixed(2) + '" r="' + (r * .55) + '" fill="#6a9a72"/>'; };
    var bed = function (x, y, ww, hh) { return R(x, y, ww, hh, '#ffffff', .08, ' stroke="#c9d1d4" stroke-width=".03"') + R(x + .08, y + .1, ww / 2 - .14, .42, '#eef1f2', .08) + R(x + ww / 2 + .06, y + .1, ww / 2 - .14, .42, '#eef1f2', .08) + R(x, y + hh * .58, ww, hh * .42, '#8fb3bd', .06); };
    rooms.forEach(function (r) {
      var X = r.x, Y = r.y, W = r.w, Hh = r.h;
      if (r.t === 'liv') {
        var sw = Math.min(3, W * .42), sx = X + W - sw - .5, sy = Y + Hh - 1.25;
        fu += R(sx - .25, Y + Hh - 3.2, sw + .5, 2.1, '#c9d6d8', .1);
        fu += '<g class="sofa" filter="url(#nlas-sh)">' + R(sx, sy, sw, .95, '#2f6f86', .16) + R(sx + .12, sy + .12, sw - .24, .55, '#3e8aa3', .1) + R(sx + sw - .95, sy - 1.3, .95, 1.4, '#2f6f86', .16) + '</g>';
        fu += '<g filter="url(#nlas-sh)">' + R(sx + sw / 2 - .6, Y + Hh - 2.55, 1.2, .62, '#9aa7ad', .3) + R(sx + .2, Y + Hh - 3.1, .8, .8, '#f4f5f4', .25, ' stroke="#c9d1d4" stroke-width=".03"') + '</g>';
        var dx = X + Math.max(.6, W * .12), dy = Y + Math.min(1.2, Hh * .2);
        if (W > 7) {
          fu += '<g filter="url(#nlas-sh)">' + R(dx, dy, 2, 1, '#7f8c92', .12);
          for (var c = 0; c < 3; c++) { fu += R(dx + .18 + c * .62, dy - .5, .45, .42, '#f4f5f4', .1) + R(dx + .18 + c * .62, dy + 1.08, .45, .42, '#f4f5f4', .1); }
          fu += '</g>';
          if (n < 6) fu += '<g filter="url(#nlas-sh)">' + R(X + .1, Y + Hh - .72, Math.min(3.4, W * .3), .62, '#f7f7f5', .04, ' stroke="#b9c3c6" stroke-width=".03"') + '<circle cx="' + (X + .7).toFixed(2) + '" cy="' + (Y + Hh - .41).toFixed(2) + '" r=".16" fill="#cfd8db"/><circle cx="' + (X + 1.6).toFixed(2) + '" cy="' + (Y + Hh - .41).toFixed(2) + '" r=".12" fill="#4b5459"/><circle cx="' + (X + 1.95).toFixed(2) + '" cy="' + (Y + Hh - .41).toFixed(2) + '" r=".12" fill="#4b5459"/>' + R(X + .6, Y + Hh - 2.1, 2.1, .85, '#eef0ef', .06, ' stroke="#b9c3c6" stroke-width=".03"') + '</g>';
        }
        fu += plant(X + .45, Y + .45, .32);
      } else if (r.t === 'master') {
        var bw = Math.min(1.8, W - .9), bh = Math.min(2.05, Hh - .9);
        fu += '<g filter="url(#nlas-sh)">' + bed(X + (W - bw) / 2, Y + Hh - bh - .1, bw, bh) + R(X + (W - bw) / 2 - .5, Y + Hh - .55, .42, .42, '#9aa7ad', .06) + R(X + (W + bw) / 2 + .08, Y + Hh - .55, .42, .42, '#9aa7ad', .06) + '</g>';
        fu += R(X + .08, Y + .15, .58, Math.min(2.2, Hh - 2.6 > .5 ? Hh - 2.6 : .5), '#dfe4e5', .03, ' stroke="#b9c3c6" stroke-width=".03"');
      } else if (r.t === 'bed' || r.t === 'mmd') {
        var b2w = Math.min(1.2, W - .7), b2h = Math.min(1.95, Hh - .5);
        if (r.t === 'mmd') fu += '<g filter="url(#nlas-sh)">' + R(X + .15, Y + .2, Math.min(1.4, W - .4), .6, '#9aa7ad', .05) + R(X + .45, Y + .9, .5, .5, '#2f6f86', .12) + '</g>' + R(X + W - .55, Y + .2, .4, Hh - .4, '#d2d8da', .03);
        else fu += '<g filter="url(#nlas-sh)">' + bed(X + W - b2w - .2, Y + .2, b2w, b2h) + R(X + .15, Y + Hh - .75, Math.min(1.1, W - b2w - .5 > .6 ? W - b2w - .5 : .6), .55, '#9aa7ad', .05) + '</g>';
      } else if (r.t === 'bath') {
        fu += '<g filter="url(#nlas-sh)">' + R(X + .1, Y + .1, Math.min(.95, W - .2), .95, '#f7fbfc', .12, ' stroke="#b9c8cd" stroke-width=".03"') + '<ellipse cx="' + (X + W / 2).toFixed(2) + '" cy="' + (Y + Hh - .45).toFixed(2) + '" rx=".2" ry=".28" fill="#ffffff" stroke="#b9c8cd" stroke-width=".03"/>' + R(X + W - .62, Y + 1.3, .52, Math.min(.95, Hh - 1.6), '#f7fbfc', .05, ' stroke="#b9c8cd" stroke-width=".03"') + '</g>';
      } else if (r.t === 'kit') {
        fu += '<g filter="url(#nlas-sh)">' + R(X + .1, Y + .1, W - .2, .62, '#f7f7f5', .04, ' stroke="#b9c3c6" stroke-width=".03"') + R(X + .7, Y + 1.4, W - 1.4, .9, '#eef0ef', .06, ' stroke="#b9c3c6" stroke-width=".03"') + '</g>';
      } else if (r.t === 'entry') {
        fu += R(X + .1, Y + .1, Math.min(1.2, W - .2), .34, '#d2d8da', .03) + plant(X + W - .35, Y + Hh - .35, .2);
      }
    });
    // balcony: two loungers and plants
    fu += '<g filter="url(#nlas-sh)">' + R(w * .62, .35, .7, 1.45, '#f4f5f4', .2, ' stroke="#c9d1d4" stroke-width=".03"') + R(w * .62 + .95, .35, .7, 1.45, '#f4f5f4', .2, ' stroke="#c9d1d4" stroke-width=".03"') + '<circle cx="' + (w * .3).toFixed(2) + '" cy="1.05" r=".45" fill="#9aa7ad"/></g>' + plant(.5, .55, .3) + plant(w - .5, .55, .3);
    o += fu;
    // walls: thick outside, thin inside; windows on the facade; doors
    rooms.forEach(function (r) { o += '<rect x="' + r.x.toFixed(2) + '" y="' + r.y.toFixed(2) + '" width="' + r.w.toFixed(2) + '" height="' + r.h.toFixed(2) + '" fill="none" stroke="#1f2b33" stroke-width="' + (r.t === 'mmd' ? .3 : .1) + '"/>'; });
    o += '<rect x="0" y="' + bal + '" width="' + w + '" height="' + d + '" fill="none" stroke="#1f2b33" stroke-width=".24"/>';
    for (var wx = .5; wx < w - .4; wx += 1.6) o += '<line x1="' + wx.toFixed(2) + '" y1="' + bal + '" x2="' + Math.min(w - .3, wx + 1.15).toFixed(2) + '" y2="' + bal + '" stroke="#7fe3ee" stroke-width=".12"/>';
    o += '<rect x="0" y="0" width="' + w + '" height="' + bal + '" fill="none" stroke="#5e6f78" stroke-width=".05"/>';
    rooms.forEach(function (r) {
      if (r.y > bal + .1) { var dx = r.x + Math.min(r.w - .2, .3), dy = r.y; o += '<line x1="' + dx.toFixed(2) + '" y1="' + dy.toFixed(2) + '" x2="' + (dx + .8).toFixed(2) + '" y2="' + dy.toFixed(2) + '" stroke="#f3f1ec" stroke-width=".14"/><path d="M' + dx.toFixed(2) + ' ' + dy.toFixed(2) + ' a.8 .8 0 0 0 .8 .8" fill="none" stroke="#5e6f78" stroke-width=".03"/>'; }
    });
    if (!mini) {
      var fs = Math.max(.38, Math.min(.52, w / 30));
      rooms.forEach(function (r) {
        var fz = Math.min(fs, r.w / (r.n.length * .5)), cx = r.t === 'liv' ? r.x + r.w * .74 : r.x + r.w / 2, cy = r.t === 'liv' ? r.y + .3 + fz : r.y + r.h - .3 - fz * 1.3;
        var lw = Math.max(r.n.length * fz * .5, 1.6 * fz) + .3;
        o += '<g class="lab"><rect x="' + (cx - lw / 2).toFixed(2) + '" y="' + (cy - fz * .95).toFixed(2) + '" width="' + lw.toFixed(2) + '" height="' + (fz * 2.05).toFixed(2) + '" rx="' + (fz * .3).toFixed(2) + '" fill="rgba(11,27,39,.78)"/>' +
          '<text x="' + cx.toFixed(2) + '" y="' + (cy - fz * .1).toFixed(2) + '" font-size="' + fz.toFixed(2) + '">' + esc(r.n) + '</text><text class="m2" x="' + cx.toFixed(2) + '" y="' + (cy + fz * .82).toFixed(2) + '" font-size="' + (fz * .78).toFixed(2) + '">' + fmt(r.w * r.h, 0) + ' מ״ר</text></g>';
      });
      o += '<text class="bal" x="' + (w * .3) + '" y="' + (bal - .3) + '" font-size="' + (fs * .9).toFixed(2) + '">מרפסת ' + (f.sea ? 'לים' : f.b === 90 ? 'לעיר' : '') + '</text>';
    }
    return o + '</svg>';
  }
  /* the floor plan: the typical floor (or the top floor) with this flat lit; north up, the sea on the left */
  var KEY = { typ: { 1: [2, 40, 10.4, 54], 2: [2, 54, 10.4, 70], 3: [2, 70, 10.4, 84], 4: [19.6, 40, 28, 54], 5: [19.6, 54, 28, 70], 6: [19.6, 70, 28, 84], 7: [10.4, 40, 19.6, 46.5] }, top: { 1: [2, 40, 10.4, 84], 2: [19.6, 40, 28, 84] } };
  function keyplan(f) {
    var K = f.f >= 46 ? KEY.top : KEY.typ, o = '<svg class="pn-key" viewBox="-1 37 32 50" role="img" aria-label="תוכנית הקומה: הדירה מסומנת">';
    o += '<rect x="2" y="40" width="26" height="44" fill="#132f40" stroke="#9fb6c3" stroke-width=".4"/>';
    Object.keys(K).forEach(function (u) { var b = K[u], on = Number(u) === f.u; o += '<rect x="' + b[0] + '" y="' + (124 - b[3]) + '" width="' + (b[2] - b[0]) + '" height="' + (b[3] - b[1]) + '" fill="' + (on ? '#36d1e0' : '#1d4255') + '" stroke="#0b1b27" stroke-width=".5"/>'; });
    o += '<rect x="11.5" y="62" width="7" height="12" fill="#0b1b27"/><text x="15" y="69" font-size="2.6">ליבה</text><text x="-.2" y="63" font-size="2.8" class="sea">ים</text><path d="M24 86.5l1.6-3 1.6 3z" fill="#f7f6f2"/></svg>';
    return '<div class="pn-keyw">' + o + '<span>תוכנית הקומה</span></div>';
  }
  function dragDemo(m) { // a short "drag the sofa" hint toward the designer: twice, then it rests
    if (RM.matches) return;
    var s = m.querySelector('.sofa'); if (!s || !s.animate) return;
    var h = m.querySelector('.pn-drag');
    setTimeout(function () {
      if (!s.isConnected) return;
      s.animate([{ transform: 'translate(0,0)' }, { transform: 'translate(-1.1px,0)' }, { transform: 'translate(-1.1px,0)' }, { transform: 'translate(0,0)' }], { duration: 2600, iterations: 2, easing: 'ease-in-out' });
      if (h) h.classList.add('go');
    }, 900);
  }

  /* ---------------------------------------------------------------- choosing a flat */
  function select(f, fromPop) {
    S.sel = f;
    $s('hint').classList.add('off');
    redraw();
    var detail = { floor: f.f, heightM: eye(f), bearing: f.b, unit: String(f.id), toward: DIRS[f.b], project: 'aurelia', label: title(f) };
    window.__nlpsPick = { floor: f.f, facing: DIR[f.b], unit: String(f.id), example: true, name: 'Aurelia Sports' };
    try { dispatchEvent(new CustomEvent('nl:floor', { detail: { floor: f.f, heightM: eye(f) } })); dispatchEvent(new CustomEvent('nl:facing', { detail: detail })); } catch (e) { /* none */ }
    if (!fromPop) { try { history.replaceState(history.state, '', location.pathname + location.search + '#dira=' + f.id); } catch (e) { /* none */ } }
  }
  function openFlat(f, fromStage) {
    if (!F) { data().then(function () { openFlat(byId[f.id] || f, fromStage); }); return; }
    var first = S.mode !== 'flat';
    select(f);
    panelFlat(f, first && !RM.matches);
    window.__nlas.opened++;
    track('aurelia_flat_open', { floor: f.f, unit: f.u, from: fromStage ? 'stage' : 'other' });
    var g = fromStage && S.img && S.ids ? gidOfFlat(f) : 0;
    var unhold = function () { var h = $p('.pn-flat'); if (h) h.classList.remove('hold'); var b = $s('band'); if (b) b.classList.remove('hold'); };
    var go = function () {
      layout(); redraw(); setBarVar();
      if (!first || RM.matches) { unhold(); cueMap(); return; }
      pullOut(f, g).then(function () { unhold(); cueMap(); });
    };
    if (PHONE()) { // the stage gets compact (the tower stays, the flat centred), and the page brings both into the eye
      requestAnimationFrame(function () { // the stage is already compact (no height transition on phones): settle the page at once
        layout(); redraw();
        var top = S.el.getBoundingClientRect().top + scrollY - 58;
        if (Math.abs(scrollY - top) > 4) { try { scrollTo({ top: top, behavior: 'instant' }); } catch (e) { scrollTo(0, top); } }
        fitPhone();
        setTimeout(go, 80);
      });
    } else go();
  }
  /* small labels that tell people what to do (Ben: "תוויות קטנות כאלה, שיבינו מה צריכים לעשות"): one on the tower before any tap
     (.nlas-hint), one on the map after the tap, one on the view; each fades after its first use */
  var CUE = { map: 0, view: 0 }, cueMk = null;
  function cueMap() {
    if (CUE.map) return;
    areaMap().then(function (map) {
      var gl = window.mapboxgl; if (!map || !gl || CUE.map) return;
      if (!cueMk) {
        var e = document.createElement('div'); e.className = 'nlas-cue nlas-cue-map'; e.textContent = 'האלומה מראה לאן הדירה פונה';
        cueMk = new gl.Marker({ element: e, anchor: 'bottom', offset: [0, -78] }); // above the wedge's tip: the map turns the flat's way up
        var off = function () { cueOff('map'); }; map.getContainer().addEventListener('pointerdown', off, { once: true });
        setTimeout(off, 12000);
      }
      cueMk.setLngLat(LL()).addTo(map); window.__nlas.cueMap = Math.round(performance.now());
    });
  }
  function cueOff(k) {
    if (CUE[k]) return; CUE[k] = 1;
    if (k === 'view') { Array.prototype.forEach.call(S.el.querySelectorAll('.pn-cue'), function (e) { e.classList.add('off'); setTimeout(function () { if (e.parentNode) e.remove(); }, 600); }); return; }
    var e = cueMk && cueMk.getElement();
    if (!e) return; e.classList.add('off');
    setTimeout(function () { if (cueMk) cueMk.remove(); }, 600);
  }
  /* the pull-out (Ben loved "the flat sliding out of the tower and opening into its plan"), about 1.2 s: the flat's own slice of the
     facade leaves the tower at its floor (a dark socket stays where it was), travels into the panel (phones: into the band under the
     tower), turns and opens into its furnished cut-away. Nothing covers the stage, no veil; a tap on "דילוג" ends it; reduced
     motion = no flight at all (openFlat). The skip button sits in the landing spot, never on the stage's labels or the call. */
  function pullOut(f, g) {
    var ph = PHONE(), land = ph ? $s('band') : $p('.pn-media'); if (!land) return Promise.resolve();
    var tr = land.getBoundingClientRect(), t0 = performance.now(), DUR = 1200;
    var po = document.createElement('div'); po.className = 'nlas-po'; document.body.appendChild(po);
    var anims = [], done = false, res, p = new Promise(function (r) { res = r; });
    var finish = function () { if (done) return; done = true; anims.forEach(function (a) { try { a.finish(); } catch (e) { /* none */ } }); po.remove(); window.__nlas.lastPull = Math.round(performance.now() - t0); res(); };
    var skip = document.createElement('button'); skip.type = 'button'; skip.className = 'po-skip'; skip.textContent = 'דילוג'; skip.onclick = finish;
    skip.style.top = (ph ? tr.top + Math.max(4, (tr.height - 34) / 2) : tr.top + 8) + 'px'; skip.style.left = (tr.left + 8) + 'px'; po.appendChild(skip);
    var sr = S.el.querySelector('.nlas-stage').getBoundingClientRect(), vd = D.views[S.view], b = g && S.lay ? vd.on[g] : null;
    var from = b ? { x: sr.left + S.lay.dx + (b[1] + b[3]) / 2 * S.lay.s, y: sr.top + S.lay.dy + (b[2] + b[4]) / 2 * S.lay.s, w: Math.max(18, (b[3] - b[1]) * S.lay.s), h: Math.max(8, (b[4] - b[2]) * S.lay.s) }
      : { x: sr.left + sr.width / 2, y: sr.top + sr.height * .45, w: 60, h: 18 };
    // the socket the flat leaves on the facade, and the flat's light
    var hole = document.createElement('div'); hole.className = 'po-hole'; Object.assign(hole.style, { left: from.x - from.w / 2 + 'px', top: from.y - from.h / 2 + 'px', width: from.w + 'px', height: from.h + 'px' }); po.appendChild(hole);
    anims.push(hole.animate([{ opacity: 0 }, { opacity: 1, offset: .14 }, { opacity: 1, offset: .85 }, { opacity: 0 }], { duration: DUR, fill: 'forwards' }));
    var ring = document.createElement('div'); ring.className = 'po-ring'; Object.assign(ring.style, { left: from.x + 'px', top: from.y + 'px', width: from.w + 14 + 'px', height: from.h + 14 + 'px' }); po.appendChild(ring);
    anims.push(ring.animate([{ opacity: 0, transform: 'translate(-50%,-50%) scale(.8)' }, { opacity: 1, transform: 'translate(-50%,-50%) scale(1.1)', offset: .35 }, { opacity: 0, transform: 'translate(-50%,-50%) scale(1.6)' }], { duration: 480, easing: 'ease-out', fill: 'forwards' }));
    // the volume: the flat's real proportions; its front is the facade itself (the same photo), its floor the furnished cut-away
    var bw = ph ? Math.min(innerWidth * .84, 340) : Math.min(tr.width * .86, 420), sc = bw / f.w, bd = Math.max(40, f.d * sc), k = bw / from.w;
    var bh = Math.max(22, Math.min(bw * .4, from.h * k));
    var facade = b && S.img ? "background-image:url('" + String(S.img.currentSrc || S.img.src).replace(/'/g, '%27') + "');background-size:" + (vd.w * S.lay.s * k).toFixed(1) + 'px ' + (vd.h * S.lay.s * k).toFixed(1) + 'px;background-position:' + (-b[1] * S.lay.s * k).toFixed(1) + 'px ' + (-(b[2] * S.lay.s * k) - (bh - from.h * k) / 2).toFixed(1) + 'px;' : '';
    var wrap = document.createElement('div'); wrap.className = 'po-boxw';
    var box = document.createElement('div'); box.className = 'po-box';
    var face = function (cls, w, h, t, inner, st) { return '<div class="po-f ' + cls + '" style="width:' + w + 'px;height:' + h + 'px;margin:' + (-h / 2) + 'px 0 0 ' + (-w / 2) + 'px;transform:' + t + ';' + (st || '') + '">' + (inner || '') + '</div>'; };
    box.innerHTML = face('po-front', bw, bh, 'translateZ(' + bd / 2 + 'px)', facade ? '<i class="po-ph" style="' + facade + '"></i>' : '') + face('po-back', bw, bh, 'rotateY(180deg) translateZ(' + bd / 2 + 'px)') +
      face('po-side', bd, bh, 'rotateY(90deg) translateZ(' + bw / 2 + 'px)') + face('po-side', bd, bh, 'rotateY(-90deg) translateZ(' + bw / 2 + 'px)') +
      face('po-top', bw, bd, 'rotateX(90deg) translateZ(' + bh / 2 + 'px)') + face('po-bot', bw, bd, 'rotateX(90deg) translateZ(' + (-bh / 2) + 'px)', cutImg(f) ? '<img class="po-cut" alt="" src="' + esc(cutImg(f)) + '">' : planSvg(f, 'mini'));
    wrap.style.perspectiveOrigin = from.x.toFixed(1) + 'px ' + from.y.toFixed(1) + 'px'; // it comes straight out of its balcony
    wrap.appendChild(box); po.appendChild(wrap);
    var to = { x: tr.left + tr.width / 2, y: tr.top + tr.height / 2 }, s0 = Math.max(.05, from.w / bw), E = 'cubic-bezier(.45,0,.2,1)';
    var T = function (x, y, z, s, rx, ry) { return 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) translateZ(' + z + 'px) scale(' + s.toFixed(3) + ') rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)'; };
    var mid = { x: from.x + (to.x - from.x) * .45, y: Math.min(from.y, to.y) + (Math.max(from.y, to.y) - Math.min(from.y, to.y)) * .3 - 24 };
    var kf = [
      { transform: T(from.x, from.y, 0, s0, 0, 0), easing: E },
      { transform: T(from.x, from.y, 70, s0 * 1.7, -6, 0), offset: .16, easing: E },                       // it leaves the facade, toward us
      { transform: T(mid.x, mid.y, 110, (s0 * 1.7 + .9) / 2, -24, -22), offset: .42, easing: E },           // it travels, turning
      { transform: T(to.x, to.y, 0, .94, -62, -8), offset: .66, easing: E },
      { transform: T(to.x, to.y, 0, 1, -90, 0), offset: .82, easing: E }                                  // it opens: the furnished cut-away
    ];
    var th = ph ? land.querySelector('.bd-pic img, .bd-pic svg') : null, tb = th && th.getBoundingClientRect();
    if (tb && tb.width) kf.push({ transform: T(tb.left + tb.width / 2, tb.top + tb.height / 2, 0, tb.width / bw, -90, 0) }); // phones: into the band's picture
    else kf.push({ transform: T(to.x, to.y, 0, 1, -90, 0) });
    window.__nlas.po = { from: from, to: to, g: g, bw: bw, land: ph ? 'band' : 'panel', skip: skip.getBoundingClientRect().toJSON() };
    anims.push(wrap.animate([{ opacity: 1 }, { opacity: 1, offset: .9 }, { opacity: 0 }], { duration: DUR, fill: 'forwards' }));
    anims.push(box.animate(kf, { duration: DUR, fill: 'forwards' }));
    var ph0 = box.querySelector('.po-ph'); if (ph0) anims.push(ph0.animate([{ opacity: 1 }, { opacity: 1, offset: .12 }, { opacity: 0, offset: .34 }, { opacity: 0 }], { duration: DUR, fill: 'forwards' }));
    anims.push(box.querySelector('.po-top').animate([{ opacity: 1 }, { opacity: 1, offset: .5 }, { opacity: 0, offset: .74 }, { opacity: 0 }], { duration: DUR, fill: 'forwards' }));
    Promise.all(anims.map(function (a) { return a.finished.catch(function () {}); })).then(finish);
    return p;
  }

  /* ---------------------------------------------------------------- facilities in the panel (the tower stays) */
  var FAC = {
    pool: { t: 'הבריכה האולימפית', img: 'pool', sz: '50 × 25 × 2.5 מ׳', p: 'עשרה מסלולים ברוחב 2.5 מטר, כ-3,125 טון מים, בגובה פנוי של 12 מטר. מיקום וגובה: קונספט.', src: 'מקור המידות: World Aquatics' },
    pitch: { t: 'מגרש הכדורגל', img: 'pitch', sz: '105 × 68 מ׳', p: 'על גג הבסיס, בגובה 21 מטר מעל הטיילת. עשר מסבכות פלדה מגשרות על 81 מטר, בלי עמוד מתחת למגרש. גובה ומסבכות: קונספט.', src: 'מקור המידות: IFAB, חוקי המשחק' }
  };
  function facility(k) {
    var x = FAC[k]; if (!x) return;
    track('aurelia_facility', { fac: k });
    S.mode = 'fac'; S.el.classList.remove('has-flat');
    if (S.view !== k) setView(k);
    $s('panel').innerHTML = '<div class="pn-fac"><div class="pn-top"><div class="pn-ttl"><b>' + esc(x.t) + '</b><em class="nlas-tag">הדמיה להמחשה</em></div>' +
      '<button type="button" class="pn-back" data-a="intro">› לבחירת דירה</button></div>' +
      '<div class="pn-media fac">' + '<img alt="" src="' + esc(A('img/' + x.img + '-' + (big() ? 1600 : 1280) + '.webp')) + '"></div>' +
      '<div class="pn-sz">' + esc(x.sz) + '</div><div class="pn-p">' + esc(x.p) + '</div><div class="pn-src">' + esc(x.src) + '</div>' +
      '<div class="pn-cta">' + callBtn('', 'facility') + '<button type="button" class="pn-btn ghost" data-a="lead">השארת פרטים</button></div>' +
      '<div class="pn-decl">' + DECL + '</div></div>';
  }

  /* ---------------------------------------------------------------- the call: now, or honestly not now */
  var AV = null;
  function avail() { return AV || (AV = C.avail ? fetch(C.avail, { credentials: 'omit', cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (j) { return !!(j && j.now === true); }).catch(function () { return false; }) : Promise.resolve(false)); }
  function designerUrl(f) { return (C.designer || '/tour/designer/') + '?project=aurelia' + (f ? '&unit=' + encodeURIComponent(f.id) : '') + '&pn=' + encodeURIComponent('Aurelia Sports') + '&ul=' + encodeURIComponent(location.pathname + (f ? '#dira=' + f.id : '')); }
  function callUrl(f) { return designerUrl(f) + '&call=1'; }
  function call(from) {
    var f = S.sel;
    track('aurelia_call', { from: from, floor: f ? f.f : null });
    avail().then(function (now) {
      if (now) { location.href = callUrl(f); return; }
      var host = S.el.querySelector('.nlas-panel');
      var old = host.querySelector('.pn-callsheet'); if (old) old.remove();
      var s = document.createElement('div'); s.className = 'pn-callsheet'; s.setAttribute('role', 'dialog'); s.setAttribute('aria-label', 'שיחת וידאו');
      s.innerHTML = '<b>ברגע זה אין נציג מחובר</b><span>אפשר לפתוח את חדר הווידאו עכשיו: אנחנו מקבלים הודעה ומצטרפים, והמשפחה נכנסת מקישור אחד. או שנחזור אליכם בשיחת וידאו, בשעה שנוחה לכם.</span>' +
        '<div class="row"><a class="pn-btn pri" href="' + esc(callUrl(f)) + '" data-a="room">לפתוח את החדר ולחכות</a><button type="button" class="pn-btn" data-a="callback">שתחזרו אליי בווידאו</button></div>' +
        '<button type="button" class="x" data-a="sheetx" aria-label="סגירה">×</button>';
      host.appendChild(s);
      var b = s.querySelector('.pn-btn'); if (b) b.focus({ preventScroll: true });
      var sb = s.getBoundingClientRect(); if (sb.bottom > barTop() - 8 || sb.top < 60) reveal(s);
    });
  }
  function callBand() { // Aurelia only: the booking band (#nlsch) becomes the call that opens now
    var sch = document.getElementById('nlsch'); if (!sch || sch.querySelector('.nlas-cb')) return;
    sch.classList.add('nlas-call-on');
    var b = document.createElement('div'); b.className = 'nlas-cb'; b.dir = 'rtl';
    b.innerHTML = '<div class="nlas-k">VIDEO · NOW</div><div class="nlas-cbh" role="heading" aria-level="2">שיחת וידאו על הדירה, עכשיו</div>' +
      '<div class="nlas-cbp">בלי לקבוע מועד: החדר נפתח מיד, אנחנו מקבלים הודעה ומצטרפים, ובני המשפחה נכנסים מקישור אחד ורואים איתכם את אותה דירה.</div>' + callBtn('', 'band');
    sch.insertBefore(b, sch.firstChild);
    b.addEventListener('click', function (e) { var t = e.target.closest('[data-a="call"]'); if (t) { e.preventDefault(); call('band'); } });
  }
  function toForm(msg) {
    var fm = document.getElementById('inquiry'); if (!fm) return;
    fm.scrollIntoView({ behavior: RM.matches ? 'auto' : 'smooth', block: 'start' });
    var ta = fm.querySelector('textarea'); if (ta && msg && !ta.value) ta.value = msg;
    var n = fm.querySelector('input[name="name"], input'); if (n) setTimeout(function () { try { n.focus({ preventScroll: true }); } catch (x) { /* none */ } }, 700);
  }

  /* ---------------------------------------------------------------- HIS map: the fleet's beam on #nlpjx-map, the places in it */
  var cone = null, focusMk = null;
  function areaMap() {
    if (window.NLPJX_MAP) return Promise.resolve(window.NLPJX_MAP);
    if (!document.getElementById('nlpjx-unimap')) return Promise.resolve(null);
    return new Promise(function (resolve) { document.addEventListener('nlpjx:map', function () { resolve(window.NLPJX_MAP); }, { once: true }); });
  }
  function LL() { var u = document.getElementById('nlpjx-unimap'); return u && Number(u.dataset.lat) ? [Number(u.dataset.lng), Number(u.dataset.lat)] : (F && F.origin ? [F.origin.lng, F.origin.lat] : [34.7845, 32.11]); }
  function showBeam(bearing) { // the engine's wedge (engine.js showViewCone), drawn from outside it, as bridge.js does for Rainbow
    return Promise.all([areaMap(), tags().catch(function () { return null; })]).then(function (res) {
      var map = res[0];
      var gl = window.mapboxgl; if (!map || !gl) return;
      var ll = LL();
      if (!cone) {
        var el = document.createElement('div'); el.style.pointerEvents = 'none'; el.className = 'nlas-cone';
        el.innerHTML = '<svg width="150" height="150" viewBox="0 0 150 150" style="display:block"><defs><linearGradient id="nlas-cone-g" x1="0" y1="0" x2="0" y2="1">' +
          '<stop offset="0" stop-color="' + CONE + '" stop-opacity="0"/><stop offset="1" stop-color="' + CONE + '" stop-opacity="0.55"/></linearGradient></defs>' +
          '<path d="M75 75 L44 8 A78 78 0 0 1 106 8 Z" fill="url(#nlas-cone-g)" stroke="' + CONE + '" stroke-opacity="0.35" stroke-width="1"/></svg>';
        cone = new gl.Marker({ element: el, rotationAlignment: 'map', pitchAlignment: 'map', anchor: 'center' }).setLngLat(ll);
      }
      cone.setRotation(norm(bearing)).addTo(map);
      // as bridge.js: the flat's way up, the building low in the frame; a compact map (under the tower) looks less far ahead
      // compact (under the tower): the zoom takes in the real places that way (the fifth nearest place inside the beam sets the
      // depth, 350 m to 1.2 km), so the map shows the surroundings with their names, not only the lot; the building sits low
      var hgt = map.getContainer().clientHeight, r = norm(bearing) * Math.PI / 180, ahead = 450, zm = 14.3;
      if (hgt < 420) {
        var ds = (T && T.places ? T.places : []).filter(function (p) { return p.d && angOff(p.b, bearing) <= 40; }).map(function (p) { return p.d; }).sort(function (a, b) { return a - b; });
        var D = Math.min(1200, Math.max(350, ds.length ? ds[Math.min(4, ds.length - 1)] : 700));
        var mpp = D / Math.max(120, hgt * 0.62);
        zm = Math.max(13.3, Math.min(15.2, Math.log(78271.517 * Math.cos(ll[1] * Math.PI / 180) / mpp) / Math.LN2));
        ahead = 0.3 * hgt * mpp;
      }
      map.easeTo({ center: [ll[0] + ahead * Math.sin(r) / (111320 * Math.cos(ll[1] * Math.PI / 180)), ll[1] + ahead * Math.cos(r) / 111320], zoom: zm, bearing: norm(bearing), pitch: 0, duration: 900 });
      window.__nlas.beam = norm(bearing);
    }).catch(function () { /* the map stays as it is */ });
  }
  /* Ben: his map sticks to the showroom, within the eye, also on phones: the page's own #nlpjx-map section (the same node, its
     own scripts and layers) is moved once under the tower (the engine re-adopts it after a re-render: it is moved back), shown
     compact (the map only, the beam and the named places on it) with a button to its full height and its layers */
  function dockMap() {
    if (!S.el) return;
    var sec = document.getElementById('nlpjx-map'), slot = S.el.querySelector('.nlas-mapslot');
    if (!sec || !slot) { if (slot) slot.hidden = !sec; return; }
    if (sec.parentNode === slot) return;
    slot.hidden = false; slot.appendChild(sec); mapResize(); mapTidy();
  }
  function mapResize() { try { if (window.NLPJX_MAP) window.NLPJX_MAP.resize(); } catch (e) { /* none */ } }
  function mapFocus(p, scroll) {
    areaMap().then(function (map) {
      var gl = window.mapboxgl; if (!map || !gl) return;
      if (!focusMk) { var e = document.createElement('div'); e.className = 'nlas-mapfocus'; e.innerHTML = '<i></i><b></b>'; focusMk = new gl.Marker({ element: e, anchor: 'bottom' }); }
      focusMk.getElement().querySelector('b').textContent = label(p) + (p.d ? ' · ' + dist(p.d) : '');
      focusMk.setLngLat([p.lng, p.lat]).addTo(map);
    });
    if (scroll) { var m = document.getElementById('nlpjx-unimap'); if (m && (m.getBoundingClientRect().top < 0 || m.getBoundingClientRect().bottom > innerHeight)) m.scrollIntoView({ behavior: RM.matches ? 'auto' : 'smooth', block: 'center' }); }
  }
  /* the compact map stays HIS map, readable: every marker carries its name or is not drawn at that zoom (Ben: the map tells you
     what is where). From outside areamap.js and the map section (neither file is touched): the page's future-plan dots (no
     name) step back in the compact map and the same plans are drawn as named marks that make room for the places
     (Mapbox collision, below areamap's layer); the price pills never pile up: the nearest wins, an overlapping one waits */
  var tidyOn = false;
  function compact() { var sl = S.el && S.el.querySelector('.nlas-mapslot'); return !!(sl && sl.classList.contains('compact')); }
  function mapTidy() {
    areaMap().then(function (map) {
      if (!map || tidyOn) return; tidyOn = true;
      var run = function () { try { tidy(map); } catch (e) { /* the map stays as it is */ } };
      map.on('moveend', run); map.on('idle', run);
      if (map.loaded()) plansLayer(map); else map.once('load', function () { plansLayer(map); });
      run();
    });
  }
  function plansLayer(map) {
    var gl = window.mapboxgl, P = window.NLPJX_PLANS || [], seen = {}, ll = LL(), feats = [];
    if (!gl || map.getSource('nlas-plans')) return;
    // a Hebrew page names a plan in Hebrew (or its Latin brand): the language twins of a project (-en/-ar/-ru/-fr) collapse into
    // one mark, the Hebrew page or else the English one; a project known only by a foreign-language page is not drawn here
    var LANG = /-(en|ar|ru|fr)\/?$/, rank = function (u) { var m = LANG.exec(u || ''); return !m ? 0 : m[1] === 'en' ? 1 : 9; }, best = {};
    P.forEach(function (pl) { if (!pl || !pl.lat || !pl.lng || rank(pl.url) > 1) return; var k = String(pl.url || pl.name).replace(LANG, ''); if (!best[k] || rank(pl.url) < rank(best[k].url)) best[k] = pl; });
    P = Object.keys(best).map(function (k) { return best[k]; });
    P.forEach(function (pl) {
      var n = String(pl.name || '').split(/\s[-–|]\s|:|,/)[0].replace(/[؀-ۿЀ-ӿ]+/g, '').replace(/\s+/g, ' ').trim(), key = n + '|' + Number(pl.lat).toFixed(4);
      if (!n || seen[key]) return; seen[key] = 1;
      feats.push({ type: 'Feature', geometry: { type: 'Point', coordinates: [pl.lng, pl.lat] }, properties: { n: n, u: pl.url || '', full: pl.name || n, r: Math.hypot(pl.lat - ll[1], pl.lng - ll[0]) } });
    });
    if (!feats.length) return;
    try {
      var cv = document.createElement('canvas'); cv.width = cv.height = 34; var x = cv.getContext('2d');
      x.beginPath(); x.arc(17, 17, 13, 0, 7); x.fillStyle = '#6B4FA0'; x.fill(); x.lineWidth = 5; x.strokeStyle = '#ffffff'; x.stroke();
      if (!map.hasImage('nlas-plan-dot')) map.addImage('nlas-plan-dot', x.getImageData(0, 0, 34, 34), { pixelRatio: 2 });
      map.addSource('nlas-plans', { type: 'geojson', data: { type: 'FeatureCollection', features: feats } });
      map.addLayer({ id: 'nlas-plans', type: 'symbol', source: 'nlas-plans', layout: {
        visibility: compact() ? 'visible' : 'none', 'icon-image': 'nlas-plan-dot', 'icon-allow-overlap': false, 'symbol-sort-key': ['get', 'r'],
        'text-field': ['get', 'n'], 'text-font': ['DIN Pro Medium', 'Arial Unicode MS Regular'], 'text-size': 12, 'text-variable-anchor': ['right', 'left', 'top', 'bottom'],
        'text-radial-offset': .9, 'text-justify': 'auto', 'text-optional': false, 'icon-optional': false, 'text-max-width': 9, 'text-padding': 2 },
        paint: { 'text-color': '#4a3478', 'text-halo-color': 'rgba(250,247,241,.96)', 'text-halo-width': 1.8 } }, map.getLayer('nlam-pin') ? 'nlam-pin' : undefined);
      map.on('click', 'nlas-plans', function (e) {
        var ft = e.features && e.features[0]; if (!ft) return;
        new gl.Popup({ offset: 14, maxWidth: '260px' }).setLngLat(ft.geometry.coordinates).setHTML('◆ <b>' + esc(ft.properties.full) + '</b>' + (ft.properties.u ? '<br><a href="' + esc(ft.properties.u) + '">לפרטי התוכנית ←</a>' : '')).addTo(map);
      });
    } catch (e) { /* the page's own dots stay */ }
  }
  function tidy(map) {
    var c = map.getContainer(), cr = c.getBoundingClientRect(), on = compact(), pills = [], hm = null;
    try { if (map.getLayer('nlas-plans') && map.getLayoutProperty('nlas-plans', 'visibility') !== (on ? 'visible' : 'none')) map.setLayoutProperty('nlas-plans', 'visibility', on ? 'visible' : 'none'); } catch (e) { /* none */ }
    Array.prototype.forEach.call(c.querySelectorAll('.mapboxgl-marker'), function (m) {
      if (/nlas-(cone|cue|mapfocus)/.test(m.className)) return;
      if (!m.dataset.nlas) { var bg = getComputedStyle(m).backgroundColor; m.dataset.nlas = bg === 'rgb(107, 79, 160)' ? 'plan' : /₪/.test(m.textContent) ? 'pill' : bg === 'rgb(194, 86, 58)' ? 'home' : 'x'; }
      var k = m.dataset.nlas;
      if (k === 'plan') m.classList.toggle('nlas-hide', on && !!map.getLayer('nlas-plans'));
      else if (k === 'home') hm = m.getBoundingClientRect();
      else if (k === 'pill') pills.push(m);
    });
    var sec = document.getElementById('nlpjx-map'), kept = hm ? [hm] : [];
    if (on && sec) Array.prototype.forEach.call(sec.querySelectorAll('.nlam-bar button, .nlam-range, .nlas-mapbig'), function (e) { var r = e.getBoundingClientRect(); if (r.width) kept.push(r); });
    var cx = hm ? hm.left + hm.width / 2 : cr.left + cr.width / 2, cy = hm ? hm.top + hm.height / 2 : cr.top + cr.height / 2;
    pills.map(function (m) { return { m: m, r: m.getBoundingClientRect() }; })
      .sort(function (a, b) { return Math.hypot(a.r.left - cx, a.r.top - cy) - Math.hypot(b.r.left - cx, b.r.top - cy); })
      .forEach(function (x) {
        var r = x.r, out = r.right < cr.left || r.left > cr.right || r.bottom < cr.top || r.top > cr.bottom;
        var hit = !out && kept.some(function (k) { return r.left < k.right + 3 && r.right > k.left - 3 && r.top < k.bottom + 3 && r.bottom > k.top - 3; });
        x.m.classList.toggle('nlas-hide', on && hit);
        if (!hit && !out) kept.push(r);
      });
  }
  function reveal(el) { // bring a showroom part into the eye, resting above the site's floating bars
    if (!el) return;
    var top = PHONE() ? 64 : 124, r = el.getBoundingClientRect(), room = barTop() - top, y = r.top + scrollY - top - Math.max(0, (room - r.height) / 2); // under the site's header (and its section tabs on a desktop)
    try { scrollTo({ top: Math.max(0, y), behavior: RM.matches ? 'instant' : 'smooth' }); } catch (e) { scrollTo(0, y); }
  }
  function near(f) { // what lies inside the beam: the same places as the map, sorted by distance (bridge.js showNear)
    var el = $s('near');
    tags().then(function () {
      var L = T.places.map(function (p, i) { return { p: p, i: i }; }).filter(function (x) { return x.p.d && x.p.lat && angOff(x.p.b, f.b) <= 45; }).sort(function (a, b) { return a.p.d - b.p.d; }).slice(0, 8);
      el.hidden = false;
      el.innerHTML = '<div class="nr-h"><i class="beam"></i><b>מה יש לכיוון של דירה ' + f.u + '</b><span>המקומות שבתוך הקרן על המפה</span>' +
        '' + '</div>' +
        '<div class="nr-list">' + (L.length ? L.map(function (x) {
          return '<button type="button" data-place="' + x.i + '" data-a="nearplace"><i style="background:' + (KCOL[x.p.k] || '#9fb6c3') + '"></i><b>' + esc(label(x.p)) + '</b><span>' + dist(x.p.d) + (x.p.walk ? ' · כ-' + x.p.walk + ' דק׳ הליכה' : '') + '</span></button>';
        }).join('') : '<span class="nr-none">אין לכיוון הזה מקומות מסומנים במפה.</span>') + '</div>' +
        '<div class="nr-src">מרחק בקו אווירי מהמיקום הרעיוני של המגדל; זמן ההליכה משוער. מקור: OpenStreetMap וקובצי הרובע באתר.</div>';
    }).catch(function () { el.hidden = true; });
  }
  addEventListener('nl:facing', function (e) { var d = e.detail || {}; if (d.project !== 'aurelia' || d.bearing == null) return; showBeam(d.bearing); var f = byId[d.unit]; if (f) near(f); });

  /* ---------------------------------------------------------------- clicks */
  function onClick(e) {
    var t = e.target.closest('[data-a],[data-fac],[data-view],[data-fl],[data-unit],[data-tab],[data-place],.nlas-free'); if (!t || !S.el.contains(t)) return;
    var a = t.dataset.a, f = S.sel;
    if (t.classList.contains('nlas-free')) { var bld = document.getElementById('building'), on = !bld.classList.contains('nlas-free'); bld.classList.toggle('nlas-free', on); t.setAttribute('aria-pressed', String(on)); return; }
    if (t.dataset.view) { setView(t.dataset.view); track('aurelia_view', { view: t.dataset.view }); return; }
    if (t.dataset.fac) { e.preventDefault(); facility(t.dataset.fac); return; }
    if (t.dataset.tab) { media(t.dataset.tab); track('aurelia_tab', { tab: t.dataset.tab }); return; }
    if (t.dataset.fl || t.dataset.unit) {
      var n = t.dataset.unit ? byId[t.dataset.unit] : sameUnitOn(f.f + Number(t.dataset.fl), f);
      if (n && n !== f) { var tab = ($p('.pn-media') || {}).dataset ? $p('.pn-media').dataset.tab : 'plan'; select(n); panelFlat(n, false); if (tab === 'view') media('view'); layout(); redraw(); }
      return;
    }
    if (a === 'call') { e.preventDefault(); call(t.dataset.from || 'panel'); return; }
    if (a === 'sheetx') { var sh = S.el.querySelector('.pn-callsheet'); if (sh) sh.remove(); return; }
    if (a === 'room') { track('aurelia_call_room', {}); return; }
    if (a === 'callback') { e.preventDefault(); track('aurelia_call_back', {}); toForm('אשמח שתחזרו אליי לשיחת וידאו על אורליה ספורט' + (f ? ', דירה ' + f.u + ' בקומה ' + f.f : '') + '. שעה נוחה: '); return; }
    if (a === 'lead') { e.preventDefault(); track('aurelia_lead_click', f ? { floor: f.f, unit: f.u } : {}); toForm(f ? 'אשמח לפרטים על דירה ' + f.u + ' בקומה ' + f.f + ' באורליה ספורט (' + f.r + ' חדרים, פונה ' + DIRS[f.b] + ').' : 'אשמח לפרטים על אורליה ספורט.'); return; }
    if (a === 'pricelist') { e.preventDefault(); track('aurelia_pricelist', f ? { floor: f.f, unit: f.u } : {}); toForm('אשמח לקבל את המחירון של אורליה ספורט כשייפתח' + (f ? ', ובמיוחד לדירה ' + f.u + ' בקומה ' + f.f : '') + '.'); return; }
    if (a === 'toplan') { e.preventDefault(); if ($p('.pn-media')) { media(cutImg(f) ? 'cut' : 'plan'); reveal($p('.pn-media')); } track('aurelia_band_plan', f ? { floor: f.f, unit: f.u } : {}); return; }
    if (a === 'plan-wa') { track('aurelia_plan_request', { floor: f.f, unit: f.u }); return; }
    if (a === 'designer') { track('aurelia_designer', f ? { floor: f.f, unit: f.u } : {}); return; }
    if (a === 'intro') { e.preventDefault(); if (S.view !== 'street') setView('street'); if (S.sel) { openFlat(S.sel, false); } else intro(); return; }
    if (a === 'vbclose') { viewBig(null); return; }
    if (a === 'tagx') { Array.prototype.forEach.call(S.el.querySelectorAll('.pn-tagcard'), function (c) { c.hidden = true; }); Array.prototype.forEach.call(S.el.querySelectorAll('.pn-tag.on'), function (x) { x.classList.remove('on'); }); return; }
    if (a === 'onmap' || a === 'nearplace') { var p = T && T.places[Number(t.dataset.place)]; if (p) { mapFocus(p, true); track('aurelia_place_map', { place: p.n }); } return; }
    if (a === 'mapbig') { var sl = S.el.querySelector('.nlas-mapslot'), big = sl.classList.toggle('compact') === false; t.setAttribute('aria-expanded', String(big)); t.textContent = big ? 'מפה קטנה' : 'המפה המלאה'; setTimeout(function () { if (!big) fitPhone(); mapResize(); if (S.sel) showBeam(S.sel.b); if (window.NLPJX_MAP) tidy(window.NLPJX_MAP); }, 40); track('aurelia_map_big', { big: big }); return; }
    if (a === 'tomap') { var m = document.getElementById('nlpjx-unimap') || document.getElementById('nlpjx-map'); if (m) m.scrollIntoView({ behavior: RM.matches ? 'auto' : 'smooth', block: 'center' }); return; }
    if (t.dataset.place && t.classList.contains('pn-tag')) { tagCard(Number(t.dataset.place)); return; }
  }

  /* ---------------------------------------------------------------- the engine's flats open the same flat (around the engine) */
  var ENG = { a: [270, 2], b: [270, 1], c: [180, 7], d: [90, 5], e: [90, 6], f: [270, 3] };
  function fromEngine(id) {
    var m = /^aur-t-(\d+)-([a-f])$/.exec(id || ''); if (!m || !F) return null;
    var fl = Math.max(6, Math.min(floors().slice(-1)[0], +m[1])), p = ENG[m[2]];
    var L = F.flats.filter(function (x) { return x.f === fl; });
    return L.filter(function (x) { return x.u === p[1] && x.b === p[0]; })[0] || L.filter(function (x) { return x.b === p[0]; })[0] || L[0] || null;
  }
  function intercept(e) {
    if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') return;
    var t = e.target.closest && e.target.closest('#nl-root [data-act="select"][data-id^="aur-"]'); if (!t) return;
    e.preventDefault(); e.stopImmediatePropagation(); e.stopPropagation();
    data().then(function () { var f = fromEngine(t.dataset.id); if (f) { var bld = document.getElementById('building'); if (bld) bld.classList.remove('nlas-free'); S.el.scrollIntoView({ block: 'start' }); openFlat(f, false); } });
  }
  document.addEventListener('click', intercept, true);
  document.addEventListener('keydown', intercept, true);

  /* ---------------------------------------------------------------- boot */
  function boot() {
    if (mountStage()) {
      var m = /#dira=(\d+-\d+)/.exec(location.hash);
      if (m) data().then(function () { var f = byId[m[1]]; if (f) { setView('street').then(function () { openFlat(f, true); }); } });
      return;
    }
    var t0 = Date.now(), mo = new MutationObserver(function () { if (mountStage() || Date.now() - t0 > 15000) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  window.NLAS = {
    open: function (id, fromStage) { return data().then(function () { var f = byId[id]; if (f) openFlat(f, fromStage !== false); return !!f; }); },
    tab: function (k) { media(k); }, facility: facility, intro: intro, call: call,
    tag: function (i) { return tags().then(function () { tagCard(i); }); },
    state: function () { return { mode: S.mode, view: S.view, sel: S.sel ? S.sel.id : null, pull: window.__nlas.lastPull, beam: window.__nlas.beam, tab: S.el && $p('.pn-media') ? $p('.pn-media').dataset.tab : null }; },
    screenOf: function (id) {
      var f = byId[id]; if (!f || !S.img || !S.lay) return null; var g = gidOfFlat(f); if (!g) return null;
      var r = $s('stage').getBoundingClientRect(), b = D.views[S.view].on[g], best = null, bn = -1;
      for (var y = Math.floor(b[2] * S.k); y <= Math.ceil(b[4] * S.k); y++) for (var x = Math.floor(b[1] * S.k); x <= Math.ceil(b[3] * S.k); x++) {
        if (S.ids[y * S.idW + x] !== g) continue; var n = 0;
        for (var q = -2; q <= 2; q++) for (var p = -2; p <= 2; p++) if (S.ids[(y + q) * S.idW + x + p] === g) n++;
        if (n > bn) { bn = n; best = [x, y]; }
      }
      return best ? { x: r.left + S.lay.dx + (best[0] + .5) / S.k * S.lay.s, y: r.top + S.lay.dy + (best[1] + .5) / S.k * S.lay.s } : null;
    }
  };
})();
