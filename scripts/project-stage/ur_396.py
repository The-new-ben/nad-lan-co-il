# -*- coding: utf-8 -*-
"""Release 1.72.415 = urban's HAD-396 (urban-renewal honesty), Maya round-4 ACCEPT (urban-round4-verdict.md), package 0663be07,
code b3e61a9c, CMS c5530f12; main's code-owner PASS. Every byte is read from the COMMITTED package (git show 0663be07:...), never
from a working copy, and checked against package.json (md5 per file).
  - 16 plugin files: the live text must equal the package's live md5 (the true-live base of 1.72.413/414), then it becomes the
    patched bytes (md5 pinned); php files linted by the runner, the 2 js files checked here with node --check.
  - snippet 661 (x-catalog-plus): code 4af575c452 -> 763f1dfa2c, linted on the server with a "<?php" prefix.
  - page 73 content.raw c44db0978e -> 24acab8a71; metas: 73 _yoast_wpseo_metadesc, 5471 _yoast_wpseo_title + _yoast_wpseo_metadesc.
The data patch (posts 5477-5479) is NOT part of it: report first."""
import hashlib, json, os, subprocess, tempfile

PKG = "0663be0741306f31f76bdea2f71fbf1033ee83e6"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
md5 = lambda b: hashlib.md5(b).hexdigest()


def _show(path):
    r = subprocess.run(["git", "-C", REPO, "show", f"{PKG}:{path}"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"ur_396: cannot read {path} at {PKG[:8]}: {r.stderr[:200]!r}")
    return r.stdout


P = json.loads(_show("docs/qa/had-396/final-package/package.json").decode("utf-8"))
FILES = {}   # rel -> (live_md5, patched_bytes)
SNIPPET = None
for e in P["files"]:
    b = _show("docs/qa/had-396/patched/" + e["path"])
    if md5(b) != e["patched_md5"]:
        raise SystemExit(f"ur_396: {e['path']} at {PKG[:8]} is {md5(b)[:10]}, the package says {e['patched_md5'][:10]}")
    if e["path"].startswith("snippets/"):
        SNIPPET = {"id": 661, "live_md5": e["live_md5"], "code": b.decode("utf-8"), "md5": e["patched_md5"]}
    else:
        FILES[e["path"]] = (e["live_md5"], b)
RELS = sorted(FILES)
if len(RELS) != 16 or SNIPPET is None:
    raise SystemExit(f"ur_396: expected 16 files + snippet 661, got {len(RELS)} + {SNIPPET is not None}")
for rel in RELS:
    if rel.endswith(".js"):
        with tempfile.NamedTemporaryFile("wb", suffix=".js", delete=False) as t:
            t.write(FILES[rel][1]); tmp = t.name
        try:
            r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        finally:
            os.unlink(tmp)
        if r.returncode != 0:
            raise SystemExit(f"ur_396: node --check {rel}: {r.stderr[:200]}")
C = P["cms"]["page_73"]
PAGE = {"id": 73, "before_md5": C["before_md5"], "after": _show(C["after_file"]), "after_md5": C["after_md5"], "before": _show(C["before_file"])}
if md5(PAGE["after"]) != PAGE["after_md5"] or md5(PAGE["before"]) != PAGE["before_md5"]:
    raise SystemExit("ur_396: page 73 before/after bytes do not match their md5")
METAS = []
for m in P["cms"]["metas"]:
    if not m["key"].startswith("_yoast_wpseo_"):
        raise SystemExit("ur_396: only Yoast metas are written")
    a, b = m["after"].encode("utf-8"), m["before"].encode("utf-8")
    if md5(a) != m["after_md5"] or md5(b) != m["before_md5"]:
        raise SystemExit(f"ur_396: meta {m['post']} {m['key']} text does not match its md5")
    METAS.append({"id": int(m["post"]), "key": m["key"], "before": b, "before_md5": m["before_md5"], "after": a, "after_md5": m["after_md5"]})


def apply(rel, txt):
    """The live text (LF) must be the package's live base; it becomes the pinned patched text."""
    live_md5, new_b = FILES[rel]
    if md5(txt.encode("utf-8")) != live_md5:
        raise SystemExit(f"ur_396: live {rel} is {md5(txt.encode('utf-8'))[:10]}, the package's base is {live_md5[:10]}")
    return new_b.decode("utf-8")
