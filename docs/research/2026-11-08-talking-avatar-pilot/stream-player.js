/* Ordered sentence playback. Receives actual generated chunks, never fabricates replies. */
const aborted=()=>new DOMException('Response cancelled','AbortError');

export function createSentenceQueue({signal,prepare,play,onProgress=()=>{}}){
  const seen=new Map(),pending=new Map();
  let next=0,final=false,running=false,settled=false,failure=null,preparation=Promise.resolve();
  let resolveDone,rejectDone;
  const done=new Promise((resolve,reject)=>{resolveDone=resolve;rejectDone=reject;});
  // Preparation and cancellation can finish before the polling loop awaits done.
  done.catch(()=>{});
  const finish=(error)=>{
    if(settled)return;settled=true;pending.clear();signal?.removeEventListener('abort',cancel);
    if(error){failure=error;rejectDone(error);}else resolveDone({played:next,received:seen.size});
  };
  const cancel=()=>finish(aborted());
  signal?.addEventListener('abort',cancel,{once:true});
  if(signal?.aborted)cancel();
  async function drain(){
    if(running||settled)return;running=true;
    try{
      while(pending.has(next)&&!settled){
        const entry=pending.get(next),prepared=await entry.prepared;
        if(signal?.aborted)throw aborted();
        if(prepared.error)throw prepared.error;
        await play(entry.chunk,prepared.value,signal);
        if(signal?.aborted)throw aborted();
        pending.delete(next);next++;onProgress({played:next,received:seen.size});
      }
      if(final&&!settled){
        if(pending.size)throw new Error('A spoken sentence is missing');
        finish();
      }
    }catch(error){finish(error);}
    finally{running=false;}
  }
  return {
    done,
    push(chunks){
      if(settled)return;
      for(const chunk of chunks){
        if(!Number.isInteger(chunk.index)||chunk.index<0||!chunk.audioUrl)throw new Error('Invalid speech chunk');
        const identity=JSON.stringify([chunk.audioUrl,chunk.text||'']);
        if(seen.has(chunk.index)){
          if(seen.get(chunk.index)!==identity)throw new Error('A spoken sentence changed after publication');
          continue;
        }
        if(final)throw new Error('Speech arrived after the response finished');
        seen.set(chunk.index,identity);
        const prepared=preparation.then(()=>{
          if(signal?.aborted)throw aborted();
          return prepare(chunk,signal);
        }).then(value=>({value}),error=>({error}));
        preparation=prepared.then(()=>{});
        pending.set(chunk.index,{chunk,prepared});
      }
      drain();
    },
    finish(){final=true;drain();},
    get failure(){return failure;},
    get played(){return next;},
    get received(){return seen.size;}
  };
}
