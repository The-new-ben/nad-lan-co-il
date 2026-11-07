# Talking agent (Ben 7.11.2026 night): a FICTIONAL woman made by gpt-image (never a real person). Key read inside this process only.
import base64, json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
KEY = open(r"C:\Users\777\Documents\jus-tice-secrets\openai\hadmaia-openai-key.txt", encoding="utf-8").read().strip().splitlines()[0].strip()
MODEL = "gpt-image-2.6-sunburst"
BASE = ("Photorealistic head-and-shoulders portrait of a fictional Israeli woman about 32 years old, a real-estate advisor, strikingly beautiful, "
        "warm and confident, natural blonde hair %s, light olive skin, %s eyes looking straight into the camera, a calm friendly closed-mouth smile, "
        "lips together, subtle natural makeup. Wearing a tailored white silk blouse under a slate-blue blazer. Soft daylight from a large window on the "
        "left, gentle shadow on the right cheek. Background: softly blurred modern Tel Aviv apartment with a sea view, cool slate-blue and pale grey tones "
        "(#2F6F86, #D3DCE2, #F6F8F9), no warm beige, no gold, no brown. Centered, face filling the middle third, shoulders visible, eye level, 85mm lens, "
        "shallow depth of field, natural skin texture, documentary portrait style, no text, no logo, no jewellery.")
VARS = {"a": ("in soft shoulder-length waves", "hazel-green"), "b": ("pulled back loosely with a few strands framing the face", "light brown")}
def one(k):
    body = {"model": MODEL, "prompt": BASE % VARS[k], "size": "1024x1024", "quality": "high", "n": 1}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    t0 = time.time()
    try: r = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e: return k, "HTTP %s %s" % (e.code, e.read()[:300].decode("utf-8", "replace"))
    open("face-%s.png" % k, "wb").write(base64.b64decode(r["data"][0]["b64_json"]))
    return k, {"secs": round(time.time() - t0, 1), "usage": r.get("usage")}
with ThreadPoolExecutor(2) as ex:
    for k, res in ex.map(one, list(VARS)): print(k, json.dumps(res))
