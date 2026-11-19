// Package 4 (HAD-796): the buying journey pressed on the LIVE site with real taps (phone) or clicks (desktop), test identity only.
// usage: node live_flow.mjs <page url> <width> <tag> [stopAt: sent|reserve|deposit]
// Writes live/<tag>/*.jpg and live/<tag>/result.json {ref, token, url, statuses}. Never uses real personal or payment details.
import { open, sleep } from '../2026-11-11-kikar-journey/evidence/lib.mjs';
import fs from 'node:fs/promises';
const [url, W, tag, stopAt = 'deposit'] = [process.argv[2], Number(process.argv[3] || 390), process.argv[4] || 'run', process.argv[5]];
const out = 'live/' + tag;
const MOB = W < 900;
const p = await open(url, { w: W, h: MOB ? 844 : 900, out });
const R = { tag, url, width: W, steps: [], at: new Date().toISOString() };
const step = async (name, wait = 700) => { await p.shot(String(R.steps.length).padStart(2, '0') + '-' + name, wait); R.steps.push(name); };
const rect = (sel) => p.ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)}); if(!e) return null; e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(); return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2,w:r.width,h:r.height})})()`);
async function press(sel, label) {
  const j = await rect(sel);
  if (!j) throw new Error('missing ' + (label || sel));
  await sleep(750); // the site scrolls smoothly: read the place once the scroll has settled
  const r = JSON.parse(await p.ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)}); const b=e.getBoundingClientRect(); return JSON.stringify({x:b.left+b.width/2,y:b.top+b.height/2})})()`));
  if (MOB) await p.tap(r.x, r.y);
  else { await p.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: r.x, y: r.y }); await sleep(60); await p.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: r.x, y: r.y, button: 'left', clickCount: 1 }); await sleep(50); await p.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: r.x, y: r.y, button: 'left', clickCount: 1 }); }
  await sleep(450);
}
async function type(sel, text) { await press(sel); await p.send('Input.insertText', { text }); await sleep(200); }
await sleep(6500);
await step('page', 200);
// the way in: the shell slot, the stage's step, or the chip
await sleep(MOB ? 600 : 300);
const entry = JSON.parse(await p.ev(`JSON.stringify([...document.querySelectorAll('.nlc-slotbtn,.nlc-addbtn,.nlc-stepbtn,.nlc-chip-fixed')].filter(e=>{const r=e.getBoundingClientRect(); return r.width>0&&r.height>0}).map(e=>e.className.split(' ').find(c=>c.startsWith('nlc-'))))`));
R.entries = entry;
const ck = await p.ev(`(()=>{const b=document.querySelector('.nlck-ic--bk'); return !!(b && b.getBoundingClientRect().width)})()`);
R.entry_used = ck ? 'cockpit bag' : '';
const first = ck ? '.nlck-ic--bk' : entry.includes('nlc-addbtn') ? '.nlc-addbtn' : entry.includes('nlc-slotbtn') ? '.nlc-slotbtn' : entry.includes('nlc-stepbtn') ? '.nlc-stepbtn' : '.nlc-chip-fixed';
await press(first, 'entry');
await sleep(500);
if (await p.ev(`!!document.querySelector('.nlc [data-add]')`)) await press('.nlc [data-add]', 'add');
await step('basket');
await press('.nlc [data-svc="mortgage"]'); await press('.nlc [data-svc="lawyer"]'); await press('.nlc [data-svc="inspection"]');
await press('.nlc [data-toggle$=":call"]');
await press('.nlc .nlc-pick [data-day]:nth-of-type(2)');
if (await p.ev(`!!document.querySelector('.nlc [data-win="18"]')`)) await press('.nlc [data-win="18"]'); else await press('.nlc [data-win="09"]');
await press('.nlc [data-ch="video"]');
await step('call');
await press('.nlc [data-toggle$=":price"]');
await type('.nlc [data-amt]', '6200000');
await p.ev(`document.querySelector('.nlc [data-amt]').blur()`); await sleep(300);
await step('price');
await press('.nlc [data-go="summary"]');
await step('summary');
await press('.nlc [data-go="request"]');
await step('request');
await type('#nlc-name', 'בדיקת מערכת חבילה 4');
await type('#nlc-phone', '0500000000');
await press('#nlc-consent');
await step('request-filled');
await press('.nlc [data-send]');
for (let i = 0; i < 20 && !(await p.ev(`!!document.querySelector('.nlc .nlc-ref--big')`)); i++) await sleep(500);
await step('sent', 400);
const o = JSON.parse(await p.ev(`JSON.stringify((()=>{const s=JSON.parse(localStorage.getItem('nl-cart:v1')); for (const k of s.order) if (s.projects[k].order) return s.projects[k].order; return null})())`));
Object.assign(R, { ref: o && o.ref, token: o && o.token, doc: o && o.url, errors: p.errs.slice(0, 5) });
await fs.writeFile(out + '/result.json', JSON.stringify(R, null, 1));
if (!o || stopAt === 'sent') { console.log(JSON.stringify(R)); await p.close(); process.exit(o ? 0 : 1); }
// the order document: reserve, then (gate off) the simulated deposit
await p.send('Page.navigate', { url: o.url }); await sleep(3500);
await step('doc', 300);
await p.ev(`document.getElementById('reserve').scrollIntoView()`); await step('doc-reserve', 300);
await press('#nlc-accept'); await press('#nlc-reserve'); await sleep(3500);
await p.ev(`document.getElementById('reserve').scrollIntoView()`);
R.after_reserve = await p.ev(`document.querySelector('#nlc-deposit') ? 'deposit-open' : (document.body.innerText.includes('${'reserve'}') ? 'waiting' : '?')`);
await step('after-reserve', 300);
if (stopAt === 'deposit' && R.after_reserve === 'deposit-open') {
  await press('#nlc-deposit'); await sleep(3500);
  await p.ev(`document.getElementById('reserve').scrollIntoView()`);
  await step('certificate', 300);
}
await p.ev('scrollTo(0,0)'); await step('doc-top', 200);
R.errors = p.errs.slice(0, 5);
await fs.writeFile(out + '/result.json', JSON.stringify(R, null, 1));
console.log(JSON.stringify(R));
await p.close();
