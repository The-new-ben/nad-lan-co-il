# -*- coding: utf-8 -*-
"""Screening check of the finished sound (not a listening test): local Whisper small (cached, CPU, no download) on the mix,
word timestamps, each voice block of timeline.json compared with its script line (normalised words, edit distance).

  python whisper_check.py <mix.wav> <timeline.json> <out.json>
"""
import json, re, sys
import numpy as np, librosa, whisper

NUM = {"23": "twenty three", "12": "twelve", "10": "ten", "7": "seven", "360": "three sixty"}


def norm(s):
    s = s.lower().replace("-", " ").replace("’", "'")
    s = re.sub(r"\b(\d+)\b", lambda m: NUM.get(m.group(1), m.group(1)), s)
    s = s.replace("nadlan.co.il", "nad lan dot co dot eel").replace("co.il", "co dot eel").replace("a.i.", "a i").replace(" ai ", " a i ")
    return re.sub(r"[^a-z' ]", " ", s).split()


def dist(r, h):
    d = np.zeros((len(r) + 1, len(h) + 1), int); d[:, 0] = range(len(r) + 1); d[0, :] = range(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (r[i - 1] != h[j - 1]))
    return int(d[-1, -1])


if __name__ == "__main__":
    mix, tl, out = sys.argv[1:4]
    T = json.load(open(tl, encoding="utf-8"))
    y, _ = librosa.load(mix, sr=16000)
    m = whisper.load_model("small", device="cpu")
    r = m.transcribe(y.astype(np.float32), language="en", temperature=0, beam_size=5, fp16=False, word_timestamps=True)
    words = [(w["start"], w["end"], w["word"].strip()) for s in r["segments"] for w in s.get("words", [])]
    rows = []; tot = err = 0
    for b in T["voice"]:
        hyp = " ".join(w for a, e, w in words if (a + e) / 2 >= b["a"] - .25 and (a + e) / 2 <= b["b"] + .25)
        ref = b["en"] if "say" not in b else b["say"]
        e = dist(norm(ref), norm(hyp)); tot += len(norm(ref)); err += e
        rows.append({"scene": b["scene"], "k": b["k"], "a": b["a"], "script": ref, "heard": hyp, "wordDiffs": e})
    res = {"whisper": "small (cached C:/Users/777/.cache/whisper/small.pt), CPU, temperature 0, beam 5, language en, word timestamps",
           "note": "ASR screening only, not a naturalness or listening judgement", "scriptWords": tot, "wordDiffs": err,
           "fullTranscript": r["text"].strip(), "blocks": rows}
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("words", tot, "diffs", err)
    for x in rows:
        if x["wordDiffs"]:
            print(f'{x["scene"]}.{x["k"]} [{x["wordDiffs"]}] script: {x["script"]}\n      heard: {x["heard"]}')
