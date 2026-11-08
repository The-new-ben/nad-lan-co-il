"""Task-local CPU candidate using official Turbo ONNX q4. No network or package installer.
Inference loop adapted from ResembleAI/chatterbox-turbo-ONNX model-card example.
MIT licence retained in CHATTERBOX-LICENSE.txt. Weights and runtime have separate receipts.
"""
from pathlib import Path
import hashlib,re,sys,time

class CPUVoiceEngine:
    def __init__(self,model_dir,runtime_path=None,threads=4,reference=None):
        begin=time.perf_counter();self.model_dir=Path(model_dir);self.reference=Path(reference) if reference else self.model_dir.parents[2]/'kit'/'ref-female.wav'
        if runtime_path:sys.path.insert(0,str(Path(runtime_path).resolve()))
        import numpy as np
        import onnxruntime as ort
        import soundfile as sf
        from tokenizers import Tokenizer
        self.np=np;self.ort=ort;self.sr=24000;self.threads=threads;self.turns=0
        options=ort.SessionOptions();options.intra_op_num_threads=threads;options.inter_op_num_threads=1
        self.sessions={};self.loadTimings={}
        for name in ['speech_encoder','embed_tokens','language_model','conditional_decoder']:
            start=time.perf_counter()
            self.sessions[name]=ort.InferenceSession(str(self.model_dir/'onnx'/f'{name}_q4.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
            self.loadTimings[name]=round(time.perf_counter()-start,3)
        self.tokenizer=Tokenizer.from_file(str(self.model_dir/'tokenizer.json'))
        audio,sr=sf.read(self.reference,dtype='float32')
        if sr!=24000 or audio.ndim!=1:raise ValueError('Expected unchanged mono24k reference')
        start=time.perf_counter()
        self.cond_emb,self.prompt_token,self.speaker_embeddings,self.speaker_features=self.sessions['speech_encoder'].run(None,{'audio_values':audio[np.newaxis,:]})
        self.loadTimings['referenceEncoding']=round(time.perf_counter()-start,3)
        start=time.perf_counter()
        import perth
        self.watermarker=perth.PerthImplicitWatermarker()
        self.loadTimings['watermarkerImportAndLoad']=round(time.perf_counter()-start,3)
        self.initializationSeconds=round(time.perf_counter()-begin,3)
        self.referenceSha256=hashlib.sha256(self.reference.read_bytes()).hexdigest()

    def _sentence(self,text,max_tokens=600):
        np=self.np;started=time.perf_counter();input_ids=np.array([self.tokenizer.encode(text).ids],dtype=np.int64)
        generated=np.array([[6561]],dtype=np.int64);stopped=False
        for step in range(max_tokens):
            if time.perf_counter()-started>180:raise TimeoutError('Token generation exceeded180seconds')
            embeds=self.sessions['embed_tokens'].run(None,{'input_ids':input_ids})[0]
            if step==0:
                embeds=np.concatenate((self.cond_emb,embeds),axis=1);batch,seq,_=embeds.shape
                past={i.name:np.zeros([batch,16,0,64],dtype=np.float16 if i.type=='tensor(float16)' else np.float32) for i in self.sessions['language_model'].get_inputs() if 'past_key_values' in i.name}
                mask=np.ones((batch,seq),dtype=np.int64);positions=np.arange(seq,dtype=np.int64).reshape(1,-1).repeat(batch,axis=0)
            logits,*present=self.sessions['language_model'].run(None,dict(inputs_embeds=embeds,attention_mask=mask,position_ids=positions,**past))
            scores=logits[:,-1,:];seen=np.take_along_axis(scores,generated,axis=1);seen=np.where(seen<0,seen*1.2,seen/1.2);scores=scores.copy();np.put_along_axis(scores,generated,seen,axis=1)
            input_ids=np.argmax(scores,axis=-1,keepdims=True).astype(np.int64);generated=np.concatenate((generated,input_ids),axis=-1)
            if (input_ids.flatten()==6562).all():stopped=True;break
            mask=np.concatenate([mask,np.ones((batch,1),dtype=np.int64)],axis=1);positions=positions[:,-1:]+1
            for j,key in enumerate(past):past[key]=present[j]
        tokenSeconds=time.perf_counter()-started
        if not stopped:raise RuntimeError('No stop token; rejecting truncated candidate')
        tokens=generated[:,1:-1];tokens=np.concatenate([self.prompt_token,tokens,np.full((tokens.shape[0],3),4299,dtype=np.int64)],axis=1)
        start=time.perf_counter()
        wav=self.sessions['conditional_decoder'].run(None,dict(speech_tokens=tokens,speaker_embeddings=self.speaker_embeddings,speaker_features=self.speaker_features))[0].squeeze(axis=0)
        if not np.isfinite(wav).all() or not .2<=len(wav)/self.sr<=30:raise RuntimeError('Unusable candidate audio')
        return wav,{'text':text,'stopTokenFound':stopped,'tokens':generated.shape[1]-1,'tokenSeconds':round(tokenSeconds,3),'decodeSeconds':round(time.perf_counter()-start,3),'audioSeconds':len(wav)/self.sr}

    def generate(self,text):
        started=time.perf_counter();np=self.np
        if not text.strip() or len(text)>550:raise ValueError('Expected one short reply')
        parts=re.findall(r'[^.!?]+[.!?]+|[^.!?]+$',text)
        chunks=[];segments=[]
        for part in parts:
            wav,meta=self._sentence(part.strip());chunks.extend([wav,np.zeros(int(self.sr*.22),dtype=np.float32)]);segments.append(meta)
        samples=np.concatenate(chunks[:-1]);markStart=time.perf_counter()
        samples=self.watermarker.apply_watermark(samples,sample_rate=self.sr)
        metadata={'engine':'Chatterbox Turbo ONNX q4 CPU, isolated candidate','version':self.ort.__version__,'modelRevision':'d21799bd0354adb85e348b8a0442a8405110a2cf','sampleRate':self.sr,'stopTokenFound':all(s['stopTokenFound'] for s in segments),'reference':str(self.reference),'referenceSha256':self.referenceSha256,'generationSeconds':round(time.perf_counter()-started,3),'watermarkSeconds':round(time.perf_counter()-markStart,3),'audioSeconds':len(samples)/self.sr,'segments':segments,'warm':self.turns>0,'initializationSeconds':self.initializationSeconds,'loadTimings':self.loadTimings,'turnIndex':self.turns,'text':text,'threads':self.threads,'method':'Greedy plus repetition penalty1.2; separate sentences with220ms gap; same reference; no edge trimming; output watermarked','providerCharge':0}
        self.turns+=1
        return samples,self.sr,metadata

    def iter_generate(self,text):
        """Yield each completed, watermarked sentence before starting the next.

        This optional streaming path adds no silence. The consuming worker owns
        queue gaps and backpressure. Closing the iterator leaves turns unchanged.
        The existing whole-reply generate path is intentionally independent.
        """
        if not text.strip() or len(text)>550:raise ValueError('Expected one short reply')
        parts=[part.strip() for part in re.findall(r'[^.!?]+[.!?]+|[^.!?]+$',text) if part.strip()]
        if not parts:raise ValueError('Expected at least one spoken sentence')
        turnIndex=self.turns;warm=turnIndex>0
        for index,part in enumerate(parts):
            started=time.perf_counter();generationStartedAtEpoch=time.time()
            wav,segment=self._sentence(part)
            markStart=time.perf_counter()
            samples=self.watermarker.apply_watermark(wav,sample_rate=self.sr)
            watermarkSeconds=time.perf_counter()-markStart
            if not self.np.isfinite(samples).all():raise RuntimeError('Unusable watermarked candidate audio')
            metadata={'engine':'Chatterbox Turbo ONNX q4 CPU, isolated candidate','version':self.ort.__version__,'modelRevision':'d21799bd0354adb85e348b8a0442a8405110a2cf','sampleRate':self.sr,'index':index,'text':part,'isLast':index==len(parts)-1,'stopTokenFound':segment['stopTokenFound'],'generationStartedAtEpoch':generationStartedAtEpoch,'generatedAtEpoch':time.time(),'generationSeconds':round(time.perf_counter()-started,3),'watermarkSeconds':round(watermarkSeconds,3),'audioSeconds':len(samples)/self.sr,'segments':[segment],'reference':str(self.reference),'referenceSha256':self.referenceSha256,'warm':warm,'initializationSeconds':self.initializationSeconds,'loadTimings':self.loadTimings,'turnIndex':turnIndex,'threads':self.threads,'method':'Greedy plus repetition penalty1.2; sentence streaming; same reference; no edge trimming; each sentence watermarked; no appended gap','providerCharge':0}
            yield samples,self.sr,metadata
        self.turns+=1
