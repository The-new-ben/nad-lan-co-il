"""Bounded Q4 Vulkan experiment. GPU acceleration and pinned Q4 quantization; historical CPU comparisons only. Only --go may start inference."""
from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / '.runtime/brain-q4-candidate'
MODEL = ROOT / '.runtime/brain-q4-candidate/Qwen3-1.7B-Q4_K_M.gguf'
VULKAN = ROOT / '.runtime/llama-vulkan-b12189/llama-completion.exe'
MODEL_BYTES = 1282439264
MODEL_SHA256 = 'd2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5'
CASE_IDS = ('buyer_checks', 'remote_limits', 'unknown_price', 'unknown_address',
            'identity', 'broker_actions', 'guaranteed_return', 'injected_role')
PREFLIGHT_PHYSICAL, PREFLIGHT_COMMIT = 1.6, 2.0
# Isolated GPU admission experiment only; runtime abort floors remain unchanged.
# No public-resource threshold is inferred from these provisional entry gates.
ABORT_PHYSICAL, ABORT_COMMIT = .75, 1.0
CASE_SECONDS, TOTAL_SECONDS = 90, 600
POLL_SECONDS = .1
CLEANUP_RESERVE_SECONDS = 5


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def file_record(path):
    path = Path(path)
    return {'path': str(path), 'bytes': path.stat().st_size,
            'modifiedNs': path.stat().st_mtime_ns, 'sha256': sha256(path)}


def unchanged(records):
    for record in records:
        path = Path(record['path'])
        if path.stat().st_size != record['bytes'] or path.stat().st_mtime_ns != record['modifiedNs']:
            raise RuntimeError('A reviewed input changed: ' + path.name)
        # Full model hash is checked once before any launch; only size/mtime thereafter.
        if path != MODEL and sha256(path) != record['sha256']:
            raise RuntimeError('A reviewed input hash changed: ' + path.name)


class OriginalHealth:
    """Loopback health runs separately, never blocking the memory polling loop."""
    def __init__(self):
        self.stop = threading.Event()
        self.ready = threading.Event()
        self.reason = None
        self.last_checked = None
        self.thread = threading.Thread(target=self.watch, daemon=True, name='q4-original-idle-check')

    def watch(self):
        while not self.stop.is_set():
            try:
                with urllib.request.urlopen('http://127.0.0.1:8769/api/health', timeout=1) as response:
                    health = json.load(response)
                if not isinstance(health, dict) or 'activeJobs' not in health or 'queued' not in health:
                    raise RuntimeError('Incomplete local health response.')
                if health['activeJobs'] or health['queued']:
                    self.reason = 'original_became_busy'
            except Exception:
                self.reason = 'original_health_unknown'
            self.last_checked = time.monotonic()
            self.ready.set()
            if self.reason:
                return
            self.stop.wait(.5)

    def start(self):
        self.thread.start()
        if not self.ready.wait(2):
            self.reason = 'original_health_unknown'

    def close(self):
        self.stop.set()
        self.thread.join(timeout=2)


def alive_handles(sampler):
    alive = []
    for pid, (handle, _) in sampler.handles.items():
        code = wintypes.DWORD()
        if not sampler.kernel.GetExitCodeProcess(handle, ctypes.byref(code)):
            raise RuntimeError('Could not verify owned-process exit.')
        if code.value == 259:
            alive.append(pid)
    return alive


def style_observations(answer):
    sentences = re.findall(r'[^.!?]+[.!?]+', answer)
    return {'englishCharacters': not bool(re.search(r'[\u0590-\u05ff\u0600-\u06ff\u4e00-\u9fff]', answer)),
            'twoSentences': len(sentences) == 2, 'endsWithQuestion': answer.endswith('?'),
            'words': len(answer.split()), 'within25to35WordTarget': 25 <= len(answer.split()) <= 35,
            'contentReviewPending': True}


def run_case(case, folder, brain, memory, ProcessSamples, OwnedProcessTree, health, total_deadline, records):
    started = time.monotonic()
    case_deadline = min(started + CASE_SECONDS, total_deadline)
    stop_inference_at = case_deadline - CLEANUP_RESERVE_SECONDS
    folder.mkdir()
    prompt = folder / 'prompt.txt'
    passages = brain.build_prompt(case['question'], [], prompt, concise_first=False)
    prompt_hash = hashlib.sha256(prompt.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
    if prompt_hash != case['preparedPrompt']['normalizedTextSha256']:
        raise RuntimeError('Current prompt differs from the reviewed validation plan.')
    original_command = brain.command(prompt)
    command = list(original_command)
    if command.count('-m') != 1 or command[command.index('-m') + 1] != str(brain.MODEL):
        raise RuntimeError('The original model argument is unexpected.')
    command[command.index('-m') + 1] = str(MODEL)
    command[0] = str(VULKAN)
    command[command.index('-ngl') + 1] = '99'
    command[command.index('--log-verbosity') + 1] = '3'
    command += ['--device', 'Vulkan0']
    if '--offline' not in command or any(value.startswith(('http:', 'https:')) for value in command):
        raise RuntimeError('The candidate must remain a local offline CLI command.')
    unchanged(records)
    before = memory.memory()
    result = {'id': case['id'], 'question': case['question'], 'history': [], 'processWarm': False,
              'expectedBehavior': case['expectedBehavior'], 'priorQ8': case['priorQ8'],
              'promptSha256': prompt_hash, 'promptFileSha256': sha256(prompt), 'retrievedGuide': passages,
              'originalCommand': original_command, 'command': command, 'modelPathOnlyChanged': False, 'sameQ8Model': False, 'requestedRuntimeBackend': 'Vulkan0', 'requestedGpuLayers': 99,
              'contentReviewPending': True, 'before': before, 'status': 'preflight',
              'minimumPhysicalGiB': before['availableGiB'],
              'minimumCommitGiB': before['commitCapacityAvailableGiB']}
    target = folder / 'result.json'
    save(target, result)
    if (folder.parent/'cancel').exists():
        result['status'] = 'not_started_requested'
        save(target, result)
        return result
    if health.reason:
        result['status'] = 'not_started_' + health.reason
        save(target, result)
        return result
    if before['availableGiB'] < PREFLIGHT_PHYSICAL or before['commitCapacityAvailableGiB'] < PREFLIGHT_COMMIT:
        result['status'] = 'not_started_resource_preflight'
        save(target, result)
        return result
    if time.monotonic() >= stop_inference_at:
        result['status'] = 'not_started_total_deadline'
        save(target, result)
        return result
    child = tree = sampler = None
    result.update(status='running', startedAtUTC=utc())
    save(target, result)
    try:
        with (folder/'stdout.txt').open('wb') as stdout, (folder/'stderr.txt').open('wb') as stderr, (folder/'memory.jsonl').open('w', encoding='utf-8') as log:
            env = {**os.environ, 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
                   'HF_HUB_DISABLE_TELEMETRY': '1', 'PYTHONIOENCODING': 'utf-8'}
            # CLI only: no server/listener or HTTP client is launched in the inference child.
            child = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=0x08000000 | 0x4)
            try:
                tree = OwnedProcessTree(child)  # Assign suspended child, then resume.
            except BaseException:
                child.kill()
                child.wait(timeout=1)
                raise
            sampler = ProcessSamples(child.pid)
            result['ownedPid'] = child.pid
            result['modelInferenceStarted'] = True
            save(target, result)
            while child.poll() is None:
                loop_start = time.monotonic()
                state = memory.memory()
                result['minimumPhysicalGiB'] = min(result['minimumPhysicalGiB'], state['availableGiB'])
                result['minimumCommitGiB'] = min(result['minimumCommitGiB'], state['commitCapacityAvailableGiB'])
                reason = None
                if state['availableGiB'] <= ABORT_PHYSICAL or state['commitCapacityAvailableGiB'] <= ABORT_COMMIT:
                    reason = 'resource_floor'
                elif loop_start >= stop_inference_at:
                    reason = 'total_deadline' if case_deadline == total_deadline else 'case_deadline'
                elif (folder.parent/'cancel').exists():
                    reason = 'requested'
                elif health.reason:
                    reason = health.reason
                if reason:
                    result.update(status='cancelled_'+reason, abortMemory=state, abortAtSeconds=round(loop_start-started, 3))
                    tree.terminate()
                    break
                rows = sampler.sample()
                log.write(json.dumps({'elapsedSeconds': round(loop_start-started, 3), **state, 'processes': rows}) + '\n')
                log.flush()
                time.sleep(max(0, POLL_SECONDS - (time.monotonic()-loop_start)))
            child.wait(timeout=1)
            result['childExitCode'] = child.returncode
            if result['status'] == 'running':
                result['status'] = 'generated' if child.returncode == 0 else 'child_failed'
    except BaseException as error:
        result.update(status='harness_error', errorType=type(error).__name__)
        raise
    finally:
        # Closing the containing job kills only this benchmark's owned descendants.
        if tree:
            tree.close()
        if child and child.poll() is None:
            child.wait(timeout=1)
        if sampler:
            try:
                result['processPeaks'] = sampler.sample()
                deadline = time.monotonic() + 1
                alive = alive_handles(sampler)
                while alive and time.monotonic() < deadline:
                    time.sleep(.05)
                    alive = alive_handles(sampler)
                result['ownedProcessesStopped'] = not alive
                result['remainingObservedOwnedPids'] = alive
                result['peakWorkingMiB'] = max((v['peakWorkingMiB'] for v in result['processPeaks']), default=None)
                result['peakCommitMiB'] = max((v['peakCommitMiB'] for v in result['processPeaks']), default=None)
            finally:
                sampler.close()
        result.update(wallSeconds=round(time.monotonic()-started, 3), completedAtUTC=utc())
        save(target, result)
    unchanged(records)
    raw = (folder/'stdout.txt').read_text(encoding='utf-8', errors='replace')
    diagnostic = (folder/'stderr.txt').read_text(encoding='utf8',errors='replace')
    gpu_lines = [line for line in diagnostic.splitlines() if re.search(r'offload|Vulkan.*buffer|Vulkan0',line,re.I)]
    offloaded = re.search(r'offloaded\s+(\d+)/(\d+)\s+layers',diagnostic,re.I)
    result['gpuExecutionEvidence'] = {'lines':gpu_lines,'offloadedLayers':int(offloaded.group(1)) if offloaded else None,'totalLayers':int(offloaded.group(2)) if offloaded else None,'observed':bool(offloaded and int(offloaded.group(1))>0 and any('vulkan' in line.lower() and 'buffer' in line.lower() for line in gpu_lines))}
    result['rawOutput'] = raw
    result['cleanedOutput'] = None
    result['validationError'] = None
    if result['status'] == 'generated':
        try:
            result['cleanedOutput'] = brain.clean_answer(raw)
            result['styleObservations'] = style_observations(result['cleanedOutput'])
        except RuntimeError as error:
            result['validationError'] = str(error)
            result['status'] = 'generated_validator_rejected'
    save(target, result)
    return result


def run(label):
    started = time.monotonic()
    total_deadline = started + TOTAL_SECONDS
    out = ROOT / 'evidence/latency/llm' / label
    if out.exists():
        raise RuntimeError('Refusing to overwrite an existing benchmark receipt.')
    out.mkdir(parents=True)
    report = {'startedAtUTC': utc(), 'status': 'preflight', 'candidate': str(MODEL), 'backend': 'Vulkan0', 'runtime': str(VULKAN), 'cases': [],
              'preflightPhysicalGiB': PREFLIGHT_PHYSICAL, 'preflightCommitGiB': PREFLIGHT_COMMIT,
              'abortPhysicalGiB': ABORT_PHYSICAL, 'abortCommitGiB': ABORT_COMMIT,
              'pollIntervalSeconds': POLL_SECONDS, 'perCaseDeadlineSeconds': CASE_SECONDS,
              'totalDeadlineSeconds': TOTAL_SECONDS, 'contentReviewPending': True,
              'cleanupReserveSeconds': CLEANUP_RESERVE_SECONDS,
              'coldDefinition': 'Fresh CLI process per case; operating-system file cache is not flushed.',
              'timingScope': 'Whole CLI process including model load and cleanup; not warm inference.',
              'networkScope': 'Inference child is offline local llama-completion, with no server/listener. Only parent health thread requests loopback8769. No OS firewall isolation claimed.',
              'newQ4Inference': False, 'quantizationChanged': True, 'entryThresholdsExperimentalOnly': True, 'modelDefaultChanged': False, 'packagesInstalled': False,
              'publicRequests': False, 'ownerApplicationsClosed': False}
    result_path = out/'results.json'
    save(result_path, report)
    health = None
    try:
        plan_path, provenance_path = CANDIDATE/'validation-plan.json', CANDIDATE/'provenance.json'
        plan = json.loads(plan_path.read_text(encoding='utf-8'))
        provenance = json.loads(provenance_path.read_text(encoding='utf-8'))
        if tuple(case['id'] for case in plan['cases']) != CASE_IDS:
            raise RuntimeError('The reviewed eight-case plan changed.')
        if provenance['sha256'] != MODEL_SHA256 or provenance['bytes'] != MODEL_BYTES or provenance.get('status') not in ('verified','verified_existing'):
            raise RuntimeError('The candidate provenance is not the verified pinned file.')
        if MODEL.stat().st_size != MODEL_BYTES or sha256(MODEL) != MODEL_SHA256:
            raise RuntimeError('The isolated model failed its pinned size/hash check.')
        for item in plan['sourceFiles']:
            if sha256(item['path']) != item['sha256']:
                raise RuntimeError('A source changed since preparation: ' + Path(item['path']).name)
        sys.path.insert(0, str(ROOT))
        import brain
        import memory_reclaim_api as memory
        from benchmark_mtl_loader_candidate import ProcessSamples
        from server import OwnedProcessTree
        runtime_provenance = json.loads((ROOT/'research/primary/vulkan-candidate.json').read_text(encoding='utf8'))
        if runtime_provenance['sha256'] != '9d56405579492423833cdde94cf46cae15d38333f585f3957cafebfc6fb0e182':
            raise RuntimeError('Unexpected official runtime provenance.')
        if sha256(VULKAN.parent/'release.zip') != runtime_provenance['sha256']:
            raise RuntimeError('Portable runtime archive hash mismatch.')
        source_paths = [Path(__file__), ROOT/'brain.py', ROOT/'source-page.html', ROOT/'server.py',
                        Path(__file__).with_name('benchmark_mtl_loader_candidate.py'),
                        Path(__file__).with_name('memory_reclaim_api.py'), plan_path, provenance_path,
                        Path(brain.LLAMA), MODEL, VULKAN, ROOT/'research/primary/vulkan-candidate.json']
        source_paths += list(VULKAN.parent.glob('*.dll'))
        records = [file_record(path) for path in source_paths]
        save(out/'source-manifest.json', {'files': records, 'modelProvenance': provenance,
             'reviewedSettings': plan['unchangedSettings'], 'priorQ8Comparisons': 'Historical CPU only; current Q4 Vulkan, no paired current CPU speed claim.'})
        report['before'] = memory.memory()
        device = subprocess.run([str(VULKAN),'--list-devices'],capture_output=True,text=True,timeout=15,creationflags=0x08000000)
        device_text=device.stdout+device.stderr
        device_free = re.search(r'Vulkan0:.*?([0-9]+) MiB free',device_text)
        if device.returncode or not device_free or int(device_free.group(1)) < 3072:
            raise RuntimeError('Insufficient verified Vulkan device memory for experiment.')
        report['deviceQuery']=device_text
        report['minimumDeviceFreeMiB']=3072
        health = OriginalHealth()
        health.start()
        report['status'] = 'running'
        save(result_path, report)
        for case in plan['cases']:
            result = run_case(case, out/case['id'], brain, memory, ProcessSamples, OwnedProcessTree,
                              health, total_deadline, records)
            report['cases'].append(result)
            report['newQ4Inference'] = report['newQ4Inference'] or result.get('modelInferenceStarted', False)
            save(result_path, report)
            print(json.dumps({'case': case['id'], 'status': result['status'],
                              'seconds': result.get('wallSeconds'), 'contentReviewPending': True}), flush=True)
            if result['status'] not in ('generated', 'generated_validator_rejected') or not result.get('ownedProcessesStopped', False):
                report['status'] = 'stopped_' + result['status']
                break
        else:
            report['status'] = 'eight_cases_finished_content_review_pending'
        report['after'] = memory.memory()
        report['minimumPhysicalGiB'] = min((c['minimumPhysicalGiB'] for c in report['cases']), default=None)
        report['minimumCommitGiB'] = min((c['minimumCommitGiB'] for c in report['cases']), default=None)
        report['peakWorkingMiB'] = max((c.get('peakWorkingMiB') or 0 for c in report['cases']), default=0)
        report['peakCommitMiB'] = max((c.get('peakCommitMiB') or 0 for c in report['cases']), default=0)
        unchanged(records)
    except BaseException as error:
        report.update(status='harness_error', errorType=type(error).__name__, error=str(error))
        raise
    finally:
        if health:
            health.close()
        report.update(completedAtUTC=utc(), wallSeconds=round(time.monotonic()-started, 3))
        save(result_path, report)
    print(json.dumps({'receipt': str(result_path), 'status': report['status'], 'contentReviewPending': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go', action='store_true')
    parser.add_argument('--label', default='q4-vulkan-eight-01')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', args.label):
        parser.error('Use a short lowercase label with letters, numbers, hyphens or underscores.')
    if args.go:
        run(args.label)
    else:
        print(json.dumps({'preparedOnly': True, 'inferenceStarted': False, 'cases': 8,
              'preflightPhysicalGiB': PREFLIGHT_PHYSICAL, 'preflightCommitGiB': PREFLIGHT_COMMIT,
              'abortPhysicalGiB': ABORT_PHYSICAL, 'abortCommitGiB': ABORT_COMMIT,
              'perCaseDeadlineSeconds': CASE_SECONDS, 'totalDeadlineSeconds': TOTAL_SECONDS}))
