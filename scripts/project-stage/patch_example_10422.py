# -*- coding: utf-8 -*-
"""v104.22 (2.10.2026, the V2 loop turn 6, V4 step 3; HAD-380): the building's rooms in the example apartment's 360.
The manifest's example gains "facilities" (the tower C lobby, the basement pool and gym, rendered from the Kikar world by
scripts/interior/kikar_facility.py; illustrations: the builder puts the pool, gym and spa on a basement level, so they have no
window). The album's gallery strip gets one 360 tile per room; the fleet viewer (../tour.js, BuildingWalk v96) opens with the
apartment's living room and the rooms as one building: its "בבניין" bar walks between them; a tile opens at its room.
  python patch_example_10422.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "project-stage", "world", "example.js")
s = open(P, encoding="utf-8").read()
if "v104.22" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


W = {
    "he": "    styleNote: 'רעיון עיצוב להמחשה.', stylesN: (n) => `${n} סגנונות עיצוב`, // v104.21",
    "en": "    styleNote: 'A design idea, for illustration.', stylesN: (n) => `${n} design styles`, // v104.21",
    "fr": "    styleNote: 'Une idée d’aménagement, à titre d’illustration.', stylesN: (n) => `${n} styles d’aménagement`, // v104.21",
    "ru": "    styleNote: 'Идея дизайна, для иллюстрации.', stylesN: (n) => `${n} стиля дизайна`, // v104.21",
    "ar": "    styleNote: 'فكرة تصميم للتوضيح.', stylesN: (n) => `${n} أنماط تصميم`, // v104.21",
}
ADD = {
    "he": """    inBuilding: 'בבניין', aptPlace: 'הדירה', facChip: 'מתקן לדוגמה', facCap: 'הדמיה להמחשה', // v104.22
    fac: { lobby: ['הלובי', 'הלובי במגדל C', 'לובי בקומת הכניסה, עם עמדת שמירה.'], pool: ['הבריכה', 'הבריכה בקומת המרתף', 'הבריכה, חדר הכושר והספא נמצאים באחת מקומות המרתף.'],
      gym: ['חדר הכושר', 'חדר הכושר בקומת המרתף', 'באחת מקומות המרתף, ליד הבריכה והספא.'] },""",
    "en": """    inBuilding: 'In the building', aptPlace: 'The apartment', facChip: 'Example facility', facCap: 'An illustration', // v104.22
    fac: { lobby: ['Lobby', 'The lobby of tower C', 'The entrance-floor lobby, with a concierge desk.'], pool: ['Pool', 'The pool on a basement level', 'The pool, the gym and the spa are on one of the basement levels.'],
      gym: ['Gym', 'The gym on a basement level', 'On one of the basement levels, beside the pool and the spa.'] },""",
    "fr": """    inBuilding: 'Dans l’immeuble', aptPlace: 'L’appartement', facChip: 'Équipement à titre d’exemple', facCap: 'Illustration', // v104.22
    fac: { lobby: ['Hall', 'Le hall de la tour C', 'Le hall d’entrée, avec un poste d’accueil.'], pool: ['Piscine', 'La piscine au sous-sol', 'La piscine, la salle de sport et le spa sont à l’un des niveaux de sous-sol.'],
      gym: ['Salle de sport', 'La salle de sport au sous-sol', 'À l’un des niveaux de sous-sol, près de la piscine et du spa.'] },""",
    "ru": """    inBuilding: 'В здании', aptPlace: 'Квартира', facChip: 'Пример', facCap: 'Иллюстрация', // v104.22
    fac: { lobby: ['Лобби', 'Лобби башни C', 'Лобби на входном этаже, с постом охраны.'], pool: ['Бассейн', 'Бассейн на подземном этаже', 'Бассейн, тренажёрный зал и спа находятся на одном из подземных этажей.'],
      gym: ['Тренажёрный зал', 'Тренажёрный зал на подземном этаже', 'На одном из подземных этажей, рядом с бассейном и спа.'] },""",
    "ar": """    inBuilding: 'في المبنى', aptPlace: 'الشقة', facChip: 'مرفق للتوضيح', facCap: 'رسم توضيحي', // v104.22
    fac: { lobby: ['الردهة', 'ردهة البرج C', 'ردهة طابق الدخول، مع مكتب حراسة.'], pool: ['المسبح', 'المسبح في الطابق السفلي', 'المسبح والنادي الرياضي والسبا في أحد الطوابق السفلية.'],
      gym: ['النادي الرياضي', 'النادي الرياضي في الطابق السفلي', 'في أحد الطوابق السفلية، بجانب المسبح والسبا.'] },""",
}
for L in W:
    sub(W[L], W[L] + "\n" + ADD[L], "words " + L)
# the gallery strip: one 360 tile per room of the building
sub("""      ...['bedroom', 'balcony'].filter((r) => ex.stills.some((s) => s.room === r)).map((r) => {""",
    """      // v104.22: the building's rooms (360), after the apartment's own pictures
      ...['bedroom', 'balcony'].filter((r) => ex.stills.some((s) => s.room === r)).map((r) => {""", "strip mark")
sub("""    ].join('');
    const twist = (ex.twist || [])""", """      ...(Array.isArray(ex.facilities) ? ex.facilities : []).filter((f) => T.fac[f.id]).map((f) => `<button class="nlex__tile nlex__tile--360" type="button" data-fac="fac-${esc(f.id)}"><span class="nlex__thumb"><img src="${esc(U(f.base + '-thumb.webp'))}" width="480" height="270" alt="" decoding="async" loading="lazy"><b class="nlex__360b">${ICON360}<span dir="ltr">360°</span></b></span><span class="nlex__tl">${esc(T.fac[f.id][0])}</span></button>`),
    ].join('');
    const twist = (ex.twist || [])""", "fac tiles")
sub("""    for (const b of body.querySelectorAll('[data-pano]')) b.addEventListener('click', () => open360(b));""",
    """    for (const b of body.querySelectorAll('[data-pano]')) b.addEventListener('click', () => open360(b));
    for (const b of body.querySelectorAll('[data-fac]')) b.addEventListener('click', () => open360(b, b.dataset.fac)); // v104.22""", "fac bind")
# the viewer: the living room (the apartment) and the building's rooms, one building
sub("""  function open360(btn) {
    if (!ex || !ex.pano) return;
    const p = ex.pano;""", """  function open360(btn, startId) {
    if (!ex || !ex.pano) return;
    const p = ex.pano;
    // v104.22: the building's rooms (the lobby, the basement pool and gym), illustrations, as 'fac' scenes of the same viewer
    const facs = (Array.isArray(ex.facilities) ? ex.facilities : []).filter((f) => T.fac[f.id]);
    const facScenes = facs.map((f) => ({ id: 'fac-' + f.id, group: 'fac', dir: 'fac-' + f.id, spot: 'fac', title: T.fac[f.id][1], note: T.fac[f.id][2],
      src: U(f.base + '.webp'), small: U(f.base + '-2k.webp'), chip: T.facChip, caption: T.facCap + '.' }));
    const places = facs.length ? [{ apt: true, label: T.aptPlace, floor: +ex.floor, dir: 'w' }].concat(facs.map((f) => ({ to: 'fac-' + f.id, label: T.fac[f.id][0] }))) : undefined;""", "open360 head")
sub("""        scenes: [{ id: p.base, dir: 'w', spot: 'living', title: T.panoTitle(o.tower, ex.floor), src: U(p.base + '.webp'), small: U(p.base + '-2k.webp'),""",
    """        start: startId || p.base, places, placesLabel: T.inBuilding,
        scenes: [{ id: p.base, dir: 'w', spot: 'living', floor: +ex.floor, title: T.panoTitle(o.tower, ex.floor), src: U(p.base + '.webp'), small: U(p.base + '-2k.webp'),""", "scenes head")
sub("""            id: st.id, label: T.styleNames[st.id] || st.id, thumb: U(st.base + '-thumb.webp'), src: U(st.base + '.webp'), small: U(st.base + '-2k.webp') }))) : undefined }],""",
    """            id: st.id, label: T.styleNames[st.id] || st.id, thumb: U(st.base + '-thumb.webp'), src: U(st.base + '.webp'), small: U(st.base + '-2k.webp') }))) : undefined }].concat(facScenes),""", "scenes tail")
open(P, "w", encoding="utf-8", newline="\n").write(s)
print("example.js patched (v104.22)")
