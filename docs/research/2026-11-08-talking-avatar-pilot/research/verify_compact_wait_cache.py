"""No-model tests of bounded admission and exact completed streaming cache."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import threading
import time
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server

SOURCE = ROOT/'evidence/local-compact-conversation/identity-02'
SAVED = json.loads((SOURCE/'receipt.json').read_text(encoding='utf-8'))
ANSWER = SAVED['answer']
OUT = ROOT/'evidence/compact-wait-cache-controls/final'
OUT.mkdir(parents=True, exist_ok=True)
checks = []


def check(name, passed): checks.append({'name': name, 'passed': bool(passed)})


def job():
    identity = uuid.uuid4().hex
    folder = OUT/identity; folder.mkdir()
    return {'id': identity, 'session': identity, 'text': 'Who are you, and how can you help me?',
            'folder': folder, 'phase': 'queued', 'created': time.time(), 'cancel': threading.Event(),
            'process': None, 'activePid': None, 'timings': {}}


class Clock:
    def __init__(self): self.now, self.waits, self.cancel_at, self.cancelled = 0, [], None, False
    def monotonic(self): return self.now
    def is_set(self): return self.cancelled
    def wait(self, seconds):
        self.waits.append(seconds); self.now += seconds
        if self.cancel_at is not None and self.now >= self.cancel_at: self.cancelled = True
        return self.cancelled


class VoiceFixture:
    process = tree = None
    def __init__(self): self.calls, self.mode = 0, 'success'
    def release_for_memory(self, job): pass
    def cancel_idle_owner(self, session): pass
    def stop(self): pass
    def generate(self, job, text, target, on_chunk=None):
        self.calls += 1
        assert text == ANSWER
        folder = target.parent/target.stem; folder.mkdir(exist_ok=True)
        if on_chunk:
            for entry in SAVED['chunks']:
                index = entry['index']
                shutil.copyfile(SOURCE/f'chunk-{index}.wav', folder/f'chunk-{index}.wav')
                on_chunk(entry['metadata'])
                if self.mode == 'fail_first': raise RuntimeError('Controlled failure after first sentence.')
                if self.mode == 'cancel_first':
                    server.cancel(job); raise server.Cancelled()
        shutil.copyfile(SOURCE/'reply.wav', target)
        target.with_suffix('.json').write_text(json.dumps(SAVED['voiceMetadata']), encoding='utf-8')
        if self.mode == 'cancel_full': server.cancel(job)


def main():
    with patch.object(server, 'MEMORY_PROFILE', 'compact'):
        for name in ('recovery', 'exhaustion', 'cancel', 'stage_deadline', 'job_deadline'):
            current, clock = job(), Clock()
            current['cancel'] = clock
            if name == 'cancel': clock.cancel_at = .2
            if name == 'job_deadline': current['deadlineMonotonic'] = .15
            def resource():
                return {'physicalGiB': 3, 'commitGiB': 3 if name == 'recovery' and clock.now >= .3 else 1.9}
            with patch.object(server.time, 'monotonic', side_effect=clock.monotonic), \
                 patch.object(server, 'memory_resources', side_effect=resource):
                try:
                    server.compact_entry(current, 'voice', deadline=.15 if name == 'stage_deadline' else None)
                    outcome = 'admitted'
                except server.ResourceBusy: outcome = 'resource_busy'
                except server.Cancelled: outcome = 'cancelled'
                except RuntimeError: outcome = 'deadline'
            expected = {'recovery': 'admitted', 'exhaustion': 'resource_busy', 'cancel': 'cancelled',
                        'stage_deadline': 'deadline', 'job_deadline': 'deadline'}[name]
            check(name+'_correct_result', outcome == expected)
            check(name+'_bounded_polling', clock.now <= 30.0001 and max(clock.waits, default=0) <= .10001)
            check(name+'_wait_recorded', current['resourceAdmission'][0]['waitSeconds'] == round(clock.now, 3))
            if name == 'exhaustion': check('full_wait_bound_is_thirty_seconds', abs(clock.now-30) < .001)
        current = job(); current['process'] = type('OwnedFixture', (), {'poll': lambda self: None})()
        try: server.compact_entry(current, 'voice'); refused = False
        except RuntimeError: refused = True
        check('no_wait_while_process_active', refused)

    responses = OUT/'responses'; responses.mkdir(exist_ok=True)
    voice = VoiceFixture()
    with contextlib.ExitStack() as stack:
        for name, value in {'PORT':8770, 'VOICE_ENGINE':'onnx-q4', 'STREAMING':True, 'MEMORY_PROFILE':'compact',
                            'SEQUENTIAL_MODELS':True, 'CANDIDATE_BRAIN':None, 'CANDIDATE_VOICE':voice,
                            'RESPONSES':responses}.items(): stack.enter_context(patch.object(server, name, value))
        stack.enter_context(patch.object(server, 'memory_resources', return_value={'physicalGiB':3.5,'commitGiB':4}))
        runner = stack.enter_context(patch.object(server, 'run_child', return_value=ANSWER))
        for mode in ('fail_first', 'cancel_first', 'cancel_full'):
            cache = OUT/(mode+'-cache'); cache.mkdir(exist_ok=True)
            voice.mode = mode; current = job()
            with patch.object(server, 'VOICE_CACHE', cache): server.process_job(current)
            check(mode+'_never_cached', current['phase'] == 'error' and not list(cache.iterdir()))
        voice.mode = 'success'
        original_release = server.release_candidate_models
        for name in ('cleanup_failure', 'cancel_during_cleanup'):
            cache = OUT/(name+'-cache'); cache.mkdir(exist_ok=True)
            current, seen = job(), []
            def release(target, **kwargs):
                if kwargs['reason'] == 'after_request':
                    seen.append(server.public_job(target))
                    if name == 'cleanup_failure': raise RuntimeError('Controlled cleanup failure.')
                    server.cancel(target)
                else: return original_release(target, **kwargs)
            with patch.object(server, 'VOICE_CACHE', cache), patch.object(server, 'release_candidate_models', side_effect=release):
                server.process_job(current)
            check(name+'_never_publishes_transient_done', seen and all(item['phase'] != 'done' and 'result' not in item for item in seen))
            check(name+'_never_caches_or_succeeds', current['phase'] == 'error' and 'result' not in current and not list(cache.iterdir()))
        cache = OUT/'success-cache'; cache.mkdir(exist_ok=True)
        with patch.object(server, 'VOICE_CACHE', cache):
            first = job(); before = voice.calls; server.process_job(first)
            check('successful_stream_commits_complete_cache', first['phase'] == 'done' and first.get('voiceCacheStored') is True
                  and first['result']['voiceCacheHit'] is False and len(first.get('chunks', [])) == 2)
            second = job(); model_calls = runner.call_count; server.process_job(second)
            check('cache_hit_still_answers_current_question', runner.call_count == model_calls+1)
            check('stream_cache_hit_has_full_audio_no_chunks', second['phase'] == 'done'
                  and second['result']['voiceCacheHit'] is True and second['result']['voiceGenerationPerformed'] is False
                  and not second.get('chunks') and not second.get('streaming') and voice.calls == before+1)
            check('cache_audio_exact_complete_pcm', (responses/(second['id']+'.wav')).read_bytes() == (SOURCE/'reply.wav').read_bytes())
            check('changed_text_is_cache_miss', not server.load_voice_cache(job(), ANSWER+' Extra.', responses/'different.wav'))
            with patch.object(server, 'STREAMING', False):
                check('whole_watermark_is_separate_cache', not server.load_voice_cache(job(), ANSWER, responses/'whole.wav'))
            identity = server.voice_cache_descriptor(ANSWER)['identity']
            check('settings_are_in_cache_identity', identity['ortSeedBeforeConstruction'] == 682
                  and identity['torchSeedAfterConstruction'] == 682 and identity['watermarkMode'] == 'per-sentence'
                  and identity['repetitionPenalty'] == 1.2 and identity['referenceSha256'] == SAVED['voiceMetadata']['referenceSha256'])
        for field, wrong in [('referenceSha256','wrong'),('ortSeedBeforeConstruction',1),('torchSeedAfterConstruction',1),
                             ('modelRevision','wrong'),('text',ANSWER+' Extra.'),('streamedBySentence',False)]:
            metadata = copy.deepcopy(SAVED['voiceMetadata']); metadata[field] = wrong
            try: server.validate_completed_voice(SOURCE/'reply.wav', metadata, ANSWER); refused = False
            except ValueError: refused = True
            check(field+'_mismatch_rejected', refused)
        cancelled_cache = OUT/'cancel_at_commit'; cancelled_cache.mkdir(exist_ok=True)
        current = job(); current.update(phase='done', answer=ANSWER); current['cancel'].set()
        with patch.object(server, 'VOICE_CACHE', cancelled_cache):
            try: server.store_completed_voice_cache(current,SOURCE/'reply.wav',SAVED['voiceMetadata']); refused=False
            except server.Cancelled: refused=True
        check('cancelled_final_checkpoint_never_commits', refused and not list(cancelled_cache.iterdir()))

    receipt = {'scope':'Controlled model/voice routing; existing identity-02 audio copied only into isolated test cache. No inference.',
               'modelInference':False,'serverRestarted':False,'publicChanges':False,'actualCachePrimed':False,
               'checks':checks,'passed':sum(item['passed'] for item in checks),'total':len(checks),
               'sourceSha256':hashlib.sha256((ROOT/'server.py').read_bytes()).hexdigest()}
    (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':receipt['passed'],'total':receipt['total'],'failures':[c for c in checks if not c['passed']]}))
    if receipt['passed'] != receipt['total']: raise SystemExit(1)


if __name__ == '__main__': main()
