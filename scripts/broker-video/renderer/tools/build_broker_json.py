"""Build data/<slug>.json for the broker video composer from PUBLIC nad-lan.co.il pages.

Read-only: it only GETs public pages, the public REST API and public images.

  python tools/build_broker_json.py --slug meital-katzir

Sources
  /professionals/<slug>/          name, brand, role, licence, phone, portrait (featured image)
  /brokers/<slug>/                the broker's listing links, in the broker's own order
  /wp-json/wp/v2/nadlan_property  meta (price, listing_type, nl_broker_id) matched by link
  each listing page               title, kicker (deal + area), facts table, cover + gallery photos

Rules (never invent, omit what is unknown)
  price  : shown only when the REST price is > 0 AND that exact number is printed in the
           listing's lead paragraph; rent gets "לחודש". Otherwise null.
  rooms  : facts "חדרים" (leading number only); villas without rooms fall back to "סוויטות".
  size   : facts "שטח בנוי" / "שטח" / "שטח לפי ארנונה", printed as the page prints it (keeps "כ-").
  floor  : facts "קומה"; omitted when the page itself is ambiguous (contains "או");
           villas without a floor fall back to "מפלסים".
  photos : the page's cover photo + gallery, largest size the site serves.

An optional art-direction file data/<slug>.art.json (hand-made) chooses and orders photos,
sets focus points / clean crops per orientation, and may override any listing field.
"""
import argparse, html, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://nad-lan.co.il"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0 Safari/537.36"


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "he-IL,he;q=0.9"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def clean(x):
    x = re.sub(r"<[^>]+>", "", x)
    x = html.unescape(x)
    return re.sub(r"\s+", " ", x).strip()


def strip_code(s):
    return re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", s, flags=re.S)


def largest(img_tag):
    src = re.search(r'\ssrc="([^"]+)"', img_tag).group(1)
    w = re.search(r'\swidth="(\d+)"', img_tag)
    h = re.search(r'\sheight="(\d+)"', img_tag)
    best_w, best = (int(w.group(1)) if w else 0), src
    ss = re.search(r'srcset="([^"]+)"', img_tag)
    if ss:
        for part in ss.group(1).split(","):
            m = re.match(r"(\S+)\s+(\d+)w", part.strip())
            if m and int(m.group(2)) > best_w:
                best_w, best = int(m.group(2)), m.group(1)
    return best


def first_number(s):
    m = re.search(r"\d+(?:\.\d+)?", s)
    return m.group(0) if m else None


def parse_broker_card(slug):
    raw = fetch(f"{SITE}/professionals/{slug}/")
    s = strip_code(raw)
    h1 = clean(re.search(r"<h1[^>]*>(.*?)</h1>", s, flags=re.S).group(1))
    name, _, brand = h1.partition(" · ")
    txt = clean(s)
    lic = re.search(r"רישיון תיווך\s*\|?\s*(\d{5,8})", txt) or re.search(r"רישיון[^\d]{0,20}(\d{5,8})", txt)
    # phone: the number printed on the broker's own site (visible button), else the card's JSON-LD
    site = fetch(f"{SITE}/brokers/{slug}/")
    phone = re.search(r'class="nlb-num">\s*(0\d{1,2}-?\d{7})\s*<', site) \
        or re.search(r'"telephone"\s*:\s*"(0\d{1,2}-?\d{7})"', raw) \
        or re.search(r"(0\d{1,2}-\d{7})", txt)
    role = "מתווכת" if "מתווכת" in txt else ("מתווך" if "מתווך" in txt else "")
    img = re.search(r"<img[^>]+wp-post-image[^>]*>", s)
    portrait = largest(img.group(0)) if img else None
    return {"name": name.strip(), "brand": brand.strip(), "role": role,
            "licence": lic.group(1) if lic else None, "phone": phone.group(1) if phone else None,
            "portrait_url": portrait}


def listing_links(slug):
    s = fetch(f"{SITE}/brokers/{slug}/")
    out = []
    for l in re.findall(r'href="(https://nad-lan\.co\.il/properties/[^"#?]+)"', s):
        if l not in out:
            out.append(l)
    return out


def rest_meta():
    data = json.loads(fetch(f"{SITE}/wp-json/wp/v2/nadlan_property?per_page=100&_fields=id,link,title,meta"))
    return {p["link"]: p for p in data}


def parse_listing(url):
    s = strip_code(fetch(url))
    art = re.search(r'<article class="nlx".*?</article>', s, flags=re.S)
    a = art.group(0) if art else s
    def cls(c):
        m = re.search(r'class="%s"[^>]*>(.*?)</(?:p|h2|span|div)>' % c, a, flags=re.S)
        return clean(m.group(1)) if m else None
    facts = {}
    dl = re.search(r'<dl class="nlx-facts">(.*?)</dl>', a, flags=re.S)
    if dl:
        for dt, dd in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", dl.group(1), flags=re.S):
            facts[clean(dt)] = clean(dd)
    photos = []
    cov = re.search(r'<figure class="nlx-plate nlx-plate--photo"[^>]*>\s*(<img[^>]+>)', a, flags=re.S)
    if cov:
        photos.append(largest(cov.group(1)))
    gal = re.search(r'<div class="nlx-gallery">(.*?)</div>', a, flags=re.S)
    if gal:
        for im in re.findall(r"<img[^>]+>", gal.group(1)):
            u = largest(im)
            if u not in photos:
                photos.append(u)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, flags=re.S)
    return {"title": cls("nlx-title") or (clean(h1.group(1)) if h1 else ""), "kicker": cls("nlx-kicker") or "",
            "dek": cls("nlx-dek") or "", "facts": facts, "photos": photos}


def facts_line(f):
    out = []
    rooms = f.get("חדרים")
    if rooms and first_number(rooms):
        out.append(f"{first_number(rooms)} חדרים")
    elif f.get("סוויטות") and first_number(f["סוויטות"]):
        out.append(f"{first_number(f['סוויטות'])} סוויטות")
    for k in ("שטח בנוי", "שטח", "שטח לפי ארנונה", "שטח דירה"):
        if f.get(k) and "מ״ר" in f[k]:
            out.append(f[k].replace("כ- ", "כ-"))
            break
    floor = f.get("קומה")
    if floor and " או " not in f" {floor} ":
        out.append(f"קומה {floor}")
    elif not floor and f.get("מפלסים") and first_number(f["מפלסים"]):
        out.append(f"{first_number(f['מפלסים'])} מפלסים")
    return out


def price_text(meta, dek):
    p = meta.get("price")
    try:
        p = int(float(p))
    except (TypeError, ValueError):
        return None
    if p <= 0:
        return None
    formatted = f"{p:,}"
    if formatted not in dek:          # published on the page? if not, never show it
        return None
    return f"{formatted} ₪" + (" לחודש" if meta.get("listing_type") == "rent" else "")


def download(url, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    fn = os.path.join(dest_dir, url.split("/")[-1])
    if not (os.path.exists(fn) and os.path.getsize(fn) > 0):
        with open(fn, "wb") as f:
            f.write(fetch(url, binary=True))
    return fn


def image_size(path):
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--max-photos", type=int, default=5)
    args = ap.parse_args()
    slug = args.slug
    img_dir = os.path.join(ROOT, "img", slug)
    art_path = os.path.join(ROOT, "data", f"{slug}.art.json")
    art = json.load(open(art_path, encoding="utf-8")) if os.path.exists(art_path) else {}

    card = parse_broker_card(slug)
    portrait_file = download(card["portrait_url"], img_dir) if card["portrait_url"] else None
    meta_by_link = rest_meta()
    listings = []
    for link in listing_links(slug):
        page = parse_listing(link)
        rec = meta_by_link.get(link, {})
        meta = rec.get("meta") or {}
        key = meta.get("nl_card_key") or str(rec.get("id", ""))
        kicker_parts = [p.strip() for p in page["kicker"].split(" · ") if p.strip()]
        deal = {"sale": "למכירה", "rent": "להשכרה"}.get(meta.get("listing_type"), "")
        area = kicker_parts[-1] if kicker_parts else (meta.get("neighborhood") or "")
        a = art.get("listings", {}).get(key, {})
        chosen = a.get("photos")  # [{"file": "...", "focus": [x,y], "crop": {...}}] in order
        if chosen:
            by_name = {u.split("/")[-1]: u for u in page["photos"]}
            photo_specs = [dict(p, url=by_name[p["file"]]) for p in chosen]
        else:
            photo_specs = [{"file": u.split("/")[-1], "url": u} for u in page["photos"][: args.max_photos]]
        photos = []
        for spec in photo_specs:
            fn = download(spec["url"], img_dir)
            w, h = image_size(fn)
            ph = {"src": f"img/{slug}/{spec['file']}", "w": w, "h": h}
            for k in ("focus", "crop"):
                if k in spec:
                    ph[k] = spec[k]
            photos.append(ph)
        item = {
            "id": rec.get("id"), "key": key, "url": link,
            "title": page["title"], "deal": deal, "area": area,
            "facts": facts_line(page["facts"]),
            "price": price_text(meta, page["dek"]),
            "photos": photos,
        }
        for k in ("title", "deal", "area", "facts", "price", "hero", "fit", "zoom"):
            if k in a:
                item[k] = a[k]
        item["source"] = {"kicker": page["kicker"], "facts": page["facts"], "lead": page["dek"],
                          "photos_on_page": len(page["photos"])}
        listings.append(item)

    data = {
        "slug": slug,
        "name": art.get("name", card["name"]),
        "brand": art.get("brand", card["brand"]),
        "role": art.get("role", card["role"]),
        "licence": art.get("licence", card["licence"]),
        "phone": art.get("phone", card["phone"]),
        "site": f"nad-lan.co.il/brokers/{slug}",
        "cta": art.get("cta", "לתיאום סיור פרטי"),
        "portrait": dict({"src": f"img/{slug}/{os.path.basename(portrait_file)}" if portrait_file else None},
                         **art.get("portrait", {})),
        "listings": listings,
    }
    out = os.path.join(ROOT, "data", f"{slug}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("wrote", out, "listings:", len(listings))


if __name__ == "__main__":
    main()
