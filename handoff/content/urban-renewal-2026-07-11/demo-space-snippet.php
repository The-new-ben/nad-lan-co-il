add_action( 'rest_api_init', function () {
  register_rest_route( 'nadlanfix/v1', '/demo-space', array(
    'methods' => 'POST',
    'permission_callback' => function () { return current_user_can( 'manage_options' ); },
    'callback' => function () {
      $exists = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids',
        'meta_query' => array( array( 'key' => 'is_demo', 'value' => '1' ) ) ) );
      if ( $exists ) { return array( 'id' => (int) $exists[0], 'existed' => true ); }
      $id = wp_insert_post( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'private',
        'post_title' => 'דוגמה: הרצל 45, גבעתיים (פרויקט שהושלם)' ), true );
      if ( is_wp_error( $id ) ) { return $id; }
      $dirs = array( 'west', 'south', 'east', 'north' );
      $apts = array();
      for ( $f = 1; $f <= 4; $f++ ) {
        for ( $p = 0; $p < 3; $p++ ) {
          $n = ( $f - 1 ) * 3 + $p + 1;
          $apts[] = array( 'id' => 'f' . $f . '-' . ( $p + 1 ), 'floor' => $f, 'pos' => $p, 'dir' => $dirs[ $p % 4 ],
            'label' => 'דירה ' . $n, 'consent_status' => 'consented',
            'docs' => array( 'id_copy' => true, 'ownership_nesach' => true, 'signed_agreement' => true, 'poa' => true ),
            'contact_note' => '', 'note' => ( 8 === $n ? 'הצטרפו לאחר גישור, נובמבר 2021' : ( 3 === $n ? 'ירושה הוסדרה במרץ 2020' : '' ) ),
            'updated' => '2026-06-30 10:00:00' );
        }
      }
      $updates = array(
        array( 'text' => 'טופס 4 התקבל! מסירת מפתחות החלה. תודה לכל השכנים על שבע שנים של שותפות. נתוני הדגמה.', 'at' => '2026-06-15 09:00:00', 'by' => 0 ),
        array( 'text' => 'הבנייה הושלמה, מתחילים בדיקות מסירה עם המפקח מטעמנו.', 'at' => '2026-03-02 12:00:00', 'by' => 0 ),
        array( 'text' => 'שלד קומה אחרונה הושלם. ביקור דיירים באתר בתיאום המפקח ב-15 לחודש.', 'at' => '2025-06-20 16:30:00', 'by' => 0 ),
        array( 'text' => 'הפינוי הושלם, כולם קיבלו את דמי השכירות לחודשיים הראשונים מראש. ההריסה מתחילה בשבוע הבא.', 'at' => '2023-09-01 08:00:00', 'by' => 0 ),
        array( 'text' => 'היתר הבנייה התקבל! חתמנו על נספחי המפרט הסופיים ובחירת הדירות הושלמה לפי הנוסחה שנקבעה.', 'at' => '2023-04-18 14:00:00', 'by' => 0 ),
        array( 'text' => 'התב"ע אושרה בוועדה המחוזית לאחר שנתיים. 14 קומות, 44 דירות חדשות.', 'at' => '2022-11-07 19:00:00', 'by' => 0 ),
        array( 'text' => 'עדכון חשוב: המחלוקת עם דירה 8 הסתיימה בגישור בעזרת עורך הדין והשמאי - הושגה התאמה בתמורה בשל כיוון הדירה, וכולם חתמו. 100% הסכמה!', 'at' => '2021-11-23 20:00:00', 'by' => 0 ),
        array( 'text' => 'הגענו ל-67%: מבחינה חוקית אפשר לפעול מול סרבנים, אבל הנציגות בחרה קודם בגישור. פגישה עם דירה 8 נקבעה.', 'at' => '2021-05-10 18:00:00', 'by' => 0 ),
        array( 'text' => 'נבחר היזם: אלמוגים בנייה בעמ, לאחר השוואת 4 הצעות עם השמאי. ערבויות חוק מכר מלאות בהסכם.', 'at' => '2021-01-14 19:30:00', 'by' => 0 ),
        array( 'text' => 'הירושה בדירה 3 הוסדרה, צו קיום צוואה התקבל. ממשיכים בהחתמות.', 'at' => '2020-03-08 11:00:00', 'by' => 0 ),
        array( 'text' => 'נבחרו אנשי המקצוע מטעמנו: עורכת דין דיירים ושמאי. שכר הטרחה על היזם שייבחר, כמקובל.', 'at' => '2019-12-02 19:00:00', 'by' => 0 ),
        array( 'text' => 'אסיפת דיירים ראשונה: 10 מתוך 12 הגיעו, נבחרה נציגות של 3. פרוטוקול הופץ לכולם.', 'at' => '2019-09-15 20:00:00', 'by' => 0 ),
      );
      $log = array(
        array( 'stage' => 0, 'at' => '2019-09-15 20:00:00', 'by' => 0 ),
        array( 'stage' => 1, 'at' => '2019-10-01 19:00:00', 'by' => 0 ),
        array( 'stage' => 2, 'at' => '2020-01-10 10:00:00', 'by' => 0 ),
        array( 'stage' => 3, 'at' => '2019-12-02 19:00:00', 'by' => 0 ),
        array( 'stage' => 4, 'at' => '2021-01-14 19:30:00', 'by' => 0 ),
        array( 'stage' => 5, 'at' => '2021-06-01 09:00:00', 'by' => 0 ),
        array( 'stage' => 6, 'at' => '2023-04-18 14:00:00', 'by' => 0 ),
        array( 'stage' => 7, 'at' => '2023-09-01 08:00:00', 'by' => 0 ),
        array( 'stage' => 8, 'at' => '2023-11-15 07:30:00', 'by' => 0 ),
        array( 'stage' => 9, 'at' => '2026-06-15 09:00:00', 'by' => 0 ),
      );
      update_post_meta( $id, 'owner_user_id', get_current_user_id() );
      update_post_meta( $id, 'is_demo', '1' );
      update_post_meta( $id, 'address', 'הרצל 45' );
      update_post_meta( $id, 'city', 'גבעתיים' );
      update_post_meta( $id, 'floors', 4 );
      update_post_meta( $id, 'units_per_floor', 3 );
      update_post_meta( $id, 'track', 'pinui_binui' );
      update_post_meta( $id, 'renewal_stage', 9 );
      update_post_meta( $id, 'renewal_apartments', wp_slash( wp_json_encode( $apts, JSON_UNESCAPED_UNICODE ) ) );
      update_post_meta( $id, 'renewal_updates', wp_slash( wp_json_encode( $updates, JSON_UNESCAPED_UNICODE ) ) );
      update_post_meta( $id, 'renewal_stage_log', wp_slash( wp_json_encode( $log, JSON_UNESCAPED_UNICODE ) ) );
      update_post_meta( $id, 'member_emails', wp_slash( wp_json_encode( array(), JSON_UNESCAPED_UNICODE ) ) );
      update_post_meta( $id, 'invite_token', wp_generate_password( 24, false, false ) );
      return array( 'id' => (int) $id, 'url' => home_url( '/my-renewal/?space=' . (int) $id ) );
    },
  ) );
} );
