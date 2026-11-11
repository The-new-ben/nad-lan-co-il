# -*- coding: utf-8 -*-
"""HAD-712, the English Kikar page (post 8114) after its own search research (docs/research/2026-11-11-kikar-search/lang-en.md,
11.11.2026). The page already answers most English searches (for sale, who sells, map, address, shops, foreign buyers). Two words
English searchers use were missing from its headings:
  - "stores": autocomplete gives "kikar hamedina stores" beside "kikar hamedina tel aviv shops" (US, UK, Israel).
  - "project" / "development": "kikar hamedina project", "kikar hamedina tel aviv development / transformation"; the story chapter was
    titled "From the plots of 1942 to the frame of 2026", which is also out of date (the towers' construction was reported completed
    in October 2026, already in the page's own timeline).
Two heading rewordings, no new fact, no FAQ change (so no schema release). Title and H1 untouched. Anchored on the LIVE text, pinned md5,
backup before, read-back after; dry by default.   python scripts/kikar/had712_en_intent.py [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
PID, SLUG, PIN = 8114, "hamedina-en", "43c161a617e54633e0c3b78ac33edebe"  # written by had712_lang.py en, 11.11.2026 18:50 local
SWAPS = [
    ("<h2>From the plots of 1942 to the frame of 2026</h2>", "<h2>The Kikar Hamedina project: from the plots of 1942 to the completed towers of 2026</h2>"),
    ("<h3>Luxury shopping on the ring</h3>", "<h3>Luxury stores and shops on the ring</h3>"),
]

if __name__ == "__main__":
    GO = "--go" in sys.argv
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712e"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
    assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
    raw = g["content"]["raw"]
    now = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if now != PIN:
        raise SystemExit("the live post changed since it was read (%s, modified %s)" % (now[:10], g["modified"]))
    new = raw
    for a, b in SWAPS:
        if new.count(a) != 1:
            raise SystemExit("anchor x%d: %s" % (new.count(a), a))
        new = new.replace(a, b)
    assert new.count("<h2>") == raw.count("<h2>") and new.count("<h3>") == raw.count("<h3>")
    print("[plan] en post %d: %d heading rewordings; %d -> %d chars" % (PID, len(SWAPS), len(raw), len(new)))
    if not GO:
        sys.exit(0)
    bk = os.path.join(REPO, "docs", "qa", "had-712")
    stamp = time.strftime("%Y%m%dT%H%M%S")
    io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
    s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
    assert s1 in (200, 201), (s1, str(r1)[:300])
    s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
    ok = r["content"]["raw"] == new
    res = {"lang": "en", "post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(),
           "read_back_equal": ok, "modified": r.get("modified"), "what": "intent headings"}
    json.dump({"stamp": stamp, "result": res}, open(os.path.join(bk, "result-en-intent-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
    if not ok:
        sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
        raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
    print("[done] en post %d written and read back (%s)" % (PID, stamp))
