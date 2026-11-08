"""One stage per process. Reuses the existing voice environment without modifying it."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import sys
import time

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['OMP_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'


def no_network(*args, **kwargs):
    raise RuntimeError('Network is disabled in this local speech worker.')


socket.socket.connect = no_network
socket.socket.connect_ex = no_network
socket.create_connection = no_network

ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT.parent / 'kit' / 'ref-female.wav'
WHISPER = Path('C:/Users/777/.cache/whisper/small.pt')


def transcribe(source, target):
    import numpy as np
    import soundfile as sf
    import torch
    import whisper
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    started = time.monotonic()
    audio, sr = sf.read(source, dtype='float32')
    if sr != 16000 or audio.ndim != 1 or not 0.25 <= len(audio)/sr <= 20.05:
        raise ValueError('Please record between a quarter second and twenty seconds.')
    if float(np.max(np.abs(audio))) < .005 or float(np.sqrt(np.mean(audio**2))) < .0008:
        raise ValueError('No clear speech was heard. Please try again or type a question.')
    model = whisper.load_model(str(WHISPER), device='cpu')
    loaded = time.monotonic()
    result = model.transcribe(audio, language='en', fp16=False, temperature=0,
                              condition_on_previous_text=False, verbose=False)
    text = result['text'].strip()
    if not text or all(s.get('no_speech_prob', 0) > .8 for s in result.get('segments', [])):
        raise ValueError('No clear speech was heard. Please try again or type a question.')
    if len(text) > 1200:
        raise ValueError('Please ask one short question.')
    payload = {'text': text, 'duration': len(audio)/sr, 'loadSeconds': round(loaded-started, 3),
               'inferenceSeconds': round(time.monotonic()-loaded, 3), 'engine': 'Whisper small, CPU, offline'}
    target.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def synthesize(source, target):
    import librosa
    import numpy as np
    import soundfile as sf
    import torch
    from huggingface_hub import snapshot_download
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS, Conditionals
    threads = int(os.environ.get('NL3D_VOICE_THREADS', '4'))
    torch.set_num_threads(max(1, min(threads, 8)))
    torch.set_num_interop_threads(1)
    torch.manual_seed(682)
    text = source.read_text(encoding='utf-8').strip()
    if not text or len(text) > 550:
        raise ValueError('Invalid response text.')
    started = time.monotonic()
    cached = snapshot_download('ResembleAI/chatterbox', local_files_only=True,
        allow_patterns=['ve.pt', 't3_mtl23ls_v2.safetensors', 's3gen.pt',
                        'grapheme_mtl_merged_expanded_v1.json', 'conds.pt', 'Cangjie5_TC.json'])
    model = ChatterboxMultilingualTTS.from_local(Path(cached), device='cpu')
    model_loaded = time.monotonic()
    reference_hash = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()
    reference_cache = ROOT/'.runtime'/('reference-'+reference_hash[:16]+'-'+Path(cached).name[:12]+'.pt')
    if reference_cache.exists():
        model.conds = Conditionals.load(reference_cache, map_location='cpu')
        reference_cache_hit = True
    else:
        model.prepare_conditionals(str(REFERENCE), exaggeration=.5)
        model.conds.save(reference_cache)
        reference_cache_hit = False
    loaded = time.monotonic()
    parts = re.findall(r'[^.!?]+[.!?]+|[^.!?]+$', text)
    chunks = []
    sentence_timings = []
    for sentence in parts:
        part_started = time.monotonic()
        wav = model.generate(sentence.strip(), language_id='en', exaggeration=.5,
                             cfg_weight=.5, temperature=.65)
        samples = wav.squeeze(0).numpy()
        samples, _ = librosa.effects.trim(samples, top_db=38)
        chunks.extend([samples, np.zeros(int(model.sr*.22), dtype=np.float32)])
        sentence_timings.append({'text': sentence.strip(), 'seconds': round(time.monotonic()-part_started, 3),
                                 'audioSeconds': round(len(samples)/model.sr, 3)})
    samples = np.concatenate(chunks[:-1])
    if not 1 <= len(samples)/model.sr <= 35 or not np.isfinite(samples).all():
        raise RuntimeError('The local voice returned an unusable recording.')
    sf.write(target, samples, model.sr, subtype='PCM_16')
    # Amplitude cues are deliberately subtle; they are not phoneme recognition.
    step = int(model.sr*.08)
    energies = [float(np.sqrt(np.mean(samples[i:i+step]**2))) for i in range(0, len(samples), step)]
    level = max(float(np.percentile(energies, 70)), .012)
    cues = []
    for i, energy in enumerate(energies):
        value = 'X' if energy < max(.004, level*.10) else ('C' if energy > level*1.8 else 'B')
        start, end = round(i*step/model.sr, 3), round(min((i+1)*step, len(samples))/model.sr, 3)
        if cues and cues[-1]['value'] == value:
            cues[-1]['end'] = end
        else:
            cues.append({'start': start, 'end': end, 'value': value})
    payload = {'cues': cues, 'duration': len(samples)/model.sr,
               'loadSeconds': round(loaded-started, 3), 'inferenceSeconds': round(time.monotonic()-loaded, 3),
               'modelLoadSeconds': round(model_loaded-started, 3),
               'referenceSeconds': round(loaded-model_loaded, 3), 'referenceCacheHit': reference_cache_hit,
               'engine': 'Chatterbox Multilingual, CPU, offline', 'reference': str(REFERENCE),
               'referenceSha256': reference_hash,
               'exaggeration': .5, 'cfgWeight': .5, 'temperature': .65,
               'sentenceTimings': sentence_timings, 'torchThreads': torch.get_num_threads(),
               'cueMethod': '80 ms PCM amplitude, not phoneme recognition'}
    target.with_suffix('.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['stt', 'tts'])
    parser.add_argument('source', type=Path)
    parser.add_argument('target', type=Path)
    args = parser.parse_args()
    (transcribe if args.stage == 'stt' else synthesize)(args.source, args.target)
