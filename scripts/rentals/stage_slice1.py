# -*- coding: utf-8 -*-
"""Stages the FINAL whole files of rentals slice 1 for the release script (local only, nothing is deployed):
docs/rentals/build/slice1/release/plugins/nadlan-config/... + MANIFEST.json. Each changed file = the CURRENT main-checkout file
plus only our change (hunks of HUNKS.md; the t2_* keys appended at the end of "ui" in he.json / en.json with the base's own
formatting and CRLF)."""
import re, json, hashlib, pathlib, subprocess, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
PL = "plugins/nadlan-config/"
OUT = ROOT / "docs/rentals/build/slice1/release" / PL
S1 = ROOT / "docs/rentals/build/slice1"
if OUT.parent.parent.exists():
    shutil.rmtree(OUT.parent.parent)
CRLF = chr(13) + chr(10); LF = chr(10)
md5 = lambda b: hashlib.md5(b).hexdigest()
rd = lambda p: open(p, "rb").read()
def put(rel, data):
    p = OUT / rel[len(PL):]; p.parent.mkdir(parents=True, exist_ok=True); open(p, "wb").write(data)
md = open(S1 / "HUNKS.md", encoding="utf8").read()
hunks = re.findall(r"^## \d+\. `([^`]+)`.*?old \(1 occurrence\):\n```\n(.*?)\n```\nnew:\n```\n(.*?)\n```", md, re.S | re.M)
man, by = [], {}
for path, old, new in hunks:
    by.setdefault(path, []).append([old, new])
for path, pairs in by.items():
    base = rd(ROOT / path); txt = base.decode("utf8"); eol = "\r\n" if "\r\n" in txt else "\n"
    for old, new in pairs:
        assert txt.count(old) == 1, (path, old)
        txt = txt.replace(old, new.replace("\n", eol), 1)
    out = txt.encode("utf8"); put(path, out)
    man.append({"rel": path[len(PL):], "kind": "changed", "base_md5": md5(base), "staged_md5": md5(out), "how": "hunk", "eol": "CRLF" if eol == "\r\n" else "LF", "pairs": pairs})
for lg in ("he", "en"):
    path = PL + "assets/rentals/i18n/%s.json" % lg
    base = rd(ROOT / path); txt = base.decode("utf8"); eol = CRLF if CRLF in txt else LF
    add = json.load(open(S1 / ("strings-%s.json" % lg), encoding="utf8"))
    lines = txt.split(eol)
    i = next(n for n, l in enumerate(lines) if l == '"msg": {') - 1
    assert lines[i] == "}," or lines[i] == "},", lines[i]
    live = json.loads(txt)["ui"]; assert not [k for k in add if k in live], "key collision"
    lines[i - 1] += ","
    rows = ['%s: %s' % (json.dumps(k, ensure_ascii=False), json.dumps(v, ensure_ascii=False)) for k, v in add.items()]
    lines[i:i] = [r + "," for r in rows[:-1]] + [rows[-1]]
    out = eol.join(lines).encode("utf8"); j = json.loads(out.decode("utf8"))
    assert set(j["ui"]) == set(live) | set(add) and list(j["ui"])[:len(live)] == list(live) and j["msg"] == json.loads(txt)["msg"]
    put(path, out)
    man.append({"rel": path[len(PL):], "kind": "changed", "base_md5": md5(base), "staged_md5": md5(out), "how": "whole file", "eol": ("CRLF" if eol == chr(13) + chr(10) else "LF"), "added_keys": len(add)})
for rel in ("assets/rentals/rm-plan2d.js", "assets/rentals/rm-today.js", "assets/rentals/rm-today.css", "inc/rentals/today.php"):
    data = rd(ROOT / PL / rel); put(PL + rel, data)
    man.append({"rel": rel, "kind": "new", "base_md5": None, "staged_md5": md5(data), "how": "whole file"})
(S1 / "release/MANIFEST.json").write_text(json.dumps({"slice": "rentals-slice-1 (HAD-795)", "root": "plugins/nadlan-config/", "note": "base = the main-checkout file as it was when staged; page.php and rm-boot.js did not exist in the main checkout before this session (copied from worktree bold-cray-ad2cea), so the release script must compare base_md5 with the LIVE file first", "files": man}, ensure_ascii=False, indent=1), encoding="utf8")
# checks
PHP = next(iter(sorted(pathlib.Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/PHP.PHP.8.1_*/php.exe"))))
bad = 0
for f in OUT.rglob("*"):
    if f.suffix == ".php":
        r = subprocess.run([str(PHP), "-l", str(f)], capture_output=True, text=True); print(r.stdout.strip()); bad += r.returncode
    elif f.suffix == ".js":
        r = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True); print("node --check", f.name, "ok" if r.returncode == 0 else r.stderr); bad += r.returncode
    elif f.suffix == ".json":
        json.load(open(f, encoding="utf8")); print("json.load ok", f.name)
for m in man: print("%-8s %-9s %s base=%s staged=%s" % (m["kind"], m["how"], m["rel"], m["base_md5"], m["staged_md5"]))
sys.exit(1 if bad else 0)
