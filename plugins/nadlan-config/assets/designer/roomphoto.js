// "The floor and paint in your room" (NadLan). A person photographs a real room, marks the floor (and a wall if they want),
// picks a floor from our catalogue or a wall colour, and sees their own room with it: true perspective, the original light
// and shadows kept. Everything runs in the browser: the photo never leaves the device. No server, no AI.
//
//   import { mountRoomPhoto } from '.../assets/designer/roomphoto.js';
//   const r = await mountRoomPhoto(host, { lang: 'he', version: '1' });   ...   r.destroy();
//
// The host decides the size; the tool fills it, inside its own shadow root (the site's CSS cannot reach it).
// The math (floor from four taps, patterns, light) is in photowarp.js and is checked in node.
import * as W from './photowarp.js';
import { FINISHES } from './catalog.js';
import { strings } from './strings.js';

const BASE = new URL('.', import.meta.url).href;
const FONTS = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&display=swap';
const MAX_SIDE = 2400, DEG = Math.PI / 180;
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const TXT = {
  he: {
    dir: 'rtl', title: 'הריצוף והצבע בחדר שלכם',
    lead: 'מעלים צילום של החדר, מסמנים את הרצפה, ובוחרים ריצוף. רואים את החדר שלכם, לא חדר לדוגמה.',
    pick: 'בחירת צילום', shoot: 'צילום עכשיו', sample: 'לנסות על חדר לדוגמה',
    privacy: 'הצילום נשאר במכשיר שלכם. הוא לא נשלח לאתר ולא נשמר אצלנו.',
    tip: 'הכי טוב לצלם לרוחב, מגובה החזה, כך שרואים את הקיר שמולכם ואת הרצפה עד אליו.',
    newPhoto: 'צילום אחר', loading: 'מכינים את הצילום', working: 'מציירים את החדר', badFile: 'לא הצלחנו לפתוח את הקובץ. נסו צילום אחר.',
    cornersH: 'מסמנים את הרצפה',
    cornersP: 'געו בארבע פינות של הרצפה, לפי הסדר. אם פינה מוסתרת, סמנו איפה שהיא אמורה להיות.',
    cornersTip: 'הפינות הקרובות אליכם בדרך כלל מחוץ לתמונה. במקומן סמנו נקודה על קו הקיר, ליד תחתית הצילום, בכל צד.',
    cornersDrag: 'אפשר לגרור כל נקודה כדי לדייק.', count: (n) => 'סומנו ' + n + ' מתוך 4', again: 'לסמן מחדש', next: 'המשך',
    badQuad: 'הנקודות לא יוצרות רצפה. סמנו ארבע פינות מסביב לרצפה.',
    furnH: 'רהיטים על הרצפה',
    furnP: 'ספה או שולחן עומדים על הרצפה? געו מסביב לרהיט, נקודה אחרי נקודה, והריצוף החדש לא יצויר עליו.',
    furnDone: 'סיום הרהיט', undoPt: 'ביטול הנקודה האחרונה', furnCount: (n) => 'רהיטים שהוצאו: ' + n, furnClear: 'מחיקת הרהיטים',
    draftCount: (n) => 'נקודות מסביב לרהיט: ' + n, wallDraft: (n) => 'נקודות בקיר: ' + n, closeTip: 'אפשר לסגור גם בנגיעה בנקודה הראשונה.',
    sizeH: 'כמה רחב החדר?', sizeP: 'המידה לאורך הקיר שמולכם, הקו האדום בתמונה, בסנטימטרים.',
    widthL: 'רוחב בס״מ', depthL: 'עומק בס״מ (רשות)', eg: 'למשל 420',
    sizeWhy: 'עם מידה, האריחים מצוירים בגודל אמיתי ומופיעים שטח ומחיר משוער.', noSize: 'בלי מידה', badSize: 'המידה צריכה להיות בין 100 ל־3000 ס״מ.',
    guess: 'בלי מידה, גודל האריחים משוער לפי הצילום.',
    finH: 'בוחרים ריצוף', dirL: 'כיוון ההנחה', move: 'הזזת נקודת ההתחלה', moveHint: 'גוררים על הרצפה בתמונה כדי להזיז את הריצוף.', center: 'למרכז',
    perSqm: 'למ״ר', noPrice: 'אין טווח מחיר שפורסם', cm: 'ס״מ', to: ' עד ', shekel: '₪', boards: 'לוחות', seamless: 'משטח רציף, בלי פוגות',
    wallH: 'לצבוע קיר', wallP: 'געו בפינות הקיר, נקודה אחרי נקודה, ולחצו סיום הקיר. אחר כך בוחרים גוון.',
    wallDone: 'סיום הקיר', wallCount: (n) => 'קירות מסומנים: ' + n, wallClear: 'מחיקת הקירות', noPaint: 'בלי צבע',
    paintPrice: (a) => 'צביעת קירות בערך ' + a + ' ₪ למ״ר, לפי טווחי מחיר שפורסמו.', needWall: 'כדי לראות את הגוון, סמנו קיר על התמונה.',
    toWall: 'לצבוע קיר', toResult: 'לפני ואחרי',
    resH: 'לפני ואחרי', resP: 'גוררים את הקו על התמונה.', save: 'שמירת התמונה', saved: 'התמונה נשמרה במכשיר.',
    area: (a) => 'שטח הרצפה בערך ' + a + ' מ״ר', priceLine: (lo, hi) => 'הריצוף הזה בערך ' + lo + ' עד ' + hi + ' ₪ לפי טווחי מחיר שפורסמו',
    noPriceLine: 'לריצוף הזה עוד אין טווח מחיר שפורסם', needSize: 'כדי לראות שטח ומחיר משוער, הוסיפו את רוחב החדר.', addSize: 'הוספת מידה',
    depthGuess: 'העומק משוער מהצילום.', truth: 'זו המחשה על הצילום שלכם. הגוון בפועל תלוי באור ובמסך.',
    before: 'לפני', after: 'אחרי', width: 'רוחב', sampleNote: 'החדר לדוגמה כבר מסומן. בחרו ריצוף, או גררו את הנקודות.',
    tabs: { corners: 'רצפה', furniture: 'רהיטים', size: 'מידה', finish: 'ריצוף', wall: 'קיר', result: 'תוצאה' }, tabsL: 'שלבים',
    stage: 'התמונה של החדר', fileName: 'החדר-שלי-חדש.jpg',
  },
  en: {
    dir: 'ltr', title: 'Flooring and paint in your own room',
    lead: 'Upload a photo of the room, mark the floor, and pick a floor. You see your own room, not a sample room.',
    pick: 'Choose a photo', shoot: 'Take a photo now', sample: 'Try it on a sample room',
    privacy: 'The photo stays on your device. It is not sent to the site and we do not keep it.',
    tip: 'Best: a landscape photo from chest height, showing the wall in front of you and the floor up to it.',
    newPhoto: 'Another photo', loading: 'Preparing the photo', working: 'Drawing the room', badFile: 'We could not open that file. Try another photo.',
    cornersH: 'Mark the floor',
    cornersP: 'Tap the four corners of the floor, in order. If a corner is hidden, mark where it should be.',
    cornersTip: 'The corners nearest to you are usually outside the photo. Mark a point on the wall line near the bottom of the photo on each side instead.',
    cornersDrag: 'You can drag any point to fine-tune it.', count: (n) => n + ' of 4 marked', again: 'Start again', next: 'Next',
    badQuad: 'These points do not make a floor. Mark four corners around the floor.',
    furnH: 'Furniture on the floor',
    furnP: 'A sofa or a table standing on the floor? Tap around it, point by point, and the new floor will not be drawn over it.',
    furnDone: 'Done with this piece', undoPt: 'Remove the last point', furnCount: (n) => 'Pieces left out: ' + n, furnClear: 'Clear the furniture',
    draftCount: (n) => 'Points around the piece: ' + n, wallDraft: (n) => 'Points on the wall: ' + n, closeTip: 'You can also close it by tapping the first point.',
    sizeH: 'How wide is the room?', sizeP: 'Along the wall in front of you, the red line in the photo, in centimetres.',
    widthL: 'Width in cm', depthL: 'Depth in cm (optional)', eg: 'e.g. 420',
    sizeWhy: 'With a measure, tiles are drawn at their true size, and you see the area and an estimated price.', noSize: 'No measure', badSize: 'The measure should be between 100 and 3000 cm.',
    guess: 'With no measure, the tile size is estimated from the photo.',
    finH: 'Choose a floor', dirL: 'Laying direction', move: 'Move the starting point', moveHint: 'Drag on the floor in the photo to shift the pattern.', center: 'Centre',
    perSqm: 'per m²', noPrice: 'No published price range', cm: 'cm', to: ' to ', shekel: '₪', boards: 'Boards', seamless: 'Seamless, no joints',
    wallH: 'Paint a wall', wallP: 'Tap the corners of the wall, point by point, then press Done with this wall. Then pick a colour.',
    wallDone: 'Done with this wall', wallCount: (n) => 'Walls marked: ' + n, wallClear: 'Clear the walls', noPaint: 'No paint',
    paintPrice: (a) => 'Wall painting about ' + a + ' ₪ per m², from published price ranges.', needWall: 'To see the colour, mark a wall on the photo.',
    toWall: 'Paint a wall', toResult: 'Before and after',
    resH: 'Before and after', resP: 'Drag the line on the photo.', save: 'Save the picture', saved: 'The picture was saved on your device.',
    area: (a) => 'Floor area about ' + a + ' m²', priceLine: (lo, hi) => 'this floor about ' + lo + ' to ' + hi + ' ₪ from published price ranges',
    noPriceLine: 'no published price range for this floor yet', needSize: 'To see the area and an estimated price, add the width of the room.', addSize: 'Add a measure',
    depthGuess: 'The depth is estimated from the photo.', truth: 'This is an illustration on your photo. The real shade depends on the light and the screen.',
    before: 'Before', after: 'After', width: 'Width', sampleNote: 'The sample room is already marked. Pick a floor, or drag the points.',
    tabs: { corners: 'Floor', furniture: 'Furniture', size: 'Size', finish: 'Flooring', wall: 'Wall', result: 'Result' }, tabsL: 'Steps',
    stage: 'The photo of the room', fileName: 'my-room-new.jpg',
  },
};

const EN_FIN = { 'porcelain-80': 'Porcelain tile 80×80', 'porcelain-60': 'Porcelain tile 60×60, anti-slip', 'oak-plank': 'Engineered oak, three-layer', laminate: 'Laminate', spc: 'Wood-look SPC', terrazzo: 'Terrazzo', deck: 'Balcony decking' };
// The floors to try: the finishes of our catalogue (names, colours, prices from it), plus drawing-only patterns. A porcelain
// tile of any size is priced with the published range for porcelain flooring supplied and laid; a floor with no published
// range says so and shows no price.
const FLOORS = [
  { k: 'porcelain-80', cat: 'porcelain-80', tex: 'tile', w: 80, h: 80, price: 'tile_supplied_laid' },
  { k: 'porcelain-60', cat: 'porcelain-60', tex: 'tile', w: 60, h: 60, price: 'tile_supplied_laid' },
  { k: 'porcelain-100', he: 'גרניט פורצלן 100×100', en: 'Porcelain tile 100×100', tex: 'tile', w: 100, h: 100, a: '#E6E5E1', b: '#CBCAC4', price: 'tile_supplied_laid' },
  { k: 'porcelain-60x120', he: 'גרניט פורצלן 60×120', en: 'Porcelain tile 60×120', tex: 'tile', w: 120, h: 60, a: '#A7AAA8', b: '#8B8F8D', grout: '#6F7371', price: 'tile_supplied_laid' },
  { k: 'oak-plank', cat: 'oak-plank', tex: 'wood', pw: 19, pl: 160 },
  { k: 'laminate', cat: 'laminate', tex: 'wood', pw: 19, pl: 128 },
  { k: 'spc', cat: 'spc', tex: 'wood', pw: 18, pl: 122 },
  { k: 'terrazzo', cat: 'terrazzo', tex: 'terrazzo' },
  { k: 'concrete', he: 'מראה בטון', en: 'Concrete look', tex: 'concrete', a: '#A6A5A1', b: '#8E8D89' },
  { k: 'deck', cat: 'deck', tex: 'deck', pw: 14, pl: 120 },
].map((f) => {
  const c = f.cat ? FINISHES[f.cat] : null;
  return { ...f, he: f.he || (c && c.he) || f.k, en: f.en || EN_FIN[f.cat] || f.k, a: f.a || (c && c.a), b: f.b || (c && c.b), w: f.w || (c && c.size), price: f.price || (c && c.price) || null };
}).filter((f) => f.a);

// sixteen wall colours with plain names (no brand names)
const PAINTS = [
  ['#F3F4F1', 'לבן נקי', 'Clean white'], ['#ECE8DE', 'לבן שבור', 'Off white'], ['#D6D8D7', 'אפור בהיר', 'Light grey'], ['#ABAEAA', 'אפור אבן', 'Stone grey'],
  ['#5A5E61', 'אפור פחם', 'Charcoal grey'], ['#2C2E30', 'שחור רך', 'Soft black'], ['#CBDCE5', 'תכלת עדין', 'Pale blue'], ['#8D9EAE', 'כחול אפרפר', 'Grey blue'],
  ['#3F5D77', 'כחול ים', 'Sea blue'], ['#A9B6A1', 'ירוק מרווה', 'Sage green'], ['#707655', 'ירוק זית', 'Olive green'], ['#30493F', 'ירוק בקבוק', 'Bottle green'],
  ['#D9CCB4', 'חול', 'Sand'], ['#EAD8A6', 'צהוב חמאה', 'Butter yellow'], ['#C9A6A0', 'ורוד עתיק', 'Dusty pink'], ['#8B6F5B', 'אדמה', 'Earth'],
].map(([hex, he, en]) => ({ hex, he, en }));

function ensureFonts() { // a font must be declared in the document itself; a shadow root cannot load one
  if (document.querySelector('link[data-nd-fonts]')) return;
  const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = FONTS; l.setAttribute('data-nd-fonts', ''); document.head.appendChild(l);
}
const mkCanvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };

/** the price range to show for one published record (where most sources sit when known, else the full span) */
function span(p) {
  if (!p) return null;
  const t = p.typical_low != null && p.typical_high != null;
  return { lo: t ? p.typical_low : p.low, hi: t ? p.typical_high : p.high };
}

// ======================================================================= the sample room
/**
 * Paints a believable room by ray casting a box room (floor, three walls, ceiling, a window with a sun patch on the floor,
 * a door, a picture) and drawing a sofa and a table on it. Returns the picture and its exact geometry: the floor corners to
 * mark, the furniture outlines, the true measures, and where the sun patch is. The local check uses it with its own camera.
 * o = { w, h, lens (x long side), pos [x,y,z] cm, yaw, pitch (degrees), oldFloor: 'tile' | 'wood', wall: hex }
 */
export function paintRoom(o = {}) {
  const w = o.w || 2400, h = o.h || 1800, Lside = Math.max(w, h);
  const R = { W: 420, D: 520, H: 270 };
  const cam = W.camera({ w, h, f: (o.lens || 0.75) * Lside, pos: o.pos || [210, -40, 150], yaw: (o.yaw || 0) * DEG, pitch: (o.pitch ?? -10) * DEG });
  const C = cam.pos, win = { y0: 200, y1: 330, z0: 100, z1: 210, mull: 265 };
  const sl = Math.hypot(1, 0.3, 1.1), sun = [1 / sl, 0.3 / sl, -1.1 / sl];
  const foot = [[325, 415, 220, 430], [190, 280, 150, 205]];
  const old = o.oldFloor === 'wood'
    ? W.makePattern({ tex: 'wood', pw: 9, pl: 60, a: '#7A5537', b: '#5B3C26' })
    : W.makePattern({ tex: 'tile', w: 45, h: 45, g: 0.5, a: '#CEC7BA', b: '#B3AB9D', grout: '#8E887E', tv: 0.12 });
  const wallLin = W.hexToLinear(o.wall || '#E8E7E3'), ceilLin = W.hexToLinear('#EFEFED');
  const doorLin = W.hexToLinear('#7C8186'), frameLin = W.hexToLinear('#4E5357'), picLin = [W.hexToLinear('#22313F'), W.hexToLinear('#C3A35A'), W.hexToLinear('#8FA7B5')];
  const skyTop = W.hexToLinear('#B9D3E8'), skyLow = W.hexToLinear('#F1F3EF');
  const cv = mkCanvas(w, h), ctx = cv.getContext('2d'), img = ctx.createImageData(w, h), d = img.data, col = [0, 0, 0];
  const ex = Math.exp;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const r = cam.ray(x + 0.5, y + 0.5);
      let t = Infinity, s = -1;
      if (r[2] < 0) { const k = -C[2] / r[2]; if (k < t) { t = k; s = 0; } }
      if (r[2] > 0) { const k = (R.H - C[2]) / r[2]; if (k < t) { t = k; s = 1; } }
      if (r[0] < 0) { const k = -C[0] / r[0]; if (k < t) { t = k; s = 2; } }
      if (r[0] > 0) { const k = (R.W - C[0]) / r[0]; if (k < t) { t = k; s = 3; } }
      if (r[1] > 0) { const k = (R.D - C[1]) / r[1]; if (k < t) { t = k; s = 4; } }
      const X = C[0] + r[0] * t, Y = C[1] + r[1] * t, Z = C[2] + r[2] * t, rl = Math.hypot(r[0], r[1], r[2]);
      let lr, lg, lb;
      if (s === 0) { // floor
        const fp = (t * rl) / cam.f / Math.max(0.15, Math.abs(r[2]) / rl);
        old(X, Y, fp, fp, col);
        let lt = 0.48 + 0.4 * ex(-Math.hypot(X, Y - 265) / 230);
        const sk = X / sun[0], Yw = Y - sk * sun[1], Zw = -sk * sun[2];
        const e = Math.min(Yw - win.y0, win.y1 - Yw, Zw - win.z0, win.z1 - Zw);
        lt += 1.7 * W.clamp01(e / 5 + 0.5) * W.clamp01((Math.abs(Yw - win.mull) - 3) / 3 + 0.5);
        let ao = (1 - 0.32 * ex(-X / 18)) * (1 - 0.32 * ex(-(R.W - X) / 18)) * (1 - 0.36 * ex(-(R.D - Y) / 18));
        for (const f of foot) { const dx = Math.max(f[0] - X, 0, X - f[1]), dy = Math.max(f[2] - Y, 0, Y - f[3]), dd = Math.hypot(dx, dy); ao *= 1 - 0.5 * ex(-dd / 8) - 0.16 * ex(-dd / 40); }
        lt *= ao * 0.86; lr = col[0] * lt; lg = col[1] * lt; lb = col[2] * lt;
      } else if (s === 1) { // ceiling
        let lt = (0.62 - 0.14 * (Y / R.D)) * (1 - 0.25 * ex(-X / 25)) * (1 - 0.25 * ex(-(R.W - X) / 25)) * (1 - 0.3 * ex(-(R.D - Y) / 25));
        if (Math.hypot(X - 210, Y - 330) < 16) lt = 1.25;
        lr = ceilLin[0] * lt; lg = ceilLin[1] * lt; lb = ceilLin[2] * lt;
      } else if (s === 2) { // the window wall: in its own shadow
        let lt = (0.36 + 0.1 * (Z / R.H)) * (1 - 0.3 * ex(-Z / 16)) * (1 - 0.25 * ex(-(R.H - Z) / 20)) * (1 - 0.3 * ex(-(R.D - Y) / 20));
        let c = wallLin;
        if (Y > win.y0 && Y < win.y1 && Z > win.z0 && Z < win.z1) {
          const fe = Math.min(Y - win.y0, win.y1 - Y, Z - win.z0, win.z1 - Z);
          if (fe < 5 || Math.abs(Y - win.mull) < 2.5) { c = frameLin; lt = 0.5; }
          else { const k = (Z - win.z0) / (win.z1 - win.z0); c = [skyLow[0] + (skyTop[0] - skyLow[0]) * k, skyLow[1] + (skyTop[1] - skyLow[1]) * k, skyLow[2] + (skyTop[2] - skyLow[2]) * k]; lt = 1.05; }
        } else if (Z < 9) lt *= 0.82;
        lr = c[0] * lt; lg = c[1] * lt; lb = c[2] * lt;
      } else if (s === 3) { // the wall facing the window
        let lt = (0.74 + 0.12 * ex(-Math.abs(Y - 290) / 160)) * (1 - 0.3 * ex(-Z / 16)) * (1 - 0.25 * ex(-(R.H - Z) / 20)) * (1 - 0.3 * ex(-(R.D - Y) / 20));
        let c = wallLin;
        if (Y > 250 && Y < 370 && Z > 128 && Z < 196) {
          const fe = Math.min(Y - 250, 370 - Y, Z - 128, 196 - Z);
          c = fe < 3 ? picLin[0] : Y < 300 ? picLin[2] : Z > 165 ? picLin[1] : picLin[0];
          if (fe >= 3) lt *= 0.95;
        } else if (Z < 9) lt *= 0.84;
        lr = c[0] * lt; lg = c[1] * lt; lb = c[2] * lt;
      } else if (s === 4) { // the wall in front
        let lt = (0.56 + 0.22 * ex(-X / 170)) * (1 - 0.3 * ex(-X / 18)) * (1 - 0.3 * ex(-(R.W - X) / 18)) * (1 - 0.3 * ex(-Z / 16)) * (1 - 0.25 * ex(-(R.H - Z) / 20));
        let c = wallLin;
        if (X > 290 && X < 385 && Z < 212) {
          const fe = Math.min(X - 290, 385 - X, 212 - Z);
          c = fe < 4 ? frameLin : doorLin;
          if (Math.hypot(X - 300, Z - 100) < 2.5) { c = W.hexToLinear('#D7D9DA'); lt *= 1.2; }
        } else if (Z < 9) lt *= 0.84;
        lr = c[0] * lt; lg = c[1] * lt; lb = c[2] * lt;
      } else { lr = lg = lb = 0.5; }
      const vx = (x - w / 2) / Lside, vy = (y - h / 2) / Lside, vig = 1 - 0.32 * (vx * vx + vy * vy), nz = 1 + (W.hash(x * 7 + 3, y * 13 + 1) - 0.5) * 0.035;
      const j = (y * w + x) * 4;
      d[j] = W.linearToSrgb(W.shoulder(lr * vig * nz)); d[j + 1] = W.linearToSrgb(W.shoulder(lg * vig * nz)); d[j + 2] = W.linearToSrgb(W.shoulder(lb * vig * nz)); d[j + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  // furniture: boxes, the faces that look at the camera, far ones first; lit from the window side
  const box = (x0, x1, y0, y1, z0, z1, hex) => ({ x0, x1, y0, y1, z0, z1, hex });
  const sofa = [box(325, 415, 220, 430, 0, 42, '#46555E'), box(395, 415, 220, 430, 42, 90, '#4A5962'), box(325, 395, 220, 240, 42, 64, '#4A5962'), box(325, 395, 410, 430, 42, 64, '#4A5962'),
    box(330, 395, 241, 325, 42, 55, '#56666F'), box(330, 395, 325, 409, 42, 55, '#56666F'), box(380, 396, 250, 300, 55, 88, '#5C6C74'), box(380, 396, 350, 400, 55, 88, '#5C6C74')];
  const table = [box(190, 280, 150, 205, 30, 38, '#D3C7B2'), box(195, 275, 155, 200, 0, 30, '#E4E3DF')];
  const lightDir = (() => { const v = [-1, -0.2, 0.55], n = Math.hypot(...v); return v.map((a) => a / n); })();
  const faces = [];
  for (const b of [...sofa, ...table]) {
    const V = (x, y, z) => [x ? b.x1 : b.x0, y ? b.y1 : b.y0, z ? b.z1 : b.z0];
    const F = [[[-1, 0, 0], [V(0, 0, 0), V(0, 1, 0), V(0, 1, 1), V(0, 0, 1)]], [[1, 0, 0], [V(1, 0, 0), V(1, 1, 0), V(1, 1, 1), V(1, 0, 1)]],
      [[0, -1, 0], [V(0, 0, 0), V(1, 0, 0), V(1, 0, 1), V(0, 0, 1)]], [[0, 1, 0], [V(0, 1, 0), V(1, 1, 0), V(1, 1, 1), V(0, 1, 1)]], [[0, 0, 1], [V(0, 0, 1), V(1, 0, 1), V(1, 1, 1), V(0, 1, 1)]]];
    for (const [n, vs] of F) {
      const cx = vs.reduce((a, v) => a + v[0], 0) / 4, cy = vs.reduce((a, v) => a + v[1], 0) / 4, cz = vs.reduce((a, v) => a + v[2], 0) / 4;
      if (n[0] * (C[0] - cx) + n[1] * (C[1] - cy) + n[2] * (C[2] - cz) <= 0) continue;
      const lit = 0.38 + 0.55 * Math.max(0, n[0] * lightDir[0] + n[1] * lightDir[1] + n[2] * lightDir[2]) + (n[2] > 0 ? 0.12 : 0);
      faces.push({ dist: Math.hypot(cx - C[0], cy - C[1], cz - C[2]), pts: vs.map((v) => cam.project(v)), hex: b.hex, lit, zlow: Math.min(...vs.map((v) => v[2])) });
    }
  }
  faces.sort((a, b) => b.dist - a.dist);
  for (const f of faces) {
    const c = W.hexToLinear(f.hex).map((v) => W.linearToSrgb(v * f.lit));
    ctx.beginPath(); f.pts.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.closePath();
    ctx.fillStyle = 'rgb(' + c.join(',') + ')'; ctx.fill();
    ctx.strokeStyle = 'rgba(20,24,28,.35)'; ctx.lineWidth = Math.max(1, Lside / 1600); ctx.stroke();
  }
  const clipRect = (poly, x0, y0, x1, y1) => { // Sutherland-Hodgman: the outline as far as it can be tapped on the photo
    const edge = (pts, inside, cut) => { const o = []; pts.forEach((p, i) => { const q = pts[(i + pts.length - 1) % pts.length], a = inside(p), b = inside(q); if (a) { if (!b) o.push(cut(q, p)); o.push(p); } else if (b) o.push(cut(q, p)); }); return o; };
    const atX = (X) => (q, p) => [X, q[1] + ((p[1] - q[1]) * (X - q[0])) / (p[0] - q[0])], atY = (Y) => (q, p) => [q[0] + ((p[0] - q[0]) * (Y - q[1])) / (p[1] - q[1]), Y];
    let r = edge(poly, (p) => p[0] >= x0, atX(x0)); r = edge(r, (p) => p[0] <= x1, atX(x1)); r = edge(r, (p) => p[1] >= y0, atY(y0)); return edge(r, (p) => p[1] <= y1, atY(y1));
  };
  const hull = (boxes) => clipRect(W.convexHull(boxes.flatMap((b) => [0, 1].flatMap((i) => [0, 1].flatMap((j) => [0, 1].map((k) => cam.project([i ? b.x1 : b.x0, j ? b.y1 : b.y0, k ? b.z1 : b.z0]).slice(0, 2)))))), -0.04 * w, -0.04 * h, 1.04 * w, 1.04 * h);
  // the near edge of the marked rectangle: the nearest depth at which both side walls still meet the floor inside the photo
  let nearY = R.D - 60;
  for (let Y = 0; Y < R.D - 60; Y += 5) {
    const a = cam.project([0, Y, 0]), b = cam.project([R.W, Y, 0]), m = 0.02 * Lside;
    if (a[2] > 0 && b[2] > 0 && a[0] > m && b[0] < w - m && a[1] < h - m && b[1] < h - m && a[0] < w && b[0] > 0) { nearY = Y; break; }
  }
  const P = (X, Y, Z = 0) => cam.project([X, Y, Z]).slice(0, 2);
  return {
    canvas: cv, w, h, cam, room: R, nearY,
    corners: [P(0, R.D), P(R.W, R.D), P(R.W, nearY), P(0, nearY)], width: R.W, depth: R.D - nearY,
    furniture: [hull(sofa), hull(table)], footprints: foot,
    sunAt: P(141, 307), shadeAt: P(141, 470), backWall: [P(0, R.D, 0), P(R.W, R.D, 0), P(R.W, R.D, R.H), P(0, R.D, R.H)],
    project: P,
  };
}

// ======================================================================= the tool
export async function mountRoomPhoto(host, opts = {}) {
  const lang = opts.lang === 'en' ? 'en' : 'he', T = TXT[lang], fine = strings(lang).budFine;
  const nf = new Intl.NumberFormat(lang === 'en' ? 'en-US' : 'he-IL');
  const nf1 = new Intl.NumberFormat(lang === 'en' ? 'en-US' : 'he-IL', { maximumFractionDigits: 1, minimumFractionDigits: 1 });
  ensureFonts();
  const shadow = host.shadowRoot || host.attachShadow({ mode: 'open' });
  shadow.textContent = '';
  const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = BASE + 'roomphoto.css?v=' + (opts.version || '1');
  const root = document.createElement('div'); root.className = 'rp'; root.dir = T.dir; root.lang = lang;
  const touch = typeof matchMedia === 'function' && matchMedia('(pointer: coarse)').matches;
  const tabs = ['corners', 'furniture', 'size', 'finish', 'wall', 'result'];
  root.innerHTML =
    '<div class="box pre"><header><div><h2>' + esc(T.title) + '</h2><p data-r="sub"></p></div><button class="btn hb" data-a="new" hidden>' + esc(T.newPhoto) + '</button></header>' +
    '<section class="stage" data-r="stage" aria-label="' + esc(T.stage) + '"><canvas data-r="cv"></canvas>' +
    '<div class="start" data-r="start"><div class="in"><p class="lead">' + esc(T.lead) + '</p>' +
    '<div class="acts"><button class="btn go" data-a="pick">' + esc(T.pick) + '</button>' + (touch ? '<button class="btn" data-a="shoot">' + esc(T.shoot) + '</button>' : '') + '</div>' +
    '<p class="priv">' + esc(T.privacy) + '</p><p class="tip">' + esc(T.tip) + '</p><button class="btn link" data-a="sample">' + esc(T.sample) + '</button></div></div>' +
    '<p class="busy" data-r="busy" hidden></p></section>' +
    '<nav data-r="nav" aria-label="' + esc(T.tabsL) + '" hidden>' + tabs.map((k) => '<button data-step="' + k + '">' + esc(T.tabs[k]) + '</button>').join('') + '</nav>' +
    '<section class="panel" data-r="panel" hidden></section>' +
    '<input type="file" accept="image/*" data-r="file" hidden><input type="file" accept="image/*" capture="environment" data-r="cam" hidden>' +
    '<div class="toast" data-r="toast" role="status" hidden></div></div>';
  shadow.append(css, root);
  const $ = (k) => root.querySelector('[data-r="' + k + '"]');
  await new Promise((r) => { if (css.sheet) r(); else { css.addEventListener('load', r, { once: true }); css.addEventListener('error', r, { once: true }); } });

  const cv = $('cv'), ctx = cv.getContext('2d'), stage = $('stage');
  let alive = true, prices = null, toastT = 0;
  fetch(BASE + 'data/price-ranges.json?v=' + (opts.version || '1')).then((r) => (r.ok ? r.json() : null)).then((j) => { prices = j && j.items; if (alive && step !== 'start') panel(); }).catch(() => {});

  // ---- state
  let step = 'start', iw = 0, ih = 0, srcCanvas = null, srcData = null, L = null, after = null, afterCtx = null, afterData = null, maskCtx = null;
  let corners = [], furniture = [], walls = [], draft = [], width = null, depth = null;
  let finish = FLOORS[0].k, rot = 0, off = [0, 0], moveMode = false, paint = null, split = 0.5;
  let frame = null, floorMask = null, light = null, lref = 0.2, wallMask = null, wref = 0.5;
  let floorDirty = true, wallDirty = true, hasAfter = false, drag = null, raf = 0, busyN = 0, renders = 0, lastSave = null;
  const typed = {}; // what is being typed in the size fields, kept across redraws of the panel
  const timings = {}, view = { s: 1, ox: 0, oy: 0, dpr: 1, cw: 0, ch: 0 }, pats = {}, swatches = {};
  const pat = (k) => pats[k] || (pats[k] = W.makePattern(FLOORS.find((f) => f.k === k)));

  const toast = (msg) => { const t = $('toast'); t.textContent = msg; t.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => (t.hidden = true), 3400); };
  const setBusy = (msg) => { const b = $('busy'); if (msg) { busyN++; b.textContent = msg; b.hidden = false; } else { busyN = Math.max(0, busyN - 1); if (!busyN) b.hidden = true; } };
  const tick = () => new Promise((r) => requestAnimationFrame(() => setTimeout(r, 0)));

  // ---- loading a photo
  async function loadFile(file) {
    if (!file) return;
    setBusy(T.loading); await tick();
    const t0 = performance.now();
    let src = null, sw = 0, sh = 0;
    try { src = await createImageBitmap(file, { imageOrientation: 'from-image' }); sw = src.width; sh = src.height; }
    catch (e) {
      try { const url = URL.createObjectURL(file); const im = new Image(); im.src = url; await im.decode(); src = im; sw = im.naturalWidth; sh = im.naturalHeight; setTimeout(() => URL.revokeObjectURL(url), 1000); }
      catch (e2) { src = null; }
    }
    if (!alive) return;
    if (!src || !sw || !sh) { setBusy(); toast(T.badFile); return; }
    setImage(src, sw, sh);
    if (src.close) src.close();
    timings.load_ms = Math.round(performance.now() - t0);
    setBusy();
    go('corners');
  }
  function setImage(src, sw, sh) {
    const k = Math.min(1, MAX_SIDE / Math.max(sw, sh));
    iw = Math.max(1, Math.round(sw * k)); ih = Math.max(1, Math.round(sh * k));
    srcCanvas = mkCanvas(iw, ih);
    const sc = srcCanvas.getContext('2d', { willReadFrequently: true });
    sc.imageSmoothingQuality = 'high'; sc.drawImage(src, 0, 0, iw, ih);
    srcData = sc.getImageData(0, 0, iw, ih);
    L = W.luminance(srcData.data, iw * ih);
    after = mkCanvas(iw, ih); afterCtx = after.getContext('2d'); afterData = afterCtx.createImageData(iw, ih);
    maskCtx = mkCanvas(iw, ih).getContext('2d', { willReadFrequently: true });
    delete typed.win; delete typed.din;
    corners = []; furniture = []; walls = []; draft = []; width = null; depth = null; off = [0, 0]; rot = 0; paint = null; moveMode = false; split = 0.5;
    frame = null; floorMask = null; light = null; wallMask = null; floorDirty = wallDirty = true; hasAfter = false;
    $('start').hidden = true; root.querySelector('[data-a="new"]').hidden = false;
  }
  async function loadSample() {
    setBusy(T.working); await tick();
    const t0 = performance.now(), room = paintRoom({ w: 1600, h: 1200 }); // smaller than a photo: it opens fast on a phone
    if (!alive) return;
    setImage(room.canvas, room.w, room.h);
    corners = room.corners.map((p) => [...p]); furniture = room.furniture.map((p) => p.map((q) => [...q]));
    width = room.width; depth = room.depth;
    timings.sample_ms = Math.round(performance.now() - t0);
    setBusy();
    go('finish');
    toast(T.sampleNote);
  }

  // ---- the work: masks, light, the new picture
  function polyMask(incl, excl) {
    const c = maskCtx;
    c.globalCompositeOperation = 'source-over'; c.clearRect(0, 0, iw, ih); c.fillStyle = '#fff';
    const fill = (p) => { c.beginPath(); p.forEach((q, i) => (i ? c.lineTo(q[0], q[1]) : c.moveTo(q[0], q[1]))); c.closePath(); c.fill(); };
    incl.forEach(fill);
    c.globalCompositeOperation = 'destination-out'; excl.forEach(fill); c.globalCompositeOperation = 'source-over';
    const d = c.getImageData(0, 0, iw, ih).data, m = new Uint8Array(iw * ih);
    for (let i = 0; i < m.length; i++) m[i] = d[i * 4 + 3];
    return W.featherMask(m, iw, ih, Math.max(1, Math.round(Math.max(iw, ih) / 1400)));
  }
  function prepFloor() {
    floorDirty = false;
    if (corners.length !== 4) { frame = null; return; }
    const t0 = performance.now();
    const fr = W.floorFrame(corners, iw, ih, { width, depth });
    if (!fr) { frame = null; floorMask = null; toast(T.badQuad); return; }
    frame = fr;
    floorMask = polyMask([W.floorRegion(fr.quad, iw, ih)], furniture);
    // wide enough to wash out the old floor's own boards and tiles; shadows and a sun patch are larger and stay
    const r = W.floorLight(L, floorMask, iw, ih, Math.max(4, Math.round(Math.max(iw, ih) * 0.026)));
    light = r.light; lref = r.ref;
    timings.prep_ms = Math.round(performance.now() - t0);
  }
  function prepWall() {
    wallDirty = false;
    if (!walls.length) { wallMask = null; return; }
    const t0 = performance.now();
    wallMask = polyMask(walls, furniture);
    wref = W.maskMedian(L, wallMask);
    timings.wall_ms = Math.round(performance.now() - t0);
  }
  function render(stepPx) {
    const t0 = performance.now(), out = afterData.data;
    out.set(srcData.data);
    let any = false;
    if (wallMask && paint != null) { W.paintWall({ out, mask: wallMask, L, ref: wref, color: W.hexToLinear(PAINTS[paint].hex), n: iw * ih }); any = true; }
    if (frame && floorMask && finish) {
      W.renderFloor({ out, w: iw, h: ih, mask: floorMask, light, ref: lref, H: frame.H, pattern: pat(finish), rot: rot * DEG, origin: [frame.W / 2 + off[0], off[1]], step: stepPx });
      any = true;
    }
    afterCtx.putImageData(afterData, 0, 0);
    hasAfter = any;
    if (stepPx === 1) { timings.render_ms = Math.round(performance.now() - t0); renders++; }
  }
  /** redraw the new picture; heavy work (new marks) shows a "drawing" line first so the phone does not look frozen */
  let pending = null;
  function update(preview) {
    if (!srcData) return;
    if (pending) { pending.preview = pending.preview && preview; return; }
    pending = { preview };
    const heavy = floorDirty || wallDirty;
    const run = () => {
      const p = pending; pending = null;
      if (!alive || !srcData) return;
      if (floorDirty) prepFloor();
      if (wallDirty) prepWall();
      render(p.preview ? 2 : 1);
      if (heavy) setBusy();
      draw();
      if (step !== 'start') panel(true);
    };
    if (heavy && !preview) { setBusy(T.working); requestAnimationFrame(() => setTimeout(run, 0)); }
    else requestAnimationFrame(run);
  }

  // ---- the stage
  function fit() {
    const r = stage.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 3);
    const cw = Math.max(1, Math.round(r.width)), ch = Math.max(1, Math.round(r.height));
    if (cv.width !== Math.round(cw * dpr) || cv.height !== Math.round(ch * dpr)) { cv.width = Math.round(cw * dpr); cv.height = Math.round(ch * dpr); }
    view.dpr = dpr; view.cw = cw; view.ch = ch;
    if (iw) { const m = 14, s = Math.min((cw - 2 * m) / iw, (ch - 2 * m) / ih); view.s = s; view.ox = (cw - iw * s) / 2; view.oy = (ch - ih * s) / 2; }
  }
  const toV = (p) => [view.ox + p[0] * view.s, view.oy + p[1] * view.s];
  const toImg = (v) => [(v[0] - view.ox) / view.s, (v[1] - view.oy) / view.s];
  const clampImg = (p) => [Math.min(iw * 1.08, Math.max(-iw * 0.08, p[0])), Math.min(ih * 1.08, Math.max(-ih * 0.08, p[1]))];
  const path = (pts, close) => { ctx.beginPath(); pts.forEach((p, i) => { const v = toV(p); if (i) ctx.lineTo(v[0], v[1]); else ctx.moveTo(v[0], v[1]); }); if (close) ctx.closePath(); };
  let hatch = null;
  function draw() {
    if (!alive) return;
    fit();
    const { dpr, cw, ch, s, ox, oy } = view;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, cw, ch);
    if (!srcCanvas || step === 'start') return;
    ctx.imageSmoothingQuality = 'high';
    const showAfter = hasAfter && step !== 'corners' && step !== 'size';
    ctx.drawImage(showAfter ? after : srcCanvas, ox, oy, iw * s, ih * s);
    if (step === 'result') {
      const sx = ox + split * iw * s, rtl = T.dir === 'rtl';
      ctx.save(); ctx.beginPath();
      if (rtl) ctx.rect(sx, oy, ox + iw * s - sx, ih * s); else ctx.rect(ox, oy, sx - ox, ih * s);
      ctx.clip(); ctx.drawImage(srcCanvas, ox, oy, iw * s, ih * s); ctx.restore();
      ctx.fillStyle = '#fff'; ctx.fillRect(sx - 1.5, oy, 3, ih * s);
      ctx.strokeStyle = '#0F2233'; ctx.lineWidth = 1; ctx.strokeRect(sx - 2, oy, 4, ih * s);
      const hy = oy + ih * s / 2;
      ctx.fillStyle = '#0F2233'; ctx.fillRect(sx - 15, hy - 24, 30, 48);
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(sx - 5, hy - 7); ctx.lineTo(sx - 10, hy); ctx.lineTo(sx - 5, hy + 7); ctx.moveTo(sx + 5, hy - 7); ctx.lineTo(sx + 10, hy); ctx.lineTo(sx + 5, hy + 7); ctx.stroke();
      const tag = (txt, x, alignEnd) => { ctx.font = '600 13px "IBM Plex Sans Hebrew",Arial,sans-serif'; const tw = ctx.measureText(txt).width + 16; const bx = alignEnd ? x - tw : x; ctx.fillStyle = '#0F2233'; ctx.fillRect(bx, oy + 8, tw, 26); ctx.fillStyle = '#fff'; ctx.textBaseline = 'middle'; ctx.textAlign = 'center'; ctx.fillText(txt, bx + tw / 2, oy + 21); };
      const bl = rtl ? T.after : T.before, br = rtl ? T.before : T.after;
      tag(bl, ox + 8, false); tag(br, ox + iw * s - 8, true);
      return;
    }
    // the floor outline
    const q = corners.length === 4 ? W.orderFloor(corners) : null;
    if (step === 'corners') {
      if (q) {
        const reg = W.floorRegion(q, iw, ih);
        ctx.fillStyle = 'rgba(31,95,168,.16)'; path(reg, true); ctx.fill();
        ctx.setLineDash([8, 6]); ctx.strokeStyle = '#1F5FA8'; ctx.lineWidth = 2; path([q[1], reg[2]]); ctx.stroke(); path([q[0], reg[3]]); ctx.stroke(); ctx.setLineDash([]);
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; path(q, true); ctx.stroke(); ctx.strokeStyle = '#1F5FA8'; ctx.lineWidth = 2; path(q, true); ctx.stroke();
      } else if (corners.length > 1) {
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; path(corners); ctx.stroke(); ctx.strokeStyle = '#1F5FA8'; ctx.lineWidth = 2; path(corners); ctx.stroke();
      }
      corners.forEach((p, i) => handle(p, drag && drag.list === corners && drag.i === i));
    }
    if (step === 'size' && q) { // the far edge in dimension red: this is the width being asked for
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 6; path([q[0], q[1]]); ctx.stroke();
      ctx.strokeStyle = '#B5302A'; ctx.lineWidth = 3; path([q[0], q[1]]); ctx.stroke();
      const a = toV(q[0]), b = toV(q[1]);
      for (const v of [a, b]) { ctx.fillStyle = '#B5302A'; ctx.fillRect(v[0] - 2, v[1] - 9, 4, 18); }
      const lbl = width ? nf.format(width) + ' ' + T.cm : T.width;
      ctx.font = '600 14px "IBM Plex Mono",monospace'; const tw = ctx.measureText(lbl).width + 14, mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2 - 24;
      ctx.fillStyle = '#fff'; ctx.fillRect(mx - tw / 2, my - 13, tw, 26); ctx.strokeStyle = '#B5302A'; ctx.lineWidth = 2; ctx.strokeRect(mx - tw / 2, my - 13, tw, 26);
      ctx.fillStyle = '#B5302A'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(lbl, mx, my);
    }
    if (step === 'furniture' || step === 'wall') {
      const polys = step === 'furniture' ? furniture : walls;
      if (!hatch) { const hc = mkCanvas(10, 10), hx = hc.getContext('2d'); hx.strokeStyle = 'rgba(15,34,51,.55)'; hx.lineWidth = 1.5; hx.beginPath(); hx.moveTo(0, 10); hx.lineTo(10, 0); hx.stroke(); hatch = ctx.createPattern(hc, 'repeat'); }
      for (const p of polys) {
        if (step === 'furniture') { ctx.fillStyle = hatch; path(p, true); ctx.fill(); }
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; path(p, true); ctx.stroke();
        ctx.strokeStyle = step === 'furniture' ? '#0F2233' : '#1F5FA8'; ctx.lineWidth = 2; ctx.setLineDash([7, 5]); path(p, true); ctx.stroke(); ctx.setLineDash([]);
        p.forEach((pt, i) => handle(pt, drag && drag.list === p && drag.i === i, true));
      }
      if (draft.length) {
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 4; path(draft); ctx.stroke(); ctx.strokeStyle = '#1F5FA8'; ctx.lineWidth = 2; path(draft); ctx.stroke();
        draft.forEach((p, i) => handle(p, drag && drag.list === draft && drag.i === i, false, i === 0 && draft.length >= 3));
      }
    }
    if (drag && drag.kind === 'pt' && !(drag.closeOnTap && !drag.moved)) loupe(drag.v, drag.list[drag.i]);
  }
  function handle(p, on, small, first) {
    const v = toV(p), r = small ? 6 : 8;
    if (first) { ctx.strokeStyle = '#1F5FA8'; ctx.lineWidth = 2; ctx.strokeRect(v[0] - 13, v[1] - 13, 26, 26); }
    ctx.fillStyle = on ? '#1F5FA8' : '#fff'; ctx.fillRect(v[0] - r, v[1] - r, 2 * r, 2 * r);
    ctx.strokeStyle = '#0F2233'; ctx.lineWidth = 2; ctx.strokeRect(v[0] - r, v[1] - r, 2 * r, 2 * r);
  }
  function loupe(v, p) { // a square magnifier above the finger: the point being set is under its cross
    const S = 124, Z = 3, { cw, s } = view;
    let bx = v[0] - S / 2, by = v[1] - S - 46;
    if (by < 6) by = v[1] + 46;
    bx = Math.max(6, Math.min(cw - S - 6, bx));
    const rw = S / (s * Z);
    ctx.save(); ctx.beginPath(); ctx.rect(bx, by, S, S); ctx.clip();
    ctx.fillStyle = '#E6ECF0'; ctx.fillRect(bx, by, S, S);
    ctx.drawImage(srcCanvas, p[0] - rw / 2, p[1] - rw / 2, rw, rw, bx, by, S, S);
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(bx + S / 2, by + 8); ctx.lineTo(bx + S / 2, by + S - 8); ctx.moveTo(bx + 8, by + S / 2); ctx.lineTo(bx + S - 8, by + S / 2); ctx.stroke();
    ctx.strokeStyle = '#1F5FA8'; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.restore();
    ctx.strokeStyle = '#0F2233'; ctx.lineWidth = 2; ctx.strokeRect(bx, by, S, S);
  }

  // ---- fingers and mouse on the photo (touch-action:none is on the photo only)
  const viewPt = (e) => { const r = cv.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  const hitIndex = (pts, v, tol = 26) => { let best = -1, bd = tol; pts.forEach((p, i) => { const q = toV(p), d = Math.hypot(q[0] - v[0], q[1] - v[1]); if (d < bd) { bd = d; best = i; } }); return best; };
  function down(e) {
    if (!srcData || (e.button != null && e.button > 0)) return;
    const v = viewPt(e), p = clampImg(toImg(v));
    let d = null;
    if (step === 'corners') {
      const k = hitIndex(corners, v);
      if (k >= 0) d = { kind: 'pt', list: corners, i: k };
      else if (corners.length < 4) { corners.push(p); d = { kind: 'pt', list: corners, i: corners.length - 1, added: true }; }
    } else if (step === 'furniture' || step === 'wall') {
      const polys = step === 'furniture' ? furniture : walls, k = hitIndex(draft, v);
      if (k >= 0) d = { kind: 'pt', list: draft, i: k, closeOnTap: k === 0 && draft.length >= 3 };
      else {
        if (!draft.length) for (const poly of polys) { const kk = hitIndex(poly, v, 14); if (kk >= 0) { d = { kind: 'pt', list: poly, i: kk, committed: step }; break; } }
        if (!d) { draft.push(p); d = { kind: 'pt', list: draft, i: draft.length - 1, added: true }; }
      }
    } else if (step === 'finish' && moveMode && frame) d = { kind: 'origin', last: W.apply(frame.H, p[0], p[1]) };
    else if (step === 'result') { d = { kind: 'split' }; split = Math.min(1, Math.max(0, (v[0] - view.ox) / (iw * view.s))); }
    if (!d) return;
    e.preventDefault();
    try { cv.setPointerCapture(e.pointerId); } catch (err) { /* a synthetic pointer */ }
    d.id = e.pointerId; d.v0 = v; d.v = v; d.moved = false; drag = d;
    draw();
  }
  function move(e) {
    if (!drag || e.pointerId !== drag.id) return;
    e.preventDefault();
    const v = viewPt(e);
    if (Math.hypot(v[0] - drag.v0[0], v[1] - drag.v0[1]) > 5) drag.moved = true;
    drag.v = v;
    if (drag.kind === 'pt') { if (!(drag.closeOnTap && !drag.moved)) drag.list[drag.i] = clampImg(toImg(v)); draw(); }
    else if (drag.kind === 'origin') {
      const p = toImg(v), q = W.apply(frame.H, p[0], p[1]);
      if (q && drag.last) { off[0] += q[0] - drag.last[0]; off[1] += q[1] - drag.last[1]; }
      drag.last = q; update(true);
    } else if (drag.kind === 'split') { split = Math.min(1, Math.max(0, (v[0] - view.ox) / (iw * view.s))); draw(); }
  }
  function up(e) {
    if (!drag || e.pointerId !== drag.id) return;
    const d = drag; drag = null;
    if (d.kind === 'pt') {
      if (d.closeOnTap && !d.moved) closeDraft();
      else if (d.list === corners) { floorDirty = true; if (corners.length === 4) { if (!W.orderFloor(corners)) toast(T.badQuad); else update(); } }
      else if (d.committed) { floorDirty = true; wallDirty = true; update(); }
    } else if (d.kind === 'origin') update();
    draw(); panel(true);
  }
  cv.addEventListener('pointerdown', down);
  cv.addEventListener('pointermove', move);
  cv.addEventListener('pointerup', up);
  cv.addEventListener('pointercancel', up);
  function closeDraft() {
    if (draft.length < 3) return;
    (step === 'wall' ? walls : furniture).push(draft); draft = [];
    floorDirty = true; wallDirty = true; update(); panel();
  }

  // ---- the panel under (or beside) the photo
  const money = (v) => '<span class="mono">' + nf.format(v) + '</span>';
  function floorSize(f) {
    if (f.tex === 'concrete') return T.seamless;
    if (f.tex === 'wood' || f.tex === 'deck') return T.boards + ' <span class="mono">' + f.pw + '×' + f.pl + '</span> ' + T.cm;
    return '<span class="mono">' + (f.h && f.h !== f.w ? f.h + '×' + f.w : f.w + '×' + f.w) + '</span> ' + T.cm;
  }
  function floorPrice(f) {
    const s = prices && f.price ? span(prices[f.price]) : null;
    if (!s || s.lo == null || s.hi == null) return null;
    return { lo: Math.floor(s.lo / 10) * 10, hi: Math.ceil(s.hi / 10) * 10 };
  }
  function swatch(f) {
    if (swatches[f.k]) return swatches[f.k];
    const n = 60, c = mkCanvas(n, n), x = c.getContext('2d'), im = x.createImageData(n, n), p = pat(f.k), o = [0, 0, 0], cm = f.tex === 'wood' || f.tex === 'deck' ? 110 : f.tex === 'terrazzo' ? 60 : Math.max(130, (f.w || 60) * 1.8), fp = cm / n;
    for (let y = 0; y < n; y++) for (let xx = 0; xx < n; xx++) {
      p(xx * fp + 7, y * fp + 5, fp, fp, o); const j = (y * n + xx) * 4;
      im.data[j] = W.linearToSrgb(o[0] * 1.05); im.data[j + 1] = W.linearToSrgb(o[1] * 1.05); im.data[j + 2] = W.linearToSrgb(o[2] * 1.05); im.data[j + 3] = 255;
    }
    x.putImageData(im, 0, 0);
    return (swatches[f.k] = c.toDataURL());
  }
  function summary() {
    if (!frame) return '';
    if (!frame.measured) return '<p class="fine">' + esc(T.needSize) + '</p><button class="btn" data-a="tosize">' + esc(T.addSize) + '</button>';
    const f = FLOORS.find((x) => x.k === finish), a = frame.sqm, pr = f && floorPrice(f);
    let s = '<p class="sum"><b>' + T.area('<span class="mono dim">' + nf1.format(a) + '</span>') + '</b> · ';
    s += pr ? T.priceLine(money(Math.floor((pr.lo * a) / 100) * 100), money(Math.ceil((pr.hi * a) / 100) * 100)) : esc(T.noPriceLine);
    s += '</p>';
    if (!frame.depthMeasured) s += '<p class="fine">' + esc(T.depthGuess) + '</p>';
    if (pr) s += '<p class="fine">' + esc(fine) + '</p>';
    return s;
  }
  function draftControls(isWall) {
    if (!draft.length) return '';
    return '<p class="count">' + esc(isWall ? T.wallDraft(draft.length) : T.draftCount(draft.length)) + '</p><p class="fine">' + esc(T.closeTip) + '</p>' +
      '<div class="row"><button class="btn go" data-a="close"' + (draft.length < 3 ? ' disabled' : '') + '>' + esc(isWall ? T.wallDone : T.furnDone) + '</button><button class="btn" data-a="undopt">' + esc(T.undoPt) + '</button></div>';
  }
  function panel(soft) {
    const el = $('panel');
    root.firstChild.classList.toggle('pre', step === 'start');
    if (step === 'start') { el.hidden = true; return; }
    el.hidden = false;
    $('nav').hidden = false;
    root.querySelectorAll('nav [data-step]').forEach((b) => { b.setAttribute('aria-current', b.dataset.step === step ? 'step' : 'false'); b.disabled = b.dataset.step !== 'corners' && !frame; });
    const sub = $('sub'); sub.textContent = T.tabs[step];
    if (soft && el.dataset.step === step && shadow.activeElement && shadow.activeElement.tagName === 'INPUT') return; // never wipe a field being typed in
    if (soft && el.dataset.step === step && step !== 'corners' && step !== 'furniture' && step !== 'wall' && step !== 'finish' && step !== 'result') return; // keep a half-typed size field
    el.dataset.step = step;
    let h = '';
    if (step === 'corners') {
      h = '<h3>' + esc(T.cornersH) + '</h3><p>' + esc(T.cornersP) + '</p><p class="fine">' + esc(corners.length < 4 ? T.cornersTip : T.cornersDrag) + '</p>' +
        '<div class="row"><span class="count">' + esc(T.count(corners.length)) + '</span>' + (corners.length ? '<button class="btn" data-a="clearc">' + esc(T.again) + '</button>' : '') +
        '<button class="btn go" data-a="next"' + (frame ? '' : ' disabled') + '>' + esc(T.next) + '</button></div>';
    } else if (step === 'furniture') {
      h = '<h3>' + esc(T.furnH) + '</h3><p>' + esc(T.furnP) + '</p>' + draftControls(false) +
        (!draft.length ? '<div class="row"><span class="count">' + esc(T.furnCount(furniture.length)) + '</span>' + (furniture.length ? '<button class="btn" data-a="clearf">' + esc(T.furnClear) + '</button>' : '') + '<button class="btn go" data-a="next">' + esc(T.next) + '</button></div>' : '');
    } else if (step === 'size') {
      h = '<h3>' + esc(T.sizeH) + '</h3><p>' + esc(T.sizeP) + '</p><div class="fields"><label><span>' + esc(T.widthL) + '</span><input data-r="win" type="number" inputmode="numeric" min="100" max="3000" step="1" placeholder="' + esc(T.eg) + '" value="' + esc(typed.win != null ? typed.win : width || '') + '"></label>' +
        '<label><span>' + esc(T.depthL) + '</span><input data-r="din" type="number" inputmode="numeric" min="100" max="3000" step="1" value="' + esc(typed.din != null ? typed.din : depth || '') + '"></label></div>' +
        '<p class="fine">' + esc(T.sizeWhy) + '</p><div class="row"><button class="btn" data-a="nosize">' + esc(T.noSize) + '</button><button class="btn go" data-a="setsize">' + esc(T.next) + '</button></div>';
    } else if (step === 'finish') {
      h = '<h3>' + esc(T.finH) + '</h3>' + (frame && !frame.measured ? '<p class="fine warn">' + esc(T.guess) + '</p>' : '') + '<div class="fin">' +
        FLOORS.map((f) => { const pr = floorPrice(f); return '<button class="opt" data-a="fin" data-k="' + f.k + '" aria-pressed="' + (f.k === finish) + '"><img alt="" src="' + swatch(f) + '"><span><b>' + esc(f[lang]) + '</b><small>' + floorSize(f) + '</small><small class="pr">' + (pr ? money(pr.lo) + T.to + money(pr.hi) + ' ' + T.shekel + ' ' + T.perSqm : prices ? esc(T.noPrice) : '') + '</small></span></button>'; }).join('') +
        '</div><div class="row"><span class="lbl">' + esc(T.dirL) + '</span><span class="seg">' + [0, 45, 90].map((a) => '<button class="btn" data-a="rot" data-v="' + a + '" aria-pressed="' + (rot === a) + '"><span class="mono">' + a + '°</span></button>').join('') + '</span></div>' +
        '<div class="row"><button class="btn" data-a="move" aria-pressed="' + moveMode + '">' + esc(T.move) + '</button><button class="btn" data-a="center">' + esc(T.center) + '</button></div>' +
        (moveMode ? '<p class="fine">' + esc(T.moveHint) + '</p>' : '') + summary() + '<p class="fine">' + esc(T.truth) + '</p>' +
        '<div class="row"><button class="btn" data-a="towall">' + esc(T.toWall) + '</button><button class="btn go" data-a="toresult">' + esc(T.toResult) + '</button></div>';
    } else if (step === 'wall') {
      const pp = prices && span(prices.wall_paint_m2);
      h = '<h3>' + esc(T.wallH) + '</h3><p>' + esc(T.wallP) + '</p>' + draftControls(true) +
        (!draft.length ? '<div class="row"><span class="count">' + esc(T.wallCount(walls.length)) + '</span>' + (walls.length ? '<button class="btn" data-a="clearw">' + esc(T.wallClear) + '</button>' : '') + '</div>' : '') +
        (!walls.length && !draft.length && paint != null ? '<p class="fine warn">' + esc(T.needWall) + '</p>' : '') +
        '<div class="pal">' + PAINTS.map((c, i) => '<button class="sw" data-a="paint" data-i="' + i + '" aria-pressed="' + (paint === i) + '"><i style="background:' + c.hex + '"></i><span>' + esc(c[lang]) + '</span></button>').join('') +
        '<button class="sw none" data-a="paint" data-i="-1" aria-pressed="' + (paint == null) + '"><i></i><span>' + esc(T.noPaint) + '</span></button></div>' +
        (pp ? '<p class="fine">' + T.paintPrice(money(pp.lo) + T.to + money(pp.hi)) + '</p>' : '') +
        '<div class="row"><button class="btn go" data-a="toresult">' + esc(T.toResult) + '</button></div>';
    } else if (step === 'result') {
      h = '<h3>' + esc(T.resH) + '</h3><p class="fine">' + esc(T.resP) + '</p>' + summary() +
        '<div class="row"><button class="btn go wide" data-a="save">' + esc(T.save) + '</button></div><p class="fine">' + esc(T.truth) + '</p><p class="fine">' + esc(T.privacy) + '</p>';
    }
    const st = el.scrollTop; el.innerHTML = h; el.scrollTop = st;
  }
  function go(s) {
    if (s !== 'corners' && s !== 'start' && !frame && corners.length === 4) prepFloor();
    if (s !== 'corners' && s !== 'start' && !frame) s = 'corners';
    if (draft.length && s !== step) draft = [];
    step = s; moveMode = false;
    panel();
    $('panel').scrollTop = 0;
    if (s === 'finish' || s === 'result' || s === 'wall' || s === 'furniture') update();
    draw();
  }
  function readSize() {
    const wv = +(($('win') || {}).value || 0), dv = +(($('din') || {}).value || 0);
    if (!(wv >= 100 && wv <= 3000) || (dv && !(dv >= 100 && dv <= 3000))) { toast(T.badSize); return false; }
    width = Math.round(wv); depth = dv ? Math.round(dv) : null; floorDirty = true; return true;
  }
  root.addEventListener('click', (e) => {
    const t = e.target.closest('[data-a],[data-step]');
    if (!t || t.disabled) return;
    if (t.dataset.step) { go(t.dataset.step); return; }
    const a = t.dataset.a;
    if (a === 'pick') $('file').click();
    else if (a === 'shoot') $('cam').click();
    else if (a === 'sample') loadSample();
    else if (a === 'new') { step = 'start'; root.firstChild.classList.add('pre'); srcData = null; srcCanvas = null; L = null; $('start').hidden = false; $('nav').hidden = true; $('panel').hidden = true; t.hidden = true; $('sub').textContent = ''; draw(); }
    else if (a === 'clearc') { corners = []; frame = null; floorDirty = true; hasAfter = false; panel(); draw(); }
    else if (a === 'next') go(tabs[tabs.indexOf(step) + 1]);
    else if (a === 'close') closeDraft();
    else if (a === 'undopt') { draft.pop(); panel(); draw(); }
    else if (a === 'clearf') { furniture = []; floorDirty = wallDirty = true; update(); panel(); }
    else if (a === 'clearw') { walls = []; wallDirty = true; update(); panel(); }
    else if (a === 'nosize') { width = null; depth = null; floorDirty = true; go('finish'); }
    else if (a === 'setsize') { if (readSize()) go('finish'); }
    else if (a === 'tosize') go('size');
    else if (a === 'fin') { finish = t.dataset.k; root.querySelectorAll('[data-a="fin"]').forEach((b) => b.setAttribute('aria-pressed', b === t)); update(); }
    else if (a === 'rot') { rot = +t.dataset.v; update(); }
    else if (a === 'move') { moveMode = !moveMode; panel(); }
    else if (a === 'center') { off = [0, 0]; update(); }
    else if (a === 'paint') { paint = +t.dataset.i < 0 ? null : +t.dataset.i; update(); panel(); }
    else if (a === 'towall') go('wall');
    else if (a === 'toresult') go('result');
    else if (a === 'save') save();
  });
  root.addEventListener('input', (e) => { const k = e.target.dataset && e.target.dataset.r; if (k === 'win' || k === 'din') typed[k] = e.target.value; });
  root.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target.matches && e.target.matches('input') && readSize()) go('finish'); });
  for (const k of ['file', 'cam']) $(k).addEventListener('change', (e) => { const f = e.target.files && e.target.files[0]; e.target.value = ''; loadFile(f); });

  async function save() {
    if (!after) return;
    const blob = await new Promise((r) => after.toBlob(r, 'image/jpeg', 0.92));
    if (!blob) return;
    lastSave = { bytes: blob.size, type: blob.type };
    const a = document.createElement('a'), url = URL.createObjectURL(blob);
    a.href = url; a.download = T.fileName; a.style.display = 'none';
    root.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
    if (typeof opts.onSave === 'function') opts.onSave(blob);
    toast(T.saved);
  }

  const ro = new ResizeObserver(() => draw());
  ro.observe(stage);
  draw();

  return {
    destroy() {
      alive = false; ro.disconnect(); cancelAnimationFrame(raf); clearTimeout(toastT);
      cv.removeEventListener('pointerdown', down); cv.removeEventListener('pointermove', move); cv.removeEventListener('pointerup', up); cv.removeEventListener('pointercancel', up);
      shadow.textContent = '';
      srcData = afterData = L = light = floorMask = wallMask = null;
    },
    /** for the local check only: geometry and pixels, never sent anywhere */
    _test: {
      imgToClient: (x, y) => { fit(); const r = cv.getBoundingClientRect(), v = toV([x, y]); return [r.left + v[0], r.top + v[1]]; },
      state: () => ({ step, iw, ih, corners: corners.length, furniture: furniture.length, walls: walls.length, draft: draft.length, renders, busy: busyN > 0 || !!pending, finish, rot, paint, hasAfter, frame: frame && { W: frame.W, D: frame.D, measured: frame.measured, fromPhoto: frame.fromPhoto, f: frame.f, sqm: frame.sqm } }),
      timings, get lastSave() { return lastSave; },
      read: (which, x, y) => { const d = (which === 'before' ? srcData : afterData).data, j = (Math.round(y) * iw + Math.round(x)) * 4; return [d[j], d[j + 1], d[j + 2]]; },
      mean: (which, x0, y0, x1, y1) => { const d = (which === 'before' ? srcData : afterData).data; let r = 0, g = 0, b = 0, n = 0; for (let y = Math.round(y0); y <= y1; y++) for (let x = Math.round(x0); x <= x1; x++) { const j = (y * iw + x) * 4; r += d[j]; g += d[j + 1]; b += d[j + 2]; n++; } return [r / n, g / n, b / n]; },
    },
  };
}
