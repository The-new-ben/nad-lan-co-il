// Package 4: open an order document on the live site, screenshot it, and press the deposit (simulation) when it is open.
// usage: node live_doc.mjs <doc url> <width> <tag>
import { open, sleep } from '../2026-11-11-kikar-journey/evidence/lib.mjs';
const [url, W, tag] = [process.argv[2], Number(process.argv[3] || 1440), process.argv[4] || 'doc'];
const MOB = W < 900;
const p = await open(url, { w: W, h: MOB ? 844 : 900, out: 'live/' + tag });
await sleep(3000);
const shotAt = async (n) => { await p.ev(`(document.getElementById('reserve')||document.body).scrollIntoView()`); await p.shot(n, 400); };
await shotAt('20-approved');
const st = await p.ev(`document.querySelector('#nlc-deposit') ? 'deposit-open' : 'no-deposit'`);
if (st === 'deposit-open') {
  const r = JSON.parse(await p.ev(`(()=>{const e=document.querySelector('#nlc-deposit'); e.scrollIntoView({block:'center'}); const b=e.getBoundingClientRect(); return JSON.stringify({x:b.left+b.width/2,y:b.top+b.height/2})})()`));
  if (MOB) await p.tap(r.x, r.y); else { await p.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: r.x, y: r.y, button: 'left', clickCount: 1 }); await p.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: r.x, y: r.y, button: 'left', clickCount: 1 }); }
  await sleep(3500);
  await shotAt('21-certificate');
}
await p.ev('scrollTo(0,0)'); await p.shot('22-doc-top', 300);
console.log(JSON.stringify({ st, text: (await p.ev(`document.getElementById('reserve').innerText.replace(/\\s+/g,' ').slice(0,400)`)), errors: p.errs.slice(0, 3) }));
await p.close();
