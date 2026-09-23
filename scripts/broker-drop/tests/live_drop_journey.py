# -*- coding: utf-8 -*-
"""A broker's real journey on the test broker: two photos and a message through the public drop link, then the build.
The test broker publishes as drafts (auto 0), so nothing goes live here."""
import io, json, re, sys, time, urllib.request, urllib.error
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
SP = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\638c26e3-6032-438a-9641-ab6fd06c26f5\scratchpad"
TOKEN = re.search(r"/drop/([a-z0-9]{24})/", open(SP + r"\test_drop_url.txt", encoding="utf-8").read()).group(1)
API = "https://nad-lan.co.il/wp-json/nadlan/v1/drop/" + TOKEN
UA = "Mozilla/5.0 (Linux; Android 14) Chrome/128 Mobile"
MSG = ("למכירה: דירת 4 חדרים בפלורנטין, תל אביב. 98 מ\"ר ומרפסת 10 מ\"ר, קומה 3 מתוך 6 עם מעלית. "
       "ממ\"ד, חניה ומחסן. משופצת, מטבח חדש ומיזוג מיני מרכזי. 3.4 מיליון ש\"ח. כניסה בינואר.")


def photo(i):
    im = Image.new("RGB", (1600, 1067), (231, 225, 212))
    d = ImageDraw.Draw(im)
    for y in range(1067):
        c = int(231 - y * 0.06)
        d.line([(0, y), (1600, y)], fill=(c, c - 6, c - 18))
    d.rectangle([80, 80, 1520, 987], outline=(31, 75, 92), width=6)
    d.text((110, 110), "TEST PHOTO %d (nad-lan system check)" % i, fill=(31, 75, 92))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=82)
    return b.getvalue()


def upload(data, name):
    bnd = "----nl%d" % time.time_ns()
    body = (("--%s\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"%s\"\r\nContent-Type: image/jpeg\r\n\r\n" % (bnd, name)).encode() + data + ("\r\n--%s--\r\n" % bnd).encode())
    r = urllib.request.Request(API + "/photo", data=body, method="POST", headers={"User-Agent": UA, "Content-Type": "multipart/form-data; boundary=" + bnd})
    with urllib.request.urlopen(r, timeout=120) as x:
        return json.loads(x.read().decode())


def post(path, body):
    r = urllib.request.Request(API + path, data=json.dumps(body, ensure_ascii=False).encode(), method="POST", headers={"User-Agent": UA, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=200) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "null")


ids = []
for i in (1, 2):
    j = upload(photo(i), "test-%d.jpg" % i)
    ids.append(j["id"])
    print("photo", i, j.get("id"), j.get("w"), j.get("h"))
t0 = time.time()
s, r = post("/submit", {"text": MSG, "photos": ids})
print("submit:", s, round(time.time() - t0, 1), "s", json.dumps(r, ensure_ascii=False)[:300])
if r.get("state") != "ready":
    raise SystemExit(0)
t0 = time.time()
s, r = post("/build/%d" % r["drop"], {})
print("build:", s, round(time.time() - t0, 1), "s", json.dumps(r, ensure_ascii=False)[:900])
json.dump({"photos": ids, "build": r}, open(SP + r"\e2e3_state.json", "w", encoding="utf-8"), ensure_ascii=False)
