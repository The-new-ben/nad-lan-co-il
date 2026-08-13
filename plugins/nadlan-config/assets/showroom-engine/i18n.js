/* ============================================================================
   NadLan Showroom - i18n LAYER  (window.NADLAN_I18N)
   ----------------------------------------------------------------------------
   Every UI string the engine renders is a key here. No chrome text is hardcoded
   in HTML or engine.js. In WordPress these tables become the theme's translation
   files (or pll__/__() calls); the engine swaps to a server t() with no markup
   change. See NOTES.md for the full key inventory.

   HE + EN are complete. FR / RU / AR are SCAFFOLDED: every slot exists (cloned
   from EN as a placeholder) so the owner's translators fill values in place.
   Resolution order in t():  lang -> en -> he -> key.
   Marketing / SEO PROSE is NOT here - that lives in data.js content blocks as
   owner-filled placeholders. These are functional labels only.
   ============================================================================ */
(function () {
  "use strict";

  var HE = {
    /* brand + languages */
    brand: "נדל\u05F4ן", brand_sub: "תצוגת פרויקטים",
    lang_he: "עברית", lang_en: "English", lang_fr: "Français", lang_ru: "Русский", lang_ar: "العربية",
    city_tlv: "תל אביב",

    /* project display names (data references these) */
    proj_ashira_name: "Ashira", proj_rainbow_name: "Rainbow", proj_dimri_name: "דימרי ימה",

    /* directions (enum -> label) */
    dir_west: "מערב", dir_east: "מזרח", dir_north: "צפון", dir_south: "דרום",
    "dir_south-west": "דרום-מערב", "dir_north-west": "צפון-מערב", "dir_south-east": "דרום-מזרח", "dir_north-east": "צפון-מזרח",
    /* statuses */
    status_available: "להמחשה", status_reserved: "בעדיפות", status_sold: "נמכרה", status_unknown: "סטטוס לבירור",
    /* orientation cues on the 3D stage */
    orient_sea: "הים", orient_reading: "ארובת רידינג", orient_district: "רובע שדה דב", orient_district_north: "המשך הרובע",
    view_sea_reading: "ים וארובת רידינג", view_district: "רובע שדה דב", view_sea_court: "ים וחצר", view_urban: "מרקם עירוני", view_garden: "גן פנימי", view_sea: "ים פתוח", view_park: "פארק", view_coast: "קו החוף", view_court: "חצר פנימית", view_promenade: "טיילת",

    /* composition templates */
    apt_word: "דירה", rooms_label: "{n} חדרים", floor_label: "קומה {n}", sqm_unit: "מ\u05F4ר",
    unit_short: "דירה {label} · קומה {floor}",
    price_on_request: "אומדן לפי פנייה",

    /* nav */
    nav_projects: "פרויקטים", nav_areas: "אזורים", nav_guides: "מידע ומדריכים", nav_list: "שיווק עם נדל\u05F4ן",

    secnav_building: "בניין", secnav_apartments: "דירות", secnav_environment: "סביבה", secnav_media: "מדיה", secnav_info: "מידע", secnav_aria: "ניווט בעמוד",
    secnav_price: "מחיר",
    price_eyebrow: "מחיר ואומדן", price_title: "מחיר ואומדן באזור",
    price_estimate_label: "טווח עסקאות מדווחות", price_estimate_label_psqm: "טווח מחיר למ\u05F4ר",
    price_avg_psqm: "ממוצע מבוקש {v} למ\u05F4ר", per_sqm_short: "למ\u05F4ר",
    price_nonbinding: "אומדן לא מחייב · אינו מחיר יזם או הצעה", price_updated_label: "עודכן",
    price_pending: "אומדן מחיר ועסקאות השוואה יוצגו עם קבלת נתונים מאומתים.",
    comps_title: "עסקאות שנמכרו באזור", comps_pending: "עסקאות השוואה יוצגו עם קבלת נתונים מאומתים.",
    comps_col_date: "תאריך", comps_col_rooms: "חדרים", comps_col_sqm: "שטח", comps_col_total: "מחיר", comps_col_psqm: "למ\u05F4ר",
    comps_source: "מקור: מדלן / רשות המסים",
    /* hero / intent (block 2) */
    hero_eyebrow: "רובע שדה דב · מול הים",
    hero_cta_primary: "השארת פרטים",
    hero_cta_secondary: "לבחירת דירה",
    fact_floors: "קומות", fact_homes: "דירות לבחירה", fact_homes_total: "דירות בפרויקט", fact_from_floor: "קומות גבוהות",

    /* 3D theater (block 3) */
    theater_eyebrow: "תצוגת הפרויקט",
    theater_title: "בוחרים דירה מתוך הבניין",
    theater_hint: "גררו לסיבוב · הקישו על דירה",
    view_3d: "תלת מימד", view_facade: "חזית",
    generic_model: "המחשה כללית - לא מבנה הפרויקט",
    light_day: "יום", light_dusk: "שקיעה", light_night: "לילה",
    cotour_start: "שיתוף סיור חי", cotour_live: "משדרים סיור חי", cotour_copied: "קישור הצטרפות הועתק",
    cotour_following: "סיור מודרך פעיל - המסך עוקב אחרי המציג",
    legend_available: "להמחשה, כפוף לאישור היזם", legend_reserved: "בעדיפות", legend_sold: "נמכרה",
    loading_model: "טוען תצוגה…",
    model_error: "התצוגה התלת ממדית לא נטענה. נציג חומר מאושר כאשר יעלה לפרויקט.",
    map_error_missing_token: "Mapbox token missing",
    map_error_missing_coords: "חסרות קואורדינטות למפה",
    map_error_library: "מפה לא נטענה",

    /* facade backup (block 4) */
    facade_title: "בחירה מהירה מהחזית",
    facade_sub: "כל ריבוע הוא דירה. מתאים גם למובייל ולבחירה מדויקת.",
    concept_badge: "קונספט / לא חומר רשמי",
    facade_concept_note: "תמונת קונספט בלבד. בחירת דירה על חזית תיפתח אחרי העלאת חזית רשמית מהיזם.",
    facade_missing_title: "חסרה חזית רשמית",
    facade_missing_text: "לא נטען קובץ חזית מאושר לפרויקט, ולכן בחירת דירה על חזית לא מוצגת.",

    /* apartment panel (block 5) */
    panel_prompt: "בחרו דירה מהבניין או מהחזית",
    panel_floor: "קומה", panel_rooms: "חדרים", panel_sqm: "שטח", panel_balcony: "מרפסת",
    panel_view: "נוף", panel_dir: "כיוון", panel_status: "סטטוס", panel_price: "אומדן",
    tab_plan: "תכנית", tab_view: "הנוף מהחלון", tab_tour: "סיור",
    plan_coming: "תכנית הדירה תוצג לאחר קבלת תוכנית מכר מאושרת.",
    view_coming: "מבט מהדירה יוצג לאחר אימות מיקום מול היזם.",
    interior_generic_note: "הדמיית פנים כללית להמחשה בלבד, טרם התקבלו תוכניות מהיזם",
    btn_rfp: "בנו לי הצעה לדירה הזו",
    btn_brochure: "עמוד דירה להדפסה (PDF)",
    btn_winview: "להמשיך למפה החיה עם כל הסביבה",
    winview_note: "גררו להביט סביב - הצידה, למטה ולמעלה. גובה הקומה והכיוון אמיתיים; להמחשה, לא צילום מהדירה.",
    winview_title: "כך נראה הנוף מהחלון של הדירה הזאת",
    winview_turn_left: "להביט שמאלה",
    winview_turn_right: "להביט ימינה",
    winview_fs: "מסך מלא", winview_fs_exit: "יציאה ממסך מלא",
    tab_view_dir: "הנוף מהחלון · {d}",
    sun_sim_label: "סימולציית שמש", sun_time_aria: "בחירת שעה ביום",
    sun_sim_note: "מסלול שמש אמיתי ליום שוויון לפי קו הרוחב של הפרויקט. גיאומטרי בלבד, ללא הצללות מבניינים שכנים.",
    sun_direct_now: "שמש ישירה עכשיו",
    filter_active: "מסונן: {f}", filter_show_all: "הצג הכל",
    view_interior_label: "הדמיית פנים לדירה",
    fp_salon: "סלון ופינת אוכל", fp_kitchen: "מטבח", fp_mamad: "ממ״ד",
    fp_master: "חדר שינה הורים", fp_bed: "חדר שינה", fp_balcony: "מרפסת",
    fp_aria: "סיור פנימי בדירה - גררו כדי להביט סביב",
    fp_hint: "גררו להסתכל · לחצו על דלת למעבר חדר",
    fp_tag: "הדמיה סכמטית להמחשה - נוצרה מנתוני הדירה",
    fp_to_room: "אל {room}", fp_area_approx: "{label} · כ־{area} מ״ר",
    tour_coming: "סיור פנים יוצג כאשר יתקבל קישור מאושר.",
    dt_exterior: "חזית הבניין", dt_street_entrance: "כניסה מהרחוב", dt_entrance: "כניסה",
    dt_lobby: "לובי", dt_stairwell: "חדר מדרגות", dt_elevator: "מעלית", dt_entry_hall: "מבואה",
    dt_living_room: "סלון", dt_kitchen: "מטבח", dt_master_bedroom: "חדר שינה הורים",
    dt_second_bedroom: "חדר שינה", dt_bathroom: "חדר רחצה", dt_balcony: "מרפסת",
    dtour_tag: "סיור בדירת דוגמה סטנדרטית - הדמיה להמחשה. סיור ייעודי מהיזם יחליף אותו עם קבלתו.",
    dtour_hint: "גררו להביט · חצים או דלתות למעבר חלל",
    dtour_next: "לחלל הבא", dtour_prev: "לחלל הקודם",
    dtour_tag_dedicated: "הדמיות ייעודיות לפרויקט - להמחשה בלבד.",
    dtour_tag_premium: "סיור בדירת דוגמה פרימיום - הדמיה להמחשה. סיור ייעודי מהיזם יחליף אותו עם קבלתו.",
    mortgage_est: "החזר חודשי משוער: {v}",
    mortgage_note: "לפי מימון 70%, 25 שנה, ריבית 5% - אומדן בלבד, אינו הצעת מימון.",
    dtour_tag_units: "הדמיות פנים של דירות בפרויקט - להמחשה בלבד.",
    tour_title: "סיור פנים", tour_open: "פתיחת סיור וירטואלי", tour_open_pano: "פתיחת סיור 360", tour_lazy_hint: "לחיצה אחת ואתם בפנים.", tour_pending: "סיור 360 מהיזם יעלה כאן עם אישורו. בינתיים אפשר לצעוד בתוך כל דירה דרך לוח הדירות למטה.",
    btn_inquire: "מעניין אותי", btn_save: "שמירה", btn_saved: "נשמר", btn_compare: "להשוואה",
    btn_compared: "בהשוואה", btn_share: "שיתוף", btn_close: "סגירה", link_copied: "הקישור הועתק",

    /* inventory (block 6) */
    inventory_title: "כל הדירות בפרויקט",
    inventory_sub: "בחירה כאן מסמנת את הדירה גם בבניין וגם בחזית.",
    filter_all: "הכל", filter_available: "זמינות", filter_3: "3 חד׳", filter_4: "4 חד׳", filter_5: "5 חד׳",
    filter_favs: "שמורות",
    results_count: "{n} דירות",
    recent_title: "נצפו לאחרונה",
    scarcity_last: "הדירה הזמינה האחרונה של {rooms} חדרים בפרויקט",
    scarcity_left: "נותרו {n} דירות {rooms} חדרים זמינות בפרויקט",
    scarcity_show: "להצגתן בבניין",
    btn_wa_share: "וואטסאפ",
    reset_view: "חזרה לתצוגה מלאה",
    sun_hours: "כ-{h} שעות שמש ישירה ביום שוויון",
    sun_note: "הערכה גיאומטרית לפי כיוון וקו רוחב בלבד, ללא הצללות סביבה",
    compare_top: "הבולטת לפי שטח, קומה ומרפסת",

    /* apartment studio */
    nlst_open: "סטודיו עיצוב הדירה",
    nlst_title: "סטודיו עיצוב הדירה",
    nlst_auto: "סדרו לי אוטומטית", nlst_auto_note: "נקודת פתיחה לעריכה - לא תכנון מחייב",
    nlst_it_tvunit: "מזנון טלוויזיה", nlst_it_armchair: "כורסה", nlst_it_dresser: "שידה",
    nlst_it_rug: "שטיח", nlst_it_plant: "עציץ", nlst_it_bench: "ספסל פינת אוכל",
    nlst_honest: "תרשים סכמטי להמחשה לפי נתוני הדירה - אינו תוכנית מכר",
    nlst_palette: "רהיטים ותבניות (מידות אמיתיות)",
    nlst_cm: 'ס"מ',
    nlst_notes: "הערות ובקשות מיוחדות",
    nlst_notes_ph: "לדוגמה: הכנה לנקודת חשמל למטען רכב, הרחבת דלת אמבטיה, הנמכת מתגים...",
    nlst_pros: "אדריכלים ומעצבים מהמאגר",
    nlst_rotate: "סיבוב",
    nlst_undo: "ביטול פעולה",
    nlst_note: "הערה לפריט",
    nlst_delete: "מחיקה",
    nlst_clear: "ניקוי הכל",
    nlst_send_rfp: "צירוף התכנון לבקשת הצעה",
    nlst_send_wa: "שיתוף בוואטסאפ",
    nlst_video: "שיחת וידאו עם נציג",
    nlst_video_msg: "אשמח לתאם שיחת וידאו על התכנון הזה:",
    nlst_count: "{n} פריטים בתכנון",
    nlst_scale: "מעטפת סכמטית {m} מ'",
    nlst_note_ph: "הערה לפריט (עד 200 תווים)",
    nlst_sum_head: "תכנון דירה {label} · קומה {floor} · {project}",
    nlst_salon: "סלון ומטבח פתוח", nlst_kitchen: "מטבח", nlst_master: "חדר הורים", nlst_bed: "חדר", nlst_bath: "רחצה ושירותים",
    nlst_it_sofa2: "ספה זוגית", nlst_it_sofa3: "ספה תלת מושבית", nlst_it_bed_double: "מיטה זוגית", nlst_it_bed_single: "מיטת יחיד",
    nlst_it_table4: "שולחן אוכל 4", nlst_it_table6: "שולחן אוכל 6", nlst_it_wardrobe: "ארון קיר", nlst_it_fridge: "מקרר",
    nlst_it_washer: "מכונת כביסה", nlst_it_desk: "שולחן עבודה", nlst_it_crib: "מיטת תינוק", nlst_it_bath: "אמבטיה",
    nlst_it_wheel: "רדיוס סיבוב כיסא גלגלים 150", nlst_it_door80: "פתח דלת נגיש 80",

    /* media (block 7) */
    media_title: "גלריה, וידאו וסיור",
    media_empty: "חומרי מדיה יתווספו עם קבלתם מהיזם.",
    media_gallery: "גלריה", media_video: "וידאו", media_tour: "סיור וירטואלי",

    /* the complete world (block 8) */
    world_eyebrow: "הסביבה",
    world_title: "כל מה שמסביב",
    world_sub: "מיקום, תחבורה, חינוך, פנאי ומסחר, לצד נתוני הרובע.",
    map_title: "מפת הסביבה", map_project_here: "כאן הפרויקט",
    spoke_transport: "תחבורה", spoke_education: "חינוך", spoke_facilities: "פנאי ומסחר", spoke_anchor: "ציוני דרך",
    spoke_reading_tower: "ארובת רידינג", spoke_beach: "חוף וטיילת", spoke_light_rail: "הרכבת הקלה, הקו הירוק",
    spoke_yarkon_park: "פארק הירקון", spoke_school: "מוסדות חינוך", spoke_commercial: "מרכז מסחרי", spoke_road: "צירי תנועה ראשיים",
    stat_plan: "תכנית מתאר", stat_units: "דירות מתוכננות", stat_dunams: "דונם", stat_residents: "תושבים מתוכננים",
    area_sde_dov: "רובע שדה דב", area_sde_dov_blurb: "⟦תיאור קצר של הרובע⟧",
    nearby_projects: "פרויקטים סמוכים",

    /* investor (block 9) */
    investor_title: "קונים מחו\u05F4ל",
    investor_sub: "ליווי לרוכשים בינלאומיים: תהליך, מסמכים, מימון ומיסוי.",
    investor_pt_process: "תהליך רכישה מסודר", investor_pt_legal: "ליווי משפטי ומס", investor_pt_finance: "מימון ומטבע",
    investor_cta: "לתיאום שיחה",

    /* SEO body (block 10) - heading chrome only; prose from data.content */
    seo_eyebrow: "על הפרויקט",
    faq_title: "שאלות נפוצות",

    /* inquiry (block 11) - the money moment */
    form_title: "מעוניינים בדירה? נחזור אליכם",
    form_sub: "השאירו פרטים ונחזור עם המידע על הדירה שבחרתם.",
    form_name: "שם מלא", form_phone: "טלפון", form_email: "אימייל (לא חובה)",
    form_submit: "שליחת פנייה", form_submitting: "שולח…",
    form_success: "תודה! קיבלנו את הפנייה ונחזור אליכם בקרוב.",
    form_error: "יש למלא שם וגם טלפון או אימייל.",
    form_consent: "הפנייה אינה מהווה הזמנה או התחייבות. נתוני הדגמה.",
    form_unit_ctx: "הפנייה מתייחסת לדירה {label} · קומה {floor} · {rooms} חד׳",
    form_no_unit: "פנייה כללית על הפרויקט",
    whatsapp_cta: "וואטסאפ", sticky_cta: "מעניין אותי",

    /* compare */
    compare_title: "השוואת דירות",
    compare_empty: "הוסיפו דירות להשוואה",
    compare_clear: "ניקוי",
    compare_inquire: "פנייה על הנבחרת",

    /* disclaimer (block 12) + badges */
    demo_badge: "הדמיה להמחשה",
    disclaimer_title: "הצהרת המחשה",
    disclaimer_text: "המודל, החזית והדירות הם המחשה ראשונית ואינם תוכנית מכר או מלאי מאושר. מחיר וזמינות יש לאמת מול היזם. אין באמור הצעה או התחייבות.",

    /* home */
    home_hero_eyebrow: "נדל\u05F4ן בישראל · פרויקטים חדשים",
    home_hero_title: "בוחרים דירה, פרויקט וסביבה, לפני שמתקדמים",
    home_hero_sub: "מבט אמיתי על הפרויקט, הדירות והסביבה, במקום אחד.",
    home_search_area: "אזור", home_search_type: "סוג", home_search_cta: "חיפוש",
    home_gallery_eyebrow: "הפרויקטים שלנו",
    home_gallery_title: "פרויקטים חדשים בשדה דב",
    home_gallery_sub: "בחרו פרויקט ובחנו אותו דירה-דירה.",
    card_explore: "כניסה לפרויקט", card_units: "{n} דירות לבחירה",
    home_areas_title: "לפי אזור",
    home_areas_sub: "כניסה לפי רובע ואזור.",
    home_list_title: "משווקים פרויקט?",
    home_list_sub: "הציגו את הפרויקט שלכם בתצוגה תלת-ממדית שמייצרת פניות.",
    home_list_cta: "שיווק עם נדל\u05F4ן",

    /* footer */
    footer_tagline: "תצוגת פרויקטים ונדל\u05F4ן בישראל",
    footer_rights: "© נדל\u05F4ן · כל הנתונים להמחשה עד לאישור היזם",
    footer_col_projects: "פרויקטים", footer_col_areas: "אזורים", footer_col_company: "החברה", footer_col_langs: "שפות"
  };

  var EN = {
    brand: "NadLan", brand_sub: "Project showroom",
    lang_he: "עברית", lang_en: "English", lang_fr: "Français", lang_ru: "Русский", lang_ar: "العربية",
    city_tlv: "Tel Aviv",
    proj_ashira_name: "Ashira", proj_rainbow_name: "Rainbow", proj_dimri_name: "Dimri Yama",
    dir_west: "West", dir_east: "East", dir_north: "North", dir_south: "South",
    "dir_south-west": "South-west", "dir_north-west": "North-west", "dir_south-east": "South-east", "dir_north-east": "North-east",
    status_available: "Illustrative", status_reserved: "On hold", status_sold: "Sold", status_unknown: "Status on request",
    orient_sea: "The sea", orient_reading: "Reading Tower", orient_district: "Sde Dov district", orient_district_north: "District, north",
    view_sea_reading: "Sea & Reading Tower", view_district: "Sde Dov district", view_sea_court: "Sea & courtyard", view_urban: "Urban fabric", view_garden: "Inner garden", view_sea: "Open sea", view_park: "Park", view_coast: "Coastline", view_court: "Inner court", view_promenade: "Promenade",
    apt_word: "Apartment", rooms_label: "{n} rooms", floor_label: "Floor {n}", sqm_unit: "m\u00B2",
    unit_short: "Apt {label} · Floor {floor}",
    price_on_request: "Estimate on request",
    nav_projects: "Projects", nav_areas: "Areas", nav_guides: "Guides", nav_list: "List with us",
    secnav_building: "Building", secnav_apartments: "Apartments", secnav_environment: "Surroundings", secnav_media: "Media", secnav_info: "Info", secnav_aria: "On-page navigation",
    secnav_price: "Price",
    price_eyebrow: "Price & estimate", price_title: "Price & area estimate",
    price_estimate_label: "Recorded transaction range", price_estimate_label_psqm: "Price per m\u00B2 range",
    price_avg_psqm: "Avg asking {v}/m\u00B2", per_sqm_short: "/m\u00B2",
    price_nonbinding: "Non-binding estimate, not a developer price or offer", price_updated_label: "Updated",
    price_pending: "A price estimate and comparable sales will appear once verified data is available.",
    comps_title: "Recent sales nearby", comps_pending: "Comparable sales will appear once verified data is available.",
    comps_col_date: "Date", comps_col_rooms: "Rooms", comps_col_sqm: "Area", comps_col_total: "Price", comps_col_psqm: "/m\u00B2",
    comps_source: "Source: Madlan / Israel Tax Authority",
    hero_eyebrow: "Sde Dov district · By the sea",
    hero_cta_primary: "Enquire",
    hero_cta_secondary: "Choose an apartment",
    fact_floors: "Floors", fact_homes: "Homes to choose", fact_homes_total: "Homes in project", fact_from_floor: "High floors",
    theater_eyebrow: "Project showroom",
    theater_title: "Choose an apartment from the building",
    theater_hint: "Drag to rotate · tap an apartment",
    view_3d: "3D", view_facade: "Facade",
    generic_model: "General illustration - not this project's building",
    light_day: "Day", light_dusk: "Dusk", light_night: "Night",
    cotour_start: "Share live tour", cotour_live: "Broadcasting live tour", cotour_copied: "Join link copied",
    cotour_following: "Guided tour active - your screen follows the presenter",
    legend_available: "Illustrative, subject to developer confirmation", legend_reserved: "On hold", legend_sold: "Sold",
    loading_model: "Loading view…",
    model_error: "The 3D model did not load. Approved material will appear once it is added to this project.",
    map_error_missing_token: "Mapbox token missing",
    map_error_missing_coords: "Map coordinates missing",
    map_error_library: "Map failed to load",
    facade_title: "Quick pick from the facade",
    facade_sub: "Each square is an apartment. Ideal on mobile and for precise picking.",
    concept_badge: "Concept / not official material",
    facade_concept_note: "Concept image only. Apartment picking on the facade will open after an official facade is uploaded by the developer.",
    facade_missing_title: "Official facade missing",
    facade_missing_text: "No approved facade file is loaded for this project, so facade apartment picking is not shown.",
    panel_prompt: "Select an apartment from the building or the facade",
    panel_floor: "Floor", panel_rooms: "Rooms", panel_sqm: "Area", panel_balcony: "Balcony",
    panel_view: "View", panel_dir: "Facing", panel_status: "Status", panel_price: "Estimate",
    tab_plan: "Plan", tab_view: "Window view", tab_tour: "Tour",
    plan_coming: "The floor plan will appear once an approved sales plan is provided.",
    view_coming: "The view from the apartment will appear after location is verified.",
    interior_generic_note: "Generic interior visualization for illustration only, developer plans pending",
    btn_rfp: "Build me an offer for this apartment",
    btn_brochure: "Apartment one-pager (PDF)",
    btn_winview: "Continue on the live area map",
    winview_note: "Drag to look around - sideways, down and up. Real floor height and direction; illustrative, not a photo from the unit.",
    winview_title: "This is the view from this apartment's window",
    winview_turn_left: "Look left",
    winview_turn_right: "Look right",
    winview_fs: "Full screen", winview_fs_exit: "Exit full screen",
    tab_view_dir: "Window view · {d}",
    sun_sim_label: "Sun simulation", sun_time_aria: "Choose time of day",
    sun_sim_note: "Real equinox sun path for the project's latitude. Geometric only, no shading from nearby buildings.",
    sun_direct_now: "Direct sun now",
    filter_active: "Filtered: {f}", filter_show_all: "Show all",
    view_interior_label: "Interior visualization",
    fp_salon: "Living and dining", fp_kitchen: "Kitchen", fp_mamad: "Safe room",
    fp_master: "Master bedroom", fp_bed: "Bedroom", fp_balcony: "Balcony",
    fp_aria: "Walk inside the apartment - drag to look around",
    fp_hint: "Drag to look · click a door to change rooms",
    fp_tag: "Schematic visualization built from this apartment's data",
    fp_to_room: "To {room}", fp_area_approx: "{label} · approx. {area} m²",
    tour_coming: "An interior tour will appear once an approved link is provided.",
    dt_exterior: "Building exterior", dt_street_entrance: "Street entrance", dt_entrance: "Entrance",
    dt_lobby: "Lobby", dt_stairwell: "Stairwell", dt_elevator: "Elevator", dt_entry_hall: "Entry hall",
    dt_living_room: "Living room", dt_kitchen: "Kitchen", dt_master_bedroom: "Master bedroom",
    dt_second_bedroom: "Second bedroom", dt_bathroom: "Bathroom", dt_balcony: "Balcony",
    dtour_tag: "A walk through a standard sample apartment - illustration. The developer's dedicated tour will replace it once received.",
    dtour_hint: "Drag to look \u00B7 arrows or doors to move between spaces",
    dtour_next: "Next space", dtour_prev: "Previous space",
    dtour_tag_dedicated: "Visualizations dedicated to this project - illustration only.",
    dtour_tag_premium: "A walk through a premium sample apartment - illustration. The developer's dedicated tour will replace it once received.",
    mortgage_est: "Est. monthly payment: {v}",
    mortgage_note: "Assuming 70% financing, 25 years, 5% rate - estimate only, not a financing offer.",
    dtour_tag_units: "Interior visualizations of this project's apartments - illustration only.",
    tour_title: "Interior tour", tour_open: "Open virtual tour", tour_open_pano: "Open 360 tour", tour_lazy_hint: "One click and you are inside.", tour_pending: "The developer's 360 tour will appear here once approved. Meanwhile, walk inside any apartment from the inventory board below.",
    btn_inquire: "I'm interested", btn_save: "Save", btn_saved: "Saved", btn_compare: "Compare",
    btn_compared: "Comparing", btn_share: "Share", btn_close: "Close", link_copied: "Link copied",
    inventory_title: "All apartments",
    inventory_sub: "Picking here marks the apartment on the building and the facade too.",
    filter_all: "All", filter_available: "Available", filter_3: "3 rm", filter_4: "4 rm", filter_5: "5 rm",
    filter_favs: "Saved",
    results_count: "{n} apartments",
    recent_title: "Recently viewed",
    scarcity_last: "The last available {rooms}-room apartment in this project",
    scarcity_left: "{n} available {rooms}-room apartments left in this project",
    scarcity_show: "Show them on the building",
    btn_wa_share: "WhatsApp",
    reset_view: "Back to full view",
    sun_hours: "~{h} direct-sun hours on an equinox day",
    sun_note: "Geometric estimate from orientation and latitude only, no surrounding shading",
    compare_top: "Stands out by area, floor and balcony",

    /* apartment studio */
    nlst_open: "Apartment Design Studio",
    nlst_title: "Apartment Design Studio",
    nlst_auto: "Auto-arrange", nlst_auto_note: "A starting point to edit - not a binding plan",
    nlst_it_tvunit: "TV unit", nlst_it_armchair: "Armchair", nlst_it_dresser: "Dresser",
    nlst_it_rug: "Rug", nlst_it_plant: "Plant", nlst_it_bench: "Dining bench",
    nlst_honest: "Schematic illustration based on this unit's data - not a sale plan",
    nlst_palette: "Furniture and templates (real dimensions)",
    nlst_cm: "cm",
    nlst_notes: "Notes and special requests",
    nlst_notes_ph: "e.g. EV-charger electrical point, wider bathroom door, lowered switches...",
    nlst_pros: "Architects and designers from our directory",
    nlst_rotate: "Rotate",
    nlst_undo: "Undo",
    nlst_note: "Item note",
    nlst_delete: "Delete",
    nlst_clear: "Clear all",
    nlst_send_rfp: "Attach design to my offer request",
    nlst_send_wa: "Share on WhatsApp",
    nlst_video: "Video call with a representative",
    nlst_video_msg: "I would like to schedule a video call about this design:",
    nlst_count: "{n} items in the design",
    nlst_scale: "Schematic envelope {m} m",
    nlst_note_ph: "Item note (up to 200 chars)",
    nlst_sum_head: "Apartment design {label} · floor {floor} · {project}",
    nlst_salon: "Living room + open kitchen", nlst_kitchen: "Kitchen", nlst_master: "Master bedroom", nlst_bed: "Bedroom", nlst_bath: "Bath + WC",
    nlst_it_sofa2: "2-seat sofa", nlst_it_sofa3: "3-seat sofa", nlst_it_bed_double: "Double bed", nlst_it_bed_single: "Single bed",
    nlst_it_table4: "Dining table 4", nlst_it_table6: "Dining table 6", nlst_it_wardrobe: "Wardrobe", nlst_it_fridge: "Fridge",
    nlst_it_washer: "Washing machine", nlst_it_desk: "Desk", nlst_it_crib: "Baby crib", nlst_it_bath: "Bathtub",
    nlst_it_wheel: "Wheelchair turning radius 150", nlst_it_door80: "Accessible door clearance 80",
    media_title: "Gallery, video and tour",
    media_empty: "Media will be added once provided by the developer.",
    media_gallery: "Gallery", media_video: "Video", media_tour: "Virtual tour",
    world_eyebrow: "The surroundings",
    world_title: "The complete world",
    world_sub: "Location, transport, education, leisure and retail, with the district figures.",
    map_title: "Area map", map_project_here: "Project here",
    spoke_transport: "Transport", spoke_education: "Education", spoke_facilities: "Leisure & retail", spoke_anchor: "Landmarks",
    spoke_reading_tower: "Reading Tower", spoke_beach: "Beach & promenade", spoke_light_rail: "Light rail, Green line",
    spoke_yarkon_park: "HaYarkon Park", spoke_school: "Schools", spoke_commercial: "Retail center", spoke_road: "Main routes",
    stat_plan: "Master plan", stat_units: "Planned homes", stat_dunams: "Dunams", stat_residents: "Planned residents",
    area_sde_dov: "Sde Dov district", area_sde_dov_blurb: "⟦Short area description⟧",
    nearby_projects: "Nearby projects",
    investor_title: "Foreign buyers",
    investor_sub: "Guidance for international buyers: process, documents, financing and tax.",
    investor_pt_process: "Clear buying process", investor_pt_legal: "Legal & tax support", investor_pt_finance: "Financing & currency",
    investor_cta: "Book a call",
    seo_eyebrow: "About the project",
    faq_title: "Frequently asked questions",
    form_title: "Interested? We'll get back to you",
    form_sub: "Leave your details and we'll return with information on the apartment you chose.",
    form_name: "Full name", form_phone: "Phone", form_email: "Email (optional)",
    form_submit: "Send enquiry", form_submitting: "Sending…",
    form_success: "Thank you. We received your enquiry and will be in touch soon.",
    form_error: "Please enter a name and a phone or email.",
    form_consent: "This enquiry is not an order or commitment. Illustrative data.",
    form_unit_ctx: "Enquiry for apartment {label} · Floor {floor} · {rooms} rooms",
    form_no_unit: "General project enquiry",
    whatsapp_cta: "WhatsApp", sticky_cta: "I'm interested",
    compare_title: "Compare apartments",
    compare_empty: "Add apartments to compare",
    compare_clear: "Clear",
    compare_inquire: "Enquire on selected",
    demo_badge: "Illustrative",
    disclaimer_title: "Illustrative notice",
    disclaimer_text: "The model, facade and apartments are an initial illustration, not a sales plan or approved inventory. Verify price and availability with the developer. Nothing here is an offer or commitment.",
    home_hero_eyebrow: "Real estate in Israel · New projects",
    home_hero_title: "Choose an apartment, a project and a neighborhood before you commit",
    home_hero_sub: "A real look at the project, the apartments and the surroundings, in one place.",
    home_search_area: "Area", home_search_type: "Type", home_search_cta: "Search",
    home_gallery_eyebrow: "Our projects",
    home_gallery_title: "New projects in Sde Dov",
    home_gallery_sub: "Pick a project and explore it apartment by apartment.",
    card_explore: "Enter project", card_units: "{n} apartments",
    home_areas_title: "By area",
    home_areas_sub: "Enter by district and area.",
    home_list_title: "Marketing a project?",
    home_list_sub: "Show your project in a 3D showroom that generates enquiries.",
    home_list_cta: "List with us",
    footer_tagline: "Project showroom and real estate in Israel",
    footer_rights: "© NadLan · All data illustrative pending developer approval",
    footer_col_projects: "Projects", footer_col_areas: "Areas", footer_col_company: "Company", footer_col_langs: "Languages"
  };

  /* FR / RU / AR - scaffold: every slot present, EN placeholder values. Owner's
     translators overwrite in place. Engine still falls back to EN if a key is
     ever missing. */
  var FR = Object.assign({}, EN);
  var RU = Object.assign({}, EN);
  var AR = Object.assign({}, EN);
  /* a few high-visibility endonym/ázimuth tweaks so the scaffold reads natively
     in the language switcher even before full translation */
  AR.brand = "نادلان"; AR.brand_sub = "معرض المشاريع";
  RU.brand_sub = "Витрина проектов";
  FR.brand_sub = "Vitrine des projets";
  FR.interior_generic_note = "Visualisation interieure generique, a titre indicatif, plans du promoteur en attente";
  RU.interior_generic_note = "Типовая визуализация интерьера, только для иллюстрации, планы застройщика ожидаются";
  AR.interior_generic_note = "تصور داخلي عام للتوضيح فقط، بانتظار مخططات المطور";
  FR.btn_rfp = "Preparez-moi une offre pour ce logement";
  RU.btn_rfp = "Подготовьте мне предложение по этой квартире";
  AR.btn_rfp = "جهزوا لي عرضا لهذه الشقة";
  FR.btn_winview = "Continuer sur la carte interactive du quartier";
  RU.btn_winview = "Продолжить на живой карте района";
  AR.btn_winview = "المتابعة على خريطة المنطقة الحية";
  FR.winview_note = "Glissez pour regarder autour - de cote, en bas, en haut. Hauteur d'etage et orientation reelles; illustration, pas une photo du logement.";
  RU.winview_note = "Тяните, чтобы осмотреться - в стороны, вниз и вверх. Реальная высота этажа и направление; иллюстрация, не фото из квартиры.";
  AR.winview_note = "اسحبوا للنظر حولكم - جانبا وأسفل وأعلى. ارتفاع الطابق والاتجاه حقيقيان؛ للتوضيح، ليست صورة من الشقة.";
  FR.winview_turn_left = "Regarder a gauche"; FR.winview_turn_right = "Regarder a droite";
  RU.winview_turn_left = "Посмотреть влево"; RU.winview_turn_right = "Посмотреть вправо";
  AR.winview_turn_left = "النظر يسارا"; AR.winview_turn_right = "النظر يمينا";
  /* the tab must state the ACTION, never a bare compass value (owner law
     2026-08-05: "דרום מערב" told users nothing about what the click reveals) */
  FR.tab_view = "Vue de la fenetre"; FR.tab_view_dir = "Vue de la fenetre · {d}";
  FR.winview_title = "Voici la vue depuis la fenetre de cet appartement";
  RU.tab_view = "Вид из окна"; RU.tab_view_dir = "Вид из окна · {d}";
  RU.winview_title = "Так выглядит вид из окна этой квартиры";
  AR.tab_view = "الإطلالة من النافذة"; AR.tab_view_dir = "الإطلالة من النافذة · {d}";
  AR.winview_title = "هذه هي الإطلالة من نافذة هذه الشقة";
  FR.view_interior_label = "Visualisation interieure";
  RU.view_interior_label = "Визуализация интерьера";
  AR.view_interior_label = "تصور داخلي للشقة";
  FR.fp_salon = "Sejour et salle a manger"; FR.fp_kitchen = "Cuisine"; FR.fp_mamad = "Piece securisee";
  FR.fp_master = "Chambre parentale"; FR.fp_bed = "Chambre"; FR.fp_balcony = "Balcon";
  FR.fp_aria = "Visite interieure du logement - faites glisser pour regarder autour";
  FR.fp_hint = "Glissez pour regarder · cliquez sur une porte pour changer de piece";
  FR.fp_tag = "Visualisation schematique creee a partir des donnees du logement";
  FR.fp_to_room = "Vers {room}"; FR.fp_area_approx = "{label} · env. {area} m²";
  RU.fp_salon = "Гостиная и столовая"; RU.fp_kitchen = "Кухня"; RU.fp_mamad = "Защищенная комната";
  RU.fp_master = "Главная спальня"; RU.fp_bed = "Спальня"; RU.fp_balcony = "Балкон";
  RU.fp_aria = "Прогулка внутри квартиры - потяните, чтобы осмотреться";
  RU.fp_hint = "Тяните, чтобы смотреть · нажмите на дверь для перехода";
  RU.fp_tag = "Схематичная визуализация, построенная по данным квартиры";
  RU.fp_to_room = "В {room}"; RU.fp_area_approx = "{label} · около {area} м²";
  AR.fp_salon = "غرفة المعيشة والسفرة"; AR.fp_kitchen = "المطبخ"; AR.fp_mamad = "الغرفة المحصنة";
  AR.fp_master = "غرفة النوم الرئيسية"; AR.fp_bed = "غرفة نوم"; AR.fp_balcony = "الشرفة";
  AR.fp_aria = "جولة داخل الشقة - اسحب للنظر حولك";
  AR.fp_hint = "اسحب للنظر · انقر على باب للانتقال بين الغرف";
  AR.fp_tag = "تصور تخطيطي مبني على بيانات الشقة";
  AR.fp_to_room = "إلى {room}"; AR.fp_area_approx = "{label} · نحو {area} م²";
  FR.tour_lazy_hint = "Un clic et vous etes a l'interieur.";
  RU.tour_lazy_hint = "Один клик - и вы внутри.";
  AR.tour_lazy_hint = "نقرة واحدة وأنتم في الداخل.";
  FR.tour_pending = "La visite 360 du promoteur apparaitra ici des validation. En attendant, entrez dans chaque logement depuis le tableau des appartements ci-dessous.";
  RU.tour_pending = "360-тур от застройщика появится здесь после утверждения. А пока зайдите внутрь любой квартиры через таблицу квартир ниже.";
  FR.dt_exterior = "Facade de l'immeuble"; FR.dt_street_entrance = "Entree depuis la rue"; FR.dt_entrance = "Entree";
  FR.dt_lobby = "Hall d'accueil"; FR.dt_stairwell = "Cage d'escalier"; FR.dt_elevator = "Ascenseur"; FR.dt_entry_hall = "Vestibule";
  FR.dt_living_room = "Sejour"; FR.dt_kitchen = "Cuisine"; FR.dt_master_bedroom = "Chambre parentale";
  FR.dt_second_bedroom = "Deuxieme chambre"; FR.dt_bathroom = "Salle de bain"; FR.dt_balcony = "Balcon";
  FR.dtour_tag = "Visite d'un logement type standard - illustration. La visite dediee du promoteur la remplacera des reception.";
  FR.dtour_hint = "Glissez pour regarder \u00B7 fleches ou portes pour changer d'espace";
  FR.dtour_next = "Espace suivant"; FR.dtour_prev = "Espace precedent";
  FR.dtour_tag_dedicated = "Visualisations dediees a ce projet - illustration uniquement.";
  FR.dtour_tag_premium = "Visite d'un logement type premium - illustration. La visite dediee du promoteur la remplacera des reception.";
  FR.mortgage_est = "Mensualite estimee : {v}";
  FR.mortgage_note = "Sur la base d'un financement de 70%, 25 ans, taux 5% - estimation uniquement, pas une offre de financement.";
  RU.dtour_tag_premium = "Прогулка по премиальной образцовой квартире - иллюстрация. Специальный тур застройщика заменит ее после получения.";
  RU.mortgage_est = "Примерный ежемесячный платеж: {v}";
  RU.mortgage_note = "При финансировании 70%, 25 лет, ставка 5% - только оценка, не предложение финансирования.";
  AR.dtour_tag_premium = "جولة في شقة نموذجية فاخرة - للتوضيح. ستحل جولة المطور المخصصة محلها فور استلامها.";
  AR.mortgage_est = "القسط الشهري التقديري: {v}";
  AR.mortgage_note = "على أساس تمويل 70%، 25 سنة، فائدة 5% - تقدير فقط، ليس عرض تمويل.";
  FR.dtour_tag_units = "Visualisations interieures des logements de ce projet - illustration uniquement.";
  RU.dt_exterior = "Фасад здания"; RU.dt_street_entrance = "Вход с улицы"; RU.dt_entrance = "Вход";
  RU.dt_lobby = "Лобби"; RU.dt_stairwell = "Лестничная клетка"; RU.dt_elevator = "Лифт"; RU.dt_entry_hall = "Прихожая";
  RU.dt_living_room = "Гостиная"; RU.dt_kitchen = "Кухня"; RU.dt_master_bedroom = "Главная спальня";
  RU.dt_second_bedroom = "Вторая спальня"; RU.dt_bathroom = "Ванная"; RU.dt_balcony = "Балкон";
  RU.dtour_tag = "Прогулка по стандартной образцовой квартире - иллюстрация. Специальный тур застройщика заменит ее после получения.";
  RU.dtour_hint = "Тяните, чтобы смотреть \u00B7 стрелки или двери для перехода";
  RU.dtour_next = "Следующее пространство"; RU.dtour_prev = "Предыдущее пространство";
  RU.dtour_tag_dedicated = "Визуализации, созданные для этого проекта - только иллюстрация.";
  RU.dtour_tag_units = "Визуализации интерьеров квартир этого проекта - только иллюстрация.";
  AR.dt_exterior = "واجهة المبنى"; AR.dt_street_entrance = "المدخل من الشارع"; AR.dt_entrance = "المدخل";
  AR.dt_lobby = "اللوبي"; AR.dt_stairwell = "بيت الدرج"; AR.dt_elevator = "المصعد"; AR.dt_entry_hall = "الردهة";
  AR.dt_living_room = "غرفة المعيشة"; AR.dt_kitchen = "المطبخ"; AR.dt_master_bedroom = "غرفة النوم الرئيسية";
  AR.dt_second_bedroom = "غرفة النوم الثانية"; AR.dt_bathroom = "الحمام"; AR.dt_balcony = "الشرفة";
  AR.dtour_tag = "جولة في شقة نموذجية قياسية - للتوضيح. ستحل جولة المطور المخصصة محلها فور استلامها.";
  AR.dtour_hint = "اسحبوا للنظر \u00B7 الأسهم أو الأبواب للتنقل بين المساحات";
  AR.dtour_next = "المساحة التالية"; AR.dtour_prev = "المساحة السابقة";
  AR.dtour_tag_dedicated = "تصورات مخصصة لهذا المشروع - للتوضيح فقط.";
  AR.dtour_tag_units = "تصورات داخلية لشقق هذا المشروع - للتوضيح فقط.";
  AR.tour_pending = "ستظهر جولة 360 من المطور هنا فور اعتمادها. حتى ذلك الحين، ادخلوا إلى أي شقة عبر لوحة الشقق أدناه.";

  /* Core labels used directly by the v2 scene and its tools. These cannot
     inherit EN: the private sandbox is the five-language acceptance surface. */
  Object.assign(FR, {
    status_available: "Illustratif", status_reserved: "En attente", status_sold: "Vendu", status_unknown: "Statut sur demande",
    panel_floor: "Étage", panel_rooms: "Pièces", panel_sqm: "Surface", panel_balcony: "Balcon",
    btn_save: "Enregistrer", btn_saved: "Enregistré", btn_compare: "Comparer",
    btn_compared: "Dans la comparaison", btn_share: "Partager",
    dir_west: "Ouest", dir_east: "Est", dir_north: "Nord", dir_south: "Sud",
    "dir_south-west": "Sud-ouest", "dir_north-west": "Nord-ouest",
    "dir_south-east": "Sud-est", "dir_north-east": "Nord-est",
    floor_label: "Étage {n}", rooms_label: "{n} pièces", sqm_unit: "m² de surface",
    tab_plan: "Plan du logement", tab_view: "Vue depuis la fenêtre", tab_tour: "Visite",
    plan_coming: "Le plan apparaîtra dès qu’un plan de vente approuvé sera fourni.",
    winview_turn_left: "Regarder à gauche", winview_turn_right: "Regarder à droite",
    tour_open: "Ouvrir la visite virtuelle",
    form_name: "Nom complet", form_phone: "Téléphone", form_email: "E-mail (facultatif)",
    form_consent: "Cette demande n’est ni une commande ni un engagement. Données illustratives.",
    form_submitting: "Envoi…", form_submit: "Envoyer la demande",
    theater_eyebrow: "Sélection dans le projet",
    theater_title: "Choisissez un logement dans l’immeuble",
    theater_hint: "Faites glisser pour tourner · touchez un logement",
    view_3d: "Vue 3D", view_facade: "Façade",
    generic_model: "Illustration générale, différente de l’immeuble du projet",
    loading_model: "Chargement de la vue…",
    model_error: "Le modèle 3D n’a pas été chargé. Les documents approuvés apparaîtront dès leur ajout au projet.",
    reset_view: "Revenir à la vue d’ensemble",
    legend_available: "Illustratif, sous réserve de confirmation du promoteur",
    legend_reserved: "En attente", legend_sold: "Vendu",
    panel_prompt: "Choisissez un logement dans l’immeuble ou sur la façade",
    inventory_title: "Tous les logements",
    inventory_sub: "Votre choix ici repère aussi le logement dans l’immeuble et sur la façade.",
    filter_all: "Tous", filter_available: "Disponibles", filter_3: "3 pièces",
    filter_4: "4 pièces", filter_5: "5 pièces", filter_favs: "Enregistrés",
    filter_active: "Filtre : {f}", filter_show_all: "Tout afficher",
    results_count: "{n} logements", recent_title: "Consultés récemment",
    concept_badge: "Concept, document non officiel",
    facade_concept_note: "Image conceptuelle uniquement. La sélection sur façade sera disponible après réception d’une façade officielle du promoteur.",
    facade_missing_title: "Façade officielle manquante",
    facade_missing_text: "Aucun fichier de façade approuvé n’est disponible ; la sélection sur façade n’est donc pas affichée.",
    sun_sim_label: "Simulation solaire", sun_time_aria: "Choisir l’heure de la journée",
    sun_sim_note: "Trajectoire solaire réelle à l’équinoxe selon la latitude du projet. Calcul géométrique sans ombrage des bâtiments voisins.",
    cotour_start: "Partager une visite en direct", nlst_open: "Studio de conception du logement"
  });

  Object.assign(RU, {
    status_available: "Для иллюстрации", status_reserved: "В резерве", status_sold: "Продано", status_unknown: "Статус по запросу",
    panel_floor: "Этаж", panel_rooms: "Комнаты", panel_sqm: "Площадь", panel_balcony: "Балкон",
    btn_save: "Сохранить", btn_saved: "Сохранено", btn_compare: "Сравнить",
    btn_compared: "Добавлено к сравнению", btn_share: "Поделиться",
    dir_west: "Запад", dir_east: "Восток", dir_north: "Север", dir_south: "Юг",
    "dir_south-west": "Юго-запад", "dir_north-west": "Северо-запад",
    "dir_south-east": "Юго-восток", "dir_north-east": "Северо-восток",
    floor_label: "Этаж {n}", rooms_label: "Комнат: {n}", sqm_unit: "м²",
    tab_plan: "План", tab_view: "Вид из окна", tab_tour: "Тур",
    plan_coming: "План появится после получения утверждённого плана продажи.",
    winview_turn_left: "Посмотреть влево", winview_turn_right: "Посмотреть вправо",
    tour_open: "Открыть виртуальный тур",
    form_name: "Полное имя", form_phone: "Телефон", form_email: "Эл. почта (необязательно)",
    form_consent: "Это обращение не является заказом или обязательством. Данные приведены для иллюстрации.",
    form_submitting: "Отправка…", form_submit: "Отправить обращение",
    theater_eyebrow: "Выбор в проекте",
    theater_title: "Выберите квартиру в здании",
    theater_hint: "Поворачивайте перетаскиванием · нажмите на квартиру",
    view_3d: "Трёхмерный вид", view_facade: "Фасад",
    generic_model: "Общая иллюстрация, не здание этого проекта",
    loading_model: "Загрузка вида…",
    model_error: "Трёхмерная модель не загрузилась. Утверждённые материалы появятся после добавления в проект.",
    reset_view: "Вернуться к общему виду",
    legend_available: "Иллюстрация, требуется подтверждение застройщика",
    legend_reserved: "В резерве", legend_sold: "Продано",
    panel_prompt: "Выберите квартиру в здании или на фасаде",
    inventory_title: "Все квартиры",
    inventory_sub: "Выбор здесь также отмечает квартиру в здании и на фасаде.",
    filter_all: "Все", filter_available: "Доступные", filter_3: "3 комнаты",
    filter_4: "4 комнаты", filter_5: "5 комнат", filter_favs: "Сохранённые",
    filter_active: "Фильтр: {f}", filter_show_all: "Показать все",
    results_count: "Квартир: {n}", recent_title: "Недавно просмотренные",
    concept_badge: "Концепция, неофициальный материал",
    facade_concept_note: "Только концептуальное изображение. Выбор на фасаде станет доступен после загрузки официального фасада застройщика.",
    facade_missing_title: "Нет официального фасада",
    facade_missing_text: "Для проекта не загружен утверждённый фасад, поэтому выбор квартир на фасаде не отображается.",
    sun_sim_label: "Моделирование солнца", sun_time_aria: "Выбрать время дня",
    sun_sim_note: "Реальная траектория солнца в день равноденствия для широты проекта. Только геометрический расчёт, без теней соседних зданий.",
    cotour_start: "Поделиться живым туром", nlst_open: "Студия дизайна квартиры"
  });

  Object.assign(AR, {
    status_available: "للتوضيح", status_reserved: "قيد الحجز", status_sold: "تم البيع", status_unknown: "الحالة عند الطلب",
    panel_floor: "الطابق", panel_rooms: "الغرف", panel_sqm: "المساحة", panel_balcony: "الشرفة",
    btn_save: "حفظ", btn_saved: "محفوظة", btn_compare: "مقارنة",
    btn_compared: "ضمن المقارنة", btn_share: "مشاركة",
    dir_west: "الغرب", dir_east: "الشرق", dir_north: "الشمال", dir_south: "الجنوب",
    "dir_south-west": "الجنوب الغربي", "dir_north-west": "الشمال الغربي",
    "dir_south-east": "الجنوب الشرقي", "dir_north-east": "الشمال الشرقي",
    floor_label: "الطابق {n}", rooms_label: "{n} غرف", sqm_unit: "م²",
    tab_plan: "المخطط", tab_view: "الإطلالة من النافذة", tab_tour: "الجولة",
    plan_coming: "سيظهر المخطط بعد استلام مخطط بيع معتمد.",
    winview_turn_left: "النظر إلى اليسار", winview_turn_right: "النظر إلى اليمين",
    tour_open: "فتح الجولة الافتراضية",
    form_name: "الاسم الكامل", form_phone: "الهاتف", form_email: "البريد الإلكتروني (اختياري)",
    form_consent: "هذا الطلب ليس أمر شراء أو التزامًا. البيانات للتوضيح.",
    form_submitting: "جارٍ الإرسال…", form_submit: "إرسال الطلب",
    theater_eyebrow: "اختيار الشقة في المشروع",
    theater_title: "اختاروا شقة من المبنى",
    theater_hint: "اسحبوا لتدوير المبنى · اضغطوا على شقة",
    view_3d: "عرض ثلاثي الأبعاد", view_facade: "الواجهة",
    generic_model: "تصور عام وليس مبنى هذا المشروع",
    loading_model: "جارٍ تحميل العرض…",
    model_error: "تعذر تحميل النموذج الثلاثي الأبعاد. ستظهر المواد المعتمدة بعد إضافتها إلى المشروع.",
    reset_view: "العودة إلى العرض الكامل",
    legend_available: "للتوضيح ويخضع لتأكيد المطور",
    legend_reserved: "قيد الحجز", legend_sold: "تم البيع",
    panel_prompt: "اختاروا شقة من المبنى أو من الواجهة",
    inventory_title: "جميع الشقق",
    inventory_sub: "الاختيار هنا يحدد الشقة أيضًا في المبنى وعلى الواجهة.",
    filter_all: "الكل", filter_available: "المتاحة", filter_3: "3 غرف",
    filter_4: "4 غرف", filter_5: "5 غرف", filter_favs: "المحفوظة",
    filter_active: "التصفية: {f}", filter_show_all: "عرض الكل",
    results_count: "{n} شقق", recent_title: "شوهدت مؤخرًا",
    concept_badge: "تصور مبدئي وليس مادة رسمية",
    facade_concept_note: "صورة مبدئية فقط. سيتاح الاختيار على الواجهة بعد رفع واجهة رسمية من المطور.",
    facade_missing_title: "الواجهة الرسمية غير متاحة",
    facade_missing_text: "لم يُرفع ملف واجهة معتمد لهذا المشروع، لذلك لا يظهر اختيار الشقق على الواجهة.",
    sun_sim_label: "محاكاة الشمس", sun_time_aria: "اختيار وقت اليوم",
    sun_sim_note: "مسار شمسي حقيقي ليوم الاعتدال بحسب خط عرض المشروع. حساب هندسي فقط من دون ظلال المباني المجاورة.",
    cotour_start: "مشاركة جولة مباشرة", nlst_open: "استوديو تصميم الشقة"
  });

  /* ---- selected-unit surface additions (audit 2026-08-08) ---- */
Object.assign(HE, {
  unit_back_building: "חזרה לבניין",
  unit_selected: "הדירה שבחרתם",
  unit_beam_title: "החלון פונה אל {view}",
  unit_beam_note: "כך הדירה מונחת ביחס לסביבה",
  unit_beam_view_short: "נוף מהחלון",
  inv_band: "קומות {from}–{to}",
  inv_bands_aria: "בחירת טווח קומות",
  unit_window_panorama_note: "כיוון החלון המדויק בבדיקה מול היזם — מוצג מבט פנורמי 360° מגובה הקומה",
  unit_beam_ahead: "בכיוון הזה:",
  unit_beam_nearest: "הכי קרוב:",
  dist_m: "מ׳",
  dist_km: "ק״מ",
  unit_tools_aria: "דרכים להכיר את הדירה",
  unit_quick_actions: "שמירה, השוואה ושיתוף",
  unit_door_plan: "איך הדירה מחולקת? פתחו את התוכנית",
  unit_door_view: "החלון פונה אל {view}. לחצו להסתכל החוצה",
  unit_door_tour: "רוצים להרגיש את החלל? היכנסו לסיור",
  unit_door_studio: "איך הדירה תיראה שלכם? פתחו את המעצב",
  unit_tool_back: "חזרה לדירה",
  unit_offer: "רוצים אותה? בנו הצעה לדירה הזו",
  unit_map_unverified: "הכיוון אמיתי; מפת הסביבה תופיע לאחר אימות מיקום הפרויקט"
});

Object.assign(EN, {
  unit_back_building: "Back to the building",
  unit_selected: "The home you selected",
  unit_beam_title: "This window faces {view}",
  unit_beam_note: "See how the home sits within its surroundings",
  unit_beam_view_short: "Window view",
  inv_band: "Floors {from}–{to}",
  inv_bands_aria: "Choose a floor range",
  unit_window_panorama_note: "Exact window bearing pending developer confirmation — showing a 360° panorama from this floor's height",
  unit_beam_ahead: "That way:",
  unit_beam_nearest: "Closest:",
  dist_m: "m",
  dist_km: "km",
  unit_tools_aria: "Ways to explore this home",
  unit_quick_actions: "Save, compare and share",
  unit_door_plan: "How is the home arranged? Open the floor plan",
  unit_door_view: "The window faces {view}. Look outside",
  unit_door_tour: "Want to feel the space? Step inside the tour",
  unit_door_studio: "How could it look as yours? Open the designer",
  unit_tool_back: "Back to the home",
  unit_offer: "Feels right? Build an offer for this home",
  unit_map_unverified: "The direction is verified; the area map will appear once the project location is verified"
});

Object.assign(FR, {
  unit_back_building: "Retour à l’immeuble",
  unit_selected: "Le logement que vous avez choisi",
  unit_beam_title: "Cette fenêtre donne sur {view}",
  unit_beam_note: "Voyez comment le logement s’oriente dans son environnement",
  unit_beam_ahead: "Dans cette direction :",
  unit_beam_nearest: "Le plus proche :",
  dist_m: "m",
  dist_km: "km",
  unit_tools_aria: "Façons de découvrir le logement",
  unit_quick_actions: "Enregistrer, comparer et partager",
  unit_door_plan: "Comment le logement est-il organisé ? Ouvrez le plan",
  unit_door_view: "La fenêtre donne sur {view}. Regardez dehors",
  unit_door_tour: "Envie de ressentir l’espace ? Entrez dans la visite",
  unit_door_studio: "À quoi ressemblerait-il chez vous ? Ouvrez le décorateur",
  unit_tool_back: "Retour au logement",
  unit_offer: "Il vous plaît ? Construisez une offre pour ce logement",
  unit_map_unverified: "L’orientation est vérifiée ; la carte apparaîtra après validation de l’emplacement"
});

Object.assign(RU, {
  unit_back_building: "Назад к зданию",
  unit_selected: "Выбранная квартира",
  unit_beam_title: "Окно выходит на {view}",
  unit_beam_note: "Посмотрите, как квартира ориентирована относительно окружения",
  unit_beam_ahead: "В этом направлении:",
  unit_beam_nearest: "Ближе всего:",
  dist_m: "м",
  dist_km: "км",
  unit_tools_aria: "Способы познакомиться с квартирой",
  unit_quick_actions: "Сохранить, сравнить и поделиться",
  unit_door_plan: "Как устроена квартира? Откройте план",
  unit_door_view: "Окно выходит на {view}. Посмотрите наружу",
  unit_door_tour: "Хотите почувствовать пространство? Войдите в тур",
  unit_door_studio: "Как она будет выглядеть вашей? Откройте дизайнер",
  unit_tool_back: "Назад к квартире",
  unit_offer: "Подходит? Составьте предложение по этой квартире",
  unit_map_unverified: "Направление проверено; карта появится после проверки местоположения проекта"
});

Object.assign(AR, {
  unit_back_building: "العودة إلى المبنى",
  unit_selected: "الشقة التي اخترتموها",
  unit_beam_title: "تتجه النافذة نحو {view}",
  unit_beam_note: "هكذا تقع الشقة بالنسبة إلى محيطها",
  unit_beam_ahead: "في هذا الاتجاه:",
  unit_beam_nearest: "الأقرب:",
  dist_m: "م",
  dist_km: "كم",
  unit_tools_aria: "طرق للتعرّف إلى الشقة",
  unit_quick_actions: "الحفظ والمقارنة والمشاركة",
  unit_door_plan: "كيف تتوزع المساحات؟ افتحوا المخطط",
  unit_door_view: "تتجه النافذة نحو {view}. اضغطوا للنظر إلى الخارج",
  unit_door_tour: "تريدون الإحساس بالمساحة؟ ادخلوا الجولة",
  unit_door_studio: "كيف ستبدو الشقة بطابعكم؟ افتحوا المصمم",
  unit_tool_back: "العودة إلى الشقة",
  unit_offer: "أعجبتكم؟ ابنوا عرضًا لهذه الشقة",
  unit_map_unverified: "الاتجاه حقيقي؛ ستظهر خريطة المحيط بعد التحقق من موقع المشروع"
});

/* ---- private selected-unit journey v2: complete acceptance copy ---- */
Object.assign(HE, {
  unit_quick_actions_v2: "שמירה, שיתוף והשוואת דירות",
  unit_compare_open: "השוו דירות",
  unit_compare_title: "איך הדירה הזאת עומדת מול אחרות?",
  unit_compare_intro: "בחרו דירה שנייה, ואם תרצו גם שלישית, וראו רק את הנתונים שנמסרו לפרויקט.",
  unit_compare_slots_aria: "בחירת דירות להשוואה",
  unit_compare_slot_current: "הדירה שבחרתם",
  unit_compare_slot_second: "מול איזו דירה?",
  unit_compare_slot_third: "רוצים להוסיף עוד אחת?",
  unit_compare_optional_empty: "בלי דירה שלישית",
  unit_compare_option: "{label}, {rooms} חדרים, קומה {floor}",
  unit_compare_summary_aria: "השוואת נתוני הדירות שנבחרו",
  unit_compare_status: "מצב",
  unit_compare_field: "מה בודקים",
  unit_compare_difference: "שונה",
  unit_compare_not_provided: "לא נמסר",
  unit_compare_unavailable: "אין כרגע דירה נוספת בפרויקט להשוואה.",
  unit_lab_page_title: "{project} · מעבדת בחירת דירה פרטית",
  unit_window_direction_unavailable: "כיוון החלון עדיין בבדיקה, ולכן לא מוצג נוף כיווני מטעה.",
  unit_beam_open_short: "פתחו מפה",
  unit_direction_unknown: "כיוון בבדיקה",
  unit_v2_marker: "דירה בקומה {floor}",
  unit_compare_remove: "הסרת הדירה מההשוואה",
  unit_v2_identity: "{rooms} חדרים · קומה {floor} · כיוון {direction}",
  unit_v2_instruction: "הבניין, הכיוון וכל הדרכים להכיר את הדירה נשארים יחד במסך אחד.",
  unit_beam_region: "כיוון הדירה ומפת הסביבה",
  unit_beam_open: "פתחו את מפת הסביבה וגלו מה נמצא לאורך הכיוון",
  unit_area_open_aria: "פתיחת מפת הסביבה המלאה",
  unit_contact_cta: "רוצים לבדוק אם היא מתאימה לכם? דברו איתנו עליה",
  unit_area_title: "מה מחכה סביב הדירה",
  unit_contact_title: "שיחה על הדירה שבחרתם",
  unit_studio_title: "הדירה, בסגנון שלכם",
  unit_plan_canvas_aria: "תוכנית הדירה הניתנת להזזה ולהגדלה",
  unit_plan_alt: "תוכנית דירת {rooms} חדרים בקומה {floor}",
  unit_plan_controls: "בקרי הגדלה של התוכנית",
  unit_plan_zoom_out: "הקטנת התוכנית",
  unit_plan_zoom_in: "הגדלת התוכנית",
  unit_plan_reset: "איפוס",
  unit_plan_hint: "גררו כדי להתמקד באזור מסוים. צבטו או השתמשו בכפתורי ההגדלה.",
  unit_window_canvas_aria: "מבט אינטראקטיבי מכיוון חלון הדירה",
  unit_window_hint: "גררו כדי להביט לצדדים ולגובה. הכיוון והקומה נגזרים מנתוני הדירה; התצוגה היא להמחשה.",
  unit_studio_iframe_title: "מעצב הדירה האינטראקטיבי",
  unit_studio_external: "פתיחת המעצב בחלון מלא",
  unit_studio_unavailable: "המעצב אינו זמין כרגע לדירה זו.",
  unit_area_map_aria: "מפה אינטראקטיבית של סביבת הפרויקט",
  unit_area_note: "סובבו, הגדילו והתרחקו כדי להבין את הרחובות, החוף והמרחקים סביב הפרויקט.",
  unit_area_external: "פתיחת המיקום במפות Google",
  unit_area_unavailable: "מפת הסביבה תופיע לאחר אימות מיקום הפרויקט.",
  unit_contact_intro: "השאירו דרך נוחה לחזור אליכם לגבי דירת {rooms} חדרים, קומה {floor}, בשטח {sqm} מ״ר.",
  unit_contact_message: "מה תרצו לדעת?",
  unit_contact_submit: "חזרו אליי לגבי הדירה הזאת",
  unit_contact_name_error: "נא להזין שם בן שני תווים לפחות.",
  unit_contact_channel_error: "נא להזין טלפון או כתובת דוא״ל.",
  unit_contact_email_error: "נא להזין כתובת דוא״ל תקינה.",
  unit_contact_consent_error: "יש לאשר את תנאי הפנייה לפני השליחה.",
  unit_contact_validation_error: "חסרים כמה פרטים לפני שנוכל לשלוח את הפנייה.",
  unit_contact_unavailable: "ערוץ הפניות אינו זמין כרגע. אפשר לנסות שוב מאוחר יותר.",
  unit_contact_payload: "בקשת מידע על דירת {rooms} חדרים, קומה {floor}, {sqm} מ״ר.",
  unit_contact_success: "הפנייה התקבלה. נחזור אליכם לגבי הדירה שבחרתם.",
  unit_contact_failure: "הפנייה לא נשלחה. הפרטים נשמרו בטופס כדי שתוכלו לנסות שוב."
});

Object.assign(EN, {
  unit_quick_actions_v2: "Save, share and compare homes",
  unit_compare_open: "Compare homes",
  unit_compare_title: "How does this home compare?",
  unit_compare_intro: "Choose a second home, and an optional third, to compare only the project facts provided.",
  unit_compare_slots_aria: "Choose homes to compare",
  unit_compare_slot_current: "Your selected home",
  unit_compare_slot_second: "Which home should sit beside it?",
  unit_compare_slot_third: "Would you like to add one more?",
  unit_compare_optional_empty: "No third home",
  unit_compare_option: "{label}, {rooms} rooms, floor {floor}",
  unit_compare_summary_aria: "Comparison of the selected homes",
  unit_compare_status: "Status",
  unit_compare_field: "Fact",
  unit_compare_difference: "Different",
  unit_compare_not_provided: "Not provided",
  unit_compare_unavailable: "There is no second home in this project to compare right now.",
  unit_lab_page_title: "{project} · Private apartment journey lab",
  unit_window_direction_unavailable: "The window direction is still being verified, so no misleading directional view is shown.",
  unit_beam_open_short: "Open map",
  unit_direction_unknown: "Direction being verified",
  unit_v2_marker: "Home on floor {floor}",
  unit_compare_remove: "Remove this home from the comparison",
  unit_v2_identity: "{rooms} rooms · Floor {floor} · Facing {direction}",
  unit_v2_instruction: "The building, orientation and every way to explore this home stay together on one screen.",
  unit_beam_region: "Home orientation and area map",
  unit_beam_open: "Open the area map and discover what lies in this direction",
  unit_area_open_aria: "Open the full area map",
  unit_contact_cta: "Could this be your home? Talk to us about it",
  unit_area_title: "What surrounds this home",
  unit_contact_title: "Talk about the home you selected",
  unit_studio_title: "Make the home feel like yours",
  unit_plan_canvas_aria: "Pan and zoom the floor plan",
  unit_plan_alt: "Floor plan for a {rooms}-room home on floor {floor}",
  unit_plan_controls: "Floor-plan zoom controls",
  unit_plan_zoom_out: "Zoom out of the floor plan",
  unit_plan_zoom_in: "Zoom into the floor plan",
  unit_plan_reset: "Reset",
  unit_plan_hint: "Drag to inspect an area. Pinch or use the zoom controls.",
  unit_window_canvas_aria: "Interactive view in the direction of the home’s window",
  unit_window_hint: "Drag to look sideways and vertically. Floor and direction come from the home data; the scene is illustrative.",
  unit_studio_iframe_title: "Interactive home designer",
  unit_studio_external: "Open the designer in a full window",
  unit_studio_unavailable: "The designer is not available for this home yet.",
  unit_area_map_aria: "Interactive map of the project area",
  unit_area_note: "Rotate and zoom to understand the streets, coast and distances around the project.",
  unit_area_external: "Open this location in Google Maps",
  unit_area_unavailable: "The area map will appear once the project location is verified.",
  unit_contact_intro: "Leave the best way to reach you about this {rooms}-room, {sqm} sqm home on floor {floor}.",
  unit_contact_message: "What would you like to know?",
  unit_contact_submit: "Contact me about this home",
  unit_contact_name_error: "Enter a name with at least two characters.",
  unit_contact_channel_error: "Enter a phone number or email address.",
  unit_contact_email_error: "Enter a valid email address.",
  unit_contact_consent_error: "Accept the enquiry terms before sending.",
  unit_contact_validation_error: "A few details are still needed before the enquiry can be sent.",
  unit_contact_unavailable: "Enquiries are temporarily unavailable. Please try again later.",
  unit_contact_payload: "Information request for a {rooms}-room, {sqm} sqm home on floor {floor}.",
  unit_contact_success: "Your enquiry was received. We will contact you about the home you selected.",
  unit_contact_failure: "The enquiry was not sent. Your details remain in the form so you can try again."
});

Object.assign(FR, {
  unit_quick_actions_v2: "Enregistrer, partager et comparer",
  unit_compare_open: "Comparer les logements",
  unit_compare_title: "Comment ce logement se compare-t-il ?",
  unit_compare_intro: "Choisissez un deuxième logement, puis éventuellement un troisième, pour comparer uniquement les données fournies par le projet.",
  unit_compare_slots_aria: "Choisir les logements à comparer",
  unit_compare_slot_current: "Votre logement sélectionné",
  unit_compare_slot_second: "Quel logement placer à côté ?",
  unit_compare_slot_third: "Souhaitez-vous en ajouter un autre ?",
  unit_compare_optional_empty: "Sans troisième logement",
  unit_compare_option: "{label}, {rooms} pièces, étage {floor}",
  unit_compare_summary_aria: "Comparaison des logements sélectionnés",
  unit_compare_status: "Statut",
  unit_compare_field: "Donnée",
  unit_compare_difference: "Différent",
  unit_compare_not_provided: "Non renseigné",
  unit_compare_unavailable: "Aucun deuxième logement du projet n’est disponible pour une comparaison immédiate.",
  unit_lab_page_title: "{project} · Laboratoire privé de sélection d’un logement",
  unit_window_direction_unavailable: "L’orientation de la fenêtre est en cours de vérification ; aucune vue directionnelle trompeuse n’est affichée.",
  unit_beam_open_short: "Ouvrir la carte",
  unit_direction_unknown: "Orientation en cours de vérification",
  unit_v2_marker: "Logement à l’étage {floor}",
  unit_compare_remove: "Retirer ce logement de la comparaison",
  unit_v2_identity: "{rooms} pièces · Étage {floor} · Orientation {direction}",
  unit_v2_instruction: "L’immeuble, l’orientation et toutes les façons de découvrir ce logement restent réunis sur un seul écran.",
  unit_beam_region: "Orientation du logement et carte du quartier",
  unit_beam_open: "Ouvrez la carte et découvrez ce qui se trouve dans cette direction",
  unit_area_open_aria: "Ouvrir la carte complète du quartier",
  unit_contact_cta: "Ce logement pourrait vous convenir ? Parlons-en",
  unit_area_title: "Ce qui entoure le logement",
  unit_contact_title: "Échanger sur le logement choisi",
  unit_studio_title: "Imaginez le logement à votre image",
  unit_plan_canvas_aria: "Plan déplaçable et zoomable",
  unit_plan_alt: "Plan d’un logement de {rooms} pièces à l’étage {floor}",
  unit_plan_controls: "Commandes de zoom du plan",
  unit_plan_zoom_out: "Réduire le plan",
  unit_plan_zoom_in: "Agrandir le plan",
  unit_plan_reset: "Réinitialiser",
  unit_plan_hint: "Faites glisser pour examiner une zone. Pincez ou utilisez les commandes de zoom.",
  unit_window_canvas_aria: "Vue interactive dans la direction de la fenêtre",
  unit_window_hint: "Faites glisser pour regarder sur les côtés et en hauteur. L’étage et l’orientation viennent des données du logement ; la scène est illustrative.",
  unit_studio_iframe_title: "Décorateur interactif du logement",
  unit_studio_external: "Ouvrir le décorateur en plein écran",
  unit_studio_unavailable: "Le décorateur n’est pas encore disponible pour ce logement.",
  unit_area_map_aria: "Carte interactive des environs du projet",
  unit_area_note: "Tournez et zoomez pour comprendre les rues, le littoral et les distances autour du projet.",
  unit_area_external: "Ouvrir cet emplacement dans Google Maps",
  unit_area_unavailable: "La carte apparaîtra après vérification de l’emplacement du projet.",
  unit_contact_intro: "Indiquez le meilleur moyen de vous joindre au sujet de ce logement de {rooms} pièces, {sqm} m², à l’étage {floor}.",
  unit_contact_message: "Que souhaitez-vous savoir ?",
  unit_contact_submit: "Contactez-moi pour ce logement",
  unit_contact_name_error: "Saisissez un nom d’au moins deux caractères.",
  unit_contact_channel_error: "Saisissez un numéro de téléphone ou une adresse e-mail.",
  unit_contact_email_error: "Saisissez une adresse e-mail valide.",
  unit_contact_consent_error: "Acceptez les conditions de contact avant l’envoi.",
  unit_contact_validation_error: "Quelques informations sont encore nécessaires avant l’envoi.",
  unit_contact_unavailable: "Le service de contact est temporairement indisponible. Réessayez plus tard.",
  unit_contact_payload: "Demande d’information pour un logement de {rooms} pièces, {sqm} m², à l’étage {floor}.",
  unit_contact_success: "Votre demande a bien été reçue. Nous vous contacterons au sujet du logement choisi.",
  unit_contact_failure: "La demande n’a pas été envoyée. Vos informations restent dans le formulaire pour réessayer."
});

Object.assign(RU, {
  unit_quick_actions_v2: "Сохранить, поделиться и сравнить",
  unit_compare_open: "Сравнить квартиры",
  unit_compare_title: "Как эта квартира выглядит в сравнении?",
  unit_compare_intro: "Выберите вторую квартиру и, при желании, третью. Сравнение покажет только данные, предоставленные проектом.",
  unit_compare_slots_aria: "Выбор квартир для сравнения",
  unit_compare_slot_current: "Выбранная вами квартира",
  unit_compare_slot_second: "С какой квартирой сравнить?",
  unit_compare_slot_third: "Добавить ещё одну квартиру?",
  unit_compare_optional_empty: "Без третьей квартиры",
  unit_compare_option: "{label}, {rooms} комн., этаж {floor}",
  unit_compare_summary_aria: "Сравнение выбранных квартир",
  unit_compare_status: "Статус",
  unit_compare_field: "Параметр",
  unit_compare_difference: "Отличается",
  unit_compare_not_provided: "Не указано",
  unit_compare_unavailable: "Сейчас в проекте нет второй квартиры для сравнения.",
  unit_lab_page_title: "{project} · Закрытая лаборатория выбора квартиры",
  unit_window_direction_unavailable: "Направление окна уточняется, поэтому вводящий в заблуждение вид не показывается.",
  unit_beam_open_short: "Открыть карту",
  unit_direction_unknown: "Направление уточняется",
  unit_v2_marker: "Квартира на этаже {floor}",
  unit_compare_remove: "Убрать эту квартиру из сравнения",
  unit_v2_identity: "{rooms} комнаты · Этаж {floor} · Направление {direction}",
  unit_v2_instruction: "Здание, ориентация и все способы изучить квартиру остаются вместе на одном экране.",
  unit_beam_region: "Ориентация квартиры и карта района",
  unit_beam_open: "Откройте карту района и узнайте, что находится в этом направлении",
  unit_area_open_aria: "Открыть полную карту района",
  unit_contact_cta: "Подходит ли вам эта квартира? Обсудите её с нами",
  unit_area_title: "Что окружает квартиру",
  unit_contact_title: "Обсудить выбранную квартиру",
  unit_studio_title: "Представьте квартиру в своём стиле",
  unit_plan_canvas_aria: "План квартиры с перемещением и масштабированием",
  unit_plan_alt: "План {rooms}-комнатной квартиры на этаже {floor}",
  unit_plan_controls: "Управление масштабом плана",
  unit_plan_zoom_out: "Уменьшить план",
  unit_plan_zoom_in: "Увеличить план",
  unit_plan_reset: "Сбросить",
  unit_plan_hint: "Перетаскивайте план для просмотра деталей. Используйте жест щипка или кнопки масштаба.",
  unit_window_canvas_aria: "Интерактивный вид по направлению окна квартиры",
  unit_window_hint: "Перетаскивайте, чтобы смотреть по сторонам и вверх. Этаж и направление взяты из данных квартиры; сцена является иллюстрацией.",
  unit_studio_iframe_title: "Интерактивный дизайнер квартиры",
  unit_studio_external: "Открыть дизайнер в полном окне",
  unit_studio_unavailable: "Дизайнер пока недоступен для этой квартиры.",
  unit_area_map_aria: "Интерактивная карта района проекта",
  unit_area_note: "Поворачивайте и масштабируйте карту, чтобы понять расположение улиц, побережья и расстояния.",
  unit_area_external: "Открыть это место в Google Maps",
  unit_area_unavailable: "Карта района появится после проверки местоположения проекта.",
  unit_contact_intro: "Оставьте удобный способ связи по поводу {rooms}-комнатной квартиры площадью {sqm} м² на этаже {floor}.",
  unit_contact_message: "Что вы хотите узнать?",
  unit_contact_submit: "Свяжитесь со мной по этой квартире",
  unit_contact_name_error: "Введите имя не короче двух символов.",
  unit_contact_channel_error: "Введите номер телефона или адрес электронной почты.",
  unit_contact_email_error: "Введите корректный адрес электронной почты.",
  unit_contact_consent_error: "Подтвердите условия обращения перед отправкой.",
  unit_contact_validation_error: "Для отправки обращения нужно заполнить ещё несколько полей.",
  unit_contact_unavailable: "Сервис обращений временно недоступен. Повторите попытку позже.",
  unit_contact_payload: "Запрос информации о {rooms}-комнатной квартире площадью {sqm} м² на этаже {floor}.",
  unit_contact_success: "Ваше обращение получено. Мы свяжемся с вами по поводу выбранной квартиры.",
  unit_contact_failure: "Обращение не отправлено. Данные остались в форме, чтобы вы могли повторить попытку."
});

Object.assign(AR, {
  unit_quick_actions_v2: "حفظ الشقق ومشاركتها ومقارنتها",
  unit_compare_open: "قارنوا الشقق",
  unit_compare_title: "كيف تبدو هذه الشقة عند المقارنة؟",
  unit_compare_intro: "اختاروا شقة ثانية، ويمكن إضافة ثالثة، لمقارنة البيانات التي قدمها المشروع فقط.",
  unit_compare_slots_aria: "اختيار الشقق للمقارنة",
  unit_compare_slot_current: "الشقة التي اخترتموها",
  unit_compare_slot_second: "بأي شقة تريدون مقارنتها؟",
  unit_compare_slot_third: "هل تريدون إضافة شقة أخرى؟",
  unit_compare_optional_empty: "من دون شقة ثالثة",
  unit_compare_option: "{label}، {rooms} غرف، الطابق {floor}",
  unit_compare_summary_aria: "مقارنة بيانات الشقق المختارة",
  unit_compare_status: "الحالة",
  unit_compare_field: "البيان",
  unit_compare_difference: "مختلف",
  unit_compare_not_provided: "غير مذكور",
  unit_compare_unavailable: "لا توجد حاليًا شقة ثانية في المشروع للمقارنة.",
  unit_lab_page_title: "{project} · مختبر خاص لاختيار الشقة",
  unit_window_direction_unavailable: "اتجاه النافذة قيد التحقق، لذلك لا نعرض مشهدًا اتجاهيًا قد يكون مضللًا.",
  unit_beam_open_short: "افتحوا الخريطة",
  unit_direction_unknown: "الاتجاه قيد التحقق",
  unit_v2_marker: "شقة في الطابق {floor}",
  unit_compare_remove: "إزالة هذه الشقة من المقارنة",
  unit_v2_identity: "{rooms} غرف · الطابق {floor} · الاتجاه {direction}",
  unit_v2_instruction: "يبقى المبنى والاتجاه وكل طرق استكشاف الشقة معًا في شاشة واحدة.",
  unit_beam_region: "اتجاه الشقة وخريطة المنطقة",
  unit_beam_open: "افتحوا خريطة المنطقة واكتشفوا ما يوجد في هذا الاتجاه",
  unit_area_open_aria: "فتح خريطة المنطقة الكاملة",
  unit_contact_cta: "هل يمكن أن تناسبكم هذه الشقة؟ تحدثوا معنا عنها",
  unit_area_title: "ما الذي يحيط بالشقة",
  unit_contact_title: "التحدث عن الشقة التي اخترتموها",
  unit_studio_title: "تخيلوا الشقة بأسلوبكم",
  unit_plan_canvas_aria: "مخطط قابل للتحريك والتكبير",
  unit_plan_alt: "مخطط شقة من {rooms} غرف في الطابق {floor}",
  unit_plan_controls: "أدوات تكبير مخطط الشقة",
  unit_plan_zoom_out: "تصغير المخطط",
  unit_plan_zoom_in: "تكبير المخطط",
  unit_plan_reset: "إعادة الضبط",
  unit_plan_hint: "اسحبوا لمعاينة منطقة محددة. استخدموا القرص بالأصابع أو أزرار التكبير.",
  unit_window_canvas_aria: "مشهد تفاعلي باتجاه نافذة الشقة",
  unit_window_hint: "اسحبوا للنظر إلى الجانبين والأعلى. الطابق والاتجاه مأخوذان من بيانات الشقة؛ المشهد للتوضيح.",
  unit_studio_iframe_title: "مصمم الشقة التفاعلي",
  unit_studio_external: "فتح المصمم في نافذة كاملة",
  unit_studio_unavailable: "المصمم غير متاح لهذه الشقة حاليًا.",
  unit_area_map_aria: "خريطة تفاعلية لمحيط المشروع",
  unit_area_note: "دوروا الخريطة وكبروها لفهم الشوارع والساحل والمسافات المحيطة بالمشروع.",
  unit_area_external: "فتح الموقع في خرائط Google",
  unit_area_unavailable: "ستظهر خريطة المنطقة بعد التحقق من موقع المشروع.",
  unit_contact_intro: "اتركوا وسيلة التواصل الأنسب بشأن شقة من {rooms} غرف بمساحة {sqm} م² في الطابق {floor}.",
  unit_contact_message: "ماذا تريدون أن تعرفوا؟",
  unit_contact_submit: "تواصلوا معي بشأن هذه الشقة",
  unit_contact_name_error: "أدخلوا اسمًا من حرفين على الأقل.",
  unit_contact_channel_error: "أدخلوا رقم هاتف أو عنوان بريد إلكتروني.",
  unit_contact_email_error: "أدخلوا عنوان بريد إلكتروني صحيحًا.",
  unit_contact_consent_error: "يجب الموافقة على شروط التواصل قبل الإرسال.",
  unit_contact_validation_error: "ما زالت بعض التفاصيل مطلوبة قبل إرسال الطلب.",
  unit_contact_unavailable: "خدمة الطلبات غير متاحة مؤقتًا. حاولوا مرة أخرى لاحقًا.",
  unit_contact_payload: "طلب معلومات عن شقة من {rooms} غرف بمساحة {sqm} م² في الطابق {floor}.",
  unit_contact_success: "تم استلام طلبكم. سنتواصل معكم بشأن الشقة التي اخترتموها.",
  unit_contact_failure: "لم يتم إرسال الطلب. بقيت بياناتكم في النموذج لتتمكنوا من المحاولة مجددًا."
});

/* Directional copy is visible at the centre of the v2 decision scene. It must
   never inherit English in FR/RU/AR merely because those dictionaries began
   as EN clones. Short labels are reserved for 568x320-class landscape. */
Object.assign(HE, {
  unit_door_plan_short: "תוכנית",
  unit_door_view_short: "נוף מהחלון",
  unit_door_tour_short: "סיור בדירה",
  unit_door_studio_short: "מעצב"
});
Object.assign(EN, {
  unit_door_plan_short: "Floor plan",
  unit_door_view_short: "Window view",
  unit_door_tour_short: "Home tour",
  unit_door_studio_short: "Designer"
});
Object.assign(FR, {
  orient_sea: "La mer", orient_reading: "La tour Reading",
  orient_district: "Le quartier Sde Dov", orient_district_north: "Le nord du quartier",
  view_sea_reading: "Mer et tour Reading", view_district: "Quartier Sde Dov",
  view_sea_court: "Mer et cour", view_urban: "Tissu urbain",
  view_garden: "Jardin intérieur", view_sea: "Mer dégagée",
  view_park: "Parc", view_coast: "Littoral", view_court: "Cour intérieure",
  view_promenade: "La promenade",
  unit_door_plan_short: "Plan", unit_door_view_short: "Vue fenêtre",
  unit_door_tour_short: "Visite", unit_door_studio_short: "Décorateur"
});
Object.assign(RU, {
  orient_sea: "Море", orient_reading: "Башня Рединг",
  orient_district: "Район Сде-Дов", orient_district_north: "Север района",
  view_sea_reading: "Море и башня Рединг", view_district: "Район Сде-Дов",
  view_sea_court: "Море и двор", view_urban: "Городская застройка",
  view_garden: "Внутренний сад", view_sea: "Открытое море",
  view_park: "Парк", view_coast: "Береговая линия", view_court: "Внутренний двор",
  view_promenade: "Набережная",
  unit_door_plan_short: "План", unit_door_view_short: "Вид из окна",
  unit_door_tour_short: "Тур", unit_door_studio_short: "Дизайнер"
});
Object.assign(AR, {
  orient_sea: "البحر", orient_reading: "برج ريدينغ",
  orient_district: "حي سديه دوف", orient_district_north: "شمال الحي",
  view_sea_reading: "البحر وبرج ريدينغ", view_district: "حي سديه دوف",
  view_sea_court: "البحر والفناء", view_urban: "المشهد الحضري",
  view_garden: "الحديقة الداخلية", view_sea: "البحر المفتوح",
  view_park: "الحديقة", view_coast: "الساحل", view_court: "الفناء الداخلي",
  view_promenade: "الممشى البحري",
  unit_door_plan_short: "المخطط", unit_door_view_short: "الإطلالة",
  unit_door_tour_short: "الجولة", unit_door_studio_short: "المصمم"
});

  window.NADLAN_I18N = {
    langs: { he: HE, en: EN, fr: FR, ru: RU, ar: AR },
    fallback: ["en", "he"]
  };
})();
