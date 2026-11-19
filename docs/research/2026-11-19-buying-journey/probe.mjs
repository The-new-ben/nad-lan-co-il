import { open, sleep } from '../2026-11-11-kikar-journey/evidence/lib.mjs';
const p = await open(process.argv[2], { w: Number(process.argv[3] || 1440), h: 900, out: 'live/probe' });
await sleep(6500);
console.log(await p.ev(`JSON.stringify({cart: !!window.NLCart, btns: [...document.querySelectorAll('.nlc-slotbtn,.nlc-stepbtn,.nlc-addbtn,.nlc-chip-fixed')].map(b=>{const r=b.getBoundingClientRect(); return b.className+' '+Math.round(r.x)+','+Math.round(r.y)+' '+Math.round(r.width)+'x'+Math.round(r.height)})})`));
console.log(await p.ev(`(()=>{const b=document.querySelector('.nlc-slotbtn'); b.scrollIntoView({block:'center'}); const r=b.getBoundingClientRect(); const e=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return 'hit: '+(e? e.tagName+'.'+e.className : null)})()`));
console.log(await p.ev(`(()=>{document.querySelector('.nlc-slotbtn').click(); return new Promise(r=>setTimeout(()=>{const n=document.querySelector('.nlc'); r('sheet: '+(n? (n.hidden?'hidden':'open '+getComputedStyle(n.querySelector('.nlc__sheet')).transform) : 'none'))},800))})()`));
console.log('errors', JSON.stringify(p.errs));
await p.close();
