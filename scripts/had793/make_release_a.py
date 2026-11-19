# -*- coding: utf-8 -*-
"""HAD-793 release A (packages 7-8 of the long film, 19.11.2026), generates scripts/project-stage/deploy<new>.py:
  SWAP inc/page-lang.php: on an English, French, Russian or Arabic page the author's name follows the page's language (block, meta author,
       share labels, Person and Article schema; ben-betesh = "Ben Betesh"); article title and headings of en/fr/ru posts in IBM Plex Sans;
       on a wide screen the article's contents beside the opening (it scrolls with the page, nothing floats). Gap 24.
  SWAP inc/near-finder.php (v4 payload: "areas", the city median of a 4-room home from the site's own value.json, cache key nadlan_nf_v4),
       assets/near-finder/finder.js + finder.css (the few-listings state: new projects as a background layer, city medians as map labels,
       the "what else is here" block under the list). Gaps 25 and 31.
  SWAP assets/instruments/tools/mquick.js (v6: French and Russian dictionaries) and HUNKS on the live inc/instruments.php
       (instruments_hunks.py: fr / ru blocks for tools, the mquick fr + ru names, LTR section, Latin fonts, FAQ headings). Gap 23;
       the /fr/ and /ru/ mortgage calculator pages are created after this release by scripts/had793/pages_fr_ru.py.
  SWAP assets/project-stage/bridge.js, built on the LIVE text (scripts/had793/live/bridge.js; the repo copy carries unreleased
       "local only" batches): the view from the floor gains "today / by the plan" (the quarter's planned projects as schematic masses)
       and eight directions. Gap 22.
  SWAP assets/tours/sde-dov-tour.html: people with a body and a walking gait, beach life, the walk reaches the sea ("אל הים",
       ?focus=sea), and the reduced-motion boot fix (the tour did not start for visitors who ask for reduced motion). Gap 21.
  python scripts/had793/make_release_a.py <prev> <new>"""
import ast, os, sys, hashlib
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PS = os.path.join(REPO, "scripts", "project-stage"); sys.path.insert(0, PS); sys.path.insert(0, H)
import kl_release  # noqa: E402
import instruments_hunks as IH  # noqa: E402
PREV, NEW = int(sys.argv[1]), int(sys.argv[2])
F = ["inc/page-lang.php", "inc/near-finder.php", "assets/near-finder/finder.js", "assets/near-finder/finder.css", "assets/instruments/tools/mquick.js",
     "assets/project-stage/bridge.js", "assets/tours/sde-dov-tour.html"]
BR = os.path.join(H, "live", "bridge.js")
A = "/wp-content/plugins/nadlan-config/assets/near-finder/"
M = "/wp-content/plugins/nadlan-config/assets/instruments/tools/mquick.js"
T = "t%da" % NEW
V = "1.72.%d" % NEW
rows = [
    (A + "finder.js?%s=1" % T, ['function drawCtx(', 'nlnf-few__go', 'NadLan near finder v1'], ['Fatal error']),
    (A + "finder.css?%s=1" % T, ['.nlnf-few__go', '.nlnf-lg--ctx'], ['Fatal error']),
    ("/wp-json/nadlan/v1/near-finder?%s=1" % T, ['"areas":[{"n":', '"r4":5229800', '"areas_src":'], ['Fatal error']),
    ("/properties/?%s=1" % T, ['id="nlnf-app"', 'near-finder/finder.js?ver=' + V], ['Fatal error', 'Warning</b>', 'Notice</b>']),
    ("/israel-mortgage-non-residents/?%s=1" % T, ['id="nlpglang-latin"', '<meta name="author" content="Ben Betesh"', '"name":"Ben Betesh"', 'israel-mortgage-ltv-caps-2026-v2'],
     ['Fatal error', 'content="בן בטש"', '"name":"בן בטש"', '>בן בטש</a>']),
    ("/en/mortgage-calculator/?%s=1" % T, ['<html lang="en"', 'Quick mortgage calculator', 'tools/mquick.js?ver=' + V], ['Fatal error', 'Warning</b>']),
    ("/mortgage-calculator/?%s=1" % T, ['data-nli="mquick"', 'מחשבון משכנתא מהיר', '<section class="nli" dir="rtl" lang="he"'], ['Fatal error', 'Warning</b>', 'Simulateur de crédit']),
    (M + "?%s=1" % T, ['function quarterX(', 'Simulateur de crédit immobilier', 'Ипотечный калькулятор', 'Quick mortgage calculator'], ['Fatal error']),
    ("/wp-content/plugins/nadlan-config/assets/project-stage/bridge.js?%s=1" % T, ['function planGeo(', 'nl-ps-plan', 'function walkOpts(startId)', 'alReady'], ['Fatal error']),
    ("/projects/rainbow-tel-aviv/?%s=1" % T, ['id="nlps-view"', 'bridge.js?ver=' + V], ['Fatal error', 'Warning</b>']),
    ("/tour/sde-dov/?%s=1" % T, ['function walkToSea(', 'personShader(M_WALK, true)', 'id="mmSea"', '<h2>שלושה פרויקטים ברובע</h2>', 'NARR_FIX_BASE'],
     ['Fatal error', "if (typeof narrPlay === 'function') { narrCh = station;"]),
]
ROWS = "".join("    (%r, %r, %r, []),\n" % r for r in rows)
kl_release.build_release(PREV, NEW, F, [], {"inc/instruments.php": IH.H}, {"inc/instruments.php": IH.LIVE_MD5}, ROWS,
                         "author name in the page's language, the few-listings map on /properties/, the mortgage calculator in French and Russian, the floor view by the plan, the Sde Dov walk to the sea",
                         "HAD-793 release A: packages 7-8 of the long film")
p = os.path.join(PS, "deploy%d.py" % NEW)
s = open(p, encoding="utf-8").read()
# 1. the inherited pin on inc/near-finder.php (written by 1.72.595) accepts this release's text too, so later runners are not blocked
new_md5 = hashlib.md5(open(os.path.join(REPO, "plugins", "nadlan-config", "inc", "near-finder.php"), "rb").read()).hexdigest()
a = 'if _nf.get("missing") or _nf.get("md5") != "c7fffca3f06350211193fa0ded50295c":'
b = 'if _nf.get("missing") or _nf.get("md5") not in ("c7fffca3f06350211193fa0ded50295c", "%s"):  # 1.72.%d (HAD-793) writes it' % (new_md5, NEW)
if s.count(a) == 1:
    s = s.replace(a, b)
else:
    assert 'if _nf.get("missing") or _nf.get("md5") not in (' in s, "the near-finder pin is not where it was"
# 2. bridge.js ships from the live-based copy: the runner reads it from OVR only while its md5 is the pinned one
bmd5 = hashlib.md5(open(BR, "rb").read()).hexdigest()
lines = s.split("\n"); hit = 0
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        pin = ast.literal_eval(l[len("PIN = "):]); pin["assets/project-stage/bridge.js"] = bmd5; lines[k] = "PIN = " + repr(pin); hit += 1
s = "\n".join(lines)
assert hit == 1, hit
a = '    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()\n'
b = ('    _o = OVR.get(rel)  # HAD-793: a file built on the LIVE text, used only while its md5 is the pinned one\n'
     '    NEW[rel] = open(_o if (_o and os.path.exists(_o) and md5(open(_o, "rb").read()) == PIN.get(rel)) else os.path.join(PLUG, *rel.split("/")), "rb").read()\n')
assert s.count(a) == 1, s.count(a)
s = s.replace(a, b)
a2 = "\nNEW = {}\nfor rel in FILES:\n"
assert s.count(a2) == 1, s.count(a2)
s = s.replace(a2, "\nOVR = {'assets/project-stage/bridge.js': os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts', 'had793', 'live', 'bridge.js')}\nNEW = {}\nfor rel in FILES:\n")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("deploy%d.py written; near-finder pin also accepts %s; bridge.js from the live-based copy %s" % (NEW, new_md5[:10], bmd5[:10]))
