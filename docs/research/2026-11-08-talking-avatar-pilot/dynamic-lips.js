/* Local audio-to-viseme adapter. Inference vendor is MIT InterviewFlowAI 0.3.0.
   Owns no playback, renderer, microphone, analytics, or remote service. */
import {parseVisemeModel} from './vendor/talking-avatar/visemeModel.js';
import {VisemeDetector} from './vendor/talking-avatar/visemeDetector.js';
import {buildSegments,mouthAt as weightsAt} from './vendor/talking-avatar/coarticulation.js';

const modelURL=new URL('./vendor/talking-avatar/viseme-model.bin',import.meta.url);
let modelPromise=null;
const abortError=()=>new DOMException('Speech analysis cancelled','AbortError');
function check(signal){if(signal?.aborted)throw abortError();}
async function checkedFetch(url,signal){
  const response=await fetch(url,{signal});
  if(!response.ok)throw new Error(`Local speech analysis HTTP ${response.status}`);
  return response.arrayBuffer();
}
export async function loadVisemeModel(){
  if(!modelPromise)modelPromise=checkedFetch(modelURL).then(parseVisemeModel).catch(error=>{modelPromise=null;throw error;});
  return modelPromise;
}

// One mouthOpen shape cannot reproduce rounded/spread lips. This projection keeps
// sound-dependent opening and closure, while the caller controls final small scale.
const OPENNESS={aa:1,O:.72,E:.68,I:.42,U:.32,RR:.35,CH:.30,SS:.24,TH:.25,DD:.24,kk:.26,nn:.25};
export function createMouthTimeline(events,duration){
  const segments=buildSegments(events);
  return seconds=>{
    if(!Number.isFinite(seconds)||seconds<0||seconds>=duration)return 0;
    const weights=weightsAt(segments,seconds*1000);
    let open=0;
    for(const [name,weight] of Object.entries(weights))open+=(OPENNESS[name]||0)*weight;
    // Upstream coarticulation already gives bilabials and f/v priority over vowels.
    return Math.min(1,Math.max(0,open));
  };
}

export async function analyzeSamples(samples,sampleRate,{model,signal,yieldEverySeconds=.25}={}){
  if(!(samples instanceof Float32Array)||!Number.isFinite(sampleRate)||sampleRate<8000)throw new TypeError('Expected mono float audio and a valid sample rate');
  check(signal);
  const activeModel=model||await loadVisemeModel();
  check(signal);
  const events=[];
  const detector=new VisemeDetector(activeModel,sampleRate,0,event=>events.push(event));
  const chunk=Math.max(1,Math.round(sampleRate*yieldEverySeconds));
  const started=performance.now();
  let computeMs=0,maxChunkMs=0;
  for(let at=0;at<samples.length;at+=chunk){
    check(signal);
    const tick=performance.now();
    detector.push(samples.subarray(at,at+chunk));
    const elapsed=performance.now()-tick;computeMs+=elapsed;maxChunkMs=Math.max(maxChunkMs,elapsed);
    await new Promise(resolve=>setTimeout(resolve,0));
  }
  check(signal);
  const flushStarted=performance.now();detector.flush();computeMs+=performance.now()-flushStarted;
  const duration=samples.length/sampleRate;
  return {source:'local-learned-visemes',version:'0.3.0',events,duration,analysisMs:performance.now()-started,computeMs,maxChunkMs,mouthAt:createMouthTimeline(events,duration)};
}

function analyzeInWorker(samples,sampleRate,signal){
  return new Promise((resolve,reject)=>{
    check(signal);
    const worker=new Worker(new URL('./dynamic-lips-worker.js',import.meta.url),{type:'module'});
    const finish=(fn,value)=>{signal?.removeEventListener('abort',cancel);worker.terminate();fn(value);};
    const cancel=()=>finish(reject,abortError());
    signal?.addEventListener('abort',cancel,{once:true});
    worker.onmessage=({data})=>{
      if(data.error){finish(reject,new Error(data.error));return;}
      const timeline=createMouthTimeline(data.events,data.duration);
      finish(resolve,{...data,worker:true,mouthAt:timeline});
    };
    worker.onerror=event=>finish(reject,new Error(event.message||'Local speech worker failed'));
    // Copy the transfer buffer so a worker/CSP failure can fall back without refetching.
    const transferable=samples.slice();
    worker.postMessage({samples:transferable,sampleRate},[transferable.buffer]);
  });
}

export async function analyzeSpeech(url,{signal,useWorker=true,...options}={}){
  check(signal);
  const [bytes,model]=await Promise.all([checkedFetch(url,signal),loadVisemeModel()]);
  check(signal);
  // OfflineAudioContext decodes audio without claiming or starting an output stream.
  const Decoder=globalThis.OfflineAudioContext||globalThis.webkitOfflineAudioContext;
  if(!Decoder)throw new Error('Local speech decoder unavailable');
  const decoder=new Decoder(1,1,16000);
  const buffer=await decoder.decodeAudioData(bytes);
  check(signal);
  const mono=new Float32Array(buffer.length);
  for(let c=0;c<buffer.numberOfChannels;c++){
    const channel=buffer.getChannelData(c);
    for(let i=0;i<mono.length;i++)mono[i]+=channel[i]/buffer.numberOfChannels;
  }
  if(useWorker&&typeof Worker!=='undefined'){
    try{return await analyzeInWorker(mono,buffer.sampleRate,signal);}
    catch(error){check(signal);/* Worker not allowed by host CSP: retain chunked local fallback. */}
  }
  return analyzeSamples(mono,buffer.sampleRate,{model,signal,...options});
}
