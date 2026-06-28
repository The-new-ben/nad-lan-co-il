/* ============================================================================
   NadLan Showroom — DATA LAYER  (window.NADLAN_SHOWROOM)
   ----------------------------------------------------------------------------
   CMS-READY, NOT CMS-WIRED. Every value the engine renders comes from this
   object or from an i18n key (engine/i18n.js). In WordPress this entire object
   is printed by the theme:
       window.NADLAN_SHOWROOM = <?php echo wp_json_encode( nadlan_showroom_payload() ); ?>;
   Field names mirror the repo `nadlan_project` / showroom-payload.json shape so
   the port is a straight swap. See NOTES.md for the full field inventory.

   ============================================================================ */
(function () {
  "use strict";

  /* --- shared spokes (hub-and-spoke DB; many projects reference one record) --- */
  var SPOKES = {
    "reading-tower":   { id: "reading-tower",   type: "anchor",     icon: "landmark",  label_key: "spoke_reading_tower",   geo: { lat: 32.0972, lng: 34.7725 } },
    "tlv-beach":       { id: "tlv-beach",       type: "facility",   icon: "wave",      label_key: "spoke_beach",           geo: { lat: 32.1045, lng: 34.7702 } },
    "light-rail-green":{ id: "light-rail-green",type: "transport",  icon: "train",     label_key: "spoke_light_rail",      geo: { lat: 32.1018, lng: 34.7836 } },
    "yarkon-park":     { id: "yarkon-park",     type: "facility",   icon: "tree",      label_key: "spoke_yarkon_park",     geo: { lat: 32.0975, lng: 34.7900 } },
    "sde-dov-school":  { id: "sde-dov-school",  type: "education",  icon: "school",    label_key: "spoke_school",          geo: { lat: 32.1083, lng: 34.7861 } },
    "commercial-hub":  { id: "commercial-hub",  type: "facility",   icon: "store",     label_key: "spoke_commercial",      geo: { lat: 32.1066, lng: 34.7849 } },
    "ayalon-access":   { id: "ayalon-access",   type: "transport",  icon: "road",      label_key: "spoke_road",            geo: { lat: 32.1100, lng: 34.7950 } }
  };

  /* --- areas: a project belongs to an area; area owns the map + spoke set --- */
  var AREAS = {
    "sde-dov": {
      id: "sde-dov",
      label_key: "area_sde_dov",
      blurb_key: "area_sde_dov_blurb",
      /* map: real geo for the WordPress Mapbox port + normalized x/y (%) for the
         engine's built-in stylized map. Pins resolve labels via spoke label_key. */
      map: {
        center: { lat: 32.1045, lng: 34.7835 },
        zoom: 14,
        bbox: { w: 34.766, s: 32.092, e: 34.802, n: 32.116 },
        coast_x: 16,
        project_pin: { x: 33, y: 50 },
        pins: [
          { ref: "reading-tower",    x: 24, y: 82 },
          { ref: "tlv-beach",        x: 11, y: 34 },
          { ref: "light-rail-green", x: 58, y: 60 },
          { ref: "yarkon-park",      x: 70, y: 80 },
          { ref: "sde-dov-school",   x: 62, y: 30 },
          { ref: "commercial-hub",   x: 52, y: 42 },
          { ref: "ayalon-access",    x: 86, y: 56 }
        ]
      },
      /* spoke modules shown in block 8; each module = a card group. Stats values
         are sourced public Sde Dov figures the owner verifies before publish. */
      stats: [
        { id: "plan",      value: "TA/4444",  label_key: "stat_plan" },
        { id: "units",     value: "16,000",   label_key: "stat_units" },
        { id: "dunams",    value: "1,300",    label_key: "stat_dunams" },
        { id: "residents", value: "40,000",   label_key: "stat_residents" }
      ],
      spoke_groups: [
        { id: "transport", icon: "train",  label_key: "spoke_transport", items: ["light-rail-green", "ayalon-access"] },
        { id: "education", icon: "school", label_key: "spoke_education", items: ["sde-dov-school"] },
        { id: "facilities",icon: "store",  label_key: "spoke_facilities",items: ["tlv-beach", "yarkon-park", "commercial-hub"] },
        { id: "anchor",    icon: "landmark",label_key:"spoke_anchor",    items: ["reading-tower"] }
      ]
    }
  };

  /* --- unit factory: structured facts only; display strings composed via i18n --- */
  function unit(o) {
    return {
      id: o.id, label: o.label, building: o.building,
      floor: o.floor, rooms: o.rooms, sqm: o.sqm, balcony: o.balcony || "",
      dir: o.dir,
      status: o.status,
      recommended: !!o.recommended,
      view_key: o.view_key || "",       // optional content key (per-lang in project.content)
      price_estimate_key: "price_on_request",
      plan: o.plan || "",               // floor-plan asset url (empty -> tab shows "coming")
      interior_url: o.interior_url || "",
      tour_url: o.tour_url || "",
      hotspot_position: o.hotspot_position || "",
      hotspot_normal: o.hotspot_normal || "0 0 1",
      camera_orbit: o.camera_orbit || "",
      stage_x: o.stage_x, stage_y: o.stage_y, stage_w: o.stage_w || 17, stage_h: o.stage_h || 9
    };
  }

  /* --- projects (the catalog). Ashira = real values from the repo payload. --- */
  var PROJECTS = {
    "ashira-sde-dov": {
      slug: "ashira-sde-dov", area: "sde-dov", building: "Ashira",
      name_key: "proj_ashira_name", city_key: "city_tlv",
      floors: 20, floor_height_m: 3.05, viewbox: "0 0 1000 1333",
      model_glb: "engine/models/ashira.glb",
      model_poster: "engine/models/ashira-poster.jpg",
      facade_image: "engine/models/ashira-facade.jpg",
      default_orbit: "-30deg 73deg 142m", default_target: "0m 30m 0m", frame_radius_m: 142,
      orientation: { west: "orient_sea", south: "orient_reading", east: "orient_district", north: "orient_district_north" },
      concept: true,
      video_url: "", tour_url: "", gallery: [],   // contractor-fed media -> block 7 collapses while empty
      units: [
        unit({ id: "ashira-18-west",   label: "18W", building: "Ashira", floor: 18, rooms: 5, sqm: 132, dir: "west",       status: "available", recommended: true,  view_key: "view_sea_reading",  hotspot_position: "0 18 0",  camera_orbit: "-42deg 60deg 95%",  stage_x: 42, stage_y: 30, plan: "plans/ashira-5.svg" }),
        unit({ id: "ashira-14-city",   label: "14C", building: "Ashira", floor: 14, rooms: 4, sqm: 104, dir: "east",       status: "available", recommended: false, view_key: "view_district",     hotspot_position: "4 14 0",  camera_orbit: "30deg 64deg 95%",   stage_x: 58, stage_y: 42, plan: "plans/ashira-4.svg" }),
        unit({ id: "ashira-10-corner", label: "10P", building: "Ashira", floor: 10, rooms: 4, sqm: 118, dir: "south-west", status: "reserved",  recommended: true,  view_key: "view_sea_court",    hotspot_position: "-4 10 0", camera_orbit: "-58deg 66deg 92%",  stage_x: 32, stage_y: 56, plan: "plans/ashira-4-corner.svg" }),
        unit({ id: "ashira-07-east",   label: "7A",  building: "Ashira", floor: 7,  rooms: 3, sqm: 82,  dir: "east",       status: "sold",      recommended: false, view_key: "view_urban",       hotspot_position: "4 7 0",   camera_orbit: "36deg 68deg 92%",   stage_x: 64, stage_y: 66, plan: "plans/ashira-3.svg" }),
        unit({ id: "ashira-04-garden", label: "4G",  building: "Ashira", floor: 4,  rooms: 3, sqm: 92,  dir: "west",       status: "available", recommended: false, view_key: "view_garden",      hotspot_position: "0 4 0",   camera_orbit: "-48deg 72deg 90%",  stage_x: 48, stage_y: 78, plan: "plans/ashira-3-garden.svg" })
      ],
      content: {
        he: { tagline: "דירות חדשות בשדה דב, מול הים", hero_p: "בחרו דירה לפי קומה, כיוון, שטח ונוף, וקבלו תמונת מצב ברורה של הפרויקט והסביבה לפני פנייה לנציג.", seo_h: "Ashira שדה דב: בחירת דירה מתוך הבניין", seo_p: "העמוד מרכז את מסע הבחירה של הרוכש: תצוגת בניין, בחירת דירה, תכנית, כיוון, נוף, סביבת רובע שדה דב ופנייה שמגיעה עם פרטי הדירה שבחרתם. הנתונים להמחשה ויש לאמת מחיר וזמינות מול היזם." },
        en: { tagline: "New homes in Sde Dov, by the sea", hero_p: "Choose a home by floor, facing, area and view, then enquire with the exact apartment context attached.", seo_h: "Ashira Sde Dov: choose an apartment from the building", seo_p: "This page is built around the buyer journey: understand the building, select a home, review the plan and direction, see the surrounding district and send an enquiry linked to the apartment selected. All data is illustrative and must be verified with the developer." },
        fr: { tagline: "Logements neufs à Sde Dov, près de la mer", hero_p: "Choisissez un appartement par étage, orientation, surface et vue avant de contacter l’équipe.", seo_h: "Ashira Sde Dov: choisir un appartement dans l’immeuble", seo_p: "La page aide l’acheteur à comprendre le bâtiment, choisir un logement, consulter le plan et découvrir le quartier avant de laisser une demande ciblée." },
        ru: { tagline: "Новые квартиры в Сде-Дов у моря", hero_p: "Выберите квартиру по этажу, стороне, площади и виду, прежде чем отправить заявку.", seo_h: "Ashira Sde Dov: выбор квартиры в здании", seo_p: "Страница помогает покупателю увидеть проект, выбрать квартиру, изучить план и окружение, а затем отправить заявку с выбранной квартирой." },
        ar: { tagline: "شقق جديدة في سديه دوف قرب البحر", hero_p: "اختاروا الشقة حسب الطابق والاتجاه والمساحة والإطلالة قبل إرسال الطلب.", seo_h: "Ashira سديه دوف: اختيار شقة من داخل المبنى", seo_p: "تعرض الصفحة رحلة المشتري: فهم المبنى، اختيار الشقة، مراجعة الخطة والتعرّف إلى البيئة المحيطة قبل إرسال طلب مرتبط بالشقة المختارة." }
      }
    },

    "rainbow-tel-aviv": {
      slug: "rainbow-tel-aviv", area: "sde-dov", building: "Rainbow",
      name_key: "proj_rainbow_name", city_key: "city_tlv",
      floors: 40, floor_height_m: 3.05, viewbox: "0 0 1000 1333",
      model_glb: "engine/models/rainbow.glb",
      model_poster: "engine/models/rainbow-poster.jpg",
      facade_image: "engine/models/rainbow-facade.jpg",
      default_orbit: "-30deg 72deg 210m", default_target: "0m 52m 0m", frame_radius_m: 210,
      orientation: { west: "orient_sea", south: "orient_reading", east: "orient_district", north: "orient_district_north" },
      concept: true, video_url: "", tour_url: "", gallery: [],
      units: [
        unit({ id: "rainbow-31", label: "31W", building: "Rainbow", floor: 31, rooms: 5, sqm: 156, dir: "west",       status: "available", recommended: true,  view_key: "view_sea",      hotspot_position: "0 31 0",  camera_orbit: "-40deg 58deg 92%", stage_x: 46, stage_y: 24, plan: "plans/plan-5.svg" }),
        unit({ id: "rainbow-24", label: "24N", building: "Rainbow", floor: 24, rooms: 4, sqm: 128, dir: "north-west", status: "available", recommended: false, view_key: "view_park",     hotspot_position: "-3 24 0", camera_orbit: "-56deg 62deg 92%", stage_x: 34, stage_y: 40, plan: "plans/plan-4.svg" }),
        unit({ id: "rainbow-16", label: "16W", building: "Rainbow", floor: 16, rooms: 4, sqm: 112, dir: "west",       status: "reserved",  recommended: false, view_key: "view_coast",    hotspot_position: "0 16 0",  camera_orbit: "-44deg 66deg 90%", stage_x: 50, stage_y: 56, plan: "plans/plan-4.svg" }),
        unit({ id: "rainbow-08", label: "8S",  building: "Rainbow", floor: 8,  rooms: 3, sqm: 82,  dir: "south-west", status: "available", recommended: false, view_key: "view_court",    hotspot_position: "-3 8 0",  camera_orbit: "-60deg 70deg 90%", stage_x: 40, stage_y: 72, plan: "plans/plan-3.svg" })
      ],
      content: {
        he: { tagline: "מגדל מול הים בשדה דב", hero_p: "Rainbow מציג דירות גבוהות מול קו החוף, עם בחירה לפי קומה, כיוון ושטח.", seo_h: "Rainbow תל אביב: מגדל מגורים בשדה דב", seo_p: "התצוגה מאפשרת לסנן דירות, להבין את היחס לים ולרובע, ולהשאיר פנייה על דירה מסוימת. הנתונים להמחשה עד לקבלת אישור מלא מהיזם." },
        en: { tagline: "Seafront tower in Sde Dov", hero_p: "Rainbow presents high-rise homes near the coastline with apartment selection by floor, facing and area.", seo_h: "Rainbow Tel Aviv: residential tower in Sde Dov", seo_p: "The showroom lets buyers filter apartments, understand the relation to the sea and district, and enquire about a specific home. Data is illustrative pending developer approval." },
        fr: { tagline: "Tour résidentielle face à la mer à Sde Dov", hero_p: "Choisissez un appartement Rainbow par étage, orientation et surface.", seo_h: "Rainbow Tel Aviv: tour résidentielle à Sde Dov", seo_p: "La présentation aide à comparer les logements et à envoyer une demande ciblée." },
        ru: { tagline: "Башня у моря в Сде-Дов", hero_p: "Выберите квартиру Rainbow по этажу, стороне и площади.", seo_h: "Rainbow Tel Aviv: жилой проект в Сде-Дов", seo_p: "Витрина помогает сравнить квартиры и отправить точную заявку." },
        ar: { tagline: "برج سكني مقابل البحر في سديه دوف", hero_p: "اختاروا شقة في Rainbow حسب الطابق والاتجاه والمساحة.", seo_h: "Rainbow تل أبيب: برج سكني في سديه دوف", seo_p: "تساعد الواجهة على مقارنة الشقق وإرسال طلب محدد." }
      }
    },

    "dimri-yama": {
      slug: "dimri-yama", area: "sde-dov", building: "Dimri Yama",
      name_key: "proj_dimri_name", city_key: "city_tlv",
      floors: 24, floor_height_m: 3.1, viewbox: "0 0 1000 1333",
      model_glb: "engine/models/dimri.glb",
      model_poster: "engine/models/dimri-poster.jpg",
      facade_image: "engine/models/dimri-facade.jpg",
      default_orbit: "-30deg 73deg 150m", default_target: "0m 32m 0m", frame_radius_m: 150,
      orientation: { west: "orient_sea", south: "orient_reading", east: "orient_district", north: "orient_district_north" },
      concept: true, video_url: "", tour_url: "", gallery: [],
      units: [
        unit({ id: "dimri-22", label: "22W", building: "Dimri Yama", floor: 22, rooms: 5, sqm: 165, dir: "west",       status: "available", recommended: true,  view_key: "view_sea",   hotspot_position: "0 22 0",  camera_orbit: "-40deg 60deg 92%", stage_x: 48, stage_y: 28, plan: "plans/plan-5.svg" }),
        unit({ id: "dimri-15", label: "15S", building: "Dimri Yama", floor: 15, rooms: 4, sqm: 120, dir: "south-west", status: "available", recommended: false, view_key: "view_promenade", hotspot_position: "-3 15 0", camera_orbit: "-58deg 66deg 90%", stage_x: 38, stage_y: 50, plan: "plans/plan-4.svg" }),
        unit({ id: "dimri-09", label: "9N",  building: "Dimri Yama", floor: 9,  rooms: 3, sqm: 88,  dir: "north-west", status: "reserved",  recommended: false, view_key: "view_park",   hotspot_position: "-3 9 0",  camera_orbit: "-56deg 70deg 90%", stage_x: 52, stage_y: 68, plan: "plans/plan-3.svg" })
      ],
      content: {
        he: { tagline: "בניין גן מול הים", hero_p: "דימרי ימה מציג דירות ברובע שדה דב עם דגש על סביבת מגורים, גינות, כיווני אוויר ונגישות לים.", seo_h: "דימרי ימה שדה דב: בחירת דירה לפי קומה וסביבה", seo_p: "התצוגה מציגה את הפרויקט, הדירות והסביבה באופן ברור כדי לחבר בין בחירת הדירה לבין החיים היומיומיים ברובע." },
        en: { tagline: "Garden building by the sea", hero_p: "Dimri Yama presents homes in Sde Dov with a focus on living environment, gardens, facing and access to the sea.", seo_h: "Dimri Yama Sde Dov: choose by floor and surroundings", seo_p: "The showroom connects apartment selection with the daily-life context of the district." },
        fr: { tagline: "Immeuble-jardin près de la mer", hero_p: "Dimri Yama met en avant le cadre de vie, les jardins et l’accès à la mer.", seo_h: "Dimri Yama Sde Dov", seo_p: "La page relie le choix de l’appartement à l’environnement du quartier." },
        ru: { tagline: "Дом-сад у моря", hero_p: "Dimri Yama показывает квартиры с акцентом на среду, сады и доступ к морю.", seo_h: "Dimri Yama Sde Dov", seo_p: "Страница связывает выбор квартиры с окружением района." },
        ar: { tagline: "مبنى حدائق قرب البحر", hero_p: "يعرض Dimri Yama الشقق مع التركيز على البيئة والحدائق والقرب من البحر.", seo_h: "Dimri Yama سديه دوف", seo_p: "تربط الصفحة اختيار الشقة ببيئة الحي اليومية." }
      }
    }
  };

  window.NADLAN_SHOWROOM = {
    schema: "nadlan-showroom-engine/v2",
    config: {
      brand_key: "brand",
      lead_endpoint: "/wp-json/nadlan/v1/lead",
      whatsapp: "",                       // e.g. "972500000000" -> owner fills; sticky WhatsApp hides while empty
      phone: "",
      demo: true,                         // shows the "illustrative" disclaimer band + badges
      default_project: "ashira-sde-dov",
      default_lang: "he",
      languages: ["he", "en", "fr", "ru", "ar"],
      rtl_languages: ["he", "ar"]
    },
    spokes: SPOKES,
    areas: AREAS,
    projects: PROJECTS,
    order: ["ashira-sde-dov", "rainbow-tel-aviv", "dimri-yama"]
  };
})();
