add_action('rest_api_init', function () {
  register_rest_route('nadlan-diag', '/plugin', array(
    'methods' => 'GET',
    'permission_callback' => function () { return current_user_can('manage_options'); },
    'callback' => function () {
      if ( ! function_exists('get_plugin_data') ) { require_once ABSPATH.'wp-admin/includes/plugin.php'; }
      $file = WP_PLUGIN_DIR.'/nadlan-config/nadlan-config.php';
      $data = file_exists($file) ? get_plugin_data($file, false, false) : array();
      $t = get_site_transient('update_plugins');
      $pending = null; $noupd = null;
      if ( is_object($t) && ! empty($t->response['nadlan-config/nadlan-config.php']) ) {
        $r = $t->response['nadlan-config/nadlan-config.php'];
        $pending = array('new_version'=>isset($r->new_version)?$r->new_version:null, 'package'=>isset($r->package)?$r->package:null);
      }
      if ( is_object($t) && ! empty($t->no_update['nadlan-config/nadlan-config.php']) ) {
        $nu = $t->no_update['nadlan-config/nadlan-config.php'];
        $noupd = array('new_version'=>isset($nu->new_version)?$nu->new_version:null, 'package'=>isset($nu->package)?$nu->package:null);
      }
      $auto = (array) get_option('auto_update_plugins', array());
      $dirs = array();
      foreach ( glob(WP_PLUGIN_DIR.'/*', GLOB_ONLYDIR) as $d ) { $dirs[] = basename($d); }
      $dphp = @file_get_contents(WP_PLUGIN_DIR.'/nadlan-config/inc/directory.php');
      $has_new = $dphp !== false ? (strpos($dphp,'nldc-project') !== false) : null;
      $suspect = array_values(array_filter($dirs, function($n){ return $n !== 'nadlan-config' && preg_match('/\.tmp|-old|-backup|upgrade|nadlan-config-/i',$n); }));
      return array(
        'installed_version' => isset($data['Version'])?$data['Version']:null,
        'pending_update'    => $pending,
        'no_update_entry'   => $noupd,
        'auto_update_on'    => in_array('nadlan-config/nadlan-config.php', $auto, true),
        'total_plugin_dirs' => count($dirs),
        'nadlan_dirs'       => array_values(array_filter($dirs, function($n){ return strpos($n,'nadlan') !== false; })),
        'suspect_dirs'      => $suspect,
        'directory_php_has_new_card' => $has_new,
      );
    },
  ));
});