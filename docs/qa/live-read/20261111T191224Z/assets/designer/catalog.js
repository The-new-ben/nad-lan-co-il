// The designer's catalogue (HAD-705, first step). Generic real-size pieces and floor finishes. `price` names a record in
// data/price-ranges.json: a published Israeli price RANGE, never one shop's price and never a site name. Sizes in cm.
export const ITEMS = {
  'gen.sofa3': { he: 'ספה תלת מושבית', w: 240, d: 100, h: 88, shape: 'sofa', model: 'sofa3', price: 'sofa_3seat' },
  'gen.armchair': { he: 'כורסה', w: 85, d: 85, h: 80, shape: 'sofa', price: 'armchair' },
  'gen.coffee': { he: 'שולחן סלון', w: 110, d: 60, h: 40, shape: 'table', price: 'coffee_table' },
  'gen.dining6': { he: 'שולחן אוכל ל-6', w: 180, d: 90, h: 75, shape: 'table', price: 'dining_table_6' },
  'gen.chair': { he: 'כיסא אוכל', w: 46, d: 55, h: 82, shape: 'box', model: 'dining-chair', price: 'dining_chair' },
  'gen.tv': { he: 'מזנון טלוויזיה', w: 180, d: 40, h: 45, shape: 'box', price: 'tv_console' },
  'gen.rug': { he: 'שטיח', w: 230, d: 160, h: 2, shape: 'rug', price: 'rug_160x230' },
  'gen.bed160': { he: 'מיטה זוגית 160', w: 175, d: 205, h: 88, shape: 'bed', model: 'bed160', price: 'bed_double_with_mattress' },
  'gen.bedset': { he: 'מיטה זוגית עם שידות', w: 242, d: 200, h: 96, shape: 'bed', model: 'bed120', price: 'bed_double_with_mattress' },
  'gen.bedside': { he: 'שידת לילה', w: 45, d: 40, h: 50, shape: 'box' },
  'gen.bed120': { he: 'מיטה וחצי 120', w: 120, d: 200, h: 55, shape: 'bed', price: 'bed_single' },
  'gen.wardrobe': { he: 'ארון הזזה 200', w: 200, d: 60, h: 240, shape: 'box', price: 'wardrobe_sliding_2m' },
  'gen.wardrobe2': { he: 'ארון שתי דלתות', w: 127, d: 62, h: 240, shape: 'box', model: 'wardrobe200' },
  'gen.desk': { he: 'שולחן עבודה', w: 120, d: 60, h: 75, shape: 'table', price: 'desk' },
  'gen.lamp': { he: 'מנורת רצפה', w: 40, d: 40, h: 160, shape: 'plant', price: 'floor_lamp' },
  'gen.kitchen': { he: 'ארונות מטבח ומשטח', w: 330, d: 60, h: 90, shape: 'counter', price: { per_m: ['kitchen_cab_mid', 'worktop_quartz'] } },
  'gen.island': { he: 'אי מטבח', w: 160, d: 90, h: 90, shape: 'counter', price: 'kitchen_island' },
  'gen.plant': { he: 'עציץ', w: 45, d: 45, h: 140, shape: 'plant' },
};

// status: base = part of the example specification, upgrade = a change from it. Example labels only, not a developer's list.
export const FINISHES = {
  'porcelain-80': { he: 'גרניט פורצלן 80×80', status: 'base', tex: 'tile', size: 80, a: '#D9DBD6', b: '#BFC3BD' },
  'porcelain-60': { he: 'גרניט פורצלן 60×60 נגד החלקה', status: 'base', tex: 'tile', size: 60, a: '#C9CED1', b: '#AEB5B9' },
  'oak-plank': { he: 'פרקט עץ תלת שכבתי', status: 'upgrade', tex: 'wood', size: 160, a: '#B98F5E', b: '#8E6A41', price: 'engineered_parquet' },
  laminate: { he: 'פרקט למינציה', status: 'upgrade', tex: 'wood', size: 150, a: '#CDB08A', b: '#A88A63', price: 'laminate' },
  spc: { he: 'ריצוף SPC דמוי עץ', status: 'upgrade', tex: 'wood', size: 140, a: '#A79887', b: '#857767', price: 'spc_vinyl' },
  terrazzo: { he: 'טראצו', status: 'upgrade', tex: 'terrazzo', size: 100, a: '#D8D2C8', b: '#6E7B85' },
  deck: { he: 'ריצוף מרפסת', status: 'base', tex: 'deck', size: 120, a: '#9A948A', b: '#7D776E' },
};
export const FLOOR_CHOICES = ['porcelain-80', 'oak-plank', 'laminate', 'spc', 'terrazzo'];

let n = 0;
const it = (sku, x, y, rot = 0) => ({ id: 'i' + ++n, sku, x, y, rot, status: 'decor' });
export const STARTER = [
  // a piece faces +y (down the sheet) at rot 0; its back is on the -y side
  it('gen.rug', 455, 210, 90), it('gen.sofa3', 330, 210, 270), it('gen.tv', 588, 210, 90), it('gen.dining6', 200, 430), it('gen.plant', 60, 60),
  it('gen.kitchen', 184, 857, 180), it('gen.island', 185, 660),
  it('gen.bedset', 732, 190, 270), it('gen.chair', 150, 365), it('gen.chair', 250, 365), it('gen.chair', 150, 495, 180), it('gen.chair', 250, 495, 180),
  it('gen.bed160', 1215, 190, 90), it('gen.wardrobe2', 1066, 344, 180),
];
