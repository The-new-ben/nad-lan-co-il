<?php
// Lints and runs registry-snippet.php on the real data with WordPress stubs: php test_summary.php
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
require __DIR__ . '/registry-snippet.php';
$e = s1_sdplan_registry_entry();
$out = s1_sdplan_summary( __DIR__ . '/../data/sdplan.json' );
$ok = isset( $e['sdplan']['data'] ) && strpos( $out, '<table>' ) !== false && substr_count( $out, '<tr>' ) === 74 && strpos( $out, '9,316' ) !== false && ! preg_match( '/[–—]/u', $out );
echo ( $ok ? 'OK' : 'BAD' ), ' summary: ', strlen( $out ), ' bytes, rows ', substr_count( $out, '<tr>' ) - 1, "\n", mb_substr( strip_tags( $out ), 0, 420 ), "\n";
exit( $ok ? 0 : 1 );
