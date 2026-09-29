<?php
/**
 * UnitDesignRequest v102, Codex LEAD-E2E-UNIT-CONTRACT (29.9): the REAL /nadlan/v1/lead callback (inc/conversion-cta.php)
 * in both branches, lead test mode OFF and ON (inc/lead-e2e.php), chained into the real nadlan_rfp_create (inc/rfp.php).
 * Memory only (rfp_memory_wp.php): no WordPress, database, network; email is recorded, never sent. Synthetic buyers only.
 *   php scripts/project-stage/test_lead_contract.php      JSON out, exit 1 on any failure
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
$LEAD = $GLOBALS['WP_ROUTES']['nadlan/v1/lead']['callback'] ?? null;
if (!$LEAD) { fwrite(STDERR, "the /lead route was not registered\n"); exit(2); }

function reset_mem($e2e) {
    $GLOBALS['M'] = ['seq' => 900, 'inserts' => [], 'writes' => [], 'options' => ['nadlan_feature_lead_e2e' => $e2e ? '1' : '0'], 'content' => [], 'names' => [], 'hooks' => [],
        'transients' => [], 'mail' => [], 'projects' => ['rainbow-tel-aviv' => 101, 'duo-tel-aviv' => 102],
        'types' => [101 => 'nadlan_project', 102 => 'nadlan_project'], 'meta' => []];
}
function lead($body) { $r = ($GLOBALS['LEAD'])(new WP_REST_Request($body)); return $r instanceof WP_Error ? ['error' => $r->code, 'status' => $r->data['status'] ?? 0] : $r; }
function persisted($id) { return ['project' => (string) get_post_meta($id, 'project_slug', true), 'unit' => (string) get_post_meta($id, 'unit', true)]; }
function rfp($body) { $r = nadlan_rfp_create(new WP_REST_Request($body)); return $r instanceof WP_Error ? ['error' => $r->code] : $r; }
$buyer = ['name' => 'בדיקה סינתטית', 'phone' => '0500000000', 'source' => 'apartment-designer', 'consent' => 1];
$R = [];
function ok($id, $cond, $what) { $GLOBALS['R'][] = ['id' => $id, 'pass' => (bool) $cond, 'what' => $what]; }

foreach ([false, true] as $e2e) {
    $tag = $e2e ? 'ON' : 'OFF';
    reset_mem($e2e);
    $a = lead($buyer + ['project_slug' => 'rainbow-tel-aviv', 'unit' => '13-e']);
    ok("$tag-1", !empty($a['lead_id']) && !empty($a['lead_key']) && persisted($a['lead_id']) === ['project' => 'rainbow-tel-aviv', 'unit' => '13-e'],
       "lead test mode $tag: a request for 13-e gets a lead that names 13-e, and its key");
    $d = rfp(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'lead_id' => $a['lead_id'] ?? 0, 'lead_key' => $a['lead_key'] ?? '', 'client_ref' => 'synthetic' . $tag . '00000001']);
    ok("$tag-2", ($d['lead_linked'] ?? false) === true, "lead test mode $tag: the request document for 13-e is linked to that lead");
    $again = lead($buyer + ['project_slug' => 'rainbow-tel-aviv', 'unit' => '13-e']);
    if ($e2e) {
        ok("ON-3", ($again['lead_id'] ?? 0) === $a['lead_id'] && !empty($again['idempotent']) && ($again['lead_key'] ?? '') === $a['lead_key'], 'test mode ON: the same request again is the same lead (idempotent), with the same key');
    } else {
        ok("OFF-3", !empty($again['lead_id']) && !empty($again['lead_key']) && persisted($again['lead_id'])['unit'] === '13-e', 'test mode OFF: the same request again is recorded again (no de-duplication on this path, as before), with its own matching key');
    }
    $b = lead($buyer + ['project_slug' => 'rainbow-tel-aviv', 'unit' => '25-w']);
    ok("$tag-4", !empty($b['lead_id']) && $b['lead_id'] !== $a['lead_id'] && persisted($b['lead_id'])['unit'] === '25-w' && persisted($a['lead_id'])['unit'] === '13-e' && !empty($b['lead_key']),
       "lead test mode $tag: the same buyer asking about 25-w gets a NEW lead naming 25-w; the 13-e lead keeps 13-e");
    $c = lead($buyer + ['project_slug' => 'duo-tel-aviv', 'unit' => 'N-25-w']);
    ok("$tag-5", !empty($c['lead_id']) && !in_array($c['lead_id'], [$a['lead_id'], $b['lead_id']], true) && persisted($c['lead_id'])['project'] === 'duo-tel-aviv',
       "lead test mode $tag: another project with no card id is another lead");
    $d1 = lead($buyer + ['project_slug' => 'rainbow-tel-aviv', 'unit' => '7-n', 'card_id' => 101]);
    $d2 = lead($buyer + ['project_slug' => 'rainbow-tel-aviv', 'unit' => '9-s', 'card_id' => 101]);
    ok("$tag-6", !empty($d1['lead_id']) && !empty($d2['lead_id']) && $d1['lead_id'] !== $d2['lead_id'] && persisted($d2['lead_id'])['unit'] === '9-s',
       "lead test mode $tag: the same project card, two units: two leads");
    $x = rfp(['project' => 'rainbow-tel-aviv', 'unit' => '25-w', 'lead_id' => $a['lead_id'], 'lead_key' => $a['lead_key'], 'client_ref' => 'synthetic' . $tag . '00000002']);
    ok("$tag-7", ($x['lead_linked'] ?? true) === false, "lead test mode $tag: 13-e's lead and key cannot be attached to a 25-w document");
    ok("$tag-8", nadlan_rfp_lead_key_for($a['lead_id'], 'rainbow-tel-aviv', '25-w') === '', "lead test mode $tag: no key is ever issued for a lead whose persisted unit is another one");
}
// requests with no project/unit keep exactly the old fingerprint (no change for the site's other forms)
$f = ['name' => 'x', 'phone' => '0500000000', 'email' => ''];
ok('FP-OLD', nadlan_lead_e2e_fingerprint_base(0, $f) === md5('0|' . '|0500000000' . '|x'), 'a lead without project/unit: the same fingerprint as before the change');
$fail = array_filter($R, function ($x) { return !$x['pass']; });
echo json_encode(['mode' => 'memory-only; the branch conversion-cta.php (/lead) + lead-e2e.php + rfp.php; synthetic buyers; email recorded, never sent',
    'sha256' => ['conversion-cta.php' => hash_file('sha256', $ROOT . '/inc/conversion-cta.php'), 'lead-e2e.php' => hash_file('sha256', $ROOT . '/inc/lead-e2e.php'), 'rfp.php' => hash_file('sha256', $ROOT . '/inc/rfp.php')],
    'passed' => count($R) - count($fail), 'failed' => count($fail), 'results' => $R], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), "\n";
exit($fail ? 1 : 0);
