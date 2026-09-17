#!/usr/bin/env bash
# One step: rebuild the blocks, repackage, and sync the package into the path the runner reads.
set -e
cd "$(dirname "$0")/package/source"
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python build/build.py >/dev/null
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python build/package.py >/dev/null
cd ..
python - <<'PY'
import os, shutil, filecmp
src = "source/dist/nadlan-meital-listings/listings"; dst = "listings"; n = 0
for L in sorted(os.listdir(src)):
    for f in sorted(os.listdir(os.path.join(src, L))):
        a = os.path.join(src, L, f); b = os.path.join(dst, L, f)
        if not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
            shutil.copy2(a, b); n += 1
print(n, "file(s) synced into package/listings")
PY
