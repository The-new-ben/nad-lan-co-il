# Builds the talking-agent demo: mp3 + Rhubarb lip-sync cues per language, then demo/index.html from demo/template.html.
# python build_demo.py            (needs greet-he.wav / greet-en.wav from voice_local.py and demo/bg.jpg)
import json, os, subprocess, sys, wave
sys.stdout.reconfigure(encoding="utf-8")
FF = r"C:\Users\777\AppData\Local\Programs\Shotcut\ffmpeg.exe"
RH = r"C:\Users\777\Documents\Hadmaya-Visual-Studio\2026-10-28\work\rhubarb-proof\runtime\Rhubarb-Lip-Sync-1.14.0-Windows\rhubarb.exe"
TEXT = json.load(open("lines.json", encoding="utf-8"))
UI = {"he": {"who": "היועצת של נדל״ן", "sub": "דמות ממוחשבת · מכירה כל פרויקט, מחיר ובדיקה", "talk": "דברו איתי", "type": "כתבו שאלה",
             "note": "דמות שנוצרה במחשב. בקרוב: שיחה חיה בקול.", "live": "מדברת", "tap": "הקישו כדי לשמוע"},
      "en": {"who": "NadLan advisor", "sub": "A computer-made character · knows every project, price and check", "talk": "Talk to me", "type": "Type a question",
             "note": "A computer-made character. Live voice chat coming soon.", "live": "Speaking", "tap": "Tap to hear her"}}
data = {"meta": json.load(open("demo/meta.json"))}
for lang in (sys.argv[1:] or ["en"]):
    src = "greet-%s.wav" % lang; wav = "greet-%s-16.wav" % lang
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", wav], check=True)
    with wave.open(wav) as w: dur = w.getnframes() / float(w.getframerate())
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", wav, "-ac", "1", "-ar", "24000", "-b:a", "64k", "demo/greet-%s.mp3" % lang], check=True)
    cues_path = "greet-%s.cues.json" % lang
    cmd = [RH, "-r", "phonetic" if lang == "he" else "pocketSphinx", "-f", "json", "--extendedShapes", "GX", "--machineReadable", "-o", cues_path, wav]
    if lang == "en":
        open("dialog-en.txt", "w", encoding="utf-8").write(TEXT["en"]); cmd[1:1] = ["-d", "dialog-en.txt"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    assert os.path.exists(cues_path), r.stderr[-500:]
    cues = json.load(open(cues_path, encoding="utf-8"))["mouthCues"]
    data[lang] = {"audio": "greet-%s.mp3" % lang, "cues": cues, "dur": round(dur, 2), "text": TEXT[lang], "ui": UI[lang]}
    print(lang, "dur %.2fs, %d cues" % (dur, len(cues)))
html = open("demo/template.html", encoding="utf-8").read().replace("/*DATA*/{}", json.dumps(data, ensure_ascii=False))
open("demo/index.html", "w", encoding="utf-8").write(html)
print("demo/index.html written")
