# -*- coding: utf-8 -*-
"""Free local English voice for the developer film v3: Microsoft VibeVoice-Realtime-0.5B (cached in the HF hub cache, CPU,
fp32, sdpa), after C:/Users/777/nad-lan/VibeVoice/demo/realtime_model_inference_from_file.py. No network: HF_HUB_OFFLINE=1.
Run with C:/Users/777/nad-lan/vibevoice-env/Scripts/python.exe.

  python voice_vibevoice.py test  <out_dir> [voice,voice,...]            the test line (same text as voice_kokoro.py)
  python voice_vibevoice.py lines <lines.json> <out_dir> <voice>         every sentence of the film
"""
import copy, glob, hashlib, json, os, pathlib, sys, time
os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
sys.path.insert(0, "C:/Users/777/nad-lan/VibeVoice")
sys.path.insert(0, "C:/Users/777/Documents/ChatGPT-Work/courtai-judge-pilot-2026-10-16")
import torch
from services.vibevoice.speech_text import prepare_speech
from vibevoice.modular.modeling_vibevoice_streaming_inference import VibeVoiceStreamingForConditionalGenerationInference
from vibevoice.processor.vibevoice_streaming_processor import VibeVoiceStreamingProcessor
from transformers.cache_utils import DynamicCache
from transformers.modeling_outputs import BaseModelOutputWithPast

VOICES = "C:/Users/777/nad-lan/VibeVoice/demo/voices/streaming_model"
TEST = ("Your marketing department runs the campaign. We're the special unit you send in for one mission: "
        "bringing you buyers who are ready to sign. Nad lan dot co dot il, slash marketing.")
torch.set_num_threads(8)


def load():
    t = time.monotonic()
    proc = VibeVoiceStreamingProcessor.from_pretrained("microsoft/VibeVoice-Realtime-0.5B")
    m = VibeVoiceStreamingForConditionalGenerationInference.from_pretrained("microsoft/VibeVoice-Realtime-0.5B", torch_dtype=torch.float32,
                                                                          device_map="cpu", attn_implementation="sdpa")
    m.eval(); m.set_ddpm_inference_steps(num_steps=5)
    print("loaded in", round(time.monotonic() - t, 1), "s", flush=True)
    return proc, m


def say(proc, m, text, voice, out):
    spoken = prepare_speech(text, "en")
    with torch.serialization.safe_globals([BaseModelOutputWithPast, DynamicCache]):
        pre = torch.load(os.path.join(VOICES, voice + ".pt"), map_location="cpu", weights_only=True)
    inp = proc.process_input_with_cached_prompt(text=spoken, cached_prompt=pre, padding=True, return_tensors="pt", return_attention_mask=True)
    t = time.monotonic()
    with torch.no_grad():
        o = m.generate(**inp, max_new_tokens=None, cfg_scale=1.5, tokenizer=proc.tokenizer, generation_config={"do_sample": False},
                       verbose=False, all_prefilled_outputs=copy.deepcopy(pre))
    el = time.monotonic() - t
    proc.save_audio(o.speech_outputs[0], output_path=str(out))
    n = o.speech_outputs[0].shape[-1]
    return {"voice": voice, "text": text, "spoken": spoken, "path": str(out), "sr": 24000, "seconds": round(n / 24000, 3),
            "genSeconds": round(el, 1), "sha256": hashlib.sha256(pathlib.Path(out).read_bytes()).hexdigest()}


if __name__ == "__main__":
    proc, m = load()
    if sys.argv[1] == "test":
        out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
        vs = sys.argv[3].split(",") if len(sys.argv) > 3 else ["en-Carter_man", "en-Frank_man", "en-Grace_woman"]
        rec = []
        for v in vs:
            r = say(proc, m, TEST, v, out / f"vibevoice_{v}.wav"); rec.append(r); print(json.dumps(r), flush=True)
            json.dump({"engine": "VibeVoice-Realtime-0.5B, CPU fp32, cfg 1.5, 5 diffusion steps", "takes": rec},
                      open(out / "vibevoice_receipt.json", "w"), indent=1)
    else:
        lines = json.load(open(sys.argv[2], encoding="utf-8")); out = pathlib.Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
        rec = []
        for L in lines:
            for k, s in enumerate(L["en"]):
                r = say(proc, m, s.get("say", s["text"]), sys.argv[4], out / f"{L['id']}_{k + 1}.wav"); r["id"] = L["id"]; r["k"] = k + 1
                rec.append(r); print(r["id"], r["k"], r["seconds"], r["genSeconds"], flush=True)
        json.dump({"engine": "VibeVoice-Realtime-0.5B", "voice": sys.argv[4], "takes": rec}, open(out / "receipt.json", "w"), indent=1)
