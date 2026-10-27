() => {
  const vw = innerWidth, vh = innerHeight; const hidden = [];
  const rx = /cookie|consent|privacy|we value your|welcome to|fair housing|qualtrics|planning on buying|sign in with google|כניסה ל|עוגיות|באמצעות חשבון|this site uses|got it|allow all|manage cookies|accept all|decline all|are you planning|subscribe|newsletter|chat live|interested in arranging/i;
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el); if (cs.position !== 'fixed' && cs.position !== 'absolute' && cs.position !== 'sticky') continue;
    if (cs.display === 'none') continue; const r = el.getBoundingClientRect(); if (r.width*r.height < 2000) continue;
    const t = (el.innerText||'').slice(0,400); const z = parseInt(cs.zIndex)||0;
    const isGoogle = el.tagName==='IFRAME' && /accounts\.google|gsi/.test(el.src||'');
    const backdrop = cs.position==='fixed' && r.width>=vw*0.9 && r.height>=vh*0.9 && t.trim().length===0 && !el.querySelector('img,video,canvas');
    if (isGoogle || (cs.position!=='sticky' && rx.test(t) && t.length < 1500 && (z>=10 || cs.position==='fixed')) || backdrop) { el.style.setProperty('display','none','important'); hidden.push(t.slice(0,50)); }
  }
  for (const id of ['credential_picker_container','credential_picker_iframe']) { const e = document.getElementById(id); if (e) e.style.setProperty('display','none','important'); }
  document.documentElement.style.overflow='auto'; document.body.style.overflow='auto';
  return hidden;
}