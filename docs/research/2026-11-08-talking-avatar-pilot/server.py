"""Loopback-only approval prototype. Run with Python; open http://127.0.0.1:8769/."""
from __future__ import annotations

from email import policy
from email.parser import BytesParser
from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import argparse
import json
import hashlib
import mimetypes
import os
from pathlib import Path
import queue
import re
import signal
import shutil
import subprocess
import threading
import time
from urllib.parse import unquote, urlsplit
import uuid
import wave

import brain
import property_context

ROOT = Path(__file__).resolve().parent
WORK = ROOT / '.runtime' / 'jobs'
RESPONSES = ROOT / 'responses'
VOICE_CACHE = ROOT / '.runtime' / 'voice-cache'
VOICE_PYTHON = Path('C:/Users/777/nad-lan/voice-rig/venv/Scripts/python.exe')
FFMPEG = Path('C:/Users/777/AppData/Local/Programs/Shotcut/ffmpeg.exe')
HOST, PORT = '127.0.0.1', 8769
VOICE_ENGINE = 'mtl'
STREAMING = False
PREWARM_ENABLED = False
CANDIDATE_BRAIN = None
STT_ENGINE = 'whisper-small'
CONCISE_FIRST = False
SEQUENTIAL_MODELS = False
BRAIN_MODEL = 'q8'
NO_REPACK = False
MEMORY_PROFILE = 'legacy'
CANDIDATE_MIN_MEMORY_GB = 3.0
COMPACT_ENTRY_PHYSICAL, COMPACT_ENTRY_COMMIT = 2.3, 2.5
COMPACT_FLOOR_PHYSICAL, COMPACT_FLOOR_COMMIT = .75, 1.0
COMPACT_ADMISSION_WAIT_SECONDS = 30.0
LIMIT = 15 * 1024 * 1024
LOCK = threading.RLock()
JOBS = {}
HISTORY = {}
TOKEN_STATES = {}
TOKEN_TTL = 120
REGISTRATION_DEADLINE = 20
TOKEN_LIMIT = 128
TOKEN_SESSION_LIMIT = 256


def token_state(session, create=True):
    """Called under LOCK. Bounded per-session tombstones never affect other sessions."""
    now = time.monotonic()
    for key, state in list(TOKEN_STATES.items()):
        state['cancelled'] = {token: expiry for token, expiry in state['cancelled'].items() if expiry > now}
        for token, item in list(state['requests'].items()):
            job = JOBS.get(item.get('jobId'))
            if item['expires'] <= now and (not job or job['phase'] in ('done', 'error')):
                del state['requests'][token]
        if now-state['touched'] > 900 and not state['requests'] and not state['cancelled'] and state['barrierUntil'] <= now:
            del TOKEN_STATES[key]
    state = TOKEN_STATES.get(session)
    if state is None and create:
        if len(TOKEN_STATES) >= TOKEN_SESSION_LIMIT:
            return None
        state = {'requests': {}, 'cancelled': {}, 'barrierUntil': 0, 'touched': now}
        TOKEN_STATES[session] = state
    if state:
        state['touched'] = now
    return state


def token_cancelled(state, request_id):
    now = time.monotonic()
    return state['barrierUntil'] > now or state['cancelled'].get(request_id, 0) > now


def cancelled_request(request_id):
    return {'requestId': request_id, 'phase': 'error', 'cancelled': True,
            'errorCode': 'cancelled', 'error': 'The question was cancelled.'}


class PendingQueue(queue.Queue):
    def purge_cancelled(self):
        """Recycle queued slots immediately, without counting removed work twice."""
        with self.mutex:
            kept = [job for job in self.queue if not job['cancel'].is_set()]
            removed = len(self.queue)-len(kept)
            if removed:
                self.queue.clear()
                self.queue.extend(kept)
                self.unfinished_tasks -= removed
                self.not_full.notify_all()
                if self.unfinished_tasks == 0:
                    self.all_tasks_done.notify_all()
            return removed


PENDING = PendingQueue(maxsize=4)
HIDDEN = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
ENV = {**os.environ, 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
       'HF_HUB_DISABLE_TELEMETRY': '1', 'TOKENIZERS_PARALLELISM': 'false',
       'OMP_NUM_THREADS': '4', 'MKL_NUM_THREADS': '4', 'PYTHONIOENCODING': 'utf-8'}


class Cancelled(Exception):
    pass


class ResourceBusy(RuntimeError):
    pass


class OwnedProcessTree:
    """A Windows job contains the venv launcher and its real Python child."""
    def __init__(self, child):
        import ctypes
        from ctypes import wintypes
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        size = ctypes.c_size_t
        class Basic(ctypes.Structure):
            _fields_ = [('processTime', ctypes.c_int64), ('jobTime', ctypes.c_int64),
                        ('flags', wintypes.DWORD), ('minSet', size), ('maxSet', size),
                        ('activeLimit', wintypes.DWORD), ('affinity', size),
                        ('priority', wintypes.DWORD), ('scheduling', wintypes.DWORD)]
        class Counters(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint64) for name in
                        ('readOps', 'writeOps', 'otherOps', 'readBytes', 'writeBytes', 'otherBytes')]
        class Limits(ctypes.Structure):
            _fields_ = [('basic', Basic), ('io', Counters), ('processMemory', size),
                        ('jobMemory', size), ('peakProcess', size), ('peakJob', size)]
        self.api.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.api.CreateJobObjectW.restype = wintypes.HANDLE
        self.api.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self.api.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self.api.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        self.api.CloseHandle.argtypes = [wintypes.HANDLE]
        self.handle = self.api.CreateJobObjectW(None, None)
        limits = Limits()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if (not self.handle or not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits))
                or not self.api.AssignProcessToJobObject(self.handle, wintypes.HANDLE(int(child._handle)))):
            self.close()
            raise ctypes.WinError(ctypes.get_last_error())
        native = ctypes.WinDLL('ntdll')
        native.NtResumeProcess.argtypes = [wintypes.HANDLE]
        native.NtResumeProcess.restype = ctypes.c_long
        if native.NtResumeProcess(wintypes.HANDLE(int(child._handle))) != 0:
            self.close()
            raise RuntimeError('Could not start the owned local worker.')

    def terminate(self):
        if self.handle:
            self.api.TerminateJobObject(self.handle, 1)

    def wait_empty(self, timeout=10):
        """Wait for every owned descendant to exit before starting another model."""
        import ctypes
        from ctypes import wintypes
        class Accounting(ctypes.Structure):
            _fields_ = [(name, ctypes.c_int64) for name in ('user', 'kernel', 'periodUser', 'periodKernel')] + [
                (name, wintypes.DWORD) for name in ('faults', 'total', 'active', 'terminated')]
        self.api.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                                      wintypes.DWORD, ctypes.c_void_p]
        deadline = time.monotonic()+timeout
        while self.handle:
            value = Accounting()
            if not self.api.QueryInformationJobObject(self.handle, 1, ctypes.byref(value), ctypes.sizeof(value), None):
                raise ctypes.WinError(ctypes.get_last_error())
            if not value.active:
                return
            if time.monotonic() >= deadline:
                raise RuntimeError('An owned model process has not finished shutting down.')
            time.sleep(.02)

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None


def memory_resources():
    """Windows available physical memory and remaining process commit capacity."""
    if os.name != 'nt':
        return {'physicalGiB': 0, 'commitGiB': 0}
    import ctypes
    class Memory(ctypes.Structure):
        _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [
            (name, ctypes.c_uint64) for name in ('totalPhysical', 'availablePhysical',
                'totalPage', 'availablePage', 'totalVirtual', 'availableVirtual', 'extended')]
    state = Memory()
    state.length = ctypes.sizeof(state)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(state)):
        return {'physicalGiB': 0, 'commitGiB': 0}
    return {'physicalGiB': state.availablePhysical/(1024**3),
            'commitGiB': state.availablePage/(1024**3)}


def available_memory_gb():
    return memory_resources()['physicalGiB']


def memory_thresholds():
    if MEMORY_PROFILE == 'compact':
        return {'entryPhysicalGiB': COMPACT_ENTRY_PHYSICAL, 'entryCommitGiB': COMPACT_ENTRY_COMMIT,
                'runtimePhysicalFloorGiB': COMPACT_FLOOR_PHYSICAL,
                'runtimeCommitFloorGiB': COMPACT_FLOOR_COMMIT, 'pollIntervalSeconds': .1,
                'stageAdmissionWaitSeconds': COMPACT_ADMISSION_WAIT_SECONDS,
                'provisionalForLongVoice': True}
    return {'entryPhysicalGiB': CANDIDATE_MIN_MEMORY_GB if VOICE_ENGINE == 'onnx-q4' else None,
            'entryCommitGiB': None, 'runtimePhysicalFloorGiB': None, 'runtimeCommitFloorGiB': None}


def observe_resources(job, state):
    job['minimumPhysicalGiB'] = min(job.get('minimumPhysicalGiB', float('inf')), state['physicalGiB'])
    job['minimumCommitGiB'] = min(job.get('minimumCommitGiB', float('inf')), state['commitGiB'])


def compact_entry(job, stage_name, deadline=None):
    if MEMORY_PROFILE != 'compact':
        return
    if job.get('process') is not None and job['process'].poll() is None:
        raise RuntimeError('Cannot wait for stage admission while an owned process is running.')
    started = time.monotonic()
    stop_at = min(started+COMPACT_ADMISSION_WAIT_SECONDS,
                  deadline if deadline is not None else float('inf'),
                  job.get('deadlineMonotonic', float('inf')))
    admission = {'stage': stage_name, 'atEpoch': time.time(), 'outcome': 'waiting'}
    job.setdefault('resourceAdmission', []).append(admission)
    try:
        while True:
            checkpoint(job)
            if deadline is not None and time.monotonic() >= deadline:
                admission['outcome'] = 'deadline'
                raise RuntimeError('The local step took too long while waiting for resources.')
            state = memory_resources()
            observe_resources(job, state)
            admission.update(state)
            if state['physicalGiB'] >= COMPACT_ENTRY_PHYSICAL and state['commitGiB'] >= COMPACT_ENTRY_COMMIT:
                admission['outcome'] = 'admitted'
                return
            if time.monotonic() >= stop_at:
                admission['outcome'] = 'resource_busy'
                raise ResourceBusy('This computer is busy. Please try again shortly.')
            job['cancel'].wait(min(.1, max(0, stop_at-time.monotonic())))
    except Cancelled:
        admission['outcome'] = 'cancelled'
        raise
    except RuntimeError:
        if admission['outcome'] == 'waiting':
            admission['outcome'] = 'deadline_or_error'
        raise
    finally:
        admission['waitSeconds'] = round(time.monotonic()-started, 3)


def answer_command(prompt):
    command = list(brain.command(prompt))
    if NO_REPACK:
        command.append('--no-repack')
    return command


def validated_candidate_answer(raw, job):
    """Only explicit content rejections get an editorial boundary, never failures."""
    try:
        return brain.clean_answer(raw)
    except RuntimeError as exc:
        if PORT != 8770:
            raise
        reason = str(exc)
        if reason == 'The answer included an unverified figure; please rephrase the question.':
            mode = 'source_gap_response'
            answer = ('The saved guide does not establish that exact figure or address, so I cannot verify it. '
                      'Which property or cost would you like help preparing questions about?')
        elif reason in ("The answer exceeded this guide's role; please rephrase the question.",
                        'The answer incorrectly described the computer-made guide.'):
            mode = 'role_boundary_response'
            answer = ("I'm a fictional, computer-made guide and cannot arrange viewings, negotiate or act as your broker. "
                      'Would you like help preparing questions for the right professional?')
        else:
            raise
        # Raw rejected output stays in the private job folder/receipt, never result/chunks.
        job['validatorRejection'] = {'reason': reason, 'raw': raw, 'mode': mode}
        job['answerProvenance'] = {'mode': mode, 'sourceUrl': brain.SOURCE_URL,
                                  'languageModelInference': False, 'modelAttempted': True}
        return answer


def voice_cache_descriptor(answer, *, engine=None, streaming=None):
    engine = VOICE_ENGINE if engine is None else engine
    streaming = STREAMING if streaming is None else streaming
    reference_hash = hashlib.sha256((ROOT.parent/'kit'/'ref-female.wav').read_bytes()).hexdigest()
    if engine == 'mtl':
        # Keep the original approved voice's established cache namespace.
        key = hashlib.sha256((f'chatterbox-v2|{reference_hash}|.5|.5|.65|'+answer).encode()).hexdigest()
        return {'cacheKey': key, 'identity': {'engine': engine, 'text': answer,
                'referenceSha256': reference_hash, 'watermarkMode': 'whole-reply'}}
    if engine != 'onnx-q4':
        raise ValueError('Unknown cache voice engine.')
    identity = {'engine': engine, 'text': answer, 'modelRevision': 'd21799bd0354adb85e348b8a0442a8405110a2cf',
                'voiceImplementation': 'encoder-release-seeded', 'referenceSha256': reference_hash,
                'ortSeedBeforeConstruction': 682, 'torchSeedAfterConstruction': 682,
                'runtimeVersion': '1.31.1', 'threads': 4, 'decoding': 'greedy', 'repetitionPenalty': 1.2,
                'watermarkMode': 'per-sentence' if streaming else 'whole-reply'}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'cacheKey': key, 'identity': identity}


def validate_completed_voice(wav_path, metadata, answer, *, engine=None, streaming=None):
    """Validate a complete output, never individual chunks, before cache adoption."""
    descriptor = voice_cache_descriptor(answer, engine=engine, streaming=streaming)
    identity = descriptor['identity']
    wav_path = Path(wav_path)
    if not 44 < wav_path.stat().st_size <= 4*1024*1024:
        raise ValueError('The completed voice file has an invalid size.')
    with wave.open(str(wav_path), 'rb') as wav:
        duration = wav.getnframes()/wav.getframerate()
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getframerate() != 24000:
            raise ValueError('The completed voice format differs from the cache profile.')
        if len(wav.readframes(wav.getnframes())) != wav.getnframes()*2:
            raise ValueError('The completed voice file is truncated.')
    if not .5 <= duration <= 35 or abs(float(metadata['duration'])-duration) > .001:
        raise ValueError('The completed voice duration differs from its metadata.')
    if not isinstance(metadata.get('cues'), list) or not isinstance(metadata.get('cueMethod'), str):
        raise ValueError('The completed voice has no playback metadata.')
    if identity['engine'] == 'onnx-q4':
        for field in ('text', 'modelRevision', 'voiceImplementation', 'referenceSha256',
                      'ortSeedBeforeConstruction', 'torchSeedAfterConstruction', 'threads'):
            if metadata.get(field) != identity[field]:
                raise ValueError('The completed voice does not match the exact cache profile: '+field)
        if metadata.get('version') != identity['runtimeVersion'] or metadata.get('referenceEncoderReleased') is not True:
            raise ValueError('The completed voice implementation differs.')
        if metadata.get('stopTokenFound') is not True or abs(float(metadata['audioSeconds'])-duration) > .001:
            raise ValueError('The voice did not finish the complete answer.')
        per_sentence = identity['watermarkMode'] == 'per-sentence'
        if bool(metadata.get('streamedBySentence')) != per_sentence:
            raise ValueError('The voice watermark mode differs.')
        expected = [part.strip() for part in re.findall(r'[^.!?]+[.!?]+|[^.!?]+$', answer) if part.strip()]
        segments = metadata.get('segments', [])
        if len(segments) != len(expected) or not all(s.get('stopTokenFound') is True for s in segments):
            raise ValueError('The voice is missing a completed sentence.')
        if per_sentence:
            for index, (text, segment) in enumerate(zip(expected, segments)):
                if (segment.get('index') != index or segment.get('text') != text
                        or segment.get('isLast') != (index == len(expected)-1)
                        or not str(segment.get('method', '')).startswith('Greedy plus repetition penalty1.2;')):
                    raise ValueError('The streamed sentence metadata is incomplete or differs.')
        elif not str(metadata.get('method', '')).startswith('Greedy plus repetition penalty1.2;'):
            raise ValueError('The voice decoding settings differ.')
    return descriptor


def load_voice_cache(job, answer, target):
    descriptor = voice_cache_descriptor(answer)
    cached_wav = VOICE_CACHE/(descriptor['cacheKey']+'.wav')
    cached_meta = cached_wav.with_suffix('.json')
    if not cached_wav.is_file() or not cached_meta.is_file():
        return False
    try:
        metadata = json.loads(cached_meta.read_text(encoding='utf-8'))
        if not isinstance(metadata, dict):
            return False
        if VOICE_ENGINE == 'onnx-q4':
            if metadata.get('cacheIdentity') != descriptor['identity'] or metadata.get('cacheComplete') is not True:
                return False
            if metadata.get('cachedAudioSha256') != hashlib.sha256(cached_wav.read_bytes()).hexdigest():
                return False
            validate_completed_voice(cached_wav, metadata, answer)
        checkpoint(job)
        shutil.copyfile(cached_wav, target)
        shutil.copyfile(cached_meta, target.with_suffix('.json'))
        checkpoint(job)
        job['voiceCacheIdentity'] = descriptor['identity']
        job['voiceCacheSource'] = metadata.get('cacheProvenance', {'type': 'historical_completed_voice'})
        return True
    except (OSError, ValueError, KeyError, TypeError, wave.Error) as exc:
        job['voiceCacheReadError'] = type(exc).__name__
        return False


def store_completed_voice_cache(job, wav_path, metadata, *, engine=None, streaming=None, provenance=None):
    """Commit metadata last, after complete success and a final owned-job check."""
    descriptor = validate_completed_voice(wav_path, metadata, job['answer'], engine=engine, streaming=streaming)
    wav_bytes = Path(wav_path).read_bytes()
    output = {**metadata, 'cacheIdentity': descriptor['identity'], 'cacheComplete': True,
              'cachedAudioSha256': hashlib.sha256(wav_bytes).hexdigest(),
              'cacheProvenance': provenance or {'type': 'completed_local_job', 'jobId': job['id']}}
    VOICE_CACHE.mkdir(parents=True, exist_ok=True)
    target = VOICE_CACHE/(descriptor['cacheKey']+'.wav')
    temporary = VOICE_CACHE/(descriptor['cacheKey']+'.'+uuid.uuid4().hex+'.tmp')
    temporary_meta = temporary.with_suffix('.json.tmp')
    try:
        temporary.write_bytes(wav_bytes)
        temporary_meta.write_text(json.dumps(output, indent=2), encoding='utf-8')
        with LOCK:
            checkpoint(job)
            if job.get('phase') != 'done':
                raise ValueError('Only a successful complete reply may enter the voice cache.')
            os.replace(temporary, target)
            os.replace(temporary_meta, target.with_suffix('.json'))
            job['voiceCacheStored'] = True
            job['voiceCacheIdentity'] = descriptor['identity']
        return {'cacheKey': descriptor['cacheKey'], 'audioSha256': output['cachedAudioSha256']}
    finally:
        temporary.unlink(missing_ok=True)
        temporary_meta.unlink(missing_ok=True)


def select_brain_model(name, port, persistent=False):
    """Explicit local selection only; no loading, download or silent substitution."""
    if name not in ('q8', 'q4'):
        raise ValueError('Unknown answer model.')
    if name == 'q4':
        if port != 8770 or persistent:
            raise ValueError('Q4 requires port 8770 without the unvalidated persistent answer adapter.')
        path = ROOT/'.runtime'/'brain-q4-candidate'/'Qwen3-1.7B-Q4_K_M.gguf'
        if not path.is_file() or path.stat().st_size != 1282439264:
            raise ValueError('The verified local Q4 model is missing.')
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024*1024), b''):
                digest.update(block)
        if digest.hexdigest() != 'd2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5':
            raise ValueError('The local Q4 model does not match its verified hash.')
        return path
    return ROOT/'.runtime'/'Qwen3-1.7B-Q8_0.gguf'


def brain_model_label():
    return 'Qwen3 1.7B '+('Q4_K_M' if BRAIN_MODEL == 'q4' else 'Q8_0')


class PersistentCandidateVoice:
    """Optional low-memory candidate. The current job owns it while generating."""
    def __init__(self, worker_script=None, min_start_memory_gb=None):
        self.process = None
        self.tree = None
        self.stderr = None
        self.events = queue.Queue()
        self.ready = False
        self.active_job_id = None
        self.owner_session = None
        self.idle_timer = None
        self.worker_script = Path(worker_script) if worker_script else ROOT/'onnx_voice_worker.py'
        self.min_start_memory_gb = CANDIDATE_MIN_MEMORY_GB if min_start_memory_gb is None else min_start_memory_gb

    def stop(self):
        with LOCK:
            if self.idle_timer:
                self.idle_timer.cancel()
                self.idle_timer = None
            if self.tree:
                self.tree.terminate()
            if self.process:
                try:
                    self.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=10)
            if self.tree:
                self.tree.close()
            if self.stderr:
                self.stderr.close()
            self.process = self.tree = self.stderr = None
            self.ready = False
            self.active_job_id = self.owner_session = None

    def cancel_idle_owner(self, session):
        if self.process and self.active_job_id is None and self.owner_session == session:
            self.stop()

    def release_for_memory(self, job):
        if self.process and available_memory_gb() < 3:
            self.stop()
            job['warmVoiceReleasedForMemory'] = True

    def start(self, job, deadline=None):
        if self.idle_timer:
            self.idle_timer.cancel()
            self.idle_timer = None
        if self.process and self.process.poll() is not None:
            self.stop()
        if self.process:
            with LOCK:
                checkpoint(job)
                job['process'], job['processTree'] = self.process, self.tree
                job['activePid'] = self.process.pid
                self.active_job_id = job['id']
                self.owner_session = job.get('session')
            return True
        if MEMORY_PROFILE == 'compact':
            compact_entry(job, 'voice', deadline=deadline)
        elif available_memory_gb() < self.min_start_memory_gb:
            raise ResourceBusy('This computer is busy. Please try again shortly.')
        self.events = queue.Queue()
        self.stderr = (ROOT/'.runtime'/('onnx-worker-'+uuid.uuid4().hex[:8]+'.stderr.log')).open('wb')
        with LOCK:
            checkpoint(job)
            process = subprocess.Popen([str(VOICE_PYTHON), str(self.worker_script)],
                cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr,
                env=ENV, text=True, encoding='utf-8', errors='replace', bufsize=1,
                creationflags=HIDDEN | (0x4 if os.name == 'nt' else 0))
            self.process = process
            self.active_job_id = job['id']
            self.owner_session = job.get('session')
            job['process'] = process
            job['activePid'] = process.pid
            try:
                self.tree = OwnedProcessTree(process) if os.name == 'nt' else None
                job['processTree'] = self.tree
            except Exception:
                process.kill()
                process.wait(timeout=10)
                self.stop()
                raise
        events = self.events
        def collect():
            for line in process.stdout:
                try:
                    event = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if isinstance(event, dict) and event.get('type') in ('ready', 'chunk', 'result', 'error'):
                    events.put(event)
            events.put({'type': 'worker-exit'})
        threading.Thread(target=collect, daemon=True, name='optional-voice-output').start()
        return False

    def wait_event(self, job, deadline):
        while True:
            checkpoint(job)
            if time.monotonic() > deadline:
                raise RuntimeError('The optional local voice took too long.')
            try:
                event = self.events.get(timeout=.1)
            except queue.Empty:
                if not self.process or self.process.poll() is not None:
                    raise RuntimeError('The optional local voice worker stopped.')
                continue
            checkpoint(job)
            if event['type'] == 'worker-exit':
                raise RuntimeError('The optional local voice worker stopped.')
            return event

    def detach(self, job):
        with LOCK:
            job['process'] = job['processTree'] = None
            job['activePid'] = None
            if self.active_job_id == job['id']:
                self.active_job_id = None
            if self.process and self.ready:
                expected = self.process
                def expire():
                    with LOCK:
                        if self.process is expected and self.active_job_id is None:
                            self.stop()
                self.idle_timer = threading.Timer(120, expire)
                self.idle_timer.daemon = True
                self.idle_timer.start()

    def prewarm(self, job):
        started = time.monotonic()
        try:
            warm = self.start(job, deadline=started+180)
            job['voiceWorkerPid'] = self.process.pid
            if not self.ready:
                event = self.wait_event(job, started+180)
                if event['type'] != 'ready':
                    raise RuntimeError(event.get('error', 'The optional voice could not load.'))
                self.ready = True
            job['prewarmWorkerReused'] = warm
        except Exception:
            self.stop()
            raise
        finally:
            self.detach(job)
            job['timings']['prewarm'] = round(time.monotonic()-started, 3)
            if self.process and available_memory_gb() < 2:
                self.stop()
        return bool(self.process and self.ready)

    def generate(self, job, text, target, on_chunk=None):
        started = time.monotonic()
        deadline = started+240
        warm = False
        try:
            warm = self.start(job, deadline=deadline)
            job['voiceWorkerPid'] = self.process.pid
            if not self.ready:
                event = self.wait_event(job, deadline)
                if event['type'] != 'ready':
                    raise RuntimeError(event.get('error', 'The optional voice could not load.'))
                self.ready = True
                job['timings']['voice worker load'] = event.get('loadSeconds')
            checkpoint(job)
            request = {'id': job['id'], 'text': text, 'target': str(target), 'stream': on_chunk is not None}
            self.process.stdin.write(json.dumps(request)+'\n')
            self.process.stdin.flush()
            while True:
                event = self.wait_event(job, deadline)
                if event.get('id') != job['id']:
                    raise RuntimeError('The optional voice returned a mismatched reply.')
                if event['type'] != 'chunk':
                    break
                if not on_chunk:
                    raise RuntimeError('The voice returned an unexpected sentence.')
                published = on_chunk(event['chunk'])
                checkpoint(job)
                self.process.stdin.write(json.dumps({'type': 'chunk-ack', 'id': job['id'],
                    'index': event['chunk']['index'], 'publishedAtEpoch': published})+'\n')
                self.process.stdin.flush()
            if event['type'] != 'result':
                raise RuntimeError(event.get('error', 'The optional voice could not finish.'))
            checkpoint(job)
            job['voiceWorkerWarm'] = warm
        except Exception:
            self.stop()
            raise
        finally:
            self.detach(job)
            job['timings']['voice'] = round(time.monotonic()-started, 3)
            if self.process and available_memory_gb() < 2:
                self.stop()


CANDIDATE_VOICE = PersistentCandidateVoice()


def stop_child(job):
    tree = job.get('processTree')
    child = job.get('process')
    if tree:
        tree.terminate()
    elif child and child.poll() is None:
        child.terminate()


def checkpoint(job):
    if job['cancel'].is_set():
        raise Cancelled()
    child = job.get('process')
    if MEMORY_PROFILE == 'compact' and time.monotonic() >= job.get('deadlineMonotonic', float('inf')):
        if child is not None and child.poll() is None:
            stop_child(job)
        raise RuntimeError('The local reply deadline was reached.')
    if MEMORY_PROFILE == 'compact' and child is not None and child.poll() is None:
        state = memory_resources()
        observe_resources(job, state)
        if state['physicalGiB'] <= COMPACT_FLOOR_PHYSICAL or state['commitGiB'] <= COMPACT_FLOOR_COMMIT:
            job['resourceAbort'] = {**state, 'phase': job.get('phase'), 'atEpoch': time.time()}
            stop_child(job)
            raise ResourceBusy('This computer is busy. Please try again shortly.')


def stage(job, phase):
    with LOCK:
        checkpoint(job)
        job['phase'] = phase


def run_child(job, args, name, timeout):
    """Track only this job's direct process; never touch owner applications."""
    checkpoint(job)
    started = time.monotonic()
    compact_entry(job, name, deadline=started+timeout)
    folder = job['folder']
    with (folder / f'{name}.stdout.log').open('wb') as out, (folder / f'{name}.stderr.log').open('wb') as err:
        with LOCK:
            checkpoint(job)
            # Suspend before assigning the Windows job so a launcher cannot escape it.
            flags = HIDDEN | (0x4 if os.name == 'nt' else 0)
            child = subprocess.Popen(args, cwd=ROOT, stdin=subprocess.DEVNULL,
                                     stdout=out, stderr=err, env=ENV, creationflags=flags)
            job['process'] = child
            job['activePid'] = child.pid
            try:
                job['processTree'] = OwnedProcessTree(child) if os.name == 'nt' else None
            except Exception:
                child.kill()
                child.wait(timeout=10)
                job['process'] = None
                raise
        try:
            while child.poll() is None:
                if job['cancel'].wait(.1):
                    stop_child(job)
                    child.wait(timeout=10)
                    raise Cancelled()
                checkpoint(job)
                if time.monotonic() - started > timeout:
                    stop_child(job)
                    child.wait(timeout=10)
                    raise RuntimeError(f'The local {name} step took too long. Please try a shorter question.')
            checkpoint(job)
            if child.returncode:
                raise RuntimeError(f'The local {name} step failed. Please try again or use the text question.')
        finally:
            if child.poll() is None:
                stop_child(job)
                child.wait(timeout=10)
            with LOCK:
                try:
                    if job.get('processTree'):
                        try:
                            if SEQUENTIAL_MODELS:
                                job['processTree'].terminate()
                                job['processTree'].wait_empty()
                        finally:
                            job['processTree'].close()
                finally:
                    job['processTree'] = None
                    job['process'] = None
                    job['activePid'] = None
            job['timings'][name] = round(time.monotonic() - started, 3)
    return (folder / f'{name}.stdout.log').read_text(encoding='utf-8', errors='replace')


def decode_recording(job):
    """Normalize recorder timestamp gaps while bounding actual decoded samples."""
    source = Path(job['audio'])
    if not source.is_file() or not 0 < source.stat().st_size <= LIMIT:
        raise ValueError('The recording is empty or exceeds the upload limit.')
    decoded = job['folder']/'question.wav'
    run_child(job, [str(FFMPEG), '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
                   '-threads', '1', '-filter_threads', '1',
                   '-protocol_whitelist', 'file,pipe', '-format_whitelist', 'matroska,webm,mov,mp4,m4a,wav,ogg',
                   '-i', str(source), '-map', '0:a:0', '-vn', '-sn', '-dn',
                   '-af', 'asetpts=N/SR/TB', '-t', '20.1',
                   '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(decoded)], 'audio decode', 25)
    with wave.open(str(decoded), 'rb') as wav:
        if wav.getframerate() != 16000 or wav.getnchannels() != 1 or wav.getsampwidth() != 2:
            raise ValueError('The recording could not be decoded.')
        duration = wav.getnframes()/wav.getframerate()
    if duration > 20.05:
        raise ValueError('Please keep the recording under twenty seconds.')
    if duration < .25:
        raise ValueError('Please record at least a quarter second.')
    job['decodedAudioDuration'] = duration
    return decoded


def release_candidate_models(job, *, voice=False, answer=False, reason):
    """Explicit sequential mode never carries an owned model into the next stage."""
    targets = []
    if voice and CANDIDATE_VOICE.process:
        targets.append(('voice', CANDIDATE_VOICE.tree, CANDIDATE_VOICE.stop))
    if answer and CANDIDATE_BRAIN and CANDIDATE_BRAIN.process:
        targets.append(('answer', CANDIDATE_BRAIN.process_tree, CANDIDATE_BRAIN.close))
    for name, tree, close in targets:
        try:
            if tree:
                tree.terminate()
                tree.wait_empty()
        finally:
            close()
        job.setdefault('modelResidencyEvents', []).append({'model': name, 'event': 'unloaded', 'reason': reason})


def cancel(job):
    with LOCK:
        job['cancel'].set()
        job['phase'] = 'error'
        job['error'] = 'The question was cancelled.'
        job['errorCode'] = 'cancelled'
        job['cancelled'] = True
        job.pop('result', None)
        job.pop('chunks', None)
        stop_child(job)
        PENDING.purge_cancelled()
        CANDIDATE_VOICE.cancel_idle_owner(job.get('session'))
        if CANDIDATE_BRAIN:
            CANDIDATE_BRAIN.cancel(job['id'])
            CANDIDATE_BRAIN.cancel_idle_owner(job.get('session'))
    # Reply access checks job state, so even a completed file cannot be replayed after cancel.


def receipt(job):
    data = {key: job[key] for key in ('id', 'phase', 'text', 'created', 'timings', 'cancelled') if key in job}
    data.update({key: job[key] for key in ('result', 'error', 'retrieval', 'kind', 'streaming', 'chunks',
                                          'streamingEvents', 'prewarmWorkerReused', 'brainWarm', 'brainTimings',
                                          'brainReleasedForMemory', 'warmVoiceReleasedForMemory', 'voiceWorkerPid',
                                          'availableMemoryAtStartGiB', 'resourceRequirementGiB', 'failedAfterChunks',
                                          'errorCode', 'technicalError', 'requestId', 'decodedAudioDuration',
                                          'modelResidencyEvents', 'answerProvenance', 'validatorRejection',
                                          'resourceAdmission', 'resourceAbort', 'minimumPhysicalGiB',
                                          'minimumCommitGiB', 'voiceCacheIdentity', 'voiceCacheSource',
                                          'voiceCacheStored', 'voiceCacheReadError', 'voiceCacheWriteError') if key in job})
    data['offline'] = True
    data['providerCharge'] = 0
    data['voiceEngine'] = VOICE_ENGINE
    data['sttEngine'] = STT_ENGINE
    data['persistentBrain'] = CANDIDATE_BRAIN is not None
    data['sequentialModels'] = SEQUENTIAL_MODELS
    data['brainModel'] = BRAIN_MODEL
    data['brainModelFile'] = brain.MODEL.name
    data['noRepack'] = NO_REPACK
    data['memoryProfile'] = MEMORY_PROFILE
    data['memoryThresholds'] = memory_thresholds()
    data['voiceImplementation'] = 'encoder-release-seeded' if VOICE_ENGINE == 'onnx-q4' else 'original-mtl'
    data['sequentialStages'] = [('faster-whisper small.en int8 if audio' if STT_ENGINE == 'faster-small-en' else 'Whisper small if audio'), brain_model_label(),
                                'Chatterbox Multilingual' if VOICE_ENGINE == 'mtl' else 'Chatterbox Turbo ONNX q4 candidate']
    if VOICE_ENGINE == 'onnx-q4':
        data['warmVoiceMayRemainResident'] = not SEQUENTIAL_MODELS
    (job['folder'] / 'receipt.json').write_text(json.dumps(data, indent=2), encoding='utf-8')


def process_job(job):
    started = time.monotonic()
    folder = job['folder']
    completed_result = None
    try:
        checkpoint(job)
        job['startedMonotonic'] = started
        if MEMORY_PROFILE == 'compact':
            job['deadlineMonotonic'] = started+max(0, 600-(time.time()-job['created']))
        if SEQUENTIAL_MODELS:
            release_candidate_models(job, voice=True, answer=True, reason='before_request')
        elif CANDIDATE_BRAIN:
            job['brainReleasedForMemory'] = CANDIDATE_BRAIN.release_for_memory(3.0)
        CANDIDATE_VOICE.release_for_memory(job)
        job['availableMemoryAtStartGiB'] = round(available_memory_gb(), 3)
        job['resourceRequirementGiB'] = memory_thresholds()['entryPhysicalGiB']
        if MEMORY_PROFILE == 'compact':
            compact_entry(job, 'request')
        elif VOICE_ENGINE == 'onnx-q4' and job['availableMemoryAtStartGiB'] < CANDIDATE_MIN_MEMORY_GB:
            raise ResourceBusy('This computer is busy. Please try again shortly.')
        if job.get('kind') == 'prewarm':
            stage(job, 'warming')
            warmed = CANDIDATE_VOICE.prewarm(job)
            with LOCK:
                checkpoint(job)
                job['result'] = {'warmed': warmed, 'voiceEngine': VOICE_ENGINE}
                job['phase'] = 'done'
            return
        if job.get('audio'):
            stage(job, 'transcribing')
            decoded = decode_recording(job)
            transcript = folder / 'transcript.json'
            stt_command = ([str(VOICE_PYTHON), str(ROOT/'fast_stt_worker.py'), str(decoded), str(transcript)]
                           if STT_ENGINE == 'faster-small-en' else
                           [str(VOICE_PYTHON), str(ROOT/'speech_worker.py'), 'stt', str(decoded), str(transcript)])
            run_child(job, stt_command, 'transcription', 150)
            job['text'] = json.loads(transcript.read_text(encoding='utf-8'))['text']
        stage(job, 'thinking')
        CANDIDATE_VOICE.release_for_memory(job)
        with LOCK:
            history = list(HISTORY.get(job['session'], []))
        reviewed = property_context.reviewed_answer(job['text'], history) if PORT == 8770 else None
        if reviewed:
            answer = reviewed['text']
            job['answerProvenance'] = {key: value for key, value in reviewed.items() if key != 'text'}
            job['answerProvenance']['modelAttempted'] = False
            job['retrieval'] = [{'sourceUrl': reviewed['sourceUrl'], 'sourcePage': reviewed['sourcePage'],
                                 'sourceDate': reviewed['sourceDate'], 'topic': reviewed['topic']}]
            job['timings']['answer'] = 0
        else:
            prompt = folder / 'prompt.txt'
            job['retrieval'] = brain.build_prompt(job['text'], history, prompt, concise_first=CONCISE_FIRST)
            job['answerProvenance'] = {'mode': 'language_model', 'sourceUrl': brain.SOURCE_URL,
                                      'languageModelInference': True, 'modelAttempted': True}
        if not reviewed and CANDIDATE_BRAIN:
            def attach_brain(process):
                with LOCK:
                    job['process'] = process
                    job['processTree'] = None
                    job['activePid'] = process.pid if process else None
                    if process:
                        checkpoint(job)
            generated = CANDIDATE_BRAIN.answer(job['text'], history, cancel_event=job['cancel'],
                request_id=job['id'], session_id=job['session'], on_process=attach_brain, concise_first=CONCISE_FIRST)
            checkpoint(job)
            raw, answer = generated['raw'], generated['text']
            job['retrieval'] = generated['sources']
            job['brainWarm'], job['brainTimings'] = generated['warm'], generated['timings']
            job['timings']['answer'] = round(generated['timings']['total'], 3)
            (folder/'answer.stdout.log').write_text(raw, encoding='utf-8')
        elif not reviewed:
            raw = run_child(job, answer_command(prompt), 'answer', 180)
            answer = validated_candidate_answer(raw, job)
        job['answer'] = answer
        answer_file = folder / 'answer.txt'
        answer_file.write_text(answer, encoding='utf-8')
        stage(job, 'synthesizing')
        wav_file = RESPONSES / (job['id'] + '.wav')
        # Only an exact, previously generated answer with the same voice settings is reused.
        # This never supplies a substitute answer when the language model fails.
        if load_voice_cache(job, answer, wav_file):
            job['timings']['voice'] = 0
            job['voiceCacheHit'] = True
        else:
            if VOICE_ENGINE == 'onnx-q4':
                if SEQUENTIAL_MODELS:
                    release_candidate_models(job, answer=True, reason='before_voice')
                elif CANDIDATE_BRAIN:
                    if CANDIDATE_BRAIN.release_for_memory(3.0):
                        job['brainReleasedForMemory'] = True
                if STREAMING:
                    job['streaming'] = True
                    job['chunks'] = []
                    job['streamingEvents'] = []
                    def publish(chunk):
                        with LOCK:
                            checkpoint(job)
                            index = len(job['chunks'])
                            if chunk.get('index') != index:
                                raise RuntimeError('The voice returned an out-of-order sentence.')
                            chunk_file = RESPONSES/job['id']/f'chunk-{index}.wav'
                            if not chunk_file.is_file():
                                raise RuntimeError('The generated sentence file is missing.')
                            published = time.time()
                            elapsed = round(time.monotonic()-started, 3)
                            job['chunks'].append({**chunk, 'audioUrl': f"/responses/{job['id']}/chunk-{index}.wav",
                                                  'publishedAtEpoch': published})
                            job['streamingEvents'].append({'event': 'chunk-published', 'index': index,
                                                           'atEpoch': published, 'elapsedSeconds': elapsed})
                            if index == 0:
                                job['timings']['firstChunkReadySeconds'] = elapsed
                            job['phase'] = 'streaming'
                            return published
                    CANDIDATE_VOICE.generate(job, answer, wav_file, on_chunk=publish)
                else:
                    CANDIDATE_VOICE.generate(job, answer, wav_file)
            else:
                run_child(job, [str(VOICE_PYTHON), str(ROOT/'speech_worker.py'), 'tts', str(answer_file), str(wav_file)], 'voice', 420)
            checkpoint(job)
            job['voiceCacheHit'] = False
        voice = json.loads(wav_file.with_suffix('.json').read_text(encoding='utf-8'))
        result = {'audioUrl': '/responses/' + wav_file.name, 'text': answer, 'userText': job['text'],
                  'cues': voice['cues'], 'duration': voice['duration'],
                  **{key: value for key, value in job['answerProvenance'].items()
                     if key in ('mode', 'sourceUrl', 'sourcePage', 'sourceDate', 'languageModelInference',
                                'currentAvailabilityVerified', 'modelAttempted')},
                  'cueMethod': voice['cueMethod'], 'voiceCacheHit': job['voiceCacheHit'],
                  'voiceGenerationPerformed': not job['voiceCacheHit'],
                  'voiceEngine': VOICE_ENGINE, 'voiceCandidate': VOICE_ENGINE == 'onnx-q4',
                  'voiceWorkerWarm': job.get('voiceWorkerWarm', False),
                  'brainWarm': job.get('brainWarm', False), 'persistentBrain': CANDIDATE_BRAIN is not None}
        with LOCK:
            checkpoint(job)
            # Publish only after the finally block has verified owned cleanup.
            completed_result = result
    except Cancelled:
        cancel(job)
    except Exception as exc:
        with LOCK:
            if not job['cancel'].is_set():
                diagnostic = str(exc)
                job['phase'] = 'error'
                job['technicalError'] = diagnostic
                job['failedAfterChunks'] = len(job.get('chunks', []))
                job.pop('chunks', None)
                job.pop('result', None)
                if isinstance(exc, ResourceBusy) or 'Insufficient free physical memory' in diagnostic:
                    job['errorCode'] = 'resource_busy'
                    job['error'] = 'This computer is busy. Please try again shortly.'
                else:
                    job['errorCode'] = 'reply_failed'
                    job['error'] = 'The reply could not finish. Please try again.'
    finally:
        if SEQUENTIAL_MODELS:
            try:
                release_candidate_models(job, voice=True, answer=True, reason='after_request')
            except Exception as exc:
                with LOCK:
                    job['phase'] = 'error'
                    job['technicalError'] = 'Owned model cleanup failed: '+str(exc)
                    job['errorCode'] = 'reply_failed'
                    job['error'] = 'The reply could not finish. Please try again.'
                    job.pop('result', None)
                    job.pop('chunks', None)
        if completed_result is not None and job['phase'] != 'error':
            try:
                with LOCK:
                    checkpoint(job)
                    # Public polls and cancellation share this lock, so there is
                    # no visible done result before cleanup/cache commit completes.
                    job['phase'] = 'done'
                    if not job.get('voiceCacheHit'):
                        try:
                            store_completed_voice_cache(job, wav_file, voice)
                        except Cancelled:
                            raise
                        except Exception as exc:
                            # Cache failure alone does not invalidate complete audio.
                            job['voiceCacheWriteError'] = type(exc).__name__+': '+str(exc)
                    job['result'] = completed_result
                    HISTORY.setdefault(job['session'], []).append({'user': job['text'], 'assistant': answer})
                    HISTORY[job['session']] = HISTORY[job['session']][-4:]
            except Cancelled:
                cancel(job)
            except Exception as exc:
                with LOCK:
                    job['phase'] = 'error'
                    job['technicalError'] = 'Final reply publication failed: '+str(exc)
                    job['errorCode'] = 'reply_failed'
                    job['error'] = 'The reply could not finish. Please try again.'
                    job.pop('result', None)
                    job.pop('chunks', None)
        job['timings']['total'] = round(time.monotonic()-started, 3)
        receipt(job)


def worker():
    while True:
        job = PENDING.get()
        try:
            process_job(job)
        finally:
            PENDING.task_done()


def public_job(job):
    with LOCK:
        data = {'jobId': job['id'], 'phase': job['phase'], 'timings': dict(job['timings'])}
        data.update({key: job[key] for key in ('result', 'error', 'errorCode', 'cancelled') if key in job})
        if job.get('requestId'):
            data['requestId'] = job['requestId']
        if job.get('kind') == 'prewarm':
            data['kind'] = 'prewarm'
        if job.get('streaming'):
            data.update({'streaming': True, 'chunks': list(job.get('chunks', [])),
                         'userText': job['text'], 'responseText': job.get('answer', ''),
                         'completed': job['phase'] == 'done'})
        return data


class Handler(SimpleHTTPRequestHandler):
    server_version = 'NadLanLocal/1.0'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def setup(self):
        super().setup()
        self.connection.settimeout(20)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def allowed(self):
        if self.headers.get('Host', '') not in (f'{HOST}:{PORT}', f'localhost:{PORT}'):
            self.json_response({'error': 'This prototype accepts loopback requests only.'}, 403)
            return False
        origin = self.headers.get('Origin')
        if self.command == 'POST' and origin and origin not in (f'http://{HOST}:{PORT}', f'http://localhost:{PORT}'):
            self.json_response({'error': 'Only the local prototype can submit questions.'}, 403)
            return False
        if self.command == 'POST' and self.headers.get('Sec-Fetch-Site') == 'cross-site':
            self.json_response({'error': 'Only the local prototype can submit questions.'}, 403)
            return False
        return True

    def session(self):
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get('Cookie', ''))
            value = cookie.get('nl3d-session')
            if value and re.fullmatch(r'[a-f0-9]{32}', value.value):
                return value.value, False
        except Exception:
            pass
        return uuid.uuid4().hex, True

    def json_response(self, data, status=200, session=None):
        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        if session:
            self.send_header('Set-Cookie', f'nl3d-session={session}; Path=/; HttpOnly; SameSite=Strict')
        self.end_headers()
        self.wfile.write(payload)

    def find_job(self, job_id):
        session, _ = self.session()
        with LOCK:
            job = JOBS.get(job_id)
            if not job or job['session'] != session:
                self.json_response({'error': 'Question not found.'}, 404)
                return None
            return job

    def do_GET(self):
        if not self.allowed():
            return
        path = unquote(urlsplit(self.path).path)
        if path == '/api/session':
            session, fresh = self.session()
            self.json_response({'ready': True}, session=session if fresh else None)
            return
        if path == '/api/health':
            with LOCK:
                active_jobs = sum(job['phase'] not in ('queued', 'done', 'error') for job in JOBS.values())
            missing = [p.name for p in (VOICE_PYTHON, FFMPEG, brain.LLAMA, brain.MODEL,
                       ROOT.parent/'kit'/'ref-female.wav', ROOT/'source-page.html',
                       Path('C:/Users/777/.cache/whisper/small.pt')) if not p.is_file()]
            if VOICE_ENGINE == 'onnx-q4':
                candidate = ROOT/'.runtime'/'chatterbox-onnx-test'
                required = [candidate/'onnx_engine.py', ROOT/'research'/'onnx_encoder_release_candidate.py', candidate/'tokenizer.json',
                            candidate/'ort-1.31.1'/'onnxruntime'/'__init__.py']
                required += [candidate/'onnx'/(name+'_q4'+suffix) for name in
                             ('speech_encoder', 'embed_tokens', 'language_model', 'conditional_decoder')
                             for suffix in ('.onnx', '.onnx_data')]
                missing += [p.name for p in required if not p.is_file()]
            self.json_response({'available': not missing, 'localOnly': True, 'offline': True,
                                'missing': missing, 'readiness': 'local file checks, models load on demand',
                                'queued': PENDING.qsize(), 'activeJobs': active_jobs, 'maxRecordingSeconds': 20,
                                'requestCancellation': True,
                                'voiceEngine': VOICE_ENGINE, 'voiceCandidate': VOICE_ENGINE == 'onnx-q4',
                                'streaming': STREAMING, 'prewarmAvailable': PREWARM_ENABLED,
                                'persistentBrain': CANDIDATE_BRAIN is not None, 'sttEngine': STT_ENGINE,
                                'sequentialModels': SEQUENTIAL_MODELS,
                                'brainModel': BRAIN_MODEL, 'brainModelFile': brain.MODEL.name,
                                'noRepack': NO_REPACK, 'memoryProfile': MEMORY_PROFILE,
                                'resourceAdmission': {'physicalGiB': memory_thresholds()['entryPhysicalGiB'],
                                                      'commitGiB': memory_thresholds()['entryCommitGiB']},
                                'memoryThresholds': memory_thresholds(),
                                'voiceImplementation': 'encoder-release-seeded' if VOICE_ENGINE == 'onnx-q4' else 'original-mtl',
                                'reviewedPropertyFacts': PORT == 8770,
                                'conciseFirst': CONCISE_FIRST})
            return
        match = re.fullmatch(r'/api/jobs/([a-f0-9]{32})', path)
        if match:
            job = self.find_job(match[1])
            if job:
                self.json_response(public_job(job))
            return
        authorized_response = False
        chunk_match = re.fullmatch(r'/responses/([a-f0-9]{32})/chunk-(\d+)\.wav', path)
        if chunk_match:
            job = self.find_job(chunk_match[1])
            if not job:
                return
            with LOCK:
                valid = (job['phase'] in ('streaming', 'done') and not job['cancel'].is_set()
                         and any(chunk['index'] == int(chunk_match[2]) for chunk in job.get('chunks', [])))
            if not valid:
                self.json_response({'error': 'This sentence is no longer available.'}, 404)
                return
            authorized_response = True
        match = re.fullmatch(r'/responses/([a-f0-9]{32})\.wav', path)
        if match:
            job = self.find_job(match[1])
            if not job:
                return
            if job['phase'] != 'done' or job['cancel'].is_set():
                self.json_response({'error': 'This reply is no longer available.'}, 404)
                return
            authorized_response = True
        if path.startswith('/api/'):
            self.json_response({'error': 'Not found.'}, 404)
            return
        if path in ('/', '/conversation-preview.html'):
            html = (ROOT/'site-preview.html').read_text(encoding='utf-8')
            marker = '<script type="module" src="widget.js"></script>'
            if marker not in html:
                self.send_error(500, 'The local preview module was not found.')
                return
            if STREAMING:
                configuration = {'conversationEndpoint': '/api/converse', 'pollInterval': 300}
                if PREWARM_ENABLED:
                    configuration['prewarmEndpoint'] = '/api/prewarm'
                replacement = ('<script>window.__NL3D={...(window.__NL3D||{}),...'+json.dumps(configuration)+'};</script>\n'
                               '<script type="module" src="widget-stream.js"></script>')
            else:
                replacement = '<script>window.__NL3D={...(window.__NL3D||{}),conversationEndpoint:"/api/converse"};</script>\n'+marker
            html = html.replace(marker, replacement)
            payload = html.encode('utf-8')
            session, fresh = self.session()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            if fresh:
                self.send_header('Set-Cookie', f'nl3d-session={session}; Path=/; HttpOnly; SameSite=Strict')
            self.end_headers()
            self.wfile.write(payload)
            return
        resolved = (ROOT / path.lstrip('/')).resolve()
        if (not resolved.is_relative_to(ROOT) or not resolved.is_file()
                or any(part.startswith('.') for part in resolved.relative_to(ROOT).parts)
                or resolved.suffix.lower() not in {'.html', '.css', '.js', '.mjs', '.json', '.glb',
                    '.png', '.jpg', '.jpeg', '.webp', '.svg', '.mp3', '.wav', '.woff', '.woff2', '.bin', '.wasm'}
                or path.startswith('/responses/') and not authorized_response):
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self):
        # Static-file checks also apply to HEAD. Job audio uses authenticated GET.
        if not self.allowed():
            return
        path = unquote(urlsplit(self.path).path)
        resolved = (ROOT / path.lstrip('/')).resolve()
        if path == '/':
            self.path = '/site-preview.html'
            resolved = ROOT/'site-preview.html'
        if (not resolved.is_relative_to(ROOT) or not resolved.is_file()
                or any(part.startswith('.') for part in resolved.relative_to(ROOT).parts)
                or resolved.suffix.lower() not in {'.html', '.css', '.js', '.mjs', '.glb', '.png', '.jpg', '.webp', '.mp3', '.woff2', '.bin', '.wasm'}):
            self.send_error(404)
            return
        super().do_HEAD()

    def do_POST(self):
        if not self.allowed():
            return
        path = urlsplit(self.path).path
        token_match = re.fullmatch(r'/api/requests/([A-Za-z0-9_-]{16,80})/cancel', path)
        if token_match:
            session, fresh = self.session()
            request_id = token_match[1]
            if fresh:
                self.json_response({'errorCode': 'session_required', 'error': 'Please reopen the conversation and try again.'}, 409)
                return
            with LOCK:
                state = token_state(session)
                if state is None:
                    self.json_response({'errorCode': 'resource_busy', 'error': 'This computer is busy. Please try again shortly.'}, 429)
                    return
                if request_id in state['cancelled'] or len(state['cancelled']) < TOKEN_LIMIT:
                    state['cancelled'][request_id] = time.monotonic()+TOKEN_TTL
                else:
                    # Overflow fails closed only for new requests in this session.
                    state['barrierUntil'] = time.monotonic()+TOKEN_TTL
                registered = state['requests'].get(request_id)
                job = JOBS.get(registered.get('jobId')) if registered else None
                if job:
                    cancel(job)
                    receipt(job)
            self.json_response(cancelled_request(request_id))
            return
        if path == '/api/prewarm':
            if not PREWARM_ENABLED or not STREAMING or VOICE_ENGINE != 'onnx-q4':
                self.json_response({'error': 'Prewarming is available only in the optional local comparison.'}, 404)
                return
            session, fresh = self.session()
            request_id = self.headers.get('X-NL-Request-ID')
            if request_id and not re.fullmatch(r'[A-Za-z0-9_-]{16,80}', request_id):
                self.json_response({'errorCode': 'invalid_request_id', 'error': 'Please try again.'}, 400)
                return
            if request_id and fresh:
                self.json_response({'errorCode': 'session_required', 'error': 'Please reopen the conversation and try again.'}, 409, session=session)
                return
            with LOCK:
                state = token_state(session) if request_id else None
                if request_id:
                    if state is None or len(state['requests']) >= TOKEN_LIMIT and request_id not in state['requests']:
                        self.json_response({'errorCode': 'resource_busy', 'error': 'This computer is busy. Please try again shortly.'}, 429)
                        return
                    if token_cancelled(state, request_id):
                        self.json_response(cancelled_request(request_id), 409)
                        return
                    registered = state['requests'].get(request_id)
                    prior_job = JOBS.get(registered.get('jobId')) if registered else None
                    if prior_job:
                        self.json_response(public_job(prior_job), 202)
                        return
                existing = next((job for job in JOBS.values() if job['session'] == session
                                 and job.get('kind') == 'prewarm' and job['phase'] not in ('done', 'error')), None)
                if existing:
                    if request_id:
                        state['requests'][request_id] = {'jobId': existing['id'], 'expires': time.monotonic()+900}
                    self.json_response({**public_job(existing), **({'requestId': request_id} if request_id else {})},
                                       202, session if fresh else None)
                    return
                PENDING.purge_cancelled()
                if PENDING.full():
                    self.json_response({'error': 'The local voice is busy. Please try again shortly.'}, 429)
                    return
                job_id = uuid.uuid4().hex
                folder = WORK/job_id
                folder.mkdir(parents=True)
                job = {'id': job_id, 'session': session, 'kind': 'prewarm', 'text': '', 'phase': 'queued',
                       'created': time.time(), 'folder': folder, 'cancel': threading.Event(),
                       'process': None, 'activePid': None, 'timings': {}}
                if request_id:
                    job['requestId'] = request_id
                    state['requests'][request_id] = {'jobId': job_id, 'expires': time.monotonic()+900}
                JOBS[job_id] = job
                PENDING.put_nowait(job)
            self.json_response({'jobId': job_id, 'phase': 'queued', 'kind': 'prewarm',
                                **({'requestId': request_id} if request_id else {})}, 202, session if fresh else None)
            return
        match = re.fullmatch(r'/api/jobs/([a-f0-9]{32})/cancel', path)
        if match:
            job = self.find_job(match[1])
            if job:
                cancel(job)
                receipt(job)
                self.json_response(public_job(job))
            return
        if path != '/api/converse':
            self.json_response({'error': 'Not found.'}, 404)
            return
        request_started = time.monotonic()
        request_id = self.headers.get('X-NL-Request-ID')
        reserved_here = False
        session = None
        registered_job = None
        if request_id:
            if not re.fullmatch(r'[A-Za-z0-9_-]{16,80}', request_id):
                self.json_response({'errorCode': 'invalid_request_id', 'error': 'Please try sending the question again.'}, 400)
                return
            session, fresh = self.session()
            if fresh:
                self.json_response({'errorCode': 'session_required', 'error': 'Please reopen the conversation and try again.'},
                                   409, session=session)
                return
            with LOCK:
                state = token_state(session)
                if state is None or len(state['requests']) >= TOKEN_LIMIT and request_id not in state['requests']:
                    self.json_response({'errorCode': 'resource_busy', 'error': 'This computer is busy. Please try again shortly.'}, 429)
                    return
                if token_cancelled(state, request_id):
                    self.json_response(cancelled_request(request_id), 409)
                    return
                prior = state['requests'].get(request_id)
                if prior:
                    prior_job = JOBS.get(prior.get('jobId'))
                    if prior_job:
                        self.json_response(public_job(prior_job), 202)
                    else:
                        self.json_response({'errorCode': 'request_pending', 'error': 'This question is already arriving.'}, 409)
                    return
                state['requests'][request_id] = {'jobId': None, 'expires': request_started+REGISTRATION_DEADLINE}
                reserved_here = True
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if self.headers.get('Transfer-Encoding') or not 0 < size <= LIMIT:
                self.json_response({'error': 'Please send a recording smaller than fifteen megabytes.'}, 413)
                return
            body = self.rfile.read(size)
            if len(body) != size:
                raise ValueError('The recording was incomplete. Please try again.')
            if time.monotonic()-request_started > REGISTRATION_DEADLINE:
                self.json_response({'errorCode': 'upload_timeout', 'error': 'The question took too long to arrive. Please try again.'}, 408)
                return
            content_type = self.headers.get('Content-Type', '')
            text, audio = '', None
            if content_type.startswith('application/json'):
                value = json.loads(body)
                if not isinstance(value, dict):
                    raise ValueError('Please send a text question object.')
                text = value.get('text', '')
                if not isinstance(text, str) or not text.strip() or len(text) > 1200:
                    raise ValueError('Please type one short question.')
                text = text.strip()
            elif content_type.startswith('multipart/form-data'):
                message = BytesParser(policy=policy.default).parsebytes(
                    ('Content-Type: '+content_type+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+body)
                for part in message.iter_parts():
                    if part.get_param('name', header='content-disposition') == 'audio':
                        audio = part.get_payload(decode=True)
                        break
                if not audio or len(audio) > LIMIT:
                    raise ValueError('Please attach a short audio recording.')
            else:
                self.json_response({'error': 'Send a text question or microphone recording.'}, 415)
                return
            session, fresh = self.session()
            with LOCK:
                if request_id:
                    state = token_state(session)
                    if not state or token_cancelled(state, request_id):
                        self.json_response(cancelled_request(request_id), 409)
                        return
                    if time.monotonic()-request_started > REGISTRATION_DEADLINE:
                        self.json_response({'errorCode': 'upload_timeout', 'error': 'The question took too long to arrive. Please try again.'}, 408)
                        return
                for previous in list(JOBS.values()):
                    if previous['session'] == session and previous['phase'] not in ('done', 'error') and previous.get('kind') != 'prewarm':
                        cancel(previous)
                PENDING.purge_cancelled()
                if PENDING.full():
                    self.json_response({'error': 'The local voice is busy. Please try again shortly.'}, 429)
                    return
                job_id = uuid.uuid4().hex
                folder = WORK / job_id
                folder.mkdir(parents=True)
                job = {'id': job_id, 'session': session, 'text': text, 'phase': 'queued',
                       'created': time.time(), 'folder': folder, 'cancel': threading.Event(),
                       'process': None, 'activePid': None, 'timings': {}}
                if request_id:
                    job['requestId'] = request_id
                    state['requests'][request_id] = {'jobId': job_id, 'expires': time.monotonic()+900}
                if audio:
                    job['audio'] = folder / 'upload.audio'
                    job['audio'].write_bytes(audio)
                JOBS[job_id] = job
                registered_job = job
                PENDING.put_nowait(job)
            self.json_response({'jobId': job_id, 'phase': 'queued', **({'requestId': request_id} if request_id else {})},
                               202, session if fresh else None)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self.json_response({'error': str(exc)}, 400)
        except (TimeoutError, ConnectionError):
            self.close_connection = True
            if registered_job:
                cancel(registered_job)
                receipt(registered_job)
        finally:
            if reserved_here and session:
                with LOCK:
                    state = token_state(session, create=False)
                    item = state['requests'].get(request_id) if state else None
                    if item and not item.get('jobId'):
                        del state['requests'][request_id]

    def log_message(self, fmt, *args):
        print(time.strftime('%H:%M:%S'), fmt % args, flush=True)


def main():
    global VOICE_ENGINE, STREAMING, PREWARM_ENABLED, CANDIDATE_BRAIN, STT_ENGINE, CONCISE_FIRST, SEQUENTIAL_MODELS, BRAIN_MODEL, PORT, NO_REPACK, MEMORY_PROFILE
    parser = argparse.ArgumentParser()
    parser.add_argument('--voice-engine', choices=('mtl', 'onnx-q4'), default='mtl',
                        help='mtl preserves the existing voice; onnx-q4 is an optional comparison')
    parser.add_argument('--port', type=int, choices=(8769, 8770), default=8769)
    parser.add_argument('--streaming', action='store_true', help='publish actual per-sentence candidate speech on port 8770')
    parser.add_argument('--prewarm', action='store_true', help='enable explicit first-gesture prewarming on the streaming candidate')
    parser.add_argument('--persistent-brain', action='store_true', help='reuse the same local Qwen in the optional comparison')
    parser.add_argument('--stt-engine', choices=('whisper-small', 'faster-small-en'), default='whisper-small')
    parser.add_argument('--concise-first', action='store_true', help='experimental shorter prompt; not accepted for the review')
    parser.add_argument('--sequential-models', action='store_true', help='unload owned candidate models between stages and after each turn')
    parser.add_argument('--brain-model', choices=('q8', 'q4'), default='q8', help='explicit local Q4 comparison on port 8770; default preserves Q8')
    parser.add_argument('--no-repack', action='store_true', help='explicit candidate Q4 CPU mapped-weight path')
    parser.add_argument('--memory-profile', choices=('legacy', 'compact'), default='legacy',
                        help='compact is a provisional sequential Q4/ONNX profile; original defaults remain unchanged')
    args = parser.parse_args()
    if args.port == 8769 and (args.voice_engine != 'mtl' or args.streaming):
        parser.error('Port 8769 preserves the original MTL review. Use --port 8770 for the candidate.')
    if args.port == 8770 and args.voice_engine != 'onnx-q4':
        parser.error('Port 8770 is reserved for the optional ONNX comparison.')
    if args.prewarm and not args.streaming:
        parser.error('Prewarming is available only with the streaming candidate.')
    if args.persistent_brain and args.port != 8770:
        parser.error('The persistent answer worker is available only on candidate port 8770.')
    if args.stt_engine != 'whisper-small' and args.port != 8770:
        parser.error('The optional English transcription worker is available only on candidate port 8770.')
    if args.concise_first and args.port != 8770:
        parser.error('The experimental shorter prompt is available only on candidate port 8770.')
    if args.sequential_models and (args.port != 8770 or args.prewarm):
        parser.error('Sequential models require candidate port 8770 and cannot be combined with prewarming.')
    if args.no_repack and (args.port != 8770 or args.brain_model != 'q4' or args.persistent_brain):
        parser.error('--no-repack requires candidate Q4 on port 8770 without a persistent answer worker.')
    if args.memory_profile == 'compact' and (args.port != 8770 or args.brain_model != 'q4'
            or not args.no_repack or not args.sequential_models or args.persistent_brain):
        parser.error('Compact memory requires candidate port 8770, Q4, --no-repack and --sequential-models.')
    try:
        selected_brain = select_brain_model(args.brain_model, args.port, args.persistent_brain)
    except ValueError as exc:
        parser.error(str(exc))
    VOICE_ENGINE = args.voice_engine
    STREAMING = args.streaming
    PREWARM_ENABLED = args.prewarm
    PORT = args.port
    STT_ENGINE = args.stt_engine
    CONCISE_FIRST = args.concise_first
    SEQUENTIAL_MODELS = args.sequential_models
    BRAIN_MODEL = args.brain_model
    NO_REPACK = args.no_repack
    MEMORY_PROFILE = args.memory_profile
    brain.MODEL = selected_brain
    if args.persistent_brain:
        from research.candidate_brain_server import WarmBrainCandidate
        CANDIDATE_BRAIN = WarmBrainCandidate(process_tree_factory=OwnedProcessTree)
    WORK.mkdir(parents=True, exist_ok=True)
    RESPONSES.mkdir(exist_ok=True)
    VOICE_CACHE.mkdir(exist_ok=True)
    mimetypes.add_type('application/javascript', '.mjs')
    mimetypes.add_type('model/gltf-binary', '.glb')
    threading.Thread(target=worker, daemon=True, name='sequential-local-inference').start()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'Local approval prototype: http://{HOST}:{PORT}/', flush=True)
    print('Offline CPU inference. No deployment and no paid service.', flush=True)
    print('Voice engine: '+VOICE_ENGINE+(' (approved lighter voice for the pilot)' if VOICE_ENGINE != 'mtl' else '')+
          ('; true sentence streaming enabled' if STREAMING else ''), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        with LOCK:
            for job in JOBS.values():
                if job['phase'] not in ('done', 'error'):
                    cancel(job)
        CANDIDATE_VOICE.stop()
        if CANDIDATE_BRAIN:
            CANDIDATE_BRAIN.close()
        server.server_close()


if __name__ == '__main__':
    main()
