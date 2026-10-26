<?php
define( 'ABSPATH', __DIR__ );
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return (string) $s; }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function get_option( $k, $d = false ) { return $d; }
function add_filter() {} function add_action() {} function is_page() { return false; } function apply_filters( $t, $v ) { return $v; } function wc_get_product() { return null; }
function current_user_can() { return false; }
require __DIR__ . '/../../../../plugins/nadlan-config/inc/advertise-tiers.php';
echo nadlan_adt_render();
