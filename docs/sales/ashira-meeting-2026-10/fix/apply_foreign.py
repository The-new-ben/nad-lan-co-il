# -*- coding: utf-8 -*-
"""HAD-543 (Ben 18.10 "start fixing before the meeting"): wording slips on the four foreign Ashira posts. Exact replacements on
the live raw (backups live-<lang>-<id>.raw), guarded: live must equal the backup, POST 200, fetch-back equal, title/canonical/H1
unchanged, old phrase gone. Manual rollback: --rollback posts the backups back."""
import os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "af"}; exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
JOBS = {
 "en": (4927, "ashira-sde-dov-en", [("collagen tanning area", "collagen light-therapy room"), ("collagen tanning", "collagen light therapy"),
        ("Walking away is a valid outcome of due diligence.", "The right apartment is the one that fits your needs.")]),
 "fr": (4926, "ashira-sde-dov-fr", [("un espace de bronzage au collagène", "une cabine de luminothérapie au collagène")]),
 "ru": (4924, "ashira-sde-dov-ru", [("коллагеновый солярий", "коллагенарий (светотерапия)")]),
 "ar": (4925, "ashira-sde-dov-ar", [("تسمير بالكولاجين", "علاج ضوئي بالكولاجين")]),
}
rollback = "--rollback" in sys.argv
get = lambda slug: urllib.request.urlopen(urllib.request.Request(f"https://nad-lan.co.il/projects/{slug}/?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0 Chrome/128"}), timeout=90).read().decode("utf-8", "replace")
inv = lambda h: (re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip(), (re.search(r'rel="canonical" href="([^"]+)"', h) or [None, None])[1], h.count("<h1"))
fails = 0
for lang, (pid, slug, reps) in JOBS.items():
    backup = open(os.path.join(HERE, f"live-{lang}-{pid}.raw"), "rb").read().decode("utf-8")
    s, d, _ = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit"); cur = d["content"]["raw"]
    if rollback:
        target = backup
    else:
        if cur != backup:
            print(lang, "STOP: live differs from the backup (edited since). Skipped."); fails += 1; continue
        target = cur
        for a, b in reps:
            if a not in target: print(lang, "STOP: phrase not found:", a); fails += 1; target = None; break
            target = target.replace(a, b)
        if target is None: continue
    lb = get(slug)
    s2, r2, _ = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": target})
    s3, d3, _ = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit")
    time.sleep(2); la = get(slug)
    open(os.path.join(HERE, f"after-live-{lang}.html"), "w", encoding="utf-8").write(la)
    ok = s2 in (200, 201) and d3["content"]["raw"] == target and inv(la) == inv(lb)
    if not rollback: ok = ok and all(a not in la for a, _ in reps if a != "collagen tanning area")
    print(lang, "PASS" if ok else "FAIL", "| status", s2, "| fetch-back", d3["content"]["raw"] == target, "| invariants", inv(la) == inv(lb))
    fails += 0 if ok else 1
sys.exit(1 if fails else 0)
