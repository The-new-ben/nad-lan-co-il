# -*- coding: utf-8 -*-
"""Listen to a narrated cut: whisper (small, Hebrew) on the 16 kHz WAV that `render.py audio` saved, per line window and
for the whole track, compared with the script in data/<slug>.narration.json.

  C:\\Users\\777\\nad-lan\\voice-rig\\venv\\Scripts\\python.exe tools\\transcribe.py --project rainbow-tel-aviv ^
      --wav frames\\rainbow-tel-aviv_1080x1920_narrated_web_16k.wav --size 1080x1920

Whisper small is an imperfect judge of Hebrew (it misspells and writes numbers as digits); the per-line word match
below ignores punctuation and vowel marks, so the diffs are the signal, not the score.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOLD_S = 6 / 30


def norm(s):
    s = re.sub(r"[\u0591-\u05C7]", "", s)                 # vowel marks
    s = s.replace("״", "").replace('"', "").replace("׳", "").replace("'", "")
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if w]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="rainbow-tel-aviv")
    ap.add_argument("--wav", required=True)
    ap.add_argument("--clips", default=None, help="JSON file with the composer's narration clips (start per line)")
    ap.add_argument("--model", default="small")
    args = ap.parse_args()
    import numpy as np, librosa, whisper
    N = json.load(open(os.path.join(ROOT, "data", f"{args.project}.narration.json"), encoding="utf-8"))
    audio, _ = librosa.load(args.wav, sr=16000, mono=True)
    wm = whisper.load_model(args.model)
    starts = None
    if args.clips:
        starts = {c["id"]: c["start"] for c in json.load(open(args.clips, encoding="utf-8"))}
    rows = []
    for L in N["lines"]:
        if starts is None:
            break
        t0 = HOLD_S + starts[L["id"]]
        t1 = t0 + L["secs"]
        seg = audio[int(t0 * 16000): int(t1 * 16000)].astype(np.float32)
        r = wm.transcribe(seg, language="he", fp16=False, condition_on_previous_text=False)
        heard = r["text"].strip()
        want = norm(L["text"]); got = norm(heard)
        hit = sum(1 for w in want if w in got)
        rows.append({"id": L["id"], "script": L["text"], "heard": heard, "words_matched": f"{hit}/{len(want)}"})
        print(f"{L['id']:10} {hit:2}/{len(want):<2}  SCRIPT: {L['text']}\n{'':16}HEARD:  {heard}", flush=True)
    full = wm.transcribe(audio.astype(np.float32), language="he", fp16=False)["text"].strip()
    print("\nWHOLE TRACK HEARD:", full)
    out = os.path.splitext(args.wav)[0] + "_transcript.json"
    json.dump({"wav": args.wav, "model": args.model, "lines": rows, "whole": full}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", out)


if __name__ == "__main__":
    main()
