import json,sys,glob,re
rows={}
for f in sys.argv[1:]:
    for l in open(f,encoding='utf-8'):
        try: d=json.loads(l)
        except: continue
        for k,v in d.items():
            if isinstance(v,dict) and 'u' in v: rows[k]=v
fam={}
for slug,v in rows.items():
    if slug.startswith('%') or re.match(r'^\d+-%',slug): continue
    m=re.match(r'^(.*)-(en|fr|ru|ar)$',slug)
    base,lang=(m.group(1),m.group(2)) if m else (slug,'he')
    fam.setdefault(base,{})[lang]=v
COLS=[('tower','מגדל 3D'),('floorView','נוף לפי קומה'),('designer','מעצב'),('call','שיחת וידאו'),('basket','סל/RFP'),('alert','התראת מחיר'),('film','סרט'),('v360','360'),('surr','סביבה')]
def cell(v,c):
    if c=='designer': return bool(v.get('designerStep') or v.get('rowDesign') or v.get('designerProj'))
    if c=='call': return bool(v.get('rowCall') or v.get('call'))
    if c=='basket': return bool(v.get('slotFilled') or v.get('basket'))
    if c=='film': return bool(v.get('film') or v.get('rowFilm'))
    if c=='v360': return bool(v.get('v360') or v.get('rowTour'))
    return bool(v.get(c))
FLAG=['rainbow-tel-aviv','duo-tel-aviv','ashira-sde-dov','dimri-yama-sde-dov','h-infinity-somail-tel-aviv','hamedina','first-sde-dov','gindi-vogue-sde-dov','einstein-tower']
order=FLAG+sorted(b for b in fam if b not in FLAG)
out=['| פרויקט | שפה | '+' | '.join(n for _,n in COLS)+' |','|'+'---|'*(len(COLS)+2)]
tot={c:[0,0] for c,_ in COLS}; js=[]
for b in order:
    if b not in fam: continue
    for lang in ['he','en','fr','ru','ar']:
        v=fam[b].get(lang)
        if not v:
            if b in FLAG: out.append('| %s | %s | %s |'%(b,lang,' | '.join(['אין דף']*len(COLS))))
            continue
        cs=[]
        for c,_ in COLS:
            ok=cell(v,c); tot[c][0]+=ok; tot[c][1]+=1; cs.append('✓' if ok else '✗')
        out.append('| %s | %s | %s |'%(b,lang,' | '.join(cs)))
        js.append({'base':b,'lang':lang,**{c:cell(v,c) for c,_ in COLS}})
out.append('| **סה"כ** | | '+' | '.join('%d/%d'%tuple(tot[c]) for c,_ in COLS)+' |')
print('\n'.join(out)); json.dump(js,open('parity.json','w',encoding='utf-8'),ensure_ascii=False)
