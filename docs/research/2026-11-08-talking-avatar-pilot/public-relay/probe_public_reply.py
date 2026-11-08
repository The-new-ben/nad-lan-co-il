"""One genuine public HTTP question, without a browser or model fixture.

Session/CSRF values stay in memory and are never saved or printed.
This proves public inference and returned audio, not browser playback or microphone input.
"""
from pathlib import Path
import argparse, hashlib, http.cookiejar, io, json, time, urllib.error, urllib.request, uuid, wave
from urllib.parse import urlsplit
from worker import memory_gib

ROOT=Path(__file__).resolve().parents[1]
BASE='https://nad-lan.co.il'
PAGE=BASE+'/en/buy-property-in-israel/'
API='/wp-json/nadlan-talk/v1'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--go',action='store_true')
parser.add_argument('--audio',type=Path,help='Explicit controlled WAV fixture; not a claim of a physical microphone test.')
args=parser.parse_args()
if not args.go:
    print(json.dumps({'prepared':True,'question':'Who are you?','publicRequests':False}))
    raise SystemExit(0)
OUT=ROOT/'evidence/public-relay/real-reply-recovery'
OUT.mkdir(parents=True,exist_ok=True)
if (OUT/'receipt.json').exists():
    previous=(OUT/'receipt.json').read_bytes()
    archive=OUT/('previous-'+hashlib.sha256(previous).hexdigest()[:12]+'.json')
    if not archive.exists():archive.write_bytes(previous)
report={'startedUtc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'testType':'GENUINE_PUBLIC_HTTP_WAV_QUESTION' if args.audio else 'GENUINE_PUBLIC_HTTP_TEXT_QUESTION',
        'question':'Who are you, and how can you help me?' if args.audio else 'Who are you?','modelsMocked':False,'browserPlaybackTested':False,'microphoneTested':False,
        'privateCredentialsLoaded':False,'phases':[],'outcome':'not_submitted'}
jar=http.cookiejar.CookieJar()
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
opener=urllib.request.build_opener(NoRedirect(),urllib.request.HTTPCookieProcessor(jar))
csrf=None
def request(path,method='GET',body=None,binary=False):
    assert path.startswith(API+'/') and not '..' in path
    headers={'User-Agent':'NadLanPilotQA/1.0','Referer':PAGE,'Origin':BASE}
    if csrf:headers['X-NL-CSRF']=csrf
    if body is not None:headers['Content-Type']='application/json'
    req=urllib.request.Request(BASE+path,data=json.dumps(body).encode() if body is not None else None,method=method,headers=headers)
    try:r=opener.open(req,timeout=25)
    except urllib.error.HTTPError as e:r=e
    with r:
        payload=r.read(5*1024*1024)
        return r.status,payload if binary else json.loads(payload)
def save():
    (OUT/'receipt.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
status,session=request(API+'/session')
csrf=session.get('csrf')
report['session']={'status':status,'ready':session.get('ready'),'available':session.get('available')}
report['memoryBeforeGiB']=round(memory_gib(),3)
save()
if status!=200 or not session.get('available') or not csrf:
    report['outcome']='not_ready';save();print(json.dumps(report));raise SystemExit(2)
token='recovery_'+uuid.uuid4().hex
started=time.monotonic()
headers={'User-Agent':'NadLanPilotQA/1.0','Referer':PAGE,'Origin':BASE,'X-NL-CSRF':csrf,
         'X-NL-Request-ID':token,'Content-Type':'application/json'}
payload=json.dumps({'text':report['question']}).encode()
if args.audio:
    recorded=args.audio.read_bytes()
    with wave.open(io.BytesIO(recorded),'rb') as source:duration=source.getnframes()/source.getframerate()
    assert .25<=duration<=20 and len(recorded)<15*1024*1024
    report['controlledInput']={'file':args.audio.name,'sha256':hashlib.sha256(recorded).hexdigest(),'durationSeconds':duration,
        'source':'Local Windows synthesized English test question; not Ben or a physical microphone'}
    boundary='nadlanProbe'+uuid.uuid4().hex
    payload=(f'--{boundary}\r\nContent-Disposition: form-data; name="duration"\r\n\r\n{duration}\r\n'
        f'--{boundary}\r\nContent-Disposition: form-data; name="audio"; filename="controlled-question.wav"\r\n'
        'Content-Type: audio/wav\r\n\r\n').encode()+recorded+f'\r\n--{boundary}--\r\n'.encode()
    headers['Content-Type']='multipart/form-data; boundary='+boundary
req=urllib.request.Request(BASE+API+'/converse',data=payload,headers=headers,method='POST')
job=None;finished=False
try:
    try:r=opener.open(req,timeout=25)
    except urllib.error.HTTPError as e:r=e
    with r: status=r.status;ack=json.load(r)
    report['submitStatus']=status
    if status!=202:
        report.update(outcome='rejected',errorCode=ack.get('code',ack.get('errorCode')));save()
        print(json.dumps({'outcome':report['outcome'],'status':status}));raise SystemExit(3)
    job=ack['jobId'];report['jobId']=job;report['outcome']='running';save()
    poll_retries=0
    while time.monotonic()-started<580:
        status,state=request(API+'/jobs/'+job)
        if status==429 and state.get('code')=='busy' and poll_retries<3:
            delay=2**poll_retries;poll_retries+=1
            event={'elapsedSeconds':round(time.monotonic()-started,3),'status':status,'code':'busy','retryDelaySeconds':delay}
            report.setdefault('transientPollRetries',[]).append(event)
            save();print(json.dumps(event),flush=True);time.sleep(delay);continue
        if status!=200:
            report.update(outcome='poll_failed',pollStatus=status,errorCode=state.get('code',state.get('errorCode')))
            break
        poll_retries=0
        phase=state.get('phase');elapsed=round(time.monotonic()-started,3)
        if not report['phases'] or phase!=report['phases'][-1]['phase']:
            event={'phase':phase,'elapsedSeconds':elapsed,'freeMemoryGiB':round(memory_gib(),3)}
            report['phases'].append(event);print(json.dumps(event),flush=True)
        report['elapsedSeconds']=elapsed
        if phase=='done':
            result=state.get('result',{})
            report['result']=result
            path=result.get('audioUrl','')
            if path.startswith(BASE+'/'):
                parsed=urlsplit(path)
                assert parsed.scheme=='https' and parsed.netloc=='nad-lan.co.il' and not parsed.query and not parsed.fragment
                path=parsed.path
            assert path.startswith(API+'/audio/'+job+'/')
            audioStatus,audio=request(path,binary=True)
            assert audioStatus==200
            with wave.open(io.BytesIO(audio),'rb') as w:
                report['audio']={'frames':w.getnframes(),'rate':w.getframerate(),'channels':w.getnchannels(),
                    'duration':w.getnframes()/w.getframerate(),'bytes':len(audio),'sha256':hashlib.sha256(audio).hexdigest()}
            (OUT/'reply.wav').write_bytes(audio)
            report['outcome']='completed';finished=True;break
        if phase in ('error','cancelled'):
            report.update(outcome=phase,errorCode=state.get('errorCode'));finished=True;break
        if memory_gib()<.30:
            report['outcome']='cancelled_critical_memory';break
        save();time.sleep(2)
    else:report['outcome']='timed_out'
finally:
    if not finished:
        try:request(API+'/requests/'+token+'/cancel','POST',{})
        except Exception:pass
    report['elapsedSeconds']=round(time.monotonic()-started,3)
    report['memoryAfterGiB']=round(memory_gib(),3)
    save()
print(json.dumps({'outcome':report['outcome'],'seconds':report['elapsedSeconds'],'result':report.get('result')}),flush=True)
