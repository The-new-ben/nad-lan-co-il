# -*- coding: utf-8 -*-
"""A TEMPORARY music bed (until Eleven Music): warm ambient piano and pads, 72 bpm, Dmaj9 - Bm11 - Gmaj7 - A6sus, synthesised
here (no third-party audio). python music_temp.py <seconds> -> audio/music_temp.wav"""
import sys, wave, numpy as np
SR = 48000; T = float(sys.argv[1]) if len(sys.argv) > 1 else 130
n = int(SR * T); L = np.zeros(n); R = np.zeros(n)
bpm = 72; beat = 60 / bpm; bar = 4 * beat
f = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = [[50, 57, 61, 64, 66, 69], [47, 54, 57, 62, 64, 66], [43, 50, 54, 59, 62, 66], [45, 52, 57, 59, 62, 64]]
rng = np.random.default_rng(7)
def note(t0, dur, hz, amp, kind, pan=0.0):
    i0 = int(t0 * SR); m = min(n - i0, int((dur + 2.5) * SR))
    if m <= 0: return
    t = np.arange(m) / SR
    if kind == "piano":
        env = np.exp(-t * 1.6) * (1 - np.exp(-t * 400))
        s = sum(np.sin(2 * np.pi * hz * k * t + rng.random()) * a for k, a in ((1, 1), (2, .35), (3, .12), (4, .06))) * env
    else:
        env = np.minimum(1, t / 1.8) * np.exp(-np.maximum(0, t - dur) * 1.2)
        s = sum(np.sin(2 * np.pi * hz * d * t) for d in (0.997, 1.0, 1.004)) / 3 * env
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i0:i0 + m] += s * amp * l; R[i0:i0 + m] += s * amp * r
t = 0.0; k = 0
while t < T:
    ch = CH[k % 4]
    for m in ch[:4]: note(t, bar, f(m), 0.05, "pad", rng.uniform(-.5, .5))
    note(t, bar, f(ch[0] - 12), 0.07, "pad")
    if t > 6:  # the piano enters after the opening
        for j, m in enumerate([ch[2], ch[4], ch[5], ch[3], ch[4], ch[2], ch[5], ch[4]]):
            note(t + j * beat / 2 + rng.uniform(0, .02), beat, f(m + 12), 0.11 * (0.8 + 0.4 * rng.random()), "piano", rng.uniform(-.6, .6))
    t += bar; k += 1
# a simple room: decaying noise as an impulse response
ir = rng.standard_normal(int(SR * 2.4)) * np.exp(-np.arange(int(SR * 2.4)) / SR * 2.8); ir /= np.abs(ir).sum() / 6
def conv(x):
    N = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:len(x)]
L = L * 0.6 + conv(L) * 0.4; R = R * 0.6 + conv(R) * 0.4
fade = np.minimum(1, np.arange(n) / (SR * 3)) * np.minimum(1, (n - np.arange(n)) / (SR * 5))
st = np.stack([L * fade, R * fade], 1); st /= np.abs(st).max() * 1.12
w = wave.open("audio/music_temp.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes()); w.close()
print("audio/music_temp.wav", T, "s")
