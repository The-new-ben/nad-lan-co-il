# -*- coding: utf-8 -*-
"""v104.23 (2.10.2026, the V2 loop turn 7, V4 step 4; HAD-380): the building walk in the Kikar example apartment's 360
(the fleet's BuildingWalk v96 in tour.js: doors standing in the picture, a lift panel, a crossfade between illustrations).
  - the living room: "יציאה מהדירה · למעלית" at the hall door (examples.json pano.door, located in the render: yaw -128.2,
    pitch -2.75, by scripts/interior/kikar_interior.py's KH_DIAG locate);
  - the lobby, the pool and the gym: "למעלית" at their lift or entrance (examples.json facilities[].door, from kikar_facility.py's
    KF_LOCATE);
  - the lift: "לאן?" with floor 30 (the example apartment), the lobby (the entrance floor) and the basement's pool and gym;
  - every text of the viewer in the page's language (the lift, "אתם כאן", "חזרה" also fixes the language pages' back button).
  python patch_example_10423.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "project-stage", "world", "example.js")
s = open(P, encoding="utf-8").read()
if "v104.23" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


ANCH = {"he": "    inBuilding: 'בבניין', aptPlace: 'הדירה', facChip: 'מתקן לדוגמה', facCap: 'הדמיה להמחשה', // v104.22",
        "en": "    inBuilding: 'In the building', aptPlace: 'The apartment', facChip: 'Example facility', facCap: 'An illustration', // v104.22",
        "fr": "    inBuilding: 'Dans l’immeuble', aptPlace: 'L’appartement', facChip: 'Équipement à titre d’exemple', facCap: 'Illustration', // v104.22",
        "ru": "    inBuilding: 'В здании', aptPlace: 'Квартира', facChip: 'Пример', facCap: 'Иллюстрация', // v104.22",
        "ar": "    inBuilding: 'في المبنى', aptPlace: 'الشقة', facChip: 'مرفق للتوضيح', facCap: 'رسم توضيحي', // v104.22"}
WALK = {
    "he": "    walk: { exit: 'יציאה מהדירה', exitSub: 'למעלית', toLift: 'למעלית', title: 'לאן?', note: 'מעבר להמחשה', close: 'סגירה', here: 'אתם כאן', back: 'חזרה', floorN: (f) => `קומה ${f}`, aptSub: 'דירה לדוגמה', lobbySub: 'קומת הכניסה', baseSub: 'קומת המרתף' }, // v104.23",
    "en": "    walk: { exit: 'Leave the apartment', exitSub: 'to the lift', toLift: 'To the lift', title: 'Where to?', note: 'An illustrated move', close: 'Close', here: 'You are here', back: 'Back', floorN: (f) => `Floor ${f}`, aptSub: 'Example apartment', lobbySub: 'Entrance floor', baseSub: 'Basement level' }, // v104.23",
    "fr": "    walk: { exit: 'Sortir de l’appartement', exitSub: 'vers l’ascenseur', toLift: 'Vers l’ascenseur', title: 'Où aller ?', note: 'Déplacement illustré', close: 'Fermer', here: 'Vous êtes ici', back: 'Retour', floorN: (f) => `${f}e étage`, aptSub: 'Appartement témoin', lobbySub: 'Rez-de-chaussée', baseSub: 'Sous-sol' }, // v104.23",
    "ru": "    walk: { exit: 'Выйти из квартиры', exitSub: 'к лифту', toLift: 'К лифту', title: 'Куда?', note: 'Условный переход', close: 'Закрыть', here: 'Вы здесь', back: 'Назад', floorN: (f) => `${f}-й этаж`, aptSub: 'Пример квартиры', lobbySub: 'Входной этаж', baseSub: 'Подземный этаж' }, // v104.23",
    "ar": "    walk: { exit: 'الخروج من الشقة', exitSub: 'إلى المصعد', toLift: 'إلى المصعد', title: 'إلى أين؟', note: 'انتقال توضيحي', close: 'إغلاق', here: 'أنتم هنا', back: 'رجوع', floorN: (f) => `الطابق ${f}`, aptSub: 'شقة نموذجية', lobbySub: 'طابق الدخول', baseSub: 'الطابق السفلي' }, // v104.23",
}
for L in ANCH:
    sub(ANCH[L], ANCH[L] + "\n" + WALK[L], "words " + L)
# the rooms' doors to the lift
sub("""      src: U(f.base + '.webp'), small: U(f.base + '-2k.webp'), chip: T.facChip, caption: T.facCap + '.' }));""",
    """      src: U(f.base + '.webp'), small: U(f.base + '-2k.webp'), chip: T.facChip, caption: T.facCap + '.',
      doors: Array.isArray(f.door) ? [{ to: 'lift', at: f.door, label: T.walk.toLift }] : undefined })); // v104.23""", "fac doors")
# the lift's stops and the viewer's own words
sub("""        start: startId || p.base, places, placesLabel: T.inBuilding,""",
    """        start: startId || p.base, places, placesLabel: T.inBuilding,
        // v104.23 (BuildingWalk): the lift's stops: the example apartment's floor, the lobby, the basement's rooms
        lift: facs.length ? { title: T.walk.title, note: T.walk.note, stops: [{ floor: +ex.floor, label: T.walk.floorN(ex.floor), sub: T.walk.aptSub }].concat(
          facs.map((f) => ({ to: 'fac-' + f.id, label: T.fac[f.id][0], sub: f.id === 'lobby' ? T.walk.lobbySub : T.walk.baseSub }))) } : undefined,
        liftClose: T.walk.close, hereLabel: T.walk.here, backLabel: T.walk.back,""", "lift")
# the living room's door out of the apartment
sub("""        scenes: [{ id: p.base, dir: 'w', spot: 'living', floor: +ex.floor, title: T.panoTitle(o.tower, ex.floor), src: U(p.base + '.webp'), small: U(p.base + '-2k.webp'),""",
    """        scenes: [{ id: p.base, dir: 'w', spot: 'living', floor: +ex.floor, title: T.panoTitle(o.tower, ex.floor), src: U(p.base + '.webp'), small: U(p.base + '-2k.webp'),
          doors: facs.length && Array.isArray(p.door) ? [{ to: 'lift', at: p.door, label: T.walk.exit, sub: T.walk.exitSub }] : undefined, // v104.23""", "apt door")
open(P, "w", encoding="utf-8", newline="\n").write(s)
print("example.js patched (v104.23)")
