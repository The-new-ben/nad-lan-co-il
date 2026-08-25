# -*- coding: utf-8 -*-
"""Aurelia Sde Dov — live build runner (owner GO 26.8.2026: clean slug, no preview,
compact card). Creates the nadlan_project post, uploads media, seeds meta via a
temporary Code Snippets REST bridge, installs the persistent x-aurelia-experience
snippet, verifies, and prints redacted evidence JSON. Zero-dependency (urllib)."""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, re, secrets, sys, time, urllib.request, urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "wp-assets")
PKG = os.path.join(HERE, "zip", "aurelia-master-recipe-1.0.0-rc3")
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
EVIDENCE = {"steps": []}

def log(step, **kw):
    EVIDENCE["steps"].append({"step": step, **kw})
    print(f"[{step}] " + json.dumps(kw, ensure_ascii=False)[:300])

# ---- DPAPI ----
class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

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
USER = sec["username"]
PASS = dpapi_unprotect(sec["password_dpapi"])
AUTH = "Basic " + base64.b64encode(f"{USER}:{PASS}".encode()).decode()

def req(method, path, body=None, ctype="application/json", extra=None, timeout=90, raw=False):
    url = path if path.startswith("http") else BASE + path
    data = None
    if body is not None:
        data = body if isinstance(body, (bytes, bytearray)) else json.dumps(body, ensure_ascii=False).encode("utf-8")
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", "NadLan-Aurelia-Build/1.0")
    if body is not None:
        r.add_header("Content-Type", ctype)
    for k, v in (extra or {}).items():
        r.add_header(k, v)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            payload = resp.read()
            return resp.status, payload if raw else json.loads(payload.decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        payload = e.read()
        try:
            return e.code, json.loads(payload.decode("utf-8"))
        except Exception:
            return e.code, {"raw": payload[:400].decode("utf-8", "replace")}

def must(status, payload, what, ok=(200, 201)):
    if status not in ok:
        print(json.dumps(EVIDENCE, ensure_ascii=False)[:2000])
        raise SystemExit(f"FATAL {what}: HTTP {status}: {json.dumps(payload, ensure_ascii=False)[:400]}")
    return payload

# ---- 0. health ----
s, h = req("GET", "/wp-json/nadlan/v1/health")
must(s, h, "health")
log("health", version=h.get("version"), status=h.get("status"))
assert h.get("status") == "ok"

# ---- 1. media uploads ----
MIME = {".jpg": "image/jpeg", ".png": "image/png", ".glb": "model/gltf-binary"}
ALTS = {
    "aurelia-tower-sde-dov-hero.jpg": "מגדל אורליה שדה דב ושני אגפי הגן מול הים",
    "aurelia-living-room-interior.jpg": "סלון דירה באורליה שדה דב עם חזית זכוכית אל הים",
    "aurelia-wellness-amenities.jpg": "מתחם הבריאות והבריכה באורליה שדה דב",
    "aurelia-quarter-aerial-view.jpg": "אורליה בתוך רובע שדה דב — מבט אווירי אל קו החוף",
    "aurelia-living-panorama-360.jpg": "פנורמת 360 של חלל המגורים באורליה",
    "aurelia-bedroom-panorama-360.jpg": "פנורמת 360 של סוויטת ההורים באורליה",
    "aurelia-pool-panorama-360.jpg": "פנורמת 360 של בריכת האינפיניטי באורליה",
    "aurelia-gym-panorama-360.jpg": "פנורמת 360 של מועדון הכושר באורליה",
    "aurelia-plan-2br.png": "תוכנית דירת 2 חדרים באורליה שדה דב",
    "aurelia-plan-3br.png": "תוכנית דירת 3 חדרים באורליה שדה דב",
    "aurelia-plan-4br.png": "תוכנית דירת 4 חדרים באורליה שדה דב",
    "aurelia-plan-5br.png": "תוכנית דירת 5 חדרים באורליה שדה דב",
    "aurelia-plan-penthouse.png": "תוכנית פנטהאוז באורליה שדה דב",
    "aurelia-site-plan.png": "תוכנית המתחם של אורליה שדה דב",
}
media = {}
glb_pending = None
for name in sorted(os.listdir(ASSETS)):
    p = os.path.join(ASSETS, name)
    ext = os.path.splitext(name)[1].lower()
    with open(p, "rb") as f:
        blob = f.read()
    s, m = req("POST", "/wp-json/wp/v2/media", body=blob, ctype=MIME.get(ext, "application/octet-stream"),
               extra={"Content-Disposition": f'attachment; filename="{name}"'}, timeout=180)
    if s in (200, 201):
        media[name] = {"id": m["id"], "url": m["source_url"]}
        alt = ALTS.get(name, "")
        if alt:
            req("POST", f"/wp-json/wp/v2/media/{m['id']}", body={"alt_text": alt, "title": alt})
        log("media", name=name, id=m["id"], url=m["source_url"])
    elif ext == ".glb":
        glb_pending = (name, blob)
        log("media-glb-deferred", name=name, http=s, note="will write via bridge")
    else:
        must(s, m, f"media {name}")

U = lambda n: media[n]["url"]

# ---- 2. units transform ----
with open(os.path.join(PKG, "01-DEMO-LAB", "data", "units.json"), encoding="utf-8") as f:
    src_units = json.load(f)
PLAN_URL = {
    "plan-2br": U("aurelia-plan-2br.png"), "plan-3br": U("aurelia-plan-3br.png"),
    "plan-4br": U("aurelia-plan-4br.png"), "plan-5br": U("aurelia-plan-5br.png"),
    "plan-penthouse": U("aurelia-plan-penthouse.png"),
}
units = []
for u in src_units:
    status = "reserved" if u.get("availability") == "שמור" else "available"
    units.append({
        "id": u["id"], "label": u.get("label", u["id"]), "building": u.get("building", "Aurelia Tower"),
        "floor": u["floor"], "line": u.get("line", ""), "rooms": u["rooms"], "sqm": u["sqm"],
        "balcony": u.get("balcony", 0), "dir": u.get("dir", ""), "directionAzimuth": u.get("directionAzimuth", 0),
        "view": u.get("view", ""), "status": status,
        "recommended": u.get("availability") == "בעדיפות",
        "price": u.get("price", 0),
        "plan": PLAN_URL.get(u.get("plan_id", ""), PLAN_URL["plan-3br"]),
        "tour_url": f"{BASE}/projects/aurelia/?aurelia_tour={u['id']}",
        "hotspot_position": u.get("hotspot_position", ""), "hotspot_normal": u.get("hotspot_normal", "0 0 1"),
        "camera_orbit": u.get("camera_orbit", ""),
    })
units_json = json.dumps(units, ensure_ascii=False, separators=(",", ":"))
prices = [u["price"] for u in units if u["price"]]
log("units", count=len(units), bytes=len(units_json.encode("utf-8")), price_min=min(prices), price_max=max(prices))

# ---- 3. create the post ----
ARTICLE = (
    '<p><strong>אורליה שדה דב (Aurelia Sde Dov)</strong> — מגדל בן 47 קומות ושני אגפי גן בני שמונה קומות ברובע שדה דב '
    'בתל אביב-יפו, דקות הליכה מקו החוף. בפרויקט 320 דירות בתמהיל של 2–6 חדרים ופנטהאוזים, והמחיר המלא של כל דירה מוצג '
    'בכרטיס שלה. מערכת הבחירה שבעמוד מחברת כל דירה לתוכנית שלה, לכיוון ולנוף מהחלון, לסיור הפנים, לעיצוב הדירה '
    'ולבקשת תוכניות ומחירים — מסע אחד שנשמר מרגע הבחירה ועד הפגישה.</p>'
    '<p>בוחרים דירה ישירות על הבניין או מרשימת המלאי: כל בחירה מעדכנת יחד את הכרטיס, את התוכנית, את המפה ואת אלומת '
    'הכיוון. הדירות המערביות צופות אל הים ואל הטיילת; הדירות המזרחיות פונות אל הרובע החדש ואל פארק הירקון. במפלסי '
    'המתקנים: בריכת אינפיניטי באורך 42 מטר, ספא ותרמו-גארדן, מועדון כושר, חללי עבודה, מועדון דיירים, סוויטת אורחים, '
    'קונסיירז׳ וחדר משלוחים מקורר.</p>'
    '<h2>איך בוחרים דירה באורליה שדה דב</h2>'
    '<p>המסע בנוי סביב הדירה שבחרתם: פותחים את הבניין התלת-ממדי, מסובבים אותו ובוחרים קומה וקו — או מסננים את המלאי '
    'לפי מספר חדרים. הכרטיס מציג קומה, כיוון, שטח, מרפסת ומחיר; ממנו ממשיכים לתוכנית הדירה, למבט מהחלון בגובה הקומה '
    'האמיתי, לסיור פנים ולסטודיו העיצוב. בסיום, בקשת התוכניות והמחירים יוצאת עם כל ההקשר שנבחר — בלי להתחיל מחדש.</p>'
    '<h2>הרובע: שדה דב</h2>'
    '<p>רובע שדה דב הוא פרויקט החוף הגדול של תל אביב — כ-16,000 יחידות דיור מתוכננות על קו הים, לצד פארקים, שדרות, '
    'מסחר שכונתי ותוואי הרכבת הקלה. אורליה יושבת בלב הרובע: הים במרחק הליכה קצרה מערבה, פארק הירקון ונמל תל אביב '
    'דרומה, והעיר כולה נפתחת מזרחה.</p>'
)
post_body = {
    "title": "Aurelia Sde Dov - אורליה שדה דב",
    "slug": "aurelia",
    "status": "publish",
    "content": ARTICLE,
    "excerpt": "בחרו דירה באורליה שדה דב לפי קומה וכיוון, צפו בתוכנית ובנוף והמשיכו לפגישה עם כל ההקשר.",
    "meta": {
        "developer_name": "Aurelia Development Group",
        "address": "רובע שדה דב, תל אביב-יפו",
        "city": "תל אביב יפו",
        "neighborhood": "שדה דב",
        "project_type": "new",
        "project_status": "construction",
        "num_units": 320,
        "num_buildings": 3,
        "num_floors": 47,
        "completion_year": 2030,
        "price_min": min(prices),
        "price_max": max(prices),
        "lat": 32.1057,
        "lng": 34.7779,
        "source": "nadlan-flagship",
        "data_quality": "enriched",
        "project_price_updated": "08/2026",
        "project_3d_default_orbit": "-28deg 69deg 185m",
        "project_3d_default_target": "0m 79m 0m",
        "project_gallery_json": json.dumps([
            U("aurelia-tower-sde-dov-hero.jpg"), U("aurelia-quarter-aerial-view.jpg"),
            U("aurelia-wellness-amenities.jpg"), U("aurelia-living-room-interior.jpg"),
            U("aurelia-site-plan.png"),
        ], ensure_ascii=False),
        "project_interior_panoramas": json.dumps([
            {"url": U("aurelia-living-panorama-360.jpg"), "title": "סלון, מטבח ומרפסת"},
            {"url": U("aurelia-bedroom-panorama-360.jpg"), "title": "סוויטת הורים"},
            {"url": U("aurelia-pool-panorama-360.jpg"), "title": "בריכת האינפיניטי"},
            {"url": U("aurelia-gym-panorama-360.jpg"), "title": "מועדון הכושר"},
        ], ensure_ascii=False),
        "project_faq_json": json.dumps([
            {"q": "איך בוחרים דירה באורליה שדה דב?", "a": "לוחצים על נקודה בבניין או על שורה במלאי; הכרטיס, התוכנית, הנוף והפנייה ממשיכים עם אותה דירה."},
            {"q": "איפה רואים את מחיר הדירה?", "a": "המחיר המלא מופיע בכרטיס הדירה לצד הקומה, הכיוון, השטח והמרפסת."},
            {"q": "אפשר לראות תוכנית ונוף לכל דירה?", "a": "כן. לכל דירה תוכנית לפי מספר החדרים ומבט מהחלון לפי הכיוון וגובה הקומה."},
            {"q": "מה יש בבניין עצמו?", "a": "בריכת אינפיניטי, ספא, מועדון כושר, חללי עבודה, מועדון דיירים, סוויטת אורחים, קונסיירז׳ וחדר משלוחים."},
        ], ensure_ascii=False),
        "project_area_json": json.dumps({
            "label": {"he": "רובע שדה דב", "en": "Sde Dov Quarter"},
            "blurb": {"he": "רובע החוף החדש של תל אביב — ים, פארק, רכבת קלה ושירותים במרחק הליכה", "en": "Tel Aviv's new coastal quarter — sea, park, light rail and daily services within walking distance"},
            "coast_x": 16,
            "stats": [
                {"value": "כ-16,000", "label": {"he": "יחידות דיור מתוכננות ברובע", "en": "planned homes in the quarter"}},
                {"value": "5 דק'", "label": {"he": "הליכה לחוף הים", "en": "walk to the beach"}},
                {"value": "47", "label": {"he": "קומות במגדל אורליה", "en": "Aurelia tower floors"}},
                {"value": "2030", "label": {"he": "אכלוס משוער", "en": "estimated occupancy"}},
            ],
            "groups": [
                {"icon": "pin", "label": {"he": "חוף וטיילת", "en": "Beach & promenade"}, "items": [
                    {"he": "קו ראשון לחוף שדה דב ולטיילת המתחדשת", "en": "First line to the Sde Dov beach and renewed promenade"},
                    {"he": "רצועת החוף נמשכת דרומה עד נמל תל אביב", "en": "The coastline continues south to the Tel Aviv Port"}]},
                {"icon": "landmark", "label": {"he": "פארק ופנאי", "en": "Parks & leisure"}, "items": [
                    {"he": "פארק הירקון וגני יהושע ברכיבה קצרה", "en": "Yarkon Park a short ride away"},
                    {"he": "שבילי אופניים לאורך הירקון וקו החוף", "en": "Bike paths along the Yarkon and the coast"}]},
                {"icon": "train", "label": {"he": "תחבורה", "en": "Transit"}, "items": [
                    {"he": "הקו הירוק של הרכבת הקלה מתוכנן לשרת את הרובע", "en": "The light-rail Green Line is planned to serve the quarter"},
                    {"he": "נתיבי איילון וצירי העיר במרחק נסיעה קצר", "en": "Ayalon lanes and city routes a short drive away"}]},
                {"icon": "store", "label": {"he": "מסחר ושירותים", "en": "Retail & services"}, "items": [
                    {"he": "מסחר שכונתי מתוכנן בקומות הקרקע ברובע", "en": "Neighborhood retail planned at street level"},
                    {"he": "מרכזי מסחר ושירותים ברמת אביב ובנמל", "en": "Retail centers in Ramat Aviv and the Port"}]},
            ],
        }, ensure_ascii=False),
    },
}
s, post = req("POST", "/wp-json/wp/v2/nadlan_project", body=post_body)
must(s, post, "post create")
POST_ID = post["id"]
LINK = post.get("link", "")
log("post", id=POST_ID, link=LINK, slug=post.get("slug"))

# ---- 4. bridge snippet: seed unregistered meta + glb + taxonomy + purge ----
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-aurelia-seed/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$out = array();
			$pid = isset( $b['post_id'] ) ? (int) $b['post_id'] : 0;
			if ( ! empty( $b['lint'] ) ) {
				try {
					token_get_all( (string) $b['lint'], TOKEN_PARSE );
					$out['lint'] = 'ok';
				} catch ( ParseError $e ) {
					return new WP_Error( 'lint', $e->getMessage(), array( 'status' => 400 ) );
				}
			}
			if ( $pid && ! empty( $b['meta'] ) && is_array( $b['meta'] ) ) {
				foreach ( $b['meta'] as $k => $v ) {
					$k = sanitize_key( $k ) === $k || 0 === strpos( $k, '_yoast' ) ? $k : '';
					if ( '' === $k ) { continue; }
					update_post_meta( $pid, $k, is_string( $v ) ? wp_slash( $v ) : $v );
					$out['meta'][ $k ] = is_string( $v ) ? strlen( $v ) : 1;
				}
			}
			if ( $pid && ! empty( $b['tax_city'] ) ) {
				$r = wp_set_object_terms( $pid, sanitize_text_field( (string) $b['tax_city'] ), 'nadlan_city', false );
				$out['tax'] = is_wp_error( $r ) ? $r->get_error_message() : count( (array) $r );
			}
			if ( ! empty( $b['file_b64'] ) && ! empty( $b['file_name'] ) ) {
				$up = wp_get_upload_dir();
				$dir = trailingslashit( $up['basedir'] ) . '2026/08';
				if ( ! wp_mkdir_p( $dir ) ) { return new WP_Error( 'mkdir', 'no dir', array( 'status' => 500 ) ); }
				$name = sanitize_file_name( (string) $b['file_name'] );
				$data = base64_decode( (string) $b['file_b64'], true );
				if ( false === $data ) { return new WP_Error( 'b64', 'bad payload', array( 'status' => 400 ) ); }
				$path = $dir . '/' . $name;
				file_put_contents( $path, $data );
				$out['file'] = array( 'url' => trailingslashit( $up['baseurl'] ) . '2026/08/' . $name, 'md5' => md5_file( $path ), 'bytes' => filesize( $path ) );
			}
			if ( ! empty( $b['purge'] ) ) {
				do_action( 'litespeed_purge_all' );
				$out['purged'] = 1;
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)

def snip_req(method, path, body=None):
    return req(method, f"/wp-json/code-snippets/v1/snippets{path}", body=body)

s, created = snip_req("POST", "", {"name": f"tmp-aurelia-seed-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, created, "bridge create")
BR_ID = created["id"]
s, upd = snip_req("PUT", f"/{BR_ID}", {"name": created["name"], "code": BRIDGE, "scope": "global", "active": False})
must(s, upd, "bridge update")
s, act = snip_req("PUT", f"/{BR_ID}/activate", {})
must(s, act, "bridge activate", ok=(200, 201))
log("bridge", id=BR_ID)

def seed(payload, what):
    payload["token"] = TOKEN
    s, r = req("POST", "/wp-json/nadlan-aurelia-seed/v1/apply", body=payload, timeout=180)
    must(s, r, what)
    return r

# GLB via bridge if REST media refused
if glb_pending:
    name, blob = glb_pending
    r = seed({"file_b64": base64.b64encode(blob).decode(), "file_name": name}, "glb write")
    assert r["file"]["md5"] == hashlib.md5(blob).hexdigest(), "GLB md5 mismatch"
    media[name] = {"id": 0, "url": r["file"]["url"]}
    log("glb", url=r["file"]["url"], md5=r["file"]["md5"])

GLB_URL = media["aurelia-tower-semantic-v2.glb"]["url"]

bridge_meta = {
    "project_3d_units": units_json,
    "project_model_glb": GLB_URL,
    "project_model_poster": U("aurelia-tower-sde-dov-hero.jpg"),
    "project_3d_image": U("aurelia-tower-sde-dov-hero.jpg"),
    "project_default_interior": U("aurelia-living-room-interior.jpg"),
    "project_3d_floor_height_m": "3.05",
    "project_floors": "47",
    "building": "Aurelia Tower",
    "project_subtitle": "מגדל 47 קומות ושני אגפי גן מול הים — בחירת דירה, תוכנית, נוף ופנייה במסע אחד",
    "project_hero_eyebrow": "רובע שדה דב · דקות מהים",
    "project_3d_avg_price_per_sqm": "99000",
    "project_3d_price_source_note": "מחירי הדירות המלאים מוצגים בכרטיס של כל דירה",
    "project_featured": "1",
    "geo_confidence": "site",
    "project_env_landmarks": json.dumps([
        {"label": {"he": "הים", "en": "The sea"}, "lat": 32.1057, "lng": 34.7710},
        {"label": {"he": "נמל תל אביב", "en": "Tel Aviv Port"}, "lat": 32.0967, "lng": 34.7754},
        {"label": {"he": "פארק הירקון", "en": "Yarkon Park"}, "lat": 32.0975, "lng": 34.7860},
        {"label": {"he": "ארובת רידינג", "en": "Reading"}, "lat": 32.0997, "lng": 34.7723},
    ], ensure_ascii=False),
    "project_3d_environment_json": json.dumps({
        "orientation": {"west": "orient_sea", "south": "orient_reading", "east": "orient_district", "north": "orient_district_north"}
    }, ensure_ascii=False),
    "_yoast_wpseo_title": "אורליה שדה דב Aurelia | דירות, תוכניות, נוף ומחירים | נדלן",
    "_yoast_wpseo_metadesc": "בחרו דירה באורליה שדה דב לפי קומה וכיוון, צפו בתוכנית, בנוף ובסיור הפנים, בדקו את מתקני הפרויקט והסביבה וקבלו תוכניות ומחירים מותאמים לדירה שבחרתם.",
    "_yoast_wpseo_focuskw": "אורליה שדה דב",
}
r = seed({"post_id": POST_ID, "meta": bridge_meta, "tax_city": "תל אביב יפו"}, "meta seed")
log("meta-seed", keys=len(r.get("meta", {})), tax=r.get("tax"))

# ---- 5. experience snippet (persistent) ----
with open(os.path.join(HERE, "snippet_experience.php"), encoding="utf-8") as f:
    EXP = f.read()
EXP = EXP.replace("{{POST_ID}}", str(POST_ID)).replace("{{PANO_LIVING_URL}}", U("aurelia-living-panorama-360.jpg"))
EXP_CODE = re.sub(r"^<\?php\s*", "", EXP, count=1)
r = seed({"lint": "<?php\n" + EXP_CODE}, "experience lint")
log("lint", result=r.get("lint"))
s, created2 = snip_req("POST", "", {"name": "x-aurelia-experience", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, created2, "experience create")
EXP_ID = created2["id"]
s, upd2 = snip_req("PUT", f"/{EXP_ID}", {"name": "x-aurelia-experience", "code": EXP_CODE, "scope": "global", "active": False})
must(s, upd2, "experience update")
s, act2 = snip_req("PUT", f"/{EXP_ID}/activate", {})
must(s, act2, "experience activate", ok=(200, 201))
log("experience-snippet", id=EXP_ID, sha256=hashlib.sha256(EXP_CODE.encode()).hexdigest()[:16])

# ---- 6. purge + delete bridge ----
seed({"purge": 1}, "cache purge")
s, deleted = snip_req("DELETE", f"/{BR_ID}", None)
log("bridge-delete", http=s)

# ---- 7. verify ----
time.sleep(2)
s, page = req("GET", f"{BASE}/projects/aurelia/", raw=True)
html = page.decode("utf-8", "replace") if isinstance(page, (bytes, bytearray)) else ""
checks = {
    "http": s,
    "bytes": len(page) if isinstance(page, (bytes, bytearray)) else 0,
    "h1_count": len(re.findall(r"<h1", html)),
    "payload": "NADLAN_SHOWROOM" in html,
    "glb": GLB_URL.split("/")[-1] in html,
    "units_in_payload": html.count('"hotspot_position"'),
    "adapter": "nlaur-overlay" in html or "nlaur-dot" in html or "nlaur" in html,
    "title": (re.search(r"<title>(.*?)</title>", html, re.S) or [None, ""])[1] if "<title>" in html else "",
    "yoast_desc": "בחרו דירה באורליה" in html,
    "notice_removed": "nl-projnotice" not in html,
    "aurelia_name": "אורליה שדה דב" in html,
}
log("verify-page", **{k: (v if not isinstance(v, str) else v[:120]) for k, v in checks.items()})

for probe in ("/projects/rainbow-tel-aviv/", "/projects/h-infinity-somail-tel-aviv/", "/"):
    s2, body = req("GET", BASE + probe, raw=True)
    log("spot", path=probe, http=s2, bytes=len(body) if isinstance(body, (bytes, bytearray)) else 0)

s, h2 = req("GET", "/wp-json/nadlan/v1/health")
log("health-after", version=h2.get("version"), status=h2.get("status"))

with open(os.path.join(HERE, "deploy100-evidence.json"), "w", encoding="utf-8") as f:
    json.dump({"post_id": POST_ID, "link": LINK, "media": {k: v["url"] for k, v in media.items()},
               "experience_snippet_id": EXP_ID, "checks": checks, "steps": EVIDENCE["steps"]}, f, ensure_ascii=False, indent=1)
print("DONE post_id=%s link=%s" % (POST_ID, LINK))
