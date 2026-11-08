"""Prepared isolated original-voice benchmark. Only --go starts the owned child."""
from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
VOICE_PYTHON = Path('C:/Users/777/nad-lan/voice-rig/venv/Scripts/python.exe')
CHECKPOINT = Path('C:/Users/777/.cache/huggingface/hub/models--ResembleAI--chatterbox/snapshots/5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18')
REFERENCE = ROOT.parent/'kit/ref-female.wav'
# This is the agent's controlled public identity-question answer, not Ben's microphone.
TEXT_SOURCE = ROOT/'.runtime/jobs/87a159f1027a4f00ae308066b26e7d86/answer.txt'
OUT = ROOT/'evidence/original-mtl-loader-candidate'
PHYSICAL_FLOOR = .75
COMMIT_FLOOR = 1.0
PREFLIGHT_PHYSICAL = 6.0
PREFLIGHT_COMMIT = 8.0


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2), encoding='utf8')


def child():
    def blocked(*args, **kwargs):
        raise RuntimeError('Network is disabled in the isolated voice benchmark.')
    socket.socket.connect = blocked
    socket.socket.connect_ex = blocked
    socket.create_connection = blocked
    for key, value in {'HF_HUB_OFFLINE':'1', 'TRANSFORMERS_OFFLINE':'1', 'HF_HUB_DISABLE_TELEMETRY':'1',
                       'OMP_NUM_THREADS':'4', 'MKL_NUM_THREADS':'4', 'TOKENIZERS_PARALLELISM':'false'}.items():
        os.environ[key] = value
    from mtl_loader_candidate import file_sha256, load_original_mtl_candidate
    import inspect
    import librosa
    import numpy as np
    import soundfile as sf
    import torch
    import s3tokenizer.model_v2 as s3tokenizer_model
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS, Conditionals, VoiceEncoder, T3, S3Gen

    installed = Path(inspect.getfile(ChatterboxMultilingualTTS)).parent
    checkpoint_files = ['ve.pt', 't3_mtl23ls_v2.safetensors', 's3gen.pt',
                        'grapheme_mtl_merged_expanded_v1.json', 'conds.pt', 'Cangjie5_TC.json']
    sources = [Path(__file__), Path(__file__).with_name('mtl_loader_candidate.py'), ROOT/'speech_worker.py',
               Path(inspect.getfile(ChatterboxMultilingualTTS)), Path(inspect.getfile(VoiceEncoder)),
               Path(inspect.getfile(T3)), Path(inspect.getfile(S3Gen)),
               Path(inspect.getfile(s3tokenizer_model)), REFERENCE, TEXT_SOURCE]
    sources += [CHECKPOINT/name for name in checkpoint_files]
    manifest = [{'path':str(path), 'bytes':path.stat().st_size, 'modifiedNs':path.stat().st_mtime_ns,
                 'sha256':file_sha256(path)} for path in sources]
    save_json(OUT/'source-manifest.json', {'files':manifest,'checkpointRevision':CHECKPOINT.name})
    original_text = TEXT_SOURCE.read_text(encoding='utf8').strip()
    text = re.findall(r'[^.!?]+[.!?]+|[^.!?]+$', original_text)[0].strip()
    if text != "I'm a fictional, computer-made guide.":
        raise RuntimeError('The reviewed controlled benchmark sentence changed.')
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    torch.manual_seed(682)
    started = time.monotonic()
    model, verification = load_original_mtl_candidate(CHECKPOINT, OUT)
    model_loaded = time.monotonic()
    reference_hash = file_sha256(REFERENCE)
    cache = ROOT/'.runtime'/('reference-'+reference_hash[:16]+'-'+CHECKPOINT.name[:12]+'.pt')
    cache_hash = file_sha256(cache) if cache.exists() else None
    if cache.exists():
        model.conds = Conditionals.load(cache, map_location='cpu')
        reference_cache_hit = True
    else:
        model.prepare_conditionals(str(REFERENCE), exaggeration=.5)
        model.conds.save(OUT/'candidate-reference-conditionals.pt')
        reference_cache_hit = False
    before_speech_rng = torch.get_rng_state().numpy().tobytes()
    (OUT/'rng-before-speech.bin').write_bytes(before_speech_rng)
    ready = time.monotonic()
    print(json.dumps({'phase':'loaded','loadSeconds':round(ready-started,3)}), flush=True)
    wav = model.generate(text, language_id='en', exaggeration=.5, cfg_weight=.5, temperature=.65)
    samples = wav.squeeze(0).numpy()
    samples, _ = librosa.effects.trim(samples, top_db=38)
    if not 1 <= len(samples)/model.sr <= 35 or not np.isfinite(samples).all():
        raise RuntimeError('The original voice candidate returned an unusable recording.')
    sf.write(OUT/'candidate.wav', samples, model.sr, subtype='PCM_16')
    after_speech_rng = torch.get_rng_state().numpy().tobytes()
    (OUT/'rng-after-speech.bin').write_bytes(after_speech_rng)
    # Recheck all small inputs; large weights retain size/mtime plus their initial full hash.
    large_weights = {CHECKPOINT/name for name in ('ve.pt','t3_mtl23ls_v2.safetensors','s3gen.pt')}
    for item in manifest:
        path = Path(item['path'])
        if path.stat().st_size != item['bytes'] or path.stat().st_mtime_ns != item['modifiedNs']:
            raise RuntimeError('A reviewed source changed during the experiment.')
        if path not in large_weights and file_sha256(path) != item['sha256']:
            raise RuntimeError('A reviewed small input changed during the experiment.')
    if reference_cache_hit and file_sha256(cache) != cache_hash:
        raise RuntimeError('The original reference cache changed during the experiment.')
    result = {'outcome':'generated', 'engine':'Original Chatterbox Multilingual, CPU, offline',
              'loaderCandidate':True, 'installedEnvironmentModified':False, 'serverDefaultChanged':False,
              'text':text, 'textSourceSha256':file_sha256(TEXT_SOURCE), 'referenceSha256':reference_hash,
              'referenceCacheHit':reference_cache_hit, 'referenceCacheSha256':cache_hash,
              'exaggeration':.5,'cfgWeight':.5,'temperature':.65,'seed':682,'threads':4,
              'modelLoadAndVerificationSeconds':round(model_loaded-started,3),
              'referenceSeconds':round(ready-model_loaded,3), 'generationSeconds':round(time.monotonic()-ready,3),
              'audioSeconds':len(samples)/model.sr,'sampleRate':model.sr,
              'audioSha256':file_sha256(OUT/'candidate.wav'),
              'rngBeforeSpeechSha256':hashlib.sha256(before_speech_rng).hexdigest(),
              'rngAfterSpeechSha256':hashlib.sha256(after_speech_rng).hexdigest(),
              'parameterVerificationComplete':verification.get('complete',False),
              'baselineAudioEqualityTested':False, 'humanListeningApproval':False,
              'rngContinuityScope':'Checkpoint loads and assignment verified unchanged; normal constructor order preserved. No separate full baseline runtime comparison yet.'}
    save_json(OUT/'child-result.json', result)
    print(json.dumps({'phase':'generated','audioSeconds':result['audioSeconds']}), flush=True)


class ProcessSamples:
    """Read-only native process handles retained through exit for OS peak counters."""
    def __init__(self, root_pid):
        import memory_reclaim_api as api
        self.api, self.root_pid, self.handles = api, root_pid, {}
        self.kernel = api.kernel
        class Entry(ctypes.Structure):
            _fields_=[('dwSize',wintypes.DWORD),('cntUsage',wintypes.DWORD),('pid',wintypes.DWORD),
                ('heap',ctypes.c_size_t),('module',wintypes.DWORD),('threads',wintypes.DWORD),
                ('parent',wintypes.DWORD),('priority',wintypes.LONG),('flags',wintypes.DWORD),('name',wintypes.WCHAR*260)]
        self.Entry=Entry
        self.kernel.CreateToolhelp32Snapshot.argtypes=[wintypes.DWORD,wintypes.DWORD]
        self.kernel.CreateToolhelp32Snapshot.restype=wintypes.HANDLE
        self.kernel.Process32FirstW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)]
        self.kernel.Process32NextW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)]
    def sample(self):
        snapshot=self.kernel.CreateToolhelp32Snapshot(2,0);entry=self.Entry();entry.dwSize=ctypes.sizeof(entry);inventory={}
        try:
            ok=self.kernel.Process32FirstW(snapshot,ctypes.byref(entry))
            while ok:
                inventory[entry.pid]=(entry.parent,entry.name)
                ok=self.kernel.Process32NextW(snapshot,ctypes.byref(entry))
        finally:self.kernel.CloseHandle(snapshot)
        owned={self.root_pid}
        while True:
            expanded=owned|{pid for pid,(parent,_) in inventory.items() if parent in owned}
            if expanded==owned:break
            owned=expanded
        for pid in owned:
            if pid not in self.handles and pid in inventory:
                handle=self.kernel.OpenProcess(0x1000|0x10,False,pid)
                if handle:self.handles[pid]=(handle,inventory[pid][1])
        rows=[]
        for pid,(handle,name) in self.handles.items():
            value=self.api.Counters();value.cb=ctypes.sizeof(value)
            if self.api.psapi.GetProcessMemoryInfo(handle,ctypes.byref(value),value.cb):
                rows.append({'pid':pid,'name':name,'workingMiB':round(value.working/2**20,3),
                    'privateCommittedMiB':round(value.private/2**20,3),'peakWorkingMiB':round(value.peakWorking/2**20,3),
                    'peakCommitMiB':round(value.peakPagefile/2**20,3)})
        return rows
    def close(self):
        for handle,_ in self.handles.values():self.kernel.CloseHandle(handle)


def parent(timeout):
    import memory_reclaim_api as memory
    sys.path.insert(0,str(ROOT))
    from server import OwnedProcessTree  # Import-safe; no HTTP server/model is started.
    if OUT.exists():
        raise RuntimeError('Refusing to overwrite a prior candidate experiment. Review and archive it deliberately.')
    OUT.mkdir(parents=True)
    report={'status':'preflight','physicalAbortFloorGiB':PHYSICAL_FLOOR,'commitAbortFloorGiB':COMMIT_FLOOR,
            'preflightPhysicalGiB':PREFLIGHT_PHYSICAL,'preflightCommitGiB':PREFLIGHT_COMMIT,
            'maximumSeconds':timeout,'productionDefaultsChanged':False,'publicRequests':False,
            'monitorIntervalSeconds':.1,'samplesEverySeconds':.25,'before':memory.memory()}
    def save():save_json(OUT/'parent-receipt.json',report)
    save()
    with urllib.request.urlopen('http://127.0.0.1:8769/api/health',timeout=3) as response:health=json.load(response)
    if health.get('activeJobs') or health.get('queued'):
        report['status']='not_started_original_busy';save();return
    if report['before']['availableGiB'] < PREFLIGHT_PHYSICAL or report['before']['commitCapacityAvailableGiB'] < PREFLIGHT_COMMIT:
        report['status']='not_started_resource_preflight';save();return
    process=tree=sampler=None
    health_stop, health_busy, health_failed = threading.Event(), threading.Event(), threading.Event()
    def watch_original():
        while not health_stop.is_set():
            try:
                with urllib.request.urlopen('http://127.0.0.1:8769/api/health',timeout=1) as response:state=json.load(response)
                if state.get('activeJobs') or state.get('queued'):
                    health_busy.set();return
            except Exception:
                health_failed.set();return
            health_stop.wait(1)
    health_thread=threading.Thread(target=watch_original,daemon=True,name='candidate-original-idle-check')
    health_thread.start()
    started=time.monotonic();last_sample=0.;report['minimumPhysicalGiB']=report['before']['availableGiB']
    report['minimumCommitGiB']=report['before']['commitCapacityAvailableGiB']
    try:
        with (OUT/'child.stdout.log').open('wb') as stdout, (OUT/'child.stderr.log').open('wb') as stderr, (OUT/'memory.jsonl').open('w') as log:
            env={**os.environ,'PYTHONIOENCODING':'utf-8','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
            process=subprocess.Popen([str(VOICE_PYTHON),str(Path(__file__).resolve()),'--child'],cwd=ROOT,
                stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,env=env,creationflags=0x08000000|0x4)
            try:tree=OwnedProcessTree(process)
            except Exception:
                process.kill();process.wait(timeout=10);raise
            sampler=ProcessSamples(process.pid);report.update(status='running',ownedLauncherPid=process.pid);save()
            while process.poll() is None:
                elapsed=time.monotonic()-started;state=memory.memory()
                report['minimumPhysicalGiB']=min(report['minimumPhysicalGiB'],state['availableGiB'])
                report['minimumCommitGiB']=min(report['minimumCommitGiB'],state['commitCapacityAvailableGiB'])
                if state['availableGiB'] <= PHYSICAL_FLOOR or state['commitCapacityAvailableGiB'] <= COMMIT_FLOOR:
                    report.update(status='cancelled_resource_floor',abortAtSeconds=round(elapsed,3),abortMemory=state)
                    tree.terminate();break
                if elapsed>=timeout or (OUT/'cancel').exists():
                    report.update(status='cancelled_deadline_or_requested',abortAtSeconds=round(elapsed,3));tree.terminate();break
                if health_busy.is_set() or health_failed.is_set():
                    report['status']='cancelled_original_became_busy' if health_busy.is_set() else 'cancelled_original_health_unknown'
                    tree.terminate();break
                if elapsed-last_sample>=.25:
                    rows=sampler.sample();log.write(json.dumps({'elapsed':round(elapsed,3),**state,'processes':rows})+'\n');log.flush()
                    last_sample=elapsed
                time.sleep(.1)
            process.wait(timeout=10)
            report['processPeaks']=sampler.sample();report['childExitCode']=process.returncode
            if report['status']=='running':report['status']='completed' if process.returncode==0 and (OUT/'child-result.json').exists() else 'child_failed'
    except BaseException as error:
        report.update(status='parent_error',errorType=type(error).__name__)
        raise
    finally:
        if tree:tree.close()
        if process and process.poll() is None:process.wait(timeout=10)
        if sampler:sampler.close()
        health_stop.set();health_thread.join(timeout=2)
        report.update(elapsedSeconds=round(time.monotonic()-started,3),after=memory.memory());save()
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',action='store_true')
    parser.add_argument('--child',action='store_true',help=argparse.SUPPRESS)
    parser.add_argument('--timeout',type=int,default=420)
    args=parser.parse_args()
    if not 60<=args.timeout<=420:parser.error('Timeout must be60 to420 seconds.')
    if args.child:child()
    elif args.go:parent(args.timeout)
    else:print(json.dumps({'preparedOnly':True,'modelsLoaded':False,'physicalAbortFloorGiB':PHYSICAL_FLOOR,
                          'commitAbortFloorGiB':COMMIT_FLOOR,'preflightPhysicalGiB':PREFLIGHT_PHYSICAL,
                          'preflightCommitGiB':PREFLIGHT_COMMIT,'sentence':"I'm a fictional, computer-made guide."}))
