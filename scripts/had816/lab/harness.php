<?php
// HAD-816 local lab: renders inc/transit.php without WordPress (stubs only), into lab/out-<lang>.html
define('ABSPATH', __DIR__);
define('NADLAN_CONFIG_VERSION', 'lab');
$GLOBALS['H'] = array(); $GLOBALS['F'] = array(); $GLOBALS['S'] = '';
function get_option($k, $d = false) { return $d; }
function update_option() {}
function add_rewrite_rule() {} function flush_rewrite_rules() {}
function add_action($h, $f, $p = 10) { $GLOBALS['H'][$h][] = $f; }
function add_filter($h, $f, $p = 10) { $GLOBALS['F'][$h][] = $f; }
function get_query_var() { return ''; }
function plugins_url($p, $f) { return '/plugin/' . $p; }
function home_url($p = '/') { return 'https://nad-lan.co.il' . $p; }
function esc_html($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function esc_attr($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function esc_url($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function wp_json_encode($o, $f = 0) { return json_encode($o, $f); }
function wp_enqueue_style($h, $u) { $GLOBALS['S'] .= '<link rel="stylesheet" href="' . $u . '">'; }
function wp_enqueue_script($h, $u) { $GLOBALS['JS'] = $u; }
function wp_add_inline_script($h, $c) { $GLOBALS['IJS'] = $c; }
function get_header() {
  $la = 'lang="he" dir="rtl"'; foreach ($GLOBALS['F']['language_attributes'] ?? array() as $f) { $la = $f(); }
  echo '<!doctype html><html ' . $la . '><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>lab</title>';
  echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Noto+Serif+Hebrew:wght@600;700&display=swap">';
  foreach ($GLOBALS['H']['wp_head'] ?? array() as $f) { $f(); }
  echo $GLOBALS['S'] . '<style>body{margin:0}.labbar{position:fixed;left:16px;right:90px;bottom:16px;height:56px;border-radius:30px;background:#0f7a63;color:#fff;display:flex;align-items:center;justify-content:center;font:700 16px Assistant}</style></head><body><header style="height:56px;border-bottom:1px solid #e3e1da;display:flex;align-items:center;padding:0 16px;font:800 20px Assistant;color:#1f4b5c">נדל״ן</header>';
}
function get_footer() { echo '<div class="labbar">ייעוץ חינם (סרגל האתר)</div><script>' . $GLOBALS['IJS'] . '</script><script src="' . $GLOBALS['JS'] . '"></script></body></html>'; }
require __DIR__ . '/../../../plugins/nadlan-config/inc/transit.php';
$lang = $argv[1] ?? 'he';
ob_start(); nltr_render($lang); file_put_contents(__DIR__ . '/out-' . $lang . '.html', ob_get_clean());
echo "ok $lang\n";
