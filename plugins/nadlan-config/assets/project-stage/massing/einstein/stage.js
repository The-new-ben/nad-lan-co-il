/* MassingStage data for Einstein Tower (HAD-794). The code is shared: ../massing.js. Facts: the project page (S001, S002; Hagag Group): 215 homes in 3 buildings, a 28-floor tower and two 13-floor residential buildings over a double commercial base, Einstein and Levi Eshkol.
   Building shapes and places on the lot are an illustration; the caption on the stage says so. */
const SPEC = {
 "name": "EINSTEIN TOWER",
 "lat": 32.111736,
 "lng": 34.788433,
 "grid": 11,
 "floorH": 3.3,
 "city": "../../ashira/city.json",
 "mainId": "tower",
 "camAz": 150,
 "posterAlt": "הדמיה של EINSTEIN TOWER: מגדל בן 28 קומות ושני מבנים בני 13 קומות מעל בסיס מסחרי",
 "buildings": [
  {
   "id": "tower",
   "main": true,
   "floors": 28,
   "x": 0,
   "z": 0,
   "w": 28,
   "d": 28
  },
  {
   "id": "b1",
   "floors": 13,
   "baseM": 9,
   "x": 44,
   "z": -22,
   "w": 32,
   "d": 16
  },
  {
   "id": "b2",
   "floors": 13,
   "baseM": 9,
   "x": 44,
   "z": 24,
   "w": 32,
   "d": 16
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
