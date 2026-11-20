// Shared data for the 3D harness (xray.js) and the flat drawing (plan4r.html): the service runs and the part metadata of example-4r.
// Plan centimetres: X right, Y down the sheet, Z up. Right angles only. Electricity runs at 90 cm inside the walls and dips into the
// slab (z 8) where a door or an opening interrupts the wall; cold z 28, hot 6 cm beside it; gas z 60.
export const COL = { c: '#1565c0', h: '#c62828', g: '#f5b800', e: '#6a3fc8' };
export const RUNS = [
  { id: 'c-boiler', sys: 'c', serves: ['boiler'], pts: [[812, 888, 28], [670, 888, 28], [670, 888, 76], [670, 862, 76]] },
  { id: 'c-washer', sys: 'c', serves: ['washer'], pts: [[812, 888, 28], [812, 722, 28], [812, 722, 70]] },
  { id: 'c-toilet', sys: 'c', serves: ['bath'], pts: [[812, 775, 28], [834, 775, 28]] },
  { id: 'c-shower', sys: 'c', serves: ['bath'], pts: [[812, 888, 28], [812, 888, 104], [836, 888, 104]] },
  { id: 'c-sink', sys: 'c', serves: ['sink'], pts: [[812, 888, 28], [548, 888, 28], [548, 888, 8], [432, 888, 8], [432, 888, 28], [286, 888, 28], [286, 888, 92], [286, 880, 92], [273, 880, 92]] },
  { id: 'h-sink', sys: 'h', serves: ['sink'], pts: [[794, 862, 116], [818, 862, 116], [818, 862, 28], [818, 894, 28], [548, 894, 28], [548, 894, 8], [432, 894, 8], [432, 894, 28], [254, 894, 28], [254, 894, 92], [254, 880, 92], [267, 880, 92]] },
  { id: 'h-shower', sys: 'h', serves: ['bath'], pts: [[818, 862, 28], [818, 842, 28], [818, 842, 104], [836, 842, 104]] },
  { id: 'g-hob', sys: 'g', serves: ['cooktop'], pts: [[-18, 900, 60], [120, 900, 60], [120, 860, 60], [120, 860, 90]] },
  { id: 'e-trunk', sys: 'e', serves: ['acLiving', 'shutter', 'acBed'], pts: [[601, 860, 139], [601, 860, 90], [620, 860, 90], [620, 830, 90], [620, 830, 8], [620, 730, 8], [620, 730, 90], [620, 500, 90], [620, 500, 8], [620, 380, 8], [620, 380, 90], [620, 0, 90]] },
  { id: 'e-north-w', sys: 'e', serves: ['acLiving', 'shutter'], pts: [[620, 0, 90], [555, 0, 90]] },
  { id: 'e-acl', sys: 'e', serves: ['acLiving'], pts: [[555, 0, 90], [555, 0, 105], [555, 14, 105]] },
  { id: 'e-shutter', sys: 'e', serves: ['shutter'], pts: [[555, 0, 90], [494, 0, 90], [494, 0, 245], [486, 0, 245]] },
  { id: 'e-acb', sys: 'e', serves: ['acBed'], pts: [[620, 0, 90], [920, 0, 90], [920, 0, 105], [920, 14, 105]] },
  { id: 'e-kitchen', sys: 'e', serves: ['cooktop', 'fridge'], pts: [[620, 860, 90], [620, 900, 90], [560, 900, 90], [560, 900, 8], [420, 900, 8], [420, 900, 90], [120, 900, 90], [120, 880, 90]] },
  { id: 'e-fridge', sys: 'e', serves: ['fridge'], pts: [[360, 900, 90], [360, 560, 90], [360, 560, 100], [352, 560, 100]] },
  { id: 'e-laundry', sys: 'e', serves: ['boiler', 'washer'], pts: [[620, 900, 90], [826, 900, 90], [826, 745, 90], [826, 745, 60], [811, 745, 60]] },
  { id: 'e-boiler', sys: 'e', serves: ['boiler'], pts: [[748, 900, 90], [748, 900, 118]] },
];
// anchor [x, y, z] of each part (the point a tap target or a camera aims at), roomPt a floor point inside its room, sys the systems it sits on
export const PART_META = {
  acLiving: { anchor: [555, 23, 105], roomPt: [555, 80], sys: { e: 1, ac: 1 }, he: 'מזגן סלון', state: 'soon' },
  shutter: { anchor: [310, 0, 200], roomPt: [310, 80], sys: { e: 1 }, he: 'תריס סלון', state: 'ok' },
  cooktop: { anchor: [120, 850, 94], roomPt: [200, 740], sys: { e: 1, g: 1 }, he: 'כיריים ותנור', state: 'ok' },
  fridge: { anchor: [318, 560, 100], roomPt: [250, 580], sys: { e: 1 }, he: 'מקרר', state: 'ok' },
  sink: { anchor: [270, 868, 100], roomPt: [200, 740], sys: { w: 1 }, he: 'כיור וברז ראשי', state: 'ok' },
  panel: { anchor: [601, 860, 160], roomPt: [540, 840], sys: { e: 1 }, he: 'לוח חשמל', state: 'ok' },
  acBed: { anchor: [920, 23, 105], roomPt: [920, 120], sys: { e: 1, ac: 1 }, he: 'מזגן חדר שינה', state: 'ok' },
  mamad: { anchor: [1190, 580, 100], roomPt: [1160, 700], sys: {}, he: 'דלת וחלון הממ"ד', state: 'ok' },
  bath: { anchor: [875, 810, 40], roomPt: [900, 760], sys: { w: 1 }, he: 'מקלחת ואסלה', state: 'ok' },
  boiler: { anchor: [720, 862, 116], roomPt: [720, 800], sys: { w: 1, e: 1 }, he: 'דוד שמש', state: 'fault' },
  washer: { anchor: [780, 722, 45], roomPt: [720, 800], sys: { w: 1, e: 1 }, he: 'מכונת כביסה', state: 'ok' },
};
// short names written on the floor / on the flat drawing, by room id of the plan
export const ROOM_SHORT = { living: 'סלון', kitchen: 'מטבח', hall: 'כניסה', master: 'שינה', bed2: 'שינה', corridor: 'מסדרון', wc: 'שירותים', laundry: 'שירות', bath: 'רחצה', mamad: 'ממ"ד', balcony: 'מרפסת' };
// line icons of the parts (the same paths as docs/rentals/design/board1/Plan.dc.html), 24 x 24 viewBox, stroke 1.7
export const ICON_PATHS = {
  ac: '<rect x="3" y="6" width="18" height="8" rx="2"></rect><path d="M6 11h12M8 17v2M12 17v2M16 17v2"></path>',
  shutter: '<rect x="4" y="3" width="16" height="18" rx="1.5"></rect><path d="M4 8h16M4 12h16M4 16h16"></path>',
  cooktop: '<rect x="3" y="4" width="18" height="16" rx="2"></rect><circle cx="9" cy="10" r="2.2"></circle><circle cx="15.5" cy="10" r="2.2"></circle><path d="M7 16h10"></path>',
  fridge: '<rect x="6" y="2.5" width="12" height="19" rx="2"></rect><path d="M6 9.5h12M9 6v1.5M9 12.5v3"></path>',
  sink: '<path d="M5 20h14M8 20v-9a4 4 0 0 1 8 0v1M16 12h3M12 4v3"></path>',
  panel: '<rect x="4" y="3" width="16" height="18" rx="2"></rect><path d="M8 8v4M12 8v4M16 8v4M8 16h8"></path>',
  mamad: '<rect x="5" y="2.5" width="14" height="19" rx="1.5"></rect><circle cx="12" cy="12" r="3"></circle><path d="M12 9v6M9 12h6"></path>',
  bath: '<path d="M6 21V8a4 4 0 0 1 8 0M11 11h6M12 14v1M14 15v1.5M16 14v1"></path>',
  boiler: '<rect x="5" y="3.5" width="14" height="6" rx="3"></rect><path d="M6 12.5h12l2.5 8h-17zM12 12.5v8M8 9.5v3M16 9.5v3"></path>',
  washer: '<rect x="4" y="3" width="16" height="18" rx="2"></rect><circle cx="12" cy="13" r="4"></circle><path d="M7 6.5h2"></path>',
  clock: '<circle cx="12" cy="12" r="8.5"></circle><path d="M12 7.2V12l3.2 2"></path>',
};
export const PART_ICON = { acLiving: 'ac', acBed: 'ac', shutter: 'shutter', cooktop: 'cooktop', fridge: 'fridge', sink: 'sink', panel: 'panel', mamad: 'mamad', bath: 'bath', boiler: 'boiler', washer: 'washer' };
