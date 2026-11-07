"""Optional task-local English transcription candidate, one process per recording."""
from pathlib import Path
import json
import os
import socket
import sys
import time

os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                  HF_HUB_DISABLE_TELEMETRY='1', OMP_NUM_THREADS='4', MKL_NUM_THREADS='4')


def offline(*args, **kwargs):
    raise RuntimeError('Network is disabled in this local transcription worker.')


socket.socket.connect = offline
socket.socket.connect_ex = offline
socket.create_connection = offline


def main():
    started = time.monotonic()
    root = Path(__file__).resolve().parent
    source, target = map(Path, sys.argv[1:3])
    sys.path.insert(0, str(root/'.runtime'/'stt-candidate'))
    from stt_engine import EnglishSTT
    import soundfile as sf
    audio, sample_rate = sf.read(source, dtype='float32')
    if sample_rate != 16000:
        raise ValueError('Expected a local mono sixteen-kilohertz recording.')
    engine = EnglishSTT(threads=4)
    text, metadata = engine.transcribe(audio)
    payload = {**metadata, 'text': text, 'workerTotalSeconds': round(time.monotonic()-started, 3),
               'workerPersistent': False, 'networkDisabledForInference': True}
    target.write_text(json.dumps(payload, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
