import sys, time
from playwright.sync_api import sync_playwright
url, tool = sys.argv[1], sys.argv[2]
JS = r"""(tool)=>{const y=e=>Math.round(e.getBoundingClientRect().top+scrollY);const h1=document.querySelector('h1'),t=document.querySelector('[data-nli="'+tool+'"]');
const sec=t.closest('section');const before=[];let s=sec.previousElementSibling;let k=0;while(s&&k<5){before.push(s.tagName+' '+(s.innerText||'').slice(0,50).split('\n').join(' '));s=s.previousElementSibling;k++}
return {h1:y(h1),tool:y(t),before:before}}"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome"); pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(url + "?nlv=%d" % time.time(), wait_until="load", timeout=120000)
    pg.wait_for_selector('[data-nli="%s"] .nli__fig' % tool, timeout=60000)
    print(pg.evaluate(JS, tool)); b.close()
