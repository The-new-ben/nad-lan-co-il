add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlan-tools/v1', '/coupon', array('methods'=>'POST','permission_callback'=>function(){return current_user_can('update_plugins');},
    'callback'=>function(){
      if ( ! class_exists('WC_Coupon') ) return array('ok'=>false,'why'=>'no wc');
      $existing = wc_get_coupon_id_by_code('firstmonth');
      if ( ! $existing ) {
        $c = new WC_Coupon();
        $c->set_code('firstmonth');
        $c->set_discount_type('percent');
        $c->set_amount(100);
        $c->set_product_ids(array(476));
        $c->set_usage_limit_per_user(1);
        $c->set_individual_use(true);
        $c->set_description('Free first month for Pro tier - auto-applied at checkout (funnel.php). Renewal engine bills month 2.');
        $c->save();
        $existing = $c->get_id();
      }
      // honest product naming at the moment of payment
      wp_update_post(array('ID'=>476,'post_title'=>'Pro - אנשי מקצוע נדלן (חודש ראשון חינם, לאחר מכן 349 ₪ לחודש)'));
      do_action('litespeed_purge_all'); wp_cache_flush();
      return array('ok'=>true,'coupon_id'=>$existing,'product_title'=>get_the_title(476));
    }));
});
