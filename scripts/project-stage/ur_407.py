# -*- coding: utf-8 -*-
"""Release 1.72.416 = urban's HAD-407 + HAD-408 + HAD-409 (the project room's header, headings, buttons and wording), Maya's scoped
PASS (docs/coordination/codex-had407-409-qa-2026-10-03.md) for commit 82f41176 ONLY; main's code-owner pre-check PASS.
Every byte is read from the commit (git show 82f41176:docs/qa/had-407/patched/...), and its MD5 must equal the one Maya accepted.
The live text must equal the package's base (what 1.72.415 wrote) before it becomes the patched bytes."""
import hashlib, json, os, subprocess

PKG = "82f41176cf3a4aa57f2d97ffa1d510191fce8c50"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
md5 = lambda b: hashlib.md5(b).hexdigest()
ACCEPTED = {"inc/urban-space.php": "4fd19149ebdbab4223bb363fa7d26bc2", "inc/i18n.php": "b98253493343a2f966be6028a6512d89"}


def _show(path):
    r = subprocess.run(["git", "-C", REPO, "show", f"{PKG}:{path}"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"ur_407: cannot read {path} at {PKG[:8]}: {r.stderr[:200]!r}")
    return r.stdout


T = json.loads(_show("docs/qa/had-407/md5.json").decode("utf-8"))
FILES = {}
for e in T:
    b = _show("docs/qa/had-407/patched/" + e["file"])
    if md5(b) != e["patched_md5"] or ACCEPTED.get(e["file"]) != md5(b):
        raise SystemExit(f"ur_407: {e['file']} at {PKG[:8]} is {md5(b)[:10]}, not the accepted {ACCEPTED.get(e['file'], '?')[:10]}")
    FILES[e["file"]] = (e["live_md5"], b)
RELS = sorted(FILES)
if RELS != sorted(ACCEPTED):
    raise SystemExit("ur_407: the package files are not exactly the two accepted ones")


def apply(rel, txt):
    live_md5, new_b = FILES[rel]
    if md5(txt.encode("utf-8")) != live_md5:
        raise SystemExit(f"ur_407: live {rel} is {md5(txt.encode('utf-8'))[:10]}, the package's base is {live_md5[:10]}")
    return new_b.decode("utf-8")
