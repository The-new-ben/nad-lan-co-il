add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/wcstate', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      $products = get_posts(array('post_type'=>'product','post_status'=>'any','posts_per_page'=>20));
      $list = array();
      foreach ($products as $p) { $list[] = array('id'=>$p->ID,'title'=>$p->post_title,'status'=>$p->post_status,'price'=>get_post_meta($p->ID,'_price',true)); }
      $gw = get_option('woocommerce_greeninvoice_settings');
      $gwshape = array();
      if (is_array($gw)) foreach ($gw as $k=>$v) { $gwshape[$k] = is_string($v) ? ($v===''?'EMPTY':(strlen($v)>20?substr($v,0,4).'...('.strlen($v).')':$v)) : gettype($v); }
      return array('products'=>$list,'gateway_settings'=>$gwshape,
        'checkout_page'=> function_exists('wc_get_checkout_url') ? wc_get_checkout_url() : 'n/a',
        'currency'=> get_option('woocommerce_currency'));
    }));
});
