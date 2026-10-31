import csv,json,re,urllib.parse,collections,sys
D=r'C:\Users\777\nad-lan\nad-lan-co-il\docs\research\2026-11-01-keyword-map'
qp=list(csv.DictReader(open(D+r'\gsc-query-page-90d.csv',encoding='utf-8')))
qo=list(csv.DictReader(open(D+r'\gsc-query-90d.csv',encoding='utf-8')))
def norm(s):
    s=s.lower()
    s=re.sub(r'(^|\s)ת["״]?א(?=\s|$)',r'תל אביב',s)
    s=re.sub(r'(^|\s)פ["״]?ת(?=\s|$)',r'פתח תקווה',s)
    for a,b in [('״',''),('"',''),("'",''),('׳',''),('-',' '),('פרוייקט','פרויקט'),('פנטהאוס','פנטהאוז'),('פנטאוז','פנטהאוז'),('פנטהואז','פנטהאוז'),('קריית','קרית'),('פתח תקוה','פתח תקווה'),('גבעתים','גבעתיים'),('תל אביב יפו','תל אביב'),('ראשלצ','ראשון לציון')]:
        s=s.replace(a,b)
    return re.sub(r'\s+',' ',s).strip()
CITIES={'תל אביב':['תל אביב','tel aviv','telaviv'],'רמת גן':['רמת גן','ramat gan'],'גבעתיים':['גבעתיים','givatayim'],'הרצליה':['הרצליה','herzliya'],'פתח תקווה':['פתח תקווה','petah tikva','petach tikva'],'בת ים':['בת ים','bat yam'],'חולון':['חולון','holon'],'ראשון לציון':['ראשון לציון','rishon'],'רמת השרון':['רמת השרון','ramat hasharon'],'קרית אונו':['קרית אונו','kiryat ono'],'בני ברק':['בני ברק','bnei brak'],'אילת':['אילת','eilat']}
OTHER=['ירושלים','חיפה','נתניה','אשדוד','באר שבע','אשקלון','רחובות','כפר סבא','רעננה','מודיעין','חדרה','נהריה','לוד','רמלה','יבנה','הוד השרון','דובאי','קפריסין','יוון']
def city_of(q):
    found=[c for c,vs in CITIES.items() if any(v in q for v in vs)]
    if 'אילת' in found:
        # Eilat street in another city: "אילת 22 חולון", "מתחם אילת רמת השרון"
        if re.search(r'אילת \d',q) or len(found)>1 or any(o in q for o in OTHER): found=[c for c in found if c!='אילת']
    if 'רמת השרון' in found and 'רמת גן' in found: pass
    return found
def intent_of(q):
    if any(w in q for w in ['פינוי','התחדשות','תמא','תמ"א','tama','pinui','urban renewal']): return 'renewal'
    if 'פנטהאוז' in q or 'penthouse' in q: return 'penthouse'
    if 'יוקר' in q or 'luxury' in q: return 'luxury'
    if 'קו ראשון' in q or 'מול הים' in q or 'על הים' in q or 'נוף לים' in q or 'seafront' in q: return 'seafront'
    if 'מגדל' in q: return 'towers'
    if 'פרויקט' in q or 'project' in q or ('דיר' in q and ('חדש' in q or 'מקבלן' in q)) or 'קבלן' in q or 'new apartment' in q: return 'newproj'
    if 'השכר' in q or 'שכירות' in q or 'שכר דירה' in q or 'rent' in q: return 'rent'
    if 'השקע' in q or 'invest' in q: return 'invest'
    if 'מחיר' in q or 'כמה עול' in q or 'שווי' in q or 'price' in q or 'עסקאות' in q or 'הערכת' in q: return 'prices'
    if 'למכיר' in q or 'for sale' in q or 'מכירה' in q: return 'sale'
    if 'נדלן' in q or 'real estate' in q: return 'nadlan'
    return 'other'
rows=[]
for r in qp:
    q=norm(r['query']); rows.append(dict(q=q,raw=r['query'],page=urllib.parse.unquote(r['page']).replace('https://nad-lan.co.il',''),c=int(r['clicks']),i=int(r['impressions']),p=float(r['position']),cities=city_of(q),intent=intent_of(q)))
json.dump(rows,open('qp_norm.json','w',encoding='utf-8'),ensure_ascii=False)
# bucket report
B=collections.defaultdict(list)
for r in rows:
    for c in r['cities']: B[(c,r['intent'])].append(r)
    if not r['cities'] and r['intent'] in ('penthouse','luxury','seafront','towers'): B[('*',r['intent'])].append(r)
    if r['intent'] in ('penthouse','luxury','seafront') : B[('LUX',r['intent'])].append(r)
def summ(lst):
    i=sum(x['i'] for x in lst); c=sum(x['c'] for x in lst); p=(sum(x['p']*x['i'] for x in lst)/i) if i else 0
    return i,c,p
out=[]
for k in sorted(B,key=lambda k:-summ(B[k])[0]):
    lst=B[k]; i,c,p=summ(lst)
    pages=collections.defaultdict(lambda:[0,0,0.0]); 
    for x in lst: pages[x['page']][0]+=x['i']; pages[x['page']][1]+=x['c']; pages[x['page']][2]+=x['p']*x['i']
    pl=sorted(pages.items(),key=lambda kv:-kv[1][0])
    qs=collections.defaultdict(int)
    for x in lst: qs[x['raw']]+=x['i']
    tq=sorted(qs.items(),key=lambda kv:-kv[1])[:6]
    print(f"\n## {k} impr={i} clicks={c} pos={p:.1f} queries={len(qs)}")
    for pg,(pi,pc,pp) in pl[:6]: print(f"   {pi:5d} {pc:3d} {pp/pi:5.1f} {pg}")
    print('   top q:',' | '.join(f'{a}({b})' for a,b in tq))
