# -*- coding: utf-8 -*-
"""An independent critic for the post (29.10.2026): Gemini 4 Argon through OpenRouter (key read inside this process only, never
printed) scores the frames and the post text against the checklist drawn from the award-winning and top real-estate posts
(campaign/fb-research-2026-10-29.md), as a jury would, and lists concrete fixes.
  python critic.py <lang> [--model google/gemini-4-argon]   -> out/<lang>/critic.json"""
import base64, io, json, os, re, subprocess, sys, time, urllib.request
import imageio_ffmpeg
H = os.path.dirname(os.path.abspath(__file__)); KP = os.path.dirname(os.path.dirname(H))
KEY_FILE = r"C:\Users\777\Documents\jus-tice-secrets\openrouter\hadmaia-openrouter-key.txt"
args = sys.argv[1:]; LANG = args[0]; MODEL = args[args.index("--model") + 1] if "--model" in args else "google/gemini-4-argon"
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
O = os.path.join(H, "out", LANG); FF = imageio_ffmpeg.get_ffmpeg_exe()
research = io.open(os.path.join(os.path.dirname(H), "fb-research-2026-10-29.md"), encoding="utf-8").read()
m = re.search(r"\n#+[^\n]*checklist[^\n]*\n(.*?)(?=\n#+ |\Z)", research, re.S | re.I)
checklist = m.group(1).strip() if m else research[-6000:]


def img(path, maxw=900):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=85)
    return {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()}}


def frame(video, t):
    p = os.path.join(O, "_f.png")
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", video, "-frames:v", "1", p], check=True)
    x = img(p, 540); os.remove(p); return x


parts = [{"type": "text", "text": (
    "You are a jury member of an international advertising award (real-estate social category) and a Meta creative strategist. "
    "Judge this ORGANIC Facebook post for one real luxury apartment against the checklist below, which was drawn from award-winning and "
    "top-performing real-estate social posts. Be strict and specific; do not invent facts about the property. The images: the 4:5 cover, "
    "six 1:1 cards, and frames of the 9:16 Reel at 0.5 s, 1.5 s, 6 s, 10 s, 15 s, 19 s and the end card. Then the post text, first "
    "comment and the short version.\n\nCHECKLIST:\n" + checklist + "\n\n"
    "Answer in JSON only: {\"scores\": [{\"criterion\": str, \"pass\": bool, \"evidence\": str}], \"overall_10\": number, "
    "\"hook_verdict\": str, \"strongest\": [str], \"fixes\": [{\"what\": str, \"why\": str, \"priority\": \"high|medium|low\"}]}")}]
parts.append({"type": "text", "text": "COVER 4:5:"}); parts.append(img(os.path.join(O, "cover-4x5.jpg")))
for i in range(1, 7):
    parts.append({"type": "text", "text": "CARD %d:" % i}); parts.append(img(os.path.join(O, "card-%d.jpg" % i), 600))
reel = os.path.join(O, "reel-9x16-full.mp4") if os.path.exists(os.path.join(O, "reel-9x16-full.mp4")) else os.path.join(O, "reel-9x16.mp4")
for t in (0.5, 1.5, 6, 10, 15, 19, 22):
    parts.append({"type": "text", "text": "REEL at %.1f s:" % t}); parts.append(frame(reel, t))
for n in ("post", "comment", "short"):
    parts.append({"type": "text", "text": "%s TEXT:\n%s" % (n.upper(), io.open(os.path.join(O, n + ".txt"), encoding="utf-8").read())})
key = open(KEY_FILE, encoding="utf-8").read().strip()
body = {"model": MODEL, "messages": [{"role": "user", "content": parts}], "response_format": {"type": "json_object"}, "temperature": 0.2}
t0 = time.time()
rq = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode("utf-8"),
                            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
r = json.loads(urllib.request.urlopen(rq, timeout=600).read())
txt = r["choices"][0]["message"]["content"]
txt = re.sub(r"^```(?:json)?|```$", "", txt.strip()).strip()
res = json.loads(txt); res["_model"] = MODEL; res["_seconds"] = round(time.time() - t0); res["_cost"] = r.get("usage", {}).get("cost")
io.open(os.path.join(O, "critic.json"), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print(LANG, MODEL, "overall", res.get("overall_10"), "| passed", sum(1 for s in res["scores"] if s["pass"]), "of", len(res["scores"]), "| fixes", len(res.get("fixes", [])), "| cost", res["_cost"])
for f in res.get("fixes", []): print("  -", f.get("priority"), "|", f.get("what"))
