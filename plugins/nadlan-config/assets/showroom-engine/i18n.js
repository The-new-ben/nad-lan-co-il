/* ============================================================================
   NadLan Showroom — i18n LAYER  (window.NADLAN_I18N)
   ----------------------------------------------------------------------------
   Every UI string the engine renders is a key here. No chrome text is hardcoded
   in HTML or engine.js. In WordPress these tables become the theme's translation
   files (or pll__/__() calls); the engine swaps to a server t() with no markup
   change. See NOTES.md for the full key inventory.

   HE + EN are complete. FR / RU / AR are SCAFFOLDED: every slot exists (cloned
   from EN as a placeholder) so the owner's translators fill values in place.
   Resolution order in t():  lang -> en -> he -> key.
   Marketing / SEO PROSE is NOT here — that lives in data.js content blocks as
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
    status_available: "זמינה", status_reserved: "בעדיפות", status_sold: "נמכרה",
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
    legend_available: "זמינה", legend_reserved: "בעדיפות", legend_sold: "נמכרה",
    loading_model: "טוען תצוגה…",

    /* facade backup (block 4) */
    facade_title: "בחירה מהירה מהחזית",
    facade_sub: "כל ריבוע הוא דירה. מתאים גם למובייל ולבחירה מדויקת.",

    /* apartment panel (block 5) */
    panel_prompt: "בחרו דירה מהבניין או מהחזית",
    panel_floor: "קומה", panel_rooms: "חדרים", panel_sqm: "שטח", panel_balcony: "מרפסת",
    panel_view: "נוף", panel_dir: "כיוון", panel_status: "סטטוס", panel_price: "אומדן",
    tab_plan: "תכנית", tab_view: "מבט", tab_tour: "סיור",
    plan_coming: "תכנית הדירה תוצג לאחר קבלת תוכנית מכר מאושרת.",
    view_coming: "מבט מהדירה יוצג לאחר אימות מיקום מול היזם.",
    tour_coming: "סיור פנים יוצג כאשר יתקבל קישור מאושר.",
    btn_inquire: "מעניין אותי", btn_save: "שמירה", btn_saved: "נשמר", btn_compare: "להשוואה",
    btn_compared: "בהשוואה", btn_share: "שיתוף", btn_close: "סגירה", link_copied: "הקישור הועתק",

    /* inventory (block 6) */
    inventory_title: "כל הדירות בפרויקט",
    inventory_sub: "בחירה כאן מסמנת את הדירה גם בבניין וגם בחזית.",
    filter_all: "הכל", filter_available: "זמינות", filter_3: "3 חד׳", filter_4: "4 חד׳", filter_5: "5 חד׳",
    results_count: "{n} דירות",

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

    /* SEO body (block 10) — heading chrome only; prose from data.content */
    seo_eyebrow: "על הפרויקט",

    /* inquiry (block 11) — the money moment */
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
    status_available: "Available", status_reserved: "On hold", status_sold: "Sold",
    orient_sea: "The sea", orient_reading: "Reading Tower", orient_district: "Sde Dov district", orient_district_north: "District, north",
    view_sea_reading: "Sea & Reading Tower", view_district: "Sde Dov district", view_sea_court: "Sea & courtyard", view_urban: "Urban fabric", view_garden: "Inner garden", view_sea: "Open sea", view_park: "Park", view_coast: "Coastline", view_court: "Inner court", view_promenade: "Promenade",
    apt_word: "Apartment", rooms_label: "{n} rooms", floor_label: "Floor {n}", sqm_unit: "m\u00B2",
    unit_short: "Apt {label} · Floor {floor}",
    price_on_request: "Estimate on request",
    nav_projects: "Projects", nav_areas: "Areas", nav_guides: "Guides", nav_list: "List with us",
    secnav_building: "Building", secnav_apartments: "Apartments", secnav_environment: "Surroundings", secnav_media: "Media", secnav_info: "Info", secnav_aria: "On-page navigation",
    hero_eyebrow: "Sde Dov district · By the sea",
    hero_cta_primary: "Enquire",
    hero_cta_secondary: "Choose an apartment",
    fact_floors: "Floors", fact_homes: "Homes to choose", fact_from_floor: "High floors",
    theater_eyebrow: "Project showroom",
    theater_title: "Choose an apartment from the building",
    theater_hint: "Drag to rotate · tap an apartment",
    view_3d: "3D", view_facade: "Facade",
    legend_available: "Available", legend_reserved: "On hold", legend_sold: "Sold",
    loading_model: "Loading view…",
    facade_title: "Quick pick from the facade",
    facade_sub: "Each square is an apartment. Ideal on mobile and for precise picking.",
    panel_prompt: "Select an apartment from the building or the facade",
    panel_floor: "Floor", panel_rooms: "Rooms", panel_sqm: "Area", panel_balcony: "Balcony",
    panel_view: "View", panel_dir: "Facing", panel_status: "Status", panel_price: "Estimate",
    tab_plan: "Plan", tab_view: "View", tab_tour: "Tour",
    plan_coming: "The floor plan will appear once an approved sales plan is provided.",
    view_coming: "The view from the apartment will appear after location is verified.",
    tour_coming: "An interior tour will appear once an approved link is provided.",
    btn_inquire: "I'm interested", btn_save: "Save", btn_saved: "Saved", btn_compare: "Compare",
    btn_compared: "Comparing", btn_share: "Share", btn_close: "Close", link_copied: "Link copied",
    inventory_title: "All apartments",
    inventory_sub: "Picking here marks the apartment on the building and the facade too.",
    filter_all: "All", filter_available: "Available", filter_3: "3 rm", filter_4: "4 rm", filter_5: "5 rm",
    results_count: "{n} apartments",
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

  /* FR / RU / AR — scaffold: every slot present, EN placeholder values. Owner's
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

  window.NADLAN_I18N = {
    langs: { he: HE, en: EN, fr: FR, ru: RU, ar: AR },
    fallback: ["en", "he"]
  };
})();
