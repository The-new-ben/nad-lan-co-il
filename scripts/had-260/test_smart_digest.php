<?php
/**
 * HAD-260: tests for the smart daily email (plugins/nadlan-config/inc/smart-digest.php).
 * No WordPress, no database, no mail: the pure helpers run against small stubs.
 *   php scripts/had-260/test_smart_digest.php                 JSON out, exit 1 on any failure
 *   php scripts/had-260/test_smart_digest.php --preview FILE  also writes the preview HTML (mock data)
 */
declare(strict_types=1);
if (PHP_SAPI !== 'cli') { exit(2); }
define('ABSPATH', __DIR__ . '/');
define('DAY_IN_SECONDS', 86400);
define('HOUR_IN_SECONDS', 3600);
$GLOBALS['HOOKS'] = [];
function add_action($h, $cb, $p = 10, $a = 1) { $GLOBALS['HOOKS'][$h][] = $cb; return true; }
function add_filter($h, $cb, $p = 10, $a = 1) { $GLOBALS['HOOKS'][$h][] = $cb; return true; }
function apply_filters($h, $v, ...$rest) { return $v; }
function get_option($k, $d = false) { return $GLOBALS['OPT'][$k] ?? $d; }
function esc_html($s) { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }
function esc_url($s) { $s = (string) $s; return preg_match('#^(https?:|tel:|mailto:)#i', $s) ? htmlspecialchars($s, ENT_QUOTES, 'UTF-8') : ''; }

require dirname(__DIR__, 2) . '/plugins/nadlan-config/inc/smart-digest.php';

$R = [];
function ok($id, $cond, $what) { $GLOBALS['R'][] = ['id' => $id, 'pass' => (bool) $cond, 'what' => $what]; }

/* 1. test-lead filter: the patterns seen on the live site (HAD-260 findings) */
$tests = [
    ['name' => 'בדיקת מערכת אורליה ספורט', 'phone' => '0521112233'],
    ['name' => 'QA Codex', 'phone' => '0547778899'],
    ['name' => 'Ben', 'title' => 'E2E lead - General - 2026-08-01 10:00'],
    ['name' => 'בדיקת 3D', 'email' => 'x@gmail.com'],
    ['name' => 'דני', 'phone' => '0500000001'],
    ['name' => 'דני', 'phone' => '+972-50-000-0003'],
    ['name' => 'רות', 'phone' => '0520000007'],
    ['name' => 'רות', 'email' => 'qa.a@example.test'],
    ['name' => 'רות', 'email' => 'buyer@example.com'],
    ['name' => 'רות', 'email' => 'test+lead@gmail.com'],
    ['name' => 'רות', 'phone' => '0501234567'],
    ['name' => 'בדיקה סינתטית', 'phone' => '0500000000'],
    ['name' => 'רות', 'flags' => ['1']],
    ['name' => 'test', 'phone' => '0529998877'],
];
foreach ($tests as $i => $l) {
    ok('test-' . $i, nadlan_sd_is_test_lead($l), 'a system test is hidden: ' . json_encode($l, JSON_UNESCAPED_UNICODE));
}
$real = [
    ['name' => 'דנה כהן', 'phone' => '052-666-7788', 'email' => 'dana.cohen@gmail.com'],
    ['name' => 'Testa Levi', 'phone' => '0541239876'],
    ['name' => 'יוסי', 'phone' => '+972 54 555 0101', 'flags' => ['', '0']],
    ['name' => 'Qader', 'email' => 'qader@walla.co.il'],
    ['name' => 'בן', 'phone' => '0508123456', 'title' => 'בן - קנייה - 2026-06-03 09:12'],
];
foreach ($real as $i => $l) {
    ok('real-' . $i, !nadlan_sd_is_test_lead($l), 'a real lead stays visible: ' . json_encode($l, JSON_UNESCAPED_UNICODE));
}

/* 2. the subject carries the numbers */
$lead = ['name' => 'א', 'phone' => '0541112233'];
ok('subj-1', nadlan_sd_subject(['date_label' => '7.10', 'leads' => [$lead, $lead], 'decisions' => [['text' => 'x']]]) === 'נדלן · 7.10 · 2 לידים חדשים · החלטה אחת מחכה לך', 'two leads, one decision');
ok('subj-2', nadlan_sd_subject(['date_label' => '7.10', 'leads' => [$lead]]) === 'נדלן · 7.10 · ליד חדש אחד', 'one lead, nothing waiting');
ok('subj-3', nadlan_sd_subject(['date_label' => '7.10', 'leads' => [], 'decisions' => [['text' => 'x'], ['text' => 'y'], ['text' => 'z']]]) === 'נדלן · 7.10 · אין לידים חדשים · 3 החלטות מחכות לך', 'no leads, three decisions');
ok('subj-4', nadlan_sd_subject(['date_label' => '7.10', 'leads' => [], 'decisions' => [], 'issues' => [['text' => 'x']]]) === 'נדלן · 7.10 · אין לידים חדשים · תקלה אחת', 'an issue alone is not quiet');
ok('subj-5', nadlan_sd_subject(['date_label' => '7.10', 'leads' => [], 'decisions' => [], 'issues' => [], 'still_open' => ['lead' => 2]]) === 'נדלן · 7.10 · אין חדש, הכול שקט', 'already-reported items do not break the quiet day');
ok('quiet-1', nadlan_sd_is_quiet(['leads' => [], 'decisions' => [], 'issues' => [], 'still_open' => ['referral' => 1]]), 'quiet when only already-reported items are open');
ok('quiet-2', !nadlan_sd_is_quiet(['leads' => [$lead]]), 'not quiet with a new lead');

/* 3. call and WhatsApp links */
$pl = nadlan_sd_phone_links('050-111-2233');
ok('phone-1', $pl['tel'] === 'tel:+972501112233' && $pl['wa'] === 'https://wa.me/972501112233', 'local number to +972 links');
$pl = nadlan_sd_phone_links('+972 54 555 0101');
ok('phone-2', $pl['tel'] === 'tel:+972545550101' && $pl['wa'] === 'https://wa.me/972545550101', 'international number kept');
ok('phone-3', nadlan_sd_phone_links('')['tel'] === '', 'no phone, no links');

/* 4. the HTML: RTL, the links, escaping */
$html = nadlan_sd_render_html(['date_label' => '7.10', 'inbox_url' => 'https://nad-lan.co.il/wp-admin/admin.php?page=nadlan-inbox',
    'leads' => [['name' => '<script>x</script>', 'phone' => '0541112233', 'handled_url' => 'https://nad-lan.co.il/wp-admin/admin-post.php?action=nadlan_sd_handled&lead=5&sig=abc', 'question' => 'שאלה']]]);
ok('html-1', strpos($html, 'dir="rtl"') !== false, 'right to left');
ok('html-2', strpos($html, '<script>') === false && strpos($html, '&lt;script&gt;') !== false, 'names are escaped');
ok('html-3', strpos($html, 'https://wa.me/972541112233') !== false && strpos($html, 'tel:+972541112233') !== false, 'call and WhatsApp buttons');
ok('html-4', strpos($html, 'סמן טופל') !== false && strpos($html, 'action=nadlan_sd_handled') !== false, 'the mark-handled link');
ok('html-5', strpos($html, 'Lead Inbox') !== false, 'the inbox link');
$quiet = nadlan_sd_render_html(['date_label' => '7.10', 'inbox_url' => 'https://nad-lan.co.il/wp-admin/admin.php?page=nadlan-inbox']);
ok('html-6', strpos($quiet, 'אין חדש, הכול שקט') !== false, 'quiet day says one line');

/* preview (mock data, fictional people) */
$argv = $GLOBALS['argv'];
$pi = array_search('--preview', $argv, true);
if ($pi !== false && !empty($argv[$pi + 1])) {
    $site = 'https://nad-lan.co.il';
    $h = fn($id) => $site . '/wp-admin/admin-post.php?action=nadlan_sd_handled&lead=' . $id . '&sig=PREVIEW';
    $busy = [
        'date_label' => '8.10', 'window_label' => 'מ-7.10 08:00 עד 8.10 08:00 (נתונים מדומים לתצוגה בלבד)',
        'inbox_url' => $site . '/wp-admin/admin.php?page=nadlan-inbox',
        'leads' => [
            ['name' => 'דוגמה: נועה לוי', 'phone' => '054-555-0101', 'email' => 'noa.example@gmail.com', 'page_title' => 'כיכר המדינה, תל אביב', 'page_url' => $site . '/projects/kikar-hamedina/',
             'question' => 'מה המחיר של 4 חדרים בקומה גבוהה? · קנייה · 4 חדרים', 'handled_url' => $h(901), 'edit_url' => $site . '/wp-admin/post.php?post=901&action=edit'],
            ['name' => 'דוגמה: אבי מזרחי', 'phone' => '052-555-0102', 'page_title' => 'מחירי דירות באשדוד', 'page_url' => $site . '/ashdod-apartment-prices/',
             'question' => 'מחפש דירה להשקעה עד 2 מיליון', 'ack_failed' => true, 'handled_url' => $h(902), 'edit_url' => $site . '/wp-admin/post.php?post=902&action=edit'],
        ],
        'test_hidden' => 3,
        'compare' => [
            ['label' => 'לידים אמיתיים', 'values' => [2, 0, 1]],
            ['label' => 'מודעות חדשות', 'values' => [1, 1, 0]],
        ],
        'compare_note' => 'לחיצות וואטסאפ וחיוג נמדדות כרגע רק ב-Google Analytics, לא באתר, ולכן לא מופיעות כאן.',
        'decisions' => [
            ['text' => 'ליד שעדיין לא טופל: דוגמה: שירה כץ (050-555-0103)', 'detail' => 'נכנס לפני 3 ימים, מתוך עמוד פרויקט. סמן טופל, או פתח וסגור אותו.', 'url' => $h(880), 'cta' => 'סמן טופל'],
            ['text' => 'הפניה פתוחה: דוגמה: לקוח → איש מקצוע (הצעת מחיר)', 'detail' => 'מצב: הועברה', 'url' => $site . '/wp-admin/post.php?post=870&action=edit', 'cta' => 'לעדכן מצב'],
        ],
        'still_open' => ['lead' => 1],
        'issues' => [
            ['text' => 'מייל האישור ללקוח לא נשלח לליד של דוגמה: אבי מזרחי.', 'detail' => 'הליד נשמר, אבל הלקוח לא קיבל אישור. כדאי לחזור אליו בטלפון.'],
            ['text' => '2 מיילים מהאתר לא נשלחו ב-24 השעות האחרונות.', 'detail' => 'למשל: אישור פנייה. שגיאה: Could not instantiate mail function.'],
        ],
    ];
    $calm = ['date_label' => '9.10', 'window_label' => 'מ-8.10 08:00 עד 9.10 08:00 (נתונים מדומים)', 'inbox_url' => $busy['inbox_url'], 'still_open' => ['referral' => 1],
             'compare' => [['label' => 'לידים אמיתיים', 'values' => [0, 2, 0]]], 'compare_note' => $busy['compare_note']];
    $page = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HAD-260 smart digest preview</title>'
        . '<style>body{margin:0;background:#E9E4DA;font-family:Arial,sans-serif}.cap{max-width:652px;margin:24px auto 6px;padding:0 16px;font-size:13px;color:#444}.cap b{font-size:15px;color:#111}</style></head><body>'
        . '<div class="cap"><b>יום עם פעילות</b><br>נושא המייל: ' . esc_html(nadlan_sd_subject($busy)) . '<br>נתונים מדומים, אנשים בדויים. נוצר מהפונקציה האמיתית nadlan_sd_render_html.</div>'
        . nadlan_sd_render_html($busy)
        . '<div class="cap"><b>יום שקט</b> (ברירת המחדל: לא נשלח בכלל. כך הוא נראה אם מדליקים "לשלוח גם ביום שקט")<br>נושא המייל: ' . esc_html(nadlan_sd_subject($calm)) . '</div>'
        . nadlan_sd_render_html($calm) . '</body></html>';
    file_put_contents($argv[$pi + 1], $page);
}

$fail = array_values(array_filter($R, fn($r) => !$r['pass']));
echo json_encode(['total' => count($R), 'failed' => count($fail), 'failures' => $fail], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT), "\n";
exit($fail ? 1 : 0);
