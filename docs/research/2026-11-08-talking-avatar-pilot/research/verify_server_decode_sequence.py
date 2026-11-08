"""Real server helpers and owned FFmpeg/process fixtures. No model inference."""
from __future__ import annotations
import ctypes
from ctypes import wintypes
import json
from pathlib import Path
import subprocess
import sys
import threading
import time
import uuid
import wave

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import server
import memory_reclaim_api as native
from audio_decode_candidate import build_decode_command

OUT=ROOT/'evidence/server-decode-sequence'
FIXTURES=ROOT/'evidence/audio-decode-candidate'


def job(name, source=None):
    folder=OUT/name;folder.mkdir()
    return {'id':uuid.uuid4().hex,'session':'controlled-'+name,'folder':folder,
            'cancel':threading.Event(),'timings':{},'phase':'transcribing',
            'audio':source,'text':'','created':time.time()}


def pcm(path):
    with wave.open(str(path),'rb') as value:return value.readframes(value.getnframes())


def handle_for(pid):
    handle=native.kernel.OpenProcess(0x1000|0x10,False,pid)
    if not handle:raise ctypes.WinError(ctypes.get_last_error())
    return handle


def alive(handle):
    code=wintypes.DWORD()
    if not native.kernel.GetExitCodeProcess(handle,ctypes.byref(code)):raise ctypes.WinError(ctypes.get_last_error())
    return code.value==259


def sleeper_tree(label):
    marker=OUT/(label+'-child.pid')
    script="import subprocess,sys,time;from pathlib import Path;p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);Path(sys.argv[1]).write_text(str(p.pid));time.sleep(30)"
    process=subprocess.Popen([sys.executable,'-c',script,str(marker)],stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000|0x4)
    try:tree=server.OwnedProcessTree(process)
    except BaseException:process.kill();process.wait(timeout=5);raise
    deadline=time.monotonic()+3
    while not marker.exists() and time.monotonic()<deadline:time.sleep(.01)
    if not marker.exists():tree.close();raise RuntimeError('Controlled child did not start.')
    handles=[handle_for(process.pid),handle_for(int(marker.read_text()))]
    return process,tree,handles


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'receipt.json').exists():raise RuntimeError('Previous receipt exists; archive deliberately before rerunning.')
    checks=[]
    def check(name,condition,**details):
        checks.append({'case':name,'passed':bool(condition),**details});assert condition,name
    check('original_defaults_preserved',server.VOICE_ENGINE=='mtl' and server.STT_ENGINE=='whisper-small'
          and server.BRAIN_MODEL=='q8' and not server.SEQUENTIAL_MODELS)
    gap_job=job('gap',FIXTURES/'synthetic-gap234.webm')
    decoded=server.decode_recording(gap_job)
    check('real_run_child_recovers_gapped_pcm',pcm(decoded)==pcm(FIXTURES/'normal-output.wav'),
          duration=gap_job['decodedAudioDuration'],ownedDecodeSeconds=gap_job['timings']['audio decode'])
    check('decode_child_detached_after_return',gap_job['process'] is None and gap_job['processTree'] is None and gap_job['activePid'] is None)
    edge=job('twenty',FIXTURES/'synthetic-20.wav');server.decode_recording(edge)
    check('twenty_seconds_accepted',edge['decodedAudioDuration']==20)
    for name,source in [('overlong','synthetic-21-gap.webm'),('tiny','synthetic-too-short.wav'),('oversized','synthetic-oversized-input.bin')]:
        current=job(name,FIXTURES/source)
        try:server.decode_recording(current)
        except ValueError:rejected=True
        else:rejected=False
        check(name+'_rejected_without_stt',rejected and not(current['folder']/'transcript.json').exists())
        if name=='oversized':check('oversize_rejected_before_subprocess',not current['timings'])

    # Slow only our synthetic decoder so cancellation can be observed deterministically.
    cancel_job=job('cancel',FIXTURES/'synthetic-normal.webm')
    command=build_decode_command(server.FFMPEG,cancel_job['audio'],cancel_job['folder']/'question.wav')
    command.insert(command.index('-i'),'-re')
    outcome={}
    def decode_slowly():
        try:server.run_child(cancel_job,command,'controlled slow decode',25);outcome['state']='finished'
        except server.Cancelled:outcome['state']='cancelled'
        except BaseException as error:outcome['state']=type(error).__name__
    thread=threading.Thread(target=decode_slowly);thread.start()
    deadline=time.monotonic()+3
    while not cancel_job.get('activePid') and time.monotonic()<deadline:time.sleep(.01)
    child=cancel_job.get('process');assert child and child.poll() is None
    cancelled_at=time.monotonic();server.cancel(cancel_job);thread.join(timeout=5)
    check('real_decode_cancel_stops_owned_ffmpeg',not thread.is_alive() and outcome.get('state')=='cancelled' and child.poll() is not None,
          cancellationSeconds=round(time.monotonic()-cancelled_at,3))
    check('cancel_clears_owned_process_fields',cancel_job['process'] is None and cancel_job['processTree'] is None and cancel_job['activePid'] is None)

    # Actual owned process trees stand in for resident models; no model is imported.
    voice_process,voice_tree,voice_handles=sleeper_tree('voice')
    brain_process,brain_tree,brain_handles=sleeper_tree('brain')
    old_brain=server.CANDIDATE_BRAIN
    class ControlledBrain:
        process=brain_process
        process_tree=brain_tree
        def close(self):
            self.process_tree.terminate();self.process.wait(timeout=5);self.process_tree.close();self.process=None
    server.CANDIDATE_VOICE.process=voice_process;server.CANDIDATE_VOICE.tree=voice_tree
    server.CANDIDATE_VOICE.ready=True
    server.CANDIDATE_BRAIN=ControlledBrain()
    try:
        check('owned_residency_fixture_started',all(alive(handle) for handle in voice_handles+brain_handles))
        residency=job('residency')
        server.release_candidate_models(residency,voice=True,answer=True,reason='before_request')
        check('sequential_release_waits_for_all_owned_descendants',all(not alive(handle) for handle in voice_handles+brain_handles))
        check('sequential_release_records_both_models',[event['model'] for event in residency['modelResidencyEvents']]==['voice','answer'])
        check('resident_references_cleared',server.CANDIDATE_VOICE.process is None and server.CANDIDATE_BRAIN.process is None)
    finally:
        voice_tree.close();brain_tree.close();server.CANDIDATE_BRAIN=old_brain
        for handle in voice_handles+brain_handles:native.kernel.CloseHandle(handle)

    # Candidate-only flags reject incompatible/default-port use before serving anything.
    for name,args in [('sequential-default',['--sequential-models']),
        ('sequential-prewarm',['--port','8770','--voice-engine','onnx-q4','--streaming','--prewarm','--sequential-models']),
        ('q4-default',['--brain-model','q4']),
        ('q4-persistent',['--port','8770','--voice-engine','onnx-q4','--brain-model','q4','--persistent-brain'])]:
        result=subprocess.run([sys.executable,str(ROOT/'server.py'),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=8,creationflags=0x08000000)
        check(name+'_rejected_before_server_start',result.returncode==2)
    selected=server.select_brain_model('q4',8770,False)
    check('explicit_q4_file_hash_validated_without_loading',selected.name=='Qwen3-1.7B-Q4_K_M.gguf')
    check('q8_default_selection_unchanged',server.select_brain_model('q8',8769)==server.brain.MODEL)
    report={'testType':'REAL_SERVER_HELPERS_AND_OWNED_SYNTHETIC_PROCESS_FIXTURES','modelsLoaded':False,
        'ownerAudioRead':False,'publicRequests':False,'existingServerRestarted':False,
        'decode':'Real installed ffmpeg via server.run_child and OwnedProcessTree',
        'residency':'Sleep-only Python parent/descendant trees, not model inference',
        'checks':checks,'passed':len(checks)}
    (OUT/'receipt.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
