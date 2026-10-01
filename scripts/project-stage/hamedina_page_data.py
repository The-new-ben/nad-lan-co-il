# -*- coding: utf-8 -*-
"""The Kikar Hamedina posts (P7a he/en; P8 fr/ru/ar), as data: slug, title, content, SEO and meta. One source for deploy369.py (through
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
            "source": "kikar_hamedina",  # 1.72.391: a machine key, so the card prints no source line (the owner, 1.10: no source names on the page)
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
            "source": "kikar_hamedina",  # 1.72.391: a machine key, so the card prints no source line (the owner, 1.10: no source names on the page)
            "project_mode": "review",
        },
    },
    # P8 (1.72.370): the French, Russian and Arabic siblings, culturally rewritten (serp-fr.md, serp-ru.md, serp-ar.md). The
    # meta follows the English page's (city, neighbourhood and status in Hebrew: inc/lang-pages.php translates them on the page);
    # developer_name fits the notice's sentence in each language ("le site officiel de %s", "официальным сайтом %s", "لـ%s").
    "fr": {
        "slug": "hamedina-fr",
        "title": "Tours Kikar Hamedina, Tel Aviv",
        "file": "post-fr.html",
        "seo_title": "Tours Kikar Hamedina à Tel Aviv : appartements, prix et 3D",
        "seo_desc": "Tours Kikar Hamedina à Tel Aviv : 3 tours torsadées, 453 appartements, ventes de 9,58 à 10,63 M₪, livraison, le parc et la vue de chaque étage.",
        "faq_h2": "Questions fréquentes",
        "meta": {
            "lat": LAT, "lng": LNG,
            "developer_name": "la société des propriétaires fonciers de Kikar Hamedina",
            "contractor_name": "Electra Construction et Ashtrom",
            "architect_name": "Yaski Mor Sivan Architectes",
            "city": "תל אביב יפו",
            "neighborhood": "הצפון החדש, סביבת כיכר המדינה",
            "address": "Rue He Be’Iyar, Kikar Hamedina",
            "gush": "6213",
            "project_type": "new_build",
            "project_status": "בבנייה",
            "num_units": 453, "num_buildings": 3, "num_floors": 40,
            "amenities": "Piscine, Salle de sport, Spa, Salles de soins, Salles polyvalentes, Parking souterrain, Parc public avec étang",
            "source": "kikar_hamedina",  # 1.72.391: a machine key, so the card prints no source line (the owner, 1.10: no source names on the page)
            "project_mode": "review",
        },
    },
    "ru": {
        "slug": "hamedina-ru",
        "title": "Башни Кикар ха-Медина, Тель-Авив",
        "file": "post-ru.html",
        "seo_title": "Башни Кикар ха-Медина, Тель-Авив: цены, сделки, карта и 3D",
        "seo_desc": "Башни Кикар ха-Медина в Тель-Авиве: 3 закрученные башни, 453 квартиры, сделки от 9,58 до 10,63 млн ₪, сроки заселения, парк и вид с каждого этажа.",
        "faq_h2": "Частые вопросы",
        "meta": {
            "lat": LAT, "lng": LNG,
            "developer_name": "компании владельцев земли на Кикар ха-Медина",
            "contractor_name": "Electra Construction и Ashtrom",
            "architect_name": "Yaski Mor Sivan Architects",
            "city": "תל אביב יפו",
            "neighborhood": "הצפון החדש, סביבת כיכר המדינה",
            "address": "He Be’Iyar, Кикар ха-Медина",
            "gush": "6213",
            "project_type": "new_build",
            "project_status": "בבנייה",
            "num_units": 453, "num_buildings": 3, "num_floors": 40,
            "amenities": "Бассейн, Тренажёрный зал, Спа, Процедурные кабинеты, Многофункциональные залы, Подземная парковка, Общественный парк с прудом",
            "source": "kikar_hamedina",  # 1.72.391: a machine key, so the card prints no source line (the owner, 1.10: no source names on the page)
            "project_mode": "review",
        },
    },
    "ar": {
        "slug": "hamedina-ar",
        # the owner's ruling of 28.9.2026: the Arabic pages' titles in English; the page itself speaks Arabic
        "title": "Kikar Hamedina Towers, Tel Aviv",
        "file": "post-ar.html",
        "seo_title": "Kikar Hamedina Towers, Tel Aviv: Prices, Deals & 3D Map",
        "seo_desc": "أبراج كيكار همدينا في تل أبيب: 3 أبراج ملتفّة و453 شقة، صفقات بين 9.58 و10.63 مليون ₪، مواعيد السكن، الحديقة والإطلالة من كل طابق.",
        "faq_h2": "أسئلة شائعة",
        "meta": {
            "lat": LAT, "lng": LNG,
            "developer_name": "شركة أصحاب الأرض في كيكار همدينا",
            "contractor_name": "Electra Construction وAshtrom",
            "architect_name": "Yaski Mor Sivan للهندسة المعمارية",
            "city": "תל אביב יפו",
            "neighborhood": "הצפון החדש, סביבת כיכר המדינה",
            "address": "He Be’Iyar، كيكار همدينا",
            "gush": "6213",
            "project_type": "new_build",
            "project_status": "בבנייה",
            "num_units": 453, "num_buildings": 3, "num_floors": 40,
            "amenities": "بركة سباحة, نادٍ رياضي, سبا, غرف علاج, قاعات متعددة الاستخدامات, موقف سيارات تحت الأرض, حديقة عامة مع بركة",
            "source": "kikar_hamedina",  # 1.72.391: a machine key, so the card prints no source line (the owner, 1.10: no source names on the page)
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
    if lang != "he":  # the language pages carry their FAQPage as meta (inc/schema-meta.php); the Hebrew page builds its own
        m["_nl_faq_schema"] = base64.b64encode(faq_json(lang).encode("utf-8")).decode("ascii")
    return m


if __name__ == "__main__":
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    for l in POSTS:
        c = content(l)
        print(l, POSTS[l]["slug"], "| content", len(c), "chars | FAQ pairs", len(faq_pairs(l)), "| title", len(POSTS[l]["seo_title"]), "| desc", len(POSTS[l]["seo_desc"]))
        print("   lead:", re.match(r"<p>(.*?)</p>", c).group(1)[:90], "...")
    print(faq_json("en")[:300])
