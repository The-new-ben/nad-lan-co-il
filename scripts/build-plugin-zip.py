#!/usr/bin/env python3
"""Canonical, cross-platform builder for the nadlan-config plugin ZIP.

WHY THIS EXISTS: a Windows-built ZIP once stored entry paths with backslashes
(`nadlan-config\\inc\\file.php`). On Linux/uPress those do NOT unpack as folders
— they become literal junk files inside the plugin directory, creating a
"phantom" plugin and jamming the uPress plugin manager. This builder ALWAYS
writes forward-slash, `nadlan-config/`-rooted paths, and refuses to emit a ZIP
that contains a single backslash entry.

Usage:  python3 scripts/build-plugin-zip.py            # uses Version: header
        python3 scripts/build-plugin-zip.py 1.66.3     # explicit version
"""
import os, re, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "plugins", "nadlan-config")
DIST = os.path.join(ROOT, "plugin-dist")


def detect_version():
    head = open(os.path.join(SRC, "nadlan-config.php"), encoding="utf-8").read(4000)
    m = re.search(r"^\s*\*\s*Version:\s*([0-9][0-9.]*)", head, re.M)
    if not m:
        sys.exit("could not detect Version: header")
    return m.group(1)


def build(version):
    out = os.path.join(DIST, f"nadlan-config-{version}.zip")
    if os.path.exists(out):
        os.remove(out)
    files = []
    for dp, _, fns in os.walk(SRC):
        for fn in fns:
            files.append(os.path.join(dp, fn))
    files.sort()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            # ALWAYS forward slashes, ALWAYS rooted at nadlan-config/
            rel = os.path.relpath(f, SRC).replace(os.sep, "/").replace("\\", "/")
            z.write(f, "nadlan-config/" + rel)
    # Guard: reject poison before it can ever ship
    z = zipfile.ZipFile(out)
    names = z.namelist()
    bad = [n for n in names if "\\" in n]
    rooted = all(n.startswith("nadlan-config/") for n in names)
    crc = z.testzip()
    if bad or not rooted or crc is not None:
        os.remove(out)
        sys.exit(f"REJECTED unsafe ZIP: backslash={len(bad)} rooted={rooted} crc={crc}")
    print(f"OK {os.path.basename(out)} entries={len(names)} backslash=0 rooted=True crc=ok")
    return out


if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else detect_version()
    build(v)
