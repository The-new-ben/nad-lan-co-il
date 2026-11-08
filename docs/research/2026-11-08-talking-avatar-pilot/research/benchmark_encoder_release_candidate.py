"""Prepared single-sentence encoder-release experiment. Only --go launches it."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
import wave

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT/'.runtime/chatterbox-onnx-test'
VOICE_PYTHON = Path('C:/Users/777/nad-lan/voice-rig/venv/Scripts/python.exe')
REFERENCE = ROOT.parent/'kit/ref-female.wav'
REFERENCE_SHA = 'bf0e02b74ba5fe4193c1496566ce8782724b18d4d12de63442813468c6ad2efd'
SAVED_AUDIO = ROOT/'evidence/chatterbox-onnx-q4/warm-next-question.wav'
SAVED_AUDIO_SHA = '836fd0691cc9130c1f6f167db88560dd6f717b9f8d63d2358c1926a766b3dce9'
TEXT = 'What city and budget do you have in mind?'
PREFLIGHT_PHYSICAL, PREFLIGHT_COMMIT = 1.8, 2.2
ABORT_PHYSICAL, ABORT_COMMIT = .75, 1.0
POLL_SECONDS, INFERENCE_SECONDS, TOTAL_SECONDS = .1, 120, 180


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for data in iter(lambda:stream.read(1024*1024), b''):
            h.update(data)
    return h.hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')


def pcm_receipt(path):
    with wave.open(str(path), 'rb') as wav:
        params = {'channels':wav.getnchannels(), 'sampleRate':wav.getframerate(),
                  'sampleWidth':wav.getsampwidth(), 'frames':wav.getnframes()}
        data = wav.readframes(wav.getnframes())
    return {**params, 'pcmSha256':hashlib.sha256(data).hexdigest(), 'fileSha256':sha256(path)}


def child(out):
    def blocked(*args, **kwargs):
        raise RuntimeError('Network is disabled in this isolated voice experiment.')
    socket.socket.connect = socket.socket.connect_ex = socket.create_connection = blocked
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_HUB_DISABLE_TELEMETRY='1',
                      TOKENIZERS_PARALLELISM='false', OMP_NUM_THREADS='4', MKL_NUM_THREADS='4')
    import memory_reclaim_api as memory
    from onnx_encoder_release_candidate import EncoderReleasedVoice
    started = time.monotonic()
    def event(value):
        value = {**value, 'machineMemory':memory.memory()}
        print(json.dumps(value), flush=True)
        with (out/'phases.jsonl').open('a', encoding='utf-8') as log:
            log.write(json.dumps(value)+'\n')
    engine = EncoderReleasedVoice(model_dir=MODEL_DIR, runtime_path=MODEL_DIR/'ort-1.31.1',
                                 threads=4, reference=REFERENCE, evidence_dir=out, phase_callback=event)
    loaded = time.monotonic()
    samples, sr, metadata = engine.generate(TEXT)
    engine.event('generated_with_original_watermark')
    import soundfile as sf
    engine.np.save(out/'watermarked-float.npy', samples)
    sf.write(out/'candidate.wav', samples, sr, subtype='PCM_16')
    actual, prior = pcm_receipt(out/'candidate.wav'), pcm_receipt(SAVED_AUDIO)
    exact = all(actual[key] == prior[key] for key in ('channels','sampleRate','sampleWidth','frames','pcmSha256'))
    result = {'status':'generated', 'text':TEXT, 'metadata':metadata,
              'initializationSeconds':round(loaded-started,3),
              'wholeChildSeconds':round(time.monotonic()-started,3),
              'candidatePCM':actual, 'savedApprovedPCM':prior, 'savedPCMExactlyEqual':exact,
              'comparisonScope':'Saved same-text warm PCM16; historical cold/warm state differs. No concurrent or new baseline generation.',
              'intermediateBaselineAvailable':False, 'intermediateEqualityClaimed':False,
              'instrumentation':engine.instrumentation(), 'newHumanListeningApproval':False,
              'publicOrDefaultChange':False, 'providerCharge':0}
    save(out/'child-result.json', result)
    print(json.dumps({'phase':'finished', 'savedPCMExactlyEqual':exact}), flush=True)


def parent(label):
    import memory_reclaim_api as memory
    from benchmark_mtl_loader_candidate import ProcessSamples
    from benchmark_qwen_q4_candidate import OriginalHealth, alive_handles
    sys.path.insert(0, str(ROOT))
    from server import OwnedProcessTree
    started = time.monotonic()
    deadline = started + TOTAL_SECONDS
    out = ROOT/'evidence/chatterbox-encoder-release'/label
    if out.exists():
        raise RuntimeError('Refusing to overwrite an earlier experiment.')
    out.mkdir(parents=True)
    report = {'status':'preflight', 'text':TEXT, 'before':memory.memory(),
              'preflightPhysicalGiB':PREFLIGHT_PHYSICAL, 'preflightCommitGiB':PREFLIGHT_COMMIT,
              'physicalAbortFloorGiB':ABORT_PHYSICAL, 'commitAbortFloorGiB':ABORT_COMMIT,
              'guardBasis':'Provisional short-sentence-only estimate, not a measured encoder-release requirement.',
              'inferenceTimeoutSeconds':INFERENCE_SECONDS, 'totalTimeoutSeconds':TOTAL_SECONDS,
              'pollSeconds':POLL_SECONDS, 'publicOrDefaultChange':False,
              'ownerApplicationsClosed':False, 'inferenceStarted':False}
    report['minimumPhysicalGiB'] = report['before']['availableGiB']
    report['minimumCommitGiB'] = report['before']['commitCapacityAvailableGiB']
    process = tree = sampler = health = None
    manifest = []
    try:
        save(out/'parent-receipt.json',report)
        state = report['before']
        if state['availableGiB'] < PREFLIGHT_PHYSICAL or state['commitCapacityAvailableGiB'] < PREFLIGHT_COMMIT:
            report['status'] = 'not_started_resource_preflight'
            return
        if sha256(REFERENCE) != REFERENCE_SHA or sha256(SAVED_AUDIO) != SAVED_AUDIO_SHA:
            raise RuntimeError('Reviewed reference or comparison audio changed.')
        provenance = json.loads((MODEL_DIR/'download-receipt.json').read_text(encoding='utf-8'))
        if provenance['revision'] != 'd21799bd0354adb85e348b8a0442a8405110a2cf':
            raise RuntimeError('Reviewed model provenance changed.')
        paths = [Path(__file__),Path(__file__).with_name('onnx_encoder_release_candidate.py'),
                 Path(__file__).with_name('benchmark_qwen_q4_candidate.py'),
                 Path(__file__).with_name('benchmark_mtl_loader_candidate.py'),
                 Path(__file__).with_name('memory_reclaim_api.py'), ROOT/'server.py',
                 MODEL_DIR/'onnx_engine.py', MODEL_DIR/'download-receipt.json', REFERENCE, SAVED_AUDIO]
        for item in provenance['files']:
            path = MODEL_DIR/item['path']
            if path.stat().st_size != item['bytes'] or sha256(path) != item['sha256']:
                raise RuntimeError('A pinned model artifact changed: '+path.name)
            paths.append(path)
        for path in dict.fromkeys(paths):
            manifest.append({'path':str(path),'bytes':path.stat().st_size,
                             'modifiedNs':path.stat().st_mtime_ns,'sha256':sha256(path)})
        save(out/'source-manifest.json',{'files':manifest, 'modelRevision':provenance['revision']})
        health = OriginalHealth()
        health.start()
        state = memory.memory()
        if health.reason:
            report['status'] = 'not_started_'+health.reason
            return
        if state['availableGiB'] < PREFLIGHT_PHYSICAL or state['commitCapacityAvailableGiB'] < PREFLIGHT_COMMIT:
            report.update(status='not_started_resource_preflight', beforeLaunch=state)
            return
        if (out/'cancel').exists() or time.monotonic() >= deadline-5:
            report['status'] = 'not_started_cancel_or_deadline'
            return
        report.update(status='running', beforeLaunch=state)
        with (out/'stdout.txt').open('wb') as stdout, (out/'stderr.txt').open('wb') as stderr, (out/'memory.jsonl').open('w',encoding='utf-8') as log:
            env = {**os.environ,'PYTHONIOENCODING':'utf-8','HF_HUB_OFFLINE':'1',
                   'TRANSFORMERS_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1',
                   'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','TOKENIZERS_PARALLELISM':'false'}
            process = subprocess.Popen([str(VOICE_PYTHON),str(Path(__file__).resolve()),'--child','--label',label],
                cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                creationflags=0x08000000|0x4)
            try:
                tree = OwnedProcessTree(process)
            except BaseException:
                process.kill()
                process.wait(timeout=1)
                raise
            sampler = ProcessSamples(process.pid)
            report.update(inferenceStarted=True, ownedLauncherPid=process.pid)
            save(out/'parent-receipt.json',report)
            stop_at = min(time.monotonic()+INFERENCE_SECONDS,deadline)-5
            while process.poll() is None:
                tick = time.monotonic()
                state = memory.memory()
                report['minimumPhysicalGiB'] = min(report['minimumPhysicalGiB'],state['availableGiB'])
                report['minimumCommitGiB'] = min(report['minimumCommitGiB'],state['commitCapacityAvailableGiB'])
                reason = ('resource_floor' if state['availableGiB'] <= ABORT_PHYSICAL or state['commitCapacityAvailableGiB'] <= ABORT_COMMIT else
                          'deadline' if tick >= stop_at else 'requested' if (out/'cancel').exists() else health.reason)
                if reason:
                    report.update(status='cancelled_'+reason,abortMemory=state)
                    tree.terminate()
                    break
                rows = sampler.sample()
                if not rows:
                    report['status'] = 'cancelled_process_memory_unavailable'
                    tree.terminate()
                    break
                log.write(json.dumps({'elapsedSeconds':round(tick-started,3),**state,'processes':rows})+'\n')
                log.flush()
                time.sleep(max(0,POLL_SECONDS-(time.monotonic()-tick)))
            process.wait(timeout=1)
            report['exitCode'] = process.returncode
            if report['status'] == 'running':
                report['status'] = 'generated_review_pending' if process.returncode == 0 else 'child_failed'
        for item in manifest:
            path = Path(item['path'])
            if path.stat().st_size != item['bytes'] or path.stat().st_mtime_ns != item['modifiedNs']:
                raise RuntimeError('An experiment source changed.')
            if item['bytes'] < 5*1024*1024 and sha256(path) != item['sha256']:
                raise RuntimeError('A small experiment input hash changed.')
    except BaseException as exc:
        report.update(status='harness_error',errorType=type(exc).__name__,error=str(exc))
        raise
    finally:
        if tree:
            tree.close()
        try:
            if process and process.poll() is None:
                process.wait(timeout=1)
            if sampler:
                report['processPeaks'] = sampler.sample()
                alive = alive_handles(sampler)
                until = time.monotonic()+1
                while alive and time.monotonic() < until:
                    time.sleep(.05)
                    alive = alive_handles(sampler)
                report['ownedProcessesStopped'] = not alive
                report['remainingObservedOwnedPids'] = alive
                report['peakWorkingMiB'] = max((v['peakWorkingMiB'] for v in report['processPeaks']),default=None)
                report['peakCommitMiB'] = max((v['peakCommitMiB'] for v in report['processPeaks']),default=None)
        except BaseException as exc:
            report.update(cleanupVerified=False,cleanupErrorType=type(exc).__name__)
        finally:
            if sampler:
                sampler.close()
            if health:
                health.close()
            report.update(after=memory.memory(),wallSeconds=round(time.monotonic()-started,3))
            save(out/'parent-receipt.json',report)
            print(json.dumps({'receipt':str(out/'parent-receipt.json'),'status':report['status']}),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',action='store_true')
    parser.add_argument('--child',action='store_true',help=argparse.SUPPRESS)
    parser.add_argument('--label',default='short-01')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',args.label):
        parser.error('Use a short lowercase label.')
    if args.child:
        child(ROOT/'evidence/chatterbox-encoder-release'/args.label)
    elif args.go:
        parent(args.label)
    else:
        print(json.dumps({'preparedOnly':True,'inferenceStarted':False,'text':TEXT,
              'preflightPhysicalGiB':PREFLIGHT_PHYSICAL,'preflightCommitGiB':PREFLIGHT_COMMIT,
              'physicalAbortFloorGiB':ABORT_PHYSICAL,'commitAbortFloorGiB':ABORT_COMMIT,
              'changes':'reference encoder lifetime only; separate candidate; no runtime/arena/watermark change'}))
