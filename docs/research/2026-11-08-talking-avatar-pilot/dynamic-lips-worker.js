// Run inference off the rendering thread. This worker only fetches the local model.
import {analyzeSamples} from './dynamic-lips.js';
self.onmessage=async({data})=>{
  try{
    const result=await analyzeSamples(data.samples,data.sampleRate);
    const {mouthAt,...serializable}=result;
    self.postMessage(serializable);
  }catch(error){self.postMessage({error:error.message||String(error)});}
};
