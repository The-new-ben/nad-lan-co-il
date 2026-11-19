// Package 4 (HAD-796) 1.72.715 proof: the Kikar shared-apartment link (#dira=) puts that apartment into the basket. Opens the basket only; sends nothing.
import { open, sleep } from '../2026-11-11-kikar-journey/evidence/lib.mjs';
import fs from 'node:fs/promises';
const url = process.argv[2] || 'https://nad-lan.co.il/projects/hamedina/#dira=B24-262';
const out = 'live/C-phone-kikar-dira-715';
const p = await open(url, { w: 390, h: 844, out });
await sleep(6500);
await p.shot('00-page', 200);
const sel = await p.ev(`(()=>{const b=document.querySelector('.nlck-ic--bk'); if(b&&b.getBoundingClientRect().width) return '.nlck-ic--bk'; const e=[...document.querySelectorAll('.nlc-slotbtn,.nlc-stepbtn,.nlc-chip-fixed')].find(e=>e.getBoundingClientRect().width>0); return e? '.'+e.className.split(' ')[0] : ''})()`);
await p.ev(`document.querySelector(${JSON.stringify(sel)}).scrollIntoView({block:'center'})`); await sleep(750);
const r = JSON.parse(await p.ev(`JSON.stringify((()=>{const b=document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect(); return {x:b.left+b.width/2,y:b.top+b.height/2}})())`));
await p.tap(r.x, r.y); await sleep(1500);
await p.shot('01-basket', 400);
const R = { url, entry: sel, at: new Date().toISOString(),
  unit: JSON.parse(await p.ev(`JSON.stringify((()=>{try{const s=JSON.parse(localStorage.getItem('nl-cart:v1')); return s.projects.hamedina && s.projects.hamedina.unit}catch(e){return null}})())`)),
  sheet: await p.ev(`(document.querySelector('.nlc')||{}).innerText ? document.querySelector('.nlc').innerText.slice(0,400) : ''`),
  errors: p.errs.slice(0, 5) };
await fs.writeFile(out + '/result.json', JSON.stringify(R, null, 1));
console.log(JSON.stringify(R));
await p.close();
