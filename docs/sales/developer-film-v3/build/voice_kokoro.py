# -*- coding: utf-8 -*-
"""Free local English voice for the developer film v3 (Kokoro-82M v1.0 fp32, CPU, no network during inference).
Pattern: C:/Users/777/Documents/Hadmaya-Visual-Studio/2026-10-28/scripts/run_free_voice_demo.py (same models, same
speech preparation from services/vibevoice/speech_text.py). Run with C:/Users/777/nad-lan/voice-rig/venv/Scripts/python.exe.

  python voice_kokoro.py test  <out_dir>                         the 12-15 s test line in three voices
  python voice_kokoro.py variant [--variant <name>] [--force]   the takes a variant still needs (no flag: main-he): one WAV per
                                 group into the variant's voice.takes folder, with the variant's voice and speed; a take is made
                                 again only when it is missing or its text, voice, speed or phoneme fix changed (receipt.json
                                 records them); --force makes all of them again
"""
import hashlib, json, os, pathlib, sys, time
STUDIO = pathlib.Path("C:/Users/777/Documents/Hadmaya-Visual-Studio/2026-10-28/voice-research")
sys.path.insert(0, str(STUDIO / "lib"))
sys.path.insert(0, "C:/Users/777/Documents/ChatGPT-Work/courtai-judge-pilot-2026-10-16")
os.environ["OMP_NUM_THREADS"] = "4"; os.environ["TOKENIZERS_PARALLELISM"] = "false"
from services.vibevoice.speech_text import prepare_speech
import numpy as np, onnxruntime as ort, soundfile as sf
from kokoro_onnx import Kokoro

TEST = ("Your marketing department runs the campaign. We're the special unit you send in for one mission: "
        "bringing you buyers who are ready to sign. Nad lan dot co dot il, slash marketing.")


def model():
    o = ort.SessionOptions(); o.intra_op_num_threads = 4; o.inter_op_num_threads = 1; o.enable_cpu_mem_arena = False
    s = ort.InferenceSession(str(STUDIO / "models/kokoro-v1.0.onnx"), sess_options=o, providers=["CPUExecutionProvider"])
    return Kokoro.from_session(s, str(STUDIO / "models/voices-v1.0.bin"))


def say(m, text, voice, speed, out, ph=None):
    """ph: [[from, to], ...] phoneme replacements (a pronunciation fix the spelling cannot carry)"""
    spoken = prepare_speech(text, "en"); lang = "en-gb" if voice.startswith("b") else "en-us"
    t = time.monotonic()
    if ph:
        spoken = m.tokenizer.phonemize(spoken, lang)
        for a_, b_ in ph:
            assert a_ in spoken, (a_, spoken); spoken = spoken.replace(a_, b_)
    a, sr = m.create(spoken, voice=voice, speed=speed, lang=lang, is_phonemes=bool(ph))
    el = time.monotonic() - t
    sf.write(out, a, sr, subtype="PCM_16")
    return {"voice": voice, "speed": speed, "text": text, "spoken": spoken, "path": str(out), "sr": sr,
            "seconds": round(len(a) / sr, 3), "genSeconds": round(el, 2), "peak": round(float(np.max(np.abs(a))), 3),
            "sha256": hashlib.sha256(pathlib.Path(out).read_bytes()).hexdigest()}


if __name__ == "__main__":
    if sys.argv[1] == "variant":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import variant as VAR
        VA = VAR.load(); PA = VAR.Paths(VA); vo = VA["voice"]; voice = vo["voice"]; speed = float(vo.get("speed", 1.0))
        assert vo.get("engine", "kokoro") == "kokoro", "this script makes Kokoro takes only"
        out = pathlib.Path(PA.takes); out.mkdir(parents=True, exist_ok=True); rp = out / "receipt.json"
        old = {f"{x['id']}_{x['k']}": x for x in json.load(open(rp))["takes"]} if rp.exists() else {}
        oldv = json.load(open(rp)).get("voice") if rp.exists() else None
        need = []
        for L in VA["scenes"]:
            for k, g in enumerate(L["groups"]):
                key = f"{L['id']}_{k + 1}"; o = old.get(key); text = g.get("say", g["en"]); sp = g.get("speed", speed)
                same = (o is not None and (out / f"{key}.wav").exists() and o.get("text") == text and abs(o.get("speed", sp) - sp) < 1e-9
                        and (oldv or voice) == voice and ("ph" not in o or o.get("ph") == g.get("ph")))
                if "--force" in sys.argv or not same:
                    need.append((L["id"], k + 1, text, sp, g.get("ph")))
        print(VA["name"], ":", len(need), "takes to make,", sum(len(L["groups"]) for L in VA["scenes"]) - len(need), "kept", flush=True)
        if need:
            m = model()
            for sid, k, text, sp, ph in need:
                r = say(m, text, voice, sp, out / f"{sid}_{k}.wav", ph); r["id"] = sid; r["k"] = k
                if ph:
                    r["ph"] = ph
                old[f"{sid}_{k}"] = r; print(sid, k, r["seconds"], flush=True)
            json.dump({"engine": "Kokoro-82M v1.0 fp32 (kokoro-onnx), CPU", "voice": voice, "speed": speed, "takes": list(old.values())},
                      open(rp, "w"), indent=1)
        sys.exit()
    m = model()
    if sys.argv[1] == "test":
        out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); rec = []
        for v in ["am_michael", "bm_george", "af_heart"]:
            r = say(m, TEST, v, 0.95, out / f"kokoro_{v}.wav"); rec.append(r); print(json.dumps(r), flush=True)
        json.dump({"engine": "Kokoro-82M v1.0 fp32 (kokoro-onnx), CPU", "takes": rec}, open(out / "kokoro_receipt.json", "w"), indent=1)
    else:
        lines = json.load(open(sys.argv[2], encoding="utf-8")); out = pathlib.Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
        voice = sys.argv[4]; speed = float(sys.argv[5]) if len(sys.argv) > 5 else 0.95; rec = []
        only = sys.argv[6].split(",") if len(sys.argv) > 6 else None   # regenerate only these takes (e.g. s12_3)
        for L in lines:                       # script_v3.json: scenes, each with groups (one generation per group)
            for k, g in enumerate(L["groups"]):
                fn = out / f"{L['id']}_{k + 1}.wav"
                if only and f"{L['id']}_{k + 1}" not in only:
                    continue
                r = say(m, g.get("say", g["en"]), voice, g.get("speed", speed), fn, g.get("ph"))
                r["id"] = L["id"]; r["k"] = k + 1; rec.append(r); print(r["id"], r["k"], r["seconds"], flush=True)
        rp = out / "receipt.json"
        if only and rp.exists():   # keep the other takes' records
            old = json.load(open(rp)); keep = [x for x in old["takes"] if f"{x['id']}_{x['k']}" not in only]; rec = keep + rec
        json.dump({"engine": "Kokoro-82M v1.0 fp32 (kokoro-onnx), CPU", "voice": voice, "speed": speed, "takes": rec},
                  open(rp, "w"), indent=1)
