// Package 4 (HAD-788): public competitor pages, phone 390 + desktop 1440, screenshot + first text. GETs only, no forms.
import { open, sleep } from '../2026-11-11-kikar-journey/evidence/lib.mjs';
import fs from 'node:fs/promises';
const L = [
  ['tesla', 'https://www.tesla.com/modely/design'],
  ['apple-bag', 'https://www.apple.com/shop/buy-iphone'],
  ['opendoor', 'https://www.opendoor.com/'],
  ['redfin', 'https://www.redfin.com/buy-a-home/offer'],
  ['compass', 'https://www.compass.com/'],
  ['emaar', 'https://properties.emaar.com/en/'],
  ['damac', 'https://www.damacproperties.com/en/'],
  ['taylor', 'https://www.taylormorrison.com/home-reservation-system'],
  ['unlatch', 'https://www.unlatch.com/'],
];
const only = process.argv.slice(2);
const out = {};
for (const [k, u] of L) {
  if (only.length && !only.includes(k)) continue;
  for (const w of [390, 1440]) {
    let p;
    try {
      p = await open(u, { w, h: w < 900 ? 844 : 900, out: 'bench' });
      await sleep(6000);
      await p.shot(k + '-' + w, 500);
      if (w === 1440) out[k] = { url: u, at: new Date().toISOString(), title: await p.ev('document.title'), text: await p.ev("document.body ? document.body.innerText.replace(/\s+/g,' ').slice(0,2500) : ''") };
      console.log('ok', k, w);
    } catch (e) { console.log('fail', k, w, String(e).slice(0, 120)); }
    if (p) await p.close();
  }
}
await fs.writeFile('bench/texts-' + (only.join('-') || 'all') + '.json', JSON.stringify(out, null, 1));
