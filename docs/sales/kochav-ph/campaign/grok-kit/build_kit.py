# -*- coding: utf-8 -*-
"""Assemble the Grok Bot campaign kit (30.10.2026): docs, ready posts, assets, raw media, research, site data,
frameworks; lint every text; check every link; write ASSETS.csv and MANIFEST.json (sha256)."""
import os, io, sys, json, shutil, hashlib, subprocess, csv, re, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import group_texts as G

KP = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\kochav-ph"
POST = os.path.join(KP, "campaign", "post")
MS = r"C:\Users\777\seo-kit\vendor\marketingskills"
DST = r"C:\Users\777\Documents\grok-bot\nadlan-campaign"
LANGS = ["he", "en", "fr", "ru"]

if os.path.exists(DST):
    shutil.rmtree(DST)
os.makedirs(DST)
J = lambda *p: os.path.join(DST, *p)


def cp(src, *dst):
    d = J(*dst); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(src, d)


def wr(text, *dst):
    d = J(*dst); os.makedirs(os.path.dirname(d), exist_ok=True)
    io.open(d, "w", encoding="utf-8", newline="\n").write(text.rstrip("\n") + "\n")


# 1. docs
D = os.path.join(H, "docs")
for f in ("START-HERE.md", "RULES.md", "FACTS-kochav.md", "CHANNELS.md"):
    cp(os.path.join(D, f), f)
cp(os.path.join(D, "product-marketing.md"), ".agents", "product-marketing.md")

# 2. ready posts (the approved texts as built, plus the new group variants)

for l in LANGS:
    o = os.path.join(POST, "out", l)
    wr(io.open(os.path.join(o, "post.txt"), encoding="utf-8").read(), "posts-ready", l, "page-post.txt")
    com = io.open(os.path.join(o, "comment.txt"), encoding="utf-8").read()
    wr(com, "posts-ready", l, "page-first-comment.txt")
    wr(com.replace("&utm_medium=organic", "&utm_medium=group").replace(
        "utm_campaign=kochav-ph-%s" % l, "utm_campaign=kochav-ph-%s&utm_content={group}" % l),
       "posts-ready", l, "group-first-comment.txt")
    a, b = io.open(os.path.join(o, "group.txt"), encoding="utf-8").read().split("\n\n• • •\n\n")
    wr(a, "posts-ready", l, "group-A.txt"); wr(b, "posts-ready", l, "group-B.txt")
    wr(G.C[l], "posts-ready", l, "group-C-family.txt")
    wr(G.D[l], "posts-ready", l, "group-D-listing.txt")
    wr(G.E[l], "posts-ready", l, "group-E-question.txt")
wr("""# posts-ready
טקסטים מוכנים לפרסום, לכל שפה תיקייה.
- page-post.txt: הפוסט לעמוד NadLan, עם הרילס assets/<lang>/reel-9x16-full.mp4.
- page-first-comment.txt: התגובה הראשונה בעמוד, עם הקישור.
- group-A עד group-E: חמישה נוסחים שונים לקבוצות (מתי משתמשים בכל אחד: CHANNELS.md סעיף 2).
- group-first-comment.txt: התגובה הראשונה בקבוצה. להחליף את {group} בשם הקבוצה באותיות לטיניות, בלי רווחים (למשל tlv-apartments-sale).
אישור: בן, 30.10.2026, "לפרסם כמו שזה". הנוסחים C, D ו-E נכתבו באותו יום מאותן עובדות בדיוק.
""", "posts-ready", "README.md")

# 3. assets (built media) + films
CARD = {"he": ["76 מ״ר של מרפסות, המרפסת הראשית בערב", "סלון ומטבח במרחב אחד", "מטבח עם אי ארוך", "תוכנית הדירה (הדמיה על פי תוכנית האדריכל)", "פארק הירקון ליד הבית", "כרטיס סיום: מיטל, טלפון ורישיון"]}
rows = []


def probe(p):
    """(WxH, seconds): PIL for stills, ffmpeg's own header read for video."""
    if p.endswith(".jpg"):
        from PIL import Image
        return "%dx%d" % Image.open(p).size, ""
    import imageio_ffmpeg
    e = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-i", p], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", e); s = re.search(r"Video: .*?, (\d{2,5})x(\d{2,5})", e)
    return ("%sx%s" % s.groups() if s else ""), ("%.1f" % (int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))) if d else "")


USE = {"reel-9x16-full.mp4": "Reel ראשי בעמוד ובקבוצות (מסך מלא, ההליכה של מיטל בדירה)",
       "reel-9x16.mp4": "Reel חלופי: הסרטון של מיטל בחלון ריבועי, לסטוריז",
       "feed-4x5.mp4": "וידאו לפיד 4:5 כשהרילס לא מתאים",
       "cover-4x5.jpg": "תמונת הפוסט הבודדת, או התמונה הראשונה באלבום"}
for l in LANGS:
    o = os.path.join(POST, "out", l)
    for f in sorted(os.listdir(o)):
        if f.endswith((".jpg", ".mp4")):
            cp(os.path.join(o, f), "assets", l, f)
            size, dur = probe(os.path.join(o, f))
            m = re.match(r"card-(\d)\.jpg", f)
            use = USE.get(f) or ("אלבום, תמונה %s: %s" % (m.group(1), CARD["he"][int(m.group(1)) - 1]) if m else "")
            rows.append(["assets/%s/%s" % (l, f), l, size, dur, use, "הדמיה, מסומנת" if f == "card-4.jpg" else "צילום אמיתי מהדירה"])
FILM = os.path.join(KP, "film", "v3", "web")
for f, use in (("kochav-film-en-v3b.mp4", "סרט מלא בקריינות אנגלית, לעמוד הנכס ולתגובות בלבד"),
               ("kochav-film-en-v3b-he.mp4", "אותו סרט עם כתוביות בעברית, לעמוד הנכס ולתגובות בלבד")):
    cp(os.path.join(FILM, f), "assets", "film", f)
    size, dur = probe(os.path.join(FILM, f))
    rows.append(["assets/film/" + f, "en" if f.endswith("v3b.mp4") else "he", size, dur, use, "מכיל סצנות אווירה מסומנות הדמיה"])

# 4. raw media from Meital (real photos and her own reels, for new posts over the year)
REAL = os.path.join(KP, "tour", "real")
for f in sorted(os.listdir(REAL)):
    if f.endswith(".jpg"):
        cp(os.path.join(REAL, f), "raw-media", "photos", f)
        rows.append(["raw-media/photos/" + f, "", probe(os.path.join(REAL, f))[0], "", "צילום מקור של מיטל, לפוסטים חדשים", "צילום אמיתי מהדירה"])
MEI = os.path.join(KP, "_private-research", "meital-sources")
for f, use in (("ig_DX6qd1ro1NG_01_fresh-2026-10-22.mp4", "הרילס האנכי של מיטל כמו שפורסם (הכותרת שלה צרובה בתמונה). המקור של reel-9x16-full"),
               ("ig_DYRLyC6NVyS_01_fresh-2026-10-22.mp4", "הרילס הריבועי של מיטל (פנים הדירה והמרפסות). המקור של reel-9x16")):
    cp(os.path.join(MEI, f), "raw-media", "meital-reels", f)
    size, dur = probe(os.path.join(MEI, f))
    rows.append(["raw-media/meital-reels/" + f, "", size, dur, use, "וידאו אמיתי מהדירה"])
cp(os.path.join(KP, "plan", "web", "img", "dollhouse.jpg"), "raw-media", "plan-render.jpg")
rows.append(["raw-media/plan-render.jpg", "", probe(os.path.join(KP, "plan", "web", "img", "dollhouse.jpg"))[0], "", "תוכנית הדירה כפי שפורסמה באתר", "הדמיה על פי תוכנית האדריכל: לסמן תמיד"])
with io.open(J("ASSETS.csv"), "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh); w.writerow(["file", "lang", "size_px", "seconds", "use", "media_type"]); w.writerows(rows)

# 5. research
R = os.path.join(KP, "campaign")
for f, n in (("fb-research-2026-10-29.md", "fb-research-2026-10-29.md"), ("channels.md", "channels-abroad.md"),
             ("boards.md", "boards.md"), ("keywords.md", "keywords.md"), ("penthouse-seo.md", "penthouse-seo.md")):
    cp(os.path.join(R, f), "research", n)
for l in LANGS:
    cp(os.path.join(POST, "out", l, "critic.json"), "research", "critic", "critic-%s.json" % l)
cp(os.path.join(POST, "critic-before.json"), "research", "critic", "critic-before.json")
wr("""# research
- fb-research-2026-10-29.md: 12 קמפיינים שזכו בפרסים, 13 מפרסמי נדל״ן מובילים, הנחיות Meta לגדלים ואזורים בטוחים, נתוני חשיפה אורגנית, כללי האתיקה למתווכים, ורשימת הבדיקה (סעיף 6). כל טענה עם מקור ותאריך.
- channels-abroad.md ו-boards.md: ערוצים ולוחות מודעות בחו״ל ובישראל, עם מחירים וחוקים כפי שנקראו ב-21.10.2026.
- keywords.md ו-penthouse-seo.md: מחקר מילות מפתח וחיפושים בגוגל על פנטהאוזים, בעברית ובאנגלית. מסמכים פנימיים: לא לצטט מהם לפוסטים מספרים שלא נמצאים ב-FACTS.
- critic/: ציוני השופט העצמאי (Gemini) מול רשימת הבדיקה של הזוכים, לפני התיקונים ואחריהם, בכל שפה.
""", "research", "README.md")

# 6. site inventory + Search Console
for f in ("site-urls.csv", "gsc-pages-90d.csv", "gsc-queries-90d.csv"):
    cp(os.path.join(H, f), "site", f)
wr("""# site
- site-urls.csv: כל 4,599 העמודים החיים מה-sitemap של nad-lan.co.il, נכון ל-30.10.2026. רק לעמודים האלה מותר לקשר.
- gsc-pages-90d.csv: Search Console, 1.8 עד 28.10.2026, לפי עמוד: קליקים, חשיפות, CTR, מיקום ממוצע.
- gsc-queries-90d.csv: אותה תקופה, לפי חיפוש. מה אנשים באמת מקלידים.
מפות ה-sitemap: nadlan_project (פרויקטים), nadlan_property (נכסים), nadlan_professional (אנשי מקצוע), nadlan_term (מדריכים ומונחים), page (עמודים וכלים), post (כתבות), nadlan_intl (שפות אחרות).
""", "site", "README.md")

# 7. frameworks (MIT)
for s in ("marketing-plan", "social", "community-marketing", "marketing-psychology", "video"):
    shutil.copytree(os.path.join(MS, "skills", s), J("frameworks", s), ignore=shutil.ignore_patterns("evals"))
cp(os.path.join(MS, "LICENSE"), "frameworks", "LICENSE")
wr("""# frameworks
העתק של חמישה skills מתוך https://github.com/coreyhaines31/marketingskills (גרסה 2.11.0, רישיון MIT, הקובץ LICENSE כאן).
הסדר: קודם marketing-plan לתוכנית השנתית, אחר כך social לכל פוסט, community-marketing לקבוצות, video לרילס,
ו-marketing-psychology לניסוח. כל מקום שה-skill מפנה ל-.agents/product-marketing.md, הקובץ נמצא בתיקייה הזאת.
החוקים ב-RULES.md גוברים על כל מה שכתוב כאן.
""", "frameworks", "README.md")

# 8. outbox skeleton
wr("""# outbox
כאן גרוק בוט כותב את מה שהוא מייצר (רשימה מלאה ב-START-HERE.md):
01-plan-12-months.md · 02-calendar.csv · 03-post-bank/ · 04-groups.csv · weekly/ · questions-for-ben.md
""", "outbox", "README.md")
wr("date,time,channel,lang,format,asset,text_file,link_with_utm,status,post_url,notes", "outbox", "02-calendar.csv")
wr("name,url,lang,members,last_post_seen,listings_allowed,brokers_allowed,links_allowed,page_can_post,listing_day,admin_approval,rules_summary,last_kochav_post", "outbox", "04-groups.csv")
for d in ("03-post-bank", "weekly"):
    os.makedirs(J("outbox", d), exist_ok=True)

# 9. lint every text we ship for the bot to post
BAN = ["—", "–", "תלת ממד", "תלת-ממד", "3D", "ממשק", "דמו", "הדגמה", "מנגנון", "אינטראקטיב", "פלטפורמ", "טכנולוג", "סימולצ",
       "אטלס", "Atlas", "אפס ", "interface", "demo", "hotspot", "190", "80 מ", "80 sqm", "80\u00a0m", "80\u00a0м", "למ״ר", "per sqm", "שוכר", "tenant"]
bad = []
for l in LANGS:
    for f in sorted(os.listdir(J("posts-ready", l))):
        t = io.open(J("posts-ready", l, f), encoding="utf-8").read()
        for b in BAN:
            if b in t:
                bad.append((l, f, b))
        if f.startswith(("page-post", "group-")) and not f.startswith("group-first"):
            if "3131540" not in t:
                bad.append((l, f, "licence missing"))
            if not re.search(r"18[,\u00a0 ]000[,\u00a0 ]000", t):
                bad.append((l, f, "price missing"))
print("lint:", "OK" if not bad else bad)

# 10. links: every URL in the ready texts must answer 200
urls = set()
for l in LANGS:
    for f in os.listdir(J("posts-ready", l)):
        urls |= set(re.findall(r"https://nad-lan\.co\.il/[^\s?]+", io.open(J("posts-ready", l, f), encoding="utf-8").read()))
for u in sorted(urls):
    try:
        c = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).status
    except Exception as e:
        c = str(e)
    print("link", c, u)

# 11. manifest
man = {"built": "2026-10-30", "for": "Grok Bot", "by": "Claude (claude-opus-5-5) for Ben", "files": {}}
total = 0
for root, _, files in os.walk(DST):
    for f in files:
        p = os.path.join(root, f); rel = os.path.relpath(p, DST).replace("\\", "/")
        if rel == "MANIFEST.json":
            continue
        man["files"][rel] = {"bytes": os.path.getsize(p), "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest()}
        total += os.path.getsize(p)
man["total_bytes"] = total
json.dump(man, io.open(J("MANIFEST.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("kit:", DST, len(man["files"]), "files,", total // (1024 * 1024), "MB")
