import re, json, sys
lines=open(sys.argv[1],encoding='utf-8').read().split('\n')
def num(s):
    s=s.replace('€','').replace('.','').replace(',','.').strip()
    return float(s)
def pct(s):
    return float(s.strip('()%').replace(',','.').replace('+',''))/100
out={'sale':{},'rent':{}}
section=None
i=0
bands=['έως 80 τμ','81 έως 120 τμ','121 τμ και άνω']
while i<len(lines):
    l=lines[i]
    if l.startswith('Τιμές ακινήτων προς πώληση'): section='sale'
    if l.startswith('Τιμές ακινήτων προς ενοικίαση'): section='rent'
    if section and i+1<len(lines) and lines[i+1]=='Διαθέσιμα ακίν.':
        area=l
        j=i+2
        rec={'listings':{},'price':{}}
        mode='listings'
        while j<len(lines) and j<i+60:
            if lines[j]=='Τιμή ακινήτου ανά τ.μ.': mode='price'
            if lines[j] in bands:
                b=lines[j]
                try:
                    a,b2,c=lines[j+1],lines[j+2],lines[j+3]
                    if mode=='listings':
                        rec['listings'][b]=[num(a),num(b2),pct(c)]
                    else:
                        rec['price'][b]=[num(a),num(b2),pct(c)]
                except Exception as e:
                    rec.setdefault('err',[]).append(str(e))
                j+=4; continue
            if j>i+3 and j+1<len(lines) and lines[j+1]=='Διαθέσιμα ακίν.': break
            j+=1
        out[section][area]=rec
        i=j; continue
    i+=1
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out['sale']),len(out['rent']))
print(list(out['sale'])); print(list(out['rent']))
