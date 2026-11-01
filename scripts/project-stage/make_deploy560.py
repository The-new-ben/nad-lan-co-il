# -*- coding: utf-8 -*-
"""make deploy560.py from deploy559.py: 1.72.560 StageButtonWords (Ben 1.11.2026: "כן, תשנה את זה לקבלת מחירים ופרטים מהיזם",
then "גם באשירה ובכל המקומות"). The big WhatsApp button under the opening paragraph of every stage page said "לקבלת תוכניות
ומחירים"; it now says "לקבלת מחירים ופרטים מהיזם", the floating bar's words (Claude Design v105.9). The WhatsApp messages ask for
prices and details instead of plans, in five languages. Files swapped whole (the drift check compares each with its last release):
- inc/project-stage.php: the two hero buttons, the WhatsApp message (he/en/fr/ru/ar);
- assets/project-stage/bridge.js: the stage's own button and its WhatsApp message;
- assets/project-stage/i18n-dom.js: the language pages' WhatsApp messages;
- i18n/stage-dict.json: the new button words in en/fr/ru/ar (the old key stays);
- inc/cta-sheet.php: the first choice in the WhatsApp sheet, five languages;
- assets/basket/basket.js: the basket's line and message.
The inherited checks that pinned the old words move to the new ones."""
import hashlib, os, re
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
# the repo holds newer, unreleased versions of project-stage.php, bridge.js and stage-dict.json (live = releases 472, 469, 361), so
# those three get hunks on their LIVE text (ashira_560_src.py, tested against live-560/); the other three equal live plus these
# words and are swapped whole
FILES = ["assets/project-stage/i18n-dom.js", "inc/cta-sheet.php", "assets/basket/basket.js"]
RELS = ["inc/project-stage.php", "assets/project-stage/bridge.js", "i18n/stage-dict.json"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
open(os.path.join(H, "ashira_560.py"), "w", encoding="utf-8", newline="\n").write(open(os.path.join(H, "ashira_560_src.py"), encoding="utf-8").read())
src = open(os.path.join(H, "deploy559.py"), encoding="utf-8").read()
lines = src.split("\n")
for i, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[i] = "PIN = " + repr(PIN)
    elif l.startswith("NEWFILES = set("):
        lines[i] = "NEWFILES = set()"
    elif l.startswith("FILES = ["):
        lines[i] = "FILES = " + repr(FILES)
    elif l.startswith("PHP_RELS = ["):
        lines[i] = "PHP_RELS = " + repr(RELS) + "  # 1.72.560: the three hunked files, restored from .bak560 on rollback (with the three swapped FILES)"
src = "\n".join(lines)
for a, b in [("1.72.559", "1.72.560"), ("ps559", "ps560"), ("bak559", "bak560"), ("make_deploy559", "make_deploy560"),
             ("deploy-result-559", "deploy-result-560"), ("speed-559", "speed-560"), ("posts-before-559", "posts-before-5_41"),
             ("deploy-result-558", "deploy-result-559"), ("1.72.558", "1.72.559")]:
    src = src.replace(a, b)
src = src.replace("posts-before-5_41", "posts-before-560")
src = re.sub(r"\?t559([a-z]?)=1", r"?t560\1=1", src)
src = re.sub(r"&t559([a-z]?)=1", r"&t560\1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(559, 329, -1)", src)
assert n == 1, n
src, n = re.subn(r"import ashira_559 as PX  # noqa: E402 \([^)]*\)", "import ashira_560 as PX  # noqa: E402 (1.72.560: the button words on the live stage files)", src)
assert n == 1, n
NEW = "לקבלת מחירים ופרטים מהיזם"
# the inherited checks: Rainbow's button and the Rainbow English page's WhatsApp messages
for a, b, k in [("'לקבלת תוכניות ומחירים'", "'" + NEW + "'", 1),
                ("'Hello%2C%20I%20would%20like%20plans%20and%20prices%20for%20Rainbow%20Tel%20Aviv%20%28nad-lan.co.il%29'",
                 "'Hello%2C%20I%20would%20like%20prices%20and%20details%20for%20Rainbow%20Tel%20Aviv%20%28nad-lan.co.il%29'", 1),
                ("'Hello, I would like plans and prices for the apartment on floor {floor}'",
                 "'Hello, I would like prices and details for the apartment on floor {floor}'", 1)]:
    assert src.count(a) == k, (a[:40], src.count(a))
    src = src.replace(a, b)
# the same messages pinned URL-encoded (Rainbow he t350/t351, DUO ru t350); the first run rolled back on them
from urllib.parse import quote
for a, b, k in [("שלום, אשמח לקבל תוכניות ומחירים ב", "שלום, אשמח לקבל מחירים ופרטים על ", 2),
                ("хочу получить планировки и цены:", "хочу получить цены и подробности:", 1)]:
    a, b = quote(a, safe=""), quote(b, safe="")
    assert src.count(a) == k, (a[:40], src.count(a))
    src = src.replace(a, b)
anchor = "    ('/wp-content/plugins/nadlan-config/assets/instruments/tools/dira.js?t560d=1',"
assert src.count(anchor) == 1, src.count(anchor)
OLD = "<span>לקבלת תוכניות ומחירים</span>"  # the page also prints a code comment that quotes the old words (conversion-cta.php)
ADD = [("/projects/dimri-yama-sde-dov/?t560c=1", ["<span>" + NEW + "</span>", "%D7%9E%D7%97%D7%99%D7%A8%D7%99%D7%9D%20%D7%95%D7%A4%D7%A8%D7%98%D7%99%D7%9D%20%D7%A2%D7%9C"], ["Fatal error", OLD]),
       ("/projects/ashira-sde-dov/?t560c=1", ["<span>" + NEW + "</span>"], ["Fatal error", OLD]),
       ("/projects/duo-tel-aviv/?t560c=1", ["<span>" + NEW + "</span>"], ["Fatal error", OLD]),
       ("/projects/rainbow-tel-aviv/?t560c=1", ["<span>" + NEW + "</span>", "ולבקש בוואטסאפ מחירים ופרטים לקומה"], ["Fatal error", OLD, "בוואטסאפ תוכניות ומחירים", "לבקש תוכניות ומחירים"]),
       ("/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?t560b=1", ["cta: '" + NEW + "'", "'שלום, אשמח לקבל מחירים ופרטים '"], ["תוכניות ומחירים"]),
       ("/wp-content/plugins/nadlan-config/assets/project-stage/i18n-dom.js?t560b=1", ["I would like prices and details for", "les prix et les détails de", "цены и подробности:", "الأسعار والتفاصيل"], ["plans and prices", "планировки и цены"]),
       ("/wp-content/plugins/nadlan-config/i18n/stage-dict.json?t560b=1", ['"' + NEW + '"', "Prices and details from the developer"], []),
       ("/wp-content/plugins/nadlan-config/assets/basket/basket.js?t560b=1", ["אשמח למחירים, לפרטים ולזמינות."], ["אשמח לתוכניות"])]
src = src.replace(anchor, "".join("    (%r, %r, %r),\n" % t for t in ADD) + anchor)
src = re.sub(r'print\("RELEASE 1\.72\.560 LIVE: [^"]*"\)', 'print("RELEASE 1.72.560 LIVE: the stage button says prices and details from the developer, on every stage page")', src)
open(os.path.join(H, "deploy560.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy560.py + ashira_560.py written")
