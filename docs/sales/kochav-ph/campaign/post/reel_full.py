# -*- coding: utf-8 -*-
"""The full-screen Reel (29.10.2026, Ben: "much higher level"): Meital's own vertical walk through the home (her reel of the listing,
720x1280) fills the 9:16 frame, as the agents behind the award-winning listing Reels show homes, instead of a square window.
Her burned-in title and logo are covered by the top band and the bottom fade (the band carries the words in each language, inside
Meta's Reels safe zone). The opening and the park are her photos, the end card is the broker's. Reuses build.py's pages and helpers.
  python reel_full.py [he en fr ru]   -> out/<lang>/reel-9x16-full.mp4"""
import io, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(H, "build.py"), encoding="utf-8").read()
ns = {"__name__": "b", "__file__": os.path.join(H, "build.py")}
exec(compile(src[:src.index("with sync_playwright() as p:")], "build.py", "exec"), ns)
page, shoot, ff, ENC, music, URI = ns["page"], ns["shoot"], ns["ff"], ns["ENC"], ns["music"], ns["URI"]
IMG, TMP, MEI, P, INK, MIST, FF = ns["IMG"], ns["TMP"], ns["MEI"], ns["P"], ns["INK"], ns["MIST"], ns["FF"]
from playwright.sync_api import sync_playwright
LANGS = [a for a in sys.argv[1:] if not a.startswith("--")] or ["he", "en", "fr", "ru"]
DX6 = os.path.join(MEI, "ig_DX6qd1ro1NG_01_fresh-2026-10-22.mp4")  # Meital's vertical reel: corridor, kitchen, living, dining, terrace
# (kind, source, from, to, crop centre x for photos, the caption = index into IMG[lang]["segs"])
CUT = [("photo", P("L07_DV6aYANjLBm_02.jpg"), 0, 2.8, 0.66, 0), ("clip", DX6, 0.0, 5.0, None, 2), ("clip", DX6, 5.0, 10.0, None, 1),
       ("clip", DX6, 15.0, 20.0, None, 3), ("photo", P("L07_DX9wx4ziADM_08.jpg"), 0, 3.2, 0.5, 4)]
END_S, XF = 4.4, 0.4


def band(c, k, cap):
    t, s = c["segs"][cap]
    bars = "".join('<i style="flex:1;height:5px;border-radius:3px;background:%s"></i>' % ("#8FC1D4" if j <= k else "rgba(255,255,255,.22)") for j in range(5))
    return page(c, 1080, 1920, (
        # the top band hides Meital's burned-in title (5% to 23% of the frame) and carries the words; the bottom fade softens her logo
        '<div style="position:absolute;left:0;right:0;top:0;height:720px;background:linear-gradient(180deg,rgba(20,33,43,1) 0,rgba(20,33,43,1) 600px,rgba(20,33,43,0) 740px)"></div>'
        '<div style="position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(0deg,rgba(20,33,43,.92),rgba(20,33,43,0))"></div>'
        '<div style="position:absolute;inset-inline:66px;top:286px;display:grid;gap:10px">'
        '<div class="k">%s</div><div class="serif fit" data-min="50" style="font-size:76px;line-height:1.08;text-wrap:balance">%s</div>'
        '<div style="font:500 33px/1.32 var(--sans);color:%s;text-wrap:balance">%s</div></div>' % (c["kicker"], t, MIST, s) +
        '<div style="position:absolute;inset-inline:66px;top:552px;font:600 25px/1.3 var(--sans);color:#8FC1D4">%s · %s</div>' % (c["end"][1], c["lic_short"]) +
        '<div style="position:absolute;inset-inline:66px;top:604px;display:flex;gap:8px">%s</div>' % bars +
        '<span class="chip" style="top:690px;left:90px"><i></i>%s</span>' % c["real"]), True)


def clip(k, kind, src, a, b, cx):
    out = os.path.join(TMP, "full%d.mp4" % k)
    if os.path.exists(out): return out
    if kind == "photo":
        n = int(round(b * 30)); e = "(on/%d)" % (n - 1); ease = "(%s*%s*(3-2*%s))" % (e, e, e)
        crop = "crop='ih*9/16':ih:'max(0,min(iw-ih*9/16,iw*%f-ih*9/32))':0" % cx
        ff("-loop", "1", "-i", src, "-vf", "format=rgb24,%s,scale=2160:3840:flags=lanczos,zoompan=z='1+0.06*%s':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*0.5':d=%d:s=1080x1920:fps=30,"
           "eq=contrast=1.04:saturation=1.05" % (crop, ease, n), "-frames:v", n, *ENC, out)
    else:
        n = int(round((b - a) * 30))
        ff("-ss", "%.3f" % a, "-t", "%.3f" % (b - a + 0.2), "-i", src, "-an", "-vf",
           "scale=1080:1920:flags=lanczos,unsharp=5:5:0.7,eq=contrast=1.06:saturation=1.1:gamma=0.98", "-frames:v", n, *ENC, out)
    return out


with sync_playwright() as p:
    br = p.chromium.launch(channel="msedge"); pg = br.new_page()
    for lang in LANGS:
        for k, s in enumerate(CUT):
            shoot(pg, band(IMG[lang], k, s[5]), os.path.join(TMP, "bf_%s_%d.png" % (lang, k)), 1080, 1920, True)
    br.close()
clips = [clip(k, s[0], s[1], s[2], s[3], s[4]) for k, s in enumerate(CUT)]
durs = [s[3] if s[0] == "photo" else s[3] - s[2] for s in CUT] + [END_S]
for lang in LANGS:
    parts = []
    for k, cl in enumerate(clips):
        out = os.path.join(TMP, "ff_%s_%d.mp4" % (lang, k)); n = int(round(durs[k] * 30))
        ff("-i", cl, "-i", os.path.join(TMP, "bf_%s_%d.png" % (lang, k)), "-filter_complex", "[0:v][1:v]overlay=0:0,format=yuv420p", "-frames:v", n, *ENC, out)
        parts.append(out)
    end = os.path.join(TMP, "f_%s_9x16_end.mp4" % lang)  # the broker's end card from build.py
    assert os.path.exists(end), "run build.py first"
    parts.append(end)
    silent = os.path.join(TMP, "vf_%s.mp4" % lang); T = ns["join"](parts, silent, durs)
    wav = music(T, None); final = os.path.join(H, "out", lang, "reel-9x16-full.mp4")
    ff("-i", silent, "-i", wav, "-filter_complex", "[1:a]atrim=0:%.2f,afade=t=in:d=0.6,afade=t=out:st=%.2f:d=1.4,loudnorm=I=-16:TP=-1.5:LRA=11[a]" % (T, T - 1.4),
       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", final)
    print(lang, "full-screen reel %.1f s" % T, os.path.getsize(final) // 1024, "KB", flush=True)
