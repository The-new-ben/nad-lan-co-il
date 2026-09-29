<?php
/**
 * UnitDesignRequest (v102) browser test's LOCAL endpoint: the browser's POST /wp-json/nadlan/v1/lead and /rfp are routed here
 * by the browser tests (Playwright route), never to the site. BOTH run the branch's REAL code over the in-memory doubles
 * (rfp_memory_wp.php): /lead is the /nadlan/v1/lead callback of inc/conversion-cta.php (with inc/lead-e2e.php, so the lead
 * test mode's branch runs when the state's option nadlan_feature_lead_e2e is '1'), /rfp is nadlan_rfp_create. Email is
 * recorded in the state, never sent. State persists in a JSON file between requests.
 *
 *   php rfp_local_endpoint.php lead|rfp|state <statefile> < body.json      -> {"status": 200, "body": {...}}
 *   php rfp_local_endpoint.php render <statefile> < {"token": "..."}        -> the rendered document (HTML)
 * Control (in the state file): "fail_insert_times": N makes the next N document inserts fail (a server-side failure);
 * "options": {"nadlan_feature_lead_e2e": "1"} runs the lead test-mode branch.
 */
declare(strict_types=1);
if (PHP_SAPI !== 'cli') { exit(2); }
$ROOT = dirname(__DIR__, 2) . '/plugins/nadlan-config';
require __DIR__ . '/rfp_memory_wp.php';
require $ROOT . '/inc/project-stage.php';
require $ROOT . '/inc/rfp.php';
require $ROOT . '/inc/lead-e2e.php';
require $ROOT . '/inc/conversion-cta.php';
foreach ($GLOBALS['WP_HOOKS']['rest_api_init'] ?? [] as $cb) { if (is_callable($cb)) { $cb(); } }

[$op, $stateFile] = [$argv[1] ?? '', $argv[2] ?? ''];
$st = is_file($stateFile) ? json_decode((string) file_get_contents($stateFile), true) : null;
$GLOBALS['M'] = is_array($st) ? $st : ['seq' => 900, 'inserts' => [], 'writes' => [], 'options' => [], 'content' => [], 'names' => [], 'hooks' => [], 'leads' => [], 'transients' => [], 'mail' => [], 'fail_insert_times' => 0,
    'projects' => ['rainbow-tel-aviv' => 101, 'duo-tel-aviv' => 102], 'types' => [101 => 'nadlan_project', 102 => 'nadlan_project'], 'meta' => []];
foreach (['types', 'meta', 'content', 'names'] as $k) { $fixed = []; foreach (($GLOBALS['M'][$k] ?? []) as $id => $v) { $fixed[(int) $id] = $v; } $GLOBALS['M'][$k] = $fixed; }
$GLOBALS['M']['hooks'] = [];
$body = json_decode((string) stream_get_contents(STDIN), true);
$out = ['status' => 400, 'body' => ['ok' => false]];
if ($op === 'lead') {
    // the real /lead callback; the state keeps its own record of what the browser asked, for the tests
    $r = ($GLOBALS['WP_ROUTES']['nadlan/v1/lead']['callback'])(new WP_REST_Request($body));
    if ($r instanceof WP_Error) { $out = ['status' => (int) ($r->data['status'] ?? 400), 'body' => ['code' => $r->code]]; }
    else {
        $GLOBALS['M']['leads'][] = ['id' => (int) ($r['lead_id'] ?? 0), 'source' => (string) ($body['source'] ?? ''), 'unit' => (string) ($body['unit'] ?? ''), 'idempotent' => !empty($r['idempotent'])];
        $out = ['status' => 200, 'body' => $r];
    }
} elseif ($op === 'rfp') {
    if (($GLOBALS['M']['fail_insert_times'] ?? 0) > 0) { $GLOBALS['M']['fail_insert'] = true; $GLOBALS['M']['fail_insert_times']--; }
    $r = nadlan_rfp_create(new WP_REST_Request($body));
    $GLOBALS['M']['fail_insert'] = false;
    $out = $r instanceof WP_Error ? ['status' => (int) ($r->data['status'] ?? 500), 'body' => ['code' => $r->code, 'data' => $r->data]] : ['status' => 200, 'body' => $r];
} elseif ($op === 'render') {
    // the document as the site renders it (nadlan_rfp_render prints the page and exits)
    $GLOBALS['M']['hooks'] = [];
    nadlan_rfp_render(new WP_REST_Request(['token' => (string) ($body['token'] ?? '')]));
    exit(0);
} elseif ($op === 'state') {
    $docs = [];
    foreach ($GLOBALS['M']['types'] as $id => $t) { if ($t === 'nadlan_rfp') { $docs[] = json_decode($GLOBALS['M']['content'][$id], true); } }
    $out = ['status' => 200, 'body' => ['leads' => $GLOBALS['M']['leads'], 'docs' => $docs]];
}
if ($op !== 'state') { file_put_contents($stateFile, json_encode($GLOBALS['M'], JSON_UNESCAPED_UNICODE)); }
echo json_encode($out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
