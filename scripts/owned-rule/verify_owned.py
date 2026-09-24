# -*- coding: utf-8 -*-
"""Live checks for the "listing with an owner" rule and the professionals directory for brokers (HAD-251, HAD-249).
Reads the public, cache-busted HTML (no login) and checks the rendered <body> in both directions: what must be
there, and what must be gone. Usage: python verify_owned.py [--phase css-removed]"""
import html as H, io, json, re, sys, time, urllib.request, urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
PHASE_CSS_REMOVED = "--phase" in sys.argv and "css-removed" in sys.argv

def get(path):
    sep = "&" if "?" in path else "?"
    r = urllib.request.Request(BASE + path + sep + "nlv=%d" % int(time.time() * 1000), headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")

def body_of(t):
    b = t.split("<body", 1)[-1]
    return b

def text_of(b):
    b = re.sub(r"<(script|style)\b.*?</\1>", " ", b, flags=re.S | re.I)
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", b)))

def cls(b, name):
    return len(re.findall(r'class="[^"]*(?<![\w-])' + re.escape(name) + r'(?![\w-])[^"]*"', b))

results = []
def check(page, name, ok, detail=""):
    results.append((page, name, bool(ok), detail))

OWNED = "/properties/tzukei-aviv-3-rooms-berlin-for-sale/"
OFAKIM = "/properties/%d7%9c%d7%9e%d7%9b%d7%99%d7%a8%d7%94-%d7%91%d7%90%d7%95%d7%a4%d7%a7%d7%99%d7%9d-%d7%a9%d7%9b%d7%95%d7%a0%d7%aa-%d7%a9%d7%a4%d7%99%d7%a8%d7%90-%d7%a7%d7%95%d7%98%d7%92-5-%d7%97%d7%93%d7%a8%d7%99%d7%9d/"
CARD = "/professionals/meital-katzir/"

# ---- an owned listing (Meital L04) ----
s, t = get(OWNED); b = body_of(t); x = text_of(b)
check("owned listing", "HTTP 200", s == 200, s)
for c in ("nlps", "nlps-3d", "nlps-hero", "nlps-facade", "nlps-costs", "nlps-map-sec", "nlcard", "nlcard-claim", "nlrc", "nlsch", "nlx-similar", "nlx-signals", "nlcta-start", "nlcta-wa", "yoast-breadcrumbs", "wp-block-post-featured-image", "nlsch-jump"):
    check("owned listing", "no ." + c, cls(b, c) == 0, cls(b, c))
check("owned listing", "no model-viewer script", "model-viewer" not in t, t.count("model-viewer"))
check("owned listing", "no mv-ux script", "mv-ux.js" not in t)
h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", b, re.S)
check("owned listing", "exactly one H1", len(h1) == 1, len(h1))
check("owned listing", "the H1 is the hidden title", bool(re.search(r'<h1 class="nlo-title">', b)))
check("owned listing", "her article is there", cls(b, "nlx") >= 1 and 'id="nlx-L04-he"' in b)
check("owned listing", "her name links to her site", 'class="nlx-home" href="https://nad-lan.co.il/brokers/meital-katzir/"' in b)
more = re.search(r'<section class="nlo-more".*?</section>', b, re.S)
check("owned listing", "'more by this broker' section", bool(more))
if more:
    m = more.group(0)
    hrefs = re.findall(r'class="nlo-card" href="([^"]+)"', m)
    check("owned listing", "3 cards, all hers, not this one", len(hrefs) == 3 and all("/properties/" in u for u in hrefs) and OWNED not in hrefs, hrefs)
    check("owned listing", "heading links her name to her site", 'עוד נכסים של <a href="https://nad-lan.co.il/brokers/meital-katzir/">מיטל קציר</a>' in m)
    check("owned listing", "same deal first (sale)", "למכירה" in re.findall(r'class="nlo-kicker">([^<]*)', m)[0] if re.findall(r'class="nlo-kicker">([^<]*)', m) else False)
check("owned listing", "no portal WhatsApp 972525101555 in the body", "972525101555" not in b)
check("owned listing", "her WhatsApp is there", "972523631582" in b)
check("owned listing", "no 'זה הכרטיס שלכם'", "זה הכרטיס שלכם" not in x)
check("owned listing", "no 'נכסים דומים'", "נכסים דומים" not in x)
check("owned listing", "no 'תיאום מועד ביומן'", "תיאום מועד ביומן" not in x)
check("owned listing", "hreflang kept (3)", len(re.findall(r"hreflang=", t.split("</head>")[0])) == 3, len(re.findall(r"hreflang=", t.split("</head>")[0])))
if PHASE_CSS_REMOVED:
    check("owned listing", "the hiding CSS is gone from the page", ".single-nadlan_property .nlps-hero" not in t and "article.nlx~*" not in t)

# ---- the control: an old-wizard owner listing keeps the portal layers ----
s, t = get(OFAKIM); b = body_of(t); x = text_of(b)
check("Ofakim control", "HTTP 200", s == 200, s)
check("Ofakim control", "portal layer .nlps still there", cls(b, "nlps") >= 1)
check("Ofakim control", "card .nlcard still there", cls(b, "nlcard") >= 1)
check("Ofakim control", "no raw 'owner_wizard' / 'cottage' / 'sale'", not re.search(r"owner_wizard|\bcottage\b|\bsale\b", x), re.findall(r"owner_wizard|\bcottage\b|\bsale\b", x)[:3])
check("Ofakim control", "type and deal in Hebrew", "קוטג׳" in x and "למכירה" in x)
check("Ofakim control", "one H1", len(re.findall(r"<h1\b", b)) == 1)

# ---- Meital's card in the directory ----
s, t = get(CARD); b = body_of(t); x = text_of(b)
check("her card", "HTTP 200", s == 200, s)
check("her card", "gender: 'מתווכת' pill", 'class="nlpp-pill">מתווכת<' in b and 'class="nlpf-pill">מתווכת<' in b)
check("her card", "no masculine 'מתווך' pill", 'pill">מתווך<' not in b)
check("her card", "licence badge after a real check", "מאומת בפנקס המתווכים" in x and "3131540" in x)
check("her card", "no 'מאומת ברשם (gov.il)' by field", "מאומת ברשם (gov.il)" not in x)
check("her card", "no 'טרם התקבלו'", "טרם התקבלו" not in x)
check("her card", "no 'הצעת מחיר'", "הצעת מחיר" not in x)
check("her card", "no video button without meeting_url", "וידאו" not in x)
check("her card", "'תיאום סיור' straight to her", "תיאום סיור" in x and "wa.me/972523631582" in b)
hdr = b.split('class="nlpp-bio"', 1)[0]
check("her card", "header buttons never go to the portal number", "972525101555" not in hdr)
check("her card", "no 'זמינות גבוהה'", "זמינות גבוהה" not in x)
check("her card", "no claim pitch", "זה הכרטיס שלכם" not in x and "רשם הקבלנים הרשמי" not in x)
check("her card", "no raw 'metavech' / 'broker_minisite'", not re.search(r"metavech|broker_minisite", x), re.findall(r"metavech|broker_minisite", x)[:3])
check("her card", "no booking band / 'תיאום מועד ביומן'", cls(b, "nlsch") == 0 and "תיאום מועד ביומן" not in x)
check("her card", "no contractors as 'similar'", "בעלי מקצוע דומים" not in x or "קבלן" not in x.split("בעלי מקצוע דומים", 1)[-1][:600])
check("her card", "breadcrumb in Hebrew", "NadLan Professionals" not in x and "אנשי מקצוע" in x)
check("her card", "plugin trail has 'מתווכים'", bool(re.search(r'<nav class="nlbc".*?מתווכים.*?</nav>', b, re.S)))
check("her card", "exactly one H1", len(re.findall(r"<h1\b", b)) == 1, len(re.findall(r"<h1\b", b)))
check("her card", "link to her site", 'href="https://nad-lan.co.il/brokers/meital-katzir/"' in b)

# ---- the directory ----
s, t = get("/professionals/"); b = body_of(t); x = text_of(b)
check("directory", "HTTP 200", s == 200, s)
check("directory", "H1 without 'מאומת'", "<h1>מצאו בעל מקצוע לנדל״ן</h1>" in b)
lead = re.search(r'<p class="nldir-lead">(.*?)</p>', b, re.S)
check("directory", "lead from the sources", bool(lead) and "קבלנים רשומים מפנקס הקבלנים" in lead.group(1) and "ומתווכת אחת עם רישיון שנבדק בפנקס המתווכים" in lead.group(1), text_of(lead.group(1)) if lead else "")
check("directory", "old claim gone", "מאומתים מול פנקס הקבלנים" not in x)
check("directory", "title without 'מאומתים'", "מאומתים" not in t.split("</title>")[0].split("<title>")[-1], t.split("</title>")[0].split("<title>")[-1][:120])
check("directory", "no 'היו הראשונים לדרג' on cards", "היו הראשונים לדרג" not in x)

# ---- a contractor from the register (control) ----
s, t = get("/professionals/%d7%97%d7%9b%d7%99%d7%9d-%d7%a8%d7%a0%d7%99-%d7%90%d7%9c%d7%93%d7%a8/"); b = body_of(t); x = text_of(b)
check("contractor control", "HTTP 200", s == 200, s)
check("contractor control", "register badge (source = register)", "מאומת ברשם (gov.il)" in x)
check("contractor control", "quote request kept for a contractor", "הצעת מחיר" in x)
check("contractor control", "no 'טרם התקבלו'", "טרם התקבלו" not in x)
check("contractor control", "similar professionals kept", "בעלי מקצוע דומים" in x)
check("contractor control", "claim prompt names the contractors register", "ממאגר רשם הקבלנים הרשמי" in x)

# ---- a broker page (her English twin): no portal pill ----
s, t = get("/en/brokers/meital-katzir/tzukei-aviv-3-room-apartment-for-sale/"); b = body_of(t)
check("English twin", "HTTP 200", s == 200, s)
check("English twin", "no portal WhatsApp pill", cls(b, "nlcta-wa") == 0)

# ---- health ----
s, t = get("/wp-json/nadlan/v1/healthcheck")
try:
    hc = json.loads(t)
except Exception:
    hc = {}
check("health", "owned rule reported on", (hc.get("owned_rule") or {}).get("on") is True, hc.get("owned_rule"))

bad = 0
for page, name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {page:18s} {name}" + ("" if ok else f"   [{detail}]"))
    bad += not ok
print(f"\n{len(results) - bad}/{len(results)} checks pass")
sys.exit(1 if bad else 0)
