import { open, sleep } from './lib.mjs';
const slug = process.argv[2] || 'ashira-sde-dov', out = 'shots/' + slug;
const p = await open(`https://nad-lan.co.il/projects/${slug}/?jr=3`, { out });
await sleep(3500); await p.scrollTo('.nlps-stagebox'); await sleep(2000);
await p.ev(`document.querySelector('.rbs-open').click()`); await sleep(7000);
const state = () => p.ev(`(()=>{const q=(s)=>document.querySelector(s); const t=(s)=>{const e=q(s); return e? (e.hidden||getComputedStyle(e).display==='none'||getComputedStyle(e).opacity==='0'?'[hidden] ':'')+(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,200):null}; return JSON.stringify({root:q('.rbs').className.replace('rbs dus ashira ','').replace('rbs ',''), hint:t('.rbs-hint'), kick:t('.dus-label-kick'), title:t('.rbs-label-title'), line:t('.rbs-label-line'), facing:t('.rbs-label-facing'), more:t('.rbs-label-more'), steps:[...document.querySelectorAll('.nlps-step')].filter(e=>/is-|on|done|cur/.test(e.className)).map(e=>e.className+':'+e.textContent.trim().slice(0,12)).join(' | '), basket:t('.nlbk-count'), hash: location.hash})})()`);
const cv = JSON.parse(await p.ev(`(()=>{const e=document.querySelector('.nlps-stagebox canvas'); const r=e.getBoundingClientRect(); return JSON.stringify({x:r.left,y:r.top,w:r.width,h:r.height, pe:getComputedStyle(e).pointerEvents, ta:getComputedStyle(e).touchAction})})()`));
console.log('canvas', JSON.stringify(cv));
const mouse = async (x, y) => { await p.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, pointerType: 'mouse' }); await sleep(120); await p.send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }); await sleep(70); await p.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 }); };
// 1. tap the tower's label, then the tower
console.log('label btn', await p.ev(`(()=>{const L=[...document.querySelectorAll('.rbs [class*=tag], .rbs [class*=chip], .rbs button')].filter(e=>/המגדל/.test(e.textContent)); return L.map(e=>e.tagName+'.'+e.className+':'+e.textContent.trim()).join(' | ')})()`));
for (const [fx, fy, n] of [[0.47, 0.45, 'a'], [0.47, 0.62, 'b'], [0.80, 0.80, 'c']]) {
  await mouse(cv.x + cv.w * fx, cv.y + cv.h * fy); await sleep(2600); await p.shot('06-mouse-' + n, 300);
  console.log('mouse ' + n, await state());
}
console.log('events', await p.ev(`JSON.stringify((window.dataLayer||[]).map(x=>x&&x.event? x.event : (x&&x[0]==='event'? x[1]+' '+JSON.stringify(x[2]||{}).slice(0,110):null)).filter(Boolean).slice(-14))`));
// 2. the three actions on the label
for (const act of ['view', 'inside', 'design']) {
  console.log('act ' + act, await p.ev(`(()=>{const b=document.querySelector('.rbs-act[data-act="${act}"]'); if(!b) return 'no'; b.click(); return 'clicked'})()`));
  await sleep(4500); await p.shot('07-act-' + act, 300);
  console.log('  after', await p.ev(`(()=>{const steps=[...document.querySelectorAll('.nlps-step')].map(e=>e.className.replace('nlps-step','').trim()||'-').join(','); const m=document.getElementById('nlps-view-map'); const vis=(e)=>e&&e.getBoundingClientRect().height>0; const iframes=[...document.querySelectorAll('iframe')].filter(vis).map(f=>f.src.slice(0,120)); const panels=[...document.querySelectorAll('[id^=nlps-]')].filter(e=>vis(e)&&e.getBoundingClientRect().top<innerHeight&&e.getBoundingClientRect().bottom>0).map(e=>e.id).slice(0,12); return JSON.stringify({steps, y:Math.round(scrollY), viewMapSvg: m? m.querySelectorAll('svg,canvas,path').length:null, panels, iframes, hash:location.hash, url: location.pathname+location.search})})()`));
  if (act !== 'view') { await p.ev('history.length>1 && null'); }
}
console.log('ERRS', p.errs.length, p.errs.slice(0, 3));
await p.close();
