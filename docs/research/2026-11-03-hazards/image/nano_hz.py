# -*- coding: utf-8 -*-
"""Hero image for /asbestos/ (HAD-670 R13c), Nano Banana through OpenRouter, the same route as docs/sales/kochav-ph/plan/nano/nano_plan.py:
the key is read inside this process only and never printed or written. No text in the image: the Hebrew and English labels are HTML over it.
  python nano_hero.py <job> [--model google/gemini-nano-banana-2.1]    jobs: aerial, antenna, survey"""
import base64, json, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = r"C:\Users\777\Documents\jus-tice-secrets\openrouter\hadmaia-openrouter-key.txt"
args = sys.argv[1:]; MODEL = "google/gemini-nano-banana-2.1"
if "--model" in args: MODEL = args[args.index("--model") + 1]
JOB = args[0] if args else "cut"
COMMON = ("Absolutely NO text, NO letters, NO numbers, NO labels, NO arrows, NO icons, NO watermark, NO logo. "
          "Real contemporary Israeli city, accurate: white and light-stone apartment blocks of 4 to 12 floors, solar water heaters on roofs, "
          "palm and ficus trees, wide streets. Clear Mediterranean daylight, no golden-hour or sepia cast, no warm filter. "
          "Calm, factual, editorial real-estate photography quality, crisp, high detail. Not alarming, no smoke plumes, no danger signs.")
PROMPTS = {
    "aerial": "A photoreal aerial view from a drone at about 45 degrees over a typical Israeli city neighbourhood (like Tel Aviv or Holon): "
              "residential apartment blocks with roof gardens and solar heaters, one rooftop carrying small grey cellular antenna panels, a high-voltage "
              "transmission line with lattice pylons crossing the edge of the neighbourhood along a green strip, an electrical substation fenced yard, "
              "a fuel station at a corner of a main road, a light-industrial zone with flat warehouse roofs in the far background. Everything at true scale, "
              "subtle, the way it really looks. Wide 16:9 composition. " + COMMON,
    "antenna": "A photoreal close view of the roof of an Israeli apartment building: three slim grey sector cellular antenna panels on a short mast "
               "with cable trays, beside solar water heaters and a parapet, the city's rooftops behind in soft focus, blue sky. Wide 16:9. " + COMMON,
    "survey": "A photoreal interior of a bright Israeli apartment living room with a balcony door: a professional radiation surveyor, seen from behind "
              "and the side (face not visible), holds a handheld RF and magnetic-field meter with a probe near the window, a tripod-mounted probe in the room. "
              "Ordinary home furniture, calm and practical. Wide 16:9. " + COMMON,
}


def run(job):
    with open(KEY_FILE, encoding="utf-8") as f:
        k = f.read().strip()
    body = {"model": MODEL, "modalities": ["image", "text"], "image_config": {"aspect_ratio": "16:9"},
            "messages": [{"role": "user", "content": [{"type": "text", "text": PROMPTS[job]}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode("utf-8"),
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json",
                                          "HTTP-Referer": "https://nad-lan.co.il", "X-Title": "nad-lan hazards hero"})
    t0 = time.time()
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        print("ERROR", e.code, e.read().decode("utf-8", "replace")[:300]); return
    msg = d["choices"][0]["message"]; imgs = msg.get("images") or []
    if not imgs:
        print("no image returned; text:", (msg.get("content") or "")[:200]); return
    raw = base64.b64decode(imgs[0]["image_url"]["url"].split(",", 1)[1])
    name = "%s-%s-%s.png" % (job, MODEL.split("/")[-1], time.strftime("%H%M%S"))
    open(os.path.join(H, name), "wb").write(raw)
    u = d.get("usage") or {}
    line = "%s | %s | %s | %.0fs | cost %s" % (time.strftime("%Y-%m-%d %H:%M"), MODEL, name, time.time() - t0, u.get("cost"))
    open(os.path.join(H, "LOG.md"), "a", encoding="utf-8").write("- " + line + "\n")
    print("saved", name, len(raw), "bytes |", line)


run(JOB)
