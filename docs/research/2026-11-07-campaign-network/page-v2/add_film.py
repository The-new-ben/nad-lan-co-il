# HAD-678 (Ben 7.11.2026 evening): put developer film v3 on /marketing/ (page 8827), high on the page but AFTER the answer paragraph and the CTAs
# (H1 -> answer paragraph with the head keyword -> CTAs -> film -> tools). Additive: live raw content + one CSS rule set + one figure + VideoObject JSON-LD.
# Usage: python add_film.py            (plan only, no writes)
#        python add_film.py --go       (upload media if missing, back up the live page, update it, verify the public HTML)
import io, json, os, re, subprocess, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "film"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
FILMDIR = os.path.join(REPO, "docs", "sales", "developer-film-v3")
FILM = os.path.join(FILMDIR, "he-web-16x9.mp4"); POSTER = os.path.join(FILMDIR, "poster-16x9.jpg")
FFMPEG = r"C:\Users\777\AppData\Local\Programs\Python\Python311\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"
for f, cap in ((FILM, 15_500_000), (POSTER, 210_000)):
    assert os.path.exists(f), ("missing", f); assert os.path.getsize(f) <= cap, ("too big", f, os.path.getsize(f))
info = subprocess.run([FFMPEG, "-hide_banner", "-i", FILM], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
m = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", info); assert m, info[:300]
secs = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + (1 if int(m.group(4)) >= 50 else 0)
assert re.search(r"1280x720", info), "not 1280x720"
dur_iso = "PT%dM%dS" % (secs // 60, secs % 60); dur_he = "%d:%02d" % (secs // 60, secs % 60)
script = json.load(io.open(os.path.join(FILMDIR, "build", "script_v3.json"), encoding="utf-8"))
transcript = " ".join(g["en"] for s in script for g in s.get("groups", []) if g.get("en"))
assert "ChatGPT" in transcript and "Gemini" in transcript and "Claude" in transcript, "film text has no ChatGPT/Gemini/Claude line yet"

def media(path, mime, title, alt, name):
    slug = os.path.splitext(name)[0]
    s, r, _ = req("GET", "/wp-json/wp/v2/media?search=%s&per_page=20&_fields=id,source_url,slug,media_details" % slug); assert s == 200, (s, r)
    hit = [x for x in r if x["source_url"].rsplit("/", 1)[-1] == name]
    if hit: return hit[0]["id"], hit[0]["source_url"], "exists"
    if not GO: return None, "(would upload %s, %d bytes)" % (name, os.path.getsize(path)), "plan"
    body = open(path, "rb").read()
    rq = urllib.request.Request(ns["BASE"] + "/wp-json/wp/v2/media", data=body, method="POST")
    rq.add_header("Authorization", ns["AUTH"]); rq.add_header("User-Agent", ns["UA"]); rq.add_header("Content-Type", mime)
    rq.add_header("Content-Disposition", 'attachment; filename="%s"' % name)
    with urllib.request.urlopen(rq, timeout=600) as resp: up = json.loads(resp.read().decode())
    s2, _, _ = req("POST", "/wp-json/wp/v2/media/%d" % up["id"], {"title": title, "alt_text": alt}); assert s2 in (200, 201), s2
    return up["id"], up["source_url"], "uploaded"

TITLE = "שיווק פרויקט נדל״ן לקונים בארץ ובחו״ל: סרט למנכ״לים של חברות בנייה ויזמות"
fid, furl, fst = media(FILM, "video/mp4", TITLE, "", "developer-film-v3-he.mp4")
pid, purl, pst = media(POSTER, "image/jpeg", TITLE + " (תמונת פתיחה)", "קונה בוחר קומה ודירה בפרויקט חדש בתל אביב", "developer-film-v3-poster.jpg")
print("[media] film", fst, fid, furl); print("[media] poster", pst, pid, purl)

CAP = ("סרט קצר למנכ״לים של חברות בנייה ויזמות: קונה מחו״ל או מהארץ מוצא את הפרויקט שלכם, נוחת בתוכו, בוחר קומה ודירה, "
       "ומגיע אליכם מוכן לשיחה. קריינות באנגלית, כתוביות בעברית, %s דקות." % dur_he)
CSS = (".nlu1-film{margin:4px 0 22px;max-width:960px}.nlu1-film video{display:block;width:100%;height:auto;aspect-ratio:16/9;"
       "background:#12202A;border-radius:6px}.nlu1-film figcaption{font-size:14px;line-height:1.6;color:#3E4C58;margin-top:8px;max-width:74ch}")
LD = {"@context": "https://schema.org", "@type": "VideoObject", "name": TITLE,
      "description": "איך קונה בארץ ובחו״ל מוצא פרויקט חדש בחיפוש בשפה שלו, בגוגל ובתשובות של ChatGPT, Gemini ו־Claude, נוחת בעמוד הפרויקט, "
                     "בוחר קומה, נוף ודירה, קובע שיחת וידאו עם צוות המכירות ומלווה עד החוזה.",
      "thumbnailUrl": [purl], "uploadDate": "2026-11-07T20:00:00+02:00", "duration": dur_iso, "contentUrl": furl, "inLanguage": "en",
      "transcript": transcript, "embedUrl": "https://nad-lan.co.il/marketing/#film"}
BLOCK = ('<figure class="nlu1-film" id="film"><video controls playsinline preload="none" poster="%s" width="1280" height="720" '
         'aria-label="%s"><source src="%s" type="video/mp4"></video><figcaption>%s</figcaption></figure>'
         '<script type="application/ld+json">%s</script>') % (purl, TITLE, furl, CAP, json.dumps(LD, ensure_ascii=False))
vis = re.sub(r"<[^>]+>", " ", CAP + TITLE); assert not re.search(r"[–—]", vis), "long dash"

s, r, _ = req("GET", "/wp-json/wp/v2/pages/8827?context=edit&_fields=content,link,modified"); assert s == 200, s
raw = r["content"]["raw"]
ANCH = '<a class="nlu1-btn" href="#planner">בנו קמפיין לקונים בחו״ל</a></div>'
assert "nlu1-film" not in raw, "film already on the page"
assert raw.count(ANCH) == 1 and raw.count("</style>") >= 1, ("anchor", raw.count(ANCH))
k = raw.index(ANCH) + len(ANCH); st = raw.index("</style>")
new = raw[:st] + CSS + raw[st:k] + "\n" + BLOCK + raw[k:]
local = io.open(os.path.join(H, "page_he.html"), encoding="utf-8").read()
print("[plan] live %d chars (modified %s) -> %d; live == local page_he.html: %s" % (len(raw), r["modified"], len(new), raw.strip() == local.strip()))
print("[plan] duration %s, transcript %d words, caption: %s" % (dur_iso, len(transcript.split()), CAP))
if not GO or fid is None: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-8827-%s-pre-film.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/8827", {"content": new}); assert s2 in (200, 201), s2
io.open(os.path.join(H, "page_he_live.html"), "w", encoding="utf-8", newline="").write(new)
time.sleep(6)
live = urllib.request.urlopen(urllib.request.Request(r["link"] + "?f=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print({"video": live.count('class="nlu1-film"'), "src": furl in live, "VideoObject": '"VideoObject"' in live, "FAQPage": '"FAQPage"' in live,
       "nlcamp": 'data-nli="nlcamp"' in live, "nlbudget": 'data-nli="nlbudget"' in live, "raw shortcode": "[nadlan_tool" in live,
       "h1": len(re.findall(r"<h1[\s>]", live)), "fatal": "Fatal error" in live, "film after lead": live.find('class="nlu1-lead"') < live.find('class="nlu1-cta"') < live.find('class="nlu1-film"') < live.find('data-nli="nlbudget"')})
