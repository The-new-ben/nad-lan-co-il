"""Real loopback HTTP fixtures. No WordPress credentials, public traffic or models."""
from __future__ import annotations
import base64
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import threading
import time
import urllib.request
import urllib.error
import uuid
import wave
from unittest.mock import patch

import worker

buffer = io.BytesIO()
with wave.open(buffer, 'wb') as output:
    output.setparams((1, 2, 24000, 0, 'NONE', 'not compressed'))
    output.writeframes(b'\0\0'*2400)
SILENT_WAV = buffer.getvalue()
lock = threading.RLock()
local_jobs, cookie_requests, token_cancels, local_id_cancels = {}, [], [], []
relay_jobs, pending, updates, readiness = {}, [], [], []
owner_a, owner_b = 'a'*64, 'b'*64
SUBMIT_DELAY = .35
SESSION_FAIL = False


class Base(BaseHTTPRequestHandler):
    def log_message(self, *_): pass
    def send(self, value, status=200, headers=None):
        data = json.dumps(value).encode()
        self.send_response(status)
        for key, item in (headers or {}).items(): self.send_header(key, item)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def body(self):
        raw = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        return json.loads(raw or b'{}')


class Local(Base):
    def do_GET(self):
        if self.path == '/api/session':
            if SESSION_FAIL:
                self.send({'error':'controlled unavailable fixture'},503)
                return
            self.send({'ready': True}, headers={'Set-Cookie':'nl3d-session='+uuid.uuid4().hex+'; Path=/; HttpOnly; SameSite=Strict'})
        elif self.path == '/api/health':
            self.send({'available':True,'requestCancellation':True,'queued':0,'activeJobs':0})
        elif self.path.startswith('/responses/'):
            self.send_response(200)
            self.send_header('Content-Length', str(len(SILENT_WAV)))
            self.end_headers()
            self.wfile.write(SILENT_WAV)
        else:
            job_id = self.path.split('/')[-1]
            with lock:
                job = local_jobs[job_id]
                assert job['cookie'] == self.headers.get('Cookie')
                job['polls'] += 1
                if job['text']=='lease-lost' and job['polls']>1:
                    time.sleep(.08)
                if job.get('cancelled'):
                    self.send({'phase':'error','cancelled':True})
                    return
                chunk = {'index':0,'text':'Synthetic first sentence.', 'audioUrl':f'/responses/{job_id}/chunk-0.wav'}
                if job['polls'] == 1:
                    self.send({'phase':'streaming','userText':job['text'],'responseText':'Synthetic first sentence. Synthetic second sentence.', 'chunks':[chunk]})
                elif job['text'] == 'fail-later':
                    self.send({'phase':'error','errorCode':'reply_failed','chunks':[]})
                else:
                    second = {'index':1,'text':'Synthetic second sentence.', 'audioUrl':f'/responses/{job_id}/chunk-1.wav'}
                    self.send({'phase':'done','userText':job['text'],'chunks':[chunk,second], 'result':{
                        'audioUrl':f'/responses/{job_id}.wav','text':'Synthetic first sentence. Synthetic second sentence.',
                        'voiceEngine':'CONTROLLED_SILENT_FIXTURE','voiceCacheHit':False}})
    def do_POST(self):
        if self.path == '/api/converse':
            length = int(self.headers['Content-Length'])
            raw = self.rfile.read(length)
            text = json.loads(raw)['text'] if self.headers['Content-Type']=='application/json' else 'audio-fixture'
            token = self.headers['X-NL-Request-ID']
            cookie = self.headers.get('Cookie')
            job_id = uuid.uuid4().hex
            with lock:
                local_jobs[job_id] = {'cookie':cookie,'text':text,'polls':0,'token':token}
                cookie_requests.append({'text':text,'cookie':cookie,'token':token})
            if text in ('cancel-before-id','stop-before-id'): time.sleep(SUBMIT_DELAY)
            local_jobs[job_id]['responseSentAt'] = time.monotonic()
            self.send({'jobId':job_id,'phase':'queued'},202)
        elif '/requests/' in self.path:
            token = self.path.split('/')[3]
            with lock:
                token_cancels.append((token,time.monotonic()))
                for job in local_jobs.values():
                    if job['token']==token and job['cookie']==self.headers.get('Cookie'):job['cancelled']=True
            self.send({'cancelled':True})
        else:
            job_id = self.path.split('/')[3]
            with lock:
                local_id_cancels.append(job_id)
                assert local_jobs[job_id]['cookie']==self.headers.get('Cookie')
                local_jobs[job_id]['cancelled']=True
            self.send({'cancelled':True})


class Remote(Base):
    def do_GET(self):
        job_id = self.path.split('/')[-1]
        with lock:
            job = relay_jobs[job_id]
            assert self.headers['X-NL-Lease']==job['leaseToken']
            job['statusReads']=job.get('statusReads',0)+1
            if job['text']=='lease-lost' and job['statusReads']>1:
                self.send({'code':'lease'},404)
                return
            if job['text']=='cancel-before-id' and time.monotonic()-job['claimedAt']>.1:job['cancelled']=True
            self.send({'phase':'cancelled' if job.get('cancelled') else job.get('phase','claimed'),
                       'cancelled':job.get('cancelled',False),'deadlineAt':job['deadlineAt'],'leaseUntil':time.time()+45})
    def do_POST(self):
        body = self.body()
        with lock:
            if self.path.endswith('/claim'):
                readiness.append(body)
                job = pending.pop(0) if body['ready'] and pending else None
                if job:
                    job['claimedAt']=time.monotonic()
                    relay_jobs[job['jobId']]=job
                self.send({'job':job})
                return
            job_id = self.path.split('/')[-2]
            job = relay_jobs[job_id]
            assert body['leaseToken']==job['leaseToken']
            if job['text']=='cancel-during-busy' and body['event']=='chunk':
                job['chunkAttempts']=job.get('chunkAttempts',0)+1
                job['cancelled']=True
                self.send({'code':'busy','data':{'status':429}},429)
                return
            if job.get('cancelled'):
                self.send({'code':'cancelled','cancelled':True},409)
                return
            if body['event'] in ('chunk','done'):
                assert base64.b64decode(body['audioBase64'])==SILENT_WAV
                assert body['duration']==.1
            updates.append({'jobId':job_id,**body})
            if body['event']=='done':job['phase']='done'
            if body['event']=='error':job['phase']='error'
            self.send({'accepted':True,'cancelled':False})


def serve(handler):
    server = ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread = threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    return server, f'http://127.0.0.1:{server.server_port}'


def make_job(text, owner=owner_a, audio=False):
    job={'jobId':uuid.uuid4().hex,'leaseToken':uuid.uuid4().hex+uuid.uuid4().hex[:16],
         'ownerKey':owner,'requestId':str(uuid.uuid4()),'text':text,'mime':'',
         'deadlineAt':time.time()+60,'expiresAt':time.time()+90,'leaseUntil':time.time()+45}
    if audio:job.update(audioBase64=base64.b64encode(SILENT_WAV).decode(),mime='audio/wav')
    pending.append(job)
    return job


def main():
    global SESSION_FAIL
    local, local_base = serve(Local)
    remote, remote_base = serve(Remote)
    def private_request(method,path,body=None,timeout=None,headers=None):
        request=urllib.request.Request(remote_base+path,method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={'Content-Type':'application/json',**(headers or {})})
        try:response=urllib.request.urlopen(request,timeout=timeout)
        except urllib.error.HTTPError as error:response=error
        with response:return response.status,json.load(response),dict(response.headers)
    relay = worker.RelayWorker(worker.RelayAPI(private_request),local_base,
        memory=lambda:4,worker_id='fixture_worker',poll=.03,monitor_interval=.025)
    checks=[]
    try:
        def check_retry_case(name, replies, expected_calls, expected_error=None):
            calls=[]
            def request(method,path,body=None,**kwargs):
                calls.append(time.monotonic())
                response=replies[min(len(calls)-1,len(replies)-1)]
                if isinstance(response,Exception):raise response
                return (*response,{})
            api=worker.RelayAPI(request)
            try:
                value=api.call('POST','/worker/claim',{'workerId':'retry_fixture','ready':False})
                assert expected_error is None and value=={'job':None}
            except worker.RelayError as error:
                assert (error.status,error.code)==expected_error
            assert len(calls)==expected_calls
            checks.append({'case':name,'passed':True,'attempts':len(calls),
                           'elapsedSeconds':round(calls[-1]-calls[0],3)})

        busy=(429,{'code':'busy'})
        success=(200,{'job':None})
        check_retry_case('lock_busy_recovers_after_two_bounded_retries',[busy,busy,success],3)
        check_retry_case('lock_busy_exhaustion_stops_at_three_attempts',[busy],3,(429,'busy'))
        check_retry_case('rate429_is_never_retried',[(429,{'code':'rate'})],1,(429,'rate'))
        for status in (401,403,404,409,500):
            check_retry_case(f'http{status}_is_never_retried',[(status,{'code':'busy'})],1,(status,'busy'))
        check_retry_case('uncertain_transport_is_never_replayed',[OSError('controlled transport failure')],1,(0,'transport_failed'))
        assert worker.failure_fields(worker.RelayError(429,'busy'))=={'failureStatus':429,'failureCode':'busy'}
        assert worker.failure_fields(worker.RelayError(500,'SECRET_VALUE_do_not_log'))['failureCode']=='unrecognized_error'
        assert worker.failure_fields(worker.RelayError(500,{'secret':'do_not_log'}))['failureCode']=='unrecognized_error'
        checks.append({'case':'failure_diagnostics_only_allow_controlled_status_and_code','passed':True})

        health_reads=[]
        class HealthOnly:
            def open(self,url,**kwargs):
                assert url in ('http://127.0.0.1:8769/api/health','http://127.0.0.1:8770/api/health')
                health_reads.append(url)
                return io.BytesIO(json.dumps({'available':True,'requestCancellation':True,'queued':0,'activeJobs':0}).encode())
        with patch.object(worker.urllib.request,'build_opener',return_value=HealthOnly()):
            for physical,commit,ready in ((7.0,9.2,False),(7.2,9.0,False),(7.1,9.1,True),(8.0,10.0,True)):
                guarded=worker.RelayWorker(None,'http://127.0.0.1:8769',memory=lambda:physical,
                    commit_memory=lambda:commit,minimum_memory=1.0)
                assert guarded.readiness()==(ready,None if ready else 'resource_busy')
                checks.append({'case':f'original_independent_reserves_{physical}_{commit}','passed':True,'ready':ready})
            for physical,commit,ready in ((3.0,.1,True),(2.9,99,False)):
                guarded=worker.RelayWorker(None,'http://127.0.0.1:8770',memory=lambda:physical,commit_memory=lambda:commit)
                assert guarded.readiness()==(ready,None if ready else 'resource_busy')
                checks.append({'case':f'optional_existing_guard_{physical}_{commit}','passed':True,'ready':ready})
        assert len(health_reads)==6
        checks.append({'case':'resource_readiness_only_reads_health_never_submits_or_loads_models','passed':True})

        for text, owner in [('owner-a-first',owner_a),('owner-b-first',owner_b),('owner-a-next',owner_a)]:
            job=make_job(text,owner)
            outcome=relay.run_once()
            assert outcome['outcome']=='done' and outcome['chunks']==2
            events=[item for item in updates if item['jobId']==job['jobId'] and item['event'] in ('chunk','done')]
            assert [item['event'] for item in events]==['chunk','chunk','done']
            assert [item['index'] for item in events[:2]]==[0,1]
        assert cookie_requests[0]['cookie']!=cookie_requests[1]['cookie']
        assert cookie_requests[0]['cookie']==cookie_requests[2]['cookie']
        checks.append({'case':'separate_visitor_cookies_and_same_visitor_reuse','passed':True})
        checks.append({'case':'cumulative_chunk_deduplication_and_complete_replay_forwarding','passed':True})

        job=make_job('audio',owner_b,audio=True)
        assert relay.run_once()['outcome']=='done'
        assert cookie_requests[-1]['text']=='audio-fixture'
        checks.append({'case':'bounded_audio_forwarding_uses_visitor_cookie','passed':True})

        job=make_job('cancel-before-id')
        started=time.monotonic()
        outcome=relay.run_once()
        assert outcome['outcome']=='cancelled'
        assert any(token==job['requestId'] and at-started<.3 for token,at in token_cancels)
        local_id=next(key for key,value in local_jobs.items() if value['token']==job['requestId'])
        assert local_id in local_id_cancels
        assert not any(item['jobId']==job['jobId'] and item['event'] in ('chunk','done') for item in updates)
        checks.append({'case':'close_before_id_cancels_token_then_late_job_no_audio','passed':True})

        job=make_job('fail-later')
        outcome=relay.run_once()
        assert outcome['outcome']=='failed'
        events=[item['event'] for item in updates if item['jobId']==job['jobId']]
        assert events.count('chunk')==1 and events[-1]=='error' and 'done' not in events
        checks.append({'case':'later_sentence_failure_publishes_error_never_success','passed':True})

        job=make_job('lease-lost')
        outcome=relay.run_once()
        assert outcome['outcome']=='cancelled'
        assert any(token==job['requestId'] for token,_ in token_cancels)
        assert not any(item['jobId']==job['jobId'] and item['event']=='done' for item in updates)
        checks.append({'case':'lost_lease_stops_owned_local_work_without_late_success','passed':True})

        job=make_job('cancel-during-busy')
        outcome=relay.run_once()
        assert outcome['outcome']=='cancelled'
        assert relay_jobs[job['jobId']]['chunkAttempts']==1
        assert any(token==job['requestId'] for token,_ in token_cancels)
        assert not any(item['jobId']==job['jobId'] and item['event'] in ('chunk','done') for item in updates)
        checks.append({'case':'cancellation_during_busy_backoff_prevents_retry_and_audio_publication','passed':True})

        job=make_job('stop-before-id')
        stop_path=worker.ROOT/'.runtime'/('relay-stop-fixture-'+uuid.uuid4().hex)
        relay.stop_file=stop_path
        stopped={}
        stop_thread=threading.Thread(target=lambda:stopped.update(relay.run_once()))
        stop_thread.start()
        deadline=time.monotonic()+2
        while time.monotonic()<deadline and not any(value['token']==job['requestId'] for value in local_jobs.values()):time.sleep(.005)
        try:
            stop_path.write_text('controlled stop fixture',encoding='utf-8')
            stop_thread.join(timeout=3)
            assert not stop_thread.is_alive() and stopped['outcome']=='cancelled'
            assert any(token==job['requestId'] for token,_ in token_cancels)
        finally:
            stop_path.unlink(missing_ok=True)
            relay.stop_file=None
            relay.stop.clear()
        checks.append({'case':'hidden_worker_stop_file_cancels_only_its_current_request','passed':True})

        SESSION_FAIL=True
        before_count=len(local_jobs)
        job=make_job('local-session-unavailable','c'*64)
        try:
            outcome=relay.run_once()
            assert outcome['outcome']=='failed' and not outcome['submitted']
            assert len(local_jobs)==before_count
            assert any(item['jobId']==job['jobId'] and item['event']=='error' for item in updates)
        finally:SESSION_FAIL=False
        checks.append({'case':'local_session_failure_finishes_public_job_without_submitting','passed':True})

        local_count=len(local_jobs)
        relay.memory=lambda:1.25
        make_job('must-not-run')
        outcome=relay.run_once()
        assert outcome['outcome']=='resource_busy' and not outcome['submitted']
        assert len(local_jobs)==local_count and readiness[-1]['ready'] is False
        checks.append({'case':'memory_guard_advertises_busy_without_claiming_or_submitting','passed':True})
        try:worker.RelayWorker(None,'http://0.0.0.0:8770')
        except ValueError:pass
        else:raise AssertionError('public binding accepted')
        checks.append({'case':'local_backend_loopback_only','passed':True})
        receipt={'testType':'REAL_LOCAL_HTTP_RELAY_WORKER_FIXTURES','modelInference':False,
            'publicRequests':False,'productionCredentialsLoaded':False,
            'audio':'100 ms silent PCM fixture, not generated speech','checks':checks,'passed':len(checks)}
        destination=worker.ROOT/'evidence'/'public-relay'/'worker-controls-resource-admission.json'
        destination.parent.mkdir(exist_ok=True)
        destination.write_text(json.dumps(receipt,indent=2),encoding='utf-8')
        print(json.dumps(receipt,indent=2))
    finally:
        relay.shutdown()
        local.shutdown();local.server_close()
        remote.shutdown();remote.server_close()


if __name__=='__main__':main()
