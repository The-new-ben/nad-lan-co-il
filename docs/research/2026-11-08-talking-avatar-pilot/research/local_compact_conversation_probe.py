"""Prepare one genuine local multipart speech turn. Only --go submits a request."""
from __future__ import annotations
import argparse
import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import queue
import re
import subprocess
import sys
import threading
import time
import uuid
import wave

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:8770'
SOURCE=ROOT/'evidence/public-relay/real-reply-recovery/controlled-identity-question.wav'
SOURCE_SHA='8753b7990e0c80d0a5ff0574e5e8614fbaf604105be163fefff311c50a0a15f7'
QUESTION='Who are you, and how can you help me?'
TOTAL_SECONDS=240
CANCEL_RESERVE_SECONDS=25
PHYSICAL_FLOOR,COMMIT_FLOOR=.75,1.0
ENTRY_PHYSICAL,ENTRY_COMMIT=2.3,2.5
POLL_SECONDS=.1


def save(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def wav_info(data):
    with wave.open(io.BytesIO(data),'rb') as wav:
        params={'channels':wav.getnchannels(),'sampleRate':wav.getframerate(),
                'sampleWidth':wav.getsampwidth(),'frames':wav.getnframes()}
        pcm=wav.readframes(wav.getnframes())
    return {**params,'seconds':params['frames']/params['sampleRate'],
            'fileSha256':hashlib.sha256(data).hexdigest(),'pcmSha256':hashlib.sha256(pcm).hexdigest()}


def listener_pid():
    result=subprocess.run(['netstat','-ano','-p','tcp'],capture_output=True,text=True,timeout=5)
    matches=[]
    for line in result.stdout.splitlines():
        parts=line.split()
        if len(parts)==5 and parts[0]=='TCP' and parts[1]=='127.0.0.1:8770' and parts[3]=='LISTENING':
            matches.append(int(parts[4]))
    if result.returncode or len(set(matches))!=1:
        raise RuntimeError('Cannot identify the unique IPv4 loopback8770 listener.')
    return matches[0]


def typed_question(value):
    value=value.strip()
    if not value or len(value)>1200 or '\x00' in value:
        raise argparse.ArgumentTypeError('Use one nonempty question of at most 1200 characters.')
    return value


def safe_label(value):
    reserved={'con','prn','aux','nul',*(f'com{i}' for i in range(1,10)),*(f'lpt{i}' for i in range(1,10))}
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',value) or value in reserved:
        raise argparse.ArgumentTypeError('Use a safe lowercase evidence label.')
    return value


def request_payload(token,question=None):
    if question is not None:
        return {'requestId':token,'text':question}
    return {'requestId':token,'audioBase64':base64.b64encode(SOURCE.read_bytes()).decode('ascii'),'mime':'audio/wav'}


def run(label,server_pid,question=None):
    import memory_reclaim_api as memory
    from benchmark_mtl_loader_candidate import ProcessSamples
    from benchmark_qwen_q4_candidate import alive_handles
    spec=importlib.util.spec_from_file_location('local_relay_contract',ROOT/'public-relay/worker.py')
    relay=importlib.util.module_from_spec(spec);spec.loader.exec_module(relay)
    # Importing worker.py only defines its classes; private helper/RelayAPI are never used.
    started=time.monotonic();deadline=started+TOTAL_SECONDS
    out=ROOT/'evidence/local-compact-conversation'/label
    if out.exists():raise RuntimeError('Refusing to overwrite an earlier probe.')
    out.mkdir(parents=True)
    token='compact_'+uuid.uuid4().hex
    expected_question=question if question is not None else QUESTION
    input_details=({'type':'typed_text','textSha256':hashlib.sha256(question.encode('utf-8')).hexdigest(),
                    'source':'Controlled local typed HTTP question; not a browser, phone or microphone test.'}
                   if question is not None else {'path':str(SOURCE),'sha256':sha(SOURCE),
                    'source':'Existing Windows-synthesized English fixture; not a person or physical microphone.'})
    record={'status':'preflight','testType':'REAL_LOCAL_HTTP_TYPED_QUESTION' if question is not None else 'REAL_LOCAL_HTTP_MULTIPART_WINDOWS_SYNTHESIZED_QUESTION',
        'question':expected_question,'requestToken':token,'serverPID':server_pid,'base':BASE,
        'controlledInput':input_details,
        'modelsMocked':False,'browserOrPlaybackTested':False,'physicalMicrophoneTested':False,
        'publicRequests':False,'privateCredentialsLoaded':False,'maximumSeconds':TOTAL_SECONDS,
        'abortPhysicalGiB':PHYSICAL_FLOOR,'abortCommitGiB':COMMIT_FLOOR,
        'cancellationScope':'Only this fresh cookie session and request token/job. No process is killed by this probe.',
        'phases':[],'chunks':[],'cancellationAttempts':[],'before':memory.memory(),
        'minimumPhysicalGiB':None,'minimumCommitGiB':None,'submissionAttempted':False}
    record['minimumPhysicalGiB']=record['before']['availableGiB']
    record['minimumCommitGiB']=record['before']['commitCapacityAvailableGiB']
    events=queue.Queue();stop=threading.Event();finished=threading.Event()
    shared={'session':None,'jobId':None,'phase':None,'networkError':None,'done':False}
    sampler=network_thread=cancel_thread=None
    idle_support_pids={server_pid}
    manifest=[]

    def emit(kind,**values):
        events.put({'kind':kind,'atEpoch':time.time(),'elapsedSeconds':round(time.monotonic()-started,3),**values})

    def cancel_own():
        session=shared['session']
        if session is None:return
        paths=['/api/requests/'+token+'/cancel']
        if shared['jobId']:paths.append('/api/jobs/'+shared['jobId']+'/cancel')
        for path in paths:
            try:
                response=session.request('POST',path,b'')
                emit('cancel_ack',path=path,response=response)
            except relay.RelayError as exc:
                emit('cancel_failed',path=path,errorCode=exc.code,httpStatus=exc.status)

    def request_cancel(reason):
        nonlocal cancel_thread
        if not stop.is_set():
            stop.set();record['abortReason']=reason;record['status']='cancelled_'+reason
            record['abortAtSeconds']=round(time.monotonic()-started,3)
        if shared['session'] is not None and cancel_thread is None:
            cancel_thread=threading.Thread(target=cancel_own,daemon=True,name='compact-probe-own-cancel')
            cancel_thread.start()

    def network():
        try:
            session=relay.LocalSession(BASE);shared['session']=session
            health=session.request('GET','/api/health');emit('health',value=health)
            required={'voiceEngine':'onnx-q4','sttEngine':'faster-small-en','brainModel':'q4',
                      'sequentialModels':True,'streaming':True,'memoryProfile':'compact',
                      'noRepack':True,'voiceImplementation':'encoder-release-seeded'}
            if not health.get('available') or not health.get('requestCancellation') or any(health.get(k)!=v for k,v in required.items()):
                raise RuntimeError('The reviewed compact profile is not active.')
            if health.get('resourceAdmission')!={'physicalGiB':ENTRY_PHYSICAL,'commitGiB':ENTRY_COMMIT}:
                raise RuntimeError('The compact admission limits changed.')
            if health.get('activeJobs') or health.get('queued'):
                raise RuntimeError('The server is already handling another request.')
            state=memory.memory()
            if state['availableGiB']<ENTRY_PHYSICAL or state['commitCapacityAvailableGiB']<ENTRY_COMMIT:
                emit('not_submitted',reason='resource_preflight',memory=state);return
            if stop.is_set():return
            emit('submit_started')
            job=session.submit(request_payload(token,question))
            job_id=job.get('jobId')
            if not isinstance(job_id,str) or not re.fullmatch(r'[a-f0-9]{32}',job_id):
                raise RuntimeError('Invalid local job identifier.')
            shared['jobId']=job_id;emit('submitted',job=job)
            if stop.is_set():cancel_own();return
            previous=None;seen=set()
            while not stop.is_set():
                data=session.request('GET','/api/jobs/'+job_id)
                shared['phase']=data.get('phase')
                if data.get('phase')!=previous:
                    previous=data.get('phase');emit('phase',job=data)
                for chunk in data.get('chunks',[]):
                    index=chunk.get('index')
                    if not isinstance(index,int) or index<0:raise RuntimeError('Invalid chunk index.')
                    if index in seen:continue
                    if index!=len(seen):raise RuntimeError('Unexpected chunk order.')
                    expected=f'/responses/{job_id}/chunk-{index}.wav'
                    if chunk.get('audioUrl')!=expected:raise RuntimeError('Chunk does not belong to this request.')
                    if stop.is_set():return
                    payload=session.request('GET',expected,binary=True)
                    if stop.is_set():return
                    (out/f'chunk-{index}.wav').write_bytes(payload);seen.add(index)
                    emit('chunk',index=index,phaseWhenFetched=data.get('phase'),audio=wav_info(payload),
                         combinedFileAlreadyExists=(ROOT/'responses'/f'{job_id}.wav').exists(),metadata=chunk)
                if data.get('phase') in ('done','error'):
                    emit('terminal',job=data)
                    if data['phase']=='done':
                        expected=f'/responses/{job_id}.wav'
                        if data.get('result',{}).get('audioUrl')!=expected:raise RuntimeError('Final audio does not belong to this request.')
                        payload=session.request('GET',expected,binary=True)
                        if stop.is_set():return
                        (out/'reply.wav').write_bytes(payload)
                        emit('full_audio',audio=wav_info(payload));shared['done']=True
                    break
                stop.wait(.25)
        except Exception as exc:
            shared['networkError']=type(exc).__name__
            emit('network_error',errorType=type(exc).__name__,errorCode=getattr(exc,'code',None),httpStatus=getattr(exc,'status',None),
                 message=str(exc) if not isinstance(exc,relay.RelayError) else None)
        finally:
            finished.set()

    def drain(log):
        while True:
            try:event=events.get_nowait()
            except queue.Empty:break
            log.write(json.dumps(event)+'\n');log.flush()
            kind=event['kind']
            if kind=='health':record['health']=event['value']
            elif kind=='submit_started':record['submissionAttempted']=True;record['status']='request_pending'
            elif kind=='submitted':record['jobId']=event['job']['jobId'];record['submitReceipt']=event
            elif kind=='phase':record['phases'].append(event);record['status']='active';record['lastJob']=event['job']
            elif kind=='chunk':record['chunks'].append(event)
            elif kind=='terminal':record['terminalJob']=event['job'];record['terminalObservedSeconds']=event['elapsedSeconds']
            elif kind=='full_audio':record['fullAudio']=event;record['status']='reply_received'
            elif kind.startswith('cancel_'):record['cancellationAttempts'].append(event)
            elif kind=='not_submitted':record['status']='not_submitted_'+event['reason'];record['preflightRefusal']=event
            elif kind=='network_error':record['networkError']=event

    try:
        save(out/'receipt.json',record)
        if question is None:
            if record['controlledInput']['sha256']!=SOURCE_SHA:raise RuntimeError('Controlled fixture changed.')
            record['controlledInput']['wave']=wav_info(SOURCE.read_bytes())
        if listener_pid()!=server_pid:raise RuntimeError('Provided PID does not own loopback8770.')
        paths=[Path(__file__),ROOT/'server.py',ROOT/'brain.py',ROOT/'property_context.py',ROOT/'onnx_voice_worker.py',ROOT/'fast_stt_worker.py',
               ROOT/'public-relay/worker.py',ROOT/'research/onnx_encoder_release_candidate.py',
               ROOT/'research/benchmark_mtl_loader_candidate.py',ROOT/'research/memory_reclaim_api.py']
        if question is None:paths.append(SOURCE)
        manifest=[{'path':str(p),'bytes':p.stat().st_size,'modifiedNs':p.stat().st_mtime_ns,'sha256':sha(p)} for p in paths]
        save(out/'source-manifest.json',{'files':manifest})
        sampler=ProcessSamples(server_pid);initial=sampler.sample()
        if not initial or any(v['pid']!=server_pid and v['name'].lower()!='conhost.exe' for v in initial):
            raise RuntimeError('Server is unavailable or has pre-existing model descendants.')
        idle_support_pids.update(v['pid'] for v in initial if v['name'].lower()=='conhost.exe')
        record['idleSupportProcesses']=[{'pid':v['pid'],'name':v['name']} for v in initial]
        # Hidden Windows launches may retain their own idle console host. Exclude only
        # this observed baseline set; every later model descendant must still exit.
        network_thread=threading.Thread(target=network,daemon=True,name='compact-probe-http')
        network_thread.start();quiet_since=None
        with (out/'events.jsonl').open('w',encoding='utf-8') as event_log,(out/'memory.jsonl').open('w',encoding='utf-8') as memory_log:
            while time.monotonic()<deadline:
                tick=time.monotonic();state=memory.memory()
                record['minimumPhysicalGiB']=min(record['minimumPhysicalGiB'],state['availableGiB'])
                record['minimumCommitGiB']=min(record['minimumCommitGiB'],state['commitCapacityAvailableGiB'])
                if state['availableGiB']<=PHYSICAL_FLOOR or state['commitCapacityAvailableGiB']<=COMMIT_FLOOR:request_cancel('resource_floor')
                elif tick>=deadline-CANCEL_RESERVE_SECONDS:request_cancel('deadline')
                elif (out/'cancel').exists():request_cancel('requested')
                elif shared['networkError']:request_cancel('network_error')
                if stop.is_set() and cancel_thread is None:request_cancel(record.get('abortReason','requested'))
                rows=sampler.sample()
                if not rows:request_cancel('process_memory_unavailable')
                live=[pid for pid in alive_handles(sampler) if pid not in idle_support_pids]
                memory_log.write(json.dumps({'elapsedSeconds':round(tick-started,3),**state,'processes':rows,
                                              'liveServerDescendants':live,'phase':shared['phase']})+'\n')
                memory_log.flush();drain(event_log)
                if finished.is_set() and not live and (cancel_thread is None or not cancel_thread.is_alive()):
                    quiet_since=quiet_since or tick
                    if tick-quiet_since>=.5:break
                else:quiet_since=None
                time.sleep(max(0,POLL_SECONDS-(time.monotonic()-tick)))
            if not finished.is_set() or any(pid not in idle_support_pids for pid in alive_handles(sampler)):
                request_cancel('deadline')
            drain(event_log)
        record['networkThreadFinished']=finished.is_set()
        record['cancellationThreadFinished']=cancel_thread is None or not cancel_thread.is_alive()
        record['observedServerDescendantsStopped']=not any(pid not in idle_support_pids for pid in alive_handles(sampler))
        record['processPeaks']=sampler.sample()
        children=[v for v in record['processPeaks'] if v['pid'] not in idle_support_pids]
        record['maxSingleDescendantPeakWorkingMiB']=max((v['peakWorkingMiB'] for v in children),default=None)
        record['maxSingleDescendantPeakCommitMiB']=max((v['peakCommitMiB'] for v in children),default=None)
        job_id=shared['jobId']
        if job_id:
            for key,path in [('serverJobReceipt',ROOT/'.runtime/jobs'/job_id/'receipt.json'),
                             ('transcription',ROOT/'.runtime/jobs'/job_id/'transcript.json'),
                             ('voiceMetadata',ROOT/'responses'/f'{job_id}.json')]:
                if path.exists():record[key]=json.loads(path.read_text(encoding='utf-8'))
            job=record.get('terminalJob',record.get('lastJob',{}))
            transcript=record.get('transcription',{}).get('text',job.get('result',{}).get('userText',job.get('userText','')))
            answer=job.get('result',{}).get('text',job.get('responseText',''))
            input_matches=re.findall(r'[a-z]+',transcript.lower())==re.findall(r'[a-z]+',expected_question.lower())
            record.update(transcript=transcript if question is None else None,answer=answer,
                transcriptionPerformed=question is None and 'transcription' in record,
                transcriptExactWords=input_matches if question is None else None,
                typedQuestionExactWords=input_matches if question is not None else None,
                answerContentReviewPending=True)
            record['cacheFlags']={key:job.get('result',{}).get(key) for key in ('voiceCacheHit','voiceWorkerWarm','brainWarm','persistentBrain')}
            record['answerProvenance']={key:job.get('result',{}).get(key) for key in
                ('mode','sourceUrl','sourcePage','sourceDate','languageModelInference','modelAttempted')}
        if record.get('fullAudio') and record['chunks']:
            parts=[];formats=[]
            for chunk in record['chunks']:
                with wave.open(str(out/f'chunk-{chunk["index"]}.wav'),'rb') as wav:
                    formats.append((wav.getnchannels(),wav.getsampwidth(),wav.getframerate()))
                    parts.append(wav.readframes(wav.getnframes()))
            record['chunkConcatenation']={'allFormatsSame':len(set(formats))==1,
                'pcmSha256':hashlib.sha256(b''.join(parts)).hexdigest(),
                'exactFullPCM':hashlib.sha256(b''.join(parts)).hexdigest()==record['fullAudio']['audio']['pcmSha256']}
        for item in manifest:
            p=Path(item['path'])
            if p.stat().st_size!=item['bytes'] or p.stat().st_mtime_ns!=item['modifiedNs'] or sha(p)!=item['sha256']:
                raise RuntimeError('A probe source changed during the run.')
        if record.get('abortReason'):record['status']='cancelled_'+record['abortReason']
        elif shared['done']:record['status']='real_local_reply_received_review_pending'
        elif record.get('terminalJob',{}).get('phase')=='error':record['status']='server_error'
    except BaseException as exc:
        request_cancel('probe_error')
        record.update(status='probe_error',errorType=type(exc).__name__,error=str(exc))
        # Allow the request-scoped HTTP cancellation to finish even when observation
        # fails. Never substitute an OS kill against the shared server or its jobs.
        until=min(deadline,time.monotonic()+22)
        with (out/'events.jsonl').open('a',encoding='utf-8') as event_log:
            while time.monotonic()<until:
                if stop.is_set() and cancel_thread is None and shared['session'] is not None:
                    request_cancel('probe_error')
                drain(event_log)
                if (network_thread is None or finished.is_set()) and (cancel_thread is None or not cancel_thread.is_alive()):break
                time.sleep(.1)
            drain(event_log)
        record['networkThreadFinished']=finished.is_set() if network_thread else True
        record['cancellationThreadFinished']=cancel_thread is None or not cancel_thread.is_alive()
        raise
    finally:
        # Read-only sampler cleanup; the server and all other request owners are untouched.
        if sampler:sampler.close()
        record.update(after=memory.memory(),elapsedSeconds=round(time.monotonic()-started,3))
        save(out/'receipt.json',record)
        print(json.dumps({'receipt':str(out/'receipt.json'),'status':record['status'],
                          'submissionAttempted':record['submissionAttempted']}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',action='store_true')
    parser.add_argument('--label',type=safe_label,default='identity-01')
    parser.add_argument('--server-pid',type=int)
    parser.add_argument('--question',type=typed_question,help='Optional typed local question; omitting it preserves the controlled identity WAV.')
    args=parser.parse_args()
    if args.go:
        if not args.server_pid or args.server_pid<=0:parser.error('--server-pid is required for the live probe.')
        run(args.label,args.server_pid,args.question)
    else:print(json.dumps({'preparedOnly':True,'inferenceSubmitted':False,'base':BASE,'question':args.question if args.question is not None else QUESTION,
        'inputMode':'typed_text' if args.question is not None else 'controlled_wav',
        'fixture':None if args.question is not None else str(SOURCE),'maximumSeconds':TOTAL_SECONDS,'abortPhysicalCommitGiB':[PHYSICAL_FLOOR,COMMIT_FLOOR],
        'requires':'--go and the current PID verified as loopback8770 listener'}))
