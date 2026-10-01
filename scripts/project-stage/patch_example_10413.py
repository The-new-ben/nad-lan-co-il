# -*- coding: utf-8 -*-
"""v104.13 (1.10.2026, loop turn 22, HAD-375): the evening joins the example apartment's album.
The evening v2 render (interior mapping for the lit towers; 21.9, 19:00, the sun 5.06 deg below the horizon) ships at CARD SIZE
ONLY (the manifest's "max": 1200; no -2k file): the release gate's verdict. The time switch reads day · sunset · evening in five
languages (the plan's words); the world's night opens the album at evening, the album's evening sets the world to night; a
manifest without an evening falls back to sunset as before. Patches world/example.js and hamedina/tour/examples.json.
  python patch_example_10413.py"""
import io, os, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PS = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage")
JS = os.path.join(PS, "world", "example.js")
MAN = os.path.join(PS, "hamedina", "tour", "examples.json")
s = open(JS, encoding="utf-8").read()
if "v104.13" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


sub(" * (by day or at sunset), the corner bedroom,", " * (by day, at sunset or in the evening), the corner bedroom,", "head 1")
sub(" *   h.setTod('day' | 'sunset' | 'night'); h.close();", " *   h.setTod('day' | 'sunset' | 'night'); h.close();   (the world's night is the album's evening)", "head 2")
sub(" * (at 'night' the album opens at sunset and says so: its evening picture was not up to the bar);",
    " * (v104.13: at 'night' the album opens at evening, the 19:00 picture, shown at card size only; a manifest without an evening\n * opens at sunset as before);", "head 3")
for a, b, nm in (("tod: { day: 'יום', sunset: 'שקיעה' }", "tod: { day: 'יום', sunset: 'שקיעה', evening: 'ערב' }", "he"),
                 ("tod: { day: 'Day', sunset: 'Sunset' }", "tod: { day: 'Day', sunset: 'Sunset', evening: 'Evening' }", "en"),
                 ("tod: { day: 'Jour', sunset: 'Coucher du soleil' }", "tod: { day: 'Jour', sunset: 'Coucher du soleil', evening: 'Soir' }", "fr"),
                 ("tod: { day: 'День', sunset: 'Закат' }", "tod: { day: 'День', sunset: 'Закат', evening: 'Вечер' }", "ru"),
                 ("tod: { day: 'نهار', sunset: 'غروب' }", "tod: { day: 'نهار', sunset: 'غروب', evening: 'مساء' }", "ar")):
    sub(a, b, "words " + nm)
sub("""// the album has day and sunset (P9c review: the evening render's lit-window towers were below the owner's bar); a world at night
// opens the album at sunset, its switch says sunset, and the world follows it there
const TOD_OF_WORLD = { day: 'day', sunset: 'sunset', night: 'sunset' };
const WORLD_OF_TOD = { day: 'day', sunset: 'sunset' };""",
    """// v104.13 (loop turn 22): the album has day, sunset and evening (the evening v2: interior mapping for the lit towers, 19:00).
// The world's night opens it at evening and its evening sets the world to night; a manifest without an evening opens at sunset
const TOD_OF_WORLD = { day: 'day', sunset: 'sunset', night: 'evening' };
const WORLD_OF_TOD = { day: 'day', sunset: 'sunset', evening: 'night' };""", "maps")
sub("""  const picHtml = (base, kind, alt, sizes, eager) => {
    const ws = kind === 'still' ? `${U(base + '-thumb.webp')} 480w, ${U(base + '-card.webp')} 1200w, ${U(base + '-2k.webp')} 2048w`""",
    """  // v104.13: a still marked "max": 1200 in the manifest has no -2k (the evening: premium at card size, computed-looking at 2048)
  const picHtml = (base, kind, alt, sizes, eager, max) => {
    const ws = kind === 'still' && !(+max && +max <= 1200) ? `${U(base + '-thumb.webp')} 480w, ${U(base + '-card.webp')} 1200w, ${U(base + '-2k.webp')} 2048w`""", "pic")
sub("next.innerHTML = picHtml(base, kind, capOf(it), '(max-width: 899px) 100vw, 760px', eager);",
    "next.innerHTML = picHtml(base, kind, capOf(it), '(max-width: 899px) 100vw, 760px', eager, it.max);", "pic call")
sub("""    const living = ['day', 'sunset'].filter((t) => still('living', t));""",
    """    if (!still('living', tod)) tod = still('living', 'sunset') ? 'sunset' : 'day'; // v104.13: a manifest without this time
    const living = ['day', 'sunset', 'evening'].filter((t) => still('living', t));""", "living list")
open(JS, "w", encoding="utf-8", newline="\n").write(s)

t = open(MAN, encoding="utf-8").read()  # a text insertion keeps the manifest's own layout
a = '    { "base": "living-c30w-sunset", "room": "living", "time": "sunset", "hour": "17:36", "facing": 263.6 },\n'
if '"time": "evening"' not in t:
    if t.count(a) != 1:
        raise SystemExit("[manifest] anchor")
    t = t.replace(a, a + '    { "base": "living-c30w-evening", "room": "living", "time": "evening", "hour": "19:00", "facing": 260.6, "max": 1200 },\n')
    t = t.replace('"rendered": "30.9.2026, the sun of 21.9.2026 (Israel daylight time) over 32.087N 34.790E;',
                  '"rendered": "30.9.2026 (the evening 1.10.2026, interior mapping for the lit towers; card size only), the sun of 21.9.2026 (Israel daylight time) over 32.087N 34.790E (19:00: 5.06 degrees below the horizon);')
    json.loads(t)
    open(MAN, "w", encoding="utf-8", newline="\n").write(t)
print("example.js + examples.json patched (v104.13)")
