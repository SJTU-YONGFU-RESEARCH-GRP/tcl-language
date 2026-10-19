export function runTcl(spec,onStatus=()=>{},limit=5000){
 let cancel;
 const promise=new Promise((resolve,reject)=>{
  const worker=new Worker(new URL('./worker.js',import.meta.url));let done=false;
  let timer=setTimeout(()=>finish(Error('解释器加载超时。请检查网络后重试。')),25000);
  function finish(error,result){if(done)return;done=true;clearTimeout(timer);worker.terminate();onStatus(error?'error':'done');error?reject(error):resolve(result);}
  cancel=()=>finish(Error('本次运行已停止。代码草稿保留。'));
  worker.onerror=e=>finish(Error(e.message||'Tcl Worker 加载失败'));
  worker.onmessage=e=>{const m=e.data;if(m.type==='ready'){onStatus('running');clearTimeout(timer);timer=setTimeout(()=>finish(Error('运行超过 5 秒，已终止。请检查循环条件。')),limit);worker.postMessage(spec);}else if(m.type==='result')finish(null,m);else if(m.type==='failure')finish(Error(m.message));};
  onStatus('loading');
 });return {promise,stop:()=>cancel?.()};
}
