# -*- coding: utf-8 -*-
"""Proof that Kikar Hamedina P9a (1.72.371, hamedina_ps_patch371.py) leaves every other page byte for byte as it was, and changes
the five Kikar pages ONLY by the four hunks:
  - Rainbow, DUO, Dimri Yama and Ashira (Hebrew and English): every rendered piece identical;
  - Kikar Hamedina he, en, fr, ru, ar: every piece identical once the hunks' new text is put back to the old (the Hebrew degrees
    as a word, the phone's landing lane in the world page's style, the Russian page's Cyrillic block) - so nothing else moved.

Two pairs, rendered by ps_render_harness.php (WordPress stubbed, the plugin's real assets):
  release: what 1.72.370 wrote (md5 ae0966a4...)       vs  that + the P9a hunks (what deploy371 writes)
  branch:  git HEAD's file (the P8 hunks and Batch 1/2)  vs  the working file (+ the P9a hunks)
Writes docs/research/2026-09-30-kikar-hamedina/p9a-identity.json.

  python scripts/project-stage/ps_identity_proof371.py
"""
import hashlib, io, json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import ps_identity_proof as I  # noqa: E402  render / pieces (it sets stdout to UTF-8)
import hamedina_ps_patch371 as P9  # noqa: E402

OUT = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "p9a-identity.json")
SAME = ["rainbow-tel-aviv", "rainbow-tel-aviv-en", "duo-tel-aviv", "duo-tel-aviv-en", "dimri-yama-sde-dov", "dimri-yama-sde-dov-en",
        "ashira-sde-dov", "ashira-sde-dov-en"]
KIKAR = ["hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar"]
BACK = [("1.25 מעלות בכל קומה", "1.25° בכל קומה"), ("כ-50 מעלות לאורך מגדל", "כ-50° לאורך מגדל"),
        (P9.LANE_NEW.split("\n")[-1].split("'")[1], "")]  # the lane's CSS rule, as the page prints it
CYR = re.compile(r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n<style id="nadlan-ps-world-cyr">.*?</style>\n', re.S)


def back(s):
    s = s or ""
    for new, old in BACK:
        s = s.replace(new, old)
    return CYR.sub("", s)


def compare(before, after, label):
    ok, rows = True, []
    for slug in SAME + KIKAR:
        b, a = I.pieces(I.render(before, slug)), I.pieces(I.render(after, slug))
        kikar = slug in KIKAR
        diff = [k for k in b if b[k] != a.get(k)]
        extra = {k: v for k, v in a.items() if k not in b}
        if kikar:
            same = all(b[k] == back(a.get(k)) for k in b) and all(not back(v).strip() for v in extra.values())
            # and the hunks really show: the lane on every Kikar page, the Cyrillic only on the Russian one, the degrees in Hebrew
            head = "".join(v or "" for k, v in a.items() if k.startswith("wp_head"))
            shows = BACK[2][0] in head and (("nadlan-ps-world-cyr" in head) == (slug == "hamedina-ru"))
            if slug == "hamedina":
                shows = shows and "1.25 מעלות בכל קומה" in (a.get("composed") or "") and "1.25°" not in (a.get("composed") or "")
            same = same and shows
        else:
            same = not diff and all(not (v or "").strip() for v in extra.values())
        ok = ok and same
        rows.append({"slug": slug, "ok": same, "pieces": len(b), "changed_pieces": diff, "kikar": kikar})
        print(f"[{label}] {'OK  ' if same else 'FAIL'} {slug:24s} pieces {len(b):2d}" + (f"  changed only by the P9a hunks: {diff}" if kikar and diff else "") + ("" if same else f"  differs: {diff}"))
    return ok, rows


def main():
    tmp = tempfile.mkdtemp(prefix="ps371-ident-")
    live = os.path.join(tmp, "live-370.php")
    io.open(live, "w", encoding="utf-8", newline="").write(P9.live370())
    rel = os.path.join(tmp, "release-371.php")
    io.open(rel, "w", encoding="utf-8", newline="").write(P9.release_text())
    head = os.path.join(tmp, "branch-head.php")
    open(head, "wb").write(subprocess.run(["git", "-C", REPO, "show", "HEAD:" + P9.REL], capture_output=True).stdout)
    if P9.carries(open(head, encoding="utf-8").read())["lane"]:  # after the P9a commit, the branch's "before" is the commit before it
        log = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "-n", "40", "--", P9.REL], capture_output=True, text=True).stdout.split()
        for c in log:
            src = subprocess.run(["git", "-C", REPO, "show", f"{c}:{P9.REL}"], capture_output=True).stdout
            if not P9.carries(src.decode("utf-8"))["lane"]:
                open(head, "wb").write(src)
                print("[branch] before = the file at", c[:8], "(the last commit without the P9a hunks)")
                break
    work = os.path.join(REPO, *P9.REL.split("/"))
    ok1, r1 = compare(live, rel, "release")
    ok2, r2 = compare(head, work, "branch ")
    res = {"release": {"before": "370 live (md5 " + hashlib.md5(open(live, "rb").read()).hexdigest() + ")",
                       "after": "371 release (md5 " + hashlib.md5(open(rel, "rb").read()).hexdigest() + ")", "ok": ok1, "rows": r1},
           "branch": {"before": "the branch file without the P9a hunks", "after": "working file", "ok": ok2, "rows": r2}}
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    good = ok1 and ok2
    print("RESULT", "OK: the eight stage pages byte for byte the same; the five Kikar pages changed only by the P9a hunks" if good else "DIFFERENT")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
