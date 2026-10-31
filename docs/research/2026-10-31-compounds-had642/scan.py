import csv,re,html,random,sys,json,urllib.request,concurrent.futures as cf
rows=[r for r in csv.DictReader(open(sys.argv[1],encoding='utf-8')) if 'nadlan_project' in r['sitemap']]
heb=[r['url'] for r in rows if '%d7' in r['url'].lower()]
random.seed(7); sample=random.sample(heb,80)
def get(u):
    try:
        req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 nadlan-audit'})
        return u,urllib.request.urlopen(req,timeout=40).read().decode('utf-8','replace')
    except Exception as e: return u,'ERR '+str(e)
out=[]
with cf.ThreadPoolExecutor(8) as ex:
    for u,s in ex.map(get,sample):
        if s.startswith('ERR'): out.append({'u':u,'err':s[:80]}); continue
        m=re.search(r'<main.*?</main>',s,re.S); main=m.group(0) if m else s
        body=re.sub(r'<script.*?</script>|<style.*?</style>','',main,flags=re.S)
        txt=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',body)))
        h1=re.findall(r'<h1[^>]*>(.*?)</h1>',s,re.S); h1=html.unescape(re.sub('<[^>]+>','',h1[0])).strip() if h1 else ''
        h1pos=txt.find(h1[:12]) if h1 else -1
        km=[float(x) for x in re.findall(r'(\d+(?:\.\d+)?) ק״מ',txt)]
        out.append({'u':u,'h1':h1,'gov':'data.gov.il' in txt,'robots':re.findall(r'<meta name="robots" content="([^"]+)"',s)[:1],
          'words':len(txt.split()),'h1pos':h1pos,'abbr':bool(re.search(r'\b(ר"ג|ת"א|פ"ת|ב"ב|ר"ל|ק"א|ב"ש|ר"ע)',h1)),
          'tlatmemad':txt.count('תלת ממד'),'cmp_far':sum(1 for k in km if k>=2),'cmp_n':len(km),
          'video_call':'הדגם, הקומות, הנוף' in txt,'stage':re.findall(r'סטטוס (\S+ \S+ \S+)',txt)[:1],
          'type':re.findall(r'סוג פרויקט (\S+)',txt)[:1],'units':re.findall(r'יחידות דיור (\d+)',txt)[:1],
          'title':html.unescape(re.findall(r'<title>(.*?)</title>',s,re.S)[0]) if '<title>' in s else ''})
json.dump(out,open('scan.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
ok=[o for o in out if 'err' not in o]
print('fetched',len(ok),'errors',len(out)-len(ok))
print('gov-source pages',sum(o['gov'] for o in ok))
g=[o for o in ok if o['gov']]
import statistics as st
print('noindex',sum(1 for o in g if o['robots'] and 'noindex' in o['robots'][0]))
print('median words in main',st.median(o['words'] for o in g))
print('H1 not first (text before it >150 chars)',sum(1 for o in g if o['h1pos']>150))
print('abbrev in H1',sum(o['abbr'] for o in g),[o['h1'] for o in g if o['abbr']][:6])
print('"תלת ממד" visible',sum(1 for o in g if o['tlatmemad']))
print('comparison rows >=2km: pages',sum(1 for o in g if o['cmp_far']),'of',sum(1 for o in g if o['cmp_n']))
print('video-call text promising model/floors/view',sum(o['video_call'] for o in g))
from collections import Counter
print('types',Counter((o['type'] or ['?'])[0] for o in g).most_common())
print('stages',Counter((o['stage'] or ['?'])[0] for o in g).most_common(8))
print('titles sample',[o['title'][:70] for o in g[:5]])
