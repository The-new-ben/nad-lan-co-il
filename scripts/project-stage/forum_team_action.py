# -*- coding: utf-8 -*-
"""HAD-787, Ben's order of 21.11.2026 evening (through the coordinator): "add some action" in the forum from the team, openly as
"צוות נדל"ן" and never as a pretend visitor: (a) a short reply to Alona Mor in discussion 6, (b) one more useful fact from our own
pages on each of the six opening questions (a second voice, signed by the team), (c) four practical threads on what buyers ask.
EVERY FACT IS READ AGAIN ON THE LIVE PAGE IT COMES FROM before anything is written; a missing fact stops the run. Nothing on soil
or contamination; no project or company next to a negative topic; no long dashes; each post ends with a real question.

  python scripts/project-stage/forum_team_action.py check    only read the facts on the live pages
  python scripts/project-stage/forum_team_action.py post     check, then write what is not there yet (by text)
Never while a release runner is active (docs/coordination/claude-codex.md)."""
import html, json, os, re, secrets, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
if MODE not in ("check", "post"):
    raise SystemExit("usage: forum_team_action.py check|post")
sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://nad-lan.co.il"
TEAM = "forum-team@nad-lan.co.il"
G = "/buying-apartment/"
K = "/projects/hamedina/"

# the reply to Alona (discussion 6). The card facts are the product's own: inc/pro-forum-card.php (name, trade, city, phone; shown after approval)
ALONA = (6, "היי אלונה, ברוכה הבאה. לא צריך לשלוח אנשים לגוגל. מתחת לתיבת התשובה, ליד השם שלך, יש קישור \"אני בעל מקצוע\". "
            "לוחצים, ממלאים שם, מקצוע, עיר וטלפון, ואחרי אישור קצר שלנו הכרטיס שלך מופיע ליד כל תשובה שתכתבי כאן. "
            "אם תבחרי להציג את הטלפון, פונים אלייך ישר ולא דרך האתר. באותו מקום יש גם \"תמונת פרופיל\", שווה להעלות אחת. "
            "ועל הדרך, איזה סוג עבודות את הכי אוהבת לקחת?")

# a second voice on the six opening questions: (title of the discussion, text, [ (page, words that must be on it today) ])
R = [
 ("כמה דירות מתוכננות בשדה דב, ובאיזה חלק של הרובע?",
  "עוד פרט מהדף של מתחם הצפון: לצד הדירות מתוכננים שם גם כ-26,000 מ\"ר מסחר וכ-30,000 מ\"ר תעסוקה. כלומר רחוב עם חנויות ומשרדים ליד הבית, לא שכונת שינה. "
  "מי שגר היום מעל מסחר פעיל: זה מפריע לכם או דווקא נוח?",
  [("/sde-dov/tzafon/", ["כ-26,000 מ\"ר מסחר", "כ-30,000 מ\"ר תעסוקה"])]),
 ("מה יהיה בפארק החוף של שדה דב, וכמה הוא קרוב לבתים?",
  "חוץ מפארק החוף מתוכנן גם פארק על התוואי של מסלול ההמראה הישן, ופארק לינארי שמחבר את מזרח העיר לים. ולגבי הכסף: בתחילת 2026 המחיר הממוצע ברובע היה סביב "
  "81,000 ש\"ח למ\"ר, ודירות צמודות לשטח ירוק או עם נוף לים עשויות להגיע עד כ-100,000. הייתם משלמים את הפער הזה על נוף?",
  [("/sde-dov/parks/", ["פארק מסלול על תוואי מסלול ההמראה ההיסטורי", "פארק לינארי המחבר את מזרח העיר לים", "כ-81,000 ש\"ח", "עד כ-100,000 ש\"ח למ\"ר"])]),
 ("כ-3,700 חדרי מלון בשדה דב: יתרון או חיסרון למי שקונה דירה?",
  "פירוט לפי מתחמים: כ-1,700 חדרים במרכז וכ-1,320 בצפון. הרובע יושב על כ-2 ק\"מ של חוף, ליד נמל תל אביב ומעגנת רדינג. "
  "מי שגר היום ליד מלון גדול, איך זה מרגיש בסופי שבוע?",
  [("/sde-dov/hotels/", ["כ-1,700 חדרים", "כ-1,320 חדרים", "כ-2 ק\"מ של חוף", "מעגנת רדינג"])]),
 ("מתי צפויה מסירת הדירות במגדלי כיכר המדינה?",
  "פרט שעוזר לקרוא את לוח הזמנים: היתר הבנייה ניתן ב-12.2022, וגמר השלד היה ב-23.4.2026. השלמת הבנייה היא שלב בבנייה, לא מסירה. ביניהם יש עוד טופס 4. "
  "שווה לשאול את המוכר מה כתוב בהסכם על איחור. מה אמרו לכם?",
  [(K, ["היתר בנייה 12.2022", "גמר שלד ב-23.4.2026", "זהו שלב בבנייה, בנפרד ממסירת הדירות"])]),
 ("מה טווח המחירים במגדלי כיכר המדינה, לפי מקורות גלויים?",
  "עוד שני מספרים מאותם מקורות, להשוואה. חציון השכונה ברבעון הראשון של 2026 היה 4.94 מיליון ₪ לדירת 3 חדרים ו-8.46 מיליון לדירת 5 חדרים. "
  "ובעסקאות של קומות 38 ו-39 יוצא כ-68,000 עד 76,000 ₪ למ\"ר. מה ראיתם אתם במודעות?",
  [(K, ["4.94 מיליון ₪ לדירת 3 חדרים", "8.46 מיליון ל- 5 חדרים", "כ- 68,000 עד 76,000 ₪ למ\"ר"])]),
 ("שלושה מגדלים ו-453 דירות בכיכר המדינה: מה חשוב לבדוק לפני שבוחרים מגדל וקומה?",
  "טיפ מעשי: בדף הפרויקט אפשר לבחור מגדל, קומה ודירה לפי כיוון, ולראות את תוכנית הקומה ואת הנוף מהחלונות. המגדלים בנויים עם סיבוב עדין בין הקומות, "
  "אז כדאי לבדוק את הנוף בקומה עצמה ולא להניח לפי קומה אחרת. לאיזה כיוון הייתם רוצים את הסלון?",
  [(K, ["בחרו מגדל, קומה ודירה לפי כיוון", "את תוכנית הקומה", "את הנוף מהחלונות", "סיבוב עדין בין הקומות"])]),
]

# four practical threads: (category, title, text, facts)
T = [
 ("law", "לפני שחותמים עם קבלן: מה בודקים בעצמכם, ומה משאירים לעורך הדין?",
  "כמה דברים אפשר לבדוק לבד, עוד לפני הפגישה. בפנקס הקבלנים רואים אם הקבלן רשום ומה הסיווג שלו. לפי חוק המכר, הקבלן לא מקבל יותר מ-7% מהמחיר בלי בטוחה "
  "כמו ערבות או פוליסה. עורך דין מטעמכם עולה בדרך כלל 0.5% עד 1% מהמחיר ועוד מע\"מ, וכדאי להביא אותו לפני זיכרון הדברים ולא אחריו. "
  "מה אתם בדקתם לפני החתימה, ומה גיליתם מאוחר מדי?",
  [(G, ["פנקס הקבלנים", "האם הוא רשום בענף הבנייה, מה הסיווג שלו", "לא מקבל יותר מ־7% מהמחיר בלי בטוחה כמו ערבות או פוליסה", "עורך דין מטעמכם 0.5% עד 1% מהמחיר ועוד מע\"מ", "עורך דין מטעמכם, לפני זיכרון דברים"])]),
 ("law", "הצמדה למדד תשומות הבנייה: כמה מהמחיר באמת צמוד?",
  "הרבה קונים בטוחים שכל המחיר צמוד. בחוזה שנחתם מ-7.7.2022 זה לא כך: 20% שמשלמים בחתימה לא צמודים בכלל, ומכל תשלום אחר מותר להצמיד עד מחצית, ורק עד מועד המסירה שבחוזה. "
  "לפי הפרסום של ספטמבר 2026 המדד עלה ב-3.6% ב-12 חודשים. בחשבון גס, על דירה של 2,000,000 ש\"ח ועלייה כזו בשנה, ההבדל בין הכול צמוד לחצי צמוד הוא עשרות אלפי שקלים. "
  "בדקתם איך זה כתוב בחוזה שלכם?",
  [("/new-projects/construction-input-index/", ["בחוזה מ־7.7.2022: 20% מהמחיר המשולמים בחתימה אינם צמודים", "מותר להצמיד עד מחצית", "עד מועד המסירה שבחוזה", "9.2026", "שינוי ב־12 חודשים: 3.6%"])]),
 ("law", "מפרט בדירה מקבלן: מה חייב להיות כתוב בו?",
  "המפרט הוא מסמך חובה. היזם מצרף אותו לחוזה כשהוא חתום, בטופס קבוע, וממלא כל פריט במדויק. כל תיקון במפרט צריך חתימה של שני הצדדים. "
  "ומה שפחות מוכר: יזם שלא מסר מפרט כנדרש נחשב כמי שהתחייב לאיכות גבוהה. לכן קוראים אותו שורה שורה לפני החתימה, לא אחריה. "
  "על איזה סעיף במפרט התווכחתם עם הקבלן?",
  [(G, ["המפרט הוא מסמך חובה", "היזם מצרף אותו לחוזה, חתום", "בטופס קבוע", "ממלא כל פריט במדויק", "כל תיקון בו טעון חתימה של שני הצדדים", "ייחשב כמי שהתחייב לאיכות גבוהה"])]),
 ("general", "אותה דירה בשתי קומות שונות: איך משווים?",
  "ההבדל בין שתי קומות הוא לא רק המחיר. קודם בודקים מה רואים מהחלון בכל אחת, כי קומה אחת יכולה להיות מעל הבניין שממול והשנייה בדיוק מולו. "
  "בדף של ריינבו תל אביב אצלנו בוחרים קומה ורואים את הנוף ממנה, וזה עוזר להבין את ההבדל עוד לפני משרד המכירות. אחר כך שואלים כמה עולה כל קומה נוספת. "
  "כמה הייתם מוסיפים על עוד חמש קומות?",
  [("/projects/rainbow-tel-aviv/", ["בוחרים קומה ורואים את הנוף"])]),
]
for s in [ALONA[1]] + [x[1] for x in R] + [x[1] for x in T] + [x[2] for x in T]:  # Ben: no long dashes
    assert "—" not in s and "–" not in s and " - " not in s, s[:40]


def norm(s):
    s = html.unescape(s)
    for a, b in (("״", '"'), ("׳", "'"), ("“", '"'), ("”", '"'), ("’", "'"), ("‏", ""), ("‎", ""), (" ", " "), ("־", "-")):
        s = s.replace(a, b)
    return re.sub(r"\s+", "", s)


_pages = {}
def page(path):
    if path not in _pages:
        raw = urllib.request.urlopen(urllib.request.Request(BASE + path + "?t=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
        raw = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
        _pages[path] = norm(re.sub(r"<[^>]+>", " ", raw))
    return _pages[path]


bad = n = 0
for item in R + [t[1:] for t in T]:
    for path, words in item[2]:
        for w in words:
            ok = norm(w) in page(path); n += 1; bad += 0 if ok else 1
            print(("OK   " if ok else "MISS ") + path + " | " + w)
print("facts: %d checked, %d missing" % (n, bad))
if bad:
    raise SystemExit("STOP: a fact is not on its live page today; nothing was written")
if MODE == "check":
    raise SystemExit(0)

_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "forum_team_action_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-forum-team-action/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nlf_t' ) || ! function_exists( 'nlf_on_reply_live' ) ) { return array( 'err' => 'forum module not loaded' ); }
			$mt = nlf_t( 'members' ); $tt = nlf_t( 'topics' ); $rt = nlf_t( 'replies' );
			$mid = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $mt WHERE contact = %s", (string) $b['team'] ) );
			if ( ! $mid ) { return array( 'err' => 'the team member is missing' ); }
			$out = array( 'replies' => array(), 'topics' => array(), 'kept' => 0, 'missing' => array() );
			$reply = function ( $tid, $body ) use ( $wpdb, $rt, $tt, $mid, &$out ) {
				$t = $wpdb->get_row( $wpdb->prepare( "SELECT id, status FROM $tt WHERE id = %d", (int) $tid ), ARRAY_A );
				if ( ! $t || 'live' !== $t['status'] ) { $out['missing'][] = (int) $tid; return; }
				$hash = hash( 'sha256', $body );
				if ( (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $rt WHERE topic_id = %d AND member_id = %d AND body_hash = %s", (int) $tid, $mid, $hash ) ) > 0 ) { $out['kept']++; return; }
				$wpdb->insert( $rt, array( 'topic_id' => (int) $tid, 'member_id' => $mid, 'body' => $body, 'status' => 'live', 'body_hash' => $hash, 'created_at' => nlf_now_sql() ) );
				$rid = (int) $wpdb->insert_id;
				if ( $rid ) { nlf_on_reply_live( $rid ); $out['replies'][] = array( (int) $tid, $rid ); } // the forum's own effects: the count, the last time, the notices to who follows
			};
			$reply( (int) $b['alona'][0], (string) $b['alona'][1] );
			foreach ( (array) $b['answers'] as $a ) {
				$tid = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $tt WHERE member_id = %d AND title = %s", $mid, (string) $a[0] ) );
				if ( ! $tid ) { $out['missing'][] = (string) $a[0]; continue; }
				$reply( $tid, (string) $a[1] );
			}
			$i = 0;
			foreach ( (array) $b['topics'] as $t ) {
				list( $cat, $title, $body ) = $t;
				if ( (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $tt WHERE member_id = %d AND title = %s", $mid, $title ) ) > 0 ) { $out['kept']++; continue; }
				$at = gmdate( 'Y-m-d H:i:s', time() - 60 * 2 * $i ); $i++;
				$wpdb->insert( $tt, array( 'cat' => $cat, 'kind' => 'question', 'title' => $title, 'body' => $body, 'member_id' => $mid, 'city' => '', 'status' => 'live',
					'reply_count' => 0, 'view_count' => 0, 'thanks_count' => 0, 'body_hash' => hash( 'sha256', $body ), 'created_at' => $at, 'last_at' => $at ) );
				if ( $wpdb->insert_id ) { $out['topics'][] = (int) $wpdb->insert_id; }
			}
			if ( function_exists( 'nlfp2_places' ) ) { foreach ( array_keys( nlfp2_places() ) as $k ) { nlfp2_purge_page( $k ); } }
			do_action( 'litespeed_purge_all' );
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-forum-team-action-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    body = {"token": TOKEN, "team": TEAM, "alona": list(ALONA), "answers": [[x[0], x[1]] for x in R], "topics": [list(t[:3]) for t in T]}
    s, r, _ = req("POST", "/wp-json/nadlan-forum-team-action/v1/run", body, timeout=180); must(s, r, "run")
    print("[team action]", json.dumps(r, ensure_ascii=False))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
