/* Fresh native Tcl/WASM interpreter and memory filesystem for each run. */
importScripts('vendor/require.js');
require.config({baseUrl:new URL('.',self.location.href).href,paths:{tcl:'vendor'}});
require(['tcl/wacl'],function(wacl){wacl.onReady(async function(interp){
 const M=interp.Module,evalTcl=M.cwrap('Tcl_Eval','number',['number','string']),get=M.cwrap('Tcl_GetStringResult','string',['number']);
 const word=s=>'"'+String(s).replace(/\\/g,'\\\\').replace(/"/g,'\\"').replace(/\$/g,'\\$').replace(/\[/g,'\\[').replace(/\r/g,'\\r').replace(/\n/g,'\\n')+'"';
 const evaluate=code=>{const status=evalTcl(interp.interp,code);return {status,value:get(interp.interp)}};
 let stdout=[],stderr=[],events=[],observe=false;
 interp.stdout=s=>stdout.push(String(s).replace(/\r$/,''));
 interp.stderr=s=>{s=String(s);if(observe&&s.startsWith('__WS_EVENT__')){try{events.push(JSON.parse(s.slice(12)))}catch{}return;}stderr.push(s);};
 evaluate('encoding system utf-8; fconfigure stdout -encoding utf-8 -translation lf; fconfigure stderr -encoding utf-8 -translation lf; file mkdir /work; cd /work');
 try{const helpers=await fetch(new URL('runtime.tcl',self.location.href)).then(r=>{if(!r.ok)throw Error('Runtime helper unavailable');return r.text()});const r=evaluate(helpers);if(r.status)throw Error(r.value);}catch(e){self.postMessage({type:'failure',message:String(e)});return;}
 const version=evaluate('info patchlevel').value;self.postMessage({type:'ready',version});
 self.onmessage=e=>{
  try{
   const s=e.data;stdout=[];stderr=[];events=[];
   for(const [path,contents] of Object.entries(s.files||{})){
    if(path.startsWith('/')||path.split('/').includes('..'))throw Error('Fixture paths must stay in the virtual working directory');
    const q=word(path);const r=evaluate(`file mkdir [file dirname ${q}]; set ::__fixture [open ${q} w]; puts -nonewline $::__fixture ${word(contents)}; close $::__fixture; unset ::__fixture`);if(r.status)throw Error(r.value);
   }
   evaluate(`set argv [list ${(s.argv||[]).map(word).join(' ')}];set argc ${(s.argv||[]).length}`);
   if(s.trace!==false){evaluate('foreach ::__ws::cmd {set incr lappend expr if foreach for while regexp proc dict string open gets close source oo::class} {if {[llength [info commands $::__ws::cmd]]} {trace add execution $::__ws::cmd leave ::__ws::observe}}; unset ::__ws::cmd');stdout=[];stderr=[];events=[];observe=true;}
   let run=evaluate(s.code);
   evaluate('flush stdout;flush stderr');
   if(s.after&&run.status===0){stdout=[];stderr=[];events=[];run=evaluate(s.after);evaluate('flush stdout;flush stderr');}
   observe=false;
   evaluate('set ::__ws::busy 1; foreach ::__ws::cmd {set incr lappend expr if foreach for while regexp proc dict string open gets close source oo::class} {catch {trace remove execution $::__ws::cmd leave ::__ws::observe}}; unset ::__ws::cmd');
   const output=stdout.join('\n').replace(/\n+$/,'');
   let variables=[],files=[];try{variables=JSON.parse(evaluate('::__ws::snapshot').value);files=JSON.parse(evaluate('::__ws::files').value);}catch{}
   const tests=[];evaluate('set ::workshop_stdout '+word(output));
   if(run.status===0)for(const check of s.checks||[]){const r=evaluate(check.script);tests.push({label:check.label,ok:r.status===0&&r.value==='1',error:r.status?r.value:null});}
   self.postMessage({type:'result',version,output,stderr:stderr.join('\n'),result:run.value,error:run.status?run.value:null,variables,files,events,tests});
  }catch(e){self.postMessage({type:'failure',message:String(e)});}
 };
});},e=>self.postMessage({type:'failure',message:'Tcl engine could not load: '+e}));
