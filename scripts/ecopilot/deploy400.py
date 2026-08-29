# -*- coding: utf-8 -*-
"""EcoCity pilot content goes live on the two flagship pages (owner order 28.8:
"תבדוק ואם אפשר לחבר לאתר"). Fact-register rules enforced: attributed developer
claims, no floors for Stricker, no inventory/prices/architect/permit, disclosure
kept. Full before-state backup for rollback."""
import base64, ctypes, ctypes.wintypes, io, json, os, re, secrets, sys, time, urllib.request, urllib.error
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
HERE = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi(b64):
    raw = base64.b64decode(b64)
    bi = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("dpapi")
    try:
        return ctypes.string_at(bo.pbData, bo.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pbData)

sec = json.load(open(SECRETS_PATH, encoding="utf-8-sig"))
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi(sec['password_dpapi'])}".encode()).decode()

def req(method, path, body=None, timeout=120, raw=False):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-EcoPilot/1.0")
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            payload = resp.read()
            return resp.status, payload if raw else json.loads(payload.decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        p = e.read()
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}

def must(s, p, what, ok=(200, 201)):
    if s not in ok:
        raise SystemExit(f"FATAL {what}: HTTP {s}: {json.dumps(p, ensure_ascii=False)[:300]}")
    return p

DISCLOSURE = ('<p><small>עמוד זה הוא עמוד מידע עצמאי של nad-lan.co.il ואינו האתר הרשמי של אקו סיטי. '
              'מלאי, מחיר, מפרט, היתר ומועד מסירה מחייבים רק לפי מידע עדכני מהיזם וממסמכי העסקה. '
              'העובדות בעמוד נבדקו ב-28.08.2026 מול פרסומי היזם ומקורות עירוניים.</small></p>')

BNEI = {
    "post_id": 6693,
    "content": (
        '<p><strong>בני דן 54-56</strong> הוא פרויקט מגורים של אקו סיטי בצפון תל אביב, לאורך פארק הירקון. '
        'לפי עמוד היזם שנבדק ב-28 באוגוסט 2026, מדובר בבניין בוטיק בן שמונה קומות. אקו סיטי מציינת שכל '
        'הדירות נהנות מחזית פתוחה, וכי בפרויקט מתוכננות מרפסות עמוקות מהסטנדרט וחניות רגילות. נכון למועד '
        'הבדיקה הפרויקט מוצג בשיווק ולקראת ביצוע, עם אכלוס מתוכנן בשנת 2028.</p>'
        '<p>העמוד הזה נבנה כדי לעזור לכם להבין את הפרויקט ואת חיי הפארק לפני פנייה: מה מאומת, מה טענת יזם '
        'שדורשת בדיקה בתוכנית המכר, ואילו בדיקות כדאי להשלים לפני חתימה. מלאי, מחירים ושטחים יוצגו כאן רק '
        'כשיגיעו ממקור מאושר ומתוארך.</p>'
        '<h2>הפארק כתוכנית יומית</h2>'
        '<p>הסיפור של בני דן מתחיל בבוקר: יציאה מהבניין אל הרחוב, תנועה לאורך פארק הירקון, וחזרה אל המרפסת '
        'ואל חלל המגורים. הפארק, מהשטחים הירוקים הגדולים בעיר, משרת ריצה, רכיבה, הליכה ופנאי, והוא חלק '
        'משגרת היום של הכתובת הזו ולא תמונת רקע. את המבט מכל קומה נציג במודל כסימולציה מסומנת, לצד צילומים '
        'מתועדים כשיהיו.</p>'
        '<h2>מרפסות, חזיתות וחניה: מה אומר היזם</h2>'
        '<p>אקו סיטי מתארת חזית פתוחה לכל הדירות, מרפסות עמוקות מהסטנדרט וחניות רגילות. אלה מאפיינים '
        'תכנוניים לפי היזם: את היישום בכל דירה בודקים בתוכנית המכר, במפרט ובהסכם, כולל מידות המרפסת, כיוון '
        'הדירה וההצמדות. חזית פתוחה היום אינה הבטחה לנוף פתוח לתמיד, והבדיקה הנכונה היא מול הזכויות '
        'והתוכניות בסביבה.</p>'
        '<h2>צפון תל אביב, לאורך הירקון</h2>'
        '<p>הסביבה נבנית מפארק, תחבורה, חינוך, תרבות ושירותים. הרכבת הקלה בקו הירוק היא תשתית מתוכננת עם '
        'תחנה בשם יהודה המכבי, ונציג אותה כעתידית עד שתפעל. מוסדות החינוך נבדקים מול הרישום העירוני לפי שנת '
        'הלימודים, והחוף הוא יעד עירוני ולא חלק מהפרויקט. להרחבה על האזור: '
        '<a href="https://nad-lan.co.il/new-projects/north-tel-aviv-new-projects/">פרויקטים חדשים בצפון תל אביב</a>, '
        'ולכלי הבדיקה: <a href="https://nad-lan.co.il/apartment-buying-checklist/">צ׳קליסט בדיקות לפני קנייה</a> '
        'ו<a href="https://nad-lan.co.il/purchase-tax-calculator/">מחשבון מס רכישה</a>.</p>'
        '<h2>מה בודקים לפני פגישה</h2>'
        '<p>מומלץ להגיע לפגישת מכירה עם רשימה סדורה: תוכנית הדירה והמידות, מידות המרפסת והצללתה, הצמדת '
        'החניה והמחסן, שלב ההיתר והליווי הבנקאי, המפרט הטכני, לוח התשלומים ומועד המסירה החוזי. אפשר לבקש '
        'מאיתנו מידע עדכני מהפרויקט דרך הטופס, ונחזור אליכם עם מה שידוע ומאומת.</p>'
        + DISCLOSURE
    ),
    "faq": [
        {"q": "איפה נמצא הפרויקט?", "a": "ברחוב בני דן 54-56 בצפון תל אביב, לאורך פארק הירקון."},
        {"q": "האם כל הדירות פונות לפארק?", "a": "אקו סיטי מציינת שכל הדירות נהנות מחזית פתוחה. את היישום בכל דירה בודקים בתוכנית המכר, ואין בכך הבטחה לנוף פתוח לתמיד."},
        {"q": "כמה קומות יש בבניין?", "a": "לפי עמוד אקו סיטי שנבדק ב-28 באוגוסט 2026, הבניין מתנשא לגובה שמונה קומות."},
        {"q": "כמה דירות יש בפרויקט?", "a": "מספר הדירות הכולל טרם אומת במקור ראשוני, ולכן איננו מציגים אותו. נעדכן כשיתקבל נתון מאושר מהיזם."},
        {"q": "מה מיוחד במרפסות?", "a": "היזם מתאר מרפסות עמוקות מהסטנדרט. כדי להעריך שימושיות בודקים מידה, שטח, כיוון והצללה בתוכנית הדירה הספציפית."},
        {"q": "האם לכל דירה יש חניה?", "a": "היזם מציין חניות רגילות בפרויקט. הצמדת חניה לדירה מסוימת נקבעת במסמכי העסקה בלבד."},
        {"q": "מה הסטטוס ומתי האכלוס?", "a": "נכון ל-28 באוגוסט 2026 הפרויקט מוצג בשיווק ולקראת ביצוע, עם יעד אכלוס בשנת 2028. המועד המחייב הוא המועד החוזי."},
    ],
    "yoast_title": "בני דן 54-56: פרויקט אקו סיטי מול פארק הירקון | נדלן",
    "yoast_desc": "בני דן 54-56 בתל אביב: בניין בן 8 קומות בקו הראשון לפארק לפי אקו סיטי. עובדות מאומתות, סטטוס, סביבה, מרפסות וכלי בדיקה לרוכש.",
    "focuskw": "בני דן 54-56",
    "subtitle": "בניין בוטיק בן שמונה קומות לאורך פארק הירקון לפי אקו סיטי: חזיתות פתוחות, מרפסות עמוקות ובדיקות רוכש מסודרות",
    "eyebrow": "אקו סיטי · פארק הירקון",
}

STRICKER = {
    "post_id": 6694,
    "content": (
        '<p><strong>שטריקר 13-ברנדיס 14</strong> הוא פרויקט מגורים של אקו סיטי בשתי כתובות סמוכות בצפון תל '
        'אביב. לפי עמוד הפרויקט של היזם, התכנון כולל שני בניינים, 26 דירות בכל בניין, ובהם פנטהאוזים '
        'המשתרעים על קומה שלמה. נכון ל-28 באוגוסט 2026, אקו סיטי מציגה את הפרויקט בשיווק ולקראת ביצוע, עם '
        'אכלוס מתוכנן בשנת 2028. הסטטוס והמועד עשויים להשתנות, ולכן מאמתים אותם מול היזם ובמסמכי המכר לפני '
        'כל החלטה.</p>'
        '<p>הסיפור של הכתובת לא נבנה ממרחקים משוערים אלא מחיבור למוקדים עירוניים ברורים: יהודה המכבי, כיכר '
        'מילאנו, פארק הירקון והקו הירוק המתוכנן. בעמוד הזה מכירים את צמד הבניינים, מבינים מה מאומת ומה עדיין '
        'חסר, ומתכוננים נכון לפגישת המכירה.</p>'
        '<h2>שני בניינים, 26 דירות בכל אחד</h2>'
        '<p>המבנה המאומת לפי עמוד היזם: שני בנייני בוטיק, 26 דירות בכל בניין, 52 דירות בסך הכול. אקו סיטי '
        'מציינת גם פנטהאוזים המשתרעים על קומה שלמה; אילו יחידות בדיוק, באיזה שטח ובאיזה מפרט, נבדק מול טבלת '
        'היחידות והתוכניות. תמהיל, שטחים, חניה, מחסן ומלאי יוצגו כאן רק לאחר קבלת קובץ מאושר מהיזם.</p>'
        '<h2>מרחב יהודה המכבי וכיכר מילאנו</h2>'
        '<p>עמוד היזם מציין את יהודה המכבי, כיכר מילאנו, הפארק ותחנת הרכבת הקלה כעוגני הסביבה של הפרויקט. '
        'תחנת יהודה המכבי היא חלק מהקו הירוק המתוכנן, ולכן היא מוצגת כתשתית עתידית ולא כשירות פעיל. את '
        'השגרה סביב הכתובות בונים מהרחובות עצמם, מהכיכר ומפארק הירקון הסמוך למרחב. להרחבה: '
        '<a href="https://nad-lan.co.il/new-projects/north-tel-aviv-new-projects/">פרויקטים חדשים בצפון תל אביב</a> '
        'ו<a href="https://nad-lan.co.il/projects/bnei-dan-54-56/">בני דן 54-56 של אקו סיטי ליד הפארק</a>.</p>'
        '<h2>מבדיקה ראשונה לפגישה מוכנה</h2>'
        '<p>הדרך הנכונה: בוחרים תחילה בין שני הבניינים, אחר כך קומה וכיוון, ורק אז עוברים לתוכנית ולפנייה. '
        'לפגישה מגיעים עם שאלות סדורות: שלב ההיתר והליווי, טבלת היחידות והפנטהאוזים, מידות ומפרט, לוח '
        'תשלומים ומועד מסירה חוזי. כלים לעזרה: '
        '<a href="https://nad-lan.co.il/apartment-buying-checklist/">צ׳קליסט בדיקות לפני קנייה</a> '
        'ו<a href="https://nad-lan.co.il/mortgage-calculator/">מחשבון משכנתא</a>.</p>'
        + DISCLOSURE
    ),
    "faq": [
        {"q": "כמה דירות מתוכננות בפרויקט?", "a": "לפי עמוד אקו סיטי שנבדק ב-28 באוגוסט 2026: שני בניינים, 26 דירות בכל בניין, 52 דירות בסך הכול."},
        {"q": "האם יש פנטהאוזים?", "a": "אקו סיטי מציינת פנטהאוזים המשתרעים על קומה שלמה. אילו יחידות בדיוק ובאיזה מפרט נבדק מול טבלת היחידות של היזם."},
        {"q": "מה סטטוס הפרויקט ומתי האכלוס?", "a": "נכון ל-28 באוגוסט 2026 הפרויקט מוצג בשיווק ולקראת ביצוע, עם יעד אכלוס בשנת 2028 לפי היזם. המועד המחייב הוא המועד החוזי."},
        {"q": "האם הרכבת הקלה כבר פועלת באזור?", "a": "לא. תחנת יהודה המכבי היא חלק מהקו הירוק המתוכנן, והיא מוצגת כתשתית עתידית עד שתפעל."},
        {"q": "היכן בדיוק שתי הכתובות?", "a": "שטריקר 13 וברנדיס 14, שתי כתובות סמוכות בצפון תל אביב, במרחב שבין יהודה המכבי לכיכר מילאנו."},
    ],
    "yoast_title": "שטריקר 13-ברנדיס 14: פרויקט אקו סיטי בתל אביב | נדלן",
    "yoast_desc": "שטריקר 13 וברנדיס 14 בתל אביב: שני בניינים, 26 דירות בכל בניין ופנטהאוזים על קומה שלמה לפי היזם. סטטוס, סביבה, תוכניות ומידע מאומת.",
    "focuskw": "שטריקר 13 ברנדיס 14",
    "subtitle": "שני בנייני בוטיק של אקו סיטי בין יהודה המכבי לכיכר מילאנו: 26 דירות בכל בניין ופנטהאוזים על קומה שלמה לפי היזם",
    "eyebrow": "אקו סיטי · צפון תל אביב",
}

for spec in (BNEI, STRICKER):
    assert "\u2014" not in spec["content"] and "\u2013" not in spec["content"], "dash law"

# ---- 1. before-state backup ----
backup = {}
for spec in (BNEI, STRICKER):
    pid = spec["post_id"]
    s, p = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=id,slug,title,content.raw,meta")
    must(s, p, f"read {pid}")
    backup[pid] = p
with open(os.path.join(HERE, "ecopilot-before-state.json"), "w", encoding="utf-8") as f:
    json.dump(backup, f, ensure_ascii=False, indent=1)
for pid, p in backup.items():
    print(f"[before] {pid} {p['slug']} content.raw {len(p['content']['raw'])} chars, faq set: {bool((p.get('meta') or {}).get('project_faq_json'))}")

# ---- 2. bridge for unregistered meta (subtitle/eyebrow/yoast) ----
TOKEN = secrets.token_hex(16)
CODE = (
    "add_action( 'rest_api_init', function () {\n"
    "\tregister_rest_route( 'nadlan-ecopilot/v1', '/seed', array(\n"
    "\t\t'methods' => 'POST',\n"
    "\t\t'permission_callback' => function () { return current_user_can( 'manage_options' ); },\n"
    "\t\t'callback' => function ( $req ) {\n"
    "\t\t\t$b = $req->get_json_params();\n"
    "\t\t\tif ( ! is_array( $b ) || ! hash_equals( '" + TOKEN + "', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'no', 'no', array( 'status' => 403 ) ); }\n"
    "\t\t\t$out = array();\n"
    "\t\t\t$pid = (int) ( $b['post_id'] ?? 0 );\n"
    "\t\t\tif ( ! empty( $b['before'] ) ) {\n"
    "\t\t\t\tforeach ( array( 'project_subtitle', 'project_hero_eyebrow', '_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw', 'num_floors', 'floors' ) as $k ) {\n"
    "\t\t\t\t\t$out['before'][ $k ] = (string) get_post_meta( $pid, $k, true );\n"
    "\t\t\t\t}\n"
    "\t\t\t\treturn $out;\n"
    "\t\t\t}\n"
    "\t\t\tforeach ( (array) ( $b['meta'] ?? array() ) as $k => $v ) {\n"
    "\t\t\t\tupdate_post_meta( $pid, $k, wp_slash( (string) $v ) );\n"
    "\t\t\t\t$out['meta'][ $k ] = mb_strlen( (string) $v );\n"
    "\t\t\t}\n"
    "\t\t\tif ( ! empty( $b['purge'] ) ) { do_action( 'litespeed_purge_all' ); $out['purged'] = 1; }\n"
    "\t\t\treturn $out;\n"
    "\t\t},\n"
    "\t) );\n"
    "} );\n"
)
s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": f"tmp-ecopilot-{int(time.time())}", "code": CODE, "scope": "global", "active": False})
must(s, c, "bridge create")
SID = c["id"]
must(*req("PUT", f"/wp-json/code-snippets/v1/snippets/{SID}/activate", {}), "bridge activate")

def seed(payload, what):
    payload["token"] = TOKEN
    s, r = req("POST", "/wp-json/nadlan-ecopilot/v1/seed", body=payload)
    must(s, r, what)
    return r

meta_before = {}
for spec in (BNEI, STRICKER):
    meta_before[spec["post_id"]] = seed({"post_id": spec["post_id"], "before": 1}, "meta before")["before"]
with open(os.path.join(HERE, "ecopilot-before-meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta_before, f, ensure_ascii=False, indent=1)
print("[before-meta]", json.dumps(meta_before, ensure_ascii=False)[:400])

# ---- 3. apply ----
for spec in (BNEI, STRICKER):
    pid = spec["post_id"]
    s, p = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {
        "content": spec["content"],
        "meta": {"project_faq_json": json.dumps(spec["faq"], ensure_ascii=False)},
    })
    must(s, p, f"content {pid}")
    seed({"post_id": pid, "meta": {
        "project_subtitle": spec["subtitle"],
        "project_hero_eyebrow": spec["eyebrow"],
        "_yoast_wpseo_title": spec["yoast_title"],
        "_yoast_wpseo_metadesc": spec["yoast_desc"],
        "_yoast_wpseo_focuskw": spec["focuskw"],
    }}, f"meta {pid}")
    print(f"[applied] {pid} modified {p.get('modified')}")

seed({"purge": 1}, "purge")
s, d = req("DELETE", f"/wp-json/code-snippets/v1/snippets/{SID}", None)
print("[bridge-delete]", s)

# ---- 4. verify ----
time.sleep(8)
for spec in (BNEI, STRICKER):
    slug = "bnei-dan-54-56" if spec["post_id"] == 6693 else "stricker-13-brandeis-14"
    s, page = req("GET", f"/projects/{slug}/", raw=True)
    h = page.decode("utf-8", "replace")
    title = (re.search(r"<title>(.*?)</title>", h, re.S) or [None, ""])[1]
    body_i = h.find("nadlan-project-article")
    art = h[body_i:] if body_i > 0 else h
    print(f"[verify] {slug}: http {s} | h1 {len(re.findall(chr(60)+'h1', h))} | title: {title.strip()[:70]}"
          f" | opener: {'אקו סיטי' in art} | faq: {'שאלות' in art or 'FAQ' in art.upper()}"
          f" | emdash-visible: {art.count(chr(0x2014))} | disclosure: {'עמוד מידע עצמאי' in art}")
print("ECOPILOT DONE")
