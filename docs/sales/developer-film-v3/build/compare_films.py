# -*- coding: utf-8 -*-
"""Are two builds of a film the same? File bytes, duration, frame count, and every decoded video frame and audio packet
(ffmpeg framemd5), so "identical" is proven frame by frame, not assumed.

  python compare_films.py <dirA> <dirB> [file ...]        default files: the main-he outputs
"""
import hashlib, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from variant import FF

A, B = sys.argv[1], sys.argv[2]
FILES = sys.argv[3:] or ["he-web-16x9.mp4", "en-vo_he-sub_16x9.mp4", "en-vo_he-sub_9x16.mp4", "poster-16x9.jpg"]


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def fmd5(p, stream):
    r = subprocess.run([FF, "-v", "error", "-i", p, "-map", "0:" + stream, "-f", "framemd5", "-"], capture_output=True, text=True).stdout
    return [l.rsplit(",", 1)[1].strip() for l in r.splitlines() if l and not l.startswith("#")]


def dur(p):
    r = subprocess.run([FF, "-hide_banner", "-i", p], capture_output=True, text=True).stderr
    return r.split("Duration: ")[1].split(",")[0] if "Duration: " in r else "-"


ok = True
for f in FILES:
    a, b = os.path.join(A, f), os.path.join(B, f)
    same = md5(a) == md5(b)
    line = f"{f}: bytes {'IDENTICAL' if same else 'differ'} ({os.path.getsize(a)} / {os.path.getsize(b)})"
    if f.endswith(".mp4"):
        va, vb = fmd5(a, "v"), fmd5(b, "v"); aa, ab = fmd5(a, "a"), fmd5(b, "a")
        vd = sum(x != y for x, y in zip(va, vb)) + abs(len(va) - len(vb)); ad = sum(x != y for x, y in zip(aa, ab)) + abs(len(aa) - len(ab))
        line += f"; duration {dur(a)} / {dur(b)}; video frames {len(va)} / {len(vb)}, differing {vd}; audio packets {len(aa)} / {len(ab)}, differing {ad}"
        ok = ok and vd == 0 and ad == 0
    else:
        ok = ok and same
    print(line)
print("RESULT:", "same film" if ok else "NOT the same")
