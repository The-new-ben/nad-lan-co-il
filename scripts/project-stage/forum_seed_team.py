# -*- coding: utf-8 -*-
"""HAD-787 opening discussions by the forum team (Ben, 18.11.2026 night: "תיצור עוד דיונים... שימשוך אנשים... קניית דירה, אזורים,
דירה מקבלן"). Every discussion is signed by ONE honest account, "צוות נדל"ן" (contact forum-team@nad-lan.co.il), written in a plain
human voice, built on questions people really type into Google (docs/research/2026-11-18-arena/manual-2026-11-18/NOTES.md) and on
public numbers (Tax Authority averages, data.nadlan.gov.il, version 20-08-2026). No invented person, apartment, price or reply.

  python scripts/project-stage/forum_seed_team.py seed     write the team member and the discussions (idempotent: removes the old ones first)
  python scripts/project-stage/forum_seed_team.py unseed   remove them (stops if a real member already answered one)
Never run while a release runner is active (docs/coordination/claude-codex.md)."""
import json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
if MODE not in ("seed", "unseed"):
    raise SystemExit("usage: forum_seed_team.py seed|unseed")
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "forum_seed_team_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]

TEAM = ("forum-team@nad-lan.co.il", 'צוות נדל"ן')

# cat, city, title, body
T = [
 ("general", "רמת גן",
  "רמת גן או גבעתיים: כמעט 700 אלף שקל הבדל על אותה דירת 4 חדרים. על מה משלמים?",
  "לפי נתוני רשות המסים (עדכון אוגוסט 2026), דירת 4 חדרים נמכרה בשנה האחרונה בממוצע ב-3,314,200 שקל ברמת גן, וב-3,999,300 שקל בגבעתיים. "
  "הערים צמודות, ובין חלק מהשכונות יש כמה דקות הליכה. אז מה עושה את ההבדל? בתי ספר, גיל הבניינים, תחבורה, התחדשות עירונית, או פשוט השם? "
  "מי שגר באחת מהן, או התלבט בין שתיהן לפני שקנה: מה הכריע אצלכם, והאם הייתם בוחרים אותו דבר היום?"),
 ("law", "",
  "קיבלתם מפתח מהקבלן? מה בדקתם ביום המסירה, ומה גיליתם רק אחר כך",
  "ביום המסירה מגיעים עם פרוטוקול מוכן, ויש לחץ לחתום מהר. כל ליקוי שלא נכתב שם הופך אחר כך לוויכוח. "
  "לפי חוק המכר (דירות) יש תקופת בדק של שנה עד שבע שנים, לפי סוג הליקוי, ואחריה עוד שלוש שנים של אחריות. ובכל זאת, הרבה יותר פשוט כשהליקוי כתוב כבר בפרוטוקול. "
  "מי שעבר מסירה: הבאתם בודק מוסמך? מה הוא מצא שלא הייתם רואים לבד? ומה הייתם עושים אחרת?"),
 ("law", "",
  "המסירה מתעכבת וטופס 4 עוד לא הגיע. מישהו קיבל פיצוי בלי ללכת לבית משפט?",
  "בחוזה כתוב תאריך, ואז מגיע מכתב מהקבלן על \"עיכובים שאינם בשליטתו\". "
  "חוק המכר (דירות) קובע פיצוי על איחור במסירה לפי שכר דירה של דירה דומה, ואחרי שמונה חודשי איחור הפיצוי גדל. "
  "בפועל, איך זה עבד אצלכם? הקבלן שילם מעצמו או קיזז מהתשלום האחרון? הייתם צריכים עורך דין? ומה עשיתם עם שכר הדירה בינתיים?"),
 ("general", "",
  "מבצע 20/80 או הלוואת קבלן: כמה זה באמת שווה בכסף?",
  "כמעט כל פרויקט חדש מציע היום 20 אחוז עכשיו ו-80 במסירה, או הלוואה של הקבלן בלי ריבית. על הנייר זה נשמע כמו הנחה. "
  "השאלה האמיתית היא כמה עולה הכסף שלא שילמתם עד המסירה, והאם המחיר במבצע זהה למחיר בלי מבצע. "
  "מי שקנה במבצע כזה: ביקשתם מהקבלן מחיר בלי המבצע לפני שחתמתם? כמה הוא היה? ויועצי משכנתאות כאן: איך אתם מחשבים את זה ללקוח?"),
 ("build", "",
  "קונים דירה ישנה ומשפצים: מה נכנס בשיפוץ מלא, ולמה ההצעות כל כך רחוקות זו מזו?",
  "שאלה שחוזרת אצל הרבה קונים של דירה יד שנייה: מקבלים שלוש הצעות לשיפוץ מלא של אותה דירה, והפער ביניהן כמעט כפול. "
  "בעלי מקצוע: מה אתם כוללים במחיר, ומה כמעט תמיד נשאר מחוץ להצעה ומפתיע את הלקוח באמצע? חשמל חדש? צנרת מתחת לריצוף? אלומיניום? "
  "ומי ששיפץ לאחרונה: כמה זה יצא בסוף לעומת ההצעה הראשונה?"),
 ("law", "",
  "מוכרים את הדירה היחידה ורוצים פטור ממס שבח: איפה נתקעתם?",
  "על הנייר זה פשוט: דירה יחידה, בבעלות של 18 חודשים לפחות, ובלי מכירה אחרת בפטור ב-18 החודשים האחרונים. "
  "בפועל יש מקרים פחות פשוטים: חלק בדירה של ההורים, ירושה, קנייה של דירה חדשה לפני שהישנה נמכרה. "
  "מי שמכר לאחרונה: איך עבר אצלכם מול רשות המסים? ועורכי דין ושמאים בפורום: מה הטעות שאתם רואים הכי הרבה?"),
 ("loans", "",
  "דירה ראשונה: כמה הון עצמי צריך באמת, מעבר ל-25 האחוז?",
  "בדירה ראשונה הבנק מממן עד 75 אחוז משווי הדירה, ולכן מדברים תמיד על 25 אחוז הון עצמי. "
  "אבל יש עוד הוצאות שלא נכנסות למשכנתא: עורך דין, שמאי, יועץ משכנתאות, הובלה, ולפעמים גם מס רכישה ושיפוץ קטן. "
  "מי שקנה בשנתיים האחרונות: כמה כסף יצא לכם בפועל מעבר להון העצמי? ומה הייתם שמים בצד מראש אם הייתם קונים היום?"),
]

for t in T:  # Ben: no long dashes
    for s in t[2:]:
        assert "—" not in s and "–" not in s and " - " not in s, s[:40]

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-forum-team/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nlf_t' ) ) { return array( 'err' => 'forum module not loaded' ); }
			$mt = nlf_t( 'members' ); $tt = nlf_t( 'topics' ); $rt = nlf_t( 'replies' );
			$c = (string) $b['team'][0];
			$mid = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $mt WHERE contact = %s", $c ) );
			$gone = 0;
			if ( $mid ) {
				$real = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $rt WHERE member_id <> %d AND topic_id IN (SELECT id FROM $tt WHERE member_id = %d)", $mid, $mid ) );
				if ( $real > 0 ) { return array( 'err' => 'stopped: ' . $real . ' answers by other members sit on team discussions; nothing was deleted' ); }
				$gone = (int) $wpdb->query( $wpdb->prepare( "DELETE FROM $tt WHERE member_id = %d", $mid ) );
			}
			if ( 'unseed' === $b['mode'] ) {
				if ( $mid ) { $wpdb->query( $wpdb->prepare( "DELETE FROM $mt WHERE id = %d", $mid ) ); }
				do_action( 'litespeed_purge_all' ); return array( 'removed_topics' => $gone );
			}
			$now = gmdate( 'Y-m-d H:i:s' );
			if ( ! $mid ) {
				$wpdb->insert( $mt, array( 'display_name' => (string) $b['team'][1], 'contact' => $c, 'contact_hash' => nlf_contact_hash( $c, nlf_key() ), 'role_label' => '', 'trade' => '',
					'approved_posts' => 20, 'status' => 'ok', 'session_hash' => '', 'created_at' => $now, 'last_seen' => $now ) );
				$mid = (int) $wpdb->insert_id;
			}
			$made = array(); $i = 0;
			foreach ( (array) $b['topics'] as $t ) {
				list( $cat, $city, $title, $body ) = $t;
				$at = gmdate( 'Y-m-d H:i:s', time() - 60 * 7 * ( count( $b['topics'] ) - $i ) ); $i++;
				$wpdb->insert( $tt, array( 'cat' => $cat, 'kind' => 'question', 'title' => $title, 'body' => $body, 'member_id' => $mid, 'city' => $city, 'status' => 'live',
					'reply_count' => 0, 'view_count' => 0, 'thanks_count' => 0, 'body_hash' => hash( 'sha256', $body ), 'created_at' => $at, 'last_at' => $at ) );
				$made[] = (int) $wpdb->insert_id;
			}
			do_action( 'litespeed_purge_all' );
			return array( 'team_member' => $mid, 'replaced' => $gone, 'topics' => $made );
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)

s, c = snip("POST", "", {"name": f"tmp-forum-team-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-forum-team/v1/run", {"token": TOKEN, "mode": MODE, "team": TEAM, "topics": T}, timeout=120); must(s, r, "run")
    print("[team]", json.dumps(r, ensure_ascii=False))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
