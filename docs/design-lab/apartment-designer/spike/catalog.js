// Spike catalogue (HAD-703). Generic real-size pieces and three floor finishes, with NO prices:
// real products, prices, sources, dates and VAT basis arrive with the catalogue task (HAD-705). Sizes in cm.
export const ITEMS = {
  'gen.sofa3': { he: 'ספה תלת מושבית', w: 240, d: 95, h: 82, shape: 'sofa' },
  'gen.armchair': { he: 'כורסה', w: 85, d: 85, h: 80, shape: 'sofa' },
  'gen.dining6': { he: 'שולחן אוכל ל-6', w: 180, d: 90, h: 75, shape: 'table' },
  'gen.tv': { he: 'מזנון טלוויזיה', w: 180, d: 40, h: 45, shape: 'box' },
  'gen.rug': { he: 'שטיח', w: 240, d: 170, h: 2, shape: 'rug' },
  'gen.bed160': { he: 'מיטה זוגית 160', w: 160, d: 200, h: 55, shape: 'bed' },
  'gen.bed120': { he: 'מיטה וחצי 120', w: 120, d: 200, h: 55, shape: 'bed' },
  'gen.wardrobe': { he: 'ארון בגדים', w: 200, d: 60, h: 240, shape: 'box' },
  'gen.desk': { he: 'שולחן עבודה', w: 120, d: 60, h: 75, shape: 'table' },
  'gen.kitchen': { he: 'ארונות מטבח', w: 330, d: 60, h: 90, shape: 'counter' },
  'gen.island': { he: 'אי מטבח', w: 160, d: 90, h: 90, shape: 'counter' },
  'gen.plant': { he: 'עציץ', w: 45, d: 45, h: 140, shape: 'plant' },
};

// status: base = part of the example specification, upgrade = a change from it. Example labels only, not a developer's list.
export const FINISHES = {
  'porcelain-80': { he: 'גרניט פורצלן 80×80', status: 'base', tex: 'tile', size: 80, a: '#D9DBD6', b: '#BFC3BD' },
  'porcelain-60': { he: 'גרניט פורצלן 60×60 נגד החלקה', status: 'base', tex: 'tile', size: 60, a: '#C9CED1', b: '#AEB5B9' },
  'oak-plank': { he: 'פרקט אלון', status: 'upgrade', tex: 'wood', size: 160, a: '#B98F5E', b: '#8E6A41' },
  terrazzo: { he: 'טראצו', status: 'upgrade', tex: 'terrazzo', size: 100, a: '#D8D2C8', b: '#6E7B85' },
  deck: { he: 'ריצוף מרפסת', status: 'base', tex: 'deck', size: 120, a: '#9A948A', b: '#7D776E' },
};
export const FLOOR_CHOICES = ['porcelain-80', 'oak-plank', 'terrazzo'];

let n = 0;
const it = (sku, x, y, rot = 0) => ({ id: 'i' + ++n, sku, x, y, rot, status: 'decor' });
export const STARTER = [
  // a piece faces +y (down the sheet) at rot 0; its back is on the -y side
  it('gen.rug', 455, 210, 90), it('gen.sofa3', 330, 210, 270), it('gen.tv', 588, 210, 90), it('gen.dining6', 200, 430), it('gen.plant', 60, 60),
  it('gen.kitchen', 184, 857, 180), it('gen.island', 185, 660),
  it('gen.bed160', 730, 150, 270), it('gen.wardrobe', 860, 345, 180),
  it('gen.bed120', 1207, 140, 90), it('gen.desk', 1085, 345, 180),
];
