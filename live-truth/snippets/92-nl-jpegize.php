add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/jpegize', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      require_once ABSPATH.'wp-admin/includes/image.php';
      $ids = range(5125,5136); $out=array();
      foreach ($ids as $id) {
        $file = get_attached_file($id);
        if (!$file || !file_exists($file)) { $out[$id]='missing'; continue; }
        if (preg_match('/\.jpe?g$/i',$file)) { $out[$id]='already-jpg'; continue; }
        $ed = wp_get_image_editor($file);
        if (is_wp_error($ed)) { $out[$id]='editor: '.$ed->get_error_message(); continue; }
        $ed->set_quality(82);
        $new = preg_replace('/\.png$/i','.jpg',$file);
        $saved = $ed->save($new,'image/jpeg');
        if (is_wp_error($saved)) { $out[$id]='save: '.$saved->get_error_message(); continue; }
        update_attached_file($id,$saved['path']);
        wp_update_post(array('ID'=>$id,'post_mime_type'=>'image/jpeg'));
        wp_update_attachment_metadata($id, wp_generate_attachment_metadata($id,$saved['path']));
        $out[$id]=array('old'=>filesize($file),'new'=>filesize($saved['path']));
        /* PNG original kept on disk deliberately */
      }
      delete_transient('nadlan_default_tour_v1');
      do_action('litespeed_purge_all'); wp_cache_flush();
      return $out;
    }));
});
