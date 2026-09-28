# -*- coding: utf-8 -*-
"""Writes data/duo-tel-aviv.json, DUO's film (ProjectFilm v79 for a second project). Every visible line carries its
source: the live page (read 28.9.2026) and docs/research/2026-09-28-duo/duo-film-facts.md (the developer's reports, its
site, Globes). Left out on purpose, as the research says: the average price per m² (before and after VAT read as a
contradiction in 45 seconds), the 2021 deals, the penthouses' private pools, a height in metres.
The views scene takes DUO's example-apartment cards and facility rooms from the plugin's tour folder, when they exist.
  python scripts/project-video/data/build_duo.py"""
import io, json, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(VID))
TOUR = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "duo", "tour")
IMG = "img/duo-tel-aviv/"
R = "docs/research/2026-09-28-duo/duo-film-facts.md"


def t(text, source):
    return {"text": text, "source": source}


def img(state, fl, fp):
    return {"landscape": {"src": IMG + "stage-%s_1920x1080.jpg" % state, "focus": fl}, "portrait": {"src": IMG + "stage-%s_1080x1920.jpg" % state, "focus": fp}}


scenes = [
    {"id": "title", "type": "title", "dur": 5.0, "render": True, "image": img("hero", [0.5, 0.42], [0.5, 0.36]), "zoom": "in",
     "title": t("DUO תל אביב", "the page H1 'מגדלי דואו תל אביב DUO Tel Aviv' (the Latin brand as the developer writes it)"),
     "line": t("אבן גבירול פינת ארלוזורוב, מתחם סומייל", "the page's line under the H1 (place)"),
     "small": t("יזם: אפריקה ישראל מגורים", "the page's line under the H1 (developer)")},
    {"id": "location", "type": "card", "dur": 4.8, "render": True, "image": img("quarter-own", [0.45, 0.45], [0.42, 0.4]), "zoom": "out",
     "kicker": t("המיקום", "section name"),
     "title": t("בלב תל אביב", R + " line 1 (the company's 2025 report: the Ibn Gabirol, Arlozorov and Ben Saruk junction)"),
     "lines": [t("במפגש אבן גבירול, ארלוזורוב ובן סרוק", R + " line 1"),
               t("חיבור ישיר לקו הירוק מקומת המינוס אחת, לפי החברה", R + " line 8 (the CEO in Globes, 19.4.2026)")],
     "source": t("לפי דוח החברה לשנת 2025 וגלובס, 19.4.2026", R + " lines 1 and 8")},
    {"id": "buildings", "type": "card", "dur": 4.8, "render": True, "image": img("lot", [0.5, 0.45], [0.5, 0.38]), "zoom": "in",
     "kicker": t("הבניינים", "section name"),
     "title": t("2 מגדלים של 54 קומות", R + " line 2; the page's facts ('בניינים: 2 מגדלים של 54 קומות')"),
     "lines": [t("50 קומות מגורים בכל מגדל", R + " line 2; the page's facts"),
               t("668 דירות, מ-2 עד 5 חדרים ופנטהאוזים", R + " line 3 (the 2025 report: 668; the developer's site: 2-5 rooms and penthouses)")],
     "source": t("לפי דוח החברה, היתר הבנייה ואתר היזם", R + " lines 2 and 3; the page's facts (668 by the permit)")},
    {"id": "facilities", "type": "list", "dur": 8.4, "render": True, "image": img("facilities", [0.5, 0.42], [0.5, 0.3]), "zoom": "in",
     "kicker": t("המתקנים בפרויקט", "the page's stage legend chip 'מתקנים בפרויקט'"),
     "items": [t("לובי ראשי בגובה של כ-7 מטרים", R + " line 4 (the developer's site)"),
               t("בריכת אינפיניטי על גג מבנה הלובי", R + " line 5 (the developer's site)"),
               t("מתחם וולנס וחדר כושר", R + " line 6 (the developer's site: the wellness complex with direct entry from the lobby)"),
               t("מסחר בשלוש קומות, כ-13 אלף מ״ר", R + " line 7 (the 2025 report)"),
               t("חניון בחמש קומות מרתף", "the page's facts ('חניה: 5 קומות מרתף, לפי החלטת רשות הרישוי, 9.2025')")],
     "source": t("לפי אתר היזם, דוח החברה ורשות הרישוי. מיקום המתקנים בציור להמחשה.", R + " lines 4-7; the page's stage source line ('מיקום המתקנים להמחשה')")},
    {"id": "sales", "type": "card", "dur": 5.0, "render": False, "panel": "paper",
     "kicker": t("מכירות", "section name"),
     "stats": [{"value": t("372 מתוך 510", R + " line 9 (Q2 2026 report, section 1.3: signed contracts at 30.6.2026)"),
                "caption": t("דירות בשיווק נמכרו עד 6.2026, לפי דוח היזם", R + " line 9")},
               {"value": t("כ-11 מיליון ₪", R + " line 10 (Q2 2026 report, section 3.5: 12 units, average 10,985K ₪ including VAT)"),
                "caption": t("הממוצע לדירה, כולל מע״מ, ב-12 הדירות שנמכרו ב-1-6.2026", R + " line 10")}],
     "source": t("מקור: דוח אפריקה ישראל מגורים לרבעון השני של 2026. מחיר וזמינות מחייבים אישור היזם.", R + " lines 9-10; the page's caveat")},
    {"id": "status", "type": "card", "dur": 4.6, "render": True, "image": img("hero-noon", [0.5, 0.45], [0.5, 0.38]), "zoom": "out",
     "kicker": t("מצב הפרויקט", "section name"),
     "title": t("בבנייה, 87% הושלמו", R + " line 12 (Q2 2026 report: 87%)"),
     "lines": [t("השלמה מתוכננת ב-2027, לפי החברה", R + " line 12; the page's facts ('השלמה מתוכננת ב-2027, לפי דוח החברה')")],
     "source": t("דוח החברה לרבעון השני של 2026; גלובס, 19.4.2026", R + " line 12")},
]

# the views: DUO's example apartment and facility rooms, when the tour folder has them (the cards only; the full files are 360s)
views = []
for f, title, line, src in (("living-25w-card.jpg", "קומה 25", "מהסלון, מבט מערבה לכיוון הים", "file name living-25w: floor 25, living room, west; the page's sector words for 280°"),
                            ("living-25n-card.jpg", "קומה 25", "מהסלון, מבט צפונה", "file name living-25n: floor 25, living room, north"),
                            ("fac-pool-card.jpg", "הבריכה על גג מבנה הלובי", "בין שני המגדלים", "the facility room (illustration); the developer's site: the pool on the lobby building's roof")):
    p = os.path.join(TOUR, f)
    if os.path.exists(p):
        os.makedirs(os.path.join(VID, IMG, "views"), exist_ok=True)
        shutil.copyfile(p, os.path.join(VID, IMG, "views", f))
        views.append({"src": IMG + "views/" + f, "from": "plugins/nadlan-config/assets/project-stage/duo/tour/" + f, "title": t(title, src), "line": t(line, src)})
if len(views) >= 2:
    scenes.append({"id": "views", "type": "views", "dur": 10.5, "render": True, "kicker": t("בתוך הפרויקט", "the page's example apartment and facility rooms"),
                   "items": views, "source": t("דירה לדוגמה ומתקנים: הדמיה להמחשה, החלוקה, הגמרים והנוף משוערים", "the page's tour note ('הדמיית פנים להמחשה בלבד')")})
scenes.append({"id": "outro", "type": "outro", "dur": 6.6, "render": False, "kicker": t("DUO תל אביב", "the page H1"),
               "actions": [t("שיחת וידאו עם נציג", "the page's hero button 'שיחת וידאו עם נציג'") | {"primary": True},
                           t("שאלות? וואטסאפ", "the page's WhatsApp link wa.me/972525101555, in Israeli format") | {"sub": "052-510-1555"}]})

rb = json.load(io.open(os.path.join(HERE, "rainbow-tel-aviv.json"), encoding="utf-8"))
doc = {"slug": "duo-tel-aviv", "page": "https://nad-lan.co.il/projects/duo-tel-aviv/", "checked": "2026-09-28",
       "note": "Every visible line carries its source: the live page (read 28.9.2026) and " + R + ". Stills are ours: the live 3D stage captured by capture.py, and the page's own tour cards. All of them are illustrations.",
       "sources": {"research": R, "page": "https://nad-lan.co.il/projects/duo-tel-aviv/ (read 28.9.2026)"},
       "brand": rb["brand"], "labels": rb["labels"], "scenes": scenes}
io.open(os.path.join(HERE, "duo-tel-aviv.json"), "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
print("ok", len(scenes), "scenes,", len(views), "views,", round(sum(s["dur"] for s in scenes), 1), "s")
