"""Isolated same-voice lifecycle experiment. Importing this module starts no model.

Only the reference encoder's lifetime/load order differs. The approved token,
decoder, whole-reply and watermark operations are inherited without rewriting.
"""
from pathlib import Path
import gc
import hashlib
import importlib.util
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / '.runtime/chatterbox-onnx-test'
spec = importlib.util.spec_from_file_location('approved_onnx_engine', MODEL_DIR/'onnx_engine.py')
approved = importlib.util.module_from_spec(spec)
spec.loader.exec_module(approved)


def array_receipt(value):
    return {'shape': list(value.shape), 'dtype': str(value.dtype), 'bytes': value.nbytes,
            'sha256': hashlib.sha256(value.tobytes(order='C')).hexdigest()}


class SessionProbe:
    """Observe existing inputs/outputs without replacing an inference operation."""
    def __init__(self, owner, name, session):
        self.owner, self.name, self.session = owner, name, session

    def __getattr__(self, name):
        return getattr(self.session, name)

    def run(self, output_names, inputs, *args, **kwargs):
        probe = self.owner.active_probe
        if probe is not None and self.name == 'embed_tokens':
            probe['embeddingInputs'].append(inputs['input_ids'].tolist())
        if probe is not None and self.name == 'conditional_decoder':
            probe['decoderSpeechTokens'] = inputs['speech_tokens'].tolist()
            probe['decoderInput'] = array_receipt(inputs['speech_tokens'])
        outputs = self.session.run(output_names, inputs, *args, **kwargs)
        if probe is not None and self.name == 'conditional_decoder':
            wav = outputs[0].squeeze(axis=0)
            probe['preWatermarkPCM'] = array_receipt(wav)
            if self.owner.evidence_dir:
                self.owner.np.save(self.owner.evidence_dir/f'pre-watermark-{probe["index"]}.npy', wav)
        return outputs


class EncoderReleasedVoice(approved.CPUVoiceEngine):
    def __init__(self, model_dir=MODEL_DIR, runtime_path=None, threads=4,
                 reference=None, evidence_dir=None, phase_callback=None):
        begin = time.perf_counter()
        self.model_dir = Path(model_dir)
        self.reference = Path(reference) if reference else ROOT.parent/'kit/ref-female.wav'
        self.evidence_dir = Path(evidence_dir) if evidence_dir else None
        self.phase_callback = phase_callback
        self.events, self.probes, self.active_probe = [], [], None
        if runtime_path:
            sys.path.insert(0, str(Path(runtime_path).resolve()))
        import numpy as np
        import onnxruntime as ort
        import soundfile as sf
        from tokenizers import Tokenizer
        self.np, self.ort, self.sr, self.threads, self.turns = np, ort, 24000, threads, 0
        options = ort.SessionOptions()
        options.intra_op_num_threads, options.inter_op_num_threads = threads, 1
        self.sessions, self.loadTimings = {}, {}
        # Preserve original provider, graph optimizations, arena and thread options.
        start = time.perf_counter()
        encoder = ort.InferenceSession(str(self.model_dir/'onnx/speech_encoder_q4.onnx'),
                                       sess_options=options, providers=['CPUExecutionProvider'])
        self.loadTimings['speech_encoder'] = round(time.perf_counter()-start, 3)
        self.event('encoder_loaded')
        self.tokenizer = Tokenizer.from_file(str(self.model_dir/'tokenizer.json'))
        audio, sr = sf.read(self.reference, dtype='float32')
        if sr != 24000 or audio.ndim != 1:
            raise ValueError('Expected unchanged mono24k reference')
        start = time.perf_counter()
        outputs = encoder.run(None, {'audio_values': audio[np.newaxis, :]})
        names = ('cond_emb', 'prompt_token', 'speaker_embeddings', 'speaker_features')
        # Owned copies break any possible output/allocator lifetime link to the encoder.
        for name, value in zip(names, outputs):
            setattr(self, name, value.copy())
        if len(outputs) != len(names):
            raise RuntimeError('Unexpected reference encoder output count.')
        self.loadTimings['referenceEncoding'] = round(time.perf_counter()-start, 3)
        self.conditioning = {name: array_receipt(getattr(self, name)) for name in names}
        if self.evidence_dir:
            np.savez(self.evidence_dir/'conditioning.npz', **{name:getattr(self,name) for name in names})
        self.event('encoded_before_release')
        # value is the loop's last original output, so explicitly release that alias too.
        del outputs, value, encoder, audio
        gc.collect()
        self.event('encoder_released')
        for name in ('embed_tokens', 'language_model', 'conditional_decoder'):
            start = time.perf_counter()
            session = ort.InferenceSession(str(self.model_dir/'onnx'/f'{name}_q4.onnx'),
                                           sess_options=options, providers=['CPUExecutionProvider'])
            self.sessions[name] = SessionProbe(self, name, session)
            self.loadTimings[name] = round(time.perf_counter()-start, 3)
        self.event('remaining_sessions_loaded')
        start = time.perf_counter()
        import perth
        self.watermarker = perth.PerthImplicitWatermarker()
        self.loadTimings['watermarkerImportAndLoad'] = round(time.perf_counter()-start, 3)
        self.initializationSeconds = round(time.perf_counter()-begin, 3)
        self.referenceSha256 = hashlib.sha256(self.reference.read_bytes()).hexdigest()
        self.event('ready_with_original_watermarker')

    def event(self, name):
        event = {'phase':name, 'atEpoch':time.time()}
        self.events.append(event)
        if self.phase_callback:
            self.phase_callback(event)

    def _sentence(self, text, max_tokens=600):
        probe = {'index':len(self.probes), 'text':text, 'embeddingInputs':[]}
        self.probes.append(probe)
        self.active_probe = probe
        try:
            wav, metadata = super()._sentence(text, max_tokens=max_tokens)
            # Every embedding input after the text prompt is the previous emitted token.
            probe['emittedTokenIds'] = [int(token) for batch in probe['embeddingInputs'][1:]
                                       for row in batch for token in row] + [6562]
            probe['stopTokenFound'] = metadata['stopTokenFound']
            probe['metadata'] = metadata
            return wav, metadata
        finally:
            self.active_probe = None

    def instrumentation(self):
        return {'candidate':'reference encoder released before remaining sessions load',
                'conditioning':self.conditioning, 'events':self.events, 'sentences':self.probes,
                'baseSentenceMethodInherited':True, 'baseGenerateMethodInherited':True,
                'watermarkChanged':False, 'arenaChanged':False, 'noGradAdded':False,
                'originalEngineSource':str(MODEL_DIR/'onnx_engine.py')}
