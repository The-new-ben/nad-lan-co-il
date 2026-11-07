# -*- coding: utf-8 -*-
"""One place for the paths and the variant files of the nad-lan developer film (every build script imports this).

A variant is one version of the film: variants/<name>.json (audience, languages, voice, scenes with the English voice-over and the
Hebrew subtitle lines, the picture module of every scene, the output file names). With no --variant the approved film is built:
main-he.

  ROOT   docs/sales/developer-film-v3 (this repo folder: variants, voice takes, captures, scripts, finished films)
  WORK   C:/Users/777/Documents/film-studio-work/nadlan-developer-film (outside the repo, too big and partly Ben's footage):
         web/ (every picture the film page draws, shared by all variants), casts_raw/ (the raw screencasts), v2_assets.json,
         var/<name>/ (one variant's sound and frames)
"""
import json, os, sys

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(H)
WORK = os.environ.get("NADLAN_FILM_WORK", r"C:\Users\777\Documents\film-studio-work\nadlan-developer-film")
WEB = os.path.join(WORK, "web")
DEFAULT = "main-he"
FF = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
KOKORO_PY = r"C:\Users\777\nad-lan\voice-rig\venv\Scripts\python.exe"     # Kokoro, Whisper, vo_build (numpy + soundfile)
SYS_PY = r"C:\Users\777\AppData\Local\Programs\Python\Python311\python.exe"  # Playwright, Pillow, the music bed (as built in v2/v3)


def arg(name, default=None, argv=None):
    a = sys.argv if argv is None else argv
    return a[a.index(name) + 1] if name in a else default


def name(argv=None):
    return arg("--variant", DEFAULT, argv)


def load(n=None):
    n = n or name()
    v = json.load(open(os.path.join(ROOT, "variants", n + ".json"), encoding="utf-8"))
    assert v["name"] == n, ("the file name and the name inside differ", n, v["name"])
    return v


class Paths:
    """every place one variant reads or writes; --out <dir> (relative to ROOT) writes the finished files elsewhere (a check run)"""
    def __init__(self, v, argv=None):
        self.v = v; n = v["name"]; o = v.get("outputs", {})
        self.out = os.path.join(ROOT, arg("--out", o.get("dir", "out/" + n), argv))
        self.work = os.path.join(WORK, "var", n)
        self.audio = os.path.join(self.work, "audio")
        self.takes = os.path.join(ROOT, v.get("voice", {}).get("takes", "out/%s/voice" % n))
        self.tl_web = os.path.join(WEB, "timelines", n + ".json")      # what film.html reads (?tl=timelines/<name>.json)
        self.tl_rel = "timelines/%s.json" % n
        self.files = {k: os.path.join(self.out, o.get(k, d)) for k, d in (
            ("h", "en-vo_he-sub_16x9.mp4"), ("v", "en-vo_he-sub_9x16.mp4"), ("web", "he-web-16x9.mp4"), ("poster", "poster-16x9.jpg"),
            ("sheet_h", "en-vo_he-sub_16x9-sheet.jpg"), ("sheet_v", "en-vo_he-sub_9x16-sheet.jpg"), ("timeline", "timeline.json"),
            ("whisper", "whisper_check.json"), ("voice_flac", "voice-over.flac"))}

    def frames(self, f):
        return os.path.join(self.work, "frames_" + f)


def scenes_check(v):
    """the rules every variant keeps (also run by film.py before a build)"""
    bad = []
    for s in v["scenes"]:
        for g in s["groups"]:
            for t in [g["en"], g.get("say", "")] + g["he"] + list(s.get("screen", {}).values()):
                if "\u2014" in t or "\u2013" in t:
                    bad.append("long dash: " + t)
                low = t.lower()
                for w in ("broker", "hotjar", "realtor", "מתווך", "מתווכ", "תיווך", "ceo", "מנכ\"ל", "מנכ״ל"):
                    if w in low:
                        bad.append("forbidden word '%s': %s" % (w, t))
    mods = [s.get("module", s["id"]) for s in v["scenes"]]
    if len(mods) != len(set(mods)):
        bad.append("a picture module is used twice: %s" % mods)
    return bad
