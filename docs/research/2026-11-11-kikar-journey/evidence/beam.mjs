import { open, sleep } from './lib.mjs';
const slug = process.argv[2] || 'ashira-sde-dov', out = 'shots/' + slug;
const p = await open(`https://nad-lan.co.il/projects/${slug}/?jr=6`, { out });
await sleep(3500); await p.scrollTo('.nlps-stagebox'); await sleep(2000);
await p.ev(`document.querySelector('.rbs-open').click()`); await sleep(7000);
const cv = JSON.parse(await p.ev(`(()=>{const e=document.querySelector('.nlps-stagebox canvas'); const r=e.getBoundingClientRect(); return JSON.stringify({x:r.left,y:r.top,w:r.width,h:r.height})})()`));
const mouse = async (x, y) => { await p.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }); await sleep(120); await p.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }); await sleep(70); await p.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }); };
await mouse(cv.x + cv.w * 0.47, cv.y + cv.h * 0.45); await sleep(2600);
// hide the label card to see the model with the ring, then look for anything beam-like on the page
await p.ev(`(()=>{const m=document.querySelector('.rbs-label-min'); m&&m.click()})()`); await p.shot('13-picked-min', 900);
console.log('beamish', await p.ev(`(()=>{const out=[]; document.querySelectorAll('[class*=beam],[class*=cone],[class*=sight],[class*=fov],[id*=beam],[id*=cone],[class*=wedge],[class*=sector]').forEach(e=>out.push(e.tagName+'#'+e.id+'.'+(e.getAttribute('class')||'')+' y'+Math.round(e.getBoundingClientRect().top+scrollY)+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height))); return out.slice(0,20).join(' || ')||'none in DOM'})()`));
for (const sel of ['#nlps-view', '#nlpjx-unimap', '#nlpjx-map']) { console.log(sel, await p.scrollTo(sel, 80)); await p.shot('14-' + sel.replace('#', ''), 3500); }
console.log('unimap layers', await p.ev(`(()=>{const m=document.getElementById('nlpjx-unimap'); if(!m) return 'none'; const mm=m.__map||window.nlpjxMap||null; const st=[...m.querySelectorAll('canvas,svg,path')].length; return JSON.stringify({children:m.children.length, nodes:st, text:m.parentElement.innerText.replace(/\s+/g,' ').slice(0,300)})})()`));
console.log('ERRS', p.errs.length);
await p.close();
