// Room names found in the project plans (Hebrew, the source) in en, fr, ru and ar.
//   import { roomName } from './roomnames.js';   roomName('ממ״ד', 'fr') -> 'Pièce sécurisée (Mamad)'
// An exact match first, then a match without gershayim and extra spaces, then the same with a trailing number kept
// ('חדר שינה 2' -> 'Bedroom 2'). An unknown name comes back in Hebrew, unchanged.
const LIVING_DINING = { en: 'Living room and dining area', fr: 'Séjour et coin repas', ru: 'Гостиная и обеденная зона', ar: 'غرفة معيشة وركن طعام' };
const LIVING = { en: 'Living room', fr: 'Salon', ru: 'Гостиная', ar: 'غرفة معيشة' };
const BATH = { en: 'Bathroom', fr: 'Salle de bains', ru: 'Ванная', ar: 'حمّام' };
const MASTER = { en: 'Main bedroom', fr: 'Chambre parentale', ru: 'Родительская спальня', ar: 'غرفة نوم رئيسية' };

export const ROOM_NAMES = {
  'חדר דיור ופינת אוכל': LIVING_DINING,
  'סלון ופינת אוכל': LIVING_DINING,
  'חדר דיור': { en: 'Living room', fr: 'Séjour', ru: 'Гостиная', ar: 'غرفة معيشة' },
  'סלון': LIVING,
  'סלון ומטבח': { en: 'Living room and kitchen', fr: 'Salon et cuisine', ru: 'Гостиная с кухней', ar: 'غرفة معيشة ومطبخ' },
  'מטבח ופינת אוכל': { en: 'Kitchen and dining area', fr: 'Cuisine et coin repas', ru: 'Кухня и обеденная зона', ar: 'مطبخ وركن طعام' },
  'פינת אוכל': { en: 'Dining area', fr: 'Coin repas', ru: 'Обеденная зона', ar: 'ركن طعام' },
  'מטבח': { en: 'Kitchen', fr: 'Cuisine', ru: 'Кухня', ar: 'مطبخ' },
  'חדר רחצה': BATH,
  'רחצה': BATH,
  'חדר רחצה הורים': { en: 'Main bathroom', fr: 'Salle de bains parentale', ru: 'Родительская ванная', ar: 'حمّام غرفة النوم الرئيسية' },
  'מקלחת הורים': { en: 'Main shower room', fr: 'Salle d’eau parentale', ru: 'Родительская душевая', ar: 'غرفة استحمام رئيسية' },
  'מקלחת': { en: 'Shower room', fr: 'Salle d’eau', ru: 'Душевая', ar: 'غرفة استحمام' },
  'חדר שינה הורים': MASTER,
  'שינה הורים': MASTER,
  'יחידת הורים': { en: 'Main bedroom suite', fr: 'Suite parentale', ru: 'Родительская спальня с санузлом', ar: 'جناح نوم رئيسي' },
  'חדר שינה': { en: 'Bedroom', fr: 'Chambre', ru: 'Спальня', ar: 'غرفة نوم' },
  'חדר ילדים': { en: 'Children’s room', fr: 'Chambre d’enfant', ru: 'Детская', ar: 'غرفة أطفال' },
  'ממ״ד': { en: 'Safe room (Mamad)', fr: 'Pièce sécurisée (Mamad)', ru: 'Защищённая комната (мамад)', ar: 'غرفة محصنة (ممّاد)' },
  'כניסה': { en: 'Entrance', fr: 'Entrée', ru: 'Прихожая', ar: 'مدخل' },
  'מבואה': { en: 'Entrance hall', fr: 'Hall d’entrée', ru: 'Холл', ar: 'ردهة المدخل' },
  'מסדרון': { en: 'Corridor', fr: 'Couloir', ru: 'Коридор', ar: 'ممر' },
  'מרפסת': { en: 'Balcony', fr: 'Balcon', ru: 'Балкон', ar: 'شرفة' },
  'מרפסת שמש': { en: 'Open balcony', fr: 'Balcon ouvert', ru: 'Открытый балкон', ar: 'شرفة مكشوفة' },
  'מרפסת שירות': { en: 'Laundry balcony', fr: 'Balcon buanderie', ru: 'Хозяйственный балкон', ar: 'شرفة غسيل' },
  'שירות': { en: 'Utility room', fr: 'Buanderie', ru: 'Подсобное помещение', ar: 'غرفة خدمات' },
  'חדר כביסה': { en: 'Laundry room', fr: 'Buanderie', ru: 'Постирочная', ar: 'غرفة غسيل' },
  'שירותי אורחים': { en: 'Guest toilet', fr: 'WC invités', ru: 'Гостевой туалет', ar: 'دورة مياه للضيوف' },
  'שירותים': { en: 'Toilet', fr: 'WC', ru: 'Туалет', ar: 'دورة مياه' },
  'חדר עבודה': { en: 'Study', fr: 'Bureau', ru: 'Кабинет', ar: 'غرفة مكتب' },
  'חדר ארונות': { en: 'Walk-in closet', fr: 'Dressing', ru: 'Гардеробная', ar: 'غرفة ملابس' },
  'מחסן': { en: 'Storeroom', fr: 'Cellier', ru: 'Кладовая', ar: 'مخزن' },
  'פינת משפחה': { en: 'Family corner', fr: 'Coin famille', ru: 'Семейный уголок', ar: 'ركن العائلة' },
  'חלל חדש': { en: 'New space', fr: 'Nouvel espace', ru: 'Новое помещение', ar: 'مساحة جديدة' },
  'גינה': { en: 'Garden', fr: 'Jardin', ru: 'Сад', ar: 'حديقة' },
  'לא חלק מהדירה': { en: 'Not part of the apartment', fr: 'Hors de l’appartement', ru: 'Не часть квартиры', ar: 'ليس جزءًا من الشقة' },
};

// gershayim (Hebrew ״, ASCII ", typographic “ ” and „) are dropped, spaces collapsed
const norm = (s) => String(s).replace(/[״"“”„]/g, '').replace(/\s+/g, ' ').trim();
const BY_NORM = Object.fromEntries(Object.keys(ROOM_NAMES).map((k) => [norm(k), ROOM_NAMES[k]]));

export function roomName(he, lang) {
  if (he == null || he === '') return he;
  if (!lang || lang === 'he') return he;
  const exact = ROOM_NAMES[he];
  if (exact && exact[lang]) return exact[lang];
  const n = norm(he);
  const hit = BY_NORM[n];
  if (hit && hit[lang]) return hit[lang];
  const m = n.match(/^(.*\S)\s+(\d+)$/); // a numbered room: 'חדר שינה 2'
  if (m && BY_NORM[m[1]] && BY_NORM[m[1]][lang]) return BY_NORM[m[1]][lang] + ' ' + m[2];
  return he;
}
