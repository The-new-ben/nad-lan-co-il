# -*- coding: utf-8 -*-
"""One instrumental bed for the Kochav reel from Eleven Music (the owner's ElevenLabs account). The key is read here only,
never printed. Usage: python music_eleven.py <seconds> <out.mp3>"""
import json, sys, urllib.request, urllib.error

KEY_PATH = r"C:\Users\777\Documents\jus-tice-secrets\elevenlabs\elevenlabs-api-key.txt"
secs, out = float(sys.argv[1]), sys.argv[2]
key = open(KEY_PATH, encoding="utf-8-sig").read().strip()
body = {
    "prompt": "Elegant modern luxury real estate promo bed: warm deep house groove at 100 BPM, soft felt piano chords, airy pads, "
              "light percussion, calm and uplifting, sunset over the sea mood, no vocals, a clean musical ending",
    "music_length_ms": int(secs * 1000),
}
req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", data=json.dumps(body).encode(),
                             method="POST", headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
try:
    with urllib.request.urlopen(req, timeout=300) as r:
        data = r.read()
        print("status", r.status, "bytes", len(data), "type", r.headers.get("Content-Type"))
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read()[:300].decode("utf-8", "replace"))
    sys.exit(1)
open(out, "wb").write(data)
print("OUT", out)
