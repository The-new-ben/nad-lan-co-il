# -*- coding: utf-8 -*-
"""One-off patch (21.10.2026): the listing's building in the Kochav world: floors you can pick, an elevator panel, an info card,
the real view from the building, a terrace eye point. Applied once to index.html."""
import io, os
H = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(H, "index.html")
s = io.open(p, encoding="utf-8").read()
assert "pickFloor" not in s, "already patched"
CSS = r"""
#lift{left:max(16px,env(safe-area-inset-left,0px));top:calc(env(safe-area-inset-top,0px) + 74px);background:var(--glass);border:1.5px solid var(--ink);display:grid;gap:4px;padding:8px;direction:rtl}
#lift b{font-size:12px;color:var(--mute);text-align:center}
#lift button{font:500 14px 'IBM Plex Mono',monospace;min-width:52px;min-height:34px;border:1px solid var(--line);background:#fff;color:var(--ink);cursor:pointer}
#lift button.home{border-color:var(--blue);color:var(--blue);font-weight:700}
#lift button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
#bpanel{right:max(16px,env(safe-area-inset-right,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 34px);width:min(400px,calc(100vw - 32px));background:var(--sheet);border:1.5px solid var(--ink);direction:rtl}
#bpanel header{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:10px 14px;border-bottom:1.5px solid var(--ink)}
#bpanel header b{font-size:16px}
#bpanel .body{padding:10px 14px;font-size:14px;line-height:1.55}
#bpanel .body p{margin:0 0 8px}
#bpanel .row{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 12px}
#bpanel .note{font-size:12px;color:var(--mute);padding:0 14px 12px;margin:0}
#bview{position:fixed;inset:0;z-index:25;background:rgba(15,34,51,.92);display:grid;place-items:center;padding:16px}
#bview figure{margin:0;max-width:min(1100px,100%);background:var(--sheet);border:1.5px solid var(--ink)}
#bview img{display:block;width:100%;height:auto}
#bview figcaption{display:flex;justify-content:space-between;gap:10px;align-items:center;padding:10px 14px;direction:rtl;font-size:14px}
@media (max-width:760px){#lift{top:auto;bottom:calc(env(safe-area-inset-bottom,0px) + 190px);grid-template-columns:repeat(7,1fr)}#lift b{grid-column:1/-1}#lift button{min-width:0}#bpanel{bottom:calc(env(safe-area-inset-bottom,0px) + 12px)}}
"""
R = []
R.append(("body.cine .hud,body.cine #go,body.cine #load{display:none!important}", "body.cine .hud,body.cine #go,body.cine #load{display:none!important}" + CSS))
R.append(('    <button class="btn" id="aboutBridge" type="button">על הגשר</button>', '    <button class="btn" id="bldBtn" type="button">הבניין</button>\n    <button class="btn" id="aboutBridge" type="button">על הגשר</button>'))
R.append(('<div class="hud" id="foot">', '''<div class="hud" id="lift" hidden><b>קומה</b></div>
<div class="hud" id="bpanel" hidden><header><b id="bT"></b><button class="btn" id="bX" type="button">חזרה להליכה</button></header><div class="body" id="bB"></div><div class="row" id="bR"></div><p class="note">קווי הבניין לפי שכבת המבנים של העירייה, והגובה (כ־46 מ׳) לפי מודל פני השטח. חלוקת הקומות, הנסיגות והמרפסת הן הדמיה עד לקבלת התוכנית.</p></div>
<div id="bview" hidden><figure><img id="bvImg" alt="הנוף מהבניין: מגדלי תל אביב מעל פארק הירקון, צילום אמיתי"><figcaption><span>הנוף מהבניין: מגדלי תל אביב מעל פארק הירקון. צילום אמיתי.</span><button class="btn" id="bvX" type="button">סגירה</button></figcaption></figure></div>
<div class="hud" id="foot">'''))
BLD = r"""
/* ---------------- the listing's building (building.json: the city's outline, about 46 m; floors and terrace illustrated) ---------------- */
const BLDG = await fetch('building.json').then((r) => r.json()).catch(() => null);
const BM = { on: false, az: 0.9, el: 0.32, r: 120, ty: 22, sel: 0, floors: [], c: [0, 0] };
if (BLDG) {
  const ring = BLDG.ring.slice(0, -1).map((p) => [p[0], p[1]]);
  let cx = 0, cz = 0; for (const [x, z] of ring) { cx += x; cz += z; } cx /= ring.length; cz /= ring.length; BM.c = [cx, cz];
  const inset = (k) => ring.map(([x, z]) => [cx + (x - cx) * k, cz + (z - cz) * k]);
  const G0 = BLDG.ground, ST = BLDG.story, N = BLDG.floors;
  const facade = mat.white.clone(), glassF = new THREE.MeshStandardMaterial({ color: 0xcfe0ea, roughness: 0.08, metalness: 0.3, envMapIntensity: 1.1 });
  const slabM = new THREE.MeshStandardMaterial({ color: 0xf4f4f1, roughness: 0.6 });
  const mkFloor = (n, poly, y0, y1, m) => { const A = new Acc(); walls(A, poly, y0, y1, n === 0 ? 9 : 10, n === 0 ? 4.6 : 9.6, (n * 0.37) % 1); const mm = m.clone(); mm.emissive = new THREE.Color(0x000000); const me = add(A, mm); me.userData.floor = n; BM.floors[n] = me; return me; };
  mkFloor(0, ring, 0, G0, mat.retail);
  for (let n = 1; n <= N; n++) {
    const y0 = G0 + (n - 1) * ST, y1 = y0 + ST, poly = n === N ? inset(0.7) : n === N - 1 ? inset(0.84) : ring;
    mkFloor(n, poly, y0, y1, n >= N - 1 ? glassF : facade);
    const S2 = new Acc(); walls(S2, poly, y1 - 0.28, y1, 6, 6); cap(S2, poly, y1, 6); add(S2, slabM);
  }
  // the terraces left by the setbacks: a deck and a glass railing at the edge (illustration)
  const deckM = M(T.deck, { roughness: 0.75 }), railM = new THREE.MeshStandardMaterial({ color: 0xd6e7ee, roughness: 0.05, transparent: true, opacity: 0.28, side: THREE.DoubleSide, depthWrite: false });
  for (const [n, k] of [[N - 1, 1.0], [N, 0.84]]) {
    const y = G0 + (n - 1) * ST, D2 = new Acc(); cap(D2, k === 1 ? ring : inset(k), y + 0.01, 2.2); add(D2, deckM, false);
    const Rl = new Acc(); walls(Rl, k === 1 ? ring : inset(k), y, y + 1.1, 4, 4); add(Rl, railM, false);
  }
  const roof = new Acc(); cap(roof, inset(0.7), G0 + N * ST + 0.02, 6); add(roof, mat.roof);
  COLL.push(ring);
  const Lf = $('lift');
  for (let n = N; n >= 0; n--) { const b = document.createElement('button'); b.type = 'button'; b.textContent = n === 0 ? 'ק' : String(n); b.dataset.n = n; if (n === BLDG.home_floor) b.classList.add('home'); b.onclick = () => pickFloor(n); Lf.append(b); }
}
const FLOOR_TXT = (n) => {
  const N = BLDG.floors;
  if (n === BLDG.home_floor) return { t: 'קומה 11 · המיני פנטהאוז', b: '<p>5 חדרים, כ־197 מ״ר, ומרפסת שמש של כ־74 מ״ר הפתוחה לשלושה כיוונים: קו הרקיע של תל אביב, פארק הירקון והים. נגרות בהתאמה אישית, מטבח מעוצב, מיזוג VRF, ממ״ד, 2 חניות ומחסן.</p><p>הנכס שמוצע כאן למכירה.</p>', home: true };
  if (n === N) return { t: 'קומה ' + N + ' · קומת הגג', b: '<p>הקומה העליונה, בנסיגה. אין לנו פרטים עליה, והיא אינה חלק מהנכס.</p>' };
  if (n === 0) return { t: 'קומת הקרקע · לובי', b: '<p>כניסה ולובי. בבניין חדר כושר לדיירים. ממול: המרכז המסחרי של השכונה, עם מעדנייה, סופרמרקט ובתי קפה.</p>' };
  return { t: 'קומה ' + n, b: '<p>קומת מגורים. בבניין 12 קומות; אין לנו פרטים על הדירות בקומה זו.</p>' };
};
function pickFloor(n) {
  if (!BLDG) return; BM.sel = n; BM.eye = null;
  for (const [k, me] of BM.floors.entries()) { if (!me) continue; const on = k === n; me.material.emissive.setHex(on ? (k === BLDG.home_floor ? 0x2f7fd0 : 0x6d7f90) : (k === BLDG.home_floor ? 0x0f3a66 : 0x000000)); me.material.emissiveIntensity = on ? 0.55 : 0.35; }
  for (const b of $('lift').querySelectorAll('button')) b.classList.toggle('on', Number(b.dataset.n) === n);
  BM.ty = n === 0 ? 3 : BLDG.ground + (n - 0.5) * BLDG.story; BM.el = Math.max(0.12, Math.min(0.6, 0.18 + n * 0.012));
  const f = FLOOR_TXT(n); $('bT').textContent = f.t; $('bB').innerHTML = f.b; const Rw = $('bR'); Rw.textContent = '';
  if (f.home) {
    const v = document.createElement('button'); v.className = 'btn pri'; v.type = 'button'; v.textContent = 'הנוף מהבניין (צילום אמיתי)'; v.onclick = () => { $('bvImg').src = 'view-11.jpg'; $('bview').hidden = false; }; Rw.append(v);
    const w = document.createElement('button'); w.className = 'btn'; w.type = 'button'; w.textContent = 'לעמוד על המרפסת'; w.onclick = () => standOnTerrace(); Rw.append(w);
  }
  $('bpanel').hidden = false;
}
function standOnTerrace() { // the eye at the 11th-floor terrace edge, looking south-west over the park (the height, illustrated)
  const y = BLDG.ground + (BLDG.home_floor - 1) * BLDG.story + 1.65; BM.eye = { y, x: BM.c[0] - 11, z: BM.c[1] + 12 };
}
function openBuilding(on = true) {
  BM.on = on && !!BLDG; $('lift').hidden = !BM.on; $('bpanel').hidden = true; $('near').style.display = BM.on ? 'none' : ''; $('map').style.display = BM.on ? 'none' : ''; $('joy').style.visibility = BM.on ? 'hidden' : '';
  BM.eye = null; $('bldBtn').classList.toggle('on', BM.on);
  if (BM.on) pickFloor(BLDG.home_floor);
}
$('bldBtn').onclick = () => openBuilding(!BM.on);
$('bX').onclick = () => openBuilding(false);
$('bvX').onclick = () => { $('bview').hidden = true; };
function renderBM() {
  if (BM.eye) { camera.position.set(BM.eye.x, BM.eye.y, BM.eye.z); camera.lookAt(BM.eye.x - 40 + Math.sin(BM.az) * 30, BM.eye.y - 6, BM.eye.z + 60); }
  else { const r = BM.r, c = BM.c; camera.position.set(c[0] + r * Math.cos(BM.el) * Math.sin(BM.az), BM.ty + r * Math.sin(BM.el), c[1] + r * Math.cos(BM.el) * Math.cos(BM.az)); camera.lookAt(c[0], BM.ty, c[1]); }
  sun.position.set(BM.c[0] + SUN.x * 300, SUN.y * 300, BM.c[1] + SUN.z * 300); sun.target.position.set(BM.c[0], 0, BM.c[1]); sun.target.updateMatrixWorld();
  if (bloom.strength > 0) composer.render(); else renderer.render(scene, camera);
}
"""
R.append(("// Sde Dov: our project pages around, schematic masses (quarter.json), planned or being built", BLD + "\n// Sde Dov: our project pages around, schematic masses (quarter.json), planned or being built"))
a = "canvas.addEventListener('pointermove', (e) => { if (!drag || e.pointerId !== drag.id) return;"
R.append((a, a + " if (BM.on) { BM.az -= (e.clientX - drag.x) * 0.006; BM.el = Math.max(0.05, Math.min(1.2, BM.el + (e.clientY - drag.y) * 0.004)); drag.x = e.clientX; drag.y = e.clientY; return; }"))
a2 = "  if (moved < 8 && quick) {"
R.append((a2, "  if (BM.on) { if (moved < 8 && quick) { const r = canvas.getBoundingClientRect(); const v = new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(v, camera); const hit = ray.intersectObjects(BM.floors.filter(Boolean), false)[0]; if (hit) pickFloor(hit.object.userData.floor); } return; }\n" + a2))
R.append(("canvas.addEventListener('pointerup', (e) => {", "canvas.addEventListener('wheel', (e) => { if (!BM.on) return; e.preventDefault(); BM.r = Math.max(35, Math.min(420, BM.r * (e.deltaY > 0 ? 1.1 : 0.9))); BM.eye = null; }, { passive: false });\ncanvas.addEventListener('pointerup', (e) => {"))
R.append(("  if (CINE) return;", "  if (CINE) return;\n  if (BM.on) { if (!drag && !BM.eye) BM.az += dt * 0.05; renderBM(); return; }"))
R.append(("window.__walk = { P, BR, ready: true,", "window.__walk = { P, BR, BM, openBuilding, pickFloor, standOnTerrace, ready: true,"))
for x, y in R:
    assert s.count(x) == 1, x[:70]; s = s.replace(x, y, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s); print("patched")
