# -*- coding: utf-8 -*-
"""Nano Banana (Gemini image models) through OpenRouter, on the architect's plan of the Kochav mini penthouse (27.10.2026).
Same route as complete99's scripts/gen_images.py: the key is read from the owner's secrets folder inside this process only and is
never printed or written. The plan image goes in as the input; the model returns a luxury visual that keeps the layout, with no
text and no dimensions (the broker does not want measurable areas shown).
  python nano_plan.py <job> [--model google/gemini-nano-banana-2.1]
  jobs: iso (3D isometric cut-away), top (furnished top-down), both"""
import base64, io, json, os, sys, time, urllib.request
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); PLAN = os.path.join(os.path.dirname(H), "plan-raw-0.jpeg")
KEY_FILE = r"C:\Users\777\Documents\jus-tice-secrets\openrouter\hadmaia-openrouter-key.txt"
args = sys.argv[1:]; MODEL = "google/gemini-nano-banana-2.1"
if "--model" in args: MODEL = args[args.index("--model") + 1]
JOB = args[0] if args else "iso"
COMMON = ("The input is an architect's floor plan of a real 5-room penthouse apartment in Tel Aviv: entrance from the stair core, a large "
          "living room with a sofa group and two armchairs, a dining table, a long kitchen island PARALLEL to the long kitchen wall, three "
          "bedrooms, bathrooms, a laundry, and a large L-shaped terrace with pergolas wrapping two sides, plus a small balcony. "
          "Keep the layout EXACTLY as drawn: the same walls, room shapes, openings, the island orientation and the terrace shape. Do not add, "
          "move or remove any wall, room, column, arch or window. "
          "Finishes like the real apartment: large light-grey stone floor tiles in the living area and kitchen, light oak in the bedrooms, a dark "
          "walnut feature wall behind the TV, white walls, a black kitchen island with leather bar stools, cream sofas, a grey wood-look deck and "
          "frameless glass railings on the terrace, aluminium pergolas. "
          "Absolutely NO text, NO room labels, NO numbers, NO dimension lines, NO scale bar, NO watermark, NO logo. No city, no skyline, no buildings "
          "around: a clean soft off-white studio background. Real-estate marketing quality, photoreal, soft natural daylight, gentle shadows.")
PROMPTS = {
    "iso": "Turn this floor plan into a photorealistic 3D isometric cut-away render of the apartment seen from about 35 degrees above, walls cut at "
           "waist height so every room is visible, furnished as in the plan. " + COMMON,
    "top": "Turn this floor plan into a photorealistic furnished top-down 3D floor plan (orthographic, seen straight from above), with real materials "
           "and soft shadows. " + COMMON,
}


def png_b64(path, maxw=2048):
    im = Image.open(path).convert("RGB"); im.thumbnail((maxw, maxw))
    b = io.BytesIO(); im.save(b, "PNG"); return base64.b64encode(b.getvalue()).decode()


def run(job):
    with open(KEY_FILE, encoding="utf-8") as f:
        k = f.read().strip()
    body = {"model": MODEL, "modalities": ["image", "text"], "image_config": {"aspect_ratio": "4:3"},
            "messages": [{"role": "user", "content": [{"type": "text", "text": PROMPTS[job]},
                                                       {"type": "image_url", "image_url": {"url": "data:image/png;base64," + png_b64(PLAN)}}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode("utf-8"),
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json",
                                          "HTTP-Referer": "https://nad-lan.co.il", "X-Title": "nad-lan plan visual"})
    t0 = time.time()
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        print("ERROR", e.code, e.read().decode("utf-8", "replace")[:300]); return
    msg = d["choices"][0]["message"]; imgs = msg.get("images") or []
    if not imgs:
        print("no image returned; text:", (msg.get("content") or "")[:200]); return
    url = imgs[0]["image_url"]["url"]; raw = base64.b64decode(url.split(",", 1)[1])
    name = "%s-%s.png" % (job, MODEL.split("/")[-1])
    open(os.path.join(H, name), "wb").write(raw)
    u = d.get("usage") or {}
    line = "%s | %s | %s | %.0fs | cost %s | tokens %s" % (time.strftime("%Y-%m-%d %H:%M"), MODEL, name, time.time() - t0, u.get("cost"), u.get("total_tokens"))
    print("saved", name, len(raw), "bytes |", line)
    with open(os.path.join(H, "LOG.md"), "a", encoding="utf-8") as f:
        f.write("- " + line + "\n")


for j in (["iso", "top"] if JOB == "both" else [JOB]):
    run(j)
