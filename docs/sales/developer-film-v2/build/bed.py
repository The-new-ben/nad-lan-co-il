# -*- coding: utf-8 -*-
"""The quiet music bed for the developer film v2: synthesised here (no third-party audio), after the house pattern of
docs/sales/kochav-ph/film/music_temp.py, cooler harmony to match the cool picture: Am9 - Fmaj7 - Cmaj9 - G6, 70 bpm,
soft pads, a sparse high bell figure, a room. Ben's own track is his English voice-over, so it is not used under the Hebrew cut.

  python bed.py <seconds> <out.wav>       then loudness-normalised to -20 LUFS (a quiet bed under captions)
"""
import json, subprocess, sys, wave
import numpy as np
FF = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
SR = 48000; T = float(sys.argv[1]); OUT = sys.argv[2]
n = int(SR * T); L = np.zeros(n); R = np.zeros(n)
bpm = 70; beat = 60 / bpm; bar = 4 * beat
f = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [[45, 52, 55, 59, 64, 71], [41, 48, 52, 57, 60, 64], [48, 55, 59, 62, 64, 67], [43, 50, 55, 59, 62, 64]]
rng = np.random.default_rng(11)


def note(t0, dur, hz, amp, kind, pan=0.0):
    i0 = int(t0 * SR); m = min(n - i0, int((dur + 3.0) * SR))
    if m <= 0:
        return
    t = np.arange(m) / SR
    if kind == "bell":
        env = np.exp(-t * 2.2) * (1 - np.exp(-t * 300))
        s = (np.sin(2 * np.pi * hz * t) + 0.25 * np.sin(2 * np.pi * hz * 2.76 * t) * np.exp(-t * 4)) * env
    else:
        env = np.minimum(1, t / 2.4) * np.exp(-np.maximum(0, t - dur) * 1.0)
        s = sum(np.sin(2 * np.pi * hz * d * t + k) for k, d in enumerate((0.996, 1.0, 1.005))) / 3 * env
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i0:i0 + m] += s * amp * l; R[i0:i0 + m] += s * amp * r


t = 0.0; k = 0
while t < T:
    ch = CH[k % 4]
    for m in ch[1:5]:
        note(t, bar, f(m), 0.045, "pad", rng.uniform(-.6, .6))
    note(t, bar, f(ch[0] - 12), 0.06, "pad")
    if t > 5:
        for j, m in enumerate([ch[4], ch[5], ch[3], ch[5]]):
            if rng.random() < 0.8:
                note(t + j * beat + rng.uniform(0, .03), beat, f(m + 12), 0.06 * (0.7 + 0.5 * rng.random()), "bell", rng.uniform(-.7, .7))
    t += bar; k += 1
ir = rng.standard_normal(int(SR * 2.8)) * np.exp(-np.arange(int(SR * 2.8)) / SR * 2.4); ir /= np.abs(ir).sum() / 6


def conv(x):
    N = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]


L = L * 0.55 + conv(L) * 0.45; R = R * 0.55 + conv(R) * 0.45
fade = np.minimum(1, np.arange(n) / (SR * 1.5)) * np.minimum(1, (n - np.arange(n)) / (SR * 4.0))
st = np.stack([L * fade, R * fade], 1); st /= np.abs(st).max() * 1.12
raw = OUT + ".raw.wav"
w = wave.open(raw, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes()); w.close()
r = subprocess.run([FF, "-hide_banner", "-i", raw, "-af", "loudnorm=I=-20:TP=-2:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
mm = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af", "loudnorm=I=-20:TP=-2:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true,aresample=48000"
                % (mm["input_i"], mm["input_tp"], mm["input_lra"], mm["input_thresh"], mm["target_offset"]), "-ar", "48000", OUT], check=True)
print(OUT, T, "s, measured in", mm["input_i"], "LUFS")
