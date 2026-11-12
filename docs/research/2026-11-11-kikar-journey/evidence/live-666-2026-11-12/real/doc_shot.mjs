import { browser } from '../harness.mjs';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
for (const [w, h] of [[390, 844], [1440, 900]]) { const b = await browser({ w, h, L: 'he' }); await b.go('https://nad-lan.co.il/wp-json/nadlan/v1/rfp/fa5ilp5aejtclskf1yizs69p'); await sleep(2500); await b.shot(`real-doc-${w}`); console.log(w, 'errs', b.errs.length); await b.close(); }
