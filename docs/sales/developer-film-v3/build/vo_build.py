# -*- coding: utf-8 -*-
"""Lay the voice-over on the film's timeline, time the Hebrew subtitles to it, and mix the sound (local only).

  python vo_build.py <voice_dir> <out_dir> [--bed <bed.wav>]

- <voice_dir>/<scene>_<group>.wav from voice_kokoro.py (one generation per group of script_v3.json)
- every take is trimmed of its own silence (-45 dB, 40 ms kept), then placed: the scene's lead, the groups with their gaps
  (default 0.32 s), the scene's tail; the next scene starts where this one ends
- a group with two subtitle lines is split at the pause nearest to its "split" fraction (the pause found in the take itself)
- out: vo.wav (48 kHz stereo, the voice only, -16 LUFS), timeline.json (scenes, voice blocks, subtitle cues), and with --bed
  mix.wav: the bed ducked 12 dB under the voice (pauses shorter than 1.6 s keep it ducked), then the whole mix to -16 LUFS
  integrated, true peak -1.5 dBTP (two-pass ffmpeg loudnorm, linear)
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf

FF = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
H = os.path.dirname(os.path.abspath(__file__))
SR = 48000


def load48(fn):
    y, sr = sf.read(fn, dtype="float32")
    if y.ndim > 1:
        y = y.mean(1)
    if sr != SR:   # band-limited resample by FFT (the takes are 24 kHz)
        n = int(round(len(y) * SR / sr)); Y = np.fft.rfft(y); Z = np.zeros(n // 2 + 1, complex); Z[:len(Y)] = Y
        y = np.fft.irfft(Z, n) * (SR / sr)
    return y.astype(np.float32)


def rms_db(y, win=0.02):
    w = int(SR * win); n = len(y) // w
    r = np.sqrt((y[:n * w].reshape(n, w) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(r), w


def trim(y):
    db, w = rms_db(y); on = np.where(db > -45)[0]
    if not len(on):
        return y
    a = max(0, on[0] * w - int(.04 * SR)); b = min(len(y), (on[-1] + 1) * w + int(.04 * SR))
    return y[a:b]


def split_at(y, frac):
    """the centre of the pause (>= 100 ms under -38 dB) nearest to frac of the take"""
    db, w = rms_db(y, 0.01); quiet = db < -38; best = None; i = 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - i) * 0.01 >= 0.1 and i > 0 and j < len(quiet):
                c = (i + j) / 2 * 0.01
                if best is None or abs(c - frac * len(y) / SR) < abs(best - frac * len(y) / SR):
                    best = c
            i = j
        else:
            i += 1
    return best if best is not None else frac * len(y) / SR


def loudnorm(src, dst, I, tp=-1.5):
    r = subprocess.run([FF, "-hide_banner", "-i", src, "-af", f"loudnorm=I={I}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-af",
                    f"loudnorm=I={I}:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
                    f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample={SR}", "-ar", str(SR), dst], check=True)
    r2 = subprocess.run([FF, "-hide_banner", "-i", dst, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m2 = json.loads(r2[r2.rindex("{"):r2.rindex("}") + 1])
    return {"before": float(m["input_i"]), "after": float(m2["input_i"]), "truePeak": float(m2["input_tp"])}


if __name__ == "__main__":
    VD, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
    S = json.load(open(os.path.join(H, "script_v3.json"), encoding="utf-8"))
    t = 0.0; parts = []; scenes = []; cues = []; blocks = []
    for s in S:
        a = t; t += s.get("lead", .35)
        for k, g in enumerate(s["groups"]):
            if k:
                t += g.get("gap", .32)
            y = trim(load48(os.path.join(VD, f"{s['id']}_{k + 1}.wav"))); d = len(y) / SR
            parts.append((t, y)); blocks.append({"scene": s["id"], "k": k + 1, "a": round(t, 3), "b": round(t + d, 3), "en": g["en"], **({"say": g["say"]} if "say" in g else {})})
            he = g["he"]
            if len(he) == 1:
                cues.append({"scene": s["id"], "a": t, "b": t + d, "he": he[0], "en": g["en"]})
            else:
                c = split_at(y, g["split"][0])
                cues.append({"scene": s["id"], "a": t, "b": t + c, "he": he[0], "en": g["en"] + " [1/2]"})
                cues.append({"scene": s["id"], "a": t + c, "b": t + d, "he": he[1], "en": g["en"] + " [2/2]"})
            t += d
        t += s.get("tail", .55)
        scenes.append({"id": s["id"], "a": round(a, 3), "b": round(t, 3), "pic": s["pic"]})
    DUR = round(t, 2)
    # subtitle display: in 0.08 s before the words, out 0.35 s after (never into the next line)
    for i, c in enumerate(cues):
        c["a"] = round(max(0, c["a"] - .08), 3)
        nxt = cues[i + 1]["a"] - .08 if i + 1 < len(cues) else DUR
        c["b"] = round(min(c["b"] + .35, nxt - .06), 3)
    vo = np.zeros(int(DUR * SR) + SR, np.float32)
    for a, y in parts:
        i = int(round(a * SR)); vo[i:i + len(y)] += y
    vo = vo[:int(DUR * SR)]
    raw = os.path.join(OUT, "vo_raw.wav"); sf.write(raw, np.stack([vo, vo], 1), SR, subtype="PCM_24")
    ln_vo = loudnorm(raw, os.path.join(OUT, "vo.wav"), -16)
    tl = {"duration": DUR, "scenes": scenes, "voice": blocks, "cues": cues, "voLoudness": ln_vo}
    if "--bed" in sys.argv:
        bed, sr = sf.read(sys.argv[sys.argv.index("--bed") + 1], dtype="float32")
        assert sr == SR and len(bed) >= len(vo) - SR, (sr, len(bed), len(vo))
        bed = np.pad(bed, ((0, max(0, len(vo) - len(bed))), (0, 0)))[:len(vo)]
        v, _ = sf.read(os.path.join(OUT, "vo.wav"), dtype="float32"); v = v[:len(vo)]
        # where the voice speaks (pauses under 1.6 s count as speaking), the bed sits 12 dB lower; 0.25 s down, 0.8 s up
        act = np.zeros(len(vo), bool)
        for b in blocks:
            act[int(b["a"] * SR):int(b["b"] * SR)] = True
        idx = np.where(act)[0]; gaps = np.where(np.diff(idx) > 1)[0]
        for g in gaps:
            if (idx[g + 1] - idx[g]) / SR < 1.6:
                act[idx[g]:idx[g + 1]] = True
        target = np.where(act, 10 ** (-12 / 20), 1.0).astype(np.float32)
        gain = np.empty_like(target); g = 1.0; down = 1 / (0.25 * SR); up = 1 / (0.8 * SR)
        look = int(0.2 * SR)   # start going down 0.2 s before the first word
        tgt = np.minimum(target, np.concatenate([target[look:], np.ones(look, np.float32)]))
        for i in range(len(tgt)):
            g = max(tgt[i], g - down) if tgt[i] < g else min(tgt[i], g + up)
            gain[i] = g
        mix = v + bed * gain[:, None]
        rawm = os.path.join(OUT, "mix_raw.wav"); sf.write(rawm, mix, SR, subtype="PCM_24")
        tl["mixLoudness"] = loudnorm(rawm, os.path.join(OUT, "mix.wav"), -16)
        tl["duck"] = "bed -12 dB while the voice speaks (pauses < 1.6 s stay ducked), 0.25 s down with 0.2 s look-ahead, 0.8 s up"
    json.dump(tl, open(os.path.join(OUT, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("duration", DUR, "s;", len(cues), "cues;", json.dumps({k: v for k, v in tl.items() if "oud" in k}))
    for s in scenes:
        print(s["id"], s["a"], s["b"], round(s["b"] - s["a"], 2))
