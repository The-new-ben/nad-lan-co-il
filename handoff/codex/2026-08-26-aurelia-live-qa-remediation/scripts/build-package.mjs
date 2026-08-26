import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const packageRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:[A-Za-z]:)/, p => p.slice(1))), '..');
const repoRoot = path.resolve(packageRoot, '..', '..', '..');
const previousRoot = path.join(repoRoot, 'handoff', 'codex', '2026-08-25-aurelia-master-recipe');

const writeJson = (relative, value) => {
  const target = path.join(packageRoot, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
};
const writeText = (relative, value) => {
  const target = path.join(packageRoot, relative);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, value, 'utf8');
};
const sha256 = buffer => crypto.createHash('sha256').update(buffer).digest('hex');
const csvCell = value => `"${String(value ?? '').replaceAll('"', '""')}"`;

const facilities = [
  {
    id: 'facility-lobby-concierge', order: 1, nameHe: 'לובי וקונסיירז׳', nameEn: 'Lobby & concierge',
    level: 'G', zone: 'arrival', areaSqm: 420, capacity: 70,
    asset: '04-ASSETS/facilities/facility-01-lobby-concierge-360.png',
    summaryHe: 'חלל הכניסה המרכזי מחבר בין הרחוב, הקונסיירז׳, אזור ההמתנה, חדר החבילות ומעליות המגורים.',
    equipment: ['2 עמדות קונסיירז׳', 'שערי כניסה מאובטחים', 'טרקלין המתנה', 'חדר חבילות', 'אזור דואר', 'לובי מעליות', 'לולאת השראה לכבדי שמיעה'],
    sceneHotspots: ['עמדת קונסיירז׳', 'שערי דיירים', 'חדר חבילות', 'לובי מעליות', 'טרקלין אורחים', 'מסלול נגיש']
  },
  {
    id: 'facility-infinity-pool', order: 2, nameHe: 'בריכת אינפיניטי ומרפסת Wellness', nameEn: 'Infinity pool & wellness terrace',
    level: 'L05', zone: 'west-podium', areaSqm: 780, capacity: 96,
    asset: '04-ASSETS/facilities/facility-02-infinity-pool-360.png',
    summaryHe: 'בריכת שחייה מלאה עם אזור שיזוף, מקלחות, מלתחות, תחנת מגבות וגישה נגישה למים.',
    equipment: ['בריכת מסלולים', 'מעלון בריכה', 'מקלחות', 'מלתחות', 'תחנת מגבות', 'מיטות שיזוף', 'עמדת בטיחות'],
    sceneHotspots: ['מסלול שחייה', 'מעלון נגיש', 'מלתחות', 'מקלחות', 'תחנת מגבות', 'מרפסת הים']
  },
  {
    id: 'facility-gym', order: 3, nameHe: 'מועדון כושר', nameEn: 'Residents gym',
    level: 'L04', zone: 'west-podium', areaSqm: 610, capacity: 58,
    asset: '04-ASSETS/facilities/facility-03-gym-360.png',
    summaryHe: 'חדר כושר מחולק לקרדיו, כוח, משקולות חופשיות, אימון פונקציונלי, מתיחות והתאוששות.',
    equipment: ['12 עמדות קרדיו', '8 מכשירי כוח', '2 ספסלי משקולות', 'כלוב פונקציונלי', 'משקולות חופשיות', 'אזור מתיחות', 'תחנת מים'],
    sceneHotspots: ['קרדיו', 'מכשירי כוח', 'משקולות חופשיות', 'אימון פונקציונלי', 'מתיחות', 'לוקרים ומים']
  },
  {
    id: 'facility-spa-recovery', order: 4, nameHe: 'ספא והתאוששות', nameEn: 'Spa & recovery suite',
    level: 'L04', zone: 'east-podium', areaSqm: 460, capacity: 42,
    asset: '04-ASSETS/facilities/facility-04-spa-recovery-360.png',
    summaryHe: 'מתחם טיפולים והתאוששות עם סאונה, חדר אדים, חדרי טיפול, אזור מנוחה ומלתחות נגישות.',
    equipment: ['סאונה', 'חדר אדים', '2 חדרי טיפול', '12 מיטות מנוחה', 'תחנת שתייה', 'מקלחות', 'אחסון מגבות'],
    sceneHotspots: ['קבלה', 'סאונה', 'חדר אדים', 'חדר טיפולים', 'מנוחה', 'מלתחות נגישות']
  },
  {
    id: 'facility-lounge-library', order: 5, nameHe: 'טרקלין דיירים וספרייה', nameEn: 'Residents lounge & library',
    level: 'L03', zone: 'central-podium', areaSqm: 530, capacity: 82,
    asset: '04-ASSETS/facilities/facility-05-residents-lounge-library-360.png',
    summaryHe: 'טרקלין גמיש לפגישות, קריאה ואירוח, עם ספרייה, חדרים שקטים, עמדת קפה ויציאה למרפסת.',
    equipment: ['ספרייה', '4 קבוצות ישיבה', '2 חדרים שקטים', 'עמדת קפה', 'שקעי טעינה', 'אח דקורטיבי', 'מרפסת'],
    sceneHotspots: ['ספרייה', 'טרקלין', 'חדר שקט', 'קפה', 'טעינה', 'מרפסת']
  },
  {
    id: 'facility-coworking', order: 6, nameHe: 'מועדון עסקים ועבודה', nameEn: 'Coworking & business club',
    level: 'L03', zone: 'east-podium', areaSqm: 490, capacity: 64,
    asset: '04-ASSETS/facilities/facility-06-coworking-business-club-360.png',
    summaryHe: 'סביבת עבודה מלאה הכוללת עמדות אישיות, חדרי ישיבות, תאי שיחה, הדפסה ומטבחון.',
    equipment: ['24 עמדות עבודה', '4 חדרי ישיבות', '5 תאי שיחה', 'עמדת הדפסה', 'מסך מצגות', 'מטבחון', 'עמדות נגישות'],
    sceneHotspots: ['עמדות עבודה', 'חדר ישיבות', 'תא שיחה', 'הדפסה', 'מצגות', 'מטבחון']
  },
  {
    id: 'facility-childrens-club', order: 7, nameHe: 'מועדון ילדים ומשפחה', nameEn: 'Children’s club & family room',
    level: 'L02', zone: 'garden-podium', areaSqm: 440, capacity: 55,
    asset: '04-ASSETS/facilities/facility-07-childrens-club-360.png',
    summaryHe: 'מועדון משפחתי בטוח עם אזורי פעוטות, יצירה, קריאה, משחק רך, ישיבת הורים ואחסון עגלות.',
    equipment: ['אזור פעוטות', 'משחק רך', 'שולחנות יצירה', 'פינת קריאה', 'ישיבת הורים', 'שטיפת ידיים', 'חניית עגלות'],
    sceneHotspots: ['פעוטות', 'משחק רך', 'יצירה', 'קריאה', 'הורים', 'אחסון עגלות']
  },
  {
    id: 'facility-private-dining', order: 8, nameHe: 'חדר אוכל ואירוח פרטי', nameEn: 'Private dining & events',
    level: 'L03', zone: 'west-podium', areaSqm: 370, capacity: 44,
    asset: '04-ASSETS/facilities/facility-08-private-dining-event-360.png',
    summaryHe: 'חלל אירוח שניתן להזמנה עם שולחן מרכזי, מטבח תצוגה, הכנת קייטרינג, בר ומרפסת.',
    equipment: ['שולחן ל-24', 'מטבח תצוגה', 'הכנת קייטרינג', 'בר', 'מסך מצגות', 'טרקלין גמיש', 'מרפסת'],
    sceneHotspots: ['שולחן אירוח', 'מטבח', 'קייטרינג', 'בר', 'מסך', 'מרפסת']
  },
  {
    id: 'facility-sky-garden', order: 9, nameHe: 'גן שמיים וטרקלין שקיעה', nameEn: 'Sky garden & sunset lounge',
    level: 'L47', zone: 'roof', areaSqm: 690, capacity: 88,
    asset: '04-ASSETS/facilities/facility-09-rooftop-sky-garden-360.png',
    summaryHe: 'גן גג מוגן רוח עם אזורי ישיבה, מטבח חוץ, שולחנות, שבילים נגישים ותצפית לים ולפארק.',
    equipment: ['צמחייה מוגנת רוח', '5 קבוצות ישיבה', 'מטבח חוץ', '4 שולחנות', 'תאורת לילה', 'שביל נגיש', 'לובי מעליות'],
    sceneHotspots: ['מבט לים', 'מבט לפארק', 'מטבח חוץ', 'ישיבה', 'שביל נגיש', 'לובי הגג']
  },
  {
    id: 'facility-cinema', order: 10, nameHe: 'חדר קולנוע פרטי', nameEn: 'Private cinema',
    level: 'L02', zone: 'east-podium', areaSqm: 230, capacity: 32,
    asset: '04-ASSETS/facilities/facility-10-private-cinema-360.png',
    summaryHe: 'חדר הקרנה אקוסטי עם ישיבה מדורגת, מקומות נגישים, מערכת AV, מזנון קטן ולובי אקוסטי.',
    equipment: ['מסך הקרנה', '28 מושבים', '2 מקומות כיסא גלגלים', 'מערכת AV', 'תאורת מעברים', 'מזנון', 'לובי אקוסטי'],
    sceneHotspots: ['מסך', 'ישיבה', 'מקומות נגישים', 'מערכת AV', 'מזנון', 'יציאות']
  },
  {
    id: 'facility-movement-studio', order: 11, nameHe: 'סטודיו יוגה ופילאטיס', nameEn: 'Yoga & Pilates studio',
    level: 'L04', zone: 'south-podium', areaSqm: 310, capacity: 36,
    asset: '04-ASSETS/facilities/facility-11-yoga-pilates-360.png',
    summaryHe: 'סטודיו תנועה עם מכשירי רפורמר, אזור מזרנים, באר, אחסון, מראות ומרווחי עבודה נגישים.',
    equipment: ['10 מכשירי רפורמר', 'אזור 20 מזרנים', 'באר', 'קיר מראות', 'אחסון ציוד', 'עמדת מדריך', 'תחנת מים'],
    sceneHotspots: ['רפורמר', 'מזרנים', 'באר', 'מראות', 'אחסון', 'עמדת מדריך']
  },
  {
    id: 'facility-mobility-room', order: 12, nameHe: 'חדר אופניים, ניידות ושירות', nameEn: 'Bicycle, mobility & service room',
    level: 'B1', zone: 'service-core', areaSqm: 360, capacity: 150,
    asset: '04-ASSETS/facilities/facility-12-bicycle-mobility-room-360.png',
    summaryHe: 'חדר שירות מאובטח לאופניים, מטען, עגלות וכיסאות גלגלים, עם תיקון, טעינה, רחצה וחבילות.',
    equipment: ['110 מתקני אופניים', '12 מקומות אופני מטען', '16 לוקרי טעינה', 'עמדת תיקון', 'שטיפת אופניים', 'אחסון עגלות', 'לוקרי חבילות'],
    sceneHotspots: ['חניית אופניים', 'אופני מטען', 'טעינה', 'תיקון', 'רחצה', 'חבילות']
  }
].map(f => ({
  ...f,
  valueMode: 'prototype-generated-estimate',
  modelAnchor: { type: 'gltf-node', nodeName: `FACILITY__${f.id.replace('facility-', '').replaceAll('-', '_').toUpperCase()}`, requiredInSemanticGlb: true },
  planAnchor: { type: 'facility-zone-feature', featureId: f.id, source: 'facility-zones.geojson' },
  buyerActions: ['פתיחת סיור 360', 'הצגה במפת המתחם', 'הצגת נתוני המתקן', 'שמירה למועדפים', 'שיחה עם נציג על המתקן'],
  accessibility: ['מסלול ללא מדרגה', 'רוחב מעבר נגיש', 'נקודת סיבוב לכיסא גלגלים', 'תיאור טקסטואלי מקביל לסיור'],
  hoursModel: 'managed-in-cms',
  publicMissingCopyAllowed: false
}));

const sourceFingerprint = {
  capturedAt: '2026-08-26T00:00:00+03:00',
  url: 'https://nad-lan.co.il/projects/aurelia/?project=aurelia&lang=he&unit=aur-t-13-e',
  captureMode: 'public-server-response-view-source',
  http: { status: 200, server: 'nginx', charset: 'UTF-8', bytes: 496379 },
  rawSha256: '004a1559cfe928c732f00a551e420fde75bd5191c262c7088a5331eaff7b40bc',
  rawHashUse: 'Evidence for this single response only; repeated raw responses vary because of contact/email obfuscation.',
  canonicalizedSnapshot: { chars: 490124, sha256: '7dc8375e5408535eab85d8f92d97cc3b23e30d27b98c53efbe5533d087bcb0de', stableAcrossTwoRequests: true },
  redactedSnapshot: { chars: 232714, sha256: 'a70f6a9a5cf56ef43c6e1256a7c7b6af04ca5f8056af0e66924eedf6998f9340', stableAcrossTwoRequests: true, stored: false, reason: 'Do not place public tokens/endpoints/contact payload under public uploads or in the handoff.' },
  seo: {
    title: 'אורליה שדה דב Aurelia | דירות, תוכניות, נוף ומחירים | נדלן',
    canonical: 'https://nad-lan.co.il/projects/aurelia/', h1Count: 1,
    robots: 'index, follow', hreflang: ['he', 'x-default'],
    runtimeLanguagesDeclared: ['he', 'en', 'fr', 'ru', 'ar'],
    structuredDataBlocks: 5,
    structuredDataTypes: ['Yoast graph', 'FAQPage', 'ApartmentComplex', 'BreadcrumbList', 'FAQPage'],
    schemaContradictions: ['Two non-identical BreadcrumbList objects', 'Two FAQPage objects', 'Facilities claimed in FAQ/meta but facilities data and UI are absent', 'ApartmentComplex lacks image, offers and amenityFeature']
  },
  favicon: { sourceHasIcons: true, urlsRespond200: true, mimeValid: true, conclusion: 'Not broken in public source. SERP absence must be checked with live SERP/GSC recrawl evidence.' },
  missingSecurityHeadersObserved: ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Content-Type-Options', 'Referrer-Policy', 'Permissions-Policy', 'X-Frame-Options'],
  runtime: {
    pluginHealthLive: '1.72.220', pluginRepoObserved: '1.72.206',
    coreAssetsByteEqualOrLineEndingOnly: ['engine.js', 'mv-ux.js', 'showroom.css', 'mapbox-init.js', 'studio.js', 'buyflow.js', 'i18n.js', 'tokens.css', 'editorial.css'],
    liveOnlyInlineAdapter: { sha256: 'fa8249a43bdceefe07cfefbe9fd3ad278eab15e9594de3776799743e6b4bdd31', chars: 8104, repositoryMatch: false, behavior: 'Hides 320 canonical hotspots and creates six overlay dots.' }
  }
};

const adminContract = {
  capturedAt: '2026-08-26T00:00:00+03:00', postId: 7514, slug: 'aurelia', postType: 'nadlan_project',
  title: 'Aurelia Sde Dov - אורליה שדה דב', contentChars: 1408, excerptChars: 87,
  recipeBox: { renderedChecks: 0, renderedMessage: 'המתכון מופעל כעת רק על פרויקט האב אורליה.', problem: 'Prototype hard-scoping does not match live post 7514/slug aurelia.' },
  bomBox: { renderedAssemblies: 0, renderedMessage: 'ה-BOM מופעל כעת רק על פרויקט האב אורליה.', problem: 'Prototype hard-scoping does not match live post 7514/slug aurelia.' },
  showroomMeta: { enabled: true, latitude: 32.1057, longitude: 34.7779, posterPresent: true, glbPresent: true },
  p3dMeta: {
    modelType: 'procedural', glbPresent: true, usdzPresent: false, projectVideoPresent: false, projectTourPresent: false, cesiumTilesPresent: false,
    cameraLock: 'horizontal', autoRotate: false, floorHeightM: 3.05, groundElevationM: null, averageEstimatedPricePerSqm: 99000,
    units: 320, status: { available: 302, reserved: 18 },
    unitFieldCoverage: { plan: 320, hotspotPosition: 320, hotspotNormal: 320, price: 320, azimuth: 0, interiorUrl: 0, viewAsset: 0 },
    uniquePlans: 5
  },
  yoast: {
    title: 'אורליה שדה דב Aurelia | דירות, תוכניות, נוף ומחירים | נדלן',
    description: 'בחרו דירה באורליה שדה דב לפי קומה וכיוון, צפו בתוכנית, בנוף ובסיור הפנים, בדקו את מתקני הפרויקט והסביבה וקבלו תוכניות ומחירים מותאמים לדירה שבחרתם.',
    focusKeyphrase: 'אורליה שדה דב',
    contradiction: 'The description claims facilities although no facilities contract or UI exists.'
  }
};

const liveFindings = [
  ['LIVE-001','red','מובייל','320 hotspots קאנוניים מוסתרים: opacity 0 ו-pointer-events none; ה-adapter החי יוצר שש נקודות שגם הן hidden/0×0 בבדיקה.','Browser DOM + computed styles + live-only inline adapter hash','plugins/nadlan-config/assets/showroom-engine/engine.js:370-395'],
  ['LIVE-002','red','מובייל','320 hotspots מוסתרים נשארים tabindex=0 ויוצרים מאות תחנות focus בלתי נראות.','Browser keyboard/DOM audit','plugins/nadlan-config/assets/showroom-engine/engine.js:370-395'],
  ['LIVE-003','red','בחירת דירה','בחירת דירה מהמלאי מעדכנת unit אך משאירה את כרטיס היחידה אלפי פיקסלים מעל המשתמש.','Click replay 390/400 CSS px','plugins/nadlan-config/assets/showroom-engine/engine.js:4106-4140'],
  ['LIVE-004','red','כרטיס יחידה','סגירת הכרטיס מסירה state/URL אך הכרטיס נשאר מוצג עם תוכן ישן.','Click replay + computed display/opacity','plugins/nadlan-config/assets/showroom-engine/engine.js:4106-4140'],
  ['LIVE-005','red','ניווט','קישורי היכולת העליונים href=# אינם מביאים למודל, בחירת דירה או מראה מהחלון.','Click replay 390','public inline renderer'],
  ['LIVE-006','red','ניווט','כפתור בניין ב-progress/section nav נלכד בידי ווידג׳ט הנגישות החופף.','Hit testing 390','theme/project sticky navigation'],
  ['LIVE-007','red','ניווט','CTA מעניין אותי אינו מביא לטופס ההתעניינות.','Click replay 390','project CTA wiring'],
  ['LIVE-008','red','מתקנים','אין facilities/amenities בחוזה, ב-DOM או בחוויית הבחירה.','Payload + DOM + admin audit','plugins/nadlan-config/inc/facility-chips.php:75-90'],
  ['LIVE-009','red','סיור פנים','ארבע סצנות panorama קיימות ב-data אך הממשק חושף רק את הראשונה, ללא קישורי מעבר.','Pannellum runtime + DOM','plugins/nadlan-config/assets/showroom-engine/engine.js:1069-1090'],
  ['LIVE-010','red','סיור דירה','מסלול aurelia_tour הוא background-position על תמונה אחת; אינו סיור 360/POV.','Live route source + click replay','live-only route; no repository match'],
  ['LIVE-011','red','סטודיו','התכנון אינו משתמש בגאומטריית התוכנית האמיתית, חלונות, דלתות, אזורים רטובים או קירות.','Studio DOM + source audit','plugins/nadlan-config/assets/showroom-engine/studio.js'],
  ['LIVE-012','red','סטודיו','Auto arrange הציב רוב פריטי הדוגמה מחוץ לגבולות התוכנית הסינתטית.','Studio click replay 390','plugins/nadlan-config/assets/showroom-engine/studio.js'],
  ['LIVE-013','red','BOM','אין SKU, כמויות, מחיר, BOM מוצג או snapshot שרת לתכנון.','DOM + source + endpoint schema','plugins/nadlan-config/inc/rfp.php:105-117'],
  ['LIVE-014','red','RFP','סיכום הסטודיו נמצא בהודעת lead בלבד ונשמט מ-POST של RFP.','Static code trace','plugins/nadlan-config/assets/showroom-engine/buyflow.js:240-264'],
  ['LIVE-015','red','ועידה','כפתור וידאו פותח lead/WhatsApp; אין ועידת וידאו, room או media API.','Static code + public source','plugins/nadlan-config/assets/showroom-engine/studio.js:311-317'],
  ['LIVE-016','orange','מפה ואלומה','קוד Mapbox והאלומה אמיתי ועובד, אך 0/320 יחידות מכילות azimuth מדויק; הכיוון נגזר משמונה תוויות.','Admin contract + code trace','plugins/nadlan-config/assets/showroom-engine/engine.js:1315-1357'],
  ['LIVE-017','orange','מפה ואלומה','מפת Mapbox אינה מאותחלת עד אינטראקציה עם מסנן מפה; לפני כן אזור המפה ריק.','Click replay + DOM','plugins/nadlan-config/inc/project-experience.php:447-535'],
  ['LIVE-018','red','מובייל','במת המדיה ברוחב כ-498px בתוך viewport 390px וחתוכה בכ-133px.','Bounding boxes 390','showroom responsive CSS'],
  ['LIVE-019','red','מובייל','בקרי Pannellum נמצאים מחוץ למסך וחלקם 26×26 ללא שם נגיש.','Bounding boxes + accessibility tree','Pannellum runtime CSS'],
  ['LIVE-020','red','מובייל','הכרטיס מכסה כ-62% מגובה המודל ויש לו גלילה פנימית ארוכה; הבניין אינו נשאר גלוי.','Bounding boxes 390/400','showroom panel CSS'],
  ['LIVE-021','red','מובייל','ווידג׳טים קבועים של header, project nav, accessibility, lead ו-WhatsApp נערמים ומסתירים פעולות.','Fixed/sticky inventory + screenshots','theme + project CSS'],
  ['LIVE-022','red','מובייל','קישורי ניווט גלובלי יוצאים שמאלה מה-viewport.','Bounding boxes 390','theme header'],
  ['LIVE-023','red','מובייל','תאריכי תיאום פגישה מאוחרים יוצאים מחוץ ל-viewport.','Bounding boxes 390','scheduler CSS'],
  ['LIVE-024','yellow','מלאי','320 יחידות קיימות, אך 60 כרטיסים מרונדרים כברירת מחדל והמקטע ארוך מאוד.','DOM count + section height','plugins/nadlan-config/assets/showroom-engine/engine.js'],
  ['LIVE-025','orange','מלאי','WordPress שומר 302 available ו-18 reserved, אך availability הציבורי אינו עקבי.','Admin JSON vs public payload','plugins/nadlan-config/inc/showroom-engine.php:155-260'],
  ['LIVE-026','orange','תוכניות','לכל 320 היחידות plan, אך יש רק חמש תמונות תוכנית ייחודיות.','Admin JSON aggregate','project_3d_units'],
  ['LIVE-027','red','נוף','0/320 יחידות מכילות asset למראה מהחלון.','Admin JSON aggregate','project_3d_units'],
  ['LIVE-028','red','פנים','0/320 יחידות מכילות interior_url.','Admin JSON aggregate','project_3d_units'],
  ['LIVE-029','red','חזית','ה-UI מציג לקונה טקסט פיתוח על חזית חסרה וחומר עתידי.','Public buyer copy','project facade renderer'],
  ['LIVE-030','orange','מודל','modelType באדמין הוא procedural למרות שקישור GLB קיים.','Admin field audit','project_3d_model_type'],
  ['LIVE-031','orange','מודל','אין USDZ, project video, project tour או Cesium URL בשדות הפרויקט.','Admin field audit','nadlan-p3d metabox'],
  ['LIVE-032','red','אדמין','תיבת המתכון מציגה 0 נורות בפוסט החי בגלל hard-scope לאב-טיפוס אחר.','Admin DOM','prototype plugin scope'],
  ['LIVE-033','red','אדמין','תיבת BOM מציגה 0 מערכות בפוסט החי בגלל hard-scope לאב-טיפוס אחר.','Admin DOM','prototype plugin scope'],
  ['LIVE-034','red','WordPress','תוסף האב-טיפוס קשיח ל-post 7304 ול-slug aurelia-sde-dov, בעוד החי הוא 7514/aurelia.','Repository vs admin','handoff prototype PHP'],
  ['LIVE-035','red','WordPress','חבילת WordPress אינה כוללת assets או importer; אינה פרויקט מלא להתקנה.','ZIP inventory','handoff WordPress package'],
  ['LIVE-036','red','WordPress','project_facilities משמש CSV ב-core אך adapter מנסה JSON decode; התוצאה מערך ריק.','Static code trace','plugins/nadlan-config/inc/facility-chips.php'],
  ['LIVE-037','red','WordPress','adapter נוסף יוצר מערכת בחירה שנייה ואינו מפעיל את ה-semantic mesh adapter שכבר נכתב.','Static code trace','handoff unit-selection-adapter.js'],
  ['LIVE-038','red','WordPress','adapter משתמש unit_id והמנוע החי משתמש unit; ניתן ליצור שתי בחירות שונות.','Static code trace','handoff adapter + core engine'],
  ['LIVE-039','red','Source','adapter inline חי של 8,104 תווים אינו קיים בריפו ולכן אינו ניתן לשחזור או review.','Source/repo fingerprint diff','live inline nadlan-engine-core-js-after'],
  ['LIVE-040','orange','Source','plugin health חי 1.72.220 מול repo 1.72.206.','Version fingerprint','plugin health vs repository'],
  ['LIVE-041','orange','SEO','hreflang כולל רק he ו-x-default למרות שה-runtime מצהיר חמש שפות.','View Source','public head'],
  ['LIVE-042','orange','SEO','שני BreadcrumbList ושני FAQPage שאינם זהים.','JSON-LD parse','public source'],
  ['LIVE-043','red','SEO','meta/FAQ מבטיחים מתקנים שאינם קיימים בחוויה.','Source vs feature contract','Yoast meta + JSON-LD'],
  ['LIVE-044','yellow','SEO','favicon קיים, תקין ומחזיר 200; היעדר SERP אינו מוכח ככשל קוד.','Source + HTTP/MIME','public head icons'],
  ['LIVE-045','orange','Security','נמצאה היעדרות של שישה headers רוחביים בתגובה שנבדקה.','HTTP response headers','server configuration'],
  ['LIVE-046','red','נגישות','בקרי close/tabs/actions רבים קטנים מיעד המוצר 44×44.','Bounding boxes','showroom + studio CSS'],
  ['LIVE-047','red','נגישות','פריטי סטודיו הם div ללא role/tabindex/aria.','DOM audit','studio.js'],
  ['LIVE-048','red','תוכן','תוכן הפוסט באדמין 1,408 תווים בלבד, רחוק ממאמר הפרויקט המלא שהוגדר.','Admin field length','post_content'],
  ['LIVE-049','orange','SEO','Yoast title תקין ב-source אך DOM runtime נצפה עם title אחר; יש לבדוק מי כותב document.title.','Source vs rendered DOM','runtime title writer'],
  ['LIVE-050','yellow','מפה ואלומה','בחירת inventory כן החליפה unit, URL, active card ומרקר כיוון—זה הקוד הקאנוני שיש לשמר.','Positive click proof','engine.js:1315-1357,4106-4140'],
  ['LIVE-051','red','Cache/runtime','engine.js מוגש לשנה עם אותו ver=1.72.220 ללא fingerprint בשם; דפדפנים יכולים להריץ JS ישן מול payload/CSS חדשים.','Response cache headers + source/runtime comparison','asset versioning and cache policy'],
  ['LIVE-052','red','Cache/runtime','באותו סשן payload מכבה selected-unit surface, אך DOM נבנה במסלול החדש בלי ה-CSS שלו—split-brain גרסאות, לא רק תקלה עיצובית.','Payload flags + DOM class + missing CSS rules','engine.js:218-232,2162-2285; showroom-engine.php:493-509'],
  ['LIVE-053','red','SEO','engine.js דורס document.title התקין מהשרת בכל render ומחליף אותו בכותרת חלשה יותר.','Exact source trace + rendered DOM','plugins/nadlan-config/assets/showroom-engine/engine.js:218-232'],
  ['LIVE-054','orange','RFP','ה-summary הגלוי אינו מציג RFP; חיבור הסטודיו תלוי בכפתור legacy מוסתר שנשאר ב-DOM במקום API/event ישיר.','DOM + source trace + click proof','studio.js:310; engine.js:482,2260-2285'],
  ['LIVE-055','red','סיור דירה','ה-tour בתוך dialog במובייל נמדד בכ-303×153px—קטן מדי למסע POV או החלטה.','Browser bounding box','tour dialog CSS'],
  ['LIVE-056','yellow','Reliability','נצפתה תגובת 502 חולפת בפתיחת לשונית חדשה ואזהרת rAF timed out in updateSource; reload הצליח.','Network/console observation','server/runtime monitoring']
].map(([id,status,domain,actual,evidence,codeRef]) => ({ id, status, domain, actual, evidence, codeRef, nonBlocking: true }));

const codeRefMap = {
  sourceSeo: ['public View Source snapshot', 'plugins/nadlan-config/inc/showroom-engine.php:155-260'],
  navigation: ['plugins/nadlan-config/assets/showroom-engine/engine.js:370-560', 'theme project navigation'],
  mobile: ['plugins/nadlan-config/assets/showroom-engine/showroom.css', 'plugins/nadlan-config/assets/showroom-engine/mv-ux.js'],
  selection: ['plugins/nadlan-config/assets/showroom-engine/engine.js:171-197', 'plugins/nadlan-config/assets/showroom-engine/engine.js:370-395', 'plugins/nadlan-config/assets/showroom-engine/engine.js:4106-4140'],
  map: ['plugins/nadlan-config/assets/showroom-engine/engine.js:1267-1357', 'plugins/nadlan-config/inc/project-experience.php:447-535'],
  tour: ['plugins/nadlan-config/assets/showroom-engine/engine.js:953-1090'],
  facilities: ['plugins/nadlan-config/inc/facility-chips.php:75-90', 'plugins/nadlan-config/inc/showroom-engine.php:804-817', '03-DATA/aurelia-facilities.json'],
  studio: ['plugins/nadlan-config/assets/showroom-engine/studio.js', 'plugins/nadlan-config/assets/showroom-engine/buyflow.js:240-264', 'plugins/nadlan-config/inc/rfp.php:105-117'],
  conference: ['plugins/nadlan-config/assets/showroom-engine/engine.js:684-733', 'plugins/nadlan-config/assets/showroom-engine/studio.js:311-317'],
  wordpress: ['plugins/nadlan-config/inc/showroom-engine.php:155-260', 'handoff prototype plugin'],
  content: ['post_content', '_yoast_wpseo_title', '_yoast_wpseo_metadesc'],
  performance: ['public network/runtime evidence', 'showroom asset loader']
};

const domains = [];
const addCriteria = (prefix, domain, area, criteria, method, expectedPrefix = '') => {
  criteria.forEach((criterion, index) => domains.push({
    id: `${prefix}-${String(index + 1).padStart(3, '0')}`,
    domain, area, title: criterion,
    expected: expectedPrefix ? `${expectedPrefix}: ${criterion}` : criterion,
    method,
    evidenceRequired: ['public URL or admin post ID', 'viewport/language/network profile', 'observed value or click outcome', 'timestamp', 'runtime/source hash'],
    statusModel: 'red/orange/yellow/green; non-blocking', nonBlocking: true,
    codeReferences: codeRefMap[area] || [],
    viewports: ['320x720','360x800','390x844','430x932','768x1024','1440x1000'],
    languages: ['he','en','fr','ru','ar']
  }));
};

addCriteria('V2-SEO','Source, SERP and semantic contract','sourceSeo',[
  'Raw public server HTML is captured, hashed and diffed before DOM scripts run','Source title equals the approved SEO title','Rendered document.title equals Source title','One canonical exists and points to the owning project URL','Query parameters do not create competing canonical targets','One H1 exists and matches project intent','Breadcrumb labels and URLs form one consistent hierarchy','Exactly one BreadcrumbList graph represents the visible breadcrumb','FAQ schema is emitted once and mirrors visible questions','ApartmentComplex identity matches visible project name and address','ApartmentComplex includes a representative image','ApartmentComplex amenities mirror facilities data','Offers are omitted unless an approved feed exists','Robots is index/follow for the owning page','Five language siblings exist before hreflang is emitted','hreflang URLs return 200 and self-reference','x-default has an intentional target','Open Graph title matches approved title','Open Graph image is a valid 1.91:1 share asset','Twitter card image resolves with correct MIME','favicon href resolves 200 with supported MIME','favicon is square and at least 48x48 or a valid SVG','apple-touch icon resolves 200','No duplicate icon declarations disagree','Meta description describes only working buyer capabilities','Meta description contains the decision value, not development language','No placeholder/waiting/developer copy appears in Source','No unrelated project name appears in Source','No unredacted private token is stored in public snapshot storage','Public asset script versions are captured','Inline adapter hash is captured','Live-only code without repository owner raises orange/red','Plugin health version matches repository release','Structured data parses without JSON error','Source snapshot retention is private or redacted','SERP favicon status is evidenced from SERP/GSC, not inferred from DOM'
],'source+HTTP+schema parse');

addCriteria('V2-NAV','Page order, progress and navigation','navigation',[
  'Breadcrumbs precede project identity','Opening paragraph appears before the first disclaimer','Progress bar appears before the decision cockpit','Every progress item points to an existing unique anchor','Every progress click moves the intended section below sticky chrome','Active progress state follows scroll position','Progress state can be operated by keyboard','Progress labels remain legible at 320px','Hero primary CTA opens the selection cockpit','Hero secondary CTA opens project materials or meeting action','Top feature cards use real anchors or actions, never href=#','Building nav action cannot be intercepted by accessibility widget','Apartment nav action reveals at least one selection method','Plan nav action preserves selected unit','View nav action preserves selected unit','Facilities nav action opens the facilities cockpit','Environment nav action opens the project map','Article nav action reaches the first editorial heading','Inquiry nav action reaches a working form','Back action restores the previous module and same unit','Sticky project header never overlaps global header','Sticky project header never overlaps progress bar','Fixed bottom conversion bar leaves room for focused controls','Only one sticky conversion bar is active at a time','No global navigation item is positioned outside viewport','Scheduling dates and times remain reachable without page-level horizontal scroll','Deep link with unit returns to the selected unit state','Browser back/forward restores journey state','Page refresh retains unit and language','Skip link reaches the main project content'
],'interaction+DOM+hit-test');

addCriteria('V2-MOB','Mobile cockpit geometry and interaction','mobile',[
  'No page-level horizontal overflow at 320px','No page-level horizontal overflow at 390px','The building remains visible when the unit card opens','The unit card uses a compact bottom sheet at 320px','The unit card uses a compact bottom sheet at 390px','The bottom sheet has one internal scroll region at most','Closing the sheet removes it visually and from pointer hit-testing','Closing the sheet restores focus to its trigger','Model center does not shift when the sheet opens','Model orbit remains usable above the sheet','Model hotspots are not covered by fixed conversion CTAs','Accessibility widget has a reserved non-overlapping slot','Pannellum canvas fits the viewport width','Pannellum controls remain inside the viewport','Mapbox canvas fits the viewport width','Map controls remain inside the viewport','Studio toolbar wraps or scrolls within its own container','Studio close button remains visible','All primary controls meet the product target of 44x44 CSS px','Every undersized map pin has an equivalent list control','Text remains readable at 200 percent zoom','Non-map content reflows at 320 CSS px','Focused elements are not obscured by sticky layers','Safe-area insets are applied to bottom actions','Landscape orientation preserves primary actions','Touch scroll does not accidentally orbit the model','Orbit gesture does not trap vertical page scrolling','One tap activates a visible response within 200ms when loaded','Loading indicator disappears when the module becomes usable','Error recovery is a buyer action, not developer copy','Virtual keyboard does not hide inquiry submit controls','Long Hebrew and Arabic labels wrap without clipping','LTR languages reverse layout without moving spatial directions','Back/close controls stay in a consistent corner by direction','No nested scroll reset loses the current unit'
],'browser click replay+bounding boxes');

addCriteria('V2-SEL','3D model and unit selection','selection',[
  'Poster is visually aligned with the loaded model','Model has an explicit loaded state','Model has an explicit error state','GLB URL returns 200 with a model MIME type','GLB semantic version is recorded','Camera opening orbit is defined per project','Camera orbit limits prevent viewing the model underside','Reset camera returns to project opening orbit','Auto-rotate pauses on user interaction','Model can be operated by pointer and touch','Every selectable unit has one canonical unit_id','Every selectable unit maps to a semantic mesh or authored anchor','Semantic mesh nodes encode unit_id in name or extras','Authored anchors use model coordinates, not CSS percentages','Every anchor includes a surface normal','Every anchor lies within the model bounding box','Every anchor projects within the model host','Every anchor follows the model on every camera frame','Hotspot and mesh click emit the same unit-selected event','Inventory card click emits the same unit-selected event','Floor slicer click emits the same unit-selected event','Facade click emits the same unit-selected event','Deep link emits the same unit-selected event','Only one selection controller owns active unit state','No live-only overlay hides the canonical selection layer','Hidden hotspots are removed from tab order','Visible hotspots have accessible unit labels','Hotspots expose a 44px hit area without changing their anchor point','Selected hotspot remains visually distinct','Sold units cannot be selected','Reserved units have one consistent state across model and inventory','Filter counts exclude unavailable units consistently','Room filter returns correct units','Floor filter returns correct units','Direction filter returns correct units','Estimated-price filter returns correct units','Multiple filters combine predictably','Clearing filters restores the previous selected unit when still valid','Zero-result state suggests a useful next action','Inventory is virtualized or paginated on mobile','Inventory does not render a multi-thousand-pixel wall by default','Floor bands expose all floors with matches','Unit card shows floor','Unit card shows rooms','Unit card shows interior area','Unit card shows balcony area','Unit card shows direction/view','Unit card shows estimated price','Unit card shows inventory status','Unit card action asks for that exact unit','Selection updates URL with the canonical unit parameter','Browser back restores prior unit','Closing card does not erase selection unless user explicitly clears it','Unit state survives movement to plan, map, view, tour and studio','Analytics records selection origin and unit_id','Click proof is required before the selection light can be green'
],'model contract+click replay+ray/anchor validation');

addCriteria('V2-UNIT','Unit card, plan, map, beam and view','map',[
  'Unit card opens within the current viewport after inventory selection','Unit card internal scroll resets only when selected unit changes','Unit card close leaves no stale panel','Plan tab is reachable at 320px','View tab is reachable at 320px','Interior tab is reachable at 320px','Studio action is reachable at 320px','Inquiry action is reachable at 320px','Plan URL resolves 200 with image or SVG MIME','Plan belongs to the selected unit type','Plan shows north arrow','Plan labels room functions','Plan includes readable dimensions','Plan distinguishes interior and balcony areas','Plan supports pinch or controlled zoom','Plan has a text equivalent','Plan download uses the same unit_id','Map is initialized before the user reaches the view section','Mapbox instance is adopted rather than duplicated','Map remains directly below the building decision stage','Project point equals the admin latitude/longitude','Unit selection updates the existing GeoJSON/marker state','View beam originates at the project point','View beam uses authored azimuth_deg when available','Fallback direction mapping is visibly flagged only in admin','View beam half-angle is defined','View beam radius is defined','Map bearing and beam direction agree','Unit direction label and beam direction agree','Changing unit updates beam without rebuilding the map','Changing unit updates camera without losing POI filters','Map POI filters have accurate result counts','POI selection shows name, category, distance and route','Map has a non-canvas list equivalent','Window view uses selected unit_id','Window view camera includes bearing','Window view camera includes elevation from floor','Window view camera includes pitch and FOV','Window view distinguishes direction and height tier','Window view is not a generic still presented as interactive','Window view can open full-screen','Return from window view restores same unit','Share link restores unit and view state','Unit plan, map, beam and view are one atomic evidence bundle','No map/beam code is replaced by a CSS illustration','Positive live code proof cites showViewCone/easeMapToUnitView','Click proof is captured at 320, 390 and 1440','Every state transition has loading, ready and error states','No buyer-facing copy describes implementation work','Estimated prices remain natural buyer copy','Official-price mode is opt-in per project field'
],'interaction+data contract+visual evidence');

addCriteria('V2-TOUR','Interior tour and project media','tour',[
  'Project tour opens inside the decision journey','Per-unit tour preserves unit_id','Tour renderer is spherical/WebGL, not background-position','Panorama uses a 2:1 equirectangular source','Panorama horizon is level','Panorama left/right seam is acceptable','Tour includes a room graph','Every scene has a unique scene_id','Scene hotspots navigate to valid scene_id values','Scene selector exposes every included room','Plan minimap shows current scene','Plan minimap is synchronized with scene changes','Tour supports touch drag','Tour has a non-drag control alternative','Tour controls meet touch target size','Tour controls have accessible names','Tour supports full-screen','Tour exits to the same unit card','Apartment type determines the correct tour set','Bedroom, living, balcony and kitchen are separately inspectable','Facility scenes are not mixed into the apartment room graph','Project sample-home tour is labeled separately from unit type tour','Panorama poster loads before the viewer','Panorama failures retain useful project navigation','No default generic scene is silently reused across every unit','Scene load and scene change events are measured','Tour click proof is required before green'
],'asset inspection+click replay+scene graph validation');

const facilityCriteria = [
  'has one facility_id used by card, model, plan, panorama and analytics','has a semantic GLB node or authored facility polygon','has a plan/masterplan feature and level','opens from a model or masterplan hotspot','opens from an equivalent accessible list item','opens a real panorama with a 2:1 source','has scene hotspots for functional zones/equipment','shows area and capacity as estimated prototype values','shows equipment/features in buyer language','shows accessibility and route from lobby','supports save/favorite and share','supports ask-a-representative with facility context','returns to the same project/unit context','has a 200/MIME/hash asset proof','does not use another facility image as a substitute','has no waiting/developer copy in public UI'
];
facilities.forEach((facility, fIndex) => facilityCriteria.forEach((criterion, index) => domains.push({
  id: `V2-FAC-${String(fIndex + 1).padStart(2,'0')}-${String(index + 1).padStart(2,'0')}`,
  domain: 'Facilities and amenities', area: 'facilities', facilityId: facility.id,
  title: `${facility.nameHe}: ${criterion}`, expected: criterion,
  method: 'facility contract+asset+DOM+interaction',
  evidenceRequired: ['facility_id','model/plan anchor proof','asset hash and MIME','click replay','viewport/language','timestamp'],
  statusModel: 'red/orange/yellow/green; non-blocking', nonBlocking: true,
  codeReferences: codeRefMap.facilities,
  viewports: ['320x720','390x844','768x1024','1440x1000'], languages: ['he','en','fr','ru','ar']
})));

addCriteria('V2-STU','Apartment studio, engineering BOM and quotation','studio',[
  'Studio opens with the selected unit_id','Studio loads the selected unit plan geometry','Studio plan geometry includes exterior walls','Studio plan geometry includes internal walls','Studio plan geometry includes doors and swing arcs','Studio plan geometry includes windows','Studio plan geometry includes wet zones','Studio plan geometry includes structural no-change zones','Studio scale is calibrated in meters','Every placed item has an accessible interactive role','Every placed item can be selected by keyboard','Drag has a keyboard/single-pointer alternative','Collision rules prevent overlapping fixed geometry','Door clearance rules are enforced','Wheelchair turning-radius object uses true scale','Accessible door option updates the correct opening','Plumbing options are limited to compatible wet zones','Electrical additions use defined wall/ceiling anchors','Every option has SKU','Every option has unit of measure','Every option has quantity','Every option has estimated price impact','Every option records dependency rules','Undo and redo preserve deterministic state','Auto-arrange keeps every item within legal bounds','Auto-arrange does not block doors or circulation','Configuration has a stable configuration_id','Configuration is saved server-side','Configuration can be restored by link','Configuration produces a top-view image','Configuration produces a perspective image','Configuration produces a room-by-room BOM','BOM groups base specification and buyer changes','BOM includes quantities and option codes','BOM includes estimated price totals','BOM records recipe and catalog version','RFP stores the full studio snapshot','RFP PDF includes unit, plan, options and totals','Lead payload includes configuration_id','Representative opens the same configuration','Studio closes back to the same unit','Studio click proof is required before green'
],'data contract+geometry rules+click replay+RFP persistence');

addCriteria('V2-CONV','Lead, RFP, meeting, co-tour and analytics','conference',[
  'Inquiry CTA preserves project_id and unit_id','Plan request preserves unit_id','Price request preserves unit_id','Facility inquiry preserves facility_id','Studio inquiry preserves configuration_id','Form submit is never tested against a live person without confirmation','Consent state is explicit and recorded','Success state identifies what was requested','Failure state offers retry without losing context','RFP endpoint stores an immutable request snapshot','RFP document is private by default','Scheduler date grid remains reachable at 320px','Scheduler time choice remains reachable at 320px','Meeting booking stores unit and configuration context','Video action opens a real meeting room','Camera/microphone permission is requested only after a user click','Meeting participants share selected unit state','Meeting participants share plan/view/facility state','Late joiner receives current state snapshot','Co-tour room expiry and roles are defined','Co-tour state updates are versioned','WhatsApp is a channel option, not the video engine','Analytics records module open/close','Analytics records unit-selected source','Analytics records plan/view/tour/facility/studio use','Analytics records errors and load times','No demo submission reaches production leads during QA'
],'endpoint trace+click replay+analytics evidence');

addCriteria('V2-WP','WordPress ownership, fields, migrations and lights','wordpress',[
  'Checklist attaches by capability or post type, not hard-coded post ID','BOM attaches by capability or post type, not hard-coded slug','Live post 7514 renders the checklist lights','Live post 7514 renders BOM systems','Checklist remains non-blocking for save and publish','Every light links to its owning field or code component','Every light stores evidence and timestamp','Every light stores recipe version and runtime hash','Green is impossible without required evidence type','Interactive green requires browser click proof','Source green requires public server HTML proof','Asset green requires URL, MIME, dimensions and hash','Manual evidence records owner and date','project_facilities CSV remains backward compatible for chips','Detailed facilities use a separate versioned JSON field','Facilities renderer consumes the detailed field','project_3d_units has one documented schema','Unit status maps to one enum','Canonical query key is unit','unit_id remains a temporary read-only alias during migration','Drawings map resolves plan_id to unit.plan','Semantic GLB version is stored','Every unit has authored azimuth or an explicit admin light','Every unit can link a view camera or tier asset','Interior tour graph is a separate versioned field','Project media manifest uses WordPress attachment IDs','Importer resolves relative assets to attachment URLs','Importer is idempotent','Importer has dry-run output','Importer creates a backup/export before mutation','Migration never runs on page render','Live-only inline code is moved into version control','Plugin version and asset hashes are exposed in admin','Source fingerprint storage is private/redacted','Five-language parity has an automated report','SEO title has one owner','Document title is not rewritten to a conflicting value','Facility/SEO claims derive from the same feature contract','Cesium eligibility is data-driven, not slug allowlist','Admin saves do not discard unknown future schema keys','Package contains assets, importer, contract and rollback instructions','WordPress package verification runs before ZIP creation'
],'admin DOM+repository trace+schema validation');

addCriteria('V2-CONTENT','Content, intent and buyer evidence','content',[
  'Project page owns one defined keyword intent','City and neighborhood pages own separate intents','SEO title begins with the strongest project identity','H1 uses the natural bilingual project name','Opening paragraph answers who, what, where, status and estimated price','Opening paragraph describes working selection capabilities','Decision cockpit precedes the long article','Facilities section precedes generic editorial depth','Article contains approximately 5,000 useful words when the project brief requires it','Article headings map to buyer questions','Developer entity has a dedicated linked profile','Architect entity has a dedicated linked profile','Engineer and contractor entities are linked where available','Facilities are described with operational detail','Building systems are derived from engineering BOM','Estimated prices are labeled naturally in buyer copy','Official-price mode is used only when explicitly set','Transaction and street data retain provenance internally','Neighborhood content includes transport, education, services and public realm','Environment tools support the claims made in prose','FAQ answers are visible before schema emission','No paragraph repeats the focus keyword mechanically','Five language versions preserve facts and actions','RTL/LTR does not reverse geographic directions','Public copy never says waiting for developer materials','Public copy never describes QA or implementation','Every capability named in copy has a working action','Disclaimers remain in the designated global/legal location','Article tables remain readable at 320px','Internal links do not create project/area cannibalization','Content update records source date and editor'
],'content map+source+rendered DOM+manual editorial evidence');

addCriteria('V2-PERF','Accessibility, reliability and performance','performance',[
  'LCP field target is at most 2.5 seconds at p75','INP field target is at most 200ms at p75','CLS field target is at most 0.1 at p75','Poster is the LCP candidate before GLB','GLB is lazy-loaded by intent','Mapbox is loaded by proximity or intent','Pannellum is loaded only when a tour opens','Studio bundle is loaded only when studio opens','Cesium is loaded only when environment tour opens','Images use responsive sizes and modern formats','360 assets use a mobile-appropriate delivery tier','GLB uses mesh/texture compression where compatible','320-unit inventory is virtualized','Only visible hotspots participate in layout and tab order','No duplicate selection overlay is loaded','Module errors are isolated and recoverable','A transient 502 has retry behavior','Console has no uncaught exception during the buyer path','Network failures preserve unit state','Reduced motion is honored','Focus order matches visual order','Canvas tools have text/list equivalents','Color is not the only inventory-status signal','Contrast meets the selected WCAG target','Form errors are announced','Touch actions have single-pointer alternatives','Page content reflows at 320 CSS px','Fixed content does not obscure focused controls','Performance evidence records device/network/version','No light is green from lab-only synthetic data'
],'browser performance+accessibility tree+network replay');

const previousChecklistPath = path.join(previousRoot, '01-DEMO-LAB', 'data', 'master-checklist.json');
const previousChecklist = JSON.parse(fs.readFileSync(previousChecklistPath, 'utf8'));
const priorDefinitions = previousChecklist.definitions.map(def => ({ ...def, sourceRecipe: '2026-08-25-v1' }));
const atomicChecklist = {
  schemaVersion: '2.0.0', project: 'aurelia', mode: 'non-blocking-lights', generatedAt: '2026-08-26',
  purpose: 'Atomic, evidence-carrying recipe for the public buyer page and the WordPress editor. It reports red/orange/yellow/green but never blocks save or publish.',
  statusMeaning: previousChecklist.statusModel,
  counts: { priorDefinitions: priorDefinitions.length, newAtomicDefinitions: domains.length, totalDefinitions: priorDefinitions.length + domains.length, liveFindings: liveFindings.length, facilities: facilities.length },
  profiles: previousChecklist.profiles,
  evidencePolicy: {
    greenRequires: { source: 'public server HTML hash', interaction: 'successful browser click replay at required viewport', asset: 'file/URL, MIME, dimensions and SHA-256', data: 'field path plus observed value', manual: 'named owner, timestamp and attached evidence' },
    greenForbiddenWhen: ['Only a DOM node exists', 'Only a field is populated', 'Only a CSS mock exists', 'Only a lab result exists for a live claim', 'The action is covered or unreachable'],
    nonBlocking: true
  },
  liveFindings,
  definitions: [...priorDefinitions, ...domains]
};

const clickMatrixRows = [
  ['Viewport','Entry','Action','Expected','Observed','Status','Evidence'],
  ['390/400','Hero','Tap לבחירת דירה','Chooser visible below sticky chrome','Model/chooser reached, but fixed bars cover lower model','red','browser click + bounding boxes'],
  ['390','Top capabilities','Tap מודל','Scroll to model','No scroll; href=#','red','scrollY before/after'],
  ['390','Top capabilities','Tap בחירת דירה','Scroll to inventory/chooser','No scroll; href=#','red','scrollY before/after'],
  ['390','Top capabilities','Tap מראה מהחלון','Open/preserve selected unit view','No action','red','click replay'],
  ['390','Section nav','Tap בניין','Reach building stage','Accessibility widget captures hit','red','elementFromPoint'],
  ['390','Inventory','Tap unit card','Open same unit card in viewport','unit/URL updates; panel remains far above viewport','red','URL + panel rect'],
  ['390','Unit card','Tap close','Panel hidden and focus restored','URL selection clears; stale panel remains visible','red','computed display/opacity'],
  ['390','Unit card','Tap plan','Plan for same unit','Reachability interfered with by overlapping layers','red','hit test'],
  ['390','Unit card','Tap map/view','Map and real beam update','Underlying wiring updates unit/direction marker, but action is difficult to reach','orange','positive code/click proof + reachability failure'],
  ['390','Media','Open 360','Spherical viewer with scene chooser','Pannellum canvas opens; only first scene exposed, controls clipped','red','canvas + controls rect'],
  ['390','Per-unit tour','Open tour URL','POV room graph','Flat background pan; three labels on one image','red','route source + click'],
  ['390','Studio','Launch studio','Real plan geometry and BOM','Synthetic rectangle; no geometry/BOM; auto-arrange overflow','red','studio DOM/click'],
  ['390','Inquiry','Tap מעניין אותי','Form in viewport with unit context','No scroll to form','red','form rect'],
  ['320','Showroom','Inspect fixed layers','Building remains visible and selectable','Lead/WhatsApp bars cover lower model and hotspots','red','aurelia-live-320-showroom.png'],
  ['1440','Source/SEO','Compare source and runtime title','One title owner','Source/Yoast and observed runtime title disagree','orange','source vs DOM']
];

const extracts = [
  ['payload-builder','plugins/nadlan-config/inc/showroom-engine.php',155,260],
  ['runtime-title-writer','plugins/nadlan-config/assets/showroom-engine/engine.js',218,232],
  ['unit-position','plugins/nadlan-config/assets/showroom-engine/engine.js',171,197],
  ['theater-and-hotspots','plugins/nadlan-config/assets/showroom-engine/engine.js',370,395],
  ['unit-tabs','plugins/nadlan-config/assets/showroom-engine/engine.js',520,560],
  ['interior-tour','plugins/nadlan-config/assets/showroom-engine/engine.js',953,1090],
  ['map-adoption-and-sync','plugins/nadlan-config/assets/showroom-engine/engine.js',1267,1296],
  ['view-cone-and-map-ease','plugins/nadlan-config/assets/showroom-engine/engine.js',1315,1357],
  ['legacy-unit-selection','plugins/nadlan-config/assets/showroom-engine/engine.js',4106,4140],
  ['selected-unit-summary','plugins/nadlan-config/assets/showroom-engine/engine.js',2162,2285],
  ['project-map','plugins/nadlan-config/inc/project-experience.php',447,535],
  ['rfp-schema','plugins/nadlan-config/inc/rfp.php',105,117],
  ['co-tour','plugins/nadlan-config/assets/showroom-engine/engine.js',684,733]
].map(([id, file, start, end]) => {
  const abs = path.join(repoRoot, file);
  const lines = fs.readFileSync(abs, 'utf8').split(/\r?\n/);
  const excerpt = lines.slice(start - 1, end).join('\n');
  return { id, file, startLine: start, endLine: end, fileSha256: sha256(fs.readFileSync(abs)), excerptSha256: sha256(excerpt), excerpt };
});

for (const facility of facilities) {
  const abs = path.join(packageRoot, facility.asset);
  const buf = fs.readFileSync(abs);
  facility.assetSha256 = sha256(buf);
  facility.assetBytes = buf.length;
}

const assetManifest = {
  schemaVersion: '1.0.0', generatedAt: '2026-08-26', usage: 'Aurelia prototype/remediation lab and later WordPress media import',
  publicCopyRule: 'Generated facilities are presented to buyers as the project experience. Provenance and approval state remain internal.',
  panoramaContract: { projection: 'equirectangular', expectedAspectRatio: 2, intendedRenderer: 'Pannellum 2.5.6 via the existing engine loader', textAllowed: false, peopleAllowed: false },
  assets: facilities.map(f => ({ facilityId: f.id, path: f.asset, bytes: f.assetBytes, sha256: f.assetSha256 }))
};

writeJson('01-EVIDENCE/public-source-fingerprint.json', sourceFingerprint);
writeJson('01-EVIDENCE/admin-contract-snapshot.json', adminContract);
writeJson('01-EVIDENCE/live-findings.json', liveFindings);
writeText('01-EVIDENCE/mobile-click-matrix.csv', clickMatrixRows.map(row => row.map(csvCell).join(',')).join('\n') + '\n');
writeJson('03-DATA/aurelia-facilities.json', { schemaVersion: '1.0.0', projectId: 'aurelia', facilities });
writeJson('03-DATA/atomic-checklist-v2.json', atomicChecklist);
writeText('03-DATA/atomic-checklist-v2.csv', [
  ['id','domain','area','title','method','nonBlocking','codeReferences'].map(csvCell).join(','),
  ...atomicChecklist.definitions.map(item => [item.id,item.domain,item.area||'',item.title,item.mode||item.method,item.nonBlocking,(item.codeReferences||[]).join(' | ')].map(csvCell).join(','))
].join('\n') + '\n');
writeJson('04-ASSETS/asset-manifest.json', assetManifest);
writeJson('05-CODE/canonical-code-excerpts.json', { schemaVersion: '1.0.0', generatedAt: '2026-08-26', note: 'Exact excerpts from the repository at package build time. Rebuild and diff hashes when code changes.', extracts });
writeJson('05-CODE/code-hash-baseline.json', { generatedAt: '2026-08-26', files: extracts.map(x => ({ id:x.id, file:x.file, startLine:x.startLine, endLine:x.endLine, fileSha256:x.fileSha256, excerptSha256:x.excerptSha256 })) });

const backlog = liveFindings.map((finding, index) => ({
  sequence: index + 1, id: finding.id, priority: finding.status === 'red' ? 'P0/P1' : finding.status === 'orange' ? 'P1/P2' : 'P2',
  domain: finding.domain, problem: finding.actual, evidence: finding.evidence, codeOwner: finding.codeRef,
  acceptance: 'The corresponding atomic checklist item can become green only with the required evidence; WordPress save/publish remains unblocked.'
}));
writeText('08-BACKLOG/remediation-backlog.csv', [
  ['sequence','id','priority','domain','problem','evidence','codeOwner','acceptance'].map(csvCell).join(','),
  ...backlog.map(row => Object.values(row).map(csvCell).join(','))
].join('\n') + '\n');

const downloadsDir = path.join(packageRoot, 'downloads');
const downloadHashes = fs.existsSync(downloadsDir)
  ? fs.readdirSync(downloadsDir).filter(name => name.toLowerCase().endsWith('.zip')).sort().map(name => ({ name, sha256: sha256(fs.readFileSync(path.join(downloadsDir, name))) }))
  : [];
writeText('downloads/SHA256SUMS.txt', downloadHashes.map(item => `${item.sha256}  ${item.name}`).join('\n') + (downloadHashes.length ? '\n' : ''));

const integrityFiles = [];
const walk = dir => {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory() && entry.name !== 'downloads') walk(full);
    else if (entry.isFile() && !['MANIFEST-SHA256.txt', 'package-verification.json'].includes(entry.name)) {
      integrityFiles.push({ path: path.relative(packageRoot, full).replaceAll('\\','/'), sha256: sha256(fs.readFileSync(full)) });
    }
  }
};
walk(packageRoot);
writeText('MANIFEST-SHA256.txt', integrityFiles.sort((a,b)=>a.path.localeCompare(b.path)).map(x => `${x.sha256}  ${x.path}`).join('\n') + '\n');

console.log(JSON.stringify({ packageRoot, facilities: facilities.length, atomicChecks: atomicChecklist.definitions.length, liveFindings: liveFindings.length, excerpts: extracts.length }, null, 2));
