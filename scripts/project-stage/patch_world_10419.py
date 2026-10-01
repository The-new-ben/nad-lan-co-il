# -*- coding: utf-8 -*-
"""v104.19 (1.10.2026, the V2 loop turn 3, item V3; HAD-380): the chosen apartment's prices as public information.
Under the floor plan, once an apartment is chosen: the deals in the project (world.json model.plan.deals: three 4-room 140 m²
apartments on floors 38-39, ₪9.58M-10.63M, average ₪9.93M, about ₪71,000 per m²) and the towers' average (about ₪65,000 per m²;
₪80,000-150,000 on the upper floors and in the penthouses), headed "מידע גלוי". No source names on the page (the sources stay in
facts.md). The sizes line loses its own tag (one "מידע גלוי" for the block). Numbers in each language's own format; every number
range kept in reading order in RTL.
  python patch_world_10419.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world")
JS, CSS = os.path.join(D, "world.js"), os.path.join(D, "world.css")
s = open(JS, encoding="utf-8").read()
css = open(CSS, encoding="utf-8").read()
if "v104.19" in s or "v104.19" in css:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


WORDS = {
    "he": ("    aptViews: 'הנוף מהדירה', aptPick: 'הקישו על דירה בתוכנית הקומה', pubTag: 'מידע גלוי',",
           """    dealsH: 'עסקאות בפרויקט', money: (x) => `${x} מיליון ₪`, avgM: (x) => `ממוצע ${x} מיליון ₪`, // v104.19
    dealsWhat: (n, r, a, f0, f1) => `${n} עסקאות · ${r} חדרים, ${a} מ״ר · קומות ${f0}–${f1}`, ppm: (x) => `כ-${x} ₪ למ״ר`,
    towersAvg: (a, lo, hi) => `ממוצע העסקאות במגדלים כ-${a} ₪ למ״ר · בקומות הגבוהות ובפנטהאוזים ${lo}–${hi} ₪ למ״ר`,"""),
    "en": ("    aptViews: 'Views from the apartment', aptPick: 'Tap an apartment on the floor plan', pubTag: 'Public information',",
           """    dealsH: 'Deals in the project', money: (x) => `₪${x}M`, avgM: (x) => `average ₪${x}M`, // v104.19
    dealsWhat: (n, r, a, f0, f1) => `${n} deals · ${r} rooms, ${a} m² · floors ${f0}–${f1}`, ppm: (x) => `about ₪${x} per m²`,
    towersAvg: (a, lo, hi) => `Deals in the towers average about ₪${a} per m² · upper floors and penthouses ₪${lo}–${hi} per m²`,"""),
    "fr": ("    aptViews: 'Les vues de l’appartement', aptPick: 'Touchez un appartement sur le plan de l’étage', pubTag: 'Information publique',",
           """    dealsH: 'Ventes dans le projet', money: (x) => `${x} M₪`, avgM: (x) => `moyenne ${x} M₪`, // v104.19
    dealsWhat: (n, r, a, f0, f1) => `${n} ventes · ${r} pièces, ${a} m² · étages ${f0}–${f1}`, ppm: (x) => `environ ${x} ₪ le m²`,
    towersAvg: (a, lo, hi) => `Moyenne des ventes dans les tours : environ ${a} ₪ le m² · étages élevés et penthouses ${lo}–${hi} ₪ le m²`,"""),
    "ru": ("    aptViews: 'Виды из квартиры', aptPick: 'Нажмите на квартиру на плане этажа', pubTag: 'Открытые данные',",
           """    dealsH: 'Сделки в проекте', money: (x) => `${x} млн ₪`, avgM: (x) => `в среднем ${x} млн ₪`, // v104.19
    dealsWhat: (n, r, a, f0, f1) => `${n} сделки · ${r} комнаты, ${a} м² · этажи ${f0}–${f1}`, ppm: (x) => `около ${x} ₪ за м²`,
    towersAvg: (a, lo, hi) => `Средняя цена сделок в башнях около ${a} ₪ за м² · верхние этажи и пентхаусы ${lo}–${hi} ₪ за м²`,"""),
    "ar": ("    aptViews: 'الإطلالات من الشقة', aptPick: 'اضغطوا على شقة في مخطط الطابق', pubTag: 'معلومات منشورة',",
           """    dealsH: 'صفقات في المشروع', money: (x) => `${x} مليون ₪`, avgM: (x) => `المتوسط ${x} مليون ₪`, // v104.19
    dealsWhat: (n, r, a, f0, f1) => `${n} صفقات · ${r} غرف، ${a} م² · الطوابق ${f0}–${f1}`, ppm: (x) => `نحو ${x} ₪ للمتر المربع`,
    towersAvg: (a, lo, hi) => `متوسط الصفقات في الأبراج نحو ${a} ₪ للمتر المربع · الطوابق العليا والبنتهاوس ${lo}–${hi} ₪ للمتر المربع`,"""),
}
for k, (a, b) in WORDS.items():
    sub(a, a + "\n" + b, "words " + k)

# the sizes line without its own tag; the deals block under the plan (before the windows)
sub("""      `<div class="nlw-aptsize"><span class="nlw-pub">${esc(T.pubTag)}</span> ${esc(sz[0])} <span class="nlw-nw">${rng(sz[1])}</span> · <span class="nlw-nw">${rng(sz[2])}</span></div>`;""",
    """      `<div class="nlw-aptsize">${esc(sz[0])} <span class="nlw-nw">${rng(sz[1])}</span> · <span class="nlw-nw">${rng(sz[2])}</span></div>`;""", "sizes")
sub("""    return `<div class="nlw-planwrap"><div class="nlw-plan">${planSvg()}<div class="nlw-planinfo">${info}</div></div>${views}${seg}` +""",
    """    return `<div class="nlw-planwrap"><div class="nlw-plan">${planSvg()}<div class="nlw-planinfo">${info}</div></div>${u == null ? '' : dealsHtml(rng)}${views}${seg}` +""", "deals place")
sub("""  function bindPlan() {""", """  // v104.19 (V3): the deals in the project and the towers' average, as public information (world.json model.plan.deals; the sources
  // stay in facts.md, never named on the page); numbers in the language's own format
  const nfmt = (n) => Number(n).toLocaleString(lang === 'fr' ? 'fr-FR' : lang === 'ru' ? 'ru-RU' : 'en-US');
  const mfmt = (x) => (lang === 'fr' || lang === 'ru' ? String(x).replace('.', ',') : String(x));
  function dealsHtml(rng) {
    const Dl = PLAN().deals;
    if (!Dl) return '';
    return `<div class="nlw-deals"><div class="nlw-deals__h"><span class="nlw-pub">${esc(T.pubTag)}</span> ${esc(T.dealsH)}</div>` +
      `<div class="nlw-deals__v">${rng(T.money(`${mfmt(Dl.m[0])}–${mfmt(Dl.m[1])}`))} <small>· ${esc(T.avgM(mfmt(Dl.avg)))}</small></div>` +
      `<div class="nlw-deals__s">${rng(T.dealsWhat(Dl.n, Dl.rooms, Dl.sqm, Dl.floors[0], Dl.floors[1]))} · ${esc(T.ppm(nfmt(Dl.ppsqm)))}</div>` +
      `<div class="nlw-deals__s">${rng(T.towersAvg(nfmt(Dl.towers_ppsqm), nfmt(Dl.top_ppsqm[0]), nfmt(Dl.top_ppsqm[1])))}</div></div>`;
  }
  function bindPlan() {""", "deals html")
# the number ranges: also a range with thousands separators or decimals ("9.58–10.63", "80,000–150,000", "80 000–150 000")
sub("""    const rng = (t) => esc(t).replace(/(\\d+–\\d+)/g, '<bdi dir="ltr">$1</bdi>');""",
    """    const rng = (t) => esc(t).replace(/(\\d[\\d.,\\u00a0\\u202f]*–\\d[\\d.,\\u00a0\\u202f]*\\d|\\d+–\\d+)/g, '<bdi dir="ltr">$1</bdi>'); // v104.19: decimals and thousands""", "rng")
open(JS, "w", encoding="utf-8", newline="\n").write(s)

css = css.rstrip("\n") + "\n\n" + """/* v104.19 (V3): the deals in the project, public information, under the floor plan */
.nlw-deals { margin-top: 12px; padding: 10px 12px; border: 1px solid var(--nlw-hair); border-radius: 10px; background: #FBF8F2; display: grid; gap: 4px; }
.nlw-deals__h { font-size: 13px; font-weight: 700; color: var(--nlw-ink); display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.nlw-deals__v { font-size: 19px; font-weight: 800; color: var(--nlw-ink); line-height: 1.3; }
.nlw-deals__v small { font-size: 13px; font-weight: 600; color: var(--nlw-ink-2); }
.nlw-deals__s { font-size: 12.5px; line-height: 1.45; color: var(--nlw-ink-2); }
"""
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("world.js + world.css patched (v104.19)")
