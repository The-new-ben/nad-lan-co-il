"""One-page authorized pilot. Dry plan by default, scoped files, backup and readback.
Reuses the existing README deployment authentication helper inside this process.
Never prints credentials or modifies measurement configuration.
"""
from pathlib import Path
import argparse,base64,hashlib,json,re,secrets,subprocess,time,urllib.request
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parent
REPO=Path(r'C:\Users\777\nad-lan\nad-lan-co-il')
PAGE=5154
URL='https://nad-lan.co.il/en/buy-property-in-israel/'
START='<!-- nlagent:start -->';END='<!-- nlagent:end -->'
parser=argparse.ArgumentParser();parser.add_argument('--go',action='store_true');parser.add_argument('--conversation',action='store_true');args=parser.parse_args()
helper=(REPO/'scripts/skin-a/deployskin.py').read_text(encoding='utf-8')
private={'__name__':'avatar_deploy_auth'}
exec(compile(helper[:helper.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')],str(REPO/'scripts/skin-a/deployskin.py'),'exec'),private)
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,request,fp,code,message,headers,newurl):return None
opener=urllib.request.build_opener(NoRedirect())
private['urllib']=SimpleNamespace(request=SimpleNamespace(Request=urllib.request.Request,urlopen=opener.open),error=urllib.error)
req=private['req']
def require(status,value,label,allowed=(200,201,204)):
    if status not in allowed:raise RuntimeError(label+' failed: HTTP '+str(status))
    return value
def snippets(method,path='',data=None):
    status,value,_=req(method,'/wp-json/code-snippets/v1/snippets'+path,data)
    return require(status,value,'snippet '+method)
status,page,_=req('GET',f'/wp-json/wp/v2/pages/{PAGE}?context=edit&_fields=id,content,link,status')
require(status,page,'read page')
assert page['id']==PAGE and page['link'].rstrip('/')==URL.rstrip('/') and page['status']=='publish'
raw=page['content']['raw']
assert raw.count(START)==1 and raw.count(END)==1,'Expected exactly one old avatar block'
a=raw.index(START);b=raw.index(END)+len(END)
manifest=json.loads((ROOT/'public-package/manifest.json').read_text(encoding='utf-8'))
release=manifest['releaseId']
assert re.fullmatch(r'v-[a-f0-9]{12}',release)
subdir='nadlan-avatar/'+release
base=URL.split('/en/')[0]+'/wp-content/uploads/'+subdir+'/'
config={'fallbackUrl':base+'assets/portrait-cutout-v2.webp','storageKey':'nlag-closed','revealDelay':0}
if args.conversation:
    api='/wp-json/nadlan-talk/v1'
    config.update(apiBase=api,conversationEndpoint=api+'/converse',sessionEndpoint=api+'/session',healthEndpoint=api+'/health',pollInterval=1000)
block=(START+f'<link rel="stylesheet" href="{base}widget.css">'
       +'<script type="module" data-nlag-pilot="'+release+'">'
       +"if(['/en/buy-property-in-israel/','/en/buy-property-in-israel'].includes(location.pathname)){window.__NL3D="
       +json.dumps(config,separators=(',',':'))+';import('+json.dumps(base+'widget.js')+');}</script>'+END)
new=raw[:a]+block+raw[b:]
module=re.search(r'<script\b[^>]*>(.*?)</script>',block,re.S).group(1)
syntax=subprocess.run(['node','--input-type=module','--check'],input=module,text=True,capture_output=True)
if syntax.returncode:raise RuntimeError('Prepared module syntax failed: '+syntax.stderr)
plan={'page':PAGE,'url':URL,'releaseId':release,'assetBytes':manifest['totalBytes'],'assetFiles':len(manifest['files']),'conversation':args.conversation,'outsideBlockUnchanged':raw[:a]+raw[b:]==new[:a]+new[a+len(block):],'pageBeforeSHA256':hashlib.sha256(raw.encode()).hexdigest(),'pageAfterSHA256':hashlib.sha256(new.encode()).hexdigest(),'newPaidServices':0}
out=ROOT/'evidence/public-deployment';out.mkdir(parents=True,exist_ok=True)
(out/'plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
(out/'prepared-block.html').write_text(block,encoding='utf-8')
print(json.dumps(plan))
if not args.go:raise SystemExit(0)
assert plan['outsideBlockUnchanged']
stamp=time.strftime('%Y%m%dT%H%M%S')
backup=out/f'page-5154-{stamp}-before.html';backup.write_text(raw,encoding='utf-8')
allowed={item['path']:item['sha256'] for item in manifest['files']}
token=secrets.token_hex(24)
bridge=r'''
add_action('rest_api_init',function(){register_rest_route('nadlan-avatar-ops/v1','/asset',array(
'methods'=>'POST','permission_callback'=>function(){return current_user_can('manage_options');},
'callback'=>function($request){$b=$request->get_json_params();
if(!is_array($b)||!hash_equals('__TOKEN__',(string)($b['token']??''))){return new WP_Error('denied','Denied',array('status'=>403));}
$allowed=json_decode('__ALLOWED__',true);$name=(string)($b['path']??'');
if(!isset($allowed[$name])){return new WP_Error('path','Unknown asset',array('status'=>400));}
$data=base64_decode((string)($b['data']??''),true);
if(false===$data||!hash_equals($allowed[$name],hash('sha256',$data))){return new WP_Error('hash','Asset mismatch',array('status'=>400));}
$up=wp_get_upload_dir();$dir=trailingslashit($up['basedir']).'__SUBDIR__/';$target=$dir.$name;
if(!wp_mkdir_p(dirname($target))){return new WP_Error('mkdir','Asset directory unavailable',array('status'=>500));}
if(is_file($target)&&!hash_equals($allowed[$name],hash_file('sha256',$target))){return new WP_Error('existing','Existing asset differs',array('status'=>409));}
if(!is_file($target)&&file_put_contents($target,$data,LOCK_EX)!==strlen($data)){return new WP_Error('write','Asset write failed',array('status'=>500));}
return array('sha256'=>hash_file('sha256',$target),'bytes'=>filesize($target),'url'=>trailingslashit($up['baseurl']).'__SUBDIR__/'.$name);
}));});
'''.replace('__TOKEN__',token).replace('__ALLOWED__',json.dumps(allowed,separators=(',',':'))).replace('__SUBDIR__',subdir)
created=snippets('POST',data={'name':'tmp-nadlan-avatar-assets-'+stamp,'code':'/* scoped asset staging */','scope':'global','active':False})
snippet_id=created['id'];uploaded=[];page_written=False
try:
    snippets('PUT',f'/{snippet_id}',{'name':created['name'],'code':bridge,'scope':'global','active':False})
    snippets('PUT',f'/{snippet_id}/activate',{})
    for item in manifest['files']:
        payload={'token':token,'path':item['path'],'data':base64.b64encode((ROOT/'public-package'/item['path']).read_bytes()).decode()}
        status,result,_=req('POST','/wp-json/nadlan-avatar-ops/v1/asset',payload)
        require(status,result,'asset upload')
        assert result['sha256']==item['sha256'] and result['bytes']==item['bytes']
        with urllib.request.urlopen(urllib.request.Request(result['url']+'?verify='+item['sha256'][:12],headers={'User-Agent':'Mozilla/5.0'}),timeout=90) as response:actual=response.read()
        assert hashlib.sha256(actual).hexdigest()==item['sha256'],'Public asset readback mismatch'
        uploaded.append({'path':item['path'],'url':result['url'],'bytes':len(actual),'sha256':item['sha256']})
    # Re-read immediately before writing; never overwrite another editor's intervening change.
    status,current,_=req('GET',f'/wp-json/wp/v2/pages/{PAGE}?context=edit&_fields=content')
    require(status,current,'pre-write read');assert current['content']['raw']==raw,'Page changed during staging'
    status,result,_=req('POST',f'/wp-json/wp/v2/pages/{PAGE}',{'content':new})
    require(status,result,'page update');page_written=True
    status,readback,_=req('GET',f'/wp-json/wp/v2/pages/{PAGE}?context=edit&_fields=content')
    require(status,readback,'page readback');assert readback['content']['raw']==new,'Page readback differs'
    receipt={**plan,'backup':str(backup),'assets':uploaded,'pageReadbackExact':True,'pageWritten':True}
    (out/f'receipt-{stamp}.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    (out/'latest.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps({'pageWritten':True,'url':URL,'releaseId':release,'assetsVerified':len(uploaded)}))
except BaseException:
    if page_written:
        status,current,_=req('GET',f'/wp-json/wp/v2/pages/{PAGE}?context=edit&_fields=content')
        if status==200 and current['content']['raw']==new:
            status,result,_=req('POST',f'/wp-json/wp/v2/pages/{PAGE}',{'content':raw});require(status,result,'rollback')
    raise
finally:
    # Remove only this task's temporary, authenticated asset uploader.
    snippets('PUT',f'/{snippet_id}/deactivate',{})
    snippets('DELETE',f'/{snippet_id}')
