import csv,json,re,urllib.parse,collections
D=r'C:\Users\777\nad-lan\nad-lan-co-il\docs\research\2026-11-01-keyword-map'
exec(open('analyze.py',encoding='utf-8').read().split('rows=[]')[0].split("qp=list")[0])  # imports
src=open('analyze.py',encoding='utf-8').read()
ns={}
exec(src.split('rows=[]')[0],ns)
norm=ns['norm']
STRIP={'תל','רמת','גבעתיים','הרצליה','פתח','בת','חולון','ראשון','קרית','בני','אילת','מרכז','שחמון','שדה','צפון','ישראל'}
def key(s):
    s=norm(s)
    return ' '.join((w[1:] if w.startswith('ב') and w[1:] in STRIP else w) for w in s.split())
qo=list(csv.DictReader(open(D+r'\gsc-query-90d.csv',encoding='utf-8')))
qp=list(csv.DictReader(open(D+r'\gsc-query-page-90d.csv',encoding='utf-8')))
qp28=list(csv.DictReader(open(D+r'\gsc-query-page-28d.csv',encoding='utf-8')))
Q=collections.defaultdict(list)
for r in qo: Q[key(r['query'])].append(r)
P=collections.defaultdict(list)
for r in qp: P[key(r['query'])].append(r)
P28=collections.defaultdict(list)
for r in qp28: P28[key(r['query'])].append(r)
sv={x['keyword']:x for x in json.load(open('sv.json',encoding='utf-8'))['tasks'][0]['result']}
groups=json.load(open('groups.json',encoding='utf-8'))
def pth(u): return urllib.parse.unquote(u).replace('https://nad-lan.co.il','')
res={}
for g,ks in groups.items():
    for k in ks:
        kk=key(k)
        qs=Q.get(kk,[])
        i=sum(int(r['impressions']) for r in qs); c=sum(int(r['clicks']) for r in qs)
        p=(sum(float(r['position'])*int(r['impressions']) for r in qs)/i) if i else None
        pages=collections.defaultdict(lambda:[0,0,0.0])
        for r in P.get(kk,[]):
            pp=pth(r['page']); pages[pp][0]+=int(r['impressions']); pages[pp][1]+=int(r['clicks']); pages[pp][2]+=float(r['position'])*int(r['impressions'])
        pl=[(pp,v[0],v[1],round(v[2]/v[0],1)) for pp,v in sorted(pages.items(),key=lambda kv:-kv[1][0])]
        pages28=collections.defaultdict(lambda:[0,0.0])
        for r in P28.get(kk,[]):
            pp=pth(r['page']); pages28[pp][0]+=int(r['impressions']); pages28[pp][1]+=float(r['position'])*int(r['impressions'])
        pl28=[(pp,v[0],round(v[1]/v[0],1)) for pp,v in sorted(pages28.items(),key=lambda kv:-kv[1][0])]
        x=sv.get(k,{})
        res[k]=dict(group=g,vol=x.get('search_volume'),cpc=x.get('cpc'),comp=x.get('competition'),gsc_impr=i,gsc_clicks=c,gsc_pos=round(p,1) if p else None,variants=[r['query'] for r in qs],pages90=pl[:5],pages28=pl28[:4])
json.dump(res,open('terms.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for k,v in res.items():
    print(f"{v['group'][:3]}|{k}|{v['vol']}|{v['gsc_impr']}/{v['gsc_clicks']}/{v['gsc_pos']}|90:{v['pages90'][:3]}|28:{v['pages28'][:2]}")

# dead-share per term (pages under /city/ or /cities/ answer 410 since 25.8.2026)
for k,v in res.items():
    kk=key(k); dead=0
    for r in P.get(kk,[]):
        pp=pth(r['page'])
        if pp.startswith(('/city/','/cities/')): dead+=int(r['impressions'])
    v['dead_city_impr']=dead
json.dump(res,open('terms.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
