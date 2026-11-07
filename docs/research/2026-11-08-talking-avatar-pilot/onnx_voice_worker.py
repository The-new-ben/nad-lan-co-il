"""Optional isolated Chatterbox Turbo ONNX candidate, never the default voice.

The stdio protocol is private to server.py. Model files and runtime stay in the
task folder; the existing voice environment is not installed into or modified.
"""
from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path
import socket
import sys
import time

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT/'.runtime'/'chatterbox-onnx-test'
os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                  HF_HUB_DISABLE_TELEMETRY='1', TOKENIZERS_PARALLELISM='false')


def deny_network(*args, **kwargs):
    raise RuntimeError('Network is disabled in this local voice worker.')


socket.socket.connect = deny_network
socket.socket.connect_ex = deny_network
socket.create_connection = deny_network


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False), flush=True)


def amplitude_cues(samples, sample_rate):
    import numpy as np
    samples = np.asarray(samples).reshape(-1)
    step = int(sample_rate*.08)
    energies = [float(np.sqrt(np.mean(samples[i:i+step]**2))) for i in range(0, len(samples), step)]
    level = max(float(np.percentile(energies, 70)), .012)
    cues = []
    for i, energy in enumerate(energies):
        value = 'X' if energy < max(.004, level*.10) else ('C' if energy > level*1.8 else 'B')
        start = round(i*step/sample_rate, 3)
        end = round(min((i+1)*step, len(samples))/sample_rate, 3)
        if cues and cues[-1]['value'] == value:
            cues[-1]['end'] = end
        else:
            cues.append({'start': start, 'end': end, 'value': value})
    return cues


def stream_turn(engine, request, target):
    """Publish one newly synthesized sentence, then wait until the server exposes it."""
    import numpy as np
    import soundfile as sf
    folder = target.parent/target.stem
    folder.mkdir(exist_ok=True)
    iterator = iter(engine.iter_generate(request['text']))
    chunks, segments = [], []
    started = time.monotonic()
    while True:
        try:
            with contextlib.redirect_stdout(sys.stderr):
                samples, sample_rate, metadata = next(iterator)
        except StopIteration:
            break
        index = len(chunks)
        if metadata.get('index') != index or not metadata.get('stopTokenFound'):
            raise RuntimeError('The voice candidate returned an incomplete sentence.')
        samples = np.asarray(samples).reshape(-1)
        if not np.isfinite(samples).all() or not .2 <= len(samples)/sample_rate <= 30:
            raise RuntimeError('The voice candidate returned invalid sentence audio.')
        if not metadata.get('isLast'):
            samples = np.concatenate((samples, np.zeros(int(sample_rate*.22), dtype=np.float32)))
        chunk_path = folder/f'chunk-{index}.wav'
        sf.write(chunk_path, samples, sample_rate, subtype='PCM_16')
        chunk = {'index': index, 'text': metadata['text'], 'duration': len(samples)/sample_rate,
                 'cues': amplitude_cues(samples, sample_rate),
                 'generatedAtEpoch': metadata.get('generatedAtEpoch'),
                 'audioWrittenAtEpoch': time.time(), 'isLast': bool(metadata.get('isLast'))}
        # Emission is outside redirect_stdout. The acknowledgment prevents the next
        # sentence from starting until the HTTP-visible job state contains this one.
        emit({'type': 'chunk', 'id': request['id'], 'chunk': chunk})
        ack_line = sys.stdin.readline()
        if not ack_line:
            raise RuntimeError('The server stopped while publishing a sentence.')
        ack = json.loads(ack_line)
        if ack.get('type') != 'chunk-ack' or ack.get('id') != request['id'] or ack.get('index') != index:
            raise RuntimeError('Invalid sentence publication acknowledgment.')
        metadata['publishedAtEpoch'] = ack.get('publishedAtEpoch')
        metadata['nextSentenceMayStartAtEpoch'] = time.time()
        chunk_path.with_suffix('.json').write_text(json.dumps({**metadata, **chunk}, indent=2), encoding='utf-8')
        chunks.append(samples)
        segments.append(metadata)
    if not chunks or not segments[-1].get('isLast'):
        raise RuntimeError('The streamed answer did not finish.')
    samples = np.concatenate(chunks)
    metadata = {key: value for key, value in segments[-1].items()
                if key not in ('index', 'isLast', 'text', 'generatedAtEpoch', 'publishedAtEpoch', 'nextSentenceMayStartAtEpoch')}
    metadata.update({'text': request['text'], 'segments': segments, 'streamedBySentence': True,
                     'audioSeconds': len(samples)/sample_rate,
                     'watermarkSeconds': round(sum(segment.get('watermarkSeconds', 0) for segment in segments), 3),
                     'generationSeconds': round(sum(segment.get('generationSeconds', 0) for segment in segments), 3),
                     'streamingElapsedSeconds': round(time.monotonic()-started, 3),
                     'generationStartedAtEpoch': segments[0].get('generationStartedAtEpoch'),
                     'allSentencesGeneratedAtEpoch': segments[-1].get('generatedAtEpoch'),
                     'method': 'Each new sentence watermarked and published before generating the next; 220 ms gap on nonfinal chunks'})
    return samples, sample_rate, metadata


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    started = time.monotonic()
    sys.path.insert(0, str(CANDIDATE))
    with contextlib.redirect_stdout(sys.stderr):
        # API adapted to the independently benchmarked engine, not a second model implementation.
        from onnx_engine import CPUVoiceEngine
        engine = CPUVoiceEngine(model_dir=CANDIDATE,
                                runtime_path=CANDIDATE/'ort-1.31.1', threads=4)
    emit({'type': 'ready', 'loadSeconds': round(time.monotonic()-started, 3),
          'engine': 'Chatterbox Turbo ONNX q4, optional comparison'})
    for line in sys.stdin:
        request = {}
        try:
            request = json.loads(line)
            if request.get('type') == 'shutdown':
                return
            text = request['text']
            target = Path(request['target']).resolve()
            if not target.is_relative_to((ROOT/'responses').resolve()) or target.suffix != '.wav':
                raise ValueError('Invalid local response path.')
            if not isinstance(text, str) or not text or len(text) > 550:
                raise ValueError('Invalid response text.')
            turn_start = time.monotonic()
            if request.get('stream'):
                samples, sample_rate, metadata = stream_turn(engine, request, target)
            else:
                with contextlib.redirect_stdout(sys.stderr):
                    samples, sample_rate, metadata = engine.generate(text)
            with contextlib.redirect_stdout(sys.stderr):
                import numpy as np
                import soundfile as sf
                if not np.isfinite(samples).all() or not .5 <= len(samples)/sample_rate <= 35:
                    raise RuntimeError('The voice candidate returned invalid audio.')
                if not metadata.get('stopTokenFound'):
                    raise RuntimeError('The voice candidate did not finish its answer.')
                sf.write(target, samples, sample_rate, subtype='PCM_16')
            payload = {**metadata, 'engine': metadata.get('engine', 'Chatterbox Turbo ONNX q4, optional comparison'),
                       'duration': len(samples)/sample_rate, 'cues': amplitude_cues(samples, sample_rate),
                       'cueMethod': '80 ms PCM amplitude, not phoneme recognition',
                       'workerTurnSeconds': round(time.monotonic()-turn_start, 3)}
            target.with_suffix('.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
            emit({'type': 'result', 'id': request['id'], 'metadata': payload})
        except Exception as exc:
            emit({'type': 'error', 'id': request.get('id'), 'error': str(exc)})


if __name__ == '__main__':
    main()
