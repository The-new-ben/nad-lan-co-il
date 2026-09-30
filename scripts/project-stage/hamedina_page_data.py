# -*- coding: utf-8 -*-
"""The two Kikar Hamedina posts (P7a), as data: slug, title, content, SEO and meta. One source for deploy369.py (through
gen_deploy369.py), preview_hamedina.py and scripts/seo/project_meta.py.

- The content is docs/research/2026-09-30-kikar-hamedina/post-he.html / post-en.html, stored as ONE line (no whitespace between
  tags), so wpautop never adds a <br> inside a table and the lead stays the first <p> of 100+ characters.
- Meta per the build recipe (feature-inventory.md section 3, step 3) and the fleet's own values (read on the live REST, 30.9):
  city "תל אביב יפו" on both (as dimri-yama-sde-dov-en), project_type "new_build", project_status in Hebrew, geocoded lat/lng =
  the plot centre (area.md 1). No price meta (price_min/price_range): the page shows dated deals, never a "from" price.
- Hebrew meta strings use gershayim/geresh (״ ׳), never ASCII quotes (docs/playbooks/project-factory.md section 4).
- The FAQ schema: the Hebrew page builds its FAQPage from the visible <h2>שאלות נפוצות</h2> (inc/project-stage.php compose);
  the English page carries _nl_faq_schema (base64 of the JSON, inc/schema-meta.php). One FAQPage per page.
"""
import base64, html, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RES = os.path.join(REPO, "docs", "research", "2026-09-30-kikar-hamedina")
LAT, LNG = 32.086758, 34.789776

POSTS = {
    "he": {
        "slug": "hamedina",
        "title": "מגדלי כיכר המדינה, תל אביב",
        "file": "post-he.html",
        "seo_title": "מגדלי כיכר המדינה תל אביב: מחירים, עסקאות, מפה ותלת ממד",
        "seo_desc": "מגדלי כיכר המדינה בתל אביב: 3 מגדלים מסתובבים ו-453 דירות, עסקאות ב-9.58 עד 10.63 מיליון ₪, מועדי האכלוס, הפארק והאגם, והנוף מכל קומה.",
        "faq_h2": "שאלות נפוצות",
        "meta": {
            "lat": LAT, "lng": LNG,
            "developer_name": "חברת בעלי הקרקע בכיכר המדינה",
            "contractor_name": "אלקטרה בנייה ואשטרום",
            "architect_name": "יסקי מור סיון אדריכלים",
            "city": "תל אביב יפו",
            "neighborhood": "הצפון החדש, סביבת כיכר המדינה",
            "address": "ה׳ באייר, כיכר המדינה",
            "gush": "6213",
            "project_type": "new_build",
            "project_status": "בבנייה",
            "num_units": 453, "num_buildings": 3, "num_floors": 40,
            "amenities": "בריכה, חדר כושר, ספא, חדרי טיפולים, אולמות רב תכליתיים, חניון תת-קרקעי, פארק ציבורי ואגם",
            "project_facilities": "בריכה, ספא, חדר כושר, חניון",
            "source": "אשטרום, אלקטרה, גלובס, כלכליסט, מאקו, עיריית תל אביב-יפו",
            "project_mode": "review",
        },
    },
    "en": {
        "slug": "hamedina-en",
        "title": "Kikar Hamedina Towers, Tel Aviv",
        "file": "post-en.html",
        "seo_title": "Kikar Hamedina Towers Tel Aviv: Prices, Deals, Map & 3D",
        "seo_desc": "Kikar Hamedina Towers, Tel Aviv: 3 twisting towers, 453 apartments, deals at ₪9.58M to ₪10.63M, occupancy dates, the park and the view from every floor.",
        "faq_h2": "Frequently asked questions",
        "meta": {
            "lat": LAT, "lng": LNG,
            "developer_name": "the Kikar Hamedina landowners’ company",
            "contractor_name": "Electra Construction and Ashtrom",
            "architect_name": "Yaski Mor Sivan Architects",
            "city": "תל אביב יפו",
            "neighborhood": "הצפון החדש, סביבת כיכר המדינה",
            "address": "He Be’Iyar Street, Kikar Hamedina",
            "gush": "6213",
            "project_type": "new_build",
            "project_status": "בבנייה",
            "num_units": 453, "num_buildings": 3, "num_floors": 40,
            "amenities": "Pool, Gym, Spa, Treatment rooms, Multi-purpose halls, Underground parking, Public park with a pond",
            "source": "Ashtrom, Electra, Globes, Calcalist, Mako, Tel Aviv-Yafo municipality",
            "project_mode": "review",
        },
    },
}
for _l, _p in POSTS.items():
    assert len(_p["seo_title"]) <= 66, (_l, len(_p["seo_title"]))
    assert len(_p["seo_desc"]) <= 155, (_l, len(_p["seo_desc"]))
    for _k, _v in _p["meta"].items():
        assert '"' not in str(_v), ("ASCII quote in meta", _l, _k)


def content(lang):
    raw = io.open(os.path.join(RES, POSTS[lang]["file"]), encoding="utf-8").read()
    return re.sub(r">\s*\n\s*<", "><", raw.strip())


def faq_pairs(lang):
    c = content(lang)
    i = c.find("<h2>" + POSTS[lang]["faq_h2"] + "</h2>")
    seg = c[i:]
    j = seg.find("</section>")
    out = []
    for q, a in re.findall(r"<h3>(.*?)</h3><p>(.*?)</p>", seg[:j]):
        clean = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
        out.append((clean(q), clean(a)))
    return out


def faq_json(lang):
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_pairs(lang)]}
    return json.dumps(ld, ensure_ascii=False, separators=(",", ":"))


def meta(lang):
    """every meta the runner writes, in order (the Yoast fields and, on the English page, the FAQ schema, included)"""
    m = dict(POSTS[lang]["meta"])
    m["_yoast_wpseo_title"] = POSTS[lang]["seo_title"]
    m["_yoast_wpseo_metadesc"] = POSTS[lang]["seo_desc"]
    if lang == "en":
        m["_nl_faq_schema"] = base64.b64encode(faq_json("en").encode("utf-8")).decode("ascii")
    return m


if __name__ == "__main__":
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    for l in POSTS:
        c = content(l)
        print(l, POSTS[l]["slug"], "| content", len(c), "chars | FAQ pairs", len(faq_pairs(l)), "| title", len(POSTS[l]["seo_title"]), "| desc", len(POSTS[l]["seo_desc"]))
        print("   lead:", re.match(r"<p>(.*?)</p>", c).group(1)[:90], "...")
    print(faq_json("en")[:300])
