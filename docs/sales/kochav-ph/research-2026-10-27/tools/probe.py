"""Read-only benchmark probe: loads each public page at 390x844 (mobile) and 1280x800 (desktop),
saves first-screen screenshots and measures price / facts / media / CTA positions.
Never clicks, never submits, never logs in. Consent overlays are hidden with CSS only (no click)."""
import sys, json, re, asyncio, os, datetime
from playwright.async_api import async_playwright

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
targets = json.load(open(sys.argv[1], encoding='utf-8'))
SHOTS = sys.argv[2]
OUT = sys.argv[3]
os.makedirs(SHOTS, exist_ok=True)
os.makedirs(os.path.join(SHOTS, 'full'), exist_ok=True)

UA_DESK = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
UA_MOB = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1'

CONSENT_CSS = """
#onetrust-consent-sdk, #onetrust-banner-sdk, .onetrust-pc-dark-filter, #CybotCookiebotDialog, #CybotCookiebotDialogBodyUnderlay,
#didomi-host, #usercentrics-root, #truste-consent-track, .truste_box_overlay, #cookie-law-info-bar, .cky-consent-container,
.cky-overlay, #cmpbox, #cmpbox2, .cc-window, .cookie-banner, #cookie-banner, .cookie-consent, #cookieConsent, #cookie-notice,
[id*='cookie-consent' i], [class*='cookie-consent' i], [id*='cookiebanner' i], [class*='CookieBanner' i], [aria-label*='cookie' i][role='dialog'],
#sp_message_container, .qc-cmp2-container, #qc-cmp2-container, .evidon-banner, #_evidon_banner, .osano-cm-window, #hs-eu-cookie-confirmation
{ display:none !important; visibility:hidden !important; }
html, body { overflow: auto !important; }
"""

PROBE_JS = r"""
(hint) => {
  const vw = innerWidth, vh = innerHeight;
  const sy = scrollY;
  const vis = (el) => { if(!el) return false; const cs = getComputedStyle(el);
    if (cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)===0) return false;
    if (el.checkVisibility && !el.checkVisibility({opacityProperty:true, visibilityProperty:true, contentVisibilityAuto:true})) return false;
    const r = el.getBoundingClientRect(); if (!(r.width>2 && r.height>2)) return false;
    if (cs.clip && cs.clip.startsWith('rect(0')) return false;
    return true; };
  const box = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {y: Math.round(r.top+scrollY), x: Math.round(r.left), w: Math.round(r.width), h: Math.round(r.height),
      fs: parseFloat(cs.fontSize), fw: cs.fontWeight, color: cs.color, ff: cs.fontFamily.split(',')[0].replace(/["']/g,'')}; };
  const txt = (el, n=120) => ((el.innerText||el.textContent||'').replace(/\s+/g,' ').trim()).slice(0,n);
  const all = Array.from(document.querySelectorAll('body *'));
  const curRx = /(₪|\$|US\$|USD|£|GBP|€|EUR|AED|CA\$|ש["״]ח|NIS|ILS)\s?\d[\d,.]*\s?(M|K|million|mil|מיליון|מ['׳])?|\d[\d,.]{3,}\s?(₪|ש["״]ח|AED|USD|EUR|GBP|NIS|ILS|\$)|price\s+(on|upon)\s+(request|application)|\bPOA\b|מחיר\s+לפי\s+בקשה/i;
  // ---- price candidates: smallest elements whose text matches ----
  const cands = [];
  for (const el of all) {
    if (['SCRIPT','STYLE','NOSCRIPT','OPTION','SELECT','svg','path'].includes(el.tagName)) continue;
    const t = txt(el, 200);
    if (!t || t.length > 70) continue;
    if (!curRx.test(t)) continue;
    // deepest: skip if a child also matches
    let childMatch = false;
    for (const c of el.children) { const ct = txt(c, 200); if (ct && ct.length<=70 && curRx.test(ct)) { childMatch = true; break; } }
    if (childMatch) continue;
    if (!vis(el)) continue;
    if (el.closest('nav, footer, select, [role=listbox]')) continue;
    const digits = t.replace(/[^\d]/g,'');
    let val = parseInt(digits||'0',10);
    if (/\d\s?(M|million|mil|מיליון)/i.test(t)) { const m = t.match(/(\d+(?:[.,]\d+)?)\s?(M|million|mil|מיליון)/i); if (m) val = parseFloat(m[1].replace(',','.'))*1e6; }
    const b = box(el);
    cands.push({t, val, digits, ...b, tag: el.tagName, cls: (el.className&&el.className.baseVal===undefined? String(el.className):'').slice(0,60)});
  }
  let price = null;
  if (hint) {
    const h = String(hint);
    const hm = (Number(h)/1e6);
    price = cands.filter(c => c.digits.includes(h) || (c.val>0 && Math.abs(c.val - Number(h)) < 1)).sort((a,b)=>a.y-b.y)[0] || null;
  }
  if (!price) price = cands.filter(c => c.val >= 500000 || /request|application|POA|לפי בקשה/i.test(c.t)).sort((a,b)=>a.y-b.y)[0] || null;
  let priceCtx = null;
  if (price) {
    // find the element again for context
    const el = all.find(e => { const r=e.getBoundingClientRect(); return Math.round(r.top+scrollY)===price.y && Math.round(r.left)===price.x && txt(e,200)===price.t; });
    if (el) {
      let p = el.parentElement, k=0; while (p && txt(p,400).length < 60 && k<6) { p = p.parentElement; k++; }
      priceCtx = p ? txt(p, 260) : null;
    }
  }
  // ---- h1 ----
  const h1all = Array.from(document.querySelectorAll('h1'));
  const h1s = h1all.filter(vis);
  const h1 = h1s.length ? {t: txt(h1s[0], 140), ...box(h1s[0]), count: h1all.length, visibleCount: h1s.length} : null;
  const h1hidden = h1all.filter(e=>!vis(e)).map(e=>({t: txt(e,140), ...box(e)}));
  // largest-font visible short text in first viewport = the headline the eye sees
  let headline = null; const foldTexts = [];
  for (const el of all) {
    if (['SCRIPT','STYLE','NOSCRIPT'].includes(el.tagName)) continue;
    const own = Array.from(el.childNodes).filter(n=>n.nodeType===3).map(n=>n.nodeValue).join(' ').replace(/\s+/g,' ').trim();
    if (!own || own.length<2) continue;
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect(); if (r.top >= vh || r.bottom <= 0) continue;
    const cs = getComputedStyle(el); const fs = parseFloat(cs.fontSize);
    foldTexts.push({t: own.slice(0,80), y: Math.round(r.top+scrollY), fs, fw: cs.fontWeight, tag: el.tagName});
    if (!headline || fs > headline.fs) headline = {t: own.slice(0,100), y: Math.round(r.top+scrollY), fs, fw: cs.fontWeight, ff: cs.fontFamily.split(',')[0].replace(/["']/g,''), tag: el.tagName};
  }
  // inline price: exact substring rect inside any visible text node
  let inlinePrice = null;
  { const rx = /(₪|\$|US\$|USD|£|GBP|€|EUR|AED|CA\$|ש["״]ח|NIS|ILS)?\s?\d{1,3}(?:[,.]\d{3})+(?:\.\d+)?\s?(₪|ש["״]ח|AED|USD|EUR|GBP|NIS|ILS)?|(₪|\$|£|€|AED)\s?\d+(?:\.\d+)?\s?(M|m|million|mil)/g;
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (tw.nextNode()) { const n = tw.currentNode; const v = n.nodeValue; if (!v || !/\d/.test(v)) continue;
      const pe = n.parentElement; if (!pe || ['SCRIPT','STYLE','NOSCRIPT','OPTION'].includes(pe.tagName) || pe.closest('nav,footer,select')) continue;
      rx.lastIndex = 0; let m;
      while ((m = rx.exec(v))) { const s = m[0]; if (!/[₪$£€]|AED|USD|EUR|GBP|NIS|ILS|ש["״]ח/.test(s)) continue;
        let val = parseInt(s.replace(/[^\d]/g,'')||'0',10); const mm = s.match(/(\d+(?:\.\d+)?)\s?(M|m|million|mil)/); if (mm) val = parseFloat(mm[1])*1e6;
        const ok = hint ? (s.replace(/[^\d]/g,'').includes(String(hint)) || Math.abs(val-Number(hint))<1) : val>=500000;
        if (!ok) continue; if (!vis(pe)) continue;
        const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index+s.length); const rr = rg.getBoundingClientRect();
        if (rr.width<2) continue; const cs = getComputedStyle(pe);
        const cand = {t: s.trim(), y: Math.round(rr.top+scrollY), x: Math.round(rr.left), w: Math.round(rr.width), h: Math.round(rr.height), fs: parseFloat(cs.fontSize), fw: cs.fontWeight, tag: pe.tagName, inSentence: v.trim().length > s.length+12, ctx: v.replace(/\s+/g,' ').trim().slice(0,160)};
        if (!inlinePrice || cand.y < inlinePrice.y) inlinePrice = cand; } } }
  // hero media: biggest visual element intersecting the first viewport
  let hero = null;
  for (const el of document.querySelectorAll('img, video, iframe, canvas, picture, [style*="background-image"], div, section, header')) {
    if (!vis(el)) continue; const r = el.getBoundingClientRect(); if (r.top >= vh || r.bottom <= 0) continue;
    const isMedia = ['IMG','VIDEO','IFRAME','CANVAS'].includes(el.tagName) || (getComputedStyle(el).backgroundImage||'').includes('url(');
    if (!isMedia) continue; const ih = Math.min(r.bottom, vh) - Math.max(r.top, 0); const iw = Math.min(r.right, vw) - Math.max(r.left, 0);
    const a = Math.max(0,ih)*Math.max(0,iw); if (!hero || a > hero.area) hero = {tag: el.tagName, area: Math.round(a), share: +(a/(vw*vh)).toFixed(2), y: Math.round(r.top+scrollY), h: Math.round(r.height), w: Math.round(r.width), src: (el.currentSrc||el.src||'').slice(0,100)}; }
  // ---- facts row: first element mentioning beds/rooms/size ----
  const factRx = /(\d+\s*(bed|bd|br\b|bedrooms?|bath|ba\b|rooms?|חדרים|חד'|sq\.?\s?ft|sf\b|ft²|m²|sqm|מ["״]ר|מ״ר|מטר)|קומה\s*\d+|floor\s*\d+)/i;
  let facts = null;
  for (const el of all) {
    const t = txt(el, 200); if (!t || t.length>60 || !factRx.test(t)) continue;
    let childMatch=false; for (const c of el.children){ const ct=txt(c,200); if(ct&&ct.length<=60&&factRx.test(ct)){childMatch=true;break;} }
    if (childMatch || !vis(el) || el.closest('nav, footer, h1, h2, title')) continue;
    const b = box(el); if (!facts || b.y < facts.y) facts = {t, ...b};
  }
  // ---- media ----
  const imgs = Array.from(document.images).filter(i => { const r=i.getBoundingClientRect(); return r.width>=160 && r.height>=110; });
  const firstImg = imgs.filter(i=>vis(i) && !i.closest('header, nav, [class*=menu i]')).map(i=>({src:(i.currentSrc||i.src).slice(0,140), ...box(i)})).sort((a,b)=>a.y-b.y)[0]||null;
  const bigBg = all.filter(e=>{const cs=getComputedStyle(e); if(!cs.backgroundImage||cs.backgroundImage==='none'||!cs.backgroundImage.includes('url(')) return false; const r=e.getBoundingClientRect(); return r.width>=300&&r.height>=200;}).map(e=>box(e)).sort((a,b)=>a.y-b.y)[0]||null;
  const srcset = new Set(Array.from(document.images).map(i=>(i.currentSrc||i.src||'').split('?')[0]).filter(s=>s && !/logo|icon|sprite|avatar|pixel|data:/i.test(s)));
  const videos = Array.from(document.querySelectorAll('video, iframe[src*="youtube"], iframe[src*="vimeo"], iframe[src*="youtu.be"], iframe[data-src*="youtube"], iframe[src*="wistia"]')).map(v=>({tag:v.tagName, src:(v.currentSrc||v.src||v.getAttribute('data-src')||'').slice(0,120), autoplay: v.autoplay||/autoplay=1/.test(v.src||''), ...box(v), visible: vis(v)}));
  const tours = Array.from(document.querySelectorAll('iframe[src*="matterport"], iframe[src*="my.matterport"], iframe[src*="kuula"], iframe[src*="cupix"], iframe[src*="giraffe360"], iframe[src*="tour"]')).map(v=>({src:(v.src||'').slice(0,120), ...box(v)}));
  const maps = Array.from(document.querySelectorAll('iframe[src*="google.com/maps"], iframe[src*="maps.google"], .gm-style, .mapboxgl-map, .maplibregl-map, .leaflet-container, [class*="map-container" i]')).filter(vis).map(m=>({cls:String(m.className).slice(0,50), ...box(m)})).sort((a,b)=>a.y-b.y);
  // ---- text-based markers ----
  const bodyText = (document.body.innerText||'');
  const photoCount = (() => { const m = bodyText.match(/(\d{1,3})\s*(photos|images|pictures|תמונות)/i) || bodyText.match(/\b1\s*\/\s*(\d{1,3})\b/) || bodyText.match(/(\d{1,3})\s*\+\s*(photos|תמונות)?/i); return m ? m[0].slice(0,30) : null; })();
  const firstText = (rx, maxLen=60) => { let best=null; for (const el of all) { if (['SCRIPT','STYLE','NOSCRIPT'].includes(el.tagName)) continue; const t = txt(el,200); if(!t||t.length>maxLen||!rx.test(t)) continue; let cm=false; for(const c of el.children){const ct=txt(c,200); if(ct&&ct.length<=maxLen&&rx.test(ct)){cm=true;break;}} if(cm||!vis(el)) continue; const b=box(el); if(!best||b.y<best.y) best={t,...b,tag:el.tagName}; } return best; };
  const floorplan = firstText(/floor\s?-?plans?|floorplan|תוכנית|תכנית|שרטוט|plan(s)?\b/i);
  const mortgage = firstText(/mortgage|calculator|משכנתא|מחשבון/i, 80);
  const tourTxt = firstText(/virtual tour|3d tour|360|matterport|walkthrough|סיור/i, 60);
  const mapTxt = firstText(/\bmap\b|מפה|location|neighbo(u)?rhood|שכונה/i, 40);
  const ctaRx = /contact|inquire|enquire|schedule|request|book a|book viewing|arrange|call|whatsapp|e-?mail agent|message|צור קשר|תיאום|לתאם|השאר|השאירו|וואטסאפ|ווטסאפ|התקשר|לפרטים|ייעוץ|שלח/i;
  const ctas = Array.from(document.querySelectorAll('a, button, [role=button], input[type=submit]')).filter(e=>{const t=txt(e,80)||e.value||e.getAttribute('aria-label')||''; return ctaRx.test(t) && vis(e) && !e.closest('footer');}).map(e=>({t: (txt(e,60)||e.value||e.getAttribute('aria-label')||'').slice(0,60), ...box(e)})).sort((a,b)=>a.y-b.y).slice(0,6);
  const tel = Array.from(document.querySelectorAll('a[href^="tel:"]')).filter(vis).map(e=>box(e).y).sort((a,b)=>a-b);
  const wa = Array.from(document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp"]')).filter(vis).map(e=>box(e).y).sort((a,b)=>a-b);
  const mail = Array.from(document.querySelectorAll('a[href^="mailto:"]')).filter(vis).length;
  const forms = Array.from(document.querySelectorAll('form')).filter(vis).map(f=>({inputs: f.querySelectorAll('input,textarea').length, y: box(f).y})).filter(f=>f.inputs>=2).sort((a,b)=>a.y-b.y);
  // fixed / sticky bars
  const fixed = [];
  for (const el of all) { const cs = getComputedStyle(el); if (cs.position!=='fixed' && cs.position!=='sticky') continue; if(!vis(el)) continue; const r=el.getBoundingClientRect(); if (r.width*r.height < 1500) continue; if (r.width>=vw*0.95 && r.height>=vh*0.9) continue; fixed.push({pos: cs.position, top: Math.round(r.top), bottom: Math.round(vh-r.bottom), w: Math.round(r.width), h: Math.round(r.height), t: txt(el,90)}); }
  const agentTxt = firstText(/listing agent|agent|broker|advisor|negotiator|סוכן|מתווך|תיווך|realtor/i, 50);
  const pdf = Array.from(document.querySelectorAll('a[href$=".pdf"], a[href*=".pdf?"]')).map(a=>txt(a,40)||a.href.slice(-40)).slice(0,5);
  const blocked = /just a moment|access denied|captcha|are you a robot|רובוט|pardon our interruption|verify you are human|attention required/i.test(document.title + ' ' + bodyText.slice(0,600));
  return {vw, vh, docH: document.documentElement.scrollHeight, title: document.title, blocked,
    price, priceCtx, inlinePrice, headline, h1hidden, hero, foldTexts: foldTexts.sort((a,b)=>b.fs-a.fs).slice(0,14), priceCands: cands.sort((a,b)=>a.y-b.y).slice(0,8).map(c=>({t:c.t,y:c.y,fs:c.fs})),
    h1, facts, firstImg, bigBg, imgUnique: srcset.size, imgBig: imgs.length, videos: videos.slice(0,5), tours, maps: maps.slice(0,3),
    photoCount, floorplan, mortgage, tourTxt, mapTxt, ctas, tel, wa, mail, forms: forms.slice(0,3), fixed: fixed.slice(0,8), agentTxt, pdf,
    textLen: bodyText.length};
}
"""

async def capture(browser, t, mode):
    name, url, hint = t['name'], t['url'], t.get('hint')
    if mode == 'm':
        ctx = await browser.new_context(viewport={'width':390,'height':844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                                        user_agent=UA_MOB, locale=t.get('locale','en-US'))
    else:
        ctx = await browser.new_context(viewport={'width':1280,'height':800}, device_scale_factor=1, user_agent=UA_DESK, locale=t.get('locale','en-US'))
    await ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    page = await ctx.new_page()
    w = 390 if mode=='m' else 1280
    res = {'name': name, 'url': url, 'width': w, 'read_at_utc': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
    try:
        r = await page.goto(url, wait_until='load', timeout=75000)
        res['status'] = r.status if r else None
        await page.wait_for_timeout(t.get('wait', 6000))
        res['final_url'] = page.url
        # raw first screen (with whatever overlays a first-time visitor sees)
        raw = os.path.join(SHOTS, f"{name}-{w}-raw.png")
        await page.screenshot(path=raw)
        await page.add_style_tag(content=CONSENT_CSS)
        await page.wait_for_timeout(600)
        clean = os.path.join(SHOTS, f"{name}-{w}.png")
        await page.screenshot(path=clean)
        res['top'] = await page.evaluate(PROBE_JS, hint)
        # scroll through to trigger lazy content, then measure again
        H = await page.evaluate('document.documentElement.scrollHeight')
        y = 0
        step = 700 if mode=='m' else 650
        while y < min(H, 30000):
            y += step
            await page.evaluate(f'window.scrollTo(0,{y})')
            await page.wait_for_timeout(250)
            H = await page.evaluate('document.documentElement.scrollHeight')
        await page.wait_for_timeout(1200)
        await page.evaluate('window.scrollTo(0,0)')
        await page.wait_for_timeout(1200)
        res['after'] = await page.evaluate(PROBE_JS, hint)
        # full page reference (jpeg, capped)
        try:
            Hc = min(await page.evaluate('document.documentElement.scrollHeight'), 14000 if mode=='m' else 9000)
            await page.screenshot(path=os.path.join(SHOTS, 'full', f"{name}-{w}-full.jpg"), full_page=True, type='jpeg', quality=45,
                                  clip={'x':0,'y':0,'width':w,'height':Hc})
        except Exception as e:
            res['full_err'] = str(e)[:120]
    except Exception as e:
        res['error'] = str(e)[:300]
        try:
            await page.screenshot(path=os.path.join(SHOTS, f"{name}-{w}-raw.png"))
        except Exception:
            pass
    await ctx.close()
    return res

async def main():
    sem = asyncio.Semaphore(int(os.environ.get('PAR', '4')))
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, headless=True, args=['--disable-blink-features=AutomationControlled'])
        async def run(t, m):
            async with sem:
                r = await capture(b, t, m)
                print('done', t['name'], m, r.get('status'), r.get('error','')[:80], flush=True)
                return r
        res = await asyncio.gather(*[run(t, m) for t in targets for m in ('m','d')])
        await b.close()
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

asyncio.run(main())
