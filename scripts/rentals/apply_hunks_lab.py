# -*- coding: utf-8 -*-
"""Applies docs/rentals/build/slice1/HUNKS.md to LAB COPIES only (never the real files):
checks that every old line occurs exactly once, writes the patched files to
docs/design-lab/rentals/slice1-patched/, then php -l / node --check on them."""
import re, pathlib, subprocess, sys, shutil
ROOT = pathlib.Path(__file__).resolve().parents[2]
md = (ROOT / "docs/rentals/build/slice1/HUNKS.md").read_text(encoding="utf8")
OUT = ROOT / "docs/design-lab/rentals/slice1-patched"
OUT.mkdir(parents=True, exist_ok=True)
PHP = next(iter(sorted(pathlib.Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/PHP.PHP.8.1_*/php.exe"))), None)
hunks = re.findall(r"^## \d+\. `([^`]+)`.*?old \(1 occurrence\):\n```\n(.*?)\n```\nnew:\n```\n(.*?)\n```", md, re.S | re.M)
copies, bad = {}, 0
for path, old, new in hunks:
    src = ROOT / path
    txt = copies.get(path) or open(src, encoding="utf8", newline="").read()
    eol = "\r\n" if "\r\n" in txt else "\n"
    n = txt.count(old)
    print(("OK   " if n == 1 else "FAIL ") + "%s occurrences=%d  %s" % (path, n, old.strip()[:70]))
    if n != 1:
        bad += 1; continue
    copies[path] = txt.replace(old, new.replace("\r\n", "\n").replace("\n", eol), 1)
for path, txt in copies.items():
    dst = OUT / pathlib.Path(path).name
    open(dst, "w", encoding="utf8", newline="").write(txt)
    if dst.suffix == ".php" and PHP:
        r = subprocess.run([str(PHP), "-l", str(dst)], capture_output=True, text=True); print(r.stdout.strip() or r.stderr.strip())
    elif dst.suffix == ".js":
        r = subprocess.run(["node", "--check", str(dst)], capture_output=True, text=True); print("node --check", dst.name, "ok" if r.returncode == 0 else r.stderr)
print("hunks", len(hunks), "problems", bad)
sys.exit(1 if bad else 0)
