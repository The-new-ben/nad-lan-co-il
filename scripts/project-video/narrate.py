# -*- coding: utf-8 -*-
"""Voice a project video: data/<slug>.narration.json -> audio/<slug>/<id>.mp3 + the timings the composer needs.

  C:\\Users\\777\\nad-lan\\voice-rig\\venv\\Scripts\\python.exe narrate.py --project rainbow-tel-aviv [--force]

Runs in the voice-rig venv (edge-tts 7.2.8, mutagen). Each line's 'spoken' text is read by he-IL-AvriNeural at the
file's rate (-8%, the site's tours). A scene that is too short for its line is stretched (never the voice rushed):
  scene dur = max(silent dur, at + speech end + tail)            (the line ends before the scene's text fades out)
  view item = max(silent share, at + speech end + 0.45)          (each view card gets its own line)
  facilities list: the names are revealed in step with the voice
The result goes back into the narration JSON under "timing" (and each line gets 'file' and 'secs'); composer.html
applies it only with &narr=1, so the silent film keeps its own timing.
"""
import argparse, asyncio, json, math, os

ROOT = os.path.dirname(os.path.abspath(__file__))


def up(x, step=0.05):
    return round(math.ceil(x / step - 1e-9) * step, 2)


async def synth(text, voice, rate, path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="rainbow-tel-aviv")
    ap.add_argument("--force", action="store_true", help="re-synthesize clips that already exist")
    # 28.9.2026: the owner found edge-tts's Hebrew poor; Chatterbox + Dicta (his 4.7/5 blind test, tts_chatterbox.py)
    ap.add_argument("--engine", choices=("edge", "chatterbox"), default="edge")
    ap.add_argument("--lang", default="he")
    args = ap.parse_args()
    from mutagen.mp3 import MP3
    npath = os.path.join(ROOT, "data", f"{args.project}.narration.json")
    N = json.load(open(npath, encoding="utf-8"))
    D = json.load(open(os.path.join(ROOT, "data", f"{args.project}.json"), encoding="utf-8"))
    out_dir = os.path.join(ROOT, "audio", args.project + ("" if args.engine == "edge" else "-" + args.engine))
    os.makedirs(out_dir, exist_ok=True)
    lead, tail = N.get("lead", 0.35), N.get("tail", 0.55)
    for L in N["lines"]:
        path = os.path.join(out_dir, L["id"] + (".mp3" if args.engine == "edge" else ".wav"))
        if args.force or not os.path.exists(path):
            if args.engine == "edge":
                asyncio.run(synth(L["spoken"], N["voice"], N["rate"], path))
            else:
                from tts_chatterbox import synth_wav
                import time
                for attempt in range(4):  # the voice server sleeps when idle: 503/504 while it wakes
                    try:
                        synth_wav(L["spoken"], args.lang, path)
                        break
                    except Exception as e:
                        if attempt == 3:
                            raise
                        print("  wait (%s)" % str(e)[:60]); time.sleep(40)
        L["file"] = os.path.relpath(path, ROOT).replace("\\", "/")
        if path.endswith(".wav"):
            import wave
            with wave.open(path, "rb") as w:
                L["secs"] = round(w.getnframes() / float(w.getframerate()), 3)
        else:
            L["secs"] = round(MP3(path).info.length, 3)
        # where the speech really starts and ends (edge-tts pads ~0.2 s before and ~0.9 s after)
        import librosa
        y, sr = librosa.load(path, sr=None, mono=True)
        idx = librosa.effects.split(y, top_db=40)
        L["speech"] = [round(idx[0][0] / sr, 3), round(idx[-1][1] / sr, 3)]
        # the onset the audio check uses: first 10 ms window at 5% of the clip's loudest window (render.py audio)
        import numpy as np
        hop = sr // 100
        rms = np.sqrt(np.array([np.mean(y[i:i + hop] ** 2) for i in range(0, len(y) - hop, hop)]))
        L["onset"] = round(int(np.argmax(rms >= rms.max() * 0.05)) / 100, 2)
        print(f"{L['id']:11} {L['secs']:5.2f} s  speech {L['speech'][0]:.2f}-{L['speech'][1]:.2f}  {L['text']}")

    scenes = {s["id"]: s for s in D["scenes"]}
    timing = {"scenes": {}, "viewItems": None, "list": None}
    for sid, s in scenes.items():
        lines = [L for L in N["lines"] if L["scene"] == sid]
        dur = s["dur"]
        if s["type"] == "views":
            n = len(s["items"]); share = s["dur"] / n
            items = []
            for k in range(n):
                Lk = next((L for L in lines if L.get("item") == k), None)
                need = (Lk.get("at", lead if k == 0 else 0.3) + Lk["speech"][1] + 0.45) if Lk else share
                if Lk:
                    Lk["at"] = Lk.get("at", lead if k == 0 else 0.3)
                items.append(up(max(share, need)))
            timing["viewItems"] = items
            dur = round(sum(items), 2)
        elif lines:
            L = lines[0]
            L["at"] = L.get("at", lead)
            end_pad = 1.0 if s["type"] == "outro" else tail
            dur = up(max(s["dur"], L["at"] + L["speech"][1] + end_pad))
            if s["type"] == "list":
                n = len(s["items"])
                sp = L["speech"][1] - L["speech"][0]
                timing["list"] = {"start": round(L["at"] + L["speech"][0] + 0.1, 2), "step": round(max(0.85, (sp - 0.6) / n), 2)}
                dur = up(max(dur, timing["list"]["start"] + timing["list"]["step"] * (n - 1) + 1.2 + tail))
        timing["scenes"][sid] = dur
    total = round(sum(timing["scenes"].values()), 2)
    timing["total"] = total
    N["timing"] = timing
    json.dump(N, open(npath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    silent = round(sum(s["dur"] for s in D["scenes"]), 2)
    print("scene durations:", json.dumps(timing["scenes"]), "views:", timing["viewItems"], "list:", timing["list"])
    print(f"total {total} s (silent film {silent} s)")


if __name__ == "__main__":
    main()
