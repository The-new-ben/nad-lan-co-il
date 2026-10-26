# -*- coding: utf-8 -*-
"""G1 depth proof wrapper: runs tools/depth_proof.py (unchanged) on the G1 competitor set, with Hebrew URL paths percent-encoded
(the shared tool sends them raw and urllib refuses non-ASCII paths, so kolzchut, alonim, mashcantaman, meyda and wikipedia
were silently skipped). gov.il and madlan.co.il answer 403 to scripts and are measured from the real-Chrome reads instead
(see dna.md section 3). --ours may be a local preview URL (http://127.0.0.1:PORT/...) for the predicted after-proof.
  python docs/research/2026-10-26-upgrades/g1-dira-behanacha/proof_run.py [--ours URL] [--out FILE]"""
import os, sys, urllib.parse, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
sys.path.insert(0, os.path.join(REPO, "tools"))
import depth_proof as dp
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
_fetch = dp.fetch
def q(u):
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), p.query, p.fragment))
dp.fetch = lambda u: _fetch(q(u))
THEM = [
    "https://www.kolzchut.org.il/he/דירה_בהנחה_(מחיר_למשתכן)",      # 7 דירה בהנחה, AIO source on מחיר למשתכן
    "https://www.shikun-maof.co.il/dira/",                              # 3 דירה בהנחה, AIO source
    "https://alonim.co.il/דירה-בהנחה/",                                 # 4 דירה בהנחה, AIO source
    "https://mashcantaman.co.il/כל-מכרזי-מחיר-למשתכן/",                 # 5 מחיר למשתכן (3 mobile)
    "https://mgad.co.il/meshtakenn/",                                   # 7 מחיר למשתכן
    "https://www.midrag.co.il/Midragonim/Answer/17081",                 # 9 מחיר למשתכן
    "https://www.israhc.org/affordablehousingindexml",                  # 10 מחיר למשתכן
    "https://akc.co.il/subsidized-housing-lotteries/",                  # 14 מחיר למשתכן
    "https://www.meyda.org.il/משכנתא/אתר-הגרלות-מחיר-למשתכן/",          # 16 מחיר למשתכן
    "https://www.mizrahi-tefahot.co.il/mortgages/magazine/mishtaken/",  # AIO source, 18 הגרלות
    "https://he.wikipedia.org/wiki/מחיר_למשתכן",                        # AIO source
    "https://www.nadlancenter.co.il/article/350",                       # 12 הגרלות, 2 מחיר מטרה
    "https://www.nadlancenter.co.il/article/14284",                     # 2 דירה בהנחה mobile
    "https://www.mako.co.il/finances-real-estate/Article-3621b87eb1e5e91027.htm",  # 7 דירה בהנחה mobile
    "https://wizbid.co.il/lotteries/1544",                              # programmatic lottery pages with odds
]
args = sys.argv[1:]
ours = args[args.index("--ours") + 1] if "--ours" in args else "https://nad-lan.co.il/dira-behanacha/"
out = args[args.index("--out") + 1] if "--out" in args else os.path.join(H, "proof-before.md")
sys.argv = ["depth_proof.py", "--ours", ours, "--them"] + THEM + ["--out", out]
dp.main() if hasattr(dp, "main") else None
