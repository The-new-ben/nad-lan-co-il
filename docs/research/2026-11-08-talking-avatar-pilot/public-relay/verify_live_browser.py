"""Anonymous native Chrome production smoke, explicit --go only.

No route interception, response fixtures, backend substitution or private credentials.
Exactly one logical identity question is attempted. A real unavailable response
is retained as unavailable, never counted as a successful conversation.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE='https://nad-lan.co.il'
URL=BASE+'/en/buy-property-in-israel/'
API='/wp-json/nadlan-talk/v1'
OUT=ROOT/'evidence'/'public-relay'/'live-browser'


GEOMETRY='''() => {
 const box=element=>{const b=element.getBoundingClientRect();return {x:b.x,y:b.y,width:b.width,height:b.height,left:b.left,right:b.right,top:b.top,bottom:b.bottom};};
 const root=document.querySelector('.nl3d'),rect=box(root);
 const obstacles=[...new Set(document.querySelectorAll('#nlcta,#nla11y,.nlcta,.nla11y,[data-avatar-obstacle]'))]
  .filter(e=>e.getClientRects().length).map(e=>({id:e.id,box:box(e)}))
  .filter(x=>x.box.width>0&&x.box.height>0&&x.box.bottom>0&&x.box.top<innerHeight)
  .map(x=>({...x,overlap:rect.left<x.box.right&&rect.right>x.box.left&&rect.top<x.box.bottom&&rect.bottom>x.box.top}));
 return {viewport:{width:innerWidth,height:innerHeight},avatar:rect,obstacles,
  controls:[...root.querySelectorAll('button')].filter(e=>e.getClientRects().length).map(e=>({label:e.getAttribute('aria-label'),...box(e)}))};
}'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',action='store_true',help='run only after the deployment owner confirms ready')
    args=parser.parse_args()
    manifest=json.loads((ROOT/'public-package'/'manifest.json').read_text())
    release=manifest['releaseId']
    assets=BASE+'/wp-content/uploads/nadlan-avatar/'+release+'/'
    if not args.go:
        print(json.dumps({'prepared':True,'publicRequests':False,'releaseId':release,'requires':'deployment-ready message and --go'}))
        return
    OUT.mkdir(parents=True,exist_ok=True)
    report={'testType':'ANONYMOUS_NATIVE_CHROME_PRODUCTION_SMOKE','url':URL,'expectedRelease':release,
        'routeMocks':False,'backendFixtures':False,'productionCredentialsLoaded':False,
        'permissionTest':'Native Chrome denies microphone permission; no recording is captured.',
        'logicalQuestionLimit':1,'question':'Who are you?','checks':[],'viewports':{},'assetFailures':[],
        'avatarJavaScriptErrors':[],'otherJavaScriptErrors':[],'conversation':{'outcome':'not_attempted'},'startedAt':time.time()}
    def save():
        (OUT/'receipt.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    def check(name,condition,detail=None,required=True):
        report['checks'].append({'name':name,'pass':bool(condition),'detail':detail,'required':required})
        save();print(('PASS ' if condition else 'FAIL ')+name,flush=True)
        if required and not condition:raise AssertionError(name)
    def observe(page):
        def response_seen(response):
            if response.url.startswith(assets) and response.status>=400:
                report['assetFailures'].append({'path':urlsplit(response.url).path,'status':response.status})
        def failed(request):
            if request.url.startswith(assets) and request.failure!='net::ERR_ABORTED':
                report['assetFailures'].append({'path':urlsplit(request.url).path,'failure':request.failure})
        def error_seen(error):
            target='avatarJavaScriptErrors' if 'nadlan-avatar/' in str(error.stack or '') else 'otherJavaScriptErrors'
            report[target].append(str(error))
        page.on('response',response_seen);page.on('requestfailed',failed);page.on('pageerror',error_seen)
    def wait_ready(page):
        response=page.goto(URL,wait_until='domcontentloaded',timeout=60000)
        check('Published guide responds successfully',response is not None and response.status==200)
        page.wait_for_function('window.NLAvatar && NLAvatar.renderer!=="pending"',timeout=45000)
        page.wait_for_selector('.nl3d[data-visible="true"]',timeout=15000)
        check('Live page has exactly the deployed one-page signature',page.locator('script[data-nlag-pilot]').count()==1 and page.locator('script[data-nlag-pilot]').get_attribute('data-nlag-pilot')==release)
        check('Avatar starts silent before a trusted gesture',page.evaluate('NLAvatar.audio.paused && !NLAvatar.diagnostics().started'))
    def greeting(page,name):
        page.locator('.nl3d-face').click()
        page.wait_for_function('!NLAvatar.audio.paused && NLAvatar.audio.currentTime>.2',timeout=15000)
        state=page.evaluate('({audio:NLAvatar.diagnostics().audio,source:NLAvatar.audio.currentSrc,firstInteractionAt:NLAvatar.firstInteractionAt})')
        check(name+' first trusted tap plays the original greeting',state['source']==assets+'assets/greet-en.mp3' and state['audio']['currentTime']>.2 and state['firstInteractionAt'] is not None)
        report['viewports'][name]['greeting']=state
        page.screenshot(path=str(OUT/(name+'-speaking.png')))
    contexts=[]
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(channel='chrome',headless=True,args=['--deny-permission-prompts'])
        try:
            for name,width,height in (('desktop',1440,900),('phone',390,844)):
                context=browser.new_context(viewport={'width':width,'height':height})
                contexts.append(context)
                page=context.new_page();observe(page)
                wait_ready(page)
                page.wait_for_timeout(500)
                geometry=page.evaluate(GEOMETRY);report['viewports'][name]=geometry
                rect=geometry['avatar']
                check(name+' head remains within the viewport',rect['left']>=0 and rect['top']>=0 and rect['right']<=width+1 and rect['bottom']<=height+1)
                check(name+' head keeps its compact dimensions',rect['width']<=178 if width>=900 else rect['width']<=146,{'width':rect['width'],'height':rect['height']})
                check(name+' WhatsApp and accessibility controls are observed',any(item['id']=='nlcta' for item in geometry['obstacles']) and any(item['id']=='nla11y' for item in geometry['obstacles']))
                check(name+' avatar does not overlap WhatsApp or accessibility controls',all(not item['overlap'] for item in geometry['obstacles']))
                page.screenshot(path=str(OUT/(name+'-before.png')))
                greeting(page,name)
                page.locator('.nl3d-cc').click()
                check(name+' captions expose an editable text question',page.locator('.nl3d-caption').is_visible() and page.locator('#nl3d-question').is_editable())
                if name=='desktop':
                    page.locator('.nl3d-close').click()
                    check('Close stops the live greeting',page.evaluate('NLAvatar.audio.paused && NLAvatar.diagnostics().closed'))
                    page.reload(wait_until='domcontentloaded')
                    page.wait_for_function('window.NLAvatar && NLAvatar.state==="closed"',timeout=15000)
                    check('Close persists only in the isolated browser storage',page.locator('.nl3d').count()==0 and page.evaluate('NLAvatar.audio.paused'))
                    context.close();contexts.remove(context)
                    continue

                # Actual HTTPS browser responses and cookie properties; never log the cookie or CSRF value.
                session=page.evaluate('''async api=>{const r=await fetch(api+'/session',{cache:'no-store'});const d=await r.json();return {status:r.status,ready:d.ready,available:d.available,cacheControl:r.headers.get('cache-control')};}''',API)
                health=page.evaluate('''async api=>{const r=await fetch(api+'/health',{cache:'no-store'});return {status:r.status,body:await r.json(),cacheControl:r.headers.get('cache-control')};}''',API)
                report['publicSession']=session;report['publicHealth']=health
                cookie=[item for item in context.cookies(BASE) if item['name']=='nadlan_talk_session']
                flags={'present':len(cookie)==1,'httpOnly':bool(cookie and cookie[0]['httpOnly']),
                       'secure':bool(cookie and cookie[0]['secure']),'sameSite':cookie[0]['sameSite'] if cookie else None}
                check('Actual HTTPS session cookie is Secure HttpOnly Strict',flags['present'] and flags['httpOnly'] and flags['secure'] and flags['sameSite']=='Strict',flags)
                check('Public session and health responses prohibit caching',session['status']==200 and session['ready'] and health['status']==200 and 'no-store' in (session['cacheControl'] or '') and 'no-store' in (health['cacheControl'] or ''))
                page.locator('.nl3d-mic').click()
                page.wait_for_function('document.querySelector(".nl3d-status").textContent==="Mic not allowed"',timeout=15000)
                check('Native microphone permission denial leaves text input usable',page.locator('#nl3d-question').is_editable() and page.locator('.nl3d-text-form [type=submit]').is_enabled(),{'status':page.locator('.nl3d-status').inner_text()})
                page.screenshot(path=str(OUT/'phone-microphone-denied.png'))

                submissions=[]
                def submission_response(response):
                    if response.url==BASE+API+'/converse' and response.request.method=='POST':
                        try:
                            data=response.json()
                            submissions.append({'status':response.status,'cacheControl':response.headers.get('cache-control'),
                                'phase':data.get('phase'),'jobId':data.get('jobId'),'errorCode':data.get('errorCode',data.get('code')),
                                'message':data.get('error',data.get('message'))})
                        except Exception:submissions.append({'status':response.status,'unreadableResponse':True})
                page.on('response',submission_response)
                report['conversation']['readinessBeforeQuestion']=health['body'].get('available') is True
                report['conversation']['probePurpose']='One genuine identity question if ready; otherwise one explicitly authorized rejection probe.'
                page.locator('#nl3d-question').fill('Who are you?')
                began=time.monotonic();page.locator('.nl3d-text-form [type=submit]').click()
                deadline=began+600
                last_state=None
                while time.monotonic()<deadline:
                    page.wait_for_timeout(500)
                    state=page.evaluate('({state:NLAvatar.state,audio:NLAvatar.diagnostics().audio,errors:NLAvatar.errors,reply:NLAvatar.lastReplyText||"",stream:NLAvatar.streamTelemetry,sendEnabled:!document.querySelector(".nl3d-text-form [type=submit]").disabled,caption:document.querySelector(".nl3d-caption-text").textContent})')
                    if state['state']!=last_state:
                        print('Conversation state: '+state['state'],flush=True);last_state=state['state']
                    report['conversation'].update(elapsedSeconds=round(time.monotonic()-began,3),submissions=submissions,state=state)
                    save()
                    if submissions and submissions[-1]['status']>=400 and state['sendEnabled']:
                        report['conversation']['outcome']='unavailable' if submissions[-1]['status']==503 else 'rejected'
                        break
                    if state['sendEnabled'] and state['state']=='waiting' and state['errors']:
                        report['conversation']['outcome']='failed';break
                    if state['sendEnabled'] and state['state']=='ended' and state['reply']:
                        report['conversation']['outcome']='completed';break
                else:
                    report['conversation']['outcome']='timed_out'
                    if page.locator('.nl3d-cancel').is_visible():page.locator('.nl3d-cancel').click()
                outcome=report['conversation']['outcome']
                if outcome=='unavailable':
                    check('Unavailable worker returns an actual503 without a job',submissions[-1]['status']==503 and not submissions[-1].get('jobId'),submissions[-1])
                    check('Unavailable reply is explicitly not presented as success',bool(state['caption']) and state['sendEnabled'] and state['audio']['paused'],{'outcome':outcome,'caption':state['caption']})
                    check('Unavailable response also prohibits caching','no-store' in (submissions[-1].get('cacheControl') or ''))
                elif outcome=='completed':
                    check('One genuine live conversation reaches completed audio',True,{'elapsedSeconds':report['conversation']['elapsedSeconds'],'text':state['reply']})
                    report['conversation']['genuineModelPipeline']='Public relay and worker selected by the deployed owner configuration; no mocked response.'
                else:
                    check('Conversation outcome is recorded without a success claim',False,{'outcome':outcome},required=False)
                page.screenshot(path=str(OUT/'phone-conversation-result.png'))
                page.locator('.nl3d-close').click()
                context.close();contexts.remove(context)

            other=browser.new_context(viewport={'width':1440,'height':900});contexts.append(other)
            page=other.new_page();observe(page)
            response=page.goto(BASE+'/',wait_until='domcontentloaded',timeout=60000)
            page.wait_for_timeout(1800)
            check('Homepage remains outside the one-page pilot',response is not None and response.status==200 and page.locator('script[data-nlag-pilot],.nl3d').count()==0 and page.evaluate('typeof window.NLAvatar==="undefined"'))
            other.close();contexts.remove(other)
            check('No failed public avatar asset request',not report['assetFailures'],report['assetFailures'])
            check('No avatar JavaScript exception',not report['avatarJavaScriptErrors'],report['avatarJavaScriptErrors'])
        except Exception as error:
            report['failure']=type(error).__name__+': '+str(error)
            try:page.screenshot(path=str(OUT/'failure.png'))
            except Exception:pass
            save();raise
        finally:
            for context in contexts:
                try:context.close()
                except Exception:pass
            browser.close()
            report['completedAt']=time.time()
            report['passed']=sum(item['pass'] for item in report['checks'])
            report['total']=len(report['checks'])
            save()
    print(json.dumps({'passed':report['passed'],'total':report['total'],'conversation':report['conversation']['outcome'],'receipt':str(OUT/'receipt.json')}),flush=True)


if __name__=='__main__':main()
