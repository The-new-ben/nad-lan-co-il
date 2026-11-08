"""Control fixtures only: no speech recognition, language or voice model loads."""
from __future__ import annotations
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
import types
import uuid
import wave
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import server

OUT = ROOT/'evidence/compact-integration-controls'
OUT.mkdir(exist_ok=True)
checks = []


def check(name, passed):
    checks.append({'name': name, 'passed': bool(passed)})


def new_job(question='What should I check before buying a home?'):
    identity = uuid.uuid4().hex
    folder = OUT/identity
    folder.mkdir()
    return {'id': identity, 'session': identity, 'text': question, 'folder': folder,
            'phase': 'queued', 'created': time.time(), 'cancel': threading.Event(),
            'process': None, 'activePid': None, 'timings': {}}


class FixtureVoice:
    process = tree = None
    def __init__(self):
        self.spoken = []
    def release_for_memory(self, job):
        pass
    def generate(self, job, text, target, on_chunk=None):
        self.spoken.append(text)
        with wave.open(str(target), 'wb') as wav:
            wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(24000)
            wav.writeframes(b'\0\0'*14400)
        target.with_suffix('.json').write_text(json.dumps({'cues': [], 'duration': .6,
            'cueMethod': 'CONTROL FIXTURE SILENCE, NO TTS'}), encoding='utf-8')
    def stop(self):
        pass
    def cancel_idle_owner(self, session):
        pass


def main():
    responses, cache = OUT/'responses', OUT/'cache'
    responses.mkdir(exist_ok=True); cache.mkdir(exist_ok=True)
    voice = FixtureVoice()
    with contextlib.ExitStack() as stack:
        values = {'PORT': 8770, 'VOICE_ENGINE': 'onnx-q4', 'BRAIN_MODEL': 'q4',
                  'NO_REPACK': True, 'SEQUENTIAL_MODELS': True, 'MEMORY_PROFILE': 'compact',
                  'STREAMING': False, 'CANDIDATE_BRAIN': None, 'CANDIDATE_VOICE': voice,
                  'RESPONSES': responses, 'VOICE_CACHE': cache}
        for name, value in values.items():
            stack.enter_context(patch.object(server, name, value))
        stack.enter_context(patch.object(server, 'memory_resources', return_value={'physicalGiB': 3.5, 'commitGiB': 4.0}))
        command = server.answer_command(Path('fixture-prompt.txt'))
        check('Q4_candidate_adds_only_no_repack', command == server.brain.command(Path('fixture-prompt.txt')) + ['--no-repack'])
        with patch.object(server, 'NO_REPACK', False):
            check('default_command_unchanged', server.answer_command(Path('fixture-prompt.txt')) == server.brain.command(Path('fixture-prompt.txt')))

        for name, resources in [('physical_entry', {'physicalGiB': 2.299, 'commitGiB': 4}),
                                ('commit_entry', {'physicalGiB': 4, 'commitGiB': 2.499})]:
            job = new_job()
            with patch.object(server, 'memory_resources', return_value=resources):
                try:
                    server.compact_entry(job, 'fixture')
                    rejected = False
                except server.ResourceBusy:
                    rejected = True
            check(name+'_independently_rejected', rejected)
        with patch.object(server, 'memory_resources', return_value={'physicalGiB': 2.3, 'commitGiB': 2.5}):
            server.compact_entry(new_job(), 'fixture')
            check('exact_entry_thresholds_accepted', True)

        job = new_job('What is the asking price of the Kochav HaTzafon mini-penthouse?')
        with patch.object(server, 'run_child', side_effect=AssertionError('No model should run for a reviewed fact.')):
            server.process_job(job)
        check('reviewed_fact_bypasses_model', job['phase'] == 'done' and job['timings']['answer'] == 0)
        result = job.get('result', {})
        check('reviewed_fact_attributed_not_inference', result.get('sourcePage') == 7812 and
              result.get('mode') == 'reviewed_property_facts' and result.get('languageModelInference') is False and
              result.get('modelAttempted') is False and result.get('sourceUrl') == server.property_context.SOURCE_URL)

        fixtures = [
            ('figure', 'The property is at 123 Main Street. Do you want details?', 'source_gap_response'),
            ('role', 'I can arrange a viewing for you. When would you like to visit?', 'role_boundary_response'),
            ('identity', "I'm a licensed broker with local experience. What kind of home do you want?", 'role_boundary_response'),
        ]
        for name, raw, mode in fixtures:
            job = new_job()
            with patch.object(server, 'run_child', return_value=raw):
                server.process_job(job)
            result = job.get('result', {})
            check(name+'_rejection_speaks_editorial_boundary', job['phase'] == 'done' and result.get('mode') == mode
                  and result.get('languageModelInference') is False and result.get('modelAttempted') is True)
            check(name+'_raw_never_public_or_spoken', raw not in voice.spoken and raw not in json.dumps(server.public_job(job)))
            private = json.loads((job['folder']/'receipt.json').read_text(encoding='utf-8'))
            check(name+'_raw_rejection_private', private.get('validatorRejection', {}).get('raw') == raw)

        for name, effect in [('transport', RuntimeError('The local answer step failed.')),
                             ('timeout', RuntimeError('The local answer step took too long.')),
                             ('empty', '')]:
            job, before = new_job(), len(voice.spoken)
            kwargs = {'side_effect': effect} if isinstance(effect, Exception) else {'return_value': effect}
            with patch.object(server, 'run_child', **kwargs):
                server.process_job(job)
            check(name+'_has_no_success_fallback', job['phase'] == 'error' and 'result' not in job and len(voice.spoken) == before)

        with patch.object(server, 'PORT', 8769):
            try:
                server.validated_candidate_answer(fixtures[0][1], new_job())
                rejected = False
            except RuntimeError:
                rejected = True
            check('original_validator_behavior_preserved', rejected)
            job = new_job('What is the asking price of the Kochav HaTzafon mini-penthouse?')
            with patch.object(server, 'run_child', return_value=fixtures[0][1]) as runner:
                server.process_job(job)
            check('original_does_not_use_new_property_lookup', runner.call_count == 1 and job['phase'] == 'error')

        # Real owned processes, without importing any model libraries. Both resource
        # dimensions independently terminate only this job's sleeping child tree.
        for name, low in [('physical', {'physicalGiB': .74, 'commitGiB': 4}),
                          ('commit', {'physicalGiB': 4, 'commitGiB': .99})]:
            job, before = new_job(), time.monotonic()
            def resources():
                return low if job.get('process') is not None else {'physicalGiB': 3.5, 'commitGiB': 4}
            with patch.object(server, 'memory_resources', side_effect=resources):
                try:
                    server.run_child(job, [sys.executable, '-c', 'import time;time.sleep(30)'], 'sleep control '+name, 5)
                    stopped = False
                except server.ResourceBusy:
                    stopped = True
            check(name+'_runtime_floor_stops_owned_process', stopped and time.monotonic()-before < 3
                  and job['process'] is None and job['activePid'] is None and 'resourceAbort' in job)
        with patch.object(server, 'memory_resources', side_effect=AssertionError('Idle jobs do not own a process.')):
            server.checkpoint(new_job())
            check('runtime_guard_does_not_touch_idle_or_other_processes', True)

        # Exercise the actual health handler, with response transport only replaced.
        class HealthFixture:
            path = '/api/health'
            def allowed(self): return True
            def json_response(self, value, *args, **kwargs): self.response = value
        handler = HealthFixture()
        server.Handler.do_GET(handler)
        check('health_reports_exact_compact_admission', handler.response['memoryProfile'] == 'compact'
              and handler.response['resourceAdmission'] == {'physicalGiB': 2.3, 'commitGiB': 2.5}
              and handler.response['noRepack'] is True and handler.response['voiceImplementation'] == 'encoder-release-seeded')
        with patch.object(server, 'MEMORY_PROFILE', 'legacy'), patch.object(server, 'VOICE_ENGINE', 'mtl'):
            check('original_has_no_new_local_guard', server.memory_thresholds()['entryPhysicalGiB'] is None)
        with patch.object(server, 'MEMORY_PROFILE', 'legacy'):
            check('legacy_candidate_guard_stays_three', server.memory_thresholds()['entryPhysicalGiB'] == 3.0)

    # Worker initialization is a control fixture: all heavy imports/constructors are
    # replaced, so this checks adapter and seed ordering without running inference.
    calls, emitted = [], []
    fake_ort = types.SimpleNamespace(__version__='1.31.1', set_seed=lambda n: calls.append(('ort', n)))
    fake_torch = types.SimpleNamespace(manual_seed=lambda n: calls.append(('torch', n)))
    class EngineFixture:
        def __init__(self, **kwargs): calls.append(('encoder-released-constructor', kwargs['threads']))
    fake_adapter = types.SimpleNamespace(EncoderReleasedVoice=EngineFixture)
    original_connect = socket.socket.connect, socket.socket.connect_ex, socket.create_connection
    try:
        spec = importlib.util.spec_from_file_location('voice_worker_control_fixture', ROOT/'onnx_voice_worker.py')
        worker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(worker)
        with patch.dict(sys.modules, {'onnxruntime': fake_ort, 'torch': fake_torch,
                                      'research.onnx_encoder_release_candidate': fake_adapter}), \
             patch.object(worker, 'emit', side_effect=emitted.append), \
             patch.object(sys, 'stdin', io.StringIO('{"type":"shutdown"}\n')):
            worker.main()
    finally:
        socket.socket.connect, socket.socket.connect_ex, socket.create_connection = original_connect
    check('optimized_worker_adapter_and_seed_order', calls == [('ort', 682), ('encoder-released-constructor', 4), ('torch', 682)])
    check('optimized_worker_ready_metadata', emitted[0]['voiceImplementation'] == 'encoder-release-seeded')

    for name, args in [
        ('original_no_repack', ['--no-repack']),
        ('candidate_q8_no_repack', ['--port', '8770', '--voice-engine', 'onnx-q4', '--no-repack']),
        ('compact_without_no_repack', ['--port', '8770', '--voice-engine', 'onnx-q4', '--brain-model', 'q4', '--sequential-models', '--memory-profile', 'compact']),
        ('compact_without_sequential', ['--port', '8770', '--voice-engine', 'onnx-q4', '--brain-model', 'q4', '--no-repack', '--memory-profile', 'compact']),
        ('persistent_q4_no_repack', ['--port', '8770', '--voice-engine', 'onnx-q4', '--brain-model', 'q4', '--no-repack', '--persistent-brain']),
    ]:
        run = subprocess.run([sys.executable, str(ROOT/'server.py'), *args], capture_output=True, text=True, timeout=5,
                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        check(name+'_rejected_before_launch', run.returncode == 2 and 'error:' in run.stderr)

    receipt = {'scope': 'Controlled raw-model/voice fixtures and real owned sleeping processes; no model inference.',
               'modelInference': False, 'browserUsed': False, 'publicChanges': False,
               'checks': checks, 'passed': sum(item['passed'] for item in checks), 'total': len(checks),
               'sourceHashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                for name in ('server.py', 'onnx_voice_worker.py', 'property_context.py')}}
    (OUT/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': receipt['passed'], 'total': receipt['total'],
                      'failures': [item for item in checks if not item['passed']]}))
    if receipt['passed'] != receipt['total']: raise SystemExit(1)


if __name__ == '__main__':
    main()
