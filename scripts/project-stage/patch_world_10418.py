# -*- coding: utf-8 -*-
"""v104.18 (1.10.2026, the V2 loop turn 2, item V2; HAD-380): apartments by direction, from a computed floor plan.
The floor-view step 3 was eight compass buttons. Now it is the floor's plan: a small key plan, north up and turned with the floor
(1.25 degrees a floor), with the four corner apartments round the spiral core (world.json model.plan, "corner4": computed from the
plate inside the glass line, about 850-900 m2, from 453 units over 117 floors, from the published 132-170 m2 sizes, and checked
against the listings' directions, floor 35 south-east and a high floor north-west, which fall on this plan's corners).
  1. tap an apartment on the plan (or its keyboard button): it is chosen, the view from its corner opens, its glass on that floor
     glows gold in the 3D;
  2. beside the plan: its name ("דירה פינתית צפון-מערבית"), the project's apartment sizes as public information, and its three
     windows (its two sides and its corner) to look out of;
  3. moving floor or tower keeps the apartment nearest the same corner, and a window inside it;
  4. the WhatsApp source line names the apartment ("... · דירה פינתית צפון-מערבית · מערבה"); no unit number is invented;
  5. the example apartment (c30w) is the north-west corner apartment: its button shows on any of its windows, and the album's
     line says the side its pictures face;
  6. one line under the plan says it is schematic (on the top floors: the larger penthouses there).
  python patch_world_10418.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world")
JS, CSS = os.path.join(D, "world.js"), os.path.join(D, "world.css")
s = open(JS, encoding="utf-8").read()
css = open(CSS, encoding="utf-8").read()
if "v104.18" in s or "v104.18" in css:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


# 0. the words, five languages
WORDS = {
    "he": ("    steps: ['בחרו מגדל', 'בחרו קומה', 'בחרו דירה לפי כיוון'], // v104.17",
           """    aptName: (i) => `דירה פינתית ${['צפונית', 'צפון-מזרחית', 'מזרחית', 'דרום-מזרחית', 'דרומית', 'דרום-מערבית', 'מערבית', 'צפון-מערבית'][i]}`, // v104.18
    aptViews: 'הנוף מהדירה', aptPick: 'הקישו על דירה בתוכנית הקומה', pubTag: 'מידע גלוי',
    aptSize: (s, r) => ['דירות בפרויקט:', `${s[0]}–${s[1]} מ״ר`, `${r[0]}–${r[1]} חדרים`],
    planLbl: 'תוכנית הקומה', planN: 'צ',
    planNote: 'תוכנית סכמטית: 4 דירות פינתיות בקומה טיפוסית',
    planTop: 'בקומות העליונות: דירות פנטהאוז גדולות יותר',"""),
    "en": ("    steps: ['Choose a tower', 'Choose a floor', 'Choose an apartment by its direction'], // v104.17",
           """    aptName: (i) => `${['North', 'North-east', 'East', 'South-east', 'South', 'South-west', 'West', 'North-west'][i]} corner apartment`, // v104.18
    aptViews: 'Views from the apartment', aptPick: 'Tap an apartment on the floor plan', pubTag: 'Public information',
    aptSize: (s, r) => ['Apartments here:', `${s[0]}–${s[1]} m²`, `${r[0]}–${r[1]} rooms`],
    planLbl: 'Floor plan', planN: 'N',
    planNote: 'Schematic plan: 4 corner apartments on a typical floor',
    planTop: 'On the top floors: larger penthouses',"""),
    "fr": ("    steps: ['Choisissez une tour', 'Choisissez un étage', 'Choisissez un appartement selon son orientation'], // v104.17",
           """    aptName: (i) => `Appartement d’angle ${['nord', 'nord-est', 'est', 'sud-est', 'sud', 'sud-ouest', 'ouest', 'nord-ouest'][i]}`, // v104.18
    aptViews: 'Les vues de l’appartement', aptPick: 'Touchez un appartement sur le plan de l’étage', pubTag: 'Information publique',
    aptSize: (s, r) => ['Appartements du projet :', `${s[0]}–${s[1]} m²`, `${r[0]}–${r[1]} pièces`],
    planLbl: 'Plan de l’étage', planN: 'N',
    planNote: 'Plan schématique : 4 appartements d’angle par étage courant',
    planTop: 'Aux derniers étages : des penthouses plus grands',"""),
    "ru": ("    steps: ['Выберите башню', 'Выберите этаж', 'Выберите квартиру по стороне света'], // v104.17",
           """    aptName: (i) => `Угловая квартира: ${['север', 'северо-восток', 'восток', 'юго-восток', 'юг', 'юго-запад', 'запад', 'северо-запад'][i]}`, // v104.18
    aptViews: 'Виды из квартиры', aptPick: 'Нажмите на квартиру на плане этажа', pubTag: 'Открытые данные',
    aptSize: (s, r) => ['Квартиры в проекте:', `${s[0]}–${s[1]} м²`, `${r[0]}–${r[1]} комнат`],
    planLbl: 'План этажа', planN: 'С',
    planNote: 'Схема: 4 угловые квартиры на типовом этаже',
    planTop: 'На верхних этажах: пентхаусы большей площади',"""),
    "ar": ("    steps: ['اختاروا البرج', 'اختاروا الطابق', 'اختاروا الشقة حسب اتجاهها'], // v104.17",
           """    aptName: (i) => `شقة زاوية باتجاه ${['الشمال', 'الشمال الشرقي', 'الشرق', 'الجنوب الشرقي', 'الجنوب', 'الجنوب الغربي', 'الغرب', 'الشمال الغربي'][i]}`, // v104.18
    aptViews: 'الإطلالات من الشقة', aptPick: 'اضغطوا على شقة في مخطط الطابق', pubTag: 'معلومات منشورة',
    aptSize: (s, r) => ['شقق المشروع:', `${s[0]}–${s[1]} م²`, `${r[0]}–${r[1]} غرف`],
    planLbl: 'مخطط الطابق', planN: 'ش',
    planNote: 'مخطط تخطيطي: 4 شقق زاوية في الطابق النموذجي',
    planTop: 'في الطوابق العليا: شقق بنتهاوس أكبر',"""),
}
for k, (a, b) in WORDS.items():
    sub(a, a + "\n" + b, "words " + k)

# 1. the state: the chosen apartment
sub("""    tower: null, floor: null, facing: null, view: 'out',
    season:""", """    tower: null, floor: null, facing: null, view: 'out', apt: null, // v104.18: apt, the corner apartment (0-3) on the floor plan
    season:""", "state")

# 2. the plan's geometry, after the facings
sub("""  const dirWord = (b) => T.dirs[Math.round(norm360(b) / 45) % 8];
""", """  const dirWord = (b) => T.dirs[Math.round(norm360(b) / 45) % 8];
  // ---------------------------------------------------------------- V2: the floor's apartments (v104.18, HAD-380)
  // world.json model.plan "corner4": a computed, schematic plan (no official plan is public, and the plan says so once): four corner
  // apartments round the spiral core. Apartment u's corner faces plate + 45 + 90u; it looks out on its corner and on its half of the
  // two sides beside it (the facings c - 45, c, c + 45). Ordered like the facings: from the corner nearest north, clockwise.
  const PLAN = () => (W && W.model && W.model.plan && W.model.plan.kind === 'corner4' ? W.model.plan : null);
  function aptCorners(k, f) {
    const th = TW[k].plateAt(f);
    const L = [0, 1, 2, 3].map((u) => norm360(th + 45 + 90 * u)).sort((a, b) => a - b);
    let s0 = 0, best = 999; L.forEach((b, i) => { const d = Math.min(b, 360 - b); if (d < best) { best = d; s0 = i; } });
    return L.slice(s0).concat(L.slice(0, s0));
  }
  function aptFacings(k, f, u) {
    const c = aptCorners(k, f)[u], L = facingBearings(k, f);
    return [c - 45, c, c + 45].map((b) => L.findIndex((x) => angDiff(x, b) < 1));
  }
  // the apartment a window belongs to: the current one when it has that window; else the corner's own, or for a side the apartment
  // clockwise from it (the example c30w: its living room faces the west side, its bedroom north-west)
  function aptOf(k, f, idx, cur) {
    if (cur != null && aptFacings(k, f, cur).includes(idx)) return cur;
    const b = facingBearing(k, f, idx) + 22.5, C4 = aptCorners(k, f);
    let u = 0; C4.forEach((c, i) => { if (angDiff(c, b) < angDiff(C4[u], b)) u = i; });
    return u;
  }
  const aptName = (k, f, u) => T.aptName(Math.round(norm360(aptCorners(k, f)[u]) / 45) % 8);
  // moving floor or tower keeps the apartment nearest the same corner, and a window inside it
  const aptKeep = () => (S.apt != null && S.tower && S.floor && PLAN() ? aptCorners(S.tower, S.floor)[S.apt] : null);
  function aptRestore(keepC) {
    if (keepC == null) return;
    const C4 = aptCorners(S.tower, S.floor); let u = 0; C4.forEach((c, i) => { if (angDiff(c, keepC) < angDiff(C4[u], keepC)) u = i; });
    S.apt = u;
    const fs = aptFacings(S.tower, S.floor, u);
    if (S.facing != null && !fs.includes(S.facing)) {
      const b = facingBearing(S.tower, S.floor, S.facing);
      S.facing = fs.reduce((a, i) => (angDiff(facingBearing(S.tower, S.floor, i), b) < angDiff(facingBearing(S.tower, S.floor, a), b) ? i : a), fs[1]);
    }
  }
""", "plan geometry")

# 3. a window picked anywhere joins its apartment; the floor and the tower keep the apartment
sub("""    S.facing = idx;
    S.view = 'window';""", """    S.facing = idx;
    if (PLAN()) S.apt = aptOf(S.tower, S.floor, idx, S.apt); // v104.18
    S.view = 'window';""", "setFacing apt")
sub("""    let keepB = S.facing != null && S.floor ? facingBearing(S.tower, S.floor, S.facing) : null;
    S.floor = f;
    if (keepB != null) { const list = facingBearings(S.tower, f); let bi = 0; list.forEach((b, i) => { if (angDiff(b, keepB) < angDiff(list[bi], keepB)) bi = i; }); S.facing = bi; }""",
    """    let keepB = S.facing != null && S.floor ? facingBearing(S.tower, S.floor, S.facing) : null;
    const keepC = aptKeep();
    S.floor = f;
    if (keepB != null) { const list = facingBearings(S.tower, f); let bi = 0; list.forEach((b, i) => { if (angDiff(b, keepB) < angDiff(list[bi], keepB)) bi = i; }); S.facing = bi; }
    aptRestore(keepC);""", "setFloor apt")
sub("""    const keepB = S.facing != null && S.tower && S.floor ? facingBearing(S.tower, S.floor, S.facing) : null;
    S.tower = k;
    S.floor = clamp(keepFloor || 30, 1, TW[k].N);
    if (keepB != null) { const list = facingBearings(k, S.floor); let bi = 0; list.forEach((b, i) => { if (angDiff(b, keepB) < angDiff(list[bi], keepB)) bi = i; }); S.facing = bi; }""",
    """    const keepB = S.facing != null && S.tower && S.floor ? facingBearing(S.tower, S.floor, S.facing) : null;
    const keepC = aptKeep();
    S.tower = k;
    S.floor = clamp(keepFloor || 30, 1, TW[k].N);
    if (keepB != null) { const list = facingBearings(k, S.floor); let bi = 0; list.forEach((b, i) => { if (angDiff(b, keepB) < angDiff(list[bi], keepB)) bi = i; }); S.facing = bi; }
    aptRestore(keepC);""", "pickTower apt")

# 4. the WhatsApp source line names the apartment (never a unit number)
sub("""      tower: S.tower, floor: T.pickLabel(S.floor, S.tower), facing: b != null ? dirWord(b) : '',""",
    """      tower: S.tower, floor: T.pickLabel(S.floor, S.tower), facing: b != null ? (S.apt != null && PLAN() ? `${aptName(S.tower, S.floor, S.apt)} · ` : '') + dirWord(b) : '',""",
    "pick")

# 5. the 3D: the chosen apartment's glass on that floor glows gold (the whole floor before an apartment is chosen)
sub("""    const gp = [], gi = plateOutline(X.gHalf + 0.08, X.NEXP, 96);""",
    """    // v104.18: with an apartment chosen, only its glass (its quarter of the plate, side middle to side middle round its corner)
    let gi = plateOutline(X.gHalf + 0.08, X.NEXP, 96);
    const gp = [];
    if (S.apt != null && PLAN()) {
      const a0 = aptCorners(S.tower, f)[S.apt] - 45 - th; gi = [];
      for (let a = 0; a <= 90; a += 3) { const phi = (a0 + a) * DEG, r = plateRadius(X.gHalf + 0.08, X.NEXP, phi); gi.push([r * Math.cos(phi), r * Math.sin(phi)]); }
    }
    const arc = S.apt != null && PLAN();""", "veil")
sub("""    for (let k = 0; k < gi.length; k++) {
      const k2 = (k + 1) % gi.length;
      const a = w(gi[k][0], gi[k][1], y0 + X.SLAB_T)""", """    for (let k = 0; k < gi.length - (arc ? 1 : 0); k++) {
      const k2 = (k + 1) % gi.length;
      const a = w(gi[k][0], gi[k][1], y0 + X.SLAB_T)""", "veil loop")

# 6. the panel: step 3 is the floor plan (the eight buttons stay for a world without a plan); with a plan the step is alone on its
#    line and the window / outside switch sits under the apartment's windows
sub("""          `<div class="nlw-lbl"><span class="nlw-step"><b>3</b>${esc(T.steps[2])}</span>${S.facing != null ? `<span class="nlw-seg">${chip(T.viewOut, S.view === 'out', 'data-view="out"')}${chip(T.viewWin, S.view === 'window', 'data-view="window"')}</span>` : ''}</div>` +""",
    """          (PLAN() ? `<div class="nlw-step"><b>3</b>${esc(T.steps[2])}</div>` :
          `<div class="nlw-lbl"><span class="nlw-step"><b>3</b>${esc(T.steps[2])}</span>${S.facing != null ? `<span class="nlw-seg">${chip(T.viewOut, S.view === 'out', 'data-view="out"')}${chip(T.viewWin, S.view === 'window', 'data-view="window"')}</span>` : ''}</div>`) +""", "step 3 line")
sub("""          facesHtml() + (S.facing == null && !nar ? `<div class="nlw-note">${esc(T.pickFacing)}</div>` : '') + exampleHtml() +""",
    """          (PLAN() ? planHtml() : facesHtml() + (S.facing == null && !nar ? `<div class="nlw-note">${esc(T.pickFacing)}</div>` : '')) + exampleHtml() +""",
    "panel step 3")
sub("""        const fr = p.querySelector('.nlw-faces'); if (fr) fr.outerHTML = facesHtml();
        bindFaces();""", """        const fr = p.querySelector('.nlw-faces'); if (fr) fr.outerHTML = facesHtml();
        const pw = p.querySelector('.nlw-planwrap'); if (pw) { pw.outerHTML = planHtml(); bindPlan(); } // v104.18
        bindFaces();""", "light panel")
sub("""    bindFaces();
    bindExample();
  }
""", """    bindFaces();
    bindPlan();
    bindExample();
  }
  // v104.18 (V2): the floor plan, north up and turned with the floor; the apartment's name, the project's sizes and its windows
  // a direction's name in a quarter: two short lines ("צפון" over "מערב"), so it never runs past the quarter's lines
  function planLabel(w, q) {
    const parts = String(w).split(/[-\s]+/).filter(Boolean), lh = 9.4, y0 = q[1] + 3 - (parts.length - 1) * lh / 2;
    return `<text x="${q[0].toFixed(1)}" y="${y0.toFixed(1)}" text-anchor="middle">${parts.map((t, i) => `<tspan x="${q[0].toFixed(1)}" dy="${i ? lh : 0}">${esc(t)}</tspan>`).join('')}</text>`;
  }
  function planSvg() {
    const P = PLAN(), X = TW[S.tower], f = S.floor, th = X.plateAt(f), R = 42, n = X.NEXP, core = R * (P.core_r || 0.3);
    const ru = th * DEG, eu = [Math.sin(ru), -Math.cos(ru)], ev = [Math.cos(ru), Math.sin(ru)];
    const pt = (r, phi) => { const u = r * Math.cos(phi), v = r * Math.sin(phi); return [u * eu[0] + v * ev[0], u * eu[1] + v * ev[1]]; };
    const fx = (q) => `${q[0].toFixed(1)},${q[1].toFixed(1)}`;
    const C4 = aptCorners(S.tower, f);
    const apts = C4.map((c, u) => {
      const a0 = c - 45 - th, out = [], inn = [];
      for (let a = 0; a <= 90; a += 5) { const phi = (a0 + a) * DEG; out.push(fx(pt(plateRadius(R, n, phi), phi))); }
      for (let a = 90; a >= 0; a -= 10) { const phi = (a0 + a) * DEG; inn.push(fx(pt(core, phi))); }
      const lc = (c - th) * DEG, q = pt((core + plateRadius(R, n, lc)) / 2 + 2, lc), on = S.apt === u;
      return `<g class="nlw-apt${on ? ' is-on' : ''}" data-apt="${u}" role="button" tabindex="0" aria-pressed="${on ? 'true' : 'false'}" aria-label="${esc(aptName(S.tower, f, u))}">` +
        `<path d="M${out.concat(inn).join('L')}Z"/>${planLabel(T.dirsShort[Math.round(norm360(c) / 45) % 8], q)}</g>`;
    }).join('');
    const coreC = `<circle class="nlw-core" cx="0" cy="0" r="${core.toFixed(1)}"/>`;
    const look = S.apt != null && S.facing != null ? (() => { const b = facingBearing(S.tower, f, S.facing) * DEG, r0 = plateRadius(R, n, b - ru) + 1.5;
      const p0 = [Math.sin(b) * r0, -Math.cos(b) * r0], p1 = [Math.sin(b - 0.32) * (r0 + 9), -Math.cos(b - 0.32) * (r0 + 9)], p2 = [Math.sin(b + 0.32) * (r0 + 9), -Math.cos(b + 0.32) * (r0 + 9)];
      return `<path class="nlw-look" d="M${fx(p0)}L${fx(p1)}L${fx(p2)}Z"/>`; })() : '';
    return `<svg class="nlw-plansvg" viewBox="-58 -58 116 116" role="group" aria-label="${esc(T.planLbl)}">${apts}${coreC}${look}` +
      `<g class="nlw-north" aria-hidden="true"><path d="M52,-57L55.5,-48L48.5,-48Z"/><text x="52" y="-39" text-anchor="middle">${esc(T.planN)}</text></g></svg>`;
  }
  function planHtml() {
    const P = PLAN(), f = S.floor, u = S.apt, top = f > TW[S.tower].N - (P.top_floors || 0);
    const sz = T.aptSize(P.sqm, P.rooms);
    // a number range reads in order in Hebrew and Arabic too (an en dash between numbers turns them around in an RTL line)
    const rng = (t) => esc(t).replace(/(\d+–\d+)/g, '<bdi dir="ltr">$1</bdi>');
    const info = u == null ? `<div class="nlw-note">${esc(T.aptPick)}</div>` :
      `<div class="nlw-aptname">${esc(aptName(S.tower, f, u)).replace(/(\S+-\S+)/g, '<span class="nlw-nw">$1</span>')}</div>` +
      `<div class="nlw-aptsize"><span class="nlw-pub">${esc(T.pubTag)}</span> ${esc(sz[0])} <span class="nlw-nw">${rng(sz[1])}</span> · <span class="nlw-nw">${rng(sz[2])}</span></div>`;
    const views = u == null ? '' :
      `<div class="nlw-aptviews" role="group" aria-label="${esc(T.aptViews)}"><span class="nlw-eyebrow">${esc(T.aptViews)}</span>` +
      `<div class="nlw-row">${aptFacings(S.tower, f, u).map((i) => chip(T.dirsShort[Math.round(norm360(facingBearing(S.tower, f, i)) / 45) % 8], S.facing === i, `data-face="${i}"`)).join('')}</div></div>`;
    const seg = S.facing != null ? `<div class="nlw-row nlw-seg nlw-planseg">${chip(T.viewWin, S.view === 'window', 'data-view="window"')}${chip(T.viewOut, S.view === 'out', 'data-view="out"')}</div>` : '';
    return `<div class="nlw-planwrap"><div class="nlw-plan">${planSvg()}<div class="nlw-planinfo">${info}</div></div>${views}${seg}` +
      `<div class="nlw-note nlw-plannote">${esc(top ? T.planTop : T.planNote)}</div></div>`;
  }
  function bindPlan() {
    if (!ui.panel) return;
    ui.panel.querySelectorAll('[data-apt]').forEach((g) => {
      g.addEventListener('click', () => pickApt(+g.dataset.apt));
      g.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pickApt(+g.dataset.apt); } });
    });
  }
  function pickApt(u, source = 'user') {
    if (!S.tower || !S.floor || !PLAN()) return;
    const had = document.activeElement && document.activeElement.closest && document.activeElement.closest('[data-apt]');
    S.apt = clamp(u | 0, 0, 3);
    setFacing({ index: aptFacings(S.tower, S.floor, S.apt)[1] }, source); // the view from its corner
    const g = had && ui.panel && ui.panel.querySelector(`[data-apt="${S.apt}"]`);
    if (g) g.focus({ preventScroll: true });
  }
""", "plan html")

sub("""    setFloor(+x.floor, 'user');
    setFacing(exampleBearing(x, +x.floor), 'user');""", """    setFloor(+x.floor, 'user');
    S.apt = null; // v104.18: the example's own apartment, not the one its side shares
    setFacing(exampleBearing(x, +x.floor), 'user');""", "goExample apt")
# 7. the example apartment is the north-west corner apartment: its button on any of its windows; the album says its pictures' side
sub("""  function exampleAt(k, f, idx) {
    if (!k || !f || idx == null || !TW[k]) return null;
    const b = facingBearing(k, f, idx);
    return exList().find((x) => String(x.tower).toUpperCase() === k && f >= +x.band[0] && f <= +x.band[1] && angDiff(b, exampleBearing(x, f)) < 1) || null;
  }""", """  function exampleAt(k, f, idx) {
    if (!k || !f || idx == null || !TW[k]) return null;
    const b = facingBearing(k, f, idx);
    return exList().find((x) => {
      if (String(x.tower).toUpperCase() !== k || f < +x.band[0] || f > +x.band[1]) return false;
      if (!PLAN() || S.apt == null) return angDiff(b, exampleBearing(x, f)) < 1;
      // v104.18: the example's apartment (the one its own window belongs to), on any of that apartment's windows
      const L = facingBearings(k, f); let xi = 0; L.forEach((y, i) => { if (angDiff(y, exampleBearing(x, f)) < angDiff(L[xi], exampleBearing(x, f))) xi = i; });
      return aptOf(k, f, xi, null) === S.apt;
    }) || null;
  }""", "exampleAt")
sub("""    const b = facingBearing(S.tower, S.floor, S.facing);
    pickExample(true);""", """    const b = PLAN() ? exampleBearing(x, S.floor) : facingBearing(S.tower, S.floor, S.facing); // v104.18: the side its pictures face
    pickExample(true);""", "open example")

open(JS, "w", encoding="utf-8", newline="\n").write(s)

css = css.rstrip("\n") + "\n\n" + """/* v104.18 (V2): the floor plan in step 3: a key plan (north up, turned with the floor) beside the chosen apartment */
.nlw-planwrap { margin-top: 6px; }
.nlw-plan { display: grid; grid-template-columns: 148px minmax(0, 1fr); gap: 12px; align-items: center; }
.nlw-plansvg { display: block; width: 148px; height: 148px; overflow: visible; }
.nlw-apt { cursor: pointer; outline: none; }
.nlw-apt path { fill: var(--nlw-paper); stroke: var(--nlw-ink); stroke-width: 1.1; stroke-linejoin: round; transition: fill .15s; }
.nlw-apt text { font: 700 8.6px/1 Heebo, Assistant, sans-serif; fill: var(--nlw-ink); pointer-events: none; }
.nlw-apt:hover path { fill: #F6EEDD; }
.nlw-apt.is-on path { fill: #E9D9B3; stroke: var(--nlw-gold); stroke-width: 1.8; }
.nlw-apt:focus-visible path { stroke: var(--nlw-ink); stroke-width: 2.4; }
.nlw-plansvg .nlw-core { fill: var(--nlw-hair); stroke: var(--nlw-ink); stroke-width: 0.8; }
.nlw-plansvg .nlw-look { fill: var(--nlw-gold); }
.nlw-north path { fill: var(--nlw-ink); }
.nlw-north text { font: 700 8px/1 Heebo, Assistant, sans-serif; fill: var(--nlw-ink); }
.nlw-planinfo { display: grid; gap: 6px; min-width: 0; }
.nlw-aptname { font-weight: 800; font-size: 15px; line-height: 1.3; color: var(--nlw-ink); }
.nlw-aptsize { font-size: 13px; line-height: 1.45; color: var(--nlw-ink-2); }
.nlw-pub { display: inline-block; padding: 1px 7px; border-radius: 999px; background: #F3EEE3; border: 1px solid var(--nlw-hair); font-size: 11.5px; font-weight: 700; color: var(--nlw-ink); }
.nlw-aptviews { margin-top: 10px; }
.nlw-aptviews .nlw-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; margin-top: 4px; }
.nlw-aptviews .nlw-chip, .nlw-planseg .nlw-chip { min-width: 0; padding-inline: 6px; justify-content: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.nlw-planseg { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 8px; }
.nlw-nw { white-space: nowrap; }
.nlw-plannote { margin-top: 6px; }
@media (max-width: 380px) { .nlw-plan { grid-template-columns: 124px minmax(0, 1fr); } .nlw-plansvg { width: 124px; height: 124px; } }
"""
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("world.js + world.css patched (v104.18)")
