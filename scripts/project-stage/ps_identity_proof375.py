# -*- coding: utf-8 -*-
"""Proof that Kikar Hamedina P9c (1.72.375, hamedina_ps_patch375.py) leaves every other page byte for byte as it was, and changes
the five Kikar pages ONLY by its hunks:
  - Rainbow, DUO, Dimri Yama and Ashira (Hebrew and English): every rendered piece identical;
  - Kikar Hamedina he, en, fr, ru, ar: every piece identical once the hunks' new text is put back to the old (the example
    apartment in the config and in the world's page config, the mount's option and the analytics line, the accessibility
    corner's script, the Arabic phone lane in the world page's style) - so nothing else moved; and the hunks really show.

Two pairs, rendered by ps_render_harness.php (WordPress stubbed, the plugin's real assets, so tour/examples.json is found):
  release: what 1.72.371 wrote (md5 ab944286..., still live at 1.72.372)  vs  that + the P9c hunks (what deploy375 writes)
  branch:  the branch file without the P9c hunks                          vs  the working file
Writes docs/research/2026-09-30-kikar-hamedina/p9c-identity.json.

  python scripts/project-stage/ps_identity_proof375.py
"""
import hashlib, io, json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import ps_identity_proof as I  # noqa: E402  render / pieces (it sets stdout to UTF-8)
import hamedina_ps_patch375 as PC  # noqa: E402

OUT = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "p9c-identity.json")
SAME = ["rainbow-tel-aviv", "rainbow-tel-aviv-en", "duo-tel-aviv", "duo-tel-aviv-en", "dimri-yama-sde-dov", "dimri-yama-sde-dov-en",
        "ashira-sde-dov", "ashira-sde-dov-en"]
KIKAR = ["hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar"]
BACK = [(PC.MOUNT_NEW, PC.MOUNT_OLD), (PC.A11Y_NEW, PC.A11Y_OLD), (PC.AR_LANE, "")]
EX_JSON = re.compile(r',"examples":\[\{"id":"c30w".*?\}\]')                                  # the config, as JSON
EX_CFG = re.compile(r',&quot;examples&quot;:\{&quot;url&quot;:&quot;[^&]*&quot;,&quot;list&quot;:\[.*?\]\}')  # the page config, escaped


def back(s):
    s = s or ""
    for new, old in BACK:
        s = s.replace(new, old)
    s = EX_JSON.sub("", s)
    return EX_CFG.sub("", s)


def compare(before, after, label):
    ok, rows = True, []
    for slug in SAME + KIKAR:
        b, a = I.pieces(I.render(before, slug)), I.pieces(I.render(after, slug))
        kikar = slug in KIKAR
        diff = [k for k in b if b[k] != a.get(k)]
        extra = {k: v for k, v in a.items() if k not in b}
        if kikar:
            same = all(b[k] == back(a.get(k)) for k in b) and all(not back(v).strip() for v in extra.values())
            head = "".join(v or "" for k, v in a.items() if k.startswith("wp_head"))
            foot = "".join(v or "" for k, v in a.items() if k.startswith("wp_footer"))
            comp = a.get("composed") or ""
            shows = {"lane_ar": PC.AR_LANE in head, "examples_cfg": bool(EX_CFG.search(comp)) and r"tour\/examples.json" in comp,
                     "mount": "examples: c.examples || null" in foot, "a11y": "AccessibleCorner" in foot}
            same = same and all(shows.values())
        else:
            shows = {}
            same = not diff and all(not (v or "").strip() for v in extra.values())
        ok = ok and same
        rows.append({"slug": slug, "ok": same, "pieces": len(b), "changed_pieces": diff, "kikar": kikar, "shows": shows})
        print(f"[{label}] {'OK  ' if same else 'FAIL'} {slug:24s} pieces {len(b):2d}" + (f"  changed only by the P9c hunks: {diff} {shows}" if kikar and diff else "") + ("" if same else f"  differs: {diff}"))
    return ok, rows


def main():
    tmp = tempfile.mkdtemp(prefix="ps375-ident-")
    live = os.path.join(tmp, "live-371.php")
    io.open(live, "w", encoding="utf-8", newline="").write(PC.live371())
    rel = os.path.join(tmp, "release-375.php")
    io.open(rel, "w", encoding="utf-8", newline="").write(PC.release_text())
    work = os.path.join(REPO, *PC.REL.split("/"))
    cur = io.open(work, encoding="utf-8", newline="").read()
    before = cur
    for name, old, new in PC.HUNKS:  # the branch's "before": the working file with the P9c hunks taken out again
        before = before.replace(new, old)
    if any(PC.carries(before).values()):
        raise SystemExit("FATAL: could not take the P9c hunks out of the working file")
    head = os.path.join(tmp, "branch-before.php")
    io.open(head, "w", encoding="utf-8", newline="").write(before)
    ok1, r1 = compare(live, rel, "release")
    ok2, r2 = compare(head, work, "branch ")
    res = {"release": {"before": "371 live (md5 " + hashlib.md5(open(live, "rb").read()).hexdigest() + ")",
                       "after": "375 release (md5 " + hashlib.md5(open(rel, "rb").read()).hexdigest() + ")", "ok": ok1, "rows": r1},
           "branch": {"before": "the working file without the P9c hunks", "after": "working file", "ok": ok2, "rows": r2}}
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    good = ok1 and ok2
    print("RESULT", "OK: the eight stage pages byte for byte the same; the five Kikar pages changed only by the P9c hunks" if good else "DIFFERENT")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
