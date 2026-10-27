# -*- coding: utf-8 -*-
"""The Kochav HaTzafon film, v3 (27.10.2026): the re-cut after the broker's corrections of 22.10.
- no price per square metre anywhere (cards and narration);
- no tall buildings that do not exist: every shot made from our 3D city, and every photoreal still derived from it that shows
  the surroundings, is out; the only kept simulation is a tight crop of the planned bridge (boulevard, bridge, lawns, no
  buildings), labelled "simulation"; AI lifestyle stills stay only where no towers show (two park stills are cropped below the
  horizon);
- Meital's real footage and photographs carry the film (the home, the terraces, her drone photos and drone video);
- tennis courts and football pitches; a NEW home in a NEW building; areas only as "about 197 sqm" / "about 80 sqm of terraces";
- end card: Meital Katzir · Nadlan Al HaYam, 052-3631582, large.
Builds both cuts from one picture and one sound mix:
  python compose_v3.py [--fast] [--only en|he]  ->  kochav-film-en-v3.mp4, kochav-film-en-v3-he.mp4, kochav-film-v3.jpg
Nothing here uploads anything; outputs stay in this folder."""
import json, os, re, shutil, subprocess, sys, wave
import imageio_ffmpeg

H = os.path.dirname(os.path.abspath(__file__))          # film/v3
F = os.path.dirname(H)                                   # film
KP = os.path.dirname(F)                                  # kochav-ph
FF = imageio_ffmpeg.get_ffmpeg_exe()
REELS = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\kochav\reels"
MEI = os.path.join(KP, "_private-research", "meital-sources")
REAL = os.path.join(KP, "tour", "real")
DYRL = os.path.join(MEI, "ig_DYRLyC6NVyS_01_fresh-2026-10-22.mp4")   # Meital's reel of 13.5.2026 (picture only, no sound)
TMP = os.path.join(H, "_build"); os.makedirs(TMP, exist_ok=True)
FONTS = os.path.join(TMP, "fonts")
FAST = "--fast" in sys.argv
PRESET = "veryfast" if FAST else "slow"
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
N = json.load(open(os.path.join(H, "narration_v3.json"), encoding="utf-8"))
DJ = json.load(open(os.path.join(H, "audio", "durations_v3.json")))
D, ASRC = DJ["dur"], DJ["src"]
GRADE = "eq=contrast=1.05:saturation=1.07:gamma=0.98,vignette=PI/5"
XS, XF = 0.35, 0.5   # crossfades: inside a scene, between scenes
PAD = 0.8            # air after each scene's narration
END_HOLD = 6.0       # the end card


def ff(*a):
    subprocess.run([FF, "-y", "-loglevel", "error", *[str(x) for x in a]], check=True, cwd=TMP)


def dur(p):
    r = subprocess.run([FF, "-i", p], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r); return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


ENC = ["-c:v", "libx264", "-preset", PRESET, "-crf", "16", "-pix_fmt", "yuv420p", "-color_range", "tv"]
TV = "scale=out_range=tv,format=yuv420p"


# ---------------- shot makers ----------------
def still(key, src, dur_, crop, z0=1.0, z1=1.07, fx=0.5, fy=0.5, dx=0.0, dy=0.0):
    """Ken Burns on a 16:9 crop of a photo: 4K inside, eased zoom and drift."""
    n = int(round(dur_ * 30)); out = os.path.join(TMP, "s_%s_%d.mp4" % (key, n))
    if os.path.exists(out): return out
    cx, cy, cw, ch = crop
    e = "(on/%d)" % max(1, n - 1); ease = "(%s*%s*(3-2*%s))" % (e, e, e)
    z = "%f+(%f)*%s" % (z0, z1 - z0, ease)
    x = "(iw-iw/zoom)*(%f+(%f)*%s)" % (fx, dx, ease); y = "(ih-ih/zoom)*(%f+(%f)*%s)" % (fy, dy, ease)
    ff("-loop", "1", "-i", src, "-vf", "format=rgb24,crop=%d:%d:%d:%d,scale=3840:2160:flags=lanczos,zoompan=z='%s':x='%s':y='%s':d=%d:s=1920x1080:fps=30,%s,%s"
       % (cw, ch, cx, cy, z, x, y, n, GRADE, TV), "-frames:v", n, *ENC, out)
    return out


def reel(key, k, t0, t1, speed=1.0, band=0.40):
    """Meital's vertical reels (frames as in v2): a 16:9 band clear of her burned-in text and logo; slow motion by interpolation."""
    a, b = int(round(t0 * 30)), int(round(t1 * 30)); n = int(round((b - a) / speed))
    out = os.path.join(TMP, "r_%s_%s_%d_%d_%s.mp4" % (key, k, a, b, str(speed).replace(".", "")))
    if os.path.exists(out): return out
    vf = "crop=1054:593:8:%d,scale=1920:1080:flags=lanczos,unsharp=5:5:0.6" % int(1920 * band)
    if speed != 1.0: vf += ",setpts=PTS/%f,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir" % speed
    ff("-framerate", "30", "-start_number", a, "-i", os.path.join(REELS, k, "f%05d.jpg"), "-vf", vf + "," + GRADE + "," + TV,
       "-frames:v", n, *ENC, out)
    return out


def mclip(key, src, t0, t1, speed, crop, lift=0.0):
    """A piece of one of Meital's original reel files (picture only), cropped to 16:9 and slowed."""
    n = int(round((t1 - t0) / speed * 30)); out = os.path.join(TMP, "m_%s_%d.mp4" % (key, n))
    if os.path.exists(out): return out
    cx, cy, cw, ch = crop
    # this reel's own edit has lifted, milky blacks (darkest pixels at 50-90 of 255) and little colour: put the black point
    # back where the darkest pixel is and restore some colour, before the film's grade
    lv = "colorlevels=rimin=%.2f:gimin=%.2f:bimin=%.2f," % (lift, lift, lift) if lift else ""
    vf = "crop=%d:%d:%d:%d,scale=1920:1080:flags=lanczos,unsharp=5:5:0.8,%seq=saturation=1.45:gamma=0.97,setpts=(PTS-STARTPTS)/%f" % (cw, ch, cx, cy, lv, speed)
    if speed != 1.0: vf += ",minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir"
    ff("-ss", "%.3f" % t0, "-t", "%.3f" % (t1 - t0 + 0.2), "-i", src, "-an", "-vf", vf + "," + GRADE + "," + TV, "-r", "30", "-frames:v", n, *ENC, out)
    return out


def join(parts, out, xf=XS):
    if os.path.exists(out): return out
    if len(parts) == 1: shutil.copy(parts[0], out); return out
    ins = []; [ins.extend(["-i", p]) for p in parts]
    f = []; acc = dur(parts[0]); prev = "0:v"
    for i in range(1, len(parts)):
        lab = "v%d" % i; f.append("[%s][%d:v]xfade=transition=fade:duration=%f:offset=%f[%s]" % (prev, i, xf, acc - xf, lab)); acc += dur(parts[i]) - xf; prev = lab
    ff(*ins, "-filter_complex", ";".join(f), "-map", "[%s]" % prev, *ENC, out)
    return out


P = lambda n: os.path.join(REAL, n + ".jpg")
ST = lambda n: os.path.join(F, "stills", n + ".png")
TAGS = {
    "ill": ("Illustration", "איור"),
    "air": ("Aerial photo of the neighbourhood", "צילום אוויר של השכונה"),
    "airvid": ("Aerial video of the area", "צילום אוויר של האזור"),
    "today": ("Aerial photo · the neighbourhood and the park today", "צילום אוויר · השכונה והפארק היום"),
    "sim": ("Planned bridge · simulation", "הגשר המתוכנן · הדמיה"),
    "sdedov": ("Aerial photo · the Sde Dov quarter under construction", "צילום אוויר · רובע שדה דב בבנייה"),
}
# (maker, kwargs, tag). A still with dur None fills the scene to its narration + air.
S = [
 ("open", None, [
    (reel, dict(key="A", k="r2", t0=2.4, t1=3.85, speed=0.45, band=0.45), "airvid"),
    (still, dict(key="p09wide", src=P("L07_DZp43r5DIou_09"), dur_=None, crop=(0, 165, 1638, 921), z0=1.0, z1=1.07), "air")]),
 ("morning", ("MORNING", "בוקר"), [
    (still, dict(key="morning", src=ST("morning"), dur_=None, crop=(0, 80, 1536, 864), z0=1.04, z1=1.14, fx=0.35, dx=0.2), "ill"),
    (reel, dict(key="C", k="r2", t0=24.2, t1=25.0, speed=0.3, band=0.42), "airvid")]),
 ("centre", ("THE NEIGHBOURHOOD CENTRE", "המרכז השכונתי"), [
    (still, dict(key="cafe", src=ST("cafe"), dur_=4.4, crop=(0, 80, 1536, 864), z0=1.06, z1=1.14, fx=0.4, dx=0.15), "ill"),
    (still, dict(key="deli", src=ST("deli"), dur_=3.6, crop=(0, 80, 1536, 864), z0=1.05, z1=1.12), "ill"),
    (still, dict(key="nuts", src=ST("nuts"), dur_=None, crop=(0, 80, 1536, 864), z0=1.10, z1=1.02), "ill")]),
 ("bridge", ("THE BRIDGE TO YARKON PARK", "הגשר לפארק הירקון"), [
    (reel, dict(key="D", k="r2", t0=25.12, t1=26.0, speed=0.42, band=0.42), "airvid"),
    (still, dict(key="p09low", src=P("L07_DZp43r5DIou_09"), dur_=6.8, crop=(200, 480, 1280, 720), z0=1.0, z1=1.08, fy=0.85, dy=-0.7), "today"),
    (still, dict(key="bridgesim", src=ST("real_bridge_top"), dur_=None, crop=(560, 315, 880, 495), z0=1.0, z1=1.06, fx=0.4, dx=0.2), "sim")]),
 ("park", ("YARKON PARK", "פארק הירקון"), [
    (reel, dict(key="B", k="r2", t0=22.9, t1=24.1, speed=0.42, band=0.42), "airvid"),
    (still, dict(key="family", src=ST("park_family"), dur_=4.35, crop=(100, 445, 1040, 585), z0=1.0, z1=1.06), "ill"),
    (still, dict(key="sport", src=ST("sport"), dur_=2.65, crop=(0, 345, 1207, 679), z0=1.04, z1=1.0, fx=0.2), "ill"),
    (mclip, dict(key="dyrl_air", src=DYRL, t0=0.03, t1=1.87, speed=0.5, crop=(150, 305, 570, 321), lift=0.24), "airvid")]),
 ("home", ("A BRAND-NEW HOME", "בית חדש לגמרי"), [
    (still, dict(key="living", src=P("L07_DV6aYANjLBm_01"), dur_=4.6, crop=(0, 0, 1820, 1024), z0=1.0, z1=1.07, fx=0.45), ""),
    (reel, dict(key="h1", k="r2", t0=6.65, t1=8.05, speed=0.75, band=0.30), ""),
    (reel, dict(key="h2", k="r2", t0=11.0, t1=12.45, speed=0.8, band=0.40), ""),  # the living-room wall joinery, seen from the dining side
    (reel, dict(key="h3", k="r2", t0=8.15, t1=10.8, speed=0.9, band=0.30), ""),
    (reel, dict(key="h4", k="r1", t0=2.0, t1=4.4, speed=0.9, band=0.30), ""),
    (still, dict(key="kids", src=P("L07_DX9wx4ziADM_04"), dur_=None, crop=(0, 300, 1366, 768), z0=1.0, z1=1.07, fx=0.55), "")]),
 ("terrace", ("THE TERRACES", "המרפסות"), [
    (reel, dict(key="t1", k="r2", t0=20.2, t1=22.2, speed=0.75, band=0.42), ""),
    (reel, dict(key="t2", k="r1", t0=17.0, t1=19.6, speed=0.85, band=0.40), ""),
    (mclip, dict(key="dyrl_cov", src=DYRL, t0=23.0, t1=25.8, speed=0.55, crop=(0, 150, 720, 405), lift=0.24), "")]),
 ("numbers", ("THE NUMBERS", "המספרים"), [
    (mclip, dict(key="dyrl_view", src=DYRL, t0=29.05, t1=31.85, speed=0.26, crop=(0, 120, 720, 405), lift=0.28), ""),
    (still, dict(key="p06", src=P("L07_DX9wx4ziADM_06"), dur_=9.0, crop=(0, 130, 1440, 810), z0=1.0, z1=1.08, fx=0.6), "sdedov"),
    (still, dict(key="covered", src=P("L07_DX9wx4ziADM_03"), dur_=None, crop=(0, 300, 1366, 768), z0=1.0, z1=1.08, fx=0.6), "")]),
 ("close", None, [
    (reel, dict(key="dusk", k="r2", t0=26.8, t1=28.9, speed=0.55, band=0.38), ""),
    (still, dict(key="dusk_photo", src=P("L07_DV6aYANjLBm_02"), dur_=None, crop=(0, 0, 1820, 1024), z0=1.0, z1=1.08, fx=0.6), "")]),
]

# ---------------- scenes ----------------
scene_files, scene_d, shot_tl = [], [], []
for sid, title, shots in S:
    need = D[sid] + 0.5 + (PAD if sid != "close" else END_HOLD)
    parts = [None] * len(shots); fill = None
    for i, (fn, kw, tag) in enumerate(shots):
        if fn is still and kw["dur_"] is None: fill = i; continue
        parts[i] = fn(**kw)
    if fill is not None:
        rest = sum(dur(p) for p in parts if p) - XS * (len(parts) - 1)
        kw = dict(shots[fill][1]); kw["dur_"] = round(max(2.5, need - rest), 2); parts[fill] = still(**kw)
    total = sum(dur(p) for p in parts) - XS * (len(parts) - 1)
    if total < need - 0.05:  # hold the last shot
        last = parts[-1]; ext = need - total + 0.05; out = last.replace(".mp4", "_ext%d.mp4" % int(ext * 100))
        if not os.path.exists(out): ff("-i", last, "-vf", "tpad=stop_mode=clone:stop_duration=%f" % ext, *ENC, out)
        parts[-1] = out
    sf = join(parts, os.path.join(TMP, "scene_%s.mp4" % sid))
    scene_files.append(sf); scene_d.append(dur(sf))
    t = 0.0; tl = []
    for p, (fn, kw, tag) in zip(parts, shots):
        d_ = dur(p); tl.append((t, t + d_ - XS, tag, kw["key"])); t += d_ - XS
    shot_tl.append(tl)
    print(sid, "need %.2f got %.2f" % (need, scene_d[-1]), flush=True)

starts = []; acc = 0.0
for i, d_ in enumerate(scene_d):
    starts.append(acc); acc += d_ - (XF if i < len(scene_d) - 1 else 0)
TOTAL = acc
print("TOTAL", round(TOTAL, 2), flush=True)
body = os.path.join(TMP, "body.mp4")
if not os.path.exists(body):
    ins = []; [ins.extend(["-i", p]) for p in scene_files]
    f = []; prev = "0:v"; off = 0.0
    for i in range(1, len(scene_files)):
        off += scene_d[i - 1] - XF; lab = "b%d" % i
        f.append("[%s][%d:v]xfade=transition=fade:duration=%f:offset=%f[%s]" % (prev, i, XF, off, lab)); prev = lab
    ff(*ins, "-filter_complex", ";".join(f), "-map", "[%s]" % prev, *ENC, body)
# where every shot sits in the film (for CHANGES.md and the frame check)
json.dump({"total": TOTAL, "scenes": [{"sid": s[0], "start": round(st, 2), "dur": round(d_, 2),
           "shots": [{"key": k, "tag": tg, "from": round(st + a, 2), "to": round(st + b, 2)} for a, b, tg, k in tl]}
          for s, st, d_, tl in zip(S, starts, scene_d, shot_tl)]}, open(os.path.join(H, "timeline_v3.json"), "w"), indent=1)


# ---------------- caption timing: sentences snapped to the pauses in the voice ----------------
def silences(path):
    r = subprocess.run([FF, "-hide_banner", "-i", path, "-af", "silencedetect=n=-38dB:d=0.22", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return list(zip(s, e))


def split_sents(text):
    return [s.strip() for s in re.split(r"(?<=[.!?:])\s+", text) if s.strip()]


def timed(sid):
    """[(t0, t1)] per sentence, in scene time (the narration starts 0.5 s into the scene)."""
    p = os.path.join(H, ASRC[sid]); d = D[sid]; sil = silences(p)
    s0 = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    s1 = sil[-1][0] if sil and sil[-1][1] > d - 0.05 else d
    inner = [(a, b) for a, b in sil if a > s0 + 0.1 and b < s1 - 0.1]
    sents = split_sents(dict(N["scenes"])[sid])
    spoken = split_sents(N.get("say", {}).get(sid, dict(N["scenes"])[sid]))  # proportions from what is SAID ("twenty twenty-three", not "2023")
    if len(spoken) != len(sents): spoken = sents
    L = [len(x) for x in spoken]; tot = sum(L)
    cuts = []; accl = 0
    for k in range(len(sents) - 1):
        accl += L[k]; est = s0 + (s1 - s0) * accl / tot
        cand = [ab for ab in inner if abs((ab[0] + ab[1]) / 2 - est) < 1.6 and (not cuts or ab[0] > cuts[-1][1] + 0.3)]
        # a sentence ends on a longer breath: prefer the long pause near the estimate
        cuts.append(min(cand, key=lambda ab: abs((ab[0] + ab[1]) / 2 - est) - 0.8 * (ab[1] - ab[0])) if cand else (est, est))
    edges = [(s0, None)] + cuts + [(None, s1)]
    out = []
    for k in range(len(sents)):
        a = edges[k][1] if k else s0; b = edges[k + 1][0] if k + 1 < len(edges) - 1 else s1
        out.append((0.5 + a - 0.08, 0.5 + b + 0.25))
    return sents, out, [(0.5 + a, 0.5 + b) for a, b in inner]


def chunks(text, n, frac=0.5):
    """Split a long caption at the comma nearest `frac` of its length (n = 1 or 2)."""
    if n == 1: return [text]
    idx = [m.end() for m in re.finditer(r",\s", text)]
    if not idx: return [text]
    c = min(idx, key=lambda i: abs(i - len(text) * frac)); return [text[:c].strip(), text[c:].strip()]


# ---------------- the subtitle files ----------------
ACC = "&H00BFB34F"  # sea teal (BGR)


def ts(t):
    t = max(0, t); return "%d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)


CARDS = {  # (big, label, source): one card per slot; no price per square metre anywhere
 "en": [("NIS 6.1M", "median home deal in Kochav HaTzafon, 2023 to Oct 2025", "4th highest in Israel · Mako"),
        ("16,000", "new homes planned in the Sde Dov quarter, to the north", "Approved plan, Tel Aviv District Committee"),
        ("2028", "planned opening of the Green Line light rail", "Maariv, Aug 2025"),
        ("100 m", "homes this close to Yarkon Park were worth more", "Technion study, Shefer & Zakai, 2003"),
        ("+5% to 20%+", "home values next to new city park links abroad", "HR&A Advisors, 2014")],
 "he": [("6.1 מיליון ₪","העסקה החציונית בכוכב הצפון, 2023 עד אוקטובר 2025", "הרביעית בגובהה בישראל · מאקו"),
        ("16,000", "דירות חדשות מתוכננות ברובע שדה דב, מצפון", "תוכנית מאושרת, הוועדה המחוזית תל אביב"),
        ("2028", "פתיחה מתוכננת של הקו הירוק ברכבת הקלה", "מעריב, אוגוסט 2025"),
        ("100 מטר", "דירות במרחק כזה מפארק הירקון היו שוות יותר", "מחקר הטכניון, שפר וזכאי, 2003"),
        ("5%–20%+", "ערך דירות ליד חיבורים חדשים לפארקים בעולם", "HR&A Advisors, 2014")],
}
TXT = {
 "en": dict(title="KOCHAV HATZAFON", tagline="A new mini penthouse in a new boutique building · north Tel Aviv",
            area="Area data, not a valuation of this home",
            e1="Mini penthouse · Kochav HaTzafon", e2="A new home in a new boutique building, north Tel Aviv",
            e3="5 rooms  ·  about 197 sqm  ·  about 80 sqm of terraces  ·  floor 11", e4="PRIVATE VIEWING",
            e5="Meital Katzir · Nadlan Al HaYam", e6="052-3631582", e7="From abroad +972 52-363-1582  ·  nad-lan.co.il"),
 "he": dict(title="כוכב הצפון", tagline="מיני פנטהאוז חדש בבניין בוטיק חדש · צפון תל אביב",
            area="נתוני אזור, לא הערכת שווי של הנכס",
            e1="מיני פנטהאוז · כוכב הצפון", e2="נכס חדש בבניין בוטיק חדש, צפון תל אביב",
            e3="5 חדרים  ·  כ-197 מ״ר  ·  כ-80 מ״ר מרפסות  ·  קומה 11", e4="לתיאום צפייה פרטית",
            e5="מיטל קציר · נדל״ן על הים", e6="052-3631582", e7="nad-lan.co.il"),
}


def build_ass(lang):
    he = lang == "he"; L = TXT[lang]
    LAT, HEB, SEG, SEGL = "Bahnschrift", "Gisha", "Segoe UI", "Segoe UI Semilight"
    big = HEB if he else LAT; sub = HEB if he else LAT; lab = SEG if he else SEGL
    e = "-1" if he else "1"  # -1: libass picks the base direction from the text (right-to-left for Hebrew)
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "WrapStyle: 0", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           "Style: Chap,%s,%d,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,%d,0,0,0,100,100,%d,0,1,0,2,7,110,110,92,%s" % (big, 44 if he else 40, 1 if he else 0, 1 if he else 9, e),
           "Style: Big,%s,%d,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,2,0,1,0,3,1,110,110,250,%s" % (big, 112 if he else 104, e),
           "Style: Sub,%s,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,3,14,0,2,250,250,64,%s" % (sub, 44 if he else 40, e),
           "Style: Tag,Segoe UI,%d,&H00E6E6E6,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,1,0,1,1,1,9,60,52,132,%s" % (24 if he else 22, e),
           "Style: Num,Bahnschrift,118,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,0,0,1,0,3,1,110,110,330,1",
           "Style: NumH,Gisha,112,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,0,0,1,0,3,1,110,110,330,-1",
           "Style: Lab,%s,%d,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,0,0,1,1.4,2,1,112,110,270,%s" % (lab, 40 if he else 38, e),
           "Style: Src,Segoe UI,%d,&H00D0D0D0,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,1,0,1,1,1,1,114,110,236,%s" % (26 if he else 22, e),
           "Style: End1,%s,66,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,2,0,1,0,3,5,110,110,0,%s" % (big, e),
           "Style: End2,%s,38,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,0,0,1,1.2,2,5,110,110,0,%s" % (lab, e),
           "Style: EndN,%s,70,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,1,0,1,0,3,5,110,110,0,%s" % (big, e),
           "Style: EndP,Bahnschrift,118,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,1,0,0,0,100,100,3,0,1,0,3,5,110,110,0,1",
           "Style: EndS,%s,30,&H00FFFFFF,&H00FFFFFF,&H64000000,&H00000000,0,0,0,0,100,100,%d,0,1,1.2,2,5,110,110,0,%s" % (lab if he else SEG, 1 if he else 6, e),
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    ev = lambda a, b, st, txt, l=0: ass.append("Dialogue: %d,%s,%s,%s,,0,0,0,,%s" % (l, ts(a), ts(b), st, txt))
    bar = "{\\c%s}━━{\\c&H00FFFFFF}" % ACC
    for (sid, title, shots), st, d_, tl in zip(S, starts, scene_d, shot_tl):
        if title:
            ev(st + 0.3, st + 4.2, "Chap", "{\\fad(400,500)}%s  %s" % (bar, title[1 if he else 0]))
        for a, b, tag, key in tl:
            if tag: ev(st + a + 0.25, st + b - 0.1, "Tag", "{\\fad(300,300)}" + TAGS[tag][1 if he else 0])
        sents, times, inner = timed(sid)
        hes = N["he"][sid]; assert len(hes) == len(sents), (sid, len(hes), len(sents))
        for k, ((a, b), en_s, he_s) in enumerate(zip(times, sents, hes)):
            b = min(b, times[k + 1][0] - 0.04) if k + 1 < len(times) else b
            n = 2 if len(en_s) > 100 or len(he_s) > 90 else 1
            ce = chunks(en_s, n); ch_ = chunks(he_s, len(ce), len(ce[0]) / max(1, len(en_s)))
            if len(ce) != len(ch_): ce, ch_ = [en_s], [he_s]
            if len(ce) == 2:  # split at the pause inside the sentence if there is one, else by length
                est = a + (b - a) * len(ce[0]) / (len(ce[0]) + len(ce[1]))
                near = [m for m in inner if a + 0.8 < m[0] < b - 0.8 and abs((m[0] + m[1]) / 2 - est) < 1.4]
                if near:
                    mid = min(near, key=lambda m: abs((m[0] + m[1]) / 2 - est)); spans = [(a, mid[0] + 0.15), (mid[1] - 0.08, b)]
                else:
                    spans = [(a, est - 0.03), (est, b)]
            else:
                spans = [(a, b)]
            for (x0, x1), c in zip(spans, ch_ if he else ce):
                ev(st + x0, st + x1, "Sub", c)
    # the opening title
    if he:
        ev(0.6, 5.8, "Big", "{\\an3\\pos(1810,690)\\fad(700,700)}" + L["title"])
        ev(1.0, 5.8, "Lab", "{\\an9\\pos(1807,712)\\fad(700,700)\\fs44}%s  %s" % (bar, L["tagline"]))
    else:
        ev(0.6, 5.8, "Big", "{\\an1\\pos(110,690)\\fad(700,700)}" + L["title"])
        ev(1.0, 5.8, "Lab", "{\\an7\\pos(113,712)\\fad(700,700)\\fs42}%s  %s" % (bar, L["tagline"]))
    # the numbers: one card per slot, following the sentences
    i_num = [s[0] for s in S].index("numbers"); s0n = starts[i_num]; sents, times, inner = timed("numbers")
    (a1, b1), (a2, b2), (a3, b3) = times[1], times[2], times[3]
    def split_at_pause(a, b, frac):
        est = a + (b - a) * frac; near = [m for m in inner if a + 1.0 < m[0] < b - 1.0]
        m = min(near, key=lambda m: abs((m[0] + m[1]) / 2 - est)) if near else (est, est); return (m[0] + m[1]) / 2
    m2 = split_at_pause(a2, b2, 0.55); m3 = split_at_pause(a3, b3, 0.45)
    slots = [(a1, b1), (a2, m2), (m2, b2), (a3, m3), (m3, scene_d[i_num] - 0.7)]
    for k, (bigt, labt, srct) in enumerate(CARDS[lang]):
        a, b = s0n + slots[k][0] + 0.05, s0n + slots[k][1] - 0.05
        if he:
            ev(a, b, "NumH" if re.search("[֐-׿]", bigt) else "Num", "{\\an3\\pos(1810,700)\\fad(350,300)}" + bigt, 2)
            ev(a + 0.15, b, "Lab", "{\\an9\\pos(1807,722)\\fad(350,300)}" + labt, 2)
            ev(a + 0.3, b, "Src", "{\\an9\\pos(1805,780)\\fad(350,300)}" + srct, 2)
        else:
            ev(a, b, "Num", "{\\an1\\pos(110,700)\\fad(350,300)}" + bigt, 2)
            ev(a + 0.15, b, "Lab", "{\\an7\\pos(113,722)\\fad(350,300)}" + labt, 2)
            ev(a + 0.3, b, "Src", "{\\an7\\pos(115,778)\\fad(350,300)}" + srct, 2)
    ev(s0n + 0.8, s0n + scene_d[i_num] - 0.8, "Tag", "{\\fad(300,300)}" + L["area"])
    # the end card: who to call, large and clear
    e0 = TOTAL - END_HOLD + 0.2
    ev(e0, TOTAL, "End1", "{\\fad(600,0)\\pos(960,250)}" + L["e1"], 3)
    ev(e0 + 0.2, TOTAL, "End2", "{\\fad(600,0)\\pos(960,330)}" + L["e2"], 3)
    ev(e0 + 0.35, TOTAL, "End2", "{\\fad(600,0)\\pos(960,386)\\fs34}" + L["e3"], 3)
    ev(e0 + 0.6, TOTAL, "EndS", "{\\fad(600,0)\\pos(960,505)\\c%s}%s" % (ACC, L["e4"]), 3)
    ev(e0 + 0.7, TOTAL, "EndN", "{\\fad(600,0)\\pos(960,580)}" + L["e5"], 3)
    ev(e0 + 0.85, TOTAL, "EndP", "{\\fad(600,0)\\pos(960,700)}" + L["e6"], 3)
    ev(e0 + 1.0, TOTAL, "EndS", "{\\fad(600,0)\\pos(960,800)}" + L["e7"], 3)
    p = os.path.join(H, "film_%s.ass" % lang)
    open(p, "w", encoding="utf-8").write("\n".join(ass)); return p


# ---------------- sound: the narration on its scenes, the music bed under it, -16 LUFS ----------------
mus = os.path.join(H, "audio", "music_temp.wav")
need_mus = TOTAL + 1
if not os.path.exists(mus) or dur(mus) < need_mus:
    subprocess.run([sys.executable, os.path.join(F, "music_temp.py"), "%.1f" % need_mus], check=True, cwd=H)  # writes v3/audio/
mix = os.path.join(TMP, "mix.wav"); norm = os.path.join(TMP, "mix_norm.wav")
if not os.path.exists(norm):
    ains = ["-i", mus]; af = []
    for i, (sid, _, _) in enumerate(S):
        ains += ["-i", os.path.join(H, ASRC[sid])]
        ms = int((starts[i] + 0.5) * 1000); af.append("[%d:a]adelay=%d|%d,aformat=sample_rates=48000:channel_layouts=stereo[n%d]" % (i + 1, ms, ms, i))
    af.append("".join("[n%d]" % i for i in range(len(S))) + "amix=inputs=%d:normalize=0,asplit=2[nar][nar2]" % len(S))
    af.append("[0:a]atrim=0:%f,afade=t=in:d=2,afade=t=out:st=%f:d=4,volume=0.42[mb]" % (TOTAL, TOTAL - 4))
    af.append("[mb][nar]sidechaincompress=threshold=0.04:ratio=6:attack=40:release=600[duck]")
    af.append("[duck][nar2]amix=inputs=2:normalize=0,atrim=0:%f[aout]" % TOTAL)
    ff(*ains, "-filter_complex", ";".join(af), "-map", "[aout]", "-ar", "48000", "-c:a", "pcm_s24le", mix)
    r = subprocess.run([FF, "-hide_banner", "-i", mix, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    ff("-i", mix, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true,aresample=48000"
       % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]), "-ar", "48000", "-c:a", "pcm_s24le", norm)

# ---------------- the picture: gradient under the number cards, titles, end card, watermark ----------------
if not os.path.isdir(FONTS):
    os.makedirs(FONTS)
    for fn in ["bahnschrift.ttf", "segoeui.ttf", "segoeuib.ttf", "segoeuil.ttf", "segoeuisl.ttf", "gisha.ttf", "gishabd.ttf"]:
        shutil.copy(os.path.join(r"C:\Windows\Fonts", fn), FONTS)
from PIL import Image
import numpy as np
for side in ("l", "r"):
    g = os.path.join(TMP, "grad_%s.png" % side)
    if not os.path.exists(g):
        x = np.linspace(0, 1, 1920); al = (np.clip(1 - x / 0.62, 0, 1) ** 1.6 * 0.78 * 255).astype("uint8")
        if side == "r": al = al[::-1]
        im = np.zeros((1080, 1920, 4), "uint8"); im[..., 3] = al[None, :]; Image.fromarray(im, "RGBA").save(g)
i_num = [s[0] for s in S].index("numbers"); gn0 = starts[i_num] + 0.2; gn1 = starts[i_num] + scene_d[i_num] - 0.5
for lang in ("en", "he"):
    if ONLY and lang != ONLY: continue
    ass = build_ass(lang); shutil.copy(ass, os.path.join(TMP, os.path.basename(ass)))
    if "--ass-only" in sys.argv: print("ass:", ass); continue
    out = os.path.join(H, "kochav-film-en-v3.mp4" if lang == "en" else "kochav-film-en-v3-he.mp4")
    vf = ["[1:v]format=rgba,fade=t=in:st=%f:d=0.7:alpha=1,fade=t=out:st=%f:d=0.7:alpha=1[g]" % (gn0, gn1),
          "[0:v][g]overlay=0:0:shortest=1[v1]",
          "[v1]drawbox=x=0:y=0:w=1920:h=1080:color=black@0.58:t=fill:enable='gte(t,%f)',subtitles=%s:fontsdir=fonts,fade=t=in:d=0.8,fade=t=out:st=%f:d=1.2[v0]"
          % (TOTAL - END_HOLD, os.path.basename(ass), TOTAL - 1.2),
          "[3:v]format=rgba,colorchannelmixer=aa=0.82,scale=400:-1[wm]", "[v0][wm]overlay=W-w-40:34:shortest=1,%s,setsar=1[v]" % TV]  # square pixels (crops rescaled to 16:9 carry a tiny SAR otherwise)
    ff("-i", body, "-loop", "1", "-framerate", "30", "-i", os.path.join(TMP, "grad_%s.png" % ("r" if lang == "he" else "l")), "-i", norm,
       "-loop", "1", "-framerate", "30", "-i", os.path.join(F, "wm.png"),
       "-filter_complex", ";".join(vf), "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", PRESET, "-crf", "18", "-pix_fmt", "yuv420p",
       "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-r", "30",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", "%f" % TOTAL, out)
    print("film:", out, round(TOTAL, 2), "s", flush=True)

# ---------------- the poster: a real shot of the home (Meital's photograph of the living room), graded as in the film ----------------
if "--ass-only" in sys.argv: sys.exit(0)
poster = os.path.join(H, "kochav-film-v3.jpg")
liv = [sh for sc in json.load(open(os.path.join(H, "timeline_v3.json")))["scenes"] for sh in sc["shots"] if sh["key"] == "living"][0]
tp = liv["from"] + 1.2
ff("-ss", "%.2f" % tp, "-i", body, "-loop", "1", "-i", os.path.join(F, "wm.png"), "-filter_complex",
   "[1:v]format=rgba,colorchannelmixer=aa=0.82,scale=400:-1[wm];[0:v][wm]overlay=W-w-40:34", "-frames:v", "1", "-q:v", "2", poster)
print("poster:", poster)
