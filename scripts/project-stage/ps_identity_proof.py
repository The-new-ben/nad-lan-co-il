# -*- coding: utf-8 -*-
"""Proof that KikarHamedinaWorld (P7a) leaves the four stage projects byte for byte as they were.

For Rainbow, DUO, Dimri Yama and Ashira, in Hebrew and on the English sibling, it renders with ps_render_harness.php (WordPress
stubbed, the plugin's real assets) everything inc/project-stage.php prints: the stage config, nadlan_ps_current(), the
composed page top, and every wp_head / wp_footer piece. Two pairs are compared:
  branch:  the branch file before P7a (before) vs the working file (after, the hunks applied)
  release: 65af09be's file (the live base)     vs 65af09be + the hunks (the file deploy369 would write)
Every piece must match exactly; a hook the new file adds must print nothing on these pages. Kikar Hamedina itself is rendered
too (after only), to show it composes. Writes docs/research/2026-09-30-kikar-hamedina/p7-identity.json.

  python scripts/project-stage/ps_identity_proof.py
"""
import hashlib, io, json, os, subprocess, sys, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import hamedina_ps_patch as P  # noqa: E402

REL = P.REL
HARNESS = os.path.join(HERE, "ps_render_harness.php")
OUT = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina", "p7-identity.json")
SLUGS = ["rainbow-tel-aviv", "duo-tel-aviv", "dimri-yama-sde-dov", "ashira-sde-dov"]


def git_show(rev):
    r = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{REL}"], capture_output=True)
    if r.returncode:
        raise SystemExit("git show " + rev)
    return r.stdout


def render(path, slug):
    r = subprocess.run(["php", HARNESS, path, slug], capture_output=True, env={**os.environ, "NL_SITE_WA": "972525101555", "NL_VER": "1.72.368"})
    if r.returncode:
        raise SystemExit(f"harness failed on {slug}: {r.stderr.decode('utf-8', 'replace')[:400]}")
    return json.loads(r.stdout.decode("utf-8"))


def pieces(d):
    out = {"config": d.get("config"), "current": d.get("current"), "composed": d.get("composed")}
    for h in ("wp_head", "wp_footer"):
        for k, v in (d.get(h) or {}).items():
            out[h + "@" + k] = v
    return out


def md5(s):
    return hashlib.md5((s or "").encode("utf-8")).hexdigest()


def compare(before_path, after_path, label):
    rows, ok = [], True
    for base in SLUGS:
        for slug in (base, base + "-en"):
            b, a = pieces(render(before_path, slug)), pieces(render(after_path, slug))
            # a hook the new file adds (the world page's style) prints nothing here; hooks keep their order by priority
            extra = {k: v for k, v in a.items() if k not in b}
            same = all(b[k] == a.get(k) for k in b)
            empty_extra = all(not (v or "").strip() for v in extra.values())
            ok = ok and same and empty_extra
            rows.append({"slug": slug, "identical": same, "new_hooks_silent": empty_extra, "pieces": len(b),
                         "composed_bytes": len((b.get("composed") or "").encode("utf-8")),
                         "md5": {k: md5(v) for k, v in b.items()},
                         "diff": [k for k in b if b[k] != a.get(k)], "extra": sorted(extra)})
            print(f"[{label}] {'SAME' if same and empty_extra else 'DIFF'} {slug:26s} pieces {len(b):2d}  composed {rows[-1]['composed_bytes']:6d} B"
                  + ("" if same else f"  differs: {rows[-1]['diff']}") + (f"  new hooks: {sorted(extra)} (silent)" if extra else ""))
    return ok, rows


def main():
    tmp = tempfile.mkdtemp(prefix="ps-ident-")
    # "before" on the branch: the newest commit of the file that carries none of the hunks (HEAD before P7a was committed)
    revs = subprocess.run(["git", "-C", REPO, "rev-list", "HEAD", "--", REL], capture_output=True, text=True).stdout.split()
    before_rev = next(r for r in revs if not any(P.carries(git_show(r).decode("utf-8")).values()))
    print("branch before =", before_rev[:10])
    head = os.path.join(tmp, "branch-before.php"); open(head, "wb").write(git_show(before_rev))
    live = os.path.join(tmp, "live-base.php"); open(live, "wb").write(git_show(P.BASE_COMMIT))
    rel_copy = os.path.join(tmp, "release-after.php")
    open(rel_copy, "wb").write(P.apply(git_show(P.BASE_COMMIT).decode("utf-8"), P.BASE_COMMIT).encode("utf-8"))
    work = os.path.join(REPO, *REL.split("/"))
    ok1, r1 = compare(head, work, "branch ")
    ok2, r2 = compare(live, rel_copy, "release")
    kh = render(work, "hamedina")
    khe = render(work, "hamedina-en")
    res = {"branch": {"before": before_rev, "after": "working file", "ok": ok1, "rows": r1},
           "release": {"before": P.BASE_COMMIT + " (live, md5 " + hashlib.md5(open(live, 'rb').read()).hexdigest() + ")",
                       "after": "65af09be + hunks (md5 " + hashlib.md5(open(rel_copy, 'rb').read()).hexdigest() + ")", "ok": ok2, "rows": r2},
           "hamedina": {"he_composed_bytes": len((kh.get("composed") or "").encode("utf-8")), "en_composed_bytes": len((khe.get("composed") or "").encode("utf-8")),
                        "he_has_world": 'nlps-stage--world' in (kh.get("composed") or ""), "en_has_world": 'nlps-stage--world' in (khe.get("composed") or "")}}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    print("hamedina:", res["hamedina"])
    print("RESULT", "OK: the four projects are byte for byte the same (branch and release)" if ok1 and ok2 else "DIFFERENT")
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    sys.exit(main())
