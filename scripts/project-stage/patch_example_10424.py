# -*- coding: utf-8 -*-
"""v104.24 (2.10.2026, the V2 loop turn 8, V4 step 5; HAD-380): the spa and the car park in the Kikar example apartment's 360.
The rooms are data (examples.json facilities: spa, parking, with their doors to the lift); this adds their words in five
languages, so a tile, a "בבניין" button and a lift stop appear for each. True facts only (docs/research/2026-09-30-kikar-hamedina/
facts.md): the spa and treatment rooms on one of the basement levels beside the pool and the gym; the parking levels underground,
two spaces per apartment. The count of parking levels (3 or 4 in the sources) is not stated.
  python patch_example_10424.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "project-stage", "world", "example.js")
s = open(P, encoding="utf-8").read()
if "v104.24" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


GYM = {"he": "      gym: ['חדר הכושר', 'חדר הכושר בקומת המרתף', 'באחת מקומות המרתף, ליד הבריכה והספא.'] },",
       "en": "      gym: ['Gym', 'The gym on a basement level', 'On one of the basement levels, beside the pool and the spa.'] },",
       "fr": "      gym: ['Salle de sport', 'La salle de sport au sous-sol', 'À l’un des niveaux de sous-sol, près de la piscine et du spa.'] },",
       "ru": "      gym: ['Тренажёрный зал', 'Тренажёрный зал на подземном этаже', 'На одном из подземных этажей, рядом с бассейном и спа.'] },",
       "ar": "      gym: ['النادي الرياضي', 'النادي الرياضي في الطابق السفلي', 'في أحد الطوابق السفلية، بجانب المسبح والسبا.'] },"}
MORE = {
    "he": "      spa: ['הספא', 'הספא בקומת המרתף', 'ספא וחדרי טיפולים, באחת מקומות המרתף, ליד הבריכה וחדר הכושר.'],\n"
          "      parking: ['החניון', 'החניון התת־קרקעי', 'קומות החניה מתחת לקרקע; שתי חניות לכל דירה.'] }, // v104.24",
    "en": "      spa: ['Spa', 'The spa on a basement level', 'A spa and treatment rooms, on one of the basement levels, beside the pool and the gym.'],\n"
          "      parking: ['Parking', 'The underground car park', 'The parking levels are underground; two spaces per apartment.'] }, // v104.24",
    "fr": "      spa: ['Spa', 'Le spa au sous-sol', 'Un spa et des salles de soins, à l’un des niveaux de sous-sol, près de la piscine et de la salle de sport.'],\n"
          "      parking: ['Parking', 'Le parking souterrain', 'Les niveaux de parking sont en sous-sol ; deux places par appartement.'] }, // v104.24",
    "ru": "      spa: ['Спа', 'Спа на подземном этаже', 'Спа и процедурные кабинеты на одном из подземных этажей, рядом с бассейном и тренажёрным залом.'],\n"
          "      parking: ['Паркинг', 'Подземный паркинг', 'Уровни паркинга находятся под землёй; два места на квартиру.'] }, // v104.24",
    "ar": "      spa: ['السبا', 'السبا في الطابق السفلي', 'سبا وغرف علاج في أحد الطوابق السفلية، بجانب المسبح والنادي الرياضي.'],\n"
          "      parking: ['موقف السيارات', 'موقف السيارات تحت الأرض', 'طوابق الموقف تحت الأرض؛ موقفان لكل شقة.'] }, // v104.24",
}
for L in GYM:
    sub(GYM[L], GYM[L][:-3] + ",\n" + MORE[L], "words " + L)
# the lift: the car park's stop says "קומות החניה", the other basement rooms "קומת המרתף"
WALK_END = {"he": "baseSub: 'קומת המרתף' }, // v104.23", "en": "baseSub: 'Basement level' }, // v104.23", "fr": "baseSub: 'Sous-sol' }, // v104.23",
            "ru": "baseSub: 'Подземный этаж' }, // v104.23", "ar": "baseSub: 'الطابق السفلي' }, // v104.23"}
PARK_SUB = {"he": "קומות החניה", "en": "Parking levels", "fr": "Niveaux de parking", "ru": "Уровни паркинга", "ar": "طوابق الموقف"}
for L in WALK_END:
    sub(WALK_END[L], WALK_END[L].replace(" }, // v104.23", ", parkSub: '" + PARK_SUB[L] + "' }, // v104.23 + v104.24 parkSub"), "parkSub " + L)
sub("""sub: f.id === 'lobby' ? T.walk.lobbySub : T.walk.baseSub }))) } : undefined,""",
    """sub: f.id === 'lobby' ? T.walk.lobbySub : f.id === 'parking' ? (T.walk.parkSub || T.walk.baseSub) : T.walk.baseSub }))) } : undefined, // v104.24 parkSub""", "lift parkSub")
open(P, "w", encoding="utf-8", newline="\n").write(s)
print("example.js patched (v104.24)")
