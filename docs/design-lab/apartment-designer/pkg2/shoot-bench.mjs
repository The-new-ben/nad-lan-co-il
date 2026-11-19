// node shoot-bench.mjs [--only=ours]   Benchmark pictures for package 2 (HAD-792): the world's best public pages + our live designer (BEFORE).
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { browser, sleep } from './cdp.mjs';
const here = path.dirname(fileURLToPath(import.meta.url)), out = path.join(here, 'bench');
const only = (process.argv.find((a) => a.startsWith('--only=')) || '').split('=')[1] || '';
const WORLD = [
  ['ikea-kreativ', 'https://www.ikea.com/us/en/home-design/'],
  ['planner5d', 'https://planner5d.com/'],
  ['matterport', 'https://matterport.com/discover'],
  ['roomstyler', 'https://roomstyler.com/'],
  ['coohom', 'https://www.coohom.com/'],
  ['floorplanner', 'https://floorplanner.com/'],
];
const b = await browser();
try {
  if (!only || only === 'world') for (const [k, u] of WORLD) {
    const p = await b.page({ w: 1440, h: 900, dpr: 1, mobile: false, url: u });
    await sleep(6000); await p.shot(path.join(out, 'world-' + k + '-desktop.png')); console.log('shot', k); await p.close();
  }
  if (!only || only === 'ours') {
    const live = process.argv.find((a) => a.startsWith('--base=')) ? process.argv.find((a) => a.startsWith('--base=')).split('=')[1] : 'https://nad-lan.co.il';
    const tag = process.argv.find((a) => a.startsWith('--tag=')) ? process.argv.find((a) => a.startsWith('--tag=')).split('=')[1] : 'before';
    for (const [w, h, mobile, nm] of [[390, 844, true, 'phone'], [1440, 900, false, 'desktop']]) {
      const p = await b.page({ w, h, dpr: mobile ? 2 : 1, mobile, url: live + '/tour/designer/?project=ashira&t=' + Date.now() });
      const ok = await p.wait('(()=>{const h=document.getElementById("host");return !!(h&&h.shadowRoot&&h.shadowRoot.querySelector("canvas"))})()', 40000);
      await sleep(3500); await p.shot(path.join(out, 'ours-' + tag + '-' + nm + '-doll.png'));
      // walk mode
      await p.ev('(()=>{const b=document.getElementById("host").shadowRoot.querySelector("[data-nd=m-walk]");b&&b.click();return 1})()').catch(() => 0);
      await sleep(2500); await p.shot(path.join(out, 'ours-' + tag + '-' + nm + '-walk.png'));
      console.log('ours', nm, ok, p.errors.slice(0, 3)); await p.close();
    }
  }
} finally { await b.close(); }
