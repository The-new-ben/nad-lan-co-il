# -*- coding: utf-8 -*-
"""quick gate for one ChatGPT part file (raw/<lang>-pN.html): words, artifacts, banned words, unmatched numbers"""
import io, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import check_article as CA
for path in sys.argv[1:]:
    lang = os.path.basename(path).split("-")[0]
    h = io.open(path, encoding="utf-8-sig").read()
    arts = re.findall(r"<small>\s*:chatgpt-content-reference[^<]*</small>|:chatgpt-content-reference\{[^}]*\}|【[^】]*】|turn\d+file\d+", h)
    tmp = os.path.join(HERE, "raw", "_tmp.html"); io.open(tmp, "w", encoding="utf-8").write(h)
    wc = json.loads(subprocess.run(["node", os.path.join(HERE, "wordcount.js"), tmp, lang], capture_output=True, text=True, encoding="utf-8").stdout)
    bans = CA.banned(h, lang); rows = CA.fact_check(h, lang); un = [r for r in rows if not r["ok"]]
    dash = h.count("—") + h.count("–")
    print("==", os.path.basename(path), "| words", wc["words_all"], "| sections", wc["sections"], "| artifacts", len(arts), "| dashes", dash, "| banned", len(bans), "| numbers", len(rows), "unmatched", len(un))
    for p, c in bans: print("   BANNED", p, "…", c)
    for r in un: print("   UNMATCHED", r["num"], "…", r["ctx"])
    os.remove(tmp)
