# -*- coding: utf-8 -*-
"""Hebrew (and other) narration through the Hadmaya speech gateway: Chatterbox Multilingual + Dicta, the voice the owner
rated 4.7/5 in his blind test of 27.9.2026 (Codex consult, docs/research/2026-09-28-codex-consult-1.md).

The gateway is the Supabase function text-to-speech-openai of the courtai project; its public anon key is read from that
repo's client config, and the owner's access grant from the secrets folder, inside this process only: neither is ever
printed, logged or written anywhere. Each call returns one WAV (24 kHz, mono, 16-bit).
  from tts_chatterbox import synth_wav; synth_wav("שלום", "he", "out.wav")
  python tts_chatterbox.py "טקסט לבדיקה" out.wav [he|en]      (a one-line test)"""
import base64, json, os, re, sys, urllib.request, uuid, wave, io

COURTAI = r"C:\Users\777\Documents\ChatGPT-Work\courtai-voice-science-2026-09-27"
GRANT = r"C:\Users\777\Documents\jus-tice-secrets\hadmaya\access-codes-20260922.json"
URL = "https://mlnwpocuvjnelttvscja.supabase.co/functions/v1/text-to-speech-openai"
_SESSION = "nadlan-film-" + str(uuid.uuid4())


def _auth():
    cfg = open(os.path.join(COURTAI, "src", "integrations", "supabase", "config.ts"), encoding="utf-8").read()
    key = re.search(r"const FALLBACK_ANON_KEY = '([^']+)'", cfg).group(1)
    grant = json.load(open(GRANT, encoding="utf-8"))["pro"]
    return key, grant


def synth_wav(text, lang, path, voice="shimmer", role="judge"):
    key, grant = _auth()
    body = dict(text=text, language=lang, provider="openai", voicePolicy="participant", voice=voice, role=role, sessionId=_SESSION)
    req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "apikey": key, "x-hadmaya-access": grant})
    with urllib.request.urlopen(req, timeout=180) as r:
        res = json.load(r)
    if res.get("provider") != "chatterbox":
        raise RuntimeError("the gateway answered with another provider: %s" % res.get("provider"))
    audio = base64.b64decode(res["audioContent"])
    with wave.open(io.BytesIO(audio), "rb") as w:
        params = (w.getnchannels(), w.getsampwidth(), w.getframerate())
        secs = w.getnframes() / float(w.getframerate())
    open(path, "wb").write(audio)
    return {"secs": round(secs, 3), "format": params}


if __name__ == "__main__":
    t, out = sys.argv[1], sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "he"
    print(json.dumps(synth_wav(t, lang, out)))
