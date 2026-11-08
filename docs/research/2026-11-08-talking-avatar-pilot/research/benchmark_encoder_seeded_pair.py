"""Prepared seeded baseline/candidate comparison. Default path runs no models."""
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

from benchmark_encoder_release_candidate import (ROOT, MODEL_DIR, VOICE_PYTHON,
    REFERENCE, REFERENCE_SHA, TEXT, sha256, pcm_receipt, save)

SEED = 682
PREFLIGHT = {'baseline':(2.0,2.5), 'candidate':(1.8,2.2)}
ABORT_PHYSICAL, ABORT_COMMIT = .75, 1.0
POLL_SECONDS, CHILD_SECONDS, TOTAL_SECONDS = .1, 120, 360


def child(folder, variant):
    def blocked(*args, **kwargs):
        raise RuntimeError('Network disabled in isolated seeded comparison.')
    socket.socket.connect = socket.socket.connect_ex = socket.create_connection = blocked
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',
        OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',TOKENIZERS_PARALLELISM='false')
    sys.path.insert(0,str(MODEL_DIR/'ort-1.31.1'))
    import onnxruntime as ort
    if ort.__version__ != '1.31.1':
        raise RuntimeError('Unexpected ONNX runtime.')
    # Set before ANY model session is constructed; random kernel state is per session.
    ort.set_seed(SEED)
    from onnx_encoder_release_candidate import EncoderReleasedVoice, SessionProbe, array_receipt, approved
    import memory_reclaim_api as memory

    class InstrumentedBaseline(EncoderReleasedVoice):
        def __init__(self, **kwargs):
            self.evidence_dir=folder
            self.phase_callback=event
            self.events,self.probes,self.active_probe=[],[],None
            # Exact original constructor: keeps all four sessions and original load order.
            approved.CPUVoiceEngine.__init__(self, **kwargs)
            names=('cond_emb','prompt_token','speaker_embeddings','speaker_features')
            self.conditioning={name:array_receipt(getattr(self,name)) for name in names}
            self.np.savez(folder/'conditioning.npz',**{name:getattr(self,name) for name in names})
            for name in ('embed_tokens','language_model','conditional_decoder'):
                self.sessions[name]=SessionProbe(self,name,self.sessions[name])
            self.event('baseline_ready_without_encoder_release')

        def instrumentation(self):
            result=super().instrumentation()
            result['candidate']='original constructor with observation wrappers only'
            return result

    def event(value):
        value={**value,'machineMemory':memory.memory()}
        with (folder/'phases.jsonl').open('a',encoding='utf-8') as log:
            log.write(json.dumps(value)+'\n')
        print(json.dumps(value),flush=True)

    start=time.monotonic()
    kwargs={'model_dir':MODEL_DIR,'runtime_path':MODEL_DIR/'ort-1.31.1',
            'threads':4,'reference':REFERENCE}
    if variant=='baseline':
        engine=InstrumentedBaseline(**kwargs)
    else:
        engine=EncoderReleasedVoice(**kwargs,evidence_dir=folder,phase_callback=event)
    loaded=time.monotonic()
    # Perth already imported Torch through its normal constructor in both variants.
    # Its direct watermark path has no random operation; this fixes residual RNG state
    # without moving the large Torch import ahead of the reference encoder.
    import torch
    torch.manual_seed(SEED)
    rng_before=hashlib.sha256(torch.get_rng_state().numpy().tobytes()).hexdigest()
    samples,sr,metadata=engine.generate(TEXT)
    rng_after=hashlib.sha256(torch.get_rng_state().numpy().tobytes()).hexdigest()
    import soundfile as sf
    engine.np.save(folder/'watermarked-float.npy',samples)
    sf.write(folder/'candidate.wav',samples,sr,subtype='PCM_16')
    result={'status':'generated','variant':variant,'text':TEXT,'ortSeedBeforeConstruction':SEED,
        'torchSeedAfterConstructionBeforeGeneration':SEED,'torchRngBefore':rng_before,
        'torchRngAfter':rng_after,'torchRngConsumedDuringGeneration':rng_before!=rng_after,
        'threads':4,'runtimeVersion':ort.__version__,'modelRevision':metadata['modelRevision'],
        'initializationSeconds':round(loaded-start,3),'wholeChildSeconds':round(time.monotonic()-start,3),
        'metadata':metadata,'pcm':pcm_receipt(folder/'candidate.wav'),
        'watermarkedFloat':array_receipt(samples),'instrumentation':engine.instrumentation(),
        'watermarkOrArenaChanged':False,'firstDecoderInvocation':True,'historicalPCMEqualityExpected':False,
        'scope':'One seeded nine-word comparison only. No general voice-quality or long-reply claim.'}
    save(folder/'child-result.json',result)
    print(json.dumps({'phase':'finished','variant':variant}),flush=True)


def run_variant(variant,folder,health,deadline,memory,ProcessSamples,OwnedProcessTree,alive_handles):
    folder.mkdir()
    start=time.monotonic()
    state=memory.memory()
    physical,commit=PREFLIGHT[variant]
    result={'variant':variant,'status':'preflight','before':state,'inferenceStarted':False,
        'preflightPhysicalGiB':physical,'preflightCommitGiB':commit,
        'minimumPhysicalGiB':state['availableGiB'],'minimumCommitGiB':state['commitCapacityAvailableGiB']}
    target=folder/'parent-receipt.json'
    process=tree=sampler=None
    try:
        if health.reason:
            result['status']='not_started_'+health.reason
            return result
        if state['availableGiB']<physical or state['commitCapacityAvailableGiB']<commit:
            result['status']='not_started_resource_preflight'
            return result
        if (folder.parent/'cancel').exists() or time.monotonic()>=deadline-5:
            result['status']='not_started_cancel_or_deadline'
            return result
        with (folder/'stdout.txt').open('wb') as stdout,(folder/'stderr.txt').open('wb') as stderr,(folder/'memory.jsonl').open('w',encoding='utf-8') as log:
            env={**os.environ,'PYTHONIOENCODING':'utf-8','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1',
                 'HF_HUB_DISABLE_TELEMETRY':'1','OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4',
                 'TOKENIZERS_PARALLELISM':'false'}
            process=subprocess.Popen([str(VOICE_PYTHON),str(Path(__file__).resolve()),'--child',variant,'--label',folder.parent.name],
                cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,creationflags=0x08000000|0x4)
            try:
                tree=OwnedProcessTree(process)
            except BaseException:
                process.kill();process.wait(timeout=1)
                raise
            sampler=ProcessSamples(process.pid)
            result.update(status='running',inferenceStarted=True,ownedLauncherPid=process.pid)
            save(target,result)
            stop_at=min(time.monotonic()+CHILD_SECONDS,deadline)-5
            while process.poll() is None:
                tick=time.monotonic();state=memory.memory()
                result['minimumPhysicalGiB']=min(result['minimumPhysicalGiB'],state['availableGiB'])
                result['minimumCommitGiB']=min(result['minimumCommitGiB'],state['commitCapacityAvailableGiB'])
                reason=('resource_floor' if state['availableGiB']<=ABORT_PHYSICAL or state['commitCapacityAvailableGiB']<=ABORT_COMMIT else
                        'deadline' if tick>=stop_at else 'requested' if (folder.parent/'cancel').exists() else health.reason)
                if reason:
                    result.update(status='cancelled_'+reason,abortMemory=state)
                    tree.terminate();break
                rows=sampler.sample()
                if not rows:
                    result['status']='cancelled_process_memory_unavailable'
                    tree.terminate();break
                log.write(json.dumps({'elapsedSeconds':round(tick-start,3),**state,'processes':rows})+'\n')
                log.flush()
                time.sleep(max(0,POLL_SECONDS-(time.monotonic()-tick)))
            process.wait(timeout=1);result['exitCode']=process.returncode
            if result['status']=='running':
                result['status']='generated' if process.returncode==0 else 'child_failed'
    except BaseException as exc:
        result.update(status='harness_error',errorType=type(exc).__name__,error=str(exc))
        raise
    finally:
        if tree:tree.close()
        try:
            if process and process.poll() is None:process.wait(timeout=1)
            if sampler:
                result['processPeaks']=sampler.sample()
                alive=alive_handles(sampler);until=time.monotonic()+1
                while alive and time.monotonic()<until:
                    time.sleep(.05);alive=alive_handles(sampler)
                result['ownedProcessesStopped']=not alive
                result['remainingObservedOwnedPids']=alive
                result['peakWorkingMiB']=max((v['peakWorkingMiB'] for v in result['processPeaks']),default=None)
                result['peakCommitMiB']=max((v['peakCommitMiB'] for v in result['processPeaks']),default=None)
        except BaseException as exc:
            result.update(ownedProcessesStopped=False,cleanupErrorType=type(exc).__name__)
        finally:
            if sampler:sampler.close()
            result.update(after=memory.memory(),wallSeconds=round(time.monotonic()-start,3))
            save(target,result)
    return result


def parent(label):
    import memory_reclaim_api as memory
    from benchmark_mtl_loader_candidate import ProcessSamples
    from benchmark_qwen_q4_candidate import OriginalHealth,alive_handles
    sys.path.insert(0,str(ROOT))
    from server import OwnedProcessTree
    started=time.monotonic();deadline=started+TOTAL_SECONDS
    out=ROOT/'evidence/chatterbox-encoder-seeded'/label
    if out.exists():raise RuntimeError('Refusing to overwrite an earlier comparison.')
    out.mkdir(parents=True)
    report={'status':'preflight','variants':[],'ortSeed':SEED,'text':TEXT,
        'physicalAbortFloorGiB':ABORT_PHYSICAL,'commitAbortFloorGiB':ABORT_COMMIT,
        'totalTimeoutSeconds':TOTAL_SECONDS,'childTimeoutSeconds':CHILD_SECONDS,'pollSeconds':POLL_SECONDS,
        'sequentialFreshProcesses':True,'noPublicOrDefaultChanges':True,'ownerApplicationsClosed':False,
        'acceptanceScope':'One seeded nine-word sample only; factuality and long replies are not tested.'}
    health=None;records=[]
    try:
        if sha256(REFERENCE)!=REFERENCE_SHA:raise RuntimeError('Reference changed.')
        provenance=json.loads((MODEL_DIR/'download-receipt.json').read_text(encoding='utf-8'))
        if provenance['revision']!='d21799bd0354adb85e348b8a0442a8405110a2cf':raise RuntimeError('Model revision changed.')
        paths=[Path(__file__),Path(__file__).with_name('onnx_encoder_release_candidate.py'),
               Path(__file__).with_name('benchmark_encoder_release_candidate.py'),
               Path(__file__).with_name('benchmark_qwen_q4_candidate.py'),
               Path(__file__).with_name('benchmark_mtl_loader_candidate.py'),
               Path(__file__).with_name('memory_reclaim_api.py'),ROOT/'server.py',
               MODEL_DIR/'onnx_engine.py',MODEL_DIR/'download-receipt.json',REFERENCE]
        for item in provenance['files']:
            p=MODEL_DIR/item['path']
            if p.stat().st_size!=item['bytes'] or sha256(p)!=item['sha256']:raise RuntimeError('Pinned model file changed.')
            paths.append(p)
        for p in dict.fromkeys(paths):
            records.append({'path':str(p),'bytes':p.stat().st_size,'modifiedNs':p.stat().st_mtime_ns,'sha256':sha256(p)})
        save(out/'source-manifest.json',{'files':records,'modelRevision':provenance['revision']})
        def recheck():
            for item in records:
                p=Path(item['path'])
                if p.stat().st_size!=item['bytes'] or p.stat().st_mtime_ns!=item['modifiedNs']:raise RuntimeError('Reviewed input changed.')
                if item['bytes']<5*1024*1024 and sha256(p)!=item['sha256']:raise RuntimeError('Small input hash changed.')
        health=OriginalHealth();health.start()
        for variant in ('baseline','candidate'):
            recheck()
            result=run_variant(variant,out/variant,health,deadline,memory,ProcessSamples,OwnedProcessTree,alive_handles)
            report['variants'].append(result);save(out/'pair-receipt.json',report)
            if result['status']!='generated' or not result.get('ownedProcessesStopped',False):
                report['status']='stopped_'+variant+'_'+result['status'];return
        recheck()
        base=json.loads((out/'baseline/child-result.json').read_text(encoding='utf-8'))
        cand=json.loads((out/'candidate/child-result.json').read_text(encoding='utf-8'))
        b,c=base['instrumentation'],cand['instrumentation']
        bs,cs=b['sentences'][0],c['sentences'][0]
        checks={'conditioningArraysExact':b['conditioning']==c['conditioning'],
                'emittedTokensExact':bs['emittedTokenIds']==cs['emittedTokenIds'],
                'decoderInputsExact':bs['decoderInput']==cs['decoderInput'],
                'preWatermarkFloatPCMExact':bs['preWatermarkPCM']==cs['preWatermarkPCM'],
                'watermarkedFloatPCMExact':base['watermarkedFloat']==cand['watermarkedFloat'],
                'finalPCM16Exact':base['pcm']['pcmSha256']==cand['pcm']['pcmSha256'],
                'referenceExact':base['metadata']['referenceSha256']==cand['metadata']['referenceSha256']==REFERENCE_SHA,
                'bothStopTokensFound':bool(base['metadata']['stopTokenFound'] and cand['metadata']['stopTokenFound'])}
        report.update(status='pair_generated_review_pending',equalityChecks=checks,allEqualityChecksPassed=all(checks.values()))
    except BaseException as exc:
        report.update(status='harness_error',errorType=type(exc).__name__,error=str(exc));raise
    finally:
        if health:health.close()
        report['wallSeconds']=round(time.monotonic()-started,3)
        save(out/'pair-receipt.json',report)
        print(json.dumps({'receipt':str(out/'pair-receipt.json'),'status':report['status']}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--go',action='store_true')
    parser.add_argument('--child',choices=('baseline','candidate'),help=argparse.SUPPRESS)
    parser.add_argument('--label',default='pair-01')
    args=parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',args.label):parser.error('Use a short lowercase label.')
    if args.child:child(ROOT/'evidence/chatterbox-encoder-seeded'/args.label/args.child,args.child)
    elif args.go:parent(args.label)
    else:print(json.dumps({'preparedOnly':True,'inferenceStarted':False,'seed':SEED,'text':TEXT,
        'preflightPhysicalCommitGiB':PREFLIGHT,'abortPhysicalCommitGiB':[ABORT_PHYSICAL,ABORT_COMMIT],
        'sequentialVariants':['baseline','candidate'],'noPublicOrDefaultChanges':True}))
