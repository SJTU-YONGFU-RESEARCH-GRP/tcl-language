import {runtimeActionSound} from './action-sounds.js?v=1f251ee98b8c';
import {sceneSVG,CAST} from './adventure-art.js?v=1f251ee98b8c';
import {createRuntimeModel,advanceRuntime} from './runtime-story.js?v=1f251ee98b8c';
import {language,t,localize} from './i18n.js?v=1f251ee98b8c';
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const b=(zh,en)=>language()==='en'?en:zh;
let live=null;
export function clearRuntime(){live?.destroy();live=null;}
export function runtimeSnapshot(){return live?.snapshot();}
export function startRuntime(){live?.start();}
export function pushRuntime(event){live?.push(event);}
export function finishRuntime(event){live?.finish(event);}
export function editRuntime(){live?.edited();}
export function afterRuntime(callback){if(live)live.after(callback);else callback();}
function describe(e){
 if(!e)return b('点击「运行代码」。只有实际执行到的操作，才会出现在这里。','Choose Run code. Only operations that really execute appear here.');
 if(e.kind==='object-deleted')return b(`对象 ${e.args?.[0]} 已销毁。`,`Object ${e.args?.[0]} was destroyed.`);
 if(e.kind==='stdout')return b(`芯芯听到了输出：${e.text}`,`Chip heard the output: ${e.text}`);
 const a=e.args||[];
 if(e.kind==='set'||e.kind==='incr'||e.kind==='lappend')return b(`${a[1]} 现在是 ${e.result}`,`${a[1]} is now ${e.result}`);
 if(e.kind==='foreach'&&e.phase==='enter')return b(`开始遍历 ${e.argLists?.[2]?.length||0} 项；每一次实际累加都会触发动作。`,`Visiting ${e.argLists?.[2]?.length||0} items. Each actual accumulation triggers an action.`);
 if(e.kind==='call'||e.kind==='object'||e.kind==='class')return b(`${a[0]} 返回：${e.result||'（空值）'}`,`${a[0]} returned: ${e.result||'(empty)'}`);
 if(e.code!==0&&e.code!==2)return b(`执行遇到问题：${e.result}`,`Execution reported a problem: ${e.result}`);
 return b(`${a[0]||e.kind} 已执行${e.result?`，结果是 ${e.result}`:''}`,`${a[0]||e.kind} executed${e.result?`; result: ${e.result}`:''}`);
}
export function mountRuntime(root,lesson,storyboard,snapshot,{onAction=()=>{}}={}){
 clearRuntime();
 const abort=new AbortController(),on=(el,type,fn)=>el.addEventListener(type,fn,{signal:abort.signal});
 let model=createRuntimeModel(lesson.id),probe=createRuntimeModel(lesson.id),history=[],cursor=0,paused=false,timer=null,finished=false,outcome=null,validation=null,dirty=false,callbacks=[];
 let motion=true;try{motion=localStorage.getItem('tcl-quest-motion')!=='off';}catch{}
 motion=motion&&!matchMedia('(prefers-reduced-motion: reduce)').matches;
 root.innerHTML=`<section class="runtime-stage ${motion?'':'still'}" aria-labelledby="runtime-title"><header><div><span class="runtime-kicker">${b('EXECUTION → STORY · 真实执行驱动','EXECUTION → STORY · Real execution')}</span><h3 id="runtime-title">${b('芯芯的实时剧情窗','Chip’s Live Story Window')}</h3></div><span class="runtime-validation">${b('运行后自动推进','Advances when code runs')}</span></header><div class="runtime-canvas"></div><div class="runtime-beats" aria-label="${b('实时剧情进度','Live story progress')}">${storyboard.steps.map((beat,i)=>`<span data-runtime-beat="${i}"><b>${i+1}</b>${esc(beat.title)}</span>`).join('')}</div><div class="runtime-narration"><span class="runtime-speaker">${esc(t(CAST[lesson.world+1].name))}</span><p class="runtime-description" role="status"></p><details class="runtime-details"><summary>${b('查看运行记录和变量','Show execution record and variables')}</summary><pre class="runtime-command" data-verbatim></pre><div class="runtime-vars"></div><p class="runtime-note">${b('这是实际执行轨迹的动画回放；编辑代码后请重新运行。XP 只由「提交挑战」检查决定。','This animation replays real execution events. Run again after editing. Only Check mission can award XP.')}</p></details></div><div class="runtime-controls"><button class="secondary runtime-pause">${b('Ⅱ 暂停推进','Ⅱ Pause story')}</button><button class="secondary runtime-next">${b('下一步 →','Next step →')}</button><button class="secondary runtime-replay">${b('↺ 回放运行','↺ Replay run')}</button><button class="secondary runtime-last">${b('快进到最后','Jump to end')}</button><span class="runtime-position"></span></div><div class="runtime-warning" hidden></div></section>`;
 const el=root.querySelector('.runtime-stage'),q=s=>el.querySelector(s);
 function render(animate=true){
  const p={...model.props};
  // Keep small teaching canvases readable. The event text and output remain available.
  if(p.items)p.items=p.items.slice(0,6);if(p.rows)p.rows=p.rows.slice(0,3);if(p.lines)p.lines=p.lines.slice(-3);
  q('.runtime-canvas').innerHTML=sceneSVG(lesson.id,lesson.world,p,model.step,validation==='passed'?'success':'ready',animate&&motion);
  q('.runtime-description').textContent=dirty?b('草稿已修改；画面保留上次实际运行，请重新运行以更新。','Draft changed. This shows the last actual run; run again to update it.'):describe(model.lastEvent);
  q('.runtime-command').textContent=model.lastEvent?(model.lastEvent.kind==='stdout'?`puts → ${model.lastEvent.text}`:model.lastEvent.command):b('等待执行事件…','Waiting for execution events…');
  q('.runtime-vars').innerHTML=model.changed.map(x=>`<span><code>${esc(x.name)}</code><b data-verbatim>${esc(x.value.length>60?x.value.slice(0,60)+'…':x.value)}</b></span>`).join('');
  el.querySelectorAll('[data-runtime-beat]').forEach(x=>{x.classList.toggle('active',+x.dataset.runtimeBeat===model.step);x.classList.toggle('seen',+x.dataset.runtimeBeat<model.step);});
  q('.runtime-pause').textContent=paused?b('▶ 继续推进','▶ Resume story'):b('Ⅱ 暂停推进','Ⅱ Pause story');
  q('.runtime-pause').disabled=cursor>=history.length&&finished;
  q('.runtime-next').disabled=cursor>=history.length;
  q('.runtime-replay').disabled=!history.length;
  q('.runtime-last').disabled=cursor>=history.length;
  q('.runtime-position').textContent=`${cursor} / ${history.length}`;
  el.dataset.status=dirty?'edited':validation==='passed'?'passed':outcome?.error?'error':finished&&cursor>=history.length?'done':'playing';
  q('.runtime-validation').textContent=validation==='passed'?b('✓ 任务检查通过','✓ Mission checks passed'):validation==='failed'?b('仍有检查未通过','Some checks still fail'):dirty?b('请重新运行','Run again'):finished&&cursor>=history.length?b('回放完成 · 尚未代表通关','Replay complete · Check to earn XP'):finished?paused?b('执行完成 · 回放已暂停','Finished · Replay paused'):b('执行完成 · 正在回放','Finished · Replaying'):b('运行驱动自动推进','Advances from execution');
  localize(el);
 }
 function idle(){if(finished&&cursor>=history.length){clearTimeout(timer);timer=null;const done=callbacks;callbacks=[];done.forEach(fn=>fn());}}
 function next(){
  if(cursor>=history.length){idle();return;}
  const before=structuredClone(model.props),oldStep=model.step,event=history[cursor++];
  advanceRuntime(model,event);render();
  const cue=runtimeActionSound(lesson.id,before,model.props,event,oldStep,model.step);
  el.dataset.soundCue=cue||'';el.dataset.soundCursor=String(cursor);
  if(cue&&!document.hidden)onAction(cue);
  idle();
 }
 function schedule(){
  if(timer||paused||dirty||cursor>=history.length)return;
  timer=setTimeout(()=>{timer=null;next();schedule();},Math.max(70,520-Math.max(0,history.length-cursor-8)*20));
 }
 function pause(){onAction(null);paused=true;clearTimeout(timer);timer=null;render(false);}
 on(q('.runtime-pause'),'click',()=>{onAction(null);paused=!paused;clearTimeout(timer);timer=null;render(false);if(!paused)schedule();});
 on(q('.runtime-next'),'click',()=>{onAction(null);paused=true;clearTimeout(timer);timer=null;next();});
 on(q('.runtime-replay'),'click',()=>{onAction(null);clearTimeout(timer);timer=null;model=createRuntimeModel(lesson.id);cursor=0;paused=false;dirty=false;render();schedule();});
 on(q('.runtime-last'),'click',()=>{onAction(null);el.dataset.soundCue='';clearTimeout(timer);timer=null;while(cursor<history.length)advanceRuntime(model,history[cursor++]);render(false);idle();});
 on(document,'visibilitychange',()=>{if(document.hidden)pause();});
 live={
  destroy(){onAction(null);clearTimeout(timer);callbacks=[];abort.abort();},
  snapshot(){return {lesson:lesson.id,history,cursor,paused,finished,outcome,validation,dirty};},
  start(){onAction(null);el.dataset.soundCue='';clearTimeout(timer);timer=null;model=createRuntimeModel(lesson.id);probe=createRuntimeModel(lesson.id);history=[];cursor=0;paused=false;finished=false;outcome=null;validation=null;dirty=false;callbacks=[];q('.runtime-warning').hidden=true;render();el.closest('.lab')?.scrollIntoView({block:'start'});},
  push(event){
   const changed=advanceRuntime(probe,event);
   if(changed||['set','incr','lappend','open','gets','call','class','object','object-deleted','error'].includes(event.kind)||event.kind==='stdout'){
    history.push(event);render(false);schedule();
   }
  },
  finish(event){
   if(event.traceLimit){q('.runtime-warning').hidden=false;q('.runtime-warning').textContent=b('运行较长：最多记录 256 个执行事件；数组和列表只绘制部分项目。完整结果见输出区。','Long run: at most 256 execution events are recorded. Lists are drawn in part; see the output for the complete result.');}
   if(event.unavailable){q('.runtime-warning').hidden=false;q('.runtime-warning').textContent=b('执行追踪不可用；代码仍会正常运行，但本次不推进剧情。','Execution tracing is unavailable. The code still runs, but this run cannot advance the story.');}
   if(event.validation)validation=event.validation;
   if(event.done){finished=true;outcome=event;}
   render(false);schedule();idle();
  },
  edited(){if(!history.length&&!finished)return;onAction(null);dirty=true;paused=true;clearTimeout(timer);timer=null;render(false);},
  after(fn){if(finished&&cursor>=history.length)fn();else callbacks.push(fn);}
 };
 if(snapshot?.lesson===lesson.id){history=snapshot.history;cursor=0;for(const e of history)advanceRuntime(probe,e);while(cursor<snapshot.cursor)advanceRuntime(model,history[cursor++]);paused=snapshot.paused;finished=snapshot.finished;outcome=snapshot.outcome;validation=snapshot.validation;dirty=snapshot.dirty;}
 render(false);schedule();
}
