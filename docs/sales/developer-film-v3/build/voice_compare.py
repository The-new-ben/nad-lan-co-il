# -*- coding: utf-8 -*-
"""Screen the voice test takes (no listening claim): Whisper small (cached, CPU) transcript and word errors against the
script, speaking rate, pitch (pYIN) median and spread in semitones, pause share. Run with the voice-rig venv python.

  python voice_compare.py <tests_dir>      -> <tests_dir>/compare.json
"""
import glob, json, os, re, sys
import numpy as np, librosa, whisper

REF = ("Your marketing department runs the campaign. We're the special unit you send in for one mission: "
       "bringing you buyers who are ready to sign. Nad lan dot co dot il, slash marketing.")
norm = lambda s: re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("-", " ")).split()


def wer(r, h):
    d = np.zeros((len(r) + 1, len(h) + 1), int); d[:, 0] = range(len(r) + 1); d[0, :] = range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return int(d[-1, -1])


if __name__ == "__main__":
    D = sys.argv[1]
    m = whisper.load_model("small", device="cpu")
    out = []
    for f in sorted(glob.glob(os.path.join(D, "*.wav"))):
        y, sr = librosa.load(f, sr=16000)
        tr = m.transcribe(y.astype(np.float32), language="en", temperature=0, beam_size=5, fp16=False)["text"].strip()
        f0, vf, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, frame_length=1024)
        f0 = f0[~np.isnan(f0)]
        st = 12 * np.log2(f0 / np.median(f0))
        rms = librosa.feature.rms(y=y, frame_length=512, hop_length=160)[0]
        silent = float((rms < 0.1 * np.median(rms[rms > 0])).mean())
        rec = {"file": os.path.basename(f), "seconds": round(len(y) / sr, 2), "transcript": tr,
               "wordErrors": wer(norm(REF), norm(tr)), "refWords": len(norm(REF)),
               "wordsPerSecond": round(len(norm(REF)) / (len(y) / sr), 2),
               "f0MedianHz": round(float(np.median(f0)), 1), "pitchSpreadSemitones": round(float(np.std(st)), 2),
               "pitchRange90Semitones": round(float(np.percentile(st, 95) - np.percentile(st, 5)), 2),
               "pauseShare": round(silent, 3)}
        out.append(rec); print(json.dumps(rec, ensure_ascii=False), flush=True)
    json.dump({"reference": REF, "whisper": "small, CPU, temperature 0, beam 5", "takes": out},
              open(os.path.join(D, "compare.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
