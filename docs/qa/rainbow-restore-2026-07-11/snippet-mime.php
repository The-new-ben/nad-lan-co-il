// temp: allow glb+svg media upload during the restore window (benign filters only)
add_filter( 'upload_mimes', function ( $m ) {
	$m['glb'] = 'model/gltf-binary';
	$m['svg'] = 'image/svg+xml';
	return $m;
} );
add_filter( 'wp_check_filetype_and_ext', function ( $data, $file, $filename, $mimes ) {
	if ( preg_match( '/\.glb$/i', $filename ) ) { $data['ext'] = 'glb'; $data['type'] = 'model/gltf-binary'; }
	if ( preg_match( '/\.svg$/i', $filename ) ) { $data['ext'] = 'svg'; $data['type'] = 'image/svg+xml'; }
	return $data;
}, 10, 4 );
