<?php
/**
 * UnitDesignRequest (design system v102, HAD-346 Batch 2): the request callback, exercised in memory against the branch's
 * real inc/rfp.php + inc/project-stage.php. No WordPress bootstrap, database, network, mail or file writes; every id, name
 * and number is synthetic. Modelled on Codex's scripts/labs/audit-rfp-dry-run.php (the characterization of the old code),
 * extended to the Batch 2 contract. This is not a browser, WordPress or live acceptance.
 *
 *   php scripts/project-stage/test_rfp_request.php            the cases, JSON out, exit 1 on any failure
 *   php scripts/project-stage/test_rfp_request.php render     prints the rendered document of a full request (for a screenshot)
 */
declare(strict_types=1);
if (PHP_SAPI !== 'cli') { exit(2); }
$ROOT = dirname(__DIR__, 2) . '/plugins/nadlan-config';

require __DIR__ . '/rfp_memory_wp.php';
require $ROOT . '/inc/project-stage.php';
require $ROOT . '/inc/rfp.php';

function reset_mem() {
    $GLOBALS['M'] = ['seq' => 900, 'inserts' => [], 'writes' => [], 'options' => [], 'content' => [], 'names' => [], 'hooks' => [],
        'projects' => ['rainbow-tel-aviv' => 101, 'duo-tel-aviv' => 102, 'fixture-project' => 103, 'private-lab' => 104],
        'types' => [101 => 'nadlan_project', 102 => 'nadlan_project', 103 => 'nadlan_project', 104 => 'nadlan_project', 5001 => 'nadlan_lead', 5002 => 'nadlan_lead'],
        'meta' => [
            103 => ['project_3d_units' => json_encode([['id' => 'fixture-13-e', 'label' => 'Fixture 13 east', 'floor' => 13, 'rooms' => 4, 'sqm' => 120, 'dir' => 'east']])],
            104 => ['_nadlan_private_unit_journey' => 'private-unit-journey-v2'],
            5001 => ['project_slug' => 'rainbow-tel-aviv', 'unit' => '13-e'],
            5002 => ['project_slug' => 'rainbow-tel-aviv', 'unit' => '25-w'],
        ]];
}
function call($payload) {
    $before = count($GLOBALS['M']['inserts']);
    $r = nadlan_rfp_create(new WP_REST_Request($payload));
    $new = array_slice($GLOBALS['M']['inserts'], $before);
    return ['r' => $r, 'status' => $r instanceof WP_Error ? ($r->data['status'] ?? 0) : 200, 'code' => $r instanceof WP_Error ? $r->code : '',
        'inserted' => count($new), 'doc' => $new ? json_decode($GLOBALS['M']['content'][$new[0]], true) : null];
}
function design($project, $unit, $notes = 8) {
    $n = [];
    for ($i = 1; $i <= $notes; $i++) { $n[] = ['target' => ['kind' => $i === 1 ? 'element' : 'item', 'id' => $i === 1 ? 'door-bath' : 'f' . $i], 'label' => 'Note ' . $i, 'text' => $i === 1 ? 'Wider opening, 90 cm (synthetic)' : 'Synthetic note ' . $i]; }
    return ['schema' => 'nadlan-unit-design', 'v' => 1, 'project' => $project, 'unit_id' => $unit, 'geometry_revision' => 'sdedov-sample-2026-07', 'source' => 'designer-3d',
        'layers' => ['space3d' => ['items' => [['id' => 'f1', 'kind' => 'sofa', 'label' => 'Sofa', 'room' => 'Living', 'x' => 1, 'z' => 1, 'ry' => 0.5]]],
                     'plan2d' => ['items' => [['uid' => 'iab12', 'type' => 'sofa3', 'x' => 120, 'y' => 40, 'rot' => 90, 'note' => '']]]],
        'notes' => $n, 'choices' => [['cat' => 'wall', 'label' => 'Walls', 'pick' => 'Gallery white']], 'mood' => 'sunset',
        'checks' => ['performed_checks' => ['footprint_room'], 'warnings' => [['code' => 'outside_room', 'item' => 'f1', 'message' => 'Synthetic warning']]]];
}
$R = [];
function ok($id, $cond, $what) { $GLOBALS['R'][] = ['id' => $id, 'pass' => (bool) $cond, 'what' => $what]; }

if (($argv[1] ?? '') === 'render') {
    reset_mem();
    $key = nadlan_rfp_lead_key(5001, 'rainbow-tel-aviv', '13-e');
    $c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'lang' => 'he', 'name' => 'בדיקה', 'client_ref' => 'synthetic0000render', 'lead_id' => 5001, 'lead_key' => $key,
        'design' => array_replace(design('rainbow-tel-aviv', '13-e'), ['notes' => array_map(function ($i) { return ['target' => ['kind' => 'element', 'id' => 'n' . $i], 'label' => ['דלת חדר הרחצה', 'דלת הממ״ד', 'חלון חדר השינה', 'חלון המטבח', 'דלת הכניסה', 'דלת ההזזה למרפסת', 'הספה', 'המטבח'][$i - 1], 'text' => ['פתח רחב יותר לחדר הרחצה, 90 ס״מ', 'דלת ממ״ד נפתחת החוצה', 'תריס חשמלי', 'חלון גבוה יותר מעל הכיור', 'דלת כניסה רחבה', 'מסילה שקועה ברצפה', 'ספה פינתית', 'אי מטבח'][$i - 1]]; }, range(1, 8)),
            'choices' => [['cat' => 'wall', 'label' => 'צבע הקירות', 'pick' => 'לבן גלריה'], ['cat' => 'floor', 'label' => 'הרצפה', 'pick' => 'אלון בהיר']],
            'layers' => ['space3d' => ['items' => [['id' => 'f1', 'kind' => 'sofa', 'label' => 'ספה', 'room' => 'סלון', 'x' => 1, 'z' => 1, 'ry' => 0.5]]]]])]);
    $tok = $c['doc']['token'];
    $GLOBALS['M']['meta'][$c['r']['url'] ? 901 : 0]['rfp_token'] = $tok;
    // the render looks the token up through WP_Query(meta rfp_token)
    $GLOBALS['M']['types'][901] = 'nadlan_rfp';
    nadlan_rfp_render(new WP_REST_Request(['token' => $tok]));
    exit(0);
}

// the existing rejections stay first (Codex RFP-04..08)
reset_mem();
$c = call(['project' => 'private-lab', 'unit' => '13-e']); ok('RFP-04', $c['status'] === 404 && !$c['inserted'], 'private lab project: 404, nothing written');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '']); ok('RFP-05', $c['status'] === 400 && !$c['inserted'], 'empty unit: 400, nothing written');
$c = call(['project' => 'missing', 'unit' => '13-e']); ok('RFP-06', $c['status'] === 404 && !$c['inserted'], 'missing project: 404');
$c = call(['project' => 'fixture-project', 'unit' => 'fixture-13-e', 'floor' => 999, 'sqm' => 1]); ok('RFP-07', $c['status'] === 200 && $c['doc']['unit']['floor'] === 13 && (float) $c['doc']['unit']['sqm'] === 120.0, 'inventory facts come from the server, not the client');
$c = nadlan_rfp_create(new WP_REST_Request(null)); ok('RFP-08', $c instanceof WP_Error && $c->data['status'] === 400, 'non-object payload: 400');

// RFP-02: unknown units are refused, example units resolve, case is kept
reset_mem();
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => 'unknown-unit']); ok('RFP-02', $c['status'] === 422 && $c['code'] === 'unit_unknown' && !$c['inserted'], 'unknown non-empty unit: 422 unit_unknown, nothing written (was unit=null)');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '40-e']); ok('RFP-02b', $c['status'] === 422 && !$c['inserted'], 'floor 40 on a 39-floor tower: 422');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-x']); ok('RFP-02c', $c['status'] === 422 && !$c['inserted'], 'a side the stage does not have: 422');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e']); ok('UNIT-01', $c['status'] === 200 && $c['doc']['unit']['id'] === '13-e' && $c['doc']['unit']['example'] === true, 'Rainbow example unit 13-e resolves, marked example');
$c = call(['project' => 'duo-tel-aviv', 'unit' => 'n-25-w']); ok('UNIT-02', $c['status'] === 200 && $c['doc']['unit']['id'] === 'N-25-w', 'DUO n-25-w resolves to N-25-w (case kept, not lowercased)');
$c = call(['project' => 'duo-tel-aviv', 'unit' => 'X-25-w']); ok('UNIT-03', $c['status'] === 422, 'a tower DUO does not have: 422');

// RFP-01: the whole design reaches the document, layers apart, checks apart
reset_mem();
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'client_ref' => 'synthetic00000001', 'design' => design('rainbow-tel-aviv', '13-e', 8)]);
$d = $c['doc']['design'] ?? [];
ok('RFP-01', $c['status'] === 200 && count($d['notes'] ?? []) === 8 && ($d['notes'][0]['text'] ?? '') === 'Wider opening, 90 cm (synthetic)', 'all 8 notes in the document, the wider opening first');
ok('RFP-01b', ($d['layers']['space3d']['units'] ?? '') === 'm' && ($d['layers']['plan2d']['units'] ?? '') === 'cm' && ($d['layers']['plan2d']['items'][0]['x'] ?? 0) == 120, '2D (cm, top-left, deg) and 3D (m, centre, rad) stay separate layers, values unconverted');
ok('RFP-01c', ($d['geometry_revision'] ?? '') === 'sdedov-sample-2026-07' && ($d['checks']['warnings'][0]['code'] ?? '') === 'outside_room' && ($c['r']['notes'] ?? 0) === 8, 'geometry revision and checks (apart) kept; the receipt counts 8 notes');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'design' => design('rainbow-tel-aviv', '25-w')]); ok('DESIGN-409', $c['status'] === 409 && $c['code'] === 'design_mismatch' && !$c['inserted'], "a design for 25-w sent as 13-e's request: 409, nothing written");
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'design' => design('duo-tel-aviv', '13-e')]); ok('DESIGN-409b', $c['status'] === 409 && !$c['inserted'], 'the same unit id in another project: 409');
$big = design('rainbow-tel-aviv', '13-e', 120); $big['notes'][0]['text'] = str_repeat('א', 900);
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'design' => $big]); ok('DESIGN-CAP', count($c['doc']['design']['notes']) === 80 && mb_strlen($c['doc']['design']['notes'][0]['text']) === 400, 'caps: 80 notes of 400 characters (never silently beyond)');

// idempotency: a double click / retry / late duplicate gets the same receipt
reset_mem();
$p = ['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'client_ref' => 'synthetic00000002', 'design' => design('rainbow-tel-aviv', '13-e')];
$a = call($p); $b = call($p);
ok('IDEM-01', $a['inserted'] === 1 && $b['inserted'] === 0 && $b['r']['duplicate'] === true && $b['r']['ref'] === $a['r']['ref'], 'the same client_ref twice: one document, the same ref, duplicate=true');
$c = call(array_replace($p, ['unit' => '25-w', 'design' => design('rainbow-tel-aviv', '25-w')])); ok('IDEM-02', $c['status'] === 409 && $c['code'] === 'client_ref_taken' && !$c['inserted'], "A's client_ref reused for B: 409, B untouched");
$GLOBALS['M']['options']['nadlan_rfp_lock_synthetic00000003'] = time(); // a live attempt
$c = call(array_replace($p, ['client_ref' => 'synthetic00000003'])); ok('IDEM-03', $c['status'] === 409 && $c['code'] === 'in_progress' && !$c['inserted'], 'a request still being created: 409 in_progress, no second document');
$GLOBALS['M']['fail_insert'] = true;
$c = call(array_replace($p, ['client_ref' => 'synthetic00000004'])); $GLOBALS['M']['fail_insert'] = false;
$d2 = call(array_replace($p, ['client_ref' => 'synthetic00000004']));
ok('IDEM-04', $c['status'] === 500 && !isset($GLOBALS['M']['options']['nadlan_rfp_lock_synthetic00000004']) && $d2['inserted'] === 1, 'a failed insert releases its lock; the retry with the same client_ref creates the document once');

// Codex RFP-B2-DRAFT (29.9): the races, one reference = one content, periodic angles
$P = ['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'client_ref' => 'synthetic0000race1', 'design' => design('rainbow-tel-aviv', '13-e')];
reset_mem(); $inner = null;
$GLOBALS['M']['hooks']['insert'] = function () use (&$inner, $P) { $inner = call($P); }; // B enters while A inserts (A holds the lock)
$a = call($P);
ok('RACE-01', count($GLOBALS['M']['inserts']) === 1 && $inner['status'] === 409 && $inner['code'] === 'in_progress' && $a['status'] === 200, 'B arrives while A inserts: B gets 409 in_progress, one document');
reset_mem(); $inner = null;
$GLOBALS['M']['hooks']['release'] = function () use (&$inner, $P) { $inner = call($P); }; // B enters just before A releases its lock
$a = call($P);
ok('RACE-02', count($GLOBALS['M']['inserts']) === 1 && ($inner['r']['duplicate'] ?? false) === true && ($inner['r']['ref'] ?? '') === $a['r']['ref'], "B arrives between A's insert and A's release (Codex's two-document case): B gets A's receipt, one document");
reset_mem(); $inner = null;
// B's first look happens before A exists; A then runs to the end; B must look again after its lock
$GLOBALS['M']['hooks']['find'] = function () use (&$inner, $P) { $GLOBALS['M']['hooks']['find'] = null; $inner = call($P); };
$b = call($P);
ok('RACE-03', count($GLOBALS['M']['inserts']) === 1 && ($b['r']['duplicate'] ?? false) === true && $b['r']['ref'] === ($inner['r']['ref'] ?? '-'), 'a stale look-before-lock: the second look after the lock finds the first document, no second one');
reset_mem();
$GLOBALS['M']['options']['nadlan_rfp_lock_synthetic0000race1'] = time() - 600; // an attempt that died ten minutes ago
$c = call($P); $d = call($P);
ok('RACE-04', count($GLOBALS['M']['inserts']) === 1 && $c['status'] === 200 && ($d['r']['duplicate'] ?? false) === true && !isset($GLOBALS['M']['options']['nadlan_rfp_lock_synthetic0000race1']), 'a stale lock is taken over once; the next attempt replays; no lock is left behind');
reset_mem();
$GLOBALS['M']['options']['nadlan_rfp_lock_synthetic0000race1'] = time() - 5; // a live attempt
$c = call($P);
ok('RACE-05', $c['status'] === 409 && $c['code'] === 'in_progress' && !$c['inserted'], 'a fresh lock (a live attempt) is respected: 409 in_progress');
reset_mem();
$a = call($P); $P9 = $P; $P9['design'] = design('rainbow-tel-aviv', '13-e', 9); $c = call($P9);
ok('FP-01', $c['status'] === 409 && $c['code'] === 'client_ref_conflict' && !$c['inserted'], 'the same reference with 9 notes instead of 8: 409 client_ref_conflict, never the old 8-note receipt');
$P9['client_ref'] = 'synthetic0000race2'; $c = call($P9);
ok('FP-02', $c['status'] === 200 && $c['r']['notes'] === 9 && $c['inserted'] === 1, 'the changed content with a new reference: a new document with its 9 notes');
reset_mem();
$turns = design('rainbow-tel-aviv', '13-e');
$turns['layers']['space3d']['items'] = [['id' => 'p', 'kind' => 'chair', 'x' => 0, 'z' => 0, 'ry' => 12 * M_PI / 4], ['id' => 'n', 'kind' => 'chair', 'x' => 0, 'z' => 0, 'ry' => -12 * M_PI / 4], ['id' => 'q', 'kind' => 'chair', 'x' => 0, 'z' => 0, 'ry' => 9 * M_PI / 4]];
$turns['layers']['plan2d']['items'] = [['uid' => 'a', 'type' => 'sofa3', 'x' => 0, 'y' => 0, 'rot' => 450], ['uid' => 'b', 'type' => 'sofa3', 'x' => 0, 'y' => 0, 'rot' => -90], ['uid' => 'c', 'type' => 'sofa3', 'x' => 0, 'y' => 0, 'rot' => 720]];
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'design' => $turns]);
$ry = array_column($c['doc']['design']['layers']['space3d']['items'], 'ry'); $rot = array_column($c['doc']['design']['layers']['plan2d']['items'], 'rot');
$same = function ($a, $b) { return abs(atan2(sin($a - $b), cos($a - $b))) < 1e-5; };
ok('ANG-01', $same($ry[0], 3 * M_PI) && $same($ry[1], -3 * M_PI) && $same($ry[2], M_PI / 4) && abs($ry[0]) <= M_PI && abs($ry[1]) <= M_PI && abs($ry[2] - M_PI / 4) < 1e-5, 'radians: 3π, -3π and 9π/4 keep their orientation, brought into one turn (no 139° error)');
ok('ANG-02', array_map('floatval', $rot) === [90.0, 270.0, 0.0], 'degrees: 450 -> 90, -90 -> 270, 720 -> 0');

// RFP-03: a lead is linked only with its own key, for its own project and unit
reset_mem();
$k = nadlan_rfp_lead_key(5001, 'rainbow-tel-aviv', '13-e');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'lead_id' => 5001]); ok('RFP-03', $c['status'] === 200 && $c['doc']['lead_id'] === 0 && !in_array([5001, 'rfp_id', 901], $GLOBALS['M']['writes'], true), 'a bare lead id: document created, no link, the lead untouched');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'lead_id' => 5001, 'lead_key' => str_repeat('0', 32)]); ok('RFP-03b', $c['doc']['lead_id'] === 0, 'a wrong key: no link');
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'lead_id' => 5002, 'lead_key' => nadlan_rfp_lead_key(5002, 'rainbow-tel-aviv', '13-e')]); ok('RFP-03c', $c['doc']['lead_id'] === 0, "a key made for 13-e on a lead that names 25-w: no link");
$c = call(['project' => 'rainbow-tel-aviv', 'unit' => '13-e', 'lead_id' => 5001, 'lead_key' => $k]); ok('RFP-03d', $c['doc']['lead_id'] === 5001 && ($GLOBALS['M']['meta'][5001]['rfp_id'] ?? 0) > 0 && $c['r']['lead_linked'] === true, 'the right key for the right lead: linked');

$fail = array_filter($R, function ($x) { return !$x['pass']; });
echo json_encode(['mode' => 'memory-only; the branch rfp.php + project-stage.php; synthetic data; NOT live or browser acceptance',
    'rfp_php_sha256' => hash_file('sha256', $ROOT . '/inc/rfp.php'), 'project_stage_php_sha256' => hash_file('sha256', $ROOT . '/inc/project-stage.php'),
    'passed' => count($R) - count($fail), 'failed' => count($fail), 'results' => $R], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE), "\n";
exit($fail ? 1 : 0);
