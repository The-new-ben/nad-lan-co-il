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
CANDIDATE_MIN_MEMORY_GB = 3.0
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

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None


def available_memory_gb():
    if os.name != 'nt':
        return 0
    import ctypes
    class Memory(ctypes.Structure):
        _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [
            (name, ctypes.c_uint64) for name in ('totalPhysical', 'availablePhysical',
                'totalPage', 'availablePage', 'totalVirtual', 'availableVirtual', 'extended')]
    state = Memory()
    state.length = ctypes.sizeof(state)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(state)):
        return 0
    return state.availablePhysical/(1024**3)


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

    def start(self, job):
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
        if available_memory_gb() < self.min_start_memory_gb:
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
            warm = self.start(job)
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
            warm = self.start(job)
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


def stage(job, phase):
    with LOCK:
        checkpoint(job)
        job['phase'] = phase


def run_child(job, args, name, timeout):
    """Track only this job's direct process; never touch owner applications."""
    checkpoint(job)
    started = time.monotonic()
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
                if job.get('processTree'):
                    job['processTree'].close()
                    job['processTree'] = None
                job['process'] = None
                job['activePid'] = None
            job['timings'][name] = round(time.monotonic() - started, 3)
    return (folder / f'{name}.stdout.log').read_text(encoding='utf-8', errors='replace')


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
                                          'errorCode', 'technicalError', 'requestId') if key in job})
    data['offline'] = True
    data['providerCharge'] = 0
    data['voiceEngine'] = VOICE_ENGINE
    data['sttEngine'] = STT_ENGINE
    data['persistentBrain'] = CANDIDATE_BRAIN is not None
    data['sequentialStages'] = [('faster-whisper small.en int8 if audio' if STT_ENGINE == 'faster-small-en' else 'Whisper small if audio'), 'Qwen3 1.7B Q8_0',
                                'Chatterbox Multilingual' if VOICE_ENGINE == 'mtl' else 'Chatterbox Turbo ONNX q4 candidate']
    if VOICE_ENGINE == 'onnx-q4':
        data['warmVoiceMayRemainResident'] = True
    (job['folder'] / 'receipt.json').write_text(json.dumps(data, indent=2), encoding='utf-8')


def process_job(job):
    started = time.monotonic()
    folder = job['folder']
    try:
        checkpoint(job)
        job['startedMonotonic'] = started
        if CANDIDATE_BRAIN:
            job['brainReleasedForMemory'] = CANDIDATE_BRAIN.release_for_memory(3.0)
        CANDIDATE_VOICE.release_for_memory(job)
        job['availableMemoryAtStartGiB'] = round(available_memory_gb(), 3)
        job['resourceRequirementGiB'] = CANDIDATE_MIN_MEMORY_GB
        if VOICE_ENGINE == 'onnx-q4' and job['availableMemoryAtStartGiB'] < CANDIDATE_MIN_MEMORY_GB:
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
            decoded = folder / 'question.wav'
            run_child(job, [str(FFMPEG), '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
                           '-protocol_whitelist', 'file,pipe', '-format_whitelist', 'matroska,webm,mov,mp4,m4a,wav,ogg',
                           '-i', str(job['audio']), '-t', '20.1',
                           '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', str(decoded)], 'audio decode', 25)
            with wave.open(str(decoded), 'rb') as wav:
                duration = wav.getnframes()/wav.getframerate()
            if duration > 20.05:
                raise ValueError('Please keep the recording under twenty seconds.')
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
        prompt = folder / 'prompt.txt'
        job['retrieval'] = brain.build_prompt(job['text'], history, prompt, concise_first=CONCISE_FIRST)
        if CANDIDATE_BRAIN:
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
        else:
            raw = run_child(job, brain.command(prompt), 'answer', 180)
            answer = brain.clean_answer(raw)
        job['answer'] = answer
        answer_file = folder / 'answer.txt'
        answer_file.write_text(answer, encoding='utf-8')
        stage(job, 'synthesizing')
        wav_file = RESPONSES / (job['id'] + '.wav')
        # Only an exact, previously generated answer with the same voice settings is reused.
        # This never supplies a substitute answer when the language model fails.
        reference_hash = hashlib.sha256((ROOT.parent/'kit'/'ref-female.wav').read_bytes()).hexdigest()
        voice_identity = (f'chatterbox-v2|{reference_hash}|.5|.5|.65|' if VOICE_ENGINE == 'mtl' else
                          f'chatterbox-turbo-onnx-q4|d21799bd0354|{reference_hash}|greedy|1.2|')
        cache_key = hashlib.sha256((voice_identity+answer).encode()).hexdigest()
        cached_wav = VOICE_CACHE / (cache_key+'.wav')
        cached_meta = cached_wav.with_suffix('.json')
        if not STREAMING and cached_wav.exists() and cached_meta.exists():
            shutil.copyfile(cached_wav, wav_file)
            shutil.copyfile(cached_meta, wav_file.with_suffix('.json'))
            job['timings']['voice'] = 0
            job['voiceCacheHit'] = True
        else:
            if VOICE_ENGINE == 'onnx-q4':
                if CANDIDATE_BRAIN:
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
            if not STREAMING:
                shutil.copyfile(wav_file, cached_wav)
                shutil.copyfile(wav_file.with_suffix('.json'), cached_meta)
            job['voiceCacheHit'] = False
        voice = json.loads(wav_file.with_suffix('.json').read_text(encoding='utf-8'))
        result = {'audioUrl': '/responses/' + wav_file.name, 'text': answer, 'userText': job['text'],
                  'cues': voice['cues'], 'duration': voice['duration'], 'sourceUrl': brain.SOURCE_URL,
                  'cueMethod': voice['cueMethod'], 'voiceCacheHit': job['voiceCacheHit'],
                  'voiceEngine': VOICE_ENGINE, 'voiceCandidate': VOICE_ENGINE == 'onnx-q4',
                  'voiceWorkerWarm': job.get('voiceWorkerWarm', False),
                  'brainWarm': job.get('brainWarm', False), 'persistentBrain': CANDIDATE_BRAIN is not None}
        with LOCK:
            checkpoint(job)
            job['result'] = result
            job['phase'] = 'done'
            HISTORY.setdefault(job['session'], []).append({'user': job['text'], 'assistant': answer})
            HISTORY[job['session']] = HISTORY[job['session']][-4:]
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
                required = [candidate/'onnx_engine.py', candidate/'tokenizer.json',
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
    global VOICE_ENGINE, STREAMING, PREWARM_ENABLED, CANDIDATE_BRAIN, STT_ENGINE, CONCISE_FIRST, PORT
    parser = argparse.ArgumentParser()
    parser.add_argument('--voice-engine', choices=('mtl', 'onnx-q4'), default='mtl',
                        help='mtl preserves the existing voice; onnx-q4 is an optional comparison')
    parser.add_argument('--port', type=int, choices=(8769, 8770), default=8769)
    parser.add_argument('--streaming', action='store_true', help='publish actual per-sentence candidate speech on port 8770')
    parser.add_argument('--prewarm', action='store_true', help='enable explicit first-gesture prewarming on the streaming candidate')
    parser.add_argument('--persistent-brain', action='store_true', help='reuse the same local Qwen in the optional comparison')
    parser.add_argument('--stt-engine', choices=('whisper-small', 'faster-small-en'), default='whisper-small')
    parser.add_argument('--concise-first', action='store_true', help='experimental shorter prompt; not accepted for the review')
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
    VOICE_ENGINE = args.voice_engine
    STREAMING = args.streaming
    PREWARM_ENABLED = args.prewarm
    PORT = args.port
    STT_ENGINE = args.stt_engine
    CONCISE_FIRST = args.concise_first
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
    print('Voice engine: '+VOICE_ENGINE+(' (optional comparison, not the approved voice)' if VOICE_ENGINE != 'mtl' else '')+
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
