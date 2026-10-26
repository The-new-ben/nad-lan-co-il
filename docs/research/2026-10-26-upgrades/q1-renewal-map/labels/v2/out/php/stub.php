<?php
define('ABSPATH', __DIR__);
function add_filter(){}
function add_action(){}
function add_shortcode(){}
function apply_filters($t, $v){ return $v; }
function wp_json_encode($d, $o = 0){ return json_encode($d, $o); }
require __DIR__ . '/inc/urban-map.php';
echo nadlan_ur_map_v2_boot();
