# -*- coding: utf-8 -*-
"""Proof that Kikar Hamedina P8 (1.72.370, hamedina_ps_patch370.py) leaves every page that exists today byte for byte as it was:
Rainbow, DUO, Dimri Yama and Ashira (Hebrew and English) and Kikar Hamedina itself in Hebrew and English. Only the new
language pages (hamedina-fr, -ru, -ar) change: before P8 they had the English words, now their own.

Two pairs, rendered by ps_render_harness.php (WordPress stubbed, the plugin's real assets) with every piece compared:
  release: what 1.72.369 wrote (65af09be + the 369 hunks, md5 e6c9fc1c...)  vs  that + the P8 hunks (what deploy370 writes)
  branch:  git HEAD's file (the 369 hunks and the unreleased Batch 1/2)       vs  the working file (+ the P8 hunks)
Writes docs/research/2026-09-30-kikar-hamedina/p8-identity.json.

  python scripts/project-stage/ps_identity_proof370.py
"""
import hashlib, io, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import ps_identity_proof as I  # noqa: E402  render / pieces / md5 (it sets stdout to UTF-8)
import hamedina_ps_patch370 as P8  # noqa: E402

OUT = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "p8-identity.json")
SAME = ["rainbow-tel-aviv", "rainbow-tel-aviv-en", "duo-tel-aviv", "duo-tel-aviv-en", "dimri-yama-sde-dov", "dimri-yama-sde-dov-en",
        "ashira-sde-dov", "ashira-sde-dov-en", "hamedina", "hamedina-en"]
NEW = ["hamedina-fr", "hamedina-ru", "hamedina-ar"]


def compare(before, after, label):
    ok, rows = True, []
    for slug in SAME:
        b, a = I.pieces(I.render(before, slug)), I.pieces(I.render(after, slug))
        if slug.startswith("hamedina"):
            # the Kikar Hamedina config itself gains i18n fr/ru/ar (that is the change): compared without them, and every
            # rendered piece (the page top, the head, the footer) must stay byte for byte the same
            for k in ("config", "current"):
                for d in (a, b):
                    j = json.loads(d[k]) if d.get(k) else None
                    if j and isinstance(j.get("i18n"), dict):
                        for l in ("fr", "ru", "ar"):
                            j["i18n"].pop(l, None)
                    d[k] = json.dumps(j, ensure_ascii=False, sort_keys=True) if j is not None else None
        extra = {k: v for k, v in a.items() if k not in b}
        same = all(b[k] == a.get(k) for k in b) and all(not (v or "").strip() for v in extra.values())
        ok = ok and same
        rows.append({"slug": slug, "identical": same, "pieces": len(b), "diff": [k for k in b if b[k] != a.get(k)]})
        print(f"[{label}] {'SAME' if same else 'DIFF'} {slug:24s} pieces {len(b):2d}" + ("" if same else f"  differs: {rows[-1]['diff']}"))
    return ok, rows


def main():
    tmp = tempfile.mkdtemp(prefix="ps370-ident-")
    live = os.path.join(tmp, "live-369.php")
    io.open(live, "w", encoding="utf-8", newline="").write(P8.live369())
    rel = os.path.join(tmp, "release-370.php")
    io.open(rel, "w", encoding="utf-8", newline="").write(P8.release_text())
    head = os.path.join(tmp, "branch-head.php")
    open(head, "wb").write(subprocess.run(["git", "-C", REPO, "show", "HEAD:" + P8.REL], capture_output=True).stdout)
    work = os.path.join(REPO, *P8.REL.split("/"))
    ok1, r1 = compare(live, rel, "release")
    ok2, r2 = compare(head, work, "branch ")
    new = {}
    for slug in NEW:
        d = I.render(rel, slug)
        c = d.get("composed") or ""
        new[slug] = {"composed_bytes": len(c.encode("utf-8")), "world": "nlps-stage--world" in c,
                     "lang": slug[-2:], "lang_in_cfg": ("&quot;lang&quot;:&quot;%s&quot;" % slug[-2:]) in c}
        print(f"[new    ] {slug}: {new[slug]}")
    res = {"release": {"before": "369 live (md5 " + hashlib.md5(open(live, "rb").read()).hexdigest() + ")",
                       "after": "370 release (md5 " + hashlib.md5(open(rel, "rb").read()).hexdigest() + ")", "ok": ok1, "rows": r1},
           "branch": {"before": "git HEAD", "after": "working file", "ok": ok2, "rows": r2}, "new_pages": new}
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    good = ok1 and ok2 and all(v["world"] and v["lang_in_cfg"] for v in new.values())
    print("RESULT", "OK: every existing page byte for byte the same; fr/ru/ar compose in their own language" if good else "DIFFERENT")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
