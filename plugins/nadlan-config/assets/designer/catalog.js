// The designer's catalogue (HAD-705, first step). Generic real-size pieces and floor finishes. `price` names a record in
// data/price-ranges.json: a published Israeli price RANGE, never one shop's price and never a site name. Sizes in cm.
export const ITEMS = {
  'gen.sofa3': { he: 'ספה תלת מושבית', n: { en: 'Three-seat sofa', fr: 'Canapé 3 places', ru: 'Трёхместный диван', ar: 'كنبة بثلاثة مقاعد' }, w: 240, d: 100, h: 88, shape: 'sofa', model: 'sofa3', price: 'sofa_3seat' },
  'gen.armchair': { he: 'כורסה', n: { en: 'Armchair', fr: 'Fauteuil', ru: 'Кресло', ar: 'كرسي بذراعين' }, w: 85, d: 85, h: 80, shape: 'sofa', price: 'armchair' },
  'gen.coffee': { he: 'שולחן סלון', n: { en: 'Coffee table', fr: 'Table basse', ru: 'Журнальный столик', ar: 'طاولة قهوة' }, w: 110, d: 60, h: 40, shape: 'table', price: 'coffee_table' },
  'gen.dining6': { he: 'שולחן אוכל ל-6', n: { en: 'Dining table for 6', fr: 'Table à manger 6 personnes', ru: 'Обеденный стол на 6 человек', ar: 'طاولة طعام لستة أشخاص' }, w: 180, d: 90, h: 75, shape: 'table', price: 'dining_table_6' },
  'gen.chair': { he: 'כיסא אוכל', n: { en: 'Dining chair', fr: 'Chaise de salle à manger', ru: 'Обеденный стул', ar: 'كرسي طعام' }, w: 46, d: 55, h: 82, shape: 'box', model: 'dining-chair', price: 'dining_chair' },
  'gen.tv': { he: 'מזנון טלוויזיה', n: { en: 'TV console', fr: 'Meuble TV', ru: 'Тумба под телевизор', ar: 'وحدة تلفاز' }, w: 180, d: 40, h: 45, shape: 'box', price: 'tv_console' },
  'gen.rug': { he: 'שטיח', n: { en: 'Rug', fr: 'Tapis', ru: 'Ковёр', ar: 'سجادة' }, w: 230, d: 160, h: 2, shape: 'rug', price: 'rug_160x230' },
  'gen.bed160': { he: 'מיטה זוגית 160', n: { en: 'Double bed 160', fr: 'Lit double 160', ru: 'Двуспальная кровать 160', ar: 'سرير مزدوج 160' }, w: 175, d: 205, h: 88, shape: 'bed', model: 'bed160', price: 'bed_double_with_mattress' },
  'gen.bedset': { he: 'מיטה זוגית עם שידות', n: { en: 'Double bed with bedside tables', fr: 'Lit double avec chevets', ru: 'Двуспальная кровать с тумбочками', ar: 'سرير مزدوج مع طاولتين جانبيتين' }, w: 242, d: 200, h: 96, shape: 'bed', model: 'bed120', price: 'bed_double_with_mattress' },
  'gen.bedside': { he: 'שידת לילה', n: { en: 'Bedside table', fr: 'Table de chevet', ru: 'Прикроватная тумбочка', ar: 'طاولة سرير جانبية' }, w: 45, d: 40, h: 50, shape: 'box' },
  'gen.bed120': { he: 'מיטה וחצי 120', n: { en: 'Small double bed 120', fr: 'Lit 120', ru: 'Полутороспальная кровать 120', ar: 'سرير نصف مزدوج 120' }, w: 120, d: 200, h: 55, shape: 'bed', price: 'bed_single' },
  'gen.wardrobe': { he: 'ארון הזזה 200', n: { en: 'Sliding-door wardrobe 200', fr: 'Armoire à portes coulissantes 200', ru: 'Шкаф-купе 200', ar: 'خزانة بأبواب منزلقة 200' }, w: 200, d: 60, h: 240, shape: 'box', price: 'wardrobe_sliding_2m' },
  'gen.wardrobe2': { he: 'ארון שתי דלתות', n: { en: 'Two-door wardrobe', fr: 'Armoire deux portes', ru: 'Двухдверный шкаф', ar: 'خزانة ببابين' }, w: 127, d: 62, h: 240, shape: 'box', model: 'wardrobe200' },
  'gen.desk': { he: 'שולחן עבודה', n: { en: 'Desk', fr: 'Bureau', ru: 'Письменный стол', ar: 'مكتب' }, w: 120, d: 60, h: 75, shape: 'table', price: 'desk' },
  'gen.lamp': { he: 'מנורת רצפה', n: { en: 'Floor lamp', fr: 'Lampadaire', ru: 'Торшер', ar: 'مصباح أرضي' }, w: 40, d: 40, h: 160, shape: 'plant', price: 'floor_lamp' },
  'gen.kitchen': { he: 'ארונות מטבח ומשטח', n: { en: 'Kitchen cabinets and worktop', fr: 'Meubles de cuisine et plan de travail', ru: 'Кухонные шкафы и столешница', ar: 'خزائن مطبخ وسطح عمل' }, w: 330, d: 60, h: 90, shape: 'counter', price: { per_m: ['kitchen_cab_mid', 'worktop_quartz'] } },
  'gen.island': { he: 'אי מטבח', n: { en: 'Kitchen island', fr: 'Îlot de cuisine', ru: 'Кухонный остров', ar: 'جزيرة مطبخ' }, w: 160, d: 90, h: 90, shape: 'counter', price: 'kitchen_island' },
  'gen.plant': { he: 'עציץ', n: { en: 'Potted plant', fr: 'Plante en pot', ru: 'Растение в горшке', ar: 'نبتة في أصيص' }, w: 45, d: 45, h: 140, shape: 'plant' },
};

// status: base = part of the example specification, upgrade = a change from it. Example labels only, not a developer's list.
export const FINISHES = {
  'porcelain-80': { he: 'גרניט פורצלן 80×80', n: { en: 'Porcelain tiles 80×80', fr: 'Grès cérame 80×80', ru: 'Керамогранит 80×80', ar: 'بلاط بورسلان 80×80' }, status: 'base', tex: 'tile', size: 80, a: '#D9DBD6', b: '#BFC3BD' },
  'porcelain-60': { he: 'גרניט פורצלן 60×60 נגד החלקה', n: { en: 'Anti-slip porcelain tiles 60×60', fr: 'Grès cérame antidérapant 60×60', ru: 'Противоскользящий керамогранит 60×60', ar: 'بلاط بورسلان مانع للانزلاق 60×60' }, status: 'base', tex: 'tile', size: 60, a: '#C9CED1', b: '#AEB5B9' },
  'oak-plank': { he: 'פרקט עץ תלת שכבתי', n: { en: 'Engineered wood parquet', fr: 'Parquet contrecollé', ru: 'Трёхслойный паркет', ar: 'باركيه خشبي ثلاثي الطبقات' }, status: 'upgrade', tex: 'wood', size: 160, a: '#B98F5E', b: '#8E6A41', price: 'engineered_parquet' },
  laminate: { he: 'פרקט למינציה', n: { en: 'Laminate flooring', fr: 'Parquet stratifié', ru: 'Ламинат', ar: 'باركيه لامينيت' }, status: 'upgrade', tex: 'wood', size: 150, a: '#CDB08A', b: '#A88A63', price: 'laminate' },
  spc: { he: 'ריצוף SPC דמוי עץ', n: { en: 'Wood-look SPC flooring', fr: 'Sol SPC aspect bois', ru: 'SPC-покрытие под дерево', ar: 'أرضية SPC بمظهر الخشب' }, status: 'upgrade', tex: 'wood', size: 140, a: '#A79887', b: '#857767', price: 'spc_vinyl' },
  terrazzo: { he: 'טראצו', n: { en: 'Terrazzo', fr: 'Terrazzo', ru: 'Терраццо', ar: 'تيرازو' }, status: 'upgrade', tex: 'terrazzo', size: 100, a: '#D8D2C8', b: '#6E7B85' },
  deck: { he: 'ריצוף מרפסת', n: { en: 'Balcony flooring', fr: 'Sol de balcon', ru: 'Покрытие для балкона', ar: 'أرضية الشرفة' }, status: 'base', tex: 'deck', size: 120, a: '#9A948A', b: '#7D776E' },
};
export const FLOOR_CHOICES = ['porcelain-80', 'oak-plank', 'laminate', 'spc', 'terrazzo'];
// wall paint per room (HAD-792): a colour the buyer asks for, said in the design order; price not included (paint is usually
// part of the developer's specification in white; a colour is a request to the developer or a later job)
export const WALLS = {
  'w-white': { he: 'לבן', n: { en: 'White', fr: 'Blanc', ru: 'Белый', ar: 'أبيض' }, hex: '#EEF0EE', status: 'base' },
  'w-mist': { he: 'אפור ערפל', n: { en: 'Mist grey', fr: 'Gris brume', ru: 'Туманно-серый', ar: 'رمادي ضبابي' }, hex: '#D6DCE0', status: 'upgrade' },
  'w-sky': { he: 'כחול שמיים בהיר', n: { en: 'Pale sky blue', fr: 'Bleu ciel pâle', ru: 'Бледно-голубой', ar: 'أزرق سماوي فاتح' }, hex: '#C7D8E6', status: 'upgrade' },
  'w-sage': { he: 'ירוק מרווה', n: { en: 'Sage green', fr: 'Vert sauge', ru: 'Шалфейный зелёный', ar: 'أخضر مريمية' }, hex: '#B8C6B3', status: 'upgrade' },
  'w-olive': { he: 'זית עמוק', n: { en: 'Deep olive', fr: 'Olive profond', ru: 'Глубокий оливковый', ar: 'زيتوني داكن' }, hex: '#7F8C6E', status: 'upgrade' },
  'w-slate': { he: 'פחם', n: { en: 'Charcoal', fr: 'Anthracite', ru: 'Графит', ar: 'فحمي' }, hex: '#4B5661', status: 'upgrade' },
};
export const WALL_CHOICES = Object.keys(WALLS);
/** a catalogue word in the page language: the Hebrew is the source, n holds the others */
export const label = (rec, lang) => (!rec ? '' : !lang || lang === 'he' ? rec.he : (rec.n && (rec.n[lang] || rec.n.en)) || rec.he);

let n = 0;
const it = (sku, x, y, rot = 0) => ({ id: 'i' + ++n, sku, x, y, rot, status: 'decor' });
export const STARTER = [
  // a piece faces +y (down the sheet) at rot 0; its back is on the -y side
  it('gen.rug', 455, 210, 90), it('gen.sofa3', 330, 210, 270), it('gen.tv', 588, 210, 90), it('gen.dining6', 200, 430), it('gen.plant', 60, 60),
  it('gen.kitchen', 184, 857, 180), it('gen.island', 185, 660),
  it('gen.bedset', 732, 190, 270), it('gen.chair', 150, 365), it('gen.chair', 250, 365), it('gen.chair', 150, 495, 180), it('gen.chair', 250, 495, 180),
  it('gen.bed160', 1215, 190, 90), it('gen.wardrobe2', 1066, 344, 180),
];
