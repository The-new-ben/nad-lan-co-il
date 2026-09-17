#!/usr/bin/env python3
"""Meital minisite: hierarchy + Yoast + publish. Owner order 17.9.2026 ("publish all").
Phases: --phase1 (city term, /brokers/ generic page, parent, re-patch drafts with collision-safe CSS)
        --snippet (Yoast titles/descriptions via a temporary x- code snippet, then removed)
        --publish [--only=L07,...|broker|brokers] (status publish)   --verify (live GET checks)
Credentials: DPAPI in-process only, never printed."""
import base64, ctypes, ctypes.wintypes as wt, json, os, re, sys, time, urllib.request, urllib.error, urllib.parse, html as htmlmod

SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
PKG = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\aa08c3e7-cd8f-4254-9186-99468d8a8a08\scratchpad\meital\nadlan-meital-listings"
HERE = os.path.dirname(os.path.abspath(__file__))
WP = "https://nad-lan.co.il"
ARGS = sys.argv[1:]
ONLY = [a.split("=", 1)[1] for a in ARGS if a.startswith("--only=")]
ONLY = set(ONLY[0].split(",")) if ONLY else set()

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi_unprotect(b64):
    raw = base64.b64decode(b64)
    blob_in = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        raise RuntimeError("DPAPI decrypt failed")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)

with open(SECRETS_PATH, encoding="utf-8-sig") as f:
    sec = json.load(f)
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi_unprotect(sec['password_dpapi'])}".encode()).decode()

def req(method, path, body=None, params=None, raw=False):
    url = WP + ("" if raw else "/wp-json") + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={"Authorization": AUTH, "Content-Type": "application/json; charset=utf-8", "User-Agent": "nadlan-runner"})
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            b = resp.read()
            return resp.status, (b.decode("utf-8", "replace") if raw else json.loads(b.decode() or "null"))
    except urllib.error.HTTPError as e:
        b = e.read()
        try:
            return e.code, (b.decode("utf-8", "replace") if raw else json.loads(b.decode() or "null"))
        except Exception:
            return e.code, None

def rd(p):
    return open(os.path.join(PKG, p), encoding="utf-8").read()

MAP_PATH = os.path.join(PKG, "data", "import-map.json")
imap = json.load(open(MAP_PATH, encoding="utf-8"))
idx = json.load(open(os.path.join(PKG, "data", "listings.json"), encoding="utf-8"))["listings"]
STATE_PATH = os.path.join(HERE, "meital_publish_state.json")
state = json.load(open(STATE_PATH, encoding="utf-8")) if os.path.exists(STATE_PATH) else {}
def save_state():
    json.dump(state, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# collision-safe extras: hide the theme's own listing layers on these pages, keep the theme H1 in the DOM (visually hidden)
EXTRA_LISTING = """
/* nad-lan: hide theme listing layers that the prestige block already covers */
.nlps-price,.nlps-facts,.nlps-chips,.nlps-trust,.nlps-hl,.nlps-3d,.nlps-facade,.nlps-costs,.nlps-map-sec,.nlcard,article.nlx~div.nlx{display:none!important}
.nlps{margin:0!important;padding:0!important}
.nlps-hero{margin:0!important;padding:0!important;min-height:0!important;border:0!important;background:none!important}
.nlps-title{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important;margin:0!important}
"""
EXTRA_BROKER = """
/* nad-lan: the hero carries the visible name; the theme H1 stays in the DOM for search engines */
body.page-id-{PID} .entry-content>h1,body.page-id-{PID} h1:not(.nlb-name):not(.nlb-h2){position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important}
"""

def inline_css(content, css):
    marker = "<!-- wp:html -->"
    assert content.startswith(marker)
    return marker + "\n<style>\n" + css + "\n</style>\n" + content[len(marker):]

BROKERS_PAGE = {
    "title": "מיניסייט למתווכים ולמשרדי תיווך",
    "slug": "brokers",
    "excerpt": "עמוד מותג ונכסים למתווך בתוך נדלן: דף בית ממותג, עמוד מלא לכל נכס עם מספרים ומקורות, סינון ומפה, וואטסאפ ישיר, עברית ואנגלית.",
    "content": """<!-- wp:paragraph -->
<p><strong>האתר שלכם בתוך נדלן.</strong> דף בית ממותג על שמכם, עמוד מלא לכל נכס, סינון לפי אזור וחדרים, כרטיס ביקור דיגיטלי וגרסה באנגלית לקונים מחו"ל. הכול נבנה על הנכסים האמיתיים שלכם, ושום עמוד לא עולה לאוויר בלי אישור שלכם.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>מה כלול</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li><strong>דף בית ממותג.</strong> השם והמותג שלכם, חיפוש נכסים, אזורי פעילות, כפתור וואטסאפ קבוע ופס יצירת קשר.</li><li><strong>עמוד מלא לכל נכס.</strong> מחיר ומחיר למ"ר, מס רכישה לפי סוג רוכש, מימון, השוואות שוק והסביבה, עם מקור לכל מספר.</li><li><strong>סינון ומפה.</strong> לפי סוג עסקה, אזור וחדרים, ומפה עם מספר הנכסים בכל שכונה.</li><li><strong>כרטיס ביקור דיגיטלי.</strong> חזית וגב עם קוד שפותח שיחה בוואטסאפ, ופוסט מוכן לאינסטגרם.</li><li><strong>עברית ואנגלית.</strong> כל עמוד בשתי השפות, לקונים מקומיים ולמשקיעים מחו"ל.</li><li><strong>פניות מכל נכס.</strong> הודעת וואטסאפ עם קוד הנכס, חיוג בלחיצה וטופס לתיאום סיור.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>איך זה עובד</h2>
<!-- /wp:heading -->
<!-- wp:list {"ordered":true} -->
<ol><li><strong>שולחים את הנכסים.</strong> קישור לאינסטגרם, לאתר או לרשימת הנכסים הפעילים. אנחנו אוספים את הפרטים.</li><li><strong>אנחנו בונים ובודקים.</strong> עמוד מלא לכל נכס, בעברית ובאנגלית, ודף בית ממותג.</li><li><strong>מאשרים ומפרסמים.</strong> עוברים על הנוסח והמחירים. שום עמוד לא עולה בלי אישור בכתב שלכם.</li></ol>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>הצטרפות</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>רוצים מיניסייט כזה? השאירו פרטים ונחזור אליכם עם הצעה ועם דוגמה שנבנית על הנכסים שלכם. <a href="/advertise/">להשארת פרטים</a> או <a href="/contact/">דברו איתנו</a>.</p>
<!-- /wp:paragraph -->""",
}

def phase1():
    # 1. city term for Herzliya (Latin slug) + assign to L01
    st, terms = req("GET", "/wp/v2/nadlan_city", params={"per_page": 100})
    byname = {t["name"]: t["id"] for t in terms}
    if "הרצליה" not in byname:
        st, t = req("POST", "/wp/v2/nadlan_city", {"name": "הרצליה", "slug": "herzliya"})
        print("term herzliya:", st, (t or {}).get("id"), (t or {}).get("slug"))
        byname["הרצליה"] = (t or {}).get("id")
    else:
        print("term herzliya exists:", byname["הרצליה"])
    state["term_herzliya"] = byname["הרצליה"]
    # 2. /brokers/ generic page
    st, ex = req("GET", "/wp/v2/pages", params={"slug": "brokers", "status": "publish,draft,private", "context": "edit"})
    if st == 200 and ex:
        bid = ex[0]["id"]; print("brokers page exists:", bid)
    else:
        st, p = req("POST", "/wp/v2/pages", {"status": "draft", "title": BROKERS_PAGE["title"], "slug": BROKERS_PAGE["slug"], "content": BROKERS_PAGE["content"], "excerpt": BROKERS_PAGE["excerpt"]})
        bid = (p or {}).get("id"); print("brokers page created:", st, bid, (p or {}).get("link"))
    state["brokers_page"] = bid
    # 3. broker page under /brokers/ + demote its own H1 + collision-safe CSS
    pid = imap["broker-he"]
    content = rd("broker/content-broker-he.html")
    content = content.replace('<h1 class="nlb-name">', '<h2 class="nlb-name nlb-h2">').replace("</h1>", "</h2>")
    content = inline_css(content, rd("broker/nlb-broker.css") + EXTRA_BROKER.replace("{PID}", str(pid)))
    st, r = req("POST", f"/wp/v2/pages/{pid}", {"parent": bid, "content": content, "slug": "meital-katzir"})
    print("broker page parent+patch:", st, (r or {}).get("link"), "h1 in saved:", ((r or {}).get("content") or {}).get("raw", "").count("<h1"))
    # 4. re-patch the 11 listing drafts with collision-safe CSS (+ Herzliya term on L01)
    css = rd("assets/nlx-prestige.css") + EXTRA_LISTING
    for it in idx:
        key = f"{it['id']}-he"; pid = imap[key]
        p = json.load(open(os.path.join(PKG, "listings", it["id"], "wp-he.json"), encoding="utf-8"))
        body = {"content": inline_css(rd(f"listings/{it['id']}/{p['content_file']}"), css)}
        if it["id"] == "L01" and state.get("term_herzliya"):
            body["nadlan_city"] = [state["term_herzliya"]]
        st, r = req("POST", f"/wp/v2/nadlan_property/{pid}", body)
        raw = ((r or {}).get("content") or {}).get("raw", "")
        print(f"patched {key} id={pid}: HTTP {st}, saved {len(raw)} chars, hide-rules present: {'article.nlx~div.nlx' in raw}")
    save_state()

def yoast_map():
    m = {}
    for it in idx:
        seo = json.load(open(os.path.join(PKG, "listings", it["id"], "seo.json"), encoding="utf-8"))["he"]["yoast_meta"]
        m[str(imap[f"{it['id']}-he"])] = seo
    bs = json.load(open(os.path.join(PKG, "broker", "seo-broker.json"), encoding="utf-8"))["he"]
    m[str(imap["broker-he"])] = {"_yoast_wpseo_title": bs["title"], "_yoast_wpseo_metadesc": bs["desc"], "_yoast_wpseo_focuskw": bs["kw"]}
    if state.get("brokers_page"):
        m[str(state["brokers_page"])] = {"_yoast_wpseo_title": "מיניסייט למתווכים | עמוד מותג ונכסים בתוך נדלן", "_yoast_wpseo_metadesc": BROKERS_PAGE["excerpt"], "_yoast_wpseo_focuskw": "מיניסייט למתווכים"}
    return m

def snippet():
    m = yoast_map()
    payload = base64.b64encode(json.dumps(m, ensure_ascii=False).encode("utf-8")).decode()
    code = ("add_action('init', function () {\n"
            "  if (get_option('x_meital_yoast_v1')) { return; }\n"
            f"  $m = json_decode(base64_decode('{payload}'), true);\n"
            "  if (!is_array($m)) { return; }\n"
            "  foreach ($m as $id => $f) { foreach ($f as $k => $v) { update_post_meta((int) $id, $k, $v); } }\n"
            "  update_option('x_meital_yoast_v1', 1, false);\n"
            "});\n")
    st, c = req("POST", "/code-snippets/v1/snippets", {"name": "x-meital-yoast", "code": code, "scope": "global", "active": False})
    sid = (c or {}).get("id"); print("snippet create:", st, sid)
    if not sid:
        print(json.dumps(c, ensure_ascii=False)[:300]); return
    st, a = req("PUT", f"/code-snippets/v1/snippets/{sid}/activate", {}); print("activate:", st)
    st, _ = req("GET", "/?x-meital-yoast=1", raw=True); print("trigger GET home:", st)
    time.sleep(1)
    st, _ = req("PUT", f"/code-snippets/v1/snippets/{sid}/deactivate", {}); print("deactivate:", st)
    st, _ = req("DELETE", f"/code-snippets/v1/snippets/{sid}", None); print("delete:", st)
    state["yoast_snippet_id"] = sid; save_state()

def publish():
    targets = []
    for it in idx:
        if not ONLY or it["id"] in ONLY:
            targets.append(("nadlan_property/" + str(imap[it["id"] + "-he"]), it["id"]))
    if not ONLY or "brokers" in ONLY:
        targets.append((f"pages/{state['brokers_page']}", "brokers"))
    if not ONLY or "broker" in ONLY:
        targets.append((f"pages/{imap['broker-he']}", "broker"))
    for path, key in targets:
        st, r = req("POST", f"/wp/v2/{path}", {"status": "publish"})
        print(f"publish {key}: HTTP {st} status={ (r or {}).get('status') } link={ (r or {}).get('link') }")
        state.setdefault("published", {})[key] = (r or {}).get("link")
        time.sleep(0.4)
    save_state()

def verify():
    for key, link in (state.get("published") or {}).items():
        if not link: continue
        try:
            with urllib.request.urlopen(urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"}), timeout=90) as resp:
                s = resp.read().decode("utf-8", "replace"); code = resp.status
        except urllib.error.HTTPError as e:
            code = e.code; s = ""
        title = re.search(r"<title>(.*?)</title>", s, re.S)
        ttl = htmlmod.unescape(title.group(1)).strip()[:70] if title else "-"
        h1n = len(re.findall(r"<h1[\s>]", s))
        prestige = ("nlx-mast" in s) or ("nlb-" in s)
        theme_block = "nlx-signals" in s
        print(key + ": " + str(code) + " title=" + ttl + " h1=" + str(h1n) + " prestige=" + str(prestige) + " theme-nlx-block=" + str(theme_block) + " bytes=" + str(len(s)))

if "--phase1" in ARGS: phase1()
if "--snippet" in ARGS: snippet()
if "--publish" in ARGS: publish()
if "--verify" in ARGS: verify()
def fixh1():
    # the block theme prints no H1 on pages: restore the hero H1 on the broker page, add an H1 to /brokers/
    pid = imap["broker-he"]
    width_css = ("\n/* nad-lan: let the broker page run full width inside the block theme */\n"
                 "body.page-id-" + str(pid) + " .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:0!important;margin-right:0!important}\n"
                 "body.page-id-" + str(pid) + " .entry-content{padding-left:0!important;padding-right:0!important}\n")
    content = inline_css(rd("broker/content-broker-he.html"), rd("broker/nlb-broker.css") + width_css)
    st, r = req("POST", f"/wp/v2/pages/{pid}", {"content": content})
    print("broker page h1 restored:", st, ((r or {}).get("content") or {}).get("raw", "").count("<h1"))
    bid = state["brokers_page"]
    h1 = '<!-- wp:heading {"level":1} -->\n<h1>' + BROKERS_PAGE["title"] + '</h1>\n<!-- /wp:heading -->\n'
    st, r = req("POST", f"/wp/v2/pages/{bid}", {"content": h1 + BROKERS_PAGE["content"]})
    print("brokers page h1 added:", st, ((r or {}).get("content") or {}).get("raw", "").count("<h1"))

if "--fixh1" in ARGS: fixh1()

print("done")
