# -*- coding: utf-8 -*-
"""HAD-787: six opening questions of the team for the questions blocks of /sde-dov/ and /projects/hamedina/.
Ben's word, 21.11.2026 (through the coordinator; his order of 18.11 in this session asked for opening discussions on places such as
Sde Dov): publish, signed openly "צוות נדל"ן", with the prices written as ranges from public sources. No invented visitor, no invented
answer; every post ends with an open question to readers.
EVERY FIGURE IS READ AGAIN ON THE LIVE PAGE IT COMES FROM before anything is written: a missing figure stops the run.

  python scripts/project-stage/forum_seed_place.py check     only read the figures on the live pages
  python scripts/project-stage/forum_seed_place.py seed      check, then write the posts that are not there yet (by title) with their place tag
  python scripts/project-stage/forum_seed_place.py unseed    remove these posts (stops if another member already answered one)
Never while a release runner is active (docs/coordination/claude-codex.md)."""
import html, json, os, re, secrets, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
if MODE not in ("check", "seed", "unseed"):
    raise SystemExit("usage: forum_seed_place.py check|seed|unseed")
sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://nad-lan.co.il"
TEAM = "forum-team@nad-lan.co.il"

# place, title, body, [ (page, the words that must be on that page today) ]
T = [
 ("sde-dov", "כמה דירות מתוכננות בשדה דב, ובאיזה חלק של הרובע?",
  "לפי התכנון, במתחם הצפון מתוכננות כ-4,000 יחידות דיור ובמתחם המרכז כ-7,100. במרכז מתוכננים גם כ-65,000 מ\"ר מסחר וכ-148,000 מ\"ר תעסוקה. "
  "מי שבודק דירה ברובע: באיזה מתחם אתם מתעניינים, ומה הכריע אצלכם?",
  [("/sde-dov/tzafon/", ["כ-4,000 יחידות דיור"]), ("/sde-dov/merkaz/", ["כ-7,100 יחידות דיור", "כ-65,000 מ\"ר מסחר", "כ-148,000 מ\"ר תעסוקה"])]),
 ("sde-dov", "מה יהיה בפארק החוף של שדה דב, וכמה הוא קרוב לבתים?",
  "פארק החוף מתוכנן על כ-240 דונם, לאורך החזית המערבית של הרובע וליד קו החוף של צפון תל אביב. הוא העוגן הירוק הגדול ברובע. "
  "למי שמשווה בין פרויקטים: עד כמה הקרבה לפארק ולים משפיעה על הבחירה שלכם, ועל המחיר שאתם מוכנים לשלם?",
  [("/sde-dov/parks/", ["כ-240 דונם", "לאורך החזית המערבית של הרובע", "קו החוף של צפון תל אביב"])]),
 ("sde-dov", "כ-3,700 חדרי מלון בשדה דב: יתרון או חיסרון למי שקונה דירה?",
  "ברובע מתוכננים כ-3,700 חדרי מלון, בהיקף של כ-200,000 מ\"ר מלונאות. מתוכם כ-1,700 חדרים במתחם המרכז. "
  "יש מי שרואה בזה חיים ומסחר ליד הבית, ויש מי שחושש מעומס. איך אתם רואים את זה?",
  [("/sde-dov/hotels/", ["כ-3,700 חדרי מלון", "כ-200,000 מ\"ר מלונאות"]), ("/sde-dov/merkaz/", ["כ-1,700 חדרי מלון"])]),
 ("hamedina", "מתי צפויה מסירת הדירות במגדלי כיכר המדינה?",
  "מועד אכלוס רשמי לא פורסם. לפי פרסומים מאוקטובר 2026, טופס 4 צפוי עד סוף 2026 או בתחילת 2027, ומסירת הדירות בין הרבעון הראשון של 2027 למאי 2027. "
  "השלמת הקמת המגדלים פורסמה באוקטובר 2026. המועד המחייב לכל דירה הוא זה שכתוב בהסכם עם המוכר. מי שקנה או מתעניין: איזה מועד נמסר לכם?",
  [("/projects/hamedina/", ["מועד אכלוס רשמי לא פורסם", "טופס 4 צפוי עד סוף 2026 או בתחילת 2027", "מסירת הדירות בין הרבעון הראשון של 2027 למאי 2027",
                            "השלמת הקמת המגדלים פורסמה ב-10.2026", "המועד שבהסכם עם המוכר"])]),
 ("hamedina", "מה טווח המחירים במגדלי כיכר המדינה, לפי מקורות גלויים?",
  "לפי מקורות גלויים: הערכות שפורסמו באוקטובר 2026 מדברות על כ-65,000 ₪ למ\"ר בממוצע במגדלים. בעסקאות שדווחו ב-2024 בקומות 38 ו-39 נמכרו דירות 4 חדרים "
  "בשטח 140 מ\"ר ב-9.58 עד 10.63 מיליון ₪. בשכונה שסביב הכיכר, חציון העסקאות לדירת 4 חדרים ברבעון הראשון של 2026 היה 6.84 מיליון ₪. "
  "המחיר של כל דירה נקבע בהסכם עם המוכר. באיזה טווח מחירים נתקלתם?",
  [("/projects/hamedina/", ["65,000 ₪ למ\"ר", "ההערכות שפורסמו באוקטובר 2026", "בקומות 38-39 נרשמו עסקאות של 9.58 עד 10.63 מיליון ₪", "4 חדרים בשטח 140 מ\"ר",
                            "מ-4.2024 עד 12.2024", "ברבעון הראשון של 2026", "6.84 מיליון"])]),
 ("hamedina", "שלושה מגדלים ו-453 דירות בכיכר המדינה: מה חשוב לבדוק לפני שבוחרים מגדל וקומה?",
  "בפרויקט שלושה מגדלי מגורים, שניים של 40 קומות ואחד של 37, ובהם 453 דירות. המגדלים עומדים בתוך טבעת רחוב ה' באייר, לצד פארק ציבורי מתוכנן של כ-40 דונם. "
  "הבנייה בידי אלקטרה ואשטרום. מי שכבר בחר דירה: מה הכריע אצלכם, המגדל, הקומה, הכיוון או התכנון?",
  [("/projects/hamedina/", ["שלושה מגדלי מגורים ובהם 453 דירות", "40, 40 ו-37 קומות", "טבעת רחוב ה' באייר", "פארק ציבורי מתוכנן של כ-40 דונם", "אלקטרה ואשטרום"])]),
]
for t in T:  # Ben: no long dashes
    for s in t[1:3]:
        assert "—" not in s and "–" not in s and " - " not in s, s[:40]


def norm(s):
    s = html.unescape(s)
    for a, b in (("״", '"'), ("׳", "'"), ("“", '"'), ("”", '"'), ("’", "'"), ("‏", ""), ("‎", ""), (" ", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", "", s)


_pages = {}
def page(path):
    if path not in _pages:
        raw = urllib.request.urlopen(urllib.request.Request(BASE + path + "?t=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
        raw = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
        _pages[path] = norm(re.sub(r"<[^>]+>", " ", raw))
    return _pages[path]


bad = 0
for place, title, body, facts in T:
    for path, words in facts:
        for w in words:
            ok = norm(w) in page(path)
            bad += 0 if ok else 1
            print(("OK   " if ok else "MISS ") + path + " | " + w)
print("figures: %d checked, %d missing" % (sum(len(w) for t in T for _, w in t[3]), bad))
if bad:
    raise SystemExit("STOP: a figure is not on its live page today; nothing was written")
if MODE == "check":
    raise SystemExit(0)

_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "forum_seed_place_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-forum-place-seed/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nlf_t' ) || ! function_exists( 'nlfp2_t' ) ) { return array( 'err' => 'forum or place module not loaded' ); }
			nlfp2_install();
			if ( ! nlfp2_ready() ) { return array( 'err' => 'place table not ready' ); }
			$mt = nlf_t( 'members' ); $tt = nlf_t( 'topics' ); $rt = nlf_t( 'replies' ); $pt = nlfp2_t();
			$mid = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $mt WHERE contact = %s", (string) $b['team'] ) );
			if ( ! $mid ) { return array( 'err' => 'the team member is missing (run forum_seed_team.py seed first)' ); }
			$out = array( 'made' => array(), 'kept' => array(), 'removed' => array() );
			$i = 0; $n = count( (array) $b['topics'] );
			foreach ( (array) $b['topics'] as $t ) {
				list( $place, $title, $body ) = $t;
				if ( ! nlfp2_key_ok( $place ) ) { return array( 'err' => 'unknown place ' . $place ); }
				$id = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $tt WHERE member_id = %d AND title = %s", $mid, $title ) );
				if ( 'unseed' === $b['mode'] ) {
					if ( ! $id ) { continue; }
					if ( (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $rt WHERE topic_id = %d AND member_id <> %d", $id, $mid ) ) > 0 ) { $out['kept'][] = $id; continue; }
					$wpdb->delete( $rt, array( 'topic_id' => $id ) ); $wpdb->delete( $pt, array( 'topic_id' => $id ) ); $wpdb->delete( $tt, array( 'id' => $id ) );
					$out['removed'][] = $id; continue;
				}
				if ( $id ) { $wpdb->replace( $pt, array( 'topic_id' => $id, 'place' => $place ) ); $out['kept'][] = $id; $i++; continue; }
				$at = gmdate( 'Y-m-d H:i:s', time() - 60 * 3 * $i ); $i++; // the first of each place is the newest, so it is the first row
				$wpdb->insert( $tt, array( 'cat' => 'general', 'kind' => 'question', 'title' => $title, 'body' => $body, 'member_id' => $mid, 'city' => 'תל אביב', 'status' => 'live',
					'reply_count' => 0, 'view_count' => 0, 'thanks_count' => 0, 'body_hash' => hash( 'sha256', $body ), 'created_at' => $at, 'last_at' => $at ) );
				$id = (int) $wpdb->insert_id;
				if ( $id ) { $wpdb->replace( $pt, array( 'topic_id' => $id, 'place' => $place ) ); $out['made'][] = array( $id, $place ); }
			}
			foreach ( array_keys( nlfp2_places() ) as $k ) { nlfp2_purge_page( $k ); }
			do_action( 'litespeed_purge_all' );
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-forum-place-seed-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-forum-place-seed/v1/run", {"token": TOKEN, "mode": MODE, "team": TEAM, "topics": [list(t[:3]) for t in T]}, timeout=120); must(s, r, "run")
    print("[place seed]", json.dumps(r, ensure_ascii=False))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
