# -*- coding: utf-8 -*-
"""HAD-801: the /sde-dov/ entry clip re-recorded after the seated cyclist + delivery courier (23.11.2026) under NEW names
(sde-dov-2036-entry-walk-v2-*.mp4) so no browser keeps the old take from its cache. One hunk on inc/sdedov-teaser.php (live 74eb6011a9).
  python make_deploy_clipv2.py <prev release number>"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = int(sys.argv[1]); NEW = PREV + 1
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REL = "inc/sdedov-teaser.php"
LIVE = open(os.path.join(REPO, "plugins", "nadlan-config", *REL.split("/")), encoding="utf-8").read()
MD5 = hashlib.md5(LIVE.encode("utf-8")).hexdigest()
assert MD5.startswith("74eb6011a9"), ("the repo copy is not the 1.72.748 live text", MD5)
A = "'media/wordpress/clips/sde-dov-2036-entry-walk-'"
assert LIVE.count(A) == 1
H = [(A, "'media/wordpress/clips/sde-dov-2036-entry-walk-v2-'")]
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/sde-dov/?tclip2=1', ['data-nlq', 'id=\"walk\"', 'nlqw-clip-js', 'media/wordpress/clips/sde-dov-2036-entry-walk-v2-phone.mp4', 'הדמיה להמחשה, על פי התכנית', 'class=\"nlam'], %s, []),\n"
        "    ('/?tclip2=1', ['nlhp-svcard--tour'], ['Fatal error', 'sde-dov-2036-entry-walk-'], []),\n"
        "    ('/tour/sde-dov/media/wordpress/clips/sde-dov-2036-entry-walk-v2-phone.mp4', [], [], []),\n"
        "    ('/tour/sde-dov/?tclip2=1', ['walk-DGQMIG45-r3.js', 'הדמיה להמחשה, על פי התכנית'], ['Fatal error'], []),\n") % BAD
kl_release.build_release(PREV, NEW, [], [], {REL: H}, {REL: MD5}, ROWS,
                         "the /sde-dov/ entry clip shows the seated cyclist and the delivery courier (new clip names)",
                         "HAD-801 entry clip v2")
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy%d.py" % NEW)
_t = open(_d, encoding="utf-8").read()
_old = "('/sde-dov/?tclip=1', ['data-nlq', 'id=\"walk\"', 'nlqw-clip', 'media/wordpress/clips/sde-dov-2036-entry-walk-phone.mp4'"
assert _t.count(_old) == 1, _t.count(_old)
_t = _t.replace(_old, _old.replace("entry-walk-phone.mp4", "entry-walk-v2-phone.mp4"))
print("inherited clip row moved to the v2 name")
_a = '            s, html = page(path + sep + "nlv=" + tag)\n'
if _t.count(_a) == 1 and "time.sleep(0.7)" not in _t:
    _t = _t.replace(_a, '            time.sleep(0.7)\n' + _a + '            for _k in range(3):\n                if s != 429:\n                    break\n'
                    '                print(f"[page] 429 on {path[:70]}: waiting {30 * (_k + 1)} s")\n                time.sleep(30 * (_k + 1))\n'
                    '                s, html = page(path + sep + "nlv=" + tag + "q%d" % _k)\n')
    print("runner: 0.7 s pause per check, 429 retried")
open(_d, "w", encoding="utf-8", newline=chr(10)).write(_t)
