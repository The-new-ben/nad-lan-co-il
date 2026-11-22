(() => {
  'use strict';
  if (window.__nadlanQuarterWalk || !window.HTMLDialogElement || !HTMLDialogElement.prototype.showModal) return;
  window.__nadlanQuarterWalk = true;
  const key = 'nadlanQuarterWalk';
  let active = null;
  const owned = new Set();
  const openerFor = (section,index) => section?.querySelectorAll('[data-entry]')[index];
  const storeKey = (link) => ['nlq.walk',location.pathname,location.search,link.closest('[data-nlq]').dataset.instance].join('|');
  function remembered(link, value) {
    try {
      if (value) sessionStorage.setItem(storeKey(link), value);
      const saved = sessionStorage.getItem(storeKey(link));
      return saved?.startsWith('#') ? saved : '';
    } catch { return ''; }
  }
  function track(name, data) {
    try { if (typeof window.nlTrack === 'function') window.nlTrack(name,data); } catch {}
  }
  function button(tag, label) {
    const node = document.createElement(tag);
    node.textContent = label;
    return node;
  }
  function save(row) {
    try {
      const child = row.frame.contentWindow;
      const hash = child.round2StreetCell?.live ? child.round2StreetCell.getHash() : child.tour?.getHash();
      if (hash && row.link.matches('.nlq-enter')) remembered(row.link,hash);
      return hash;
    } catch {}
  }
  function restore(row) {
    clearTimeout(row.warning);
    row.barObserver?.disconnect();
    save(row);
    try {row.frame.contentWindow.tour?.world?.renderer?.setAnimationLoop(null);} catch {}
    row.dialog.close();
    row.dialog.remove();
    active = null;
    const docStyle=document.documentElement.style;
    if(docStyle.overflow==='hidden') docStyle.overflow=row.previousOverflow;
    const main = row.section.querySelector('.nlq-enter');
    if (remembered(main)) main.textContent = row.section.dataset.resume;
    row.link.focus({preventScroll:true});
    const scroll=()=>window.scrollTo({top:row.top,left:row.left,behavior:'instant'});
    scroll();requestAnimationFrame(()=>{if(!active)scroll();});
    track('tour_embed_close',{place_id:row.link.dataset.entry||null});
  }
  function leave() {
    if (!active) return;
    const row = active;
    if (history.state?.[key]?.id === row.id && owned.has(row.id)) {
      if(row.leaving)return;
      row.leaving=true;
      history.back();
      setTimeout(()=>{if(active===row){const state={...history.state};delete state[key];history.replaceState(state,'');restore(row);}},600);
      return;
    }
    if(history.state?.[key]?.id===row.id){const state={...history.state};delete state[key];history.replaceState(state,'');}
    restore(row);
  }
  function mount(section, link, state) {
    if (active || !section || !link) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin) return;
    const old = link.matches('.nlq-enter') ? remembered(link) : '';
    if (old) url.hash = old;
    const dialog = document.createElement('dialog');
    dialog.className = 'nlq-dialog';
    dialog.lang = section.lang;
    dialog.dir = section.dir;
    const title = section.querySelector('h2')?.textContent || link.textContent;
    dialog.setAttribute('aria-label',title);
    const bar = document.createElement('div');
    bar.className = 'nlq-bar';
    const close = button('button',section.dataset.close);
    close.type = 'button';close.autofocus = true;
    const separate = button('a',section.dataset.open);
    separate.href = url.href;
    separate.target = '_blank';
    separate.rel = 'noopener';
    const status = document.createElement('p');
    status.className = 'nlq-status';
    status.setAttribute('role','status');
    status.textContent = section.dataset.loading;
    const frame = document.createElement('iframe');
    frame.title = title;
    frame.dataset.nlqFrame = '';
    frame.allow = 'fullscreen; xr-spatial-tracking; gyroscope; accelerometer';
    frame.allowFullscreen = true;
    const row = {section,link,dialog,frame,id:state.id,top:scrollY,left:scrollX,previousOverflow:document.documentElement.style.overflow};
    active = row;
    document.documentElement.style.overflow='hidden';
    close.onclick = leave;
    separate.onclick = () => {
      const value = save(row);
      if (value) { const current = new URL(link.href);current.hash=value;const lang=new URLSearchParams(value.slice(1)).get('lang');if(lang)current.searchParams.set('lang',lang);separate.href=current.href; }
      track('tour_embed_open_page',{place_id:link.dataset.entry||null});
    };
    dialog.addEventListener('cancel',event=>{event.preventDefault();leave();});
    row.warning = setTimeout(()=>{if(active===row)status.textContent=section.dataset.failure;},15000);
    frame.addEventListener('load',()=>{
      if (active !== row) return;
      try {
        const doc = frame.contentDocument;
        if (!doc?.querySelector('#stage')) { status.textContent = section.dataset.failure;return; }
        row.barObserver?.disconnect();
        const labels = JSON.parse(section.dataset.barLabels || '{}');
        const syncBar = () => {
          const lang = doc.documentElement.lang;
          if (!Object.hasOwn(labels, lang)) return;
          bar.lang = lang;
          bar.dir = doc.documentElement.dir || section.dir;
          close.textContent = labels[lang].close;
          separate.textContent = labels[lang].open;
        };
        syncBar();
        row.barObserver = new MutationObserver(syncBar);
        row.barObserver.observe(doc.documentElement,{attributes:true,attributeFilter:['lang','dir']});
        const ready=()=>{if(active===row){clearTimeout(row.warning);status.hidden=true;}};
        if(frame.contentWindow.round2StreetCell?.ledger.ready || frame.contentWindow.tourReady || doc.querySelector('#hud')?.hidden)ready();
        else for(const event of ['round2-cell-ready','nlq-tour-ready'])frame.contentWindow.addEventListener(event,ready,{once:true});
        doc.addEventListener('keydown',event=>{
          if (event.key !== 'Escape' || event.repeat || doc.pointerLockElement) return;
          if (['#sheet','#photoBar','#caption','#inLobby','#cancelShore'].some(sel=>{
            const el=doc.querySelector(sel);return el && !el.hidden;
          }) || frame.contentWindow.tour?.state.ride) return;
          event.preventDefault();event.stopImmediatePropagation();leave();
        },true);
      } catch {status.textContent=section.dataset.failure;}
    });
    frame.src = url.href;
    bar.append(close,separate);dialog.append(bar,status,frame);
    document.body.append(dialog);dialog.showModal();
    close.focus({preventScroll:true});
    track('tour_embed_open',{place_id:link.dataset.entry||null,resumed:!!old});
  }
  document.addEventListener('click',event=>{
    if (event.defaultPrevented || event.button!==0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('[data-nlq] [data-entry]');
    if (!link || active || new URL(link.href).origin !== location.origin) return;
    const section=link.closest('[data-nlq]');
// Optional ordinary-link opening. Native browser history returns to the same article.
if(section.dataset.view==='page'){
  const destination=new URL(link.href);
  destination.searchParams.set('walk','1');
  const old=!destination.hash&&link.matches('.nlq-enter')?remembered(link):'';
  if(old)destination.hash=old;
  if(link.matches('.nlq-enter')){
    try{
      const bookmark={key:storeKey(link),path:destination.pathname,query:destination.search,expires:Date.now()+30000};
      sessionStorage.setItem('nlq.direct-entry',JSON.stringify(bookmark));
    }catch{}
  }
  track('tour_embed_open',{place_id:link.dataset.entry||null,resumed:!!old,presentation:'page'});
  if(destination.href!==link.href){event.preventDefault();location.assign(destination.href);}
  return;
}

    const state={id:Date.now().toString(36),section:[...document.querySelectorAll('[data-nlq]')].indexOf(section),index:[...section.querySelectorAll('[data-entry]')].indexOf(link),instance:section.dataset.instance};
    event.preventDefault();
    const parentState=history.state && typeof history.state==='object' ? history.state : {};
    history.pushState({...parentState,[key]:state},'');
    owned.add(state.id);
    mount(section,link,state);
  });
  function stateSection(state){return [...document.querySelectorAll('[data-nlq]')].find(s=>s.dataset.instance===state.instance);}
  addEventListener('popstate',()=>{
    const state=history.state?.[key];
    if(active && active.id!==state?.id) restore(active);
    if(!active && state){
      const section=stateSection(state);
      mount(section,openerFor(section,state.index),state);
    }
  });
  addEventListener('pagehide',()=>{if(active)save(active);});
  const init=()=>{
    for(const section of document.querySelectorAll('[data-nlq]')){
      const link=section.querySelector('.nlq-enter');
      if(link && remembered(link))link.textContent=section.dataset.resume;
    }
    const state=history.state?.[key];
    if(state){const section=stateSection(state);mount(section,openerFor(section,state.index),state);}
  };
  addEventListener('pageshow',event=>{if(event.persisted)init();});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
