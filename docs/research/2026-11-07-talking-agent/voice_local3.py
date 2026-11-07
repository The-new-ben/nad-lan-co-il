# Talking agent voice v3 (Ben 7.11.2026): LOCAL Chatterbox Multilingual. English: guided by ref-female.wav (our local Kokoro af_heart).
# Hebrew: the model's own built-in female voice + text with niqqud (the clearest Hebrew in our 3.9 tests). Every sentence is checked by
# Whisper (must hold the words, no extra tail) and retried up to 3 times; silences trimmed; joined with short pauses.
import json, sys, time, re
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, librosa, torch, torchaudio as ta, whisper
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
PARTS = {
 "he": [("הַיי, בְּרוּכִים הַבָּאִים לְנַדְלָן.", "היי ברוכים הבאים לנדלן"),
        ("אֲנִי כָּאן כְּדֵי לַעֲזוֹר לָכֶם לִמְצֹא אֶת הַבַּיִת הַנָּכוֹן.", "אני כאן כדי לעזור לכם למצוא את הבית הנכון"),
        ("מְחִירִים, מַשְׁכַּנְתָּא, פְּרוֹיֶקְטִים חֲדָשִׁים, וְכָל הַבְּדִיקוֹת לִפְנֵי שֶׁחוֹתְמִים.", "מחירים משכנתא פרויקטים חדשים וכל הבדיקות לפני שחותמים"),
        ("עַל מָה נְדַבֵּר?", "על מה נדבר")],
 "en": [("Hi, welcome to Nad-Lan.", "hi welcome to"), ("I'm here to help you find the right home in Israel.", "i'm here to help you find the right home in israel"),
        ("Prices, mortgages, new projects, and every check before you sign.", "prices mortgages new projects and every check before you sign"),
        ("What shall we talk about?", "what shall we talk about")]}
def norm(s): return [w for w in re.sub(r"[^\w\s']", " ", s.lower()).split() if w]
t0 = time.time(); m = ChatterboxMultilingualTTS.from_pretrained(device="cpu"); wm = whisper.load_model("small"); print("loaded %.0fs" % (time.time() - t0), flush=True)
default_conds = m.conds
out = {}
for lang in sys.argv[1:] or ["he", "en"]:
    if lang == "en": m.prepare_conditionals("ref-female.wav", exaggeration=0.5)
    else: m.conds = default_conds
    sil = torch.zeros(1, int(m.sr * 0.28)); chunks = []
    for text, plain in PARTS[lang]:
        best = None
        for k in range(3):
            w = m.generate(text, language_id=lang, exaggeration=0.5, cfg_weight=0.5, temperature=0.65)
            y = w.squeeze(0).numpy(); y, _ = librosa.effects.trim(y, top_db=38)
            y16 = librosa.resample(y, orig_sr=m.sr, target_sr=16000)
            heard = wm.transcribe(y16.astype(np.float32), language=lang, fp16=False)["text"]
            tw, hw = norm(plain), norm(heard)
            hit = sum(1 for x in tw if x in hw) / len(tw); extra = max(0, len(hw) - len(tw) - 1)
            score = hit - 0.15 * extra
            print("  %s try%d %.1fs hit %.2f extra %d | %s" % (lang, k + 1, len(y) / m.sr, hit, extra, heard.strip()[:70]), flush=True)
            if best is None or score > best[0]: best = (score, y)
            if hit >= 0.8 and extra == 0: break
        chunks += [torch.from_numpy(best[1]).unsqueeze(0), sil]
    wav = torch.cat(chunks[:-1], dim=1); path = "greet-%s.wav" % lang; ta.save(path, wav, m.sr)
    y, sr = librosa.load(path, sr=16000); f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
    out[lang] = {"secs": round(len(y) / sr, 2), "median_f0": round(float(np.nanmedian(f0)), 1)}
    print(lang, json.dumps(out[lang]), flush=True)
json.dump(out, open("voice-receipt.json", "w"), indent=1)
