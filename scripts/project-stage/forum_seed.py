# -*- coding: utf-8 -*-
"""HAD-726 sample discussions for the professionals' forum, by Ben's order (12.11.2026: "תכניס לי כמה הודעות לפורום, אני
אמחוק אותם יותר מאוחר... שיתוף פעולה בין קבלנים, חברות גמר, מעצבים... שיראה אמיתי לגמרי").
Every sample member is on example.invalid with the address prefix "seed-" (no mail is ever delivered), none is linked to a
register card (pro_id stays empty), and `unseed` removes them and everything they wrote, in one run.

  python scripts/project-stage/forum_seed.py seed      write the members, the discussions and the answers (idempotent: unseed first)
  python scripts/project-stage/forum_seed.py unseed    remove all of it
  python scripts/project-stage/forum_seed.py video-off|video-on   the sample members' "call me by video" switch (off since 18.11.2026)
  python scripts/project-stage/forum_seed.py cookies   new session cookies for two sample members (for the two-browser video test)"""
import json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MODE = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
if MODE not in ("seed", "unseed", "cookies", "video-off", "video-on"):
    raise SystemExit("usage: forum_seed.py seed|unseed|cookies|video-off|video-on")
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "forum_seed_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]

# key, display name, trade (inc/pro-forum-trades.php), role
PEOPLE = [
    ("avi", "אבי מזרחי", "kablan", "pro"), ("yossi", "יוסי אלמוג", "finishing", "pro"), ("ronit", "רונית שגב", "interior_designer", "pro"),
    ("dana", "דנה ברק", "architect", "pro"), ("muhamad", "מוחמד חטיב", "skeleton", "pro"), ("eli", "אלי פרץ", "windows", "pro"),
    ("shiran", "שירן כהן", "kitchens", "pro"), ("omer", "עומר לוי", "electrician", "pro"), ("gilad", "גלעד רוזן", "tama", "pro"),
    ("maya", "מאיה דהן", "project_manager", "pro"), ("nir", "ניר אשכנזי", "waterproofing", "pro"), ("tal", "טל בן דוד", "developer", "pro"),
    ("roi", "רועי גבאי", "", "owner"),
]

# each discussion: kind, cat, city, author, hours ago it opened, views, title, body, [ (author, hours ago, body, thanks) ], solved index or -1, need
T = [
 ("collab", "build", "קרית מוצקין", "avi", 52, 214,
  "מחפש קבלן גמר לשיתוף פעולה קבוע בקריות, שלושה בניינים של 24 דירות",
  "אנחנו מסיימים שלד בשני בניינים בקרית מוצקין, והשלישי נכנס לעבודה בינואר. עד היום עבדנו עם צוות גמר אחד והוא נשאר מאחור: כל דירה חיכתה לו בממוצע שלושה שבועות אחרי הטיח. אני מחפש קבלן גמר עם צוות של לפחות 8 אנשים שיכול לקחת בניין שלם: ריצוף, חיפוי, גבס, צבע ונקודות אינסטלציה. מחיר לפי מ\"ר, תשלום שוטף פלוס 45 מיום שהמפקח מאשר את החשבון. מי שעבד בהיקפים כאלה ויכול להראות בניין שמסר, שיכתוב כאן ונקבע שיחה.",
  [("yossi", 49, "עשינו בשנה האחרונה שני פרויקטים של 30 דירות בראשון ובנס ציונה. הצוות שלי 11 אנשים, כולל רצף ראשי וגבסן קבוע. בקריות לא עבדנו עד עכשיו, אבל אם יש לינה לצוות בשבועות הארוכים אנחנו בפנים. שאלה אחת לפני שמדברים על מחיר: מי קונה את החומרים, אתם או קבלן הגמר? זה משנה לי את המחיר בערך ב-25 אחוז.", 3),
   ("avi", 47, "ריצוף וחיפוי אנחנו קונים מספק אחד בהזמנה מרוכזת. גבס וצבע עליכם. אם זה מתאים, תפתח מהדיון שיחת וידאו מחר בבוקר ואראה לך את התוכניות של הבניין הראשון.", 1),
   ("maya", 30, "טיפ מניסיון בבאר שבע: תגדירו בחוזה מראש מה נחשב דירה שמוכנה לגמר, אחרת כל צד סופר את שלושת השבועות אחרת. אצלנו זה נסגר בטופס קבלה שהמפקח חותם עליו, עם תמונה של כל חדר.", 6),
   ("yossi", 26, "סגרנו שיחה לשבוע הבא. מאיה, את הטופס אני לוקח, תודה.", 2)], 2, None),
 ("collab", "design", "תל אביב", "ronit", 40, 188,
  "מעצבת פנים מחפשת נגר וקבלן שיפוצים לעבודה משותפת על ארבע דירות באותו מגדל",
  "יש לי ארבעה לקוחות שקנו דירות באותו מגדל בצפון תל אביב, מסירה צפויה במרץ. כולם רוצים שינויי דיירים ואחר כך שיפוץ קל: מטבח בהתאמה, ארונות, הנמכות גבס ותאורה. במקום לנהל ארבעה קבלנים אני רוצה צוות אחד שעובד מול אותו מפקח של היזם ומכיר את הלו\"ז של הבניין. אני מביאה תוכניות מלאות וכתב כמויות. מחפשת נגר שעושה גם מטבחים, וקבלן שיפוצים שכבר עבד מול חברת ניהול של מגדל ויודע מה זה אישורי עבודה, שעות שקט ומעלית שירות.",
  [("shiran", 38, "אנחנו עושים מטבחים וארונות בפתח תקווה ועבדנו בשני מגדלים ברמת החייל. שאלה חשובה: הדירות מקבלות את המטבח של הקבלן ואתם מפרקים, או שהלקוחות ויתרו עליו מראש? בזיכוי על המטבח מהיזם יש כסף שהלקוחות שלך יכולים לנצל.", 4),
   ("ronit", 35, "שלושה מתוך ארבעה ויתרו, הרביעי עוד מתלבט. אשמח שתכיני הצעה לשלושה. את התוכניות אני מעלה לכאן בשבוע הבא.", 0),
   ("omer", 20, "אם יש הנמכות ותאורה, כדאי לתאם איתי לפני הגבס. בשינויי דיירים אפשר לבקש מהיזם להזיז נקודות כבר בזמן הבנייה ולחסוך פתיחת קירות אחר כך. אני זמין לשיחת וידאו מהדיון.", 5),
   ("ronit", 18, "בדיוק בשביל זה פתחתי את זה כאן. עומר, מדברים מחר.", 1)], -1, None),
 ("seek", "build", "גבעתיים", "gilad", 30, 156,
  "מחפש מהנדס קונסטרוקציה ויועץ קרקע לפרויקט פינוי בינוי קטן בגבעתיים",
  "בניין של 16 דירות ברחוב שקט, הריסה ובנייה מחדש של 38 דירות עם שתי קומות חניון. יש אדריכל ויש חתימות של 80 אחוז מהדיירים. חסרים לנו מהנדס קונסטרוקציה שתכנן חניונים תת קרקעיים צמוד לבניינים קיימים, ויועץ קרקע שיכין סקר וקידוחי ניסיון. הבניין השכן ישן, ואני רוצה שמישהו יחשוב על דיפון ועל מדידת תזוזות כבר בתכנון, ולא אחרי שמופיעים סדקים.",
  [("dana", 27, "גלעד, תחבר את יועץ הקרקע לפני שהקונסטרוקטור מתחיל. בפרויקט שלנו ברמת גן הקידוחים הראו מי תהום בעומק 6 מטר, וזה שינה את כל תכנון החניון: יצאה קומה אחת פחות ותקציב אחר לגמרי.", 7),
   ("muhamad", 22, "אנחנו מבצעים שלד וחניונים, לא מתכננים. מבחינת ביצוע, דיפון כלונסאות ליד בניין ישן צריך לקחת בחשבון גם רעידות מהקידוח. תבקשו ממי שתבחרו תוכנית מדידה עם נקודות על הבניין השכן לפני שמתחילים. זה גם מגן עליכם אם השכנים טוענים לנזק.", 5),
   ("gilad", 15, "תודה לשניכם. מוחמד, כשנגיע לביצוע אני חוזר אליך. בינתיים מחפש עדיין קונסטרוקטור, מי שעשה חניון כזה מוזמן לכתוב.", 0)], 0, ("structural", "גבעתיים")),
 ("question", "build", "חולון", "nir", 26, 131,
  "איטום גג מעל דירות: יריעות ביטומניות או פוליאוריה? שואל את מי שעשה את שתיהן",
  "יזם בחולון ביקש הצעה לאיטום גג של 600 מ\"ר מעל קומת מגורים, עם מזגנים ומערכת סולארית על הגג. המתכנן כתב יריעות ביטומניות בשתי שכבות, והיזם שואל על פוליאוריה כי שמע שזה מהיר יותר. יש לי ניסיון טוב עם שתיהן, אבל אני רוצה לשמוע מאחרים איך זה מחזיק אחרי חמש שנים כשטכנאים עולים לגג כל הזמן.",
  [("maya", 23, "בבאר שבע יש לנו שני גגות עם פוליאוריה משנת 2021. מה שלמדנו: הכנת המשטח קובעת הכול. בגג אחד הבטון לא היה יבש מספיק, ותוך שנה הופיעו בועות. היום אנחנו לא נותנים להתחיל בלי מדידת לחות מתועדת.", 8),
   ("avi", 19, "בגגות עם הרבה ציוד אני נשאר עם ביטומני ומסלולי הליכה מסומנים לטכנאים. הבעיה אצלי אף פעם לא הייתה החומר, אלא המתקין של המזגנים שקודח בגג אחרי שהאיטום כבר גמור.", 4),
   ("nir", 12, "שתי נקודות טובות. אציע ליזם פוליאוריה רק עם מדידת לחות, ופרט מוכן מראש לכל בסיס של מזגן. מי שרוצה לראות את הפרט, אני מעלה אותו לכאן.", 2)], 0, None),
 ("collab", "renewal", "נתניה", "tal", 22, 142,
  "יזם בפרויקט ראשון של 12 דירות בנתניה מחפש צוות: אדריכל, מנהל פרויקט ומשווק",
  "קנינו מגרש של דונם בצפון נתניה, ההיתר בתהליך ל-12 דירות בשלוש קומות. אני מגיע מעולם ההשקעות ולא מתחום הבנייה, ולכן אני מחפש צוות שכבר עבד יחד ולא אוסף של ספקים. אשלם לפי אבני דרך, ולמנהל הפרויקט מוכן לחלוק בחיסכון אם נסיים מתחת לתקציב.",
  [("maya", 20, "טל, לפני שמחפשים אדריכל תעשה בדיקת כדאיות עם כמאי ושמאי. ראיתי יזמים בפרויקט ראשון שגילו בשלב ההיתר שהעלות למ\"ר יוצאת קרוב מאוד למחיר המכירה באזור.", 9),
   ("dana", 17, "אנחנו עושים פרויקטים בהיקף הזה. אשמח לשיחת וידאו קצרה, תפתח אותה מכאן כשנוח לך.", 2),
   ("tal", 14, "שתיכן צודקות. מאיה, יש כמאי שעבדת איתו ותמליצי? מעדיף מישהו מהפורום.", 0),
   ("maya", 9, "תפרסם בקשה בפורום ותכתוב בה כמאי, ואני אגיב למי שאני מכירה.", 3)], 0, None),
 ("work", "design", "ראשון לציון", "yossi", 70, 263,
  "סיימנו שיפוץ מלא של דירת 4 חדרים בראשון לציון ב-11 שבועות: מה עבד ומה הייתי עושה אחרת",
  "שיפוץ מלא בבניין משנות השמונים: חשמל חדש, אינסטלציה, ריצוף, מטבח, שני חדרי רחצה ואלומיניום. עבדנו עם המעצבת של הלקוחה מהיום הראשון ועם נגרית שהכרנו כאן בפורום. מה עבד: לוח זמנים שבועי אחד לכל בעלי המקצוע בקבוצה אחת, והזמנת חלונות כבר ביום הראשון, כי אספקה לוקחת שישה שבועות. מה הייתי עושה אחרת: בדיקת צנרת במצלמה לפני התמחור. מצאנו קו ביוב סדוק מתחת לריצוף, וזה הוסיף שבוע.",
  [("eli", 66, "תודה על הקרדיט על ההזמנה המוקדמת. לכל מי שקורא: בבניינים ישנים תמדדו את הפתחים רק אחרי שמפרקים את המשקופים הישנים, אחרת יש הפתעות של 2 עד 3 ס\"מ.", 6),
   ("ronit", 60, "11 שבועות לשיפוץ כזה זה מצוין. אהבתי את הקבוצה האחת לכל בעלי המקצוע, זה חוסך לי כל שבוע שעות של טלפונים.", 3),
   ("shiran", 44, "היה כיף לעבוד איתכם. הלקוחה שלחה תמונות של המטבח אחרי חודש, הכול עומד יפה.", 4)], -1, None),
 ("seek", "design", "הרצליה", "roi", 11, 97,
  "קנינו דירה יד שנייה בהרצליה ורוצים לשפץ לפני הכניסה. מחפשים מעצבת וקבלן שעובדים יחד",
  "דירת 4 חדרים בקומה שלישית, בניין בלי מעלית. רוצים לפתוח את המטבח לסלון, להחליף ריצוף ואת שני חדרי הרחצה. התקציב בערך 350 אלף שקל, ויש לנו חודשיים וחצי עד שנגמר החוזה בדירה השכורה. עדיף צוות שכבר עבד יחד, שלא נהיה באמצע.",
  [("ronit", 9, "רועי, קיר בין מטבח לסלון בבניינים כאלה הוא הרבה פעמים קיר נושא. לפני הכול מהנדס צריך לבדוק אותו. אם הוא נושא, אפשר לפתוח חלקית עם קורה, וזו עלות נוספת שכדאי לדעת מראש.", 5),
   ("yossi", 7, "חודשיים וחצי זה צפוף אבל אפשרי, אם ההחלטות על ריצוף וכלים סניטריים נסגרות לפני שמתחילים. אני ורונית עבדנו יחד, נשמח לבוא לראות.", 2),
   ("roi", 5, "מעולה. אפשר לקבוע קודם שיחת וידאו? אנחנו עוד לא גרים שם.", 0)], -1, ("interior_designer", "הרצליה")),
 ("question", "build", "באר שבע", "omer", 8, 76,
  "עמדות טעינה לרכב חשמלי בחניון של בניין חדש: איך מכינים את החיבור כבר בשלב השלד",
  "בשני פרויקטים השנה ביקשו ממני להוסיף עמדות טעינה אחרי שהחניון כבר גמור. זה אומר חציבות, תעלות על התקרה והגדלת חיבור מול חברת החשמל. מי שמתכנן היום בניין, שימו בתוכנית החשמל תעלה ראשית לאורך החניון וצנרת ריקה לכל חניה. זה עולה מעט בשלב השלד וחוסך הרבה אחר כך. מעניין אותי לשמוע מקבלנים: כמה מכם כבר מכניסים את זה למפרט?",
  [("muhamad", 6, "אצלנו זה נכנס למפרט בשני הפרויקטים האחרונים, לבקשת היזם. הצנרת הריקה עלתה כמעט כלום כשהיא נכנסה לפני היציקה.", 3),
   ("tal", 4, "זה בדיוק מסוג הדברים שאני לא יודע לשאול. עומר, תוכל להסתכל על התוכנית שלי בנתניה?", 1),
   ("omer", 2, "בשמחה. תפתח שיחת וידאו מהדיון ונעבור עליה יחד.", 2)], -1, None),
]

for t in T:  # Ben: no long dashes
    for s in [t[6], t[7]] + [r[2] for r in t[8]]:
        assert "—" not in s and "–" not in s and " - " not in s, s[:40]

TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-forum-seed/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'bad', 'token', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nlf_t' ) ) { return array( 'err' => 'forum module not loaded' ); }
			nlf_install();
			$mt = nlf_t( 'members' ); $tt = nlf_t( 'topics' ); $rt = nlf_t( 'replies' );
			$ids = array_map( 'intval', $wpdb->get_col( "SELECT id FROM $mt WHERE contact LIKE 'seed-%@example.invalid'" ) );
			$mode = (string) $b['mode'];
			if ( 'video-off' === $mode || 'video-on' === $mode ) { // 18.11.2026: since 1.72.698 a call pill shows next to every member who allowed video; nobody answers for a sample member
				$n = 0;
				if ( function_exists( 'nlfc_pref_set' ) ) { foreach ( $ids as $id ) { nlfc_pref_set( $id, 'video-on' === $mode ? 1 : 0, 0 ); $n++; } }
				do_action( 'litespeed_purge_all' );
				return array( 'video' => $mode, 'members' => $n );
			}
			if ( 'cookies' === $mode ) {
				$out = array();
				foreach ( array( 'avi', 'yossi' ) as $k ) {
					$tok = bin2hex( random_bytes( 32 ) );
					$wpdb->update( $mt, array( 'session_hash' => hash( 'sha256', $tok ), 'last_seen' => nlf_now_sql() ), array( 'contact' => 'seed-' . $k . '@example.invalid' ) );
					$out[ $k ] = $tok;
				}
				return array( 'cookies' => $out );
			}
			$gone = array();
			if ( $ids ) {
				$in = implode( ',', $ids );
				// 18.11.2026: real members answered sample discussions. Their answers are never deleted with the samples:
				// the run stops and names them, until the owner decides what happens to those answers.
				$real = (int) $wpdb->get_var( "SELECT COUNT(*) FROM $rt WHERE member_id NOT IN ($in) AND topic_id IN (SELECT id FROM $tt WHERE member_id IN ($in))" );
				if ( $real > 0 ) { return array( 'err' => 'stopped: ' . $real . ' answers by real members sit on sample discussions; nothing was deleted' ); }
				$tids = array_map( 'intval', $wpdb->get_col( "SELECT id FROM $tt WHERE member_id IN ($in)" ) );
				foreach ( array( 'replies', 'thanks', 'flags', 'follows' ) as $tb ) { $gone[ $tb ] = (int) $wpdb->query( 'DELETE FROM ' . nlf_t( $tb ) . " WHERE member_id IN ($in)" ); }
				if ( $tids ) { $tin = implode( ',', $tids ); $gone['replies_on_their_topics'] = (int) $wpdb->query( "DELETE FROM $rt WHERE topic_id IN ($tin)" ); }
				$gone['topics']  = (int) $wpdb->query( "DELETE FROM $tt WHERE member_id IN ($in)" );
				if ( function_exists( 'nlfc_table' ) ) { $wpdb->query( 'DELETE FROM ' . nlfc_table() . " WHERE member_id IN ($in)" ); }
				$gone['members'] = (int) $wpdb->query( "DELETE FROM $mt WHERE id IN ($in)" );
			}
			if ( 'unseed' === $mode ) { do_action( 'litespeed_purge_all' ); return array( 'removed' => $gone ); }
			$now = time(); $sql = function ( $h ) use ( $now ) { return gmdate( 'Y-m-d H:i:s', $now - (int) round( $h * 3600 ) ); };
			$mid = array();
			foreach ( (array) $b['people'] as $p ) {
				$c = 'seed-' . $p[0] . '@example.invalid';
				$wpdb->insert( $mt, array( 'display_name' => $p[1], 'contact' => $c, 'contact_hash' => nlf_contact_hash( $c, nlf_key() ), 'role_label' => $p[3], 'trade' => $p[2],
					'approved_posts' => 6, 'status' => 'ok', 'session_hash' => '', 'created_at' => $sql( 24 * 9 ), 'last_seen' => $sql( 1 + count( $mid ) * 0.7 ) ) );
				$mid[ $p[0] ] = (int) $wpdb->insert_id;
			}
			if ( function_exists( 'nlfc_install' ) ) { nlfc_install(); }
			if ( function_exists( 'nlfc_pref_set' ) ) { foreach ( $mid as $m ) { nlfc_pref_set( $m, 1, 0 ); } }
			$made = array();
			foreach ( (array) $b['topics'] as $t ) {
				list( $kind, $cat, $city, $who, $h, $views, $title, $body, $reps, $solved, $need ) = $t;
				$last = $reps ? $reps[ count( $reps ) - 1 ][1] : $h;
				$row = array( 'cat' => $cat, 'kind' => $kind, 'title' => $title, 'body' => $body, 'member_id' => $mid[ $who ], 'city' => $city, 'status' => 'live',
					'reply_count' => count( $reps ), 'view_count' => (int) $views, 'thanks_count' => 0, 'body_hash' => hash( 'sha256', $body ), 'created_at' => $sql( $h ), 'last_at' => $sql( $last ) );
				if ( 'seek' === $kind ) { $row['status_seek'] = 'open'; if ( $need ) { $row['need_profession'] = $need[0]; $row['need_city'] = $need[1]; } }
				$wpdb->insert( $tt, $row ); $tid = (int) $wpdb->insert_id;
				$rids = array();
				foreach ( $reps as $r ) {
					$wpdb->insert( $rt, array( 'topic_id' => $tid, 'member_id' => $mid[ $r[0] ], 'body' => $r[2], 'status' => 'live', 'thanks_count' => (int) $r[3], 'body_hash' => hash( 'sha256', $r[2] ), 'created_at' => $sql( $r[1] ) ) );
					$rids[] = (int) $wpdb->insert_id;
				}
				if ( $solved >= 0 && isset( $rids[ $solved ] ) ) { $wpdb->update( $tt, array( 'solved_reply_id' => $rids[ $solved ] ), array( 'id' => $tid ) ); }
				$made[] = $tid;
			}
			do_action( 'litespeed_purge_all' );
			return array( 'members' => count( $mid ), 'topics' => $made, 'removed_first' => $gone );
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-forum-seed-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-forum-seed/v1/run", {"token": TOKEN, "mode": MODE, "people": PEOPLE, "topics": T}, timeout=120); must(s, r, "run")
    if MODE == "cookies":
        out = os.path.join(os.environ.get("TEMP", "."), "nlf_seed_cookies.json")
        json.dump(r, open(out, "w", encoding="utf-8"))
        print("[seed] cookies for avi + yossi saved to", out)
    else:
        print("[seed]", json.dumps(r, ensure_ascii=False))
finally:
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
