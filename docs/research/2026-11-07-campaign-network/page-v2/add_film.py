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
script = json.load(io.open(os.path.join(FILMDIR, "variants", "main-he.json"), encoding="utf-8"))["scenes"]  # one file per film version (FILM-STUDIO.md)
transcript = " ".join(g["en"] for s in script for g in s.get("groups", []) if g.get("en"))
assert "ChatGPT" in transcript and "Gemini" in transcript and "Claude" in transcript, "film text has no ChatGPT/Gemini/Claude line yet"

def media(path, mime, title, alt, name):
    slug = os.path.splitext(name)[0]
    s, r, _ = req("GET", "/wp-json/wp/v2/media?slug=%s&_fields=id,source_url,slug" % slug); assert s == 200, (s, r)
    hit = [x for x in r if x["source_url"].rsplit("/", 1)[-1] == name]
    if hit:
        if GO: req("POST", "/wp-json/wp/v2/media/%d" % hit[0]["id"], {"title": title, "alt_text": alt})  # keep the library title neutral
        return hit[0]["id"], hit[0]["source_url"], "exists"
    if not GO: return None, "(would upload %s, %d bytes)" % (name, os.path.getsize(path)), "plan"
    body = open(path, "rb").read()
    rq = urllib.request.Request(ns["BASE"] + "/wp-json/wp/v2/media", data=body, method="POST")
    rq.add_header("Authorization", ns["AUTH"]); rq.add_header("User-Agent", ns["UA"]); rq.add_header("Content-Type", mime)
    rq.add_header("Content-Disposition", 'attachment; filename="%s"' % name)
    with urllib.request.urlopen(rq, timeout=600) as resp: up = json.loads(resp.read().decode())
    s2, _, _ = req("POST", "/wp-json/wp/v2/media/%d" % up["id"], {"title": title, "alt_text": alt}); assert s2 in (200, 201), s2
    return up["id"], up["source_url"], "uploaded"

# Ben 7.11 night: public text never says who the film is for (no "for CEOs"); it is "a short video that describes our capabilities".
LANG = "en" if "--en" in sys.argv else "he"
TITLE_HE = "שיווק פרויקט נדל״ן לקונים בארץ ובחו״ל: מה אנחנו עושים, בסרטון"
CFG = {
  "he": {"page": 8827, "local": "page_he.html", "anchor": '<a class="nlu1-btn" href="#planner">בנו קמפיין לקונים בחו״ל</a></div>', "title": TITLE_HE,
         "cap": "בסרטון: כך קונה מהארץ ומחו״ל מוצא את הפרויקט, נוחת בתוכו, בוחר קומה, נוף ודירה, ומגיע לצוות המכירות כשהוא כבר יודע מה הוא קונה.",
         "desc": "איך קונה בארץ ובחו״ל מוצא פרויקט חדש בחיפוש בשפה שלו, בגוגל ובתשובות של ChatGPT, Gemini ו־Claude, נוחת בעמוד הפרויקט, "
                 "בוחר קומה, נוף ודירה, קובע שיחת וידאו עם צוות המכירות ומלווה עד החוזה.", "embed": "https://nad-lan.co.il/marketing/#film"},
  "en": {"page": 8829, "local": "page_en.html", "anchor": '<a class="nlu1-btn" href="#planner">Plan a campaign for buyers abroad</a></div>',
         "title": "Marketing a new real estate project to buyers in Israel and abroad: what we do, on video",
         "cap": "In this video: how a buyer in Israel or abroad finds the project, lands inside it, picks a floor, a view and an apartment, and reaches the sales team already knowing what he is buying.",
         "desc": "How a buyer in Israel or abroad finds a new project when searching in his own language, on Google and inside the answers of ChatGPT, "
                 "Gemini and Claude, lands on the project page, picks a floor, a view and an apartment, books a video call with the sales team and is "
                 "accompanied to the contract.", "embed": "https://nad-lan.co.il/en/marketing/#film"}}[LANG]
fid, furl, fst = media(FILM, "video/mp4", TITLE_HE, "", "developer-film-v3-he.mp4")
pid, purl, pst = media(POSTER, "image/jpeg", TITLE_HE + " (תמונת פתיחה)", "קונה בוחר קומה ודירה בפרויקט חדש בתל אביב", "developer-film-v3-poster.jpg")
print("[media] film", fst, fid, furl); print("[media] poster", pst, pid, purl)
TITLE = CFG["title"]; CAP = CFG["cap"]
for w in ("מנכ", "CEO", "chief executive", "מחלקת השיווק", "marketing department", "קריינות", "כתוביות", "voice-over", "subtitles"): assert w.lower() not in (TITLE + CAP + CFG["desc"]).lower(), ("audience leak", w)
CSS = (".nlu1-film{margin:4px 0 22px;max-width:960px}.nlu1-film video{display:block;width:100%;height:auto;aspect-ratio:16/9;"
       "background:#12202A;border-radius:6px}.nlu1-film figcaption{font-size:14px;line-height:1.6;color:#3E4C58;margin-top:8px;max-width:74ch}")
LD = {"@context": "https://schema.org", "@type": "VideoObject", "name": TITLE, "description": CFG["desc"],
      "thumbnailUrl": [purl], "uploadDate": "2026-11-07T20:00:00+02:00", "duration": dur_iso, "contentUrl": furl, "inLanguage": "en",
      "transcript": transcript, "embedUrl": CFG["embed"]}
BLOCK = ('<figure class="nlu1-film" id="film"><video controls playsinline preload="none" poster="%s" width="1280" height="720" '
         'aria-label="%s"><source src="%s" type="video/mp4"></video><figcaption>%s</figcaption></figure>'
         '<script type="application/ld+json">%s</script>') % (purl, TITLE, furl, CAP, json.dumps(LD, ensure_ascii=False))
vis = re.sub(r"<[^>]+>", " ", CAP + TITLE + CFG["desc"]); assert not re.search(r"[–—]", vis), "long dash"

s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,modified" % CFG["page"]); assert s == 200, s
raw = r["content"]["raw"]
if 'class="nlu1-film"' in raw:   # already there: swap the old block (wording fix), nothing else
    a = raw.index('<figure class="nlu1-film"'); b = raw.index("</script>", a) + len("</script>")
    assert raw[a:b].count("application/ld+json") == 1 and raw.count('class="nlu1-film"') == 1
    new = raw[:a] + BLOCK + raw[b:]; mode = "swap"
else:
    assert raw.count(CFG["anchor"]) == 1 and raw.count("</style>") >= 1, ("anchor", raw.count(CFG["anchor"]))
    k = raw.index(CFG["anchor"]) + len(CFG["anchor"]); st = raw.index("</style>")
    new = raw[:st] + CSS + raw[st:k] + "\n" + BLOCK + raw[k:]; mode = "insert"
local = io.open(os.path.join(H, CFG["local"]), encoding="utf-8").read()
print("[plan] %s page %d %s: live %d chars (modified %s) -> %d; live == local %s: %s" % (LANG, CFG["page"], mode, len(raw), r["modified"], len(new), CFG["local"], raw.strip() == local.strip()))
print("[plan] duration %s, transcript %d words\n  title: %s\n  caption: %s" % (dur_iso, len(transcript.split()), TITLE, CAP))
if not GO or fid is None: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s-pre-film-%s.html" % (CFG["page"], time.strftime("%Y%m%d-%H%M%S"), mode)), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % CFG["page"], {"content": new}); assert s2 in (200, 201), s2
io.open(os.path.join(H, CFG["local"]), "w", encoding="utf-8", newline="").write(new)   # repo copy = live
time.sleep(6)
live = urllib.request.urlopen(urllib.request.Request(r["link"] + "?f=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print({"video": live.count('class="nlu1-film"'), "src": furl in live, "VideoObject": '"VideoObject"' in live, "FAQPage": '"FAQPage"' in live,
       "nlcamp": 'data-nli="nlcamp"' in live, "nlbudget": 'data-nli="nlbudget"' in live, "raw shortcode": "[nadlan_tool" in live,
       "h1": len(re.findall(r"<h1[\s>]", live)), "fatal": "Fatal error" in live, "CEO words": bool(re.search(r"מנכ״ל|מנכ\"ל|CEO", live)),
       "film after lead": live.find('class="nlu1-lead"') < live.find('class="nlu1-cta"') < live.find('class="nlu1-film"') < live.find('data-nli="nlbudget"')})
