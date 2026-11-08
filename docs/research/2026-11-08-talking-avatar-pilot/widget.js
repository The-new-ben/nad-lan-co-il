/* Local approval prototype. Optional conversation uses the configured local endpoint.
   No analytics or live deployment.
   NadLan Instruments palette and IBM Plex Sans are inherited from its Claude Design identity. */
import * as THREE from './vendor/three.module.js';
import {GLTFLoader} from './vendor/GLTFLoader.js';

const base = new URL('./', import.meta.url);
const supplied = window.__NL3D || {};
const cfg = {
  modelUrl:new URL('assets/nadlan-advisor-v2.glb',base).href,
  voiceUrl:new URL('assets/greet-en.mp3',base).href,
  cuesUrl:new URL('assets/greet-en.cues.json',base).href,
  fallbackUrl:new URL('assets/portrait-cutout-v2.png',base).href,
  originalUrl:new URL('assets/fallback-original.webp',base).href,
  storageKey:'nlag-closed', revealDelay:450, mouthGain:.62,
  obstacles:'#nlcta, #nla11y, .nlcta, .nla11y, [data-avatar-obstacle]',
  ...supplied
};
const audio = new Audio(cfg.voiceUrl);
audio.preload='auto';
audio.setAttribute('playsinline','');
let resolveReady;
const api = window.NLAvatar = {
  state:'initializing', renderer:'pending', audio, startedAt:null, firstInteractionAt:null,
  frames:0, mouth:0, blink:0, errors:[], modelStats:null,
  ready:new Promise(resolve=>{resolveReady=resolve;}),
  close:()=>close(), diagnostics:()=>diagnostics()
};
api.playSpeech=options=>playSpeech(options);
api.stopSpeech=()=>{cancelSpeechAnalysis();cancelQuestion();stopRecording(false);pause();};
api.enableConversation=endpoint=>{cfg.conversationEndpoint=endpoint;if(mic){mic.hidden=false;textForm.hidden=false;cc.setAttribute('aria-label','Show captions and text question');}};
let closed=false, started=false, starting=false, revealed=false, readyResolved=false,playAttempt=0,pageSuspended=false;
let root,face,caption,captionPanel,feedback,textForm,textInput,cancelButton,cc,mic,status,fallback,canvas;
let renderer,scene,camera,model,rig,raf=0,lastFrame=0,mouth=0;
let cues=[],morphMeshes=[],blinkMaterials=[];
let dynamicMouth=null,speechAnalysisController=null;
let revealTimer=0,positionTimer=0;
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
const cleanups=[];
let transcript="Hi, welcome to NadLan. I'm here to help you find the right home in Israel: prices, mortgages, new projects, and every check before you sign. What shall we talk about?";
let sentenceCues=[
  [0,1.85,'Hi, welcome to NadLan.'],
  [1.85,7.9,"I'm here to help you find the right home in Israel: prices, mortgages, new projects,"],
  [7.9,10.2,'and every check before you sign.'],
  [10.2,99,'What shall we talk about?']
];
let recorder=null,micStream=null,micPermissionGeneration=0,recordingSendGeneration=0,micAnalyser=null,micContext=null,micRaf=0,recordingTimeout=0;
let recordingStarted=0,hadSpeech=false,lastSpeechAt=0,requestController=null,currentJobId=null;
function listen(target,type,fn,opts) {target.addEventListener(type,fn,opts);cleanups.push(()=>target.removeEventListener(type,fn,opts));}
function ready() {if(!readyResolved){readyResolved=true;resolveReady(api);}}
function storageClosed(){try{return localStorage.getItem(cfg.storageKey)==='1';}catch{return false;}}
function diagnostics(){return {
  state:api.state,renderer:api.renderer,closed,started,visible:revealed,frames:api.frames,
  mouth:api.mouth,blink:api.blink,startedAt:api.startedAt,firstInteractionAt:api.firstInteractionAt,
  audio:{paused:audio.paused,currentTime:audio.currentTime,duration:Number.isFinite(audio.duration)?audio.duration:null},
  modelStats:api.modelStats,lipAnalysis:api.lipAnalysis||null,errors:[...api.errors],reducedMotion:reducedMotion.matches,
  bounds:root&&!closed?rect(root.getBoundingClientRect()):null
};}
function rect(r){return {x:r.x,y:r.y,width:r.width,height:r.height,top:r.top,right:r.right,bottom:r.bottom,left:r.left};}
function close(){
  if(closed)return;closed=true;api.state='closed';playAttempt++;starting=false;audio.pause();
  clearTimeout(revealTimer);clearTimeout(positionTimer);cancelAnimationFrame(raf);raf=0;
  stopRecording(false);cancelQuestion();cancelSpeechAnalysis();
  cleanups.splice(0).forEach(fn=>fn());
  if(root){root.hidden=true;root.setAttribute('aria-hidden','true');}
  try{localStorage.setItem(cfg.storageKey,'1');}catch{}
  if(renderer){renderer.dispose();renderer.forceContextLoss();}
  ready();
}
function reveal(){
  if(closed)return;revealed=true;root.dataset.visible='true';position();
  if(api.state==='initializing')api.state='waiting';schedule();
}
function firstInteraction(event){
  if(!event.isTrusted||closed||started||starting||document.hidden||speechBusy())return;
  if(event.type==='keydown'&&(event.ctrlKey||event.altKey||event.metaKey||['Shift','Control','Alt','Meta','Escape','Tab'].includes(event.key)))return;
  if(event.target instanceof Element&&event.target.closest('.nl3d-close,.nl3d-cc,.nl3d-mic,.nl3d-caption'))return;
  api.firstInteractionAt=performance.now();reveal();speak(false);
}
function speechBusy(){return pageSuspended||api.state==='microphone-permission'||recorder?.state==='recording'||!!requestController||!!speechAnalysisController;}
function speak(replay=false,responseReady=false){
  if(closed||starting||document.hidden||pageSuspended||(!responseReady&&speechBusy()))return;
  if(!audio.paused&&!replay)return;
  if(replay||audio.ended)audio.currentTime=0;
  const attempt=++playAttempt;starting=true;status.textContent='Starting…';
  // play() is invoked synchronously from the trusted user event, before any awaited work.
  const playPromise=audio.play();
  Promise.resolve(playPromise).then(()=>{
    if(attempt!==playAttempt)return;
    starting=false;if(closed){audio.pause();return;}
    started=true;api.state='speaking';api.startedAt=performance.now();
    status.textContent='Speaking';face.setAttribute('aria-label','Pause voice');clearInputFeedback();
    schedule();
  }).catch(error=>{
    if(attempt!==playAttempt)return;
    starting=false;api.state='waiting';status.textContent='Tap to hear';
    if(error.name!=='NotAllowedError')api.errors.push('audio:'+error.name);
  });
}
function pause(){playAttempt++;starting=false;audio.pause();if(closed)return;api.state='paused';status.textContent='Tap to resume';face.setAttribute('aria-label','Resume voice');schedule();}
async function playSpeech({url,cues:nextCues=[],text='',captionCues=null}){
  if(closed)throw new Error('Character is closed');
  cancelSpeechAnalysis();playAttempt++;starting=false;audio.pause();dynamicMouth=null;
  const controller=new AbortController();speechAnalysisController=controller;
  const speechUrl=new URL(url,location.href).href;
  api.state='preparing-speech';status.textContent='Preparing voice…';phaseFeedback('synthesizing');
  try{
    const {analyzeSpeech}=await import('./dynamic-lips.js');
    const timeline=await analyzeSpeech(speechUrl,{signal:controller.signal});
    if(closed||controller.signal.aborted)return;
    dynamicMouth=timeline.mouthAt;
    api.lipAnalysis={source:timeline.source,worker:timeline.worker===true,events:timeline.events.length,duration:timeline.duration,analysisMs:timeline.analysisMs,maxChunkMs:timeline.maxChunkMs};
  }catch(error){
    if(error.name==='AbortError'||closed)return;
    api.errors.push('lip-analysis:'+error.message);
  }
  if(closed||controller.signal.aborted)return;
  speechAnalysisController=null;
  audio.src=speechUrl;audio.currentTime=0;
  cues=Array.isArray(nextCues)?nextCues:(nextCues.mouthCues||[]);
  transcript=text;sentenceCues=captionCues||[[0,Infinity,text]];caption.textContent=text;
  started=true;starting=false;reveal();speak(false,true);
}
function cancelSpeechAnalysis(){speechAnalysisController?.abort();speechAnalysisController=null;}
function inputFeedback(message,{open=true,kind='processing'}={}){
  if(closed||!feedback)return;
  feedback.textContent=message;feedback.hidden=false;feedback.dataset.kind=kind;caption.hidden=true;
  root.dataset.micState=kind;textForm.hidden=!cfg.conversationEndpoint;
  if(open){captionPanel.hidden=false;cc.setAttribute('aria-pressed','true');cc.setAttribute('aria-label','Hide captions');}
  positionCaption();
}
function clearInputFeedback(){
  if(feedback)feedback.hidden=true;if(caption)caption.hidden=false;if(root)delete root.dataset.micState;
}
function phaseFeedback(phase){
  const message=({queued:'Question received. Waiting for a reply…',claimed:'Question received. Preparing a reply…',
    transcribing:'Recording received. Turning your speech into text…',thinking:'Preparing an answer…',
    speaking:'Preparing the spoken reply…',synthesizing:'Preparing the spoken reply…',streaming:'Preparing the spoken reply…'})[phase]||'Preparing your reply…';
  inputFeedback(message,{open:false});
}
function microphoneFailure(error){
  const message=error.name==='NotAllowedError'||error.name==='SecurityError'
    ?'Microphone access was not allowed. Allow it in your browser, or type your question.'
    :error.name==='NotFoundError'?'No microphone was found. Connect one or type your question.'
    :'The microphone could not start. Please try again or type your question.';
  api.state='waiting';status.textContent='Try microphone';mic.disabled=false;mic.setAttribute('aria-busy','false');
  mic.setAttribute('aria-label','Try microphone again');inputFeedback(message,{kind:'error'});
}
async function startRecording(){
  if(closed||!cfg.conversationEndpoint)return;
  if(recorder?.state==='recording'){stopRecording(true);return;}
  // A microphone tap is conversation intent, even while permission is pending or denied.
  started=true;reveal();cancelQuestion();cancelSpeechAnalysis();playAttempt++;audio.pause();starting=false;
  if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){
    api.state='waiting';status.textContent='Mic unavailable';
    inputFeedback('Voice recording is unavailable in this browser. You can type your question below.',{kind:'error'});return;
  }
  api.state='microphone-permission';status.textContent='Allow microphone';mic.disabled=true;mic.setAttribute('aria-busy','true');
  inputFeedback('Allow microphone access in your browser to start listening.',{kind:'permission'});
  const permissionGeneration=++micPermissionGeneration;
  try{
    const grantedStream=await navigator.mediaDevices.getUserMedia({audio:true});
    if(closed||document.hidden||pageSuspended||permissionGeneration!==micPermissionGeneration){grantedStream.getTracks().forEach(t=>t.stop());if(!closed&&permissionGeneration===micPermissionGeneration){mic.disabled=false;mic.setAttribute('aria-busy','false');api.state='waiting';status.textContent='Mic stopped';inputFeedback('Recording did not start. Tap the microphone again or type a question.',{open:false,kind:'idle'});}return;}
    micStream=grantedStream;
    const mime=['audio/webm;codecs=opus','audio/webm','audio/mp4'].find(type=>MediaRecorder.isTypeSupported(type));
    const activeRecorder=new MediaRecorder(micStream,mime?{mimeType:mime}:undefined),parts=[];
    recorder=activeRecorder;const sendGeneration=++recordingSendGeneration;
    activeRecorder.ondataavailable=e=>{if(e.data.size)parts.push(e.data);};
    activeRecorder.onstop=()=>{if(recorder===activeRecorder)recorder=null;if(activeRecorder.__send&&sendGeneration===recordingSendGeneration&&!closed&&!pageSuspended)sendRecording(new Blob(parts,{type:activeRecorder.mimeType}));};
    recorder.start();started=true;recordingStarted=performance.now();lastSpeechAt=recordingStarted;hadSpeech=false;
    api.state='listening';status.textContent='Listening…';mic.disabled=false;mic.setAttribute('aria-busy','false');mic.setAttribute('aria-pressed','true');mic.setAttribute('aria-label','Stop recording and send question');
    inputFeedback('Listening. Tap the microphone again to send your question.',{kind:'listening'});
    recordingTimeout=setTimeout(()=>stopRecording(true),20000);
    // Local voice activity is used only to end this explicitly requested microphone recording.
    try{
      micContext=new (window.AudioContext||window.webkitAudioContext)();
      micAnalyser=micContext.createAnalyser();micAnalyser.fftSize=512;
      micContext.createMediaStreamSource(micStream).connect(micAnalyser);
      monitorSpeech();
    }catch{}
  }catch(error){if(closed||permissionGeneration!==micPermissionGeneration)return;stopRecording(false);api.errors.push('microphone:'+error.name);microphoneFailure(error);}
}
function monitorSpeech(){
  if(!micAnalyser||recorder?.state!=='recording')return;
  const values=new Uint8Array(micAnalyser.fftSize);micAnalyser.getByteTimeDomainData(values);
  const rms=Math.sqrt(values.reduce((sum,v)=>sum+((v-128)/128)**2,0)/values.length),now=performance.now();
  if(rms>.025){hadSpeech=true;lastSpeechAt=now;}
  if(hadSpeech&&now-lastSpeechAt>1500&&now-recordingStarted>1600){stopRecording(true);return;}
  micRaf=requestAnimationFrame(monitorSpeech);
}
function stopRecording(send){
  const active=recorder?.state==='recording'||api.state==='microphone-permission';
  micPermissionGeneration++;
  if(!send)recordingSendGeneration++;
  clearTimeout(recordingTimeout);cancelAnimationFrame(micRaf);micRaf=0;
  if(recorder){recorder.__send=send;if(recorder.state!=='inactive')recorder.stop();}
  micStream?.getTracks().forEach(t=>t.stop());micStream=null;micAnalyser=null;
  micContext?.close().catch(()=>{});micContext=null;
  if(mic){mic.disabled=send;mic.setAttribute('aria-busy','false');mic.setAttribute('aria-pressed','false');mic.setAttribute('aria-label','Ask a question by voice');}
  if(active&&!closed){api.state=send?'processing-recording':'waiting';status.textContent=send?'Sending…':'Mic stopped';
    inputFeedback(send?'Finishing your recording…':'Recording stopped. You can try again or type a question.',{open:false,kind:send?'processing':'idle'});}
}
async function sendRecording(blob){
  const body=new FormData();body.append('audio',blob,blob.type.includes('mp4')?'question.m4a':'question.webm');
  return sendQuestion({body});
}
function cancelQuestion(){
  const pending=!!requestController||!!speechAnalysisController;
  cancelSpeechAnalysis();
  const controller=requestController;requestController=null;controller?.abort();cancelRequestToken(controller);
  if(currentJobId){fetch(`/api/jobs/${encodeURIComponent(currentJobId)}/cancel`,{method:'POST',keepalive:true}).catch(()=>{});currentJobId=null;}
  if(pending&&!closed){
    playAttempt++;starting=false;audio.pause();api.state='waiting';status.textContent='Tap to hear';face.setAttribute('aria-label','Hear voice');
    mic.disabled=false;textForm.querySelector('[type="submit"]').disabled=false;cancelButton.hidden=true;
  }
}
function cancelRequestToken(controller){
  const token=controller?.requestToken;if(!token)return;
  controller.requestToken=null;
  fetch(`/api/requests/${encodeURIComponent(token)}/cancel`,{method:'POST',keepalive:true}).catch(()=>{});
}
async function checkConversation(){
  if(!cfg.conversationEndpoint||closed)return;
  try{
    const response=await fetch(cfg.healthEndpoint||'/api/health');
    const health=await response.json();
    if(closed)return;
    if(!response.ok||health.available===false){caption.textContent='Voice conversation is unavailable just now. Please try again shortly.';}
  }catch{if(!closed)caption.textContent='Voice conversation is unavailable just now. Please try again shortly.';}
}
async function sendQuestion(fetchOptions){
  playAttempt++;starting=false;audio.pause();
  api.state='thinking';status.textContent='Sending…';mic.disabled=true;
  inputFeedback('Sending your question…');
  if(textForm){textForm.querySelector('[type="submit"]').disabled=true;cancelButton.hidden=false;}
  requestController=new AbortController();
  const controller=requestController;
  try{
    controller.requestToken=crypto.randomUUID();
    const headers=new Headers(fetchOptions.headers||{});headers.set('X-NL-Request-ID',controller.requestToken);
    // Keep the submission receipt available so a late job can still be cancelled.
    // Polling and audio work use the abort signal; large microphone uploads do not use keepalive.
    const response=await fetch(cfg.conversationEndpoint,{method:'POST',...fetchOptions,headers});
    let data=await response.json();
    if(closed||pageSuspended||controller.signal.aborted||requestController!==controller){
      cancelRequestToken(controller);
      if(data.jobId)fetch(`/api/jobs/${encodeURIComponent(data.jobId)}/cancel`,{method:'POST',keepalive:true}).catch(()=>{});
      throw new DOMException('Cancelled','AbortError');
    }
    if(!response.ok)throw new Error(data.error||'Voice response unavailable');
    const startedWaiting=performance.now();
    currentJobId=data.jobId||null;
    while(data.jobId&&!(data.audioUrl||data.result?.audioUrl)&&data.phase!=='error'&&data.status!=='error'){
      if(controller.signal.aborted)throw new DOMException('Aborted','AbortError');
      if(performance.now()-startedWaiting>600000)throw new Error('Response took too long');
      const phase=data.phase||data.status||'thinking';api.state=phase;phaseFeedback(phase);
      status.textContent=({transcribing:'Transcribing…',thinking:'Thinking…',speaking:'Preparing voice…',synthesizing:'Preparing voice…'})[phase]||'One moment…';
      await new Promise(resolve=>setTimeout(resolve,1200));
      const jobUrl=data.jobUrl||`/api/jobs/${encodeURIComponent(data.jobId)}`;
      const poll=await fetch(jobUrl,{signal:controller.signal});
      const next=await poll.json();if(!poll.ok)throw new Error(next.error||'Response unavailable');
      data={jobId:data.jobId,...next};
    }
    if(data.error||data.phase==='error'||data.status==='error')throw new Error(data.error||'Response unavailable');
    data=data.result||data;
    if(!data.audioUrl)throw new Error('Response has no audio');
    if(closed)return;
    api.lastUserText=data.userText||'';api.lastReplyText=data.text||'';
    await playSpeech({url:data.audioUrl,cues:data.cues||[],text:data.text||''});
  }catch(error){cancelRequestToken(controller);if(!closed&&requestController===controller){if(error.name!=='AbortError'){api.errors.push('conversation:'+error.message);inputFeedback('The reply could not finish. Try the microphone again or type another question.',{kind:'error'});}api.state='waiting';status.textContent=error.name==='AbortError'?'Tap to hear':'Please try again';}}
  finally{if(requestController===controller){requestController=null;currentJobId=null;if(mic&&!closed){mic.disabled=false;textForm.querySelector('[type="submit"]').disabled=false;cancelButton.hidden=true;}}}
}
function updateCaption(){const line=sentenceCues.find(([a,b])=>audio.currentTime>=a&&audio.currentTime<b);caption.textContent=line?line[2]:transcript;}
function position(){
  if(!root||closed)return;
  const viewportWidth=window.visualViewport?.width||innerWidth,viewportHeight=window.visualViewport?.height||innerHeight;
  const minLeft=Math.max(8,viewportWidth-root.offsetWidth-(viewportWidth>=900?24:12));
  root.style.setProperty('--nl3d-left',`${minLeft}px`);
  let bottom=14;
  // Keep both existing site controls completely clear, using their actual current rectangles.
  const obstacles=[...document.querySelectorAll(cfg.obstacles)].filter(el=>el!==root&&el.getClientRects().length)
    .map(el=>el.getBoundingClientRect()).filter(r=>r.width>0&&r.height>0&&r.bottom>0&&r.top<viewportHeight);
  const width=root.offsetWidth,height=root.offsetHeight;
  for(const r of obstacles){
    if(minLeft<r.right+12&&minLeft+width>r.left-12&&r.bottom>viewportHeight*.45)
      bottom=Math.max(bottom,viewportHeight-r.top+14);
  }
  if(!obstacles.length)bottom=140;
  bottom=Math.min(bottom,Math.max(8,viewportHeight-height-12));
  root.style.setProperty('--nl3d-bottom',`${Math.round(bottom)}px`);
  positionCaption();resize();
}
function positionCaption(){
  if(!captionPanel||captionPanel.hidden||!root)return;
  const vw=window.visualViewport?.width||innerWidth,vh=window.visualViewport?.height||innerHeight;
  const r=root.getBoundingClientRect(),pw=captionPanel.offsetWidth;
  captionPanel.style.left=`${Math.max(8-r.left,Math.min(root.offsetWidth-pw,vw-8-r.left-pw))}px`;
  captionPanel.style.top='auto';captionPanel.style.bottom='calc(100% + 10px)';
  const p=captionPanel.getBoundingClientRect();
  if(p.top<8){
    // Wide short viewports have room beside the head. Keep the requested panel
    // on screen rather than leaving its questions and captions above the edge.
    captionPanel.style.bottom='auto';
    if(r.left-p.width-10>=8)captionPanel.style.left=`${-p.width-10}px`;
    else if(r.right+p.width+10<vw-8)captionPanel.style.left=`${root.offsetWidth+10}px`;
    captionPanel.style.top=`${Math.max(8,Math.min(r.top,vh-p.height-8))-r.top}px`;
  }
}
function queuePosition(){clearTimeout(positionTimer);positionTimer=setTimeout(position,60);}
function resize(){
  if(!renderer||!camera||!face)return;
  const w=face.clientWidth,h=face.clientHeight;
  const frameHeight=cfg.frameHeight||1.68;
  camera.left=-frameHeight*w/h/2;camera.right=frameHeight*w/h/2;
  camera.top=frameHeight/2;camera.bottom=-frameHeight/2;camera.updateProjectionMatrix();
  renderer.setSize(w,h,false);renderOnce();
}
function morph(name,value){for(const mesh of morphMeshes){const i=mesh.morphTargetDictionary?.[name];if(i!==undefined)mesh.morphTargetInfluences[i]=value;}}
function renderOnce(){if(renderer&&scene&&camera&&!closed&&!document.hidden){renderer.render(scene,camera);api.frames++;}}
function schedule(){if(!raf&&!closed&&!document.hidden&&renderer&&revealed)raf=requestAnimationFrame(tick);}
function tick(now){
  raf=0;if(closed||document.hidden||!revealed||!renderer)return;
  const dt=Math.min(.1,(now-lastFrame)/1000||.033);
  if(now-lastFrame<32){schedule();return;}lastFrame=now;
  const active=!audio.paused&&!audio.ended;
  let target=0;
  if(active){if(dynamicMouth)target=dynamicMouth(audio.currentTime)*cfg.mouthGain;else{const cue=cues.find(c=>audio.currentTime>=c.start&&audio.currentTime<c.end);if(cue&&!['A','X'].includes(cue.value))target=(cue.value==='D'?.8:.5)*cfg.mouthGain;}}
  mouth+=(target-mouth)*(1-Math.exp(-dt*22));
  if(Math.abs(mouth)<.001)mouth=0;
  api.mouth=mouth;morph('mouthOpen',mouth);
  const t=now/1000;
  const blinkPhase=t%5.3;
  const blink=reducedMotion.matches?0:(blinkPhase>.07&&blinkPhase<.24?Math.sin((blinkPhase-.07)/.17*Math.PI):0);
  api.blink=blink;
  // Reuse the approved closed-eye artwork on the same 3D surface. Collapsing
  // the iris texture with a morph looked like a squint, so that morph stays off.
  morph('blink',0);for(const material of blinkMaterials)material.opacity=blink;
  if(rig){rig.rotation.y=reducedMotion.matches?0:Math.sin(t*.58)*.042;rig.rotation.x=reducedMotion.matches?0:Math.sin(t*.41)*.008;}
  if(active)updateCaption();renderOnce();
  // A reduced-motion visitor gets static idle frames; mouth still follows the spoken greeting.
  if(!reducedMotion.matches||active||mouth>0)schedule();
}
async function loadModel(){
  try{
    renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,powerPreference:'low-power'});
    renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));renderer.outputColorSpace=THREE.SRGBColorSpace;
    renderer.setClearColor(0x000000,0);renderer.toneMapping=THREE.NoToneMapping;
    scene=new THREE.Scene();camera=new THREE.OrthographicCamera(-1,1,1,-1,.01,100);
    camera.position.set(0,.10,5);camera.lookAt(0,.10,0);
    scene.add(new THREE.AmbientLight(0xffffff,2));
    const gltf=await new GLTFLoader().loadAsync(cfg.modelUrl);
    if(closed){gltf.scene.traverse(o=>{if(o.geometry)o.geometry.dispose();});return;}
    model=gltf.scene;const box=new THREE.Box3().setFromObject(model),size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());
    model.position.sub(center);rig=new THREE.Group();rig.add(model);scene.add(rig);
    if(cfg.modelRotation)rig.rotation.set(...cfg.modelRotation);
    let vertices=0,triangles=0;model.traverse(o=>{if(o.isMesh){vertices+=o.geometry.attributes.position.count;triangles+=(o.geometry.index?.count||o.geometry.attributes.position.count)/3;if(o.morphTargetInfluences)morphMeshes.push(o);if(o.name==='BlinkOverlay'){const mats=Array.isArray(o.material)?o.material:[o.material];for(const material of mats){material.transparent=true;material.opacity=0;material.depthWrite=false;blinkMaterials.push(material);}o.renderOrder=2;}}});
    api.modelStats={size:size.toArray(),vertices,triangles,morphTargets:morphMeshes.map(o=>Object.keys(o.morphTargetDictionary||{}))};
    api.renderer='webgl';fallback.hidden=true;resize();schedule();ready();
  }catch(error){
    api.renderer='fallback';api.errors.push('model:'+String(error.message||error));
    if(renderer){renderer.dispose();renderer=null;}canvas.hidden=true;fallback.hidden=false;ready();
  }
}
async function init(){
  if(storageClosed()){closed=true;api.state='closed';api.renderer='not-loaded';ready();return;}
  root=document.createElement('aside');root.className='nl3d';root.id='nl3d';root.setAttribute('aria-label','NadLan computer-made character');
  root.innerHTML=`<button class="nl3d-face" aria-label="Hear greeting"><img class="nl3d-fallback" alt="" draggable="false"><canvas class="nl3d-canvas" aria-hidden="true"></canvas><span class="nl3d-status">Tap to hear</span></button><button class="nl3d-close" aria-label="Close character"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m3 3 10 10M13 3 3 13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button><p class="nl3d-disclosure">Computer-made character</p><button class="nl3d-mic" hidden aria-label="Ask a question by voice" aria-pressed="false" aria-busy="false" aria-describedby="nl3d-feedback"><svg viewBox="0 0 20 20" aria-hidden="true"><rect x="7" y="2" width="6" height="10" rx="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M4 9v1a6 6 0 0 0 12 0V9M10 16v3M6.5 19h7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span class="nl3d-mic-stop" aria-hidden="true"></span></button><button class="nl3d-cc" aria-label="Show greeting captions" aria-pressed="false" aria-controls="nl3d-caption"><span aria-hidden="true">CC</span></button><div id="nl3d-caption" class="nl3d-caption" hidden><p id="nl3d-feedback" class="nl3d-feedback" role="status" aria-live="polite" aria-atomic="true" hidden></p><p class="nl3d-caption-text"></p><form class="nl3d-text-form" hidden><label for="nl3d-question">Or type your question</label><input id="nl3d-question" name="question" type="text" maxlength="500" autocomplete="off" placeholder="Ask in English" required><button type="submit">Send</button><button type="button" class="nl3d-cancel" hidden>Cancel response</button></form></div>`;
  document.body.appendChild(root);
  face=root.querySelector('.nl3d-face');captionPanel=root.querySelector('.nl3d-caption');caption=root.querySelector('.nl3d-caption-text');feedback=root.querySelector('.nl3d-feedback');textForm=root.querySelector('.nl3d-text-form');textInput=root.querySelector('input');cancelButton=root.querySelector('.nl3d-cancel');cc=root.querySelector('.nl3d-cc');mic=root.querySelector('.nl3d-mic');status=root.querySelector('.nl3d-status');fallback=root.querySelector('img');canvas=root.querySelector('canvas');
  mic.hidden=!cfg.conversationEndpoint;listen(mic,'click',e=>{e.stopPropagation();startRecording();});
  textForm.hidden=!cfg.conversationEndpoint;
  if(cfg.conversationEndpoint)cc.setAttribute('aria-label','Show captions and text question');
  listen(textForm,'submit',event=>{event.preventDefault();event.stopPropagation();const text=textInput.value.trim();if(!text||requestController)return;stopRecording(false);audio.pause();started=true;textInput.value='';sendQuestion({headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});});
  listen(cancelButton,'click',()=>{cancelQuestion();stopRecording(false);audio.pause();});
  fallback.src=cfg.fallbackUrl;fallback.onerror=()=>{if(fallback.src!==cfg.originalUrl){fallback.src=cfg.originalUrl;fallback.dataset.original='true';}};
  caption.textContent=transcript;
  listen(root.querySelector('.nl3d-close'),'click',e=>{e.stopPropagation();close();});
  // The global first-tap handler owns a first click on the portrait too; avoid an immediate pause.
  listen(face,'click',e=>{e.stopPropagation();if(speechBusy()||(api.firstInteractionAt!==null&&performance.now()-api.firstInteractionAt<350))return;if(!audio.paused)pause();else speak(audio.ended);});
  listen(cc,'click',e=>{e.stopPropagation();captionPanel.hidden=!captionPanel.hidden;cc.setAttribute('aria-pressed',String(!captionPanel.hidden));cc.setAttribute('aria-label',captionPanel.hidden?(cfg.conversationEndpoint?'Show captions and text question':'Show greeting captions'):'Hide captions');updateCaption();positionCaption();if(!captionPanel.hidden)checkConversation();});
  listen(document,'pointerup',firstInteraction,true);listen(document,'keydown',firstInteraction,true);
  listen(document,'visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;if(!audio.paused)pause();if(recorder?.state==='recording'){stopRecording(false);api.state='waiting';status.textContent='Tap to hear';}}else{lastFrame=0;renderOnce();schedule();}});
  listen(window,'pagehide',()=>{pageSuspended=true;pause();stopRecording(false);cancelQuestion();cancelSpeechAnalysis();cancelAnimationFrame(raf);raf=0;});
  listen(window,'pageshow',()=>{pageSuspended=false;if(!closed){renderOnce();schedule();}});
  listen(window,'resize',queuePosition);listen(window,'scroll',queuePosition,{passive:true});
  if(window.visualViewport){listen(visualViewport,'resize',queuePosition);listen(visualViewport,'scroll',queuePosition);}
  listen(reducedMotion,'change',()=>{renderOnce();schedule();});
  listen(audio,'ended',()=>{api.state='ended';status.textContent='Hear again';face.setAttribute('aria-label','Hear again');updateCaption();schedule();});
  listen(canvas,'webglcontextlost',e=>{e.preventDefault();cancelAnimationFrame(raf);raf=0;if(!closed){api.renderer='fallback';fallback.hidden=false;canvas.hidden=true;}});
  if('ResizeObserver' in window){const observer=new ResizeObserver(queuePosition);document.querySelectorAll(cfg.obstacles).forEach(el=>observer.observe(el));cleanups.push(()=>observer.disconnect());}
  fetch(cfg.cuesUrl).then(r=>{if(!r.ok)throw new Error('cue load');return r.json();}).then(data=>{cues=data.mouthCues||[];}).catch(e=>api.errors.push(e.message));
  position();revealTimer=setTimeout(reveal,cfg.revealDelay);loadModel();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
