# -*- coding: utf-8 -*-
"""Hero image for /asbestos/ (HAD-668 R11d), Nano Banana through OpenRouter, the same route as docs/sales/kochav-ph/plan/nano/nano_plan.py:
the key is read inside this process only and never printed or written. No text in the image: the Hebrew and English labels are HTML over it.
  python nano_hero.py <job> [--model google/gemini-nano-banana-2.1]    jobs: cut (cutaway of a 1960s-70s shikun), roof (the roof close-up)"""
import base64, json, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = r"C:\Users\777\Documents\jus-tice-secrets\openrouter\hadmaia-openrouter-key.txt"
args = sys.argv[1:]; MODEL = "google/gemini-nano-banana-2.1"
if "--model" in args: MODEL = args[args.index("--model") + 1]
JOB = args[0] if args else "cut"
COMMON = ("Absolutely NO text, NO letters, NO numbers, NO labels, NO arrows, NO watermark, NO logo, NO people, NO hazmat suits. "
          "Real Israeli architecture of the 1960s and 1970s, accurate materials. Colour world: concrete and fibre-cement greys, white plaster, "
          "a clear Mediterranean sky, no warm sepia or golden-hour cast. Editorial architectural visualisation quality, crisp, high detail, soft daylight.")
PROMPTS = {
    "cut": "A photoreal architectural cutaway illustration of a typical Israeli 'shikun' apartment block from the 1960s-70s: four storeys of flats "
           "standing on concrete pilotis (columns) with an open ground floor, white-grey plaster facade, small balconies with simple metal railings, "
           "seen from the street at a slight three-quarter angle. One corner of the building is cut open like an architectural section so the stairwell, "
           "two flats and the roof are visible inside. On the flat roof: a low roof shed covered with grey CORRUGATED ASBESTOS-CEMENT sheets, solar water "
           "heaters and their tanks. Down the facade: grey asbestos-cement drain and sewage pipes and a gutter. On one balcony: a grey fibre-cement planter box. "
           "On the roof: a grey asbestos-cement chimney flue pipe. In the small front yard: a storage shed with a corrugated grey fibre-cement roof. "
           "The asbestos-cement elements are slightly weathered, grey, with their typical ribbed texture, intact. Wide 16:9 composition with calm space "
           "on the left and right for labels to be added later. " + COMMON,
    "cut2": "A photoreal isometric architectural diorama of a typical Israeli 'shikun' apartment block from the 1960s-70s, standing on a clean pale-grey "
            "ground plate: four storeys of flats on concrete pilotis with an open ground floor, plaster facade, small balconies with metal railings and "
            "roller shutters. The front-right corner is removed by one clean straight vertical architectural section, so the floors, two flats and the "
            "stairwell are seen inside, structurally coherent (every stair flight connects floor to floor, slabs are continuous). On the flat roof: a low "
            "roof shed covered with grey CORRUGATED ASBESTOS-CEMENT sheets, solar water heaters with tanks, and a grey asbestos-cement chimney flue pipe. "
            "Down the facade: grey asbestos-cement drain and sewage pipes. On one balcony: a grey fibre-cement planter box. In the yard: a small storage "
            "shed with a corrugated grey fibre-cement roof. The asbestos-cement parts are weathered grey with their ribbed texture, intact. "
            "Wide 16:9, the building centred with calm empty space on both sides. " + COMMON,
    "roof": "A photoreal close view over a flat Tel Aviv apartment-building roof from the 1970s: a weathered grey CORRUGATED ASBESTOS-CEMENT sheet roof "
            "shed with its typical wave profile and a few lichen spots, beside solar water heaters and white tanks, an old grey asbestos-cement water pipe "
            "running along the parapet, other rooftops of the city in soft focus behind. Wide 16:9. " + COMMON,
}


def run(job):
    with open(KEY_FILE, encoding="utf-8") as f:
        k = f.read().strip()
    body = {"model": MODEL, "modalities": ["image", "text"], "image_config": {"aspect_ratio": "16:9"},
            "messages": [{"role": "user", "content": [{"type": "text", "text": PROMPTS[job]}]}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode("utf-8"),
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json",
                                          "HTTP-Referer": "https://nad-lan.co.il", "X-Title": "nad-lan asbestos hero"})
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
