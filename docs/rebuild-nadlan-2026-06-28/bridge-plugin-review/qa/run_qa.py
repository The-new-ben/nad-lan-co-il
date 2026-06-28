from pathlib import Path
import base64, json, mimetypes, re, os, html
from playwright.sync_api import sync_playwright
BASE=Path('/mnt/data/nadlan_bridge_build/nadlan-content-showroom-bridge')
QA=Path('/mnt/data/nadlan_bridge_build/qa')
QA.mkdir(parents=True, exist_ok=True)
css=(BASE/'assets/bridge.css').read_text()
js=(BASE/'assets/bridge.js').read_text()

def data_uri(path):
    p=Path(path)
    mime=mimetypes.guess_type(str(p))[0] or 'application/octet-stream'
    return 'data:%s;base64,%s'%(mime, base64.b64encode(p.read_bytes()).decode())
poster=data_uri(BASE/'assets/engine/models/ashira-poster.jpg')
facade=data_uri(BASE/'assets/engine/models/ashira-facade.jpg')
plan4=data_uri(BASE/'assets/plans/plan-4br.svg')
plan5=data_uri(BASE/'assets/plans/plan-5br.svg')
plan3=data_uri(BASE/'assets/plans/plan-3br.svg')

def payload(lang='he'):
    return {
      'lang':lang,
      'languages':['he','en','fr','ru','ar'],
      'config':{'default_lang':lang,'home_url':'/','catalog_url':'/projects/','lead_endpoint':''},
      'project':{
        'slug':'ashira-sde-dov','title':'Ashira','area_label':'רובע שדה דב · תל אביב','floors':20,
        'poster':poster,'facade':facade,'model':'','avg_price_per_sqm':77000,
        'content':{
          'he':{'hero_p':'דירות חדשות מול הים בשדה דב. בוחרים דירה מתוך הבניין, רואים קומה, כיוון ונוף, ובודקים אומדן מחיר וסביבה לפני פנייה.','seo_h':'דירות למכירה ב-Ashira שדה דב: מה לבדוק לפני בחירה','seo_p':'בחירת דירה ב-Ashira אינה רק מספר חדרים. רוכש רציני צריך להבין את הקומה, הכיוון, הנוף, המרחק לים והרובע המתפתח סביב הפרויקט.'},
          'en':{'hero_p':'New seafront homes in Sde Dov. Choose an apartment from the building, see floor, facing and view, and check the neighborhood before you enquire.','seo_h':'Ashira Sde Dov apartments for sale: what to check before choosing','seo_p':'Choosing a home at Ashira is not only a room count. Buyers need to understand the floor, facing, view, sea proximity and the district around the project.'}
        },
        'units':[
          {'id':'ashira-18-west','floor':18,'rooms':5,'sqm':132,'balcony':18,'dir':'west','status':'available','view':'ים וארובת רידינג','stage_x':42,'stage_y':30,'plan':plan5},
          {'id':'ashira-14-city','floor':14,'rooms':4,'sqm':104,'balcony':12,'dir':'east','status':'available','view':'רובע שדה דב והעיר','stage_x':58,'stage_y':42,'plan':plan4},
          {'id':'ashira-10-corner','floor':10,'rooms':4,'sqm':118,'balcony':14,'dir':'south-west','status':'reserved','view':'ים וחצר פנימית','stage_x':32,'stage_y':56,'plan':plan4},
          {'id':'ashira-07-east','floor':7,'rooms':3,'sqm':82,'balcony':10,'dir':'east','status':'sold','view':'חזית עירונית','stage_x':64,'stage_y':66,'plan':plan3},
          {'id':'ashira-04-garden','floor':4,'rooms':3,'sqm':92,'balcony':16,'dir':'west','status':'available','view':'גן, ים ושדרה','stage_x':48,'stage_y':78,'plan':plan3}
        ],
        'comps':[
          {'address':'שדה דב 4','rooms':4,'sqm':115,'price':'₪8.9M','date':'04/2026'},
          {'address':'המעגן 11','rooms':4,'sqm':122,'price':'₪9.4M','date':'03/2026'},
          {'address':'נמל ת״א 9','rooms':5,'sqm':140,'price':'₪11.2M','date':'02/2026'}
        ]
      }
    }

def html_for(payload, kind='showroom'):
    cls='nlcb-showroom' if kind=='showroom' else 'nlcb-gallery-root'
    return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>%s</style></head><body style="margin:0;background:#FAF7F1"><div class="nlcb-shell %s" data-payload="%s"></div><script>%s</script></body></html>'%(css,cls,html.escape(json.dumps(payload,ensure_ascii=False), quote=True),js)

def gallery_payload(lang='he'):
    p=payload(lang)['project']
    p2=json.loads(json.dumps(p)); p2['title']='Rainbow'; p2['poster']=data_uri(BASE/'assets/engine/models/rainbow-poster.jpg'); p2['facade']=data_uri(BASE/'assets/engine/models/rainbow-facade.jpg'); p2['slug']='rainbow-tel-aviv'; p2['url']='/projects/rainbow-tel-aviv/'
    p3=json.loads(json.dumps(p)); p3['title']='דימרי ימה'; p3['poster']=data_uri(BASE/'assets/engine/models/dimri-poster.jpg'); p3['facade']=data_uri(BASE/'assets/engine/models/dimri-facade.jpg'); p3['slug']='dimri-yama'; p3['url']='/projects/dimri-yama/'
    p['url']='/projects/ashira-sde-dov/'
    return {'lang':lang,'languages':['he','en','fr','ru','ar'],'config':{'home_url':'/','catalog_url':'/projects/'},'projects':[p,p2,p3]}

# save preview html files with data URIs
for name, pay, kind in [('project-he',payload('he'),'showroom'),('project-en',payload('en'),'showroom'),('gallery-he',gallery_payload('he'),'gallery')]:
    (BASE/'previews'/(name+'.html')).write_text(html_for(pay,kind),encoding='utf-8')

report=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'])
    for name,pay,kind,viewport in [
        ('desktop-he',payload('he'),'showroom',{'width':1440,'height':1200}),
        ('desktop-en',payload('en'),'showroom',{'width':1440,'height':1200}),
        ('mobile-he',payload('he'),'showroom',{'width':390,'height':844}),
        ('mobile-en',payload('en'),'showroom',{'width':390,'height':844}),
        ('gallery-desktop-he',gallery_payload('he'),'gallery',{'width':1440,'height':1100}),
    ]:
        page=browser.new_page(viewport=viewport)
        errors=[]
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        page.set_content(html_for(pay,kind), wait_until='load')
        page.wait_for_timeout(500)
        if kind=='showroom':
            # interaction checks
            page.click('[data-view="facade"]')
            page.wait_for_timeout(100)
            page.click('[data-unit="ashira-10-corner"]')
            page.wait_for_timeout(200)
            selected=page.eval_on_selector('[name="unit"]','el=>el.value')
        else:
            selected='n/a'
        sw=page.evaluate('document.documentElement.scrollWidth')
        iw=page.evaluate('window.innerWidth')
        text=page.evaluate('document.body.innerText')
        leaks={term:text.count(term) for term in ['GLB','BIM','hotspot','mesh','Lovable','Codex','Featured','Sponsored','⟦','—']}
        direction=page.eval_on_selector('.nlcb-shell','el=>({dir:el.getAttribute("dir"),lang:el.getAttribute("lang")})')
        shot=QA/(name+'.png')
        page.screenshot(path=str(shot), full_page=True)
        report.append({'name':name,'screenshot':shot.name,'viewport':viewport,'dir':direction,'scroll_width':sw,'inner_width':iw,'overflow':sw>iw,'selected_unit':selected,'errors':errors,'leaks':leaks})
        page.close()
    browser.close()

md=['# NadLan Content Showroom Bridge QA','', 'Generated in sandbox with Chromium using inline static previews. This is not live WordPress QA.','']
for r in report:
    md.append('## '+r['name'])
    md.append('- screenshot: '+r['screenshot'])
    md.append('- viewport: '+str(r['viewport']))
    md.append('- lang/dir: '+json.dumps(r['dir'],ensure_ascii=False))
    md.append('- selected unit after click: '+str(r['selected_unit']))
    md.append('- horizontal overflow: '+str(r['overflow'])+' (scrollWidth '+str(r['scroll_width'])+', innerWidth '+str(r['inner_width'])+')')
    md.append('- JS errors: '+(json.dumps(r['errors'],ensure_ascii=False) if r['errors'] else 'none'))
    md.append('- visible leak counts: '+json.dumps(r['leaks'],ensure_ascii=False))
    md.append('')
(QA/'report.md').write_text('\n'.join(md),encoding='utf-8')
print('\n'.join(md[:80]))
