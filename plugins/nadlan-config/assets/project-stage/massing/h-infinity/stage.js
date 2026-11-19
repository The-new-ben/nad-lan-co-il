/* MassingStage data for H Infinity (HAD-794). The code is shared: ../massing.js. Facts: the project page (Merkaz HaNadlan 11.10.2026; Hagag Group): a 52-floor residential tower and a boutique building over a retail floor, about 278 homes, 128 Ibn Gabirol, Somail north.
   Building shapes and places on the lot are an illustration; the caption on the stage says so. */
const SPEC = {
 "name": "H Infinity",
 "lat": 32.087284,
 "lng": 34.78272,
 "grid": 10,
 "floorH": 3.3,
 "city": "../../duo/city.json",
 "mainId": "tower",
 "camAz": 315,
 "posterAlt": "הדמיה של H Infinity: מגדל בן 52 קומות ובניין בוטיק, במתחם סומייל",
 "buildings": [
  {
   "id": "tower",
   "main": true,
   "floors": 52,
   "x": 0,
   "z": 0,
   "w": 30,
   "d": 30
  },
  {
   "id": "boutique",
   "floors": 7,
   "baseM": 4.5,
   "x": -38,
   "z": 18,
   "w": 30,
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
