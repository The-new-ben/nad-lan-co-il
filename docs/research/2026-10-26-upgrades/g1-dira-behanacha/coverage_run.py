# -*- coding: utf-8 -*-
"""G1 fact coverage wrapper: runs tools/fact_coverage.py (unchanged) on coverage-facts.json and the same competitor set as
proof_run.py, with Hebrew URL paths percent-encoded (the shared tool sends them raw). gov.il and madlan answer 403 to scripts.
  python coverage_run.py [--ours URL] [--out FILE]"""
import os, sys, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
sys.path.insert(0, os.path.join(REPO, "tools")); sys.path.insert(0, H)
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
import fact_coverage as fc
_t = fc.text
def q(u):
    p = urllib.parse.urlsplit(u); return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), p.query, p.fragment))
fc.text = lambda u: _t(q(u))
import importlib.util
spec = importlib.util.spec_from_file_location("proof_run_list", os.path.join(H, "proof_run.py"))
src = open(os.path.join(H, "proof_run.py"), encoding="utf-8").read()
THEM = eval(src[src.index("THEM = [") + 7: src.index("]\nargs") + 1])
a = sys.argv[1:]
ours = a[a.index("--ours") + 1] if "--ours" in a else "https://nad-lan.co.il/dira-behanacha/"
out = a[a.index("--out") + 1] if "--out" in a else os.path.join(H, "coverage-before.md")
sys.argv = ["fact_coverage.py", "--facts", os.path.join(H, "coverage-facts.json"), "--urls", ours] + THEM + ["--out", out]
fc.main()
