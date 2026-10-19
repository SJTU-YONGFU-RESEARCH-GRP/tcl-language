/* One Worker per run: fresh Tcl interpreter and virtual filesystem. */
importScripts('vendor/require.js');
importScripts('trace-source.js?v=1f251ee98b8c');
require.config({baseUrl:new URL('.',self.location.href).href,paths:{tcl:'vendor'}});
require(['tcl/wacl'],function(wacl){
  wacl.onReady(function(interp){
    const M=interp.Module;
    const evaluate=M.cwrap('Tcl_Eval','number',['number','string']);
    const result=M.cwrap('Tcl_GetStringResult','string',['number']);
    evaluate(interp.interp,'encoding system utf-8\nfconfigure stdout -encoding utf-8 -translation lf\nfconfigure stderr -encoding utf-8 -translation lf');
    let output=[],observing=false,marker='',traceCount=0,traceLimitReached=false;
    function write(s){const text=String(s).replace(/\r$/,'');output.push(text);if(observing)self.postMessage({type:'stdout',text});}
    interp.stdout=write;
    interp.stderr=s=>{const text=String(s).replace(/\r$/,'');if(observing&&marker&&text.startsWith(marker)){try{const event=JSON.parse(text.slice(marker.length));if(event.command.includes('::__quest_'))return;traceCount++;if(event.index>=256)traceLimitReached=true;self.postMessage({type:'trace',event});}catch{}return;}write(text);};
    self.postMessage({type:'ready'});
    self.onmessage=function(e){
      try{
        output=[];traceCount=0;traceLimitReached=false;
        let observerNS=null;
        if(e.data.trace){
          const token=Math.random().toString(36).slice(2);
          observerNS='::__quest_'+token;marker='__QUEST_'+token+'__';
          const setup=self.QUEST_TRACE_TCL.replaceAll('@NS@',observerNS).replaceAll('@MARKER@',marker);
          if(evaluate(interp.interp,setup)===0){observing=true;evaluate(interp.interp,`set ${observerNS}::enabled 1`);}else{observerNS=null;self.postMessage({type:'trace-unavailable'});}
        }
        const code=evaluate(interp.interp,e.data.code);
        const value=result(interp.interp);
        observing=false;
        if(observerNS)evaluate(interp.interp,`set ${observerNS}::enabled 0`);
        if(traceLimitReached)self.postMessage({type:'trace-limit'});
        const userOutput=output.join('\n');
        const tests=[];
        if(code===0){
          for(const check of e.data.checks||[]){
            const script=check.script||`expr {${check.expr}}`;
            const status=evaluate(interp.interp,script);
            const v=result(interp.interp);
            tests.push({label:check.label,ok:status===0&&v==='1',error:status!==0?v:undefined});
          }
        }
        self.postMessage({type:'result',output:userOutput,result:value,error:code!==0?value:null,tests});
      }catch(err){self.postMessage({type:'failure',message:String(err)});}
    };
  });
},function(err){self.postMessage({type:'failure',message:'无法加载 Tcl 引擎：'+err});});
