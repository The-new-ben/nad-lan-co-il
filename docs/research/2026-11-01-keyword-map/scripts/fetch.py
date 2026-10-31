import urllib.request,urllib.parse,re,json,sys,html
paths=['/projects/','/city/תל אביב יפו/projects/','/city/תל-אביב-יפו/projects/','/projects/?city=תל אביב-יפו','/cities/תל-אביב-יפו/','/city/תל-אביב-יפו/',
'/city/רמת גן/projects/','/city/רמת-גן/projects/','/city/רמת-גן/','/city/ראשון לציון/projects/','/city/ראשון-לציון/projects/','/city/ראשון-לציון/',
'/city/הרצליה/projects/','/city/הרצליה/','/city/פתח-תקוה/projects/','/city/בת-ים/projects/','/city/בת-ים/','/city/חולון/','/city/חולון/projects/',
'/city/קרית אונו/projects/','/city/קרית-אונו/projects/','/city/רמת-השרון/projects/','/city/בני-ברק/','/city/בני-ברק/projects/','/city/גבעתים/projects/','/city/גבעתיים/projects/',
'/city/אילת/','/city/אילת/projects/','/eilat-apartment-prices/','/projects/22-צין-פארן/','/projects/6-ברנע/','/projects/שדרות-התמרים-סינג-סינג/',
'/luxury-tel-aviv/','/luxury-apartments-israel-guide-he/','/tel-aviv-penthouse-prices/','/property-value/luxury-apartments-tel-aviv/','/tel-aviv-luxury-apartment-prices/','/tel-aviv-seafront-apartment-prices/','/new-projects/new-projects-tel-aviv/','/herzliya-projects/']
out=[]
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
op=urllib.request.build_opener(NoRedir)
for p in paths:
    u='https://nad-lan.co.il'+urllib.parse.quote(p,safe='/?=&')
    import subprocess,time
    time.sleep(1.2)
    pr=subprocess.run(['curl','-s','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36','-H','Accept: text/html','-w','QQQ%{http_code}QQ%{redirect_url}',u],capture_output=True)
    txt=pr.stdout.decode('utf-8','replace'); m=re.search(r'QQQ(\d+)QQ(.*)$',txt,re.S)
    st=int(m.group(1)); loc=m.group(2); b=txt[:m.start()]
    t=re.search(r'<title[^>]*>(.*?)</title>',b,re.S); h=re.search(r'<h1[^>]*>(.*?)</h1>',b,re.S)
    c=re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)',b) or re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']canonical',b)
    rb=re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)',b)
    clean=lambda s: html.unescape(re.sub(r'<[^>]+>','',s)).strip() if s else ''
    row=dict(path=p,status=st,location=urllib.parse.unquote(loc),title=clean(t.group(1)) if t else '',h1=clean(h.group(1)) if h else '',canonical=urllib.parse.unquote(c.group(1)) if c else '',robots=rb.group(1) if rb else '')
    out.append(row); print(json.dumps(row,ensure_ascii=False))
json.dump(out,open('live-pages.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
