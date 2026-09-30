/*
 * The example apartment (design system v104.2 "KikarHamedinaWorld", P9c of the Kikar Hamedina loop, HAD-375).
 *
 * Opened by the world's "היכנסו לדירה לדוגמה" (world.js, openExampleApt): nothing here, and none of its pictures, loads before
 * that press. An album over the page (a dialog, full screen on a phone): the living room at the time of day the floor view shows
 * (day, sunset, evening), the corner bedroom, the balcony, the 360 of the living room in the fleet's viewer (../tour.js, the
 * same viewer as Rainbow's and DUO's rooms), and the twist strip: the same window on floors 20, 30 and 38. Every picture is an
 * illustration and says so: the chip "דירה לדוגמה" and the line "התוכנית להמחשה, חלוקת הדירות לא פורסמה" are always on screen.
 *
 *   const h = openExample({ url, id, lang, tower, floor, bearing, facing, tod, wa, opener, onTod, onClose });
 *   h.setTod('day' | 'sunset' | 'night'); h.close();
 *
 * url: the manifest (hamedina/tour/examples.json, its files beside it); id: the example (e.g. 'c30w'); floor / facing: what the
 * visitor chose in the world (the pictures say which floor they are from when it differs); tod: the floor view's time of day
 * ('night' shows the evening picture); wa: the world's WhatsApp link (the site's interceptor adds the source line); onTod(k):
 * the album's own time switch tells the world, so the two never disagree.
 *
 * Words: he, en, fr, ru, ar (each written for its reader). No <p>/<h*> inside: the theme's !important rules on those leak in.
 */
let cssDone = false;
function ensureCss() {
  if (cssDone || document.querySelector('link[data-nlex-css]')) { cssDone = true; return; }
  const l = document.createElement('link');
  l.rel = 'stylesheet';
  l.href = new URL('./example.css' + new URL(import.meta.url).search, import.meta.url).href;
  l.setAttribute('data-nlex-css', '');
  document.head.appendChild(l);
  cssDone = true;
}

const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const frNum = (x) => String(x).replace('.', ',');

// a bearing in a sentence: a word in Hebrew and Arabic (the sign beside an RTL word reads backwards, v104.1), else the sign isolated
const DEGW = { he: (n) => `${n} מעלות`, ar: (n) => `${n} درجة` };
const deg = (lang, n) => (DEGW[lang] ? esc(DEGW[lang](n)) : `<bdi dir="ltr">${esc(n)}°</bdi>`);

const WORDS = {
  he: {
    chip: 'דירה לדוגמה',
    label: 'התוכנית להמחשה, חלוקת הדירות לא פורסמה',
    title: (rooms) => `דירה לדוגמה, ${rooms} חדרים`,
    eyebrow: (k, f, dir) => `מגדל ${k} · קומה ${f} · פונה ${dir}`,
    size: (rooms, sqm, src) => `בגודל שפורסם בעסקאות במגדלים: ${rooms} חדרים, ${sqm} מ״ר (${src})`,
    sizeSrc: 'גלובס, 2.5.2025',
    from: (f0, f) => `התמונות מקומה ${f0}; בחרתם קומה ${f}, והנוף ממנה דומה מאוד`,
    todLbl: 'שעות היום', tod: { day: 'יום', sunset: 'שקיעה', evening: 'ערב' },
    tile: { living: (t) => `הסלון · ${t}`, bedroom: 'חדר השינה', balcony: 'המרפסת', pano: 'סיור 360 בסלון' },
    date: '21 בספטמבר',
    lit: 'האורות בחלונות העיר: הדמיה להמחשה',
    cap: {
      living: (t, h) => `הסלון ב${t === 'יום' ? 'יום' : t === 'שקיעה' ? 'שקיעה' : 'ערב'} · 21 בספטמבר, ${h}`,
      bedroom: (h) => `חדר השינה בפינה, חלון מעוגל לצפון-מערב · 21 בספטמבר, ${h}`,
      balcony: (h) => `המרפסת בשקיעה, מבט אל מגדל A · 21 בספטמבר, ${h}`,
      twist: (f, b, h) => `אותו חלון בקומה ${f}, פונה ${b} · 21 בספטמבר, ${h}`,
    },
    go360: 'להסתכל מסביב בסלון',
    wa: 'ייעוץ חינם על דירה כזו',
    gallery: 'תמונות מהדירה',
    twistH: 'אותו חלון בקומות 20, 30 ו-38',
    twistCap: 'כל קומה במגדל מסתובבת 1.25 מעלות ביחס לקומה שמתחתיה, ולכן אותו חלון פונה בכל קומה לכיוון מעט אחר, והנוף זז איתו.',
    twistItem: (f) => `קומה ${f}`,
    notesSum: 'מה בתמונות להמחשה',
    notes: (eye) => [
      'הדירה, החלוקה, הגמרים והריהוט הם הדמיה להמחשה. תוכניות הקומה ותמהיל הדירות לא פורסמו.',
      'הגודל: 4 חדרים ו-140 מ״ר, כמו שלוש העסקאות שפורסמו בקומות 38 ו-39 (גלובס, 2.5.2025). באיזה מגדל נמכרה כל דירה לא פורסם.',
      `הנוף: הבניינים, הגבהים, הרחובות והעצים לפי המידע הפתוח של עיריית תל אביב-יפו, מגובה העיניים בקומה 30 (כ-${eye} מ׳) ובכיוון שהצד הזה פונה אליו. גובה קומה של 4 מ׳ הוא הערכה.`,
      'השמש: מסלול השמש מעל תל אביב ב-21 בספטמבר, בשעה שכתובה בכל תמונה.',
      'הסיבוב של 1.25 מעלות בכל קומה פורסם. כיוונו, עם כיוון השעון או נגדו, לא פורסם; בהדמיה הוא נגד כיוון השעון, כמו בסיור הווירטואלי בכיכר.',
    ],
    renders: 'יש כרגע תמונות לדירה אחת: מגדל C, קומה 30, בצד המערבי.',
    close: 'סגירה', loading: 'טוענים את הדירה', error: 'התמונה לא נטענה. נסו שוב מאוחר יותר.',
    drag: 'גררו כדי להסתכל מסביב',
    panoTitle: (k, f) => `הסלון בשקיעה · מגדל ${k} · קומה ${f}`,
    panoNote: (f, h) => `הסלון מקומה ${f}, 21 בספטמבר, ${h}. הריהוט והגמרים להמחשה.`,
  },
  en: {
    chip: 'Example apartment',
    label: 'The layout is an illustration; the apartment mix has not been published',
    title: (rooms) => `An example ${rooms}-room apartment`,
    eyebrow: (k, f, dir) => `Tower ${k} · floor ${f} · facing ${dir}`,
    size: (rooms, sqm, src) => `The size of the published deals in the towers: ${rooms} rooms, ${sqm} m² (${src})`,
    sizeSrc: 'Globes, 2.5.2025',
    from: (f0, f) => `The pictures are from floor ${f0}; you chose floor ${f}, and its view is very close`,
    todLbl: 'Time of day', tod: { day: 'Day', sunset: 'Sunset', evening: 'Evening' },
    tile: { living: (t) => `Living room · ${t.toLowerCase()}`, bedroom: 'Bedroom', balcony: 'Balcony', pano: '360° living room' },
    date: '21 September',
    lit: 'the city’s lit windows: illustration',
    cap: {
      living: (t, h) => `The living room · ${t.toLowerCase()} · 21 September, ${h}`,
      bedroom: (h) => `The corner bedroom, its curved window to the north-west · 21 September, ${h}`,
      balcony: (h) => `The balcony at sunset, looking at tower A · 21 September, ${h}`,
      twist: (f, b, h) => `The same window on floor ${f}, facing ${b} · 21 September, ${h}`,
    },
    go360: 'Look around the living room',
    wa: 'Free advice on an apartment like this',
    gallery: 'Pictures of the apartment',
    twistH: 'The same window on floors 20, 30 and 38',
    twistCap: 'Every floor of the tower turns 1.25° from the one below, so the same window faces a slightly different way on every floor, and the view turns with it.',
    twistItem: (f) => `Floor ${f}`,
    notesSum: 'What is illustrated',
    notes: (eye) => [
      'The apartment, its layout, finishes and furniture are an illustration. The floor plans and the apartment mix have not been published.',
      'The size: 4 rooms and 140 m², like the three published deals on floors 38 and 39 (Globes, 2.5.2025). Which tower each was in was not published.',
      `The view: buildings, heights, streets and trees from the Tel Aviv-Yafo municipality's open data, from eye height on floor 30 (about ${eye} m) along the way this side faces. A floor height of 4 m is an estimate.`,
      'The sun: its path over Tel Aviv on 21 September, at the time given with each picture.',
      'The turn of 1.25° per floor is published; its direction, clockwise or counter-clockwise, is not. The illustration turns counter-clockwise, like the virtual tour of the square.',
    ],
    renders: 'Pictures exist for one apartment so far: tower C, floor 30, on the west side.',
    close: 'Close', loading: 'Loading the apartment', error: 'The picture did not load. Please try again later.',
    drag: 'Drag to look around',
    panoTitle: (k, f) => `The living room at sunset · tower ${k} · floor ${f}`,
    panoNote: (f, h) => `The living room on floor ${f}, 21 September, ${h}. Furniture and finishes are an illustration.`,
  },
  fr: {
    chip: 'Appartement témoin',
    label: 'Plan à titre d’illustration ; la répartition des appartements n’a pas été publiée',
    title: (rooms) => `Un appartement témoin de ${rooms} pièces`,
    eyebrow: (k, f, dir) => `Tour ${k} · étage ${f} · orientation ${dir}`,
    size: (rooms, sqm, src) => `À la taille des ventes publiées dans les tours : ${rooms} pièces, ${sqm} m² (${src})`,
    sizeSrc: 'Globes, 02/05/2025',
    from: (f0, f) => `Les images sont prises au ${f0}e étage ; vous avez choisi le ${f}e, dont la vue est très proche`,
    todLbl: 'Moment de la journée', tod: { day: 'Jour', sunset: 'Coucher du soleil', evening: 'Soir' },
    tile: { living: (t) => `Séjour · ${t.toLowerCase()}`, bedroom: 'Chambre', balcony: 'Balcon', pano: 'Séjour à 360°' },
    date: '21 septembre',
    lit: 'fenêtres éclairées de la ville : illustration',
    cap: {
      living: (t, h) => `Le séjour · ${t.toLowerCase()} · 21 septembre, ${h.replace(':', ' h ')}`,
      bedroom: (h) => `La chambre d’angle, sa baie arrondie vers le nord-ouest · 21 septembre, ${h.replace(':', ' h ')}`,
      balcony: (h) => `Le balcon au coucher du soleil, face à la tour A · 21 septembre, ${h.replace(':', ' h ')}`,
      twist: (f, b, h) => `La même fenêtre au ${f}e étage, orientée à ${b} · 21 septembre, ${h.replace(':', ' h ')}`,
    },
    go360: 'Regarder tout autour du séjour',
    wa: 'Conseil gratuit sur ce type de bien',
    gallery: 'Images de l’appartement',
    twistH: 'La même fenêtre aux 20e, 30e et 38e étages',
    twistCap: 'Chaque étage de la tour pivote de 1,25° par rapport à celui du dessous : la même fenêtre regarde donc un peu ailleurs à chaque étage, et la vue tourne avec elle.',
    twistItem: (f) => `${f}e étage`,
    notesSum: 'Ce qui est illustré',
    notes: (eye) => [
      'L’appartement, son plan, ses finitions et son mobilier sont une illustration. Les plans d’étage et la répartition des appartements n’ont pas été publiés.',
      'La surface : 4 pièces et 140 m², comme les trois ventes publiées aux 38e et 39e étages (Globes, 02/05/2025). La tour de chacune n’a pas été publiée.',
      `La vue : immeubles, hauteurs, rues et arbres d’après les données ouvertes de la municipalité de Tel Aviv-Jaffa, à hauteur des yeux au 30e étage (environ ${frNum(eye)} m) et dans la direction de cette façade. Une hauteur d’étage de 4 m est une estimation.`,
      'Le soleil : sa course au-dessus de Tel Aviv le 21 septembre, à l’heure indiquée pour chaque image.',
      'La rotation de 1,25° par étage est publiée ; son sens, horaire ou antihoraire, ne l’est pas. L’illustration tourne dans le sens antihoraire, comme la visite virtuelle de la place.',
    ],
    renders: 'Des images existent pour l’instant pour un seul appartement : tour C, 30e étage, façade ouest.',
    close: 'Fermer', loading: 'Chargement de l’appartement', error: 'L’image ne s’est pas chargée. Réessayez plus tard.',
    drag: 'Glissez pour regarder autour',
    panoTitle: (k, f) => `Le séjour au coucher du soleil · tour ${k} · ${f}e étage`,
    panoNote: (f, h) => `Le séjour au ${f}e étage, 21 septembre, ${h.replace(':', ' h ')}. Mobilier et finitions à titre d’illustration.`,
  },
  ru: {
    chip: 'Пример квартиры',
    label: 'Планировка условная; состав квартир не опубликован',
    title: (rooms) => `Пример ${rooms}-комнатной квартиры`,
    eyebrow: (k, f, dir) => `Башня ${k} · этаж ${f} · окна на ${dir}`,
    size: (rooms, sqm, src) => `Площадь как в опубликованных сделках в башнях: ${rooms} комнаты, ${sqm} м² (${src})`,
    sizeSrc: 'Globes, 02.05.2025',
    from: (f0, f) => `Снимки с ${f0}-го этажа; вы выбрали ${f}-й, вид с него почти такой же`,
    todLbl: 'Время суток', tod: { day: 'День', sunset: 'Закат', evening: 'Вечер' },
    tile: { living: (t) => `Гостиная · ${t.toLowerCase()}`, bedroom: 'Спальня', balcony: 'Балкон', pano: 'Гостиная 360°' },
    date: '21 сентября',
    lit: 'освещённые окна города: иллюстрация',
    cap: {
      living: (t, h) => `Гостиная · ${t.toLowerCase()} · 21 сентября, ${h}`,
      bedroom: (h) => `Угловая спальня, закруглённое окно на северо-запад · 21 сентября, ${h}`,
      balcony: (h) => `Балкон на закате, вид на башню A · 21 сентября, ${h}`,
      twist: (f, b, h) => `То же окно на ${f}-м этаже, направление ${b} · 21 сентября, ${h}`,
    },
    go360: 'Осмотреть гостиную',
    wa: 'Бесплатная консультация о такой квартире',
    gallery: 'Снимки квартиры',
    twistH: 'То же окно на 20-м, 30-м и 38-м этажах',
    twistCap: 'Каждый этаж башни повёрнут на 1,25° относительно нижнего, поэтому одно и то же окно на каждом этаже смотрит немного в другую сторону, и вид поворачивается вместе с ним.',
    twistItem: (f) => `${f}-й этаж`,
    notesSum: 'Что показано условно',
    notes: (eye) => [
      'Квартира, планировка, отделка и мебель условны. Поэтажные планы и состав квартир не опубликованы.',
      'Площадь: 4 комнаты и 140 м², как в трёх опубликованных сделках на 38-м и 39-м этажах (Globes, 02.05.2025). В какой башне была каждая, не опубликовано.',
      `Вид: здания, высоты, улицы и деревья по открытым данным муниципалитета Тель-Авива-Яффо, с высоты глаз на 30-м этаже (около ${frNum(eye)} м) и в ту сторону, куда обращён этот фасад. Высота этажа 4 м оценочная.`,
      'Солнце: его путь над Тель-Авивом 21 сентября, во время, указанное у каждого снимка.',
      'Поворот на 1,25° на этаж опубликован; его направление, по часовой стрелке или против, не опубликовано. На иллюстрации башня повёрнута против часовой стрелки, как и в виртуальной прогулке по площади.',
    ],
    renders: 'Пока есть снимки одной квартиры: башня C, 30-й этаж, западная сторона.',
    close: 'Закрыть', loading: 'Загружаем квартиру', error: 'Снимок не загрузился. Попробуйте позже.',
    drag: 'Ведите пальцем, чтобы осмотреться',
    panoTitle: (k, f) => `Гостиная на закате · башня ${k} · этаж ${f}`,
    panoNote: (f, h) => `Гостиная на ${f}-м этаже, 21 сентября, ${h}. Мебель и отделка условны.`,
  },
  ar: {
    chip: 'شقة نموذجية',
    label: 'المخطط للتوضيح، ولم يُنشر توزيع الشقق',
    title: (rooms) => `شقة نموذجية من ${rooms} غرف`,
    eyebrow: (k, f, dir) => `البرج ${k} · الطابق ${f} · باتجاه ${dir}`,
    size: (rooms, sqm, src) => `بمساحة الصفقات المنشورة في الأبراج: ${rooms} غرف، ${sqm} م² (${src})`,
    sizeSrc: 'غلوبس، 2.5.2025',
    from: (f0, f) => `الصور من الطابق ${f0}؛ اخترتم الطابق ${f}، والإطلالة منه قريبة جداً`,
    todLbl: 'وقت اليوم', tod: { day: 'نهار', sunset: 'غروب', evening: 'مساء' },
    tile: { living: (t) => `الصالون · ${t}`, bedroom: 'غرفة النوم', balcony: 'الشرفة', pano: 'جولة 360 في الصالون' },
    date: '21 أيلول',
    lit: 'نوافذ المدينة المضاءة: رسم توضيحي',
    cap: {
      living: (t, h) => `الصالون · ${t} · 21 أيلول، ${h}`,
      bedroom: (h) => `غرفة النوم في الزاوية، ونافذتها المقوّسة نحو الشمال الغربي · 21 أيلول، ${h}`,
      balcony: (h) => `الشرفة عند الغروب، مع إطلالة على البرج A · 21 أيلول، ${h}`,
      twist: (f, b, h) => `النافذة نفسها في الطابق ${f}، باتجاه ${b} · 21 أيلول، ${h}`,
    },
    go360: 'تجوّلوا بنظركم في الصالون',
    wa: 'استشارة مجانية حول شقة كهذه',
    gallery: 'صور من الشقة',
    twistH: 'النافذة نفسها في الطوابق 20 و30 و38',
    twistCap: 'كل طابق في البرج يدور بمقدار 1.25 درجة عن الطابق الذي تحته، لذلك تطل النافذة نفسها في كل طابق على اتجاه مختلف قليلاً، وتدور الإطلالة معها.',
    twistItem: (f) => `الطابق ${f}`,
    notesSum: 'ما هو توضيحي',
    notes: (eye) => [
      'الشقة وتقسيمها وتشطيباتها وأثاثها رسم توضيحي. لم تُنشر مخططات الطوابق ولا توزيع الشقق.',
      'المساحة: 4 غرف و140 م²، مثل الصفقات الثلاث المنشورة في الطابقين 38 و39 (غلوبس، 2.5.2025). لم يُنشر في أي برج كانت كل منها.',
      `الإطلالة: المباني والارتفاعات والشوارع والأشجار وفق البيانات المفتوحة لبلدية تل أبيب يافا، من ارتفاع النظر في الطابق 30 (نحو ${eye} م) وفي الاتجاه الذي تطل عليه هذه الواجهة. ارتفاع الطابق 4 م تقديري.`,
      'الشمس: مسارها فوق تل أبيب في 21 أيلول، في الساعة المذكورة مع كل صورة.',
      'الدوران بمقدار 1.25 درجة في كل طابق منشور؛ أما اتجاهه، مع عقارب الساعة أو عكسها، فلم يُنشر. في الرسم التوضيحي يدور عكس عقارب الساعة، كما في الجولة الافتراضية في الميدان.',
    ],
    renders: 'توجد حالياً صور لشقة واحدة: البرج C، الطابق 30، الجهة الغربية.',
    close: 'إغلاق', loading: 'جارٍ تحميل الشقة', error: 'لم يتم تحميل الصورة. حاولوا مرة أخرى لاحقاً.',
    drag: 'اسحبوا للنظر حولكم',
    panoTitle: (k, f) => `الصالون عند الغروب · البرج ${k} · الطابق ${f}`,
    panoNote: (f, h) => `الصالون في الطابق ${f}، 21 أيلول، ${h}. الأثاث والتشطيبات للتوضيح.`,
  },
};

const TOD_OF_WORLD = { day: 'day', sunset: 'sunset', night: 'evening' };
const WORLD_OF_TOD = { day: 'day', sunset: 'sunset', evening: 'night' };
const ICON360 = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><ellipse cx="12" cy="12" rx="9.5" ry="4.2"/><path d="M12 3.2v1.6M16.2 7.9l1.6-1.4M7.8 7.9 6.2 6.5"/><path d="m15.4 17.6 2.3-1.2-1.1-2.3"/></svg>';
const ICONX = '<svg viewBox="0 0 20 20" aria-hidden="true" stroke="currentColor" stroke-width="1.8"><path d="M4 4l12 12M16 4L4 16"/></svg>';
const ICONWA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.7l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.6.3 2.7 2.7 0 0 0-.9 2c0 1.2.9 2.4 1 2.5.1.2 1.7 2.6 4.2 3.7 1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.5Z"/></svg>';

export function openExample(o) {
  ensureCss();
  if (window.__nlExample && typeof window.__nlExample.close === 'function') window.__nlExample.close();
  const lang = WORDS[o.lang] ? o.lang : 'en';
  const T = WORDS[lang];
  const rtl = lang === 'he' || lang === 'ar';
  const prevFocus = o.opener || document.activeElement;
  let tod = TOD_OF_WORLD[o.tod] || 'sunset';
  let man = null, ex = null, cur = null, alive = true, viewer = null;

  const root = document.createElement('div');
  root.className = 'nlex';
  root.dir = rtl ? 'rtl' : 'ltr';
  root.lang = lang;
  root.setAttribute('role', 'dialog');
  root.setAttribute('aria-modal', 'true');
  root.setAttribute('aria-labelledby', 'nlex-t');
  const eyebrow = T.eyebrow(o.tower, o.floor, o.facing || '');
  root.innerHTML = `<div class="nlex__backdrop" data-close></div>
    <div class="nlex__box">
      <div class="nlex__top">
        <div class="nlex__head"><span class="nlex__eyebrow">${esc(eyebrow)}</span><span class="nlex__title" id="nlex-t">${esc(T.chip)}</span></div>
        <button class="nlex__x" type="button" data-close aria-label="${esc(T.close)}">${ICONX}</button>
      </div>
      <div class="nlex__body"><div class="nlex__loading" role="status">${esc(T.loading)}<span class="nlex__bar"><i></i></span></div></div>
    </div>`;
  document.body.appendChild(root);
  document.documentElement.classList.add('nlex-open');
  const body = root.querySelector('.nlex__body');
  const xBtn = root.querySelector('.nlex__x');
  xBtn.focus();

  // ------------------------------------------------------------------ the manifest, then the album
  const mu = new URL(o.url, location.href);
  const ver = mu.search;
  const U = (f) => new URL(f, mu).href.split('?')[0] + ver;
  fetch(mu.href, { credentials: 'same-origin' }).then((r) => (r.ok ? r.json() : Promise.reject(new Error('examples ' + r.status)))).then((d) => {
    if (!alive) return;
    man = d;
    ex = (d.examples || []).find((e) => e.id === o.id) || (d.examples || [])[0];
    if (!ex) throw new Error('no example');
    build();
  }).catch(() => { if (alive) body.innerHTML = `<div class="nlex__loading nlex__loading--err" role="alert">${esc(T.error)}</div>`; });

  const timeOf = (s) => (s && s.time) || 'day';
  const still = (room, t) => ex.stills.find((s) => s.room === room && s.time === t);
  const picHtml = (base, kind, alt, sizes, eager) => {
    const ws = kind === 'still' ? `${U(base + '-thumb.webp')} 480w, ${U(base + '-card.webp')} 1200w, ${U(base + '-2k.webp')} 2048w`
      : `${U(base + '-thumb.webp')} 480w, ${U(base + '-card.webp')} 1200w`;
    return `<picture><source type="image/webp" srcset="${esc(ws)}" sizes="${esc(sizes)}"><img src="${esc(U(base + '-card.jpg'))}" width="1200" height="675" alt="${esc(alt)}" decoding="async"${eager ? ' fetchpriority="high"' : ''}></picture>`;
  };
  const eyeH = () => ((+ex.floor - 1) * (+ex.fh || 4) + 1.6).toFixed(1);
  const capOf = (it) => {
    if (it.kind === 'twist') return T.cap.twist(it.floor, deg(lang, Math.round(it.bearing)), it.hour);
    if (it.room === 'living') return T.cap.living(T.tod[it.time], it.hour) + (it.time === 'evening' ? ' · ' + T.lit : ''); // the city's lit windows at night are an illustration (like the world's night view)
    return T.cap[it.room](it.hour);
  };

  function build() {
    const size = ex.size || {};
    const fromLine = +ex.floor !== +o.floor ? `<div class="nlex__from">${esc(T.from(ex.floor, o.floor))}</div>` : '';
    const living = ['day', 'sunset', 'evening'].filter((t) => still('living', t));
    root.querySelector('.nlex__title').textContent = T.title(size.rooms || 4);
    const tiles = [
      `<button class="nlex__tile nlex__tile--360" type="button" data-pano><span class="nlex__thumb"><img src="${esc(U(ex.pano.base + '-thumb.webp'))}" width="480" height="270" alt="" decoding="async"><b class="nlex__360b">${ICON360}<span dir="ltr">360°</span></b></span><span class="nlex__tl">${esc(T.tile.pano)}</span></button>`,
      `<button class="nlex__tile" type="button" data-room="living" aria-pressed="false"><span class="nlex__thumb"><img data-living src="${esc(U(still('living', tod === 'evening' || tod === 'day' || tod === 'sunset' ? tod : 'sunset').base + '-thumb.webp'))}" width="480" height="270" alt="" decoding="async"></span><span class="nlex__tl" data-living-l>${esc(T.tile.living(T.tod[tod]))}</span></button>`,
      ...['bedroom', 'balcony'].filter((r) => ex.stills.some((s) => s.room === r)).map((r) => {
        const s = ex.stills.find((x) => x.room === r);
        return `<button class="nlex__tile" type="button" data-room="${r}" aria-pressed="false"><span class="nlex__thumb"><img src="${esc(U(s.base + '-thumb.webp'))}" width="480" height="270" alt="" decoding="async"></span><span class="nlex__tl">${esc(T.tile[r])}</span></button>`;
      }),
    ].join('');
    const twist = (ex.twist || []).map((w) => `<button class="nlex__tw" type="button" data-twist="${+w.floor}" aria-pressed="false"><span class="nlex__thumb"><img src="${esc(U(w.base + '-thumb.webp'))}" width="480" height="270" alt="" decoding="async" loading="lazy"><b class="nlex__fl">${esc(T.twistItem(w.floor))}</b></span><span class="nlex__tl">${deg(lang, Math.round(w.bearing))}</span></button>`).join('');
    body.innerHTML = `<div class="nlex__main">
        <div class="nlex__hero" data-hero>
          <div class="nlex__pic"></div>
          <span class="nlex__chip">${esc(T.chip)}</span>
          <button class="nlex__go360" type="button" data-pano>${ICON360}<span>${esc(T.go360)}</span><small dir="ltr">360°</small></button>
        </div>
        <div class="nlex__cap" data-cap aria-live="polite"></div>
        <div class="nlex__todrow"><span class="nlex__lbl">${esc(T.todLbl)}</span><span class="nlex__seg" role="group" aria-label="${esc(T.todLbl)}">${living.map((t) => `<button type="button" data-tod="${t}" aria-pressed="false">${esc(T.tod[t])}</button>`).join('')}</span></div>
        <div class="nlex__strip" role="group" aria-label="${esc(T.gallery)}">${tiles}</div>
      </div>
      <div class="nlex__side">
        <div class="nlex__label"><span class="nlex__chip nlex__chip--in">${esc(T.chip)}</span><span>${esc(T.label)}</span></div>
        <div class="nlex__size">${esc(T.size(size.rooms || 4, size.sqm || 140, T.sizeSrc))}</div>
        ${fromLine}
        ${o.wa ? `<a class="nlex__wa" href="${esc(o.wa)}" target="_blank" rel="noopener">${ICONWA}<span>${esc(T.wa)}</span></a>` : ''}
        <div class="nlex__twist">
          <div class="nlex__h">${esc(T.twistH)}</div>
          <div class="nlex__tws" role="group" aria-label="${esc(T.twistH)}">${twist}</div>
          <div class="nlex__note">${esc(T.twistCap)}</div>
        </div>
        <details class="nlex__notes"><summary>${esc(T.notesSum)}</summary><ul>${T.notes(eyeH()).map((n) => `<li>${esc(n)}</li>`).join('')}<li>${esc(T.renders)}</li></ul></details>
      </div>`;
    for (const b of body.querySelectorAll('[data-pano]')) b.addEventListener('click', () => open360(b));
    for (const b of body.querySelectorAll('[data-room]')) b.addEventListener('click', () => showRoom(b.dataset.room));
    for (const b of body.querySelectorAll('[data-tod]')) b.addEventListener('click', () => { setTod(b.dataset.tod, true); });
    for (const b of body.querySelectorAll('[data-twist]')) b.addEventListener('click', () => showTwist(+b.dataset.twist));
    showRoom('living', true);
  }

  function show(it, eager) {
    cur = it;
    const base = it.base, kind = it.kind === 'twist' ? 'twist' : 'still';
    const pic = body.querySelector('.nlex__pic');
    if (!pic) return;
    // the next picture goes on top at once (a picture outside the page would not load its srcset), shown when it has loaded
    const first = !pic.firstChild;
    const next = document.createElement('div');
    next.className = 'nlex__picin' + (first ? '' : ' is-wait');
    next.innerHTML = picHtml(base, kind, capOf(it), '(max-width: 899px) 100vw, 760px', eager);
    const img = next.querySelector('img');
    const done = () => {
      if (!alive) return;
      if (cur !== it) { next.remove(); return; }
      next.classList.remove('is-wait');
      for (const c of [...pic.children]) if (c !== next) c.remove();
      pic.classList.remove('is-err');
    };
    img.addEventListener('load', done, { once: true });
    img.addEventListener('error', () => { if (alive && cur === it) { done(); pic.classList.add('is-err'); pic.dataset.err = T.error; } }, { once: true });
    pic.appendChild(next);
    if (img.complete && img.naturalWidth) done();
    body.querySelector('[data-cap]').innerHTML = esc(capOf(it)).replace(/&lt;bdi dir=&quot;ltr&quot;&gt;(.*?)&lt;\/bdi&gt;/g, '<bdi dir="ltr">$1</bdi>');
    mark();
  }
  function showRoom(room, eager) {
    if (!ex) return;
    let s = room === 'living' ? still('living', tod) || still('living', 'sunset') : ex.stills.find((x) => x.room === room);
    if (!s) return;
    show({ ...s, kind: 'still' }, eager);
    if (room !== 'living' && s.time !== tod) { tod = s.time; tellWorld(); }
  }
  function showTwist(f) {
    const w = (ex.twist || []).find((x) => +x.floor === f);
    if (w) show({ ...w, kind: 'twist', hour: w.hour || '14:30' });
  }
  function setTod(t, fromAlbum) {
    if (!still('living', t)) return;
    tod = t;
    if (ex && body.querySelector('.nlex__pic')) {
      const img = body.querySelector('[data-living]');
      if (img) img.src = U(still('living', t).base + '-thumb.webp');
      const lb = body.querySelector('[data-living-l]');
      if (lb) lb.textContent = T.tile.living(T.tod[t]);
      showRoom('living');
    }
    if (fromAlbum) tellWorld();
  }
  function tellWorld() { if (typeof o.onTod === 'function') o.onTod(WORLD_OF_TOD[tod] || 'day'); }
  function mark() {
    const it = cur || {};
    for (const b of body.querySelectorAll('[data-tod]')) b.setAttribute('aria-pressed', it.kind !== 'twist' && b.dataset.tod === timeOf(it) ? 'true' : 'false');
    for (const b of body.querySelectorAll('[data-room]')) b.setAttribute('aria-pressed', it.kind !== 'twist' && b.dataset.room === it.room ? 'true' : 'false');
    for (const b of body.querySelectorAll('[data-twist]')) b.setAttribute('aria-pressed', it.kind === 'twist' && +b.dataset.twist === +it.floor ? 'true' : 'false');
  }

  // ------------------------------------------------------------------ the 360: the fleet's viewer (tour.js), over the album
  function open360(btn) {
    if (!ex || !ex.pano) return;
    const p = ex.pano;
    import(new URL('../tour.js' + new URL(import.meta.url).search, import.meta.url).href).then((m) => {
      if (!alive) return;
      viewer = m.openTour({
        scenes: [{ id: p.base, dir: 'w', spot: 'living', title: T.panoTitle(o.tower, ex.floor), src: U(p.base + '.webp'), small: U(p.base + '-2k.webp'),
          note: T.panoNote(ex.floor, p.hour), chip: T.chip }],
        chip: T.chip, caption: T.label + '.', hint: T.drag, close: T.close, lang, dir: rtl ? 'rtl' : 'ltr', errorText: T.error, opener: btn,
        onClose: () => { viewer = null; },
      });
    }).catch(() => { /* the album stays; the viewer's own error line covers a failed picture */ });
  }

  // ------------------------------------------------------------------ keys, focus, close
  const focusables = () => [...root.querySelectorAll('button, a[href], summary')].filter((e) => !e.disabled && e.getClientRects().length);
  function onKey(e) {
    if (document.documentElement.classList.contains('nlat-open') || e.defaultPrevented) return; // the 360 viewer handles its own keys
    if (e.key === 'Escape') { e.preventDefault(); close(); return; }
    if (e.key === 'Tab') {
      const f = focusables();
      if (!f.length) return;
      const i = f.indexOf(document.activeElement);
      if (e.shiftKey && (i <= 0)) { e.preventDefault(); f[f.length - 1].focus(); } else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
    }
  }
  document.addEventListener('keydown', onKey);
  for (const b of root.querySelectorAll('[data-close]')) b.addEventListener('click', () => close());
  function close() {
    if (!alive) return;
    alive = false;
    if (viewer && typeof viewer.close === 'function') viewer.close();
    document.removeEventListener('keydown', onKey);
    root.remove();
    document.documentElement.classList.remove('nlex-open');
    if (window.__nlExample === api) window.__nlExample = null;
    // back to the button that opened it; the floor view may have drawn that button again meanwhile (the time of day), so its twin
    const twin = o.opener && o.opener.dataset && o.opener.dataset.example ? document.querySelector('[data-example="' + o.opener.dataset.example.replace(/"/g, '') + '"]') : null;
    const back = prevFocus && prevFocus.isConnected ? prevFocus : twin;
    if (back && back.focus) back.focus({ preventScroll: true });
    if (typeof o.onClose === 'function') o.onClose();
  }
  const api = {
    close,
    setTod: (k) => { const t = TOD_OF_WORLD[k]; if (t && t !== tod) setTod(t, false); },
    get tod() { return tod; },
    get shown() { return cur ? { kind: cur.kind || 'still', room: cur.room || null, time: cur.time || null, floor: cur.floor || null, base: cur.base } : null; },
    el: root,
  };
  window.__nlExample = api;
  return api;
}
