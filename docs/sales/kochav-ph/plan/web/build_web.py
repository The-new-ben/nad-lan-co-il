# -*- coding: utf-8 -*-
"""Build web/plan.html: interactive plan component for the listing page (RTL Hebrew, phone first).
Inlines svg/plan-lux.svg (title and legend groups removed, viewBox cropped) and renders/dollhouse-hotspots.json.
Images it uses: web/img/dollhouse.jpg (Blender render) and web/img/real-*.jpg (the broker's own photos, resized).
No dimensions anywhere.   python build_web.py"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(H)
svg = open(os.path.join(ROOT, "svg", "plan-lux.svg"), encoding="utf-8").read()
svg = re.sub(r'<g id="title".*?</g>', "", svg, flags=re.S)
svg = re.sub(r'<g id="legend".*?</g>\s*(?=</svg>)', "", svg, flags=re.S)
svg = re.sub(r'<svg ([^>]*?)viewBox="[^"]*" width="\d+" height="\d+"', r'<svg \1viewBox="170 10 3860 3900" preserveAspectRatio="xMidYMid meet" class="np-svg" focusable="false"', svg, count=1)
svg = svg.replace("<title>", '<title id="np-svg-title">', 1)
plan = json.load(open(os.path.join(ROOT, "trace", "plan.json"), encoding="utf-8"))
hs = json.load(open(os.path.join(ROOT, "renders", "dollhouse-hotspots.json"), encoding="utf-8"))
ORDER = ["living", "dining", "kitchen", "terrace", "entry", "corridor", "wc", "room_a", "bed1", "bed2", "bed3", "closet",
         "ensuite", "bath", "laundry", "balcony", "service", "ledge"]
PHOTOS = {"living": "img/real-living.jpg", "kitchen": "img/real-kitchen.jpg", "dining": "img/real-dining.jpg",
          "terrace": "img/real-terrace.jpg", "bath": "img/real-bath.jpg"}
names = {r["id"]: r["he"] for r in plan["rooms"]}
# two rooms share a name on the plan; the chips need to tell them apart without numbers
CHIP = dict(names); CHIP["bed1"] = "חדר שינה א׳"; CHIP["bed3"] = "חדר שינה ב׳"   # the plan has no north arrow, so no compass words
rooms = [{"id": i, "name": names[i], "chip": CHIP[i], "photo": PHOTOS.get(i), "hs": hs["rooms"].get(i)} for i in ORDER]

HTML = r"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>תוכנית הדירה | מיני פנטהאוז בכוכב הצפון</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif+Hebrew:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#14212B;--teal:#1F4B5C;--sea:#2F6F86;--line:#E3E8EC;--mist:#F5F8F9;--muted:#5F7785}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font-family:Assistant,"Segoe UI",Arial,sans-serif}
.np{max-width:1180px;margin:0 auto;padding:16px}
.np-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px;margin-bottom:12px}
.np-eyebrow{margin:0 0 2px;font-size:14px;font-weight:600;letter-spacing:.02em;color:var(--sea)}
.np-title{margin:0;font-family:"Noto Serif Hebrew",Georgia,serif;font-weight:600;font-size:clamp(26px,5.4vw,40px);line-height:1.1}
.np-seg{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:3px;background:#fff}
.np-seg button{min-height:44px;min-width:96px;padding:0 18px;border:0;border-radius:999px;background:transparent;color:var(--ink);font:600 16px Assistant,sans-serif;cursor:pointer}
.np-seg button[aria-pressed="true"]{background:var(--ink);color:#fff}
.np-body{display:grid;grid-template-columns:minmax(0,1fr);gap:14px}
.np-body>*{min-width:0}
@media (min-width:900px){.np-body{grid-template-columns:minmax(0,1.65fr) minmax(0,1fr);align-items:start}}
.np-stage{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:16px;background:#fff;aspect-ratio:1/1;touch-action:pan-y;user-select:none;-webkit-user-select:none;outline:none}
.np-stage.is3d{aspect-ratio:3/2;background:#e6ebee}
.np-stage:focus-visible{box-shadow:0 0 0 3px var(--sea)}
.np-canvas{position:absolute;inset:0;transform-origin:0 0;will-change:transform}
.np-svg{width:100%;height:100%;display:block}
.np-3d{position:absolute;inset:0;display:none}
.np-3d img{width:100%;height:100%;object-fit:contain;display:block;pointer-events:none;-webkit-user-drag:none}
.is3d .np-3d{display:block}.is3d .np-svg{display:none}
.room{cursor:pointer;outline:none}
.room .hl{fill:var(--sea);fill-opacity:0;stroke:var(--teal);stroke-opacity:0;stroke-width:10;transition:fill-opacity .2s,stroke-opacity .2s}
.room:hover .hl{fill-opacity:.07}
.room:focus-visible .hl{stroke-opacity:.6}
.room.active .hl{fill-opacity:.16;stroke-opacity:.9}
.np-tag{position:absolute;transform:translate(-50%,-120%);padding:6px 12px;border-radius:999px;background:var(--ink);color:#fff;font:600 15px Assistant,sans-serif;white-space:nowrap;pointer-events:none;box-shadow:0 6px 18px rgba(20,33,43,.25);display:none}
.np-tag::after{content:"";position:absolute;left:50%;bottom:-6px;transform:translateX(-50%);border:6px solid transparent;border-bottom:0;border-top-color:var(--ink)}
.np-tag.on{display:block}
.np-badge{position:absolute;bottom:10px;right:10px;margin:0;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.92);border:1px solid var(--line);color:var(--teal);font:600 13px Assistant,sans-serif;pointer-events:none}
.np-tools{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:8px}
.np-zoom{display:flex;gap:6px;flex:0 0 auto}
.np-zoom button{width:44px;height:44px;border-radius:12px;border:1px solid var(--line);background:#fff;color:var(--ink);font:600 22px Assistant,sans-serif;line-height:1;cursor:pointer;box-shadow:0 2px 10px rgba(20,33,43,.10)}
.np-zoom button:focus-visible,.np-chip:focus-visible,.np-seg button:focus-visible{outline:3px solid var(--sea);outline-offset:2px}
.np-hint{margin:0 2px;font-size:14px;line-height:1.35;color:var(--muted)}
.np-chips{display:flex;gap:8px;overflow-x:auto;padding:10px 2px 6px;scroll-snap-type:x proximity;-webkit-overflow-scrolling:touch}
.np-chip{flex:0 0 auto;scroll-snap-align:start;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--ink);font:600 15px Assistant,sans-serif;cursor:pointer}
.np-chip[aria-pressed="true"]{background:var(--teal);border-color:var(--teal);color:#fff}
@media (min-width:900px){.np-chips{flex-wrap:wrap;overflow:visible}}
.np-panel{border:1px solid var(--line);border-radius:16px;padding:16px;background:var(--mist);min-height:120px}
.np-panel h3{margin:0 0 6px;font-family:"Noto Serif Hebrew",Georgia,serif;font-weight:600;font-size:26px}
.np-panel p{margin:0;color:var(--muted);font-size:15px}
.np-panel figure{margin:12px 0 0}
.np-panel img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:12px;display:block;background:#dfe5e8}
.np-panel figcaption{margin-top:6px;font-size:13px;color:var(--muted)}
.np-foot{margin:10px 2px 0;font-size:12px;color:var(--muted)}
@media (prefers-reduced-motion:reduce){.room .hl{transition:none}}
</style>
</head>
<body>
<section class="np" id="np-plan" aria-labelledby="np-title">
  <div class="np-head">
    <div>
      <p class="np-eyebrow">מיני פנטהאוז · כוכב הצפון</p>
      <h2 class="np-title" id="np-title">תוכנית הדירה</h2>
    </div>
    <div class="np-seg" role="group" aria-label="תצוגת התוכנית">
      <button type="button" data-mode="2d" aria-pressed="true">תוכנית</button>
      <button type="button" data-mode="3d" aria-pressed="false">תלת־ממד</button>
    </div>
  </div>
  <div class="np-body">
    <div>
      <div class="np-stage" id="np-stage" tabindex="0" role="application" aria-roledescription="תוכנית אינטראקטיבית" aria-label="תוכנית הדירה. בחרו חדר מהרשימה או הקישו עליו. מקשי פלוס ומינוס להגדלה.">
        <div class="np-canvas" id="np-canvas">
          __SVG__
          <div class="np-3d" id="np-3d"><img src="img/dollhouse.jpg" alt="הדמיית תלת־ממד של הדירה, חתך בגובה המותניים, על פי תוכנית האדריכל" width="2400" height="1600" decoding="async"></div>
          <div class="np-tag" id="np-tag" aria-hidden="true"></div>
        </div>
        <p class="np-badge">הדמיה על פי תוכנית האדריכל</p>
      </div>
      <div class="np-tools">
        <p class="np-hint">הקישו על חדר כדי לראות אותו · צביטה או הקשה כפולה להגדלה</p>
        <div class="np-zoom" role="group" aria-label="הגדלה">
          <button type="button" data-z="in" aria-label="הגדלה">+</button>
          <button type="button" data-z="out" aria-label="הקטנה">−</button>
          <button type="button" data-z="reset" aria-label="חזרה לתצוגה המלאה">⤢</button>
        </div>
      </div>
      <div class="np-chips" id="np-chips" role="group" aria-label="חדרי הדירה"></div>
    </div>
    <div class="np-panel" id="np-panel" aria-live="polite">
      <h3>בחרו חדר</h3>
      <p>הקישו על חדר בתוכנית או ברשימה, ותראו אותו מסומן יחד עם צילום אמיתי מהדירה, כשיש כזה.</p>
    </div>
  </div>
  <p class="np-foot">הדמיה על פי תוכנית האדריכל, להמחשה בלבד. הריהוט בתוכנית כפי ששורטט על ידי האדריכל, והמיטות לצורך המחשה.</p>
</section>
<script>
(function(){
  var ROOMS = __ROOMS__;
  var byId = {}; ROOMS.forEach(function(r){ byId[r.id] = r; });
  var stage = document.getElementById("np-stage"), canvas = document.getElementById("np-canvas"),
      tag = document.getElementById("np-tag"), panel = document.getElementById("np-panel"),
      chips = document.getElementById("np-chips"), svg = canvas.querySelector("svg"), mode = "2d", current = null;
  // chips
  ROOMS.forEach(function(r){
    var b = document.createElement("button"); b.type = "button"; b.className = "np-chip"; b.textContent = r.chip;
    b.setAttribute("aria-pressed", "false"); b.dataset.room = r.id;
    b.addEventListener("click", function(){ select(r.id, true); });
    chips.appendChild(b);
  });
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function select(id, fromList){
    var r = byId[id]; if (!r) return; current = id;
    svg.querySelectorAll(".room").forEach(function(g){ g.classList.toggle("active", g.dataset.room === id); });
    chips.querySelectorAll(".np-chip").forEach(function(c){ c.setAttribute("aria-pressed", c.dataset.room === id ? "true" : "false"); });
    var html = "<h3>" + esc(r.name) + "</h3>";
    if (r.photo) html += '<figure><img src="' + r.photo + '" alt="' + esc(r.name) + ' - צילום אמיתי מהדירה" loading="lazy"><figcaption>צילום אמיתי מהדירה</figcaption></figure>';
    else html += "<p>החדר מסומן בתוכנית.</p>";
    panel.innerHTML = html;
    placeTag();
    if (fromList) { var c = chips.querySelector('[data-room="' + id + '"]'); if (c && c.scrollIntoView) c.scrollIntoView({block:"nearest", inline:"nearest"}); }
  }
  function placeTag(){
    var r = current && byId[current];
    if (mode !== "3d" || !r || !r.hs) { tag.classList.remove("on"); return; }
    // the image is letterboxed with object-fit:contain; hotspots are fractions of the image
    var W = canvas.clientWidth, H = canvas.clientHeight, ar = 2400/1600, iw = W, ih = W/ar;
    if (ih > H) { ih = H; iw = H*ar; }
    var ox = (W-iw)/2, oy = (H-ih)/2;
    tag.style.left = (ox + r.hs[0]*iw) + "px"; tag.style.top = (oy + r.hs[1]*ih) + "px";
    tag.textContent = r.name; tag.classList.add("on");
  }
  // mode toggle
  document.querySelectorAll(".np-seg button").forEach(function(b){
    b.addEventListener("click", function(){
      mode = b.dataset.mode;
      document.querySelectorAll(".np-seg button").forEach(function(x){ x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      stage.classList.toggle("is3d", mode === "3d"); reset(); placeTag();
    });
  });
  // zoom and pan
  var s = 1, tx = 0, ty = 0, MAX = 4;
  function clamp(){ var w = stage.clientWidth, h = stage.clientHeight;
    tx = Math.min(0, Math.max(w - w*s, tx)); ty = Math.min(0, Math.max(h - h*s, ty)); }
  function apply(){ clamp(); canvas.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + s + ")";
    stage.style.touchAction = s > 1.001 ? "none" : "pan-y"; }
  function zoomAt(px, py, ns){ ns = Math.max(1, Math.min(MAX, ns)); tx = px - (px - tx)*(ns/s); ty = py - (py - ty)*(ns/s); s = ns; apply(); }
  function reset(){ s = 1; tx = 0; ty = 0; apply(); }
  function center(){ return [stage.clientWidth/2, stage.clientHeight/2]; }
  document.querySelectorAll(".np-zoom button").forEach(function(b){
    b.addEventListener("click", function(){ var c = center();
      if (b.dataset.z === "in") zoomAt(c[0], c[1], s*1.5); else if (b.dataset.z === "out") zoomAt(c[0], c[1], s/1.5); else reset(); });
  });
  stage.addEventListener("wheel", function(e){ if (!e.ctrlKey) return; e.preventDefault(); // trackpad pinch only; plain wheel scrolls the page
    var r = stage.getBoundingClientRect(); zoomAt(e.clientX - r.left, e.clientY - r.top, s*Math.exp(-e.deltaY*0.01)); }, {passive:false});
  stage.addEventListener("keydown", function(e){ var c = center();
    if (e.key === "+" || e.key === "=") { zoomAt(c[0], c[1], s*1.5); e.preventDefault(); }
    else if (e.key === "-") { zoomAt(c[0], c[1], s/1.5); e.preventDefault(); }
    else if (e.key === "0" || e.key === "Escape") { reset(); }
    else if (s > 1 && /^Arrow/.test(e.key)) { var d = 40; if (e.key === "ArrowLeft") tx += d; if (e.key === "ArrowRight") tx -= d; if (e.key === "ArrowUp") ty += d; if (e.key === "ArrowDown") ty -= d; apply(); e.preventDefault(); }
  });
  svg.querySelectorAll(".room").forEach(function(g){
    g.addEventListener("keydown", function(e){ if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(g.dataset.room); } });
  });
  var P = new Map(), pinch = null, down = null, lastTap = null;
  stage.addEventListener("pointerdown", function(e){
        P.set(e.pointerId, {x:e.clientX, y:e.clientY});
    if (P.size === 2) { var a = Array.from(P.values()); var r = stage.getBoundingClientRect();
      pinch = {d:Math.hypot(a[0].x-a[1].x, a[0].y-a[1].y), s:s, mx:(a[0].x+a[1].x)/2 - r.left, my:(a[0].y+a[1].y)/2 - r.top}; down = null; }
    else if (P.size === 1) { down = {x:e.clientX, y:e.clientY, t:Date.now(), moved:false, lx:e.clientX, ly:e.clientY}; }
  });
  stage.addEventListener("pointermove", function(e){
    if (!P.has(e.pointerId)) return; P.set(e.pointerId, {x:e.clientX, y:e.clientY});
    if (pinch && P.size === 2) { var a = Array.from(P.values()); var d = Math.hypot(a[0].x-a[1].x, a[0].y-a[1].y);
      var ns = Math.max(1, Math.min(MAX, pinch.s * d / pinch.d)); tx = pinch.mx - (pinch.mx - tx)*(ns/s); ty = pinch.my - (pinch.my - ty)*(ns/s); s = ns; apply(); return; }
    if (down) { var dx = e.clientX - down.lx, dy = e.clientY - down.ly;
      if (Math.hypot(e.clientX-down.x, e.clientY-down.y) > 8) down.moved = true;
      if (s > 1.001 && down.moved) { if (!stage.hasPointerCapture(e.pointerId)) stage.setPointerCapture(e.pointerId); tx += dx; ty += dy; apply(); }
      down.lx = e.clientX; down.ly = e.clientY; }
  });
  function end(e){
    var wasTap = down && !down.moved && (Date.now() - down.t) < 400 && P.size === 1;
    P.delete(e.pointerId); if (P.size < 2) pinch = null;
    if (e.type !== "pointerup" || !wasTap) { if (!P.size) down = null; return; }
    var r = stage.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top, now = Date.now();
    if (lastTap && now - lastTap.t < 320 && Math.hypot(px-lastTap.x, py-lastTap.y) < 30) { // double tap
      if (s > 1.001) reset(); else zoomAt(px, py, 2.4); lastTap = null; }
    else { lastTap = {t:now, x:px, y:py}; tapSelect(e.clientX, e.clientY, px, py); }
    down = null;
  }
  stage.addEventListener("pointerup", end); stage.addEventListener("pointercancel", end);
  function tapSelect(cx, cy, px, py){
    if (mode === "2d") { var el = document.elementFromPoint(cx, cy); var g = el && el.closest && el.closest(".room"); if (g) select(g.dataset.room); return; }
    // 3D: nearest room label point on the image
    var W = canvas.clientWidth, H = canvas.clientHeight, ar = 2400/1600, iw = W, ih = W/ar; if (ih > H) { ih = H; iw = H*ar; }
    var ox = (W-iw)/2, oy = (H-ih)/2, ux = (px - tx)/s, uy = (py - ty)/s, best = null, bd = 1e9;
    ROOMS.forEach(function(r){ if (!r.hs) return; var d = Math.hypot(ox + r.hs[0]*iw - ux, oy + r.hs[1]*ih - uy); if (d < bd) { bd = d; best = r; } });
    if (best && bd < Math.max(60, iw*0.09)) select(best.id);
  }
  window.addEventListener("resize", function(){ apply(); placeTag(); });
  apply();
})();
</script>
</body>
</html>
"""
out = HTML.replace("__SVG__", svg).replace("__ROOMS__", json.dumps(rooms, ensure_ascii=False))
open(os.path.join(H, "plan.html"), "w", encoding="utf-8").write(out)
print("plan.html", len(out))
