"""HAD-605 check (26.10.2026): runs the PATCHED urban-hub.php route under php-cli with WordPress stubbed (transients in memory,
fake complex posts), as one IP: 130 lookups of 3 cities repeated, then 125 different queries, then a cached city again.
Expected: repeats are cache hits that never count; misses stop at 120 with a 429 carrying the Hebrew message and Retry-After;
a cached city still answers while the IP is at its limit; once the fixed hour from the first counted call is over, a new query is
answered again. Before the fix the same run is cut at call 31.

    python had605_test.py      (needs build2.py first: out/urban-hub.patched.php)
"""
import io
import json
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib2  # noqa: E402

STUB = r"""<?php
define('ABSPATH', __DIR__); define('HOUR_IN_SECONDS', 3600);
$GLOBALS['T'] = array(); $GLOBALS['ROUTE'] = null; $GLOBALS['Q'] = 0;
function get_transient($k){ return $GLOBALS['T'][$k] ?? false; }
function set_transient($k,$v,$t=0){ $GLOBALS['T'][$k] = $v; return true; }
function sanitize_text_field($s){ return trim(strip_tags((string)$s)); }
function wp_unslash($s){ return $s; }
function apply_filters($t,$v){ return $v; }
function add_action($h,$f){ if ($h === 'rest_api_init') { $f(); } }
function add_shortcode(){}
function home_url($p=''){ return 'https://nad-lan.co.il'.$p; }
function register_rest_route($ns,$r,$a){ $GLOBALS['ROUTE'] = $a['callback']; }
class WP_Error { public $code; public $msg; public $data; function __construct($c,$m,$d){ $this->code=$c; $this->msg=$m; $this->data=$d; } }
class WP_REST_Response { public $data; public $status; public $headers = array(); function __construct($d=null,$s=200){ $this->data=$d; $this->status=$s; } function header($k,$v){ $this->headers[$k]=$v; } }
function rest_ensure_response($d){ return $d instanceof WP_REST_Response ? $d : new WP_REST_Response($d, 200); }
function get_posts($a){ $GLOBALS['Q']++; $o = array(); for ($i = 0; $i < 3; $i++) { $p = new stdClass(); $p->ID = $i + 1; $o[] = $p; } return $o; }
function get_the_title($p){ return 'מתחם ' . $p->ID; }
function get_permalink($p){ return 'https://nad-lan.co.il/projects/x' . $p->ID . '/'; }
function get_post_meta($id,$k,$s){ return $k === 'city' ? 'עיר' : ''; }
class Req { public $p; function __construct($p){ $this->p=$p; } function get_param($k){ return $this->p[$k] ?? ''; } }
$_SERVER['REMOTE_ADDR'] = '203.0.113.7';
require $argv[1];
$cb = $GLOBALS['ROUTE'];
$log = array('repeat_ok'=>0,'repeat_429'=>0,'miss_ok'=>0,'miss_429'=>0,'first_429_at'=>null,'msg'=>null,'retry'=>null,'hit_while_limited'=>null);
$cities = array('רמת גן','חולון','בת ים');
for ($i = 0; $i < 130; $i++) { $r = $cb(new Req(array('city'=>$cities[$i % 3]))); $s = is_object($r) && isset($r->status) ? $r->status : (($r instanceof WP_Error) ? $r->data['status'] : 200); if ($s === 429) $log['repeat_429']++; else $log['repeat_ok']++; }
for ($i = 0; $i < 125; $i++) { $r = $cb(new Req(array('city'=>'עיר', 'q'=>'רחוב ' . $i))); $s = ($r instanceof WP_Error) ? $r->data['status'] : (is_object($r) ? $r->status : 200);
  if ($s === 429) { $log['miss_429']++; if ($log['first_429_at'] === null) { $log['first_429_at'] = $i + 1; $log['msg'] = $r instanceof WP_Error ? $r->msg : $r->data['message']; $log['retry'] = $r instanceof WP_Error ? null : ($r->headers['Retry-After'] ?? null); } } else $log['miss_ok']++; }
$k = 'nadlan_ur_lk_' . md5('203.0.113.7'); $log['stored'] = is_array($GLOBALS['T'][$k] ?? null) ? 'count + window start' : gettype($GLOBALS['T'][$k] ?? null);
if (is_array($GLOBALS['T'][$k] ?? null)) { $GLOBALS['T'][$k][1] -= 3601; $r2 = $cb(new Req(array('city'=>'עיר', 'q'=>'רחוב אחרי שעה'))); $log['new_query_after_the_hour'] = ($r2 instanceof WP_REST_Response) ? $r2->status : 'other'; $GLOBALS['T'][$k][1] += 3601; $GLOBALS['T'][$k][0] = 999; }
$r = $cb(new Req(array('city'=>'רמת גן'))); $log['hit_while_limited'] = ($r instanceof WP_Error) ? 'error ' . $r->data['status'] : ($r->status . ' ' . count($r->data['matches'] ?? array()) . ' matches');
$log['db_queries'] = $GLOBALS['Q'];
echo json_encode($log, JSON_UNESCAPED_UNICODE);
"""


def run(target):
    p = os.path.join(lib2.OUT, 'had605-stub.php')
    open(p, 'w', encoding='utf-8', newline='\n').write(STUB)
    r = subprocess.run([lib2.PHP, p, target], capture_output=True)
    out = r.stdout.decode('utf-8')
    if not out.startswith('{'):
        raise SystemExit((r.stderr.decode('utf-8', 'replace') + out)[:600])
    return json.loads(out)


res = {'patched': run(os.path.join(lib2.OUT, 'urban-hub.patched.php')),
       'repo_today': run(os.path.join(lib2.REPO, 'plugins', 'nadlan-config', 'inc', 'urban-hub.php'))}
json.dump(res, open(os.path.join(lib2.OUT, 'had605-test.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
