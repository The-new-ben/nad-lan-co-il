"""Verify only the completed identity-02 output; --go explicitly adopts its cache."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import threading
import wave

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'evidence/local-compact-conversation/identity-02'
WAV_SHA = '9f0e7a95ebc8aa13b7175d8ff6fafaf1352e912425aec38c150cbd5569fa681e'
PCM_SHA = '1ae2f8bd85759116a3a63a7ac9968dcf3ef9548eb3eb2e450213a41eca8e3ad2'
ANSWER = "I'm a fictional, computer-made guide. Are you looking to buy a property and need assistance preparing questions?"
sys.path.insert(0, str(ROOT))
import server


def pcm(path):
    with wave.open(str(path), 'rb') as wav:
        if (wav.getnchannels(),wav.getsampwidth(),wav.getframerate()) != (1,2,24000):
            raise ValueError('The controlled completed audio format changed.')
        return wav.readframes(wav.getnframes())


def main(go=False):
    source = json.loads((SOURCE/'receipt.json').read_text(encoding='utf-8'))
    local = source['serverJobReceipt']; result = local['result']; metadata = source['voiceMetadata']
    if (source['status'] != 'real_local_reply_received_review_pending' or source['modelsMocked'] is not False
            or source['observedServerDescendantsStopped'] is not True or local['phase'] != 'done'
            or local['id'] != source['jobId'] or local.get('cancelled')
            or source['answer'] != ANSWER or result['text'] != ANSWER
            or result['voiceCacheHit'] is not False or result['voiceEngine'] != 'onnx-q4'
            or source['chunkConcatenation']['exactFullPCM'] is not True):
        raise ValueError('The fixed source is not the completed uncached controlled reply.')
    wav = SOURCE/'reply.wav'
    if hashlib.sha256(wav.read_bytes()).hexdigest() != WAV_SHA or hashlib.sha256(pcm(wav)).hexdigest() != PCM_SHA:
        raise ValueError('The known completed reply changed.')
    chunks = source['chunks']
    if len(chunks) != 2 or [entry['index'] for entry in chunks] != [0,1]:
        raise ValueError('The fixed source does not contain both complete sentences.')
    if hashlib.sha256(b''.join(pcm(SOURCE/f'chunk-{index}.wav') for index in (0,1))).hexdigest() != PCM_SHA:
        raise ValueError('The actual sentence files do not concatenate to the known reply.')
    descriptor = server.validate_completed_voice(wav, metadata, ANSWER, engine='onnx-q4', streaming=True)
    report = {'preparedOnly':not go,'existingCompleteVoiceVerified':True,'cacheWritten':False,
              'source':'identity-02','sourceJobId':source['jobId'],'cacheKey':descriptor['cacheKey'],
              'waveSha256':WAV_SHA,'pcmSha256':PCM_SHA,'watermarkMode':'per-sentence',
              'newModelInference':False,'newSpeechSynthesis':False,'publicRequest':False}
    if go:
        job = {'id':source['jobId'],'answer':ANSWER,'phase':'done','cancel':threading.Event(),'process':None}
        adopted = server.store_completed_voice_cache(job,wav,metadata,engine='onnx-q4',streaming=True,
            provenance={'type':'verified_existing_completed_local_job','jobId':source['jobId'],
                        'sourceReceipt':'evidence/local-compact-conversation/identity-02/receipt.json'})
        report.update(cacheWritten=True,adopted=adopted)
        target = ROOT/'evidence/compact-wait-cache-controls/identity-02-cache-adoption.json'
        target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',action='store_true')
    main(parser.parse_args().go)
