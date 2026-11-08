"""Scoped HAD-682 relay deployment. Read-only plan by default; --go mutates.

Only the exact named relay Code Snippet and nadlan_talk_enabled may change.
No page, shared plugin, DNS, analytics, voice process or public tunnel is changed.
"""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import re
import secrets
import subprocess
import time
import urllib.error
import urllib.request
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parent
HELPER=Path('C:/Users/777/nad-lan/nad-lan-co-il/scripts/skin-a/deployskin.py')
HELPER_STOP='s, h, _ = req("GET", "/wp-json/nadlan/v1/health")'
BASE='https://nad-lan.co.il'
PAGE=BASE+'/en/buy-property-in-israel/'
NAME='HAD682 NadLan one-page talk-back relay'
SNIPPETS='/wp-json/code-snippets/v1/snippets'
OPTION='nadlan_talk_enabled'
PHP='C:/Users/777/tools/php-8.3/php.exe'
OUT=ROOT.parent/'evidence/public-relay/deployment'

class DeployError(RuntimeError): pass
class TransportError(DeployError): pass
class HTTPStatusError(DeployError):
    def __init__(self,message,status):super().__init__(message);self.status=status
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,request,fp,code,message,headers,newurl): return None

def load_request():
    pieces=HELPER.read_text(encoding='utf-8').split(HELPER_STOP,1)
    if len(pieces)!=2:raise DeployError('Private helper boundary changed; review required.')
    prefix=pieces[0].replace('sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")','')
    private={'__name__':'had682_relay_auth'}
    exec(compile(prefix,str(HELPER),'exec'),private)
    if private.get('BASE')!=BASE:raise DeployError('Private helper does not target the approved website.')
    opener=urllib.request.build_opener(NoRedirect())
    private['urllib']=SimpleNamespace(request=SimpleNamespace(Request=urllib.request.Request,urlopen=opener.open),error=urllib.error)
    return private['req']

def digest(value):return hashlib.sha256(value.encode('utf-8')).hexdigest()
def snapshot(value):
    if value is None:return None
    return {k:value[k] for k in ('id','name','code','scope','active','desc','priority','tags') if k in value}
def fingerprint(value):return digest(json.dumps(snapshot(value),sort_keys=True,separators=(',',':')))
def is_enabled(state):return state.get('exists') and state.get('value') not in (False,None,'',0,'0')
def save(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')

def option_bridge(token,route):
    """Fixed option only; best-effort expected-state check, not an atomic DB CAS."""
    assert re.fullmatch(r'[a-f0-9]{48}',token) and re.fullmatch(r'state-[a-f0-9]{16}',route)
    return r'''
/* HAD682 temporary fixed-option bridge. No arbitrary options, paths or PHP execution. */
add_action('rest_api_init',function(){register_rest_route('nadlan-talk-deploy/v1','/__ROUTE__',array(
'methods'=>array('GET','POST'),
'permission_callback'=>function($request){return current_user_can('manage_options')
 && function_exists('rest_get_authenticated_app_password') && rest_get_authenticated_app_password()
 && hash_equals('__TOKEN__',(string)$request->get_header('x-nl-relay-ops'));},
'callback'=>function($request){
 $state=function(){$missing=new stdClass();$v=get_option('nadlan_talk_enabled',$missing);return array('exists'=>$v!==$missing,'value'=>$v===$missing?null:$v);};
 $current=$state();
 if($request->get_method()==='POST'){
  $body=$request->get_json_params();$expected=$body['expected']??null;$desired=$body['desired']??null;
  $valid=function($s){return is_array($s)&&isset($s['exists'])&&is_bool($s['exists'])&&array_key_exists('value',$s)
   && ((!$s['exists']&&$s['value']===null)||($s['exists']&&in_array($s['value'],array(true,false,0,1,'','0','1'),true)));};
  if(!$valid($expected)||!$valid($desired)){return new WP_Error('state','Invalid option state.',array('status'=>400));}
  if($current!==$expected){return new WP_Error('changed','Option changed during deployment.',array('status'=>409));}
  if($desired['exists']){update_option('nadlan_talk_enabled',$desired['value'],false);}else{delete_option('nadlan_talk_enabled');}
  $current=$state();
 }
 return new WP_REST_Response($current,200,array('Cache-Control'=>'private, no-store, max-age=0'));
}));});
'''.replace('__TOKEN__',token).replace('__ROUTE__',route)

class Deployment:
    def __init__(self,request,source,out=OUT):
        self.request=request;self.source=source;self.out=Path(out)
        self.code=re.sub(r'^\s*<\?php\s*','',source,count=1)
        if self.code==source or 'class nadlan_Talk_Relay' not in self.code or "const NS = 'nadlan-talk/v1'" not in self.code:
            raise DeployError('Unexpected relay source; refusing deployment.')
        self.stamp=time.strftime('%Y%m%dT%H%M%S')+'-'+secrets.token_hex(3)
        self.out.mkdir(parents=True,exist_ok=True)
        self.temp_id=None;self.temp_name='tmp-HAD682-relay-option-'+self.stamp
        self.route='state-'+secrets.token_hex(8);self.token=secrets.token_hex(24)
        self.ops='/wp-json/nadlan-talk-deploy/v1/'+self.route
        self.sid=None;self.prior=None;self.prior_option=None;self.changed=False;self.option_changed=False;self.option_after=None
        self.receipt={'scope':{'snippetName':NAME,'option':OPTION,'page':5154,'url':PAGE},'sourceSHA256':digest(source),
                      'snippetCodeSHA256':digest(self.code),'startedAt':self.stamp,'productionChanges':False,'temporaryBridgeRemoved':False}

    def call(self,method,path,body=None,allowed=(200,201),**kwargs):
        try:status,value,headers=self.request(method,path,body,**kwargs)
        except Exception:raise TransportError(method+' request failed; no credential or response content logged.') from None
        if status not in allowed:raise HTTPStatusError(method+' '+path+' returned HTTP '+str(status),status)
        return value,headers

    def snip(self,method,suffix='',body=None,allowed=(200,201,204)):
        return self.call(method,SNIPPETS+suffix,body,allowed=allowed)[0]

    def find(self,name=NAME):
        values=self.snip('GET')
        if not isinstance(values,list):raise DeployError('Unexpected snippet list format.')
        matches=[x for x in values if x.get('name')==name]
        if len(matches)>1:raise DeployError('Duplicate exact snippet names; refusing to choose one.')
        if not matches:return None
        item=self.snip('GET','/'+str(int(matches[0]['id'])))
        if item.get('name')!=name:raise DeployError('Snippet changed while reading.')
        if name==NAME and ('class nadlan_Talk_Relay' not in item.get('code','') or "nadlan-talk/v1" not in item.get('code','')):
            raise DeployError('The matching name is not the expected relay module.')
        return item

    def plan(self,disable=False):
        self.prior=self.find();self.sid=self.prior['id'] if self.prior else None
        plan={**self.receipt,'mode':'disable' if disable else 'deploy','dryRun':True,
              'existingSnippet':None if self.prior is None else {'id':self.sid,'active':bool(self.prior.get('active')),'codeSHA256':digest(self.prior.get('code',''))},
              'priorOption':'Read and backed up through a temporary authenticated endpoint only when --go is used.',
              'actions':(['Set only nadlan_talk_enabled false','Deactivate only the exact named relay snippet'] if disable else
                         ['Back up exact prior relay snippet and option','Create or update only the exact named relay snippet','Activate and verify relay code','Set only nadlan_talk_enabled true','Verify readback and public health route']),
              'cleanup':'Remove this invocation\'s temporary option snippet in finally.',
              'newPaidServices':0,'pageContentChanges':False,'sharedPluginChanges':False,'startsWorker':False}
        save(self.out/('plan-'+self.stamp+'.json'),plan);save(self.out/'plan.json',plan)
        return plan

    def state(self):
        value,_=self.call('GET',self.ops,headers={'X-NL-Relay-Ops':self.token})
        if not isinstance(value,dict) or type(value.get('exists')) is not bool or 'value' not in value:
            raise DeployError('Unexpected option state response.')
        scalar=value['value']
        if (not value['exists'] and scalar is not None) or (value['exists'] and (type(scalar) not in (str,int,bool) or scalar not in (True,False,0,1,'','0','1'))):
            raise DeployError('Unexpected option value; refusing to overwrite it.')
        return value

    def set_state(self,expected,desired):
        try:
            self.call('POST',self.ops,{'expected':expected,'desired':desired},headers={'X-NL-Relay-Ops':self.token})
            self.option_changed=True
        except (TransportError,HTTPStatusError) as error:
            if isinstance(error,TransportError) or error.status>=500:
                # A write may commit before its response is lost. Recover from a fresh
                # read only when it matches our desired value. This is best-effort,
                # not proof of ownership against a simultaneous identical external edit.
                try:
                    recovered=self.state()
                    if recovered!=expected and recovered['exists']==desired['exists'] and bool(is_enabled(recovered))==bool(is_enabled(desired)):
                        self.option_changed=True;self.option_after=recovered;self.receipt['optionWriteAcknowledgmentLost']=True
                except DeployError:self.receipt['optionWriteOutcomeUnknown']=True
            raise
        # A fresh request reads the persisted WordPress type, not its write-time cache.
        actual=self.state()
        self.option_after=actual
        if actual['exists']!=desired['exists'] or (actual['exists'] and bool(is_enabled(actual))!=bool(is_enabled(desired))):
            raise DeployError('Option readback did not match requested state.')
        return actual

    def create_bridge(self):
        created=self.snip('POST',body={'name':self.temp_name,'code':'/* HAD682 fixed-option bridge staging */','scope':'global','active':False})
        self.temp_id=int(created['id'])
        self.snip('PUT','/'+str(self.temp_id),{'name':self.temp_name,'code':option_bridge(self.token,self.route),'scope':'global','active':False})
        self.snip('PUT','/'+str(self.temp_id)+'/activate',{})

    def cleanup_bridge(self):
        # Recover only this exact unique name if creation succeeded but its response was lost.
        item=self.find(self.temp_name)
        if item:
            sid=int(item['id'])
            try:self.snip('PUT','/'+str(sid)+'/deactivate',{})
            except DeployError:pass
            # Still attempt removal if deactivate committed but its response failed.
            try:self.snip('DELETE','/'+str(sid))
            except DeployError:
                if self.find(self.temp_name) is not None:raise
        if self.find(self.temp_name) is not None:raise DeployError('Temporary option snippet still exists.')
        status,_,_=self.request('GET',self.ops,headers={'X-NL-Relay-Ops':self.token})
        if status!=404:raise DeployError('Temporary option endpoint did not disappear.')
        self.receipt['temporaryBridgeRemoved']=True

    def restore_snippet(self):
        current=self.find()
        if current is not None and self.sid is not None and int(current['id'])!=int(self.sid):
            raise DeployError('Relay identity changed; automatic rollback refused.')
        if current is not None and current.get('code') not in (self.code,(self.prior or {}).get('code')):
            raise DeployError('Relay code changed externally; automatic rollback refused.')
        if self.prior is None:
            if current:
                self.snip('PUT','/'+str(current['id'])+'/deactivate',{});self.snip('DELETE','/'+str(current['id']))
            if self.find() is not None:raise DeployError('New relay snippet rollback failed.')
        else:
            if not current:raise DeployError('Prior snippet disappeared; refusing to recreate a different identity.')
            body={k:v for k,v in snapshot(self.prior).items() if k not in ('id','active')}
            body['active']=False
            self.snip('PUT','/'+str(self.sid)+'/deactivate',{})
            self.snip('PUT','/'+str(self.sid),body)
            if self.prior.get('active'):self.snip('PUT','/'+str(self.sid)+'/activate',{})
            restored=self.find()
            if fingerprint(restored)!=fingerprint(self.prior):raise DeployError('Prior snippet readback differs after rollback.')

    def rollback(self):
        result={'attempted':True,'snippetRestored':False,'optionRestored':False}
        try:
            # Never overwrite an intervening option edit when this invocation did not
            # successfully write that option. A failed compare-and-swap is not ownership.
            current=self.state()
            option_owned=self.option_changed and current==self.option_after
            if self.option_changed and not option_owned and current!=self.prior_option:
                result['externalOptionEditPreserved']=True
            if option_owned and is_enabled(current):self.set_state(current,{'exists':True,'value':False})
            self.restore_snippet();result['snippetRestored']=True
            if self.prior_option is not None and option_owned:
                current=self.state();self.set_state(current,self.prior_option)
                result['optionRestored']=self.state()==self.prior_option
                if not result['optionRestored']:raise DeployError('Prior option readback differs.')
            elif self.prior_option is not None:
                result['optionRestored']=self.state()==self.prior_option
                if not result['optionRestored']:result['externalOptionEditPreserved']=True
        except Exception as error:result['error']=str(error)
        self.receipt['rollback']=result
        return result['snippetRestored'] and result['optionRestored']

    def execute(self,disable=False):
        if self.prior is None and self.sid is None:
            # plan() is also needed when there is no prior snippet; it has no mutations.
            self.plan(disable)
        self.receipt['mode']='disable' if disable else 'deploy'
        error=None
        try:
            self.create_bridge()
            self.prior_option=self.state()
            backup={'schema':1,'site':BASE,'snippetName':NAME,'snippet':snapshot(self.prior),'option':{'name':OPTION,**self.prior_option},'sourceSHA256':digest(self.source)}
            backup_path=self.out/('backup-'+self.stamp+'.json');save(backup_path,backup)
            self.receipt['backup']=str(backup_path)
            if fingerprint(self.find())!=fingerprint(self.prior):raise DeployError('Relay changed during staging.')
            if self.state()!=self.prior_option:raise DeployError('Option changed during staging.')
            if disable:
                self.set_state(self.prior_option,{'exists':True,'value':False});self.option_changed=True
                if self.sid is not None:
                    self.changed=True;self.snip('PUT','/'+str(self.sid)+'/deactivate',{})
            else:
                body={'name':NAME,'code':self.code,'scope':'global','active':False}
                self.changed=True
                if self.sid is None:self.sid=int(self.snip('POST',body=body)['id'])
                else:self.snip('PUT','/'+str(self.sid),body)
                staged=self.find()
                if staged.get('code')!=self.code or staged.get('active'):raise DeployError('Inactive relay staging readback differs.')
                self.snip('PUT','/'+str(self.sid)+'/activate',{})
                active=self.find()
                if active.get('code')!=self.code or not active.get('active'):raise DeployError('Relay activation readback differs.')
                self.set_state(self.prior_option,{'exists':True,'value':True});self.option_changed=True
                health,headers=self.call('GET','/wp-json/nadlan-talk/v1/health',auth=False,headers={'Referer':PAGE,'Origin':BASE})
                if not isinstance(health,dict) or 'available' not in health:raise DeployError('Public relay health response is invalid.')
                if 'no-store' not in str(headers.get('Cache-Control',headers.get('cache-control',''))):raise DeployError('Public relay health is missing no-store.')
                self.receipt['health']={'routeResponds':True,'available':health['available'],'unavailableCode':health.get('unavailableCode')}
            final=self.find();state=self.state()
            if bool(is_enabled(state))==bool(disable) or (disable and final and final.get('active')):raise DeployError('Final relay state mismatch.')
            self.receipt.update(productionChanges=True,snippetId=self.sid,snippetActive=bool(final and final.get('active')),optionAfter=state,success=True)
        except BaseException as exc:
            error=exc;self.receipt['success']=False;self.receipt['error']=str(exc) if isinstance(exc,DeployError) else type(exc).__name__
            if self.changed or self.option_changed:self.rollback()
        finally:
            try:self.cleanup_bridge()
            except Exception as cleanup_error:
                self.receipt['cleanupError']=str(cleanup_error);self.receipt['success']=False
                if error is None:error=DeployError('Temporary bridge cleanup failed; inspect the receipt.')
            save(self.out/('receipt-'+self.stamp+'.json'),self.receipt);save(self.out/'latest.json',self.receipt)
        if error:raise DeployError('Relay operation did not complete cleanly. See the saved receipt.') from None
        return self.receipt

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',action='store_true',help='perform the explicitly approved scoped operation')
    parser.add_argument('--disable',action='store_true',help='plan disabling admission and deactivating only this relay; requires --go to mutate')
    args=parser.parse_args()
    path=ROOT/'nadlan-talk-relay.php'
    lint=subprocess.run([PHP,'-l',str(path)],capture_output=True,text=True)
    if lint.returncode:raise DeployError('Relay PHP lint failed.')
    deploy=Deployment(load_request(),path.read_text(encoding='utf-8'))
    plan=deploy.plan(args.disable)
    print(json.dumps({k:plan[k] for k in ('mode','dryRun','existingSnippet','sourceSHA256','pageContentChanges','startsWorker')}))
    if not args.go:return
    receipt=deploy.execute(args.disable)
    print(json.dumps({k:receipt.get(k) for k in ('success','snippetId','snippetActive','optionAfter','temporaryBridgeRemoved','health')}))

if __name__=='__main__':main()
