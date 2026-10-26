# -*- coding: utf-8 -*-
"""G5 honesty statement, predicted: runs tools/depth_proof.py and tools/fact_coverage.py (both unchanged) with OUR page = the local
preview (served from the repo; the tool and listings are mounted as on the live page: the tool's summary is not in the preview, so
the live raw HTML will hold slightly more), against the pages Google shows for the head terms and for the tail the page targets.
Hebrew paths are percent-encoded (the shared tools send them raw). Madlan (Cloudflare) and Yad2 (Radware CAPTCHA) refuse scripts:
Madlan's numbers come from the real-Chrome read (raw/g5/comp/c02-chrome-read.md); Yad2 could not be read at all.
  python proof_run.py            -> proof-predicted.md + coverage-predicted.md
  python proof_run.py --live     -> the same against https://nad-lan.co.il/דירות-להשכרה/ after the release (proof-after.md, coverage-after.md)"""
import functools, http.server, os, sys, threading, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
sys.path.insert(0, os.path.join(REPO, "tools"))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
import depth_proof as dp, fact_coverage as fc
def q(u):
    p = urllib.parse.urlsplit(u); return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), p.query, p.fragment))
_f, _t = dp.fetch, fc.text
dp.fetch = lambda u: _f(q(u)); fc.text = lambda u: _t(q(u))
THEM = [
    "https://www.homeless.co.il/rent/",                                   # דירה להשכרה #3, listings board
    "https://www.onmap.co.il/search/homes/rent",                          # דירה להשכרה #20 (TA #7)
    "https://www.komo.co.il/code/nadlan/apartments-for-rent.asp?nehes=1", # דירה להשכרה #8
    "https://isratowers.co.il/rent/",                                     # דירה להשכרה #18
    "https://www.mako.co.il/finances-real-estate/Article-d3c7171678afc71027.htm",  # the only article in the top 20 (#19)
    "https://www.mako.co.il/news-money/consumer/Article-a4637aada5f6f91027.htm",   # כמה עולה לשכור דירה #4, AIO source
    "https://www.ynet.co.il/economy/article/yokra14892044",               # שכר דירה ממוצע #2, AIO source on 3 queries
    "https://scoutrbot.com/data/rent-report",                             # מחירי שכירות #8, AIO source
    "https://seenker.com/tools/rent-calculator",                          # מחשבון שכר דירה #3
    "https://www.dirobot.co.il/",                                         # מחירי שכירות #4
    "https://www.hon.co.il/מדד-שכר-דירה/",                                 # מחירי שכירות #7, מחשבון שכר דירה #1 is hon too
    "https://www.kolzchut.org.il/he/הגבלת_סכום_הערובה_שמותר_לדרוש_משוכר_דירה",  # ערבות לשכירות #5
    "https://www.wecheck.co.il/blog/חוק-שכירות-הוגנת/",                    # חוק שכירות הוגנת, AIO source
    "https://www.diffe-rent.co.il/המדריך-להשכרה-מוצלחת/חוזה-וביטחונות/ערבויות-לשכירות/",  # ערבות לשכירות #2
    "https://jus-tice.co.il/fair-rental-law-2017/",                       # חוק שכירות הוגנת #6 (Ben's other site)
]
LIVE = "--live" in sys.argv
if LIVE:
    ours = "https://nad-lan.co.il/דירות-להשכרה/"; tag = "after"
else:
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47959), functools.partial(http.server.SimpleHTTPRequestHandler, directory=REPO))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    ours = "http://127.0.0.1:47959/docs/research/2026-10-26-upgrades/g5-rentals/preview/g5-page-render.html"; tag = "predicted"
sys.argv = ["depth_proof.py", "--ours", ours, "--them"] + THEM + ["--out", os.path.join(H, "proof-%s.md" % tag)]
dp.main()
sys.argv = ["fact_coverage.py", "--facts", os.path.join(H, "coverage-facts.json"), "--urls", ours] + THEM + ["--out", os.path.join(H, "coverage-%s.md" % tag)]
fc.main()
