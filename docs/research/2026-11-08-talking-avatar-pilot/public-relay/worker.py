"""Outbound-only WordPress relay. No listener, model import or paid provider.

Run only after the one-page relay has been reviewed and explicitly enabled.
Credentials stay in the existing private WordPress helper's memory.
"""
from __future__ import annotations

import argparse
import base64
from collections import OrderedDict
import copy
import ctypes
import http.cookiejar
import io
import json
from pathlib import Path
import re
import signal
import threading
import time
from types import SimpleNamespace
import urllib.error
import urllib.request
from urllib.parse import urlsplit
import uuid
import wave

ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = '/wp-json/nadlan-talk/v1'
HELPER = Path('C:/Users/777/nad-lan/nad-lan-co-il/scripts/skin-a/deployskin.py')
HELPER_STOP = 's, h, _ = req("GET", "/wp-json/nadlan/v1/health")'
INPUT_LIMIT = 15 * 1024 * 1024
OUTPUT_LIMIT = 4 * 1024 * 1024
MIN_MEMORY_GIB = 3.0
ORIGINAL_MIN_MEMORY_GIB = 7.1
ORIGINAL_MIN_COMMIT_GIB = 9.1
BUSY = 'This computer is busy. Please try again shortly.'


class RelayError(RuntimeError):
    def __init__(self, status=0, code='transport_failed'):
        super().__init__(code)
        self.status, self.code = status, code


class TurnCancelled(Exception):
    pass


def failure_fields(error):
    """Only controlled identifiers, never response bodies, credentials or paths."""
    allowed = {
        'audio', 'busy', 'changed', 'csrf', 'event', 'index', 'input_expired',
        'lease', 'not_found', 'origin', 'page', 'phase', 'rate', 'request_id',
        'session_required', 'storage', 'text', 'unavailable', 'upload_size',
        'worker_auth', 'worker_id', 'cancelled', 'resource_busy', 'reply_failed',
        'transport_failed', 'relay_rejected', 'invalid_relay_response',
        'local_session_failed', 'local_session_missing', 'invalid_local_path',
        'local_unavailable', 'local_audio_failed', 'invalid_local_response',
        'local_rejected', 'invalid_audio', 'invalid_audio_type', 'invalid_text',
        'invalid_owner', 'reply_too_large', 'invalid_reply_audio', 'invalid_claim',
        'invalid_local_job', 'invalid_chunk_order', 'invalid_local_phase',
        'invalid_request_id', 'request_pending', 'upload_timeout', 'failed',
    }
    if not isinstance(error, RelayError):
        return {'failureStatus': 0, 'failureCode': 'internal_error'}
    return {'failureStatus': error.status if isinstance(error.status, int) and 0 <= error.status <= 599 else 0,
            'failureCode': error.code if isinstance(error.code, str) and error.code in allowed else 'unrecognized_error'}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def memory_capacity_gib():
    class Memory(ctypes.Structure):
        _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [
            (name, ctypes.c_uint64) for name in ('totalPhysical', 'availablePhysical',
                'totalPage', 'availablePage', 'totalVirtual', 'availableVirtual', 'extended')]
    state = Memory()
    state.length = ctypes.sizeof(state)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(state)):
        return {'physical': 0.0, 'commit': 0.0}
    # availablePage is remaining commit capacity, not free pagefile disk space.
    return {'physical': state.availablePhysical / 1024**3,
            'commit': state.availablePage / 1024**3}


def memory_gib():
    return memory_capacity_gib()['physical']


def commit_gib():
    return memory_capacity_gib()['commit']


def load_private_request():
    """Execute only the previously authorized helper definitions, never deployment."""
    source = HELPER.read_text(encoding='utf-8').split(HELPER_STOP, 1)
    if len(source) != 2:
        raise RuntimeError('The existing private helper changed; review it before running.')
    prefix = source[0].replace('sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")', '')
    namespace = {'__name__': 'nadlan_private_relay_auth'}
    exec(compile(prefix, str(HELPER), 'exec'), namespace)
    if namespace.get('BASE') != 'https://nad-lan.co.il':
        raise RuntimeError('The private helper does not target the approved website.')
    # Keep the helper API, but never forward its Authorization header on a redirect.
    opener = urllib.request.build_opener(NoRedirect())
    namespace['urllib'] = SimpleNamespace(request=SimpleNamespace(
        Request=urllib.request.Request, urlopen=opener.open), error=urllib.error)
    return namespace['req']


class RelayAPI:
    def __init__(self, private_request, cancel_check=None):
        self.request = private_request
        self.cancel_check = cancel_check

    def with_cancel_check(self, check):
        # Keep instrumentation/subclass behavior, without sharing a mutable turn guard.
        scoped = copy.copy(self)
        scoped.cancel_check = check
        return scoped

    def call(self, method, path, body=None, lease=None):
        if not re.fullmatch(r'/worker/(claim|jobs/[a-f0-9]{32}(/update)?)', path):
            raise ValueError('Unexpected relay path.')
        for attempt, delay in enumerate((0, .3, .9)):
            if delay:
                time.sleep(delay)
            if self.cancel_check:
                self.cancel_check()
            try:
                status, value, _ = self.request(method, NAMESPACE+path, body,
                    timeout=10, headers={'X-NL-Lease': lease} if lease else None)
            except Exception:
                # An uncertain transport may have executed the mutation. Never replay it.
                raise RelayError() from None
            # This exact WordPress lock refusal occurs before the route callback.
            # A rate limit or any other status/code is never retried.
            if status == 429 and isinstance(value, dict) and value.get('code') == 'busy' and attempt < 2:
                continue
            break
        if status not in (200, 201, 202):
            raise RelayError(status, str(value.get('code', 'relay_rejected')) if isinstance(value, dict) else 'relay_rejected')
        if not isinstance(value, dict):
            raise RelayError(status, 'invalid_relay_response')
        return value

    def claim(self, worker_id, ready, unavailable_code=None):
        return self.call('POST', '/worker/claim', {
            'workerId': worker_id, 'ready': ready, 'unavailableCode': unavailable_code}).get('job')

    def status(self, job):
        return self.call('GET', '/worker/jobs/'+job['jobId'], lease=job['leaseToken'])

    def update(self, job, event, **fields):
        return self.call('POST', '/worker/jobs/'+job['jobId']+'/update',
                         {'leaseToken': job['leaseToken'], 'event': event, **fields})


class LocalSession:
    def __init__(self, base):
        self.base = base
        jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPCookieProcessor(jar))
        try:
            with opener.open(base+'/api/session', timeout=5) as response:
                if not json.load(response).get('ready'):
                    raise RelayError(code='local_session_failed')
        except (OSError, ValueError):
            raise RelayError(code='local_session_failed') from None
        self.cookie = '; '.join(f'{item.name}={item.value}' for item in jar)
        if not self.cookie:
            raise RelayError(code='local_session_missing')

    def request(self, method, path, data=None, headers=None, binary=False):
        # Never fetch an audio URL outside the local backend, including redirects.
        if not re.fullmatch(r'/(api/(converse|session|health|jobs/[a-f0-9]{32}(/cancel)?|requests/[A-Za-z0-9_-]{16,80}/cancel)|responses/[a-f0-9]{32}(\.wav|/chunk-\d+\.wav))', path):
            raise RelayError(code='invalid_local_path')
        request = urllib.request.Request(self.base+path, data=data, method=method,
            headers={'Cookie': self.cookie, 'Origin': self.base, **(headers or {})})
        try:
            response = urllib.request.build_opener(NoRedirect()).open(request, timeout=25 if path=='/api/converse' else 10)
        except urllib.error.HTTPError as error:
            response = error
        except Exception:
            raise RelayError(code='local_unavailable') from None
        with response:
            payload = response.read(OUTPUT_LIMIT+1 if binary else 2*1024*1024)
            if binary:
                if response.status != 200 or len(payload) > OUTPUT_LIMIT:
                    raise RelayError(response.status, 'local_audio_failed')
                return payload
            try:
                value = json.loads(payload)
            except ValueError:
                raise RelayError(response.status, 'invalid_local_response') from None
            if response.status not in (200, 201, 202):
                raise RelayError(response.status, value.get('errorCode', 'local_rejected'))
            return value

    def submit(self, job):
        headers = {'X-NL-Request-ID': job['requestId']}
        if job.get('audioBase64'):
            encoded = job['audioBase64']
            if not isinstance(encoded, str) or len(encoded) > ((INPUT_LIMIT+2)//3)*4:
                raise RelayError(code='invalid_audio')
            try:
                audio = base64.b64decode(encoded, validate=True)
            except ValueError:
                raise RelayError(code='invalid_audio') from None
            if not 0 < len(audio) < INPUT_LIMIT-1024:
                raise RelayError(code='invalid_audio')
            mime = job.get('mime', '')
            if not re.fullmatch(r'audio/[A-Za-z0-9.+-]+(?:;codecs=[A-Za-z0-9.,+-]+)?|video/webm', mime):
                raise RelayError(code='invalid_audio_type')
            boundary = 'nlrelay'+uuid.uuid4().hex
            data = (f'--{boundary}\r\nContent-Disposition: form-data; name="audio"; filename="recording.audio"\r\n'
                    f'Content-Type: {mime}\r\n\r\n').encode()+audio+f'\r\n--{boundary}--\r\n'.encode()
            headers['Content-Type'] = 'multipart/form-data; boundary='+boundary
        else:
            text = job.get('text')
            if not isinstance(text, str) or not 0 < len(text.strip()) <= 1200:
                raise RelayError(code='invalid_text')
            data = json.dumps({'text': text}).encode()
            headers['Content-Type'] = 'application/json'
        return self.request('POST', '/api/converse', data, headers)

    def cancel(self, token, job_id=None):
        # Always cancel the token, including while the initial HTTP upload is pending.
        paths = ['/api/requests/'+token+'/cancel']
        if job_id:
            paths.append('/api/jobs/'+job_id+'/cancel')
        for path in paths:
            try:
                self.request('POST', path, b'')
            except RelayError:
                pass


class OwnerSessions:
    def __init__(self, base, limit=128, idle_seconds=1800):
        self.base, self.limit, self.idle_seconds = base, limit, idle_seconds
        self.sessions = OrderedDict()

    def get(self, owner):
        if not isinstance(owner, str) or not re.fullmatch(r'[a-f0-9]{64}', owner):
            raise RelayError(code='invalid_owner')
        now = time.monotonic()
        for key, (_, touched) in list(self.sessions.items()):
            if now-touched > self.idle_seconds:
                del self.sessions[key]
        pair = self.sessions.pop(owner, None)
        session = pair[0] if pair else LocalSession(self.base)
        self.sessions[owner] = session, now
        while len(self.sessions) > self.limit:
            self.sessions.popitem(last=False)
        return session


def wav_fields(data):
    if len(data) > OUTPUT_LIMIT:
        raise RelayError(code='reply_too_large')
    try:
        with wave.open(io.BytesIO(data), 'rb') as source:
            duration = source.getnframes()/source.getframerate()
            if source.getnchannels() != 1 or source.getsampwidth() != 2 or not 0 < duration <= 90:
                raise ValueError()
    except (wave.Error, ValueError, EOFError, ZeroDivisionError):
        raise RelayError(code='invalid_reply_audio') from None
    return {'audioBase64': base64.b64encode(data).decode('ascii'), 'duration': duration}


class RelayWorker:
    def __init__(self, api, local_base, *, memory=memory_gib, minimum_memory=MIN_MEMORY_GIB,
                 commit_memory=commit_gib, worker_id=None, poll=.3, monitor_interval=1.0, stop_file=None):
        parsed = urlsplit(local_base)
        if parsed.scheme != 'http' or parsed.hostname != '127.0.0.1' or parsed.path not in ('', '/') or parsed.query or parsed.fragment or parsed.username:
            raise ValueError('The voice service must remain on IPv4 loopback.')
        self.api, self.local_base = api, local_base.rstrip('/')
        self.memory, self.commit_memory = memory, commit_memory
        original = parsed.port == 8769
        self.minimum_memory = max(minimum_memory, ORIGINAL_MIN_MEMORY_GIB) if original else minimum_memory
        self.minimum_commit = ORIGINAL_MIN_COMMIT_GIB if original else 0.0
        self.worker_id = worker_id or 'local_'+uuid.uuid4().hex
        self.sessions = OwnerSessions(self.local_base)
        self.stop = threading.Event()
        self.poll, self.monitor_interval = poll, monitor_interval
        self.current = None
        self.stop_file = Path(stop_file) if stop_file else None

    def stopping(self):
        if self.stop_file and self.stop_file.exists():
            self.stop.set()
        return self.stop.is_set()

    def readiness(self):
        try:
            with urllib.request.build_opener(NoRedirect()).open(self.local_base+'/api/health', timeout=3) as response:
                health = json.load(response)
            if not health.get('available') or not health.get('requestCancellation'):
                return False, 'local_unavailable'
            if health.get('queued', 0) or health.get('activeJobs', 0):
                return False, 'resource_busy'
            if self.memory() < self.minimum_memory:
                return False, 'resource_busy'
            if self.minimum_commit and self.commit_memory() < self.minimum_commit:
                return False, 'resource_busy'
            return True, None
        except Exception:
            return False, 'local_unavailable'

    def run_once(self):
        ready, reason = self.readiness()
        job = self.api.claim(self.worker_id, ready, reason)
        if job:
            # A misconfigured relay must not override the computer's resource guard.
            if not ready:
                self.api.update(job, 'error', errorCode='resource_busy' if reason=='resource_busy' else 'failed')
                return {'outcome': reason, 'submitted': False}
            return self.handle(job)
        return {'outcome': 'idle' if ready else reason, 'submitted': False}

    def handle(self, job):
        for key, pattern in (('jobId', r'[a-f0-9]{32}'), ('leaseToken', r'[a-f0-9]{48}'),
                             ('requestId', r'[A-Za-z0-9_-]{16,80}')):
            if not isinstance(job.get(key), str) or not re.fullmatch(pattern, job[key]):
                raise RelayError(code='invalid_claim')
        try:
            session = self.sessions.get(job.get('ownerKey'))
        except RelayError as error:
            self.api.update(job, 'error', errorCode='failed')
            return {'outcome': 'failed', 'submitted': False, 'chunks': 0, **failure_fields(error)}
        cancelled, finished = threading.Event(), threading.Event()
        local_job = {'id': None}
        deadline = min(float(job.get('deadlineAt', 0)), time.time()+600)
        if job.get('cancelled') or deadline <= time.time():
            session.cancel(job['requestId'])
            return {'outcome': 'cancelled', 'submitted': False}
        self.current = (session, job['requestId'], local_job, cancelled)

        def abort():
            cancelled.set()
            session.cancel(job['requestId'], local_job['id'])

        def check():
            if cancelled.is_set() or self.stopping() or time.time() >= deadline:
                raise TurnCancelled()

        turn_api = self.api.with_cancel_check(check)
        failure = {}

        def monitor():
            next_heartbeat = 0.0
            while not finished.is_set():
                if self.stopping() or time.time() >= deadline:
                    abort()
                    return
                try:
                    status = turn_api.status(job)
                    if status.get('cancelled') or status.get('phase') in ('error', 'cancelled'):
                        abort()
                        return
                    if status.get('phase') == 'done':
                        return
                    if float(status.get('deadlineAt', deadline)) <= time.time():
                        abort()
                        return
                    if time.monotonic() >= next_heartbeat:
                        turn_api.update(job, 'heartbeat')
                        next_heartbeat = time.monotonic()+10
                except TurnCancelled:
                    abort()
                    return
                except RelayError as error:
                    if error.status == 409:
                        try:
                            if turn_api.status(job).get('phase') == 'done':
                                return
                        except (RelayError, TurnCancelled):
                            pass
                    failure.update(failure_fields(error))
                    # Lease uncertainty stops local work instead of producing orphan audio.
                    abort()
                    return
                finished.wait(self.monitor_interval)

        monitor_thread = threading.Thread(target=monitor, name='relay-lease-monitor', daemon=True)
        monitor_thread.start()
        sent = set()
        result = {'outcome': 'failed', 'submitted': False, 'chunks': 0}
        completed = False
        try:
            check()
            reply = session.submit(job)
            if not re.fullmatch(r'[a-f0-9]{32}', str(reply.get('jobId', ''))):
                raise RelayError(code='invalid_local_job')
            local_job['id'] = reply['jobId']
            result['submitted'] = True
            check()  # A late ID is still canceled in finally if close won the race.
            last_progress = None
            while True:
                check()
                data = session.request('GET', '/api/jobs/'+local_job['id'])
                check()
                if data.get('phase') == 'error':
                    if data.get('cancelled'):
                        raise TurnCancelled()
                    raise RelayError(code=data.get('errorCode', 'reply_failed'))
                phase = data.get('phase')
                translated_phase = {'transcribing':'transcribing', 'thinking':'thinking',
                                    'synthesizing':'synthesizing', 'streaming':'streaming'}.get(phase)
                progress = (translated_phase, data.get('userText'), data.get('responseText'))
                if translated_phase and progress != last_progress:
                    turn_api.update(job, 'progress', phase=translated_phase,
                                    userText=data.get('userText', ''), responseText=data.get('responseText', ''),
                                    inputConsumed=phase not in ('queued', 'transcribing'))
                    last_progress = progress
                for chunk in data.get('chunks', []):
                    index = chunk.get('index')
                    if index in sent:
                        continue
                    if not isinstance(index, int) or index != len(sent) or index > 7:
                        raise RelayError(code='invalid_chunk_order')
                    check()
                    audio = session.request('GET', chunk['audioUrl'], binary=True)
                    check()
                    turn_api.update(job, 'chunk', index=index, text=chunk.get('text', ''),
                                    **wav_fields(audio))
                    sent.add(index)
                    result['chunks'] = len(sent)
                if phase == 'done':
                    final = data.get('result', {})
                    audio = session.request('GET', final['audioUrl'], binary=True)
                    check()
                    turn_api.update(job, 'done', text=final.get('text', ''),
                                    userText=data.get('userText', final.get('userText', '')),
                                    voiceEngine=final.get('voiceEngine', 'mtl'),
                                    voiceCacheHit=bool(final.get('voiceCacheHit', False)), **wav_fields(audio))
                    completed = True
                    result['outcome'] = 'done'
                    return result
                if phase not in ('queued', 'transcribing', 'thinking', 'synthesizing', 'streaming'):
                    raise RelayError(code='invalid_local_phase')
                cancelled.wait(self.poll)
        except TurnCancelled:
            result['outcome'] = 'cancelled'
            return result
        except Exception as error:
            failure.update(failure_fields(error))
            if isinstance(error, RelayError) and error.status in (404, 409):
                try:
                    remote = self.api.status(job)
                    if remote.get('cancelled') or remote.get('phase') in ('cancelled', 'error'):
                        cancelled.set()
                except RelayError:
                    cancelled.set()
            code = 'resource_busy' if isinstance(error, RelayError) and error.code=='resource_busy' else 'failed'
            result['outcome'] = 'cancelled' if cancelled.is_set() else code
            if not cancelled.is_set():
                try:
                    self.api.update(job, 'error', errorCode=code)
                except RelayError:
                    pass
            return result
        finally:
            finished.set()
            if not completed:
                abort()
            monitor_thread.join(timeout=12)
            result.update(failure)
            self.current = None

    def shutdown(self):
        self.stop.set()
        if self.current:
            session, token, local_job, cancelled = self.current
            cancelled.set()
            session.cancel(token, local_job['id'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-base', required=True, choices=('http://127.0.0.1:8769', 'http://127.0.0.1:8770'))
    parser.add_argument('--check-local', action='store_true', help='check files/resources only; no credentials, public request or model load')
    parser.add_argument('--run', action='store_true', help='explicitly begin the reviewed outbound public pilot')
    parser.add_argument('--once', action='store_true', help='claim at most one turn, then stop')
    args = parser.parse_args()
    worker = RelayWorker(None, args.local_base)
    if args.check_local:
        ready, reason = worker.readiness()
        print(json.dumps({'ready': ready, 'reason': reason, 'modelsLoaded': False}))
        return
    if not args.run:
        parser.error('Use --check-local for a local check or --run for the explicitly enabled pilot.')
    worker.stop_file = ROOT/'.runtime'/'public-relay.stop'
    if worker.stop_file.exists():
        parser.error('The relay stop request is present. Remove it deliberately before starting a new run.')
    worker.api = RelayAPI(load_private_request())
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, lambda *_: worker.shutdown())
    try:
        while not worker.stopping():
            try:
                outcome = worker.run_once()
                if outcome['outcome'] not in ('idle', 'resource_busy', 'local_unavailable'):
                    print(json.dumps(outcome), flush=True)
            except RelayError as error:
                print(json.dumps({'outcome': 'relay_unavailable', **failure_fields(error)}), flush=True)
            if args.once:
                break
            worker.stop.wait(3)
    finally:
        worker.shutdown()
        try:
            worker.api.claim(worker.worker_id, False, 'local_unavailable')
        except RelayError:
            pass


if __name__ == '__main__':
    main()
