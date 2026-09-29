<?php
/**
 * In-memory WordPress doubles for the request callback (inc/rfp.php) and the stage's unit resolver (inc/project-stage.php):
 * no bootstrap, database, network, mail or file writes; all state in $GLOBALS['M']. Shared by test_rfp_request.php (the
 * cases) and rfp_local_endpoint.php (the browser test's local endpoint). Synthetic data only.
 */
if ( ! defined( 'ABSPATH' ) ) { define('ABSPATH', __DIR__ . '/memory-only/'); }
if ( ! defined( 'OBJECT' ) ) { define('OBJECT', 'OBJECT'); }
if ( ! defined( 'NADLAN_CONFIG_VERSION' ) ) { define('NADLAN_CONFIG_VERSION', 'test'); }
if ( ! defined( 'HOUR_IN_SECONDS' ) ) { define('HOUR_IN_SECONDS', 3600); }
final class WP_REST_Request implements ArrayAccess {
    private $payload; function __construct($payload) { $this->payload = $payload; }
    function get_json_params() { return $this->payload; }
    function offsetGet($k): mixed { return $this->payload[$k] ?? null; }
    function offsetExists($k): bool { return isset($this->payload[$k]); }
    function offsetSet($k, $v): void {} function offsetUnset($k): void {}
}
final class WP_Error { public $code; public $data; function __construct($code, $message = '', $data = []) { $this->code = $code; $this->data = $data; } function get_error_code() { return $this->code; } }
final class WP_Query {
    public $posts = [];
    function __construct($a) {
        if (($a['post_type'] ?? '') === 'nadlan_rfp' && isset($a['meta_key'])) {
            foreach ($GLOBALS['M']['meta'] as $id => $m) { if (($m[$a['meta_key']] ?? null) === $a['meta_value'] && ($GLOBALS['M']['types'][$id] ?? '') === 'nadlan_rfp') { $this->posts[] = $id; break; } }
        }
    }
}
class WP_Post { public $ID; public $post_password = ''; public $post_type = ''; }
function add_action($h, $cb = null, ...$r) { $GLOBALS['WP_HOOKS'][$h][] = $cb; } function add_filter(...$a) {} function register_rest_route($ns, $route, $args) { $GLOBALS['WP_ROUTES'][$ns . $route] = $args; } function register_post_type(...$a) {}
function apply_filters($h, $v) { return $v; }
function sanitize_title($v) { return trim(preg_replace('/[^a-z0-9-]+/', '-', strtolower((string) $v)), '-'); }
function sanitize_key($v) { return preg_replace('/[^a-z0-9_-]/', '', strtolower((string) $v)); }
function sanitize_text_field($v) { return trim(strip_tags((string) $v)); }
function sanitize_textarea_field($v) { return trim(strip_tags((string) $v)); }
function wp_salt($s = 'auth') { return 'synthetic-salt'; }
function get_page_by_path($slug, $f, $t) {
    if ($t === 'nadlan_rfp') {
        hook('find');
        foreach ($GLOBALS['M']['names'] as $id => $n) { if ($n === $slug && ($GLOBALS['M']['types'][$id] ?? '') === 'nadlan_rfp') { return (object) ['ID' => $id]; } }
        return null;
    }
    return isset($GLOBALS['M']['projects'][$slug]) ? (object) ['ID' => $GLOBALS['M']['projects'][$slug]] : null;
}
/* a deterministic point where a second request can enter the first one's flow (Codex's RFP-B2-DRAFT race method) */
function hook($at) { $h = $GLOBALS['M']['hooks'][$at] ?? null; if ($h) { unset($GLOBALS['M']['hooks'][$at]); $h(); } }
function get_post_meta($id, $k, $single = true) { return $GLOBALS['M']['meta'][$id][$k] ?? ''; }
function get_post_type($id) { return $GLOBALS['M']['types'][$id] ?? false; }
function get_post_field($f, $id) { return $f === 'post_content' ? ($GLOBALS['M']['content'][$id] ?? '') : ''; }
function get_the_title($id) { return 'Synthetic project ' . $id; }
function get_permalink($id) { $slug = array_search((int) $id, $GLOBALS['M']['projects'] ?? [], true); return (getenv('NL_SITE_BASE') ?: 'https://example.invalid') . '/projects/' . ($slug !== false ? $slug : 'p' . $id) . '/'; }
function wp_generate_password($n, $a = true, $b = false) { return substr(str_repeat(bin2hex(random_bytes(16)), 2), 0, $n); }
function wp_json_encode($v, $f = 0) { return json_encode($v, $f); }
function wp_slash($v) { return addslashes($v); }
function wp_insert_post($v, $e = false) {
    if (!empty($GLOBALS['M']['fail_insert'])) { return new WP_Error('db', 'synthetic failure', ['status' => 500]); }
    hook('insert');
    $id = ++$GLOBALS['M']['seq']; $GLOBALS['M']['inserts'][] = $id; $GLOBALS['M']['types'][$id] = $v['post_type'];
    if (!empty($v['post_name'])) { $GLOBALS['M']['names'][$id] = $v['post_name']; }
    $GLOBALS['M']['content'][$id] = stripslashes($v['post_content']); return $id;
}
function update_post_meta($id, $k, $v) { $GLOBALS['M']['meta'][$id][$k] = $v; $GLOBALS['M']['writes'][] = [$id, $k, $v]; return true; }
function add_option($k, $v, $d = '', $a = 'yes') { if (isset($GLOBALS['M']['options'][$k])) { return false; } $GLOBALS['M']['options'][$k] = $v; return true; }
function delete_option($k) { hook('release'); unset($GLOBALS['M']['options'][$k]); return true; }
function is_wp_error($v) { return $v instanceof WP_Error; }
function rest_ensure_response($v) { return $v; }
function rest_url($p) { return (getenv('NL_REST_BASE') ?: 'https://example.invalid/wp-json/') . $p; }
function add_query_arg($k, $v, $url) { return $url . (strpos($url, '?') === false ? '?' : '&') . $k . '=' . $v; }
function get_option($k, $d = false) { return $GLOBALS['M']['options'][$k] ?? $d; }
function is_admin() { return false; } function is_singular($t = '') { return false; }
function status_header($c) { $GLOBALS['M']['status'] = $c; } function esc_html($v) { return htmlspecialchars((string) $v, ENT_QUOTES); }
function esc_attr($v) { return htmlspecialchars((string) $v, ENT_QUOTES); } function esc_url($v) { return htmlspecialchars((string) $v, ENT_QUOTES); }
function post_password_required($id) { return false; }

/* the lead path (inc/conversion-cta.php + inc/lead-e2e.php): recorded, never sent */
if ( ! defined( 'MINUTE_IN_SECONDS' ) ) { define('MINUTE_IN_SECONDS', 60); }
function sanitize_email($v) { $v = trim((string) $v); return filter_var($v, FILTER_VALIDATE_EMAIL) ? $v : ''; }
function is_email($v) { return (bool) filter_var((string) $v, FILTER_VALIDATE_EMAIL); }
function esc_url_raw($v) { return (string) $v; }
function absint($v) { return abs((int) $v); }
function get_transient($k) { return $GLOBALS['M']['transients'][$k] ?? false; }
function set_transient($k, $v, $t = 0) { $GLOBALS['M']['transients'][$k] = $v; return true; }
function current_time($f, $gmt = 0) { return $f === 'mysql' ? gmdate('Y-m-d H:i:s') : gmdate('Y-m-d H:i'); }
function wp_mail($to, $subject, $body = '', ...$r) { $GLOBALS['M']['mail'][] = ['to' => $to, 'subject' => $subject]; return true; }
function admin_url($p = '') { return 'https://example.invalid/wp-admin/' . $p; }
function home_url($p = '') { return 'https://example.invalid' . $p; }
function get_bloginfo($k = '') { return 'NadLan (test)'; }
function get_post($id) { $t = $GLOBALS['M']['types'][(int) $id] ?? null; if (!$t) { return null; } $o = new WP_Post(); $o->ID = (int) $id; $o->post_type = $t; return $o; }
function update_option($k, $v, $a = null) { $GLOBALS['M']['options'][$k] = $v; return true; }
function add_post_meta($id, $k, $v, $u = false) { $GLOBALS['M']['meta'][$id][$k] = $v; return true; }
function wp_parse_args($a, $d = []) { return array_merge((array) $d, (array) $a); }
function do_action(...$a) {}
function current_user_can($c) { return false; }


