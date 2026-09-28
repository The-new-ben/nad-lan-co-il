# -*- coding: utf-8 -*-
"""Writes data/nadlan-developers.json: the film for developers (the owner, 28.9.2026: "a video to present it to developers").
What a buyer meets on a project page today, shown with the live site's own screens (capture_dev.py) and its renders. No
traffic, lead or sales number of ours is claimed: only what the page does. Screens are labelled "צילום מסך מהאתר"; the
renders keep "הדמיה להמחשה". The outro carries the site's own WhatsApp number (the pages' links).
  python scripts/project-video/data/build_developers.py"""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "img/nadlan-developers/fit/"


def t(text, source):
    return {"text": text, "source": source}


def im(name, fl=(0.5, 0.45), fp=(0.5, 0.45)):
    return {"landscape": {"src": IMG + name, "focus": list(fl)}, "portrait": {"src": IMG + name, "focus": list(fp)}}


def v(name, title, line, src):
    return {"src": IMG + name, "from": "capture_dev.py (the live site, 28.9.2026)", "title": t(title, src), "line": t(line, src)}


SCREEN = t("צילום מסך מהאתר", "the screens are the live site's, captured by capture_dev.py")
scenes = [
    {"id": "title", "type": "title", "dur": 5.2, "render": True, "image": im("rb-pool-360.jpg", (0.55, 0.5), (0.62, 0.5)), "zoom": "in",
     "title": t("חדר המכירות של הפרויקט, בעמוד אחד", "what the project pages do (1.72.265-1.72.345)"),
     "line": t("מה קונה רואה היום בעמוד פרויקט בנדל״ן", "the film's subject"),
     "small": t("ריינבו תל אביב ו-DUO תל אביב, 9.2026", "the two pages the screens come from")},
    {"id": "building", "type": "card", "dur": 4.8, "render": True, "image": im("duo-stage-floor.jpg", (0.5, 0.45), (0.45, 0.4)), "zoom": "in",
     "kicker": t("הבניין", "section name"),
     "title": t("הבניין בתלת ממד, על המגרש האמיתי", "the stage (project-stage.php): the lot, the towers and the city around by the Tel Aviv GIS layers"),
     "lines": [t("קומה אחרי קומה, וכל כיוון במילים של המקום", "the stage's floor ring and the sectors' words")],
     "source": t("לפי שכבות עיריית תל אביב-יפו. הדמיה להמחשה.", "the stage's source line on the pages")},
    {"id": "pick", "type": "views", "dur": 11.0, "render": True, "label": SCREEN,
     "kicker": t("הקונה בוחר", "section name"),
     "items": [v("rb-stage-floor.jpg", "קומה 25", "לכיוון הים, דירה לדוגמה על הבניין", "Rainbow's stage, floor 25 west"),
               v("rb-view.jpg", "הנוף והמפה", "מה רואים מהגובה הזה, ומה יש סביב", "the view from the floor and the area map"),
               v("rb-slice.jpg", "חתך הקומה", "התוכנית של הקומה, להמחשה", "FloorSlice v87")],
     "source": t("צילומי מסך מעמוד ריינבו תל אביב, 28.9.2026", "capture_dev.py")},
    {"id": "inside", "type": "views", "dur": 11.0, "render": True,
     "kicker": t("נכנסים פנימה", "section name"),
     "items": [v("rb-inside-warm.jpg", "בתוך הדירה", "דירה לדוגמה ב־360°, בשלושה סגנונות עיצוב", "ApartmentTour, ApartmentStyles v80/v85"),
               v("rb-pool-360.jpg", "הבריכה", "על הגג, והמתקנים ב־360°", "FacilityRooms v83"),
               v("duo-inside.jpg", "גם ב־DUO", "הסלון בקומה 25, בארבעת הכיוונים", "DuoRooms v92 (1.72.353)")],
     "source": t("הדמיות להמחשה, לא לפי תוכנית מכר", "the pages' own caption")},
    {"id": "with-you", "type": "views", "dur": 11.0, "render": False, "label": SCREEN,
     "kicker": t("והקונה ממשיך איתכם", "section name"),
     "items": [v("rb-basket.jpg", "סל הדירה", "הדירה, העיצוב, הצוות והמחיר המלא, לנציג", "BasketOne v86"),
               v("duo-deals.jpg", "עסקאות", "לפי קומה, כל שורה עם המקור שלה", "DUO's ProjectDeals (1.72.342)"),
               v("rb-en-stage.jpg", "בשפת הקונה", "הבמה באנגלית, בצרפתית, ברוסית ובערבית", "StageLanguages v90 (1.72.351)")],
     "source": t("צילומי מסך מהאתר, 28.9.2026", "capture_dev.py")},
    {"id": "outro", "type": "outro", "dur": 6.6, "render": False, "kicker": t("הפרויקט שלכם בנדל״ן", "the film's ask"),
     "actions": [t("שיחה איתנו בוואטסאפ", "the site's WhatsApp link on every page") | {"primary": True},
                 t("nad-lan.co.il", "the site's domain") | {"sub": "052-510-1555"}]},
]
rb = json.load(io.open(os.path.join(HERE, "rainbow-tel-aviv.json"), encoding="utf-8"))
doc = {"slug": "nadlan-developers", "page": "https://nad-lan.co.il/", "checked": "2026-09-28",
       "note": "The film for developers: the live site's own screens and renders; no traffic or sales number of ours is claimed.",
       "sources": {"screens": "scripts/project-video/capture_dev.py, 28.9.2026"},
       "brand": rb["brand"], "labels": rb["labels"], "scenes": scenes}
io.open(os.path.join(HERE, "nadlan-developers.json"), "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
print("ok", len(scenes), "scenes,", round(sum(s["dur"] for s in scenes), 1), "s")
