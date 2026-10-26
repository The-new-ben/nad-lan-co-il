# -*- coding: utf-8 -*-
"""S1 predicted proof (local, reads only): builds preview/s1-page-proof.html = the served hub content with the new sections at their
anchors AND the tool's no-script summary in the shortcode's place (what Google reads on the live page after the release; the
summary comes from tool/registry-snippet.php run by php), serves the repo on 127.0.0.1:47933, then runs
  tools/depth_proof.py   --ours <the local proof page> --them <the same competitors as proof-before.md>  -> proof-predicted.md
  tools/fact_coverage.py --facts coverage-facts.json --urls <live hub> <local proof page> <competitors>  -> coverage.md
The after-release proof is the same two commands with --ours https://nad-lan.co.il/sde-dov/?x=<time>.
  python docs/research/2026-10-26-upgrades/s1-sde-dov/proof_s1.py"""
import functools, http.server, io, os, re, subprocess, sys, threading, time
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
PHP = "<?php function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');} require %r; echo s1_sdplan_summary(%r);" % (
    os.path.join(H, "tool", "registry-snippet.php").replace("\\", "/"), os.path.join(H, "data", "sdplan.json").replace("\\", "/"))
summary = subprocess.run(["php", "-r", PHP[6:]], capture_output=True, text=True, encoding="utf-8").stdout
assert "<table>" in summary, summary[:200]
pg = io.open(os.path.join(H, "preview", "s1-page-render.html"), encoding="utf-8").read()
TOOL = re.search(r'<section class="nli" dir="rtl" lang="he" aria-label="כל מגרש ברובע שדה דב">.*?</section>', pg, flags=re.S).group(0)
proof = pg.replace(TOOL, TOOL.replace("</h2></div></div></section>", "</h2>" + summary + "</div></div></section>"))
proof = re.sub(r'<script src="[^"]+" defer></script>', "", proof)  # Google's view: no scripts run
io.open(os.path.join(H, "preview", "s1-page-proof.html"), "w", encoding="utf-8", newline="").write(proof)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 47933), functools.partial(http.server.SimpleHTTPRequestHandler, directory=REPO))
threading.Thread(target=srv.serve_forever, daemon=True).start()
LOCAL = "http://127.0.0.1:47933/docs/research/2026-10-26-upgrades/s1-sde-dov/preview/s1-page-proof.html"
THEM = ["https://sdedov.co.il/", "https://sdedov.co.il/about/", "https://he.wikipedia.org/wiki/%D7%A0%D7%9E%D7%9C_%D7%94%D7%AA%D7%A2%D7%95%D7%A4%D7%94_%D7%93%D7%91_%D7%94%D7%95%D7%96",
        "https://www.prashkovsky.co.il/project/sde-dov-tel-aviv/", "https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx", "https://www.ynet.co.il/economy/article/sjh600ms11gx",
        "https://project-tlv.info/places/sde-dov/", "https://www.adam-ma.co.il/projects/%D7%A9%D7%93%D7%94-%D7%93%D7%91/", "https://sdedov.co.il/category/magazine/"]
env = dict(os.environ, PYTHONIOENCODING="utf-8")
r1 = subprocess.run([sys.executable, os.path.join(REPO, "tools", "depth_proof.py"), "--ours", LOCAL, "--them"] + THEM + ["--out", os.path.join(H, "proof-predicted.md")], capture_output=True, text=True, encoding="utf-8", env=env)
print(r1.stdout[-4000:], r1.stderr[-800:])
r2 = subprocess.run([sys.executable, os.path.join(REPO, "tools", "fact_coverage.py"), "--facts", os.path.join(H, "coverage-facts.json"), "--urls", "https://nad-lan.co.il/sde-dov/?x=%d" % time.time(), LOCAL] + THEM + ["--out", os.path.join(H, "coverage.md")], capture_output=True, text=True, encoding="utf-8", env=env)
print(r2.stdout[-6000:], r2.stderr[-800:])
srv.shutdown()
