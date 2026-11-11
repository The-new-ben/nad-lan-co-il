# -*- coding: utf-8 -*-
"""HAD-712, the Russian Kikar article (post 8117), after scripts/kikar/had712_lang.py ru (11.11.2026 19:12 UTC): the public-source audit
(tools/source_audit.py) flags visible dashes, and the Russian additions brought 9 of them (8 visible on the page before, 18 after).
Every dash the additions brought is reworded without one; nothing else changes. Four of them sit in FAQ answers, so the FAQ schema meta
follows in release 1.72.653 (kl_release.build(..., meta_only=True)). Anchored replacements on the LIVE text, pinned md5, backup before,
read-back after (restored if it differs); dry by default.   python scripts/kikar/had712_ru_dashes.py [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
PID, SLUG, PIN = 8117, "hamedina-ru", "4857804d6574e8c2aae31277de1d0e58"  # written by had712_lang.py ru, 11.11.2026 19:12 UTC
N = "\xa0"
SWAPS = [  # (old, new, how many times)
    ("а башня B — примерно 157 м.", "а башня B достигает примерно 157 м.", 2),  # the facts row and the height answer
    ("до примерно 160 м; башня B, в 37 этажей, — примерно 157 м", "до примерно 160 м; башня B, в 37 этажей, достигает примерно 157 м", 1),
    ("около 78 дунамов — площадь всего плана, а один только общественный парк — около 40 дунамов;",
     "около 78 дунамов составляет площадь всего плана, а один только общественный парк занимает около 40 дунамов;", 1),
    ("составит около 4" + N + "000–5" + N + "000" + N + "₪", "составит примерно от 4" + N + "000 до 5" + N + "000" + N + "₪", 2),  # the fee paragraph and the fee answer
    ("адреса в разрешениях на строительство — He Be’Iyar", "адреса в разрешениях на строительство: He Be’Iyar", 1),
    ("а улица Жаботинского — с востока.", "а улица Жаботинского с востока.", 1),
]


def apply(raw):
    for old, new, n in SWAPS:
        if raw.count(old) != n:
            raise SystemExit("anchor x%d (want %d): %s" % (raw.count(old), n, old[:80]))
        raw = raw.replace(old, new)
    return raw


if __name__ == "__main__":
    GO = "--go" in sys.argv
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712d"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
    assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
    raw = g["content"]["raw"]
    now = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if now != PIN:
        raise SystemExit("the live post changed since it was read (%s, modified %s)" % (now[:10], g["modified"]))
    new = apply(raw)
    d = lambda t: t.count("—") + t.count("–")
    print("[plan] ru post %d: dashes %d -> %d; %d -> %d chars" % (PID, d(raw), d(new), len(raw), len(new)))
    if not GO:
        sys.exit(0)
    bk = os.path.join(REPO, "docs", "qa", "had-712")
    stamp = time.strftime("%Y%m%dT%H%M%S")
    io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
    s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
    assert s1 in (200, 201), (s1, str(r1)[:300])
    s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
    ok = r["content"]["raw"] == new
    res = {"lang": "ru", "post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(),
           "read_back_equal": ok, "modified": r.get("modified"), "replacements": len(SWAPS), "what": "dashes"}
    json.dump({"stamp": stamp, "result": res}, open(os.path.join(bk, "result-ru-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
    if not ok:
        sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
        raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
    print("[done] ru post %d written and read back (%s)" % (PID, stamp))
