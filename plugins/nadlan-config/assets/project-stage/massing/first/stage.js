/* MassingStage data for FIRST Sde Dov (HAD-794). The code is shared: ../massing.js. Facts: the project page (Hagag Group): a 45-floor tower beside three 9-floor boutique buildings, 350 homes (258 in the tower, 92 in the boutique buildings).
   Building shapes and places on the lot are an illustration; the caption on the stage says so. */
const SPEC = {
 "name": "FIRST",
 "lat": 32.114141,
 "lng": 34.784411,
 "grid": 11,
 "floorH": 3.3,
 "city": "../../dimri/city.json",
 "mainId": "tower",
 "camAz": 140,
 "posterAlt": "הדמיה של FIRST שדה דב: מגדל בן 45 קומות ושלושה בנייני בוטיק בני 9 קומות",
 "buildings": [
  {
   "id": "tower",
   "main": true,
   "floors": 45,
   "x": 0,
   "z": 0,
   "w": 32,
   "d": 28
  },
  {
   "id": "b1",
   "floors": 9,
   "x": -46,
   "z": -26,
   "w": 28,
   "d": 18
  },
  {
   "id": "b2",
   "floors": 9,
   "x": -46,
   "z": 28,
   "w": 28,
   "d": 18
  },
  {
   "id": "b3",
   "floors": 9,
   "x": 42,
   "z": 34,
   "w": 28,
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
