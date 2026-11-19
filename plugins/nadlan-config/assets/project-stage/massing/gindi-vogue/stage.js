/* MassingStage data for Gindi Vogue Sde Dov (HAD-794). The code is shared: ../massing.js. Facts: the project page (Merkaz HaNadlan 3.2025; Gindi): three buildings, a 44-floor tower and buildings of 20 and 9 floors, 708 homes.
   Building shapes and places on the lot are an illustration; the caption on the stage says so. */
const SPEC = {
 "name": "GINDI VOGUE",
 "lat": 32.110644,
 "lng": 34.783587,
 "grid": 11,
 "floorH": 3.3,
 "city": "../../dimri/city.json",
 "mainId": "tower",
 "camAz": 140,
 "posterAlt": "הדמיה של גינדי ווג שדה דב: מגדל בן 44 קומות ובניינים של 20 ו-9 קומות",
 "buildings": [
  {
   "id": "tower",
   "main": true,
   "floors": 44,
   "x": 0,
   "z": 0,
   "w": 32,
   "d": 30
  },
  {
   "id": "mid",
   "floors": 20,
   "x": 48,
   "z": -8,
   "w": 32,
   "d": 20
  },
  {
   "id": "low",
   "floors": 9,
   "x": -44,
   "z": 26,
   "w": 36,
   "d": 18
  }
 ]
};
export function mountMassingStage(container, options) {
  const q = new URL(import.meta.url).search;
  const api = {};
  api.ready = import(new URL('../massing.js', import.meta.url).href + q).then((m) => {
    const inner = m.mount(container, options, SPEC, new URL('./', import.meta.url).href);
    for (const k of Object.keys(inner)) { if (k !== 'ready' && k !== 'floor') api[k] = inner[k]; }
    Object.defineProperty(api, 'floor', { get: () => inner.floor });
    return inner.ready;
  });
  return api;
}
