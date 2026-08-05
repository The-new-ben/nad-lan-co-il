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
    status_available: "להמחשה", status_reserved: "בעדיפות", status_sold: "נמכרה",
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
    fact_floors: "קומות", fact_homes: "דירות לבחירה", fact_from_floor: "קומות גבוהות",

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
    status_available: "Illustrative", status_reserved: "On hold", status_sold: "Sold",
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
    fact_floors: "Floors", fact_homes: "Homes to choose", fact_from_floor: "High floors",
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
  RU.fp_salon = "Гостиная и столовая"; RU.fp_kitchen = "Кухня"; RU.fp_mamad = "Защищенная комната";
  RU.fp_master = "Главная спальня"; RU.fp_bed = "Спальня"; RU.fp_balcony = "Балкон";
  RU.fp_aria = "Прогулка внутри квартиры - потяните, чтобы осмотреться";
  RU.fp_hint = "Тяните, чтобы смотреть · нажмите на дверь для перехода";
  RU.fp_tag = "Схематичная визуализация, построенная по данным квартиры";
  AR.fp_salon = "غرفة المعيشة والسفرة"; AR.fp_kitchen = "المطبخ"; AR.fp_mamad = "الغرفة المحصنة";
  AR.fp_master = "غرفة النوم الرئيسية"; AR.fp_bed = "غرفة نوم"; AR.fp_balcony = "الشرفة";
  AR.fp_aria = "جولة داخل الشقة - اسحب للنظر حولك";
  AR.fp_hint = "اسحب للنظر · انقر على باب للانتقال بين الغرف";
  AR.fp_tag = "تصور تخطيطي مبني على بيانات الشقة";
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

  window.NADLAN_I18N = {
    langs: { he: HE, en: EN, fr: FR, ru: RU, ar: AR },
    fallback: ["en", "he"]
  };
})();
