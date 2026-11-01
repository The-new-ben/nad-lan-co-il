# -*- coding: utf-8 -*-
"""make deploy562.py from deploy561.py: 1.72.562 WhatsAppWordsBack (Ben 1.11.2026, late: "אני לא רציתי שתשנה את הניסוח בכפתורי
וואטסאפ", then "כן, תחזיר הכל כמו שהיה"). Every WhatsApp wording changed on 1.11 goes back to what it was before:
- inc/conversion-cta.php: the project pages' bar ("לקבלת מחירים, תוכניות והטבות", five languages) as before 1.72.557; the
  WhatsApp tap still reaches GA4 (1.72.558, not a wording);
- inc/i18n.php (hunks on the live text): the bar on every other page, as before 1.72.557;
- inc/project-stage.php, assets/project-stage/bridge.js, i18n/stage-dict.json (hunks on the live text): the stage buttons
  ("לקבלת תוכניות ומחירים") and the WhatsApp messages, as before 1.72.560;
- assets/project-stage/i18n-dom.js, inc/cta-sheet.php, assets/basket/basket.js: swapped whole with the versions from before 1.72.560.
The four article sentences on Rainbow and Ashira return through cms_words_560.py --undo (before this release). The inherited
checks that pinned the 1.11 words go back to the old ones; the checks 1.72.560 added are dropped."""
import hashlib, os, re
from urllib.parse import quote
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
FILES = ["inc/conversion-cta.php", "assets/project-stage/i18n-dom.js", "inc/cta-sheet.php", "assets/basket/basket.js"]
RELS = ["inc/i18n.php", "inc/project-stage.php", "assets/project-stage/bridge.js", "i18n/stage-dict.json"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
open(os.path.join(H, "ashira_562.py"), "w", encoding="utf-8", newline="\n").write(open(os.path.join(H, "ashira_562_src.py"), encoding="utf-8").read())
src = open(os.path.join(H, "deploy561.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("):
        lines[i] = "NEWFILES = set()"
    elif l.startswith("FILES = ["):
        lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["):
        lines[i] = "PHP_RELS = " + repr(RELS) + "  # 1.72.562: the four hunked files, restored from .bak562 on rollback (with the four swapped FILES)"
src = "\n".join(lines)
for a, b in [("1.72.561", "1.72.562"), ("ps561", "ps562"), ("bak561", "bak562"), ("make_deploy561", "make_deploy562"),
             ("deploy-result-561", "deploy-result-562"), ("speed-561", "speed-562"), ("posts-before-561", "posts-before-5_41"),
             ("deploy-result-560", "deploy-result-561"), ("1.72.560", "1.72.561")]:
    src = src.replace(a, b)
src = src.replace("posts-before-5_41", "posts-before-562")
src = re.sub(r"\?t561([a-z]?)=1", r"?t562\1=1", src)
src = re.sub(r"&t561([a-z]?)=1", r"&t562\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(561, 329, -1)", src)
assert n == 1, n
src, n = re.subn(r"import ashira_561 as PX  # noqa: E402 \([^)]*\)", "import ashira_562 as PX  # noqa: E402 (1.72.562: the WhatsApp words back, on the live text)", src)
assert n == 1, n
# 1) drop the checks 1.72.560 added (they pin the 1.11 words on the stage)
out, dropped = [], 0
for l in src.split("\n"):
    if l.startswith("    (") and any(m in l for m in ("<span>לקבלת מחירים ופרטים מהיזם</span>", "cta: 'לקבלת מחירים ופרטים מהיזם'",
                                                     "I would like prices and details for', 'les prix", '\'"לקבלת מחירים ופרטים מהיזם"\'',
                                                     "אשמח למחירים, לפרטים ולזמינות.")):
        dropped += 1
        continue
    out.append(l)
src = "\n".join(out)
assert dropped == 8, dropped
# 2) the bar's words back (longer forms first), the KH_WA line as it was before 1.72.557
OLD_HE, OLD_EN, OLD_FR, OLD_RU, OLD_AR = ("<b>לקבלת מחירים, תוכניות והטבות</b>", "<b>Prices, floor plans and offers</b>", "<b>Prix, plans et offres</b>",
                                          "<b>Цены, планировки и акции</b>", "<b>الأسعار والمخططات والعروض</b>")
for a, b in [("<b>לקבלת מחירים ופרטים מהיזם</b>", OLD_HE), ("<b>לקבלת מחירים ופרטים</b>", OLD_HE),
             ('aria-label="וואטסאפ · לקבלת מחירים ופרטים מהיזם"', 'aria-label="וואטסאפ · לקבלת מחירים, תוכניות והטבות"'),
             ('aria-label="וואטסאפ · לקבלת מחירים ופרטים"', 'aria-label="וואטסאפ · לקבלת מחירים, תוכניות והטבות"'),
             ("<b>Prices and details from the developer</b>", OLD_EN), ("<b>Prices and details</b>", OLD_EN),
             ('aria-label="WhatsApp: prices and details from the developer"', 'aria-label="WhatsApp — prices, floor plans and offers"'),
             ('aria-label="WhatsApp: prices and details"', 'aria-label="WhatsApp — prices, floor plans and offers"'),
             ("<b>Prix et détails du promoteur</b>", OLD_FR), ("<b>Prix et détails</b>", OLD_FR),
             ("<b>Цены и детали от застройщика</b>", OLD_RU), ("<b>Цены и подробности</b>", OLD_RU),
             ("<b>الأسعار والتفاصيل من المطوّر</b>", OLD_AR), ("<b>الأسعار والتفاصيل</b>", OLD_AR)]:
    src = src.replace(a, b)
_kh = [l for l in src.split("\n") if l.startswith("KH_WA = {")]
assert len(_kh) == 1, len(_kh)
src = src.replace(_kh[0], 'KH_WA = {"he": "' + OLD_HE + '", "en": "' + OLD_EN + '", "fr": "' + OLD_FR + '", "ru": "' + OLD_RU + '", "ar": "' + OLD_AR + '"}  # 1.72.562: the bar as before 1.11 (Ben)')
# the 1.72.557 checks that forbade the old words on Zohi and Rainbow
for a in (", 'תוכניות והטבות']", ", 'תוכניות והטבות', "):
    src = src.replace(a, "]" if a.endswith("]") else ", ")
# 3) the stage's button and messages back (1.72.560's own swaps, reversed)
for a, b, k in [("'לקבלת מחירים ופרטים מהיזם'", "'לקבלת תוכניות ומחירים'", 1),
                ("'Hello%2C%20I%20would%20like%20prices%20and%20details%20for%20Rainbow%20Tel%20Aviv%20%28nad-lan.co.il%29'",
                 "'Hello%2C%20I%20would%20like%20plans%20and%20prices%20for%20Rainbow%20Tel%20Aviv%20%28nad-lan.co.il%29'", 1),
                ("'Hello, I would like prices and details for the apartment on floor {floor}'",
                 "'Hello, I would like plans and prices for the apartment on floor {floor}'", 1),
                (quote("שלום, אשמח לקבל מחירים ופרטים על ", safe=""), quote("שלום, אשמח לקבל תוכניות ומחירים ב", safe=""), 2),
                (quote("хочу получить цены и подробности:", safe=""), quote("хочу получить планировки и цены:", safe=""), 1)]:
    assert src.count(a) == k, (a[:40], src.count(a))
    src = src.replace(a, b)
# nothing of the 1.11 words may stay in a check
for w in ("מחירים ופרטים מהיזם", "<b>לקבלת מחירים ופרטים", "Prices and details", "prices and details", "Prix et détails", "Цены и детали",
          "Цены и подробности", "цены и подробности", "الأسعار والتفاصيل", quote("מחירים ופרטים", safe="")):
    assert w not in src, w
anchor = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t562d=1',"
assert src.count(anchor) == 1, src.count(anchor)
ADD = [("/?t562r=1", [OLD_HE, 'aria-label="וואטסאפ · לקבלת מחירים, תוכניות והטבות"'], ["Fatal error", "<b>לקבלת מחירים ופרטים"]),
       ("/projects/dimri-yama-sde-dov/?t562r=1", [OLD_HE, "<span>לקבלת תוכניות ומחירים</span>", quote("שלום, אשמח לקבל תוכניות ומחירים ב", safe="")], ["Fatal error", "מחירים ופרטים מהיזם"]),
       ("/projects/ashira-sde-dov/?t562r=1", [OLD_HE, "<span>לקבלת תוכניות ומחירים</span>", "ולבקשת תוכניות ומחירים."], ["Fatal error", "מחירים ופרטים מהיזם", "ולבקשת מחירים ופרטים"]),
       ("/projects/rainbow-tel-aviv/?t562r=1", [OLD_HE, "<span>לקבלת תוכניות ומחירים</span>", "ולבקש בוואטסאפ תוכניות ומחירים לקומה"], ["Fatal error", "מחירים ופרטים מהיזם", "ולבקש בוואטסאפ מחירים ופרטים"]),
       ("/brokers/meital-katzir/?t562r=1", [OLD_HE], ["Fatal error", "<b>לקבלת מחירים ופרטים"]),
       ("/projects/zohi-sde-dov/?t562r=1", [OLD_HE, "window.gtag('event',n,p||{})"], ["Fatal error", "מחירים ופרטים מהיזם"]),
       ("/en/?t562r=1", [OLD_EN], ["Fatal error", "Prices and details"]),
       ("/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?t562r=1", ["cta: 'לקבלת תוכניות ומחירים'"], ["מחירים ופרטים"]),
       ("/wp-content/plugins/nadlan-config/assets/project-stage/i18n-dom.js?t562r=1", ["I would like plans and prices for"], ["prices and details"]),
       ("/wp-content/plugins/nadlan-config/assets/basket/basket.js?t562r=1", ["אשמח לתוכניות, למחירים ולזמינות."], ["אשמח למחירים, לפרטים"])]
src = src.replace(anchor, "".join("    (%r, %r, %r),\n" % t for t in ADD) + anchor)
src = re.sub(r'print\("RELEASE 1\.72\.562 LIVE: [^"]*"\)', 'print("RELEASE 1.72.562 LIVE: every WhatsApp wording is back to what it was before 1.11")', src)
open(os.path.join(H, "deploy562.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy562.py + ashira_562.py written; dropped the 1.72.560 checks:", dropped)
